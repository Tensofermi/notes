# 从薛定谔方程到 NNQS

NNQS 的核心问题来自定态薛定谔方程：

$$
H|\Psi\rangle = E|\Psi\rangle .
$$

在数值计算中，这常常变成一个巨大 Hamiltonian 矩阵的最小本征值问题。神经网络量子态的想法是用一个可微函数 $\psi_\theta(x)$ 表示本征向量分量，再用变分 Monte Carlo 估计能量和梯度。

对应到教学版程序：

```text
物理问题        H |Psi> = E |Psi>
矩阵语言        求 Hamiltonian 最小本征值
basis 标签      occupation bitstring x
NNQS 表示       psi_theta(x)
VMC 估计        sample x -> E_loc(x) -> energy/gradient
代码流程        state -> model -> sampler -> hamiltonian -> trainer
```

## 定态方程

含时薛定谔方程为：

$$
i\hbar{\partial\over\partial t}|\Psi(t)\rangle
  = H|\Psi(t)\rangle .
$$

许多电子结构计算关心定态，尤其是能量最低的基态。定态问题写作：

$$
H|\Psi\rangle = E|\Psi\rangle .
$$

这就是线性代数中的本征值问题。$E$ 是能量本征值，$|\Psi\rangle$ 是对应的波函数；基态能量 $E_0$ 是最小本征值。

如果选定一组 basis $\{|x\rangle\}$，波函数可以展开为：

$$
|\Psi\rangle = \sum_x \psi(x)|x\rangle .
$$

代回定态方程得到：

$$
\sum_{x'}H_{xx'}\psi(x') = E\psi(x),
\qquad
H_{xx'}=\langle x|H|x'\rangle .
$$

于是物理问题落成了矩阵问题：求矩阵 $H$ 的最小本征值和本征向量。

## Occupation Bitstring Basis

电子结构问题先选一组 spin orbital。每个 spin orbital 只能空着或被占据，因此一个 many-body basis state 可以写成 occupation bitstring：

$$
x = [0,1,1,0,0,1,\ldots].
$$

在二次量子化语言中，Hamiltonian 常写为：

$$
H
= \sum_{pq}h_{pq}a_p^\dagger a_q
+ {1\over 2}\sum_{pqrs}h_{pqrs}
  a_p^\dagger a_q^\dagger a_r a_s .
$$

这里 $a_p^\dagger$ 和 $a_p$ 分别创建、湮灭第 $p$ 个 spin orbital 上的电子。选定 basis 后，occupation bitstring 就成为矩阵行列的标签。

教学版采用的 qubit 顺序为：

$$
[\alpha_0,\beta_0,\alpha_1,\beta_1,\ldots].
$$

例如：

$$
[1,0,0,1]
$$

表示 $\alpha_0$ 占据、$\beta_1$ 占据，其余为空。

如果有 $M$ 个 spin orbital，完整 Fock space 维度为：

$$
2^M .
$$

固定电子数 $N$ 后，维度降为：

$$
{M\choose N}.
$$

如果进一步固定 $\alpha,\beta$ 电子数：

$$
{M/2\choose N_\alpha}{M/2\choose N_\beta}.
$$

这解释了 `state.py` 为什么要处理 `n_alpha`、`n_beta` 和 electron conservation mask。

## 维度困难

小体系可以显式构造 Hamiltonian 矩阵并对角化：

$$
H\psi = E\psi .
$$

但 Hilbert space 维度随 orbital 数组合爆炸。例如：

$$
{60\choose 30}\sim 10^{17}.
$$

这意味着：

- 波函数向量 $\psi(x)$ 无法完整存储。
- Hamiltonian 矩阵更无法显式存储。
- 精确对角化只能处理很小的 active space。

所以需要一个压缩表示：给定 state $x$，能按需计算 $\psi(x)$，同时避免保存完整向量。

## 变分原理

变分原理给出：

$$
E[\psi]
= {\langle\psi|H|\psi\rangle\over\langle\psi|\psi\rangle}
\ge E_0 .
$$

只要给出一个合法的候选波函数，就可以算出一个基态能量上界。求基态可以转化成优化问题：

$$
\min_\theta
E[\psi_\theta]
=
\min_\theta
{\langle\psi_\theta|H|\psi_\theta\rangle
\over
\langle\psi_\theta|\psi_\theta\rangle}.
$$

NNQS 把候选波函数写成神经网络：

$$
x \mapsto \psi_\theta(x).
$$

这样，模型参数 $\theta$ 替代完整的波函数向量成为优化对象。

## NNQS 表示

教学版使用复波函数：

$$
\psi_\theta(x)
  = \exp(\log A_\theta(x))\exp(i\phi_\theta(x)).
$$

其中：

- `AmplitudeTransformer` 输出 $\log A_\theta(x)$。
- `PhaseMLP` 输出 $\phi_\theta(x)$。
- `NeuralQuantumState.forward(states)` 返回 `log_amp`、`phase`、`psi`。

代码接口为：

```python
out = model(states)
log_amp = out["log_amp"]
phase = out["phase"]
psi = out["psi"]
```

对应公式：

$$
\psi_\theta(x)
  = \exp(\mathrm{log\_amp}(x))
    \exp(i\,\mathrm{phase}(x)).
$$

训练完成后，权重 $\theta$ 固定下来，网络就可以看作一个可查询的波函数。推理时给定构型 $x$，模型直接 forward 得到：

$$
\log A_\theta(x),\qquad \phi_\theta(x),\qquad \psi_\theta(x).
$$

其中振幅决定采样概率：

$$
p_\theta(x)=|\psi_\theta(x)|^2=\exp(2\log A_\theta(x)),
$$

相位 $\phi_\theta(x)$ 决定 Hamiltonian 连接不同构型时的相干叠加。

## 自回归振幅

VMC 需要从概率分布中采样：

$$
p_\theta(x)
  = {|\psi_\theta(x)|^2\over\sum_{x'}|\psi_\theta(x')|^2}.
$$

教学版把 bitstring 按 spatial orbital 合成 token：

| pair | token |
| --- | ---: |
| $00$ | 0 |
| $10$ | 1 |
| $01$ | 2 |
| $11$ | 3 |

自回归模型写出联合概率：

$$
P_\theta(x)
  = \prod_i P_\theta(t_i\mid t_{<i}).
$$

取对数：

$$
\log P_\theta(x)
  = \sum_i \log P_\theta(t_i\mid t_{<i}).
$$

由于采样概率等于模方：

$$
P_\theta(x)=|\psi_\theta(x)|^2
  = \exp(2\log A_\theta(x)),
$$

振幅部分定义为：

$$
\log A_\theta(x)
  = {1\over 2}\sum_i\log P_\theta(t_i\mid t_{<i}).
$$

这个结构让 amplitude 可以直接逐 token 采样，并自然给出 normalized probability。

## 相位

相位不影响 $x$ 被采样到的概率，因为：

$$
|\exp(\log A+i\phi)|^2=\exp(2\log A).
$$

但 local energy 里会出现：

$$
{\psi_\theta(x')\over\psi_\theta(x)}.
$$

当 Hamiltonian 连接不同 basis state 时，相位决定不同贡献的相干叠加。教学版用 `PhaseMLP` 直接读取完整 bitstring，输出一个实数相位：

$$
\phi_\theta(x)=\mathrm{PhaseMLP}(x).
$$

## Local Energy

能量期望为：

$$
E_\theta
  = {\sum_{xx'}\psi_\theta(x)^*H_{xx'}\psi_\theta(x')
     \over
     \sum_x |\psi_\theta(x)|^2}.
$$

整理成采样友好的形式：

$$
E_\theta
  = \sum_x p_\theta(x)E_{\rm loc}(x),
$$

其中：

$$
E_{\rm loc}(x)
  = \sum_{x'}H_{xx'}{\psi_\theta(x')\over\psi_\theta(x)}.
$$

这个公式很重要：对采样到的 $x$，只需要找出 Hamiltonian 能连接到哪些 $x'$，再调用模型计算 $\psi_\theta(x')$ 和 $\psi_\theta(x)$。

如果 Hamiltonian 是 Pauli string 之和：

$$
H = \sum_k c_kP_k,
$$

每个 $P_k$ 作用到 bitstring 后只产生一个 connected state 以及一个矩阵元因子。`ExactHamiltonian` 正是在逐项执行这件事。

## 采样与 Counts

采样 $10^5$ 次时，很多 state 会重复出现。VMC 估计只需要知道每个 unique state 出现了几次，所以采样器返回：

```text
unique_states, counts, psi_values
```

权重为：

$$
w(x) = {\mathrm{count}(x)\over\sum_{x'}\mathrm{count}(x')}.
$$

能量估计写成：

$$
E_{\rm mean}
  = \sum_x w(x)E_{\rm loc}(x).
$$

教学版采样器还在每一步使用 restricted electron mask，保证最终 bitstring 满足固定的 $N_\alpha$ 和 $N_\beta$。

## VMC 梯度

目标是最小化：

$$
E(\theta)
  = {\langle\psi_\theta|H|\psi_\theta\rangle
     \over
     \langle\psi_\theta|\psi_\theta\rangle}.
$$

VMC 梯度可以写成：

$$
\nabla_\theta E
  = 2\,\mathrm{Re}\left[
      \left\langle
      (E_{\rm loc}(x)-E_{\rm mean})
      \nabla_\theta\log\psi_\theta(x)^*
      \right\rangle_{p_\theta}
    \right].
$$

教学版构造一个 proxy loss：

$$
L_{\rm proxy}
  = 2\,\mathrm{Re}\left[
      \sum_x w(x)\,
      \overline{\log\psi_\theta(x)}
      (E_{\rm loc}(x)-E_{\rm mean})
    \right].
$$

对这个 proxy 调用 `backward()`，PyTorch 就会把 VMC 梯度写入模型参数。

## 代码总结构

整个程序可以按物理概念对应到模块：

| 物理概念 | 代码模块 | 作用 |
| --- | --- | --- |
| occupation basis | `state.py` | bitstring、token、电子数约束 |
| 波函数 ansatz | `models.py` | `AmplitudeTransformer` + `PhaseMLP` |
| $\lvert\psi\rvert^2$ 采样 | `sampling.py` | `unique_states` + `counts` |
| Hamiltonian | `hamiltonian.py` | local energy |
| 变分优化 | `trainer.py` | energy mean、loss proxy、optimizer |
| 实验配置 | `config.py` | YAML 到 dataclass |
| 命令行 | `cli/train.py` | 训练入口 |

一轮训练可以压缩为：

```text
sample states
  -> evaluate local energies
  -> estimate energy mean
  -> build VMC proxy loss
  -> backward and optimizer.step
```

## 阅读建议

初读代码可以按这个顺序：

1. `state.py`：先确认 bitstring 和 token 表示。
2. `models.py`：看 `log_amp`、`phase`、`psi` 如何生成。
3. `sampling.py`：看自回归采样和 counts。
4. `hamiltonian.py`：看 local energy。
5. `trainer.py`：看一轮训练如何串联。
6. `cli/train.py`：看命令行如何进入 trainer。

修改代码时，建议每次只动一条链路，并同步补对应测试：

| 修改对象 | 优先测试 |
| --- | --- |
| 模型 | `tests/test_models.py`、`tests/test_sampling.py` |
| 采样 | `tests/test_sampling.py`、trainer smoke |
| Hamiltonian | `tests/test_hamiltonian.py`、CPU CLI smoke |
| 训练公式 | `tests/test_trainer.py`、CPU/GPU smoke |

## 一句话总结

NNQS+VMC 的图像是：

$$
\text{用神经网络按需计算 }\psi_\theta(x),
\quad
\text{用采样估计 }E_\theta\text{ 和 }\nabla_\theta E,
\quad
\text{通过变分优化逼近基态。}
$$
