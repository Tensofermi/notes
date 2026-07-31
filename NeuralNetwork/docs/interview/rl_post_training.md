# 强化学习与后训练题

强化学习题在通用 AI 岗里通常不会考完整理论，而是考你是否理解“训练信号来自环境反馈或偏好反馈”。大模型后训练里，SFT、reward model、PPO、DPO 也经常一起被问。

## 题目：策略、价值函数和奖励分别是什么？

**来源背景**：RL 基础面试题改写。

**考点定位**：MDP、policy、value、reward。

**先给结论**：

- 策略 $\pi(a\mid s)$：在状态 $s$ 下选择动作 $a$ 的概率。
- 奖励 $r$：环境给出的即时反馈。
- 价值函数 $V^\pi(s)$：从状态 $s$ 出发按策略 $\pi$ 行动的长期期望回报。

**解题思路**：

折扣回报：

$$
G_t=\sum_{k=0}^{\infty}\gamma^k r_{t+k}.
$$

状态价值：

$$
V^\pi(s)=\mathbb E_\pi[G_t\mid s_t=s].
$$

动作价值：

$$
Q^\pi(s,a)=\mathbb E_\pi[G_t\mid s_t=s,a_t=a].
$$

**易错点**：

- reward 是即时反馈，return 是长期累计。
- value 不是环境直接给的，而是估计出来的。

**关联阅读**：[策略、价值函数与环境交互](../rl/policy_value_environment.md)。

## 题目：为什么 reward shaping 可能有风险？

**来源背景**：游戏 AI / 强化学习面试题改写。

**考点定位**：奖励设计、目标错位。

**先给结论**：reward shaping 能加速学习，但如果奖励设计不当，智能体可能优化代理目标而不是最终目标。

**解题思路**：

例如小车上山任务，如果只奖励“速度大”，智能体可能学会来回摆动但不上山。如果只惩罚时间，可能导致策略过于激进。

好的 reward shaping 应该：

- 与最终目标方向一致。
- 不鼓励钻空子。
- 尺度适中。
- 能在 sparse reward 下提供学习信号。

**易错点**：

- reward 高不代表行为符合人类意图。
- 稀疏奖励难学，密集奖励容易错设目标。

**关联阅读**：[奖励函数设计](../rl/reward_design.md)。

## 题目：策略梯度为什么可以优化不可导环境？

**来源背景**：RL 目标函数面试题改写。

**考点定位**：log-derivative trick、采样估计。

**先给结论**：策略梯度不需要环境对动作可导，它对策略概率求导，通过采样轨迹的回报来估计梯度。

**解题思路**：

目标：

$$
J(\theta)=\mathbb E_{\tau\sim p_\theta(\tau)}[R(\tau)].
$$

梯度：

$$
\nabla_\theta J
=
\mathbb E
\left[
R(\tau)\nabla_\theta\log p_\theta(\tau)
\right].
$$

若环境转移不依赖 $\theta$，则：

$$
\nabla_\theta\log p_\theta(\tau)
=
\sum_t\nabla_\theta\log\pi_\theta(a_t\mid s_t).
$$

**易错点**：

- 不需要对环境求导，但需要对策略网络求导。
- 方差通常很大，所以要 baseline 或 advantage。

**关联阅读**：[目标函数、折扣回报与策略梯度](../rl/objective_policy_gradient.md)。

## 题目：PPO 中 $r_t(\theta)$ 是什么？

**来源背景**：RLHF / PPO 面试题改写。

**考点定位**：重要性采样、策略更新约束。

**先给结论**：

$$
r_t(\theta)
=
{\pi_\theta(a_t\mid s_t)\over\pi_{\theta_{\rm old}}(a_t\mid s_t)}.
$$

它表示新策略相对旧策略对同一动作的概率变化。

**解题思路**：

若 $A_t>0$，动作比预期好，希望 $r_t$ 增大。若 $A_t<0$，动作比预期差，希望 $r_t$ 减小。

PPO 使用 clip：

$$
\mathrm{clip}(r_t,1-\epsilon,1+\epsilon)
$$

限制策略一步变化过大。

**易错点**：

- PPO 不是简单“奖励越大越更新”，它还限制新旧策略距离。
- $r_t$ 是概率比，不是 reward 比。

**关联阅读**：[PPO 的基本动机](../rl/ppo.md)。

## 题目：RLHF 为什么需要 KL 约束？

**来源背景**：大模型后训练题改写。

**考点定位**：策略漂移、参考模型、分布约束。

**先给结论**：KL 约束防止模型为了追求 reward 过度偏离原始语言模型，降低语言质量崩坏和 reward hacking 风险。

**解题思路**：

后训练目标常包含：

$$
\mathbb E[R(x,y)]
-
\beta D_{\rm KL}
\left(
\pi_\theta(\cdot\mid x)
\Vert
\pi_{\rm ref}(\cdot\mid x)
\right).
$$

第一项鼓励高 reward，第二项限制模型不要离参考模型太远。

**易错点**：

- reward model 本身可能被利用。
- KL 系数太大，模型学不动；太小，模型容易漂移。

**关联阅读**：[统计物理视角下的大模型训练](../physics_ml/statphys_llm_training.md)。

## 题目：SFT 和 RLHF 的训练信号有什么不同？

**来源背景**：LLM 后训练基础题改写。

**考点定位**：监督学习、偏好优化、强化学习。

**先给结论**：SFT 的训练信号是“标准答案 token”；RLHF 的训练信号是“回答好坏的偏好或 reward”。

**解题思路**：

SFT loss：

$$
L_{\rm SFT}
=
-\sum_i\log\pi_\theta(y_i\mid x,y_{<i}).
$$

RLHF 优化：

$$
\max_\theta
\mathbb E_{y\sim\pi_\theta}
[R(x,y)]
-
\beta D_{\rm KL}(\pi_\theta\Vert\pi_{\rm ref}).
$$

**易错点**：

- SFT 是 teacher forcing，训练时看到标准前缀。
- RLHF 的样本来自当前策略或旧策略采样。

**关联阅读**：[概述](../index.md)。

## 题目：VMC 和强化学习有什么相似点？

**来源背景**：NNQS 与 RL 交叉理解题改写。

**考点定位**：自采样、目标信号、分布依赖参数。

**先给结论**：二者都不是简单固定数据集监督学习。样本分布依赖当前参数，训练信号来自环境或物理目标。

**解题思路**：

RL：

```text
policy_theta
  -> sample trajectory
  -> reward
  -> update theta
```

VMC：

```text
psi_theta
  -> sample configurations from |psi_theta|^2
  -> local energy
  -> update theta
```

零温 VMC 最小化能量，RL 通常最大化 reward。

**易错点**：

- VMC 的目标来自 Hamiltonian，不是人工 reward。
- 两者梯度估计形式有相似直觉，但物理含义不同。

**关联阅读**：[VMC 的闭环训练视角](../vmc_closed_loop.md)。

## 题目：DPO 和 PPO 式 RLHF 的区别是什么？

**来源背景**：大模型后训练面试题改写。

**考点定位**：偏好优化、reward model、在线 / 离线训练。

**先给结论**：PPO 式 RLHF 通常显式训练 reward model，并用策略梯度优化模型；DPO 直接用偏好数据构造分类式目标，绕开显式 reward model 和在线 RL 采样流程。

**解题思路**：

偏好数据通常形如：

```text
prompt x
chosen response y_w
rejected response y_l
```

DPO 的直觉是：提高 chosen 相对 rejected 的概率，同时用 reference model 控制偏离程度。它把偏好优化写成一个稳定的监督学习式目标。

PPO 式 RLHF 流程更像：

```text
policy 生成回答
  -> reward model 打分
  -> PPO 更新 policy
  -> KL 限制偏离 reference
```

DPO 流程更像：

```text
固定偏好数据
  -> 比较 chosen / rejected 的 log probability
  -> 直接优化策略
```

**易错点**：

- DPO 不是普通 SFT，它使用成对偏好。
- PPO 不是只最大化 reward，还需要 KL 或 clip 限制。
- DPO 更简单稳定，但效果仍依赖偏好数据质量和 reference model。

**关联阅读**：[强化学习与后训练题](rl_post_training.md)。
