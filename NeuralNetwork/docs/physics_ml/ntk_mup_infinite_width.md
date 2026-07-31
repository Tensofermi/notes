# NTK、μP 与无限宽极限

Scaling law 讨论的是：

$$
\text{模型规模、数据量、算力}
\quad\Rightarrow\quad
\text{loss 怎样下降}.
$$

NTK 和 $\mu P$ 讨论的是另一件事：

$$
\text{网络宽度 } n\to\infty
\quad\Rightarrow\quad
\text{训练动力学会变成什么}.
$$

这两类问题经常被放在一起讲，因为它们都用了“scale”这个词，但它们不是一回事。

## 先区分三个概念

| 概念 | 关心的问题 |
| --- | --- |
| scaling exponent | loss 随 $N,D,C$ 扩大怎样下降 |
| compute-optimal scaling | 固定训练 compute 时，参数量和 token 数怎样分配 |
| infinite-width parametrization | 宽度 $n$ 变大时，初始化、学习率、输出缩放如何设置 |

如果说 scaling law 是“训练预算规划”，那么 NTK 和 $\mu P$ 更像是“宽度极限下的动力学坐标系”。

## NTK 是什么？

NTK 是 **Neural Tangent Kernel**。

设神经网络输出为：

$$
f_\theta(x),
$$

参数是 $\theta$。在初始化点 $\theta_0$ 附近做一阶 Taylor 展开：

$$
f_\theta(x)
\approx
f_{\theta_0}(x)
+
\nabla_\theta f_{\theta_0}(x)\cdot(\theta-\theta_0).
$$

于是每个输入 $x$ 都可以对应一个特征向量：

$$
\phi(x)=\nabla_\theta f_{\theta_0}(x).
$$

两个输入之间的相似度就是：

$$
K_\theta(x,x')
=
\nabla_\theta f_\theta(x)\cdot\nabla_\theta f_\theta(x').
$$

这就是 NTK。

## NTK 的直观理解

普通神经网络训练时，参数在动，表示也在变。

NTK 极限说的是：在某些无限宽设定下，网络训练可以近似看成：

```text
特征几乎固定
只在线性化后的函数空间里做梯度下降
```

也就是说，神经网络被近似成一个 kernel method。

这带来一个好处：训练动力学变得更容易分析。因为在函数空间中，很多非凸参数优化问题可以转成 kernel gradient flow。

但它也有一个限制：

> NTK 极限更接近 lazy training，不太能描述真实大模型中强烈的 feature learning。

所谓 lazy，是指网络函数主要沿初始化附近的切空间变化，内部表示没有发生足够大的重组。

## 什么是 feature learning？

如果模型训练时只是最后的线性组合变了，而底层特征几乎不动，那更像 kernel machine。

如果训练过程中中间层表示也发生系统性变化，例如：

```text
早期层学局部模式
中间层学语法/结构
高层学任务相关抽象
```

这就更接近 feature learning。

真实大模型训练通常不是纯 lazy 的。模型会在训练中塑造自己的内部表示。因此，只用 NTK 描述大模型并不充分。

## μP 想解决什么？

$\mu P$ 是 **maximal update parametrization**。

它关心的问题是：

> 当网络宽度变大时，怎样缩放初始化、学习率和不同层参数，才能让模型更新保持非平凡？

这里“非平凡”的意思是：

- 更新不能太小，否则变成 lazy / 不学习特征。
- 更新不能太大，否则训练发散。
- 不同宽度模型的训练动力学最好可以比较。

用一句话说：

> $\mu P$ 试图找到一种宽度缩放规则，让小模型调出来的超参数可以迁移到大模型。

这就是 $\mu$Transfer 的思想。

## power counting 的角色

$\mu P$ 背后有一个很重要的方法：power counting。

假设宽度是 $n$，我们关心不同量随 $n$ 的幂次：

$$
W_{ij}\sim n^{-a},
$$

$$
\Delta W_{ij}\sim n^{-b},
$$

$$
\Delta f\sim n^c.
$$

理想情况下，希望函数输出的更新量满足：

$$
\Delta f\sim O(1).
$$

如果：

$$
\Delta f\to 0,
$$

更新太小，模型接近 lazy。

如果：

$$
\Delta f\to\infty,
$$

更新太大，训练动力学不稳定。

所以 power counting 的作用是：判断每个缩放选择会不会让训练进入合理的极限。

## 一个非常简化的宽度缩放图像

考虑一层宽度为 $n$ 的隐藏层。输出大致是很多神经元贡献的和：

$$
f(x)
=
\sum_{i=1}^n a_i h_i(x).
$$

如果每个项大小都是 $O(1)$，总和会随 $n$ 变大而爆炸。

所以初始化时常需要让权重随宽度缩放，例如 $1/\sqrt n$ 量级。这样前向传播的激活方差不会随着宽度无限增长。

但训练时还要考虑反向传播：

```text
权重初始化怎么缩放
学习率怎么缩放
输出层怎么缩放
不同层的更新量怎么缩放
```

不同选择会导致不同的无限宽极限。NTK 是一种极限，$\mu P$ 试图构造更保留 feature learning 的极限。

## μP 和 scaling law 的关系

$\mu P$ 不是 loss scaling exponent。

更准确的关系是：

```text
scaling law:
    给定一批已经训练好的模型，拟合 loss 随 N/D/C 的下降规律。

μP:
    训练更大模型之前，先规定宽度变化时参数化和超参数如何缩放。
```

它们可以配合使用：

1. 用 $\mu P$ 让不同宽度模型的最优超参数更可迁移。
2. 用小模型调参，减少大模型调参成本。
3. 再用 scaling law 估计大模型训练后的 loss 或能力趋势。

但不要把二者混成一句话：

> scaling exponent 不是 $\mu P$ 的指数，$\mu P$ 也不是 Chinchilla scaling law。

## 和物理类比

物理里研究尺度变化时，常问：

```text
哪些量 relevant？
哪些量 irrelevant？
哪些组合在极限下保持有限？
```

神经网络宽度理论也有类似味道：

```text
宽度 n -> infinity
权重方差如何缩放
学习率如何缩放
输出变化量是否保持 O(1)
```

但这只是类比。神经网络训练不是平衡统计物理系统，$\mu P$ 也不是严格意义上的 RG fixed point。

更准确地说：

> 物理中的尺度分析提供了一种思考方式；NTK 和 $\mu P$ 是神经网络训练动力学里具体可计算的宽度极限理论。

## 已核实来源

- [Neural Tangent Kernel: Convergence and Generalization in Neural Networks](https://arxiv.org/abs/1806.07572)：Jacot, Gabriel, Hongler 2018，提出 NTK，用 kernel 描述无限宽网络的训练动力学。
- [Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer](https://arxiv.org/abs/2203.03466)：Yang et al. 2022，提出 $\mu P$ / $\mu$Transfer 相关方法，核心目标是让很多最优超参数跨模型大小保持稳定。
- [Scaling Law：模型、数据与算力的幂律规律](scaling_laws.md)：本章前一页，讨论 $N,D,C$ 和 loss 的经验幂律。
