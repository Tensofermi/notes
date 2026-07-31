# 能斯特定理和热力学第三定律

**★** 能斯特发现在低温下$\Delta G<0$和$\Delta H<0$两个化学反应的判据，能给出几乎相同的结果。我们考虑等温过程，并运用洛必达法则：

$$
\Delta G=\Delta H-T\Delta S\Rightarrow \lim_{T \to 0}(\Delta S)=\lim_{T \to 0}\frac{\Delta H-\Delta G}{T} =\left(\frac{\partial \Delta H}{\partial T}\right)_0-\left(\frac{\partial \Delta G}{\partial T}\right)_0
$$

根据能斯特的相切假设，得到：

$$
\boxed{\lim_{T \to 0}(\Delta S)=0}
$$

此即热力学第三定律。此外，其等价表述为：不可能通过有限步骤使得物体冷却到绝对零度。

对于降温而言，最有效的是可逆绝热过程。由于使得物体的温度尽可能低，一定会低于周围物体的温度，从而吸收热量，因而可逆绝热过程效果最好。对于有限步无法达到$0K$，可以用绝热去磁化的例子，分析其S-T图，粗略得到结果。

最后，热三还告诉我们$S(0,y_A)=S(0,y_B)$，即在$0K$时任意两种状态的熵相等。利用这一性质，可以有以下推论。

**★** 首先，对于在趋于$0K$的热容有：

$$
C_y=T\left(\frac{\partial S}{\partial T}\right)_y\Rightarrow \lim_{T \to 0}C_y=0
$$

此外，关于熵与压强和体积的关系，利用麦氏关系，也可得到类似的结论：

$$
\lim_{T \to 0}\left(\frac{\partial S}{\partial p}\right)_T=\lim_{T \to 0}-\left(\frac{\partial V}{\partial T}\right)_p=0\qquad \lim_{T \to 0}\left(\frac{\partial S}{\partial V}\right)_T=\lim_{T \to 0}\left(\frac{\partial p}{\partial T}\right)_V=0
$$

也就是说，趋于$0K$时，$\alpha\rightarrow0,\beta\rightarrow0$

由于$0K$时不同相的熵也相等，从而根据克拉伯龙方程:

$$
\frac{dp}{dT}=\frac{s^\beta-s^\alpha}{v^\beta-v^\alpha}=0
$$

这说明，一级相变的相平衡曲线趋于$0K$时，斜率为0.

**★** 既然体系趋于$0K$的熵为绝对的常数，那么索性直接令其为0，这便是普朗克关于绝对熵概念的想法。即：

$$
\lim_{T \to 0}S_0=0\Rightarrow S(T,y)=\int_0^T\frac{C_y}{T}dT
$$

统计物理中，还会对熵有更进一步的认识。
