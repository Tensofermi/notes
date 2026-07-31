# Monte Carlo 核心原理

Monte Carlo 方法的核心，是用随机抽样来估计积分、求和或期望值：

$$
\langle O\rangle=\sum_s O(s)\pi(s)
$$

或连续变量形式

$$
\langle O\rangle=\int O(x)\pi(x)\,dx.
$$

这一思想本身并不要求样本一定来自 Markov chain。若能直接从目标分布 $\pi$ 产生样本，就可以直接用样本平均估计观测量；若不能直接采样，就需要进一步构造重要性采样或 Markov chain Monte Carlo 方法。统计物理中最常见的情形属于后者，因为构型空间巨大、归一化常数未知，而且通常只能计算构型之间的相对权重。

## 直接采样、重要性采样和 MCMC

Monte Carlo 的第一层思想是直接采样。若能直接产生

$$
s_1,s_2,\cdots,s_N\sim \pi(s),
$$

那么样本平均

$$
\langle O\rangle\simeq \frac1N\sum_{i=1}^NO(s_i)
$$

就是最自然的估计。某些问题确实接近这种情形。例如普通 percolation 中，每条边按概率 $p$ 独立开闭；简单随机行走中，每一步按给定分布独立选方向。这类构型可以每次从头生成，样本之间大致独立。

统计物理中的难点在于，目标分布通常是

$$
\pi(s)=\frac{W(s)}{Z},
\qquad
Z=\sum_s W(s),
$$

其中 $Z$ 很难计算，构型空间也无法枚举。重要性采样的想法是：不要在所有构型上平均分配计算资源，而是让样本更多地出现在权重大的区域。这样估计

$$
\langle O\rangle
=
\sum_sO(s)\pi(s)
$$

时，大部分样本都真正贡献到物理平均。

MCMC 是统计物理里最常用的重要性采样实现方式。它不要求直接生成独立的 $\pi(s)$ 样本，而是构造一条 Markov chain：

$$
s_0\to s_1\to s_2\to\cdots
$$

只要这条链以 $\pi(s)$ 为平稳分布，热化后得到的构型就可以用于估计物理量。对于 $O(n)$ 自旋模型、格点场论、量子路径积分这类复杂分布，Metropolis 更新通常只需要局域权重比，因此可以作为最基本的 MCMC 构造。之后还可以根据模型结构，引入 cluster、worm、loop、辅助场或张量网络等变量变换来提高效率。

Markov chain 产生的是关联样本。相邻构型来自同一条随机轨道，因此

$$
s_i,\ s_{i+1},\ s_{i+2}
$$

之间通常不能当作独立样本。于是需要热化时间、自关联时间、有效样本数等概念。很多非局域算法的发展动机，正是减少这种相关性，让同样计算时间产生更多有效独立样本。

还有一些介于直接采样和 MCMC 之间的做法。例如 Tensor Network Monte Carlo 会先用张量网络近似边缘分布，以自回归方式生成近似独立的自旋构型，再用 MCMC 步骤修正张量网络近似带来的偏差。这样的思想对无序体系和自旋玻璃很有价值，相关例子见 [arXiv:2409.06538](https://arxiv.org/abs/2409.06538)。

一旦决定用 MCMC，问题就从“如何随机抽样”变成“如何构造一个以目标分布为平衡分布的随机过程”。这时才需要引入转移概率、平稳分布、遍历性和 detailed balance 这些条件。

## 合法的随机过程

对固定出发点 $s$，下一步一定会跳到某个构型 $s'$，包括可能留在原地。因此所有去向的概率必须加起来等于 $1$：

$$
\sum_{s'}P(s\to s')=1.
$$

在 Ising 模型中，一个构型可以写为

$$
s=\{s_1,s_2,\cdots,s_N\},\qquad s_i=\pm 1.
$$

一次单 spin flip 更新会尝试翻转某个 $s_i$。如果新构型被接受，就从 $s$ 跳到 $s'$；如果被拒绝，就留在原地。也就是说，$P(s\to s)$ 对应拒绝更新后留在原构型的概率。没有这项，转移概率通常无法归一化。

## 平稳分布

假设第 $t$ 步系统处于构型 $s$ 的概率是 $W_t(s)$。经过一次更新后，第 $t+1$ 步处于 $s$ 的概率为

$$
W_{t+1}(s)=\sum_{s'}W_t(s')P(s'\to s).
$$

这句话的意思是：下一步到达 $s$，可以从任意旧构型 $s'$ 跳过来。于是要把“原来在 $s'$ 的概率”和“从 $s'$ 跳到 $s$ 的概率”相乘，再对所有 $s'$ 求和。

如果目标权重 $W(s)$ 满足

$$
W(s)=\sum_{s'}W(s')P(s'\to s),
$$

那么一旦系统分布达到 $W(s)$，经过一次更新后仍然是 $W(s)$。这就是平稳分布条件，也常叫 global balance。

严格来说，采样分布应该是

$$
\pi(s)=\frac{W(s)}{Z},
\qquad
Z=\sum_s W(s).
$$

但把它代入平稳条件：

$$
\frac{W(s)}{Z}
=
\sum_{s'}\frac{W(s')}{Z}P(s'\to s).
$$

两边乘以 $Z$，就回到

$$
W(s)=\sum_{s'}W(s')P(s'\to s).
$$

因此 Monte Carlo 不需要知道归一化常数 $Z$。这正是它能够处理配分函数、后验分布和复杂能量模型的关键。

## 转移矩阵语言

如果构型空间是有限的，可以把所有构型排成一个列表：

$$
s_1,s_2,\cdots,s_{\Omega}.
$$

一次 Monte Carlo 更新就对应一个矩阵：

$$
\mathbf P_{ij}=P(s_j\to s_i).
$$

这里采用列向量约定：$\mathbf P_{ij}$ 表示从第 $j$ 个构型出发，下一步到达第 $i$ 个构型的概率。由于从任意构型出发，下一步一定会到达某个构型，矩阵每一列都满足

$$
\sum_i \mathbf P_{ij}=1.
$$

这样的矩阵称为 stochastic matrix。若把第 $n$ 步的概率分布写成列向量

$$
\boldsymbol p_n
=
\begin{pmatrix}
p_n(s_1)\\
p_n(s_2)\\
\vdots\\
p_n(s_\Omega)
\end{pmatrix},
$$

那么一步更新就是

$$
\boldsymbol p_{n+1}
=
\mathbf P\boldsymbol p_n.
$$

经过 $n$ 步：

$$
\boldsymbol p_n
=
\mathbf P^n\boldsymbol p_0.
$$

平稳分布则是转移矩阵的右本征向量：

$$
\mathbf P\boldsymbol\pi=\boldsymbol\pi.
$$

也就是说，$\boldsymbol\pi$ 对应本征值

$$
\lambda_0=1.
$$

这就是前面 global balance 的矩阵形式。

## Perron-Frobenius 定理的作用

Perron-Frobenius 定理告诉我们：对于满足适当连通性和非周期性的非负矩阵，最大的本征值是正的，并且对应一个非负本征向量。对 Markov chain 的转移矩阵来说，这个最大本征值就是

$$
\lambda_0=1.
$$

在 Monte Carlo 中，我们希望的不只是“存在一个平稳分布”，还希望从任意初始构型出发，长时间后都会收敛到同一个目标分布。这通常需要两个条件。

第一，链要 **irreducible**，也就是构型空间中任意两个重要构型之间都能通过若干次更新互相到达。物理上这叫 ergodicity。若某个更新只能在一个拓扑扇区里移动，就只能采样该扇区内的平衡分布。

第二，链要 **aperiodic**，也就是不会被迫以固定周期来回跳。实际 Metropolis 算法中，因为拒绝更新会产生

$$
P(s\to s)>0,
$$

这通常会打破周期性。

在这些条件下，Perron-Frobenius 定理保证：

1. 最大本征值 $\lambda_0=1$ 是唯一的。
2. 对应的平稳分布可以取为正分布。
3. 其他本征值满足

$$
|\lambda_\alpha|<1,\qquad \alpha\ge 1.
$$

于是任意初始分布都可以分解成

$$
\boldsymbol p_0
=
\boldsymbol\pi
+\sum_{\alpha\ge1}c_\alpha\boldsymbol v_\alpha,
$$

经过 $n$ 步后变成

$$
\boldsymbol p_n
=
\boldsymbol\pi
+\sum_{\alpha\ge1}c_\alpha\lambda_\alpha^n\boldsymbol v_\alpha.
$$

因为 $|\lambda_\alpha|<1$，非平衡成分会随步数衰减，最后只剩下平稳分布 $\boldsymbol\pi$。这就是“热化”在矩阵语言中的含义。

## 第二本征值与混合时间

收敛快慢由最慢衰减的非平稳模式决定。若按绝对值排序：

$$
1=\lambda_0>|\lambda_1|\ge |\lambda_2|\ge\cdots,
$$

那么长时间行为通常由 $\lambda_1$ 控制：

$$
\boldsymbol p_n-\boldsymbol\pi
\sim
\lambda_1^n.
$$

若 $\lambda_1$ 接近 $1$，衰减很慢，链需要很长时间才能忘记初始构型。定义谱隙

$$
\Delta=1-|\lambda_1|.
$$

谱隙越大，热化越快；谱隙越小，热化越慢。

当 $|\lambda_1|$ 接近 $1$ 时，可以写成

$$
|\lambda_1|^n
=
\exp(n\ln|\lambda_1|)
\simeq
\exp[-n(1-|\lambda_1|)].
$$

因此最慢模式的指数衰减时间大约是

$$
\tau_{\rm exp}
=
-\frac{1}{\ln|\lambda_1|}
\simeq
\frac{1}{1-|\lambda_1|}
=
\frac{1}{\Delta}.
$$

这里 $\tau_{\rm exp}$ 称为 exponential autocorrelation time 或 relaxation time。它控制热化尾部：若想让初始条件的影响衰减到很小，热化步数通常要取为若干倍 $\tau_{\rm exp}$。

## Detailed Balance

直接构造满足 global balance 的 $P(s\to s')$ 通常很难。实际中常用更强但更容易检查的条件：

$$
W(s)P(s\to s')=W(s')P(s'\to s).
$$

这叫 detailed balance。它的含义是：在平衡状态下，从 $s$ 流向 $s'$ 的概率流，等于从 $s'$ 流向 $s$ 的概率流。

如果 detailed balance 对任意 $s,s'$ 成立，那么对 $s'$ 求和：

$$
\sum_{s'}W(s)P(s\to s')
=
\sum_{s'}W(s')P(s'\to s).
$$

利用概率归一化

$$
\sum_{s'}P(s\to s')=1,
$$

左边变成 $W(s)$，于是自动得到

$$
W(s)=\sum_{s'}W(s')P(s'\to s).
$$

所以 detailed balance 是构造正确 Monte Carlo 更新的常用充分条件。

### Detailed Balance 与对称化

若把 detailed balance 写成归一化分布的形式：

$$
\pi_j\mathbf P_{ij}
=
\pi_i\mathbf P_{ji},
$$

则转移矩阵在带权内积下是自伴的。更直观地，可以做相似变换：

$$
\widetilde{\mathbf P}_{ij}
=
\pi_i^{-1/2}\mathbf P_{ij}\pi_j^{1/2}.
$$

detailed balance 保证

$$
\widetilde{\mathbf P}_{ij}
=
\widetilde{\mathbf P}_{ji}.
$$

所以 $\widetilde{\mathbf P}$ 是实对称矩阵，本征值为实数。这使得“模式衰减”的图像非常清楚：每个本征模式按自己的 $\lambda_\alpha^n$ 衰减。没有 detailed balance 的算法也可以正确，只要满足 global balance；但谱分析会更复杂，可能出现复本征值。

## Proposal 与 Acceptance

实际算法通常把一次转移拆成两步：

$$
P(s\to s')=A(s\to s')P_{\rm acc}(s\to s').
$$

其中 $A(s\to s')$ 是 proposal probability，即“尝试从 $s$ 走到 $s'$”的概率；$P_{\rm acc}(s\to s')$ 是接受率。

detailed balance 要求

$$
W(s)A(s\to s')P_{\rm acc}(s\to s')
=
W(s')A(s'\to s)P_{\rm acc}(s'\to s).
$$

一种标准选择是 Metropolis-Hastings 接受率：

$$
P_{\rm acc}(s\to s')
=
\min\left[
1,
\frac{W(s')A(s'\to s)}{W(s)A(s\to s')}
\right].
$$

如果 proposal 对称，

$$
A(s\to s')=A(s'\to s),
$$

则接受率简化为

$$
P_{\rm acc}(s\to s')
=
\min\left[
1,
\frac{W(s')}{W(s)}
\right].
$$

这就是最常见的 Metropolis 公式。

## Ising 单 Spin Flip

考虑经典 Ising 模型的 reduced Hamiltonian：

$$
\mathcal H(s)=-K\sum_{\langle ij\rangle}s_is_j.
$$

构型权重为

$$
W(s)=e^{-\mathcal H(s)}
=
\exp\left(K\sum_{\langle ij\rangle}s_is_j\right).
$$

如果只翻转一个 spin

$$
s_i\to -s_i,
$$

只有它和最近邻之间的局域能量会改变。翻转前局域能量为

$$
\mathcal H_{\rm old}
=
-Ks_i\sum_{j\in\partial i}s_j,
$$

翻转后为

$$
\mathcal H_{\rm new}
=
Ks_i\sum_{j\in\partial i}s_j.
$$

因此能量差是

$$
\Delta
=
\mathcal H_{\rm new}-\mathcal H_{\rm old}
=
2K s_i\sum_{j\in\partial i}s_j.
$$

权重比为

$$
\frac{W(s')}{W(s)}
=
e^{-\Delta}.
$$

若单 spin proposal 是对称的，Metropolis 接受率就是

$$
P_{\rm acc}
=
\min(1,e^{-\Delta})
=
\min\left(1,e^{-2K s_i\sum_{j\in\partial i}s_j}\right).
$$

这条公式背后的完整逻辑是：

1. 概率归一化保证 $P(s\to s')$ 是合法转移概率。
2. 平稳分布条件保证采样目标是 $W(s)$。
3. detailed balance 给出构造转移概率的实用方法。
4. proposal 与 acceptance 分解让算法可以只用权重比。
5. 对 Ising 单点更新，权重比只依赖局域能量差。

## 从谱隙看算法效率

不同 Monte Carlo 更新的目标分布可以完全一样，但转移矩阵 $\mathbf P$ 不同，因此本征谱不同。一个高效算法的意义并不只是“每一步便宜”，还包括让第二大本征值远离 $1$，也就是让谱隙更大。

局域 Metropolis 更新在临界点附近常出现临界慢化。直观上，相关长度很大，而局域更新每次只改动很小区域，大尺度模式变化很慢。谱语言中，这意味着

$$
|\lambda_1|\to 1,
\qquad
\Delta\to0.
$$

自关联时间随系统尺寸增长，常写为

$$
\tau\sim L^z,
$$

这里的 $z$ 称为动态临界指数。它描述的是 **Monte Carlo 更新规则所定义的 Markov chain 动力学**，因此不是静态临界指数。静态指数 $\nu,\beta,\gamma,\eta$ 由模型的平衡普适类决定；$z$ 还依赖你选择的算法。例如同一个 Ising 模型，用单 spin Metropolis、Wolff cluster 或 Swendsen-Wang 更新，会有相同的平衡分布，却可能有很不同的 $z$。

更一般地，临界慢化常写成

$$
\tau\sim \xi^z.
$$

在临界点的有限系统中，相关长度被系统尺寸截断：

$$
\xi\sim L,
$$

于是得到

$$
\tau(L,T_c)\sim L^z.
$$

从转移矩阵角度，若用最慢本征模式定义时间尺度，

$$
\tau_{\rm exp}
=
-\frac{1}{\ln|\lambda_1|},
$$

则可以定义

$$
\tau_{\rm exp}(L,T_c)\sim L^{z_{\rm exp}}.
$$

等价地，谱隙满足

$$
\Delta(L)
=
1-|\lambda_1(L)|
\sim L^{-z_{\rm exp}},
$$

这里使用了 $|\lambda_1|\approx1$ 时 $\tau_{\rm exp}\simeq1/\Delta$。这给出动态指数最干净的谱定义。

实际测量时，人们常用某个观测量 $O$ 的积分自关联时间：

$$
\tau_{\rm int}(O;L,T_c)\sim L^{z_{\rm int}(O)}.
$$

这个指数可能依赖观测量，因为不同观测量和最慢模式的重叠不同。通常讨论算法效率时，会报告能量、磁化、cluster size 或目标物理量对应的 $\tau_{\rm int}$。cluster、loop、worm 等非局域更新的目的，就是更有效地改变大尺度自由度，增大谱隙，降低这些自关联时间。

## 算法实现的抽象结构

Monte Carlo 算法的实现通常需要把几类职责分开：

- **构型**：保存当前状态，以及局域能量、邻接关系、粒子数、世界线片段等辅助信息。
- **更新器**：给出 proposal，计算权重比或能量差，并按接受率更新构型。
- **观测量**：测量能量、磁化率、关联函数、绕数、Binder ratio 等。
- **随机数产生器**：提供均匀随机数、离散抽样、高斯抽样等。
- **数据输出与分析**：记录参数、热化步数、采样数、误差、关联时间和随机种子。

关键约束是让“构型如何存储”“更新如何改变构型”“观测量如何从构型读出”三件事保持清晰对应。这样可以降低更新错误、测量错误和数据分析错误相互掩盖的风险。
