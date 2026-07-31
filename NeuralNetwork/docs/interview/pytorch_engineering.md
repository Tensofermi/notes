# PyTorch 与工程实现题

PyTorch 题的核心是：能否把公式落成可靠代码。面试里常见追问包括 shape、dtype、device、autograd、`nn.Module`、训练模式和保存加载。

## 题目：`view` 和 `reshape` 有什么区别？

**来源背景**：PyTorch tensor 操作面试题改写。

**考点定位**：内存连续性、shape 变换。

**先给结论**：`view` 要求 tensor 内存连续；`reshape` 会尽量返回 view，必要时复制数据。

**解题思路**：

```python
x = torch.randn(2, 3, 4)
y = x.transpose(1, 2)

# y.view(2, 12) 可能报错，因为 y 不连续
z = y.reshape(2, 12)
```

转置、permute 后 tensor 的 stride 改变，可能不再 contiguous。此时要么使用 `reshape`，要么：

```python
z = y.contiguous().view(2, 12)
```

**易错点**：

- `reshape` 可能复制数据，不能总是假设零开销。
- shape 对了不代表语义对了，尤其是 batch 和 sequence 维度。

**关联阅读**：[常用 Tensor 操作](../pytorch/tensor_ops.md)。

## 题目：Broadcasting 是什么？

**来源背景**：PyTorch / NumPy 基础题改写。

**考点定位**：张量形状、自动扩展。

**先给结论**：broadcasting 允许不同 shape 的 tensor 在兼容维度上自动扩展，而不实际复制所有数据。

**解题思路**：

例如：

```python
x = torch.randn(2, 3, 4)
bias = torch.randn(4)
y = x + bias
```

`bias` 的 shape `[4]` 会被看成 `[1, 1, 4]`，再扩展到 `[2, 3, 4]`。

规则从右往左对齐维度，每一维要么相等，要么其中一个是 1。

**易错点**：

- broadcasting 可能掩盖 shape bug。
- 需要明确哪个维度是 batch、sequence、channel。

**关联阅读**：[Broadcasting](../pytorch/tensor_ops.md#broadcasting)。

## 题目：为什么每轮训练前要 `optimizer.zero_grad()`？

**来源背景**：PyTorch 训练循环高频题改写。

**考点定位**：梯度累积、训练循环。

**先给结论**：PyTorch 默认梯度会累积到 `.grad` 上，不清零就会把多轮 backward 的梯度加在一起。

**解题思路**：

标准循环：

```python
optimizer.zero_grad()
pred = model(x)
loss = criterion(pred, y)
loss.backward()
optimizer.step()
```

如果不清零，第二次 `backward()` 后：

```text
p.grad = 第一轮梯度 + 第二轮梯度
```

这通常不是想要的更新方向。

**易错点**：

- 梯度累积本身可以用于模拟大 batch，但要有意控制。
- `zero_grad(set_to_none=True)` 可以减少显存写入，行为略有差异。

**关联阅读**：[训练循环](../pytorch/training_loop.md)。

## 题目：`model.train()`、`model.eval()` 和 `torch.no_grad()` 是一回事吗？

**来源背景**：米哈游 / 字节工程面高频题改写。

**考点定位**：训练模式、推理模式、计算图。

**先给结论**：不是一回事。`train/eval` 控制模块行为；`no_grad` 控制是否记录计算图。

**解题思路**：

`model.eval()` 影响：

- Dropout 关闭随机置零。
- BatchNorm 使用 running statistics。

`torch.no_grad()` 影响：

- 不构建 autograd graph。
- 降低显存占用。
- 加快推理。

推理常用：

```python
model.eval()
with torch.no_grad():
    y = model(x)
```

**易错点**：

- 只写 `no_grad()` 不会关闭 Dropout。
- 只写 `eval()` 仍然可能记录计算图。

**关联阅读**：[保存、加载与 train/eval 模式](../pytorch/state_dict_train_eval.md)。

## 题目：`torch.compile()` 是什么？为什么第一次运行可能更慢？

**来源背景**：PyTorch 2.x 工程优化题改写。

**考点定位**：eager mode、图捕获、编译开销、性能测试。

**先给结论**：`torch.compile()` 会尝试把 PyTorch 运算区域捕获成图并交给后端编译优化；第一次运行可能包含图捕获和 kernel 编译开销，所以真正的加速通常要看 warmup 之后的重复调用。

**解题思路**：

普通 PyTorch 默认是 eager mode：

```text
Python 调用一个算子
  -> 执行
  -> 返回中间 tensor
  -> Python 再调用下一个算子
```

`torch.compile()` 的思路是：

```text
捕获可编译区域
  -> 生成优化后的执行代码
  -> 后续相同输入模式复用编译结果
```

最小用法：

```python
model = MyModel()
compiled_model = torch.compile(model)

# 第一次可能触发编译
y = compiled_model(x)

# 后续调用才更能体现加速
y = compiled_model(x)
```

如果在 CUDA 上测性能，要注意同步：

```python
torch.cuda.synchronize()
t0 = time.perf_counter()
for _ in range(100):
    compiled_model(x)
torch.cuda.synchronize()
t1 = time.perf_counter()
```

**易错点**：

- 只测第一次调用会把编译开销算进去。
- 输入 shape 频繁变化可能导致重新编译。
- `print`、`.item()`、文件 IO、复杂 Python 控制流可能造成 graph break。
- `torch.compile()` 不替代 `model.eval()` 和 `torch.no_grad()`。
- 先保证 eager mode 正确，再考虑 compile。

**关联阅读**：[torch.compile：从 eager mode 到编译加速](../pytorch/torch_compile.md)。

## 题目：`nn.Module` 如何知道哪些参数要训练？

**来源背景**：PyTorch 模块机制面试题改写。

**考点定位**：参数注册、子模块嵌套。

**先给结论**：赋值为 `nn.Parameter` 或 `nn.Module` 的属性会被自动注册，出现在 `model.parameters()` 和 `state_dict()` 中。

**解题思路**：

```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(4, 2)
        self.scale = nn.Parameter(torch.ones(()))

    def forward(self, x):
        return self.scale * self.fc(x)
```

`self.fc` 是子模块，`self.scale` 是参数，都会被注册。

**易错点**：

- 普通 tensor 属性不会自动作为参数训练。
- Python list 中的子模块不会自动注册，应使用 `nn.ModuleList`。
- 不需要手动调用 `forward`，应调用 `model(x)`。

**关联阅读**：[nn.Module 的核心机制](../pytorch/nn_module.md)。

## 题目：`state_dict` 保存的是什么？

**来源背景**：模型保存加载工程题改写。

**考点定位**：参数、buffer、checkpoint。

**先给结论**：`state_dict` 保存模型参数和 buffer，例如权重、bias、BatchNorm running mean 等。

**解题思路**：

保存：

```python
torch.save(model.state_dict(), "model.pt")
```

加载：

```python
model = MyModel()
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()
```

训练 checkpoint 通常还保存：

```python
{
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "step": step,
}
```

**易错点**：

- 只保存模型参数不能恢复 optimizer 动量。
- 加载后做推理要切 `eval()`。
- `map_location` 可以解决设备不一致问题。

**关联阅读**：[保存、加载与 train/eval 模式](../pytorch/state_dict_train_eval.md)。

## 题目：Autograd 计算图什么时候会断？

**来源背景**：PyTorch 调试题改写。

**考点定位**：计算图、detach、不可导操作。

**先给结论**：使用 `detach()`、`.item()`、转 NumPy、在 `no_grad` 中计算、或使用不可导操作，都可能断开梯度路径。

**解题思路**：

下面代码中 `y` 没有梯度：

```python
x = torch.tensor(2.0, requires_grad=True)
y = (x * x).detach()
z = y * 3
```

因为 `detach()` 返回不跟踪梯度的新 tensor。

**易错点**：

- `.item()` 会把 tensor 变成 Python 标量。
- 记录 loss 日志时可以 `.item()`，但不能把它再拿去构造训练 loss。
- inplace 修改参与梯度的 tensor 可能破坏反向传播。

**关联阅读**：[Autograd 与计算图](../pytorch/autograd.md)。

## 题目：如何定位 device mismatch？

**来源背景**：深度学习工程调试题改写。

**考点定位**：CPU/GPU、模型和数据设备一致性。

**先给结论**：模型参数、输入 tensor、标签 tensor、临时创建 tensor 必须在同一 device 上。

**解题思路**：

常见 bug：

```python
device = torch.device("cuda")
model.to(device)
x = x.to(device)

# 错误：forward 里新建了 CPU tensor
mask = torch.ones(seq_len, seq_len)
```

应写：

```python
mask = torch.ones(seq_len, seq_len, device=x.device)
```

**易错点**：

- 在 forward 里创建 tensor 时要指定 device。
- buffer 应使用 `register_buffer`，跟随模型迁移。

**关联阅读**：[Tensor、Shape、Dtype 与 Device](../pytorch/tensor_shape_dtype_device.md)。
