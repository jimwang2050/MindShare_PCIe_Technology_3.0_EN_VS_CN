当根收到 Error Message 时，它采取的操作部分由 Root Control 寄存器中的设置决定。图 15-18 描述了此寄存器并突出显示了指定是否应将收到的 Error Message 报告为 System Error 的三个字段。在一些基于 x86 的系统中，如果错误被启用以触发 System Error，则可能会发出 NMI (Non-Maskable Interrupt)。

通过标准寄存器无法配置报告 Error Message 的其他选项。最可能的情况是向处理器发出将调用错误处理程序 (Error Handler) 的中断，它可能会记录错误并尝试清除问题。

**682**

**第 15 章：错误检测与处理**

_图 15-18：Root Control 寄存器_

**==> 图片 [313 x 142] 已省略 <==**

**----- Start of picture text -----**<br>
15 5 4 3 2 1 0<br>RsvdP<br>CRS Software Visibility Enable<br>PME Interrupt Enable<br>System Error on Fatal Error Enable<br>System Error on Non-Fatal Error Enable<br>System Error on Correctable Error Enable<br>**----- End of picture text -----**<br>


## **链路错误 (Link Errors)**

链路故障通常在物理层检测到，并传送到数据链路层。对于下游设备，如果链路遇到 Fatal 错误且无法正常运行，则无法向主机报告错误。在这些情况下，错误必须由上游设备报告。如果软件可以将错误隔离到给定链路，则处理不可纠正错误（或防止将来发生不可纠正错误）的一个步骤是重新训练链路。Link Control 寄存器包括一个允许软件强制链路重新训练的位，如图 15-19 在第 684 页所示。如果这解决了问题，则操作会在很少停机的情况下恢复。

**683**

**PCI Ex ress Technolo p gy**

_图 15-19：Link Control 寄存器 — 强制链路重新训练_

**==> 图片 [297 x 260] 已省略 <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


一旦请求重新训练后，软件可以轮询 Link Status 寄存器中的 _Link Training_ 位以查看训练何时完成。图 15-20 突出显示此状态位。当此位为 1b 时，链路仍处于重新训练过程中（或尚未开始重新训练）。一旦物理层报告链路处于活动状态（意味着训练过程已成功完成），硬件将清除此位。

**684**

**第 15 章：错误检测与处理**

_图 15-20：Link Status 寄存器中的链路训练状态_

**==> 图片 [360 x 167] 已省略 <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


## **高级错误报告 (AER, Advanced Error Reporting)**

图 15-21 在第 686 页所示的高级错误报告结构允许更复杂的错误处理。这些寄存器提供以下一些附加功能：

- 更好地粒度地记录实际发生的错误类型

- 控制指定每种不可纠正错误类型的严重性

- 支持记录有错误的数据包的标头

- 标准化根的控制以中断形式报告收到的 Error Message

- 识别 PCIe 拓扑中错误的来源

- 能够屏蔽报告个别类型的错误

**685**

## **PCI Ex ress Technolo p gy**

_图 15-21：Advanced Error Capability 结构_

|Root Ports &<br>Root Complex<br>Event Collectors<br>Functions<br>that support<br>TLP Prefixes|Root Error Command<br>Root Error Status<br>Uncorr.  Error Source ID<br>Corr.  Error Source ID<br>TLP Prefix Log Register<br>00h<br>04h<br>08h<br>0Ch<br>10h<br>14h<br>18h<br>1Ch<br>2Ch<br>30h<br>34h<br>38h<br>PCIe Extended CapabilityRegister<br>Uncorrectable Error Status Register<br>Uncorrectable Error Mask Register<br>Uncorrectable Error SeverityRegister<br>Correctable Error Status Register<br>Correctable Error Mask Register<br>Advanced Error Capability and Control Register<br>Header Log Register|
|---|---|



## **Advanced Error Capability and Control**

让我们从查看 Advanced Error Capability and Control 寄存器开始对 AER 的讨论。端到端 CRC (ECRC) 生成和检查需要 AER，并且此寄存器（如图 15-22 在第 687 页所示）报告

**686**

**第 15 章：错误检测与处理**

此设备是否支持 ECRC。如果支持，配置软件可以通过设置适当的位来启用（并强制）使用它。

此寄存器的低 5 位包含 First Error Pointer，由硬件在更新 Uncorrectable Error 状态位时设置。共有 32 个状态位，First Error Pointer 指示哪个未屏蔽的 Uncorrectable Error 是首先被检测到的，即当所有其他状态位仍为 0 时设置了哪个状态位。第一个错误是最有趣的，因为其他错误可能是由第一个错误引起的。

_图 15-22：Advanced Error Capability and Control 寄存器_

|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||
|RsvdP<br>ECRC Check Enable(RWS)<br>ECRC Check Capable(RO)<br>ECRC Generation Enable(RWS)<br>ECRC Generation Capable(RO)<br>Multiple Header Recording Capable(RO)<br>Multiple Header Recording Enable(RWS<br>TLP Prefix Log Present(ROS)<br>31|||||First Error<br>Pointer (ROS)<br><br>)<br>0<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12|||||||||
||RsvdP||||||||||||First Error<br>Pointer (ROS)|
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||



从 2.1 规范版本开始，此功能得到增强，允许跟踪多个错误。因此，如果多个错误状态位已被设置和清除，那么其含义实际上更像"最旧错误指针"（Oldest Error Pointer）。当相应的状态位被软件清除时，指针由硬件更新，此时它指向下一个检测到的错误（有关不可纠正错误的列表，请参见第 691 页的图 15-25）。有趣的是，如果该错误已被多次检测，则下一个错误可能再次是相同的错误，其结果是更新的指针仍指示相同的值。

由于可以在 Uncorrectable Status 寄存器中记录多个错误，因此存储多个标头也将非常有帮助。硬件必须被设计为能够记录至少一个标头，但允许支持更多。如果支持，则 Multiple Header Recording Capable 位将被设置，并且 Multiple Header Recording Enable 位可用于启用存储多个标头。每当 First Error Pointer 指示未设置或未实现的状态位位置时，这意味着没有更多不可纠正错误需要处理。

**687**

**PCI Ex ress Technolo p gy**

此寄存器中的最后一位 TLP Prefix Log Present 指示 TLP Prefix Log 寄存器是否包含 First Error Pointer 指示的不可纠正错误的有效信息。

此寄存器中的字段以及其他 AER 寄存器具有各种特征，缩写如下：

- RO — Read Only，由硬件设置

- ROS — Read Only and Sticky（见下一节关于 sticky 位）

- RsvdP — Reserved and Preserved。这些位不得用于任何目的，但软件必须小心维护它们包含的任何值。

- RsvdZ — Reserved and Zero。不得用于任何目的，并且必须始终写入零的位。

- RWS — Readable, Writeable and Sticky

- • RW1CS — Readable, Write 1 to Clear, and Sticky

## **处理粘性位 (Handling Sticky Bits)**

几个 AER 寄存器字段采用 sticky 位，这意味着重置不会清除其内容。所有其他寄存器字段在重置时都强制为默认值，但这些不会。这是一个好主意，因为链路可能遇到无法在不复位的情况下清除的故障。如果问题出在失败链路的下游设备中，则在链路再次工作之前其寄存器内容不可用，重置将实现这一点。但是如果寄存器被重置清除，则信息将丢失。为了解决这个问题，sticky 位通过重置保持错误状态信息可用。具体来说，sticky 位将在 FLR (Function Level Reset)、热复位 (Hot Reset) 和热重启 (Warm Reset) 中存活下来，因为有电源使其保持活动状态。如果有像 Vaux 这样的辅助电源在主电源关闭时使其保持活动状态，则它们甚至可以在冷复位 (Cold Reset) 中存活。

## **高级可纠正错误处理 (Advanced Correctable Error Handling)**

高级错误报告提供了记录已检测到哪些特定可纠正错误的能力。这些错误可用于向主机系统发起 Correctable Error Message。尽管系统操作继续正常进行，但报告可纠正错误可能很有用，因为它允许系统软件查看哪些组件出现问题并预测它们将来是否可能完全失败。

**688**

**第 15 章：错误检测与处理**

## **高级可纠正错误状态 (Advanced Correctable Error Status)**

可纠正错误将自动在 Advanced Correctable Error Status 寄存器（如图 15-23 在第 689 页所示）中设置相应的位，无论该错误是否通过 Error Message 报告。这些位通过软件向位位置写入"1"来清除，因此被指定为 RW1CS。

_图 15-23：Advanced Correctable Error Status 寄存器_

|31|31||16|15|14|13|12|11|9|8|8|7|7|6|6|5||1|0|0||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||RsvdZ||||||RsvdZ|||||||||RsvdZ|||||
|||Header Log Overflow Status||||||||||||||||||||
|||Corrected Internal Error Status||||||||||||||||||||
|||Advisory Non-Fatal Error Status||||||||||||||||||||
|||Replay Timer Timeout Status||||||||||||||||||||
|||REPLAY_NUM Rollover Status||||||||||||||||||||
|||Bad DLLP Status||||||||||||||||||||
|||Bad TLP Status||||||||||||||||||||
|||Receiver Error Status||||||||||||||||||||
||||注意：所有位被指定为 RW1CS||||||||||||||||||||


