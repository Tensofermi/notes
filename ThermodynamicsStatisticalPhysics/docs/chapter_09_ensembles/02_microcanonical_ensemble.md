# 微正则系综

**★** 考虑能量恒为$E$的平衡孤立系统，即认为能量E、体积V和粒子数N都为常数的系统，该系统组成的系综称为微正则系综。由于孤立和平衡的属性，有：

$$
\frac{d\rho}{dt}=0\qquad\frac{\partial \rho}{\partial t}=0\quad\Rightarrow\quad\rho=Const.
$$

如果这里直接承认等概率原理，可得到经典统计系综的分布概率$(\Delta E \rightarrow 0)$ :

$$
\rho=\left\{\begin{matrix}
C\quad &E\ll H\ll E+\Delta E \\
0\quad &others
\end{matrix}\right.\qquad C=\frac{1}{\int_{\Delta E}d\Omega}
$$

以及量子统计系综的分布概率，其中$\Omega(N,E,V)$表示量子态总数：

$$
\rho_s=\left\{\begin{matrix}
C\quad &E_s=E \\
0\quad &E_s\neq E
\end{matrix}\right. \qquad C=\frac{1}{\Omega(N,E,V)}
$$

然而，如果不利用等概率原理这个统计假设，而是从纯力学出发，导出相同的结果，这便是玻尔兹曼的思路，涉及到*各态历经假说*。不幸的是，这个假设在数学上被证明是错误的，并且逐渐地，更多人开始认同将等概率原理作为超脱于纯力学而属于统计物理的基本假设。我们采取这种简洁明了的做法。

**★** 为了研究微正则系综的结构，可以将孤立系统$A^{(0)}$看成由两个子系统$A_1$和$A_2$组成，并且之间可交换能量、体积和粒子，那么有如下关系：

$$
\Omega^{(0)}(N^{(0)},E^{(0)},V^{(0)})=\Omega_1(N_1,E_1,V_1)\cdot\Omega_2(N_2,E_2,V_2)
$$

$$
N^{(0)}=N_1+N_2\qquad E^{(0)}=E_1+E_2\qquad V^{(0)}=V_1+V_2
$$

故$\Omega^{(0)}$可以看作为$(N_1,E_1,V_1)$的函数:

$$
\Omega^{(0)}=\Omega_1(N_1,E_1,V_1)\cdot\Omega_2(N^{(0)}-N_1,E^{(0)}-E_1,V^{(0)}-V_1)
$$

再根据最概然分布条件$\delta ln(\Omega^{(0)})=0$得到：

$$
\delta ln(\Omega^{(0)})=\left(\frac{\partial ln\Omega^{(0)}}{\partial N_1}\right)_{E_1,V_1}\delta{N_1}+\left(\frac{\partial ln\Omega^{(0)}}{\partial E_1}\right)_{V_1,N_1}\delta{E_1}+\left(\frac{\partial ln\Omega^{(0)}}{\partial V_1}\right)_{N_1,E_1}\delta{V_1}=0
$$

由于$\delta N_1,\delta E_1,\delta V_1$任意变动，故：

$$
\left(\frac{\partial ln\Omega^{(0)}}{\partial N_1}\right)_{E_1,V_1}=\left(\frac{\partial ln\Omega_1}{\partial N_1}\right)_{E_1,V_1}+\left(\frac{\partial ln\Omega_2}{\partial (N^{(0)}-N_1)}\right)_{E_1,V_1}\frac{d (N^{(0)}-N_1)}{d N_1}=0
$$

$$
\Rightarrow \left(\frac{\partial ln\Omega_1}{\partial N_1}\right)_{E_1,V_1}=\left(\frac{\partial ln\Omega_2}{\partial N_2}\right)_{E_1,V_1}=\left(\frac{\partial ln\Omega_2}{\partial N_2}\right)_{E_2,V_2}
$$

同理，综合得到：

$$
\left(\frac{\partial ln\Omega_1}{\partial N_1}\right)_{E_1,V_1}=\left(\frac{\partial ln\Omega_2}{\partial N_2}\right)_{E_2,V_2}=\alpha
$$

$$
\left(\frac{\partial ln\Omega_1}{\partial E_1}\right)_{V_1,N_1}=\left(\frac{\partial ln\Omega_2}{\partial E_2}\right)_{V_2,N_2}=\beta
$$

$$
\left(\frac{\partial ln\Omega_1}{\partial V_1}\right)_{N_1,E_1}=\left(\frac{\partial ln\Omega_2}{\partial V_2}\right)_{N_2,E_2}=\gamma
$$

其中$\alpha,\beta,\gamma$为引入的常数，并且上式可看作平衡条件。从而，对于给定系统的微观状态数$\Omega(N,E,V)$，可以有:

$$
dln(\Omega)=\beta dE+\gamma dV+\alpha dN
$$

类比熵的全微分$dS=\frac{dU}{T}+\frac{p}{T}dV-\frac{\mu}{T}dN$,自然有：

$$
\boxed{S=kln(\Omega)}\quad\Rightarrow\quad\boxed{\alpha=-\frac{\mu}{kT}\qquad\beta=\frac{1}{kT}\qquad\gamma=\frac{p}{kT}}
$$

上面假设$S$与$ln(\Omega)$的比例系数为$k$，即实验上测得的玻尔兹曼常数。$S$与$ln(\Omega)$的关系，称为玻尔兹曼关系。

**★** 将经典系统视为满足非简并条件的非定域的量子系统(需要考虑全同性)，若系统由多种粒子组成，且第$i$种粒子的个数为$N_i$,那么总的微观状态$\Omega$有：

$$
\Omega=\frac{1}{\prod_iN_i!h^f}\int_{\Delta E}d\Omega
$$

现在利用上式讨论单原子理想气体组成的孤立系统,设其具有固定能量$E$,固定体积$V$,固定粒子数$N$。由于理想气体是满足非简并条件的非定域系统，且能级准连续，故其微观状态为：

$$
\Omega(N,E,V)=\frac{1}{N!h^{3N}}\int_{\Delta E} d\Omega=\frac{V^{N}}{N!h^{3N}}\int_{\Delta E} d^3\vec{p}_1...d^3\vec{p}_{N}
$$

单原子仅考虑平动，故体系的哈密顿量为：

$$
H=\sum_{i=1}^N\frac{|\vec{p_i}|^2}{2m}=\frac{\sum_{i=1}^N(p^2_{xi}+p_{yi}^2+p_{zi}^2)}{2m}=\frac{P^2}{2m}\Rightarrow P=\sqrt{\sum_{i=1}^{N}(p^2_{xi}+p_{yi}^2+p_{zi}^2)}
$$

其中$P$为动量空间中的半径，由此将$d^3\vec{p}_1...d^3\vec{p}_{N}$看作在$3N$维空间半径$P$从$\sqrt{2mE}$到$\sqrt{2m(E+\Delta E)}$的球壳，根据$d$维空间中球的体积，得到：

$$
\boxed{V_d=\frac{\pi^{\frac{d}{2}}}{\Gamma(\frac{d}{2}+1)}R^d}\quad\Rightarrow\quad S_d=V_d'=\frac{d\pi^{\frac{d}{2}}}{\Gamma(\frac{d}{2}+1)}R^{d-1}\quad\Rightarrow\quad S_{3N}=\frac{3N\pi^{\frac{3N}{2}}}{\Gamma(\frac{3N}{2}+1)}R^{3N-1}
$$

代入$R=P$并且积分，得到：

$$
\Omega(N,E,V)=\frac{V^{N}}{N!h^{3N}}\frac{3N\pi^{\frac{3N}{2}}}{\Gamma(\frac{3N}{2}+1)}\int_{\sqrt{2mE}}^{\sqrt{2m(E+\Delta E)}} P^{3N-1}dP
$$

$$
=\frac{V^{N}}{N!h^{3N}}\frac{3N\pi^{\frac{3N}{2}}}{\Gamma(\frac{3N}{2}+1)}\frac{(2m)^{\frac{3N}{2}}\left[(E+\Delta E)^{\frac{3N}{2}}-E^{\frac{3N}{2}}\right]}{3N}
$$

$$
=
\frac{V^{N}}{N!h^{3N}}\frac{(2m\pi)^{\frac{3N}{2}}}{\Gamma(\frac{3N}{2}+1)}\left[(E+\Delta E)^{\frac{3N}{2}}-E^{\frac{3N}{2}}\right]=\frac{V^{N}}{N!h^{3N}}\frac{(2m\pi E)^{\frac{3N}{2}}}{\Gamma(\frac{3N}{2}+1)}\left[(1+\frac{\Delta E}{E})^{\frac{3N}{2}}-1\right]
$$

由于$\frac{\Delta E}{E}\rightarrow0$,利用近似$(1+x)^\alpha-1\approx\alpha x$得到:

$$
\Omega(N,E,V)=\frac{V^{N}}{N!h^{3N}}\frac{(2m\pi E)^{\frac{3N}{2}}}{\Gamma(\frac{3N}{2}+1)}\frac{3N}{2}\frac{\Delta E}{E}=\Sigma(E)\frac{3N}{2}\frac{\Delta E}{E}\propto E^{\frac{3N}{2}}
$$

其中$\Sigma(E)$表示能量小于$E$的微观状态数，由此可以简化表达。

利用玻尔兹曼关系$S=kln(\Omega)$不难得到特性函数$S(N,E,V)$,从而得到其他热力学量。综上，微正则系综求解问题的方法是先求出$\Omega$,从而得到特性函数$S$,最终得到其他热力学量。但由于计算复杂，由此引入其他的系综。
