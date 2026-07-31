# 固体热容理论

**★** 与非定域的理想气体不同，固体中的粒子由于相互作用形成了稳定的结构，从而可以通过位置将粒子分辨，因而固体通常被视作定域系统。

根据能量均分定理，粒子的能量表达式相当于3个振子，具有6个平方项，从而固体热容$C_V=3Nk$.然而，实验上测得的大部分固体仅在高温下满足此式，在低温情况下将趋向于0.当然，这也是热三的必然结果.

为了调和上面的矛盾，Einstein将固体粒子的每个振子看作是量子力学中的一维谐振子，并假设其频率均为$\omega$,从而得到粒子配分函数：

$$
\varepsilon_n=\left(n+\frac{1}{2}\right)\hbar\omega\quad(n=0,1,2,...)\quad\Rightarrow\quad Z_1=\sum_{n=0}^{\infty}e^{-\beta\varepsilon_n}=\frac{e^{-\frac{\beta\hbar\omega}{2}}}{1-e^{-\beta\hbar\omega}}
$$

若固体中有N个粒子，即有3N个振子(*x,y,z三个方向*)，具有6N个平方项(*一个振子具有两个平方项*).应当注意，上式的能量是对于振子而言的，不是粒子也不是平方项，从而内能有：

$$
U=-3N\frac{\partial}{\partial\beta}ln(Z_1)=3N\frac{\hbar\omega}{2}+\frac{3N\hbar\omega}{e^{\beta\hbar\omega}-1}
$$

*如果从具有玻色子属性的“声子”的角度来看，内能实际上就是声子的零点能加上其服从玻色分布的能量的统计平均。*对内能关于温度求导可得到热容：

$$
C_V=\frac{\partial U}{\partial T}=3Nk\left(\frac{\hbar\omega}{kT}\right)^2\frac{e^{\frac{\hbar\omega}{kT}}}{(e^{\frac{\hbar\omega}{kT}}-1)^2}
$$

为了方便理解，将$\omega$也可看作某种温度，引入Einstein特征温度$\theta_E$:

$$
\theta_E=\frac{\hbar\omega}{k}\quad\Rightarrow\quad\boxed{C_V=3Nk\left(\frac{\theta_E}{T}\right)^2\frac{e^{\frac{\theta_E}{T}}}{(e^{\frac{\theta_E}{T}}-1)^2}}
$$

当取高温极限时，$T\gg\theta_E$从而$C_V\rightarrow 3Nk$;当取低温极限并且温度趋向于0时，$T\ll\theta_E,T\rightarrow0$从而$C_V\rightarrow0$.由此描述了固体热容随温度的变化，解释了实验现象。然而，由于一开始简单假设了所有振子的频率都相同，使得热容过快的趋向于0。但从量子谐振子模型出发，利用能级差$\hbar\omega$与温度$kT$的相互竞争，显现出固体不同温度下具有不同热容的图景是正确的。

**★** 基于Einstein给出的能量分布，德拜将固体看作连续介质，类比黑体辐射电磁波频率分布的推导方法，给出在低温下与实验符合非常好的德拜模型。但要注意，固体中的波动不仅仅有横波(T)，还存在纵波(L)，因而两种色散关系要分开写出：

$$
\omega=c_tk\quad\omega=c_lk
$$

与电磁波的推导类似，使用周期性边界条件，考虑到横波有两个自由度，纵波有一个自由度，从而处在$\omega\sim\omega+d\omega$范围内的振子的个数为：

$$
dn=\frac{L^3}{2\pi^2}\left(\frac{1}{c_l^3}+\frac{2}{c_t^3}\right)\omega^2d\omega=B\omega^2d\omega\quad\Rightarrow \quad B=\frac{L^3}{2\pi^2}\left(\frac{1}{c_l^3}+\frac{2}{c_t^3}\right)
$$

注意，固体中振子的个数为$3N$,从而存在截止频率$\omega_D$,称为德拜频率。

$$
\int_0^{\omega_D}B\omega^2d\omega=3N\quad\Rightarrow\quad\omega_D^3=\frac{9N}{B}
$$

从而，内能由单个振子的平均能量导出：

$$
U=\int_0^{\omega_D}\left(\frac{\hbar\omega}{2}+\frac{\hbar\omega}{e^{\beta\hbar\omega}-1}\right)B\omega^2d\omega=U_0+3NkT\mathscr{D}(x)
$$

其中：

$$
U_0=\frac{B\hbar\omega_D^4}{8}\qquad\mathscr{D}(x)=\frac{3}{x^3}\int_0^x\frac{y^3dy}{e^y-1}\qquad x=\frac{\theta_D}{T}=\frac{\hbar\omega_D}{kT}\qquad y=\frac{\hbar\omega}{kT}
$$

高温条件下$x\ll1$,从而$\mathscr{D}(x)\rightarrow1$,热容$C_V\rightarrow 3Nk$.低温条件下$x\gg1$,从而有：

$$
\mathscr{D}(x)\rightarrow\frac{3}{x^3}\int_0^\infty\frac{y^3dy}{e^y-1}=\frac{\pi^4}{15}\cdot\frac{3}{x^3}=\frac{\pi^4}{5x^3}\quad\Rightarrow\quad\boxed{C_V=3Nk\frac{4\pi^4}{5}\left(\frac{T}{\theta_D}\right)^3}
$$

此即德拜$T^3$律.对于非金属固体与实验相符，对于金属固体在低温下还要考虑自由电子对热容的贡献。此外，由于将固体视作连续介质，从而适用条件为$\lambda_D\gg a$,其中$a$为固体原子的尺度。
