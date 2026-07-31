# 第五章 金属电子论

## 金属的电导和热导

### 1.德鲁特模型
将金属中的自由电子看作理想气体，并利用如下近似：

(1)自由电子近似：除了碰撞，忽略电子与离子之间的相互作用。

(2)独立电子近似：忽略电子与电子之间的相互作用。

(3)碰撞假设：电子碰撞后的速度仅与碰撞时的温度有关，速度的方向是各向同性的。电子通过碰撞处于热平衡状态。

(4)弛豫时间近似：电子两次碰撞之间的平均时间$\tau$称为弛豫时间，电子在$dt$时间所受碰撞的概率正比于$dt/\tau$.利用平均自由程$\ell$和方均根速率$v_{rms}$可将弛豫时间表示为$v_{rms}\cdot\tau=\ell$

(5)经典粒子假设(隐含假设)：默认电子是经典粒子，满足M.B.分布和经典能量均分定理。

根据这些假设，分析电子的动量变化。当电子受到碰撞时，电子向各个方向运动，从而对平均动量无贡献；当未发生碰撞时，电子受外力加速，从而对平均动量有贡献，由此：

$$
\vec{p}(t+dt)=\left(1-\frac{dt}{\tau}\right)[\vec{p}(t)+\vec{F}(t)dt]
$$

忽略高阶小量之后，得到：

$$
m_e\frac{d\vec{v}(t)}{dt}=\vec{F}(t)-\frac{m_e\vec{v}(t)}{\tau}
$$

**金属电导率**：考虑$\vec{F}(t)=-e\vec{E}$,并代入试解$\vec{v}=\vec{v}_0e^{-i\omega t}$得到：

$$
\vec{v}_0=\frac{e\vec{E}_0}{im_e(\omega+i/\tau)}\quad\Rightarrow\quad\vec{j}(\vec{r},t)=-n_ee\vec{v}(\vec{r},t)=-\frac{n_ee^2}{im_e(\omega+i/\tau)}\vec{E}_0
$$

由金属的本构关系$\vec{j}=\sigma\vec{E}_0$可知：

$$
\sigma(\omega)=-\frac{n_ee^2}{im_e(\omega+i/\tau)}\qquad\qquad\boxed{\sigma(0)=\frac{n_ee^2}{m_e}\tau=\frac{n_ee^2\ell}{m_ev_{rms}}}
$$

从而导出金属电导率的表达式，可见其仅与电子密度$n_e$和弛豫时间$\tau$有关。在室温下，典型金属电阻率约为$\rho\sim10^{-6}\Omega\cdot cm$，对应电导率$\sigma\sim10^{6}(\Omega\cdot cm)^{-1}$；弛豫时间$\tau\sim10^{-14}s$,平均自由程$\ell\sim1nm$,正好是原子的间距量级。

**金属热导率**：根据分子动理学的理论分析，并假设电子热容满足经典能量均分(实际上电子热容与温度呈一次方关系)，则：

$$
\kappa=\frac{1}{3}C_ev_{rms}\ell=\frac{1}{3}C_ev_{rms}^2\tau=\frac{1}{2}n_ek_Bv_{rms}^2\tau=\frac{1}{2}n_ek_Bv_{rms}\ell
$$

**维德曼-夫兰兹定律**：根据金属的电导率和热导率的比值，以及动能与温度的关系，不难得到：

$$
\frac{1}{2}m_ev_{rms}^2=\frac{3}{2}k_BT\quad\Rightarrow\quad\boxed{\frac{\kappa}{\sigma}=\frac{3}{2}\left(\frac{k_B}{e}\right)^2T}
$$

即在一定温度下，金属的电导率与热导率成正比，即维德曼-夫兰兹定律。虽然德鲁特模型似乎可以解释这一现象，但对定量的实验结果却差了一倍之多。

### 2.索末菲模型
为了处理德鲁特模型当中残留的经典力学印记，索末菲模型利用量子理论，将金属视为囚禁电子的无限深势阱，结合F.D.分布，将电子的方均根速度修正为费米速度$v_F$，电子能量修正为费米能级$E_F$：

$$
k_F=(3\pi^2n_e)^{1/3}\qquad v_F=\frac{\hbar k_F}{m_e}\qquad E^0_F=\frac{\hbar^2k_F^2}{2m_e}=k_BT_F\qquad\overline{E}=\frac{3}{5}E^0_F
$$

这在$T=0K$下得到的结果。对于$T\neq0K$的情况，其相关物理量为：

$$
E_F=E_F^0\left[1-\frac{\pi^2}{12}\left(\frac{k_BT}{E_F^0}\right)^2\right]\quad U=\frac{3}{5}NE_F^0\left[1+\frac{5}{12}\pi^2\left(\frac{k_BT}{E_F^0}\right)^2\right]\quad C_e=N\frac{\pi^2k_B^2T}{2E_F^0}
$$

*上面的详细推导参考统计物理的相关部分。相比统计物理更加数学化的做法，这里通常在倒空间，用能态密度以及“费米球”的概念来计算费米能。*由于金属的费米温度都很高，满足$T_F\gg T$,因而离费米面远的能量的电子都保持在$T=0K$的状态，并且有$E^0_F\approx E_F$.

有了修正的电子热容，再将$v_{rms}$替换为$v_F$,就可以得到修正维德曼-夫兰兹定律：

$$
\boxed{\frac{\kappa}{\sigma}=\frac{1}{3}\left(\frac{\pi k_B}{e}\right)^2T}
$$

从而定量上与实验基本符合，但在低温下，由于热传导与导电过程的弛豫时间$\tau$并不相等，从而导致低温下的计算结果与实验偏差过大。

*对于 $s$ 维空间的费米波矢，可写为：*

$$
\boxed{k_F=4^{\frac{s-1}{2s}}\sqrt{\pi}\left[n\left(\frac{s}{2}!\right)\right]^{\frac{1}{s}}}
$$

*具体过程，详见“补充内容”。*

**马西森定则**:金属的电阻分为与温度有关的本征电阻$\rho_L$以及与温度无关的剩余电阻$\rho_0$,从而：

$$
\rho(T)=\rho_0+\rho_L(T)
$$

可以这样理解：索末菲模型当中的电子与离子实的碰撞，实际上是电子德布罗意波被不完美晶格的散射，如晶格振动(声子)、点缺陷或杂质原子等。在理想晶格则不发生散射，如光通过透明的晶体一样，这时晶体内电子的平均自由程无限大，从而没有电阻。本征电阻$\rho_L$是电子与晶格振动散射的结果，因而温度越高，越偏离理想晶格，从而电阻越大。剩余电阻$\rho_0$是自由电子与晶格中缺陷或杂质原子等散射产生的，仅依赖于缺陷或杂质的浓度，在低温下占主要贡献。

**自由电子气模型的局限性**：自由电子气模型不仅简单，而且对于一价金属的电子热容、泡利顺磁、维德曼-夫兰兹定律等符合的相当好；同时自由电子忽略了电子与晶格的作用，因而对一些实验结果无法解释：(1)无法给出各向异性晶体的电导率，例如石墨(2)对于贵金属的热容难以解释(3)无法解释导体、半导体、绝缘体产生的根源(4)默认金属费米面是球面，然而实验表明，通常情况下，金属费米面都不是球面。

*事实上，自由电子气模型是在能带理论建立之前的，不过由于国内大部分教材都是将金属电子论放在能带理论之后，因而本套梳理也采用了这样的顺序。*

### 3.利用玻尔兹曼方程计算电导
玻尔兹曼方程常用于处理输运问题，即由强度量的不均匀分布引起的广延量的流动。在金属导电问题当中，与之对应的是电势的不均匀分布引起的电荷的流动；因而需要计算的便是它们之间的关联量——电阻率$\rho$.*为了简洁，这里仅仅给出电阻率与温度的关系所需要的推导，对于一些细节做了省略。*

设分布函数$f(\vec{k},\vec{r},t)$,考虑到$J_e=nqv$,从而电流$\vec{J}_e$可以表达为：

$$
\boxed{\vec{J}_e=-\frac{2e}{(2\pi)^3}\int \vec{v}(\vec{k})f(\vec{k})d\vec{k}}
$$

因而关键是计算出$f$的表达式，即可根据$J_e=\sigma E$给出电导率的表达式。为了求出$f$，考虑其随时间的演化，这归功于电子随电场的漂移和与其他粒子的碰撞：

$$
\frac{\partial f}{\partial t}=\left(\frac{\partial f}{\partial t}\right)_{shift}+\left(\frac{\partial f}{\partial t}\right)_{coll}
$$

对于漂移，假设空间各向同性，有$\nabla_{k} \vec{k}=\nabla_{r} \vec{r}=Const.$,由连续性方程展开得到：

$$
\left(\frac{\partial f}{\partial t}\right)_{shift}=-\frac{d\vec{k}}{dt}\cdot\nabla_{k}f-\frac{d\vec{r}}{dt}\cdot\nabla_r f
$$

对于碰撞，考虑散射前后两个态$\vec{k}$和$\vec{k}'$,设其单位时间跃迁概率为$\theta(\vec{k},\vec{k}')$,且不考虑自旋改变的情况，那么单位时间从$k$态流走的概率$a$为：

$$
a=\frac{1}{(2\pi)^3}\int f(\vec{k})[1-f(\vec{k}')]\theta(\vec{k},\vec{k}')d\vec{k}'
$$

同理，也可得到单位时间流入$k$态的概率$b$,并引入唯象的弛豫时间$\tau(\vec{k})$,使用线性假设，用与平衡态分布$f_0$的差值描述碰撞带来的回复效果:

$$
\left(\frac{\partial f}{\partial t}\right)_{coll}=b-a=-\frac{f-f_0}{\tau(\vec{k})}
$$

考虑定态问题，即满足$\frac{\partial f}{\partial t}=0$,并且仅考虑电场，不考虑温度场等分布，并利用$\frac{d\vec{k}}{dt}=\frac{-e\vec{E}}{\hbar}$得到：

$$
\boxed{\frac{e}{\hbar}\vec{E}\cdot\nabla_{k}f=\frac{f-f_0}{\tau(\vec{k})}}
$$

弱场近似下，可将$f$展开为$f\approx f_0+f_1$,代入得到:

$$
f_1=-e\tau(\vec{k})\vec{E}\cdot\vec{v}(\vec{k})\left(-\frac{\partial f_0}{\partial E}\right)\approx -e\tau(\vec{k})\vec{E}\cdot\vec{v}(\vec{k})\delta(E-E_F)
$$

从而将$f$代入$J_e$当中，对比$J_e=\sigma E$可得电导率为：

$$
\sigma=\frac{1}{4\pi^3}\frac{e^2}{\hbar}\int\tau(\vec{k}_F)\frac{\vec{v}(\vec{k}_F)\vec{v}(\vec{k}_F)}{|\vec{v}(\vec{k}_F)|}dS_F\quad\rightarrow\quad\boxed{\sigma=\frac{ne^2\tau(\vec{k}_F)}{m^*}}
$$

若考虑费米面为球面，得到上式电导率与弛豫时间正比的关系式，从而电阻率和弛豫时间成反比。到此为止，只需要搞清楚$\frac{1}{\tau}$与温度的关系，即可得到电阻率与温度的关系。设散射前后波矢的夹角为$\eta$,并考虑弹性散射带来的细致平衡$\theta(\vec{k},\vec{k}')=\theta(\vec{k}',\vec{k})$,再利用几何关系，可以导出：

$$
\boxed{\frac{1}{\tau(\vec{k})}=\frac{2\pi}{(2\pi)^3}\int\theta(\vec{k},\vec{k}',\eta)(1-\cos\eta)k_F^2\sin\eta\,d\eta}
$$

建立了$\tau$与$\theta$的关系之后，下面只要得到$\theta$的表达式，问题就解决了。由于电阻是由于非周期的势场引起的，因而将非周期部分的势场当做微扰，利用量子力学微扰的方法，代入一维原子链的色散关系进行计算，并且仅考虑N过程，最终得到：

$$
\theta(\vec{k},\vec{k}',\vec{q})=\frac{\pi^2}{Nmc^2}\left|\hat{e}\cdot\frac{I_{kk'}}{|\vec{q}|}\right|^2n(\vec{q})\omega(\vec{q})\delta_{k'_F-k_F,\pm q}\delta[E(\vec{k}')-E(\vec{k})]
$$

代入，得到弛豫时间的表达式：

$$
\boxed{\frac{1}{\tau}=\frac{3}{(2\pi)^4}\frac{\pi^2}{Nmc^2}k_F^2\left(\frac{dE}{dk}\right)_{k_F}^{-1}\int\left|\hat{e}\cdot\frac{I_{kk'}}{\left|\vec{k}'_F-\vec{k}_F\right|}\right|^2n(\vec{k}'_F-\vec{k}_F)\omega(\vec{k}'_F-\vec{k}_F)(1-\cos\eta)\sin\eta\,d\eta}
$$

其中$\omega(q)=cq$.下面考虑高温和低温近似，分析电阻与温度的关系：

在高温下，由于$k_BT\gg\hbar\omega$：

$$
n(\vec{k}_F-\vec{k}'_F)=\frac{1}{e^{\frac{\hbar\omega(\vec{k}_F-\vec{k}'_F)}{k_BT}}-1}\approx\frac{k_BT}{\hbar\omega(\vec{k}_F-\vec{k}'_F)}
$$

进而电阻呈$T$律，电导呈$\frac{1}{T}$律.

在低温下，主要考虑小波矢的小角度散射，即$\eta\rightarrow0$：

$$
1-\cos\eta\rightarrow\frac{1}{2}\eta^2\qquad \sin\eta\rightarrow\eta  \qquad \omega=c\left|\vec{k}'_F-\vec{k}_F\right|\rightarrow ck_F\eta
$$

注意这里最后一式将$\eta$与$\omega$联系了起来，令$z=\frac{\hbar\omega}{k_BT}$,将$\eta$换元后，可以提出$T^5$项，即电阻呈$T^5$律，电导呈$\frac{1}{T^5}$律.其中$T^3$来自声子数量的贡献，$T^2$来自声子对电子散射的贡献，由于电子-电子散射过小，故忽略。

## 金属的费米面

前面假设金属的费米面呈球形，而事实上由于周期势场的作用，当费米面开始靠近布里渊区边界时，会发生畸变，从上一章等能面垂直于布里渊区边界的性质也可以想见这一点。为了绘制更加真实的费米面，哈里森基于垂直关系，发明了一套构图法，可以简便的描绘出费米面的大体形貌。此外，也可以利用费米波矢$k_F$和电子浓度$n$，估算费米球的大小，进而对不同类型的金属进行分析：

1.碱金属

具有bcc结构，且核外仅一个电子，其第一布里渊区为正十二面体，从中心到边界的最短距离约为$1.414\frac{\pi}{a}$,电子浓度为$n=\frac{2}{a^3}$.对于三维空间的费米波矢$k_F=(3n\pi^2)^{1/3}\approx1.24\frac{\pi}{a}$,因而完全落在第一布里渊区，故非常接近自由电子。

2.贵金属

以Cu为例，具有fcc结构，核外仅有一个在4s态上的电子，因而费米波矢$k_F=(3n\pi^2)^{1/3}\approx1.563\frac{\pi}{a}$,而第一布里渊区的内切球半径为$1.732\frac{\pi}{a}$,看似完全落在第一布里渊区，实际上还是会在边界的方向上发生畸变。此外，由于3d电子的影响，贵金属的许多性质与碱金属不同。

3.二价金属和三价金属

不难估算，其费米波矢都超过第一布里渊区，因而会发生严重的畸变，从而不能用自由电子气描述。

*关于测量费米面的方法，见上一章磁场中准经典运动的部分，这里从略。*

## 功函数和接触电势

功函数：设电子能量达到$E_0$时，电子脱离金属束缚，考虑到电子的费米能量$E_F$，则功函数$W=E_0-E_F$.由于热激发可近似为M.B.分布，但速度$v=\hbar \frac{k}{m}$、态密度等物理量需要采用量子力学的描述，进而由此得到热激发电流密度：

$$
j=BT^2e^{-\frac{W}{k_BT}}
$$

接触电势：两块金属由于费米能量的不同，接触后费米面高的会有电子流向费米面低的一侧，从而使得一侧带正电，一侧带负电，进而产生接触电势。

*P.S.关于半导体的理论部分，主要是基于在价带$E_v$和导带$E_c$的边界处进行自由电子近似的展开，并假设近似服从M.B.分布，讨论价带空穴和导带电子在电场下漂移和扩散的问题，从基本的pn结逐渐上升为复杂器件的过程，详见“补充内容”，这里从略。*
