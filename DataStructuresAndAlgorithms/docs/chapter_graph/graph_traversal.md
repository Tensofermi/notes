# 图的遍历

树代表的是“一对多”的关系，而图则具有更高的自由度，可以表示任意的“多对多”关系。因此，我们可以把树看作图的一种特例。显然，**树的遍历操作也是图的遍历操作的一种特例**。

图和树都需要应用搜索算法来实现遍历操作。图的遍历方式也可分为两种：<u>广度优先遍历</u>和<u>深度优先遍历</u>。

## 一张图，先手动走两遍

把字母看成房间，连线表示双向可通行，跨一条线算一步。从 A 出发，遇到多个未发现的邻居时按字母顺序考虑。

```text
    A
   / \
  B   C
  |   |
  D───E
```

**广度优先（BFS）**像维护一张待办列表：先放 A，每次拿出队首，把新发现的邻居依次排到末尾。节点一入队就标记为已发现，否则沿着环会反复发现同一个节点。

| 本轮拿出 | 本轮新入队 | 处理后的队列 |
| --- | --- | --- |
| A | B、C | B、C |
| B | D | C、D |
| C | E | D、E |
| D | 无，E 已入队 | E |
| E | 无 | 空 |

从 A 出发，B、C 距离 1 步，D、E 距离 2 步。处理第 1 层时发现的第 2 层排在队尾，所以不会抢在第 1 层之前。

**深度优先（DFS）**先走一条路，走不动再回头。沿着 `A → B → D → E → C` 走，到 C 时它的邻居 A、E 都已经到过，便逐层返回。DFS 能到达同样的房间，但第一次走到 C 时已经走了 4 条边，尽管 A 与 C 本来相邻。因此要找等权图上的最少步数，选 BFS；若要探索分支、回溯或检测环，DFS 常更自然。

??? question "先预测：只删掉 A–C 这条边，会发生什么？"

    新图只剩 `A—B—D—E—C` 这条路。BFS 和 DFS 都按 A、B、D、E、C 发现节点。从 A 到 C 的最少步数变为 4。两种算法给出相同访问顺序，源于图上没有分支可选。

可以把同样的图放进 [VisuAlgo](https://visualgo.net/zh/dfsbfs)，先预测每一步再看动画。后面的代码展示如何把纸面上的队列、递归和标记变成程序。

## 广度优先遍历

**广度优先遍历是一种由近及远的遍历方式，从某个节点出发，始终优先访问距离最近的顶点，并一层层向外扩张**。如下图所示，从左上角顶点出发，先遍历它的邻接顶点，再遍历这些顶点新发现的邻居，直至能从起点到达的顶点都访问完毕。

![图的广度优先遍历](graph_traversal.assets/graph_bfs.png)

### 算法实现

BFS 通常借助队列来实现，代码如下所示。队列具有“先入先出”的性质，这与 BFS 的“由近及远”的思想异曲同工。

1. 将遍历起始顶点 `startVet` 加入队列，并开启循环。
2. 在循环的每轮迭代中，弹出队首顶点并记录访问。只将尚未发现的邻接顶点加入队尾，入队时立即标记。
3. 队列空时结束。若图不连通，要从其余未访问的顶点另外开始遍历。

为了防止重复遍历顶点，我们需要借助一个哈希集合 `visited` 来记录哪些节点已被访问。

!!! tip

    哈希集合可以看作一个只存储键的哈希表。正常散列和负载假设下，平均可用 $O(1)$ 时间记录或检查一个键。这里用它判断一个节点是否已进入待处理队列。

=== "Python"

    ```python title="graph_bfs.py"
    def graph_bfs(graph: GraphAdjList, start_vet: Vertex) -> list[Vertex]:
        """广度优先遍历"""
        # 使用邻接表来表示图，以便获取指定顶点的所有邻接顶点
        # 顶点遍历序列
        res = []
        # 哈希集合，用于记录已被访问过的顶点
        visited = set[Vertex]([start_vet])
        # 队列用于实现 BFS
        que = deque[Vertex]([start_vet])
        # 以顶点 vet 为起点，循环直至访问完所有顶点
        while len(que) > 0:
            vet = que.popleft()  # 队首顶点出队
            res.append(vet)  # 记录访问顶点
            # 遍历该顶点的所有邻接顶点
            for adj_vet in graph.adj_list[vet]:
                if adj_vet in visited:
                    continue  # 跳过已被访问的顶点
                que.append(adj_vet)  # 只入队未访问的顶点
                visited.add(adj_vet)  # 标记该顶点已被访问
        # 返回顶点遍历序列
        return res
    ```

代码相对抽象，建议对照下图来加深理解。

=== "<1>"
    ![图的广度优先遍历步骤](graph_traversal.assets/graph_bfs_step1.png)

=== "<2>"
    ![graph_bfs_step2](graph_traversal.assets/graph_bfs_step2.png)

=== "<3>"
    ![graph_bfs_step3](graph_traversal.assets/graph_bfs_step3.png)

=== "<4>"
    ![graph_bfs_step4](graph_traversal.assets/graph_bfs_step4.png)

=== "<5>"
    ![graph_bfs_step5](graph_traversal.assets/graph_bfs_step5.png)

=== "<6>"
    ![graph_bfs_step6](graph_traversal.assets/graph_bfs_step6.png)

=== "<7>"
    ![graph_bfs_step7](graph_traversal.assets/graph_bfs_step7.png)

=== "<8>"
    ![graph_bfs_step8](graph_traversal.assets/graph_bfs_step8.png)

=== "<9>"
    ![graph_bfs_step9](graph_traversal.assets/graph_bfs_step9.png)

=== "<10>"
    ![graph_bfs_step10](graph_traversal.assets/graph_bfs_step10.png)

=== "<11>"
    ![graph_bfs_step11](graph_traversal.assets/graph_bfs_step11.png)

!!! question "广度优先遍历的序列是否唯一？"

    不唯一。广度优先遍历只要求按“由近及远”的顺序遍历，**而多个相同距离的顶点的遍历顺序允许被任意打乱**。以上图为例，顶点 $1$、$3$ 的访问顺序可以交换，顶点 $2$、$4$、$6$ 的访问顺序也可以任意交换。

### 复杂度分析

**时间复杂度**：所有顶点都会入队并出队一次，使用 $O(|V|)$ 时间；在遍历邻接顶点的过程中，由于是无向图，因此所有边都会被访问 $2$ 次，使用 $O(2|E|)$ 时间；总体使用 $O(|V| + |E|)$ 时间。

**空间复杂度**：列表 `res` ，哈希集合 `visited` ，队列 `que` 中的顶点数量最多为 $|V|$ ，使用 $O(|V|)$ 空间。

## 深度优先遍历

**深度优先遍历是一种优先走到底、无路可走再回头的遍历方式**。如下图所示，从左上角顶点出发，访问当前顶点的某个邻接顶点，直到走到尽头时返回，再继续走到尽头并返回，以此类推，直至所有顶点遍历完成。

![图的深度优先遍历](graph_traversal.assets/graph_dfs.png)

### 算法实现

这种“走到尽头再返回”的算法范式通常基于递归来实现。与广度优先遍历类似，在深度优先遍历中，我们也需要借助一个哈希集合 `visited` 来记录已被访问的顶点，以避免重复访问顶点。

=== "Python"

    ```python title="graph_dfs.py"
    def graph_dfs(graph: GraphAdjList, start_vet: Vertex) -> list[Vertex]:
        """深度优先遍历"""
        # 使用邻接表来表示图，以便获取指定顶点的所有邻接顶点
        # 顶点遍历序列
        res = []
        # 哈希集合，用于记录已被访问过的顶点
        visited = set[Vertex]()
        dfs(graph, visited, res, start_vet)
        return res
    ```

深度优先遍历的算法流程如下图所示。

- **直虚线代表向下递推**，表示开启了一个新的递归方法来访问新顶点。
- **曲虚线代表向上回溯**，表示此递归方法已经返回，回溯到了开启此方法的位置。

为了加深理解，建议将下图与代码结合起来，在脑中模拟（或者用笔画下来）整个 DFS 过程，包括每个递归方法何时开启、何时返回。

=== "<1>"
    ![图的深度优先遍历步骤](graph_traversal.assets/graph_dfs_step1.png)

=== "<2>"
    ![graph_dfs_step2](graph_traversal.assets/graph_dfs_step2.png)

=== "<3>"
    ![graph_dfs_step3](graph_traversal.assets/graph_dfs_step3.png)

=== "<4>"
    ![graph_dfs_step4](graph_traversal.assets/graph_dfs_step4.png)

=== "<5>"
    ![graph_dfs_step5](graph_traversal.assets/graph_dfs_step5.png)

=== "<6>"
    ![graph_dfs_step6](graph_traversal.assets/graph_dfs_step6.png)

=== "<7>"
    ![graph_dfs_step7](graph_traversal.assets/graph_dfs_step7.png)

=== "<8>"
    ![graph_dfs_step8](graph_traversal.assets/graph_dfs_step8.png)

=== "<9>"
    ![graph_dfs_step9](graph_traversal.assets/graph_dfs_step9.png)

=== "<10>"
    ![graph_dfs_step10](graph_traversal.assets/graph_dfs_step10.png)

=== "<11>"
    ![graph_dfs_step11](graph_traversal.assets/graph_dfs_step11.png)

!!! question "深度优先遍历的序列是否唯一？"

    与广度优先遍历类似，深度优先遍历序列的顺序也不是唯一的。给定某顶点，先往哪个方向探索都可以，即邻接顶点的顺序可以任意打乱，都是深度优先遍历。
    
    以树的遍历为例，“根 $\rightarrow$ 左 $\rightarrow$ 右”“左 $\rightarrow$ 根 $\rightarrow$ 右”“左 $\rightarrow$ 右 $\rightarrow$ 根”分别对应前序、中序、后序遍历，它们展示了三种遍历优先级，然而这三者都属于深度优先遍历。

### 复杂度分析

**时间复杂度**：所有顶点都会被访问 $1$ 次，使用 $O(|V|)$ 时间；所有边都会被访问 $2$ 次，使用 $O(2|E|)$ 时间；总体使用 $O(|V| + |E|)$ 时间。

**空间复杂度**：列表 `res` ，哈希集合 `visited` 顶点数量最多为 $|V|$ ，递归深度最大为 $|V|$ ，因此使用 $O(|V|)$ 空间。

## 下一步：给边加上代价或顺序

BFS 的层数等于最少经过的边数。若每条边代价不同，接着读[最短路径](shortest_paths.md)。如果边表示「必须先完成」，则需要检查当前前置任务是否都已结束，接着读[拓扑排序](topological_sort.md)。
