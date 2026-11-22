# 参考资料

## 教材

1. James F. Kurose, Keith W. Ross, *Computer Networking: A Top-Down Approach*。本笔记采用自顶向下的主线。
2. Andrew S. Tanenbaum, David J. Wetherall, *Computer Networks*。
3. W. Richard Stevens, *TCP/IP Illustrated, Volume 1: The Protocols*。
4. Douglas E. Comer, *Internetworking with TCP/IP, Volume One*。

## 中文视频选读

- **湖科大教书匠《计算机网络微课堂》**。先做时延小题，再看交换机怎样学习 MAC 地址。看交换机分集时，可以暂停预测第一帧会走哪些端口，以及回复到达后表里多了哪一项。[时延习题](https://www.bilibili.com/video/BV1c4411d7jb/?p=13) · [交换机自学习](https://www.bilibili.com/video/BV1c4411d7jb/?p=37) · [作者合集](https://www.bilibili.com/list/ml962700202?bvid=BV1c4411d7jb&oid=64605483)
- **技术蛋老师的 Docker 网络模式讲解**。配合[容器网络](chapter_09_virtual_network/01_interfaces_bridges_tunnels.md)，先画出容器自己的监听地址和宿主发布的入口，再看 Bridge、Host、None 三种模式改变了哪一段路径。[Docker 网络模式视频](https://www.bilibili.com/video/BV1Aj411r71b/)
- **CNCF × Alibaba 云原生公开课**。理解同机网桥以后再看 Kubernetes 的 CNI 段，追踪 Pod 网卡和地址由谁准备。B 站链接是转载分集。[理解 CNI](https://www.bilibili.com/video/BV1r7411r7h7/?p=26) · [课程原页](https://edu.aliyun.com/course/314164/)

## 关键标准

- [RFC 8200: Internet Protocol, Version 6](https://www.rfc-editor.org/rfc/rfc8200)
- [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293)
- [RFC 768: User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)
- [RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 1035: Domain Names — Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112)
- [RFC 9113: HTTP/2](https://www.rfc-editor.org/rfc/rfc9113)
- [RFC 9114: HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [RFC 9000: QUIC](https://www.rfc-editor.org/rfc/rfc9000)
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [RFC 826: Address Resolution Protocol](https://www.rfc-editor.org/rfc/rfc826)

RFC 是协议行为的最终依据，但不适合第一次接触时从头硬读。更有效的顺序是：先用教材建立问题意识，再带着具体问题查 RFC 的术语、状态机和边界条件，最后通过抓包验证自己的理解。

## 实验与工具

- Wireshark：交互式抓包与协议字段分析。
- `tcpdump`：终端抓包，适合远程服务器和自动化环境。
- `curl`：观察 HTTP 请求、响应、重定向和 TLS 连接。
- `dig`：检查 DNS 查询路径和记录。
- `ping`、`traceroute`：基于 ICMP 或逐跳超时探测可达性。
- `ss`、`lsof`：检查本机监听端口和连接状态。
- `openssl s_client`：查看证书链与 TLS 协商结果。

## 关于版本与边界

网络协议会演进，操作系统实现也会采用不同优化。本笔记强调稳定的核心机制；涉及拥塞控制算法、浏览器缓存策略、DNS 加密和 TLS 配置时，应以实际系统文档、抓包结果与当前标准为准。
