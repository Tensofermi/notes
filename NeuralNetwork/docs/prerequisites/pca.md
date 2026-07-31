# PCA：从协方差到主成分

PCA 是 Principal Component Analysis，主成分分析。它是一种线性降维方法。

目标是：在尽量保留数据主要变化方向的前提下，把高维数据投影到低维空间。

## 数据矩阵

设有 $n$ 个样本，每个样本 $p$ 个特征：

$$
X\in\mathbb{R}^{n\times p}.
$$

第 $i$ 行是一个样本：

$$
x_i\in\mathbb{R}^p.
$$

PCA 首先对每个特征中心化：

$$
\tilde X=X-\mu,
$$

其中 $\mu$ 是特征均值。

## 协方差矩阵

中心化后，协方差矩阵为：

$$
C
=
{1\over n-1}\tilde X^{\mathsf T}\tilde X.
$$

它的形状是：

$$
C\in\mathbb{R}^{p\times p}.
$$

$C_{ab}$ 表示第 $a$ 个特征和第 $b$ 个特征如何共同变化。

## 主成分

PCA 寻找方向 $w$，使投影后的方差最大：

$$
\max_{\|w\|=1}
\mathrm{Var}(\tilde Xw).
$$

这个目标等价于：

$$
\max_{\|w\|=1}
w^{\mathsf T}Cw.
$$

解是协方差矩阵最大特征值对应的特征向量：

$$
Cw=\lambda w.
$$

特征值越大，说明该方向上的方差越大。

## 降维步骤

PCA 的流程：

1. 数据中心化。
2. 计算协方差矩阵。
3. 求特征值和特征向量。
4. 按特征值从大到小排序。
5. 取前 $k$ 个特征向量组成投影矩阵 $W_k$。
6. 得到低维表示：

$$
Z=\tilde X W_k.
$$

其中：

$$
Z\in\mathbb{R}^{n\times k}.
$$

## 方差解释率

第 $i$ 个主成分解释的方差比例为：

$$
{\lambda_i\over\sum_j\lambda_j}.
$$

前 $k$ 个主成分累计解释率为：

$$
{\sum_{i=1}^k\lambda_i\over\sum_j\lambda_j}.
$$

这个值可以帮助选择降到几维。

## NumPy 示例

```python
import numpy as np

X = np.array([
    [2.5, 2.4],
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
])

X_centered = X - X.mean(axis=0, keepdims=True)
C = np.cov(X_centered, rowvar=False)

eigvals, eigvecs = np.linalg.eigh(C)
order = np.argsort(eigvals)[::-1]
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]

W = eigvecs[:, :1]
Z = X_centered @ W

print(Z)
```

## 和神经网络的关系

PCA 是线性表示学习。它只能找线性投影方向。

神经网络可以看成非线性表示学习：

$$
z=f_\theta(x).
$$

如果任务结构主要是线性的，PCA 可能已经很有效。如果数据结构高度非线性，神经网络通常更灵活。

在物理构型分析中，PCA 常作为基线方法。CNN 或 Transformer 则可以学习更复杂的局域结构和长程依赖。

## 招聘考点

!!! question "代表题：PCA 为什么要先中心化？"
    PCA 寻找的是样本相对均值的最大方差方向。若不先减去均值，主成分可能被整体偏移主导，而不是反映真实的变化方向。中心化后协方差矩阵为 $C={1\over n-1}X_c^{\mathsf T}X_c$，最大特征值对应的特征向量就是第一主成分。完整题解见 [数学、概率与线性代数题](../interview/math_probability.md)。
