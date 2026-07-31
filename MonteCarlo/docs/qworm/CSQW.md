
# 连续空间的世界线 Worm 算法

连续时间世界线方法把虚时方向连续化，而空间坐标仍固定在离散格点上，适合处理晶格相互作用模型。
对于 $^4{\rm He}$ 气体超流转变温度这类连续空间问题，空间坐标不能被过度离散化。常见做法是保留足够细的虚时离散，使其不影响目标物理量，同时把每个世界面的空间坐标视为连续变量。

相比于晶格上的哈密顿量，连续空间的哈密顿量仍然可以分为对角项 $\hat{H}_0$ 和非对角项 $\hat{V}$ :

$$
\hat{H} = \hat{H}_0 + \hat{V}
$$

$$
\hat{H_0} = \sum_{i<j} U(\vec{r}_{i,j}), \quad
\hat{V} = - \sum_i \lambda_i \nabla_i^2
$$

其中非对角项 $\hat{V}$ 当中 $\lambda_i = {\hbar^2}/{2m_i}$ 与不同粒子的质量相关，描述了动能项。对角项 $\hat{H}_0$ 则描述了不同粒子之间的相互作用。

## 配分函数空间

配分函数空间 $\mathcal Z$ 由闭合世界线构型组成。

连续空间体系的配分函数仍可写成世界线构型求和：

$$
\mathcal{Z} = \sum_{\lbrace \alpha^{(i)} \rbrace} \prod_{i=0}^{N-1} \langle \alpha^{(i+1)} | e^{-\tau \hat{H}} | \alpha^{(i)} \rangle
=\sum_{\lbrace \alpha^{(i)} \rbrace}  W(\lbrace \alpha^{(i)} \rbrace)
$$

其中基矢量 $\alpha$ 由各个粒子的空间位置组成，
对配分函数其中的一个重复单元，利用 Trotter 分解有:

$$
\langle \alpha^{(i+1)} |e^{-\tau \hat{H}} | \alpha^{(i)} \rangle  \approx 
e^{-\tau H_0} \langle \alpha^{(i+1)} | e^{-\tau \hat{V}}| \alpha^{(i)}\rangle 
$$

与格点连续时间算法不同，连续空间中的动能传播子可以显式写出。利用矩阵的直积公式：

$$
(\textbf{A}_1 \otimes \textbf{B}_1) (\textbf{A}_2 \otimes \textbf{B}_2) = 
(\textbf{A}_1 \textbf{A}_2) \otimes (\textbf{B}_1 \textbf{B}_2)
$$

再根据定义 $| \alpha^{(i)}\rangle = \bigotimes_{j}^{N_p} | \alpha^{(i)}_j\rangle$，将多个粒子的动能拆成单个粒子的乘积：

$$
 \langle \alpha^{(i+1)} | e^{-\tau \hat{V}}| \alpha^{(i)}\rangle = 
 \prod_j^{N_p} \langle \alpha^{(i+1)}_j | e^{-\tau \hat{V}}| \alpha^{(i)}_j\rangle
$$

其中 $N_p$ 是粒子数，下标 $j$ 标记粒子，上标 $(i)$ 标记世界面。基矢量 $|\alpha^{(i)}\rangle$ 被拆成各粒子位置态的直积。单粒子动能传播子不会像格点 hopping 矩阵元那样只允许少数相邻态；下一世界面中的位置可以连续变化，权重由相邻世界面上的坐标差决定：

$$ 
\langle \alpha^{(i+1)}_j | e^{-\tau \hat{V}}| \alpha^{(i)}_j\rangle
 = \left(\frac{1}{4 \pi \lambda_j \tau} \right)^{d/2} \exp{\left( - \frac{(\vec{r}_j^{(i+1)} - \vec{r}_j^{(i)})^2}{4\lambda_j \tau} \right)}
$$

其中 $d$ 是空间维数。上式也称为自由粒子密度矩阵，记为 $\rho_0(\vec r_j^{(i)},\vec r_j^{(i+1)},\tau)$。因此配分函数空间权重可写为：

$$
W(\lbrace \alpha^{(i)} \rbrace) \approx \sum_{\lbrace \alpha^{(i)} \rbrace} \prod_{i=0}^{N-1}  \langle \alpha^{(i+1)} | e^{-\tau \hat{V}}| \alpha^{(i)}\rangle \exp \left({-\sum_{i=0}^{N-1} H_0^{(i)} \tau} \right)
$$

由于空间坐标连续，相邻世界面的粒子坐标几乎总是不同，连续空间路径不再按离散 kink 数分类。动能传播子沿整个虚时方向连续贡献权重，对角相互作用则以势能作用量进入。

## 格林函数空间

格林函数空间 $\mathcal G$ 由带两个开放端点的世界线构型组成。

为了进行 worm 更新，引入产生、湮灭场算符并定义松原格林函数：

$$
G(I,M,\tau_I,\tau_M)
=
\left\langle
\hat{b}_I(\tau_I)\hat{b}^\dagger_M(\tau_M)
\right\rangle
=
\frac{g(I,M,\tau_I,\tau_M)}{\mathcal{Z}}.
$$

其中

$$
g(I,M,\tau_I,\tau_M)
=
{\rm Tr}\left[
\mathcal{T}
\hat{b}_I(\tau_I)
\hat{b}^\dagger_M(\tau_M)
e^{-\beta\hat{H}}
\right].
$$

这里 $I,M$ 表示 worm 两端所在的空间位置或粒子坐标，$\tau_I,\tau_M$ 表示两端所在的虚时。格林函数空间的配分函数就是对两端所有可能时空位置求和：

$$
\mathcal{G}
=
\int d\vec r_I d\vec r_M
\int_0^\beta d\tau_I
\int_0^\beta d\tau_M\,
g(I,M,\tau_I,\tau_M)
=
\sum_{\mathcal C\in\mathcal G}W_{\mathcal G}(\mathcal C).
$$

因此 Worm 算法实际抽样的是扩展空间

$$
\mathcal{Z}_w = \mathcal{Z} + \omega_G \mathcal{G}
$$

其中 $\omega_G$ 用来调节配分函数空间和格林函数空间的相对访问频率。


连续空间中两个粒子严格处于同一位置的概率为零；在常用坐标表象下，端点算符不会像软核格点玻色子那样额外带来可变的 $\sqrt{n_I(n_M+1)}$ 占据数因子。

因此 $W_{\mathcal G}$ 与 $W$ 的主要差别来自端点积分测度 $\tau^2 d\vec r_I d\vec r_M$，以及开放或闭合世界线时被移除、补回的自由传播子 $\rho_0$。

这一点和格点连续时间算法不同。格点算法中的非对角事件是离散 kink，worm 端点通常可以避开同一虚时时刻的 kink；连续空间算法的动能传播子却在每一段虚时上都存在。开放端点会切断或补回某段自由传播子，因此格林函数空间权重必须显式处理相应的 $\rho_0$ 因子。


## 常见体系

$$    
\hat{H} = -\frac{1}{2}\sum_{i=1}^N \nabla_i^2
+ \frac{1}{2} \sum_{i=1}^N \frac{z_i^2}{\xi^4} + 
\sum_{i<j} \left\lbrace  V_{\rm{dd}}(r_{ij}) + \left(\frac{\sigma}{r_{ij}}\right)^{12} \right\rbrace
$$

## 构型的更新

连续空间 Worm 算法的更新仍然在

$$
\mathcal{Z}_w=\mathcal{Z}+\omega_G\mathcal{G}
$$

中进行。与连续时间格点模型不同，这里每个世界面上的粒子坐标都是连续变量，相邻世界面之间的传播子

$$
\rho_0(\vec r,\vec r',\tau)
$$

本身就是权重的重要组成部分。因此更新不只是移动虚时位置，还要改变粒子坐标、开放或闭合世界线、增减粒子段，并处理交换置换。

各更新的接受率统一来自

$$
P_{\rm acc}(\nu\to\nu')
=
\min\left[
1,
\frac{W(\nu')A(\nu'\to\nu)}
{W(\nu)A(\nu\to\nu')}
\right]
$$

给出；如果构型处于格林函数空间，还需要包含 $\omega_G$、worm 端点积分测度和相应的 proposal 概率。

### Wiggle/Displace

`Wiggle` 和 `Displace` 都在配分函数空间 $\mathcal Z$ 中更新闭合世界线，不改变粒子数，也不引入 worm 端点。

`Wiggle` 通常选择某条世界线的一段连续虚时区间，固定两端坐标，只重新抽样中间若干世界面的粒子坐标。它的目的类似于连续时间算法中的局域片段移动：在不改变拓扑结构的情况下，让路径在空间中充分松弛。由于动能传播子是高斯形式，proposal 常参考自由粒子 Brownian bridge，使动能权重尽量被 proposal 吸收，接受率主要由相互作用能变化决定。

`Displace` 则把整条世界线或一段路径整体平移：

$$
\vec r_i^{(k)}\to \vec r_i^{(k)}+\Delta\vec r.
$$

它改变的是粒子在盒子中的整体位置，而不是路径形状。若采用周期边界，需要把坐标重新映射回模拟盒。该更新对液体、气体和弱束缚体系很有用，可以避免世界线质心移动过慢。

这两类更新对应连续时间算法中“移动已有片段”的思想，但连续空间中移动的是坐标轨迹，而不是晶格上的占据数片段。

### Open/Close

`Open` 和 `Close` 负责在配分函数空间 $\mathcal Z$ 与格林函数空间 $\mathcal G$ 之间切换。

`Open` 从一条闭合世界线中选取一个虚时片段，将其切开，形成两个 worm 端点。切开后，中间被移除或改写的传播子不再作为闭合路径的一部分，而是进入格林函数空间的权重。两个端点可以理解为连续空间版本的产生、湮灭算符位置。

`Close` 是反向操作：当两个 worm 端点属于可闭合的同一条开放世界线时，尝试重新连接它们，恢复闭合路径并回到 $\mathcal Z$ 空间。

接受率中需要比较：

- 闭合路径权重与开放路径权重；
- 被删除或补回的自由传播子 $\rho_0$；
- 相互作用能积分的变化；
- 选择世界线、选择虚时区间、选择新坐标路径的 proposal 概率；
- $\mathcal G$ 空间相对权重 $\omega_G$。

在结构上，它对应连续时间算法里的 `Create/Delete Worm`，但连续空间中还要处理端点之间路径坐标的连续抽样。

### Insert/Remove

`Insert` 和 `Remove` 用于在格林函数空间中增减一条完整开放世界线段，通常与 grand-canonical ensemble 中粒子数涨落有关。

`Insert` 尝试在某个虚时区间插入一段新的开放路径。proposal 需要选择起止虚时、端点坐标，并根据自由传播子或 Brownian bridge 生成中间坐标。新路径带来动能传播子、相互作用能和化学势项的变化。

`Remove` 是反向操作：选择已有开放路径段并删除。若删除后构型满足目标空间的约束，则按反向权重比接受。

这类更新的作用类似连续时间算法中创建或删除一段 segment，但连续空间中 segment 不再只是占据数常数片段，而是一条带有空间坐标轨迹的路径。

接受率必须包含插入路径的积分测度。实现时最容易出错的地方，是 proposal 中坐标采样密度与权重中的自由传播子是否一致；若两者设计得好，许多高斯传播子因子可以在比值中抵消。

### Advance/Recede

`Advance` 和 `Recede` 在格林函数空间 $\mathcal G$ 中移动 worm 端点的虚时位置，从而改变开放世界线的长度。

`Advance` 让某个 worm 端点沿虚时方向前进一段距离，并为新增长的路径段生成空间坐标。新增部分的权重来自自由传播子、相互作用能以及可能的化学势项。

`Recede` 则让端点后退，删除一段已有路径。它是 `Advance` 的反向过程。

这对应连续时间算法中 worm head 在虚时方向的 `Shift Worm`，但连续空间中端点移动不仅改变时间长度，也引入或删除一段连续坐标路径。因此 proposal 通常需要同时抽样时间长度和空间轨迹。

接受率中应检查：

- 新增或删除路径段的传播子权重；
- 对角相互作用能积分的变化；
- 端点时间长度 proposal 的正反向概率；
- 空间路径 proposal 的正反向概率；
- 周期虚时边界下是否跨过 $\beta$。

如果端点移动跨过其他粒子世界线或周期边界，构型的置换结构也可能改变，需要与 `Swap` 更新配合。

### Swap

`Swap` 用于处理相同粒子的置换。对于玻色体系，配分函数需要对所有粒子置换求和；在路径积分表示中，这对应世界线可以在虚时周期边界处互相连接，形成交换环。

局域坐标更新通常很难改变置换拓扑。`Swap` 的作用是让 worm 端点尝试接到另一条世界线上，从而改变开放路径与闭合路径的连接关系。若最终闭合，构型可能形成不同长度的 permutation cycle。

可以把它理解为连续空间版本的“worm 在空间方向移动”：连续时间格点 Worm 中，worm head 通过创建或删除 kink 从一个格点移动到相邻格点；连续空间中没有固定格点，worm 端点通过选择附近粒子的世界线并重连路径来改变粒子标签和置换结构。

接受率需要比较重连前后的传播子、相互作用能、选择目标世界线的概率，以及生成连接路径的 proposal 概率。对玻色体系，长交换环与超流响应密切相关，因此 `Swap` 是否高效会直接影响低温超流模拟的采样质量。

## 连续空间 worm 的更新流程

连续空间 worm 模拟通常按 block 和 pass 组织。一次 pass 由若干更新 move 组成，直到构型回到配分函数空间并达到最低更新次数后，再测量对角观测量。主循环可以概括为：

```text
for each block:
    for each pass:
        do:
            choose closed-worldline move or open-worm move
            update one-body density-matrix histogram if possible
        while move count is too small or worm is still open
        shift imaginary-time origin
        measure diagonal observables
    write partial results
```

其中一个关键细节是：对角量测量前，构型必须回到 $\mathcal Z$ 空间；$\mathcal G$ 空间主要用于更新开放世界线并测量一体密度矩阵。

连续空间 worm 的 move 可以按物理作用分成几类：

| 更新类型 | 所在空间 | 作用 |
| --- | --- | --- |
| 路径形变 | $\mathcal Z$ | 选择一段闭合路径，固定端点，用 Brownian-bridge 形式重采样中间 bead |
| 整体平移 | $\mathcal Z$ | 对未缠结的闭合世界线做整体空间平移 |
| 开放端点前进 | $\mathcal G$ | 增长开放路径，生成新 bead，并逐层比较传播子和相互作用权重 |
| 开放端点后退 | $\mathcal G$ | 删除开放路径的一段，是前进更新的反向过程 |
| 闭合 worm | $\mathcal G\to\mathcal Z$ | 尝试用自由传播子端点检验和路径重采样闭合开放世界线 |
| 置换重连 | $\mathcal G$ | 选择另一条世界线并重连，改变置换结构 |
| 一体密度矩阵测量 | $\mathcal G$ | 在只有一个 worm 打开时累积端点间距和虚时差的统计 |
| 置换环统计 | $\mathcal Z$ | 在闭合构型中统计 permutation cycle 分布 |

多组分体系还需要记录每个组分的统计类型、动能系数、粒子数和进入 $\mathcal G$ 空间的相对权重。统计类型决定是否允许 Bose/Fermi/Boltzmann 置换结构；动能系数控制自由传播子的扩散尺度；opening weight 控制开放 worm 空间的访问频率。

连续空间 worm 的难点不在于 move 种类的数量，而在于每个 move 都要同时维护三类信息：

1. 每条世界线在各虚时层上的连续空间坐标；
2. 相互作用势能、力或高阶作用量修正所需的缓存量；
3. 置换连接、开放端点和当前 worm 所属组分。

因此，接受检验通常不能只比较端点传播子，还要把新路径和其他活跃粒子的相互作用变化纳入权重比。若采用四阶作用量，力平方修正项也会随路径更新一起变化。

## 参数检查

连续空间 worm 的参数通常分阶段确定。

第一，先在配分函数空间做短预热，调节路径形变、整体平移和 opening weight 等参数，使主要更新有可用的接受率。

第二，在格林函数空间检查开放端点的访问频率、置换重连尝试次数和端点距离分布。如果 $\mathcal G$ 空间访问太少，一体密度矩阵和长交换环统计都会很差；如果访问太多，对角观测量的有效测量次数会下降。

第三，对固定温度 $T$ 增加虚时层数 $N$，检查能量、超流刚度或其他目标观测量是否在误差棒内收敛。确定可用的 $\tau=\beta/N$ 后，同一作用量近似下的其他温度点应保持相同的虚时步长量级。

第四，只要相互作用强度、密度、温度范围或 trial move 尺度发生明显变化，就需要重新检查接受率、Trotter 收敛和热化长度。
