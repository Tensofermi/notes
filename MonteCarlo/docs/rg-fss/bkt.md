# BKT 相变

Berezinskii-Kosterlitz-Thouless 相变是二维连续对称性体系中最特别的一类相变。它和普通 Landau 相变不同：低温相没有真正的长程序，但有代数衰减的准长程序；高温相是指数衰减的无序相；两者之间的转变由拓扑缺陷，也就是 vortex 的束缚与解束缚控制。

最典型的例子是二维 XY 模型：

$$
H=-J\sum_{\langle ij\rangle}
\cos(\theta_i-\theta_j),
$$

其中

$$
\mathbf S_i=(\cos\theta_i,\sin\theta_i).
$$

它具有全局 $U(1)$ 连续对称性：

$$
\theta_i\to \theta_i+\alpha.
$$

根据 Mermin-Wagner 定理，二维 XY 模型在有限温不能有真正的

$$
\langle e^{i\theta}\rangle\ne0.
$$

但这不意味着它只能有普通无序相。二维 XY 模型低温下可以有准长程序。

## 先看物理直觉

低温时，相邻角度差较小，可以写成 spin-wave 理论：

$$
H_{\rm sw}
=
\frac{\rho_s}{2}
\int d^2x\,(\nabla\theta)^2.
$$

这个高斯理论给出关联函数

$$
G(r)
=
\left\langle
e^{i[\theta(r)-\theta(0)]}
\right\rangle
\sim
r^{-\eta}.
$$

其中

$$
\eta=\frac{T}{2\pi\rho_s}.
$$

这说明低温相具有代数长程序，而非真正的常数长程序。代数衰减比指数衰减慢得多，因此仍然代表一种临界相。

二维 XY 模型还有一个 spin-wave 理论看不到的自由度：vortex。绕着 vortex 走一圈，角度变化为

$$
\oint \nabla\theta\cdot d\mathbf l
=
2\pi q,
$$

其中

$$
q\in\mathbb Z
$$

是 vortex charge。$q=1$ 是 vortex，$q=-1$ 是 antivortex。

低温下，vortex 和 antivortex 倾向于成对束缚；高温下，vortex 对可以解束缚，形成自由 vortex 气体。BKT 相变就是 vortex pair unbinding transition。

## 单个 vortex 的能量和熵

考虑一个位于原点、charge 为 $q$ 的 vortex。远离核心时，

$$
\theta(\mathbf r)=q\varphi,
$$

于是

$$
|\nabla\theta|=\frac{|q|}{r}.
$$

代入 spin-wave 能量：

$$
E_v
=
\frac{\rho_s}{2}
\int_a^L d^2x\,(\nabla\theta)^2.
$$

使用极坐标：

$$
\begin{aligned}
E_v
&=
\frac{\rho_s}{2}
\int_a^L r\,dr
\int_0^{2\pi}d\varphi
\frac{q^2}{r^2}\\
&=
\pi\rho_s q^2
\ln\frac{L}{a}.
\end{aligned}
$$

这里 $a$ 是 vortex core 尺度，$L$ 是系统尺寸。单个 vortex 的能量随系统尺寸对数发散。

但 vortex 可以放在系统中很多位置。位置数约为

$$
\left(\frac{L}{a}\right)^2,
$$

所以熵为

$$
S_v
\simeq
2\ln\frac{L}{a}.
$$

自由能为

$$
F_v
=
E_v-TS_v
=
\left(\pi\rho_s q^2-2T\right)
\ln\frac{L}{a}.
$$

对最小 vortex $q=\pm1$：

$$
F_v
=
\left(\pi\rho_s-2T\right)
\ln\frac{L}{a}.
$$

若

$$
T<\frac{\pi\rho_s}{2},
$$

单个自由 vortex 的自由能随 $L$ 增大而变大，自由 vortex 被抑制。若

$$
T>\frac{\pi\rho_s}{2},
$$

熵占优，自由 vortex 会大量出现。

这个简单能熵竞争给出 BKT 相变的核心直觉：

$$
\boxed{
T_{\rm BKT}
\simeq
\frac{\pi\rho_s}{2}.
}
$$

更精确地说，$\rho_s$ 应该取为重整化后的 stiffness。

## vortex 对与二维 Coulomb gas

多个 vortex 的角度场可以写为多个解的叠加。将其代入能量后，得到 vortex 之间的对数相互作用：

$$
E_{\rm vort}
=
\pi\rho_s
\sum_i q_i^2\ln\frac{L}{a}
-2\pi\rho_s
\sum_{i<j}
q_iq_j
\ln\frac{r_{ij}}{a}
+N_v E_c.
$$

这里 $E_c$ 是 vortex core energy。有限能构型需要总 charge 为零：

$$
\sum_i q_i=0.
$$

因此二维 XY 模型的 vortex 部分可以映射为二维 Coulomb gas：正负电荷之间具有对数相互作用。

定义无量纲 stiffness

$$
K=\frac{\rho_s}{T},
$$

以及 vortex fugacity

$$
y=e^{-E_c/T}.
$$

小 $y$ 表示 vortex 核心能很大，自由 vortex 稀少；大 $y$ 表示 vortex 容易出现。

## RG 方程的物理来源

BKT RG 的思想是逐步积分掉短距离的 vortex-antivortex 小偶极对，然后看 $K$ 和 $y$ 如何变化。

先看 fugacity 的 scaling。一个 vortex-antivortex 小对的相对位置积分有二维面积因子，因此粗粒化时有

$$
y\to y b^2.
$$

但产生一个 vortex 对还要付出对数相互作用能。最小 vortex 的能量贡献带来因子

$$
b^{-\pi K}.
$$

所以最低阶下

$$
y'\sim y b^{2-\pi K}.
$$

写成微分形式：

$$
\boxed{
\frac{dy}{dl}
=
(2-\pi K)y
}
$$

其中

$$
l=\ln b.
$$

这条式子说明：当

$$
\pi K>2,
$$

vortex fugacity 是 irrelevant，低温下 vortex 对被束缚；当

$$
\pi K<2,
$$

vortex fugacity 是 relevant，高温下自由 vortex 增殖。

第二条 RG 方程描述 vortex 小偶极对对 stiffness 的屏蔽。vortex 对会极化，削弱长距离 stiffness，因此

$$
\boxed{
\frac{dK^{-1}}{dl}
=
4\pi^3 y^2
}
$$

到最低非平凡阶，BKT RG 方程为

$$
\boxed{
\begin{aligned}
\frac{dK^{-1}}{dl}
&=
4\pi^3y^2,\\
\frac{dy}{dl}
&=
(2-\pi K)y.
\end{aligned}
}
$$

不同文献会对 $K$ 和 $y$ 采用不同归一化，数值系数可能变化，但方程结构相同。

## RG 流图

RG 流有三类重要区域。

第一，低温区域：

$$
K>\frac2\pi.
$$

此时

$$
\frac{dy}{dl}<0,
$$

vortex fugacity 流向

$$
y\to0.
$$

系统流向一条 Gaussian fixed line。低温相是一整条临界线，不是一个孤立固定点。不同温度对应不同 stiffness 和不同指数

$$
\eta=\frac{1}{2\pi K}.
$$

第二，高温区域：

$$
K<\frac2\pi.
$$

此时 $y$ 增长，vortex 解束缚，系统进入指数关联的无序相。

第三，临界 separatrix。它把束缚相和解束缚相分开。在线性近似中，临界条件为

$$
\pi K_c=2.
$$

于是

$$
K_c=\frac2\pi.
$$

代回

$$
\eta=\frac{1}{2\pi K},
$$

得到 BKT 转变点处的普适指数

$$
\boxed{
\eta(T_{\rm BKT})=\frac14.
}
$$

## 普适刚度跳跃

由于

$$
K=\frac{\rho_s}{T},
$$

临界条件

$$
K_c=\frac2\pi
$$

给出

$$
\boxed{
\rho_s(T_{\rm BKT}^-)
=
\frac{2T_{\rm BKT}}{\pi}.
}
$$

这就是 Nelson-Kosterlitz universal jump。它的含义是：从低温侧接近 BKT 转变时，重整化后的 stiffness 到达普适值；一旦进入高温侧，自由 vortex 屏蔽 stiffness，使长距离 stiffness 跳到零。

在 Monte Carlo 中，二维量子 boson 或 classical XY 模型常通过 helicity modulus、spin stiffness 或 winding number 来估计 $\rho_s$，再用这条普适跳跃关系定位 $T_{\rm BKT}$。

## 超流与 XY 模型的对应

BKT 理论不只适用于经典 XY 磁体，也适用于二维超流的相位涨落。以 Bose-Hubbard 模型为例：

$$
H
=
-t\sum_{\langle ij\rangle}
(b_i^\dagger b_j+b_j^\dagger b_i)
+\frac{U}{2}\sum_i n_i(n_i-1)
-\mu\sum_i n_i.
$$

在振幅涨落较小的超流区域，可以写成

$$
b_i\simeq \sqrt{\rho_0}e^{i\theta_i}.
$$

代入 hopping 项得到

$$
-t(b_i^\dagger b_j+b_j^\dagger b_i)
\simeq
-2t\rho_0\cos(\theta_i-\theta_j).
$$

于是低能有效模型就是二维 XY 模型：

$$
H_{\rm eff}
=
-J\sum_{\langle ij\rangle}
\cos(\theta_i-\theta_j),
\qquad
J\simeq 2t\rho_0.
$$

这里 $\theta_i$ 是超流相位，$J$ 或连续理论中的 $\rho_s$ 是相位刚度。超流速度与相位梯度相关：

$$
\mathbf v_s
\propto
\nabla\theta.
$$

绕闭合路径一圈时，

$$
\oint\nabla\theta\cdot d\mathbf l
=
2\pi n,
\qquad n\in\mathbb Z.
$$

因此 vortex 在超流语言中就是量子化环流的拓扑缺陷。二维超流失去相干性的方式，正是 vortex-antivortex 对从束缚到解束缚。

这个对应在数值上很有用：classical XY 模型、二维量子 boson 的 winding number、helicity modulus 和 superfluid stiffness 常常描述同一类长距离物理，只是显微模型不同。

这里要注意“有序”的说法。在二维有限温短程体系中，单粒子相位关联不能趋向常数，因此严格地说没有真正的

$$
\langle b\rangle\ne0.
$$

但低温 BKT 相中，关联函数可以代数衰减：

$$
\langle b^\dagger(r)b(0)\rangle
\sim r^{-\eta}.
$$

这种准长程序足以给出非零的长距离刚度和稳定的超流响应。数值上如果只看有限尺寸的磁化或 condensate fraction，很容易误以为有普通长程序；因此 BKT 分析更应该看 stiffness、winding、关联指数和对数修正。

## 双层 XY、PSF 与配对 BKT 图像

双层或两组分体系提供了一个稍丰富的 BKT 图像。一个简化的双层 XY 模型可写为

$$
H
=
-J\sum_{\langle ij\rangle}
\left[
\cos(\theta_{i,a}-\theta_{j,a})
+\cos(\theta_{i,b}-\theta_{j,b})
\right]
-K\sum_i\cos(\theta_{i,a}-\theta_{i,b}).
$$

定义对称和反对称相位：

$$
\theta_+
=
\frac{\theta_a+\theta_b}{2},
\qquad
\theta_-
=
\frac{\theta_a-\theta_b}{2}.
$$

$\theta_+$ 描述整体相位，也就是总超流通道；$\theta_-$ 描述两层之间的相对相位。层间耦合 $K$ 会倾向于锁定相对相位，使低能涨落主要由整体相位控制。

把层内梯度项用这两个变量改写，可以看到两个通道的含义更清楚。连续近似下，

$$
(\nabla\theta_a)^2+(\nabla\theta_b)^2
=
2(\nabla\theta_+)^2
+2(\nabla\theta_-)^2.
$$

层间项则近似为

$$
-K\cos(\theta_a-\theta_b)
=
-K\cos(2\theta_-).
$$

因此 $\theta_-$ 会受到一个 pinning potential，而 $\theta_+$ 仍然是整体 $U(1)$ 相位。若相对相位被锁住，两层的 vortex 倾向于绑定在一起；若相对通道也很软，就可能出现更丰富的 defect，例如只在一层中出现的 vortex、两层共同 vortex、或相对相位的 domain-wall-like 激发。

在配对超流的语言中，单粒子相干可能被抑制，而配对算符仍保持相干：

$$
\langle b\rangle=0,
\qquad
\langle b^2\rangle\ne0
$$

或在二维有限温体系中表现为配对关联的代数衰减。对应的 BKT 转变可以理解为“配对相位”的 vortex 解束缚，而不是单粒子相位的普通 XY 解束缚。

更具体地说，若低能有效自由度不是单个相位 $e^{i\theta}$，而是配对相位

$$
e^{i2\theta},
$$

那么最自然的关联函数也从单粒子关联变成配对关联：

$$
G_1(r)=\langle b^\dagger(r)b(0)\rangle,
\qquad
G_2(r)=\langle b^{\dagger 2}(r)b^2(0)\rangle.
$$

普通超流中，$G_1$ 和 $G_2$ 都可以有代数衰减；配对超流中，$G_1$ 可能指数衰减，而 $G_2$ 仍然代数衰减。此时 Monte Carlo 或张量网络分析应优先看配对关联、配对刚度、相对通道是否 gapped，以及对应 vortex 的行为。

从 BKT 角度看，配对相位的基本 vortex 和单粒子相位的 vortex 不是同一个对象。若物理有序变量是 $e^{i2\theta}$，那么 $\theta$ 绕 $\pi$ 已经让 $2\theta$ 绕 $2\pi$。这类 half-vortex 或 composite vortex 是否允许、能量如何、是否被层间耦合禁闭，都会影响实际相图。教程里不把这些说成普遍结论，是因为它们依赖具体模型；但作为读图方式，它提醒我们：多通道 BKT 相变的关键是先找出真正保持代数关联的相位变量。

需要谨慎的是，具体 bilayer 模型可能有多个通道、多个刚度和不同类型的 vortex，例如单层 vortex、两层共同 vortex、相对相位 defect 等。哪些缺陷先增殖取决于耦合、密度、约束和观测量定义。因此在教程中更稳妥的说法是：双层 XY 和 PSF 提供了 BKT 机制在多通道相位场中的一个重要背景，而具体相图需要由模型和数值数据决定。

实际读 bilayer 或 PSF 数值结果时，可以按下面顺序整理：

1. 写清楚显微自由度：两层、两组分，还是单组分但允许配对。
2. 找出低能相位变量：总相位、相对相位、配对相位分别是什么。
3. 判断哪些通道有刚度，哪些通道被 pin 住或变成 massive。
4. 对每个候选相位变量写出相应关联函数。
5. 再讨论 vortex 解束缚和 BKT 临界点。

这样做可以避免把“单粒子超流消失”“配对超流出现”“相对相位锁定”“BKT 转变”混成同一句话。它们有关联，但不是同一个判断。

## 关联长度的本质奇异性

普通二阶相变中，关联长度通常幂律发散：

$$
\xi\sim |T-T_c|^{-\nu}.
$$

BKT 相变不同。高温侧接近 $T_{\rm BKT}$ 时，RG 流在临界 separatrix 附近走得非常慢，最终才流向强耦合无序相。这导致关联长度呈本质奇异性：

$$
\boxed{
\xi
\sim
\exp\left(
\frac{b}{\sqrt{T-T_{\rm BKT}}}
\right)
}
\qquad (T>T_{\rm BKT}).
$$

这里 $b$ 是非普适常数。这个公式说明 BKT 相变非常难数值定位：$\xi$ 增长极快，有限尺寸系统很容易误以为自己还在临界相。

## 有限尺寸标度和 Monte Carlo 判据

BKT 相变的有限尺寸分析不能直接套普通二阶相变的幂律形式

$$
tL^{1/\nu}.
$$

因为 BKT 的关联长度不是幂律发散。常用判据包括：

1. **helicity modulus 或 stiffness jump**：

$$
\rho_s(T_{\rm BKT})
=
\frac{2T_{\rm BKT}}{\pi}.
$$

有限尺寸下有对数修正，常用形式为

$$
\rho_s(L,T_{\rm BKT})
=
\frac{2T_{\rm BKT}}{\pi}
\left[
1+\frac{1}{2\ln L+C}
\right],
$$

其中 $C$ 是非普适常数。不同约定下修正项可能写在倒数 stiffness 上，但核心是 $1/\ln L$ 修正。

2. **关联函数指数**：

低温相

$$
G(r)\sim r^{-\eta(T)}.
$$

在转变点

$$
\eta=\frac14.
$$

有限尺寸中，结构因子或磁化矩可满足

$$
\langle m^2\rangle
\sim
L^{-\eta}.
$$

在 $T_{\rm BKT}$ 附近应看到 $\eta\simeq1/4$。

3. **vortex 观测量**：

可以测量 vortex density、vortex-antivortex pair 分布、自由 vortex 数目等。低温下 vortex 多以紧束缚对出现；高温下自由 vortex 增多。

4. **data collapse 的修改形式**：

高温侧可用

$$
\frac{L}{\xi(T)}
$$

作为标度变量，其中

$$
\xi(T)
\sim
\exp\left(
\frac{b}{\sqrt{T-T_{\rm BKT}}}
\right).
$$

因此 collapse 变量应改成

$$
L\exp\left[
-\frac{b}{\sqrt{T-T_{\rm BKT}}}
\right].
$$

## 和 Mermin-Wagner 定理的关系

Mermin-Wagner 定理禁止二维短程连续对称性系统在有限温有真正长程序。BKT 相变正是这一限制下出现的新型相变：

- 低温相：无真正磁化，但有代数关联。
- 高温相：关联函数指数衰减。
- 转变机制：vortex-antivortex 从束缚到解束缚。
- RG 图像：vortex fugacity 从 irrelevant 变为 relevant。

所以 BKT 相变没有违反 Mermin-Wagner 定理。它展示的是另一种相变范式：拓扑缺陷的绑定状态取代了 Landau 序参量是否非零，成为区分相结构的核心。

## 小结

BKT 相变可以用三层图像理解。

第一层是物理直觉：低温下角度场平滑，vortex-antivortex 成对束缚；高温下熵促使自由 vortex 增殖。

第二层是能熵竞争：单个 vortex 的自由能为

$$
F_v
=
(\pi\rho_s-2T)\ln(L/a),
$$

由此得到解束缚的粗略条件

$$
T_{\rm BKT}\simeq \frac{\pi\rho_s}{2}.
$$

第三层是 RG 理论：$K$ 和 vortex fugacity $y$ 满足

$$
\frac{dK^{-1}}{dl}=4\pi^3y^2,
\qquad
\frac{dy}{dl}=(2-\pi K)y.
$$

这套 RG 给出低温 fixed line、vortex 解束缚、普适刚度跳跃、$\eta=1/4$ 和关联长度本质奇异性。BKT 相变的特殊性正来自这些结构。
