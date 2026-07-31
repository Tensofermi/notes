# Bose气体和Fermi气体的热力学量

**★** 为了研究非定域系统，通常引入巨配分函数$\Xi$:

$$
B.E.\quad\Xi=\prod_l\Xi_l=\prod_l(1-e^{-\alpha-\beta\varepsilon_l})^{-\omega_l}\qquad F.D.\quad\Xi=\prod_l\Xi_l=\prod_l(1+e^{-\alpha-\beta\varepsilon_l})^{\omega_l}
$$

注意玻色分布和费米分布巨配分函数的正负号差异。*至于巨配分函数如此定义的动机和合理性，到下一章系综理论的最后才能说清楚，本章仅需接受这个定义即可。*对于常用的热力学量，这里也直接给出，详细过程可类比粒子配分函数或见系综理论。

$$
\overline{N}=-\frac{\partial}{\partial \alpha}ln\Xi\quad U=-\frac{\partial}{\partial\beta}ln\Xi\quad Y=-\frac{1}{\beta}\frac{\partial}{\partial y}ln\Xi\quad J=-kTln\Xi
$$

$$
S=k\left(ln\Xi-\alpha\frac{\partial}{\partial\alpha}ln\Xi-\beta\frac{\partial}{\partial\beta}ln\Xi\right)\qquad F=-kTln\Xi+kT\alpha\frac{\partial}{\partial\alpha}ln\Xi
$$

$$
S=kln(\Omega)\qquad\alpha=-\frac{\mu}{kT}
$$

**★** 在近独立最概然分布中引入的“非简并条件”表明，如果满足$e^\alpha\gg1$或$n\lambda_T^3\ll1$的条件，玻色分布和费米分布均可近似为玻尔兹曼分布来处理(*但要考虑$N!$的修正项*).数学上，巨配分函数可由粒子配分函数决定：

$$
ln\Xi=\pm\sum_l\omega_lln(1\pm e^{-\alpha -\beta\varepsilon_l})\approx\sum_l\omega_le^{-\alpha-\beta\varepsilon_l}=e^{-\alpha}Z_1
$$

如果将条件放宽一点，即满足$e^\alpha>1$，称为*弱简并条件。*这时就要考虑玻色分布和费米分布的差异性，并利用弱简并条件进行近似处理。当满足$e^\alpha\leqslant1$时，称为*强简并条件*。注意，只要非定域系统不满足非简并条件，就要用巨配分函数进行计算。*此外，由于之后系综理论中推导玻色和费米分布时，是将一般的巨配分函数利用玻色和费米系统的微观状态数$\Omega$进行形式上的改造，因而不用考虑全同性带来的$N!$修正项的问题。*

**★** 首先研究弱简并玻色气体的性质。为了方便，这里假设气体粒子自旋为0，并且仅考虑非相对论的平动情况：

$$
\varepsilon=\frac{p^2}{2m}\quad\Rightarrow\quad ln\Xi=-\sum_l\omega_lln(1-e^{-\alpha-\beta\varepsilon_l})=-\int\frac{d\omega_{\mu}}{h^3}ln(1-e^{-\alpha-\beta\varepsilon})
$$

上式用到了平动能级准连续的特性。为了方便处理积分，通常将变量换为能量，从而由态密度表达：

$$
ln\Xi=-\int_0^\infty D(\varepsilon)ln(1-e^{-\alpha-\beta\varepsilon})d\varepsilon=-\frac{2\pi V}{h^3}(2m)^{\frac{3}{2}}\int_0^\infty \varepsilon^{\frac{1}{2}}ln(1-e^{-\alpha-\beta\varepsilon})d\varepsilon
$$

为了方便处理，令$x=\beta\varepsilon>0$,从而化为：

$$
ln\Xi=-\frac{2\pi V}{h^3}(\frac{2m}{\beta})^{\frac{3}{2}}\int_0^\infty x^{\frac{1}{2}}ln(1-e^{-\alpha-x})dx=\frac{2\pi V}{h^3}(\frac{2m}{\beta})^{\frac{3}{2}}\int_0^\infty x^{\frac{1}{2}}\sum_{i=1}^\infty\frac{e^{-(\alpha+x)i}}{i}dx
$$

上式利用到了弱简并条件$e^{\alpha}>1$,即$e^{-\alpha-x}<e^{-\alpha}<1$.故对$ln(1-e^{-\alpha-x})$进行展开，由此可以将求和中的每一项进行积分，得到：

$$
ln\Xi=V\left(\frac{2\pi m}{\beta h^2}\right)^{3/2}\sum_{i=1}^\infty\frac{z^{ i}}{i^{5/2}}=\frac{V}{\lambda_T^3}Li_{5/2}(z)
$$

其中$\boxed{z=e^{-\alpha}=e^{\frac{\mu}{kT}}<1}$称为逸度，并有$n\lambda_T^3=Li_{3/2}(z)$。在弱简并极限下，才有$z\approx n\lambda_T^3$。由此得到各个热力学量：

$$
N=\frac{V}{\lambda_{T}^3}Li_{3/2}(z)\qquad U=\frac{3}{2}kT\frac{V}{\lambda_T^3}Li_{5/2}(z)\qquad p=\frac{kT}{\lambda_T^3}Li_{5/2}(z)
$$

联立上式，不难得到：

$$
U=\frac{3}{2}NkT\frac{Li_{5/2}(z)}{Li_{3/2}(z)}\approx\frac{3}{2}NkT\left(1-\frac{z}{2^{5/2}}\right)=\frac{3}{2}NkT\left(1-\frac{n\lambda_{T}^3}{4\sqrt{2}}\right)
$$

$$
p=nkT\frac{Li_{5/2}(z)}{Li_{3/2}(z)}\approx nkT\left(1-\frac{z}{2^{5/2}}\right)=nkT\left(1-\frac{n\lambda_{T}^3}{4\sqrt{2}}\right)
$$

弱简并费米气体的性质也可用类似的方法得到，不过费米子通常自旋为$\frac{1}{2}$,故要考虑自旋简并度$g=2$带来的额外自由度，从而：

$$
ln\Xi=-2\frac{V}{\lambda_{T}^3}Li_{5/2}(-z)
$$

同理不难求得各个热力学量，这里仅列出内能和物态方程的近似表达式：

$$
U\approx\frac{3}{2}NkT\left(1+\frac{n\lambda_{T}^3}{8\sqrt{2}}\right)\qquad p\approx nkT\left(1+\frac{n\lambda_{T}^3}{8\sqrt{2}}\right)
$$

不难发现，当气体满足非简并条件$n\lambda_{T}^3\ll1$时，玻色和费米气体的物态方程均退化为之前的经典理想气体的情况。此外，对比玻色气体和费米气体的内能，不难看出玻色气体之间似乎有某种相互的吸引力，使得内能降低；而费米气体则有相互排斥的力，使得内能增大。这便是有趣的*统计关联*，也就是量子力学中的交换力效应，完全是由于粒子的全同性所要求的波函数的对称和反对称所引起的。

至于强简并气体的讨论，将在下面几节展开。
