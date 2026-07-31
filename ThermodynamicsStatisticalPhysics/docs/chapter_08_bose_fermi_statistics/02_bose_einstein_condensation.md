# Bose-Einstein凝聚

**★** 在讨论BEC之前，先来研究一下玻色气体粒子数的性质：

$$
N=\frac{V}{\lambda_{T}^3}Li_{3/2}(z)>0,\qquad z=e^{\mu/kT}
$$

对理想玻色气体，基态能量取为0时需有$\mu\leqslant0$，因此$0<z\leqslant1$。这不是单纯由$N>0$推出的，而是由玻色分布分母$e^{\beta(\varepsilon-\mu)}-1$必须为正推出的。

此外，在此区间范围内$Li_{3/2}(z)$是单调递增的，故在$z=0$时取得最小值$Li_{3/2}(0)=0$;在$z=1$时取得最大值$Li_{3/2}(1)=\zeta(\frac{3}{2})\approx2.612$.

现在考虑当总粒子数$N$固定，温度下降的情况。根据$\frac{1}{\lambda_T^3}\sim T^{\frac{3}{2}}$的关系,$Li_{3/2}(z)$必然要上升，才能保持激发态容纳足够多的粒子。然而$Li_{3/2}(z)$的取值上限为$\zeta(\frac{3}{2})$,从而当温度下降到足够低的$T_c$时，激发态可容纳的粒子数达到上限，剩余粒子只能进入基态。

$$
N=\frac{V}{\lambda_{T_c}^3}Li_{3/2}(1)=\frac{V}{h^3}(2\pi m kT_c)^{3/2}Li_{3/2}(1)\quad\Rightarrow\quad n\lambda_{T}^3>\zeta(\frac{3}{2})\approx2.612
$$

上式即为这种临界状态所满足的等式；当$n\lambda_T^3>\zeta(\frac{3}{2})$时，仅靠激发态已经无法容纳全部粒子。事实上，上一节推导玻色气体的巨配分函数时，其中$D(\varepsilon)\sim\varepsilon^{\frac{1}{2}}$,使得处于基态$\varepsilon=0$的量子态对连续态密度没有贡献。低于$T_c$时，基态粒子数开始宏观增大，这正是BEC的体现；由于这里涉及$z=e^{-\alpha}\rightarrow1$,故属于强简并的情况。
*

**★** 下面将基态粒子数对巨配分函数的贡献单独作为一项，$ln\Xi$修正为:

$$
ln\Xi=-\sum_l\omega_lln(1-e^{-\alpha-\beta\varepsilon_l})=-\omega_1ln(1-e^{-\alpha})+\frac{V}{\lambda_T^3}Li_{5/2}(z)
$$

为了方便，取基态简并度为1，即$\omega_1=1$,从而得到修正的粒子数为：

$$
\boxed{N=\frac{z}{1-z}+\frac{V}{\lambda_{T}^3}Li_{3/2}(z)}
$$

对于内能和物态方程，由于$ln\Xi$的基态修正项中不含$\beta$和外参量$V$,故仍为原来的表达式。然而，有时为了研究$T<T_c$条件下，各个热力学量与$\frac{T}{T_c}$的关系，默认$z\approx1$;且$T=T_c$时，基态粒子数可以忽略不计，那么有：

$$
N\approx\frac{V}{\lambda_{T_c}^3}Li_{3/2}(1)\quad\Rightarrow\quad N_{exc}=N\left(\frac{T}{T_c}\right)^{3/2}\quad N_0=N\left[1-\left(\frac{T}{T_c}\right)^{3/2}\right]
$$

注意粒子数$N$的表达式中温度恒为$T_c$,而其他热力学量中的$T$为变量。故：

$$
\frac{pV}{NkT}=\frac{U}{\frac{3}{2}NkT}=\frac{Li_{5/2}(z)}{Li_{3/2}(z)}\left(\frac{T}{T_c}\right)^{3/2}\quad\Rightarrow\quad C_V=\left(\frac{\partial U}{\partial T}\right)_V=\frac{15Li_{5/2}(z)}{4Li_{3/2}(z)}Nk\left(\frac{T}{T_c}\right)^{3/2}
$$

即当$T\rightarrow0$时，$U,p$和$C_V$分别以$T^{5/2}$和$T^{3/2}$的幂次趋向于0.*这体现出玻色气体的特点，但在强简并的费米气体中，由于泡利不相容原理，能量、压强等不会随温度趋向于0.*

值得注意，严格来说$z(T)$需要根据粒子数方程$N=N(T,z)$来确定。在热力学极限下，$T<T_c$时通常取$z\rightarrow1$，而不是把$z$看成趋于0。

**★** 本节从巨配分函数导出的粒子数出发，发现在低于$T_c$的温度下，粒子数会减少，从而判断BEC的存在。然而，分析新的体系这样的过程也许过于繁杂，我们可以从化学势$\mu$入手，分析临界状态，从而判断$T_c$是否存在。例如分析二维玻色气体不会发生BEC,但处在磁光陷阱中的二维原子却可以。
