# 有限温辅助场蒙卡

有限温 AFQMC 的目标是计算

$$
Z={\rm Tr}\,e^{-\beta\hat H},
$$

以及热平均

$$
\langle O\rangle
=
\frac{1}{Z}
{\rm Tr}
\left[
Oe^{-\beta\hat H}
\right].
$$

与零温投影算法相比，有限温算法没有试探波函数边界；虚时方向首尾相接，形成一个闭合圆。这个闭合结构会让权重自然出现

$$
\det(I+\prod_\ell B_\ell).
$$

## Trace 与虚时切片

仍以 Hubbard 模型为例，将哈密顿量分成

$$
\hat H=\hat K+\hat V.
$$

把 $\beta$ 分成 $L_\tau$ 片后，

$$
e^{-\beta\hat H}
\simeq
\prod_{\ell=1}^{L_\tau}
e^{-\Delta\tau\hat K}
e^{-\Delta\tau\hat V},
\qquad
\Delta\tau=\frac{\beta}{L_\tau}.
$$

对每个时空点做 Hubbard-Stratonovich 变换，得到辅助场构型

$$
s=\{s_{i,\ell}\}.
$$

给定 $s$ 后，单粒子传播矩阵为

$$
B_\ell^\sigma(s_\ell)
=
e^{-\Delta\tau K}
e^{V_\ell^\sigma(s_\ell)}.
$$

把所有虚时切片连乘：

$$
\mathcal B^\sigma(s)
=
B_{L_\tau}^\sigma
B_{L_\tau-1}^\sigma
\cdots
B_1^\sigma.
$$

利用二次型费米子 trace 恒等式：

$$
{\rm Tr}\,
e^{\hat c^\dagger A_1\hat c}
\cdots
e^{\hat c^\dagger A_m\hat c}
=
\det
\left[
I+e^{A_1}\cdots e^{A_m}
\right],
$$

可得辅助场权重

$$
\boxed{
W(s)
=
C
\prod_\sigma
\det
\left[
I+\mathcal B^\sigma(s)
\right].
}
$$

于是有限温 AFQMC 的采样空间就是所有 $s_{i,\ell}=\pm1$ 的构型。

## Equal-Time Green 函数

给定辅助场后，等时 Green 函数定义为

$$
G^\sigma_{ij}(\ell)
=
\langle
\hat c_{i\sigma}
\hat c_{j\sigma}^\dagger
\rangle_{s,\ell}.
$$

若观测量放在第 $\ell$ 层之后，定义循环乘积

$$
\mathcal B^\sigma_\ell
=
B_\ell^\sigma
B_{\ell-1}^\sigma
\cdots
B_1^\sigma
B_{L_\tau}^\sigma
\cdots
B_{\ell+1}^\sigma.
$$

则

$$
\boxed{
G^\sigma(\ell)
=
\left[
I+\mathcal B^\sigma_\ell
\right]^{-1}.
}
$$

从这个 Green 函数可以得到密度：

$$
\langle \hat n_{i\sigma}\rangle_s
=
1-G^\sigma_{ii}.
$$

动能项通常写成

$$
\langle \hat K\rangle_s
=
\sum_{ij,\sigma}
K_{ij}
\langle
\hat c_{i\sigma}^\dagger
\hat c_{j\sigma}
\rangle_s,
$$

而

$$
\langle
\hat c_{i\sigma}^\dagger
\hat c_{j\sigma}
\rangle_s
=
\delta_{ij}-G^\sigma_{ji}.
$$

相互作用能和关联函数则通过密度与 Wick 收缩得到。

## 局域辅助场更新

有限温算法常用 sweep 更新：依次遍历所有虚时层和空间点，尝试翻转

$$
s_{i,\ell}\to -s_{i,\ell}.
$$

该更新只改变 $B_\ell^\sigma$ 中一个对角元素。记变化矩阵为

$$
B_\ell^{\sigma\,\prime}
=(I+\Delta^\sigma)B_\ell^\sigma,
$$

其中

$$
\Delta^\sigma_{jj}=0
\quad (j\ne i).
$$

行列式比具有局域形式：

$$
r_\sigma
=
1+
(1-G^\sigma_{ii})\Delta^\sigma_{ii}.
$$

总权重比为

$$
r=\prod_\sigma r_\sigma.
$$

若 proposal 对称，接受率为

$$
P_{\rm acc}
=
\min(1,r).
$$

接受后，Green 函数可用 Sherman-Morrison 公式更新。典型形式是

$$
G'_{mn}
=
G_{mn}
-
\frac{
\left(G_{mi}-\delta_{mi}\right)
\Delta_{ii}
G_{in}
}{
1+(1-G_{ii})\Delta_{ii}
}.
$$

不同文献对 $G=\langle cc^\dagger\rangle$ 或 $G=\langle c^\dagger c\rangle$ 的定义不同，公式符号也会随之变化。因此需要先固定 Green 函数定义，再统一密度、行列式比和更新公式。

## Green 函数传播

在一个 sweep 中，如果从第 $\ell$ 层移动到第 $\ell+1$ 层，Green 函数可以通过相似变换传播：

$$
G(\ell+1)
=
B_{\ell+1}
G(\ell)
B_{\ell+1}^{-1}.
$$

这一步避免每一层都重新求逆。不过传播会累积舍入误差，因此每隔若干层需要从稳定化矩阵重新计算 $G$。

常见流程为：

1. 在某一层用稳定化乘积构造准确的 $G$。
2. 在该层做空间点局域更新。
3. 将 $G$ 传播到下一层。
4. 重复若干层后重新稳定化。

## 矩阵乘积稳定化

低温下 $L_\tau$ 很大，直接计算

$$
B_{L_\tau}\cdots B_1
$$

会数值病态。原因是不同单粒子模式在虚时传播中按

$$
e^{-\beta \epsilon_n}
$$

缩放，尺度差随 $\beta$ 指数增长。

常用做法是将传播矩阵分块：

$$
\mathcal B
=
(B_{L_\tau}\cdots B_{L_\tau-m+1})
\cdots
(B_m\cdots B_1).
$$

每个块做 QR 或 SVD 分解，例如

$$
B_{\ell+m}\cdots B_{\ell+1}
=
QDR.
$$

其中 $D$ 存放尺度，$Q,R$ 保留方向。计算

$$
\left(I+\mathcal B\right)^{-1}
$$

时，也要用稳定化形式进行矩阵代数，避免直接把所有矩阵乘回去。

## 测量

有限温算法中，热平均写为

$$
\langle O\rangle
=
\frac{
\sum_s O(s)W(s)
}{
\sum_s W(s)
}.
$$

若没有 sign problem，直接按 $W(s)$ 抽样即可。若存在符号，需要使用

$$
\langle O\rangle
=
\frac{\langle O(s)\,{\rm sign}(s)\rangle_{|W|}}
{\langle {\rm sign}(s)\rangle_{|W|}}.
$$

常见测量包括：

- 粒子数与压缩率。
- 动能、相互作用能和总能量。
- 自旋关联函数与结构因子。
- 配对关联函数。
- 单粒子 Green 函数和谱函数相关的虚时关联。

等时观测量可以直接由 $G(\ell)$ 得到；不等时关联函数需要保存或重构不同虚时层之间的传播子。

## 与零温算法的比较

有限温算法的边界条件是虚时周期 trace：

$$
\det(I+B_{L_\tau}\cdots B_1).
$$

零温算法的边界条件是试探 Slater determinant：

$$
\det(P^\dagger B_{L_\tau}\cdots B_1P).
$$

因此二者在物理图像上分别对应：

- 有限温：热系综，参数是 $\beta$。
- 零温：基态投影，参数是投影长度 $\Theta$ 和试探态 $|\Psi_T\rangle$。

实现层面上，两者都要处理辅助场更新、Green 函数维护、矩阵稳定化和 sign problem。掌握有限温算法后，再看零温算法，很多公式只是把 trace 边界换成 Slater determinant 边界。

## 常见检查

- 增大 $L_\tau$ 或减小 $\Delta\tau$，检查 Trotter 误差。
- 增大系统尺寸，检查有限尺寸效应。
- 改变稳定化间隔，确认结果不依赖数值分块。
- 监控平均符号，判断统计误差是否可信。
- 用非相互作用极限 $U=0$ 或小系统 exact diagonalization 做 benchmark。

有限温 AFQMC 可以被看作一个非常清楚的流程：把虚时离散化，用辅助场解耦相互作用，积分掉费米子得到行列式权重，再在辅助场构型空间中做 Monte Carlo。
