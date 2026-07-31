# 模型训练就是函数拟合

神经网络训练可以先不从“智能”或“学习”理解，而是从函数拟合理解：

> 给定一个函数族 $f_\theta$，通过数据或物理目标确定参数 $\theta$。

这里的函数族可以是：

- 多项式。
- 线性模型。
- 张量网络。
- 神经网络。
- 神经网络量子态 $\psi_\theta(x)$。

区别只在于函数形式不同，优化目标不同。

## 监督学习中的函数拟合

给定数据集：

$$
\mathcal D=\{(x_i,y_i)\}_{i=1}^N,
$$

模型为：

$$
\hat y_i=f_\theta(x_i).
$$

训练目标是让预测接近标签：

$$
L(\theta)
=
{1\over N}
\sum_{i=1}^N
\ell(f_\theta(x_i),y_i).
$$

如果是回归，常用：

$$
\ell(\hat y,y)=(\hat y-y)^2.
$$

如果是分类，常用交叉熵：

$$
\ell(z,y)=-\log\mathrm{softmax}(z)_y.
$$

## 参数更新

训练的基本闭环是：

```text
输入 x
  -> forward 得到 f_theta(x)
  -> 计算 loss
  -> backward 得到梯度
  -> optimizer 更新参数
```

数学上写成：

$$
\theta
\leftarrow
\theta-\eta\nabla_\theta L(\theta),
$$

其中 $\eta$ 是学习率。

这一步并不要求你手动求导。现代深度学习框架会通过自动微分计算：

$$
\nabla_\theta L(\theta).
$$

PyTorch 中对应：

```python
loss.backward()
optimizer.step()
```

## 从固定数据到动态数据

监督学习通常有固定数据集：

$$
(x_i,y_i)\sim p_{\rm data}.
$$

训练过程中，数据分布不依赖 $\theta$。这是一种开放式优化：

```text
固定数据 -> loss -> 更新参数
```

但不是所有训练都这样。

在强化学习中，策略 $\pi_\theta(a\mid s)$ 会影响下一批轨迹。参数变了，采样到的状态和动作也会变。

在 VMC / NQS 中，采样分布是：

$$
p_\theta(x)=|\psi_\theta(x)|^2.
$$

参数 $\theta$ 更新后，波函数变了，下一轮样本也变。这就是闭环训练：

```text
当前参数 -> 当前分布 -> 采样 -> 目标估计 -> 更新参数 -> 新分布
```

## 变分视角

很多物理问题不是拟合标签，而是最小化一个泛函。例如 VMC 中：

$$
E(\theta)
=
{\langle\psi_\theta|H|\psi_\theta\rangle
\over
\langle\psi_\theta|\psi_\theta\rangle}.
$$

训练目标变成：

$$
\theta^\star
=
\arg\min_\theta E(\theta).
$$

这仍然是函数拟合，只是“标签”不再来自外部数据，而来自物理目标：基态能量最小。

## 统一表

| 场景 | 函数 | 优化目标 |
| --- | --- | --- |
| 回归 | $f_\theta(x)$ | MSE 最小 |
| 分类 | $p_\theta(y\mid x)$ | 交叉熵最小 |
| 语言模型 | $p_\theta(t_i\mid t_{<i})$ | next-token loss 最小 |
| 强化学习 | $\pi_\theta(a\mid s)$ | reward 最大 |
| VMC / NQS | $\psi_\theta(x)$ | 能量最小 |

因此，理解训练系统时可以先问：

1. 模型表示什么函数？
2. 输入和输出是什么？
3. 目标函数是什么？
4. 样本分布是否依赖当前参数？

这四个问题决定了训练问题的结构。

