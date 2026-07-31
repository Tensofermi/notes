# 物态方程

**★** 为了描述不同物体的热力学参量的关系，有必要引入物态方程的概念。首先要明确的是，根据热0给出热平衡下温度的存在性，从而才能利用物态方程给出温度与状态参量之间的函数关系。因而：物态方程描述的是平衡状态下的情况，且必须含有温度。注意一个物态方程只能描述某一单相系。

一般而言，物态方程可以通过实验测得或统计物理推导得到。后一种将在下半部分展开。

为了实验中方便测定，通常引入辅助的物理量：

$$
\boxed{
\alpha=\frac{1}{V}\left ( \frac{\partial V}{\partial T} \right )_{p}\quad\beta=\frac{1}{p}\left ( \frac{\partial p}{\partial T} \right )_{V}\quad\kappa_{T}=-\frac{1}{V}\left ( \frac{\partial V}{\partial p} \right )_{T}
}
$$

以上三种最为常见，分别为体胀系数、压强系数、等温压缩系数(注意负号)。

$\beta$是不易测量的，但通过隐函数定理不难由$F(p,V,T)=0$得到：

$$
\left(\frac{\partial V}{\partial p}\right)_{T}\left(\frac{\partial p}{\partial T}\right)_{V}\left(\frac{\partial T}{\partial V}\right)_{p}=-1\Rightarrow
\boxed{
\alpha=\kappa_{T}\beta p}
$$

为了见识以上系数的作用，考虑将体积写成温度和压强的函数$V=V(T,p)$:

$$
\mathrm{d}V=\left(\frac{\partial V}{\partial T}\right)_{p}\mathrm{d}T+\left(\frac{\partial V}{\partial p}\right)_{T}\mathrm{d}p=\alpha V \mathrm{d}T-\kappa_{T}V\mathrm{d}p
$$

这时通过实验测得$\alpha\text{和}\kappa_{T}$代入微分式，再积分即可得到物态方程。若这两个系数为常数，可以直接积分得到：

$$
\int_{V_0}^{V}\frac{dV'}{V'}=\int_{T_0}^{T}\alpha dT'-\int_{p_0}^{p}\kappa_{T} dp' \Rightarrow V(T,p)=V_0 e^{\alpha(T-T_0)-\kappa_{T}(p-p_0)}
$$

通常将上式进行等价无穷小近似，作为物态方程分析问题(通常是液态和固体):

$$
\boxed{V=V_0[1+\alpha(T-T_0)-\kappa_{T}(p-p_0)]}
$$

**以上的这种全微分展开的方法贯穿热力学的始末，很多Tips需要后续不断积累。例如，微分式的积分下限通常为已知状态的定值，上限为变量。**

下面举几个物态方程的例子：

- 理想气体方程：$pV=nRT$由于此方程没有考虑分子之间的吸引力和排斥力，因此只能描述气体，不能描述相变。且在**温度高、压强小**时与实际气体符合的更好,**因而对压强取趋于0的极限，可将任何气体系统化为理想气体的形式，进而得到一些隐藏的结果**。常见的变形有：$p=\frac{N}{V}\frac{R}{N_A}T=n_{D}k_{B}T$和$\rho=\frac{pM}{RT}$，以及压强极小时的极限：$pV\rightarrow nRT$.
- 范氏气体方程：$(p+\frac{an^2}{V^2})(V-nb)=nRT$考虑分子间的相互作用和分子大小，分别用a和b对理想气体方程进行修正得到的。其考虑相互作用时用到了“平均场近似”，且可以解释相变和临界点等现象。
- 顺磁性固体：$M=\frac{C}{T-\theta}H$称为居里-外斯定理，同样使用了“平均场近似”的思想，统计物理部分将会进行相关推导。

**★** 根据是否与系统质量或物质的量成正比，可以将热力学量分为**广延量**和**强度量**，且通常将两个广延量相除得到一个强度量。

需要注意，当系统满足热力学极限:$ \mathop{lim}\limits_{N,V \to \infty}\frac{N}{V}=\mathrm{finite} $，以上区分才能成立。
