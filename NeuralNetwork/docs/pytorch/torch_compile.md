# torch.compile：从 eager mode 到编译加速

`torch.compile()` 是 PyTorch 2.x 引入的模型加速入口。它的目标不是改变模型数学形式，而是把一段 PyTorch 代码捕获成更容易优化的计算图，再交给后端编译器生成更高效的执行代码。

可以先用一句话理解：

> 普通 PyTorch 是边执行 Python 边调用算子；`torch.compile()` 尝试把可优化的 PyTorch 运算区域抓成图，减少 Python 开销，并融合部分算子。

官方文档把 `torch.compile` 描述为 PyTorch 2.x 的核心编译功能，底层通常涉及 TorchDynamo 的图捕获和 TorchInductor 的代码生成。更完整的接口细节见 [PyTorch `torch.compile` API](https://docs.pytorch.org/docs/stable/generated/torch.compile.html) 和 [torch.compiler 文档](https://docs.pytorch.org/docs/stable/torch.compiler.html)。

## eager mode 是什么

PyTorch 默认是 eager mode，也就是写一行、执行一行：

```python
import torch

x = torch.randn(4, 8)
w = torch.randn(8, 16)

y = x @ w
z = torch.relu(y)
print(z.shape)
```

这种模式的好处是：

- 容易调试。
- Python 控制流自然可用。
- 出错位置通常比较直观。

缺点是：如果模型由很多小算子组成，Python 调度开销和中间 tensor 读写会变成性能瓶颈。

`torch.compile()` 试图在不放弃 PyTorch 动态体验的前提下，把稳定的计算区域编译优化。

## 最小用法

最常见写法是把 `nn.Module` 包一层：

```python
import torch
from torch import nn

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Linear(64, 4),
        )

    def forward(self, x):
        return self.net(x)

model = MLP()
compiled_model = torch.compile(model)

x = torch.randn(32, 16)
y = compiled_model(x)
print(y.shape)
```

也可以编译普通函数：

```python
import torch

@torch.compile
def f(x, w):
    return torch.relu(x @ w)

x = torch.randn(32, 16)
w = torch.randn(16, 64)

y = f(x, w)
print(y.shape)
```

PyTorch 也提供 `nn.Module.compile()` 形式，用于原地编译模块：

```python
model = MLP()
model.compile()

y = model(torch.randn(32, 16))
```

初学时更推荐 `compiled_model = torch.compile(model)`，因为它更容易保留原始模型对象，方便调试和对照。

## 它到底优化了什么

普通 eager 执行可以粗略理解为：

```text
Python 调用 matmul
  -> 返回中间 tensor
Python 调用 bias add
  -> 返回中间 tensor
Python 调用 relu
  -> 返回中间 tensor
Python 调用下一层
  -> ...
```

`torch.compile()` 会尝试变成：

```text
捕获一段可编译计算图
  -> 交给 backend
  -> 生成更高效代码
  -> 后续相同模式的输入复用编译结果
```

典型收益来自：

- 减少 Python 调度开销。
- 融合相邻算子，减少中间 tensor 读写。
- 对特定硬件生成更合适的 kernel。
- 对重复执行的模型 forward / training step 缓存编译结果。

它不是魔法。模型中如果大部分时间已经花在高度优化的大矩阵乘法上，收益可能有限；如果模型有很多小算子、Python 开销明显、shape 比较稳定，收益更容易出现。

## 第一次会慢：编译开销

`torch.compile()` 通常是懒编译。第一次调用时需要捕获图、生成代码和编译 kernel，所以第一次运行可能明显变慢：

```python
compiled_model = torch.compile(model)

# 第一次：可能包含编译开销
y = compiled_model(x)

# 后续：复用编译结果，才体现加速
y = compiled_model(x)
```

所以测性能时不能只测第一次。

更合理的 benchmark 写法是：

```python
import time
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(1024, 4096),
    nn.GELU(),
    nn.Linear(4096, 1024),
)

x = torch.randn(64, 1024)
compiled_model = torch.compile(model)

# warmup，触发编译
for _ in range(5):
    compiled_model(x)

t0 = time.perf_counter()
for _ in range(50):
    compiled_model(x)
t1 = time.perf_counter()

print((t1 - t0) / 50)
```

如果在 CUDA 上测，还需要同步，否则计时只测到异步 launch：

```python
if torch.cuda.is_available():
    torch.cuda.synchronize()

t0 = time.perf_counter()
for _ in range(50):
    compiled_model(x)

if torch.cuda.is_available():
    torch.cuda.synchronize()

t1 = time.perf_counter()
```

## 训练中怎么用

可以直接编译模型，然后照常训练：

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(16, 64),
    nn.ReLU(),
    nn.Linear(64, 1),
)

model = torch.compile(model)

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

x = torch.randn(128, 16)
y = torch.randn(128, 1)

for step in range(20):
    pred = model(x)
    loss = loss_fn(pred, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(loss.item())
```

这里 autograd 仍然工作。编译器会围绕 forward 和 backward 做图捕获与优化。不过，官方文档也专门提醒过：`torch.compile` 下的 autograd 语义在一些高级用法中可能和 eager mode 不完全一样，复杂自定义梯度、高阶导数、动态 backward 行为需要额外小心。相关说明见 [torch.compile autograd semantics](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/torch.compiler_backward.html)。

实践建议：

- 先保证 eager mode 代码正确。
- 再加 `torch.compile()`。
- 如果结果变慢或报错，先退回 eager mode 定位问题。
- 对复杂训练代码，优先编译纯模型 forward，而不是把所有日志、采样、文件写入逻辑都放进编译区域。

## 推理中怎么用

推理时常见写法：

```python
model.eval()
model = torch.compile(model)

with torch.no_grad():
    y = model(x)
```

如果模型会被反复调用很多次，编译开销可以被后续请求摊薄，`torch.compile()` 更可能划算。

如果只是临时跑一次脚本，例如只预测一张图片，编译开销可能大于加速收益。

推理部署时还要区分几类工具：

| 工具 | 主要作用 |
| --- | --- |
| `model.eval()` | 切换 Dropout / BatchNorm 等模块行为 |
| `torch.no_grad()` | 关闭梯度记录，减少显存 |
| `torch.compile()` | 捕获和编译可优化计算区域 |
| AMP / 低精度 | 使用 FP16 / BF16 等降低计算和显存成本 |
| 量化 | 用 INT8 / INT4 等压缩权重和计算，主要用于推理 |

它们解决的问题不同，可以组合使用。

## 常用参数

`torch.compile` 的常见参数包括：

```python
compiled_model = torch.compile(
    model,
    backend="inductor",
    mode=None,
    fullgraph=False,
    dynamic=None,
)
```

常见含义：

| 参数 | 含义 |
| --- | --- |
| `backend` | 编译后端，默认通常是 `inductor` |
| `mode` | 编译策略，例如默认模式、减少 overhead、最大化 autotune 等 |
| `fullgraph` | 是否要求整段代码捕获成一个完整图 |
| `dynamic` | 是否尝试支持动态 shape |

常见 `mode`：

| mode | 直觉 |
| --- | --- |
| `None` | 默认策略 |
| `"reduce-overhead"` | 尽量减少 Python / launch 开销，常用于小 batch 或推理 |
| `"max-autotune"` | 花更多编译时间寻找更快 kernel，适合长期重复运行 |

这些模式不保证总是更快。正确做法是用你的真实模型、真实 batch size 和真实硬件测。

## graph break 是什么

`torch.compile()` 不是把任意 Python 程序都无条件变成一个大图。遇到难以捕获的 Python 行为时，编译器可能把图断开，这叫 graph break。

例如：

```python
def f(x):
    print(x.shape)  # Python 副作用，可能导致 graph break
    return torch.relu(x)

compiled_f = torch.compile(f)
```

常见 graph break 来源：

- `print`、日志、文件 IO。
- 把 tensor 转成 Python 标量后参与控制流，例如 `.item()`。
- 复杂 Python 数据结构操作。
- 某些暂不支持的算子或第三方扩展。
- 输入 shape / dtype / device 频繁变化。

graph break 不一定是错误，但会降低优化效果。写可编译模型时，核心 forward 最好保持“tensor 输入，tensor 输出，中间主要是 tensor 运算”。

## 动态 shape 和重新编译

如果输入 shape 频繁变化，编译器可能需要重新编译多个版本。例如：

```python
compiled_model(torch.randn(32, 16))
compiled_model(torch.randn(64, 16))
compiled_model(torch.randn(128, 16))
```

不同 batch size、sequence length 可能触发新的编译路径。官方 API 文档中也说明，编译结果会被缓存，但 guard failure 可能导致重新编译。

对 Transformer 来说，动态 sequence length 很常见。工程上常用几种办法：

- 固定或分桶 sequence length。
- 用 padding 把长度整理到有限几个档位。
- 对推理服务按长度分组 batch。
- 需要时尝试 `dynamic=True`，但仍以实测为准。

## 保存模型时要注意什么

`torch.compile()` 主要影响执行方式，不改变模型参数本身。保存模型时，通常仍然保存原始模型的 `state_dict`：

```python
raw_model = MLP()
compiled_model = torch.compile(raw_model)

torch.save(raw_model.state_dict(), "model.pt")
```

如果代码里只保留了 compiled model，很多情况下也能访问参数，但工程上更清晰的做法是保留原始模型对象，保存和加载仍然围绕 `state_dict`。

推荐流程：

```text
定义原始模型
  -> 加载 state_dict
  -> 切换 eval 或 train
  -> 按需要 torch.compile
  -> 执行训练或推理
```

不要把 `torch.compile()` 当成模型文件格式。它不是 `torch.save` 的替代品。

## 什么时候适合用

适合尝试：

- 模型会重复运行很多次。
- GPU 上 Python overhead 或 kernel launch overhead 明显。
- forward 主要由 PyTorch tensor 运算构成。
- shape 相对稳定。
- 你愿意做 benchmark 和回退方案。

不一定适合：

- 只运行一次的小脚本。
- forward 里混了大量 Python 控制流、日志和 IO。
- 输入 shape 极其不稳定。
- 代码还没有在 eager mode 下验证正确。
- 正在调试复杂 autograd 问题。

## 和 TorchScript、FX、ONNX 的关系

这些工具都和“图”有关，但目标不同：

| 工具 | 主要用途 |
| --- | --- |
| `torch.compile()` | 在 PyTorch 内部加速训练或推理 |
| TorchScript | 早期 PyTorch 图化和部署方案，现在很多场景被新工具替代 |
| FX | 捕获和变换 PyTorch graph 的工具层 |
| `torch.export` | 导出更稳定、更可分析的图表示 |
| ONNX | 跨框架部署交换格式 |

初学时可以先记住：

> `torch.compile()` 主要是“让 PyTorch 程序跑得更快”；ONNX / export 更偏“把模型带到别的运行环境”。

## 最小排查清单

如果 `torch.compile()` 没有带来收益，按这个顺序排查：

1. eager mode 是否正确。
2. 是否只测了第一次调用，把编译开销算进去了。
3. 是否在 CUDA 计时时忘了 `torch.cuda.synchronize()`。
4. 输入 shape 是否频繁变化，导致反复重新编译。
5. forward 里是否有 `print`、`.item()`、IO 或复杂 Python 控制流。
6. 模型是否主要由已经高度优化的大矩阵乘法构成，导致额外收益有限。
7. 是否应该尝试 `mode="reduce-overhead"` 或 `mode="max-autotune"`。

## 招聘考点

!!! question "代表题：`torch.compile()` 为什么第一次运行可能更慢？"
    因为第一次调用通常包含图捕获、代码生成、kernel 编译和 autotune 等开销。它的收益主要来自后续重复调用时复用编译结果。如果只跑一次，编译成本可能大于加速收益。

!!! question "代表题：`torch.compile()`、`model.eval()` 和 `torch.no_grad()` 有什么区别？"
    `model.eval()` 控制模块行为，`torch.no_grad()` 控制是否记录计算图，`torch.compile()` 控制执行优化方式。三者不是替代关系，推理时经常组合使用：先 `eval()`，再按需要 `compile()`，执行时放在 `no_grad()` 或 `inference_mode()` 中。

!!! question "代表题：什么是 graph break？"
    graph break 是编译器无法继续捕获当前 Python / PyTorch 程序为同一个计算图时发生的断点。它不一定导致程序错误，但会让编译区域变碎，从而降低优化效果。常见原因包括 `.item()` 后参与 Python 控制流、打印日志、文件 IO、复杂数据结构操作和暂不支持的算子。

## 小结

`torch.compile()` 是 PyTorch 2.x 以后非常重要的工程工具。它的位置应该放在“代码已经正确之后的性能优化层”，而不是基础语法层。

最稳妥的使用原则是：

```text
先写清楚 eager PyTorch
  -> 验证数值正确
  -> 加 torch.compile
  -> warmup 后 benchmark
  -> 观察 graph break / recompilation
  -> 决定是否保留
```

如果只记一句话：

> `torch.compile()` 不负责让错误代码变正确，它负责尝试让已经正确、可捕获、会重复运行的 PyTorch 代码跑得更快。
