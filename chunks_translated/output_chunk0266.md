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