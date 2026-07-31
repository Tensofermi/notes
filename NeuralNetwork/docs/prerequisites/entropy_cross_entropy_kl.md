# 信息熵、交叉熵与 KL 散度

信息熵、交叉熵和 KL 散度是理解分类训练、语言模型和分布匹配的基础。

它们的关系可以先记成：

$$
H(P,Q)=H(P)+D_{\rm KL}(P\Vert Q).
$$

其中：

- $H(P)$：真实分布自身的不确定性。
- $H(P,Q)$：用模型分布 $Q$ 解释真实分布 $P$ 的代价。
- $D_{\rm KL}(P\Vert Q)$：模型分布偏离真实分布的额外代价。

## 信息熵

离散分布 $P(x)$ 的熵定义为：

$$
H(P)
=
-\sum_x P(x)\log P(x).
$$

直觉：

- 分布越均匀，不确定性越大，熵越大。
- 分布越集中，不确定性越小，熵越小。

如果 $P$ 是 one-hot：

$$
P(x^\star)=1,
$$

则：

$$
H(P)=0.
$$

## 交叉熵

设真实分布为 $P$，模型预测分布为 $Q$。交叉熵定义为：

$$
H(P,Q)
=
-\sum_x P(x)\log Q(x).
$$

它衡量：如果真实数据来自 $P$，但我们用 $Q$ 来编码或解释，需要付出多少代价。

分类任务中，真实标签通常是 one-hot。若真实类别为 $y$，则：

$$
H(P,Q)
=
-\log Q(y).
$$

这就是交叉熵损失。

## KL 散度

KL 散度定义为：

$$
D_{\rm KL}(P\Vert Q)
=
\sum_x P(x)\log{P(x)\over Q(x)}.
$$

它不是距离，因为一般：

$$
D_{\rm KL}(P\Vert Q)\ne D_{\rm KL}(Q\Vert P).
$$

但它满足：

$$
D_{\rm KL}(P\Vert Q)\ge 0,
$$

且当 $P=Q$ 时为 0。

## 三者关系

展开 KL：

$$
D_{\rm KL}(P\Vert Q)
=
\sum_x P(x)\log P(x)
-
\sum_x P(x)\log Q(x).
$$

因此：

$$
D_{\rm KL}(P\Vert Q)
=
-H(P)+H(P,Q).
$$

也就是：

$$
H(P,Q)=H(P)+D_{\rm KL}(P\Vert Q).
$$

训练时 $P$ 是数据分布，不由模型控制。因此最小化交叉熵等价于最小化前向 KL：

$$
\min_\theta H(P,Q_\theta)
\Longleftrightarrow
\min_\theta D_{\rm KL}(P\Vert Q_\theta).
$$

## Softmax + CrossEntropy

分类模型输出 logits：

$$
z=(z_1,\ldots,z_C).
$$

softmax 给出：

$$
p_i={e^{z_i}\over\sum_j e^{z_j}}.
$$

若真实类别是 $y$，loss 为：

$$
L=-\log p_y.
$$

展开：

$$
L=-z_y+\log\sum_j e^{z_j}.
$$

对 logits 的梯度是：

$$
{\partial L\over\partial z_i}
=
p_i-\mathbf 1[i=y].
$$

这个结果很重要：梯度就是“预测概率减真实概率”。

## 和 Transformer 的关系

decoder-only Transformer 训练时预测下一个 token：

$$
P_\theta(t_{i+1}\mid t_{\le i}).
$$

交叉熵损失为：

$$
L
=
-\sum_i\log P_\theta(t_{i+1}\mid t_{\le i}).
$$

这就是在用模型分布逼近数据中的 next-token 条件分布。更多训练目标细节见 [训练目标与 Mask](../Transformer/training.md)。

## 数值稳定

softmax 和交叉熵会涉及指数和对数。实际实现通常不会先显式算 softmax 再取 log，而是使用数值稳定版本。相关精度问题见 [数值精度](../numerical_precision.md)。

## 招聘考点

!!! question "代表题：为什么交叉熵等价于最大似然？"
    对 one-hot 分类标签，单样本负对数似然为 $L=-\log p_\theta(y\mid x)$，这正是交叉熵。对整个数据集取平均，就是最大化真实样本在模型分布下的 log likelihood。进一步看，它等价于最小化 $D_{\rm KL}(P_{\rm data}\Vert P_\theta)$。完整题解见 [机器学习基础题](../interview/ml_basics.md)。
