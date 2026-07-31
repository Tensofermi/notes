# 数值精度、显存与推理优化题

这类题很适合区分“只懂模型结构”和“能做工程落地”。回答时要把 dtype、字节数、显存来源、吞吐和延迟讲清楚。

如果想先建立从硬件、kernel、框架到推理服务的全局图像，可以先读 [大模型 Infra 全景：从硬件到服务](../infra_overview.md)。本页重点把其中的数值精度、显存和推理优化拆成代表题。

## 题目：FP32、FP16、BF16 的主要区别是什么？

**来源背景**：华为 / 字节大模型训练和推理工程题改写。

**考点定位**：浮点格式、动态范围、精度。

**先给结论**：

- FP32 稳定但占显存多。
- FP16 精度和范围都更小，容易 overflow / underflow。
- BF16 指数位和 FP32 一样多，动态范围大，更适合大模型训练。

**解题思路**：

| 格式 | 字节 | 特点 |
| --- | --- | --- |
| FP32 | 4 | 稳定基准 |
| FP16 | 2 | 快、省显存，但范围窄 |
| BF16 | 2 | 范围大，尾数少 |

大模型训练常用 BF16，因为梯度和激活的数值范围可能很宽。

**易错点**：

- BF16 不是比 FP16 更“精细”，它是动态范围更大。
- 低精度训练通常仍保留一些 FP32 状态，例如 optimizer state。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：为什么 FP16 训练需要 loss scaling？

**来源背景**：混合精度训练面试题改写。

**考点定位**：underflow、梯度缩放、反向传播。

**先给结论**：FP16 能表示的很小数有限，小梯度可能下溢为 0。loss scaling 先把 loss 放大，让梯度落在可表示范围内，更新前再缩回来。

**解题思路**：

若原 loss 为 $L$，缩放后：

$$
L'=sL.
$$

反向传播得到：

$$
g' = s g.
$$

optimizer 更新前再用：

$$
g={g'\over s}.
$$

**易错点**：

- loss scaling 不改变真实优化目标。
- 如果缩放太大导致 overflow，需要动态降低 scale。
- BF16 因为动态范围大，通常不需要同样程度的 loss scaling。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：一个 7B 参数模型用 FP16 权重大约占多少显存？

**来源背景**：大模型部署估算题改写。

**考点定位**：参数量、dtype、GB/GiB。

**先给结论**：只算权重：

$$
7\times10^9\times2\text{ bytes}=14\text{ GB}
\approx13.0\text{ GiB}.
$$

**解题思路**：

FP16 每个参数 2 bytes。显存估算先从权重开始，再加：

- KV cache。
- activation。
- framework workspace。
- CUDA kernel 临时 buffer。
- 如果训练，还要加梯度和 optimizer state。

**易错点**：

- 推理显存不等于权重显存。
- 训练显存远大于推理显存。
- GB 是 $10^9$ bytes，GiB 是 $2^{30}$ bytes。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：KV cache 显存怎么估算？

**来源背景**：大模型推理优化高频题改写。

**考点定位**：KV cache、序列长度、batch size、层数。

**先给结论**：

$$
\text{bytes}
=
2\times L\times B\times h\times N\times d_h
\times \text{bytes\_per\_element}.
$$

**解题思路**：

其中：

- $2$：K 和 V 两份。
- $L$：decoder 层数。
- $B$：batch size。
- $h$：head 数。
- $N$：上下文长度。
- $d_h$：每个 head 的维度。

因为 $h d_h=d_m$，也可以写成：

$$
2\times L\times B\times N\times d_m
\times \text{bytes\_per\_element}.
$$

**易错点**：

- KV cache 随上下文长度线性增长。
- 多用户并发时 batch 维也会增加。
- GQA / MQA 会减少 K/V head 数，显著降低 cache。

**关联阅读**：[KV Cache](../Transformer/kv_cache.md)、[大模型 Infra 全景](../infra_overview.md)。

## 题目：INT8 量化为什么能加速推理？

**来源背景**：模型部署和推理优化题改写。

**考点定位**：量化、内存带宽、矩阵乘法。

**先给结论**：INT8 把权重或激活从浮点数压缩到 8-bit，减少显存和内存带宽，并可利用硬件 INT8 矩阵乘加加速。

**解题思路**：

简单对称量化：

$$
x_q=\mathrm{round}\left({x\over s}\right),
\quad
x\approx s x_q.
$$

其中 $s$ 是 scale。

量化收益：

- 权重体积约为 FP32 的 1/4。
- 相比 FP16 也可约减半。
- 更少数据搬运通常提升吞吐。

**易错点**：

- 量化不一定总加速，取决于硬件和 kernel。
- 激活 outlier 会影响量化误差。
- 训练后量化和量化感知训练效果不同。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：吞吐和延迟有什么区别？

**来源背景**：线上推理系统面试题改写。

**考点定位**：系统指标、batching、服务优化。

**先给结论**：延迟是单个请求等待多久；吞吐是单位时间处理多少请求或 token。

**解题思路**：

- latency：用户等待时间。
- throughput：tokens/s 或 requests/s。

增大 batch 往往提高吞吐，但可能增加单请求延迟。LLM 服务常通过 continuous batching 平衡两者。

**易错点**：

- 只看 tokens/s 不够，交互式应用还要看首 token 延迟。
- batch 太大可能被 KV cache 或显存限制。

**关联阅读**：[KV Cache](../Transformer/kv_cache.md)。

## 题目：Softmax 为什么容易有数值问题？

**来源背景**：深度学习数值稳定题改写。

**考点定位**：指数溢出、log-sum-exp。

**先给结论**：softmax 需要计算指数，logit 很大时 $e^x$ 可能 overflow；通常先减最大值。

**解题思路**：

$$
\mathrm{softmax}(z_i)
=
{e^{z_i}\over\sum_j e^{z_j}}.
$$

令：

$$
m=\max_jz_j.
$$

则：

$$
{e^{z_i}\over\sum_j e^{z_j}}
=
{e^{z_i-m}\over\sum_j e^{z_j-m}}.
$$

数值更稳定。

**易错点**：

- 数学等价不代表数值实现等价。
- attention score、classification logits、language model logits 都可能遇到这个问题。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：推理时为什么可以用比训练更低的精度？

**来源背景**：模型部署面试题改写。

**考点定位**：训练 / 推理差异、梯度、鲁棒性。

**先给结论**：推理只做 forward，不需要保存反向传播中间量和 optimizer state，对小数值误差通常更鲁棒，因此可以更激进地使用低精度或量化。

**解题思路**：

训练需要：

- 参数。
- 激活。
- 梯度。
- optimizer state。

推理主要需要：

- 参数。
- 当前激活。
- KV cache。

所以推理更适合使用 FP16/BF16/INT8/INT4。

**易错点**：

- 低精度可能损害小模型、长上下文或数学推理任务。
- 量化前后需要评估任务指标。

**关联阅读**：[数值精度](../numerical_precision.md)。
