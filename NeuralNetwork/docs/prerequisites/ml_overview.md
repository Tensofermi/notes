# 机器学习地图

机器学习的核心问题可以概括为一句话：

> 用数据或交互信号确定一个参数化函数，使它在未来输入上给出有用输出。

把模型写成：

$$
f_\theta:x\mapsto y,
$$

其中 $x$ 是输入，$y$ 是输出，$\theta$ 是可调参数。不同机器学习方法的差别主要来自三件事：

- 样本从哪里来。
- 优化信号是什么。
- 输出 $y$ 如何解释。

## 按学习方式分类

| 类型 | 样本形式 | 优化信号 | 典型任务 |
| --- | --- | --- | --- |
| 监督学习 | $(x,y)$ | 预测和标签的误差 | 分类、回归 |
| 无监督学习 | $x$ | 数据结构本身 | 聚类、降维、密度估计 |
| 自监督学习 | 从 $x$ 构造标签 | 预测被遮住或未来的部分 | 语言模型、表示学习 |
| 强化学习 | $(s,a,r,s')$ | 长期回报 | 控制、游戏、智能体 |
| 变分学习 | 从当前模型采样 | 能量、自由能或变分目标 | VMC、变分推断 |

监督学习中，数据集通常固定。训练目标是：

$$
\min_\theta {1\over N}\sum_{i=1}^N
\ell(f_\theta(x_i),y_i).
$$

自监督学习看起来没有人工标签，但会从数据中构造标签。例如 causal language modeling 中，输入前缀，目标是下一个 token：

$$
P_\theta(t_{i+1}\mid t_{\le i}).
$$

强化学习的样本来自环境交互。策略 $\pi_\theta(a\mid s)$ 选择动作，环境给出 reward，训练目标是最大化长期回报。

VMC / NQS 更特殊：样本来自当前波函数分布：

$$
p_\theta(x)=|\psi_\theta(x)|^2.
$$

参数更新会改变波函数，也会改变下一轮采样分布，所以这是一个闭环优化问题。

## 按输出类型分类

### 分类

分类任务输出离散类别。模型通常先输出 logits：

$$
z\in\mathbb{R}^C,
$$

再经过 softmax 得到类别概率：

$$
p_i={e^{z_i}\over\sum_j e^{z_j}}.
$$

常见损失是交叉熵。它和 KL 散度的关系见 [信息熵、交叉熵与 KL 散度](entropy_cross_entropy_kl.md)。

### 回归

回归任务输出连续数值，例如：

$$
f_\theta(x)\in\mathbb{R}.
$$

常见损失是均方误差：

$$
L(\theta)= {1\over N}\sum_i(f_\theta(x_i)-y_i)^2.
$$

最小二乘、Gauss-Newton 和 Levenberg-Marquardt 都可以看成回归优化方法，详见 [优化方法：梯度下降、Gauss-Newton 与 LM](optimization_methods.md)。

### 生成建模

生成模型学习数据分布：

$$
p_\theta(x)\approx p_{\rm data}(x).
$$

语言模型通常用链式法则把联合概率拆开：

$$
p_\theta(t_0,\ldots,t_{N-1})
=
\prod_i p_\theta(t_i\mid t_{<i}).
$$

这也是 decoder-only Transformer 和自回归 NNQS 的共同结构。

## 按数据结构分类

| 数据结构 | 常见模型 |
| --- | --- |
| 表格数据 | 线性模型、决策树、梯度提升树、MLP |
| 图像或格点构型 | CNN、ViT |
| 序列 | RNN、LSTM、Transformer |
| 图结构 | GNN |
| 量子 many-body 构型 | Tensor network、RBM、Transformer NQS |

模型结构通常和数据结构匹配。CNN 利用局部平移结构，Transformer 利用 attention 处理长程依赖，NNQS 则用神经网络压缩表示指数维 Hilbert space 中的波函数。

## 推断视角

机器学习不只是训练函数，也经常是在做推断：根据观测数据判断未知标签、隐藏变量、参数或未来结果。

| 场景 | 推断对象 |
| --- | --- |
| 分类模型 | 标签 $y$ |
| 贝叶斯模型 | 参数后验 $p(\theta\mid D)$ |
| 隐马尔可夫模型 | 隐藏状态序列 |
| 图模型 | 节点边缘概率 |
| POMDP | belief state |
| LLM 部署 | 下一个 token 或完整输出 |

更细的区分见 [推断、统计推断与信念传播](inference_belief_propagation.md)。

## 本站中的位置

这组笔记主要关心三条线：

1. 神经网络作为参数化函数。
2. Transformer 作为概率分布建模工具。
3. NNQS 把神经网络函数解释为波函数 $\psi_\theta(x)$。

因此后续所有章节都可以回到同一个抽象：

$$
\text{输入}
\xrightarrow{f_\theta}
\text{输出}
\xrightarrow{\text{目标函数}}
\text{更新 }\theta.
$$
