# 模型结构

教学版 NNQS 把复波函数拆成两个可读性很强的部分：

$$
\psi_\theta(x)
  = \exp(\log A_\theta(x))\exp(i\phi_\theta(x)).
$$

其中 $ \log A_\theta(x) $ 决定采样概率，$ \phi_\theta(x) $ 决定复相位。

## Bitstring 到 Token

输入 state 是 $0/1$ occupation bitstring：

$$
x = [\alpha_0,\beta_0,\alpha_1,\beta_1,\ldots].
$$

每个 spatial orbital 的 $\alpha,\beta$ 两个占据数组成一个 token：

| pair | token | 含义 |
| --- | ---: | --- |
| $00$ | 0 | 空 |
| $10$ | 1 | 只有 $\alpha$ 电子 |
| $01$ | 2 | 只有 $\beta$ 电子 |
| $11$ | 3 | 双占据 |

Transformer 输入前会加 start token：

```text
[S, token_0, token_1, ...]
```

这样第 $i$ 个位置预测 $t_i$ 时，只依赖左侧已经生成的 token。

## AmplitudeTransformer

`AmplitudeTransformer` 是 causal Transformer。它学习联合概率的链式分解：

$$
P_\theta(t_0,\ldots,t_{L-1})
  = \prod_{i=0}^{L-1}P_\theta(t_i\mid t_{<i}).
$$

取对数：

$$
\log P_\theta(x)
  = \sum_i \log P_\theta(t_i\mid t_{<i}).
$$

采样概率希望等于波函数模方：

$$
P_\theta(x) = |\psi_\theta(x)|^2
  = \exp(2\log A_\theta(x)).
$$

因此代码中定义：

$$
\log A_\theta(x)
  = {1 \over 2}\sum_i \log P_\theta(t_i\mid t_{<i}).
$$

这个 $1/2$ 很关键：Transformer 建模的是概率，波函数振幅是概率幅。

## PhaseMLP

采样只依赖 $ |\psi_\theta(x)|^2 $，相位不改变 state 被抽到的概率。Hamiltonian 连接不同 basis state 时，local energy 中会出现比值：

$$
{\psi_\theta(x') \over \psi_\theta(x)}.
$$

这时相位会决定不同贡献的相干叠加。教学版把这部分交给一个独立 MLP：

$$
\phi_\theta(x)=\mathrm{PhaseMLP}(x).
$$

这样 amplitude 与 phase 的责任比较清楚：

| 模块 | 输入 | 输出 | 主要作用 |
| --- | --- | --- | --- |
| `AmplitudeTransformer` | pair token 序列 | `log_amp` | 产生可采样的概率模型 |
| `PhaseMLP` | 完整 bitstring | `phase` | 给复波函数补相位 |
| `NeuralQuantumState` | bitstring | `log_amp, phase, psi` | 统一波函数接口 |

## Forward 接口

主接口是：

```python
out = model(states)
```

返回字典：

```python
log_amp = out["log_amp"]
phase = out["phase"]
psi = out["psi"]
```

对应公式：

$$
\psi_\theta(x)
  = \exp(\mathrm{log\_amp}(x))\exp(i\,\mathrm{phase}(x)).
$$

## 一个 4-Qubit 例子

设：

$$
x=[1,0,0,1].
$$

按 $[\alpha_0,\beta_0,\alpha_1,\beta_1]$ 分组：

$$
[1,0]\to 1,\qquad [0,1]\to 2.
$$

token 序列是：

```text
[1, 2]
```

Transformer 不直接输出 $\psi(x)$。它先输出每一步 token 的条件概率：

| 步骤 | 已知内容 | 要预测的 token | 例子中的 log probability |
| --- | --- | --- | ---: |
| 第 0 步 | start token $S$ | $t_0=1$ | $-0.7$ |
| 第 1 步 | $S,t_0=1$ | $t_1=2$ | $-1.2$ |

把两步加起来，得到这个完整 state 的 log probability：

$$
\log P(x)
  = \log P(t_0=1\mid S)
  + \log P(t_1=2\mid S,t_0=1)
  = -0.7-1.2=-1.9.
$$

波函数的模方才是采样概率：

$$
P(x)=|\psi(x)|^2.
$$

如果写成 $\psi(x)=\exp(\log A(x))\exp(i\phi(x))$，那么：

$$
|\psi(x)|^2 = \exp(2\log A(x)).
$$

所以振幅的 log 要取一半：

$$
\log A(x)
  = {1\over 2}\log P(x)
  = {1\over 2}(-1.9)
  = -0.95.
$$

假设 `PhaseMLP` 另外输出相位：

$$
\phi(x)=0.3.
$$

最终复波函数就是：

$$
\psi(x)
  = \exp(-0.95)\exp(0.3i).
$$

如果只看大小，$\exp(-0.95)\approx 0.3867$。第二个因子 $\exp(0.3i)$ 只负责把这个数转到复平面上的相位角 $0.3$。
