# 从镜像到进程：一次可重复的容器运行

**先修**：[进程](../chapter_02_processes/01_process_thread_context.md)、[权限](01_protection_security.md)、[虚拟机与容器](02_virtual_machines_containers.md)。

**读完能做**：跟踪一个服务从镜像引用到运行，区分它在文件、进程、网络和权限上的边界。

## 同一个程序，三种运行环境

假设你已能运行一个监听 8000 端口的 Python HTTP 服务。直接运行时，它继承当前用户、目录和可见网络。把它放进虚拟机，客体有自己的内核和虚拟设备。放进 Linux 容器时，宿主机内核仍执行系统调用，namespace 改变程序能看到的进程、挂载和网络视图，cgroup 对一组进程进行资源控制和统计。

容器还需要单独考虑权限：进程 UID、可读写挂载、capabilities、系统调用过滤，以及出站网络分别约束不同动作。沙箱是一组围绕**威胁模型**选出来的边界。处理不受信任的代码时，可能需要更强的隔离、受控凭据和最小挂载。资源限额主要解决某个任务把共享资源用尽的问题。

## 镜像怎样变成进程

| 阶段 | 问题 | 输出 |
| --- | --- | --- |
| 构建 | 用哪些文件和启动配置 | 镜像清单、配置及内容层 |
| 分发 | 到哪里找这一版内容 | Registry 中可拉取的镜像引用 |
| 准备 | 进程看到哪套文件、网络和资源约束 | 根文件系统、挂载、namespace、cgroup 与安全配置 |
| 启动 | 执行什么程序，退出后怎么办 | 在节点内核上运行的进程及退出状态 |

标签适合起可读的名字。标签可以被重新指向；摘要标识特定内容，适合在 Recipe 中记录依赖。镜像层可以复用。运行时的可写层跟容器实例走，需要跨重建保留的数据应写向明确挂载的持久位置。Docker 提供构建和运行入口；containerd 可管理镜像和容器生命周期，底层 OCI runtime 负责按运行配置启动进程。在 Kubernetes 里，Pod 可以让多个容器共享网络等资源，并成为调度单位。

## 观察一个只在本机开放的服务

具备 Docker 环境时，在空目录里运行如下命令。这个教学例子采用可读标签，复现实验记录时可以额外记下实际镜像摘要。

```sh
docker run --rm -d --name notes-http-demo \
  -p 127.0.0.1:8000:8000 --memory=128m --cap-drop=ALL \
  --security-opt=no-new-privileges=true \
  python:3-slim python -m http.server 8000 --directory /tmp
curl -i http://127.0.0.1:8000/
docker exec notes-http-demo sh -c 'echo "$$"; cat /proc/self/cgroup'
docker logs notes-http-demo
docker stop notes-http-demo
```

镜像需可下载，本机 8000 端口需空闲。先预测：应用已在容器监听时，去掉 `-p` 是否还会通过上述宿主机端口访问？再分别观察进程、端口和日志。应用的挂载目录、对外访问范围和凭据应根据实际任务分别决定。

## 自测

如果把 checkpoint 留在容器可写层，运行同一个镜像并新建容器时会发生什么？

??? note "参考思路"
    新容器从镜像与新的可写层开始，原容器产生的 checkpoint 不随镜像出现。应把需要恢复的数据持久化到独立位置，并记录对应版本和路径。

参考 [OCI 三份规范的分工](https://opencontainers.org/about/overview/)与 [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)。
