# 利用粒子配分函数推导热力学量

**★** 考虑在服从玻尔兹曼分布的系统中，粒子处在$\varepsilon_l$能级的概率为：

$$
P_l=\frac{a_l}{\sum_la_l}=\frac{\omega_le^{-\alpha-\beta\varepsilon_l}}{\sum_l\omega_le^{-\alpha-\beta\varepsilon_l}}=\frac{\omega_le^{-\beta\varepsilon_l}}{\sum_l\omega_le^{-\beta\varepsilon_l}}=\frac{\omega_le^{-\beta\varepsilon_l}}{Z_1}\Rightarrow \boxed{Z_1=\sum_l\omega_le^{-\beta\varepsilon_l}}
$$

这里引入**粒子配分函数**$Z_1$，可见其作用相当于归一化因子。此外，注意其角标$1$表示单粒子的意思，原因在于目前的讨论都基于子相空间，子系统都是单粒子，之后系综理论当中还会出现(系统)配分函数$Z$和巨配分函数$\Xi$等.

热力学量有两类，一类直接与微观量有对应，从而求出相应微观量的统计平均，就得出此热力学量，例如内能、广义力；另一类与微观量没有直接对应，需要利用热力学公式类比求出，例如热量、熵。

基于$Z_1(\beta,y)$为$\beta$和外参量$y$的函数，将基本热力学量进行改写，首先从体系的内能和粒子数入手：

$$
N=\sum_la_l=e^{-\alpha}\sum_l\omega_le^{-\beta\varepsilon_l}=e^{-\alpha}Z_1\Rightarrow\boxed{e^{-\alpha}=\frac{N}{Z_1}}
$$

$$
U=\sum_l\varepsilon_la_l=e^{-\alpha}\sum_l\varepsilon_l\omega_le^{-\beta\varepsilon_l}=e^{-\alpha}\left(-\frac{\partial}{\partial\beta}\right)\sum_l\omega_le^{-\beta\varepsilon_l}
$$

联立以上两式，即用代换$e^{-\alpha}=\frac{N}{Z_1}$得到：

$$
U=\frac{N}{Z_1}\left(-\frac{\partial}{\partial\beta}\right)Z_1=-N\left(\frac{\partial}{\partial\beta}\right)ln(Z_1)\Rightarrow\boxed{U=-N\frac{\partial}{\partial\beta}ln(Z_1)}
$$

根据微观过程的能量守恒，即外界对系统做功等于系统微观能量的增量：

$$
Ydy=\sum_la_l\frac{\partial\varepsilon_l}{\partial y}dy
$$

从而可将广义力改写如下：

$$
\Rightarrow Y=\sum_la_l\frac{\partial\varepsilon_l}{\partial y}=e^{-\alpha}\sum_l\frac{\partial\varepsilon_l}{\partial y}\omega_le^{-\beta\varepsilon_l}=e^{-\alpha}\sum_l\frac{\partial\varepsilon_l}{\partial y}\omega_l\frac{-1}{\beta}\frac{\partial}{\partial \varepsilon_l}e^{-\beta \varepsilon_l}
$$

$$
\Rightarrow Y=e^{-\alpha}\left(-\frac{1}{\beta}\frac{\partial}{\partial y}\right)\sum_l\omega_le^{-\beta \varepsilon_l}\Rightarrow\boxed{Y=-\frac{N}{\beta}\frac{\partial}{\partial y}ln(Z_1)}
$$

由此得到广义力$Y$基于$Z_1$的表达式。为了形象理解，以压强为例：$\delta W=Ydy=-pdV=pd(-V)$由于目标是求出不带负号的$p$，从而必须将负号丢给$dV$，这里的细节需要深刻理解，经常要用到。从而有:

$$
p=\frac{N}{\beta}\frac{\partial}{\partial V}ln(Z_1)
$$

注意以上求出的$U$和$Y$的表达式，本质上都是对与之相应的微观量进行统计平均，并统一地用$Z_1$进行表达而已。与此不同，熵$S$没有直接对应的微观量，无法进行统计平均，而需要热力学公式的类比才能导出：

对比内能的宏观与微观表达式，将广义力做功的表达式代入可看出：做功改变系统能级本身的大小，吸热改变系统不同能级上的粒子数，即：

$$
dU=\delta Q+\delta W=\sum_l\varepsilon_lda_l+\sum_la_ld\varepsilon_l\Rightarrow \delta W=\sum_la_ld\varepsilon_l
$$

$$
\Rightarrow\delta Q=dU-\delta W=dU-Ydy=\sum_l\varepsilon_lda_l
$$

一方面，热力学部分中提到，温度$T$的倒数为$\delta Q$的积分因子，即:$dS=\frac{1}{T}\delta Q$.另一方面，拉格朗日乘子$\beta$也为$\delta Q$的积分因子，证明如下：(为了方便运算，这里采用$\delta Q=dU-Ydy$)

$$
\beta\delta Q=\beta(dU-Ydy)=-N\beta d\left(\frac{\partial ln(Z_1)}{\partial \beta}\right)+N\frac{\partial ln(Z_1)}{\partial y}dy
$$

根据$ln(Z_1)$的全微分，可将上式凑成全微分的形式：

$$
dln(Z_1)=\frac{\partial ln(Z_1)}{\partial\beta}d\beta+\frac{\partial ln(Z_1)}{\partial y}dy\quad\Rightarrow\quad \beta\delta Q=Nd\left(ln(Z_1)-\beta\frac{\partial ln(Z_1)}{\partial \beta}\right)
$$

由此即证$\beta$也为$\delta Q$的积分因子。根据微分方程理论，两个积分因子的比值为熵的全微分的函数，设这个函数为$k(S)$,称为玻尔兹曼常数，从而：

$$
\beta=\frac{1}{k(S)T}
$$

上一章提到，多种分的最概然分布当中$\beta$相同，即当多个系统相互接触达到平衡态时，拥有共同的$\beta$，由此否认了$\beta$会随熵$S$变化。进而$k(S)$也为常量函数，实验上测得为$1.38\times10^{-23}J/K$.由此根据$dS=\frac{\delta Q}{T}$得到熵的表达式：

$$
dS=k\beta\delta Q=kNd\left(ln(Z_1)-\beta\frac{\partial ln(Z_1)}{\partial \beta}\right)
$$

根据绝对熵$S_0=0$的规定，积分结果为：

$$
\boxed{S=Nk\left(ln(Z_1)-\beta\frac{\partial}{\partial \beta}ln(Z_1)\right)}
$$

至此，玻尔兹曼分布下的基本热力学量都已经完全与$Z_1$建立联系了，其他热力学量均可由此导出。例如常用到的自由能$F$:

$$
F=U-TS=-NkTln(Z_1)\Rightarrow\boxed{F=-NkTln(Z_1)}
$$

类比$F(T,V)$和$Z_1(\beta,y)=Z_1(\frac{1}{kT},V)$,其变量仅仅差了玻尔兹曼常数$k$，这样也就不难理解为何两者形式如此相像。

此外，应当注意以上都是基于定域系统讨论的结果，当系统是通过非简并条件近似为玻尔兹曼分布的非定域系统时，一定要考虑其系统微观状态数$\Omega$的影响，这就涉及到玻尔兹曼关系的问题。

**★** 对常用代换$e^{-\alpha}=\frac{N}{Z_1}$两边取对数得到：$ln(Z_1)=ln(N)+\alpha$,代入熵的表达式当中,消去$Z_1$项：

$$
S=k(Nln(N)+\alpha N+\beta U)=k\left[Nln(N)+\sum_l(\alpha+\beta\varepsilon_l)a_l\right]
$$

代入玻尔兹曼分布$a_l=\omega_le^{-\alpha-\beta\varepsilon_l}$,并且逆向使用Stirling公式：

$$
S=kln(\Omega_{M.B.})\Rightarrow \boxed{S=kln(\Omega)}
$$

上式表明在玻尔兹曼系统中，熵与微观状态数有直接的关系，并将这一特性推广到任意系统，称为**玻尔兹曼关系**。

由此不难想见，对于通过非简并条件近似为玻尔兹曼分布的非定域系统，由于其微观状态数与定域系统相差$N!$倍，从而涉及$\Omega$的熵以及与熵相关的表达式都应进行修正：

$$
\Omega=\Omega_{B,E}=\Omega_{F.D.}=\frac{\Omega_{M.B.}}{N!}\Rightarrow S=kln(\Omega)=kln(\Omega_{M.B.})-kln(N!)
$$

即只需在之前导出的熵的基础之上，减去$kln(N!)$即可。同时，自由能也可根据定义进行修改：

$$
\boxed{S'=S-kln(N!)\qquad F'=F+kTln(N!)}
$$

由此可见，在求系统的热力学量时，首先要明确的是系统的定域性。*此外，系综理论中将以上的修正项都封装在配分函数$Z$当中了，并且$N!$仅仅出现在非定域系统满足非简并条件的热力学量中，从而系统可以近似为玻尔兹曼分布。但对于强简并系统，所使用的巨配分函数就不用考虑此项。*

事实上，熵除了以上的表达形式，还有很多的等价表达。例如可以利用粒子处在$s$态的概率$P_s$来表达：

$$
P_s=\frac{e^{-\alpha-\beta\varepsilon_s}}{N}=\frac{e^{-\beta\varepsilon_s}}{Z_1}\Rightarrow S=Nk\left(ln(Z_1)-\beta\frac{\partial}{\partial \beta}ln(Z_1)\right)
$$

设粒子平均能量为$\bar{\varepsilon}=\frac{U}{N}$并利用$\sum_sP_s=1$,则：

$$
S=Nk\left(ln(Z_1)+\beta\bar{\varepsilon}\right)=Nk\left(ln(Z_1)\sum_sP_s+\beta\sum_sP_s\varepsilon_s\right)=Nk\sum_sP_s(ln(Z_1)+\beta\varepsilon_s)
$$

对$P_s$的定义式取对数，代入得到：

$$
ln(P_s)=-\beta\varepsilon_s-ln(Z_1)\Rightarrow\boxed{S=-Nk\sum_sP_slnP_s}
$$

上式的启发意义颇大，表明熵的大小可以理解为信息缺乏的度量。此外，将$P_s$换为其他形式的概率，类似的熵的基本形式也不变，如信息熵、纠缠熵。

**★** 最后，我们对经典的粒子配分函数进行讨论。经典系统的特征就是能级准连续，根据准连续条件，得到能级占据的分布，进而得到粒子配分函数：

$$
\frac{\Delta\varepsilon}{kT}\ll1\Rightarrow da_l=\frac{d\omega}{h^r}e^{-\alpha-\beta\varepsilon_l}\Rightarrow \boxed{Z_1=\int\frac{d\omega}{h^r}e^{-\beta\varepsilon_l}}
$$

以上利用经典系统能级的连续性，将求和写为积分形式。在分析例如理想气体能级准连续的系统时，常常会用到此式。
