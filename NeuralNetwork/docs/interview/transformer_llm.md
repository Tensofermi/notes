# Transformer 与 LLM 题

Transformer 题通常有两类：一类考结构细节，例如 QKV、mask、multi-head；另一类考大模型训练和推理，例如 SFT、RLHF、KV cache、RAG、LoRA、量化。

## 题目：Tokenizer 和 Embedding 有什么区别？

**来源背景**：华为 / 字节 LLM 基础面试题改写。

**考点定位**：文本离散化、token id、向量表示。

**先给结论**：tokenizer 把文本变成 token id；embedding 把 token id 查表变成向量。

**解题思路**：

流程是：

```text
text
  -> tokenizer
  -> token ids
  -> embedding table
  -> dense vectors
```

若词表大小为 $|V|$，hidden dimension 为 $d_m$，embedding 矩阵：

$$
W_{\rm TE}\in\mathbb{R}^{|V|\times d_m}.
$$

输入 token id $t_i$ 后，取第 $t_i$ 行：

$$
x_i=W_{\rm TE}[t_i].
$$

**易错点**：

- tokenizer 本身通常不是神经网络层。
- embedding 是可训练参数。
- 同一个文本在不同 tokenizer 下可能被切成不同 token。

**关联阅读**：[Token、Embedding 与 Shape](../Transformer/tokenization_embedding.md)。

## 题目：Q、K、V 分别是什么意思？

**来源背景**：Transformer 高频基础题改写。

**考点定位**：self-attention、相似度、信息读取。

**先给结论**：Query 表示“我想找什么”，Key 表示“我有什么特征可被匹配”，Value 表示“如果被关注，要提供什么信息”。

**解题思路**：

输入：

$$
X\in\mathbb{R}^{B\times N\times d_m}.
$$

线性投影：

$$
Q=XW_Q,\quad K=XW_K,\quad V=XW_V.
$$

attention score：

$$
S={QK^{\mathsf T}\over\sqrt{d_h}}.
$$

权重：

$$
A=\mathrm{softmax}(S).
$$

输出：

$$
O=AV.
$$

**易错点**：

- Q/K 用来算权重，V 才是被加权求和的信息。
- self-attention 中 Q/K/V 都来自同一个输入；cross-attention 中 Q 和 K/V 来源不同。

**关联阅读**：[Attention 机制](../Transformer/attention.md)。

## 题目：为什么 attention 要除以 $\sqrt{d_k}$？

**来源背景**：字节 / 华为 Transformer 结构题改写。

**考点定位**：点积方差、softmax 饱和、数值稳定。

**先给结论**：若 $q,k$ 各维方差约为 1，则点积 $q\cdot k$ 的方差约为 $d_k$。除以 $\sqrt{d_k}$ 可以让 score 尺度稳定，避免 softmax 过早饱和。

**解题思路**：

假设：

$$
q_j,k_j
$$

独立、均值 0、方差 1。则：

$$
q\cdot k=\sum_{j=1}^{d_k}q_jk_j.
$$

方差约为：

$$
\mathrm{Var}(q\cdot k)\approx d_k.
$$

所以缩放：

$$
{q\cdot k\over\sqrt{d_k}}
$$

使方差回到常数级。

**易错点**：

- 缩放不是为了改变 shape，而是为了控制数值尺度。
- 如果 score 太大，softmax 会接近 one-hot，梯度变差。

**关联阅读**：[Attention 机制](../Transformer/attention.md)。

## 题目：Causal mask 的作用是什么？

**来源背景**：decoder-only、语言模型和 NNQS 自回归考点改写。

**考点定位**：自回归、信息泄露、mask shape。

**先给结论**：causal mask 防止当前位置看到未来 token，保证训练目标和推理过程一致。

**解题思路**：

语言模型训练预测：

$$
P(t_{i+1}\mid t_{\le i}).
$$

如果第 $i$ 个位置能看到 $t_{i+1}$，训练就泄露答案。mask 将未来位置的 attention score 设为 $-\infty$：

$$
S_{ij}=-\infty,\quad j>i.
$$

softmax 后这些位置权重为 0。

**易错点**：

- causal mask 不等于 padding mask。
- 训练可并行计算所有位置，但信息流仍然被 mask 限制。
- NNQS 自回归采样也需要这个结构约束。

**关联阅读**：[训练目标与 Mask](../Transformer/training.md)。

## 题目：Encoder-only、Decoder-only、Encoder-Decoder 有什么区别？

**来源背景**：BERT、GPT、T5 类模型比较题改写。

**考点定位**：架构、mask、任务类型。

**先给结论**：

- encoder-only：双向理解，适合分类、抽取、表征。
- decoder-only：单向生成，适合自回归语言模型。
- encoder-decoder：输入编码 + 输出生成，适合翻译、摘要等 seq2seq。

**解题思路**：

| 架构 | attention | 典型任务 |
| --- | --- | --- |
| Encoder-only | 双向 self-attention | 文本分类、检索、抽取 |
| Decoder-only | causal self-attention | 续写、对话、代码生成 |
| Encoder-Decoder | encoder 双向，decoder causal + cross-attention | 翻译、摘要 |

LLM 多采用 decoder-only，因为预训练目标和推理方式都是 next-token prediction，结构简单且容易扩展。

**易错点**：

- embedding 不是 encoder。
- decoder-only 训练时可以并行，推理时通常逐 token 串行。

**关联阅读**：[Decoder-only 的直觉问答](../Transformer/decoder_only_intuition.md)。

## 题目：KV cache 缓存的是什么？为什么能加速？

**来源背景**：大模型推理优化高频题改写。

**考点定位**：自回归推理、缓存、显存换速度。

**先给结论**：KV cache 缓存历史 token 在每层的 key 和 value。生成新 token 时，只需要算新 token 的 Q/K/V，并让新 Q 读取历史 K/V，避免重复计算历史前缀。

**解题思路**：

第 $n$ 步生成时，历史 cache：

$$
K,V\in\mathbb{R}^{B\times h\times n\times d_h}.
$$

新 token 的 query：

$$
Q_{\rm new}\in\mathbb{R}^{B\times h\times1\times d_h}.
$$

attention score：

$$
Q_{\rm new}K_{\rm cache}^{\mathsf T}
\in
\mathbb{R}^{B\times h\times1\times n}.
$$

**易错点**：

- 通常不缓存历史 Q，因为未来不会再用历史 Q。
- KV cache 加速推理，但增加显存。
- 训练整段序列时通常不用 KV cache。

**关联阅读**：[KV Cache](../Transformer/kv_cache.md)。

## 题目：SFT、Reward Model、RLHF 分别是什么？

**来源背景**：大模型训练流程面试题改写。

**考点定位**：后训练、监督微调、偏好学习、强化学习。

**先给结论**：

- SFT：用高质量指令数据做监督微调。
- Reward Model：学习人类偏好分数。
- RLHF：用 reward 指导策略继续优化，常见方法包括 PPO 类方法。

**解题思路**：

流程：

```text
预训练模型
  -> SFT
  -> reward model / preference model
  -> RLHF 或 DPO 类偏好优化
```

SFT 最大化标准答案概率。Reward Model 输入回答，输出偏好分数。RLHF 优化策略时需要限制新模型不要偏离参考模型太远。

**易错点**：

- SFT 不是强化学习。
- reward 不是人工手写规则，而常由偏好数据训练得到。
- PPO 中的 KL 约束用于防止模型偏离过大。

**关联阅读**：[PPO 的基本动机](../rl/ppo.md)。

## 题目：LoRA 为什么能减少微调参数量？

**来源背景**：LLM 微调和部署面试题改写。

**考点定位**：低秩分解、参数高效微调。

**先给结论**：LoRA 冻结原权重，只学习一个低秩增量：

$$
\Delta W=BA,
$$

其中秩 $r\ll d$，所以新增参数远少于完整矩阵。

**解题思路**：

原矩阵：

$$
W\in\mathbb{R}^{d_{\rm out}\times d_{\rm in}}.
$$

LoRA 学：

$$
A\in\mathbb{R}^{r\times d_{\rm in}},
\quad
B\in\mathbb{R}^{d_{\rm out}\times r}.
$$

新增参数量：

$$
r(d_{\rm in}+d_{\rm out})
$$

远小于：

$$
d_{\rm in}d_{\rm out}.
$$

**易错点**：

- LoRA 不是量化；它是参数高效微调。
- LoRA 通常插在 attention 或 MLP 的线性层上。
- 推理时可把 $\Delta W$ 合并回原权重。

**关联阅读**：[Decoder 的基本结构](../Transformer/decoder.md)。

## 题目：RAG 解决什么问题？

**来源背景**：华为 / 字节大模型应用题改写。

**考点定位**：检索增强生成、向量数据库、幻觉缓解。

**先给结论**：RAG 在生成前先从外部知识库检索相关材料，把材料作为上下文喂给模型，从而减少模型只依赖参数记忆。

**解题思路**：

流程：

```text
query
  -> embedding
  -> 向量检索 top-k 文档
  -> 拼接 prompt
  -> LLM 生成回答
```

RAG 适合知识更新频繁、需要引用来源、内部文档问答等场景。

**易错点**：

- RAG 不能保证完全无幻觉，检索质量和 prompt 设计仍然重要。
- 向量检索召回错误时，模型可能基于错误上下文生成。
- RAG 不是训练方法，更多是推理时的系统架构。

**关联阅读**：[数值精度、显存与推理优化题](precision_inference.md)。
