# 辐射系统中的光子气体

**★** 与之前波动的观点不同，这里将辐射系统看作由全同的光子组成的系统。注意到光子化学势$\mu=0\Rightarrow e^\alpha=1$,故属于强简并的情况，从而不能使用粒子配分函数进行计算，而要使用巨配分函数。*光子的自旋为1,按常理来说应该有$-1,0,1$三种自旋态，但由于不存在一个光子的静止参考系，因此对于任何观察者来说，光都有一个运动方向，其角动量都只能绕着其运动方向进行旋转，因此就只有左旋和右旋两种自旋态。*

此外，由于上一章已经得到辐射系统的能量分布，因此本节仅仅利用巨配分函数推导系统整体的性质，体会一下巨配分函数的使用方法。

$$
ln\Xi=-\sum_l\omega_lln(1-e^{-\beta\varepsilon_l})=-\int_0^\infty D(\omega)ln(1-e^{-\alpha-\beta\hbar\omega})d\omega
$$

上式将简并度化为角频率的态密度，直接利用上一章推导的结果得到：

$$
ln\Xi=-\frac{V}{c^3\pi^2}\int_0^\infty\omega^2 ln(1-e^{-\beta\hbar\omega})d\omega=\frac{\pi^2V}{45c^3}\frac{1}{(\beta\hbar)^3}
$$

注意上式需要将$\omega^2d\omega\rightarrow \frac{1}{3}d\omega^3$进行一步分部积分，从而化为熟悉的积分形式进行计算。据此可以导出各种热力学量:

$$
U=-\frac{\partial}{\partial\beta}ln\Xi=\frac{\pi^2k^4V}{15c^3\hbar^3}T^4\qquad p=\frac{U}{3V}=\frac{\pi^2k^4}{45c^3\hbar^3}T^4
$$

$$
J_u=\frac{cU}{4V}=\frac{\pi^2k^4}{60c^2\hbar^3}T^4\qquad S=k\left(ln\Xi-\beta\frac{\partial}{\partial\beta}ln\Xi\right)=\frac{4\pi^2k^4V}{45c^3\hbar^3}T^3V
$$

注意辐射通量密度$J_u$是基于三维的效果，对于二维辐射有$J_u=\frac{cU}{\pi V}$.

**★** 对于辐射系统，既可以利用波动的观点，亦可利用粒子的观点，虽然两者的数学处理差异很大，但结果完全相同。这一点在分析固体热容时，既可以用谐振子的观点，也可以利用声子的观点类似。这一类将体系的波动，利用粒子的观点分析的方法叫元激发，也可理解为二次量子化或场量子化。通常在温度不太高的低能系统中比较常用，具体细节可参考凝聚态的
相关书籍。
