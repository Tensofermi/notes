# 几何观测量

只要构型可以表示为节点和连接关系，就可以定义一组几何观测量。它们常出现在 cluster、loop、percolation、random graph 和几何表象的 Monte Carlo 分析中。

几何观测量直观，但它们不是“画图用的附属量”。很多时候，几何量就是某个物理响应的另一种写法。例如 FK cluster 的大小矩和磁化率有关，worldline 的 winding number 和超流刚度有关。因此，每个几何量都需要对应到明确的物理问题。

## Cluster 大小

设一个构型中所有 cluster 的大小为

$$
C_1\ge C_2\ge C_3\ge\cdots.
$$

常用观测量包括：

- $C_1$：最大 cluster 大小。
- $C_2$：次大 cluster 大小。
- $N_c$：cluster 数目。
- $N_b$：激活 bond 数目。

在渗流和临界现象中，$C_1/L^d$ 可作为序参量的几何版本，$C_2$ 常用于观察临界附近的大涨落。

为什么最大 cluster 有时能当作序参量？在无序相中，典型 cluster 尺寸远小于系统体积，因而

$$
\frac{C_1}{L^d}\to0.
$$

在有序或 percolating 相中，会出现一个占据有限体积分数的宏观 cluster，于是

$$
\frac{C_1}{L^d}
$$

趋向非零。次大 cluster $C_2$ 则常在临界附近变大，因为此时系统中同时存在许多跨尺度团簇。若 $C_1$ 很大但 $C_2$ 很小，通常说明系统已经进入明显有序或贯通相；若 $C_1$ 和 $C_2$ 都有强涨落，则往往更接近临界区域。

## Wrapping 与 Winding

如果系统有周期边界，可以进一步定义拓扑观测量：

- wrapping probability $R$：是否存在跨越周期边界的 cluster。
- winding number $\vec W$：loop 或世界线绕周期边界的次数。

这些量通常是无量纲的，因此适合做有限尺寸标度分析。不同尺寸的 wrapping probability 或 winding ratio 曲线常在临界点附近交叉。

计算 wrapping 时，不能只看 cluster 是否碰到盒子两侧。周期边界下，cluster 可能从右边界跨出去又从左边界回来。更稳的做法是在 BFS 或并查集中记录每个站点相对种子点的“展开坐标” $\tilde{\mathbf r}_i$。当搜索一条 bond $i\to j$ 时，若已经访问过 $j$，但新路径给出的展开坐标与旧坐标不同：

$$
\tilde{\mathbf r}_i+\Delta\mathbf r_{ij}
\ne
\tilde{\mathbf r}_j,
$$

两者差值就是一个周期方向的绕行向量。由此可以判断 $x,y,\cdots$ 方向是否发生 wrapping。

worldline 或 loop 构型中的 winding number 更常写为净跨边界次数：

$$
W_\mu=\frac{1}{L_\mu}
\sum_{\ell\in{\rm loop}}\Delta r_{\ell,\mu}.
$$

在量子 Monte Carlo 中，winding number 的涨落常与超流刚度相关；在 classical cluster 表象中，wrapping probability 则常作为无量纲临界量使用。

## 回转半径

对一个 cluster，回转半径描述它的空间延展：

$$
R_g^2
=
\frac{1}{C}\sum_{i\in C}
|\vec r_i-\vec r_{\rm cm}|^2.
$$

其中 $\vec r_{\rm cm}$ 是 cluster 的质心。最大 cluster 和次大 cluster 的回转半径可以记为 $T_1,T_2$，用于区分紧致团簇和延展团簇。

在周期边界下，计算 $R_g$ 时应使用展开坐标或先选择一套连续的 cluster 坐标，否则跨边界 cluster 会被错误地拉长。例如一个实际很紧的团簇若横跨 $x=0$ 边界，直接用盒内坐标会把它误认为延展到整个系统。

对一个已展开的 cluster，可同时记录

$$
\sum_{i\in C}\tilde{\mathbf r}_i,
\qquad
\sum_{i\in C}\tilde{\mathbf r}_i^2,
$$

从而在一次搜索结束后快速得到质心和 $R_g$。

## 分布量

除了均值，也常测量分布：

$$
n(s,L)
$$

表示大小为 $s$ 的 cluster 数密度；

$$
T(s,L)
$$

表示给定大小 cluster 的典型空间延展。

分布量比单个平均值包含更多信息，但也需要更多样本。分析时要注意 binning、归一化和尾部分布误差。

以 cluster 大小分布为例，常见标度形式为

$$
n(s,L)
\sim
s^{-\tau}f(s/L^{d_F}),
$$

其中 $d_F$ 是 cluster 的分形维度。这个式子表达的是：临界点附近没有单一特征大小，直到有限尺寸给出的截止

$$
s_{\max}\sim L^{d_F}.
$$

实际画分布时，小 $s$ 区域容易受格点细节影响，大 $s$ 尾部样本很少，二者都不适合盲目拟合。更稳的做法是结合 $C_1$、$C_2$、wrapping probability 和分布 collapse 一起判断。

## 与物理量的关系

几何观测量通常是物理量的另一种表达，并非额外装饰。例如在 FK 表象中，磁化率可以与 cluster 大小矩联系起来；在世界线 QMC 中，绕数与超流刚度有关。

因此设计几何观测量时，应先问清楚：它对应哪个物理响应，是否具有明确的标度维度，以及误差是否可控。

几个常见对应关系如下：

| 几何量 | 常见物理含义 |
| --- | --- |
| $C_1/L^d$ | percolating cluster 的序参量 |
| $\sum_C C^2/N$ | FK 表象中与磁化率相关的大小矩 |
| wrapping probability | 无量纲临界定位量 |
| winding number fluctuation | 世界线 QMC 中的刚度或超流密度 |
| $R_g$ 与 $d_F$ | cluster 空间延展和分形结构 |

这些关系依赖具体表象。普通自旋构型中随便定义的几何团簇，不一定等同于 FK cluster；loop 表象中的 winding，也不等同于任意 cluster 的 wrapping。使用前要先确认构型的几何连接规则来自哪一个统计权重。

## 测量实现的选择

若几何量只需要 cluster 大小，使用并查集通常最简单：

- 每条激活 bond 执行一次 union。
- 最后统计每个 root 的大小。
- 得到 $C_1,C_2,N_c$ 等量。

若需要 wrapping、winding、回转半径或 cluster 的空间形状，BFS/DFS 往往更直接：

- 队列中保存站点和展开坐标。
- 访问 bond 时同步记录边界穿越。
- cluster 生长完毕后计算大小、质心、$R_g$ 和绕行向量。

也可以把两者结合起来：并查集负责连通性，额外的边列表或位移表负责几何信息。关键是不要在生成 bond 后丢掉方向和周期位移，否则很多拓扑观测量无法可靠重建。
