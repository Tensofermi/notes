# 总览：从知识点到题型

这个专题把华为、字节、米哈游近几年公开面经和岗位要求中反复出现的 AI / 算法 / 大模型考点，改写成代表题来讲。这里的目标不是复刻原题，而是把“题目背后的知识结构”讲清楚。

题目主要来自公开面经考点、招聘方向和常见笔试题型的整理。使用时要注意：公司每年题目会变，真正稳定的是知识点和解题方法。

## 怎么读

建议按下面路线：

```text
先学知识页
  -> 看对应代表题
  -> 回到专题题库刷同类题
  -> 按公司路线查缺补漏
```

如果是准备笔试，优先看：

1. [数学、概率与线性代数题](math_probability.md)
2. [机器学习基础题](ml_basics.md)
3. [深度学习与训练题](deep_learning_training.md)
4. [AI 方向编程题思路](coding_ai.md)

如果是准备算法工程或大模型面试，优先看：

1. [Transformer 与 LLM 题](transformer_llm.md)
2. [PyTorch 与工程实现题](pytorch_engineering.md)
3. [数值精度、显存与推理优化题](precision_inference.md)
4. [强化学习与后训练题](rl_post_training.md)

## 题目格式

每道题尽量按统一结构写：

```text
题目
  -> 来源背景
  -> 考点定位
  -> 先给结论
  -> 解题思路
  -> 公式推导 / 代码实现
  -> 易错点
  -> 关联阅读
```

这样做的原因是：招聘题通常不难在公式本身，难在面试时要把“为什么”讲清楚。比如问 AdamW，不只是背公式，还要说明 weight decay 为什么不应该简单混进 Adam 的梯度里；问 KV cache，不只是说缓存 K/V，还要会估算显存。

## 公司画像

| 公司 | 常见形态 | 准备重点 |
| --- | --- | --- |
| 华为 | AI 选择题、编程题、工程推理、模型部署相关问题 | 数学基础、机器学习基础、Transformer、数值精度、显存估算、推理优化 |
| 字节 | 算法题、机器学习面试、推荐 / NLP / LLM 项目深挖 | 数据结构算法、LR/GBDT/深度模型、Transformer、召回排序、训练和推理系统 |
| 米哈游 | 工程面、图形 / 视觉 / 游戏 AI、深度学习基础 | PyTorch、CV/生成模型、C++/Python 工程、推理优化、强化学习和智能体 |

## 公开来源说明

本专题参考的是公开网页、公开面经和公开岗位描述，例如：

- [牛客华为 AI 岗机考整理](https://www.nowcoder.com/discuss/794930989293117440)
- [CSDN 华为 AI 岗笔试整理](https://blog.csdn.net/nju_spy/article/details/153254025)
- [CodeFun2000 笔试题路线](https://codefun2000.com/)
- [华为 AI 招聘方向](https://career.huawei.com/reccampportal/globle/huawei-special-recruitment.html)
- [字节校园招聘岗位](https://jobs.bytedance.com/campus/position/7508758933424490770/detail)
- [米哈游校园招聘](https://campus.mihoyo.com/)

为避免版权和泄露风险，本站不逐字搬运任何疑似未授权题目。所有题目都按“公开考点代表题”重写，重点放在知识解释和解题方法。

## 高频考点总表

| 模块 | 高频问题 | 对应专题 |
| --- | --- | --- |
| 概率统计 | 条件概率、期望、方差、MLE、KL | [数学、概率与线性代数题](math_probability.md) |
| 机器学习 | PCA、KMeans、EM、SVM、决策树、GBDT | [机器学习基础题](ml_basics.md) |
| 深度学习 | 过拟合、正则化、BN/LN、优化器、loss 曲线 | [深度学习与训练题](deep_learning_training.md) |
| Transformer | QKV、mask、multi-head、decoder-only、KV cache | [Transformer 与 LLM 题](transformer_llm.md) |
| PyTorch | shape、autograd、Module、state_dict、train/eval | [PyTorch 与工程实现题](pytorch_engineering.md) |
| 推理优化 | FP16/BF16、量化、显存、吞吐、延迟 | [数值精度、显存与推理优化题](precision_inference.md) |
| 强化学习 | policy、value、reward、PPO、RLHF | [强化学习与后训练题](rl_post_training.md) |
| 编程题 | 数组、字符串、DP、图、模拟、top-k | [AI 方向编程题思路](coding_ai.md) |

## 使用原则

一道题最好做到三层掌握：

1. 会算：能写出公式或代码。
2. 会解释：能把直觉讲清楚。
3. 会迁移：题目换一个背景仍然能认出同一个模型。

例如“交叉熵为什么等价于最大似然”可以出现在分类模型、语言模型、推荐排序、策略学习甚至变分分布拟合里。只记答案不够，关键是知道它在分布匹配中扮演什么角色。

