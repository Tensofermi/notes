# 热力学·统计物理简述-下

> 原发布于 B 站专栏：[热力学·统计物理简述-下](https://www.bilibili.com/read/cv12346637/)
> 发布日期：2021-07-27

## 统计物理

统计物理主要围绕三大统计分布展开，最后补充一些系综理论，这便是国内的主流讲法。

**基础理论：** 将宏观物理量看作是微观物理量的统计平均，基于**等概率原理——对于处在平衡状态的孤立系统，系统各个可能的微观状态**$\Omega_i$**出现的概率是相等的，**通过某种分布$\{a_l\}$出现的**概率**来描述不同微观态对宏观物理量的贡献比例，进而有：

$\bar{A}=\frac{1}{T}\int_{0}^{T}A(t)dt\sim \sum_sA_s\frac{1}{\Omega}\sim \sum_{\{a_l\}}A_{l}\frac{\Omega_{\{a_l\}}}{\Omega}$

其中，分布$\{a_l\}$是基于能级的不同进行分类的，具体情况详见热统梳理p50的表格。由此也引入统计物理的三个基本问题: (1)如何描述系统的微观态？(2)各微观态的统计权重是多少？(3)如何计算各个热力学量？

在讨论系综之前，使用相空间$\Gamma$的子空间，即“子相空间”$\mu$的概念。这种体系称为“近独立子系”，忽略粒子与粒子之间的相互作用，但又要依靠足够小的相互作用使系统处于平衡态。

$\Gamma=\mu_1\otimes...\otimes\mu_n$

通常，讨论的粒子都是全同的，因而可以仅着眼于$\mu$空间进行分析。基于$\oint pdq=nh$带来的量子化，可以得到自由度为r的2r维$\mu$空间当中，物理量$A$的态密度$D(A)$的表达式：

$\boxed{D(A)dA=\frac{\prod_{i=1}^{r}(dq_idp_i)}{h^r}}$

由此开启了统计物理处理“权重”问题的新篇章，也为固体物理中的模式密度、能态密度等概念的引入做了铺垫。

 对于量子系统而言，如果粒子是非定域的，在运动当中其波函数会重叠，进而导致全同粒子无法分辨，根据粒子本身是玻色子还是费米子，可以分为**玻色系统**和**费米系统**。在粒子数N，能量E，体积V确定的情况下，根据热统梳理p53-p55的推导，得到B.E.分布以及F.D.分布：

$\boxed{a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}\pm1}}$

如果粒子由于定域而可以分辨，那么同理得到M.B.分布：

$\boxed{a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}}}$

 对于经典系统而言，由于无论定域与否都可分辨，故为M.B.分布，但经典系统的能级是连续的，故有：

$\omega_l\rightarrow \frac{d\omega_\mu}{h_0^r}\Rightarrow\boxed{da_l=\frac{d\omega_\mu}{e^{\alpha+\beta\varepsilon_l}h_0^r}}$

 非简并条件：当满足$\omega_l\gg a_l$或$e^{\alpha}\gg 1$时，B.E.分布和F.D.分布将退化为M.B.分布，但微观态$\Omega$却相差$N！$,这便是全同性带来的效果，也正是如此，才会造成吉布斯佯谬。由此，非定域的玻色和费米系统无法完全称为定域的玻尔兹曼系统，仅仅是分布上可以相近！

 能级准连续条件：当满足$\frac{\Delta\varepsilon}{k_BT}\ll1$时，量子的玻尔兹曼系统将过渡到经典系统，从而能级连续，进而使得求和变为积分，使计算变得简单些。

 最后，根据三种分布的数学形式，通常会遇到如下的积分，这里不加证明地给出如下公式，方便手动进行计算：

$$
\int_{0}^{\infty}\frac{x^n}{e^{bx^m}+i}\,dx
=
\underbrace{
  \overbrace{
    \underbrace{
      \frac{1}{m}\frac{\Gamma(s)}{b^s}
    }_{\mathrm{M.B.},\,i=0}
    \cdot \zeta(s)
  }^{\mathrm{B.E.},\,i=-1}
  \cdot \frac{2^s-2}{2^s}
}_{\mathrm{F.D.},\,i=1},
\qquad
s=\frac{n+1}{m},\quad i=0,\pm 1
$$

其中$s=\frac{n+1}{m}$，第一项$\Gamma(s)$为伽马函数，与阶乘的关系为：$\Gamma(s)=(s-1)!$，常用到的首项为$\Gamma(\frac{1}{2})=\sqrt{\pi}$；第二项$\zeta(s)$是黎曼zeta函数，需要记住常见的几个：

$\zeta(2)=\frac{\pi^2}{6},\zeta(4)=\frac{\pi^4}{90}$

注意事项：(1)积分区间为一维半空间，常见计算多为对全空间的积分，因而通常是要对结果乘以2的。(2)对于b的取值，需要满足$Re(b)>0$才能使用此式。(3)对于某些简单的积分，使用此式可能会出现极限不定型，因此使用之前请慎重考虑。

**M.B分布：** 考虑在服从M.B.分布的系统中，粒子处在$\varepsilon_l$能级的概率为：

$P_l=\frac{a_l}{\sum_la_l}=\frac{\omega_le^{-\alpha-\beta\varepsilon_l}}{\sum_l\omega_le^{-\alpha-\beta\varepsilon_l}}=\frac{\omega_le^{-\beta\varepsilon_l}}{\sum_l\omega_le^{-\beta\varepsilon_l}}=\frac{\omega_le^{-\beta\varepsilon_l}}{Z_1}\Rightarrow \boxed{Z_1=\sum_l\omega_le^{-\beta\varepsilon_l}}$

由此引入**粒子配分函数$Z_1$**，再根据粒子数、内能的定义以及热力学公式的类比，可以导出粒子配分函数与所有热力学量之间的关系，故只要求得了$Z_1$，所有热力学量就得到了。详细的推导见热统梳理p58-p60.

 讨论经典系统，设$x_i,x_j$为2r个广义坐标中的任意一项。利用玻尔兹曼分布可得：

$\left \langle x_i\frac{\partial \varepsilon}{\partial x_j} \right \rangle=\frac{\int x_i\frac{\partial \varepsilon}{\partial x_j} e^{-\beta\varepsilon(q,p)}d\omega}{\int e^{-\beta\varepsilon(q,p)}d\omega}=\frac{\int x_i\frac{\partial \varepsilon}{\partial x_j} e^{-\beta\varepsilon(q,p)}dx_jd\omega'}{\int e^{-\beta\varepsilon(q,p)}d\omega}=\frac{k_BT\delta_{ij}\int e^{-\beta\varepsilon(q,p)}dx_jd\omega'}{\int e^{-\beta\varepsilon(q,p)}d\omega}$

$\Rightarrow\boxed{\left \langle x_i\frac{\partial \varepsilon}{\partial x_j} \right \rangle =k_BT\delta_{ij}}$

这便是广义的**能量均分定理**。

 应用以上的概念和定理，通常讨论二能级系统、理想气体、黑体辐射和固体声子热容。

**（1）二能级系统：$Z_1=\sum_l\omega_le^{-\beta\varepsilon_l}=e^{\beta\mu B}+e^{-\beta\mu B}=2cosh(\frac{\mu B}{k_BT})$**

这里考虑两个非简并的能级$\mu B$和$-\mu B$，写出粒子配分函数之后，得到内能、热容、熵、磁矩等热力学量，进而讨论高温弱磁场、低温强磁场两种情况下的近似，并且出现“负温度”，“肖特基热容”这些有趣的物理。

**（2）理想气体：$Z_1=\int\frac{dxdydzdp_xdp_ydp_z}{h^3}e^{-\beta\frac{p_x^2+p_y^2+p_z^2}{2m}}\Rightarrow\boxed{Z_1=\frac{V}{h^3}\left(\frac{2m\pi}{\beta}\right)^{\frac{3}{2}}}$**

由于理想气体能级准连续，故将求和改为积分，写出如上的粒子配分函数，得到各个热力学量。此外，还可以讨论麦克斯韦速度分布的问题。

 当然，实际的气体不仅仅有平动，还要考虑转动、振动的问题，简单而言，可以根据能量均分定理从能量的平方项的数量得到内能、热容，但这种考量仅仅是经典的，忽略了量子效应。

$\varepsilon=\varepsilon^t+\varepsilon^r+\varepsilon^v+\varepsilon^e+\varepsilon^n$

就量子观点而言，更加全面的分析需要考虑平动能级、转动能级、振动能级、电子能级、核能级，但另一方面，由于热运动难以使得电子和核跃迁到激发态，因此电子和核被冻结在基态而不产生贡献，从而仅考虑前三项的贡献。

 转动能级需要考虑角动量量子化来计算，如果是全同的原子组成的分子气体，需要根据波函数的对称性，对转动量子数的奇偶性作出限制。最简单的例子就是氢气有正氢和仲氢的区分。

 振动能级需要利用量子谐振子进行计算，其结果与后续的声子热容是类似的。在常温近似下，可以回到由能量均分定理导出的结果。

$​\theta_n\gg\theta_e\gg\theta_v\ge k_BT\ge\theta_r$

以上是几种能级与热运动的能量的对比。

**（3）黑体辐射：** 能量均分定理对经典系统基本是适用的，但当去研究量子系统时却会出现大问题，黑体辐射便是一个很好的例证。

 由于电磁波的能量有两个平方项，从而能量为$\varepsilon=k_BT$，设能量分布的谱为$U(\omega)$，考虑横波带来的两个自由度，并根据电磁波的色散关系$\omega=ck$，得到模式密度$dn$，整理得到：

$U(\omega)d\omega=\left\langle \varepsilon \right\rangle 2dn=\boxed{k_BT\frac{L^3\omega^2}{c^3\pi^2}d\omega}$

不难发现上式的积分是发散的，并不符合$T^4$律。如果将能量量子化为$\hbar\omega$，那么：

$Z_1=\sum_{n=0}^{\infty}e^{-\frac{n\hbar\omega}{k_BT}}=\frac{e^{\frac{\hbar\omega}{k_BT}}}{e^{\frac{\hbar\omega}{k_BT}}-1}\quad\Rightarrow\quad \left\langle \varepsilon \right\rangle=\frac{\hbar\omega}{e^{\frac{\hbar\omega}{k_BT}}-1}$

进而得到：

$U(\omega)d\omega=\frac{\hbar\omega}{e^{\frac{\hbar\omega}{k_BT}}-1}\frac{L^3\omega^2}{c^3\pi^2}d\omega=\boxed{\frac{L^3}{c^3\pi^2}\frac{\hbar\omega^3}{e^{\frac{\hbar\omega}{k_BT}}-1}d\omega}$

将上式积分，便可以得到$T^4$律，说明电磁波的能量的量子化的！

**（4）固体声子热容：**

$\varepsilon_n=\left(n+\frac{1}{2}\right)\hbar\omega\quad(n=0,1,2,...)\quad\Rightarrow\quad Z_1=\sum_{n=0}^{\infty}e^{-\beta\varepsilon_n}=\frac{e^{-\frac{\beta\hbar\omega}{2}}}{1-e^{-\beta\hbar\omega}}$

 爱因斯坦假设固体原子振动的频率都相同，从而利用量子化的谐振子得到各个热力学量(也可以直接从声子出发，根据玻色统计得到内能)，解释了固体热容在0K时趋于0的实验事实，但下降的速度并不符合实验测得的$T^3$律。

 由此，德拜假设频率具有一定的分布，并且有上限(德拜频率)，并假设符合弹性波的色散关系，分为横波和纵波进行讨论，得到了符合$T^3$律的固体声子热容理论。

 这部分内容也是固体物理学的重点内容！

**F.D.分布 & B.E.分布：** 若非定域系统不满足非简并条件，那么就要使用巨配分函数，巨配分函数的导出需要从系综理论出发，这里直接给出对应的F.D.分布和B.E.分布的结果：

$B.E.\quad\Xi=\prod_l\Xi_l=\prod_l(1-e^{-\alpha-\beta\varepsilon_l})^{-\omega_l}\qquad F.D.\quad\Xi=\prod_l\Xi_l=\prod_l(1+e^{-\alpha-\beta\varepsilon_l})^{\omega_l}$

之后的讨论主要围绕弱简并$e^{\alpha}>1$和强简并$e^\alpha\leqslant1$两种情况进行。

**（1）弱简并理想气体：** 将自由粒子的色散关系代入巨配分函数的表达式中，根据弱简并条件，对难以积分成解析式的部分进行展开，从而得到：

$B.E.\qquad ln\Xi=V\left(\frac{2\pi m}{\beta h^2}\right)^{3/2}\sum_{i=1}^\infty\frac{z^{ i}}{i^{5/2}}=\frac{V}{\lambda_T^3}Li_{5/2}(z)$

$F.D.\qquad ln\Xi=-2\frac{V}{\lambda_{T}^3}Li_{5/2}(-z)$

这里假设玻色子自旋为0，费米子自旋为1/2；其中$z=e^{-\alpha}$，$Li(z)$为无穷级数展开的简化表达，由此导出内能和压强：

$U\approx\frac{3}{2}Nk_BT\left(1\pm\frac{n\lambda_{T}^3}{4\sqrt{2}}\right)\qquad p\approx nk_BT\left(1\pm\frac{n\lambda_{T}^3}{4\sqrt{2}}\right)$

玻色子取减号，费米子取加号，这表明弱简并气体存在统计关联，使得内能和压强增加或减少，这来源于全同粒子产生的量子效应。

**（2）爱因斯坦凝聚态BEC：**

$N=\frac{V}{\lambda_{T}^3}Li_{3/2}(z)>0\quad\Rightarrow\quad Li_{3/2}(z)>0\quad\Rightarrow\quad z\in[0,1]$

借用弱简并玻色理想气体的结论，粒子数的表达式如上。由于粒子数必然是大于0的正整数，故根据$ Li_{3/2}(z)$的值域，使得z限制在[0,1]当中。假设粒子数守恒，那么当温度下降时$ Li_{3/2}(z)$ 必然要上升，但$ Li_{3/2}(z)$ 的上升是有极值的，当温度过低，$ Li_{3/2}(z)$ 无法继续上升，出现粒子数减少的现象，这些粒子都去哪里了呢？原来，这些粒子都凝聚到了基态，从而对态密度无贡献，需要重新把它们考虑进来，进而计算BEC的种种性质。

**（3）光子气体：** 与之前不同，这里将电磁波看作光子气体，从强简并的玻色体系出发，写出巨配分函数：

$ln\Xi=-\sum_l\omega_lln(1-e^{-\beta\varepsilon_l})=-\int_0^\infty D(\omega)ln(1-e^{-\alpha-\beta\hbar\omega})d\omega$

$ln\Xi=-\frac{V}{c^3\pi^2}\int_0^\infty\omega^2 ln(1-e^{-\beta\hbar\omega})d\omega=\frac{\pi^2V}{45c^3}\frac{1}{(\beta\hbar)^3}$

由此直接就计算出了各个热力学量。对于辐射系统，既可以利用波动的观点，亦可利用粒子的观点，虽然两者的数学处理差异很大，但结果完全相同。这一点在分析固体热容时，既可以用谐振子的观点，也可以利用声子的观点类似。这一类将体系的波动，利用粒子的观点分析的方法叫元激发，也可理解为二次量子化或场量子化。通常在温度不太高的低能系统中比较常用，具体细节可参考凝聚态的相关书籍。

**（4）金属电子气：**

有时为了方便，求解某些热力学量时，不一定要从巨配分函数出发，而是用统计平均的思想，直接与热力学量相联系：

$\bar{N}=\sum_sf_s=\int_0^\infty f(\varepsilon)D(\varepsilon)d\varepsilon\quad U=\sum_s\varepsilon_sf_s=\int_0^\infty \varepsilon f(\varepsilon)D(\varepsilon)d\varepsilon\quad p=\frac{2U}{3V}$

考虑0K时的电子气，这时电子的分布呈现阶跃函数的形式，因而积分上限直接截断为最高的能量，记为费米能级，进而根据自由电子的能态密度计算积分，得到费米能的表达式：

$\quad\boxed{\varepsilon_F=\frac{\hbar^2}{2m_e}(3\pi^2 n)^{\frac{2}{3}}}$

可见费米能与电子的数密度$n$高度相关，并且费米能可以表达出内能和压强等热力学量。

考虑不为0K时的电子气，由于积分上限必须为无穷大，但又无法得到初等的形式，故需要通过索末菲展开公式进行近似，从而获得电子热容呈$T$律。

 这部分内容亦是固体物理学的重点内容！

**系综理论：** 系综理论直接在相空间$\Gamma$中讨论问题，并基于保守体系的正则方程：

$\frac{\partial H}{\partial p_i}=\dot{q_i}\qquad\frac{\partial H}{\partial q_i}=-\dot{p_i}\quad (i=1,2,...,f)$

这里设体系的自由度为$f$，设相空间体积元$d\Omega$，引入概率密度$\rho d\Omega$，由正则方程可以导出**刘维尔定理**：

$​\boxed{\frac{d\rho}{dt}=0}$

即表明相空间的密度不变，从而支持等概率假设。

**（1）微正则系综：** 考虑能量E，体积V，粒子数N都不变的系统，即具有孤立系统的特性。从微观态$\Omega$出发，考虑两个子系统，便可以窥见微正则系综的结构，并利用玻尔兹曼假设得到三种参数的定义：

$\boxed{S=k_Bln(\Omega)}\quad\Rightarrow\quad\boxed{\alpha=-\frac{\mu}{k_BT}\qquad\beta=\frac{1}{k_BT}\qquad\gamma=\frac{p}{k_BT}}$

此外，从微观态出发，也可以对理想气体进行简单的讨论。

不难看出，微正则系统的特性函数便是熵$S$.

**（2）正则系综：** 从微正则系综出发，考虑大热源r与系统s接触的情形，设温度T，体积V，粒子数N都不变，对应封闭系统。

$E_s+E_r=E^{(0)}\quad E_s\ll E^{(0)}$

根据系统能量远小于总能量，进而对其进行展开，从而引入配分函数$Z$(注意讨论其与粒子配分函数$Z_1$的关系)，讨论简单的涨落问题。此外，可以利用集团展开对非理想气体进行研究，详见详见李政道《统计力学》p65-p74等其他参考书。

不难看出，正则系统的特性函数便是自由能$F$.

**（3）巨正则系综：** 仍然从微正则系综出发，考虑系统与热源可以交换粒子数，设温度T，体积V，化学势μ都不变，对应开放系统。

$$
E_s+E_r=E^{(0)},\qquad E_s\ll E^{(0)},\qquad
N+N_r=N^{(0)},\qquad N\ll N^{(0)}
$$

与正则系综的推导类似，可以得到巨配分函数

$$
\Xi=\sum_N\sum_s e^{-\alpha N-\beta E_s},
$$

并讨论其涨落。此外，可以讨论吸附模型的粒子数问题；严格推导B.E.和F.D.分布的表达式，并给出巨配分函数的另一种形式，也就是之前使用的方便计算的形式。推导详见热统梳理p87-p89.

不难看出，巨正则系统的特性函数是巨势$J$.

从实用性的角度，最为常用的是正则系综和巨正则系综，而这两者的选取通常很微妙。一般的规律是：定域系统或满足非简并条件的非定域系统常用正则系综，不满足非简并条件的非定域系统常用巨正则系综。

## 补充内容

推荐科普读物《边缘奇迹——相变与临界现象》，这个方向可能也是up以后要研究的方向QAQ
