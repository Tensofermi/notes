# 训练循环：forward、backward、optimizer.step

PyTorch 训练循环的标准结构是：

```text
取 batch
  -> forward
  -> loss
  -> zero_grad
  -> backward
  -> optimizer.step
```

## 最小监督学习例子

```python
import torch
from torch import nn

torch.manual_seed(0)

X = torch.randn(128, 3)
true_w = torch.tensor([[2.0], [-1.0], [0.5]])
y = X @ true_w + 0.1 * torch.randn(128, 1)

model = nn.Linear(3, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
loss_fn = nn.MSELoss()

for step in range(100):
    pred = model(X)
    loss = loss_fn(pred, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(loss.item())
print(model.weight)
```

这段代码包含完整训练闭环。

## 每一步在做什么

### forward

```python
pred = model(X)
```

数学上是：

$$
\hat y=f_\theta(X).
$$

### loss

```python
loss = loss_fn(pred, y)
```

数学上是：

$$
L(\theta)=\ell(f_\theta(X),y).
$$

### zero_grad

```python
optimizer.zero_grad()
```

PyTorch 会累积梯度，所以每次更新前需要清空旧梯度。

### backward

```python
loss.backward()
```

计算：

$$
\nabla_\theta L(\theta).
$$

### step

```python
optimizer.step()
```

执行参数更新。SGD 中近似为：

$$
\theta\leftarrow\theta-\eta\nabla_\theta L.
$$

## Mini-batch 训练

真实训练通常不用全量数据，而是 mini-batch：

```python
from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for epoch in range(5):
    for xb, yb in loader:
        pred = model(xb)
        loss = loss_fn(pred, yb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

mini-batch 梯度是全量梯度的随机估计。

## train 和 eval

训练前：

```python
model.train()
```

推理或验证前：

```python
model.eval()
```

这会影响 Dropout、BatchNorm 等模块。

验证时还应关闭梯度：

```python
model.eval()
with torch.no_grad():
    pred = model(X)
```

## 和 VMC 训练闭环的对比

监督学习数据集固定：

```text
固定 batch
  -> model
  -> loss
  -> backward
  -> update
```

VMC / NNQS 的样本来自当前模型：

```text
当前 theta
  -> psi_theta
  -> p_theta(x)=|psi_theta(x)|^2
  -> sample x
  -> local energy
  -> VMC gradient proxy
  -> update theta
  -> 新的 p_theta
```

差别是：监督学习的样本分布通常固定，VMC 的样本分布依赖当前参数。详见 [VMC 的闭环训练视角](../vmc_closed_loop.md)。

## 常见训练问题

| 现象 | 常见原因 |
| --- | --- |
| loss 不下降 | 学习率不合适、模型太弱、数据处理错误 |
| loss 变成 `nan` | 学习率过大、数值溢出、非法除法 |
| 梯度一直是 0 | detach、不可导操作、激活饱和 |
| GPU 报错 device mismatch | 模型和数据不在同一 device |
| 显存越来越大 | 保存了带计算图的 tensor |

训练循环看似固定，但调试时要同时检查 shape、dtype、device、loss 数值和梯度。

## 招聘考点

!!! question "代表题：为什么每轮训练前要 `optimizer.zero_grad()`？"
    PyTorch 默认会把每次 `backward()` 得到的梯度累积到参数的 `.grad` 上。如果不清零，下一轮更新使用的是多轮梯度之和。除非有意做 gradient accumulation，否则标准训练循环应先 `zero_grad()`，再 `backward()` 和 `step()`。完整题解见 [PyTorch 与工程实现题](../interview/pytorch_engineering.md)。
