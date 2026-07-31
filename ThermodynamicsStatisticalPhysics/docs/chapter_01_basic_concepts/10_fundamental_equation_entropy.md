# 热力学基本方程、理想气体的熵与相关计算

**★** 对于一般过程而言，由$dS\geqslant\frac{\delta Q}{T}$和热一得到：

$$
\boxed{dU \leqslant TdS+\delta W}
$$

即封闭系统热力学基本方程的一般形式，**但要注意，分析$\delta Q=0$不能使用此不等式，因为$TdS\geqslant\delta Q$**.此外，对于可逆过程的热力学基本方程有：

$$
dU=TdS+\sum_{i} Y_idy_i\Rightarrow \boxed{dU=TdS-pdV}
$$

**★** 根据理想气体方程和热力学基本方程得到：

$$
dS=\frac{dU+pdV}{T}=\frac{n C_{V,m}dT}{T}+\frac{nRdV}{V}
$$

**默认热容不变**，积分得到熵变：

$$
\Delta S=nC_{V,m}ln(\frac{T_2}{T_1})+nRln(\frac{V_2}{V_1})
$$

**根据熵和体积的广延性**，也可写出熵的表达式：

$$
S(T,V)=nC_{V,m}lnT+nRlnV+S_0\qquad S_0=nS_{m0}-nRln(n)
$$

此外代入$V=\frac{nRT}{p}$得到熵变和熵的表达式：

$$
\Delta S=nC_{p,m}ln(\frac{T_2}{T_1})-nRln(\frac{p_2}{p_1})
$$

$$
S(T,p)=nC_{p,m}lnT-nRlnp+S_0\qquad S_0=nS_{m0}
$$

上式中，注意熵变和熵的区别，后面计算同种气体混合的熵增会用到。**原因在于，划线部分是考虑体积的广延性得到的。然而，由于通常考虑的气体粒子数固定，这一点常常容易被忽视。**

**Tips:(1)计算熵变之前要明确过程是否可逆，当过程是在等压环境下发生，需要考察$dS=\frac{C_pdT}{T}$各项进行分析。
(2)此外，当热机在运行时，$Q_1=W+Q_2$的关系需要经常使用。(3)计算相变熵变时，需要利用熵是状态函数的特性，构造巧妙的回路进行差的计算,类似于高中的盖斯定律。**
