# 相变理论概览

相变理论把微观模型、有效自由能、长距离涨落和 Monte Carlo 观测量连接起来。RG、有限尺寸标度、Mermin-Wagner 定理和 BKT 相变分别描述这条链条中的不同尺度和不同机制。

统计物理研究相变时，常常在三个层次之间来回切换：

1. 微观配分函数。
2. 有效自由能或有效作用量。
3. 宏观序参量、关联函数和响应函数。

Monte Carlo 直接在微观构型空间中采样；相变理论则试图把采样结果压缩成少数长距离自由度的语言。

一条基本主线是：

$$
\text{模型}
\rightarrow
\text{对称性与序参量}
\rightarrow
\text{有效场论}
\rightarrow
\text{RG 与有限尺寸标度}
\rightarrow
\text{Monte Carlo 观测量}.
$$

这里每一步都在丢掉一部分细节，同时保留长距离最重要的信息。例如 Ising 模型的微观变量是 $s_i=\pm1$，但在临界点附近，我们常用连续场 $\phi(x)$ 来描述粗粒化磁化。这个替换不是说自旋真的变成了连续变量，而是说大尺度涨落可以用连续场更方便地组织。

## 热力学极限与奇异性

严格意义上的平衡相变定义在热力学极限中：

$$
N\to\infty,
\qquad
L\to\infty,
\qquad
\rho=\frac{N}{L^d}\ {\rm fixed}.
$$

有限系统的配分函数通常是控制参数的解析函数，所以自由能也不会真正出现非解析奇点。Monte Carlo 在有限 $L$ 上看到的是圆滑峰、交点漂移、有限尺寸 rounded transition；真正的相变来自 $L\to\infty$ 后这些结构变尖、变陡，最终形成奇异性。

这件事可以从三个层次理解。

第一，在配分函数层次，有限系统的零点通常位于复温度或复外场平面。随着系统尺寸增大，这些零点可能向实轴逼近。Lee-Yang 零点和 Fisher 零点的思想正是用零点分布刻画热力学极限中的相变。有限系统本身通常仍是解析的；非解析性来自热力学极限中零点累积并夹住实参数轴。

第二，在自由能层次，奇异性表现为自由能密度

$$
f=-\frac{1}{\beta V}\ln Z
$$

在某个控制参数处不解析。若一阶导数不连续，通常称为一级相变；若一阶导数连续而二阶导数发散或不连续，常称为连续相变或二级相变。更高阶分类可以按自由能第几阶导数首次出现奇异来组织，不过现代临界现象更常用序参量、关联长度、临界指数和 RG 固定点来分类。

第三，在观测量层次，奇异性表现为响应函数发散或出现不连续。例如比热、磁化率、关联长度可以写成自由能导数或关联函数积分：

$$
C\sim \frac{\partial^2 f}{\partial T^2},
\qquad
\chi\sim \frac{\partial^2 f}{\partial h^2}.
$$

普通二级相变中，关联长度发散，长距离涨落控制标度行为。BKT 相变更特殊：相关长度以 essential singularity 发散，低温侧呈准长程序，传统 Landau 序参量图像不足以完整描述它。

## 三个层次

最底层是配分函数：

$$
Z=\sum_{\{x\}}e^{-\beta H(x)}.
$$

它包含所有微观构型的统计权重。给定 $Z$ 后，可以定义自由能：

$$
F=-\frac1\beta\ln Z.
$$

自由能是热力学信息的生成函数。比如磁化率、比热、压缩率等响应量，都可以看作自由能对外场或控制参数的导数。

再往上，是序参量和关联函数。序参量用来区分不同宏观相，例如：

- Ising 磁化强度 $m$。
- $O(N)$ 模型中的向量磁化。
- 超流中的相位刚度或 winding number。
- 渗流中的 spanning cluster 或 wrapping probability。

可以把这三层理解为：

$$
\text{微观构型}
\longrightarrow
\text{自由能}
\longrightarrow
\text{序参量与响应函数}.
$$

RG 的作用就是解释：为什么许多微观细节在长距离下会消失，只剩下维度、对称性、相互作用范围和序参量结构这些少数信息。

对 Monte Carlo 来说，这三层还有一个实用含义。程序直接生成的是微观构型；数据文件里保存的是能量、磁化、cluster 大小、绕数等观测量；最后论文或笔记里讨论的往往是临界指数、普适类和标度函数。若不清楚自己正在哪一层说话，就很容易把“显微模型的特殊定义”和“长距离普适结论”混在一起。

## Landau 范式

Landau 理论的核心思想是用序参量和对称性破缺描述相变。设系统的微观哈密顿量具有对称群 $G$。高温无序相通常保持 $G$；低温有序相可能只保持子群 $H$，于是发生

$$
G\to H
$$

的自发对称性破缺。

以铁磁体为例，序参量是磁化

$$
\mathbf m=\langle \mathbf S\rangle.
$$

高温时

$$
\mathbf m=0.
$$

低温时

$$
\mathbf m\ne0,
$$

系统选择一个方向，旋转对称性被破缺。

Landau 自由能把这种图像写成序参量的解析展开。例如 Ising 型相变：

$$
F(m)=F_0+\frac{t}{2}m^2+\frac{u}{4}m^4-hm+\cdots.
$$

其中 $t$ 控制距离临界点的远近，$u>0$ 保证稳定性，$h$ 是外场。若 $t<0$，自由能的极小值从 $m=0$ 分裂到

$$
m=\pm\sqrt{-t/u}.
$$

这就是最简单的对称性破缺图像。

Landau 图像最容易懂，也最容易被误用。它适合描述“某个局域序参量从零变成非零”的相变，例如 Ising 铁磁相变。但它默认自由能可以按序参量解析展开，也默认相变主要由序参量幅度控制。BKT 相变、拓扑序、某些约束模型或强涨落低维系统，都可能超出这个简单范式。因此后面的 Mermin-Wagner 和 BKT 章节不是 Landau 理论的小修小补，而是在说明 Landau 图像的边界。

## 从 Landau 到 LGW

Landau 理论只考虑均匀序参量。真实系统中，序参量可以随空间变化，因此需要 Landau-Ginzburg-Wilson 泛函：

$$
\mathcal F[\phi]
=
\int d^dx
\left[
\frac12(\nabla\phi)^2
+\frac{t}{2}\phi^2
+\frac{u}{4!}\phi^4
-h\phi
+\cdots
\right].
$$

这里梯度项描述空间涨落；$\phi^2$ 项描述 Gaussian 质量；$\phi^4$ 项是最低阶非线性相互作用。更高阶项通常可以写下，但在临界点附近常常是 RG irrelevant 的。

对 $O(N)$ 模型，场变成 $N$ 分量向量：

$$
\boldsymbol\phi=(\phi_1,\cdots,\phi_N),
$$

LGW 泛函为

$$
\mathcal F[\boldsymbol\phi]
=
\int d^dx
\left[
\frac12(\nabla\boldsymbol\phi)^2
+\frac{t}{2}\boldsymbol\phi^2
+\frac{u}{4!}(\boldsymbol\phi^2)^2
\right].
$$

这就是 Ising、XY、Heisenberg 等连续或离散自旋模型最常用的有效场论入口。

这里的 $\phi(x)$ 可以理解为一个粗粒化变量。它不是单个格点上的自旋，而是某个小区域内序参量的平均。梯度项惩罚相邻区域的序参量变化，因此控制空间关联；质量项 $t\phi^2$ 控制系统离临界点有多远；相互作用项 $\phi^4$ 控制涨落之间的非线性耦合。RG 做的事情，就是不断改变粗粒化尺度，观察这些项的相对重要性如何变化。

## LGW 的边界

LGW 理论是一套强大的唯象框架。它从序参量、对称性和局域有效作用量出发，解释了大量普通连续相变。但它不直接包含显微模型的所有信息，也不会自动捕捉所有相结构。

最典型的边界有三类。

第一，低维连续对称性强涨落。二维短程 XY 模型没有普通 Landau 意义下的有限温长程序，却有 BKT 相变。这里关键变量不是序参量幅度从零变成非零，而是涡旋-反涡旋的束缚与解束缚，以及低温侧的准长程序。

第二，拓扑缺陷和几何 sector。percolation、FK cluster、loop model、vortex gas 等体系中，很多关键观测量是几何连通性或拓扑缺陷，而不是单个局域序参量的均匀期望值。

第三，量子多体中的拓扑序和广义对称性。普通 Landau 范式按全局对称性破缺分类相；拓扑序、SPT 相、规范结构和任意子激发提示还存在不由局域序参量完全刻画的相。最近关于 generalized Landau paradigm 的讨论尝试把这些现象组织为广义对称性及其破缺、generalized gauging 和 topological holography / symmetry TFT 语言下的相结构。这部分目前更适合作为扩展视角：它提醒 LGW 是基础入口，但不是相变理论的终点。

### 广义 Landau 范式的视角

`arXiv:2511.19793` 的核心动机可以概括为：普通 Landau 范式把相分类为“普通全局对称性是否破缺”，但许多量子相的区分并不来自一个局域序参量的期望值。更高层的组织方式，是把拓扑序、SPT 相、规范约束和某些非传统临界点理解为广义对称性、广义 gauging 以及 topological holography / symmetry TFT 结构中的相与相变。

这并不是说 LGW 理论被废弃了。更准确的说法是：

- 如果问题有清楚的局域序参量、普通全局对称性和短程相互作用，LGW/RG 仍然是最有效的入口。
- 如果两个相没有传统对称性破缺差别，却有不同的拓扑简并、任意子内容、边界态或约束 sector，就需要比局域序参量更丰富的结构。
- 在 Monte Carlo 中，这类问题常表现为：必须测量非局域量、缠绕数、拓扑 sector、弦序参量、Wilson loop、entanglement 相关量，或者需要在扩展构型空间中保持某种约束。

广义 Landau 范式目前更像一个组织框架：它提示哪些超出局域序参量的结构也应被视为“对称性及其破缺”的广义形式，但具体模型中的可测量判据仍要回到关联函数、缺陷、边界响应、拓扑简并或规范约束。因此，这里把“广义 Landau 范式”放在相变概览中，只作为判断边界的提醒：不要把所有相变都先验地塞进一个局域 $\phi^4$ 泛函。

## 为什么常保留到四次项

在 Gaussian 固定点附近，先由梯度项确定场的工程量纲：

$$
[\phi]=\frac{d-2}{2}.
$$

若相互作用为

$$
g_p\int d^dx\,\phi^p,
$$

则 coupling 的 RG 量纲为

$$
y_p=d-p\frac{d-2}{2}.
$$

令 $y_p=0$ 得到对应的上临界维度：

$$
d_c(p)=\frac{2p}{p-2}.
$$

对 Ising/$O(N)$ 的 $\phi^4$ 理论，

$$
d_c=4.
$$

当 $d>4$ 时，$\phi^4$ 相互作用在长距离下变得 irrelevant，平均场指数成立；当 $d<4$ 时，涨落会把体系带向相互作用固定点。

若模型没有 $\phi\to-\phi$ 对称性，三次项可能允许：

$$
g_3\phi^3.
$$

这时

$$
d_c(3)=6.
$$

这正是渗流、某些 Potts/cluster 场论和 $\phi^3$ 理论中上临界维度为 $6$ 的量纲来源。

## 常见经典自旋模型

最近邻 $O(N)$ 模型可写为

$$
H=-J\sum_{\langle ij\rangle}
\mathbf S_i\cdot\mathbf S_j,
\qquad
|\mathbf S_i|=1.
$$

典型特例包括：

| $N$ | 模型 | 对称性 | 二维有限温行为 |
| --- | --- | --- | --- |
| 1 | Ising | $\mathbb Z_2$ | 有普通二阶相变 |
| 2 | XY | $U(1)$ | 有 BKT 相变 |
| 3 | Heisenberg | $O(3)$ | 无有限温连续对称性破缺 |

二维中，连续对称性的长程序受 Mermin-Wagner 定理限制；离散对称性的 Ising 模型不受这个限制。

$q$-state Potts 模型为

$$
H=-J\sum_{\langle ij\rangle}
\delta_{\sigma_i,\sigma_j},
\qquad
\sigma_i=1,\cdots,q.
$$

它具有 $S_q$ 置换对称性。$q=2$ 时等价于 Ising；通过 Fortuin-Kasteleyn 表示，$q\to1$ 给出普通渗流。

## Potts、FK 与 percolation

Potts 模型和 percolation 的共同母体是 FK/random-cluster 表示。其权重可以写成

$$
W(\omega)
\propto
p^{o(\omega)}
(1-p)^{c(\omega)}
q^{k(\omega)}.
$$

其中 $o(\omega)$ 是开边数，$c(\omega)$ 是闭边数，$k(\omega)$ 是 cluster 数。参数 $q$ 不只表示颜色数，也可以看成每个 cluster 的 fugacity。

因此：

$$
\text{FK/random-cluster}
\supset
\begin{cases}
q=2 & \text{Ising},\\
q\to1 & \text{percolation},\\
q\to0 & \text{spanning tree/forest 极限}.
\end{cases}
$$

需要区分 spin sector 和 cluster sector。同一个 Potts 微观模型，可以从自旋序参量的角度研究，也可以从 FK cluster 几何量的角度研究。二者在某些情况下有不同的连续场论和不同的几何指数。

这句话很重要。自旋相关函数问的是“两个点的颜色或方向是否相关”；cluster 相关函数问的是“两个点是否属于同一个几何连通块”。在 FK 表象中它们常常紧密相连，但并不意味着所有几何指数都能从普通自旋场论里直接读出。数值模拟中如果测的是最大 cluster、wrapping probability 或 cluster 半径分布，就应该明确自己正在看 cluster sector。

### 为什么 O(n) 常对应四次场论

这里讨论为什么 $O(n)$ 模型常对应 $\phi^4$ 理论。

连续场论里常见的 $O(n)$ 模型写成一个 $n$ 分量实场

$$
\boldsymbol\phi(x)
=
(\phi_1,\cdots,\phi_n).
$$

如果显微模型具有 $O(n)$ 对称性，那么有效自由能只能由 $O(n)$ 不变量组成，最基本的不变量是

$$
\boldsymbol\phi^2
=
\sum_{a=1}^n\phi_a^2.
$$

因此 Landau-Ginzburg 泛函的最低几项通常写成

$$
\mathcal H[\boldsymbol\phi]
=
\int d^dx
\left[
\frac12(\nabla\boldsymbol\phi)^2
+\frac{r}{2}\boldsymbol\phi^2
+\frac{u}{4!}(\boldsymbol\phi^2)^2
-\boldsymbol h\cdot\boldsymbol\phi
\right].
$$

为什么没有三次项？因为 $O(n)$ 对称性包含反演

$$
\boldsymbol\phi\to-\boldsymbol\phi.
$$

任何奇数次的标量项都会在这个变换下变号，因此被对称性禁止。二次项控制是否接近临界点；四次项是稳定自由能所需的最低非线性项，也是 Gaussian 固定点附近最重要的相互作用项。因此短程 Ising、XY、Heisenberg 等普通自旋临界点常被组织到 $\phi^4$ 或 $O(n)$ Wilson-Fisher 理论中。

这里的逻辑不是“显微自旋一定连续，所以写 $\phi^4$”，而是“临界点附近的粗粒化序参量是一个慢变量；对称性允许的最低非高斯相互作用是四次项”。Ising 的显微变量虽然只有 $\pm1$，但粗粒化磁化场可以连续变化；由于它有 $\mathbb Z_2$ 对称性，仍然禁止 $\phi^3$，所以最低非线性项是 $\phi^4$。

### 为什么 percolation 和一般 Potts 会出现三次场论

这里讨论为什么 percolation 和一般 Potts 理论中常出现 $\phi^3$ 项。

Potts 模型更容易让人混乱，因为它同时有自旋表象和 FK cluster 表象。对 $q$-state Potts，自旋序参量不是一个普通的 $q$ 分量向量，而是一个受 $S_q$ 置换对称性约束的对象。粗略说，它有 $q-1$ 个独立分量，并且允许某些 $S_q$ 不变量。

关键点是：一般 $q$ 的 $S_q$ 对称性并不等同于

$$
\boldsymbol\phi\to-\boldsymbol\phi.
$$

因此三次不变量通常不被禁止。Landau 展开中可以出现

$$
g\,\mathcal I_3(\boldsymbol\phi),
$$

其中 $\mathcal I_3$ 是 $S_q$ 允许的三次不变量。于是一般 Potts 的临界场论自然带有 $\phi^3$ 型相互作用，其上临界维度也相应变为

$$
d_c=6.
$$

percolation 的 $\phi^3$ 来源可以从 FK/random-cluster 表象理解得更清楚。在 FK 权重

$$
W(\omega)
\propto
p^{o(\omega)}
(1-p)^{c(\omega)}
q^{k(\omega)}
$$

中，$q$ 是 cluster fugacity。把 $q\to1$ 时，边的开闭变成普通 Bernoulli percolation。这里真正延拓的是 cluster sector，而不是一个“1-state 自旋磁化场”。percolation 的核心观测量是连通性、cluster 大小和 spanning/wrapping 事件，这些对象属于 FK cluster 几何语言。其连续极限中最低非高斯相互作用同样是 cubic，因此常说 percolation 由 $\phi^3$ 型场论描述。

这也解释了一个常见疑问：为什么 $q=2$ Potts 等价于 Ising，但 Ising 又不是 $\phi^3$ 而是 $\phi^4$？

答案是要分清两条分支。

第一条是 **spin sector**。当 $q=2$ 时，Potts 自旋序参量只有一个独立分量，$S_2$ 置换对称性退化成 Ising 的 $\mathbb Z_2$ 反演对称性：

$$
\phi\to-\phi.
$$

于是三次项

$$
\phi^3
$$

被禁止，最低稳定非线性项是

$$
\phi^4.
$$

这就是 Ising spin 临界点由 $\phi^4$ 理论描述的原因。

第二条是 **cluster sector**。即使显微模型是 $q=2$ 的 Ising，若研究的是 FK cluster 的几何性质，也可能需要另一套几何语言。许多 cluster 观测量和 spin 观测量有精确关系，但这不意味着所有几何指数都来自同一个普通磁化场的 $\phi^4$ 展开。尤其当讨论 percolation 极限 $q\to1$ 时，正确对象是 random-cluster 模型的 cluster 分支，而不是把 $q=1$ 当成普通自旋模型。

最实用的记忆方式是：

$$
\text{$O(n)$ 或 Ising spin sector}
\quad\Rightarrow\quad
\text{反演/旋转对称性禁止 cubic}
\quad\Rightarrow\quad
\phi^4,
$$

而

$$
\text{一般 Potts / FK cluster / percolation}
\quad\Rightarrow\quad
\text{cubic 通常允许}
\quad\Rightarrow\quad
\phi^3.
$$

这个说法仍然是场论层面的总览，不是说所有维度、所有 $q$ 都存在完全相同的连续相变。例如二维 Potts 有特殊的共形场论结构，大 $q$ 的 Potts 转变可能变成一级相变。关键点是：场论中保留 $\phi^3$ 还是 $\phi^4$，首先由对称性、观测 sector 和最低允许相互作用决定。

## 容易混淆的几条线

第一，序参量不等于观测量全集。序参量是区分相的核心量，但 Monte Carlo 还会测能量、比热、磁化率、Binder ratio、关联长度、cluster 几何量等。很多无量纲量本身不是序参量，却非常适合定位临界点。

第二，平均场指数不等于“粗糙近似”。平均场可以来自忽略涨落的 Landau 鞍点，也可以在高维、长程、完全图或危险无关变量控制的有限尺寸区域中自然出现。看到平均场指数时，应该问：这是热力学极限的 Gaussian 固定点，还是有限尺寸零模主导的有效标度？

第三，连续场论不等于连续自旋模型。Ising 自旋是离散的，但临界点附近的粗粒化磁化场可以是连续的。反过来，XY 模型的显微变量是连续角度，但二维短程情况下并不会产生普通 Landau 长程序，而是出现 BKT 准长程序。

第四，普适类不是只由哈密顿量名字决定。维度、对称性、序参量分量数、相互作用范围、守恒律、边界条件和约束都可能改变长距离行为。因此“这是 Ising/Potts/XY”只是起点，还要说明是在短程还是长程、二维还是三维、普通自旋 sector 还是 cluster sector。

## 与 Monte Carlo 的关系

相变理论给出应该测什么，Monte Carlo 给出如何测。

- Landau/LGW 告诉我们序参量、磁化率、比热、关联函数如何定义。
- RG 告诉我们临界指数和有限尺寸标度形式。
- Mermin-Wagner 定理提醒我们低维连续对称性不能有真正长程序。
- BKT 理论说明二维 $U(1)$ 系统可以通过拓扑缺陷发生非 Landau 型相变。
- FK/cluster 表象提示我们可以用几何观测量研究临界性。

后面的章节会分别展开这些主题。
