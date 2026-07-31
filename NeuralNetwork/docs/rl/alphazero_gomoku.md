# 实践：AlphaZero 五子棋代码导读

这一节参考 [junxiaosong/AlphaZero_Gomoku](https://github.com/junxiaosong/AlphaZero_Gomoku)，把强化学习从公式拉回到一套可以读懂、可以运行、可以改造的代码结构里。

这个项目实现的是一个简化版 AlphaZero：不用人类棋谱，从自我对弈开始训练五子棋智能体。五子棋比围棋和国际象棋小很多，所以它适合作为理解 AlphaZero 训练闭环的实践入口。项目 README 也明确说，它的目的就是在简单棋类上聚焦 AlphaZero 的训练 scheme。

先给整体结论：

```text
当前棋盘 s
  -> 神经网络 f_theta(s) 输出先验策略 p 和局面价值 v
  -> MCTS 用 p 和 v 搜索，得到更强的落子分布 pi
  -> 按 pi 自我对弈，走完整盘棋，得到胜负结果 z
  -> 保存训练样本 (s, pi, z)
  -> 用神经网络拟合 pi 和 z
  -> 新网络继续指导下一轮 MCTS 和自我对弈
```

这套结构的关键不是某一个模块，而是一个闭环：

$$
f_\theta
\xrightarrow{\text{指导搜索}}
\pi_{\text{MCTS}}
\xrightarrow{\text{自我对弈}}
(s,\pi,z)
\xrightarrow{\text{监督训练}}
f_{\theta'}
$$

所以 AlphaZero 并不是普通的“策略梯度直接从 reward 反传”。它更像是：

> 用搜索把当前网络变强一点，再让网络模仿搜索后的结果。

## 代码文件地图

项目核心文件可以按功能分成四层：

| 文件 | 角色 | 对应强化学习概念 |
| --- | --- | --- |
| `game.py` | 五子棋棋盘、合法动作、胜负判断、自我对弈接口 | 环境、状态、动作、episode |
| `mcts_alphaZero.py` | AlphaZero 风格 MCTS | 搜索、策略改进、exploration |
| `policy_value_net_pytorch.py` | PyTorch 策略价值网络 | 函数近似器、policy head、value head |
| `train.py` | 自我对弈、数据增强、训练、评估、保存模型 | 训练闭环、replay buffer、评估 |
| `mcts_pure.py` | 不使用神经网络的纯 MCTS | baseline opponent |
| `human_play.py` | 人机对弈入口 | 推理和交互 |

这几个文件正好对应强化学习的基本问题：

```text
环境在哪里？      game.py
策略在哪里？      policy_value_net_pytorch.py + MCTSPlayer
价值在哪里？      value head
数据从哪里来？    self-play
目标函数是什么？  policy loss + value loss
怎么变强？        MCTS policy improvement + network update
```

## 五子棋作为 MDP

先把五子棋写成强化学习语言。

状态 $s_t$ 是当前棋盘：

$$
s_t=\text{board position at move }t.
$$

动作 $a_t$ 是在某个空位落子：

$$
a_t\in\{\text{empty board positions}\}.
$$

环境转移是确定性的：

$$
s_{t+1}=T(s_t,a_t).
$$

奖励通常只在终局给出：

$$
z=
\begin{cases}
+1, & \text{当前样本对应的玩家最后赢棋},\\
-1, & \text{当前样本对应的玩家最后输棋},\\
0, & \text{平局}.
\end{cases}
$$

这和 CartPole 那种每一步都有 reward 的任务不同。棋类任务的 reward 很稀疏：中间每一步并不直接告诉你“这步好不好”，必须走完整盘棋才知道胜负。

因此 AlphaZero 的困难是：

- 只靠终局胜负训练，信号太稀疏；
- 只靠当前网络选动作，早期网络很弱；
- 只靠随机探索，棋盘分支太多；
- 所以需要 MCTS 把“当前网络”临时增强成“搜索后的策略”。

## 棋盘状态表示

`game.py` 中的 `Board.current_state()` 返回一个 shape 为：

$$
4\times \text{width}\times \text{height}
$$

的数组。四个 channel 分别是：

| channel | 含义 |
| --- | --- |
| 0 | 当前玩家的棋子位置 |
| 1 | 对手的棋子位置 |
| 2 | 上一步落子位置 |
| 3 | 当前执棋方信息 |

注意这里的状态是从“当前玩家视角”组织的，而不是固定黑棋/白棋视角。这样做很重要，因为同一个棋盘如果轮到不同玩家行动，价值含义会反过来。

可以把输入理解成一个很小的图像：

```text
state[0]: 我方棋子平面
state[1]: 对方棋子平面
state[2]: 最近一步平面
state[3]: 当前先后手平面
```

所以后面的策略价值网络自然使用 CNN。五子棋棋盘有局部空间结构：横、竖、斜方向的连子模式都可以由卷积捕捉。

## 自我对弈样本

`Game.start_self_play()` 是训练数据的入口。

每一步保存三类信息：

```python
states.append(self.board.current_state())
mcts_probs.append(move_probs)
current_players.append(self.board.current_player)
```

其中：

- `state` 是当前棋盘；
- `mcts_probs` 是 MCTS 在根节点得到的落子分布；
- `current_player` 记录这个 state 是从哪个玩家视角保存的。

一盘棋结束后，代码根据最终赢家生成：

```python
winners_z = np.zeros(len(current_players))
if winner != -1:
    winners_z[np.array(current_players) == winner] = 1.0
    winners_z[np.array(current_players) != winner] = -1.0
```

这一步非常关键。因为每个状态都是“当时要行动的玩家”的视角，所以同一个终局胜负要转成对应玩家的 $z$：

$$
z_t=
\begin{cases}
+1, & \text{第 }t\text{ 步行动方最后赢},\\
-1, & \text{第 }t\text{ 步行动方最后输},\\
0, & \text{平局}.
\end{cases}
$$

最终训练样本是：

$$
(s_t,\pi_t,z_t).
$$

这里的 $\pi_t$ 不是人类标签，也不是网络原始输出，而是 MCTS 搜索后的改进策略。

## 数据增强：利用棋盘对称性

`train.py` 里的 `get_equi_data()` 对自我对弈数据做旋转和翻转。

五子棋规则对棋盘旋转、左右翻转是不变的。因此如果：

$$
(s,\pi,z)
$$

是一个合法训练样本，那么旋转后的：

$$
(R(s),R(\pi),z)
$$

也应该是合法样本。

代码中每个样本会经过四种旋转，再做水平翻转，因此最多扩展出 8 份数据。

这相当于把“问题的对称性”显式注入训练集。它的作用有三点：

- 增大样本量；
- 降低网络记忆具体坐标的倾向；
- 让模型更快学到“棋形”而不是“位置编号”。

这和图像任务中的随机翻转、旋转增强是同一个思想。

## 策略价值网络

`policy_value_net_pytorch.py` 中的 `Net` 是一个双头网络：

```text
输入棋盘 state
  -> 共享卷积 trunk
  -> policy head: 输出每个落子位置的 log probability
  -> value head: 输出当前局面对当前玩家的胜率倾向
```

共享部分是三层卷积：

```python
self.conv1 = nn.Conv2d(4, 32, kernel_size=3, padding=1)
self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
```

policy head 输出棋盘上每个位置的概率：

$$
p_\theta(a\mid s),
\qquad
a=1,\ldots,\text{width}\times\text{height}.
$$

value head 输出一个标量：

$$
v_\theta(s)\in[-1,1].
$$

其中：

- $v_\theta(s)\approx 1$：当前玩家大概率赢；
- $v_\theta(s)\approx -1$：当前玩家大概率输；
- $v_\theta(s)\approx 0$：局面接近均势或平局。

这就是 AlphaZero 的核心函数近似器：

$$
f_\theta(s)=\left(p_\theta(\cdot\mid s),v_\theta(s)\right).
$$

一个网络同时输出 policy 和 value，是因为 MCTS 同时需要这两种信息：

- policy $p$：告诉搜索优先看哪些动作；
- value $v$：告诉搜索叶子局面大概好不好。

## 损失函数

训练时，网络要拟合自我对弈生成的目标：

$$
(s,\pi,z).
$$

其中：

- $\pi$ 是 MCTS visit count 归一化后的策略；
- $z$ 是终局胜负；
- 网络输出 $p_\theta$ 和 $v_\theta$。

AlphaZero 常用损失可以写成：

$$
\mathcal L(\theta)
=
(z-v_\theta(s))^2
-
\sum_a \pi(a\mid s)\log p_\theta(a\mid s)
+c\|\theta\|_2^2.
$$

三项分别对应：

| 项 | 作用 |
| --- | --- |
| $(z-v)^2$ | 价值头拟合最终胜负 |
| $-\sum_a \pi_a\log p_a$ | 策略头模仿 MCTS 改进策略 |
| $c\|\theta\|_2^2$ | L2 正则，抑制过拟合 |

项目的 PyTorch 版本中对应代码是：

```python
value_loss = F.mse_loss(value.view(-1), winner_batch)
policy_loss = -torch.mean(torch.sum(mcts_probs * log_act_probs, 1))
loss = value_loss + policy_loss
```

这看起来像监督学习，因为目标 $\pi,z$ 已经在 replay buffer 里。但这些标签不是外部数据集给的，而是通过当前网络自我对弈加 MCTS 生成的。

所以它兼具两种特征：

```text
数据来源：强化学习，自我对弈，环境胜负
参数更新：监督学习，拟合 pi 和 z
```

这也是 AlphaZero 很适合作为强化学习实践案例的原因。

## MCTS 的数据结构

`mcts_alphaZero.py` 中每个 `TreeNode` 保存四个核心量：

| 变量 | 含义 |
| --- | --- |
| `_P` | 网络给出的先验概率 |
| `_Q` | 当前节点的平均价值估计 |
| `_n_visits` | 访问次数 |
| `_u` | 探索奖励 |

MCTS 选择子节点时最大化：

$$
Q(s,a)+U(s,a).
$$

项目中 $U$ 的形式是：

$$
U(s,a)
=
c_{\text{puct}}
P(s,a)
\frac{\sqrt{N(s)}}{1+N(s,a)}.
$$

更准确地说，代码实现为：

```python
self._u = (
    c_puct * self._P *
    np.sqrt(self._parent._n_visits) / (1 + self._n_visits)
)
return self._Q + self._u
```

这里的直觉是：

- $Q(s,a)$ 高：说明这个动作历史搜索结果好；
- $P(s,a)$ 高：说明网络认为这个动作有希望；
- $N(s,a)$ 小：说明这个动作还没有充分探索；
- $c_{\text{puct}}$ 控制相信先验和探索的强度。

这和普通 $\epsilon$-greedy 的思想类似，都是在“利用已知好动作”和“探索不确定动作”之间折中。区别是 MCTS 的探索不是随机乱试，而是在树结构里有方向地展开。

## 一次 MCTS playout 做了什么

`MCTS._playout()` 可以拆成四步：

```text
Selection
  从根节点开始，反复选择 Q + U 最大的子节点

Expansion
  到达叶子节点后，用神经网络给出的 action probabilities 扩展子节点

Evaluation
  用神经网络 value head 估计叶子局面对当前玩家的价值

Backup
  把 leaf value 沿路径反向更新回根节点
```

对应代码逻辑是：

```python
node = self._root
while True:
    if node.is_leaf():
        break
    action, node = node.select(self._c_puct)
    state.do_move(action)

action_probs, leaf_value = self._policy(state)

if not end:
    node.expand(action_probs)
else:
    leaf_value = terminal_result

node.update_recursive(-leaf_value)
```

这里有一个容易出错的地方：为什么 backup 时会出现负号？

五子棋是二人零和博弈。当前玩家觉得好，对手就觉得坏。沿着搜索路径往上一层，行动方会交替变化，因此 value 的符号要交替翻转。

如果叶子节点从当前玩家视角看是：

$$
v=+1,
$$

那么上一层对手视角就是：

$$
-v=-1.
$$

所以代码中 `update_recursive(-leaf_value)` 和递归里的 `-leaf_value` 都是在处理视角切换。

## 从访问次数得到训练策略

每一步真正落子前，MCTS 会运行多次 playout。项目默认小棋盘训练中：

```python
self.n_playout = 400
```

搜索结束后，根节点每个动作都有访问次数：

$$
N(s,a).
$$

然后用温度参数转成动作分布：

$$
\pi(a\mid s)
\propto
N(s,a)^{1/\tau}.
$$

项目中通过：

```python
act_probs = softmax(1.0 / temp * np.log(np.array(visits) + 1e-10))
```

实现等价形式。

温度 $\tau$ 的作用：

| 温度 | 效果 |
| --- | --- |
| 较大 | 分布更平，探索更多 |
| 较小 | 分布更尖，更接近选择访问次数最多的动作 |
| 接近 0 | 近似 argmax |

训练数据里的 $\pi$ 不是网络直接输出，而是搜索后的 visit-count policy。它通常比原始网络策略更强，因此可以作为网络下一轮学习的目标。

## 自我对弈中的 Dirichlet 噪声

自我对弈时，如果每次都选择 MCTS 认为最好的动作，数据会很快变窄，模型容易只在已有经验附近循环。

因此项目在 self-play 模式下加入 Dirichlet 噪声：

```python
move = np.random.choice(
    acts,
    p=0.75 * probs
      + 0.25 * np.random.dirichlet(0.3 * np.ones(len(probs)))
)
```

这一步只用于自我对弈训练。它的含义是：

$$
\pi_{\text{sample}}
=
0.75\pi_{\text{MCTS}}
+0.25\eta,
\qquad
\eta\sim\operatorname{Dirichlet}(\alpha).
$$

这样可以强迫模型探索一些 MCTS 当前不太确定的动作。没有这类探索，self-play 很容易早早收敛到狭窄策略。

## 根节点复用

`MCTS.update_with_move()` 会把搜索树根节点移动到真实落子后的子节点：

```python
if last_move in self._root._children:
    self._root = self._root._children[last_move]
    self._root._parent = None
else:
    self._root = TreeNode(None, 1.0)
```

这叫 tree reuse。因为真实落子以后，原来搜索树中对应子树仍然有用，没有必要全部丢掉。

在自我对弈中：

- 每走一步后复用子树；
- 一盘棋结束后重置 MCTS root。

在普通对弈或评估中：

- 代码默认每步后重置 root；
- 这样避免对手动作和内部树状态不一致。

## 训练流水线

`TrainPipeline.run()` 是完整训练循环：

```text
for batch in game_batch_num:
    collect_selfplay_data()
    if replay_buffer 足够大:
        policy_update()
    每隔 check_freq:
        policy_evaluate()
        save_model()
```

核心参数包括：

| 参数 | 默认值 | 含义 |
| --- | ---: | --- |
| `board_width` / `board_height` | 6 / 6 | 棋盘大小 |
| `n_in_row` | 4 | 连成几个算赢 |
| `n_playout` | 400 | 每步 MCTS 模拟次数 |
| `c_puct` | 5 | PUCT 探索强度 |
| `buffer_size` | 10000 | replay buffer 大小 |
| `batch_size` | 512 | 每次训练 mini-batch |
| `epochs` | 5 | 每轮 policy update 重复训练次数 |
| `kl_targ` | 0.02 | 控制更新幅度的 KL 目标 |

小棋盘设置是为了让普通电脑能跑得动。如果直接上标准 $15\times15$ 五子棋，动作空间和搜索成本都会明显变大。

## 为什么训练时监控 KL

`policy_update()` 中先记录旧网络输出：

```python
old_probs, old_v = self.policy_value_net.policy_value(state_batch)
```

训练若干步后计算：

$$
D_{\text{KL}}(p_{\text{old}}\Vert p_{\text{new}})
=
\sum_a p_{\text{old}}(a)
\log\frac{p_{\text{old}}(a)}{p_{\text{new}}(a)}.
$$

如果 KL 太大，就提前停止当前 batch 的训练，并降低学习率倍率：

```python
if kl > self.kl_targ * 4:
    break

if kl > self.kl_targ * 2:
    self.lr_multiplier /= 1.5
elif kl < self.kl_targ / 2:
    self.lr_multiplier *= 1.5
```

这和 PPO 的思想有相似之处：不要让新策略相对旧策略变化太猛。区别是：

- PPO 用 clip 目标或 KL penalty 控制策略梯度更新；
- 这个项目用训练前后策略分布的 KL 来调学习率和 early stopping。

两者都在解决同一个工程问题：

> 策略一旦更新太激进，后续采样分布会突变，训练容易不稳定。

## 评估：和纯 MCTS 对弈

项目用 `policy_evaluate()` 定期评估当前网络：

```python
current_mcts_player = MCTSPlayer(policy_value_fn, n_playout=self.n_playout)
pure_mcts_player = MCTS_Pure(n_playout=self.pure_mcts_playout_num)
```

评估方式是让当前 AlphaZero player 和纯 MCTS player 对弈。

这里要注意：这不是训练目标本身，只是一个监控指标。训练目标仍然是拟合 self-play 中产生的 $(s,\pi,z)$。评估的作用是判断当前模型是否真的变强，并在表现变好时保存 best policy。

## 和普通策略梯度的区别

普通 policy gradient 更接近：

$$
\nabla_\theta J(\theta)
\approx
\sum_t
\nabla_\theta\log\pi_\theta(a_t\mid s_t)
G_t.
$$

它直接提高高回报轨迹中动作的概率。

AlphaZero 五子棋这套代码则是：

```text
当前网络 -> MCTS 搜索 -> 改进策略 pi
终局胜负 -> value target z
用 supervised loss 拟合 pi 和 z
```

它没有直接对：

$$
\log\pi_\theta(a_t\mid s_t)G_t
$$

做梯度上升，而是把搜索后的策略当成训练标签。

可以把它理解成一种 policy iteration：

```text
Policy evaluation:
  用自我对弈终局 z 训练 value head

Policy improvement:
  用 MCTS 把 p_theta 改进成 pi_MCTS

Policy distillation:
  让 p_theta 拟合 pi_MCTS
```

这比纯策略梯度多了一个搜索改进步骤。对棋类这种可模拟、规则明确、离散动作的任务，搜索能显著提高数据质量。

## 和 PPO / RLHF 的对照

这套五子棋代码和 PPO、RLHF 都属于强化学习，但训练信号来源不同：

| 方法 | 样本来源 | 训练信号 | 更新方式 |
| --- | --- | --- | --- |
| Policy Gradient | 策略采样轨迹 | 回报 $G_t$ 或 advantage | 直接优化策略目标 |
| PPO | 策略采样轨迹 | advantage + ratio clipping | 限制策略更新幅度 |
| AlphaZero | 自我对弈 + MCTS | MCTS 策略 $\pi$ 和胜负 $z$ | 监督拟合策略和值 |
| RLHF | 模型回答 + 人类/奖励模型反馈 | reward / preference | PPO 或其他后训练算法 |

所以不要把“强化学习”狭义理解成“必须用 PPO”。强化学习的本质是：

> 数据来自智能体和环境交互，目标由长期结果定义。

AlphaZero 用监督损失更新网络，但数据和标签来自自我对弈搜索，因此仍然是强化学习。

## 和神经网络训练闭环的关系

如果从本站的总图来看，AlphaZero 五子棋正好连接了几个章节：

```text
PyTorch Module
  -> CNN policy-value network

强化学习 MDP
  -> board state, legal action, terminal reward

Monte Carlo / search
  -> many MCTS playouts estimate action quality

交叉熵和 MSE
  -> policy head imitates pi, value head fits z

KL
  -> monitor policy update size
```

它也和 VMC / NNQS 有一个结构类比：

| 领域 | 当前模型产生什么 | 用什么改进信号 | 再训练什么 |
| --- | --- | --- | --- |
| AlphaZero | 自我对弈棋局 | MCTS 策略和终局胜负 | 策略价值网络 |
| VMC / NNQS | 构型样本 | 局域能和能量梯度 | 波函数参数 |
| 语言模型 | token 分布 | next-token loss 或偏好奖励 | decoder 参数 |

共同点是：训练数据不是永远固定的。模型变了，采样分布也会变，下一轮训练看到的经验也会变。

## 实践阅读顺序

读这套代码时建议按下面顺序：

1. 先读 `game.py` 的 `Board`，确认状态、动作、终局判断。
2. 再读 `Game.start_self_play()`，看训练样本 $(s,\pi,z)$ 如何产生。
3. 读 `policy_value_net_pytorch.py`，看网络如何输出 action probabilities 和 value。
4. 读 `mcts_alphaZero.py` 的 `TreeNode` 和 `_playout()`，理解 PUCT、expand、backup。
5. 最后读 `train.py`，把 self-play、augmentation、buffer、policy update、evaluation 串起来。

不要一开始就陷入每个 Python 语法细节。先抓住数据流：

```text
board.current_state()
  -> policy_value_fn()
  -> MCTS.get_move_probs()
  -> start_self_play()
  -> data_buffer
  -> train_step()
```

只要这条线通了，这个项目的主体就通了。

## 可以动手改的实验

如果想把它当成强化学习实验课，可以从这些小改动开始：

### 改 MCTS playout 次数

把：

```python
self.n_playout = 400
```

改成 100、400、800，对比：

- 每盘棋耗时；
- 训练数据质量；
- 对纯 MCTS 的胜率；
- policy entropy 变化。

预期现象是：playout 越多，单步搜索越强，但生成数据越慢。

### 改探索噪声

把：

```python
0.75 * probs + 0.25 * dirichlet_noise
```

中的 0.25 改小或改大，观察自我对弈是否更单一或更混乱。

噪声太小，探索不足；噪声太大，MCTS 的改进策略被破坏。

### 改棋盘大小

从 $6\times6$、四子连珠开始，再尝试 $8\times8$、五子连珠。观察训练时间和胜率提升速度。

这能直观看到动作空间大小对 MCTS 和神经网络训练的影响。

### 替换网络结构

可以把三层 CNN 改成更深的 residual CNN：

```text
Conv
  -> Residual blocks
  -> policy head
  -> value head
```

这会更接近原始 AlphaZero。重点观察：

- 是否更容易过拟合；
- 是否需要更大 replay buffer；
- 训练是否更慢；
- value loss 是否更稳定。

## 旧版 PyTorch 代码的注意点

这个项目的 PyTorch 文件写于较早版本，里面有一些旧 API：

```python
Variable(...)
loss.data[0]
F.tanh(...)
F.log_softmax(x)
```

如果迁移到现代 PyTorch，通常要改成：

```python
state_batch = torch.tensor(state_batch, dtype=torch.float32, device=device)
loss.item()
torch.tanh(...)
F.log_softmax(x, dim=1)
```

学习这套代码时，重点应该放在 AlphaZero 的训练结构，而不是照抄旧 API。

## 小结

AlphaZero 五子棋实践可以压缩成一句话：

> 神经网络给 MCTS 提供先验策略和局面价值，MCTS 生成更强的落子分布，自我对弈产生胜负标签，网络再反过来拟合搜索结果和终局结果。

对应到公式：

$$
f_\theta(s)
=
(p_\theta,v_\theta),
$$

$$
\pi_{\text{MCTS}}
=
\operatorname{Search}(s;f_\theta),
$$

$$
\mathcal L(\theta)
=
(z-v_\theta(s))^2
-
\pi_{\text{MCTS}}^\top\log p_\theta(\cdot\mid s).
$$

这页要带走的核心不是“五子棋怎么写”，而是强化学习实践里最重要的一种闭环：

```text
模型参与产生数据
  -> 数据反过来训练模型
  -> 新模型改变下一轮数据分布
```

这和监督学习固定数据集的训练很不一样，也是强化学习、VMC、LLM 后训练共同容易不稳定但也非常强大的地方。

