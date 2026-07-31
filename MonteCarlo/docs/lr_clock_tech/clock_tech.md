# Clock 算法

长程模型的朴素困难是：一次更新似乎要检查一个站点和所有其他站点的相互作用。若系统有 $N$ 个格点，逐对检查的成本通常是

$$
O(N)
$$

每次局域更新，或者

$$
O(N^2)
$$

每个 sweep。Clock 类算法的目标是跳过那些“几乎肯定不会真正影响本次更新”的远距离相互作用，只访问少数可能触发事件的 pair。

这类方法的核心不是改变目标分布，而是把许多 Bernoulli 判断组织得更聪明。只要因子化和补偿步骤写对，采样的仍然是原来的长程模型。

`arXiv:2305.14082` 中的 clock factorized quantum Monte Carlo 可以看成这类思想在量子 Monte Carlo 中的系统化版本。它把 factorized Metropolis filter、bound rejection event、递归树结构和 worm 更新结合起来，目标是在长程相互作用或长程 hopping 存在时，把局域更新中本来需要访问 $O(N)$ 个相互作用项的步骤降到 $O(1)$ 或接近常数的候选事件抽样。

## 从一串 Bernoulli 事件开始

假设一次更新需要依次检查很多 pair，每个 pair 有一个事件概率

$$
p_{ij}.
$$

这个事件可以是：

- cluster 算法中，pair $ij$ 是否放 bond；
- factorized Metropolis 中，pair $ij$ 是否触发拒绝；
- 其他 rejection-free 或 event-chain 更新中的局域事件。

朴素做法是对每个 $j$ 抽一次随机数，判断事件是否发生。若大部分 $p_{ij}$ 都很小，这会浪费很多时间在“不发生”的判断上。

Clock 思想是：与其逐个问

$$
\text{第 }1\text{ 个不发生吗？第 }2\text{ 个不发生吗？}\cdots,
$$

不如直接抽样“下一次发生事件在第几个位置”。这和几何分布的思想相同。

## 构型无关的上界概率

困难在于，真实概率 $p_{ij}$ 往往依赖当前构型。例如 cluster 加键概率可能依赖 $s_i,s_j$ 是否满足低能条件；Metropolis 的拒绝概率可能依赖能量差。

因此先找一个构型无关的包络概率

$$
\hat p_{ij},
$$

使得对所有构型都有

$$
0\le p_{ij}\le \hat p_{ij}\le1.
$$

然后把真实事件拆成两步：

$$
p_{ij}
=
\hat p_{ij}
\frac{p_{ij}}{\hat p_{ij}}.
$$

第一步只用 $\hat p_{ij}$，不需要访问自旋构型；只有第一步触发后，才访问构型并用

$$
\frac{p_{ij}}{\hat p_{ij}}
$$

做第二次接受。这样保证总概率仍然是 $p_{ij}$。

直观地说，$\hat p_{ij}$ 是一个“候选事件”的概率，$p_{ij}/\hat p_{ij}$ 是候选事件成为真实事件的校正概率。只要上界成立，第二步概率就不会超过 $1$。

## 为什么可以加速

若 $\hat p_{ij}$ 很小，那么连续很多 pair 都不触发候选事件的概率很大。此时可以用累计概率一次性跳过一段。

设按某个顺序排列候选 pair：

$$
j=1,2,\cdots.
$$

从当前位置 $m$ 出发，下一次候选事件发生在 $n$ 的概率为

$$
\left[
\prod_{k=m}^{n-1}(1-\hat p_{ik})
\right]\hat p_{in}.
$$

因此可以预先保存累计量

$$
\Lambda_n
=
\sum_{k\le n}
-\ln(1-\hat p_{ik}).
$$

抽一个随机数 $u\in(0,1)$，令

$$
\Delta=-\ln u,
$$

然后在累计表中找到第一个满足

$$
\Lambda_n-\Lambda_{m-1}\ge \Delta
$$

的位置。中间那些 pair 就被一次性跳过了。

这就是 Clock 的“时钟”图像：每个 pair 都有一个触发率，随机时钟走到下一次响铃的位置时，才真正访问构型。

## 用在 cluster 加键中

长程 Swendsen-Wang 或 Wolff 更新中，真实加键概率可写为

$$
p_{ij}^{B}(s)
=
\mathbf 1_{\text{可加键}}(s_i,s_j)
\left(1-e^{-2\beta J_{ij}}\right).
$$

对铁磁 Ising 模型，只有同号自旋才可加键。因此可以取

$$
\hat p_{ij}^{B}
=
1-e^{-2\beta J_{ij}}.
$$

第一步根据 $\hat p_{ij}^{B}$ 抽候选 bond；第二步只检查当前 $s_i,s_j$ 是否同号。若同号，候选 bond 成为真实 bond；若不同号，则丢弃。

这样远距离小概率 bond 不需要逐条检查。对衰减足够快的幂律相互作用，候选事件数可以远小于 $N$。

## 用在 factorized Metropolis 中

普通 Metropolis 接受率看总能量差：

$$
P_{\rm acc}
=
\min(1,e^{-\beta\Delta E}).
$$

若能量差可分成 pair 贡献

$$
\Delta E=\sum_j\Delta E_{ij},
$$

可以使用因子化接受率：

$$
P_{\rm acc}
=
\prod_j
\min(1,e^{-\beta\Delta E_{ij}}).
$$

这等价于每个 pair 都有一个“拒绝事件”。若任意一个因子拒绝，本次更新就拒绝；若所有因子通过，更新接受。

对每个 pair，拒绝概率为

$$
p_{ij}^{A}
=
1-\min(1,e^{-\beta\Delta E_{ij}}).
$$

若能找到构型无关上界

$$
p_{ij}^{A}\le \hat p_{ij}^{A},
$$

就可以同样用 Clock 抽样下一次候选拒绝事件。候选拒绝触发后，再计算真实的 $p_{ij}^{A}/\hat p_{ij}^{A}$ 判断是否真的拒绝。

这一步比 cluster 更微妙，因为需要为能量差的拒绝概率找可靠上界。若自旋变量有界，例如 classical spin 满足 $|\mathbf S_i|=1$，通常比较容易构造；若变量无界，上界设计会困难得多。

## First-rejection 事件

Clock factorized QMC 的一个关键表述是 first-rejection event。因子化接受率为

$$
P_{\rm fac}
=
\prod_{j=1}^{N-1}P_j.
$$

可以把它理解成一串独立测试：

$$
1,2,\cdots,N-1.
$$

只要其中某一个因子拒绝，整个 proposed update 就拒绝。于是更新命运可以由“第一个拒绝来自哪里”决定：

$$
\text{first rejection at }j.
$$

若所有因子都通过，则更新接受。朴素顺序测试仍可能要检查 $O(N)$ 个因子；Clock 的目标是直接抽出第一个候选拒绝事件，而不是逐个检查。

真实拒绝概率为

$$
q_j=1-P_j.
$$

如果 $q_j$ 依赖当前构型，直接抽样仍然昂贵。于是引入构型无关上界

$$
q_j\le \hat q_j.
$$

先按 $\hat q_j$ 抽 first-bound-rejection event；抽到候选 $j$ 后，再用

$$
\frac{q_j}{\hat q_j}
$$

判断它是否成为真实拒绝。若不是，则继续往后抽下一个候选。这样既利用了构型无关表的快速抽样，又保留真实构型依赖概率。

## 递归 Clock 和树结构

当候选概率数量很多时，可以把所有 $\hat q_j$ 组织成一棵树。每个叶子对应一个 interaction factor；内部节点保存其子树中至少出现一个 bound rejection 的概率。

对一个节点 $A$，若其子节点为 $a$，则“子树中没有 bound rejection”的概率是

$$
\prod_{a\in A}(1-\hat q_a).
$$

所以该节点发生 bound rejection 的概率为

$$
\hat Q_A
=
1-
\prod_{a\in A}(1-\hat q_a).
$$

抽样时先在根节点判断是否有候选事件；若有，再递归进入对应子树，直到定位到某个叶子 $j$。这就是 recursive clock sampling 的树结构图像。

这个结构的价值是：

- 远距离小概率事件可以被批量跳过。
- 若相互作用只依赖距离，表可以预计算并复用。
- 若某些概率随参数变化，可以只更新树的一部分。
- 对大量小概率离散事件，可以达到 $O(1)$ 或 $O(\log N)$ 级别的候选抽样成本。

实际实现中，树结构、累计表、Walker alias、dynamic thinning 都是在解决同一个问题：如何从一大组小概率事件中快速抽到下一次候选事件。

## 与量子 Worm 的结合

Clock 技巧不只适用于经典 Metropolis。长程量子模型的世界线构型中，某个局域更新常常只改变一个站点在虚时区间

$$
[\tau_1,\tau_2]
$$

上的占据数或自旋状态。若存在长程密度-密度相互作用，则这个局域改变会影响它和所有其他世界线之间的作用量：

$$
\Delta U
=
\sum_j \Delta U_j.
$$

普通 Metropolis 需要逐个计算所有 $\Delta U_j$，成本为 $O(N)$。因子化后写成

$$
P_{\rm fac}
=
\prod_j
\exp[-(\Delta U_j)^+].
$$

然后同样用 bound rejection event 和 recursive clock 抽样第一个可能拒绝的相互作用项。

在 extended Bose-Hubbard 的 worm 算法中，常见更新包括：

- create/delete worm；
- move worm head；
- insert/delete kink before worm head；
- insert/delete kink after worm head。

这些更新虽然在世界线图像中不同，但只要它们对长程对角相互作用的改变能分解为一组 $\Delta U_j$，就可以套用同一个 Clock factorized filter。

若还有长程 hopping，proposal 本身也要设计。一个自然选择是让跳跃目标 $j$ 的 proposal 概率与 hopping 强度同阶，例如

$$
\mathcal A(i\to j)
\propto
t_{ij}.
$$

这样可以抵消接受率里随距离衰减的 hopping 因子，避免大量提出几乎不会接受的远距离 kink。由于 $\mathcal A(i\to j)$ 只依赖格点几何和 hopping 参数，可以预先用 alias table 抽样。

## 代价和 box 技巧

因子化 Metropolis 的接受率通常小于或等于普通 Metropolis。原因是普通 Metropolis 先求总能量差：

$$
\Delta E=\sum_j\Delta E_j,
$$

不同项之间可以互相补偿；因子化形式

$$
\prod_j e^{-[\Delta E_j]^+}
$$

逐项拒绝，丢掉了这种补偿。

对非阻挫、绝对能量 extensive 的体系，这个代价往往可以接受，换来的 $O(N)\to O(1)$ 或近似 $O(1)$ 加速很值得。对阻挫或慢衰减长程体系，接受率可能下降明显。

一种折中办法是 box technique：把若干容易互相补偿的 interaction terms 合成一个 box，对每个 box 做因子化：

$$
P_{\rm fac}^{\rm box}
=
\prod_B
\exp\left[
-
\left(
\sum_{j\in B}\Delta E_j
\right)^+
\right].
$$

若每个 box 只含一个项，就回到完全因子化；若所有相互作用放进同一个 box，就回到普通 Metropolis。实际算法可以在二者之间选择，以平衡接受率和计算成本。

## 上界怎么选

上界 $\hat p_{ij}$ 必须满足两个要求：

1. 对所有可能构型都大于等于真实概率。
2. 不能比真实概率大太多，否则候选事件太多，加速效果会变差。

对铁磁幂律耦合，一个自然上界通常随距离衰减：

$$
\hat p_{ij}\sim \beta J_{ij}
\sim
\frac{\beta}{r_{ij}^{d+\sigma}}
$$

在弱耦合或远距离处成立。近距离 pair 的概率可能不小，可以直接逐条检查；Clock 主要负责跳过大量远距离小概率 pair。

## 算法骨架

一个典型 Clock 抽样过程如下：

1. 为每个距离壳层或每个候选 pair 构造 $\hat p_{ij}$。
2. 预计算累计表 $\Lambda_n=\sum_{k\le n}-\ln(1-\hat p_{ik})$。
3. 从当前位置开始抽 $\Delta=-\ln u$。
4. 用二分查找或 alias/cumulative table 找到下一次候选事件。
5. 访问构型，计算真实概率比例 $p_{ij}/\hat p_{ij}$。
6. 若第二步接受，则执行真实事件；否则继续抽下一次候选事件。

如果相互作用只依赖距离，累计表可以对所有站点复用；若耦合还依赖方向、边界或无序，需要为相应类别分别建表。

## 常见检查

Clock 算法最需要检查的是“加速之后采样的还是不是原模型”。可以做几个测试：

- 小系统上和朴素 $O(N^2)$ 枚举算法比较能量、磁化和 bond 数。
- 统计候选事件成为真实事件的频率，确认平均概率和理论 $p_{ij}$ 一致。
- 检查 detailed balance 或 global balance 的推导没有因为上界选择而破坏。
- 改变上界的松紧，物理结果应保持一致，只有运行时间变化。
- 对长程周期格子，确认 pair 顺序和累计表没有漏掉或重复某些距离壳层。

概括地说，Clock 算法不是一个新的物理近似，而是一种事件抽样技巧。它的价值在于把大量小概率远程判断从“逐个检查”改成“直接跳到下一次可能发生的地方”。
