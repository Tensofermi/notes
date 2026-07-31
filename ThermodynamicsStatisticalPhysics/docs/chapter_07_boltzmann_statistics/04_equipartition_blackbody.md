# 广义能量均分定理与黑体辐射

%广义能量均分定理，应用：瑞利金斯公式

**★** 这里基于平衡态的*经典系统*，直接推导广义能量均分定理。设$x_i,x_j$为2r个广义坐标中的任意一项。利用玻尔兹曼分布可得：

$$
\left \langle x_i\frac{\partial \varepsilon}{\partial x_j} \right \rangle=\frac{\int x_i\frac{\partial \varepsilon}{\partial x_j} e^{-\beta\varepsilon(q,p)}d\omega}{\int e^{-\beta\varepsilon(q,p)}d\omega}=\frac{\int x_i\frac{\partial \varepsilon}{\partial x_j} e^{-\beta\varepsilon(q,p)}dx_jd\omega'}{\int e^{-\beta\varepsilon(q,p)}d\omega}=\frac{kT\delta_{ij}\int e^{-\beta\varepsilon(q,p)}dx_jd\omega'}{\int e^{-\beta\varepsilon(q,p)}d\omega}
$$

$$
\Rightarrow\boxed{\left \langle x_i\frac{\partial \varepsilon}{\partial x_j} \right \rangle =kT\delta_{ij}}
$$

注意，推导过程中运用了分部积分的技巧。

在使用时，常见的能量具有$\varepsilon=ax_i^2$的形式，从而有：

$$
\left\langle 2ax_i^2\right\rangle=kT\quad\Rightarrow\quad\left\langle \varepsilon\right\rangle=\frac{1}{2}kT
$$

即**粒子能量中每个平方项的平均值等于$\frac{1}{2}kT$.**

如果将$\varepsilon$改为$H$，如法炮制可得到具有相互作用的广义能量均分定理。再利用哈密顿正则方程，可以得到非常重要的**位力定理**：

$$
\boxed{\left \langle x_i\frac{\partial H}{\partial x_j} \right \rangle =kT\delta_{ij}}\quad\Rightarrow\quad \boxed{\left \langle \sum_iq_iF_i \right \rangle=-3NkT}
$$

位力定理表明系统各个自由度坐标$q_i$与对该自由度的作用力$F_i$的乘积之和为$-3NkT$,并且$\left \langle \sum_iq_iF_i \right \rangle$被称为位力。

**★** 能量均分定理对经典系统基本是适用的，但当去研究量子系统时却会出现大问题，黑体辐射便是一个很好的例证。

辐射的本质就是电磁波的发射，其所产生的效应通常是不同电磁波的统计平均的综合效果。*对于电磁波，一般有两种观点。一种是以电磁场波动的观点来看待，即用Maxwell方程组来描述，也是本节采用的观点；另一种是以粒子的观点，将光看成光子组成的“理想气体”，这将在玻色统计部分展开。**一说，对于同一频率的电磁波，由于振幅不同从而可以分辨；但从粒子的角度看，振幅的变化仅仅是全同光子个数的不同，故不可分辨。事实上，电磁波作为经典的波，属于经典系统，肯定是可分辨的。*为了数学上的方便，这里假设容器为边长为L的立方体，并采用周期性边界条件。

首先将辐射场看作无穷多单色平面波的叠加，根据周期性边界条件：

$$
k_i=\frac{2\pi}{L}n_i\qquad(i=x,y,z\quad n_i=\pm1,\pm2,...)
$$

考察波矢大小在$k\sim k+dk$范围内单色平面波的个数$dn$：

$$
dn=dn_xdn_ydn_z=\left(\frac{L}{2\pi}\right)^3dk_xdk_ydk_z=4\pi k^2\left(\frac{L}{2\pi}\right)^3dk
$$

由于电磁波为横波，因而还要考虑偏振带来的额外自由度,所以单色平面波个数应该为$2dn$.有了电磁波个数的分布，下面就要求出每个波的能量，相乘即可得出谱密度。根据电磁波的能量和能量均分定理：

$$
\left\langle \varepsilon \right\rangle=\left\langle \frac{1}{2}\varepsilon_0 E^2+\frac{1}{2}\mu_0H^2 \right\rangle=kT
$$

最后将$dk$利用色散关系$\omega=ck$换为$d\omega$，即可得到能量分布$U(\omega)d\omega$：

$$
\qquad Ud\omega=\left\langle \varepsilon \right\rangle 2dn=\boxed{kT\frac{L^3\omega^2}{c^3\pi^2}d\omega}
$$

上式即瑞利-金斯公式，虽然它在低频区与实验结果符合的非常好，但显然对频率积分会发现总的能量会发散到无穷大，并不符合$aT^4$，这便是紫外灾难。

问题出在均分定理上：普朗克假设电磁波的能量为$\varepsilon=n\hbar\omega$,从而：

$$
Z_1=\sum_{n=0}^{\infty}e^{-\frac{n\hbar\omega}{kT}}=\frac{e^{\frac{\hbar\omega}{kT}}}{e^{\frac{\hbar\omega}{kT}}-1}\quad\Rightarrow\quad \left\langle \varepsilon \right\rangle=\frac{\hbar\omega}{e^{\frac{\hbar\omega}{kT}}-1}
$$

从而得到能量分布为：

$$
Ud\omega=\frac{\hbar\omega}{e^{\frac{\hbar\omega}{kT}}-1}\frac{L^3\omega^2}{c^3\pi^2}d\omega=\boxed{\frac{L^3}{c^3\pi^2}\frac{\hbar\omega^3}{e^{\frac{\hbar\omega}{kT}}-1}d\omega}
$$

对其频率进行积分有：

$$
\int_0^\infty Ud\omega=\frac{k^4\pi^2L^3}{15c^3\hbar^3}T^4\Rightarrow u=\frac{k^4\pi^2}{15c^3\hbar^3}T^4\Rightarrow \boxed{a=\frac{k^4\pi^2}{15c^3\hbar^3}}\Rightarrow\boxed{\sigma=\frac{k^4\pi^2}{60c^2\hbar^3}}
$$

显然普朗克的假设不仅解决了紫外灾难，还定量计算出热力学中无法计算的待定系数，更是推动了量子力学的发展。
