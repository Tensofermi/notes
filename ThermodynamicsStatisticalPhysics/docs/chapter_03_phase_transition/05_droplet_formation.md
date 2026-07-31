# 液滴的形成

**★** 本节利用平衡判据分析液滴和其气相组成的系统的平衡问题，并考虑液滴表面相带来的影响。事实上，表面相可以看作是产生额外压力的“膜”。

这里利用内能判据进行分析，当然也可用自由能等其他判据。并设液相为$\alpha$,气相为$\beta$,表面相为$\gamma$,根据判据有：

$$
\begin{array}{l}
\left\{\begin{matrix}
\delta U=0\\
\delta S=0\quad\delta V=0\quad \delta n=0
\end{matrix}\right.
\end{array}
\qquad
\begin{array}{l}
\left\{\begin{matrix}
\delta U^\alpha&=&T^\alpha\delta S^\alpha-p^\alpha\delta V^\alpha+\mu^\alpha\delta n^\alpha\\
\delta U^\beta&=&T^\beta\delta S^\beta-p^\beta\delta V^\beta+\mu^\beta\delta n^\beta\\
\delta U^\gamma&=&T^\gamma\delta S^\gamma+\sigma\delta A
\end{matrix}\right.
\end{array}
$$

上式默认理想表面的粒子数为0，从而不含表面相的化学势。此外，为了分析几何约束，这里假设液滴为球体，因为其表面积最小最稳定，且处理起来方便。

$$
V^\alpha=\frac{4}{3}\pi r^3\qquad A=4\pi r^2\quad\Rightarrow\quad \delta V^\alpha=4\pi r^2\delta r\qquad \delta A=8\pi r\delta r
$$

并代入约束条件$\delta S=0\quad\delta V=0\quad \delta n=0$中，得到：

$$
\delta U=\left(T^\alpha-T^\gamma\right)\delta S^\alpha+\left(T^\beta-T^\gamma\right)\delta S^\beta-\left(p^\alpha-p^\beta-\frac{2\sigma}{r}\right)4\pi r^2\delta r+\left(\mu^\alpha-\mu^\beta\right)\delta n^\alpha=0
$$

注意到$\delta S^\alpha,\delta S^\beta,\delta r,\delta n^\alpha$独立变化，故：

$$
\boxed{T^\alpha=T^\beta=T^\gamma\qquad p^\alpha=p^\beta+\frac{2\sigma}{r}\qquad\mu^\alpha=\mu^\beta}
$$

可见，由于表面相的存在使得液滴压强增大，这是表面张力使液滴收缩的体现。如果液滴和气相的地位互换，则这份压力要靠气泡来承受，可以利用$r\rightarrow -r$实现。此外，考虑带电球体时:$\sigma\delta A\rightarrow \delta(q\phi)=q\left(\frac{\partial \phi}{\partial r}\right)	\delta r$.

**★** 下面利用相平衡条件，讨论液滴形成的问题。对于液相$\alpha$和气相$\beta$，水平面和球形面液相的化学势应该满足(平衡条件下，$p$为水平面蒸气压强，$p^\beta$为球形面蒸气压强)：

$$
\mu^\alpha(T,p)=\mu^\beta(T,p)\qquad\mu^\alpha(T,p^\beta+\frac{2\sigma}{r})=\mu^\beta(T,p^\beta)
$$

对于液相，由于$p^\beta-p\ll\frac{2\sigma}{r}$,故对球形面液相化学势在$p$附近进行展开得到：

$$
\mu^\alpha(T,p^\beta+\frac{2\sigma}{r})\approx\mu^\alpha(T,p)+(p^\beta-p+\frac{2\sigma}{r})\frac{\partial \mu^\alpha}{\partial p}=\mu^\alpha(T,p)+(p^\beta-p+\frac{2\sigma}{r})v^\alpha
$$

假设蒸气为理想气体，根据$G_m=RT(\phi+ln(p))$,则球形面摩尔吉布斯函数可用水平面表达为：

$$
\mu^\beta(T,p^\beta)=\mu^\beta(T,p)+RTln(\frac{p^\beta}{p})
$$

联立各式，得到：

$$
RTln(\frac{p^\beta}{p})=(p^\beta-p+\frac{2\sigma}{r})v^\alpha\approx \frac{2\sigma}{r}v^\alpha\Rightarrow \boxed{r_c=\frac{2\sigma v^\alpha}{RTln(\frac{p^\beta}{p})}}
$$

*推导思路：将球形两相压强相等的关系式展开为平面压强项与附加项之和，利用水平两相压强相等，导出两相的附加项相等，从而得到半径的关系。*其中$r_c$称为中肯半径。当$r>r_c$时，由画直线的式子不难看出$\mu^\alpha<\mu^\beta$,从而气相不断转化为液相，最终发生气到液的相变。当$r<r_c$时，同理有$\mu^\alpha>\mu^\beta$,即液相不断向气相转化。综上，由于$r_c$恒正，只有$p^\beta>p$才可能发生气到液的相变，即过饱和蒸气。如果凝结核半径不够，也不能发生相变。

此外，考虑气泡平衡$(r\rightarrow -r)$，可以解释过热液体的现象。
