# 相空间与刘维尔定理

**★** 若所研究的系统由*相互作用*的多种粒子组成，第$i$种粒子的自由度为$r_i$,粒子数为$N_i$,从而系统的自由度为$f=\sum_ir_iN_i$,所对应相空间$\Gamma$的维数为$2f$.系统状态由相空间中代表点$(q_1,...,q_f,p_1,...,p_f)$表示，并由正则方程：

$$
\frac{\partial H}{\partial p_i}=\dot{q_i}\qquad\frac{\partial H}{\partial q_i}=-\dot{p_i}\quad (i=1,2,...,f)
$$

确定代表点的轨迹，即系统状态随时间的变化。为了区分子相空间中的体积元$d\omega$,相空间中采用$d\Omega$表示体积元：

$$
\rho(q_1,...q_f,p_1,...,p_f,t)dq_1...dq_fdp_1...dp_f=\rho(q_1,...q_f,p_1,...,p_f,t)d\Omega
$$

其中$\rho d\Omega$表示系统代表点在$d\Omega$处出现的概率，称为系统微观状态的**概率密度**。结合概率密度的一般性质，有：

$$
\int\rho d\Omega=1\qquad\bar{A}=\int A\cdot\rho d\Omega
$$

分别表示概率归一化和力学量$A$的统计平均。从而，求解$\rho$的具体表达式，便是统计物理的核心任务。

有时还会引入**代表点密度**$\widetilde{\rho}$.从而$\widetilde{\rho}d\Omega$表示在$d\Omega$范围内，代表点的个数，也就是系统微观状态的个数。设$\mathscr{N}$为系统微观态的总数，从而：

$$
\rho d\Omega=\frac{\widetilde{\rho}d\Omega}{\int\widetilde{\rho}d\Omega}=\frac{\widetilde{\rho}d\Omega}{\mathscr{N}}\propto\widetilde{\rho}d\Omega\qquad\int\widetilde{\rho}d\Omega=\mathscr{N}
$$

可见$\rho d\Omega$与$\widetilde{\rho}d\Omega$成正比关系。

**★** 通常来说，为了研究一枚硬币投掷后出现正反面的概率，会将硬币在一个时间段内反复投掷，统计两种状态出现的次数，从而计算硬币两种状态出现的概率。然而，这种做法必然涉及到利用时间来区分投掷的次数，从而对时间形成依赖。为了摆脱对时间的依赖，可以在同一时刻投掷大量相同的硬币，从而一次性得出结果。如果将“硬币”视作我们所研究的“系统”，那么“大量相同的硬币”即为“系综”的对应。可见，系综仅仅是一个概念性质的工具，引入的目的是用系综平均来代替时间平均。

进一步说，按照系综的精神，系综可以看作是所研究的系统在一定宏观条件下的各种微观状态的“化身”。那么$\mathscr{N}$个微观状态就对应着$\mathscr{N}$个假想的系统，它们组成的集合就是系综。

**★** 设系统的哈密顿量$H(q_1,...,q_f,p_1,...,p_f)$不显含时间$t$，即系统为*保守系*。为了方便理解，利用$\rho d\Omega$与$\widetilde{\rho}d\Omega$成正比的性质，先讨论代表点密度$\widetilde{\rho}$，并定义相空间中的坐标$\vec{r}$和速度$\vec{v}$：

$$
\vec{r}=(q_1,...,q_f,p_1,...,p_f)\qquad\vec{v}=(\dot{q_1},...,\dot{q_f},\dot{p_1},...,\dot{p_f})
$$

类比流密度守恒的表达式有：

$$
-\frac{\partial\widetilde{\rho}}{\partial t}=\nabla\cdot(\widetilde{\rho}\vec{v})=\nabla\widetilde{\rho}\cdot\vec{v}+\widetilde{\rho}\nabla\cdot\vec{v}=\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial q_i}\dot{q_i}+\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial p_i}\dot{p_i}+\widetilde{\rho}\left(\sum_{i=1}^f\frac{\partial\dot{q_i}}{\partial q_i}+\sum_{i=1}^f\frac{\partial\dot{p_i}}{\partial p_i}\right)
$$

代入保守系的正则方程，并默认二阶偏导可交换，则有：

$$
=\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial q_i}\dot{q_i}+\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial p_i}\dot{p_i}+\widetilde{\rho}\left(\sum_{i=1}^f\frac{\partial^2H}{\partial q_i\partial p_i}-\sum_{i=1}^f\frac{\partial^2H}{\partial p_i\partial q_i}\right)=\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial q_i}\dot{q_i}+\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial p_i}\dot{p_i}
$$

$$
\Rightarrow-\frac{\partial\widetilde{\rho}}{\partial t}=\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial q_i}\dot{q_i}+\sum_{i=1}^f\frac{\partial\widetilde{\rho}}{\partial p_i}\dot{p_i}
$$

从而得到：

$$
\Rightarrow\frac{d\widetilde{\rho}}{dt}=\frac{\partial \widetilde{\rho}}{\partial t}+\sum_{i=1}^f\left(\frac{\partial \widetilde{\rho}}{\partial q_i}\dot{q_i}+\frac{\partial \widetilde{\rho}}{\partial p_i}\dot{p_i}\right)=0
$$

*这就是刘维尔定理，又称为密度不变或流体不可压缩定理。刘维尔定理对等概率假设是个有力的支持。相空间中的一个系统的不同微观状态用代表点表示，如果这些点在某一时刻是均匀分布的，则在任何时刻也是均匀的，既不扩张，也不会缩小。这是相密度守恒的自然结果。相密度的物理意义是表示在某时刻在相等的体积内找到的概率量度。所以，密度不变即表示等概率假设是成立的。*

也就是说，根据正比关系，也可以表述如下：

$$
\boxed{\frac{d\rho}{dt}=0}
$$

此外要注意两点(1)$\frac{d\rho}{dt}=0$表示两个区域的概率密度不随时间变化；$\frac{\partial\rho}{\partial t}=0$表示同一区域的概率密度不随时间变化，即系统达到平衡态。
(2)由于这里默认正则方程为保守系下的形式，故需要注意刘维尔定理的适用条件为保守系。
