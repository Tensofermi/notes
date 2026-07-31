# Metropolis 更新

Metropolis 是最基础的局域 MCMC 更新。它的目标是：给定目标权重 $W(s)$，构造一个以 $W(s)$ 为平稳分布的 Markov chain。它通常不需要知道配分函数 $Z$，只需要计算新旧构型的权重比。

一次更新可以分成两步：

1. 从当前构型 $s$ 提出候选构型 $s'$。
2. 按接受率决定是否把 $s$ 替换成 $s'$。

如果 proposal probability 记为 $A(s\to s')$，接受率记为 $P_{\rm acc}(s\to s')$，完整转移概率就是

$$
P(s\to s')
=
A(s\to s')P_{\rm acc}(s\to s').
$$

为了满足 detailed balance，可以选 Metropolis-Hastings 接受率：

$$
P_{\rm acc}(s\to s')
=
\min\left[
1,
\frac{W(s')A(s'\to s)}
{W(s)A(s\to s')}
\right].
$$

若 proposal 对称，

$$
A(s\to s')=A(s'\to s),
$$

接受率化为最常见的形式：

$$
P_{\rm acc}(s\to s')
=
\min\left[
1,
\frac{W(s')}{W(s)}
\right].
$$

这就是 Metropolis 的通用性来源：只要能算出权重比，通常就能写出一个正确的更新。

## Ising 单自旋翻转

以 Ising 模型为例：

$$
H=-J\sum_{\langle ij\rangle}s_is_j-h\sum_i s_i,
\qquad
s_i=\pm1.
$$

最简单的 proposal 是随机选一个格点 $i$，尝试

$$
s_i\to -s_i.
$$

只有与 $i$ 相连的局域能量会改变。设局域场为

$$
h_i^{\rm loc}
=
J\sum_{j\in\partial i}s_j+h,
$$

翻转前后能量差为

$$
\Delta E
=
E(s')-E(s)
=
2s_i h_i^{\rm loc}.
$$

Boltzmann 权重比为

$$
\frac{W(s')}{W(s)}
=
e^{-\beta\Delta E}.
$$

因此对称 proposal 下

$$
P_{\rm acc}
=
\min(1,e^{-\beta\Delta E}).
$$

若 $\Delta E<0$，新构型能量更低，总是接受；若 $\Delta E>0$，仍有概率接受。后者很重要，因为链需要跨过局域能量障碍，才能正确采样整个平衡分布。

## 直接采样的区别

Metropolis 属于 MCMC。它产生的是一条相关构型序列：

$$
s_0,s_1,s_2,\cdots.
$$

直接采样则每次从目标分布中独立产生一个构型。例如普通 percolation 可以对每条边独立掷硬币；简单随机行走可以每一步按固定分布抽方向。这类问题中，样本相关性通常很小。

自旋模型和格点场论更常见的情形是：目标分布只知道未归一化权重 $W(s)$，且直接抽样很困难。Metropolis 用局域权重比绕开了配分函数 $Z$，代价是引入热化时间和自关联时间。

从重要性采样角度看，Metropolis 并不是在构型空间中均匀乱走，而是让 Markov chain 更多停留在 $W(s)$ 大的区域。观测量平均仍然写成

$$
\langle O\rangle
\simeq
\frac1{N_{\rm meas}}\sum_{m=1}^{N_{\rm meas}}O(s_m),
$$

但这些 $s_m$ 不是独立抽出的样本，而是同一条链热化后的访问记录。因此 Metropolis 程序至少要同时记录三类信息：

- 当前构型 $s$ 以及它的能量或局域场。
- 接受、拒绝和测量次数。
- 热化步数、测量间隔和随机种子。

前两类决定算法是否正确和高效，第三类决定结果是否可复现、误差是否可信。

## 局域 proposal 怎么设计

Metropolis 更新的自由度主要在 proposal $A(s\to s')$。接受率只是保证目标分布正确；采样效率很大程度上由 proposal 决定。

一个好的 proposal 通常要满足几件事：

- **容易反向**：能清楚写出 $A(s\to s')$ 和 $A(s'\to s)$，最好二者相等。
- **局域代价低**：能用局域能量差计算权重比，而不是每步重算总能量。
- **遍历性足够**：长期来看能到达目标分布支持上的所有重要构型。
- **步长合适**：既不要几乎每次都被拒绝，也不要每步只做极小扰动。

Ising 单自旋翻转是最简单的对称 proposal：随机选一个格点并翻转它。连续自旋模型则常见两类 proposal。第一类是在当前角度附近加一个小扰动：

$$
\theta_i'=\theta_i+\delta,
\qquad
\delta\sim{\rm Uniform}(-\Delta,\Delta).
$$

第二类是完全重抽一个方向：

$$
\theta_i'\sim{\rm Uniform}(0,2\pi).
$$

前者在低温时接受率通常较高，但移动慢；后者移动幅度大，但低温下容易被拒绝。常见做法是把 $\Delta$ 当作可调参数，在热化前做短暂调节，使接受率落在一个合理区间。这个调节只能用于确定模拟参数；正式测量阶段不应继续根据历史接受率改变 proposal，否则 Markov chain 的平稳性需要重新论证。

对长程相互作用，局域 proposal 仍然可以只翻一个自由度，但能量差可能涉及所有其他格点。此时要么维护局域场以便 $O(1)$ 或低成本更新，要么使用 clock、alias、FFT 等技巧降低一次 sweep 的代价。也就是说，proposal 的形式可以简单，但数据结构必须配合模型相互作用范围。

## Sweep、热化和测量

一次单点 proposal 只尝试改变一个自由度。为了让不同系统尺寸之间的 Markov chain 时间有可比性，常把 $N$ 次单点尝试称为一个 sweep，其中 $N$ 是自由度数。对 $L^d$ 格点模型，

$$
N=L^d.
$$

典型 Markov chain 流程可以写成：

```text
initialize configuration
for sweep in thermalization:
    for step in 1..N:
        metropolis_update()

for sweep in measurement:
    for step in 1..N:
        metropolis_update()
    if sweep % measure_interval == 0:
        measure_observables()
```

热化阶段的样本不进入最终平均。它的作用是让初始构型的影响衰减掉。冷启动、有序初态和随机初态可以作为简单检查：如果热化足够长，它们在同一组参数下的能量、磁化或目标观测量应当收敛到同一区间。

测量间隔也不是越小越好。每个 sweep 都测量可以保留最多信息，但相邻数据高度相关；隔若干 sweep 测量可以减小存储量，却不能替代自关联时间估计。最终误差仍应通过 blocking 或积分自关联时间处理。

## 接受率和拒绝率

接受率是最容易监控的运行指标之一。设总尝试次数为 $N_{\rm try}$，接受次数为 $N_{\rm acc}$，则

$$
r_{\rm acc}
=
\frac{N_{\rm acc}}{N_{\rm try}},
\qquad
r_{\rm rej}=1-r_{\rm acc}.
$$

接受率太低，说明 proposal 经常提出权重极小的构型，链长时间停在原地；接受率太高也不一定好，可能意味着每次移动太小，构型在空间中缓慢扩散。对连续变量的局域 Metropolis，常通过调节步长 $\Delta$ 在两者之间折中。对离散模型，proposal 往往没有连续步长可调，这时更重要的是混入 cluster、worm 或其他非局域更新。

拒绝并不是错误。相反，拒绝更新对应转移概率中的 $P(s\to s)$，它既参与概率归一化，也常帮助打破周期性。程序中一个常见错误是“被拒绝时不记录样本”。正确做法是：如果到了测量时刻，无论上一轮 proposal 是否接受，都从当前构型测量。被拒绝意味着当前构型在 Markov chain 中重复出现一次，它本来就应该带权计入时间平均。

## 正确性检查点

实现 Metropolis 更新时，可以把正确性检查拆成几层。

第一层是局域能量差。随机挑选若干次更新，比较“局域公式给出的 $\Delta E$”和“重算总能量后的差值”。这能抓出边界条件、邻接表和符号错误。

第二层是 detailed balance 的权重比。对小系统可以枚举构型，直接检查

$$
W(s)P(s\to s')
=
W(s')P(s'\to s)
$$

是否成立。实际大系统不能枚举，但小系统测试很有价值。

第三层是已知极限。高温极限下，许多模型接近独立随机变量；低温极限下，能量和序参量有明确趋势；小尺寸系统还可以和精确枚举结果比较。

第四层是统计诊断。不同 seed、不同初态、不同热化长度和不同测量间隔应给出相容结果；blocking 误差应出现平台。若平均值随热化长度漂移，优先怀疑没有热化；若误差随 block size 持续上升，说明链长度可能不足或自关联时间太长。

## Heat Bath

heat bath 是另一种局域更新。它不先提出一个候选值再接受或拒绝，而是固定其他自由度后，直接从局域条件分布中重抽：

$$
P(s_i|\{s_{j\ne i}\})
=
\frac{W(s_i,\{s_{j\ne i}\})}
{\sum_{s_i'}W(s_i',\{s_{j\ne i}\})}.
$$

对 Ising 模型，固定邻居后

$$
P(s_i=+1|\{s_{j\ne i}\})
=
\frac{e^{\beta h_i^{\rm loc}}}
{e^{\beta h_i^{\rm loc}}+e^{-\beta h_i^{\rm loc}}}
=
\frac{1+\tanh(\beta h_i^{\rm loc})}{2}.
$$

heat bath 的局域变量总是被接受，所以拒绝率为零。但它仍然是局域更新，在临界点附近同样可能出现大尺度模式移动缓慢的问题。

## 优点和代价

Metropolis 的优点：

- 实现简单，只需要局域能量差或权重比。
- 适用范围很广，连续变量、离散变量、带约束模型都可以先尝试。
- 很适合作为复杂算法的校验基线。

Metropolis 的代价：

- 样本是 Markov chain 上的关联样本，需要估计自关联时间。
- 临界点附近容易出现临界慢化。
- proposal 若设计得不好，可能接受率很低，或者在构型空间中移动很慢。

因此实际研究中常把 Metropolis 当作基础工具：先用它建立正确性，再根据模型结构发展 cluster、worm、loop、SSE、辅助场或张量网络采样来提高效率。
