# Autograd 与计算图

PyTorch 的 autograd 负责自动求导。它记录 forward 过程中的张量运算，并在 `backward()` 时按链式法则计算梯度。

## requires_grad

如果一个 tensor 需要梯度，设置：

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x * x + 3 * x
y.backward()

print(x.grad)
```

数学上：

$$
y=x^2+3x,
\qquad
{dy\over dx}=2x+3.
$$

当 $x=2$ 时，梯度为 7。

## 计算图

PyTorch 使用动态图。每次 forward 都会构建一张新的计算图。

```python
x = torch.randn(3, requires_grad=True)
y = (x * x).sum()

print(y.grad_fn)
y.backward()
print(x.grad)
```

`grad_fn` 记录这个 tensor 是通过什么操作得到的。

## 为什么标量可以直接 backward

`backward()` 默认要求输出是标量。

```python
x = torch.randn(3, requires_grad=True)
y = x * x

# y.backward()  # 会报错
y.sum().backward()
print(x.grad)
```

如果输出不是标量，需要手动提供外部梯度：

```python
x = torch.randn(3, requires_grad=True)
y = x * x

external_grad = torch.ones_like(y)
y.backward(external_grad)
print(x.grad)
```

这对应向量-雅可比积。

## 梯度累积

PyTorch 默认累积梯度：

```python
x = torch.tensor(1.0, requires_grad=True)

y1 = x * 2
y1.backward()
print(x.grad)

y2 = x * 3
y2.backward()
print(x.grad)
```

第二次输出是累加后的梯度。

训练时必须清梯度：

```python
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

否则每个 batch 的梯度会叠加到一起。

## detach

`detach()` 返回一个不再追踪梯度的新 tensor。

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.detach()

print(y.requires_grad)
print(z.requires_grad)
```

常见用途：

- 记录日志时不希望保留计算图。
- 截断反向传播。
- 把 tensor 转成 NumPy 前先分离。

```python
value = y.detach().cpu().numpy()
```

## no_grad

推理时通常不需要梯度：

```python
from torch import nn

model = nn.Linear(3, 1)
x = torch.randn(4, 3)

with torch.no_grad():
    y = model(x)

print(y.requires_grad)
```

`torch.no_grad()` 会降低内存占用，因为不需要保存反向传播中间量。

## torch.autograd.grad

有时只想拿梯度，不想写入 `.grad`：

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3

grad_x = torch.autograd.grad(y, x)[0]
print(grad_x)
```

这在实现自定义梯度、物理约束或高阶导数时常用。

## 常见错误

### 忘记 zero_grad

训练 loss 看起来异常，先检查是否每轮调用：

```python
optimizer.zero_grad()
```

### 对非叶子张量看 grad

默认只有叶子张量保存 `.grad`。如果要看中间张量梯度：

```python
y.retain_grad()
```

### inplace 修改

inplace 操作可能破坏 autograd 需要的中间值。遇到相关报错，先移除带 `_` 的操作。

## 和训练闭环的关系

autograd 做的是：

$$
L
\rightarrow
\nabla_\theta L.
$$

它不决定目标函数是什么，也不决定优化器怎么更新。PyTorch 训练系统分三层：

| 层 | 负责 |
| --- | --- |
| `nn.Module` | 定义 $f_\theta(x)$ |
| `autograd` | 计算梯度 |
| `torch.optim` | 更新参数 |

