# 理想气体平动热力学量与Maxwell速度分布

%注意化学势阿尔法、泻流

**★** 根据三维理想气体平动能量和能级连续的特征，可直接得到$Z_1$：

$$
\varepsilon=\frac{p^2}{2m}\Rightarrow Z_1=\int\frac{dxdydzdp_xdp_ydp_z}{h^3}e^{-\beta\frac{p_x^2+p_y^2+p_z^2}{2m}}\Rightarrow\boxed{Z_1=\frac{V}{h^3}\left(\frac{2m\pi}{\beta}\right)^{\frac{3}{2}}}
$$

上式默认气体的体积为V.由此立即得到体系的内能和压强：

$$
U=\frac{3}{2}NkT\qquad p=\frac{NkT}{V}
$$

对于熵的导出需要注意，如果使用定域系统的熵表达式，就会使得熵不满足广延性，产生之前提到的吉布斯佯谬，因而必须将理想气体视作非定域系统，使用*非定域修正*的熵的表达式，从而得到：

$$
S=\frac{3}{2}NklnT+Nkln\frac{V}{N}+\frac{3}{2}Nk\left[\frac{5}{3}+ln\left(\frac{2\pi mk}{h^2}\right)\right]
$$

注意理想气体熵的表达式中含有普朗克常数$h$，说明理想气体必定涉及量子力学。为了验证其正确性，可通过Sakur-Tetrode描述饱和蒸气压公式。通过对理想气体熵的改写以及相变潜热$L$不难导出此公式：

$$
S_{vap}\approx S_{vap}-S_{con}=\frac{L}{T}\quad\Rightarrow\quad lnp=-\frac{L}{RT}+\frac{5}{2}lnT+\frac{5}{2}+ln\left[k^{\frac{5}{2}}\left(\frac{2\pi m}{h^2}\right)^{\frac{3}{2}}\right]
$$

对于涉及到自由能的化学势，也需要采用*非定域修正*的形式进行计算：

$$
\mu=\left(\frac{\partial F}{\partial N}\right)_{T,V}=-kTln\left(\frac{Z_1}{N}\right)=-kTln(e^\alpha)=-kT\alpha\Rightarrow\boxed{\alpha=-\frac{\mu}{kT}}
$$

$$
\boxed{e^\alpha=\frac{Z_1}{N}=\frac{V}{Nh^3}\left(\frac{2m\pi}{\beta}\right)^{\frac{3}{2}}}\Rightarrow \mu=kTln\left[\frac{Nh^3}{V}\left(\frac{\beta}{2m\pi}\right)^{\frac{3}{2}}\right]
$$

**★** 这里对非简并条件$e^\alpha\gg1$进行讨论:

$$
e^a=\frac{V}{Nh^3}\left(\frac{2m\pi}{\beta}\right)^{\frac{3}{2}}=\frac{V}{N}\left(\frac{2m\pi kT}{h^2}\right)^{\frac{3}{2}}\gg1
$$

可见理想气体的化学势为负值。此外，该条件也可用德布罗意热波长$\lambda_T$写为：

$$
\lambda_T=\frac{h}{\sqrt{2\pi mkT}}\quad n=\frac{N}{V}\quad\Rightarrow\quad \boxed{n\lambda_T^3\ll1}
$$

**★** 基于以上平动的讨论，下面导出Maxwell速度分布。考虑理想气体在$dv_xdv_ydv_z$范围内的粒子数：

$$
da_l=\frac{Vdp_xdp_ydp_z}{h^3}e^{-\alpha-\beta\varepsilon_l}
$$

根据总粒子数为N的条件，可以得到与之前自洽的$e^{-\alpha}$:

$$
\int\frac{Vdp_xdp_ydp_z}{h^3}e^{-\alpha-\beta\varepsilon_l}=N\quad\Rightarrow\quad e^{-\alpha}=\frac{N}{V}\left(\frac{h^2}{2\pi mkT}\right)^{\frac{3}{2}}
$$

利用$dp_i=mdv_i$的关系代换，求出以$dv_xdv_ydv_z$为变量的粒子数表达式：

$$
da_l=N\left(\frac{m}{2\pi kT}\right)^{\frac{3}{2}}e^{-\frac{m}{2kT}(v_x^2+v_y^2+v_z^2)}dv_xdv_ydv_z=Nf(\vec{v})dv_xdv_ydv_z
$$

上式即导出了Maxwell速度分布，对于此分布的正确性，可由*多普勒增宽效应*所验证。此外，由于之前的章节已经对分布速度进行了研究，这里仅对泻流问题进行简单讨论：

$$
\Gamma_1=\Gamma_2\Rightarrow n_1\bar{v_1}=n_2\bar{v_2}\Rightarrow \frac{p_1}{\sqrt{T_1}}=\frac{p_2}{\sqrt{T_2}}
$$

上式考虑了小孔两边粒子达到平衡的条件$\Gamma_1=\Gamma_2$,再通过$p=nkT$和$T=\frac{1}{3k}m\bar{v^2}\approx\frac{1}{3k}m\bar{v}^2$进行化简,得到压强和温度的关系。
