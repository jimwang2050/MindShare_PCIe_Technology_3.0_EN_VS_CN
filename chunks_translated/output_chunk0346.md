这些值由软件编程到表中以在正常运行期间使用。规范建议该表位于 TPH Requester Capability 结构中，如第 906 页的图 20‐16 所示，但也可以选择内置到 MSI‐X 表中。对于给定的功能，只能使用这两个表位置中的一个。该位置在 Requester Capability 寄存器的 ST Table Location 字段 [10:9] 中给出，如第 907 页的图 20‐17 所示。这 2 位的编码在第 907 页的表 20‐2 中显示。

_图 20‐16：TPH Requester Capability 结构_

|31|15|0<br>7|
|---|---|
|PCI Express Capabilities Register|Next Cap<br>Pointer|PCI Express<br>Cap ID (17h)|
|TPH Requester Capability Register|||
|TPH Requester Control Register|||
|TPH ST Table (optional)<br>(Sized by number of ST entries)|||



**906**

**第 20 章：规范修订版 2.1 的更新**

_图 20‐17：TPH 能力和控制寄存器_

**==> picture [340 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPH Requester Capability Register<br>
31 27 26 16 15 11 10 9 8 7 3 2 1 0<br>
RsvdP ST Table Size RsvdP RsvdP<br>
ST Table Location<br>
Extended TPH Requester Supported<br>
Device-Specific Mode Supported<br>
Interrupt Vector Mode Supported<br>
No ST Mode Supported<br>
TPH Requester Control Register<br>
31 10 9 8 7 3 2 0<br>
RsvdP RsvdP<br>
TPH Requester Enable<br>
ST Mode Select<br>
**----- End of picture text -----**<br>


_表 20‐2：ST 表位置编码_

|**位 [10:9]**|**ST 表位置**|
|---|---|
|00b|不存在|
|01b|位于 Requester Capa‐<br>bility 结构中|
|10b|位于 MSI‐X 表中|
|11b|保留|



**907**

**PCI Express 技术**

Requester Capability 寄存器在位 [26:16] 中列出 ST 表中的条目数。每个表条目宽 2 字节，在 TPH Capability 寄存器集中实现的 ST 表在第 908 页的图 20‐18 中显示，其中突出显示了条目零。Requester Capability 寄存器还描述了请求方支持哪些 ST 模式（通过低 3 位）：

- **No ST** - 对 ST 位使用零。在 TPH Requester Control 寄存器的 ST Mode Select 字段中当值 = 000b 时选择。

- **Interrupt Vector** - 使用中断向量号作为到表的偏移，这意味着值包含在 MSI‐X 表中。（ST Mode Select 值 = 001b。）

- **Device‐Specific** - 使用设备特定的方法偏移到 TPH Capability 结构中的 ST 表，因为 ST 值位于那里。这是推荐的实现方式，尽管如何将给定的请求与特定 ST 条目关联超出了规范的范围。（ST Mode Select 值 = 010b。）

- 所有其他 ST Mode Select 编码保留供将来使用。

_图 20‐18：TPH Capability ST 表_

||31|24|23|16|15|8|7|0||
|---|---|---|---|---|---|---|---|---|---|
||ST Upper Entry (1)||ST|Lower Entry (1)|ST Upper Entry (0)||ST Lower Entry (0)|||
||ST Upper Entry (3)||ST|Lower Entry (3)|ST Upper Entry (2)||ST Lower Entry (2)|||
|||||||||||
|||ST Upper Entry|ST Lower Entry|||ST Upper Entry|ST Lower Entry||
|||(Table Size)||(Table Size)||(Table Size - 1)|(Table Size - 1)|||
|||||||||||



## **TLP 前缀**

如果需要，可以通过添加可选的 TLP 前缀来扩展 Steering Tag 位。当 TLP 带有一个或多个前缀时，头通过设置 Format 字段的最高有效位来报告，如第 909 页的图 20‐19 所示。

**908**

**第 20 章：规范修订版 2.1 的更新**

_图 20‐19：TPH 前缀指示_

**==> picture [344 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
Fmt At T T E<br>
Byte 0 Type R TC R R Attr AT Length<br>
1  0 0 tr H D P<br>
Last DW 1st DW<br>
Byte 4 Requester ID Tag<br>
BE BE<br>
Byte 8 Address [63:32]<br>
Byte 12 Address [31:2] PH<br>
**----- End of picture text -----**<br>


## **IDO（基于 ID 的排序）**

事务排序规则对于正确的流量流动很重要，但有时不需要这些规则，在这些情况下可以改善延迟。特别是，来自不同请求方的 TLP 之间不太可能存在依赖关系，因此此功能允许软件启用它们以进行重新排序以提高性能。此操作的详细信息在第 301 页名为"基于 ID 的排序 (IDO)"的部分中描述。

## **ARI（备用路由 ID 解释）**

此可选功能的动机是增加端点可用的功能号。设备号在像 PCI 这样的共享总线架构中很有用，但在点对点架构中通常不需要。因此，规范编写者选择允许设备以不同的方式解释 ID 路由命令的目标。这是通过将设备号始终定义为零，然后允许功能号使用 ID 中以前是设备号的 5 位来实现的。实际上，设备号消失了，而功能号增加到 8 位。使用 ARI 的 TLP 的目标需要被启用以在使用此功能之前识别它，但路径中的路由元素不必知道这一点。它们仅查看总线号以确定路由。

**909**

**PCI Express 技术**

## **电源管理改进**

有四项新增功能可以改善系统有效管理电源的能力，在此列出。所有这些内容在第 703 页的第 16 章"电源管理"中介绍。

## **DPA（动态功率分配）**

一组新的扩展配置寄存器定义了 D0 以下的最多 32 个子状态。这允许软件轻松地更改设备的电源状态，而无需承担一直转换到 D1 设备电源状态的延迟惩罚。要了解更多信息，请参阅第 714 页的"动态功率分配 (DPA)"。

## **LTR（延迟容忍报告）**

允许端点报告它们可以容忍的延迟以响应其请求，使系统软件能够就系统响应时间和睡眠状态做出更好的选择。要了解更多信息，请参阅第 784 页的"LTR（延迟容忍报告）"。

## **OBFF（优化缓冲区刷新和填充）**

类似地，允许系统报告端点应该或不应该启动 DMA 或中断流量的首选时间段，有助于协调系统睡眠时间并改善电源管理。有关更多信息，请参阅第 776 页的"OBFF（优化缓冲区刷新和填充）"。

## **ASPM 选项**

此更改只是允许设备在选择这样做时支持没有 ASPM 链路电源管理。在以前的规范版本中，对 L0s 的支持是强制性的，但现在它变为可选的。

**910**

**第 20 章：规范修订版 2.1 的更新**

## **配置改进**

添加了一些配置寄存器以改善设备的软件可见性和控制。

## **内部错误报告**

这旨在为像交换机这样没有驱动程序来处理此类问题的设备提供一种标准化的方式来报告内部问题。它还添加了在多个 TLP 头导致错误时跟踪多个 TLP 头（而不是像以前那样只有一个）的能力。本主题在名为第 667 页的"内部错误"的错误章节中介绍。

## **可调整大小的 BAR**

这组新的扩展配置寄存器允许使用大量本地内存的设备报告它们是否可以处理较小的内存量，如果可以，什么大小是可接受的。知道查找它们的软件可以找到新寄存器（如第 912 页的图 20‐20 所示），并根据系统内存和其他设备的竞争要求，对它们进行编程以为平台提供适当的内存大小。

这些寄存器的使用适用一些规则：

1. 为避免混淆，只有在 Command 寄存器中的 Memory Enable 位已被清除时，才应更改 BAR 大小。

2. 规范强烈建议功能不要通告比它们可以有效使用的更大的 BAR。

3. 为了确保最佳性能，软件应分配将在系统上工作的最大 BAR 大小。

**911**

## **PCI Express 技术**

## _图 20‐20：可调整大小的 BAR 寄存器_

**==> picture [363 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 20 19 16 15 0<br>
Next Extended Version PCIe Extended Capability ID<br>
Capability Offset (1h) (0015h for Resizable BAR)<br>
31 0 Offset<br>
PCIe Enhanced Capability Header 000h<br>
Resizable BAR Capability Register (0) 004h<br>
Register Pair<br>
for each  Reserved Resizable BAR Control Register (0) 008h<br>
supported<br>
BAR …<br>
Resizable BAR Capability Register (n) n*8 +4<br>
Reserved Resizable BAR Control Register (n) n*8 +8<br>
**----- End of picture text -----**<br>


## **Capability 寄存器**

此寄存器仅报告哪些 BAR 大小适用于此功能。位 4 到 23 用于此目的，值如下所示：

- 位 4 - 1MB BAR 大小适用于此功能

- 位 5 - 2MB

- 位 6 - 4MB

- ...

- 位 23 - 512GB 适用于此功能

_图 20‐21：可调整大小的 BAR Capability 寄存器_

**==> picture [242 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24   23 4   3 0<br>
RsvdP RsvdP<br>
**----- End of picture text -----**<br>


## **Control 寄存器**

此寄存器中的 BAR Index 字段报告此大小所指的 BAR（0 到 5 是可能的）。Number of Resizable BARs 字段仅为 Control

**912**

**第 20 章：规范修订版 2.1 的更新**

寄存器零定义，并为所有其他寄存器保留。它说明了六个可能的 BAR 中实际有多少个具有可调整的大小。最后，BAR Size 字段由软件编程以指定由 BAR Index 字段指示的 BAR 的所需大小（0 = 1MB，1=2MB，2=4MB，...，19=512GB）。

_图 20‐22：可调整大小的 BAR Control 寄存器_

**==> picture [281 x 136] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 13  12 8   7 5   4 3    2 0<br>
RsvdP RsvdP<br>
BAR Size (RW)<br>
Number of Resizable<br>
BARs (RO)<br>
BAR Index (RO)<br>
**----- End of picture text -----**<br>


一旦对可调整大小的值进行了编程，则枚举软件将能够像往常一样工作：将所有 F 写入每个 BAR 然后回读将报告所选的大小。请注意，如果大小值已更改，则 BAR 的内容将丢失，如果先前已设置，则需要重新编程。图 20‐23（第 914 页）突出显示了 Type 0 头的配置头空间中的 BAR 寄存器。

**913**

**PCI Express 技术**

## _图 20‐23：Type0 配置头中的 BAR_

**==> picture [160 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 2 1 0 DW<br>
Device Vendor 00<br>
ID ID<br>
Status Command 01<br>
Register Register<br>
Class Code Revision 02<br>
ID<br>
HeaderType LatencyTimer CacheLineSize 03<br>
04<br>
Base Address 0<br>
05<br>
Base Address 1<br>
06<br>
Base Address 2<br>
07<br>
Base Address 3<br>
08<br>
Base Address 4<br>
09<br>
Base Address 5<br>
10<br>
CardBus CIS Pointer<br>
Subsystem ID SubsystemVendor ID 11<br>
Expansion ROM 12<br>
Base Address<br>
Reserved CapabilitiesPointer 13<br>
14<br>
Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>
**----- End of picture text -----**<br>


## **简化的排序表**
