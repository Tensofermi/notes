# 策略、价值函数与环境交互

强化学习研究智能体如何通过和环境交互学习策略。

基本循环：

```text
state -> policy -> action -> environment -> reward, next state
```

## 基本对象

| 对象 | 记号 | 含义 |
| --- | --- | --- |
| 状态 | $s$ | 环境当前信息 |
| 动作 | $a$ | 智能体选择 |
| 奖励 | $r$ | 环境反馈 |
| 策略 | $\pi_\theta(a\mid s)$ | 给定状态选择动作的概率 |
| 转移 | $P(s'\mid s,a)$ | 环境动力学 |

策略是一个条件分布：

$$
\pi_\theta(a\mid s).
$$

这和语言模型的：

$$
p_\theta(t_i\mid t_{<i})
$$

形式相似，只是条件从文本前缀变成环境状态。

## CartPole 例子

CartPole 中，状态可以包含：

```text
小车位置
小车速度
杆子角度
杆子角速度
```

动作通常是：

```text
向左推
向右推
```

策略网络输入状态，输出两个动作的 logits：

```python
import torch
from torch import nn

policy = nn.Sequential(
    nn.Linear(4, 32),
    nn.Tanh(),
    nn.Linear(32, 2),
)

state = torch.randn(1, 4)
logits = policy(state)
probs = torch.softmax(logits, dim=-1)

print(probs)
```

## 回报

强化学习优化的不是单步奖励，而是长期回报：

$$
G_t
=
\sum_{k=0}^{\infty}
\gamma^k r_{t+k}.
$$

其中 $\gamma\in[0,1]$ 是折扣因子。

折扣因子的作用：

- 保证无限和可控。
- 表达当前奖励比远期奖励更重要。
- 让递推结构更稳定。

## 价值函数

状态价值函数：

$$
V^\pi(s)
=
\mathbb E_\pi[G_t\mid s_t=s].
$$

动作价值函数：

$$
Q^\pi(s,a)
=
\mathbb E_\pi[G_t\mid s_t=s,a_t=a].
$$

策略告诉你怎么行动，价值函数评估状态或动作有多好。

更完整的推导，包括马尔可夫过程、马尔可夫奖励过程、MDP、Bellman 期望方程和 Monte Carlo 价值估计，见 [强化学习中的 Monte Carlo](monte_carlo.md)。

如果想看一个完整代码实践，可以继续读 [实践：AlphaZero 五子棋代码导读](alphazero_gomoku.md)。那一页把五子棋写成 MDP，并展示自我对弈、MCTS、策略价值网络和训练循环如何拼成一个强化学习系统。

如果关心大模型和机器人结合的方向，可以读 [机器人 Scaling Law 与具身智能](robotics_scaling.md)。那一页讨论为什么机器人不能只照搬语言模型 scaling law，以及 Vision-Language-Action 模型、跨 embodiment 数据和环境多样性为什么重要。

## 与监督学习的差别

监督学习通常有固定标签：

$$
(x_i,y_i).
$$

强化学习没有直接告诉每个状态下的正确动作。它只给 reward，策略需要通过交互发现哪些动作长期更好。

因此 RL 的困难来自：

- 样本由当前策略产生。
- reward 可能延迟。
- 探索和利用需要平衡。
- 目标是长期回报，不是单步误差。

## 部分可观测和 belief state

上面的写法默认智能体能看到完整状态 $s_t$。如果只能看到观测 $o_t$，问题就变成部分可观测 MDP，也就是 POMDP。

这时智能体不能直接知道真实状态，只能维护一个 belief state：

$$
b_t(s)
=
P(s_t=s\mid o_1,a_1,o_2,a_2,\ldots,o_t).
$$

它表示：

> 在当前所有观测和动作历史下，真实状态是 $s$ 的概率。

因此 belief state 是一种统计推断对象：智能体用历史信息推断当前隐藏状态，再基于这个概率分布做决策。更一般的 inference、belief 和 belief propagation 见 [推断、统计推断与信念传播](../prerequisites/inference_belief_propagation.md)。
