# 图

## 先定边的含义，再问下一步

用[单向关注关系](graph.md)练习画箭头，再把同一张图写成[矩阵和邻接表](graph_operations.md)。接下来按[队列和回溯](graph_traversal.md)分别走一遍，最后改变图的问题，求[带权路径](shortest_paths.md)或[依赖顺序](topological_sort.md)。

![图](../assets/covers/chapter_graph.jpg)

!!! abstract

    在生命旅途中，我们就像是一个个节点，被无数看不见的边相连。
    
    每一次的相识与相离，都在这张巨大的网络图中留下独特的印记。

## 三个不同的问题

先用[遍历](graph_traversal.md)找能到达哪些节点，再让每条边带有代价，用[最短路径](shortest_paths.md)挑一条路线。若边表示先后依赖，就用[拓扑排序](topological_sort.md)找可执行顺序。用同一张图分别问这三个问题，可以看出队列、优先队列和入度表各自维护了什么。
