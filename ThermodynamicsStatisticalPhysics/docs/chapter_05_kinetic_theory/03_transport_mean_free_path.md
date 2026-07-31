# 输运过程、平均自由程

**★** 对于非平衡态的输运过程，这里仅讨论**粘滞(动量转移),扩散(质量转移),热传导(能量转移)**.

**■** 对于粘滞，可以从牛顿粘滞方程入手：

$$
f=\frac{dP}{dt}=-\eta\frac{du}{dz}A\Rightarrow J_p=\frac{dP}{Adt}=-\eta\frac{du}{dz}\Rightarrow \boxed{J_p=-\eta \partial_z u}
$$

$J_p$为切向动量流密度，即单位时间单位面积不同层之间转移的动量。

微观机制：流体分子由于热运动而在层流间穿行，热运动导致 的传递率各向同性，但是动量的交换不均匀，会导致动量不同的两层逐渐缩小差距。

**■** 对于扩散，要注意区分自扩散(总体质心位移不大)、互扩散(总体质心位移较大)和自由扩散(分子向真空不受阻碍的扩散)。扩散由菲克定律描述：

$$
J_N=-D\frac{dn}{dz}\Rightarrow \boxed{J_N=-D\nabla n}
$$

$J_N$为“双单”的扩散粒子数，D为扩散系数。

微观机制：分子数密度不均匀并且没有力量维持这种不均匀，于是发生层间分子质量的净交换。

**■** 对于热传导，仅仅是热传递的内容之一。至于热对流和热辐射，这里不进行讨论。热传导由傅里叶定律描述：

$$
J_T=-\kappa\frac{dT}{dz}\Rightarrow \boxed{J_T=-\kappa\nabla T}
$$

$J_T$为热流密度。类比电压、电阻和电流，热传导也有类似的式子，这里从略。

微观机制：对于气体，热运动使得不同能量的分子发生交换；对于固体和液体，主要是振动的分子发生碰撞而传递能量。

更进一步，如果用场的思想来考虑热传导问题，设体积为$V$表面积为$S$的区域，“双单”放出的热量为$f$，且该区域比热容为$c$，密度为$\rho$.用标量场$u(\vec{r},t)$来描述区域的温度，由物质增加的热量等于流进区域的热与区域内产生的热之和，可写出：

$$
\int_V{c\rho d\tau u_t}=-\oint_S\vec{J_T}\cdot\vec{n}d\sigma+\int_Vfd\tau=-\int_V\nabla\cdot\vec{J_T}d\tau+\int_Vfd\tau
$$

代入$J_T=-\kappa\nabla u$,不难得到体系的微分方程，再令区域均匀($\kappa=Const.$)且无热源($f=0$)则可化为：

$$
c\rho u_t=f+\nabla\cdot(\kappa\nabla u)\Rightarrow \boxed{u_t-\frac{\kappa}{\rho c}\nabla^2u=\frac{f}{\rho c}}\Rightarrow \boxed{u_t=\frac{\kappa}{\rho c}\nabla^2u}
$$

即得到热传导方程。

**★** 平均自由程即粒子平均两次碰撞所走的位移。定义$\bar{Z}$为单个粒子单位时间碰撞的平均次数，$\bar{v}$即单位时间平均位移，从而可以定义$\bar{\lambda}=\frac{\bar{v}}{\bar{Z}}$.

从而研究清楚$\bar{Z}$很关键，这里再引入碰撞截面的概念。设两种粒子的半径为$r_A,r_B$则之间的碰撞截面为$\sigma=\pi(r_A+r_B)^2$.现在以单个粒子为参考系：

$$
\bar{Z}=\frac{\Delta N}{\Delta t}=\frac{n\sigma \bar{v_{12}}\Delta t}{\Delta t}=\sqrt{2}n\sigma\bar{v}
$$

为了简单讨论，上式利用了同种粒子速度统计的关系式：$\overline{v}_{12}=\sqrt{2}\bar{v}$,由于与玻尔兹曼积分微分方程有关(详见汪书习题11-5)，这里直接用结论。*但对于电子，其速度过大，从而有这样的关系$\overline{v}_{12}\approx\bar{v}$.*通常而言，平均自由程为：

$$
\boxed{\bar{\lambda}=\frac{\bar{v}}{\bar{Z}}=\frac{1}{\sqrt{2}n\sigma}=\frac{kT}{\sqrt{2}\sigma p}}
$$

此外，对于稀薄气体，若容器尺度为L,则有$\bar{\lambda}\approx L$.通常粘滞对应与器壁摩擦，扩散对应泻流，热传导对应与器壁交换能量。这里不详细展开。

**★** 最后利用平均自由程粗略推导三种输运现象的系数表达式。基本假设：所有穿过分界面进行输运的分子均来自于离分界面距离等于平均自由程的地方,且默认$\Gamma=\frac{n\bar{v}}{6}$.

$$
f=\frac{dP}{dt}=\frac{\frac{1}{6}n\bar{v}Adtm(u_d-u_u)}{dt}=-\frac{\frac{1}{6}n\bar{v}Adtm \frac{du}{dz}\Delta z}{dt}=-\frac{\frac{1}{6}n\bar{v}Adtm \frac{du}{dz}2\bar{\lambda}}{dt}
$$

$$
=-\frac{1}{3}nm\bar{v}\bar{\lambda}\frac{du}{dz}A\Rightarrow \boxed{\eta=\frac{1}{3}nm\bar{v}\bar{\lambda}=\frac{1}{3}\rho \bar{v}\bar{\lambda}}
$$

$$
J_N=\frac{dN}{dtA}=\frac{\Delta\Gamma dtA}{dtA}=\frac{1}{6}\Delta n\bar{v}=\frac{1}{6}\bar{v}\left(-2\frac{dn}{dz}\bar{\lambda}\right)=
-\frac{1}{3}\bar{v}\bar{\lambda}\frac{dn}{dz}
\Rightarrow \boxed{D=\frac{1}{3}\bar{v}\bar{\lambda}}
$$

$$
J_T=\frac{dQ}{dtA}=\frac{\Gamma \Delta \bar{E}dtA}{dtA}=\frac{1}{6} n\bar{v}\Delta\bar{E_t}=\frac{1}{6}n\bar{v}\left(-2\frac{d\bar{E_t}}{dT}\frac{dT}{dz}\bar{\lambda}\right)=\frac{1}{6}n\bar{v}\left(-3k\frac{dT}{dz}\bar{\lambda}\right)=
$$

$$
-\frac{1}{2}kn\bar{v}\bar{\lambda}\frac{dT}{dz}\Rightarrow \boxed{\kappa=\frac{1}{2}kn\bar{v}\bar{\lambda}}
$$

注意，这里考虑层与层之间的输运过程，通常上层被损失，下层被获得，因而要仔细考量正负号的问题。严格的推导有些复杂，这里仅采用普物热学的方法。最后的热导率也仅考虑的单原子分子的平动动能。
