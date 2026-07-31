# 机器学习基础题

机器学习基础题常考“概念是否真的理解”。回答时不要只背定义，要能说清楚模型假设、优化目标、优缺点和适用场景。

## 题目：过拟合和欠拟合分别是什么？

**来源背景**：华为 / 字节 / 米哈游机器学习基础面试题改写。

**考点定位**：泛化误差、模型容量、正则化。

**先给结论**：欠拟合是训练集和测试集都表现差；过拟合是训练集表现好但测试集表现差。

**解题思路**：

| 情况 | 训练误差 | 测试误差 | 常见原因 |
| --- | --- | --- | --- |
| 欠拟合 | 高 | 高 | 模型太弱、特征不足、训练不充分 |
| 过拟合 | 低 | 高 | 模型太强、数据少、噪声大、正则不足 |

解决方法：

- 欠拟合：增大模型、增加特征、训练更久、调大学习率到合理范围。
- 过拟合：增加数据、正则化、dropout、early stopping、数据增强、减小模型。

**易错点**：

- 训练误差低不是最终目标，泛化才是目标。
- 正则化不是让训练误差更低，而是控制模型复杂度。

**关联阅读**：[模型训练就是函数拟合](../prerequisites/training_as_function_fitting.md)。

## 题目：KMeans 的目标函数是什么？

**来源背景**：聚类算法笔试题改写。

**考点定位**：无监督学习、聚类、交替优化。

**先给结论**：KMeans 最小化样本到所属簇中心的平方距离和。

**解题思路**：

设簇中心为 $\mu_1,\ldots,\mu_K$，样本分配为 $c_i$，目标为：

$$
\min_{\{c_i\},\{\mu_k\}}
\sum_i\|x_i-\mu_{c_i}\|_2^2.
$$

算法交替执行：

1. 固定中心，把样本分给最近中心。
2. 固定分配，把中心更新为簇内均值。

**易错点**：

- KMeans 对初值敏感。
- KMeans 假设簇大致是球形。
- KMeans 不是分类，因为没有标签。

**关联阅读**：[机器学习地图](../prerequisites/ml_overview.md)。

## 题目：EM 算法在优化什么？

**来源背景**：华为 AI 岗机器学习选择题考点改写。

**考点定位**：隐变量模型、最大似然、下界优化。

**先给结论**：EM 用 E 步估计隐变量后验，用 M 步最大化期望 complete-data log likelihood，本质是在优化观测数据似然的下界。

**解题思路**：

观测变量为 $x$，隐变量为 $z$，目标是：

$$
\log p_\theta(x)=\log\sum_zp_\theta(x,z).
$$

E 步：

$$
q(z)=p_{\theta^{old}}(z\mid x).
$$

M 步：

$$
\theta^{new}
=
\arg\max_\theta
\mathbb E_{q(z)}
[\log p_\theta(x,z)].
$$

**易错点**：

- E 步不是更新模型参数，而是更新隐变量分布。
- EM 通常收敛到局部最优。
- KMeans 可以看作硬分配版本的 EM 直觉。

**关联阅读**：[最大似然与前向 KL](../prerequisites/mle_forward_kl.md)。

## 题目：SVM 为什么要最大化间隔？

**来源背景**：传统机器学习面试题改写。

**考点定位**：分类边界、margin、正则化。

**先给结论**：最大间隔让分类边界离最近样本尽可能远，从而提高对扰动的鲁棒性。

**解题思路**：

线性分类器：

$$
f(x)=w^{\mathsf T}x+b.
$$

硬间隔 SVM：

$$
\min_{w,b}{1\over2}\|w\|^2
\quad
\text{s.t. }
y_i(w^{\mathsf T}x_i+b)\ge1.
$$

因为几何间隔与 $1/\|w\|$ 成正比，所以最小化 $\|w\|^2$ 等价于最大化间隔。

**易错点**：

- 支持向量是离边界最近、决定边界的样本。
- 软间隔允许分类错误，引入 slack variable。
- kernel trick 不是显式升维，而是通过核函数计算内积。

**关联阅读**：[优化方法](../prerequisites/optimization_methods.md)。

## 题目：决策树、随机森林和 GBDT 有什么区别？

**来源背景**：字节推荐 / 机器学习面试高频题改写。

**考点定位**：树模型、bagging、boosting。

**先给结论**：决策树是单棵树；随机森林是多棵树并行投票，降低方差；GBDT 是多棵树串行拟合残差，降低偏差。

**解题思路**：

| 模型 | 训练方式 | 主要作用 |
| --- | --- | --- |
| 决策树 | 单模型递归划分 | 可解释、容易过拟合 |
| 随机森林 | bagging，多树并行 | 降低方差 |
| GBDT | boosting，多树串行 | 降低偏差，拟合复杂函数 |

GBDT 每一步学习当前损失的负梯度方向。平方损失下，这等价于拟合残差。

**易错点**：

- 随机森林的树之间相对独立。
- GBDT 的树是串行依赖的。
- XGBoost / LightGBM 是工程增强版 GBDT，不只是普通决策树集合。

**关联阅读**：[机器学习地图](../prerequisites/ml_overview.md)。

## 题目：Bagging、Boosting、Stacking 区别是什么？

**来源背景**：集成学习面试题改写。

**考点定位**：模型集成、偏差-方差、二层学习器。

**先给结论**：

- Bagging：并行训练多个弱相关模型，平均或投票。
- Boosting：串行训练，后一个模型重点修正前一个模型错误。
- Stacking：把多个模型输出作为新特征，再训练二层模型。

**解题思路**：

Bagging 的代表是随机森林。Boosting 的代表是 AdaBoost、GBDT、XGBoost。Stacking 常用于竞赛，把不同模型的预测结果组合。

**易错点**：

- Stacking 需要避免数据泄露，二层模型应使用 out-of-fold 预测。
- Boosting 更容易过拟合，需要控制树深、学习率和轮数。

**关联阅读**：[机器学习地图](../prerequisites/ml_overview.md)。

## 题目：最大似然和最小 KL 有什么关系？

**来源背景**：概率模型、语言模型和分类模型考点改写。

**考点定位**：MLE、forward KL、经验分布。

**先给结论**：最大似然等价于最小化数据分布到模型分布的前向 KL：

$$
D_{\rm KL}(P_{\rm data}\Vert P_\theta).
$$

**解题思路**：

前向 KL：

$$
D_{\rm KL}(P_{\rm data}\Vert P_\theta)
=
\mathbb E_{x\sim P_{\rm data}}
\left[
\log P_{\rm data}(x)-\log P_\theta(x)
\right].
$$

第一项与 $\theta$ 无关，所以最小化 KL 等价于最大化：

$$
\mathbb E_{x\sim P_{\rm data}}\log P_\theta(x).
$$

这就是最大似然。

**易错点**：

- 前向 KL 和反向 KL 行为不同。
- 交叉熵训练语言模型就是 next-token 条件分布上的 MLE。

**关联阅读**：[最大似然与前向 KL](../prerequisites/mle_forward_kl.md)。

## 题目：分类模型为什么常输出 logits 而不是概率？

**来源背景**：深度学习实现和 PyTorch 损失函数考点改写。

**考点定位**：logits、softmax、数值稳定。

**先给结论**：logits 是 softmax 前的原始分数。训练时直接把 logits 交给交叉熵函数，可以使用 log-sum-exp 技巧，数值更稳定。

**解题思路**：

softmax：

$$
p_i={e^{z_i}\over\sum_j e^{z_j}}.
$$

交叉熵：

$$
L=-z_y+\log\sum_j e^{z_j}.
$$

实际实现会先减去最大 logit：

$$
\log\sum_j e^{z_j}
=
m+\log\sum_j e^{z_j-m},
\quad
m=\max_j z_j.
$$

**易错点**：

- 不要在 `CrossEntropyLoss` 前手动 softmax。
- logits 不是概率，可以为负，也不要求和为 1。

**关联阅读**：[信息熵、交叉熵与 KL 散度](../prerequisites/entropy_cross_entropy_kl.md)。

