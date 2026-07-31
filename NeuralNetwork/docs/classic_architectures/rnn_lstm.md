# RNN、GRU 与 LSTM

RNN, recurrent neural network，是处理序列的经典模型。它的核心思想是：

> 把前面读过的 prefix 压缩进一个递推隐藏态。

给定输入序列：

$$
x_0,x_1,\ldots,x_{T-1},
$$

普通 RNN 每一步更新：

$$
h_t = \phi(W_xx_t + W_hh_{t-1}+b).
$$

这里 $h_t$ 是 hidden state。它应该包含从 $x_0$ 到 $x_t$ 的历史信息。

## RNN 和 decoder-only Transformer 的对应

decoder-only Transformer 做的是：

```text
[S, t0, t1, t2, ...]
  -> 每个位置预测下一个 token
```

RNN 也可以做同样的自回归任务：

```text
h0 记住 [S]
h1 记住 [S, t0]
h2 记住 [S, t0, t1]
h3 记住 [S, t0, t1, t2]
```

然后：

$$
\mathrm{logits}_t = W_{\rm out}h_t+b_{\rm out}.
$$

所以 RNN、LSTM、GRU、decoder-only Transformer 都可以建模：

$$
P(t_0,t_1,\ldots,t_{N-1})
=
\prod_{i=0}^{N-1}P(t_i\mid t_{<i}).
$$

区别在于 prefix 怎么表示：

| 模型 | prefix 表示方式 |
| --- | --- |
| RNN | 压缩成一个 hidden state |
| LSTM / GRU | 用门控 hidden state 记住更长信息 |
| Transformer | 每个位置通过 attention 直接读取历史 token |

## 普通 RNN 的问题

普通 RNN 每一步都把旧信息和新输入混合成新 $h_t$。这会带来两个问题：

1. 长期信息容易被覆盖。
2. 反向传播时梯度容易消失或爆炸。

从反向传播角度看，梯度要反复乘上类似 $W_h$ 的矩阵。时间步很长时，乘积可能趋近 0，也可能爆炸。

这就是 LSTM 和 GRU 出现的背景：用门控机制控制信息保留、写入和输出。

## LSTM 的核心

LSTM 每一步有两个状态：

```text
h_t: hidden state，暴露给外部的输出状态
c_t: cell state，内部长期记忆
```

每个时间步接收：

$$
x_t,\quad h_{t-1},\quad c_{t-1},
$$

输出：

$$
h_t,\quad c_t.
$$

LSTM 的核心是三个门和一个候选记忆：

| 符号 | 名字 | 作用 |
| --- | --- | --- |
| $f_t$ | forget gate | 决定旧记忆保留多少 |
| $i_t$ | input gate | 决定新信息写入多少 |
| $\tilde c_t$ | candidate cell | 候选新记忆内容 |
| $o_t$ | output gate | 决定把多少内部记忆暴露出去 |

完整公式：

$$
f_t=\sigma(W_f[h_{t-1},x_t]+b_f),
$$

$$
i_t=\sigma(W_i[h_{t-1},x_t]+b_i),
$$

$$
\tilde c_t=\tanh(W_c[h_{t-1},x_t]+b_c),
$$

$$
c_t=f_t\odot c_{t-1}+i_t\odot \tilde c_t,
$$

$$
o_t=\sigma(W_o[h_{t-1},x_t]+b_o),
$$

$$
h_t=o_t\odot\tanh(c_t).
$$

最关键的是：

$$
c_t=f_t\odot c_{t-1}+i_t\odot \tilde c_t.
$$

它不是每一步完全重写记忆，而是在旧记忆上做加法式更新。这条 cell state 路径可以看成一种记忆通道。

## LSTM 的直观比喻

可以把 LSTM 想成一个会记笔记的人。每读一个 token，它问三件事：

```text
以前笔记里哪些内容该忘？
当前 token 哪些新信息值得写进去？
现在要把笔记里的哪些内容拿出来用于预测？
```

对应关系：

| 问题 | LSTM 组件 |
| --- | --- |
| 忘多少旧信息 | forget gate $f_t$ |
| 写多少新信息 | input gate $i_t$ |
| 新内容是什么 | candidate memory $\tilde c_t$ |
| 输出多少记忆 | output gate $o_t$ |

## GRU

GRU, gated recurrent unit，是比 LSTM 更简洁的门控 RNN。它没有单独的 cell state，而是直接维护 hidden state。

常见公式：

$$
z_t=\sigma(W_zx_t+U_zh_{t-1}+b_z),
$$

$$
r_t=\sigma(W_rx_t+U_rh_{t-1}+b_r),
$$

$$
\tilde h_t=\tanh(W_hx_t+U_h(r_t\odot h_{t-1})+b_h),
$$

$$
h_t=(1-z_t)\odot h_{t-1}+z_t\odot \tilde h_t.
$$

其中：

| 门 | 作用 |
| --- | --- |
| update gate $z_t$ | 控制保留旧 hidden 还是写入新 hidden |
| reset gate $r_t$ | 控制计算候选状态时看多少旧 hidden |

GRU 参数更少，计算更轻；LSTM 结构更显式，长期记忆通道更清楚。

## 自回归 RNN 的 PyTorch 写法

下面用 `nn.GRU` 写一个最小自回归模型。输入 token 形状：

```text
tokens: [batch, length]
```

输出：

```text
logits: [batch, length, n_tokens]
```

其中 `logits[:, i, :]` 预测 `tokens[:, i]`。

下面代码里的 `gather` 用来从词表维取出真实 token 对应的 log probability。这个 API 的 shape 规则见 [常用 Tensor 操作：索引、gather、拼接、拆分与矩阵乘法](../pytorch/tensor_ops.md#gather)。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class RNNAutoregressive(nn.Module):
    def __init__(self, n_tokens: int, d_model: int, n_layers: int = 1):
        super().__init__()
        self.n_tokens = n_tokens
        self.start_token = n_tokens
        self.embedding = nn.Embedding(n_tokens + 1, d_model)
        self.rnn = nn.GRU(
            input_size=d_model,
            hidden_size=d_model,
            num_layers=n_layers,
            batch_first=True,
        )
        self.output = nn.Linear(d_model, n_tokens)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        batch, _ = tokens.shape
        start = torch.full(
            (batch, 1),
            self.start_token,
            dtype=tokens.dtype,
            device=tokens.device,
        )
        model_input = torch.cat([start, tokens[:, :-1]], dim=1)
        x = self.embedding(model_input)
        hidden, _ = self.rnn(x)
        return self.output(hidden)

    def log_prob(self, tokens: torch.Tensor) -> torch.Tensor:
        logits = self.forward(tokens)
        logp_all = F.log_softmax(logits, dim=-1)
        chosen = logp_all.gather(
            dim=-1,
            index=tokens.unsqueeze(-1),
        ).squeeze(-1)
        return chosen.sum(dim=-1)
```

## 生成时缓存什么

Transformer 推理时缓存历史 K/V：

```text
t0 -> KV0
t1 -> KV1
t2 -> KV2
```

RNN 更简单，只缓存一个 hidden state：

```text
h_t = f(h_{t-1}, x_t)
```

所以 RNN 生成时很省缓存，但表达能力受限于 hidden state 容量。

| 模型 | 生成时缓存 |
| --- | --- |
| RNN / GRU / LSTM | hidden state，LSTM 还缓存 cell state |
| Transformer | 每层每个历史 token 的 key/value |
| PixelCNN | 通常不方便高效缓存 |
| RBM | 不按顺序生成，常用 Gibbs sampling |

## LSTM 和 Transformer 的区别

LSTM 是递推结构：

$$
h_t \text{ depends on } h_{t-1}.
$$

所以它很难在时间维完全并行：

```text
x_0 -> x_1 -> x_2 -> x_3
```

Transformer 的 self-attention 可以让所有 token 同时计算，并通过 causal mask 保证不看未来：

```text
x_0, x_1, x_2, x_3 同时进入 attention
```

对比：

| 模型 | 优点 | 缺点 |
| --- | --- | --- |
| RNN | 简单，天然序列递推 | 长期依赖弱，难并行 |
| LSTM / GRU | 门控缓解长期依赖 | 仍然顺序计算，超长依赖有限 |
| Transformer | 并行性强，长距离路径短 | attention 复杂度高，需要位置编码和 KV cache |

历史上可以粗略看成：

```text
RNN
  -> LSTM / GRU
  -> Attention + RNN
  -> Transformer
```
