# 优化方法：梯度下降、Gauss-Newton 与 LM

训练模型就是优化参数。不同优化方法对目标函数局部形状使用的信息不同。

最常见的梯度下降只使用一阶梯度。Gauss-Newton 和 Levenberg-Marquardt 主要用于最小二乘问题，会近似使用二阶曲率信息。

## 一般优化问题

目标函数写成：

$$
\min_\theta L(\theta).
$$

梯度下降更新为：

$$
\theta_{k+1}
=
\theta_k-\eta\nabla_\theta L(\theta_k).
$$

其中 $\eta$ 是学习率。

梯度下降的优点是简单，适合大规模参数。神经网络中常见 SGD、Adam、AdamW 都是在这个思想上加入动量、自适应学习率或权重衰减。

## 最小二乘问题

很多拟合问题可以写成：

$$
L(\theta)
=
{1\over 2}\|r(\theta)\|^2
=
{1\over 2}\sum_i r_i(\theta)^2,
$$

其中 $r_i(\theta)$ 是 residual。例如：

$$
r_i(\theta)=f_\theta(x_i)-y_i.
$$

令 Jacobian 为：

$$
J_{ij}
=
{\partial r_i\over\partial\theta_j}.
$$

梯度为：

$$
\nabla_\theta L
=
J^{\mathsf T}r.
$$

## Newton 方法

Newton 方法使用 Hessian：

$$
H=\nabla_\theta^2 L.
$$

更新方向 $\Delta\theta$ 满足：

$$
H\Delta\theta=-\nabla_\theta L.
$$

即：

$$
\theta\leftarrow\theta+\Delta\theta.
$$

Newton 方法局部收敛快，但 Hessian 计算和存储代价很高，不适合大型神经网络的完整训练。

## Gauss-Newton

对最小二乘目标，Hessian 可以写成：

$$
H
=
J^{\mathsf T}J
+
\sum_i r_i\nabla_\theta^2 r_i.
$$

Gauss-Newton 忽略第二项，使用近似：

$$
H\approx J^{\mathsf T}J.
$$

于是方向满足：

$$
J^{\mathsf T}J\Delta\theta
=
-J^{\mathsf T}r.
$$

当 residual 已经较小，或者模型在局部接近线性时，这个近似通常有效。

## Levenberg-Marquardt

Levenberg-Marquardt 在 Gauss-Newton 上加入阻尼：

$$
(J^{\mathsf T}J+\lambda I)\Delta\theta
=
-J^{\mathsf T}r.
$$

当 $\lambda$ 很小时，它接近 Gauss-Newton。  
当 $\lambda$ 很大时，它接近梯度下降。

因此 LM 可以看成在两种行为之间插值：

| $\lambda$ | 行为 |
| --- | --- |
| 小 | 更相信二阶近似，步子更像 Gauss-Newton。 |
| 大 | 更保守，步子更像梯度下降。 |

## 和神经网络优化的关系

大型神经网络一般不用完整 Gauss-Newton 或 LM，原因是：

- 参数量太大，$J^{\mathsf T}J$ 难以存储。
- mini-batch 噪声较大，精确二阶信息不稳定。
- GPU 上一阶方法更容易扩展。

但二阶思想仍然重要：

- 自然梯度使用 Fisher 信息矩阵修正方向。
- K-FAC 近似二阶曲率。
- VMC 中 stochastic reconfiguration 和自然梯度形式接近。
- Adam 的二阶矩估计虽然不是 Hessian，但也在自适应缩放梯度。

## 拟合优度

物理和数值拟合中常看残差是否合理。如果观测误差为 $\sigma_i$，可定义：

$$
\chi^2
=
\sum_i
\left({y_i-f_\theta(x_i)\over\sigma_i}\right)^2.
$$

自由度为：

$$
\mathrm{dof}=N-p,
$$

其中 $N$ 是数据点数，$p$ 是拟合参数数。

归一化卡方：

$$
\chi^2_{\rm red}
=
{\chi^2\over\mathrm{dof}}.
$$

如果误差模型正确，$\chi^2_{\rm red}$ 接近 1 通常表示拟合合理。

## 实用判断

| 问题 | 常用方法 |
| --- | --- |
| 大规模神经网络 | SGD、Adam、AdamW |
| 小规模非线性最小二乘 | Gauss-Newton、LM |
| 物理变分优化 | 梯度下降、自然梯度、stochastic reconfiguration |
| 需要拟合优度检验 | $\chi^2/\mathrm{dof}$ |

后续 PyTorch 教程中的训练循环主要使用一阶优化器；VMC 章节会再说明能量目标下的梯度代理。

## 招聘考点

!!! question "代表题：Adam 和 AdamW 的区别是什么？"
    Adam 使用梯度一阶矩和二阶矩来自适应缩放更新；AdamW 将 weight decay 从 Adam 的梯度更新中解耦出来。SGD 中 L2 正则和 weight decay 近似等价，但 Adam 的自适应缩放会改变 L2 项的效果，所以大模型训练中更常用 AdamW。完整题解见 [深度学习与训练题](../interview/deep_learning_training.md)。
