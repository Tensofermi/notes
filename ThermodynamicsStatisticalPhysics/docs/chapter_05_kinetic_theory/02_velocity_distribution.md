# 速度分布

**★** 从概率论的角度而言，Maxwell速度分布即正态分布：

$$
v_x\backsim N(0,\frac{kT}{m})\Rightarrow f(v_x)=\sqrt{\frac{m}{2\pi kT}}e^{-\frac{mv_x^2}{2kT}}\Rightarrow\boxed{f(\vec{v})=\left(\frac{m}{2\pi kT}\right)^{\frac{3}{2}}e^{-\frac{mv^2}{2kT}}}
$$

由此不难得到三维到一维空间的Maxwell速率分布：

$$
f(v)\backsim 4\pi v^2f(\vec{v})\qquad f(v)\backsim 2\pi vf(v_x)f(v_y)\qquad f(v)\backsim 2f(v_x)
$$

分别对应速度空间的球壳表面积、圆的周长、关于原点对称的两点。其中三维空间的最为常用，即：

$$
f(v)=4\pi v^2\left(\frac{m}{2\pi kT}\right)^{\frac{3}{2}}e^{-\frac{mv^2}{2kT}}
$$

利用三维速率分布，可以求出平均速率、方均根速率、最几速率：

$$
\bar{v}=\frac{\int_0^\infty vf(v)dv}{\int_0^\infty f(v)dv}=\sqrt{\frac{8kT}{\pi m}}\qquad v_{rms}=\sqrt{\frac{\int_0^\infty v^2f(v)dv}{\int_0^\infty f(v)dv}}=\sqrt{\frac{3kT}{m}}
$$

$$
f'(v)=0\Rightarrow v_p=\sqrt{\frac{2kT}{m}}
$$

**★** 根据以上公式，考虑x轴某一方向的粒子与器壁发生的碰撞，可以更加严格地导出$\Gamma$的微观表达：

$$
\Gamma=\frac{\Delta N}{\Delta A\Delta t}=\frac{n\Delta A\overline{v}_{x_+}\Delta t}{\Delta A\Delta t}=n\int_0^\infty v_xf(v_x)dv_x=n\sqrt{\frac{kT}{2\pi m}}=\frac{n\bar{v}}{4}
$$

从Maxwell分布还可以看出能量均分定理的一些启示，即有$\bar{v^2}=3\bar{v_x^2}=3\bar{v_y^2}=3\bar{v_z^2}$(注意速度和速率积分上下限的区别)：

$$
\int_0^\infty v^2f(v)\,dv=3\int_{-\infty}^\infty v_x^2f(v_x)\,dv_x=3\int_{-\infty}^\infty v_y^2f(v_y)\,dv_y=3\int_{-\infty}^\infty v_z^2f(v_z)\,dv_z=\frac{3kT}{m}
$$

**★** 此外，还有所谓玻尔兹曼分布，即对于保守场的势能$\epsilon(r) $,粒子数服从：

$$
N(r)\propto e^{-\frac{\epsilon(r) }{kT}}
$$

由此，Maxwell速度分布也可看作是$\epsilon=\frac{1}{2}mv^2 $的玻尔兹曼分布。
