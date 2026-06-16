|Type [4:0]|Byte 0 Bit 4:0|对于 Completion，包类型是 01010b。|

**197**

## **PCI Express Technology**

*Table 5‐7: Completion Header Fields (Continued)*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Completion 必须在此处使用与相应 Request 相同的值。|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|指示此 TLP 是否使用基于 ID 的排序。要了解更多信息，请参见第 301 页 "ID Based Ordering (IDO)"。|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|对于 Completion 是保留的。|
|TD<br>(TLP Digest)|Byte 2 Bit 7|如果 = 1，指示 TLP 末端存在 digest 字段。|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|如果 = 1，指示数据负载已被 poison。|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Completion 必须在此处使用与相应 Request 相同的值。|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|对于 Completion，Address Type 是保留的且必须为零，但不要求甚至不建议接收方检查此字段。|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|指示 DW 中的数据负载大小。对于 Completion，此字段反映与此完成相关联的数据负载大小。|
|Completer ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识 Completer 以支持问题调试。<br>Byte 4 7:0 = Completer Bus #<br>Byte 5 7:3 = Completer Dev #<br>Byte 5 2:0 = Completer Function #|

**198**

**Chapter 5: TLP Elements**

*Table 5‐7: Completion Header Fields (Continued)*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Compl. Status [2:0]<br>(Completion Status<br>Code)|Byte 6 Bit 7:5|这些位指示此 Completion 的状态。<br>000b = Successful Completion (SC)<br>001b = Unsupported Request (UR)<br>010b = Config Req Retry Status (CRS)<br>100b = Completer abort (CA)<br>所有其他代码均保留。请参见第 200 页 "Summary of Completion Status Codes"。|
|BCM<br>(Byte Count Modified)|Byte 6 Bit 4|这仅由 PCI‐X Completer 使用，指示 Byte Count 字段仅报告第一个负载而不是剩余的总负载。请参见第 201 页 "Using The Byte Count Modified Bit"。|
|Byte Count [11:0]|Byte 6 Bit 3:0<br>Byte 7 Bit 7:0|满足读请求的剩余字节数，由原始请求的 Length 字段派生。请参见第 201 页 "Data Returned For Read Requests:" 了解由多个完成引起的特殊情况。|
|Requester ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|从 Request 复制，用作此 Completion 的返回地址（目标）。<br>Byte 8, 7:0 = Requester Bus #<br>Byte 9, 7:3 = Requester Device #<br>Byte 9, 2:0 = Requester Function #|
|Tag [7:0]|Byte 10 Bit 7:0|这必须是随 Request 接收的 Tag 值。Requester 根据 Tag 将此 Completion 与挂起的 Request 关联。|

**199**

**PCI Express Technology**

*Table 5‐7: Completion Header Fields (Continued)*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Lower Address [6:0]|Byte 11 Bit 6:0|为读请求返回的第一个数据的字节对齐地址的低 7 位。由 Request 的 Length 和 Byte Enables 计算得出，它通过显示在到达下一个 Read Completion Boundary 之前可以传输多少字节来协助缓冲区管理。请参见第 200 页 "Calculating Lower Address Field"。|

## **Summary of Completion Status Codes.**

- 000b (SC) Successful Completion：请求被正确服务。

- 001b (UR) Unsupported Request：请求不合法或未被 Completer 识别。这是一种错误情况，但 Completer 的响应方式取决于其设计所遵循的规范修订版本。在 1.1 规范之前，这被视为不可纠正的错误，但对于 1.1 及更高版本，它被视为 Advisory Non‐Fatal Error。详见第 663 页 "Unsupported Request (UR) Status"。

- 010b (CRS) Configuration Request Retry Status：Completer 暂时无法服务配置请求，应在稍后重试该请求。

- 100b (CA) Completer Abort：Completer 本应能够服务该请求但出于某种原因失败。这是一种不可纠正的错误。

**Calculating The Lower Address Field.** 此字段由 Completer 设置，以反映完成负载中返回的第一个已启用数据字节的字节对齐地址。硬件通过考虑 DW 起始地址和原始请求中 First DW Byte Enable 字段中提供的 Byte Enable 模式来计算此值。

对于 Memory Read 请求，地址是 DW 起始地址的偏移量：

- 如果 First DW Byte Enable 字段为 1111b，则第一个 DW 中的所有字节都被启用，偏移量为 0。此字段与 DW 对齐的起始地址匹配。

- 如果 First DW Byte Enable 字段为 1110b，则第一个 DW 中的高三字节被启用，偏移量为 1。此字段是 DW 起始地址 + 1。

- 如果 First DW Byte Enable 字段为 1100b，则第一个 DW 中的高二字节被启用

**200**

**Chapter 5: TLP Elements**

- 在第一个 DW 中，偏移量为 2。此字段是 DW 起始地址 + 2。

- • 如果 First DW Byte Enable 字段为 1000b，则第一个 DW 中只有高字节被启用，偏移量为 3。此字段是 DW 起始地址 + 3。

计算后，将低 7 位放入完成头的 Lower Address 字段中，以便处理读完成小于整个负载并需要在第一个 RCB 处停止的情况。事务的拆分必须在 RCB 上进行，传输到第一个 RCB 的字节数基于起始地址。

对于 AtomicOp Completion，Lower Address 字段是保留的。对于所有其他 Completion 类型，它设置为零。

**Using The Byte Count Modified Bit.** 此位仅由 PCI‐X Completer 设置，但如果使用 PCIe 到 PCI‐X 的桥，它们可能存在于 PCIe 拓扑中。其断言的规则包括：

1. 仅当读请求将被拆分为多个完成时，才由 PCI‐X Completer 设置。

2. 仅针对该系列的第一个 Completion 设置，且仅当第一个 Completion 包含反映第一个 Completion 负载（而不是总剩余负载）的 Byte Count 字段时才设置。Requester 理解，尽管 Byte Count 似乎表明这是此请求的最后一个 Completion，但实际上此 Completion 之后还会有其他 Completion 来满足原始请求的需要。

3. 对于该系列的后续 Completion，必须取消断言 BCM 位，且 Byte Count 字段将照常反映总剩余计数。

4. 接收设置了 BCM 位的 Completion 的设备必须正确解释这种情况。

5. Lower Address 字段由 Completer 在带数据的完成期间设置，以反映正在返回的第一个已启用数据字节的地址

## **Data Returned For Read Requests:**

1. 读请求可能需要多个完成才能得到满足，但总的数据传输最终必须等于原始请求的大小，否则可能会导致 Completion Timeout 错误。

2. 给定的 Completion 只能服务一个 Request。

3. IO 和 Configuration 读始终为 1 DW，并且将始终由单个 Completion 满足

4. 状态码不是 SC（成功）的 Completion 终止事务。

**201**

## **PCI Express Technology**

5. 在处理具有多个完成的读请求时必须遵守 Read Completion Boundary (RCB)。对于根复合体 (Root Complex)，RCB 为 64 字节或 128 字节，因为允许修改其端口之间流动的包的大小，并且所使用的值在配置寄存器中可见。

6. 桥和端点可以实现一个用于在软件控制下选择 RCB 大小（64 或 128 字节）的位。

7. 完全在已对齐 RCB 边界内的 Completion 必须一次传输完成，因为传输不会到达 RCB，而 RCB 是合法早期停止的唯一位置。

8. 单个读请求的多个 Completion 必须按升序地址返回数据。

## **Receiver Completion Handling Rules:**

1. 收到的与挂起请求不匹配的 Completion 是 Unexpected Completion，被视为错误。

2. 状态码不是 SC 或 CRS 的 Completion 将作为错误处理，与之关联的缓冲区空间将被释放。

3. 当根复合体在配置周期中收到 CRS 状态时，请求被终止。接下来发生什么是实现特定的，但如果根支持它，则该操作由其 Root Control 寄存器中 CRS Software Visibility 位的设置定义。

   - 如果未启用 CRS Software Visibility，根将针对实现特定的次数重新发出配置请求，然后放弃并断定目标有问题。

   - 如果启用了 CRS Software Visibility，设计为支持它的软件将始终先读取 Vendor ID 字段的两个字节。如果硬件随后收到该 Request 的 CRS，它将返回值 0001h 作为 Vendor ID。该值由 PCI‐SIG 保留用于此用途，不对应于任何有效的 Vendor ID，并将此事件通知软件。这允许软件在等待目标就绪时（可能在复位后长达 1 秒）继续执行其他任务，而不是停滞不前。任何其他配置读或写将由根作为新请求自动重试设计特定的迭代次数。

4. 对配置以外的请求的 CRS 状态是非法的，可能被报告为 Malformed TLP。

5. 状态码为保留代码的 Completion 按代码为 UR 进行处理。6. 如果收到的读完成或 AtomicOp 完成的状态不是 SC，则完成中不包含数据，Requester 必须认为此 Request 已终止。Requester 如何处理这种情况是实现特定的。

**202**

**Chapter 5: TLP Elements**

7. 在为读请求返回多个完成的情况下，状态码不是 SC 的完成将结束事务。设备对错误之前接收的数据的处理是实现特定的。

8. 为了与 PCI 兼容，当配置周期以指示 Unsupported Request 的完成结束时，根复合体可能需要合成全"1"的读值。这类似于当枚举软件尝试从未存在的设备读取时发生的 PCI Master Abort。

## **Message Requests**

Message Request 取代了 PCI 和 PCI‐X 上使用的许多中断、错误和电源管理的边带信号。所有 Message Request 都使用 4DW 头格式，但并非所有字段在每种消息类型中都被使用。第 8 到 15 字节的字段对于某些 Messages 没有定义，并在这些情况下保留。Messages 的处理方式很像 Posted Memory Write 事务，但它们的路由可以基于地址、ID，并且在某些情况下路由可以是隐式的。包头中的 _routing subfield_（Byte 0, bits 2:0）指示使用哪种路由方法以及定义了哪些附加头寄存器。通用的 Message Request 头格式显示在第 203 页的图 5‐11 中。

*Figure 5‐11: 4DW Message Request Header Format*