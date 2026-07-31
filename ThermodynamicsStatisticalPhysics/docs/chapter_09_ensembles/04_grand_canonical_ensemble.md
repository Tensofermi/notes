# 巨正则系综

**★** 顺着上节的思路，若系统与热源不仅有能量交换，还能进行*粒子数的交换*，并保持系统体积、化学势恒定且与热源达到热平衡，由这样的开放系统组成的系综称为巨正则系综。根据固定的参数，通常表示为$(\mu,T,V)$.

同样可以将热源$A_r$与开放系统$A_s$看作一个孤立系统$A^{(0)}$，利用微正则系综来研究。由于整体能量和粒子数守恒，有：

$$
E_s+E_r=E^{(0)}\quad E_s\ll E^{(0)}  \qquad N+N_r=N^{(0)}\quad N\ll N^{(0)}
$$

根据等概率原理，得到：

$$
\rho_{s,N}=\frac{\Omega_r(N^{(0)}-N,E^{(0)}-E_s)}{\Omega^{(0)}}\propto\Omega_r(N^{(0)}-N,E^{(0)}-E_s)
$$

由于$ E_s\ll E^{(0)}$和$N\ll N^{(0)}$的关系，对$\Omega_r$取对数、展开得到：

$$
ln\Omega_r(N^{(0)}-N,E^{(0)}-E_s)\approx ln\Omega_r(N^{(0)},E^{(0)})-\alpha N-\beta E_s
$$

从而得到概率的正比关系：

$$
\rho_{s,N}\propto e^{ln\Omega_r(N^{(0)},E^{(0)})-\alpha N-\beta E_s}=\Omega_r(N^{(0)},E^{(0)})e^{-\alpha N-\beta E_s}\propto e^{-\alpha N-\beta E_s}
$$

$$
\Rightarrow\boxed{\rho_{s,N}=\frac{1}{\Xi}e^{-\alpha N-\beta E_s}\quad\Xi=\sum_{N=0}^\infty\sum_se^{-\alpha N-\beta E_s}}
$$

其中$\Xi$为巨配分函数。需要注意，系统所含粒子数不同时，其量子态也不同，因而*描述量子态应先明确粒子数。*例如描述满足经典极限的系统,则有：

$$
\boxed{\rho_N d\Omega_N=\frac{d\Omega_N}{N!h^{f}}\frac{1}{\Xi}e^{-\alpha N-\beta E_s}\quad \Xi=\sum_{N=0}^\infty\frac{e^{-\alpha N}}{N!h^f}\int e^{-\beta E_s}d\Omega_N}
$$

此外，不难得到巨配分函数与配分函数的关系：

$$
\Xi=\sum_{N=0}^\infty e^{-\alpha N}\sum_s e^{-\beta E_s}=\sum_{N=0}^\infty e^{-\alpha N}Z=\sum_{N=0}^\infty e^{-\alpha N}Z_1^N\quad or\quad\sum_{N=0}^\infty e^{-\alpha N}\frac{Z_1^N}{N!}
$$

例如对于非定域的理想气体的巨配分函数为$\Xi=e^{e^{-\alpha}Z_1}$.

**★** 巨正则系综计算热力学量的公式推导如下：

$$
\overline{N}=\sum_N\sum_s N\rho_{s,N}=\frac{1}{\Xi}\sum_N\sum_s Ne^{-\alpha N-\beta E_s}=-\frac{\partial}{\partial \alpha}ln\Xi
$$

$$
U=\overline{E}=\sum_N\sum_sE_s\rho_{s,N}=\frac{1}{\Xi}\sum_N\sum_sE_se^{-\alpha N-\beta E_s}=-\frac{\partial}{\partial\beta}ln\Xi
$$

$$
Y=\sum_N\sum_s\frac{\partial E_s}{\partial y}\rho_{s,N}=\frac{1}{\Xi}\sum_N\sum_s\frac{\partial E_s}{\partial y}e^{-\alpha N-\beta E_s}=-\frac{1}{\beta}\frac{\partial}{\partial y}ln\Xi
$$

$$
S=k\left(ln\Xi-\alpha\frac{\partial}{\partial\alpha}ln\Xi-\beta\frac{\partial}{\partial\beta}ln\Xi\right)\qquad F=-kTln\Xi+kT\alpha\frac{\partial}{\partial\alpha}ln\Xi
$$

显然这里自由能的表达形式不够简单，主要原因是其不是巨正则系综$(\mu,T,V)$的函数，故可采用之前在热力学中定义的巨势函数：

$$
J=F-G=F-\overline{N}\mu=-kTln\Xi
$$

由此，巨势函数即为巨正则系综的特性函数。

与正则系综一样，这里讨论巨正则系综的能量涨落以及粒子数涨落。对于能量涨落，形式上仍可由对$\beta$的二阶导数得到，但巨正则系综中粒子数也会涨落，因此这里的热容应理解为固定$\alpha$和$V$时的响应量，而不是固定粒子数的正则热容：

$$
\overline{(E_s-\overline{E})^2}=-\left(\frac{\partial\overline{E}}{\partial\beta}\right)_{\alpha,V}=kT^2\left(\frac{\partial\overline{E}}{\partial T}\right)_{\alpha,V}\qquad\frac{\overline{(E_s-\overline{E})^2}}{\overline{E}^2}\propto\frac{1}{N}
$$

下面推导粒子数的涨落：

$$
\overline{N^2}=\sum_N\sum_sN^2\rho_{s,N}=\frac{1}{\Xi}\frac{\partial^2}{\partial\alpha^2}\sum_N\sum_se^{-\alpha N-\beta E_s}=\overline{N}^2-\frac{\partial\overline{N}}{\partial\alpha}
$$

$$
\Rightarrow\overline{(N-\overline{N})^2}=\overline{N^2}-\overline{N}^2=-\frac{\partial\overline{N}}{\partial\alpha}=kT\frac{\partial\overline{N}}{\partial\mu}
$$

利用$d\mu=-sdT+vdp$在等温条件下的等式，并利用体积固定的条件：

$$
\left(\frac{\partial \mu}{\partial v}\right)_T=v\left(\frac{\partial p}{\partial v}\right)_T\quad v=\frac{V}{\overline{N}}\Rightarrow\frac{\overline{(N-\overline{N})^2}}{\overline{N}^2}=\frac{kT}{V}\kappa_{T}\propto\frac{1}{N}
$$

**★** 下面讨论两个巨正则系综有趣的应用。

(1)固体表面的吸附率：设吸附中心的总数为$N_0$,被吸附分子平均数为$\overline{N}$,吸附率定义为$\theta=\frac{\overline{N}}{N_0}$,若被吸附的分子带来的能量为$-\varepsilon_0$,则有$N$个分子被吸附，体系能量为$E_s=-N\varepsilon_0$,从而被吸附的巨配分函数为：

$$
\Xi=\sum_{N=0}^{N_0}\sum_se^{-\alpha N-\beta E_s}=\sum_{N=0}^{N_0} \sum_se^{\beta(\mu+\varepsilon_0)N}
$$

上式用到了$\alpha=-\beta\mu$.对于同一$N$共有$C_{N_0}^N$种组合，故对$s$的求和可以写为：

$$
\Xi=\sum_{N=0}^{N_0}\frac{N_0!}{N!(N_0-N)!}e^{\beta (\mu+\varepsilon_0)N}=\left[1+e^{\beta(\mu+\varepsilon_0)}\right]^{N_0}
$$

上式用到了二项式展开的逆过程。利用上式巨配分函数，可以求出$\overline{N}$.若将分子视为理想气体，代入理想气体的化学势，得到：

$$
\overline{N}=-\frac{\partial}{\partial\alpha}ln\Xi=\frac{N_0}{1+e^{-\beta(\mu+\varepsilon_0)}}\quad\Rightarrow\quad\theta=\frac{1}{1+\frac{kT}{p}\left(\frac{2\pi mkT}{h^2}\right)^{3/2}e^{-\frac{\varepsilon_0}{kT}}}
$$

上式表明，$\theta$随$p$的上升而增大，随$T$的上升而减小．

(2)推导玻色分布和费米分布：之前讨论近独立子系的玻色和费米分布时所使用的巨配分函数似乎与这里不同，事实上这源于$\sum_s$求和方式的不同。下面通过改变巨配分函数的求和方式，以此导出上一章巨配分函数的特殊形式，并导出玻色分布和费米分布。

首先将相同的能量进行分类，从而营造出粒子数和能量均固定的求和环境。而满足两者固定的系统状态的个数(简并度)，正好就是近独立子系所考虑在分布$\{a_l\}$下的微观状态数$\Omega[\{a_l\}]$,从而：

$$
\Xi=\sum_N\sum_se^{-\alpha N-\beta E_s}=\sum_N\sum_E\Omega[\{a_l\}] e^{-\alpha N-\beta E}
$$

其次，利用粒子数与能量固定的条件，得到：

$$
N=\sum_la_l\quad E=\sum_l\varepsilon_la_l\quad\Rightarrow\quad\Xi=\sum_{N,E}\Omega[\{a_l\}]e^{-\sum_l(\alpha+\beta\varepsilon_l)a_l}
$$

现在将分布$\{a_l\}$推广到能量和粒子数不固定的情况，即$\sum_{\{a_l\}}$表示对一切可能的分布求和：

$$
\Xi=\sum_{\{a_l\}}\Omega[\{a_l\}]e^{-\sum_l(\alpha+\beta\varepsilon_l)a_l}
$$

设对于某个能级$l$总的量子态为$W_l$个，从而有$\Omega[\{a_l\}]=\prod_lW_l$,由此：

$$
\Xi=\sum_{\{a_l\}}\prod_l\left[W_le^{-(\alpha+\beta\varepsilon_l)a_l}\right]=\prod_l\Xi_l\quad\Rightarrow\quad\boxed{\Xi_l=\sum_{a_l}W_le^{-(\alpha+\beta\varepsilon_l)a_l}}
$$

上式求和变换的技巧在于将系统按整个分布去求和，转化为对单个能级的求和再连乘，从而定义出$\Xi_l$.对于玻色系统和费米系统的某个能级$l$，有：

$$
B.E.\quad\Xi_l=\sum_{a_l=0}^\infty C_{w_l+a_l-1}^{a_l}e^{-(\alpha+\beta\varepsilon_l)a_l}\qquad F.D.\quad\Xi_l=\sum_{a_l=0}^{\omega_l}C_{w_l}^{a_l}e^{-(\alpha+\beta\varepsilon_l)a_l}
$$

利用$(1-x)^{-\omega_l}$和$(1+x)^{\omega_l}$的展开式，得到巨配分函数：

$$
B.E.\quad\Xi=\prod_l\Xi_l=\prod_l(1-e^{-\alpha-\beta\varepsilon_l})^{-\omega_l}\qquad F.D.\quad\Xi=\prod_l\Xi_l=\prod_l(1+e^{-\alpha-\beta\varepsilon_l})^{\omega_l}
$$

以上即上一章引入的巨配分函数，可见其本质和本章的完全相同，只不过形式不同而已。最后，导出能级$l$上的粒子数分布：

$$
B.E.\quad\bar{a_l}=-\frac{\partial}{\partial\alpha}ln\Xi_l=\frac{\omega_l}{e^{\alpha+\beta \varepsilon_l}-1}\qquad F.D.\quad\bar{a_l}=-\frac{\partial}{\partial\alpha}ln\Xi_l=\frac{\omega_l}{e^{\alpha+\beta \varepsilon_l}+1}
$$

**★** 最后，讨论一下三种系综的关系。如果满足热力学极限条件

$$
\mathop{lim}\limits_{N,V \to \infty}\frac{N}{V}=\mathrm{finite}
$$

那么三种系综是等价的,例如粒子数守恒的理想气体也可利用巨配分函数来计算。但若不满足此条件，往往会导出错误的结果。

对于概率$\rho_{s,N}$而言，若将巨正则系综中的粒子数$N$固定，则退化为正则系综的概率$\rho_s$.如果再将正则系综的能量$E_s$固定，则概率将成为常数，即为微正则系综的概率$\rho_s=Const.$

从实用性的角度，最为常用的是正则系综和巨正则系综，而这两者的选取通常很微妙。一般的规律是*定域系统或满足非简并条件的非定域系统常用正则系综，不满足非简并条件的非定域系统常用巨正则系综。*
