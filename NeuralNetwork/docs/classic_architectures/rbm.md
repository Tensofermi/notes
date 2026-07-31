# RBM：能量模型与神经网络量子态

RBM, restricted Boltzmann machine，是经典的能量模型，也曾是神经网络量子态中非常重要的 ansatz。

它和 RNN、PixelCNN、decoder-only Transformer 的范式不同。

自回归模型做的是：

```text
逐个位置输出 conditional probability
```

RBM 做的是：

```text
给整个 configuration 一个能量、自由能或振幅分数
```

## 结构

RBM 有两层变量：

```text
visible layer: v1 v2 v3 ... vN
hidden layer:  h1 h2 h3 ... hM
```

visible 和 hidden 之间全连接，同层内部没有连接：

```text
v_i  --  h_j
```

这就是 restricted 的含义。没有同层连接，使得某些条件分布可以分解，采样和推导更简单。

## 概率模型版本

对二值 visible $v$ 和 hidden $h$，RBM 能量常写成：

$$
E(v,h)
=
-a^Tv-b^Th-v^TWh.
$$

联合概率：

$$
P(v,h)
=
{e^{-E(v,h)}\over Z}.
$$

其中配分函数：

$$
Z=\sum_{v,h}e^{-E(v,h)}.
$$

visible 的概率是把 hidden 求和：

$$
P(v)
=
\sum_hP(v,h)
=
{e^{-F(v)}\over Z}.
$$

$F(v)$ 叫 free energy。对 Bernoulli hidden，可以解析求和得到：

$$
F(v)
=
-a^Tv
-
\sum_j
\log\left(1+\exp(b_j+W_jv)\right).
$$

问题在于 $Z$ 通常很难精确计算。这也是 energy-based model 的典型困难：

> 给一个构型打分容易，得到全局归一化概率难。

## NNQS 版本

在神经网络量子态里，RBM 常被用作波函数 ansatz。对自旋构型：

$$
\sigma_i\in\{-1,+1\},
$$

一种常见形式是：

$$
\log\psi(\sigma)
=
\sum_i a_i\sigma_i
+
\sum_j
\log
2\cosh
\left(
b_j+\sum_iW_{ji}\sigma_i
\right).
$$

这里 hidden spin 已经被解析求和掉，所以 `forward` 可以直接返回每个构型的 log amplitude：

```text
sigma:   [batch, n_visible]
log_psi: [batch]
```

这和自回归模型不同。自回归模型通常输出：

```text
logits: [batch, length, n_tokens]
```

RBM 输出的是整个构型的分数。

## RBM Wavefunction 的 PyTorch 写法

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class RBMWaveFunction(nn.Module):
    def __init__(self, n_visible: int, n_hidden: int):
        super().__init__()
        self.visible_bias = nn.Parameter(torch.zeros(n_visible))
        self.hidden_bias = nn.Parameter(torch.zeros(n_hidden))
        self.weight = nn.Parameter(0.01 * torch.randn(n_hidden, n_visible))

    def forward(self, sigma: torch.Tensor) -> torch.Tensor:
        """
        sigma:   [batch, n_visible], values in {-1, +1}
        return:  log_psi [batch]
        """
        visible_term = sigma @ self.visible_bias
        hidden_pre = F.linear(sigma, self.weight, self.hidden_bias)
        hidden_term = torch.log(2.0 * torch.cosh(hidden_pre)).sum(dim=-1)
        return visible_term + hidden_term
```

数值上，`log(cosh(x))` 在 $|x|$ 很大时可能不稳定。更稳的实现会用等价变形或 `softplus`。

## Bernoulli RBM 的 PyTorch 写法

下面是概率模型版本的 free energy：

```python
class BernoulliRBM(nn.Module):
    def __init__(self, n_visible: int, n_hidden: int):
        super().__init__()
        self.visible_bias = nn.Parameter(torch.zeros(n_visible))
        self.hidden_bias = nn.Parameter(torch.zeros(n_hidden))
        self.weight = nn.Parameter(0.01 * torch.randn(n_hidden, n_visible))

    def free_energy(self, v: torch.Tensor) -> torch.Tensor:
        """
        v:      [batch, n_visible], values in {0, 1}
        return: F(v) [batch]
        """
        visible_term = -(v @ self.visible_bias)
        hidden_pre = F.linear(v, self.weight, self.hidden_bias)
        hidden_term = -F.softplus(hidden_pre).sum(dim=-1)
        return visible_term + hidden_term
```

这里：

$$
P(v)
\propto
e^{-F(v)}.
$$

## 为什么训练和采样更麻烦

自回归模型可以直接算：

$$
\log P(t_0,\ldots,t_{N-1})
=
\sum_i
\log P(t_i\mid t_{<i}).
$$

每一项都是局部 softmax，天然归一化。

RBM 则是：

$$
\log P(v)
=
-F(v)-\log Z.
$$

问题在于：

$$
Z=\sum_v e^{-F(v)}
$$

通常无法精确求。因此 classical RBM 训练时常用 contrastive divergence、persistent contrastive divergence、Gibbs sampling 等近似方法。

从采样角度：

```text
自回归模型:
  从左到右直接采样 t_i ~ P(t_i | t_<i)

RBM:
  在 visible 和 hidden 之间来回 Gibbs sampling
```

## 和 NNQS 的关系

RBM 是早期 NNQS 的代表，因为它直接给出波函数振幅：

$$
\sigma\mapsto\psi_\theta(\sigma).
$$

它体现了神经网络量子态的核心思想：

> 不显式存储指数维 Hilbert space 中每个构型的振幅，而是用有限参数函数生成振幅。

但是 RBM 的结构相对固定，表达复杂长程结构时可能需要很多 hidden units。现代 NNQS 常用 autoregressive network、CNN、Transformer、normalizing flow 等更灵活的结构。

## RBM、PixelCNN、Transformer 对比

| 模型 | 概率范式 | `forward` 常见输出 | 是否天然归一化 |
| --- | --- | --- | --- |
| PixelCNN | 自回归条件概率 | 每个格点 logits | 是 |
| Transformer | 自回归条件概率 | 每个位置 next-token logits | 是 |
| RBM | energy / free energy | 每个构型一个分数 | 通常不是 |

从 NNQS 角度看：

```text
RBM:
  configuration -> log amplitude

Autoregressive model:
  prefix -> next token probability

Transformer NNQS:
  用 decoder-only 结构表示构型概率，再得到振幅
```

