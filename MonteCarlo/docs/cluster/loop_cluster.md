# 蠕虫算法

蠕虫算法 worm algorithm 是一类非常重要的非局域更新。它的核心思想是：

> 不强行让构型每一步都停留在配分函数空间，而是临时引入两个缺陷端点，让一个端点在构型中移动、沿路修改 bond 或 worldline，最后两个端点相遇并湮灭，回到物理构型空间。

这个思想和 [集团算法](cluster_algo.md) 很像：二者都会一次改变一串、一个团簇或一个大尺度几何对象，从而降低自关联时间。区别在于：

| 算法 | 几何对象 | 主要空间 |
| --- | --- | --- |
| cluster | 连通团簇 | 通常一直在配分函数空间 |
| loop | 闭合路径 | 通常一直满足局域约束 |
| worm | 带两个端点的开路径 | 临时进入格林函数空间 |

以下以 Ising 模型的 loop representation 为主线，说明 ordinary worm、irregular worm、lifted worm 与 loop-cluster 表象之间的关系。

## 从 Ising 到 loop 表象

考虑无外场 ferromagnetic Ising 模型。先把后面会用到的图论符号固定下来：

| 符号 | 含义 |
| --- | --- |
| $G=(V,E)$ | 格子图，$V$ 是顶点集合，$E$ 是最近邻边集合 |
| $\lvert V\rvert$ | 顶点数，也就是格点数；若线性尺寸为 $L$，则 $\lvert V\rvert=L^d$ |
| $\lvert E\rvert$ | 无向最近邻边数；$d$ 维 hypercubic lattice 上 $\lvert E\rvert=dL^d$ |
| $A\subseteq E$ | high-temperature 展开中被选中的边集合，也叫 occupied bonds 或 active bonds |
| $\lvert A\rvert$ | 当前 occupied bond 的条数 |
| $d_i(A)$ | 集合 $A$ 中与顶点 $i$ 相接的 occupied bond 条数 |

这里的 $A$ 只表示“当前被占据的边集合”。在算法状态中，可以把每条边记录为占据或未占据，分别对应 $e\in A$ 与 $e\notin A$。

模型配分函数为：

$$
Z
=
\sum_{\{\sigma\}}
\exp\left(
K\sum_{\langle ij\rangle}\sigma_i\sigma_j
\right),
\qquad
\sigma_i=\pm1.
$$

对每条边使用恒等式：

$$
e^{K\sigma_i\sigma_j}
=
\cosh K
\left(
1+\sigma_i\sigma_j\tanh K
\right).
$$

令：

$$
x=\tanh K.
$$

展开所有边：

$$
Z
=
(\cosh K)^{|E|}
\sum_{\{\sigma\}}
\prod_{\langle ij\rangle}
\left(
1+x\sigma_i\sigma_j
\right).
$$

每条边有两种选择：

- 不选这条边，贡献 $1$；
- 选这条边，贡献 $x\sigma_i\sigma_j$。

把被选中的边集合记为 $A\subseteq E$。则：

$$
\prod_{\langle ij\rangle\in A}
x\sigma_i\sigma_j
=
x^{|A|}
\prod_i\sigma_i^{d_i(A)}.
$$

其中 $d_i(A)$ 是边集合 $A$ 中与顶点 $i$ 相连的激活边数。

对自旋求和：

$$
\sum_{\sigma_i=\pm1}\sigma_i^{d_i(A)}
=
\begin{cases}
2, & d_i(A)\text{ 为偶数},\\
0, & d_i(A)\text{ 为奇数}.
\end{cases}
$$

所以只有每个顶点度数都是偶数的图会留下来。于是：

$$
Z
=
2^{|V|}(\cosh K)^{|E|}
\sum_{A\in{\rm even}}
x^{|A|}.
$$

这就是 Ising 的 loop representation 或 high-temperature graph representation。

到这里为止，可以把构型从自旋变量 $\{\sigma_i\}$ 换成边集合 $A$。边集合 $A$ 的统计权重为

$$
W(A)\propto x^{|A|},
$$

但它只能在满足偶度约束时贡献给配分函数。

这里的 $A\in{\rm even}$ 表示：

> 每个顶点都有偶数条激活 bond。

因此激活 bond 组成的是闭合 loop 的集合。没有端点，没有孤立的奇度顶点。

## 为什么需要 worm

在 even graph 空间里，如果只做局域更新，会很不方便。因为单独翻转一条 bond 会让这条边的两个端点度数奇偶性改变，产生两个奇度顶点，构型立刻离开 $Z$ 空间。

如果强行只在 $Z$ 空间更新，最小的局域合法变化通常是翻转一个闭合 plaquette 或一条闭合 loop。这类更新可以做，但设计和遍历性会依赖模型和几何。

worm 算法换了一个角度：

> 允许中间构型出现两个奇度顶点，把它们看作 worm 的两个端点。

设两个端点为：

```text
Ira
Masha
```

当 `Ira != Masha` 时，构型属于开图空间，也常叫格林函数空间 $\mathcal G$。当 `Ira == Masha` 时，两个缺陷湮灭，所有顶点重新为偶度，构型回到配分函数空间 $\mathcal Z$。

可以写成扩展空间：

$$
\mathcal Z_{\rm ext}
=
\mathcal Z
+
\omega_G\mathcal G.
$$

在 Ising loop 表象中：

- $\mathcal Z$：所有顶点偶度的闭合 loop 构型；
- $\mathcal G$：恰有两个奇度顶点的开路径构型；
- worm head 移动时，沿途切换 bond 占据状态。

## 普通 worm 更新

最基础的 Ising worm 更新可以这样理解。

从一个 even graph 出发：

1. 随机选一个站点，让 `Ira = Masha`。
2. 随机选择一个端点作为活动端点，通常移动 `Ira`。
3. 从 `Ira` 随机选择一个近邻方向。
4. 设对应边为 $e=(i,j)$。
5. 若 $e$ 已占据，则删除它，并把 `Ira` 移到 $j$。
6. 若 $e$ 未占据，则以概率 $x=\tanh K$ 添加它，并把 `Ira` 移到 $j$。
7. 若 `Ira == Masha`，worm 闭合，回到 $\mathcal Z$ 空间。

写成伪代码：

```text
Ira = random site
Masha = Ira

while true:
    with probability 1/2:
        swap(Ira, Masha)

    choose random nearest-neighbor direction
    j = neighbor(Ira, direction)
    e = bond(Ira, j)

    if bond[e] occupied:
        bond[e] = empty
        Ira = j
    else:
        with probability x = tanh(K):
            bond[e] = occupied
            Ira = j

    if Ira == Masha:
        break
```

这就是 ordinary worm 的最小结构：未占据 bond 添加时以 $x=\tanh K$ 接受，已占据 bond 删除时直接接受。

## 为什么接受率是这样

loop 表象中构型权重为：

$$
W(A)\propto x^{|A|}.
$$

若添加一条 bond：

$$
|A|\to |A|+1,
$$

权重比为：

$$
{W(A')\over W(A)}=x.
$$

因此对称选边 proposal 下，添加 bond 的接受率可以取：

$$
P_{\rm add}=x=\tanh K.
$$

若删除一条 bond：

$$
|A|\to |A|-1,
$$

权重比为：

$$
{W(A')\over W(A)}={1\over x}.
$$

由于 $0<x<1$，${1/x}>1$，Metropolis 接受率为 1。

所以普通 Ising worm 的局部规则非常简单：

| 当前 bond | 操作 | 接受概率 |
| --- | --- | --- |
| 空 | 添加 | $\tanh K$ |
| 占据 | 删除 | $1$ |

它的直观含义是：loop 表象中每条激活 bond 都带一个因子 $x$，所以添加一条要付出 $x$ 的权重代价，删除一条则提高权重。

## 奇度端点如何移动

每次切换一条边的占据状态，会改变这条边两端顶点的度数奇偶性。

如果活动端点在 $i$，另一端点在 $m$，切换边 $ij$ 后：

- 顶点 $i$ 的奇偶性改变；
- 顶点 $j$ 的奇偶性改变；
- 由于 $i$ 原本是奇点，切换后 $i$ 变回偶点；
- $j$ 变成新的奇点。

所以奇点从 $i$ 移动到 $j$。这就是 worm head 在图上走动的几何图像。

当 $j=m$ 时，两个奇点相遇并消失，构型回到所有顶点偶度的 $\mathcal Z$ 空间。

## 配分函数空间更新和格林函数空间更新

这里比较 $\mathcal Z$ 更新和 $\mathcal G$ 更新。

worm 更新有两种常见组织方式：

| 方式 | 行为 |
| --- | --- |
| 完整 worm | 从 $\mathcal Z$ 出发，运行到端点相遇，再回到 $\mathcal Z$ |
| 扩展空间单步更新 | 在扩展空间中走一步，若端点相遇则重新随机创建端点 |

`Worm()` 更像一次完整更新：

```text
closed graph
  -> create two coincident endpoints
  -> move endpoint many steps
  -> endpoints meet
  -> closed graph
```

`Worm_G()` 更像在 $\mathcal Z+\mathcal G$ 扩展系综中逐步演化：

```text
extended state
  -> move one worm endpoint by one step
  -> if closed, restart endpoints
```

两种写法的目标不同。若只想采样物理构型，可以在 worm 闭合时测量；若还想利用 worm 端点分离分布测量关联函数，则 $\mathcal G$ 空间本身也有物理含义。

## 关联函数的直觉

Ising 自旋关联函数：

$$
\langle \sigma_i\sigma_j\rangle
$$

在 high-temperature graph 表象中，对应两个奇度端点固定在 $i,j$ 的图权重与普通 even graph 权重之比。

因此 worm 算法中两个端点的相对位置分布天然携带关联函数信息。粗略地说：

> worm 两端经常相距多远，反映了系统中自旋相关能传播多远。

这也是 worm 算法非常适合测量 Green 函数或关联函数的原因。世界线 QMC 中的 worm 端点通常直接对应产生 / 湮灭算符插入；Ising loop 表象中则对应两个奇度缺陷。

## Irregular / lifted worm

普通 worm 每一步随机选近邻方向，然后根据该边是否占据决定添加或删除。它的随机游走会频繁回头，尤其在高维或临界附近可能效率不够。

irregular / lifted worm 在普通 worm 的基础上引入一个额外变量：

$$
\lambda=\pm1.
$$

可以理解为：

- $\lambda=+1$：当前倾向于增加 bond；
- $\lambda=-1$：当前倾向于删除 bond。

若更新成功，$\lambda$ 保持不变；若更新失败，$\lambda$ 反向。这样 Markov chain 不再像普通随机游走那样每步完全重新选择“加或删”，而是在扩展状态空间中带有一种持续方向。

这就是 lifted 思想：

> 在状态空间中增加方向变量，让链少做无意义的来回抖动；可以不满足传统 detailed balance，但要满足 global balance。

## 顶点度数

irregular worm 的局部选择依赖活动端点 `Ira` 的顶点度数。

定义：

$$
n_i
=
\#\{\text{incident occupied bonds at }i\}.
$$

在 $d$ 维 hypercubic lattice 上：

$$
{\rm NNb}=2d.
$$

若 $\lambda=+1$，算法只从空 bond 中选择一条来尝试添加。因此可选方向数为：

$$
{\rm NNb}-n_i.
$$

若 $\lambda=-1$，算法只从已占据 bond 中选择一条来尝试删除。因此可选方向数为：

$$
n_i.
$$

对应的两个基本动作是：

| 动作 | 含义 |
| --- | --- |
| 添加 bond | 从未占据 incident bond 中抽一条，尝试添加 |
| 删除 bond | 从已占据 incident bond 中抽一条，尝试删除 |

## Irregular worm 的接受率

因为 proposal 不再是“从所有方向均匀选”，而是“从空边或占据边中均匀选”，所以接受率要补偿 proposal 的不对称性。

设当前活动端点为 $i$，候选邻居为 $j$，当前度数为 $n_i,n_j$，总近邻数为 $q=2d$，并令：

$$
x=\tanh K.
$$

当 worm 处于开图空间，即两个端点不同，添加一条空 bond 的接受率可写成：

$$
P_{\rm inc}
=
x\,
{q-n_i\over n_j+1}.
$$

删除一条占据 bond 的接受率可写成：

$$
P_{\rm dec}
=
{n_i\over x\,(q-n_j+1)}.
$$

实际接受概率使用：

$$
\min(1,P_{\rm inc})
\quad\text{或}\quad
\min(1,P_{\rm dec}).
$$

实际接受概率使用 $\min(1,P)$。当未截断的 $P>1$ 时，该 proposal 总是被接受。

这些因子的来源是 proposal 选择数的修正。例如添加前从 $q-n_i$ 条空边中选一条；添加后，反向删除时邻居 $j$ 上相应占据边数量变成 $n_j+1$。因此 detailed/global balance 的权重比不只是 $x$，还要乘上 proposal 比。

## 端点重合时的修正

当 $\mathrm{Ira}=\mathrm{Masha}$ 时，worm 位于 $\mathcal Z$ 空间的入口 / 出口。此时两个端点重合，选择活动端点和反向过程有额外对称性，接受率需要包含两端选择贡献的和。

添加时：

$$
P_a
=
{1\over q-n_i}
+
{1\over q-n_j},
$$

$$
P_b
=
{1\over n_i+1}
+
{1\over n_j+1},
$$

$$
P_{\rm inc}^{(0)}
=
x\,{P_b\over P_a}.
$$

删除时：

$$
P_a
=
{1\over n_i}
+
{1\over n_j},
$$

$$
P_b
=
{1\over q-n_i+1}
+
{1\over q-n_j+1},
$$

$$
P_{\rm dec}^{(0)}
=
{1\over x}\,{P_b\over P_a}.
$$

这部分是 irregular worm 最容易写错的地方。普通 worm 的规则很简单，但 irregular worm 因为按空边 / 占据边定向抽样，必须在端点重合处正确处理 proposal multiplicity。

## Irregular worm 伪代码

一轮完整 `irrWorm()` 可以写成：

```text
Ira = random site
Masha = Ira

while true:
    with probability 1/2:
        swap(Ira, Masha)

    n = degree(Ira)

    if lambda == +1 and n < q:
        choose one empty incident bond uniformly
        compute degree of neighbor j
        accept add with corrected probability
        if accepted:
            occupy bond
            Ira = j
        else:
            lambda = -1

    else if lambda == -1 and n > 0:
        choose one occupied incident bond uniformly
        compute degree of neighbor j
        accept delete with corrected probability
        if accepted:
            empty bond
            Ira = j
        else:
            lambda = +1

    else:
        lambda = -lambda

    if Ira == Masha:
        break
```

其中 $\mathrm{degree}(\mathrm{Ira})$ 表示活动端点相邻的 $2d$ 条边中已有占据的条数。

## 格点与 bond 的索引

在 hypercubic lattice 上，worm 更新需要能从格点索引稳定地找到相邻格点和相邻 bond。关键量包括：

| 量 | 含义 |
| --- | --- |
| $d$ | 空间维度 |
| $L$ | 每个方向线性尺寸 |
| $L^d$ | 系统体积 |
| $2d$ | 每个格点的近邻方向数 |
| bond 占据变量 | 记录每条无向边是否属于当前图构型 |
| $\mathrm{Ira},\mathrm{Masha}$ | worm 两个端点 |
| $\lambda$ | lifted 或 irregular 更新中的方向变量 |
| $x$ | $\tanh K$ |

对 $d$ 维 hypercubic lattice，最近邻无向边数为：

$$
|E|=dL^d.
$$

因此只需要存每条无向边一次。虽然近邻方向有 $2d$ 个，但正方向和负方向指向同一条无向 bond。bond 索引的作用就是把任意方向的相邻关系映射到唯一的无向边。

这点很重要：worm head 移动时可以沿正向或负向走，但切换的是同一条物理 bond。

## Bond 构型的合法性

在 $\mathcal Z$ 空间中，每个顶点必须偶度：

$$
n_i\equiv0\pmod2.
$$

在 $\mathcal G$ 空间中，除 `Ira` 和 `Masha` 外，其他顶点偶度；两个端点奇度。

这给调试提供了最直接的检查：

```text
如果 Ira == Masha:
    所有顶点 degree 都必须为偶数
else:
    Ira 和 Masha 为奇数 degree
    其他顶点为偶数 degree
```

loop-cluster 更新在回溯得到闭合路径后，也需要检查每个顶点度数是否为偶数。worm 更新同样应检查 bond 索引、周期边界和接受率是否共同保持正确的奇偶约束。

## Loop-cluster 和 worm 的关系

loop-cluster 更新和 worm 不同，但可以使用同一个 bond 构型语言。

它的流程大致是：

1. 对所有空 bond，以概率 $x=\tanh K$ 激活。
2. 对激活 bond 形成的图做 DFS。
3. 当 DFS 遇到已经访问过且不是父节点的邻居时，检测到一个 loop。
4. 沿父指针回溯，找出该 loop 的边。
5. 以概率 $1/2$ 标记并切换这条 loop。
6. 最后清理临时标记，得到新的 even graph。

这类算法更接近 loop / cluster 更新：它试图在闭合图结构中找出可整体切换的 loop。而 worm 则是从两个端点的开路径出发，让端点随机移动并沿路切换 bond。

可以这样区分：

| 方法 | 中间是否允许奇度端点 | 更新对象 |
| --- | --- | --- |
| loop-cluster | 通常不强调开放端点 | 检测到的闭合 loop |
| ordinary worm | 允许两个奇度端点 | worm 走过的开路径 |
| irregular/lifted worm | 允许两个奇度端点，并引入 $\lambda$ | 带方向持续性的开路径 |

## 观测量

loop representation 中最基本的构型是边集合 $A$。因此很多观测量都先从 $A$ 出发，再进一步分析它的连通结构、端点运动或闭合时间。

最简单的量是 occupied bond 数：

$$
N_b=\lvert A\rvert
=
\sum_{e\in E} n_e,
\qquad
n_e=
\begin{cases}
1, & e\in A,\\
0, & e\notin A.
\end{cases}
$$

这里 $n_e$ 是边 $e$ 的占据变量，因此 $\lvert A\rvert$ 就是 occupied bonds 的总数。

常见测量对象包括：

| 量 | 含义 |
| --- | --- |
| $N_b=\lvert A\rvert$ | occupied bond 数，也就是当前图中被占据的边数 |
| $T_{\rm worm}$ | worm 从创建到闭合的步数 |
| $C_1,C_2$ | 最大、次大 loop cluster 大小 |
| $S_2,S_4$ | cluster size moments |
| $R(s,L)$ | 给定 cluster size 的回转半径 |
| $n(s,L)$ | cluster size distribution |
| endpoint distance | worm 两端分离分布，对应关联信息 |

这些量的测量时机略有不同：

- $N_b$ 是闭合图和开图中都可以定义的即时构型量。
- $T_{\rm worm}$ 只有在一次 worm 从创建到闭合以后才完整。
- $C_1,C_2,S_2,S_4,R(s,L),n(s,L)$ 通常在 worm 闭合、构型回到 $\mathcal Z$ 空间以后测量，因为这时所有顶点重新满足偶度约束。
- endpoint distance 属于 $\mathcal G$ 空间测量，关注两个端点分离时的统计分布。

lifted worm 的测量通常会在多次 worm 运动后累积：

- worm return time；
- bond 数及平方；
- worm 走动过程中的 unwrapped distance；
- bond number 和 worm time 的 histogram。

这说明 worm 算法不只是更新工具，也自然给出几何和关联长度相关的信息。尤其在高维 Ising 的 loop representation 中，worm 的空间扩散性质和 loop 几何量对有限尺寸标度很敏感。

## 和高维 Ising 有什么关系

高维 Ising 在 $d>4$ 后进入平均场临界行为，但周期边界条件下会出现比较细的有限尺寸标度结构。自旋表象和 loop / FK 几何表象看到的对象不完全一样。

loop representation 中，磁化率、关联长度和 loop 几何常可以通过随机游走 / loop 的语言理解。例如 worm return time、端点扩散距离、loop cluster size 等量，都在反映同一个问题：

> 临界涨落如何在高维周期盒子中延展？

这也是高维 Ising 研究常使用 loop 表象的原因：它把有限尺寸行为变成了可测量的几何对象。

## 和世界线 worm 的关系

[连续时间 Worm](../qworm/CTQW.md) 和 [连续空间 Worm](../qworm/CSQW.md) 与这里的 Ising loop worm 共享同一个框架：

```text
Z space:
    物理构型，没有开放端点

G space:
    插入两个算符或两个缺陷端点

worm update:
    创建端点 -> 移动端点 -> 修改局部构型 -> 湮灭端点
```

差别在于具体构型语言：

| 场景 | 构型 | worm 端点含义 |
| --- | --- | --- |
| Ising loop | 激活 bond 图 | 两个奇度顶点 |
| SSE / 顶点模型 | operator string / vertex legs | 改变局域顶点状态的入口和出口 |
| 连续时间世界线 | 虚时 kink 和 occupation | 产生 / 湮灭算符插入 |
| 连续空间世界线 | 粒子路径 | open worldline endpoints |

因此，学 Ising loop worm 的价值不只在 Ising 模型本身。它给出了 worm 算法最干净的离散图版本，有助于理解更复杂的量子 Monte Carlo worm。

## 与集团算法的对照

cluster 和 worm 都是为了解决临界慢化，但它们切入点不同。

| 项目 | cluster | worm |
| --- | --- | --- |
| 表象 | FK / random-cluster 或 embedded Ising | loop / high-temperature graph / worldline |
| 更新对象 | 一整个连通团簇 | 一条由端点扫出的路径 |
| 合法性 | cluster 翻转后仍在物理空间 | 中间允许进入 $\mathcal G$ 空间 |
| 适合观测 | cluster size、wrapping、几何连通性 | Green function、关联函数、return time、loop 几何 |
| 常见难点 | bond 生成、连通分量、几何测量 | 端点权重、proposal 修正、闭合时间 |

一个实用判断是：

- 如果模型有自然的 FK 表象，cluster 更新通常最自然。
- 如果模型有守恒流、loop、worldline 或需要测关联函数，worm 往往更自然。
- 如果普通 worm 随机游走太慢，可以考虑 directed / lifted / irregular worm。

## 文献中的几条推广线

`PhysRevE.97.042126` 的 lifted worm 版本说明，worm 不一定要是可逆随机游走。可以在扩展空间里再引入一个 lifting 变量，让端点在一段时间内保留运动方向或更新模式，只有在特定事件后才改变该变量。这样做的目标不是改变目标分布，而是减少端点来回撤销同一段路径的概率。检查这类算法时，重点从 ordinary detailed balance 转成全局平衡或成对的 lifted balance：扩展变量求和以后，边缘分布仍必须是原来的 loop 权重。

`arXiv:2306.12218` 把 $O(N)$ 自旋模型写成一族图表示。其要点是：不同分量可以被组织成 directed flow 子图和 undirected loop 子图；在每个格点上，前者满足流守恒，后者满足 Euler 偶度条件。这样 Ising、XY、Heisenberg 以及更高 $N$ 的模型可以放在同一类 worm 更新语言下。worm 的“端点违反局域约束”不是 Ising loop 的特殊技巧，而是许多图表示中都能使用的通用更新思想。

`arXiv:1909.02719v2` 的 Loop-Cluster 思路则把 Potts 模型的 FK bond 变量和 $q$-flow loop 变量耦合起来。它强调 SW cluster、loop 表象和 worm/loop 更新之间不是互斥关系：同一个 Potts 模型可以在 spin、FK bond、flow loop 这些表象之间转换，算法效率取决于哪个表象让约束和大尺度运动最容易处理。

因此可以把 Potts 和 $O(N)$ 中的算法关系粗略整理成：

| 模型 | cluster 线索 | worm / loop 线索 |
| --- | --- | --- |
| Ising | FK cluster、SW、Wolff | high-temperature even graph、ordinary/lifted worm |
| q-Potts | FK random-cluster、SW | q-flow loop、LC joint model |
| $O(N)$ | embedded Ising / Wolff reflection | flow-loop 图表示、按局域守恒约束移动端点 |

这张表不表示每个模型都有同样简单的接受率。它只说明设计算法时可以先问两个问题：是否有自然的 bond cluster 条件分布？是否有自然的 loop/flow 守恒约束？前者通常导向 SW/Wolff，后者通常导向 worm。

## 正确性检查清单

worm 更新最容易错的地方通常在局域约束和索引一致性。可以按下面顺序检查：

1. `Bond` 是否每条无向边只存一次。
2. `getNNSite` 和 `getNNBond` 在周期边界下是否一致。
3. $\mathcal Z$ 空间中所有顶点是否偶度。
4. $\mathcal G$ 空间中是否只有两个奇度端点。
5. 添加 bond 的权重因子是否为 $x=\tanh K$。
6. 删除 bond 是否正确使用反向权重比。
7. irregular worm 是否补偿了空边 / 占据边选择数。
8. 端点重合时 proposal multiplicity 是否单独处理。
9. `Tworm`、$N_b$、端点位移等观测量是否只在合适时机测量。
10. 小系统是否能和精确枚举或普通 worm 比较。

## 小结

蠕虫算法的关键在于它改变了更新空间：

$$
\mathcal Z
\quad\longrightarrow\quad
\mathcal Z+\omega_G\mathcal G.
$$

在 $\mathcal Z$ 中，构型必须满足所有局域约束；在 $\mathcal G$ 中，两个端点暂时违反约束，并把这种违反沿图移动。端点走过的路径不断切换 bond，最后闭合时就得到一个新的合法 loop 构型。

普通 worm 用最简单的权重比 $x=\tanh K$ 添加 bond、删除 bond 总接受；irregular / lifted worm 则进一步引入方向变量 $\lambda$，按空边或占据边定向抽样，并用度数修正接受率。前者清楚，后者更高效，但也更容易写错。

和 cluster 算法一样，worm 的最终评价标准仍然只有两个：

> 采样的目标分布是否正确？自关联时间是否真正下降？
