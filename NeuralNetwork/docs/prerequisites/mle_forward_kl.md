# 最大似然与前向 KL

最大似然估计和交叉熵训练本质上是同一件事：让模型分布尽量解释观测数据。

设真实数据来自分布 $P_{\rm data}(x)$，模型为 $Q_\theta(x)$。最大似然训练最大化：

$$
\prod_{i=1}^N Q_\theta(x_i).
$$

为了计算方便，通常最大化 log likelihood：

$$
\sum_{i=1}^N \log Q_\theta(x_i).
$$

等价地，最小化 negative log likelihood：

$$
L(\theta)
=
-{1\over N}\sum_{i=1}^N \log Q_\theta(x_i).
$$

## 从有限样本到期望

当样本数很大时，经验平均近似真实分布期望：

$$
-{1\over N}\sum_{i=1}^N \log Q_\theta(x_i)
\approx
-\mathbb E_{x\sim P_{\rm data}}
\log Q_\theta(x).
$$

右边就是交叉熵：

$$
H(P_{\rm data},Q_\theta)
=
-\sum_x P_{\rm data}(x)\log Q_\theta(x).
$$

## 与前向 KL 的等价

KL 散度为：

$$
D_{\rm KL}(P_{\rm data}\Vert Q_\theta)
=
\sum_x P_{\rm data}(x)
\log{P_{\rm data}(x)\over Q_\theta(x)}.
$$

展开：

$$
D_{\rm KL}(P_{\rm data}\Vert Q_\theta)
=
\sum_x P_{\rm data}(x)\log P_{\rm data}(x)
-
\sum_x P_{\rm data}(x)\log Q_\theta(x).
$$

第一项与 $\theta$ 无关。因此：

$$
\arg\min_\theta
D_{\rm KL}(P_{\rm data}\Vert Q_\theta)
=
\arg\min_\theta
H(P_{\rm data},Q_\theta).
$$

也就是：

> 最大似然 = 最小化交叉熵 = 最小化前向 KL。

## 为什么叫前向 KL

这里的方向是：

$$
D_{\rm KL}(P_{\rm data}\Vert Q_\theta).
$$

期望在真实数据分布下取：

$$
\mathbb E_{x\sim P_{\rm data}}[\cdots].
$$

这意味着模型会被强迫覆盖数据中出现的模式。如果某个真实样本 $x$ 满足 $P_{\rm data}(x)>0$，但模型给 $Q_\theta(x)\approx 0$，代价会很大。

反向 KL 是：

$$
D_{\rm KL}(Q_\theta\Vert P_{\rm data}),
$$

期望在模型分布下取。它更容易出现 mode-seeking 行为，即模型集中在少数高概率模式上。

## 语言模型中的形式

语言模型数据是 token 序列：

$$
t_0,\ldots,t_{N-1}.
$$

自回归分解：

$$
Q_\theta(t_0,\ldots,t_{N-1})
=
\prod_i
Q_\theta(t_i\mid t_{<i}).
$$

最大似然等价于最小化：

$$
L(\theta)
=
-\sum_i
\log Q_\theta(t_i\mid t_{<i}).
$$

这正是 decoder-only Transformer 的训练目标。

## 和 NNQS 的差别

NNQS 的目标通常不是拟合外部样本分布，而是通过变分原理最小化能量：

$$
E(\theta)
=
\mathbb E_{x\sim p_\theta}
[E_{\rm loc}(x)].
$$

这里采样分布 $p_\theta$ 本身依赖模型参数，不是固定的 $P_{\rm data}$。所以它不是普通最大似然，而是参数依赖分布上的闭环优化。

