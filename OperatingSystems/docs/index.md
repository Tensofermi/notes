# 操作系统笔记

打开浏览器的同时，音乐还在播放，文件也能继续下载。处理器（CPU）、内存和设备由多个程序共享，**操作系统**负责分配它们，并限制每个程序能做什么。它还提供统一的使用方式，例如让程序按名字读文件，由系统处理具体的磁盘型号。

如果没有操作系统，每个程序都要自己处理键盘中断、磁盘扇区、物理内存地址和设备时序。更困难的是，多个程序会同时争用同一批硬件资源。操作系统解决的核心问题因此不是“怎样封装几个函数”，而是：

> 如何在共享而有限的硬件上，为许多程序提供方便、高效、可靠并且彼此隔离的运行环境？

第一次读，可以在两个终端[运行同一段程序](chapter_02_processes/01_process_thread_context.md)，观察它们为什么能够分别等待和继续。然后用[两张地址对照表](chapter_04_memory/01_address_space_paging.md)算出同一个地址怎样指向不同的内存。能解释这两件事后，再用[同一个网页服务对照普通进程和容器](chapter_06_protection_virtualization/03_image_to_process.md)。

## 三个核心角色

| 角色 | 解决的问题 | 典型抽象 |
| --- | --- | --- |
| 抽象机器 | 硬件接口过于具体且差异很大 | [进程](chapter_02_processes/01_process_thread_context.md)代表程序的一次运行，[文件](chapter_05_storage_io/01_files_directories_inodes.md)给数据一个可查找的名字 |
| 资源管理器 | 多个任务争用有限资源 | [调度](chapter_02_processes/03_cpu_scheduler_lab.md)决定谁先使用处理器，设备请求也可以分批排队 |
| 隔离与保护者 | 程序可能出错，甚至具有恶意 | [地址翻译](chapter_04_memory/01_address_space_paging.md)给各个程序独立的内存视图，[权限检查](chapter_06_protection_virtualization/01_protection_security.md)限制可执行的操作 |

这些目标有时会相互牵制。攒齐十个磁盘请求再一起处理，可能让系统每秒完成更多请求，也可能让第一个请求等更久。每单位时间完成的工作量叫**吞吐量**，一项工作从发起到得到结果的时间叫**延迟**。

## 一个最小但完整的例子

应用程序读取文件时，常见代码只有一行：

```c
ssize_t n = read(fd, buf, 4096);
```

`fd` 是打开文件后得到的编号，`buf` 是用于接收数据的一段内存，`n` 记录 `read` 返回的结果。内核是操作系统里负责管理机器资源的核心部分。应用通过**系统调用**向它请求服务，读文件的大致路径如下：

```text
应用调用 read
  -> 内核根据编号找到已打开的文件
  -> 检查内存里是否已有一份可用的文件数据
  -> 必要时请设备读入，期间让其他工作先运行
  -> 把读到的字节放到应用提供的缓冲区
```

内核为文件数据留在内存中的这份副本叫**页缓存**，稍后会在[文件系统一章](chapter_05_storage_io/index.md)认识它。试着想象同一段数据连读两次：第二次若能复用副本，就可能省去一次设备读写（I/O）。可以在[读系统调用案例](chapter_07_case_diagnostics/01_read_system_call_path.md)逐步跟踪。

## 全局心智模型

以等输入的程序为例，键还没按下时，它先等待；设备通知新输入到了，它就有机会继续。把「记录当前处境，事件到来后按规则改变记录」这样的模型叫**状态机**。内核也按类似方式处理应用的请求、时钟或设备的通知，以及地址访问失败等事件。具体有哪些入口和后续动作，可以从[系统调用、中断与异常](chapter_01_foundations/02_kernel_user_syscalls_interrupts.md)开始读。

```text
事件到达
  -> 保存必要现场
  -> 进入内核并识别事件
  -> 检查权限与参数
  -> 更新内核对象和队列
  -> 可能阻塞、唤醒或调度
  -> 恢复某个执行流
```

这个模型比“内核是一个一直运行的大程序”更准确：没有用户工作或外部事件时，内核通常没有独立的业务要做；它主要在需要仲裁和服务时获得控制权。

## 学习路线

| 阶段 | 从哪里读 | 读完能解释 |
| --- | --- | --- |
| 第 1–4 章：一个程序怎样运行 | [特权与系统调用](chapter_01_foundations/index.md)、[进程与线程](chapter_02_processes/index.md)、[调度实验](chapter_02_processes/03_cpu_scheduler_lab.md)、[并发与同步](chapter_03_concurrency/index.md) | 谁正在运行、谁在等、何时需要加锁 |
| 第 5–7 章：程序怎样访问数据 | [虚拟内存](chapter_04_memory/index.md)、[文件和 I/O](chapter_05_storage_io/index.md)、[崩溃一致性](chapter_05_storage_io/02_journaling_crash_disk.md) | 一次访问如何完成，写入何时可恢复 |
| 第 8–10 章：怎样隔离程序 | [权限与保护](chapter_06_protection_virtualization/01_protection_security.md)、[虚拟机](chapter_06_protection_virtualization/02_virtual_machines_containers.md)、[容器与镜像](chapter_06_protection_virtualization/03_image_to_process.md) | 哪些资源可见、谁允许访问、隔离的代价是什么 |
| 第 11–13 章：怎样把任务交给集群 | [集群编排](chapter_08_workload_platform/01_jobs_and_admission.md)、[重试与恢复](chapter_08_workload_platform/02_retries_and_artifacts.md)、[MatrixInfra 案例](chapter_08_workload_platform/03_matrixinfra_case.md) | 任务在哪里等待，何时能恢复，产物如何追溯 |

第一次学习可以先手算一次调度和一次地址翻译，再完成一个本机 HTTP 进程的容器实验。[OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/)可配合前三个阶段阅读；[MIT xv6](https://mit-pdos.github.io/xv6-riscv-book/)可用于对照内核实现。集群运行需要网络基础，建议先读<a href="../ComputerNetworks/index.html">网络课程的应用与传输层</a>。

## 学习方法

操作系统的概念可以和可观察的证据对应。看到[上下文切换](chapter_02_processes/01_process_thread_context.md)需要时间时，问问系统保存了哪些让程序继续运行的信息。看到读取文件很慢时，先问数据是否已经在内存里，再问这次访问是否真的等了设备。

建议对每个机制做三层追问：

1. 抽象层：它向上提供了什么稳定接口？
2. 机制层：内核和硬件实际维护了哪些状态？
3. 策略层：当选择不唯一时，系统采用什么权衡？

机制回答“能不能做到”，策略回答“应该怎样选择”。页表是机制，页面置换算法是策略；定时器中断和上下文保存是机制，调度算法是策略。把二者分开，很多概念会清楚得多。

## 实验边界

笔记中的命令优先采用只读观测方式。`strace`、`ps`、`vmstat`、`iostat`、`perf stat` 等工具的可用性取决于操作系统、内核配置和权限；执行前应先确认目标进程和运行环境，不在生产系统上盲目进行高开销跟踪。

继续阅读前，可以先带着三个问题：

- 为什么普通函数调用不能直接替代系统调用？
- 为什么一个线程等待磁盘时，另一个线程还能使用 CPU？
- 为什么程序访问的地址通常不是内存条上的真实物理地址？

后续章节会逐步建立回答这些问题所需的模型。
