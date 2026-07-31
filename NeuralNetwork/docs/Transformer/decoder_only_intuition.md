# Decoder-only 的直觉问答

这一页用问答方式补充 decoder-only Transformer 的直觉。详细公式见 [Decoder 的基本结构](decoder.md)。

## 为什么叫 encoder 和 decoder

原始 Transformer 是 encoder-decoder 架构，用于机器翻译。

```text
源语言句子 -> encoder -> 上下文表示 -> decoder -> 目标语言句子
```

encoder 负责把输入序列编码成上下文化表示。decoder 负责在已有目标前缀基础上生成下一个 token。

在 GPT 这类模型中，只有 decoder stack，因此称为 decoder-only。

## Embedding 算不算 encoder

从广义上说，embedding 把 token id 编码成向量：

$$
t_i\mapsto x_i\in\mathbb{R}^{d_{\rm model}}.
$$

但在 Transformer 架构术语中，encoder 是由 self-attention 和 FFN 堆叠成的模块，不是单纯 embedding。

因此更准确的说法是：

```text
embedding 是输入表示层
encoder 是一种双向上下文化模块
decoder 是一种带 causal mask 的自回归模块
```

## Decoder-only 是不是一个字一个字读输入

训练时不是。

训练时完整序列一次输入：

```text
[BOS, t0, t1, ..., tN]
```

GPU 可以并行计算所有位置。causal mask 只限制信息流：

$$
\text{第 }i\text{ 个位置只能看见 }j\le i.
$$

所以：

```text
计算是并行的
语义依赖是因果的
```

推理时才是严格逐 token：

```text
prefix -> next token -> longer prefix -> next token
```

## KV cache 为什么有用

推理第 $n$ 步时，历史 token 的 key/value 已经算过。如果每一步都重算整个 prefix，会浪费计算。

KV cache 保存每层历史：

$$
K_{\rm cache},V_{\rm cache}
\in
\mathbb{R}^{B\times h\times n\times d_h}.
$$

下一步只算新 token 的 $Q,K,V$，再让新 query 读取历史 cache。

## 为什么主流 LLM 多用 decoder-only

主要原因是 next-token prediction 可以统一很多任务：

```text
翻译: 把下面中文翻译成英文: ...
问答: 问题: ... 回答:
代码: 根据注释补全代码:
推理: 给定条件，继续写解答:
```

只要任务能写成文本续写，就可以用同一个训练目标：

$$
\max_\theta\sum_i\log p_\theta(t_i\mid t_{<i}).
$$

decoder-only 的工程优势：

- 结构统一。
- 训练目标简单。
- 大规模语料天然适配。
- 推理时 KV cache 清晰。
- 多任务可以通过 prompt 统一。

encoder 没有消失。BERT、检索模型、双塔模型、embedding 模型仍然常用 encoder-only。

## Decoder-only 是不是在逼模型学习

可以这样理解：causal mask 让模型不能偷看未来，只能从左侧上下文中提取规律。

训练目标要求：

$$
p_\theta(t_{i+1}\mid t_{\le i})
$$

尽量接近真实数据中的下一个 token 分布。为了做好这个任务，模型必须学习语法、语义、事实、格式和任务模式。

但不要把它神秘化。它优化的仍然是一个明确的概率目标：next-token likelihood。

## 人类写作和 decoder-only 的差别

标准 decoder-only 生成是单调展开的。一旦输出 token，后续只能接着写，不能直接修改前文。

人类写作常常是：

```text
草稿 -> 回看 -> 修改 -> 重排 -> 定稿
```

这更像全局优化，而不是单调采样。

## 系统层推理机制：反悔式写作

如果想让 LLM 更接近人类写作，可以在系统层引入“反悔”机制：

- 先生成草稿，再评审和重写。
- 先写隐藏推理，再输出正式答案。
- 支持局部编辑，而不是只能续写。
- 用搜索在多个候选路径中选择。
- 维护一个可撤销窗口。

这些机制不是标准 decoder block 的一部分。它们通常属于推理框架、工具调用、搜索策略或产品交互层。

为什么不直接作为底层范式？

- KV cache 会失效或变复杂。
- 流式输出体验更难设计。
- 训练目标不再只是 next-token prediction。
- 算力成本更高。

因此当前主流做法仍是：底层用 decoder-only，高层通过推理框架补充草稿、反思、搜索和编辑能力。

