# 辅助场蒙卡的基本思想

辅助场 Monte Carlo 的核心问题是：费米子带有反对易关系，许多相互作用模型的权重很难直接写成正数概率。辅助场方法的做法是先把相互作用项用一个额外的经典场解耦，然后在给定辅助场构型的情况下，把费米子自由度精确积分掉。最后需要抽样的对象变成辅助场构型。

最常见的例子是 Hubbard 模型：

$$
\hat H=
-t\sum_{\langle ij\rangle,\sigma}
\left(
\hat c_{i\sigma}^{\dagger}\hat c_{j\sigma}
+\hat c_{j\sigma}^{\dagger}\hat c_{i\sigma}
\right)
+U\sum_i
\left(\hat n_{i\uparrow}-\frac12\right)
\left(\hat n_{i\downarrow}-\frac12\right).
$$

第一项是 hopping，第二项是 onsite interaction。若没有 $U$，这是一个二次型费米子问题，可以用单粒子矩阵处理；困难恰好来自四费米子相互作用。辅助场的作用，就是把四费米子项变成“费米子二次型 + 辅助场求和”。

## 从配分函数出发

有限温配分函数为

$$
Z={\rm Tr}\,e^{-\beta \hat H}.
$$

把虚时长度 $\beta$ 分成 $L_\tau$ 片，

$$
\Delta\tau=\frac{\beta}{L_\tau},
$$

并将哈密顿量写成

$$
\hat H=\hat K+\hat V,
$$

其中 $\hat K$ 是二次型 hopping 项，$\hat V$ 是相互作用项。利用 Trotter 分解：

$$
e^{-\Delta\tau(\hat K+\hat V)}
=
e^{-\Delta\tau \hat K}
e^{-\Delta\tau \hat V}
+\mathcal O(\Delta\tau^2).
$$

于是

$$
Z
\simeq
{\rm Tr}
\prod_{\ell=1}^{L_\tau}
e^{-\Delta\tau \hat K}
e^{-\Delta\tau \hat V}.
$$

这一写法把问题变成一层一层虚时切片的乘积。接下来要处理的是每个切片上的相互作用指数。

## Hubbard-Stratonovich 变换

Hubbard-Stratonovich 变换的目标是将

$$
e^{-\Delta\tau U
\left(\hat n_{\uparrow}-\frac12\right)
\left(\hat n_{\downarrow}-\frac12\right)}
$$

改写为对辅助场 $s=\pm 1$ 的求和。对于排斥 Hubbard 模型，常用的离散自旋通道分解为

$$
e^{-\Delta\tau U
\left(\hat n_{\uparrow}-\frac12\right)
\left(\hat n_{\downarrow}-\frac12\right)}
=
\frac12 e^{-\Delta\tau U/4}
\sum_{s=\pm 1}
e^{\lambda s(\hat n_{\uparrow}-\hat n_{\downarrow})},
$$

其中 $\lambda$ 由

$$
\cosh \lambda = e^{\Delta\tau U/2}
$$

确定。这里的常数因子通常可以并入整体归一化；真正重要的是，相互作用被写成了自旋向上和自旋向下粒子各自感受到的外场。

在整个时空格点上，辅助场构型记为

$$
s=\{s_{i,\ell}\},
\qquad
i=1,\cdots,N_s,\quad
\ell=1,\cdots,L_\tau.
$$

给定 $s$ 以后，费米子哈密顿量重新变成二次型。二次型费米子可以精确求迹，这一步正是 AFQMC 与许多局域更新算法的分水岭。

## 积分掉费米子

对每一个虚时切片和自旋方向，可以定义单粒子传播矩阵

$$
B_\ell^\sigma(s_\ell)
=
e^{-\Delta\tau K}
e^{V_\ell^\sigma(s_\ell)}.
$$

这里 $K$ 是 hopping 对应的单粒子矩阵，$V_\ell^\sigma$ 是辅助场给出的对角矩阵。对于上面的 spin-channel 分解，

$$
\left[V_\ell^\uparrow\right]_{ij}
=
\lambda s_{i,\ell}\delta_{ij},
\qquad
\left[V_\ell^\downarrow\right]_{ij}
=
-\lambda s_{i,\ell}\delta_{ij}.
$$

有限温 trace 的一个关键恒等式是：

$$
{\rm Tr}
\left[
e^{\hat c^\dagger A_1\hat c}
e^{\hat c^\dagger A_2\hat c}
\cdots
e^{\hat c^\dagger A_m\hat c}
\right]
=
\det
\left[
I+
e^{A_1}e^{A_2}\cdots e^{A_m}
\right].
$$

因此，配分函数可以写成辅助场构型的求和：

$$
Z
=
\sum_{\{s\}}
W(s),
$$

其中

$$
\boxed{
W(s)
=
C
\det M_\uparrow(s)
\det M_\downarrow(s)
}
$$

并且

$$
M_\sigma(s)
=
I+
B_{L_\tau}^\sigma(s_{L_\tau})
\cdots
B_2^\sigma(s_2)
B_1^\sigma(s_1).
$$

这样，原本的量子多体求和变成了对辅助场 $s_{i,\ell}$ 的经典 Monte Carlo 抽样。每一步更新尝试改变一个或一组辅助场，然后根据行列式权重比决定接受概率。

## 构型权重与接受率

若从构型 $s$ 尝试更新到 $s'$，常用 Metropolis 接受率为

$$
P_{\rm acc}(s\to s')
=
\min\left[
1,
\frac{W(s')}{W(s)}
\frac{A(s'\to s)}{A(s\to s')}
\right].
$$

对于对称 proposal，接受率简化为

$$
P_{\rm acc}(s\to s')
=
\min\left[
1,
\frac{\det M_\uparrow(s')\det M_\downarrow(s')}
{\det M_\uparrow(s)\det M_\downarrow(s)}
\right].
$$

实际计算很少每次从头计算两个行列式。若只翻转一个辅助场 $s_{i,\ell}$，单粒子传播矩阵只发生局域变化，可以用 Green 函数和 Sherman-Morrison 公式快速得到行列式比，并在接受后更新 Green 函数。

这个结构是有限温 determinantal QMC 的标准主线。Assaad 与 Evertz 的综述 *World-line and Determinantal Quantum Monte Carlo Methods for Spins, Phonons and Electrons* 将它概括为三步：Trotter 分解、Hubbard-Stratonovich 解耦、对二次型费米子求迹得到行列式权重。后续所有 Green 函数传播、局域更新和稳定化技巧，都是为了高效维护这一行列式权重。

## Sign Problem

Monte Carlo 需要把构型权重解释成概率。若

$$
W(s)\ge 0
$$

对所有构型成立，那么可以直接按 $W(s)$ 抽样。很多半填充、双分格 Hubbard 模型在粒子空穴对称性下满足

$$
\det M_\uparrow(s)=\det M_\downarrow(s),
$$

于是

$$
W(s)=\left[\det M_\uparrow(s)\right]^2\ge 0.
$$

一般情形中，权重可能为负数或复数。此时常写成

$$
W(s)=|W(s)|\,{\rm sign}(s),
$$

按 $|W(s)|$ 抽样，并把符号放进观测量：

$$
\langle O\rangle
=
\frac{\langle O(s)\,{\rm sign}(s)\rangle_{|W|}}
{\langle {\rm sign}(s)\rangle_{|W|}}.
$$

当平均符号

$$
\langle {\rm sign}\rangle_{|W|}
$$

随系统尺寸或低温指数衰减时，误差会快速放大。这就是 sign problem。它是费米子量子 Monte Carlo 中最根本的困难之一，不能只看作实现细节。

## 观测量框架

给定辅助场构型后，许多观测量可以由单粒子 Green 函数得到：

$$
G^\sigma_{ij}(s)
=
\langle \hat c_{i\sigma}\hat c_{j\sigma}^{\dagger}\rangle_s.
$$

例如密度满足

$$
\langle \hat n_{i\sigma}\rangle_s
=
1-G^\sigma_{ii}(s),
$$

而二体关联函数可以通过 Wick 定理化成 Green 函数的组合。于是 AFQMC 的计算流程通常分成四层：

1. 根据当前辅助场维护传播矩阵和 Green 函数。
2. 尝试局域或全局更新辅助场。
3. 用行列式比计算接受率。
4. 在平衡后测量 Green 函数、能量和关联函数。

## 常见注意事项

- **Trotter 误差**：有限 $\Delta\tau$ 会带来系统误差，通常需要对多个 $\Delta\tau$ 外推。
- **矩阵乘积不稳定**：低温或大系统中，许多 $B$ 矩阵连乘会病态，需要 QR、SVD 或稳定化分块。
- **更新效率**：局域更新便宜但可能自关联时间长；全局更新更容易跨越构型障碍，但接受率和代价需要平衡。
- **符号问题**：平均符号很小时，即使程序完全正确，统计误差也会让结果失去可用性。
- **测量频率**：Green 函数重算和稳定化有成本，测量间隔需要结合自关联时间设置。

## 有限温 DQMC 的计算流程

有限温 DQMC 的核心流程可以由几条公式串起来：

1. 辅助场构型的权重来自

$$
W(s)=
\prod_{\sigma=\uparrow,\downarrow}
\det\left[I+B^\sigma(s)\right].
$$

2. 等时 Green 函数可以写成

$$
G(\tau,\tau)
=
\left[
I+B(\tau,0)B(\beta,\tau)
\right]^{-1}.
$$

3. 翻转一个 onsite HS 场时，矩阵变化是 rank-one 的，行列式比可化成

$$
r_\sigma
=
1+\Delta_{ii}^\sigma
\left(1-G^\sigma_{ii}\right).
$$

4. 接受后用 Sherman-Morrison 公式更新 $G$，然后逐层传播到下一虚时层。

这套流程说明，DQMC 的效率来自两个事实：相互作用被 HS 场局域化，单点更新只改变一个对角元素；费米子已经被积分掉，测量可以尽量从 Green 函数和 Wick 定理得到。

## 高级试探波函数的 AFQMC

`arXiv:2505.18519v1` 讨论的是投影型 fermion AFQMC 中如何使用更复杂的 trial wave function。普通 phaseless 或 constrained AFQMC 常用单个 Slater determinant 或少量 determinant 线性组合做试探态；试探态既影响符号/相位约束，也影响 importance sampling 的效率。

该工作的思路是：若相关试探波函数可以写成“隐藏变量积分下的 Slater determinant 叠加”，就可以把 walker 与一个广义 Metropolis 抽样耦合起来，随机抽样这些隐藏变量，而不是显式展开一个巨大的 determinant 列表。对 AFQMC 主线而言，重要结论不是具体化学计算细节，而是下面这点：

AFQMC 的核心对象仍然是 Slater determinant walker；更复杂的相关试探态可以通过额外的随机变量和重要性抽样进入约束与权重，而不一定破坏低阶多项式标度。

这可以作为零温 AFQMC 章节中“试探态选择会影响精度与效率”的补充背景。

从这个角度看，AFQMC 的主线很清楚：用辅助场把相互作用费米子问题变成一组二次型费米子问题，再用行列式权重在辅助场空间中做 Monte Carlo。
