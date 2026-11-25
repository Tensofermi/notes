# 任务怎样从一台机器走到一组机器

## 从提交成功追到进程真正启动

用[需要两张计算卡的任务 J](01_jobs_and_admission.md)先核对额度，再核对哪台机器放得下。随后模拟[提交结果丢失或恢复点只写了一半](02_retries_and_artifacts.md)。恢复点也叫 **checkpoint**，记录任务重启后接着运行所需的状态。最后做[完整训练案例](03_matrixinfra_case.md)。

读完[单机调度](../chapter_02_processes/03_cpu_scheduler_lab.md)、[容器运行](../chapter_06_protection_virtualization/03_image_to_process.md)和[文件持久化](../chapter_05_storage_io/02_journaling_crash_disk.md)后，可以把问题扩大到一组统一管理的服务器，这就是**集群**（cluster）。想象两台服务器和三个任务：什么时候允许任务开始、在哪台机器运行、失败后怎样接着做——这些单机时代不存在的问题，正是本章的主线。

- [提交、准入、放置与执行](01_jobs_and_admission.md)从任务状态、队列及节点约束出发。
- [重试、产物与恢复](02_retries_and_artifacts.md)从客户端超时和半写入 checkpoint 出发。
- [MatrixInfra 综合练习](03_matrixinfra_case.md)结合真实平台的公开接口，观察不同工作负载对上述机制的要求。
