# 金属中的自由电子气体

**★** 本节研究金属中的自由导电电子的特性，由于其弥散在整个金属内，故可以将它们看作自由电子气体。利用铜原子的数据，并假设一个铜原子贡献一个电子，得到$n\lambda_T^3\approx3400\gg1$,故为强简并情况。

电子的自旋为$\frac{1}{2}$,从而自旋自由度为2.这里假设电子的速度不够快，从而满足经典的能量动量关系。故一个量子态上的平均电子数为：

$$
f(\varepsilon)=\frac{1}{e^{(\varepsilon-\mu)/kT}+1}\qquad \varepsilon=\frac{p^2}{2m}\qquad D(\varepsilon)=\frac{4\pi V}{h^3}(2m)^{\frac{3}{2}}\varepsilon^{\frac{1}{2}}
$$

有时为了方便，求解某些热力学量时，不一定要从巨配分函数出发，而是用统计平均的思想，直接与热力学量相联系：

$$
\bar{N}=\sum_sf_s=\int_0^\infty f(\varepsilon)D(\varepsilon)d\varepsilon\quad U=\sum_s\varepsilon_sf_s=\int_0^\infty \varepsilon f(\varepsilon)D(\varepsilon)d\varepsilon\quad p=\frac{2U}{3V}
$$

由此可见，确定$f(\varepsilon)$和$D(\varepsilon)$的形式十分重要。

**★** 首先考虑$T=0K$的理想情况，设此时化学势为$\mu(0)$,那么$f(\varepsilon)$在$\varepsilon<\mu(0)$的值为1，在$\varepsilon>\mu(0)$的值为0,相当于一个阶跃函数。从物理上讲，当$T=0K$电子会尽可能占据最低的能级，但由于泡利不相容原理，两个电子不能占据同一个量子态，进而使得电子可以占据较高的能级，而最高的能级被称为*费米能级*，记作$\varepsilon_F$,也就是这里$0K$的化学势$\mu(0)$.根据总电子数$N$：

$$
N=\int_0^\infty f(\varepsilon)D(\varepsilon)d\varepsilon=\int_0^{\mu(0)} D(\varepsilon)d\varepsilon=\frac{8\pi V}{3h^3}[2m\mu(0)]^{\frac{3}{2}}
$$

$$
\Rightarrow\quad\boxed{\varepsilon_F=\mu(0)=\frac{\hbar^2}{2m}(3\pi^2 n)^{\frac{2}{3}}}
$$

由费米能级，可以引出费米动量、费米速度和费米温度：

$$
p_F=\sqrt{2m\varepsilon_F}=\hbar(3\pi^2n)^{\frac{1}{3}}\qquad v_F=\frac{p_F}{m}\qquad T_F=\frac{\varepsilon_F}{k}
$$

可见，除常数外，体密度$n$在这些量中起决定性作用。*可知，电子的动能与$n^{\frac{2}{3}}$成正比；电子之间的相互作用能，由于体密度为3维的，故与$\frac{1}{r}\sim n^{\frac{1}{3}}$成正比。从而体密度$n$越大，相互作用越容易忽略，从而越接近理想气体。与之相反，若体密度$n$很小，则会出现维格纳晶格的现象*

既然$\mu(0)$已经求出，即可利用统计平均的方法得到内能和压强：

$$
U=\int_0^\infty \varepsilon f(\varepsilon)D(\varepsilon)d\varepsilon=\int_0^{\mu(0)} \varepsilon D(\varepsilon)d\varepsilon=\frac{3}{5}N\mu(0)
$$

$$
p(0)=\frac{2U}{3V}=\frac{2}{5}n\mu(0)
$$

**★** 现在考察$T\neq0K$的情况，根据总电子数$N$和内能$U$的统计平均：

$$
N=\int_0^\infty f(\varepsilon)D(\varepsilon)d\varepsilon=\frac{4\pi V}{h^3}(2m)^{\frac{3}{2}}\int_0^\infty\frac{\varepsilon^{\frac{1}{2}}d\varepsilon}{e^{(\varepsilon-\mu)/kT}+1}
$$

$$
U=\int_0^\infty \varepsilon f(\varepsilon)D(\varepsilon)d\varepsilon=\frac{4\pi V}{h^3}(2m)^{\frac{3}{2}}\int_0^\infty\frac{\varepsilon^{\frac{3}{2}}d\varepsilon}{e^{(\varepsilon-\mu)/kT}+1}
$$

对于上式的积分，可以直接套用*索末菲展开*的公式：

$$
\int_{-\infty}^{\infty}\frac{H(\varepsilon)}{e^{\beta(\varepsilon-\mu)}+1}d\varepsilon=\int_{-\infty}^\mu H(\varepsilon)d\varepsilon+\frac{\pi^2}{6}\left(\frac{1}{\beta}\right)^2 H'(\mu)+O\left(\frac{1}{\beta\mu}\right)^4
$$

可以将$H(\varepsilon)$处理成分段函数，即$\varepsilon<0$时，$H(\varepsilon)=0$;而$\varepsilon\geqslant0$时，$H(\varepsilon)$为$\varepsilon^{\frac{1}{2}}$或$\varepsilon^{\frac{3}{2}}$,为了表达方便令$C=\frac{4\pi V}{h^3}(2m)^{\frac{3}{2}}$,不难得到：

$$
N=\frac{2}{3}C\mu^{\frac{3}{2}}\left[1+\frac{\pi^2}{8}\left(\frac{kT}{\mu}\right)^2\right]\qquad U=\frac{2}{5}C\mu^{\frac{5}{2}}\left[1+\frac{5\pi^2}{8}\left(\frac{kT}{\mu}\right)^2\right]
$$

由此也可解出化学势：

$$
\mu=\left(\frac{3N}{2C}\right)^{\frac{2}{3}}\left[1+\frac{\pi^2}{8}\left(\frac{kT}{\mu}\right)^2\right]^{-\frac{2}{3}}\approx\mu(0)\left[1+\frac{\pi^2}{8}\left(\frac{kT}{\mu(0)}\right)^2\right]^{-\frac{2}{3}}\approx\mu(0)\left[1-\frac{\pi^2}{12}\left(\frac{kT}{\mu(0)}\right)^2\right]
$$

为了得到化学势$\mu$随温度的显式，这里将第二项的$\mu$近似为$\mu(0)$,并进行多项式近似得到上述表达式。可见化学势随着温度上升而下降。由此，可导出金属中电子贡献的热容：

$$
U\approx\frac{3}{5}N\mu(0)\left[1+\frac{5}{12}\pi^2\left(\frac{kT}{\mu(0)}\right)^2\right]\quad\Rightarrow\quad C_V^e=\left(\frac{\partial U}{\partial T}\right)_V=Nk\frac{\pi^2kT}{2\mu(0)}=\gamma_0T
$$

可见，电子热容与温度是正比关系，结合之前德拜固体热容的理论，可将金属低温热容表达如下：

$$
C_V=\gamma_0T+AT^3
$$
