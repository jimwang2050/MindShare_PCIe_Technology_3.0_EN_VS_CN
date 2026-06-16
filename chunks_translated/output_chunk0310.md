- Completer 收到一个由于设备中某些永久性错误状态而无法处理的请求 (Request)。例如，一张无线 LAN 卡因天线未获批而无法通过其无线电进行发送或接收，因此不接受新数据包。

- Completer 收到检测到 ACS (Access Control Services) 错误的请求。这种情况的一个例子是实现 ACS 寄存器的根端口 (Root Port) 启用了 ACS Translation Blocking。如果在该端口上看到 AT 字段不是默认值的内存请求，就会发生 ACS 违规。

- PCIe-to-PCI 桥 (Bridge) 可能收到一个目标为 PCI 总线的请求。PCI 允许目标设备在因某种永久性状态或函数 (Function) 编程规则被违反而无法完成请求时发出目标中止 (target abort)。作为响应，桥将返回一个 CA 状态的完成 (Completion)。

中止请求的 Completer 可以通过 Non-fatal Error Message 向根 (Root) 报告该错误，并且如果该请求需要完成，则状态将为 CA。

## **意外完成 (Unexpected Completion)**

当 Requester 收到完成时，它使用事务描述符 (Requester ID 和 Tag) 将其与先前的请求进行匹配。在极少数情况下，事务描述符可能不匹配任何先前的请求。这可能是因为完成在返回到指定 Requester 的途中被错误路由。收到意外完成的设备可以发送一个 Advisory Non-fatal Error Message，但预计正确的 Requester 最终会超时并采取适当的措施，因此该错误消息优先级较低。

**664**

**第 15 章：错误检测与处理**

## **完成超时 (Completion Timeout)**

对于永不收到其所期望的完成的待处理请求，规范定义了一种完成超时机制。规范明确地将其用于检测完成没有合理机会返回的情况；它应当长于任何正常预期的延迟。

完成超时计时器必须由所有发起期望完成的请求的设备实现，但只发起配置事务的设备除外。另请注意，每个等待完成的请求都是独立计时的，因此必须有一种方法为每个未完成的事务单独计时。规范的 1.x 和 2.0 版本定义了超时值的允许范围，如下所示：

- 强烈建议设备在发出请求后不少于 10ms 才超时；但是，如果设备需要更精细的粒度，超时可以早至 50µs。

- 设备必须不迟于 50ms 超时。

从 2.1 规范版本开始，在 PCI Express Capability Block 中增加了 Device Control Register 2，以便软件可见和控制超时值，如图 15-8 在第 665 页所示。

_图 15-8：Device Control Register 2_

**==> 图片 [152 x 122] 已省略 <==**

**----- Start of picture text -----**<br>
3 oO 0000b = 50µs - 50ms<br>0001b = 50µs - 100µs<br>A<br>0010b = 1ms - 10ms<br>EK of<br>0101b = 16ms - 55ms<br>B<br>0110b = 65ms - 210ms<br>1001b = 260ms - 900ms<br>C<br>1010b = 1s - 3.5s<br>1100b = 4s - 13s<br>D<br>[ 1110b = 17s - 64s<br>高位<br>选择范围<br>**----- End of picture text -----**<br>


如果请求需要多个完成才能返回所请求的数据，单个完成不会停止计时器。相反，计时器会持续运行，直到所有数据都已返回，无论需要多少个完成。如果在超时时仅返回了部分数据，Requester 可以丢弃或保留这些数据。

**665**

**PCI Ex ress Technolo p gy**

## **链路流控相关错误 (Link Flow Control Related Errors)**

在将数据包转发到数据链路层进行传输之前，事务层 (Transaction Layer) 必须检查流控 (Flow Control, FC) 信用，以确保链路邻居的接收缓冲区有足够的空间容纳它。可能发生流控违规，这些违规被认为是不可纠正的。与流控相关的协议违规可由接收流控信息的端口检测到并与之关联。以下给出了一些示例：

- 链路伙伴在任意虚通道 (Virtual Channel) 的 FC 初始化期间未公布规范所定义的至少最小数量的 FC 信用。

- 链路伙伴公布的 FC 信用超过允许的最大数量（数据负载最多 2047 个未使用信用，标头最多 127 个未使用信用）。

- 收到的 FC 更新在初始被通告为无限的信用字段中包含非零值。

- 接收缓冲区溢出，导致数据丢失。此检查是可选的，但检测到的违规被认为是致命 (Fatal) 错误。

## **格式错误的 TLP (Malformed TLP)**

到达事务层的 TLP 会检查其是否违反数据包格式规则。数据包格式的违规被认为是致命错误，因为这意味着发送方在协议上犯了严重错误（例如未能正确维护其计数器），其结果是它不再按预期执行。以下是一些被视为格式错误（malformed）的数据包示例：

- 数据负载超过最大有效负载大小 (Max payload size)。

- 数据长度与标头中指定的长度不匹配。

- 内存起始地址和长度组合导致事务跨越自然对齐的 4KB 边界。

- TLP Digest（TD 字段）指示与数据包大小不对应（ECRC 意外缺失或存在）。

- 字节使能 (Byte Enable) 违规。

- 未定义的 Type 字段值。

- 违反读完成边界 (Read Completion Boundary, RCB) 值的完成。

- 对非配置请求的响应中包含 Configuration Request Retry Status 状态的完成。

- Traffic Class 字段包含未分配给已启用虚通道的值（也称为 TC 过滤）。

**666**

**第 15 章：错误检测与处理**

- I/O 和 Configuration 请求违规（检查可选）— 示例：TC 字段、Attr[1:0] 和 AT 字段必须全部为零，而 Length 字段必须具有值 1。

- 下游发送的中断仿真消息（检查可选）。

- 收到的 TLP 带有 TLP Prefix 错误：

   - 

   - TLP Prefix 但无 TLP Header

- End-to-End TLP Prefix 位于 Local Prefix 之前

- 不支持的 Local TLP Prefix 类型

- 

      - 超过 4 个 End-to-End TLP Prefix

   - End-to-End TLP Prefix 多于所支持的数量

- 需要使用 TC0 的事务类型具有不同的 TC 值：

   - 

   - I/O Read 或 Write 请求以及相应的完成

- Configuration Read 或 Write 请求以及相应的完成

- — Error Messages

- INTx messages

- Power Management messages

- Unlock messages

- Slot Power messages

- LTR messages

- 

   - OBFF messages

- AtomicOp 操作数与架构化值不匹配。

- AtomicOp 地址未与操作数大小自然对齐。

- 事务类型的路由不正确（例如，需要路由到根复合体的事务被发现远离根复合体）。

## **内部错误 (Internal Errors)**

## **问题 (The Problem)**

PCIe 规范的早期版本不包括报告设备内与接口本身事务无关的错误机制。对于端点 (Endpoint) 而言这并不是真正的问题，因为它们具有关联的供应商特定的设备驱动程序，可以检测和报告内部错误。然而，交换机 (Switch) 被视为由操作系统管理的系统资源，通常没有软件来帮助进行内部错误检测。在高端系统中，遏制错误的能力很重要，因此交换机供应商创建了专有的内部错误处理方法。不幸的是，由于不同供应商的解决方案互不兼容，最终结果是它们很少被使用。

**667**

**PCI Ex ress Technolo p gy**

## **解决方案 (The Solution)**

为了缓解这种情况，2.1 规范版本中增加了标准化的内部错误报告选项。什么构成内部错误的定义超出了规范的范围，但它们可以报告为已纠正 (Corrected) 或未纠正 (Uncorrectable) 的内部错误。

Corrected Internal Error 意味着硬件已屏蔽或绕过错误，没有信息丢失或行为不当。例如内部存储位置上的 ECC 错误被自动纠正。另一方面，Uncorrectable Internal Error 意味着操作不当已导致潜在的数据丢失，例如内部存储位置上的奇偶校验错误。报告内部错误是可选的，如果使用它，则必须存在 AER (Advanced Error Reporting) 寄存器以支持它。

## **如何报告错误 (How Errors are Reported)**

## **介绍 (Introduction)**

PCI Express 包含三种报告错误的方法，如下所示。前两种（完成和被毒化的数据包）已在前文介绍，所以我们的下一个主题将是错误消息 (Error Messages)。

- Completions — 完成状态 (Completion Status) 向 Requester 报告错误

- Poisoned Packet — 向接收方报告 TLP 中的坏数据

- Error Message — 向主机（软件）报告错误

## **错误消息 (Error Messages)**

PCIe 取消了 PCI 的边带信号，并用 Error Messages 替代。这些消息提供了 PERR# 和 SERR# 信号无法传达的信息，例如识别检测的函数并指示错误的严重程度。图 15-9 说明了错误消息格式。请注意，它们被路由到根复合体 (Root Complex) 进行处理。Message Code 定义了正在发信号的消息类型。毫不奇怪，规范定义了三种类型的错误消息，如表 15-2 所示。

**668**

**第 15 章：错误检测与处理**

_表 15-2：错误消息代码与描述_

**==> 图片 [389 x 479] 已省略 <==**

**----- Start of picture text -----**<br>
Message<br>Name Description<br>Code<br>30h ERR_COR 设备检测到可纠正错误。这是由硬件自动<br>纠正的，不需要软件干预。但是，无论如<br>何报告它们都可能会有所帮助，这样软件<br>可以观察趋势，例如越来越多的可纠正错误。<br>31h ERR_NONFATAL 指示不可纠正的 Non-Fatal 错误。没有可<br>用的硬件纠正机制，但链路仍然可靠地工作。<br>将需要软件关注以解决该问题。<br>33h ERR_FATAL 指示不可纠正的 Fatal 错误。没有可用的硬<br>件纠正机制，且链路操作在某些重要方面已<br>失败。将需要软件关注，并且可能需要至少<br>重置一个设备才能解决此问题。<br>图 15-9：错误消息格式<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 1 1 0  0 0 0 tr H D P<br>Message Code<br>Byte 4 Requester ID Tag<br>(30h, 31h or 33h)<br>Byte 8 错误消息保留<br>Byte 12 错误消息保留<br>路由到根复合体 30h = ERR_COR<br>31h = ERR_NONFATAL<br>33h = ERR_FATAL<br>**----- End of picture text -----**<br>


**669**

**PCI Ex ress Technolo p gy**

## **建议性非致命错误 (Advisory Non-Fatal Errors)**
