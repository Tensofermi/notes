# MLP：最基本的全连接网络

MLP, multi-layer perceptron，是最基础的前馈神经网络。它的输入是一个固定长度向量，输出可以是分类 logits、回归值，也可以是某种隐藏表示。

最简单的一层线性变换是：

$$
y = xW + b.
$$

如果只有线性层，无论堆多少层，整体仍然只是一个线性变换。MLP 的关键是在线性层之间插入非线性激活函数：

$$
h_1 = \phi(xW_1+b_1),
$$

$$
h_2 = \phi(h_1W_2+b_2),
$$

$$
\hat y = h_2W_3+b_3.
$$

其中 $\phi$ 可以是 ReLU、GELU、tanh、sigmoid 等。

## 直观理解

MLP 可以理解成：

```text
原始输入
  -> 线性组合
  -> 非线性弯折
  -> 再线性组合
  -> 再非线性弯折
  -> 输出
```

线性层负责把特征重新混合，非线性负责让模型表达弯曲的决策边界。

如果没有非线性：

$$
xW_1W_2W_3
$$

可以合并成：

$$
xW.
$$

所以深度本身不够，深度 + 非线性才有意义。

## Shape

假设输入：

$$
x\in\mathbb R^{B\times d_{\rm in}}.
$$

一层全连接：

$$
W\in\mathbb R^{d_{\rm in}\times d_{\rm out}},
\qquad
b\in\mathbb R^{d_{\rm out}}.
$$

输出：

$$
y=xW+b\in\mathbb R^{B\times d_{\rm out}}.
$$

对 PyTorch 的 `nn.Linear(d_in, d_out)` 来说，权重保存形状通常是：

```text
weight: [d_out, d_in]
bias:   [d_out]
```

但数学上常写成右乘 $xW$。二者只是约定不同。

## 最小 PyTorch 例子

```python
import torch
import torch.nn as nn


class MLPClassifier(nn.Module):
    def __init__(self, d_in: int, d_hidden: int, n_classes: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, d_hidden),
            nn.GELU(),
            nn.Linear(d_hidden, d_hidden),
            nn.GELU(),
            nn.Linear(d_hidden, n_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x:      [batch, d_in]
        return: [batch, n_classes]
        """
        return self.net(x)


model = MLPClassifier(d_in=784, d_hidden=256, n_classes=10)
x = torch.randn(32, 784)
logits = model(x)
print(logits.shape)  # torch.Size([32, 10])
```

分类时，`logits` 还不是概率。交叉熵损失会在内部做 `log_softmax`：

```python
labels = torch.randint(0, 10, (32,))
loss = nn.CrossEntropyLoss()(logits, labels)
```

## MLP 的优点和限制

优点：

- 结构简单。
- 对固定长度向量很自然。
- 很适合表格特征、embedding 后的特征、Transformer block 里的 feed-forward 子层。
- 实现和调试成本低。

限制：

- 不直接利用图像的局部平移结构。
- 不直接利用序列顺序。
- 参数量容易随输入维度变大。
- 对可变长度输入不自然。

例如一张 $224\times224\times3$ 图片，如果直接展平成向量输入 MLP，第一层就要面对：

$$
224\times224\times3=150528
$$

维输入。这样既浪费参数，也忽略了相邻像素之间的局部结构。CNN 正是为了解决这个问题。

## MLP 在现代网络中的位置

虽然 MLP 很基础，但它并没有被淘汰。

Transformer block 里有一个重要子层就是 MLP / FFN：

$$
\mathrm{FFN}(x)
=
W_2\phi(W_1x+b_1)+b_2.
$$

它对每个 token 位置单独作用：

```text
attention: token 之间交换信息
MLP: 每个 token 内部做非线性加工
```

所以现代大模型不是不用 MLP，而是把 MLP 放在更复杂的结构中使用。

## 和压缩思想的关系

MLP 学的是从输入向量到输出的压缩表示：

```text
高维输入
  -> hidden representation
  -> 输出
```

如果 hidden representation 抓住了任务相关结构，就不需要为每个输入单独存一个答案表。

