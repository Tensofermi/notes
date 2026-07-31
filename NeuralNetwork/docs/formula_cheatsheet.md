# 工程公式速查

这页不再整理某个具体模型或 NNQS 项目的公式，而是汇总神经网络工程里最常用的估算公式。它的用途是快速回答：

```text
显存够不够
通信量大不大
训练吞吐是否合理
推理 KV cache 会不会爆
量化以后能省多少
```

这些公式都是工程估算。真实系统还会有 allocator 碎片、临时 workspace、kernel 实现、padding、并行策略和框架开销。

## 参数量

线性层参数量：

$$
\text{params}
= d_{\rm in}d_{\rm out} + d_{\rm out}.
$$

如果忽略 bias：

$$
\text{params}
\approx d_{\rm in}d_{\rm out}.
$$

Embedding 参数量：

$$
\text{params}_{\rm emb}
= |\mathcal V| d_{\rm model}.
$$

LM head 若不和 embedding 共享权重：

$$
\text{params}_{\rm lm}
= d_{\rm model}|\mathcal V|.
$$

若使用 weight tying，则通常令：

$$
W_{\rm lm}=W_{\rm emb}^T,
$$

可以少存一份输出分类矩阵。

## Transformer Block 粗略参数量

对标准 decoder block，设 hidden size 为 $d$，MLP 中间维度为 $d_{\rm ff}$。

Attention 中 Q、K、V、O 四个投影约为：

$$
\text{params}_{\rm attn}
\approx 4d^2.
$$

MLP 若是两层：

$$
\text{params}_{\rm mlp}
\approx 2dd_{\rm ff}.
$$

若 $d_{\rm ff}=4d$，则：

$$
\text{params}_{\rm mlp}
\approx 8d^2.
$$

所以一个 block 粗略为：

$$
\text{params}_{\rm block}
\approx 12d^2.
$$

这就是很多 decoder-only 模型参数量估算的起点。

## Dtype 字节数

常见 dtype 的单元素字节数：

| dtype | bytes |
| --- | ---: |
| FP64 | 8 |
| FP32 | 4 |
| TF32 | 存储通常仍按 FP32 看 |
| FP16 | 2 |
| BF16 | 2 |
| FP8 | 1 |
| INT8 | 1 |
| INT4 | 0.5 |

显存估算的基本公式是：

$$
\text{bytes}
= \text{num\_elements}\times \text{bytes\_per\_element}.
$$

注意厂商显存容量常按 GB 标注，而程序里常看到 GiB：

$$
1\ {\rm GB}=10^9\ {\rm bytes},
\qquad
1\ {\rm GiB}=2^{30}\ {\rm bytes}.
$$

## 推理权重显存

只考虑模型权重：

$$
\text{weight memory}
\approx
P\times \text{bytes\_per\_param},
$$

其中 $P$ 是参数量。

例如 7B 参数模型：

| dtype | 权重显存粗略值 |
| --- | ---: |
| FP32 | $7\times10^9\times4\approx 28$ GB |
| FP16 / BF16 | $7\times10^9\times2\approx 14$ GB |
| INT8 | $7\times10^9\times1\approx 7$ GB |
| INT4 | $7\times10^9\times0.5\approx 3.5$ GB |

真实推理还要加：

```text
KV cache
  + runtime buffers
  + temporary workspace
  + CUDA context / allocator overhead
```

## 训练显存

训练显存通常远大于推理显存，因为要存：

```text
weights
  + gradients
  + optimizer states
  + activations
  + temporary buffers
```

若用 AdamW，FP32 master weights + gradients + 一阶动量 + 二阶动量的粗略成本可能达到：

$$
\text{memory per param}
\approx
2\ {\rm bytes}
+2\ {\rm bytes}
+4\ {\rm bytes}
+4\ {\rm bytes}
+4\ {\rm bytes}
=16\ {\rm bytes},
$$

这里假设前向权重是 FP16/BF16，优化器状态以 FP32 保存。不同框架和 ZeRO/FSDP 策略会改变这个数。

所以粗略估算：

$$
\text{training state memory}
\approx 16P\ {\rm bytes}
$$

再加 activation。

## Activation 显存

activation 显存和 batch、sequence length、hidden size、层数有关：

$$
\text{activation elements}
\propto
B\times N\times d\times L.
$$

粗略写作：

$$
\text{activation memory}
\approx
c_{\rm act} B N d L
\times \text{bytes\_per\_element},
$$

其中 $c_{\rm act}$ 取决于具体实现：是否保存 attention 中间量、是否使用 activation checkpointing、是否使用 FlashAttention。

降低 activation 显存的常见方法：

| 方法 | 代价 |
| --- | --- |
| 减小 batch size | 吞吐下降 |
| 减小 sequence length | 上下文变短 |
| gradient accumulation | 单步变慢，但有效 batch 可保持 |
| activation checkpointing | 反向时重算 forward，算力开销增加 |
| FlashAttention | 减少 attention 中间显存 |

## KV Cache 显存

自回归推理中，每层要缓存 K 和 V。

设：

- $L$：层数。
- $B$：并发序列数。
- $N$：每条序列上下文长度。
- $d_{\rm kv}$：每层 K 或 V 的总 hidden 维度。
- $s$：每个元素字节数。

则：

$$
\text{KV bytes}
=
2 L B N d_{\rm kv} s.
$$

如果是 MHA，通常：

$$
d_{\rm kv}=n_h d_h=d_{\rm model}.
$$

如果是 MQA / GQA，K/V head 数小于 query head 数：

$$
d_{\rm kv}=n_{\rm kv}d_h,
\qquad
n_{\rm kv}<n_h.
$$

因此 GQA/MQA 能显著降低 KV cache 显存。

## Attention 复杂度

单头 self-attention 的打分矩阵：

$$
S=QK^T\in \mathbb R^{N\times N}.
$$

计算复杂度约为：

$$
O(N^2d_h),
$$

attention matrix 显存约为：

$$
O(N^2).
$$

多头合起来仍可粗略看作：

$$
O(N^2d_{\rm model}).
$$

这解释了为什么长上下文训练会很贵。序列长度翻倍时，attention 的核心开销通常接近四倍。

## MLP 复杂度

Transformer 中 MLP 的计算通常很重。

若中间维度为 $d_{\rm ff}$，单个 token 的两层 MLP 约为：

$$
2dd_{\rm ff}
$$

次乘加。对 batch 和序列：

$$
O(BNd d_{\rm ff}).
$$

当 $d_{\rm ff}=4d$ 时：

$$
O(8BNd^2).
$$

在很多 decoder-only 模型中，MLP 的 FLOPs 占比不低于 attention，尤其在上下文不太长时。

## 训练 FLOPs 粗估

常用粗估：

$$
\text{training FLOPs per token}
\approx 6P,
$$

其中 $P$ 是非 embedding 参数量。这个经验式把 forward、backward 和梯度计算粗略合在一起。

训练总 FLOPs：

$$
\text{total FLOPs}
\approx
6P T,
$$

其中 $T$ 是训练 token 数。

这是宏观估算，不适合替代 profiler。它适合回答：

```text
模型参数量和 token 数给定时，需要大约多少计算量？
```

## 推理 FLOPs 粗估

decode 阶段每生成一个 token，模型大致需要一次 forward。

粗略估计：

$$
\text{decode FLOPs per token}
\approx 2P.
$$

但真实延迟不只取决于 FLOPs。decode 可能受下面因素限制：

- KV cache 读写。
- batch 太小导致 Tensor Core 利用率低。
- kernel launch 开销。
- sampling 和服务调度。
- 多卡通信。

所以推理优化不能只盯参数量，还要看 batch、上下文长度、KV cache 和调度策略。

## 吞吐

训练吞吐常用：

$$
\text{tokens/sec}
=
{\text{global batch size}\times \text{sequence length}
\over
\text{step time}}.
$$

其中：

$$
\text{global batch size}
=
\text{micro batch}
\times
\text{data parallel size}
\times
\text{gradient accumulation steps}.
$$

推理吞吐常用：

$$
\text{output tokens/sec}
=
{\text{generated tokens}
\over
\text{wall time}}.
$$

服务系统还会拆成：

| 指标 | 含义 |
| --- | --- |
| TTFT | 首 token 延迟 |
| TPOT | 每个输出 token 平均延迟 |
| request throughput | 每秒完成多少请求 |
| token throughput | 每秒生成多少 token |

## 通信量粗估

Data Parallel 中，每步要同步梯度。若参数量为 $P$，梯度 dtype 为 $s$ bytes，则梯度总量约为：

$$
P s.
$$

All-reduce 的实际网络流量和算法、拓扑、GPU 数有关。ring all-reduce 下，每张卡通信量粗略为：

$$
2{n-1\over n}Ps,
$$

其中 $n$ 是 GPU 数。

Tensor Parallel 中，通信对象常常不是梯度，而是 activation。此时要根据被切分的矩阵维度估算 all-gather 或 reduce-scatter 的张量大小。

## 量化压缩比

从 FP16 到 INT8，权重理论上减半：

$$
{2\ \text{bytes}\over 1\ \text{byte}}=2.
$$

从 FP16 到 INT4，理论上四分之一：

$$
{2\ \text{bytes}\over 0.5\ \text{bytes}}=4.
$$

但实际显存不会完全按这个比例下降，因为还有：

- scale / zero-point。
- group metadata。
- KV cache。
- runtime buffer。
- 未量化层，例如 embedding、norm、lm head。

## 经验判断表

| 现象 | 优先估算 |
| --- | --- |
| 一加载模型就 OOM | 权重显存、量化、tensor parallel |
| prompt 长就 OOM | KV cache、attention 中间量、sequence length |
| 训练一 backward 就 OOM | activation、optimizer state、gradient accumulation |
| GPU 利用率低 | dataloader、kernel launch、batch size、通信等待 |
| decode 慢 | KV cache、batching、sampling、CUDA graph |
| 多卡扩展差 | all-reduce / all-gather 通信量、pipeline bubble |

## 关联阅读

- [大模型 Infra 全景：从硬件到服务](infra_overview.md)
- [工程导读：从模型代码到系统代码](code_walkthrough.md)
- [数值精度](numerical_precision.md)
- [KV Cache](Transformer/kv_cache.md)
- [数值精度、显存与推理优化题](interview/precision_inference.md)
