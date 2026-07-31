# 训练目标与 Mask

Transformer 结构本身只定义了如何计算表示。不同训练目标会决定 mask 方式、标签构造和模型用途。

可以先记住三句话：

- Encoder 训练常常是“看完整输入，学习表征”。
- Decoder 训练是“并行计算，但信息流保持自回归”。
- KV cache 主要属于推理/采样阶段，不属于常规全序列训练。

## Causal Language Modeling

Decoder-only 模型常用 causal language modeling。给定序列：

$$
t_0,t_1,\ldots,t_{N-1},
$$

模型学习：

$$
P(t_0,\ldots,t_{N-1})
=\prod_{i=0}^{N-1}P(t_i\mid t_{<i}).
$$

训练时使用 causal mask，保证第 $i$ 个位置不能看见 $j>i$ 的 token。

如果 logits 的形状是：

$$
\mathrm{logits}\in\mathbb{R}^{B\times N\times V},
$$

那么第 $i$ 个位置通常用来预测第 $i+1$ 个 token：

$$
\mathrm{target}_i=t_{i+1}.
$$

交叉熵损失：

$$
L
=-\sum_i \log P_\theta(t_{i+1}\mid t_{\le i}).
$$

这时所有位置的 logits 可以一次算出来。causal mask 约束的是“每个位置能看见哪些 token”，并不妨碍 GPU 用矩阵乘法并行计算整段序列。

实际训练时，logits、softmax、loss 和梯度还会受到数值精度影响。FP32、BF16、FP16、loss scaling 和量化的背景见 [数值精度](../numerical_precision.md)。

## Masked Language Modeling

Encoder-only 模型常用 masked language modeling。训练时随机遮住部分 token：

```text
原序列:  A B C D E
输入:    A [MASK] C D [MASK]
目标:    B, E
```

模型可以双向看见上下文，因此适合学习表征：

$$
P(t_i\mid t_{\rm visible}).
$$

MLM 常用于预训练 encoder，比如 BERT。

## Seq2Seq 训练

Encoder-decoder 模型用于条件生成。给定源序列 $x$ 和目标序列 $y$：

$$
P(y\mid x)
=\prod_i P(y_i\mid y_{<i},x).
$$

Encoder 对 $x$ 做双向编码；decoder 在生成 $y_i$ 时：

- 用 causal self-attention 读取 $y_{<i}$。
- 用 cross-attention 读取 encoder 输出。

## Teacher Forcing

训练自回归模型时，常用 teacher forcing：模型第 $i$ 步输入真实前缀，而不是输入自己上一步生成的 token。

例如目标序列为：

```text
[BOS, A, B, C, EOS]
```

输入给 decoder：

```text
[BOS, A, B, C]
```

训练目标：

```text
[A, B, C, EOS]
```

这样所有位置可以并行计算损失。

## Padding Mask

batch 内序列长度不同时，会用 padding 补齐：

```text
[A, B, C, PAD, PAD]
[D, E, F, G,   H  ]
```

padding token 不应参与 attention，也不应贡献 loss。因此需要：

- attention 中用 padding mask 屏蔽 PAD。
- loss 中忽略 PAD 位置。

## 推理与 KV Cache

训练时有完整序列，推理时只有当前前缀。生成第 $n$ 个 token 时，模型输入通常是：

```text
[t0, t1, ..., t_{n-1}]
```

如果每一步都重算整个前缀，历史 token 的 key/value 会重复计算。KV cache 缓存每一层历史 token 的 $K,V$：

$$
K_{\rm cache},V_{\rm cache}
\in
\mathbb{R}^{B\times h\times n\times d_h}.
$$

下一步只需要新 token 的：

$$
Q_{\rm new},K_{\rm new},V_{\rm new}
\in
\mathbb{R}^{B\times h\times 1\times d_h}.
$$

然后把 $K_{\rm new},V_{\rm new}$ 接到历史 cache 后面，让新的 query 读取全部历史。详细过程见 [KV Cache](kv_cache.md)。

这也解释了训练和推理的计算方式差别：

| 阶段 | 输入方式 | 是否常用 KV cache |
| --- | --- | --- |
| 训练 | 整段序列并行输入 | 通常不用 |
| 推理/生成 | 一个 token 一个 token 生成 | 常用 |
| NNQS 自回归采样 | 一个 pair token 一个 pair token 采样 | 可选，用于加速 |

## 对 NNQS 的训练差异

NNQS 的 amplitude network 也给出自回归概率：

$$
P_\theta(x)=\prod_i P_\theta(t_i\mid t_{<i}).
$$

但它的训练目标通常不是普通语言模型的交叉熵。VMC 中优化的是能量：

$$
E(\theta)
=
{\langle\psi_\theta|H|\psi_\theta\rangle
\over
\langle\psi_\theta|\psi_\theta\rangle}.
$$

因此 NNQS 使用 Transformer 表示概率分布，却通过 local energy 和变分梯度更新参数。这是它和自然语言模型最大的区别。
