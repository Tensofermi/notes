# 化学平衡和化学常数

**★** 方便起见，这里仅考虑单相系的化学平衡。化学反应作为对系统组分摩尔量的约束条件，需要拥有普世的数学表述。可以先从简单、具体的例子入手：

$$
2\mathrm{H}_2+\mathrm{O}_2 \xrightarrow{\text{燃烧}} 2\mathrm{H}_2\mathrm{O}
$$

规定生成物的化学计量数为正，反应物的为负，并统一用$v_i$表示。各个组分的化学式用$A_i$表示。则此化学反应可写为：

$$
\sum_i v_iA_i=2\mathrm{H}_2\mathrm{O}-2\mathrm{H}_2-\mathrm{O}_2=0
$$

在化学反应中，组分的变化是根据化学计量数的比例进行的，即反应进度的定义。因而可以找到一个共同的比例因子$dn$：

$$
dn_i=v_idn\quad(i=1,2,...,k)
$$

考虑等温等压下的吉布斯平衡判据，并将上式变分代入：

$$
\delta n_i=v_i\delta n\quad\Rightarrow\quad\delta G=\sum_i \mu_i\delta n_i=\delta n\sum_i v_i \mu_i=0\Rightarrow \boxed{\sum_iv_i\mu_i=0}
$$

上式即化学平衡条件。根据$\delta G<0$的趋势，当$\sum_iv_i\mu_i<0$时反应正向进行，$\sum_iv_i\mu_i>0$时反应逆向进行。

**★** 我们将混合气体的$\mu_i=RT(\phi_i+ln(px_i))$代入化学平衡条件：

$$
\sum_iv_i[RT(\phi_i+ln(px_i))]=0\Rightarrow \sum_iv_iln(px_i)=\boxed{-\sum_iv_i\phi_i(T)=lnK_p(T)}
$$

上式中$K_p$即定压平衡常数。严格说平衡常数应由无量纲的相对压强或逸度定义；这里沿用热力学笔记中的简写，把标准压强吸收到$\phi_i(T)$中。利用$p_i=px_i$可将化学平衡条件写为：

$$
K_p(T)=\prod_ip_i^{v_i}=\prod_ip^{v_i}x_i^{v_i}=p^{v}\prod_ix_i^{v_i}=p^{v}K(T,p)
$$

上式中$K(T,p)$称为平衡常数，$v=\sum_iv_i$为化学计量数之和,当反应前后摩尔数不变时，$K(T,p)$也仅仅是温度的函数。

与化学平衡判据类似，当$\prod_ip_i^{v_i}=K_p$时,化学反应平衡。当$\prod_ip_i^{v_i}<K_p$时,化学反应正向进行。当$\prod_ip_i^{v_i}>K_p$时，化学反应逆向进行。
