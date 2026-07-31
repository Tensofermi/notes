# PixelCNN：二维格点上的自回归模型

PixelCNN 是一种用于二维离散数据的自回归模型。它最早常用于图像像素建模，也很适合帮助理解二维格点上的概率分解。

假设有一个二维 token grid：

```text
t00 t01 t02 t03
t10 t11 t12 t13
t20 t21 t22 t23
```

PixelCNN 先规定一个顺序，通常是 raster scan：

```text
t00 -> t01 -> t02 -> t03 -> t10 -> t11 -> ...
```

然后建模：

$$
P(\{t_{x,y}\})
=
\prod_{x,y}
P(t_{x,y}\mid \text{previous pixels}).
$$

这里 previous pixels 指：

```text
当前位置上面的所有行
当前位置左边的格点
```

## 为什么需要 mask

自回归模型不能在预测当前位置时偷看当前位置真实 token，也不能看未来位置。

普通 $3\times3$ 卷积会看：

```text
x x x
x x x
x x x
```

但第一层 PixelCNN 预测当前位置时，只能看：

```text
1 1 1
1 0 0
0 0 0
```

这叫 Type-A mask。中心位置为 0，表示不能看自己。

后续层常用 Type-B mask：

```text
1 1 1
1 1 0
0 0 0
```

后续层可以看中心 hidden，是因为第一层已经保证这个 hidden 不含原始当前位置 token。

## PixelCNN 和 Transformer

Transformer 的 causal mask 是作用在 attention matrix 上：

```text
position i 只能 attend 到 j <= i
```

PixelCNN 的 mask 是作用在 convolution kernel 上：

```text
卷积核只能看上方和左方
```

所以二者都是自回归模型，只是实现 causal structure 的方式不同：

| 模型 | causal 机制 |
| --- | --- |
| decoder-only Transformer | masked self-attention |
| RNN / LSTM | 时间递推天然因果 |
| PixelCNN | masked convolution |

## 最小 MaskedConv2d

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class MaskedConv2d(nn.Conv2d):
    def __init__(self, mask_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert mask_type in ["A", "B"]

        mask = torch.ones_like(self.weight)
        _, _, kh, kw = mask.shape
        cy = kh // 2
        cx = kw // 2

        if mask_type == "A":
            mask[:, :, cy, cx:] = 0
        else:
            mask[:, :, cy, cx + 1 :] = 0

        mask[:, :, cy + 1 :, :] = 0
        self.register_buffer("mask", mask)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.conv2d(
            x,
            self.weight * self.mask,
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )
```

## 最小 PixelCNN

输入：

```text
tokens: [batch, height, width]
```

输出：

```text
logits: [batch, n_tokens, height, width]
```

下面代码里的 `gather` 会沿 token channel 维取出真实格点 token 的 log probability。`gather` 的 shape 规则见 [常用 Tensor 操作：索引、gather、拼接、拆分与矩阵乘法](../pytorch/tensor_ops.md#gather)。

```python
class PixelCNN(nn.Module):
    def __init__(self, n_tokens: int, hidden_channels: int = 64, n_layers: int = 6):
        super().__init__()
        self.n_tokens = n_tokens

        layers = [
            MaskedConv2d(
                "A",
                in_channels=n_tokens,
                out_channels=hidden_channels,
                kernel_size=3,
                padding=1,
            ),
            nn.ReLU(),
        ]

        for _ in range(n_layers - 1):
            layers.extend(
                [
                    MaskedConv2d(
                        "B",
                        in_channels=hidden_channels,
                        out_channels=hidden_channels,
                        kernel_size=3,
                        padding=1,
                    ),
                    nn.ReLU(),
                ]
            )

        layers.append(nn.Conv2d(hidden_channels, n_tokens, kernel_size=1))
        self.net = nn.Sequential(*layers)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        x = F.one_hot(tokens, num_classes=self.n_tokens).float()
        x = x.permute(0, 3, 1, 2)
        return self.net(x)

    def log_prob(self, tokens: torch.Tensor) -> torch.Tensor:
        logits = self.forward(tokens)
        logp_all = F.log_softmax(logits, dim=1)
        chosen = logp_all.gather(
            dim=1,
            index=tokens.unsqueeze(1),
        ).squeeze(1)
        return chosen.flatten(1).sum(dim=-1)
```

## 在物理格点中的含义

如果构型是二维自旋：

$$
\sigma_{x,y}\in\{-1,+1\},
$$

可以把它按 raster scan 分解：

$$
P(\sigma)
=
P(\sigma_{0,0})
P(\sigma_{0,1}\mid\sigma_{0,0})
P(\sigma_{0,2}\mid\sigma_{0,0},\sigma_{0,1})
\cdots.
$$

PixelCNN 学的是每个格点在过去格点条件下的分布：

```text
previous lattice sites -> current site probability
```

优点：

- 对二维格点结构自然。
- 训练时所有位置 logits 可以并行算。
- 概率天然归一化。

缺点：

- 生成时仍要逐格点采样。
- 长程信息传播依赖卷积层数。
- 强长程关联系统可能需要 dilation、residual block 或 attention 增强。

所以 PixelCNN 可以理解成：

```text
二维局域因果光锥模型
```

而 decoder-only Transformer 更像：

```text
全局因果注意力模型
```
