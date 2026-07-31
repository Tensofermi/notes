# 数据处理与误差估计

Monte Carlo 的输出不是普通确定性程序的输出。每个观测量都带有统计误差，而且相邻样本通常相关。因此数据处理不能只做简单平均，还要判断热化、相关性、误差棒和不同随机种子的合并方式。

一个常见流程是：

$$
{\rm raw\ data}
\rightarrow
{\rm thermalization\ cut}
\rightarrow
{\rm blocking}
\rightarrow
{\rm average/error}
\rightarrow
{\rm fit/collapse}
\rightarrow
{\rm plot}.
$$

## 热化

Markov chain 通常不是从平衡分布开始的。前面一段样本主要反映初始构型，而不是目标分布，需要丢掉。这段过程称为热化。

用转移矩阵语言，若初始分布为 $\boldsymbol p_0$，经过 $n$ 步后

$$
\boldsymbol p_n=\mathbf P^n\boldsymbol p_0.
$$

在满足 ergodicity 和 aperiodicity 的情况下，可以把它写成

$$
\boldsymbol p_n
=
\boldsymbol\pi
+\sum_{\alpha\ge1}c_\alpha\lambda_\alpha^n\boldsymbol v_\alpha.
$$

这里 $\boldsymbol\pi$ 是目标平衡分布，$\lambda_\alpha$ 是转移矩阵的非平稳本征值。热化的意思就是让

$$
\sum_{\alpha\ge1}c_\alpha\lambda_\alpha^n\boldsymbol v_\alpha
$$

足够小，使得样本主要来自 $\boldsymbol\pi$。

最慢衰减通常由第二大本征值控制。若

$$
|\lambda_1|\approx 1,
$$

则热化很慢。对应的指数热化时间为

$$
\tau_{\rm exp}
=
-\frac{1}{\ln|\lambda_1|}
\simeq
\frac{1}{1-|\lambda_1|}.
$$

所以热化步长 $N_{\rm therm}$ 不能只凭感觉给一个固定数字。更合理的经验是让

$$
N_{\rm therm}
$$

至少达到若干倍最慢 relaxation time。实际模拟中 $\lambda_1$ 很少直接可得，因此通常用观测量的时间序列来间接判断。

如果观测量序列为

$$
O_1,O_2,\cdots,O_N,
$$

热化后只使用

$$
O_{N_{\rm therm}+1},\cdots,O_N.
$$

判断热化可以看几个信号：

- 不同初始构型的观测量是否收敛到同一区间。
- 能量、磁化率等慢变量是否已经没有系统漂移。
- 增加热化步数后，最终平均值是否在误差范围内稳定。

临界点附近自关联时间会变长，热化步数也要相应增加。

需要注意，热化和采样相关性是两个不同问题：

- 热化关心初始条件是否已经被遗忘。
- 自关联时间关心平衡态样本之间相隔多少步才近似独立。

一个模拟可能已经热化，但样本仍然高度相关；这时平均值没有明显漂移，误差棒却会被严重低估。

## 样本平均与简单误差

若样本近似独立，均值估计为

$$
\bar O=\frac{1}{N}\sum_{i=1}^N O_i,
$$

误差估计为

$$
{\rm Err}(O)=
\sqrt{\frac{1}{N(N-1)}\sum_{i=1}^N(O_i-\bar O)^2}.
$$

但 Monte Carlo 样本通常来自同一条 Markov chain，相邻样本存在相关性。此时上式会低估误差。

## 自关联时间

定义归一化自关联函数

$$
C(t)=
\frac{\langle (O_i-\bar O)(O_{i+t}-\bar O)\rangle}
{\langle (O_i-\bar O)^2\rangle}.
$$

这里的 $t$ 是 Markov chain 的时间间隔，也就是相隔多少次测量或多少个 sweep。为了避免和温度偏离量混淆，有时也写成 $C_O(\ell)$：

$$
C_O(\ell)
=
\frac{
\langle (O_i-\bar O)(O_{i+\ell}-\bar O)\rangle
}{
\langle (O_i-\bar O)^2\rangle
}.
$$

若样本完全独立，那么

$$
C_O(\ell>0)=0.
$$

Markov chain 样本通常不独立，$C_O(\ell)$ 会随 $\ell$ 衰减。很多时候长时间尾部近似为

$$
C_O(\ell)\sim e^{-\ell/\tau_{\rm exp}}.
$$

这个指数尾部与转移矩阵的第二本征值有关：

$$
\tau_{\rm exp}
=
-\frac{1}{\ln|\lambda_1|}.
$$

更完整地说，观测量 $O$ 的自关联函数可以分解成各个本征模式的叠加：

$$
C_O(\ell)
=
\sum_{\alpha\ge1}a_\alpha(O)\lambda_\alpha^\ell.
$$

其中 $a_\alpha(O)$ 表示观测量 $O$ 与第 $\alpha$ 个慢模的重叠。若某个观测量几乎不耦合最慢模式，它看到的自关联时间可能比全局最慢的 $\tau_{\rm exp}$ 小。因此不同观测量的自关联时间可以不同。

积分自关联时间可写为

$$
\tau_{\rm int}
=
\frac{1}{2}+\sum_{t=1}^{\infty}C(t).
$$

有效独立样本数大约是

$$
N_{\rm eff}\sim \frac{N}{2\tau_{\rm int}}.
$$

这说明采样次数 $N$ 很大并不自动代表误差很小。如果更新算法移动很慢，样本之间高度相关，真正有效的样本数会少很多。

均值误差也要相应修正。若单点方差为

$$
\sigma_O^2=\langle O^2\rangle-\langle O\rangle^2,
$$

则相关样本的均值方差近似为

$$
{\rm Var}(\bar O)
\simeq
\frac{2\tau_{\rm int}\sigma_O^2}{N}.
$$

这和独立样本公式

$$
{\rm Var}(\bar O)=\frac{\sigma_O^2}{N}
$$

相比，多了因子 $2\tau_{\rm int}$。因此

$$
N_{\rm eff}
=
\frac{N}{2\tau_{\rm int}}
$$

可以理解为真正等效的独立样本数。

需要区分两个时间尺度：

| 名称 | 含义 | 主要用途 |
| --- | --- | --- |
| $\tau_{\rm exp}$ | 最慢本征模式的指数衰减时间 | 控制热化尾部 |
| $\tau_{\rm int}$ | 某个观测量自关联函数的积分 | 控制均值误差和有效样本数 |

通常有

$$
\tau_{\rm int}(O)\le \tau_{\rm exp}
$$

的直觉关系，因为 $\tau_{\rm exp}$ 是全局最慢模式，而 $\tau_{\rm int}$ 还取决于观测量是否看得见这个慢模。实际分析时，热化要保守地参考慢变量；误差棒要用目标观测量自己的 $\tau_{\rm int}$ 或 blocking 平台估计。

实际 Monte Carlo 中，$\tau_{\rm exp}$ 往往很难直接测量，因为它需要知道转移矩阵的第二大本征值，或者从自关联函数极长时间尾部中拟合最慢指数衰减。长时间尾部的信号通常噪声很大，尤其在大系统和临界点附近更难稳定估计。

因此误差估计通常使用 $\tau_{\rm int}$。它可以从观测量时间序列直接估计，并且正好进入均值误差公式：

$$
{\rm Var}(\bar O)
\simeq
\frac{2\tau_{\rm int}(O)\sigma_O^2}{N}.
$$

但 $\tau_{\rm int}(O)$ 不是 $\tau_{\rm exp}$ 的简单替代品。它衡量的是观测量 $O$ 的有效独立样本数；$\tau_{\rm exp}$ 衡量的是整条 Markov chain 最慢模式的松弛。若 $O$ 与最慢模式重叠很小，$\tau_{\rm int}(O)$ 可以显著小于 $\tau_{\rm exp}$。因此实践上常见的分工是：

- 用较保守的热化检查和慢变量监控来覆盖 $\tau_{\rm exp}$ 的影响。
- 用 $\tau_{\rm int}(O)$ 或 blocking 平台来给目标观测量估计误差。
- 若专门研究算法动力学指数，再尝试从慢变量的长时间尾部或谱信息估计 $\tau_{\rm exp}$。

## 自关联时间与算法效率

Monte Carlo 算法产生构型的效率，常用自关联时间来衡量。若两个算法每一步计算成本相近，那么 $\tau_{\rm int}$ 小的算法更高效，因为同样长度的 Markov chain 给出更多有效独立样本。

更公平的比较应考虑 CPU 时间。若一次 sweep 的成本为 $c_{\rm sweep}$，则得到一个有效独立样本的大致成本为

$$
c_{\rm eff}
\sim
2\tau_{\rm int}c_{\rm sweep}.
$$

有些非局域算法单步更贵，但自关联时间下降很多，最终仍然更划算。

在临界点附近，自关联时间常随系统尺寸增长：

$$
\tau_{\rm int}\sim L^z.
$$

更准确地说，动态临界指数来自

$$
\tau\sim \xi^z.
$$

临界点有限系统中 $\xi$ 被 $L$ 截断，于是

$$
\tau(L,T_c)\sim L^z.
$$

这里的 $\tau$ 可以有两种常用选择。第一种是最慢 relaxation time：

$$
\tau_{\rm exp}(L,T_c)
\sim L^{z_{\rm exp}}.
$$

它和转移矩阵第二大本征值直接相关：

$$
\tau_{\rm exp}
=
-\frac{1}{\ln|\lambda_1|}
\simeq
\frac{1}{1-|\lambda_1|}.
$$

因此谱隙的有限尺寸标度为

$$
\Delta(L)
=
1-|\lambda_1(L)|
\sim L^{-z_{\rm exp}}.
$$

第二种是实际数据分析中更常用的积分自关联时间：

$$
\tau_{\rm int}(O;L,T_c)
\sim L^{z_{\rm int}(O)}.
$$

这里要把观测量 $O$ 写出来，因为 $\tau_{\rm int}$ 取决于观测量和慢模的重叠。能量、磁化、Binder ratio 或绕数看到的慢模可能不同，因此拟合出来的 $z_{\rm int}$ 也可能不同。若只是笼统写

$$
\tau_{\rm int}\sim L^z,
$$

通常是在上下文已经固定了观测量和算法的情况下省略记号。

需要强调，$z$ 是算法相关的动力学指数。它不是平衡分布本身的静态临界指数。同一个模型、同一个临界点，换一种更新算法，$\nu,\eta,\beta,\gamma$ 不变，但 $z$ 可能显著改变。

局域更新往往有较大的 $z$，这就是临界慢化。cluster、loop、worm 等更新希望通过一次改变大尺度结构来减小 $z$。谱语言中，它们试图让第二本征值远离 $1$，即增大谱隙

$$
\Delta=1-|\lambda_1|.
$$

所以“算法高效”可以从两个等价角度理解：

- 时间序列角度：自关联时间小，有效独立样本数大。
- 转移矩阵角度：谱隙大，非平衡慢模衰减快。

## Blocking

blocking 是处理相关样本的实用方法。把样本按连续区间分成大小为 $B$ 的 block：

$$
\bar O_k^{(B)}
=
\frac{1}{B}\sum_{i=(k-1)B+1}^{kB}O_i.
$$

然后把这些 block average 当作新的样本来估计误差。随着 $B$ 增大，block 之间的相关性降低，误差估计会逐渐进入平台。这个平台值通常比逐点误差更可信。

实际使用中可以画出误差随 block size 的变化。如果误差没有平台，说明样本长度可能还不够。

## 多随机种子合并

实际模拟常用多个随机种子并行计算。假设第 $i$ 组数据给出平均值 $Q_i$ 和误差 $E_i$。如果各组统计独立，可以用反方差加权平均：

$$
Q_{\rm new}
=
\frac{\sum_i Q_i/E_i^2}{\sum_i 1/E_i^2},
\qquad
E_{\rm new}
=
\frac{1}{\sqrt{\sum_i 1/E_i^2}}.
$$

同时可以检查一致性：

$$
\chi^2
=
\sum_i\frac{(Q_i-Q_{\rm new})^2}{E_i^2}.
$$

如果 $\chi^2$ 明显异常，通常说明某些随机种子没有充分热化、误差被低估，或者程序参数并不完全一致。

## 数据组织：从多参数表到一维曲线

一次 Monte Carlo 进程通常只采样参数空间中的一个点。若观测量记为 $\mathcal O$，完整数据其实是一个多元函数：

$$
\mathcal O(L,\beta,J,K,\sigma,\cdots).
$$

实际分析时很少直接处理这个多元函数，而是先固定大部分参数，把数据切成若干条一维曲线。例如：

- 固定 $L,J,K,\sigma$，看 $\mathcal O(\beta)$，用于找临界点。
- 固定 $\beta,J,K,\sigma$，看 $\mathcal O(L)$，用于标度拟合。
- 固定 $L,\beta$，扫描 $\sigma$ 或其他模型参数，观察 crossover。

因此原始数据最好至少保留这些列：

| 类型 | 常见列 |
| --- | --- |
| 模型参数 | $L,\beta,J,K,\sigma,\cdots$ |
| 运行信息 | seed、热化步数、测量步数、bin size |
| 观测量 | mean、error、可选的 autocorrelation 或 blocking 信息 |

整理数据时，一个实用原则是：每一行对应一个物理参数点和一个观测量，每一列只表达一种含义。这样后面按参数筛选、合并随机种子、做交点和拟合都会更稳。

一个比较不容易出错的工作流是：

1. 先按 seed 保存原始时间序列或 bin 后数据，不要只保存最终平均值。
2. 对每个 seed 单独检查热化、blocking 平台和异常漂移。
3. 在确认单个 seed 可靠后，再合并同一参数点的多个 seed。
4. 合并后得到标准表格，例如 $(L,\beta,\sigma,Q,\delta Q)$。
5. 从标准表格中切出一维曲线，例如固定 $(L,\sigma)$ 后得到 $Q(\beta)$。
6. 最后才做交点、collapse 或临界指数拟合。

这样做的好处是每一步都能回退检查。若一开始就把所有 seed 和参数点混成一张最终表，后面发现某个尺寸异常时，很难判断问题来自热化、误差估计、参数录入还是拟合假设。

## 二阶矩关联长度

Monte Carlo 数据分析中经常使用无量纲量 $\xi/L$ 定位临界点。这里的 $\xi$ 常常不是从实空间关联函数直接拟合出来的指数衰减长度，而是 **二阶矩关联长度**。很多文章会直接引用公式

$$
\xi_L
=
\frac{1}{2\sin(k_{\min}/2)}
\sqrt{
\frac{S(\mathbf 0)}{S(\mathbf k_{\min})}
-1
},
$$

其中 $\mathbf k_{\min}$ 是最小非零动量，例如二维方格子上可取

$$
\mathbf k_{\min}=\left(\frac{2\pi}{L},0\right).
$$

这个公式并不是凭空来的。它来自一个很简单的想法：若长距离涨落可以用一个带质量的高斯场近似，那么动量空间关联函数在小 $k$ 处应当具有 Ornstein-Zernike 形式

$$
S(\mathbf k)
\simeq
\frac{A}{\xi^{-2}+k^2}.
$$

这里 $S(\mathbf k)$ 是结构因子，也就是序参量场的动量空间二点函数。对格点自旋或标量场 $\phi_x$，常用定义为

$$
S(\mathbf k)
=
\frac{1}{N}
\left\langle
\left|
\sum_x \phi_x e^{i\mathbf k\cdot x}
\right|^2
\right\rangle .
$$

特别地，

$$
S(\mathbf 0)
=
\frac{1}{N}
\left\langle
\left|
\sum_x\phi_x
\right|^2
\right\rangle
$$

就是零动量涨落，通常和磁化率只差一个温度或体积约定因子。

若体系处在显式外场中，或在有限系统中使用了固定方向的有序态，严格说应使用连通结构因子，即从二点函数中减去

$$
\langle \phi\rangle^2
$$

对应的背景。很多零场模拟中，由于有限系统的对称性没有真正破缺，直接用上面的 $S(\mathbf 0)$ 已经等价于磁化涨落；但在有序相或带外场分析时，这个约定需要写清楚。

如果先在连续空间中推导，取 $\mathbf k=\mathbf 0$ 得到

$$
S(\mathbf 0)
\simeq
\frac{A}{\xi^{-2}},
$$

而小的非零动量给出

$$
S(\mathbf k)
\simeq
\frac{A}{\xi^{-2}+k^2}.
$$

把两式相除：

$$
\frac{S(\mathbf 0)}{S(\mathbf k)}
=
\frac{\xi^{-2}+k^2}{\xi^{-2}}
=
1+k^2\xi^2.
$$

于是

$$
\xi
=
\frac{1}{k}
\sqrt{
\frac{S(\mathbf 0)}{S(\mathbf k)}
-1
}.
$$

这就是二阶矩关联长度公式的连续版本。它的含义是：不用在实空间拟合 $G(r)$ 的指数尾部，只需要比较零动量涨落和最小非零动量涨落，就可以估计关联函数在长波处的宽度。

为什么格点公式里不是 $1/k_{\min}$，而是

$$
\frac{1}{2\sin(k_{\min}/2)}?
$$

原因是格点上的二阶差分在动量空间不是精确的 $k^2$，而是

$$
\hat k^2
=
4\sum_{\mu}
\sin^2\frac{k_\mu}{2}.
$$

对最近邻格点拉普拉斯算符，

$$
-\nabla^2_{\rm lat}
\quad\longleftrightarrow\quad
\hat k^2.
$$

当 $k$ 很小时，$\hat k^2\simeq k^2$，所以连续公式会在大 $L$ 极限恢复。但在有限格点上，使用 $\hat k$ 可以显著减少离散化误差。若只取一个方向的最小动量 $\mathbf k_{\min}=(2\pi/L,0,\cdots)$，则

$$
\hat k_{\min}=2\sin\frac{\pi}{L}
=
2\sin\frac{k_{\min}}{2}.
$$

因此得到常用公式：

$$
\boxed{
\xi_L
=
\frac{1}{2\sin(k_{\min}/2)}
\sqrt{
\frac{S(\mathbf 0)}{S(\mathbf k_{\min})}
-1
}
}.
$$

实际测量时可以对所有等价最小动量方向取平均。例如二维方格子可以同时使用 $(2\pi/L,0)$ 和 $(0,2\pi/L)$，三维可以使用三个坐标方向。这样可以降低统计噪声，也能检查各向同性是否良好。

这个公式有几个使用前提。第一，它依赖小动量处的 Ornstein-Zernike 形状，因此最适合普通二阶相变附近或无序相中的长波涨落。第二，在 BKT 相变、强各向异性体系、长程相互作用体系或存在多个软模的模型中，$\xi_L$ 仍然可以作为非常有用的无量纲量，但对它的解释要谨慎。第三，若序参量有多个分量，应先明确 $S(\mathbf k)$ 是哪个通道的结构因子；例如磁性通道、配对通道、相对相位通道可能给出不同的关联长度。

从数据分析角度，$\xi_L/L$ 常和 Binder ratio、wrapping probability 一样用于交点分析。它的优势是和长波涨落直接相关；缺点是对 $S(\mathbf k_{\min})$ 的统计误差比较敏感，尤其当最小非零动量结构因子很小时，误差会被比值放大。

## 临界点交点外推

很多无量纲量适合用曲线交点定位临界点，例如 Binder ratio、wrapping probability、$\xi/L$ 或某些 winding ratio。设这类量为

$$
Q(\beta,L).
$$

对普通自发对称性破缺相变，有限尺寸标度常写成

$$
Q(\beta,L)
=
f\left[(\beta-\beta_c)L^{1/\nu}\right]
+L^{-\omega}g\left[(\beta-\beta_c)L^{1/\nu}\right]
+\cdots.
$$

若追踪相邻尺寸 $L$ 和 $sL$ 的交点，记为

$$
Q(\beta_L,L)=Q(\beta_L,sL),
$$

则交点位置通常按

$$
\beta_L=\beta_c+aL^{-\omega_{\rm eff}}+\cdots
$$

外推到 $L\to\infty$。这里 $\omega_{\rm eff}$ 不一定等于严格的 leading irrelevant exponent；在数据范围有限时，它常吸收了多个修正项。

实际找交点时，可以先在相邻温度点之间寻找

$$
\Delta Q(\beta)=Q(\beta,sL)-Q(\beta,L)
$$

变号的区间，再用线性或低阶插值得到 $\beta_L$ 和 $Q_L$。如果曲线较平滑，也可以先对每个 $L$ 的 $Q(\beta,L)$ 做局部插值，再解交点。

线性插值的具体形式很简单。假设在 $\beta_a,\beta_b$ 之间发生变号：

$$
\Delta Q_a=\Delta Q(\beta_a),
\qquad
\Delta Q_b=\Delta Q(\beta_b),
\qquad
\Delta Q_a\Delta Q_b<0.
$$

把 $\Delta Q(\beta)$ 近似为直线，则交点位置为

$$
\beta_L
=
\beta_a
-
\Delta Q_a
\frac{\beta_b-\beta_a}{\Delta Q_b-\Delta Q_a}.
$$

再把 $\beta_L$ 代回其中一条插值曲线，就得到交点高度 $Q_L$。这个过程看起来朴素，但很实用：它只依赖交点附近的数据，不会让远离临界点的曲线形状影响结果。

交点误差不能只看单条曲线的误差棒。常用做法是对参与插值的 $Q$ 值按其误差做 bootstrap 或 Gaussian resampling，每次重新求交点，最后用交点样本的标准差作为

$$
\delta\beta_L,\qquad \delta Q_L.
$$

这样误差传播会自然包含曲线斜率的影响：交点附近曲线越平，$\beta_L$ 的不确定性越大。

实际分析中还要做两个稳定性检查。第一，改变尺寸配对，例如比较 $(L,2L)$ 和 $(L,3L/2)$ 的交点外推是否一致。第二，改变拟合最小尺寸 $L_{\min}$。若去掉小尺寸后 $\beta_c$ 明显漂移，说明有限尺寸修正还没有被拟合式充分描述。

## BKT 临界点的对数外推

BKT 相变的临界点外推和普通二阶相变不同，因为关联长度不是幂律发散，而是

$$
\xi\sim
\exp\left(\frac{b}{\sqrt{|T-T_{\rm BKT}|}}\right).
$$

有限尺寸 $L$ 截断关联长度时，伪临界点偏移通常带有对数形式。若用某个固定的无量纲值 $Q^\ast$ 截取不同尺寸曲线

$$
Q(\beta_L,L)=Q^\ast,
$$

常用外推形式为

$$
\beta_L
=
\beta_c+\frac{a}{(\ln L/L_0)^2}
+\cdots.
$$

这里 $L_0$ 和 $a$ 是拟合参数或半经验参数。实际使用时不要只选一个 $Q^\ast$：应改变若干个位于临界区域附近的截取值，检查外推出的 $\beta_c$ 是否在误差内一致。若不同 $Q^\ast$ 给出系统性漂移，通常说明尺寸还不够大，或者对数修正没有被充分吸收。

BKT 外推最容易踩的坑是把它当成普通幂律相变处理。若直接用

$$
\beta_L=\beta_c+aL^{-\omega}
$$

去拟合 BKT 伪临界点，有限尺寸范围不大时也可能看起来能拟合，但得到的 $\beta_c$ 往往带有系统偏差。BKT 的对数修正收敛很慢，因此更应该把不同判据放在一起比较：固定 $Q^\ast$ 截距、stiffness universal jump、$\eta=1/4$、vortex 观测量或 BKT collapse。多个判据一致时，临界点判断才比较可信。

## Reweighting

如果模拟在参数 $K_0$ 下采样，而目标是附近的 $K$，可以使用 reweighting。设构型能量相关量为 $E(s)$，权重变化为

$$
\frac{W_K(s)}{W_{K_0}(s)}
=
e^{-(K-K_0)E(s)}.
$$

则观测量可估计为

$$
\langle O\rangle_K
=
\frac{
\langle O(s)e^{-(K-K_0)E(s)}\rangle_{K_0}
}{
\langle e^{-(K-K_0)E(s)}\rangle_{K_0}
}.
$$

reweighting 的有效范围取决于两个分布的重叠程度。离采样点太远时，估计会被少数样本支配，误差迅速变差。

## 拟合与画图

Monte Carlo 数据最终通常用于拟合临界点、临界指数或有限尺寸标度函数。拟合前要确认三件事：

- 误差棒是否包含自关联和多随机种子合并的不确定性。
- 不同系统尺寸、参数点的采样质量是否相近。
- 拟合区间是否避开明显的有限尺寸修正或非渐近区域。

图像展示时，平均值和误差棒同样重要。没有误差棒的 Monte Carlo 图通常不能支持定量结论。
