# Token、Embedding 与 Shape

Transformer 不直接处理原始文本或物理 bitstring，而是先把输入转成离散 token，再把 token 映射成连续向量。

本页只解决一个问题：Transformer 的输入 $X\in\mathbb{R}^{B\times N\times d_{\rm model}}$ 是怎么来的。

```text
原始对象
  -> token id
  -> embedding lookup
  -> [B, N, d_model]
```

## 从对象到 Token

自然语言中，token 可以是子词、字符或词片段。例如：

```text
"Transformer is useful"
  -> [Transformer, is, useful]
  -> [13542, 318, 4465]
```

NNQS 中，token 可以来自 occupation bitstring 的局部分组。例如把每个 spatial orbital 的 $\alpha,\beta$ 占据合成一个 pair token：

| pair | token |
| --- | ---: |
| $00$ | 0 |
| $10$ | 1 |
| $01$ | 2 |
| $11$ | 3 |

这时词表大小就是：

$$
V=4.
$$

## Token ID 张量

设 batch size 为 $B$，序列长度为 $N$。输入 token id 的形状通常是：

$$
T\in\mathbb{N}^{B\times N}.
$$

例如：

```text
T.shape = [B, N]
```

每个元素是一个整数，表示词表中的某个 token。

## Embedding 矩阵

Embedding 层是一张查表矩阵：

$$
E\in\mathbb{R}^{V\times d_{\rm model}}.
$$

第 $t$ 个 token 对应第 $t$ 行向量：

$$
e_t = E[t]\in\mathbb{R}^{d_{\rm model}}.
$$

查表后得到：

$$
X_{\rm tok}\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

这里的 $d_{\rm model}$ 是 Transformer 内部统一使用的隐藏维度。

可以把 embedding 理解为把离散符号放进一个连续向量空间。token id 本身没有大小关系，编号 3 并不比编号 2 “更大”；模型真正使用的是查表后的向量。

## 为什么需要统一维度

一个 Transformer block 内部有 attention、FFN、残差连接和 LayerNorm。残差连接要求输入输出能够相加，所以主干张量通常一直保持同一个形状：

$$
X\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

Attention 和 FFN 可以临时投影到别的维度，但 block 输出还会回到 $d_{\rm model}$。

## Shape 速查

| 对象 | 形状 | 含义 |
| --- | --- | --- |
| token ids | $[B,N]$ | 离散 token 编号 |
| embedding table | $[V,d_{\rm model}]$ | 每个 token 的向量 |
| embedded input | $[B,N,d_{\rm model}]$ | Transformer 主干输入 |
| logits | $[B,N,V]$ | 每个位置对词表的打分 |

## 对 NNQS 的意义

在教学版 NNQS 中，原始输入是 occupation bitstring：

$$
x=[\alpha_0,\beta_0,\alpha_1,\beta_1,\ldots].
$$

它先被转成 pair token 序列：

$$
t=[t_0,t_1,\ldots,t_{L-1}],
\qquad
t_i=\alpha_i+2\beta_i.
$$

之后就可以像语言模型一样，用 Transformer 逐位置建模：

$$
P_\theta(t_i\mid t_{<i}).
$$

这里的 tokenization 不是自然语言分词，而是物理自由度的重新打包：把同一个 spatial orbital 上的 $\alpha,\beta$ 占据合成一个四值 token。
