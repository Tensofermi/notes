# 数学、概率与线性代数题

这类题通常不直接考很深的数学，而是考你能否把机器学习中的矩阵、概率和优化说清楚。华为、字节的 AI / 算法岗位尤其常见。

## 题目：PCA 为什么要对数据中心化？

**来源背景**：华为 / 字节公开面经中 PCA、协方差矩阵、降维考点改写。

**考点定位**：协方差、特征值分解、主成分方向。

**先给结论**：PCA 要找的是数据相对均值的变化方向，因此应先减去均值。如果不中心化，第一主成分可能被样本均值偏移主导，而不是被真实方差方向主导。

**解题思路**：

给定数据矩阵：

$$
X\in\mathbb{R}^{n\times d}.
$$

中心化后：

$$
X_c=X-\mathbf{1}\mu^{\mathsf T},
\qquad
\mu={1\over n}\sum_{i=1}^n x_i.
$$

PCA 使用协方差矩阵：

$$
C={1\over n-1}X_c^{\mathsf T}X_c.
$$

主成分是 $C$ 最大特征值对应的特征向量。这个方向表示投影后方差最大。

**公式推导 / 代码实现**：

若投影方向为单位向量 $w$，投影方差为：

$$
\mathrm{Var}(X_cw)=w^{\mathsf T}Cw.
$$

最大化：

$$
\max_{\|w\|=1}w^{\mathsf T}Cw
$$

会得到最大特征值对应的特征向量。

**易错点**：

- PCA 不是用原始 $X^{\mathsf T}X$ 直接做特征分解，而是用中心化后的协方差。
- PCA 是无监督线性降维，不使用标签。
- 特征值越大，解释方差越大。

**关联阅读**：[PCA：从协方差到主成分](../prerequisites/pca.md)。

## 题目：标准化后变量的均值和方差是多少？

**来源背景**：机器学习笔试中数据预处理考点改写。

**考点定位**：均值、方差、标准化、数值尺度。

**先给结论**：若：

$$
z={x-\mu\over\sigma},
$$

则 $z$ 的均值为 0，方差为 1。

**解题思路**：

期望：

$$
\mathbb E[z]
=
{\mathbb E[x]-\mu\over\sigma}
=0.
$$

方差：

$$
\mathrm{Var}(z)
=
\mathrm{Var}\left({x-\mu\over\sigma}\right)
=
{1\over\sigma^2}\mathrm{Var}(x)
=1.
$$

**易错点**：

- 减均值改变均值，不改变方差。
- 除以标准差会把方差缩放为 1。
- 如果 $\sigma=0$，需要加 $\epsilon$ 或直接删除常数特征。

**关联阅读**：[LayerNorm 相关解释](../Transformer/decoder.md#layernorm)。

## 题目：给定两个矩阵相乘，如何判断输出 shape？

**来源背景**：AI 笔试和 PyTorch 面试中 shape 推理考点改写。

**考点定位**：矩阵乘法、batch matrix multiplication、Transformer shape。

**先给结论**：最后一维和倒数第二维对齐，剩余维度按 batch 维广播或保留。

**解题思路**：

普通矩阵乘法：

$$
A\in\mathbb{R}^{m\times k},
\quad
B\in\mathbb{R}^{k\times n},
\quad
AB\in\mathbb{R}^{m\times n}.
$$

在 attention 中：

$$
Q,K\in\mathbb{R}^{B\times h\times N\times d_h}.
$$

则：

$$
QK^{\mathsf T}
\in
\mathbb{R}^{B\times h\times N\times N}.
$$

**易错点**：

- $K$ 要转置最后两个维度，不是转置所有维度。
- attention score 的两个 $N$ 分别表示 query 位置和 key 位置。
- 多头维度 $h$ 是 batch-like 维度，不参与点积。

**关联阅读**：[Attention 机制](../Transformer/attention.md)。

## 题目：伪逆什么时候有用？

**来源背景**：线性回归、最小二乘和数值优化考点改写。

**考点定位**：最小二乘、不可逆矩阵、欠定 / 超定系统。

**先给结论**：当 $X^{\mathsf T}X$ 不可逆或病态时，可以用 Moore-Penrose 伪逆求最小二乘解。

**解题思路**：

线性最小二乘：

$$
\min_w\|Xw-y\|_2^2.
$$

正规方程为：

$$
X^{\mathsf T}Xw=X^{\mathsf T}y.
$$

如果 $X^{\mathsf T}X$ 可逆：

$$
w=(X^{\mathsf T}X)^{-1}X^{\mathsf T}y.
$$

更稳定的写法是：

$$
w=X^+y.
$$

其中 $X^+$ 是伪逆。

**易错点**：

- 实际数值计算中不推荐显式求逆。
- 伪逆可以给出最小范数解，但不代表泛化一定好。
- 病态矩阵常需要正则化。

**关联阅读**：[优化方法](../prerequisites/optimization_methods.md)。

## 题目：交叉熵为什么常用于分类？

**来源背景**：华为 / 字节 ML 基础题改写。

**考点定位**：概率模型、负对数似然、softmax。

**先给结论**：分类模型输出类别概率，交叉熵等价于最大化正确类别的似然；最小化交叉熵就是让模型给真实类别更高概率。

**解题思路**：

真实类别为 $y$，模型给出的概率为：

$$
p_\theta(y\mid x).
$$

单样本负对数似然：

$$
L=-\log p_\theta(y\mid x).
$$

这就是 one-hot 标签下的交叉熵。

**易错点**：

- PyTorch `CrossEntropyLoss` 输入是 logits，不是 softmax 后概率。
- 多分类交叉熵和二分类 BCE 形式不同。
- loss 小不代表置信度校准一定好。

**关联阅读**：[信息熵、交叉熵与 KL 散度](../prerequisites/entropy_cross_entropy_kl.md)。

## 题目：条件概率链式法则如何推出自回归模型？

**来源背景**：语言模型、NNQS 自回归建模考点改写。

**考点定位**：条件概率、链式法则、next-token prediction。

**先给结论**：任意联合分布都可以写成一串条件概率的乘积，自回归模型就是用神经网络逐项建模这些条件概率。

**解题思路**：

对序列 $t_1,\ldots,t_N$：

$$
P(t_1,\ldots,t_N)
=
\prod_{i=1}^N P(t_i\mid t_{<i}).
$$

语言模型学习：

$$
P_\theta(t_i\mid t_{<i}).
$$

NNQS 中也可以把构型拆成 token，并建模：

$$
p_\theta(x)=\prod_iP_\theta(t_i\mid t_{<i}).
$$

**易错点**：

- 链式法则总是成立；模型近似的是每个条件概率。
- causal mask 是结构约束，保证不能看未来。
- NNQS 中 $p_\theta(x)=|\psi_\theta(x)|^2$，振幅还要取平方根关系。

**关联阅读**：[自回归、贝叶斯递推与语言模型](../Transformer/autoregressive_probability.md)。

## 题目：首次出现连续两个正面的期望抛硬币次数是多少？

**来源背景**：概率期望类笔试题改写。

**考点定位**：状态递推、期望方程、马尔可夫状态。

**先给结论**：期望次数是 6。

**解题思路**：

设：

- $E_0$：当前没有连续前缀。
- $E_1$：刚刚抛出一个正面 H。

从 $E_0$ 出发：

$$
E_0=1+{1\over2}E_1+{1\over2}E_0.
$$

从 $E_1$ 出发：

$$
E_1=1+{1\over2}\cdot0+{1\over2}E_0.
$$

解得：

$$
E_0=6.
$$

**易错点**：

- 抛出 T 后状态回到 $E_0$，不是简单从头“扣掉一次”。
- 这类题要先定义状态，再写期望方程。

**关联阅读**：[概率分布、熵与配分函数](../prerequisites/probability_entropy_partition.md)。

## 题目：向量检索库中一亿个 768 维 FP32 向量大约占多少内存？

**来源背景**：华为 / 字节向量检索和大模型工程估算题改写。

**考点定位**：显存 / 内存估算、GB 与 GiB、dtype。

**先给结论**：

一亿个 768 维 FP32 向量需要：

$$
10^8\times768\times4
=307.2\times10^9\text{ bytes}
\approx307.2\text{ GB}
\approx286.1\text{ GiB}.
$$

**解题思路**：

FP32 每个数 4 bytes。总元素数：

$$
10^8\times768.
$$

总字节数除以 $10^9$ 是 GB，除以 $2^{30}$ 是 GiB。

**易错点**：

- 硬盘厂商和系统显示可能使用不同单位。
- 真实检索系统还需要索引结构、元数据、缓存，不只是原始向量。
- 如果用 FP16，原始向量大小约减半。

**关联阅读**：[数值精度](../numerical_precision.md)。

