|||Pending Bits||||DW5|


**813**

**PCI Ex ress 3.0 Technolo p gy**

## **Capability ID**

值为 **05h** 的 Capability ID 标识 MSI 能力，并且是只读值。

## **下一个能力指针**

寄存器的第二个字节是只读值，它给出从配置空间顶部开始的双字对齐偏移量，该偏移量指向链接列表中的下一个 Capability 结构，否则包含 00h 以指示链接列表的结尾。

## **消息控制寄存器**

图 17-14（第 814 页）和表 17-2（第 814 页）说明了消息控制寄存器的布局和用法。

_Figure 17-14: Message Control Register_

**==> picture [358 x 114] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9 8 7 6 4 3 1 0<br>
Reserved<br>
MSI Enable<br>
Multiple Message Capable<br>
Multiple Message Enable<br>
64-bit Address Capable<br>
Per-vector Masking Capable<br>
**----- End of picture text -----**<br>


_Table 17-2: Format and Usage of Message Control Register_

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|0|MSI Enable|Read/Write. State after reset is 0, indicating that the<br>device's MSI capability is disabled.<br>• **0**= Function is**disabled**from using**MSI**. It must<br>use MSI-X or else INTx Messages.<br>• **1**= Function is**enabled**to use**MSI**to request<br>service and won't use MSI-X or INTx Messages.|


**814**

**第 17 章：中断支持**

_Table 17-2: Format and Usage of Message Control Register (Continued)_

|**Bit(s)**|**Field Name**||**Description**|
|---|---|---|---|
|3:1|Multiple Message<br>Capable||Read-Only. System software reads this field to<br>determine how many messages (interrupt vectors)<br>the Function would like to use. The requested<br>number of messages is a power of two, therefore a<br>Function that would like three messages must<br>request that four messages be allocated to it.<br>**Value**<br>   **Number of Messages Requested**<br>000b                                    1<br>001b                                    2<br>010b                                    4<br>011b                                    8<br>100b                                   16<br>101b                                   32<br>110b                              Reserved<br>111b                              Reserved|
|6:4|Multiple Message<br>Enable||Read/Write. After system software reads the Multi‐<br>ple Message Capable field (previous row in this<br>table) to see how many messages (interrupt vec‐<br>tors) are requested by the Function, it programs a<br>3-bit value in this field indicating the actual num‐<br>ber of messages allocated to the Function. The<br>number allocated can be equal to or less than the<br>number actually requested. The state of this field<br>after reset is 000b.<br>**Value**<br>   **Number of Messages Requested**<br>000b                                    1<br>001b                                    2<br>010b                                    4<br>011b                                    8<br>100b                                   16<br>101b                                   32<br>110b                              Reserved<br>111b                              Reserved|


**815**

**PCI Ex ress 3.0 Technolo p gy**

_Table 17-2: Format and Usage of Message Control Register (Continued)_

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|7|64-bit Address<br>Capable|Read-Only.<br>• 0 = Function does not implement the upper 32<br>bits of the Message Address register; only a 32-<br>bit address is possible.<br>• 1 = Function implements the upper 32 bits of the<br>Message Address register and is capable of gen‐<br>erating a 64-bit memory address.|
|8|Per-Vector<br>Masking Capable|Read-Only.<br>• 0 = Function does not implement the Mask Bit<br>register or the Pending Bit register; software<br>does NOT have the ability to mask individual<br>interrupts with this capability structure.<br>• 1 = Function does implement the Mask Bit regis‐<br>ter or the Pending Bit register; software does<br>have the ability to mask individual interrupts<br>with this capability structure.|
|15:9|Reserved|Read-Only. Always zero.|


## **消息地址寄存器**

32 位消息地址寄存器的低两位为零且无法更改，强制软件分配的地址是双字对齐的。通常，这是系统 CPU 中本地 APIC 的地址。在基于 x86 的系统（Intel 兼容）中，该地址传统上为 FEEx_xxxxh，其中低 20 位指示哪个本地 APIC 是目标以及有关中断本身的一些其他信息。重要的是要注意，地址的解释方式取决于平台，而不是由 PCI 或 PCIe 规范规定。

包含消息地址的位 [63:32] 的寄存器对于原生 PCI Express 设备是必需的，但对于旧式端点是可选的。如果设置了消息控制寄存器的第 7 位，则该寄存器存在。如果是，则它是一个读/写寄存器，与消息地址 [31:0] 寄存器结合使用，以启用来自该 Function 的 64 位内存地址用于中断传递。

**816**

**第 17 章：中断支持**

## **消息数据寄存器**

系统软件将基本消息数据模式写入此 16 位读/写寄存器。当 Function 生成中断请求时，它将 32 位数据值写入消息地址寄存器中指定的内存地址。此数据的高 16 位始终设置为零，而低 16 位由消息数据寄存器提供。

如果已将多个消息分配给 Function，则它修改消息数据寄存器值的低位（可修改的位数取决于配置软件已分配给 Function 的消息数）以形成其希望报告的事件的适当值。例如，请参见第 820 页的"Basics of Generating an MSI Interrupt Request"。

## **屏蔽位寄存器和挂起位寄存器**

如果 Function 支持每向量屏蔽（在消息控制寄存器的位 [8] 中指示），则这些寄存器存在。可以使用 MSI 请求并分配给 Function 的最大中断消息（中断向量）数为 32。因此这两个寄存器长度为 32 位，每个潜在的中断消息都有自己的屏蔽位和挂起位。如果设置了屏蔽位寄存器的位 [0]，则屏蔽中断消息 0（这是来自该 Function 的基本向量）。如果设置了位 [1]，则屏蔽中断消息 1（这是基本向量 + 1）。

当屏蔽中断消息时，不能发送该向量的 MSI。相反，相应的挂起位被设置。这允许软件屏蔽来自 Function 的各个中断，然后定期轮询该 Function 以查看是否有挂起的屏蔽中断。

如果软件清除了屏蔽位并且设置了相应的挂起位，则 Function 必须立即发送 MSI 请求。中断消息发送后，Function 将清除挂起位。

## **MSI 配置基础**

以下列表指定了软件为 PCI Express 设备配置 MSI 中断所采取的步骤。请参考第 819 页的图 17-15。

1. 在启动时，枚举软件扫描系统中的所有 PCI 兼容 Function（有关枚举过程的讨论，请参见第 109 页的"Single Root Enumeration Example"）。

**817**

## **PCI Ex ress 3.0 Technolo p gy**

2. 一旦发现 Function，软件就会读取 Capabilities List Pointer，以查找链接列表中第一个能力结构的位置。

3. 如果在列表中找到 MSI Capability 结构（Capability ID 为 05h），则软件读取设备的消息控制寄存器中的 Multiple Message Capable 字段，以确定设备支持多少个事件特定的消息以及它是否支持 64 位消息地址或仅 32 位。然后软件分配等于或小于该值的消息数，并将该值写入 Multiple Message Enable 字段。至少会将一条消息分配给设备。

4. 软件将基本消息数据模式写入设备的消息数据寄存器，并将双字对齐的内存地址写入设备的消息地址寄存器，作为 MSI 写入的目标地址。

5. 最后，软件设置设备消息控制寄存器中的 MSI Enable 位，从而启用它生成 MSI 写入并禁用其他中断传递选项。

**818**

**第 17 章：中断支持**

_Figure 17-15: Device MSI Configuration Process_

**==> picture [159 x 456] intentionally omitted <==**

**----- Start of picture text -----**<br>
Scan PCI bus(es)<br>
until device<br>
discovered<br>
New<br>
N<br>
Capabilities<br>
?<br>
Y<br>
MSI N<br>
Capable<br>
?<br>
Y<br>
Determine number of<br>
messages requested<br>
and assign number<br>
of messages to device<br>
Write base data<br>
pattern into<br>
Message Data<br>
Register<br>
Assign Memory<br>
Address to Message<br>
Address Register<br>
Enable device to<br>
use MSI with<br>
MSI Enable bit<br>
in Message Control<br>
Register<br>
**----- End of picture text -----**<br>


**819**

**PCI Ex ress 3.0 Technolo p gy**

## **生成 MSI 中断请求的基础**

图 17-16（第 821 页）说明了 MSI 内存写事务头和数据字段的内容。要点包括：

- 格式字段必须为 011b（对于原生 Function），表示 4DW 头（64 位地址）带数据，但对于旧式端点，它可能为 010b，表示 32 位地址。

- No Snoop 和 Relaxed Ordering 的属性位必须为零。

- 长度字段必须为 01h，以指示最大数据有效负载为 1DW。

- 第一个 BE 字段必须为 1111b，指示 DW 的所有四个字节中的数据有效，即使对于 MSI 上部两个字节始终为零。

- 最后一个 BE 字段必须为 0000b，指示单个 DW 事务。

- 头内的地址字段直接来自 MSI 能力寄存器内的地址字段。

- 数据有效负载的低 16 位来自 MSI 能力寄存器内的数据字段。

## **多条消息**

如果系统软件为 Function 分配了多个消息，则通过修改所分配的消息数据值的低位以针对每种设备特定事件类型发送不同的消息，从而创建多个值。

例如，假设以下情况：

- 已为设备分配了四条消息。

- 数据值 49A0h 已分配给设备的消息数据寄存器。

- 内存地址 FEEF_F00Ch 已写入设备的消息地址寄存器。

- 当四个事件之一发生时，设备通过对内存地址 FEEF_F00Ch 执行双字写入来生成请求，数据值为 0000_49A0h、0000_49A1h、0000_49A2h 或 0000_49A3h。换句话说，修改数据值的低两位以指定发生的事件。如果此 Function 已分配 8 条消息，则可以修改低三位。此外，设备始终使用 0000h 作为其消息数据值的高 2 字节。

**820**

**第 17 章：中断支持**

_Figure 17-16: Format of Memory Write Transaction for Native-Device MSI Delivery_

**==> picture [329 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>
