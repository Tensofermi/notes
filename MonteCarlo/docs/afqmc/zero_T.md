# 零温辅助场蒙卡

零温 AFQMC 研究的是基态性质。它不直接计算

$$
Z={\rm Tr}\,e^{-\beta \hat H},
$$

而是利用虚时投影：

$$
|\Psi_0\rangle
\propto
\lim_{\Theta\to\infty}
e^{-\Theta\hat H}
|\Psi_T\rangle.
$$

这里 $|\Psi_T\rangle$ 是试探波函数，只要它和真实基态 $|\Psi_0\rangle$ 有非零重叠，足够长的虚时投影就会压低激发态成分。若

$$
|\Psi_T\rangle
=
\sum_n a_n|\Psi_n\rangle,
$$

则

$$
e^{-\Theta \hat H}|\Psi_T\rangle
=
\sum_n a_n e^{-\Theta E_n}|\Psi_n\rangle.
$$

当 $\Theta$ 足够大时，最低能态保留下来。这个图像非常像有限温中的 $\beta\to\infty$ 极限，但零温算法保留了试探态边界，因此在实现和测量上有自己的结构。

## 投影形式

基态期望值写为

$$
\langle O\rangle
=
\frac{
\langle \Psi_T|
e^{-\Theta\hat H}
O
e^{-\Theta\hat H}
|\Psi_T\rangle
}{
\langle \Psi_T|
e^{-2\Theta\hat H}
|\Psi_T\rangle
}.
$$

把总投影长度 $2\Theta$ 切成 $L_\tau$ 片：

$$
\Delta\tau=\frac{2\Theta}{L_\tau}.
$$

与有限温类似，做 Trotter 分解：

$$
e^{-\Delta\tau\hat H}
\simeq
e^{-\Delta\tau\hat K}
e^{-\Delta\tau\hat V}.
$$

再对每个虚时切片做 Hubbard-Stratonovich 变换，得到辅助场构型

$$
s=\{s_{i,\ell}\}.
$$

给定辅助场后，自旋 $\sigma$ 的单粒子传播矩阵仍写为

$$
B_\ell^\sigma(s_\ell)
=
e^{-\Delta\tau K}e^{V_\ell^\sigma(s_\ell)}.
$$

## Slater Determinant 边界

零温 AFQMC 通常选取 Slater determinant 作为试探波函数：

$$
|\Psi_T^\sigma\rangle
=
\prod_{m=1}^{N_\sigma}
\left(
\sum_i P^\sigma_{im}\hat c^\dagger_{i\sigma}
\right)
|0\rangle.
$$

矩阵 $P^\sigma$ 的大小为

$$
N_s\times N_\sigma,
$$

其中 $N_s$ 是空间格点数，$N_\sigma$ 是该自旋方向的粒子数。二次型传播作用在 Slater determinant 上仍然得到 Slater determinant，因此给定辅助场后，整个振幅可以写成有限维行列式。

记

$$
\mathcal B^\sigma(s)
=
B_{L_\tau}^\sigma
\cdots
B_2^\sigma
B_1^\sigma.
$$

则构型权重为

$$
\boxed{
W(s)=
\prod_\sigma
\det
\left[
(P^\sigma)^\dagger
\mathcal B^\sigma(s)
P^\sigma
\right].
}
$$

有限温算法中出现的是 $I+\prod B$；零温算法中出现的是试探态矩阵夹住的传播子。这是两类算法最直观的差别。

## 左右传播子

为了测量位于虚时中间的观测量，通常把传播分成左、右两半。若观测量插在第 $\ell$ 层附近，可定义

$$
R_\ell^\sigma
=
B_\ell^\sigma
B_{\ell-1}^\sigma
\cdots
B_1^\sigma
P^\sigma,
$$

以及

$$
L_\ell^\sigma
=
\left[
B_{L_\tau}^\sigma
\cdots
B_{\ell+1}^\sigma
\right]^\dagger
P^\sigma.
$$

这里 $R_\ell^\sigma$ 和 $L_\ell^\sigma$ 都是 $N_s\times N_\sigma$ 矩阵。构型权重可以写成

$$
W_\sigma(s)
=
\det
\left[
(L_\ell^\sigma)^\dagger R_\ell^\sigma
\right].
$$

这种左右夹逼结构说明：零温算法中的测量最好放在投影中间。越靠近边界，结果越容易受到试探波函数影响；投影长度足够大时，中间区域才代表基态。

## Equal-Time Green 函数

给定左右 Slater determinant 后，equal-time Green 函数可写为

$$
G^\sigma_{ij}
=
\langle
\hat c_{i\sigma}
\hat c_{j\sigma}^\dagger
\rangle_s.
$$

若定义

$$
S^\sigma=(L^\sigma)^\dagger R^\sigma,
$$

则一个常用表达是

$$
\boxed{
G^\sigma
=
I
-
R^\sigma
(S^\sigma)^{-1}
(L^\sigma)^\dagger .
}
$$

因此密度为

$$
\langle \hat n_{i\sigma}\rangle_s
=
1-G^\sigma_{ii}.
$$

二体观测量通过 Wick 定理化为 Green 函数组合。例如

$$
\langle
\hat n_{i\sigma}\hat n_{j\sigma'}
\rangle_s
$$

在 $\sigma=\sigma'$ 和 $\sigma\ne\sigma'$ 时有不同的收缩形式，指标顺序需要与 Green 函数定义保持一致。

## 局域更新

一次常见更新是翻转某个时空点的辅助场：

$$
s_{i,\ell}\to -s_{i,\ell}.
$$

这只改变第 $\ell$ 层的对角矩阵 $V_\ell^\sigma$。因此新旧传播矩阵之间的差别是局域的，可以写成

$$
B_\ell^{\sigma\,\prime}
=
(I+\Delta^\sigma)B_\ell^\sigma,
$$

其中 $\Delta^\sigma$ 只有第 $i$ 个对角元非零。行列式比可以用当前 Green 函数快速计算，形式上可写为

$$
r_\sigma
=
1+
(1-G^\sigma_{ii})\Delta^\sigma_{ii}.
$$

总接受率为

$$
P_{\rm acc}
=
\min\left[
1,
\prod_\sigma r_\sigma
\right].
$$

若更新被接受，Green 函数可以用 rank-one 公式更新，而不用从头构造左右传播子。实际代码会在连续多次局域更新后，周期性地重新计算 Green 函数以控制舍入误差。

## 数值稳定化

虚时传播矩阵连乘是零温 AFQMC 中最容易出问题的地方。矩阵

$$
B_mB_{m-1}\cdots B_1
$$

会同时包含指数放大的方向和指数衰减的方向。随着 $\Theta$ 增大，直接相乘会丢失线性独立性。

常用处理方式是每隔若干层做一次分解：

$$
B_{\ell+p}\cdots B_{\ell+1}Q
=
Q'R
$$

或使用 SVD：

$$
UDV.
$$

其中 $D$ 存储尺度，$U,V$ 存储方向。这类分解把“大数小数”和“方向信息”分开保存，避免一个矩阵乘积吞掉全部精度。

## 投影长度与试探态

零温算法有两个重要外推：

- **投影长度外推**：增大 $\Theta$，检查观测量是否达到平台。
- **Trotter 外推**：减小 $\Delta\tau$，检查离散虚时误差。

试探态选择会影响收敛速度。常见选择包括：

- 自由费米子基态。
- 平均场基态。
- 带有轻微对称性破缺的 Slater determinant。

只要试探态与目标基态重叠非零，足够长的投影可以消除边界影响。较好的试探态能显著减少所需投影长度。

## 零温算法流程

零温 AFQMC 的典型流程为：

1. 构造试探态矩阵 $P^\sigma$。
2. 初始化辅助场 $s_{i,\ell}$。
3. 维护左右传播子和 Green 函数。
4. 逐层翻转辅助场并用行列式比接受或拒绝。
5. 定期重算 Green 函数并做 QR/SVD 稳定化。
6. 在投影中心附近测量能量、密度、关联函数。
7. 对投影长度、Trotter 步长和统计误差做检查。

零温 AFQMC 的优点是可以直接接近基态；代价是需要控制试探态边界、投影长度和矩阵稳定化。理解左右 Slater determinant 的结构，是理解这一算法的关键。
