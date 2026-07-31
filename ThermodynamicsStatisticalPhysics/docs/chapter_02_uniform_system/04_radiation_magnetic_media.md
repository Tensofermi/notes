# 热辐射、磁介质的热学性质

**★** 对于热辐射而言，通常利用黑体模型进行讨论，即空窖模型。利用热二不难证明，空窖的内能密度$u=\frac{U}{V}$仅是温度T的函数，不随空窖的其他性质发生变化。从而得到$U(T,V)=u(T)V$.

根据电动力学中电磁波压强p与能量密度u之间的关系——*简单来说，这源于光子的能量动量关系$\varepsilon=pc$以及三维空间的测度，在统计物理中可由压强的微观表达式得到，这里先接受即可*：

$$
p=\frac{1}{3}u
$$

上式也是光子气体的“物态方程”。再利用内能对体积的依赖关系得到：

$$
\left(\frac{\partial U}{\partial V}\right)_T=T\left(\frac{\partial p}{\partial T}\right)_V-p\Rightarrow \boxed{u(T)=aT^4}\Rightarrow U=aT^4V
$$

不难看出压强和温度并不独立：$p=\frac{1}{3}aT^4$,这也是热辐射的独特之处。

对于体系的熵也不难求得：

$$
dS=\frac{1}{T}(dU+pdV)=d(\frac{4}{3}aT^3V)\Rightarrow S=\frac{4}{3}aT^3V
$$

上式考虑到$V=0$时$S=0$，故无积分常数。

有了内能和熵的表达式，不难得到：

$$
H=\frac{4}{3}aT^4V\qquad F=-\frac{1}{3}aT^4V\qquad G=0
$$

其中$G=0$体现了系统粒子数不守恒的特性，下一章将通过变分说明这一点。对于绝热过程，只需令$S=Const.$即可得到绝热方程。

类比分子动理论中的气体碰壁数$\Gamma$，热辐射系统也可引入辐射通量密度J，表示单位时间单位面积通过的辐射能量。类比严格气体碰壁数$\Gamma=\frac{1}{4}n\bar{v}$,辐射通量密度$J=\frac{1}{4}cu$,证明如下：

$$
JdA=\frac{cudA}{4\pi}\int \cos(\theta)d\Omega=\frac{cudA}{4\pi}\int_{0}^{\frac{\pi}{2}}\sin(\theta)\cos(\theta)d\theta\int_{0}^{2\pi}d\varphi =\frac{1}{4}cudA
$$

上式可以这样理解：辐射由某一点发出，呈球面向外辐射，其中$\varphi $为源点到辐射点连线的旋转轴的转角，故取值到$2\pi$。因为沿某一方向辐射的贡献为半个球面，从而$\theta$取值到$\frac{\pi}{2}$.由此得到Stefan-Boltzmann定律:

$$
J=\frac{1}{4}caT^4=\sigma T^4
$$

利用上式可以通过测量辐射通量密度，得到物体的表面温度。

**★** 对于磁介质的磁化绝热过程，由之前导出的非体积功，不难得到：

$$
dU=TdS+Vd(\frac{\mu_0 H^2}{2})+\mu_0 VHdM\approx TdS+\mu_0 Hdm
$$

上式忽略了真空中的磁场强度变化和体积变化，仅考虑磁化强度的变化。且$m=MV$为总磁矩。类比之前的热力学基本方程，相当于:

$$
p\rightarrow -\mu_0H\quad V\rightarrow m
$$

由此不难得到$dG=-SdT-m\mu_0dH$和麦氏关系$\left(\frac{\partial S}{\partial H}\right)_T=\mu_0\left(\frac{\partial m}{\partial T}\right)_H$.

类比之前定容热容的定义，这里可以定义定磁场热容。从而再利用上述麦氏关系将我们要研究的**温度随磁场变化的绝热过程**，表达为：

$$
C_H=T\left(\frac{\partial S}{\partial T}\right)_H\Rightarrow \boxed{ \left(\frac{\partial T}{\partial H}\right)_S}=-\left(\frac{\partial T}{\partial S}\right)_H\left(\frac{\partial S}{\partial H}\right)_T=\boxed{-\frac{T}{C_H}\mu_0\left(\frac{\partial m}{\partial T}\right)_H}
$$

再代入居里定律$m=\frac{CV}{T}H(C>0)$，得到：

$$
\boxed{\left(\frac{\partial T}{\partial H}\right)_S=\mu_0\frac{CVH}{TC_H}}
$$

通常上式为非负的，从而可以利用绝热去磁化制冷。注意，这里的结论来自于居里定律，当磁场过强会产生其他效应。

**★** 现在我们尝试考虑磁介质体积的变化，内能和吉布斯函数的微分式为：

$$
dU=TdS+\mu_0 Hdm-pdV\Rightarrow dG=-SdT-\mu_0mdH+Vdp
$$

从而得到麦氏关系：

$$
\left(\frac{\partial V}{\partial H}\right)_{p,T}=-\mu_0\left(\frac{\partial m}{\partial p}\right)_{H,T}
$$

上式左右联系了磁致伸缩效应和压磁效应，
