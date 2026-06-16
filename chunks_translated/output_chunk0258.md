为了实现此目标，一种称为 LCRC (Link Cyclic Redundancy Code) 的错误检测码被添加到每个 TLP 中。错误检查的第一步是简单地验证此代码在接收方是否仍然正确求值。如果每个报文还被赋予一个唯一的增量序列号，那么将很容易分清在已发送的几个报文中哪个报文遇到了错误。使用该序列号，我们还可以要求 TLP 必须以其发送的相同顺序成功接收。这个简单的规则使在接收方数据链路层检测缺失的 TLP 变得容易。

与 Ack/Nak 协议相关的数据链路层中的基本块在图 10-2（第 319 页）中更详细地示出。通过链路发送的每个 TLP 在接收方通过评估报文中的 LCRC（首先）和序列号（其次）进行检查。接收设备通过返回 Ack 通知发送设备已收到良好的 TLP。在发送方收到

**318**

**第 10 章：Ack/Nak 协议**

Ack 表示接收方已成功接收至少一个 TLP。另一方面，发送方接收到 Nak 表明接收方已至少收到一个错误的 TLP。在这种情况下，发送方将重新发送适当的 TLP，希望这次有更好的结果。这是合理的，因为导致传输错误的因素很可能是瞬时事件，重放 (replay) 将有很好的机会解决问题。

_图 10-2：Ack/Nak 协议概述_

**==> 图片 [374 x 237] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transmit Receiver<br>Device A Device B<br>From To<br>Transaction Layer Transaction Layer<br>Tx Rx<br>Data Link Layer Data Link Layer<br>TLP DLLP DLLP TLP<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux De-mux<br>Error<br>Mux Mux Check<br>Tx Rx Tx Rx<br>DLLP<br>ACK /<br>NAK<br>Link<br>TLP<br>Sequence TLP LCRC<br>**----- 图片文字结束 -----**<br>


由于协议中的发送和接收设备都同时具有发送和接收侧，因此本章将使用以下术语：

- **发送方 (Transmitter)** 指发送 TLP 的设备

- **接收方 (Receiver)** 指接收 TLP 的设备

**319**

**PCI Exress Technology**

## **Ack/Nak 协议的要素**

数据链路层的主要 Ack/Nak 协议元素如图 10-3（第 320 页）所示。要一次考虑的事情太多了，所以让我们从关注发送方元素开始，它们在图 10-4（第 322 页）中的较大视图中显示。

_图 10-3：Ack/Nak 协议的要素_

**==> 图片 [375 x 242] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (TX) Block TLPs; Report Transaction Layer (RX)<br>DLL protocol error<br>Yes Increment NRS Good TLPs<br>No<br>TLPs (NTS-AS) ≥ 2048?<br>(Continue) NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Assign<br>SequenceNumber (IncrementNEXT_TRANSMIT_SEQ (NTS)) Seq Num < NRS (Duplicate TLP)(Schedule Ack) Seq Num>, <, =NRS?<br>REPLAY_TIMER<br>LCRC Increment on Replay) Seq Num > NRS (Lost TLP)<br>REPLAY_NUM<br>Generator (Send Nak) Yes<br>Purge Older TLPs (Reset Both)<br>(Send Nak) No Pass<br>Retry (Replay)Buffer (Replay)Yes Nak?Nak (Update)AckD_SEQ (AS)No Nak Flag Clear?Set & Send Nak LCRC?<br>Yes AckNak<br>(TLP copy) SeqNum = AS? NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>(TLP copy) Yes Ack Nak<br>(Discard) No CRC?Pass  GeneratorAck/Nak AckNak LatencyTimer<br>Ack/Nak<br>DLLP Link<br>TLP TLP<br>Block TLP during Replay<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- 图片文字结束 -----**<br>


## **发送方元素**

当 TLP 从事务层到达时，会执行几项操作以准备它们在接收方进行可靠的错误检测。如图所示，首先为 TLP 分配从 12 位 NEXT_TRANSMIT_SEQ 计数器获得的下一个序列号。

**320**

**第 10 章：Ack/Nak 协议**

## **NEXT_TRANSMIT_SEQ 计数器**

此计数器生成将分配给下一个传入 TLP 的序列号。它是一个 12 位的计数器，在复位时或当链路层报告 DL_Down（链路层处于非活动状态）时初始化为 0。由于它随每个 TLP 连续递增并且只向前计数，因此计数器最终会达到其最大值 4095，并在继续计数时回绕到 0。

分配给 TLP 的此序列号将在接收方发送的 Ack 或 Nak 中用于引用重放缓冲区 (Replay Buffer) 中的此 TLP。有人可能认为如此大的计数器意味着可能有大量的未确认 TLP 在传输中，但实际上这是极不可能的。主要原因是接收方有要求在特定时间内为成功接收的 TLP 发送回一个 Ack。该时间在第 328 页的"AckNak_LATENCY_TIMER"中详细讨论，但通常只够传输几个最大大小的报文。

## **LCRC 生成器**

此块基于要发送的头部和数据生成 32 位 CRC (Cyclic Redundancy Check) 码，并将其添加到传出报文的末尾以促进错误检测。名称来源于以下事实：此 _校验码_（从要发送的报文计算）是 _冗余_（不添加信息）的，并且源自 _循环码_。虽然 CRC 不为接收方提供足够的信息来执行 ECC (Error Correcting Code) 方法那样的自动纠错，但它确实提供了可靠的错误检测。CRC 通常用于串行传输，因为它们易于在硬件中实现，并且擅长检测突发错误：一串不正确的位。由于这在串行设计中比并行模型更可能发生，因此它有助于解释为什么 CRC 是串行传输中错误检测的良好选择。CRC 码是使用 TLP 的所有字段（包括序列号）计算的。接收方将进行相同的计算并将其结果与 TLP 中的 LCRC 字段进行比较。如果它们不匹配，则在接收方的链路层中检测到错误。

## **重放缓冲区**

重放缓冲区 (replay buffer) 或重试缓冲区 (retry buffer) 按其传输顺序存储 TLP，包括序列号和 LCRC。当发送方接收到 Ack 指示 TLP 已成功到达接收方时，它会从重放缓冲区中清除那些序列号等于或早于 Ack 中序列号的 TLP。通过这种方式，设计允许一个 Ack 代表多个成功的 TLP，从而减少了必须发送的 Ack 数量。由于报文必须始终按顺序查看，因此如果收到一个

**321**

**PCI Exress Technology**

序列号为 7 的 Ack，则不仅 TLP 7 被成功接收，而且其之前的所有报文也必须已被成功接收，因此没有理由在重放缓冲区中保留它们的副本。

如果收到 Nak，则 Nak 中的序列号仍然指示最后 _良好的_ 接收报文。因此，即使收到 Nak 也会导致发送方从重放缓冲区中清除 TLP。但是，因为它是 Nak，这意味着某些内容未在接收方成功接收，因此在清除所有已确认的 TLP 后，发送方必须按顺序重放重放缓冲区中所有剩余的内容。例如，如果收到序列号为 9 的 Nak，则报文 9 和所有先前的报文都从重放缓冲区中清除，因为接收方已确认它们已成功接收。但是，因为它是 Nak，发送方必须随后按顺序重放重放缓冲区中所有剩余的 TLP，从报文 10 开始。

_图 10-4：与 Ack/Nak 协议相关联的发送方元素_

**==> 图片 [217 x 275] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (TX) Block TLPs; Report<br>DLL protocol error<br>Yes<br>No<br>TLPs (NTS-AS) ≥ 2048?<br>(Continue)<br>Assign<br>Sequence<br>Number NEXT_TRANSMIT_SEQ (NTS)<br>(Increment)<br>REPLAY_TIMER<br>LCRC Increment on Replay)<br>REPLAY_NUM<br>Generator<br>Purge Older TLPs<br>(Reset Both)<br>Nak AckD_SEQ (AS)<br>Retry (Replay)Buffer Yes Nak? (Update) No<br>(Replay)<br>Yes AckNak<br>SeqNum = AS?<br>(TLP copy)<br>(TLP copy) Yes<br>No Pass<br>(Discard) CRC?<br>Link<br>Block TLP during Replay<br>**----- 图片文字结束 -----**<br>


**322**

**第 10 章：Ack/Nak 协议**

## **REPLAY_TIMER 计数**

此计时器实际上是一个看门狗计时器。它确保发送方正在接收已发送 TLP 的 Ack/Nak 报文。如果此计时器到期，则意味着发送方已发送一个或多个 TLP，但未在预期的时间范围内收到确认。解决方法是重新发送重放缓冲区中的所有内容并重新启动 REPLAY_TIMER。

此计时器在任何 TLP 已传输但尚未确认时都处于运行状态。如果 REPLAY_TIMER 当前未运行，则在发送任何 TLP 的最后一个符号时启动。如果计时器已经在运行，则发送其他 TLP 不会重置计时器值。当收到确认重放缓冲区中 TLP 的 Ack 或 Nak 时，计时器重置回 0，如果重放缓冲区中仍有 TLP（已传输但尚未确认的 TLP），则它会立即开始重新计数。但是，如果收到的 Ack 确认了重放缓冲区中的最后一个 TLP，意味着重放缓冲区现在为空，则 REPLAY_TIMER 重置为 0 但不计数。它将不会再次开始计数，直到下一个 TLP 的最后一个符号被传输。

## **REPLAY_NUM 计数**

此 2 位计数器跟踪在接收到 Nak 或 REPLAY_TIMER 超时之后的重放尝试次数。当 REPLAY_NUM 计数从 11b 回绕到 00b（表示对同一组 TLP 进行了 4 次失败的传递尝试）时，数据链路层自动强制物理层重新训练链路（LTSSM 进入 Recovery 状态）。重新训练完成后，它将尝试再次发送失败的 TLP。REPLAY_NUM 计数器在复位时或当链路层处于非活动状态时初始化为 00b。每当收到序列号比上次看到的更新的 Ack DLLP 时，它也会被重置，这意味着正在取得进展。

## **ACKD_SEQ 寄存器**

此 12 位寄存器存储最近接收到的 Ack 或 Nak 的序列号。它在复位时或当数据链路层处于非活动状态时初始化为全 1。此寄存器使用接收到的 Ack 或 Nak 的 AckNak_Seq_Num [11:0] 字段更新。将 ACKD_SEQ 计数与最后接收到的 Ack 或 Nak 中的序列号进行比较，以检查是否取得进展。如果最新的 Ack/Nak 的序列号晚于 ACKD_SEQ 寄存器，那么我们正在取得进展。

**323**

## **PCI Exress Technology**

顺便说一句，我们使用术语"较晚的序列号"来解释以下事实：与 PCIe 中的大多数计数器一样，序列号计数器仅向前计数，这意味着它们最终会回绕回零。从技术上讲，较晚的数字将意味着数值更高的值，但我们必须记住，当计数器达到 4095（它是 12 位计数器）时，下一个更高的数字将为零。这种回绕效果将在后面的示例中更容易看到，如第 331 页的"Ack/Nak 示例"中所示。
