# 特性函数、G-H方程

**★** 有了以上的数学基础，试想能不能从可测的热容和物态方程出发，先导出基本热力学量，再导出其他所有热力学量呢？

由物态方程和内能U的全微分即可得到：

$$
U=\int\left\{C_VdT+\left[T\left(\frac{\partial p}{\partial T}\right)_V-p\right]dV\right\} +U_0
$$

再根据S的全微分得到：

$$
S=\int\left[\frac{C_V}{T}dT+\left(\frac{\partial p}{\partial T}\right)_VdV\right]+S_0
$$

(P.S.注意$dS=\frac{dU}{T}+\frac{pdV}{T}$并不与上式矛盾，因为U的全微分还有体积项)

类似的方法，H和用$C_p$表达的S也不难得出：

$$
H=\int\left\{C_pdT+\left[V-T\left(\frac{\partial V}{\partial T}\right)_p\right]dp\right\} +H_0
$$

$$
S=\int\left[\frac{C_p}{T}dT-\left(\frac{\partial V}{\partial T}\right)_pdp\right]+S_0
$$

根据F和G定义式，代入U(或H)和S的表达式即可求得F和G，详见G-H方程。由于G在后面的章节十分重要，因而这里写出理想气体的吉布斯函数。

$$
G=H-TS=\int C_pdT+H_0-T\left(\int \frac{C_p}{T}dT-nRln(p)+S_0\right)
$$

根据$\frac{1}{T}\int C_p dT=\int \frac{C_pdT}{T}+\int d(\frac{1}{T})\int C_pdT$得到：

$$
G_m=-T\int\frac{dT}{T^2}\int C_{p,m}dT+H_{m,0}-TS_{m,0}+RTln(p)
$$

通常写作如下形式：

$$
\boxed{G_m=RT[\phi(T)+ln(p)]}
$$

**★** 利用特性函数可以将以上信息浓缩为U(S,V),H(S,p),F(T,V),G(T,p)中的一个，再根据求导数的方式得到所有的热力学函数。以U为例进行说明。

由U(S,V)代入$\left(\frac{\partial U}{\partial S}\right)_V=T$和$\left(\frac{\partial U}{\partial V}\right)_S=-p$，分别得到S(T,V)和p(S,V)。再将结果联立消去S得到P(T,V)，最后再联立消去U中的S，即可得到U(T,V)。从而得到三个基本热力学量。即，特性函数蕴含了物态方程、内能和熵。

**★** 在由F导出U或由G导出H的过程中，难免要使用G-H方程：

$$
F+TS=\boxed{F-T\left(\frac{\partial F}{\partial T}\right)_V=U}\qquad G+TS=\boxed{G-T\left(\frac{\partial G}{\partial T}\right)_p=H}
$$

利用定义式和麦氏关系，对上式做变形的式子均为G-H方程。例如：

$$
U=H-pV=G-T\left(\frac{\partial G}{\partial T}\right)_p-p\left(\frac{\partial G}{\partial p}\right)_T
$$

**■** 对于一个表面张力的系统，由于$\sigma(T)$仅为温度的函数，因而由：

$$
dF=-SdT+\sigma dA\Rightarrow \sigma(T)=\left(\frac{\partial F}{\partial A}\right)_T\Rightarrow F=\sigma(T)A
$$

上式考虑了$A=0$时$F=0$，故无积分常数。再由G-H方程得到：

$$
U=A(\sigma -T\frac{d\sigma}{dT})
$$
