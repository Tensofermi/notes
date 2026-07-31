# 化学势的引入、平衡判据、稳定平衡判据

**★** 考虑一个开放均匀的系统，对于1mol的内能$du=Tds-pdv$,与总量之间的关系为$U=nu,S=ns,V=nv$,取微分得到：

$$
dU=udn+ndu=udn+Tnds-pndv=(u-Ts+pv)dn+TdS-pdV
$$

上式用到了$dS=sdn+nds,dV=vdn+ndv$.令化学势$\boxed{\mu=u-Ts+pv}$,即摩尔吉布斯函数.从而可将开放系统的基本热力学方程写作：

$$
\boxed{dU=TdS-pdV+\mu dn}
$$

对于另外3个常用特性函数的微分式，只要直接加上$\mu dn$项即可，因为其定义式中未涉及粒子数。因而有：

$$
\mu=\left(\frac{\partial U}{\partial n}\right)_{S,V}=\left(\frac{\partial H}{\partial n}\right)_{S,p}=\left(\frac{\partial F}{\partial n}\right)_{T,V}=\left(\frac{\partial G}{\partial n}\right)_{T,p}
$$

此外还可定义巨势函数$\boxed{J=F-\mu n=F-G}$从而:

$$
dJ=-SdT-pdV-nd\mu
$$

统计物理中的巨配分函数会涉及。

**★** 现在我们利用熵判据，推导$\phi$相孤立系统的平衡判据。通常的方法是拉格朗日乘子法。这里引入乘子所附加的约束为：$U=\sum n_iu_i,V=\sum n_iv_i,n=\sum n_i$都为定值，从而得到(求和默认i=1,...,$\phi$)：

$$
\delta U=\sum u_i\delta n_i+n_i\delta u_i=0\quad\delta V=\sum v_i\delta n_i+n_i\delta v_i=0\quad\delta n=\sum \delta n_i=0
$$

再根据摩尔熵变和$S=\sum n_is_i$:

$$
\delta s_i=\frac{\delta u_i}{T_i}+\frac{p_i\delta v_i}{T_i}\qquad\delta S=\sum s_i\delta n_i+n_i\delta s_i
$$

最后利用拉格朗日乘子法，并且为了方便分别设乘子为$-\frac{1}{T},-\frac{p}{T},\frac{\mu}{T}$，由$\tilde{\delta}S=0$:

$$
\tilde{\delta}S=\delta S-\frac{\delta U}{T}-\frac{p\delta V}{T}+\frac{\mu\delta n}{T}=0
$$

代入各式，并化为以$\delta u_i,\delta v_i,\delta n_i$三个独立变量的形式：

$$
\tilde{\delta} S=\sum n_i\left(\frac{1}{T_i}-\frac{1}{T}\right)\delta u_i+\sum n_i\left(\frac{p_i}{T_i}-\frac{p}{T}\right)\delta v_i+\sum\left(\frac{\mu}{T}-\frac{\mu_i}{T_i}\right)\delta n_i=0
$$

从而得到，平衡判据(分别对应热平衡、力学平衡、相平衡)：

$$
\boxed{T_i=T\qquad p_i=p\qquad \mu_i=\mu}
$$

以上对于孤立系统中$\phi$个相都成立，当$\phi=2$以上推导可以简化许多。

如果不满足平衡判据，利用$\delta S>0$的发展趋势，不难得到：(1)$T_i>T\Rightarrow \delta u_i<0$,**即能量从高温相传向低温**(2)$p_i>p\Rightarrow \delta v_i>0$,**即压强大的将膨胀，小的将收缩**(3)$\mu_i>\mu\Rightarrow \delta n_i<0$,**即化学势高的会向化学势低的转化。**此外，可以看出平衡判据均为强度量。

对于某些粒子数不受守恒约束的体系，若该粒子数可以独立变化且没有额外约束项，则平衡时相应化学势为0，典型例子是光子气体的$\mu=0$。但对一般化学反应体系，粒子数变化仍受化学计量关系约束，不能简单推出每个组分的化学势都为0。

**★** 最后讨论稳定平衡判据。利用$\delta^2S<0$经过复杂的推导得到：

$$
\delta^2 S=-\frac{C_V}{T^2}(\delta T)^2+\frac{1}{T}\left(\frac{\partial p}{\partial V}\right)_T(\delta V)^2<0
$$

从而得到稳定平衡判据：

$$
\boxed{C_V>0\qquad\left(\frac{\partial p}{\partial V}\right)_T<0}
$$

上式表明一种“负反馈”机制，也是勒夏特列原理的核心。
