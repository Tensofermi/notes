# 范氏气体节流过程、焦汤系数

**★** 对应上一章的焦耳实验和焦耳系数，这里讨论后续进行的节流过程的实验，以及对应的焦汤系数。所谓节流过程，即将多孔塞一端的高压气体压向另一端低压的区域，研究气体的温度变化。

设节流过程前后气体的状态参量为$(p_1,V_1,T_1,U_1,H_1)$和$(p_2,V_2,T_2,U_2,H_2)$由于多孔塞两端压强是恒定的，并且整个体系绝热，因而不难得到：

$$
U_2-U_1=W=p_1V_1-p_2V_2\Rightarrow \boxed{H_1=H_2}
$$

注意我们仅关注初末状态，中间的过程十分复杂，且对状态量无影响。

由此，既然整个过程是等焓的，出于研究气体温度随压强变化的目的，不妨引入焦汤系数$\mu$:

$$
\mu=\left(\frac{\partial T}{\partial p}\right)_H
$$

再根据$f(H,T,p)=0$的偏导关系以及上一节的结论，不难得到：

$$
\mu=-\left(\frac{\partial T}{\partial H}\right)_p\left(\frac{\partial H}{\partial p}\right)_T=-\frac{1}{C_p}\left(\frac{\partial H}{\partial p}\right)_T=\boxed{\frac{1}{C_p}\left[T\left(\frac{\partial V}{\partial T}\right)_p-V\right]}=\frac{V}{C_p}(T\alpha-1)
$$

由于$C_p>0$因而$\mu$的正负取决于$T\left(\frac{\partial V}{\partial T}\right)_p-V$
.并称$\mu>0$的区域为制冷区，$\mu<0$的区域为致温区，因而反转曲线$\mu=0$十分重要。由于理想气体恒有$\mu=0$因而温度不变化，这里利用范氏气体进行推导。

由$\mu=0$得到：

$$
T\left(\frac{\partial V}{\partial T}\right)_p=V\Rightarrow \frac{8RTb}{a}=\left(\frac{b^2p}{a}+\frac{3RTb}{2a}+1\right)^2
$$

得到上式需要比较复杂的数学技巧，详见林书p83.由上式即可画出p-T图中的反转曲线。工业上常利用此原理进行制冷操作。
