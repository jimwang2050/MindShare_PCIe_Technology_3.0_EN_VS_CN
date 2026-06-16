## **DLLP 包大小固定为 8 字节**

数据链路层包对于 8b/10b 和 128b/130b 始终是 8 字节长，由以下组件组成：

1. 一个 1 DW 核心（4 字节），包含一个字节的 DLLP Type 字段和三个字节的其他属性。属性随 DLLP 类型而变化。

2. 一个 2 字节的 CRC 值，它是根据 DLLP 的核心内容计算得出的。需要指出的是，此 CRC 与添加到 TLP 的 LCRC 不同。此 CRC 仅为 16 位，其计算方式与 TLP 中的 32 位 LCRC 不同。此 CRC 被附加到核心 DLLP 上，然后这 6 字节被传递到物理层。

**310**

**第 9 章：DLLP 元素**

3. 如果使用 8b/10b 编码，则将一个 DLLP 起始 (Start of DLLP, SDP) 控制符号和一个结束良好 (End Good, END) 控制符号添加到包的开始和结束。与往常一样，在传输之前，物理层将字节编码为 10 位符号以进行传输。

4. 在 Gen3 模式下，当使用 128b/130b 编码时，会在包的前面添加一个 2 字节的 SDP 标记以构成 8 字节的包，并且没有 END 符号或标记。

请注意，DLLP 永远没有数据有效负载；所有信息都携带在包的四个核心字节中。

## **DLLP 包类型**

定义了四组 DLLP，分别处理 Ack/Nak、电源管理和流控，以及一个供应商特定版本。其中一些有多个变体，第 311 页的表 9-1 总结了每个变体以及它们的 _DLLP Type_ 字段编码。

_表 9-1：DLLP 类型_

|**DLLP 类型**|**类型字段**<br>**编码**|**用途**|
|---|---|---|
|Ack (TLP 确认)|0000 0000b|TLP 传输完整性|
|Nak (TLP 否定确认)|0001 0000b|TLP 传输完整性|
|PM_Enter_L1|0010 0000b|电源管理|
|PM_Enter_L23|0010 0001b|电源管理|
|PM_Active_State_Request_L1|0010 0011b|电源管理|
|PM_Request_Ack|0010 0100b|电源管理|
|供应商特定|0011 0000b|供应商定义|
|InitFC1‐P|0100 0xxxb|TLP 流控<br>（xxx = VC 号）|
|InitFC1‐NP|0101 0xxxb|TLP 流控|



**311**

**PCI Exress Technology**

_表 9-1：DLLP 类型（续）_

|**DLLP 类型**|**类型字段**<br>**编码**|**用途**|
|---|---|---|
|InitFC1‐Cpl|0110 0xxxb|TLP 流控|
|InitFC2‐P|1100 0xxxb|TLP 流控|
|InitFC2‐NP|1101 0xxxb|TLP 流控|
|InitFC2‐Cpl|1110 0xxxb|TLP 流控|
|UpdateFC‐P|1000 0xxxb|TLP 流控|
|UpdateFC‐NP|1001 0xxxb|TLP 流控|
|UpdateFC‐Cpl|1010 0xxxb|TLP 流控|
|保留|其他|保留|



## **Ack/Nak DLLP 格式**

设备用于确认 (Ack) 或否定确认 (Nak) TLP 接收的 DLLP 格式如图 9-3 所示，其字段在第 313 页的"Ack/Nak DLLP 字段"中描述。有关如何使用这些 DLLP 来处理 Ack/Nak 协议的更多讨论，请参考第 10 章（标题为"Ack/Nak 协议"，第 317 页）。

_图 9-3：Ack 或 Nak DLLP 格式_

**==> 图片 [366 x 104] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved AckNak_Seq_Num<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


**312**

**第 9 章：DLLP 元素**

_表 9-2：Ack/Nak DLLP 字段_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP 类型|Byte 0, [7:0]|指示 DLLP 的类型：<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|如果收到一个良好的 TLP：<br>• 如果传入的序列号 = NEXT_RCV_SEQ（与预期的匹配），则使用该序列号调度 Ack DLLP。<br>• 如果传入的序列号早于 NEXT_RCV_SEQ 计数（收到了重复的 TLP），则使用 NEXT_RCV_SEQ - 1 调度 Ack DLLP（实际上，这是最后一个良好 TLP 的序列号）。<br>对于收到的有问题的 TLP：<br>• 如果 TLP 出错或其序列号高于 NEXT_RCV_SEQ，则使用 NEXT_RCV_SEQ - 1 调度 Nak DLLP。|
|16 位 CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|此 16 位 CRC 保护此 DLLP 的内容。计算基于 Ack/Nak 的字节 0-3。|



## **电源管理 DLLP 格式**

电源管理 DLLP 信息如图 9-4 所示，其字段在第 314 页的表 9-3 中描述。要了解这些报文在电源管理中的使用详情，请参考第 16 章（标题为"电源管理"，第 703 页）。

**313**

**PCI Exress Technology**

_图 9-4：电源管理 DLLP 格式_

**==> 图片 [372 x 95] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1 0 0 x x x Reserved<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


_表 9-3：电源管理 DLLP 字段_

|**字段**<br>**名称**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP<br>类型|Byte 0, [7:0]|指示 DLLP 类型。对于电源管理 DLLP：<br>0010 0000b = PM_Enter_L1<br>0010 0001b = PM_Enter_L23<br>0010 0011b = PM_Active_State_Request_L1<br>0010 0100b = PM_Request_Ack|
|16 位<br>CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|用于保护 DLLP 内容的 16 位 CRC。计算基于字节 0-3，无论是否使用了字段。|



## **流控 DLLP 格式**

像许多其他串行传输总线一样，PCI 通过使用基于信用的流控方案来提高传输效率。此主题在第 6 章（标题为"流控"，第 215 页）中有详细介绍。DLLP 用于传达流控信用信息。多种不同的 DLLP 初始化流控信用。另一类更新 DLLP 用于在恢复接收器缓冲区空间时管理运行时信用管理。有两种流控初始化 DLLP 称为 InitFC1 和 InitFC2，以及一种流控更新 DLLP 称为 UpdateFC。

所有三种变体的包格式如图 9-5（第 315 页）所示，而表 9-4（第 315 页）描述了其中包含的字段。

**314**

**第 9 章：DLLP 元素**

_图 9-5：流控 DLLP 格式_

**==> 图片 [369 x 105] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 x x x x 0 VC ID R HeaderFC R DataFC<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


_表 9-4：流控 DLLP 字段_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP 类型|Byte 0, [7:4]|此代码指示 FC DLLP 的类型：<br>0100b = InitFC1‐P (Posted 请求)<br>0101b = InitFC1‐NP (Non-Posted 请求)<br>0110b = InitFC1‐Cpl (Completions)<br>0101b = InitFC2‐P (Posted 请求)<br>1101b = InitFC2‐NP (Non-Posted 请求)<br>1110b = InitFC2‐Cpl (Completions)<br>1000b = UpdateFC‐P (Posted 请求)<br>1001b = UpdateFC‐NP (Non-Posted 请求)<br>1010b = UpdateFC‐Cpl (Completions)|
||Byte 0, [3]|必须为 0b，作为流控编码的一部分。|
||Byte 0, [2:0]|VC ID。指示要用这些信用更新的虚通道（VC 0‐7）。|
|HdrFC|Byte 1, [5:0]<br>Byte 2, [7:6]|包含指定虚通道的头部存储的信用计数。每个信用代表 1 个头部 + 可选的 TLP Digest (ECRC) 的空间。|
|DataFC|Byte 2, [3:0]<br>Byte 3, [7:0]|包含指定虚通道的数据存储的信用计数。每个信用代表 16 字节。|



**315**

**PCI Exress Technology**

_表 9-4：流控 DLLP 字段（续）_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|16 位 CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|保护此 DLLP 内容的 16 位 CRC。计算基于字节 0-3，无论是否使用了所有字段。|



## **供应商特定 DLLP 格式**

最后定义的 DLLP 类型用于供应商特定目的。因此，规范仅定义了 DLLP 类型字段（0011 0000b），其余内容留给供应商自定义使用。

_图 9-6：供应商特定 DLLP 格式_

**==> 图片 [372 x 99] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1 1 0 0 0 0 Vendor-Defined<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


**316**

## _**10 Ack/Nak 协议**_

## **上一章**

在上一章中，我们描述了数据链路层包 (Data Link Layer Packets, DLLP)。我们描述了 DLLP 类型的使用、格式和定义以及其相关字段的详细信息。DLLP 用于支持 Ack/Nak 协议、电源管理、流控机制，并可用于供应商定义的目的。

## **本章**

本章描述数据链路层的一个关键特性：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。Ack DLLP 确认 TLP 的成功接收，而 Nak DLLP 指示传输错误。我们描述在未检测到 TLP 或 DLLP 错误时的正常操作规则，以及与 TLP 和 DLLP 错误相关联的错误恢复机制。

## **下一章**

下一章描述物理层的逻辑子块，它准备用于串行传输和接收的报文。完成此操作需要几个步骤，我们将在此详细描述。本章涵盖了与使用 8b/10b 编码的规范的前两个版本 Gen1 和 Gen2 相关的逻辑。Gen3 的逻辑不使用 8b/10b 编码，将在名为"物理层 - 逻辑 (Gen3)"的第 407 页的章节中单独描述。

## **目标：可靠的 TLP 传输**

数据链路层的功能（如图 10-1（第 318 页）所示）是确保 TLP 的可靠交付。规范要求误码率 (BER) 不差于 10[‐12]，但错误仍会经常发生以引起麻烦，并且单个位错误将破坏整个报文。随着新一代链路速率的持续提高，这个问题只会变得更加严重。

**317**

**PCI Exress Technology**

## _图 10-1：数据链路层_

**==> 图片 [375 x 277] 已省略 <==**

**----- 图片文字开始 -----**<br>
Memory, I/O, Configuration R/W Requests or Message Requests or Completions<br>(Software layer sends / receives address/transaction type/data/message index)<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Transaction layer Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers Buffers<br>per VC Management per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC ACK/NAK CRC ACK/NAK CRC Sequence TLP LCRC<br>Data Link layer TLP Replay De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**----- 图片文字结束 -----**<br>
