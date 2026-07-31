# 奖励函数设计

奖励函数决定强化学习智能体优化什么。设计不当时，智能体可能学到形式上高分但实际无用的行为。

## 奖励的基本作用

奖励是环境给策略的训练信号：

$$
r_t=r(s_t,a_t,s_{t+1}).
$$

策略目标是最大化期望回报：

$$
J(\theta)
=
\mathbb E_{\pi_\theta}
\left[
\sum_t\gamma^t r_t
\right].
$$

## Sparse Reward

稀疏奖励只在成功或失败时给信号。

CartPole 中可以写成：

```python
reward = 1.0 if not done else 0.0
```

优点是目标清晰。缺点是学习早期很难知道哪些动作有帮助。

## Dense Reward

密集奖励每一步都提供更细反馈。

例如 CartPole：

```python
reward = 1.0
reward -= 0.1 * abs(pole_angle)
reward -= 0.01 * abs(cart_position)
```

这样模型更容易知道杆子越直、位置越居中越好。

风险是：奖励塑形可能改变原本任务目标。

## Reward Shaping

奖励塑形是在原始奖励上加入辅助项，让学习更容易。

原则：

1. 奖励应和真实目标一致。
2. 不要给容易钻空子的代理目标。
3. 尽量让奖励尺度稳定。

MountainCar 中，最终目标是到达山顶。但如果只在成功时奖励，训练很慢。可以加入位置或能量相关的 shaping，让智能体更快学到先后退蓄力再上坡。

## 常见错误

### 奖励只优化局部行为

如果只奖励“杆子角度小”，小车可能跑出边界。

### 奖励尺度过大

某一项奖励太大，会压制其它目标。

### 惩罚过强

如果每个动作都有大惩罚，策略可能学到保守或停滞行为。

## 和物理优化的类比

强化学习最大化 reward。  
VMC 最小化 energy。

可以类比为：

| 强化学习 | VMC |
| --- | --- |
| 策略 $\pi_\theta(a\mid s)$ | 波函数 $\psi_\theta(x)$ |
| trajectory sample | 构型 sample |
| reward | $-E_{\rm loc}$ 的优化信号 |
| maximize return | minimize energy |

这个类比不是严格等价，但能帮助理解：训练信号不一定来自固定标签，也可以来自环境或物理目标。

