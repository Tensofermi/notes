# VMC 训练

VMC 每轮训练围绕四个动作展开：

```text
sample -> local_energy -> energy_mean -> gradient update
```

这套流程把巨大 Hilbert space 上的求和，换成从当前波函数分布中抽样后的统计估计。

## 采样分布

模型给出波函数：

$$
\psi_\theta(x)
  = \exp(\log A_\theta(x))\exp(i\phi_\theta(x)).
$$

采样分布取模方：

$$
p_\theta(x)
  = {|\psi_\theta(x)|^2 \over \sum_{x'}|\psi_\theta(x')|^2}.
$$

教学版使用自回归 amplitude，因此可以逐 token 采样。采样器返回：

```text
unique_states, counts, psi_values
```

对应权重：

$$
w(x) = {\mathrm{count}(x) \over \sum_{x'}\mathrm{count}(x')}.
$$

## Local Energy

能量期望可以写成：

$$
E_\theta
  = \sum_x p_\theta(x)E_{\rm loc}(x),
$$

其中局域能为：

$$
E_{\rm loc}(x)
  = \sum_{x'}H_{xx'}{\psi_\theta(x')\over \psi_\theta(x)}.
$$

这个公式把 Hamiltonian 的作用限制在采样到的 $x$ 附近。`ExactHamiltonian` 逐个 Pauli term 找 connected state；`CppHamiltonian` 调用旧 C++ 后端计算同一件事。

## 能量估计

一轮采样下，平均能量估计为：

$$
E_{\rm mean}
  = \sum_x w(x) E_{\rm loc}(x).
$$

日志里的 `energy_real` 是 $E_{\rm mean}$ 的实部。理想情况下，物理 Hamiltonian 的能量应当是实数；`energy_imag` 可以作为数值误差或实现错误的信号。

## VMC 梯度

变分目标是：

$$
E(\theta)
  = {\langle\psi_\theta|H|\psi_\theta\rangle
     \over
     \langle\psi_\theta|\psi_\theta\rangle}.
$$

VMC 常用的 log-derivative 梯度可写成：

$$
\nabla_\theta E
  = 2\,\mathrm{Re}\left[
      \left\langle
      (E_{\rm loc}(x)-E_{\rm mean})
      \nabla_\theta \log \psi_\theta(x)^*
      \right\rangle_{p_\theta}
    \right].
$$

教学版用一个实数 proxy loss 让 PyTorch 产生这条梯度：

$$
L_{\rm proxy}
  = 2\,\mathrm{Re}\left[
      \sum_x w(x)\,
      \overline{\log\psi_\theta(x)}\,
      (E_{\rm loc}(x)-E_{\rm mean})
    \right].
$$

`loss_proxy` 的数值不作为训练目标解释，它的作用是把正确方向写入模型参数的 `.grad`。

## 从公式到代码变量

`trainer.py` 中常见变量和公式的对应关系如下：

| 代码变量 | 数学对象 |
| --- | --- |
| `states_cpu` | $x$ |
| `counts_cpu` | $\mathrm{count}(x)$ |
| `weights_np` | $w(x)$ |
| `local_energies` | $E_{\rm loc}(x)$ |
| `energy_mean` | $E_{\rm mean}$ |
| `eloc_corr` | $E_{\rm loc}(x)-E_{\rm mean}$ |
| `outputs["log_amp"]` | $\log A_\theta(x)$ |
| `outputs["phase"]` | $\phi_\theta(x)$ |

令：

$$
\log\psi_\theta(x)=\log A_\theta(x)+i\phi_\theta(x),
\qquad
E_{\rm loc}(x)-E_{\rm mean}=a(x)+ib(x).
$$

则：

$$
\mathrm{Re}\left[
\overline{\log\psi_\theta(x)}(a+ib)
\right]
= \log A_\theta(x)a(x)+\phi_\theta(x)b(x).
$$

代码可以完全用实数张量写：

```python
loss_proxy = 2.0 * torch.sum(
    weights * (outputs["log_amp"] * corr_real + outputs["phase"] * corr_imag)
)
```

## 跑通标准

第一次 smoke test 重点看工程链路：

1. `n_samples` 等于配置里的采样数。
2. `n_unique` 大于 0。
3. `energy_real`、`energy_imag`、`loss_proxy` 都是有限数。
4. `train_log.csv` 正常生成。
5. checkpoint 文件正常生成。

研究收敛时，再增大 `n_samples`、`n_epochs`，并换成真实的 `qubit_op.data`。
