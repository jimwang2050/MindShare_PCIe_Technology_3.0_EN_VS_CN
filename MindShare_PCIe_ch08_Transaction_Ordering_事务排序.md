# 📘 第 8 章　事务排序 (Chapter 8. Transaction Ordering)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0257.md` ... `chunks/chunk0263.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [8.1 Transaction Ordering — 事务排序](#sec-8-1)
- [8.2 Transaction Ordering — 事务排序](#sec-8-2)
- [8.3 Transaction Ordering — 事务排序](#sec-8-3)
- [8.4 Transaction Ordering — 事务排序](#sec-8-4)
- [8.5 Transaction Ordering — 事务排序](#sec-8-5)
- [8.6 Transaction Ordering — 事务排序](#sec-8-6)

<a id="sec-8-1"></a>
## 8.1 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

Device A Device B<br>Device Core Device Core<br>PCI-XP Core PCI-XP Core<br>Hardware/Software Hardware/Software<br>Interface
Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX)
(TX)<br>Framing C Framing<br>DLLP R<br>(SDP) C (END)<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1
0<br>Byte 0 DLLP Type (Fields Vary With DLLP Type)<br>Byte 4 16 Bit CRC<br>## **DLLP Packet Size is Fixed at 8 Bytes**

Data Link Layer Packets are always 8 bytes long for both 8b/10b and 128b/130b and consist of the following components: 

1. A 1 DW core (4 bytes) containing the one‐byte DLLP Type field and three additional bytes of attributes. The attributes vary with the DLLP
type.

2. A 2‐byte CRC value that is calculated based on the core contents of the DLLP. It is important to point out that this CRC is different
from the LCRCs added to TLPs. This CRC is only 16 bits in size and is calculated differently than the 32‐bit LCRCs in TLPs. This CRC is
appended to the core DLLP and then these 6 bytes are passed to the Physical Layer.
3. If 8b/10b encoding is in use, a Start of DLLP (SDP) control symbol and an End Good (END) control symbol are added to the beginning and
end of the packet. As usual, before transmission the Physical Layer encodes the bytes into 10‐bit symbols for transmission.

4. In Gen3 mode, when 128b/130b encoding is in use, a 2‐byte SDP Token is added to the front of the packet to create the 8‐byte packet and
there is no END symbol or token.

Note that there is never a data payload with a DLLP; all the information is car‐ ried in the core four bytes of the packet.

</td>
<td width="50%">

## **DLLP 包大小固定为 8 字节**

数据链路层包对于 8b/10b 和 128b/130b 始终是 8 字节长，由以下组件组成：

1. 一个 1 DW 核心（4 字节），包含一个字节的 DLLP Type 字段和三个字节的其他属性。属性随 DLLP 类型而变化。

2. 一个 2 字节的 CRC 值，它是根据 DLLP 的核心内容计算得出的。需要指出的是，此 CRC 与添加到 TLP 的 LCRC 不同。此 CRC 仅为 16 位，其计算方式与 TLP 中的 32 位 LCRC 不同。此 CRC 被附加到核心 DLLP 上，然后这 6
字节被传递到物理层。

**第 9 章：DLLP 元素**

3. 如果使用 8b/10b 编码，则将一个 DLLP 起始 (Start of DLLP, SDP) 控制符号和一个结束良好 (End Good, END) 控制符号添加到包的开始和结束。与往常一样，在传输之前，物理层将字节编码为 10 位符号以进行传输。

4. 在 Gen3 模式下，当使用 128b/130b 编码时，会在包的前面添加一个 2 字节的 SDP 标记以构成 8 字节的包，并且没有 END 符号或标记。

请注意，DLLP 永远没有数据有效负载；所有信息都携带在包的四个核心字节中。

</td>
</tr>
<tr>
<td width="50%">

## **DLLP Packet Types** 

There are four groups of DLLPs defined that deal with Ack/Nak, Power Man‐ agement, and Flow Control, along with one Vendor Specific version.
Some of these have several variants, and Table 9‐1 on page 311 summarizes each variant as well as their _DLLP Type_ field encoding.

_Table 9‐1: DLLP Types_ 

|**DLLP Type**|**Type Field**<br>**Encoding**|**Purpose**|
|---|---|---|
|Ack (TLP Acknowledge)|0000 0000b|TLP transmission integrity|
|Nak (TLP Negative Acknowl‐<br>edge)|0001 0000b|TLP transmission integrity|
|PM_Enter_L1|0010 0000b|Power Management|
|PM_Enter_L23|0010 0001b|Power Management|
|PM_Active_State_Request_L1|0010 0011b|Power Management|
|PM_Request_Ack|0010 0100b|Power Management|
|Vendor Specific|0011 0000b|Vendor Defined|
|InitFC1‐P|0100 0xxxb|TLP Flow Control<br>(xxx = VC number)|
|InitFC1‐NP|0101 0xxxb|TLP Flow Control|


_Table 9‐1: DLLP Types (Continued)_ 

|**DLLP Type**|**Type Field**<br>**Encoding**|**Purpose**|
|---|---|---|
|InitFC1‐Cpl|0110 0xxxb|TLP Flow Control|
|InitFC2‐P|1100 0xxxb|TLP Flow Control|
|InitFC2‐NP|1101 0xxxb|TLP Flow Control|
|InitFC2‐Cpl|1110 0xxxb|TLP Flow Control|
|UpdateFC‐P|1000 0xxxb|TLP Flow Control|
|UpdateFC‐NP|1001 0xxxb|TLP Flow Control|
|UpdateFC‐Cpl|1010 0xxxb|TLP Flow Control|
|Reserved|Others|Reserved|

</td>
<td width="50%">

## **DLLP 包类型**

定义了四组 DLLP，分别处理 Ack/Nak、电源管理和流控，以及一个供应商特定版本。其中一些有多个变体，第 311 页的表 9-1 总结了每个变体以及它们的 _DLLP Type_ 字段编码。

_表 9-1：DLLP 类型_

|**DLLP 类型**|**类型字段 编码**|**用途**|
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


_表 9-1：DLLP 类型（续）_

|**DLLP 类型**|**类型字段 编码**|**用途**|
|---|---|---|
|InitFC1‐Cpl|0110 0xxxb|TLP 流控|
|InitFC2‐P|1100 0xxxb|TLP 流控|
|InitFC2‐NP|1101 0xxxb|TLP 流控|
|InitFC2‐Cpl|1110 0xxxb|TLP 流控|
|UpdateFC‐P|1000 0xxxb|TLP 流控|
|UpdateFC‐NP|1001 0xxxb|TLP 流控|
|UpdateFC‐Cpl|1010 0xxxb|TLP 流控|
|保留|其他|保留|

</td>
</tr>
<tr>
<td width="50%">

## **Ack/Nak DLLP Format** 

The format of the DLLP used by a device to Ack (acknowledge) or Nak (nega‐ tively acknowledge) the receipt of a TLP is illustrated in Figure
9‐3, and its fields are described in “Ack/Nak DLLP Fields” on page 313. For more discus‐ sion on how these are used to handle the Ack/Nak
protocol, refer to Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317.

_Figure 9‐3: Ack Or Nak DLLP Format_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

_Table 9‐2: Ack/Nak DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:0]|Indicates the type of DLLP: • 0000 00...|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|If a good TLP was received:<br>• If incoming Sequence Number =<br>NEXT_RCV_SEQ (matched what
was<br>expected), schedule Ack DLLP with that<br>number.<br>• If incoming Sequence Number was ear‐<br>lier than NEXT_RCV_SEQ count
(a<br>duplicate TLP was received), schedule<br>Ack DLLP with NEXT_RCV_SEQ ‐ 1<br>(effectively, this is the number of the last<br>good
TLP).<br>For a TLP received with a problem:<br>• If the TLP had an error, or its Sequence<br>Number was higher than<br>NEXT_RCV_SEQ,
schedule a Nak<br>DLLP with NEXT_RCV_SEQ ‐ 1.|
|16‐bit CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|This 16‐bit CRC protects the contents of<br>this DLLP. Calculation is based on Bytes 0‐<br>3 of
the Ack/Nak.|

</td>
<td width="50%">

## **Ack/Nak DLLP 格式**

设备用于确认 (Ack) 或否定确认 (Nak) TLP 接收的 DLLP 格式如图 9-3 所示，其字段在第 313 页的"Ack/Nak DLLP 字段"中描述。有关如何使用这些 DLLP 来处理 Ack/Nak 协议的更多讨论，请参考第 10 章（标题为"Ack/Nak
协议"，第 317 页）。

_图 9-3：Ack 或 Nak DLLP 格式_

**==> 图片 [366 x 104] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved
AckNak_Seq_Num<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


**第 9 章：DLLP 元素**

_表 9-2：Ack/Nak DLLP 字段_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP 类型|Byte 0, [7:0]|指示 DLLP 的类型：<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|如果收到一个良好的 TLP：<br>• 如果传入的序列号 = NEXT_RCV_SEQ（与预期的匹配），则使用该序列号调度 Ack DLLP。<br>• 如果传入的序列号早于
NEXT_RCV_SEQ 计数（收到了重复的 TLP），则使用 NEXT_RCV_SEQ - 1 调度 Ack DLLP（实际上，这是最后一个良好 TLP 的序列号）。<br>对于收到的有问题的 TLP：<br>• 如果 TLP 出错或其序列号高于
NEXT_RCV_SEQ，则使用 NEXT_RCV_SEQ - 1 调度 Nak DLLP。|
|16 位 CRC|Byte 4, [7:0] Byte 5, [7:0]|此 16 位 CRC 保护此 DLLP 的内容。计算基于 Ack/Nak ...|

</td>
</tr>
<tr>
<td width="50%">

## **Power Management DLLP Format** 

Power management DLLP information is shown in Figure 9‐4, and its fields are described in Table 9‐3 on page 314. To learn more about the use
of these packets in power management, refer to Chapter 16, entitled ʺPower Management,ʺ on page 703.

_Figure 9‐4: Power Management DLLP Format_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


_Table 9‐3: Power Management DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP<br>Type|Byte 0, [7:0]|Indicates DLLP type. For Power Management DLLPs:<br>0010 0000b = PM_Enter_L1<br>0010 0001b =
PM_Enter_L23<br>0010 0011b = PM_Active_State_Request_L1<br>0010 0100b = PM_Request_Ack|
|16‐bit<br>CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|A 16‐Bit CRC used to protect DLLP contents. Calcula‐<br>tion is based on Bytes 0‐3, regardless
of whether fields<br>are used.|

</td>
<td width="50%">

## **电源管理 DLLP 格式**

电源管理 DLLP 信息如图 9-4 所示，其字段在第 314 页的表 9-3 中描述。要了解这些报文在电源管理中的使用详情，请参考第 16 章（标题为"电源管理"，第 703 页）。

_图 9-4：电源管理 DLLP 格式_

**==> 图片 [372 x 95] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1 0 0 x x x Reserved<br>Byte 4 16 位
CRC<br>**----- 图片文字结束 -----**<br>


_表 9-3：电源管理 DLLP 字段_

|**字段 名称**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP<br>类型|Byte 0, [7:0]|指示 DLLP 类型。对于电源管理 DLLP：<br>0010 0000b = PM_Enter_L1<br>0010 0001b = PM_Enter_L23<br>0010 0011b =
PM_Active_State_Request_L1<br>0010 0100b = PM_Request_Ack|
|16 位 CRC|Byte 4, [7:0] Byte 5, [7:0]|用于保护 DLLP 内容的 16 位 CRC。计算基于字节 0-3，无论是...|

</td>
</tr>
<tr>
<td width="50%">

## **Flow Control DLLP Format** 

Like many other serial transport buses, PCIe improves transport efficiency by using a credit‐based flow control scheme. This topic is
covered in detail in Chapter 6, entitled ʺFlow Control,ʺ on page 215. DLLPs are used to communi‐ cate flow control credit information. A
variety of different DLLPs initialize flow control credits. Another category of update DLLPs are used to manage the runt‐ ime credit
management as receiver buffer space is recovered. There are two Flow Control Initialization DLLPs called InitFC1 and InitFC2, and one Flow
Control Update DLLP called UpdateFC.

The packet format for all three variants is illustrated in Figure 9‐5 on page 315, while Table 9‐4 on page 315 describes the fields
contained in it.
_Figure 9‐5: Flow Control DLLP Format_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


_Table 9‐4: Flow Control DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:4]|This code indicates the type of FC DLLP:<br>0100b = InitFC1‐P (Posted Requests)<br>0101b = InitFC1‐NP (Non‐Posted
Requests)<br>0110b = InitFC1‐Cpl (Completions)<br>0101b = InitFC2‐P (Posted Requests)<br>1101b = InitFC2‐NP (Non‐Posted Requests)<br>1110b =
InitFC2‐Cpl (Completions)<br>1000b = UpdateFC‐P (Posted Requests)<br>1001b = UpdateFC‐NP (Non‐Posted Requests)<br>1010b = UpdateFC‐Cpl
(Completions)|
||Byte 0, [3]|Must be 0b as part of flow control encoding.|
|Byte 0, [2:0]|VC ID. Indicates the Virtual Channel ...|
|HdrFC|Byte 1, [5:0]<br>Byte 2, [7:6]|Contains the credit count for header storage for<br>the specified Virtual Channel. Each credit
repre‐<br>sents space for 1 header + the optional TLP Digest<br>(ECRC).|
|DataFC|Byte 2, [3:0]<br>Byte 3, [7:0]|Contains the credit count for data storage for the<br>specified Virtual Channel. Each credit
represents<br>16 bytes.|


_Table 9‐4: Flow Control DLLP Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|16‐bit CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|A 16‐Bit CRC that protects the contents of this<br>DLLP. Calculation is based on Bytes 0‐3,
regard‐<br>less of whether all fields are used.|

</td>
<td width="50%">

## **流控 DLLP 格式**

像许多其他串行传输总线一样，PCI 通过使用基于信用的流控方案来提高传输效率。此主题在第 6 章（标题为"流控"，第 215 页）中有详细介绍。DLLP 用于传达流控信用信息。多种不同的 DLLP 初始化流控信用。另一类更新 DLLP
用于在恢复接收器缓冲区空间时管理运行时信用管理。有两种流控初始化 DLLP 称为 InitFC1 和 InitFC2，以及一种流控更新 DLLP 称为 UpdateFC。

所有三种变体的包格式如图 9-5（第 315 页）所示，而表 9-4（第 315 页）描述了其中包含的字段。

**第 9 章：DLLP 元素**

_图 9-5：流控 DLLP 格式_

**==> 图片 [369 x 105] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 x x x x 0 VC ID R HeaderFC R DataFC<br>Byte 4 16 位
CRC<br>**----- 图片文字结束 -----**<br>


_表 9-4：流控 DLLP 字段_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP 类型|Byte 0, [7:4]|此代码指示 FC DLLP 的类型：<br>0100b = InitFC1‐P (Posted 请求)<br>0101b = InitFC1‐NP (Non-Posted 请求)<br>0110b = InitFC1‐Cpl
(Completions)<br>0101b = InitFC2‐P (Posted 请求)<br>1101b = InitFC2‐NP (Non-Posted 请求)<br>1110b = InitFC2‐Cpl (Completions)<br>1000b =
UpdateFC‐P (Posted 请求)<br>1001b = UpdateFC‐NP (Non-Posted 请求)<br>1010b = UpdateFC‐Cpl (Completions)|
||Byte 0, [3]|必须为 0b，作为流控编码的一部分。|
||Byte 0, [2:0]|VC ID。指示要用这些信用更新的虚通道（VC 0‐7）。|
|HdrFC|Byte 1, [5:0] Byte 2, [7:6]|包含指定虚通道的头部存储的信用计数。每个信用代表 1 个头部 + 可选的 ...|
|DataFC|Byte 2, [3:0]<br>Byte 3, [7:0]|包含指定虚通道的数据存储的信用计数。每个信用代表 16 字节。|


_表 9-4：流控 DLLP 字段（续）_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|16 位 CRC|Byte 4, [7:0] Byte 5, [7:0]|保护此 DLLP 内容的 16 位 CRC。计算基于字节 0-3，无论是否...|

</td>
</tr>
<tr>
<td width="50%">

## **Vendor-Specific DLLP Format** 

The last defined DLLP type is used for vendor specific purposes. Therefore only the DLLP Type field is defined by the spec (0011 0000b),
leaving the remaining contents available for vendor‐defined use.

_Figure 9‐6: Vendor‐Specific DLLP Format_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **供应商特定 DLLP 格式**

最后定义的 DLLP 类型用于供应商特定目的。因此，规范仅定义了 DLLP 类型字段（0011 0000b），其余内容留给供应商自定义使用。

_图 9-6：供应商特定 DLLP 格式_

**==> 图片 [372 x 99] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1 1 0 0 0 0 Vendor-Defined<br>Byte 4 16 位
CRC<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## _**10 Ack/Nak Protocol**_

</td>
<td width="50%">

## _**10 Ack/Nak 协议**_

</td>
</tr>
<tr>
<td width="50%">

## **The Previous Chapter** 

In the previous chapter we describe _Data Link Layer Packets_ (DLLPs). We describe the use, format, and definition of the DLLP types and the
details of their related fields. DLLPs are used to support Ack/Nak protocol, power man‐ agement, flow control mechanism and can be used for
vendor‐defined pur‐ poses.

</td>
<td width="50%">

## **上一章**

在上一章中，我们描述了数据链路层包 (Data Link Layer Packets, DLLP)。我们描述了 DLLP 类型的使用、格式和定义以及其相关字段的详细信息。DLLP 用于支持 Ack/Nak 协议、电源管理、流控机制，并可用于供应商定义的目的。

</td>
</tr>
<tr>
<td width="50%">

## **This Chapter** 

This chapter describes a key feature of the Data Link Layer: an automatic, hard‐ ware‐based mechanism for ensuring reliable transport of
TLPs across the Link. Ack DLLPs confirm successful reception of TLPs while Nak DLLPs indicate a transmission error. We describe the normal
rules of operation when no TLP or DLLP error is detected as well as error recovery mechanisms associated with both TLP and DLLP errors.

</td>
<td width="50%">

## **本章**

本章描述数据链路层的一个关键特性：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。Ack DLLP 确认 TLP 的成功接收，而 Nak DLLP 指示传输错误。我们描述在未检测到 TLP 或 DLLP 错误时的正常操作规则，以及与 TLP 和 DLLP
错误相关联的错误恢复机制。

</td>
</tr>
<tr>
<td width="50%">

## **The Next Chapter** 

The next chapter describes the Logical sub‐block of the Physical Layer, which prepares packets for serial transmission and reception.
Several steps are needed to accomplish this and they are described in detail. This chapter covers the logic associated with the first two
spec versions Gen1 and Gen2 that use 8b/10b encoding. The logic for Gen3 does not use 8b/10b encoding and is described separately in the
chapter called “Physical Layer ‐ Logical (Gen3)” on page 407.

</td>
<td width="50%">

## **下一章**

下一章描述物理层的逻辑子块，它准备用于串行传输和接收的报文。完成此操作需要几个步骤，我们将在此详细描述。本章涵盖了与使用 8b/10b 编码的规范的前两个版本 Gen1 和 Gen2 相关的逻辑。Gen3 的逻辑不使用 8b/10b 编码，将在名为"物理层 - 逻辑
(Gen3)"的第 407 页的章节中单独描述。

</td>
</tr>
<tr>
<td width="50%">

## **Goal: Reliable TLP Transport** 

The function of the Data Link Layer (shown in Figure 10‐1 on page 318) is to ensure reliable delivery of TLPs. The spec requires a BER (Bit
Error Rate) of no worse than 10[‐12] , but errors will still happen often enough to cause trouble, and a single bit error will corrupt an
entire packet. This problem will only become more pronounced as Link rates continue to increase with new generations.

</td>
<td width="50%">

## **目标：可靠的 TLP 传输**

数据链路层的功能（如图 10-1（第 318 页）所示）是确保 TLP 的可靠交付。规范要求误码率 (BER) 不差于 10[‐12]，但错误仍会经常发生以引起麻烦，并且单个位错误将破坏整个报文。随着新一代链路速率的持续提高，这个问题只会变得更加严重。

</td>
</tr>
<tr>
<td width="50%">

## _Figure 10‐1: Data Link Layer_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## _图 10-1：数据链路层_

**==> 图片 [375 x 277] 已省略 <==**

**----- 图片文字开始 -----**<br>
Memory, I/O, Configuration R/W Requests or Message Requests or Completions<br>(Software layer sends / receives address/transaction
type/data/message index)<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header
Data Payload ECRC Header Data Payload ECRC<br>Transaction layer Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers
Buffers<br>per VC Management per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC ACK/NAK CRC ACK/NAK CRC
Sequence TLP LCRC<br>Data Link layer TLP Replay De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link
Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver
Training Differential Receiver<br>Port<br>Link<br>**----- 图片文字结束 -----**<br>

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0361_img2_tight.png" alt="Figure from page 361 (img 2)" width="700">

<a id="sec-8-2"></a>
## 8.2 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

To facilitate this goal, an error detection code called an LCRC (Link Cyclic Redundancy Code) is added to each TLP. The first step in error
checking is sim‐ ply to verify that this code still evaluates correctly at the receiver. If each packet is given a unique incremental
Sequence Number as well, then it will be easy to sort out which packet, out of several that have been sent, encountered an error. Using that
Sequence Number, we can also require that TLPs must be success‐ fully received in the same order they were sent. This simple rule makes it
easy to detect missing TLPs at the Receiver’s Data Link Layer.

The basic blocks in the Data Link Layer associated with the Ack/Nak protocol are shown in greater detail in Figure 10‐2 on page 319. Every
TLP sent across the Link is checked at the receiver by evaluating the LCRC (first) and Sequence Number (second) in the packet. The receiving
device notifies the transmitting device that a good TLP has been received by returning an Ack. Reception of an

**Cha ter 10: Ack/Nak Protocol p** 

Ack at the transmitter means that the receiver has received at least one TLP suc‐ cessfully. On the other hand, reception of a Nak by the
transmitter indicates that the receiver has received at least one TLP in error. In that case, the transmitter will re‐send the appropriate
TLP(s) in hopes of a better result this time. This is sensible, because things that would cause a transmission error would likely be
transient events and a replay will have a very good chance of solving the prob‐ lem.

_Figure 10‐2: Overview of the Ack/Nak Protocol_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


Since both the sending and receiving devices in the protocol have both a trans‐ mit and a receive side, this chapter will use the terms: 

- **Transmitter** to mean the device that sends TLPs 

- **Receiver** to mean the device that receives TLPs

</td>
<td width="50%">

为了实现此目标，一种称为 LCRC (Link Cyclic Redundancy Code) 的错误检测码被添加到每个 TLP
中。错误检查的第一步是简单地验证此代码在接收方是否仍然正确求值。如果每个报文还被赋予一个唯一的增量序列号，那么将很容易分清在已发送的几个报文中哪个报文遇到了错误。使用该序列号，我们还可以要求 TLP 必须以其发送的相同顺序成功接收。这个简单的规则使在接收方数据链路层检测缺失的
TLP 变得容易。

与 Ack/Nak 协议相关的数据链路层中的基本块在图 10-2（第 319 页）中更详细地示出。通过链路发送的每个 TLP 在接收方通过评估报文中的 LCRC（首先）和序列号（其次）进行检查。接收设备通过返回 Ack 通知发送设备已收到良好的 TLP。在发送方收到

**第 10 章：Ack/Nak 协议**

Ack 表示接收方已成功接收至少一个 TLP。另一方面，发送方接收到 Nak 表明接收方已至少收到一个错误的 TLP。在这种情况下，发送方将重新发送适当的 TLP，希望这次有更好的结果。这是合理的，因为导致传输错误的因素很可能是瞬时事件，重放 (replay)
将有很好的机会解决问题。

_图 10-2：Ack/Nak 协议概述_

**==> 图片 [374 x 237] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transmit Receiver<br>Device A Device B<br>From To<br>Transaction Layer Transaction Layer<br>Tx Rx<br>Data Link Layer Data Link Layer<br>TLP
DLLP DLLP TLP<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux De-mux<br>Error<br>Mux Mux Check<br>Tx Rx
Tx Rx<br>DLLP<br>ACK /<br>NAK<br>Link<br>TLP<br>Sequence TLP LCRC<br>**----- 图片文字结束 -----**<br>


由于协议中的发送和接收设备都同时具有发送和接收侧，因此本章将使用以下术语：

- **发送方 (Transmitter)** 指发送 TLP 的设备

- **接收方 (Receiver)** 指接收 TLP 的设备

</td>
</tr>
<tr>
<td width="50%">

## **Elements of the Ack/Nak Protocol** 

The major Ack/Nak protocol elements of the Data Link Layer are shown in Fig‐ ure 10‐3 on page 320. There’s too much to consider all at once,
though, so let’s begin by focusing on just the transmitter elements, which are shown in a larger view in Figure 10‐4 on page 322.

_Figure 10‐3: Elements of the Ack/Nak Protocol_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **Ack/Nak 协议的要素**

数据链路层的主要 Ack/Nak 协议元素如图 10-3（第 320 页）所示。要一次考虑的事情太多了，所以让我们从关注发送方元素开始，它们在图 10-4（第 322 页）中的较大视图中显示。

_图 10-3：Ack/Nak 协议的要素_

**==> 图片 [375 x 242] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (TX) Block TLPs; Report Transaction Layer (RX)<br>DLL protocol error<br>Yes Increment NRS Good TLPs<br>No<br>TLPs (NTS-AS)
≥ 2048?<br>(Continue) NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Assign<br>SequenceNumber (IncrementNEXT_TRANSMIT_SEQ (NTS)) Seq Num < NRS
(Duplicate TLP)(Schedule Ack) Seq Num>, <, =NRS?<br>REPLAY_TIMER<br>LCRC Increment on Replay) Seq Num > NRS (Lost
TLP)<br>REPLAY_NUM<br>Generator (Send Nak) Yes<br>Purge Older TLPs (Reset Both)<br>(Send Nak) No Pass<br>Retry (Replay)Buffer (Replay)Yes
Nak?Nak (Update)AckD_SEQ (AS)No Nak Flag Clear?Set & Send Nak LCRC?<br>Yes AckNak<br>(TLP copy) SeqNum = AS? NAK_SCHEDULED Good
TLP?<br>Clear Nak Flag<br>(TLP copy) Yes Ack Nak<br>(Discard) No CRC?Pass GeneratorAck/Nak AckNak LatencyTimer<br>Ack/Nak<br>DLLP
Link<br>TLP TLP<br>Block TLP during Replay<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **Transmitter Elements** 

As TLPs arrive from the Transaction Layer, several things are done to prepare them for robust error detection at the receiver. As shown in
the diagram TLPs are first assigned the next sequential Sequence Number, obtained from the 12‐ bit NEXT_TRANSMIT_SEQ counter.

**Cha ter 10: Ack/Nak Protocol p**

</td>
<td width="50%">

## **发送方元素**

当 TLP 从事务层到达时，会执行几项操作以准备它们在接收方进行可靠的错误检测。如图所示，首先为 TLP 分配从 12 位 NEXT_TRANSMIT_SEQ 计数器获得的下一个序列号。

**第 10 章：Ack/Nak 协议**

</td>
</tr>
<tr>
<td width="50%">

## **NEXT_TRANSMIT_SEQ Counter** 

This counter generates the Sequence Number that will be assigned to the next incoming TLP. It’s a 12‐bit counter that is initialized to 0 at
reset or when the Link Layer reports DL_Down (Link Layer is inactive). Since it increments con‐ tinuously with each TLP and only counts
forward, the counter eventually reaches its max value of 4095 and rolls over to 0 as it continues to count.

This Sequence Number assigned to the TLP will be used in the Ack or Nak sent by the receiver to reference this TLP in the Replay Buffer. One
might think that such a large counter means that a large number of unacknowledged TLPs could be in flight, but in practice this is very
unlikely. The main reason is that the receiver has a requirement to send an Ack back for successfully received TLPs within a certain amount
of time. That amount of time is discussed in detail in “AckNak_LATENCY_TIMER” on page 328, but is typically only long enough to transmit a
few max sized packets.

</td>
<td width="50%">

## **NEXT_TRANSMIT_SEQ 计数器**

此计数器生成将分配给下一个传入 TLP 的序列号。它是一个 12 位的计数器，在复位时或当链路层报告 DL_Down（链路层处于非活动状态）时初始化为 0。由于它随每个 TLP 连续递增并且只向前计数，因此计数器最终会达到其最大值 4095，并在继续计数时回绕到 0。

分配给 TLP 的此序列号将在接收方发送的 Ack 或 Nak 中用于引用重放缓冲区 (Replay Buffer) 中的此 TLP。有人可能认为如此大的计数器意味着可能有大量的未确认 TLP 在传输中，但实际上这是极不可能的。主要原因是接收方有要求在特定时间内为成功接收的
TLP 发送回一个 Ack。该时间在第 328 页的"AckNak_LATENCY_TIMER"中详细讨论，但通常只够传输几个最大大小的报文。

</td>
</tr>
<tr>
<td width="50%">

## **LCRC Generator** 

This block generates a 32‐bit CRC (Cyclic Redundancy Check) code based on the header and data to be sent and adds it to the end of the
outgoing packet to facilitate error detection. The name is derived from the fact that this _check code_ (calculated from the packet to be
sent) is _redundant_ (adds no information), and is derived from _cyclic codes_ . Although a CRC doesn’t supply enough information for the
Receiver to do automatic error correction the way ECC (Error Correcting Code) methods can, it does provide robust error detection. CRCs are
commonly used in serial transports because they’re easy to implement in hardware, and because they’re good at detecting burst errors: a
string of incorrect bits. Since this is more likely to happen in a serial design than a parallel model, it helps explain why a CRC is a good
choice for error detection in serial transports. The CRC code is calculated using all fields of the TLP, including the Sequence Num‐ ber.
The receiver will make the same calculation and compare its result to the LCRC field in the TLP. If they don’t match, an error is detected
in the Receiver’s Link Layer.

</td>
<td width="50%">

## **LCRC 生成器**

此块基于要发送的头部和数据生成 32 位 CRC (Cyclic Redundancy Check) 码，并将其添加到传出报文的末尾以促进错误检测。名称来源于以下事实：此 _校验码_（从要发送的报文计算）是 _冗余_（不添加信息）的，并且源自 _循环码_。虽然 CRC
不为接收方提供足够的信息来执行 ECC (Error Correcting Code) 方法那样的自动纠错，但它确实提供了可靠的错误检测。CRC
通常用于串行传输，因为它们易于在硬件中实现，并且擅长检测突发错误：一串不正确的位。由于这在串行设计中比并行模型更可能发生，因此它有助于解释为什么 CRC 是串行传输中错误检测的良好选择。CRC 码是使用 TLP 的所有字段（包括序列号）计算的。接收方将进行相同的计算并将其结果与
TLP 中的 LCRC 字段进行比较。如果它们不匹配，则在接收方的链路层中检测到错误。

</td>
</tr>
<tr>
<td width="50%">

## **Replay Buffer** 

The replay buffer, or retry buffer, stores TLPs, including the Sequence Number and LCRC, in the order of their transmission. When the
transmitter receives an Ack indicating that TLPs have reached the receiver successfully, it purges from the Replay Buffer those TLPs whose
Sequence Number is equal to or earlier than the number in the Ack. In this way, the design allows one Ack to represent several successful
TLPs, reducing the number of Acks that must be sent. Since the packets must always be seen in order, then if an Ack is received with a

Sequence Number of 7, then not only was TLP 7 received successfully, but all the packets before it must also have been received
successfully, so there is no reason to keep a copy of them in the replay buffer.

If a Nak is received, the Sequence Number in the Nak still indicates the last _good_ packet received. So even receiving a Nak can cause the
transmitter to purge TLPs from the replay buffer. However, because it is a Nak, it means that some‐ thing was not received successfully at
the receiver, so after purging all the acknowledged TLPs, the transmitter must replay everything still in the replay buffer in order. For
example, if a Nak is received with a Sequence Number of 9, then packet 9 and all prior packets are purged from the replay buffer, because
the receiver acknowledged that they have been successfully received. However, because it is a Nak, the transmitter must then replay all the
remaining TLPs in the replay buffer in order, starting with packet 10.

_Figure 10‐4: Transmitter Elements Associated with the Ack/Nak Protocol_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


**Cha ter 10: Ack/Nak Protocol p**

</td>
<td width="50%">

## **重放缓冲区**

重放缓冲区 (replay buffer) 或重试缓冲区 (retry buffer) 按其传输顺序存储 TLP，包括序列号和 LCRC。当发送方接收到 Ack 指示 TLP 已成功到达接收方时，它会从重放缓冲区中清除那些序列号等于或早于 Ack 中序列号的
TLP。通过这种方式，设计允许一个 Ack 代表多个成功的 TLP，从而减少了必须发送的 Ack 数量。由于报文必须始终按顺序查看，因此如果收到一个

序列号为 7 的 Ack，则不仅 TLP 7 被成功接收，而且其之前的所有报文也必须已被成功接收，因此没有理由在重放缓冲区中保留它们的副本。

如果收到 Nak，则 Nak 中的序列号仍然指示最后 _良好的_ 接收报文。因此，即使收到 Nak 也会导致发送方从重放缓冲区中清除 TLP。但是，因为它是 Nak，这意味着某些内容未在接收方成功接收，因此在清除所有已确认的 TLP
后，发送方必须按顺序重放重放缓冲区中所有剩余的内容。例如，如果收到序列号为 9 的 Nak，则报文 9 和所有先前的报文都从重放缓冲区中清除，因为接收方已确认它们已成功接收。但是，因为它是 Nak，发送方必须随后按顺序重放重放缓冲区中所有剩余的 TLP，从报文 10 开始。

_图 10-4：与 Ack/Nak 协议相关联的发送方元素_

**==> 图片 [217 x 275] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (TX) Block TLPs; Report<br>DLL protocol error<br>Yes<br>No<br>TLPs (NTS-AS) ≥
2048?<br>(Continue)<br>Assign<br>Sequence<br>Number NEXT_TRANSMIT_SEQ (NTS)<br>(Increment)<br>REPLAY_TIMER<br>LCRC Increment on
Replay)<br>REPLAY_NUM<br>Generator<br>Purge Older TLPs<br>(Reset Both)<br>Nak AckD_SEQ (AS)<br>Retry (Replay)Buffer Yes Nak? (Update)
No<br>(Replay)<br>Yes AckNak<br>SeqNum = AS?<br>(TLP copy)<br>(TLP copy) Yes<br>No Pass<br>(Discard) CRC?<br>Link<br>Block TLP during
Replay<br>**----- 图片文字结束 -----**<br>


**第 10 章：Ack/Nak 协议**

</td>
</tr>
<tr>
<td width="50%">

## **REPLAY_TIMER Count** 

This timer is effectively a watchdog timer. It makes sure that the transmitter is receiving Ack/Nak packets for TLPs that have been
transmitted. If this timer expires, it means that the transmitter has sent one or more TLPs that it has not received an acknowledgement for
in the expected time frame. The fix is to retransmit everything in the replay buffer and restart the REPLAY_TIMER.

This timer is running anytime a TLP has been transmitted but not yet acknowledged. If the REPLAY_TIMER is not currently running, it is
started when the last Symbol of any TLP is transmitted. If the timer is already running, then sending additional TLPs does not reset the
timer value. When an Ack or Nak is received that acknowledges TLPs in the replay buffer, the timer resets back to 0, and if there are still
TLPs in the replay buffer (TLPs that have been transmitted, but not yet acknowledged), it immediately starts counting again. However, if an
Ack is received that acknowledges the last TLP in the replay buffer, meaning the replay buffer is now empty, the REPLAY_TIMER resets to 0
but does not count. It will not begin counting again until the last Symbol of the next TLP is transmitted.

</td>
<td width="50%">

## **REPLAY_TIMER 计数**

此计时器实际上是一个看门狗计时器。它确保发送方正在接收已发送 TLP 的 Ack/Nak 报文。如果此计时器到期，则意味着发送方已发送一个或多个 TLP，但未在预期的时间范围内收到确认。解决方法是重新发送重放缓冲区中的所有内容并重新启动 REPLAY_TIMER。

此计时器在任何 TLP 已传输但尚未确认时都处于运行状态。如果 REPLAY_TIMER 当前未运行，则在发送任何 TLP 的最后一个符号时启动。如果计时器已经在运行，则发送其他 TLP 不会重置计时器值。当收到确认重放缓冲区中 TLP 的 Ack 或 Nak 时，计时器重置回
0，如果重放缓冲区中仍有 TLP（已传输但尚未确认的 TLP），则它会立即开始重新计数。但是，如果收到的 Ack 确认了重放缓冲区中的最后一个 TLP，意味着重放缓冲区现在为空，则 REPLAY_TIMER 重置为 0 但不计数。它将不会再次开始计数，直到下一个 TLP
的最后一个符号被传输。

</td>
</tr>
<tr>
<td width="50%">

## **REPLAY_NUM Count** 

This 2‐bit counter tracks the number of replay attempts after reception of a Nak or a REPLAY_TIMER time‐out. When the REPLAY_NUM count rolls
over from 11b to 00b (indicating 4 failed attempts to deliver the same set of TLPs), the Data Link Layer automatically forces the Physical
Layer to retrain the Link (LTSSM goes to the Recovery state). When re‐training is finished, it will attempt to send the failed TLPs again.
The REPLAY_NUM counter is initialized to 00b at reset, or when the Link Layer is inactive. It is also reset whenever an Ack DLLP is received
with a Sequence Number that is more recent than the last one seen, meaning forward progress is being made.

</td>
<td width="50%">

## **REPLAY_NUM 计数**

此 2 位计数器跟踪在接收到 Nak 或 REPLAY_TIMER 超时之后的重放尝试次数。当 REPLAY_NUM 计数从 11b 回绕到 00b（表示对同一组 TLP 进行了 4 次失败的传递尝试）时，数据链路层自动强制物理层重新训练链路（LTSSM 进入 Recovery
状态）。重新训练完成后，它将尝试再次发送失败的 TLP。REPLAY_NUM 计数器在复位时或当链路层处于非活动状态时初始化为 00b。每当收到序列号比上次看到的更新的 Ack DLLP 时，它也会被重置，这意味着正在取得进展。

</td>
</tr>
<tr>
<td width="50%">

## **ACKD_SEQ Register** 

This 12‐bit register stores the Sequence Number of the most recently received Ack or Nak. It is initialized to all 1s at reset, or when the
Data Link Layer is inac‐ tive. This register is updated with the AckNak_Seq_Num [11:0] field of a received Ack or Nak. The ACKD_SEQ count is
compared with the Sequence Number in the last received Ack or Nak to check for forward progress. If the lat‐ est Ack/Nak had a Sequence
Number later than the ACKD_SEQ register, then we’re making forward progress.

</td>
<td width="50%">

## **ACKD_SEQ 寄存器**

此 12 位寄存器存储最近接收到的 Ack 或 Nak 的序列号。它在复位时或当数据链路层处于非活动状态时初始化为全 1。此寄存器使用接收到的 Ack 或 Nak 的 AckNak_Seq_Num [11:0] 字段更新。将 ACKD_SEQ 计数与最后接收到的 Ack 或
Nak 中的序列号进行比较，以检查是否取得进展。如果最新的 Ack/Nak 的序列号晚于 ACKD_SEQ 寄存器，那么我们正在取得进展。

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

As an aside, we use the term “later Sequence Number” to account for the fact that, like most counters in PCIe, the Sequence Number counters
only count for‐ ward, meaning that they’ll eventually roll over back to zero. Technically, a later number would mean a numerically higher
value, but we have to remember that when the counter reaches 4095 (it’s a 12‐bit counter), the next higher number will be zero. This
wrap‐around effect will be easier to see in the examples later, as in “Ack/Nak Examples” on page 331.

</td>
<td width="50%">

## **PCI Exress Technology**

顺便说一句，我们使用术语"较晚的序列号"来解释以下事实：与 PCIe 中的大多数计数器一样，序列号计数器仅向前计数，这意味着它们最终会回绕回零。从技术上讲，较晚的数字将意味着数值更高的值，但我们必须记住，当计数器达到 4095（它是 12
位计数器）时，下一个更高的数字将为零。这种回绕效果将在后面的示例中更容易看到，如第 331 页的"Ack/Nak 示例"中所示。

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0361_img1.png" alt="Figure from page 361 (img 1)" width="700">

<a id="sec-8-3"></a>
## 8.3 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

As shown in Figure 10‐4 on page 322, when an Ack or Nak makes forward progress it causes TLPs with Sequence Numbers equal to or older than
the value in the DLLP to be purged out of the Replay Buffer. It also resets both the REPLAY_TIMER and the REPLAY_NUM count. If no forward
progress is made, no TLPs can be purged so we only check to see if it’s a Nak that would necessi‐ tate a replay.

This is a good place to mention a potential problem with the counters: the num‐ ber of TLPs sent might theoretically become much larger than
the number that have been acknowledged by the receiver. As mentioned earlier, this is very unlikely; it’s only mentioned here for
completeness. The problem is basically the same as it for the Flow Control counters (see “Stage 3 — Counters Roll Over” on page 234) and has
the same solution: the NEXT_TRANSMIT_SEQ and ACKD_SEQ counters are never allowed to be separated by more than half their total count value.
If a large number of TLPs are sent without acknowledgement so that the NEXT_TRANSMIT_SEQ count value is later than ACKD_SEQ count by 2048,
no more TLPs will be accepted from the Transaction Layer until this is resolved by receiving more Acks. If the difference between the
Sequence Num‐ ber sent and the acknowledged count ever did exceed half the maximum count value, a Data Link Layer protocol error would be
reported. (For more on error reporting, see “Data Link Layer Errors” on page 655.)

</td>
<td width="50%">

如图 10-4（第 322 页）所示，当 Ack 或 Nak 取得进展时，它会导致序列号等于或早于 DLLP 中值的 TLP 从重放缓冲区中清除。它还会重置 REPLAY_TIMER 和 REPLAY_NUM 计数。如果没有取得进展，则无法清除任何
TLP，因此我们只检查它是否是会引起重放的 Nak。

这是提及计数器潜在问题的好地方：发送的 TLP 数量在理论上可能远大于接收方已确认的数量。如前所述，这是极不可能的；此处提及只是为了完整起见。问题基本上与流控计数器的问题相同（参见第 234 页的"阶段 3 —
计数器回绕"）并具有相同的解决方案：NEXT_TRANSMIT_SEQ 和 ACKD_SEQ 计数器永远不允许被超过其总计数值一半的值分隔。如果发送了大量 TLP 而没有确认，使得 NEXT_TRANSMIT_SEQ 计数值比 ACKD_SEQ 计数晚 2048，则在通过接收更多
Ack 解决此问题之前，将不再从事务层接受更多 TLP。如果发送的序列号与已确认计数之间的差异确实超过最大计数值的一半，则将报告数据链路层协议错误。（有关错误报告的更多信息，请参见第 655 页的"数据链路层错误"。）

</td>
</tr>
<tr>
<td width="50%">

## **DLLP CRC Check** 

This block checks for errors in the 16‐bit CRC of DLLPs. If an error is detected, the DLLP is discarded and a Correctable Error may be
reported, if enabled. No further action is taken because there is no mechanism to replay or correct failed DLLPs. Instead, we simply wait
for the next successful Ack/Nak, which will get the counters back up‐to‐date and allow normal operation to continue.

</td>
<td width="50%">

## **DLLP CRC 检查**

此块检查 DLLP 的 16 位 CRC 中的错误。如果检测到错误，则丢弃该 DLLP，并可能报告一个可纠正错误（如果已启用）。不会采取进一步的操作，因为没有重放或更正失败 DLLP 的机制。相反，我们只是等待下一个成功的
Ack/Nak，它将使计数器恢复最新状态并允许正常操作继续。

</td>
</tr>
<tr>
<td width="50%">

## **Receiver Elements** 

Incoming TLPs are first checked for LCRC errors and then for Sequence Num‐ bers. If there are no errors, the TLP is forwarded to the
receiver’s Transaction

**Cha ter 10: Ack/Nak Protocol p** 

Layer. If there are errors, the TLP is discarded and a Nak will be scheduled unless there was already a Nak outstanding. 

Figure 10‐5 on page 325 illustrates the receiver Data Link Layer elements associ‐ ated with processing of inbound TLPs and outbound Ack/Nak
DLLPs.

_Figure 10‐5: Receiver Elements Associated with the Ack/Nak Protocol_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **接收方元素**

传入的 TLP 首先检查 LCRC 错误，然后检查序列号。如果没有错误，则 TLP 将转发到接收方的事务层。如果有错误，则 TLP 被丢弃，并且将调度一个 Nak，除非已经有一个 Nak 未完成。

**第 10 章：Ack/Nak 协议**

图 10-5（第 325 页）说明了与入站 TLP 和出站 Ack/Nak DLLP 处理相关联的接收方数据链路层元素。

_图 10-5：与 Ack/Nak 协议相关联的接收方元素_

**==> 图片 [223 x 281] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule
Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send
Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) =
AckNak_Seq_Num[11:0]<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **LCRC Error Check** 

This block checks for transmission errors in the received TLP by verifying the 32‐bit LCRC. This block calculates an LCRC value based on the
received bits of the TLP and then compares the calculated LCRC to the received LCRC. If they match, then all the bits of the packet were
received exactly as they were trans‐ mitted. If it doesn’t match, then there was a bit error in the TLP so it gets dropped and a Nak will be
sent to get a replay of that packet and any TLPs sent after the bad packet.

</td>
<td width="50%">

## **LCRC 错误检查**

此块通过验证 32 位 LCRC 来检查接收到的 TLP 中的传输错误。此块根据接收到的 TLP 位计算 LCRC 值，然后将计算出的 LCRC 与接收到的 LCRC 进行比较。如果它们匹配，则报文的所有位都按发送时完全接收。如果不匹配，则 TLP
中存在位错误，因此它被丢弃，并将发送 Nak 以重放该报文和错误报文之后发送的所有 TLP。

</td>
</tr>
<tr>
<td width="50%">

## **NEXT_RCV_SEQ Counter** 

The 12‐bit NEXT_RCV_SEQ (Next Receive Sequence number) counter keeps track of the expected Sequence Number and is used to verify sequential
packet reception. It’s initialized to 0 at reset or when the Data Link Layer is inactive, and is incremented once for each good TLP
forwarded to the Transaction Layer. TLPs that have errors or were nullified are not sent to the Transaction Layer and therefore don’t
increment this counter.

</td>
<td width="50%">

## **NEXT_RCV_SEQ 计数器**

12 位 NEXT_RCV_SEQ（下一个接收序列号）计数器跟踪预期的序列号，并用于验证顺序报文接收。它在复位时或当数据链路层处于非活动状态时初始化为 0，并且对于转发到事务层的每个良好 TLP 递增一次。有错误或被作废的 TLP 不会发送到事务层，因此不会增加此计数器。

</td>
</tr>
<tr>
<td width="50%">

## **Sequence Number Check** 

If the LCRC check was OK, the TLP’s Sequence Number is checked against the expected count (the NRS number). As can be seen in Figure 10‐5 on
page 325, there are three possible outcomes of this check:

1. The TLP Sequence Number equals the NRS count (the number we’re expecting). In this case, everything is good: the TLP is accepted and for‐
warded to the Transaction Layer and the NRS count is incremented. The Receiver schedules an Ack, but it doesn’t have to be sent until the
AckNak_LATENCY_TIMER expires. In the meantime, other good TLPs may be received, incrementing the NEXT_RCV_SEQ counter. Then, once the timer
expires, a single Ack is sent with the Sequence Number of the last good TLP received (NRS ‐ 1). That allows one Ack to represent several
suc‐ cessful TLPs and reduces overhead, since a dedicated Ack is not required for every TLP.

2. If the TLP’s Sequence Number is earlier than the NRS count (smaller than expected), this TLP has been seen before and is a duplicate. As
long as the expected Sequence Number and received Sequence Number don’t get sepa‐ rated by more than half the total count value (2048), this
is not an error, but is seen as a duplicate, meaning the TLP has already been accepted earlier. In this case, the TLP is silently dropped
(no Nak, no error reporting) and an Ack is sent with the Sequence Number of the last good TLP it received (NRS ‐ 1). Why would this
situation happen? The transmitter may not have received a transmitted Ack, so his REPLAY_TIMER expired and he retrans‐ mitted everything in
his Replay Buffer. By sending the transmitter an Ack with the Sequence Number of the last good packet we received, we’re noti‐ fying him of
the furthest progress we’ve made.

3. If the TLP’s Sequence Number is a later Sequence Number than NEXT_RCV_SEQ count (larger than expected), then the Link Layer has missed a
TLP. For example, if we’re expecting Sequence Number 30 and the incoming TLP has Sequence Number 31 we know there’s a problem. The numbers
must be sequential and, since they aren’t, one must have failed

**Cha ter 10: Ack/Nak Protocol p** 

and been dropped, as might happen at the Physical Layer. This out‐of‐order TLP is discarded, whether or not it had any other errors because
we must accept TLPs in order, and a Nak will be sent if there wasn’t one already out‐ standing.

The concept of the expected sequence number (NRS) incrementing as new TLPs are successfully received and seeing how that affects the sliding
windows for the invalid range of sequence numbers and the duplicate range of sequence numbers can be seen in Figure 10‐6.

_Figure 10‐6: Examples of Sequence Number Ranges_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **序列号检查**

如果 LCRC 检查通过，则将 TLP 的序列号与预期计数（NRS 编号）进行检查。如图 10-5（第 325 页）所示，此检查有三种可能的结果：

1. TLP 序列号等于 NRS 计数（我们期望的编号）。在这种情况下，一切正常：TLP 被接受并转发到事务层，并且 NRS 计数递增。接收方调度一个 Ack，但不必在 AckNak_LATENCY_TIMER 到期之前发送它。在此期间，可能会收到其他良好的 TLP，从而增加
NEXT_RCV_SEQ 计数器。然后，一旦计时器到期，将发送一个 Ack，其中包含最后接收到的良好 TLP 的序列号（NRS - 1）。这允许一个 Ack 代表多个成功的 TLP 并减少开销，因为不需要为每个 TLP 都使用专用的 Ack。

2. 如果 TLP 的序列号早于 NRS 计数（小于预期），则该 TLP 之前已见过，是重复的。只要预期序列号和接收到的序列号不被超过总计数值一半（2048）的值分隔，这不算错误，但被视为重复，意味着该 TLP 之前已被接受。在这种情况下，TLP 被静默丢弃（无
Nak，无错误报告），并发送一个 Ack，其中包含它接收到的最后良好 TLP 的序列号（NRS - 1）。为什么会出现这种情况？发送方可能未收到已发送的 Ack，因此其 REPLAY_TIMER
已过期，并重新发送了其重放缓冲区中的所有内容。通过向发送方发送一个带有我们接收到的最后良好报文序列号的 Ack，我们正在通知它我们已取得的最远进展。

3. 如果 TLP 的序列号是比 NEXT_RCV_SEQ 计数更晚的序列号（大于预期），则链路层已错过一个 TLP。例如，如果我们在等待序列号 30 并且传入的 TLP 具有序列号 31，我们就知道存在问题。编号必须按顺序排列，既然不是，则一定有一个失败了

**第 10 章：Ack/Nak 协议**

并已被丢弃，例如可能在物理层发生。这种乱序 TLP 将被丢弃，无论它是否有任何其他错误，因为我们必须按顺序接受 TLP，并且如果尚未有未完成的 Nak，则将发送一个 Nak。

预期序列号 (NRS) 随着新 TLP 的成功接收而递增的概念，以及它如何影响无效序列号范围和重复序列号范围的滑动窗口，可以在图 10-6 中看到。

_图 10-6：序列号范围示例_

**==> 图片 [270 x 286] 已省略 <==**

**----- 图片文字开始 -----**<br>
0 30 2078 4095<br>Dupli- Invalid<br>Duplicate<br>cate (out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 31 2079
4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 32 2080
4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **NAK_SCHEDULED Flag** 

This flag is set whenever the receiver schedules a Nak, and is cleared when the receiver successfully receives the TLP with the expected
Sequence Number (NRS). The spec is clear that the receiver must not schedule additional Nak DLLPs while the NAK_SCHEDULED flag remains set.
The author’s opinion is

that this is intended to prevent the possibility of an endless loop; a case in which the transmitter begins to replay some packets but the
receiver sends another Nak before the replays finish and causes it to restart sending them again. What‐ ever the motivation, once a Nak has
been sent there will be no more Naks forth‐ coming until the problem is resolved by successful receipt of the replayed TLP with the correct
Sequence Number.

</td>
<td width="50%">

## **NAK_SCHEDULED 标志**

每当接收方调度一个 Nak 时，此标志被置位，并在接收方成功接收到具有预期序列号 (NRS) 的 TLP 时被清除。规范明确规定，接收方在 NAK_SCHEDULED 标志保持置位时不得调度其他 Nak DLLP。作者认为

这是为了防止出现无限循环的可能性；在这种情况下，发送方开始重放某些报文，但接收方在重放完成之前发送另一个 Nak，并导致它重新开始发送它们。无论动机如何，一旦发送了 Nak，在问题通过成功接收具有正确序列号的重放 TLP 得到解决之前，将不会有更多 Nak 出现。

</td>
</tr>
<tr>
<td width="50%">

## **AckNak_LATENCY_TIMER** 

This timer is running anytime a receiver successfully receives a TLP that it has not yet acknowledged. The receiver is required to send an
Ack once the timer expires. The length of time the AckNak Latency Timer runs is dictated by the spec (see “AckNak_LATENCY_TIMER” on page
328) and determines how long a receiver can coalesce Acks. Once the AckNak Latency Timer expires, an Ack with sequence number NRS‐1 is
generated and sent which indicates the last good packet it received. This timer is reset whenever an Ack or Nak are sent and it only
restarts once a new good TLP is received.

</td>
<td width="50%">

## **AckNak_LATENCY_TIMER**

此计时器在接收方成功接收尚未确认的 TLP 时一直处于运行状态。接收方需要在计时器到期时发送一个 Ack。AckNak 延迟计时器运行的时间长度由规范规定（参见第 328 页的"AckNak_LATENCY_TIMER"），并确定接收方可以合并 Ack 的时间。一旦 AckNak
延迟计时器到期，将生成并发送一个序列号为 NRS‐1 的 Ack，它指示最后接收到的良好报文。每当发送 Ack 或 Nak 时，此计时器都会重置，并且只有在接收到新的良好 TLP 时才会重新启动。

</td>
</tr>
<tr>
<td width="50%">

## **Ack/Nak Generator** 

Ack or Nak DLLPs are scheduled by the error checking blocks and contain a 12‐ bit AckNak_Seq_Num field as illustrated in Figure 10‐7 on page
328. It calcu‐ lates this number by subtracting one from the NRS count, which results in reporting the last good Sequence Number received.
That’s because a good TLP received increments NRS before scheduling the Ack, while a failed TLP just schedules a Nak without incrementing
NRS. This method makes it easier to handle failed packets because the error in the TLP might have been in the Sequence Number, so that
number can’t be used in the Nak. Instead, it uses the number of the last good TLP; what we’re expecting minus one. The only case where this
value doesn’t represent the last good TLP is for the first TLP after a reset. If that first TLP, using Sequence Number 0, fails, the
resulting Nak will have an AckNak_Seq_Num value of zero minus one which results in all 1’s.

_Figure 10‐7: Ack Or Nak DLLP Format_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


**Cha ter 10: Ack/Nak Protocol p** 

_Table 10‐1: Ack or Nak DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:0]|Indicates the type: • 0000 0000b = Ac...|
|AckNak_Seq_Num|Byte 2, [3:0] Byte 3, [7:0]|This value will always be NEXT_RCV_SE...|
|16‐bit CRC|Byte 4, [7:0] Byte 5, [7:0]|16‐bit CRC used to protect the conten...|

</td>
<td width="50%">

## **Ack/Nak 生成器**

Ack 或 Nak DLLP 由错误检查块调度，并包含一个 12 位的 AckNak_Seq_Num 字段，如图 10-7（第 328 页）所示。它通过从 NRS 计数中减去 1 来计算此数字，从而报告最后接收到的良好序列号。这是因为接收到的良好 TLP 会在调度 Ack
之前递增 NRS，而失败的 TLP 只会调度 Nak 而不递增 NRS。这种方法使处理失败报文更容易，因为 TLP 中的错误可能在序列号中，因此该号码不能在 Nak 中使用。相反，它使用最后良好 TLP 的号码；我们预期的减一。唯一不表示最后良好 TLP 的情况是复位后的第一个
TLP。如果使用序列号 0 的第一个 TLP 失败，则生成的 Nak 的 AckNak_Seq_Num 值将为零减一，结果为全 1。

_图 10-7：Ack 或 Nak DLLP 格式_

**==> 图片 [386 x 97] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved
AckNak_Seq_Num<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


**第 10 章：Ack/Nak 协议**

_表 10-1：Ack 或 Nak DLLP 字段_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP 类型|Byte 0, [7:0]|指示类型：<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|此值将始终为 NEXT_RCV_SEQ 计数 - 1。|
|16 位 CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|用于保护此 DLLP 内容的 16 位 CRC。|

</td>
</tr>
<tr>
<td width="50%">

## **Ack/Nak Protocol Details** 

This section describes the detailed transmitter and receiver behavior in process‐ ing TLPs and Ack/Nak DLLPs. Several examples are used to
demonstrate vari‐ ous cases that may occur.

</td>
<td width="50%">

## **Ack/Nak 协议详细信息**

本节描述了在处理 TLP 和 Ack/Nak DLLP 时发送方和接收方的详细行为。使用了一些示例来演示可能发生的各种情况。

</td>
</tr>
<tr>
<td width="50%">

## **Transmitter Protocol Details**

</td>
<td width="50%">

## **发送方协议详细信息**

</td>
</tr>
<tr>
<td width="50%">

## **Sequence Number** 

Referring back to Figure 10‐4 on page 322, when TLPs are delivered by the Transaction Layer to the Link Layer, one of the first steps is to
append a 12‐bit Sequence Number. Keep in mind that the next incremental Sequence Number may actually be smaller, as will happen when the
counter rolls over back to zero after it reaches a maximum value of 4095. Consequently, a value of zero can actually be ‘larger’ than a
value of 4095, for example. It may help to think of the Sequence Number comparison as evaluating a ‘window’ of numbers that con‐ sistently
moves upward and rolls over. To clarify this concept, such a count roll‐ over is used in several of the upcoming examples.

</td>
<td width="50%">

## **序列号**

参考图 10-4（第 322 页），当 TLP 由事务层传送到链路层时，第一步是附加一个 12 位的序列号。请记住，下一个增量序列号实际上可能更小，例如当计数器在达到最大值 4095 后回绕回零时就会发生这种情况。因此，例如，零的值实际上可以"大于"4095
的值。将序列号比较视为评估一个持续向上移动并回绕的"窗口"可能会有所帮助。为了阐明此概念，在接下来的几个示例中使用了这样的计数回绕。

</td>
</tr>
<tr>
<td width="50%">

## **32-Bit LCRC** 

The transmitter also generates and appends a 32‐bit LCRC (Link CRC) based on the TLP contents (Sequence Number, Header, Data Payload and
ECRC).

## **Replay (Retry) Buffer**

</td>
<td width="50%">

## **32 位 LCRC**

发送方还根据 TLP 内容（序列号、头部、数据有效负载和 ECRC）生成并附加一个 32 位的 LCRC (Link CRC)。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **重放（重试）缓冲区**

**概述。** 在设备传输 TLP 之前，它将 TLP 的副本存储在重放缓冲区中。（_请注意，规范使用术语重试缓冲区 (Retry Buffer)，但在本书中选择了"重放"而不是"重试"，以更清楚地区分此机制与旧的 PCI 重试机制_）。每个缓冲区条目存储一个完整的
TLP，包括其所有字段，包括序列号（12 位宽，占两个字节）、头部（最多 16 字节）、可选的数据有效负载（最多 4KB）、可选的 ECRC（4 字节）和 LCRC 字段（4 字节）。

需要注意的是，规范以这种方式描述了重放缓冲区，但它并不是必须以这种方式实现的规范要求。只要您的设备能够在需要时按规范定义重放一系列 TLP，那么如何在设备内完成这一点的设计就完全取决于设计人员。拥有如上所述行为的重放缓冲区是实现此目的的一种方法。

**重放缓冲区大小调整。** 规范编写者选择不指定重放缓冲区的大小，将其作为设备设计人员的优化。它应该足够大以存储尚未被 Ack 确认的 TLP，以便在正常操作条件下它不会变满并停止从事务层传入的新 TLP，但也要足够小以降低成本。要确定最佳缓冲区大小，设计人员将考虑：

- 来自接收方的 Ack DLLP 延迟。

- 物理链路引起的延迟。

- 接收方 L0s 退出到 L0 的延迟。换句话说，缓冲区应足够大以容纳 TLP 而不会在链路从 L0s 状态返回到 L0 时停顿。

当发送方收到 Ack 时，它会从重放缓冲区中清除序列号等于或早于 Ack 中序列号的 TLP（_通常此术语为"小于"，但计数器回绕行为有时会使该评估不正确，因此选择了"早于"一词_）。类似地，当发送方收到 Nak 时，它仍然会从重放缓冲区中清除序列号等于或早于 Nak
中到达的序列号的 TLP，但随后它还会重放（重新发送）较晚序列号的 TLP（重放缓冲区中剩余的 TLP）。

**第 10 章：Ack/Nak 协议**

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **发送方对 Ack DLLP 的响应**

接收方返回的单个 Ack 可以确认多个 TLP；不必每个发送的 TLP 都收到一个专用的 Ack。接收方可以获得多个良好的 TLP，并发送一个带有最后接收到的良好 TLP 序列号的 Ack。发送方对取得进展的 Ack（具有比上次看到的更晚的序列号）的响应是将 AckD_SEQ
寄存器加载为新 Ack 的序列号。它还会重置 REPLAY_NUM 计数器和 REPLAY_TIMER，并清除重放缓冲区中由该 Ack 确认的所有 TLP。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **Ack/Nak 示例**

**示例 1。** 在以下讨论中请考虑图 10-8（第 332 页）。

1. 设备 A 发送序列号为 3、4、5、6、7 的 TLP。

2. 设备 B 成功接收 TLP 3 并将其 NEXT_RCV_SEQ 计数器从 3 增加到 4。由于设备 B 先前已确认所有成功接收的 TLP，因此 AckNak_LATENCY_TIMER 未运行。在接收到 TLP 3 后，设备 B 现在已成功接收到一个尚未确认的
TLP，因此启动 AckNak_LATENCY_TIMER（这相当于调度一个 Ack）。

3. 设备 B 在 AckNak_LATENCY_TIMER 到期之前成功接收 TLP 4 和 5。接收 TLP 4 和 5 不会重置 AckNak_LATENCY_TIMER。

4. 一旦 AckNak_LATENCY_TIMER 到期，设备 B 发送一个序列号为 5 的 Ack，这是最后接收到的良好 TLP。AckNak_LATENCY_TIMER 被重置，但在成功接收到 TLP 6 之前不会重新启动。

5. 设备 A 接收到 Ack 5，重置 REPLAY_TIMER 和 REPLAY_NUM 计数器，因为正在取得进展。并且它会从重放缓冲区中清除序列号早于或等于 5 的 TLP。

6. 一旦设备 B 接收到 TLP 6 和 7 并且其 AckNak_LATENCY_TIMER 再次到期，它将发送一个序列号为 7 的 Ack，根据本示例，这将清除设备 A 重放缓冲区中最后两个 TLP。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **PCI Exress Technology**

_图 10-8：示例 1 — Ack 示例_

**==> 图片 [378 x 249] 已省略 <==**

**----- 图片文字开始 -----**<br>
3 Good TLP<br>Receive Buffer<br>4 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>5 Good TLP<br>Replay
Buffer 8 NEXT_RCV_SEQ<br>6<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 7<br>6 Ack<br>Purge Lat Tmr<br>5 5<br>4<br>Earlier TLP 3
Ack/Nak<br>Generator<br>Link<br>7 6<br>**----- 图片文字结束 -----**<br>


**示例 2。** 此示例显示与示例 1 完全相同的行为，但它指出了序列号的回绕行为，如图 10-9（第 333 页）所示。

1. 设备 A 发送序列号为 4094、4095、0、1 和 2 的 TLP，其中 TLP 4094 是本例中发送的第一个 TLP，TLP 2 是本例中发送的最后一个 TLP。

2. 设备 B 按该顺序成功接收序列号为 4094、4095、0、1 的 TLP。接收 TLP 4094 会导致 AckNak_LATENCY_TIMER 启动。TLP 4095、0 和 1 在 AckNak_LATENCY_TIMER 到期之前被接收。TLP 2 仍在传输中。

3. 由于 AckNak_LATENCY_TIMER 已到期，设备 B 发送一个序列号为 1 的 Ack，以确认 TLP 1 以及所有先前的 TLP（本例中为 0、4095 和 4094）的接收。

4. 设备 A 成功接收 Ack 1，从重放缓冲区中清除 TLP 4094、4095、0 和 1，并重置 REPLAY_TIMER 和 REPLAY_NUM 计数。

**第 10 章：Ack/Nak 协议**

_图 10-9：示例 2 — 序列号回绕的 Ack_

**==> 图片 [381 x 260] 已省略 <==**

**----- 图片文字开始 -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>1
Good TLP<br>Replay Buffer 3 NEXT_RCV_SEQ<br>2<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 2 Ack<br>Purge<br>1 1<br>0 Lat
Tmr<br>4095<br>Earlier TLP 4094 Ack/Nak<br>Generator<br>Link<br>2<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **发送方对 Nak 的响应**

Nak 表示发生了问题。当发送方收到 Nak 时，它首先从重放缓冲区中清除任何具有较早或相等序列号的 TLP，然后按 Nak 中的序列号紧随其后的序列号开始重放剩余的 TLP。如果 Nak 导致至少一个 TLP 从缓冲区中被清除，那么我们已经取得了进展。在这种情况下，发送方重置
REPLAY_NUM 计数器和 REPLAY_TIMER，并将 AckD_SEQ 寄存器加载为 Nak 的序列号。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **TLP 重放**

当需要重放时，发送方阻止从事务层接受新的 TLP。然后它按它们放入缓冲区的相同顺序（如 FIFO）重放缓冲区中必要的 TLP。重放事件后，数据链路层解除阻止从事务层接受新的 TLP。

重放的 TLP 保留在缓冲区中，直到它们在稍后的某个时间最终被确认。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **高效的 TLP 重放**

必须在重放期间处理接收到的 Ack 或 Nak DLLP。因此这里有两个主要选项：发送方可以保留它们直到重放完成，然后评估 Ack 或 Nak 并采取适当的步骤。另一个选项是在重放期间开始处理新的 Ack/Nak DLLP。如果使用此选项，新接收的 Ack
可能会在重放进行时从缓冲区中清除某些条目，从而可能减少需要重放的 TLP 数量并节省链路上的时间。这是允许的，但重要的是要记住，一旦 TLP 开始传输，就必须完成。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **Nak 的示例**

请考虑图 10-10（第 335 页）。

1. 设备 A 发送序列号为 4094、4095、0、1 和 2 的 TLP。

2. 设备 B 无错误地接收 TLP 4094，并将 NEXT_RCV_SEQ 计数增加到 4095，然后启动 AckNak_LATENCY_TIMER。

3. 设备 B 在接收到的下一个 TLP (TLP 4095) 中检测到 CRC 错误，并设置 NAK_SCHEDULED 标志，这将导致发送序列号为 4094（NEXT_RCV_SEQ 计数 - 1）的 Nak。设备 B 不会等到 AckNak_LATENCY_TIMER
到期后再发送 Nak。它通常会在下一个报文边界上发送。事实上，由于已调度 Nak 进行传输，因此 AckNak_LATENCY_TIMER 已停止并重置。

4. 设备 B 将继续评估传入的 TLP，寻找 TLP 4095。但是，由于设备 A 尚不知道存在问题，它已发送报文 0、1 和 2，设备 B 将接收它们。但是，设备 B 不会接受它们，即使它们可能是良好的 TLP（这意味着它们未通过 LCRC
检查）。这是因为所有报文必须按顺序接受。所以设备 B 将简单地丢弃这些报文，因为它们被视为顺序错误，但不会发送额外的 Nak。即使这些 TLP 中的一个或多个未通过 LCRC 检查，也不会发送额外的 NAK。NAK_SCHEDULED 标志已置位，只有当设备 B 成功接收到预期的
TLP（本例中为 TLP 4095）时，它才会被清除。

**第 10 章：Ack/Nak 协议**

5. 设备 A 接收到 Nak 4094，并从重放缓冲区中清除 TLP 4094 和较早的 TLP（本例中没有）。此外，由于已取得进展，它会重置 REPLAY_TIMER 和 REPLAY_NUM 计数。

6. 由于接收到的确认 DLLP 是 Nak 而不是 Ack，设备 A 然后重放重放缓冲区中所有剩余的 TLP（TLP 4095、0、1 和 2）并重新启动 REPLAY_TIMER，并将 REPLAY_NUM 计数加一。

7. 一旦设备 B 接收到重放的 TLP 4095，它将清除 NAK_SCHEDULED 标志，递增 NEXT_RCV_SEQ 计数，并启动 AckNak_LATENCY_TIMER。

_图 10-10：Nak 的示例_

**==> 图片 [372 x 242] 已省略 <==**

**----- 图片文字开始 -----**<br>
Receive Buffer 4094 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3
NEXT_RCV_SEQ<br>4095<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 4095 LCRC fail<br>Later TLP 2<br>1<br>0 Lat Tmr<br>4095 Nak 0 Out of
sequence<br>Earlier TLP 4094 Purge 4094 Ack/Nak<br>Generator<br>Link<br>Replayed TLPs<br>2 1 0 4095 2 1<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **TLP 的重复重放**

**概述。** 每次发送方收到 Nak 时，它会重放缓冲区内容，并且 2 位 REPLAY_NUM 计数器递增以跟踪重放事件的数量。前一个示例中由 Nak 导致的重放将使 REPLAY_NUM 递增。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **PCI Exress Technology**

如果重放未清除问题，那么我们就进入了新的情况。接收方已设置 Nak Scheduled 标志，并且在看到有问题的 TLP 被正确接收之前无法再发送任何 Ack 或 Nak。如果由于某种原因重放未发生这种情况，则接收方将没有任何响应。拯救我们的是发送方的
REPLAY_TIMER。当它超时时，将重新发送重放缓冲区的全部内容，REPLAY_NUM 计数器将递增，并且 REPLAY_TIMER 将被重置并重新启动。如果 REPLAY_TIMER 在没有收到表示取得进展的 Ack 或 Nak
的情况下到期，则此重放过程可以重复多达三次。如果在第三次重放后仍然没有取得进展并且 REPLAY_TIMER 再次到期，这将导致 REPLAY_NUM 计数器从 3 回绕到 0。

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-8-4"></a>
## 8.4 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

**General.** Before a device transmits a TLP, it stores a copy of the TLP in the Replay Buffer. ( _Note that the spec uses the term Retry
Buffer but in this book ‘Replay’ was chosen instead of ‘Retry’ to more clearly distinguish this mechanism from the old PCI Retry mechanism_
). Each buffer entry stores a complete TLP with all of its fields including the Sequence Number (12 bits wide, it occu‐ pies two bytes),
Header (up to 16 bytes), an optional Data Payload (up to 4KB), an optional ECRC (four bytes) and the LCRC field (four bytes).

It is important to note that the spec describes the Replay Buffer in this fash‐ ion, but it is NOT a spec requirement that it be implemented
this way. As long as your device can replay a sequence of TLPs if required, as defined by the spec, then how that is accomplished within a
device is completely up to the designer. Having a Replay Buffer that behaves as described above is one way to accomplish this.

**Replay Buffer Sizing.** The spec writers chose not to specify the Replay Buffer size, leaving it as an optimization for the device
designers. It should be made big enough to store TLPs that haven’t yet been acknowledged by Acks so that under normal operating conditions
it doesn’t become full and stall new TLPs coming in from the Transaction Layer, but also small enough to keep the cost down. To determine
the optimal buffer size, a designer will consider:

- Ack DLLP Latency from the receiver. 

- Delays caused by the physical Link. 

- Receiver L0s exit latency to L0. In other words, the buffer should be big enough to hold TLPs without stalling while the Link returns from
the L0s state to L0.

When the transmitter receives an Ack, it purges TLPs from the Replay Buffer with Sequence Numbers equal to or earlier than the Sequence Num‐
ber in the Ack ( _normally this term would be ‘smaller than’ but the counter roll‐ over behavior will sometimes make that an incorrect
evaluation, so the term ‘earlier than’ was chosen instead_ ). Similarly, when the transmitter receives a Nak, it still purges the Replay
Buffer of TLPs with Sequence Numbers that are equal to or earlier than the Sequence Number that arrives in the Nak, but then it also replays
(re‐sends) TLPs of later Sequence Numbers (the remain‐ ing TLPs in the Replay Buffer).

**Cha ter 10: Ack/Nak Protocol p**

</td>
<td width="50%">

**重放编号回绕。** 当这种情况发生时，假设一定是链路出了问题，因此链路层触发物理层重新训练链路，导致其进入 Recovery 状态（参见第 571 页的"Recovery State"）。如果实现了可选的高级错误报告寄存器，则 Replay Number Rollover
错误状态位也将被设置（第 688 页的"高级可纠正错误处理"）。在重新训练过程中保留重放缓冲区的内容并且不初始化链路层（这只是重新训练链路，而不是执行链路复位）。重新训练完成后，发送方恢复相同的重放过程，希望问题已清除并且 TLP 现在可以成功重放。

规范未描述如果链路训练未清除问题，设备可能如何处理重复的回绕事件。作者见过市售的硬件没有任何机制来检测此情况，并且陷入重新训练的无限循环中。因此，似乎应该建议设备跟踪重新训练尝试的次数。经过足够的尝试后，设备可以发出不可纠正的致命错误信号或中断，以此方式通知软件这种情况。

</td>
</tr>
<tr>
<td width="50%">

## **Transmitter’s Response to an Ack DLLP** 

A single Ack returned by the receiver may acknowledge multiple TLPs; it isn’t necessary that every TLP transmitted receive a dedicated Ack.
The receiver can get multiple good TLPs and send one Ack with the Sequence Number of the last good TLP received. The transmitter’s response
to an Ack that makes forward progress (has a Sequence Number that is later than the last one seen) is to load the AckD_SEQ register with the
Sequence Number of the new Ack. It also resets the REPLAY_NUM counter and REPLAY_TIMER, and purges the Replay Buffer of all TLPs that were
acknowledged by that Ack.

</td>
<td width="50%">

## **重放计时器**

发送方 REPLAY_TIMER 在任何已传输但尚未确认的 TLP 存在时都处于运行状态。REPLAY_TIMER 的目标是确保 TLP 及时得到确认。如果此计时器到期，则表明到那时本应已接收到 Ack 或
Nak，因此一定出现了问题，从发送方的角度来看，解决方法是执行重放，这意味着重新发送重放缓冲区中的所有内容。

**第 10 章：Ack/Nak 协议**

基于此计时器的目的，其超时值应该与接收方中的 AckNak_LATENCY_TIMER 相关联，这是有道理的。事实上，REPLAY_TIMER 仅为 AckNak_LATENCY_TIMER 的三倍长。

规范中的公式确定计时器的计数值。其到期触发重放事件并递增 REPLAY_NUM 计数器。超时可能出现的一些情况是：如果 Ack 或 Nak 在传输途中丢失，或者因为接收方中的错误阻止其返回 Ack 或 Nak。与计时器相关的规则：

- 如果尚未运行，则计时器在任何 TLP 的最后一个符号被传输时启动

- 在以下情况下，计时器被重置并重新启动：

 - 收到表示取得进展的 Ack，并且重放缓冲区中仍有未确认的 TLP

 - 发生重放事件，并且发送了第一个重放 TLP 的最后一个符号

- 在以下情况下，计时器被重置并保持：

 - 没有要传输的 TLP，或重放缓冲区为空

 - 收到 Nak；当发送了第一个重放 TLP 的最后一个符号时重新启动

 - 计时器到期；当发送了第一个重放 TLP 的最后一个符号时重新启动

 - 数据链路层处于非活动状态

- 计时器在链路训练或重新训练期间保持

**REPLAY_TIMER 方程。** 超时值主要取决于最大数据有效负载和链路的宽度。下面给出了以符号时间为单位计算 REPLAY_TIMER 值的方程。请注意，该值仅为 Ack/Nak 延迟值的三倍。

( Max_Payload_Size + TLPOverhead ) * AckFactor LinkWidth

+ InternalDelay *** 3** + _Rx_L0s_Adjustment_ ) _此术语已删除_（_针对 Gen2 及更高版本_）

方程字段定义如下：

- **Max_Payload_Size** — Device Control Register 中的值。在多个 Function 具有不同 Max_Payload_Size 值的情况下，规范建议使用它们中的最小值。

- **TLP Overhead** — 数据有效负载之外的额外 TLP 字段（序列号、头部、摘要、LCRC 和 Start/End 成帧符号）。在规范中，开销值被视为 28 个符号的常量。

- **AckFactor (AF)** — 基本上是一个模糊因子，表示在必须发送 Ack 之前可以接收的最大有效负载大小的 TLP 数。AF 值的范围从 1.0 到 3.0，旨在平衡链路带宽效率和重放缓冲区大小。第 339 页的图 10-11
中的表显示了各种链路宽度和有效负载大小的 Ack Factor 值。选择这些 Ack Factor 值是为了允许实现良好的性能而不需要大型的不经济的缓冲区。

- **LinkWidth** — 范围从 x1（1 位宽）到 x32（32 位宽）。

- **InternalDelay** — 在接收方内处理 TLP 以及在发送方内处理 DLLP (Ack) 的内部延迟。此值在规范中以符号时间定义，并且取决于链路速度：Gen1 = 19，Gen2 = 70，Gen3 = 115。

- **Rx_L0s_Adjustment** — 这是 1.x PCIe 规范中包含但在 2.0 及更高版本的 PCIe 规范中已删除的值。它可用于说明接收电路从 L0s 退出到 L0 所需的时间。设置 Link Control 寄存器的 Extended Sync 位会影响从
L0s 的退出时间，必须在该调整中予以考虑。有趣的是，规范编写者在创建其重放计时器值表时选择假设此值为零。在以下部分中会有更多内容。

**REPLAY_TIMER 汇总表。** 第 339 页的图 10-11 是 Gen1 速率的汇总表，示出了 REPLAY_TIMER 方程中各种变量值的计时器加载值。这些数字已针对较新版本的规范进行了更改，可以在第 350
页的"较新规范版本的时序差异"一节中找到新表及其讨论。所有表值的容差为 -0% 到 +100%。

请注意，规范中的表值（此处为方便起见复制）被认为是"未调整的"，因为它们省略了方程中涉及从 L0s 恢复时间的最后一项。规范中未对此进行解释，但如果链路必须从 L0s 唤醒到 L0 才能在超时可能是错误的情况下重放报文，那将是糟糕的电源管理。

**第 10 章：Ack/Nak 协议**

完全避免此问题的一个简单方法是让发送方确保在进入 L0s 之前重放缓冲区为空。规范要求进入 L1 时执行该步骤，但不要求 L0s，原因可能与所涉及的相对风险有关。进入 L1 需要更长的恢复到 L0
的过程，并且存在一些失败的小风险。如果恢复失败，物理层状态机将不得不执行更多的链路训练，这是一个清除到链路层的 LinkUp 标志的过程，导致链路层重新初始化。如果在发生这种情况时重放缓冲区中有条目，它们将丢失并可能导致问题。从 L0s
的恢复风险显然被认为足够低，不需要该要求。尽管如此，L0s 延迟在构建表时被省略，使读者对此感到困惑。作者认为，规范编写者期望设计人员采取措施以确保在 L0s 中不会发生重放计时器超时（通过在进入 L0s 之前清空重放缓冲区），或者如果观察到 Ack 路径处于 L0s，则将延迟。

_图 10-11：Gen1 未调整的 REPLAY_TIMER 值_

|**Max_Payload** **Size**|**X1** **Link**|**X2** **Link**|**X4** **Link**|**X8** **Link**|**X12** **Link**|**x16** **Link**|**X32** **Link**|
|---|---|---|---|---|---|---|---|---|
||**128 字节**|**711**|**384**|**219**|**201**|**174**|**144**|**99**|
||**256 字节**|**1248**|**651**|**354**|**321**|**270**|**216**|**135**|
||**512 字节**|**1677**|**867**|**462**|**258**|**327**|**258**|**156**|
||**1024 字节**|**3213**|**1635**|**846**|**450**|**582**|**450**|**252**|
||**2048 字节**|**6285**|**3171**|**1614**|**834**|**1095**|**834**|**444**|
||**4096 字节**|**12,429**|**6243**|**3150**|**1602**|**2118**|**1602**|**828**|

</td>
</tr>
<tr>
<td width="50%">

## **Ack/Nak Examples** 

**Example 1.** Consider Figure 10‐8 on page 332 for the following discus‐ sion. 

1. Device A transmits TLPs with Sequence Numbers 3, 4, 5, 6, 7. 

2. Device B successfully receives TLP 3 and increments its NEXT_RCV_SEQ counter from 3 to 4. Since Device B had previously acknowledged all
successfully received TLPs, the AckNak_LATENCY_TIMER was not running. Having received TLP 3, Device B has now successfully received a TLP
that it has not acknowledged, so the AckNak_LATENCY_TIMER is started (this is equivalent of scheduling an Ack).

3. Device B successfully receives TLPs 4 and 5 before the AckNak_LATENCY_TIMER expires. Receiving TLPs 4 and 5 does NOT reset the
AckNak_LATENCY_TIMER.

4. Once the AckNak_LATENCY_TIMER expires, Device B sends a single Ack with the Sequence Number 5, the last good TLP received. The
AckNak_LATENCY_TIMER is reset but does not restart until it suc‐ cessfully receives TLP 6.

5. Device A receives Ack 5, resets the REPLAY_TIMER and REPLAY_NUM counter, because forward progress is being made. And it purges TLPs from
the Replay Buffer that have Sequence Numbers earlier than or equal to 5.

6. Once Device B receives TLPs 6 and 7 and its AckNak_LATENCY_TIMER expires again, it will send an Ack with a Sequence Number of 7 which
will purge the last two TLPs in the Replay Buffer of Device A (according to this example).

</td>
<td width="50%">

## **发送方 DLLP 处理**

Ack/Nak 错误检查块确定接收到的 DLLP 的 16 位 CRC 中是否存在错误。如果检测到错误，则丢弃该 DLLP。这被视为可纠正错误，可能已设置为在可选的高级错误报告寄存器中报告（参见第 688 页的"高级可纠正错误处理"中的 Bad
DLLP），但不会采取进一步的操作，因为这实际上不是问题。下一个成功接收的该类型 DLLP 将使计数器恢复最新状态。因此，TLP 可能比原本清除的时间稍晚清除，或者重放可能在稍后的时间发生，但不会丢失任何信息。当然，如果成功 Ack 之间的延迟变得太大，REPLAY_TIMER
可能会到期，从而导致 TLP 被重放。

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 10‐8: Example 1 ‐ Example of Ack_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


**Example 2.** This example is showing the exact same behavior as Exam‐ ple 1, but it is pointing out the rollover behavior for the Sequence
Numbers, as show in Figure 10‐9 on page 333.

1. Device A transmits TLPs with Sequence Numbers 4094, 4095, 0, 1, and 2 where TLP 4094 is the first TLP sent and TLP 2 is the last TLP sent
in this example.

2. Device B successfully receives TLPs with Sequence Numbers 4094, 4095, 0, 1 in that order. Reception of TLP 4094 causes the
AckNak_LATENCY_TIMER to start. TLPs 4095, 0 and 1 are received before the AckNak_LATENCY_TIMER expires. TLP 2 is still en route.

3. Because the AckNak_LATENCY_TIMER expires, Device B send an Ack with a Sequence Number of 1 to acknowledge receipt of TLP 1 and all prior
TLPs (0, 4095 and 4094 in this example).

4. Device A successfully receives Ack 1, purges TLPs 4094, 4095, 0, and 1 from the Replay Buffer and resets the REPLAY_TIMER and REPLAY_NUM
count.

**Cha ter 10: Ack/Nak Protocol p** 

_Figure 10‐9: Example 2 ‐ Ack with Sequence Number Rollover_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **接收方协议详细信息**

</td>
</tr>
<tr>
<td width="50%">

## **Transmitter’s Response to a Nak** 

A Nak indicates that a problem has occurred. When a transmitter receives one, it first purges from the Replay Buffer any TLPs with earlier
or equal Sequence Numbers and then replays the remaining TLPs starting with the Sequence Number immediately after the Sequence Number in the
Nak. If the Nak caused at least one TLP to be purged from the buffer, then we’ve made forward progress. In that case, the transmitter resets
the REPLAY_NUM counter and REPLAY_TIMER and loads the AckD_SEQ register with the Sequence Number of the Nak.

</td>
<td width="50%">

## **物理层**

在物理层接收的 TLP 会检查接收方错误（例如成帧、差异和无效符号）。如果此级别存在错误，则 TLP 被丢弃，并且链路层可能通过某些特定于设计的方法被通知，以便它可以调度 Nak 并重放报文。如果未通知链路层，那么最终它将检测到序列号违规，这将导致 Nak 和重放。

**第 10 章：Ack/Nak 协议**

_图 10-12：Ack/Nak 接收方元素_

**==> 图片 [224 x 283] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule
Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send
Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) =
AckNak_Seq_Num[11:0]<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **TLP Replay** 

When a Replay becomes necessary, the transmitter blocks acceptance of new TLPs from its Transaction Layer. It then replays the necessary
TLPs in the buffer in the same order they were placed into the buffer (like a FIFO). After the replay event, the Data Link Layer unblocks
acceptance of new TLPs from its Transac‐

tion Layer. The replayed TLPs remain in the buffer until they are finally acknowledged at some later time.

</td>
<td width="50%">

## **TLP LCRC 检查**

如果不存在物理层错误，则链路层首先检查 CRC 错误。接收方根据接收到的 TLP（不包括 LCRC 字段）计算预期的 LCRC 值，并将该值与 TLP 的 32 位 LCRC 进行比较。如果两者匹配，则 TLP 是良好的。否则，将丢弃 TLP 并且接收方将调度一个 Nak。

</td>
</tr>
<tr>
<td width="50%">

## **Efficient TLP Replay** 

Ack or Nak DLLPs received during replay must be processed. So there are two main options here, the transmitter may hold them until the
replay is finished and then evaluate the Acks or Naks and take the appropriate steps. Another option would be to begin processing the new
Ack/Nak DLLPs even during the replay. If this option is used, the newly received Acks might purge some entries from the buffer while replay
is in progress, possibly reducing the number of TLPs that need to be replayed and saving time on the Link. This is allowed, but it is
important to remember that once a TLP is started for transmission, it must be completed.

</td>
<td width="50%">

## **下一个接收到的 TLP 的序列号**

如果 LCRC 正确，则接收方接下来将 NEXT_RCV_SEQ 计数器与应在新接收的 TLP 中的序列号进行比较。在正常操作条件下，这两个数字将匹配。如果它们匹配，则接收方将 TLP 转发到事务层，递增 NEXT_RCV_SEQ 计数器，并调度一个 Ack。

如果接收到的 TLP 的序列号早于或晚于 NEXT_RCV_SEQ 计数，那么我们有两种情况之一：重复的 TLP 或乱序的 TLP。

**重复的 TLP。** 如果传入报文的序列号早于（逻辑上较小）预期值，则意味着发送方决定重新发送接收方之前已看到的报文。此重复报文不是错误，尽管我们通过重新发送它浪费了链路上的时间。这可能是由发送方的超时引起的，如果前一个 TLP 的 Ack 或 Nak
失败。当接收方看到此情况时，重复报文将被丢弃，并使用它接收到的最后良好 TLP 的序列号（可能与重放 TLP 中的序列号不同）调度 Ack。

</td>
</tr>
<tr>
<td width="50%">

## **Example of a Nak** 

Consider Figure 10‐10 on page 335. 

1. Device A transmits TLPs with Sequence Number 4094, 4095, 0, 1, and 2. 

2. Device B receives TLP 4094 without error and increments the NEXT_RCV_SEQ count to 4095 and starts the AckNak_LATENCY_TIMER. 

3. Device B detects a CRC error in the next TLP received (TLP 4095) and sets the NAK_SCHEDULED flag, which will cause a Nak to be sent with
Sequence Number 4094 (NEXT_RCV_SEQ count ‐ 1). Device B does NOT wait until the AckNak_LATENCY_TIMER expires before sending the Nak. It will
typically be sent on the next packet boundary. In face, since a Nak is scheduled for transmission, the AckNak_LATENCY_TIMER is stopped and
reset.

4. Device B will continue evaluating incoming TLPs looking for TLP 4095. However, because Device A did not know there was a problem yet, it
had sent packets 0, 1 and 2, which Device B will receive. However, Device B will not accept them, even though they may be good TLPs (meaning
they did not fail the LCRC check). This is because all packets have to be accepted in order. So Device B will simply drop those packets
because they are considered out of sequence, but no addition Nak will be sent. Even if one or more of these TLPs fail the LCRC check, no
additional NAK is sent. The NAK_SCHEDULED flag is already set and it will only be cleared once Device B successfully receives the TLP it is
expecting (TLP 4095 in this example).

**Cha ter 10: Ack/Nak Protocol p** 

5. Device A receives Nak 4094 and purges TLP 4094 and earlier TLPs (none in this example) from the Replay Buffer. Also, since forward
progress was made, it resets the REPLAY_TIMER and REPLAY_NUM count.

6. Since the acknowledge DLLP received was a Nak and not an Ack, Device A then replays all remaining TLPs in the Replay Buffer (TLPs 4095,
0, 1, and 2) and restarts the REPLAY_TIMER and increments the REPLAY_NUM count by one.

7. Once Device B receives the replayed TLP 4095, it will clear the NAK_SCHEDULED flag, increment the NEXT_RCV_SEQ count and start the
AckNak_LATENCY_TIMER.

_Figure 10‐10: Example of a Nak_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **Repeated Replay of TLPs** 

**General.** Each time the transmitter receives a Nak, it replays the buffer contents, and the 2‐bit REPLAY_NUM counter is incremented to
keep track of the number of replay events. The replay caused by a Nak in the previous example will increment REPLAY_NUM.

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

If the replay doesn’t clear the problem, though, we enter a new situation. The receiver has set the Nak Scheduled Flag and cannot send any
more Acks or Naks until it sees the offending TLP correctly received. If the replay doesn’t make that happen for some reason, then there
will be no response from the receiver. What saves us now is the transmitter’s REPLAY_TIMER. When it times out, the entire contents of the
Replay Buffer will be resent, the REPLAY_NUM counter will be incremented and the REPLAY_TIMER will be reset and restarted. If the
REPLAY_TIMER expires without receiving an Ack or Nak indicating forward progress, this replay process can be repeated up to three times. If
after the third replay, there is still no forward progress and the REPLAY_TIMER expires again, this would cause the REPLAY_NUM counter to
roll over from 3 back to 0.

</td>
<td width="50%">

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-8-5"></a>
## 8.5 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

**Replay Number Rollover.** When this happens, the assumption is that there must be something wrong with the Link, so the Link Layer trig‐
gers the Physical Layer to re‐train the Link, causing it to go into the Recov‐ ery State (see “Recovery State” on page 571). If the optional
Advanced Error Reporting registers are implemented, the Replay Number Rollover error status bit will also be set (“Advanced Correctable
Error Handling” on page 688). The Replay Buffer contents are preserved and the Link Layer is not initialized during the re‐training process
(this is simply re‐training the Link, not performing a reset of the Link). When re‐training completes, the transmitter resumes the same
replay process again in hopes that the prob‐ lem has been cleared and the TLPs can now be replayed successfully.

The spec does not describe how a device might handle repeated rollover events if the Link training doesn’t clear the problem. The author has
seen commercially available hardware that had no mechanism to detect this con‐ dition and got stuck in an endless loop of re‐training. It
seems good there‐ fore, to recommend that a device track the number of re‐train attempts. After sufficient attempts, the device could signal
an Uncorrectable Fatal Error or an interrupt as a way to notify software of this condition.

</td>
<td width="50%">

**乱序 TLP。** 如果传入报文的序列号晚于（逻辑上较大）预期值，则唯一的解释是必定丢失了一个 TLP。这是可纠正的错误，通过发送 Nak 来处理。传入的报文是否良好无关紧要，因为它们只能按正确的序列号顺序接受。该报文被丢弃，接收方等待具有预期序列号的 TLP。

当接收到带有 CRC 错误、被作废或序列号检查失败的 TLP 时，NEXT_RCV_SEQ 计数器不会递增。

发送方根据 PCI 排序规则对 TLP 进行排序，以维持正确的程序流并避免潜在的死锁和活锁条件（参见第 8 章，标题为"事务排序"，第 285 页）。接收方需要保留此顺序并应用以下三条规则：

- 当接收方检测到错误的 TLP 时，它会丢弃该 TLP 以及流水线中跟随的所有新 TLP，直到检测到重放的 TLP。

- 重复的 TLP 将被丢弃。

- 在等待丢失或损坏的 TLP 期间接收到的 TLP 将被丢弃。

</td>
</tr>
<tr>
<td width="50%">

## **Replay Timer** 

The transmitter REPLAY_TIMER is running anytime there are TLPs that have been transmitted but have not yet been acknowledged. The goal of
the REPLAY_TIMER is to ensure that TLPs are being acknowledged in a timely fashion. If this timer expires, it indicates that an Ack or Nak
should have been received by that point in time, so something must have gone wrong and the fix from the transmitter’s point‐of‐view is to
perform a replay, meaning to re‐send everything in the Replay Buffer.

**Cha ter 10: Ack/Nak Protocol p** 

Based on the purpose of this timer, it makes sense that its timeout value should be correlated the AckNak_LATENCY_TIMER in the receiver. In
fact, the REPLAY_TIMER is simply three times longer than the AckNak_LATENCY_TIMER.

A formula in the spec determines the timer’s count value. Its expiration triggers a replay event and increments the REPLAY_NUM counter. A
couple of cases where timeout may arise is if an Ack or Nak is lost en route, or because an error in the receiver prevents it from returning
an Ack or Nak. Timer‐related rules:

- If not already running, the timer starts when the last symbol of any TLP is transmitted 

- The timer is reset and restarted when: 

 - An Ack indicating forward progress is received, AND there are still unacknowledged TLPs in the Replay Buffer 

 - A Replay event occurs and the last symbol of the first replayed TLP is sent 

- The timer is reset and held when: 

 - There are no TLPs to transmit, or the Replay Buffer is empty 

 - A Nak is received; it restarts when the last symbol of the first replayed TLP is sent 

 - The timer expires; it restarts when the last symbol of the first replayed TLP is sent 

 - 

 - The Data Link Layer is inactive 

- The timer is held during Link training or re‐training 

**REPLAY_TIMER Equation.** The timeout value depends primarily on the max data payload and the width of the Link. The equation to calculate
the REPLAY_TIMER value in symbol times is given below. Note that the value is simply three times the Ack/Nak Latency value.

. 

( Max_Payload_Size + TLPOverhead ) * AckFactor LinkWidth ( 

+ InternalDelay *** 3** + _Rx_L0s_Adjustment_ ) _this term removed_ ( _for Gen2 and later_ ) 

The equation fields are defined as follows: 

- **Max_Payload_Size** ‐ the value in the Device Control Register. In the case of multiple Functions with different Max_Payload_Size values,
the spec recommends using the smallest one of them.

- **TLP Overhead** ‐ the additional TLP fields beyond the data payload (sequence number, header, digest, LCRC and Start/End framing sym‐
bols). In the spec, the overhead value is treated as a constant of 28 sym‐ bols.

- **AckFactor** (AF) ‐ is basically a fudge factor representing the number of max payload‐sized TLPs that can be received before an Ack must
be sent. The AF value ranges from 1.0 to 3.0 and is intended to balance Link bandwidth efficiency and Replay Buffer size. The table in
Figure 10‐11 on page 339 shows the Ack Factor values for various link widths and payload sizes. These Ack Factor values are chosen to allow
imple‐ mentations to achieve good performance without requiring a large uneconomical buffer.

- **LinkWidth** ‐ ranges from x1 (1‐bit wide) to x32 (32‐bits wide). 

- **InternalDelay** ‐ the internal delay of processing a TLP within the receiver and DLLPs (Acks) within the transmitter. This value is
defined in the spec in symbol times, and depends on the Link speed: Gen1 = 19, Gen2 = 70, Gen3 = 115.

- **Rx_L0s_Adjustment** ‐ This is a value that was included in the 1.x PCIe specs but was dropped for 2.0 and later PCIe specs. It could be
used to account for the time required by the receive circuits to exit from L0s to L0. Setting the Extended Sync bit of the Link Control
register affects the exit time from L0s and must be taken into account in this adjustment. Interestingly, the spec writers chose to assume
this to be zero when cre‐ ating their table of Replay Timer values. More on this in the following section.

**REPLAY_TIMER Summary Table.** Figure 10‐11 on page 339 is a summary table for the Gen1 rate that shows timer load values for various
values of the variables in the REPLAY_TIMER equation. The numbers have changed for the newer generations of the spec, and the new tables and
a dis‐ cussion of them can be found in the section called “Timing Differences for Newer Spec Versions” on page 350. The tolerance for all of
the table values is ‐0% to +100%.

Note that the table values in the spec (copied here for convenience) are con‐ sidered “unadjusted” because they leave out the last item of
the equation involving the time to recover from L0s. No explanation is given for this in the spec, but if the Link had to wake up from L0s
to L0 just to replay a packet in case the timeout might have been an error, that would be poor power management.

**Cha ter 10: Ack/Nak Protocol p** 

A simple way to avoid this problem altogether is for the transmitter to ensure that the Replay Buffer is empty before entering L0s. The spec
requires that step for entry into L1 but not L0s, and the reason probably has to do with the relative risk involved. Going to L1 requires a
longer recovery process back to L0 that has some small risk of failure. If it fails to recover, the Physical Layer state machine will have
to do more of the Link training, a process that clears the LinkUp flag to the Link Layer, causing the Link Layer to re‐initialize. If there
were entries in the Replay Buffer when that happened they’d be lost and problems could result. The recovery risk from L0s was evidently
considered low enough not to warrant that requirement. Still, the L0s latency was left out when the table was constructed, leaving the
reader to wonder about this. In the author’s opinion, the spec writers expected designers to take steps to ensure that a Replay Timer
timeout either doesn’t occur while in L0s (by emptying the Replay Buffer before L0s entry), or will be delayed if the path for the Acks is
observed to be in L0s.

_Figure 10‐11: Gen1 Unadjusted REPLAY_TIMER Values_ 

|**Max_Payload** **Size**|**X1** **Link**|**X2** **Link**|**X4** **Link**|**X8** **Link**|**X12** **Link**|**x16** **Link**|**X32** **Link**|
|---|---|---|---|---|---|---|---|---|
||**128 Bytes**|**711**|**384**|**219**|**201**|**174**|**144**|**99**|
||**256 Bytes**|**1248**|**651**|**354**|**321**|**270**|**216**|**135**|
||**512 Bytes**|**1677**|**867**|**462**|**258**|**327**|**258**|**156**|
||**1024 Bytes**|**3213**|**1635**|**846**|**450**|**582**|**450**|**252**|
||**2048 Bytes**|**6285**|**3171**|**1614**|**834**|**1095**|**834**|**444**|
||**4096 Bytes**|**12,429**|**6243**|**3150**|**1602**|**2118**|**1602**|**828**|
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||

</td>
<td width="50%">

## **接收方调度 Ack DLLP**

如果接收方的数据链路层未检测到传入 TLP 中的错误，它会将 TLP 转发到事务层。NEXT_RCV_SEQ 计数器递增，并且接收方启动 AckNak_LATENCY_TIMER（假设它尚未运行）。这等同于"调度一个 Ack"。允许接收方继续接收良好的 TLP 而无需发送
Ack，直到 AckNak_LATENCY_TIMER 到期。当计时器到期时

**第 10 章：Ack/Nak 协议**

仅发送一个 Ack，其中包含最后良好 TLP 的序列号，确认已成功接收当前 Ack 序列号之前的所有 TLP。此技术通过减少 Ack/Nak 流量来提高链路效率。回顾一下，此技术之所以有效，是因为 TLP 必须始终按顺序成功接收。

</td>
</tr>
<tr>
<td width="50%">

## **Transmitter DLLP Handling** 

The Ack/Nak Error Checking block determines whether there is an error in the 16‐bit CRC of a received DLLP. If an error is detected, the
DLLP is discarded. This is considered a correctable error and may have been set up to be reported in the optional Advanced Error Reporting
registers (see Bad DLLP in “Advanced Correctable Error Handling” on page 688), but no further action is taken because this isn’t really a
problem. The next successfully received DLLP of that type will bring the counters back up to speed. Consequently, TLPs might be purged a
little later than they would have been or a replay may happen at a later time, but no information is lost. Of course, if the delay between
successful Acks becomes too large, the REPLAY_TIMER could expire, causing the TLPs to be replayed.

</td>
<td width="50%">

## **接收方调度 Nak**

如前面在接收方逻辑讨论中所提到的（参见第 324 页的"接收方元素"），当接收方检测到 TLP 上的错误时，它会丢弃错误的报文，并在 NAK_SCHEDULED 标志（如果已清除）已清除时设置它，这将导致使用 NEXT_RCV_SEQ 计数 - 1 的序列号调度一个
Nak。由于现在已调度 Nak，因此 AckNak_LATENCY_TIMER 已重置并停止。可以将调度 Nak 视为"边沿触发"事件，而不是电平触发事件。正是看到 NAK_SCHEDULED 标志的上升沿才会导致调度 Nak。在下一个上升沿之前无法再发送另一个
Nak，这意味着必须先清除 NAK_SCHEDULED 标志（下降沿）。只有两个事件会清除 NAK_SCHEDULED 标志。第一个是成功接收预期的下一个 TLP（序列号与 NEXT_RCV_SEQ 计数匹配的 TLP）。第二个是链路复位（不是重新训练，而是复位）。

尽管尽快将 Nak 传送到发送方很重要（直到失败的那个被无误地看到之前不能接受其他 TLP），但其他传出的 TLP、DLLP 或有序集可能正在进行中或具有比 Nak 更高的优先级，这意味着接收方必须延迟 Nak 的传输，直到它们完成（参见第 350
页的"推荐用于调度报文的优先级"）。同时，如果其他 TLP 到达接收方，则它们将被丢弃，并且在 NAK_SCHEDULED 标志置位时不会调度其他 Ack 或 Nak。

</td>
</tr>
<tr>
<td width="50%">

## **Receiver Protocol Details**

</td>
<td width="50%">

## **AckNak_LATENCY_TIMER**

此计时器定义了接收方在必须为成功接收的 TLP（或 TLP 序列）发送 Ack 之前可以等待多长时间。如前所述，当接收方成功接收尚未确认的 TLP 时，此计时器一直处于运行状态。一旦计时器到期，将调度一个 Ack 进行传输，其中包含它接收到的最后良好 TLP 的序列号。调度
Ack 会重置 AckNak_LATENCY_TIMER，并且只有在成功接收下一个 TLP 时才会再次开始计数。

</td>
</tr>
<tr>
<td width="50%">

## **Physical Layer** 

TLPs received at the Physical Layer are checked for receiver errors (such as framing, disparity, and invalid symbols). If there are errors
at this level, the TLP is discarded and the Link Layer may be informed by some design‐specific method so it can schedule a Nak and have the
packet replayed. If the Link Layer is not informed, then eventually it will detect a Sequence Number violation and that will cause a Nak and
a replay.

**Cha ter 10: Ack/Nak Protocol p** 

_Figure 10‐12: Ack/Nak Receiver Elements_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **AckNak_LATENCY_TIMER 方程。**

AckNak_LATENCY_TIMER 的超时值由规范定义，并根据协商的链路宽度和启用的最大有效负载大小而变化。下面显示了定义超时的方程：

( Max_Payload_Size + TLPOverhead ) * AckFactor

+ InternalDelay + _Tx_L0s_Adjustment_ LinkWidth _此术语已删除_（_针对 Gen2 及更高版本_）

计时器中的值以符号时间为单位给出，即将一个符号发送到链路上所需的时间：Gen1 为 4ns，Gen2 为 2ns，Gen3 为 1ns。

方程字段为：

- **Max_Payload_Size** — Device Control Register 中的值。在多个 Function 具有不同 Max_Payload_Size 值的情况下，规范建议使用它们中的最小值。

- **TLPOverhead** — 数据有效负载之外的额外 TLP 字段（序列号、头部、摘要、LCRC 和 Start/End 成帧符号）。在规范中，开销值被视为 28 个符号的常量。

- **AckFactor (AF)** — 基本上是一个模糊因子，表示在必须发送 Ack 之前可以接收的最大有效负载大小的 TLP 数。AF 值的范围从 1.0 到 3.0，旨在平衡链路带宽效率和重放缓冲区大小。第 339 页的图 10-11
中的表显示了各种链路宽度和有效负载大小的 Ack Factor 值。选择这些 Ack Factor 值是为了允许实现良好的性能而不需要大型的不经济的缓冲区。

- **LinkWidth** — 范围从 x1（1 位宽）到 x32（32 位宽）。— 从 1 到 32 个 Lane。

- **InternalDelay** — 在接收方内处理 TLP 以及在发送方内处理 DLLP (Ack) 的内部延迟。此值在规范中以符号时间定义，并且取决于链路速度：Gen1 = 19，Gen2 = 70，Gen3 = 115。

- **Tx_L0s_Adjustment** — 这是 1.x PCIe 规范中包含但在 2.0 及更高版本的 PCIe 规范中已删除的值。它可用于说明接收电路从 L0s 退出到 L0 所需的时间。设置 Link Control 寄存器的 Extended Sync 位会影响从
L0s 的退出时间，必须在该调整中予以考虑。有趣的是，规范编写者在创建其重放计时器值表时选择假设此值为零。

**第 10 章：Ack/Nak 协议**

**AckNak_LATENCY_TIMER 汇总表。** 第 345 页的图 10-2 显示了 AckNak_LATENCY_TIMER 方程中使用的所有可能值的 Gen1 计时器加载值。较高的数据速率会更改方程和生成的表（参见第 350
页的"较新规范版本的时序差异"）。与重放计时器表类似，此表的构建假设方程中的 L0s 调整为零，然后将生成的值称为"未调整"。请注意，所有表值的容差为 -0% 到 +100%。

_表 10-2：Gen1 未调整的 Ack 传输延迟_

|**Max_Payload** **Size**|**X1** **Link**|**X2** **Link**|**X4** **Link**|**X8** **Link**|**X12** **Link**|**x16** **Link**|**X32** **Link**|
|---|---|---|---|---|---|---|---|
|**128
字节**|**237**<br>**(AF=1.4)**|**128**<br>**(AF=1.4)**|**73**<br>**(AF=1.4)**|**67**<br>**(AF=2.5)**|**58**<br>**(AF=3.0)**|**48**<br>**(AF=3.0)**|**33**<br>**(AF=3.0)**|
|**256
字节**|**416**<br>**(AF=1.4)**|**217**<br>**(AF=1.4)**|**118**<br>**(AF=1.4)**|**107**<br>**(AF=2.5)**|**90**<br>**(AF=3.0)**|**72**<br>**(AF=3.0)**|**45**<br>**(AF=3.0)**|
|**512
字节**|**559**<br>**(AF=1.0)**|**289**<br>**(AF=1.0)**|**154**<br>**(AF=1.0)**|**86**<br>**(AF=1.0)**|**109**<br>**(AF=2.0)**|**86**<br>**(AF=2.0)**|**52**<br>**(AF=2.0)**|
|**1024
字节**|**1071**<br>**(AF=1.0)**|**545**<br>**(AF=1.0)**|**282**<br>**(AF=1.0)**|**150**<br>**(AF=1.0)**|**194**<br>**(AF=2.0)**|**150**<br>**(AF=2.0)**|**84**<br>**(AF=2.0)**|
|**2048
字节**|**2095**<br>**(AF=1.0)**|**1057**<br>**(AF=1.0)**|**538**<br>**(AF=1.0)**|**278**<br>**(AF=1.0)**|**365**<br>**(AF=2.0)**|**278**<br>**(AF=2.0)**|**148**<br>**(AF=2.0)**|
|**4096
字节**|**4143**<br>**(AF=1.0)**|**2081**<br>**(AF=1.0)**|**1050**<br>**(AF=1.0)**|**534**<br>**(AF=1.0)**|**706**<br>**(AF=2.0)**|**534**<br>**(AF=2.0)**|**276**<br>**(AF=2.0)**|

</td>
</tr>
<tr>
<td width="50%">

## **TLP LCRC Check** 

If there were no Physical Layer errors, the Link Layer checks first for CRC errors. The receiver calculates an expected LCRC value from the
received TLP (excluding the LCRC field) and compares this value with the TLP’s 32‐bit LCRC. If the two match, the TLP is good. Otherwise,
the TLP is discarded and the receiver schedules a Nak.

</td>
<td width="50%">

## **更多示例**

在课堂设置中，示例通常使理解 Ack/Nak 过程变得容易得多，因此这里提供了一些示例来说明特殊情况。

</td>
</tr>
<tr>
<td width="50%">

## **Next Received TLP’s Sequence Number** 

If the LCRC was correct, the receiver next compares the NEXT_RCV_SEQ counter against the Sequence Number that should be in the
newly‐received TLP. Under normal operational conditions, these two numbers will match. If they do, the receiver forwards the TLP to the
Transaction Layer, increments the NEXT_RCV_SEQ counter, and schedules an Ack.

If the received TLP’s Sequence Number turns out to be earlier or later than the NEXT_RCV_SEQ count, we have one of two cases: a duplicate
TLP or an out of sequence TLP.

**Duplicate TLP.** If the Sequence Number of the incoming packet is ear‐ lier (logically smaller) than the expected value, it means the
transmitter decided to resend a packet that the receiver has already seen before. This duplicate packet is not an error although we are
wasting time on the Link by resending it. This might be caused by a timeout at the transmitter if the Ack or Nak for a previous TLP failed.
When this is seen at the receiver, the duplicate packet is discarded and an Ack is scheduled with the Sequence Number of the last good TLP
it has received (which is probably not the same Sequence Number in the replayed TLP).

</td>
<td width="50%">

## **丢失的 TLP**

请考虑第 346 页的图 10-13，展示如何检测和处理丢失的 TLP。

1. 设备 A 发送 TLP 4094、4095、0、1 和 2。

2. 设备 B 成功接收 TLP 4094，因此它启动其 AckNak_LATENCY_TIMER 并递增其 NEXT_RCV_SEQ 计数。此后，它还接收 TLP 4095 和 0。

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **PCI Exress Technology**

3. 接收 TLP 0 后，AckNak_LATENCY_TIMER 到期，这会导致它调度一个序列号为 0 的 Ack。

4. 看到 Ack 0 后，设备 A 从其重放缓冲区中清除 TLP 4094、4095 和 0。

5. TLP 1 由于某种原因在传输途中丢失（可能是物理层将其丢弃），而 TLP 2 到达。序列号检查向设备 B 显示 TLP 2 的序列号不等于 NEXT_RCV_SEQ 计数，而是处于乱序范围内。

6. 设备 B 丢弃 TLP 2 并设置 NAK_SCHEDULED 标志，这将在这种情况下发送 Nak 0 (NEXT_RCV_SEQ 计数 - 1)。

7. 收到 Nak 0 后，设备 A 重放 TLP 1 和 2。它会从重放缓冲区中清除 TLP 0 以及任何较早的 TLP，但它们已被先前的操作删除，因此变得不必要。

8. TLP 1 和 2 无错误地到达设备 B，并被转发到事务层。

_图 10-13：处理丢失的 TLP_

**==> 图片 [382 x 265] 已省略 <==**

**----- 图片文字开始 -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link
Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>1<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 2 Out of sequence<br>Later TLP 2<br>1 Ack<br>Purge
Lat Tmr<br>0 0<br>4095<br>Earlier TLP 4094 Ack/Nak<br>0 Nak Generator<br>Link<br>Replayed TLPs<br>2 1<br>**----- 图片文字结束 -----**<br>


**第 10 章：Ack/Nak 协议**

</td>
</tr>
<tr>
<td width="50%">

</td>
<td width="50%">

## **错误的 Ack**

图 10-14（第 347 页）显示了处理损坏的 Ack 的协议。

1. 设备 A 发送 TLP 4094、4095、0、1 和 2。

2. 设备 B 接收 TLP 4094、4095 和 0，将 NEXT_RCV_SEQ 设置为 1，并在 AckNak_LATENCY_TIMER 到期时返回 Ack 0。

3. Ack 0 在链路上的传输过程中有一个位错误，因此当设备 A 检查其 16 位 CRC 时，它未通过检查并被丢弃。这意味着 TLP 4094、4095 和 0 保留在设备 A 的重放缓冲区中。

4. TLP 1 和 2 到达设备 B 并且是良好的，因此 NEXT_RCV_SEQ 计数递增到 3，并且一旦 AckNak_LATENCY_TIMER 再次到期，就返回 Ack 2。

5. Ack 2 安全到达设备 A，设备 A 从其重放缓冲区中清除 TLP 4094、4095、0、1 和 2。

如果 Ack 2 也丢失或损坏，并且没有其他 Ack 或 Nak DLLP 返回到设备 A，则其 REPLAY_TIMER 到期，导致其整个缓冲区被重放。设备 B 看到 TLP 4094、4095、0、1 和 2 并认为它们是重复的 [它们的序列号早于 NEXT_RCV_SEQ
计数 (3)]。它们被丢弃，由于重复报文，会向设备 A 返回 _另一个_ Ack 2。

_图 10-14：处理错误的 Ack_

**==> 图片 [368 x 221] 已省略 <==**

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-8-6"></a>
## 8.6 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

**Out of Sequence TLP.** If the Sequence Number of the incoming packet is later (logically larger) than the expected value, the only
explana‐ tion is that a TLP must have been lost. This is a correctable error and is han‐ dled by sending a Nak. It doesn’t matter if the
incoming packet is good because they can only be accepted in correct Sequence Number order. The packet is discarded and the receiver waits
for a TLP with the expected Sequence Number.

The NEXT_RCV_SEQ counter is not incremented when a TLP is received with a CRC error, or was nullified, or for which the Sequence Number
check fails.

A transmitter orders TLPs according to the PCI ordering rules to maintain cor‐ rect program flow and avoid potential deadlock and livelock
conditions (see Chapter 8, entitled ʺTransaction Ordering,ʺ on page 285). The Receiver is required to preserve this order and applies these
three rules:

- When the receiver detects a bad TLP, it discards the TLP and all new TLPs that follow in the pipeline until the replayed TLPs are
detected.

- Duplicate TLPs are discarded. 

- TLPs received while waiting for a lost or corrupt TLP are discarded.

</td>
<td width="50%">

既然我们已经描述了协议的工作方式，现在是解释其一般操作异常的好时机。PCIe 支持称为"直通模式 (cut-through mode)"的交换机特性，可用于改善大型 TLP 通过交换机的传输延迟。

**第 10 章：Ack/Nak 协议**

</td>
</tr>
<tr>
<td width="50%">

## **Receiver Schedules An Ack DLLP** 

If the Data Link Layer of the receiver does not detect an error in an incoming TLP, it forwards the TLP to the Transaction Layer. The
NEXT_RCV_SEQ counter is incremented and the receiver starts the AckNak_LATENCY_TIMER (assuming it was not already running). This is the
equivalent of “scheduling an Ack.” The receiver is allowed to continue receiving good TLPs without sending an Ack until the
AckNak_LATENCY_TIMER expires. When the timer expires it

**Cha ter 10: Ack/Nak Protocol p** 

sends just one Ack with the Sequence Number of the last good TLP, acknowl‐ edging good receipt of all received TLPs up to the Sequence
Number in the cur‐ rent Ack. This technique improves Link efficiency by reducing Ack/Nak traffic. For review, recall that this technique
works because the TLPs must always be successfully received in order.

</td>
<td width="50%">

## **背景**

考虑一个示例，其中一个大型 TLP 需要通过交换机，如图 10-16（第 357 页）所示。由于入口交换机端口在看到整个 TLP
之前无法判断报文中是否有错误，因此它通常会存储整个报文并在转发到出口端口之前检查错误。这种存储转发方法有效，但对于大型报文，通过交换机的延迟可能很大，这可能是某些应用程序的问题。如果可能的话，最好尽量减少这种延迟。

</td>
</tr>
<tr>
<td width="50%">

## **Receiver Schedules a Nak** 

As mentioned earlier in the discussion of the receiver logic (see “Receiver Ele‐ ments” on page 324), when the receiver detects an error on
a TLP, it discards the bad packet and sets the NAK_SCHEDULED flag if it was clear, which will cause a Nak to be scheduled with the Sequence
Number of NEXT_RCV_SEQ count ‐ 1. Since a Nak is now scheduled, the AckNak_LATENCY_TIMER is reset and halted. Scheduling a Nak can be
thought of as being an “edge‐triggered” event instead of a level‐triggered event. It is seeing the rising edge of the NAK_SCHEDULED flag
that causes a Nak to be scheduled. Another Nak can‐ not be sent until the next rising edge, which means the NAK_SCHEDULED flag must be
cleared (falling edge) first. There are only two events that will clear the NAK_SCHEDULED flag. The first is successfully receiving the
expected next TLP (TLP with a Sequence Number that matches the NEXT_RCV_SEQ count). The second is a reset of the link (not retraining, but
reset).

Although it’s important to get the Nak to the transmitter quickly (no other TLPs can be accepted until the failed one is seen without
errors), other outgoing TLPs, DLLPs or Ordered Sets already be in progress or have a higher priority than the Nak which means the receiver
would have to delay the transmission of the Nak until they’re done (see “Recommended Priority To Schedule Packets” on page 350). In the
meantime, if other TLPs arrive at the receiver they are dis‐ carded and no additional Acks or Naks will be scheduled while the NAK_SCHEDULED
flag is set.

</td>
<td width="50%">

## **延迟改进选项**

由于 TLP 的第一部分包含带有报文路由信息的头部，因此一种选择是假设报文是良好报文，并在接收到整个报文之前就开始评估头部中的路由信息。这将允许交换机在评估该路由后立即开始将 TLP
转发到出口端口。然后，出口端口可以继续开始通过其链路发送它，只要这样做不会导致交换机内的下溢情况。（如果入口端口是 x1 而出口端口是 x16，则可能很容易发生潜在的下溢情况。出口端口发送报文的速度将远快于其被接收的速度。）

当然，入口端口在接收到报文末尾的 LCRC 之前无法检查报文中的错误，因此存在一个小风险，即正在向外转发的 TLP 可能实际上包含错误。最终，TLP 的末尾到达入口端口，可以检查报文。如果发现有错误，则入口端口对错误的 TLP 采取正常行为，并简单地发送一个 Nak
以重放报文。但是，现在我们必须处理这样一个问题：现在我们知道大部分已损坏的报文已经被转发到出口端口。在这种情况下我们有什么选择？我们可以完成报文的转发并等待相邻接收方在看到错误时发送
Nak，但重放缓冲区中的报文将是错误的报文，因此那里的重放无法解决问题。我们可能截断传输中的错误报文，但规范不允许这种可能性。要使其工作，我们需要另一个选项，这就是直通选项发挥作用的地方。

</td>
</tr>
<tr>
<td width="50%">

## **AckNak_LATENCY_TIMER** 

This timer defines how long a receiver can wait before it must send an Ack for a successfully received TLP (or sequence of TLPs). As stated
before, this timer is running anytime a receiver successfully receives a TLP that it has not yet acknowledged. Once the timer expires, an
Ack is scheduled for transmission with the Sequence Number of the last good TLP it received. Scheduling an Ack resets the
AckNak_LATENCY_TIMER and it only starts counting again once the next TLP is successfully received.

</td>
<td width="50%">

## **直通操作**

直通模式提供了上一节中描述的转发问题的解决方案：如果在传入报文中看到错误，则已经在外发途中的报文必须被"**作废 (nullified)**"。

**作废**的报文以 EDB (end bad) 符号而不是 END (end good) 符号终止，并且为了使条件非常清楚，TLP 的 32 位 LCRC 从原始计算值反相（1 的补码）。本质上，作废的报文被视为从未存在过。在交换机出口端口上，这意味着重放缓冲区丢弃该报文，并且
NEXT_TRANSMIT_SEQ 计数器减一（回滚）。

当设备接收到它识别为已作废的 TLP 的 TLP 时，它只是丢弃该报文并将其视为从未存在过。NEXT_RCV_SEQ 不会递增，AckNak_LATENCY_TIMER 不会启动，也不会设置 NAK_SCHEDULED。接收设备静默丢弃已作废的 TLP 并且不会为其返回
Ack/Nak。

</td>
</tr>
<tr>
<td width="50%">

## **AckNak_LATENCY_TIMER Equation.** 

The timeout value for the AckNak_LATENCY_TIMER is defined by the spec and varies based on the Negotiated Link Width and Max Payload Size
Enabled. The equation which defines the timeout is shown below:

( Max_Payload_Size + TLPOverhead ) * AckFactor 

+ InternalDelay + _Tx_L0s_Adjustment_ LinkWidth _this term removed_ ( _for Gen2 and later_ ) 

The value in the timer is given in symbol times, the time it takes to send one symbol across the Link: 4ns for Gen1, 2ns for Gen2, and 1ns
for Gen3.

The equation fields are: 

- **Max_Payload_Size** ‐ the value in the Device Control Register. In the case of multiple Functions with different Max_Payload_Size values,
the spec recommends using the smallest one of them.

- **TLPOverhead** ‐ the additional TLP fields beyond the data payload (sequence number, header, digest, LCRC and Start/End framing sym‐
bols). In the spec, the overhead value is treated as a constant of 28 sym‐ bols.

- **AckFactor** (AF) ‐ is basically a fudge factor representing the number of max payload‐sized TLPs that can be received before an Ack must
be sent. The AF value ranges from 1.0 to 3.0 and is intended to balance Link bandwidth efficiency and Replay Buffer size. The table in
Figure 10‐11 on page 339 shows the Ack Factor values for various link widths and payload sizes. These Ack Factor values are chosen to allow
imple‐ mentations to achieve good performance without requiring a large uneconomical buffer.

- **LinkWidth** ‐ ranges from x1 (1‐bit wide) to x32 (32‐bits wide).‐ from 1 to 32 Lanes. 

- **InternalDelay** ‐ the internal delay of processing a TLP within the receiver and DLLPs (Acks) within the transmitter. This value is
defined in the spec in symbol times, and depends on the Link speed: Gen1 = 19, Gen2 = 70, Gen3 = 115.

- **Tx_L0s_Adjustment** : ‐ This is a value that was included in the 1.x PCIe specs but was dropped for 2.0 and later PCIe specs. It could
be used to account for the time required by the receive circuits to exit from L0s to L0. Setting the Extended Sync bit of the Link Control
register affects the exit time from L0s and must be taken into account in this adjustment. Interestingly, the spec writers chose to assume
this to be zero when cre‐ ating their table of Replay Timer values.

**Cha ter 10: Ack/Nak Protocol p** 

**AckNak_LATENCY_TIMER Summary Table.** Figure 10‐2 on page 345 shows the Gen1 timer load values for all the possible values used in the
AckNak_LATENCY_TIMER equation. Higher data rates change the equation and the resulting table (see “Timing Differences for Newer Spec
Versions” on page 350). Like the Replay Timer table, this table is con‐ structed by assuming the L0s adjustment in the equation is zero and
then referring to the resulting values as ‘unadjusted’. Note that the tolerance for all of the table values is ‐0% to +100%.

_Table 10‐2: Gen1 Unadjusted Ack Transmission Latency_ 

|**Max_Payload** **Size**|**X1** **Link**|**X2** **Link**|**X4** **Link**|**X8** **Link**|**X12** **Link**|**x16** **Link**|**X32** **Link**|
|---|---|---|---|---|---|---|---|
|**128
Bytes**|**237**<br>**(AF=1.4)**|**128**<br>**(AF=1.4)**|**73**<br>**(AF=1.4)**|**67**<br>**(AF=2.5)**|**58**<br>**(AF=3.0)**|**48**<br>**(AF=3.0)**|**33**<br>**(AF=3.0)**|
|**256
Bytes**|**416**<br>**(AF=1.4)**|**217**<br>**(AF=1.4)**|**118**<br>**(AF=1.4)**|**107**<br>**(AF=2.5)**|**90**<br>**(AF=3.0)**|**72**<br>**(AF=3.0)**|**45**<br>**(AF=3.0)**|
|**512
Bytes**|**559**<br>**(AF=1.0)**|**289**<br>**(AF=1.0)**|**154**<br>**(AF=1.0)**|**86**<br>**(AF=1.0)**|**109**<br>**(AF=2.0)**|**86**<br>**(AF=2.0)**|**52**<br>**(AF=2.0)**|
|**1024
Bytes**|**1071**<br>**(AF=1.0)**|**545**<br>**(AF=1.0)**|**282**<br>**(AF=1.0)**|**150**<br>**(AF=1.0)**|**194**<br>**(AF=2.0)**|**150**<br>**(AF=2.0)**|**84**<br>**(AF=2.0)**|
|**2048
Bytes**|**2095**<br>**(AF=1.0)**|**1057**<br>**(AF=1.0)**|**538**<br>**(AF=1.0)**|**278**<br>**(AF=1.0)**|**365**<br>**(AF=2.0)**|**278**<br>**(AF=2.0)**|**148**<br>**(AF=2.0)**|
|**4096
Bytes**|**4143**<br>**(AF=1.0)**|**2081**<br>**(AF=1.0)**|**1050**<br>**(AF=1.0)**|**534**<br>**(AF=1.0)**|**706**<br>**(AF=2.0)**|**534**<br>**(AF=2.0)**|**276**<br>**(AF=2.0)**|

</td>
<td width="50%">

## **直通操作示例**

图 10-16（第 357 页）说明了从左侧进入、通过交换机并最终到达右侧端点的 TLP。在左侧链路上发生 TLP 错误。步骤如下：

1. 在交换机入口端口看到传入的 TLP。它在传输过程中已损坏，但尚未知晓。

2. TLP 头部到达，被解码，并且报文在直通操作中转发到目标出口端口。

3. 最终，报文的末尾到达，交换机入口端口能够完成 LCRC 错误检查。它发现 CRC 错误，并将 Nak 返回给 TLP 源。

4. 在出口端口，交换机将错误 TLP 末尾的 END 成帧符号替换为 EDB，并反相计算出的 LCRC 值。TLP 现在被"作废"，交换机从重放缓冲区中丢弃它。

5. 作废的报文到达端点。端点检测到 EDB 符号和反相的 LCRC，并静默丢弃该报文。它不会返回 Nak。

现在假设 TLP 源设备重放报文并且没有发生错误。和以前一样，TLP 以非常短的延迟转发到出口端口。当

**第 10 章：Ack/Nak 协议**

TLP 的其余部分到达交换机时，没有错误，因此将 Ack 返回给 TLP 源，然后该 TLP 源从其重放缓冲区中清除该 TLP。这一次交换机出口端口将 TLP 的副本保留在其重放缓冲区中。当 TLP 到达目标时，报文没有错误，端点返回 Ack。基于此，交换机从其重放缓冲区中清除
TLP 的副本，序列完成。

_图 10-16：显示错误处理的交换机直通模式_

**==> 图片 [378 x 107] 已省略 <==**

**----- 图片文字开始 -----**<br>
Error occurs<br>1) 2) 4)<br>END TLP STP END TLP STP EDB TLP STP<br>EDB TLP STP<br>Switch Endpoint<br>5) Discard Packet<br>NAK 6) No ACK or
NAK<br>3)<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **More Examples** 

In the classroom setting examples often make it much easier to grasp the Ack/ Nak process and so some of them are presented here to
illustrate special cases.

</td>
<td width="50%">

## 第四部分：

# 物理层

</td>
</tr>
<tr>
<td width="50%">

## **Lost TLPs** 

Consider Figure 10‐13 on page 346, showing how a lost TLP is detected and handled. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B successfully receives TLP 4094 so it starts its AckNak_LATENCY_TIMER and increments its NEXT_RCV_SEQ count. After that, it also
receives TLPs 4095 and 0.

</td>
<td width="50%">

## _**11 物理层 - 逻辑 (Gen1 和 Gen2)**_

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

3. After receiving TLP 0, the AckNak_LATENCY_TIMER expires which causes it to schedule an Ack with Sequence Number of 0. 

4. Seeing Ack 0, Device A purges TLPs 4094, 4095, and 0 from its replay buffer. 

5. TLP 1 is lost en route for some reason (maybe the Physical Layer dropped it), and TLP 2 arrives instead. The Sequence Number check shows
Device B that TLP 2’s Sequence Number is not equal to the NEXT_RCV_SEQ count but is in the out of sequence range.

6. Device B discards TLP 2 and sets the NAK_SCHEDULED flag which will send a Nak 0 (NEXT_RCV_SEQ count ‐ 1) in this case. 

7. Upon receipt of Nak 0, Device A replays TLPs 1 and 2. It would purge TLP 0 and any earlier ones in the Replay Buffer, but they were
removed earlier so that becomes unnecessary.

8. TLPs 1 and 2 arrive without error at Device B and are forwarded to the Transaction Layer. 

_Figure 10‐13: Handling Lost TLPs_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>


**Cha ter 10: Ack/Nak Protocol p**

</td>
<td width="50%">

## **上一章**

上一章描述了 Ack/Nak 协议：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。Ack DLLP 确认 TLP 的良好接收，而 Nak DLLP 指示传输错误。本章描述了正常操作规则以及错误恢复机制。

</td>
</tr>
<tr>
<td width="50%">

## **Bad Ack** 

Figure 10‐14 on page 347 which shows the protocol for handling a corrupt Ack. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B receives TLPs 4094, 4095, and 0, sets NEXT_RCV_SEQ to 1, and returns Ack 0 because the AckNak_LATENCY_TIMER had expired. 

3. Ack 0 has a bit during its flight on the Link, so when Device A checks its 16‐ bit CRC, it fails the check and is discarded. This means
TLPs 4094, 4095, and 0 remain in Device A’s Replay Buffer.

4. TLPs 1 and 2 arrive at Device B and are good, so NEXT_RCV_SEQ count increments to 3 and Ack 2 is returned once the AckNak_LATENCY_TIMER
expires again.

5. Ack 2 arrives safely at Device A, which purges its Replay Buffer of TLPs 4094, 4095, 0, 1, and 2. 

If Ack 2 is also lost or corrupted and no further Ack or Nak DLLPs are returned to Device A, its REPLAY_TIMER expires causing a replay of
its entire buffer. Device B sees TLPs 4094, 4095, 0, 1 and 2 and considers them to be duplicates [their sequence numbers are earlier than
NEXT_RCV_SEQ count (3)]. They are discarded and _another_ Ack 2 would be returned to Device A because of the duplicate packets.

_Figure 10‐14: Handling Bad Ack_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **本章**

本章描述物理层的逻辑子块。它准备用于串行传输和恢复的报文。完成此操作需要几个步骤，我们将在此详细描述。本章涵盖了使用 8b/10b 编码的 Gen1 和 Gen2 协议相关联的逻辑。Gen3 的逻辑不使用 8b/10b 编码，将在名为"物理层 - 逻辑 (Gen3)"的第 407
页的章节中单独描述。

</td>
</tr>
<tr>
<td width="50%">

## **Bad Nak** 

Figure 10‐15 on page 349 which shows protocol for handling a corrupt Nak. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B receives TLPs 4094, 4095, and 0 all successfully (and the AckNak_LATENCY_TIMER has not yet expired). The next TLP that it
receives fails the LCRC check, so Device B sets the NAK_SCHEDULED flag, and resets and holds the AckNak_LATENCY_TIMER. The Nak is transmit‐
ted back with a Sequence Number of the last good TLP received, 0.

3. Nak 0 fails the 16‐bit CRC check at Device A and is discarded. 

4. At this point, Device B will not be sending anymore Acks or Naks until it successfully receives the next TLP it is expecting, TLP 1 in
this example. However, this will require a replay. Device A does not yet know that a replay is required because the one Nak that was sent
back was corrupted and discarded. This gets resolved by the REPLAY_TIMER. The REPLAY_TIMER will eventually expire because it has not seen an
Ack or Nak that makes forward progress in the specified time frame.

5. Once the REPLAY_TIMER expires, Device A will replay all TLPs in the Replay Buffer, increment REPLAY_NUM count and reset and restart the
REPLAY_TIMER.

6. Device B will receive TLPs 4094, 4095 and 0 and recognize that they are duplicates. The duplicate TLPs will be dropped and an Ack will be
sched‐ uled with a Sequence Number 0 (indicating the furthest progress made).

7. Once TLP 1 is successfully received by Device B, it will clear the NAK_SCHEDULED flag, increment the NEXT_RCV_SEQ and restart the
AckNak_LATENCY_TIMER because it has successfully received a TLP that it has not yet acknowledged.

**Cha ter 10: Ack/Nak Protocol p**

</td>
<td width="50%">

## **下一章**

下一章描述了第三代 (Gen3) PCIe 的物理层特性。主要变化包括无需将频率加倍即可将带宽相对于 Gen2 加倍的能力，这是通过消除对 8b/10b 编码的需求来实现的。在 Gen3 速度下需要更强大的信号补偿。进行这些更改比预期的要复杂得多。

</td>
</tr>
<tr>
<td width="50%">

## _Figure 10‐15: Handling Bad Nak_ 

<img src="figures/page/page0361.png" alt="Figure from page 361" width="700">

<br>

</td>
<td width="50%">

## **物理层概述**

本物理层概述介绍了 Gen1、Gen2 和 Gen3 实现之间的关系。此后，重点是与 Gen1 和 Gen2 相关联的逻辑物理层实现。Gen3 的逻辑物理层实现将在下一章中描述。

物理层位于外部物理链路和数据链路层之间接口的底部。它将来自数据链路层的出站报文转换为串行比特流，并在链路的所有 Lane 上计时输出。此层还从链路的所有 Lane 恢复接收端的比特流。接收逻辑将比特反序列化为符号流，重新组装报文，并将 TLP 和 DLLP 转发到数据链路层。

_图 11-1：PCIe 端口层_

**==> 图片 [307 x 307] 已省略 <==**

**----- 图片文字开始 -----**<br>
Software layer sends and receives address and transaction information<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet
(TLP) Transaction Layer Packet (TLP)<br>Header Data Payload ECRC Header Data Payload ECRC<br>Transaction layer<br>Flow Control<br>Transmit
Receive<br>Virtual Channel<br>Buffers Buffers<br>Management<br>per VC per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link
Packet<br>Sequence TLP LCRC Ack/Nak CRC Ack/Nak CRC Sequence TLP LCRC<br>Data Link layer TLP Retry De-mux<br>Buffer<br>TLP Error<br>Mux
Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode
Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**-----
图片文字结束 -----**<br>


**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

层的内容是概念性的，不定义精确的逻辑块，但就设计人员将它们划分为与规范匹配的逻辑块而言，由于数据速率的不断提高对物理层的影响比对其他层更大，因此它们的实现可以受益。按分层职责划分设计允许物理层适应更高的时钟速率，同时在其他层中尽可能少地进行更改。

PCIe 规范的 3.0 版本未使用特定术语来区分规范的各个版本所定义的不同传输速率。考虑到这一点，在本书中定义并使用以下术语。

- **Gen1** — PCIe 的第一代（1.x 版本），工作速率为 2.5 GT/s

- **Gen2** — 第二代（2.x 版本），工作速率为 5.0 GT/s

- **Gen3** — 第三代（3.x 版本），工作速率为 8.0 GT/s

物理层由两个子块组成：逻辑部分和电气部分，如图 11-2 所示。两者都包含独立的发送和接收逻辑，允许双单工通信。

_图 11-2：物理层的逻辑和电子子块_

**==> 图片 [366 x 241] 已省略 <==**

**----- 图片文字开始 -----**<br>
Physical Layer Physical Layer<br>Tx Rx Tx Rx<br>Logical Logical<br>Tx Rx Tx Rx<br>Electrical Electrical<br>Link<br>Tx+ Tx- Rx+ Rx- CTX Tx-
Tx+ Rx- Rx+<br>CTX<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **Error Situations Handled by Ack/Nak** 

The Ack/Nak protocol guarantees reliable delivery of TLPs despite several pos‐ sible errors. The list of errors below includes the
correction mechanism used to resolve them.

- **LCRC error** in a TLP. **Solution** : Receiver detects LCRC error and schedules a Nak that contains the NEXT_RCV_SEQ count ‐ 1. In
response, the trans‐ mitter replays at least one TLP, starting with the one that failed.

- **TLPs lost** en route to the receiver’s Data Link Layer ( _e.g._ Physical Layer detects issue with packet and drops it). **Solution** :
The receiver checks the Sequence Number on all received TLPs, expecting them to arrive with the next sequential Sequence Number. If a TLP is
lost, the Sequence Number of the next one that succeeds will be out of sequence. In response, the Receiver

 - schedules a Nak with NRS count ‐ 1, and the transmitter replays at least one TLP, starting with the missing one. 

- **Corrupted Ack or Nak** en route to the transmitter. **Solution:** The Transmit‐ ter detects a CRC error in the DLLP (see “Receiver
handling of DLLPs” on page 309), discards the packet and simply waits for the next one.

 - **Ack Case:** A subsequent Ack received with a later Sequence Number causes the transmitter Replay Buffer to purge all TLPs with Sequence
Numbers equal to or earlier than it. The transmitter is unaware that anything was wrong (except for a potential case of the Replay Buffer
temporarily filling up).

 - **Nak Case:** The receiver, having set the Nak Scheduled flag, will not send another Nak or any Acks until it successfully receives the
next expected TLP, meaning a replay is needed. Of course, the transmitter doesn’t know it needs to replay if the Nak was lost. In this case,
the REPLAY_TIMER will eventually expire and trigger the replay.

- **No Ack/Nak seen** within the expected time. **Solution** : REPLAY_TIMER timeout triggers a replay. 

- **Receiver fails to send Ack/Nak** for a received TLP. **Solution** : Again, the transmitter’s REPLAY_TIMER will expire and result in a
replay.

</td>
<td width="50%">

## **观察**

规范描述了物理层的功能，但故意对实现细节含糊其辞。显然，规范编写者不愿提供细节或示例实现，因为他们希望为各个供应商留出空间，以通过巧妙或创造性的逻辑版本增加价值。但对于我们的讨论来说，示例是必不可少的，选择了一个示例来说明这些概念。重要的是要明确指出，本示例尚未经过测试或验证，也不应认为设计人员必须以这种方式实现物理层。

</td>
</tr>
<tr>
<td width="50%">

## **Recommended Priority To Schedule Packets** 

A device may have many types of TLPs, DLLPs and Ordered Sets to transmit on a given Link. The recommended priority for scheduling packets
is:

1. Completion of any TLP or DLLP currently in progress (highest priority) 2. Ordered Set 

3. Nak 

4. Ack 

5. Flow Control 

6. Replay Buffer re‐transmissions 

7. TLPs that are waiting in the Transaction Layer 

8. All other DLLP transmissions (lowest priority)

</td>
<td width="50%">

## **发送逻辑概述**

为简单起见，让我们从该层发送方的高级概述开始，如图 11-3（第 365 页）所示。从顶部开始，我们可以看到从数据链路层输入的报文字节首先进入缓冲区。此处设置缓冲区是有意义的，因为有时必须延迟来自数据链路层的报文流，以允许有序集报文和其他项目注入到字节流中。

对于 Gen1 和 Gen2 操作，这些注入项是用于标记报文边界和创建有序集的控制字符和数据字符。为了区分这两种类型的字符，添加了一个 D/K# 位（数据或"Kontrol"）。该逻辑可以根据字符源查看 D/K# 应采用什么值。

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

Gen3 操作模式不使用控制字符，因此使用数据模式来构成识别传输字节是否与 TLP/DLLP 或有序集相关联的有序集。在 128 位（16 字节）数据块的开头插入一个 2 位同步头 (Sync Header)。同步头通知接收方接收到的块是数据块（TLP 或 DLLP
相关字节）还是有序集块。由于 Gen3 模式下没有控制字符，因此不需要 D/K# 位。

_图 11-3：物理层发送详细信息_

**==> 图片 [252 x 355] 已省略 <==**

**----- 图片文字开始 -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters
Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Gen3 Scrambler Lane 1, ... ,N-1 Gen3
Scrambler<br>Scrambler Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>8 10 Tx Clk 8 10<br>Mux
Mux<br>Gen3 Sync<br>Serializer Bits Generator Serializer<br>Mux Mux<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- 图片文字结束 -----**<br>


接下来，来自上层的并行数据字节被发送到字节交叉 (Byte Striping) 逻辑，在此处它们被分布或交叉到该链路的所有 Lane 上。每个报文的一个字节通过一个 Lane 传输，并且所有活动 Lane 都用于发送的每个报文。链路的所有 Lane
同时传输，因此字节必须足够快地进入此逻辑以适应这种情况。例如，如果有八个 Lane，则来自上层的八个并行字节可以到达字节交叉逻辑，从而允许数据同时被时钟输出到所有 Lane。

</td>
</tr>
<tr>
<td width="50%">

## **Timing Differences for Newer Spec Versions** 

As mentioned earlier, the timer values for the Ack/Nak protocol are different for Gen2 and later versions of the spec. To improve
readability of the text, only the Gen1 versions (2.5 GT/s rate) were included in the earlier discussion, but all three versions are included
here for convenience.

**Cha ter 10: Ack/Nak Protocol p** 

As before, the values given are in symbol times, so the actual time is that value multiplied by the time needed to deliver one symbol over
the Link at that rate. For review, the time to transmit one symbol (known as a Symbol Time) is 4ns for Gen1, 2ns for Gen2, and 1.25ns to
transmit 1 byte for Gen3.

</td>
<td width="50%">

## **PCI Exress Technology**

接下来是加扰器 (Scrambler)，它将伪随机模式与传出数据字节进行 XOR
运算以混合位。尽管这看起来可能会引入问题，但实际上并不会，因为加扰模式是可预测的，并非真正的随机，因此接收方可以使用相同的算法轻松恢复原始数据。如果加扰器失去同步，则接收方将无法理解比特流，因此，为了防止出现此问题，会定期重置加扰器（Gen1 和
Gen2）。这样，如果加扰器确实彼此失去同步，则无需很长时间即可重新初始化并重新同步。对于 Gen1 和 Gen2 模式，每当检测到 COM 字符时就会发生重新初始化。对于 Gen3 模式，每当看到 EIEOS 有序集时就会发生重新初始化。在 Gen3 模式中使用更复杂的 24
位加扰器，因此如图 11-3（第 365 页）所示存在通过 Gen3 加扰器的替代路径。

对于 Gen1 和 Gen2 模式，加扰后的 8 位字符然后由 8b/10b 编码器编码以进行传输。请记住，字符是未编码的 8 位字节，而符号是 8b/10b 逻辑的 10 位编码输出。8b/10b 编码有几个优点，但它确实会增加开销。

对于 Gen3，显示了一条绕过编码器的单独路径。换句话说，报文的加扰字节在没有 8b/10b 编码的情况下被传输。同步位生成器在每个 16 字节报文块之前添加一个 2 位同步头。添加的 2 位同步头将以下 16 字节块标识为数据块或有序集块。每 16 字节（128 位）添加 2
位同步头是 Gen3 的 128b/130b 编码方案的基础。

最后，符号被序列化为比特流，并转发到物理层的电子子块，然后传输到链路的另一端。

</td>
</tr>
<tr>
<td width="50%">

## **Ack Transmission Latency (AckNak Latency)** 

One interesting difference between the spec versions is the way the L0s recov‐ ery time is considered. In the 1.x specs, an argument is
included in the AckNak_LATENCY_TIMER equation to account for this, but the tables in the spec based on that equation put its value at zero
and call the resulting values ‘unadjusted’. Beginning with the 2.0 spec, the L0s recovery value is dropped from the equation altogether and
the text states that the receiver is not required to adjust Ack scheduling based on L0s exit latency or the value of the Extended Sync bit.
None of the table values contain an L0s recovery component and are therefore all still called ‘unadjusted’.

Note that, since the AF (Ack Factor) values are the same in all the tables and were shown in the earlier presentation of the Gen1 table,
they’re not included in the tables here.

Also, as it was for Gen1, the tolerance for all of the table values is ‐0% to +100%. To illustrate this, Table 10‐3 on page 351 lists the
time for a x1 Link and Max Payload size of 128 Bytes as 237 symbol times. Legal values would therefore range from no less than 237 symbol
times to no more than 474.

</td>
<td width="50%">

## **接收逻辑概述**

图 11-4（第 367 页）显示了组成接收方逻辑的关键元素。下面描述的过程是对每个 Lane 执行的。这次从底部开始，首先要提及的是接收方时钟和数据恢复
(CDR)。此过程的第一步是基于传入比特流中的跳变来恢复时钟。该恢复的时钟忠实地再现发送方用于发送数据的时钟，并用于将传入的比特锁存到反序列化缓冲区中。

CDR 过程的下一步是找到 Gen1/Gen2 符号边界，并将恢复的时钟除以 10 以将 10 位符号锁存到弹性缓冲区中。对于 Gen3，下一步是获取块锁定 (Block Lock)，然后将与块中 16 个字节中的每一个关联的 8 位符号锁存到弹性缓冲区中 —
在下一章中会有更多内容。

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

控制弹性缓冲区的逻辑通过在检测到 SOS (SKP 有序集) 时根据需要添加或删除 SKP 符号来调整恢复的时钟与接收方的本地时钟之间的细微时钟变化。最后，接收方的本地时钟将每个符号移出弹性缓冲区。

_图 11-4：物理层接收逻辑详细信息_

**==> 图片 [262 x 336] 已省略 <==**

**----- 图片文字开始 -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K#
Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler
De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR
Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- 图片文字结束 -----**<br>


使用 8b/10b 解码器，Gen1/Gen2 符号被解码，从而将 10 位符号转换为 8 位字符。去扰器应用在发送方使用的相同加扰方法来恢复原始数据。最后，来自每个 Lane 的字节被取消交叉以形成字节流，该字节流将被转发到数据链路层。只有 TLP 和 DLLP
被加载到接收缓冲区并发送到数据链路层。

</td>
</tr>
<tr>
<td width="50%">

## **2.5 GT/s Operation** 

_Table 10‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|237|128|73|67|58|48|33|
|256 Bytes|416|217|118|107|90|72|45|
|512 Bytes|559|289|154|86|109|86|52|
|1024 Bytes|1071|545|282|150|194|150|84|
|2048 Bytes|2095|1057|538|278|365|278|148|

</td>
<td width="50%">

## **发送逻辑详细信息 (仅 Gen1 和 Gen2)**

本节提供了与上一节中确定的步骤相关的更多详细信息。在本讨论期间，请参考第 369 页的图 11-5 中的框图。

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

_Table 10‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|4096 Bytes|4143|2081|1050|534|706|534|276|

</td>
<td width="50%">

## **Tx 缓冲区**

再次从图顶部开始，缓冲区接受来自数据链路层的 TLP 和 DLLP，以及指定新报文何时开始的"控制"信息。如前所述，该缓冲区允许我们不时停止字符流，以便插入控制字符和有序集。还显示了一个"节流 (throttle)"信号传回数据链路层，以便在缓冲区变满时停止字符流。

</td>
</tr>
<tr>
<td width="50%">

## **5.0 GT/s Operation** 

_Table 10‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|288|179|124|118|109|99|84|
|256 Bytes|467|268|169|158|141|123|96|
|512 Bytes|610|340|205|137|160|137|103|
|1024 Bytes|1122|596|333|201|245|201|135|
|2048 Bytes|2146|1108|589|329|416|329|199|
|4096 Bytes|4194|2132|1101|585|757|585|327|

</td>
<td width="50%">

## **Mux 和控制逻辑**

多路复用器（如图 11-6（第 370 页）所示）用于将特殊控制 (K) 字符插入来自缓冲区的数据流中。只有物理层使用 K 控制字符；它们在传输期间被插入并在接收方被删除。多路复用器的四个不同输入是：

- **发送数据缓冲区**。当数据链路层提供报文时，多路复用器会通过字符流。来自缓冲区的所有字符都是 D 字符，因此在 Tx 缓冲区内容被门控时，D/K# 信号被驱动为高电平。

- **起始和结束字符**。这些控制字符被添加到每个 TLP 和 DLLP 的开始和结束（参见第 371 页的图 11-7），并允许接收方轻松检测报文的边界。有两个起始字符：STP 指示 TLP 的开始，而 SDP 指示 DLLP
的开始。来自数据链路层的指示器连同报文类型一起确定要插入的成帧字符类型。还有两个结束字符，正常传输的结束良好 (END) 字符，以及处理某些错误情况的结束错误 (EDB) 字符。起始和结束字符是 K 字符，因此在插入起始和结束字符时，D/K#
信号被驱动为低电平（有关控制字符列表，请参见第 386 页的表 11-1）。

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-5：物理层发送逻辑详细信息 (仅 Gen1 和 Gen2)_

**==> 图片 [190 x 285] 已省略 <==**

**----- 图片文字开始 -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters
Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Scrambler Lane 1, ... ,N-1 Scrambler<br>8 8<br>D/K#
Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane
N<br>**----- 图片文字结束 -----**<br>


- **有序集**。如前所述，控制字符仅由物理层使用，上层看不到。跨链路的一些通信是必要的，用于发起和维护链路操作，这是通过交换有序集来完成的。每个有序集以称为逗号 (COM) 的 K 字符开头，并根据所传递的有序集类型包含其他 K 或 D
字符。有序集始终在四字节边界上对齐，并在各种情况下进行传输，包括：

 - 错误恢复、发起事件（例如热复位）或退出低功耗状态。在这些情况下，训练序列 1 和 2 (TS1 和 TS2) 有序集通过链路进行交换。

 - 在周期性间隔，多路复用器插入 SKIP 有序集模式，以促进接收方的时钟容限补偿。有关此过程的详细描述，请参考第 391 页的"时钟补偿"。

</td>
</tr>
<tr>
<td width="50%">

## **8.0 GT/s Operation** 

_Table 10‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|333|224|169|163|154|144|129|
|256 Bytes|512|313|214|203|186|168|141|
|512 Bytes|655|385|250|182|205|182|148|
|1024 Bytes|1167|641|378|246|290|246|180|
|2048 Bytes|2191|1153|634|374|461|374|244|
|4096 Bytes|4239|2177|1146|630|802|630|372|


**Cha ter 10: Ack/Nak Protocol p**

</td>
<td width="50%">

## **PCI Exress Technology**

- 当设备希望将其发送方置于电子空闲状态时，必须通知链路另一端的远程接收方。多路复用器会插入一个**电子空闲有序集**来完成此操作。

- 当设备希望将链路电源状态从 L0s 低功耗状态更改为 L0 全功率状态时，它会将一组**快速训练序列 (Fast Training Sequence, FTS)** 有序集发送到接收方。接收方使用此有序集将其 PLL 重新同步到发送方时钟。

- **逻辑空闲序列。**当没有准备发送的报文且没有要发送的有序集时，链路在逻辑上处于空闲状态。为了使接收方 PLL 锁定到发送方的频率，重要的是发送方继续发送某些内容，因此在该情况下插入逻辑空闲字符。逻辑空闲非常简单，仅由一串数据 00h 字符组成。

_图 11-6：发送逻辑多路复用器_

**==> 图片 [380 x 260] 已省略 <==**

**----- 图片文字开始 -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle<br>N*8<br>Tx<br>Buffer Control/ Ordered<br>CharactersToken LogicalIdle
Sets<br>N*8<br>N*8 8 8 8 N*8 Ordered Sets:<br>Mux Tx TS1, TS2,<br>Buffer<br>N*8 D/K# STP, SDP SKIP Logical<br>END, EDB Electrical Idle
Idle<br>Lane 0 Byte Striping Lane N<br>N*8<br>8 D/K# 8 D/K#<br>D K K/D D<br>Scrambler Lane 1, ... ,N-1 Scrambler Mux<br>8 8<br>D/K# Tx Local
D/K# N*8 D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane N<br>Lane 1, ...
,N-1<br>**----- 图片文字结束 -----**<br>


**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-7：使用起始和结束控制字符的 TLP 和 DLLP 报文成帧_

**==> 图片 [289 x 161] 已省略 <==**

**----- 图片文字开始 -----**<br>

</td>
</tr>
<tr>
<td width="50%">

## **Replay Timer** 

Much like the AckNak Latency Timer calculation, L0s recovery time is consid‐ ered differently for the Replay Timer in newer spec versions.
In the 1.x specs, an argument is included in the Replay Timer equation to account for this, but the tables in the spec based on that
equation put its value at zero and call the result‐ ing values ‘unadjusted’. Beginning with the 2.0 spec, the argument is dropped from the
equation altogether and the text states that the transmitter should com‐ pensate for L0s exit if it will be used, either by statically
adding that time to the table values or by sensing when the Link is in that state and allowing extra time in that case. The table values
still don’t contain an L0s component and are still called ‘unadjusted’.

As a final word on this topic, the spec strongly recommends that a transmitter should not do a replay on a Replay Timer timeout if it’s
possible that the delay in receiving an Ack was caused by the other device’s transmitter being in the L0s state.

Note that, just like for the Ack Latency Timer tables, the tolerance for all of the table values is ‐0% to +100%. To illustrate this, Table
10‐6 on page 353 lists the time for a x1 Link and Max Payload size of 128 Bytes as 711 symbol times. Legal values would therefore range from
no less than 711 symbol times to no more than 1422.

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **2.5 GT/s Operation** 

_Table 10‐6: Gen1 Unadjusted REPLAY_TIMER Values in Symbol Times_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|711|384|219|201|174|144|99|
|256 Bytes|1248|651|354|321|270|216|135|
|512 Bytes|1677|867|462|258|327|258|156|
|1024 Bytes|3213|1635|846|450|582|450|252|
|2048 Bytes|6285|3171|1614|834|1095|834|444|
|4096 Bytes|12429|6243|3150|1602|2118|1602|828|

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **5.0 GT/s Operation** 

_Table 10‐7: Gen2 Unadjusted REPLAY_TIMER Values in Symbol Times_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|864|537|372|354|327|297|252|
|256 Bytes|1401|804|507|474|423|369|288|
|512 Bytes|1830|1020|615|411|480|411|309|
|1024 Bytes|3366|1788|999|603|735|603|405|
|2048 Bytes|6438|3324|1767|987|1248|987|597|
|4096 Bytes|12582|6396|3303|1755|2271|1755|981|

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **8.0 GT/s Operation** 

_Table 10‐8: Gen3 Unadjusted REPLAY_TIMER Values_ 

|Max Payload|x1 Link|x2 Link|x4 Link|x8 Link|x12 Link|x16 Link|x32 Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|999|672|507|489|462|432|387|
|256 Bytes|1536|939|642|609|558|504|423|
|512 Bytes|1965|1155|750|546|615|546|444|
|1024 Bytes|3501|1923|1134|738|870|738|540|
|2048 Bytes|6573|3459|1902|1122|1383|1122|732|
|4096 Bytes|12717|6531|3438|1890|2406|1890|1116|


## **Switch Cut-Through Mode**

</td>
<td width="50%">

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
