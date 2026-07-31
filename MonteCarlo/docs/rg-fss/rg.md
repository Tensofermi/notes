# LGW 相变理论与重整化群

## 概述

连续相变附近，体系会出现越来越大的相关长度。此时许多微观细节会被长距离涨落平均掉，真正重要的是少数慢变量、对称性、维度以及相互作用范围。Landau-Ginzburg-Wilson 理论正是沿着这条思路建立起来的。

LGW 与 RG 的基本结构包括：

1. 从最简单的 Landau 零模理论出发，只考虑均匀序参量；
2. 说明在无梯度项时如何理解 $y_t$ 和 $y_h$；
3. 推导 $y_t,y_h$ 与六个常见临界指数之间的关系；
4. 解释平均场理论为什么可看成高维或无穷维极限；
5. 引入 Ginzburg 的空间涨落项，得到 LGW 泛函；
6. 用量纲分析求 Gaussian 固定点的 $y_t,y_h$ 与上临界维度；
7. 推广到 $\phi^p$ 相互作用与长程 $k^\sigma$ 涨落项；
8. 用 Wilson RG 的语言重新整理这些结论。

为了避免符号混乱，下文统一记

$$
t\propto T-T_c
$$

为距离临界点的温度变量，$h$ 为外场，$d$ 为空间维度。

## Landau 零模理论

### 最简单的无梯度哈密顿量

Landau 理论从序参量出发。对于 Ising 型相变，序参量是标量 $m$，体系具有

$$
m\to -m
$$

的对称性。在只保留均匀序参量的情况下，可以写出最简单的 Landau 哈密顿量或自由能：

$$
\mathcal H_L(m)=L^d\left[
\frac{t}{2}m^2+\frac{u}{4}m^4-hm
\right].
$$

这里 $L^d$ 是系统体积，$u>0$ 保证自由能稳定。这个理论只保留全空间平均的 $m$，因此常被称为零模理论。

平衡态由鞍点方程给出：

$$
\frac{\partial \mathcal H_L}{\partial m}=0.
$$

直接计算得到

$$
tm+um^3-h=0.
$$

当 $h=0$ 且 $t<0$ 时，非零解满足

$$
m^2=-\frac{t}{u}.
$$

所以

$$
m\sim (-t)^{1/2},
$$

由此得到平均场指数

$$
\boxed{\beta=\frac12}.
$$

当 $t>0$ 且 $h\to 0$ 时，$m$ 很小，鞍点方程近似为

$$
tm\simeq h.
$$

于是

$$
m\simeq \frac{h}{t},
$$

磁化率为

$$
\chi=\frac{\partial m}{\partial h}\sim t^{-1}.
$$

因此

$$
\boxed{\gamma=1}.
$$

在临界等温线 $t=0$ 上，

$$
um^3=h,
$$

所以

$$
m\sim h^{1/3},
$$

得到

$$
\boxed{\delta=3}.
$$

再看自由能奇异部分。将 $m^2=-t/u$ 代回自由能密度，可得

$$
f_{\rm sing}\sim -\frac{t^2}{u}.
$$

比热对应自由能对温度变量的二阶导数，因此

$$
C\sim -\frac{\partial^2 f_{\rm sing}}{\partial t^2}\sim {\rm const}.
$$

平均场比热指数为

$$
\boxed{\alpha=0}.
$$

> 这一套推导只用到了均匀序参量的鞍点。它可以给出 $\alpha,\beta,\gamma,\delta$，却还没有真正的空间涨落和相关长度。

### 无梯度项时的温度和磁场指数

RG 语境下，$y_t$ 和 $y_h$ 描述温度变量与外场在尺度变换下的放大规律：

$$
t'=b^{y_t}t,\qquad h'=b^{y_h}h.
$$

纯 Landau 零模理论缺少空间坐标和梯度项，无法直接执行通常的空间粗粒化。不过它仍然可以给出一组有限尺寸意义下的有效标度指数。

在临界点 $t=h=0$，四次项控制零模涨落：

$$
\mathcal H_L(m)\sim L^d u m^4.
$$

典型涨落由 $\mathcal H_L(m)\sim 1$ 估计：

$$
L^d m^4\sim 1.
$$

因此

$$
m\sim L^{-d/4}.
$$

质量项的尺度为

$$
\begin{aligned}
L^d t m^2
&\sim L^d t L^{-d/2}\\
&=tL^{d/2}.
\end{aligned}
$$

所以温度变量的有限尺寸组合是

$$
tL^{d/2}.
$$

这给出零模有效指数

$$
\boxed{y_t^\ast=\frac d2}.
$$

外场项的尺度为

$$
\begin{aligned}
L^d h m
&\sim L^d h L^{-d/4}\\
&=hL^{3d/4}.
\end{aligned}
$$

因此

$$
\boxed{y_h^\ast=\frac{3d}{4}}.
$$

这两个量带有星号，是为了提醒它们属于零模有限尺寸标度。真正的 Gaussian RG 本征值会在加入梯度项后自然出现。

把 $y_t^\ast,y_h^\ast$ 代入常见标度关系，可以重新得到 Landau 平均场指数。例如

$$
\begin{aligned}
\beta
&=\frac{d-y_h^\ast}{y_t^\ast}\\
&=\frac{d-\frac{3d}{4}}{\frac d2}\\
&=\frac12,
\end{aligned}
$$

$$
\begin{aligned}
\gamma
&=\frac{2y_h^\ast-d}{y_t^\ast}\\
&=\frac{\frac{3d}{2}-d}{\frac d2}\\
&=1,
\end{aligned}
$$

$$
\begin{aligned}
\delta
&=\frac{y_h^\ast}{d-y_h^\ast}\\
&=\frac{\frac{3d}{4}}{\frac d4}\\
&=3.
\end{aligned}
$$

## 温度和磁场指数与六个临界指数

下面用 $y_t,y_h$ 推导六个常见临界指数。

接下来先不限制 $y_t,y_h$ 的来源，只假设在某个 RG 固定点附近，奇异自由能密度满足齐次标度形式：

$$
f_s(t,h)=b^{-d}f_s(tb^{y_t},hb^{y_h}).
$$

这里 $b>1$ 表示把长度尺度放大的因子。这个式子是临界指数之间建立联系的核心。

先解释一下这个式子里最容易让人困惑的因子 $b^{-d}$。RG 变换可以理解为两步：先把短距离自由度粗粒化掉，再把长度单位重新放大。若系统线性尺寸为 $L$，一次尺度因子为 $b$ 的 RG 之后，

$$
L\to L'=\frac{L}{b}.
$$

因此格点数或体积尺度从

$$
L^d
$$

变为

$$
\left(\frac{L}{b}\right)^d.
$$

也就是说，一个新的粗粒化格点代表原来的

$$
b^d
$$

个微观格点。二维系统中，若原来是 $8\times 8$ 的格子，取 $b=2$ 后就变成 $4\times 4$ 的粗粒化格子，自由度数减少

$$
\frac{8^2}{4^2}=4=2^2=b^d.
$$

自由能密度定义为

$$
f=\frac{F}{V}.
$$

由于它是每单位体积的自由能，粗粒化之后一个新单位体积对应原来的 $b^d$ 个微观体积单位。若仍用原来的微观体积单位来表示密度，就会出现

$$
f_s\to b^{-d}f_s.
$$

这正是标度公式前面 $b^{-d}$ 的来源。它并不表示物理自由能凭空消失，而是表示描述单位变粗后，单位体积的计数方式发生了变化。

这里也要分清主动和被动两种视角。主动地说，block spin 把 $b^d$ 个微观格点合成一个粗格点，格点间距从

$$
a\to a'=ba.
$$

被动地说，我们换用粗粒化后的坐标系，把原来长度为 $b$ 的距离记成新坐标里的 $1$，也就是

$$
x\to x'=\frac{x}{b},
\qquad
x=bx'.
$$

这两种写法并不矛盾。$a'=ba$ 强调观察尺度变粗；$x'=x/b$ 强调坐标数值按新单位重新计量。连续积分测度也随之变为

$$
d^dx'=b^{-d}d^dx.
$$

因此在自由能密度的标度关系中，$b^{-d}$ 可以看作体积单位重新计量带来的因子。

耦合参数同时发生流动：

$$
t\to t'=tb^{y_t},
\qquad
h\to h'=hb^{y_h}.
$$

若 $y_t>0$，温度偏离量是 relevant 方向；只要 $t\ne0$，粗粒化后它会越来越明显。若 $y_h>0$，外场也是 relevant 方向。临界点满足

$$
t=0,\qquad h=0,
$$

在 RG 后仍然是

$$
t'=0,\qquad h'=0,
$$

因此它对应一个固定点。

参数变换与空间变换是同一套 RG 逻辑的两面。空间坐标重新定义为

$$
x'=\frac{x}{b},
$$

所有带尺度量纲的对象都要跟着重新定义。场本身有 scaling dimension：

$$
\phi'(x')=b^{x_\phi}\phi(bx').
$$

温度偏离量 $t$ 在 RG 语言中表示某个算符前面的 coupling。以 LGW 泛函为例：

$$
\mathcal H[\phi]
=
\int d^dx
\left[
\frac12(\nabla\phi)^2
+\frac{t}{2}\phi^2
+\frac{u}{4!}\phi^4
-h\phi
\right].
$$

这里 $t$ 乘在 $\phi^2$ 前面，$h$ 乘在 $\phi$ 前面。更一般地，如果某个扰动写成

$$
\delta\mathcal H
=
g\int d^dx\,\mathcal O(x),
$$

而算符 $\mathcal O$ 的 scaling dimension 为 $\Delta_{\mathcal O}$，即

$$
\mathcal O(x)=b^{-\Delta_{\mathcal O}}\mathcal O'(x'),
$$

同时

$$
d^dx=b^d d^dx',
$$

那么这个 coupling 在 RG 后变为

$$
g'=g b^{d-\Delta_{\mathcal O}}.
$$

因此

$$
\boxed{y_g=d-\Delta_{\mathcal O}}.
$$

对温度场和磁场分别有

$$
y_t=d-\Delta_{\phi^2},
\qquad
y_h=d-\Delta_\phi.
$$

临界现象中常写

$$
\Delta_\phi=\frac{d-2+\eta}{2},
$$

于是

$$
\boxed{
y_h=d-\Delta_\phi
=\frac{d+2-\eta}{2}
}.
$$

这说明 $t\to tb^{y_t}$ 和 $h\to hb^{y_h}$ 来自空间缩放与算符缩放共同诱导出的 coupling 变换。

还可以从相关体积理解 $f_s$ 的大小。临界附近的奇异自由能密度有估计

$$
f_s\sim \xi^{-d}.
$$

一个相关体积 $\xi^d$ 大约贡献一个独立的临界自由能量级，所以单位体积中的独立临界涨落数目约为 $1/\xi^d$。当接近临界点时 $\xi\to\infty$，于是 $f_s$ 本身可以趋向于零；真正发散的通常是它的导数，例如比热和磁化率：

$$
C\sim \frac{\partial^2 f_s}{\partial t^2},
\qquad
\chi\sim \frac{\partial^2 f_s}{\partial h^2}.
$$

完整自由能可分成解析部分与奇异部分：

$$
f(t,h)=f_{\rm regular}(t,h)+f_s(t,h).
$$

RG 标度主要描述的是其中负责临界奇异性的 $f_s$。

### 相关长度指数

由相关长度的标度式可以得到 $\nu$。

相关长度满足

$$
\xi(t)=b\,\xi(tb^{y_t}).
$$

取

$$
tb^{y_t}=1,
$$

即

$$
b=t^{-1/y_t},
$$

可得

$$
\xi\sim t^{-1/y_t}.
$$

因此

$$
\boxed{\nu=\frac1{y_t}}.
$$

### 比热指数

由奇异自由能的标度式可以得到 $\alpha$。

令

$$
b=\lvert t\rvert^{-1/y_t}.
$$

自由能奇异部分满足

$$
f_s(t,0)\sim \lvert t\rvert^{d/y_t}.
$$

比热来自自由能对温度变量的二阶导数：

$$
C\sim \frac{\partial^2 f_s}{\partial t^2}.
$$

因此

$$
C\sim \lvert t\rvert^{d/y_t-2}.
$$

得到

$$
\boxed{\alpha=2-\frac d{y_t}}.
$$

### 序参量指数

由磁化强度的标度式可以得到 $\beta$。

磁化强度为

$$
m=-\frac{\partial f_s}{\partial h}.
$$

由自由能标度形式可得

$$
m(t,h)=b^{-d+y_h}m(tb^{y_t},hb^{y_h}).
$$

仍取 $b=\lvert t\rvert^{-1/y_t}$，有

$$
m(t,0)\sim \lvert t\rvert^{(d-y_h)/y_t}.
$$

所以

$$
\boxed{\beta=\frac{d-y_h}{y_t}}.
$$

### 磁化率指数

由磁化率的标度式可以得到 $\gamma$。

磁化率为

$$
\chi=\frac{\partial m}{\partial h}
=-\frac{\partial^2 f_s}{\partial h^2}.
$$

所以

$$
\chi(t,0)\sim b^{-d+2y_h}.
$$

取 $b=\lvert t\rvert^{-1/y_t}$，得到

$$
\chi\sim \lvert t\rvert^{-(2y_h-d)/y_t}.
$$

因此

$$
\boxed{\gamma=\frac{2y_h-d}{y_t}}.
$$

### 临界等温线指数

由临界等温线上的磁化响应可以得到 $\delta$。

在 $t=0$ 时取

$$
hb^{y_h}=1,
$$

即

$$
b=h^{-1/y_h}.
$$

于是

$$
m(0,h)\sim b^{-d+y_h}
\sim h^{(d-y_h)/y_h}.
$$

与

$$
m\sim h^{1/\delta}
$$

比较，得到

$$
\boxed{\delta=\frac{y_h}{d-y_h}}.
$$

### 反常维数

由临界点关联函数的尺度变换可以得到 $\eta$。

外场项为

$$
\int d^d x\,h\phi.
$$

若场的 scaling dimension 为 $x_\phi$，则

$$
y_h=d-x_\phi.
$$

临界点处的关联函数满足

$$
G(r)=\langle \phi(r)\phi(0)\rangle
\sim \frac1{r^{2x_\phi}}.
$$

标准定义写作

$$
G(r)\sim \frac1{r^{d-2+\eta}}.
$$

于是

$$
2x_\phi=d-2+\eta.
$$

代入 $x_\phi=d-y_h$，得到

$$
\boxed{\eta=d+2-2y_h}.
$$

常见指数可整理为：

| 指数 | 定义 |
| --- | --- |
| $\alpha$ | $C\sim \lvert t\rvert^{-\alpha}$ |
| $\beta$ | $m\sim (-t)^\beta$ |
| $\gamma$ | $\chi\sim \lvert t\rvert^{-\gamma}$ |
| $\delta$ | $m\sim h^{1/\delta}$ |
| $\nu$ | $\xi\sim \lvert t\rvert^{-\nu}$ |
| $\eta$ | $G(r)\sim r^{-(d-2+\eta)}$ |

> 上述关系依赖普通 hyperscaling。高于上临界维度时，危险无关变量会改变有限尺寸标度结构，使用这些关系时需要结合具体固定点判断。

## 平均场与无穷维图像

Landau 平均场理论忽略空间涨落，只保留一个全局序参量 $m$。这等价于假设每个自由度都感受到整体平均环境，局域涨落被充分平均。

高维体系中，这种图像会越来越准确。直观原因包括：

- 格点的有效邻居数增多，单个邻居的涨落影响被平均；
- 随机行走在高维中回返概率降低，局域涨落的反馈变弱；
- 临界涨落相对于平均序参量的贡献下降；
- 鞍点近似越来越稳定。

这一点可以通过 Ginzburg 判据看得更清楚。Landau 平均场给出

$$
m^2\sim \frac{\lvert t\rvert}{u}.
$$

Gaussian 理论中

$$
\xi\sim \lvert t\rvert^{-1/2}.
$$

一个相关体积内的场涨落大致满足

$$
\langle(\delta\phi)^2\rangle_\xi\sim \xi^{2-d}.
$$

于是涨落与平均序参量平方的比值为

$$
\frac{\langle(\delta\phi)^2\rangle_\xi}{m^2}
\sim
\frac{\xi^{2-d}}{\lvert t\rvert}.
$$

代入 $\xi\sim \lvert t\rvert^{-1/2}$，得到

$$
\frac{\langle(\delta\phi)^2\rangle_\xi}{m^2}
\sim
\lvert t\rvert^{(d-4)/2}.
$$

当 $t\to 0$ 时：

- $d>4$ 时，该比值趋于 $0$，平均场稳定；
- $d<4$ 时，该比值发散，涨落改变临界行为；
- $d=4$ 时为边缘情况，通常出现对数修正。

因此短程 $\phi^4$ 理论的上临界维度为

$$
\boxed{d_c=4}.
$$

从这个意义上说，Landau 平均场可看成高维极限或无穷维极限中的临界理论。

## Ginzburg 泛函与梯度涨落

Landau 理论只考虑均匀序参量。Ginzburg 的关键推广是允许序参量随空间变化：

$$
m\longrightarrow \phi(x).
$$

自由能也从普通函数推广为泛函：

$$
\mathcal H[\phi]
=\int d^d x
\left[
\frac12(\nabla\phi)^2
+\frac{t}{2}\phi^2
+\frac{u}{4!}\phi^4
-h\phi
\right].
$$

这就是 Landau-Ginzburg-Wilson 理论的基本形式。各项含义如下：

- $\frac12(\nabla\phi)^2$ 描述空间涨落的代价；
- $\frac{t}{2}\phi^2$ 是质量项；
- $\frac{u}{4!}\phi^4$ 是相互作用项；
- $h\phi$ 是外场耦合。

对于 $O(n)$ 模型，序参量是 $n$ 分量场

$$
\boldsymbol\phi=(\phi_1,\cdots,\phi_n),
$$

泛函写为

$$
\mathcal H[\boldsymbol\phi]
=\int d^d x
\left[
\frac12(\nabla\boldsymbol\phi)^2
+\frac{t}{2}\boldsymbol\phi^2
+\frac{u}{4!}(\boldsymbol\phi^2)^2
-\boldsymbol h\cdot\boldsymbol\phi
\right].
$$

加入梯度项之后，理论中出现空间尺度、动量、传播子和相关长度。$y_t,y_h$ 也就可以通过标准量纲分析得到。

## Gaussian 固定点的量纲分析

先从完整的短程 $\phi^4$ 理论写起：

$$
\mathcal H
=\int d^d x
\left[
\frac K2(\nabla\phi)^2
+\frac{t}{2}\phi^2
+\frac u{4!}\phi^4
-h\phi
\right].
$$

Gaussian fixed point 指的是相互作用和相关扰动都取固定点值：

$$
u^\ast=0,\qquad t^\ast=0,\qquad h^\ast=0.
$$

此时长波哈密顿量只剩二次型：

$$
\mathcal H_{\rm G}
=
\frac12\int d^dx\,
K(\nabla\phi)^2.
$$

这才是 “Gaussian” 的来源：哈密顿量是二次型，路径积分是 Gaussian 积分，不同动量模式之间没有相互作用。传播子为

$$
G(k)=\frac{1}{Kk^2+t}.
$$

在临界点 $t=0$，$K$ 只改变传播子的整体振幅：

$$
G(k)\sim \frac{1}{Kk^2}.
$$

因此可以通过场重定义把 $K$ 吸收到 $\phi$ 中：

$$
\phi'=\sqrt K\,\phi.
$$

这一步只是选择场的归一化，或称 canonical normalization。**固定 $K=1$ 不是 Gaussian fixed point 的定义；Gaussian fixed point 的定义是 $u^\ast=0$，也就是固定点哈密顿量只有二次型。**

在这个固定点附近做量纲分析时，我们先用二次梯度项决定场的工程量纲。也就是要求

$$
\int d^d x\,(\nabla\phi)^2\sim 1.
$$

这里并不是说只有梯度项无量纲。完整哈密顿量中的每一项最终都必须无量纲：

$$
\int d^dx\,t\phi^2,\qquad
\int d^dx\,u\phi^4,\qquad
\int d^dx\,h\phi
$$

也都要无量纲。区别在于：梯度项先用来选择 $\phi$ 的归一化；一旦 $\phi$ 的量纲确定，其他项的无量纲条件就用来决定 $t,u,h$ 的量纲。

这一步也解释了为什么这是 Gaussian 固定点附近的量纲分析：我们把 $\phi^4$ 项看成加在二次自由理论上的扰动

$$
\delta\mathcal H
=
\int d^dx\,u\phi^4,
$$

然后问这个扰动在 Gaussian 固定点附近是 relevant 还是 irrelevant。若真正的固定点是 Wilson-Fisher 固定点，也就是

$$
u^\ast\ne0,
$$

那么场的 scaling dimension 不再只是工程量纲，算符也可能发生混合，需要在新固定点附近重新线性化 RG。

这里先说明一个容易混淆的记号问题。前面讲 RG 粗粒化时，我们使用的是被动坐标：

$$
x\to x'=\frac{x}{b}.
$$

它的意思是：粗粒化后一个新单位长度代表原来的 $b$ 个微观长度，所以同一段物理距离在新坐标里的数值变小。

而在量纲分析中，我们常说某个量在长度尺度 $L$ 下如何缩放，或者等价地写“大尺度”

$$
L\to bL.
$$

这不是另一个 RG 规则，而是同一件事的主动说法：我们在问把观察距离放大 $b$ 倍时，场和耦合常数应带什么长度量纲。两种写法的对应关系是：

| 视角 | 写法 | 含义 |
| --- | --- | --- |
| 被动坐标重计量 | $x'=x/b$ | 同一段距离用粗坐标表示，数值变小 |
| 主动尺度放大 | $L\to bL$ | 观察更大的物理长度尺度 |

所以这里用 $L$ 的幂次做量纲分析，和前面的 $x'=x/b$ 不矛盾。它们只是一个从坐标数值看，一个从物理长度尺度看。

$K$ 的存在不会改变 Gaussian 固定点处的工程量纲，但这不等于说 $K$ 在物理上永远无所谓。$K$ 会影响非普适量，例如相关长度的振幅、刚度、helicity modulus 的数值单位等。普适临界指数不依赖 $K$ 的具体取值，是因为在固定点分析中可以用场归一化把梯度项系数固定住，再研究 $t,h,u$ 等真正改变长距离行为的方向。

若模型的长波动能不是 $k^2$，而是长程相互作用中常见的 $k^\sigma$，那就要把梯度项换成对应的非局域 Gaussian 项，场的量纲也会改变。短程 $\phi^4$ 理论这里默认的是 $k^2$ 动能。

另外，若写成线性的 $K\nabla\phi$，它通常不是稳定的体积动能项。对标量场，

$$
\int d^dx\,\nabla\phi
$$

是边界项；在周期边界或无边界情形下不控制体涨落。真正控制 Gaussian 长波涨落的是二次型 $(\nabla\phi)^2$。

由于

$$
[d^d x]\sim L^d,\qquad [\nabla]\sim L^{-1},
$$

可得

$$
L^d L^{-2}[\phi]^2\sim 1.
$$

因此

$$
[\phi]\sim L^{-(d-2)/2}.
$$

场的 scaling dimension 为

$$
\boxed{x_\phi=\frac{d-2}{2}}.
$$

### 求温度指数

这里求 $y_t$。

质量项满足

$$
\int d^d x\,t\phi^2\sim 1.
$$

代入 $[\phi]^2\sim L^{-(d-2)}$，得到

$$
L^d[t]L^{-(d-2)}\sim 1.
$$

所以

$$
[t]\sim L^{-2}.
$$

对应 RG 本征指数

$$
\boxed{y_t=2}.
$$

### 求磁场指数

这里求 $y_h$。

外场项满足

$$
\int d^d x\,h\phi\sim 1.
$$

代入 $[\phi]\sim L^{-(d-2)/2}$，得到

$$
L^d[h]L^{-(d-2)/2}\sim 1.
$$

因此

$$
[h]\sim L^{-(d+2)/2}.
$$

对应

$$
\boxed{y_h=\frac{d+2}{2}}.
$$

### 求四次耦合与上临界维度

这里求 $u$ 的标度量纲与上临界维度。

四次项满足

$$
\int d^d x\,u\phi^4\sim 1.
$$

由于

$$
[\phi]^4\sim L^{-2(d-2)},
$$

有

$$
L^d[u]L^{-2(d-2)}\sim 1.
$$

所以

$$
[u]\sim L^{-(4-d)}.
$$

四次耦合的 RG 指数为

$$
\boxed{y_u=4-d}.
$$

于是：

- $d<4$ 时，$u$ 为 relevant；
- $d=4$ 时，$u$ 为 marginal；
- $d>4$ 时，$u$ 为 irrelevant。

上临界维度由 $y_u=0$ 给出：

$$
\boxed{d_c=4}.
$$

这里的 $y_t=2$ 和 $y_h=(d+2)/2$ 是 Gaussian 固定点的量纲分析结果。低于上临界维度时，$u$ 会把体系带向新的相互作用固定点，真实指数会发生修正。

需要强调：这不是说 $y_u$ 像一个外力一样把 $y_t,y_h$ “直接重整化掉”。更准确的说法是：

1. 在 Gaussian 固定点附近，线性化 RG 的本征值是

$$
y_t^{\rm G}=2,\qquad
y_h^{\rm G}=\frac{d+2}{2},\qquad
y_u^{\rm G}=4-d.
$$

2. 当 $d<4$ 时，$y_u^{\rm G}>0$，所以只要 $u$ 不严格等于零，RG 流就会离开 Gaussian 固定点。

3. 流离开之后，会到达另一个固定点，也就是 Wilson-Fisher 固定点：

$$
u^\ast\ne0.
$$

4. 真正的临界指数应当在新固定点附近重新线性化 RG 得到：

$$
y_t=\frac1\nu,\qquad
y_h=\frac{d+2-\eta}{2}.
$$

因此，低维中的指数变化来自“控制长距离物理的固定点变了”，而不是在同一个 Gaussian 固定点上把 $y_t,y_h$ 随手改一下。$u$ 的作用是让 Gaussian 固定点不稳定，并把系统带到带相互作用的 Wilson-Fisher 固定点。

这也是为什么 $d<4$ 的 Ising、$O(n)$ 模型不再有平均场指数。以三维 Ising 为例，

$$
\nu\approx0.630,\qquad \eta\approx0.036,
$$

所以

$$
y_t\approx1.587,\qquad
y_h\approx\frac{3+2-0.036}{2}\approx2.482,
$$

明显不同于 Gaussian 的

$$
y_t^{\rm G}=2,\qquad y_h^{\rm G}=2.5.
$$

### Dangerous irrelevant variable 是什么意思

当 $d>4$ 时，

$$
y_u=4-d<0,
$$

所以 $u$ 在 Gaussian 固定点是 irrelevant。普通 irrelevant 变量的意思是：长距离下它越来越小，临界指数和主导标度函数通常不依赖它。

但是 $\phi^4$ 理论中的 $u$ 在 $d>4$ 有一个特殊性：它虽然在 RG 意义下 irrelevant，却不能在所有问题里直接设成零。原因是它负责稳定 Landau 自由能。若只保留

$$
F(m)\sim L^d\left(\frac t2m^2-hm\right),
$$

在 $t<0$ 的有序相或临界零模涨落中，自由能没有稳定的四次项，磁化分布无法正常归一化。必须保留

$$
F(m)\sim L^d\left(\frac t2m^2+\frac u4m^4-hm\right).
$$

这就是 dangerous irrelevant variable 的含义：

> $u$ 对固定点稳定性和临界指数来说是 irrelevant，但某些物理量的振幅、有限尺寸标度或有序相标度会以奇异方式依赖 $u$，因此不能简单令 $u=0$。

一个直接例子是在临界点 $t=h=0$，零模满足

$$
L^d u m^4\sim1,
$$

所以

$$
m\sim u^{-1/4}L^{-d/4},
\qquad
\chi\sim u^{-1/2}L^{d/2}.
$$

这里的 $u^{-1/4}$ 和 $u^{-1/2}$ 说明了 dangerous 的含义：若天真地令 $u\to0$，这些量反而发散。$u$ 在 RG 下变小，但它仍以奇异振幅进入某些观测量。这也是高维 PBC 中会出现

$$
y_t^{\rm CG}=\frac d2,\qquad
y_h^{\rm CG}=\frac{3d}{4}
$$

这类零模有限尺寸指数的根源。

也可以换一种说法：高维 PBC 的 GFP+CG 两尺度图像，是对最终标度结构的描述；dangerous irrelevant variable 是在 $\phi^4$ RG 语言中解释 CG 零模为什么仍然必须保留的机制。若我们已经把自由能写成

$$
f
=
L^{-d}\tilde f_{\rm GF}(tL^2,hL^{(d+2)/2})
+
L^{-d}\tilde f_{\rm CG}(tL^{d/2},hL^{3d/4}),
$$

那么做实际数据分析时可以直接使用 GFP/CG 两扇区，而不必每一步都重新提 $u$ 的 dangerous irrelevant 性。但从理论来源看，$\phi^4$ 中的 CG 零模项正是因为 $u$ 虽然 irrelevant，却不能在零模自由能中设为零。

## 从四次项到一般高次项

下面把 $\phi^4$ 推广到 $\phi^p$。

考虑更一般的相互作用：

$$
\mathcal H[\phi]
=\int d^d x
\left[
\frac12(\nabla\phi)^2
+\frac{t}{2}\phi^2
+g_p\phi^p
-h\phi
\right].
$$

在 Gaussian 固定点，

$$
x_\phi=\frac{d-2}{2}.
$$

因此 $\phi^p$ 耦合的 RG 指数为

$$
y_p=d-px_\phi.
$$

代入 $x_\phi$ 得到

$$
y_p=d-\frac{p(d-2)}2.
$$

上临界维度由 $y_p=0$ 决定：

$$
d-\frac{p(d-2)}2=0.
$$

解得

$$
\boxed{d_c(p)=\frac{2p}{p-2}}.
$$

几个例子为：

| 相互作用 | 上临界维度 |
| --- | --- |
| $\phi^3$ | $d_c=6$ |
| $\phi^4$ | $d_c=4$ |
| $\phi^6$ | $d_c=3$ |

这里 $\phi^4$ 对应普通 Ising 或 $O(n)$ 临界点；$\phi^6$ 常出现在三临界点，因为此时 $\phi^4$ 项也需要被调到零；$\phi^3$ 常出现在缺少 $\phi\to-\phi$ 对称性的理论中。

对应的 Landau 平均场指数也可以直接求。若

$$
F(m)=L^d\left[
\frac{t}{2}m^2+g_pm^p-hm
\right],
$$

极值方程为

$$
tm+pg_pm^{p-1}-h=0.
$$

当 $h=0,t<0$ 时，

$$
m^{p-2}\sim -t,
$$

所以

$$
\boxed{\beta=\frac1{p-2}}.
$$

在 $t=0$ 时，

$$
h\sim m^{p-1},
$$

因此

$$
\boxed{\delta=p-1}.
$$

磁化率仍满足

$$
\boxed{\gamma=1}.
$$

自由能奇异部分满足

$$
f_s\sim \lvert t\rvert^{p/(p-2)}.
$$

于是

$$
\boxed{\alpha=2-\frac{p}{p-2}=\frac{p-4}{p-2}}.
$$

例如 $p=4$ 给出普通平均场指数；$p=6$ 给出三临界平均场指数：

$$
\alpha=\frac12,\qquad
\beta=\frac14,\qquad
\gamma=1,\qquad
\delta=5.
$$

## 从短程梯度到长程动量核

下面把 $k^2$ 推广到 $k^\sigma$，对应长程情况。

短程体系的 Gaussian 涨落项在动量空间中为

$$
k^2|\phi_k|^2.
$$

对于长程相互作用，低动量行为常写为

$$
k^\sigma|\phi_k|^2.
$$

对应的实空间形式可记为分数 Laplacian：

$$
\frac12\int d^d x\,
\phi(x)(-\nabla^2)^{\sigma/2}\phi(x).
$$

此时 Gaussian 泛函为

$$
\mathcal H_G
=\int d^d x
\left[
\frac12\phi(-\nabla^2)^{\sigma/2}\phi
+\frac{t}{2}\phi^2
-h\phi
\right].
$$

量纲分析从长程动能项开始：

$$
\int d^d x\,\phi(-\nabla^2)^{\sigma/2}\phi\sim 1.
$$

由于

$$
(-\nabla^2)^{\sigma/2}\sim L^{-\sigma},
$$

有

$$
L^d[\phi]^2L^{-\sigma}\sim 1.
$$

所以

$$
[\phi]\sim L^{-(d-\sigma)/2},
$$

即

$$
\boxed{x_\phi=\frac{d-\sigma}{2}}.
$$

质量项给出

$$
\boxed{y_t=\sigma}.
$$

外场项给出

$$
\boxed{y_h=\frac{d+\sigma}{2}}.
$$

四次项的指数为

$$
\begin{aligned}
y_u
&=d-4x_\phi\\
&=d-2(d-\sigma)\\
&=2\sigma-d.
\end{aligned}
$$

因此长程 $\phi^4$ 理论的上临界维度为

$$
\boxed{d_c=2\sigma}.
$$

更一般地，长程 $\phi^p$ 理论满足

$$
y_p=d-p\frac{d-\sigma}{2}.
$$

令 $y_p=0$，得到

$$
\boxed{d_c(p,\sigma)=\frac{p\sigma}{p-2}}.
$$

当 $\sigma=2$ 时，回到短程结果：

$$
d_c(p)=\frac{2p}{p-2}.
$$

长程 Gaussian 传播子满足

$$
G(k)\sim \frac1{k^\sigma}.
$$

而一般临界理论中

$$
G(k)\sim \frac1{k^{2-\eta}}.
$$

因此长程 Gaussian 区域中

$$
\boxed{\eta=2-\sigma}.
$$

> 长程模型还存在长程固定点与短程固定点之间的 crossover。简单量纲分析给出边界 $\sigma=2$，更精细的 Sak 判据会把边界修正为 $\sigma_\ast=2-\eta_{\rm SR}$。

## Wilson RG 的理论深化

Landau 与 Ginzburg 的构造给出了有效场论。Wilson RG 进一步说明这些有效理论为什么具有普适性，以及为什么低维涨落会改变平均场指数。

从 LGW 泛函出发：

$$
\mathcal H[\phi]
=\int d^d x
\left[
\frac12(\nabla\phi)^2
+\frac{t}{2}\phi^2
+\frac{u}{4!}\phi^4
-h\phi
+\cdots
\right].
$$

Wilson RG 的基本步骤如下。

第一步，将场分成慢模和快模：

$$
\phi=\phi_<+\phi_>,
$$

其中

$$
\phi_<:\ |k|<\Lambda/b,
\qquad
\phi_>:\ \Lambda/b<|k|<\Lambda.
$$

第二步，积分掉快模：

$$
e^{-\mathcal H_{\rm eff}[\phi_<]}
=\int D\phi_>\,
e^{-\mathcal H[\phi_<+\phi_>]}.
$$

第三步，重新缩放动量、坐标和场：

$$
k'=bk,\qquad x'=x/b,
$$

$$
\phi'(x')=b^{x_\phi}\phi(x).
$$

这里采用的是被动坐标写法：短波快模已经被积分掉，剩下的慢模满足 $|k|<\Lambda/b$。为了把截止重新放回 $\Lambda$，动量要放大

$$
k'=bk.
$$

动量和长度互为倒数，所以坐标同时写成

$$
x'=\frac{x}{b}.
$$

若把 $x=bx'$ 代回场，就得到更完整的写法：

$$
\phi'(x')=b^{x_\phi}\phi(bx').
$$

其中 $x_\phi$ 是场的 scaling dimension。空间坐标重新计量之后，场也要重新缩放，才能让梯度项、二点函数或传播子的规范化保持在约定形式下。

完成这些步骤后，耦合常数会发生流动：

$$
t\to t',\qquad h\to h',\qquad u\to u'.
$$

固定点满足耦合在尺度变换下保持不变。固定点附近可以线性化：

$$
t'=b^{y_t}t,\qquad h'=b^{y_h}h,\qquad u'=b^{y_u}u.
$$

若 $y>0$，该扰动为 relevant；若 $y<0$，该扰动为 irrelevant；若 $y=0$，该扰动为 marginal，需要更高阶分析。

Gaussian 固定点为

$$
u^\ast=0.
$$

在短程 $\phi^4$ 理论中，

$$
y_t=2,\qquad
y_h=\frac{d+2}{2},\qquad
y_u=4-d.
$$

因此：

- $d>4$ 时，$u$ 在长距离下衰减，平均场指数成立；
- $d=4$ 时，$u$ 为边缘变量，出现对数修正；
- $d<4$ 时，$u$ 增长，Gaussian 固定点不稳定。

当 $d<4$ 时，体系会流向 Wilson-Fisher 固定点：

$$
u^\ast\neq 0.
$$

在这个固定点，临界指数包含涨落修正。例如三维 Ising 普适类中，

$$
\nu\approx 0.630,\qquad \eta\approx 0.036.
$$

于是

$$
y_t=\frac1\nu\approx 1.587,
$$

$$
y_h=\frac{d+2-\eta}{2}\approx 2.482.
$$

这说明量纲分析能准确给出 Gaussian 固定点附近的指数和上临界维度；若体系流向相互作用固定点，真实指数需要 Wilson RG、$\epsilon$ 展开、Monte Carlo 或 bootstrap 等方法来确定。

## 总结

从最简单的 Landau 零模理论开始，可以得到平均场指数

$$
\alpha=0,\qquad
\beta=\frac12,\qquad
\gamma=1,\qquad
\delta=3.
$$

在零模有限尺寸意义下，临界涨落给出

$$
\boxed{y_t^\ast=\frac d2,\qquad y_h^\ast=\frac{3d}{4}}.
$$

加入 Ginzburg 梯度项后，Gaussian 固定点的量纲分析给出

$$
\boxed{y_t=2,\qquad y_h=\frac{d+2}{2},\qquad y_u=4-d}.
$$

短程 $\phi^4$ 理论的上临界维度为

$$
\boxed{d_c=4}.
$$

若相互作用推广为 $\phi^p$，则

$$
\boxed{d_c(p)=\frac{2p}{p-2}}.
$$

若涨落项从 $k^2$ 推广为 $k^\sigma$，则

$$
\boxed{y_t=\sigma,\qquad y_h=\frac{d+\sigma}{2},\qquad d_c=2\sigma}.
$$

更一般地，

$$
\boxed{d_c(p,\sigma)=\frac{p\sigma}{p-2}}.
$$

最后，$y_t,y_h$ 与六个常见临界指数之间的关系为

$$
\boxed{
\nu=\frac1{y_t},\quad
\alpha=2-\frac d{y_t},\quad
\beta=\frac{d-y_h}{y_t},\quad
\gamma=\frac{2y_h-d}{y_t},\quad
\delta=\frac{y_h}{d-y_h},\quad
\eta=d+2-2y_h
}.
$$

这些公式把 Landau 平均场、Ginzburg 涨落、Wilson RG 和有限尺寸标度连接在一起。实际使用时，需要先判断体系对应的固定点，再决定使用 Gaussian 指数、平均场指数，或带有涨落修正的非平庸指数。
