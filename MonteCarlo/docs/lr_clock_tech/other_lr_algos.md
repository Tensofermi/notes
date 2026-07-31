# 其他长程算法

长程相互作用的主要困难是：每个自由度都可能和系统中大量其他自由度相互作用。若每次局域更新都重新计算能量差，代价通常是

$$
\mathcal O(N)
$$

一次 sweep 就变成

$$
\mathcal O(N^2).
$$

对于相互作用

$$
J(r)\sim \frac{1}{r^{d+\sigma}},
$$

远距离项虽然单个很小，但数量很多；截断得太粗会改变有限尺寸行为，完整保留又会让程序很慢。Clock 算法是一种重要加速思路，除此之外还有几类常见办法。

## 直接截断

最简单做法是设定截断半径 $R_c$：

$$
J(r)=0,\qquad r>R_c.
$$

这样每个格点只和半径 $R_c$ 内的点相互作用，单次局域更新代价变为

$$
\mathcal O(R_c^d).
$$

截断的优点是实现简单，缺点也很明显：如果研究对象正是长程临界行为，粗截断会改变物理。它适合以下情况：

- 长程尾部衰减很快。
- 只关心短程主导的区域。
- 用多个 $R_c$ 做外推，检查结果是否稳定。

实际使用时，最好记录有效相互作用：

$$
J_{ij}^{\rm eff}=J(r_{ij})\Theta(R_c-r_{ij}),
$$

并在论文或笔记中说明截断方案。不同截断方式会带来不同的有限尺寸修正。

## 最小镜像与周期求和

周期边界下，距离可以用最小镜像定义：

$$
r_{ij}
=
\min_{\mathbf n\in \mathbb Z^d}
|\mathbf r_i-\mathbf r_j+\mathbf n L|.
$$

这给出一个 $N-1$ 个有效相互作用对象的朴素长程模型。另一种做法是把所有周期镜像都加进来：

$$
J_{ij}^{\rm image}
=
\sum_{\mathbf n\in \mathbb Z^d}
\frac{1}
{|\mathbf r_i-\mathbf r_j+\mathbf nL|^{d+\sigma}}.
$$

镜像求和更接近无限周期阵列，但实现上要处理收敛和自相互作用。对于幂律相互作用，镜像求和可能收敛较慢，需要 Ewald 类分解。

选择哪一种定义，会影响有限尺寸数据。重要的是在模拟和标度分析中保持一致。

## Ewald 类分解

Ewald 方法常用于库仑相互作用，也可以推广到某些长程核。它的思想是把慢收敛的实空间求和拆成两部分：

$$
J(r)=J_{\rm short}(r)+J_{\rm long}(r).
$$

其中 $J_{\rm short}$ 在实空间快速衰减，$J_{\rm long}$ 在动量空间处理。形式上常写成

$$
\sum_{\mathbf r} J(\mathbf r)O(\mathbf r)
=
\sum_{\mathbf r} J_{\rm short}(\mathbf r)O(\mathbf r)
+
\sum_{\mathbf k} \tilde J_{\rm long}(\mathbf k)\tilde O(\mathbf k).
$$

这种方法适合能量或场可以写成卷积的情形。它的优势是精度高、有限尺寸定义清楚；代价是实现复杂，并且对每种相互作用核都要重新推导合适的分解。

## Luijten-Blote 思想

长程 Swendsen-Wang 或 Wolff 更新中，若逐一检查所有远距离键，代价很高。Luijten-Blote 算法利用累计概率跳过大量未占据的键。

设从某个格点出发，第 $j$ 个候选键的加键概率为

$$
p_j=1-e^{-2\beta J_j}.
$$

直接做法是对每个 $j$ 抽一次随机数。若很多 $p_j$ 很小，大部分尝试都会失败。更好的做法是先抽出“下一次成功出现在哪里”。定义未成功的累计概率：

$$
Q(n)=\prod_{j=1}^{n}(1-p_j).
$$

若随机数 $u\in(0,1)$，可以通过

$$
Q(n)<u\le Q(n-1)
$$

确定下一个被访问的候选位置。这样算法直接跳过一段失败事件，只在可能加键的位置访问构型。

这一思想和 Clock 算法很接近：把许多小概率事件的逐个判断，改成对等待距离的抽样。

Luijten-Blote 的关键是：候选距离的抽样只依赖耦合常数和温度，而不依赖当前自旋取值。以长程 ferromagnetic Ising 为例，先按

$$
p_j=1-e^{-2\beta J_j}
$$

抽出候选 bond 的距离或排序位置，再检查该 pair 是否满足 Ising / Potts 的加键条件。若条件不满足，候选 bond 丢弃；若满足，就加入 cluster。这样不会改变真实加键概率，因为候选步骤和构型检查相乘后仍然等于原来的 SW 加键规则。

算法骨架可以写成：

```text
for each seed or active cluster site i:
    n = 0
    while n < number_of_possible_partners:
        draw next candidate index n from cumulative no-bond table
        map n to partner j
        if spin condition is satisfied:
            activate bond (i,j)
            add j to cluster if new
        continue from n + 1
```

这里最容易错的是“排序位置到真实格点 $j$”的映射。对平移不变格子，可以按位移壳层预先建立表；对无序图或开边界系统，则需要为每个 $i$ 维护不同的候选列表。只要候选列表和朴素 $O(N^2)$ SW 使用同一组 $J_{ij}$，该加速不会引入截断。

## Fukui-Todo 的 $O(N)$ cluster 方法

Fukui-Todo 算法进一步把长程 cluster 的复杂度降到 $O(N)$ 量级。它的目标不是近似长程 SW，而是生成与朴素长程 Swendsen-Wang 完全等价的随机动力学。文献 `arXiv:0802.0272` 和 JCP `10.1016/j.jcp.2008.12.022` 强调了三点：

- 不截断相互作用范围；
- 满足 detailed balance；
- 生成的随机动力学等价于完整 $O(N^2)$ Swendsen-Wang。

它和 Luijten-Blote 的共同点是都跳过大量未占据 bond；区别在于 Fukui-Todo 使用更适合批量抽样的累计概率和数据结构，使得长程 Ising cluster sweep 可以达到线性复杂度。核心抽样问题可以写成：

$$
P(\text{next active bond is }m)
=
\left[
\prod_{k<n}^{m-1}(1-p_k)
\right]p_m.
$$

其中 $p_k=1-e^{-2\beta J_k}$。如果能够快速从这个分布中抽样下一条 active bond，就不需要检查中间大量未激活的远距离 pair。cluster 生长本身仍然是 SW：active bond 只是在满足同色或同向条件时真正连接两个自由度。

能量和比热测量也需要配合处理。长程 cluster 更新可以避免逐 pair 生成 bond，但若每次测量仍然重新求

$$
E=-\sum_{i<j}J_{ij}s_is_j,
$$

测量会重新变成 $O(N^2)$。Fukui-Todo 方法中还讨论了如何用采样到的 bond 和辅助量在线性时间估计能量及比热。因此需要把“更新复杂度”和“测量复杂度”分开检查，否则更新已经加速，测量仍可能成为瓶颈。

## Clock 与 Luijten-Blote / Fukui-Todo 的关系

三者可以统一成“从大量小概率事件中抽下一次事件”的问题：

| 方法 | 事件 | 常见目标 |
| --- | --- | --- |
| Luijten-Blote | 下一条候选 cluster bond | 长程 SW/Wolff 的 $O(N\log N)$ 类加速 |
| Fukui-Todo | 下一条真实 SW 等价 bond | 长程 Ising cluster 的 $O(N)$ sweep |
| Clock factorized | 下一次 bound rejection 或候选事件 | 长程 Metropolis / quantum worm 的 $O(1)$ 或低成本局域更新 |

差别在于事件的含义。cluster 算法里的事件是“加 bond”，发生后会扩大 cluster；factorized Metropolis 里的事件是“拒绝”，发生后会终止或否决 proposal。二者都可以用累计概率、树结构、alias table 或 thinning 技巧实现，但 detailed balance 的证明不同，不能只因为形式相似就混用接受率。

## Alias 与累计表

如果相互作用只依赖距离或位移

$$
J_{ij}=J(\mathbf r_i-\mathbf r_j),
$$

可以预先构造候选位移的概率表。比如在 proposal 中按

$$
P(\mathbf r)\propto |J(\mathbf r)|
$$

抽取一个远距离伙伴，再用 Metropolis 因子修正权重：

$$
P_{\rm acc}
=
\min\left[
1,
\frac{W(C')P(C'\to C)}
{W(C)P(C\to C')}
\right].
$$

抽样离散分布时常用两种结构：

- 累计分布表：构造 $F_m=\sum_{j\le m}p_j$，再二分查找。
- Alias table：预处理后 $\mathcal O(1)$ 抽样。

这类方法适合“远距离候选很多，但每次只需要选少数几个”的更新。它不自动解决接受率问题；proposal 设计仍需和权重比配合。

## FFT 与卷积加速

对于具有平移不变性的长程相互作用，能量常写成卷积：

$$
E
=
\frac12
\sum_{ij}
J(\mathbf r_i-\mathbf r_j)
s_i s_j.
$$

定义局域场

$$
h_i=\sum_j J(\mathbf r_i-\mathbf r_j)s_j.
$$

若每次都重新计算 $h_i$，代价为 $\mathcal O(N^2)$。利用 FFT，可以在

$$
\mathcal O(N\log N)
$$

时间内从整个构型计算所有 $h_i$：

$$
h=\mathcal F^{-1}
\left[
\tilde J(\mathbf k)\tilde s(\mathbf k)
\right].
$$

这适合批量计算能量、做全局 proposal 或混合动力学类更新。对于单点 Metropolis，如果每次翻转后都更新全部场，仍然可能不划算。一个折中做法是局域更新中维护场：

$$
h_j\to h_j-2J_{ji}s_i
$$

代价仍为 $\mathcal O(N)$；隔一段时间用 FFT 重新校准场，控制误差。

## 预判定与层级自适应 Metropolis

除了 cluster 型算法，长程系统中也可以保留普通 Metropolis 动力学，只是把“是否需要算完整能量差”这一步加速。

`arXiv:2508.09775v1` 的 predecision scheme 以 lattice long-range Metropolis 为目标。它利用相互作用项的上界或分层估计，先判断一次 proposal 是否已经可以接受或拒绝；只有在预判定不够时，才继续展开更多长程贡献。对幂律势

$$
V(r)=r^{-d-\sigma}
$$

该文给出的复杂度目标是：对 $V(r)=r^{-d-\sigma}$，当 $\sigma<d$ 时从 $\mathcal O(N^2)$ sweep 降到

$$
\mathcal O\!\left(N^{2-\sigma/d}\right),
$$

当 $\sigma>d$ 时降到

$$
\mathcal O(N).
$$

更重要的是，它声称在相同随机数序列下产生与显式求和 Metropolis 完全相同的 Markov chain。因此它不是“随机截断近似”，而是提前判断普通 Metropolis 最终会接受还是拒绝。它适合需要保留局域动力学含义的 nonequilibrium 或动力学研究。

一个简化图像是：Metropolis 接受条件可以写成比较随机阈值和能量差，

$$
u < e^{-\beta\Delta E}.
$$

等价地比较

$$
-\beta^{-1}\ln u
$$

和 $\Delta E$。若长程能量差被分成近邻项、若干远距离壳层项和剩余误差上界，那么只要已经计算出的部分和剩余上界足以确定不等式真假，就可以停止；只有边界情况才继续展开更多项。

`arXiv:2207.14670` 的 fast hierarchical adaptive algorithm 走的是相近路线：把远距离相互作用按空间层级组织起来，对 proposal 的能量差做分层处理，并在需要时逐级细化。它强调生成的构型序列可以和标准长程 Metropolis 完全一致，因此不是近似截断，而是对同一算法的快速实现。

层级自适应方法的基本数据结构可以理解为一棵空间树：

1. 近距离相互作用逐项精确计算。
2. 远距离区域先用一个 cell 或 block 的总贡献上界估计。
3. 若上界已经足够决定接受/拒绝，就不再展开这个 block。
4. 若不够，就把 block 分裂成更小的子块继续细化。

对 $1/r^{d+\sigma}$ 这类单调衰减势，远距离 block 的贡献可以给出严格误差界；对 Lennard-Jones 或符号可变相互作用，上界需要分开处理吸引、排斥或绝对值贡献。该方法报告的平均复杂度为 $O(N\log N)$，优点是一般性强，缺点是实现比简单累计表更复杂。

这两类方法和 alias proposal 的区别是：

- alias / cumulative table 改变的是候选对象怎么抽；
- predecision / hierarchical adaptive 改变的是接受或拒绝时如何避免完整求和；
- 如果声称“和标准 Metropolis 完全等价”，就必须检查随机数使用顺序、上界构造和提前停止规则是否严格对应原接受率。

## 连续空间的 cell-veto 思想

`PhysRevE.94.031302` 的 cell-veto Monte Carlo 主要面向连续空间长程体系。连续空间中每个粒子和所有其他粒子相互作用，单次移动若逐项计算能量差，代价同样很高。cell-veto 的做法是把空间划分成 cell，用 cell 级别的相互作用上界先抽样可能 veto 这次移动的区域；只有真正被选中的 cell 或粒子才需要精细计算。

这种算法和 Luijten-Blote/Clock 的思想很接近：不要逐个访问大量“小概率会影响接受率”的对象，而是直接抽样下一个可能产生 veto 的事件。区别在于连续空间没有固定格点 neighbor list，cell 上界、粒子分布和移动 proposal 的几何关系会成为实现重点。

可以把 cell-veto 写成连续空间版本的 factorized Metropolis。设一次移动 $i:\mathbf r\to\mathbf r'$ 对其他粒子 $j$ 的能量差为

$$
\Delta U_{ij}.
$$

普通 Metropolis 看总和 $\sum_j\Delta U_{ij}$。factorized veto 则把每个粒子或 cell 看成一个可能拒绝本次移动的因子。为避免逐粒子检查，先为每个 cell 构造上界

$$
\hat q_C
\ge
\max_{\mathbf r_j\in C}
\left[
1-\min(1,e^{-\beta\Delta U_{ij}})
\right].
$$

抽到某个 cell 后，再在 cell 内抽粒子并计算真实 veto 概率。若真实 veto 发生，移动拒绝；若没有发生，继续寻找下一个可能 veto 的 cell。这样远处大量粒子的微小拒绝概率被压缩到 cell 级事件。

cell-veto 尤其适合连续空间中相互作用有明确几何上界的情形，例如单调衰减的 pair potential。若势能有硬核、强各向异性或多体项，cell 上界会变得更难构造，效率和正确性都需要重新检查。

## 随机截断和随机势切换

随机截断不能只写成“期望上等于原耦合”。在 Monte Carlo 权重中，正确性要求的是扩展构型空间的平衡分布，而不是只要求

$$
\mathbb E[J_{ij}^{\rm stoch}]=J_{ij}.
$$

因此使用随机截断时，应把被保留/删除的相互作用也看成辅助变量，并写出联合权重。一个安全的检查原则是：

- 切换后的辅助相互作用是否有明确的条件分布；
- 在固定辅助变量时，对自旋或粒子的更新是否满足 detailed balance；
- 更新辅助变量时，边缘化后是否恢复原始 Boltzmann 权重；
- 额外随机性是否显著增加能量估计方差。

若只把 $J_{ij}$ 随机替换成 $0$ 或 $J_{ij}/p_{ij}$，但没有给出联合权重推导，那么它最多是无偏能量估计思路，不能自动保证采样正确。

## 参考算法地图

几类长程算法可以按目标和风险整理为：

| 场景 | 代表思路 | 主要优点 | 主要检查点 |
| --- | --- | --- | --- |
| 长程 Ising / Potts cluster | Luijten-Blote、Fukui-Todo | 跳过大量未占据 bond | 加键概率、累计表、detailed balance |
| 平移不变格点模型 | FFT / 卷积 | 批量计算场或能量快 | 周期边界定义、归一化、aliasing |
| 局域 Metropolis 动力学 | predecision、hierarchical adaptive | 保持标准 Metropolis 链 | 上界严格性、随机数序列、提前停止 |
| 连续空间长程体系 | cell-veto | 避免逐粒子求和 | cell 上界、veto 抽样、移动 proposal |
| 快速试算或短程主导 | 截断 / 随机截断 | 实现简单 | 是否改变普适类和有限尺寸修正 |

## 如何选择

不同算法适合不同问题：

- **只要快速试算**：先用截断，检查是否能复现实验性趋势。
- **研究长程临界指数**：优先使用完整周期定义、Clock/Luijten-Blote 类加速或可控镜像求和。
- **相互作用平移不变**：考虑 FFT 计算场或能量。
- **cluster 更新可用**：用累计概率跳过未占据长程键。
- **局域 Metropolis 为主**：维护局域场，必要时结合 Clock 或 alias proposal。

长程体系的算法选择不能只看复杂度，还要看有限尺寸定义。若算法加速改变了相互作用本身，后续的临界标度分析就会跟着改变。

## 常见检查

- 对小系统直接 $\mathcal O(N^2)$ 算法做 benchmark。
- 检查每个格点的总耦合

$$
J_{\rm tot}(i)=\sum_{j\ne i}J_{ij}
$$

是否与格点位置无关。

- 比较奇偶 $L$ 的周期距离定义，确认没有某些方向被重复或漏算。
- 若使用截断，改变 $R_c$ 并观察物理量是否稳定。
- 若使用累计概率或 alias 表，检查抽样分布是否与目标概率一致。

长程算法的重点在于两件事：一方面减少无效访问，另一方面保持有限系统中每个格点看到的相互作用环境一致。
