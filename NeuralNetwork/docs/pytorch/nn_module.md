# nn.Module 的核心机制

`nn.Module` 是 PyTorch 中组织模型的核心抽象。

它的本质是：

$$
\texttt{nn.Module}
\equiv
\text{带参数管理能力的函数}.
$$

一个 Module 主要提供三件事：

1. 参数注册。
2. forward 计算定义。
3. 子模块嵌套。

## 最小 Module

```python
import torch
from torch import nn

class TinyLinear(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(3, 2)

    def forward(self, x):
        return self.linear(x)

model = TinyLinear()
x = torch.randn(4, 3)
y = model(x)

print(y.shape)
```

调用：

```python
y = model(x)
```

实际会进入 `forward`，但不要直接写：

```python
model.forward(x)
```

因为 `model(x)` 还会处理 hooks、autocast、分布式包装和其它内部逻辑。

## 参数注册

当你写：

```python
self.linear = nn.Linear(3, 2)
```

PyTorch 会自动发现这个子模块中的参数。

```python
for name, param in model.named_parameters():
    print(name, param.shape)
```

输出类似：

```text
linear.weight torch.Size([2, 3])
linear.bias torch.Size([2])
```

这些参数会被：

- `model.parameters()` 返回。
- optimizer 更新。
- `state_dict()` 保存。
- `.to(device)` 移动到对应设备。

## nn.Parameter

如果要自己定义可训练参数，用 `nn.Parameter`：

```python
class Scale(nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(()))

    def forward(self, x):
        return self.weight * x

model = Scale()
print(list(model.parameters()))
```

普通 tensor 不会自动注册为参数：

```python
self.x = torch.ones(3)  # 不会出现在 parameters()
```

## register_buffer

有些 tensor 不是参数，但应该跟着模型保存和移动 device。例如 running mean、mask、固定常数。

```python
class WithMask(nn.Module):
    def __init__(self):
        super().__init__()
        self.register_buffer("mask", torch.ones(3))

    def forward(self, x):
        return x * self.mask
```

buffer 会出现在 `state_dict()` 中，但不会被 optimizer 更新。

## 子模块嵌套

复杂模型由小模块组合：

```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.net(x)

model = MLP()
print(model)
```

函数视角：

$$
f_\theta(x)
=
f_3(f_2(f_1(x))).
$$

模块嵌套让参数自动管理保持一致。

## 函数空间视角

`nn.Module` 定义一个参数化函数族：

$$
\{f_\theta\}.
$$

训练是在这个函数族中寻找：

$$
\theta^\star
=
\arg\min_\theta L(f_\theta).
$$

对 NNQS 来说，`NeuralQuantumState` 也是一个 Module，只是它表示的不是普通预测函数，而是：

$$
x\mapsto\psi_\theta(x).
$$

## 三层分离

PyTorch 训练系统可以拆成：

| 层 | PyTorch 对象 | 数学含义 |
| --- | --- | --- |
| 模型结构 | `nn.Module` | $f_\theta$ |
| 自动微分 | `autograd` | $\nabla_\theta L$ |
| 优化器 | `torch.optim` | $\theta\leftarrow\theta-\eta g$ |

理解这三层，基本就理解了 PyTorch 训练代码的骨架。

