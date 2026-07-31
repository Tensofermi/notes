# Attention 与 Potts 模型视角

这一页提供一个高级类比：把 self-attention 看成学习变量之间相互作用的机制，和 Potts 模型中的耦合结构进行对照。

这不是 Transformer 的基础理解路径。基础公式见 [Attention 机制](attention.md)。

## Potts 模型

Potts 模型中，每个位置 $i$ 有一个离散状态：

$$
s_i\in\{1,\ldots,q\}.
$$

能量可以写成：

$$
E(s)
=
-\sum_{i<j}J_{ij}(s_i,s_j)
-\sum_i h_i(s_i).
$$

其中：

- $J_{ij}$：位置 $i,j$ 之间的相互作用。
- $h_i$：单点偏置。

概率分布为：

$$
P(s)
=
{1\over Z}
\exp[-\beta E(s)].
$$

## Self-attention

Transformer 中，每个 token 位置有 hidden vector：

$$
x_i\in\mathbb{R}^{d_{\rm model}}.
$$

attention score 为：

$$
S_{ij}
=
{q_i\cdot k_j\over\sqrt{d_h}}.
$$

softmax 后得到权重：

$$
A_{ij}
=
{\exp(S_{ij})\over\sum_m\exp(S_{im})}.
$$

输出：

$$
\tilde x_i
=
\sum_j A_{ij}v_j.
$$

## 类比关系

| Potts 模型 | Self-attention |
| --- | --- |
| 离散状态 $s_i$ | token / hidden state $x_i$ |
| 耦合 $J_{ij}$ | attention score $S_{ij}$ |
| Boltzmann 权重 | softmax 权重 |
| 相互作用决定统计关联 | attention 决定信息读取 |

关键相似点是：两者都用成对关系刻画变量之间的依赖。

## 重要差别

这个类比不能过度解释。

Potts 模型的 $J_{ij}$ 通常是显式参数或物理耦合。  
Transformer 的 $S_{ij}$ 是由输入动态生成的：

$$
S_{ij}
=
{(x_iW^Q)(x_jW^K)^{\mathsf T}\over\sqrt{d_h}}.
$$

因此 attention 不是固定耦合，而是 data-dependent interaction。

## 为什么这个视角有用

在物理问题中，我们关心构型变量之间的关联。attention 可以看成一种可学习、输入依赖的关联读取机制。

对 NNQS 来说，这意味着 Transformer 有能力表示：

- 局域关联。
- 长程关联。
- 由当前构型决定的有效相互作用。
- 不同 head 对应的多种关联通道。

## 不展开的部分

更深入的工作会讨论 factored self-attention、样本复杂性和 replica 分析。这些内容依赖更重的统计物理工具，不作为本站基础路线的一部分。

本站采用的用法更实际：

> 把 attention 视为一种学习构型中条件依赖和有效相互作用的模块。

