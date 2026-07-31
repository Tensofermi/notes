# Transformer 与 NNQS

教学版 NNQS 中，Transformer 的角色是表示波函数振幅对应的概率分布。它使用的是 decoder-only 的自回归结构。

## 从 Bitstring 到 Token

电子 occupation bitstring 写作：

$$
x=[\alpha_0,\beta_0,\alpha_1,\beta_1,\ldots].
$$

每两个 qubit 合成一个 pair token：

$$
t_i=\alpha_i+2\beta_i.
$$

于是：

$$
x\quad\longrightarrow\quad
t=[t_0,t_1,\ldots,t_{L-1}].
$$

这一步把物理 basis state 转成了 Transformer 可以处理的离散序列。

## 自回归概率

AmplitudeTransformer 建模：

$$
P_\theta(t_0,\ldots,t_{L-1})
=
\prod_{i=0}^{L-1}P_\theta(t_i\mid t_{<i}).
$$

取 log：

$$
\log P_\theta(x)
=
\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

因为：

$$
P_\theta(x)=|\psi_\theta(x)|^2,
$$

所以：

$$
\log A_\theta(x)
=
{1\over 2}\log P_\theta(x)
=
{1\over 2}\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

这就是模型中 `log_amp` 前面出现 $1/2$ 的原因。

## 为什么需要 Causal Mask

计算 $P_\theta(t_i\mid t_{<i})$ 时，第 $i$ 个位置只能使用左侧 token。若模型看见了 $t_i$ 右边的信息，它就不再是合法的自回归分解。

Causal mask 保证：

$$
P_\theta(t_i\mid t_{<i})
$$

只依赖已经生成的前缀。

## Electron Mask

自然语言模型通常只需要 causal mask。NNQS 还要满足电子数守恒，例如固定 $N_\alpha$、$N_\beta$。因此采样时会使用 electron mask，禁止生成会违反电子数约束的 token。

概念上，每一步都在做：

```text
给出 prefix
  -> 计算下一个 token 的 logits
  -> 屏蔽不合法 token
  -> softmax
  -> sample
```

这样最终生成的 bitstring 自动满足物理约束。

## KV Cache 是否需要

NNQS 自回归采样和语言模型生成很像：

```text
[] -> t0 -> t1 -> ... -> t_{L-1}
```

每一步都基于当前 prefix 预测下一个 pair token。如果实现时每一步都重新把 prefix 输入 Transformer，那么历史 token 的 $K,V$ 会被重复计算。

KV cache 可以缓存历史 prefix 的 key/value：

$$
K_{\rm cache},V_{\rm cache}
\in
\mathbb{R}^{B\times h\times n\times d_h}.
$$

下一步只计算新 token 的 $Q,K,V$，再用新 query 读取历史 cache。这能加速长序列采样。

不过在教学版 NNQS 中，优先级通常是：

1. 先把自回归概率和 electron mask 写清楚。
2. 再把 local energy 与 VMC 梯度写对。
3. 当采样成为瓶颈时，再考虑 KV cache。

所以 KV cache 是工程优化，不是 NNQS 的物理核心。理解主线时，可以先忽略它；优化采样速度时，再回来看 [KV Cache](kv_cache.md)。

## Phase 网络

AmplitudeTransformer 只决定：

$$
|\psi_\theta(x)|^2.
$$

复波函数还需要相位：

$$
\psi_\theta(x)
=
\exp(\log A_\theta(x))\exp(i\phi_\theta(x)).
$$

教学版用 `PhaseMLP` 单独输出：

$$
\phi_\theta(x).
$$

这个拆分让采样和相位学习分开，便于理解和调试。

## 与语言模型的相同点

| 方面 | 语言模型 | NNQS |
| --- | --- | --- |
| 输入 | text token | pair token |
| 结构 | decoder-only Transformer | decoder-like AmplitudeTransformer |
| 分解 | $P(t_i\mid t_{<i})$ | $P_\theta(t_i\mid t_{<i})$ |
| mask | causal mask | causal mask + electron mask |

## 与语言模型的不同点

| 方面 | 语言模型 | NNQS |
| --- | --- | --- |
| 目标 | 预测下一个 token | 最小化变分能量 |
| loss | cross entropy | VMC proxy loss |
| 输出解释 | token 概率 | 波函数振幅 |
| 额外结构 | 通常实概率 | 复相位 $\phi_\theta(x)$ |

所以，NNQS 借用了 Transformer 的自回归概率建模能力，但服务的目标是量子多体基态求解。
