# 📘 第 10 章　Ack/Nak 协议 (Chapter 10. Ack/Nak Protocol)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0271.md` ... `chunks/chunk0277.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Ack/Nak Protocol](#-本章目录-table-of-contents)

<a id="sec-10-1"></a>
## 10.1 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

There are several Link power states that allow power savings under certain con‐ ditions. These are L0s, L1, L2, and L3, which represent progressively lower power and also longer recovery time to get the link back to the fully‐operation state of L0. The L0s state can only be entered under hardware control, while L1 can be initiated by hardware or software. Since L0s and L1 can be controlled by hardware, they are referred to by the spec as ASPM (Active State Power Man‐ agement) states. For more on the details of link and device power management see the section “Active State Power Management (ASPM)” on page 735. 

## **Link Training and Initialization** 

As we’ve just briefly mentioned in this chapter, the Physical Layer is also responsible for initializing the link after a reset. However, this topic is too big to cover here and is instead covered in Chapter 14, entitled ʺLink Initialization & Training,ʺ on page 505. 

**405** 

**PCI Ex ress Technolo p gy** 

**406** 

## _**12**_ 

## _**Physical Layer ‐ Logical (Gen3)**_ 

## **The Previous Chapter** 

The previous chapter describes the Gen1/Gen2 logical sub‐block of the Physical Layer. This layer prepares packets for serial transmission and recovery, and the several steps needed to accomplish this are described in detail. The chapter cov‐ ers logic associated with the Gen1 and Gen2 protocol that use 8b/10b encoding/ decoding. 

## **This Chapter** 

This chapter describes the logical Physical Layer characteristics for the third generation (Gen3) of PCIe. The major change includes the ability to double the bandwidth relative to Gen2 speed without needing to double the frequency (Link speed goes from 5 GT/s to 8 GT/s). This is accomplished by eliminating 8b/10b encoding when in Gen3 mode. More robust signal compensation is nec‐ essary at Gen3 speed. 

## **The Next Chapter** 

The next chapter describes the Physical Layer electrical interface to the Link. The need for signal equalization and the methods used to accomplish it are also discussed here. This chapter combines electrical transmitter and receiver char‐ acteristics for both Gen1, Gen2 and Gen3 speeds. 

## **Introduction to Gen3** 

Recall that when a PCIe Link enters training (i.e., after a reset) it always begins using Gen1 speed for backward compatibility. If higher speeds were advertised during the training, the Link will immediately transition to the Recovery state and attempt to change to the highest commonly‐supported speed. 

**407** 

## **PCI Ex ress Technolo p gy** 

The major motivation for upgrading the PCIe spec to Gen3 was to double the bandwidth, as shown in Table 12‐1 on page 408. The straightforward way to accomplish this would have been to simply double the signal frequency from 5 GT/s to 10 Gb/s, but doing that presented several problems: 

- Higher frequencies consume substantially more power, a condition exacer‐ bated by the need for sophisticated conditioning logic (equalization) to maintain signal integrity at the higher speeds. In fact, the power demand of this equalizing logic is mentioned in PCISIG literature as a big motivation for keeping the frequency as low as practical. 

- Some circuit board materials experience significant signal degradation at higher frequencies. This problem can be overcome with better materials and more design effort, but those add cost and development time. Since PCIe is intended to serve a wide variety of systems, the goal was that it should work well in inexpensive designs, too. 

- Similarly, allowing new designs to use the existing infrastructure (circuit boards and connectors, for example) minimizes board design effort and cost. Using higher frequencies makes that more difficult because trace lengths and other parameters must be adjusted to account for the new tim‐ ing, and that makes high frequencies less desirable. 

_Table 12‐1: PCI Express Aggregate Bandwidth for Various Link Widths_ 

|**Link Width**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 Bandwidth**<br>**(GB /s)**|0.5|1|2|4|6|8|16|
|**Gen2 Bandwidth**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 Bandwidth**<br>**(GB/s)**|2|4|8|16|24|32|64|



These considerations led to two significant changes to the Gen3 spec compared with the previous generations: a new encoding model and a more sophisticated signal equalization model. 

**408** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **New Encoding Model** 

The logical part of the Physical Layer replaced the 8b/10b encoding with a new 128b/130b encoding scheme. Of course, this meant departing from the well‐ understood 8b/10b model used in many serial designs. Designers were willing to take this step to recover the 20% transmission overhead imposed by the 8b/ 10b encoding. Using 128b/130b means the Lanes are now delivering 8 bits/byte instead of 10 bits, and that means an 8.0 GT/s data rate that doubles the band‐ width. This equates to a bandwidth of 1 GB/s in each direction. 

To illustrate the difference between these two encodings, first consider Figure 12‐1 that shows the general 8b/10b packet construction. The arrows highlight the Control (K) characters representing the framing Symbols for the 8b/10b packets. Receivers know what to expect by recognizing these control characters. See “8b/10b Encoding” on page 380 to review the benefits of this encoding scheme. 

_Figure 12‐1: 8b/10b Lane Encoding_ 

**==> picture [344 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
‘D’ Characters<br>STP Sequence Header Data Payload  ECRC LCRC END<br>‘D’ Characters<br>‘K’ Character ‘K’ Character<br>SDP DLLP Type Misc. CRC END<br>‘K’ Character ‘K’ Character<br>**----- End of picture text -----**<br>


By comparison, Figure 12‐2 on page 410 shows the 128b/130b encoding. This encoding does not affect bytes being transferred, instead the characters are grouped into blocks of 16 bytes with a 2‐bit Sync field at the beginning of each block. The 2‐bit Sync field specifies whether the block includes Data (10b) or Ordered Sets (01b). Consequently, the Sync field indicates to the receiver what kind of traffic to expect and when it will begin. Ordered sets are similar to the 8b/10b version in that they must be driven on all the Lanes simultaneously. That requires getting the Lanes properly synchronized and this is part of the training process (see “Achieving Block Alignment” on page 438). 

**409** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐2: 128b/130b Block Encoding_ 

**==> picture [354 x 50] intentionally omitted <==**

**----- Start of picture text -----**<br>
0    1 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7<br>Sync  Symbol 0 Symbol 1 Symbol 15<br>Field<br>**----- End of picture text -----**<br>


## **Sophisticated Signal Equalization** 

The second change is made to the electrical sub‐block of the Physical Layer and involves more sophisticated signal equalization both at the transmit side of the Link and optionally at the receiver. Gen1 and Gen2 implementations use a fixed Tx de‐emphasis to achieve good signal quality. However, increasing transmis‐ sion frequencies beyond 5 GT/s causes signal integrity problems to become more pronounced, requiring more transmitter and receiver compensation. This can be managed somewhat at the board level but the designers wanted to allow the external infrastructure to remain the same as much as possible, and instead placed the burden on the PHY transmitter and receiver circuits. For more details on signal conditioning, refer to “Solution for 8.0 GT/s ‐ Transmitter Equalization” on page 474. 

## **Encoding for 8.0 GT/s** 

As previously discussed, the Gen3 128b/130b encoding method uses Link‐wide packets and per‐Lane block encoding. This section provides additional details regarding the encoding. 

## **Lane-Level Encoding** 

To illustrate the use of Blocks, consider Figure 12‐3 on page 411, where a single‐ Lane Data Block is shown. At the beginning are the two Sync Header bits fol‐ lower by 16 bytes (128 bits) of information resulting in 130 transmitted bits. The Sync Header simply defines whether a Data block (10b) or an Ordered Set (01b) is being sent. You may have noticed the Data Block in Figure 12‐3 has a Sync Header value of 01 rather than the 10b value mentioned above. This is because the least significant bit of the Sync Header is sent first when transmitting the block across the link. Notice the symbols following the Sync Header are also sent with the least significant bit first. 

**410** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐3: Sync Header Data Block Example_ 

**==> picture [374 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 1 Symbol 15<br>(01)<br>128-bit Payload<br>Data Block<br>UI UI UI<br>0 2 10 122<br>= = = =<br>Time Time Time Time<br>**----- End of picture text -----**<br>


## **Block Alignment** 

Like previous implementations, Gen3 achieves Bit Lock first and then attempts to establish Block Alignment locking. This requires receivers to find the Sync Header that demarcates the Block boundary. Transmitters establish this bound‐ ary by sending recognizable EIEOS patterns consisting of alternating bytes of 00h and FFh, as shown in Figure 12‐4. Thus, the use of EIEOS has expanded from simply exiting Electrical Idle to also serving as the synchronizing mecha‐ nism that establishes Block Alignment. Note that the Sync Header bits immedi‐ ately precede and follow the EIEOS (not shown in the illustration). See “Achieving Block Alignment” on page 438 for details regarding this process. 

_Figure 12‐4: Gen3 Mode EIEOS Symbol Pattern_ 

**==> picture [89 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


**411** 

**PCI Ex ress Technolo p gy** 

## **Ordered Set Blocks** 

Ordered Sets have much the same meaning they did in Gen1 and Gen2. They are used to manage Lane protocol. When an Ordered Set Block is sent it must appear on all the Lanes at the same time and almost always consists of 16 bytes with one exception. The one exception to this size rule is the SOS (SKP Ordered Set) which can have SKP Symbols added or removed in groups of four by clock compensation logic (associated with a Link Repeater for example) and can therefore legally be 8, 12, 16, 20, or 24 bytes long. 

The basic format of the Ordered Set Block is similar to the Data Block, except that the Sync Header bits are reversed, as shown in Figure 12‐5 on page 412. 

_Figure 12‐5: Gen3 x1 Ordered Set Block Example_ 

**==> picture [347 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 0 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 1 Symbol 15<br>(10)<br>128-bit Payload<br>Ordered Set Block<br>UI UI UI<br>0 2 10 122<br>= = = =<br>Time Time Time Time<br>**----- End of picture text -----**<br>


The spec defines seven Ordered Sets for Gen3 (one additional Ordered Set over Gen1 and Gen2 PCIe). In most cases, their functionality is the same as it was for the previous generations. 

1. SOS ‐ Skip Ordered Set: used for clock compensation. See “Ordered Set Example ‐ SOS” on page 426 for more detail. 

2. EIOS ‐ Electrical Idle Ordered Set: used to enter Electrical Idle state 

3. EIEOS ‐ Electrical Idle Exit Ordered Set: used for two purposes now: — Electrical Idle Exit as before 

   - Block alignment indicator for 8.0 GT/s 

4. TS1 ‐ Training Sequence 1 Ordered Set 

5. TS2 ‐ Training Sequence 2 Ordered Set 

6. FTS ‐ Fast Training Sequence Ordered Set 

7. SDS ‐ Start of Data Stream Ordered Set: new ‐ see “Data Stream and Data Blocks” on page 413 for more 

**412**

</td>
<td style="background-color:#e8e8e8">

有几个链路电源状态允许在特定条件下节省功耗。这些状态是 L0s、L1、L2 和 L3，它们表示逐步降低的功耗以及将链路恢复到完全运行状态 L0 时所需的更长恢复时间。L0s 状态只能在硬件控制下进入，而 L1 可以由硬件或软件发起。由于 L0s 和 L1 可以由硬件控制，它们被规范称为 ASPM（Active State Power Management，活动状态电源管理）状态。有关链路和设备电源管理的更多详细信息，请参见第 735 页的"活动状态电源管理 (ASPM)"一节。

## **链路训练和初始化**

正如我们刚刚在本章中简要提到的，物理层还负责在复位后初始化链路。但是，这个主题太大，无法在此处涵盖，而是在第 505 页的第 14 章"链路初始化与训练"中介绍。

**405**

**PCI Express 技术**

**406**

## _**12**_

## _**物理层 - 逻辑 (Gen3)**_

## **上一章**

上一章描述了物理层的 Gen1/Gen2 逻辑子块。该层准备用于串行传输和恢复的数据包，并详细描述了完成此操作所需的几个步骤。该章涵盖了与 Gen1 和 Gen2 协议相关联的逻辑，这些协议使用 8b/10b 编码/解码。

## **本章**

本章描述了 PCIe 第三代（Gen3）的逻辑物理层特性。主要变化包括在不使频率翻倍的情况下将带宽相对于 Gen2 速率翻倍的能力（链路速率从 5 GT/s 增加到 8 GT/s）。这是通过在 Gen3 模式下消除 8b/10b 编码来实现的。在 Gen3 速率下需要更强的信号补偿。

## **下一章**

下一章描述了物理层与链路的电气接口。本章还讨论了对信号均衡的需求以及实现该均衡的方法。本章结合了 Gen1、Gen2 和 Gen3 速率的电气发送器和接收器特性。

## **Gen3 简介**

回想一下，当 PCIe 链路进入训练时（即，在复位之后），它始终从 Gen1 速率开始以保持向后兼容性。如果在训练期间通告了更高的速率，则链路将立即转换到 Recovery 状态，并尝试更改为双方共同支持的最高速率。

**407**

## **PCI Express 技术**

将 PCIe 规范升级到 Gen3 的主要动机是将带宽翻倍，如第 408 页的表 12‐1 所示。完成此操作的直接方法是将信号频率从 5 GT/s 简单地翻倍到 10 Gb/s，但这样做带来了几个问题：

- 更高的频率消耗更多的功率，由于在更高速度下保持信号完整性需要复杂的调理逻辑（均衡），这种情况会更加严重。事实上，PCISIG 文献中提到这种均衡逻辑的功耗是将频率保持在尽可能低的水平的一个重要动机。

- 某些电路板材料在更高频率下会出现严重的信号衰减。可以通过更好的材料和更多的设计工作来克服这个问题，但这些会增加成本和开发时间。由于 PCIe 旨在服务于各种系统，目标是它也应能在低成本设计中良好工作。

- 类似地，允许新设计使用现有的基础设施（例如电路板和连接器）可以最大程度地减少电路板设计工作量和成本。使用更高的频率会使这变得更加困难，因为必须调整走线长度和其他参数以适应新的时序，这使得高频不太受欢迎。

_表 12‐1：不同链路宽度的 PCI Express 总带宽_

|**链路宽度**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 带宽**<br>**(GB/s)**|0.5|1|2|4|6|8|16|
|**Gen2 带宽**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 带宽**<br>**(GB/s)**|2|4|8|16|24|32|64|



这些考虑导致了与前几代相比 Gen3 规范的两个重大变化：新的编码模型和更复杂的信号均衡模型。

**408**

**第 12 章：物理层 - 逻辑 (Gen3)**

## **新的编码模型**

物理层的逻辑部分用新的 128b/130b 编码方案取代了 8b/10b 编码。当然，这意味着要摆脱许多串行设计中使用的、人们已经很好理解的 8b/10b 模型。设计人员愿意采取这一步骤来回收 8b/10b 编码所造成的 20% 传输开销。使用 128b/130b 意味着 Lane 现在每个字节传递 8 位而不是 10 位，这意味着 8.0 GT/s 的数据速率将带宽翻倍。这相当于每个方向 1 GB/s 的带宽。

为了说明这两种编码之间的差异，首先考虑图 12-1，它显示了通用的 8b/10b 数据包构造。箭头突出显示了表示 8b/10b 数据包成帧符号的控制（K）字符。接收器通过识别这些控制字符知道会发生什么。请参阅第 380 页的"8b/10b 编码"以回顾此编码方案的优势。

_图 12‐1：8b/10b Lane 编码_

**==> picture [344 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
'D' Characters<br>STP Sequence Header Data Payload  ECRC LCRC END<br>
'D' Characters<br>
'K' Character 'K' Character<br>
SDP DLLP Type Misc. CRC END<br>
'K' Character 'K' Character<br>
**----- End of picture text -----**<br>


相比之下，第 410 页的图 12‐2 显示了 128b/130b 编码。此编码不影响正在传输的字节，而是将字符分组为 16 字节的块，每个块的开头有一个 2 位 Sync 字段。2 位 Sync 字段指定块是包含数据（10b）还是有序集（01b）。因此，Sync 字段向接收器指示期望的流量类型以及何时开始。有序集与 8b/10b 版本类似，因为它们必须在所有 Lane 上同时驱动。这要求正确同步 Lane，这是训练过程的一部分（请参见第 438 页的"实现块对齐"）。

**409**

**PCI Express 技术**

_图 12‐2：128b/130b 块编码_

**==> picture [354 x 50] intentionally omitted <==**

**----- Start of picture text -----**<br>
0    1 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7<br>
Sync  Symbol 0 Symbol 1 Symbol 15<br>
Field<br>
**----- End of picture text -----**<br>


## **复杂的信号均衡**

第二个更改是在物理层的电气子块中进行的，涉及在链路发送端以及可选地在接收端进行更复杂的信号均衡。Gen1 和 Gen2 实现使用固定的 Tx 去加重来实现良好的信号质量。然而，将传输频率提高到 5 GT/s 以上会导致信号完整性问题变得更加突出，需要更多的发送器和接收器补偿。这可以在电路板级别进行一些管理，但设计人员希望允许外部基础设施尽可能保持不变，而将负担放在 PHY 发送器和接收器电路上。有关信号调理的更多详细信息，请参阅第 474 页的"8.0 GT/s 解决方案 - 发送器均衡"。

## **8.0 GT/s 编码**

如前所述，Gen3 128b/130b 编码方法使用链路范围的数据包和按 Lane 的块编码。本节提供有关编码的其他详细信息。

## **Lane 级别编码**

为了说明块的使用，请考虑第 411 页的图 12‐3，其中显示了单 Lane 数据块。开头是两个 Sync Header 位，后跟 16 字节（128 位）信息，共产生 130 个传输位。Sync Header 仅定义正在发送的是数据块（10b）还是有序集（01b）。您可能已经注意到图 12‐3 中的数据块的 Sync Header 值为 01，而不是上面提到的 10b 值。这是因为当跨链路传输块时，Sync Header 的最低有效位首先发送。请注意，Sync Header 之后的符号也以最低有效位优先发送。

**410**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12‐3：Sync Header 数据块示例_

**==> picture [374 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync Symbol 0 Symbol 1 Symbol 15<br>
(01)<br>
128-bit Payload<br>
Data Block<br>
UI UI UI<br>
0 2 10 122<br>
= = = =<br>
Time Time Time Time<br>
**----- End of picture text -----**<br>


## **块对齐**

与之前的实现一样，Gen3 首先实现位锁定（Bit Lock），然后尝试建立块对齐（Block Alignment）锁定。这要求接收器找到作为块边界标记的 Sync Header。发送器通过发送由交替的 00h 和 FFh 字节组成的可识别的 EIEOS 模式来建立此边界，如图 12‐4 所示。因此，EIEOS 的使用已从仅仅退出电气空闲扩展为还可作为建立块对齐的同步机制。请注意，Sync Header 位紧接在 EIEOS 之前和之后（图中未显示）。有关此过程的详细信息，请参见第 438 页的"实现块对齐"。

_图 12‐4：Gen3 模式 EIEOS 符号模式_

**==> picture [89 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 00000000<br>
1 11111111<br>
2 00000000<br>
3 11111111<br>
4 00000000<br>
13 11111111<br>
14 00000000<br>
15 11111111<br>
**----- End of picture text -----**<br>


**411**

**PCI Express 技术**

## **有序集块**

有序集在 Gen1 和 Gen2 中的含义大致相同。它们用于管理 Lane 协议。当发送有序集块时，它必须同时出现在所有 Lane 上，并且几乎总是由 16 个字节组成，只有一个例外。此大小规则的一个例外是 SOS（SKP 有序集），它可以通过时钟补偿逻辑（例如与链路中继器相关联）以四个为一组添加或删除 SKP 符号，因此合法长度可以是 8、12、16、20 或 24 字节。

有序集块的基本格式与数据块类似，只是 Sync Header 位是相反的，如第 412 页的图 12‐5 所示。

_图 12‐5：Gen3 x1 有序集块示例_

**==> picture [347 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 0 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync Symbol 0 Symbol 1 Symbol 15<br>
(10)<br>
128-bit Payload<br>
Ordered Set Block<br>
UI UI UI<br>
0 2 10 122<br>
= = = =<br>
Time Time Time Time<br>
**----- End of picture text -----**<br>


规范为 Gen3 定义了七个有序集（比 Gen1 和 Gen2 PCIe 多一个有序集）。在大多数情况下，它们的功能与前几代相同。

1. SOS - Skip 有序集：用于时钟补偿。有关更多详细信息，请参见第 426 页的"有序集示例 - SOS"。

2. EIOS - Electrical Idle 有序集：用于进入电气空闲状态

3. EIEOS - Electrical Idle Exit 有序集：现在用于两个目的：— 电气空闲退出，如以前

   - 8.0 GT/s 的块对齐指示符

4. TS1 - Training Sequence 1 有序集

5. TS2 - Training Sequence 2 有序集

6. FTS - Fast Training Sequence 有序集

7. SDS - Start of Data Stream 有序集：新增 - 有关更多信息，请参见第 413 页的"数据流和数据块"

**412**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-2"></a>
## 10.2 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Chapter 12: Physical Layer - Logical (Gen3)** 

To give the reader an example of the Ordered Set structure, Figure 12‐6 shows the content of an FTS Ordered Set when running at 8.0 GT/s. An Ordered Set Block is only recognized as an Ordered Set by the Sync Header, and identified as an FTS type by the first Symbol in the Block. The right‐hand side of the figure lists the Ordered Set Identifiers (the first Symbol for each Ordered Set) that serve to identify the type of Ordered Set is being transmitted. 

_Figure 12‐6: Gen3 FTS Ordered Set Example_ 

|**8Bh**<br>**14**<br>**8Dh**<br>**13**<br>**80h**<br>**12**<br>**7Fh**<br>**11**<br>**88h**<br>**10**<br>**ECh**<br>**9**<br>**6Eh**<br>**8**<br>**25h**<br>**7**<br>**C9h**<br>**6**<br>**C6h**<br>**5**<br>**CCh**<br>**4**<br>**C7h**<br>**3**<br>**4Eh**<br>**2**<br>**8Eh**<br>**15**<br>**47h**<br>**1**<br>**55h**<br>**0**<br>**01b**<br>**Sync Header**<br>**Value**<br>**Symbol**<br>**FTS Ordered Set**|**8Bh**<br>**14**<br>**8Dh**<br>**13**<br>**80h**<br>**12**<br>**7Fh**<br>**11**<br>**88h**<br>**10**<br>**ECh**<br>**9**<br>**6Eh**<br>**8**<br>**25h**<br>**7**<br>**C9h**<br>**6**<br>**C6h**<br>**5**<br>**CCh**<br>**4**<br>**C7h**<br>**3**<br>**4Eh**<br>**2**<br>**8Eh**<br>**15**<br>**47h**<br>**1**<br>**55h**<br>**0**<br>**01b**<br>**Sync Header**<br>**Value**<br>**Symbol**<br>**FTS Ordered Set**|**AAh**<br>**SKP**<br>**2Dh**<br>**TS2**<br>**1Eh**<br>**TS1**<br>**E1**<br>**SDS**<br>**55h**<br>**FTS**<br>**66h**<br>**EIOS**<br>**00h**<br>**EIEOS**<br>**First Symbol**<br>**Ordered Set**<br>**Ordered Set Identifiers**|**AAh**<br>**SKP**<br>**2Dh**<br>**TS2**<br>**1Eh**<br>**TS1**<br>**E1**<br>**SDS**<br>**55h**<br>**FTS**<br>**66h**<br>**EIOS**<br>**00h**<br>**EIEOS**<br>**First Symbol**<br>**Ordered Set**<br>**Ordered Set Identifiers**|
|---|---|---|---|
|**Symbol**|**Value**|**Ordered Set**|**First Symbol**|
|**Sync Header**|**01b**|**EIEOS**|**00h**|
|**0**|**55h**|**EIOS**|**66h**|
|**1**|**47h**|**FTS**|**55h**|
|**2**|**4Eh**|**SDS**|**E1**|
|**3**|**C7h**|**TS1**|**1Eh**|
|**4**|**CCh**|**TS2**|**2Dh**|
|**5**|**C6h**|**SKP**|**AAh**|
|**6**|**C9h**|||
|**7**|**25h**|||
|**8**|**6Eh**|||
|**9**|**ECh**|||
|**10**|**88h**|||
|**11**|**7Fh**|||
|**12**|**80h**|||
|**13**|**8Dh**|||
|**14**|**8Bh**|||
|**15**|**8Eh**|||



## **Data Stream and Data Blocks** 

The Link enters a Data Stream by sending an SDS Ordered Set and transitioning to the L0 Link state. While in a Data Stream multiple Data Blocks are trans‐ ferred, until the Data Stream ends with an EDS Token (unless an error ends it early). An EDS Token always occupies the last four Symbols of the Data Block that precedes an Ordered Set. An exception is made for Skip Ordered Sets because they do not interrupt a Data Stream as long as certain conditions are 

**413** 

**PCI Ex ress Technolo p gy** 

met that are discussed later. A Data Stream is no longer in effect when the Link state transitions out of the L0 state to any other Link state, such as Recovery. For more on Link states, see “Link Training and Status State Machine (LTSSM)” on page 518. 

## **Data Block Frame Construction** 

Data Blocks comprise TLPs, DLLP, and Tokens that are used to deliver the infor‐ mation. Five types of Data structures (called Tokens) are also used within a Data Block. Each has patterns for easy detection by the receiver. Three of the token may be sent at the beginning of a block (i.e., immediately following a Sync Data Block). These include: 

- Start TLP (STP) — followed by a TLP 

- Start DLLP (SDP) — followed by a DLLP 

- Logical Idle (IDLA) — sent when there is no packet activity 

The remaining Tokens are delivered at the end of the Data Block: 

- End of Data Stream (EDS) — Precedes the transition to Ordered Sets 

- End Bad (EDB) — reports a nullified packet has been detected 

Figure 12‐7 provides an example of a Data Block consisting of a single lane TLP transmission. 

_Figure 12‐7: Gen3 x1 Frame Construction Example_ 

**==> picture [376 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Header and Data Payload (8 bytes, same as 2.0) LCRC (4 bytes, same as 2.0)<br>Symbol 15<br>Sequence Sequence<br>1111b LEN [3:0] LEN [10:4] Parity bit Number [11:8]Frame CRC [3:0] Number [7:0]<br>**----- End of picture text -----**<br>


**414** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

In summary, the contents of a given Data Block vary depending on the activity: 

- IDLs — when no packets are being delivered Data Blocks consist of nothing but IDL. (The spec designates IDL as one of the Tokens) 

- TLPs — One or more TLPs may be sent in a given Data Block depend‐ ing on the link width. 

- DLLPs — One or more DLLPs may be sent in a Data Block. 

- Combinations of the activity listed above may be delivered in a single Data Block 

## **Framing Tokens** 

The spec defines five Framing Tokens (or just “Tokens” for short) that are allowed to appear in a Data Block, and those are repeated for convenience here in Figure 12‐8 on page 417. The five Tokens are: 

**1. STP ‐ Start TLP** : Much like earlier version, but now includes dword count for the entire packet. 

**2. SDP ‐ Start DLLP** 

3. **EDB ‐ End Bad** : Used to nullify a TLP the way it was in earlier Gen1 and Gen2 designs, but now four EDB symbols in a row are sent. The END (End Good) symbol is done away now; if not explicitly marked as bad, the TLP will be assumed to be good. 

**4. EDS ‐ End of Data Stream** : Last dword of a Data Stream, indicating that at least one Ordered Set will follow. Curiously, the Data Stream may not actually be ended by this event. If the Ordered Set that follows it is an SOS and is immediately followed by another Data Block, the Data Stream continues. If the Ordered Set that follows the EDS is anything other than SOS, or if the SOS is not followed by a Data Block, the Data Stream ends. 

**5. IDL ‐ Logical Idle:** The Idle Token is simply data zero bytes sent during Link Logical Idle state when no TLPs or DLLPs are ready to transmit. 

The difference between the way the spec shows the Tokens and the way they’re presented in Figure 12‐8 on page 417 is that this drawing shows both bytes and bits in little‐endian order instead of the big‐endian bit representa‐ tion used in the spec. The reason it’s shown that way is to illustrate the order that the bits will actually appear on the Lane. 

## **Packets** 

The STP and SDP, indicate the start of a packet as shown in Figure 12‐7 

- **TLPs** . An **STP** Token consists of a nibble of 1’s followed by an 11‐bit dword‐ length field. The length counts all the dwords of the TLP, including the 

**415** 

## **PCI Ex ress Technolo p gy** 

Token, header, optional data payload, optional digest, and LCRC. That allows the receiver to count dwords to recognize where the TLP ends. Con‐ sequently, it’s very important to verify that the Length field doesn’t have an error, and so it has a 4‐bit Frame CRC, and an even parity bit that protects both the Length and Frame CRC fields. The combination of these bits pro‐ vides a robust triple‐bit‐flip detection capability for the Token (as many as 3 bits could be incorrect and it would still be recognized as an error). The 11‐ bit Length field allows for a TLP of 2K dwords (8KB) for the entire TLP. 

- **DLLPs** . The **SDP** Token indicates the beginning of a DLLP and doesn’t include a length field because it will always be exactly 8 bytes long: the 2‐ byte Token is followed by 4 bytes of DLLP payload and 2 bytes of DLLP LCRC. Perhaps coincidently, this DLLP length is the same as it was in ear‐ lier PCIe generations, but they also do not have an end good symbol. 

The **EDB** Token is added to the end of TLPs that are nullified. For a normal TLP, there is no “end good” indication; it’s assumed to be good unless explicitly marked as bad. If the TLP ends up being nullified, the LCRC value is inverted and an EDB Token is appended as an extension of the TLP, although it’s not included in the length value. Physical layer receivers must check for the EDB at the end of every TLP and inform the Link layer if they see one. Not surprisingly, receiving an EDB at any time other than immediately after a TLP will be consid‐ ered to be a Framing Error. 

**416** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## _Figure 12‐8: Gen3 Frame Token Examples_ 

**==> picture [368 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 STP<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 SDP<br>Symbol 0 Symbol 1<br>Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 EDS<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 EDB<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Tx<br>0 1 2 3 4 5 6 7 IDL<br>Symbol 0<br>0011 0101<br>1111 1000b 0000 0001b 0000 1001b 0000 0000b<br>0000 0011b 0000 0011b 0000 0011b 0000 0011b<br>0000 0000b<br>Sequence Sequence<br>1111b LEN [0:3] LEN [4:10] Frame Parity bitNumber [8:11]Frame CRC [0:3] Number [0:7]<br>0000b 1111b<br>**----- End of picture text -----**<br>


## **Transmitter Framing Requirements** 

To begin this discussion, it will be helpful first to define a couple of things. First, recall that a Data Stream starts with the first Symbol following an SDS and it may contain Data Blocks made up of Tokens, TLPs and DLLPs. The Data Stream finishes with the last Symbol before an Ordered Set other than SOS, or when a Framing Error is detected. During a Data Stream no Ordered Sets can be sent except for the SOS. 

Secondly, since framing problems will usually result in a Framing Error, it will help to explain what happens in that case. When Framing Errors occur, they are 

**417** 

## **PCI Ex ress Technolo p gy** 

considered Receiver Errors and will be reported as such. The Receiver stops processing the Data Stream in progress and will only process a new Data Stream when it sees an SDS Ordered Set. In response to the error, a recovery process is initiated by directing the LTSSM to the Recovery state from L0. The expectation is that this will be resolved in the Physical Layer and will not require any action by the upper layers. In addition, the spec states that the round‐trip time to accomplish this is expected to take less than 1  s from the time both Ports have entered Recovery. 

Now, with that background in place, let’s continue with the framing require‐ ments. While in a Data Stream, a transmitter must observe the following rules: 

- When sending a TLP: 

   - An STP Token must be immediately followed by the entire contents of the TLP as delivered from the Link Layer, even if it’s nullified. 

   - If the TLP was nullified, the EDB Token must appear immediately after the last dword of the TLP, but must not be included in the TLP length value. 

   - An STP cannot be sent more than once per Symbol Time on the Link. 

- When sending a DLLP: 

   - An SDP Token must be immediately followed by the entire contents of the DLLP as delivered from the Data Link Layer. 

   - 

      - An SDP cannot be sent more than once per Symbol Time on the Link. 

- When sending an SOS (SKP Ordered Set) within a Data Stream: 

   - Send an EDS Token in the last dword of the current Data Block. 

   - Send the SOS as the next Ordered Set Block. 

   - Send another Data Block immediately after the SOS. The Data Stream resumes with the first Symbol of this subsequent Data Block. 

   - If multiple SOS’s are scheduled, they can’t be back‐to‐back as they were in earlier generations. Instead, each one must be preceded by a Data Block that ends with the EDS Token. The Data block can be filled with TLPs, DLLPs or IDLs during this time.

</td>
<td style="background-color:#e8e8e8">

- 要结束数据流，在当前数据块的最后一个 dword 中发送 EDS 令牌，然后跟随 EIOS 以进入低功耗链路状态，或在所有其他情况下跟随 EIEOS。

- 如果链路上没有发送 TLP、DLLP 或其他成帧令牌，则必须在所有通道上发送 IDL 令牌。

- 对于多通道链路：

   - 在发送 IDL 令牌之后，下一个 TLP 或 DLLP 的第一个字符必须在开始时位于通道 0 中。EDS 令牌必须始终是数据块的最后一个 dword，因此可能不总是遵循该规则。

   - IDL 令牌必须用于在字符时间内填充原本为空的 dword。例如，如果 x8 链路有一个 TLP

**418**

**第 12 章：物理层 - 逻辑 (Gen3)**

在通道 3 中结束，但发送方没有另一个 TLP 或 DLLP 准备好在通道 4 中开始，则 IDL 必须填充剩余的字节，直到该字符时间结束。

- 由于数据包仍然是 4 字节的倍数，就像在早期代中一样，它们将以 4 通道边界开始和结束。例如，具有在通道 3 中结束的 DLLP 的 x8 链路可以通过将其 STP 令牌放在通道 4 中来启动下一个 TLP。

## **接收器成帧要求 (Receiver Framing Requirements)**

当接收器看到数据流时，适用以下规则：

- 当预期成帧令牌时，看起来像任何其他内容的字符将是成帧错误 (Framing Errors)。

- 下面列表中显示的某些错误检查和报告是可选的，并且规范指出它们彼此独立可选。

- 接收到 STP 时：

   - 接收器必须检查帧 CRC 和帧奇偶校验字段，任何不匹配将是成帧错误。（请注意，具有成帧错误的 STP 令牌在报告此错误时不视为 TLP 的一部分。）

   - 紧接 TLP 最后一个 DW 之后的字符是要处理的下一个令牌，并且接收器必须检查它是否是被作废的 TLP 的 EDB 令牌的开始。

   - 可选地检查长度值是否为零；如果检测到，则是成帧错误。

   - 可选地检查在同一字符时间内是否有超过一个 STP 令牌的到达。如果检查并检测到，则这是成帧错误。

- 接收到 EDB 时：

   - 接收器必须在检测到第一个 EDB 字符时，或在已接收到任何剩余字节之后，通知链路层。

   - 如果令牌中的任何字符不是 EDB，则结果是成帧错误。

   - EDB 令牌唯一合法的时间是在 TLP 之后；任何其他用途将是成帧错误。

   - 紧接 EDB 令牌之后的字符将是要处理的下一个令牌的第一个字符。

- 当作为数据块最后一个 DW 接收到 EDS 令牌时：

   - 接收器必须停止处理数据流。

   - 仅接受 SKP、EIOS 或 EIEOS 有序集合作为下一个；接收到任何其他有序集合将是成帧错误。

   - 如果在 EDS 之后接收到 SKP 有序集合，则接收器必须从跟随的数据块的第一个字符恢复数据流处理，除非检测到成帧错误。

**419**

## **PCI Ex ress Technolo p gy**

- 接收到 SDP 令牌时：

   - DLLP 之后的字符是要处理的下一个令牌。

   - 可选地检查同一字符时间内是否有超过一个 SDP 令牌。如果检查并发生这种情况，则是成帧错误。

- 接收到 IDL 令牌时：

   - 下一个令牌允许在 IDL 令牌之后的任何 DW 对齐通道上开始。对于 x4 或更窄的链路，这意味着下一个令牌只能在下一个字符时间的通道 0 中开始。对于更宽的链路，有更多的选项。例如，x16 链路可以在当前字符时间的通道 0、4、8 或 12 中开始下一个令牌。

   - 在同一字符时间内预期与 IDL 一起出现的唯一令牌将是另一个 IDL 或 EDS。

- 在处理数据流期间，接收器将看到以下内容作为成帧错误：

   - 紧接 SDS 之后的有序集合。

   - 具有非法 Sync Header（11b 或 00b）的块。这可以选择地在通道错误状态寄存器中报告。

   - 在任何通道上的有序集合块，在上一个块中未接收到 EDS 令牌。

   - 紧接上一个块中的 EDS 令牌之后的数据块。

   - 可选地，验证所有通道是否接收相同的有序集合。

## **从成帧错误中恢复 (Recovery from Framing Errors)**

如果在处理数据流时看到成帧错误，则接收器必须：

- 报告接收器错误（如果可选的高级错误报告寄存器可用，则设置第 421 页图 12-9 中显示的状态位）。

- 停止处理数据流。处理新的数据流可以在看到下一个 SDS 有序集合时开始。

- 启动错误恢复过程。如果链路处于 L0 状态，则将涉及转换到 Recovery 状态。规范说通过 Recovery 状态的时间"预期"小于 1 μs。

- 请注意，从成帧错误恢复不一定预期会直接导致通过 Ack/Nak 机制的数据链路层发起的恢复活动。当然，如果 TLP 因错误而丢失或损坏，则将需要重传事件。

**420**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12-9：AER 可纠正错误寄存器_

**==> 图片 [366 x 190] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 16 15 14 13 12 11 9 8 7 6 5 1 0<br>
RsvdZ RsvdZ RsvdZ<br>
Header Log Overflow Status<br>
Corrected Internal Error Status<br>
Advisory Non-Fatal Error Status<br>
Replay Timer Timeout Status<br>
REPLAY_NUM Rollover Status<br>
Bad DLLP Status<br>
Bad TLP Status<br>
Receiver Error Status<br>
注意：所有指定为 RW1CS 的位<br>
**----- 图片文字结束 -----**<br>


## **Gen3 物理层发送逻辑 (Gen3 Physical Layer Transmit Logic)**

第 422 页的图 12-10 说明了支持 Gen3 速度的物理层发送逻辑的概念框图。整体设计与 Gen2 非常相似，因此无需再次介绍所有细节，但存在一些差异。建议那些 PCIe 新手回顾第 361 页的早期章节"物理层 - 逻辑 (Gen1 和 Gen2)"，以了解物理层设计的基础。让我们从图的顶部开始，解释 Gen3 的变化。一如既往，重要的是要指出此实现仅用于教学目的，并非旨在显示实际的 Gen3 物理层实现。

## **多路复用器 (Multiplexer)**

TLP 和 DLLP 从数据链路层到达顶部。多路复用器混合构建完整 TLP 或 DLLP 所需的 STP 或 SDP 令牌。上一节描述了令牌格式。

**421**

## **PCI Ex ress Technolo p gy**

_图 12-12：Gen3 x8 示例：TLP 跨越块边界_

_图 12-10：Gen3 物理层发送器详细信息_

**==> 图片 [260 x 371] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
来自数据链路层<br>
数据包边界指示符<br>
Throttle N*8<br>
Tx<br>
缓冲区 控制/ 有序<br>
令牌 逻辑 集合<br>
字符 空闲<br>
N*8 8 8 8<br>
Mux<br>
N*8 D/K#<br>
通道 0 字节交错 通道 N<br>
8 D/K# 8 D/K#<br>
Gen3 加扰器 通道 1, ... ,N-1 Gen3 加扰器<br>
加扰器 加扰器<br>
8 8<br>
D/K# Tx 本地 D/K#<br>
PLL<br>
8b/10b 8b/10b<br>
编码器 编码器<br>
8 10 Tx 时钟 8 10<br>
Mux Mux<br>
Gen3 同步<br>
串行器 位生成器 串行器<br>
Mux Mux<br>
Tx Tx<br>
通道 0 通道 1, ... ,N-1 通道 N<br>
**----- 图片文字结束 -----**<br>


**422**

**第 12 章：物理层 - 逻辑 (Gen3)**

Gen3 TLP 边界由 TLP 数据包开头的 STP 令牌的 Length 字段中的 dword 计数定义，因此不需要 END 帧字符。

当结束数据流或仅在发送 SOS 之前，EDS 令牌被多路复用到数据流中。基于 Skip 计时器，SOS 由多路复用器定期插入数据流中。其他有序集合（如 TS1、TS2、FTS、EIEOS、EIOS、SDS）也可以根据链路需求进行多路复用，并且位于数据流之外。

数据包以块形式传输，由 2 位 Sync Header 标识。Sync Header 由多路复用器添加。但是，Sync Header 由字节交错逻辑在多通道链路的所有通道上复制。

当没有数据包或有序集合要发送但链路要保持在 L0 状态时，IDL（逻辑空闲或数据零）令牌用作填充。这些像其他数据字节一样被加扰，并由接收器识别为填充。

## **字节交错 (Byte Striping)**

此逻辑将要传递的字节分散到所有可用通道上。成帧规则在第 417 页的"发送器成帧要求 (Transmitter Framing Requirements)"中已经描述过，所以现在让我们看一些示例并讨论这些规则如何应用。

首先考虑第 424 页图 12-11 中所示的示例，其中说明了 4 通道链路。请注意，Sync Header 位在新块开始时同时出现在所有通道上，并定义块类型（本例中为数据块）。块编码为每个通道独立处理，但字节（或字符）像早期 PCIe 代一样交错分布在所有通道上。

**423**

**PCI Ex ress Technolo p gy**

_图 12-11：Gen3 字节交错 x4_

**==> 图片 [376 x 222] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
通道 0 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync 字符 0 字符 4 字符 60<br>
通道 1 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync 字符 1 字符 5 字符 61<br>
通道 2 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync 字符 2 字符 6 字符 62<br>
通道 3 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync 字符 3 字符 7 字符 63<br>
**----- 图片文字结束 -----**<br>


## **字节交错 x8 示例 (Byte Striping x8 Example)**

接下来，考虑第 425 页图 12-12 中所示的 x8 链路，这是从规范重绘以使其更易读的示例。这里的位流是垂直的而不是水平的。在顶部我们可以看到 Sync 位按小端序显示（按要求），同时出现在所有通道上，并指示数据块正在开始。

在此示例中，首先发送 TLP，因此字符 0-4 包含 STP 成帧令牌，其中包括整个 TLP 的 7 DW 长度（包括令牌）。接收器需要知道 TLP 的长度，因为对于 8 GT/s 速度，没有 END 控制字符。相反，接收器计算 dword，如果未观察到 EDB（End Bad），则假定 TLP 是好的。在这种情况下，TLP 在字符 3 的通道 3 处结束。

**424**

**第 12 章：物理层 - 逻辑 (Gen3)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-3"></a>
## 10.3 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- To end a Data Stream, send the EDS Token in the last dword of the current Data Block and follow that with either the EIOS to go into a low power Link state, or an EIEOS for all other cases. 

- The IDL Token must be sent on all Lanes if a TLP, DLLP, or other Framing Token is not being sent on the Link. 

- For multi‐Lane Links: 

   - After sending an IDL Token, the first Symbol of the next TLP or DLLP must be in Lane 0 when it starts. An EDS Token must always be the last dword of a Data Block and therefore may not always follow that rule. 

   - IDL Tokens must be used to fill in dwords during a Symbol Time that would otherwise be empty. For example, if a x8 Link has a TLP that 

**418** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

ends in Lane 3, but the sender doesn’t have another TLP or a DLLP ready to start in Lane 4, then IDLs must fill in the remaining bytes until the end of that Symbol Time. 

- Since packets are still multiples of 4 bytes as they were in the earlier generations, they’ll start and end on 4‐Lane boundaries. For example, a x8 Link with a DLLP that ends in Lane 3 could start the next TLP by placing its STP Token in Lane 4. 

## **Receiver Framing Requirements** 

When a Data Stream is seen at the Receiver, the following rules apply: 

- When Framing Tokens are expected, Symbols that look like anything else will be Framing Errors. 

- Some error checks and reports shown in the list below are optional, and the spec points out that they are independently optional. 

- When an STP is received: 

   - Receivers must check the Frame CRC and Frame Parity fields, and any mismatch will be a Framing Error. (Note that an STP Token with a Framing Error isn’t considered to be part of a TLP when reporting this error.). 

   - The Symbol immediately after the last DW of the TLP is the next Token to process, and Receivers must check to see whether it’s the start of an EDB Token showing that the TLP has been nullified. 

   - Optionally check for length value of zero; if detected, it’s a Framing Error. 

   - Optionally check for the arrival of more than one STP Token in the same Symbol Time. If checking and detected, this is a Framing Error. 

- When an EDB is received: 

   - Receiver must inform the Link Layer as soon as the first EDB Symbol is detected, or after any of the remaining bytes of it have been received. 

   - If any Symbols in the Token are not EDBs, the result is a Framing Error. 

   - The only legal time for an EDB Token is right after a TLP; any other use will be a Framing Error. 

   - The Symbol immediately following the EDB Token will be the first Symbol of the next Token to be processed. 

- When an EDS Token is received as the last DW of a Data Block: 

   - Receivers must stop processing the Data Stream. 

   - Only a SKP, EIOS, or EIEOS Ordered Set will be acceptable next; receiv‐ ing any other Ordered set will be a Framing Error. 

   - If a SKP Ordered Set is received after an EDS, Receivers must resume Data Stream processing with the first Symbol of the Data Block that fol‐ lows, unless a Framing Error was detected. 

**419** 

## **PCI Ex ress Technolo p gy** 

- When an SDP Token is received: 

   - The Symbol immediately after the DLLP is the next Token to be pro‐ cessed. 

   - Optionally check for more than one SDP Token in the same Symbol Time. If checking and this occurs, it is a Framing Error. 

- When an IDL Token is received: 

   - The next Token is allowed to begin on any DW‐aligned Lane following the IDL Token. For Links that are x4 or narrower, that means the next Token can only start in Lane 0 of the next Symbol Time. For wider Links there are more options. For example, a x16 Link could start the next Token in Lane 0, 4, 8, or 12 of the current Symbol Time. 

   - The only Token that would be expected in the same Symbol Time as an IDL would be another IDL or an EDS. 

- While processing a Data Stream, Receivers will see the following as Fram‐ ing Errors: 

   - 

   - An Ordered Set immediately following an SDS. 

- A Block with an illegal Sync Header (11b or 00b). This can optionally be reported in the Lane Error Status register. 

- An Ordered Set Block on any Lane without receiving an EDS Token in the previous Block. 

- A Data Block immediately following an EDS Token in the previous block. 

- 

- Optionally, verify that all Lanes receive the same Ordered Set. 

## **Recovery from Framing Errors** 

If a Framing Error is seen while processing a Data Stream, the Receiver must: 

- Report a Receiver Error (if the optional Advanced Error Reporting registers are available, set the status bit shown in Figure 12‐9 on page 421). 

- Stop processing the Data Stream. Processing a new Data Stream can begin when the next SDS Ordered Set is seen. 

- Initiate the error recovery process. If the Link is in the L0 state, that will involve a transition to the Recovery state. The spec says that the time through the Recovery state is “expected” to be less than 1  s. 

- Note that recovery from Framing Errors is not necessarily expected to directly cause Data Link Layer initiated recovery activity via the Ack/Nak mechanism. Of course, if a TLP is lost or corrupted as a result of the error, then a replay event will be needed. 

**420** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐9: AER Correctable Error Register_ 

**==> picture [366 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 14 13 12 11 9 8 7 6 5 1 0<br>RsvdZ RsvdZ RsvdZ<br>Header Log Overflow Status<br>Corrected Internal Error Status<br>Advisory Non-Fatal Error Status<br>Replay Timer Timeout Status<br>REPLAY_NUM Rollover Status<br>Bad DLLP Status<br>Bad TLP Status<br>Receiver Error Status<br>Note: all bits designated RW1CS<br>**----- End of picture text -----**<br>


## **Gen3 Physical Layer Transmit Logic** 

Figure 12‐10 on page 422 illustrates a conceptual block diagram of the Physical Layer transmit logic that supports Gen3 speeds. The overall design is very simi‐ lar to Gen2 so there’s no need to go through all the details again but there are some differences. Those who are new to PCIe are encouraged to review the ear‐ lier chapter called “Physical Layer ‐ Logical (Gen1 and Gen2)” on page 361 to learn the basics of the Physical Layer design. Let’s start at the top of the diagram and explain the changes for Gen3 along the way. As before, it’s important to point out that this implementation is only for instructional purposes and is not meant to show an actual Gen3 Physical Layer implementation. 

## **Multiplexer** 

TLPs and DLLPs arrive from the Data Link Layer at the top. The multiplexer mixes in the STP or SDP Tokens necessary to build a complete TLP or DLLP. The previous section described the Token formats. 

**421** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐10: Gen3 Physical Layer Transmitter Details_ 

**==> picture [260 x 371] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Gen3 Scrambler Lane 1, ... ,N-1 Gen3 Scrambler<br>Scrambler Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>8 10 Tx Clk 8 10<br>Mux Mux<br>Gen3 Sync<br>Serializer Bits Generator Serializer<br>Mux Mux<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- End of picture text -----**<br>


**422** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

Gen3 TLP boundaries are defined by the dword count in the Length field of the STP Token at the beginning of a TLP packet, therefore, no END frame character is needed. 

When ending a Data Stream or just before sending an SOS, the EDS Token in muxed into the Data Stream. At regular intervals, based on a Skip timer, an SOS is inserted into the Data Stream by the multiplexer. Other Ordered‐Sets such as TS1, TS2, FTS, EIEOS, EIOS, SDS may also be muxed based on Link require‐ ments and are outside the Data Stream. 

Packets are transmitted in Blocks which are identified by the 2‐bit Sync Header. The Sych Header is added by the multiplexer. However, the Sych Header is rep‐ licated on all Lanes of a multi‐Lane Link by the Byte Striping logic. 

When there are no packets or Ordered Sets to send but the Link is to remain active in L0 state, the IDL (Logical Idle, or data zero) Tokens are used as fillers. These are scrambled just like other data bytes and are recognized as filler by the Receiver. 

## **Byte Striping** 

This logic spreads the bytes to be delivered across all the available Lanes. The framing rules were described earlier in “Transmitter Framing Requirements” on page 417, so now let’s look at some examples and discuss how the rules apply. 

Consider first the example shown in Figure 12‐11 on page 424, where a 4‐Lane Link is illustrated. Notice that the Sync Header bits appear on all the Lanes at the same time when a new Block begins and define the block type (a Data Block in this example). Block encoding is handled independently for each Lane, but the bytes (or symbols) are striped across all the Lanes just as they were for the earlier generations of PCIe. 

**423** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐11: Gen3 Byte Striping x4_ 

**==> picture [376 x 222] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane 0 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 4 Symbol 60<br>Lane 1 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 1 Symbol 5 Symbol 61<br>Lane 2 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 2 Symbol 6 Symbol 62<br>Lane 3 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 3 Symbol 7 Symbol 63<br>**----- End of picture text -----**<br>


## **Byte Striping x8 Example** 

Next, consider the x8 Link shown in Figure 12‐12 on page 425, which is an example from the spec redrawn to make it easier to read. Here the bit stream is vertical instead of horizontal. At the top we can see that the Sync bits, shown in little‐endian order as required, appear on all Lanes simultaneously and indicate that a Data Block is starting. 

In this example, a TLP is sent first, so Symbols 0 ‐ 4 contain the STP framing Token, which includes a length of 7 DW for the entire TLP including the Token. The receiver needs to know the length of the TLP because for 8 GT/s speeds there is no END control character. Instead, the receiver counts the dwords and if there is no EDB (End Bad) observed, the TLP is assumed to be good. In this case, the TLP ends on Lane 3 of Symbol 3. 

**424** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_ 

|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|
|---|---|---|---|---|---|---|---|---|
||||||||||

</td>
<td style="background-color:#e8e8e8">

有几个链路电源状态允许在特定条件下节省功耗。这些状态是 L0s、L1、L2 和 L3，它们表示逐步降低的功耗以及将链路恢复到完全运行状态 L0 时所需的更长恢复时间。L0s 状态只能在硬件控制下进入，而 L1 可以由硬件或软件发起。由于 L0s 和 L1 可以由硬件控制，它们被规范称为 ASPM（Active State Power Management，活动状态电源管理）状态。有关链路和设备电源管理的更多详细信息，请参见第 735 页的"活动状态电源管理 (ASPM)"一节。

## **链路训练和初始化**

正如我们刚刚在本章中简要提到的，物理层还负责在复位后初始化链路。但是，这个主题太大，无法在此处涵盖，而是在第 505 页的第 14 章"链路初始化与训练"中介绍。

**405**

**PCI Express 技术**

**406**

## _**12**_

## _**物理层 - 逻辑 (Gen3)**_

## **上一章**

上一章描述了物理层的 Gen1/Gen2 逻辑子块。该层准备用于串行传输和恢复的数据包，并详细描述了完成此操作所需的几个步骤。该章涵盖了与 Gen1 和 Gen2 协议相关联的逻辑，这些协议使用 8b/10b 编码/解码。

## **本章**

本章描述了 PCIe 第三代（Gen3）的逻辑物理层特性。主要变化包括在不使频率翻倍的情况下将带宽相对于 Gen2 速率翻倍的能力（链路速率从 5 GT/s 增加到 8 GT/s）。这是通过在 Gen3 模式下消除 8b/10b 编码来实现的。在 Gen3 速率下需要更强的信号补偿。

## **下一章**

下一章描述了物理层与链路的电气接口。本章还讨论了对信号均衡的需求以及实现该均衡的方法。本章结合了 Gen1、Gen2 和 Gen3 速率的电气发送器和接收器特性。

## **Gen3 简介**

回想一下，当 PCIe 链路进入训练时（即，在复位之后），它始终从 Gen1 速率开始以保持向后兼容性。如果在训练期间通告了更高的速率，则链路将立即转换到 Recovery 状态，并尝试更改为双方共同支持的最高速率。

**407**

## **PCI Express 技术**

将 PCIe 规范升级到 Gen3 的主要动机是将带宽翻倍，如第 408 页的表 12‐1 所示。完成此操作的直接方法是将信号频率从 5 GT/s 简单地翻倍到 10 Gb/s，但这样做带来了几个问题：

- 更高的频率消耗更多的功率，由于在更高速度下保持信号完整性需要复杂的调理逻辑（均衡），这种情况会更加严重。事实上，PCISIG 文献中提到这种均衡逻辑的功耗是将频率保持在尽可能低的水平的一个重要动机。

- 某些电路板材料在更高频率下会出现严重的信号衰减。可以通过更好的材料和更多的设计工作来克服这个问题，但这些会增加成本和开发时间。由于 PCIe 旨在服务于各种系统，目标是它也应能在低成本设计中良好工作。

- 类似地，允许新设计使用现有的基础设施（例如电路板和连接器）可以最大程度地减少电路板设计工作量和成本。使用更高的频率会使这变得更加困难，因为必须调整走线长度和其他参数以适应新的时序，这使得高频不太受欢迎。

_表 12‐1：不同链路宽度的 PCI Express 总带宽_

|**链路宽度**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 带宽**<br>**(GB/s)**|0.5|1|2|4|6|8|16|
|**Gen2 带宽**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 带宽**<br>**(GB/s)**|2|4|8|16|24|32|64|



这些考虑导致了与前几代相比 Gen3 规范的两个重大变化：新的编码模型和更复杂的信号均衡模型。

**408**

**第 12 章：物理层 - 逻辑 (Gen3)**

## **新的编码模型**

物理层的逻辑部分用新的 128b/130b 编码方案取代了 8b/10b 编码。当然，这意味着要摆脱许多串行设计中使用的、人们已经很好理解的 8b/10b 模型。设计人员愿意采取这一步骤来回收 8b/10b 编码所造成的 20% 传输开销。使用 128b/130b 意味着 Lane 现在每个字节传递 8 位而不是 10 位，这意味着 8.0 GT/s 的数据速率将带宽翻倍。这相当于每个方向 1 GB/s 的带宽。

为了说明这两种编码之间的差异，首先考虑图 12-1，它显示了通用的 8b/10b 数据包构造。箭头突出显示了表示 8b/10b 数据包成帧符号的控制（K）字符。接收器通过识别这些控制字符知道会发生什么。请参阅第 380 页的"8b/10b 编码"以回顾此编码方案的优势。

_图 12‐1：8b/10b Lane 编码_

**==> picture [344 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
'D' Characters<br>STP Sequence Header Data Payload  ECRC LCRC END<br>
'D' Characters<br>
'K' Character 'K' Character<br>
SDP DLLP Type Misc. CRC END<br>
'K' Character 'K' Character<br>
**----- End of picture text -----**<br>


相比之下，第 410 页的图 12‐2 显示了 128b/130b 编码。此编码不影响正在传输的字节，而是将字符分组为 16 字节的块，每个块的开头有一个 2 位 Sync 字段。2 位 Sync 字段指定块是包含数据（10b）还是有序集（01b）。因此，Sync 字段向接收器指示期望的流量类型以及何时开始。有序集与 8b/10b 版本类似，因为它们必须在所有 Lane 上同时驱动。这要求正确同步 Lane，这是训练过程的一部分（请参见第 438 页的"实现块对齐"）。

**409**

**PCI Express 技术**

_图 12‐2：128b/130b 块编码_

**==> picture [354 x 50] intentionally omitted <==**

**----- Start of picture text -----**<br>
0    1 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7<br>
Sync  Symbol 0 Symbol 1 Symbol 15<br>
Field<br>
**----- End of picture text -----**<br>


## **复杂的信号均衡**

第二个更改是在物理层的电气子块中进行的，涉及在链路发送端以及可选地在接收端进行更复杂的信号均衡。Gen1 和 Gen2 实现使用固定的 Tx 去加重来实现良好的信号质量。然而，将传输频率提高到 5 GT/s 以上会导致信号完整性问题变得更加突出，需要更多的发送器和接收器补偿。这可以在电路板级别进行一些管理，但设计人员希望允许外部基础设施尽可能保持不变，而将负担放在 PHY 发送器和接收器电路上。有关信号调理的更多详细信息，请参阅第 474 页的"8.0 GT/s 解决方案 - 发送器均衡"。

## **8.0 GT/s 编码**

如前所述，Gen3 128b/130b 编码方法使用链路范围的数据包和按 Lane 的块编码。本节提供有关编码的其他详细信息。

## **Lane 级别编码**

为了说明块的使用，请考虑第 411 页的图 12‐3，其中显示了单 Lane 数据块。开头是两个 Sync Header 位，后跟 16 字节（128 位）信息，共产生 130 个传输位。Sync Header 仅定义正在发送的是数据块（10b）还是有序集（01b）。您可能已经注意到图 12‐3 中的数据块的 Sync Header 值为 01，而不是上面提到的 10b 值。这是因为当跨链路传输块时，Sync Header 的最低有效位首先发送。请注意，Sync Header 之后的符号也以最低有效位优先发送。

**410**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12‐3：Sync Header 数据块示例_

**==> picture [374 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync Symbol 0 Symbol 1 Symbol 15<br>
(01)<br>
128-bit Payload<br>
Data Block<br>
UI UI UI<br>
0 2 10 122<br>
= = = =<br>
Time Time Time Time<br>
**----- End of picture text -----**<br>


## **块对齐**

与之前的实现一样，Gen3 首先实现位锁定（Bit Lock），然后尝试建立块对齐（Block Alignment）锁定。这要求接收器找到作为块边界标记的 Sync Header。发送器通过发送由交替的 00h 和 FFh 字节组成的可识别的 EIEOS 模式来建立此边界，如图 12‐4 所示。因此，EIEOS 的使用已从仅仅退出电气空闲扩展为还可作为建立块对齐的同步机制。请注意，Sync Header 位紧接在 EIEOS 之前和之后（图中未显示）。有关此过程的详细信息，请参见第 438 页的"实现块对齐"。

_图 12‐4：Gen3 模式 EIEOS 符号模式_

**==> picture [89 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 00000000<br>
1 11111111<br>
2 00000000<br>
3 11111111<br>
4 00000000<br>
13 11111111<br>
14 00000000<br>
15 11111111<br>
**----- End of picture text -----**<br>


**411**

**PCI Express 技术**

## **有序集块**

有序集在 Gen1 和 Gen2 中的含义大致相同。它们用于管理 Lane 协议。当发送有序集块时，它必须同时出现在所有 Lane 上，并且几乎总是由 16 个字节组成，只有一个例外。此大小规则的一个例外是 SOS（SKP 有序集），它可以通过时钟补偿逻辑（例如与链路中继器相关联）以四个为一组添加或删除 SKP 符号，因此合法长度可以是 8、12、16、20 或 24 字节。

有序集块的基本格式与数据块类似，只是 Sync Header 位是相反的，如第 412 页的图 12‐5 所示。

_图 12‐5：Gen3 x1 有序集块示例_

**==> picture [347 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 0 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync Symbol 0 Symbol 1 Symbol 15<br>
(10)<br>
128-bit Payload<br>
Ordered Set Block<br>
UI UI UI<br>
0 2 10 122<br>
= = = =<br>
Time Time Time Time<br>
**----- End of picture text -----**<br>


规范为 Gen3 定义了七个有序集（比 Gen1 和 Gen2 PCIe 多一个有序集）。在大多数情况下，它们的功能与前几代相同。

1. SOS - Skip 有序集：用于时钟补偿。有关更多详细信息，请参见第 426 页的"有序集示例 - SOS"。

2. EIOS - Electrical Idle 有序集：用于进入电气空闲状态

3. EIEOS - Electrical Idle Exit 有序集：现在用于两个目的：— 电气空闲退出，如以前

   - 8.0 GT/s 的块对齐指示符

4. TS1 - Training Sequence 1 有序集

5. TS2 - Training Sequence 2 有序集

6. FTS - Fast Training Sequence 有序集

7. SDS - Start of Data Stream 有序集：新增 - 有关更多信息，请参见第 413 页的"数据流和数据块"

**412**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-4"></a>
## 10.4 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|**Symbol 0**<br>**Sync**<br>**Symbol 1**<br>**Symbol 2**<br>**Symbol 3**<br>**Symbol 4**<br>**Symbol 5**<br>**Symbol 6**<br>**Symbol 7**|**Lane 0**<br>**Lane 1**<br>**Lane 2**<br>**Lane 3**||||IDL<br>IDL<br>IDL<br>IDL<br>Data DW 17<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>Data DW 15<br>Hea3er DW 3<br>Header DW 1<br>SDP Token<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>DW 21<br>DW 19<br>DW 3<br>DW 1<br>**TLP**<br>**straddles**<br>**Block**<br>**boundary**<br>**Lane 4**<br>**Lane 5**<br>**Lane 6**<br>**Lane 7**<br>**Logical**<br>**Idle**<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL||||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
||STP Token: Length=7, CRC, Parity, Seq Num||||||||
||||TLP||||||
||||||||||
||**LCRC**||||SDP Token||||
|||DLLP|||IDL|IDL|IDL|IDL|
||IDL|IDL|IDL|IDL|IDL|IDL|IDL|IDL|
||STP Token: Length=23, CRC, Parity, Seq Num|||||Header DW 1<br>DW 1|||
|||Header DW 2<br>DW 2||||Hea3er DW 3<br>DW 3|||
|**Symbol 15**<br>**Sync**<br>**Symbol 0**<br>**Symbol 1**||Data DW 14<br>DW 18||||Data DW 15<br>DW 19|||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
|||Data DW 16<br>DW 20||||Data DW 17<br>DW 21|||
||**LCRC**||||IDL|IDL|IDL|IDL|
||||||||||
||||||||||



Next a DLLP is sent beginning with the SDP Token on Lanes 4 and 5. Since a DLLP is always 8 Symbols long, it will finish in Lane 3 of Symbol 4. Momen‐ tarily, there are no other packets to send, so IDL Symbols are transferred until another packet is ready. When IDLs are sent, the next STP Token can only start in Lane 0. In the example, the TLP starts in Lane 0 of Symbol 6. 

The packet length for the next TLP is 23 DW and that presents an interesting sit‐ uation because there are only 20 dwords available before the next Block bound‐ ary. When the Data Block ends the transmitter sends Sync and continues TLP transmission during Symbol 0 of the next Block. In other words, Packets simply straddle Block boundaries when necessary. Finally, the TLP finishes in Lane 3 of Symbol 1. Once again there are no packets ready to send, so IDLs are sent. 

## **Nullified Packet x8 Example** 

Nullified TLPs can occur when a TLP is being transferred across a switch to reduce latency. This is called Switch Cut‐Through operation. The reader may choose to review the section entitled “Switch Cut‐Through Mode” on page 354 before proceeding with this discussion. 

**425** 

## **PCI Ex ress Technolo p gy** 

A nullified TLP can occur when a switch forwards a packet to the egress port before having received the packet at the ingress port and before error checking. Because an error was detected in this example, the TLP must be nullified. 

Figure 12‐13 illustrates the steps taken to nullify TLP. The TLP being sent by the egress port, starts in the first block (Lane 0 of Symbol 6). When the error is detected, the egress port inverts the CRC (Lanes 0‐3 of Symbol 1) and adds an EDB token immediately following the TLP (Lanes 4‐7 of symbol 1). Together, those two changes make it clear to the Receiver that this TLP has been nullified and should be discarded. Note that the EDB bytes are not included in the packet length field, because they dynamically added to a packet in flight when an error occurs. 

_Figure 12‐13: Gen3 x8 Nullified Packet_ 

||||||||||
|---|---|---|---|---|---|---|---|---|
|**Symbol 0**<br>**Sync**<br>**Symbol 1**<br>**Symbol 2**<br>**Symbol 3**<br>**Symbol 4**<br>**Symbol 5**<br>**Symbol 6**<br>**Symbol 7**|**Lane 0**<br>**Lane 1**<br>**Lane 2**<br>**Lane 3**||||EDB<br>EDB<br>EDB<br>EDB<br>Data DW 17<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>Data DW 15<br>Hea3er DW 3<br>Header DW 1<br>SDP Token<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>DW 21<br>DW 19<br>DW 3<br>DW 1<br>**TLP**<br>**straddles**<br>**Block**<br>**boundary**<br>**Lane 4**<br>**Lane 5**<br>**Lane 6**<br>**Lane 7**<br>**Logical**<br>**Idle**<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>**Nullified  TLP**||||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
||STP Token: Length=7, CRC, Parity, Seq Num||||||||
||||TLP||||||
||||||||||
||**LCRC**||||SDP Token||||
|||DLLP|||IDL|IDL|IDL|IDL|
||IDL|IDL|IDL|IDL|IDL|IDL|IDL|IDL|
||STP Token: Length=23, CRC, Parity, Seq Num|||||Header DW 1<br>DW 1|||
|||Header DW 2<br>DW 2||||Hea3er DW 3<br>DW 3|||
|**Symbol 15**<br>**Sync**<br>**Symbol 0**<br>**Symbol 1**||Data DW 14<br>DW 18||||Data DW 15<br>DW 19|||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
|||Data DW 16<br>DW 20||||Data DW 17<br>DW 21|||
||LCRC (inverted)||||EDB|EDB|EDB|EDB|
||||||||||
||||||||||



## **Ordered Set Example - SOS** 

Now let’s consider an example of Ordered Set transmission. As shown in Figure 12‐14 on page 427, an Ordered Set is indicated by the 2‐bit Sync Header value of 01b. The bytes that follow will be understood by the receiver to make up an Ordered Set that is always 16 bytes (128 bits) in length. The one exception is the 

**426** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

SOS (Skip Ordered Set), because it can be changed by intermediate receivers in increments of 4 bytes at a time for clock compensation. Consequently, an SOS is legally allowed to be 8, 12, 16, 20, or 24 Symbols in length. In the absence of a Link repeater device that does not add or delete SKPs in a SOS, a SOS will also be made up of 16 bytes. 

_Figure 12‐14: Gen3 x1 Ordered Set Construction_ 

**==> picture [376 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 1 Symbol 15<br>(10)<br>128-bit Payload<br>Ordered Set Block<br>0 2UI 10UI 122UI<br>= = = =<br>Time Time Time Time<br>**----- End of picture text -----**<br>


To illustrate an Ordered Set, let’s use an SOS to show the various features and how they work together. Consider Figure 12‐15 on page 428, where a Data Block is followed by an SOS. The framing rules state that the previous Data Block must end with an EDS Token in the last dword to let the receiver know that an Ordered Set is coming. If the current Data Stream is to continue, the Ordered Set that follows must be an SOS, and that must be followed in turn by another Data Block. This example doesn’t show it, but it’s possible that a TLP might be incom‐ plete at this point and would straddle the SOS by resuming transmission in the Data Block that must immediately follow the SOS. 

Receiving the EDS Token means that the Data Stream is either ending or paus‐ ing to insert an SOS. An EDS is the only Token that can start on a dword‐ aligned Lane in the same Symbol Time as an IDL, and this example does just that, beginning in Lane 4 of Symbol Time 15. Recall that EDS must also be in the last dword of the Data Block. According to the receiver framing requirements, only an Ordered Set Block is allowed after an EDS and must be an SOS, EIOS, or EIEOS or else it will be seen as a framing error. As was true for earlier spec ver‐ sions, the Ordered Sets must appear on all Lanes at the same time. Receivers may optionally check to ensure that each Lane sees the same Ordered Set. 

In our example, a 16 byte SOS is seen next, and is recognized by the Ordered Set Sych Header as well as the SKP byte pattern. There are always 4 Symbols at the end of the SOS that contain the current 24‐bit scrambler LFSR state. In Symbol 

**427** 

**PCI Ex ress Technolo p gy** 

12 the Receiver knows that the SKP characters have ended and also that the Block has three more bytes to deliver per Lane. These are the output of the scrambling logic LFSR, as shown in Table 12‐2 on page 428. 

_Figure 12‐15: Gen3 x8 Skip Ordered Set (SOS) Example_ 

**==> picture [384 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane 0 Lane 1 Lane 2 Lane 3 Lane 4 Lane 5 Lane 6 Lane 7<br>Data<br>Sync 01 01 01 01 01 01 01 01 Block<br>Symbol 0 STP Token:STP: LengthLength=7,= 7, CRC,CRC,Parity,Parity, Seq NumSeq Num<br>Symbol 1 (TLPTLP7 DW )<br>Symbol 2<br>Symbol 3 LCRC SDP Token<br>Symbol 4 DLLP IDL IDL IDL IDL<br>Symbol 5 IDL IDL IDL IDL IDL IDL IDL IDL End of<br>Symbol 6 SDP Token DLLP Data<br>Stream<br>Symbol 7 IDL IDL IDL IDL IDL IDL IDL IDL<br>Marker<br>Symbol 15 IDL IDL IDL IDL EDS Token Marker(End of Data StreamPacket )<br>Sync 10 10 10 10 10 10 10 10 OrderedSet Block<br>Symbol 0 SKP SKP SKP SKP SKP SKP SKP SKP<br>Symbol 3 SKP SKP SKP SKP SKP SKP SKP SKP End of<br>SOS<br>Symbol 4 SKP_END SKP_END SKP_END SKP_END SKP_END SKP_END SKP_END SKP_END<br>LFSR<br>Symbol 5 LFSR LFSR LFSR LFSR LFSR LFSR LFSR LFSR output<br>Symbol 6 LFSR LFSR LFSR LFSR LFSR LFSR LFSR LFSR as filler<br>Symbol 7 LFSR LFSR LFSR LFSR LFSR LFSR LFSR LFSR<br>Data<br>Sync 01 01 01 01 01 01 01 01 Block<br>**----- End of picture text -----**<br>


_Table 12‐2: Gen3 16‐bit Skip Ordered Set Encoding_ 

|**Symbol**<br>**Number**|**Value**|**Description**|
|---|---|---|
|0 to 11|AAh|SKP Symbol. Since Symbol 0 is the Ordered Set Identifier,<br>this is seen as an SOS.|
|12|E1h|SKP_END Symbol, which indicates that the SOS will be com‐<br>plete after 3 more Symbols|



**428** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Table 12‐2: Gen3 16‐bit Skip Ordered Set Encoding (Continued)_ 

|**Symbol**<br>**Number**|**Value**|**Description**|
|---|---|---|
|13|00‐FFh|a) If LTSSM state is Polling.Compliance: AAh<br>b) Else if prior block was a Data Block:<br>Bit [7] = Data Parity<br>Bit [6:0] = LFSR [22:16]<br>c) Else<br>Bit [7] = ~LFSR [22]<br>Bit [6:0] = LFSR [22:16]|
|14|00‐FFh|a) If LTSSM state is Polling.Compliance: Error_Status [7:0]<br>b) Else LFSR [15:8]|
|15|00‐FFh|a) If LTSSM state is Polling.Compliance: Error_Status [7:0]<br>b) Else LFSR [7:0]|



The Data Parity bit mentioned in the table is the even parity of all the Data Block scrambled bytes that have been sent since the most recent SDS or SOS and is created independently for each Lane. Receivers are required to calculate and check the parity. If the bits don’t match, the Lane Error Status register bit corre‐ sponding to the Lane that saw the error must be set, but this is not considered a Receiver Error and does not initiate Link retraining. 

The 8‐bit Error_Status field only has meaning when the LTSSM is in the Poll‐ ing.Compliance state (see “Polling.Compliance” on page 529 for more details). For our example of an SOS following a Data Block, byte 13 is the Data Parity bit and LFSR[22:16], while the last two bytes are LFSR bits [15:0]. 

## **Transmitter SOS Rules** 

The SOS rules for Transmitters when using 128b/130b include: 

- An SOS must be scheduled to occur within 370 to 375 blocks. In Loopback mode, however, the Loopback Master must schedule two SOS’s within that time, and they must be no more than two blocks from each other. 

- SOS’s can still only be sent on packet boundaries and may be accumulated as a result. However, consecutive SOS’s are not permitted; they must be sep‐ arated by a Data Block. 

- It’s recommended that SOS timers and counters be reset whenever the Transmitter is Electrically Idle. 

**429** 

**PCI Ex ress Technolo p gy** 

- The Compliance SOS bit in Link Control Register 2 has no effect when using 128b/130b. (It’s used to disable SOSs during Compliance testing for 8b/10b, but that isn’t an option for 128b/130b.) 

## **Receiver SOS Rules** 

The Skip Ordered Set rules for Receivers when using 128b/130b include: 

- They must tolerate receiving SOS’s at an average interval of 370‐375 blocks. Note that the first SOS after Electrical Idle may arrive earlier than that, since Transmitters are not required to reset SOS timers during Electrical Idle time.

</td>
<td style="background-color:#e8e8e8">

- 接收器必须检查数据流中的每个 SOS 前面是否都有一个以 EDS 结束的数据块。

## **加扰 (Scrambling)**

128b/130b 的加扰逻辑相对于以前的 PCIe 代进行了修改，以解决 8b/10b 编码自动处理的两个问题：保持 DC 平衡和提供足够的转换密度。通过回顾，请记住 DC 平衡意味着位流具有相等数量的 1 和 0。这旨在避免"DC 漂移 (DC wander)"问题，其中传输介质由于 1 或 0 的普遍存在而向一个电压或另一个电压充电，以至于难以在所需时间内切换信号。另一个问题是接收器处的时钟恢复需要看到输入信号中的足够边沿，以便能够将它们与恢复的时钟进行比较并根据需要调整时序和相位。

如果没有 8b/10b 来处理这些问题，则采取了三个步骤：首先，新的加扰方法在较长时间内改善了转换密度和 DC 平衡，但不能像 8b/10b 那样在短时间内保证它们。其次，训练期间使用的 TS1 和 TS2 有序集合模式包含根据需要进行调整以改善 DC 平衡的字段。第三，接收器必须比早期代更稳健和更能容忍这些问题。

## **LFSR 数量 (Number of LFSRs)**

在较低的数据速率下，每个通道以相同的方式加扰，因此单个线性反馈移位寄存器 (LFSR) 可以为所有通道提供加扰输入。对于 Gen3，设计人员希望相邻通道具有不同的加扰值。原因可能包括希望通过相对于彼此加扰输出来降低通道之间串扰的可能性，并避免每个通道上的值相同，就像

**430**

**第 12 章：物理层 - 逻辑 (Gen3)**

发送 IDL 时发生的那样。规范描述了实现此目标的两种方法，一种强调低延迟，另一种强调低成本。

**第一种选择：多个 LFSR。** 一种解决方案是为每个通道实现单独的 LFSR，并使用不同的起始值或"种子 (seed)"初始化每个 LFSR。这具有简单和速度快的优点，但代价是增加了逻辑。如图 12-16 所示，每个 LFSR 根据规范中给出的多项式 G(X) = X[23] + X[21] + X[16] + X[8] + X[5] + X[2] + 1 创建伪随机输出。该多项式比以前的版本更长，并且由于不同的种子值，行为也略有不同。为每个通道指定了八个不同的种子值，需要八个不同的 LFSR，每个通道 0 到 7 一个。

_图 12-16：Gen3 每通道 LFSR 加扰逻辑_

**==> 图片 [369 x 155] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>
+ + +<br>
种子 种子 种子 种子 种子 种子 种子 种子 种子 种子 种子 种子<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>
D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>
+ +<br>
种子 种子 种子 种子 种子 种子 种子 种子 种子 种子 种子<br>
D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>
数据输入 + 数据输出<br>
**----- 图片文字结束 -----**<br>


每个通道的 24 位种子值列在第 432 页的表 12-3 中。该系列重复自身，意味着通道 8 的种子与通道 0 相同，因此仅显示前 8 个值。每个通道使用相同的 LFSR 和相同的抽头点来创建加扰输出，不同的种子值给出所需的差异。

**431**

## **PCI Ex ress Technolo p gy**

_表 12-3：Gen3 加扰器种子值_

|**通道**|**种子值**|
|---|---|
|0|1DBFBCh|
|1|0607BBh|
|2|1EC760h|
|3|18C0DBh|
|4|010F12h|
|5|19CFC9h|
|6|0277CEh|
|7|1BB807h|


**第二种选择：单个 LFSR。** 另一种解决方案如图 12-17（第 433 页）所示，用于通道 2、10、18 和 26，是仅使用一个 LFSR 并通过对不同的抽头点进行 XOR 来创建每个通道的加扰输入。由于只有一个 LFSR，所有通道的种子值都相同（全 1），但每个通道的加扰"抽头方程 (Tap Equation)"通过组合不同的抽头点派生，如第 433 页的表 12-4 所示。规范还指出，4 个通道的抽头方程可以通过对其位邻居的抽头值进行 XOR 来派生：

- 通道 0 = 通道 7 XOR 通道 1（请注意，向较低通道号进行的过程会环绕，结果是通道 7 被认为低于通道 0）

- 通道 2 = 通道 1 XOR 通道 3

- 通道 4 = 通道 3 XOR 通道 5

- 通道 6 = 通道 5 XOR 通道 7

单 LFSR 解决方案使用的门数少于多 LFSR 版本，但通过 XOR 过程会产生额外的延迟，提供了不同的成本/性能选项。

**432**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12-17：Gen3 单 LFSR 加扰器_

**==> 图片 [378 x 162] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>
+ + +<br>
种子 种子 种子 种子 种子 种子 种子 种子 种子 种子 种子 种子<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>
D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>
+ +<br>
种子 种子 种子 种子 种子 种子 种子 种子 种子 种子 种子<br>
D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>
+<br>
通道 2、10、18 和 26 的"抽头方程"<br>
数据输入 + 数据输出<br>
（对于通道 2、10、18 或 26）<br>
**----- 图片文字结束 -----**<br>


_表 12-4：单 LFSR 加扰器的 Gen3 抽头方程_

|**通道号**|**抽头方程**|
|---|---|
|0, 8, 16, 24<br>|D9 xor D13|
|1, 9, 17, 25<br>|D1 xor D13|
|2, 10, 18, 26<br>|D13 xor D22|
|3, 11, 19, 27<br>|D1 xor D22|
|4, 12, 20, 28<br>|D3 xor D22|
|5, 13, 21, 29|D1 xor D3|
|6, 14, 22, 30|D3 xor D9|
|7, 15, 23, 31|D1 xor D9|


## **加扰规则 (Scrambling Rules)**

Gen3 加扰器 LFSR（无论是一个还是多个）不会持续前进，而只是根据正在发送的内容前进。加扰器必须定期重新初始化，这会在每次看到 EIEOS 或 FTSOS 时进行。规范给出了几条加扰规则，此处列出以方便使用：

**433**

## **PCI Ex ress Technolo p gy**

- Sync Header 位不加扰，也不推进 LFSR。

- 发送器 LFSR 在发送最后一个 EIEOS 字符时重置，接收器 LFSR 在接收到最后一个 EIEOS 字符时重置。

- TS1 和 TS2 有序集合：

   - 字符 0 旁路加扰

   - 字符 1 到 13 被加扰

   - 字符 14 和 15 可能被加扰，也可能不被加扰。规范声明，如果需要改善 DC 平衡，它们将旁路加扰，否则将被加扰（有关如何维护 DC 平衡的更多详细信息，请参见第 510 页的"TS1 和 TS2 有序集合 (TS1 and TS2 Ordered Sets)"）。

- 有序集合 FTS、SDS、EIEOS、EIOS 和 SOS 的所有字符旁路加扰。尽管如此，输出数据流将具有足够的转换密度以允许时钟恢复，并且为有序集合选择的字符会产生 DC 平衡的输出。

- 即使被旁路，发送器也会为其所有有序集合字符推进 LFSR，但 SOS 中的字符除外。

- 接收器也是如此，检查传入有序集合的字符 0 以查看它是否是 SOS。如果是，则 LFSR 不会为该块中的任何字符推进。否则 LFSR 会为该块中的所有字符推进。

- 所有数据块字符都被加扰并推进 LFSR。

- 字符以小端序加扰，这意味着最低有效位首先被加扰，最高有效位最后被加扰。

- 每通道 LFSR 的种子值取决于 LTSSM 首次进入 Configuration.Idle（已完成 Polling 状态）时分配给该通道的通道号。种子值（模 8）如第 432 页的表 12-3 所示，并且一旦分配，只要 LinkUp = 1 就不会更改，即使通过返回到 Configuration 状态来更改通道分配也是如此。

- 与 8b/10b 不同，使用 128b/130b 编码时无法禁用加扰，因为需要它来帮助信号完整性。不期望链路在没有它的情况下可靠地运行，因此它必须始终开启。

- Loopback Slave 不得对环回位进行加扰或解扰。

## **串行器 (Serializer)**

此移位寄存器的工作方式与 Gen1/Gen2 数据速率相同，只是它现在一次接收 8 位而不是 10 位（即，串行器是 8 位并串转换移位寄存器）。

**434**

**第 12 章：物理层 - 逻辑 (Gen3)**

## **Sync Header 位的 Mux**

最后，必须注入两个 Sync Header 位以将下一个字符块区分为数据块或有序集合块。这些是每个 130 位块的前两位，并且它们的逻辑可以添加到发送器中对设计有意义的任何位置。在此示例中，为简单起见，这些位在过程结束时注入。无论在何处包含它们，来自上面的字节流都必须停止以留出时间。在此示例中，需要一种方法来通知上面的逻辑暂停两个位时间。传入数据包流将在发送 Sync 位的时间内在 Tx 缓冲区中排队。

## **Gen3 物理层接收逻辑 (Gen3 Physical Layer Receive Logic)**

与早期代一样，接收器逻辑（第 436 页图 12-18 所示）以 CDR（时钟和数据恢复，Clock and Data Recovery）电路开始。这可能包括一个 PLL，它基于预期频率的知识和位流中的边沿来锁定发送器时钟频率，以生成恢复的时钟 (Rx Clock)。此恢复的时钟将传入位锁存到解串缓冲区中，然后一旦在 LTSSM 的 Recovery 状态期间建立了块对齐 (Block Alignment)，恢复的时钟除以 8.125 的另一个版本 (Rx Clock/8.125) 将 8 位字符锁存到弹性缓冲区中。之后，解扰器从加扰字符中重新创建原始数据。字节绕过 8b/10b 解码器并直接传递到字节解交错逻辑。最后，有序集合被过滤掉，剩余的 TLP 和 DLLP 字节流被转发到数据链路层。

在下面的讨论中，从下往上描述每个部分。重点是描述针对 8.0 GT/s 改变的物理层方面。未从 Gen1/Gen2 改变的子块将不在本节中描述。

## **差分接收器 (Differential Receiver)**

差分接收器逻辑未更改，但电气更改以改善信号完整性（参见第 468 页的"信号补偿 (Signal Compensation)"），以及建立信号均衡的训练更改在第 577 页的"链路均衡概述 (Link Equalization Overview)"中介绍。

**435**

## **PCI Ex ress Technolo p gy**

_图 12-18：Gen3 物理层接收器详细信息_

**==> 图片 [276 x 369] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
到数据链路层<br>
eceiTLP/DLLP 指示符<br>
N*8<br>
Rx<br>
缓冲区<br>
TLP/DLLP<br>
N*8 指示符<br>
数据包<br>
过滤<br>
块<br>
N*8 D/K# 类型<br>
通道 0 字节解交错 通道 N<br>
8 8<br>
Mux Mux<br>
8 8 8 8<br>
D/K# D/K#<br>
Gen3 解扰器 Gen3 解扰器<br>
解扰器 解扰器<br>
8 8 D/K# 8 8 D/K#<br>
8b/10b 8b/10b<br>
解码器 解码器<br>
Gen3 Gen3<br>
10 块 10 块<br>
类型 类型<br>
CDR 逻辑 CDR 逻辑<br>
Rx Rx<br>
通道 0 通道 1, ..,N-1 通道 N<br>
**----- 图片文字结束 -----**<br>


**436**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12-19：Gen3 CDR 逻辑_

**==> 图片 [385 x 234] 已故意省略 <==**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---




<img src="figures/embedded/page0001_img2_tight.png" alt="Figure from page 1" width="700">


<img src="figures/embedded/page0001_img1.png" alt="Figure from page 1" width="700">

<a id="sec-10-5"></a>
## 10.5 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Receivers must check to see that every SOS in a Data Stream is preceded by a Data Block that ends with EDS. 

## **Scrambling** 

The scrambling logic for 128b/130b is modified from the previous PCIe genera‐ tions to address the two issues that 8b/10b encoding handled automatically: maintaining DC Balance and providing a sufficient transition density. By way of review, recall that DC Balance means the bit stream has an equal number of ones and zeros. This is intended to avoid the problem of “DC wonder”, in which the transmission medium is charged toward one voltage or the other so much, by a prevalence of ones or zeros, that it becomes difficult to switch the signal within the necessary time. The other problem is that clock recovery at the Receiver needs to see enough edges in the input signal to be able to compare them to the recovered clock and adjust the timing and phase as needed. 

Without 8b/10b to handle these issues, three steps were taken: First, the new scrambling method improves both transition density and DC Balance over longer time periods, but doesn’t guarantee them over short periods the way 8b/ 10b did. Second, the TS1 and TS2 Ordered Set patterns used during training include fields that are adjusted as needed to improve DC Balance. And third, Receivers must be more robust and tolerant of these issues than they were in the earlier generations. 

## **Number of LFSRs** 

At the lower data rates every Lane was scrambled in the same way, so a single Linear‐Feedback Shift Register (LFSR) could supply the scrambling input for all of them. For Gen3, though, the designers wanted different scrambling values for neighboring Lanes. The reasons probably include a desire to decrease the possibility of cross‐talk between the Lanes by scrambling their outputs with respect to each other and avoid having the same value on each Lane, as might 

**430** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

happen when sending IDLs. The spec describes two approaches to achieving this goal, one that emphasizes lower latency and one that emphasizes lower cost. 

**First Option: Multiple LFSRs.** One solution is to implement a separate LFSR for each Lane, and initialize each with a different starting value or “seed”. This has the advantage of simplicity and speed, at the cost of add‐ ing logic. As shown in Figure 12‐16, each LFSR creates a pseudo‐random output based on the polynomial given in the spec as G(X) = X[23] + X[21] + X[16] + X[8] + X[5] + X[2] + 1. This polynomial is longer than the previous version and also behaves a little differently because of the different seed values. Eight different seed values for each Lane are specified requiring eight different LFSRs, one per Lane 0 through 7. 

_Figure 12‐16: Gen3 Per‐Lane LFSR Scrambling Logic_ 

**==> picture [369 x 155] intentionally omitted <==**

**----- Start of picture text -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>+ + +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+ +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>Data In + Data Out<br>**----- End of picture text -----**<br>


The 24‐bit seed value for each Lane is listed in Table 12‐3 on page 432. The series repeats itself, meaning the seed for Lane 8 will be the same as Lane 0, so only the first 8 values are shown. Every Lane uses the same LFSR and the same tap points to create the scrambling output, and the different seed val‐ ues give the desired difference. 

**431** 

## **PCI Ex ress Technolo p gy** 

_Table 12‐3: Gen3 Scrambler Seed Values_ 

|**Lane**|**Seed Value**|
|---|---|
|0|1DBFBCh|
|1|0607BBh|
|2|1EC760h|
|3|18C0DBh|
|4|010F12h|
|5|19CFC9h|
|6|0277CEh|
|7|1BB807h|



**Second Option: Single LFSR.** The alternative solution, illustrated in Figure 12‐17 on page 433 for Lanes 2, 10, 18, and 26, is to use just one LFSR and create the scrambling inputs for each Lane by XORing different tap points together. Since there’s only one LFSR, the seed value is the same for all Lanes (all ones), but the scrambling “Tap Equation” for each Lane is derived by combining different tap points, as shown in Table 12‐4 on page 433. The spec also notes that 4 of the Lanes Tap Equations can be derived by XORing the tap values of their bit neighbors: 

- Lane 0 = Lane 7 XOR Lane 1 (note that the process of going to lower Lane numbers wraps around, with the result that Lane 7 is considered lower that Lane 0) 

- Lane 2 = Lane 1 XOR Lane 3 

- Lane 4 = Lane 3 XOR Lane 5 

- Lane 6 = Lane 5 XOR Lane 7 

The single‐LFSR solution uses fewer gates than the multi‐LFSR version does, but incurs extra latency through the XOR process, providing a differ‐ ent cost/performance option. 

**432** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐17: Gen3 Single‐LFSR Scrambler_ 

**==> picture [378 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>+ + +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+ +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+<br>“Tap Equation” for Lanes 2, 10, 18, and 26<br>Data In + Data Out<br>(for Lanes 2, 10, 18, or 26)<br>**----- End of picture text -----**<br>


_Table 12‐4: Gen3 Tap Equations for Single‐LFSR Scrambler_ 

|**Lane Numbers**<br>**T**|**ap Equation**|
|---|---|
|0, 8, 16, 24<br>|D9 xor D13|
|1, 9, 17, 25<br>|D1 xor D13|
|2, 10, 18, 26<br>|D13 xor D22|
|3, 11, 19, 27<br>|D1 xor D22|
|4, 12, 20, 28<br>|D3 xor D22|
|5, 13, 21, 29|D1 xor D3|
|6, 14, 22, 30|D3 xor D9|
|7, 15, 23, 31|D1 xor D9|



## **Scrambling Rules** 

The Gen3 scrambler LFSRs (whether one or more) do not continually advance, but only advance based on what is being sent. The scramblers must be re‐initial‐ ized periodically and that takes place whenever an EIEOS or FTSOS is seen. The spec gives several rules for scrambling that are listed here for convenience: 

**433** 

## **PCI Ex ress Technolo p gy** 

- Sync Header bits are not scrambled and do not advance the LFSR. 

- The Transmitter LFSR is reset when the last EIEOS Symbol has been sent, and the Receiver LFSR is reset when the last EIEOS Symbol is received. 

- TS1 and TS2 Ordered Sets: 

   - Symbol 0 bypasses scrambling 

   - Symbols 1 to 13 are scrambled 

   - Symbols 14 and 15 may or may not be scrambled. The spec states that they will bypass scrambling if necessary to improve DC Balance, but otherwise will be scrambled (see “TS1 and TS2 Ordered Sets” on page 510 for more details on how DC Balance is maintained). 

- All Symbols of the Ordered Sets FTS, SDS, EIEOS, EIOS, and SOS bypass scrambling. Despite this, the output data stream will have sufficient transi‐ tion density to allow clock recovery and the symbols chosen for the Ordered Sets result in a DC balanced output. 

- Even when bypassed, Transmitters advance their LFSRs for all Ordered Set Symbols except for those in the SOS. 

- Receivers do the same, checking Symbol 0 of an incoming Ordered Set to see whether it is an SOS. If so, the LFSRs are not advanced for any of the Symbols in that Block. Otherwise the LFSRs are advanced for all the Sym‐ bols in that Block. 

- All Data Block Symbols are scrambled and advance the LFSRs. 

- Symbols are scrambled in little‐endian order, meaning the least‐significant bit is scrambled first and the most‐significant bit is scrambled last. 

- The seed value for a per‐Lane LFSR depends on the Lane number assigned to the Lane when the LTSSM first entered Configuration.Idle (having fin‐ ished the Polling state). The seed values, modulo 8, are shown in Table 12‐3 on page 432 and, once assigned, won’t change as long LinkUp = 1 even if Lane assignments are changed by going back to the Configuration state. 

- Unlike 8b/10b, scrambling cannot be disabled while using 128b/130b encod‐ ing because it is needed to help with signal integrity. It’s not expected that the Link would operate reliably without it, so it must always be on. 

- A Loopback Slave must not scramble or de‐scramble the looped‐back bit. 

## **Serializer** 

This shift register works like it does for Gen1/Gen2 data rates except that it is now receiving 8 bits at a time instead of 10 (i.e., the serializer is an 8‐bit parallel to serial shift register). 

**434** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **Mux for Sync Header Bits** 

Finally, the two Sync Header bits must be injected to distinguish the next Block of characters as a Data Block or an Ordered Set Block. These are the first two bits of each 130‐bit Block and the logic for them could be added anywhere in the transmitter that makes sense for the design. In this example the bits are injected at the end of the process for simplicity. Wherever they are included, the flow of bytes from above must be stalled to allow time for them. In this example there will need to be a way to inform the logic above to pause for two bit times. The flow of incoming packets will just be queued in the Tx Buffer during the time the Sync bits are being sent. 

## **Gen3 Physical Layer Receive Logic** 

As in the earlier generations, the Receiver’s logic, shown in Figure 12‐18 on page 436, begins with the CDR (Clock and Data Recovery) circuit. This probably includes a PLL that locks onto the frequency of the Transmitter clock based on knowledge of the expected frequency and the edges in the bit stream to gener‐ ate a recovered clock (Rx Clock). This recovered clock latches the incoming bits into a deserializing buffer and then, once Block Alignment has been established (during the Recovery state of the LTSSM), another version of the recovered clock that is divided by 8.125 (Rx Clock/8.125) latches the 8‐bit Symbols into the Elastic Buffer. After that, the de‐scrambler recreates the original data from the scrambled characters. The bytes bypass the 8b/10b decoder and are delivered directly to the Byte Un‐striping logic. Finally, the Ordered Sets are filtered out, and the remaining byte stream of TLPs and DLLPs is forwarded up to the Data Link Layer. 

In the following discussion, each part is described working upward from the bottom. The focus is on describing aspects of the Physical Layer changed for 8.0 GT/s. Sub‐block unchanged from Gen1/Gen2 will not be described in this sec‐ tion. 

## **Differential Receiver** 

The differential receiver logic is unchanged, but there are electrical changes to improve signal integrity (see “Signal Compensation” on page 468), as well as training changes to establish signal equalization, which are covered in “Link Equalization Overview” on page 577. 

**435** 

## **PCI Ex ress Technolo p gy** 

_Figure 12‐18: Gen3 Physical Layer Receiver Details_ 

**==> picture [276 x 369] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


**436** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐19: Gen3 CDR Logic_ 

**==> picture [385 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

块对齐 块类型<br>
& 块类型 控制<br>
检测逻辑 字符<br>
解串行化 通道<br>
寄存器 弹性 去偏斜<br>
缓冲区 延迟<br>
8 8 电路<br>
控制 本地<br>
串行<br>
时钟<br>
流<br>
PLL<br>
Rx<br>
D+<br>
时钟<br>
Rx 时钟<br>
差分<br>
恢复<br>
D- 接收器 Rx 时钟 / 8.125<br>
串行位 PLL<br>
流<br>
a     b     c     d     e     f     g     h     a<br>
**----- 图片文字结束 -----**<br>


## **CDR（时钟和数据恢复）逻辑 (CDR (Clock and Data Recovery) Logic)**

## **Rx 时钟恢复 (Rx Clock Recovery)**

尽管新的加扰方案有助于时钟恢复，但它不能保证短间隔内的良好转换密度。因此，CDR 逻辑现在必须能够在没有那么多边沿的情况下保持更长时间的同步。规范中没有给出完成此操作的具体方法，但可能需要更稳健的 PLL（锁相环，Phase-Locked Loop）或 DLL（延迟锁定环，Delay-Locked Loop）电路。

CDR 逻辑现在不同的另一个方面是，弹性缓冲区使用的内部时钟并不像人们预期的那样只是 Rx 时钟除以 8。原因当然是输入不是规则的 8 位字节倍数。相反，它是 2 位 Sync Header 后跟 16 个字节。这额外的两位必须在某处考虑。规范不要求任何特定的实现，但一种解决方案如图 12-19（第 437 页）所示，时钟除以 8.125，以在 130 个位时间内产生 16 个时钟边沿。

**437**

**PCI Ex ress Technolo p gy**

然后可以使用块类型检测逻辑从解串器中取出它无论如何都需要检查的多余两位，当达到块边界时间时，确保只有 8 位字节被传递到弹性缓冲区。

为了在本讨论中解决所有悬而未决的问题，8.0 GT/s 数据速率的内部时钟实际上是 8.0 GHz / 8.125 = 0.985 GHz。这导致略低于通常用于描述 Gen3 带宽的 1.0 GB/s 数据速率，但差异足够小（比 1 GB/s 低 1.5%），通常不会提及。

## **解串器 (Deserializer)**

传入数据由恢复的 Rx 时钟定时送入每个通道的串行转并行转换器，如图 12-19（第 437 页）所示。8 位字符被发送到弹性缓冲区，并通过 Rx 时钟除以 8.125 的版本被送入弹性缓冲区，以正确容纳 130 位中的 16 个字节。

## **实现块对齐 (Achieving Block Alignment)**

训练期间发送的 EIEOS 用于标识 130 位块的边界。如第 438 页图 12-20 所示，可以通过在位流中将其识别为交替的 00h 和 FFh 字节模式来识别此有序集合。当看到此模式时，EIEOS 的最后一个字符被解释为块边界，并且测试下一个 130 位将揭示边界是否正确。如果不正确，则逻辑继续搜索此模式。规范将此过程描述为分三个阶段进行：未对齐 (Unaligned)、已对齐 (Aligned) 和锁定 (Locked)。

_图 12-20：EIEOS 字符模式_

**==> 图片 [75 x 137] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
0 00000000<br>
1 11111111<br>
2 00000000<br>
3 11111111<br>
4 00000000<br>
13 11111111<br>
14 00000000<br>
15 11111111<br>
**----- 图片文字结束 -----**<br>


**438**

**第 12 章：物理层 - 逻辑 (Gen3)**

**未对齐阶段 (Unaligned Phase)。** 接收器在电气空闲期之后进入此阶段，例如在更改为 8.0 GT/s 或退出低功耗链路状态之后。在此阶段，块对齐逻辑监视 EIEOS 的到达，因为交替字节的结束必须对应于块的结束。当看到 EIEOS 时，调整对齐，逻辑进入下一阶段。在此之前，它还必须根据任何 SOS 的到达调整其块对齐。

**已对齐阶段 (Aligned Phase)。** 在此阶段，接收器继续监视 EIEOS，并在必要时根据其看到的位和块对齐进行调整。但是，由于它们已经暂时标识了块边界，它们现在还可以搜索 SDS（数据流开始，Start of Data Stream）有序集合以指示数据流的开始。当看到 SDS 时，接收器进入锁定阶段。在此之前，它还必须根据 SOS 的到达调整其块对齐。如果检测到未定义的 Sync Header（值为 00b 或 11b），则允许接收器返回到未对齐阶段。规范指出，这在链路训练期间 EIEOS 后跟 TS 有序集合时会发生。

**锁定阶段 (Locked Phase)。** 一旦接收器到达此阶段，它就不再调整其块对齐。相反，它现在期望在 SDS 之后看到数据块，如果此时必须重新调整对齐，则一些未对齐的数据可能会丢失。如果检测到未定义的 Sync Header，则允许接收器返回到未对齐或已对齐阶段。只要停止数据流处理，就可以将接收器从锁定阶段转换到另一个阶段（有关数据流的规则，请参见第 413 页的"数据流和数据块 (Data Stream and Data Blocks)"）。

**特殊情况：Loopback。** 在讨论块对齐时，规范描述了链路处于 Loopback 模式时会发生什么。Loopback Master 必须能够在 Loopback 期间调整对齐，并且允许发送 EIEOS 并基于 Loopback.Active 期间回送的检测到的 EIEOS 调整其接收器。Loopback Slave 必须能够在 Loopback.Entry 期间调整对齐，但在 Loopback.Active 期间不得调整对齐。当 Slave 开始环回位流时，Slave 的接收器被认为处于锁定阶段。

## **块类型检测 (Block Type Detection)**

一旦实现了块对齐，接收器就可以识别传入块的开始时间并检查前两位以识别两种可能的类型中的哪一种正在传入。有序集合块仅对物理层感兴趣，因此它们不会被转发到更高的层，但数据

**439**

**PCI Ex ress Technolo p gy**

块会被转发。当检测到 Sync Header 时，此信息被发信号到物理层的其他部分，以确定当前块是否应从发送到更高层的字节流中删除。时钟恢复机制和 Sync Header 检测有效地完成了从 130 位到 128 位的转换，这必须在物理层中进行。

请注意，由于块信息对于每个通道都是相同的，此逻辑可以仅为一个通道实现，例如通道 0，如图 12-18（第 436 页）所示。但是，如果支持不同的链路宽度和通道反转 (Lane Reversal)，则需要更多通道包括此逻辑，以确保始终有一个活动通道具有此逻辑可用。一个示例可能是能够作为通道 0 操作的每个通道都将实现它，但只有当前充当通道 0 的那个才会使用它。另请注意，由于规范在这方面未提供详细信息，因此此处讨论和说明的示例只是对可行实现的有根据的猜测。

## **接收器时钟补偿逻辑 (Receiver Clock Compensation Logic)**

## **背景 (Background)**

8.0 GT/s 的时钟要求与早期规范版本相同：两个链路伙伴的时钟必须在中心频率的 +/–300 ppm（百万分之一）以内，这（在最坏情况下）导致每 1666 个时钟之后获得或丢失一个时钟。

## **弹性缓冲区的角色 (Elastic Buffer's Role)**

接收到的字符被定时送入弹性缓冲区，如图 12-21（第 441 页）所示，使用恢复的时钟并使用接收器的本地时钟送出。弹性缓冲区通过添加或移除 SKP 字符来补偿频率差，但现在它一次以四个字符为单位执行此操作，而不是一次一个。当 SKP 有序集合到达时，监视缓冲区状态的控制逻辑进行评估。如果本地时钟运行得更快，则缓冲区将接近下溢条件，逻辑可以通过在 SOS 到达时附加四个额外的 SKP 来快速重新填充缓冲区以进行补偿。另一方面，如果恢复的时钟运行得更快，则缓冲区将接近溢出条件，并且逻辑将通过删除四个 SKP 来补偿，以在看到 SOS 时快速排空缓冲区。

**440**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12-21：Gen3 弹性缓冲区逻辑_

**==> 图片 [383 x 237] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
块对齐 块类型<br>
& 块类型 控制<br>
检测逻辑 字符<br>
解串行化 通道<br>
寄存器 弹性 去偏斜<br>
缓冲区 延迟<br>
8 8 电路<br>
控制 本地<br>
串行<br>
时钟<br>
流<br>
PLL<br>
Rx<br>
D+<br>
时钟<br>
Rx 时钟<br>
差分<br>
恢复<br>
D- 接收器 Rx 时钟 / 8.125<br>
串行位 PLL<br>
流<br>
a     b     c     d     e     f     g     h     a<br>
**----- 图片文字结束 -----**<br>


Gen3 发送器每 370 到 375 个块调度一次 SOS，但与之前一样，它们只能在块边界上发送。如果在调度 SOS 时有数据包正在进行，则它们被累积并在下一个数据包边界插入。但是，与较低的数据速率不同，在 8.0 GT/s 下不允许两个连续的 SOS；它们必须由数据块分隔。接收器必须能够容忍由设备支持的最大数据包有效负载大小分隔的 SOS。

调整仅以 4 个字符为增量进行这一事实可能会影响弹性缓冲区的深度，因为需要看到 4 的差异才能应用任何补偿，并且一个大的数据包可能在本应适当的时间正在进行。因此，在确定此缓冲区的最佳大小时需要小心，让我们考虑一个示例。375 个块的允许 SOS 间隔时间，每个块 16 个字符，等于 6000 个字符时间。将其除以最坏情况的 1666 个时钟的获得或丢失时间意味着在该时间段内可能获得或丢失 3.6 个时钟。如果最大可能的 TLP（4KB）刚在下一次发送 SOS 之前开始，则其总延迟变为大约 6000 + 4096 = 10096 字符时间（对于 x1 链路），这转化为 10096 / 1666 = 6.06 个时钟的获得或丢失。因

**441**

**PCI Ex ress Technolo p gy**

此，如果支持 4KB 大小的 TLP，则缓冲区可能设计为在保证 SOS 到达之前处理多 7 个或少 7 个字符。可能在第一个 SOS 发送之前调度了两个 SOS。在较低的数据速率下，排队的 SOS 是背靠背发送的，但对于 8.0 GT/s，它们不是，并且必须由数据块分隔。每当 SOS 到达接收器时，它可以添加或移除 4 个 SKP 字符以快速填充或排空缓冲区并避免出现问题。

## **通道间偏斜 (Lane-to-Lane Skew)**

## **通道间飞行时间差异 (Flight Time Variance Between Lanes)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-6"></a>
## 10.6 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Block Alignment Block Type<br>& Block Type  Control<br>Detect Logic Sym bols<br>De-Serializing Lane<br>Register Elastic De-skew<br>Buffer Delay<br>8 8 Circuit<br>Control Local<br>Serial<br>Clock<br>Stream<br>PLL<br>Rx<br>D+<br>Clock<br>Rx Clock<br>Differential<br>Recovery<br>D- Receiver Rx Clock / 8.125<br>Serial Bit PLL<br>Stream<br>a     b     c     d     e     f     g     ha<br>**----- End of picture text -----**<br>


## **CDR (Clock and Data Recovery) Logic** 

## **Rx Clock Recovery** 

Although the new scrambling scheme helps with clock recovery, it doesn’t guar‐ antee good transition density over short intervals. As a result, the CDR logic must now be able to maintain synchronization for longer periods without as many edges. No specific method for accomplishing this is given in the spec, but a more robust PLL (Phase‐Locked Loop) or DLL (Delay‐Locked Loop) circuit will likely be needed. 

Another aspect of the CDR logic that’s different now is that the internal clock used by the Elastic Buffer is not simply the Rx clock divided by 8 as one might expect. The reason, of course, is that the input is not a regular multiple of 8‐bit bytes. Instead, it is a 2‐bit Sync Header followed by 16 bytes. Those extra two bits must be accounted for somewhere. The spec doesn’t require any particular implementation, but one solution would have the clock divided by 8.125, as shown in Figure 12‐19 on page 437, to produce 16 clock edges over 130 bit times. 

**437** 

**PCI Ex ress Technolo p gy** 

The Block Type Detection logic might then be used to take the extra two bits out of the deserializer that it needs to examine anyway, when a block boundary time is reached, ensuring that only 8‐bit bytes are delivered to the Elastic Buffer. 

Just to tie up all the loose ends on this discussion, the internal clock for the 8.0 GT/s data rate will actually be 8.0 GHz / 8.125 = 0.985 GHz. That results in slightly less than the 1.0 GB/s data rate that’s usually used to describe the Gen3 bandwidth, but the difference is small enough (1.5% less than 1 GB/s) that it usually isn’t mentioned. 

## **Deserializer** 

The incoming data is clocked into each Lane’s serial‐to‐parallel converter by the recovered Rx clock, as shown in Figure 12‐19 on page 437. The 8‐bit Symbols are sent to the Elastic Buffer and clocked into the Elastic Buffer by a version of the Rx Clock that has been divided by 8.125 to properly accommodate 16 bytes in 130 bits. 

## **Achieving Block Alignment** 

The EIEOSs sent during training serve to identify boundaries for the 130‐bit blocks. As shown in Figure 12‐20 on page 438, this Ordered Set can be recog‐ nized in a bit stream because it appears as a pattern of alternating bytes of 00h and FFh. When this pattern is seen, the last Symbol of the EIEOS is interpreted as the Block boundary, and testing the next 130 bits will reveal whether the boundary is correct. If not, the logic continues to search for this pattern. This process is described in the spec as occurring in three phases: Unaligned, Aligned, and Locked. 

_Figure 12‐20: EIEOS Symbol Pattern_ 

**==> picture [75 x 137] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


**438** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

**Unaligned Phase.** Receivers enter this phase after a period of Electrical Idle, such as after changing to 8.0 GT/s or exiting from a low‐power Link state. In this phase, the Block Alignment logic watches for the arrival of an EIEOS, since the end of the alternating bytes must correspond to the end of the Block. When an EIEOS is seen, the alignment is adjusted and the logic proceeds to the next phase. Until then, it must also adjust its Block align‐ ment based on the arrival of any SOS. 

**Aligned Phase.** In this phase Receivers continues to monitor for EIEOS and make any necessary adjustments to their bit and Block alignment if they see one. However, since they’ve tentatively identified block boundaries they can also now search for an SDS (Start of Data Stream) Ordered Set to indicate the beginning of a Data Stream. When an SDS is seen, the receiver proceeds to the Locked phase. Until then, it must also adjust its Block align‐ ment based on the arrival of SOSs. If an undefined Sync Header is detected (value of 00b or 11b) the Receiver is allowed to return to the Unaligned phase. The spec notes that this will happen during Link training when EIEOS is followed by a TS Ordered Set. 

**Locked Phase.** Once a Receiver reaches this phase, it no longer adjusts its Block alignment. Instead, it now expects to see a Data Block after the SDS and if the alignment has to be readjusted at this point, some misaligned data will probably be lost. If an undefined Sync Header is detected the Receiver is allowed to return to the Unaligned or Aligned phase. Receivers can be directed to transition out of the Locked phase to one of the others as long as Data Stream processing is stopped (see “Data Stream and Data Blocks” on page 413 for the rules regarding Data Streams). 

**Special Case: Loopback.** While discussing Block alignment, the spec describes what happens when the Link is in Loopback mode. The Loopback Master must be able to adjust alignment during Loopback, and is allowed to send EIEOS and adjust its Receiver based on a detected EIEOS when they are echoed back during Loopback.Active. The Loopback Slave must be able to adjust alignment during Loopback.Entry but must not adjust alignment during Loopback.Active. The Slave’s Receiver is considered to be in the Locked phase when the Slave begins to loop back the bit stream. 

## **Block Type Detection** 

Once Block Alignment has been achieved, the Receiver can recognize the start times of the incoming blocks and examine the first two bits to identify which of the two possible types are coming in. Ordered Set Blocks are only interesting to the Physical Layer, so they’re not forwarded to the higher layers, but Data 

**439** 

**PCI Ex ress Technolo p gy** 

Blocks do get forwarded. When the Sync Header is detected, this information is signaled to other parts of the Physical Layer to determine whether the current block should be removed from the byte stream going to the higher layers. The clock recovery mechanism and Sync Header detection effectively accomplishes the conversion from 130 bits to 128 bits that must take place in the Physical Layer. 

Note that since the block information is the same for every Lane, this logic may simply be implemented for only one Lane, such as Lane 0 as shown in Figure 12‐18 on page 436. However, if different Link widths and Lane Reversal were supported then more Lanes would need to include this logic to ensure that there would always be one active Lane with this logic available. An example might be that every Lane which is able to operate as Lane 0 would implement it, but only the one that was currently acting as Lane 0 would use it. Note also that, since the spec doesn’t give details in this regard, the examples discussed and illus‐ trated here are only educated guesses at a workable implementation. 

## **Receiver Clock Compensation Logic** 

## **Background** 

The clock requirements for 8.0 GT/s are the same as they were in the earlier spec versions: the clocks of both Link partners must be within +/– 300 ppm (parts per million) of the center frequency, which results (in the worst case) in gaining or losing one clock after every 1666 clocks. 

## **Elastic Buffer’s Role** 

The received Symbols are clocked into the elastic buffer, as shown in Figure 12‐ 21 on page 441, using the recovered clock and clocked out using the receiver’s local clock. The Elastic Buffer compensates for the frequency difference by add‐ ing or removing SKP Symbols as before, but now it does so four Symbols at a time instead of only one at a time. When a SKP Ordered Set arrives, control logic watching the status of the buffer makes an evaluation. If the local clock is running faster, the buffer will be approaching an underflow condition and the logic can compensate by appending four extra SKPs when the SOS arrives to quickly refill the buffer. On the other hand, if the recovered clock is running faster, the buffer will be approaching an overflow condition and the logic will compensate for that by deleting four SKPs to quickly drain the buffer when an SOS is seen. 

**440** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐21: Gen3 Elastic Buffer Logic_ 

**==> picture [383 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
Block Alignment Block Type<br>& Block Type  Control<br>Detect Logic Sym bols<br>De-Serializing Lane<br>Register Elastic De-skew<br>Buffer Delay<br>8 8 Circuit<br>Control Local<br>Serial<br>Clock<br>Stream<br>PLL<br>Rx<br>D+<br>Clock<br>Rx Clock<br>Differential<br>Recovery<br>D- Receiver Rx Clock / 8.125<br>Serial Bit PLL<br>Stream<br>a     b     c     d     e     f     g     ha<br>**----- End of picture text -----**<br>


Gen3 Transmitters schedule an SOS once every 370 to 375 blocks but, as before, they can only be sent on block boundaries. If a packet is in progress when SOSs are scheduled, they are accumulated and inserted at the next packet boundary. However, unlike the lower data rates, two consecutive SOSs are not allowed at 8.0 GT/s; they must be separated by a Data Block. Receivers must be able to tol‐ erate SOSs separated by the maximum packet payload size a device supports. 

The fact that adjustments are only made in increments of 4 Symbols may affect the depth of the Elastic Buffer, since a difference of 4 would need to be seen before any compensation is applied, and a large packet may be in progress at what would otherwise be the appropriate time. For that reason, care will need to be exercised in determining the optimal size of this buffer, so let’s consider an example. The allowed time between SOSs of 375 blocks at 16 Symbols per block equals 6000 Symbol times. Dividing that by the worst‐case time to gain or lose a clock of 1666 means that 3.6 clocks could be gained or lost during that period. If the largest possible TLP (4KB) had started just prior to the next SOS being sent, the overall delay for it becomes about 6000 + 4096 = 10096 Symbol times for a x1 Link, which translates to a gain or loss of 10096 / 1666 = 6.06 clocks. Conse‐ 

**441** 

**PCI Ex ress Technolo p gy** 

quently, if TLPs of 4KB in size are supported, the buffer might be designed to handle 7 Symbols too many or too few before an SOS is guaranteed to arrive. It may happen that two SOSs are scheduled before the first one is sent. At the lower data rates, the queued SOSs are sent back‐to‐back, but for 8.0 GT/s they are not and must be separated by a Data Block. Whenever an SOS does arrive at the Receiver, it can add or remove 4 SKP Symbols to quickly fill or drain the buffer and avoid a problem. 

## **Lane-to-Lane Skew** 

## **Flight Time Variance Between Lanes**

</td>
<td style="background-color:#e8e8e8">

对于多通道链路，通道之间的到达时间差异由接收器通过延迟早到达的通道直到它们全部匹配来自动纠正。规范允许通过设计者喜欢的任何方式来完成此操作，但在弹性缓冲区之后使用数字延迟具有一个优点，即到达时间差异现在已通过接收器的本地字符时钟数字化。如果一个通道的输入在一个时钟边沿上到达而另一个没有，则它们之间的差异将以时钟周期为单位测量，因此早到达可以简单地延迟适当数量的时钟以使其与晚到达者对齐（参见第 444 页图 12-22）。接收器处的最大允许偏斜是时钟周期的倍数这一事实使其变得容易，并暗示规范编写者可能已经在考虑这样的实现。如规范中定义的，接收器必须能够对 Gen1 进行高达 20ns 的去偏斜（5 个字符时间时钟，每个字符 4ns），对 Gen2 进行 8ns（4 个字符时间时钟，每个字符 2ns），对 Gen3 进行 6ns（6 个字符时间时钟，每个字符 1ns）。

## **去偏斜机会 (De-skew Opportunities)**

必须在所有通道上同时看到相同的字符才能执行去偏斜，任何有序集合都可以。但是，去偏斜仅在 L0s、Recovery 和 Configuration LTSSM 状态下执行。特别是，必须完成以下条件：

- 离开 Configuration.Complete

- 在离开 Configuration.Idle 或 Recovery.Idle 后开始处理数据流

- 离开 Recovery.RcvrCfg

- 离开 Rx_L0s.FTS

**442**

**第 12 章：物理层 - 逻辑 (Gen3)**

如果在 L0 中偏斜值发生变化（例如基于温度或电压变化），则可能发生接收器错误并导致 TLP 被重传。如果问题变得持续存在，链路最终将转换到 Recovery 状态并在那里执行去偏斜。规范指出，虽然设备不允许在 L0 中对其通道进行去偏斜，但在此状态下必须定期发送的 SOS 包含旨在帮助外部工具执行此操作的 LFSR 值。这些工具不受数据流规则的约束，可以在数据流中搜索 SOS 并使用这些模式来实现位锁定、块对齐和通道间去偏斜。

规范指出，在离开 L0s 时，发送器将发送 EIEOS，然后发送正确数量的 FTS，在每 32 个 FTS 之后插入另一个 EIEOS，然后发送最后一个 EIEOS 以帮助块对齐，最后，发送 SDS 有序集合用于去偏斜以及启动数据流。

## **接收器通道间去偏斜能力 (Receiver Lane-to-Lane De-skew Capability)**

可以理解的是，发送器只允许引入最少的偏斜，以便将偏斜预算的其余部分留给路由差异和其他变化。可以在接收器处纠正的允许偏斜量如表 12-5（第 443 页）所示，其中可以看出此偏斜对应于 Gen3 的字符时间数，就像早期数据速率一样。这允许使用延迟寄存器在使用延迟寄存器在弹性缓冲区之后完成去偏斜的相同选项，如早期 Gen1/Gen2 物理层实现中所述。

_表 12-5：信号偏斜参数_

||Gen1|Gen2|Gen3|
|---|---|---|---|
|Tx 最大偏斜|1.3 ns|1.3 ns|1.1 ns|
|Rx 最大偏斜|20 ns|8 ns|6 ns|
|字符时间周期|4ns|2ns|1ns|
|以字符时间表示<br>的 Rx 偏斜|5|4|6|

当使用 8b/10b 编码时，明确的去偏斜机制是监视 COM 控制字符，该字符必须同时出现在所有通道上。128b/130b 不提供此选项，但有序集合仍然同时到达所有通道，例如 SOS、SDS 和 EIEOS。因此，该过程可以非常相似，即使在去偏斜通道时搜索的模式不同。

**443**

**PCI Ex ress Technolo p gy**

_图 12-22：接收器链路去偏斜逻辑_

**==> 图片 [374 x 239] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
SOS, SDS, SOS, SDS,<br>
通道 0 Rx EIEOS 延迟 EIEOS<br>
（字符）<br>
SOS, SDS, SOS, SDS,<br>
通道 1 Rx EIEOS 延迟 EIEOS<br>
（字符）<br>
SOS, SDS, SOS, SDS,<br>
通道 2 Rx EIEOS 延迟 EIEOS<br>
（字符）<br>
SOS, SDS, SOS, SDS,<br>
EIEOS EIEOS<br>
通道 3 Rx 延迟<br>
（字符）<br>
SYNC SYNC<br>
SYNC SYNC<br>
SYNC SYNC<br>
SYNC SYNC<br>
**----- 图片文字结束 -----**<br>


## **解扰器 (Descrambler)**

## **概述 (General)**

接收器完全遵循与发送器相同的规则来生成加扰多项式，并简单地将相同的值再次 XOR 到输入数据以恢复原始信息。与发送端一样，它们允许为每个通道实现单独的 LFSR 或仅一个。

## **禁用解扰 (Disabling Descrambling)**

与 Gen1/Gen2 数据速率不同，在 Gen3 模式下，无法禁用解扰，因为它在促进时钟恢复和信号完整性方面发挥作用。在较低的速率下，TS1 和 TS2 控制字节中的"禁用加扰 (disable scrambling)"位用于通知链路邻居加扰已关闭。该位保留用于 8.0 GT/s 及更高的速率。

**444**

**第 12 章：物理层 - 逻辑 (Gen3)**

## **字节解交错 (Byte Un-Striping)**

此逻辑基本上与 Gen1 或 Gen2 实现相同。在某个时候，Gen3 和较低数据速率的字节流必须被多路复用在一起，图 12-23（第 445 页）中的示例显示了在解交错逻辑之前发生这种情况。

_图 12-23：物理层接收逻辑详细信息_

**==> 图片 [272 x 358] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
到数据链路层<br>
eceiTLP/DLLP 指示符<br>
N*8<br>
Rx<br>
缓冲区<br>
TLP/DLLP<br>
N*8 指示符<br>
数据包<br>
过滤<br>
块<br>
N*8 D/K# 类型<br>
通道 0 字节解交错 通道 N<br>
8 8<br>
Mux Mux<br>
8 8 8 8<br>
D/K# D/K#<br>
Gen3 解扰器 Gen3 解扰器<br>
解扰器 解扰器<br>
8 8 D/K# 8 8 D/K#<br>
8b/10b 8b/10b<br>
解码器 解码器<br>
Gen3 Gen3<br>
10 块 10 块<br>
类型 类型<br>
CDR 逻辑 CDR 逻辑<br>
Rx Rx<br>
通道 0 通道 1, ..,N-1 通道 N<br>
**----- 图片文字结束 -----**<br>


**445**

**PCI Ex ress Technolo p gy**

## **数据包过滤 (Packet Filtering)**

由字节解交错逻辑提供的串行字节流包含 TLP、DLLP、逻辑空闲 (IDL) 和有序集合。逻辑空闲字节和有序集合在此处被消除，不会转发到数据链路层。剩下的是 TLP 和 DLLP，它们与其数据包类型的指示符一起被转发。

## **接收缓冲区 (Rx Buffer)**

Rx 缓冲区保存接收到的 TLP 和 DLLP，直到数据链路层能够接受它们为止。与数据链路层的接口未在规范中描述，因此设计人员可以自由选择此类总线的宽度等细节。路径越宽，时钟频率越低，但需要更多信号和逻辑来支持它。

## **有关 Loopback 与 128b/130b 的注意事项 (Notes Regarding Loopback with 128b/130b)**

规范特别指出在更高速度下 Loopback 模式的操作。基本规则可总结如下：

- Loopback masters 必须发送实际的有序集合或数据块，但它们在从数据块更改为有序集合或反之亦然时不需要遵循正常的协议规则。换句话说，不需要 SDS 有序集合和 EDS 令牌。Slaves 不得期望或检查它们的存在。

- Masters 必须照常发送 SOS，并且必须允许环回流中的 SKP 字符数不同，因为接收器将执行时钟补偿。

- Loopback slaves 被允许通过一次添加或删除 4 个 SKP 字符来修改 SOS，就像它们通常为时钟补偿所做的那样，但生成的 SOS 必须仍然遵循正确的格式规则。

- 除了 SOS 可能如刚刚描述的那样更改，以及 EIEOS 和 EIOS 在环回中具有已定义的用途并且应避免之外，其他所有内容都应按原样环回发送。

- 如果 slave 无法获取块对齐，则它将无法按接收的方式环回所有位，并且可以添加或删除所需的字符以继续操作。

**446**

## _**13 物理层 - 电气 (Physical Layer - Electrical)**_

## **上一章 (The Previous Chapter)**

上一章描述了 PCIe 第三代（Gen3）的逻辑物理层特性。主要变化包括能够在不使频率翻倍的情况下将带宽相对于 Gen2 速度翻倍（链路速度从 5 GT/s 到 8 GT/s）。这是通过在 Gen3 模式下消除 8b/10b 编码来实现的。在 Gen3 速度下需要更稳健的信号补偿。进行这些更改比预期的更复杂。

## **本章 (This Chapter)**

本章描述了链路物理层电气接口，包括差分发送器和接收器的一些低级特性。对信号均衡的需求以及用于实现它的方法也将在此处讨论。本章结合了 Gen1、Gen2 和 Gen3 速度的电气发送器和接收器特性。

## **下一章 (The Next Chapter)**

下一章描述了物理层链路训练和状态状态机 (LTSSM) 的操作。链路的初始化过程从 Power-On 或 Reset 描述到链路在正常数据包流量期间达到完全运行的 L0 状态。此外，链路电源管理状态 L0s、L1、L2、L3 与状态之间转换的原因一起讨论。Recovery 状态期间可以重新建立位锁定、字符锁定或块锁定。

**447**

**PCI Ex ress Technolo p gy**

## **向后兼容性 (Backward Compatibility)**

规范以观察到较新的数据速率需要与较旧的速率向后兼容开始了物理层电气部分。以下摘要定义了要求：

- 所有设备的初始训练都以 2.5 GT/s 完成。

- 更改为其他速率需要链路伙伴之间的协商以确定峰值公共频率。

- 支持 8.0 GT/s 的根端口需要同时支持 2.5 和 5.0 GT/s。

- 下游设备显然必须支持 2.5 GT/s，但所有更高的速率都是可选的。这意味着 8 GT/s 设备不需要支持 5 GT/s。

此外，可选的参考时钟 (Refclk) 无论数据速率如何都保持不变，并且不需要改进的抖动特性来支持更高的速率。

尽管有这些相似之处，规范确实描述了 8.0 GT/s 速率的一些变化：

- **ESD 标准：** 早期 PCIe 版本要求所有信号和电源引脚承受一定级别的 ESD（静电放电），3.0 规范也是如此。区别在于列出了更多 JEDEC 标准，并且规范指出它们适用于设备，无论它们支持哪些速率。

- **Rx 断电阻抗 (Rx powered-off Resistance)：** 为 8.0 GT/s 指定的新阻抗值（ZRX-HIGH-IMP-DC-POS 和 ZRX-HIGH-IMP-DC-NEG）也将应用于支持 2.5 和 5.0 GT/s 的设备。

- **Tx 均衡容差 (Tx Equalization Tolerance)：** 将先前规范的 Tx 去加重值容差从 +/‐ 0.5 dB 放宽到 +/‐ 1.0 dB，使 ‐3.5 和 ‐6.0 dB 去加重容差在所有三个数据速率中保持一致。

- **Tx Margining 期间的 Tx 均衡：** 在早期规范中，此情况的去加重容差已经放宽到 +/‐ 1.0 dB。8.0 GT/s 的精度由 Tx 系数粒度和发送器在正常操作期间的 TxEQ 容差决定。

- **VTX-ACCM 和 VRX-ACCM：** 对于 2.5 和 5.0 GT/s，这些放宽到发送器为 150 mVPP，接收器为 300 mVPP。

**448**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-7"></a>
## 10.7 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

For multi‐Lane Links, the difference in arrival times between lanes is automati‐ cally corrected at the Receiver by delaying the early arrivals until they all match up. The spec allows this to be accomplished by any means a designer prefers, but using a digital delay after the elastic buffer has one advantage in that the arrival time differences are now digitized to the local Symbol clock of the receiver. If the input to one lane makes it on a clock edge and another one doesn’t, the difference between them will be measured in clock periods, so the early arrival can simply be delayed by the appropriate number of clocks to get it to line up with the late‐comers (see Figure 12‐22 on page 444). The fact that the maximum allowable skew at the receiver is a multiple of the clock periods makes this easy and infers that the spec writers may have had this implementa‐ tion in mind. As defined in the spec, the receiver must be capable of de‐skewing up to 20ns for Gen1 (5 Symbol‐time clocks at 4ns per Symbol) and 8ns for Gen2 (4 Symbol‐time clocks at 2ns per Symbol), and 6ns for Gen3 (6 Symbol‐time clocks at 1ns per Symbol). 

## **De-skew Opportunities** 

The same Symbol must be seen on all lanes at the same time to perform de‐ skewing, and any Ordered Set will do. However, de‐skewing is only performed in the L0s, Recovery, and Configuration LTSSM states. In particular, it must be completed as a condition for: 

- Leaving Configuration.Complete 

- Beginning to process a Data Stream after leaving Configuration.Idle or Recovery.Idle 

- Leaving Recovery.RcvrCfg 

- Leaving Rx_L0s.FTS 

**442** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

If skew values change while in L0 (based on temperature or voltage changes, for example), a Receiver error may occur and cause replayed TLPs. If the problem becomes persistent, the Link would eventually transition to the Recovery state and de‐skewing would take place there. The spec notes that, while devices are not allowed to de‐skew their Lanes while in L0, the SOSs that must be sent peri‐ odically in this state contain an LFSR value that is intended to aid external tools in doing this. These tools, unconstrained by the rules for Data Streams, can search for the SOSs and use the patterns to achieve Bit Lock, Block Alignment and Lane‐to‐Lane de‐skew in the midst of a Data Stream. 

The spec notes that when leaving L0s the Transmitter will send an EIEOS, then the correct number of FTSs with another EIEOS inserted after every 32 FTSs, then one last EIEOS to assist with Block Alignment and, finally, an SDS Ordered Set for the purpose of de‐skewing in addition to starting the Data Stream. 

## **Receiver Lane-to-Lane De-skew Capability** 

Understandably, the transmitter is only allowed to introduce a minimal amount of skew so as to leave the rest of the skew budget to cover routing differences and other variations. The amount of allowed skew that can be corrected at the Receiver is shown in Table 12‐5 on page 443, where it can be seen that this skew corresponds easily to a number of Symbol times for Gen3 just as it did for the earlier data rates. That allows the same option of using delay registers to accom‐ plish de‐skew after the elastic buffer as was described for Gen1/Gen2 Physical Layer implementations earlier. 

_Table 12‐5: Signal Skew Parameters_ 

||Gen1|Gen2|Gen3|
|---|---|---|---|
|Tx max skew|1.3 ns|1.3 ns|1.1 ns|
|Rx max skew|20 ns|8 ns|6 ns|
|Symbol time period|4ns|2ns|1ns|
|Rx skew expressed<br>in Symbol Times|5|4|6|



When using 8b/10b encoding, an unambiguous de‐skew mechanism is to watch for the COM control character, which must appear on all Lanes simultaneously. That option is not available for 128b/130b, but Ordered Sets still arrive at the same time on all the Lanes, such as the SOS, SDS, and EIEOS. As a result, the process can be very much the same even though the pattern to search for when de‐skewing the Lanes is different. 

**443** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐22: Receiver Link De‐Skew Logic_ 

**==> picture [374 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOS, SDS, SOS, SDS,<br>Lane 0 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>Lane 1 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>Lane 2 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>EIEOS EIEOS<br>Lane 3 Rx Delay<br>(symbols)<br>SYNC SYNC<br>SYNC SYNC<br>SYNC SYNC<br>SYNC SYNC<br>**----- End of picture text -----**<br>


## **Descrambler** 

## **General** 

Receivers follow exactly the same rules for generating the scrambling polyno‐ mial that the Transmitter does and simply XOR the same value to the input data a second time to recover the original information. Like on the transmit side, they are allowed to implement a separate LFSR for each Lane or just one. 

## **Disabling Descrambling** 

Unlike at Gen1/Gen2 data rates, in Gen3 mode, descrambling cannot be dis‐ abled because of its role in facilitating clock recovery and signal integrity. At the lower rates, the “disable scrambling” bit in the control byte of TS1s and TS2s would be used to inform a Link neighbor that scrambling was being turned off. That bit is reserved for rates of 8.0 GT/s and higher. 

**444** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **Byte Un-Striping** 

This logic is basically unchanged from Gen1 or Gen2 implementation. At some point, the byte streams for Gen3 and for the lower data rates will have to muxed together, and the example in Figure 12‐23 on page 445 shows that happening just before the un‐striping logic. 

_Figure 12‐23: Physical Layer Receive Logic Details_ 

**==> picture [272 x 358] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


**445** 

**PCI Ex ress Technolo p gy** 

## **Packet Filtering** 

The serial byte stream supplied by the byte un‐striping logic contains TLPs, DLLPs, Logical Idles (IDLs), and Ordered Sets. The Logical Idle bytes and Ordered Sets are eliminated here and are not forwarded to the Data Link layer. What remains are the TLPs and DLLPs, which get forwarded along with an indicator of their packet type. 

## **Receive Buffer (Rx Buffer)** 

The Rx Buffer holds received TLPs and DLLPs until the Data Link Layer is able to accept them. The interface to the Data Link Layer is not described in the spec, and so a designer is free to choose details like the width of this bus. The wider the path, the lower the clock frequency will be, but more signals and logic will be needed to support it. 

## **Notes Regarding Loopback with 128b/130b** 

The spec makes a special point to describe the operation of Loopback Mode at the higher rate. The basic rules can be summarized as follows: 

- Loopback masters must send actual Ordered Sets or Data Blocks, but they aren’t required to follow the normal protocol rules when changing from Data Blocks to Ordered Sets or vice versa. In other words, the SDS Ordered Set and EDS token are not required. Slaves must not expect or check for the presence of them. 

- Masters must send SOS as usual, and must allow for the number of SKP Symbols in the loopback stream to be different because the receiver will be performing clock compensation. 

- Loopback slaves are allowed to modify the SOS by adding or removing 4 SKP Symbols at a time as they normally would for clock compensa‐ tion, but the resulting SOS must still follow the proper format rules. 

- Everything should be looped back exactly as it was sent except for SOS which can change as just described, and both EIEOS and EIOS which have defined purposes in loopback and should be avoided. 

- If a slave is unable to acquire Block alignment, it won’t be able to loop back all bits as received and is allowed to add or remove Symbols as needed to continue operation. 

**446** 

## _**13 Physical Layer ‐ Electrical**_ 

## **The Previous Chapter** 

The previous chapter describes the logical Physical Layer characteristics for the third generation (Gen3) of PCIe. The major change includes the ability to double the bandwidth relative to Gen2 speed without needing to double the frequency (Link speed goes from 5 GT/s to 8 GT/s). This is accomplished by eliminating 8b/10b encoding when in Gen3 mode. More robust signal compensation is nec‐ essary at Gen3 speed. Making these changes is more complex than might be expected. 

## **This Chapter** 

This chapter describes the Physical Layer electrical interface to the Link, includ‐ ing some low‐level characteristics of the differential Transmitters and Receivers. The need for signal equalization and the methods used to accomplish it are also discussed here. This chapter combines electrical transmitter and receiver char‐ acteristics for both Gen1, Gen2 and Gen3 speeds. 

## **The Next Chapter** 

The next chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process of the Link is described from Power‐On or Reset until the Link reaches the fully‐operational L0 state during which normal packet traffic occurs. In addition, the Link power management states L0s, L1, L2, L3 are discussed along with the causes of transi‐ tions between the states. The Recovery state during which bit lock, symbol lock or block lock can be re‐established is described. 

**447** 

**PCI Ex ress Technolo p gy** 

## **Backward Compatibility** 

The spec begins the Physical Layer Electrical section with the observation that newer data rates need to be backward compatible with the older rates. The fol‐ lowing summary defines the requirements: 

- Initial training is done at 2.5 GT/s for all devices. 

- Changing to other rates requires negotiation between the Link partners to determine the peak common frequency. 

- Root ports that support 8.0 GT/s are required to support both 2.5 and 5.0 GT/s as well. 

- Downstream devices must obviously support 2.5 GT/s, but all higher rates are optional. This means that an 8 GT/s device is not required to support 5 GT/s. 

In addition, the optional Reference clock (Refclk) remains the same regardless of the data rate and does not require improved jitter characteristics to support the higher rates. 

In spite of these similarities, the spec does describe some changes for the 8.0 GT/ s rate: 

- **ESD standards:** Earlier PCIe versions required all signal and power pins to withstand a certain level of ESD (Electro‐Static Discharge) and that’s true for the 3.0 spec, too. The difference is that more JEDEC standards are listed and the spec notes that they apply to devices regardless of which rates they support. 

- **Rx powered‐off Resistance:** The new impedance values specified for 8.0 GT/s (ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG) will be applied to devices supporting 2.5 and 5.0 GT/s as well. 

- **Tx Equalization Tolerance:** Relaxing the previous spec tolerance on the Tx de‐emphasis values from +/‐ 0.5 dB to +/‐ 1.0 dB makes the ‐3.5 and ‐6.0 dB de‐emphasis tolerance consistent across all three data rates. 

- **Tx Equalization during Tx Margining:** The de‐emphasis tolerance was already relaxed to +/‐ 1.0 dB for this case in the earlier specs. The accuracy for 8.0 GT/s is determined by the Tx coefficient granularity and the TxEQ tolerances for the Transmitter during normal operation. 

- **VTX‐ACCM and VRX‐ACCM:** For 2.5 and 5.0 GT/s these are relaxed to 150 mVPP for the Transmitter and 300 mVPP for the Receiver. 

**448**

</td>
<td style="background-color:#e8e8e8">

**第 13 章：物理层 - 电气**

## **组件接口 (Component Interfaces)**

来自不同供应商的组件必须可靠地协同工作，因此指定了一组必须满足的参数。对于 2.5 GT/s，这是隐含的，对于 5.0 GT/s，明确说明，此接口的特性在设备引脚处定义。这允许独立表征组件，而不需要使用任何其他 PCIe 组件。其他接口可以在连接器或其他位置指定，但这些不在基本规范中涵盖，将在外部尺寸规范中描述，例如 _PCI Express Card Electromechanical Spec_。

## **物理层电气概述 (Physical Layer Electrical Overview)**

与每个通道相关联的电气子块，如第 450 页图 13-1 所示，提供到链路的物理接口并包含差分发送器和接收器。发送器通过将位流转换为两个具有相反极性的单端电信号，在每个通道上传递输出字符。接收器比较这两个信号，当差异足够正或足够负时，在内部生成 1 或 0 以表示预期的串行位流到物理层的其余部分。

**449**

## **PCI Ex ress Technolo p gy**

_图 13-1：物理层的电气子块_

**==> 图片 [367 x 241] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
物理层 物理层<br>
Tx Rx Tx Rx<br>
逻辑 逻辑<br>
Tx Rx Tx Rx<br>
电气 电气<br>
链路<br>
Tx+ Tx- Rx+ Rx- CTX Tx- Tx+ Rx- Rx+<br>
CTX<br>
**----- 图片文字结束 -----**<br>


当链路处于 L0 完全运行状态时，驱动器在保持正确的 DC 共模电压的同时施加与逻辑 1 和逻辑 0 相关联的差分电压。接收器将此电压感应为输入流，但如果它低于阈值，则将其理解为表示电气空闲链路条件。当链路被禁用时，或当 ASPM 逻辑将链路置于低功耗链路状态（如 L0s 或 L1）时，进入电气空闲（有关此主题的更多信息，请参见第 736 页的"电气空闲 (Electrical Idle)"）。

设备必须支持每种支持的数据速率所需的发送器均衡方法，以实现足够的信号完整性。去加重应用于 2.5 和 5.0 GT/s，更复杂的均衡过程应用于 8.0 GT/s。这些在第 468 页的"信号补偿 (Signal Compensation)"和第 587 页的"Recovery.Equalization"中更详细地描述。

驱动器和接收器具有短路容限，使 PCIe 附加卡适合热插拔环境中的热插拔事件。连接两个组件的链路通过在线添加电容器进行 AC 耦合，通常位于链路的发送器侧附近。这用于

**450**

**第 13 章：物理层 - 电气**

解耦链路伙伴之间的信号的 DC 部分，这意味着它们不必共享公共电源或接地返回路径，例如当设备通过电缆连接时。图 13-1（第 450 页）说明了电容器 (CTX) 在链路上的放置。

## **高速信号传输 (High Speed Signaling)**

PCIe 的高速信号传输环境由第 451 页图 13-2 中的图表示。这种低压差分信号环境是许多串行传输中常用的方法，其中一个原因是它提供的噪声抑制。影响一个信号的电气噪声也会影响另一个信号，因为它们位于相邻引脚上，并且它们的走线彼此非常接近。由于两个信号都受到影响，如图 13-3（第 452 页）所示，它们之间的差异变化不大，因此在接收器处看不到。

3.0 规范版本的一个设计目标是 8.0 GT/s 速率仍应与现有的标准 FR4 电路板和连接器一起工作，这是通过将编码方案从旧的 8b/10b 更改为新的 128b/130b 模型以保持低频来实现的。这个目标可能会随着下一个速度步骤（Gen4）而改变。

_图 13-2：差分发送器/接收器_

**==> 图片 [384 x 191] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
检测<br>
逻辑<br>
D+ CTX ZTX D+<br>
+<br>
通道方向 发送器一个 接收器<br>
CTX ZTX<br>
-<br>
D- D-<br>
ZTX ZTX ZRX ZRX<br>
VRX-CM = 0 V<br>
VCM<br>
VTX-CM = 0 - 3.6 V<br>
ZTX = ZRX = 50 欧姆 +/- 20%<br>
CTX = 75 - 265 nF (Gen1 和 Gen2)<br>
= 176 - 265 nF (Gen3)<br>
无规范<br>
**----- 图片文字结束 -----**<br>


**451**

## **PCI Ex ress Technolo p gy**

_图 13-3：差分共模噪声抑制_

**==> 图片 [374 x 246] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
D+<br>
D-<br>
参考电压偏移<br>
差分<br>
电压保持<br>
+ 差分 相同<br>
电压<br>
Tx Rx<br>
- +<br>
0 V 0 V<br>
-<br>
单端<br>
电压 单端<br>
电压变化<br>
瞬态噪声<br>
Tx Rx<br>
+ +<br>
Vcm Vcm<br>
- -<br>
差分<br>
电压保持相同<br>
**----- 图片文字结束 -----**<br>


## **时钟要求 (Clock Requirements)**

## **概述 (General)**

对于所有数据速率，发送器和接收器时钟都必须精确到中心频率的 +/‐ 300 ppm（百万分之一）以内。在最坏的情况下，发送器和接收器都可能在相反方向上偏离 300 ppm，导致最大差异为 600 ppm。这种最坏情况模型转化为每 1666 个时钟获得或丢失 1 个时钟，这是接收器时钟补偿逻辑必须考虑的差异。

允许设备从外部源派生其时钟，100 MHz Refclk 在 3.0 规范中仍可选地用于此目的。使用 Refclk 允许两个链路伙伴即使在应用扩频时钟时也容易保持 600 ppm 的精度。

**452**

**第 13 章：物理层 - 电气**

## **SSC（扩频时钟）(SSC (Spread Spectrum Clocking))**

SSC 是一种可选技术，用于在规定范围内缓慢调制时钟频率，以将信号的 EMI（电磁干扰）扩展到一系列频率，而不是允许其全部集中在中心频率。扩展辐射能量有助于设备或系统通过保持在阈值以下来通过政府排放标准，如图 13-4（第 454 页）所示。请注意，信号感兴趣的频率仅为时钟速率的一半，因为需要两个上升时钟边沿在数据上创建一个周期，如图 13-5（第 454 页）所示。例如，2.5 GT/s 速率使用 2.5 GHz 的位时钟，导致走线上的兴趣频率为 1.25 GHz。

规范不要求使用 SCC，但如果支持，则适用以下规则：

- 时钟可以从标称值调制 +0% 到 ‐0.5%（5000 ppm），称为"下扩频 (down spreading)"。规范未指定频率调制包络，但如图 13-6（第 455 页）所示的锯齿波模式会产生良好的结果。请注意，下扩频存在权衡，因为平均时钟频率现在将比没有 SSC 时低 0.25%，导致性能略有下降。

- 调制速率必须在 30KHz 和 33KHz 之间。

- 时钟频率精度的 +/‐ 300 ppm 要求仍然有效，因此链路伙伴之间的最大 600 ppm 变化也是如此。规范声明，大多数实现将要求两个链路伙伴使用相同的时钟源，尽管这不是必需的。一种方法可能是它们都使用调制版本的 Refclk 来派生自己的时钟（参见第 456 页的"公共 Refclk (Common Refclk)"）。

**453**

**PCI Ex ress Technolo p gy**

_图 13-4：SSC 动机_

**==> 图片 [324 x 211] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
EMI 功率阈值<br>
普通信号<br>
扩频<br>
信号<br>
范围 = 0.5%<br>
信号<br>
频率<br>
频率 (GHz)<br>
发射功率 (dB)<br>
**----- 图片文字结束 -----**<br>


_图 13-5：信号速率小于时钟速率的一半_

**==> 图片 [384 x 120] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
线上的<br>
信号<br>
Tx 时钟<br>
**----- 图片文字结束 -----**<br>


**454**

**第 13 章：物理层 - 电气**

_图 13-6：SSC 调制示例_

**==> 图片 [274 x 147] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
标称<br>
标称 - 0.5%<br>
时间<br>
调制周期/2 调制周期<br>
频率<br>
**----- 图片文字结束 -----**<br>


## **Refclk 概述 (Refclk Overview)**

接收器必须生成自己的时钟来操作其内部逻辑，但对于为输入位流生成恢复的时钟有一些选项。其详细信息已随规范的每个后续版本而发展，并基于数据速率。

## **2.5 GT/s**

在使用 2.5 GT/s 速率的早期规范版本中，有关可选 Refclk 的信息不包括在基本规范中，而是包括在 PCIe 的单独 CEM（Card Electro-Mechanical）规范中。在那里指定了许多参数，并将一些通用术语延续到规范的较新版本。Refclk 被描述为驱动 100 Ω 差分负载（+/‐ 10%）的 100 MHz 差分时钟，走线长度限制为 4 英寸。如第 453 页的"SSC（扩频时钟）(SSC (Spread Spectrum Clocking))"所述，允许 SSC。

## **5.0 GT/s**

当开发 5.0 GT/s 速率时，规范编写者选择将 Refclk 信息包括在基本规范的电气部分中，并列出了时钟架构的三个选项：

**455**

**PCI Ex ress Technolo p gy**

**公共 Refclk (Common Refclk)。** 描述的第一种架构是两个链路伙伴都使用相同的 Refclk，如图 13-7（第 456 页）所示。此实现有三个明显的优点：

- 首先，与参考时钟相关联的抖动对于 Tx 和 Rx 是相同的，因此被固有地跟踪和考虑。

- – 其次，SSC 的使用在此模型中最简单，因为如果两者都遵循相同的调制参考，则维持 Tx 和 Rx 时钟之间的 600 ppm 间隔很容易。

- 第三，Refclk 在低功耗链路状态 L0s 和 L1 期间仍然可用，这允许接收器的 CDR 保持恢复时钟的相似性，即使在没有位流提供数据中的边沿的情况下也是如此。反过来，这使得本地 PLL 不像它们本来那样漂移，从而导致与其他时钟选项相比恢复到 L0 的时间减少。

_图 13-7：共享 Refclk 架构_

**==> 图片 [374 x 138] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+<br>
Tx 通道方向 接收器<br>
寄存器 Tx 一个 Rx 寄存器<br>
-<br>
CDR<br>
PLL<br>
PLL<br>
Refclk<br>
**----- 图片文字结束 -----**<br>


**数据时钟 Rx 架构 (Data Clocked Rx Architecture)。** 在此时钟架构中，接收器根本不使用参考时钟，而只是从数据流恢复发送器时钟，如图 13-9（第 457 页）所示。这种实现显然是三种中最简单的，因此通常更受欢迎。规范不禁止在此模型中使用 SSC，但这样做会带来两个问题。首先，接收器 CDR 必须保持锁定在输入频率上，因为它通过更宽的范围（5600 ppm 而不是通常的 600 ppm）进行调制，这可能需要更复杂的逻辑。其次，必须保持 600 ppm 的最大时钟频率间隔，并且没有公共参考如何实现这一点也不太清楚。

**456**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
