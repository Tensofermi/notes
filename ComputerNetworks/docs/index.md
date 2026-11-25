# 计算机网络

不妨先想一个最朴素的问题：一台电脑怎样把一张照片交给另一台？照片太大，不能一口气塞过去，得先拆成一小份一小份的数据，每份叫作一个**分组**（packet）；每个分组要走过好几段网线或无线信号才能到达，每一段叫作一条**链路**（link）。下文的 URL 就是浏览器地址栏里的网址，HTTP 则是浏览器和服务器事先约定好的一套「怎么写请求、怎么写回应」的规则。

计算机网络解决的核心问题是：**如何让彼此独立、相隔很远、能力各异的设备，像在同一个系统中一样交换信息**。困难不只在“把比特送过去”，还在于路径会变化、分组会丢失、接收方速度有限、很多用户会竞争同一条链路，而且通信双方通常互不信任。

这套笔记用一个贯穿始终的问题组织知识：

> 在浏览器输入一个 URL 并按下回车后，页面为什么能够出现？

回答它需要同时理解 DNS 如何找地址、HTTP 如何表达请求、TLS 如何建立可信通道、TCP 或 QUIC 如何运输字节、IP 如何跨网络选路、以太网或 Wi-Fi 如何完成一跳传输。分层让我们可以逐层学习，但真正的网络行为始终是端到端的合作。

第一次读，先[在自己电脑上发一个 HTTP 请求](chapter_02_application/04_socket_and_listening.md)，比较「有 HTTP 404 响应」和「连接没有建立」两种结果。接着[把六个乱序抵达的字节拼回去](chapter_03_transport/02_reliable_transport.md)，再读[发送方为什么有时要等](chapter_03_transport/03_flow_congestion_control.md)。暂时不知道各协议细节也可以先做这三个例子。

## 学习路线

| 阶段 | 从哪里读 | 先做哪道练习 |
| --- | --- | --- |
| 第 1–2 章：看见一次请求 | [网络基础](chapter_01_foundations/index.md)、[应用层](chapter_02_application/index.md) | 启动[本机 HTTP 服务](chapter_02_application/04_socket_and_listening.md)，比较连接失败与 HTTP 404 |
| 第 3 章：把数据可靠送达 | [可靠传输](chapter_03_transport/02_reliable_transport.md)、[流量与拥塞控制](chapter_03_transport/03_flow_congestion_control.md) | 手推丢数据、丢确认和乱序时的发送与确认 |
| 第 4–6 章：找到路径与信任边界 | [网络层](chapter_04_network/index.md)、[链路层](chapter_05_link/index.md)、[TLS 与远程访问](chapter_06_security/index.md) | 标注跨子网请求每一段的地址和身份检查 |
| 第 7–10 章：把机制接到实际系统 | [虚拟网络](chapter_09_virtual_network/01_interfaces_bridges_tunnels.md)、[服务入口](chapter_09_virtual_network/02_service_discovery_proxies.md)、[数据中心互连](chapter_10_data_center/index.md) | 用[Agent 工作站](chapter_07_case_study/02_agent_workstation.md)追踪一次请求与任务 |

第一次学习可按表从上往下读。已有经验时，可先用[诊断工具与排障路径](chapter_08_diagnostics/01_diagnostic_tools.md)复盘一次故障，再补相应概念。课程可以搭配 [Kurose & Ross 交互习题](https://www-net.cs.umass.edu/kurose_ross/interactive/index.php)和 [Stanford CS144](https://web.stanford.edu/class/cs144/)的递进实验。

## 一个先行的直觉

把互联网想成跨国物流系统：

| 网络概念 | 物流类比 | 关键区别 |
| --- | --- | --- |
| 应用报文 | 包裹中的商品与订单 | 语义由应用协议决定 |
| 传输层端口 | 大楼中的房间号 | 把数据交给正确进程 |
| IP 地址 | 城市与街道地址 | 地址通常带有网络拓扑含义 |
| 路由器 | 中转站 | 每跳只决定下一站，不规划每个比特 |
| 链路层帧 | 某一段运输使用的包装 | 每经过一种链路都可能重新封装 |

这个类比能建立直觉，却不能替代协议细节。例如互联网分组可能乱序，TCP 会在端系统中恢复有序字节流；物流通常由人工识别包裹，而网络设备依赖严格的二进制首部格式。

## 学习方法

每学一个协议，都问六个问题：

1. 它要解决什么失败模式？
2. 它向上一层承诺什么服务？
3. 报文中哪些字段支撑这个承诺？
4. 状态由通信两端的设备保存，还是由沿途设备保存？
5. 它用什么资源换来了什么性质？
6. 记录并查看实际收发的数据（抓包）时，能看到哪些证据？

网络不是协议名词的堆积。真正的掌握，是能从一次请求的现象反推每一层可能发生了什么。
