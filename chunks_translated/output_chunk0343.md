这些值由软件编程到表中以在正常操作期间使用。规范建议该表位于 TPH Requester Capability 结构中，如图 20-16 所示（在第 906 页），但它也可以构建到 MSI-X 表中。对于给定的功能，只能使用这些表位置中的一个或另一个。位置在 Requester Capability 寄存器的 ST Table Location 字段 [10:9] 中给出，如图 20-17 所示（在第 907 页）。这 2 位的编码在第 907 页的表 20-2 中显示。

_图 20-16：TPH Requester Capability 结构_

|31|15|0<br>7|
|---|---|
|PCI Express Capabilities Register|Next Cap<br>Pointer|PCI Express<br>Cap ID (17h)|
|TPH Requester Capability Register||
|TPH Requester Control Register||
|TPH ST Table（可选）<br>（大小由 ST 条目数决定）||


**906**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-17：TPH Capability 和 Control 寄存器_

**==> 图片 [340 x 285] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
TPH Requester Capability Register<br>31 27 26 16 15 11 10 9 8 7 3 2 1 0<br>RsvdP ST Table Size RsvdP RsvdP<br>ST Table Location<br>Extended TPH Requester Supported<br>Device-Specific Mode Supported<br>Interrupt Vector Mode Supported<br>No ST Mode Supported<br>TPH Requester Control Register<br>31 10 9 8 7 3 2 0<br>RsvdP RsvdP<br>TPH Requester Enable<br>ST Mode Select<br>**----- 图片文字结束 -----**


_表 20-2：ST 表位置编码_

|**位 [10:9]**|**ST 表位置**|
|---|---|
|00b|不存在|
|01b|位于 Requester Capability 结构中|
|10b|位于 MSI-X 表中|
|11b|保留|


**907**

**PCI Ex ress Technolo p gy**

Requester Capability 寄存器在位 [26:16] 中列出 ST Table 中的条目数。每个表条目宽 2 字节，在 TPH Capability 寄存器集中实现的 ST Table 如图 20-18（在第 908 页）所示，其中突出显示了条目零。Requester Capability 寄存器还描述了请求者支持哪些 ST 模式，以及 3 个 LSB：

- **No ST** — 对 ST 位使用零。在 TPH Requester Control 寄存器的 ST Mode Select 字段中选择，值为 000b 时。

- **Interrupt Vector** — 使用中断向量号作为表的偏移量，这意味着值包含在 MSI-X 表中。（ST Mode Select 值 = 001b。）

- **Device-Specific** — 使用设备特定的方法偏移到 TPH Capability 结构中的 ST Table，因为 ST 值位于其中。这是建议的实现，尽管给定的请求如何与特定 ST 条目相关联超出了规范的范围。（ST Mode Select 值 = 010b。）

- 所有其他 ST Mode Select 编码保留供将来使用。

_图 20-18：TPH Capability ST Table_

||31|24|23|16|15|8|7|0||
|---|---|---|---|---|---|---|---|---|---|
||ST Upper Entry (1)||ST|Lower Entry (1)|ST Upper Entry (0)||ST Lower Entry (0)|||
||ST Upper Entry (3)||ST|Lower Entry (3)|ST Upper Entry (2)||ST Lower Entry (2)|||
|||||||||||
|||ST Upper Entry|ST Lower Entry|||ST Upper Entry|ST Lower Entry||
|||(Table Size)||(Table Size)||(Table Size - 1)|(Table Size - 1)|||
|||||||||||


## **TLP Prefixes**

如果需要，可以通过添加可选的 TLP 前缀来扩展 Steering Tag 位。当 TLP 给出一个或多个前缀时，头通过设置 Format 字段的最高有效位来报告它，如图 20-19（在第 909 页）所示。

**908**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-19：TPH 前缀指示_

**==> 图片 [344 x 126] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>1  0 0 tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- 图片文字结束 -----**


## **IDO（基于 ID 的排序）**

事务排序规则对于正确的流量流很重要，但有时不需要，并且在这些情况下可以改善延迟。特别是来自不同请求者的 TLP 之间不太可能有依赖关系，因此此功能允许软件启用它们以重新排序以提高性能。此操作的详细信息在第 301 页上名为"ID Based Ordering (IDO)"的部分中描述。

## **ARI（替代路由 ID 解释）**

此可选功能的动机是增加端点可用的功能号数。设备号在 PCI 等共享总线架构中很有用，但在点对点架构中通常不需要。因此，规范编写者选择允许设备以不同方式解释 ID 路由命令的目标。这是通过将 Device number 定义为始终为零来实现的，然后允许 Function number 使用 ID 中以前是 Device number 的 5 位。实际上，Device number 消失了，而 Function number 增加到 8 位。使用 ARI 的 TLP 的目标需要被启用以识别它，然后软件才能使用此功能，但路径中的路由元素不必意识到这一点。它们只查看总线号以确定路由。

**909**

**PCI Ex ress Technolo p gy**

## **电源管理改进**

有四项新增功能可提高系统有效管理电源的能力，它们在此处列出。所有这些内容均在第 16 章"电源管理"（第 703 页）中介绍。

## **DPA（动态功率分配）**

一组新的扩展配置寄存器定义了 D0 以下最多 32 个子状态。这允许软件轻松地更改设备的电源状态，而不会产生一直转到 D1 设备电源状态的延迟惩罚。有关详细信息，请参阅第 714 页的"动态功率分配 (DPA)"。

## **LTR（延迟容忍报告）**

允许端点报告它们可以容忍的延迟以响应其请求，使系统软件能够就系统响应时间和睡眠状态做出更好的选择。有关详细信息，请参阅第 784 页的"LTR（延迟容忍报告）"。

## **OBFF（优化缓冲区刷新和填充）**

类似地，允许系统报告端点应该或不应该启动 DMA 或中断流量的首选时间段，有助于协调系统睡眠时间并改善电源管理。有关详细信息，请参阅第 776 页的"OBFF（优化缓冲区刷新和填充）"。

## **ASPM 选项**

此更改只是允许设备在选择时支持无 ASPM 链路电源管理。在以前的规范版本中，对 L0s 的支持是强制性的，但现在它变为可选的。

**910**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

## **配置改进**

添加了一些配置寄存器以改进对设备的软件可见性和控制。

## **内部错误报告**

这旨在为没有驱动程序来处理它们的设备（如交换机）提供一种标准化的方式来报告内部问题。它还添加了在错误结果时跟踪多个 TLP 头而不是像以前那样只跟踪一个的功能。本主题在第 667 页的关于错误的"内部错误"部分中介绍。

## **Resizable BAR**

这组新的扩展配置寄存器允许使用大量本地内存的设备报告它们是否可以使用更少的内存量，如果是，则可以接受的大小。知道查找它们的软件可以找到新的寄存器，如图 20-20（在第 912 页）所示，并根据系统内存和其他设备的竞争要求对它们进行编程以给出适合平台的内存大小。

这些寄存器的使用有一些规则：

1. 为避免混淆，仅当 Command 寄存器中的 Memory Enable 位已清除时，才应更改 BAR 大小。

2. 规范强烈建议功能不要通告比其有效使用的更大的 BAR。

3. 为了确保最佳性能，软件应分配将适用于系统的最大 BAR 大小。

**911**

## **PCI Ex ress Technolo p gy**

## _图 20-20：Resizable BAR 寄存器_

**==> 图片 [363 x 166] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 20 19 16 15 0<br>Next Extended Version PCIe Extended Capability ID<br>Capability Offset (1h) (0015h for Resizable BAR)<br>31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>Resizable BAR Capability Register (0) 004h<br>Register Pair<br>for each  Reserved Resizable BAR Control Register (0) 008h<br>supported<br>BAR …<br>Resizable BAR Capability Register (n) n*8 +4<br>Reserved Resizable BAR Control Register (n) n*8 +8<br>**----- 图片文字结束 -----**


## **Capability Register**

此寄存器仅报告哪些 BAR 大小将适用于此功能。位 4 到 23 用于此目的，值如下所示：

- 位 4 — 1MB BAR 大小将适用于此功能

- 位 5 — 2MB

- 位 6 — 4MB

- ...

- 位 23 — 512GB 将适用于此功能

_图 20-21：Resizable BAR Capability 寄存器_

**==> 图片 [242 x 38] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 24   23 4   3 0<br>RsvdP RsvdP<br>**----- 图片文字结束 -----**


## **Control Register**

此寄存器中的 BAR Index 字段报告此大小引用的 BAR（0 到 5 是可能的）。Number of Resizable BARs 字段仅对 Control

**912**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

Register 0 定义，并对其余所有保留。它告诉六个可能的 BAR 中实际上有多少个具有可调整的大小。最后，BAR Size 字段由软件编程以指定 BAR Index 字段指示的 BAR 所需的大小（0 = 1MB，1=2MB，2=4MB，...，19=512GB）。

_图 20-22：Resizable BAR Control 寄存器_

**==> 图片 [281 x 136] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 13  12 8   7 5   4 3    2 0<br>RsvdP RsvdP<br>BAR Size (RW)<br>Number of Resizable<br>BARs (RO)<br>BAR Index (RO)<br>**----- 图片文字结束 -----**


一旦 Resizable 值被编程，枚举软件将能够像通常一样工作：将所有 F 写入每个 BAR 并读回它将报告所选的大小。请注意，如果大小值被更改，BAR 的内容将丢失，如果之前已设置，则需要重新编程。图 20-23（在第 914 页）突出显示了 Type 0 头的配置头空间中的 BAR 寄存器。

**913**

**PCI Ex ress Technolo p gy**

## _图 20-23：Type0 配置头中的 BAR_

**==> 图片 [160 x 273] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
3 2 1 0 DW<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>HeaderType LatencyTimer CacheLineSize 03<br>04<br>Base Address 0<br>05<br>Base Address 1<br>06<br>Base Address 2<br>07<br>Base Address 3<br>08<br>Base Address 4<br>09<br>Base Address 5<br>10<br>CardBus CIS Pointer<br>Subsystem ID SubsystemVendor ID 11<br>Expansion ROM 12<br>Base Address<br>Reserved CapabilitiesPointer 13<br>14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>**----- 图片文字结束 -----**


## **简化的排序表**
