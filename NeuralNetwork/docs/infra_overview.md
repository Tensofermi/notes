# 大模型 Infra 全景：从硬件到服务

大模型工程不是“会写 PyTorch”就结束了。PyTorch 很重要，但它只是系统栈中间的一层。

更完整的图像是：

```text
硬件
  -> 驱动 / CUDA / ROCm / NCCL
  -> kernel / 通信库 / 编译器
  -> 深度学习框架
  -> 分布式训练和推理引擎
  -> 在线服务系统
```

也可以写成：

$$
\boxed{
\text{hardware}
\rightarrow
\text{runtime}
\rightarrow
\text{kernel}
\rightarrow
\text{framework}
\rightarrow
\text{engine}
\rightarrow
\text{service}
}
$$

PyTorch / TensorFlow / JAX / Keras 位于“深度学习框架层”。它们负责表达模型、自动微分、优化器和训练循环，但当模型大到需要多卡、多机、高吞吐服务时，真正的瓶颈往往出现在更低层或更高层。

## 为什么不能只靠原生 torch

研究代码里可以写：

```python
logits = model(input_ids)
loss = criterion(logits, labels)
loss.backward()
optimizer.step()
```

这段代码表达了训练的数学闭环，但它没有解决工业规模系统里的问题：

| 问题 | 为什么原生脚本不够 |
| --- | --- |
| Python 调度开销 | eager mode 下许多小算子反复从 Python 发起，GPU 可能在等 CPU 调度 |
| 显存管理 | 权重、activation、optimizer state、KV cache、临时 workspace 都要精细管理 |
| kernel 效率 | attention、LayerNorm、RMSNorm、MoE、量化 GEMM 需要 fused 或定制 kernel |
| 多卡通信 | all-reduce、all-gather、reduce-scatter、pipeline bubble 都会影响利用率 |
| 推理调度 | 请求长短不一，需要 continuous batching、prefill/decode 分离和 KV cache 管理 |
| 服务稳定性 | 线上还需要限流、监控、扩缩容、故障恢复、版本发布和成本控制 |

所以工业界常见路线是：

```text
PyTorch / JAX 写模型
  -> 分布式训练框架扩展到多卡多机
  -> 替换高性能 kernel
  -> 编译或导出图
  -> 推理引擎执行
  -> 服务系统对外提供 API
```

这不是“抛弃 PyTorch”，而是把 PyTorch 放回系统栈中正确的位置。

## 第一层：硬件

硬件层决定了上层优化的边界。以 GPU 为例，训练和推理最关心几类资源：

| 资源 | 作用 | 常见瓶颈 |
| --- | --- | --- |
| 算力单元 | 执行矩阵乘、卷积、attention 等计算 | Tensor Core 是否吃满 |
| HBM 显存 | 存权重、activation、KV cache、optimizer state | 显存容量和显存带宽 |
| 片上存储 | registers、shared memory、cache | 数据复用是否充分 |
| GPU 间互联 | NVLink、PCIe、InfiniBand 等 | 多卡通信带宽和延迟 |
| CPU 和主机内存 | 数据加载、调度、预处理、网络请求 | CPU 调度或数据管线拖慢 GPU |

大模型里最核心的算子通常是矩阵乘法：

$$
[B,N,d_{\rm model}]
\times
[d_{\rm model},d_{\rm ff}]
\rightarrow
[B,N,d_{\rm ff}].
$$

这类操作通常是 compute-bound，重点是把 Tensor Core 吃满。

但并不是所有操作都这样。LayerNorm、RMSNorm、softmax、mask、reshape、KV cache 读写常常更接近 memory-bound，瓶颈是数据搬运而不是浮点乘加。

所以 infra 的第一条判断是：

> 当前慢，是算不动，还是搬不动？

## 第二层：驱动、Runtime 和通信库

在框架和硬件之间，还有一层运行时系统：

| 层 | 作用 |
| --- | --- |
| GPU driver | 管理设备、上下文、内存和 kernel 执行 |
| CUDA / ROCm runtime | 提供 kernel launch、stream、event、memory API |
| cuBLAS / cuDNN | 高性能矩阵乘、卷积、常见深度学习算子 |
| NCCL / RCCL | 多 GPU 通信，支持 all-reduce、all-gather、broadcast 等 collective |

单卡训练主要关心 kernel 是否高效。多卡训练还要关心通信：

```text
forward / backward 计算
  -> 梯度或 activation 通信
  -> 等待其他 GPU
  -> optimizer 更新
```

当模型和 batch 足够大时，通信可能和计算一样重要。

常见 collective：

| 通信操作 | 直觉 | 常见场景 |
| --- | --- | --- |
| all-reduce | 所有卡求和后每张卡都拿到结果 | DDP 同步梯度 |
| all-gather | 每张卡收集所有卡的分片 | tensor parallel 拼激活或权重 |
| reduce-scatter | 先规约再把结果切片分给各卡 | ZeRO / FSDP 梯度和参数分片 |
| broadcast | 一张卡发给其他卡 | 初始化参数或同步状态 |

很多训练 infra 的核心工作，就是让计算和通信重叠，减少 GPU 空等。

## 第三层：Kernel 和算子融合

神经网络最终会落成一串 kernel：

```text
matmul
  -> bias add
  -> activation
  -> dropout
  -> residual add
  -> layernorm
```

如果每一步都是独立 kernel，就会出现大量 kernel launch 和中间 tensor 读写。kernel fusion 的目标是把多个小操作合成更少的 kernel：

```text
bias + activation
residual + dropout + layernorm
QK^T + mask + softmax + PV
RMSNorm + quantization
MoE routing + grouped GEMM
```

attention 是最典型的例子。标准 attention 写作：

$$
\operatorname{softmax}
\left(
{QK^T\over\sqrt{d_h}}+M
\right)V.
$$

如果直接生成完整 $N\times N$ attention matrix，长序列时显存和带宽压力很大。FlashAttention 类算法的核心思想，是用分块和在线 softmax 减少对 HBM 的读写，而不是改变 attention 的数学定义。

这说明底层优化常常不是“换模型”，而是：

> 保持数学等价，改变数据如何在 GPU 内存层级中流动。

常见 kernel 工具：

| 工具 | 定位 |
| --- | --- |
| CUDA C++ | 直接写 GPU kernel，控制最细 |
| Triton | 用 Python 风格写高性能 GPU kernel |
| CUTLASS | NVIDIA GEMM / kernel 模板库 |
| FlashAttention | 高效 attention kernel 方案 |
| cuBLASLt | 矩阵乘加、layout、epilogue 融合等 |

真正“魔改 torch”的很多工作，其实不是改 PyTorch 主仓，而是在 PyTorch 周围接入自定义 op、Triton kernel、CUDA extension 或替换 attention backend。

## 第四层：编译器和图优化

PyTorch 默认的 eager mode 很适合研究和调试，但性能上会有 Python 调度开销。PyTorch 2.x 引入的 `torch.compile` 是编译化路线的一部分。官方说明中，`torch.compile` 是可选能力，底层涉及 TorchDynamo、AOTAutograd、PrimTorch 和 TorchInductor；第一次运行通常需要编译，后续调用才更能体现加速。详见 [PyTorch 2.x 说明](https://pytorch.org/get-started/pytorch-2-x/) 和本站 [torch.compile 教程](pytorch/torch_compile.md)。

编译器做的事情可以理解为：

```text
Python / PyTorch 程序
  -> 图捕获
  -> 算子分解
  -> 图优化和融合
  -> backend 代码生成
  -> CPU / GPU 执行
```

常见编译或图优化工具：

| 工具 | 典型位置 |
| --- | --- |
| `torch.compile` / TorchInductor | PyTorch 内部训练或推理加速 |
| XLA | JAX / TensorFlow / TPU 生态常见 |
| TensorRT | NVIDIA 推理图优化和部署 |
| TensorRT-LLM | 面向 NVIDIA GPU 的 LLM 推理优化库 |
| ONNX Runtime | 跨框架推理 runtime |

编译器不保证总是更快。它最怕：

- 输入 shape 频繁变化。
- Python 控制流太复杂。
- 图中出现不支持的算子。
- 编译开销无法被重复调用摊薄。

所以工程实践中通常先保证 eager 代码正确，再进行 compile / export / engine build。

## 第五层：深度学习框架

这一层才是大多数人最熟悉的 PyTorch / TensorFlow / JAX / Keras。

| 框架 | 更像什么 | 常见优势 |
| --- | --- | --- |
| PyTorch | 动态模型开发语言 | 研究生态强、调试直接、开源 LLM 生态活跃 |
| TensorFlow | 框架加部署生态 | 工业存量和部署工具丰富 |
| JAX | 函数式数组和编译系统 | `jit`、`vmap`、`pmap`、TPU / XLA 生态强 |
| Keras 3 | 高层多后端 API | 官方说明其可面向 JAX、TensorFlow、PyTorch 等后端开发模型，见 [Keras 3](https://keras.io/keras_3/) |
| NumPy | CPU 数值数组基础 | 数据处理、分析、小规模数值计算 |

框架层负责：

- tensor 抽象。
- autograd。
- module / layer 组织。
- optimizer。
- dataloader。
- checkpoint。
- eager 调试体验。

但框架层本身不等于完整 infra。你可以用 PyTorch 表达：

```python
loss.backward()
optimizer.step()
```

但多机多卡怎么切模型、怎么通信、怎么容错、怎么把请求调度给 GPU，仍然需要更上层或更底层的系统。

## 第六层：分布式训练

训练 infra 的目标不是“能训练”，而是：

> 让大量 GPU 在长时间训练中尽量少空转、少 OOM、可恢复、可监控。

训练显存通常包括：

```text
weights
  + gradients
  + optimizer states
  + activations
  + temporary buffers
```

如果使用 AdamW，optimizer state 通常还要存一阶、二阶动量。训练显存远大于推理显存。

常见并行策略：

| 策略 | 切什么 | 解决什么 |
| --- | --- | --- |
| Data Parallel / DDP | 数据 batch | 扩大 batch，加速训练 |
| Tensor Parallel | 单层矩阵乘的权重或激活 | 单层太大放不下一张卡 |
| Pipeline Parallel | 不同层放到不同卡 | 模型层数太多 |
| FSDP / ZeRO | 参数、梯度、optimizer state 分片 | 降低每卡显存 |
| Sequence Parallel | sequence 维拆分 | 长上下文训练 |
| Expert Parallel | MoE expert 分布到多卡 | 稀疏专家模型 |

这些策略的代价不同：

- Data Parallel 通信梯度。
- Tensor Parallel 通信 activation。
- Pipeline Parallel 有 pipeline bubble。
- FSDP / ZeRO 需要频繁 gather / scatter 参数。
- Sequence Parallel 对 attention、norm 和 layout 有要求。

训练系统还要处理：

- 数据管线是否跟得上 GPU。
- checkpoint 保存和加载。
- 节点故障恢复。
- 混合精度和 loss scaling。
- 梯度裁剪、梯度累积。
- profiling 和性能回归定位。

所以训练 infra 的核心问题是：

```text
模型能不能放下
  -> GPU 利用率高不高
  -> 通信和计算能否重叠
  -> 训练中断后能否恢复
  -> 成本是否可控
```

## 第七层：推理引擎

推理 infra 和训练 infra 的目标不同。

训练关心吞吐和稳定收敛；推理还要关心用户请求：

| 指标 | 含义 |
| --- | --- |
| TTFT | time to first token，首 token 延迟 |
| TPOT | time per output token，生成阶段每 token 延迟 |
| throughput | tokens/s 或 requests/s |
| latency | 单个请求总等待时间 |
| concurrency | 同时服务多少请求 |
| cost/token | 单 token 成本 |

LLM 推理分成两个阶段：

```text
prefill: 处理 prompt，计算所有输入 token 的 KV
decode: 逐 token 生成，每步复用 KV cache
```

prefill 更像大矩阵并行计算，吞吐较高；decode 每次只生成一个新 token，更容易受 batch 调度、KV cache 读写和 kernel launch 影响。

KV cache 是推理显存大头之一：

$$
\text{KV bytes}
=
2\times L\times B\times N\times d_{\rm kv}
\times \text{bytes\_per\_element}.
$$

其中 $2$ 表示 K 和 V，$L$ 是层数，$B$ 是并发序列数，$N$ 是上下文长度，$d_{\rm kv}$ 是 K/V 总维度。

这也是为什么推理引擎不能只是 `model.generate()`。它需要解决：

- KV cache 分配和回收。
- 不同长度请求的 batching。
- prompt prefill 和 decode 的资源分配。
- prefix cache。
- speculative decoding。
- 量化权重和 KV cache。
- CUDA graph 或其他方式降低调度开销。

典型推理引擎：

| 工具 | 重点 |
| --- | --- |
| vLLM | LLM serving，文档列出 PagedAttention、prefix caching、quantization、online serving、parallelism 等功能 |
| TensorRT-LLM | NVIDIA GPU 上构建和执行优化后的 TensorRT engine；官方文档说明其提供 Python API、Python/C++ runtime，用于高效 LLM 推理 |
| SGLang | 面向 LLM / agent workload 的 serving 和运行时 |
| TGI | Hugging Face 生态的 text generation inference server |
| Triton Inference Server | 通用模型服务 runtime，不等同于 Triton kernel language |

vLLM 的关键思想之一是把 KV cache 管理做成类似分页内存。它不是重新发明模型结构，而是在 serving 层解决显存碎片、请求调度和吞吐问题。vLLM 文档中列出了 PagedAttention、prefix caching、online serving、quantization、并行部署等能力，见 [vLLM 文档](https://docs.vllm.ai/en/stable/index.html)。

TensorRT-LLM 则更贴近 NVIDIA 推理栈。NVIDIA 文档说明 TensorRT-LLM 用 Python API 定义 LLM 并构建包含推理优化的 TensorRT engines，同时提供 Python 和 C++ runtime 执行这些 engines，见 [NVIDIA TensorRT-LLM](https://docs.nvidia.com/tensorrt-llm/)。

## 第八层：在线服务系统

推理引擎再往上，就是服务系统：

```text
client
  -> API gateway
  -> scheduler
  -> inference workers
  -> GPU runtime
  -> metrics / logs / tracing
```

服务系统要处理的问题包括：

| 问题 | 说明 |
| --- | --- |
| 请求调度 | 哪些请求放进同一个 batch |
| 流式输出 | token 生成后边算边返回 |
| 限流和排队 | 高峰期避免系统被打爆 |
| 多租户隔离 | 不同用户、模型、优先级隔离 |
| 灰度发布 | 新模型逐步放量 |
| 监控告警 | GPU 利用率、OOM、延迟、错误率 |
| 成本控制 | token 成本、空闲 GPU、cache 命中率 |

这层已经接近传统后端 / SRE / MLOps，但 LLM 服务有自己的特殊性：

- 请求长度差异极大。
- decode 是逐 token 串行过程。
- KV cache 会长期占用显存。
- batch 越大吞吐越高，但延迟可能变差。
- 用户感知强烈依赖首 token 延迟和流式稳定性。

## 训练 Infra 和推理 Infra 的区别

两条路线要分开看。

训练 infra 关心：

```text
多机多卡训练
  -> 并行策略
  -> 数据管线
  -> checkpoint
  -> 容错
  -> 通信优化
  -> 长时间稳定运行
```

推理 infra 关心：

```text
低延迟
  -> 高吞吐
  -> KV cache
  -> continuous batching
  -> quantization
  -> 服务稳定性
  -> 成本 / token
```

同样是 GPU，训练和推理的瓶颈经常不同：

| 维度 | 训练 | 推理 |
| --- | --- | --- |
| 参数 | 更新 | 固定 |
| 反向传播 | 需要 | 不需要 |
| optimizer state | 需要 | 不需要 |
| activation 保存 | 反向传播需要 | 通常不需要 |
| KV cache | 训练通常不缓存全部历史 | 自回归推理核心显存项 |
| 目标 | 收敛和吞吐 | 延迟、吞吐和成本 |
| 典型工具 | FSDP、DeepSpeed、Megatron、NeMo | vLLM、TensorRT-LLM、SGLang、TGI |

## 大模型一次请求怎么穿过系统

以在线 LLM 推理为例：

```text
用户请求
  -> API server 接收 prompt
  -> tokenizer 转成 input_ids
  -> scheduler 合并多个请求
  -> prefill 计算 prompt KV cache
  -> decode 逐 token 生成
  -> sampling 选择下一个 token
  -> detokenizer 转回文本
  -> streaming 返回给用户
```

背后对应的底层动作是：

```text
GPU 分配 KV cache
  -> kernel 执行 attention / MLP / norm
  -> 读写 HBM
  -> 可能跨 GPU 通信
  -> scheduler 插入新请求或移除完成请求
```

所以从 infra 角度看，一个 token 不是“模型吐出来的”，而是：

> 一次调度、一次或多次 kernel 执行、一次 KV cache 读写、一组采样逻辑和一次网络返回共同产生的结果。

## 常见岗位方向

大模型 infra 常见方向可以粗略分成四类。

| 方向 | 主要问题 | 需要的能力 |
| --- | --- | --- |
| 训练系统 | 多机多卡训练效率、稳定性、checkpoint | PyTorch、分布式、NCCL、性能分析 |
| 推理系统 | serving、batching、KV cache、延迟吞吐 | LLM 推理、调度、GPU runtime、后端系统 |
| Kernel / 编译器 | 自定义算子、fusion、量化 kernel | CUDA / Triton、编译器、矩阵计算 |
| 平台 / MLOps | 部署、监控、资源调度、成本治理 | Kubernetes、Ray、服务治理、可观测性 |

对应到学习路线：

```text
PyTorch 基础
  -> 数值精度和显存
  -> Transformer / KV cache
  -> torch.compile
  -> 分布式训练
  -> 推理引擎
  -> 服务系统
```

## 如何使用本章

工程导读这一组页面的目标，是把神经网络从“模型公式”放回“系统执行”里看。

| 页面 | 重点问题 |
| --- | --- |
| [从模型代码到系统代码](code_walkthrough.md) | 一个大模型工程仓库通常如何拆层 |
| [工程公式速查](formula_cheatsheet.md) | 参数量、显存、KV cache、FLOPs、吞吐如何估算 |
| [工程正确性与性能验证](verification.md) | 从单元测试到分布式、推理和服务压测如何验证 |
| [数值精度](numerical_precision.md) | FP32、FP16、BF16、量化和数值稳定性 |
| [KV Cache](Transformer/kv_cache.md) | 自回归推理为什么需要缓存，以及缓存如何占显存 |

也就是说，工程导读不是背工具名，而是建立这个判断：

> 当前瓶颈在数学、框架、kernel、通信、显存、调度，还是服务？

## 最简总结

大模型 infra 包括 PyTorch，但远远不止 PyTorch。

可以这样压缩：

```text
PyTorch 是模型表达和训练开发语言。
CUDA / kernel / compiler 决定单机执行效率。
NCCL / FSDP / ZeRO / tensor parallel 决定多卡训练效率。
vLLM / TensorRT-LLM / SGLang 决定推理吞吐、延迟和 KV cache 管理。
服务系统决定线上稳定性、扩缩容、监控和成本。
```

所以“不能直接用 torch，总得魔改一下”的本质是：

$$
\boxed{
\text{模型规模一上来，瓶颈就不只在公式，而在整个系统栈。}
}
$$

## 关联阅读

- [PyTorch 教程](pytorch/tensor_shape_dtype_device.md)
- [torch.compile：从 eager mode 到编译加速](pytorch/torch_compile.md)
- [数值精度](numerical_precision.md)
- [KV Cache](Transformer/kv_cache.md)
- [数值精度、显存与推理优化题](interview/precision_inference.md)
- [PyTorch 与工程实现题](interview/pytorch_engineering.md)
