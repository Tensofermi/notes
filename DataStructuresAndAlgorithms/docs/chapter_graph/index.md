# 图

## 先定边的含义，再问下一步

用[单向关注关系](graph.md)练习画箭头，再把同一张图写成[两点之间是否有边的表格和每个点的邻居清单](graph_operations.md)。接下来[分圈访问，或沿一条路走到底再退回来](graph_traversal.md)。给每条边记下用时，就可以[找总用时最少的路](shortest_paths.md)，也可以让箭头表示先后要求，再找[依赖顺序](topological_sort.md)。

![图](../assets/covers/chapter_graph.jpg)

!!! abstract

    在生命旅途中，我们就像是一个个节点，被无数看不见的边相连。
    
    每一次的相识与相离，都在这张巨大的网络图中留下独特的印记。

## 三个不同的问题

先用[遍历](graph_traversal.md)找能到达哪些节点，再让每条边带有代价，用[最短路径](shortest_paths.md)挑一条路线。若边表示先后依赖，就用[拓扑排序](topological_sort.md)找可执行顺序。用同一张图分别问这三个问题，可以看出队列、优先队列和入度表各自维护了什么。
