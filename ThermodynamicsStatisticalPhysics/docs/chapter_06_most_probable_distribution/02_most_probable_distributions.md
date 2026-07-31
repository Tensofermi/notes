# 由三种状态数推导三种最概然分布

**★** 目前，仅讨论全同粒子近独立子系下，即系统的哈密顿没有相互作用的交叉项，且能量$\varepsilon_i$仅为坐标$q_i$动量$p_i$的函数：

$$
E=\sum_{i=1}^N\varepsilon_i
$$

对于更加普遍的讨论，将在系综理论中进行。

对于一个全同粒子的量子系统，需要区分两个重要的概念:**定域系统**与**非定域系统**。定域系统即粒子的运动受到限制，可以通过位置加以区分，不发生波函数的重叠；非定域系统即粒子的波函数会发生重叠，从而展现出全同粒子不可分辨的特性。定域系统典型的例子就是固体中原子的振动；非定域系统的例子为自由电子气、自由光子以及作为非简并近似的理想气体。

这两种系统有本质的区别，虽然满足一些条件其最概然分布可以相同，但系统本身不能改变。例如理想气体无论如何经典近似，都无法称为定域系统，其不可分辨性不可抹除，否则会造成Gibbs佯谬，在下一章会详细讨论。

对于经典系统，粒子都是可分辨的，因而通常没有定域与否的区别，完全服从我们日常生活经验中的统计规律。但要注意，经典系统的能级是连续的。

最后，对于量子系统，还要注意**费米子**和**玻色子**的区分。对于自旋为半整数的费米子，不仅需要考虑不可分辨性，还要考虑Pauli不相容原理对量子态占据的影响，且在自然界起着“积木”的作用；对于自旋为整数的玻色子，仅考虑不可分辨性即可，且在自然界起着“粘合积木”的作用。此外，由奇数个费米子组成的仍为费米子，如${}^3 He$;由偶数个费米子组成的将变为玻色子，如${}^ 4He$.

**★** 根据以上的概念，将定域系统称为玻尔兹曼系统，服从麦克斯韦-玻尔兹曼分布；将非定域系统分为由玻色子组成的玻色系统和由费米子组成的费米系统，分别服从玻色-爱因斯坦分布和费米-狄拉克分布，下面将基于具有确定粒子数$N$能量$E$体积$V$的孤立系统导出三种最概然分布。

首先根据等概率原理，从系统的微观状态数出发，写出粒子数$N$,能级$\varepsilon_l$，简并度$\omega_l$和给定分布$\{a_l\}$下，系统对应的微观状态数$\Omega$：

(1)对于定域的玻尔兹曼系统，由于粒子可分辨，依次填满各个能级的组合为$C_{N}^{a_1}C_{N-a_1}^{a_2}...C_{a_l}^{a_l}$.即先从$N$个粒子中选取$a_1$个，填到$\varepsilon_1$能级，再从剩下的$N-a_1$个粒子中选取$a_2$个，继续填能级，直到按照分布全部填完。其次，对于某个$\varepsilon_l$能级内部，其$a_l$个粒子在简并的$\omega_l$个量子态中任意选择，故选择结果为$\omega_l^{a_l}$种,从而对于所有能级，共有$\prod_{l}\omega_l^{a_l}$种结果。综上：

$$
\Omega_{M.B.}=C_{N}^{a_1}C_{N-a_1}^{a_2}...C_{a_l}^{a_l}\cdot\prod_{l}\omega_l^{a_l}=N!\prod_{l}\frac{\omega_l^{a_l}}{a_l!}\Rightarrow\boxed{\Omega_{M.B.}=N!\prod_{l}\frac{\omega_l^{a_l}}{a_l!}}
$$

(2)对于非定域的玻色系统，由于粒子不可分辨，从而无法进行一个个填满能级的步骤，因为无论何种方式填都被视为系统的同一个状态，从而该步骤的微观状态数为1.其次，对于某个能级$\varepsilon_l$而言，同样由于不可分辨，要用到“隔板法”来分析：对于$a_l$个粒子设置$\omega_l-1$个隔板，分成$\omega_l$份，即共有$a_l+\omega_l-1$个元素。在这些元素中选取作为粒子的选择种类为$C_{\omega_l+a_l-1}^{a_l}$种，从而对于所有能级有$\prod_{l}C_{\omega_l+a_l-1}^{a_l}$种。综上：

$$
\Omega_{B.E.}=\prod_{l}C_{\omega_l+a_l-1}^{a_l}=\prod_{l}\frac{(\omega_l+a_l-1)!}{a_l!(\omega_l-1)!}\Rightarrow\boxed{\Omega_{B.E.}=\prod_{l}\frac{(\omega_l+a_l-1)!}{a_l!(\omega_l-1)!}}
$$

(3)对于非定域的费米系统，除了粒子不可分辨，还要考虑Pauli不相容原理，即相同量子态最多仅能被一个全同粒子占据。因而填充能级与玻色系统类似，产生的微观状态数为1.其次，不相容原理自动保证了$\omega_l\geqslant a_l$,否则必然会出现量子态上有两个全同粒子。对于粒子数为$a_l$,简并度为$\omega_l$的能级$\varepsilon_l$而言，相当于在$\omega_l$个量子态中选择$a_l$个被占据的态，故为$C_{\omega_l}^{a_l}$，从而对于所有能级存在$\prod_{l}C_{\omega_l}^{a_l}$种微观状态.综上：

$$
\Omega_{F.D.}=\prod_{l}C_{\omega_l}^{a_l}=\prod_{l}\frac{\omega_l!}{a_l!(\omega_l-a_l)!}\Rightarrow\boxed{\Omega_{F.D.}=\prod_{l}\frac{\omega_l!}{a_l!(\omega_l-a_l)!}}
$$

以上给出了在分布$\{a_l\}$下，系统微观状态数$\Omega$的多少，即建立了类似于“泛函”$\Omega[\{a_l\}]$,也就是说每一种分布$\{a_l\}$都映射到了一个微观状态数$\Omega$上，类似于积分泛函$J[y(x)]$.现在的目标是求出三种系统的微观状态数$\Omega$取极大的最概然分布$\{a_l\}$，这也就类似于求出满足$\delta J[y(x)]=0$的函数$y(x)$.从而我们可以从$\delta \Omega[\{a_l\}]=0$出发，求出最概然分布。当然，数学上为了消去分式带来的麻烦，通常采用$\delta ln(\Omega[\{a_l\}])=0$的形式处理.

与分析力学的范式一样，在求出最概然分布之前，需要先明确约束条件：

$$
N=\sum_{l}a_l\qquad E=\sum_la_l\varepsilon_l\quad\Rightarrow\quad\delta N=\sum_l\delta a_l\qquad \delta E=\sum_l\varepsilon_l\delta a_l
$$

即满足粒子数和能量守恒。此外，引入拉格朗日乘子$\alpha,\beta$得到：

$$
\delta ln(\Omega)-\alpha\delta N-\beta\delta E=\delta ln(\Omega)-\alpha\sum_l\delta a_l-\beta\sum_l\varepsilon_l\delta a_l=0
$$

利用Stirling近似$ln(x!)\approx x(ln(x)-1),x\gg1$可将上式第一项近似：

(1)对于玻尔兹曼系统,代入$\Omega_{M.B.}$可得：

$$
\delta ln(\Omega_{M.B.})-\alpha\sum_l\delta a_l-\beta\sum_l\varepsilon_l\delta a_l=0
$$

化简利用到$N=\sum_la_l$,并且注意除了$a_l$以外，其他都是常量，不难得到：

$$
-\sum_l\left[ln\left(\frac{a_l}{\omega_l}\right)+\alpha+\beta\varepsilon_l\right]\delta a_l=0\Rightarrow \boxed{a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}}}
$$

从而得到了玻尔兹曼分布。

(2)对于玻色系统,代入$\Omega_{B.E.}$可得：

$$
\delta ln(\Omega_{B.E.})-\alpha\sum_l\delta a_l-\beta\sum_l\varepsilon_l\delta a_l=0
$$

再利用近似$\omega_l-1\approx\omega_l$,得到：

$$
\sum_{l}\left[ln(\omega_l+a_l)-ln(a_l)-\alpha-\beta\varepsilon_l\right]\delta a_l=0\Rightarrow\boxed{a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}-1}}
$$

从而得到了玻色分布。

(3)对于费米系统,代入$\Omega_{F.D.}$可得：

$$
\delta ln(\Omega_{F.D.})-\alpha\sum_l\delta a_l-\beta\sum_l\varepsilon_l\delta a_l=0
$$

$$
\sum_{l}\left[ln(\omega_l-a_l)-ln(a_l)-\alpha-\beta\varepsilon_l\right]\delta a_l=0\Rightarrow\boxed{a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}+1}}
$$

从而得到了费米分布。

(4)除了考虑三种量子分布，有时还需要讨论经典系统的分布。由于经典系统可分辨，可粗略地看作能级连续的定域系统，因此直接对玻尔兹曼分布进行微调即可：

$$
\omega_l\rightarrow \frac{d\omega_\mu}{h^r}\Rightarrow\Omega_{C.}=N!\prod_{l}\frac{(d\omega_\mu/h^r)^{a_l}}{a_l!}\Rightarrow\boxed{da_l=\frac{d\omega_\mu}{e^{\alpha+\beta\varepsilon_l}h^r}}
$$

注意这里$\omega_l$和$d\omega_\mu$分别表示的是量子系统的简并度和子相空间的体积元，$da_l$表示在$d\omega_\mu$范围内的粒子数，由此可以推导麦克斯韦速度分布，详见下一章。相格大小取为$h^r$，这是经典极限中保留量子态计数归一化的写法。

最概然分布的推导中默认$a_l\gg1,\omega_l\gg1$，但这显然不合理，然而最终的结果是正确的。更加严格的推导见系综理论的最后。对于引入的两个系数乘子$\alpha,\beta$可以由约束条件求出：

$$
N=\sum_{l}a_l\qquad E=\sum_la_l\varepsilon_l\quad\Rightarrow\quad to\quad get \quad\alpha\quad and\quad\beta
$$

此外，对于多组分的最概然分布的推导如法炮制，需要注意写约束条件时，各粒子体系之间可以交换能量，因而能量需要合在一起写，故$\beta$相同。

**★** 现在讨论这三种分布之间的联系，当满足$\omega_l\gg a_l$时，即单个量子态上的粒子趋向于1时，可以有如下近似：

$$
\Omega_{B.E.}=\prod_{l}\frac{(\omega_l+a_l-1)!}{a_l!(\omega_l-1)!}=\prod_{l}\frac{(\omega_l+a_l-1)...\omega_l}{a_l!}\approx\prod_l\frac{\omega^{a_l}}{a_l!}=\frac{\Omega_{M.B.}}{N!}
$$

$$
\Omega_{F.D.}=\prod_{l}\frac{\omega_l!}{a_l!(\omega_l-a_l)!}=\prod_{l}\frac{\omega_l...(\omega_l-a_l+1)}{a_l!}\approx\prod_l\frac{\omega_l^{a_l}}{a_l!}=\frac{\Omega_{M.B.}}{N!}
$$

由于$N!$为常数，从而玻色分布和费米分布退化为玻尔兹曼分布。这一点也可直接从分布的表达式中看出，当满足$e^\alpha\gg1$时：

$$
a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}\pm1}\approx \frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}}
$$

从而$a_l/\omega_l\ll1$和$e^\alpha\gg1$是等价的，均称为**非简并条件**。*但要注意，玻尔兹曼系统和由非定域系统退化而来的服从玻尔兹曼分布的系统在微观状态数上的差别，由此导致涉及微观状态数的热力学量的不同，例如熵、自由能等。*

虽然非定域和定域系统可以通过非简并条件使得最终分布一致，但非定域系统终究不能转变为定域系统，即无法添加近似条件消除不可分辨的限制。但对于量子定域系统和经典系统之间，可以通过**能级准连续条件**达到一致：

$$
\frac{\Delta\varepsilon}{kT}\ll1
$$

简单来说，就是分立的能级趋向连续，使得讨论经典系统的某些物理量时，原本的求和变为积分，从而处理起来更加方便。

**★** 上面的讨论中，分布均表示为对能级(levels)的求和，参考本章开头的表格，这显然是将量子态按照能级分类后的考量，因此还存在一种更加精细的表示方式，即对量子态(states)的求和。下面展示两种不同表示之间的区别和联系，设共有$l_t$个能级，$s_t$个量子态：

$$
\sum_{l=1}^{l_t}\omega_l=s_t \qquad N=\sum_{l=1}^{l_t}a_l=\sum_{s=1}^{s_t}n_s\qquad E=\sum_{l=1}^{l_t}\varepsilon_la_l=\sum_{s=1}^{s_t}\varepsilon_sn_s
$$

$$
a_l=\frac{\omega_l}{e^{\alpha+\beta\varepsilon_l}+i}\qquad n_s=\frac{1}{e^{\alpha+\beta\varepsilon_s}+i}\qquad(i=0,\pm 1)
$$

也就是说，占据数分布的描述有两种： $\{a_l\}$ $\{n_s\}$，$a_l$表示在能级$\varepsilon_l$上(包含简并态)，总共占据的粒子数；$n_s$表示在$\left | \psi_s  \right \rangle$量子态上，占据的粒子数。

对量子态进行求和的表示使得简并度的概念得以甩掉，因为这里的简并是对能级而言的。但如果完全采用$n_s$的分布描述来研究非定域量子系统，也会带来一些问题，例如对于确定的$\{n_s\}$会有$\Omega_{B.E.}=\Omega_{F.D.}=1$.此外，后面的系综理论中，这种类似的求和形式也经常出现，需要深入理解。

**★** 最后，根据三种分布的数学形式，通常会遇到如下的积分，这里不加证明地给出如下公式，方便手动进行计算：

$$
\int_{0}^{\infty}\frac{x^n}{e^{bx^m}+i}dx=\underbrace{\overbrace{\underbrace{\frac{1}{m}\frac{\Gamma(\heartsuit)}{b^\heartsuit}}_{M.B.i=0}\cdot\sum_{k=1}^{\infty}\frac{1}{k^\heartsuit}}^{B.E.i=-1}\cdot\frac{2^\heartsuit-2}{2^\heartsuit}}_{F.D.i=1}\quad\quad(i=0,\pm 1)
$$

其中$\heartsuit=\frac{1+n}{m}$,第一项常用到$\Gamma(x)=(x-1)!$和$\Gamma(\frac{1}{2})=\sqrt{\pi}$,且第二项相当于$\zeta(\heartsuit)$,需要记住常见的几个：

$$
\zeta(2)=\frac{\pi^2}{6},\zeta(4)=\frac{\pi^4}{90}\qquad\sum_{k=1}^\infty\frac{1}{(2k)^\heartsuit}=\frac{\zeta(\heartsuit)}{2^\heartsuit}\quad \sum_{k=1}^\infty\frac{1}{(2k-1)^\heartsuit}=\frac{2^\heartsuit-1}{2^\heartsuit}\zeta(\heartsuit)
$$

**■** 注意事项：(1)积分区间为一维半空间，常见计算多为对全空间的积分，因而通常是要对结果乘以2的(2)对于b的取值，需要满足$Re(b)>0$才能使用此式(3)对于某些简单的积分，使用此式可能会出现极限不定型，因此使用之前请慎重考虑
