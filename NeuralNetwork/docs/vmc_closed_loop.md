# VMC 的闭环训练视角

VMC 和普通监督学习的关键区别是：样本分布依赖当前参数。

监督学习通常使用固定数据集：

```text
固定数据 -> loss -> gradient -> update
```

VMC 使用当前波函数定义采样分布：

```text
theta -> psi_theta -> p_theta -> sample -> local energy -> gradient -> update theta
```

参数更新后，下一轮采样分布也会改变。

## 普通函数拟合

监督学习中：

$$
L(\theta)
=
{1\over N}\sum_i
\ell(f_\theta(x_i),y_i).
$$

数据 $(x_i,y_i)$ 通常固定。训练只是改变函数 $f_\theta$。

## VMC 目标

VMC 中模型表示波函数：

$$
\psi_\theta(x).
$$

目标是最小化能量：

$$
E(\theta)
=
{\langle\psi_\theta|H|\psi_\theta\rangle
\over
\langle\psi_\theta|\psi_\theta\rangle}.
$$

写成采样形式：

$$
E(\theta)
=
\sum_x p_\theta(x)E_{\rm loc}(x),
$$

其中：

$$
p_\theta(x)
=
{|\psi_\theta(x)|^2\over\sum_{x'}|\psi_\theta(x')|^2},
$$

$$
E_{\rm loc}(x)
=
\sum_{x'}H_{xx'}
{\psi_\theta(x')\over\psi_\theta(x)}.
$$

## 闭环结构

一轮 VMC：

```text
当前 theta
  -> 定义 psi_theta(x)
  -> 定义 p_theta(x)=|psi_theta(x)|^2
  -> 从 p_theta 采样构型
  -> 计算 local energy
  -> 估计 energy mean 和梯度
  -> 更新 theta
  -> 回到第一步
```

这是自洽闭环，因为模型既定义目标估计所需的采样分布，又被这个估计更新。

## 梯度结构

VMC log-derivative 梯度：

$$
\nabla_\theta E
=
2\,\mathrm{Re}
\left[
\left\langle
(E_{\rm loc}(x)-E)
\nabla_\theta\log\psi_\theta(x)^*
\right\rangle_{p_\theta}
\right].
$$

和策略梯度类似，它包含：

```text
log probability / log wavefunction 的梯度
×
一个质量信号
```

强化学习中质量信号是 return 或 advantage。  
VMC 中质量信号是 local energy 和平均能量的差。

## 和当前代码的关系

教学版训练循环可读成：

```text
_sample_states()
  -> 根据当前模型采样

_evaluate_energy()
  -> 计算 psi 和 local energy

_vmc_loss_proxy()
  -> 构造能产生 VMC 梯度的 proxy loss

_optimizer_step()
  -> backward + optimizer.step
```

更具体的变量对应见 [VMC 训练](vmc_training.md)。

## 为什么这件事重要

闭环采样会带来额外问题：

- 样本质量依赖当前模型。
- 模型初期可能采不到重要构型。
- 参数更新会改变后续训练数据。
- 能量估计有 Monte Carlo 噪声。
- 训练稳定性依赖采样数、学习率和数值精度。

因此 VMC 调试不能只看 loss。更重要的是看：

- `energy_real` 是否下降。
- `energy_imag` 是否接近 0。
- `n_unique` 是否合理。
- local energy 是否出现极端值。
- $\psi_\theta(x')/\psi_\theta(x)$ 是否数值稳定。

