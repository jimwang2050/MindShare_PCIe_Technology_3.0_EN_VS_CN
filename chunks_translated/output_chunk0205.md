## **PCI 兼容空间**

在接下来的讨论中,请参阅第 89 页的图 3‐2。256 字节的 PCI 兼容配置空间之所以这样命名,是因为它最初是为 PCI 设计的。该空间的前 16 个双字(64 字节)是配置头部(头部类型 0 或头部类型 1)。除了使用类型 1 头部的桥功能(桥 (Bridge))外,所有功能(端点 (Endpoint))都必须实现类型 0 头部。剩余的 48 个双字用于可选寄存器,包括 PCI 能力结构。对于 PCIe 功能(端点 (Endpoint)),某些能力结构是必需的。例如,PCIe 功能(端点 (Endpoint))必须实现以下能力结构:

- PCI Express 能力结构 (Capability)

- 电源管理 (Power Management)

- MSI (消息信号中断) 和/或 MSI-X (扩展消息信号中断)

**88**

**第 3 章:配置概述**

_图 3‐2:PCI 兼容配置寄存器空间_

**==> picture [376 x 263] intentionally omitted <==**

**----- Start of picture text -----**<br>
256-Byte Type 0 Header Type 1 Header<br>Configuration Register Byte Doubleword Byte Doubleword<br>Space (per Function) 3 2 1 0 3 2 1 0<br>Device ID Vendor ID 00 Device ID Vendor ID 00<br>Status Command 01 Status Command 01<br>64-Bytes<br>PCI Configuration Class Code RevisionID 02 Class Code RevisionID 02<br>Header Space BIST HeaderType LatencyTimer Cache LineSize 03 BIST HeaderType LatencyTimer Cache LineSize 03<br>Base Address 0 04 Base Address 0 04<br>Base Address 1 05 Base Address 1 05<br>Base Address 2 06 Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>Base Address 3 07 Secondary Status I/O Limit I/O Base 07<br>Base Address 4 08 Memory Limit Memory Base 08<br>Base Address 5 09 Prefetchable Prefetchable 09<br>192-Bytes Memory Limit Memory Base<br>Capability CardBus CIS Pointer 10 Prefetchable Base - Upper 32-bits 10<br>Structures Subsystem ID SubsystemVendor ID 11 Prefetchable Limit - Upper 32-bits 11<br>Expansion ROM Base Address 12 Upper 16-bitsI/O Limit Upper 16-bitsI/O Base 12<br>Reserved CapabilitiesPointer 13 Reserved CapabilitiesPointer 13<br>Reserved 14 Expansion ROM Base Address 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 Bridge Control InterruptPin InterruptLine 15<br>Required Config Registers<br>**----- End of picture text -----**<br>