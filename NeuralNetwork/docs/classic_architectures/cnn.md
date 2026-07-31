# CNN：局部连接、权重共享与特征图

CNN, convolutional neural network，最适合处理有局部空间结构的数据，比如图片、二维格点、自旋构型、QMC snapshot。

它的核心不是“卷积这个名字”，而是两个结构假设：

1. 局部性：附近位置更相关。
2. 权重共享：同一种局部模式可以出现在不同位置。

## 为什么不用 MLP 直接处理图片

一张图片可以写成：

$$
x\in\mathbb R^{C\times H\times W}.
$$

如果展平成向量再接全连接层，第一层参数量约为：

$$
(CHW)\times d_{\rm hidden}.
$$

这有两个问题：

- 参数太多。
- 完全忽略二维邻域结构。

比如边缘、角点、纹理、局部图案可以出现在图片任意位置。MLP 会把不同位置看成完全不同的输入维度，而 CNN 会用同一个卷积核在整张图上滑动。

## 卷积在做什么

以单通道 $3\times3$ 卷积为例，一个卷积核：

$$
K\in\mathbb R^{3\times3}
$$

在图片每个局部窗口上做点积：

$$
y_{i,j}
=
\sum_{u=-1}^{1}\sum_{v=-1}^{1}
K_{u,v}x_{i+u,j+v}+b.
$$

这个 $K$ 在所有位置共享，所以它检测的是“某种局部模式是否出现”，而不是“某个固定坐标是否出现某个值”。

## 多通道卷积

真实 CNN 通常有多个输入通道和多个输出通道：

$$
x\in\mathbb R^{B\times C_{\rm in}\times H\times W}.
$$

卷积核：

$$
W\in\mathbb R^{C_{\rm out}\times C_{\rm in}\times k_h\times k_w}.
$$

输出：

$$
y\in\mathbb R^{B\times C_{\rm out}\times H'\times W'}.
$$

其中 $C_{\rm out}$ 可以理解成学出多少种局部特征探测器。

## 感受野

一层 $3\times3$ 卷积只能看局部邻域。多层堆叠后，高层特征的感受野会变大：

```text
第 1 层：看局部边缘
第 2 层：组合成角点、纹理
第 3 层：组合成局部部件
更高层：组合成更抽象结构
```

这就是 CNN 的层次表示。

## 池化和步幅

CNN 常用两种方式降低空间分辨率：

| 方法 | 作用 |
| --- | --- |
| pooling | 在局部区域取 max 或 average |
| stride convolution | 卷积核滑动步长大于 1 |

这样做可以：

- 扩大感受野。
- 降低计算量。
- 引入一定平移不变性。

但过度下采样会丢失空间细节，所以语义分割、生成模型、物理格点任务中要谨慎使用。

## 最小 PyTorch 例子

```python
import torch
import torch.nn as nn


class SmallCNN(nn.Module):
    def __init__(self, n_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Linear(64, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x:      [batch, 3, height, width]
        return: [batch, n_classes]
        """
        h = self.features(x)          # [B, 64, 1, 1]
        h = h.flatten(1)              # [B, 64]
        return self.classifier(h)


model = SmallCNN()
x = torch.randn(8, 3, 32, 32)
logits = model(x)
print(logits.shape)  # torch.Size([8, 10])
```

## CNN 和格点物理

对二维自旋、QMC 构型、格点场配置来说，CNN 很自然：

```text
格点上的局部相互作用
  -> 局部卷积核
  -> 多层组合出大尺度结构
```

例如 Ising 模型中局部邻域的排列、domain wall、cluster 形状都可以被 CNN 特征捕捉。

但 CNN 也有局限：

- 长程关联需要很多层或 dilation。
- 标准 CNN 默认平移共享，未必适合所有边界条件或非均匀结构。
- 如果相互作用图不是规则格点，GNN 或 attention 可能更自然。

## CNN 和 Transformer 的关系

CNN 的权重是固定的局部模板：

```text
同一个卷积核扫过所有位置
```

attention 的权重是输入相关的：

```text
每个 token 根据 QK 相似度决定看哪里
```

所以可以粗略理解：

```text
CNN:
  固定局部信息混合

Transformer:
  动态全局信息混合
```

CNN 参数和计算更局部，归纳偏置更强；Transformer 更灵活，但计算和数据需求通常更高。

