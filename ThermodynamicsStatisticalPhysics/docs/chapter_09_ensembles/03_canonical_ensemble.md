# 正则系综

**★** 微正则系综处理的是孤立系统，而实际问题往往都是封闭系统，甚至是开放系统。因此有必要利用微正则系综开发出其他系综，从而方便处理实际问题。*本节研究系统与大热源（或热库）接触达到平衡的正则系综。*

由于与热源接触，故系统可以与外界进行能量交换，但粒子数和体积恒定，从而可以看作封闭系统。此外由于达到平衡，故系统有确定的温度。通常由$(N,T,V)$表示正则系综的特征。

为了利用微正则系综研究正则系综，将热源$A_r$与封闭系统$A_s$组成的大系统视为一个孤立系统$A^{(0)}$，则有如下关系：

$$
E_s+E_r=E^{(0)}\quad E_s\ll E^{(0)}
$$

其中$E_s$表示系统处于$s$量子态所具有的能量，从而热源的微观状态数为$\Omega_r(E^{(0)}-E_s)$,再根据等概率原理，得到系统处于$s$态的概率:

$$
\rho_s=\frac{\Omega_r(E^{(0)}-E_s)}{\Omega^{(0)}}\propto\Omega_r(E^{(0)}-E_s)
$$

由于$E_s\ll E^{(0)}$的关系，对上式取对数再在$E_s=0$处展开到第二项：

$$
ln\Omega_r(E^{(0)}-E_s)\approx ln\Omega_r(E^{(0)})+\left(\frac{\partial ln\Omega_r}{\partial E_r}\right)_{E_r=E^{(0)}}\frac{d E_r}{d E_s}E_s=ln\Omega_r(E^{(0)})-\beta E_s
$$

从而得到概率的正比关系：

$$
\rho_s\propto e^{ln\Omega_r(E^{(0)})-\beta E_s}=\Omega_r(E^{(0)})e^{-\beta E_s}\propto e^{-\beta E_s}\quad\Rightarrow\quad\boxed{\rho_s=\frac{e^{-\beta E_s}}{Z}\quad Z=\sum_s e^{-\beta E_s}}
$$

其中$Z$称为系统配分函数或N粒子配分函数，简称为配分函数。

如果考虑经典极限，即满足非简并条件的非定域系统且能级准连续，则概率由概率密度$\rho$和相空间体积元$d\Omega$表达为：

$$
\boxed{\rho d\Omega=\frac{d\Omega}{N!h^{f}}\frac{1}{Z}e^{-\beta E_s}\quad Z=\frac{1}{N!h^f}\int e^{-\beta E_s}d\Omega}
$$

注意上式都是对系统能量$E_s$的求和，而之前在近独立子系中引入的粒子配分函数，则是对单个粒子的能量$\varepsilon_s$求和。*如果系统的能量仍然与近独立相同，即能量不含交叉项，*则配分函数与粒子配分函数有如下关系:

$$
E_s=\sum_{i=1}^N\varepsilon_{si}\quad\Rightarrow\quad Z=\sum_s e^{-\beta E_s}=\sum_s\prod_{i=1}^Ne^{-\beta\varepsilon_{si}}=\prod_{i=1}^N\sum_{si}e^{-\beta\varepsilon_{si}}
$$

上式最后一个等号利用了全同粒子*可选取的态*都相同的性质，并且最终的求和一定是$N$个粒子取不同态的全部组合，即系统取相同能量时，前面的系数为二项式系数，从而可以写成乘积的形式。由此可得：

$$
\boxed{Z=Z^N_1\qquad or\qquad Z=\frac{1}{N!}Z^N_1}
$$

**★** 与近独立子系类似，热力学量与配分函数的关系也可根据定义导出:

$$
U=\overline{E}=\sum_sE_s\rho_s=\frac{1}{Z}\sum_sE_se^{-\beta E_s}=-\frac{\partial}{\partial\beta}ln(Z)
$$

$$
Y=\sum_s\frac{\partial E_s}{\partial y}\rho_s=\frac{1}{Z}\sum_s\frac{\partial E_s}{\partial y}e^{-\beta E_s}=-\frac{1}{\beta}\frac{\partial}{\partial y}ln(Z)
$$

$$
S=k\left(ln(Z)-\beta\frac{\partial}{\partial\beta}ln(Z)\right)\qquad F=-kTln(Z)
$$

可见，配分函数导出基本热力学量的表达式中，不含$N$和$N!$,这是因为它们都在配分函数本身中蕴含。使用时要注意表达式中的正负号，以及配分函数是否除以$N!$.此外，根据正则系综(N,T,V)可看出，自由能$F$为特性函数。

下面讨论正则系综中的能量涨落，所谓涨落即*偏差平方的平均值*，故：

$$
\overline{(E_s-\overline{E})^2}=\sum_s\rho_s(E_s^2-2E_s\overline{E}+\overline{E}^2)=\overline{E^2}-\overline{E}^2
$$

其中$\overline{E^2}$可以进一步写出：

$$
\overline{E^2}=\sum_sE^2\rho_s=\sum_sE^2\frac{e^{-\beta E_s}}{Z}=\frac{1}{Z}\sum_s\frac{\partial^2}{\partial \beta^2}e^{-\beta E_s}=\frac{1}{Z}\frac{\partial^2}{\partial\beta^2}Z
$$

再做一步配分：

$$
\overline{E^2}=\frac{\partial}{\partial\beta}\left(\frac{1}{Z}\frac{\partial}{\partial\beta}Z\right)-\frac{\partial}{\partial\beta}\left(\frac{1}{Z}\right)\frac{\partial Z}{\partial\beta}=-\frac{\partial}{\partial\beta}\overline{E}+\overline{E}^2
$$

综上得到：

$$
\overline{(E_s-\overline{E})^2}=-\frac{\partial}{\partial\beta}\overline{E}=kT^2\frac{\partial\overline{E}}{\partial T}=kT^2C_V>0
$$

也可定义相对涨落：

$$
\frac{\overline{(E_s-\overline{E})^2}}{\overline{E}^2}=\frac{kT^2C_V}{\overline{E}^2}\propto\frac{1}{N}
$$

由于$\overline{E}$与$C_V$都与粒子数$N$成正比，从而表明相对涨落与粒子数成反比，$N\rightarrow\infty$,涨落趋于0.

**★** 非理想气体物态方程的推导——集团展开法

<div align="center">

*完全写清楚过于复杂，详见李政道《统计力学》p65-p74等其他参考书*

</div>
