# 虚拟网络、服务发现与远程访问

## 先让两个 8000 端口各归各的进程

把程序连同它需要的文件放进一个独立运行环境，就可以在同一台机器上启动两份。这里的 A 和 B 是两个这样的环境，也就是**容器**。它们各有自己的网络配置，能用相同的端口号。它们要互相发送数据，就需要一段由软件模拟的连接。沿着[容器 A 发送给 B 的第一个请求](01_interfaces_bridges_tunnels.md)，先看软件网线怎样连接到两端，再看数据怎样经过虚拟交换设备。把 B 移到另一台机器，再看内外地址怎样配合。最后用[后端 A 换成 B](02_service_discovery_proxies.md)说明客户端为什么还可以用同一个服务名。

这里把 [IP 路由](../chapter_04_network/03_forwarding_routing.md)、[本机 Socket](../chapter_02_application/04_socket_and_listening.md)和[TLS](../chapter_06_security/01_tls.md)接成同一条路径。先让两个隔离的网络能交换包，再让客户端在后端不断变化时仍能找到服务。

- [从虚拟网卡到隧道](01_interfaces_bridges_tunnels.md)
- [服务发现、代理与负载均衡](02_service_discovery_proxies.md)
