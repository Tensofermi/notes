# KV Cache

KV cache 是 decoder-only Transformer 推理时最重要的工程技巧之一。它解决的问题很朴素：自回归生成时，前缀 token 已经算过了，下一步没有必要把整个前缀重新算一遍。

## 先看没有 Cache 的情况

设当前已经生成了 $n$ 个 token：

```text
[t0, t1, ..., t_{n-1}]
```

为了预测下一个 token，decoder 会计算整段前缀的：

$$
Q,K,V\in\mathbb{R}^{B\times h\times n\times d_h}.
$$

然后做 causal attention：

$$
\mathrm{softmax}\left({QK^{\mathsf T}\over\sqrt{d_h}}\right)V.
$$

生成出 $t_n$ 后，下一步前缀变成：

```text
[t0, t1, ..., t_{n-1}, t_n]
```

如果不用 cache，就会重新计算 $t_0,\ldots,t_{n-1}$ 的所有 key/value。历史部分其实没有变，这就是浪费。

## Cache 到底缓存什么

在 self-attention 中，第 $i$ 个位置需要：

- 自己的 query $q_i$。
- 所有可见位置的 key $k_j$。
- 所有可见位置的 value $v_j$。

自回归推理第 $n$ 步只需要新 token 的 query：

$$
q_n.
$$

但它要读取整个历史的 key/value：

$$
k_0,\ldots,k_n,
\qquad
v_0,\ldots,v_n.
$$

所以缓存的是每一层、每一个 head 的历史 $K,V$：

$$
K_{\rm cache},V_{\rm cache}
\in
\mathbb{R}^{B\times h\times n\times d_h}.
$$

如果需要把 $Q,K,V$、mask、softmax 和 $PV$ 的矩阵关系放在一张图里看，可以对照 [Attention 机制：单头 Self-Attention 一图总览](attention.md#single-head-self-attention-overview)。

新 token 到来时，只计算：

$$
k_n,v_n\in\mathbb{R}^{B\times h\times 1\times d_h},
$$

再拼到 cache 后面：

$$
K_{\rm cache}\leftarrow
\mathrm{Concat}(K_{\rm cache},k_n),
$$

$$
V_{\rm cache}\leftarrow
\mathrm{Concat}(V_{\rm cache},v_n).
$$

## 一步推理的 Shape

假设当前 cache 长度为 $n$，新输入只有一个 token。则新 token 的隐藏状态为：

$$
X_{\rm new}\in\mathbb{R}^{B\times 1\times d_{\rm model}}.
$$

投影并拆头后：

$$
Q_{\rm new},K_{\rm new},V_{\rm new}
\in
\mathbb{R}^{B\times h\times 1\times d_h}.
$$

把 $K_{\rm new},V_{\rm new}$ 接到历史 cache 后：

$$
K_{\rm all},V_{\rm all}
\in
\mathbb{R}^{B\times h\times (n+1)\times d_h}.
$$

attention 打分为：

$$
S=
{Q_{\rm new}K_{\rm all}^{\mathsf T}\over\sqrt{d_h}}
\in
\mathbb{R}^{B\times h\times 1\times (n+1)}.
$$

输出为：

$$
H_{\rm new}
=
\mathrm{softmax}(S)V_{\rm all}
\in
\mathbb{R}^{B\times h\times 1\times d_h}.
$$

拼接所有 head 并过 $W^O$ 后回到：

$$
\mathrm{MHA}(X_{\rm new})
\in
\mathbb{R}^{B\times 1\times d_{\rm model}}.
$$

这一步只产生最后一个 token 的新表示，因为推理时我们只需要下一个 token 的 logits。

## 为什么不缓存 Query

历史 query 对下一步没有用。第 $n$ 步需要的是“当前 token 要读什么”，也就是 $q_n$。历史 token 的 query 只在它们自己作为当前位置时用过一次，之后不会再被读取。

Key 和 value 则不同。未来每一个新 token 都可能读取历史 token，所以历史 $K,V$ 值得缓存。

## 训练时为什么通常不用 KV Cache

训练时整段序列一次进入模型：

$$
X\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

模型同时计算所有位置的 $Q,K,V$，再用 causal mask 保证位置 $i$ 看不到未来。虽然 mask 限制了信息流，计算仍然是并行矩阵乘法。

KV cache 适用于逐 token 推理。训练时使用 cache 反而会破坏并行性，并且还要保留反向传播需要的中间量，通常不划算。

## 计算量直觉

不用 cache 时，生成第 $n$ 个 token 要重算长度 $n$ 的整段前缀。总计算会反复覆盖历史部分。

使用 cache 后，每一步只计算新 token 的 $Q,K,V$，再让新 query 读历史 $K,V$。注意力打分长度仍然随上下文增长：

$$
1\times n,
$$

但避免了历史 token 的重复投影和重复层计算。

## 代价

KV cache 用内存换速度。若有 $L$ 层 decoder，cache 大小大约正比于：

$$
2\times L\times B\times h\times N\times d_h.
$$

其中前面的 $2$ 来自 key 和 value 两份缓存。长上下文推理时，KV cache 会成为显存占用的重要来源。

## 和 NNQS 采样的关系

NNQS 的自回归采样也按前缀逐步生成：

```text
[] -> t0 -> t1 -> ... -> t_{L-1}
```

如果实现为“一步一步调用 Transformer”，KV cache 可以复用已经生成前缀的 key/value。每一步只计算新 pair token 的表示，再得到下一个 pair token 的概率分布。

不过教学版代码为了清晰，可能会选择每一步重算前缀，或者一次性计算整段序列的 log probability。是否引入 KV cache 取决于目标：

| 目标 | 建议 |
| --- | --- |
| 讲清楚公式和 VMC 流程 | 先不引入 KV cache |
| 加速长序列自回归采样 | 可以加入 KV cache |
| 训练整段序列的 log probability | 通常不使用 KV cache |

所以 KV cache 是推理/采样优化，不是 Transformer 数学定义本身。

## 招聘考点

!!! question "代表题：KV cache 显存怎么估算？"
    对 decoder-only 推理，KV cache 大小近似为 $2\times L\times B\times h\times N\times d_h\times\text{bytes\_per\_element}$。其中 2 来自 K/V 两份缓存，$N$ 是上下文长度。完整题解见 [数值精度、显存与推理优化题](../interview/precision_inference.md)。
