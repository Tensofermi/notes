# 华为、字节、米哈游考点地图

这一页先按公司整理准备方向。它不是“押题”，而是把公开面经和岗位描述中反复出现的知识点映射到本站章节。

## 总表

| 公司 | 常见题型 | 高频知识点 | 对应章节 |
| --- | --- | --- | --- |
| 华为 | AI 选择题、编程题、模型部署、工程推理 | PCA、EM、KMeans、Transformer、RAG、量化、显存估算 | [机器学习基础题](ml_basics.md)、[Transformer 与 LLM 题](transformer_llm.md)、[数值精度、显存与推理优化题](precision_inference.md) |
| 字节 | 算法题、ML 面试、推荐 / NLP / LLM 项目深挖 | LR、GBDT、BERT、attention、召回排序、优化器、线上推理 | [机器学习基础题](ml_basics.md)、[深度学习与训练题](deep_learning_training.md)、[PyTorch 与工程实现题](pytorch_engineering.md) |
| 米哈游 | 工程面、图形 / 视觉 / 生成模型、游戏 AI | CNN、PyTorch、数值精度、推理优化、强化学习、agent | [深度学习与训练题](deep_learning_training.md)、[强化学习与后训练题](rl_post_training.md)、[AI 方向编程题思路](coding_ai.md) |

## 华为路线

华为 AI 岗常见特点是：题面可能覆盖很宽，从数学、机器学习、深度学习到大模型部署都会出现。准备时要优先补齐基础概念和工程估算能力。

建议顺序：

```text
PCA / EM / KMeans / KL
  -> Transformer 基础
  -> 数值精度和显存估算
  -> 编程题
```

典型追问包括：

- PCA 为什么要中心化？
- EM 的 E 步和 M 步分别在优化什么？
- Transformer 中 $QK^T/\sqrt{d_k}$ 为什么要除以根号维度？
- BF16 和 FP16 谁更容易溢出？
- 一个 batch 的 KV cache 大约占多少显存？

回答策略：

1. 先说定义。
2. 再说公式。
3. 最后说工程含义。

比如显存题，不要只说“占很多显存”，而要写：

$$
\text{bytes}
=2\times L\times B\times h\times N\times d_h\times \text{bytes\_per\_element}.
$$

## 字节路线

字节算法面试通常更重视“能否把模型放到真实业务里”。因此机器学习基础、推荐系统直觉、NLP / LLM 结构、项目细节都会被追问。

建议顺序：

```text
LR / GBDT / 正则化
  -> 推荐召回和排序直觉
  -> Transformer / BERT / GPT
  -> 训练和推理工程
  -> 编程题
```

典型追问包括：

- LR 为什么适合做二分类和 CTR 预估？
- GBDT 和随机森林的区别是什么？
- BERT 和 GPT 的 mask 有什么不同？
- Adam 和 AdamW 的区别是什么？
- 如果线上推理延迟太高，你会怎么优化？

回答策略：

- 先把任务目标说清楚：分类、排序、生成、检索。
- 再把模型输入输出说清楚。
- 最后讨论线上约束：延迟、吞吐、显存、稳定性。

## 米哈游路线

米哈游公开 AI 真题相对少，准备时更适合按岗位能力反推：游戏、图形、视觉、生成模型和智能体相关岗位会重视工程实现、模型理解和系统调试能力。

建议顺序：

```text
PyTorch 工程
  -> CNN / Transformer / 生成模型基础
  -> 推理优化
  -> 强化学习和 agent
  -> C++ / Python 编程题
```

典型追问包括：

- `model.eval()` 和 `torch.no_grad()` 是一回事吗？
- BatchNorm 和 LayerNorm 为什么适用场景不同？
- 图像任务为什么常用 CNN？
- 游戏 AI 中 reward shaping 有什么风险？
- 推理时为什么可以使用 INT8 量化？

回答策略：

- 多讲 shape、数据流和运行模式。
- 工程题要能指出 bug 来源，例如 device mismatch、inplace 破坏计算图、显存泄漏。
- RL 题要强调 reward 设计可能导致模型钻空子。

## 横向能力

三家公司都需要的能力可以归纳成四类：

| 能力 | 体现 |
| --- | --- |
| 数学表达 | 能把 loss、概率、梯度、矩阵 shape 写清楚 |
| 模型理解 | 能解释模型结构为什么这样设计 |
| 工程落地 | 能处理 dtype、device、显存、推理延迟 |
| 编程实现 | 能在有限时间写出正确、可读的算法代码 |

因此复习不要只背概念。每个知识点都至少要会回答：

```text
它解决什么问题？
公式是什么？
shape 是什么？
训练时怎么用？
推理时有什么工程代价？
```

