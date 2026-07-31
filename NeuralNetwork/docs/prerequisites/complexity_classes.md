# 计算复杂度速览

计算复杂度研究问题随输入规模增长时需要多少资源。资源通常包括时间和空间。

神经网络笔记中不需要完整复杂度理论，但理解几个类别有助于判断：

- 为什么精确求解量子 many-body 问题困难。
- 为什么采样和近似方法重要。
- 为什么量子计算复杂度类和经典复杂度类不同。

## P

P 是 deterministic polynomial time。

如果一个问题可以由确定性算法在多项式时间内解决：

$$
O(n^k),
$$

则它属于 P。

直觉：P 中的问题通常被认为是经典计算上可有效求解的。

## NP

NP 是 nondeterministic polynomial time。

等价说法：如果给定一个候选解，可以在多项式时间内验证它是否正确，则问题属于 NP。

典型例子是 SAT。给定一个布尔赋值，可以快速验证公式是否满足。

## NP-complete 与 NP-hard

NP-complete 问题满足：

1. 它属于 NP。
2. 所有 NP 问题都可以多项式归约到它。

NP-hard 则不要求问题本身属于 NP，只要求它至少和 NP 中最难问题一样难。

## #P

#P 是计数复杂度类。它不只问“是否存在解”，而是问“有多少个解”。

例如：

```text
SAT: 是否存在满足赋值？
#SAT: 满足赋值有多少个？
```

计数问题通常比判定问题更难。

统计物理配分函数常常具有计数味道：

$$
Z=\sum_x e^{-\beta E(x)}.
$$

它需要对指数多状态求和，所以精确计算通常困难。

## BPP

BPP 是 bounded-error probabilistic polynomial time。

它允许随机算法，只要求错误概率有界。例如错误概率小于 $1/3$，并且可以通过重复运行降低。

Monte Carlo 方法通常属于这种随机近似思想。

## BQP

BQP 是 bounded-error quantum polynomial time。

它描述量子计算机可以在多项式时间内以有界错误概率解决的问题。

Shor 分解算法说明某些问题在量子计算机上可能比已知经典算法快得多。

## QMA

QMA 是 Quantum Merlin-Arthur。

可以粗略理解为 NP 的量子版本：证明者给出一个量子态作为证据，验证者用量子多项式时间验证。

局域 Hamiltonian 问题是 QMA-complete 的典型例子。这和量子 many-body 基态问题的困难性直接相关。

## PSPACE 和 EXP

PSPACE 包含可用多项式空间解决的问题。  
EXP 包含可用指数时间解决的问题。

一般认为：

$$
P\subseteq NP\subseteq PSPACE\subseteq EXP,
$$

但很多包含关系是否严格仍是开放问题。

## 和 NNQS 的关系

电子结构和量子 many-body 问题的 Hilbert space 维度通常指数增长：

$$
\dim\mathcal H\sim 2^N.
$$

这使得完整存储波函数向量不可行。NNQS 的目标不是改变问题的最坏情况复杂度，而是寻找一个可训练的压缩表示：

$$
x\mapsto\psi_\theta(x).
$$

实际成功依赖物理结构：局域性、对称性、低能态纠缠结构、可采样性，以及优化是否能找到好参数。

