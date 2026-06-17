# 📘 第 9 章　DLLP 元素 (Chapter 9. DLLP Elements)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0264.md` ... `chunks/chunk0270.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [DLLP Elements](#-本章目录-table-of-contents)

<a id="sec-9-1"></a>
## 9.1 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Now that we’ve described how the protocol works, this is a good time to explain an exception to its general operation. PCIe supports a Switch feature, called ‘cut‐through mode’, that can be used to improve the transfer latency for large TLPs through a Switch. 

**354** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Background** 

Consider an example where a large TLP needs to pass through a Switch as shown in Figure 10‐16 on page 357. Since the Ingress Switch Port can’t tell whether there was an error in the packet until it has seen the whole TLP, it’ll normally store the entire packet and check it for errors before forwarding it to the Egress Port. This store‐and‐forward method works but, for large packets, the latency to get through the Switch can be large which may be an issue for some applications. It would be nice to minimize this latency if possible. 

## **A Latency Improvement Option** 

Since the first part of the TLP contains the header with the routing information for the packet, one option would be to assume that the packet is a good packet and start evaluating the routing info in header even before the entire packet is received. This would allow a Switch to begin forwarding the TLP to the Egress Port as soon as that routing is evaluated. The Egress Port could then go ahead and start sending it out onto its Link, as long as doing so will not cause an underflow condition within the Switch. (A potential underflow case could eas‐ ily happen if the Ingress Port is x1 and the Egress Port is x16. The Egress Port would be sending the packet out much faster than it is being received.) 

Of course, the Ingress Port can’t check for errors in the packet until it receives the LCRC at the end of the packet, so there is a small risk involved that the TLP being forwarded out may actually contain an error. Eventually, the end of the TLP arrives at the Ingress Port and the packet can be checked. If it turns out there was an error, the Ingress Port takes the normal behavior to a bad TLP and simply sends a Nak to have the packet replayed. However, we now have to deal with the problem that most of a packet that we now know is bad has already been forwarded on to the Egress Port. What are our options at this point? We could finish forwarding the packet and wait for a Nak from the neighboring receiver when it sees the error, but the packet in the replay buffer would be the bad one, and so a replay there won’t fix the problem. We might truncate the bad packet in flight, but the spec doesn’t allow for that possibility. To make this work, we need another option, and that’s where the Cut‐Through option comes into play. 

**355** 

**PCI Ex ress Technolo p gy** 

## **Cut-Through Operation** 

Cut‐though mode provides the solution to the forwarding problem described in the previous section: if an error is seen in the incoming packet, the packet that is already on its way out must be ‘ **nullified** ’. 

A **nullified** packet is terminated with an EDB (end bad) symbol instead of an END (end good) symbol and, to make the condition very clear, the TLPs 32‐bit LCRC is inverted (1’s complement) from the original calculated value. In essence, a nullified packet is handled as though it had never existed. On the Switch Egress Port, that means the replay buffer discards the packet and the NEXT_TRANSMIT_SEQ counter is decremented by one (rolled back). 

When a device receives a TLP that it recognizes as being a nullified TLP, it sim‐ ply drops the packet and treats it as if it never existed. The NEXT_RCV_SEQ is not incremented, the AckNak_LATENCY_TIMER is not started, nor is the NAK_SCHEDULED set. The receiving device silently discards the nullified TLP and does not return an Ack/Nak for it. 

## **Example of Cut-Through Operation** 

Figure 10‐16 on page 357 illustrates a TLP coming in from the left, going through the Switch, and ending up at an Endpoint on the right. A TLP error occurs on the left Link. The steps are as follows: 

1. An incoming TLP is seen at the Switch Ingress Port. It has become cor‐ rupted in flight but that isn’t known yet. 

2. The TLP header arrives, is decoded, and the packet is forwarded to the des‐ tination Egress Port in cut‐through operation. 

3. Eventually, the end of the packet arrives and the Switch Ingress Port is able to complete the LCRC error check. It finds a CRC error and returns a Nak to the TLP source. 

4. At the Egress Port, the Switch replaces the END framing symbol at the end of the bad TLP with EDB and inverts the calculated LCRC value. The TLP is now ‘nullified’ and the Switch discards it from the Replay Buffer. 

5. The nullified packet arrives at the Endpoint. The Endpoint detects the EDB symbol and inverted LCRC and silently discards the packet. It does not return a Nak. 

Now let’s say the TLP source device replays the packet and no error occurs. As before, the TLP is forwarded to the Egress Port with very short latency. When 

**356** 

**Cha ter 10: Ack/Nak Protocol p** 

the rest of the TLP arrives at the Switch, there is no error, so an Ack is returned to the TLP source which then purges this TLP from its Replay Buffer. This time the Switch Egress Port keeps a copy of the TLP in its Replay Buffer. When the TLP reaches the destination, the packet has no errors and the Endpoint returns an Ack. Based on that, the Switch purges the copy of the TLP from its Replay Buffer and the sequence is complete. 

_Figure 10‐16: Switch Cut‐Through Mode Showing Error Handling_ 

**==> picture [378 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error occurs<br>1) 2) 4)<br>END TLP STP END TLP STP EDB TLP STP<br>EDB TLP STP<br>Switch Endpoint<br>5) Discard Packet<br>NAK 6) No ACK or NAK<br>3)<br>**----- End of picture text -----**<br>


**357** 

**PCI Ex ress Technolo p gy** 

**358** 

## Part Four: 

# Physical Layer 

## _**11 Physical Layer ‐ Logical (Gen1 and Gen2)**_ 

## **The Previous Chapter** 

The previous chapter describes the Ack/Nak Protocol: an automatic, hardware‐ based mechanism for ensuring reliable transport of TLPs across the Link. Ack DLLPs confirm good reception of TLPs while Nak DLLPs indicate a transmis‐ sion error. The chapter describes the normal rules of operation as well as error recovery mechanisms. 

## **This Chapter** 

This chapter describes the Logical sub‐block of the Physical Layer. This pre‐ pares packets for serial transmission and recovery. Several steps are needed to accomplish this and they are described in detail. This chapter covers the logic associated with the Gen1 and Gen2 protocol that use 8b/10b encoding. The logic for Gen3 does not use 8b/10b encoding and is described separately in the chap‐ ter called “Physical Layer ‐ Logical (Gen3)” on page 407. 

## **The Next Chapter** 

The next chapter describes the Physical Layer characteristics for the third gener‐ ation (Gen3) of PCIe. The major change includes the ability to double the band‐ width relative to Gen2 without needing to double the frequency by eliminating the need for 8b/10b encoding. More robust signal compensation is necessary at Gen3 speed. Making these changes is more complex than might be expected. 

**361** 

**PCI Ex ress Technolo p gy** 

## **Physical Layer Overview** 

This Physical Layer Overview introduces the relationships between the Gen1, Gen2 and Gen3 implementations. Thereafter the focus is the logical Physical Layer implementation associated with Gen1 and Gen2. The logical Physical Layer implementation for Gen3 is described in the next chapter. 

The Physical Layer resides at the bottom of the interface between the external physical link and Data Link Layer. It converts outbound packets from the Data Link Layer into a serialized bit stream that is clocked onto all Lanes of the Link. This layer also recovers the bit stream from all Lanes of the Link at the receiver. The receive logic de‐serializes the bits back into a Symbol stream, re‐assembles the packets, and forwards TLPs and DLLPs up to the Data Link Layer. 

_Figure 11‐1: PCIe Port Layers_ 

**==> picture [307 x 307] intentionally omitted <==**

**----- Start of picture text -----**<br>
Software layer sends and receives address and transaction information<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Transaction layer<br>Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers Buffers<br>Management<br>per VC per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC Ack/Nak CRC Ack/Nak CRC Sequence TLP LCRC<br>Data Link layer TLP Retry De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**----- End of picture text -----**<br>


**362** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

The contents of the layers are conceptual and don’t define precise logic blocks, but to the extent that designers do partition them to match the spec their imple‐ mentations can benefit because of the constantly increasing data rates affect the Physical Layer more than the others. Partitioning a design by layered responsi‐ bilities allows the Physical Layer to be adapted to the higher clock rates while changing as little as possible in the other layers. 

The 3.0 revision of the PCIe spec does not use specific terms to distinguish the different transmission rates defined by the versions of the spec. With that in mind, the following terms are defined and used in this book. 

- **Gen1** ‐ the first generation of PCIe (rev 1.x) operating at 2.5 GT/s 

- **Gen2** ‐ the second generation (rev 2.x) operating at 5.0 GT/s 

- **Gen3** ‐ the third generation (rev 3.x) operating at 8.0 GT/s 

The Physical Layer is made up of two sub‐blocks: the Logical part and the Elec‐ trical part as shown in Figure 11‐2. Both contain independent transmit and receive logic, allowing dual‐simplex communication. 

_Figure 11‐2: Logical and Electrical Sub‐Blocks of the Physical Layer_ 

**==> picture [366 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Physical Layer Physical Layer<br>Tx Rx Tx Rx<br>Logical Logical<br>Tx Rx Tx Rx<br>Electrical Electrical<br>Link<br>Tx+ Tx- Rx+ Rx- CTX Tx- Tx+ Rx- Rx+<br>CTX<br>**----- End of picture text -----**<br>


**363** 

**PCI Ex ress Technolo p gy** 

## **Observation** 

The spec describes the functionality of the Physical Layer but is purposefully vague regarding implementation details. Evidently, the spec writers were reluc‐ tant to give details or example implementations because they wanted to leave room for individual vendors to add value with clever or creative versions of the logic. For our discussion though, an example is indispensable, and one was cho‐ sen that illustrates the concepts. It’s important to make clear that this example has not been tested or validated, nor should a designer feel compelled to imple‐ ment a Physical Layer in such a manner. 

## **Transmit Logic Overview** 

For simplicity, let’s begin with a high‐level overview of the transmit side of this layer, shown in Figure 11‐3 on page 365. Starting at the top, we can see that packet bytes entering from the Data Link layer first go into a buffer. It makes sense to have a buffer here because there will be times when the packet flow from the Data Link Layer must be delayed to allow Ordered Set packets and other items to be injected into the flow of bytes. 

For Gen1 and Gen2 operation, these injected items are control and data charac‐ ters used to mark packet boundaries and create ordered sets. To differentiate between these two types of characters, a D/K# bit (Data or “Kontrol”) is added. The logic can see what value D/K# should take on based on the source of the character.

</td>
<td style="background-color:#e8e8e8">

'D' Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>'D' Character<br>'K' Character 'K' Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>'K' Character 'K' Character<br>**----- 图片文字结束 -----**<br>


## **字节交叉（用于宽链路）**

我们示例中显示的下一步是字节交叉，尽管仅当端口实现多个 Lane（称为宽链路）时才需要。交叉意味着字符流中的每个连续输出字符被路由到连续的 Lane。使用的 Lane 数量是在链路训练过程中配置的，基于共享链路的两个设备所支持的。

以下图中说明了字节交叉的三个示例。在第 372 页的图 11-8 中，显示了单 Lane 链路 (x1)。这不是一个非常有趣的案例，因为报文一次以一个字节进入物理层并以相同的方式离开，但它说明了字符序列的绘制方式。

第 372 页的图 11-9 显示了来自多路复用器的传入 Dword 报文。每个字节被定向到相应的 Lane。最后，第 373 页的图 11-10 说明了一个八 Lane (x8) 链路。在此示例中，需要两个 Dword 才能填充所有 8 个 Lane。这要求 Dword 以比先前示例快两倍的速率到达。每个 Lane 上发送的数据格式将在以下小节中描述。

**371**

## **PCI Exress Technology**

_图 11-8：x1 字节交叉_

**==> 图片 [154 x 220] 已省略 <==**

**----- 图片文字开始 -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- 图片文字结束 -----**<br>


_图 11-9：x4 字节交叉_

**==> 图片 [338 x 205] 已省略 <==**

**----- 图片文字开始 -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- 图片文字结束 -----**<br>


**372**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-10：使用 DWord 并行数据的 x8 字节交叉_

**==> 图片 [368 x 240] 已省略 <==**

**----- 图片文字开始 -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- 图片文字结束 -----**<br>


## **报文格式规则**

## **一般规则**

- 每个报文的总报文长度（包括起始和结束字符）始终是四的倍数。这是数据长度以 dword 为单位测量的自然扩展。

- TLP 以 STP 字符开始，以 END 或 EDB 字符结束。

- DLLP 以 SDP 开始，以 END 字符结束。并且正好 8 个字符长 (SDP + 6 字符 + END)。

- STP 和 SDP 字符在逻辑空闲传输之后开始报文传输时放置在 Lane 0 上。在其他情况下，它们可以从可被 4 整除的 Lane 编号开始。

- 接收方的物理层允许监视这些规则的违规行为，并可能将其作为接收方错误报告给数据链路层。

**373**

**PCI Exress Technology**

## **示例：x1 格式**

第 374 页的图 11-11 中所示的示例说明了通过 x1 链路（仅一个 Lane 运行的链路）传输的报文的格式。显示了一系列报文，其中穿插了一个 SKIP 有序集。末尾显示了逻辑空闲，以表示发送方没有更多报文要发送并使用空闲字符作为填充的情况。

_图 11-11：x1 报文格式_

**==> 图片 [351 x 220] 已省略 <==**

**----- 图片文字开始 -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- 图片文字结束 -----**<br>


## **x4 格式规则**

- STP 和 SDP 字符始终在 Lane 0 上发送。

- END 和 EDB 字符始终在 Lane 3 上发送。

- 当发送有序集（如 SKIP）时，它必须同时出现在所有 Lane 上。

- 当传输逻辑空闲时，它们必须同时在所有 Lane 上发送。

- 这些规则的任何违规都可能作为接收方错误报告给数据链路层。

**374**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **示例 x4 格式**

第 375 页的图 11-12 中所示的示例说明了通过 x4 链路（具有四个运行数据 Lane 的链路）发送的报文的格式。该图显示了一个 TLP，后跟在所有 Lane 上传输的用于接收方时钟补偿的 SKIP 有序集。接下来是一个 DLLP，然后是所有 Lane 上的逻辑空闲。本例强调了报文始终是 4 的字符倍数，因为起始字符始终出现在 Lane 0 中，而结束字符始终在 Lane 3 中。它还说明了有序集必须同时出现在所有 Lane 上。

_图 11-12：x4 报文格式_

**375**

**PCI Exress Technology**

## **大链路宽度报文格式规则**

以下规则适用于通过 x8、x12、x16 或 x32 链路传输报文时：

- 当在传输逻辑空闲期间之后开始传输时，STP/SDP 字符始终在 Lane 0 上发送。之后，当发送背靠背报文时，它们只能发送到可被 4 整除的 Lane 编号（Lane 4、8、12 等）。

- END/EDB 字符发送到可被 4 整除的 Lane 编号，然后减一（Lane 3、7、11 等）。

- 如果报文没有在链路的最后一个 Lane 上结束，并且没有更多准备发送的报文，则 PAD 符号用作剩余 Lane 编号的填充。逻辑空闲不能用于此目的，因为它必须同时出现在所有 Lane 上。

- 有序集必须同时在所有 Lane 上发送。

- 类似地，逻辑空闲在使用时必须在所有 Lane 上发送。

- 这些规则的任何违规都可能作为接收方错误报告给数据链路层。

## **x8 报文格式示例**

第 377 页的图 11-13 中所示的示例说明了通过 x8 链路传输的报文的格式。该图显示了一个 TLP，后跟 SKIP 有序集、一个 DLLP，最后是一个在 Lane 3 结束的 TLP。在那时，发送方没有更多准备发送的报文，但当前报文未扩展到包括所有可用 Lane。有人可能期望用逻辑空闲填充额外的 Lane，但这在这里不起作用，因为空闲必须同时出现在所有 Lane 上。因此需要另一个填充字符，规范编写者选择在此处使用 PAD 控制字符。PAD 唯一使用的另一个位置是在训练过程中。最后，由于仍没有更多要发送的报文，因此会在所有 Lane 上发送逻辑空闲。

**376**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-13：x8 报文格式_

## **加扰器**

我们示例中的下一步是加扰，如图 11-5（第 369 页）所示，旨在防止数据流中的重复模式。重复模式在链路上产生"纯音"，这意味着由该模式产生的一致频率会产生比通常更多的噪声或 EMI。通过将此能量扩展到更宽的频率范围来减少此问题是加扰的主要目标。此外，单个 Lane 上的加扰传输还可减少对宽链路上相邻 Lane 的干扰。这种"空间频率去相关"，或减少串扰噪声，有助于每个 Lane 上的接收方区分所需的信号。

**377**

## **PCI Exress Technology**

为了帮助接收方与加扰序列保持同步，控制字符不会进行加扰，因此即使加扰器失去同步，它们也可被识别。此外，COM 控制字符 (K28.5) 的每次到达都会重新初始化链路两端的加扰器，从而重新同步它们。

## **加扰算法**

规范中描述的加扰器如图 11-14（第 378 页）所示。它由一个 16 位线性反馈移位寄存器 (Linear Feedback Shift Register, LFSR) 组成，其反馈点实现以下多项式：

G(x) = X[16] + X[5] + X[4] + X[3] + 1

_图 11-14：加扰器_

LFSR 以馈送数据字节的时钟频率的 8 倍频率进行计时，其输出被计时到 8 位寄存器中，该寄存器与 8 位数据字符进行 XOR 以形成加扰的数据输出。

**378**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **一些加扰器实现规则：**

- 在多 Lane 链路实现中，与每个 Lane 相关联的加扰器必须协同工作，在每个 LFSR 中保持相同的同步值。

- 加扰仅应用于 'D' 字符，即与 TLP 和 DLLP 以及逻辑空闲 (00h) 字符相关联的字符。但是，TS1 和 TS2 有序集内的那些 'D' 字符不会被加扰。

- 加扰从不应用于 'K' 字符和有序集中的字符，例如 TS1、TS2、SKIP、FTS 和电子空闲。这些字符绕过加扰器逻辑。其中一个原因是确保即使加扰器意外失去顺序，它们仍然可以被接收方识别。

- 合规性模式字符（用于测试）也不会被加扰。

- COM 字符（不会被加扰的控制字符）用于将链路两端的 LFSR 重新初始化为 FFFFh。

- 除 COM 字符外，LFSR 通常对每个发送的 D 或 K 字符串行前进 8 次，但它在与 SKIP 有序集关联的 SKP 字符上不前进。原因在于接收方可能会添加或删除 SKP 符号以执行时钟容限补偿。改变接收方中的字符数与发送的字符数相比，如果不忽略这些字符，则会导致接收方 LFSR 中的值与发送方 LFSR 值失去同步。

## **禁用加扰**

加扰默认启用，但规范允许出于测试和调试目的禁用它。这是因为测试可能需要控制发送的确切比特模式，并且由于硬件处理加扰，因此软件没有合理的方法来强制执行特定模式。规范未定义用于指示物理层禁用加扰的特定软件机制，因此这必须是特定于设计的实现。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-2"></a>
## 9.2 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Gen3 mode of operation, doesn’t use control characters, so data patterns are used to make up the ordered sets that identify if transmitted bytes are associ‐ ated with TLPs / DLLPs or Ordered Sets. A 2‐bit Sync Header is inserted at the beginning of a 128 bit (16 byte) block of data. The Sync Header informs the receiver whether the received block is a Data Block (TLP or DLLP related bytes) or an Ordered Set Block. Since there are no control characters in Gen3 mode, the D/K# bit is not needed. 

**364** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐3: Physical Layer Transmit Details_ 

**==> picture [252 x 355] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Gen3 Scrambler Lane 1, ... ,N-1 Gen3 Scrambler<br>Scrambler Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>8 10 Tx Clk 8 10<br>Mux Mux<br>Gen3 Sync<br>Serializer Bits Generator Serializer<br>Mux Mux<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- End of picture text -----**<br>


Next, the parallel data bytes coming from the upper layers are sent to Byte Striping logic where they are spread out, or striped, onto all the lanes of this link. One byte of the packet is transferred per lane, and all active lanes are used for each packet going out. The Lanes of the Link are all transmitting at the same time, so the bytes must come into this logic fast enough to accommodate that. For example, if there are eight Lanes, eight bytes of parallel from the upper lay‐ ers may arrive at the byte‐striping logic allowing data to be clocked onto all lanes simultaneously. 

**365** 

## **PCI Ex ress Technolo p gy** 

Next is the Scrambler, which XORs a pseudo‐random pattern onto the outgoing data bytes to mix up the bits. Although it would seem that this might introduce problems, it doesn’t because the scrambling pattern is predictable and not truly random, so the receiver can use the same algorithm to easily recover the origi‐ nal data. If the scramblers get out of step then the Receiver won’t be able to make sense of the bit stream so, to guard against that problem, the scrambler is reset periodically (Gen1 and Gen2). That way, if the scramblers do get out of step with each other it won’t be long before they’re both re‐initialized and back in step again. For Gen1 and Gen2 modes that re‐initialization happens when‐ ever the COM character is detected. For Gen3 mode, it happens whenever an EIEOS ordered set is seen. A more sophisticated 24‐bit based scrambler is uti‐ lized in Gen3 mode, hence the alternate path through the Gen3 scrambler, as depicted in Figure 11‐3 on page 365. 

For Gen1 and Gen2 mode, the scrambled 8‐bit characters are then encoded for transmission by the 8b/10b Encoder. Recall that a Character is an 8‐bit un‐ encoded byte, while a Symbol is the 10‐bit encoded output of the 8b/10b logic. There are several advantages to 8b/10b encoding, but it does add overhead. 

For Gen3 a separate path is shown bypassing the encoder. In other words, scrambled bytes of a packet are transmitted without 8b/10b encoding. The Sync Bit Generator adds a 2‐bit Sync Header prior to every 16 byte block of a packet. The added 2‐bit Sync Header identifies the following 16 byte block to be either a data block or an ordered set block. This addition of a 2‐bit Sync Header every 16 bytes (128 bits) is the basis of Gen3’s 128b/130b encoding scheme. 

Finally, the Symbols are serialized into a bit stream and forwarded to the electri‐ cal sub‐block of the Physical Layer and transmitted to the other end of the link. 

## **Receive Logic Overview** 

Figure 11‐4 on page 367 shows the key elements that make up the receiver logic. The process described below is performed for each lane. Starting at the bottom this time, the first thing to mention is the receiver Clock and Data Recovery (CDR). The first step in this process is to recover the clock based on transitions in the incoming bit stream. This recovered clock faithfully reproduces the Trans‐ mitter’s clock that was used to send the data and is used to latch the incoming bits into a deserializing buffer. 

The next steps in the CDR process are to find the Gen1/Gen2 Symbol bound‐ aries and divide the recovered clock by 10 to latch the 10‐bit Symbols into the Elastic Buffer. For Gen3, the next step is to acquire Block Lock and then latch the 8‐bit Symbols associated with each of the 16 bytes in the block into the Elastic Buffer — more on this in the next chapter. 

**366** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

Logic controlling the Elastic Buffer adjusts for minor clock variations between the recovered clock and the local clock of the receiver by adding or removing SKP Symbols as needed when an SOS (SKP Ordered Set) is detected. Finally, the Receiver’s local clock moves each Symbol out of the Elastic Buffer. 

_Figure 11‐4: Physical Layer Receive Logic Details_ 

**==> picture [262 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


Using the 8b/10b Decoder, Gen1/Gen2 Symbols are decoded thus converting the 10‐bit symbols to 8‐bit characters. The descrambler applies the same scrambling method used at the transmitter to recover the original data. Finally, the bytes from each Lane are un‐striped to form a byte stream that will be forwarded up to the Data Link Layer. Only TLPs and DLLPs are loaded into the receive buffer and sent to the Data Link Layer. 

**367** 

**PCI Ex ress Technolo p gy** 

## **Transmit Logic Details (Gen1 and Gen2 Only)** 

The section provides more detail associated with the steps identified in the pre‐ vious section. Refer to the block diagram in Figure 11‐5 on page 369 during this discussion. 

## **Tx Buffer** 

Starting from the top of the diagram once again, the buffer accepts TLPs and DLLPs from the Data Link Layer, along with ‘Control’ information that specifies when a new packet begins. As mentioned, the buffer allows us to stall the flow of characters from time to time in order to insert control characters and ordered sets. A ‘throttle’ signal is also shown going back up to the Data Link Layer to stop the flow of characters if the buffer should become full. 

## **Mux and Control Logic** 

The multiplexer, shown in Figure 11‐6 on page 370, is used to insert special con‐ trol (K) characters into the data flow coming from the buffer. Only the Physical Layer uses K control characters; they are inserted during transmission and removed at the receiver. The four different inputs to the mux are: 

- **Transmit Data Buffer** . When the Data Link Layer supplies a packet, the mux gates the character stream through. All of the characters coming from the buffer are D characters, so the D/K# signal is driven high when Tx Buffer contents are gated. 

- **Start and End characters.** These Control characters are added to the start and end of every TLP and DLLP (see Figure 11‐7 on page 371) and allow a receiver to readily detect the boundaries of a packet. There are two Start characters: STP indicates the start of a TLP, while SDP indicates the start of a DLLP. An indicator from the Data Link Layer, along with the packet type, determines what type of framing character to insert. There are also two end characters, the End Good character (END) for normal transmission, and the End Bad character (EDB) to handle some error cases. Start and End charac‐ ters are K characters, so the D/K# signal is driven low when the Start and End characters are inserted (see Table 11‐1 on page 386 for a list of Control characters). 

**368** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐5: Physical Layer Transmit Logic Details (Gen1 and Gen2 Only)_ 

**==> picture [190 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Scrambler Lane 1, ... ,N-1 Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- End of picture text -----**<br>


- **Ordered Sets** . As mentioned earlier, control characters are only used by the Physical Layer and are not seen by the higher layers. Some communication across the Link is necessary to initiate and maintain Link operation, and that is accomplished by exchanging Ordered Sets. Every ordered set starts with a K character called a comma (COM), and contains other K or D char‐ acters depending on the type of Order Set be delivered. Ordered Sets are always aligned on four byte boundaries and are transmitted during a vari‐ ety of circumstances including: 

   - Error recovery, initiating events (such as Hot Reset), or exit from low‐ power states. In these cases, the Training Sequence 1 and 2 (TS1 and TS2) ordered sets are exchanged across the Link. 

   - At periodic intervals, the mux inserts the SKIP ordered set pattern to facilitate clock tolerance compensation in the receiver. For a detailed description of this process, refer to “Clock Compensation” on page 391. 

**369** 

## **PCI Ex ress Technolo p gy** 

- When a device wants to place its transmitter in the Electrical Idle state, it must inform the remote receiver at the other end of the Link. The mux inserts an **Electrical Idle ordered set** to accomplish this. 

- When a device wants to change the Link power state from L0s low power state to the L0 full‐on power state, it sends a set of **Fast Training Sequence** (FTS) ordered sets to the receiver. The receiver uses this ordered set to re‐synchronize its PLL to the transmitter clock. 

- **Logical Idle Sequence.** When there are no packets ready to transmit and no ordered sets to send, the link is logically idle. In order to keep the receiver PLL locked on to the transmitter’s frequency, it’s important that the transmitter keep sending something, so Logical Idle characters are inserted for that case. Logical Idle is very simple, and consists of nothing more than a string of Data 00h characters. 

_Figure 11‐6: Transmit Logic Multiplexer_ 

**==> picture [380 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle<br>N*8<br>Tx<br>Buffer Control/ Ordered<br>CharactersToken LogicalIdle Sets<br>N*8<br>N*8 8 8 8 N*8 Ordered Sets:<br>Mux Tx   TS1,  TS2,<br>Buffer<br>N*8 D/K# STP, SDP   SKIP Logical<br>END, EDB  Electrical Idle Idle<br>Lane 0 Byte Striping Lane N<br>N*8<br>8 D/K# 8 D/K#<br>D K K/D D<br>Scrambler Lane 1, ... ,N-1 Scrambler Mux<br>8 8<br>D/K# Tx Local D/K# N*8 D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane N<br>Lane 1, ... ,N-1<br>**----- End of picture text -----**<br>


**370** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐7: TLP and DLLP Packet Framing with Start and End Control Characters_ 

**==> picture [289 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

如果设备禁用了加扰，则通过在控制字段中设置适当的位来发送至少两个 TS1 和 TS2 与相邻设备通信，如第 539 页的"配置状态"所述。作为响应，相邻设备也禁用其加扰。

**379**

**PCI Exress Technology**

## **8b/10b 编码**

## **概述**

PCIe 的前两代使用 8b/10b 编码。每个 Lane 实现一个 8b/10b 编码器，将 8 位字符转换为 10 位符号。此编码方案由 IBM 于 1984 年获得专利，今天广泛用于许多串行传输，例如千兆以太网和光纤通道。

## **动机**

编码为串行传输实现了几个理想的目标。其中最重要的三个列在此处：

- **将时钟嵌入数据中。** 编码可确保数据流中具有足够的跳变以在接收方恢复时钟，结果是不需要分布式时钟。这避免了并行总线设计的一些限制，例如飞行时间和时钟偏移。它还消除了分配高频时钟的需要，否则会导致其他问题，例如增加的 EMI 和困难的布线。

   - 作为此过程的示例，第 381 页的图 11-15 显示了数据字节 00h 的编码结果。可以看到，这个原本没有跳变的 8 位字符转换为具有 5 个跳变的 10 位符号。8b/10b 保证足够的跳变以确保比特流中的"游程长度"（连续 1 或 0 的序列）在任何条件下不超过 5 个连续位。

- **维持直流平衡。** PCIe 使用交流耦合链路，将电容器串联放置在路径中，以将信号的直流部分与链路的另一端隔离。这允许发送方和接收方使用不同的共模电压，并且对于它们之间的路径足够长以至于它们不太可能具有完全相同的参考电压的情况，使电气设计更容易。该直流值或共模电压可以在运行时发生变化，因为当信号被驱动时线路会充电。通常，信号变化得如此之快，以至于没有时间让这引起问题，但是，如果信号平均值主要是一个电平或另一个电平，则共模值将出现漂移。称为"直流漂移"，这种漂移电压会降低接收方的信号完整性。为了进行补偿，8b/10b 编码器跟踪发送的最后一个符号的"差异 (disparity)"。差异或不平等只是简单地表示前一个符号是否有更多的 1（称为正差异），更多的 0（负差异），或者 1 和 0 平衡

**380**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

   - （中性差异）。例如，如果前一个符号具有负差异，则下一个符号应通过使用更多的 1 来平衡。

- **增强错误检测。** 编码方案还有助于检测传输错误。对于 10 位值，可能有 1024 个代码，但待编码的字符只有 256 个唯一代码。为了维持直流平衡，设计为每个字符使用两个代码，并根据发送的最后一个符号的差异选择其中一个，因此将需要 512 个代码。但是，许多中性差异编码具有相同的值（D28.5 就是一个示例），因此并非所有 512 个都被使用。因此，超过一半的可能编码未被使用，如果在接收方看到，则将被视为非法。如果传输错误确实更改了符号的位模式，那么结果很可能是这些可立即识别的非法模式之一。有关更多信息，请参见第 383 页的标题为"差异"的部分。

8b/10b 编码的主要缺点是它所需的开销。从接收方的角度来看，实际传输性能降低了 20%，因为每个字节发送 10 位，但仅在接收方恢复 8 个有效位。这是一个不小的代价，但考虑到前面提到的好处，它仍然被认为是可以接受的。

_图 11-15：8 位字符 00h 编码示例_

**==> 图片 [224 x 112] 已省略 <==**

**----- 图片文字开始 -----**<br>
8b Value<br>0 0 0 0 0 0 0 0<br>Data 00h<br>10b Encoded<br>0 11 0 0 0 1 0 1 1<br>Value<br>**----- 图片文字结束 -----**<br>


## **10 位符号的属性**

如 8b/10b 编码文献中所述，设计并非严格的 8 位到 10 位。相反，它实际上是一个 5 位到 6 位的编码，然后是 3 位到 4 位的编码。子块是设计内部的，但它们的存在有助于解释合法符号的一些属性，如下所列。不遵循这些属性的符号被视为无效。

**381**

**PCI Exress Technology**

- 比特流从不包含超过五个连续的 1 或 0，即使从一个符号的末尾到下一个符号的开头也是如此。

- 每个 10 位符号包含：

   - 四个 0 和六个 1（不一定连续），或

   - 六个 0 和四个 1（不一定连续），或

   - 五个 0 和五个 1（不一定连续）。

- 每个 10 位符号被细分为两个子块：第一个是六位宽，第二个是四位宽。

   - 6 位子块包含不超过四个 1 或四个 0。

   - 4 位子块包含不超过三个 1 或三个 0。

## **字符表示法**

8b/10b 使用一种特殊的简写符号表示法，第 382 页的图 11-16 说明了为给定字符得出简写符号的步骤：

1. 将字符划分为其 3 位和 5 位子块。

2. 转置子块的位置。

3. 为每个子块创建十进制等效值。

4. 字符采用 Dxx.y（数据字符）或 Kxx.y（控制字符）的形式。在此表示法中，xx 是 5 位字段的十进制等效值，y 是 3 位字段的十进制等效值。

_图 11-16：8b/10b 命名法_

**==> 图片 [348 x 211] 已省略 <==**

**----- 图片文字开始 -----**<br>
8b Designation Example Data (6Ah)<br>D/<br>8b Character 7 6 5 4 3 2 1 0 D 01101010<br>K#<br>Partition into D/ H G F E D C B A<br>D 011 01010<br>sub-blocks K#<br>Flip sub-blocks K#D/ E D C B A H G F D 01010 011<br>Convert sub-blocks<br>to decimal notation D/K xx . y D 10 . 3<br>Final Notation D/Kxx.y D10.3<br>**----- 图片文字结束 -----**<br>


**382**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **差异**

**定义。** 差异是指 10 位符号内 1 和 0 的数量之间的不等式，并用于帮助维持链路上的直流平衡。具有更多 0 的符号称为具有负 (-) 差异，而具有更多 1 的符号具有正 (+) 差异。当符号具有相等数量的 1 和 0 时，称为具有中性差异。有趣的是，大多数字符编码为具有 + 或 – 差异的符号，但有些仅编码为具有中性差异的符号。

**CRD (当前运行差异)。** CRD 是关于链路上差异的当前状态的信息。由于它只是一个位，因此它只能为正或负，并且并不总是在发送下一个符号时更改。要查看它的工作原理，请记住下一个解码的符号可能具有负、中性或正差异，然后考虑以下示例。如果 CRD 为正，则具有负差异的传出符号将把它更改为负，中性差异将保持为正，正差异将是错误，因为 CRD 仅一位，不能变得更正。

CRD 的初始状态（在传输任何字符之前）可能与发送方和接收方之间不匹配，但事实证明这并不重要。当接收方在训练完成后看到第一个符号时，它将检查差异错误，如果发现，则只需更改 CRD。这不会被视为错误，而只是 CRD 调整以匹配接收方和发送方。之后，只有两种合法的 CRD 情况：如果新符号具有中性差异，则它可以保持不变；如果新符号具有相反的差异，则它可以翻转为相反极性。新符号的差异与 CRD 相同是不合法的。这样的事件将是差异错误，除非发生错误，否则在初始调整之后永远不会发生。

## **编码过程**

可以通过不同方式完成 8b/10b 编码。最简单的方法可能是实现一个包含所有可能输出值的查找表。但是，此表可能需要相对大量的门。另一种方法是将解码器实现为逻辑块，这通常是首选，因为它通常会产生更小且更便宜的解决方案。编码逻辑的细节在所引用的文献中有详细描述，因此我们将重点放在其工作原理的更大图景上。

**383**

## **PCI Exress Technology**

示例 8b/10b 框图如图 11-17（第 384 页）所示。新的传出符号基于以下三件事创建：传入字符、该字符的 D/K# 指示以及 CRD。基于传出符号计算新的 CRD 值，并反馈用于编码下一个字符。编码后，生成的符号被馈送到串行器，该串行器将各个位计时输出。图 11-18（第 385 页）显示了一些示例 8b/10b 编码，这些编码对后续示例很有用。

_图 11-17：8 位到 10 位 (8b/10b) 编码器_

**==> 图片 [343 x 244] 已省略 <==**

**----- 图片文字开始 -----**<br>
Bytes from Scrambler D/K#<br>8b Character 7 6 5 4 3 2 1 0<br>H G F E D C B A<br>8b/10b Encoding Logic<br>Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>Serial Stream<br>Serializer j h g f i e d c b a to Transmitter<br>using Tx Clock<br>**----- 图片文字结束 -----**<br>


**384**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-18：示例 8b/10b 编码_

## **示例传输**

图 11-19 说明了三个字符的编码和传输：第一个和第二个是控制字符 K28.5，第三个字符是数据字符 D10.3。

在此示例中，初始 CRD 为负，因此 K28.5 编码为 001111 1010b。此符号具有正差异（1 多于 0），并导致 CRD 极性翻转为正。下一个 K28.5 编码为 110000 0101b，具有负差异。这导致 CRD 这次翻转为负。最后，D10.3 编码为 010101 1100b。由于其差异为中性，因此 CRD 在此情况下不会更改，但保持为负，以供下一个字符使用。

**385**

**PCI Exress Technology**

_图 11-19：示例 8b/10b 传输_

## **在以下示例中使用这两个字符：**

|**D/K#**|**十六进制**<br>**字节**|**二进制位**<br>**HGF EDCBA**|**字节**<br>**名称**|**CRD –**<br>**abcdei fghj**|**CRD +**<br>**abcdei fghj**|
|---|---|---|---|---|---|
|**控制(K)**|**BC**|**101 11100**|**K28.5**|**001111 1010**|**110000 0101**|
|**数据(D)**|**6A**|**011 01010**|**D10.3**|**010101 1100**|**010101 0011**|



## **示例传输**

||**CRD**|**字符**|**CRD**|**字符**|**CRD**|**字符**|**CRD**|
|---|---|---|---|---|---|---|---|
|**要传输的**<br>**字符**|**-**|**K28.5 (BCh)**|**+**|**K28.5 (BCh)**|**-**|**D10.3 (6Ah)**|**-**|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---



<img src="figures/embedded/page0361_img1.png" alt="Figure from page 361" width="700">

<a id="sec-9-3"></a>
## 9.3 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

‘D’ Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>‘D’ Character<br>‘K’ Character ‘K’ Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>‘K’ Character ‘K’ Character<br>**----- End of picture text -----**<br>


## **Byte Striping (for Wide Links)** 

The next step shown in our example is Byte Striping, although this is only needed if the port implements more than one Lane (called a wide Link). Strip‐ ing means that each consecutive outbound character in a character stream is routed onto consecutive Lanes. The number of Lanes used is configured during the Link training process based on what is supported by both devices that share the Link. 

Three examples of byte striping are illustrated in the following diagrams. In Figure 11‐8 on page 372, a single‐lane link (x1) is shown. This is not a very inter‐ esting case, since the packet enters the Physical Layer a byte at a time and goes out the same way, but illustrates the way the sequence of characters will be drawn. 

Figure 11‐9 on page 372 shows the incoming Dword packets from the muti‐ plexer. Each byte is directed to the corresponding lanes. Finally, Figure 11‐10 on page 373 illustrates an eight‐lane (x8) link. In this example, two Dwords are required to populate all 8 lanes. This requires the Dword to arrive at twice the rate as the previous example. The format of the data being sent across each lane is described in the sections that follow. 

**371** 

## **PCI Ex ress Technolo p gy** 

_Figure 11‐8: x1 Byte Striping_ 

**==> picture [154 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- End of picture text -----**<br>


_Figure 11‐9: x4 Byte Striping_ 

**==> picture [338 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- End of picture text -----**<br>


**372** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐10: x8 Byte Striping with DWord Parallel Data_ 

**==> picture [368 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- End of picture text -----**<br>


## **Packet Format Rules** 

## **General Rules** 

- The total packet length (including Start and End characters) of each packet is always a multiple of four characters. This is a natural extension of the fact that the data length is measured in dwords. 

- TLPs start with the STP character and finish with either an END or EDB character. 

- DLLPs start with SDP, terminate with the END character. and are exactly 8 characters long (SDP + 6 characters + END) 

- STP and SDP characters are placed on Lane 0 when starting the transmis‐ sion of a packet after the transmission of Logical Idles. In other cases, they may start on a Lane number divisible by 4. 

- The receiver’s Physical Layer is allowed to watch for violation of these rules and may report them as Receiver Errors to the Data Link Layer. 

**373** 

**PCI Ex ress Technolo p gy** 

## **Example: x1 Format** 

The example shown in Figure 11‐11 on page 374 illustrates the format of packets transmitted over a x1 link (a link with only one lane operational). A sequence of packets is shown interspersed with one SKIP Ordered Set. Logical Idles are shown at the end to represent the case when the transmitter has no more pack‐ ets to send and uses idle characters as filler. 

_Figure 11‐11: x1 Packet Format_ 

**==> picture [351 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- End of picture text -----**<br>


## **x4 Format Rules** 

- STP and SDP characters are always sent on Lane 0. 

- END and EDB characters are always sent on Lane 3. 

- When an ordered set such as the SKIP is sent, it must appear on all lanes simultaneously. 

- When Logical Idles are transmitted, they must be sent on all lanes simulta‐ neously. 

- Any violation of these rules may be reported as a Receiver Error to the Data Link Layer. 

**374** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Example x4 Format** 

The example shown in Figure 11‐12 on page 375 illustrates the format of packets sent over a x4 Link (link with four data lanes operational). The illustration shows one TLP followed by a SKIP ordered set transmitted on all Lanes for receiver clock compensation. Next is a DLLP, followed by Logical Idle on all lanes. This example highlights that the packets are always multiples of 4 charac‐ ters because the start character always appears in lane 0 and the end character is always in lane 3. It also illustrates that ordered sets must appear on all the lanes simultaneously. 

_Figure 11‐12: x4 Packet Format_ 

**375** 

**PCI Ex ress Technolo p gy** 

## **Large Link-Width Packet Format Rules** 

The following rules apply when a packet is transmitted over a x8, x12, x16, or x32 Link: 

- STP/SDP characters are always sent on Lane 0 when transmission starts after a period during which Logical Idles are transmitted. After that, they may only be sent on Lane numbers divisible by 4 when sending back‐to‐ back packets (Lane 4, 8, 12, etc.). 

- END/EDB characters are sent on Lane numbers divisible by 4 and then minus one (Lane 3, 7, 11, etc.). 

- If a packet doesn’t end on the last Lane of the Link and there are no more packets ready to go, PAD Symbols are used as filler on the remaining lane numbers. Logical Idle can’t be used for this purpose because it must appear on all Lanes at the same time. 

- Ordered sets must be sent on all lanes simultaneously. 

- Similarly, logical idles must be sent on all lanes when they are used. 

- Any violation of these rules may be reported as a Receiver Error to the Data Link Layer. 

## **x8 Packet Format Example** 

The example shown in Figure 11‐13 on page 377 illustrates the format of packets transmitted over a x8 link. The illustration shows a TLP followed by a SKIP ordered set, a DLLP, and finally a TLP that ends on Lane 3. At that point, the transmitter has no more packets ready to send but the current packet doesn’t extend to include all the available lanes. One might expect the extra lanes to be filled with Logical Idle, but it won’t work here because idles must appear on all lanes at the same time. So another fill character is needed, and the spec writers chose to use the PAD control character here. The only other place that PAD is used is during the training process. Finally, since there are still no more packets to send, Logical Idles are sent on all the lanes. 

**376** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐13: x8 Packet Format_ 

## **Scrambler** 

The next step in our example is scrambling, as shown in Figure 11‐5 on page 369, which is intended to prevent repetitive patterns in the data stream. Repeti‐ tive patterns create “pure tones” on the link, meaning a consistent frequency caused by the pattern that generates more than the usual noise, or EMI. Reduc‐ ing this problem by spreading this energy over a wider frequency range is the primary goal of scrambling. In addition, though, scrambled transmission on one Lane also reduces interference with adjacent Lanes on a wide Link. This “spatial frequency de‐correlation”, or reduction of crosstalk noise, helps the receiver on each lane to distinguish the desired signal. 

**377** 

## **PCI Ex ress Technolo p gy** 

To help the receiver maintain synchronization with the scrambled sequence, control characters do not get scrambled and are thus recognizable even if the scramblers get out of sync. In addition, the arrival of the COM control character (K28.5) reinitializes the scramblers on both ends of the Link each time it arrives and thus re‐synchronizes them. 

## **Scrambler Algorithm** 

The scrambler described in the spec is shown in Figure 11‐14 on page 378. It’s made of a 16‐bit Linear Feedback Shift Register (LFSR) with feedback points that implement the following polynomial: 

G(x) = X[16] + X[5] + X[4] + X[3 ] +1 

_Figure 11‐14: Scrambler_ 

The LFSR is clocked at 8 times the frequency of the clock feeding the data bytes, and its output is clocked into an 8‐bit register that is XORed with the 8‐bit data characters to form the scrambled data output. 

**378** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Some Scrambler implementation rules:** 

- On a multi‐Lane Link implementation, Scramblers associated with each Lane must operate in concert, maintaining the same simultaneous value in each LFSR. 

- Scrambling is applied to ‘D’ characters only, meaning those associated with TLP and DLLPs and the Logical Idle (00h) characters. However, those ‘D’ characters that are within the TS1 and TS2 ordered sets are not scrambled. 

- Scrambling is never applied to ‘K’ characters and characters within ordered sets, such as TS1, TS2, SKIP, FTS and Electrical Idle. These characters bypass the scrambler logic. One reason for this is to ensure they’ll still be recogniz‐ able by the receiver even if the scramblers somehow get out of sequence. 

- Compliance Pattern characters (used for testing) are also not scrambled. 

- • The COM character, a control character that does not get scrambled, is used to reinitialize the LFSR to FFFFh at both the transmitter and receiver. 

- Except for the COM character, the LFSR normally will serially advance eight times for every D or K character sent, but it does not advance on SKP characters associated with the SKIP ordered set. The reason is that a receiver may add or delete SKP Symbols to perform clock tolerance com‐ pensation. Changing the number of characters in the receiver compared to the number that were sent would cause the value in the receiver LFSR to lose synchronization with the transmitter LFSR value if they were not ignored. 

## **Disabling Scrambling** 

Scrambling is enabled by default, but the spec allows it to be disabled for test and debug purposes. That’s because testing may require control of the exact bit pattern sent and, since the hardware handles scrambling, there’s no reasonable way for the software to be able to force a specific pattern. No specific software mechanism is defined by which to instruct the Physical Layer to disable scram‐ bling, so this has to be a design‐specific implementation.

</td>
<td style="background-color:#e8e8e8">

'D' Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>'D' Character<br>'K' Character 'K' Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>'K' Character 'K' Character<br>**----- End of picture text -----**


## **字节条带化（用于宽链路）**

我们示例中显示的下一步是字节条带化 (Byte Striping)，尽管仅当端口实现多个 Lane（称为宽链路 (wide Link)）时才需要此步骤。条带化意味着字符流中的每个连续输出字符被路由到连续的 Lane 上。使用的 Lane 数在链路训练 (Link training) 过程中根据共享链路的两台设备所支持的 Lane 数进行配置。

以下图表中说明了字节条带化的三个示例。在第 372 页图 11-8 中，显示了单 Lane 链路 (x1)。这不是一个非常有趣的案例，因为数据包以字节为单位进入物理层 (Physical Layer) 并以相同方式发出，但它说明了字符序列的绘制方式。

第 372 页图 11-9 显示了来自多路复用器的传入双字 (Dword) 数据包。每个字节被定向到对应的 Lane。最后，第 373 页图 11-10 说明了八 Lane (x8) 链路。在此示例中，需要两个双字 (Dwords) 来填充所有 8 个 Lane。这要求双字以比前一示例快两倍的速率到达。后续章节中描述了通过每个 Lane 发送的数据格式。

**371**

## **PCI Express 技术**

_图 11-8：x1 字节条带化_

**==> picture [154 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- End of picture text -----**


_图 11-9：x4 字节条带化_

**==> picture [338 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- End of picture text -----**


**372**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-10：使用双字并行数据的 x8 字节条带化_

**==> picture [368 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- End of picture text -----**


## **数据包格式规则**

## **一般规则**

- 每个数据包的总长度（包括开始和结束字符）始终是 4 的倍数。这是数据长度以双字 (dwords) 为单位这一事实的自然延伸。

- TLP 以 STP 字符开始，并以 END 或 EDB 字符结束。

- DLLP 以 SDP 开头，以 END 字符结束，并且恰好为 8 个字符长 (SDP + 6 个字符 + END)。

- 在发送完逻辑空闲 (Logical Idles) 后开始传输数据包时，STP 和 SDP 字符被放置在 Lane 0 上。在其他情况下，它们可以以可被 4 整除的 Lane 号开始。

- 接收方的物理层 (Physical Layer) 允许监视对这些规则的违反情况，并可将其作为接收器错误 (Receiver Errors) 报告给数据链路层 (Data Link Layer)。

**373**

**PCI Express 技术**

## **示例：x1 格式**

第 374 页图 11-11 中所示的示例说明了通过 x1 链路（仅一个 Lane 工作的链路）传输的数据包的格式。图中显示了一系列数据包，其中穿插着一个 SKIP 有序集。最后显示逻辑空闲 (Logical Idles)，以表示发送器没有更多数据包可发送并使用空闲字符作为填充的情况。

_图 11-11：x1 数据包格式_

**==> picture [351 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- End of picture text -----**


## **x4 格式规则**

- STP 和 SDP 字符始终在 Lane 0 上发送。

- END 和 EDB 字符始终在 Lane 3 上发送。

- 当发送有序集（例如 SKIP）时，必须同时出现在所有 Lane 上。

- 当发送逻辑空闲 (Logical Idles) 时，必须同时在所有 Lane 上发送。

- 对这些规则的任何违反都可以作为接收器错误 (Receiver Error) 报告给数据链路层 (Data Link Layer)。

**374**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **x4 格式示例**

第 375 页图 11-12 中所示的示例说明了通过 x4 链路（四条数据 Lane 工作的链路）发送的数据包的格式。该图显示了在所有 Lane 上发送的一个 TLP 后跟一个 SKIP 有序集，用于接收器时钟补偿。接下来是一个 DLLP，然后是所有 Lane 上的逻辑空闲 (Logical Idle)。此示例突出表明数据包始终是 4 的倍数，因为起始字符始终出现在 Lane 0 中，结束字符始终在 Lane 3 中。它还说明有序集必须同时出现在所有 Lane 上。

_图 11-12：x4 数据包格式_

**375**

**PCI Express 技术**

## **大链路宽度数据包格式规则**

当通过 x8、x12、x16 或 x32 链路传输数据包时，以下规则适用：

- 在发送完一段时间的逻辑空闲 (Logical Idles) 后开始发送时，STP/SDP 字符始终在 Lane 0 上发送。在此之后，仅当背靠背发送数据包时，它们才能在可被 4 整除的 Lane 号上发送（Lane 4、8、12 等）。

- END/EDB 字符在可被 4 整除然后减一的 Lane 号上发送（Lane 3、7、11 等）。

- 如果数据包未在链路的最后一个 Lane 上结束，并且没有更多准备发送的数据包，则使用 PAD 符号 (PAD Symbols) 作为其余 Lane 号的填充。逻辑空闲 (Logical Idle) 不能用于此目的，因为它必须同时出现在所有 Lane 上。

- 有序集必须同时在所有 Lane 上发送。

- 类似地，在使用逻辑空闲时，必须同时在所有 Lane 上发送。

- 对这些规则的任何违反都可以作为接收器错误 (Receiver Error) 报告给数据链路层 (Data Link Layer)。

## **x8 数据包格式示例**

第 377 页图 11-13 中所示的示例说明了通过 x8 链路传输的数据包的格式。该图显示了一个 TLP 后跟一个 SKIP 有序集、一个 DLLP，最后是一个在 Lane 3 上结束的 TLP。此时，发送器没有更多准备发送的数据包，但当前数据包未扩展到包括所有可用的 Lane。人们可能期望用逻辑空闲 (Logical Idle) 填充额外的 Lane，但在这里不起作用，因为空闲必须同时出现在所有 Lane 上。因此需要另一个填充字符，规范作者选择在此处使用 PAD 控制字符。PAD 唯一使用的另一个地方是在训练过程中。最后，由于仍然没有更多数据包可发送，因此在所有 Lane 上发送逻辑空闲 (Logical Idles)。

**376**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-13：x8 数据包格式_

## **加扰器**

我们示例中的下一步是加扰 (scrambling)，如第 369 页图 11-5 所示，旨在防止数据流中出现重复模式。重复模式会在链路上产生"纯音"，即由模式引起的超过通常噪声的一致频率，或称为 EMI (电磁干扰)。通过将能量扩展到更宽的频率范围来减少此问题是加扰的主要目标。此外，一条 Lane 上的加扰传输还可减少宽链路上相邻 Lane 之间的干扰。这种"空间去相关"或串扰噪声的减少有助于每个 Lane 上的接收器区分所需信号。

**377**

## **PCI Express 技术**

为了帮助接收器与加扰序列保持同步，控制字符不会被加扰，因此即使加扰器失去同步也是可识别的。此外，COM 控制字符 (K28.5) 每次到达时都会重新初始化链路两端的加扰器，从而使其重新同步。

## **加扰算法**

规范中描述的加扰器 (scrambler) 如第 378 页图 11-14 所示。它由一个 16 位线性反馈移位寄存器 (Linear Feedback Shift Register, LFSR) 组成，其反馈点实现以下多项式：

G(x) = X[16] + X[5] + X[4] + X[3] + 1

_图 11-14：加扰器_

LFSR 以馈送数据字节的时钟频率的 8 倍频率进行计时，其输出被计时进入一个 8 位寄存器，该寄存器与 8 位数据字符进行 XOR 异或运算以形成加扰数据输出。

**378**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **一些加扰器实现规则：**

- 在多 Lane 链路 (multi‐Lane Link) 实现中，与每个 Lane 关联的加扰器 (Scramblers) 必须协调运行，在每个 LFSR 中保持相同的同步值。

- 加扰 (Scrambling) 仅应用于 'D' 字符，即那些与 TLP 和 DLLP 以及逻辑空闲 (Logical Idle, 00h) 字符相关联的字符。但是，TS1 和 TS2 有序集内的那些 'D' 字符不会被加扰。

- 加扰 (Scrambling) 从不应用于 'K' 字符以及有序集内的字符，例如 TS1、TS2、SKIP、FTS 和电气空闲 (Electrical Idle)。这些字符绕过加扰器逻辑。这样做的一个原因是确保即使加扰器以某种方式失去序列，接收器仍然可以识别它们。

- 合规模式 (Compliance Pattern) 字符（用于测试）也不被加扰。

- COM 字符（不被加扰的控制字符）用于将发送器和接收器两端的 LFSR 重新初始化为 FFFFh。

- 除 COM 字符外，LFSR 通常在每发送一个 D 或 K 字符时串行推进 8 次，但在与 SKIP 有序集关联的 SKP 字符上不推进。原因是接收器可以添加或删除 SKP 符号以执行时钟容差补偿。如果不忽略 SKP 字符，与发送的数量相比，接收器中字符数量的变化将导致接收器 LFSR 中的值与发送器 LFSR 值失去同步。

## **禁用加扰**

默认情况下启用加扰 (Scrambling)，但规范允许出于测试和调试目的将其禁用。那是因为测试可能需要控制发送的确切位模式，并且由于硬件处理加扰，软件没有合理的方法来强制特定模式。规范中未定义用于指示物理层 (Physical Layer) 禁用加扰的特定软件机制，因此这必须是特定于设计 (design‐specific) 的实现。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-4"></a>
## 9.4 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

If scrambling is disabled by a device, this gets communicated to the neighbor‐ ing device by sending at least two TS1s and TS2s that have the appropriate bit set in the control field as described in “Configuration State” on page 539. In response, the neighboring device also disables its scrambling. 

**379** 

**PCI Ex ress Technolo p gy** 

## **8b/10b Encoding** 

## **General** 

The first two generations of PCIe use 8b/10b encoding. Each Lane implements an 8b/10b Encoder that translates the 8‐bit characters into 10‐bit Symbols. This coding scheme was patented by IBM in 1984 and is widely used in many serial transports today, such as Gigabit Ethernet and Fibre Channel. 

## **Motivation** 

Encoding accomplishes several desirable goals for serial transmission. Three of the most important are listed here: 

- **Embedding a Clock into the Data.** Encoding ensures that the data stream has enough edges in it to recover a clock at the Receiver, with the result that a distributed clock is not needed. This avoids some limitations of a parallel bus design, such as flight time and clock skew. It also eliminates the need to distribute a high‐frequency clock that would cause other problems like increased EMI and difficult routing. 

   - As an example of this process, Figure 11‐15 on page 381 shows the encoding results of the data byte 00h. As can be seen, this 8‐bit character that had no transitions converts to a 10‐bit Symbol with 5 transitions. The 8b/10b guar‐ antees enough edges to ensure the “run length” (sequence of consecutive ones or zeros) in the bit stream to no more than 5 consecutive bits under any conditions. 

- **Maintaining DC Balance.** PCIe uses an AC‐coupled link, placing a capaci‐ tor serially in the path to isolate the DC part of the signal from the other end of the Link. This allows the Transmitter and Receiver to use different com‐ mon‐mode voltages and makes the electrical design easier for cases where the path between them is long enough that they’re less likely to have exactly the same reference voltages. That DC value, or common‐mode voltage, can change during run time because the line charges up when the signal is driven. Normally, the signal changes so quickly that there isn’t time for this to cause a problem but, if the signal average is predominantly one level or the other, the common‐mode value will appear to drift. Referred to as “DC Wander”, this drifting voltage degrades signal integrity at the Receiver. To compensate, the 8b/10b encoder tracks the “disparity” of the last Symbol that was sent. Disparity, or inequality, simply indicates whether the previ‐ ous Symbol had more ones than zeros (called positive disparity), more zeros than ones (negative disparity), or a balance of ones and zeros (neutral 

**380** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

   - disparity). If the previous Symbol had negative disparity, for example, the next one should balance that by using more ones. 

- **Enhancing Error Detection.** The encoding scheme also facilitates the detec‐ tion of transmission errors. For a 10‐bit value, 1024 codes are possible, but the character to be encoded only has 256 unique codes. To maintain DC bal‐ ance the design uses two codes for each character, and chooses which one based on the disparity of the last Symbol that was sent, so 512 codes would be needed. However, many of the neutral disparity encodings have the same values (D28.5 is one example), so not all 512 are used. As a result, more than half the possible encodings are not used and will be considered illegal if seen at a Receiver. If a transmission error does change the bit pat‐ tern of a Symbol, there’s a good chance the result would be one of these ille‐ gal patterns that can be recognized right away. For more on this see the section titled, “Disparity” on page 383. 

The major disadvantage of 8b/10b encoding is the overhead it requires. The actual transmission performance is degraded by 20% from the Receiver’s point of view because 10 bits are sent for each byte, but only 8 useful bits are recov‐ ered at the receiver. This is a non‐trivial price to pay but is still considered acceptable to gain the advantages mentioned. 

_Figure 11‐15: Example of 8‐bit Character 00h Encoding_ 

**==> picture [224 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
8b Value<br>0 0 0 0 0 0 0 0<br>Data 00h<br>10b Encoded<br>0 11 0 0 0 1 0 1 1<br>Value<br>**----- End of picture text -----**<br>


## **Properties of 10-bit Symbols** 

As described in the literature on 8b/10b coding, the design isn’t strictly 8 bits to 10 bits. Instead, it’s really a 5‐to‐6 bit encoding followed by a 3‐to‐4 bit encoding. The sub‐blocks are internal to the design but their existence helps to explain some of the properties for a legal Symbol, as listed below. A Symbol that doesn’t follow these properties is considered invalid. 

**381** 

**PCI Ex ress Technolo p gy** 

- The bit stream never contains more than five continuous 1s or 0s, even from the end of one Symbol to beginning of the next. 

- Each 10‐bit Symbol contains: 

   - Four 0s and six 1s (not necessarily contiguous), or 

   - Six 0s and four 1s (not necessarily contiguous), or 

   - Five 0s and five 1s (not necessarily contiguous). 

- Each 10‐bit Symbol is subdivided into two sub‐blocks: the first is six bits wide and the second is four bits wide. 

   - The 6‐bit sub‐block contains no more than four 1s or four 0s. 

   - The 4‐bit sub‐block contains no more than three 1s or three 0s. 

## **Character Notation** 

The 8b/10b uses a special notation shorthand, and Figure 11‐16 on page 382 illustrates the steps to arrive at the shorthand for a given character: 

1. Partition the character into its 3‐bit and 5‐bit sub‐blocks. 

2. Transpose the position of the sub‐blocks. 

3. Create the decimal equivalent for each sub‐block. 

4. The character takes the form Dxx.y for Data characters, or Kxx.y for Control characters. In this notation, xx is the decimal equivalent of the 5‐bit field, and y is the decimal equivalent of the 3‐bit field. 

_Figure 11‐16: 8b/10b Nomenclature_ 

**==> picture [348 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
8b Designation Example Data (6Ah)<br>D/<br>8b Character 7 6 5 4 3 2 1 0 D 01101010<br>K#<br>Partition into D/ H G F E D C B A<br>D 011 01010<br>sub-blocks K#<br>Flip sub-blocks K#D/ E D C B A H G F D 01010 011<br>Convert sub-blocks<br>to decimal notation D/K xx . y D 10 . 3<br>Final Notation D/Kxx.y D10.3<br>**----- End of picture text -----**<br>


**382** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Disparity** 

**Definition.** Disparity refers to the inequality between the number of ones and zeros within a 10‐bit Symbol and is used to help maintain DC balance on the link. A Symbol with more zeros is said to have a negative (–) dispar‐ ity, while a Symbol with more ones has a positive (+) disparity. When a Symbol has an equal number of ones and zeros, it’s said to have a neutral disparity. Interestingly, most characters encode into Symbols with + or – dis‐ parity, but some only encode into Symbols with neutral disparity. 

**CRD (Current Running Disparity).** The CRD is the information as to the current state of disparity on the link. Since it’s just a single bit it can only be positive or negative and doesn’t always change when the next Symbol is sent out. To see how it works, remember that the next Symbol decoded can have negative, neutral, or positive disparity, then consider the following example. If the CRD was positive, an outgoing Symbol with a negative dis‐ parity would change it to negative, a neutral disparity would leave it as positive, and a positive disparity would be an error because the CRD is only one bit and can’t be made more positive. 

The initial state of the CRD (before any characters are transmitted) may not match between the sender and receiver but it turns out that it doesn’t mat‐ ter. When the receiver sees the first Symbol after training is complete, it will check for a disparity error and, if one is found, just change the CRD. This won’t be considered an error but simply an adjustment of the CRD to match the receiver and sender. After that, there are only two legal CRD cases: it can remain the same if the new Symbol has neutral disparity, or it can flip to the opposite polarity if the new Symbol has the opposite disparity. What is not legal is for the disparity of the new Symbol to be the same as the CRD. Such an event would be a disparity error and should never occur after the initial adjustment unless an error has occurred. 

## **Encoding Procedure** 

There are different ways that 8b/10b encoding could be accomplished. The sim‐ plest approach is probably to implement a look‐up table that contains all the possible output values. However, this table can require a comparatively large number of gates. Another approach is to implement the decoder as a logic block, and this is usually the preferred choice because it typically results in a smaller and cheaper solution. The specifics of the encoding logic are described in detail in the referenced literature, so we’ll focus here on the bigger picture of how it works instead. 

**383** 

## **PCI Ex ress Technolo p gy** 

An example 8b/10b block diagram is shown in Figure 11‐17 on page 384. A new outgoing Symbol is created based on three things: the incoming character, the D/K# indication for that character, and the CRD. A new CRD value is computed based on the outgoing Symbol and is fed back for use in encoding the next char‐ acter. After encoding, the resulting Symbol is fed to a serializer that clocks out the individual bits. Figure 11‐18 on page 385 shows some sample 8b/10b encod‐ ings that will be useful for the example that follows. 

_Figure 11‐17: 8‐bit to 10‐bit (8b/10b) Encoder_ 

**==> picture [343 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bytes from Scrambler D/K#<br>8b Character 7 6 5 4 3 2 1 0<br>H G F E D C B A<br>8b/10b Encoding Logic<br>Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>Serial Stream<br>Serializer j h g f i e d c b a to Transmitter<br>using Tx Clock<br>**----- End of picture text -----**<br>


**384** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐18: Example 8b/10b Encodings_ 

## **Example Transmission** 

Figure 11‐19 illustrates the encode and transmission of three characters: the first and second are the control character K28.5 and the third character is the data character D10.3. 

In this example the initial CRD is negative so K28.5 encodes into 001111 1010b. This Symbol has positive disparity (more ones than zeros), and causes the CRD polarity to flip to positive. The next K28.5 is encoded into 110000 0101b and has a negative disparity. That causes the CRD this time to flip to negative. Finally, D10.3 is encoded into 010101 1100b. Since its disparity is neutral, the CRD doesn’t change in this case but remains negative for whatever the next character will be. 

**385** 

**PCI Ex ress Technolo p gy** 

_Figure 11‐19: Example 8b/10b Transmission_ 

## **Use these two characters in the example below:** 

|**D/K#**|**Hex**<br>**Byte**|**Binary Bits**<br>**HGF EDCBA**|**Byte**<br>**Name**|**CRD –**<br>**abcdei fghj**|**CRD +**<br>**abcdei fghj**|
|---|---|---|---|---|---|
|**Control(K)**|**BC**|**101 11100**|**K28.5**|**001111 1010**|**110000 0101**|
|**Data(D)**|**6A**|**011 01010**|**D10.3**|**010101 1100**|**010101 0011**|



## **Example Transmission** 

||**CRD**|**Character**|**CRD**|**Character**|**CRD**|**Character**|**CRD**|
|---|---|---|---|---|---|---|---|
|**Character to**<br>**be transmitted**|**-**|**K28.5 (BCh)**|**+**|**K28.5 (BCh)**|**-**|**D10.3 (6Ah)**|**-**|

</td>
<td style="background-color:#e8e8e8">

**'D' Character**
Transaction Layer Packet (TLP)
STP Sequence Header Data Payload  ECRC LCRC END
**'D' Character**
**'K' Character 'K' Character**
Data Link Layer Packet (DLLP)
SDP DLLP Type Misc. CRC END
**'K' Character 'K' Character**
**----- 图片文字结束 -----**


## **字节交叉（用于宽链路）**

我们示例中显示的下一步是字节交叉，尽管仅当端口实现多个 Lane（称为宽链路）时才需要。交叉意味着字符流中的每个连续输出字符被路由到连续的 Lane。使用的 Lane 数量是在链路训练过程中配置的，基于共享链路的两个设备所支持的。

以下图中说明了字节交叉的三个示例。在第 372 页的图 11-8 中，显示了单 Lane 链路 (x1)。这不是一个非常有趣的案例，因为报文一次以一个字节进入物理层并以相同的方式离开，但它说明了字符序列的绘制方式。

第 372 页的图 11-9 显示了来自多路复用器的传入 Dword 报文。每个字节被定向到相应的 Lane。最后，第 373 页的图 11-10 说明了一个八 Lane (x8) 链路。在此示例中，需要两个 Dword 才能填充所有 8 个 Lane。这要求 Dword 以比先前示例快两倍的速率到达。每个 Lane 上发送的数据格式将在以下小节中描述。

**371**

## **PCI Exress Technology**

_图 11-8：x1 字节交叉_

**==> 图片 [154 x 220] 已省略 <==**

**----- 图片文字开始 -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- 图片文字结束 -----**<br>


_图 11-9：x4 字节交叉_

**==> 图片 [338 x 205] 已省略 <==**

**----- 图片文字开始 -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- 图片文字结束 -----**<br>


**372**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-10：使用 DWord 并行数据的 x8 字节交叉_

**==> 图片 [368 x 240] 已省略 <==**

**----- 图片文字开始 -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- 图片文字结束 -----**<br>


## **报文格式规则**

## **一般规则**

- 每个报文的总报文长度（包括起始和结束字符）始终是四的倍数。这是数据长度以 dword 为单位测量的自然扩展。

- TLP 以 STP 字符开始，以 END 或 EDB 字符结束。

- DLLP 以 SDP 开始，以 END 字符结束。并且正好 8 个字符长 (SDP + 6 字符 + END)。

- STP 和 SDP 字符在逻辑空闲传输之后开始报文传输时放置在 Lane 0 上。在其他情况下，它们可以从可被 4 整除的 Lane 编号开始。

- 接收方的物理层允许监视这些规则的违规行为，并可能将其作为接收方错误报告给数据链路层。

**373**

**PCI Exress Technology**

## **示例：x1 格式**

第 374 页的图 11-11 中所示的示例说明了通过 x1 链路（仅一个 Lane 运行的链路）传输的报文的格式。显示了一系列报文，其中穿插了一个 SKIP 有序集。末尾显示了逻辑空闲，以表示发送方没有更多报文要发送并使用空闲字符作为填充的情况。

_图 11-11：x1 报文格式_

**==> 图片 [351 x 220] 已省略 <==**

**----- 图片文字开始 -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- 图片文字结束 -----**<br>


## **x4 格式规则**

- STP 和 SDP 字符始终在 Lane 0 上发送。

- END 和 EDB 字符始终在 Lane 3 上发送。

- 当发送有序集（如 SKIP）时，它必须同时出现在所有 Lane 上。

- 当传输逻辑空闲时，它们必须同时在所有 Lane 上发送。

- 这些规则的任何违规都可能作为接收方错误报告给数据链路层。

**374**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **示例 x4 格式**

第 375 页的图 11-12 中所示的示例说明了通过 x4 链路（具有四个运行数据 Lane 的链路）发送的报文的格式。该图显示了一个 TLP，后跟在所有 Lane 上传输的用于接收方时钟补偿的 SKIP 有序集。接下来是一个 DLLP，然后是所有 Lane 上的逻辑空闲。本例强调了报文始终是 4 的字符倍数，因为起始字符始终出现在 Lane 0 中，而结束字符始终在 Lane 3 中。它还说明了有序集必须同时出现在所有 Lane 上。

_图 11-12：x4 报文格式_

**375**

**PCI Exress Technology**

## **大链路宽度报文格式规则**

以下规则适用于通过 x8、x12、x16 或 x32 链路传输报文时：

- 当在传输逻辑空闲期间之后开始传输时，STP/SDP 字符始终在 Lane 0 上发送。之后，当发送背靠背报文时，它们只能发送到可被 4 整除的 Lane 编号（Lane 4、8、12 等）。

- END/EDB 字符发送到可被 4 整除的 Lane 编号，然后减一（Lane 3、7、11 等）。

- 如果报文没有在链路的最后一个 Lane 上结束，并且没有更多准备发送的报文，则 PAD 符号用作剩余 Lane 编号的填充。逻辑空闲不能用于此目的，因为它必须同时出现在所有 Lane 上。

- 有序集必须同时在所有 Lane 上发送。

- 类似地，逻辑空闲在使用时必须在所有 Lane 上发送。

- 这些规则的任何违规都可能作为接收方错误报告给数据链路层。

## **x8 报文格式示例**

第 377 页的图 11-13 中所示的示例说明了通过 x8 链路传输的报文的格式。该图显示了一个 TLP，后跟 SKIP 有序集、一个 DLLP，最后是一个在 Lane 3 结束的 TLP。在那时，发送方没有更多准备发送的报文，但当前报文未扩展到包括所有可用 Lane。有人可能期望用逻辑空闲填充额外的 Lane，但这在这里不起作用，因为空闲必须同时出现在所有 Lane 上。因此需要另一个填充字符，规范编写者选择在此处使用 PAD 控制字符。PAD 唯一使用的另一个位置是在训练过程中。最后，由于仍没有更多要发送的报文，因此会在所有 Lane 上发送逻辑空闲。

**376**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-13：x8 报文格式_

## **加扰器**

我们示例中的下一步是加扰，如图 11-5（第 369 页）所示，旨在防止数据流中的重复模式。重复模式在链路上产生"纯音"，这意味着由该模式产生的一致频率会产生比通常更多的噪声或 EMI。通过将此能量扩展到更宽的频率范围来减少此问题是加扰的主要目标。此外，单个 Lane 上的加扰传输还可减少对宽链路上相邻 Lane 的干扰。这种"空间频率去相关"，或减少串扰噪声，有助于每个 Lane 上的接收方区分所需的信号。

**377**

## **PCI Exress Technology**

为了帮助接收方与加扰序列保持同步，控制字符不会进行加扰，因此即使加扰器失去同步，它们也可被识别。此外，COM 控制字符 (K28.5) 的每次到达都会重新初始化链路两端的加扰器，从而重新同步它们。

## **加扰算法**

规范中描述的加扰器如图 11-14（第 378 页）所示。它由一个 16 位线性反馈移位寄存器 (Linear Feedback Shift Register, LFSR) 组成，其反馈点实现以下多项式：

G(x) = X[16] + X[5] + X[4] + X[3] + 1

_图 11-14：加扰器_

LFSR 以馈送数据字节的时钟频率的 8 倍频率进行计时，其输出被计时到 8 位寄存器中，该寄存器与 8 位数据字符进行 XOR 以形成加扰的数据输出。

**378**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **一些加扰器实现规则：**

- 在多 Lane 链路实现中，与每个 Lane 相关联的加扰器必须协同工作，在每个 LFSR 中保持相同的同步值。

- 加扰仅应用于 'D' 字符，即与 TLP 和 DLLP 以及逻辑空闲 (00h) 字符相关联的字符。但是，TS1 和 TS2 有序集内的那些 'D' 字符不会被加扰。

- 加扰从不应用于 'K' 字符和有序集中的字符，例如 TS1、TS2、SKIP、FTS 和电子空闲。这些字符绕过加扰器逻辑。其中一个原因是确保即使加扰器意外失去顺序，它们仍然可以被接收方识别。

- 合规性模式字符（用于测试）也不会被加扰。

- COM 字符（不会被加扰的控制字符）用于将链路两端的 LFSR 重新初始化为 FFFFh。

- 除 COM 字符外，LFSR 通常对每个发送的 D 或 K 字符串行前进 8 次，但它在与 SKIP 有序集关联的 SKP 字符上不前进。原因在于接收方可能会添加或删除 SKP 符号以执行时钟容限补偿。改变接收方中的字符数与发送的字符数相比，如果不忽略这些字符，则会导致接收方 LFSR 中的值与发送方 LFSR 值失去同步。

## **禁用加扰**

加扰默认启用，但规范允许出于测试和调试目的禁用它。这是因为测试可能需要控制发送的确切比特模式，并且由于硬件处理加扰，因此软件没有合理的方法来强制执行特定模式。规范未定义用于指示物理层禁用加扰的特定软件机制，因此这必须是特定于设计的实现。

如果设备禁用了加扰，则通过在控制字段中设置适当的位来发送至少两个 TS1 和 TS2 与相邻设备通信，如第 539 页的"配置状态"所述。作为响应，相邻设备也禁用其加扰。

**379**

**PCI Exress Technology**

## **8b/10b 编码**

## **概述**

PCIe 的前两代使用 8b/10b 编码。每个 Lane 实现一个 8b/10b 编码器，将 8 位字符转换为 10 位符号。此编码方案由 IBM 于 1984 年获得专利，今天广泛用于许多串行传输，例如千兆以太网和光纤通道。

## **动机**

编码为串行传输实现了几个理想的目标。其中最重要的三个列在此处：

- **将时钟嵌入数据中。** 编码可确保数据流中具有足够的跳变以在接收方恢复时钟，结果是不需要分布式时钟。这避免了并行总线设计的一些限制，例如飞行时间和时钟偏移。它还消除了分配高频时钟的需要，否则会导致其他问题，例如增加的 EMI 和困难的布线。

   - 作为此过程的示例，第 381 页的图 11-15 显示了数据字节 00h 的编码结果。可以看到，这个原本没有跳变的 8 位字符转换为具有 5 个跳变的 10 位符号。8b/10b 保证足够的跳变以确保比特流中的"游程长度"（连续 1 或 0 的序列）在任何条件下不超过 5 个连续位。

- **维持直流平衡。** PCIe 使用交流耦合链路，将电容器串联放置在路径中，以将信号的直流部分与链路的另一端隔离。这允许发送方和接收方使用不同的共模电压，并且对于它们之间的路径足够长以至于它们不太可能具有完全相同的参考电压的情况，使电气设计更容易。该直流值或共模电压可以在运行时发生变化，因为当信号被驱动时线路会充电。通常，信号变化得如此之快，以至于没有时间让这引起问题，但是，如果信号平均值主要是一个电平或另一个电平，则共模值将出现漂移。称为"直流漂移"，这种漂移电压会降低接收方的信号完整性。为了进行补偿，8b/10b 编码器跟踪发送的最后一个符号的"差异 (disparity)"。差异或不平等只是简单地表示前一个符号是否有更多的 1（称为正差异），更多的 0（负差异），或者 1 和 0 平衡

**380**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

   - （中性差异）。例如，如果前一个符号具有负差异，则下一个符号应通过使用更多的 1 来平衡。

- **增强错误检测。** 编码方案还有助于检测传输错误。对于 10 位值，可能有 1024 个代码，但待编码的字符只有 256 个唯一代码。为了维持直流平衡，设计为每个字符使用两个代码，并根据发送的最后一个符号的差异选择其中一个，因此将需要 512 个代码。但是，许多中性差异编码具有相同的值（D28.5 就是一个示例），因此并非所有 512 个都被使用。因此，超过一半的可能编码未被使用，如果在接收方看到，则将被视为非法。如果传输错误确实更改了符号的位模式，那么结果很可能是这些可立即识别的非法模式之一。有关更多信息，请参见第 383 页的标题为"差异"的部分。

8b/10b 编码的主要缺点是它所需的开销。从接收方的角度来看，实际传输性能降低了 20%，因为每个字节发送 10 位，但仅在接收方恢复 8 个有效位。这是一个不小的代价，但考虑到前面提到的好处，它仍然被认为是可以接受的。

_图 11-15：8 位字符 00h 编码示例_

**==> 图片 [224 x 112] 已省略 <==**

**----- 图片文字开始 -----**<br>
8b Value<br>0 0 0 0 0 0 0 0<br>Data 00h<br>10b Encoded<br>0 11 0 0 0 1 0 1 1<br>Value<br>**----- 图片文字结束 -----**<br>


## **10 位符号的属性**

如 8b/10b 编码文献中所述，设计并非严格的 8 位到 10 位。相反，它实际上是一个 5 位到 6 位的编码，然后是 3 位到 4 位的编码。子块是设计内部的，但它们的存在有助于解释合法符号的一些属性，如下所列。不遵循这些属性的符号被视为无效。

**381**

**PCI Exress Technology**

- 比特流从不包含超过五个连续的 1 或 0，即使从一个符号的末尾到下一个符号的开头也是如此。

- 每个 10 位符号包含：

   - 四个 0 和六个 1（不一定连续），或

   - 六个 0 和四个 1（不一定连续），或

   - 五个 0 和五个 1（不一定连续）。

- 每个 10 位符号被细分为两个子块：第一个是六位宽，第二个是四位宽。

   - 6 位子块包含不超过四个 1 或四个 0。

   - 4 位子块包含不超过三个 1 或三个 0。

## **字符表示法**

8b/10b 使用一种特殊的简写符号表示法，第 382 页的图 11-16 说明了为给定字符得出简写符号的步骤：

1. 将字符划分为其 3 位和 5 位子块。

2. 转置子块的位置。

3. 为每个子块创建十进制等效值。

4. 字符采用 Dxx.y（数据字符）或 Kxx.y（控制字符）的形式。在此表示法中，xx 是 5 位字段的十进制等效值，y 是 3 位字段的十进制等效值。

_图 11-16：8b/10b 命名法_

**==> 图片 [348 x 211] 已省略 <==**

**----- 图片文字开始 -----**<br>
8b Designation Example Data (6Ah)<br>D/<br>8b Character 7 6 5 4 3 2 1 0 D 01101010<br>K#<br>Partition into D/ H G F E D C B A<br>D 011 01010<br>sub-blocks K#<br>Flip sub-blocks K#D/ E D C B A H G F D 01010 011<br>Convert sub-blocks<br>to decimal notation D/K xx . y D 10 . 3<br>Final Notation D/Kxx.y D10.3<br>**----- 图片文字结束 -----**<br>


**382**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **差异**

**定义。** 差异是指 10 位符号内 1 和 0 的数量之间的不等式，并用于帮助维持链路上的直流平衡。具有更多 0 的符号称为具有负 (-) 差异，而具有更多 1 的符号具有正 (+) 差异。当符号具有相等数量的 1 和 0 时，称为具有中性差异。有趣的是，大多数字符编码为具有 + 或 – 差异的符号，但有些仅编码为具有中性差异的符号。

**CRD (当前运行差异)。** CRD 是关于链路上差异的当前状态的信息。由于它只是一个位，因此它只能为正或负，并且并不总是在发送下一个符号时更改。要查看它的工作原理，请记住下一个解码的符号可能具有负、中性或正差异，然后考虑以下示例。如果 CRD 为正，则具有负差异的传出符号将把它更改为负，中性差异将保持为正，正差异将是错误，因为 CRD 仅一位，不能变得更正。

CRD 的初始状态（在传输任何字符之前）可能与发送方和接收方之间不匹配，但事实证明这并不重要。当接收方在训练完成后看到第一个符号时，它将检查差异错误，如果发现，则只需更改 CRD。这不会被视为错误，而只是 CRD 调整以匹配接收方和发送方。之后，只有两种合法的 CRD 情况：如果新符号具有中性差异，则它可以保持不变；如果新符号具有相反的差异，则它可以翻转为相反极性。新符号的差异与 CRD 相同是不合法的。这样的事件将是差异错误，除非发生错误，否则在初始调整之后永远不会发生。

## **编码过程**

可以通过不同方式完成 8b/10b 编码。最简单的方法可能是实现一个包含所有可能输出值的查找表。但是，此表可能需要相对大量的门。另一种方法是将解码器实现为逻辑块，这通常是首选，因为它通常会产生更小且更便宜的解决方案。编码逻辑的细节在所引用的文献中有详细描述，因此我们将重点放在其工作原理的更大图景上。

**383**

## **PCI Exress Technology**

示例 8b/10b 框图如图 11-17（第 384 页）所示。新的传出符号基于以下三件事创建：传入字符、该字符的 D/K# 指示以及 CRD。基于传出符号计算新的 CRD 值，并反馈用于编码下一个字符。编码后，生成的符号被馈送到串行器，该串行器将各个位计时输出。图 11-18（第 385 页）显示了一些示例 8b/10b 编码，这些编码对后续示例很有用。

_图 11-17：8 位到 10 位 (8b/10b) 编码器_

**==> 图片 [343 x 244] 已省略 <==**

**----- 图片文字开始 -----**<br>
Bytes from Scrambler D/K#<br>8b Character 7 6 5 4 3 2 1 0<br>H G F E D C B A<br>8b/10b Encoding Logic<br>Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>Serial Stream<br>Serializer j h g f i e d c b a to Transmitter<br>using Tx Clock<br>**----- 图片文字结束 -----**<br>


**384**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-18：示例 8b/10b 编码_

## **示例传输**

图 11-19 说明了三个字符的编码和传输：第一个和第二个是控制字符 K28.5，第三个字符是数据字符 D10.3。

在此示例中，初始 CRD 为负，因此 K28.5 编码为 001111 1010b。此符号具有正差异（1 多于 0），并导致 CRD 极性翻转为正。下一个 K28.5 编码为 110000 0101b，具有负差异。这导致 CRD 这次翻转为负。最后，D10.3 编码为 010101 1100b。由于其差异为中性，因此 CRD 在此情况下不会更改，但保持为负，以供下一个字符使用。

**385**

**PCI Exress Technology**

_图 11-19：示例 8b/10b 传输_

## **在以下示例中使用这两个字符：**

|**D/K#**|**十六进制**<br>**字节**|**二进制位**<br>**HGF EDCBA**|**字节**<br>**名称**|**CRD –**<br>**abcdei fghj**|**CRD +**<br>**abcdei fghj**|
|---|---|---|---|---|---|
|**控制(K)**|**BC**|**101 11100**|**K28.5**|**001111 1010**|**110000 0101**|
|**数据(D)**|**6A**|**011 01010**|**D10.3**|**010101 1100**|**010101 0011**|



## **示例传输**

||**CRD**|**字符**|**CRD**|**字符**|**CRD**|**字符**|**CRD**|
|---|---|---|---|---|---|---|---|
|**要传输的**<br>**字符**|**-**|**K28.5 (BCh)**|**+**|**K28.5 (BCh)**|**-**|**D10.3 (6Ah)**|**-**|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-5"></a>
## 9.5 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|**Bit stream**<br>**transmitted**||**Yields**<br>**001111 1010**<br>**CRD is +**||**Yields**<br>**110000 0101**<br>**CRD is -**||**Yields**<br>**010101 1100**<br>**CRD is neutral**||
|Initialized value of CRD is don’t care. Receiver can determine from incoming bit stream||||||||



## **Control Characters** 

The 8b/10b encoding provides several special characters for Link management and Table 11‐1 on page 386 shows their encoding. 

_Table 11‐1: Control Character Encoding and Definition_ 

|**8b/10b**<br>**Name**|**Description**|
|---|---|
|K28.5|First character in any ordered set. Also used by Rx<br>to achieve Symbol lock during training.|
|K23.7|Packet filler|
|K28.0|Used in SKIP ordered set for Clock Tolerance Com‐<br>pensation|



**386** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐1: Control Character Encoding and Definition (Continued)_ 

|**Character**<br>**Name**|**8b/10b**<br>**Name**|**Description**|
|---|---|---|
|STP|K27.7|Start of a TLP|
|SDP|K28.2|Start of a DLLP|
|END|K29.7|End of Good Packet|
|EDB|K30.7|End of a bad or ‘nullified’ TLP.|
|FTS|K28.1|Used to exit from L0s low power state to L0|
|IDL|K28.3|Used to place Link into Electrical Idle state|
|EIE|K28.7|Part of the Electrical Idle Exit Ordered Set sent<br>prior to bringing the Link back to full power for<br>speeds higher than 2.5 GT/s|



- **COM** (Comma): One of the main functions of this is to be the first Symbol in the physical layer communications called ordered sets (see “Ordered sets” on page 388). It has an interesting property that makes both of its Symbol encodings easily recognizable at the receiver: they start with two bits of one polarity followed by five bits of the opposite polarity (001111 1010 or 110000 0101). This property is especially helpful for initial training, when the receiver is trying to make sense of the string of bits coming in, because it helps the receiver lock onto the incoming Symbol stream. See “Link Training and Initialization” on page 405 for more on how this works. 

- • **PAD** : On a multi‐Lane Link, if a packet to be sent doesn’t cover all the avail‐ able lanes and there are no more packets ready to send, the PAD character is used to fill in the remaining Lanes. 

- **SKP** (Skip): This is used as part of the SKIP ordered set that is sent periodi‐ cally to facilitate clock tolerance compensation. 

- **STP** (Start TLP): Inserted to identify the start of a TLP. 

- **SDP** (Start DLLP): Inserted to identify the start of a DLLP. 

- **END** : Appended to identify the end of an error‐free TLP or DLLP. 

- **EDB** (EnD Bad): Inserted to identify the end of a TLP that a forwarding device (such as a switch) wishes to ‘nullify’. This case can arise when a switch using the “cut‐through mode” forwards a packet from an ingress port to an egress port without buffering the whole packet first. Any error detected during the forwarding process creates a problem because a portion of the packet is already being delivered before the packet can be checked for 

**387** 

**PCI Ex ress Technolo p gy** 

errors. To handle this case, the switch must cancel the one that’s already in route to the destination. This is accomplished by nullifying it: ending the packet with EDB and inverting the LCRC from what it should have been. When a receiver sees a nullified packet, it discards the packet and does not return an ACK or NAK. (See the “Example of Cut‐Through Operation” on page 356.) 

- **FTS** (Fast Training Sequence): Part of the FTS ordered set sent by a device to recover a link from the L0s standby state back to the full‐on L0 state. 

- **IDL** (Idle): Part of the Electrical Idle ordered set sent to inform the receiver that the Link is transitioning into a low power state. 

- **EIE** (Electrical Idle Exit): Added in the PCIe 2.0 spec and used to help an electrically‐idle link begin the wake up process. 

## **Ordered sets** 

**General.** Ordered Sets are used for communication between the Physical Layers of Link partners and may be thought of as Lane management pack‐ ets. By definition they are a series of characters that are not TLPs or DLLPs. For Gen1 and Gen2 they always begin with the COM character. Ordered Sets are replicated on all Lanes at the same time, because each Lane is tech‐ nically an independent serial path. This also allows Receivers to verify alignment and de‐skewing. Ordered Sets are used for things like Link train‐ ing, clock tolerance compensation, and changing Link power states. 

**TS1 and TS2 Ordered Set (TS1OS/TS2OS).** Training sequences one and two are used for Link initialization and training. They allow the Link partners to achieve bit lock and Symbol lock, negotiate the link speed, and report other variables associated with Link operation. They are described in more detail in the section titled “TS1 and TS2 Ordered Sets” on page 510. 

**Electrical Idle Ordered Set (EIOS).** A Transmitter that wishes to go to a lower‐power link state sends this before ceasing transmission. Upon receipt, Receivers know to prepare for the low power state. The EIOS con‐ sists of four Symbols: the COM Symbol followed by three IDL Symbols. Receivers detect this Ordered Set and prepare for the Link to go to into Elec‐ trical Idle by ignoring input errors until exiting from Electrical Idle. Shortly after sending EIOS, the Transmitter reduces its differential voltage to less than 20mV peak. 

**FTS Ordered Set (FTSOS).** A Transmitter sends the proper number of these (the minimum number was given by the Link neighbor during train‐ ing) to take a Link from the low‐power L0s state back to the fully‐opera‐ tional L0 state. The receiver detects the FTSs, recognizes that the Link is 

**388** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

exiting from Electrical Idle, and uses them to recover Bit and Symbol Lock.The FTS Ordered Set consists of four Symbols: the COM Symbol fol‐ lowed by three FTS Symbols. 

**SKP Ordered Set (SOS).** This consists of four Symbols: the COM Symbol followed by three SKP Symbols. It’s transmitted at regular intervals and is used for Clock Tolerance Compensation as described in “Clock Compensa‐ tion” on page 391 and “Receiver Clock Compensation Logic” on page 396. Basically, the Receiver evaluates the SOS and internally adds or removes SKP Symbols as needed to prevent its elastic buffer from under‐flowing or over‐flowing. 

**Electrical Idle Exit Ordered Set (EIEOS).** Added in the PCIe 2.0 spec, this Ordered Set was defined to provide a lower‐frequency sequence required to exit the electrical idle Link state. The EIEOS for 8b/10b encod‐ ing, uses repeated K28.7 control characters to appear as a repeating string of 5 ones followed by 5 zeros. This low frequency string produces a low‐fre‐ quency signal that allows for higher signal voltages that are more readily detected at the receiver. In fact, the spec states that this pattern guarantees that the Receiver will properly detect an exit from Electrical Idle, something that scrambled data cannot do. For details on electrical idle exit, refer to the section “Electrical Idle” on page 736. 

## **Serializer** 

The 8b/10b encoder on each lane feeds a serializer that clocks the Symbols out in bit order (see Figure 11‐17 on page 384), with the least significant bit (a) shifted out first and the most significant bit (j) shifted out last. For each lane, the Sym‐ bols will be supplied to the serializer at either 250MHz or 500MHz to support a serial bit rate 10 times faster than that at 2.5 GHz or 5.0 GHz. 

## **Differential Driver** 

The differential driver that actually sends the bit stream onto the wire uses NRZ encoding. NRZ simply means that there are no special or intermediate voltage levels used. Differential signalling improves signal integrity and allows for both higher frequencies and lower voltages. Details regarding the electrical charac‐ teristics of the driver are discussed in the section “Transmitter Voltages” on page 462. 

**389** 

**PCI Ex ress Technolo p gy** 

## **Transmit Clock (Tx Clock)** 

The serialized output on each Lane is clocked out by the Tx Clock signal. As mentioned earlier, the clock frequency must be accurate to +/–300ppm around the center frequency (600ppm total variation). There are two options regarding the source of this clock. It can be generated internally or derived from an exter‐ nal reference that may optionally be available. The PCIe spec for peripheral cards includes the definition of a 100MHz reference clock supplied by the sys‐ tem board for this purpose. This reference clock is multiplied internally to derive the local clock that drives the internal logic and the Tx clock used by the serializer. 

## **Miscellaneous Transmit Topics** 

## **Logical Idle** 

In order to keep the receiver’s PLL from drifting, something must be transmit‐ ted during periods when there are no TLPs, DLLPs or ordered sets to transmit, and it is logical idle characters that are injected into the character flow during these times. Some properties of the logical idle character: 

- It’s an 8‐bit Data character with a value of 00h. 

- When sent, it goes on all Lanes at the same time and the Link is said to be in the logical idle state (not to be confused with electrical Idle—the state when the output driver stops transmitting altogether and the receiver PLL loses synchronization). 

- The logical idle character is scrambled, but a receiver can distinguish it from other data because it occurs outside of a packet framing context (i.e.: after an END or EDB, but before an STP or SDP). 

- It is 8b/10b encoded. 

- During logical idle transmission, SKIP ordered sets are still sent periodi‐ cally. 

## **Tx Signal Skew** 

Understandably, the transmitter should introduce a minimal skew between lanes to leave as much Rx skew budget as possible for routing and other varia‐ tions. The spec lists the Tx skew values as 500ps + 2 UI for Gen1, 500ps + 4UI for Gen2, and 500ps + 6 UI for Gen3. Recalling that UI (unit interval) represents one bit time on the Link, this works out as shown in Table 11‐2 below. 

**390** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐2: Allowable Transmitter Signal Skew_ 

|**Spec Version**|**Allowable Tx Skew**|
|---|---|
|Gen1|1300 ps|
|Gen2|1300 ps|
|Gen3|1250 ps|



## **Clock Compensation** 

**Background.** High‐speed serial transports like PCIe have a particular clock problem to solve. The receiver recovers a clock from the incoming bit stream and uses that to latch in the data bits, but this recovered clock is not synchronized with the receiver’s internal clock and at some point it has to begin clocking the data with its own internal clock. Even if they have an optional common external reference clock, the best they can do is to gener‐ ate an internal clock within a specified tolerance of the desired frequency. Consequently, one of the clocks will almost always have a slightly higher frequency than the other. If the transmitter clock is faster, the packets will be arriving faster than they can be taken in. To compensate, the transmitter must inject some “throw‐away characters” in the bit stream that the receiver can discard if it proves necessary to avoid a buffer over‐run condition. For PCIe, these characters which can be deleted take the form of the SKIP ordered set, which consists of a COM character followed by three SKP char‐ acters (see Figure 11‐20). For more detail on this topic, refer to “Receiver Clock Compensation Logic” on page 396). 

**SKIP ordered set Insertion Rules.** A transmitter is required to send SKIP ordered sets on a periodic basis, and the following rules apply: 

- The SKIP ordered set must be scheduled for insertion between 1180 and 1538 Symbol times (a Symbol time is the time required to send one Symbol and is 10 bit times, so at 2.5 GT/s, a Symbol time is 4ns and at 5.0 GT/s, it’s 2ns).

</td>
<td style="background-color:#e8e8e8">

|**传输的位流**||**产生**<br>**001111 1010**<br>**CRD 为 +**||**产生**<br>**110000 0101**<br>**CRD 为 -**||**产生**<br>**010101 1100**<br>**CRD 为中性**||
|CRD 的初始值为无关项 (don't care)。接收器可以从输入位流中确定||||||||
## **控制字符 (Control Characters)**

8b/10b 编码提供了多个用于链路管理的特殊字符，第 386 页的表 11-1 显示了它们的编码。

_表 11-1：控制字符编码及定义_

|**8b/10b 名称**|**描述**|
|---|---|
|K28.5|任何有序集合 (Ordered Set) 中的第一个字符。也用于接收器在训练期间实现 Symbol 锁定 (Symbol Lock)。|
|K23.7|数据包填充字符|
|K28.0|用于 SKIP 有序集合中进行时钟容差补偿 (Clock Tolerance Compensation)|

**386**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_表 11-1：控制字符编码及定义（续）_

|**字符名称**|**8b/10b 名称**|**描述**|
|---|---|---|
|STP|K27.7|TLP 的起始|
|SDP|K28.2|DLLP 的起始|
|END|K29.7|正常数据包的结束|
|EDB|K30.7|错误的或"作废" TLP 的结束|
|FTS|K28.1|用于从 L0s 低功耗状态退出到 L0|
|IDL|K28.3|用于将链路置于电气空闲 (Electrical Idle) 状态|
|EIE|K28.7|电气空闲退出有序集合 (Electrical Idle Exit Ordered Set) 的一部分，在链路恢复到高于 2.5 GT/s 的全功耗状态之前发送|

- **COM**（逗号，Comma）：其主要功能之一是作为物理层通信中称为有序集合（参见第 388 页"有序集合"）的第一个字符。它有一个有趣的特性，使其两种字符编码都容易被接收器识别：它们以两个相同极性的位开始，后跟五个相反极性的位（001111 1010 或 110000 0101）。这个特性在初始训练时特别有用，因为接收器试图理解输入的位串时，这有助于接收器锁定输入的字符流。有关其工作原理的更多内容，请参见第 405 页的"链路训练与初始化 (Link Training and Initialization)"。

- **PAD**：在多通道 (Lane) 链路上，如果要发送的数据包不能覆盖所有可用通道，并且没有其他数据包准备好发送，则使用 PAD 字符填充剩余的通道。

- **SKP**（Skip）：用作 SKIP 有序集合的一部分，定期发送以促进时钟容差补偿。

- **STP**（Start TLP，TLP 起始）：插入以标识 TLP 的开始。

- **SDP**（Start DLLP，DLLP 起始）：插入以标识 DLLP 的开始。

- **END**：附加在无错误的 TLP 或 DLLP 末尾以标识其结束。

- **EDB**（EnD Bad）：插入以标识一个 TLP 的结束，转发设备（如交换机）希望将其"作废"。这种情况可能出现在交换机使用"直通模式 (cut-through mode)"将数据包从入端口转发到出端口而没有首先缓冲整个数据包的情况下。在转发过程中检测到任何错误都会产生问题，因为部分数据包在完成错误检查之前已经被发送出去了。

**387**

**PCI Ex ress Technolo p gy**

为了处理这种情况，交换机必须取消已经在传输过程中的那个数据包。这是通过作废来完成的：用 EDB 结束数据包并将 LCRC 从其应有的值反相。当接收器看到一个被作废的数据包时，它会丢弃该数据包并且不返回 ACK 或 NAK。（参见第 356 页的"直通操作示例 (Example of Cut-Through Operation)"。）

- **FTS**（Fast Training Sequence，快速训练序列）：FTS 有序集合的一部分，由设备发送以将链路从 L0s 待命状态恢复到完全运行的 L0 状态。

- **IDL**（Idle，空闲）：电气空闲有序集合的一部分，发送给接收器通知它链路正在转换到低功耗状态。

- **EIE**（Electrical Idle Exit，电气空闲退出）：在 PCIe 2.0 规范中添加，用于帮助电气空闲链路开始唤醒过程。

## **有序集合 (Ordered sets)**

**概述。** 有序集合用于链路伙伴 (Link partners) 的物理层之间的通信，可以被视为通道管理包 (Lane management packets)。按定义，它们是一系列既不是 TLP 也不是 DLLP 的字符。对于 Gen1 和 Gen2，它们始终以 COM 字符开始。有序集合在所有通道上同时复制，因为每个通道技术上是一条独立的串行路径。这还允许接收器验证对齐和去偏斜 (de-skewing)。有序集合用于链路训练、时钟容差补偿以及更改链路功耗状态等操作。

**TS1 和 TS2 有序集合 (TS1OS/TS2OS)。** 训练序列一和二用于链路初始化和训练。它们允许链路伙伴实现位锁定 (bit lock) 和字符锁定 (Symbol lock)，协商链路速度，并报告与链路操作相关的其他变量。在第 510 页题为"TS1 和 TS2 有序集合"的部分中详细介绍了它们。

**电气空闲有序集合 (EIOS)。** 希望转换到更低功耗链路状态的发送器在停止传输之前发送此集合。收到后，接收器知道准备进入低功耗状态。EIOS 由四个字符组成：COM 字符后跟三个 IDL 字符。接收器检测到此有序集合，并通过忽略输入错误直到退出电气空闲来准备链路进入电气空闲状态。发送 EIOS 后不久，发送器将其差分电压降低到小于 20mV 的峰值。

**FTS 有序集合 (FTSOS)。** 发送器发送适当数量的这些集合（最小数量由链路相邻设备在训练期间给出）以将链路从低功耗 L0s 状态恢复到完全运行的 L0 状态。接收器检测到 FTS，识别到链路正在退出电气空闲状态，并使用它们恢复位和字符锁定。FTS 有序集合由四个字符组成：COM 字符后跟三个 FTS 字符。

**388**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

**SKP 有序集合 (SOS)。** 它由四个字符组成：COM 字符后跟三个 SKP 字符。它定期发送，用于时钟容差补偿，如第 391 页的"时钟补偿 (Clock Compensation)"和第 396 页的"接收器时钟补偿逻辑 (Receiver Clock Compensation Logic)"中所述。基本上，接收器评估 SOS 并根据需要在其内部添加或移除 SKP 字符，以防止其弹性缓冲区 (elastic buffer) 下溢或溢出。

**电气空闲退出有序集合 (EIEOS)。** 在 PCIe 2.0 规范中添加，定义此有序集合是为了提供退出电气空闲链路状态所需的低频序列。8b/10b 编码的 EIEOS 使用重复的 K28.7 控制字符，呈现为重复的 5 个 1 后跟 5 个 0 的字符串。这个低频字符串产生一个低频信号，该信号允许更高的信号电压，更容易被接收器检测到。事实上，规范指出此模式保证接收器将正确检测到电气空闲退出，而加扰数据无法做到这一点。有关电气空闲退出的详细信息，请参阅第 736 页的"电气空闲 (Electrical Idle)"。

## **串行器 (Serializer)**

每个通道上的 8b/10b 编码器馈入一个串行器 (serializer)，该串行器按位顺序将字符移出（参见第 384 页的图 11-17），最低有效位 (a) 最先移出，最高有效位 (j) 最后移出。对于每个通道，字符将以 250MHz 或 500MHz 的频率提供给串行器，以支持 2.5 GHz 或 5.0 GHz 时 10 倍快的串行比特率。

## **差分驱动器 (Differential Driver)**

实际将位流发送到线路上的差分驱动器使用 NRZ 编码。NRZ 简单地意味着不使用特殊的或中间的电压电平。差分信号改善了信号完整性，并允许更高的频率和更低的电压。有关驱动器电气特性的详细信息在第 462 页的"发送器电压 (Transmitter Voltages)"部分讨论。

**389**

**PCI Ex ress Technolo p gy**

## **发送时钟 (Tx Clock)**

每个通道上的串行化输出由 Tx Clock 信号定时移出。如前所述，时钟频率必须精确到中心频率的 +/–300ppm（总共 600ppm 变化）。关于此时钟的来源有两个选项。它可以内部生成，也可以从可能可选的外部参考时钟派生。PCIe 规范对外围卡的定义包括系统板提供的 100MHz 参考时钟，用于此目的。该参考时钟在内部倍频以派生驱动内部逻辑的本地时钟和串行器使用的 Tx 时钟。

## **其他发送主题**

## **逻辑空闲 (Logical Idle)**

为了保持接收器的 PLL 不漂移，在没有 TLP、DLLP 或有序集合可传输的时段必须传输某些东西，逻辑空闲字符在这些时间被注入到字符流中。逻辑空闲字符的一些特性：

- 它是一个值为 00h 的 8 位数据字符。

- 发送时，它同时在所有通道上进行，链路被称为处于逻辑空闲状态（不要与电气空闲混淆——电气空闲是输出驱动器完全停止传输且接收器 PLL 失去同步的状态）。

- 逻辑空闲字符被加扰，但接收器可以将其与其他数据区分开来，因为它发生在数据包成帧上下文之外（即：在 END 或 EDB 之后，但在 STP 或 SDP 之前）。

- 它是 8b/10b 编码的。

- 在逻辑空闲传输期间，SKIP 有序集合仍然定期发送。

## **Tx 信号偏斜 (Tx Signal Skew)**

可以理解的是，发送器应在通道之间引入最小偏斜，以便为路由和其他变化保留尽可能多的 Rx 偏斜预算。规范列出 Gen1 的 Tx 偏斜值为 500ps + 2 UI，Gen2 为 500ps + 4 UI，Gen3 为 500ps + 6 UI。回想一下，UI（单位间隔）表示链路上的一个位时间，这等同于下表 11-2 所示。

**390**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_表 11-2：允许的发送器信号偏斜_

|规范版本|允许的 Tx 偏斜|
|---|---|
|Gen1|1300 ps|
|Gen2|1300 ps|
|Gen3|1250 ps|

## **时钟补偿 (Clock Compensation)**

**背景。** 像 PCIe 这样的高速串行传输有一个特定的时钟问题需要解决。接收器从输入位流中恢复时钟并使用该时钟锁存数据位，但恢复的时钟并未与接收器的内部时钟同步，在某些时候它必须开始使用自己的内部时钟对数据进行计时。即使它们具有可选的公共外部参考时钟，它们能做的最好的事情是生成一个在所需频率的指定容差内的内部时钟。因此，几乎总是其中一个时钟的频率会略高于另一个。如果发送器时钟更快，则数据包将以比它们能被接收的速度更快的速度到达。为了补偿，发送器必须在位流中注入一些"可丢弃字符"，接收器如果证明有必要可以丢弃这些字符以避免缓冲区溢出情况。对于 PCIe，这些可以删除的字符采用 SKIP 有序集合的形式，由一个 COM 字符后跟三个 SKP 字符组成（参见图 11-20）。有关此主题的更多详细信息，请参阅第 396 页的"接收器时钟补偿逻辑 (Receiver Clock Compensation Logic)"）。

**SKIP 有序集合插入规则。** 发送器需要定期发送 SKIP 有序集合，以下规则适用：

- SKIP 有序集合必须调度在 1180 到 1538 字符时间内插入（字符时间是发送一个字符所需的时间，是 10 个位时间，因此在 2.5 GT/s 时，字符时间为 4ns；在 5.0 GT/s 时，为 2ns）。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-6"></a>
## 9.6 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- They are only inserted on packet boundaries (nothing is allowed to interrupt a packet) and must go simultaneously on all Lanes. If a packet is already in progress the SKP Ordered Set will have to wait. The maxi‐ mum possible packet size would require more than 4096 Symbol times, though, and during that time several SKIP ordered sets should have 

**391** 

**PCI Ex ress Technolo p gy** 

been sent. This case is handled by accumulating the SKIPs that should have gone out and injecting them all at the next packet boundary. 

- Since this ordered set must be transmitted on all Lanes simultaneously, a multi‐lane link may need to add PAD characters on some Lanes to allow the ordered set to go on all Lanes simultaneously (see Figure 11‐ 13 on page 377). 

- During low‐power link states, any counters used to schedule SKIP ordered sets must be reset. There’s no need for them when the transmit‐ ter isn’t signaling, and it wouldn’t make sense to wake up the link to send them. 

- SKIP ordered sets must not be transmitted while the Compliance Pat‐ tern is in progress. 

_Figure 11‐20: SKIP Ordered Set_ 

**==> picture [128 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
Encoding<br>COM K28.5<br>SKP K28.0<br>SKP K28.0<br>SKP K28.0<br>**----- End of picture text -----**<br>


## **Receive Logic Details (Gen1 and Gen2 Only)** 

Figure 11‐21 shows the receiver logic of the Logical Physical Layer. This section describes packet processing from the time the data is received serially on each lane until the packet byte stream is clocked into the Data Link Layer. 

**392** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐21: Physical Layer Receive Logic Details (Gen1 and Gen2 Only)_ 

**==> picture [283 x 367] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>Control<br>Receive<br>8<br>Rx<br>Buffer<br>8 Control<br>Start/End/Idle/Pad Character Removal and<br>Packet Alignment Check<br>8 D/K#<br>Lane 0 Byte Un-Striping Lane N<br>8 D/K# 8 D/K#<br>De-Scrambler De-Scrambler<br>8 D/K# 8 D/K#<br>Error 8b/10b Error 8b/10b<br>Detect Decoder Detect Decoder<br>Rx Local<br>10 PLL 10<br>Serial-to-Parallel Serial-to-Parallel<br>and Elastic Buffer and Elastic Buffer<br>Rx Clk Rx Clk<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


## **Differential Receiver** 

The first parts of the receiver logic are shown in Figure 11‐22, including the dif‐ ferential input buffer for each lane. The buffer senses peak‐to‐peak voltage dif‐ ferences and determines whether the difference represents a logical one or zero. 

**393** 

**PCI Ex ress Technolo p gy** 

For a detailed discussion of receiver characteristics, see section “Receiver Char‐ acteristics” on page 492. 

_Figure 11‐22: Receiver Logic’s Front End Per Lane_ 

**==> picture [372 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
10-bit Sym bols<br>Symbol<br>Lock<br>Lane<br>Serial-to-Parallel K28.5 Detection Elastic De-skew<br>Converter (Comma Symbol) Buffer Delay<br>10 Circuit 10<br>Differential<br>Input<br>Rx Local<br>Clock Clock<br>Control<br>D+<br>Rx Clock Local<br>Differential<br>Recovery Clock<br>D- Receiver Serial Bit PLL PLL<br>Stream<br>a     b     c     d    e     f     g     h     i      j<br>**----- End of picture text -----**<br>


## **Rx Clock Recovery** 

## **General** 

Next the receiver generates an Rx Clock from the data bit transitions in the input data stream, probably using a PLL. This recovered clock has the same fre‐ quency (2.5 or 5.0 GHz) as that of the Tx Clock that was used to clock the bit stream onto the wire. The Rx Clock is used to clock the inbound bit stream into the deserializer. The deserializer has to be aligned to the 10‐bit Symbol bound‐ ary (a process called achieving Symbol lock), and then its Symbol stream output is clocked into the elastic buffer with a version of the Rx Clock that’s been divided by 10. Even thought both must be accurate to within +/–300ppm of the center frequency, the Rx Clock is probably a little different from the Local Clock and if so, compensation is needed. 

**394** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Achieving Bit Lock** 

Recall that the 8b/10b encoding scheme guarantees the inbound serial Symbol stream will contain frequent transitions. The receiver PLL uses those transitions to create an Rx Clock that is synchronized with the Tx Clock that was used to clock the bit stream out of the transmitter. When the receiver locks on to the Tx Clock frequency, the receiver is said to have achieved **“Bit Lock”** . 

During Link training, the transmitter sends a long series of TS1 and TS2 ordered sets to the receiver, which then uses the bit transitions in them to achieve Bit Lock. There are enough transitions on the Link during normal operation for the receiver to maintain Bit Lock after that. 

## **Losing Bit Lock** 

If the Link is put in a low power state (such as L0s or L1) in which packet trans‐ mission ceases, the receiver will lose synchronization. To avoid having the error circuit see this as an error, the transmitter sends an electrical Idle ordered set (EIOS) before going to the lower power state to tell the receiver to de‐gate its input. 

## **Regaining Bit Lock** 

When the transmitter is ready to wake the Link from the L0s state, it sends a specific number FTS ordered sets (the actual number is design specific) and the receiver uses these to regain bit and Symbol lock. A relatively small number of FTSs are needed to recover and so the recovery latency is short. Because the Link is in the L0s state for a short time, the receiver PLL does not usually drift too far from the Tx Clock before it begins to receive the FTSs. If the Link was instead in the L1 low power state and the transmitter instead starts transmitting TS1OSs. This results in the Link getting re‐trained and wakeup time is longer than L0s wakeup time. Should the Link have a more serious error and the Ack/ Nak mechanism be unsuccessful in error recovery after four attempts of retry‐ ing the TLPs, the Data Link Layer signals the Physical Layer to re‐training the Link. Here again, Bit Lock is re‐established during the re‐training process. 

## **Deserializer** 

## **General** 

The incoming data is clocked into each Lane’s deserializer (serial‐to‐parallel converter) by the Rx clock (see Figure 11‐22 on page 394). The 10‐bit Symbols produced are clocked into the Elastic Buffer using a divided‐by‐10 version of the Rx Clock. 

**395** 

**PCI Ex ress Technolo p gy** 

## **Achieving Symbol Lock** 

When the receive logic starts receiving a bit stream, it is JABOB (just a bunch of bits) with no markers to differentiate Symbols or any boundaries. The receive logic must have a way to find the start and end of a 10‐bit Symbol, and the Comma (COM) Symbol serves this purpose. 

The 10‐bit encoding of the COM Symbol contains two bits of one polarity fol‐ lowed by five bits of the opposite polarity (0011111010b or 1100000101b), mak‐ ing it easily detectable. Recall that the COM Control character, like all other Control characters, is also not scrambled by the transmitter, and that ensures that the desired sequence will be seen at the receiver. Upon detection of the COM, the logic knows that the next bit received will be the first bit of the next 10‐bit Symbol. At that point, the deserializer is said to have achieved **‘Symbol Lock’** . 

The COM Symbol is used to achieve Symbol Lock as follows: 

- During Link training when the Link is first established or when re‐training is needed, and TS1 and TS2 ordered sets are transmitted. 

- When FTS ordered sets are sent to inform the receiver to change the state of the Link from L0s to L0. 

## **Receiver Clock Compensation Logic** 

## **Background** 

We’ve observed before that the clocks used by the transmitter and receiver on either end of a link aren’t required to have exactly the same frequencies. This will be the case whenever the link doesn’t use a common reference clock and introduces the problem that one of them is running slightly faster than the other. The only requirement is that both clocks must be within +/– 300 ppm (parts per million) of the center frequency. Since one could be +300 ppm and the other could be ‐300 ppm in the worst case, the worst separation between them could be 600ppm. That difference translates into a gain or loss of one Symbol clock every 1666 clocks. Once the Link is trained, the receive clock (Rx Clock) in the receiver is the same as the transmit clock (Tx Clock) at the other end of the Link (because the receive clock is derived from the bit stream). 

**396** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Elastic Buffer’s Role** 

To compensate for that worst‐case frequency difference, an elastic buffer (see Figure 11‐22 on page 394) is built into the receive path. Received Symbols are clocked into it using the recovered clock and clocked out using the receiver’s local clock. The Elastic Buffer compensates for the frequency difference by add‐ ing or removing SKP Symbols. When a SKP ordered set arrives, logic watching the status of the elastic buffer makes an evaluation. If the local clock is running faster, Symbols are being clocked out faster than they’re coming in, so the buffer will be approaching an underflow condition. The logic will compensate for this by appending an extra SKP Symbol to the ordered set when it arrives to quickly refill the buffer. On the other hand, if the recovered clock is running faster, the buffer will be approaching an overflow condition and the logic will compensate for that by deleting one of the SKP Symbols to quickly drain the buffer. These actions will make up for difference in rates of arrival and consumption of the Symbols and prevent any confusion or loss of data. 

The transmitter periodically sends the SKIP ordered sets for this purpose. As the name implies, the SKP characters are really disposable characters. Deleting or adding a SKP Symbol prevents a buffer overflow or underflow in the elastic buffer and then they get discarded along with all the other control characters when the Symbols are forwarded to the next layer. Consequently, they use a lit‐ tle bandwidth but don’t otherwise affect the flow of packets at all. 

Although lost Symbols due to an Elastic Buffer overflow or underflow is an error condition, it’s optional for receivers to check for this. If they do, and this situation occurs, a Receiver Error will be indicated to the Data Link Layer. 

The transmitter schedules a SKIP ordered set transmission once every 1180 to 1538 Symbol times. However, if the transmitter starts a maximum sized TLP transmission right at the 1538 Symbol time boundary when a SKIP ordered set is scheduled to be transmitted, the SKIP ordered set transmission is deferred. Receivers must be able to tolerate SKIP ordered sets that have a maximum sepa‐ ration dependent on the maximum packet payload size a device supports. The formula for the maximum number of Symbols ( _n_ ) between SKIP ordered sets is: _n_ = 1538 + (maximum packet payload size + 28) 

The number 28 in the equation is the TLP overhead. It is the largest number of Symbols that would be associated with the header (16 bytes), the optional ECRC (4 bytes), the LCRC (4 bytes), the sequence number (2 bytes) and the framing Symbols STP and END (2 bytes). 

**397** 

**PCI Ex ress Technolo p gy** 

## **Lane-to-Lane Skew** 

## **Flight Time Will Vary Between Lanes** 

For wide links, skew between lanes is an issue that can’t be avoided and which must be compensated at the receiver. Symbols are sent simultaneously on all lanes using the same transmit clock, but they can’t be expected to arrive at the receiver at precisely the same time. Sources of Lane‐to‐Lane skew include: 

- Differences between electrical drivers and receivers

</td>
<td style="background-color:#e8e8e8">

- 它们仅在数据包边界插入（不允许中断数据包），并且必须同时在所有通道上进行。如果数据包已在进行中，SKIP 有序集合将必须等待。最大可能的数据包大小将需要超过 4096 字符时间，尽管在那期间应已发送了几个 SKIP 有序集合。

**391**

**PCI Ex ress Technolo p gy**

此情况通过累积本应发出的 SKIP 并在下一个数据包边界全部注入来处理。

- 由于此有序集合必须同时在所有通道上发送，多通道链路可能需要在某些通道上添加 PAD 字符，以允许有序集合同时在所有通道上进行（参见第 377 页的图 11-13）。

- 在低功耗链路状态期间，用于调度 SKIP 有序集合的任何计数器必须重置。当发送器不发送信号时不需要它们，并且唤醒链路来发送它们也没有意义。

- 在合规模式 (Compliance Pattern) 进行时，不得发送 SKIP 有序集合。

_图 11-20：SKIP 有序集合_

**==> 图片 [128 x 93] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
编码<br>COM K28.5<br>SKP K28.0<br>SKP K28.0<br>SKP K28.0<br>**----- 图片文字结束 -----**<br>


## **接收逻辑详细信息（仅限 Gen1 和 Gen2）**

图 11-21 显示了逻辑物理层的接收器逻辑。本节描述了从数据在每个通道上串行接收到数据包字节流被送入数据链路层 (Data Link Layer) 期间的包处理过程。

**392**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-21：物理层接收逻辑详细信息（仅限 Gen1 和 Gen2）_

**==> 图片 [283 x 367] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
至数据链路层<br>
控制<br>
接收<br>
8<br>
Rx<br>
缓冲区<br>
8 控制<br>
起始/结束/空闲/PAD 字符移除和<br>
包对齐检查<br>
8 D/K#<br>
通道 0 字节解交错 通道 N<br>
8 D/K# 8 D/K#<br>
解扰器 解扰器<br>
8 D/K# 8 D/K#<br>
错误 8b/10b 错误 8b/10b<br>
检测 解码器 检测 解码器<br>
Rx 本地<br>
10 PLL 10<br>
串行转并行 串行转并行<br>
和弹性缓冲区 和弹性缓冲区<br>
Rx 时钟 Rx 时钟<br>
Rx Rx<br>
通道 0 通道 1, ..,N-1 通道 N<br>
**----- 图片文字结束 -----**<br>


## **差分接收器 (Differential Receiver)**

接收器逻辑的第一部分如图 11-22 所示，包括每个通道的差分输入缓冲区。缓冲区感应峰峰值电压差并确定该差值是表示逻辑 1 还是 0。

**393**

**PCI Ex ress Technolo p gy**

有关接收器特性的详细讨论，请参阅第 492 页的"接收器特性 (Receiver Characteristics)"部分。

_图 11-22：每通道接收器逻辑的前端_

**==> 图片 [372 x 217] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
10 位字符<br>
字符<br>
锁定<br>
通道<br>
串行转并行 K28.5 检测 弹性 去偏斜<br>
转换器（逗号字符）缓冲区 延迟<br>
10 电路 10<br>
差分<br>
输入<br>
Rx 本地<br>
时钟 时钟<br>
控制<br>
D+<br>
Rx 时钟 本地<br>
差分<br>
恢复 时钟<br>
D- 接收器 串行位 PLL PLL<br>
流<br>
a     b     c     d    e     f     g     h     i      j<br>
**----- 图片文字结束 -----**<br>


## **Rx 时钟恢复 (Rx Clock Recovery)**

## **概述**

接下来接收器从输入数据流中的数据位转换生成 Rx Clock，可能使用 PLL。这个恢复的时钟具有与用于将位流送上线路的 Tx Clock 相同的频率（2.5 或 5.0 GHz）。Rx Clock 用于将入站位流送入解串器。解串器必须与 10 位字符边界对齐（称为实现字符锁定的过程），然后其字符流输出由 Rx Clock 除以 10 的版本送入弹性缓冲区。即使两者都必须精确到中心频率的 +/–300ppm 以内，Rx Clock 可能与本地时钟略有不同，如果是这样，则需要补偿。

**394**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **实现位锁定 (Achieving Bit Lock)**

回想一下，8b/10b 编码方案保证入站串行字符流将包含频繁的转换。接收器 PLL 使用这些转换来创建与用于将位流移出发送器的 Tx Clock 同步的 Rx Clock。当接收器锁定 Tx Clock 频率时，接收器被称为已实现 **"位锁定 (Bit Lock)"**。

在链路训练期间，发送器向接收器发送一系列长 TS1 和 TS2 有序集合，然后接收器使用其中的位转换来实现位锁定。在此之后的正常操作期间，链路上的转换足以让接收器保持位锁定。

## **失去位锁定 (Losing Bit Lock)**

如果链路被置于低功耗状态（例如 L0s 或 L1）下，数据包传输停止，接收器将失去同步。为了避免错误电路将其视为错误，发送器在进入较低功耗状态之前发送电气空闲有序集合 (EIOS)，以告诉接收器解除其输入选通。

## **重新获得位锁定 (Regaining Bit Lock)**

当发送器准备从 L0s 状态唤醒链路时，它发送特定数量的 FTS 有序集合（实际数量是设计特定的），接收器使用这些集合重新获得位和字符锁定。恢复只需要相对较少的 FTS，因此恢复延迟很短。因为链路在 L0s 状态下的时间很短，接收器 PLL 通常在开始接收 FTS 之前不会从 Tx Clock 漂移太远。如果链路处于 L1 低功耗状态并且发送器改为开始发送 TS1OS。这导致链路被重新训练，唤醒时间比 L0s 唤醒时间长。如果链路有更严重的错误并且在四次重试 TLP 后 Ack/Nak 机制未能成功恢复错误，则数据链路层向物理层发信号以重新训练链路。同样，位锁定在重新训练过程中重新建立。

## **解串器 (Deserializer)**

## **概述**

传入数据由 Rx 时钟定时送入每个通道的解串器（串行转并行转换器）（参见第 394 页的图 11-22）。生成的 10 位字符使用 Rx Clock 除以 10 的版本被送入弹性缓冲区。

**395**

**PCI Ex ress Technolo p gy**

## **实现字符锁定 (Achieving Symbol Lock)**

当接收逻辑开始接收位流时，它是 JABOB（一堆位，没有标记来区分字符或任何边界）。接收逻辑必须有一种方法来找到 10 位字符的开始和结束，逗号 (COM) 字符就是为此目的。

COM 字符的 10 位编码包含两个相同极性的位，后跟五个相反极性的位（0011111010b 或 1100000101b），使其易于检测。回想一下，与所有其他控制字符一样，COM 控制字符也不被发送器加扰，这确保了接收器将看到所需的序列。一旦检测到 COM，逻辑就知道接收到的下一位将是下一个 10 位字符的第一位。此时，解串器被称为已实现 **"字符锁定 (Symbol Lock)"**。

COM 字符用于按如下方式实现字符锁定：

- 在链路训练期间，当链路首次建立或需要重新训练时，发送 TS1 和 TS2 有序集合。

- 当发送 FTS 有序集合以通知接收器将链路状态从 L0s 更改为 L0 时。

## **接收器时钟补偿逻辑 (Receiver Clock Compensation Logic)**

## **背景**

我们之前已经观察到链路两端的发送器和接收器使用的时钟不需要具有完全相同的频率。每当链路不使用公共参考时钟时就会发生这种情况，这就引入了一个问题，其中一个时钟运行得比另一个稍快。唯一的要求是两个时钟都必须精确到中心频率的 +/–300 ppm（百万分之一）以内。由于在最坏的情况下一个可以是 +300 ppm 而另一个是 ‐300 ppm，它们之间的最坏间隔可能是 600ppm。这种差异转化为每 1666 个时钟就有一个字符时钟的增益或损失。一旦链路被训练，接收器中的接收时钟 (Rx Clock) 与链路另一端的发送时钟 (Tx Clock) 相同（因为接收时钟是从位流中派生的）。

**396**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **弹性缓冲区的角色 (Elastic Buffer's Role)**

为了补偿这种最坏情况的频率差，弹性缓冲区（参见第 394 页的图 11-22）被内置到接收路径中。接收到的字符使用恢复的时钟送入其中，并使用接收器的本地时钟送出。弹性缓冲区通过添加或移除 SKP 字符来补偿频率差。当 SKP 有序集合到达时，监视弹性缓冲区状态的逻辑进行评估。如果本地时钟运行得更快，则字符被送出的速度比它们进入的速度更快，因此缓冲区将接近下溢条件。逻辑将通过在有序集合到达时附加额外的 SKP 字符来补偿，以快速重新填充缓冲区。另一方面，如果恢复的时钟运行得更快，缓冲区将接近溢出条件，逻辑将通过删除其中一个 SKP 字符来补偿，以在到达 SKP 时快速排空缓冲区。这些动作将弥补字符到达和消耗速率的差异，并防止任何混淆或数据丢失。

发送器为此目的定期发送 SKIP 有序集合。顾名思义，SKP 字符实际上是一次性字符。删除或添加 SKP 字符可防止弹性缓冲区溢出或下溢，然后在字符被转发到下一层时与其他控制字符一起被丢弃。因此，它们占用一点带宽，但不会以其他方式影响数据包的流动。

尽管由于弹性缓冲区溢出或下溢而丢失字符是错误情况，但接收器可以选择性地检查这一点。如果它们这样做并且发生这种情况，将向数据链路层指示接收器错误 (Receiver Error)。

发送器每 1180 到 1538 字符时间调度一次 SKIP 有序集合传输。但是，如果发送器恰好在 1538 字符时间边界时开始最大尺寸的 TLP 传输，此时正计划发送 SKIP 有序集合，则 SKIP 有序集合传输将延迟。接收器必须能够容忍 SKIP 有序集合，其最大间隔取决于设备支持的最大数据包有效负载大小。SKIP 有序集合之间的最大字符数 ( _n_ ) 的公式为： _n_ = 1538 + (最大数据包有效负载大小 + 28)

公式中的数字 28 是 TLP 开销。它是与头部（16 字节）、可选 ECRC（4 字节）、LCRC（4 字节）、序列号（2 字节）以及成帧字符 STP 和 END（2 字节）相关联的最大字符数。

**397**

**PCI Ex ress Technolo p gy**

## **通道间偏斜 (Lane-to-Lane Skew)**

## **通道间飞行时间不同 (Flight Time Will Vary Between Lanes)**

对于宽链路，通道之间的偏斜是一个不可避免的问题，必须在接收器处进行补偿。字符使用相同的发送时钟在所有通道上同时发送，但不能期望它们在完全相同的时间到达接收器。通道间偏斜的来源包括：

- 电气驱动器和接收器之间的差异

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-7"></a>
## 9.7 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Printed wiring board impedance variations 

- Trace length mismatches 

When the serial bit streams carrying a packet arrive at the receiver, this Lane‐to‐ Lane skew must be removed to receive the bytes in the correct order. This pro‐ cess is referred to as de‐skewing the link. 

## **Ordered sets Help De-Skewing** 

The unique structure of the ordered sets and the fact that they are sent simulta‐ neously on all the lanes makes them useful for detecting timing misalignment between Lanes. The spec doesn’t define a method for doing this but in Gen1 and Gen2 the receiver logic can simply look for the COM character on each lane. If it doesn’t appear at the same time on all Lanes, then the early arriving COMs are delayed until they all match up on all Lanes. 

## **Receiver Lane-to-Lane De-Skew Capability** 

This could be done by adjusting an analog delay line on the incoming signals. Alternatively, it could be done after the elastic buffer, which has the advantage that the arrival time differences are now digitized to Symbol times by the local clock of the receiver (see Figure 11‐23 on page 399). If the input to one lane makes it on a clock edge and another one doesn’t, the early arrival COMs can simply be delayed by the appropriate number of Symbol clocks to line it up with the late arriving COMs. The fact that the maximum allowable skew at the receiver is a multiple of the clock periods infers that the spec writers probably had an implementation like this in mind (see Table 11‐3 on page 399). 

**398** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐3: Allowable Receiver Signal Skew_ 

|Spec Version|Allowable Rx Skew|
|---|---|
|Gen1|20 ns<br>(5 clocks at 4ns per Symbol)|
|Gen2|8 ns<br>(4 clocks at 2ns per Symbol)|
|Gen3|6 ns<br>(4 clocks at 1.25ns per Symbol)|



In Gen3 mode there aren’t any COM characters to use for de‐skewing, but detecting Ordered Sets can still provide the necessary timing alignment. 

## **De-Skew Opportunities** 

An unambiguous pattern is needed on all lanes at the same time to perform de‐ skewing and any ordered set will do. Link training sends these, but the SKIP ordered set is sent regularly during normal Link operation. Checking its arrival time allows the skew to be checked on an ongoing basis in case it might change based on temperature or voltage. If it does, the Link will need to transition to the Recovery LTSSM state to correct it. If that happens while packets are in flight, however, a receiver error may occur and a packet could be dropped, pos‐ sibly resulting in replayed TLPs. 

_Figure 11‐23: Receiver’s Link De‐Skew Logic_ 

**==> picture [307 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
TS1/TS2 TS1/TS2<br>Lane 0 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 1 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 2 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 3 Rx FTS Delay FTS<br>(symbols)<br>COM COM<br>COM COM<br>COM COM<br>COM COM<br>**----- End of picture text -----**<br>


**399** 

**PCI Ex ress Technolo p gy** 

## **8b/10b Decoder** 

## **General** 

The first two generations of PCIe use 8b/10b, while Gen3 does not. Let’s explore the operation of it first and then consider the difference for Gen3. Refer to Fig‐ ure 11‐24 on page 401. Each receiver Lane incorporates a 10b/8b decoder which is fed from the Elastic Buffer. The decoder is shown with two lookup tables (the D and K tables) to decode the 10‐bit Symbol stream into 8‐bit characters plus the D/K# signal. The state of the D/K# signal indicates that the received Symbol is a Data (D) character if a match for the received Symbol is found in the D table, or a Control (K) character if a match for the received Symbol is discovered in the K table. 

## **Disparity Calculator** 

The decoder sets the disparity value based on the disparity of the first Symbol received. After the first Symbol, once Symbol lock has been achieved and dis‐ parity has been initialized, the calculated disparity for each subsequent Sym‐ bol’s disparity is expected to follow the rules. If it does not, a Receiver Error is reported. 

## **Code Violation and Disparity Error Detection** 

**General.** The error detection logic of the 8b/10b decoder detects illegal Symbols in the received Symbol stream. Some error checking is optional in the receiver, but the spec requires that these errors be checked and reported as a Receiver Error. The two types of errors detected are: 

## **Code Violations.** 

- Any 6‐bit sub‐block containing more than four 1s or four 0s is in error. 

- Any 4‐bit sub‐block containing more than three 1s or three 0s is in error. 

- Any 10‐bit Symbol containing more than six 1s or six 0s is in error. 

- Any 10‐bit Symbol containing more than five consecutive 1s or five con‐ secutive 0s is in error. 

- Any 10‐bit Symbol that doesn’t decode into an 8‐bit character is in error. 

## **Disparity Errors.** 

At the receiver a Symbol cannot have a disparity that doesn’t match what it should be for the CRD. If it does, a disparity error is detected. Some dispar‐ ity errors may not be detectable until the subsequent Symbol is processed 

**400** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

(see Figure 11‐25 on page 401). For example, if two bits in a Symbol flip in error, the error may not be visible and the Symbol may decode into a valid 8‐bit character. Such an error won’t be detected in the Physical Layer. 

_Figure 11‐24: 8b/10b Decoder per Lane_ 

**==> picture [373 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bytes to De-Scrambler D/K#<br>D/<br>7 6 5 4 3 2 1 0<br>K#<br>8b Character H G F E D C B A<br>To Error Reporting<br>8b/10b Look-Up Table For D Characters<br>8b/10b Look-Up Table For K Characters Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>10b Symbol<br>From Elastic Buffer<br>**----- End of picture text -----**<br>


_Figure 11‐25: Example of Delayed Disparity Error Detection_ 

||**CRD**|**Character**|**Character**|**CRD**|**Character**|**CRD**|**Character**|**CRD**|
|---|---|---|---|---|---|---|---|---|
|**Transmitted**<br>**Character Stream**|**-**|**D21.1**||**-**|**D10.2**|**-**|**D23.5**|**+**|
|**Transmitted Bit**<br>**Stream**|**-**|**101010 1001**||**-**|**010101 0101**|**-**|**111010 1010**|**+**|
|**Bit Stream After**<br>**Error**|**-**|**101010 101**<br>**1**||**+**|**010101 0101**|**+**|**111010 1010**|**+**|
|**Decoded**<br>**Character Stream**|**-**|**D21.0**||**+**|**D10.2**|**+**|**Invalid**|**+**|
|Error occurs here<br>Error detected here|||||||||



**401** 

**PCI Ex ress Technolo p gy** 

## **Descrambler** 

The descrambler is fed by the 8b/10b decoder. It only descrambles Data (D) characters associated with a TLP or DLLP (D/K# is high). It doesn’t descramble Control (K) characters or ordered sets because they’re not scrambled at the transmitter. 

## **Some Descrambler Implementation Rules:** 

- On a multi‐Lane Link, descramblers associated with each Lane must oper‐ ate in concert, maintaining the same simultaneous value in each LFSR. 

- Descrambling is applied to ‘D’ characters associated with TLP and DLLPs including the Logical Idle (00h) sequence. ‘D’ characters within ordered set are not descrambled. 

- ‘K’ characters and ordered set characters bypass the descrambler logic. 

- Compliance Pattern characters are not descrambled. 

- When a COM character enters the descrambler, it reinitializes the LFSR value to FFFFh. 

- With one exception, the LFSR serially advances eight times for every char‐ acter (D or K character) received. The LFSR does NOT advance on SKP characters associated with the SKIP ordered sets received. The reason the LFSR is not advanced on detecting SKPs is because there may be a differ‐ ence between the number of SKP characters transmitted and the SKP char‐ acters exiting the Elastic Buffer (as discussed in “Receiver Clock Compensation Logic” on page 396). 

## **Disabling Descrambling** 

By default, descrambling is always enabled, but the spec allows it to be disabled for test and debug purposes although no standard software method is given for disabling it. If the descrambler receives at least two TS1/TS2 ordered sets with the “disable scrambling” bit set on all of its configured Lanes, it disables the descrambler. 

## **Byte Un-Striping** 

Figure 11‐26 on page 403 shows eight character streams from the descramblers of a x8 Link being un‐striped into a single byte stream which is fed to the char‐ acter filter logic. 

**402** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐26: Example of x8 Byte Un‐Striping_ 

**==> picture [354 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Multiplexer block<br>Data Stream D/K#<br>Character 0<br>Character 1<br>Character 2<br>Character 3<br>Character 4<br>Character 5<br>Character 6<br>Character 7<br>Byte Un-Striping<br>Character 0 Character 1 Character 7<br>Character 8 Character 9 Character 15<br>Character 16 Character 17 Character 23<br>From Lane 0 From Lane 1 From Lane 7<br>De-Scrambler De-Scrambler De-Scrambler<br>**----- End of picture text -----**<br>


## **Filter and Packet Alignment Check** 

The serial byte stream supplied by the byte un‐striping logic contains TLPs, DLLPs, Logical Idle sequences, Control characters such as STP, SDP, END, EDB, and PADs, as well as the ordered sets. Of these, the Logical Idle sequence, the control characters and ordered sets are detected and eliminated before they get to the next layer. What remains are the TLPs and DLLPs and these are sent to the Rx Buffer along with an indicator of the start and end of each packet. 

## **Receive Buffer (Rx Buffer)** 

The Rx Buffer holds received TLPs and DLLPs after the start and end characters have been eliminated. The received packets are ready to send to the Data Link Layer. The interface to the Data Link Layer is not described in the spec, so the designer is free to decide details like data bus width. As an example, we can 

**403** 

**PCI Ex ress Technolo p gy** 

assume an interface clock of 250MHz and a Gen1 speed on the Link. For that case, the number of bytes in the data bus between these layers would be the same as the number of Lanes supported. 

## **Physical Layer Error Handling** 

## **General** 

Physical Layer errors are reported as Receiver Errors to the Data Link Layer. According to the spec, some errors must be checked and trigger a receiver error, while others are optional. 

Required error checking: 

- 8b/10b decode errors: disparity error, illegal Symbol 

Optional error checking: 

- Loss of Symbol lock (see “Achieving Symbol Lock” on page 396) 

- Elastic Buffer overflow or underflow 

- Lane deskew errors (see “Lane‐to‐Lane Skew” on page 398) 

- Packets inconsistent with format rules 

## **Response of Data Link Layer to Receiver Error** 

If the Physical Layer indicates a Receiver Error to the Data Link Layer, the Data Link Layer discards the TLP currently being received and frees any storage allo‐ cated for the TLP. It then schedules a NAK to go back to the transmitter of the TLP. That causes the transmitter to replay TLPs from the Replay Buffer, which should automatically correct the error. The Data Link Layer may also direct the Physical Layer to initiate Link re‐training. 

If the PCI Express Extended Advanced Error Capabilities register set is imple‐ mented, a Receiver Error sets the Receiver Error Status bit in the Correctable Error Status register. If enabled, the device can send an ERR_COR (correctable error) message to the Root Complex. 

**404** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Active State Power Management**

</td>
<td style="background-color:#e8e8e8">

- 印刷电路板阻抗变化

- 走线长度不匹配

当携带数据包的串行位流到达接收器时，必须移除此通道间偏斜以按正确顺序接收字节。此过程被称为链路的去偏斜 (de-skewing)。

## **有序集合有助于去偏斜 (Ordered sets Help De-Skewing)**

有序集合的独特结构以及它们在所有通道上同时发送的事实使它们可用于检测通道之间的时序失准。规范没有定义执行此操作的方法，但在 Gen1 和 Gen2 中，接收器逻辑可以简单地查找每个通道上的 COM 字符。如果它没有同时出现在所有通道上，则延迟早到达的 COM 直到它们在所有通道上匹配。

## **接收器通道间去偏斜能力 (Receiver Lane-to-Lane De-Skew Capability)**

这可以通过调整传入信号上的模拟延迟线来完成。或者，可以在弹性缓冲区之后完成，其优点是到达时间差异现在已通过接收器的本地时钟数字化为字符时间（参见第 399 页的图 11-23）。如果一个通道的输入在一个时钟边沿上到达而另一个没有，则早到达的 COM 可以简单地延迟适当数量的字符时钟，以使其与晚到达的 COM 对齐。接收器处最大允许偏斜是时钟周期的倍数这一事实表明规范编写者可能已经在考虑这样的实现（参见第 399 页的表 11-3）。

**398**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_表 11-3：允许的接收器信号偏斜_

|规范版本|允许的 Rx 偏斜|
|---|---|
|Gen1|20 ns<br>（4ns 每字符的 5 个时钟）|
|Gen2|8 ns<br>（2ns 每字符的 4 个时钟）|
|Gen3|6 ns<br>（1.25ns 每字符的 4 个时钟）|

在 Gen3 模式下没有任何 COM 字符可用于去偏斜，但检测有序集合仍然可以提供必要的时序对齐。

## **去偏斜机会 (De-Skew Opportunities)**

需要所有通道上同时出现的明确模式来执行去偏斜，任何有序集合都可以。链路训练会发送这些，但 SKIP 有序集合在正常链路操作期间定期发送。检查其到达时间允许持续检查偏斜，以防它可能根据温度或电压发生变化。如果确实如此，链路将需要转换到 Recovery LTSSM 状态来纠正它。如果这发生在数据包传输过程中，则可能发生接收器错误并可能导致数据包丢失，可能导致 TLP 被重传。

_图 11-23：接收器链路去偏斜逻辑_

**==> 图片 [307 x 164] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
TS1/TS2 TS1/TS2<br>
通道 0 Rx FTS 延迟 FTS<br>
（字符）<br>
TS1/TS2 TS1/TS2<br>
通道 1 Rx FTS 延迟 FTS<br>
（字符）<br>
TS1/TS2 TS1/TS2<br>
通道 2 Rx FTS 延迟 FTS<br>
（字符）<br>
TS1/TS2 TS1/TS2<br>
通道 3 Rx FTS 延迟 FTS<br>
（字符）<br>
COM COM<br>
COM COM<br>
COM COM<br>
COM COM<br>
**----- 图片文字结束 -----**<br>


**399**

**PCI Ex ress Technolo p gy**

## **8b/10b 解码器 (8b/10b Decoder)**

## **概述**

PCIe 的前两代使用 8b/10b，而 Gen3 不使用。让我们首先探讨其操作，然后考虑 Gen3 的差异。参见第 401 页的图 11-24。每个接收器通道都包含一个 10b/8b 解码器，由弹性缓冲区馈送。解码器显示有两个查找表（D 表和 K 表），用于将 10 位字符流解码为 8 位字符加上 D/K# 信号。D/K# 信号的状态指示接收到的字符是数据 (D) 字符如果在 D 表中找到了接收字符的匹配，或者是控制 (K) 字符如果在 K 表中发现了接收字符的匹配。

## **不一致性计算器 (Disparity Calculator)**

解码器根据接收到的第一个字符的不一致性设置不一致性值。在第一个字符之后，一旦实现字符锁定并初始化不一致性，则期望每个后续字符计算的不一致性遵循规则。如果不是这样，则报告接收器错误。

## **代码违规和不一致性错误检测 (Code Violation and Disparity Error Detection)**

**概述。** 8b/10b 解码器的错误检测逻辑检测接收字符流中的非法字符。接收器中某些错误检查是可选的，但规范要求检查这些错误并将其报告为接收器错误。检测到的两种错误类型是：

## **代码违规 (Code Violations)。**

- 任何包含超过四个 1 或四个 0 的 6 位子块是错误的。

- 任何包含超过三个 1 或三个 0 的 4 位子块是错误的。

- 任何包含超过六个 1 或六个 0 的 10 位字符是错误的。

- 任何包含超过五个连续 1 或五个连续 0 的 10 位字符是错误的。

- 任何不能解码为 8 位字符的 10 位字符是错误的。

## **不一致性错误 (Disparity Errors)。**

在接收器处，字符不能具有与 CRD 应有不一致的不一致性。如果有，则检测到不一致性错误。某些不一致性错误可能直到处理后续字符时才可检测

**400**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

（参见第 401 页的图 11-25）。例如，如果字符中的两个位因错误翻转，则该错误可能不可见，并且该字符可能解码为有效的 8 位字符。这样的错误不会在物理层中被检测到。

_图 11-24：每通道 8b/10b 解码器_

**==> 图片 [373 x 232] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
到解扰器的字节 D/K#<br>
D/<br>
7 6 5 4 3 2 1 0<br>
K#<br>
8b 字符 H G F E D C B A<br>
到错误报告<br>
D 字符的 8b/10b 查找表<br>
K 字符的 8b/10b 查找表 当前<br>
运行<br>
不一致性<br>
(CRD)<br>
CRD 计算器 j h g f i e d c b a<br>
来自弹性缓冲区的 10b 字符<br>
**----- 图片文字结束 -----**<br>


_图 11-25：延迟不一致性错误检测示例_

||**CRD**|**字符**|**字符**|**CRD**|**字符**|**CRD**|**字符**|**CRD**|
|---|---|---|---|---|---|---|---|---|
|**已传输**<br>**字符流**|**-**|**D21.1**||**-**|**D10.2**|**-**|**D23.5**|**+**|
|**已传输位**<br>**流**|**-**|**101010 1001**||**-**|**010101 0101**|**-**|**111010 1010**|**+**|
|**错误之后**<br>**的位流**|**-**|**101010 101**<br>**1**||**+**|**010101 0101**|**+**|**111010 1010**|**+**|
|**解码后**<br>**的字符流**|**-**|**D21.0**||**+**|**D10.2**|**+**|**无效**|**+**|
|错误发生在此处<br>错误检测到在此处|||||||||


**401**

**PCI Ex ress Technolo p gy**

## **解扰器 (Descrambler)**

解扰器由 8b/10b 解码器馈送。它仅解扰与 TLP 或 DLLP 相关联的数据 (D) 字符（D/K# 为高）。它不解扰控制 (K) 字符或有序集合，因为它们在发送器处未被加扰。

## **一些解扰器实现规则 (Some Descrambler Implementation Rules)：**

- 在多通道链路上，与每个通道相关联的解扰器必须协同工作，在每个 LFSR 中保持相同的同步值。

- 解扰应用于与 TLP 和 DLLP 相关联的"D"字符，包括逻辑空闲 (00h) 序列。有序集合内的"D"字符不被解扰。

- "K"字符和有序集合字符绕过解扰器逻辑。

- 合规模式字符不被解扰。

- 当 COM 字符进入解扰器时，它将 LFSR 值重新初始化为 FFFFh。

- 除一个例外外，LFSR 每接收一个字符（D 或 K 字符）就串行推进八次。LFSR 不会在接收到的 SKIP 有序集合相关联的 SKP 字符上推进。LFSR 在检测到 SKP 时不推进的原因是，传输的 SKP 字符数与退出弹性缓冲区的 SKP 字符数可能存在差异（如第 396 页的"接收器时钟补偿逻辑 (Receiver Clock Compensation Logic)"中所讨论的）。

## **禁用解扰 (Disabling Descrambling)**

默认情况下，解扰始终是启用的，但规范允许出于测试和调试目的禁用它，尽管没有给出标准的软件方法来禁用它。如果解扰器在其所有已配置通道上接收到至少两个设置了"禁用加扰 (disable scrambling)"位的 TS1/TS2 有序集合，则它禁用解扰器。

## **字节解交错 (Byte Un-Striping)**

第 403 页的图 11-26 显示了 x8 链路的解扰器的八个字符流被解交错为单个字节流，该字节流被馈送到字符过滤逻辑。

**402**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-26：x8 字节解交错示例_

**==> 图片 [354 x 225] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
来自多路复用器块的数据包字节流<br>
数据流 D/K#<br>
字符 0<br>
字符 1<br>
字符 2<br>
字符 3<br>
字符 4<br>
字符 5<br>
字符 6<br>
字符 7<br>
字节解交错<br>
字符 0 字符 1 字符 7<br>
字符 8 字符 9 字符 15<br>
字符 16 字符 17 字符 23<br>
来自通道 0 来自通道 1 来自通道 7<br>
解扰器 解扰器 解扰器<br>
**----- 图片文字结束 -----**<br>


## **过滤和包对齐检查 (Filter and Packet Alignment Check)**

由字节解交错逻辑提供的串行字节流包含 TLP、DLLP、逻辑空闲序列、控制字符（如 STP、SDP、END、EDB 和 PAD）以及有序集合。其中，逻辑空闲序列、控制字符和有序集合在被传递到下一层之前被检测并消除。剩下的是 TLP 和 DLLP，它们与每个数据包的开始和结束指示符一起被发送到 Rx 缓冲区。

## **接收缓冲区 (Rx Buffer)**

Rx 缓冲区在开始和结束字符被消除后保存接收到的 TLP 和 DLLP。接收到的数据包已准备好发送到数据链路层。与数据链路层的接口未在规范中描述，因此设计人员可以自由决定细节，如数据总线宽度。例如，我们可以

**403**

**PCI Ex ress Technolo p gy**

假设接口时钟为 250MHz，链路上的 Gen1 速度。对于这种情况，这些层之间的数据总线中的字节数将与支持的通道数相同。

## **物理层错误处理 (Physical Layer Error Handling)**

## **概述**

物理层错误作为接收器错误报告给数据链路层。根据规范，某些错误必须检查并触发接收器错误，而其他错误是可选的。

必需的检查：

- 8b/10b 解码错误：不一致性错误、非法字符

可选的错误检查：

- 失去字符锁定（参见第 396 页的"实现字符锁定 (Achieving Symbol Lock)"）

- 弹性缓冲区溢出或下溢

- 通道去偏斜错误（参见第 398 页的"通道间偏斜 (Lane-to-Lane Skew)"）

- 数据包与格式规则不一致

## **数据链路层对接收器错误的响应 (Response of Data Link Layer to Receiver Error)**

如果物理层向数据链路层指示接收器错误，则数据链路层丢弃当前正在接收的 TLP 并释放为该 TLP 分配的任何存储。然后它调度一个 NAK 返回给 TLP 的发送器。这导致发送器从 Replay Buffer 重放 TLP，这应该自动纠正错误。数据链路层也可以指示物理层发起链路重新训练。

如果实现了 PCI Express Extended Advanced Error Capabilities 寄存器组，则接收器错误会在 Correctable Error Status 寄存器中设置 Receiver Error Status 位。如果启用，设备可以向根复合体 (Root Complex) 发送 ERR_COR（可纠正错误）消息。

**404**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **活动状态电源管理 (Active State Power Management)**

有几种链路电源状态允许在某些条件下节省功耗。这些是 L0s、L1、L2 和 L3，它们表示功耗越来越低，并且恢复链路回到完全运行状态 L0 的恢复时间也越来越长。L0s 状态只能由硬件控制进入，而 L1 可以由硬件或软件启动。由于 L0s 和 L1 可以由硬件控制，因此规范将其称为 ASPM（活动状态电源管理，Active State Power Management）状态。有关链路和设备电源管理的详细信息，请参见第 735 页的"活动状态电源管理 (ASPM)"部分。

## **链路训练和初始化 (Link Training and Initialization)**

正如我们刚刚在本章中简要提到的，物理层还负责在复位后初始化链路。但是，这个主题太大，无法在此处涵盖，而是在第 14 章"链路初始化和训练 (Link Initialization & Training)"的第 505 页中介绍。

**405**

**PCI Ex ress Technolo p gy**

**406**

## _**12**_

## _**物理层 - 逻辑 (Gen3)**_

## **上一章**

上一章描述了 Gen1/Gen2 物理层的逻辑子块。该层准备数据包以进行串行传输和恢复，并详细描述了完成此操作所需的几个步骤。本章涵盖了使用 8b/10b 编码/解码的 Gen1 和 Gen2 协议相关联的逻辑。

## **本章**

本章描述了 PCIe 第三代（Gen3）逻辑物理层的特性。主要变化包括能够在不使频率翻倍的情况下将带宽相对于 Gen2 速度翻倍（链路速度从 5 GT/s 到 8 GT/s）。这是通过在 Gen3 模式下消除 8b/10b 编码来实现的。在 Gen3 速度下需要更稳健的信号补偿。

## **下一章**

下一章描述物理层到链路的电气接口。对信号均衡 (signal equalization) 的需求以及用于实现它的方法也将在此处讨论。本章结合了 Gen1、Gen2 和 Gen3 速度的电气发送器和接收器特性。

## **Gen3 介绍**

回想一下，当 PCIe 链路进入训练时（即，在复位之后），它始终从 Gen1 速度开始以实现向后兼容。如果在训练期间通告了更高的速度，则链路将立即转换到 Recovery 状态并尝试更改为最高共同支持的速度。

**407**

## **PCI Ex ress Technolo p gy**

将 PCIe 规范升级到 Gen3 的主要动机是将带宽翻倍，如第 408 页的表 12-1 所示。完成此操作的简单方法是将信号频率从 5 GT/s 翻倍到 10 Gb/s，但这样做带来了几个问题：

- 更高的频率消耗大量电力，由于需要复杂的调节逻辑（均衡）以在更高速度下保持信号完整性，这种情况更加严重。事实上，PCISIG 文献中提到均衡逻辑的功耗是使频率尽可能低的一个主要动机。

- 一些电路板材料在更高频率下会出现显著的信号衰减。这个问题可以通过使用更好的材料和更多的设计工作来解决，但这些会增加成本和开发时间。由于 PCIe 旨在服务于各种各样的系统，目标是它也应该在廉价的设计中良好工作。

- 同样，允许新设计使用现有基础设施（例如电路板和连接器）可以最大限度地减少电路板设计工作和成本。使用更高的频率使这变得更加困难，因为必须调整走线长度和其他参数以适应新的时序，这使得高频率不太理想。

_表 12-1：各种链路宽度的 PCI Express 总带宽_

|**链路宽度**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 带宽**<br>**(GB/s)**|0.5|1|2|4|6|8|16|
|**Gen2 带宽**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 带宽**<br>**(GB/s)**|2|4|8|16|24|32|64|

这些考虑导致了 Gen3 规范与前几代相比的两个重大变化：新的编码模型和更复杂的信号均衡模型。

**408**

**第 12 章：物理层 - 逻辑 (Gen3)**

## **新的编码模型 (New Encoding Model)**

物理层的逻辑部分用新的 128b/130b 编码方案替换了 8b/10b 编码。当然，这意味着要脱离许多串行设计中使用的广为人知的 8b/10b 模型。设计人员愿意采取这一步来恢复 8b/10b 编码所带来的 20% 传输开销。使用 128b/130b 意味着通道现在每个字节传输 8 位而不是 10 位，这意味着 8.0 GT/s 数据速率使带宽翻倍。这相当于每个方向 1 GB/s 的带宽。

为了说明这两种编码之间的差异，首先考虑图 12-1，它显示了一般 8b/10b 数据包构造。箭头突出显示了表示 8b/10b 数据包成帧字符的控制 (K) 字符。接收器通过识别这些控制字符来知道期望什么。有关此编码方案的好处的详细信息，请参阅第 380 页的"8b/10b 编码 (8b/10b Encoding)"。

_图 12-1：8b/10b 通道编码_

**==> 图片 [344 x 130] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
'D' 字符<br>
STP 序列 头部 数据有效负载  ECRC LCRC END<br>
'D' 字符<br>
'K' 字符 'K' 字符<br>
SDP DLLP 类型 杂项 CRC END<br>
'K' 字符 'K' 字符<br>
**----- 图片文字结束 -----**<br>


相比之下，第 410 页的图 12-2 显示了 128b/130b 编码。此编码不影响正在传输的字节，相反，字符被分组成 16 字节块，每个块的开头有 2 位 Sync 字段。2 位 Sync 字段指定块是包含数据 (10b) 还是有序集合 (01b)。因此，Sync 字段向接收器指示期望哪种类型的流量以及何时开始。有序集合类似于 8b/10b 版本，它们必须同时在所有通道上驱动。这需要正确同步通道，这是训练过程的一部分（参见第 438 页的"实现块对齐 (Achieving Block Alignment)"）。

**409**

**PCI Ex ress Technolo p gy**

_图 12-2：128b/130b 块编码_

**==> 图片 [354 x 50] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
0    1 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7<br>
Sync 字段 字符 0 字符 1 字符 15<br>
**----- 图片文字结束 -----**<br>


## **复杂的信号均衡 (Sophisticated Signal Equalization)**

第二个变化是在物理层的电气子块中进行的，涉及链路发送侧以及可选的接收器侧的更复杂的信号均衡。Gen1 和 Gen2 实现使用固定的 Tx 去加重 (de-emphasis) 来实现良好的信号质量。然而，将传输频率提高到 5 GT/s 以上会导致信号完整性问题变得更加明显，需要更多的发送器和接收器补偿。这可以在电路板级别进行一些管理，但设计人员希望允许外部基础设施尽可能保持不变，而是将负担放在 PHY 发送器和接收器电路上。有关信号调节的更多详细信息，请参阅第 474 页的"8.0 GT/s 解决方案 - 发送器均衡 (Solution for 8.0 GT/s - Transmitter Equalization)"。

## **8.0 GT/s 的编码 (Encoding for 8.0 GT/s)**

如前所述，Gen3 128b/130b 编码方法使用链路范围的数据包和每通道块编码。本节提供有关编码的其他详细信息。

## **通道级编码 (Lane-Level Encoding)**

为了说明块的使用，请考虑第 411 页的图 12-3，其中显示了一个单通道数据块。开头是 2 个 Sync Header 位，后跟 16 字节（128 位）信息，总共导致 130 个传输位。Sync Header 简单地定义正在发送的是数据块 (10b) 还是有序集合 (01b)。您可能已经注意到图 12-3 中的数据块的 Sync Header 值为 01 而不是上面提到的 10b 值。这是因为当跨链路传输块时，Sync Header 的最低有效位首先被发送。请注意，Sync Header 后面的字符也是最低有效位先发送。

**410**

**第 12 章：物理层 - 逻辑 (Gen3)**

_图 12-3：Sync Header 数据块示例_

**==> 图片 [374 x 122] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync 字符 0 字符 1 字符 15<br>
(01)<br>
128 位有效负载<br>
数据块<br>
UI UI UI<br>
0 2 10 122<br>
= = = =<br>
时间 时间 时间 时间<br>
**----- 图片文字结束 -----**<br>


## **块对齐 (Block Alignment)**

与以前的实现一样，Gen3 首先实现位锁定，然后尝试建立块对齐锁定。这要求接收器找到标识块边界的 Sync Header。发送器通过发送可识别的 EIEOS 模式来建立此边界，该模式由交替的 00h 和 FFh 字节组成，如图 12-4 所示。因此，EIEOS 的使用范围从简单地退出电气空闲扩展到还作为建立块对齐的同步机制。请注意，紧接在 EIEOS 之前和之后的 Sync Header 位（图中未显示）。有关此过程的详细信息，请参见第 438 页的"实现块对齐 (Achieving Block Alignment)"。

_图 12-4：Gen3 模式 EIEOS 字符模式_

**==> 图片 [89 x 147] 已故意省略 <==**

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


**411**

**PCI Ex ress Technolo p gy**

## **有序集合块 (Ordered Set Blocks)**

有序集合在 Gen1 和 Gen2 中的含义基本相同。它们用于管理通道协议。当发送有序集合块时，它必须同时出现在所有通道上，几乎总是由 16 个字节组成，但有一个例外。此大小规则的一个例外是 SOS（SKP 有序集合），它可以通过时钟补偿逻辑（例如与链路中继器相关联的）以 4 个字符为单位添加或移除 SKP 字符，因此合法地可以是 8、12、16、20 或 24 字节长。

有序集合块的基本格式类似于数据块，只是 Sync Header 位是相反的，如图 12-5（第 412 页）所示。

_图 12-5：Gen3 x1 有序集合块示例_

**==> 图片 [347 x 121] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
1 0 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>
Sync 字符 0 字符 1 字符 15<br>
(10)<br>
128 位有效负载<br>
有序集合块<br>
UI UI UI<br>
0 2 10 122<br>
= = = =<br>
时间 时间 时间 时间<br>
**----- 图片文字结束 -----**<br>


规范为 Gen3 定义了七个有序集合（比 Gen1 和 Gen2 PCIe 多一个有序集合）。在大多数情况下，它们的功能与前几代相同。

1. SOS - Skip 有序集合：用于时钟补偿。有关更多详细信息，请参见第 426 页的"有序集合示例 - SOS (Ordered Set Example - SOS)"。

2. EIOS - 电气空闲有序集合：用于进入电气空闲状态

3. EIEOS - 电气空闲退出有序集合：现在用于两个目的：
   - 像以前一样退出电气空闲
   - 8.0 GT/s 的块对齐指示符

4. TS1 - 训练序列 1 有序集合

5. TS2 - 训练序列 2 有序集合

6. FTS - 快速训练序列有序集合

7. SDS - 数据流开始有序集合：新增 - 有关更多信息，请参见第 413 页的"数据流和数据块 (Data Stream and Data Blocks)"

**412**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
