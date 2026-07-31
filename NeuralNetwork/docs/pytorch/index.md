# PyTorch 教程总览

PyTorch 学习的第一步不是背 API，而是建立一张命令地图：

```text
创建 tensor
  -> 调 shape / dtype / device
  -> 做索引、拼接、矩阵乘法
  -> 搭 nn.Module
  -> 计算 loss
  -> backward
  -> optimizer.step
  -> 保存、加载、推理、编译优化
```

这一页是 PyTorch 常用命令速查。每个命令后面都给出它在神经网络代码里的典型用途。

## 最小训练闭环

先看一段最短闭环：

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(3, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

x = torch.randn(32, 3)
y = torch.randn(32, 1)

model.train()
pred = model(x)
loss = loss_fn(pred, y)

optimizer.zero_grad()
loss.backward()
optimizer.step()
```

这段里已经包含 PyTorch 的核心对象：

| 对象 | 作用 |
| --- | --- |
| `torch.Tensor` | 数据和中间激活 |
| `nn.Module` | 模型和层 |
| `loss_fn` | 训练目标 |
| `loss.backward()` | 自动微分 |
| `optimizer.step()` | 参数更新 |

## Tensor 创建

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `torch.tensor(data)` | 从 Python 数据创建 tensor | 小例子、标签、手写常量 |
| `torch.zeros(shape)` | 全 0 tensor | 初始化 buffer、mask、padding |
| `torch.ones(shape)` | 全 1 tensor | mask、测试输入 |
| `torch.full(shape, value)` | 固定值填充 | 创建 `-inf` mask、常量矩阵 |
| `torch.empty(shape)` | 未初始化 tensor | 高性能底层代码，初学少用 |
| `torch.arange(n)` | 整数序列 | position id、索引 |
| `torch.linspace(a, b, steps)` | 等距浮点序列 | 画函数、测试数值 |
| `torch.eye(n)` | 单位矩阵 | 线性代数测试 |
| `torch.rand(shape)` | 均匀随机数 | 随机输入、采样测试 |
| `torch.randn(shape)` | 标准正态随机数 | 模拟输入、初始化测试 |
| `torch.randint(low, high, shape)` | 随机整数 | token id、类别标签 |
| `torch.zeros_like(x)` | 和 `x` 同形状全 0 | 保持 dtype/device 的初始化 |
| `torch.ones_like(x)` | 和 `x` 同形状全 1 | 保持 dtype/device 的 mask |
| `torch.full_like(x, value)` | 和 `x` 同形状固定值 | 常量填充 |
| `torch.randn_like(x)` | 和 `x` 同形状正态随机 | 加噪声、测试 |

对应章节：[Tensor、Shape、Dtype 与 Device](tensor_shape_dtype_device.md)。

## Shape 操作

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `x.shape` | 查看形状 | 调试所有 tensor 代码 |
| `x.ndim` | 查看维度数 | 判断 batch / sequence / channel |
| `x.numel()` | 元素总数 | 显存估算、reshape 检查 |
| `x.reshape(...)` | 改 shape | 展平、拆 batch、合并 head |
| `x.view(...)` | 改 shape，要求连续 | 性能敏感代码 |
| `x.flatten(start_dim)` | 展平部分维度 | CNN 接分类头 |
| `x.unsqueeze(dim)` | 增加长度为 1 的维度 | 补 batch 维、补 gather index 维 |
| `x.squeeze(dim)` | 删除长度为 1 的维度 | 去掉多余维度 |
| `x.transpose(dim0, dim1)` | 交换两个维度 | 矩阵转置、attention |
| `x.permute(...)` | 任意换轴 | 图像 `BHWC -> BCHW` |
| `x.contiguous()` | 变成连续内存 | `permute` 后再 `view` |

对应章节：[常用 Tensor 操作](tensor_ops.md)。

## 索引和取值

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `x[i]` | 取第 `i` 个元素或切片 | 普通索引 |
| `x[:, i]` | 取某一列或某个位置 | batch 中取同一位置 |
| `x[..., i]` | 省略前面多个维度 | 高维 tensor 末维索引 |
| `torch.gather(x, dim, index)` | 沿指定维度按 index 取值 | 取 label/token 对应 log prob |
| `x.gather(dim, index)` | `torch.gather` 的方法形式 | 自回归 `log_prob` |
| `torch.where(cond, a, b)` | 条件选择 | mask、替换异常值 |
| `x.masked_fill(mask, value)` | mask 为真处填充值 | causal mask、padding mask |

`gather` 是训练语言模型和分类模型时非常常用的命令。例如：

```python
logits = torch.randn(4, 10)
labels = torch.tensor([1, 3, 0, 9])

logp_all = torch.log_softmax(logits, dim=-1)
chosen = logp_all.gather(dim=-1, index=labels[:, None]).squeeze(-1)
```

对应章节：[gather：按索引从指定维度取值](tensor_ops.md#gather)。

## 拼接和拆分

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `torch.cat(xs, dim)` | 沿已有维度拼接 | 拼 batch、拼 head、拼 token |
| `torch.stack(xs, dim)` | 新增维度后堆叠 | 多个样本变 batch |
| `torch.chunk(x, chunks, dim)` | 尽量均分成几块 | QKV 拆分 |
| `torch.split(x, sizes, dim)` | 按指定大小拆分 | 不均匀分块 |
| `torch.unbind(x, dim)` | 沿某维拆成多个 tensor | 去掉某个维度逐项处理 |

典型 QKV 拆分：

```python
qkv = torch.randn(2, 8, 3 * 64)
q, k, v = torch.chunk(qkv, chunks=3, dim=-1)
```

对应章节：[cat 和 stack](tensor_ops.md#cat-stack)、[chunk 和 split](tensor_ops.md#chunk-split)。

## 矩阵乘法和线性代数

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `A @ B` | 矩阵乘法简写 | 线性层、attention |
| `torch.matmul(A, B)` | 支持高维 batch matmul | attention score、投影 |
| `torch.bmm(A, B)` | 3D batch 矩阵乘法 | `[B,N,D] @ [B,D,M]` |
| `torch.mm(A, B)` | 2D 矩阵乘法 | 简单线性代数 |
| `torch.einsum(pattern, ...)` | 爱因斯坦求和 | 复杂维度计算 |
| `torch.linalg.norm(x)` | 范数 | 梯度、误差、向量长度 |
| `torch.linalg.solve(A, b)` | 解线性方程 | 数值优化、线性代数实验 |

attention 里的核心：

```python
scores = torch.matmul(Q, K.transpose(-2, -1))
probs = torch.softmax(scores / (d_head ** 0.5), dim=-1)
hidden = torch.matmul(probs, V)
```

对应章节：[matmul、@ 和 bmm](tensor_ops.md#matmul-bmm)。

## 统计和归约

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `x.sum(dim)` | 求和 | loss 汇总、概率归一化检查 |
| `x.mean(dim)` | 平均 | batch loss、观测量估计 |
| `x.max(dim)` | 最大值 | logits 最大类、数值检查 |
| `x.argmax(dim)` | 最大值位置 | 预测类别 |
| `x.min(dim)` | 最小值 | 数值范围检查 |
| `x.std(dim)` | 标准差 | 数据标准化、监控 |
| `torch.isfinite(x)` | 检查是否有限 | NaN / Inf 调试 |
| `torch.isnan(x)` | 检查 NaN | 数值稳定性 |
| `torch.isinf(x)` | 检查 Inf | overflow 检查 |

常见检查：

```python
assert torch.isfinite(loss)
assert torch.isfinite(logits).all()
```

## 激活函数和概率函数

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `torch.relu(x)` | ReLU 激活 | MLP、CNN |
| `torch.sigmoid(x)` | 映射到 0 到 1 | 二分类、多标签 |
| `torch.tanh(x)` | 映射到 -1 到 1 | RNN、LSTM |
| `torch.softmax(x, dim)` | 概率归一化 | 分类概率、attention weights |
| `torch.log_softmax(x, dim)` | log 概率 | 交叉熵、log_prob |
| `torch.exp(x)` | 指数 | 概率、Boltzmann 权重 |
| `torch.log(x)` | 对数 | log likelihood |
| `torch.clamp(x, min, max)` | 截断范围 | 防止数值爆炸 |

`softmax` 必须明确 `dim`。分类和语言模型通常沿最后一维：

```python
probs = torch.softmax(logits, dim=-1)
```

## Autograd

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `requires_grad=True` | 让 tensor 记录梯度 | 可训练变量、数值实验 |
| `loss.backward()` | 反向传播 | 训练 |
| `x.grad` | 查看梯度 | 调试 |
| `torch.no_grad()` | 关闭梯度记录 | 推理、评估 |
| `torch.inference_mode()` | 更强的推理模式 | 部署推理 |
| `torch.autograd.grad(...)` | 手动求梯度 | 高阶优化、物理约束 |
| `x.detach()` | 从计算图分离 | 停止梯度 |

对应章节：[Autograd 与计算图](autograd.md)。

## nn.Module、层和损失

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `nn.Module` | 模型基类 | 自定义网络 |
| `nn.Sequential(...)` | 顺序堆层 | 简单 MLP/CNN |
| `nn.Linear` | 全连接层 | MLP、Transformer FFN |
| `nn.Conv2d` | 二维卷积 | CNN、PixelCNN |
| `nn.Embedding` | token embedding | NLP、Transformer |
| `nn.LayerNorm` | 层归一化 | Transformer |
| `nn.BatchNorm2d` | batch 归一化 | CNN |
| `nn.Dropout` | 随机失活 | 正则化 |
| `nn.CrossEntropyLoss` | 多分类交叉熵 | 分类、next-token loss |
| `nn.MSELoss` | 均方误差 | 回归 |
| `nn.BCEWithLogitsLoss` | 二分类或多标签 | logits 版本 BCE |

对应章节：[nn.Module 的核心机制](nn_module.md)、[常用层、激活函数与损失函数](layers_losses.md)。

## 优化器和训练循环

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `torch.optim.SGD` | 随机梯度下降 | 基础优化器 |
| `torch.optim.Adam` | Adam 优化器 | 常规深度学习 |
| `torch.optim.AdamW` | decoupled weight decay | Transformer、大模型常用 |
| `optimizer.zero_grad()` | 清空旧梯度 | 每步 backward 前 |
| `loss.backward()` | 计算梯度 | 训练 |
| `optimizer.step()` | 更新参数 | 训练 |
| `scheduler.step()` | 更新学习率 | warmup、cosine decay |
| `torch.nn.utils.clip_grad_norm_` | 梯度裁剪 | RNN、大模型稳定训练 |

对应章节：[训练循环：forward、backward、optimizer.step](training_loop.md)。

## Dataset 和 DataLoader

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `TensorDataset(X, y)` | 用 tensor 构造数据集 | 小实验 |
| `DataLoader(dataset, batch_size, shuffle)` | 批量加载数据 | 训练循环 |
| `Dataset` | 自定义数据集基类 | 真实项目 |
| `random_split(dataset, lengths)` | 划分数据集 | train/val split |

常见导入：

```python
from torch.utils.data import Dataset, DataLoader, TensorDataset
```

## 保存、加载和模式切换

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `model.state_dict()` | 取模型参数字典 | 保存权重 |
| `model.load_state_dict(state)` | 加载参数 | 恢复模型 |
| `torch.save(obj, path)` | 保存对象 | checkpoint |
| `torch.load(path, map_location=...)` | 加载对象 | 推理、恢复训练 |
| `model.train()` | 训练模式 | Dropout / BatchNorm 训练行为 |
| `model.eval()` | 推理模式 | 关闭 Dropout 随机性等 |
| `with torch.no_grad()` | 不记录梯度 | 推理省显存 |

对应章节：[保存、加载与 train/eval 模式](state_dict_train_eval.md)。

## Device、CUDA 和混合精度

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `torch.cuda.is_available()` | 检查 CUDA | 选择 device |
| `torch.device("cuda")` | 创建设备对象 | 模型迁移 |
| `x.to(device)` | tensor 移动到设备 | CPU/GPU 切换 |
| `model.to(device)` | 模型移动到设备 | GPU 训练 |
| `x.cpu()` | 移回 CPU | 保存、转 NumPy |
| `x.cuda()` | 移到 GPU | 快速写法 |
| `torch.cuda.synchronize()` | 等待 GPU 完成 | 准确计时 |
| `torch.autocast(...)` | 自动混合精度 | FP16/BF16 训练和推理 |

更完整的 FP32、FP16、BF16、量化和显存讨论见 [数值精度](../numerical_precision.md)。

## 编译和性能

| 命令 | 作用 | 常见用途 |
| --- | --- | --- |
| `torch.compile(model)` | 编译优化模型执行 | PyTorch 2.x 性能优化 |
| `@torch.compile` | 编译函数 | 小函数或模块 forward |
| `torch.profiler.profile(...)` | 性能分析 | 找瓶颈 |
| `torch.utils.benchmark` | 微基准测试 | 比较小算子性能 |

`torch.compile` 应该放在正确性确认之后使用，不是基础语法替代品。

对应章节：[torch.compile：从 eager mode 到编译加速](torch_compile.md)。

## 一句话路线

PyTorch 代码可以按下面这条线读：

```text
Tensor shape / dtype / device
  -> Tensor 操作
  -> nn.Module
  -> loss
  -> autograd
  -> optimizer
  -> checkpoint
  -> eval / inference
  -> compile / performance
```

如果某段代码看不懂，先不要问“这个 API 名字是什么意思”，先问：

```text
它输入 shape 是什么？
它沿哪个维度操作？
它输出 shape 是什么？
它是否参与梯度？
它在哪个 device 上？
```
