# 集团算法

集团算法的目标是一次更新一整块强关联自由度，从而减少临界慢化。它和局域 Metropolis 的目标分布可以完全相同，差别在于 proposal 直接作用在大尺度结构上。

读算法时可以把问题拆成三层：

1. 目标分布是什么，也就是希望采样的 $W(s)$。
2. 候选构型怎么提出，也就是 proposal $A(s\to s')$。
3. 如何接受或拒绝，使最终转移概率 $P(s\to s')$ 保持目标分布。

Metropolis、heat bath、cluster、worm 的差别主要在第二层。第一层通常由模型决定，第三层由 detailed balance 或 global balance 保证。“提出一个新构型”和“保证这个构型有正确权重”是两个不同问题；cluster 算法主要改变 proposal 的尺度，局域 Metropolis 和 heat bath 的内容见 [Metropolis 更新](metropolis.md)。

## 基本图像

cluster 更新的思想是一次翻转一整块强关联自由度。典型例子包括 Swendsen-Wang 和 Wolff 算法。

以 ferromagnetic Ising 模型为例，相同方向的相邻自旋可以按概率

$$
p=1-e^{-2K}
$$

连成 cluster，然后整体翻转。这样可以在临界点附近快速改变大尺度磁畴，显著减小动态临界指数。

cluster 算法的核心是引入几何表象：把原本的自旋构型转化为自旋与 bond 的联合构型，使大尺度关联能够被一次更新处理。

相关文献可以按功能分开理解。Swendsen-Wang 算法最初用于减少临界慢化，核心是把 Potts/Ising 自旋和 FK bond 变量放到同一个扩展构型空间中。Edwards-Sokal 表象随后把这种联合分布写得更系统，使 SW 算法可以直接理解为扩展空间中的条件抽样。Wolff 的 single-cluster 算法则把“找出所有 cluster 再逐个更新”改成“随机选一个种子，只生长并更新一个 cluster”，更适合用平均 cluster 体积定义等效 sweep。Niedermayer 的 general cluster updating 给出了更抽象的二能级构造语言，适合理解 $O(N)$ 这类连续自旋模型中的反射 cluster。

最常见的两个版本是：

- Swendsen-Wang：在整张格子上生成所有 bond，找到全部 cluster，然后每个 cluster 独立决定是否翻转。
- Wolff：随机选一个种子点，只生长一个 cluster，然后整体翻转这个 cluster。

二者的精神相同：低温或临界附近，相邻自旋常常强相关，逐点翻转会不断破坏又重建这些相关结构；cluster 更新则把强相关区域当作一个整体移动。

### Bond 概率的来源：二能级构造

cluster bond 来自局域 Boltzmann 权重的分解。一个标准 cluster 更新通常分成两步：

1. **cluster formation**：根据当前构型放置 bond，得到若干连通 cluster。
2. **spin operation**：对每个 cluster 独立决定是否执行某个自旋操作 $\mathcal M$，常见概率为 $1/2$。

关键在第一步。考虑一个局域相互作用单元，例如一条边 $ij$ 上的能量

$$
\varepsilon_{ij}.
$$

这里先把反温度 $\beta$ 吸收到 $\varepsilon_{ij}$ 里，因此局域 Boltzmann 权重就是

$$
e^{-\varepsilon_{ij}}.
$$

整个配分函数可写为

$$
Z
=
\sum_s
\prod_{ij}
e^{-\varepsilon_{ij}(s)}.
$$

假设对单元中的一个自由度执行操作 $\mathcal M$ 后，该单元只在两个能级之间切换：

$$
\varepsilon_0<\varepsilon_1,
$$

其中 $\varepsilon_0$ 是低能级，$\varepsilon_1$ 是高能级。此时权重可以拆成

$$
e^{-\varepsilon_{ij}}
=
e^{-\varepsilon_0}
\delta_{\varepsilon_{ij},\varepsilon_0}
+
e^{-\varepsilon_1}
\left(
1-\delta_{\varepsilon_{ij},\varepsilon_0}
\right).
$$

把它整理为

$$
e^{-\varepsilon_{ij}}
=
e^{-\varepsilon_0}
\left[
P_b\delta_{\varepsilon_{ij},\varepsilon_0}
+(1-P_b)
\right],
$$

其中

$$
P_b=1-e^{-(\varepsilon_1-\varepsilon_0)}.
$$

这个式子的算法含义是：

- 如果当前单元处于高能级 $\varepsilon_1$，则 $\delta_{\varepsilon_{ij},\varepsilon_0}=0$，只能选择“不放 bond”。
- 如果当前单元处于低能级 $\varepsilon_0$，则有两种选择：以概率 $P_b$ 放置 bond，以概率 $1-P_b$ 不放 bond。
- 一旦放置 bond，被连接的自由度必须在后续 spin operation 中一起执行 $\mathcal M$，这样 cluster 内部的低能关系不会被单独破坏。

算法构造中，更常用下面的等价判断。设当前能量为 $\varepsilon$，只对其中一个自由度执行 $\mathcal M$ 后的能量为

$$
\varepsilon^{\mathcal M}.
$$

若

$$
\varepsilon^{\mathcal M}>\varepsilon,
$$

说明当前单元是二能级中的低能状态，可以放 bond；若 $\varepsilon^{\mathcal M}\leq \varepsilon$，说明当前状态并不需要被绑定。于是 bond 概率可以直接写成

$$
\boxed{
p_{ij}
=
\max\left[
0,\,
1-\exp\left(
-(\varepsilon^{\mathcal M}-\varepsilon)
\right)
\right].
}
$$

这就是“二能级思想”的实用版本：先选定一个操作 $\mathcal M$，再比较操作前后的局域能量。若单独操作会升高能量，就用这部分能量差生成 bond，把这些自由度锁进同一个 cluster。

这种写法的重点不是“先有一个几何团簇再证明它正确”，而是反过来：先把局域权重拆成“可独立操作”和“必须绑定操作”两部分。bond 的概率就是这次局域权重拆分留下的条件概率。因此，只要 cluster formation 和 cluster operation 都按这个扩展权重抽样，整步更新就不需要额外 Metropolis 接受率；若模型中还有外场、各向异性或没有被 $\mathcal M$ 保持的项，则这些剩余项必须另行进入接受率或通过其他更新补偿。

Ising ferromagnet 中这就给出熟悉的

$$
p=1-e^{-2K}.
$$

这一推导也说明，cluster 算法能否直接使用，取决于能否为模型找到合适的低能局域单元和保持权重正确的集体操作。

把 Ising ferromagnet 代进去会更清楚。局域能量为

$$
\varepsilon_{ij}=-Ks_is_j.
$$

若两个自旋同号，能量是 $-K$；若反号，能量是 $+K$。对同号 pair，翻转其中一个自旋会把低能状态变成高能状态，因此

$$
\varepsilon_0=-K,\qquad \varepsilon_1=K.
$$

于是

$$
P_b=1-e^{-(K-(-K))}=1-e^{-2K}.
$$

激活 bond 的作用是声明：“这两个同号自旋在本轮更新中必须一起翻转。”这样翻转整个 cluster 不改变这些内部 bond 的能量，真正需要随机性的地方已经被 bond 生成步骤吸收了。

这套二能级构造是很多连续自旋 cluster 算法的共同底层逻辑。嵌入 Ising 方法、XY 反射 cluster、双层 XY 的 constrained cluster，都可以看成是在连续变量里人为选定一个操作 $\mathcal M$，把局域能量暂时压缩成“当前状态”和“操作后状态”两个能级。

### FK 几何表象

以 Ising/Potts 模型为例，cluster 更新也可以从 Fortuin-Kasteleyn 表象理解。Potts 模型的边权重可写为

$$
e^{K\delta_{\sigma_i,\sigma_j}}
=
1+v\delta_{\sigma_i,\sigma_j},
\qquad
v=e^K-1.
$$

把每条边是否取 $v\delta_{\sigma_i,\sigma_j}$ 记为 bond 变量，求和掉自旋后得到 random-cluster 权重：

$$
Z
=
\sum_{\omega}
v^{b(\omega)}
q^{k(\omega)}.
$$

其中 $b(\omega)$ 是激活 bond 数，$k(\omega)$ 是 cluster 数。若写成概率形式，bond occupation probability 为

$$
p=1-e^{-K}.
$$

FK 表象的价值不只是构造算法。它还把磁化、磁化率、渗流概率等物理量转化成 cluster 几何量，因此和后面的几何观测量紧密相连。

从算法角度看，FK 表象把“自旋是否相同”变成了“是否有 bond 连接”。从物理角度看，它把临界涨落变成了几何连通性：临界点附近，cluster 没有典型大小，大小分布呈现标度形式。正因为这样，wrapping probability、最大 cluster、cluster size distribution 等几何量可以成为判断相变的工具。

### Swendsen-Wang 和 Gibbs 采样

Swendsen-Wang 算法可以理解成在自旋变量和 bond 变量之间交替做条件抽样。设自旋构型为 $\sigma$，bond 构型为 $\omega$。联合分布可以写成

$$
\pi(\sigma,\omega)
\propto
\prod_{\langle ij\rangle}
\left[
(1-p)\delta_{\omega_{ij},0}
+
p\,\delta_{\omega_{ij},1}\delta_{\sigma_i,\sigma_j}
\right].
$$

给定自旋 $\sigma$，bond 的条件分布很简单：

- 若 $\sigma_i\ne\sigma_j$，则 $\omega_{ij}=0$。
- 若 $\sigma_i=\sigma_j$，则以概率 $p=1-e^{-K}$ 令 $\omega_{ij}=1$。

给定 bond $\omega$，每个连通 cluster 内部必须同色，而不同 cluster 之间可以独立选颜色。因此对 $q$-state Potts ferromagnet：

$$
\sigma_C\sim \{1,2,\cdots,q\}
$$

均匀抽取即可。

所以 SW 的两步

$$
\sigma\to\omega\to\sigma'
$$

就是 Edwards-Sokal 联合分布上的两块 Gibbs sampling：在扩展变量 $(\sigma,\omega)$ 的联合分布里，交替从两个条件分布抽样。这个视角很有用，因为它解释了为什么 SW 可以“全接受”：随机性已经被放进条件分布本身，而不是先提出候选再用 Metropolis 接受率修正。

这个说法也限定了 SW 的适用范围。上述联合分布依赖 ferromagnetic Potts 权重的 FK 分解；一旦相互作用带有 frustration、反铁磁约束或外场，bond 条件分布和 cluster 重染色条件分布就不再保持同样简单的形式，不能直接照搬 ferromagnetic SW 的步骤。

Wolff 算法可以看成 SW 的单 cluster 版本。它随机选一个种子，只生长包含该种子的一个 cluster，然后直接翻转或重染色。它不需要每次处理全系统，单步成本常较低；但比较不同算法效率时，要用翻转的平均体积来定义等效 sweep。若一次 Wolff 更新平均翻转 $\langle C\rangle$ 个自旋，则常用

$$
N_{\rm Wolff\ updates}\simeq \frac{N}{\langle C\rangle}
$$

次单 cluster 更新作为一个等效 sweep 的尺度。

### Detailed balance 的看法

SW 的 detailed balance 可以从扩展联合分布看得很清楚。设

$$
\pi(\sigma,\omega)
$$

是自旋与 bond 的联合权重。SW 先从

$$
\pi(\omega|\sigma)
$$

抽 bond，再从

$$
\pi(\sigma'|\omega)
$$

抽新自旋。因此自旋空间中的转移概率为

$$
P(\sigma\to\sigma')
=
\sum_\omega
\pi(\omega|\sigma)\pi(\sigma'|\omega).
$$

因为这正是对联合分布做 Gibbs 更新，边缘分布

$$
\pi(\sigma)=\sum_\omega\pi(\sigma,\omega)
$$

自动保持不变。若进一步检查概率流，也可以证明

$$
\pi(\sigma)P(\sigma\to\sigma')
=
\pi(\sigma')P(\sigma'\to\sigma).
$$

这说明 cluster 算法并没有绕开平衡条件。它只是把难以直接提出的大尺度自旋更新，改写成了扩展空间中的简单条件抽样。

### Potts 模型和反铁磁注意事项

ferromagnetic Potts 模型是 SW 最自然的应用场景。哈密顿量写成

$$
H=-K\sum_{\langle ij\rangle}\delta_{\sigma_i,\sigma_j},
\qquad
K>0.
$$

相同颜色的近邻边可以放 bond，bond 概率为

$$
p=1-e^{-K}.
$$

每个 cluster 重染成 $q$ 种颜色之一。这一步对 $q=2$ 退化为 Ising 的 cluster 翻转。

反铁磁 Potts 情形要谨慎得多。若

$$
K<0,
$$

低能关系偏好

$$
\sigma_i\ne\sigma_j.
$$

这时“相同颜色放 bond 并整体重染色”的 FK ferromagnetic 构造不再直接适用。原因是 cluster 内部的约束不再是“所有点同色”，而是带有 proper coloring 或 frustrated constraint 的几何问题。简单照搬 ferromagnetic SW 可能破坏 detailed balance，或者得到不可遍历的更新。

Wang、Swendsen 和 Kotecky 对反铁磁 Potts 模型的模拟已经说明，反铁磁情形需要新的 Monte Carlo 构造，而不是把 ferromagnetic SW 中的“同色加键、cluster 重染色”机械改符号。实际处理反铁磁 Potts 时，常见选择包括：

- 使用局域 Metropolis/heat bath 作为基线。
- 针对二分格子或特殊 $q$ 设计保持 coloring 约束的 cluster move。
- 在 random-cluster 或 loop 表象中寻找新的扩展变量。
- 用 parallel tempering、worm/loop 或问题专用 rejection-free 更新改善混合。

所以“Potts 可以用 cluster 算法”这句话默认说的是 ferromagnetic FK/SW 框架。反铁磁情形需要重新检查局域权重分解、可达性和 detailed balance；若只是为了获得可靠基线，局域 heat bath、Metropolis 或 tempering 往往比错误套用 FK cluster 更安全。

### 构造与存储

实现 cluster 更新通常有两种路径。

第一种是边生成时同步生长 cluster。Wolff 算法常用队列做 BFS：从一个种子点出发，检查邻居，按 bond 概率加入队列，并在生长结束后整体翻转。这个方法容易在生长过程中记录位移、边界穿越和回转半径。

第二种是先生成所有激活 bond，再用并查集或图搜索标记 cluster。Swendsen-Wang 算法常用这种方式，因为它需要给每个 cluster 独立决定新自旋状态。并查集非常适合快速合并连通分量，但若要测 wrapping、winding 或回转半径，通常还要额外保存相对位移或 bond 的方向信息。

对最近邻格子，bond 可以用固定方向数组存储；对长程模型或任意图，bond 更适合存为边列表：

$$
(i,j,\Delta\mathbf r_{ij},p_{ij}).
$$

这里 $\Delta\mathbf r_{ij}$ 对周期边界下的几何测量尤其重要。

一个完整的 Swendsen-Wang sweep 可以写成：

1. 清空上一轮的 bond。
2. 遍历所有允许相互作用的边 $ij$。
3. 若当前自旋满足加键条件，则按 $p_{ij}$ 激活 bond。
4. 对激活 bond 做连通分量分解。
5. 对每个 cluster 独立抽取新取向或决定是否翻转。
6. 在需要时同步测量 cluster 大小、wrapping、回转半径等几何量。

Wolff 更新则只生长一个 cluster。它的单次更新成本较低，但一次 sweep 如何定义要小心，常用约定是累计翻转的自旋数达到 $O(N)$ 后算一个 sweep。

### 连续对称最近邻自旋模型的算法组织

以 $O(N)$ 最近邻自旋模型为例，模型可写为

$$
\mathcal H
=
-\sum_{\langle ij\rangle}\mathbf S_i\cdot\mathbf S_j
-h\sum_i S_i^{(0)},
\qquad
|\mathbf S_i|=1.
$$

这里 $\mathbf S_i$ 是 $N$ 分量单位向量。$N=1$ 时退化为 Ising，自旋取 $\pm1$；$N=2$ 是 XY；$N=3$ 是 Heisenberg。算法实现通常需要维护以下信息：

| 信息 | 含义 |
| --- | --- |
| 自旋场 $\mathbf S_i$ | 第 $i$ 个格点上的 $N$ 分量单位向量 |
| 近邻映射 | 周期边界下每个格点在各方向的相邻格点 |
| 总格点数 $L^d$ | 系统体积和 sweep 归一化尺度 |
| 近邻方向数 $2d$ | cluster 生长时的候选 bond 数 |
| 生长队列 | BFS 或 DFS 生成 cluster 时保存待处理格点 |
| 访问标记 | 记录格点是否已经进入当前 cluster |

#### 格点和周期边界

常见实现会把 $d$ 维坐标压成一个整数站点编号：

$$
i=0,1,\cdots,L^d-1.
$$

需要坐标时再用除法和取模恢复各方向分量。找近邻时，对某一方向坐标加一或减一，并在越界时用周期边界拉回：

$$
x_\mu\to (x_\mu\pm1)\bmod L.
$$

这样局域更新、能量测量、cluster 生长都只需要调用同一个近邻函数，避免在算法内部到处手写边界判断。

#### 随机单位向量

对一般 $O(N)$ 模型，随机自旋可以通过高斯向量归一化生成：

1. 生成 $N$ 个独立高斯随机数 $g_a$。
2. 计算长度 $r=(\sum_a g_a^2)^{1/2}$。
3. 令

$$
S_a=\frac{g_a}{r}.
$$

这会在 $N$ 维单位球面上给出均匀方向。对 $N=2$ 或 $N=3$，也可以用角度参数化；但高斯归一化写法统一，适合任意 $N$。

#### 与局域更新的配合

局域 Metropolis 和 heat bath 的细节放在 [Metropolis 更新](metropolis.md) 中。cluster sweep 中仍常混入局域更新，主要有三个用途。

第一，作为正确性基线。先用局域更新测小系统，与精确枚举或已知结果比较，再打开 cluster 更新。

第二，补充遍历性。某些 constrained cluster 只改变构型空间中的一部分方向，需要混入局域 move 或全局旋转。

第三，处理外场、各向异性或复杂相互作用。若某些项不被 cluster 操作保持，可以对整块 cluster 加一个 Metropolis 接受率，或者在若干 cluster sweep 后用局域更新重新平衡这些项。

#### Wolff 的嵌入 Ising 更新

对连续 $O(N)$ 自旋，cluster 更新常用 **embedded Ising** 思想：先随机选一个单位向量 $\mathbf r$，然后只看每个自旋在 $\mathbf r$ 方向上的投影

$$
\sigma_i=\mathbf r\cdot\mathbf S_i.
$$

沿 $\mathbf r$ 的反射操作为

$$
\mathbf S_i
\to
\mathbf S_i'
=
\mathbf S_i-2(\mathbf S_i\cdot\mathbf r)\mathbf r.
$$

这相当于翻转投影 $\sigma_i\to-\sigma_i$，但保持垂直于 $\mathbf r$ 的分量不变。对一条近邻边 $ij$，cluster bond 概率为

$$
p_{ij}
=
\max\left[
0,\,
1-\exp\left(
-2\beta
(\mathbf r\cdot\mathbf S_i)
(\mathbf r\cdot\mathbf S_j)
\right)
\right].
$$

只有两个投影同号时，乘积为正，才可能加 bond；投影异号时 $p_{ij}=0$。Wolff 的一次更新流程是：

1. 清空 `Mem` 和 `Que`。
2. 随机生成反射轴 $\mathbf r$。
3. 随机选择种子站点。
4. 用 BFS 检查近邻，按 $p_{ij}$ 把新站点加入队列。
5. cluster 生长结束后，对队列中的所有站点做反射。

若没有外场，整个 cluster 反射可以直接接受。若有外场，外场项不再在反射下保持不变，需要额外计算 cluster 反射前后的外场能量

$$
E_h^{\rm before}
=
-h\sum_{i\in C}S_i^{(0)},
\qquad
E_h^{\rm after}
=
-h\sum_{i\in C}S_i'^{(0)}.
$$

再用 Metropolis 因子

$$
\min\left(1,e^{-\beta(E_h^{\rm after}-E_h^{\rm before})}\right)
$$

接受整块反射。实际实现中也可以用权重比写成

$$
\frac{e^{-\beta E_h^{\rm after}}}{e^{-\beta E_h^{\rm before}}}.
$$

Wolff 单团簇算法见 `PhysRevLett.62.361`。它的思想可以从这里理解：不要先把全系统分成所有团簇，再逐个决定是否翻转；而是直接从一个随机种子生长一个会被翻转的团簇。对临界系统而言，一次更新的空间尺度会自动跟随相关长度，因而比单点 Metropolis 更容易缓解临界慢化。`PhysRevLett.61.2026` 对应 Niedermayer 的 general cluster updating，更适合作为二能级/广义 cluster 构造的参考。

#### Swendsen-Wang 的 BFS 版本

Swendsen-Wang 也可以用同样的反射轴 $\mathbf r$。它会遍历整张格子，把所有 cluster 都找出来。

一个 BFS 版本的流程是：

1. 清空 `Mem`。
2. 随机生成反射轴 $\mathbf r$。
3. 从第一个未访问站点开始，BFS 生长一个 cluster。
4. 对每条近邻边，用同样的 $p_{ij}$ 决定是否连接。
5. 一个 cluster 生长结束后，测量它的大小 $C$。
6. 无外场时，以概率 $1/2$ 反射整个 cluster。
7. 有外场时，根据反射前后外场权重抽样是否反射。
8. 继续寻找下一个未访问站点，直到全系统访问完。

这种实现不必显式存储所有 bond，而是在 BFS 时“边检查、边生长”。优点是内存少，写法直接；缺点是如果之后要测 wrapping、winding 或回转半径，需要在 BFS 中同步保存展开坐标和跨边界位移。

#### 同步测量 cluster 量

Swendsen-Wang 找出所有 cluster 时，可以顺手测几何量。若当前 cluster 大小为 $C$，则累加

$$
S_2\leftarrow S_2+C^2,
\qquad
S_4\leftarrow S_4+C^4.
$$

同时维护最大和次大 cluster：

$$
C_1=\max C,
\qquad
C_2=\text{second max } C.
$$

这类量常用于 FK 几何分析。测量时通常先记录未归一化的 $S_2,S_4,C_1,C_2$，输出时再除以适当体积因子。例如 $C_1$ 常输出为 $C_1/L^d$，而 $S_2$ 可输出为 $S_2/L^{2d}$ 或根据具体定义调整。

#### 普通物理量的测量

一次测量通常包括：

- 能量：遍历每个站点和一半方向的近邻，避免 bond 双计数；
- 磁化：先求总矢量 $\mathbf M=\sum_i\mathbf S_i$，再取 $|\mathbf M|$、$M^2$、$M^4$；
- 结构因子：预先保存 $k_{\min}$ 下每个站点的 $\cos(\mathbf k\cdot\mathbf r_i)$ 和 $\sin(\mathbf k\cdot\mathbf r_i)$，测量时累加 Fourier 分量；
- 二阶矩相关长度比：用 $M^2$ 和 $M_k^2$ 组合成 $\xi_L/L$；
- cluster 量：使用上面 BFS 得到的 $N_c,S_2,S_4,C_1,C_2$。

这种组织方式有一个实际优点：更新算法只负责产生新构型，测量函数统一从当前构型计算物理量。这样更容易检查错误，也方便在 Metropolis、Wolff、Swendsen-Wang 之间切换。

### 双层 XY 模型中的二能级 cluster

双层 XY 模型给出了一个很好的例子：自由度是连续角变量，但 cluster 算法仍然可以通过二能级思想构造出来。

设每个格点 $i$ 有两层角变量

$$
\theta_{i,a},\qquad \theta_{i,b}.
$$

普通 XY 最近邻项通常形如

$$
-J\cos(\theta_{i,\ell}-\theta_{j,\ell}),
\qquad
\ell=a,b.
$$

层间二体耦合可写成

$$
-K\cos(\theta_{i,a}-\theta_{i,b}).
$$

配对相位梯度耦合则常见为

$$
-K\cos(
\theta_{i,a}+\theta_{i,b}
-
\theta_{j,a}-\theta_{j,b}
).
$$

这些能量本来是连续的。要使用 cluster 算法，需要先选定一个操作 $\mathcal M$，只比较“操作前”和“操作后”两种局域能量。这样连续能量被临时压缩成两个能级，然后按

$$
p=\max\left[
0,\,
1-\exp\left(
-(\varepsilon^{\mathcal M}-\varepsilon)
\right)
\right]
$$

放置 bond。

#### 二体层间耦合

对 ferromagnetic 层间耦合

$$
\varepsilon
=
-K\cos(\theta_{i,a}-\theta_{i,b}),
$$

可以选择反射操作

$$
\mathcal M:\theta\to-\theta.
$$

若只反射其中一个角变量，例如 $\theta_{i,b}\to-\theta_{i,b}$，操作后的能量为

$$
\varepsilon^{\mathcal M}
=
-K\cos(\theta_{i,a}+\theta_{i,b}).
$$

因此

$$
\varepsilon^{\mathcal M}-\varepsilon
=
-K\cos(\theta_{i,a}+\theta_{i,b})
+K\cos(\theta_{i,a}-\theta_{i,b}).
$$

利用恒等式

$$
\cos(x-y)-\cos(x+y)=2\sin x\sin y,
$$

得到

$$
\varepsilon^{\mathcal M}-\varepsilon
=
2K\sin\theta_{i,a}\sin\theta_{i,b}.
$$

所以层间 bond 概率为

$$
\boxed{
p_{i,ab}
=
\max\left[
0,\,
1-\exp\left(
-2K\sin\theta_{i,a}\sin\theta_{i,b}
\right)
\right].
}
$$

同一层内的最近邻 XY 项也可以用相同反射思想处理，只需要把 $K$ 换成 $J$，并把两角变量换成 $\theta_{i,\ell},\theta_{j,\ell}$。

由于这里固定选了反射轴 $\theta\to-\theta$，单靠这个操作不能遍历整个连续 $U(1)$ 空间。常用补救是每轮 cluster 更新后，对所有角变量做同一个随机全局旋转：

$$
\theta_{i,\ell}\to\theta_{i,\ell}+\varphi,
\qquad
\varphi\sim{\rm Uniform}(0,2\pi).
$$

这样反射 cluster 负责处理强关联结构，全局旋转补充连续角度方向的遍历性。

#### 配对相位梯度耦合

配对相位梯度项同时涉及四个角变量：

$$
\theta_{i,a},\theta_{i,b},\theta_{j,a},\theta_{j,b}.
$$

因此二能级构造有更多选择。核心目标仍然相同：固定一部分自由度或约束某个组合量，让操作前后只需要比较两个能级。

**方法 I：固定一层，只更新另一层。**

以固定 $a$ 层、更新 $b$ 层为例，对 $b$ 层执行

$$
\mathcal M^I:\theta_{j,b}\to\theta_{j,b}+\pi.
$$

只看会随这个操作改变的 $b$ 层最近邻项和配对梯度项，可取

$$
\varepsilon_0
=
-J\cos(\theta_{i,b}-\theta_{j,b})
-K\cos(
\theta_{i,a}+\theta_{i,b}
-
\theta_{j,a}-\theta_{j,b}
).
$$

操作后

$$
\varepsilon_1=-\varepsilon_0.
$$

因此

$$
\varepsilon_1-\varepsilon_0=-2\varepsilon_0,
$$

bond 概率为

$$
\boxed{
p_b^I
=
\max\left[
0,\,
1-\exp(2\varepsilon_0)
\right].
}
$$

生成 cluster 后，对每个 cluster 以概率 $1/2$ 执行 $\theta\to\theta+\pi$。

**方法 II：保持两层相对相位不变。**

要求

$$
\theta_{i,a}-\theta_{i,b}
$$

在操作中保持不变，可以让两层同时反射：

$$
\mathcal M^{II}:
\{\theta_{j,a},\theta_{j,b}\}
\to
\{-\theta_{j,a},-\theta_{j,b}\}.
$$

操作前能量单元为

$$
\begin{aligned}
\varepsilon_0
=&
-J\cos(\theta_{i,a}-\theta_{j,a})
-J\cos(\theta_{i,b}-\theta_{j,b})\\
&
-K\cos(
\theta_{i,a}+\theta_{i,b}
-
\theta_{j,a}-\theta_{j,b}
).
\end{aligned}
$$

操作后为

$$
\begin{aligned}
\varepsilon_1
=&
-J\cos(\theta_{i,a}+\theta_{j,a})
-J\cos(\theta_{i,b}+\theta_{j,b})\\
&
-K\cos(
\theta_{i,a}+\theta_{i,b}
+
\theta_{j,a}+\theta_{j,b}
).
\end{aligned}
$$

bond 概率为

$$
\boxed{
p_b^{II}
=
\max\left[
0,\,
1-\exp\left(
-(\varepsilon_1-\varepsilon_0)
\right)
\right].
}
$$

**方法 III：保持两层总相位不变。**

也可以让两层反向移动，使

$$
\theta_{i,a}+\theta_{i,b}
$$

保持不变。一个简单操作是

$$
\mathcal M^{III}:
\{\theta_{j,a},\theta_{j,b}\}
\to
\{\theta_{j,a}+\pi,\theta_{j,b}-\pi\}.
$$

此时配对相位梯度项在能量差中抵消，只剩两层内部最近邻项：

$$
\varepsilon_0
=
-J\cos(\theta_{i,a}-\theta_{j,a})
-J\cos(\theta_{i,b}-\theta_{j,b}).
$$

操作后同样满足

$$
\varepsilon_1=-\varepsilon_0,
$$

所以

$$
\boxed{
p_b^{III}
=
\max\left[
0,\,
1-\exp(2\varepsilon_0)
\right].
}
$$

这三种方法的差别可以概括为：

| 方法 | 保持不变的对象 | cluster 操作 | bond 概率 |
| --- | --- | --- | --- |
| I | 其中一层的角变量 | 另一层 $\theta\to\theta+\pi$ | $p_b^I=\max[0,1-e^{2\varepsilon_0}]$ |
| II | 相对相位 $\theta_a-\theta_b$ | 两层同时反射 | $p_b^{II}=\max[0,1-e^{-(\varepsilon_1-\varepsilon_0)}]$ |
| III | 总相位 $\theta_a+\theta_b$ | 两层反向平移 $\pi$ | $p_b^{III}=\max[0,1-e^{2\varepsilon_0}]$ |

这里要特别注意遍历性。二体层间耦合的 constrained reflection 可以通过随机全局旋转补充连续角度方向；配对梯度模型的约束更强，随机全局旋转通常不够，需要混入局域 Metropolis 或其他更新。一个稳妥的 sweep 可以写成：

```text
repeat:
    run one or several cluster updates
    run local Metropolis sweeps
    optionally perform global rotation if symmetry allows
    measure observables
```

这类双层 XY cluster 的价值在于，它把复杂多通道相互作用重新组织成局域二能级问题。只要能为某个局域能量单元找到合适的操作 $\mathcal M$，cluster formation 就仍然可以按同一个权重分解来写。

## Loop 更新

loop 更新常见于量子 Monte Carlo 和几何表象中。它把构型分解成闭合 loop，然后翻转或重连整条 loop。与 cluster 类似，loop 更新也是非局域更新，但更适合世界线、顶点模型、量子自旋模型等具有约束结构的问题。

loop 更新的优点是能保持局域约束，同时改变长距离结构。难点是需要为具体模型设计合适的图形规则。

## Worm 更新

worm 算法通过临时引入两个缺陷，把原本只在配分函数空间 $\mathcal Z$ 中的闭合构型，扩展到

$$
\mathcal Z_w=\mathcal Z+\omega_G\mathcal G.
$$

在格林函数空间 $\mathcal G$ 中，两个 worm head 可以移动、产生或删除 kink，从而高效改变世界线拓扑。回到 $\mathcal Z$ 空间后得到新的物理构型。

worm 算法特别适合测量格林函数、处理粒子数涨落、更新世界线构型和降低拓扑障碍。

更完整的 Ising loop representation、普通 worm、irregular / lifted worm 和 loop-cluster 关系，见 [蠕虫算法](loop_cluster.md)。

## Lifted 思想

lifted 或 event-chain 类算法通过扩展状态空间，引入额外方向、动量或事件变量，让 Markov chain 更少做随机回头路。它通常不满足传统 detailed balance，而满足更一般的 global balance。

普通随机游走会频繁来回抖动；lifted 更新则让构型在某个方向上持续移动，直到触发事件再改变方向。这类方法在连续变量系统、硬球模型和一些自旋模型中能显著降低自关联。

## 选择算法的标准

实际选择更新算法时，可以按下面顺序判断：

- 如果只是验证模型或建立基准，先用 Metropolis。
- 如果局域条件分布容易抽样，可以尝试 heat bath。
- 如果临界慢化严重，优先考虑 cluster 或 loop。
- 如果构型是世界线或需要测格林函数，考虑 worm。
- 如果拒绝率高或随机游走慢，可以研究 lifted 或 rejection-free 方法。

无论算法多复杂，最终都要回到同一件事：目标分布是否正确，自关联时间是否足够短。
