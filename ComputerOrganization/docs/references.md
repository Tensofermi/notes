# 参考资料

本套笔记力图用清晰的问题驱动主线，把从 0/1 编码到多核与 GPU 的整台机器串成一个连贯模型；而要走得更深、亲手做硬件实验或查阅商用芯片的真实规范，下面这些经得起时间检验的经典教材、视频课程与官方手册，是极佳的延伸读物。

## 经典教材与公开课程

1. **David A. Patterson, John L. Hennessy, *Computer Organization and Design: The Hardware/Software Interface***（《计算机组成与设计：硬件/软件接口》）。以 RISC-V / MIPS 为主线，循序渐进地把 ISA、数据通路、流水线、存储层次与并行主题融为一体，是与本套笔记契合度最高的入门与进阶主教材。
2. **John L. Hennessy, David A. Patterson, *Computer Architecture: A Quantitative Approach***（《计算机体系结构：量化研究方法》）。体系结构领域的经典案头书，极度强调定量公式、真实基准测试、现代乱序微体系结构、多核一致性与领域专用加速器，适合打牢基础后深入研读。
3. **Randal E. Bryant, David R. O'Hallaron, *Computer Systems: A Programmer's Perspective***（《深入理解计算机系统》，简称 **CS:APP**）。从程序员真正能观察到的代码行为出发，打通信息表示、汇编、链接、缓存优化、虚拟存储与并发，极适合搭配本站的「抽象泄漏」与「性能诊断」章节交叉对照。
4. **Andrew S. Tanenbaum, Todd Austin, *Structured Computer Organization***（《结构化计算机组成》）。以极其清晰的多层抽象视角剖析复杂机器，适合强化第 1 章建立的分层思维。
5. **Berkeley CS61C 与 CMU 15-213 公开课程材料**。前者以 RISC-V 与数字电路实践见长，后者以程序员视角的系统底层实验闻名，两套课程的讲义和作业都能把纸面模型炼成肌肉记忆。

## 中文视频选读与搭配建议

如果喜欢边看动态板书与电路演进边巩固直觉，可以按需配合以下中文课程片段：

- **哈尔滨工业大学《计算机组成原理》（刘宏伟 主讲）**：从整机结构与总线系统切入，脉络严谨清晰，非常适合与本笔记的指令、存储和 I/O 主线互相印证。[哈工大 B 站课程](https://www.bilibili.com/video/BV1tun4z9E5z/) · [高教社课程页](https://icc.hep.com.cn/loadShowHome.action?courseInfoId=5000003401)
- **北京大学《计算机组成》（陆俊林 主讲）**：板书推演极为扎实。强烈建议读完本站[一次 `lw` 的数据通路](chapter_04_cpu/datapath_instruction_cycle.md)后，对照观看数据通路一步步搭起来的过程；看到访存控制前先暂停视频，自己预测一遍各条控制信号再核对答案（B 站分集来自转载合集）。[数据通路](https://www.bilibili.com/video/BV1Bq4y1t7ea/?p=29) · [访存控制](https://www.bilibili.com/video/BV1Bq4y1t7ea/?p=31) · [北大原课](https://www.coursera.org/learn/jisuanji-zucheng)
- **知白书生《从零开始弄懂主存与 Cache 的地址映射》**：直观生动，极适合搭配本站[组内查找与替换算例](chapter_06_memory/hierarchy_cache.md)一起看——一边听讲、一边拿纸笔手算组号并判断组内哪一路命中。[Cache 专题](https://www.bilibili.com/video/BV1UB46eWE1X/)

## 官方规范与技术手册

想要核查某条指令的精确语义、浮点边界行为或外设协议细节，最终都应以一手官方规范为准：

- ***The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA***：RISC-V 非特权级指令编码、基础整数与各类扩展的权威定义；
- ***The RISC-V Instruction Set Manual, Volume II: Privileged Architecture***：特权级、异常、中断与多级页表（如 Sv39 / Sv48）的官方硬件契约；
- **IEEE 754 浮点算术标准**：单精度、双精度、半精度、舍入模式以及非正规数 / 无穷 / NaN 行为的统一准绳；
- **JEDEC DDR 内存规范与 NVM Express 规范**：想深入探索主存行缓冲与多队列存储协议的工程细节，可对照本站[主存的访问过程](chapter_06_memory/hierarchy_cache.md)与[设备上提交和完成读写的过程](chapter_07_io_parallel/device_data_paths.md)翻阅相应章节。

## 三类资料怎么配合读？

啃硬件资料时，很容易把不同定位的文档混在一起看晕。不妨记住它们各司其职的三角分工：

- **规范（Specification）**回答「软件可以依赖的**精确语义**是什么」；
- **教材（Textbook）**回答「当年为什么要**这样设计**，背后的直觉和权衡是什么」；
- **具体处理器优化手册（Optimization Manual）**回答「某一代具体硅片**内部到底怎么实现**、缓存几路、转发几拍、哪些指令走快车道」。

三者各不可替代。今后无论阅读哪一份陌生架构的手册或论文，都建议随手在笔记本上固定记下四栏：

1. **可见状态**：对外暴露哪些软件可见的寄存器、内存视图与异常边界？
2. **核心不变量**：为了保证正确性，哪些规则在任何投机与并发下都绝不能打破？
3. **主导瓶颈**：这一机制主要在攻克延迟、带宽还是并行度？
4. **资源交换**：它究竟是用什么硬件/软件代价，换来了眼前的性能收益？

最后提醒一句：本站为了凸显核心因果机制，所有公式与教学算例都做了一定程度的理想化提炼。一旦走进真实工程调优或芯片验证现场，请务必以目标 ISA 规范、具体处理器数据手册以及可复现的实测基准为准。
