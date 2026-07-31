# Scaling Law：模型、数据与算力的幂律规律

这一页讨论大模型训练里经常出现的 **scaling law**。它不是某种神秘定律，而是一类经验规律：

> 当模型参数量、训练数据量或训练算力按数量级增大时，验证 loss 往往按近似幂律下降。

这件事重要，是因为它把“模型变大有没有用”从口号变成了可以拟合、外推和规划的问题。

## 最基本的形式

语言模型通常用 cross-entropy loss 衡量预测下一个 token 的平均代价。一个常见写法是：

$$
L(N,D)
=
E
+
{A\over N^\alpha}
+
{B\over D^\beta}.
$$

其中：

| 符号 | 含义 |
| --- | --- |
| $N$ | 模型参数量 |
| $D$ | 训练 token 数 |
| $E$ | 不可约 loss，可以粗略看成数据分布本身的熵下限 |
| $\alpha,\beta$ | scaling exponent，描述 loss 随规模下降的速度 |
| $A,B$ | 和数据、架构、训练设置有关的拟合常数 |

如果只看一个变量，也可以写成：

$$
L(x)-L_\infty
\sim
A x^{-\gamma}.
$$

这里 $x$ 可以是参数量 $N$、数据量 $D$ 或训练 compute $C$。$\gamma$ 就是 scaling exponent。

## exponent 到底说明什么？

如果：

$$
\gamma>0,
$$

说明扩大规模确实还能降低 reducible loss。

如果：

$$
\gamma\approx 0,
$$

说明继续扩大这个变量带来的收益已经很小，可能被另一个瓶颈限制住了。

但要注意：

> 一个正的 scaling exponent 只能说明模型处在 scalable learning regime，不能直接证明“智能出现了”。

“智能”是功能性概念，还要看泛化、组合推理、迁移、工具使用、长期规划、鲁棒性等能力。Scaling law 给的是 loss 层面的增长趋势，不是智能的充分条件。

## Kaplan scaling law 的核心直觉

Kaplan et al. 2020 研究语言模型的 cross-entropy loss 随模型大小、数据大小和训练 compute 的变化，发现很多范围内都接近幂律。

直观上：

```text
模型越大 -> 表达能力越强
数据越多 -> 过拟合越少，分布覆盖越好
算力越多 -> 可以训练更大的模型或看更多数据
```

但这三个变量不是互相独立地“越多越好”。如果模型很大但数据太少，会浪费参数；如果数据很多但模型太小，会被模型容量卡住；如果算力有限，就必须决定算力该花在参数上还是 token 上。

这就是 compute-optimal scaling 要解决的问题。

## 固定 compute 下怎么分配模型和数据？

Chinchilla 式 scaling law 常写成：

$$
L(N,D)-E
=
A N^{-\alpha}
+
B D^{-\beta}.
$$

对 dense Transformer，训练计算量可以粗略近似为：

$$
C=\kappa ND.
$$

这里 $\kappa$ 吸收了架构常数、前向反向比例、序列长度处理等细节。固定 compute $C$ 时，令：

$$
P={C\over \kappa},
$$

则约束是：

$$
ND=P.
$$

所以：

$$
D={P\over N}.
$$

代入 loss：

$$
L-E
=
A N^{-\alpha}
+
B\left({P\over N}\right)^{-\beta}.
$$

因为：

$$
\left({P\over N}\right)^{-\beta}
=
P^{-\beta}N^\beta,
$$

所以：

$$
L-E
=
A N^{-\alpha}
+
B P^{-\beta}N^\beta.
$$

对 $N$ 求导：

$$
{d\over dN}
\left(
A N^{-\alpha}
+
B P^{-\beta}N^\beta
\right)
=
0.
$$

得到：

$$
-\alpha A N^{-\alpha-1}
+
\beta B P^{-\beta}N^{\beta-1}
=
0.
$$

移项：

$$
\alpha A N^{-\alpha-1}
=
\beta B P^{-\beta}N^{\beta-1}.
$$

两边乘以 $N^{\alpha+1}$：

$$
\alpha A
=
\beta B P^{-\beta}N^{\alpha+\beta}.
$$

因此：

$$
N_*^{\alpha+\beta}
=
{\alpha A\over \beta B}P^\beta.
$$

也就是：

$$
N_*
=
\left(
{\alpha A\over \beta B}
\right)^{1\over \alpha+\beta}
P^{\beta\over \alpha+\beta}.
$$

忽略常数并把 $P=C/\kappa$ 代回去：

$$
\boxed{
N_*(C)\sim C^{\beta\over \alpha+\beta}
}
$$

再由 $D_*=P/N_*$，得到：

$$
\boxed{
D_*(C)\sim C^{\alpha\over \alpha+\beta}
}
$$

最优 loss 的下降指数是：

$$
\boxed{
L_*(C)-E
\sim
C^{-{\alpha\beta\over \alpha+\beta}}
}
$$

所以 compute-optimal scaling 的本质是：

> 在固定算力下，不是盲目把模型做大，而是让模型参数量和训练 token 数按合适比例一起增长。

## 为什么 Chinchilla 说旧模型 undertrained？

Chinchilla 论文的核心结论是：很多早期大语言模型参数量很大，但训练 token 相对不足。也就是说它们并不是算力不足，而是算力分配不够优。

更直观地说：

```text
旧思路：把模型做得非常大，但训练数据增长没跟上。
Chinchilla 视角：同样 compute 下，较小模型 + 更多 token 可能更优。
```

这也是后来很多开源模型强调“tokens per parameter”的原因。

## fixed point 和 RG flow 的类比

从统计物理语言看，scaling law 很容易让人想到 fixed point 或 renormalization group。这个类比有启发性，但要谨慎。

可以分三层理解。

第一，loss-level 极限：

$$
N,D\to\infty
\quad\Rightarrow\quad
L(N,D)\to E.
$$

这里的 $E$ 可以看成性能层面的极限，不是严格物理 fixed point。

第二，compute-optimal trajectory：

$$
C\to bC
$$

时：

$$
N_*(C)\to b^{\beta\over \alpha+\beta}N_*(C),
$$

$$
D_*(C)\to b^{\alpha\over \alpha+\beta}D_*(C).
$$

这更像一条通向低 loss 区域的最优 scaling trajectory。

第三，真正的无限宽理论在 [NTK 与 μP](ntk_mup_infinite_width.md) 中讨论。那一页关心的不是 $N,D,C$ 怎样降低 loss，而是网络宽度 $n\to\infty$ 时训练动力学是否有良好极限。

## 和“压缩即智能”的关系

语言模型训练目标：

$$
-\log p_\theta(x_t\mid x_{<t})
$$

可以从信息论角度理解为“编码真实 token 需要多少信息量”。Loss 下降，意味着模型更好地压缩了文本分布中的规律。

但 scaling law 只告诉我们：

```text
规模扩大 -> loss 下降
```

它不自动告诉我们：

```text
模型是否掌握因果机制
模型是否能可靠规划
模型是否能跨分布泛化
模型是否真正理解
```

所以更稳妥的表述是：

> Scaling law 描述可预测压缩能力随规模增长的经验规律；智能还需要看这种压缩能否迁移、推理和行动。

## 扩展：CFT/bootstrap 语言和 AI for math

Scaling law 很容易让人联想到统计物理和场论里的尺度、临界指数、fixed point、bootstrap 等语言。这个联想有价值，但要分清楚层次。

在 CFT bootstrap 中，人们利用对称性、一致性条件和数值约束去限制理论空间。它关心的是严格数学物理对象，例如 conformal field theory 的谱、OPE 系数和临界指数。

在大模型 scaling law 中，人们拟合的是经验 loss：

$$
L(N,D,C).
$$

这不是同一个问题。更稳妥的说法是：

> 两者都关心“尺度变化下哪些结构稳定”，但大模型 scaling law 不是 CFT bootstrap 的直接应用。

不过，CFT/bootstrap 背景的人进入 AI for math 是一个值得关注的交叉方向。比如 YMSC 苏宁老师的公开主页列出的研究方向包括 bootstrap methods、artificial intelligence、conformal field theory 和 scattering amplitudes；相关 AI for math 工作也已经开始研究 transformer 在符号推理和代数结构发现中的 scaling behavior 与泛化。

本站不把这条线写成主线，因为它更偏高级研究方向。这里保留的核心判断是：

```text
可以借用尺度、约束和 fixed-point-like 语言帮助思考；
但不要把 LLM scaling law 直接说成严格的 RG 或 CFT 定理。
```

## 已核实来源

- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)：Kaplan et al. 2020，研究语言模型 loss 随模型大小、数据大小和训练 compute 的幂律关系。
- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)：Hoffmann et al. 2022，也就是 Chinchilla 论文，研究固定 compute 下模型大小和 token 数如何分配。
- [Neural Scaling Laws in Robotics](https://arxiv.org/abs/2405.14005)：机器人 scaling 相关工作，详细讨论见 [机器人 Scaling Law 与具身智能](../rl/robotics_scaling.md)。
- [Su Ning - Yau Mathematical Sciences Center, Tsinghua University](https://ymsc.tsinghua.edu.cn/en/info/1033/3749.htm)：公开主页列出其研究方向包括 bootstrap methods、artificial intelligence、conformal field theory、scattering amplitudes。
- [Discovering Hidden Algebraic Structures via Transformers with Rank-Aware Beam GRPO](https://arxiv.org/abs/2508.15766)：Jaeha Lee, Gio Huh, Ning Su, Tony Yue Yu 2025，研究 transformer 在多元多项式分解等符号任务中的结构发现、scaling behavior 和 BGRPO。
