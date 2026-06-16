如图 10-4（第 322 页）所示，当 Ack 或 Nak 取得进展时，它会导致序列号等于或早于 DLLP 中值的 TLP 从重放缓冲区中清除。它还会重置 REPLAY_TIMER 和 REPLAY_NUM 计数。如果没有取得进展，则无法清除任何 TLP，因此我们只检查它是否是会引起重放的 Nak。

这是提及计数器潜在问题的好地方：发送的 TLP 数量在理论上可能远大于接收方已确认的数量。如前所述，这是极不可能的；此处提及只是为了完整起见。问题基本上与流控计数器的问题相同（参见第 234 页的"阶段 3 — 计数器回绕"）并具有相同的解决方案：NEXT_TRANSMIT_SEQ 和 ACKD_SEQ 计数器永远不允许被超过其总计数值一半的值分隔。如果发送了大量 TLP 而没有确认，使得 NEXT_TRANSMIT_SEQ 计数值比 ACKD_SEQ 计数晚 2048，则在通过接收更多 Ack 解决此问题之前，将不再从事务层接受更多 TLP。如果发送的序列号与已确认计数之间的差异确实超过最大计数值的一半，则将报告数据链路层协议错误。（有关错误报告的更多信息，请参见第 655 页的"数据链路层错误"。）

## **DLLP CRC 检查**

此块检查 DLLP 的 16 位 CRC 中的错误。如果检测到错误，则丢弃该 DLLP，并可能报告一个可纠正错误（如果已启用）。不会采取进一步的操作，因为没有重放或更正失败 DLLP 的机制。相反，我们只是等待下一个成功的 Ack/Nak，它将使计数器恢复最新状态并允许正常操作继续。

## **接收方元素**

传入的 TLP 首先检查 LCRC 错误，然后检查序列号。如果没有错误，则 TLP 将转发到接收方的事务层。如果有错误，则 TLP 被丢弃，并且将调度一个 Nak，除非已经有一个 Nak 未完成。

**324**

**第 10 章：Ack/Nak 协议**

图 10-5（第 325 页）说明了与入站 TLP 和出站 Ack/Nak DLLP 处理相关联的接收方数据链路层元素。

_图 10-5：与 Ack/Nak 协议相关联的接收方元素_

**==> 图片 [223 x 281] 已省略 <==**

**----- 图片文字开始 -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- 图片文字结束 -----**<br>


## **LCRC 错误检查**

此块通过验证 32 位 LCRC 来检查接收到的 TLP 中的传输错误。此块根据接收到的 TLP 位计算 LCRC 值，然后将计算出的 LCRC 与接收到的 LCRC 进行比较。如果它们匹配，则报文的所有位都按发送时完全接收。如果不匹配，则 TLP 中存在位错误，因此它被丢弃，并将发送 Nak 以重放该报文和错误报文之后发送的所有 TLP。

**325**

**PCI Exress Technology**

## **NEXT_RCV_SEQ 计数器**

12 位 NEXT_RCV_SEQ（下一个接收序列号）计数器跟踪预期的序列号，并用于验证顺序报文接收。它在复位时或当数据链路层处于非活动状态时初始化为 0，并且对于转发到事务层的每个良好 TLP 递增一次。有错误或被作废的 TLP 不会发送到事务层，因此不会增加此计数器。

## **序列号检查**

如果 LCRC 检查通过，则将 TLP 的序列号与预期计数（NRS 编号）进行检查。如图 10-5（第 325 页）所示，此检查有三种可能的结果：

1. TLP 序列号等于 NRS 计数（我们期望的编号）。在这种情况下，一切正常：TLP 被接受并转发到事务层，并且 NRS 计数递增。接收方调度一个 Ack，但不必在 AckNak_LATENCY_TIMER 到期之前发送它。在此期间，可能会收到其他良好的 TLP，从而增加 NEXT_RCV_SEQ 计数器。然后，一旦计时器到期，将发送一个 Ack，其中包含最后接收到的良好 TLP 的序列号（NRS - 1）。这允许一个 Ack 代表多个成功的 TLP 并减少开销，因为不需要为每个 TLP 都使用专用的 Ack。

2. 如果 TLP 的序列号早于 NRS 计数（小于预期），则该 TLP 之前已见过，是重复的。只要预期序列号和接收到的序列号不被超过总计数值一半（2048）的值分隔，这不算错误，但被视为重复，意味着该 TLP 之前已被接受。在这种情况下，TLP 被静默丢弃（无 Nak，无错误报告），并发送一个 Ack，其中包含它接收到的最后良好 TLP 的序列号（NRS - 1）。为什么会出现这种情况？发送方可能未收到已发送的 Ack，因此其 REPLAY_TIMER 已过期，并重新发送了其重放缓冲区中的所有内容。通过向发送方发送一个带有我们接收到的最后良好报文序列号的 Ack，我们正在通知它我们已取得的最远进展。

3. 如果 TLP 的序列号是比 NEXT_RCV_SEQ 计数更晚的序列号（大于预期），则链路层已错过一个 TLP。例如，如果我们在等待序列号 30 并且传入的 TLP 具有序列号 31，我们就知道存在问题。编号必须按顺序排列，既然不是，则一定有一个失败了

**326**

**第 10 章：Ack/Nak 协议**

并已被丢弃，例如可能在物理层发生。这种乱序 TLP 将被丢弃，无论它是否有任何其他错误，因为我们必须按顺序接受 TLP，并且如果尚未有未完成的 Nak，则将发送一个 Nak。

预期序列号 (NRS) 随着新 TLP 的成功接收而递增的概念，以及它如何影响无效序列号范围和重复序列号范围的滑动窗口，可以在图 10-6 中看到。

_图 10-6：序列号范围示例_

**==> 图片 [270 x 286] 已省略 <==**

**----- 图片文字开始 -----**<br>
0 30 2078 4095<br>Dupli- Invalid<br>Duplicate<br>cate (out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 31 2079 4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 32 2080 4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>**----- 图片文字结束 -----**<br>


## **NAK_SCHEDULED 标志**

每当接收方调度一个 Nak 时，此标志被置位，并在接收方成功接收到具有预期序列号 (NRS) 的 TLP 时被清除。规范明确规定，接收方在 NAK_SCHEDULED 标志保持置位时不得调度其他 Nak DLLP。作者认为

**327**

**PCI Exress Technology**

这是为了防止出现无限循环的可能性；在这种情况下，发送方开始重放某些报文，但接收方在重放完成之前发送另一个 Nak，并导致它重新开始发送它们。无论动机如何，一旦发送了 Nak，在问题通过成功接收具有正确序列号的重放 TLP 得到解决之前，将不会有更多 Nak 出现。

## **AckNak_LATENCY_TIMER**

此计时器在接收方成功接收尚未确认的 TLP 时一直处于运行状态。接收方需要在计时器到期时发送一个 Ack。AckNak 延迟计时器运行的时间长度由规范规定（参见第 328 页的"AckNak_LATENCY_TIMER"），并确定接收方可以合并 Ack 的时间。一旦 AckNak 延迟计时器到期，将生成并发送一个序列号为 NRS‐1 的 Ack，它指示最后接收到的良好报文。每当发送 Ack 或 Nak 时，此计时器都会重置，并且只有在接收到新的良好 TLP 时才会重新启动。

## **Ack/Nak 生成器**

Ack 或 Nak DLLP 由错误检查块调度，并包含一个 12 位的 AckNak_Seq_Num 字段，如图 10-7（第 328 页）所示。它通过从 NRS 计数中减去 1 来计算此数字，从而报告最后接收到的良好序列号。这是因为接收到的良好 TLP 会在调度 Ack 之前递增 NRS，而失败的 TLP 只会调度 Nak 而不递增 NRS。这种方法使处理失败报文更容易，因为 TLP 中的错误可能在序列号中，因此该号码不能在 Nak 中使用。相反，它使用最后良好 TLP 的号码；我们预期的减一。唯一不表示最后良好 TLP 的情况是复位后的第一个 TLP。如果使用序列号 0 的第一个 TLP 失败，则生成的 Nak 的 AckNak_Seq_Num 值将为零减一，结果为全 1。

_图 10-7：Ack 或 Nak DLLP 格式_

**==> 图片 [386 x 97] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved AckNak_Seq_Num<br>Byte 4 16 位 CRC<br>**----- 图片文字结束 -----**<br>


**328**

**第 10 章：Ack/Nak 协议**

_表 10-1：Ack 或 Nak DLLP 字段_

|**字段名**|**头部字节/位**|**DLLP 功能**|
|---|---|---|
|DLLP 类型|Byte 0, [7:0]|指示类型：<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|此值将始终为 NEXT_RCV_SEQ 计数 - 1。|
|16 位 CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|用于保护此 DLLP 内容的 16 位 CRC。|



## **Ack/Nak 协议详细信息**

本节描述了在处理 TLP 和 Ack/Nak DLLP 时发送方和接收方的详细行为。使用了一些示例来演示可能发生的各种情况。

## **发送方协议详细信息**

## **序列号**

参考图 10-4（第 322 页），当 TLP 由事务层传送到链路层时，第一步是附加一个 12 位的序列号。请记住，下一个增量序列号实际上可能更小，例如当计数器在达到最大值 4095 后回绕回零时就会发生这种情况。因此，例如，零的值实际上可以"大于"4095 的值。将序列号比较视为评估一个持续向上移动并回绕的"窗口"可能会有所帮助。为了阐明此概念，在接下来的几个示例中使用了这样的计数回绕。

## **32 位 LCRC**

发送方还根据 TLP 内容（序列号、头部、数据有效负载和 ECRC）生成并附加一个 32 位的 LCRC (Link CRC)。

**329**

**PCI Exress Technology**

## **重放（重试）缓冲区**

**概述。** 在设备传输 TLP 之前，它将 TLP 的副本存储在重放缓冲区中。（_请注意，规范使用术语重试缓冲区 (Retry Buffer)，但在本书中选择了"重放"而不是"重试"，以更清楚地区分此机制与旧的 PCI 重试机制_）。每个缓冲区条目存储一个完整的 TLP，包括其所有字段，包括序列号（12 位宽，占两个字节）、头部（最多 16 字节）、可选的数据有效负载（最多 4KB）、可选的 ECRC（4 字节）和 LCRC 字段（4 字节）。

需要注意的是，规范以这种方式描述了重放缓冲区，但它并不是必须以这种方式实现的规范要求。只要您的设备能够在需要时按规范定义重放一系列 TLP，那么如何在设备内完成这一点的设计就完全取决于设计人员。拥有如上所述行为的重放缓冲区是实现此目的的一种方法。

**重放缓冲区大小调整。** 规范编写者选择不指定重放缓冲区的大小，将其作为设备设计人员的优化。它应该足够大以存储尚未被 Ack 确认的 TLP，以便在正常操作条件下它不会变满并停止从事务层传入的新 TLP，但也要足够小以降低成本。要确定最佳缓冲区大小，设计人员将考虑：

- 来自接收方的 Ack DLLP 延迟。

- 物理链路引起的延迟。

- 接收方 L0s 退出到 L0 的延迟。换句话说，缓冲区应足够大以容纳 TLP 而不会在链路从 L0s 状态返回到 L0 时停顿。

当发送方收到 Ack 时，它会从重放缓冲区中清除序列号等于或早于 Ack 中序列号的 TLP（_通常此术语为"小于"，但计数器回绕行为有时会使该评估不正确，因此选择了"早于"一词_）。类似地，当发送方收到 Nak 时，它仍然会从重放缓冲区中清除序列号等于或早于 Nak 中到达的序列号的 TLP，但随后它还会重放（重新发送）较晚序列号的 TLP（重放缓冲区中剩余的 TLP）。

**330**

**第 10 章：Ack/Nak 协议**

## **发送方对 Ack DLLP 的响应**

接收方返回的单个 Ack 可以确认多个 TLP；不必每个发送的 TLP 都收到一个专用的 Ack。接收方可以获得多个良好的 TLP，并发送一个带有最后接收到的良好 TLP 序列号的 Ack。发送方对取得进展的 Ack（具有比上次看到的更晚的序列号）的响应是将 AckD_SEQ 寄存器加载为新 Ack 的序列号。它还会重置 REPLAY_NUM 计数器和 REPLAY_TIMER，并清除重放缓冲区中由该 Ack 确认的所有 TLP。

## **Ack/Nak 示例**

**示例 1。** 在以下讨论中请考虑图 10-8（第 332 页）。

1. 设备 A 发送序列号为 3、4、5、6、7 的 TLP。

2. 设备 B 成功接收 TLP 3 并将其 NEXT_RCV_SEQ 计数器从 3 增加到 4。由于设备 B 先前已确认所有成功接收的 TLP，因此 AckNak_LATENCY_TIMER 未运行。在接收到 TLP 3 后，设备 B 现在已成功接收到一个尚未确认的 TLP，因此启动 AckNak_LATENCY_TIMER（这相当于调度一个 Ack）。

3. 设备 B 在 AckNak_LATENCY_TIMER 到期之前成功接收 TLP 4 和 5。接收 TLP 4 和 5 不会重置 AckNak_LATENCY_TIMER。

4. 一旦 AckNak_LATENCY_TIMER 到期，设备 B 发送一个序列号为 5 的 Ack，这是最后接收到的良好 TLP。AckNak_LATENCY_TIMER 被重置，但在成功接收到 TLP 6 之前不会重新启动。

5. 设备 A 接收到 Ack 5，重置 REPLAY_TIMER 和 REPLAY_NUM 计数器，因为正在取得进展。并且它会从重放缓冲区中清除序列号早于或等于 5 的 TLP。

6. 一旦设备 B 接收到 TLP 6 和 7 并且其 AckNak_LATENCY_TIMER 再次到期，它将发送一个序列号为 7 的 Ack，根据本示例，这将清除设备 A 重放缓冲区中最后两个 TLP。

**331**

## **PCI Exress Technology**

_图 10-8：示例 1 — Ack 示例_

**==> 图片 [378 x 249] 已省略 <==**

**----- 图片文字开始 -----**<br>
3 Good TLP<br>Receive Buffer<br>4 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>5 Good TLP<br>Replay Buffer 8 NEXT_RCV_SEQ<br>6<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 7<br>6 Ack<br>Purge Lat Tmr<br>5 5<br>4<br>Earlier TLP 3 Ack/Nak<br>Generator<br>Link<br>7 6<br>**----- 图片文字结束 -----**<br>


**示例 2。** 此示例显示与示例 1 完全相同的行为，但它指出了序列号的回绕行为，如图 10-9（第 333 页）所示。

1. 设备 A 发送序列号为 4094、4095、0、1 和 2 的 TLP，其中 TLP 4094 是本例中发送的第一个 TLP，TLP 2 是本例中发送的最后一个 TLP。

2. 设备 B 按该顺序成功接收序列号为 4094、4095、0、1 的 TLP。接收 TLP 4094 会导致 AckNak_LATENCY_TIMER 启动。TLP 4095、0 和 1 在 AckNak_LATENCY_TIMER 到期之前被接收。TLP 2 仍在传输中。

3. 由于 AckNak_LATENCY_TIMER 已到期，设备 B 发送一个序列号为 1 的 Ack，以确认 TLP 1 以及所有先前的 TLP（本例中为 0、4095 和 4094）的接收。

4. 设备 A 成功接收 Ack 1，从重放缓冲区中清除 TLP 4094、4095、0 和 1，并重置 REPLAY_TIMER 和 REPLAY_NUM 计数。

**332**

**第 10 章：Ack/Nak 协议**

_图 10-9：示例 2 — 序列号回绕的 Ack_

**==> 图片 [381 x 260] 已省略 <==**

**----- 图片文字开始 -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>1 Good TLP<br>Replay Buffer 3 NEXT_RCV_SEQ<br>2<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 2 Ack<br>Purge<br>1 1<br>0 Lat Tmr<br>4095<br>Earlier TLP 4094 Ack/Nak<br>Generator<br>Link<br>2<br>**----- 图片文字结束 -----**<br>


## **发送方对 Nak 的响应**

Nak 表示发生了问题。当发送方收到 Nak 时，它首先从重放缓冲区中清除任何具有较早或相等序列号的 TLP，然后按 Nak 中的序列号紧随其后的序列号开始重放剩余的 TLP。如果 Nak 导致至少一个 TLP 从缓冲区中被清除，那么我们已经取得了进展。在这种情况下，发送方重置 REPLAY_NUM 计数器和 REPLAY_TIMER，并将 AckD_SEQ 寄存器加载为 Nak 的序列号。

## **TLP 重放**

当需要重放时，发送方阻止从事务层接受新的 TLP。然后它按它们放入缓冲区的相同顺序（如 FIFO）重放缓冲区中必要的 TLP。重放事件后，数据链路层解除阻止从事务层接受新的 TLP。

**333**

**PCI Exress Technology**

重放的 TLP 保留在缓冲区中，直到它们在稍后的某个时间最终被确认。

## **高效的 TLP 重放**

必须在重放期间处理接收到的 Ack 或 Nak DLLP。因此这里有两个主要选项：发送方可以保留它们直到重放完成，然后评估 Ack 或 Nak 并采取适当的步骤。另一个选项是在重放期间开始处理新的 Ack/Nak DLLP。如果使用此选项，新接收的 Ack 可能会在重放进行时从缓冲区中清除某些条目，从而可能减少需要重放的 TLP 数量并节省链路上的时间。这是允许的，但重要的是要记住，一旦 TLP 开始传输，就必须完成。

## **Nak 的示例**

请考虑图 10-10（第 335 页）。

1. 设备 A 发送序列号为 4094、4095、0、1 和 2 的 TLP。

2. 设备 B 无错误地接收 TLP 4094，并将 NEXT_RCV_SEQ 计数增加到 4095，然后启动 AckNak_LATENCY_TIMER。

3. 设备 B 在接收到的下一个 TLP (TLP 4095) 中检测到 CRC 错误，并设置 NAK_SCHEDULED 标志，这将导致发送序列号为 4094（NEXT_RCV_SEQ 计数 - 1）的 Nak。设备 B 不会等到 AckNak_LATENCY_TIMER 到期后再发送 Nak。它通常会在下一个报文边界上发送。事实上，由于已调度 Nak 进行传输，因此 AckNak_LATENCY_TIMER 已停止并重置。

4. 设备 B 将继续评估传入的 TLP，寻找 TLP 4095。但是，由于设备 A 尚不知道存在问题，它已发送报文 0、1 和 2，设备 B 将接收它们。但是，设备 B 不会接受它们，即使它们可能是良好的 TLP（这意味着它们未通过 LCRC 检查）。这是因为所有报文必须按顺序接受。所以设备 B 将简单地丢弃这些报文，因为它们被视为顺序错误，但不会发送额外的 Nak。即使这些 TLP 中的一个或多个未通过 LCRC 检查，也不会发送额外的 NAK。NAK_SCHEDULED 标志已置位，只有当设备 B 成功接收到预期的 TLP（本例中为 TLP 4095）时，它才会被清除。

**334**

**第 10 章：Ack/Nak 协议**

5. 设备 A 接收到 Nak 4094，并从重放缓冲区中清除 TLP 4094 和较早的 TLP（本例中没有）。此外，由于已取得进展，它会重置 REPLAY_TIMER 和 REPLAY_NUM 计数。

6. 由于接收到的确认 DLLP 是 Nak 而不是 Ack，设备 A 然后重放重放缓冲区中所有剩余的 TLP（TLP 4095、0、1 和 2）并重新启动 REPLAY_TIMER，并将 REPLAY_NUM 计数加一。

7. 一旦设备 B 接收到重放的 TLP 4095，它将清除 NAK_SCHEDULED 标志，递增 NEXT_RCV_SEQ 计数，并启动 AckNak_LATENCY_TIMER。

_图 10-10：Nak 的示例_

**==> 图片 [372 x 242] 已省略 <==**

**----- 图片文字开始 -----**<br>
Receive Buffer 4094 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>4095<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 4095 LCRC fail<br>Later TLP 2<br>1<br>0 Lat Tmr<br>4095 Nak 0 Out of sequence<br>Earlier TLP 4094 Purge 4094 Ack/Nak<br>Generator<br>Link<br>Replayed TLPs<br>2 1 0 4095 2 1<br>**----- 图片文字结束 -----**<br>


## **TLP 的重复重放**

**概述。** 每次发送方收到 Nak 时，它会重放缓冲区内容，并且 2 位 REPLAY_NUM 计数器递增以跟踪重放事件的数量。前一个示例中由 Nak 导致的重放将使 REPLAY_NUM 递增。

**335**

## **PCI Exress Technology**

如果重放未清除问题，那么我们就进入了新的情况。接收方已设置 Nak Scheduled 标志，并且在看到有问题的 TLP 被正确接收之前无法再发送任何 Ack 或 Nak。如果由于某种原因重放未发生这种情况，则接收方将没有任何响应。拯救我们的是发送方的 REPLAY_TIMER。当它超时时，将重新发送重放缓冲区的全部内容，REPLAY_NUM 计数器将递增，并且 REPLAY_TIMER 将被重置并重新启动。如果 REPLAY_TIMER 在没有收到表示取得进展的 Ack 或 Nak 的情况下到期，则此重放过程可以重复多达三次。如果在第三次重放后仍然没有取得进展并且 REPLAY_TIMER 再次到期，这将导致 REPLAY_NUM 计数器从 3 回绕到 0。
