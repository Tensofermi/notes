# I/O、性能与并行 { #7-io }

## 用一张图标出每一份数据在哪里

跟一次[CPU 发起的设备读取](io_interrupt_dma_storage.md)，看数据实际走过的[设备与链路](device_data_paths.md)。理解了搬运后，再看[多个核心为何争同一缓存块](parallelism_consistency.md)，以及[把计算交给 GPU](gpu_and_server_topology.md)何时值得。

CPU 只是系统的一部分。键盘、网卡、磁盘和 SSD 速度不同、事件异步，必须通过总线、控制器、中断和 DMA 协作；当单核性能受到功耗与并行度限制后，SIMD 和多核又把问题扩展到多个执行者之间。

## 本章内容

- [总线、中断、DMA 与存储设备](io_interrupt_dma_storage.md)：比较轮询、中断和 DMA，并理解 HDD、SSD 的物理约束。
- [性能公式与 Amdahl 定律](performance_amdahl.md)：建立可计算的延迟、吞吐量、CPI 与加速上限模型。
- [SIMD、多核与缓存一致性](parallelism_consistency.md)：区分数据并行、线程并行、一致性与内存顺序。

## 一条共同主线

共同问题是**并行活动怎样协调**：CPU 与设备并行、程序不同阶段并行、多个核心并行。协调可以提高利用率，同时需要缓冲、仲裁、同步和正确性协议。先跟踪 [PCIe、网卡和 NVMe](device_data_paths.md) 上的 I/O，再看[多个 GPU 怎样通过机器拓扑交换数据](gpu_and_server_topology.md)。

## 延迟与带宽

延迟是完成一次操作要多久，带宽是单位时间能完成多少数据。提高总线宽度或并行 bank 可增加带宽，却未必缩短单次首字节延迟。批量 DMA 适合大吞吐，交互式输入更关心响应延迟。

## 本章自测

1. 为什么慢设备不应让 CPU 持续忙等？
2. 总加速比为什么不能只看被优化部分本身快了多少？
3. cache coherence 与 memory consistency 分别约束什么？
