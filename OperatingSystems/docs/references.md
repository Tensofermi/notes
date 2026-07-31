# 参考资料

本页列出这套笔记采用的主要学习线索。正文以概念重组和个人理解为主；遇到接口的精确语义、特定系统实现或版本差异时，应以对应系统的官方手册、源码和规范为准。

## 入门与主线教材

1. Remzi H. Arpaci-Dusseau, Andrea C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*。以虚拟化、并发、持久化三条主线组织，适合建立动机、机制与实验之间的联系。
2. Abraham Silberschatz, Peter B. Galvin, Greg Gagne, *Operating System Concepts*。覆盖面完整，适合作为课程章节地图和术语参考。
3. Andrew S. Tanenbaum, Herbert Bos, *Modern Operating Systems*。重视设计比较、分布式系统和安全背景。
4. Thomas Anderson, Michael Dahlin, *Operating Systems: Principles and Practice*。强调工程不变量、并发和系统构造。

## 实现与源码

1. Russ Cox、Frans Kaashoek、Robert Morris 等，*xv6: a simple, Unix-like teaching operating system*。代码规模适中，适合跟踪系统调用、进程、页表、文件系统和驱动路径。
2. Robert Love, *Linux Kernel Development*。用于理解 Linux 内核中的进程、调度、中断、同步和内存管理概念。
3. Jonathan Corbet、Alessandro Rubini、Greg Kroah-Hartman, *Linux Device Drivers*。适合理解驱动、设备模型、中断和 DMA；具体 API 可能随内核版本变化。
4. Linux 内核源码与 `Documentation/`。实现细节必须结合目标内核版本阅读，不能把旧书中的 API 当作永久契约。

## 接口与规范

- POSIX 标准：用于核对进程、线程、文件和同步原语的可移植接口语义。
- Linux man-pages：优先查阅 `man 2` 的系统调用、`man 3` 的库接口、`man 5` 的文件格式和 `man 7` 的概念说明。
- System V ABI 与目标体系结构手册：用于核对调用约定、异常入口、页表格式和特权级细节。
- 设备厂商手册：用于核对寄存器、描述符环、DMA 和中断控制器行为。

## 并发与内存模型

1. Maurice Herlihy, Nir Shavit, *The Art of Multiprocessor Programming*。深入讨论线性化、无锁结构和并发对象。
2. Paul E. McKenney, *Is Parallel Programming Hard, And, If So, What Can You Do About It?*。连接并发设计、内存序、RCU 与实际内核工程。
3. 目标语言的内存模型规范。C/C++、Java、Rust 和内核内存模型并不完全相同，不能只凭 CPU 直觉推导语言级并发语义。

## 文件系统与存储

1. Marshall Kirk McKusick 等，*The Design and Implementation of the FreeBSD Operating System*。包含文件系统和内核实现的系统性讨论。
2. 文件系统论文与设计文档：日志文件系统、软更新、写时复制、日志结构文件系统各自解决的故障模型不同。
3. 块设备和存储介质文档：HDD、SATA SSD、NVMe 和持久内存的延迟结构不同，调度策略不能脱离设备特性讨论。

## 如何使用这些资料

建议把资料分为三个层次：

| 层次 | 适合回答的问题 |
| --- | --- |
| 教材 | 为什么需要这个抽象，它和其他机制怎样连接？ |
| 规范与手册 | 接口精确定义、错误码、可移植性边界是什么？ |
| 源码与实验 | 某个版本实际怎样实现，性能瓶颈在哪里？ |

当三者看似冲突时，先检查讨论对象是否相同：教材可能描述一般模型，手册描述用户可见契约，源码描述特定版本实现。不要用实现偶然性替代接口承诺，也不要用抽象模型否定真实机器的成本。
