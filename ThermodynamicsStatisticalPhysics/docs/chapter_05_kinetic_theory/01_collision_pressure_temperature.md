# 碰壁数、压强、温度的微观表达与范氏气体修正

**★** 分子碰壁数的推导基于以下假设：(1)分子的线度<<分子之间的距离(2)不考虑碰撞之外的作用，且分子匀速直线运动(3)处于平衡态的理想气体，与壁发生完全弹性碰撞(4)分子混沌性假设(空间各向同性)

这是一个典型的“双单”问题，即单位时间单位面积发生的物理过程。假设粒子碰壁的面积为$\Delta A$，平均速度为$\bar{v}$,数密度为$n$,可得过程经历$\Delta t$的时间对某一方向发生碰撞的粒子数为$\Delta N$,再由分子碰壁数$\Gamma$的定义得到：

$$
\boxed{\Delta N=\Delta A \bar{v}\Delta t\frac{n}{6}}\quad\Rightarrow\quad \Gamma=\frac{\Delta N}{\Delta A\Delta t}=\frac{n\bar{v}}{6}
$$

上式的$1/6$来自于混沌性假设，即三维空间六个方向碰撞方向。然而更加精确的结果应该为$1/4$，后面引入麦克斯韦分布再来推导。

下面基于类似的方法推导压强的表达式。由于假设碰壁发生的是完全弹性碰撞，从而分子碰撞前后动量改变$\Delta P=2m\bar{v}\Delta N$,从而：

$$
p=\frac{F}{\Delta A}=\frac{\Delta P}{\Delta A\Delta t}=\frac{2m\bar{v}\Delta N}{\Delta A\Delta t}=\frac{\overline{v}^2mn}{3}\approx \frac{nm\overline{v^2}}{3}\Rightarrow \boxed{p=\frac{nm\overline{v^2}}{3}}
$$

上式用到近似$\bar{v}^2\approx\bar{v^2}$.考虑分子平动动能$\bar{E_t}=\frac{1}{2}m\bar{v^2}$和理想气体方程的变形$p=nkT$
不难得到：

$$
p=\frac{nm\overline{v^2}}{3}=\frac{2n}{3}\bar{E_t}=nkT\quad\Rightarrow\quad \boxed{\bar{E_t}=\frac{3}{2}kT}
$$

上式即建立了平均平动动能仅与温度的正比关系，也是能量均分定理的基础。至此，已将宏观量$p,T$与分子的平动动能$\bar{E_t}$和数密度$n$联系起来。

**★** 这里直观地解释一下范氏气体修正项的由来，严格的推导需要用到系综理论。首先考虑$1mol$分子的体积$b$，从而对于$nmol$体积修正为$V\rightarrow (V-nb)$.其次考虑分子之间的内聚力，粗略来讲，$N$个分子之间两两组合的吸引力项为$\frac{N(N-1)}{2}\approx\frac{N^2}{2}\backsim N^2$，单位体积摩尔数为$\frac{n}{V}\backsim N$，从而可以引入系数$a$将压强项修正为$p\rightarrow (p+\frac{an^2}{V^2})$,由此得到：

$$
(V-nb)(p+\frac{an^2}{V^2})=nRT
$$
