# 📘 第 5 章　TLP 元素 (Chapter 5. TLP Elements)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0230.md` ... `chunks/chunk0243.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [TLP Elements](#-本章目录-table-of-contents)

<a id="sec-5-1"></a>
## 5.1 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

the device itself. This means these internal locations need to be _addressable_ . Soft‐ ware must be able to perform a read or write operation with an address that will access the appropriate internal location within the targeted device. In order to make this work, these internal locations need to be assigned addresses from one of the address spaces supported in the system. 

PCI Express supports the exact same three address spaces that were supported in PCI: 

- Configuration 

- Memory 

- IO 

## **Configuration Space** 

As we saw in Chapter 1, configuration space was introduced with PCI to allow software to control and check the status of devices in a standardized way. PCI Express was designed to be software backwards compatible with PCI, so config‐ uration space is still supported and used for the same reason as it was in PCI. More info about configuration space (purpose of, how to access, size, contents, etc.) can be found in Chapter 3. 

Even though configuration space was originally meant to hold standardized structures (PCI‐defined headers, capability structures, etc.), it is very common for PCIe devices to have device‐specific registers mapped into their config space. In these cases, the device‐specific registers mapped into config space are often control, status or pointer registers as opposed to data storage locations. 

## **Memory and IO Address Spaces** 

## **General** 

In the early days of PCs, the internal registers/storage in IO devices were accessed via IO address space (as defined by Intel). However, because of several limitations and undesirable effects related to IO address space, that we will not be going into here, that address space quickly lost favor with software and hardware vendors. This resulted in the internal registers/storage of IO devices being mapped into memory address space (commonly referred to as memory‐ mapped IO, or MMIO). However, because early software was written to use IO address space to access internal registers/storage on IO devices, it became com‐ mon practice to map the same set of device‐specific registers in memory 

**122** 

**Chapter 4: Address Space & Transaction Routing** 

address space as well as in IO address space. This allows new software to access the internal locations of a device using memory address space (MMIO), while allowing legacy (old) software to continue to function because it can still access the internal registers of devices using IO address space. 

Newer devices that do not rely on legacy software or have legacy compatibility issues typically just map internal registers/storage through memory address space (MMIO), with no IO address space being requested. In fact, the PCI Express specification actually discourages the use of IO address space, indicat‐ ing that it is only supported for legacy reasons and may be deprecated in a future revision of the spec. 

A generic memory and IO map is shown in Figure 4‐1 on page 125. The size of the memory map is a function of the range of addresses that the system can use (often dictated by the CPU addressable range). The size of the IO map in PCIe is limited to 32 bits (4GB), although in many computers using Intel‐compatible (x86) processors, only the lower 16 bits (64KB) are used. PCIe can support mem‐ ory addresses up to 64 bits in size. 

The mapping example in Figure 4‐1 is only showing MMIO and IO space being claimed by Endpoints, but that ability is not exclusive to Endpoints. It is very common for Switches and Root Complexes to also have device‐specific registers accessed via MMIO and IO addresses. 

## **Prefetchable vs. Non-prefetchable Memory Space** 

Figure 4‐1 shows two different types of MMIO being claimed by PCIe devices: Prefetchable MMIO (P‐MMIO) and Non‐Prefetchable MMIO (NP‐MMIO). It’s important to describe the distinction between prefetchable and non‐prefetch‐ able memory space. Prefetchable space has two very well defined attributes: 

- Reads do not have side effects 

- Write merging is allowed 

Defining a region of MMIO as prefetchable allows the data in that region to be speculatively fetched ahead in anticipation that a Requester might need more data in the near future than was actually requested. The reason it’s safe to do this minor caching of the data is that reading the data doesn’t change any state info at the target device. That is to say there are no side effects from the act of reading the location. For example, if a Requester asks to read 128 bytes from an address, the Completer might prefetch the next 128 bytes as well in an effort to improve performance by having it on hand when it’s requested. However, if the Requester never asks for the extra data, the Completer will eventually have to 

**123** 

## **PCI Express Technology** 

discard it to free up the buffer space. If the act of reading the data changed the value at that address (or had some other side effect), it would be impossible to recover the discarded data. However, for prefetchable space, the read had no side effects, so it is always possible to go back and get it later since the original data would still be there. 

You may be wondering what sort of memory space might have read side effects? One example would be a memory‐mapped status register that was designed to automatically clear itself when read to save the programmer the extra step of explicitly clearing the bits after reading the status. 

Making this distinction was more important for PCI than it is for PCIe because transactions in that bus protocol did not include a transfer size. That wasn’t a problem when the devices exchanging data were on the same bus, because there was a real‐time handshake to indicate when the requester was finished and did not need anymore data, therefore knowing the byte count wasn’t so important. But when the transfer had to cross a bridge it wasn’t as easy because for reads, the bridge would need to guess the byte count when gathering data on the other bus. Guessing wrong on the transfer size would add latency and reduce performance, so having permission to prefetch could be very helpful. That’s why the notion of memory space being designated as prefetchable was helpful in PCI. Since PCIe requests do include a transfer size it’s less interesting than it was, but it’s carried forward for backward compatibility. 

**124** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐1: Generic Memory And IO Address Maps_ 

**==> picture [300 x 354] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>Memory<br>(DRAM)<br>Switch<br>Memory Map<br>2 [32]  or 2 [64]<br>MMIO<br>Legacy PCIe<br>(Prefetchable)<br>Endpoint Endpoint<br>MMIO (NP) MMIO (P)<br>MMIO<br>IO MMIO (NP) (Non-Prefetchable)<br>PCIe Functions may have registers<br>and buffers mapped into IO and<br>Memory address space<br>2 [32] IO Map System<br>Memory<br>(DRAM)<br>IO<br>Ports<br>2 [16]<br>0 0<br>**----- End of picture text -----**<br>


**125** 

**PCI Express Technology** 

## **Base Address Registers (BARs)** 

## **General** 

Each device in a system may have different requirements in terms of the amount and type of address space needed. For example, one device may have 256 bytes worth of internal registers/storage that should be accessible through IO address space and another device may have 16KB of internal registers/stor‐ age that should be accessible through MMIO. 

PCI‐based devices are not allowed to decide on their own, which addresses should be used to access their internal locations, that is the job of system soft‐ ware (i.e. BIOS and OS kernel). So the devices must provide a way for system software to determine the address space needs of the device. Once software knows what the device’s requirements are in terms of address space, then assuming the request can be fulfilled, software will simply allocate an available range of addresses, of the appropriate type (IO, NP‐MMIO or P‐MMIO), to that device. 

This is all accomplished through the Base Address Registers (BARs) in the header of configuration space. As shown in Figure 4‐2 on page 127, a Type 0 header has six BARs available (each one being 32 bits in size), while a Type 1 header has only two BARs. Type 1 headers are found in all bridge devices, which means every switch port and root complex port has a Type 1 header. Type 0 headers are in non‐bridge devices like endpoints. An example of this can be seen in Figure 4‐3 on page 128. 

System software must first determine the size and type of address space being requested by a device. The device designer knows the collective size of the internal registers/storage that should be accessible via IO or MMIO. The device designer also knows how the device will behave when those registers are accessed (i.e. do reads have side‐effects or not). This will determine whether prefetchable MMIO (reads have no side‐effects) or non‐prefetchable MMIO (reads do have side‐effects) should be requested. Knowing this information, the device designer hard‐codes the lower bits of the BARs to certain values indicat‐ ing the type and size of the address space being requested. 

The upper bits of the BARs are writable by software. Once system software checks the lower bits of the BARs to determine the size and type of address space requested, system software will then write the base address of the address range being allocated to this device into the upper bits of the BAR. Since a single 

**126** 

**Chapter 4: Address Space & Transaction Routing** 

Endpoint (Type 0 header) has six BARs, up to six different address space requests can be made. However, this is not common in the real world. Most devices will request 1‐3 different address ranges. 

Not all BARs have to be implemented. If a device does not need all the BARs to map their internal registers, the extra BARs are hard‐coded with all 0’s notifying software that these BARs are not implemented. 

_Figure 4‐2: BARs in Configuration Space_ 

**==> picture [386 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Header Type 1 Header<br>31 23 15 7 0 31 23 15 7 0<br>Device ID Vendor ID 00h Device ID Vendor ID 00h<br>Status Command 04h Status Command 04h<br>Class Code   Rev 08h Class Code   Rev 08h<br>      ID       ID<br>BIST Header Latency Cache 0Ch BIST Header Latency Cache 0Ch<br>Type Timer Line Size Type Timer Line Size<br>Base Address 0 (BAR0) 10h Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h Base Address 1 (BAR1) 14h<br>Base Address 2 (BAR2) 18h SecondaryLat Timer SubordinateBus # SecondaryBus # PrimaryBus # 18h<br>Base Address 3 (BAR3) 1Ch SecondaryStatus LimitIO BaseIO 1Ch<br>Base Address 4 (BAR4) 20h (Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Prefetchable Prefetchable<br>Base Address 5 (BAR5) 24h Memory Limit Memory Base 24h<br>CardBus CIS Pointer 28h Prefetchable Memory Base 28h<br>Upper 32 Bits<br>SubsystemDevice ID SubsystemVendor ID 2Ch Prefetchable Memory LimitUpper 32 Bits 2Ch<br>IO Limit IO Base<br>Expansion ROM Base Address 30h Upper 16 Bits Upper 16 Bits 30h<br>Reserved Capability 34h Reserved Capability 34h<br>Pointer Pointer<br>Reserved 38h Expansion ROM Base Address 38h<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch ControlBridge InterruptPin InterruptLine 3Ch<br>**----- End of picture text -----**<br>


Once the BARs have been programmed, the internal registers or local memory within the device can be accessed via the address ranges programmed into the BARs. Anytime the device sees a request with an address that maps to one of its BARs, it will accept that request because it is the target. 

**127** 

**PCI Express Technology** 

_Figure 4‐3: PCI Express Devices And Type 0 And Type 1 Header Use_ 

**==> picture [278 x 256] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

此时，BAR3 的配置完成。一旦软件在 Command 寄存器（偏移 04h）中启用 IO 地址解码，该设备将接受并响应该范围内 4000h - 40FFh（大小为 256 字节）的 IO 事务。

**133**

## **PCI Express Technology**

_图 4-6：IO BAR 设置_

**==> picture [389 x 485] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 头<br>
31 23 15 7 0<br>
未初始化的 IO BAR<br>
设备 ID 厂商 ID 00h 31 8 2 1 0<br>
状态 命令 04h XXXX XXXX XXXX XXXX XXXX XXXX 0000 00 0 1 (1)<br>
类代码   修订 08h<br>
      ID<br>
BIST 头 延迟 缓存 0Ch IO BAR 写入全 1<br>
类型 定时器 行大小 31 8 2 1 0<br>
基地址 0 (BAR0) 10h 1111 1111 1111 1111 1111 1111 0000 00 0 1 (2)<br>
基地址 1 (BAR1) 14h<br>
基地址 2 (BAR2) 18h IO BAR 写入基地址<br>
31 8 2 1 0<br>
基地址 3 (BAR3) 1Ch<br>
0000 0000 0000 0000 0100 0000 0000 00 0 1 (3)<br>
基地址 4 (BAR4) 20h (0) (0) (0) (0) (4) (0)<br>
基地址 5 (BAR5) 24h 0 = 内存请求<br>
1 = IO 请求<br>
CardBus CIS 指针 28h<br>
保留 (0)<br>
子系统设备 ID 子系统厂商 ID 2Ch<br>
256 字节对齐的<br>
扩展 ROM 基址 30h 起始地址的高 24 位（低 7 位假定为 = 0）<br>
(0000 4000h)<br>
保留 能力 34h<br>
指针<br>
保留 38h 本例：<br>
- 256 字节 IO 地址空间<br>
最大延迟 最小授权 中断引脚 中断线 3Ch - 软件在 IO 地址映射中分配 16KB 处的起始地址。<br>
注意：只有传统 PCIe 设备才应请求 IO<br>
地址空间。<br>
表 4-3：向 IO BAR 写入全 1 后读取 IO BAR 的结果<br>
BAR 位 含义<br>
0 读为 1b，表示 IO 请求。由于这是 IO 请求，bit 1<br>
保留。<br>
1 保留。硬编码为 0b。<br>
7:2 读为 0s，表示请求的大小（这些位被硬编码为 0）<br>
31:8 读为 1s，因为软件尚未用起始地址对高位<br>
进行编程。请注意，由于 bit 8 是最低<br>
有效可写位，IO 请求大小为 2 [8]，即 256 字节。<br>**----- End of picture text -----**<br>


**134**

**第 4 章：地址空间与事务路由**

## **必须按顺序评估所有 BAR**

在经历了前面三个示例后，很明显软件必须按顺序评估 BAR。

大多数时候，功能不需要所有六个 BAR。即使在我们经历的示例中，也只使用了六个可用 BAR 中的四个。如果示例中的功能不需要请求任何其他地址空间，则设备设计者将 BAR4 和 BAR5 的所有位硬编码为 0。因此即使软件将这些 BAR 写入全 1，写入也不会产生影响。评估 BAR3 后，软件将继续评估 BAR4。一旦检测到没有任何位被置位，软件就会知道此 BAR 未使用并继续评估下一个 BAR。

必须评估所有 BAR，即使软件发现某个 BAR 未使用。PCI 或 PCIe 中没有规则规定 BAR0 必须是用于地址空间请求的第一个 BAR。如果设备设计者愿意，他们可以使用 BAR4 进行地址空间请求，并将 BAR0、BAR1、BAR2、BAR3 和 BAR5 硬编码为全 0。这意味着软件必须评估头中的每个 BAR。

## **可调整大小的 BAR**

PCI Express 规范的 2.1 版本增加了通过在扩展配置空间中定义新的能力结构来更改 BAR 中请求的地址空间的大小的支持。新结构允许功能公布其可以操作的地址空间大小，然后由软件根据可用系统资源启用其中一个大小。例如，如果功能理想地希望具有 2GB 的可预取内存地址空间，但它仍然可以仅使用 1GB、512MB 或 256MB 的 P-MMIO 进行操作，则如果软件无法满足较大大小的请求，则系统软件可能仅允许该功能请求 256MB 的地址空间。

**135**

**PCI Express Technology**

## **基址和上限寄存器**

## **概述**

一旦功能的 BAR 被编程，该功能就知道它拥有哪些地址范围，这意味着该功能将声明它看到的针对其所拥有地址范围（即编程到其某个 BAR 中的地址范围）的任何事务。这是好的，但重要的是要认识到，该功能要"看到"它应该声明的事务的唯一方法是，如果它上游的桥将这些事务向下转发到目标功能所连接的适当链路。因此，每个桥（例如交换机端口和根复合体端口）需要知道其下方的地址范围，以便它可以确定哪些请求应从其主接口（上游侧）转发到其二级接口（下游侧）。如果请求针对的地址由桥下方的功能中的 BAR 拥有，则请求应转发到桥的二级接口。

Type 1 头中的 Base 和 Limit 寄存器使用位于该桥下方的地址范围进行编程。每个 Type 1 头中有三组 Base 和 Limit 寄存器。需要三组寄存器，因为桥下可能存在三个单独的地址范围：

- 可预取内存空间 (P-MMIO)

- 非可预取内存空间 (NP-MMIO)

- IO 空间 (IO)

为了解释这些 Base 和 Limit 寄存器是如何工作的，让我们继续上一节的示例，并将该已编程功能（端点）放置在交换机下，如图 4-7（第 137 页）所示。该图还列出了该功能的 BAR 所拥有的地址范围。

端点上游每个桥的 Base 和 Limit 寄存器都需要编程，但首先，我们将关注连接到端点的桥（端口 B）。

**136**

**第 4 章：地址空间与事务路由**

_图 4-7：设置基址和上限值的示例拓扑_

**==> picture [301 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体 系统内存<br>
P2P (DRAM)<br>
端口<br>
A<br>
P2P<br>
交换机<br>
端口 端口<br>
B C<br>
PCIe PCIe<br>
端点 端点<br>
BAR0：NP-MMIO (4KB)<br>
F900_0000h - F900_0FFFh<br>
BAR1-2：P-MMIO (64MB)<br>
2_4000_0000h - 243FF_FFFFh<br>
BAR3：IO (256 字节)<br>
4000h - 40FFh<br>
BAR4-5：未使用（全 0）<br>
P2P P2P<br>**----- End of picture text -----**<br>


## **可预取范围 (P-MMIO)**

Type 1 头具有两对可预取内存基址/上限寄存器。可预取内存基址/上限寄存器存储可预取地址范围低 32 位的地址信息。如果此桥支持 64 位地址解码，则还使用可预取内存基址/上限高 32 位寄存器，并保存地址范围的高 32 位（位 [63:32]）。第 138 页图 4-8 显示了软件将编程到这些寄存器中的值，以指示 2_4000_0000h - 2_43FF_FFFFh 的可预取地址范围位于该桥（端口 B）下方。这些寄存器中每个字段的含义汇总在表 4-4 中。

**137**

**PCI Express Technology**

_图 4-8：可预取内存基址/上限寄存器值示例_

**==> picture [368 x 305] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 头<br>
31 23 15 7 0 可预取基址 可预取<br>
设备 ID 厂商 ID 00h 高 32 位 内存基址<br>
31 0 15 3 0<br>
状态 命令 04h 0000 0000 0000 0000 0000 0000 0000 0010 0100 0000 0000 0001<br>
类代码       ID 修订 08h (0) (0) (0) (0) (0) (0) (0) (2) (4) (0) (0) (RO)<br>
0h = 32 位<br>
BIST 头类型 延迟定时器 行大小 缓存 0Ch 可预取基址(RW) 可预取基址的位 63:32(RW) 位 31:20 1h = 64 位<br>
基址 0 (BAR0) 10h<br>
基址 1 (BAR1) 14h 可预取范围<br>
二级 下属 二级 主 18h 基址 0000 0002 4000 0000h<br>
延迟定时器 总线号 总线号 总线号 位 19:0 对基址始终为 0<br>
二级状态 上限 IO 基址 IO 1Ch<br>
(非可预取)内存上限 (非可预取)内存基址 20h<br>
内存上限 可预取内存基址 可预取 24h 可预取上限<br>
可预取内存基址 28h 高 32 位 内存上限 可预取<br>
可预取内存上限 2Ch 31 0 15 3 0<br>
高 32 位 0000 0000 0000 0000 0000 0000 0000 0010 0100 0011 1111 0001<br>
IO 上限 IO 基址 (0) (0) (0) (0) (0) (0) (0) (2) (4) (3) (F) (RO)<br>
高 16 位 高 16 位 30h (RW) 可预取基址的位 63:32 (RW) 可预取基址的位 31:20 0h = 32 位<br>
1h = 64 位<br>
保留 能力 34h<br>
指针<br>
扩展 ROM 基址 38h<br>
可预取范围<br>
桥控制 中断引脚 中断线 3Ch 上限地址 0000 0002 43FF FFFFh<br>
位 19:0 对上限始终为 F<br>
可预取内存范围：2_4000_0000h - 2_43FF_FFFFh<br>**----- End of picture text -----**<br>


**138**

**第 4 章：地址空间与事务路由**

_表 4-4：可预取内存基址/上限寄存器含义示例_

|**寄存器**|**值**|**用途**|
|---|---|---|
|可预取内存基址|4001h|此寄存器的高 12 位保存 32 位 BASE 地址的高 12 位（位 [31:20]）。基址的低 20 位隐含为全 0，意味着基址始终在 1MB 边界上对齐。<br>此寄存器的低 4 位指示桥中是否支持 64 位地址解码器，意味着使用上基址/上限寄存器。|
|可预取内存上限|43F1h|类似地，此寄存器的高 12 位保存 32 位 LIMIT 地址的高 12 位（位 [31:20]）。上限地址的低 20 位均隐含为全 F。<br>此寄存器的低 4 位与基址寄存器的低 4 位含义相同。|
|可预取内存基址高 32 位|00000002h|保存此端口下游可预取内存 64 位 BASE 地址的高 32 位。|
|可预取内存上限高 32 位|00000002h|保存此端口下游可预取内存 64 位 LIMIT 地址的高 32 位。|



## **非可预取范围 (NP-MMIO)**

与可预取内存范围不同，非可预取内存范围仅支持 32 位地址。因此基址和上限各只有一个寄存器。按照图 4-7 中的示例，端口 B 的非可预取内存基址/上限寄存器将使用图 4-9（第 140 页）所示的值进行编程。这些值的含义汇总在表 4-5 中。

**139**

**PCI Express Technology**

_图 4-9：非可预取内存基址/上限寄存器值示例_

**==> picture [375 x 360] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 头<br>
31 23 15 7 0 (非可预取)<br>
设备 ID 厂商 ID 00h 内存基址<br>
15 3 0<br>
状态 命令 04h<br>
1111 1001 0000 0000<br>
类代码       ID 修订 08h (F) (9) (0) (RO)<br>
BIST 头 延迟 缓存 0Ch (RW) 必须为 0<br>
类型 定时器 行大小 非可预取基址的位 31:20<br>
基址 0 (BAR0) 10h<br>
基址 1 (BAR1) 14h 非可预取<br>
F900 0000h<br>
二级 下属 二级 主 18h 范围 基址<br>
延迟定时器 总线号 总线号 总线号 位 19:0 对基址始终为 0<br>
二级 状态 IO 上限 IO 基址 1Ch<br>
(非可预取) (非可预取) 20h<br>
内存上限 内存基址<br>
可预取 可预取 24h (非可预取)<br>
内存上限 内存基址 内存上限<br>
可预取内存基址 28h 15 3 0<br>
高 32 位<br>
1111 1001 0000 0000<br>
可预取内存上限 2Ch<br>
高 32 位 (F) (9) (0)<br>
IO 上限 IO 基址 (RO)<br>
高 16 位 高 16 位 30h (RW) 必须为 0<br>
非可预取上限地址的位 31:20<br>
保留 能力 34h<br>
指针<br>
扩展 ROM 基址 38h<br>
非可预取<br>
桥控制 中断引脚 中断线 3Ch 范围 上限地址 F90F FFFFh<br>
位 19:0 对上限始终为 F<br>
非可预取内存范围：F900_0000h - F90F_FFFFh<br>**----- End of picture text -----**<br>


**140**

**第 4 章：地址空间与事务路由**

_表 4-5：非可预取内存基址/上限寄存器含义示例_

|**寄存器**|**值**|**用途**|
|---|---|---|
|(非可预取) 内存基址|F900h|此寄存器的高 12 位保存 32 位 BASE 地址的高 12 位（位 [31:20]）。基址的低 20 位隐含为全 0，意味着基址始终在 1MB 边界上对齐。<br>此寄存器的低 4 位必须为 0。|
|(非可预取) 内存上限|F900h|类似地，此寄存器的高 12 位保存 32 位 LIMIT 地址的高 12 位（位 [31:20]）。上限地址的低 20 位均隐含为全 F。<br>此寄存器的低 4 位必须为 0。|



此示例展示了一个有趣的情况，其中在端口 B 的配置空间中编程的非可预取地址范围指示的范围（1MB）远大于位于下游的端点所拥有的 NP-MMIO 范围（4KB）。这是因为 Type 1 头中的内存基址/上限寄存器只能用于指定地址位 20 及以上（[31:20]）。低 20 地址位 [19:0] 是隐含的。因此可以使用内存基址/上限寄存器指定的最小地址范围是 1MB。

在我们的示例中，端点请求并被授予了 4KB 的 NP-MMIO（F900_0000h - F900_0FFFh）。端口 B 已使用指示 1MB（或 1024KB）NP-MMIO 位于该端口下游的值编程（F900_0000h - F90F_FFFFh）。这意味着浪费了 1020KB（F900_1000h - F90F_FFFFh）的内存地址空间。此地址空间不能分配给另一个端点，因为数据包的路由将无法工作。

## **IO 范围**

与可预取内存范围一样，Type 1 头具有两对 IO 基址/上限寄存器。IO 基址/上限寄存器存储 IO 地址范围低 16 位的地址信息。如果此桥支持解码 32 位 IO 地址（这在实际设备中很少见），则还使用 IO 基址/上限高 16 位寄存器，并保存 IO 地址范围的高 16 位（位 [31:16]）。

**141**

**PCI Express Technology**

按照我们的示例，第 142 页图 4-10 显示了软件将编程到这些寄存器中的值，以指示 4000h - 4FFFh 的 IO 地址范围位于该桥（端口 B）下方。这些寄存器中每个字段的含义汇总在表 4-6 中。

_图 4-10：IO 基址/上限寄存器值示例_

**==> picture [381 x 340] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 头<br>
31 23 15 7 0 IO 基址<br>
设备 ID 厂商 ID 00h 高 16 位 IO 基址<br>
15 0 7 3 0<br>
状态 命令 04h<br>
0000 0000 0000 0000 0100 0000<br>
类代码       ID 修订 08h (0) (0) (0) (0) (4) (RO)<br>
BIST 头类型 延迟定时器 行大小 缓存 0Ch (RW) IO 基址的位 31:16 (RW) IO 基址的位 15:12 0h = 16 位 1h = 32 位<br>
(如果使用)<br>
基址 0 (BAR0) 10h<br>
基址 1 (BAR1) 14h IO 范围<br>
二级 下属 二级 主 18h 基址 4000h<br>
延迟定时器 总线号 总线号 总线号 位 11:0 对 IO 基址始终为 0<br>
二级状态 IO 上限 IO 基址 1Ch<br>
(非可预取)内存上限 (非可预取)内存基址 20h<br>
内存上限 可预取内存基址 可预取 24h 高 16 位 IO 上限 IO 上限<br>
可预取内存基址 28h 15 0 7 3 0<br>
高 32 位<br>
0000 0000 0000 0000 0100 0000<br>
可预取内存上限高 32 位 2Ch (0) (0) (0) (0) (4) (RO)<br>
高 16 位 IO 上限 高 16 位 IO 基址 30h (RW) IO 上限地址的位 31:16 (RW) IO 上限地址的位 15:12 0h = 16 位 1h = 32 位<br>
保留 能力指针 34h (如果使用)<br>
扩展 ROM 基址 38h<br>
IO 范围<br>
桥控制 中断引脚 中断线 3Ch 上限地址 4FFFh<br>
位 11:0 对 IO 上限始终为 F<br>
IO 范围：4000h - 4FFFh<br>**----- End of picture text -----**<br>


**142**

**第 4 章：地址空间与事务路由**

_表 4-6：IO 基址/上限寄存器含义示例_

|**寄存器**|**值**|**用途**|
|---|---|---|
|IO 基址|40h|此寄存器的高 4 位保存 16 位 BASE 地址的高 4 位（位 [15:12]）。基址的低 12 位隐含为全 0，意味着基址始终在 4KB 边界上对齐。<br>此寄存器的低 4 位指示桥中是否支持 32 位 IO 地址解码器，意味着使用上基址/上限寄存器。|
|IO 上限|40h|类似地，此寄存器的高 4 位保存 16 位 LIMIT 地址的高 4 位（位 [15:12]）。上限地址的低 12 位均隐含为全 F。<br>此寄存器的低 4 位与基址寄存器的低 4 位含义相同。|
|IO 基址高 16 位|0000h|保存此端口下游 IO 的 32 位 BASE 地址的高 16 位。|
|IO 上限高 16 位|0000h|保存此端口下游 IO 的 32 位 LIMIT 地址的高 16 位。|



在此示例中，我们看到另一种情况，即编程到上游桥中的地址范围远远超过下游功能实际拥有的地址范围。在我们的示例中，端点拥有 256 字节的 IO 地址空间（具体为 4000h - 40FFh）。端口 B 已使用指示 4KB IO 地址空间位于下游（地址 4000h - 4FFFh）的值进行编程。同样，这只是 Type 1 头的限制。对于 IO 地址空间，低 12 位（位 [11:0]）具有隐含值，因此可以指定的最小 IO 地址范围是 4KB。此限制结果比内存范围的 1MB 最小窗口更严重。在基于 x86（Intel 兼容）的系统中，处理器仅支持 16 位 IO 地址空间，并且由于只能在桥中指定 IO 地址范围的位 [15:12]，这意味着系统中最多可以有 16 (2[4]) 个不同的 IO 地址范围。

**143**

**PCI Express Technology**

## **未使用的基址和上限寄存器**

并非每个 PCIe 设备都将使用所有三种类型的地址空间。事实上，PCI Express 规范实际上并不鼓励使用 IO 地址空间，表明它仅出于传统原因而受到支持，并可能在规范的未来版本中被弃用。

在端点不请求所有三种类型地址空间的情况下，那些设备上游的桥的基址和上限寄存器被编程为什么？它们不能被编程为全 0，因为低地址位仍将被隐含为不同（基址 = 0s；上限 = Fs），这将表示一个有效范围。因此为了处理这些情况，上限寄存器必须使用比基址更高的地址进行编程。例如，如果端点不请求 IO 地址空间，则该功能紧邻的上游桥将具有编程为 00h 的 IO Base 寄存器和编程为 F0h 的 IO Limit 寄存器。由于上限地址高于基址地址，因此桥理解这是无效设置，并将其解释为其下游没有拥有 IO 地址空间的功能。

这种使基址和上限寄存器无效的方法对所有三对基址和上限寄存器都有效，而不仅仅是对 IO 基址/上限寄存器有效。

## **健全性检查：用于地址路由的寄存器**

为了确保您理解设置 BAR 和 Base/Limit 寄存器的规则和方法，请查看第 145 页图 4-11 以确保它有意义。我们只是简单地将示例系统扩展为包括来自其他端点以及来自某个交换机端口（端口 A）的其他地址空间请求。请记住，Type 1 头也具有 BAR（恰好两个）并且可以请求地址空间。桥中的 Base/Limit 寄存器不包括同一桥的 BAR 拥有的地址。Base/Limit 寄存器仅表示位于该桥下游的地址。

**144**

**第 4 章：地址空间与事务路由**

_图 4-11：最终地址路由设置示例_

**==> picture [370 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
BAR0-1：未使用（全 0）<br>
IO 范围：4000h - 5FFFh<br>
NP-MMIO 范围：F900_0000h - F90F_FFFFh<br>
P-MMIO 范围：2_3E00_0000h - 2_440F_FFFFh<br>
CPU<br>
根复合体 系统内存<br>
P2P (DRAM)<br>
BAR0-1：[P-MMIO (1KB)]<br>
2_3E00_0000h - 2_3E00_03FFh<br>
端口 IO 范围：<br>
A NP-MMIO 范围：<br>
P2P P-MMIO 范围：<br>
交换机<br>
BAR0-1：未使用（全 0） BAR0-1：未使用（全 0）<br>
IO 范围：4000h - 4FFFh 端口 端口 IO 范围：5000h - 5FFFh<br>
NP-MMIO 范围：F900_0000h - F90F_FFFFh B C NP-MMIO 范围：未使用（基址 > 上限）<br>
P-MMIO 范围：2_4000_0000h - 2_43FF_FFFFh P-MMIO 范围：2_4400_0000h - 2_440F_FFFFh<br>
PCIe PCIe<br>
端点 端点<br>
BAR0：NP-MMIO (4KB) BAR0-1：P-MMIO (8KB)<br>
F900_0000h - F900_0FFFh 2_4400_0000h - 2_4400_1FFFh<br>
BAR1-2：P-MMIO (64MB) BAR2-4：未使用（全 0）<br>
2_4000_0000h - 243FF_FFFFh BAR5：IO (4 字节)<br>
BAR3：IO (256 字节) 5000h - 5003h<br>
4000h - 40FFh<br>
BAR4-5：未使用（全 0）<br>
4000h - 5FFFh<br>
F900_0000h - F90F_FFFFh<br>
2_4000_0000h - 2_440F_FFFFh<br>
P2P P2P<br>**----- End of picture text -----**<br>


## **TLP 路由基础**

设置上一节中描述的 BAR 和 Base/Limit 寄存器的目的是确保针对功能的流量被正确路由，以便目标功能可以看到事务并声明它们。在像 PCI 这样的共享总线架构中，所有流量对每个设备都是可见的。仅当目标位于另一条总线上且必须跨越桥时才会发生请求的路由。由于 PCIe 链路是点对点的，因此需要在设备之间传递事务时进行更多的路由。

**145**

## **PCI Express Technology**

_图 4-12：多端口 PCIe 设备具有路由职责_

**==> picture [330 x 297] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体 系统<br>
IN OUT IN OUT 内存<br>
交换机 OUT IN OUT IN<br>
传统<br>
内部使用 端点<br>
?<br>
流量类型：<br>
- 物理层有序集<br>
- 数据链路层包 (DLLP)<br>
- 事务层包 (TLP)<br>
OUT IN OUT IN<br>
    IN = 入口端口<br>
PCIe PCIe OUT = 出口端口<br>
端点 端点<br>
IN OUT<br>
OUT IN<br>**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-2"></a>
## 5.2 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

CPU<br>Root Complex System<br>Memory<br>P2P (DRAM)<br>Type 1 Headers<br>P2P (Virtual PCI-PCI Bridges)<br>Switch<br>Type 0 Headers<br>PCIe PCIe<br>Endpoint Endpoint<br>P2P P2P<br>**----- End of picture text -----**<br>


## **BAR Example 1: 32-bit Memory Address Space Request** 

Figure 4‐4 on page 130 shows the basic steps in setting up a BAR, which in this example, is requesting a 4KB block of non‐prefetchable memory (NP‐MMIO). In the figure, the BAR is shown at three points in the configuration process: 

1. In (1) of Figure 4‐4, we see the uninitialized state of the BAR. The device designer has fixed the lower bits to indicate the size and type, but the upper bits (which are read‐write) are shown as Xs to indicate their value is not known. System software will first write all 1s to every BAR (using config writes) to set all writable bits. (Of course, the hard‐coded lower bits are unaffected by any configuration writes.) The second view of the BAR, 

**128** 

**Chapter 4: Address Space & Transaction Routing** 

shown in (2) of Figure 4‐4, shows how it looks after configuration software has written all 1’s to it. 

Writing all 1s is done to determine what the least‐significant writable bit is. This bit position indicates the size of the address space being requested. In this example, the least‐significant writable bit is bit 12, so this BAR is requesting 2[12] (or 4KB) of address space. If the least significant writable bit would have been bit 20, then the BAR would have been requesting 2[20] (or 1MB) of address space. 

2. After writing all 1s to the BARs, software turns around and reads the value of each BAR, starting with BAR0, to determine the type and size of the address space being requested. Table 4‐1 on page 129 summarizes the results of the configuration read of BAR0 for this example. 

3. The final step in this process is for system software to allocate an address range to BAR0 now that software knows the size and type of the address space being requested. The third view of the BAR, in (3) of Figure 4‐4, shows how it looks after software has written the start address for the allo‐ cated block of addresses. In this example, the start address is F900_0000h. 

At this point the configuration of BAR0 is complete. Once software enables memory address decoding in the Command register (offset 04h), this device will accept any memory requests it receives that fall within the range from F900_0000h ‐ F900_0FFFh (4KB in size). 

_Table 4‐1: Results of Reading the BAR after Writing All 1s To It_ 

|**BAR Bits**|**Meaning**|
|---|---|
|0|Read as 0b, indicating a memory request. Since this is a memory request,<br>bits 3:1 also have an encoded meaning.|
|2:1|Read as 00b indicating the target only supports decoding a 32‐bit<br>address|
|3|Read as 0b, indicating request is for non‐prefetchable memory (meaning<br>reads do have side‐effects); NP‐MMIO|
|11:4|Read as all 0s, indicating the size of the request (these bits are hard‐<br>coded to 0)|
|31:12|Read as all 1s because software has not yet programmed the upper bits<br>with a start address for the block. Since bit 12 is the least significant bit<br>that could be written, the memory size requested is 212= 4KB.|



**129** 

**PCI Express Technology** 

_Figure 4‐4: 32‐Bit Non‐Prefetchable Memory BAR Set Up_ 

## **Type 0 Header** 

**==> picture [364 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 23 15 7 0<br>Device ID Vendor ID 00h Uninitialized BAR<br>31 12 4 3 2 1 0<br>Status Command 04h<br>XXXX XXXX XXXX XXXX XXXX 00000000 0 0 0 0 (1)<br>Class Code   Rev 08h<br>      ID<br>BIST Header Latency Cache 0Ch BAR Written with all 1s<br>Type Timer Line Size 31 12 4 3 2 1 0<br>Base Address 0 (BAR0) 10h 1111 1111 1111 1111 1111 00000000 0 0 0 0 (2)<br>Base Address 1 (BAR1) 14h<br>Base Address 2 (BAR2) 18h BAR Written With Base Address<br>31 12 4 3 2 1 0<br>Base Address 3 (BAR3) 1Ch 1111 1001 0000 0000 0000 00000000 0 0 0 0 (3)<br>Base Address 4 (BAR4) 20h (F) (9) (0) (0) (0)<br>Base Address 5 (BAR5) 24h 0 = Memory request1 = IO request<br>CardBus CIS Pointer 28h 00 = 32-bit decoding<br>10 = 64-bit decoding<br>SubsystemDevice ID SubsystemVendor ID 2Ch 0 = non-prefetchable1 = prefetchable<br>Expansion ROM Base Address 30h<br>Upper 20 bits of 4KB aligned<br>Reserved CapabilityPointer 34h start address (lower 12 bits assumed to be = 0)(F900 0000h)<br>Reserved 38h<br>This Example:<br>Max Lat Min Gnt Interrupt Interrupt 3Ch -4KB of non-prefetchable memory<br>Pin Line -Address range must be below 4GB (32-bit decode)<br>Note: if memory address is assigned below 4GB boundary,<br>the 3DW header must be used when targeting this device.<br>**----- End of picture text -----**<br>


## **BAR Example 2: 64-bit Memory Address Space Request** 

In the previous example, we saw BAR0 being used to request non‐prefetchable memory address space (NP‐MMIO). In this example, as shown in Figure 4‐5 on page 132, BAR1 and BAR2 are being used to request a 64MB block of prefetch‐ able memory address space. Two sequential BARs are being used here because the device supports a 64‐bit address for this request, meaning that software can allocate the requested address space above the 4GB address boundary if it 

**130** 

**Chapter 4: Address Space & Transaction Routing** 

wants to (but that is not a requirement). Since the address can be a 64‐bit address, two sequential BARs must be used together. 

As before, the BARs are shown at three points in the configuration process: 

1. In (1) of Figure 4‐5, we see the uninitialized state of the BAR pair. The device designer has hard‐coded the lower bits of the lower BAR (BAR1 in our example) to indicate the request type and size, while the bits of the upper BAR (BAR2) are all read‐write. System software’s first step was to write all 1s to every BAR. In (2) of Figure 4‐5, we see the BARs after having all 1s written to them. 

2. As described in the previous example, system software already evaluated BAR0. So software’s next step is to read the next BAR (BAR1) and evaluate it to see if the device is requesting additional address space. Once BAR1 is read, software realizes that more address space is being requested and this request is for prefetchable memory address space that can be allocated any‐ where in the 64‐bit address range. Since it supports a 64‐bit address, the next sequential BAR (BAR2 in this case) is treated as the upper 32 bits of BAR1. So software now also reads in the contents of BAR2. However, soft‐ ware does not evaluate the lower bits of BAR2 in the same way it did for BAR1, because it knows BAR2 is simply the upper 32 bits of the 64‐bit address request started in BAR1. Table 4‐2 on page 132 summarizes the results of these configuration reads. 

3. The final step in this process is for system software to allocate an address range to the BARs now that software knows the size and type of the address space being requested. The third view of the BARs in (3) of Figure 4‐5 shows the result after software has used two configuration writes to pro‐ gram the 64‐bit start address for the allocated range. In this example, bit 1 of the Upper BAR (address bit 33 in the BAR pair) is set and bit 30 of the Lower BAR (address bit 30 in the BAR pair) is set to indicate a start address of 2_4000_0000h. All other writable bits in both BARs are cleared. 

At this point, the configuration of the BAR pair (BAR1 & BAR2) is complete. Once software enables memory address decoding in the Command register (offset 04h), this device will accept any memory requests it receives that fall within the range from 2_4000_0000h ‐ 2_43FF_FFFFh (64MB in size). 

**131** 

**PCI Express Technology** 

_Figure 4‐5: 64‐Bit Prefetchable Memory BAR Set Up_ 

## **Type 0 Header** 

**==> picture [375 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 23 15 7 0 Uninitialized BAR Pair<br>Device ID Vendor ID 00h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>Status Command 04h XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XX 00 0000 0000 0000 0000 0000 1 1 0 0 (1)<br>BAR n+1 BAR n<br>Class Code   Rev 08h<br>      ID<br>BIST Header Latency Cache 0Ch<br>Type Timer Line Size BAR Pair Written with all 1s<br>Base Address 0 (BAR0) 10h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>Base Address 1 (BAR1) 14h 1111 1111 1111 1111 1111 1111 1111 1111 1111 11 00 0000 0000 0000 0000 0000 1 1 0 0 (2)<br>Base Address 2 (BAR2) 18h<br>Base Address 3 (BAR3) 1Ch<br>BAR Pair Written With Base Address<br>Base Address 4 (BAR4) 20h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>Base Address 5 (BAR5) 24h 0000 0000 0000 0000 0000 0000 0000 0010 0100 00 00 0000 0000 0000 0000 0000 1 1 0 0 (3)<br>CardBus CIS Pointer 28h (0) (0) (0) (0) (0) (0) (0) (2) (4) (0) 0 = non-prefetchable<br>SubsystemDevice ID SubsystemVendor ID 2Ch 1 = prefetchable00 = 32-bit decoding<br>10 = 64-bit decoding<br>Expansion ROM Base Address 30h<br>0 = Memory request<br>Reserved Capability 34h 1 = IO request<br>Pointer<br>Reserved 38h Upper 38 bits of 64MB alignedstart address (lower bits assumed to be = 0)<br>(0000 0002 4000 0000h)<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch<br>This Example:<br>-64MB of prefetchable memory<br>-Address range may be above 4GB boundary (64-bit decode)<br>**----- End of picture text -----**<br>


_Table 4‐2: Results Of Reading the BAR Pair after Writing All 1s To Both_ 

|**BAR**|**BAR**<br>**Bits**|**Meaning**|
|---|---|---|
|Lower|0|Read as 0b, indicating a memory request. Since this is a mem‐<br>ory request, bits 3:1 also have an encoded meaning.|
|Lower|2:1|Read as 10b indicating the target supports a 64‐bit address<br>decoder, and that the next sequential BAR contains the upper<br>32 bits of the address information.|



**132** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐2: Results Of Reading the BAR Pair after Writing All 1s To Both (Continued)_ 

|**BAR**|**BAR**<br>**Bits**|**Meaning**|
|---|---|---|
|Lower|3|Read as 1b, indicating request is for prefetchable memory<br>(meaning reads do not have side‐effects); P‐MMIO|
|Lower|25:4|Read as all 0s, indicating the size of the request (these bits are<br>hard‐coded to 0)|
|Lower|31:26|Read as all 1s because software has not yet programmed the<br>upper bits with a start address for the block. Note that because<br>bit 26 was the least significant writable bit, the memory address<br>space request size is 226, or 64MB.|
|Upper|31:0|Read as all 1s. These bits will be used as the upper 32 bits of the<br>64‐bit start address programmed by system software.|



## **BAR Example 3: IO Address Space Request** 

Continuing from the previous two examples, this same function is also request‐ ing IO space, as shown in Figure 4‐6 on page 134. In the diagram, the requesting BAR (BAR3 in the example) is shown at three points in the configuration pro‐ cess: 

1. In (1) of Figure 4‐6, we see the uninitialized state of the BAR. System soft‐ ware has previously written all 1s to every BAR and has evaluated BAR0, then BAR1 and BAR2. Now software is going to see if this device is request‐ ing additional address space with BAR3. State (2) of Figure 4‐6 shows the state of the BAR3 after the write of all 1s. 

2. Software now reads in BAR3 to evaluate the size and type of the request. Table 4‐3 on page 134 summarizes the results of this configuration read. 

3. Now that software knows this is a request for 256 bytes of IO address space, the final step is to program the BAR with the base address of the IO address range being allocated to this device, specifically this BAR. State (3) of Figure 4‐6 shows the state of the BAR after this step. In our example, the device start address is 16KB, so bit 14 is written resulting in a base address of 4000h; all other upper bits are cleared.

</td>
<td style="background-color:#e8e8e8">

如第 146 页图 4-12 所示，PCI Express 拓扑由独立的、点对点的链路组成，这些链路将每个设备与一个或多个邻居连接起来。当流量到达链路接口的入站侧（称为_入口端口_）时，该端口会检查错误，然后做出三个决定之一：

1. 接受流量并在内部使用

2. 将流量转发到适当的出站（_出口_）端口

3. 拒绝流量，因为它既不是预期目标，也不是到其的接口（请注意，还有其他原因可能拒绝流量）

**146**

**第 4 章：地址空间与事务路由**

## **接收器检查三种类型的流量**

假设链路完全运行，设备的接收器接口（入口端口）必须检测和评估三种类型链路流量的到达：有序集 (Ordered Sets)、数据链路层包 (DLLP) 和事务层包 (TLP)。有序集和 DLLP 是链路本地的，因此永远不会被路由到另一条链路。TLP 可以并且确实会根据包头中包含的路由信息从一条链路移动到另一条链路。

## **路由元素**

具有多个端口的设备（如根复合体和交换机）可以在端口之间转发 TLP，有时称为路由代理 (Routing Agents) 或路由元素 (Routing Elements)。它们接受针对内部资源的 TLP 并在入口和出口端口之间转发 TLP。

有趣的是，交换机中需要点对点路由支持，但对于根复合体来说它是可选的。点对点流量通常是一个端点发送针对另一个端点的包。

端点只有一个链路，从不期望看到除针对它们的入口流量之外的任何流量。它们只是接受或拒绝传入的 TLP。

## **TLP 路由的三种方法**

## **概述**

TLP 可以基于地址（内存或 IO）、基于 ID（即总线、设备、功能号）进行路由，或隐式路由。使用的路由方法基于 TLP 类型。第 147 页表 4-7 总结了 TLP 类型和每种类型使用的路由方法。

_表 4-7：PCI Express TLP 类型和路由方法_

|**TLP 类型**|**使用的路由方法**|
|---|---|
|内存读 [锁]、内存写、原子操作 (AtomicOp)|地址路由|
|IO 读和写|地址路由|



**147**

**PCI Express Technology**

_表 4-7：PCI Express TLP 类型和路由方法（续）_

|**TLP 类型**|**使用的路由方法**|
|---|---|
|配置读和写|ID 路由|
|消息、带数据消息|地址路由、ID 路由或隐式路由|
|完成、带数据完成|ID 路由|



消息是支持不止一种路由方法的唯一 TLP 类型。PCI Express 规范中定义的大多数消息 TLP 都使用隐式路由，但是，如果需要，供应商定义的消息可以使用地址路由或 ID 路由。

## **隐式路由和消息的目的**

在隐式路由中，既不应用地址也不应用 ID 路由信息；相反，路由是基于包头中的代码进行的，该代码指示拓扑中具有已知位置的目标，例如根复合体。这在适用隐式路由的情况下简化了消息的路由。

**为什么使用消息？** 消息事务在 PCI 或 PCI-X 中没有定义，但随 PCIe 一起引入。添加消息作为包类型的主要原因是追求 PCIe 的设计目标，即大幅减少 PCI 中实现的外侧带信号的数量（例如中断引脚、错误引脚、电源管理信号等）。因此，大多数外侧带信号被替换为消息 TLP 形式的带内包。

**隐式路由如何提供帮助** 使用带内消息代替外侧带信号需要一种在由众多点对点链路组成的拓扑中将它们路由到适当接收方的方法。隐式路由利用了交换机和其他路由元素理解上游和下游概念以及根复合体位于拓扑顶部而端点位于底部的事实。因此，消息可以使用简单的代码来表明它应该去往根复合体，例如，或者被发送到下游的所有设备。此功能消除了专门用作不同消息事务目标的地址范围或 ID 列表的定义需求。

不同类型的隐式路由可以在第 163 页的"隐式路由"中找到。

**148**

**第 4 章：地址空间与事务路由**

## **分离事务协议**

像大多数其他串行技术一样，PCI Express 使用分离事务协议 (Split Transaction Protocol)，该协议允许目标设备接收一个或多个请求，然后用单独的完成响应每个请求。这是对 PCI 总线协议的显著改进，后者使用等待状态或延迟事务（重试）来处理访问目标中的延迟。目标不是测试何时准备好执行长延迟传输，而是在它准备好时启动响应。这导致每个事务至少有两个单独的 TLP - 请求和完成（稍后将讨论，单个读请求可能导致多个完成 TLP 被发送回）。第 149 页图 4-13 说明了分离事务的请求-完成组件。本示例显示软件从端点读取数据。

_图 4-13：PCI Express 事务请求和完成 TLP_

**==> picture [304 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体 系统<br>
IN OUT 内存<br>
1) 请求 TLP（内存读）<br>
K27.7 K29.7<br>
OUT IN STP SEQ HDR LCRC END<br>
END 字节<br>
链路 CRC（4 字节）<br>
TLP 头（3DW 或 4DW）<br>
交换机<br>
TLP 序列号（2 字节）<br>
STP 符号的接收器解码指示<br>
TLP 的开始<br>
2) 带数据的完成 TLP<br>
K27.7 K29.7<br>
OUT IN STP SEQ HDR Data LCRC END<br>
PCIe<br>
端点<br>
IN OUT<br>
OUT IN<br>**----- End of picture text -----**<br>


**149**

**PCI Express Technology**

## **Posted 与 Non-Posted**

为了减轻请求-完成延迟的损失，内存写事务是 Posted 的，这意味着从请求者的角度来看，事务在请求离开请求者时即被视为已完成。如果有帮助，您可以将"发布"一词与邮政系统相关联，其中发布内存写类似于在邮件中发布一封信。一旦您将信件放入邮箱，您就将信心寄托在系统上以递送它，并且不会等待递送确认。这种方法可能比等待整个请求-完成传输要快得多，但是 - 与所有发布方案一样 - 关于事务何时（以及是否）在最终接收方成功完成存在不确定性。

在 PCIe 中，通过将所有内存写设为 Posted 所涉及的少量不确定性被认为是可接受的，以换取获得的性能。相比之下，对 IO 和配置空间的写几乎总是会影响设备行为并具有与之关联的及时性。因此，重要的是要知道那些写请求何时（以及是否）完成。由于这个原因，IO 写和配置写始终是 Non-Posted 的，并且将始终返回完成以报告操作的状态。

总之，Non-Posted 事务需要完成。Posted 事务不需要，也不应该接收完成。第 150 页表 4-8 列出了哪些 PCIe 事务是 Posted 和 Non-Posted 的。

_表 4-8：Posted 和 Non-Posted 事务_

|**请求**|**请求的处理方式**|
|---|---|
|内存写|所有**内存写请求都是 Posted 的**。不期望也不发送完成。|
|内存读<br>内存读锁定|所有**内存读请求都是 Non-Posted 的**。将由完成者返回带数据的完成（由一个或多个 TLP 组成），以提供所请求的数据和内存读的状态。在错误的情况下，将返回不带数据的完成以报告状态。|
|原子操作 (AtomicOp)|所有**原子操作请求都是 Non-Posted 的**。将由完成者返回带数据的完成，其中包含目标位置的原始值。|



**150**

**第 4 章：地址空间与事务路由**

_表 4-8：Posted 和 Non-Posted 事务（续）_

|**请求**|**请求的处理方式**|
|---|---|
|IO 读<br>IO 写|所有**IO 请求都是 Non-Posted 的**。对于写或失败的读，将返回不带数据的完成，对于成功的读，将返回带数据的完成。|
|配置读<br>配置写|所有**配置请求都是 Non-Posted 的**。对于写和失败的读，将返回不带数据的完成，对于成功的读，将返回带数据的完成。|
|消息|所有**消息都是 Posted 的**。路由方法取决于消息类型，但它们都被视为 Posted 请求。|



## **头字段定义包格式和类型**

## **概述**

如第 152 页图 4-14 所示，每个 TLP 包含一个三或四个双字（12 或 16 字节）的头。这包括_格式_和_类型_字段，它们定义头的其余部分的内容并指示 TLP 在遍历拓扑时要使用的路由方法。

**151**

**PCI Express Technology**

_图 4-14：事务层包通用 3DW 和 4DW 头_

**==> picture [256 x 344] intentionally omitted <==**

**----- Start of picture text -----**<br>
事务层包 (TLP)<br>
成帧序列头 数据摘要 LCRC 成帧<br>
(STP) 编号 (END)<br>
通用 3DW（12 字节）头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 字节 4-7 随类型字段而变化<br>
字节 8 字节 8-11 随类型字段而变化<br>
通用 4DW（16 字节）头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 字节 4-7 随类型字段而变化<br>
字节 8 字节 8-11 随类型字段而变化<br>
字节 12 字节 12-15 随类型字段而变化<br>**----- End of picture text -----**<br>


**152**

**第 4 章：地址空间与事务路由**

## **头格式/类型字段编码**

下面的第 153 页表 4-9 总结了 TLP 头格式和类型字段中使用的编码。

_表 4-9：TLP 头格式和类型字段编码_

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|内存读请求 (MRd)|000 = 3DW，无数据<br>001 = 4DW，无数据|0 0000|
|内存读锁定请求 (MRdLk)|000 = 3DW，无数据<br>001 = 4DW，无数据|0 0001|
|内存写请求 (MWr)|010 = 3DW，带数据<br>011 = 4DW，带数据|0 0000|
|IO 读请求 (IORd)|000 = 3DW，无数据|00010|
|IO 写请求 (IOWr)|010 = 3DW，带数据|0 0010|
|配置类型 0 读请求 (CfgRd0)|000 = 3DW，无数据|0 0100|
|配置类型 0 写请求<br>(CfgWr0)|010 = 3DW，带数据|0 0100|
|配置类型 1 读请求 (CfgRd1)|000 = 3DW，无数据|0 0101|
|配置类型 1 写请求<br>(CfgWr1)|010 = 3DW，带数据|0 0101|
|消息请求 (Msg)|001 = 4DW，无数据|1 0RRR*（有关 RRR，<br>请参见第 164 页的<br>"消息类型字段汇总"<br>中的路由子字段）|
|带数据消息请求 (MsgD)|011 = 4DW，带数据|1 0RRR*（有关 RRR，<br>请参见第 164 页的<br>"消息类型字段汇总"<br>中的路由子字段）|



**153**

**PCI Express Technology**

_表 4-9：TLP 头格式和类型字段编码（续）_

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|完成 (Cpl)|000 = 3DW，无数据|0 1010|
|带数据完成 (CplD)|010 = 3DW，带数据|0 1010|
|完成锁定 (CplLk)|000 = 3DW，无数据|0 1011|
|带数据完成 (CplDLk)|010 = 3DW，带数据|0 1011|
|取并加原子操作请求<br>(FetchAdd)|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1100|
|无条件交换原子操作<br>请求 (Swap)|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1101|
|比较并交换原子操作<br>请求 (CAS)|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1110|
|本地 TLP 前缀 (LPrfx)|100 = 1DW|0 LLLL|
|端到端 TLP 前缀 (EPrfx)|100 = 1DW|1 EEEE|



## **TLP 头概述**

当 TLP 在入口端口被接收时，它们首先在物理层和数据链路层检查错误。如果没有错误，则在事务层检查 TLP 以了解要使用哪种路由方法。基本步骤是：

1. _格式_和_类型_字段确定头的大小、格式和包的类型。

2. 根据与包类型关联的路由方法，设备确定它是否是预期接收方。如果是，它将接受（消费）TLP，如果不是，它将把 TLP 转发到适当的出口端口 - 受该出口端口的排序和流控规则的约束。

3. 如果此设备既不是预期接收方，也不在到预期接收方的路径上，它通常会将包作为不支持的请求 (Unsupported Request, UR) 拒绝。

**154**

**第 4 章：地址空间与事务路由**

## **应用路由机制**

一旦系统地址已配置且事务已启用，设备就会检查传入的 TLP 并使用相应的配置字段来路由包。以下各节描述了用于通过 PCI Express 互连结构路由 TLP 的每种路由机制的基本特征/功能。

## **ID 路由**

ID 路由用于定位功能在拓扑中的逻辑位置 - 总线号、设备号、功能号（通常称为 **BDF**）。它与 PCI 和 PCI-X 协议中用于配置事务的路由方法兼容。在 PCIe 中，它仍用于路由配置包，也用于路由完成和某些消息。

## **总线号、设备号、功能号限制**

PCI Express 支持与 PCI 和 PCI-X 相同的拓扑限制：

1. 使用 8 位表示总线号，因此系统中**最多可有 256 条总线**。这包括由交换机创建的内部总线。

2. 使用 5 位表示设备号，因此**每条总线最多可有 32 个设备**。较旧的 PCI 总线或交换机或根复合体中的内部总线可能承载多个下游设备。但是，外部 PCIe 链路始终是点对点的，并且链路上只有一个下游设备。外部链路的设备号被下游端口强制始终为设备 0，因此每个外部端点将始终是设备 0（除非使用替代路由 ID 解释 (ARI)，在这种情况下，没有设备号；有关 ARI 的更多信息，请参见第 909 页关于"IDO（基于 ID 的排序）"的部分。

3. 使用 3 位表示功能号，因此**每个设备最多可有 8 个内部功能**。

## **ID 路由中的关键 TLP 头字段**

如果接收的 TLP 中的 Type 字段指示要使用 ID 路由，则头中的 ID 字段（总线、设备、功能）用于执行路由检查。有两种情况：使用 3DW 头的 ID 路由和使用 4DW 头的 ID 路由（仅在消息中可能）。第 156 页图 4-15 说明了使用 ID 路由和 3DW 头的 TLP，而第 156 页图 4-16 显示了 ID 路由的 4DW 头。

**155**

**PCI Express Technology**

_图 4-15：3DW TLP 头 - ID 路由字段_

**==> picture [354 x 357] intentionally omitted <==**

**----- Start of picture text -----**<br>
使用 ID 路由的 3DW 头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
字节 0 Fmt At T T E<br>
0 x 0 Type R TC R tr R H D P Attr AT Length<br>
字节 4 字节 4-7 随类型字段而变化<br>
设备 功能<br>
字节 8 总线号 字节 10-11 随类型字段而变化<br>
使用 ARI 的功能号<br>
图 4-16：4DW TLP 头 - ID 路由字段<br>
使用 ID 路由的 4DW 头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
字节 0 Fmt At T T E<br>
0 x 1 Type R TC R tr R H D P Attr AT Length<br>
字节 4 字节 4-7 随类型字段而变化<br>
设备 功能<br>
字节 8 总线号 字节 10-11 随类型字段而变化<br>
使用 ARI 的功能号<br>
字节 12 字节 12-15 随类型字段而变化<br>**----- End of picture text -----**<br>


## **端点：单次检查**

对于 ID 路由，端点只需将包头中的 ID 字段与其自己的 BDF 进行比较即可。每个功能在其链路上每次看到类型 0 配置写时都从 TLP 头的字节 8-9 中"捕获"自己的总线和设备号。未指定应将捕获的总线和设备号信息存储在哪里，仅规定了功能必须保存它。已保存的总线

**156**

**第 4 章：地址空间与事务路由**

设备号用作该端点发起的 TLP 请求中的 Requester ID，以便该请求的完成者可以在完成包中包含 Requester ID 值。完成包中的 Requester ID 用于路由完成。

## **交换机（桥）：每个端口两次检查**

对于 ID 路由的 TLP，交换机端口首先通过将 TLP 头中的目标 ID 与其自己的 BDF 进行比较来检查它是否是预期目标，如第 158 页图 4-17 中的 (1) 所示。与端点一样，每个交换机端口在每次检测到其上游端口上的配置写（Type 0）时都会捕获自己的总线和设备号。如果 TLP 中的目标 ID 字段与交换机端口的 ID 一致，则它消费该包。如果 ID 字段不匹配，则它接下来检查 TLP 是否针对此交换机端口下方的设备。它通过检查 Secondary 和 Subordinate Bus Number 寄存器来查看 TLP 中的目标总线号是否在此范围内（含）来实现。如果是这样，则 TLP 应被向下游转发。此检查由第 158 页图 4-17 中的 (2) 表示。如果包正在向下游移动（在 Upstream Port 上收到）且与 Upstream Port 的 BDF 不匹配或不在 Secondary-Subordinate 总线范围内，则它将在 Upstream Port 上作为不支持的请求处理。

如果 Upstream Port 确定它收到的 TLP 是针对其下方某个设备的（因为目标总线号在其 Secondary-Subordinate 总线号范围内），则它将其向下游转发，并且交换机的所有下游端口都执行相同的检查。每个下游端口检查 TLP 是否针对它们。如果是，则目标端口将消费 TLP，而其他端口将忽略它。如果不是，则所有下游端口都检查 TLP 是否针对其端口下方的设备。在该检查中返回 true 的那个端口将 TLP 转发到其二级总线，而其他下游端口将忽略 TLP。

在本节中，重要的是要记住交换机上的每个端口都是一个桥，因此具有自己的 Type 1 头的配置空间。即使第 158 页图 4-17 仅显示单个 Type 1 头，实际上，每个端口（每个 P2P 桥）都有自己的 Type 1 头，并在该端口看到 TLP 时执行相同的两次检查。

**157**

**PCI Express Technology**

_图 4-17：交换机使用 ID 路由检查入站 TLP 的路由_

**==> picture [338 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 头<br>
CPU 31 23 15 7 0<br>
设备 ID 厂商 ID 00h<br>
__ es<br>
状态 命令 04h<br>
根复合体 系统内存 类代码 行大小 缓存 08h<br>
— P2P - (DRAM) ee [TT] TSS BIST 头类型 延迟定时器 ee 行大小 缓存 0Ch<br>
基址 0 (BAR0) 10h<br>
TLP ID 字段<br>
1. 包是给我的吗？<br>
(BDF) ; ee 基址 1 (BAR1) 14h<br>
二级 下属 二级 主 18h<br>
P2P 延迟定时器 总线号 总线号 总线号<br>
交换机 + 2. 包是给下方的 SS 二级状态 上限 IO 基址 1Ch<br>
某个设备的吗？ (非可预取)内存上限 (非可预取)内存基址 20h<br>
NIK —}--—— 内存上限 可预取内存基址 可预取 24h<br>
可预取内存基址 28h<br>
高 32 位<br>
可预取内存上限高 32 位 2Ch<br>
PCIe ma PCIe Cc — OO IO 上限 IO 基址<br>
oe 高 16 位 高 16 位 30h<br>
端点 端点 保留 能力 34h<br>
a 指针<br>
扩展 ROM 基址 38h<br>
—<br>
或 桥控制 中断引脚 中断线 3Ch<br>
P2P P2P<br>**----- End of picture text -----**<br>


## **地址路由**

使用地址路由的 TLP 引用与 PCI 和 PCI-X 事务相同的内存（系统内存和内存映射 IO）和 IO 地址映射。针对 4GB 以下地址（即 32 位地址）的内存请求必须使用 3DW 头，而针对 4GB 以上地址（即 64 位地址）的请求必须使用 4DW 头。IO 请求限制为 32 位地址，并且仅实现以支持传统功能。

**158**

**第 4 章：地址空间与事务路由**

## **地址路由中的关键 TLP 头字段**

当 Type 字段指示 TLP 要使用地址路由时，则头中的地址字段用于执行路由检查。这些可以是 32 位地址或 64 位地址。

**具有 32 位地址的 TLP** 对于 IO 或 32 位内存请求，使用 3DW 头，如图 4-18 所示。使用这些 TLP 寻址的内存映射寄存器因此将驻留在 4GB 内存或 IO 地址边界之下。

**具有 64 位地址的 TLP** 对于 64 位内存请求，使用 4DW 头，如图 4-19（第 160 页）所示。使用这些 TLP 寻址的内存映射寄存器能够驻留在 4GB 内存边界之上。

_图 4-18：3DW TLP 头 - 地址路由字段_

**==> picture [370 x 148] intentionally omitted <==**

**----- Start of picture text -----**<br>
使用地址路由的 3DW 头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
字节 0 Fmt At T T E<br>
Type R TC R R Attr AT Length<br>
0 x 0 tr H D P<br>
字节 4 字节 4-7 随类型字段而变化<br>
字节 8 地址 [31:2] R<br>**----- End of picture text -----**<br>


**159**

**PCI Express Technology**

_图 4-19：4DW TLP 头 - 地址路由字段_

**==> picture [372 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
使用地址路由的 4DW 头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
字节 0 Fmt At T T E<br>
Type R TC R R Attr AT Length<br>
0 x 1 tr H D P<br>
字节 4 字节 4-7 随类型字段而变化<br>
字节 8 地址 [63:32]<br>
字节 12 地址 [31:2] R<br>**----- End of picture text -----**<br>


## **端点地址检查**

如果端点接收到使用地址路由的 TLP，则它将头中的地址与其配置头中实现的每个基地址寄存器 (BAR) 进行比较，如图 4-20 所示。由于端点只有一个链路接口，它将接受或拒绝该包。如果 TLP 中的目标地址与编程到其 BAR 中的某个范围匹配，则端点将接受该包。有关如何使用 BAR 的更多信息，请参见第 126 节的"基地址寄存器 (BAR)"。

**160**

**第 4 章：地址空间与事务路由**

_图 4-20：端点检查传入 TLP 地址_

**==> picture [335 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU Type 0 头<br>
31 23 15 7 0<br>
设备 ID 厂商 ID 00h<br>
根复合体 系统 状态 命令 04h<br>
内存<br>
P2P (DRAM) 类代码 行大小 缓存 08h<br>
BIST 头 延迟 缓存 0Ch<br>
TLP 类型 定时器 行大小<br>
(地址) 基址 0 (BAR0) 10h<br>
基址 1 (BAR1) 14h<br>
P2P<br>
基址 2 (BAR2) 18h<br>
交换机 包是给我的吗？ 基址 3 (BAR3) 1Ch<br>
基址 4 (BAR4) 20h<br>
TLP { 基址 5 (BAR5) 24h<br>
(地址) CardBus CIS 指针 28h<br>
PCIe PCIe 子系统设备 ID 子系统厂商 ID 2Ch<br>
端点 端点 扩展 ROM 基址 30h<br>
保留 能力 34h<br>
TLP 地址字段 指针<br>
应与某个 BAR 匹配 保留 38h<br>
在 PCIe 功能内 最大延迟 最小授权 中断引脚 中断线 3Ch<br>
P2P P2P<br>**----- End of picture text -----**<br>


## **交换机路由**

如果传入的 TLP 使用地址路由，则交换机端口首先通过将包头中的地址与其 Type 1 配置头中的两个 BAR 进行比较来检查地址是否在本端口内是本地的，如图 4-21（第 162 页）的步骤 1 所示。如果与这些 BAR 中的一个匹配，则交换机端口是 TLP 的目标并消费该包。如果不是，则端口接下来检查其 Base/Limit 寄存器对以查看 TLP 是否针对此桥下方（下游）的功能。如果请求针对 IO 空间，它将检查 IO Base 和 Limit 寄存器，如步骤 2a 所示。但是，如果请求针对内存空间，它将检查非可预取内存基址/上限寄存器和可预取内存基址/上限寄存器，如图 4-21（第 162 页）中的步骤 2b 所示。有关如何评估 Base/Limit 寄存器对的更多信息，请参见第 136 节的"基址和上限寄存器"。

**161**

**PCI Express Technology**

_图 4-21：交换机使用地址检查入站 TLP 的路由_

**==> picture [349 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 头<br>
CPU 31 23 15 7 0<br>
设备 ID 厂商 ID 00h<br>
__ es<br>
状态 命令 04h<br>
根复合体 系统内存 类代码 行大小 缓存 08h<br>
P2P - (DRAM) [—_] e BIST 头类型 s e 延迟定时器 行大小 ee 缓存 0Ch<br>
基址 0 (BAR0) 10h<br>
TLP<br>
1. 包是给我的吗？<br>
(地址) 基址 1 (BAR1) 14h<br>
二级 下属 二级 主 18h<br>
P2P 延迟定时器 总线号 总线号 总线号<br>
2a. IO 包是给下方的 二级状态 上限 IO 基址 1Ch<br>
交换机       某个设备的吗？ | (非可预取)内存上限 (非可预取)内存基址 20h<br>
— —— 2b. 内存包是给下方的 _— 可预取 可预取 24h<br>
内存上限 内存基址<br>
      某个设备的吗？ 可预取内存基址 28h<br>
高 32 位<br>
可预取内存上限高 32 位 2Ch<br>
PCIe PCIe IO 上限 IO 基址<br>
高 16 位 高 16 位 30h<br>
7 7 ee<br>
端点 端点 保留 能力 34h<br>
es 指针<br>
扩展 ROM 基址 38h<br>
— ae<br>
ee 桥控制 中断 ee 线 3Ch<br>
P2P P2P<br>**----- End of picture text -----**<br>


要了解交换机中基于地址的 TLP 的路由，最好记住每个交换机端口都是其自己的桥。以下是桥（交换机端口）在接收到基于地址的 TLP 时采取的步骤：

## **向下游传输的 TLP（在主接口上接收）**

1. 如果 TLP 中的目标地址与某个 BAR 匹配，则此桥（交换机端口）消费 TLP，因为它是 TLP 的目标。

2. 如果 TLP 中的目标地址落在其某个 Base/Limit 寄存器集的范围内，则该包将转发到二级接口（下游）。

3. 否则 TLP 将在主接口上作为不支持的请求处理。（如果主接口上的其他桥也未声明 TLP，则也是如此。）

**162**

**第 4 章：地址空间与事务路由**

## **向上游传输的 TLP（在二级接口上接收）**

1. 如果 TLP 中的目标地址与某个 BAR 匹配，则此桥（交换机端口）消费 TLP，因为它是 TLP 的目标。

2. 如果 TLP 中的目标地址落在其某个 Base/Limit 寄存器集的范围内，则 TLP 将在二级接口上作为不支持的请求处理。（除非此端口是交换机的上游端口，否则也是如此。在这些情况下，该包可能是一个点对点事务，并将在不同于接收它的下游端口的下游端口上转发。）

3. 否则 TLP 将转发到主接口（上游），前提是 TLP 地址不是针对此桥，也不是针对此桥下方的任何功能。

## **多播能力**

PCI Express 规范的 2.1 版本增加了对指定提供多播功能的地址范围的支持。收到的落在指定为多播范围的地址范围内的任何包都根据多播规则进行路由/接受。此地址范围可能未在功能的 BAR 中保留，也可能在桥的 Base/Limit 寄存器对中，但仍需要适当地接受/转发。有关多播功能的更多信息，请参见第 889 页的"多播能力寄存器"部分。

## **隐式路由**

在某些消息包中使用的隐式路由基于路由元素对拓扑具有上游和下游方向以及顶部存在单个根复合体的认识。这允许使用一些简单的路由方法而无需分配目标地址或 ID。由于根复合体通常集成了电源管理、中断和错误处理逻辑，因此它是大多个 PCI Express 消息的源或接收方。

## **仅用于消息**

某些消息使用地址或 ID 路由而不是隐式路由，对于它们，路由机制的适用方式与那些部分中描述的相同。但是，大多数消息使用隐式路由。隐式路由的目的是模拟外侧带信号行为，因为 PCIe 的一个设计目标是尽可能消除 PCI 中的外侧带信号。这些

**163**

**PCI Express Technology**

PCI 中的外侧带信号通常要么是主机通知所有设备事件，要么是设备通知主机事件。在 PCIe 中，我们有消息 TLP 来传达这些事件。PCIe 已定义消息的事件类型包括：

- 电源管理

- INTx 传统中断信令

- 错误信令

- 锁定事务支持

- 热插拔信令

- 供应商特定信令

- 插槽功率限制设置

## **隐式路由中的关键 TLP 头字段**

对于隐式路由，头中的路由子字段用于确定消息目标。第 164 页图 4-22 说明了使用隐式路由的消息 TLP。

_图 4-22：4DW 消息 TLP 头 - 隐式路由字段_

**==> picture [355 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
消息的 4DW 头<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
字节 0 Fmt Type R TC R At R TH T E Attr AT Length<br>
0 x 1 1  0  r  r  r tr 0 D P 0 0 0 0<br>
消息<br>
字节 4 Requester ID Tag<br>
代码<br>
字节 8 字节 8-11 随消息代码字段而变化<br>
字节 12 字节 12-15 随消息代码字段而变化<br>**----- End of picture text -----**<br>


## **消息类型字段汇总**

第 165 页表 4-10 显示了如何解释消息的 TLP 头 Type 字段。如图所示，高两位指示包是消息，而低三位指定要应用的路由方法。请注意，消息 TLP 始终使用 4DW 头，无论选择哪种路由选项。

**164**

**第 4 章：地址空间与事务路由**

对于地址路由，字节 8-15 包含最多 64 位的地址，对于 ID 路由，字节 8 和 9 包含目标 BDF。

_表 4-10：消息请求头类型字段用法_

|**类型字段位**|**描述**|
|---|---|
|位 4:3|定义事务类型：<br>10b = 消息 TLP|
|位 2:0|消息路由子字段 R[2:0]<br>• 000b = 隐式 - 路由到根复合体<br>• 001b = 按地址路由（头的字节 8-15 包含地址）<br>• 010b = 按 ID 路由（头的字节 8-9 包含 ID）<br>• 011b = 隐式 - 向下游广播<br>• 100b = 隐式 - 本地：在接收方终止<br>• 101b = 隐式 - 收集并路由到根复合体<br>• 110b - 111b = 保留：在接收方终止|



## **端点处理**

对于隐式路由，端点只需检查路由子字段是否适合它。例如，端点将接受广播消息或在接收方终止的消息；但不接受隐式针对根复合体的消息。

## **交换机处理**

交换机等路由元素会考虑 TLP 到达的端口以及路由子字段代码是否适合它。例如：

1. 交换机上游端口可以合法地接收广播消息。它将复制该消息并将其转发到其所有下游端口。在交换机的下游端口上接收到的隐式路由的广播消息（意味着消息正在向上游传输）将是一个错误，将作为畸形 TLP 处理。

2. 交换机可以在下游端口上接收针对根复合体的隐式路由消息，并将其转发到其上游端口，因为根复合体的位置被认为是上游的。它不会接受在其上游端口上接收到的隐式路由到根复合体的消息（意味着消息正在向下游传输）。

**165**

## **PCI Express Technology**

3. 如果隐式路由的消息指示它应在接收方终止，则接收交换机端口将消费该消息而不是转发它。

4. 对于使用地址或 ID 路由的消息，交换机将简单地执行正常的地址或 ID 检查以决定是否接受或转发它。

## **DLLP 和有序集不路由**

DLLP 和有序集流量不会从交换机或根复合体的入口端口路由到出口端口。这些包从端口到端口通过链路从物理层传输到物理层。

DLLP 源自 PCI Express 端口的数据链路层，通过物理层传递，退出端口，穿越链路并到达相邻端口。在该端口，包通过物理层传递并最终到达数据链路层，在那里它被处理和消费。DLLP 不会进一步上移端口到事务层，因此不会被路由。

类似地，有序集包源自物理层，退出端口，穿越链路并到达相邻端口。在该端口，包到达物理层，在那里它被处理和消费。有序集不会进一步上移端口到数据链路层和事务层，因此不会被路由。

正如本章所讨论的，只有 TLP 通过交换机和根复合体进行路由。它们源自源端口的事务层并最终到达目标端口的事务层。

**166**

## 第二部分：

# 事务层

## _**5**_

## _**TLP 元素**_

## **上一章**

上一章描述了功能通过基地址寄存器 (BAR) 请求地址空间（内存地址空间或 IO 地址空间）的目的和方法，以及软件必须如何在所有桥中设置 Base/Limit 寄存器以将 TLP 从源端口路由到正确的目标端口。还讨论了 PCIe 中 TLP 路由的一般概念，包括基于地址的路由、基于 ID 的路由和隐式路由。

## **本章**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-3"></a>
## 5.3 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

At this point, the configuration of BAR3 is complete. Once software enables IO address decoding in the Command register (offset 04h), the device will accept and respond to IO transactions within the range 4000h ‐ 40FFh (256 bytes in size). 

**133** 

## **PCI Express Technology** 

_Figure 4‐6: IO BAR Set Up_ 

**==> picture [389 x 485] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Header<br>31 23 15 7 0<br>Uninitialized IO BAR<br>Device ID Vendor ID 00h 31 8 2 1 0<br>Status Command 04h XXXX XXXX XXXX XXXX XXXX XXXX 0000 00 0 1 (1)<br>Class Code   Rev 08h<br>      ID<br>BIST Header Latency Cache 0Ch IO BAR Written with all 1s<br>Type Timer Line Size 31 8 2 1 0<br>Base Address 0 (BAR0) 10h 1111 1111 1111 1111 1111 1111 0000 00 0 1 (2)<br>Base Address 1 (BAR1) 14h<br>Base Address 2 (BAR2) 18h IO BAR Written With Base Address<br>31 8 2 1 0<br>Base Address 3 (BAR3) 1Ch<br>0000 0000 0000 0000 0100 0000 0000 00 0 1 (3)<br>Base Address 4 (BAR4) 20h (0) (0) (0) (0) (4) (0)<br>Base Address 5 (BAR5) 24h 0 = Memory request<br>1 = IO request<br>CardBus CIS Pointer 28h<br>Reserved (0)<br>SubsystemDevice ID SubsystemVendor ID 2Ch<br>Upper 24 bits of 256-byte aligned<br>Expansion ROM Base Address 30h start address (lower 7 bits assumed to be = 0)<br>(0000 4000h)<br>Reserved Capability 34h<br>Pointer<br>Reserved 38h This Example:<br>-256 bytes of IO address space<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch -Software assigns the start address at 16KB in IO address map.<br>Note: Only Legacy PCIe devices should make requests for IO<br>address space.<br>Table 4‐3: Results Of Reading the IO BAR after Writing All 1s To It<br>BAR Bits Meaning<br>0 Read as 1b, indicating an IO request. Since this is an IO request, bit 1 is<br>reserved.<br>1 Reserved. Hard‐coded to 0b.<br>7:2 Read as 0s Indicates size of the request (these bits are hard‐coded to 0)<br>31:8 Read as 1s because software has not yet programmed the upper bits<br>with a start address for the block. Note that because bit 8 was the least<br>significant writable bit, the IO request size is 2 [8] , or 256 bytes.<br>**----- End of picture text -----**<br>


**134** 

**Chapter 4: Address Space & Transaction Routing** 

## **All BARs Must Be Evaluated Sequentially** 

After going through the previous three examples, it becomes clear that software must evaluate BARs in a sequential fashion. 

Most of the time, functions do not need all six BARs. Even in the examples we went through, only four of the six available BARs were used. If the function in our example did not need to request any additional address space, the device designer would hard‐code all bits of BAR4 and BAR5 to 0s. So even though soft‐ ware writes those BARs with all 1s, the writes have no affect. After evaluating BAR3, software would move on to evaluating BAR4. Once it detected that none of the bits were set, software would know this BAR is not being used and move on to evaluating the next BAR. 

All BARs must be evaluated, even if software finds a BAR that is not being used. There are no rules in PCI or PCIe, that state that BAR0 must be the first BAR used for address space requests. If a device designer chooses to, they can use BAR4 for an address space request and hard‐code BAR0, BAR1, BAR2, BAR3 and BAR5 to all 0s. This means software must evaluate every BAR in the header. 

## **Resizable BARs** 

The 2.1 version of the PCI Express specification added support for changing the size of the requested address space in the BARs by defining a new capability structure in extended config space. The new structure allows the function to advertise what address space sizes it can operate with and then have software enable one of the sizes based on the available system resources. For example, if a function would ideally like to have 2GB of prefetchable memory address space, but it could still operate with only 1GB, 512MB or 256MB of P‐MMIO, system software may only enable the function to request 256MB of address space if software would not be able to accommodate a request of a larger size. 

**135** 

**PCI Express Technology** 

## **Base and Limit Registers** 

## **General** 

Once a function’s BARs are programmed, the function knows what address range(s) it owns, which means that function will claim any transactions it sees that is targeting an address range it owns, an address range programmed into one of its BARs. This is good, but it’s important to realize that the only way that function is going to “see” the transactions it should claim is if the bridge(s) upstream of it, forward those transactions downstream to the appropriate link that the target function is connected to. Therefore, each bridge (e.g. switch ports and root complex ports) needs to know what address ranges live beneath it so it can determine which requests should be forwarded from its primary interface (upstream side) to its secondary interface (downstream side). If the request is targeting an address that is owned by a BAR in a function beneath the bridge, the request should be forwarded to the bridge’s secondary interface. 

It is the Base and Limit registers in the Type 1 headers that are programmed with the range of addresses that live beneath this bridge. There are the three sets of Base and Limit registers found in each Type 1 header. Three sets of registers are needed because there can be three separate address ranges living below a bridge: 

- Prefetchable Memory space (P‐MMIO) 

- Non‐Prefetchable Memory space (NP‐MMIO) 

- IO space (IO) 

To explain how these Base and Limit registers work, let’s continue the example from the previous section and place that programmed function (an endpoint) beneath a switch as shown in Figure 4‐7 on page 137. The figure also lists the address ranges owned by the BARs of that function. 

The Base and Limit registers of every bridge upstream of the endpoint will need to be programmed, but to start out, we’re going to focus on the bridge that is connected to the endpoint (Port B). 

**136** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐7: Example Topology for Setting Up Base and Limit Values_ 

**==> picture [301 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex MemorySystem<br>P2P (DRAM)<br>Port<br>A<br>P2P<br>Switch<br>Port Port<br>B C<br>PCIe PCIe<br>Endpoint Endpoint<br>BAR0: NP-MMIO (4KB)<br>F900_0000h - F900_0FFFh<br>BAR1-2: P-MMIO (64MB)<br>2_4000_0000h - 243FF_FFFFh<br>BAR3: IO (256 bytes)<br>4000h - 40FFh<br>BAR4-5: Not Used (All 0s)<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Prefetchable Range (P-MMIO)** 

Type 1 headers have two pairs of prefetchable memory base/limit registers. The Prefetchable Memory Base/Limit registers store address info for the lower 32 bits of the prefetchable address range. If this bridge supports decoding 64‐bit addresses, then the Prefetchable Memory Base/Limit Upper 32 Bits registers are also used and hold the upper 32 bits (bits [63:32]) of the address range. Figure 4‐ 8 on page 138 shows the values software would program into these registers to indicate that the prefetchable address range of 2_4000_0000h ‐ 2_43FF_FFFFh lives beneath that bridge (Port B). The meaning of each field in those registers is summarized in Table 4‐4. 

**137** 

**PCI Express Technology** 

_Figure 4‐8: Example Prefetchable Memory Base/Limit Register Values_ 

**==> picture [368 x 305] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>31 23 15 7 0 Prefetchable Base Prefetchable<br>Device ID Vendor ID 00h Upper 32 Bits Memory Base<br>31 0 15 3 0<br>Status Command 04h 0000 0000 0000 0000 0000 0000 0000 0010 0100 0000 0000 0001<br>Class Code       ID  Rev 08h (0) (0) (0) (0) (0) (0) (0) (2) (4) (0) (0) (RO)<br>0h = 32-bit<br>BIST HeaderType LatencyTimer Line SizeCache 0Ch Prefetchable Base Address(RW) Bits 63:32 of Prefetchable Base Address(RW) Bits 31:20 of 1h = 64-bit<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h Prefetchable Range<br>Secondary Subordinate Secondary Primary 18h Base Address 0000 0002 4000 0000h<br>Lat Timer Bus # Bus # Bus # Bits 19:0 are<br>SecondaryStatus LimitIO BaseIO 1Ch always 0s for Base<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Memory LimitPrefetchable Memory BasePrefetchable 24h Prefetchable LimitUpper 32 Bits Memory LimitPrefetchable<br>Prefetchable Memory Base 28h 31 0 15 3 0<br>Upper 32 Bits 0000 0000 0000 0000 0000 0000 0000 0010 0100 0011 1111 0001<br>Prefetchable Memory LimitUpper 32 Bits 2Ch (0) (0) (0) (0) (0) (0) (0) (2) (4) (3) (F) (RO)<br>IO Limit IO Base 0h = 32-bit<br>Upper 16 Bits Upper 16 Bits 30h (RW) Bits 63:32 of (RW) Bits 31:20 of 1h = 64-bit<br>Prefetchable Base Address Prefetchable Base Address<br>Reserved Capability 34h<br>Pointer<br>Expansion ROM Base Address 38h<br>Prefetchable Range<br>ControlBridge InterruptPin InterruptLine 3Ch Limit Address 0000 0002 43FF FFFFh<br>Bits 19:0 are<br>always Fs for Limit<br>Prefetchable Memory Range: 2_4000_0000h - 2_43FF_FFFFh<br>**----- End of picture text -----**<br>


**138** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐4: Example Prefetchable Memory Base/Limit Register Meanings_ 

|**Register**|**Value**|**Use**|
|---|---|---|
|Prefetchable Memory<br>Base|4001h|The upper 12 bits of this register hold the<br>upper 12 bits of the 32‐bit BASE address (bits<br>[31:20]). The lower 20 bits of the base address<br>are implied to be all 0s, meaning the base<br>address is always aligned on a 1MB bound‐<br>ary.<br>The lower 4 bits of this register indicate<br>whether a 64‐bit address decoder is supported<br>in the bridge, meaning the Upper Base/Limit<br>Registers are used.|
|Prefetchable Memory<br>Limit|43F1h|Similarly, the upper 12 bits of this register<br>hold the upper 12 bits of the 32‐bit LIMIT<br>address (bits [31:20]). The lower 20 bits of the<br>limit address are all implied to be all Fs.<br>The lower 4 bits of this register have the same<br>meaning as the lower 4 bits of the base regis‐<br>ter.|
|Prefetchable Memory<br>Base Upper 32 Bits|00000002h|Holds the upper 32 bits of the 64‐bit BASE<br>address for Prefetchable Memory down‐<br>stream of this port.|
|Prefetchable Memory<br>Limit Upper 32 Bits|00000002h|Holds the upper 32 bits of the 64‐bit LIMIT<br>address for Prefetchable Memory down‐<br>stream of this port.|



## **Non-Prefetchable Range (NP-MMIO)** 

Unlike the prefetchable memory range, the non‐prefetchable memory range can only support 32‐bit addresses. So there is only one register for the base and one register for the limit. Following the example in Figure 4‐7, the Non‐Prefetchable Memory Base/Limit registers of Port B would be programmed with the values shown in Figure 4‐9 on page 140. The meaning of these values is summarized in Table 4‐5. 

**139** 

**PCI Express Technology** 

_Figure 4‐9: Example Non‐Prefetchable Memory Base/Limit Register Values_ 

**==> picture [375 x 360] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

信息在 PCI Express 设备之间以包的形式移动。三个主要的包类别是_事务层包_ (TLP)、_数据链路层包_ (DLLP) 和_有序集_。本章描述了各种 TLP 的使用、格式和定义以及它们相关字段的详细信息。DLLP 在第 9 章"DLLP 元素"中单独描述，位于第 307 页。

## **下一章**

下一章讨论流控协议 (Flow Control Protocol) 的目的和详细操作。流控旨在确保发送器永远不会发送接收器无法接受的事务层包 (TLP)。这可以防止接收缓冲区溢出，并消除了对 PCI 样式低效（如断开、重试和等待状态）的需求。

## **基于包的协议介绍**

## **概述**

与并行总线不同，像 PCIe 这样的串行传输总线不使用控制信号来识别链路上给定时间正在发生的事情。相反，它们发送的比特流必须具有预期大小和可识别的格式以使接收器能够理解内容。此外，PCI 在包传输时不使用任何立即握手。

除了逻辑空闲符号和称为_有序集_的物理层包之外，信息在活动 PCIe 链路上以由符号组成的基本块（即包）的形式移动。交换的两类主要包是高级的_事务层包_ (TLP) 和低级的链路维护包称为_数据链路层包_ (DLLP)。包及其流如图 5-1（第 170 页）所示。有序集也是包，但它们不像 TLP 和 DLLP 那样用开始和结束符号成帧。它们也不像 TLP 和 DLLP 那样进行字节拆分。有序集包在链路的所有通道上复制。

_图 5-1：TLP 和 DLLP 包_

**==> picture [350 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe 设备 A PCIe 设备 B<br>
设备核心 设备核心<br>
事务层 事务层<br>
数据链路层 数据链路层<br>
物理层 物理层<br>
(RX) (TX) (RX) (TX)<br>
DLLP TLP<br>
DLLP TLP（链路）<br>
事务层包 (TLP)<br>
STP 序列号 HDR 数据 摘要 CRC 结束 TLP 类型：<br>
- 内存读/写<br>
- IO 读/写<br>
- 配置读/写<br>
- 完成<br>
- 消息<br>
数据链路层包 (DLLP)<br>
- 原子操作<br>
成帧 C 成帧 DLLP 类型：<br>
DLLP R - TLP Ack/Nak<br>
(SDP) C (END)<br>
- 电源管理<br>
- 链路流控<br>
- 供应商特定<br>**----- End of picture text -----**<br>


**170**

**第 5 章：TLP 元素**

## **基于包的协议的动机**

使用基于包的协议有三个明显的优势，特别是在数据完整性方面：

## **1. 包格式定义明确**

像 PCI 这样的早期总线允许不确定大小的传输，这使得在传输结束之前不可能识别有效负载边界。此外，任一设备都能够在传输完成之前终止传输，这使得发送方难以计算和发送覆盖整个有效负载的校验和或 CRC。相反，PCI 使用简单的奇偶校验方案并在每个数据阶段对其进行检查。

相比之下，PCIe 包具有已知的大小和格式。包开头处的包_头_指示包类型并包含必填和可选字段。头字段的大小是固定的，但地址可以是 32 位或 64 位大小。一旦传输开始，接收方就无法暂停或提前终止它。这种结构化格式允许在 TLP 中包含信息以帮助可靠传输，包括成帧符号、CRC 和包序列号。

## **2. 成帧符号定义包边界**

在 Gen1 和 Gen2 操作模式下使用 8b/10b 编码时，发送的每个 TLP 和 DLLP 包都由开始和结束控制符号成帧，清楚地定义了接收方的包边界。这是对 PCI 和 PCI-X 的重大改进，其中单个 FRAME# 信号的置位和取消置位指示事务的开始和结束。该信号（或任何其他控制信号）上的毛刺可能导致目标错误地解释总线事件。PCIe 接收器必须在得出链路活动开始或结束的结论之前正确解码完整的 10 位符号，因此意外或无法识别的符号更容易被识别并作为错误处理。

对于 Gen3 中使用的 128b/130b 编码，不再使用控制字符，也不再有这样的成帧符号。有关 Gen3 编码与早期版本之间差异的更多信息，请参见第 12 章"物理层 - 逻辑 (Gen3)"，位于第 407 页。

**171**

**PCI Ex ress Technolo p gy**

## **3. CRC 保护整个包**

与 PCI 在事务的地址和数据阶段使用的外侧带奇偶校验信号不同，PCIe 的带内 CRC 值可验证整个包的无错误传递。TLP 包还由发送器的数据链路层附加序列号，以便如果在接收器处检测到错误，则可以有问题的包可以被自动重新发送。发送器在其_重试缓冲区_ (Retry Buffer) 中维护每个发送的 TLP 的副本，直到它被接收器确认。这种 TLP 确认机制称为_Ack/Nak 协议_（在第 10 章"Ack/Nak 协议"中描述，位于第 317 页），构成了链路级 TLP 错误检测和纠正的基础。这种 Ack/Nak 协议错误恢复机制允许在发生问题的位置或链路及时解决问题，但需要本地硬件解决方案来支持它。

## **事务层包 (TLP) 详细信息**

在 PCI Express 中，高级事务源自发送设备的设备核心并在接收设备的核心处终止。事务层作用于这些请求以在发送器中组装出站 TLP 并在接收器处解释它们。在此过程中，每个设备的数据链路层和物理层也有助于最终的包组装。

## **TLP 组装和拆卸**

链路发送侧的 TLP 组装和接收侧的拆卸的一般流程如图 5-2（第 173 页）所示。现在让我们逐步完成从创建包到将其传送到接收器的核心逻辑的步骤。事务层包组装和拆卸的关键阶段在下面列出。列表编号对应于第 173 页图 5-2 中的编号。

## **发送器：**

1. 设备 A 的核心逻辑向其 PCIe 接口发送请求。如何完成这一点超出了规范或本书的范围。请求包括：

   - 目标地址或 ID（路由信息）

   - 源信息，如 Requester ID 和 Tag

   - 事务类型/包类型（要执行的命令，例如内存读）

   - 数据有效负载大小（如果有）以及数据有效负载（如果有）

   - 流量类（用于分配包优先级）

   - 请求的属性（无窥探、宽松排序等）

**172**

**第 5 章：TLP 元素**

2. 根据该请求，事务层构建 TLP 头，附加任何数据有效负载，并可选地计算和附加摘要（端到端 CRC，ECRC），如果支持并已启用。此时 TLP 被放入虚拟通道缓冲区 (Virtual Channel Buffer)。虚拟通道根据事务排序规则管理 TLP 的顺序，并验证接收器是否有足够的流控信用来接受 TLP，然后才能将其传递到数据链路层。

3. 当它到达数据链路层时，TLP 被分配一个序列号，然后基于 TLP 的内容和该序列号计算链路 CRC。生成包的副本保存在重试缓冲区中以防传输错误，同时也传递给物理层。

_图 5-2：PCIe TLP 组装/拆卸_

**==> picture [370 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) 来自发送器核心的出站：设备 A 设备 B (8) 到达接收器核心：<br>
读/写数据、 R/W 请求，<br>
完成、消息等 数据 设备 设备 完成、消息等。<br>
核心 核心<br>
(2) 事务 事务 (7)<br>
HDR 数据 摘要 层 层 HDR 数据 摘要<br>
(3) (3) 数据 数据 (6) (6)<br>
序列号 HDR 数据 摘要 CRC 链路层 链路层 序列号 HDR 数据 摘要 CRC<br>
STP(4) 序列号 HDR 数据 摘要 CRC End(4) 物理层 物理层 STP(5) 序列号 HDR 数据 摘要 CRC End(5)<br>
(RX) (TX) (RX) (TX)<br>**----- End of picture text -----**<br>


4. 物理层执行多项操作以准备包进行串行传输，包括字节拆分、加扰、编码和比特串行化。对于 Gen1 和 Gen2 设备，当使用 8b/10b 编码时，控制字符 STP 和 END 被添加到包的两端。最后，包通过链路传输。在 Gen3 模式下，STP 标记被添加到 TLP 的前端，但 END 不添加到包的末尾。而是 STP 标记包含有关 TLP 包大小的信息。

## **接收器：**

5. 在接收器（本例中为设备 B）处，为传输做准备而完成的所有操作现在都必须撤消。物理层反串行化比特流，解码得到的符号，并取消拆分字节。

**173**

**PCI Ex ress Technolo p gy**

   - 控制字符在此处被删除，因为它们仅在物理层有意义，然后包被转发到数据链路层。

6. 数据链路层计算 CRC 并将其与接收的 CRC 进行比较。如果匹配，则检查序列号。如果没有错误，则删除 CRC 和序列号，并将 TLP 传递给接收器的事务层，并通过返回 Ack DLLP 通知发送方已正确接收。在发生错误的情况下，将返回 Nak，并且发送器将重新重放其重试缓冲区中的 TLP。

7. 在事务层，TLP 被解码，并且信息被传递给核心逻辑以执行适当的操作。如果接收设备是该包的最终目标，则它检查 ECRC 错误并在有任何相关 ECRC 错误条件时向核心逻辑报告。

## **TLP 结构**

事务层包中每个字段的基本用法在第 174 页表 5-1 中定义。

_表 5-1：TLP 头类型字段定义事务变体_

|**TLP 组件**|**协议层**|**组件用途**|
|---|---|---|
|头|事务层|3 或 4DW（12 或 16 字节）大小。格式因类型而异，但头定义参数，包括：<br>• 事务类型<br>• 目标地址、ID 等<br>• 传输大小（如果有）、字节使能<br>• 属性<br>• 流量类|
|数据|事务层|可选的 1-1024 DW 有效负载，使用字节使能或字节对齐的开始和结束地址进行限定。请注意，不能指定长度为零，但可以通过指定 1 DW 的长度和全零的字节使能来近似零长度读（在某些情况下有用）。完成者的结果数据将是未定义的，但请求者不使用它，因此结果是相同的。|
|摘要/ECRC|事务层|可选。当存在时，ECRC 始终为 1 DW 大小。|



**174**

**第 5 章：TLP 元素**

## **通用 TLP 头格式**

## **概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-4"></a>
## 5.4 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Type 1 Header<br>31 23 15 7 0 (Non-Prefetchable)<br>Device ID Vendor ID 00h Memory Base<br>15 3 0<br>Status Command 04h<br>1111 1001 0000 0000<br>Class Code       ID  Rev 08h (F) (9) (0) (RO)<br>BIST Header Latency Cache 0Ch (RW) Bits 31:20 of Must be 0<br>Type Timer Line Size Non-Prefetchable Base Address<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h Non-Prefetchable<br>F900 0000h<br>Secondary Subordinate Secondary Primary 18h Range Base Address<br>Lat Timer Bus # Bus # Bus # Bits 19:0 are<br>Secondary IO IO 1Ch always 0s for Base<br>Status Limit Base<br>(Non-Prefetchable) (Non-Prefetchable) 20h<br>Memory Limit Memory Base<br>Prefetchable Prefetchable 24h (Non-Prefetchable)<br>Memory Limit Memory Base Memory Limit<br>Prefetchable Memory Base 28h 15 3 0<br>Upper 32 Bits<br>1111 1001 0000 0000<br>Prefetchable Memory Limit 2Ch<br>Upper 32 Bits (F) (9) (0)<br>IO Limit IO Base (RO)<br>Upper 16 Bits Upper 16 Bits 30h (RW) Bits 31:20 of Must be 0<br>Non-Prefetchable LimitAddress<br>Reserved Capability 34h<br>Pointer<br>Expansion ROM Base Address 38h<br>Non-Prefetchable<br>ControlBridge InterruptPin InterruptLine 3Ch Range Limit Address F90F FFFFh<br>Bits 19:0 are<br>always Fs for Limit<br>Non-Prefetchable Memory Range: F900_0000h - F90F_FFFFh<br>**----- End of picture text -----**<br>


**140** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐5: Example Non‐Prefetchable Memory Base/Limit Register Meanings_ 

|**Register**|**Value**|**Use**|
|---|---|---|
|(Non‐Prefetchable)<br>Memory Base|F900h|The upper 12 bits of this register hold the<br>upper 12 bits of the 32‐bit BASE address (bits<br>[31:20]). The lower 20 bits of the base address<br>are implied to be all 0s, meaning the base<br>address is always aligned on a 1MB bound‐<br>ary.<br>The lower 4 bits of this register must be 0s.|
|(Non‐Prefetchable)<br>Memory Limit|F900h|Similarly, the upper 12 bits of this register<br>hold the upper 12 bits of the 32‐bit LIMIT<br>address (bits [31:20]). The lower 20 bits of the<br>limit address are all implied to be all Fs.<br>The lower 4 bits of this register must be 0s.|



This example shows an interesting case where the non‐prefetchable address range programmed in Port B’s configuration space indicates a much larger range (1MB) than the NP‐MMIO range (4KB) owned by the endpoint living downstream. This is because the memory base/limit registers in the Type 1 header, can only be used to specify address bits 20 and above ([31:20]). The lower 20 address bits, [19:0], are implied. So the smallest address range that can be specified with the memory base/limit registers is 1MB. 

In our example, the endpoint requested, and was granted, 4KB of NP‐MMIO (F900_0000h ‐ F900_0FFFh). Port B was programmed with values indicating 1MB, or 1024KB, of NP‐MMIO lived downstream of that port (F900_0000h ‐ F90F_FFFFh). This means 1020KB (F900_1000h ‐ F90F_FFFFh) of memory address space is wasted. This address space CANNOT be allocated to another endpoint because the routing of the packets would not work. 

## **IO Range** 

Like with the prefetchable memory range, Type 1 headers have two pairs of IO base/limit registers. The IO Base/Limit registers store address info for the lower 16 bits of the IO address range. If this bridge supports decoding 32‐bit IO addresses (which is rare in real‐world devices), then the IO Base/Limit Upper 16 Bits registers are also used and hold the upper 16 bits (bits [31:16]) of the IO 

**141** 

**PCI Express Technology** 

address range. Following our example, Figure 4‐10 on page 142 shows the val‐ ues software would program into these registers to indicate that the IO address range of 4000h ‐ 4FFFh lives beneath that bridge (Port B). The meaning of each field in those registers is summarized in Table 4‐6. 

_Figure 4‐10: Example IO Base/Limit Register Values_ 

**==> picture [381 x 340] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>31 23 15 7 0 IO Base<br>Device ID Vendor ID 00h Upper 16 Bits IO Base<br>15 0 7 3 0<br>Status Command 04h<br>0000 0000 0000 0000 0100 0000<br>Class Code       ID  Rev 08h (0) (0) (0) (0) (4) (RO)<br>BIST HeaderType LatencyTimer Line SizeCache 0Ch (RW) Bits 31:16 ofIO Base Address of IO Base Address(RW) Bits 15:12 0h = 16-bit1h = 32-bit<br>(if used)<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h IO Range<br>Secondary Subordinate Secondary Primary 18h Base Address 4000h<br>Lat Timer Bus # Bus # Bus # Bits 11:0 are<br>SecondaryStatus LimitIO BaseIO 1Ch always 0s for IO Base<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Memory LimitPrefetchable Memory BasePrefetchable 24h Upper 16 BitsIO Limit IO Limit<br>Prefetchable Memory Base 28h 15 0 7 3 0<br>Upper 32 Bits<br>0000 0000 0000 0000 0100 0000<br>Prefetchable Memory LimitUpper 32 Bits 2Ch (0) (0) (0) (0) (4) (RO)<br>Upper 16 BitsIO Limit Upper 16 BitsIO Base 30h (RW) Bits 31:16 ofIO Limit Address of IO Limit Address(RW) Bits 15:12 0h = 16-bit1h = 32-bit<br>Reserved CapabilityPointer 34h (if used)<br>Expansion ROM Base Address 38h<br>IO Range<br>ControlBridge InterruptPin InterruptLine 3Ch Limit Address 4FFFh<br>Bits 11:0 are<br>always Fs for IO Limit<br>IO Range: 4000h - 4FFFh<br>**----- End of picture text -----**<br>


**142** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐6: Example IO Base/Limit Register Meanings_ 

|**Register**|**Value**|**Use**|
|---|---|---|
|IO Base|40h|The upper 4 bits of this register hold the<br>upper 4 bits of the 16‐bit BASE address (bits<br>[15:12]). The lower 12 bits of the base address<br>are implied to be all 0s, meaning the base<br>address is always aligned on a 4KB boundary.<br>The lower 4 bits of this register indicate<br>whether a 32‐bit IO address decoder is sup‐<br>ported in the bridge, meaning the Upper Base/<br>Limit Registers are used.|
|IO Limit|40h|Similarly, the upper 4 bits of this register hold<br>the upper 4 bits of the 16‐bit LIMIT address<br>(bits [15:12]). The lower 12 bits of the limit<br>address are all implied to be all Fs.<br>The lower 4 bits of this register have the same<br>meaning as the lower 4 bits of the base regis‐<br>ter.|
|IO Base Upper 16 Bits|0000h|Holds the upper 16 bits of the 32‐bit BASE<br>address for IO downstream of this port.|
|IO Limit Upper 16 Bits|0000h|Holds the upper 16 bits of the 32‐bit LIMIT<br>address for IO downstream of this port.|



In this example, we see another situation where the address range programmed into the upstream bridge far exceeds the actual address range owned by the downstream function. The endpoint in our example owns 256 bytes of IO address space (specifically 4000h ‐ 40FFh). Port B has been programmed with values indicating that 4KB of IO address space lives downstream (addresses 4000h ‐ 4FFFh). Again, this is simply a limitation of Type 1 headers. For IO address space, the lower 12 bits (bits [11:0]) have implied values, so the smallest range of IO addresses that can be specified is 4KB. This limitation turns out to be more serious than the 1MB minimum window for memory ranges. In x86‐ based (Intel compatible) systems, the processors only support 16 bits of IO address space, and since only bits [15:12] of the IO address range can be speci‐ fied in a bridge, that means that there can be a maximum of 16 (2[4] ) different IO address ranges in a system. 

**143** 

**PCI Express Technology** 

## **Unused Base and Limit Registers** 

Not every PCIe device will use all three types of address space. In fact, the PCI Express specification actually discourages the use of IO address space, indicat‐ ing that it is only supported for legacy reasons and may be deprecated in a future revision of the spec. 

In the cases where an endpoint does not request all three types of address space, what are the base and limit registers of the bridges upstream of those devices programmed with? They can’t be programmed with all 0s because the lower address bits would still be implied to be different (base = 0s; limit = Fs) which would represent a valid range. So to handle these cases, the limit register must be programmed with a higher address than the base. For example, if an end‐ point does not request IO address space, then the bridge immediately upstream of that function would have its IO Base register programmed to 00h and its IO Limit register programmed with F0h. Since the limit address is higher than the base address, the bridge understands this is an invalid setting and takes it to mean that there are no functions downstream of it that own IO address space. 

This method of invalidating base and limit registers is valid for all three base and limit pairs, not just for the IO base/limit registers. 

## **Sanity Check: Registers Used For Address Routing** 

To ensure that you understand the rules and methods for setting up BARs and Base/Limit registers, please look over Figure 4‐11 on page 145 to make sure it makes sense. We have simply extended the example system to include addi‐ tional address space requests from the other endpoint, as well as from one of the switch ports (Port A). Remember that Type 1 headers also have BARs (two of them to be exact) and can request address space too. The Base/Limit registers in a bridge do NOT include the addresses owned by that same bridge’s BARs. The Base/Limit registers only represent the addresses that live downstream of that bridge. 

**144** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐11: Final Example Address Routing Setup_ 

**==> picture [370 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
BAR0-1: Not Used (All 0s)<br>IO Range: 4000h - 5FFFh<br>NP-MMIO Range: F900_0000h - F90F_FFFFh<br>P-MMIO Range: 2_3E00_0000h - 2_440F_FFFFh<br>CPU<br>Root Complex MemorySystem<br>P2P (DRAM)<br>BAR0-1: [P-MMIO (1KB)]<br>2_3E00_0000h - 2_3E00_03FFh<br>Port IO Range:<br>A NP-MMIO Range:<br>P2P P-MMIO Range:<br>Switch<br>BAR0-1: Not Used (All 0s) BAR0-1: Not Used (All 0s)<br>IO Range: 4000h - 4FFFh Port Port IO Range: 5000h - 5FFFh<br>NP-MMIO Range: F900_0000h - F90F_FFFFh B C NP-MMIO Range: Not Used (Base > Limit)<br>P-MMIO Range: 2_4000_0000h - 2_43FF_FFFFh P-MMIO Range: 2_4400_0000h - 2_440F_FFFFh<br>PCIe PCIe<br>Endpoint Endpoint<br>BAR0: NP-MMIO (4KB) BAR0-1: P-MMIO (8KB)<br>F900_0000h - F900_0FFFh 2_4400_0000h - 2_4400_1FFFh<br>BAR1-2: P-MMIO (64MB) BAR2-4: Not Used (All 0s)<br>2_4000_0000h - 243FF_FFFFh BAR5: IO (4 bytes)<br>BAR3: IO (256 bytes) 5000h - 5003h<br>4000h - 40FFh<br>BAR4-5: Not Used (All 0s)<br>4000h - 5FFFh<br>F900_0000h - F90F_FFFFh<br>2_4000_0000h - 2_440F_FFFFh<br>P2P P2P<br>**----- End of picture text -----**<br>


## **TLP Routing Basics** 

The purpose of setting up the BARs and Base/Limit registers as described in the previous sections, is to ensure that traffic targeting a function will be routed cor‐ rectly so the targeted function can see the transactions and claim them. In shared‐bus architectures like PCI, all the traffic is visible to every device. The only time routing of requests happens is when the target is on another bus and must cross a bridge. Since PCIe Links are point‐to‐point, more routing will be needed to deliver transactions between devices. 

**145** 

## **PCI Express Technology** 

_Figure 4‐12: Multi‐Port PCIe Devices Have Routing Responsibilities_ 

**==> picture [330 x 297] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>IN OUT IN OUT Memory<br>Switch OUT IN OUT IN<br>Legacy<br>InternalUse Endpoint<br>?<br>Traffic Types:<br>  - Physical Layer Ordered Sets<br>  - Data Link Layer Packets (DLLPs)<br>  - Transaction Layer Packets (TLPs)<br>OUT IN OUT IN<br>    IN = INGRESS PORT<br>PCIe PCIe OUT = EGRESS PORT<br>Endpoint Endpoint<br>IN OUT<br>OUT IN<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

第 175 页图 5-3 说明了通用 TLP 4DW 头的格式和内容。在本节中，总结了几乎所有事务通用的字段。与特定事务类型相关的头格式差异将在后面介绍。

_图 5-3：通用 TLP 头字段_

**==> picture [328 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
事务层包 (TLP)<br>
成帧序列头成帧<br>
(STP)编号(End)<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
最后 DW 第一个 DW<br>
字节 4 字节 4-7 随类型而变化 BE BE<br>
字节 8 字节 8-11 随类型而变化<br>
字节 12 字节 12-15 随类型而变化（并非总是必需）<br>**----- End of picture text -----**<br>


## **通用头字段汇总**

第 176 页表 5-2 总结了每个通用 TLP 头字段的大小和用途。请注意，第 175 页图 5-3 中标记为"R"的字段是保留的，应设置为零。

**175**

## **PCI Ex ress Technolo p gy**

_表 5-2：通用头字段汇总_

|**头字段**|**头位置**|**字段用途**|
|---|---|---|
|Fmt[2:0]<br>（格式）|字节 0 位 7:5|这些位编码有关头大小以及数据有效负载是否将成为 TLP 一部分的信息：<br>00b 3DW 头，无数据<br>01b 4DW 头，无数据<br>10b 3DW 头，带数据<br>11b 4DW 头，带数据<br>4GB 以下的地址必须使用 3DW 头。规范规定，如果对 4GB 以下的地址使用 4DW 头且 64 位地址的高 32 位设置为零，则接收器行为未定义。|
|Type[4:0]|字节 0 位 4:0|这些位编码与此 TLP 一起使用的事务变体。Type 字段与 Fmt [1:0] 字段一起使用以指定事务类型、头大小以及是否存在数据有效负载。有关详细信息，请参见第 178 页的"通用头字段详细信息"。|
|TC [2:0]<br>（流量类）|字节 1 位 6:4|这些位编码要应用于此 TLP 及与其关联的完成（如果有）的流量类：<br>000b = 流量类 0（默认）<br>.<br>.<br>111b = 流量类 7<br>TC 0 是默认类，而 TC 1-7 用于提供差异化服务。有关更多信息，请参见第 247 页的"流量类 (TC)"。|
|Attr [2]<br>（属性）|字节 1 位 2|第三个属性位指示此 TLP 是否要使用基于 ID 的排序。要了解更多信息，请参见第 301 页的"基于 ID 的排序 (IDO)"。|
|TH<br>（TLP 处理提示）|字节 1 位 0|指示何时已包含 TLP 提示以使系统了解如何最好地处理此 TLP。有关其用法的讨论，请参见第 899 页的"TPH（TLP 处理提示）"。|



**176**

**第 5 章：TLP 元素**

_表 5-2：通用头字段汇总（续）_

|**头字段**|**头位置**|**字段用途**|
|---|---|---|
|TD<br>（TLP 摘要）|字节 2 位 7|如果 TD = 1，则此 TLP 已包含可选的 4 字节 TLP 摘要作为 ECRC 值。<br>一些规则：<br>• 必须由所有接收器根据此位检查摘要字段的存在。<br>• TD = 1 但没有摘要的 TLP 将作为畸形 TLP 处理。<br>• 如果设备支持检查 ECRC 且 TD=1，则它必须执行 ECRC 检查。<br>• 如果设备在最终目标不支持检查 ECRC（可选），则它必须忽略该摘要。<br>有关此主题的更多信息，请参见第 653 页的"CRC"和第 657 页的"ECRC 生成和检查"。|
|EP<br>（Poisoned 数据）|字节 2 位 6|如果 EP = 1，则伴随此数据的数据应被视为无效，即使事务被允许正常完成。有关中毒包 (Poisoned Packet) 的更多信息，请参见第 660 页的"数据中毒"。|
|Attr [1:0]<br>（属性）|字节 2 位 5:4|位 5 = 宽松排序：设置为 1 时，为此 TLP 启用 PCI-X 宽松排序。如果为 0，则使用严格的 PCI 排序。<br>位 4 = 无窥探：设置为 1 时，请求者指示此 TLP 不存在主机缓存一致性问题。因此系统硬件可以通过跳过此请求的正常处理器缓存窥探来节省时间。当为 0 时，需要 PCI 类型的缓存窥探保护。|



**177**

## **PCI Ex ress Technolo p gy**

_表 5-2：通用头字段汇总（续）_

|**头字段**|**头位置**|**字段用途**|
|---|---|---|
|地址类型 [1:0]|字节 2 位 3:2|对于内存和原子请求，此字段支持虚拟化系统的地址转换。转换协议在称为_地址转换服务_的单独规范中描述，从中可以看到该字段编码为：<br>00 = 默认/未转换<br>01 = 转换请求<br>10 = 已转换<br>11 = 保留|
|长度 [9:0]|字节 2 位 1:0<br>字节 3 位 7:0|TLP 数据有效负载传输大小，以 DW 为单位。编码：<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|最后 DW 字节使能<br>[3:0]|字节 7 位 7:4|这四个高真位一对一映射到有效负载最后一个双字内的字节。<br>位 7 = 1：最后 DW 中的字节 3 有效；否则无效<br>位 6 = 1：最后 DW 中的字节 2 有效；否则无效<br>位 5 = 1：最后 DW 中的字节 1 有效；否则无效<br>位 4 = 1：最后 DW 中的字节 0 有效；否则无效|
|第一个 DW 字节使能<br>[3:0]|字节 7 位 3:0|这四个高真位一对一映射到有效负载第一个双字内的字节。<br>位 3 = 1：第一个 DW 中的字节 3 有效；否则无效<br>位 2 = 1：第一个 DW 中的字节 2 有效；否则无效<br>位 1 = 1：第一个 DW 中的字节 1 有效；否则无效<br>位 0 = 1：第一个 DW 中的字节 0 有效；否则无效|



## **通用头字段详细信息**

在以下各节中，我们描述了第 175 页图 5-3 中所示的每个 TLP 头字段的详细信息。

**178**

**第 5 章：TLP 元素**

## **头** _**类型/格式**_ **字段编码**

第 179 页表 5-3 总结了 TLP 头 Type 和 Format (Fmt) 字段中使用的编码。

_表 5-3：TLP 头类型和格式字段编码_

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|内存读请求 (MRd)|000 = 3DW，无数据<br>001 = 4DW，无数据|0 0000|
|内存读锁定请求 (MRdLk)|000 = 3DW，无数据<br>001 = 4DW，无数据|0 0001|
|内存写请求 (MWr)|010 = 3DW，带数据<br>011 = 4DW，带数据|0 0000|
|IO 读请求 (IORd)|000 = 3DW，无数据|0 0010|
|IO 写请求 (IOWr)|010 = 3DW，带数据|0 0010|
|配置类型 0 读请求 (CfgRd0)|000 = 3DW，无数据|0 0100|
|配置类型 0 写请求 (CfgWr0)|010 = 3DW，带数据|0 0100|
|配置类型 1 读请求 (CfgRd1)|000 = 3DW，无数据|0 0101|
|配置类型 1 写请求 (CfgWr1)|010 = 3DW，带数据|0 0101|
|消息请求 (Msg)|001 = 4DW，无数据|1 0 rrr*<br>（参见路由字段）|
|带数据消息请求 (MsgD)|011 = 4DW，带数据|1 0rrr*<br>（参见路由字段）|
|完成 (Cpl)|000 = 3DW，无数据|0 1010|
|带数据完成 (CplD)|010 = 3DW，带数据|0 1010|
|完成锁定 (CplLk)|000 = 3DW，无数据|0 1011|
|带数据完成 (CplDLk)|010 = 3DW，带数据|0 1011|
|取并加原子操作请求|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1100|



**179**

**PCI Ex ress Technolo p gy**

_表 5-3：TLP 头类型和格式字段编码（续）_

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|无条件交换原子操作请求|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1101|
|比较并交换原子操作请求|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1110|
|本地 TLP 前缀|100 = TLP 前缀|0L3L2L1L0|
|端到端 TLP 前缀|100 = TLP 前缀|1E3E2E1E0|



## **摘要 / ECRC 字段**

TLP 摘要位报告端到端 CRC (ECRC) 的存在。如果软件支持并启用了此可选功能，则设备为其发起的所有 TLP 计算并应用 ECRC。请注意，使用 ECRC 要求设备包含可选的高级错误报告寄存器，因为它的能力和控制寄存器位于那里。

**ECRC 生成和检查。** ECRC 涵盖 TLP 通过互连结构转发时不会更改的所有字段。但是，在包通过拓扑时有两个位可以合法地更改：

- **Type 字段的位 0** - 当配置事务通过桥转发并且从类型 1 变为类型 0 配置事务时（因为它已到达目标总线），会发生变化。这是通过更改类型字段的位 0 来实现的。

- **错误/Poisoned (EP) 位** - 如果与包关联的数据被视为损坏，则在 TLP 通过互连结构时可能会更改。这是称为错误转发的可选功能。

**谁检查 ECRC？** ECRC 的预期目标是 TLP 的最终接收者。检查 LCRC 验证给定链路上没有传输错误，但在路由元素（交换机或根复合体）的出口端口转发到下一个链路之前，该包会重新计算，这可能会掩盖路由元素中的内部错误。为了防止这种情况，ECRC 在请求者和完成者之间的旅程中保持不变。当目标设备检查 ECRC 时，沿途的任何错误可能性都有很高的概率被检测到。

**180**

**第 5 章：TLP 元素**

规范对交换机在 ECRC 检查中的角色作了两个声明：

- 支持 ECRC 检查的交换机对发往交换机内位置的 TLP 执行此检查。"对于所有其他 TLP，交换机必须保留 ECRC（按原样转发）作为 TLP 的组成部分。"

- "请注意，交换机可以对通过交换机的 TLP 执行 ECRC 检查。交换机检测到的 ECRC 错误以与任何其他设备报告它们相同的方式报告，但不会改变 TLP 通过交换机的路径。"

## **使用字节使能**

**概述。** 与 PCI 一样，PCIe 需要一种机制来协调其 DW 对齐的地址与有时需要的非 DW 对齐的传输大小或开始/结束地址。为此，PCI Express 使用了前面在第 175 页图 5-3 和第 176 页表 5-2 中介绍的两个字节使能字段。第一个 DW 字节使能字段和最后 DW 字节使能字段允许请求者限定所传输的第一个和最后一个双字内感兴趣的字节。

## **字节使能规则**

1. 字节使能位为高真。值 0 表示不应由完成者使用数据有效负载中的相应字节。值 1 表示应使用它。

2. 如果有效数据全部在单个双字内，则最后 DW 字节使能字段必须为 = 0000b。

3. 如果头长度字段指示传输超过 1DW，则第一个 DW 字节使能必须至少启用一位。

4. 如果长度字段指示 3DW 或更多的传输，则第一个 DW 字节使能字段和最后 DW 字节使能字段必须具有连续的位设置。在这些情况下，字节使能仅用于给出有效开始和结束地址距 DW 对齐地址的字节偏移量。

5. 如果传输为 1DW，则第一个 DW 字节使能字段中允许不连续的字节使能位模式。

6. 如果传输在一个到两个 DW 之间，则第一个和第二个 DW 字节使能字段中允许不连续的字节使能位模式。

7. 传输长度为 1DW 且未设置任何字节使能的写请求是合法的，但对完成者没有影响。

**181**

## **PCI Ex ress Technolo p gy**

8. 如果 1 DW 的读请求未设置任何字节使能，则完成者返回 1 DW 的未定义数据的有效负载。这可以用作利用事务排序规则来强制所有先前已发布的写在完成返回之前输出到内存的刷新机制。

**字节使能示例。** 这种情况下的字节使能使用示例如第 182 页图 5-4 所示。请注意，传输长度必须从启用任何有效字节的第一个 DW 扩展到启用任何有效字节的最后一个 DW。因为传输超过 2DW，所以字节使能只能用于指定传输的开始地址位置（2d）和结束地址位置（34d）。

_图 5-4：使用第一个 DW 和最后 DW 字节使能字段_

## **事务描述符字段**

随着事务在请求者和完成者之间移动，有必要唯一地标识一个事务，因为同一请求者在任何时刻可能有多个分离事务排队。为了帮助解决这个问题，规范定义了几个重要的头字段，它们构成唯一的事务描述符 (Transaction Descriptor)，如图 5-5 所示。

**182**

**第 5 章：TLP 元素**

_图 5-5：事务描述符字段_

**==> picture [384 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R R Attr AT Length<br>
tr H D P<br>
字节 4 完成者 ID Cmpl CB 字节数<br>
状态 M<br>
字节 8 请求者 ID 标签 R 低地址<br>**----- End of picture text -----**<br>


虽然事务描述符字段不在相邻的头位置，但总的来说，它们描述了关键的事务属性，包括：

**事务 ID。** Requester ID（请求者的总线、设备和功能号）和 TLP 的 Tag 字段的组合。

**流量类。** 流量类 (TC) 由请求者根据核心逻辑请求添加，并通过拓扑未经修改地传送到完成者。在每个链路上，TC 映射到虚拟通道之一。

**事务属性。** 基于 ID 的排序、宽松排序和无窥探位也与请求包一起传送到完成者。

## **具有数据有效负载的 TLP 的其他规则**

以下规则适用于 TLP 包含数据有效负载时。

1. 长度字段仅指数据有效负载。

2. 有效负载中数据的第一个字节（紧接在头之后）始终与最低（开始）地址相关联。

3. 长度字段始终表示传输的整数个 DW。部分 DW 使用第一个和最后字节使能字段进行限定。

4. 规范规定，当完成者响应单个内存请求返回多个事务时，每个中间事务必须在根复合体的 64 或 128 字节自然对齐地址边界处结束。这由称为读完成边界 (RCB) 的配置位控制。所有其他设备遵循 PCI-X 协议

**183**

## **PCI Ex ress Technolo p gy**

并在自然对齐的 128 字节边界处打破此类事务。这使得桥中的缓冲区管理更简单。

5. 在发送消息请求时，长度字段是保留的，除非消息是带数据的版本 (_MsgD_)。

6. TLP 数据有效负载不得超过 Device Control 寄存器中 Max_Payload_Size 字段的当前值。只有写事务具有数据有效负载，因此此限制不适用于读请求。接收器需要在写期间检查是否违反 Max_Payload_Size 限制，违反将被视为畸形 TLP。

7. 接收器还必须检查长度字段中的值与 TLP 中实际传输的数据量之间的差异。这种类型的违规也被视为畸形 TLP。

8. 请求不得混合会导致内存访问跨越 4KB 边界的开始地址和传输长度组合。虽然对此的检查是可选的，但如果看到则视为畸形 TLP。

## **特定 TLP 格式：请求和完成 TLP**

在本节中，描述了用于完成特定事务类型的 3DW 和 4DW 头的格式。先前描述的许多通用字段适用，但重点放在与特定事务类型处理方式不同的字段上。TLP 头格式的详细描述在以下部分中描述的 TLP 类型：1) IO 请求，2) 内存请求，3) 配置请求，4) 完成和 5) 消息请求。

## **IO 请求**

虽然规范不鼓励使用 IO 事务，但允许传统设备以及可能需要依赖驻留在系统 IO 映射中而不是内存映射中的兼容设备的软件。虽然 IO 事务在技术上可以访问 32 位 IO 范围，但实际上许多系统（和 CPU）将 IO 访问限制在此范围的低 16 位（64KB）。第 185 页图 5-6 描述了系统 IO 映射以及 16 位和 32 位地址边界。不将自己标识为传统设备的设备不允许在其配置基地址寄存器中请求 IO 地址空间。

**184**

**第 5 章：TLP 元素**

_图 5-6：系统 IO 映射_

**IO 请求头格式。** 3 DW IO 请求头如图 5-7（第 185 页）所示，每个字段在后面的部分中描述。

_图 5-7：3DW IO 请求头格式_

**==> picture [281 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体<br>
IO 请求 TLP<br>
a|<br>
传统 =o 成帧(STP)序列号头数据摘要LCRC成帧(End)<br>
端点<br>
+0 +1 +2 +3<br>
对等 7 6 5 4 3 2 1 0 7 nT 6 5 4 3 2 1 0 7 6 5 4 3 2 TTT 1 0 7 6 5 4 3 2 1 0<br>
字节 0 0 x 0Fmt 0 0 0 1 0Type R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 0 1Length<br>
字节 4 请求者 ID 标签 最后 DW BE0 0 0 0 1st DWBE<br>
字节 8 地址 [31:2] R<br>**----- End of picture text -----**<br>


**185**

**PCI Ex ress Technolo p gy**

**IO 请求头字段。** 第 186 页表 5-4 描述了 IO 请求头中每个字段的位置和用途。

_表 5-4：IO 请求头字段_

|**字段名称**|**头字节/位**|**功能**|
|---|---|---|
|Fmt [2:0]<br>（格式）|字节 0 位 7:5|IO 请求的包格式：<br>000b = IO 读（3DW 无数据）<br>010b = IO 写（3DW 带数据）|
|Type [4:0]|字节 0 位 4:0|IO 请求的包类型为 00010b|
|TC [2:0]<br>（流量类）|字节 1 位 6:4|IO 请求的流量类始终为零，确保这些包永远不会干扰任何高优先级的包。|
|Attr [2]<br>（属性）|字节 1 位 2|基于 ID 的排序不适用于 IO 请求，并且此位被保留。|
|TH<br>（TLP 处理提示）|字节 1 位 0|TLP 处理提示不适用于 IO 请求，并且此位被保留。|
|TD<br>（TLP 摘要）|字节 2 位 7|指示 TLP 末尾的摘要字段 (ECRC) 的存在。|
|EP<br>（Poisoned 数据）|字节 2 位 6|指示数据有效负载（如果存在）是否被中毒。|
|Attr [1:0]<br>（属性）|字节 2 位 5:4|宽松排序和无窥探位不适用于 IO 请求，始终为零。|
|AT [1:0]<br>（地址类型）|字节 2 位 3:2|地址类型不适用于 IO 请求，这些位必须为零。|
|长度 [9:0]|字节 2 位 1:0<br>字节 3 位 7:0|以 DW 为单位指示数据有效负载大小。<br>对于 IO 请求，此字段始终为 1，因为最多只能传输 4 个字节。第一个 DW 字节使能限定使用哪些字节。|



**186**

**第 5 章：TLP 元素**

_表 5-4：IO 请求头字段（续）_

|**字段名称**|**头字节/位**|**功能**|
|---|---|---|
|请求者 ID [15:0]|字节 4 位 7:0<br>字节 5 位 7:0|标识请求者的"返回地址"以用于相应的完成。<br>字节 4，7:0 = 总线号<br>字节 5，7:3 = 设备号<br>字节 5，2:0 = 功能号|
|标签 [7:0]|字节 6 位 7:0|这些位标识来自请求者的特定请求。为每个出站请求分配一个唯一的标签值。默认情况下，仅使用位 4:0，但扩展标签和虚拟功能选项可将其扩展到 11 位，从而允许同时处理多达 2048 个未完成的请求。|
|最后 DW BE [3:0]<br>（最后 DW 字节使能）|字节 7 位 7:4|这些位必须为 0000b，因为 IO 请求只能是一个 DW 大小。|
|1st DW BE [3:0]<br>（第一个 DW 字节使能）|字节 7 位 3:0|这些位限定一个 DW 有效负载中的字节。对于 IO 请求，任何位组合都是有效的（包括全零）。|
|地址 [31:2]|字节 8 位 7:0<br>字节 9 位 7:0<br>字节 10 位 7:0<br>字节 11 位 7:2|IO 传输的 32 位起始地址的高 30 位。32 位地址的低两位被保留（00b），强制 DW 对齐的起始地址。|



**187**

**PCI Ex ress Technolo p gy**

## **内存请求**

PCI Express 内存事务包括两类：读请求及其相应的完成，以及写请求。第 188 页图 5-8 中所示的系统内存映射描述了 3DW 和 4DW 内存请求包。请记住规范多次重申的一点：内存传输绝不允许跨越 4KB 地址边界。

_图 5-8：3DW 和 4DW 内存请求头格式_

**==> picture [382 x 316] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体 内存<br>
3DW 或 4DW 内存请求 TLP<br>
成帧(STP)序列号头数据摘要LCRC成帧(End)<br>
4DW 内存请求头<br>
PCIe +0 +1 +2 +3<br>
端点 系统内存映射<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2 64<br>
字节 0 0 x 1Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>
字节 4 请求者 ID 标签 最后 DWBE 1st DWBE<br>
字节 8 地址 [63:32]<br>
字节 12 地址 [31:2] R<br>
3DW 内存请求头<br>
+0 +1 +2 +3<br>
4GB<br>
32<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2<br>
字节 0 0 x 0Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>
字节 4 请求者 ID 标签 最后 DWBE 1st DWBE 0<br>
字节 8 地址 [31:2] R<br>**----- End of picture text -----**<br>


**内存请求头字段。** 第 189 页表 5-5 中列出了 4DW 内存请求头中每个字段的位置和用途。请注意，3DW 头和 4DW 头之间的区别仅在于起始地址字段的位置和大小。

**188**

**第 5 章：TLP 元素**

_表 5-5：4DW 内存请求头字段_

|**字段名称**|**头字节/位**|**功能**|
|---|---|---|
|Fmt [2:0]<br>（格式）|字节 0 位 7:5|包格式：<br>000b = 内存读（3DW 无数据）<br>010b = 内存写（3DW 带数据）<br>001b = 内存读（4DW 无数据）<br>011b = 内存写（4DW 带数据）<br>1xxb = TLP 前缀已添加到包的开头。有关更多信息，请参见第 899 页的"TPH（TLP 处理提示）"。|
|Type[4:0]|字节 0 位 4:0|TLP 包类型字段：<br>00000b = 内存读或写<br>00001b = 内存读锁定<br>类型字段与 Fmt [1:0] 字段一起使用以指定事务类型、头大小以及是否存在数据有效负载。|
|TC [2:0]<br>（流量类）|字节 1 位 6:4|这些位编码要应用于请求及任何关联完成的流量类。<br>000b = 流量类 0（默认）<br>.<br>.<br>111b = 流量类 7<br>有关更多信息，请参见第 247 页的"流量类 (TC)"。|
|Attr [2]<br>（属性）|字节 1 位 2|指示此 TLP 是否要使用基于 ID 的排序。要了解更多信息，请参见第 301 页的"基于 ID 的排序 (IDO)"。|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-5"></a>
## 5.5 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

As illustrated in Figure 4‐12 on page 146, a PCI Express topology consists of independent, point‐to‐point links connecting each device with one or more neighbors. As traffic arrives at the inbound side of a link interface (called the _ingress port_ ), the port checks for errors, then makes one of three decisions: 

1. Accept the traffic and use it internally 

2. Forward the traffic to the appropriate outbound ( _egress_ ) port 

3. Reject the traffic because it is neither the intended target, nor an interface to it (Note that there are other reasons why traffic may be rejected) 

**146** 

**Chapter 4: Address Space & Transaction Routing** 

## **Receivers Check For Three Types of Traffic** 

Assuming a link is fully operational, the receiver interface of each device (ingress port) must detect and evaluated the arrival of the three types of link traffic: Ordered Sets, Data Link Layer Packets (DLLPs), and Transaction Layer Packets (TLPs). Ordered Sets and DLLPs are local to a link and thus are never routed to another link. TLPs can and do move from link to link, based on rout‐ ing information contained in the packet headers. 

## **Routing Elements** 

Devices with multiple ports, like Root Complexes and Switches, can forward TLPs between the ports and are sometimes called Routing Agents or Routing Elements. They accept TLPs that target internal resources and forward TLPs between ingress and egress ports. 

Interestingly, peer‐to‐peer routing support is required in Switches, but for a Root Complex it’s optional. Peer‐to‐peer traffic is typically where one Endpoint sends packets that target another Endpoint. 

Endpoints have only one Link and never expect to see ingress traffic other than what is targeting them. They simply accept or reject incoming TLPs. 

## **Three Methods of TLP Routing** 

## **General** 

TLPs can be routed based on address (either memory or IO), based on ID (meaning Bus, Device, Function number), or routed implicitly. The routing method used is based on the TLP type. Table 4‐7 on page 147 summarizes the TLP types and the routing methods used for each. 

_Table 4‐7: PCI Express TLP Types And Routing Methods_ 

|**TLP Type**|**Routing Method Used**|
|---|---|
|Memory Read [Lock], Memory Write, AtomicOp|Address Routing|
|IO Read and Write|Address Routing|



**147** 

**PCI Express Technology** 

_Table 4‐7: PCI Express TLP Types And Routing Methods (Continued)_ 

|**TLP Type**|**Routing Method Used**|
|---|---|
|Configuration Read and Write|ID Routing|
|Message, Message With Data|Address Routing, ID Rout‐<br>ing, or Implicit routing|
|Completion, Completion With Data|ID Routing|



Messages are the only TLP type that support more than one routing method. Most of the message TLPs defined in the PCI Express spec use implicit routing, however, the vendor‐defined messages could use address routing or ID routing if desired. 

## **Purpose of Implicit Routing and Messages** 

In implicit routing, neither address or ID routing information applies; instead, the packet is routed based on a code in the packet header indicating a destina‐ tion with a known location in the topology, such as the Root Complex. This sim‐ plifies routing of messages in the cases where a type of implicit routing applies. 

**Why Messages?** Message transactions were not defined in PCI or PCI‐X, but were introduced with PCIe. The main reason for adding Messages as a packet type was to pursue the PCIe design goal to drastically reduce the number of sideband signals implemented in PCI (e.g. interrupt pins, error pins, power management signals, etc.). Consequently, most of the sideband signals were replaced with in‐band packets in the form of Message TLPs. 

**How Implicit Routing Helps** Using in‐band messages in place of side‐ band signals requires a means of routing them to the proper recipient in a topology consisting of numerous point‐to‐point links. Implicit routing takes advantage of the fact that Switches and other routing elements understand the concept of upstream and downstream, and that the Root Complex is found at the top of the topology while Endpoints are found at the bottom. As a result, a Message can use a simple code to show that it should go to the Root Complex, for example, or to be sent to all devices downstream. This ability eliminates the need to define address ranges or ID lists specifically used as the target of different message transactions. 

The different types of implicit routing can be found in “Implicit Routing” on page 163. 

**148** 

**Chapter 4: Address Space & Transaction Routing** 

## **Split Transaction Protocol** 

Like most other serial technologies, PCI Express uses the split transaction proto‐ col which allows a target device to receive one or more requests and then respond to each request with a separate completion. This is a significant improvement over the PCI bus protocol that used wait‐states or delayed trans‐ actions (retries) to deal with latencies in accessing targets. Instead of testing to see when the target becomes ready to do a long‐latency transfer, the target ini‐ tiates the response whenever it’s ready. This results in at least two separate TLPs per transaction ‐ the Request and the Completion (as will be discussed later, a single read request may result in multiple completion TLPs being sent back). Figure 4‐13 on page 149 illustrates the Request‐Completion components of a split transaction. This example shows software reading data from an Endpoint. 

_Figure 4‐13: PCI Express Transaction Request And Completion TLPs_ 

**==> picture [304 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>IN OUT Memory<br>1) Request TLP (Memory Read)<br>K27.7 K29.7<br>OUT IN STP SEQ HDR LCRC END<br>END byte<br>Link CRC (4 bytes)<br>TLP Header (3DW or 4DW)<br>Switch<br>TLP Sequence Number (2 bytes)<br>Receiver decode of STP symbol indicates<br>start of a TLP<br>2) Completion w/Data TLP<br>K27.7 K29.7<br>OUT IN STP SEQ HDR Data LCRC END<br>PCIe<br>Endpoint<br>IN OUT<br>OUT IN<br>**----- End of picture text -----**<br>


**149** 

**PCI Express Technology** 

## **Posted versus Non-Posted** 

To mitigate the penalty of the Request‐Completion latency, memory write trans‐ actions are posted, meaning the transaction is considered completed from the Requester’s perspective as soon as the request leaves the Requester. If helpful, you can associate the term “posting” with the postal system, where posting a memory write is analogous to posting a letter in the mail. Once you’ve placed a letter in the postal box you put your faith in the system to deliver it and don’t wait for verification of delivery. This approach can be much faster than waiting for the entire Request‐Completion transit, but — as in all posting schemes — uncertainty exists concerning when (and if) the transaction completed success‐ fully at the ultimate recipient. 

In PCIe, the small amount of uncertainty involved by making all memory writes posted is considered acceptable in exchange for the performance gained. By contrast, writes to IO and configuration space almost always affect device behavior and have a timeliness associated with them. Consequently, it is impor‐ tant to know when (and if) those write requests completed. Because of this, IO writes and configuration writes are always non‐posted and a completion will always be returned to report the status of the operation. 

In summary, non‐posted transactions require a completion. Posted transactions do not require, and should never receive, a completion. Table 4‐8 on page 150 lists which PCIe transactions are posted and non‐posted. 

_Table 4‐8: Posted and Non‐Posted Transactions_ 

|**Request**|**How Request Is Handled**|
|---|---|
|Memory Write|All**memory write requests are posted**. No completions are<br>expected or sent.|
|Memory Read<br>Memory Read Lock|All**memory read requests are non‐posted**. A completion<br>with data (made of one or more TLPs) will be returned by the<br>Completer to deliver both the requested data and the status<br>of the memory read. In the event of an error, a completion<br>without data will be returned reporting the status.|
|AtomicOp|All**AtomicOp requests are non‐posted**. A completion with<br>data will be returned by the Completer containing the origi‐<br>nal value of the target location.|



**150** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐8: Posted and Non‐Posted Transactions (Continued)_ 

|**Request**|**How Request Is Handled**|
|---|---|
|IO Read<br>IO Write|All**IO requests are non‐posted**. A completion without data<br>will be returned for writes or failed reads, and a completion<br>with data will be returned for successful reads.|
|Configuration Read<br>Configuration Write|All**configuration requests are non‐posted**. A completion<br>without data will be returned for writes and failed reads,<br>while a completion with data will be returned for successful<br>reads.|
|Message|All**messages are posted**. The routing method depends on<br>the Message type, but they’re all considered posted requests.|



## **Header Fields Define Packet Format and Type** 

## **General** 

As shown in Figure 4‐14 on page 152, each TLP contains a three or four double‐ word (12 or 16 byte) header. This includes _Format_ and _Type_ fields that define the content of the rest of the header and indicate the routing method to be used for the TLP as it traverses the topology. 

**151** 

**PCI Express Technology** 

_Figure 4‐14: Transaction Layer Packet Generic 3DW And 4DW Headers_ 

**==> picture [256 x 344] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (END)<br>Generic 3DW (12-byte) Header<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Generic 4DW (16-byte) Header<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


**152** 

**Chapter 4: Address Space & Transaction Routing** 

## **Header Format/Type Field Encodings** 

Table 4‐9 on page 153 below summarizes the encodings used in TLP header For‐ mat and Type fields. 

_Table 4‐9: TLP Header Format and Type Field Encodings_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Memory Read Request (MRd)|000 = 3DW, no data<br>001 = 4DW, no data|0 0000|
|Memory Read Lock Request (MRdLk)|000 = 3DW, no data<br>001 = 4DW, no data|0 0001|
|Memory Write Request (MWr)|010 = 3DW, w/<br>data<br>011 = 4DW, w/<br>data|0 0000|
|IO Read Request (IORd)|000 = 3DW, no data|00010|
|IO Write Request (IOWr)|010 = 3DW, w/<br>data|0 0010|
|Config Type 0 Read Request (CfgRd0)|000 = 3DW, no data|0 0100|
|Config Type 0 Write Request<br>(CfgWr0)|010 = 3DW, w/<br>data|0 0100|
|Config Type 1 Read Request (CfgRd1)|000 = 3DW, no data|0 0101|
|Config Type 1 Write Request<br>(CfgWr1)|010 = 3DW, w/<br>data|0 0101|
|Message Request (Msg)|001 = 4DW, no data|1 0RRR* (for RRR,<br>see routing subfield<br>in “Message Type<br>Field Summary” on<br>page 164)|
|Message Request w/Data (MsgD)|011 = 4DW, w/<br>data|1 0RRR* (for RRR,<br>see routing subfield<br>in “Message Type<br>Field Summary” on<br>page 164)|



**153** 

**PCI Express Technology** 

_Table 4‐9: TLP Header Format and Type Field Encodings (Continued)_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Completion (Cpl)|000 = 3DW, no data|0 1010|
|Completion W/Data (CplD)|010 = 3DW, w/<br>data|0 1010|
|Completion‐Locked (CplLk)|000 = 3DW, no data|0 1011|

</td>
<td style="background-color:#e8e8e8">

如图 4-18（第 159 页）所示，内存或 IO 请求使用 3DW 头；如图 4-19（第 160 页）所示，64 位内存请求使用 4DW 头。图 4-18 还说明了一个事实：尽管 IO 地址空间实际上是 32 位的（在某些系统中是 16 位的），但请求中的 32 位地址放在 3DW 头的字节 8-11 中。

注意：通用字段在前面"通用 TLP 头格式"部分中有详细描述。表 4-7（第 147 页）总结了 TLP 类型和路由方法。表 4-9（第 153 页）显示了 TLP 头 Type 和 Fmt 字段的编码。

## **请求者 ID 和标签字段**

请求者 ID 和标签字段是头中的两个重要字段，因为它们一起形成事务 ID。事务 ID 唯一地标识从同一请求者同时在系统中传输的众多未完成事务中的特定事务。它们在 TLP 头中的位置如图 4-22（第 164 页）所示。完成者使用事务 ID 将相应的完成与正确的请求匹配。

## **请求者 ID 字段**

**请求者 ID** 标识 TLP 的发起者。PCI Express 请求者 ID 的格式与 PCI/PCI-X 中的格式相同：包括请求者的总线号、设备号和功能号（BDF）。发出请求时，请求者用其自己的 BDF 填充此字段，接收完成时使用它来知道该完成去往何处。

## **标签字段**

**标签** 字段是请求者分配给每个出站请求的唯一标识符。它允许请求者将传入的完成与正确的请求匹配。默认情况下，标签字段是 8 位，允许每个请求者同时跟踪多达 32 个未完成请求（位 7:5 保留且必须为零）。但是，启用 Extended Tag 位允许使用标签字段的位 7:0，允许同时跟踪多达 256 个未完成请求。

## **完成**

完成是从完成者返回到请求者的 TLP，以响应该请求者发出的非发布事务。在大多数情况下，完成被路由回到使用其 Requester ID 发起请求的请求者。除了返回所请求的数据（对于读请求）之外，完成还向请求者报告事务状态（例如，成功、错误等）。

完成有两种主要类型：完成 (Cpl) 和带数据完成 (CplD)。完成不包含数据有效负载。带数据完成包含所请求的数据。

## **完成路由**

完成始终使用 ID 路由。它们被路由回完成包中 Requester ID 字段中标识的请求者。请求者 ID 在完成包头中（字节 4-5），与请求 TLP 中的位置相同。

## **完成状态**

完成 TLP 头中的完成者 ID (Completer ID) 字段表示完成的状态。状态值包括：

- 成功完成 (SC) - 000b = 正常完成，无错误

- 不支持的请求 (UR) - 001b = 请求的寻址设备不支持该请求

- 配置请求重试状态 (CRS) - 010b = 仅对配置请求有效

- 完成者中止 (CA) - 100b = 请求者无法完成请求

## **4DW 完成头格式**

图 4-23（第 166 页）显示了 4DW 完成头格式。带数据完成使用 4DW 头，而完成（Cpl）使用 3DW 头。

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 完成者 ID Cmpl CB 字节数<br>
状态 M<br>
字节 8 请求者 ID 标签 R 低地址<br>**----- End of picture text -----**<br>


**166**

**第 4 章：地址空间与事务路由**

## **完成头字段**

完成头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：完成格式

  - 000b = 3DW 完成（无数据）

  - 010b = 3DW 带数据完成

  - 100b = 3DW 带数据的带数据完成

- **Type [4:0]**（字节 0 位 4:0）：完成类型

  - 01010b = 完成

  - 01010b = 带数据完成（与完成相同的 Type 字段）

- **TC [2:0]**（字节 1 位 6:4）：流量类。完成使用与请求相同的 TC。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序（IDO）。完成使用与请求相同的设置。

- **TD**（字节 2 位 7）：TLP 摘要。如果请求的 TD = 1，则完成包含摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。如果完成者检测到数据中的错误，则将 EP 位置位。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。完成使用与请求相同的设置。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。完成使用与请求相同的设置。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：完成数据有效负载的大小（以 DW 为单位）。对于 Cpl，此字段保留。

- **完成者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：完成者的 BDF。这标识哪个设备生成了完成。

- **完成状态 [2:0]**（字节 5 位 2:0）：指示完成状态。

- **BCM**（字节 5 位 3）：字节计数修改。指示字节计数字段是否已被修改。

- **字节计数 [11:0]**（字节 6 位 7:0，字节 7 位 7:4）：完成者返回的剩余字节数。

- **请求者 ID [15:0]**（字节 8 位 7:0，字节 9 位 7:0）：完成应路由到的请求者的 BDF。

- **标签 [7:0]**（字节 10 位 7:0）：来自对应请求的标签字段。

- **低地址 [6:0]**（字节 11 位 6:0）：对于读完成，这是返回数据中第一个启用字节的地址的低位。

## **消息请求**

消息 TLP 是 PCIe 中引入的新概念。它们用于传达传统上需要单独信号的事件。消息始终使用 4DW 头。

## **消息类型字段**

消息 TLP 头中的 Type 字段分为两个子字段：消息类型（位 4:3）和消息路由子字段（位 2:0）。

- 消息类型始终为 10b，表示这是一个消息。

- 路由子字段指定消息的目标：

  - 000b = 隐式 - 路由到根复合体

  - 001b = 按地址路由（头字节 8-15 包含地址）

  - 010b = 按 ID 路由（头字节 8-9 包含 ID）

  - 011b = 隐式 - 向下游广播

  - 100b = 隐式 - 本地：在接收方终止

  - 101b = 隐式 - 收集并路由到根复合体

  - 110b - 111b = 保留

## **消息头格式**

图 4-24（第 167 页）显示了消息 TLP 头格式。消息使用 4DW 头。

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 请求者 ID 标签 消息代码<br>
字节 8 字节 8-11 随消息代码而变化<br>
字节 12 字节 12-15 随消息代码而变化<br>**----- End of picture text -----**<br>


## **消息头字段**

消息头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：消息格式

  - 001b = 4DW 消息（无数据）

  - 011b = 4DW 消息（带数据）

- **Type [4:0]**（字节 0 位 4:0）：消息类型

  - 位 4:3 = 10b（消息）

  - 位 2:0 = 路由子字段

- **TC [2:0]**（字节 1 位 6:4）：流量类。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序。

- **TH**（字节 1 位 0）：TLP 处理提示。

- **TD**（字节 2 位 7）：TLP 摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：消息数据有效负载大小（如果存在）。

- **请求者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：发起消息的设备的 BDF。

- **标签 [7:0]**（字节 6 位 7:0）：消息标签。

- **消息代码 [7:0]**（字节 7 位 7:0）：定义消息类型的代码。这确定字节 8-15 中字段的含义。

- **字节 8-15**：随消息代码字段而变化。

## **消息代码**

PCI Express 规范定义了多个消息代码。这些代码分为几类：

- **电源管理消息**：用于电源管理事件

- **INTx 中断消息**：传统中断信令

- **错误消息**：错误信令

- **锁定事务消息**：锁定事务支持

- **热插拔消息**：热插拔信令

- **供应商定义消息**：供应商特定消息

- **插槽功率限制消息**：插槽功率限制设置

## **总结**

本章描述了 PCIe 设备中事务路由的基本机制。BAR 和 Base/Limit 寄存器一起允许系统正确路由事务。ID 路由用于配置和完成，而地址路由用于内存和 IO 请求。隐式路由允许消息传达传统信号事件而无需定义地址或 ID 范围。下一章将详细描述事务层包 (TLP) 的内容。

**167**

**第 4 章：地址空间与事务路由**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-6"></a>
## 5.6 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Completion w/Data (CplDLk)|010 = 3DW, w/<br>data|0 1011|
|Fetch and Add AtomicOp Request<br>(FetchAdd)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1100|
|Unconditional Swap AtomicOp<br>Request (Swap)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1101|
|Compare and Swap AtomicOp<br>Request (CAS)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1110|
|Local TLP Prefix (LPrfx)|100 = 1DW|0 LLLL|
|End‐to‐End TLP Prefix (EPrfx)|100 = 1DW|1 EEEE|



## **TLP Header Overview** 

When TLPs are received at an ingress port, they are first checked for errors at the Physical and Data Link Layers. If there are no errors, the TLP is examined at the Transaction Layer to learn which routing method is to be used. The basic steps are: 

1. _Format_ and _Type_ fields determine the header size, format and type of the packet. 

2. Depending on the routing method associated with the packet type, the device determines whether it’s the intended recipient. If so, it will accept (consume) the TLP, but if not, it will forward the TLP to the appropriate egress port ‐ subject to the rules for ordering and flow control for that egress port. 

3. If this device is not the intended recipient nor is it in the path to the intended recipient, it will generally reject the packet as an Unsupported Request (UR). 

**154** 

**Chapter 4: Address Space & Transaction Routing** 

## **Applying Routing Mechanisms** 

Once the system addresses have been configured and transactions are enabled, devices examine incoming TLPs and use the corresponding configuration fields to route the packet. The following sections describe the basic features/function‐ ality of each routing mechanism used in routing TLPs through the PCI Express fabric. 

## **ID Routing** 

ID routing is used to target the logical position ‐ Bus Number, Device Number, Function Number (typically referred to as **BDF** ), of a Function within the topol‐ ogy. It’s compatible with routing methods used in the PCI and PCI‐X protocols for configuration transactions. In PCIe, it is still used for routing configuration packets and is also used to route completions and some messages. 

## **Bus Number, Device Number, Function Number Limits** 

PCI Express supports the same topology limits as PCI and PCI‐X: 

1. Eight bits are used to give the bus number, so a **maximum of 256 busses** are possible in a system. This includes internal busses created by Switches. 

2. Five bits give the device number, so a **maximum of 32 devices** are possible per bus. An older PCI bus or an internal bus in a switch or root complex may host more than one downstream device. However, external PCIe links are always point‐to‐point and there’s only one downstream device on the link. The device number for an external link is forced by the downstream port to always be Device 0, so every external Endpoint will always be Device 0 (unless using Alternative Routing‐ID Interpretation (ARI), in which case, there are no device numbers; more about ARI can be found in the section on “IDO (ID‐based Ordering)” on page 909. 

3. Three bits give the function number, so a **maximum of 8 internal functions** is possible per device. 

## **Key TLP Header Fields in ID Routing** 

If the Type field in a received TLP indicates ID routing is to be used, then the ID fields in the header (Bus, Device, Function) are used to perform the routing check. There are two cases: ID routing with a 3DW header and ID routing with a 4DW header (only possible in messages). Figure 4‐15 on page 156 illustrates a TLP using ID routing and the 3DW header, while Fig‐ ure 4‐16 on page 156 shows the 4DW header for ID routing. 

**155** 

**PCI Express Technology** 

_Figure 4‐15: 3DW TLP Header ‐ ID Routing Fields_ 

**==> picture [354 x 357] intentionally omitted <==**

**----- Start of picture text -----**<br>
3DW Header Using ID Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 0 Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Device Func<br>Byte 8 Bus Number Bytes 10-11 Vary with  Type  Field<br>Function Number with ARI<br>Figure 4‐16: 4DW TLP Header ‐ ID Routing Fields<br>4DW Header Using ID Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Device Func<br>Byte 8 Bus Number Bytes 10-11 Vary with  Type  Field<br>Function Number with ARI<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


## **Endpoints: One Check** 

For ID routing, an Endpoint simply checks the ID field in the packet header against its own BDF. Each function “captures” its own Bus and Device Number every time a Type 0 configuration write is seen on its link from bytes 8‐9 in the TLP Header. Where the captured Bus and Device Number information should be stored in not specified, only that functions must save it. The saved Bus and 

**156** 

**Chapter 4: Address Space & Transaction Routing** 

Device numbers are used as the Requester ID in TLP requests that this Endpoint initiates so the Completer of that request can include the Requester ID value in the completion packet(s). The Requester ID in a completion packet is used to route the completion. 

## **Switches (Bridges): Two Checks Per Port** 

For an ID‐routed TLP, a switch port first checks to see whether it is the intended target by comparing the target ID in the TLP Header against its own BDF, as shown by (1) in Figure 4‐17 on page 158. As was true for an Endpoint, each switch port captures its own Bus and Device number every time a configuration write (Type 0) is detected on its Upstream Port. If the target ID field in the TLP agrees with the ID of the switch port, it consumes the packet. If the ID field doesn’t match, it then checks to see if the TLP is targeting a device below this switch port. It does this by checking the Secondary and Subordinate Bus Num‐ ber registers to see if the target Bus Number in the TLP is within this range (inclusive). If so, then the TLP should be forwarded downstream. This check is indicated by (2) in Figure 4‐17 on page 158. If the packet was moving down‐ stream (arrived on the Upstream Port) and doesn’t match the BDF of the Upstream Port or fall within the Secondary‐Subordinate bus range, it will be handled as an Unsupported Request on the Upstream Port. 

If the Upstream Port determines that a TLP it received is for one of the devices beneath it (because the target bus number was within the range of its Second‐ ary‐Subordinate bus number range), then it forwards it downstream and all the downstream ports of the switch perform the same checks. Each downstream port checks to see if the TLP is targeting them. If so, the targeted port will con‐ sume the TLP and the other ports ignore it. If not, all downstream ports check to see if the TLP is targeting a device beneath their port. The one port that returns true on that check will forward the TLP to its Secondary Bus and the other downstream ports ignore the TLP. 

In this section, it is important to remember that each port on a switch is a Bridge, and thus has its own configuration space with a Type 1 Header. Even though Figure 4‐17 on page 158 only shows a single Type 1 Header, in reality, each port (each P2P Bridge) has its own Type 1 Header and performs the same two checks on TLPs when they are seen by that port. 

**157** 

**PCI Express Technology** 

_Figure 4‐17: Switch Checks Routing Of An Inbound TLP Using ID Routing_ 

**==> picture [338 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>CPU 31 23 15 7 0<br>Device ID Vendor ID 00h<br>__ es<br>Status Command 04h<br>Root Complex MemorySystem Class Code Line SizeCache 08h<br>— P2P - (DRAM) ee [TT] TSS BIST HeaderType LatencyTimer ee Line SizeCache 0Ch<br>Base Address 0 (BAR0) 10h<br>TLP ID Field<br>1. Packet for me?<br>(BDF) ; ee Base Address 1 (BAR1) 14h<br>Secondary Subordinate Secondary Primary 18h<br>P2P Lat Timer Bus # Bus # Bus #<br>Switch + 2. Packet for someone    beneath me? SS SecondaryStatus LimitIO BaseIO 1Ch<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>NIK —}--—— Memory LimitPrefetchable Memory BasePrefetchable 24h<br>Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>PCIe ma PCIe Cc — OO IO Limit IO Base<br>oe Upper 16 Bits Upper 16 Bits 30h<br>Endpoint Endpoint Reserved Capability 34h<br>a Pointer<br>Expansion ROM Base Address 38h<br>—<br>or ControlBridge InterruptPin InterruptLine 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Address Routing** 

TLPs that use address routing refer to the same memory (system memory and memory‐mapped IO) and IO address maps that PCI and PCI‐X transactions do. Memory requests targeting an address below 4GB (i.e. a 32‐bit address) must use a 3DW header, and requests targeting an address above 4GB (i.e. a 64‐bit address) must use a 4DW header. IO requests are restricted to 32‐bit addresses and are only implemented to support legacy functionality. 

**158** 

**Chapter 4: Address Space & Transaction Routing** 

## **Key TLP Header Fields in Address Routing** 

When the Type field indicates address routing is to be used for a TLP, then the Address Fields in the header are used to perform the routing check. These can be 32‐bit addresses or 64‐bit addresses. 

**TLPs with 32‐Bit Address** For IO or 32‐bit memory requests, a 3DW header is used as shown in Figure 4‐18. The memory‐mapped registers tar‐ geted with these TLPs will therefore reside below the 4GB memory or IO address boundary. 

**TLPs with 64‐Bit Address** For 64‐bit memory requests, a 4DW header is used as shown in Figure 4‐19 on page 160. The memory‐mapped registers targeted with these TLPs are able to reside above the 4GB memory bound‐ ary. 

_Figure 4‐18: 3DW TLP Header ‐ Address Routing Fields_ 

**==> picture [370 x 148] intentionally omitted <==**

**----- Start of picture text -----**<br>
3DW Header Using Address Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>0 x 0 tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**159** 

**PCI Express Technology** 

_Figure 4‐19: 4DW TLP Header ‐ Address Routing Fields_ 

**==> picture [372 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
4DW Header Using Address Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>0 x 1 tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- End of picture text -----**<br>


## **Endpoint Address Checking** 

If an Endpoint receives a TLP that uses address routing then it checks the address in the header against each of its implemented Base Address Registers (BARs) in its configuration header, as shown in Figure 4‐20. Since Endpoints only have one link interface, it will either accept the packet or reject it. The End‐ point will accept the packet if the target address in the TLP matches one of the ranges programmed into its BARs. More info on how the BARs are used can be found in section “Base Address Registers (BARs)” on page 126. 

**160** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐20: Endpoint Checks Incoming TLP Address_ 

**==> picture [335 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

内存和 IO 请求字段在本节中讨论。表 4-5（第 189 页）中描述了 4DW 内存请求头中的字段。

## **完成头格式**

完成 TLP 是从完成者返回到请求者的 TLP，以响应该请求者发出的非发布事务。完成使用 3DW 或 4DW 头，取决于它们是否携带数据（带数据的完成使用 4DW 头）。完成头格式在第 190 页图 4-23 中显示。

_图 4-23：3DW 和 4DW 完成头格式_

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 完成者 ID Cmpl CB 字节数<br>
状态 M<br>
字节 8 请求者 ID 标签 R 低地址<br>**----- End of picture text -----**<br>


## **完成头字段**

完成头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：完成格式

  - 000b = 3DW 完成（无数据）

  - 010b = 3DW 带数据完成（带数据）

- **Type [4:0]**（字节 0 位 4:0）：完成类型

  - 01010b = 完成 (Cpl) 或带数据完成 (CplD)

- **TC [2:0]**（字节 1 位 6:4）：流量类。完成使用与请求相同的 TC。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序（IDO）。完成使用与请求相同的设置。

- **TD**（字节 2 位 7）：TLP 摘要。如果请求的 TD = 1，则完成包含摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。如果完成者检测到数据中的错误，则将 EP 位置位。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。完成使用与请求相同的设置。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。完成使用与请求相同的设置。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：完成数据有效负载的大小（以 DW 为单位）。对于 Cpl，此字段保留。

- **完成者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：完成者的 BDF。这标识哪个设备生成了完成。

- **完成状态 [2:0]**（字节 5 位 2:0）：指示完成状态。状态值包括：

  - 000b = 成功完成 (SC)

  - 001b = 不支持的请求 (UR)

  - 010b = 配置请求重试状态 (CRS) - 仅对配置请求有效

  - 100b = 完成者中止 (CA)

- **BCM**（字节 5 位 3）：字节计数修改。指示字节计数字段是否已被修改。

- **字节计数 [11:0]**（字节 6 位 7:0，字节 7 位 7:4）：完成者返回的剩余字节数。

- **请求者 ID [15:0]**（字节 8 位 7:0，字节 9 位 7:0）：完成应路由到的请求者的 BDF。

- **标签 [7:0]**（字节 10 位 7:0）：来自对应请求的标签字段。

- **低地址 [6:0]**（字节 11 位 6:0）：对于读完成，这是返回数据中第一个启用字节的地址的低位。

**190**

**第 4 章：地址空间与事务路由**

## **完成路由**

完成始终使用 ID 路由。它们被路由回完成包中 Requester ID 字段中标识的请求者。请求者 ID 在完成包头中（字节 4-5），与请求 TLP 中的位置相同。

## **完成拆分**

PCI Express 规范允许完成者将单个大型读请求拆分为多个完成 TLP。这对于返回跨 4KB 或更大边界的请求的数据很有用。完成者可以通过将多个完成 TLP 排队到同一请求者来拆分完成。这些拆分完成共享相同的 Requester ID 和 Tag 字段，但每个完成都包含返回数据的不同部分。

拆分完成时，必须遵循以下规则：

- 每个完成 TLP 必须以自然对齐的地址边界结束（对于 Root Complex 为 64 或 128 字节，对于其他设备为 128 字节）。此边界由读完成边界 (RCB) 配置位控制。

- 第一个拆分完成返回请求的最低地址部分。

- 后续完成返回连续地址部分。

- 最后一个完成的数据长度可能小于其他完成。

- 所有拆分完成必须使用相同的 Requester ID、Tag 和 TC。

## **完成错误处理**

完成 TLP 头中的状态字段指示事务是成功还是遇到错误。常见错误状态包括：

- **UR（不支持的请求）**：请求针对的设备无法处理该类型的请求。设备可能不存在或不支持该请求类型。

- **CA（完成者中止）**：完成者检测到错误条件并中止事务。

- **CRS（配置请求重试状态）**：仅对配置请求有效。表示设备暂时无法响应，请求者应重试。

## **消息请求**

消息 TLP 是 PCIe 中引入的新概念。它们用于传达传统上需要单独信号的事件。消息始终使用 4DW 头。

## **消息头格式**

图 4-24（第 191 页）显示了消息 TLP 头格式。

_图 4-24：消息 TLP 头格式_

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 请求者 ID 标签 消息代码<br>
字节 8 字节 8-11 随消息代码而变化<br>
字节 12 字节 12-15 随消息代码而变化<br>**----- End of picture text -----**<br>


## **消息头字段**

消息头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：消息格式

  - 001b = 4DW 消息（无数据）

  - 011b = 4DW 消息（带数据）

- **Type [4:0]**（字节 0 位 4:0）：消息类型

  - 位 4:3 = 10b（消息）

  - 位 2:0 = 路由子字段

- **TC [2:0]**（字节 1 位 6:4）：流量类。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序。

- **TH**（字节 1 位 0）：TLP 处理提示。

- **TD**（字节 2 位 7）：TLP 摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：消息数据有效负载大小（如果存在）。

- **请求者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：发起消息的设备的 BDF。

- **标签 [7:0]**（字节 6 位 7:0）：消息标签。

- **消息代码 [7:0]**（字节 7 位 7:0）：定义消息类型的代码。

- **字节 8-15**：随消息代码字段而变化。

**191**

**第 4 章：地址空间与事务路由**

## **消息路由**

消息 TLP 可以使用三种路由方法之一：地址路由、ID 路由或隐式路由。消息头 Type 字段的位 2:0（路由子字段）确定使用哪种路由方法：

- 000b = 隐式 - 路由到根复合体

- 001b = 按地址路由（头字节 8-15 包含地址）

- 010b = 按 ID 路由（头字节 8-9 包含 ID）

- 011b = 隐式 - 向下游广播

- 100b = 隐式 - 本地：在接收方终止

- 101b = 隐式 - 收集并路由到根复合体

- 110b - 111b = 保留

## **消息代码**

PCI Express 规范定义了多个消息代码。这些代码分为几类：

- **电源管理消息**：用于电源管理事件

- **INTx 中断消息**：传统中断信令

- **错误消息**：错误信令

- **锁定事务消息**：锁定事务支持

- **热插拔消息**：热插拔信令

- **供应商定义消息**：供应商特定消息

- **插槽功率限制消息**：插槽功率限制设置

## **总结**

本章描述了 PCIe 设备中事务路由的基本机制。BAR 和 Base/Limit 寄存器一起允许系统正确路由事务。ID 路由用于配置和完成，而地址路由用于内存和 IO 请求。隐式路由允许消息传达传统信号事件而无需定义地址或 ID 范围。下一章将详细描述事务层包 (TLP) 的内容。

**192**

**第 4 章：地址空间与事务路由**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-7"></a>
## 5.7 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

CPU Type 0 Header<br>31 23 15 7 0<br>Device ID Vendor ID 00h<br>Root Complex System Status Command 04h<br>Memory<br>P2P (DRAM) Class Code Line SizeCache 08h<br>BIST Header Latency Cache 0Ch<br>TLP Type Timer Line Size<br>(Addr) Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h<br>P2P<br>Base Address 2 (BAR2) 18h<br>Switch Packet for me? Base Address 3 (BAR3) 1Ch<br>Base Address 4 (BAR4) 20h<br>TLP { Base Address 5 (BAR5) 24h<br>(Addr) CardBus CIS Pointer 28h<br>PCIe PCIe SubsystemDevice ID SubsystemVendor ID 2Ch<br>Endpoint Endpoint Expansion ROM Base Address 30h<br>Reserved Capability 34h<br>TLP Address field Pointer<br>should match a BAR Reserved 38h<br>within a PCIe Function Max Lat Min Gnt InterruptPin InterruptLine 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Switch Routing** 

If an incoming TLP uses address routing, a Switch Port first checks to see if the address is local within the Port itself by comparing the address in the packet header against its two BARs in its Type 1 configuration header, as shown in Step 1 of Figure 4‐21 on page 162. If it matches one of these BARs, the switch port is the target of the TLP and consumes the packet. If not, the port then checks its Base/Limit register pairs to see if the TLP is targeting a function beneath (downstream of) this bridge. If the Request targets IO space, it will check the IO Base and Limit registers, as shown in Step 2a. However, if the Request targets memory space, it will check the Non‐ prefetchable Memory Base/ Limit registers and the Prefetchable Memory Base/Limit registers, as indicated by Step 2b in Figure 4‐21 on page 162. More info on how the Base/Limit register pairs are evaluated can be found in section “Base and Limit Registers” on page 136. 

**161** 

**PCI Express Technology** 

_Figure 4‐21: Switch Checks Routing Of An Inbound TLP Using Address_ 

**==> picture [349 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>CPU 31 23 15 7 0<br>Device ID Vendor ID 00h<br>__ es<br>Status Command 04h<br>Root Complex MemorySystem Class Code Line SizeCache 08h<br>P2P - (DRAM) [—_] e BIST HeaderType s e LatencyTimer Line Size ee Cache 0Ch<br>Base Address 0 (BAR0) 10h<br>TLP<br>1. Packet for me?<br>(Addr) Base Address 1 (BAR1) 14h<br>Secondary Subordinate Secondary Primary 18h<br>P2P Lat Timer Bus # Bus # Bus #<br>2a. IO Packet for some- SecondaryStatus LimitIO BaseIO 1Ch<br>Switch       one beneath me? | (Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>— —— 2b. Mem Packet for some- _— Prefetchable Prefetchable 24h<br>Memory Limit Memory Base<br>      one beneath me? Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>PCIe PCIe IO Limit IO Base<br>Upper 16 Bits Upper 16 Bits 30h<br>7 7 ee<br>Endpoint Endpoint Reserved Capability 34h<br>es Pointer<br>Expansion ROM Base Address 38h<br>— ae<br>ee ControlBridge InterruptPin Interrupt ee Line 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


To understand routing of address‐based TLPs in switches, it is good to remember that each switch port is its own bridge. Below are the steps that a bridge (switch port) takes upon receiving an address‐based TLP: 

## **Downstream Traveling TLPs (Received on Primary Interface)** 

1. IF the target address in the TLP matches one of the BARs, then this bridge (switch port) consumes the TLP because it is the target of the TLP. 

2. IF the target address in the TLP falls in the range of one of its Base/ Limit register sets, the packet will be forwarded to the secondary inter‐ face (downstream). 

3. ELSE the TLP will be handled as an Unsupported Request on the pri‐ mary interface. (This is true if no other bridges on the primary interface claim the TLP either.) 

**162** 

**Chapter 4: Address Space & Transaction Routing** 

## **Upstream Traveling TLPs (Received on Secondary Interface)** 

1. IF the target address in the TLP matches one of the BARs, then this bridge (switch port) consumes the TLP because it is the target of the TLP. 

2. IF the target address in the TLP falls in the range of one of its Base/ Limit register sets, the TLP will be handled as an Unsupported Request on the secondary interface. (This is true unless this port is the upstream port of the switch. In these cases, the packet may be a peer‐to‐peer transaction and will be forwarded downstream on a different down‐ stream port than the one it was received on.) 

3. ELSE the TLP will be forwarded to the primary interface (upstream) given that the TLP address is not for this bridge and is not for any func‐ tion beneath this bridge. 

## **Multicast Capabilities** 

The 2.1 version of the PCI Express specification added support for specifying a range of addresses that provide multicast functionality. Any packets received that fall within the address range specified as the multicast range are routed/ accepted according to the multicast rules. This address range might not be reserved in a function’s BARs and might not be within a bridge’s Base/Limit reg‐ ister pair, but would still need to be accepted/forwarded appropriately. More info can be found on the multicast functionality in the section on “Multicast Capability Registers” on page 889. 

## **Implicit Routing** 

Implicit routing, used in some message packets, is based on the awareness of routing elements that the topology has upstream and downstream directions and a single Root Complex at the top. This allows some simple routing methods without the need to assign a target address or ID. Since the Root Complex gen‐ erally integrates power management, interrupt, and error handling logic, it is either the source or recipient of most PCI Express messages. 

## **Only for Messages** 

Some messages use address or ID routing rather than implicit routing, and for them, the routing mechanisms are applied in the same way as described in the those sections. However, most messages use implicit routing. The purpose of implicit routing is to mimic side‐band signal behavior since a design goal for PCIe was to eliminate as many side‐band signals from PCI as possible. These 

**163** 

**PCI Express Technology** 

side‐band signals in PCI were typically either the host notifying all devices of an event or devices notifying the host of an event. In PCIe, we have Message TLPs to convey these events. The types of events that PCIe has defined messages for are: 

- Power Management 

- INTx legacy interrupt signaling 

- Error signaling 

- Locked Transaction support 

- Hot Plug signaling 

- Vendor‐specific signaling 

- Slot Power Limit settings 

## **Key TLP Header Fields in Implicit Routing** 

For implicit routing, the routing sub‐field in the header is used to determine the message destination. Figure 4‐22 on page 164 illustrates a message TLP using implicit routing. 

_Figure 4‐22: 4DW Message TLP Header ‐ Implicit Routing Fields_ 

**==> picture [355 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
4DW Header for Messages<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R TH T E Attr AT Length<br>0 x 1 1  0  r  r  r tr 0 D P 0 0 0 0<br>Message<br>Byte 4 Requester ID Tag<br>Code<br>Byte 8 Bytes 8-11 Vary with  Message Code  Field<br>Byte 12 Bytes 12-15 Vary with  Message Code  Field<br>**----- End of picture text -----**<br>


## **Message Type Field Summary** 

Table 4‐10 on page 165 shows how the TLP header Type field for Messages is interpreted. As shown, the upper two bits indicate the packet is a Message while the lower three bits specify the routing method to apply. Note that Mes‐ sage TLPs always use a 4DW header regardless of the routing option selected. 

**164** 

**Chapter 4: Address Space & Transaction Routing** 

For address routing, bytes 8‐15 contain up to a 64‐bit address, and for ID rout‐ ing, bytes 8 and 9 contain the target BDF. 

_Table 4‐10: Message Request Header Type Field Usage_ 

|**Type Field Bits**|**Description**|
|---|---|
|Bit 4:3|Defines the type of transaction:<br>10b = Message TLP|
|Bit 2:0|Message Routing Subfield R[2:0]<br>• 000b = Implicit ‐ Route to the Root Complex<br>• 001b = Route by Address (bytes 8‐15 of header contain address)<br>• 010b = Route by ID (bytes 8‐9 of header contain ID)<br>• 011b = Implicit ‐ Broadcast downstream<br>• 100b = Implicit ‐ Local: terminate at receiver<br>• 101b = Implicit ‐ Gather & route to the Root Complex<br>• 110b ‐ 111b = Reserved: terminate at receiver|



## **Endpoint Handling** 

For implicit routing, an Endpoint simply checks whether the routing sub‐field is appropriate for it. For example, an Endpoint will accept a Broadcast Message or a Message that terminates at the receiver; but not Messages that implicitly target the Root Complex. 

## **Switch Handling** 

Routing elements like Switches consider the port on which the TLP arrived on and whether the routing sub‐field code is appropriate for it. For example: 

1. A Switch Upstream Port may legitimately receive a Broadcast Message. It will duplicate that and forward it to all its Downstream Ports. An implicitly routed Broadcast Message received on a Downstream Port of a Switch (meaning the message was traveling upstream) would be an error that would be handled as a Malformed TLP. 

2. A Switch may receive implicitly routed Messages for the Root Complex on Downstream Ports and will forward these to its Upstream Port because the location of the Root Complex is understood to be upstream. It would not accept Messages received on its Upstream Port (meaning the message was traveling downstream) that are implicitly routed to the Root Complex. 

**165** 

## **PCI Express Technology** 

3. If an implicitly routed Message indicates it should terminate at the receiver, then the receiving switch port will consume the message rather than for‐ ward it. 

4. For messages routed using address or ID routing, a Switch will simply per‐ form normal address or ID checks in deciding whether to accept or forward it. 

## **DLLPs and Ordered Sets Are Not Routed** 

DLLP and Ordered Set traffic is not routed from ingress ports to egress ports of switches or root complexes. These packets move from port to port across a link from Physical Layer to Physical Layer. 

DLLPs originate at the Data Link Layer of a PCI Express port, pass through the Physical Layer, exit the port, traverse the Link and arrive at the neighboring port. At this port, the packet passes through the Physical Layer and ends up at the Data Link Layer where it is processed and consumed. DLLPs do not pro‐ ceed further up the port to the Transaction Layer and hence are not routed. 

Similarly, Ordered‐Set packets originate at the Physical Layer, exit the port, traverse the Link and arrive at the neighboring port. At this port, the packet arrives at the Physical Layer where it is processed and consumed. Ordered‐Sets do not proceed further up the port to the Data Link Layer and Transaction Layer and hence are not routed. 

As has been discussed in this chapter, only TLPs are routed through switches and root complexes. The originate at the Transaction Layer of a source port and end up at the Transaction Layer of a destination port. 

**166** 

## Part Two: 

# Transaction Layer 

## _**5**_ 

## _**TLP Elements**_ 

## **The Previous Chapter** 

The previous chapter describes the purpose and methods of a function request‐ ing address space (either memory address space or IO address space) through Base Address Registers (BARs) and how software must setup the Base/Limit registers in all bridges to route TLPs from a source port to the correct destina‐ tion port. The general concepts of TLP routing in PCI Express are also dis‐ cussed, including address‐based routing, ID‐based routing and implicit routing. 

## **This Chapter**

</td>
<td style="background-color:#e8e8e8">

## **完成头格式**

完成 TLP 是从完成者返回到请求者的 TLP，以响应该请求者发出的非发布事务。完成使用 3DW 或 4DW 头，取决于它们是否携带数据（带数据的完成使用 4DW 头）。完成头格式在第 190 页图 4-23 中显示。

_图 4-23：3DW 和 4DW 完成头格式_

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 完成者 ID Cmpl CB 字节数<br>
状态 M<br>
字节 8 请求者 ID 标签 R 低地址<br>**----- End of picture text -----**<br>


## **完成头字段**

完成头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：完成格式

  - 000b = 3DW 完成（无数据）

  - 010b = 3DW 带数据完成（带数据）

- **Type [4:0]**（字节 0 位 4:0）：完成类型

  - 01010b = 完成 (Cpl) 或带数据完成 (CplD)

- **TC [2:0]**（字节 1 位 6:4）：流量类。完成使用与请求相同的 TC。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序（IDO）。完成使用与请求相同的设置。

- **TD**（字节 2 位 7）：TLP 摘要。如果请求的 TD = 1，则完成包含摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。如果完成者检测到数据中的错误，则将 EP 位置位。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。完成使用与请求相同的设置。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。完成使用与请求相同的设置。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：完成数据有效负载的大小（以 DW 为单位）。对于 Cpl，此字段保留。

- **完成者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：完成者的 BDF。这标识哪个设备生成了完成。

- **完成状态 [2:0]**（字节 5 位 2:0）：指示完成状态。状态值包括：

  - 000b = 成功完成 (SC)

  - 001b = 不支持的请求 (UR)

  - 010b = 配置请求重试状态 (CRS) - 仅对配置请求有效

  - 100b = 完成者中止 (CA)

- **BCM**（字节 5 位 3）：字节计数修改。指示字节计数字段是否已被修改。

- **字节计数 [11:0]**（字节 6 位 7:0，字节 7 位 7:4）：完成者返回的剩余字节数。

- **请求者 ID [15:0]**（字节 8 位 7:0，字节 9 位 7:0）：完成应路由到的请求者的 BDF。

- **标签 [7:0]**（字节 10 位 7:0）：来自对应请求的标签字段。

- **低地址 [6:0]**（字节 11 位 6:0）：对于读完成，这是返回数据中第一个启用字节的地址的低位。

**190**

**第 4 章：地址空间与事务路由**

## **完成路由**

完成始终使用 ID 路由。它们被路由回完成包中 Requester ID 字段中标识的请求者。请求者 ID 在完成包头中（字节 4-5），与请求 TLP 中的位置相同。

## **完成拆分**

PCI Express 规范允许完成者将单个大型读请求拆分为多个完成 TLP。这对于返回跨 4KB 或更大边界的请求的数据很有用。完成者可以通过将多个完成 TLP 排队到同一请求者来拆分完成。这些拆分完成共享相同的 Requester ID 和 Tag 字段，但每个完成都包含返回数据的不同部分。

拆分完成时，必须遵循以下规则：

- 每个完成 TLP 必须以自然对齐的地址边界结束（对于 Root Complex 为 64 或 128 字节，对于其他设备为 128 字节）。此边界由读完成边界 (RCB) 配置位控制。

- 第一个拆分完成返回请求的最低地址部分。

- 后续完成返回连续地址部分。

- 最后一个完成的数据长度可能小于其他完成。

- 所有拆分完成必须使用相同的 Requester ID、Tag 和 TC。

## **完成错误处理**

完成 TLP 头中的状态字段指示事务是成功还是遇到错误。常见错误状态包括：

- **UR（不支持的请求）**：请求针对的设备无法处理该类型的请求。设备可能不存在或不支持该请求类型。

- **CA（完成者中止）**：完成者检测到错误条件并中止事务。

- **CRS（配置请求重试状态）**：仅对配置请求有效。表示设备暂时无法响应，请求者应重试。

## **消息请求**

消息 TLP 是 PCIe 中引入的新概念。它们用于传达传统上需要单独信号的事件。消息始终使用 4DW 头。

## **消息头格式**

图 4-24（第 191 页）显示了消息 TLP 头格式。

_图 4-24：消息 TLP 头格式_

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 请求者 ID 标签 消息代码<br>
字节 8 字节 8-11 随消息代码而变化<br>
字节 12 字节 12-15 随消息代码而变化<br>**----- End of picture text -----**<br>


## **消息头字段**

消息头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：消息格式

  - 001b = 4DW 消息（无数据）

  - 011b = 4DW 消息（带数据）

- **Type [4:0]**（字节 0 位 4:0）：消息类型

  - 位 4:3 = 10b（消息）

  - 位 2:0 = 路由子字段

- **TC [2:0]**（字节 1 位 6:4）：流量类。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序。

- **TH**（字节 1 位 0）：TLP 处理提示。

- **TD**（字节 2 位 7）：TLP 摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：消息数据有效负载大小（如果存在）。

- **请求者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：发起消息的设备的 BDF。

- **标签 [7:0]**（字节 6 位 7:0）：消息标签。

- **消息代码 [7:0]**（字节 7 位 7:0）：定义消息类型的代码。

- **字节 8-15**：随消息代码字段而变化。

**191**

**第 4 章：地址空间与事务路由**

## **消息路由**

消息 TLP 可以使用三种路由方法之一：地址路由、ID 路由或隐式路由。消息头 Type 字段的位 2:0（路由子字段）确定使用哪种路由方法：

- 000b = 隐式 - 路由到根复合体

- 001b = 按地址路由（头字节 8-15 包含地址）

- 010b = 按 ID 路由（头字节 8-9 包含 ID）

- 011b = 隐式 - 向下游广播

- 100b = 隐式 - 本地：在接收方终止

- 101b = 隐式 - 收集并路由到根复合体

- 110b - 111b = 保留

## **消息代码**

PCI Express 规范定义了多个消息代码。这些代码分为几类：

- **电源管理消息**：用于电源管理事件

- **INTx 中断消息**：传统中断信令

- **错误消息**：错误信令

- **锁定事务消息**：锁定事务支持

- **热插拔消息**：热插拔信令

- **供应商定义消息**：供应商特定消息

- **插槽功率限制消息**：插槽功率限制设置

## **总结**

本章描述了 PCIe 设备中事务路由的基本机制。BAR 和 Base/Limit 寄存器一起允许系统正确路由事务。ID 路由用于配置和完成，而地址路由用于内存和 IO 请求。隐式路由允许消息传达传统信号事件而无需定义地址或 ID 范围。下一章将详细描述事务层包 (TLP) 的内容。

**192**

**第 4 章：地址空间与事务路由**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-8"></a>
## 5.8 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Information moves between PCI Express devices in packets. The three major classes of packets are _Transaction Layer Packets_ (TLPs), _Data Link Layer Packets_ (DLLPs) and _Ordered Sets_ . This chapter describes the use, format, and definition of the variety of TLPs and the details of their related fields. DLLPs are described separately in Chapter 9, entitled ʺDLLP Elements,ʺ on page 307. 

## **The Next Chapter** 

The next chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Transaction Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like disconnects, retries, and wait‐states. 

## **Introduction to Packet-Based Protocol** 

## **General** 

Unlike parallel buses, serial transport buses like PCIe use no control signals to identify what’s happening on the Link at a given time. Instead, the bit stream they send must have an expected size and a recognizable format to make it pos‐ 

**169** 

**PCI Ex ress Technolo p gy** 

sible for the receiver to understand the content. In addition, PCIe does not use any immediate handshake for the packet while it is being transmitted. 

With the exception of the Logical Idle symbols and Physical Layer packets called _Ordered Sets_ , information moves across an active PCIe Link in fundamen‐ tal chunks called packets that are comprised of symbols. The two major classes of packets exchanged are the high‐level _Transaction Layer Packets_ (TLPs), and low‐level Link maintenance packets called _Data Link Layer Packets_ (DLLPs). The packets and their flow are illustrated in Figure 5‐1 on page 170. Ordered Sets are packets too, however, they are not framed with a start and end symbol like TLPs and DLLPs are. They are also not byte striped like TLPs and DLLPs are. Ordered Set packets are instead replicated on all Lanes of a Link. 

_Figure 5‐1: TLP And DLLP Packets_ 

**==> picture [350 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>DLLP TLP<br>DLLP TLP (Link)<br>Transaction Layer Packet (TLP)<br>STP Seq Num HDR Data Digest CRC End TLP Types:<br>- Memory Read / Write<br>- IO Read / Write<br>- Configuration Read / Write<br>- Completion<br>- Message<br>Data Link Layer Packet (DLLP)<br>- AtomicOp<br>Framing C Framing DLLP Types:<br>DLLP R - TLP Ack/Nak<br>(SDP) C (END)<br>- Power Management<br>- Link Flow Control<br>- Vendor-Specific<br>**----- End of picture text -----**<br>


**170** 

**Chapter 5: TLP Elements** 

## **Motivation for a Packet-Based Protocol** 

There are three distinct advantages to using a packet‐based protocol especially when it comes to data integrity: 

## **1. Packet Formats Are Well Defined** 

Earlier buses like PCI allow transfers of indeterminate size, making identifica‐ tion of payload boundaries impossible until the end of the transfer. In addition, either device is able to terminate the transfer before it completes, making it diffi‐ cult for the sender to calculate and send a checksum or CRC covering an entire payload. Instead, PCI uses a simple parity scheme and checks it on each data phase. 

By comparison, PCIe packets have a known size and format. The packet _header_ at the beginning indicates the packet type and contains the required and optional fields. The size of the header fields is fixed except for the address, which can be 32 bits or 64 bits in size. Once a transfer commences, the recipient can’t pause or terminate it early. This structured format allows including infor‐ mation in the TLPs to aid in reliable delivery, including framing symbols, CRC, and a packet Sequence Number. 

## **2. Framing Symbols Define Packet Boundaries** 

When using 8b/10b encoding in Gen1 and Gen2 mode of operation, each TLP and DLLP packet sent is framed by Start and End control symbols, clearly defining the packet boundaries for the receiver. This is a big improvement over PCI and PCI‐X, where the assertion and de‐assertion of the single FRAME# sig‐ nal indicates the beginning and end of a transaction. A glitch on that signal (or any of the other control signals) could cause a target to misconstrue bus events. A PCIe receiver must properly decode a complete 10‐bit symbol before conclud‐ ing Link activity is beginning or ending, so unexpected or unrecognized sym‐ bols are more easily recognized and handled as errors. 

For the 128b/130b encoding used in Gen3, control characters are no longer employed and there are no framing symbols as such. For more on the differ‐ ences between Gen3 encoding and the earlier versions, see Chapter 12, entitled ʺPhysical Layer ‐ Logical (Gen3),ʺ on page 407. 

**171** 

**PCI Ex ress Technolo p gy** 

## **3. CRC Protects Entire Packet** 

Unlike the side‐band parity signals used by PCI during the address and data phases of a transaction, the in‐band CRC value of PCIe verifies error‐free deliv‐ ery of the entire packet. TLP packets also have a Sequence Number appended to them by the transmitter’s Data Link Layer so that if an error is detected at the Receiver, the problem packet can be automatically resent. The transmitter main‐ tains a copy of each TLP sent in a _Retry Buffer_ until it has been acknowledged by the receiver. This TLP acknowledgement mechanism, called the _Ack/Nak Proto‐ col_ , (and described in Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317) forms the basis of Link‐level TLP error detection and correction. This Ack/Nak Protocol error recovery mechanism allows for a timely resolution of the prob‐ lem at the place or Link where the problem occurred, but requires a local hard‐ ware solution to support it. 

## **Transaction Layer Packet (TLP) Details** 

In PCI Express, high‐level transactions originate in the device core of the trans‐ mitting device and terminate at the core of the receiving device. The Transaction Layer acts on these requests to assemble outbound TLPs in the Transmitter and interpret them at the Receiver. Along the way, the Data Link Layer and Physical Layer of each device also contribute to the final packet assembly. 

## **TLP Assembly And Disassembly** 

The general flow of TLP assembly at the transmit side of a Link and disassem‐ bly at the receiver is shown in Figure 5‐2 on page 173. Let’s now walk through the steps from creation of a packet to its delivery to the core logic of the receiver. The key stages in Transaction Layer Packet assembly and disassembly are listed below. The list numbers correspond to the numbers in Figure 5‐2 on page 173. 

## **Transmitter:** 

1. The core logic of Device A sends a request to its PCIe interface. How this is accomplished is outside the scope of the spec or this book. The request includes: 

   - Target address or ID (routing information) 

   - Source information such as Requester ID and Tag 

   - Transaction type/packet type (Command to perform, such as a memory read.) 

   - Data payload size (if any) along with data payload (if any) 

   - Traffic Class (to assign packet priority) 

   - Attributes of the Request (No Snoop, Relaxed Ordering, etc.) 

**172** 

**Chapter 5: TLP Elements** 

2. Based on that request, the Transaction Layer builds the TLP header, appends any data payload, and optionally calculates and appends the digest (End‐to‐End CRC, ECRC) if that’s supported and has been enabled. At this point the TLP is placed into a Virtual Channel buffer. The Virtual Channel manages the sequence of TLPs according to the Transaction Order‐ ing rules and also verifies that the receiver has enough flow control credits to accept a TLP before it can be passed down to the Data Link Layer. 

3. When it arrives at the Data Link Layer, the TLP is assigned a Sequence Number and then a Link CRC is calculated based on the contents of the TLP and that Sequence Number. A copy of the resulting packet is saved in the Retry Buffer in case of transmission errors while it is also passed on to the Physical Layer. 

_Figure 5‐2: PCIe TLP Assembly/Disassembly_ 

**==> picture [370 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) Outbound From Transmitter Core: Device A Device B (8) Inbound To Receiver Core:<br>Requests to write/read data, Data R/W Requests,<br>Completions, Messages, etc. Device Device Completions, Messages, etc.<br>Core Core<br>(2) Transaction Transaction (7)<br>HDR Data Digest  Layer  Layer HDR Data Digest<br>(3) (3) Data Data (6) (6)<br>Seq Num HDR Data Digest CRC Link Layer Link Layer Seq Num HDR Data Digest CRC<br>STP(4) Seq Num HDR Data Digest CRC End(4) PhysicalLayer PhysicalLayer STP(5) Seq Num HDR Data Digest CRC End(5)<br>(RX) (TX) (RX) (TX)<br>**----- End of picture text -----**<br>


4. The Physical Layer does several things to prepare the packet for serial transmission, including byte striping, scrambling, encoding, and serializing the bits. For Gen1 and Gen2 devices, when using 8b/10b encoding, the con‐ trol characters STP and END are added to either end of the packet. Finally, the packet is transmitted across the Link. In Gen3 mode, STP token is added to the front end of a TLP, but END is not added to the end of the packet. Rather the STP token contains information about TLP packet size. 

## **Receiver:** 

5. At the Receiver (Device B in this example), everything done to prepare the packet for transmission must now be undone. The Physical Layer de‐serial‐ izes the bit stream, decodes the resulting symbols, and un‐stripes the bytes. 

**173** 

**PCI Ex ress Technolo p gy** 

   - The control characters are removed here because they only have meaning at the Physical Layer, and then the packet is forwarded to the Data Link Layer. 

6. The Data Link Layer calculates the CRC and compares it to the received CRC. If that matches, the Sequence Number is checked. If there are no errors, the CRC and Sequence Number are removed and the TLP is passed to the Transaction Layer of the receiver and notifies the sender of good reception by returning an Ack DLLP. In the event of an error a Nak will be returned instead, and the transmitter will re‐replay TLPs in its Retry Buffer. 

7. At the Transaction Layer, the TLP is decoded and the information is passed to the core logic for appropriate action. If the receiving device is the final target of this packet, it checks for ECRC errors and reports any related ECRC error condition to the core logic should there be any. 

## **TLP Structure** 

The basic usage of each field in a Transaction Layer Packet is defined in Table 5‐ 1 on page 174. 

_Table 5‐1: TLP Header Type Field Defines Transaction Variant_ 

|**TLP**<br>**Component**|**Protocol**<br>**Layer**|**Component Use**|
|---|---|---|
|Header|Transaction<br>Layer|3 or 4DW (12 or 16 bytes) in size. Format varies with<br>type, but Header defines parameters, including:<br>•<br>Transaction type<br>•<br>Target address, ID, etc.<br>•<br>Transfer size (if any), Byte Enables<br>•<br>Attributes<br>•<br>Traffic Class|
|Data|Transaction<br>Layer|Optional 1‐1024 DW Payload, which is qualified<br>with Byte Enables or byte‐aligned start and end<br>addresses. Note that a length of zero can’t be speci‐<br>fied, but a zero‐length read (useful in some cases)<br>can be approximated by specifying a length of 1 DW<br>and Byte Enables of all zero. The resulting data from<br>the Completer will be undefined but the Requester<br>doesn’t use it, so the result is the same.|
|Digest/ECRC|Transaction<br>Layer|Optional. When present, ECRC is always 1 DW in<br>size.|



**174** 

**Chapter 5: TLP Elements** 

## **Generic TLP Header Format** 

## **General**

</td>
<td style="background-color:#e8e8e8">

## **完成头格式**

完成 TLP 是从完成者返回到请求者的 TLP，以响应该请求者发出的非发布事务。完成使用 3DW 或 4DW 头，取决于它们是否携带数据（带数据的完成使用 4DW 头）。完成头格式在第 190 页图 4-23 中显示。

_图 4-23：3DW 和 4DW 完成头格式_

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 完成者 ID Cmpl CB 字节数<br>
状态 M<br>
字节 8 请求者 ID 标签 R 低地址<br>**----- End of picture text -----**<br>


## **完成头字段**

完成头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：完成格式

  - 000b = 3DW 完成（无数据）

  - 010b = 3DW 带数据完成（带数据）

- **Type [4:0]**（字节 0 位 4:0）：完成类型

  - 01010b = 完成 (Cpl) 或带数据完成 (CplD)

- **TC [2:0]**（字节 1 位 6:4）：流量类。完成使用与请求相同的 TC。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序（IDO）。完成使用与请求相同的设置。

- **TD**（字节 2 位 7）：TLP 摘要。如果请求的 TD = 1，则完成包含摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。如果完成者检测到数据中的错误，则将 EP 位置位。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。完成使用与请求相同的设置。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。完成使用与请求相同的设置。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：完成数据有效负载的大小（以 DW 为单位）。对于 Cpl，此字段保留。

- **完成者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：完成者的 BDF。这标识哪个设备生成了完成。

- **完成状态 [2:0]**（字节 5 位 2:0）：指示完成状态。状态值包括：

  - 000b = 成功完成 (SC)

  - 001b = 不支持的请求 (UR)

  - 010b = 配置请求重试状态 (CRS) - 仅对配置请求有效

  - 100b = 完成者中止 (CA)

- **BCM**（字节 5 位 3）：字节计数修改。指示字节计数字段是否已被修改。

- **字节计数 [11:0]**（字节 6 位 7:0，字节 7 位 7:4）：完成者返回的剩余字节数。

- **请求者 ID [15:0]**（字节 8 位 7:0，字节 9 位 7:0）：完成应路由到的请求者的 BDF。

- **标签 [7:0]**（字节 10 位 7:0）：来自对应请求的标签字段。

- **低地址 [6:0]**（字节 11 位 6:0）：对于读完成，这是返回数据中第一个启用字节的地址的低位。

**190**

**第 4 章：地址空间与事务路由**

## **完成路由**

完成始终使用 ID 路由。它们被路由回完成包中 Requester ID 字段中标识的请求者。请求者 ID 在完成包头中（字节 4-5），与请求 TLP 中的位置相同。

## **完成拆分**

PCI Express 规范允许完成者将单个大型读请求拆分为多个完成 TLP。这对于返回跨 4KB 或更大边界的请求的数据很有用。完成者可以通过将多个完成 TLP 排队到同一请求者来拆分完成。这些拆分完成共享相同的 Requester ID 和 Tag 字段，但每个完成都包含返回数据的不同部分。

拆分完成时，必须遵循以下规则：

- 每个完成 TLP 必须以自然对齐的地址边界结束（对于 Root Complex 为 64 或 128 字节，对于其他设备为 128 字节）。此边界由读完成边界 (RCB) 配置位控制。

- 第一个拆分完成返回请求的最低地址部分。

- 后续完成返回连续地址部分。

- 最后一个完成的数据长度可能小于其他完成。

- 所有拆分完成必须使用相同的 Requester ID、Tag 和 TC。

## **完成错误处理**

完成 TLP 头中的状态字段指示事务是成功还是遇到错误。常见错误状态包括：

- **UR（不支持的请求）**：请求针对的设备无法处理该类型的请求。设备可能不存在或不支持该请求类型。

- **CA（完成者中止）**：完成者检测到错误条件并中止事务。

- **CRS（配置请求重试状态）**：仅对配置请求有效。表示设备暂时无法响应，请求者应重试。

## **消息请求**

消息 TLP 是 PCIe 中引入的新概念。它们用于传达传统上需要单独信号的事件。消息始终使用 4DW 头。

## **消息头格式**

图 4-24（第 191 页）显示了消息 TLP 头格式。

_图 4-24：消息 TLP 头格式_

**==> picture [302 x 65] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
字节 4 请求者 ID 标签 消息代码<br>
字节 8 字节 8-11 随消息代码而变化<br>
字节 12 字节 12-15 随消息代码而变化<br>**----- End of picture text -----**<br>


## **消息头字段**

消息头中的字段及其用途如下：

- **Fmt [2:0]**（字节 0 位 7:5）：消息格式

  - 001b = 4DW 消息（无数据）

  - 011b = 4DW 消息（带数据）

- **Type [4:0]**（字节 0 位 4:0）：消息类型

  - 位 4:3 = 10b（消息）

  - 位 2:0 = 路由子字段

- **TC [2:0]**（字节 1 位 6:4）：流量类。

- **Attr [2]**（字节 1 位 2）：基于 ID 的排序。

- **TH**（字节 1 位 0）：TLP 处理提示。

- **TD**（字节 2 位 7）：TLP 摘要。

- **EP**（字节 2 位 6）：错误/Poisoned 数据。

- **Attr [1:0]**（字节 2 位 5:4）：宽松排序和无窥探。

- **AT [1:0]**（字节 2 位 3:2）：地址类型。

- **长度 [9:0]**（字节 2 位 1:0，字节 3 位 7:0）：消息数据有效负载大小（如果存在）。

- **请求者 ID [15:0]**（字节 4 位 7:0，字节 5 位 7:0）：发起消息的设备的 BDF。

- **标签 [7:0]**（字节 6 位 7:0）：消息标签。

- **消息代码 [7:0]**（字节 7 位 7:0）：定义消息类型的代码。

- **字节 8-15**：随消息代码字段而变化。

**191**

**第 4 章：地址空间与事务路由**

## **消息路由**

消息 TLP 可以使用三种路由方法之一：地址路由、ID 路由或隐式路由。消息头 Type 字段的位 2:0（路由子字段）确定使用哪种路由方法：

- 000b = 隐式 - 路由到根复合体

- 001b = 按地址路由（头字节 8-15 包含地址）

- 010b = 按 ID 路由（头字节 8-9 包含 ID）

- 011b = 隐式 - 向下游广播

- 100b = 隐式 - 本地：在接收方终止

- 101b = 隐式 - 收集并路由到根复合体

- 110b - 111b = 保留

## **消息代码**

PCI Express 规范定义了多个消息代码。这些代码分为几类：

- **电源管理消息**：用于电源管理事件

- **INTx 中断消息**：传统中断信令

- **错误消息**：错误信令

- **锁定事务消息**：锁定事务支持

- **热插拔消息**：热插拔信令

- **供应商定义消息**：供应商特定消息

- **插槽功率限制消息**：插槽功率限制设置

## **总结**

本章描述了 PCIe 设备中事务路由的基本机制。BAR 和 Base/Limit 寄存器一起允许系统正确路由事务。ID 路由用于配置和完成，而地址路由用于内存和 IO 请求。隐式路由允许消息传达传统信号事件而无需定义地址或 ID 范围。下一章将详细描述事务层包 (TLP) 的内容。

**192**

**第 4 章：地址空间与事务路由**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-9"></a>
## 5.9 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Figure 5‐3 on page 175 illustrates the format and contents of a generic TLP 4DW header. In this section, fields common to nearly all transactions are summa‐ rized. Header format differences associated with specific transaction types are covered later. 

_Figure 5‐3: Generic TLP Header Fields_ 

**==> picture [328 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Framing Sequence Framing<br>Header Data Digest LCRC<br>(STP) Number (End)<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Bytes 4-7 vary with Type BE BE<br>Byte 8 Bytes 8-11 vary with Type<br>Byte 12 Bytes 12-15 vary with Type (not always required)<br>**----- End of picture text -----**<br>


## **Generic Header Field Summary** 

Table 5‐2 on page 176 summarizes the size and use of each of the generic TLP header fields. Note that fields marked “R” in Figure 5‐3 on page 175 are reserved and should be set to zero. 

**175** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐2: Generic Header Field Summary_ 

|**Header**<br>**Field**|**Header**<br>**Location**|**Field Use**|
|---|---|---|
|Fmt[2:0]<br>(Format)|Byte 0 Bit 7:5|These bits encode information about header size and<br>whether a data payload will be part of the TLP:<br>00b 3DW header, no data<br>01b 4DW header, no data<br>10b 3DW header, with data<br>11b 4DW header, with data<br>An address below 4GB must use a 3DW header. The<br>spec states that receiver behavior is undefined if<br>4DW header is used for an address below 4GB with<br>the upper 32 bits of the 64‐bit address set to zero.|
|Type[4:0]|Byte 0 Bit 4:0|These bits encode the transaction variant used with<br>this TLP. The Type field is used with Fmt [1:0] field<br>to specify transaction type, header size, and whether<br>data payload is present. See “Generic Header Field<br>Details” on page 178 for details.|
|TC [2:0]<br>(Traffic<br>Class)|Byte 1 Bit 6:4|These bits encode the traffic class to be applied to<br>this TLP and to the completion associated with it (if<br>any):<br>000b = Traffic Class 0 (Default)<br>.<br>.<br>111b = Traffic Class 7<br>TC 0 is the default class, while TC 1‐7 are used to<br>provide differentiated services. See “Traffic Class<br>(TC)” on page 247 for additional information.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|This third Attribute bit indicates whether ID‐based<br>Ordering is to be used for this TLP. To learn more,<br>see “ID Based Ordering (IDO)” on page 301.|
|TH<br>(TLP Pro‐<br>cessing<br>Hints)|Byte 1 Bit 0|Indicates when TLP Hints have been included to<br>give the system some idea about how best to handle<br>this TLP. See “TPH (TLP Processing Hints)” on<br>page 899 for a discussion on their usage.|



**176** 

**Chapter 5: TLP Elements** 

_Table 5‐2: Generic Header Field Summary (Continued)_ 

|**Header**<br>**Field**|**Header**<br>**Location**||**Field Use**|
|---|---|---|---|
|TD<br>(TLP Digest)|Byte 2 Bit 7||If TD = 1, the optional 4‐byte TLP Digest has been<br>included with this TLP as the ECRC value.<br>Some rules<br>:<br>• Presence of the Digest field must be checked by all<br>receivers based on this bit.<br>• A TLP with TD = 1 but no Digest is handled as a<br>Malformed TLP.<br>• If a device supports checking ECRC and TD=1, it<br>must perform the ECRC check.<br>• If a device does not support checking ECRC<br>(optional) at the ultimate destination, it must<br>ignore the digest.<br>For more on this topic see “CRC” on page 653 and<br>“ECRC Generation and Checking” on page 657.|
|EP<br>(Poisoned<br>Data)|Byte 2 Bit 6||If EP = 1, the data accompanying this data should be<br>considered invalid although the transaction is being<br>allowed to complete normally. For more on poisoned<br>packets, refer to “Data Poisoning” on page 660.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4||Bit 5=Relaxed ordering<br>:When set to 1, PCI‐X<br>relaxed ordering is enabled for this TLP. If 0, then<br>strict PCI ordering is used.<br>Bit 4=No Snoop:<br>When set to 1, Requester is indicat‐<br>ing that no host cache coherency issues exist for this<br>TLP. System hardware can thus save time by skip‐<br>ping the normal processor cache snoop for this<br>request. When 0, PCI ‐type cache snoop protection is<br>required.|



**177** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐2: Generic Header Field Summary (Continued)_ 

|**Header**<br>**Field**|**Header**<br>**Location**|**Field Use**|
|---|---|---|
|Address<br>Type [1:0]|Byte 2 Bit 3:2|For Memory and Atomic Requests, this field sup‐<br>ports address translation for virtualized systems.<br>The translation protocol is described in a separate<br>spec called_Address Translation Services_, where it can<br>be seen that the field encodes as:<br>00 = Default/Untranslated<br>01 = Translation Request<br>10 = Translated<br>11 = Reserved|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|TLP data payload transfer size, in DW. Encoding:<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|Last DW<br>Byte Enables<br>[3:0]|Byte 7 Bit 7:4|These four high‐true bits map one‐to‐one to the<br>bytes within the last double word of payload.<br>Bit 7 = 1: Byte 3 in last DW is valid; otherwise not<br>Bit 6 = 1: Byte 2 in last DW is valid; otherwise not<br>Bit 5 = 1: Byte 1 in last DW is valid; otherwise not<br>Bit 4 = 1: Byte 0 in last DW is valid; otherwise not|
|First DW<br>Byte Enables<br>[3:0]|Byte 7 Bit 3:0|These four high‐true bits map one‐to‐one to the<br>bytes within the first double word of payload.<br>Bit 3 = 1: Byte 3 in first DW is valid; otherwise not<br>Bit 2 = 1: Byte 2 in first DW is valid; otherwise not<br>Bit 1 = 1: Byte 1 in first DW is valid; otherwise not<br>Bit 0 = 1: Byte 0 in first DW is valid; otherwise not|



## **Generic Header Field Details** 

In the following sections, we describe details of each TLP Header field depicted in Figure 5‐3 on page 175. 

**178** 

**Chapter 5: TLP Elements** 

## **Header** _**Type/Format**_ **Field Encodings** 

Table 5‐3 on page 179 summarizes the encodings used in TLP header Type and Format (Fmt) fields. 

_Table 5‐3: TLP Header Type and Format Field Encodings_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Memory Read Request (MRd)|000 = 3DW, no data<br>001 = 4DW, no data|0 0000|
|Memory Read Lock Request (MRdLk)|000 = 3DW, no data<br>001 = 4DW, no data|0 0001|
|Memory Write Request (MWr)|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 0000|
|IO Read Request (IORd)|000 = 3DW, no data|0 0010|
|IO Write Request (IOWr)|010 = 3DW, w/ data|0 0010|
|Config Type 0 Read Request (CfgRd0)|000 = 3DW, no data|0 0100|
|Config Type 0 Write Request (CfgWr0)|010 = 3DW, w/ data|0 0100|
|Config Type 1 Read Request (CfgRd1)|000 = 3DW, no data|0 0101|
|Config Type 1 Write Request (CfgWr1)|010 = 3DW, w/ data|0 0101|
|Message Request (Msg)|001 = 4DW, no data|1 0 rrr*<br>(see routing field)|
|Message Request W/Data (MsgD)|011 = 4DW, w/ data|1 0rrr*<br>(see routing field)|
|Completion (Cpl)|000 = 3DW, no data|0 1010|
|Completion W/Data (CplD)|010 = 3DW, w/ data|0 1010|
|Completion‐Locked (CplLk)|000 = 3DW, no data|0 1011|
|Completion W/Data (CplDLk)|010 = 3DW, w/ data|0 1011|
|Fetch and Add AtomicOp Request|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 1100|



**179** 

**PCI Ex ress Technolo p gy** 

_Table 5‐3: TLP Header Type and Format Field Encodings (Continued)_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Unconditional Swap AtomicOp<br>Request|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 1101|
|Compare and Swap AtomicOp<br>Request|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 1110|
|Local TLP Prefix|100 = TLP Prefix|0L3L2L1L0|
|End‐to‐End TLP Prefix|100 = TLP Prefix|1E3E2E1E0|



## **Digest / ECRC Field** 

The TLP Digest bit reports the presence of the End‐to‐End CRC (ECRC). If this optional feature is supported and enabled by software, devices calculate and apply an ECRC for all TLPs they originate. Note that using ECRC requires devices to include the optional Advanced Error Reporting registers, since the capability and control registers for it are located there. 

**ECRC Generation and Checking.** ECRC covers all fields that do not change as the TLP is forwarded across the fabric. However, there are two bits that can legally change as a packet makes its way across a topology: 

- **Bit 0 of the Type field** — changes when a configuration transaction is for‐ warded across a bridge and changes from a type 1 to a type 0 configuration transaction because it has reached the targeted bus. This is accomplished by changing bit 0 of the type field. 

- **Error/Poisoned (EP) bit** — this can change as a TLP traverses the fabric if the data associated with the packet is seen as corrupted. This is an optional feature referred to as error forwarding. 

**Who Checks ECRC?** The intended target of an ECRC is the ultimate recipi‐ ent of the TLP. Checking the LCRC verifies no transmission errors across a given Link, but that gets recalculated for the packet at the egress port of a rout‐ ing element (Switch or Root Complex) before being forwarded to the next Link, which could mask an internal error in the routing element. To protect against that, the ECRC is carried forward unchanged on its journey between the Requester and Completer. When the target device checks the ECRC, any error possibilities along the way have a high probability of being detected. 

**180** 

**Chapter 5: TLP Elements** 

The spec makes two statements regarding a Switch’s role in ECRC checking: 

- A Switch that supports ECRC checking performs this check on TLPs des‐ tined to a location within the Switch itself. “On all other TLPs a Switch must preserve the ECRC (forward it untouched) as an integral part of the TLP.” 

- “Note that a Switch may perform ECRC checking on TLPs passing through the Switch. ECRC Errors detected by the Switch are reported in the same way any other device would report them, but do not alter the TLPs passage through the Switch.” 

## **Using Byte Enables** 

**General.** Like PCI, PCIe needs a mechanism to reconcile its DW‐aligned addresses with the need, at times, for transfer sizes or starting/ending addresses that are not DW aligned. Toward this end, PCI Express makes use of the two Byte Enable fields introduced earlier in Figure 5‐3 on page 175 and in Table 5‐2 on page 176. The First DW Byte Enable field and the Last DW Byte Enable fields allow the Requester to qualify the bytes of interest within the first and last dou‐ ble words transferred. 

## **Byte Enable Rules** 

1. Byte enable bits are high true. A value of 0 indicates the corresponding byte in the data payload should not be used by the Completer. A value of 1 indi‐ cates it should. 

2. If the valid data is all within a single double word, the Last DW Byte enable field must be = 0000b. 

3. If the header Length field indicates a transfer is more than 1DW, the First DW Byte Enable must have at least one bit enabled. 

4. If the Length field indicates a transfer of 3DW or more, then the First DW Byte Enable field and the Last DW Byte Enable field must have contiguous bits set. In these cases, the Byte Enables are only being used to give the byte offset of the effective starting and ending address from the DW‐aligned address. 

5. Discontinuous byte enable bit patterns in the First DW Byte enable field are allowed if the transfer is 1DW. 

6. Discontinuous byte enable bit patterns in both the First and Second DW Byte enable fields are allowed if the transfer is between one and two DWs. 

7. A write request with a transfer length of 1DW and no byte enables set is legal, but has no effect on the Completer.

</td>
<td style="background-color:#e8e8e8">

第 175 页图 5-3 说明了通用 TLP 4DW 头的格式和内容。在本节中，总结了几乎所有事务通用的字段。与特定事务类型相关的头格式差异将在后面介绍。

_图 5-3：通用 TLP 头字段_

**==> picture [328 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
事务层包 (TLP)<br>
成帧序列头成帧<br>
(STP)编号(End)<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R tr R H D P Attr AT Length<br>
最后 DW 第一个 DW<br>
字节 4 字节 4-7 随类型而变化 BE BE<br>
字节 8 字节 8-11 随类型而变化<br>
字节 12 字节 12-15 随类型而变化（并非总是必需）<br>**----- End of picture text -----**<br>


## **通用头字段汇总**

第 176 页表 5-2 总结了每个通用 TLP 头字段的大小和用途。请注意，第 175 页图 5-3 中标记为"R"的字段是保留的，应设置为零。

**175**

## **PCI Ex ress Technolo p gy**

_表 5-2：通用头字段汇总_

|**头字段**|**头位置**|**字段用途**|
|---|---|---|
|Fmt[2:0]<br>（格式）|字节 0 位 7:5|这些位编码有关头大小以及数据有效负载是否将成为 TLP 一部分的信息：<br>00b 3DW 头，无数据<br>01b 4DW 头，无数据<br>10b 3DW 头，带数据<br>11b 4DW 头，带数据<br>4GB 以下的地址必须使用 3DW 头。规范规定，如果对 4GB 以下的地址使用 4DW 头且 64 位地址的高 32 位设置为零，则接收器行为未定义。|
|Type[4:0]|字节 0 位 4:0|这些位编码与此 TLP 一起使用的事务变体。Type 字段与 Fmt [1:0] 字段一起使用以指定事务类型、头大小以及是否存在数据有效负载。有关详细信息，请参见第 178 页的"通用头字段详细信息"。|
|TC [2:0]<br>（流量类）|字节 1 位 6:4|这些位编码要应用于此 TLP 及与其关联的完成（如果有）的流量类：<br>000b = 流量类 0（默认）<br>.<br>.<br>111b = 流量类 7<br>TC 0 是默认类，而 TC 1-7 用于提供差异化服务。有关更多信息，请参见第 247 页的"流量类 (TC)"。|
|Attr [2]<br>（属性）|字节 1 位 2|第三个属性位指示此 TLP 是否要使用基于 ID 的排序。要了解更多信息，请参见第 301 页的"基于 ID 的排序 (IDO)"。|
|TH<br>（TLP 处理提示）|字节 1 位 0|指示何时已包含 TLP 提示以使系统了解如何最好地处理此 TLP。有关其用法的讨论，请参见第 899 页的"TPH（TLP 处理提示）"。|



**176**

**第 5 章：TLP 元素**

_表 5-2：通用头字段汇总（续）_

|**头字段**|**头位置**|**字段用途**|
|---|---|---|
|TD<br>（TLP 摘要）|字节 2 位 7|如果 TD = 1，则此 TLP 已包含可选的 4 字节 TLP 摘要作为 ECRC 值。<br>一些规则：<br>• 必须由所有接收器根据此位检查摘要字段的存在。<br>• TD = 1 但没有摘要的 TLP 将作为畸形 TLP 处理。<br>• 如果设备支持检查 ECRC 且 TD=1，则它必须执行 ECRC 检查。<br>• 如果设备在最终目标不支持检查 ECRC（可选），则它必须忽略该摘要。<br>有关此主题的更多信息，请参见第 653 页的"CRC"和第 657 页的"ECRC 生成和检查"。|
|EP<br>（Poisoned 数据）|字节 2 位 6|如果 EP = 1，则伴随此数据的数据应被视为无效，即使事务被允许正常完成。有关中毒包 (Poisoned Packet) 的更多信息，请参见第 660 页的"数据中毒"。|
|Attr [1:0]<br>（属性）|字节 2 位 5:4|位 5 = 宽松排序：设置为 1 时，为此 TLP 启用 PCI-X 宽松排序。如果为 0，则使用严格的 PCI 排序。<br>位 4 = 无窥探：设置为 1 时，请求者指示此 TLP 不存在主机缓存一致性问题。因此系统硬件可以通过跳过此请求的正常处理器缓存窥探来节省时间。当为 0 时，需要 PCI 类型的缓存窥探保护。|



**177**

## **PCI Ex ress Technolo p gy**

_表 5-2：通用头字段汇总（续）_

|**头字段**|**头位置**|**字段用途**|
|---|---|---|
|地址类型 [1:0]|字节 2 位 3:2|对于内存和原子请求，此字段支持虚拟化系统的地址转换。转换协议在称为_地址转换服务_的单独规范中描述，从中可以看到该字段编码为：<br>00 = 默认/未转换<br>01 = 转换请求<br>10 = 已转换<br>11 = 保留|
|长度 [9:0]|字节 2 位 1:0<br>字节 3 位 7:0|TLP 数据有效负载传输大小，以 DW 为单位。编码：<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|最后 DW 字节使能<br>[3:0]|字节 7 位 7:4|这四个高真位一对一映射到有效负载最后一个双字内的字节。<br>位 7 = 1：最后 DW 中的字节 3 有效；否则无效<br>位 6 = 1：最后 DW 中的字节 2 有效；否则无效<br>位 5 = 1：最后 DW 中的字节 1 有效；否则无效<br>位 4 = 1：最后 DW 中的字节 0 有效；否则无效|
|第一个 DW 字节使能<br>[3:0]|字节 7 位 3:0|这四个高真位一对一映射到有效负载第一个双字内的字节。<br>位 3 = 1：第一个 DW 中的字节 3 有效；否则无效<br>位 2 = 1：第一个 DW 中的字节 2 有效；否则无效<br>位 1 = 1：第一个 DW 中的字节 1 有效；否则无效<br>位 0 = 1：第一个 DW 中的字节 0 有效；否则无效|



## **通用头字段详细信息**

在以下各节中，我们描述了第 175 页图 5-3 中所示的每个 TLP 头字段的详细信息。

**178**

**第 5 章：TLP 元素**

## **头** _**类型/格式**_ **字段编码**

第 179 页表 5-3 总结了 TLP 头 Type 和 Format (Fmt) 字段中使用的编码。

_表 5-3：TLP 头类型和格式字段编码_

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|内存读请求 (MRd)|000 = 3DW，无数据<br>001 = 4DW，无数据|0 0000|
|内存读锁定请求 (MRdLk)|000 = 3DW，无数据<br>001 = 4DW，无数据|0 0001|
|内存写请求 (MWr)|010 = 3DW，带数据<br>011 = 4DW，带数据|0 0000|
|IO 读请求 (IORd)|000 = 3DW，无数据|0 0010|
|IO 写请求 (IOWr)|010 = 3DW，带数据|0 0010|
|配置类型 0 读请求 (CfgRd0)|000 = 3DW，无数据|0 0100|
|配置类型 0 写请求 (CfgWr0)|010 = 3DW，带数据|0 0100|
|配置类型 1 读请求 (CfgRd1)|000 = 3DW，无数据|0 0101|
|配置类型 1 写请求 (CfgWr1)|010 = 3DW，带数据|0 0101|
|消息请求 (Msg)|001 = 4DW，无数据|1 0 rrr*<br>（参见路由字段）|
|带数据消息请求 (MsgD)|011 = 4DW，带数据|1 0rrr*<br>（参见路由字段）|
|完成 (Cpl)|000 = 3DW，无数据|0 1010|
|带数据完成 (CplD)|010 = 3DW，带数据|0 1010|
|完成锁定 (CplLk)|000 = 3DW，无数据|0 1011|
|带数据完成 (CplDLk)|010 = 3DW，带数据|0 1011|
|取并加原子操作请求|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1100|



**179**

**PCI Ex ress Technolo p gy**

_表 5-3：TLP 头类型和格式字段编码（续）_

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|无条件交换原子操作请求|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1101|
|比较并交换原子操作请求|010 = 3DW，带数据<br>011 = 4DW，带数据|0 1110|
|本地 TLP 前缀|100 = TLP 前缀|0L3L2L1L0|
|端到端 TLP 前缀|100 = TLP 前缀|1E3E2E1E0|



## **摘要 / ECRC 字段**

TLP 摘要位报告端到端 CRC (ECRC) 的存在。如果软件支持并启用了此可选功能，则设备为其发起的所有 TLP 计算并应用 ECRC。请注意，使用 ECRC 要求设备包含可选的高级错误报告寄存器，因为它的能力和控制寄存器位于那里。

**ECRC 生成和检查。** ECRC 涵盖 TLP 通过互连结构转发时不会更改的所有字段。但是，在包通过拓扑时有两个位可以合法地更改：

- **Type 字段的位 0** - 当配置事务通过桥转发并且从类型 1 变为类型 0 配置事务时（因为它已到达目标总线），会发生变化。这是通过更改类型字段的位 0 来实现的。

- **错误/Poisoned (EP) 位** - 如果与包关联的数据被视为损坏，则在 TLP 通过互连结构时可能会更改。这是称为错误转发的可选功能。

**谁检查 ECRC？** ECRC 的预期目标是 TLP 的最终接收者。检查 LCRC 验证给定链路上没有传输错误，但在路由元素（交换机或根复合体）的出口端口转发到下一个链路之前，该包会重新计算，这可能会掩盖路由元素中的内部错误。为了防止这种情况，ECRC 在请求者和完成者之间的旅程中保持不变。当目标设备检查 ECRC 时，沿途的任何错误可能性都有很高的概率被检测到。

**180**

**第 5 章：TLP 元素**

规范对交换机在 ECRC 检查中的角色作了两个声明：

- 支持 ECRC 检查的交换机对发往交换机内位置的 TLP 执行此检查。"对于所有其他 TLP，交换机必须保留 ECRC（按原样转发）作为 TLP 的组成部分。"

- "请注意，交换机可以对通过交换机的 TLP 执行 ECRC 检查。交换机检测到的 ECRC 错误以与任何其他设备报告它们相同的方式报告，但不会改变 TLP 通过交换机的路径。"

## **使用字节使能**

**概述。** 与 PCI 一样，PCIe 需要一种机制来协调其 DW 对齐的地址与有时需要的非 DW 对齐的传输大小或开始/结束地址。为此，PCI Express 使用了前面在第 175 页图 5-3 和第 176 页表 5-2 中介绍的两个字节使能字段。第一个 DW 字节使能字段和最后 DW 字节使能字段允许请求者限定所传输的第一个和最后一个双字内感兴趣的字节。

## **字节使能规则**

1. 字节使能位为高真。值 0 表示不应由完成者使用数据有效负载中的相应字节。值 1 表示应使用它。

2. 如果有效数据全部在单个双字内，则最后 DW 字节使能字段必须为 = 0000b。

3. 如果头长度字段指示传输超过 1DW，则第一个 DW 字节使能必须至少启用一位。

4. 如果长度字段指示 3DW 或更多的传输，则第一个 DW 字节使能字段和最后 DW 字节使能字段必须具有连续的位设置。在这些情况下，字节使能仅用于给出有效开始和结束地址距 DW 对齐地址的字节偏移量。

5. 如果传输为 1DW，则第一个 DW 字节使能字段中允许不连续的字节使能位模式。

6. 如果传输在一个到两个 DW 之间，则第一个和第二个 DW 字节使能字段中允许不连续的字节使能位模式。

7. 传输长度为 1DW 且未设置任何字节使能的写请求是合法的，但对完成者没有影响。

**181**

## **PCI Ex ress Technolo p gy**

8. 如果 1 DW 的读请求未设置任何字节使能，则完成者返回 1 DW 的未定义数据的有效负载。这可以用作利用事务排序规则来强制所有先前已发布的写在完成返回之前输出到内存的刷新机制。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---



<img src="figures/embedded/page0177_img1_tight.png" alt="Figure from page 177" width="700">

<a id="sec-5-10"></a>
## 5.10 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

8. If a read request of 1 DW has no byte enables set, the completer returns a 1DW data payload of undefined data. This may be used as a Flush mecha‐ nism that takes advantage of transaction ordering rules to force all previ‐ ously posted writes out to memory before the completion is returned. 

**181** 

## **PCI Ex ress Technolo p gy** 

**Byte Enable Example.** An example of byte enable use in this case is illus‐ trated in Figure 5‐4 on page 182. Note that the transfer length must extend from the first DW with any valid byte enabled to the last DW with any valid bytes enabled. Because the transfer is more than 2DW, the byte enables may only be used to specify the start address location (2d) and end address location (34d) of the transfer. 

_Figure 5‐4: Using First DW and Last DW Byte Enable Fields_ 

## **Transaction Descriptor Fields** 

As transactions move between requester and completer, it’s necessary to uniquely identify a transaction, since many split transactions may be queued up from the same Requester at any instant. To help with this, the spec defines sev‐ eral important header fields that form a unique Transaction Descriptor, as illus‐ trated in Figure 5‐5. 

**182** 

**Chapter 5: TLP Elements** 

_Figure 5‐5: Transaction Descriptor Fields_ 

**==> picture [384 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Completer ID Cmpl CB Byte Count<br>Status M<br>Byte 8 Requester ID Tag R Lower Addr<br>**----- End of picture text -----**<br>


While the Transaction Descriptor fields are not in adjacent header locations, col‐ lectively they describe key transaction attributes, including: 

**Transaction ID.** The combination of the Requester ID (Bus, Device, and Function Number of the Requester) and the Tag field of the TLP. 

**Traffic Class.** The Traffic Class (TC) is added by the requester based on the core logic request and travels unmodified through the topology to the Compl‐ eter. On every Link, the TC is mapped to one of the Virtual Channels. 

**Transaction Attributes.** The ID‐based Ordering, Relaxed Ordering, and No Snoop bits also travel with the Request packet to the Completer. 

## **Additional Rules For TLPs With Data Payloads** 

The following rules apply when a TLP includes a data payload. 

1. The Length field refers only to the data payload. 

2. The first byte of data in the payload (immediately after the header) is always associated with the lowest (start) address. 

3. The Length field always represents an integral number of DWs transferred. Partial DWs are qualified using First and Last Byte Enable fields. 

4. The spec states that, when multiple transactions are returned by a compl‐ eter in response to a single memory request, each intermediate transaction must end on naturally‐aligned 64‐ or 128‐byte address boundaries for a Root Complex. This is controlled by a configuration bit called the Read Completion Boundary (RCB). All other devices follow the PCI‐X protocol 

**183** 

## **PCI Ex ress Technolo p gy** 

and break such transactions at naturally‐aligned 128‐byte boundaries. This makes buffer management simpler in bridges. 

5. The Length field is reserved when sending Message Requests unless the message is the version with data ( _MsgD_ ). 

6. The TLP data payload must not exceed the current value in the Max_Payload_Size field of the Device Control Register. Only write transac‐ tions have data payloads, so this restriction doesn’t apply to read requests. A receiver is required to check for violations of the Max_Payload_Size limit during writes, and violations are treated as Malformed TLPs. 

7. Receivers also must check for discrepancies between the value in the Length field and the actual amount of data transferred in a TLP. This type of viola‐ tion is also treated as a Malformed TLP. 

8. Requests must not mix combinations of start address and transfer length that would cause a memory access to cross a 4KB boundary. While checking for this is optional, if seen it’s treated as a Malformed TLP. 

## **Specific TLP Formats: Request & Completion TLPs** 

In this section, the format of 3DW and 4DW headers used to accomplish specific transaction types are described. Many of the generic fields described previously apply, but an emphasis is placed on the fields which are handled differently with specific transaction types. Detailed description of TLP Header format are described is sections following for TLP types: 1) IO Request, 2) Memory Requests, 3) Configuration Requests, 4) Completions and 5) Message Requests. 

## **IO Requests** 

While the spec discourages the use of IO transactions, allowance is made for Legacy devices and for software that may need to rely on a compatible device residing in the system IO map rather than the memory map. While the IO trans‐ actions can technically access a 32‐bit IO range, in reality many systems (and CPUs) restrict IO access to the lower 16 bits (64KB) of this range. Figure 5‐6 on page 185 depicts the system IO map and the 16‐ and 32‐bit address boundaries. Devices that don’t identify themselves as Legacy devices are not permitted to request IO address space in their configuration Base Address Registers. 

**184** 

**Chapter 5: TLP Elements** 

_Figure 5‐6: System IO Map_ 

**IO Request Header Format.** A 3 DW IO request header is shown in Fig‐ ure 5‐7 on page 185 and each of the fields is described in the section that fol‐ lows. 

_Figure 5‐7: 3DW IO Request Header Format_ 

**==> picture [281 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>IO Request TLP<br>a|<br>Legacy =o Framing(STP) SequenceNumber Header Data Digest LCRC Framing(End)<br>Endpoint<br>+0 +1 +2 +3<br>Peer 7 6 5 4 3 2 1 0 7 nT 6 5 4 3 2 1 0 7 6 5 4 3 2 TTT 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 0 1 0Type R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**185** 

**PCI Ex ress Technolo p gy** 

**IO Request Header Fields.** The location and use of each field in an IO request header is described in Table 5‐4 on page 186. 

_Table 5‐4: IO Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Format for IO requests:<br>000b = IO Read (3DW without data)<br>010b = IO Write (3DW with data)|
|Type [4:0]|Byte 0 Bit 4:0|Packet type is 00010b for IO requests|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Traffic Class for IO requests is always<br>zero, ensuring that these packets will<br>never interfere with any high‐priority<br>packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|ID‐based Ordering doesn’t apply for<br>IO requests and this bit is reserved.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|TLP processing Hints don’t apply to<br>IO requests and this bit is reserved.|
|TD<br>(TLP Digest)|Byte 2 Bit 7|Indicates the presence of a digest field<br>(ECRC) at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|Indicates whether the data payload (if<br>present) is poisoned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Relaxed Ordering and No Snoop bits<br>don’t apply for IO requests and are<br>always zero.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type doesn’t apply for IO<br>requests and these bits must be zero.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW.<br>For IO requests, this field is always<br>just 1 since no more than 4 bytes can<br>be transferred. The First DW Byte<br>Enables qualify which bytes are used.|



**186** 

**Chapter 5: TLP Elements** 

_Table 5‐4: IO Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester’s “return<br>address” for corresponding Comple‐<br>tion.<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These bits identify the specific<br>requests from the requester. A unique<br>tag value is assigned to each outgoing<br>Request. By default, only bits 4:0 are<br>used, but the Extended Tag and Phan‐<br>tom Functions options can extend that<br>to 11 bits, permitting up to 2048 out‐<br>standing requests to be in progress<br>simultaneously.|
|Last DW BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These bits must be 0000b because IO<br>requests can only be one DW in size.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These bits qualify the bytes in the one‐<br>DW payload. For IO requests, any bit<br>combination is valid (including all<br>zeros).|
|Address [31:2]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:2|The upper 30 bits of the 32‐bit start<br>address for the IO transfer. The lower<br>two bits of the 32 bit address are<br>reserved (00b), forcing a DW‐aligned<br>start address.|



**187** 

**PCI Ex ress Technolo p gy** 

## **Memory Requests** 

PCI Express memory transactions include two classes: Read Requests with their corresponding Completions, and Write Requests. The system memory map shown in Figure 5‐8 on page 188 depicts both a 3DW and 4DW memory request packet. Keep in mind a point that the spec reiterates several times: a memory transfer is never permitted to cross a 4KB address boundary. 

_Figure 5‐8: 3DW And 4DW Memory Request Header Formats_ 

**==> picture [382 x 316] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex Memory<br>3DW or 4DW Memory Request TLP<br>Framing(STP) SequenceNumber Header Data Digest LCRC Framing(End)<br>4DW Memory Request Header<br>PCIe +0 +1 +2 +3<br>Endpoint System Memory Map<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2 64<br>Byte 0 0 x 1Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>3DW Memory Request Header<br>+0 +1 +2 +3<br>4GB<br>32<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2<br>Byte 0 0 x 0Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE 0<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**Memory Request Header Fields.** The location and use of each field in a 4DW memory request header is listed in Table 5‐5 on page 189. Note that the difference between a 3DW header and a 4DW header is simply the location and size of the starting Address field. 

**188** 

**Chapter 5: TLP Elements** 

_Table 5‐5: 4DW Memory Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Formats:<br>000b = Memory Read (3DW w/o data)<br>010b = Memory Write (3DW w/ data)<br>001b = Memory Read (4DW w/o data)<br>011b = Memory Write (4DW w/ data)<br>1xxb = TLP Prefix has been added to<br>the beginning of the packet. See “TPH<br>(TLP Processing Hints)” on page 899<br>for more on this.|
|Type[4:0]|Byte 0 Bit 4:0|TLP packet Type field:<br>00000b = Memory Read or Write<br>00001b = Memory Read Locked<br>Type field is used with Fmt [1:0] field<br>to specify transaction type, header<br>size, and whether data payload is<br>present.|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|These bits encode the traffic class to<br>be applied to a Request and to any<br>associated Completion.<br>000b = Traffic Class 0 (Default)<br>.<br>.<br>111b = Traffic Class 7<br>See“Traffic Class (TC)” on page 247<br>for more on this.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|Indicates whether ID‐based Ordering<br>is to be used for this TLP. To learn<br>more, see “ID Based Ordering (IDO)”<br>on page 301.|

</td>
<td style="background-color:#e8e8e8">

8. 如果 1 DW 的读请求未设置任何字节使能，则完成者返回 1 DW 的未定义数据的有效负载。这可以用作利用事务排序规则来强制所有先前已发布的写在完成返回之前输出到内存的刷新机制。

**181**

## **PCI Ex ress Technolo p gy**

**字节使能示例。** 这种情况下的字节使能使用示例如第 182 页图 5-4 所示。请注意，传输长度必须从启用任何有效字节的第一个 DW 扩展到启用任何有效字节的最后一个 DW。因为传输超过 2DW，所以字节使能只能用于指定传输的开始地址位置（2d）和结束地址位置（34d）。

_图 5-4：使用第一个 DW 和最后 DW 字节使能字段_

## **事务描述符字段**

随着事务在请求者和完成者之间移动，有必要唯一地标识一个事务，因为同一请求者在任何时刻可能有多个分离事务排队。为了帮助解决这个问题，规范定义了几个重要的头字段，它们构成唯一的事务描述符 (Transaction Descriptor)，如图 5-5 所示。

**182**

**第 5 章：TLP 元素**

_图 5-5：事务描述符字段_

**==> picture [384 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
At T T E<br>
字节 0 Fmt Type R TC R R Attr AT Length<br>
tr H D P<br>
字节 4 完成者 ID Cmpl CB 字节数<br>
状态 M<br>
字节 8 请求者 ID 标签 R 低地址<br>**----- End of picture text -----**<br>


虽然事务描述符字段不在相邻的头位置，但总的来说，它们描述了关键的事务属性，包括：

**事务 ID。** Requester ID（请求者的总线、设备和功能号）和 TLP 的 Tag 字段的组合。

**流量类。** 流量类 (TC) 由请求者根据核心逻辑请求添加，并通过拓扑未经修改地传送到完成者。在每个链路上，TC 映射到虚拟通道之一。

**事务属性。** 基于 ID 的排序、宽松排序和无窥探位也与请求包一起传送到完成者。

## **具有数据有效负载的 TLP 的其他规则**

以下规则适用于 TLP 包含数据有效负载时。

1. 长度字段仅指数据有效负载。

2. 有效负载中数据的第一个字节（紧接在头之后）始终与最低（开始）地址相关联。

3. 长度字段始终表示传输的整数个 DW。部分 DW 使用第一个和最后字节使能字段进行限定。

4. 规范规定，当完成者响应单个内存请求返回多个事务时，每个中间事务必须在根复合体的 64 或 128 字节自然对齐地址边界处结束。这由称为读完成边界 (RCB) 的配置位控制。所有其他设备遵循 PCI-X 协议

**183**

## **PCI Ex ress Technolo p gy**

并在自然对齐的 128 字节边界处打破此类事务。这使得桥中的缓冲区管理更简单。

5. 在发送消息请求时，长度字段是保留的，除非消息是带数据的版本 (_MsgD_)。

6. TLP 数据有效负载不得超过 Device Control 寄存器中 Max_Payload_Size 字段的当前值。只有写事务具有数据有效负载，因此此限制不适用于读请求。接收器需要在写期间检查是否违反 Max_Payload_Size 限制，违反将被视为畸形 TLP。

7. 接收器还必须检查长度字段中的值与 TLP 中实际传输的数据量之间的差异。这种类型的违规也被视为畸形 TLP。

8. 请求不得混合会导致内存访问跨越 4KB 边界的开始地址和传输长度组合。虽然对此的检查是可选的，但如果看到则视为畸形 TLP。

## **特定 TLP 格式：请求和完成 TLP**

在本节中，描述了用于完成特定事务类型的 3DW 和 4DW 头的格式。先前描述的许多通用字段适用，但重点放在与特定事务类型处理方式不同的字段上。TLP 头格式的详细描述在以下部分中描述的 TLP 类型：1) IO 请求，2) 内存请求，3) 配置请求，4) 完成和 5) 消息请求。

## **IO 请求**

虽然规范不鼓励使用 IO 事务，但允许传统设备以及可能需要依赖驻留在系统 IO 映射中而不是内存映射中的兼容设备的软件。虽然 IO 事务在技术上可以访问 32 位 IO 范围，但实际上许多系统（和 CPU）将 IO 访问限制在此范围的低 16 位（64KB）。第 185 页图 5-6 描述了系统 IO 映射以及 16 位和 32 位地址边界。不将自己标识为传统设备的设备不允许在其配置基地址寄存器中请求 IO 地址空间。

**184**

**第 5 章：TLP 元素**

_图 5-6：系统 IO 映射_

**IO 请求头格式。** 3 DW IO 请求头如图 5-7（第 185 页）所示，每个字段在后面的部分中描述。

_图 5-7：3DW IO 请求头格式_

**==> picture [281 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体<br>
IO 请求 TLP<br>
a|<br>
传统 =o 成帧(STP)序列号头数据摘要LCRC成帧(End)<br>
端点<br>
+0 +1 +2 +3<br>
对等 7 6 5 4 3 2 1 0 7 nT 6 5 4 3 2 1 0 7 6 5 4 3 2 TTT 1 0 7 6 5 4 3 2 1 0<br>
字节 0 0 x 0Fmt 0 0 0 1 0Type R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 0 1Length<br>
字节 4 请求者 ID 标签 最后 DW BE0 0 0 0 1st DWBE<br>
字节 8 地址 [31:2] R<br>**----- End of picture text -----**<br>


**185**

**PCI Ex ress Technolo p gy**

**IO 请求头字段。** 第 186 页表 5-4 描述了 IO 请求头中每个字段的位置和用途。

_表 5-4：IO 请求头字段_

|**字段名称**|**头字节/位**|**功能**|
|---|---|---|
|Fmt [2:0]<br>（格式）|字节 0 位 7:5|IO 请求的包格式：<br>000b = IO 读（3DW 无数据）<br>010b = IO 写（3DW 带数据）|
|Type [4:0]|字节 0 位 4:0|IO 请求的包类型为 00010b|
|TC [2:0]<br>（流量类）|字节 1 位 6:4|IO 请求的流量类始终为零，确保这些包永远不会干扰任何高优先级的包。|
|Attr [2]<br>（属性）|字节 1 位 2|基于 ID 的排序不适用于 IO 请求，并且此位被保留。|
|TH<br>（TLP 处理提示）|字节 1 位 0|TLP 处理提示不适用于 IO 请求，并且此位被保留。|
|TD<br>（TLP 摘要）|字节 2 位 7|指示 TLP 末尾的摘要字段 (ECRC) 的存在。|
|EP<br>（Poisoned 数据）|字节 2 位 6|指示数据有效负载（如果存在）是否被中毒。|
|Attr [1:0]<br>（属性）|字节 2 位 5:4|宽松排序和无窥探位不适用于 IO 请求，始终为零。|
|AT [1:0]<br>（地址类型）|字节 2 位 3:2|地址类型不适用于 IO 请求，这些位必须为零。|
|长度 [9:0]|字节 2 位 1:0<br>字节 3 位 7:0|以 DW 为单位指示数据有效负载大小。<br>对于 IO 请求，此字段始终为 1，因为最多只能传输 4 个字节。第一个 DW 字节使能限定使用哪些字节。|



**186**

**第 5 章：TLP 元素**

_表 5-4：IO 请求头字段（续）_

|**字段名称**|**头字节/位**|**功能**|
|---|---|---|
|请求者 ID [15:0]|字节 4 位 7:0<br>字节 5 位 7:0|标识请求者的"返回地址"以用于相应的完成。<br>字节 4，7:0 = 总线号<br>字节 5，7:3 = 设备号<br>字节 5，2:0 = 功能号|
|标签 [7:0]|字节 6 位 7:0|这些位标识来自请求者的特定请求。为每个出站请求分配一个唯一的标签值。默认情况下，仅使用位 4:0，但扩展标签和虚拟功能选项可将其扩展到 11 位，从而允许同时处理多达 2048 个未完成的请求。|
|最后 DW BE [3:0]<br>（最后 DW 字节使能）|字节 7 位 7:4|这些位必须为 0000b，因为 IO 请求只能是一个 DW 大小。|
|1st DW BE [3:0]<br>（第一个 DW 字节使能）|字节 7 位 3:0|这些位限定一个 DW 有效负载中的字节。对于 IO 请求，任何位组合都是有效的（包括全零）。|
|地址 [31:2]|字节 8 位 7:0<br>字节 9 位 7:0<br>字节 10 位 7:0<br>字节 11 位 7:2|IO 传输的 32 位起始地址的高 30 位。32 位地址的低两位被保留（00b），强制 DW 对齐的起始地址。|



**187**

**PCI Ex ress Technolo p gy**

## **内存请求**

PCI Express 内存事务包括两类：读请求及其相应的完成，以及写请求。第 188 页图 5-8 中所示的系统内存映射描述了 3DW 和 4DW 内存请求包。请记住规范多次重申的一点：内存传输绝不允许跨越 4KB 地址边界。

_图 5-8：3DW 和 4DW 内存请求头格式_

**==> picture [382 x 316] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
根复合体 内存<br>
3DW 或 4DW 内存请求 TLP<br>
成帧(STP)序列号头数据摘要LCRC成帧(End)<br>
4DW 内存请求头<br>
PCIe +0 +1 +2 +3<br>
端点 系统内存映射<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2 64<br>
字节 0 0 x 1Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>
字节 4 请求者 ID 标签 最后 DWBE 1st DWBE<br>
字节 8 地址 [63:32]<br>
字节 12 地址 [31:2] R<br>
3DW 内存请求头<br>
+0 +1 +2 +3<br>
4GB<br>
32<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2<br>
字节 0 0 x 0Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>
字节 4 请求者 ID 标签 最后 DWBE 1st DWBE 0<br>
字节 8 地址 [31:2] R<br>**----- End of picture text -----**<br>


**内存请求头字段。** 第 189 页表 5-5 中列出了 4DW 内存请求头中每个字段的位置和用途。请注意，3DW 头和 4DW 头之间的区别仅在于起始地址字段的位置和大小。

**188**

**第 5 章：TLP 元素**

_表 5-5：4DW 内存请求头字段_

|**字段名称**|**头字节/位**|**功能**|
|---|---|---|
|Fmt [2:0]<br>（格式）|字节 0 位 7:5|包格式：<br>000b = 内存读（3DW 无数据）<br>010b = 内存写（3DW 带数据）<br>001b = 内存读（4DW 无数据）<br>011b = 内存写（4DW 带数据）<br>1xxb = TLP 前缀已添加到包的开头。有关更多信息，请参见第 899 页的"TPH（TLP 处理提示）"。|
|Type[4:0]|字节 0 位 4:0|TLP 包类型字段：<br>00000b = 内存读或写<br>00001b = 内存读锁定<br>类型字段与 Fmt [1:0] 字段一起使用以指定事务类型、头大小以及是否存在数据有效负载。|
|TC [2:0]<br>（流量类）|字节 1 位 6:4|这些位编码要应用于请求及任何关联完成的流量类。<br>000b = 流量类 0（默认）<br>.<br>.<br>111b = 流量类 7<br>有关更多信息，请参见第 247 页的"流量类 (TC)"。|
|Attr [2]<br>（属性）|字节 1 位 2|指示此 TLP 是否要使用基于 ID 的排序。要了解更多信息，请参见第 301 页的"基于 ID 的排序 (IDO)"。|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-11"></a>
## 5.11 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|Indicates whether TLP Hints have<br>been included. See “TPH (TLP Pro‐<br>cessing Hints)” on page 899 for a dis‐<br>cussion on these hints.|



**189** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐5: 4DW Memory Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**||**Function**|
|---|---|---|---|
|TD<br>(TLP Digest)|Byte 2 Bit 7||If 1, the optional TLP Digest field is<br>included with this TLP.<br>Some rules<br>:<br>The presence of the Digest field must<br>be checked by all receivers (using this<br>bit)<br>• TLPs with TD = 1 but no Digest<br>field are treated as Malformed.<br>• If the TD bit is set, recipient must<br>perform the ECRC check if enabled.<br>• If a Receiver doesn’t support the<br>optional ECRC checking, it must<br>ignore the digest field.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6||If 1, the data accompanying this<br>packet should be considered to have<br>an error although the transaction is<br>allowed to complete normally.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4||Bit 5=Relaxed ordering<br>.<br>When set = 1, PCI‐X relaxed ordering<br>is enabled for this TLP. Otherwise,<br>strict PCI ordering is used.<br>Bit 4=No Snoop<br>.<br>If 1, system hardware is not required<br>to cause processor cache snoop for<br>coherency for this TLP. Otherwise,<br>cache snooping is required.|
|Address Type [1:0]|Byte 2 Bit 3:2||This field supports address transla‐<br>tion for virtualized systems. The<br>translation protocol is described in a<br>separate spec called_Address Transla‐_<br>_tion Services_, where it can be seen that<br>the field encodes as:<br>00 = Default/Untranslated<br>01 = Translation Request<br>10 = Translated<br>11 = Reserved|



**190** 

**Chapter 5: TLP Elements** 

_Table 5‐5: 4DW Memory Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|TLP data payload transfer size, in<br>DW. Maximum size is 1024 DW<br>(4KB), encoded as:<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies a Requester’s return<br>address for a completion:<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These identify each outstanding<br>request issued by the Requester.<br>By default only bits 4:0 are used,<br>allowing up to 32 requests to be in<br>progress at a time. If the Extended<br>Tag bit in the Control Register is set,<br>then all 8 bits may be used (256 tags).|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These qualify bytes within the last<br>DW of data transferred.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These qualify bytes within the first<br>DW of the data payload.|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|The upper 32 bits of the 64‐bit start<br>address for the memory transfer.|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|The lower 32 bits of the 64 bit start<br>address for the memory transfer. The<br>lower two bits of the address are<br>reserved, forcing a DW‐aligned start<br>address.|



**191** 

## **PCI Ex ress Technolo p gy** 

**Memory Request Notes.** Features of memory requests include: 

1. Memory data transfers are not permitted to cross a 4KB boundary. 

2. All memory‐mapped writes are posted to improve performance. 

3. Either 32‐ or 64‐bit addressing may be used. 

4. Data payload size is between 0 and 1024 DW (0‐4KB). 

5. Quality of Service features may be used, including up to 8 Traffic Classes. 

6. The No Snoop attribute can be used to relieve the system of the need to snoop processor caches when transactions target main memory. 

7. The Relaxed Ordering attribute may be used to allow devices in the packet’s path to apply the relaxed ordering rules in hopes of improving perfor‐ mance. 

## **Configuration Requests** 

PCI Express uses both Type 0 and Type 1 configuration requests the same way PCI did to maintain backward compatibility. A Type 1 cycle propagates down‐ stream until it reaches the bridge whose secondary bus matches the target bus. At that point, the configuration transaction is converted from Type 1 to Type 0 by the bridge. The bridge knows when to forward and convert configuration cycles based on the previously programmed bus number registers: Primary, Secondary, and Subordinate Bus Numbers. For more on this topic, refer to the section “Legacy PCI Mechanism” on page 91. 

**192** 

**Chapter 5: TLP Elements** 

_Figure 5‐9: 3DW Configuration Request And Header Format_ 

**==> picture [368 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Type 1<br> Configuration Request<br>Switch<br>Type 0<br> Configuration Request Configuration Request TLP<br>Framing Sequence Framing<br>PCIe Header Data Digest LCRC<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 1 0 xType R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Bus Number Device Func Rsvd Ext Reg Register R<br>Function Number with ARI Number Number<br>**----- End of picture text -----**<br>


In Figure 5‐9 on page 193, a Type 1 configuration cycle is shown making its way downstream, where it is converted to Type 0 by the bridge for that bus (accom‐ plished by changing bit 0 of the Type field). Note that, unlike PCI, only one device can reside downstream on a Link. Consequently, no IDSEL or other hardware indication is needed to tell the device that it should claim the Type 0 cycle; any Type 0 configuration cycle a device sees on its Upstream Link will be understood as targeting that device. 

**Definitions Of Configuration Request Header Fields.** Table 5‐6 on page 194 describes the location and use of each field in the configuration request header illustrated in Figure 5‐9 on page 193. 

**193** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐6: Configuration Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Always a 3DW header<br>000b = configuration read (no data)<br>010b = configuration write (with data)|
|Type [4:0]|Byte 0 Bit 4:0|00100b = Type 0 Config Request<br>00101b = Type 1 Config Request|
|TC [2:0]<br>(Transfer Class)|Byte 1 Bit 6:4|Traffic Class must be zero for Configu‐<br>ration requests, ensuring that these<br>packets will never interfere with any<br>high‐priority packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|These bits are reserved and must be<br>zero for Config Requests.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||
|TD<br>(TLP Digest)|Byte 2 Bit 7|Indicates the presence of a digest field<br>(1 DW) at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|Indicates that data payload is poi‐<br>soned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Relaxed Ordering and No Snoop bits<br>are both always = 0 in configuration<br>requests.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type is reserved for config<br>requests and must be zero.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Data payload size in DW is always = 1<br>for configuration requests. Byte<br>Enables qualify bytes within the DW<br>and any combination is legal.|



**194** 

**Chapter 5: TLP Elements** 

_Table 5‐6: Configuration Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester’s return<br>address for a completion:<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These bits identify outstanding request<br>issued by the requester. By default,<br>only bits 4:0 are used (32 outstanding<br>transactions at a time), but if the<br>Extended Tag bit in the Control Regis‐<br>ter is set = 1, then all 8 bits may be used<br>(256 tags).|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These qualify bytes in the last data DW<br>transferred. Since config requests can<br>only be one DW in size, these bits must<br>be zero.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These high‐true bits qualify bytes in<br>the first data DW transferred. For con‐<br>fig requests, any bit combination is<br>valid (including none active).|
|Completer ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|Identifies the completer being accessed<br>with this configuration cycle.<br>Byte 8, 7:0 = Bus Number<br>Byte 9, 7:3 = Device Number<br>Byte 9, 2:0 = Function Number|
|Ext Register Number<br>[3:0]<br>(Extended Register<br>Number)|Byte 10 Bit 3:0|These provide the upper 4 bits of DW<br>space for accessing the extended con‐<br>fig space. They’re combined with Reg‐<br>ister Number to create the 10‐bit<br>address needed to access the 1024 DW<br>(4096 byte) space. For PCI‐compatible<br>config space, this field must be zero.|



**195** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐6: Configuration Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Register Number [5:0]|Byte 11 Bit 7:0|As the lower 8 bits of configuration<br>DW space, these specify the register<br>number. The two lowest bits are<br>always zero, forcing DW‐aligned<br>accesses.|



**Configuration Request Notes.** Configuration requests always use the 3DW header format and are routed based on the target Bus, Device and Func‐ tion numbers. All devices “capture” their Bus and Device Number from the tar‐ get numbers in the Request whenever they receive a Type 0 configuration write cycle. The reason for that is because they’ll need it later to use as their Requester ID when they send requests of their own in the future. 

## **Completions** 

Completions are expected in response to non‐posted Request, unless errors pre‐ vent them. For example Memory, IO, or Configuration Read requests usually result in Completions with data. On the other hand, IO or Configuration Write requests usually result in a completion without data that merely reports the sta‐ tus of the transaction. 

Many fields in the Completion use the same values as the associated request, including Traffic Class, Attribute bits, and the original Requester ID (used to route the completion back to the Requester). Figure 5‐10 on page 197 shows a completion returned for a non‐posted request, and the 3DW header format it uses. Completions also supply the Completer ID in the header. Completer ID is not interesting during normal operation, but knowing where the Completion came from could be useful for error diagnosis during system debug. 

**196** 

**Chapter 5: TLP Elements** 

_Figure 5‐10:  3DW Completion Header Format_ 

**==> picture [364 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Switch<br>Non-Posted<br>Request Completion TLP<br>PCIe Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 1 0 1 0Type R TC R Attr R TH0 DT EP Attr 0 0AT Length<br>Byte 4 Completer ID Compl.Status MCB Byte Count<br>Byte 8 Requester ID Tag R Lower Address<br>**----- End of picture text -----**<br>


**Definitions Of Completion Header Fields.** Table 5‐7 on page 197 describes the location and use of each field in a completion header. 

_Table 5‐7: Completion Header Fields_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Format (always a 3DW header)<br>000b = Completion without data (Cpl)<br>010b = Completion with data (CplD)|

</td>
<td style="background-color:#e8e8e8">

|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|指示是否已包含 TLP Hints。有关这些 hints 的讨论，请参见第 899 页 "TPH (TLP Processing Hints)"。|
|---|---|---|

**189**

## **PCI Express Technology**

*Table 5‐5: 4DW Memory Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**||**Function**|
|---|---|---|---|
|TD<br>(TLP Digest)|Byte 2 Bit 7||如果为 1，则该 TLP 包含可选的 TLP Digest 字段。<br>一些规则：<br>所有接收方必须使用此位检查 Digest 字段是否存在<br>• TD = 1 但没有 Digest 字段的 TLP 将被视为 Malformed<br>• 如果设置了 TD 位，则接收方必须在启用时执行 ECRC 检查<br>• 如果接收方不支持可选的 ECRC 检查，则必须忽略 digest 字段|
|EP<br>(Poisoned Data)|Byte 2 Bit 6||如果为 1，则尽管事务被允许正常完成，但伴随此包的数据应被视为有错误。|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4||Bit 5=Relaxed ordering<br>。<br>当设置为 = 1 时，启用此 TLP 的 PCI‐X 宽松排序。否则使用严格的 PCI 排序。<br>Bit 4=No Snoop<br>。<br>如果为 1，则系统硬件不需要为此 TLP 触发处理器缓存窥探以保证一致性。否则需要缓存窥探。|
|Address Type [1:0]|Byte 2 Bit 3:2||此字段支持虚拟化系统的地址转换。转换协议在名为_Address Translation Services_的单独规范中描述，可以看到该字段编码如下：<br>00 = Default/Untranslated<br>01 = Translation Request<br>10 = Translated<br>11 = Reserved|

**190**

**Chapter 5: TLP Elements**

*Table 5‐5: 4DW Memory Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|TLP 数据负载传输大小，以 DW 为单位。最大为 1024 DW (4KB)，编码为：<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识 Requester 的完成返回地址：<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|这些标识 Requester 发出的每个未完成请求。默认仅使用位 4:0，允许同时进行 32 个请求。如果 Control 寄存器中的 Extended Tag 位被设置，则可以使用全部 8 位（256 个 tag）。|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|这些限定传输的最后一个 DW 中的字节。|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|这些限定数据负载的第一个 DW 中的字节。|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|内存传输的 64 位起始地址的高 32 位。|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|内存传输的 64 位起始地址的低 32 位。地址的低 2 位被保留，强制为 DW 对齐的起始地址。|

**191**

## **PCI Express Technology**

**Memory Request Notes.** 内存请求的特性包括：

1. 内存数据传输不允许跨越 4KB 边界。

2. 所有内存映射写都是 Posted（已发布）以提升性能。

3. 可以使用 32 位或 64 位寻址。

4. 数据负载大小在 0 到 1024 DW (0‐4KB) 之间。

5. 可以使用 QoS 特性，包括最多 8 个 Traffic Class。

6. 当事务目标是主内存时，可以使用 No Snoop 属性来免除系统窥探处理器缓存的需要。

7. 可以使用 Relaxed Ordering 属性来允许包路径中的设备应用宽松排序规则，以期提高性能。

## **Configuration Requests**

PCI Express 使用与 PCI 相同的 Type 0 和 Type 1 配置请求来保持向后兼容性。Type 1 周期向下游传播，直到到达其 secondary bus 与目标 bus 匹配的桥为止。在那时，配置事务由该桥从 Type 1 转换为 Type 0。桥根据先前编程的总线号寄存器（Primary、Secondary 和 Subordinate Bus Numbers）知道何时转发和转换配置周期。有关此主题的更多信息，请参见第 91 页 "Legacy PCI Mechanism" 一节。

**192**

**Chapter 5: TLP Elements**

*Figure 5‐9: 3DW Configuration Request And Header Format*

**==> picture [368 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Type 1<br> Configuration Request<br>Switch<br>Type 0<br> Configuration Request Configuration Request TLP<br>Framing Sequence Framing<br>PCIe Header Data Digest LCRC<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 1 0 xType R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Bus Number Device Func Rsvd Ext Reg Register R<br>Function Number with ARI Number Number<br>**----- End of picture text -----**<br>


在第 193 页的图 5‐9 中，显示了一个 Type 1 配置周期向下游传播，并由该总线的桥将其转换为 Type 0（通过改变 Type 字段的位 0 实现）。请注意，与 PCI 不同的是，一个链路上只能驻留一个下游设备。因此，不需要 IDSEL 或其他硬件指示来告知设备应该认领 Type 0 周期；任何在其上游链路上看到的 Type 0 配置周期都将被理解为针对该设备。

**Definitions Of Configuration Request Header Fields.** 第 194 页的表 5‐6 描述了图 5‐9 中所示的配置请求头中每个字段的位置和用途。

**193**

## **PCI Express Technology**

*Table 5‐6: Configuration Request Header Fields*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|始终是 3DW 头<br>000b = configuration read (no data)<br>010b = configuration write (with data)|
|Type [4:0]|Byte 0 Bit 4:0|00100b = Type 0 Config Request<br>00101b = Type 1 Config Request|
|TC [2:0]<br>(Transfer Class)|Byte 1 Bit 6:4|对于 Config 请求，Traffic Class 必须为零，确保这些包永远不会干扰任何高优先级包。|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|对于 Config 请求，这些位被保留且必须为零。|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||
|TD<br>(TLP Digest)|Byte 2 Bit 7|指示 TLP 末端存在 digest 字段（1 DW）。|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|指示数据负载已被 poison。|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|在配置请求中，Relaxed Ordering 和 No Snoop 位始终 = 0。|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|对于配置请求，Address Type 被保留且必须为零。|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|对于配置请求，DW 中的数据负载大小始终 = 1。Byte Enables 限定 DW 中的字节，任何组合都是合法的。|

**194**

**Chapter 5: TLP Elements**

*Table 5‐6: Configuration Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识 Requester 的完成返回地址：<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|这些位标识 Requester 发出的未完成请求。默认情况下，仅使用位 4:0（同时 32 个未完成事务），但如果 Control 寄存器中的 Extended Tag 位设置为 = 1，则可以使用全部 8 位（256 个 tag）。|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|这些限定传输的最后一个数据 DW 中的字节。由于配置请求只能是一个 DW 大小，这些位必须为零。|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|这些高有效位限定传输的第一个数据 DW 中的字节。对于配置请求，任何位组合都是有效的（包括没有任何 active 的情况）。|
|Completer ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|标识正在通过此配置周期访问的 Completer。<br>Byte 8, 7:0 = Bus Number<br>Byte 9, 7:3 = Device Number<br>Byte 9, 2:0 = Function Number|
|Ext Register Number<br>[3:0]<br>(Extended Register<br>Number)|Byte 10 Bit 3:0|这些提供用于访问扩展配置空间的 DW 空间的高 4 位。它们与 Register Number 组合形成访问 1024 DW (4096 字节) 空间所需的 10 位地址。对于 PCI 兼容的配置空间，此字段必须为零。|

**195**

## **PCI Express Technology**

*Table 5‐6: Configuration Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Register Number [5:0]|Byte 11 Bit 7:0|作为配置 DW 空间的低 8 位，这些指定寄存器号。最低两位始终为零，强制 DW 对齐访问。|

**Configuration Request Notes.** 配置请求始终使用 3DW 头格式，并根据目标 Bus、Device 和 Function 号进行路由。所有设备在收到 Type 0 配置写周期时都会从请求中的目标号"捕获"自己的 Bus 和 Device 号。之所以这样做，是因为它们以后在发出自己的请求时需要将其用作 Requester ID。

## **Completions**

除非出现错误阻止，否则预期 Non‐posted 请求会有完成响应。例如 Memory、IO 或 Configuration Read 请求通常会产生带数据的完成。另一方面，IO 或 Configuration Write 请求通常会产生不带数据的完成，仅报告事务的状态。

完成中的许多字段使用与相应请求相同的值，包括 Traffic Class、Attribute 位以及原始 Requester ID（用于将完成路由回 Requester）。第 197 页的图 5‐10 显示了为 Non‐posted 请求返回的完成及其使用的 3DW 头格式。完成还在头中提供 Completer ID。Completer ID 在正常操作期间并不重要，但在系统调试期间知道完成来自何处可能对错误诊断有用。

**196**

**Chapter 5: TLP Elements**

*Figure 5‐10:  3DW Completion Header Format*

**==> picture [364 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Switch<br>Non-Posted<br>Request Completion TLP<br>PCIe Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 1 0 1 0Type R TC R Attr R TH0 DT EP Attr 0 0AT Length<br>Byte 4 Completer ID Compl.Status MCB Byte Count<br>Byte 8 Requester ID Tag R Lower Address<br>**----- End of picture text -----**<br>


**Definitions Of Completion Header Fields.** 第 197 页的表 5‐7 描述了完成头中每个字段的位置和用途。

*Table 5‐7: Completion Header Fields*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|包格式（始终是 3DW 头）<br>000b = Completion without data (Cpl)<br>010b = Completion with data (CplD)|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-12"></a>
## 5.12 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Type [4:0]|Byte 0 Bit 4:0|Packet type is 01010b for Completions.|



**197** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐7: Completion Header Fields (Continued)_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Completions must use the same value<br>here as the corresponding Request.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|Indicates whether ID‐based Ordering is<br>to be used for this TLP. To learn more,<br>see “ID Based Ordering (IDO)” on<br>page 301.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|Reserved for Completions.|
|TD<br>(TLP Digest)|Byte 2 Bit 7|If = 1, indicates the presence of a<br>digest field at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|If = 1, indicates the data payload is poi‐<br>soned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Completions must use the same values<br>here as the corresponding Request.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type is reserved for Comple‐<br>tions and must be zero, but Receivers<br>are not required or even encouraged to<br>check this.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW. For<br>Completions, this field reflects the size<br>of the data payload associated with this<br>completion.|
|Completer ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Completer to support<br>debugging problems.<br>Byte 4 7:0 = Completer Bus #<br>Byte 5 7:3 = Completer Dev #<br>Byte 5 2:0 = Completer Function #|



**198** 

**Chapter 5: TLP Elements** 

_Table 5‐7: Completion Header Fields (Continued)_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Compl. Status [2:0]<br>(Completion Status<br>Code)|Byte 6 Bit 7:5|These bits indicate status for this Com‐<br>pletion.<br>000b = Successful Completion (SC)<br>001b = Unsupported Request (UR)<br>010b = Config Req Retry Status (CRS)<br>100b = Completer abort (CA)<br>All other codes are reserved. See “Sum‐<br>mary of Completion Status Codes” on<br>page 200.|
|BCM<br>(Byte Count Modified)|Byte 6 Bit 4|This is only used by PCI‐X Completers<br>and indicates that the Byte Count field<br>reports only the first payload rather<br>than the total payload remaining. See<br>“Using The Byte Count Modified Bit”<br>on page 201.|
|Byte Count [11:0]|Byte 6 Bit 3:0<br>Byte 7 Bit 7:0|Byte count remaining to satisfy a read<br>request, as derived from the original<br>request Length field. See “Data<br>Returned For Read Requests:” on<br>page 201 for special cases caused by<br>multiple completions.|
|Requester ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|Copied from the Request for use as the<br>return address (target) for this Comple‐<br>tion.<br>Byte 8, 7:0 = Requester Bus #<br>Byte 9, 7:3 = Requester Device #<br>Byte 9, 2:0 = Requester Function #|
|Tag [7:0]|Byte 10 Bit 7:0|This must be the Tag value received<br>with the Request. Requester associates<br>this Completion with a pending<br>Request based on the Tag.|



**199** 

**PCI Ex ress Technolo p gy** 

_Table 5‐7: Completion Header Fields (Continued)_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Lower Address [6:0]|Byte 11 Bit 6:0|The lower 7 bits of address for the first<br>data returned for a read request. Calcu‐<br>lated from Request Length and Byte<br>Enables, it assists buffer management<br>by showing how many bytes can be<br>transferred before reaching the next<br>Read Completion Boundary. See “Cal‐<br>culating Lower Address Field” on<br>page 200.|



## **Summary of Completion Status Codes.** 

- 000b (SC) Successful Completion: the Request was serviced properly. 

- 001b (UR) Unsupported Request: Request is not legal or was not recognized by the Completer. This is an error condition but how the Completer responds depends on the spec revision to which it was designed. Before the 1.1 spec, this were considered an uncorrectable error, but for 1.1 and later it’s treated as an Advisory Non‐Fatal Error. See the “Unsupported Request (UR) Status” on page 663 for details. 

- 010b (CRS) Configuration Request Retry Status: Completer is temporarily unable to service a configuration request, and the request should be attempted again later. 

- 100b (CA) Completer Abort: Completer should have been able to service the request but has failed for some reason. This is an uncorrectable error. 

**Calculating The Lower Address Field .** This field is set up by the Com‐ pleter to reflect the byte‐aligned address of the first enabled byte of data being returned in the Completion payload. Hardware calculates this by considering both the DW start address and the Byte Enable pattern in the First DW Byte Enable field provided in the original request. 

For Memory Read Requests, the address is an offset from the DW start address: 

- If the First DW Byte Enable field is 1111b, all bytes are enabled in the first DW and the offset is 0. This field matches the DW‐aligned start address. 

- If the First DW Byte Enable field is 1110b, the upper three bytes are enabled in the first DW and the offset is 1. This field is the DW start address + 1. 

- If the First DW Byte Enable field is 1100b, the upper two bytes are enabled 

**200** 

**Chapter 5: TLP Elements** 

- in the first DW and the offset is 2. This field is the DW start address + 2. 

- • If the First DW Byte Enable field is 1000b, only the upper byte is enabled in the first DW and the offset is 3. This field is the DW start address + 3. 

Once calculated, the lower 7 bits are placed in the Lower Address field of the Completion header to facilitate the case in which the read completion is smaller than the entire payload and needs to stop at the first RCB. Breaking a transac‐ tion must be done on RCBs, and the number of bytes transferred to reach the first one is based on start address. 

For AtomicOp Completions, the Lower Address field is reserved. For all other Completion types, it’s set to zero. 

**Using The Byte Count Modified Bit.** This bit is only set by PCI‐X Com‐ pleters, but they could exist in a PCIe topology if a bridge from PCIe to PCI‐X is used. Rules for its assertion include: 

1. It’s only set by a PCI‐X Completer if a read request is going to be broken into multiple completions. 

2. It’s only set for the first Completion of the series, and only then to indicate that the first Completion contains a Byte Count field that reflects the first Completion payload rather than the total remaining (as it normally would). The Requester understands that, even though the Byte Count appears to show that this is the last Completion for this request, this Completion will instead be followed by others to satisfy the original request as required. 

3. For subsequent Completions in the series, the BCM bit must be deasserted and the Byte Count field will reflect the total remaining count as it normally would. 

4. Devices receiving Completions with the BCM bit set must interpret this case properly. 

5. The Lower Address field is set by the Completer during completions with data to reflect the address of the first enabled byte of data being returned 

## **Data Returned For Read Requests:** 

1. A read request may require multiple completions to be fulfilled, but total data transfer must eventually equal the size of original request, or a Com‐ pletion Timeout error will probably result. 

2. A given Completion can only service one Request. 

3. IO and Configuration reads are always 1 DW, and will always be satisfied with a single Completion 

4. A Completion with a Status Code other than SC (successful) terminates a transaction. 

**201** 

## **PCI Ex ress Technolo p gy** 

5. The Read Completion Boundary (RCB) must be observed when handling a read request with multiple completions. The RCB is 64 bytes or 128 bytes for the Root Complex, since it is allowed to modify the size of packets flow‐ ing between its ports, and the value used is visible in a configuration regis‐ ter. 

6. Bridges and endpoints may implement a bit for selecting the RCB size (64 or 128 bytes) under software control. 

7. Completions that are entirely within an aligned RCB boundary must com‐ plete in one transfer, since the transfer won’t reach the RCB, which is the only place it can legally stop early. 

8. Multiple Completions for a single read request must return data in increas‐ ing address order. 

## **Receiver Completion Handling Rules:** 

1. A received Completion that doesn’t match a pending request is an Unex‐ pected Completion and treated as an error. 

2. Completions with a completion status other than SC or CRS will be handled as errors and buffer space associated with them will be released. 

3. When the Root Complex receives a CRS status during a configuration cycle, the request is terminated. What happens next is implementation specific, but if the Root supports it, the action is defined by the setting of its CRS Software Visibility bit in the Root Control register. 

   - If CRS Software Visibility is not enabled, the Root will reissue the config request for an implementation‐specific number of times before giving up and concluding the target has a problem. 

   - If CRS Software Visibility is enabled, software designed to support it will always read both bytes of the Vendor ID field first. If the hardware then receives a CRS for that Request, it returns the value 0001h for the Vendor ID. This value, reserved for this use by the PCI‐SIG, doesn’t cor‐ respond to any valid Vendor ID and informs software about this event. This allows software to go on to some other task while waiting for the target to become ready (which could take as long as 1 second after reset) rather than being stalled. Any other config read or write will simply be automatically retried by the Root as a new Request for the design‐spe‐ cific number of iterations. 

4. A CRS status in response to a request other than configuration is illegal and may be reported as a Malformed TLP. 

5. Completions with status = reserved code are treated as if the code was UR. 6. If a Read Completion or an AtomicOp Completion is received with a status other than SC, no data is included with the completion and the Requester must consider this Request terminated. How the Requester handles this case is implementation‐specific. 

**202** 

**Chapter 5: TLP Elements** 

7. In the event multiple completions are being returned for a read request, a completion status other than SC ends the transaction. Device handling of data received prior to the error is implementation‐specific. 

8. For compatibility with PCI, a Root Complex may be required to synthesize a read value of all “1’s” when a configuration cycle ends with a completion indicating an Unsupported Request. This is analogous to a PCI Master Abort that happens when enumeration software attempts to read from devices that are not present. 

## **Message Requests** 

Message Requests replace many of the interrupt, error, and power management sideband signals used on PCI and PCI‐X. All Message Requests use the 4DW header format, but not all of the fields are used in every Message type. Fields in bytes 8 through 15 are not defined for some Messages and are reserved for those cases. Messages are treated much like posted Memory Write transactions but their routing can be based on address, ID, and in some cases the routing can be implicit. The _routing subfield_ (Byte 0, bits 2:0) in the packet header indicates which routing method is used and which additional header registers are defined. The general Message Request header format is shown in Figure 5‐11 on page 203. 

_Figure 5‐11: 4DW Message Request Header Format_

</td>
<td style="background-color:#e8e8e8">

|Type [4:0]|Byte 0 Bit 4:0|对于 Completion，包类型是 01010b。|

**197**

## **PCI Express Technology**

*Table 5‐7: Completion Header Fields (Continued)*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Completion 必须在此处使用与相应 Request 相同的值。|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|指示此 TLP 是否使用基于 ID 的排序。要了解更多信息，请参见第 301 页 "ID Based Ordering (IDO)"。|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|对于 Completion 是保留的。|
|TD<br>(TLP Digest)|Byte 2 Bit 7|如果 = 1，指示 TLP 末端存在 digest 字段。|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|如果 = 1，指示数据负载已被 poison。|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Completion 必须在此处使用与相应 Request 相同的值。|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|对于 Completion，Address Type 是保留的且必须为零，但不要求甚至不建议接收方检查此字段。|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|指示 DW 中的数据负载大小。对于 Completion，此字段反映与此完成相关联的数据负载大小。|
|Completer ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识 Completer 以支持问题调试。<br>Byte 4 7:0 = Completer Bus #<br>Byte 5 7:3 = Completer Dev #<br>Byte 5 2:0 = Completer Function #|

**198**

**Chapter 5: TLP Elements**

*Table 5‐7: Completion Header Fields (Continued)*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Compl. Status [2:0]<br>(Completion Status<br>Code)|Byte 6 Bit 7:5|这些位指示此 Completion 的状态。<br>000b = Successful Completion (SC)<br>001b = Unsupported Request (UR)<br>010b = Config Req Retry Status (CRS)<br>100b = Completer abort (CA)<br>所有其他代码均保留。请参见第 200 页 "Summary of Completion Status Codes"。|
|BCM<br>(Byte Count Modified)|Byte 6 Bit 4|这仅由 PCI‐X Completer 使用，指示 Byte Count 字段仅报告第一个负载而不是剩余的总负载。请参见第 201 页 "Using The Byte Count Modified Bit"。|
|Byte Count [11:0]|Byte 6 Bit 3:0<br>Byte 7 Bit 7:0|满足读请求的剩余字节数，由原始请求的 Length 字段派生。请参见第 201 页 "Data Returned For Read Requests:" 了解由多个完成引起的特殊情况。|
|Requester ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|从 Request 复制，用作此 Completion 的返回地址（目标）。<br>Byte 8, 7:0 = Requester Bus #<br>Byte 9, 7:3 = Requester Device #<br>Byte 9, 2:0 = Requester Function #|
|Tag [7:0]|Byte 10 Bit 7:0|这必须是随 Request 接收的 Tag 值。Requester 根据 Tag 将此 Completion 与挂起的 Request 关联。|

**199**

**PCI Express Technology**

*Table 5‐7: Completion Header Fields (Continued)*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Lower Address [6:0]|Byte 11 Bit 6:0|为读请求返回的第一个数据的字节对齐地址的低 7 位。由 Request 的 Length 和 Byte Enables 计算得出，它通过显示在到达下一个 Read Completion Boundary 之前可以传输多少字节来协助缓冲区管理。请参见第 200 页 "Calculating Lower Address Field"。|

## **Summary of Completion Status Codes.**

- 000b (SC) Successful Completion：请求被正确服务。

- 001b (UR) Unsupported Request：请求不合法或未被 Completer 识别。这是一种错误情况，但 Completer 的响应方式取决于其设计所遵循的规范修订版本。在 1.1 规范之前，这被视为不可纠正的错误，但对于 1.1 及更高版本，它被视为 Advisory Non‐Fatal Error。详见第 663 页 "Unsupported Request (UR) Status"。

- 010b (CRS) Configuration Request Retry Status：Completer 暂时无法服务配置请求，应在稍后重试该请求。

- 100b (CA) Completer Abort：Completer 本应能够服务该请求但出于某种原因失败。这是一种不可纠正的错误。

**Calculating The Lower Address Field.** 此字段由 Completer 设置，以反映完成负载中返回的第一个已启用数据字节的字节对齐地址。硬件通过考虑 DW 起始地址和原始请求中 First DW Byte Enable 字段中提供的 Byte Enable 模式来计算此值。

对于 Memory Read 请求，地址是 DW 起始地址的偏移量：

- 如果 First DW Byte Enable 字段为 1111b，则第一个 DW 中的所有字节都被启用，偏移量为 0。此字段与 DW 对齐的起始地址匹配。

- 如果 First DW Byte Enable 字段为 1110b，则第一个 DW 中的高三字节被启用，偏移量为 1。此字段是 DW 起始地址 + 1。

- 如果 First DW Byte Enable 字段为 1100b，则第一个 DW 中的高二字节被启用

**200**

**Chapter 5: TLP Elements**

- 在第一个 DW 中，偏移量为 2。此字段是 DW 起始地址 + 2。

- • 如果 First DW Byte Enable 字段为 1000b，则第一个 DW 中只有高字节被启用，偏移量为 3。此字段是 DW 起始地址 + 3。

计算后，将低 7 位放入完成头的 Lower Address 字段中，以便处理读完成小于整个负载并需要在第一个 RCB 处停止的情况。事务的拆分必须在 RCB 上进行，传输到第一个 RCB 的字节数基于起始地址。

对于 AtomicOp Completion，Lower Address 字段是保留的。对于所有其他 Completion 类型，它设置为零。

**Using The Byte Count Modified Bit.** 此位仅由 PCI‐X Completer 设置，但如果使用 PCIe 到 PCI‐X 的桥，它们可能存在于 PCIe 拓扑中。其断言的规则包括：

1. 仅当读请求将被拆分为多个完成时，才由 PCI‐X Completer 设置。

2. 仅针对该系列的第一个 Completion 设置，且仅当第一个 Completion 包含反映第一个 Completion 负载（而不是总剩余负载）的 Byte Count 字段时才设置。Requester 理解，尽管 Byte Count 似乎表明这是此请求的最后一个 Completion，但实际上此 Completion 之后还会有其他 Completion 来满足原始请求的需要。

3. 对于该系列的后续 Completion，必须取消断言 BCM 位，且 Byte Count 字段将照常反映总剩余计数。

4. 接收设置了 BCM 位的 Completion 的设备必须正确解释这种情况。

5. Lower Address 字段由 Completer 在带数据的完成期间设置，以反映正在返回的第一个已启用数据字节的地址

## **Data Returned For Read Requests:**

1. 读请求可能需要多个完成才能得到满足，但总的数据传输最终必须等于原始请求的大小，否则可能会导致 Completion Timeout 错误。

2. 给定的 Completion 只能服务一个 Request。

3. IO 和 Configuration 读始终为 1 DW，并且将始终由单个 Completion 满足

4. 状态码不是 SC（成功）的 Completion 终止事务。

**201**

## **PCI Express Technology**

5. 在处理具有多个完成的读请求时必须遵守 Read Completion Boundary (RCB)。对于根复合体 (Root Complex)，RCB 为 64 字节或 128 字节，因为允许修改其端口之间流动的包的大小，并且所使用的值在配置寄存器中可见。

6. 桥和端点可以实现一个用于在软件控制下选择 RCB 大小（64 或 128 字节）的位。

7. 完全在已对齐 RCB 边界内的 Completion 必须一次传输完成，因为传输不会到达 RCB，而 RCB 是合法早期停止的唯一位置。

8. 单个读请求的多个 Completion 必须按升序地址返回数据。

## **Receiver Completion Handling Rules:**

1. 收到的与挂起请求不匹配的 Completion 是 Unexpected Completion，被视为错误。

2. 状态码不是 SC 或 CRS 的 Completion 将作为错误处理，与之关联的缓冲区空间将被释放。

3. 当根复合体在配置周期中收到 CRS 状态时，请求被终止。接下来发生什么是实现特定的，但如果根支持它，则该操作由其 Root Control 寄存器中 CRS Software Visibility 位的设置定义。

   - 如果未启用 CRS Software Visibility，根将针对实现特定的次数重新发出配置请求，然后放弃并断定目标有问题。

   - 如果启用了 CRS Software Visibility，设计为支持它的软件将始终先读取 Vendor ID 字段的两个字节。如果硬件随后收到该 Request 的 CRS，它将返回值 0001h 作为 Vendor ID。该值由 PCI‐SIG 保留用于此用途，不对应于任何有效的 Vendor ID，并将此事件通知软件。这允许软件在等待目标就绪时（可能在复位后长达 1 秒）继续执行其他任务，而不是停滞不前。任何其他配置读或写将由根作为新请求自动重试设计特定的迭代次数。

4. 对配置以外的请求的 CRS 状态是非法的，可能被报告为 Malformed TLP。

5. 状态码为保留代码的 Completion 按代码为 UR 进行处理。6. 如果收到的读完成或 AtomicOp 完成的状态不是 SC，则完成中不包含数据，Requester 必须认为此 Request 已终止。Requester 如何处理这种情况是实现特定的。

**202**

**Chapter 5: TLP Elements**

7. 在为读请求返回多个完成的情况下，状态码不是 SC 的完成将结束事务。设备对错误之前接收的数据的处理是实现特定的。

8. 为了与 PCI 兼容，当配置周期以指示 Unsupported Request 的完成结束时，根复合体可能需要合成全"1"的读值。这类似于当枚举软件尝试从未存在的设备读取时发生的 PCI Master Abort。

## **Message Requests**

Message Request 取代了 PCI 和 PCI‐X 上使用的许多中断、错误和电源管理的边带信号。所有 Message Request 都使用 4DW 头格式，但并非所有字段在每种消息类型中都被使用。第 8 到 15 字节的字段对于某些 Messages 没有定义，并在这些情况下保留。Messages 的处理方式很像 Posted Memory Write 事务，但它们的路由可以基于地址、ID，并且在某些情况下路由可以是隐式的。包头中的 _routing subfield_（Byte 0, bits 2:0）指示使用哪种路由方法以及定义了哪些附加头寄存器。通用的 Message Request 头格式显示在第 203 页的图 5‐11 中。

*Figure 5‐11: 4DW Message Request Header Format*

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-13"></a>
## 5.13 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Fmt<br>0 x 1|Type<br>1  0  r  r  r|R|TC|R|At<br>tr|R|TH<br>0|T<br>D|E<br>P|Attr<br>0 0|AT<br>0 0|Length||
||Requester ID||||||||Tag|||||Message<br>Code|
||Bytes 8-11 Vary with_Message Code_Field||||||||||||||
||Bytes 12-15 Vary with_Message Code_Field||||||||||||||



**203** 

**PCI Ex ress Technolo p gy** 

## **Message Request Header Fields.** 

_Table 5‐8: Message Request Header Fields_ 

|**Field Name**|**Header Byte/**<br>**Bit**||**Function**|
|---|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5||Packet Format. Always a 4DW header<br>001b = Message Request without data<br>011b = Message Request with data|
|Type [4:0]|Byte 0 Bit 4:0||TLP packet type field. Set to:<br>Bit 4:3:<br>10b = Msg<br>Bit 2:0<br>(Message Routing Subfield)<br>000b = Implicitly Routed to RC (Root<br>Complex)<br>001b = Routed by address<br>010b = Routed by ID<br>011b = Implicitly Broadcast from RC<br>100b = Local; terminate at receiver<br>101b = Gather & route to RC<br>0thers = Reserved, treated as Local|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4||TC is always zero for most Message<br>Requests, ensuring that they don’t inter‐<br>fere with high‐priority packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2||Indicates whether ID‐based Ordering is<br>to be used for this TLP. To learn more, see<br>“ID Based Ordering (IDO)” on page 301.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||Reserved, except as noted.|
|TD|Byte 2 Bit 7||If = 1, indicates the presence of a<br>digest field (1 DW) at the end of the TLP<br>(preceding LCRC and END)|
|EP|Byte 2 Bit 6||If = 1, indicates the data payload (if<br>present) is poisoned.|



**204** 

**Chapter 5: TLP Elements** 

_Table 5‐8: Message Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/**<br>**Bit**|**Function**|
|---|---|---|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Except as noted, these are always<br>reserved in Message Requests.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type is reserved for Messages<br>and must be zero, but Receivers are not<br>required or even encouraged to check<br>this.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW. For<br>Message Requests, this field is always 0<br>(no data) or 1 (one DW of data)|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester sending the mes‐<br>sage.<br>Byte 4, 7:0 = Requester Bus #<br>Byte 5, 7:3 = Requester Device #<br>Byte 5, 2:0 = Requester Function #|
|Tag [7:0]|Byte 6 Bit 7:0|Since all Message Requests are posted<br>and don’t receive Completions, no tag is<br>assigned to them. These bits should be<br>zero.|
|Message Code [7:0]|Byte 7 Bit 7:0|This field contains the code indicating<br>the type of message being sent.<br>0000 0000b = Unlock Message<br>0001 0000b = Lat. Tolerance Reporting<br>0001 0010b = Optimized Buffer Flush/Fill<br>0001 xxxxb = Power Mgt. Message<br>0010 0xxxb = INTx Message<br>0011 00xxb = Error Message<br>0100 xxxxb = Ignored Messages<br>0101 0000b = Set Slot Power Message<br>0111 111xb = Vendor‐Defined Messages|



**205** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐8: Message Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/**<br>**Bit**|**Function**|
|---|---|---|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|If address routing was selected for the<br>message (see Type 4:0 field above), then<br>this field contains the upper 32 bits of the<br>64 bit starting address.<br>Otherwise, this field is not used.|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|If address routing is selected (see Type<br>field above), then this field contains the<br>lower part of the 64‐bit starting address.<br>If ID routing is selected, Bytes 8 and 9<br>form the target ID.<br>Otherwise, this field is not used.|



**Message Notes:** The following tables specify the message coding used for each of the nine message groups, and is based on the message code field listed in Table 5‐8 on page 204. The defined message groups include: 

1. INTx Interrupt Signaling 

2. Power Management 

3. Error Signaling 

4. Locked Transaction Support 

5. Slot Power Limit Support 

6. Vendor‐Defined Messages 

7. Ignored Messages (related to Hot‐Plug support in spec revision 1.1) 

8. Latency Tolerance Reporting (LTR) 

9. Optimized Buffer Flush and Fill (OBFF) 

**INTx Interrupt Messages.** Many devices are capable of using the PCI 2.3 Message Signaled Interrupt (MSI) method of delivering interrupts, but older devices may not support it. For these cases, PCIe defines a “virtual wire” alter‐ native in which devices simulate the assertion and deassertion of the PCI inter‐ rupt pins (INTA‐INTD) by sending Messages. The interrupting device sends the first Message to inform the upstream device that an interrupt has been asserted. Once the interrupt has been serviced, the interrupting device sends a second Message to communicate that the signal has been released. For more on this protocol, refer to the section called “Virtual INTx Signaling” on page 805 for details. 

**206** 

**Chapter 5: TLP Elements** 

_Table 5‐9: INTx Interrupt Signaling Message Coding_ 

|**INTx Message**|**Message**<br>**Code 7:0**|**Routing 2:0**|
|---|---|---|
|Assert_INTA|0010 0000b|100b<br>(Local ‐<br>Terminate at Rx)|
|Assert_INTB|0010 0001b||
|Assert_INTC|0010 0010b||

</td>
<td style="background-color:#e8e8e8">

|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Fmt<br>0 x 1|Type<br>1  0  r  r  r|R|TC|R|At<br>tr|R|TH<br>0|T<br>D|E<br>P|Attr<br>0 0|AT<br>0 0|Length||
||Requester ID||||||||Tag|||||Message<br>Code|
||Bytes 8-11 Vary with_Message Code_Field||||||||||||||
||Bytes 12-15 Vary with_Message Code_Field||||||||||||||

**203**

**PCI Express Technology**

## **Message Request Header Fields.**

*Table 5‐8: Message Request Header Fields*

|**Field Name**|**Header Byte/**<br>**Bit**||**Function**|
|---|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5||包格式。始终是 4DW 头<br>001b = Message Request without data<br>011b = Message Request with data|
|Type [4:0]|Byte 0 Bit 4:0||TLP 包类型字段。设置为：<br>Bit 4:3：<br>10b = Msg<br>Bit 2:0<br>(Message Routing Subfield)<br>000b = Implicitly Routed to RC (Root Complex)<br>001b = Routed by address<br>010b = Routed by ID<br>011b = Implicitly Broadcast from RC<br>100b = Local; terminate at receiver<br>101b = Gather & route to RC<br>其他 = 保留，视为 Local|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4||对于大多数 Message Request，TC 始终为零，确保它们不干扰高优先级包。|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2||指示此 TLP 是否使用基于 ID 的排序。要了解更多信息，请参见第 301 页 "ID Based Ordering (IDO)"。|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||保留，除非另有说明。|
|TD|Byte 2 Bit 7||如果 = 1，指示 TLP 末端（紧接 LCRC 和 END 之前）存在 digest 字段（1 DW）。|
|EP|Byte 2 Bit 6||如果 = 1，指示数据负载（如果存在）已被 poison。|

**204**

**Chapter 5: TLP Elements**

*Table 5‐8: Message Request Header Fields (Continued)*

|**Field Name**|**Header Byte/**<br>**Bit**|**Function**|
|---|---|---|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|除另有说明外，在 Message Request 中这些位始终保留。|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|对于 Message，Address Type 是保留的且必须为零，但不要求甚至不建议接收方检查此字段。|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|指示 DW 中的数据负载大小。对于 Message Request，此字段始终为 0（无数据）或 1（一 DW 数据）。|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识发送消息的 Requester。<br>Byte 4, 7:0 = Requester Bus #<br>Byte 5, 7:3 = Requester Device #<br>Byte 5, 2:0 = Requester Function #|
|Tag [7:0]|Byte 6 Bit 7:0|由于所有 Message Request 都是 posted 的且不接收 Completions，因此不为其分配 tag。这些位应为零。|
|Message Code [7:0]|Byte 7 Bit 7:0|此字段包含指示所发送消息类型的代码。<br>0000 0000b = Unlock Message<br>0001 0000b = Lat. Tolerance Reporting<br>0001 0010b = Optimized Buffer Flush/Fill<br>0001 xxxxb = Power Mgt. Message<br>0010 0xxxb = INTx Message<br>0011 00xxb = Error Message<br>0100 xxxxb = Ignored Messages<br>0101 0000b = Set Slot Power Message<br>0111 111xb = Vendor‐Defined Messages|

**205**

## **PCI Express Technology**

*Table 5‐8: Message Request Header Fields (Continued)*

|**Field Name**|**Header Byte/**<br>**Bit**|**Function**|
|---|---|---|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|如果为消息选择了地址路由（参见上面的 Type 4:0 字段），则此字段包含 64 位起始地址的高 32 位。<br>否则，不使用此字段。|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|如果选择了地址路由（参见上面的 Type 字段），则此字段包含 64 位起始地址的低部分。<br>如果选择了 ID 路由，则 Byte 8 和 9 构成目标 ID。<br>否则，不使用此字段。|

**Message Notes:** 下表指定了九个消息组中每个组使用的消息编码，基于第 204 页表 5‐8 中列出的消息代码字段。已定义的消息组包括：

1. INTx 中断信令

2. 电源管理

3. 错误信令

4. Locked Transaction 支持

5. Slot Power Limit 支持

6. 供应商定义消息

7. Ignored Messages（与规范修订 1.1 中的热插拔支持相关）

8. Latency Tolerance Reporting (LTR)

9. Optimized Buffer Flush and Fill (OBFF)

**INTx Interrupt Messages.** 许多设备能够使用 PCI 2.3 Message Signaled Interrupt (MSI) 方法传递中断，但较旧的设备可能不支持。对于这些情况，PCIe 定义了一种"虚拟线路"替代方案，其中设备通过发送 Messages 来模拟 PCI 中断引脚（INTA‐INTD）的断言和取消断言。中断设备发送第一个 Message 通知上游设备已断言中断。一旦中断被服务，中断设备发送第二个 Message 通信信号已释放。有关此协议的更多信息，请参见第 805 页 "Virtual INTx Signaling" 一节。

**206**

**Chapter 5: TLP Elements**

*Table 5‐9: INTx Interrupt Signaling Message Coding*

|**INTx Message**|**Message**<br>**Code 7:0**|**Routing 2:0**|
|---|---|---|
|Assert_INTA|0010 0000b|100b<br>(Local ‐<br>Terminate at Rx)|
|Assert_INTB|0010 0001b||
|Assert_INTC|0010 0010b||

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-14"></a>
## 5.14 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Assert_INTD|0010 0011b||
|Deassert_INTA|0010 0100b||
|Deassert_INTB|0010 0101b||
|Deassert_INTC|0010 0110b||
|Deassert_INTD|0010 0111b||



Rules regarding the use of INTx Messages: 

1. They have no data payload and so the Length field is reserved. 

2. They’re only issued by Upstream Ports. Checking this rule for received packets is optional but, if checked, violations will be handled as Malformed TLPs. 

3. They’re required to use the default traffic class TC0. Receivers must check for this and violations will be handled as Malformed TLPs. 

4. Components at both ends of the Link must track the current state of the four virtual interrupts. If the logical state of one interrupt changes at the Upstream Port, it must send the appropriate INTx message. 

5. INTx signaling is disabled when the Interrupt Disable bit of the Command Register is set = 1 (as would be the case for physical interrupt lines). 

6. If any virtual INTx signals are active when the Interrupt Disable bit is set in the device, the Upstream Port must send corresponding Deassert_INTx messages. 

7. Switches must track the state of the four INTx signals independently for each Downstream Port and combine the states for the Upstream Port. 

8. The Root Complex must track the state of the four INTx lines indepen‐ dently and convert them into system interrupts in an implementation‐spe‐ cific way. 

**207** 

## **PCI Ex ress Technolo p gy** 

9. They use the routing type “Local‐Terminate at Receiver” to allow a Switch to remap the designated interrupt pin when necessary (see “Mapping and Collapsing INTx Messages” on page 808). Consequently, the Requester ID in an INTx message may be assigned by the last transmitter. 

**Power Management Messages.** PCI Express is compatible with PCI power management, and adds hardware‐based Link power management as well. Messages are used to convey some of this information, but to learn how the overall PCIe power management protocol works, refer to Chapter 16, enti‐ tled ʺPower Management,ʺ on page 703. Table 5‐10 on page 208 summarizes the four power management message types. 

_Table 5‐10: Power Management Message Coding_ 

|**Power Management Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|PM_Active_State_Nak|0001 0100b|100b|
|PM_PME|0001 1000b|000b|
|PM_Turn_Off|0001 1001b|011b|
|PME_TO_Ack|0001 1011b|101b|



Power Management Message Rules: 

1. Power Management Messages don’t have a data payload, so the Length field is reserved. 

2. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

3. PM_Active_State_Nak is sent from a Downstream Port after it observes a request from the Link neighbor to change the Link power state to L1 but it has chosen not to do so (Local ‐ Terminate at Receiver routing). 

4. PM_PME is sent upstream by the component requesting a Power Manage‐ ment Event (Implicitly Routed to the Root Complex). 

5. PM_Turn_Off is sent downstream to all endpoints (Implicitly Broadcast from the Root Complex routing). 

6. PME_TO_Ack is sent upstream by endpoints. For switches with multiple Downstream Ports, this message won’t be forwarded upstream until all Downstream Ports have received it (Gather and Route to the Root Complex routing). 

**208** 

**Chapter 5: TLP Elements** 

**Error Messages.** Error Messages are sent upstream (Implicitly Routed to the Root Complex) by enabled components that detect errors. To assist software in knowing how to service the error, the Error Message identifies the requesting agent in the Requester ID field of the message header. Table 5‐11 on page 209 describes the three error message types. 

_Table 5‐11: Error Message Coding_ 

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|ERR_COR (Correctable)|0011 0000b|000b|
|ERR_NONFATAL<br>(Uncorrectable, Non‐fatal)|0011 0001b||
|ERR_FATAL<br>(Uncorrectable, Fatal)|0011 0011b||



Error Signaling Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, so the Length field is reserved. 

3. The Root Complex converts Error Messages into system‐specific events. 

**Locked Transaction Support.** The Unlock Message is used as part of the Locked transaction protocol defined for PCI and still available to Legacy Devices. The protocol begins with a Memory Read Locked Request. When that Request is seen by Ports along the path to the target device, they implement an atomic read‐modify‐write protocol by locking out other Requesters from using VC0 until the Unlock Message is received. This Message is sent to the target to release all the Ports in the path to it and finish the Locked Transaction sequence. Table 5‐12 on page 209 summarizes the coding for this message. 

_Table 5‐12: Unlock Message Coding_ 

|**Unlock Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Unlock|0000 0000b|011b|



**209** 

**PCI Ex ress Technolo p gy** 

Unlock Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

**Set Slot Power Limit Message.** This is sent from a Downstream Port to the device plugged into the slot. This power limit is stored in the endpoint in its Device Capabilities Register. Table 5‐13 summarizes the message coding. 

_Table 5‐13: Slot Power Limit Message Coding_ 

|**Slot Power Limit Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Set_Slot_Power_Limit|0101 0000b|100b|



Set_Slot_Power_Limit Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. The data payload is 1 DW and so the Length field is set to one. Only the lower 10 bits of the 32‐bit data payload are used for slot power scaling; the upper payload bits must be set to zero. 

3. This message is sent automatically anytime the Data Link Layer transitions to DL_Up status or if a configuration write to the Slot Capabilities Register occurs while the Data Link Layer is already reporting DL_Up status. 

4. If the card in the slot already consumes less power than the power limit specified, it’s allowed to ignore the Message. 

**Vendor‐Defined Message 0 and 1.** These are intended to allow expan‐ sion of the PCIe messaging capabilities either by the spec or by vendor‐specific extensions. The header for them is shown in Figure 5‐12 on page 211, and the codes are given in Figure 5‐14 on page 211. 

**210** 

**Chapter 5: TLP Elements** 

_Figure 5‐12: Vendor‐Defined Message Header_ 

**==> picture [368 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 1Fmt 1  0  r  r  rType R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 1 1 1 1 1 1 x<br>Byte 8 Target BDF if ID Routing used, Vendor ID<br>otherwise Reserved<br>Byte 12 For Vendor Definition<br>**----- End of picture text -----**<br>


_Table 5‐14: Vendor‐Defined Message Coding_ 

|**Vendor‐Defined Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Vendor Defined Message 0|0111 1110b|000b, 010b,<br>011b, 100b|
|Vendor Defined Message 1|0111 1111b||



Vendor‐Defined Message Rules: 

1. A data payload may or may not be included with either type. 

2. Messages are distinguished by the Vendor ID field. 

3. Attribute bits [2] and [1:0] are not reserved. 

4. If the Receiver doesn’t recognize the Message: 

   - Type 1 Messages are silently discarded 

   - Type 0 Messages are treated as an Unsupported Request error condi‐ tion 

**Ignored Messages.** Listing an entire category of Messages that are to be ignored sounds a little strange without the context for it. These were formerly Hot Plug Signaling messages that supported devices that had Hot Plug indica‐ tors and push buttons on the add‐in card itself rather than on the system board. This Message type was defined through spec rev 1.0a, but this option was no longer supported beginning with the 1.1 spec release, so the details are only included here for reference. As the name now suggests, Transmitters are 

**211** 

**PCI Ex ress Technolo p gy** 

strongly encouraged not to send these messages, and Receivers are strongly encouraged to ignore them if they are seen. If they’re still going to be used any‐ way, they must conform to the 1.0a spec details. 

_Table 5‐15: Hot Plug Message Coding_ 

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Attention_Indicator_On|0100 0001b|100b|
|Attention_Indicator_Blink|0100 0011b|100b|
|Attention_Indicator_Off|0100 0000b|100b|
|Power_Indicator_On|0100 0101b|100b|
|Power_Indicator_Blink|0100 0111b|100b|
|Power_Indicator_Off|0100 0100b|100b|
|Attention_Button_Pressed|0100 1000b|100b|



Hot Plug Message Rules: 

- They are driven by a Downstream Port to the card in the slot. 

- The Attention Button Message is driven upstream by a slot device. 

**Latency Tolerance Reporting Message.** LTR Messages are used to optionally report acceptable read/write service latencies for a device. To learn more about this power management technique, see the section called “LTR (Latency Tolerance Reporting)” on page 784. 

_Figure 5‐13: LTR Message Header_ 

**==> picture [346 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1 0 0 0 0<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>**----- End of picture text -----**<br>


**212** 

**Chapter 5: TLP Elements** 

_Table 5‐16: LTR Message Coding_ 

|**Latency Tolerance Reporting Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|LTR|0001 0000|100|



LTR Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

**Optimized Buffer Flush and Fill Messages.** OBFF Messages are used to report platform power status to Endpoints and facilitate more effective sys‐ tem power management. To learn more about this technique, see the discussion called “OBFF (Optimized Buffer Flush and Fill)” on page 776. 

_Figure 5‐14: OBFF Message Header_ 

**==> picture [346 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1  0 0 1 0<br>Byte 8 Reserved<br>OBFF<br>Byte 12 Reserved<br>Code<br>**----- End of picture text -----**<br>


_Table 5‐17: LTR Message Coding_ 

|**Optimized Buffer Flush/Fill Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|OBFF|0001 0010|100|



**213** 

## **PCI Ex ress Technolo p gy** 

## OBFF Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

3. The Requester ID must be set to the Transmitting Port’s ID. 

**214** 

## _**6**_ 

## _**Flow Control**_ 

## **The Previous Chapter** 

The previous chapter discusses the three major classes of packets: _Transaction Layer Packets_ (TLPs), _Data Link Layer Packets_ (DLLPs) and _Ordered Sets_ . This chapter describes the use, format, and definition of the variety of TLPs and the details of their related fields. DLLPs are described separately in Chapter 9, enti‐ tled ʺDLLP Elements,ʺ on page 307. 

## **This Chapter**

</td>
<td style="background-color:#e8e8e8">

|Assert_INTD|0010 0011b||
|Deassert_INTA|0010 0100b||
|Deassert_INTB|0010 0101b||
|Deassert_INTC|0010 0110b||
|Deassert_INTD|0010 0111b||

有关使用 INTx Messages 的规则：

1. 它们没有数据负载，因此 Length 字段被保留。

2. 它们仅由 Upstream Ports 发出。对接收到的包检查此规则是可选的，但如果检查，违反将作为 Malformed TLPs 处理。

3. 它们必须使用默认流量类 TC0。接收方必须检查此规则，违反将作为 Malformed TLPs 处理。

4. 链路两端的组件必须跟踪四个虚拟中断的当前状态。如果 Upstream Port 的逻辑状态发生变化，则必须发送适当的 INTx 消息。

5. 当 Command Register 的 Interrupt Disable 位设置为 = 1 时，INTx 信令被禁用（与物理中断线的情况一样）。

6. 如果在设备中设置了 Interrupt Disable 位时任何虚拟 INTx 信号处于 active 状态，则 Upstream Port 必须发送相应的 Deassert_INTx 消息。

7. 交换机必须为每个 Downstream Port 独立跟踪四个 INTx 信号的状态，并为 Upstream Port 组合这些状态。

8. 根复合体必须独立跟踪四个 INTx 线的状态，并以实现特定的方式将它们转换为系统中断。

**207**

## **PCI Express Technology**

9. 它们使用 "Local‐Terminate at Receiver" 路由类型，以允许 Switch 在必要时重新映射指定的中断引脚（参见第 808 页 "Mapping and Collapsing INTx Messages"）。因此，INTx 消息中的 Requester ID 可以由最后一个发送者分配。

**Power Management Messages.** PCI Express 与 PCI 电源管理兼容，并增加了基于硬件的链路电源管理。消息用于传达其中一些信息，但要了解整个 PCIe 电源管理协议的工作原理，请参考第 16 章 "Power Management"，位于第 703 页。第 208 页的表 5‐10 总结了四种电源管理消息类型。

*Table 5‐10: Power Management Message Coding*

|**Power Management Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|PM_Active_State_Nak|0001 0100b|100b|
|PM_PME|0001 1000b|000b|
|PM_Turn_Off|0001 1001b|011b|
|PME_TO_Ack|0001 1011b|101b|

电源管理消息规则：

1. 电源管理消息没有数据负载，因此 Length 字段被保留。

2. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

3. PM_Active_State_Nak 由 Downstream Port 在观察到链路邻居请求将链路电源状态更改为 L1 但其选择不这样做时发送（Local ‐ Terminate at Receiver 路由）。

4. PM_PME 由请求电源管理事件的组件向上游发送（Implicitly Routed to the Root Complex）。

5. PM_Turn_Off 向下游发送到所有端点（Implicitly Broadcast from the Root Complex 路由）。

6. PME_TO_Ack 由端点向上游发送。对于具有多个 Downstream Ports 的交换机，在所有 Downstream Ports 收到此消息之前，该消息不会被转发到上游（Gather and Route to the Root Complex 路由）。

**208**

**Chapter 5: TLP Elements**

**Error Messages.** Error Messages 由检测到错误的已启用组件向上游发送（Implicitly Routed to the Root Complex）。为了帮助软件了解如何处理错误，Error Message 在消息头的 Requester ID 字段中标识请求代理。第 209 页的表 5‐11 描述了三种错误消息类型。

*Table 5‐11: Error Message Coding*

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|ERR_COR (Correctable)|0011 0000b|000b|
|ERR_NONFATAL<br>(Uncorrectable, Non‐fatal)|0011 0001b||
|ERR_FATAL<br>(Uncorrectable, Fatal)|0011 0011b||

错误信令消息规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，因此 Length 字段被保留。

3. 根复合体将 Error Messages 转换为系统特定的事件。

**Locked Transaction Support.** Unlock Message 用作 PCI 中定义的 Locked transaction 协议的一部分，对于 Legacy Devices 仍然可用。协议以 Memory Read Locked Request 开头。当路径中的端口看到该 Request 时，它们通过锁定其他 Requesters 使用 VC0 直到收到 Unlock Message 来实现原子读‐修改‐写协议。此消息发送到目标以释放路径中的所有端口并完成 Locked Transaction 序列。第 209 页的表 5‐12 总结了该消息的编码。

*Table 5‐12: Unlock Message Coding*

|**Unlock Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Unlock|0000 0000b|011b|

**209**

**PCI Express Technology**

Unlock Message 规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，Length 字段被保留。

**Set Slot Power Limit Message.** 这从 Downstream Port 发送到插入插槽的设备。此功率限制存储在端点中的 Device Capabilities Register 中。表 5‐13 总结了消息编码。

*Table 5‐13: Slot Power Limit Message Coding*

|**Slot Power Limit Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Set_Slot_Power_Limit|0101 0000b|100b|

Set_Slot_Power_Limit 消息规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 数据负载为 1 DW，因此 Length 字段设置为 1。32 位数据负载的低 10 位用于插槽功率缩放；高负载位必须设置为零。

3. 每当数据链路层转换到 DL_Up 状态时，或者在数据链路层已报告 DL_Up 状态时对 Slot Capabilities Register 进行配置写时，此消息都会自动发送。

4. 如果插槽中的卡已经消耗的功率小于指定的功率限制，则允许忽略该 Message。

**Vendor‐Defined Message 0 and 1.** 这些旨在允许通过规范或供应商特定扩展来扩展 PCIe 消息传递能力。它们的头显示在第 211 页的图 5‐12 中，代码在第 211 页的图 5‐14 中给出。

**210**

**Chapter 5: TLP Elements**

*Figure 5‐12: Vendor‐Defined Message Header*

**==> picture [368 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 1Fmt 1  0  r  r  rType R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 1 1 1 1 1 1 x<br>Byte 8 Target BDF if ID Routing used, Vendor ID<br>otherwise Reserved<br>Byte 12 For Vendor Definition<br>**----- End of picture text -----**<br>


*Table 5‐14: Vendor‐Defined Message Coding*

|**Vendor‐Defined Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Vendor Defined Message 0|0111 1110b|000b, 010b,<br>011b, 100b|
|Vendor Defined Message 1|0111 1111b||

供应商定义消息规则：

1. 数据负载可以包含也可以不包含在任一类型中。

2. 消息通过 Vendor ID 字段区分。

3. Attribute 位 [2] 和 [1:0] 不被保留。

4. 如果 Receiver 不识别该 Message：

   - Type 1 Messages 将被静默丢弃

   - Type 0 Messages 将被视为 Unsupported Request 错误情况

**Ignored Messages.** 列出整个要忽略的 Messages 类别在没有上下文的情况下听起来有点奇怪。这些是以前支持在插卡上而不是在系统板上具有热插拔指示器和按钮的设备的 Hot Plug Signaling 消息。此消息类型在规范修订版 1.0a 中定义，但此选项从 1.1 规范发布开始不再受支持，因此此处仅包含详细信息供参考。正如现在名称所暗示的那样，强烈建议 Transmitters 不要发送这些消息，强烈建议 Receivers 在看到这些消息时忽略它们。如果它们仍要被使用，它们必须符合 1.0a 规范细节。

**211**

**PCI Express Technology**

*Table 5‐15: Hot Plug Message Coding*

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Attention_Indicator_On|0100 0001b|100b|
|Attention_Indicator_Blink|0100 0011b|100b|
|Attention_Indicator_Off|0100 0000b|100b|
|Power_Indicator_On|0100 0101b|100b|
|Power_Indicator_Blink|0100 0111b|100b|
|Power_Indicator_Off|0100 0100b|100b|
|Attention_Button_Pressed|0100 1000b|100b|

Hot Plug Message 规则：

- 它们由 Downstream Port 驱动到插槽中的卡。

- Attention Button Message 由插槽设备向上游驱动。

**Latency Tolerance Reporting Message.** LTR Messages 用于可选地报告设备的可接受读/写服务延迟。要了解有关此电源管理技术的更多信息，请参见第 784 页 "LTR (Latency Tolerance Reporting)" 一节。

*Figure 5‐13: LTR Message Header*

**==> picture [346 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1 0 0 0 0<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>**----- End of picture text -----**<br>


**212**

**Chapter 5: TLP Elements**

*Table 5‐16: LTR Message Coding*

|**Latency Tolerance Reporting Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|LTR|0001 0000|100|

LTR Message 规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，Length 字段被保留。

**Optimized Buffer Flush and Fill Messages.** OBFF Messages 用于向 Endpoints 报告平台电源状态并促进更有效的系统电源管理。要了解有关此技术的更多信息，请参见第 776 页 "OBFF (Optimized Buffer Flush and Fill)" 讨论。

*Figure 5‐14: OBFF Message Header*

**==> picture [346 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1  0 0 1 0<br>Byte 8 Reserved<br>OBFF<br>Byte 12 Reserved<br>Code<br>**----- End of picture text -----**<br>


*Table 5‐17: LTR Message Coding*

|**Optimized Buffer Flush/Fill Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|OBFF|0001 0010|100|

**213**

## **PCI Express Technology**

## OBFF Message 规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，Length 字段被保留。

3. Requester ID 必须设置为 Transmitting Port 的 ID。

**214**

## _**6**_

## _**Flow Control**_

## **The Previous Chapter**

上一章讨论了三类主要的包：_Transaction Layer Packets_ (TLPs)、_Data Link Layer Packets_ (DLLPs) 和 _Ordered Sets_。本章描述了各种 TLP 的使用、格式和定义以及其相关字段的详细信息。DLLPs 在第 9 章 "DLLP Elements" 中单独描述，位于第 307 页。

## **This Chapter**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
