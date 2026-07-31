# 常用 Tensor 操作：索引、gather、拼接、拆分与矩阵乘法

掌握 tensor 操作的重点不是记住所有 API，而是理解 shape 如何变化。

这一页覆盖写神经网络代码时最常见的操作：

- 索引和切片。
- `gather`：按 index 从指定维度取值。
- reshape / view。
- transpose / permute。
- unsqueeze / squeeze。
- cat / stack。
- chunk / split。
- matmul / bmm。
- broadcasting。
- inplace 操作的风险。

先记住一个判断标准：

> PyTorch API 看起来很多，但真正要盯住的是：输入 shape 是什么，操作沿哪个维度发生，输出 shape 变成什么。

## 索引和切片

```python
import torch

x = torch.arange(12).reshape(3, 4)
print(x)
print(x[0])
print(x[:, 1])
print(x[1:, 2:])
```

`x[0]` 取第 0 行，shape 从 $[3,4]$ 变成 $[4]$。  
`x[:,1]` 取所有行的第 1 列，shape 也是 $[3]$。

如果想保留维度，可以写：

```python
col = x[:, 1:2]
print(col.shape)
```

得到：

```text
torch.Size([3, 1])
```

## gather：按索引从指定维度取值

普通索引适合取固定位置。`torch.gather` 更适合这种场景：

> 每一行、每一个 batch、每一个 token 位置，都有不同的 index，要从同一个维度里取对应元素。

最常见例子是分类问题。假设模型输出：

```text
logits: [batch, n_classes]
labels: [batch]
```

我们想从每一行 logits 里取出真实标签对应的分数。

```python
import torch
import torch.nn.functional as F

logits = torch.tensor(
    [
        [2.0, 0.5, -1.0],
        [0.1, 3.0, 0.2],
    ]
)
labels = torch.tensor([0, 2])

logp_all = F.log_softmax(logits, dim=-1)
chosen = torch.gather(
    logp_all,
    dim=-1,
    index=labels.unsqueeze(-1),
)

print(logp_all.shape)
print(chosen.shape)
print(chosen)
```

输出 shape 是：

```text
torch.Size([2, 3])
torch.Size([2, 1])
```

这里：

```text
第 0 行取 class 0
第 1 行取 class 2
```

所以 `labels.unsqueeze(-1)` 很关键。`gather` 要求 `index` 和输出 shape 一致；你想每行取一个值，输出就是 `[batch, 1]`，因此 index 也要是 `[batch, 1]`。

## gather 的 shape 规则

`gather(input, dim, index)` 的核心规则是：

```text
沿 dim 维，根据 index 里的编号取 input 里的值。
输出 shape 和 index shape 相同。
```

例如：

```python
x = torch.tensor(
    [
        [10, 11, 12],
        [20, 21, 22],
    ]
)
idx = torch.tensor(
    [
        [2, 0],
        [1, 1],
    ]
)

y = torch.gather(x, dim=1, index=idx)
print(y)
print(y.shape)
```

输出：

```text
tensor([[12, 10],
        [21, 21]])
torch.Size([2, 2])
```

解释：

```text
y[0, 0] = x[0, idx[0, 0]] = x[0, 2] = 12
y[0, 1] = x[0, idx[0, 1]] = x[0, 0] = 10
y[1, 0] = x[1, idx[1, 0]] = x[1, 1] = 21
y[1, 1] = x[1, idx[1, 1]] = x[1, 1] = 21
```

注意 `dim=1` 表示“每一行内部按列索引取值”。如果改成 `dim=0`，含义就变成“每一列内部按行索引取值”。

## gather 在语言模型里的用法

语言模型或自回归模型里常见：

```text
logits: [batch, length, vocab_size]
tokens: [batch, length]
```

`logits[b, i, :]` 是第 $b$ 个样本、第 $i$ 个位置对整个词表的打分。训练时，我们经常想取真实 token 的 log probability：

$$
\log P_\theta(t_i\mid t_{<i}).
$$

代码是：

```python
B, N, V = 2, 4, 5
logits = torch.randn(B, N, V)
tokens = torch.randint(0, V, (B, N))

logp_all = F.log_softmax(logits, dim=-1)      # [B, N, V]
chosen = logp_all.gather(
    dim=-1,
    index=tokens.unsqueeze(-1),
).squeeze(-1)                                 # [B, N]

log_prob_sequence = chosen.sum(dim=-1)         # [B]
```

shape 变化：

```text
tokens:              [B, N]
tokens.unsqueeze(-1): [B, N, 1]
logp_all:            [B, N, V]
chosen before squeeze: [B, N, 1]
chosen after squeeze:  [B, N]
```

这段在 RNN、PixelCNN、decoder-only Transformer、NNQS 自回归振幅里都会出现。

## gather 和 CrossEntropyLoss 的关系

`nn.CrossEntropyLoss` 本质上会做两步：

```text
log_softmax
  -> 取出 label 对应的 log probability
```

手写出来就是：

```python
logits = torch.randn(8, 10)
labels = torch.randint(0, 10, (8,))

loss_builtin = F.cross_entropy(logits, labels)

logp_all = F.log_softmax(logits, dim=-1)
chosen = logp_all.gather(dim=-1, index=labels[:, None]).squeeze(-1)
loss_manual = -chosen.mean()

torch.testing.assert_close(loss_builtin, loss_manual)
```

所以理解 `gather`，有助于理解交叉熵、next-token loss 和自回归模型的 `log_prob`。

## gather 常见错误

| 错误 | 原因 | 修法 |
| --- | --- | --- |
| `index` 少一维 | `gather` 输出 shape 跟 index 一样 | 用 `unsqueeze` 补维度 |
| `index` dtype 错 | index 必须是整数类型，通常是 `torch.long` | `index = index.long()` |
| `dim` 写错 | 沿错误维度取值 | 先写清楚要从哪一维挑 |
| 忘记 `squeeze` | 取一个值后还保留长度为 1 的维度 | 明确 `squeeze(-1)` |

一个实用判断：

> 如果你要从“类别维 / 词表维”按 label 或 token id 取值，`dim` 通常就是最后一维 `-1`。

## reshape 和 view

`reshape` 改变 tensor 形状，但元素总数必须不变。

```python
x = torch.arange(24)
y = x.reshape(2, 3, 4)
print(y.shape)
```

元素数：

$$
24=2\times3\times4.
$$

可以用 `-1` 自动推断：

```python
z = y.reshape(6, -1)
print(z.shape)
```

得到 $[6,4]$。

`view` 和 `reshape` 类似，但要求内存连续。一般初学时优先用 `reshape`。

## transpose 和 permute

矩阵转置：

```python
x = torch.randn(2, 3)
y = x.transpose(0, 1)
print(y.shape)
```

高维换轴用 `permute`：

```python
x = torch.randn(2, 3, 4)
y = x.permute(0, 2, 1)
print(y.shape)
```

如果图像数据从 $[B,H,W,C]$ 变成 PyTorch 常用的 $[B,C,H,W]$：

```python
images = torch.randn(8, 32, 32, 3)
images = images.permute(0, 3, 1, 2)
print(images.shape)
```

## unsqueeze 和 squeeze

`unsqueeze` 增加长度为 1 的维度：

```python
x = torch.randn(5)
y = x.unsqueeze(0)
z = x.unsqueeze(1)

print(y.shape)
print(z.shape)
```

输出：

```text
torch.Size([1, 5])
torch.Size([5, 1])
```

`squeeze` 删除长度为 1 的维度：

```python
x = torch.randn(1, 5, 1)
print(x.squeeze().shape)
```

如果只想删除某一个维度，建议明确写出 `dim`：

```python
x = torch.randn(1, 5, 1)
print(x.squeeze(0).shape)
```

这样不会误删其他长度为 1 的维度。写模型时这点很重要，因为 batch size 偶尔等于 1 时，裸 `squeeze()` 可能把 batch 维也删掉。

## cat 和 stack

`torch.cat` 和 `torch.stack` 都能把多个 tensor 合在一起，但含义不同。

`cat` 是沿已有维度拼接：

```python
import torch

a = torch.ones(2, 3)
b = torch.zeros(2, 3)

x0 = torch.cat([a, b], dim=0)
x1 = torch.cat([a, b], dim=1)

print(x0.shape)
print(x1.shape)
```

输出：

```text
torch.Size([4, 3])
torch.Size([2, 6])
```

这里 `dim=0` 表示把行接在一起，`dim=1` 表示把列接在一起。除拼接维之外，其他维度必须相同。

`stack` 是新增一个维度，再把 tensor 堆起来：

```python
a = torch.ones(2, 3)
b = torch.zeros(2, 3)

s0 = torch.stack([a, b], dim=0)
s1 = torch.stack([a, b], dim=1)

print(s0.shape)
print(s1.shape)
```

输出：

```text
torch.Size([2, 2, 3])
torch.Size([2, 2, 3])
```

两者的区别可以概括为：

| API | 是否新增维度 | 例子 |
| --- | --- | --- |
| `torch.cat` | 不新增维度 | $[2,3]+[2,3]\rightarrow[4,3]$ |
| `torch.stack` | 新增维度 | 两个 $[2,3]\rightarrow[2,2,3]$ |

Transformer 里常见的多头拼接就是 `cat` 或等价的 reshape 逻辑。比如每个 head 输出：

$$
h_a\in\mathbb{R}^{B\times N\times d_{\rm head}},
$$

把所有 head 沿最后一维拼起来：

```python
B, N, n_heads, d_head = 2, 4, 3, 5
heads = [torch.randn(B, N, d_head) for _ in range(n_heads)]

y = torch.cat(heads, dim=-1)
print(y.shape)
```

输出：

```text
torch.Size([2, 4, 15])
```

对应数学上的：

$$
\operatorname{Concat}(h_1,\ldots,h_{n_h})
\in
\mathbb{R}^{B\times N\times (n_h d_{\rm head})}.
$$

## chunk 和 split

`torch.chunk` 用来把 tensor 尽量平均地分成若干块：

```python
x = torch.arange(12).reshape(3, 4)
parts = torch.chunk(x, chunks=2, dim=1)

for p in parts:
    print(p)
    print(p.shape)
```

这里沿列方向把 $[3,4]$ 分成两个 $[3,2]$。

`torch.split` 可以指定每块大小：

```python
x = torch.arange(15).reshape(3, 5)
a, b, c = torch.split(x, [1, 3, 1], dim=1)

print(a.shape)
print(b.shape)
print(c.shape)
```

输出：

```text
torch.Size([3, 1])
torch.Size([3, 3])
torch.Size([3, 1])
```

两者区别：

| API | 你指定什么 | 适合场景 |
| --- | --- | --- |
| `torch.chunk(x, chunks=k, dim=...)` | 分成几块 | 均匀拆分 |
| `torch.split(x, split_size_or_sections, dim=...)` | 每块多大 | 不均匀拆分或固定块长 |

一个常见用法是把一次线性投影得到的 `qkv` 拆成 $Q,K,V$：

```python
B, N, D = 2, 4, 6
qkv = torch.randn(B, N, 3 * D)

q, k, v = torch.chunk(qkv, chunks=3, dim=-1)

print(q.shape, k.shape, v.shape)
```

输出：

```text
torch.Size([2, 4, 6]) torch.Size([2, 4, 6]) torch.Size([2, 4, 6])
```

这对应把：

$$
[B,N,3D]\rightarrow [B,N,D],[B,N,D],[B,N,D].
$$

## matmul、@ 和 bmm {#matmul-bmm}

矩阵乘法是神经网络里最核心的运算。PyTorch 中常用三种写法：

| API | 用途 |
| --- | --- |
| `A @ B` | `torch.matmul(A, B)` 的简写 |
| `torch.matmul(A, B)` | 支持向量、矩阵和 batch 矩阵乘法 |
| `torch.bmm(A, B)` | 只处理 3D batch 矩阵乘法 |

二维矩阵乘法：

```python
A = torch.randn(2, 3)
B = torch.randn(3, 4)

C = torch.matmul(A, B)
print(C.shape)
```

输出：

```text
torch.Size([2, 4])
```

数学上：

$$
[2,3]\times[3,4]\rightarrow[2,4].
$$

高维 `matmul` 会把最后两个维度当作矩阵维度，前面的维度当作 batch 维：

```python
A = torch.randn(5, 2, 3)
B = torch.randn(5, 3, 4)

C = torch.matmul(A, B)
print(C.shape)
```

输出：

```text
torch.Size([5, 2, 4])
```

这等价于对 5 个矩阵分别做乘法。

`bmm` 更严格，只接受三维输入：

```python
A = torch.randn(5, 2, 3)
B = torch.randn(5, 3, 4)

C = torch.bmm(A, B)
print(C.shape)
```

如果输入已经是三维 batch 矩阵，`bmm` 的语义更直接；如果需要自动广播或更高维 batch，使用 `matmul`。

在单头 self-attention 中，忽略 batch 时：

$$
Q,K,V\in\mathbb{R}^{N\times d_h}.
$$

打分矩阵为：

$$
S=QK^T\in\mathbb{R}^{N\times N}.
$$

代码写作：

```python
N, d_h = 4, 8
Q = torch.randn(N, d_h)
K = torch.randn(N, d_h)
V = torch.randn(N, d_h)

S = Q @ K.T
P = torch.softmax(S / (d_h ** 0.5), dim=-1)
H = P @ V

print(S.shape)
print(P.shape)
print(H.shape)
```

输出：

```text
torch.Size([4, 4])
torch.Size([4, 4])
torch.Size([4, 8])
```

带 batch 和多头时，常见 shape 是：

$$
Q,K,V\in\mathbb{R}^{B\times n_h\times N\times d_h}.
$$

此时可以直接用 `matmul`：

```python
B, n_heads, N, d_h = 2, 3, 4, 8
Q = torch.randn(B, n_heads, N, d_h)
K = torch.randn(B, n_heads, N, d_h)
V = torch.randn(B, n_heads, N, d_h)

S = torch.matmul(Q, K.transpose(-2, -1))
P = torch.softmax(S / (d_h ** 0.5), dim=-1)
H = torch.matmul(P, V)

print(S.shape)
print(H.shape)
```

输出：

```text
torch.Size([2, 3, 4, 4])
torch.Size([2, 3, 4, 8])
```

这正是 attention 的两个核心矩阵乘法：

$$
[B,n_h,N,d_h]\times[B,n_h,d_h,N]\rightarrow[B,n_h,N,N],
$$

$$
[B,n_h,N,N]\times[B,n_h,N,d_h]\rightarrow[B,n_h,N,d_h].
$$

## Broadcasting

广播允许不同 shape 的 tensor 自动对齐。

```python
x = torch.randn(2, 3)
b = torch.randn(3)
y = x + b
print(y.shape)
```

这里 $b$ 的 shape 是 $[3]$，会广播到 $[2,3]$。

广播规则从右往左对齐。两个维度兼容当且仅当：

- 相等。
- 其中一个为 1。
- 其中一个不存在。

例子：

```text
[B, N, D]
[      D]  -> 可以广播
[   N, 1]  -> 可以广播
[B, 1, D]  -> 可以广播
[B, D]     -> 通常不符合预期
```

Transformer 中位置 embedding 常用：

$$
X_{\rm tok}\in\mathbb{R}^{B\times N\times D},
\qquad
X_{\rm pos}\in\mathbb{R}^{1\times N\times D}.
$$

相加时 $X_{\rm pos}$ 沿 batch 维广播。

## where、masked_fill 和 full

mask 是深度学习代码里非常常见的一类操作。`torch.full` 经常和 mask 配合，用来创建固定值张量。

```python
scores = torch.randn(4, 4)
mask = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)

neg_inf = torch.full((4, 4), float("-inf"))
masked_scores = torch.where(mask, neg_inf, scores)

print(masked_scores.shape)
```

更常见的写法是 `masked_fill`：

```python
scores = torch.randn(4, 4)
mask = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)

masked_scores = scores.masked_fill(mask, float("-inf"))
P = torch.softmax(masked_scores, dim=-1)

print(P.shape)
```

这就是 causal mask 的基本写法：未来位置被填成 $-\infty$，softmax 后概率变成 0。更多 Transformer 解释见 [Attention 机制](../Transformer/attention.md)。

## Inplace 操作

带下划线的操作通常是 inplace：

```python
x = torch.ones(3)
x.add_(2)
print(x)
```

inplace 会直接修改原 tensor。

这可能节省内存，但在 autograd 中要小心。下面的代码可能破坏计算图需要的中间值：

```python
x = torch.randn(3, requires_grad=True)
y = x * x

# 不推荐随意 inplace 修改参与梯度计算的张量
# x.add_(1.0)
```

实践建议：

- 初学时少用 inplace。
- 需要节省显存时再明确使用。
- 如果遇到 autograd 报错，优先检查 inplace 操作。

## 最小示例：整理序列 batch

```python
import torch

B, N, D = 2, 3, 4
x = torch.randn(B, N, D)

# 合并 batch 和 sequence，常用于逐 token MLP
y = x.reshape(B * N, D)
print(y.shape)

# 处理后再还原
z = y.reshape(B, N, D)
print(z.shape)
```

shape 操作不改变数学含义，前提是你清楚每个维度代表什么。
