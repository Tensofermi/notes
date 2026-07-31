# 自回归、贝叶斯递推与语言模型

自回归模型的基础是概率链式法则。

对两个变量：

$$
P(a,b)=P(a)P(b\mid a).
$$

对三个变量：

$$
P(a,b,c)
=
P(a)P(b\mid a)P(c\mid a,b).
$$

推广到序列：

$$
P(t_0,\ldots,t_{N-1})
=
\prod_{i=0}^{N-1}
P(t_i\mid t_{<i}).
$$

这就是自回归分解。

## 为什么这总是成立

由条件概率定义：

$$
P(a,b)=P(a)P(b\mid a).
$$

再把：

$$
P(a,b,c)=P(a,b)P(c\mid a,b)
$$

代入，就得到三变量形式。

因此链式法则不是模型假设，而是概率恒等式。

模型假设在于：我们用神经网络近似每一个条件概率：

$$
P_\theta(t_i\mid t_{<i}).
$$

## 语言模型

语言模型给定前缀，预测下一个 token：

$$
t_{<i}
\rightarrow
P_\theta(t_i\mid t_{<i}).
$$

整段序列 likelihood 为：

$$
\log P_\theta(t_0,\ldots,t_{N-1})
=
\sum_i
\log P_\theta(t_i\mid t_{<i}).
$$

训练时最大化这个 log likelihood，等价于最小化 next-token cross entropy。

## 为什么需要 causal mask

如果模型在预测 $t_i$ 时能看到 $t_i$ 或未来 token，训练会作弊。

causal mask 保证第 $i$ 个位置只能访问：

$$
t_0,\ldots,t_i.
$$

如果第 $i$ 个 hidden state 用来预测 $t_{i+1}$，那么它只能看见：

$$
t_{\le i}.
$$

## 和 NNQS amplitude 的关系

NNQS 中，构型 $x$ 可以编码成 token 序列：

$$
t_0,\ldots,t_{N-1}.
$$

自回归 amplitude network 给出：

$$
P_\theta(x)
=
\prod_i P_\theta(t_i\mid t_{<i}).
$$

取对数：

$$
\log P_\theta(x)
=
\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

由于采样概率等于波函数模方：

$$
P_\theta(x)=|\psi_\theta(x)|^2.
$$

若：

$$
\psi_\theta(x)
=
\exp(\log A_\theta(x))e^{i\phi_\theta(x)},
$$

则：

$$
|\psi_\theta(x)|^2
=
\exp(2\log A_\theta(x)).
$$

因此：

$$
\log A_\theta(x)
=
{1\over2}
\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

这就是自回归语言模型和 NNQS amplitude 的连接点。

## 采样

自回归采样按顺序进行：

```text
sample t0 from P(t0)
sample t1 from P(t1 | t0)
sample t2 from P(t2 | t0,t1)
...
```

在 NNQS 中，还会加入电子数约束 mask，保证生成的 bitstring 满足物理 sector。

## 直觉

自回归建模把一个高维联合分布拆成很多低维条件分布：

$$
\text{难的联合分布}
\rightarrow
\text{一串 next-token 条件分布}.
$$

这并不让问题自动变简单，但让神经网络可以用统一的方式参数化和采样。

