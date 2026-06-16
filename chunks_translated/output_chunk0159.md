## **系统示例**

第 53 页的图 2-10 展示了一个基于 PCIe 系统的示例,该系统面向消费级台式机等低成本应用。系统实现了若干 PCIe 端口以及一些插卡插槽,但其基础架构与传统的 PCI 系统相比并无太大差异。

相比之下,第 54 页的图 2-11 所示的高端服务器系统则展示了内置的其他网络接口。在 PCIe 诞生之初,曾有人设想让它作为一种网络来替代那些较老的协议。毕竟,如果 PCIe 基本上是其他网络协议的简化版本,难道它不能胜任所有需求吗?由于种种原因,这一设想始终未能获得广泛认可,基于 PCIe 的系统在连接外部网络时通常仍采用其他传输方式。

**52**

**第 2 章:PCIe 架构概览**

这也让我们有机会重新审视"根复合体 (Root Complex) 由什么构成"这一问题。在本例中,标注为"Intel 处理器"的模块包含了众多组件,这在现代 CPU 架构中很常见。该模块包含一个 x16 PCIe 端口用于访问图形,以及 2 条 DRAM 通道,也就是说内存控制器和一些路由逻辑已被集成到 CPU 封装内部。这些资源通常被统称为"Uncore"(非核)逻辑,以区别于封装内的若干 CPU 核心及其相关逻辑。由于我们之前将根复合体 (Root) 描述为 CPU 与 PCIe 拓扑之间的接口,因此根复合体 (Root) 的一部分必然位于 CPU 封装内部。如第 54 页图 2-11 中的虚线所示,此处的根复合体 (Root) 由多个封装的部分共同组成。这种情况在未来的许多系统设计中很可能会成为常态。

_图 2-10:低成本 PCIe 系统_

**==> picture [376 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe<br>Graphics<br>DDR3<br>GFX Intel Processor<br>DDR3<br>DMI (very similar to PCIe)<br>Serial ATA<br>HiDef Audio<br>HDD<br>USB 2.0 P55 PCH  Video<br>"Ibex Peak"<br>SPI<br>BIOS<br>Gb<br>Add-in Add-in Add-in<br>Ethernet<br>PCIe ports<br>**----- End of picture text -----**

**53**

**PCI Ex ress Technolo p gy**

_图 2-11:服务器 PCIe 系统_

**==> picture [369 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>
Intel Processor<br>PCIe DDR3<br>Uncore<br>GFX<br>DDR3<br>QPI<br>IOH Root Complex<br>10 Gb<br>LAN Switch Ethernet Switch Fibre<br>Endpoint Channel<br>Endpoint Endpoint<br>10 Gb PCI Express SAS/SATA<br>Add-In Switch Ethernet to-PCI<br>RAID<br>Endpoint Endpoint<br>Endpoint<br>PCI<br>Add-In EthernetGb IEEE Slots<br>1394<br>Endpoint Endpoint<br>**----- End of picture text -----**
