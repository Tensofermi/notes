# 多元体系热力学基本方程、复相平衡、Gibbs相律

**★** **为了简便，先对某一相进行研究**：设此相组元数为k*(这里不考虑化学反应等约束使得组元和物质种类数不相等的情况，那是物理化学研究的范畴)*,基本热力学量都是广延量，保持温度和压强不变，摩尔数变为原来的$\lambda$倍：

$$
\begin{array}{l}
\left\{\begin{matrix}
V(T,p,\lambda n_1,...,\lambda n_k)=\lambda V(T,p, n_1,..., n_k)\\
U(T,p,\lambda n_1,...,\lambda n_k)=\lambda U(T,p, n_1,..., n_k)\\
S(T,p,\lambda n_1,...,\lambda n_k)=\lambda S(T,p, n_1,..., n_k)
\end{matrix}\right.
\end{array}
$$

根据齐次函数的欧拉定理(详见分析力学)得到(求和默认i=1,...,$k$)：

$$
V=\sum n_i \left(\frac{\partial V}{\partial n_i}\right)_{T,p,n_{j\neq i}}\qquad U=\sum n_i \left(\frac{\partial U}{\partial n_i}\right)_{T,p,n_{j\neq i}}\qquad S=\sum n_i \left(\frac{\partial S}{\partial n_i}\right)_{T,p,n_{j\neq i}}
$$

为了方便，定义偏摩尔量$v_i=\left(\frac{\partial V}{\partial n_i}\right)_{T,p,n_{j\neq i}},u_i=\left(\frac{\partial U}{\partial n_i}\right)_{T,p,n_{j\neq i}},s_i=\left(\frac{\partial S}{\partial n_i}\right)_{T,p,n_{j\neq i}}$.**注意偏摩尔量必须满足T和p保持不变**，并且与之前单元系的字母进行区分。由此可以方便表达偏导关系，并推广到吉布斯函数G：

$$
V=\sum n_iv_i\qquad U=\sum n_i u_i\qquad S=\sum n_i s_i\qquad G=\sum n_i\mu_i
$$

对$G(T,p,n_1,...,n_k)$进行全微分展开,并利用定义得到**多元开放系的基本热力学方程。注意，其中$\mu_i$称为偏摩尔吉布斯函数**:

$$
dG=-SdT+Vdp+\sum \mu_i d n_i\qquad \boxed{dU=TdS-pdV+\sum\mu_idn_i}
$$

此外，不难看出k+2个强度量之间的关系,也就是吉布斯关系：

$$
-SdT+Vdp+\sum_i n_i d\mu_i=0\quad\Rightarrow\quad \boxed{U=TS-pV+\sum_i\mu_i n_i}
$$

上式说明多元单相系的自由度(独立的强度量个数)为k+1.后面我们将之推广为$\phi$个相的多元体系，即吉布斯相律。

**★** 对于多元复相系统，满足某些条件后，可以定义系统总体的广延量。如各相温度压强相等，可以定义总的吉布斯函数：

$$
G=\sum_\alpha G^\alpha=\sum_\alpha\sum_i n^\alpha_i \mu^\alpha_i
$$

根据上式，可以很好地理解复相与组元的关系。下面推导复相平衡条件。

为了简便，这里仅考虑两相$\alpha,\beta$，且每相组分为k.从而每组分在两相中的粒子数守恒：$\delta n^\alpha_i+\delta n^\beta_i=0\quad(i=1,2,...,k)$.在等温等压条件下，由吉布斯平衡判据得到：

$$
\delta G=\delta G^\alpha+\delta G^\beta=\sum_{i=1}^{k}(\mu_i^\alpha-\mu_i^\beta)\delta n^\alpha_i=0\Rightarrow \boxed{\mu_i^\alpha=\mu_i^\beta\quad(i=1,2,...,k)}
$$

即各个组元在每相中的化学势相等。

**★** 根据以上结论，可以导出著名的**吉布斯相律**。考虑$\phi$个相，且对于某$\alpha$相有$k_\alpha$个组元，设总组元为$k$,则有$k_\alpha\leqslant k$。为了统一分析强度量，对于某$\alpha$相而言，将摩尔量化作组分的比例：

$$
x^\alpha_i=\frac{n^\alpha_i}{n^\alpha}\quad\Rightarrow\quad \sum_{i=1}^{k_\alpha}x^\alpha_i=1
$$

从而对于某$\alpha$相组分比例$x^\alpha_i$的自由度为$k_\alpha-1$，由于相的物理性质均匀，再算上该相的压强$p^\alpha$和
温度$T^\alpha$，就有$k_\alpha+1$个自由度。那么对于$\phi$个相，就有$\sum_{\alpha=1}^{\phi}(k_\alpha+1)$个自由度。

设某一组分占据相的个数为$\phi_i$,当然也有$\phi_i\leqslant\phi$,再根据平衡条件：

$$
T^1=T^2=...=T^\phi\qquad p^1=p^2=...=p^\phi\qquad \mu_i^1=\mu_i^2=...=\mu_i^{\phi_i}(i=1,2,...,k)
$$

则约束的自由度为$2(\phi-1)+\sum_{i=1}^{k}(\phi_i-1)$,从而系统总共的自由度为

$$
f=\sum_{\alpha=1}^{\phi}(k_\alpha+1)-2(\phi-1)-\sum_{i=1}^{k}(\phi_i-1)=k+2-\phi+\sum_{\alpha=1}^{\phi}k_\alpha-\sum_{i=1}^{k}\phi_i
$$

根据复相与组元的关系，显然有$\sum_{\alpha=1}^{\phi}k_\alpha=\sum_{i=1}^{k}\phi_i$,可以通过表格更直观的看出这一点。从而得到：

$$
\boxed{f=k+2-\phi}
$$

要注意的是，上式仅考虑了温度和压强的平衡，对于需要电磁参量等描述才能确定的体系，上面画横线的地方还需要改动，才能得到正确的自由度。

通常系统的组元数是确定的，故当相的个数增多，自由度会减少。
