# 机器人 Scaling Law 与具身智能

LLM scaling law 主要关心：

$$
L=f(N,D,C),
$$

也就是模型参数量、训练 token 数和训练 compute 如何影响语言模型 loss。

机器人也可以讨论 scaling law，但它更复杂。因为机器人不是只在文本空间里预测下一个 token，而是在物理世界中接收观测、产生动作，并受到环境动力学约束。

## 机器人 scaling 的目标变量

语言模型常看 cross-entropy loss。机器人任务更常看：

| 指标 | 含义 |
| --- | --- |
| success rate | 任务成功率 |
| action error | 动作误差 |
| episode return | 一段轨迹的累计回报 |
| failure rate | 失败率 |
| generalization gap | 新环境、新物体、新机器人上的性能下降 |

如果用失败率 $\epsilon$ 表示模型还有多少没学好，可以写一个类 scaling law 的形式：

$$
\epsilon
=
\epsilon_\infty
+
{A\over N^{\alpha_N}}
+
{B\over D^{\alpha_D}}
+
{C_E\over E^{\alpha_E}}
+
{C_O\over O^{\alpha_O}}
+
{C_B\over B_{\rm emb}^{\alpha_B}}
+
\cdots.
$$

其中：

| 符号 | 含义 |
| --- | --- |
| $N$ | 模型参数量 |
| $D$ | 轨迹数据量 |
| $E$ | 环境多样性 |
| $O$ | 物体多样性 |
| $B_{\rm emb}$ | embodiment 多样性，也就是机器人身体和动作空间的覆盖 |
| $\epsilon_\infty$ | 当前任务定义和数据条件下难以继续降低的误差下限 |

这个公式不是标准定理，而是帮助理解：机器人 scaling 不能只看参数量。

## 为什么机器人比语言模型更难 scale？

语言模型训练样本通常是：

```text
文本前缀 -> 下一个 token
```

机器人训练样本更像：

```text
图像 / 语言 / proprioception / 历史动作
    -> 连续动作
    -> 物理环境变化
    -> 成败反馈
```

复杂性至少来自五个方面。

第一，数据更贵。文本可以从互联网大规模收集，机器人轨迹需要真实设备、仿真、遥操作或人类视频。

第二，动作会改变数据分布。语言模型预测错一个 token 不会改变互联网文本本身；机器人选错动作会改变下一步状态，甚至导致任务失败。

第三，环境和物体有长尾。换一个杯子、桌面、光照、机械臂、夹爪，任务难度都可能变化。

第四，机器人身体不同。不同机器人的自由度、控制频率、动作空间、传感器都不同。

第五，安全约束更强。真实机器人错误不只是 loss 变大，还可能损坏设备或造成危险。

所以机器人 scaling 的核心不是简单堆参数，而是：

> 数据多样性、环境多样性、任务多样性、物体多样性和 embodiment coverage 一起决定模型能否泛化。

## VLA：Vision-Language-Action 模型

机器人基础模型里经常出现 VLA，也就是 Vision-Language-Action。

它的输入通常包括：

```text
视觉观测
语言指令
机器人状态
历史动作
```

输出是：

```text
机器人动作
```

RT-2 的一个关键想法是：把机器人动作表示成 token，让模型在 vision-language 预训练知识和机器人控制数据之间建立统一接口。

这和 LLM 的 next-token prediction 有相似之处：

$$
p_\theta(t_i\mid t_{<i})
$$

变成了更具身的条件分布：

$$
\pi_\theta(a_t\mid o_{\le t},\,{\rm instruction}).
$$

但动作可以是连续的、高频的、受物理约束的。因此很多新模型会结合 diffusion、flow matching 或专门的 action head。

## Open X-Embodiment 的意义

传统机器人学习经常是：

```text
一个机器人
一个任务
一个数据集
一个专门策略
```

这会导致模型泛化能力差。Open X-Embodiment / RT-X 的目标是把来自多个机器人、多个机构、多个技能的数据标准化到一个更大的机器人学习数据生态中。

它的重要性不只在“数据更多”，而在：

```text
身体更多
任务更多
物体更多
环境更多
数据格式更统一
```

这正是机器人 scaling law 中最缺的东西：多样性。

## 代表模型脉络

| 模型 / 项目 | 核心思想 |
| --- | --- |
| RT-2 | 把 vision-language 模型接到机器人动作，把动作表示为 token，从 web-scale 语义知识迁移到控制 |
| Open X-Embodiment / RT-X | 聚合多机器人、多机构、多技能数据，研究跨 embodiment 的机器人策略 |
| Octo | 开源 generalist robot policy，基于 Open X-Embodiment 轨迹训练，可微调到新机器人和新动作空间 |
| $\pi_0$ | 在预训练 VLM 上构建 flow matching 架构，用于 general robot control |
| GR00T N1 | 面向 humanoid 的 VLA foundation model，混合真实轨迹、人类视频和合成数据训练 |

这些工作共同体现了一个方向：

> 机器人学习正在从单任务策略，走向跨任务、跨平台、跨数据源的 foundation policy。

## 和强化学习的关系

机器人 foundation model 不一定全靠强化学习训练。很多时候会混合：

| 训练方式 | 作用 |
| --- | --- |
| imitation learning | 从专家轨迹学习动作 |
| behavior cloning | 直接拟合观测到动作的映射 |
| offline RL | 从离线轨迹中估计更优策略 |
| online RL | 和环境交互继续优化 |
| RLHF / preference learning | 用人类偏好或打分改善策略 |
| diffusion / flow matching | 生成连续动作轨迹 |

因此，机器人 scaling 和强化学习的关系是：

```text
RL 提供环境交互和长期回报语言
模仿学习提供大规模监督信号
VLA / foundation model 提供跨任务表示和泛化能力
```

## 为什么不能直接照搬 LLM scaling？

LLM 的一个训练样本通常可以从文本中自动切出来：

$$
(x_{<t},x_t).
$$

机器人轨迹样本则包含：

$$
(o_t,a_t,r_{t+1},o_{t+1}).
$$

而且动作 $a_t$ 会改变未来观测：

$$
o_{t+1}\sim P(\cdot\mid o_t,a_t).
$$

所以机器人不仅要学分布，还要学在分布中行动。它的 scaling 不能只看“数据量有多少”，还要看数据是否覆盖了足够多的状态、动作和失败模式。

这也是为什么机器人 scaling 里经常强调：

- sim-to-real。
- long-horizon task。
- real-time control。
- safety。
- embodiment transfer。
- 多模态观测和连续动作。

## 和本章其它内容的连接

从强化学习角度看，机器人任务可以写成 MDP 或 POMDP：

$$
S_t \to A_t \to R_{t+1},S_{t+1}.
$$

策略是：

$$
\pi_\theta(a\mid s).
$$

在部分可观测情形下，策略更接近：

$$
\pi_\theta(a_t\mid o_{\le t},a_{<t},{\rm instruction}).
$$

这和 [策略、价值函数与环境交互](policy_value_environment.md)、[强化学习中的 Monte Carlo](monte_carlo.md)、[PPO 的基本动机](ppo.md) 是同一套语言。

从大模型角度看，VLA 又继承了 [Transformer](../Transformer/index.md) 和 [Scaling Law](../physics_ml/scaling_laws.md) 的思想：用大模型和大数据学习一个可泛化的条件分布。

## 已核实来源

- [Neural Scaling Laws in Robotics](https://arxiv.org/abs/2405.14005)：Sartor & Thompson 2024，研究机器人任务中的 neural scaling laws。
- [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864)：跨机器人平台的大规模机器人学习数据和 RT-X 模型。
- [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)：把 vision-language 模型和机器人控制结合的 VLA 工作。
- [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)：基于 Open X-Embodiment 训练的开源 generalist robot policy。
- [$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164)：基于预训练 VLM 和 flow matching 的 general robot control 模型。
- [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734)：NVIDIA 面向 humanoid 的 VLA foundation model。
