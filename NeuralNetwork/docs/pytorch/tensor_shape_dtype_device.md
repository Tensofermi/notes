# Tensor、Shape、Dtype 与 Device

PyTorch 的基本数据结构是 `Tensor`。可以先把它理解成带有额外能力的多维数组：

- 保存数值。
- 记录形状。
- 指定数据类型。
- 指定所在设备。
- 可以接入自动微分。

## Tensor 是什么

一个 tensor 可以是标量、向量、矩阵，也可以是更高维数组。

```python
import torch

a = torch.tensor(3.0)
b = torch.tensor([1.0, 2.0, 3.0])
c = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

print(a.shape)
print(b.shape)
print(c.shape)
```

输出：

```text
torch.Size([])
torch.Size([3])
torch.Size([2, 2])
```

标量 shape 为空，向量是一维，矩阵是二维。

## Shape 为什么重要

神经网络中大多数错误都是 shape 错误。

常见约定：

| 数据 | 常见 shape |
| --- | --- |
| 表格 batch | $[B,d]$ |
| 图像 batch | $[B,C,H,W]$ |
| 序列 token | $[B,N]$ |
| 序列 hidden states | $[B,N,d_{\rm model}]$ |
| logits | $[B,N,V]$ 或 $[B,C]$ |

例如 Transformer 中：

$$
X\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

这三个维度分别是 batch、序列长度和隐藏维度。

## 创建 Tensor

```python
import torch

zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)
full = torch.full((2, 3), 7.0)
normal = torch.randn(2, 3)
arange = torch.arange(6)
eye = torch.eye(3)

print(zeros)
print(full)
print(normal.shape)
```

常用函数：

| 函数 | 用途 |
| --- | --- |
| `torch.zeros` | 全 0 |
| `torch.ones` | 全 1 |
| `torch.full` | 用指定数值填满 tensor |
| `torch.randn` | 标准正态随机数 |
| `torch.rand` | $[0,1)$ 均匀分布随机数 |
| `torch.arange` | 等差整数序列 |
| `torch.linspace` | 指定区间内的等距浮点数 |
| `torch.eye` | 单位矩阵 |
| `torch.tensor` | 从 Python 列表创建 |

如果想创建一个和已有 tensor 同 shape、同 dtype、同 device 的 tensor，优先使用 `*_like`：

```python
x = torch.randn(2, 3, device="cpu", dtype=torch.float32)

z = torch.zeros_like(x)
o = torch.ones_like(x)
f = torch.full_like(x, -1.0)
r = torch.randn_like(x)

print(z.shape, z.dtype, z.device)
print(f)
```

`*_like` 的好处是少写 shape、dtype 和 device，尤其适合在模型 forward 里创建 mask、临时缓存或初始化辅助张量。

## Dtype

`dtype` 决定数值精度和存储格式。

```python
x32 = torch.randn(2, 3, dtype=torch.float32)
x64 = torch.randn(2, 3, dtype=torch.float64)
i64 = torch.tensor([1, 2, 3], dtype=torch.long)

print(x32.dtype)
print(x64.dtype)
print(i64.dtype)
```

常见 dtype：

| dtype | 用途 |
| --- | --- |
| `torch.float32` | 默认浮点训练精度 |
| `torch.float64` | 高精度科学计算 |
| `torch.float16` | 半精度，常用于 GPU 混合精度 |
| `torch.bfloat16` | 大模型训练常用低精度 |
| `torch.long` | 类别标签、token id |
| `torch.bool` | mask |

数值精度的详细解释见 [数值精度](../numerical_precision.md)。

## Device

`device` 决定 tensor 在 CPU 还是 GPU 上。

```python
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.randn(2, 3, device=device)

print(x.device)
```

模型和数据必须在同一个 device 上：

```python
import torch
from torch import nn

device = "cuda" if torch.cuda.is_available() else "cpu"

model = nn.Linear(3, 2).to(device)
x = torch.randn(4, 3).to(device)

y = model(x)
print(y.shape)
```

如果模型在 GPU、数据在 CPU，会报 device mismatch。

## Token ID 和 Embedding

语言模型输入通常是整数 token id：

```python
import torch
from torch import nn

token_ids = torch.tensor([[1, 5, 2], [4, 3, 0]], dtype=torch.long)
embedding = nn.Embedding(num_embeddings=10, embedding_dim=4)

x = embedding(token_ids)
print(x.shape)
```

输出 shape：

```text
torch.Size([2, 3, 4])
```

这对应：

$$
[B,N]\rightarrow[B,N,d_{\rm model}].
$$

## 最小检查清单

写 PyTorch 代码时，先检查：

```python
print(x.shape)
print(x.dtype)
print(x.device)
```

这三个信息通常能定位一半以上的基础错误。
