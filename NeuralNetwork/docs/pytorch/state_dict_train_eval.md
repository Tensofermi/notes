# 保存、加载与 train/eval 模式

训练得到的模型参数需要保存。PyTorch 推荐保存 `state_dict()`，而不是直接保存整个模型对象。

## state_dict

`state_dict()` 是一个字典，保存参数和 buffer。

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(3, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
)

state = model.state_dict()
for key, value in state.items():
    print(key, value.shape)
```

输出类似：

```text
0.weight torch.Size([8, 3])
0.bias torch.Size([8])
2.weight torch.Size([1, 8])
2.bias torch.Size([1])
```

## 保存模型参数

```python
torch.save(model.state_dict(), "model.pt")
```

加载：

```python
new_model = nn.Sequential(
    nn.Linear(3, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
)

state = torch.load("model.pt", map_location="cpu")
new_model.load_state_dict(state)
```

模型结构必须匹配，否则参数 shape 对不上。

## 保存 checkpoint

训练中通常还保存 optimizer 状态、epoch、loss 等：

```python
checkpoint = {
    "epoch": 10,
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
}

torch.save(checkpoint, "checkpoint.pt")
```

恢复：

```python
ckpt = torch.load("checkpoint.pt", map_location="cpu")
model.load_state_dict(ckpt["model"])
optimizer.load_state_dict(ckpt["optimizer"])
start_epoch = ckpt["epoch"] + 1
```

## 为什么不直接保存整个模型

直接保存：

```python
torch.save(model, "model_full.pt")
```

会把 Python 类路径也序列化进去。代码结构变了以后可能无法加载。

保存 `state_dict` 更稳，因为它只保存张量数据。

## train 和 eval

`model.train()` 和 `model.eval()` 不控制是否计算梯度，它们控制模块行为。

```python
dropout = nn.Dropout(p=0.5)
x = torch.ones(10)

dropout.train()
print(dropout(x))

dropout.eval()
print(dropout(x))
```

训练模式下 Dropout 随机置零。eval 模式下 Dropout 不再随机置零。

BatchNorm 也会受影响：训练时使用 batch 统计量并更新 running stats，eval 时使用保存的 running stats。

## no_grad 和 eval 的区别

`eval()` 改变模块行为。  
`torch.no_grad()` 关闭梯度记录。

推理时通常两个都用：

```python
model.eval()
with torch.no_grad():
    y = model(x)
```

只写 `model.eval()` 仍然可能构建计算图。  
只写 `torch.no_grad()` 不会切换 Dropout / BatchNorm 行为。

如果还想进一步优化执行速度，可以在模型正确性确认后使用 `torch.compile()`。它不替代 `eval()` 或 `no_grad()`，而是尝试把模型中的 PyTorch 运算区域编译加速。详见 [torch.compile：从 eager mode 到编译加速](torch_compile.md)。

## 设备迁移

加载到 GPU：

```python
device = "cuda" if torch.cuda.is_available() else "cpu"

model.load_state_dict(torch.load("model.pt", map_location=device))
model.to(device)
```

更稳妥的写法是先加载到 CPU，再移动：

```python
state = torch.load("model.pt", map_location="cpu")
model.load_state_dict(state)
model.to(device)
```

## 和 NNQS 工程的关系

NNQS 训练中 checkpoint 不只保存网络参数，还应保存：

- epoch。
- optimizer state。
- 配置。
- 训练日志。
- 随机种子或采样状态。

因为 VMC 是闭环训练，恢复训练时需要尽量恢复完整状态，避免只恢复波函数却丢失优化器动量。
