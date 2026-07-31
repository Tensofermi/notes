# 目标函数、折扣回报与策略梯度

强化学习的目标是找到策略：

$$
\pi_\theta(a\mid s),
$$

使长期回报最大。

## 折扣回报

从时间 $t$ 开始的回报：

$$
G_t
=
\sum_{k=0}^{\infty}
\gamma^k r_{t+k}.
$$

折扣因子 $\gamma$ 的作用：

- 保证无限时间问题可控。
- 让近期 reward 权重更高。
- 形成 Bellman 递推。

Bellman 形式：

$$
G_t=r_t+\gamma G_{t+1}.
$$

## 策略目标

目标函数：

$$
J(\theta)
=
\mathbb E_{\tau\sim\pi_\theta}
[G(\tau)].
$$

其中 $\tau$ 是轨迹：

$$
\tau=(s_0,a_0,r_0,s_1,a_1,r_1,\ldots).
$$

## 策略梯度

策略梯度定理给出一种形式：

$$
\nabla_\theta J(\theta)
=
\mathbb E_{\pi_\theta}
\left[
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
Q^{\pi_\theta}(s_t,a_t)
\right].
$$

直觉：

- 如果某个动作带来高回报，就提高它的 log probability。
- 如果某个动作带来低回报，就降低它的 log probability。

这和 VMC 梯度中出现的 log-derivative 结构相似。

## Baseline

为了降低方差，常减去 baseline：

$$
A(s_t,a_t)=Q(s_t,a_t)-V(s_t).
$$

于是：

$$
\nabla_\theta J(\theta)
=
\mathbb E
\left[
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
A(s_t,a_t)
\right].
$$

$A$ 称为 advantage，表示动作比当前状态平均水平好多少。

如果不使用 bootstrap，也可以用完整 episode 的实际回报来估计 $Q$ 或 advantage。这就是 Monte Carlo value estimation 的基本思想，详见 [强化学习中的 Monte Carlo](monte_carlo.md)。

## 和最大似然的差别

语言模型训练最大化数据 token 的概率：

$$
\log p_\theta(t_i\mid t_{<i}).
$$

策略梯度最大化高回报动作的概率：

$$
\log \pi_\theta(a_t\mid s_t)
\times
\text{advantage}.
$$

因此两者都有“提高某些输出概率”的结构，但权重来源不同：

- 语言模型来自数据标签。
- RL 来自环境回报。

并不是所有强化学习都直接用这条 policy gradient 公式更新策略。AlphaZero 风格方法会先用 MCTS 把当前网络策略改进成搜索策略，再让网络用监督损失拟合搜索结果。具体代码闭环见 [实践：AlphaZero 五子棋代码导读](alphazero_gomoku.md)。

在机器人 foundation model 中，策略也常写成条件分布 $\pi_\theta(a_t\mid o_{\le t},{\rm instruction})$，但训练信号可能混合模仿学习、离线 RL、在线 RL、偏好学习和生成式动作建模。这个更大背景见 [机器人 Scaling Law 与具身智能](robotics_scaling.md)。
