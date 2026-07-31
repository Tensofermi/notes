# 工程正确性与性能验证

神经网络工程里的验证不是只跑通一个 notebook。模型从研究代码走向训练任务、推理引擎和在线服务时，需要分层验证：

```text
数学正确性
  -> 张量 shape 和 dtype
  -> 单机训练闭环
  -> 分布式一致性
  -> 数值稳定性
  -> 性能指标
  -> 推理服务稳定性
```

这页给出一份通用清单。它不绑定某个具体项目，而是帮助你判断一个神经网络系统是否“真的可用”。

## 第一层：静态检查

静态检查的目标是尽早发现低级错误。

常见检查：

```bash
python -m compileall .
python -m pytest tests -q
```

如果项目有类型检查或格式检查，还应运行：

```bash
ruff check .
mypy .
```

重点看：

- import 是否完整。
- 配置字段是否存在。
- 测试是否依赖本机绝对路径。
- CPU 环境下是否能完成最小测试。
- 随机种子是否能固定。

静态检查不能证明模型正确，但能防止大量低成本错误进入后续昂贵流程。

## 第二层：Shape、Dtype 和 Device

大部分深度学习 bug 都可以先从三个问题排查：

```text
shape 对不对
dtype 对不对
device 对不对
```

建议在关键边界处检查：

```python
assert input_ids.ndim == 2
assert input_ids.dtype == torch.long
assert logits.shape[:2] == input_ids.shape
assert logits.device == input_ids.device
```

常见错误：

| 错误 | 表现 |
| --- | --- |
| labels 没有 shift | loss 看似下降，但学习目标错位 |
| mask shape 广播错 | attention 泄露未来信息或错误屏蔽 |
| FP16 下做不稳定归一化 | NaN、Inf、loss spike |
| CPU tensor 混入 GPU 计算 | runtime device mismatch |
| `view` 用在非 contiguous tensor | shape 逻辑错误或直接报错 |

这层验证应当足够便宜，可以在每次改动后运行。

## 第三层：最小 Forward / Backward

任何模型在进入长训练前，都应该先跑一个极小 batch：

```python
model.train()
batch = next(iter(loader))
loss = model(**batch).loss
assert torch.isfinite(loss)
loss.backward()

for name, p in model.named_parameters():
    if p.requires_grad:
        assert p.grad is not None, name
        assert torch.isfinite(p.grad).all(), name
```

这一步验证：

- forward 能跑通。
- loss 是有限数。
- 需要训练的参数确实有梯度。
- 梯度没有 NaN / Inf。

如果这里失败，不应该继续调分布式、compile 或推理引擎。先回到模型和数据。

## 第四层：Overfit 一个小 batch

一个很实用的 sanity check：

> 让模型在一个很小 batch 上训练到 loss 明显下降。

如果小 batch 都无法过拟合，通常说明：

- labels 错了。
- loss mask 错了。
- optimizer 没有更新参数。
- 学习率极端不合适。
- 某些参数被冻结。
- forward 里错误使用了 `detach()` 或 `no_grad()`。

这一步不验证泛化，只验证训练闭环有能力把信号写入参数。

## 第五层：数值稳定性

混合精度、长序列和大 batch 都会放大数值问题。

必须监控：

```text
loss
grad_norm
learning_rate
activation max / min
NaN / Inf count
overflow / skipped step
```

常见判断：

| 现象 | 可能原因 |
| --- | --- |
| loss 突然变 NaN | 学习率过大、FP16 overflow、数据异常 |
| grad norm 爆炸 | 初始化、长序列、未裁剪梯度 |
| loss 长期不变 | 参数未更新、mask 全错、学习率太低 |
| BF16 正常但 FP16 崩 | FP16 指数范围不够，需 loss scaling |
| eval loss 比 train loss 异常低 | train/eval 模式或 dropout 处理错误 |

这部分可以结合 [数值精度](numerical_precision.md) 一起读。

## 第六层：分布式一致性

单卡正确不代表多卡正确。

分布式训练要额外验证：

- 单卡和多卡在等效 global batch 下 loss 是否接近。
- gradient accumulation 是否和真实大 batch 等价。
- DDP 参数是否在各 rank 同步。
- FSDP / ZeRO checkpoint 是否能保存和恢复。
- sampler 是否正确按 rank 切分数据。
- 所有 rank 是否都进入同样的 collective 调用。

典型问题：

| 问题 | 表现 |
| --- | --- |
| 某个 rank 数据为空 | 训练卡死或 loss 异常 |
| collective 调用不一致 | NCCL hang |
| 随机种子没有按 rank 设置 | 数据增强或 dropout 行为异常 |
| checkpoint 只保存 rank 0 局部分片 | 恢复后权重缺失 |

分布式 bug 的成本高，必须先用小模型、小数据、少 GPU 做 smoke test。

## 第七层：Checkpoint 恢复

训练任务如果不能恢复，就不能算工程可用。

最小验证：

```text
训练 N step
  -> 保存 checkpoint
  -> 重新启动
  -> 从 checkpoint 继续训练
  -> 检查 loss、step、lr、optimizer state 是否连续
```

需要保存的不只是模型权重：

| 状态 | 为什么需要 |
| --- | --- |
| model weights | 参数本体 |
| optimizer state | Adam 动量决定后续更新 |
| scheduler state | 学习率阶段不能乱 |
| grad scaler | mixed precision 恢复 |
| random state | 复现实验和数据顺序 |
| dataloader progress | 避免重复或跳过数据 |
| distributed metadata | 分片 checkpoint 恢复 |

推理加载则可以只加载权重，但也要验证 tokenizer 和 config 是否匹配。

## 第八层：性能验证

性能验证不要只看“跑得快不快”，要拆指标。

训练侧：

| 指标 | 含义 |
| --- | --- |
| tokens/sec | 训练吞吐 |
| step time | 每步耗时 |
| GPU utilization | GPU 是否空等 |
| MFU | 模型 FLOPs 利用率 |
| dataloader time | 数据管线是否拖慢 |
| communication time | 多卡通信开销 |
| peak memory | 峰值显存 |

推理侧：

| 指标 | 含义 |
| --- | --- |
| TTFT | 首 token 延迟 |
| TPOT | 每个输出 token 延迟 |
| output tokens/sec | 生成吞吐 |
| request throughput | 请求吞吐 |
| KV cache usage | 推理显存核心项 |
| batch size / concurrency | 调度能力 |

性能测试要有 warmup。涉及 `torch.compile`、CUDA graph 或推理引擎时，第一次运行通常不代表稳定性能。

## 第九层：推理正确性

推理路径经常和训练 forward 不完全相同，尤其使用 KV cache、量化、导出图或推理引擎时。

需要比较：

- eager PyTorch 输出。
- `torch.compile` 输出。
- FP16 / BF16 输出。
- INT8 / INT4 量化输出。
- KV cache 开启与关闭的输出。
- 推理引擎输出。

常见校验：

```python
torch.testing.assert_close(
    logits_ref,
    logits_opt,
    rtol=1e-2,
    atol=1e-2,
)
```

容差要根据 dtype 和算子实现调整。量化后不能期待逐元素完全一致，但应检查：

- top-k token 是否基本一致。
- perplexity 或任务指标下降是否可接受。
- 长上下文下输出是否异常。
- batch 推理和单条推理是否一致。

## 第十层：服务稳定性

模型上线后，还要验证系统行为。

服务层检查：

| 检查 | 目的 |
| --- | --- |
| 并发压测 | 找到吞吐和延迟拐点 |
| 长 prompt 压测 | 验证 KV cache 和显存上限 |
| 超时和取消 | 用户断开后是否释放资源 |
| OOM 恢复 | worker 是否能重启并隔离失败 |
| 流式输出 | token 是否稳定返回 |
| 限流 | 高峰期是否保护系统 |
| 灰度发布 | 新模型是否可逐步放量和回滚 |
| 监控告警 | 错误率、延迟、显存、GPU 利用率是否可见 |

这层问题已经不是单纯机器学习问题，而是服务工程问题。

## 推荐验证顺序

不要一开始就跑大任务。推荐顺序：

```text
unit test
  -> tiny forward/backward
  -> overfit small batch
  -> single GPU smoke
  -> multi GPU smoke
  -> checkpoint resume
  -> mixed precision run
  -> performance benchmark
  -> inference equivalence
  -> serving pressure test
```

每一层都应该有明确通过标准。没有通过标准的测试，只是在消耗 GPU 时间。

## 文档站构建

本笔记站本身也需要构建验证：

```bash
python -m mkdocs build --strict
```

如果公式、导航、链接或代码块破坏了文档构建，应先修正文档，再发布。

## 关联阅读

- [工程导读：从模型代码到系统代码](code_walkthrough.md)
- [工程公式速查](formula_cheatsheet.md)
- [大模型 Infra 全景：从硬件到服务](infra_overview.md)
- [数值精度](numerical_precision.md)
- [torch.compile：从 eager mode 到编译加速](pytorch/torch_compile.md)
