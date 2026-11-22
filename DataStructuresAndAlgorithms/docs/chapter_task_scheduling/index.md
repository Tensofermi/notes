# 综合练习：一张表看懂任务调度

## 先把就绪和能放下分成两栏

想象有四项训练或评估任务，只有两张能做模型计算的卡（**GPU**）。评估必须等训练成功，训练就是评估的**前置任务**，两者之间有**依赖**。一项任务已经到达、前置任务也都成功，就叫**就绪**。这时还要等到有足够的卡才能启动。决定哪项任务什么时候用卡，就是这个例子中的**任务调度**。先按「依赖未满足」「就绪但资源不够」「可以启动」画三栏，再比较按到达时间与按优先级挑选的结果。

??? question "两台机器各剩一张卡，为什么两卡任务仍可能等？"

    如果任务必须同机使用两张卡，剩余资源分散，任何一个位置都放不下。把多台共同执行任务的机器称为**集群**。空闲资源分散在不同机器上、合起来看明明够却无法分给这项任务，这种现象叫**资源碎片**。

**先修**：[优先队列](../chapter_heap/heap.md)、[拓扑排序](../chapter_graph/topological_sort.md)。

**目标**：先实现一个可手算的调度模型，再看公平、利用率与等待时间怎样互相影响。

## 模型

假设任意一张卡都可以给任意任务。任务启动后会一直占用分给它的卡，直到结束。系统中途收回资源、让别的任务先用的做法叫**抢占**，本例先省掉这一步。每当时钟来到任务到达或结束的时刻，先释放已结束任务的资源，再从已经到达、依赖均成功的任务中选择还放得下的任务。同一时刻可连续启动多项任务，每启动一项就扣掉它需要的卡。优先级在这里是任务表中的排序数字，数值越大越先选。若主要排序条件相同，先比较到达时间，再比较任务名。时间单位为分钟。

| 任务 | 到达时刻 | GPU 数 | 运行时长 | 前置任务 | 优先级，数值越大越高 |
| --- | ---: | ---: | ---: | --- | ---: |
| A | 0 | 2 | 4 | 无 | 1 |
| B | 1 | 1 | 3 | 无 | 1 |
| C | 2 | 2 | 2 | 无 | 3 |
| D | 2 | 1 | 2 | B | 2 |

## 手算与比较

第一种策略按到达时间检查就绪任务，借用了先到先处理（先入先出，**FIFO**）的顺序。为了让空闲卡还能服务其他任务，这个例子允许先跳过装不下的候选。比如只剩 1 张卡时，队头要 2 张、后面一项只要 1 张，后面的可以先开始。要是严格按队头等待，后面的也必须等，卡可能暂时空着。

时刻 0 启动 A，时刻 4 启动 B。此时只剩一张空闲卡，C 需要两张，所以继续等。时刻 7，B 结束，D 刚就绪。C 和 D 都在时刻 2 到达，所以按任务名先运行 C。时刻 9 再启动 D，全部在 11 结束。

优先级策略在时刻 4 先启动 C，时刻 6 启动 B，时刻 9 启动 D，也在 11 结束。C 的等待从 5 分钟降到 2 分钟，B 的等待从 3 分钟增加到 5 分钟。一张卡被分配 1 分钟，记为 1 **GPU·分钟**。两种策略都用掉了 $2\times4+1\times3+2\times2+1\times2=17$ GPU·分钟，平均分配比例为 $17/(2\times11)$，约 77%。这里只测**已分配**时间，实际计算繁忙程度还需设备指标。

## 自己动手

1. 用任务名查出它的状态和依赖，用[入度表](../chapter_graph/topological_sort.md)记录还有多少前置任务没成功。将运行中任务的结束时刻放到[最小堆](../chapter_heap/heap.md)，每次可以先看到最早结束的是谁。
2. 每轮打印时刻、空闲 GPU、刚完成的任务和新的选择。把上面两条时间线当作检查样例。
3. 为长期等待的任务临时提高排序时用的优先级。构造一串持续到来的高优先级短任务，看看低优先级任务何时得到机会。
4. 把 GPU 改成两台各一张卡的机器，要求双卡任务使用同一机器，再比较「剩余数量」与「满足放置约束」的差异。

??? example "Python 参考实现"

    把到达和结束当作会改变可用任务或资源的**事件**。一次处理完当前时刻能启动的任务，再跳到下一个事件时刻。这个小版本用排序选任务和扫描找事件，方便先验证规则。

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

现实集群里，一个团队的任务可能要先等平台核对可用额度、允许它进入后续调度，这一步叫**准入**。接下来还要决定把任务交给哪台机器、用哪几张卡，这一步叫**放置**。本节的例子从任务已经可以等待分配算起。及时让大任务拿到同一台机器上的资源，与让小任务尽早运行需要权衡。允许小任务一直插入，依赖多张卡的大任务可能很久都无法同时拿到足够的卡，这叫**饥饿**。可以限制插入次数，或根据等待多久逐步提高优先级。现实平台还会处理不同资源类型、故障和实际使用量，继续读<a href="../../OperatingSystems/chapter_08_workload_platform/01_jobs_and_admission.html">操作系统的集群编排章节</a>。
