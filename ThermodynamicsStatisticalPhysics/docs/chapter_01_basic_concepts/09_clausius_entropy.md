# 克劳修斯不等式、熵的概念、熵增原理

**★** 根据卡诺定理$\eta_{\text{可逆}}\geqslant\eta_{\text{未知热机}}$再由两不同热源间的最大效率为卡诺循环的效率得到$1-\frac{T_2}{T_1}\geqslant 1-\frac{Q_2}{Q_1} \Rightarrow \frac{Q_1}{T_1}-\frac{Q_2}{T_2}\leqslant0$

这里将之前卡诺循环中的$Q_2$定义成吸收$T_2$热源的热量，使得$Q$的正负号含义统一，则得到克劳修斯不等式：

$$
\frac{Q_1}{T_1}+\frac{Q_2}{T_2}\leqslant0
$$

上式不难推广到n个不同热源的情况，并得到连续的情形：

$$
\sum_{i=1}^{n}\frac{Q_i}{T_i}\leqslant0\Rightarrow\boxed{ \oint \frac{\delta Q}{T}\leqslant0}
$$

其中$\delta Q$为从温度$T$的热源吸收的热量，此即为克劳修斯不等式。

**★** 为了简单，可以从**可逆过程**入手，讨论克劳修斯不等式取等号的情况，从而引入熵的概念。

$$
\oint_{C}\frac{\delta Q}{T}=0\Rightarrow \int_{C_1}^{A\to B}\frac{\delta Q}{T}+\int_{C_2}^{B\to A}\frac{\delta Q}{T}=0
$$

其中$C_1$和$C_2$为C曲线的一个划分，可以表示两个起点和终点相同但过程不同的积分：

$$
\int_{C_1}^{A\to B}\frac{\delta Q}{T}=-\int_{C_2}^{B\to A}\frac{\delta Q}{T}=\int_{C_2}^{A\to B}\frac{\delta Q}{T}=Const.
$$

表明此积分只与初末的状态有关，与具体过程无关，**因而可以定义熵这个态函数**:

$$
\boxed{S_B-S_A=\int_{A}^{B}\frac{\delta Q}{T}}\Rightarrow \boxed{dS=\frac{\delta Q}{T}}
$$

可见T为$\delta Q$的积分因子,**且由于可逆过程热平衡，这里的T为系统的温度**。

**★** 讨论熵增之前，先要讨论初末状态为平衡态的**不可逆过程**。设不可逆过程A到B，并伴随一个可逆过程B到A，则有：

$$
\oint_{C}\frac{\delta Q_{\text{不可逆}}}{T}< 0\Rightarrow \int_{A}^{B}\frac{\delta Q_{\text{不可逆}}}{T}+\int_{B}^{A}\frac{\delta Q_{\text{可逆}}}{T}<0
$$

同理得到：

$$
\int_{A}^{B}\frac{\delta Q_{\text{不可逆}}}{T}<\int_{A}^{B}\frac{\delta Q_{\text{可逆}}}{T}=S_B-S_A\Rightarrow
\boxed{S_B-S_A> \int_{A}^{B}\frac{\delta Q_{\text{不可逆}}}{T}}\Rightarrow \boxed{dS>\frac{\delta Q_{\text{不可逆}}}{T}}
$$

**★** 综上，得到热二的数学表述：**(注意以下的T为环境热源的温度)**

$$
\boxed{S_B-S_A\geqslant \int_{A}^{B}\frac{\delta Q}{T}}\Rightarrow \boxed{dS\geqslant\frac{\delta Q}{T}}
$$

考虑**绝热过程**，有$\delta Q=0$,得到熵增原理：

$$
\boxed{dS\geqslant0}
$$

**表明在绝热过程(孤立系)条件下，熵永不减少。**对于任何体系，均可将之扩展成孤立系，从而使用熵增原理，此外，其也与热二等价。

- 注意熵增原理的条件为绝热过程，并且$\Delta S$是否等于零可以作为**绝热过程可逆性的判据。**其他过程则要与$\frac{\delta Q}{T}$进行比较。
- 由于表达式中$\delta Q$与系统质量成正比，因而熵是一个广延量
- 对于可逆过程，之前用p-V分析过程的想法来源于$\delta W=-pdV$。引入熵后，有$\delta Q=TdS$因而可以用T-S图分析。例如卡诺循环的T-S图就是封闭的矩形，其封闭曲线的面积即吸收的热量,又由于$\Delta U=0$所以也为系统对外作的功。

**★** 最大功的温度问题：两个温度分别为$T_1$和$T_2$的**完全相同**的热源，且**忽略体积变化**。热源之间存在热机，求最终两热源热平衡温度$T_f$的范围。

这里的切入点在于**将两个热源看成一个绝热封闭的系统**，因为只能通过对外做功一种方式改变内能,即$\Delta U=-W_{\text{系统对外}}$.这里可以通过调节W来进行分析，当做功为0时，由于内能不变，故$\Delta U=0$.当做最大功时，为可逆热机，由$dS\geqslant0$取等条件，从而满足$\Delta S=0$.设热源的热容为$C_V$可得：

$$
\Delta U=C_V(2T_f-T_1-T_2)\qquad \Delta S=C_Vln(\frac{T_f^2}{T_1T_2})
$$

再利用$\Delta U=0$和$\Delta S=0$求得$T_f$的上下限即可，得到：

$$
\sqrt{T_1T_2}\leqslant T_f\leqslant \frac{T_1+T_2}{2}
$$

注意，以上结果忽略了体积变化带来的影响，且默认热容不变。
