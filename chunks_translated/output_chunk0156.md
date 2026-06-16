## **原生 PCIe 端点与 Legacy PCIe 端点** 

端点是 PCIe 拓扑中既不是交换机 (Switch) 也不是桥 (Bridge) 的设备,在总线上作为事务的发起方 (Requester) 和完成方 (Completer)。它们位于树形拓扑分支的末端,并且只实现一个上游端口 (Upstream Port,朝向根复合体 (Root))。相比之下,一个交换机 (Switch) 可能有多个下游端口 (Downstream Port),但只能有一个上游端口 (Upstream Port)。那些原本为 PCI‐X 等老式总线设计、但现在增加了 PCIe 接口的设备,在配置寄存器中将自身标识为"Legacy PCIe 端点 (Legacy PCIe Endpoint)",这种拓扑中就包含此类设备。它们使用了一些在较新的 PCIe 设计中已被禁止的特性,例如 I/O 空间 (I/O Space) 及其 I/O 事务 (IO Transaction) 支持,或者锁定请求 (Locked Request) 支持。相对而言,"原生 PCIe 端点 (Native PCIe Endpoint)"则是完全从零开始设计的 PCIe 设备,而不是为旧式 PCI 设备增加 PCIe 接口。原生 PCIe 端点设备是内存映射设备 (MMIO 设备)。
