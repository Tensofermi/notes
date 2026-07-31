# 有限尺寸标度

Monte Carlo 模拟只能处理有限系统。临界现象真正关心的是热力学极限

$$
L\to\infty,
$$

因此需要一套方法，把不同尺寸 $L$ 的数据组织成临界点、临界指数和普适函数的信息。有限尺寸标度的核心思想很简单：

> 有限系统中，系统尺寸 $L$ 会截断相关长度 $\xi$ 的发散。

所以临界附近的观测量不只依赖温度偏离量 $t$，还依赖

$$
\frac{L}{\xi}.
$$

RG 给出这句话的精确形式。

## 相关长度与有限尺寸

连续相变附近，相关长度满足

$$
\xi(t)\sim |t|^{-\nu},
$$

其中

$$
t=\frac{T-T_c}{T_c}
$$

是约化温度。热力学极限中，当 $t\to0$ 时，

$$
\xi\to\infty.
$$

有限系统中，$\xi$ 不可能无限增长。只要

$$
\xi(t)\gtrsim L,
$$

系统就已经感受到边界和有限尺寸。有限系统真正能分辨的临界区域大约由

$$
\xi(t)\sim L
$$

决定。代入 $\xi\sim |t|^{-\nu}$，得到

$$
|t|\sim L^{-1/\nu}.
$$

所以不同尺寸的临界窗口宽度不同。系统越大，能看到的临界区域越窄。

## RG 图像

重整化群的核心步骤是：

1. 把短距离自由度粗粒化。
2. 重新定义长度单位。
3. 观察耦合参数如何流动。

对有限尺寸系统来说，若做尺度因子为 $b$ 的 RG，线性尺寸变为

$$
L\to L'=\frac{L}{b}.
$$

格点数从

$$
L^d
$$

变成

$$
\left(\frac{L}{b}\right)^d.
$$

一个粗粒化格点代表原来的

$$
b^d
$$

个微观格点。例如二维 $8\times8$ 格子取 $b=2$，粗粒化后变成 $4\times4$ 格子，自由度数减少四倍。

这里要分清主动和被动两种视角。主动地看，block spin 使格点间距变大：

$$
a\to a'=ba.
$$

被动地看，我们用粗粒化后的坐标系重新描述同一段长度：

$$
x\to x'=\frac{x}{b},
\qquad
x=bx'.
$$

二者讲的是同一个 RG 过程，只是强调不同：

| 说法 | 数学写法 | 直觉 |
| --- | --- | --- |
| 格点间距变大 | $a'=ba$ | 一个新格点代表 $b$ 个旧格点的线性长度 |
| 坐标缩小 | $x'=x/b$ | 原来长度为 $b$ 的距离，在新坐标里记作 $1$ |
| 重新归一化 | 把 $a'$ 再记作 $a$ | 让粗粒化后的模型可以和原模型比较 |

因此 $8\times8\to4\times4$ 是自由度数的变化；$x'=x/b$ 是坐标单位的重新计量。

## 参数为什么也要缩放

空间变换会诱导 coupling 的变换。温度偏离量 $t$ 控制相关长度：

$$
\xi(t)\sim |t|^{-\nu}.
$$

做 RG 后，长度在新坐标中缩小 $b$ 倍：

$$
\xi'=\frac{\xi}{b}.
$$

粗粒化后的系统仍然应满足同样的相关长度形式：

$$
\xi(t')\sim |t'|^{-\nu}.
$$

于是要求

$$
\xi(t')=\frac{\xi(t)}{b}.
$$

代入幂律形式：

$$
|t'|^{-\nu}
=
\frac{|t|^{-\nu}}{b}.
$$

因此

$$
t'=tb^{1/\nu}.
$$

所以

$$
\boxed{y_t=\frac1\nu}.
$$

这说明

$$
t\to tb^{y_t}
$$

和

$$
x\to \frac{x}{b}
$$

是直接关联的：前者是空间尺度变换诱导出的温度 scaling field 变换。临界点 $t=0$ 在 RG 下仍然满足 $t'=0$，因此它是固定点；只要 $t\ne0$，若 $y_t>0$，多次 RG 后

$$
t_n=t b^{ny_t}
$$

会越来越大，系统就离开临界固定点。

磁场同理：

$$
h\to hb^{y_h}.
$$

在 LGW 语言里，$t$ 是 $\phi^2$ 算符的 coupling，$h$ 是 $\phi$ 算符的 coupling。更一般地，若

$$
\delta\mathcal H
=
g\int d^dx\,\mathcal O(x),
$$

且 $\mathcal O$ 的 scaling dimension 是 $\Delta_{\mathcal O}$，则

$$
g'=g b^{d-\Delta_{\mathcal O}}.
$$

因此

$$
y_g=d-\Delta_{\mathcal O}.
$$

这就是 relevant、irrelevant 和 marginal 的来源：

- $y_g>0$：扰动在大尺度下放大，是 relevant。
- $y_g<0$：扰动在大尺度下衰减，是 irrelevant。
- $y_g=0$：扰动为 marginal，需要看更高阶流方程。

## 自由能的有限尺寸标度

临界理论中，更精确的写法要区分解析背景和奇异部分：

$$
f(t,h,\{u_i\},L)
=
f_a(t,h,\{u_i\},L)
+
f_s(t,h,\{u_i\},L).
$$

其中 $f_a$ 是 regular analytic background，$f_s$ 是临界奇异部分，$\{u_i\}$ 表示 irrelevant scaling fields。RG 标度形式为

$$
\boxed{
f_s(t,h,\{u_i\},L)
=
b^{-d}
f_s(tb^{y_t},hb^{y_h},\{u_i b^{y_i}\},L/b).
}
$$

这里

$$
y_t>0,\qquad y_h>0,
$$

而 irrelevant fields 满足

$$
y_i<0.
$$

前面的 $b^{-d}$ 来自体积密度。用坐标变换写：

$$
x'=\frac{x}{b},
\qquad
d^dx'=b^{-d}d^dx.
$$

自由能密度是每单位体积的量，所以它要带上这个体积因子。

有限尺寸标度的关键一步是取

$$
b=L.
$$

这相当于把整个有限系统缩放成单位大小：

$$
\frac{L}{b}=1.
$$

于是

$$
\boxed{
f_s(t,h,\{u_i\},L)
=
L^{-d}
\mathcal F(tL^{y_t},hL^{y_h},\{u_iL^{y_i}\}).
}
$$

这就是有限尺寸标度的母公式。它说明有限系统中所有临界奇异性都应当通过无量纲组合

$$
tL^{y_t},\qquad hL^{y_h},\qquad u_iL^{y_i}
$$

进入。

特别地，

$$
tL^{y_t}
$$

表示温度偏离量在系统尺度 $L$ 上的有效强度。若

$$
tL^{y_t}\ll1,
$$

系统在尺寸 $L$ 内仍然看起来接近临界；若

$$
tL^{y_t}\gg1,
$$

系统在达到尺度 $L$ 之前已经明显偏离临界点。

## 从有限尺寸标度回到热力学极限

自由能标度形式不仅能描述有限系统，也能推出热力学极限中的奇异性。先忽略外场和 irrelevant fields，写成

$$
f_s(t,L)
=
L^{-d}\mathcal F(tL^{y_t}).
$$

令

$$
x=tL^{y_t}.
$$

在热力学极限中，取 $L\to\infty$ 且固定 $t\ne0$，则

$$
x\to\infty.
$$

这时有限尺寸自由能密度应当趋向只依赖 $t$、不再依赖 $L$ 的热力学极限：

$$
f_s(t,L)\to f_s(t).
$$

因此 $L^{-d}\mathcal F(tL^{y_t})$ 中显式的 $L$ 必须被标度函数的大参数行为抵消。若假设

$$
\mathcal F(x)\sim x^p,\qquad x\to\infty,
$$

则

$$
f_s(t,L)
\sim
L^{-d}(tL^{y_t})^p
=
t^p L^{-d+py_t}.
$$

为了让热力学极限不依赖 $L$，需要

$$
-d+py_t=0.
$$

所以

$$
p=\frac{d}{y_t},
$$

从而得到

$$
\boxed{
f_s(t)\sim |t|^{d/y_t}.
}
$$

这个关系就是 hyperscaling 的一种写法。因为 $y_t=1/\nu$，它也常写成

$$
f_s(t)\sim \xi^{-d}\sim |t|^{d\nu}.
$$

能量密度是自由能密度对温度变量的一阶导数，因此奇异部分满足

$$
e_s(t)
\sim
\frac{\partial f_s}{\partial t}
\sim
|t|^{d/y_t-1}.
$$

如果

$$
y_t>d,
$$

那么

$$
\frac{d}{y_t}-1<0,
$$

能量密度的奇异部分会在 $t\to0$ 时发散。对普通局域统计模型，这通常不是连续相变中期望出现的行为，因为能量密度是每个格点局域能量的平均。连续相变中比热可以发散，但能量密度本身通常仍然有限。

同一个结论也可以直接从有限尺寸形式看出。对 $t$ 求导：

$$
e_s(t,L)
=
\frac{\partial f_s(t,L)}{\partial t}
=
L^{-d+y_t}\mathcal F'(tL^{y_t}).
$$

在临界点 $t=0$，

$$
e_s(0,L)\sim L^{y_t-d}.
$$

因此：

| 情况 | $e_s(0,L)$ 的行为 | 解释 |
| --- | --- | --- |
| $y_t<d$ | $L^{y_t-d}\to0$ | 普通连续相变，能量密度的奇异部分不发散 |
| $y_t=d$ | $O(1)$ | 一级相变的体积型有限尺寸标度，能量密度可以有跃变 |
| $y_t>d$ | 随 $L$ 发散 | 对普通局域模型通常不合理 |

这里要注意两个限制。

第一，上述推导依赖普通 hyperscaling，也就是奇异自由能密度由相关体积控制：

$$
f_s\sim \xi^{-d}.
$$

在上临界维度以上，dangerously irrelevant variable 会破坏简单 hyperscaling。因此不能直接用这段推导判断高维 PBC 零模标度中的所有有效指数。

第二，BKT 相变不属于普通幂律相关长度发散。BKT 中

$$
\xi(t)
\sim
\exp\left(\frac{c}{\sqrt{|t|}}\right),
$$

不能简单写成 $tL^{y_t}$ 并取一个有限的 $y_t$。若硬要用 $y_t=1/\nu$ 类比，则 $\nu=\infty$，等效为

$$
y_t=0.
$$

更自然的有限尺寸形式是

$$
f_s(t,L)
=
L^{-d}\mathcal G\left(\frac{L}{\xi(t)}\right).
$$

## 常见观测量的标度

从自由能对外场求导，可以得到磁化和磁化率的标度。磁化为

$$
m=-\frac{\partial f_s}{\partial h}.
$$

由自由能标度可得

$$
m(t,L)
=
L^{-d+y_h}
f_m(tL^{y_t}).
$$

利用

$$
\frac{\beta}{\nu}=d-y_h,
\qquad
y_t=\frac1\nu,
$$

写成常见形式：

$$
\boxed{
m(t,L)=L^{-\beta/\nu}f_m(tL^{1/\nu}).
}
$$

磁化率为

$$
\chi=\frac{\partial m}{\partial h}
=
-\frac{\partial^2 f_s}{\partial h^2}.
$$

因此

$$
\chi(t,L)
=
L^{-d+2y_h}
f_\chi(tL^{y_t}).
$$

也就是

$$
\boxed{
\chi(t,L)=L^{\gamma/\nu}f_\chi(tL^{1/\nu}).
}
$$

比热来自对温度变量的二阶导数：

$$
C\sim \frac{\partial^2 f_s}{\partial t^2},
$$

所以

$$
\boxed{
C(t,L)=L^{\alpha/\nu}f_C(tL^{1/\nu}).
}
$$

在临界点 $t=0$，这些式子退化为幂律：

$$
m(0,L)\sim L^{-\beta/\nu},
$$

$$
\chi(0,L)\sim L^{\gamma/\nu},
$$

$$
C(0,L)\sim L^{\alpha/\nu}.
$$

这些临界点处的尺寸依赖，是 Monte Carlo 中估计指数比的常用方法。

## 无量纲量与交点

无量纲量在 FSS 中尤其重要，因为它们没有额外的 $L$ 幂次。典型例子包括：

- Binder ratio。
- 相关长度比 $\xi_L/L$。
- percolation 或 loop 模型中的 wrapping probability。

以 Ising 型序参量为例，Binder ratio 常写为

$$
U_4
=
1-\frac{\langle m^4\rangle}{3\langle m^2\rangle^2}.
$$

它的标度形式为

$$
U_4(t,L)
=
F_U(tL^{y_t},\{u_iL^{y_i}\}).
$$

若先忽略 irrelevant fields，则

$$
U_4(t,L)=F_U(tL^{1/\nu}).
$$

在临界点 $t=0$：

$$
U_4(0,L)=F_U(0),
$$

近似与 $L$ 无关。因此不同尺寸的 Binder ratio 曲线会在临界点附近相交。实际数据中交点会随尺寸漂移，这个漂移正是有限尺寸修正的表现。

wrapping probability 或 $\xi_L/L$ 也有类似结构：

$$
R(t,L)=F_R(tL^{y_t},\{u_iL^{y_i}\}).
$$

这类量常用于定位 $T_c$，因为它们不需要先知道 $\beta/\nu$ 或 $\gamma/\nu$。

## 上临界维度以上的有限尺寸标度

前面的有限尺寸标度默认系统由一个相互作用固定点控制，有限尺寸的主要作用是把相关长度截断在 $L$。在上临界维度以上，情况会更微妙。以短程 Ising 或 $\phi^4$ 理论为例，上临界维度是

$$
d_c=4.
$$

当 $d>4$ 时，四次耦合 $u$ 在 Gaussian 固定点下是 irrelevant：

$$
y_u=4-d<0.
$$

但它又不能简单丢掉。若直接令 $u=0$，Landau 自由能在临界点附近无法稳定零模。因此 $u$ 是一个 **dangerously irrelevant variable**：它在 RG 意义下无关，却会影响有限系统中磁化、磁化率等量的尺寸标度。

这会导致一个常见现象：高维周期边界系统中，零动量模像一个平均场自由度，给出体积控制的标度。Landau 零模自由能可粗略写成

$$
F_0(m)
\sim
L^d
\left(
\frac{t}{2}m^2+\frac{u}{4}m^4-hm
\right).
$$

在临界点 $t=0,h=0$，典型磁化涨落由

$$
L^d u m^4\sim 1
$$

估计，因此

$$
m\sim L^{-d/4}.
$$

于是磁化率

$$
\chi
=
L^d\langle m^2\rangle
$$

满足

$$
\chi\sim L^{d/2}.
$$

这个结果看起来不像普通的

$$
\chi\sim L^{\gamma/\nu}=L^2
$$

平均场标度。差别来自周期边界下零模的强有限尺寸效应。它不表示热力学极限中的平均场指数错了，而是说明在有限系统中，长度 $L$ 和体积 $L^d$ 可能以不同方式进入不同观测量。

因此上临界维度以上常会出现两套有用语言。

第一套是 Gaussian 固定点的长度标度：

$$
y_t=2,\qquad
y_h=\frac{d+2}{2}.
$$

它来自长波非零动量模式，常和关联函数、小动量结构因子、有限波矢涨落有关。

第二套是零模或完全图式的体积标度。若用有限系统体积控制临界涨落，可以得到有效组合

$$
tL^{d/2},
\qquad
hL^{3d/4},
$$

以及

$$
m\sim L^{-d/4},
\qquad
\chi\sim L^{d/2}.
$$

这两套描述并不是互相否定，而是在提醒我们：上临界维度以上，有限尺寸系统中不同观测量可能受不同尺度控制。特别是周期边界条件会让零模非常突出；自由边界或不同定义的有限尺寸关联长度可能表现出不同修正。

从 Monte Carlo 角度，这一点很实际。如果在 $d>4$ 的 Ising 模型或强长程平均场区间分析数据，不应机械套用低维形式

$$
Q(t,L)=F_Q(tL^{1/\nu}).
$$

需要先判断观测量主要看的是零模、非零动量涨落，还是几何 cluster。否则同一批数据可能看起来给出“两个不同的平均场指数”。

## 高维 PBC 的 FSS

上面的讨论说明，在上临界维度以上，PBC 系统不能只说“平均场指数”。更准确地说，高维周期边界系统同时包含两个平均场扇区：一个是 Gaussian fixed point, GFP，对应非零动量的空间涨落；另一个是 complete-graph, CG，对应周期盒子中的零动量模。它们都来自平均场思想，但控制的观测量不同。

这套 GFP+CG 图像本身已经足够指导有限尺寸分析。若回到 $\phi^4$ 的 RG 语言，CG 零模项的理论来源可以理解为 dangerous irrelevant variable：四次耦合 $u$ 在 $d>4$ 是 irrelevant，但它仍负责稳定零模自由能，因此不能在零模扇区简单设为零。也就是说，GFP+CG 是标度结构，dangerous irrelevant variable 是解释这个结构为什么出现的一种 RG 机制。

对 $d>d_c=4$ 的短程 Ising 普适类，可以把自由能密度写成两项：

$$
f(t,h,L)
=
L^{-d}
\tilde f_{\rm GF}
\left(
tL^2,
hL^{(d+2)/2}
\right)
+
L^{-d}
\tilde f_{\rm CG}
\left(
tL^{d/2},
hL^{3d/4}
\right).
$$

第一项含有 GFP 指数

$$
\left(
y_t^{\rm GF},y_h^{\rm GF}
\right)
=
\left(
2,\frac{d+2}{2}
\right),
$$

第二项含有 CG 指数

$$
\left(
y_t^{\rm CG},y_h^{\rm CG}
\right)
=
\left(
\frac d2,\frac{3d}{4}
\right).
$$

同样的 Ising 型 CG 指数也适用于上临界维度以上的短程 $O(n)$ 模型。对短程 percolation，则 CG 指数换成

$$
\left(
y_t^{\rm CG},y_h^{\rm CG}
\right)
=
\left(
\frac d3,\frac{2d}{3}
\right).
$$

这些指数可以整理为：

| 标度图像 | 典型场论 | 有效指数 | 主要控制的对象 |
| --- | --- | --- | --- |
| GFP / coarse-grained $\phi^4$ | Landau $\phi^4$ 的高斯部分 | $y_t^{\rm GF}=2,\ y_h^{\rm GF}=1+d/2$ | 非零动量模、短距离涨落、关于真实空间距离的几何 |
| CG-Ising / PBC 零模 $\phi^4$ | Landau $\phi^4$ 零模 | $y_t^{\rm CG}=d/2,\ y_h^{\rm CG}=3d/4$ | 磁化、磁化率、最大 FK-Ising cluster |
| CG-percolation | $\phi^3$ / percolation 平均场 | $y_t^{\rm CG}=d/3,\ y_h^{\rm CG}=2d/3$ | 普通高维 percolation 的最大 clusters 和 cutoff |

这里的 CG 指数不是新的热力学临界指数，而是 PBC 有限系统中由零模或 complete-graph 渐近行为诱导出的有限尺寸指数。它们仍然是平均场性质，但不是同一套平均场语言。

最容易混淆的是前两行。Gaussian 固定点给出长度量纲：

$$
y_t=2,\qquad y_h=\frac{d+2}{2}.
$$

它对应的是场论中

$$
G(k)\sim \frac{1}{k^2+t}
$$

这类非零动量涨落。PBC 零模则来自 Landau 自由能

$$
F_0(m)
\sim
L^d
\left(
\frac{t}{2}m^2+\frac{u}{4}m^4-hm
\right),
$$

在临界点由 $L^d u m^4\sim 1$ 得到

$$
m\sim L^{-d/4},
\qquad
\chi\sim L^{d/2}.
$$

如果仍把这些结果写成

$$
m\sim L^{y_h-d},
\qquad
\chi\sim L^{2y_h-d},
$$

就得到

$$
y_h^{\rm CG}=\frac{3d}{4}.
$$

温度方向同理来自 $tL^d m^2\sim 1$，给出

$$
y_t^{\rm CG}=\frac d2.
$$

所以在读高维 PBC 文献时，看到 $(2,1+d/2)$ 和 $(d/2,3d/4)$ 同时出现并不矛盾。前者是 GFP 的长度量纲，后者是 PBC 零模或 complete-graph Ising 的有限尺寸量纲。

### 两点关联函数的两项结构

这套两尺度图像也会反映在两点关联函数中。对 $d>4$ 的 Ising 型系统，临界附近可以粗略写成

$$
g(r,L)
\asymp
r^{2-d}\tilde g_{\rm GF}(r/L)
+
bL^{-d/2},
$$

其中 $b$ 是非普适振幅。第一项是普通 Gaussian 关联函数的空间衰减：

$$
g_{\rm GF}(r)\sim r^{2-d}.
$$

第二项是零模产生的 CG plateau。它与距离 $r$ 无关，因此在有限周期盒子中表现为一个很低但覆盖全系统的背景项。这个背景项单点看很小，但对磁化率这种对所有距离求和的量很重要：

$$
\chi
\sim
\sum_r g(r,L).
$$

GF 项给出的量级是

$$
\sum_{r\lesssim L} r^{2-d}
\sim
L^2,
$$

而 CG plateau 给出

$$
\sum_{r} L^{-d/2}
\sim
L^dL^{-d/2}
=
L^{d/2}.
$$

当 $d>4$ 时，$L^{d/2}$ 比 $L^2$ 增长更快，因此磁化率、磁化矩这类宏观零动量观测量由 CG 扇区主导：

$$
\chi
=
L^{d/2}
\tilde\chi(tL^{d/2}).
$$

相反，带非零波矢的 susceptibility 会过滤掉常数 plateau：

$$
\chi_k
\propto
\sum_r e^{ikr}g(r,L)
\sim
L^2\tilde\chi_k(tL^2),
\qquad k\ne 0.
$$

因此 $\chi$ 和 $\chi_k$ 在高维 PBC 中可以显示不同的有限尺寸指数。前者主要看 CG 零模，后者主要看 GFP 空间涨落。对普通 percolation，plateau 的指数相应变为

$$
L^{-2d/3},
$$

与 CG-percolation 的 $y_h^{\rm CG}=2d/3$ 一致。

这也给出一个实际判据。若把 percolation 的临界关联函数粗略写成

$$
g(r,L)
\asymp
r^{2-d}
+
bL^{-2d/3},
$$

那么短距离由 $r^{2-d}$ 主导，远距离由 plateau 主导。两项相当时满足

$$
r^{2-d}
\sim
L^{-2d/3},
$$

所以 crossover 距离为

$$
r_\times
\sim
L^{2d/[3(d-2)]}.
$$

这说明即使在同一个临界点，短距离测量和全系统求和测量也可能看到不同的有效指数。前者更像 GFP，后者更像 CG。

### 两个临界窗口

自由能中的两个缩放变量还意味着两个临界窗口。Ising 型系统中，CG 变量是

$$
tL^{d/2},
$$

所以零模主导的临界窗口宽度是

$$
|t|\sim L^{-d/2}.
$$

GFP 变量是

$$
tL^2,
$$

所以非零动量涨落对应的窗口宽度是

$$
|t|\sim L^{-2}.
$$

当 $d>4$ 时，$L^{-d/2}$ 比 $L^{-2}$ 更窄。因此从远离临界点往临界点靠近时，系统会先进入较宽的 GFP window；只有非常靠近伪临界点时，才进入由零模控制的 CG window。数值分析中如果尺寸不够大，或者温度网格没有覆盖足够窄的区域，就可能在同一模型里看到两种看似不同的标度。

### 线性尺寸标度与半径标度

这里比较 $L$ 标度与 $R$ 标度。

!!! note "核心图像"
    **对 cluster size 来说，只看关于系统线性尺寸 $L$ 的 finite-size scaling，即 $C\sim L^{d_l}$，主要看到的是 complete-graph asymptotics。这类标度更接近 distance-independent quantities，例如 susceptibility 或 cluster-size distribution 的 cutoff。**

    **如果进一步看 cluster size 与 unwrapped radius 的关系 $C\sim R^{d_f}$，才是在看空间几何本身。这个 $d_f$ 反映的是 GFP 或 high-dimensional percolation 的几何性质。**

    **低于几何上临界维度时，cluster 的 unwrapped radius 仍然满足 $R\sim L$，因此用 $L$ 或用 $R$ 度量 cluster 是等价的，$d_l=d_f$。超过上临界维度后，cluster 会在周期边界的 torus 上发生 extensive wrapping，导致 $R$ 增长快于 $L$，于是 $d_l$ 和 $d_f$ 分裂。**

    **对普通短程 percolation，$d_c=6$ 以上有 $C_1,C_2\sim L^{2d/3}$，这是 complete-graph percolation 标度，并给出 $\tau=1+d/(2d/3)=5/2$；但空间几何同时满足 $s\sim R^4$，所以 $R\sim L^{d/6}$。因此 $R\sim L^{d/6}$ 是观察上临界维度 $6$ 的关键。**

    **对 FK-Ising，情况更丰富。$d>4$ 后最大 cluster 已经服从 CG-Ising 标度 $C_1\sim L^{3d/4}$，而 $C_2$ 和其他 clusters 具有不同标度。因此 $C_1$ 和 $C_2$ 不同标度是 FK-Ising 的特殊现象。这个现象可以通过 LC joint model / Loop-Cluster 图像理解：最大的 FK cluster 带有 Ising-type giant-cluster 性质，而剩余 clusters 更接近 percolation-like clusters。也正因为如此，FK-Ising 在几何表示中同时显示出 $d_c=4$ 和 $d_p=6$ 两个上临界维度。**

高维 PBC 中 cluster 的另一个关键区分，是系统线性尺寸 $L$ 和 cluster 自身的 unwrapped radius $R$。对一个 cluster size $C$，可以问两个不同问题：

| 看什么 | 记号 | 含义 |
| --- | --- | --- |
| $C$ 如何随系统线性尺寸增长 | $C\sim L^{d_l}$ | finite-size fractal dimension |
| $C$ 如何随 cluster 自身半径增长 | $C\sim R^{d_f}$ | thermodynamic fractal dimension |

低于几何上临界维度时，cluster 在周期盒子里的 unwrapped 半径仍然和系统尺度同阶：

$$
R\sim L.
$$

这时用 $L$ 或 $R$ 度量 cluster 没有本质差别，因此通常有

$$
d_l=d_f.
$$

超过上临界维度后，情况不同。cluster 可以在 torus 上发生 extensive wrapping。若把路径在周期边界外展开，cluster 的 unwrapped radius 可以比 $L$ 增长得更快：

$$
R\not\sim L.
$$

于是 $d_l$ 和 $d_f$ 会分裂。很多“高维 PBC 看起来有两套指数”的现象，根源就在这里：用 $L$ 看的是 complete-graph 型有限尺寸 cutoff，用 $R$ 看的是空间几何本身。

### 普通短程 Percolation

普通短程 percolation 的上临界维度是 $d_c=6$。

普通短程 percolation 的上临界维度是

$$
d_c=6.
$$

当 $d<6$ 时，hyperscaling 仍然成立。最大 cluster 的大小、cluster 半径和磁场标度维数可以用同一套语言描述：

$$
d_l=d_f=y_h,
\qquad
R\sim L.
$$

当 $d>6$ 时，distance-independent quantities 进入 complete-graph percolation 标度。临界窗口中最大和第二大 cluster 同阶：

$$
C_1,C_2\sim V^{2/3}=L^{2d/3}.
$$

这正对应 $\phi^3$ / percolation 平均场的有限尺寸磁场指数

$$
y_h^{\rm CG}=\frac{2d}{3}.
$$

cluster-number density 的 cutoff 因而是 $L^{2d/3}$。若写成

$$
n(s,L)
\sim
s^{-\tau}
\tilde n(s/L^{2d/3}),
$$

并使用临界 cluster 分布的归一化关系

$$
\tau=1+\frac{d}{d_l},
$$

就得到

$$
\tau
=
1+\frac{d}{2d/3}
=
\frac52.
$$

但是空间几何并不因此变成 $d_f=2d/3$。高维 percolation cluster 的 thermodynamic fractal dimension 是

$$
d_f=4,
$$

也就是

$$
C\sim R^4.
$$

把两种标度合在一起，

$$
C_1\sim L^{2d/3},
\qquad
C_1\sim R_1^4,
$$

得到

$$
R_1\sim L^{d/6}.
$$

这个公式非常重要。它说明当 $d=6$ 时 $R_1\sim L$；而当 $d>6$ 时，unwrapped radius 的增长快于盒子线性尺寸。这就是从几何角度看出 $d_c=6$ 的地方。

因此在高维 PBC percolation 中，至少要区分三种容易混在一起的“磁性维度”：

| 记号 | 定义方式 | 高维 PBC percolation 中的值 |
| --- | --- | --- |
| $d_l$ 或 $D_L$ | 最大 cluster 关于盒子线性尺寸的标度 $C_1\sim L^{d_l}$ | $2d/3$ |
| $d_f$ 或 $D_F$ | cluster size 关于 unwrapped radius 的标度 $s\sim R^{d_f}$ | $4$ |
| $y_h$ | GFP 关联函数或非零动量涨落的磁场量纲 | $1+d/2$ |

低维时这些量常常可以通过 hyperscaling 互相换算；高维 PBC 中它们描述的是不同问题。把 $D_L=2d/3$ 和 $D_F=4$ 分开，是理解 $R\sim L^{d/6}$ 的关键。

### FK-Ising 的两个上临界维度

FK-Ising 同时涉及热力学上临界维度 $d_c=4$ 与几何上临界维度 $d_p=6$。

FK-Ising 比普通 percolation 更容易混淆，因为它同时带有 Ising 的 complete-graph 标度和 percolation-like 的空间几何。一个实用图像是：

| 维度范围 | 主导图像 |
| --- | --- |
| $d<4$ | 非平凡 Ising fixed point |
| $4<d<6$ | PBC 零模 / CG-Ising，加上 GFP 几何涨落 |
| $d\ge 6$ | PBC 零模 / CG-Ising，加上高维 percolation-like 几何 |

FK-Ising 的特殊点是，最大 cluster 和其他 clusters 不是同一个标度。对 $d>4$，最大 FK cluster 继承 Ising complete-graph 的零模标度：

$$
C_1\sim L^{3d/4}=V^{3/4}.
$$

这对应上表中的

$$
y_h^{\rm CG}=\frac{3d}{4}.
$$

第二大 cluster 和其他 clusters 则不按同一指数增长。一个常见的渐近写法是

$$
C_2\sim \frac{L^{1+d/2}}{\ln L},
$$

其中对数修正依赖具体临界维度、观测定义和有限尺寸窗口。这里最重要的不是记住这个式子的每个细节，而是记住结论：在 FK-Ising 的高维 PBC 临界点，$C_1$ 和 $C_2$ 本来就不必同阶。这与普通 percolation 的 complete-graph window 不同；普通 percolation 中 $C_1$ 和 $C_2$ 都是 $V^{2/3}$ 量级。

FK-Ising 的 other clusters 更适合用 $L$ 标度和 $R$ 标度分开描述：

| 维度范围 | 用 $L$ 看 other clusters | 用 $R$ 看 other clusters | cluster 分布 |
| --- | --- | --- | --- |
| $4<d<6$ | $d_l=1+d/2$ | $d_f=1+d/2$ | $\tau=1+d/(1+d/2)$ |
| $d=6$ | $d_l=4$ | $d_f=4$，带 log 修正 | $\tau=5/2$，带 log 修正 |
| $d>6$ | $d_l=1+d/2$ | $d_f=4$ | $\tau=5/2$ |

这张表表达的是：$d>4$ 后，FK-Ising 最大 cluster 已经感受到 Ising 的 complete-graph 零模标度；但 other clusters 的空间几何还会继续经历一个以 $d_p=6$ 为界的 percolation-like crossover。也就是说，$d_c=4$ 控制 Ising 临界涨落何时进入平均场，而 $d_p=6$ 控制 cluster 几何何时进入高维 percolation 型行为。

从这个角度看，“看 $L$”与“看 $R$”会给出不同信息。若只看

$$
C\sim L^{d_l},
$$

看到的是有限系统中 cluster-size cutoff 的增长，往往更接近 complete-graph asymptotics。若进一步看

$$
C\sim R^{d_f},
$$

就能看到空间几何本身是否已经进入 $d_f=4$ 的高维 percolation 行为。因此在 FK-Ising 中，第二个上临界维度 $d_p=6$ 更自然地体现在 $R$ 标度和 cluster 几何中，而不是单独体现在最大 cluster 的 $L$ 标度里。

### FK 与 Loop 表象中的三个层次

高维 Ising 的几何表象还可以用三个层次来组织：

1. two length scales：同一个 cluster 可以用 $L$ 或 unwrapped radius $R$ 度量；
2. two configuration sectors：构型空间中可能存在一个比例趋于零、但贡献特定巨大结构的 special sector；
3. two scaling windows：临界附近同时有 CG window 和 GFP window。

为了避免记号过多，先约定

$$
(y_t,y_h)
=
\left(
2,1+\frac d2
\right)
$$

表示 GFP 指数，

$$
(y_t^{\rm CG},y_h^{\rm CG})
=
\left(
\frac d2,\frac{3d}{4}
\right)
$$

表示 CG-Ising 指数，而

$$
(y_{t,p}^{\rm CG},y_{h,p}^{\rm CG})
=
\left(
\frac d3,\frac{2d}{3}
\right)
$$

表示 CG-percolation 指数。这样 FK 与 Loop 表象的差别可以概括为：

| 表象与维度 | two length scales | special sector | scaling windows |
| --- | --- | --- | --- |
| FK, $4<d<6$ | giant cluster: $C_1\sim L^{y_h^{\rm CG}}\sim R_1^{y_h^{\rm CG}}$；other clusters: $s\sim R^{y_h}$ | special sector 的比例 $P\sim L^{y_h-y_h^{\rm CG}}$，在该 sector 中 $s\sim R^{y_h}$ | 窄窗口 $O(L^{-y_t^{\rm CG}})$；宽窗口 $O(L^{-y_t})$ |
| FK, $d\ge 6$ | giant cluster: $C_1\sim L^{y_h^{\rm CG}}\sim R_1^{9/2}$；other clusters: $s\sim R^4$ | special sector 的比例 $P\sim L^{y_{h,p}^{\rm CG}-y_h^{\rm CG}}$，在该 sector 中 $s\sim R^4$ | $O(L^{-y_t^{\rm CG}})$；并有 percolation-like 的 $O(L^{-y_{t,p}^{\rm CG}})$ 与 $O(L^{-y_t})$ |
| Loop, $d>4$ | large loop clusters: $F_{1,2}\sim L^{y_t^{\rm CG}}\sim R_{1,2}^{y_t}$；other clusters: $n(s,L)\sim s^{-(1+d/y_t)}$ | special sector 的比例 $P\sim L^{y_h-y_h^{\rm CG}}$，在该 sector 中 $F_{1,2}\sim L^{y_t^{\rm CG}}\sim R_{1,2}^{y_t}$ | 窄窗口 $O(L^{-y_t^{\rm CG}})$；宽窗口 $O(L^{-y_t})$ |

这张表不需要初学时一次记住。它想表达的核心是：FK 表象中最大的 cluster、其他 clusters、以及极少数 special-sector 构型可以分别显示不同的标度。最大 FK cluster 更像 Ising complete-graph 的 giant cluster，因此

$$
C_1\sim L^{3d/4}.
$$

剩余 clusters 则更接近 percolation-like 几何。尤其在 $d\ge 6$ 时，

$$
s\sim R^4,
\qquad
n(s,L)\sim s^{-5/2},
$$

这正是高维 percolation 的几何特征。

Loop 表象给出的是另一种组织方式。它同样有 CG window 和 GFP window，但其几何上临界结构不像 FK 表象那样再显出一个独立的 $d_p=6$。因此在这个图像下，FK-Ising 可以同时显示 $d_c=4$ 和 $d_p=6$ 两个上临界维度；Loop-Ising 的主要上临界维度仍是 $d_c=4$。这不是说两种表象描述了不同的热力学模型，而是说不同几何变量对同一个 Ising 临界点的不同扇区敏感。

### 边界条件和进入临界点的路径

上面的讨论默认的是高维 torus，也就是周期边界条件。这个前提很重要。若换成自由边界、柱状边界或其他混合边界，零模和 wrapping 的组织方式会改变，某些观测量可能更接近 GFP 标度，而不是 CG 标度。

这一点可以概括为：**PBC 最容易显出 complete-graph asymptotics；带边界的系统更容易让空间相关和表面效应进入主导。** 因此比较不同模拟结果时，边界条件必须和观测量一起说明。只写“高维 percolation 的 $C_1$ 标度”是不够的；还要说是在 PBC、FBC，还是其他边界下测量。

另一个容易被忽略的点是进入临界点的路径。若令

$$
t\sim L^{-\lambda},
$$

则不同 $\lambda$ 会让系统落入不同窗口。以高维 Ising 的高温侧为例，若 $\lambda<d/2$，CG 变量 $tL^{d/2}$ 仍然很大，系统尚未真正进入零模临界窗口；若 $\lambda\ge d/2$，零模变量保持有限或趋近临界，磁化率等宏观量会显示临界点处的 CG 标度：

$$
\chi
\sim
\begin{cases}
L^\lambda, & \lambda<d/2,\\
L^{d/2}, & \lambda\ge d/2.
\end{cases}
$$

同时，GFP 窗口由 $\lambda=2$ 分隔。因为 $\xi\sim t^{-1/2}$，所以

$$
\xi\sim L^{\lambda/2}.
$$

当 $\lambda<2$ 时，特征 cluster 半径仍小于系统尺度；当 $\lambda>2$ 时，有限尺寸效应开始强烈介入。这个观点解释了为什么同一模型在不同温度扫描方式、不同伪临界点定义下，可能给出不同的有限尺寸外观。

### 与磁化率和几何观测量的关系

FK-Ising 表象提供了一个很直观的几何读法。FK cluster 的二阶矩与磁化率有直接关系。若 cluster 大小记为 $C_i$，一个常见的量是

$$
S_2
=
\frac{1}{L^d}\sum_i C_i^2.
$$

在 FK-Ising 中，$S_2$ 与磁化率同标度：

$$
S_2\sim \chi.
$$

若最大 cluster 满足

$$
C_1\sim L^{d_{L1}},
$$

并且 $S_2$ 主要由最大 cluster 控制，则

$$
S_2\sim \frac{C_1^2}{L^d}
\sim L^{2d_{L1}-d}.
$$

另一方面，磁化率的有限尺寸标度写成

$$
\chi\sim L^{2y_h-d}.
$$

比较两式得到

$$
d_{L1}=y_h.
$$

这个关系说明，最大 cluster 的尺寸指数可以作为磁场标度维数 $y_h$ 的几何表现。它也是为什么 cluster 大小、wrapping probability、cluster 半径等几何观测量常常对普适类和 crossover 很敏感。

这里的 $y_h$ 要按具体标度扇区来理解。低于上临界维度时，它就是通常相互作用固定点的磁场标度维数；高维 PBC 的 FK-Ising 最大 cluster 中，它应读作 CG-Ising 的

$$
y_h^{\rm CG}=\frac{3d}{4},
$$

因此

$$
C_1\sim L^{y_h^{\rm CG}}.
$$

若研究的是普通高维 percolation，则对应的是 CG-percolation 的

$$
y_h^{\rm CG}=\frac{2d}{3}.
$$

但要注意，这里的 $d_{L1}$ 是按系统线性尺寸 $L$ 定义的有限尺寸指数。若改用 cluster 自身回转半径 $R$ 来定义分形维度

$$
C_1\sim R^{d_F},
$$

在上临界维度以上和周期边界条件下，$d_{L1}$ 与 $d_F$ 的关系可能不再像低维那样直接。原因仍然是零模、危险无关变量和边界条件会改变有限系统中的几何组织方式。

在这里讨论的普通 percolation 与 FK-Ising 的比较中，$C_1$ 和 $C_2$ 标度不同是 FK-Ising 的特殊现象；普通 percolation 的 complete-graph window 中 $C_1$ 和 $C_2$ 是同阶的，均为 $V^{2/3}$。这种 FK-Ising 的 $C_1$ dominance 可以从 LC joint model 或 Loop-Cluster 图像中理解：最大 FK cluster 继承了 Ising complete-graph 零模标度，而其他 clusters 更接近 percolation-like 标度。

Loop 表象也给出类似提醒。某些 loop 模型中，能量或热标度可能和 bond 数、loop 长度、返回概率等几何量相关。这样的图像很有帮助，但具体关系依赖表象和模型定义。更稳妥的用法是：把几何表象当成理解高维有限尺寸修正的补充视角，而不是在没有推导时把某个几何指数直接等同于热力学指数。

## 修正项从哪里来

真实数据很少只满足最简单的标度函数。原因主要有三类。

第一，存在 irrelevant scaling fields：

$$
u_iL^{y_i},\qquad y_i<0.
$$

对标度函数做展开：

$$
F_O(tL^{y_t},uL^{y_i})
=
F_O(tL^{y_t})
+
L^{y_i}G_O(tL^{y_t})
+\cdots.
$$

若记

$$
\omega=-y_i>0,
$$

则常写为

$$
O(t,L)
=
L^{\rho/\nu}
\left[
f_O(tL^{1/\nu})
+L^{-\omega}g_O(tL^{1/\nu})
+\cdots
\right].
$$

第二，物理参数和 scaling field 不一定完全相同。例如模拟中控制的是 $T-T_c$ 或 $p-p_c$，真正进入 RG 的 temperature field 可以是解析函数：

$$
t_{\rm RG}
=
a_1(T-T_c)
+a_2(T-T_c)^2
+\cdots.
$$

磁场也可能和温度场发生解析混合。做高精度拟合时，这会产生额外修正。

第三，解析背景 $f_a$ 会进入某些观测量。Binder ratio 这类由矩构造的无量纲量，主导标度因子会在比值中抵消，但解析背景仍可能留下次领先修正。相比之下，wrapping probability 这类几何概率通常更直接接近 universal scaling function。

在特殊情况下，若两个 irrelevant exponent 退化，还可能出现

$$
L^{-\omega}\ln L
$$

这样的对数修正。实际 Monte Carlo 分析中，一旦小尺寸数据系统性偏离，就要考虑这些修正，而不能只追求视觉上漂亮的 data collapse。

## Data Collapse

有限尺寸标度给出 data collapse 的原则。以磁化率为例：

$$
\chi(t,L)
=
L^{\gamma/\nu}
f_\chi(tL^{1/\nu}).
$$

因此如果 $T_c,\nu,\gamma$ 选择正确，重新缩放后的数据

$$
\chi(t,L)L^{-\gamma/\nu}
$$

应当作为

$$
tL^{1/\nu}
$$

的函数落在同一条曲线上。

对磁化强度则画

$$
m(t,L)L^{\beta/\nu}
\quad
\text{vs.}
\quad
tL^{1/\nu}.
$$

对 Binder ratio 这类无量纲量，直接画

$$
U_4(t,L)
\quad
\text{vs.}
\quad
tL^{1/\nu}.
$$

data collapse 是很有用的可视化检查，但它不应替代误差分析。更可靠的流程是先用无量纲量交点估计 $T_c$，再用临界点处的幂律估计指数比，最后用 collapse 检查整体自洽性。

上面这套 collapse 写法默认观测量由同一个普通标度变量 $tL^{1/\nu}$ 控制。若处在上临界维度以上，尤其是高维 PBC，需要先判断观测量属于哪个扇区。宏观零动量量如 $\chi$ 可能应画成

$$
\chi L^{-d/2}
\quad
\text{vs.}
\quad
tL^{d/2},
$$

而非零动量响应 $\chi_k$ 则更自然地按 GFP 变量

$$
\chi_k L^{-2}
\quad
\text{vs.}
\quad
tL^2
$$

组织。cluster 几何量还要进一步区分 $C\sim L^{d_l}$ 和 $C\sim R^{d_f}$。因此高维数据的 collapse 不是把 $\nu=1/2$ 代入低维公式这么简单，而是要先说明边界条件、观测量和采用的标度扇区。

## 在 Monte Carlo 数据中的流程

实际分析可以按下面顺序进行：

1. 对每个尺寸 $L$ 独立完成热化、自关联时间估计和 binning。
2. 测量能量、序参量、磁化率、Binder ratio、相关长度比或 wrapping probability。
3. 用无量纲量的交点初步定位 $T_c$。
4. 检查交点随尺寸的漂移，估计有限尺寸修正。
5. 在临界点附近拟合

$$
m(0,L)\sim L^{-\beta/\nu},
\qquad
\chi(0,L)\sim L^{\gamma/\nu}.
$$

6. 用斜率或导数估计 $1/\nu$，例如

$$
\left.\frac{dU_4}{dT}\right|_{T_c}
\sim L^{1/\nu}.
$$

7. 做 data collapse，检查 $T_c$、$\nu$ 和指数比是否同时自洽。
8. 改变最小尺寸 $L_{\min}$、加入或去掉 $L^{-\omega}$ 修正项，评估系统误差。

如果研究对象在上临界维度以上，还需要在第 5 步之前增加一个判断：当前观测量看的是普通相互作用固定点、GFP 扇区、CG 零模扇区，还是 cluster 的空间几何扇区。不同扇区对应不同横轴变量和不同前因子，不能混在同一个 collapse 中。

## 小结

有限尺寸标度可以压缩成一条 RG 逻辑：

$$
x\to x'=\frac{x}{b}
\quad
\Longrightarrow
\quad
t\to tb^{y_t}
\quad
\Longrightarrow
\quad
tL^{y_t}.
$$

空间坐标的缩放告诉我们如何改变观察尺度；coupling 的缩放告诉我们温度偏离量在该尺度上有多强；取 $b=L$ 后，有限系统的全部临界行为就被组织成 $tL^{y_t}$、$hL^{y_h}$ 和 $u_iL^{y_i}$ 这些无量纲组合。

Monte Carlo 给出有限系统的统计样本；有限尺寸标度告诉我们如何从这些样本外推到临界固定点。

在普通低维连续相变中，这通常意味着用单一变量 $tL^{1/\nu}$ 组织数据；在高维 PBC 或长程平均场区间中，则要先判断零模、非零动量涨落和几何 cluster 哪个在控制观测量。
