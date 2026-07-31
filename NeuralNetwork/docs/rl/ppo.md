# PPO 的基本动机

PPO 是 Proximal Policy Optimization。它的目标是在更新策略时避免一步走太远。

## 为什么需要限制更新幅度

策略梯度会提高高 advantage 动作的概率。但如果更新太大，新策略可能和旧策略差别很大，导致采样数据不再可靠。

PPO 的核心思想：

> 允许策略变好，但限制新旧策略概率比不要偏离太多。

## 概率比

定义：

$$
r_t(\theta)
=
{\pi_\theta(a_t\mid s_t)
\over
\pi_{\theta_{\rm old}}(a_t\mid s_t)}.
$$

如果 $r_t=1$，说明新旧策略对这个动作的概率相同。

如果 $r_t>1$，新策略更倾向该动作。

如果 $r_t<1$，新策略降低了该动作概率。

## 未裁剪目标

普通重要性采样形式可写成：

$$
L(\theta)
=
\mathbb E
\left[
r_t(\theta)A_t
\right].
$$

当 $A_t>0$，希望增加动作概率。  
当 $A_t<0$，希望降低动作概率。

## Clip 目标

PPO 使用裁剪：

$$
L^{\rm clip}(\theta)
=
\mathbb E
\left[
\min
\left(
r_t(\theta)A_t,
\mathrm{clip}(r_t(\theta),1-\epsilon,1+\epsilon)A_t
\right)
\right].
$$

这会限制 $r_t$ 偏离 1 的范围。

直觉：

- 好动作可以提高概率，但不能无限提高。
- 坏动作可以降低概率，但不能一步降太多。
- 更新保持在旧策略附近。

## PPO 不是完整 RL 教程

PPO 实际实现还会包含：

- value loss。
- entropy bonus。
- advantage estimation。
- 多轮 epoch 更新。
- trajectory buffer。

本站只需要掌握 PPO 的核心动机：用概率比和 clip 约束策略更新幅度。

## 招聘考点

!!! question "代表题：PPO 中的 $r_t(\theta)$ 是什么？"
    $r_t(\theta)=\pi_\theta(a_t\mid s_t)/\pi_{\theta_{\rm old}}(a_t\mid s_t)$，表示新策略相对旧策略对同一动作的概率变化。PPO clip 目标限制这个比值偏离 1 的幅度，从而避免策略一步更新过大。完整题解见 [强化学习与后训练题](../interview/rl_post_training.md)。
