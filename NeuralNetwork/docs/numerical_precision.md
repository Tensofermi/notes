# 数值精度：从 FP32、FP64 到混合精度

训练神经网络时，经常会看到这些词：

```text
FP64, FP32, TF32, FP16, BF16, FP8, INT8, INT4
```

它们都在回答同一个问题：

> 模型里的权重、激活值、梯度、logits 和中间矩阵乘法结果，到底用多少 bit 来表示？

数值精度不是一个只和硬件有关的小细节。它会影响：

- 显存占用。
- 训练速度。
- 推理速度。
- 梯度是否稳定。
- softmax、LayerNorm、loss 是否容易出现 `nan` 或 `inf`。
- 科学计算任务中能量、概率、期望值的可靠性。

这篇从最基础的浮点数讲起，然后再回到神经网络训练和推理。

## 一句话地图

先记住下面这张表：

| 精度 | 一句话 |
| --- | --- |
| FP64 | 很准但慢，科学计算常用，普通深度学习较少用。 |
| FP32 | 稳妥默认值，经典神经网络训练常用。 |
| TF32 | NVIDIA GPU 上加速 FP32 矩阵乘法的内部格式。 |
| FP16 | 快、省显存，但动态范围窄，训练要小心梯度下溢。 |
| BF16 | 范围接近 FP32，精度较粗，大模型训练常用。 |
| FP8 | 更激进的新低精度格式，主要用于更大规模训练或推理。 |
| INT8 / INT4 | 整数量化，主要用于推理部署。 |

如果只想先建立直觉，可以这样理解：

```text
FP64: 科学计算模式
FP32: 稳妥训练模式
BF16: 大模型训练常用模式
FP16: 快，但更挑数值稳定性
INT8/INT4: 推理压缩模式
```

## 计算机怎样表示小数

计算机不能无限精确地保存实数。比如数学里的：

$$
{1\over 3}=0.333333333\ldots
$$

小数位无限长，不可能完整存进有限 bit 里。

所以计算机只能近似表示它：

```text
0.33333334
```

或者：

```text
0.3333333333333333
```

保存得越细，需要的 bit 越多，计算和存储代价也越高。

神经网络里大量数值都是小数：

- weight。
- bias。
- activation。
- gradient。
- attention score。
- probability。
- loss。
- optimizer state。

因此精度选择会直接影响训练和推理。

## 浮点数的结构

浮点数类似二进制科学计数法：

$$
x=(-1)^s\times m\times 2^e.
$$

其中：

- $s$：sign bit，表示正负。
- $e$：exponent，指数，控制数值范围。
- $m$：mantissa 或 significand，尾数，控制有效数字精度。

可以把它理解成：

```text
符号位: 这个数是正还是负
指数位: 小数点大概应该放在哪里
尾数位: 小数点附近的有效数字有多细
```

所以浮点数有两个核心能力：

| 能力 | 主要由谁决定 | 含义 |
| --- | --- | --- |
| 动态范围 | exponent bits | 能表示多大或多小的数。 |
| 有效精度 | mantissa bits | 相近的两个数能分得多细。 |

这两个能力不一样。一个格式可以范围很大但小数粗，也可以小数较细但范围较窄。

`FP16` 和 `BF16` 的区别正好体现了这一点。

## 常见格式对比

| 格式 | 总 bit | 指数位 | 尾数位 | 大概有效十进制位数 | 常见用途 |
| --- | ---: | ---: | ---: | ---: | --- |
| FP64 | 64 | 11 | 52 | 15-16 | 高精度科学计算、数值验证。 |
| FP32 | 32 | 8 | 23 | 6-7 | 经典训练、稳定基准。 |
| TF32 | 约 19 | 8 | 10 | 约 3 | NVIDIA Tensor Core 加速矩阵乘法。 |
| FP16 | 16 | 5 | 10 | 3-4 | 混合精度训练、推理。 |
| BF16 | 16 | 8 | 7 | 2-3 | 大模型训练、稳定低精度训练。 |
| FP8 | 8 | 4 或 5 | 2 或 3 | 很低 | 新一代低精度训练/推理。 |
| INT8 | 8 | 无 | 无 | 量化整数 | 推理部署。 |
| INT4 | 4 | 无 | 无 | 更粗量化 | 大模型权重压缩。 |

表里最重要的是两列：指数位和尾数位。

指数位越多，越不容易 overflow 或 underflow。尾数位越多，越能保留小差异。

## 三个常见数值问题

低精度不是单纯“不准一点”。它可能产生三类问题。

### Rounding Error

浮点数只能保存有限有效数字，所以很多运算结果会被舍入。

例如真实结果是：

```text
1.23456789
```

低精度里可能只能保存成：

```text
1.235
```

单次误差不大，但神经网络里会做大量矩阵乘法和累加：

$$
y=\sum_{i=1}^d a_i b_i.
$$

如果 $d$ 很大，误差会不断积累。

### Overflow

如果数太大，超过当前格式能表示的最大值，就会变成：

```text
inf
```

例如 softmax 里有指数：

$$
e^x.
$$

当 $x$ 很大时，$e^x$ 很容易爆掉。

### Underflow

如果数太小，小到当前格式分辨不出来，就可能变成：

```text
0
```

训练中梯度经常很小。如果梯度被低精度舍入成 0，参数就无法正确更新。

这就是 FP16 训练里常说的 gradient underflow。

## FP32：稳妥默认值

`FP32` 是单精度浮点数：

```text
1 sign bit + 8 exponent bits + 23 mantissa bits
```

它在深度学习中长期作为默认训练精度，原因很简单：够稳。

FP32 的优点：

- 动态范围较大。
- 有效数字较多。
- 大多数算子默认支持好。
- 训练时不容易莫名其妙出现数值问题。

如果你刚开始写一个模型，FP32 通常是最安全的基线。

```python
import torch

x = torch.randn(4, 8, dtype=torch.float32)
```

在 PyTorch 中，`torch.float32` 就是 FP32。

## FP64：科学计算里的高精度

`FP64` 是双精度浮点数：

```text
1 sign bit + 11 exponent bits + 52 mantissa bits
```

它比 FP32 精确很多，但代价也明显：

- 显存占用是 FP32 的 2 倍。
- 计算通常更慢。
- 很多消费级 GPU 的 FP64 吞吐很低。

普通深度学习很少需要 FP64，因为神经网络本身是近似模型，训练还包含随机初始化、mini-batch 噪声和优化误差。

但在科学计算中，FP64 仍然很重要。比如：

- 矩阵条件数很差。
- 求逆、对角化、积分或长时间演化。
- 能量差很小，需要分辨细微差别。
- VMC / NNQS 中想验证 FP32 结果是否可靠。

对神经网络量子态来说，可以把 FP64 看成一种“数值显微镜”：平时不一定全程使用，但在怀疑数值误差时很有用。

## FP16：快，但范围窄

`FP16` 是半精度浮点数：

```text
1 sign bit + 5 exponent bits + 10 mantissa bits
```

它的好处很直接：

- 权重和激活占用显存更少。
- 内存带宽压力更小。
- GPU Tensor Core 可以更快执行矩阵乘法。

但 FP16 的指数位只有 5 位，动态范围比较窄。最大有限值约为：

$$
65504.
$$

太大的数会变成 `inf`，太小的梯度可能变成 0。

所以 FP16 训练经常需要 loss scaling。

## Loss Scaling 是什么

假设原始 loss 是：

$$
\mathcal L.
$$

FP16 下反向传播得到的某些梯度可能非常小：

$$
10^{-8},\quad 10^{-10}.
$$

这些值可能在 FP16 中下溢为 0。

Loss scaling 的想法是：先把 loss 放大：

$$
\mathcal L' = S\mathcal L.
$$

这样反向传播时梯度也放大：

$$
\nabla_\theta \mathcal L'
=
S\nabla_\theta \mathcal L.
$$

等到真正更新参数前，再把梯度除回去：

$$
\nabla_\theta \mathcal L
=
{1\over S}\nabla_\theta \mathcal L'.
$$

这样可以避免小梯度在 FP16 中直接变成 0。

PyTorch 里典型 FP16 mixed precision 写法是：

```python
scaler = torch.cuda.amp.GradScaler()

for batch in loader:
    optimizer.zero_grad()

    with torch.autocast(device_type="cuda", dtype=torch.float16):
        loss = model(batch)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

这里 `GradScaler` 会自动调整 scaling factor，发现 `inf` 或 `nan` 时会跳过当前 step 并降低 scale。

## BF16：大模型训练常用

`BF16` 是 bfloat16：

```text
1 sign bit + 8 exponent bits + 7 mantissa bits
```

它和 FP16 一样只有 16 bit，但它把更多 bit 给了 exponent。

这意味着：

- BF16 的动态范围接近 FP32。
- BF16 的尾数精度比 FP16 更粗。

看起来很反直觉：BF16 小数更粗，为什么训练大模型反而常用它？

因为神经网络训练时，很多时候更怕的是范围不够，而不是每一位小数都非常精细。

FP16 容易遇到：

```text
数太大 -> inf
梯度太小 -> 0
```

BF16 保留了 FP32 的指数范围，所以训练通常更稳，也经常不需要 loss scaling。

典型 BF16 mixed precision：

```python
for batch in loader:
    optimizer.zero_grad()

    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        loss = model(batch)

    loss.backward()
    optimizer.step()
```

一句话：

> FP16 小数更细一点，但范围窄；BF16 小数粗一点，但范围大，训练更省心。

## TF32：写的是 FP32，算得更快

`TF32` 是 NVIDIA Ampere 及之后 GPU 上常见的矩阵乘法内部格式。

它通常不是你显式保存的 dtype。你代码里可能写的是：

```python
x = torch.randn(1024, 1024, dtype=torch.float32, device="cuda")
y = x @ x
```

但底层矩阵乘法可能用 TF32 Tensor Core 加速。

TF32 大致特点是：

- 指数范围接近 FP32。
- 尾数精度比 FP32 低。
- 矩阵乘法速度更快。

对普通神经网络训练来说，TF32 往往是一个不错的速度和精度折中。

但如果你在做非常敏感的数值实验，比如比较很小的能量差，可以考虑关掉 TF32 做对照：

```python
import torch

torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
```

也可以设置 FP32 matmul 的精度偏好：

```python
torch.set_float32_matmul_precision("highest")
```

## 混合精度训练

现代训练很少简单地说“全部用 FP16”或“全部用 BF16”。更常见的是 mixed precision。

一个常见组合是：

| 对象 | 常见精度 |
| --- | --- |
| 权重存储 | FP16 / BF16，有时保留 FP32 master weights。 |
| forward 激活 | FP16 / BF16。 |
| backward 梯度 | FP16 / BF16。 |
| 矩阵乘法累加 | FP32。 |
| LayerNorm / softmax | 常用 FP32 或内部做稳定化。 |
| Adam 的一阶、二阶动量 | 通常 FP32。 |
| loss 标量 | 通常 FP32。 |

为什么矩阵乘法累加常用 FP32？

因为点积是大量乘积相加：

$$
y=\sum_{i=1}^d a_i b_i.
$$

如果 $a_i$ 和 $b_i$ 用 FP16 存储，单个乘法误差也许可以接受。但上千项累加时，累加器太低精度就容易积累明显误差。

所以硬件和框架经常使用：

```text
low precision multiply + FP32 accumulate
```

这就是混合精度的核心精神：

> 大部分地方用低精度省显存、提速度；关键位置用高精度兜住数值稳定性。

## 推理时为什么可以更低精度

训练比推理更难降精度。

训练需要：

- 保存中间激活。
- 反向传播梯度。
- 更新优化器状态。
- 长时间迭代，误差会不断影响后续参数。

推理只做 forward：

```text
input -> model -> logits/probability
```

所以推理常用更低精度：

- FP16。
- BF16。
- INT8。
- INT4。

大语言模型部署时，INT8 或 INT4 权重量化很常见，因为它能显著降低显存。

例如一个 70B 参数模型，如果每个参数用 FP16：

$$
70\times 10^9 \times 2\ \text{bytes}
\approx
140\ \text{GB}.
$$

如果权重量化到 4 bit，理论权重存储约为：

$$
70\times 10^9 \times 0.5\ \text{bytes}
\approx
35\ \text{GB}.
$$

实际还要加上 scale、zero point、KV cache 和运行时开销，但量级差异已经很明显。

## INT8 量化的基本想法

INT8 不是浮点数，而是整数。它只能表示有限个离散值，例如有符号 INT8：

$$
-128,\ldots,127.
$$

量化的核心是用一个 scale 把浮点数映射到整数：

$$
x_{\rm fp}
\approx
s(q-z).
$$

其中：

- $q$：量化后的整数。
- $s$：scale。
- $z$：zero point。

最简单的理解是：

```text
浮点数区间 -> 切成 256 个格子 -> 用 INT8 格子编号近似原值
```

量化有不同粒度：

| 方式 | 含义 |
| --- | --- |
| per-tensor | 整个张量共用一个 scale。 |
| per-channel | 每个输出通道有自己的 scale。 |
| per-group | 每组权重有自己的 scale，大模型权重量化常见。 |

粒度越细，误差通常越小，但元数据和实现复杂度也更高。

## Softmax 为什么怕低精度

softmax 是：

$$
\mathrm{softmax}(x_i)
=
{e^{x_i}\over\sum_j e^{x_j}}.
$$

问题在于指数函数增长太快。若 $x_i$ 很大，$e^{x_i}$ 容易 overflow。

稳定实现通常会先减去最大值：

$$
\mathrm{softmax}(x_i)
=
{e^{x_i-\max_j x_j}
\over
\sum_k e^{x_k-\max_j x_j}}.
$$

这样最大输入变成 0，其它输入不大于 0，指数更安全。

Transformer 里 attention 也有 softmax：

$$
\mathrm{softmax}
\left(
{QK^{\mathsf T}\over\sqrt{d_h}} + M
\right).
$$

如果 attention score 精度太低，可能影响 attention weight，进而影响上下文混合。

## LayerNorm 为什么怕低精度

LayerNorm 要计算均值和方差：

$$
\mu={1\over d}\sum_{j=1}^d x_j,
$$

$$
\sigma^2={1\over d}\sum_{j=1}^d(x_j-\mu)^2.
$$

然后：

$$
\mathrm{LN}(x_j)
=
\gamma_j{x_j-\mu\over\sqrt{\sigma^2+\epsilon}}+\beta_j.
$$

这里有减法、平方、求和、开方、除法。低精度下，方差估计可能不稳，尤其当 $x_j$ 彼此很接近时，$x_j-\mu$ 会变成小数差。

所以很多实现会让 LayerNorm 的关键统计量使用 FP32，或者使用专门优化过的 kernel。

## Log Probability 和 NNQS 的额外敏感点

在 decoder-only 模型中，语言模型关心：

$$
\log P(t_i\mid t_{<i}).
$$

在 NNQS / VMC 中，还会把所有位置的 log probability 加起来：

$$
\log P_\theta(x)
=
\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

振幅部分常写成：

$$
\log A_\theta(x)
=
{1\over 2}\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

这类量有两个特点：

- 它们经常是很多项的和。
- 它们后面可能进入指数、复数相位或能量估计。

因此在 NNQS 中，下面这些地方尤其值得关注精度：

| 位置 | 风险 |
| --- | --- |
| log probability 累加 | 长序列时误差累积。 |
| $\exp(\log A)$ | log 值太大或太小会 overflow/underflow。 |
| local energy | connected states 之间的比值可能数值跨度大。 |
| energy mean | 大量样本加权平均，累加误差会影响最后能量。 |
| VMC gradient proxy | 复数、共轭、能量差和 log wavefunction 混在一起，更容易暴露数值问题。 |

这并不意味着 NNQS 必须全程 FP64。更实际的做法是：

- 模型 forward 可以尝试 FP32 或 BF16。
- 能量估计、重要统计量、对照实验可以用 FP64 或 FP32 检查。
- 如果训练曲线异常，先用高精度小规模 case 做 sanity check。

## 什么时候该用哪种精度

可以按下面的策略选择。

| 场景 | 建议 |
| --- | --- |
| 第一次实现新模型 | 先用 FP32。 |
| 训练速度慢、显存紧张 | 尝试 BF16 mixed precision。 |
| GPU 对 BF16 支持不好 | 尝试 FP16 + loss scaling。 |
| 大模型推理 | 尝试 FP16、BF16、INT8 或 INT4。 |
| 科学计算验证 | 用 FP64 做小规模对照。 |
| 经常出现 `nan` / `inf` | 回到 FP32，关掉 TF32/低精度，逐步定位。 |
| 结果和理论差一点但不确定原因 | 比较 FP32 与 FP64 小规模结果。 |

对大多数现代 GPU 训练，优先顺序可以是：

```text
BF16 mixed precision
  -> FP32 baseline
  -> FP16 + GradScaler
  -> FP64 debug / validation
```

## 常见 PyTorch 检查方式

查看张量 dtype：

```python
print(x.dtype)
```

创建不同精度张量：

```python
x32 = torch.randn(8, 8, dtype=torch.float32)
x64 = torch.randn(8, 8, dtype=torch.float64)
x16 = torch.randn(8, 8, dtype=torch.float16, device="cuda")
xbf = torch.randn(8, 8, dtype=torch.bfloat16, device="cuda")
```

把模型转成某种 dtype：

```python
model = model.to(torch.float32)
model = model.to(torch.bfloat16)
```

临时自动混合精度：

```python
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    out = model(x)
```

检查是否有非有限数：

```python
torch.isfinite(x).all()
```

定位 `nan` 或 `inf`：

```python
if not torch.isfinite(loss):
    print("loss is not finite", loss)
```

开启异常检测：

```python
torch.autograd.set_detect_anomaly(True)
```

这个会变慢，但调试反向传播里的 `nan` 很有用。

## 数值问题排查清单

如果训练突然炸了，可以按这个顺序查：

1. 先确认 loss、logits、gradient 是否有 `nan` 或 `inf`。
2. 临时切回 FP32，看问题是否消失。
3. 如果用 FP16，检查是否启用了 GradScaler。
4. 检查 learning rate 是否过大。
5. 检查 softmax 前的 logits 或 attention score 是否特别大。
6. 检查 LayerNorm 的方差是否接近 0。
7. 检查是否有除以很小数的操作。
8. 对 NNQS，检查 $\log \psi$、$\psi(x')/\psi(x)$、local energy 是否有限。
9. 小规模 case 用 FP64 跑一遍，对比 FP32。
10. 如果只在 GPU 上出问题，检查 TF32、mixed precision 和相关 fused kernel。

一个简单的训练日志应该至少关注：

```text
loss
grad_norm
max_abs_logit
learning_rate
是否出现 nan / inf
```

对 VMC / NNQS，还可以额外关注：

```text
energy_real
energy_imag
local_energy_real 的最大最小值
log_amp 的最大最小值
unique sample 数量
```

## 最短心智模型

数值精度可以这样理解：

```text
FP64: 更像数值分析工具
FP32: 稳定基准
BF16: 训练大模型时的实用折中
FP16: 更快更省，但需要照顾动态范围
INT8/INT4: 推理部署时的压缩工具
```

训练时，不要只问“能不能用低精度”。更好的问题是：

```text
哪些部分可以低精度？
哪些部分必须高精度？
出了 nan/inf 以后如何定位？
当前任务更怕精度不够，还是更怕动态范围不够？
```

神经网络能用低精度，是因为它对小的数值误差有一定鲁棒性；但归一化、softmax、长序列 log probability、能量估计、梯度累加和优化器状态，仍然需要更谨慎的精度处理。

## 招聘考点

!!! question "代表题：FP16 和 BF16 谁更容易溢出？"
    FP16 尾数相对更多，但指数位少，动态范围窄，更容易 overflow / underflow。BF16 指数位和 FP32 一样多，动态范围大，所以大模型训练中常比 FP16 更稳。完整题解见 [数值精度、显存与推理优化题](interview/precision_inference.md)。

!!! example "代表题：7B 参数 FP16 权重大约占多少显存？"
    只算权重时，$7\times10^9\times2$ bytes $=14$ GB，约 $13.0$ GiB。真实推理还要加 KV cache、activation、临时 buffer 等。完整题解见 [数值精度、显存与推理优化题](interview/precision_inference.md)。
