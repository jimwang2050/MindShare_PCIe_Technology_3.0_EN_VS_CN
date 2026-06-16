既然我们已经描述了协议的工作方式，现在是解释其一般操作异常的好时机。PCIe 支持称为"直通模式 (cut-through mode)"的交换机特性，可用于改善大型 TLP 通过交换机的传输延迟。

**354**

**第 10 章：Ack/Nak 协议**

## **背景**

考虑一个示例，其中一个大型 TLP 需要通过交换机，如图 10-16（第 357 页）所示。由于入口交换机端口在看到整个 TLP 之前无法判断报文中是否有错误，因此它通常会存储整个报文并在转发到出口端口之前检查错误。这种存储转发方法有效，但对于大型报文，通过交换机的延迟可能很大，这可能是某些应用程序的问题。如果可能的话，最好尽量减少这种延迟。

## **延迟改进选项**

由于 TLP 的第一部分包含带有报文路由信息的头部，因此一种选择是假设报文是良好报文，并在接收到整个报文之前就开始评估头部中的路由信息。这将允许交换机在评估该路由后立即开始将 TLP 转发到出口端口。然后，出口端口可以继续开始通过其链路发送它，只要这样做不会导致交换机内的下溢情况。（如果入口端口是 x1 而出口端口是 x16，则可能很容易发生潜在的下溢情况。出口端口发送报文的速度将远快于其被接收的速度。）

当然，入口端口在接收到报文末尾的 LCRC 之前无法检查报文中的错误，因此存在一个小风险，即正在向外转发的 TLP 可能实际上包含错误。最终，TLP 的末尾到达入口端口，可以检查报文。如果发现有错误，则入口端口对错误的 TLP 采取正常行为，并简单地发送一个 Nak 以重放报文。但是，现在我们必须处理这样一个问题：现在我们知道大部分已损坏的报文已经被转发到出口端口。在这种情况下我们有什么选择？我们可以完成报文的转发并等待相邻接收方在看到错误时发送 Nak，但重放缓冲区中的报文将是错误的报文，因此那里的重放无法解决问题。我们可能截断传输中的错误报文，但规范不允许这种可能性。要使其工作，我们需要另一个选项，这就是直通选项发挥作用的地方。

**355**

**PCI Exress Technology**

## **直通操作**

直通模式提供了上一节中描述的转发问题的解决方案：如果在传入报文中看到错误，则已经在外发途中的报文必须被"**作废 (nullified)**"。

**作废**的报文以 EDB (end bad) 符号而不是 END (end good) 符号终止，并且为了使条件非常清楚，TLP 的 32 位 LCRC 从原始计算值反相（1 的补码）。本质上，作废的报文被视为从未存在过。在交换机出口端口上，这意味着重放缓冲区丢弃该报文，并且 NEXT_TRANSMIT_SEQ 计数器减一（回滚）。

当设备接收到它识别为已作废的 TLP 的 TLP 时，它只是丢弃该报文并将其视为从未存在过。NEXT_RCV_SEQ 不会递增，AckNak_LATENCY_TIMER 不会启动，也不会设置 NAK_SCHEDULED。接收设备静默丢弃已作废的 TLP 并且不会为其返回 Ack/Nak。

## **直通操作示例**

图 10-16（第 357 页）说明了从左侧进入、通过交换机并最终到达右侧端点的 TLP。在左侧链路上发生 TLP 错误。步骤如下：

1. 在交换机入口端口看到传入的 TLP。它在传输过程中已损坏，但尚未知晓。

2. TLP 头部到达，被解码，并且报文在直通操作中转发到目标出口端口。

3. 最终，报文的末尾到达，交换机入口端口能够完成 LCRC 错误检查。它发现 CRC 错误，并将 Nak 返回给 TLP 源。

4. 在出口端口，交换机将错误 TLP 末尾的 END 成帧符号替换为 EDB，并反相计算出的 LCRC 值。TLP 现在被"作废"，交换机从重放缓冲区中丢弃它。

5. 作废的报文到达端点。端点检测到 EDB 符号和反相的 LCRC，并静默丢弃该报文。它不会返回 Nak。

现在假设 TLP 源设备重放报文并且没有发生错误。和以前一样，TLP 以非常短的延迟转发到出口端口。当

**356**

**第 10 章：Ack/Nak 协议**

TLP 的其余部分到达交换机时，没有错误，因此将 Ack 返回给 TLP 源，然后该 TLP 源从其重放缓冲区中清除该 TLP。这一次交换机出口端口将 TLP 的副本保留在其重放缓冲区中。当 TLP 到达目标时，报文没有错误，端点返回 Ack。基于此，交换机从其重放缓冲区中清除 TLP 的副本，序列完成。

_图 10-16：显示错误处理的交换机直通模式_

**==> 图片 [378 x 107] 已省略 <==**

**----- 图片文字开始 -----**<br>
Error occurs<br>1) 2) 4)<br>END TLP STP END TLP STP EDB TLP STP<br>EDB TLP STP<br>Switch Endpoint<br>5) Discard Packet<br>NAK 6) No ACK or NAK<br>3)<br>**----- 图片文字结束 -----**<br>


**357**

**PCI Exress Technology**

**358**

## 第四部分：

# 物理层

## _**11 物理层 - 逻辑 (Gen1 和 Gen2)**_

## **上一章**

上一章描述了 Ack/Nak 协议：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。Ack DLLP 确认 TLP 的良好接收，而 Nak DLLP 指示传输错误。本章描述了正常操作规则以及错误恢复机制。

## **本章**

本章描述物理层的逻辑子块。它准备用于串行传输和恢复的报文。完成此操作需要几个步骤，我们将在此详细描述。本章涵盖了使用 8b/10b 编码的 Gen1 和 Gen2 协议相关联的逻辑。Gen3 的逻辑不使用 8b/10b 编码，将在名为"物理层 - 逻辑 (Gen3)"的第 407 页的章节中单独描述。

## **下一章**

下一章描述了第三代 (Gen3) PCIe 的物理层特性。主要变化包括无需将频率加倍即可将带宽相对于 Gen2 加倍的能力，这是通过消除对 8b/10b 编码的需求来实现的。在 Gen3 速度下需要更强大的信号补偿。进行这些更改比预期的要复杂得多。

**361**

**PCI Exress Technology**

## **物理层概述**

本物理层概述介绍了 Gen1、Gen2 和 Gen3 实现之间的关系。此后，重点是与 Gen1 和 Gen2 相关联的逻辑物理层实现。Gen3 的逻辑物理层实现将在下一章中描述。

物理层位于外部物理链路和数据链路层之间接口的底部。它将来自数据链路层的出站报文转换为串行比特流，并在链路的所有 Lane 上计时输出。此层还从链路的所有 Lane 恢复接收端的比特流。接收逻辑将比特反序列化为符号流，重新组装报文，并将 TLP 和 DLLP 转发到数据链路层。

_图 11-1：PCIe 端口层_

**==> 图片 [307 x 307] 已省略 <==**

**----- 图片文字开始 -----**<br>
Software layer sends and receives address and transaction information<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Transaction layer<br>Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers Buffers<br>Management<br>per VC per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC Ack/Nak CRC Ack/Nak CRC Sequence TLP LCRC<br>Data Link layer TLP Retry De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**----- 图片文字结束 -----**<br>


**362**

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
Physical Layer Physical Layer<br>Tx Rx Tx Rx<br>Logical Logical<br>Tx Rx Tx Rx<br>Electrical Electrical<br>Link<br>Tx+ Tx- Rx+ Rx- CTX Tx- Tx+ Rx- Rx+<br>CTX<br>**----- 图片文字结束 -----**<br>


**363**

**PCI Exress Technology**

## **观察**

规范描述了物理层的功能，但故意对实现细节含糊其辞。显然，规范编写者不愿提供细节或示例实现，因为他们希望为各个供应商留出空间，以通过巧妙或创造性的逻辑版本增加价值。但对于我们的讨论来说，示例是必不可少的，选择了一个示例来说明这些概念。重要的是要明确指出，本示例尚未经过测试或验证，也不应认为设计人员必须以这种方式实现物理层。

## **发送逻辑概述**

为简单起见，让我们从该层发送方的高级概述开始，如图 11-3（第 365 页）所示。从顶部开始，我们可以看到从数据链路层输入的报文字节首先进入缓冲区。此处设置缓冲区是有意义的，因为有时必须延迟来自数据链路层的报文流，以允许有序集报文和其他项目注入到字节流中。

对于 Gen1 和 Gen2 操作，这些注入项是用于标记报文边界和创建有序集的控制字符和数据字符。为了区分这两种类型的字符，添加了一个 D/K# 位（数据或"Kontrol"）。该逻辑可以根据字符源查看 D/K# 应采用什么值。

**364**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

Gen3 操作模式不使用控制字符，因此使用数据模式来构成识别传输字节是否与 TLP/DLLP 或有序集相关联的有序集。在 128 位（16 字节）数据块的开头插入一个 2 位同步头 (Sync Header)。同步头通知接收方接收到的块是数据块（TLP 或 DLLP 相关字节）还是有序集块。由于 Gen3 模式下没有控制字符，因此不需要 D/K# 位。

_图 11-3：物理层发送详细信息_

**==> 图片 [252 x 355] 已省略 <==**

**----- 图片文字开始 -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Gen3 Scrambler Lane 1, ... ,N-1 Gen3 Scrambler<br>Scrambler Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>8 10 Tx Clk 8 10<br>Mux Mux<br>Gen3 Sync<br>Serializer Bits Generator Serializer<br>Mux Mux<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- 图片文字结束 -----**<br>


接下来，来自上层的并行数据字节被发送到字节交叉 (Byte Striping) 逻辑，在此处它们被分布或交叉到该链路的所有 Lane 上。每个报文的一个字节通过一个 Lane 传输，并且所有活动 Lane 都用于发送的每个报文。链路的所有 Lane 同时传输，因此字节必须足够快地进入此逻辑以适应这种情况。例如，如果有八个 Lane，则来自上层的八个并行字节可以到达字节交叉逻辑，从而允许数据同时被时钟输出到所有 Lane。

**365**

## **PCI Exress Technology**

接下来是加扰器 (Scrambler)，它将伪随机模式与传出数据字节进行 XOR 运算以混合位。尽管这看起来可能会引入问题，但实际上并不会，因为加扰模式是可预测的，并非真正的随机，因此接收方可以使用相同的算法轻松恢复原始数据。如果加扰器失去同步，则接收方将无法理解比特流，因此，为了防止出现此问题，会定期重置加扰器（Gen1 和 Gen2）。这样，如果加扰器确实彼此失去同步，则无需很长时间即可重新初始化并重新同步。对于 Gen1 和 Gen2 模式，每当检测到 COM 字符时就会发生重新初始化。对于 Gen3 模式，每当看到 EIEOS 有序集时就会发生重新初始化。在 Gen3 模式中使用更复杂的 24 位加扰器，因此如图 11-3（第 365 页）所示存在通过 Gen3 加扰器的替代路径。

对于 Gen1 和 Gen2 模式，加扰后的 8 位字符然后由 8b/10b 编码器编码以进行传输。请记住，字符是未编码的 8 位字节，而符号是 8b/10b 逻辑的 10 位编码输出。8b/10b 编码有几个优点，但它确实会增加开销。

对于 Gen3，显示了一条绕过编码器的单独路径。换句话说，报文的加扰字节在没有 8b/10b 编码的情况下被传输。同步位生成器在每个 16 字节报文块之前添加一个 2 位同步头。添加的 2 位同步头将以下 16 字节块标识为数据块或有序集块。每 16 字节（128 位）添加 2 位同步头是 Gen3 的 128b/130b 编码方案的基础。

最后，符号被序列化为比特流，并转发到物理层的电子子块，然后传输到链路的另一端。

## **接收逻辑概述**

图 11-4（第 367 页）显示了组成接收方逻辑的关键元素。下面描述的过程是对每个 Lane 执行的。这次从底部开始，首先要提及的是接收方时钟和数据恢复 (CDR)。此过程的第一步是基于传入比特流中的跳变来恢复时钟。该恢复的时钟忠实地再现发送方用于发送数据的时钟，并用于将传入的比特锁存到反序列化缓冲区中。

CDR 过程的下一步是找到 Gen1/Gen2 符号边界，并将恢复的时钟除以 10 以将 10 位符号锁存到弹性缓冲区中。对于 Gen3，下一步是获取块锁定 (Block Lock)，然后将与块中 16 个字节中的每一个关联的 8 位符号锁存到弹性缓冲区中 — 在下一章中会有更多内容。

**366**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

控制弹性缓冲区的逻辑通过在检测到 SOS (SKP 有序集) 时根据需要添加或删除 SKP 符号来调整恢复的时钟与接收方的本地时钟之间的细微时钟变化。最后，接收方的本地时钟将每个符号移出弹性缓冲区。

_图 11-4：物理层接收逻辑详细信息_

**==> 图片 [262 x 336] 已省略 <==**

**----- 图片文字开始 -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- 图片文字结束 -----**<br>


使用 8b/10b 解码器，Gen1/Gen2 符号被解码，从而将 10 位符号转换为 8 位字符。去扰器应用在发送方使用的相同加扰方法来恢复原始数据。最后，来自每个 Lane 的字节被取消交叉以形成字节流，该字节流将被转发到数据链路层。只有 TLP 和 DLLP 被加载到接收缓冲区并发送到数据链路层。

**367**

**PCI Exress Technology**

## **发送逻辑详细信息 (仅 Gen1 和 Gen2)**

本节提供了与上一节中确定的步骤相关的更多详细信息。在本讨论期间，请参考第 369 页的图 11-5 中的框图。

## **Tx 缓冲区**

再次从图顶部开始，缓冲区接受来自数据链路层的 TLP 和 DLLP，以及指定新报文何时开始的"控制"信息。如前所述，该缓冲区允许我们不时停止字符流，以便插入控制字符和有序集。还显示了一个"节流 (throttle)"信号传回数据链路层，以便在缓冲区变满时停止字符流。

## **Mux 和控制逻辑**

多路复用器（如图 11-6（第 370 页）所示）用于将特殊控制 (K) 字符插入来自缓冲区的数据流中。只有物理层使用 K 控制字符；它们在传输期间被插入并在接收方被删除。多路复用器的四个不同输入是：

- **发送数据缓冲区**。当数据链路层提供报文时，多路复用器会通过字符流。来自缓冲区的所有字符都是 D 字符，因此在 Tx 缓冲区内容被门控时，D/K# 信号被驱动为高电平。

- **起始和结束字符**。这些控制字符被添加到每个 TLP 和 DLLP 的开始和结束（参见第 371 页的图 11-7），并允许接收方轻松检测报文的边界。有两个起始字符：STP 指示 TLP 的开始，而 SDP 指示 DLLP 的开始。来自数据链路层的指示器连同报文类型一起确定要插入的成帧字符类型。还有两个结束字符，正常传输的结束良好 (END) 字符，以及处理某些错误情况的结束错误 (EDB) 字符。起始和结束字符是 K 字符，因此在插入起始和结束字符时，D/K# 信号被驱动为低电平（有关控制字符列表，请参见第 386 页的表 11-1）。

**368**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-5：物理层发送逻辑详细信息 (仅 Gen1 和 Gen2)_

**==> 图片 [190 x 285] 已省略 <==**

**----- 图片文字开始 -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Scrambler Lane 1, ... ,N-1 Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- 图片文字结束 -----**<br>


- **有序集**。如前所述，控制字符仅由物理层使用，上层看不到。跨链路的一些通信是必要的，用于发起和维护链路操作，这是通过交换有序集来完成的。每个有序集以称为逗号 (COM) 的 K 字符开头，并根据所传递的有序集类型包含其他 K 或 D 字符。有序集始终在四字节边界上对齐，并在各种情况下进行传输，包括：

   - 错误恢复、发起事件（例如热复位）或退出低功耗状态。在这些情况下，训练序列 1 和 2 (TS1 和 TS2) 有序集通过链路进行交换。

   - 在周期性间隔，多路复用器插入 SKIP 有序集模式，以促进接收方的时钟容限补偿。有关此过程的详细描述，请参考第 391 页的"时钟补偿"。

**369**

## **PCI Exress Technology**

- 当设备希望将其发送方置于电子空闲状态时，必须通知链路另一端的远程接收方。多路复用器会插入一个**电子空闲有序集**来完成此操作。

- 当设备希望将链路电源状态从 L0s 低功耗状态更改为 L0 全功率状态时，它会将一组**快速训练序列 (Fast Training Sequence, FTS)** 有序集发送到接收方。接收方使用此有序集将其 PLL 重新同步到发送方时钟。

- **逻辑空闲序列。**当没有准备发送的报文且没有要发送的有序集时，链路在逻辑上处于空闲状态。为了使接收方 PLL 锁定到发送方的频率，重要的是发送方继续发送某些内容，因此在该情况下插入逻辑空闲字符。逻辑空闲非常简单，仅由一串数据 00h 字符组成。

_图 11-6：发送逻辑多路复用器_

**==> 图片 [380 x 260] 已省略 <==**

**----- 图片文字开始 -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle<br>N*8<br>Tx<br>Buffer Control/ Ordered<br>CharactersToken LogicalIdle Sets<br>N*8<br>N*8 8 8 8 N*8 Ordered Sets:<br>Mux Tx   TS1,  TS2,<br>Buffer<br>N*8 D/K# STP, SDP   SKIP Logical<br>END, EDB  Electrical Idle Idle<br>Lane 0 Byte Striping Lane N<br>N*8<br>8 D/K# 8 D/K#<br>D K K/D D<br>Scrambler Lane 1, ... ,N-1 Scrambler Mux<br>8 8<br>D/K# Tx Local D/K# N*8 D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane N<br>Lane 1, ... ,N-1<br>**----- 图片文字结束 -----**<br>


**370**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-7：使用起始和结束控制字符的 TLP 和 DLLP 报文成帧_

**==> 图片 [289 x 161] 已省略 <==**

**----- 图片文字开始 -----**<br>
