# Tensofermi Notes

这里集中保存个人学习笔记的 Markdown 源文件。每套笔记由 MkDocs Material 独立构建，共享同一套自动部署流程。

## 数值方法与机器学习

- [Monte Carlo](https://tensofermi.github.io/notes/MonteCarlo/)
- [Neural Network](https://tensofermi.github.io/notes/NeuralNetwork/)

## 计算机科学

- <a href="DataStructuresAndAlgorithms/index.html">数据结构与算法</a>：从复杂度、队列和图，到最短路径、任务依赖与调度练习。
- <a href="ComputerOrganization/index.html">计算机组成原理</a>：跟踪指令、访存和 I/O，再看一批数据怎样从磁盘进入 GPU。
- <a href="OperatingSystems/index.html">操作系统</a>：理解进程、调度、持久化与隔离，最后跟踪一次训练任务。
- <a href="ComputerNetworks/index.html">计算机网络</a>：沿一次请求学协议，从本机服务走到虚拟网络、数据中心和 Agent 工作站。

第一次读，可以并行学习算法和组成原理，随后把一次地址翻译、一个容器进程和一次网络请求接起来。最后完成训练平台与 Agent 工作站两个跨课案例。


## 物理

- [热力学与统计物理](https://tensofermi.github.io/notes/ThermodynamicsStatisticalPhysics/)
- [固体物理](https://tensofermi.github.io/notes/SolidStatePhysics/)
- [量子信息](https://tensofermi.github.io/notes/QuantumInformation/)
- [物理笔记合集](https://tensofermi.github.io/notes/PhysicalNotes/)

## 如何维护

正文只维护 Markdown 与必要资源。推送到 `main` 后，GitHub Actions 会严格构建全部站点并部署 GitHub Pages；生成的 HTML 不进入 Git 历史。
