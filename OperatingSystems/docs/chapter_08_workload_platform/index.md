# 任务怎样从一台机器走到一组机器

读完[单机调度](../chapter_02_processes/03_cpu_scheduler_lab.md)、[容器运行](../chapter_06_protection_virtualization/03_image_to_process.md)和[文件持久化](../chapter_05_storage_io/02_journaling_crash_disk.md)后，可以把它们放到一个集群任务里。想象两台服务器和三个任务，集群需要回答三个问题：什么时候允许任务开始、在哪台机器运行、任务失败后怎样恢复。

- [提交、准入、放置与执行](01_jobs_and_admission.md)从任务状态、队列及节点约束出发。
- [重试、产物与恢复](02_retries_and_artifacts.md)从客户端超时和半写入 checkpoint 出发。
- [MatrixInfra 综合练习](03_matrixinfra_case.md)结合真实平台的公开接口，观察不同工作负载对上述机制的要求。
