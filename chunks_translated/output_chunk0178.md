## **Ack/Nak 协议**

第 74 页图 2-25 所示的纠错功能由一种基于硬件的自动重试机制提供。如第 75 页图 2-26 所示，每个发出的 TLP 都会附加一个 LCRC（链路 CRC）和序列号（Sequence Number），由接收方进行校验。发送器（Transmitter）的重放缓冲区（Replay Buffer）会保存每一个已发送 TLP 的副本，直到相邻设备确认已成功接收。该确认由接收器（Receiver）发送一个 Ack DLLP（ACK DLLP，确认 DLLP）实现，其中包含其所见到的最后一个正确 TLP 的序列号。当发送器看到该 Ack 后，便将该序列号对应的 TLP 以及所有在它之前已发送的 TLP 一并从重放缓冲区中清除。

如果接收器检测到 TLP 错误，它会丢弃该 TLP，并向发送器返回一个 Nak，随后发送器会重放所有未被确认的 TLP，希望在下一次能够得到正确结果。由于被检测到的错误几乎都是瞬态事件，重放通常能够纠正该问题。该过程通常被称为 Ack/Nak 协议。

_图 2-25：数据链路层重放机制_

**==> picture [314 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
From To<br>事务层（Transaction Layer） 事务层（Transaction Layer）<br>Tx Rx<br>数据链路层（Data Link Layer）<br>链路（Link）包 DLLP DLLP 链路（Link）包<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux<br>Error<br>Mux Check<br>Tx Rx<br>Link<br>**----- End of picture text -----**<br>

**74**

**第 2 章：PCIe 架构概述**

_图 2-26：数据链路层处 TLP 和 DLLP 的结构_

**==> picture [368 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
事务层包（TLP, Transaction Layer Packet）<br>序列号 ID（Sequence ID） 包头（Header） 数据有效负载（Data Payload）  ECRC LCRC<br>AND<br>DLLP<br>DLLP Type Misc. CRC<br>**----- End of picture text -----**<br>

DLLP 的基本形式同样在第 75 页图 2-26 中展示，它由一个 4 字节的 DLLP Type 字段（可能包含一些其他信息）和一个 2 字节的 CRC 组成。

第 76 页图 2-27 给出了一个跨交换机（Switch）的内存读操作示例。一般来说，本例的步骤如下：

1. **步骤 1a**：请求者（Requester）发送一个内存读请求，并将其副本保存在重放缓冲区中。交换机接收到该 MRd TLP，并检查其 LCRC 和序列号。

   - 步骤 1b：由于未检测到错误，交换机向请求者返回一个 Ack DLLP。作为响应，请求者从重放缓冲区中丢弃该 TLP 的副本。

2. **步骤 2a**：交换机根据内存地址进行路由，将该 MRd TLP 转发到正确的下游端口（Egress Port），并将其副本保存在该下游端口的重放缓冲区中。完成器（Completer）收到 MRd TLP 后进行错误检查。**步骤 2b**：未检测到错误，因此完成器向交换机返回 Ack DLLP。交换机端口从其重放缓冲区中清除该 MRd TLP 的副本。

3. **步骤 3a**：作为该请求的最终目的地，完成器检查 MRd TLP 中的可选 ECRC 字段。未检测到错误，因此该请求被传递至核心逻辑。设备根据该命令获取所请求的数据，并返回一个带数据的完成报文 TLP（CplD），同时将副本保存在重放缓冲区中。交换机收到 CplD TLP 后进行错误检查。**步骤 3b**：未检测到错误，因此交换机向完成器返回 Ack DLLP。完成器从重放缓冲区中丢弃该 CplD TLP 的副本。

4. **步骤 4a**：交换机解码 CplD TLP 中的请求者 ID（Requester ID）字段，并将该报文路由到正确的下游端口，同时将副本保存在该下游端口的重放缓冲区中。请求者收到 CplD TLP 后进行错误检查。**步骤 4b**：未检测到错误，因此请求者向交换机返回 Ack DLLP。交换机从重放缓冲区中丢弃该 CplD TLP 的副本。请求者检查可选的 ECRC 字段，未发现错误，于是数据被上送至核心逻辑。

**75**
