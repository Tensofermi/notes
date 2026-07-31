# 关联函数范式

相变理论里，关联函数是一条非常核心的主线。序参量告诉我们“有没有有序”，自由能告诉我们“热力学是否奇异”，而关联函数告诉我们“涨落如何在空间中传播”。许多临界指数、结构因子、响应函数和有限尺寸标度，都可以从关联函数的长距离形式读出来。

核心逻辑可以概括为：

$$
\text{关联函数}
\rightarrow
\text{响应函数}
\rightarrow
\text{有限尺寸标度}
\rightarrow
\text{不同相的物理图像}.
$$

## 连通关联函数

设序参量场为 $\phi(x)$。最常用的是两点关联函数

$$
G(r)=\langle \phi(r)\phi(0)\rangle.
$$

如果系统有非零平均值

$$
\langle \phi\rangle=m,
$$

那么 $G(r)$ 在远距离会包含一个平凡平台：

$$
G(r)\to m^2.
$$

真正描述涨落传播的是连通关联函数：

$$
G_c(r)
=
\langle \phi(r)\phi(0)\rangle
-
\langle\phi\rangle^2.
$$

在 Ising 有序相里，这个区分尤其重要。普通关联函数有 $m^2$ 平台；连通关联函数才描述 domain-wall 或局域涨落的衰减。

## 磁化率来自关联函数积分

设总磁化为

$$
M=\sum_i s_i.
$$

磁化率可以写成涨落：

$$
\chi
=
\frac{\beta}{V}
\left(
\langle M^2\rangle-\langle M\rangle^2
\right).
$$

展开 $M^2$：

$$
\langle M^2\rangle-\langle M\rangle^2
=
\sum_{ij}
\left(
\langle s_is_j\rangle-\langle s_i\rangle\langle s_j\rangle
\right).
$$

若体系平移不变，令 $r=j-i$，得到

$$
\chi
=
\beta
\sum_r G_c(r).
$$

连续极限下就是

$$
\chi
\sim
\int d^dr\,G_c(r).
$$

这条公式非常重要：磁化率不是一个孤立定义，它本质上是所有空间关联的总和。关联函数衰减越慢，$\chi$ 越容易变大；临界点处相关长度发散，$\chi$ 因此发散。

## 结构因子和动量空间

关联函数的 Fourier 变换是结构因子或动量空间 susceptibility：

$$
\chi(k)
=
\sum_r e^{ikr}G_c(r).
$$

特别地，

$$
\chi(0)=\sum_rG_c(r)
$$

就是均匀磁化率。若相变发生在非零 ordering wavevector $Q$，例如反铁磁序，则应该看

$$
\chi(Q)=\sum_r e^{iQr}G_c(r).
$$

所以 Monte Carlo 中常测的 structure factor

$$
S(k)=\frac1V\left\langle
\left|
\sum_j e^{ik r_j}s_j
\right|^2
\right\rangle
$$

本质上也是关联函数的 Fourier 变换。实空间和动量空间只是同一件事的两种表示。

## 高温相

普通短程模型的高温相中，关联函数有有限相关长度：

$$
G_c(r)
\sim
\frac{e^{-r/\xi}}{r^{(d-1)/2}}
$$

或粗略写成

$$
G_c(r)\sim e^{-r/\xi}.
$$

因为 $\xi$ 有限，积分

$$
\chi\sim \int d^dr\,G_c(r)
$$

也是有限的。动量空间中常用 Ornstein-Zernike 形式：

$$
\chi(k)
\sim
\frac{1}{k^2+\xi^{-2}}.
$$

这说明 $\xi^{-1}$ 就是动量空间峰宽。越接近临界点，$\xi$ 越大，$\chi(k)$ 在 $k=0$ 或 $Q$ 附近越尖。

## 普通二级相变

临界点处相关长度发散：

$$
\xi\to\infty.
$$

短程临界点的连通关联函数通常写成

$$
G_c(r)
\sim
\frac{1}{r^{d-2+\eta}}.
$$

把它代入磁化率积分，并用有限系统尺寸 $L$ 作为红外截断：

$$
\chi(L)
\sim
\int_a^L dr\,r^{d-1}
\frac{1}{r^{d-2+\eta}}.
$$

积分化简为

$$
\chi(L)
\sim
\int_a^L dr\,r^{1-\eta}
\sim
L^{2-\eta}.
$$

这就是有限尺寸标度里常见的关系：

$$
\boxed{\chi(T_c,L)\sim L^{2-\eta}.}
$$

若用 RG 指数 $y_h$ 写，磁化率也满足

$$
\chi\sim L^{2y_h-d}.
$$

比较两式得到

$$
2y_h-d=2-\eta,
\qquad
y_h=\frac{d+2-\eta}{2}.
$$

所以 $\eta$ 可以从实空间关联函数读出，也可以从 $\chi$ 的有限尺寸增长读出。

## 低温有序相

离散对称性破缺的低温相，例如 Ising 铁磁相，有

$$
G(r)\to m^2.
$$

连通关联函数通常仍然指数衰减：

$$
G_c(r)=G(r)-m^2\sim e^{-r/\xi}.
$$

因此低温相中的巨大 $S(0)$ 或 $M^2$ 主要来自 $m^2$ 平台，而不是临界涨落。做数据分析时要分清：

$$
\langle M^2\rangle
\quad\text{和}\quad
\langle M^2\rangle-\langle M\rangle^2
$$

所代表的物理不同。

连续对称性破缺的低温相则会出现 Goldstone mode。以 $O(N)$ 模型为例，横向涨落的低动量传播子为

$$
G(k)\sim \frac1{k^2}.
$$

回到实空间，对连通关联函数给出

$$
G_c(r)\sim \frac1{r^{d-2}}
\qquad (d>2).
$$

所以三维 XY 或 Heisenberg 低温相即使已经有真正长程序，连通关联函数仍然可能有幂律尾巴。这和 Ising 低温相很不一样。

## BKT 相变

二维 XY 模型的低温相没有真正长程序：

$$
\langle e^{i\theta}\rangle=0.
$$

但它也不是普通高温无序相。低温 BKT 相中，关联函数代数衰减：

$$
G(r)
=
\left\langle
e^{i[\theta(r)-\theta(0)]}
\right\rangle
\sim
r^{-\eta(T)}.
$$

于是有限系统中的 susceptibility 变成

$$
\chi(L)
\sim
\int_a^L dr\,r^{d-1}r^{-\eta(T)}.
$$

在 $d=2$ 中：

$$
\chi(L)\sim L^{2-\eta(T)}.
$$

BKT 转变点处有著名结果

$$
\eta(T_{\rm BKT})=\frac14,
$$

因此

$$
\chi(L,T_{\rm BKT})\sim L^{7/4}
$$

并带有对数修正。低温侧 $\eta(T)$ 随温度连续变化，这是 BKT 相变和普通二级相变的重要差别。

## 长程模型中的裸尾巴

若哈密顿量本身含有长程耦合

$$
J(r)\sim \frac1{r^{d+\sigma}},
$$

那么关联函数可能继承一个“裸长程尾巴”：

$$
G_c(r)\supset \frac{A(T)}{r^{d+\sigma}}.
$$

高温展开的第一阶已经能看出这一点：

$$
G(r)\approx \beta J(r)
\sim
\frac{\beta}{r^{d+\sigma}}.
$$

这意味着长程模型的高温相最终远距离衰减也可能是幂律。但这不自动表示高温相是临界相，因为

$$
\chi\sim
\int^\infty dr\,r^{d-1}r^{-(d+\sigma)}
=
\int^\infty dr\,r^{-1-\sigma}
$$

对 $\sigma>0$ 仍然收敛。

在临界点，如果集体涨落给出更慢的衰减

$$
G_c(r)\sim r^{-(d-2+\eta)},
$$

它会主导 leading behavior；裸尾巴通常退为 subleading correction。长程 fixed point 的常见 Gaussian 图像给

$$
\eta_{\rm LR}=2-\sigma,
$$

因此

$$
G_c(r)\sim r^{-(d-\sigma)},
$$

这比 $r^{-(d+\sigma)}$ 衰减慢得多。

## 量子模型中的关联函数和响应

量子模型中，两点函数通常变成虚时格林函数：

$$
G(r,\tau)
=
\langle
\mathcal T_\tau
O(r,\tau)O(0,0)
\rangle.
$$

静态响应常由空间和虚时积分给出：

$$
\chi
\sim
\int_0^\beta d\tau
\sum_r
\langle O(r,\tau)O(0,0)\rangle_c.
$$

这和经典公式

$$
\chi\sim \sum_rG_c(r)
$$

是同一条逻辑的量子版本。线性响应理论中的 Kubo 公式进一步说明：外场对某个观测量的线性响应，可以用相应算符的时间关联函数表示。实频响应函数、谱函数和输运系数都建立在这套关联函数语言上。

因此在量子 Monte Carlo 中，测量 Green 函数、虚时关联函数、结构因子和 winding number，不是附加技术细节，而是把采样结果转化为响应函数和低能物理的主要入口。

## 小结

关联函数范式可以压缩为几句话：

第一，$\chi$ 是连通关联函数的积分：

$$
\chi\sim \int d^dr\,G_c(r).
$$

第二，结构因子是关联函数的 Fourier 变换：

$$
\chi(k)=\sum_r e^{ikr}G_c(r).
$$

第三，临界点处

$$
G_c(r)\sim r^{-(d-2+\eta)}
$$

直接推出

$$
\chi(L)\sim L^{2-\eta}.
$$

第四，不同相的区别可以先从 $G_c(r)$ 的衰减方式读出：高温指数衰减、普通临界幂律衰减、离散有序相有平台加连通短程涨落、连续有序相有 Goldstone 尾巴、BKT 相有温度依赖的代数衰减、长程模型还可能有裸长程背景尾巴。
