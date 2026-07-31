# SSE 随机级数展开

SSE 的全称是 stochastic series expansion。它是一种量子 Monte Carlo 方法，常用于自旋模型、硬核玻色子模型，以及许多没有 sign problem 的格点量子模型。

它的位置可以这样理解：

| 方法 | 对 $e^{-\beta\hat H}$ 的处理 | 构型语言 |
| --- | --- | --- |
| 离散虚时世界线 | Trotter 分解成很多短时间片 | 每个虚时切片上的基矢量 |
| 连续时间世界线 | 在相互作用表象中展开 kink 事件 | 连续虚时中的跃迁事件 |
| SSE | 直接对指数做 Taylor 展开 | 一个长度可变的算符串 |
| AFQMC | Trotter 分解后做 HS 变换 | 时空辅助场和费米子行列式 |

SSE 和世界线方法很接近，因为二者都在抽样“基矢量如何被一串局域算符演化”。区别在于，世界线把虚时看成几何方向，SSE 把虚时演化改写成一串算符的离散序列。这个算符序列没有预先固定的物理时间间隔，但它仍然携带了热力学信息。

## 从配分函数出发

有限温配分函数为

$$
Z={\rm Tr}\, e^{-\beta \hat H}.
$$

SSE 的第一步是直接展开指数：

$$
e^{-\beta \hat H}
=
\sum_{n=0}^{\infty}
{(-\beta)^n\over n!}
\hat H^n.
$$

于是

$$
Z
=
\sum_{\alpha}
\sum_{n=0}^{\infty}
{(-\beta)^n\over n!}
\langle \alpha|\hat H^n|\alpha\rangle.
$$

这里 $\{|\alpha\rangle\}$ 是一组完备基。对自旋模型，常选 $S^z$ 基；对硬核玻色子，常选 occupation number 基。

为了让矩阵元可以局域计算，把哈密顿量拆成一组 bond operator：

$$
\hat H
=
-\sum_{b=1}^{N_b}\hat H_b.
$$

这里 $b$ 标记格子上的局域项，例如最近邻边。负号只是一个常用约定：如果能把每个 $\hat H_b$ 的非零矩阵元做成非负数，SSE 权重就可以直接作为抽样概率。

代入后：

$$
(-\hat H)^n
=
\left(\sum_b \hat H_b\right)^n.
$$

展开这个 $n$ 次方，就得到一串长度为 $n$ 的局域算符：

$$
S_n=(b_1,b_2,\cdots,b_n).
$$

配分函数写成

$$
Z
=
\sum_{\alpha}
\sum_{n=0}^{\infty}
{\beta^n\over n!}
\sum_{S_n}
\langle \alpha|
\hat H_{b_n}
\cdots
\hat H_{b_2}
\hat H_{b_1}
|\alpha\rangle.
$$

这就是 SSE 的核心：量子配分函数变成了对初态 $|\alpha\rangle$、展开阶数 $n$、算符串 $S_n$ 的求和。

## 构型是什么

一个 SSE 构型可以写成

$$
C=(|\alpha\rangle,S_n).
$$

给定初态 $|\alpha\rangle$ 和算符串以后，可以沿着串逐个作用算符：

$$
|\alpha(p)\rangle
=
\hat H_{b_p}\cdots \hat H_{b_1}|\alpha\rangle,
\qquad
p=0,1,\cdots,n.
$$

其中 $|\alpha(0)\rangle=|\alpha\rangle$。因为配分函数中有 trace，最终必须满足周期条件：

$$
|\alpha(n)\rangle=|\alpha(0)\rangle.
$$

如果某一步矩阵元为零，这个构型的权重就是零。若所有局域矩阵元都非零且非负，构型权重为

$$
W(C)
=
{\beta^n\over n!}
\prod_{p=1}^{n}
\langle \alpha(p)|
\hat H_{b_p}
|\alpha(p-1)\rangle.
$$

这和世界线语言是一回事：算符串中的每个非对角算符会改变中间态，形成一条沿“序列方向”传播的世界线；对角算符只给权重，不改变态。

## 固定长度算符串

无限长、长度可变的算符串不适合直接抽样。常用做法是引入最大长度 $M$，并用单位算符 $\hat I$ 填充：

$$
S_M=([a_1,b_1],[a_2,b_2],\cdots,[a_M,b_M]).
$$

其中 $a_p$ 是算符类型：

| $a_p$ | 含义 |
| --- | --- |
| $0$ | 单位算符 $\hat I$ |
| $1$ | 对角算符 |
| $2$ | 非对角算符 |

非单位算符个数记为 $n$。固定长度写法下，原来的 $1/n!$ 会变成组合因子：

$$
Z
=
\sum_{\alpha}
\sum_{S_M}
{\beta^n(M-n)!\over M!}
\prod_{p=1}^{M}
\langle \alpha(p)|
\hat H_{a_p,b_p}
|\alpha(p-1)\rangle.
$$

这里单位算符的矩阵元为 $1$，所以它只参与组合计数。$M$ 需要足够大，使得采样过程中 $n$ 很少接近 $M$。经验上可以在热化阶段动态增大 $M$，让 $M$ 比观测到的最大 $n$ 留出安全余量。

## 标准例子：Heisenberg 反铁磁模型

考虑自旋 $1/2$ 反铁磁 Heisenberg 模型：

$$
\hat H
=
J\sum_{\langle ij\rangle}
\mathbf S_i\cdot \mathbf S_j,
\qquad J>0.
$$

在 $S^z$ 基下，将每条边上的相互作用写成对角和非对角两部分。常用定义是

$$
\hat H_{1,b}
=
C
-
S_i^zS_j^z,
$$

$$
\hat H_{2,b}
=
{1\over 2}
\left(
S_i^+S_j^-
+
S_i^-S_j^+
\right),
$$

并把哈密顿量写为

$$
\hat H
=
-J\sum_b
\left(
\hat H_{1,b}
-
\hat H_{2,b}
\right)
+
\text{constant}.
$$

在双分格反铁磁模型中，可以通过子格旋转或等价的符号约定，使非对角矩阵元也以正权重进入抽样。这里常数 $C$ 的作用是把对角矩阵元平移到非负区间。对自旋 $1/2$，常取 $C=1/4$，于是 antiparallel 自旋上的对角矩阵元非零，parallel 自旋上的对角矩阵元为零。

直观地说：

- 对角算符检查一条 bond 上的局域自旋状态，并给出权重。
- 非对角算符会把 $|\uparrow\downarrow\rangle$ 和 $|\downarrow\uparrow\rangle$ 互相翻转。
- 合法算符串必须让所有自旋经过整串作用后回到初态。

因此 SSE 构型可以画成一个 vertex 序列。每个非单位算符对应一个四腿 vertex：下面两条腿是作用前的自旋，下面到上面经过局域算符作用，得到作用后的自旋。

## Diagonal update

SSE 的第一类更新是 diagonal update。它只在单位算符和对角算符之间切换：

$$
\hat I
\leftrightarrow
\hat H_{1,b}.
$$

设当前算符串长度为 $M$，非单位算符数为 $n$。扫描每个位置 $p$：

1. 如果当前位置是单位算符，随机选一条 bond $b$，尝试插入对角算符 $\hat H_{1,b}$。
2. 如果当前位置是对角算符，尝试删除它，变回单位算符。
3. 如果当前位置是非对角算符，diagonal update 不动它。

插入接受率来自固定长度权重比。若 proposal 在 $N_b$ 条 bond 中均匀选一条，则

$$
P_{\rm insert}
=
\min\left[
1,
{\beta N_b
\langle \alpha(p)|\hat H_{1,b}|\alpha(p-1)\rangle
\over
M-n}
\right].
$$

删除接受率为

$$
P_{\rm remove}
=
\min\left[
1,
{M-n+1
\over
\beta N_b
\langle \alpha(p)|\hat H_{1,b}|\alpha(p-1)\rangle}
\right].
$$

这两个公式来自三项权重变化：

- 插入一个非单位算符使 $n\to n+1$；
- 固定长度权重中的组合因子从 $\beta^n(M-n)!/M!$ 变成 $\beta^{n+1}(M-n-1)!/M!$；
- 随机选 bond 的 proposal 概率给出额外的 $N_b$ 因子。

diagonal update 负责改变展开阶数 $n$，也就是改变能量相关的统计权重。

## Loop update

只做 diagonal update 不够，因为它不会有效改变自旋构型。SSE 的第二类核心更新是 loop update，也常发展成 directed-loop update。

先把算符串中的每个非单位算符看成一个 vertex。对 Heisenberg 模型，一个 vertex 有四条腿：

```text
上左腿    上右腿
  |        |
  operator
  |        |
下左腿    下右腿
```

每条腿带有一个局域自旋值。沿着算符串传播时，同一个格点在相邻 vertex 之间的腿要连起来；由于 trace 条件，末端还要和开头连起来。这样整个构型变成由 vertex legs 组成的链。

loop update 的基本步骤是：

1. 随机选一条还没访问过的 vertex leg 作为入口。
2. 根据局域 vertex 权重，选择一条出口 leg。
3. 翻转入口和出口相关的自旋，并改变 vertex 类型。
4. 沿着同一格点的连接线移动到下一个 vertex。
5. 重复直到回到起点，形成闭合 loop。
6. 以合适概率翻转整个 loop；在许多对称模型中，构造出来的 loop 可以直接翻转。

这个过程和前面蠕虫算法的精神很接近：更新对象不再是单个自旋，而是一条由局域约束连起来的路径。差别在于，SSE loop 通常在 operator string 的 vertex 图上闭合，而世界线 worm 常显式进入带两个端点的 $\mathcal G$ 空间。

## Directed-loop 思想

普通 loop update 在简单模型中已经很好用。对带磁场、各向异性、玻色 Hubbard 模型等情况，局域 vertex 权重不再高度对称，随便选出口会导致接受率低或 detailed balance 难写。Directed-loop 方法的目标是直接在 vertex 上解一个局域平衡方程。

设入口 leg 为 $i$，出口 leg 为 $j$。局域过程

$$
i\to j
$$

会把旧 vertex $v$ 变成新 vertex $v'$。定义路径权重

$$
A_{ij}(v)
=
W(v)P(i\to j|v).
$$

局域 detailed balance 要求

$$
A_{ij}(v)
=
A_{ji}(v').
$$

同时对每个入口 $i$，概率要归一化：

$$
\sum_j P(i\to j|v)=1.
$$

这组方程称为 directed-loop equations。实际求解时通常希望减少 bounce 过程，也就是入口和出口相同、loop 原路返回的情况。bounce 越多，loop 更新越像局域抖动，效率越差。

一次 directed-loop 更新可以抽象为：

```text
choose an initial leg
while loop not closed:
    read current vertex and entrance leg
    sample exit leg from directed-loop table
    update local vertex state
    move through the link to the next vertex leg
```

难点主要在两处：第一，针对具体模型列出所有允许 vertex；第二，求出非负的转移概率表。

### Directed-loop 表的实际用法

公开 SSE 教程和 ALPS 的 directed-loop 实现都采用同一类结构：先按模型参数生成局域 scattering table，而不是在每一步重新解 directed-loop equations。更新时只需要根据当前 vertex 类型和入口 leg 查表抽出口 leg。

一个典型表项包含：

| 项 | 含义 |
| --- | --- |
| `vertex_type` | 当前局域算符和四条腿上的局域态 |
| `entrance_leg` | loop 进入 vertex 的腿 |
| `exit_leg` | 被抽样选中的出口腿 |
| `new_vertex_type` | 翻转入口/出口后得到的新 vertex |
| `probability` | 满足局域平衡方程的条件概率 |

构造表时要满足三件事：

1. 每个入口的所有出口概率和为 $1$。
2. 每个局域过程和反过程满足

$$
A_{ij}(v)=A_{ji}(v').
$$

3. 所有概率非负，并尽量减少 bounce。

这解释了 directed-loop 为什么比“随便走一个 loop”更通用：外场、各向异性或软核玻色子会让不同 vertex 权重不相等，查表的局域 scattering 才能把这些不等权重精确放进更新。

### 一个 sweep 的逻辑结构

一个常见 SSE sweep 可以组织为：

```text
propagate alpha through operator string
diagonal update:
    I <-> diagonal operator
rebuild linked vertex list
loop / directed-loop update:
    repeat until enough legs are visited:
        choose an entrance leg
        follow scattering table until path closes
        update vertices and spins along the path
measure:
    expansion order n
    propagated states or improved estimators
resize M if n is too close to cutoff
```

其中 `propagate alpha` 和 `rebuild linked vertex list` 是容易被低估的两步。前者保证每个算符位置看到的中间态正确；后者保证同一个格点在相邻 vertex 之间的腿连接正确。若连接表错了，loop update 仍可能“闭合”，但测量会系统性错误。

### 和教程文献的对应

Sandvik 的 operator-loop SSE 工作（`arXiv:cond-mat/9902226`，Phys. Rev. B 59, 14157）给出固定长度 operator string、diagonal update 和 operator-loop update 的标准框架。Syljuåsen 与 Sandvik 的 directed-loop 工作（`arXiv:cond-mat/0202316`，Phys. Rev. E 66, 046701）把 loop 在 vertex 上的局域选择写成 directed-loop equations，使外场、各向异性和软核玻色子等不对称 vertex 权重也能系统处理。ALPS 的 `dirloop_sse` 文档则体现了工程化组织：先把模型解析成 vertex 类型和 scattering table，再在任意格子上执行 directed loop。

SSE 的公式和实现约束可以按三层理解：

- **数学层**：Taylor 展开 $e^{-\beta\hat H}$，得到 $(|\alpha\rangle,S_M)$。
- **局域权重层**：把哈密顿量拆成 bond operator 和 vertex。
- **更新层**：diagonal update 改变 $n$，directed loop 改变 vertex 网络和基态。

## 观测量

SSE 中很多热力学量可以直接从展开阶数 $n$ 得到。由

$$
\langle n\rangle
=
\beta \langle -\hat H\rangle
$$

可得能量估计量

$$
E
=
\langle \hat H\rangle
=
-{\langle n\rangle\over \beta}
+E_{\rm shift}.
$$

这里 $E_{\rm shift}$ 是为了让权重非负而加入的常数平移，需要在最终能量中加回去。

比热可以由 $n$ 的涨落给出：

$$
C_V
=
{1\over N}
\left(
\langle n^2\rangle
-
\langle n\rangle^2
-
\langle n\rangle
\right),
$$

其中 $N$ 是格点数。若使用了常数平移，能量本身要修正，但 $n$ 的涨落公式结构保持相同。

磁化强度、结构因子和关联函数通常从传播态 $|\alpha(p)\rangle$ 或 loop improved estimator 中测量。例如静态结构因子可写成

$$
S(\mathbf k)
=
{1\over N}
\sum_{ij}
e^{i\mathbf k\cdot(\mathbf r_i-\mathbf r_j)}
\langle S_i^zS_j^z\rangle.
$$

在算符串传播过程中，可以多次采样中间态并对这些中间态平均；这相当于利用虚时平移对称性降低方差。

## 和世界线方法的关系

SSE 没有显式把 $[0,\beta]$ 切成 $L_\tau$ 个小时间片，因此没有 Trotter 误差。展开阶数 $n$ 在统计上大约满足

$$
\langle n\rangle \sim \beta \lvert E\rvert.
$$

所以 operator string 的长度随 $\beta$ 和系统体积增长。它扮演了“虚时方向事件数”的角色。

从图像上看：

- 世界线方法记录粒子或自旋沿虚时方向如何传播。
- SSE 记录哪些局域算符按什么顺序作用。
- 非对角算符的位置对应世界线中的 kink 或 vertex。
- loop / directed-loop 更新对应在这些 vertex leg 网络上构造非局域路径。

因此，SSE 是世界线 QMC 的一种离散算符串表述。它保留了世界线的几何直觉，同时避开了离散虚时 Trotter 误差。

## 和 AFQMC 的关系

SSE 与 AFQMC 都从配分函数出发，但处理相互作用的方式不同。

| 项目 | SSE | AFQMC |
| --- | --- | --- |
| 展开对象 | $e^{-\beta\hat H}$ 的 Taylor 级数 | Trotter 切片后的相互作用项 |
| 构型 | 基矢量和算符串 | 时空辅助场 |
| 权重 | 局域矩阵元乘积 | 费米子行列式 |
| 常见对象 | 自旋、玻色子、无 sign problem 模型 | 费米 Hubbard、相互作用费米子 |
| 主要更新 | diagonal update、loop、directed loop | 辅助场翻转、Green 函数更新 |

SSE 的优势是局域权重清楚，loop 更新效率高，且没有 Trotter 误差。AFQMC 的优势是可以把费米子自由度精确积分掉，在很多费米系统中更自然。二者都可能遇到 sign problem；只是 sign problem 出现的形式不同。

## 正确性检查清单

SSE 更新的正确性可以按下面顺序检查：

1. 哈密顿量是否已经平移或改写到非负矩阵元形式。
2. $M$ 是否足够大，采样中 $n$ 是否远离上界。
3. diagonal insertion/removal 的组合因子是否正确。
4. 传播态 $|\alpha(p)\rangle$ 是否和算符串完全一致。
5. 非对角算符是否正确改变局域基态。
6. trace 周期条件 $|\alpha(M)\rangle=|\alpha(0)\rangle$ 是否满足。
7. loop 或 directed-loop 的 vertex leg 连接是否正确处理周期边界。
8. directed-loop 概率表是否非负并满足局域 detailed balance。
9. 能量中的 constant shift 是否在最终结果中加回。
10. 小系统是否能和精确对角化比较能量、比热和结构因子。

## 小结

SSE 的核心公式是

$$
Z
=
\sum_{\alpha}
\sum_{n=0}^{\infty}
{\beta^n\over n!}
\sum_{S_n}
\langle \alpha|
\hat H_{b_n}\cdots \hat H_{b_1}
|\alpha\rangle.
$$

它把量子热力学问题改写为对算符串的抽样。diagonal update 改变展开阶数，loop 或 directed-loop update 改变基态和非对角结构。对自旋和玻色系统，这套语言既保留了世界线的几何直觉，又给出了非常高效、无 Trotter 误差的有限温量子 Monte Carlo 算法。
