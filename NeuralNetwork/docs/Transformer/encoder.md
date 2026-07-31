# Encoder 的基本结构

Encoder 用来把整段输入编码成上下文化表示。它通常采用双向 self-attention，也就是每个 token 可以看见整个输入序列。

可以把 encoder 理解成“读完整段输入后，为每个位置生成一个上下文化表示”。它适合理解类任务，比如分类、检索、序列标注，也可以作为 encoder-decoder 模型里的条件信息来源。

## 输入与输出

输入经过 embedding 和位置编码后：

$$
X\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

经过 $L$ 层 encoder block 后得到：

$$
Z_L\in\mathbb{R}^{B\times N\times d_{\rm model}}.
$$

这里每个位置的向量都融合了全序列信息。

和 decoder 不同，encoder 的目标通常不是预测下一个 token，而是得到一组可供下游任务使用的表示。

## Encoder Block

一个典型 encoder block 包含：

```text
self-attention
  -> residual + layer norm
  -> feed-forward network
  -> residual + layer norm
```

由于 encoder 做的是双向表征，self-attention 中通常不使用 causal mask。若输入有 padding，则需要 padding mask，避免模型关注补齐 token。

## 双向 Self-Attention

Encoder attention 写作：

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{softmax}\left({QK^{\mathsf T}\over\sqrt{d_h}}+M_{\rm pad}\right)V.
$$

其中 $M_{\rm pad}$ 对 padding 位置填入 $-\infty$，真实 token 位置填入 $0$。

双向可见意味着第 $i$ 个位置可以读取任意第 $j$ 个位置：

$$
1\le i,j\le N.
$$

这适合分类、检索、句子表示、masked language modeling 等任务。

## FFN 与残差

每个位置独立经过同一个 FFN：

$$
\mathrm{FFN}(x)
=\sigma(xW_1+b_1)W_2+b_2.
$$

它不混合位置，只改变每个 token 的特征表示。位置之间的信息交换已经由 self-attention 完成。

Post-LN 形式：

$$
Y=\mathrm{LayerNorm}(X+\mathrm{MHA}(X)),
$$

$$
Z=\mathrm{LayerNorm}(Y+\mathrm{FFN}(Y)).
$$

Pre-LN 形式：

$$
Y=X+\mathrm{MHA}(\mathrm{LayerNorm}(X)),
$$

$$
Z=Y+\mathrm{FFN}(\mathrm{LayerNorm}(Y)).
$$

## Encoder 的输出如何使用

不同任务会取不同位置的输出：

| 任务 | 常见取法 |
| --- | --- |
| 分类 | 取 `[CLS]` 位置或 mean pooling |
| 序列标注 | 每个位置分别接分类头 |
| 检索 | 池化成一个向量 |
| encoder-decoder | 作为 decoder cross-attention 的 memory |

## Encoder 与 Decoder 的区别

| 对比项 | Encoder | Decoder |
| --- | --- | --- |
| 可见范围 | 双向 | 只能看左侧和自己 |
| 典型 mask | padding mask | causal mask + padding mask |
| 输出用途 | 表征 | 预测下一个 token |
| 代表模型 | BERT | GPT |

Encoder 的优势在于充分利用上下文，适合理解类任务。Decoder 的优势在于自然分解联合概率，适合生成和自回归建模。

如果把 Transformer 看成“信息流设计”，encoder 允许双向流动，decoder 只允许从左到右流动。这个差别来自任务目标，而不是来自 $Q,K,V$ 公式本身。
