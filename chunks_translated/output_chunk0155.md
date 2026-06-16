## **交换机与桥 (Switches and Bridges)**

交换机 (Switch) 提供扇出或聚合能力，允许将更多设备挂接到单个 PCIe 端口 (PCI Express Port)。它们充当分组路由器的角色，能够根据地址或其他路由信息识别给定分组需要经过的路径。

桥 (Bridge) 提供与其他总线（例如 PCI 或 PCI-X）的接口，甚至可以连接到另一条 PCIe 总线。第 47 页"PCIe 拓扑示例"中所示的桥有时被称为"前向桥 (forward bridge)"，它允许将较旧的 PCI 或 PCI-X 卡插入新系统中。相反的类型，或称为"反向桥 (reverse bridge)"，则允许将新的 PCIe 卡插入到旧的 PCI 系统中。

**48**

**第 2 章：PCIe 架构概述**
