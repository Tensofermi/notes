# 神经网络发展与统计物理视角

神经网络的发展可以从两个角度看：

- 工程角度：模型结构如何变得更可训练、更可扩展。
- 物理角度：大量自由度、能量景观、相变和统计学习之间的类比。

## 早期神经元模型

McCulloch-Pitts 神经元把输入加权求和，再过阈值函数：

$$
y=\Theta\left(\sum_i w_i x_i-b\right).
$$

它展示了一个重要思想：简单单元组合后可以实现逻辑计算。

感知机进一步引入可训练权重：

$$
y=\mathrm{sign}(w^{\mathsf T}x+b).
$$

但单层感知机只能表示线性可分问题。

## MLP 与反向传播

多层感知机通过隐藏层引入非线性：

$$
f_\theta(x)
=
W_2\sigma(W_1x+b_1)+b_2.
$$

反向传播让多层网络可以用链式法则高效计算梯度：

$$
\nabla_\theta L.
$$

这是现代深度学习训练的基础。

## Hopfield 网络与能量函数

Hopfield 网络把神经网络和能量函数联系起来。状态 $s_i\in\{-1,1\}$，能量可写成：

$$
E(s)
=
-{1\over2}\sum_{ij}w_{ij}s_is_j
-\sum_i b_is_i.
$$

网络更新会倾向降低能量。这和统计物理中的自旋系统非常接近。

## CNN、LSTM 与 Transformer

CNN 利用局部卷积和权重共享，适合图像和格点数据。

LSTM 通过门控结构处理序列，缓解普通 RNN 的梯度消失。

Transformer 用 attention 直接建模任意位置之间的信息读取：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{softmax}
\left({QK^{\mathsf T}\over\sqrt{d_h}}\right)V.
$$

从物理角度看，attention 可以理解为一种输入依赖的有效相互作用。

## 统计物理视角

神经网络训练包含大量参数：

$$
\theta\in\mathbb{R}^P.
$$

loss landscape 像高维能量景观：

$$
L(\theta).
$$

训练过程可以类比为在这个景观上寻找低能区域。这个类比不是严格物理等价，但有助于理解：

- 局部极小值。
- 鞍点。
- 随机梯度噪声。
- 泛化和有效自由度。
- 大模型中的涌现行为。

继续往大模型方向走，会自然遇到两个尺度问题。第一是 loss 随模型、数据和算力如何下降，见 [Scaling Law：模型、数据与算力](scaling_laws.md)。第二是宽度趋于无穷时训练动力学如何缩放，见 [NTK、μP 与无限宽极限](ntk_mup_infinite_width.md)。这两者都借用了尺度分析的语言，但前者偏经验规律和训练预算，后者偏无限宽理论和参数化。

## 和 NNQS 的连接

NNQS 更直接地把神经网络和物理连接起来：

$$
x\mapsto\psi_\theta(x).
$$

这里神经网络不是普通分类器，而是 many-body 波函数的压缩表示。训练目标也不是标签误差，而是变分能量：

$$
\min_\theta E[\psi_\theta].
$$
