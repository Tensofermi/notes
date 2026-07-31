# Transformer 笔记总览

Transformer 的核心想法是：把一串 token 变成一串向量，再让每个位置通过 attention 从其他位置读取信息。相比循环神经网络，Transformer 在一个 block 中就能让任意两个位置直接交互，因此更适合长序列与大规模并行训练。

读这一章时可以抓住一条主线：

```text
离散 token
  -> 连续向量
  -> 加入位置信息
  -> attention 混合上下文
  -> FFN 做逐位置非线性变换
  -> 输出 logits 或上下文化表示
```

这一章按从输入到训练的顺序组织：

每一层 Transformer block 都维持同一个主干形状：

$$
X\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

这件事很重要。Attention、FFN、残差连接和 LayerNorm 的作用都围绕这个主干张量展开：中间可以拆头、投影、加权求和，但回到 block 输出时仍然是一组 $d_{\rm model}$ 维 token 向量。

## 阅读顺序

如果你想先补齐 Transformer 之前的架构谱系，可以读 [经典神经网络结构总览](../classic_architectures/index.md)。那一章把 MLP、CNN、RNN/LSTM、PixelCNN 和 RBM 放到同一张图里，对比它们如何表示函数、概率分布和巨大状态空间。

1. [Token、Embedding 与 Shape](tokenization_embedding.md)：先把输入张量的形状讲清楚。
2. [位置信息](position_encoding.md)：解释为什么 attention 需要额外的位置编码。
3. [Attention 机制](attention.md)：推导 $Q,K,V$、softmax 和多头注意力。
4. [Encoder 的基本结构](encoder.md)：适合理解 BERT 一类双向表征模型。
5. [Decoder 的基本结构](decoder.md)：适合理解 GPT 与自回归生成模型。
6. [KV Cache](kv_cache.md)：理解自回归推理为什么可以缓存历史 key/value。
7. [训练目标与 Mask](training.md)：区分 causal language modeling、masked language modeling 和 seq2seq。
8. [Transformer 与 NNQS](transformer_nnqs.md)：把 decoder-only Transformer 接回神经网络量子态。

## 可视化辅助

Transformer 很适合配合交互式可视化学习。建议先用可视化工具建立整体结构直觉，再回到本站的公式和 shape 推导。

| 推荐 | 适合看什么 | 我的建议 |
| --- | --- | --- |
| [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) | GPT 式 Transformer 的整体流程、token、embedding、$Q/K/V$、attention、MLP、next-token prediction | 首推。它是交互式的，能在浏览器里运行 GPT-2 small，并展示内部组件如何协同预测下一个 token。读 [Attention 机制](attention.md) 和 [Decoder 的基本结构](decoder.md) 前后都适合看。 |
| [LLM Visualization](https://bbycroft.net/llm) | 用 3D 方式观察 LLM 的矩阵流动、层结构、attention head、残差流和 logits 输出 | 适合建立“模型是一个巨大的矩阵流水线”的全局直觉。建议在读完 token、attention、decoder 后看，用来把各个模块重新拼成整体。 |

## 三种常见结构

| 结构 | 代表模型 | Attention mask | 常见任务 |
| --- | --- | --- | --- |
| Encoder-only | BERT | 双向可见 | 表征学习、分类、检索 |
| Decoder-only | GPT | causal mask | 自回归生成、语言模型、NNQS amplitude |
| Encoder-decoder | 原始 Transformer、T5 | encoder 双向，decoder causal + cross attention | 翻译、摘要、条件生成 |

## 训练和推理的差别

训练 decoder-only 模型时，整段序列可以一次送进模型：

```text
[BOS, t0, t1, ..., t_{N-2}]
  -> 同时预测
[t0,  t1, t2, ..., t_{N-1}]
```

虽然 causal mask 限制了每个位置只能看左侧，计算本身仍然是并行的。推理或采样时，模型只能一步一步生成：

```text
prefix -> next token -> longer prefix -> next token -> ...
```

这时如果每一步都重算整个 prefix，会浪费大量计算。KV cache 正是为了解决这个问题：历史 token 的 key/value 已经算过，就缓存下来，新一步只计算新 token 的 query/key/value。

## 最短心智模型

对每个位置 $i$，attention 做的是：

$$
\text{根据 }q_i\text{ 查询所有 }k_j，
\quad
\text{得到权重 }a_{ij},
\quad
\text{再加权求和所有 }v_j.
$$

写成公式：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{softmax}\left({QK^{\mathsf T}\over\sqrt{d_h}}\right)V.
$$

Decoder-only 模型再加一层 causal mask，使第 $i$ 个位置只能读取 $j\le i$ 的信息。这样模型才能学习：

$$
P(t_0,\ldots,t_{N-1})
=\prod_{i=0}^{N-1}P(t_i\mid t_{<i}).
$$
