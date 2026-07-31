# 热力学第一定律、热容

**★** 热力学第一定律的本质就是能量守恒，**因此非平衡态也适用。但要注意，能列出方程的都是准静态过程，有些过程无法用方程描述。**通常其等式左边为状态量，右边为过程量。表示经历某个过程，其能量并不会消失，而是形式上进行了转化。对于封闭系统：

$$
dU=\delta Q+\delta W
$$

上式表示系统的内能增量为外界的传热和外界对系统做的功。(当然，之后考虑粒子数交换等还会加入新的项)且其中功、热量、内能可以这样理解：

- 功：通过外界宏观运动将能量传给系统分子热运动和分子间势能。
- 热量：通过外界分子热运动将能量传给系统分子热运动和分子间势能。当$\delta Q=0$即绝热过程。
- 内能：是态函数，表示系统微观粒子各种能量的总和。在热力学极限下，为广延量。

**★** 为了描述系统升高1K所吸收的能量，可以定义热容：

$$
C=\frac{\delta Q}{d T}
$$

注意，此时热容还是与过程相关的广延量。以下进行“去个性化”的操作：

- 比热容：$c=\frac{C}{m}$即单位质量单位温度下储存的热量。
- 摩尔热容：$C_m=\frac{C}{n}$。即单位摩尔单位温度下储存的热量，化学中常用。
- 定体热容：$C_V=\left(\frac{\delta Q}{d T}\right)_{V}=\left(\frac{\partial U}{\partial T}\right)_{V}$
根据热一，当系统的体积不变，就不会通过做体积功的方式增加内能，因此定体热容常常与内能联系起来。
- 定压热容：$C_P=\left(\frac{\delta Q}{d T}\right)_{p}=\left(\frac{\partial H}{\partial T}\right)_{p}$**其中H定义为$H=U+pV$称为焓。**在等压的体系中，经常使用，也称为恒压反应热。

通过“去个性化”产生了以上的强度量意义下的热容，且出现的最多的就是定体热容$C_V$和定压热容$C_p$了，而且它们之间的关系也非常多。**通常定义比热容比$\gamma=\frac{C_p}{C_V}$来简化表达。**

此外，定压热容和定体热容的差值可以通过定义式导出：

$$
C=\frac{\delta Q}{d T}=\frac{dU -\delta W  }{d T}=\frac{\left(\frac{\partial U}{\partial T}\right)_{V}dT+\left(\frac{\partial U}{\partial V}\right)_{T}dV}{dT}-\frac{-pdV}{dT}=\left(\frac{\partial U}{\partial T}\right)_{V}+\frac{dV}{dT}\left[\left(\frac{\partial U}{\partial V}\right)_{T}+p\right]
$$

再两边固定压强p可得：

$$
C_p=\left(\frac{\partial U}{\partial T}\right)_{V}+\left(\frac{\partial V}{\partial T}\right)_{p} \left[\left(\frac{\partial U}{\partial V}\right)_{T}+p\right]
$$

根据等体热容的性质，得到：

$$
C_p-C_V=\left(\frac{\partial V}{\partial T}\right)_{p} \left[\left(\frac{\partial U}{\partial V}\right)_{T}+p\right]
$$

那么上式中的$\left(\frac{\partial U}{\partial V}\right)_T$又该如何计算呢？根据文献：刘永军.范德瓦尔斯气体的内能及摩尔热容[J].伊犁教育学院学 报.2002,15(2):67-68 有：

$$
\left(\frac{\partial U}{\partial V}\right)_T=T\left(\frac{\partial p}{\partial T}\right)_V-p\Rightarrow \boxed{C_p-C_V=T\left(\frac{\partial V}{\partial T}\right)_{p}\left(\frac{\partial p}{\partial T}\right)_V}
$$

之后，也会用麦氏关系推出此式。
