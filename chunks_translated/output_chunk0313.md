- Receiver Error (optional) — 物理层检测到传入数据包中的错误。该数据包在物理层被丢弃，分配给它的任何缓冲区空间被释放，并通知链路层发生了接收错误。

- Bad TLP — 数据链路层检测到具有错误 LCRC、序列号乱序或错误置空的数据包。在每种情况下，链路层丢弃该数据包并向发送方报告 Nak DLLP，从而触发 TLP 重传。

- Bad DLLP — 数据链路层注意到传入的 DLLP 具有 16 位 CRC 错误，因此该数据包被丢弃。预期随后将出现相同类型的 DLLP 以补偿其包含的信息。

- REPLAY_NUM Rollover — 在数据链路层，一组 TLP 已连续四次发送未成功（没有 Ack），并且此计数器已回滚至零。硬件将自动重新训练链路以尝试清除故障状态，然后通过重放 Replay Buffer 的内容重新开始序列。

**689**

## **PCI Ex ress Technolo p gy**

- Replay Timer Timeout — 在数据链路层，已发送的 TLP 在超时期限内未收到确认（Ack 或 Nak）。硬件自动重放所有未确认的 TLP，这意味着 Replay Buffer 中的所有数据包。

- Advisory Non-Fatal Error — 在对应的 Uncorrectable Error Status 寄存器中记录这些情况的检测（见第 670 页的"Advisory Non-Fatal Errors"）并在此作为可纠正错误。如果启用，它也可能生成 Correctable Error Message。

- Corrected Internal Error (optional) — 检测到设备内部的错误，但它已被纠正或绕过而不会导致不当行为。

- Header Log Overflow (optional) — 已达到可在标头日志中存储的最大标头数。如果未在 Advanced Error Capability and Control 寄存器中设置 Multiple Header Recording Enable 位，则该数字仅为 1。

## **高级可纠正错误屏蔽 (Advanced Correctable Error Masking)**

可纠正错误报告由 Device Control 寄存器中的 Correctable Error Enable 位集中控制，但也由 Correctable Mask 寄存器（如图 15-24 所示）单独控制。屏蔽位的默认状态是清零的，这意味着当检测到任何可纠正错误时，如果已启用（意味着已设置 Correctable Error Enable 位），则可以传递 ERR_COR 消息。但是，软件可以选择设置此屏蔽寄存器中的位以防止在检测到那些特定错误时发送消息。

_图 15-24：Advanced Correctable Error Mask 寄存器_

**==> 图片 [353 x 173] 已省略 <==**

**----- Start of picture text -----**<br>
31 16 15 14 13 12 11 9 8 7 6 5 1 0<br>RsvdP RsvdP RsvdP<br>Header Log Overflow Mask<br>Corrected Internal Error Mask<br>Advisory Non-Fatal Error Mask<br>Replay Timer Timeout Mask<br>REPLAY_NUM Rollover Mask<br>Bad DLLP Mask<br>Bad TLP Mask<br>Receiver Error Mask<br>注意：所有位被指定为 RWS<br>**----- End of picture text -----**<br>


**690**

**第 15 章：错误检测与处理**

## **高级不可纠正错误处理 (Advanced Uncorrectable Error Handling)**

对于不可纠正错误，AER 提供了跟踪已发生的特定错误的能力，控制是否应将其视为 Fatal 或 Non-Fatal，并选择它是否将导致向根发送 Uncorrectable Error Message。

## **高级不可纠正错误状态 (Advanced Uncorrectable Error Status)**

当发生不可纠正错误时，该寄存器中的相应位由硬件自动设置（请参见第 691 页的图 15-25），无论该错误是否将报告给根。如果发生多个错误，硬件将为每个错误设置相应的位，并将首先在 Advanced Error Capability and Control 寄存器的 First Error Pointer 字段中记录哪一个。也有可能在对第一个错误进行服务之前检测到同一错误的多个实例。符合 2.1 规范版本或更高版本的硬件将能够跟踪设计特定数量的此类情况。

_图 15-25：Advanced Uncorrectable Error Status 寄存器_

**==> 图片 [366 x 184] 已省略 <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdZ RsvdZ RsvdZ<br>TLP Prefix Blocked Error Status<br>Atomic Op Egress Blocked Status Undefined<br>MC Blocked TLP Status<br> Uncorrectable Internal Error Status<br>ACS Violation Status<br>Data Link<br>Unsupported Request Error Status Protocol<br>ECRC Error Status Error Status<br>Malformed TLP Status<br>Surprise Down<br>Receiver Overflow Status Error Status<br>Unexpected Completion Status<br>Completer Abort Status<br>Completion Timeout Status<br>Flow Control Protocol Error Status<br>Poisoned TLP Status<br>注意：所有位被指定为 RW1CS<br>**----- End of picture text -----**<br>


以下列表从右到左描述了每个寄存器位：

- Undefined — 以前，该第一位表示物理层的链路训练失败，但该含义已在规范的 1.1 版本中删除

**691**

## **PCI Ex ress Technolo p gy**

的规范。现在软件必须忽略此位中的任何值，但可以向其写入任何值。不再需要此信息，因为位 5（Surprise Down Error）现在在更广泛的含义中包含相同的信息：链路未在物理层通信。

- Data Link Protocol Errors — 由数据链路层协议错误引起，包括 Ack/Nak 重试机制。例如，发送方收到的 Ack 或 Nak 的序列号不对应于未确认的 TLP 或 ACKD_SEQ 编号。

- Surprise Down — 如果物理层报告 LinkUp = 0b（链路不再通信）意外地发生，则这将被视为错误，除非它是允许的异常。例如，如果已设置 Link Disable 位，则 LinkUp 将被清除是预期的，并且这种情况不会是错误。此位仅对 Downstream Ports 有效，因为如果链路不起作用，将无法从 Upstream Port 读取状态。

- Poisoned TLP — 看到的 TLP 设置了 EP 位。

- Flow Control Protocol Error (optional) — 与流控机制失败相关的错误。示例：接收方报告超过 2047 个数据信用。

- Completion Timeout — 在发送 non-posted 请求后，在所需的时间内未收到完成。

- Completer Abort (optional) — Completer 由于请求问题或 Completer 失败而无法完成请求。

- Unexpected Completion — Requester 收到与任何正在等待完成的请求都不匹配的完成。

- Receiver Overflow (optional) — 到达的 TLP 多于 Receive Buffer 容纳的空间，导致溢出错误。

- Malformed TLP — 由与收到的 TLP 标头相关的错误引起（请参见第 666 页的"Malformed TLP"）。

- ECRC Error (optional) — 由接收方的 ECRC 检查失败引起。

- • Unsupported Request Error — Completer 不支持该请求。请求格式正确且没有其他错误，但无法由 Completer 完成，可能是因为它对该设备是无效命令。

- ACS Violation — 在收到的 posted 或 non-posted 请求中看到访问控制错误。

- Uncorrectable Internal Error — 设备内部检测到的错误无法由硬件自身纠正或绕过。

- MC Blocked TLP — 指定用于多播路由的 TLP 被阻止。例如，Egress Port 可被编程为阻止任何到达的具有未翻译地址的 MC 命中（请参见第 896 页的"Routing Multicast TLPs"）。

- AtomicOp Egress Blocked — 路由元素的 Egress Port 可被编

**692**

**第 15 章：错误检测与处理**

   - 程为阻止 AtomicOps 被转发到不应看到它们的代理（请参见第 897 页的"AtomicOps"）。

- TLP Prefix Blocked Error — 路由元素的 Egress Port 可被编程为不转发包含 End-to-End TLP Prefix 的 TLP。如果他们然后看到其中一个，他们将丢弃 TLP 并报告此错误。有关详细信息，请参见第 899 页的"TPH (TLP Processing Hints)"。

回想一下，Capability and Control Register 中的 First Error Pointer 指示自指针上次更新以来哪个未屏蔽的不可纠正错误是第一个到达的。错误处理软件可以读取指针以找出首先要调查的错误。例如，如果指针值为 18d，则表示 Uncorrectable Status 寄存器中的位 18 位置是首先的，这是一个 Malformed TLP。一旦该错误已被处理，软件会向状态寄存器中的位 18 写入 1 以清除该事件，从而将 First Error Pointer 更新为下一个最近的错误

## **选择不可纠正错误的严重性 (Selecting Uncorrectable Error Severity)**

软件可以在此寄存器中选择是否应将不可纠正错误视为 Fatal，从而允许针对不同应用以不同方式处理错误。例如，Poisoned TLP 默认情况下将是 Non-Fatal 条件，并在某些情况下被视为 Advisory Non-Fatal 错误，如前所述。但是软件可以通过将其严重性位设置为 1 来将其升级为 Fatal，然后它将不再是建议性情况。默认严重性值在图 15-26 在第 694 页的各个位字段中说明（1 = Fatal，0 = Non-Fatal）。如果已启用且未屏蔽，那些被选为 Non-Fatal 的错误将导致向根复合体发送 ERR_NONFATAL 消息，那些被选为 Fatal 的错误将导致 ERR_FATAL 消息。

**693**

**PCI Ex ress Technolo p gy**

_图 15-26：Advanced Uncorrectable Error Severity 寄存器_

**==> 图片 [376 x 183] 已省略 <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdP 0 0 0 1 0 0 0 1 1 0 0 0 1 0 RsvdP 1 1 RsvdP x<br>TLP Prefix Blocked Error Severity<br>Atomic Op Egress Blocked Severity Undefined<br>MC Blocked TLP Severity<br> Uncorrectable Internal Error Severity Data Link<br>ACS Violation Severity Protocol Error<br>Unsupported Request Error Severity<br>Severity<br>ECRC Error Severity<br>Malformed TLP Severity Surprise Down<br>Receiver Overflow Severity Error Severity<br>Unexpected Completion Severity<br>Completer Abort Severity<br>Completion Timeout Severity<br>Flow Control Protocol Error Severity<br>Poisoned TLP Severity<br>注意：所有位被指定为 RWS<br>**----- End of picture text -----**<br>


## **不可纠正错误屏蔽 (Uncorrectable Error Masking)**

软件可以使用 Advanced Uncorrectable Error Mask 寄存器（如图 15-27 在第 694 页所示）屏蔽单个错误，因此它们不会导致错误消息被发送。默认情况是允许每种类型的错误消息（所有屏蔽位都被清除）。

_图 15-27：Advanced Uncorrectable Error Mask 寄存器_

**==> 图片 [369 x 187] 已省略 <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdP RsvdP RsvdP<br>TLP Prefix Blocked Error Mask<br>Atomic Op Egress Blocked Mask Undefined<br>MC Blocked TLP Mask<br> Uncorrectable Internal Error Mask<br>ACS Violation Mask<br>Data Link<br>Unsupported Request Error Mask Protocol<br>ECRC Error Mask Error Mask<br>Malformed TLP Mask<br>Surprise Down<br>Receiver Overflow Mask Error Mask<br>Unexpected Completion Mask<br>Completer Abort Mask<br>Completion Timeout Mask<br>Flow Control Protocol Error Mask<br>Poisoned TLP Mask<br>注意：所有位被指定为 RWS<br>**----- End of picture text -----**<br>


**694**

**第 15 章：错误检测与处理**

## **标头记录 (Header Logging)**
