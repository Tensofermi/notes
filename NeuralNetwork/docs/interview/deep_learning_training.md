# 深度学习与训练题

深度学习面试题通常考“训练为什么会成功或失败”。重点不是背层名，而是能解释梯度、归一化、初始化、优化器和训练曲线。

## 题目：为什么深层网络需要非线性激活函数？

**来源背景**：深度学习基础笔试题改写。

**考点定位**：线性变换、表达能力、激活函数。

**先给结论**：如果没有非线性，多层线性网络仍然等价于一层线性变换，表达能力不会随层数本质增强。

**解题思路**：

两层线性网络：

$$
y=W_2(W_1x)=W x,
\quad
W=W_2W_1.
$$

无论叠多少层，只要中间没有非线性，最终还是线性函数。

加入 ReLU、GELU、tanh 等非线性后，网络可以表示复杂的非线性函数。

**易错点**：

- 激活函数不是为了“让输出变大”，而是引入非线性。
- ReLU 可能出现 dead neuron，GELU 在 Transformer 中更常见。

**关联阅读**：[常用层、激活函数与损失函数](../pytorch/layers_losses.md)。

## 题目：梯度消失和梯度爆炸为什么会发生？

**来源背景**：深层网络训练稳定性考点改写。

**考点定位**：链式法则、雅可比矩阵、初始化。

**先给结论**：反向传播是多层导数连乘。如果每层导数尺度长期小于 1，梯度会消失；长期大于 1，梯度会爆炸。

**解题思路**：

简化写成：

$$
{\partial L\over\partial x_0}
=
{\partial L\over\partial x_L}
\prod_{\ell=1}^L
{\partial x_\ell\over\partial x_{\ell-1}}.
$$

层数很深时，连乘会放大尺度问题。

缓解方式：

- 合理初始化。
- 使用残差连接。
- 使用归一化层。
- 梯度裁剪。
- 使用合适激活函数。

**易错点**：

- 梯度爆炸不一定只来自 RNN，深层 Transformer 也可能出现。
- residual 和 LayerNorm 是深层 Transformer 可训练的重要原因。

**关联阅读**：[Decoder 的基本结构](../Transformer/decoder.md)。

## 题目：BatchNorm 和 LayerNorm 有什么区别？

**来源背景**：华为 / 米哈游深度学习基础题改写。

**考点定位**：归一化维度、训练和推理差异、Transformer。

**先给结论**：BatchNorm 通常沿 batch 统计每个通道；LayerNorm 对单个样本的 hidden dimension 做归一化。Transformer 更常用 LayerNorm。

**解题思路**：

BatchNorm 依赖 batch 统计：

$$
\mu_c={1\over BN}\sum_{b,i}x_{b,i,c}.
$$

LayerNorm 对每个 token 的 hidden vector 统计：

$$
\mu_{b,i}={1\over d}\sum_jx_{b,i,j}.
$$

Transformer 中序列长度可变、batch 较小、训练和推理需要行为稳定，所以 LayerNorm 更合适。

**易错点**：

- `model.eval()` 会影响 BatchNorm 的 running statistics，但 LayerNorm 通常没有这种训练 / 推理统计差异。
- BatchNorm 不是不能用于 NLP，只是 Transformer 主流架构更适合 LayerNorm。

**关联阅读**：[LayerNorm](../Transformer/decoder.md#layernorm)。

## 题目：Residual connection 为什么有用？

**来源背景**：Transformer 和 ResNet 高频面试题改写。

**考点定位**：深层训练、信息保留、梯度传播。

**先给结论**：残差连接让网络学习修正量 $f(x)$，输出为 $x+f(x)$。它保留原始信息，并给梯度提供近似恒等路径。

**解题思路**：

若：

$$
y=x+f(x),
$$

则：

$$
{\partial y\over\partial x}
=
I+{\partial f\over\partial x}.
$$

这里的 $I$ 让梯度可以更直接地向前传播。

**易错点**：

- residual 不是简单“防止过拟合”，核心是优化和信息流。
- residual 要求相加张量 shape 一致，不一致时需要投影。

**关联阅读**：[Residual Connection](../Transformer/decoder.md#residual-connection)。

## 题目：Adam 和 AdamW 的区别是什么？

**来源背景**：字节 / 华为优化器高频题改写。

**考点定位**：自适应学习率、权重衰减、正则化。

**先给结论**：AdamW 把 weight decay 从 Adam 的梯度更新中解耦出来，通常比直接在 Adam 梯度里加 L2 正则更合理。

**解题思路**：

Adam 使用一阶矩和二阶矩：

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,
$$

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2.
$$

AdamW 更新可以理解为：

```text
先按 Adam 做自适应梯度更新
再对参数做独立 weight decay
```

**易错点**：

- SGD 中 L2 正则和 weight decay 近似等价；Adam 中不完全等价。
- bias 和 LayerNorm 参数通常不做 weight decay。

**关联阅读**：[优化方法](../prerequisites/optimization_methods.md)。

## 题目：训练 loss 突然变成 nan，应该怎么排查？

**来源背景**：深度学习工程面试题改写。

**考点定位**：数值稳定、学习率、梯度、mixed precision。

**先给结论**：按数据、loss、logits、梯度、优化器和精度设置逐层排查。

**解题思路**：

检查顺序：

1. 输入是否已经含有 `nan` 或 `inf`。
2. logits 是否过大。
3. loss 是否包含 `log(0)`、除以 0、sqrt 负数。
4. gradient norm 是否爆炸。
5. learning rate 是否过大。
6. FP16 是否使用 loss scaling。
7. LayerNorm / softmax 是否在低精度下不稳定。

**代码实现**：

```python
for name, p in model.named_parameters():
    if p.grad is not None and not torch.isfinite(p.grad).all():
        print("bad grad:", name)
```

**易错点**：

- `nan` 通常已经是结果，真正原因可能在更早一步。
- 混合精度下要先切回 FP32 做定位。

**关联阅读**：[数值精度](../numerical_precision.md)。

## 题目：Dropout 训练和推理时有什么区别？

**来源背景**：PyTorch 和深度学习基础题改写。

**考点定位**：正则化、train/eval 模式。

**先给结论**：训练时 dropout 随机置零部分激活；推理时关闭随机置零，使用完整网络。

**解题思路**：

训练时：

$$
\tilde h={m\odot h\over 1-p},
\quad
m_i\sim\mathrm{Bernoulli}(1-p).
$$

除以 $1-p$ 是为了保持期望尺度不变。

推理时直接使用 $h$。

**易错点**：

- 忘记 `model.eval()` 会导致推理结果随机。
- `torch.no_grad()` 不会自动切换 dropout 行为。

**关联阅读**：[保存、加载与 train/eval 模式](../pytorch/state_dict_train_eval.md)。

## 题目：为什么大模型训练常用 warmup？

**来源背景**：LLM 训练策略考点改写。

**考点定位**：学习率调度、训练稳定性。

**先给结论**：训练初期参数和优化器状态还不稳定，直接用大学习率容易炸；warmup 让学习率逐步升高。

**解题思路**：

常见 schedule：

```text
0 -> warmup_steps: 学习率线性升高
之后: cosine decay 或其他衰减
```

Adam 初期 $m_t,v_t$ 估计还不充分，warmup 可以降低早期过大更新的风险。

**易错点**：

- warmup 不是越长越好，过长会降低有效训练速度。
- warmup 解决的是优化稳定性，不是数据质量问题。

**关联阅读**：[训练循环](../pytorch/training_loop.md)。

