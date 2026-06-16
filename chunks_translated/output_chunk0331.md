多年前，PCI 将 MSI 支持作为可选项添加，而 PCIe 将该功能设为必需。能够自行生成 MSI 事务的外围设备为处理中断开辟了新的选择，例如赋予每个 Function 生成多个唯一中断的能力，而不仅仅是一个。

## **旧式 PCI 中断传递**

本节提供有关旧式 PCI 中断传递的更多详细信息。熟悉 PCI 的读者可能希望跳到第 805 页的"Virtual INTx Signaling"，以了解 PCIe 如何模拟此旧式模型，或者跳到第 812 页的"The MSI Model"以了解该方法。

使用中断的 PCI 设备有两种选择。它们可以使用：

- 原始规范中定义的、可共享的 INTx# 低电平有效信号。

- 随规范 2.2 版添加为可选项的消息信号中断。MSI 无需修改即可在 PCIe 系统中使用。

## **设备 INTx# 引脚**

PCI 设备最多可以实现 4 个 INTx# 信号（INTA#、INTB#、INTC# 和 INTD#）。提供多个引脚是因为 PCI 设备最多可以支持 8 个功能，每个功能允许驱动一个（但只有一个）中断引脚。在开发 PCI 时，典型系统使用包含 15 输入 8259 PIC 的芯片组，因此系统可用的 IRQ 数量（映射到中断向量）就是那么多。但是，其中许多已被用于系统用途，如系统计时器、键盘中断、鼠标中断等。此外，某些引脚是为仍可插入这些较旧系统的 ISA 卡保留的。因此，PCI 规范编写者认为只有四个 IRQ 可以可靠地用于其新总线，因此规范仅支持四个中断引脚。但是，您可能知道，PCI 总线上通常有四个以上的 PCI 设备，甚至单个设备内部可以有四个以上的功能，每个都需要自己的中断。

**800**

**第 17 章：中断支持**

这些原因就是 PCI 中断被设计为电平敏感和可共享的原因。这些信号可以简单地线或在一起以获得少量结果输出，每个输出表示中断请求。由于它们是共享的，因此当检测到中断时，中断处理程序软件将需要遍历共享同一引脚的 Function 列表，并测试哪些需要服务。

## **确定 INTx# 引脚支持**

PCI Function 在其配置头中指示对 INTx# 信号的支持。图 17-5 中所示的只读中断引脚寄存器指示此 Function 是否支持 INTx#，如果是，将在请求中断时断言哪个中断引脚。

_Figure 17-5: Interrupt Registers in PCI Configuration Header_

**==> picture [284 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 2 Byte1 0 DW<br>
Device Vendor 00<br>
ID ID<br>
Status Command 01<br>
Register Register<br>
Class Code Revision 02<br>
ID<br>
BIST HeaderType LatencyTimer CacheLineSize 03 00h = IRQ0<br>
04 01h = IRQ1<br>
Base Address 0<br>
Base Address 1 05 RW 02h = IRQ2<br>
03h = IRQ3<br>
06 access<br>
Base Address 2 04h = IRQ4<br>
Base Address 3 07 05h = IRQ5<br>
08 :<br>
Base Address 4 :<br>
:<br>
09<br>
Base Address 5 FEh = IRQ254<br>
10<br>
CardBus CIS Pointer FFh = IRQ255<br>
Subsystem ID SubsystemVendor ID 11<br>
Expansion ROM 12<br>
Base Address<br>
Reserved CapabilitiesPointer 13 RO 00h = No INTx# pin used<br>
Reserved 14 access 01h = INTA#<br>
Max_Lat Min_Gnt InterruptPin InterruptLine 15 02h = INTB#03h = INTC#<br>
04h = INTD#<br>
**----- End of picture text -----**<br>


**801**

**PCI Ex ress 3.0 Technolo p gy**

## **中断路由**

图 17-5（第 801 页）中所示的中断行寄存器提供了驱动程序需要了解的下一个信息：该设备的引脚已连接到的 PIC 的输入引脚。PIC 由系统软件编程，每个输入引脚（IRQ）具有唯一的向量号。所断言的最高优先级中断的向量被报告给处理器，然后处理器使用该向量索引到中断向量表中的相应条目。此条目指向中断设备的 ISR，处理器将执行它。

平台设计人员分配 INTx# 引脚来自设备的路由。它们可以以各种方式路由，但最终每个 INTx# 引脚都连接到中断控制器的输入。第 803 页的图 17-6 示出了一个示例，其中多个 PCI 设备中断通过可编程路由器连接到中断控制器。连接到给定可编程路由器输入的所有信号将被定向到中断控制器的特定输入。由平台软件（通常为固件）将其中断路由到公共中断控制器输入的 Function 将具有相同的中断行编号分配给它们。在此示例中，IRQ15 上连接了来自不同设备的三个 PCI INTx# 输入。因此，使用这些 INTx# 线的 Function 将共享 IRQ15，因此它们都会导致控制器在被查询时发送相同的向量。该向量将具有链接在一起的不同 Function 的三个 ISR。

## **将 INTx# 线关联到 IRQ 编号**

根据系统要求，对路由器进行编程以将其四个输入连接到四个可用的 PIC 输入。完成此操作后，与每个 Function 关联的 INTx# 引脚的路由是已知的，并且中断行号由软件写入每个 Function。该值最终由 Function 的设备驱动程序读取，以便知道已为其分配了哪个中断表条目。那就是将写入其 ISR 的起始地址的位置，此过程称为"挂接中断"。当此 Function 稍后生成中断时，CPU 将接收与中断行寄存器中指定的 IRQ 对应的向量号。CPU 使用此向量索引到中断向量表中，以获取与 Function 设备驱动程序关联的中断服务例程的入口点。

**802**

**第 17 章：中断支持**

_Figure 17-6: INTx Signal Routing is Platform Specific_

**==> picture [371 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTA#<br>
INTA#<br>
INTB# ISA<br>
Slave<br>
Programmable 8259A<br>
Interrupt<br>
Interrupt<br>
Router<br>
Controller<br>
INTA#<br>
IRQ8<br>
IRQ9 (IRQ2)<br>
IRQ10<br>
INTA# IRQ11<br>
INTB# IRQ12 ISA<br>
INTC# Input 0# IRQ13 Master<br>
INTD# InInput 2#put 1# IRQ14 IRQ15 Interrupt8259A<br>
Controller<br>
INTA# Input 3#<br>
IRQ0<br>
IRQ1<br>
Interrupt<br>
to CPU<br>
INTA# IRQ3<br>
INTB# IRQ4<br>
IRQ5<br>
IRQ6<br>
IRQ7<br>
INTA#<br>
**----- End of picture text -----**<br>


## **INTx# 信令**

INTx# 线是低电平有效信号，作为漏极开路实现，由系统在线上提供上拉电阻。连接到同一 PCI 中断请求信号线的多个设备可以同时断言它而不会损坏。

当 Function 发出中断信号时，它还会设置配置头的状态寄存器中的中断状态位。该位可由系统软件读取以查看当前是否有中断挂起。（参见第 805 页的图 17-8。）

**中断禁用。** 2.3 PCI 规范将中断禁用位（第 10 位）添加到配置头的命令寄存器中。参见第 804 页的图 17-7。该位在复位时清零，允许 INTx# 信号生成，但软件可以设置它

**803**

**PCI Ex ress 3.0 Technolo p gy**

以防止这种情况。注意，中断禁用位对消息信号中断 (MSI) 没有影响。MSI 通过 MSI 能力结构中的命令寄存器启用。启用 MSI 自动具有禁用中断引脚或仿真的效果。

**中断状态。** PCI 2.3 规范将一个只读中断状态位添加到配置状态寄存器中（如图 17-8（第 805 页）所示）。Function 在中断挂起时必须设置此状态位。此外，如果配置头的命令寄存器中的中断禁用位被清零（即中断已启用），则当此状态位被设置时，Function 的 INTx# 信号被断言。此位不受中断禁用位状态的影响。

_Figure 17-7: Configuration Command Register — Interrupt Disable Field_

**==> picture [316 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 11 10 9 8 7 6 5 4 3 2 1 0<br>
Reserved R<br>
Interrupt Disable, was Reserved<br>
Fast Back-to-Back Enable<br>
SERR# Enable<br>
Reserved, was Stepping Control<br>
Parity Error Response<br>
VGA Palette Snoop Enable<br>
Memory Write and Invalidate Enable<br>
Special Cycles<br>
Bus Master<br>
Memory Space<br>
IO Space<br>
**----- End of picture text -----**<br>


**804**

**第 17 章：中断支持**

_Figure 17-8: Configuration Status Register — Interrupt Status Field_

**==> picture [342 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 8 7 6 5 4 3 2 0<br>
R Reserved<br>
Interrupt Status<br>
Capabilities List<br>
66MHz-Capable<br>
Reserved<br>
Fast Back-to-Back Capable<br>
Master Data Parity Error<br>
DEVSEL Timing<br>
Signalled Target-Abort<br>
Received Target-Abort<br>
Received Master-Abort<br>
Signalled System Error<br>
Detected Parity Error<br>
**----- End of picture text -----**<br>


## **虚拟 INTx 信令**

## **概述**

如果在 PCIe 拓扑中使用 MSI 不可能，则将使用 INTx 信令模型。以下是可能需要能够使用 INTx 消息的设备的两个示例：

**PCIe-to-(PCI or PCI-X) 桥** — 大多数 PCI 设备将使用 INTx# 引脚，因为 MSI 支持对它们是可选的。由于 PCIe 不支持边带中断信令，因此改用带内消息。中断控制器理解该消息并将中断请求传送到 CPU，其中将包括预编程的向量号。

**启动设备** — PC 系统通常在启动序列期间使用旧式中断模型，因为 MSI 通常需要操作系统级初始化。通常，引导至少需要三个子系统：到操作员的输出（例如视频）、来自操作员的输入（通常是键盘）以及可用于获取操作系统的设备（通常是硬盘驱动器）。参与初始化系统的 PCIe 设备称为"启动设备"。启动设备将使用旧式中断支持，直到加载操作系统和设备驱动程序，此后最好使用 MSI。

**805**

**PCI Ex ress 3.0 Technolo p gy**

## **虚拟 INTx 线传递**

图 17-9（第 806 页）说明了具有 PCIe 端点和 PCI Express-to-PCI 桥的系统。如果我们假设软件未在端点上启用 MSI，它将使用 INTx 消息传递中断请求。在此示例中，桥使用 INTx 消息传播来自所连接 PCI 设备的基于引脚的中断。可以看出，桥发送 INTB 消息以发出其来自 PCI 总线的 INTB# 输入的断言和取消断言信号。PCIe 端点显示使用仿真消息发出 INTA 信号。注意，INTx# 信令涉及两条消息：

- **Assert_INTx** 消息指示虚拟 INTx# 信号的高电平到低电平转换（从无效到有效）。

- **Deassert_INTx** 消息指示低电平到高电平转换。

当 Function 传递 Assert_INTx 消息时，它还会在配置状态寄存器中设置其中断状态位，就像它断言物理 INTx# 引脚一样（参见第 805 页的图 17-8）。

_Figure 17-9: Example of INTx Messages to Virtualize INTA#-INTD# Signal Transitions_

**==> picture [230 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
