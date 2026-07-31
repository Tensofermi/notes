# 经典神经网络结构总览

在进入 Transformer、强化学习和 NNQS 之前，最好先把几类经典网络放到同一张图里看：

| 模型 | 最适合的输入结构 | 核心思想 | 输出常见形态 |
| --- | --- | --- | --- |
| MLP | 固定长度向量 | 全连接层逐层做非线性变换 | 分类 logits、回归值、特征向量 |
| CNN | 图像、格点、局部结构数据 | 局部连接 + 权重共享 | 分类 logits、特征图、像素级输出 |
| RNN / GRU / LSTM | 序列 | 用隐藏态递推压缩历史信息 | 每步 logits、最终状态、序列表示 |
| PixelCNN | 二维离散格点 | masked convolution 实现自回归分布 | 每个格点的 token logits |
| RBM | 二值构型、能量模型、波函数 ansatz | 给整个构型一个能量或振幅分数 | energy、free energy、log amplitude |
| Transformer | 序列、集合、长程依赖 | attention 让 token 直接读取上下文 | next-token logits、上下文表示 |

这些模型的差别，不只是“层长得不一样”。更本质的问题是：

> 模型如何利用数据结构，把巨大状态空间压缩成一个可计算函数。

## 两条主线

经典神经网络结构可以按两条主线理解。

第一条是判别式或函数拟合主线：

```text
input
  -> hidden representation
  -> output
```

MLP、CNN 分类器、很多视觉模型都属于这个图像。它们更像是在学一个函数：

$$
f_\theta(x)\rightarrow y.
$$

第二条是概率建模主线：

```text
configuration / sequence
  -> probability / energy / amplitude
```

RNN language model、PixelCNN、decoder-only Transformer、RBM、NNQS 都更接近这一条。它们关心的不只是预测一个标签，而是表示一个分布或波函数。

## 自回归模型和能量模型

在概率建模里，有一个非常重要的分叉。

RNN、PixelCNN、decoder-only Transformer 都可以写成自回归分解：

$$
P(t_0,t_1,\ldots,t_{N-1})
=
\prod_{i=0}^{N-1}P(t_i\mid t_{<i}).
$$

这类模型的优点是天然归一化。每一步输出一个条件概率，整条序列概率就是条件概率连乘。代码上通常返回：

```text
logits: [batch, length, n_tokens]
```

或者二维格点版本：

```text
logits: [batch, n_tokens, height, width]
```

RBM 不是这样。RBM 直接给整个 configuration 一个分数：

$$
P(v)
=
{e^{-F(v)}\over Z}.
$$

这里 $Z$ 是配分函数。它通常很难精确计算，所以 RBM 属于 energy-based model 的代表。代码上常见输出是：

```text
energy / free_energy / log_amplitude: [batch]
```

## 和 Transformer 的关系

理解这些旧模型，会让 Transformer 更清楚：

| 旧模型视角 | Transformer 做了什么 |
| --- | --- |
| MLP | 每个 token 内部仍然靠 MLP 做非线性加工 |
| CNN | attention 可以看成更灵活的、输入相关的非局域卷积 |
| RNN | 把 prefix 压缩到 hidden state，Transformer 改成直接读取所有 prefix token |
| LSTM | 用门控缓解长期依赖，Transformer 用 attention 缩短信息路径 |
| PixelCNN | 用 mask 保证自回归，Transformer 用 causal mask |
| RBM | 同样可用于概率/波函数建模，但范式从条件概率换成能量或振幅分数 |

所以 Transformer 不是凭空出现的。它继承了这些问题意识：

```text
如何表示函数
如何利用局部结构
如何处理序列
如何建模概率分布
如何在巨大状态空间中避免显式枚举
```

## 推荐阅读顺序

如果你主要想理解现代神经网络：

```text
MLP
  -> CNN
  -> RNN / LSTM / GRU
  -> PixelCNN
  -> RBM
  -> Transformer
```

如果你主要想理解 NNQS：

```text
MLP: 基本函数近似
  -> CNN / PixelCNN: 格点结构和自回归概率
  -> RBM: 早期神经网络量子态 ansatz
  -> Transformer: 现代自回归波函数表示
```

对应章节：

- [MLP：最基本的全连接网络](mlp.md)
- [CNN：局部连接、权重共享与特征图](cnn.md)
- [RNN、GRU 与 LSTM](rnn_lstm.md)
- [PixelCNN：二维格点上的自回归模型](pixelcnn.md)
- [RBM：能量模型与神经网络量子态](rbm.md)

