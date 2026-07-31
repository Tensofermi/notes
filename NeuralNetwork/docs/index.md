# 神经网络量子态笔记

这套笔记想回答一个贯穿机器学习、Transformer、强化学习、统计物理和 NNQS 的问题：

> 一个复杂系统有太多状态，无法直接穷举；我们能不能用一个可训练的函数 $f_\theta$，把它压缩成可以计算、采样、推断和优化的形式？

先把这句话说得更直白一点。

如果用最傻瓜的办法描述一个概率分布，就是把每一种可能性和它的概率全都存下来：

$$
\{x_1:p(x_1),\ x_2:p(x_2),\ \ldots,\ x_M:p(x_M)\}.
$$

问题是，很多系统的 $M$ 大得离谱。一个 $N$ 个自旋的 Ising 系统有：

$$
2^N
$$

个构型。一个长度为 $T$、词表大小为 $|\mathcal V|$ 的文本空间有：

$$
|\mathcal V|^T
$$

条可能序列。一个量子多体 Hilbert space 的维度也会随自由度指数增长。

如果真的给每个构型、每句话、每个状态都单独存一个概率，那不是“建模”，而是在硬盘里铺一张巨大到不可用的表。

神经网络让人惊讶的地方正在这里：它没有显式存下这张表，而是用一组相对有限的参数 $\theta$ 表示一个函数：

$$
x
\longmapsto
p_\theta(x),
\qquad
x_{<t}
\longmapsto
p_\theta(x_t\mid x_{<t}),
\qquad
x
\longmapsto
\psi_\theta(x).
$$

当然，这并不意味着计算免费。每次查询一个概率、生成一个 token、评估一个构型，仍然要做矩阵乘法、attention、归一化和采样。但关键区别是：

```text
傻瓜式概率表：
  内存里显式存每个状态的概率

神经网络表示：
  参数里隐式存生成这些概率的规律
```

这背后的信念是：虽然状态空间巨大，但真正重要的结构往往没有状态空间本身那么大。语言不是任意 token 的随机堆砌，物理系统不是任意构型都同等重要，图像不是任意像素噪声，策略也不是任意动作表。世界中存在可复用的结构、局部性、对称性、组合规律、因果关系和低复杂度描述。

所以这套笔记的第一层直觉是：

> 神经网络不是把所有答案背下来，而是在巨大可能性空间中学习一个可泛化的压缩表示。

更准确地说：

$$
\boxed{
\text{智能}
\approx
\text{可泛化压缩}
+
\text{预测}
+
\text{行动}
}
$$

压缩不是智能的全部，但智能必然包含压缩。一个系统如果能预测，说明它抓住了某种结构；如果这种结构能迁移到新情景，说明它不只是记忆；如果它还能支持行动和反事实判断，就更接近 agent 或科学理论。

物理学本身就是这种思想的极致例子。Ising 模型没有列举 $2^N$ 个构型的概率，而是用很短的 Hamiltonian 规定权重：

$$
H(\sigma)
=
-J\sum_{\langle ij\rangle}\sigma_i\sigma_j
-h\sum_i\sigma_i.
$$

语言模型也类似。它不可能存下所有句子，而是学习自回归分解：

$$
P_\theta(x_1,\ldots,x_T)
=
\prod_{t=1}^T
P_\theta(x_t\mid x_{<t}).
$$

NNQS 则把量子构型 $x$ 映射到波函数值 $\psi_\theta(x)$，用可训练函数压缩指数大的 Hilbert space。

因此，贯穿本站的主线可以概括为：

```text
巨大状态空间
  -> 不能显式枚举概率表
  -> 寻找低复杂度结构
  -> 用神经网络近似这个结构
  -> 通过数据、奖励或能量信号优化参数
  -> 在新输入上预测、采样、推断或行动
```

这个问题在不同领域里会换不同外衣：

| 场景 | 输入 | 模型输出 | 优化信号 |
| --- | --- | --- | --- |
| 分类模型 | 图片、文本、表格 | $p_\theta(y\mid x)$ | 标签误差 |
| 语言模型 | token 前缀 | $p_\theta(t_i\mid t_{<i})$ | next-token loss |
| 强化学习 | 状态 $s$ | 策略 $\pi_\theta(a\mid s)$ | 长期 reward |
| 统计推断 | 观测数据 $D$ | 后验或 belief | 概率一致性 |
| VMC / NNQS | 量子构型 $x$ | $\psi_\theta(x)$ | 能量最小 |

看起来题材很多，但底层结构很统一：

```text
定义状态
  -> 用概率描述不确定性
  -> 用神经网络表示函数或分布
  -> 用样本估计目标
  -> 用梯度或搜索改进参数
  -> 再回到新的分布继续采样或推断
```

这就是本站的 global picture。

## 一张总图

```text
数学和概率
  -> 熵 / KL / 最大似然 / 推断 / 优化
  -> PyTorch: tensor / autograd / Module / training loop
  -> 经典结构: MLP / CNN / RNN / LSTM / PixelCNN / RBM
  -> Transformer: token / attention / decoder / KV cache
  -> 强化学习: MDP / reward / Monte Carlo / PPO / 机器人 scaling
  -> 神经网络与物理: 统计物理类比 / scaling law / NTK / μP
  -> NNQS: psi_theta(x) / |psi|^2 采样 / VMC 能量优化
  -> 工程和招聘题: infra / 数值精度 / 显存 / 调试 / 高频考点
```

如果只记一个核心式子，可以记：

$$
\text{model}_\theta
\quad
\Longrightarrow
\quad
\text{probability / value / wavefunction}
\quad
\Longrightarrow
\quad
\text{objective}
\quad
\Longrightarrow
\quad
\theta\text{ update}.
$$

神经网络不是孤立的“层堆叠”。它更像一个通用的参数化语言：可以表示分类概率，可以表示 token 条件分布，可以表示策略，也可以表示量子波函数。

## 五个关键词

### 函数

最基本的机器学习图像是函数拟合：

$$
f_\theta:x\mapsto y.
$$

监督学习把 $x$ 映射到标签 $y$，语言模型把前缀映射到下一个 token 分布，NNQS 把构型 $x$ 映射到波函数值 $\psi_\theta(x)$。

所以第一层心智模型是：

> 训练神经网络，就是在一个巨大函数空间里找一个有用的函数。

对应章节：

- [机器学习地图](prerequisites/ml_overview.md)
- [模型训练就是函数拟合](prerequisites/training_as_function_fitting.md)
- [PyTorch 教程总览](pytorch/index.md)
- [MLP：最基本的全连接网络](classic_architectures/mlp.md)

### 概率

神经网络经常不是只输出一个数，而是输出一个分布：

$$
p_\theta(y\mid x),
\qquad
p_\theta(t_i\mid t_{<i}),
\qquad
\pi_\theta(a\mid s),
\qquad
p_\theta(x)=|\psi_\theta(x)|^2.
$$

一旦输出是概率，就会自然遇到熵、交叉熵、KL 散度、最大似然、后验推断、belief、配分函数这些概念。

第二层心智模型是：

> 学习常常是在调整一个概率分布，让它更符合数据、奖励、能量或物理约束。

对应章节：

- [概率分布、熵与配分函数](prerequisites/probability_entropy_partition.md)
- [信息熵、交叉熵与 KL 散度](prerequisites/entropy_cross_entropy_kl.md)
- [最大似然与前向 KL](prerequisites/mle_forward_kl.md)
- [推断、统计推断与信念传播](prerequisites/inference_belief_propagation.md)
- [Scaling Law：模型、数据与算力](physics_ml/scaling_laws.md)

### 结构

模型不是随便搭的。数据结构会强烈影响模型结构：

| 数据 | 结构 | 常见模型 |
| --- | --- | --- |
| 表格 | 特征列 | 线性模型、树模型、MLP |
| 图像 / 格点 | 局部邻域和平移结构 | CNN、ViT |
| 序列 | 顺序和上下文 | RNN、Transformer |
| 图 | 节点和边 | GNN、图模型 |
| 量子构型 | 指数大 Hilbert space | Tensor network、NNQS |

Transformer 的关键，是把一个 token 放到上下文中重新理解：

$$
\text{token}
\xrightarrow{\text{attention}}
\text{contextual representation}.
$$

NNQS 的关键，是用神经网络在指数大构型空间里表示波函数：

$$
x\mapsto\psi_\theta(x).
$$

第三层心智模型是：

> 架构设计是在把问题的结构写进模型。

学习 Transformer 时可以配合两个可视化工具：

| 推荐 | 适合看什么 | 我的建议 |
| --- | --- | --- |
| [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) | GPT 式 Transformer 的整体流程、token、embedding、$Q/K/V$、attention、MLP、next-token prediction | 首推。它是交互式的，适合在浏览器里跟着模型预测下一个 token 的流程走一遍。 |
| [LLM Visualization](https://bbycroft.net/llm) | 3D 方式看 LLM 的矩阵流动、层结构、attention head、残差流 | 适合建立“模型是一个巨大的矩阵流水线”的全局直觉，再回头读公式会更顺。 |

对应章节：

- [经典神经网络结构总览](classic_architectures/index.md)
- [CNN：局部连接、权重共享与特征图](classic_architectures/cnn.md)
- [RNN、GRU 与 LSTM](classic_architectures/rnn_lstm.md)
- [Transformer 笔记总览](Transformer/index.md)
- [Attention 机制](Transformer/attention.md)

### 尺度

当模型、数据和算力都变大之后，神经网络不只是“多堆几层”。规模本身会成为研究对象：

$$
L(N,D)
=
E
+
{A\over N^\alpha}
+
{B\over D^\beta}.
$$

这里 $N$ 是参数量，$D$ 是训练 token 数，$\alpha,\beta$ 描述 loss 随规模下降的速度。Scaling law 的意义是：它让“大模型为什么继续有效”变成可以拟合和推导的问题。

但尺度问题有不同层次：

| 问题 | 典型关键词 |
| --- | --- |
| 固定 compute 怎么分配模型和数据 | Chinchilla、compute-optimal scaling |
| 宽度变大时训练动力学如何保持稳定 | NTK、$\mu P$、power counting |
| 机器人能不能像语言模型一样 scale | VLA、Open X-Embodiment、embodiment diversity |

第四层心智模型是：

> 规模化学习不是只看参数量，而是参数、数据、算力、优化动力学和任务多样性的共同问题。

对应章节：

- [Scaling Law：模型、数据与算力](physics_ml/scaling_laws.md)
- [NTK、μP 与无限宽极限](physics_ml/ntk_mup_infinite_width.md)
- [机器人 Scaling Law 与具身智能](rl/robotics_scaling.md)
- [Decoder 的基本结构](Transformer/decoder.md)
- [神经网络发展与统计物理视角](physics_ml/history_statphys.md)
- [CNN 识别量子相变](physics_ml/cnn_quantum_phase.md)

### 采样

很多时候，我们无法直接求全空间的和：

$$
\sum_x p(x)O(x).
$$

状态空间太大，只能采样。

在物理 Monte Carlo 中，样本是构型：

$$
s\sim\pi(s).
$$

在强化学习 Monte Carlo 中，样本是 episode：

$$
\tau=(S_0,A_0,R_1,S_1,\ldots).
$$

在 VMC / NNQS 中，样本来自当前波函数模方：

$$
x\sim p_\theta(x)=|\psi_\theta(x)|^2.
$$

第四层心智模型是：

> 采样是把不可枚举的巨大空间，变成可以估计的有限经验。

对应章节：

- [强化学习中的 Monte Carlo](rl/monte_carlo.md)
- [实践：AlphaZero 五子棋代码导读](rl/alphazero_gomoku.md)
- [VMC 的闭环训练视角](vmc_closed_loop.md)
- [VMC 训练](vmc_training.md)

### 优化

最后，模型要被某个目标牵引：

| 场景 | 目标 |
| --- | --- |
| 分类 | cross entropy 最小 |
| 语言模型 | next-token negative log likelihood 最小 |
| 强化学习 | expected return 最大 |
| 零温 VMC | energy 最小 |
| 有限温变分方法 | free energy 最小 |

这些目标的形式不同，但训练循环都很像：

```text
产生样本或读取 batch
  -> forward
  -> 计算目标
  -> 估计梯度
  -> 更新参数
```

第五层心智模型是：

> 训练就是让参数化对象沿着目标函数的方向移动。

对应章节：

- [优化方法：梯度下降、Gauss-Newton 与 LM](prerequisites/optimization_methods.md)
- [训练循环：forward、backward、optimizer.step](pytorch/training_loop.md)
- [目标函数、折扣回报与策略梯度](rl/objective_policy_gradient.md)
- [统计物理视角下的大模型训练](physics_ml/statphys_llm_training.md)

## 训练和推理

神经网络通常有两种使用模式：训练和推理。

训练时，参数 $\theta$ 会被更新。模型先根据输入样本做 forward，得到输出，再用某个目标信号判断输出好坏，并通过反向传播或其他估计方法调整权重。

| 场景 | 样本来源 | 优化信号 |
| --- | --- | --- |
| 监督学习 | 外部训练集 | loss 最小 |
| 语言模型 | 文本 token 序列 | next-token cross entropy 最小 |
| 强化学习 | 环境交互轨迹 | reward 最大 |
| 零温 VMC / NQS | 当前波函数分布采样 | 能量最小 |
| 有限温变分方法 | 热分布或变分密度矩阵采样 | 自由能最小 |

从概率分布的角度看，训练是在调整一个参数化分布。输入通常作为条件，输出是条件概率下的结果：

$$
p_\theta(y\mid x).
$$

推理时，参数通常固定，不再更新。模型只做 forward：

- 分类模型给出类别概率。
- 语言模型自回归地产生 token。
- 策略网络给出 action。
- NNQS 把输入构型 $x$ 映射到波函数值。

NNQS 中：

$$
x
\longmapsto
\psi_\theta(x)
=
A_\theta(x)e^{i\phi_\theta(x)}.
$$

采样时使用：

$$
p_\theta(x)=|\psi_\theta(x)|^2.
$$

因此，在 NQS 里，训练好的权重本身就是一个压缩的波函数表示。

## NNQS 主线

本站最核心的物理主线是：

```text
薛定谔方程
  -> Hamiltonian 本征值问题
  -> occupation bitstring basis
  -> 神经网络波函数 psi_theta(x)
  -> 按 |psi_theta|^2 采样
  -> local energy 估计能量
  -> VMC 梯度更新参数
```

用一个式子压缩：

$$
x \xrightarrow{\text{model}} \psi_\theta(x),
\qquad
p_\theta(x)\propto|\psi_\theta(x)|^2,
\qquad
E_\theta
=
\mathbb E_{x\sim p_\theta}[E_{\rm loc}(x)].
$$

训练循环就是：

```text
抽样本
  -> 算局域能
  -> 估计平均能量
  -> 构造梯度代理
  -> 更新网络
```

对应章节：

- [从薛定谔方程到 NNQS](from_schrodinger_to_nnqs.md)
- [模型结构](model_architecture.md)
- [VMC 训练](vmc_training.md)
- [VMC 的闭环训练视角](vmc_closed_loop.md)

## 阅读路线

如果从零开始，建议按下面顺序读：

1. [机器学习地图](prerequisites/ml_overview.md)：建立监督学习、自监督、强化学习和变分学习的共同框架。
2. [模型训练就是函数拟合](prerequisites/training_as_function_fitting.md)：理解 $f_\theta$、loss、梯度更新和 VMC 闭环。
3. [推断、统计推断与信念传播](prerequisites/inference_belief_propagation.md)：区分工程 inference、贝叶斯推断、belief 和图模型消息传递。
4. [PyTorch 教程总览](pytorch/index.md)：掌握常用 torch 命令、tensor、autograd、`nn.Module`、训练循环和 `torch.compile` 性能优化。
5. [经典神经网络结构总览](classic_architectures/index.md)：补齐 MLP、CNN、RNN/LSTM、PixelCNN、RBM 这些 Transformer 之前的重要模型。
6. [Transformer 笔记总览](Transformer/index.md)：补足 decoder-only Transformer、自注意力、mask 和 KV cache。
7. [强化学习中的 Monte Carlo](rl/monte_carlo.md)：理解轨迹采样、价值函数、Bellman 方程和 TD 的关系。
8. [从薛定谔方程到 NNQS](from_schrodinger_to_nnqs.md)：建立物理图像，理解为什么用神经网络表示波函数。
9. [模型结构](model_architecture.md)：看清 $\log|\psi_\theta(x)|$、相位和复波函数输出的关系。
10. [VMC 训练](vmc_training.md)：理解 local energy、能量估计和梯度代理。
11. [从模型代码到系统代码](code_walkthrough.md)：从大模型工程背景理解模型、数据、训练、推理和服务代码如何分层。

## 四条专题路线

初学路线：

```text
预备知识
  -> 推断、统计推断与信念传播
  -> PyTorch 教程
  -> 经典神经网络结构
  -> Transformer
  -> NNQS 主线
```

物理路线：

```text
概率分布、熵与 KL
  -> 神经网络与统计物理
  -> CNN / PixelCNN / RBM
  -> 强化学习中的 Monte Carlo
  -> CNN 识别量子相变
  -> NNQS / VMC
```

工程路线：

```text
PyTorch 教程
  -> 数值精度
  -> torch.compile
  -> 大模型 Infra 全景
  -> Transformer KV cache
  -> 从模型代码到系统代码
  -> 工程公式速查
  -> 工程正确性与性能验证
```

招聘备考路线：

```text
预备知识
  -> Transformer / PyTorch / 数值精度
  -> 招聘备考专题
  -> 按华为、字节、米哈游路线查缺补漏
```

对应入口见 [招聘备考专题](interview/index.md)。这个专题不复刻原始真题，而是把公开面经和岗位要求里的高频考点改写成代表题，并把解题思路链接回本站知识页。

## 工程地图

工程导读这一组不再重复 NNQS 主线，而是把视角抬到大模型系统。可以按下面顺序建立全局图像：

```text
模型代码
  Transformer / MLP / Norm / LM head

数据代码
  tokenizer / dataset / dataloader / packing

训练代码
  forward / loss / backward / optimizer / checkpoint

分布式代码
  DDP / FSDP / tensor parallel / pipeline parallel

执行优化
  FlashAttention / fused kernel / torch.compile / CUDA graph

推理系统
  prefill / decode / KV cache / batching / quantization

服务系统
  API / scheduler / streaming / monitoring / rollback
```

对应页面：

- [大模型 Infra 全景：从硬件到服务](infra_overview.md)
- [从模型代码到系统代码](code_walkthrough.md)
- [工程公式速查](formula_cheatsheet.md)
- [工程正确性与性能验证](verification.md)
- [数值精度](numerical_precision.md)

## 最短心智模型

如果把整套笔记压缩成一句话：

> 神经网络提供可训练函数，概率提供不确定性语言，采样处理巨大状态空间，优化给出学习方向，而 NNQS 把这一整套工具用于表示和优化量子波函数。

再压缩成一条公式链：

$$
\text{state}
\xrightarrow{\text{neural network}}
\text{probability / value / wavefunction}
\xrightarrow{\text{sampling}}
\text{expectation}
\xrightarrow{\text{optimization}}
\text{better parameters}.
$$
