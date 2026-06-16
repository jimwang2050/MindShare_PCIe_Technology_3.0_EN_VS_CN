Advanced Error Reporting 结构的 4DW 部分用于存储发生未屏蔽、不可纠正错误的收到 TLP 的标头。由于当物理层或数据链路层未看到 TLP 出现问题时，标头记录才有用，因此可能性数量有限，如表 15-6 在第 695 页所示。如前所述，当实现可选的 AER 功能时，硬件必须能够记录至少一个标头，尽管它可能支持记录更多。

当 First Error Pointer 有效时，标头日志包含相应错误的标头（如果它是由传入的 TLP 引起的）。更新 Uncorrectable Error Status 寄存器将导致 Header Log 寄存器也按顺序更新为下一个值，这意味着下一个被检测到的不可纠正错误。由于硬件只能跟踪有限数量的标头，因此软件必须足够快地处理不可纠正的错误以避免耗尽标头空间。如果达到标头日志容量，则这本身就是一个可纠正的错误（Header Log Overflow）。如果超出支持的日志寄存器数量，或者如果未设置 Multiple Header Log Enable 位且在检测到新的不可纠正错误时 First Error Pointer 已有效，则可能会发生这种情况。

_表 15-6：可以使用 Header Log 寄存器的错误_

|**错误名称**|**默认分类**|
|---|---|
|Poisoned TLP Received|Uncorrectable - NonFatal|
|ECRC Check Failed|Uncorrectable - NonFatal|
|Unsupported Request|Uncorrectable - NonFatal|
|Completer Abort|Uncorrectable - NonFatal|
|Unexpected Completion|Uncorrectable - NonFatal|
|ACS Violation|Uncorrectable - NonFatal|
|Malformed TLP|Uncorrectable - Fatal|



**695**

**PCI Ex ress Technolo p gy**

## **根复合体错误跟踪和报告 (Root Complex Error Tracking and Reporting)**

根复合体是 PCIe 拓扑中设备的所有错误消息的目标。根收到的错误会更新状态寄存器，并在启用时可能报告给主机系统。

## **根复合体错误状态寄存器 (Root Complex Error Status Registers)**

当根收到错误消息时，它会在 Root Error Status 寄存器（如图 15-28 在第 697 页所示）中设置状态位。该寄存器指示收到的错误类型以及是否已收到相同类型的多个错误。请注意，在 Root Port 本身检测到的错误也会设置这些状态位，就好像该端口已向自身发送了错误消息一样。状态位为：

- ERR_COR Received

- Multiple ERR_COR Received — 收到 ERR_COR 消息，或在 ERR_COR Received 位已设置时检测到未屏蔽的根端口可纠正错误。

- ERR_FATAL/NONFATAL Received

- Multiple ERR_FATAL/NONFATAL Received — 收到 ERR_FATAL 或 ERR_NONFATAL 消息，或在 ERR_FATAL/NONFATAL Received 位已设置时检测到未屏蔽的根端口不可纠正错误。

系统可能为 Correctable、Non-Fatal 和 Fatal 错误实现单独的软件错误处理程序，因此该寄存器包括用于区分不可纠正错误是 Fatal 还是 Non-Fatal 的位：

- 如果收到的第一个 Uncorrectable Error Message 是 Fatal，则"First Uncorrectable Fatal"位也会与"Fatal Error Message Received"位一起设置。

- 如果收到的第一个 Uncorrectable Error Message 是 Non-Fatal，则设置"Non-fatal Error Message Received"位。（如果随后的 Uncorrectable Error 是 Fatal，则将设置"Fatal Error Message Received"位，但由于"First Uncorrectable Fatal"保持清零，软件知道第一个 Uncorrectable Error 是 Non-Fatal）。

**696**

**第 15 章：错误检测与处理**

_图 15-28：Root Error Status 寄存器_

**==> 图片 [327 x 143] 已省略 <==**

**----- Start of picture text -----**<br>
31 27 26 7 6 5 4 3 2 1 0<br>RsvdZ<br>Advanced Error Interrupt Message Number (RO)<br>Fatal Error Messages Received<br>Non-Fatal Error Messages Received<br>RW1CS First Uncorrectable Fatal<br>Multiple ERR_FATAL/NONFATAL Received<br>ERR_FATAL/NONFATAL Received<br>Multiple ERR_COR Received<br>ERR_COR Received<br>**----- End of picture text -----**<br>


最后，可能已（在 Root Error Command 寄存器中）启用中断以作为检测到这些事件之一的结果发送到主机系统。为了支持这一点，此寄存器中的 5 位 Interrupt Message Number 提供了要使用的 MSI 或 MSI-X 向量号，共有 32 种可能。对于 MSI，该号是距基本数据模式的偏移。对于 MSI-X，它表示要使用的表条目，并且必须是前 32 个中的一个，即使代理支持超过 32 个。此只读值由硬件设置，并且必须在分配给设备的 MSI 消息数更改时自动更新。

## **Advanced Source ID 寄存器 (Advanced Source ID Register)**

软件错误处理程序可能需要读取和清除检测和报告错误的设备中的状态寄存器。为此，错误消息包含报告该错误类型的第一个设备的 ID（Bus:Dev:Func）。如果尚未设置 ERR_FATAL/NONFATAL 位（意味着这是第一个），则 Source ID 寄存器从消息中为传入的 ERR_FATAL/NONFATAL 消息捕获该 ID。类似地，第一个收到的 ERR_COR 消息的 Source ID 也被捕获，如图 15-29 在第 698 页所示。

**697**

**PCI Ex ress Technolo p gy**

_图 15-29：Advanced Source ID 寄存器_

**==> 图片 [327 x 47] 已省略 <==**

**----- Start of picture text -----**<br>
31 0<br>ERR_FATAL/NONFATAL Source ID ERR_COR Source ID<br>(ROS) (ROS)<br>ROS: Read-Only and Sticky<br>**----- End of picture text -----**<br>


## **根错误命令寄存器 (Root Error Command Register)**

根复合体对三种错误类别中的每一种都有单独的启用位，以控制该错误类型是否将生成中断以调用错误处理程序，如图 15-30 在第 698 页所示。生成的中断将是 MSI 或 MSI-X，如"根复合体错误状态寄存器"中第 696 页所述。一旦收到中断，被调用的错误处理程序可能首先读取根复合体状态寄存器以确定错误的性质，然后转到错误的源 BDF 读取标准状态寄存器以及可能的设备特定寄存器以确定发生了什么以及应如何处理。

_图 15-30：Advanced Root Error Command 寄存器_

**==> 图片 [332 x 93] 已省略 <==**

**----- Start of picture text -----**<br>
31 3 2 1 0<br>RsvdP<br>Fatal Error Reporting Enable<br>Non-Fatal Error Reporting Enable<br>Correctable Error Reporting Enable<br>注意：所有位被指定为 RW<br>**----- End of picture text -----**<br>


## **错误记录和报告摘要 (Summary of Error Logging and Reporting)**

规范包括第 699 页的图 15-31 中的流程图，显示了函数在检测到错误时采取的操作。虚线内的部分突出显示了存在可选 AER 功能结构时添加的项目。

**698**

**第 15 章：错误检测与处理**

_图 15-31：函数内错误处理流程图_

**==> 图片 [327 x 391] 已省略 <==**

**----- Start of picture text -----**<br>
Error Detected<br>Uncorrectable Error Type? Correctable<br>Determine severity using<br> Uncorrectable Error Severity Register<br>Advisory Yes AER Yes<br>Non-Fatal Error? Implemented?<br>No No<br>Set Fatal/NonFatal Error Detected bit Set Correctable Error Detected bit<br>in Device Status Reg Done in Device Status Reg<br>If UR, set Unsupported Request If UR, set Unsupported Request<br> Detected bit in Device Status Reg  Detected bit in Device Status Reg<br>Advanced Set corresponding bit in<br>Uncorrectable Error Status RegSet corresponding bit in Error Correctable Error Status Reg<br>Reporting<br>Only Is error masked in Yes<br>Correctable Error Mask<br>Masked in Yes  Register?<br>Uncorrectable Error Mask<br> Register? No Done<br>No Done 1) Set Uncorrectable Error status bit, andIf Advisory Non-Fatal Error:<br>header, and update prefix and header As appropriate, record prefix and reporting fields and registers 2) If not masked by Uncorrectable mask,header, and update prefix and header as appropriate, record prefix and reporting fields and registers<br>both SERR and UR ReportingUR Error anddisabled? Yes UR Reporting disabled?UR error and Yes<br>No Done No Done<br>Fatal Non-Fatal<br>Severity?<br>SERR enabled or No SERR enabled or No Correctable Reporting  No<br>Fatal Error Reporting Non-Fatal Error Reporting Enabled?<br>Enabled? Enabled?<br>Yes Done Yes Done Yes Done<br>Send ERR_FATAL Send ERR_NONFATAL Send ERR_COR<br>Done Done Done<br>**----- End of picture text -----**<br>


## **软件错误调查的示例流程 (Example Flow of Software Error Investigation)**

现在我们已经了解了 PCIe 中定义的用于检测、记录和报告错误的所有机制，值得看看软件将如何找到并使用此信息来确定如何处理报告的错误。

**699**

## **PCI Ex ress Technolo p gy**

本示例将假设发起函数及其上游根端口都支持 AER。如果没有 AER 支持，则用于错误记录的标准寄存器非常有限。

本示例中使用的系统如图 15-32 在第 701 页所示。根端口的 BDF 为 0:28:0，并已启用以在收到 ERR_FATAL 或 ERR_NONFATAL 消息时生成中断。我们将按照错误处理软件将采取的步骤来确定已发生什么错误、在哪里发生以及在哪些数据包中检测到它们。

由于来自根端口 0:28:0 的中断，已调用错误处理软件。下面的步骤只是一个示例，但说明了错误处理软件收集错误信息的过程。

1. 软件根据使用的中断向量知道调用错误处理程序的是根端口 0:28:0。由于使用 MSI 或 MSI-X 中断来报告错误，因此每个根端口将具有自己唯一的一组中断向量。

2. 错误处理程序读取 0:28:0 上 AER 结构的 Root Error Status 寄存器，以确定根端口已收到哪些类型的错误消息。该寄存器中的值为 0800_007Ch，表示此根端口未收到任何 ERR_COR 消息，但已收到 ERR_FATAL 和 ERR_NONFATAL 消息，并且它收到的第一个不可纠正的错误消息是 ERR_FATAL。

3. 下一步是确定此根端口下的哪个 BDF 发送了第一个不可纠正错误。然后，软件读取根端口的 Source ID 寄存器，并找到值 0500_0000h，这表示第一个不可纠正错误的源 BDF 为 5:0:0。

4. 现在软件知道根端口 0:28:0 收到的第一个不可纠正错误是从 BDF 5:0:0 发起的 Fatal 错误。有了此信息，软件然后去读取 BDF 5:0:0 上的 Uncorrectable Error Status 寄存器，以查看在该 BDF 上已发生哪些特定的不可纠正错误。从该读取返回的值是 0004_1000h，这意味着此 BDF 已检测到至少一个 Malformed TLP 和至少一个 Poisoned TLP。但错误处理程序真正关心的是哪个先发生，因为那就是要首先处理的。

5. 为了确定多个不可纠正错误中哪个先发生，软件然后读取 5:0:0 的 Advanced Error Capability and Control 寄存器，并找到值 0000_0012h，其 First Error Pointer 值为 12h，表示第一个不可纠正错误是 Malformed TLP（位 18d），而不是 Poisoned TLP（位 12d）。

**700**

**第 15 章：错误检测与处理**

_图 15-32：错误调查示例系统_
