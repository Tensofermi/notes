# 混合理想气体、Gibbs佯谬

**★** 对于混合理想气体，在体积为V，总压为p的系统中：

$$
pV=\sum_i p_i V=\sum_i n_i RT
$$

上式可理解为道尔顿分压定律。

下面考虑一个半透膜，仅能通过某些物质$i$，而其他物质只能在一边，两边可以看作两相$\alpha$和$\beta$.对这些能通过的物质有$T^\alpha=T^\beta,p_i^\alpha=p_i^\beta,\mu_i^\alpha=\mu_i^\beta$,这是实验结果。基于此，设想一边是混合气体，另一边是能通过膜的纯气体，则有：
$\mu_i=\mu(T,p_i)$,从而可以利用纯气体的化学势分析混合气体：

$$
\mu_i=RT(\phi_i+lnp_i)=RT(\phi_i+ln(px_i))\qquad \phi_i=\frac{h_{0i}}{RT}-\int\frac{dT}{RT^2}\int c_{pi}dT-\frac{s_{0i}}{R}
$$

当热容可以看作常数时，有：

$$
\phi_i=\frac{h_{0i}}{RT}-\frac{c_{pi}}{R}lnT-\frac{s_{0i}}{R}
$$

由此根据$G=\sum n_i\mu_i$，得到吉布斯函数：

$$
\boxed{G=\sum n_iRT(\phi_i+ln(px_i))}
$$

通过$V=\frac{\partial G}{\partial p},S=-\frac{\partial G}{\partial T},H=G-T\frac{\partial G}{\partial T}$可以得到V,S,H的表达式：

$$
V=\frac{\sum n_iRT}{p}\quad S=\sum n_i\left[\int c_{pi}\frac{dT}{T}-Rln(px_i) +s_{0i}\right]\quad H=\sum n_i\left(\int c_{pi}dT+h_{0i}\right)
$$

此外也可求出内能等其他热力学量，注意适用条件是理想气体。

**★** 考察熵的函数S，可将熵表达式写为如下启发意义的形式：

$$
S=\sum n_i\left[\int c_{pi}\frac{dT}{T}-Rln(p) +s_{0i}\right]-R\sum n_ilnx_i
$$

其中第一项为纯组分的熵之和，第二项是混合之后的熵增，称为混合熵，且恒正。若将组分相同的气体混合，混合熵应该不为0；但从熵的广延性质来看，混合之后组分没变化，混合熵为0.这就是**吉布斯佯谬**.究其原因，需要用到全同粒子的特性来解释，见后面的统计物理部分。
