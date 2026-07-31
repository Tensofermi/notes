# 位置信息

Self-attention 本身只看 token 之间的相似度。若不加入位置信息，模型很难区分同一组 token 的不同排列。

本页要回答的问题是：既然 attention 输入是一组向量，模型怎么知道“第几个 token 在哪里”？

## 为什么 Attention 需要位置

Attention 的核心是：

$$
\mathrm{softmax}\left({QK^{\mathsf T}\over\sqrt{d_h}}\right)V.
$$

如果输入只包含 token embedding，attention 看到的是一组向量，而序列顺序不会自然进入公式。对语言来说：

```text
猫 追 狗
狗 追 猫
```

token 集合相同，语义却不同。对 NNQS 来说，不同 orbital 位置也对应不同物理自由度，顺序同样重要。

## 绝对位置编码

最直接的做法是给第 $i$ 个位置一个向量 $p_i$，再与 token embedding 相加：

$$
X_i = e_{t_i}+p_i.
$$

如果 $p_i$ 是可学习参数，则：

$$
P\in\mathbb{R}^{N_{\max}\times d_{\rm model}}.
$$

这种做法简单，常用于固定最大长度的模型。

加入后，Transformer 实际看到的是：

$$
X_i=e_{t_i}+p_i,
$$

其中 $e_{t_i}$ 表示 token 类型，$p_i$ 表示位置。

## 正弦位置编码

原始 Transformer 使用固定正弦位置编码：

$$
p_{i,2k}=\sin\left({i\over 10000^{2k/d_{\rm model}}}\right),
$$

$$
p_{i,2k+1}=\cos\left({i\over 10000^{2k/d_{\rm model}}}\right).
$$

它的特点是无需学习参数，并且不同频率可以表达不同尺度的位置关系。

## 相对位置与 RoPE

现代 decoder-only 模型常用相对位置信息或 RoPE。RoPE 的思想是：把位置信息注入到 query 和 key 中，使得内积 $q_i\cdot k_j$ 可以感知相对距离 $i-j$。

概念上可以理解为：

$$
q_i \to R_i q_i,\qquad
k_j \to R_j k_j,
$$

其中 $R_i$ 是与位置 $i$ 有关的旋转矩阵。这样注意力打分变成：

$$
(R_iq_i)^{\mathsf T}(R_jk_j),
$$

它自然包含相对位置信息。

## 在 NNQS 中的位置

NNQS 的 token 位置通常对应 orbital 顺序。假设原始 bitstring 为：

$$
x=[\alpha_0,\beta_0,\alpha_1,\beta_1,\ldots,\alpha_{L-1},\beta_{L-1}],
$$

每个 spatial orbital 变成一个 pair token：

$$
t_i=\alpha_i+2\beta_i,\qquad i=0,\ldots,L-1.
$$

所以 token 序列：

$$
[t_0,t_1,\ldots,t_{L-1}]
$$

的第 $i$ 个位置就对应第 $i$ 个 spatial orbital。位置编码告诉模型：

- 当前 token 是第几个 spatial orbital。
- 左右 token 在 orbital 排列中的相对位置。
- 某些局域或长程相关可能与 orbital 排序有关。

如果不加位置编码，模型只能知道某个 pair token 是 $0,1,2,3$，却难以知道它属于哪个 orbital。

## NNQS 中的具体实现

教学版最自然的实现是可学习绝对位置编码。代码结构通常是两个 embedding 相加：

```python
token_emb = nn.Embedding(vocab_size, d_model)
pos_emb = nn.Embedding(max_seq_len, d_model)

token_vec = token_emb(tokens)          # [B, L, d_model]
pos_id = torch.arange(L, device=tokens.device)
pos_vec = pos_emb(pos_id)[None, :, :]  # [1, L, d_model]

x = token_vec + pos_vec                # [B, L, d_model]
```

这里：

- `tokens[b, i]` 是第 `b` 个样本中第 $i$ 个 orbital 的 pair token。
- `token_emb(tokens[b, i])` 告诉模型“这个位置的占据类型是什么”。
- `pos_emb(i)` 告诉模型“这个占据类型出现在第几个 orbital”。
- 两者相加后，送入 Transformer block。

如果自回归实现中使用 start token，位置也要和输入序列对齐。例如训练时输入：

```text
[S, t0, t1, ..., t_{L-2}]
```

目标是：

```text
[t0, t1, t2, ..., t_{L-1}]
```

那么位置编号通常是：

```text
[0, 1, 2, ..., L-1]
```

其中位置 0 给 start token，位置 1 用来预测第一个 orbital 的 token，依此类推。也可以让 start token 单独占一个特殊位置，再把 orbital 位置从 0 开始编码；关键是训练和采样阶段必须使用同一套约定。

## 一个小例子

设有 4 个 qubit，也就是 2 个 spatial orbital：

$$
x=[1,0,0,1].
$$

按 $[\alpha_0,\beta_0,\alpha_1,\beta_1]$ 分组：

$$
t_0=1,\qquad t_1=2.
$$

如果没有位置编码，模型只看到 token 值 $1$ 和 $2$。如果把两个 token 交换成 $[2,1]$，模型很难知道这是不同 orbital 上的不同占据排列。

加入位置编码后，模型实际看到的是：

$$
e(t_0)+p_0,\qquad e(t_1)+p_1.
$$

这时 $t_0=1$ 和 $t_1=1$ 虽然 token 类型相同，但表示不同：

$$
e(1)+p_0 \ne e(1)+p_1.
$$

所以模型能够区分“第 0 个 orbital 上是 token 1”和“第 1 个 orbital 上是 token 1”。

## 选择建议

| 方法 | 优点 | 注意点 |
| --- | --- | --- |
| 可学习绝对位置 | 简单，代码直观 | 外推到更长序列较弱 |
| 正弦位置编码 | 无参数，可解释 | 表达能力相对固定 |
| RoPE | 适合 decoder-only，大模型常用 | 实现细节多一些 |
| 相对位置 bias | 直接建模距离 | 需要处理 mask 与长度 |

教学代码若以清晰为主，可先使用可学习绝对位置编码；若后面关心长序列外推，再考虑 RoPE 或相对位置 bias。
