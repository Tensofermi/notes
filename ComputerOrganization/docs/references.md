# 参考资料

## 教材与课程

1. David A. Patterson, John L. Hennessy, *Computer Organization and Design: The Hardware/Software Interface*。以 RISC-V/MIPS 为主线，适合建立 ISA、数据通路、流水线与存储层次的统一视角。
2. John L. Hennessy, David A. Patterson, *Computer Architecture: A Quantitative Approach*。更强调定量分析、现代微体系结构和并行系统，适合进阶。
3. Randal E. Bryant, David R. O'Hallaron, *Computer Systems: A Programmer's Perspective*。从程序员能观察到的行为连接汇编、链接、cache、虚拟存储和并发。
4. Andrew S. Tanenbaum, Todd Austin, *Structured Computer Organization*。擅长用层次化机器解释复杂系统。
5. Berkeley CS61C 与 CMU 15-213 的公开课程材料。前者偏组成与 RISC-V，后者偏程序员视角的系统机制。

## 中文视频选读

- **哈尔滨工业大学《计算机组成原理》**。刘宏伟主讲，课程从整机结构入手，适合与本笔记的指令、存储和 I/O 主线对照。[哈工大 B 站课程](https://www.bilibili.com/video/BV1tun4z9E5z/) · [高教社课程页](https://icc.hep.com.cn/loadShowHome.action?courseInfoId=5000003401)
- **北京大学《计算机组成》**。陆俊林主讲。读完[一次 `lw` 的数据通路](chapter_04_cpu/datapath_instruction_cycle.md)后，可看数据通路如何建立，再暂停预测访存指令的控制信号。B 站分集来自转载合集。[数据通路](https://www.bilibili.com/video/BV1Bq4y1t7ea/?p=29) · [访存控制](https://www.bilibili.com/video/BV1Bq4y1t7ea/?p=31) · [北大原课](https://www.coursera.org/learn/jisuanji-zucheng)
- **知白书生《从零开始弄懂主存与 Cache 的地址映射》**。配合[组内查找与替换算例](chapter_06_memory/hierarchy_cache.md)，先手算组号，再判断组内哪一路命中。[Cache 专题](https://www.bilibili.com/video/BV1UB46eWE1X/)

## 规范与手册

- *The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA*。
- *The RISC-V Instruction Set Manual, Volume II: Privileged Architecture*。
- IEEE 754 浮点算术标准。
- JEDEC 发布的 DDR 内存规范与 NVM Express 发布的固态存储设备规范，可对照[主存的访问过程](chapter_06_memory/hierarchy_cache.md)与[设备上提交和完成读写的过程](chapter_07_io_parallel/device_data_paths.md)。

## 阅读方法

规范回答“必须具有什么语义”，教材回答“为什么这样设计”，具体处理器优化手册回答“某个实现实际上怎样做”。三者不能互相替代。

阅读硬件资料时建议固定记录四项：

1. 软件可见状态是什么；
2. 正确性必须保持哪些不变量；
3. 性能瓶颈由延迟、带宽还是并行度决定；
4. 优化用什么资源换来了什么收益。

本站公式和例子均为教学性简化。遇到具体芯片行为，应以对应 ISA 规范、处理器手册和可复现实验为准。
