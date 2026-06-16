功率预算信息维护在一个由一个或多个 32 位条目组成的表中。每个表条目包含设备支持的不同工作模式的功率预算信息。每个表条目通过数据选择字段进行选择，然后从数据字段读取所选条目。索引值从零开始，并按顺序实现。当所选索引在数据字段中返回全零时，已找到功率预算表的结尾。第 885 页的图 19-13 说明了数据字段的格式和可用信息的类型。

_图 19-12：功率预算能力寄存器_

**==> 图片 [341 x 104] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31                                                                                               0<br>Offset<br>PCIe Extended Capability Header 00h<br>RsvdP Data Select  04h<br>Register<br>Data Register 08h<br>Power Budget<br>RsvdP 0Ch<br>Capability Register<br>**----- 图片文字结束 -----**


**884**

**第 19 章：热插拔和功率预算**

_图 19-13：功率预算数据字段格式和定义_

**==> 图片 [243 x 476] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Base Power<br>Data Scale Specifies the base power (in watts)for the state indicated by bits [20:10]. Base Power x Scale = actual power consumption.   Data Scale Values:     00b            1.0x     01b            0.1x     10b            0.01x     11b            0.001x All other encodings are reserved. PM sub state of operating condition described by this entry:  000b             Default Sub State   001b –111b   Device-specific Sub StateAll other encodings are reserved. PM state described by this entry:  00b            D0   01b            D1   10b            D2   11b            D3 D3-Cold PM State description = 11b and Aux or PME Aux in Type field.D3-Hot state = 11b + any other Type value.  entries starting with n<br>    10 9    8  7                                   0<br>State<br>PM Sub<br>PM State<br>Type<br>Rail<br>Power<br>This entire register is read-only<br>RsvdP<br>31                                            21 20      18 17     15 14 13 12<br>How it works: The power budgeting data for the function consists of a table of entry 0. Each entry is read by placing an index value in the Power Budgeting DataSelect register and then reading the value returned in the Power Budgeting Data register.The end of table is indicated by a return value of all 0's in the Data register.<br>Auxiliary<br>Type of operating condition described by this entry:  000b            PME Aux   001b   010b            Idle   011b            Sustained   111b            Maximum All other encodings are reserved.<br>Power rail of operating condition described by this entry:  000b     12V power.  001b     3.3V power.  010b     1.8V power.  111b     Thermal All other encodings are reserved.<br>**----- 图片文字结束 -----**


**885**

**PCI Ex ress Technolo p gy**

**886**

## _**20**_

## _**Spec 修订版 2.1 的更新**_

## **上一章**

上一章描述了 PCI Express 热插拔模型。还为所有支持热插拔功能的设备和形态因素定义了标准化的使用模型。功率也是热插拔卡的一个问题，当在运行时向系统添加新卡时，重要的是确保其功率需求不超过系统可以提供的内容。需要一种机制来在授予设备操作权限之前查询其功率要求。功率预算寄存器提供了该机制。

## **本章**

本章描述了规范的 2.1 版本中添加的更改和新功能。其中一些主题，如与电源管理相关的主题，在其他章节中描述，但对于其他主题，没有其他合适的位置。最后，将它们全部归集在一章中似乎是最佳方法，以确保它们都被覆盖，并帮助阐明哪些功能是新的。

## **下一章**

下一部分是本书的附录，其中包括以下主题：使用 LeCroy 工具调试 PCI Express 流量、PCI Express 架构的市场与应用、使用 PCI Express 技术实现智能适配器和多主机系统、锁定的传统支持以及本书词汇表。

## **PCIe 规范 2.1 版更改**

PCIe 规范的 2.1 版引入了若干更改以增强性能或改善操作特性。它没有增加另一种数据速率，这就是为什么它被认为是增量修订。修改可以大致分为四个改进领域：系统冗余、性能、电源管理和配置。

**887**

**PCI Ex ress Technolo p gy**

## **系统冗余改进：多播**

多播 (Multi-casting) 功能允许将 Posted Write TLP 同时路由到多个目标，从而允许自动生成数据的冗余副本或支持多头图形。如第 888 页的图 20-1 所示，可以仅基于地址将从某个端点 (Endpoint) 发送的 TLP 路由到多个目标。在此示例中，数据被发送到视频端口进行显示，而其冗余副本被自动路由到存储。当然，还有其他方法可以支持此活动，但从链路利用率的角度来看，这是非常有效的，因为它不需要接收者将数据包重新发送到辅助位置。

_图 20-1：多播系统示例_

**==> 图片 [372 x 158] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
SDRAM<br>GFX Root Complex<br>Endpoint Endpoint<br>Switch<br>NIC<br>Disk  Disk<br>SCSI SCSI<br>**----- 图片文字结束 -----**


此机制仅支持 Posted、地址路由的请求，例如包含要传送的数据的 Memory Writes，以及可以解码以显示应接收数据的端口的地址。即使其地址落在 MultiCast 地址范围内，Non-posted 请求也不会被视为多播。这些将像通常一样被视为单播 TLP。

多播操作的设置涉及为每个将涉及的路由元素和功能编程一个新的寄存器块，称为多播能力结构 (Multicast Capability structure)。该块的内容在第 889 页的图 20-2 中显示，可以看到它们定义了地址以及 MCG（多播组号），用于解释功能是应发送还是接收传入 TLP 的副本，或者端口是否应转发它们。让

**888**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

我们在接下来描述这些寄存器，并讨论它们如何用于在系统中创建多播操作。

_图 20-2：多播能力寄存器_

|20<br>31|19|19|16|15||0||||
|---|---|---|---|---|---|---|---|---|
|Next Extended<br>Capability Offset||Version<br>(1h)||PCIe Extended Capability ID<br>(0012h for Multicast)||||||
||||31|||||0|Offset|
|||||PCIe Enhanced Capability Header|||||00h|
|||||Multicast Control||Multicast Capability|||04h|
|MCGs this Function||||MC_Base_Address Register|||||08h<br>0Ch|
|is allowed to receive||||||||||
|or forward||||MC_Receive||Register|||10h<br>14h|
|MCGs this Function||||||||||
|must not send|||||||||18h|
|or forward||||MC_Block_All||Register|||1Ch|
|MCGs this Function<br>must not send or||||MC_Block_Untranslated Register|||||20h<br>24h|
|forward if the address||||||||||
|Root Ports and<br>is untranslated||||MC_Overlay_BAR|||||28h<br>2Ch|
|Switch Ports||||||||||


## **多播能力寄存器**

图顶部的 Capability Header 寄存器包括 Capability ID 0012h、4 位版本号，以及指向寄存器链接列表中下一个能力结构的指针。

## **Multicast Capability**

该寄存器在第 890 页的图 20-3 中详细显示，包含几个字段。MC_Max_Group 值定义了此功能已设计支持的多播组数减一，因此零值意味着支持一个

**889**

**PCI Ex ress Technolo p gy**

组。Window Size Requested 仅对端点有效，在交换机和根端口中保留，表示此目的所需的地址大小为 2 的幂。

_图 20-3：多播能力寄存器_

**==> 图片 [294 x 107] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
15   14   13 8   7   6   5 0<br>MC_Window_Size RsvdP MC_Max_Group<br>Requested<br>RsvdP<br>Exponent for MC  Max number of MCGs<br>MC_ECRC_ window size in  Supported minus 1<br>Regeneration_Supported endpoints –<br>RsvdP in Switches<br>and RC<br>**----- 图片文字结束 -----**


最后，第 15 位指示此功能是否支持在转发涉及地址更改的 TLP 时重新生成 ECRC 值。有关此内容的更多详细信息，请参阅第 895 页上名为"Overlay Example"的部分。

## **Multicast Control**

该寄存器如图 20-4 所示（在第 890 页），包含 MC_Num_Group，它使用软件为此功能配置的多播组数进行编程。默认数字为零，规范指出如果在此编程的值大于 MC_Max_Group 寄存器中定义的最大值，将导致未定义的行为。MC_Enable 位用于为此组件启用多播机制。

_图 20-4：多播控制寄存器_

**==> 图片 [274 x 82] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
15   14 6   5 0<br>RsvdP MC_Num_Group<br>MC_Enable Number of MCGs<br>Configured minus 1<br>**----- 图片文字结束 -----**


**890**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

## **Multicast Base Address**

基地址寄存器如图 20-5 所示（在第 891 页），包含此组件的多播地址范围的 64 位起始地址。MultiCast Index Position 寄存器指示应在其内找到 MultiCast 组 (MCG) 号的地址内的位位置。当传入 TLP 的地址落在此 Base Address 开始的多播地址范围内时，逻辑将按 Index Position 中给出的位位置数偏移到地址本身，并将接下来的位（最多 6 位，允许最多 64 个组）解释为该 TLP 的 MCG 号。MCG 号将依次指示端口是否应转发此 TLP 的副本。

_图 20-5：多播基地址寄存器_

**==> 图片 [287 x 91] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 12   11 6   5 0<br>MC_Index<br>MC_Base_Address [31:12] RsvdP<br>_Position<br>MC_Base_Address [63:32]<br>**----- 图片文字结束 -----**


图 20-6（在第 892 页）显示了如何在地址中定位 MCG 的示例。这里 Index Position 值为 24，因此 MCG 在地址位 25 到 30 中找到。有趣的是，由于基地址未定义地址的低 12 位，MC Index Position 必须为 12 或更大才有效。如果小于 12 且设置了 MC_Enable 位，则组件的行为将是未定义的。

**891**

## **PCI Ex ress Technolo p gy**

_图 20-6：多播组号的位置_

**==> 图片 [364 x 165] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [63:32]<br>Byte 12 MCG Address [31:2] R<br>MC_Index_Position = 24<br>**----- 图片文字结束 -----**


## **MC Receive**

此 64 位寄存器是一个位向量，指示此功能应接受副本的 64 个 MCG 中的哪些，或此端口应转发副本的哪些。例如，如果发现 MCG 值为 47，并且此寄存器中的第 47 位置位，则此功能应接收它或此端口应转发它。

## **MC Block All**

此 64 位寄存器指示端点功能被阻止发送的 MCG 以及交换机或根端口被阻止转发的 MCG。例如，可以在交换机或根端口中进行编程，以防止其将 MultiCast TLP 转发到不理解它们的端点。被阻止的 TLP 被视为错误条件，如何处理该错误将在下一节中描述。

## **MC Block Untranslated**

此 64 位寄存器的含义和用途几乎与 Block All 寄存器相同，只是它不适用于其 AT 头字段显示已转换的 TLP。此机制可用于设置受保护的多播窗口，使其只能接收已转换的地址。

如果由于这两个阻止寄存器之一的设置而阻止了 TLP，则它将作为 MC Blocked TLP 处理，这意味着它被丢弃并且端口

**892**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

或功能将其记录并将其作为错误发出信号。记录错误涉及在其 Status 寄存器或 Secondary Status 寄存器（视情况而定）中设置 Signaled Target Abort 位。这几乎不足以提供有用的信息，因此规范强烈建议在具有多播能力的功能中实现高级错误报告 (AER) 寄存器，以便于隔离和诊断故障。

规范指出，所有实现 MC Capability 寄存器的功能中都需要此寄存器，但如果端点功能未实现 ATS（地址转换服务）寄存器，则设计人员可以选择将这些位保留。

## **多播示例**

此时，示例将有助于说明如何使用这些寄存器来设置多播环境。要设置此环境，让我们首先为相关寄存器提供一些值：

- MC_Base_Address = 2GB（多播范围的起始地址）

- MC_Max_Group = 7（意味着此设计可能有 8 个窗口）

- MC_Window_Size_Requested = 10（意味着端点请求 2[10] 或 1KB 大小）

- MC_Index_Position = 12（意味着每个窗口的实际大小为 2[12]）

- MC_Num_Group = 5（意味着软件仅配置了 8 个可用多播窗口中的 6 个）

根据这些寄存器设置，第 894 页的图 20-7 中的图像说明了结果。多播窗口范围从 2GB 开始，范围高达 2GB + 8 *（窗口大小）。但是，软件仅启用 6 个，因此实际的多播地址范围是从 2GB 到 2GB + 24KB。窗口大小相同，对应于 MCG：MCG 0 是第一个窗口，1 是下一个窗口，依此类推。

**893**

**PCI Ex ress Technolo p gy**

_图 20-7：多播地址示例_

**==> 图片 [370 x 166] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
System Memory Map<br>MC Address Range<br>= 2GB to 2GB + 2 [12] * 6<br>= 2GB to 2GB + 24KB<br>8 MC windows available in<br>2GB + 24KB<br>MC Group 5 hardware, each at least 2 [10]<br>Only 6 MC windows are  MC Group 4MC Group 3 in size (technically, 2 [12] is<br>configured for use MC Group 2MC Group 1 min. address granularity)<br>2GB MC Group 0 MC_Base_Address<br>**----- 图片文字结束 -----**


## **MC Overlay BAR**

最后一组寄存器是实现多播的交换机和根端口所必需的，但它们未在端点中实现。此 BAR 的动机是它允许两种特殊情况。首先，即使端点不是为多播设计的，端口也可以在多播窗口中向下游转发 TLP。其次，端口可以将多播 TLP 上行转发到系统内存。在这两种情况下，这是通过用将被目标识别的地址替换请求的部分地址来实现的。这样做允许组件中的单个 BAR 用作单播和多播写入的目标，即使它不是为多播能力设计的。

如图 20-8 所示（在第 895 页），此寄存器块由将覆盖到传出 TLP 上的地址和 6 位 Overlay Size 指示符组成。此处引用的 size 简单地说就是将从原始 64 位地址保留的位数，而所有其他位将被 Overlay BAR 位替换。规范至少在一个地方错误地将其称为字节大小，但在其他地方明确表示它是一个位数。请注意，overlay size 值必须为 6 或更高才能启用 overlay 操作。如果大小给定为 5 或更低，则不会发生 overlay，地址不变。

**894**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-8：多播 Overlay BAR_

**==> 图片 [287 x 91] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 6   5 0<br>MC_Overlay<br>MC_Overlay_BAR [31:6]<br>_Size<br>MC_Overlay_BAR [63:32]<br>**----- 图片文字结束 -----**


## **Overlay 示例**

现在考虑如图 20-9（在第 896 页）所示的需要地址 overlay 的情况。这里要转发的 TLP 的地址 ABCD_BEEFh 落在定义的多播范围内（也称为多播命中），并且出口端口已使用 Overlay BAR 中的有效值进行了配置。

Overlay 情况创建了在多播能力寄存器描述中前面提到的 ECRC 值的异常情况。如果正在通过 overlay 更改地址的 TLP 包含 ECRC，则该值将被此更改错误地呈现。交换机和根端口可选择性地支持基于新地址重新生成 ECRC，以便它继续发挥其作用。如果路由代理不支持，则 ECRC 将被简单地丢弃，并且 TD 头位被强制为零以避免任何混淆。

ECRC 重新生成可能会出现潜在问题。如果传入的 TLP 已有错误，但由于地址被修改而重新生成了 ECRC 值，则会无意中隐藏原始错误。为避免这种情况，路由代理必须首先验证原始 ECRC。如果发现错误，则必须通过在追加计算出的 ECRC 值之前将其反转来强制在传出 TLP 上出现错误的 ECRC，以确保目标将其视为错误条件。

**895**

**PCI Ex ress Technolo p gy**

_图 20-9：Overlay 示例_

**==> 图片 [315 x 268] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
System Memory Map<br>PCIe BAR Range Overlaid Address:<br>FEED_0000  FEED_BEEFh<br>to FEED_FFFF<br>Original Address:<br>ABCD_BEEFh<br>Multicast Address<br>Range<br>**----- 图片文字结束 -----**


## **路由多播 TLP**

当交换机或根端口检测到 MC 命中（地址落在 MC 范围内）时，正常路由被挂起。从地址中提取 MCG，并与所有端口的 MC_Receive 寄存器进行比较，以查看其中哪些应转发此 TLP 的副本。其相应的 Receive 寄存器位置位的端口将转发 TLP 的副本，除非其相应的 MC Blocked 寄存器位也被置位。如果没有端口转发 TLP 且没有功能使用它，则将其静默丢弃。为了防止循环，永远不会在 TLP 的入口端口上重新转发，但 ACS 情况可能例外。

端点提取 MCG 并将其与其 Receive 寄存器进行比较。如果不匹配，则 TLP 被静默丢弃。如果端点不支持多播，则它会将 TLP 视为具有普通地址。

**896**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

## **拥塞避免**

多播的使用将按 MC 流量的百分比成比例地增加系统流量，这导致数据包拥塞的风险。为了避免产生反压，MC 目标应设计为"以速度"接受 MC 流量，即延迟最小。为了避免超额订阅链路，MC 发起者应限制其数据包注入速率。明智的系统设计人员将仔细选择组件以处理这种情况。例如，使用缓冲区足够大以处理预期流量的交换机和根端口，以及能够足够快地接受其传入 MC 数据包的端点，以避免出现问题。

## **性能改进**

通过添加四个新功能来增强系统性能：

1. AtomicOps 替代传统的事务锁定机制

2. TLP 处理提示 (TLP Processing Hints) 允许软件建议缓存选项

3. 基于 ID 的排序 (ID-Based Ordering) 以避免不必要的延迟

4. 替代路由 ID 解释 (Alternative Routing-ID Interpretation) 以增加设备中可用的功能数。

## **AtomicOps**

共享资源或彼此通信的处理器有时需要对系统资源进行不间断的或"原子的"访问，以执行诸如测试和设置信号量之类的操作。在并行处理器总线上，这是通过断言 Lock 引脚来锁定总线，直到发起者完成整个序列（读后跟写）来实现的，在此期间其他处理器不允许在总线上启动事务。PCI 包括一个 Locked 引脚，以在 PCI 总线上以及处理器总线上应用相同的模型，从而允许此协议与外围设备一起使用。

此模型有效，但在共享处理器总线上速度很慢，在进入 PCI 总线时甚至更糟。这就是为什么 PCIe 限制其仅用于传统设备的原因之一。然而，如今 PC 中越来越多地使用共享处理（如图形协处理器和计算加速器），这使该问题重新回到突出位置，因为不同的计算引擎需要能够共享原子协议。在 PCIe 上解决此问题的方法是引入三个新命令，每个命令可以在目标设备内原子地执行一系列操作，

**897**

## **PCI Ex ress Technolo p gy**

而不是在接口上需要一系列单独的不可中断的命令。这些新命令称为 AtomicOps，包括：

1. FetchAdd（Fetch and Add，获取并添加）— 此请求包含一个"add"值。它读取目标位置，将"add"值添加到其中，将结果存储在目标位置中，并返回目标位置的原始值。这可用于支持以原子方式更新统计计数器。

2. Swap（Unconditional Swap，无条件交换）— 此请求包含一个"swap"值。它读取目标位置，将"swap"值写入其中，并返回原始目标值。这对于以原子方式读取和清除计数器很有用。

3. CAS（Compare and Swap，比较并交换）— 此请求同时包含一个"compare"值和一个"swap"值。它读取目标位置，将其与"compare"值进行比较，如果它们相等，则写入"swap"值。最后，它返回目标位置的原始值。这可以用作管理信号量的"测试和设置"机制。
