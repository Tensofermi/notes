# 栈与队列

## 每次取出谁，由规则决定

先用[撤销动作](stack.md)理解为何要先取最后一个，再让号码按[报名顺序](queue.md)出队。若两端都需要操作，就换成[双端队列](deque.md)。最后[把队列填满](bounded_queue.md)，决定新来的元素怎么办。

![栈与队列](../assets/covers/chapter_stack_and_queue.jpg)

!!! abstract

    栈如同叠猫猫，而队列就像猫猫排队。
    
    两者分别代表先入后出和先入先出的逻辑关系。
