Local Local<br>APIC APIC<br>CPU CPU<br>Memory<br>North Bridge<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>PCI Bus<br>Interrupt Controller<br>(IO APIC)<br>Device<br>**----- End of picture text -----**<br>


## **中断延迟**

从发出中断信号到软件服务设备的时间称为中断延迟。尽管有其优点，但与其他中断传递机制一样，MSI 不提供中断延迟保证。

## **MSI 可能导致错误**

由于 MSI 作为内存写事务传递，因此与 MSI 传递相关联的错误被处理为与任何其他内存写错误条件相同。有关 ECRC 错误的处理示例，请参见第 657 页的"ECRC Generation and Checking"。当然，令人担忧的是，如果错误导致 MSI 数据包未被识别，则处理器将看不到中断。如何处理这种情况不在 PCIe 规范的范围之内。

**829**

**PCI Ex ress 3.0 Technolo p gy**

## **一些 MSI 规则和建议**

1. 规范的目的是系统软件将为 Function 分配互斥的消息，并且每条消息在传递到处理器时都将转换为独占的中断。

2. 每个 Function 不允许多个 MSI 能力寄存器集。

3. 读取消息地址寄存器会产生未定义的结果。

4. 保留的寄存器和位是只读的，并在读取时始终返回零。

5. 系统软件可以修改消息控制寄存器位，但设备本身被禁止这样做。换句话说，不允许通过"后门"机制修改这些位。

6. 至少将一条消息分配给每个设备（假设软件支持并计划在系统中使用 MSI）。

7. 系统软件不得写入包含消息数据寄存器的双字的上半部。

8. 如果设备多次写入相同的消息，则只能保证这些消息中的一条被服务。如果必须全部服务，则设备在上一次消息被服务之前不得再次生成相同的消息。

9. 如果设备具有多条分配的消息，并且它写入一系列不同的消息，则保证所有这些消息都将被服务。

## **基本系统外设的特殊注意事项**

中断也可能源自嵌入式旧式硬件，例如 IO Controller Hub 或 Super IO 设备。此类系统中通常需要的一些典型旧式设备包括：

- 串行端口

- 并行端口

- 键盘和鼠标控制器

- 系统计时器

- IDE 控制器

这些设备通常需要到 PIC 或 IO APIC 的特定 IRQ 线，以允许旧式软件正确地与它们交互。

使用 INTx 消息不能保证设备将收到它们所需的 IRQ 分配。以下示例说明了将支持适当的旧式中断分配的系统。

**830**

**第 17 章：中断支持**

## **旧式系统示例**

图 17-23（第 831 页）显示了一个较旧的 PCI Express 系统，其中包含通过专有 Hub 链路连接到根复合体的 IO Controller Hub (ICH)。ICH 中嵌入的 IO APIC 在其输入处收到中断请求时可以生成 MSI。在这种实现中，软件可以将旧式向量号分配给每个输入，以确保将调用正确的旧式软件。

此方法的优点是现有硬件可用于支持 PCIe 平台的旧式要求。该系统还要求在引导序列期间配置 MSI 子系统以供使用。如图所示的示例消除了对 INTx 消息的需求，除非 PCIe 扩展设备包含 PCI Express-to-PCI Bridge。

_Figure 17-23: PCI Express System with PCI-Based IO Controller Hub_

**==> picture [361 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>
FSB<br>
PCI Express<br>
GFX<br>
PCI Express Root Complex DDR<br>
Links SDRAM<br>
Hub Link<br>
IDE<br>
CD HDD IO Controller Hub<br>
MSI<br>
USB 2.0 Interrupt 4 INTA# - INTD#<br>
Controller<br>
LPC (APIC) PCI - 33MHz<br>
1<br>
Serial Interrupts Timer<br>
S IEEE Slots<br>
IO AC'97 1394<br>
COM1 Link<br>
COM2<br>
Modem Audio Boot<br>
Codec Codec Ethernet ROM<br>
RouterInterrupt<br>
**----- End of picture text -----**<br>


**831**

**PCI Ex ress 3.0 Technolo p gy**

**832**

## _**18 系统复位**_

## **上一章**

上一章描述了 PCIe Function 可以生成中断的不同方式。旧的 PCI 模型使用引脚执行此操作，但在串行模型中边带信号是不可取的，因此带内 MSI（消息信号中断）机制的支持成为强制性要求。为了向后兼容软件，PCI INTx# 引脚操作仍然可以使用 PCIe INTx 消息进行模拟。PCI 旧式 INTx# 方法以及较新版本的 MSI/MSI-X 都进行了描述。

## **本章**

本章描述了为 PCIe 定义的四种类型的复位机制：冷复位、热复位、热复位和功能级复位。讨论了使用边带复位 PERST# 信号来生成系统复位，还讨论了用于生成热复位的带内 TS1。

## **下一章**

下一章描述了 PCI Express 热插拔模型。还为所有支持热插拔功能的设备和外形尺寸定义了标准使用模型。热插拔卡的电源也是一个问题，当在运行时向系统添加新卡时，重要的是要确保其电源需求不超过系统可以提供的能力。需要一种机制来查询和控制设备的电源要求，电源预算 (Power Budgeting) 提供了这一点。

## **系统复位的两类**

PCI Express 规范描述了四种类型的复位机制。其中三种是早期 PCIe 规范的一部分，现在统称为**常规复位 (Conventional Resets)**，其中两种称为基本复位 (Fundamental Resets)。第四类和方法（随 2.0 规范修订版添加）称为**功能级复位 (Function Level Reset)**。

**833**

**PCI Ex ress Technolo p gy**

## **常规复位**

## **基本复位**

基本复位由硬件处理，并复位整个设备，重新初始化每个状态机以及所有硬件逻辑、端口状态和配置寄存器。该规则的一个例外是一组被标识为"粘性"的配置寄存器字段，这意味着它们保留其内容，除非所有电源都被移除。这使它们对于诊断需要复位才能使 Link 再次工作的问题非常有用，因为错误状态在复位后仍然存在，并且之后可供软件使用。如果主电源被移除但 Vaux 可用，那也将保持粘性位，但如果主电源和 Vaux 都丢失，则粘性位将与其他所有位一起被复位。

基本复位将在系统范围复位时发生，但也可以针对各个设备执行。

定义了两种类型的基本复位：

- **冷复位 (Cold Reset)**：当设备的主电源打开时产生的。循环电源将导致冷复位。

- **热复位（可选）(Warm Reset)**：通过系统特定的方式触发而不关闭主电源。例如，系统电源状态的变化可用于启动此操作。生成热复位的方法未由规范定义，因此系统设计人员将选择如何完成此操作。

当发生基本复位时：

- 对于正电压，接收器终端必须满足 ZRX-HIGH-IMP-DC-POS 参数。在 2.5 GT/s 时，这不低于 10KΩ。在更高的速度下，对于低于 200mv 的电压，它必须不低于 10KΩ，对于高于 200mv 的电压，必须为 20KΩ。这些是终端未通电时的值。

- 类似地，对于负电压，ZRX-HIGH-IMP-DC-NEG 参数在任何情况下都最小为 1KΩ。

- 发送器终端必须满足 Gen1 的 80 到 120Ω 以及 Gen2 和 Gen3 的最大 120Ω 的输出阻抗 ZTX-DIFF-DC，但可以将驱动器置于高阻抗状态。

- 发送器将直流共模电压保持在 0 到 3.6V 之间。

**834**

**Cha ter 18: S stem Reset p y**

当退出基本复位时：

- 当接收器终端启用时，接收器单端终端必须存在，以便接收器检测正常工作（Gen1 和 Gen2 为 40-60Ω，Gen3 为 50Ω±20%）。进入 Detect 时，共模阻抗必须在 50Ω±20% 的适当范围内。

- 必须在基本复位退出后 5ms 内重新启用其接收器终端 ZRX-DIFF-DC 的 100Ω，使其在训练期间可被邻居的发送器检测到。

- 发送器将直流共模电压保持在 0 到 3.6V 之间。

定义了两种传送基本复位的方法。首先，可以使用称为 PERST#（PCI Express 复位）的辅助边带信号来发信号。其次，当 PERST# 未提供给插卡或组件时，组件或插卡在电源循环时会自主生成基本复位。

## **PERST# 基本复位生成**

PCI Express 系统中的中央资源设备（例如芯片组）提供此复位。例如，第 836 页的图 18-1 中的 IO Controller Hub (ICH) 芯片可以根据系统电源的 POWERGOOD 信号的状态生成 PERST#，因为这指示主电源已打开并稳定。如果电源循环关闭，则 POWERGOOD 切换并导致 PERST# 断言和取消断言，从而导致冷复位。系统还可以提供通过其他方式切换 PERST# 的方法以实现热复位。

PERST# 信号馈送到主板上的所有 PCI Express 设备，包括连接器和图形控制器。设备可以选择使用 PERST#，但不是必需的。PERST# 还馈送到图中所示的 PCIe-to-PCI-X 桥。桥始终将其主（上游）总线上的复位转发到其辅助（下游）总线，因此 PCI-X 总线看到 RST# 被断言。

## **自主复位生成**

设备必须设计为在施加主电源时在硬件中生成自己的复位。规范未描述如何完成此操作，因此自复位机制可以内置到设备中或作为外部逻辑添加。例如，检测到上电的插卡可以使用该事件为其设备生成本地复位。如果设备检测到其电源超出指定限制，则还必须生成自主复位。

**835**

**PCI Ex ress Technolo p gy**

## **从 L2 低功耗状态唤醒链路**

作为需要自主复位的示例，其主电源已作为电源管理策略的一部分被关闭的设备如果被设计为发出唤醒信号，则可能能够请求恢复到全功率。当电源恢复时，必须对设备进行复位。系统的电源控制器可以向设备断言 PERST# 引脚，如图 18-1（第 836 页）所示，但如果它没有这样做，或者如果设备不支持 PERST#，则设备必须在感知到主电源重新施加时自主生成自己的基本复位。

_Figure 18-1: PERST# Generation_

**==> picture [299 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>
FSB<br>
GFX Root Complex<br>
DDR<br>
PCI Express SDRAM<br>
GFX<br>
PCI Express<br>
POWERGOOD PRST#<br>
PCI<br>
IO Controller Hub<br>
(ICH) IEEE<br>
1394<br>
PERST#<br>
Add-In Add-In<br>
Switch<br>
PCI Express<br>
PCI Express Link<br>
SCSI<br>
to-PCI-X<br>
PRST#<br>
PCI-X<br>
Gigabit<br>
Ethernet<br>
**----- End of picture text -----**<br>


**836**
