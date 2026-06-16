CPU<br>
Root Complex<br>
Memory<br>
Interrupt Controller<br>
Switch<br>
Assert_INTA Assert_INTB<br>
Deassert_INTA Deassert_INTB<br>
INTA#<br>
PCIe PCIe- INTB#<br>
Endpoint PCI(X) INTC#INTD#<br>
Bridge<br>
PCI(X)<br>
**----- End of picture text -----**<br>


**806**

**第 17 章：中断支持**

## **INTx 消息格式**

图 17-10（第 807 页）描述了 INTx 消息头的格式。中断控制器是这些消息的最终目的地，但是，所采用的路由方法_不是_"Route to the Root Complex"，而实际上是"Local ‐ Terminate at Receiver"，如图 17-10 所示。这有两个原因。第一个是因为沿上游路径的每个桥（包括交换机端口和根端口）可以将虚拟中断线映射到跨桥的不同虚拟中断线（例如，交换机端口收到 Assert_INTA 但在上游传播时将其映射到 Assert_INTB）。有关此 INTx 映射的更多信息，请参见第 808 页的"INTx Mapping"。

使用本地路由类型的第二个原因是由于我们正在模拟基于引脚的信号。如果端口收到映射到其主侧 INTA 的断言中断消息，并且由于先前的中断已经向上游发送了 Assert_INTA 消息，则没有理由再发送一条。INTA 已被视为已断言。有关 INTx 消息合并的更多信息，请参见第 810 页的"INTx Collapsing"。

_Figure 17-10: INTx Message Format and Type_

|||||+0|+0|||||||||+1|+1|||||||||+2|+2|+3|+3|||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||7|6|5|4|3|2|1|0||7||6|5|4|3|2||1|0|7|6||5|4|3|7 6 5 4 <br> 2 1 0|3|2|1|0||
|Byte 0|Fmt<br>0 0 1|||Type<br>1 0**1 0**||||**0**||R||TC|||R|At<br>tr||R|T<br>H|T<br>D|E<br>P||Attr||Length<br>AT|||||||
|Byte 4|||||Requester||||||||ID|||||||||||Tag||**Message**||**Code**||||
|Byte 8|||||||||||Reserved for INTx|||||||||||Messages||||||||||
|Byte 12|||||||||||Reserved for INTx|||||||||||Messages||||||||||
|**Local**|||**- Terminate**|||||||**at Receiver**|||||||||||||||**20h = Assert_INTA**|||||||
||||||||||||||||||||||||||**21h = Assert_INTB**|||||||
||||||||||||||||||||||||||**22h = Assert_INTC**|||||||
||||||||||||||||||||||||||**23h = Assert_INTD**|||||||
||||||||||||||||||||||||||**24h = Deassert_INTA**|||||||
||||||||||||||||||||||||||**25h = Deassert_INTB**|||||||
||||||||||||||||||||||||||**26h = Deassert_INTC**|||||||
||||||||||||||||||||||||||**27h = Deassert_INTD**|||||||


**807**

**PCI Ex ress 3.0 Technolo p gy**

## **INTx 消息的映射与合并**

## **INTx 映射**

交换机必须遵守 PCI 规范定义的 INTx 映射，如表 17-1（第 809 页）所示。该映射定义了当中断通过 PCI-to-PCI 桥路由时存在的虚拟连接。该映射基于 INTx 消息类型和消息的请求者 ID 字段中的设备号。

请参考第 810 页的图 17-11 作为此示例。在两个下游交换机端口上收到的断言中断消息都是 INTA 消息。每个入口端口处的虚拟 PCI-to-PCI 桥将两个 INTA 消息映射到 INTA，意味着没有变化。这是因为两个原始端点设备的设备号都为零（作为请求者 ID ReqID 的一部分包含在中断消息本身中）。表 17-1 显示来自设备 0 的中断消息映射到桥另一侧的相同 INTx 消息（即，在交换机内部，两个 INTA 消息都映射到 INTA）。因此每个下游端口将在不改变其虚拟线路的情况下向上游传播中断消息。但是，传播的中断消息不再具有原始请求者的 ReqID，它们现在具有传播中断消息的端口的 ReqID。

接下来，上游交换机端口接收传播的中断消息。来自端口 2:1:0 的 INTA 中断在被传播到上游时将被映射到 INTB 消息，因为中断消息指示它来自设备 1（ReqID 2:1:0）。由端口 2:2:0 传播的另一个中断将在从上游交换机端口发送到根端口时映射到 INTC 消息。请参考表 17-1 确认这些映射。

进行此中断映射的原因与 PCI 中的原因相同：尽可能避免多个功能共享同一 INTx# 引脚。如前所述，单功能设备在使用旧式中断时必须使用 INTA。因此，如果根端口下游的所有 Function 都使用 INTA 并且桥上没有映射，则它们都将路由到同一 IRQ。这意味着每当其中一个 Function 断言 INTA 时，必须检查所有 Function。这将导致列表末尾的 Function 的中断服务延迟很大。这种中断映射方法是一种粗略的尝试，旨在将中断（尤其是 INTA）分布在所有四个 INTx 虚拟线上，因为每个 INTx 虚拟线可以在中断控制器处映射到单独的 IRQ。

**808**

**第 17 章：中断支持**

_Table 17-1: INTx Message Mapping Across Virtual PCI-to-PCI Bridges_

|**Device Number of**<br>**Delivering INTx**|**INTx Message**<br>**Type at Input**|**INTx Message**<br>**Type at Output**|
|---|---|---|
|0, 4, 8, 12 etc.|INTA|INTA|
||INTB|INTB|
||INTC|INTC|
||INTD|INTD|
|1, 5, 9, 13 etc.|INTA|INTB|
||INTB|INTC|
||INTC|INTD|
||INTD|INTA|
|2, 6, 10, 14 etc.|INTA|INTC|
||INTB|INTD|
||INTC|INTA|
||INTD|INTB|
|3, 7, 11, 15 etc.|INTA|INTD|
||INTB|INTA|
||INTC|INTB|
||INTD|INTC|


**809**

**PCI Ex ress 3.0 Technolo p gy**

_Figure 17-11: Example of INTx Mapping_

**==> picture [295 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
Root Complex<br>
Memory<br>
Interrupt Controller<br>
Assert_INTB (ReqID 1:0:0)<br>
Assert_INTC (ReqID 1:0:0)<br>
INTA from Dev 1 maps to INTB 1:0:0 INTA from Dev 2 maps to INTC<br>
Assert_INTA (ReqID 2:1:0)<br>
Switch Assert_INTA (ReqID 2:2:0)<br>
INTA from Dev 0 maps to INTA 2:1:0 2:2:0 INTA from Dev 0 maps to INTA<br>
Assert_INTA (ReqID 3:0:0)<br>
Assert_INTA (ReqID 4:0:0)<br>
3:0:0 4:0:0<br>
PCIe PCIe<br>
Endpoint Endpoint<br>
**----- End of picture text -----**<br>


## **INTx 合并**

PCIe 交换机必须确保 INTx 消息以正确的方式向上游传递。具体来说，必须处理旧式 PCI 实现的中断路由，以便软件可以确定哪些中断路由到哪个中断控制器输入。INTx# 线可以线或连接，并路由到中断控制器上的同一 IRQ 输入，当多个设备在同一线上发出中断信号时，中断控制器只会看到第一次断言。类似地，当这些设备之一取消其 INTx# 线的断言时，该线保持断言状态，直到最后一个被关闭为止。这些相同的原则也适用于 PCIe INTx 消息。

但是，在某些情况下，两个重叠的 INTx 消息可能被出口端口处的虚拟 PCI 桥映射到相同的 INTx 消息，这要求将消息合并。考虑下面图 17-12（第 811 页）所示的示例。

**810**

**第 17 章：中断支持**

当上游交换机端口映射用于在上游链路上传递的中断消息时，根据下游交换机端口的设备号，这两个中断都将映射为 INTB。注意，因为这两个重叠的消息是相同的，所以必须将它们合并。

合并可确保中断控制器永远不会为共享中断接收到两个连续的 Assert_INTx 或 Deassert_INTx 消息。这等效于 INTx 信号被线或连接。

_Figure 17-12: Switch Uses Bridge Mapping of INTx Messages_

**==> picture [273 x 382] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
Root Complex<br>
Memory<br>
Interrupt Controller<br>
Assert_INTB (1:0:0)<br>
3<br>
Deassert_INTB (1:0:0)<br>
1:0:0<br>
Switch<br>
2:1:0 2:5:0<br>
Assert_INTA (3:0:0) Assert_INTA (4:0:0)<br>
1 2<br>
Deassert_INTA (3:0:0) Deassert_INTA (4:0:0)<br>
3:0:0 4:0:0<br>
PCIe PCIe<br>
Endpoint Endpoint<br>
Deassert_INTA (3:0:0)<br>
1<br>
Assert_INTA (3:0:0)<br>
(blocked by 1:0:0)<br>
2<br>
Assert_INTA (4:0:0) Deassert_INTA (4:0:0)<br>
(blocked by 1:0:0)<br>
3<br>
Assert_INTB (1:0:0) Deassert_INTB (1:0:0)<br>
caused by Assert_INTA (4:0:0) caused by Deassert_INTA (3:0:0)<br>
**----- End of picture text -----**<br>


**811**

**PCI Ex ress 3.0 Technolo p gy**

## **INTx 传递规则**

与 INTx 消息传递相关的规则具有一些独特特征：

- Assert_INTx 和 Deassert_INTx 仅在上游方向发出。

- 正在合并中断的交换机仅当中断状态发生变化时才向上游发出 INTx 消息。

- 链路任一侧的设备必须跟踪 INTA-INTD 断言的当前状态。

- 交换机跟踪其每个下游端口的四个虚拟线路的状态，并可在其上游端口上呈现一组合并的虚拟线路。

- 根复合体必须跟踪每个下游端口的四个虚拟线路（A-D）的状态。

- 可以使用命令寄存器中的中断禁用位来禁用 INTx 信令。

- 如果任何 INTx 虚拟线路处于活动状态，然后禁用了设备中断，则必须发送相应的 Deassert_INTx 消息。

- 如果下游交换机端口进入 DL_Down 状态，则必须取消任何活动的 INTx 虚拟线路的断言，并相应地更新上游端口（如果该 INTx 处于活动状态，则需要 Deassert_INTx 消息）。

## **MSI 模型**

PCIe Function 通过 MSI Capability 寄存器指示 MSI 支持。每个 Function 必须实现 MSI Capability 结构或 MSI-X（扩展 MSI，参见第 821 页的"The MSI-X Model"）Capability 结构，或两者都实现。MSI Capability 寄存器由配置软件设置，包括：

- 目标内存地址

- 要写入该地址的数据值

- 可以编码到数据中的唯一消息数

有关内存写事务头的回顾，请参见第 188 页的"Memory Request Header Fields"。注意，MSI 始终具有 1DW 的数据有效负载。

## **MSI 能力结构**

MSI 能力结构驻留在 PCI 兼容的配置空间区域（前 256 字节）。MSI Capability 结构有四种变体，基于它是否支持 64 位寻址或仅 32 位以及它是否支持

**812**

**第 17 章：中断支持**

每向量屏蔽 (per-vector masking)。原生 PCIe 设备需要支持 64 位寻址。MSI Capability 结构的所有四种变体都可以在图 17-13（第 813 页）中找到。

_Figure 17-13: MSI Capability Structure Variations_

|||32-bit Address|||||
|---|---|---|---|---|---|---|
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Message Data||||DW2|
|||64-bit Address|||||
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Message Address [63:32]||||DW2|
|||Message Data||||DW3|
|||32-bit Address with Per-Vector|Masking||||
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Reserved<br>Message Data||||DW2|
|||Mask Bits||||DW3|
|||Pending Bits||||DW4|
|||64-bit Address with Per-Vector|Masking||||
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Message Address [63:32]||||DW2|
|||Reserved<br>Message Data||||DW3|
|||Mask Bits||||DW4|
