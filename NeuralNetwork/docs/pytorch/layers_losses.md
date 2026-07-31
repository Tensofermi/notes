# 常用层、激活函数与损失函数

这一页整理 PyTorch 中最常见的神经网络组件。

## Linear

全连接层：

$$
y=xW^{\mathsf T}+b.
$$

PyTorch 中：

```python
import torch
from torch import nn

layer = nn.Linear(in_features=4, out_features=3)
x = torch.randn(2, 4)
y = layer(x)

print(y.shape)
```

输出：

```text
torch.Size([2, 3])
```

权重 shape 是：

```python
print(layer.weight.shape)
print(layer.bias.shape)
```

对应：

```text
torch.Size([3, 4])
torch.Size([3])
```

## Conv2d

卷积层适合图像或格点数据：

```python
conv = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)
x = torch.randn(4, 1, 28, 28)
y = conv(x)

print(y.shape)
```

输出：

```text
torch.Size([4, 8, 28, 28])
```

CNN 利用局部感受野和权重共享。它适合处理具有空间局部结构的数据，例如图像、格点构型或 QMC 压缩后的多通道构型。

## Embedding

Embedding 把整数 id 映射为向量：

```python
embed = nn.Embedding(num_embeddings=10, embedding_dim=4)
ids = torch.tensor([[1, 2, 3], [4, 5, 0]])
x = embed(ids)

print(x.shape)
```

输出：

```text
torch.Size([2, 3, 4])
```

Transformer 的 token embedding 就是这个结构。

## BatchNorm 与 LayerNorm

BatchNorm 常用于 CNN：

```python
bn = nn.BatchNorm1d(8)
x = torch.randn(16, 8)
y = bn(x)
```

LayerNorm 常用于 Transformer：

```python
ln = nn.LayerNorm(8)
x = torch.randn(2, 5, 8)
y = ln(x)
```

LayerNorm 对每个 token 的隐藏维度归一化：

$$
\mathrm{LN}:\mathbb{R}^{B\times N\times D}
\rightarrow
\mathbb{R}^{B\times N\times D}.
$$

## Dropout

Dropout 训练时随机置零一部分激活：

```python
drop = nn.Dropout(p=0.5)
x = torch.ones(5)

drop.train()
print(drop(x))

drop.eval()
print(drop(x))
```

注意：Dropout 在 `train()` 和 `eval()` 模式下行为不同。

## 激活函数

常见激活：

| 激活 | 公式或特点 |
| --- | --- |
| ReLU | $\max(0,x)$，简单稳定 |
| Sigmoid | 输出 $(0,1)$，容易饱和 |
| Tanh | 输出 $(-1,1)$ |
| GELU | Transformer 常用，平滑非线性 |

示例：

```python
x = torch.linspace(-3, 3, steps=7)
print(torch.relu(x))
print(torch.sigmoid(x))
print(torch.tanh(x))
print(nn.GELU()(x))
```

## CrossEntropyLoss

多分类常用：

```python
loss_fn = nn.CrossEntropyLoss()

logits = torch.randn(4, 3)
target = torch.tensor([0, 2, 1, 2])

loss = loss_fn(logits, target)
print(loss)
```

注意：`CrossEntropyLoss` 输入是 logits，不需要提前 softmax。

数学上：

$$
L=-\log
{e^{z_y}\over\sum_j e^{z_j}}.
$$

## MSELoss

回归常用：

```python
loss_fn = nn.MSELoss()
pred = torch.randn(4, 1)
target = torch.randn(4, 1)

loss = loss_fn(pred, target)
print(loss)
```

数学上：

$$
L={1\over N}\sum_i(\hat y_i-y_i)^2.
$$

## 组件组合

一个最小 MLP：

```python
model = nn.Sequential(
    nn.Linear(4, 16),
    nn.ReLU(),
    nn.Linear(16, 3),
)

x = torch.randn(8, 4)
logits = model(x)
print(logits.shape)
```

输出：

```text
torch.Size([8, 3])
```

