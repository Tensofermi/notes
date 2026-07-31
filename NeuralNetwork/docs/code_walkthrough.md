# 工程导读：从模型代码到系统代码

很多神经网络笔记容易停在两端：一端是数学公式，另一端是几行 PyTorch 训练循环。但真正的大模型工程在中间和上下两侧展开：

```text
模型定义
  -> 数据与 tokenizer
  -> 训练循环
  -> 分布式并行
  -> kernel / compiler 优化
  -> checkpoint 与评估
  -> 推理引擎
  -> 在线服务
```

这篇不再围绕某一个教学项目的文件名讲调用链，而是从大模型背景出发，说明工程代码通常如何分层、每层负责什么、读代码时应该抓哪些接口。

如果想先建立硬件到服务的系统栈图像，可以先读 [大模型 Infra 全景：从硬件到服务](infra_overview.md)。本页更关心“代码仓库里这些模块为什么这样拆”。

## 一份大模型工程代码通常在表达什么

一个成熟训练或推理仓库，表面上有很多目录，但核心问题一般只有四个：

| 问题 | 工程模块 |
| --- | --- |
| 模型是什么 | model、layers、attention、embedding、normalization |
| 数据怎么进来 | tokenizer、dataset、dataloader、packing、collator |
| 参数怎么更新或执行 | trainer、optimizer、scheduler、engine、runtime |
| 系统如何稳定运行 | checkpoint、evaluation、logging、profiling、serving、monitoring |

所以读工程代码时，不要从所有文件平铺开始。先找四条主线：

```text
输入如何变成 tensor
tensor 如何穿过模型
loss 或 logits 如何产生
训练或推理系统如何调度这次计算
```

## 模型层：把数学结构写成可组合模块

模型层负责表达网络结构。以 decoder-only Transformer 为例，常见拆分是：

```text
Embedding
  -> DecoderBlock x L
       -> Attention
       -> MLP
       -> Norm / residual
  -> Final Norm
  -> LM Head
```

代码上通常会对应：

```text
model.py
layers.py
attention.py
mlp.py
norm.py
positional_encoding.py
```

这一层的关键不是“能 forward”，而是每个模块都要明确：

- 输入 shape 是什么。
- 输出 shape 是什么。
- 参数 shape 是什么。
- dtype 和 device 是否跟随外部输入。
- 是否支持训练和推理两种路径。
- 是否支持 KV cache、mask、position id 等工程参数。

例如 attention 的核心数学式是：

$$
\operatorname{softmax}
\left(
{QK^T\over \sqrt{d_h}} + M
\right)V.
$$

工程代码里还会出现：

```text
attention_mask
position_ids
past_key_values
use_cache
is_causal
flash_attention_backend
```

这些不是数学公式之外的杂项，而是模型走向高效训练和推理时必须暴露的接口。

## 数据层：决定 GPU 是否吃得饱

训练代码里，模型本身经常不是唯一瓶颈。数据层如果太慢，GPU 会等 CPU。

语言模型训练的数据路径通常是：

```text
raw text
  -> tokenizer
  -> token ids
  -> sequence packing
  -> batch
  -> device transfer
  -> model input
```

常见模块：

| 模块 | 作用 |
| --- | --- |
| tokenizer | 文本和 token id 的互相转换 |
| dataset | 读取和组织样本 |
| collator | 把不同长度样本整理成 batch |
| packing | 把短文本拼成固定长度序列，提高 token 利用率 |
| dataloader | 多进程加载、prefetch、pin memory |

读这一层代码时重点看：

- batch 里的字段名是什么，例如 `input_ids`、`labels`、`attention_mask`。
- padding token 是否参与 loss。
- labels 是否相对 input 做了 shift。
- sequence packing 后样本边界如何处理。
- CPU 到 GPU 的拷贝是否成为瓶颈。

大模型训练通常按 token 计成本，不按“样本条数”计成本。一个 dataloader 是否高效，最终要看：

$$
\text{tokens/sec}
$$

而不是只看 batch size。

## 训练层：把 forward 变成可扩展的参数更新

单机 PyTorch 训练循环可以写得很短：

```python
logits = model(input_ids)
loss = criterion(logits, labels)
loss.backward()
optimizer.step()
optimizer.zero_grad()
```

但大模型训练代码会把这几行拆开，因为它要处理更多系统问题：

```text
forward
  -> loss scaling
  -> backward
  -> gradient accumulation
  -> gradient clipping
  -> distributed synchronization
  -> optimizer step
  -> lr scheduler step
  -> checkpoint
  -> evaluation
```

训练层常见配置包括：

| 配置 | 解决的问题 |
| --- | --- |
| `gradient_accumulation_steps` | 显存放不下大 batch 时累积梯度 |
| `mixed_precision` | 降低显存和提高 Tensor Core 利用率 |
| `max_grad_norm` | 控制梯度爆炸 |
| `warmup_steps` | 学习率预热，降低训练初期不稳定 |
| `checkpoint_interval` | 防止长时间训练中断后损失过大 |
| `eval_interval` | 检查模型是否真的在变好 |

读 trainer 时要判断一件事：

> 它是在表达算法，还是在管理系统状态？

很多训练框架中的 trainer，真正复杂的地方不是 loss，而是分布式、恢复、日志、混合精度和异常处理。

## 分布式层：模型太大以后代码会变形

当模型不能自然放进一张 GPU，工程代码会开始引入并行策略。

| 并行方式 | 代码变化 |
| --- | --- |
| Data Parallel | 每张卡一份模型，batch 切分，反向后同步梯度 |
| Tensor Parallel | 单层矩阵乘被切到多张卡，forward 内部出现通信 |
| Pipeline Parallel | 不同层在不同卡，代码要调度 micro-batch |
| FSDP / ZeRO | 参数、梯度、optimizer state 被分片，读写 checkpoint 更复杂 |
| Expert Parallel | MoE expert 分布在不同卡，routing 和通信成为核心 |

所以大模型仓库里经常会看到：

```text
parallel_state
process_group
rank
world_size
shard
gather
scatter
all_reduce
```

这些词说明代码已经不只是“神经网络结构”，而是在描述多设备上的张量布局。

读分布式代码时，最重要的是看清楚：

- 哪个维度被切分。
- 每张 GPU 持有什么张量分片。
- 什么时候需要通信。
- 通信后 shape 如何恢复。
- checkpoint 保存的是全量权重还是分片权重。

## Kernel 和编译层：让同一个数学式跑得更快

大模型性能优化经常不改变数学定义，只改变执行方式。

例如普通 attention 和 FlashAttention 都在算：

$$
\operatorname{softmax}
\left(
{QK^T\over\sqrt{d_h}} + M
\right)V,
$$

但后者通过分块和在线 softmax 减少 HBM 读写。

代码里常见开关：

```text
use_flash_attention
attn_implementation
torch.compile
cuda_graph
triton_kernel
fused_rmsnorm
fused_mlp
```

这些开关对应的问题是：

| 优化 | 主要收益 |
| --- | --- |
| kernel fusion | 减少 launch 和中间 tensor 读写 |
| `torch.compile` | 捕获图并做融合、代码生成 |
| CUDA graph | 降低重复推理时的 CPU launch 开销 |
| fused norm / activation | 改善 memory-bound 小算子 |
| optimized attention | 降低长序列 attention 的显存和带宽压力 |

判断这层优化是否有意义，不能只看单次运行时间。要区分：

- 首次编译开销。
- warmup 后稳定速度。
- 是否因 dynamic shape 频繁重新编译。
- 是否影响数值一致性。
- 是否只在特定 GPU 架构上有效。

## Checkpoint 层：保存的不只是参数

教学代码里，checkpoint 可能只是：

```python
torch.save(model.state_dict(), path)
```

大模型训练中，checkpoint 通常还需要保存：

```text
model weights
optimizer states
lr scheduler states
random states
gradient scaler states
data loader progress
distributed shard metadata
training config
```

原因很直接：训练可能跑几天、几周甚至更久，任意节点故障都不能从头开始。

读 checkpoint 代码时要看：

- 是否能从中断点严格恢复。
- 分布式 checkpoint 是每卡单独保存还是聚合保存。
- 保存频率是否会阻塞训练。
- 是否支持只加载模型权重做推理。
- 是否记录了 tokenizer、config、commit id 等复现实验需要的信息。

## 评估层：loss 下降不等于系统可用

训练工程里的 evaluation 不只是计算 validation loss。

常见评估包括：

| 类型 | 关注点 |
| --- | --- |
| loss / perplexity | 语言建模目标是否改善 |
| downstream benchmark | 任务能力是否改善 |
| numerical check | 是否出现 NaN、Inf、异常梯度 |
| throughput benchmark | tokens/sec 是否达标 |
| memory benchmark | 显存是否符合预期 |
| serving benchmark | 首 token 延迟、吞吐、并发能力 |

工程代码里如果只有 loss，没有吞吐、显存和稳定性指标，就很难判断它能否走向真实系统。

## 推理层：参数固定后，问题变成调度和缓存

推理代码和训练代码最大的区别是：

```text
训练：参数会更新，需要 backward 和 optimizer
推理：参数固定，需要低延迟、高吞吐、稳定服务
```

LLM 推理通常分成：

```text
prefill
  处理 prompt，生成初始 KV cache

decode
  每次生成一个新 token，复用历史 KV cache
```

代码里常见对象：

```text
request
sequence
block table
kv cache
scheduler
sampling params
logits processor
streamer
```

这里的核心不再是 `model.forward()` 本身，而是：

- 多个请求如何合 batch。
- 长短请求如何共享 GPU。
- KV cache 如何分配、回收和复用。
- 生成结束的请求如何从 batch 中移除。
- 新请求如何插入正在 decode 的批次。
- 如何平衡吞吐和延迟。

这就是 vLLM、TensorRT-LLM、SGLang、TGI 这类推理引擎要解决的问题。

## 服务层：模型变成产品以后还要过一层

在线系统会把模型能力包装成服务：

```text
HTTP / RPC request
  -> auth / rate limit
  -> tokenizer
  -> scheduler
  -> inference worker
  -> detokenizer
  -> streaming response
  -> logs / metrics / tracing
```

这层关心：

- 请求排队时间。
- 首 token 延迟。
- 生成中断和超时。
- OOM 后 worker 如何恢复。
- 多模型如何部署。
- 版本如何灰度。
- 用户输入输出如何记录和脱敏。
- 成本如何按 token 估算。

从这里开始，神经网络工程和后端系统、SRE、平台工程会明显交叉。

## 读一个大模型工程仓库的顺序

建议按下面顺序读，而不是从入口文件一路钻到底。

1. 先看 README 和配置文件，确认训练还是推理、单机还是分布式、目标硬件是什么。
2. 看模型配置：层数、hidden size、head 数、词表大小、上下文长度、dtype。
3. 看输入输出：batch 字段、shape、mask、labels、position ids。
4. 看模型 forward：attention、MLP、norm、residual、LM head、KV cache。
5. 看训练或推理主循环：谁调用 forward，什么时候 backward，什么时候 step。
6. 看分布式封装：张量在哪个维度切分，哪里发生通信。
7. 看 checkpoint：保存什么，如何恢复，是否和分布式策略绑定。
8. 看性能路径：是否用 FlashAttention、`torch.compile`、CUDA graph、量化或推理引擎。
9. 看验证脚本：如何证明正确、稳定、快。

## 最小心智模型

工程导读的目标不是记住所有工具，而是形成一张判断图：

```text
模型不收敛
  -> 先看数据、loss、优化器、精度、梯度

显存爆了
  -> 看参数、activation、optimizer state、KV cache、batch、sequence length

GPU 利用率低
  -> 看 dataloader、kernel 数量、通信等待、CPU 调度、batch 太小

推理延迟高
  -> 看 prefill/decode、KV cache、batching、kernel launch、网络和排队

线上不稳定
  -> 看 OOM 恢复、限流、监控、日志、版本和回滚
```

这就是从“会写模型”走向“能把模型跑成系统”的分界线。

## 关联阅读

- [大模型 Infra 全景：从硬件到服务](infra_overview.md)
- [工程公式速查](formula_cheatsheet.md)
- [工程正确性与性能验证](verification.md)
- [数值精度](numerical_precision.md)
- [KV Cache](Transformer/kv_cache.md)
- [torch.compile：从 eager mode 到编译加速](pytorch/torch_compile.md)
