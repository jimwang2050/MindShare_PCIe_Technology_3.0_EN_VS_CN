## **PCI Express Technology** 

_图 2‐7：配置头 (Configuration Headers)_ 

**==> picture [374 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Header Type 0 Header Type 1<br>256-Byte (used by endpoints) DW (used by bridges) DW<br>Configuration Space<br>(per function) DeviceID VendorID 00 DeviceID VendorID 00<br>RegisterStatus CommandRegister 01 RegisterStatus CommandRegister 01<br>64-Byte Class Code RevisionID 02 Class Code RevisionID 02<br>PCI ConfigurationHeader Space BIST Base Address 0HeaderType LatencyTimer CacheLineSize 0304 BISTBase Address 0HeaderType LatencyTimer CacheLineSize 0304<br>Base Address 1 05 Base Address 1 05<br>Base Address 2 06 Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>Base Address 3 07 SecondaryStatus LimitI/O BaseI/O 07<br>Base Address 4 08 MemoryLimit MemoryBase 08<br>Function-Specific192-Byte CardBus CIS PointerBase Address 5 0910 Memory LimitPrefetchablePrefetchable BaseUpper 32 BitsMemory BasePrefetchable 0910<br>Configuration Subsystem ID SubsystemVendor ID 11 Prefetchable LimitUpper 32 Bits 11<br>Header Space Expansion ROM 12 I/O Limit I/O Base 12<br>Base Address Upper 16 Bits Upper 16 Bits<br>Reserved CapabilitiesPointer 13 Reserved CapabilityPointer 13<br>Reserved 14 Expansion ROM Base Address 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 ControlBridge InterruptPin InterruptLine 15<br>**----- End of picture text -----**<br>

为了说明系统向软件呈现的方式，请参考图 2‐8（第 51 页）中所示的示例拓扑结构。与之前一样，根复合体 (Root) 位于层级结构的顶部。根复合体在内部可能相当复杂，但通常会实现一个内部总线结构以及多个桥 (Bridge) 以将拓扑扩展到多个端口。该内部总线对配置软件呈现为 PCI 总线编号 0，而 PCIe 端口则呈现为 PCI‐to‐PCI 桥 (PCI-PCI Bridge)。这种内部结构实际上可能并不是真正的 PCI 总线，但对软件而言它在此用途上呈现为 PCI 总线。由于该总线是根复合体内部的，其实际的逻辑设计不必遵循任何标准，可以是供应商专有的。 

**50** 

**第 2 章：PCIe 架构概述 (PCIe Architecture Overview)** 

_图 2‐8：拓扑示例 (Topology Example)_ 

**==> picture [345 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host<br>CPU Bridge<br>Internal Bus 0<br>Root Complex<br>Memory<br>PCI-PCI PCI-PCI PCI-PCI<br>Bridge Bridge Bridge<br>PCIe<br>Switch Endpoint PCIe<br>Bridge<br>to PCI<br>or PCI-X<br>PCIe PCIe Legacy<br>PCI/PCI-X<br>Endpoint Endpoint Endpoint<br>**----- End of picture text -----**<br>

类似地，图 2‐9（第 52 页）中所示的交换机 (Switch) 的内部组织结构对软件而言也仅仅呈现为一组共享同一条总线的桥 (Bridge)。这种方法的一个主要优点是它允许事务路由以与 PCI 相同的方式进行。枚举 (Enumeration)，即配置软件发现系统拓扑并分配总线编号和系统资源的过程，其工作方式也是相同的。我们稍后会看到一些枚举工作方式的示例，但一旦完成枚举，系统中的总线编号将会以类似于图 2‐9（第 52 页）所示的方式进行分配。 

**51** 

**PCI Express Technology** 

_图 2‐9：系统枚举示例结果 (Example Results of System Enumeration)_ 

**==> picture [264 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCI-PCI<br>Bridge<br>Internal Bus 2<br>PCI-PCI PCI-PCI PCI-PCI<br>Bridge Bridge Bridge<br>CPU<br>Root Complex<br>(internal bus 0) Memory<br>Bus 1 Bus 6 Bus 7<br>PCIe Bus 3 Switch EndpointPCIe BridgePCIe<br>Endpoint to PCI<br>Bus 4 Bus 5 or PCI-X<br>PCIe Legacy<br>Endpoint Endpoint PCI/PCI-X<br>Bus 8<br>Legend<br>Downstream port<br>Upstream port<br>**----- End of picture text -----**<br>