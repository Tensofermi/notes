# 综合练习：一张表看懂任务调度

## 先把就绪和能放下分成两栏

一项任务可以在所有依赖都成功后就绪，但还需要足够资源才会启动。另一项任务虽然只用一张卡，也不能在它的前置任务没结束时提前启动。先把每个时刻的候选分成「依赖未满足」「就绪但资源不够」「可以启动」三栏，再比较 FIFO 与优先级策略。

??? question "两台机器各剩一张卡，为什么两卡任务仍可能等？"

    如果任务必须同机使用两张卡，剩余资源分散，任何一个位置都放不下。这就是集群案例中的资源碎片。

**先修**：[优先队列](../chapter_heap/heap.md)、[拓扑排序](../chapter_graph/topological_sort.md)。

**目标**：先实现一个可手算的调度模型，再看公平、利用率与等待时间怎样互相影响。

## 模型

有两张可互换的 GPU。任务启动后一直运行到结束，无抢占。每当时钟来到任务到达或结束的时刻，先释放已结束任务的资源，再从已经到达、依赖均成功的任务中选择能装下的任务。并列按到达时间，再按任务名。时间单位为分钟。

| 任务 | 到达时刻 | GPU 数 | 运行时长 | 前置任务 | 优先级，数值越大越高 |
| --- | ---: | ---: | ---: | --- | ---: |
| A | 0 | 2 | 4 | 无 | 1 |
| B | 1 | 1 | 3 | 无 | 1 |
| C | 2 | 2 | 2 | 无 | 3 |
| D | 2 | 1 | 2 | B | 2 |

## 手算与比较

FIFO 按到达时间检查可运行任务，并跳过当前放不下的候选。时刻 0 启动 A，时刻 4 启动 B，C 需要两张卡而此时只有一张空闲。时刻 7 B 结束，D 刚就绪。按到达时间和同分规则先运行 C，时刻 9 再启动 D，全部在 11 结束。

优先级策略在时刻 4 先启动 C，时刻 6 启动 B，时刻 9 启动 D，也在 11 结束。C 的等待从 5 分钟降到 2 分钟，B 的等待从 3 分钟增加到 5 分钟。两种策略都用掉了 $2\times4+1\times3+2\times2+1\times2=17$ GPU·分钟，平均分配比例为 $17/(2\times11)$，约 77%。这里只测**已分配**时间，实际计算繁忙程度还需设备指标。

## 自己动手

1. 用字典记录任务状态和依赖，用入度表维护就绪集合。将已启动任务的结束事件放入按时间排序的最小堆。
2. 每轮打印时刻、空闲 GPU、刚完成的任务和新的选择。把上面两条时间线当作检查样例。
3. 为长期等待的任务提高有效优先级。构造一串持续到来的高优先级短任务，看看低优先级任务何时得到机会。
4. 把 GPU 改成两台各一张卡的机器，要求双卡任务使用同一机器，再比较「剩余数量」与「满足放置约束」的差异。

??? example "Python 参考实现"

    把到达和结束当作事件。一次处理完当前时刻能启动的任务，再跳到下一个事件。这个小版本用排序选任务和扫描找事件，方便先验证规则。

    ```python
    from dataclasses import dataclass


    @dataclass(frozen=True)
    class Task:
        name: str
        arrival: int
        gpus: int
        duration: int
        priority: int
        requires: tuple[str, ...] = ()


    tasks = [
        Task("A", 0, 2, 4, 1),
        Task("B", 1, 1, 3, 1),
        Task("C", 2, 2, 2, 3),
        Task("D", 2, 1, 2, 2, ("B",)),
    ]


    def simulate(tasks, capacity, rank):
        pending = list(tasks)
        running = []
        completed = set()
        starts = []
        now = 0

        while pending or running:
            for end, task in running:
                if end == now:
                    completed.add(task.name)
            running = [(end, task) for end, task in running if end > now]
            free = capacity - sum(task.gpus for _, task in running)

            ready = [task for task in pending
                     if task.arrival <= now and completed.issuperset(task.requires)]
            for task in sorted(ready, key=rank):
                if task.gpus > free:
                    continue
                free -= task.gpus
                pending.remove(task)
                running.append((now + task.duration, task))
                starts.append((task.name, now))

            future = [end for end, _ in running]
            future.extend(task.arrival for task in pending if task.arrival > now)
            if future:
                now = min(future)
            elif pending:
                raise ValueError("Dependencies or capacity prevent progress")

        return starts


    print(simulate(tasks, 2, lambda task: (task.arrival, task.name)))
    # [('A', 0), ('B', 4), ('C', 7), ('D', 9)]

    print(simulate(tasks, 2, lambda task: (-task.priority, task.arrival, task.name)))
    # [('A', 0), ('C', 4), ('B', 6), ('D', 9)]
    ```

小模型已经出现准入、放置、公平和资源碎片四个问题。现实平台还会处理不同资源类型、故障和实际使用量，继续读<a href="../../OperatingSystems/index.html">操作系统课程</a>的集群编排章节。
