# 数据结构与算法

从一个可以手算的问题开始：四项任务到达时间不同，有的还要等其他任务完成，你会怎样决定谁先运行？课程先讲清数据怎么存、操作要付出多少成本，再用队列、堆和图一步步完成这个例子。

如果只会写循环，可以先读[数组的五格插入](chapter_array_and_linkedlist/array.md)：画出每次搬动后哪一格改变。然后用[链表的同一组号码](chapter_array_and_linkedlist/linked_list.md)做同样的插入，回头看[一列号码变长时，哪些操作会跟着变慢](chapter_computational_complexity/time_complexity.md)。首次阅读选自己会的一种语言即可，其他语言的代码留作对照。

## 怎么读

| 阶段 | 先掌握什么 | 可以动手做什么 |
| --- | --- | --- |
| 第 1–2 章 | [怎样检查循环每走一步都正确](chapter_introduction/reason_about_algorithms.md)，以及[输入变大时开销怎样变](chapter_computational_complexity/index.md) | 找出最早任务，手推循环并估算开销 |
| 第 3–8 章 | 用数组和链表存顺序，[用有限格子排队](chapter_stack_and_queue/bounded_queue.md)，[用号码建目录](chapter_hashing/index.md)，[按优先级取下一项](chapter_heap/heap.md)，再练习搜索和排序 | 改一个操作频率，比较数据结构是否还适合 |
| 第 9–10 章 | 沿连线或箭头访问各个点、[找代价最小的路](chapter_graph/shortest_paths.md)、[按依赖排先后](chapter_graph/topological_sort.md) | 在同一张图里分清找路径与满足依赖 |
| 第 11–13 章 | 拆成小题、撤销一次尝试、保存已算的答案、判断能否每次只留一个选择 | 用反例检验选择策略，再做[任务调度综合练习](chapter_task_scheduling/index.md) |

初次阅读，能把示例手推一遍，再跑熟悉语言里的实现。读到复杂度时同时写下条件，比如输入是否有序、图中用来表示代价的数字能不能为负、插入位置是否已经找到。实验偶尔会得到相反直觉，原因可能是数据规模、分布或内存访问方式。

## 原始资料与拓展

本笔记中的大部分内容修改自 [Hello 算法](https://www.hello-algo.com/) 项目，原项目由 [krahets](https://github.com/krahets/hello-algo) 创建，并遵循 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。这里的改写、删补和新增内容均为个人学习记录与扩展。

下图是原项目的学习地图，可用于对照知识点。

![Hello 算法学习框架](logo/hello_algo_mindmap.png)

- [VisuAlgo 图遍历](https://visualgo.net/zh/dfsbfs)可逐步观察广度优先遍历和深度优先遍历（BFS 和 DFS，见[图的遍历](chapter_graph/graph_traversal.md)）。
- [MIT 6.006 讲义](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-notes/)适合在做完小例子后核对条件和证明。
