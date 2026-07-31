# Mermin-Wagner 定理

Mermin-Wagner 定理说明了低维系统中连续对称性和长程有序之间的张力。它最常见的表述是：

> 对于具有短程相互作用、连续对称性的体系，在 $d\le 2$ 维、有限温度下，连续对称性不能自发破缺。

更具体地说，二维各向同性 Heisenberg 模型、二维连续 $O(N)$ 模型、二维 Bose 系统中的全局 $U(1)$ 对称性，都不能在有限温度下出现真正的连续对称性破缺长程序。这个结论背后的物理原因是：低维系统里的长波 Goldstone 模涨落太强，会把试图形成的有序方向冲散。

它不排除所有相变。二维 Ising 模型可以有有限温相变，因为 Ising 是离散 $\mathbb Z_2$ 对称性；二维 XY 模型可以有 BKT 相变，因为低温相没有真正长程序，而是准长程序。

## Goldstone 模的物理图像

Mermin-Wagner 定理的直观核心是 Goldstone 模。若一个连续全局对称性发生自发破缺，基态不是孤立的一个点，而是一整族连续等价的方向。系统可以沿着这族等价方向缓慢转动，几乎不需要能量。这个软方向对应的低能激发就是 Goldstone 模。

以 XY 模型为例，低温下局域自旋方向可以写成角度场

$$
\theta(x).
$$

整体把所有角度同时平移

$$
\theta(x)\to\theta(x)+\theta_0
$$

不改变能量。若角度只在空间中非常缓慢地变化，能量代价来自梯度：

$$
H_{\rm sw}
\simeq
\frac{\rho_s}{2}
\int d^dx\,(\nabla\theta)^2.
$$

因此长波模式的能量随动量 $k$ 变小而迅速降低。傅里叶空间中，每个模式的涨落量级为

$$
\langle |\theta_k|^2\rangle
\sim
\frac{T}{\rho_s k^2}.
$$

这说明 $k\to0$ 的模式非常容易被热涨落激发。维度越低，小 $k$ 模式的相空间越少，但每个模式的涨落越强；二者竞争后，红外积分

$$
\int\frac{d^dk}{k^2}
$$

在 $d\le2$ 发散。也就是说，试图建立的全局有序方向会被长波角度涨落不断扭曲，最终无法在热力学极限中保持非零磁化。

这个图像也解释了为什么离散对称性不同。Ising 低温相只有两个离散真空，不能在两个真空之间做任意小的连续转动。低能涨落不是无质量的角度波，而是 domain wall 或局域翻转，通常有有限能量代价。因此二维 Ising 不受 Mermin-Wagner 定理限制，可以有真正长程序。

## Goldstone 与 Higgs 的一句区分

有时会听到 Goldstone 模和 Higgs 机制一起出现。这里需要区分全局对称性和局域规范对称性。

对 **连续全局对称性**，自发破缺会产生独立的无质量 Goldstone 模。例如普通 XY 或 Heisenberg 磁体的低温自旋波，就是这种意义下的软模式。

对 **局域规范对称性**，情况不同。Goldstone 自由度会被规范场吸收，成为规范场的纵向分量，使规范玻色子获得质量；剩下的振幅方向可能对应 Higgs 模。严格说，不是 Goldstone 模“自己变重”，而是它不再作为独立低能激发出现。

本节讨论的 Mermin-Wagner 定理针对的是短程相互作用、低维、连续 **全局** 对称性体系。因此这里真正起作用的是无质量 Goldstone 模带来的红外涨落。

## 3D XY 与 3D Ising 的低温关联函数

三维中，连续对称性可以在有限温下自发破缺，因为

$$
\int\frac{d^3k}{k^2}
$$

在红外端不发散。此时 XY 和 Ising 都可以有低温长程序，但它们的连通关联函数仍然不同。

对 3D XY 低温相，完整关联函数趋向于有序分量：

$$
G(r)=\langle \mathbf S(r)\cdot\mathbf S(0)\rangle
\to m^2.
$$

减去常数背景后，连通关联函数仍会有 Goldstone 模带来的幂律尾巴：

$$
G_c(r)
=G(r)-m^2
\sim
\frac{1}{r^{d-2}}
=
\frac{1}{r}
\qquad (d=3).
$$

动量空间中对应

$$
\chi_k\sim \frac{1}{k^2},
\qquad k\to0.
$$

有限尺寸系统中最小非零动量 $k_{\min}\sim 2\pi/L$，所以低温 Goldstone 模会使最低动量响应出现

$$
\chi_{k_{\min}}\sim L^2
$$

这样的强尺寸依赖。

对 3D Ising 低温相，离散对称性破缺后没有 Goldstone 模。连通关联函数一般是指数衰减：

$$
G_c(r)\sim
\frac{e^{-r/\xi}}{r^{(d-1)/2}}
$$

或在粗略讨论中写作指数衰减。它同样有

$$
G(r)\to m^2,
$$

但减去 $m^2$ 后没有连续对称性带来的长程幂律尾巴。

这点对 Monte Carlo 很实用。若低温相有连续对称性，看到小动量结构因子或低 $k$ susceptibility 随 $L$ 明显增长，并不一定表示还在临界点；它可能只是 Goldstone 模的普通低温效应。离散对称性模型中，这类低温红外增强通常不会以同样方式出现。

## 从随机行走回返看低维涨落

还有一个有用的直觉：Mermin-Wagner 定理中的红外发散，和随机行走在低维中容易回返有关。

普通随机行走在 $d=1,2$ 中是 recurrent 的：它会不断回到原点附近；在 $d\ge3$ 中是 transient 的：它有非零概率远离原点而不再回来。这个事实和格林函数

$$
G(r)
\sim
\int\frac{d^dk}{(2\pi)^d}
\frac{e^{ik\cdot r}}{k^2}
$$

的红外性质密切相关。

自旋波传播子也是 $1/k^2$。当低维随机行走反复回访同一区域时，可以直观理解为低维空间不足以“稀释”长波涨落；涨落不断累积，最终破坏连续长程序。高维中随机行走更容易逃逸，长波涨落的累计效应较弱，因此连续对称性破缺可以稳定存在。

这个类比不是严格证明，但非常有助于记忆维度边界：短程连续对称性在 $d\le2$ 被强红外涨落破坏，而在 $d>2$ 可以形成真正长程序。

## 定理说的是什么

考虑一个具有连续对称性的序参量，例如

$$
\mathbf m
=
\frac1V\int d^dx\,\boldsymbol\phi(x),
$$

其中 $\boldsymbol\phi$ 是 $O(N)$ 向量场。若连续对称性自发破缺，在热力学极限中应该存在

$$
\lim_{h\to0^+}\lim_{V\to\infty}
\langle \mathbf m\rangle_h
\ne 0.
$$

这里 $h$ 是用来选定方向的外场。Mermin-Wagner 定理说，在 $d\le2$ 的短程相互作用系统中，上式对连续对称性不成立：

$$
\lim_{h\to0^+}\lim_{V\to\infty}
\langle \mathbf m\rangle_h
=0.
$$

核心机制来自长波涨落。低维中，小动量模式的积分

$$
\int \frac{d^dk}{k^2}
$$

在红外端发散。这个发散正是定理的关键。

## 经典版本的物理证明

先看最直观的经典版本。以二维 XY 模型为例：

$$
H=-J\sum_{\langle ij\rangle}
\cos(\theta_i-\theta_j).
$$

低温下相邻角度差较小，可以展开为 spin-wave 理论：

$$
H_{\rm sw}
\simeq
\frac{\rho_s}{2}
\int d^dx\,(\nabla\theta)^2.
$$

这里 $\rho_s$ 是 stiffness。傅里叶变换后：

$$
\theta(x)
=
\frac1{\sqrt V}\sum_k \theta_k e^{ikx},
$$

哈密顿量变成

$$
H_{\rm sw}
=
\frac{\rho_s}{2}\sum_k k^2|\theta_k|^2.
$$

由能均分或高斯积分可得

$$
\langle |\theta_k|^2\rangle
=
\frac{T}{\rho_s k^2}.
$$

这说明长波模式 $k\to0$ 的角度涨落非常大。

真正决定有序的是角度差的涨落：

$$
\langle [\theta(x)-\theta(0)]^2\rangle
=
\frac{2T}{\rho_s}
\int\frac{d^dk}{(2\pi)^d}
\frac{1-\cos(kx)}{k^2}.
$$

在 $d=1$ 中，这个积分随距离线性增长：

$$
\langle [\theta(x)-\theta(0)]^2\rangle
\sim
\frac{T}{\rho_s}|x|.
$$

在 $d=2$ 中，它对数增长：

$$
\langle [\theta(x)-\theta(0)]^2\rangle
\sim
\frac{T}{\pi\rho_s}\ln\frac{|x|}{a}.
$$

若序参量写为

$$
S^+(x)=e^{i\theta(x)},
$$

那么高斯变量给出

$$
\left\langle
e^{i[\theta(x)-\theta(0)]}
\right\rangle
=
\exp\left[
-\frac12
\langle [\theta(x)-\theta(0)]^2\rangle
\right].
$$

因此：

- 在 $d=1$，关联函数指数衰减。
- 在 $d=2$，spin-wave 理论给出代数衰减。

二维中具体为

$$
\langle S^+(x)S^-(0)\rangle
\sim
\left(\frac{a}{|x|}\right)^\eta,
$$

其中

$$
\eta=\frac{T}{2\pi\rho_s}.
$$

代数衰减意味着没有真正的常数长程极限：

$$
\lim_{|x|\to\infty}
\langle S^+(x)S^-(0)\rangle
=0.
$$

这就排除了

$$
\langle S^+\rangle\ne0.
$$

这个推导非常有启发性：先假设低温存在一个有序方向，然后研究围绕该方向的 Goldstone 涨落，最后发现低维中的长波涨落发散，导致有序本身不自洽。

## 一般连续对称模型的经典图像

这里讨论一般 $O(N)$ 模型的经典图像。

对 $O(N)$ 模型，若自发选择某个方向，可以把场写成纵向分量和横向 Goldstone 模：

$$
\boldsymbol\phi(x)
\simeq
\left(
\pi_1(x),\cdots,\pi_{N-1}(x),
\sqrt{m^2-\boldsymbol\pi^2(x)}
\right).
$$

低能有效哈密顿量为

$$
H_{\rm sw}
=
\frac{\rho_s}{2}
\int d^dx
\sum_{a=1}^{N-1}
(\nabla \pi_a)^2.
$$

每个横向 Goldstone 模都有传播子

$$
\langle |\pi_a(k)|^2\rangle
\sim
\frac{T}{\rho_s k^2}.
$$

横向涨落总量为

$$
\langle \boldsymbol\pi^2\rangle
\sim
(N-1)\frac{T}{\rho_s}
\int\frac{d^dk}{(2\pi)^d}\frac1{k^2}.
$$

红外积分在 $d\le2$ 发散。若横向涨落无限大，原先假设的固定有序方向就会被破坏。因此短程连续对称性不能在低维有限温下真正自发破缺。

## Bogoliubov 不等式的证明骨架

上面的 spin-wave 推导给出物理图像。更严格的证明常用 Bogoliubov 不等式。量子形式可以写为

$$
\frac12
\langle \{A,A^\dagger\}\rangle
\,
\langle [[C,H],C^\dagger]\rangle
\ge
T
\left|
\langle [C,A]\rangle
\right|^2.
$$

这里 $A,C$ 是可选择的算符，$T$ 是温度。经典系统中也有对应的泊松括号版本。证明的思想是利用 Cauchy-Schwarz 不等式，把某个序参量和长波涨落联系起来。

以 Heisenberg 磁体为例，哈密顿量可写为

$$
H
=
-\sum_{ij}J_{ij}\mathbf S_i\cdot\mathbf S_j
-h\sum_i S_i^z.
$$

选择 Fourier 分量

$$
S_k^\alpha
=
\sum_j e^{ik r_j}S_j^\alpha.
$$

合适地取

$$
C=S_k^+,
\qquad
A=S_{-k}^-,
$$

或针对反铁磁序选择带 ordering wavevector 的版本，可以让交换子

$$
\langle [C,A]\rangle
$$

与磁化或交错磁化成正比。

另一方面，双交换子

$$
\langle [[C,H],C^\dagger]\rangle
$$

在小 $k$ 下由短程交换相互作用给出

$$
\langle [[C,H],C^\dagger]\rangle
\lesssim
{\rm const}\times k^2
+{\rm const}\times h.
$$

于是 Bogoliubov 不等式会给出类似约束：

$$
m^2
\lesssim
\frac{1}
{
\frac1V\sum_k
\frac1{k^2+h}
}.
$$

当 $d\le2$，热力学极限中

$$
\frac1V\sum_k\frac1{k^2+h}
\to
\int\frac{d^dk}{(2\pi)^d}\frac1{k^2+h}
$$

在 $h\to0$ 时红外发散。因此右边趋于零，得到

$$
m=0.
$$

这个推导的关键细节是：短程相互作用使双交换子在小 $k$ 下最多像 $k^2$；连续对称性使序参量和横向长波模耦合；低维中的 $1/k^2$ 积分发散。

## 量子版本

量子 Mermin-Wagner 定理说：对于具有连续对称性和足够短程相互作用的量子自旋或玻色体系，在 $d\le2$ 维、有限温度下，不能自发破缺连续对称性。

量子版本和经典版本的区别在于：

- 经典证明直接研究热涨落。
- 量子证明要处理非对易算符，因此常用 Bogoliubov 不等式、Duhamel 内积或反射正性等工具。

但红外机制相同。有限温量子系统在长波、低频区域仍会有强烈的横向涨落。Bogoliubov 不等式把假设的磁化强度 $m$ 与低动量求和联系起来：

$$
m^2
\int\frac{d^dk}{(2\pi)^d}
\frac1{k^2+h}
\le
{\rm const}.
$$

当 $d\le2$ 且 $h\to0$ 时，积分发散，所以

$$
m=0.
$$

这说明有限温二维量子 Heisenberg 模型不能有真正的自发磁化或 Néel 长程序。需要注意，量子系统在 $T=0$ 时等价于多一个虚时方向的量子临界问题，因此二维量子 Heisenberg 反铁磁体可以在零温有 Néel 序；这不违反定理，因为定理限制的是有限温。

## 不适用和容易误解的情况

Mermin-Wagner 定理有明确适用条件，下面几类情况需要分开看。

第一，离散对称性不受限制。二维 Ising 模型只有 $\mathbb Z_2$ 对称性，没有 Goldstone 模，因此可以在有限温发生普通二阶相变。

第二，长程相互作用可能绕开定理。若相互作用衰减太慢，小 $k$ 下的刚度不再给出简单 $k^2$ 行为，红外积分结构会改变。

第三，有限尺寸系统可以看起来有序。Monte Carlo 中若 $L$ 不够大，相关长度可能超过系统尺寸，观测量会显示很强的有序迹象。定理讨论的是热力学极限。

第四，二维 XY 模型低温相有准长程序：

$$
\langle S^+(r)S^-(0)\rangle\sim r^{-\eta}.
$$

它没有真正的

$$
\langle S^+\rangle\ne0,
$$

但关联函数也不是指数衰减。这正是 BKT 相变的入口。

## 长程相互作用版本

短程条件是 Mermin-Wagner 定理的关键。更一般地，证明常要求交换相互作用的二阶矩足够好，例如有类似

$$
\sum_r |J(r)|\,r^2<\infty
$$

的收敛条件。这个条件保证小动量展开仍然由 $k^2$ 控制，从而保留

$$
\int\frac{d^dk}{k^2}
$$

这个红外发散结构。

若相互作用是幂律衰减：

$$
J(r)\sim \frac1{r^\alpha},
$$

情况会变得更细。$\alpha$ 越大，相互作用越接近短程；$\alpha$ 越小，远距离耦合越强，长波涨落越容易被压制。Patrick Bruno 对一维和二维 Heisenberg/XY 系统给出了强化版本：对单调递减相互作用，若

$$
\alpha\ge 2D,
$$

则有限温铁磁或反铁磁长程序仍被排除；对振荡相互作用，还有不同的阈值条件。

若用长程统计物理里常见记号

$$
J(r)\sim \frac1{r^{d+\sigma}},
$$

则 $\alpha=d+\sigma$。Bruno 的单调情形条件 $\alpha\ge2D$ 在 $D=d$ 时对应

$$
\sigma\ge d.
$$

这和自旋波红外积分

$$
\int\frac{d^dk}{k^\sigma}
$$

给出的直觉边界一致：当 $\sigma\ge d$ 时，红外涨落仍然足够强，可以摧毁连续长程序；当 $\sigma<d$ 时，定理不再排除长程序，具体是否有序要看模型和缺陷物理。

因此更准确的说法是：

- 短程二维连续对称性：有限温不能真正自发破缺。
- 衰减足够快的长程相互作用：仍可能满足 Mermin-Wagner 型排除结论。
- 衰减足够慢的长程相互作用：定理的红外发散条件失效，低维连续对称性长程序可能出现。

这也是长程模型有趣的原因之一。它们不是简单地给短程模型加一个微扰尾巴，而是可能改变低动量传播子、红外涨落强度和相变类型。

## 小结

Mermin-Wagner 定理可以浓缩为一句话：

> 低维短程系统中，连续对称性一旦试图自发破缺，就会产生无质量 Goldstone 模；这些长波模在 $d\le2$ 的热涨落红外发散，从而摧毁真正长程序。

经典 spin-wave 证明展示了物理机制；Bogoliubov 不等式给出更严格的控制；量子版本说明这个结论对有限温低维量子系统同样成立。
