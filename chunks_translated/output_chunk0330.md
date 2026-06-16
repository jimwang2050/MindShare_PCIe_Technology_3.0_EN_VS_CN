_Figure 16-44: LTR ‐ Link Down Case_

**==> picture [121 x 75] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>
value<br>
Conglomerate  1200 ns115700 ns<br>
value<br>
Switch<br>
**----- End of picture text -----**<br>


**791**

**PCI Ex ress Technolo p gy**

**792**

## _**17 Interrupt Support**_

## **上一章**

上一章提供了系统电源管理讨论的整体背景以及对 PCIe 电源管理的详细描述，电源管理与 _PCI Bus PM Interface Spec_ 以及 _Advanced Configuration and Power Interface_ (ACPI) 规范兼容。PCIe 定义了对 PCI-PM 规范的扩展，主要集中在链路电源和事件管理上。还提供了对 OnNow 计划、ACPI 以及 Windows 操作系统参与的概述。

## **本章**

本章描述 PCIe Function 可以生成中断的不同方式。旧的 PCI 模型使用引脚执行此操作，但在串行模型中边带信号是不可取的，因此带内 MSI（消息信号中断）机制的支持成为强制性要求。为了向后兼容软件，PCI INTx# 引脚操作仍然可以使用 PCIe INTx 消息进行模拟。PCI 旧式 INTx# 方法以及较新版本的 MSI/MSI-X 都进行了描述。

## **下一章**

下一章描述了为 PCIe 定义的三种类型的复位：基本复位（包括冷复位和热复位）、热复位和功能级复位 (FLR)。讨论了使用边带复位 PERST# 信号来生成系统复位，还讨论了描述的基于带内 TS1 的热复位。

**793**

**PCI Ex ress 3.0 Technolo p gy**

## **中断支持背景**

## **概述**

PCI 体系结构支持来自外围设备的中断，作为提高其性能并减轻 CPU 必须轮询设备以确定何时需要服务的负担的一种手段。PCIe 在很大程度上从 PCI 继承了这种支持，允许软件向后兼容 PCI。我们在本章中提供有关系统中断处理的背景，但希望了解更多中断详细信息的读者鼓励查阅以下参考资料：

- 有关 PCI 中断的背景，请参阅 PCI 规范 3.0 版或 MindShare 教材的第 14 章：PCI System Architecture（www.mindshare.com）。

- 要了解有关 Local 和 IO APIC 的更多信息，请参阅 MindShare 教材：x86 Instruction Set Architecture。

## **两种中断传递方法**

PCI 使用路由到中央中断控制器的边带中断线。这种方法在简单的单 CPU 系统中运行良好，但存在一些缺点，这些缺点促使转移到一种称为 MSI（消息信号中断）的新方法，并带有一个称为 MSI-X（扩展）的扩展。

**旧式 PCI 中断传递** — 这种最初为 PCI 总线定义的机制由每个设备的最多四个信号或 INTx#（INTA#、INTB#、INTC# 和 INTD#）组成，如图 17-1（第 795 页）所示。在此模型中，引脚通过线或连接共享，它们最终将连接到 8259 PIC（可编程中断控制器）上的输入。当一个引脚被断言时，PIC 依次断言其到 CPU 的中断请求引脚，作为第 796 页"旧式模型"中描述的过程的一部分。

PCIe 支持此 PCI 中断功能以实现向后兼容性，但串行传输的设计目标是最小化引脚数。结果，INTx# 信号未作为边带引脚实现。相反，Function 可以生成带内中断消息数据包以指示引脚的断言或取消断言。这些消息充当"虚拟线路"，并以系统中的中断控制器（通常在根复合体中）为目标，如图 17-2（第 796 页）所示。该图还说明了使用

**794**

**第 17 章：中断支持**

引脚的旧 PCI 设备如何在 PCIe 系统中工作；桥将引脚的断言转换为向上游到根复合体的中断仿真消息 (INTx)。预期 PCIe 设备通常不需要使用 INTx 消息，但在撰写本文时，实际上它们经常这样做，因为尚未更新系统软件以支持 MSI。

_Figure 17-1: PCI Interrupt Delivery_

**— MSI 中断传递** MSI 通过使用内存写入来传递中断通知，从而消除了对边带信号的需要。术语"消息信号中断"可能会造成混淆，因为其名称中包含术语"消息"，这是 PCIe 中的 TLP 类型，但 MSI 中断是 Posted 内存写入而不是消息事务。MSI 内存写入仅通过它们寻址的目标地址与其他内存写入区分开，该地址通常由系统保留用于中断传递（例如，x86 基础系统传统上保留地址范围 FEEx_xxxxh 用于中断传递）。

图 17-2 说明了从各种类型的 PCIe 设备传递中断。所有 PCIe 设备都需要支持 MSI，但软件可能支持也可能不支持 MSI，在这种情况下，将使用 INTx 消息。图 17-2 还显示了 PCIe-to-PCI 桥如何需要将来自连接的 PCI 设备的边带中断转换为 PCIe 支持的 INTx 消息。

**795**

**PCI Ex ress 3.0 Technolo p gy**

_Figure 17-2: Interrupt Delivery Options in PCIe System_

**==> picture [370 x 274] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
Root Complex<br>
Memory<br>
Interrupt Controller<br>
INTx<br>
MSI or Message<br>
INTx Message<br>
PCIe<br>
Switch<br>
MSI or MSI or Bridge<br>
INTx Message INTx Message to PCI<br>
or PCI-X<br>
INTx#<br>
PCIe Legacy<br>
PCI/PCI-X<br>
Endpoint Endpoint<br>
**----- End of picture text -----**<br>


## **旧式模型**

## **概述**

为了说明旧式中断传递模型，请参考图 17-3（第 797 页）并考虑使用旧式中断引脚方法进行中断传递所涉及的常规步骤：

1. 设备通过向控制器断言其引脚来生成中断。在较旧的系统中，该控制器通常是具有 15 个 IRQ 输入和一个 INTR 输出的 Intel 8259 PIC。然后 PIC 将断言 INTR 以通知 CPU 一个或多个中断挂起。

**796**

**第 17 章：中断支持**

2. 一旦 CPU 检测到 INTR 的断言并准备好对其采取行动，它必须识别哪个中断实际需要服务，这是通过 CPU 在处理器总线上发出称为中断确认的特殊命令来完成的。

3. 该命令由系统路由到 PIC，PIC 返回一个称为中断向量的 8 位值，以报告当前挂起的最高优先级中断。每个 IRQ 输入的唯一向量先前已由系统软件编程。

4. 中断处理程序然后使用该向量作为中断表（由软件设置的区域，用于包含所有中断服务例程 ISR 的起始地址）中的偏移量，并获取在该位置找到的 ISR 起始地址。

5. 该地址将指向已设置为处理此中断的 ISR 的第一条指令。此处理程序将被执行，服务该中断并告诉其设备取消其 INTx# 线的断言，然后将控制权返回给先前被中断的任务。

_Figure 17-3: Legacy Interrupt Example_

**==> picture [304 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTR<br>
CPU Memory<br>
5<br>
Interrupt Service<br>
Interrupt<br>
Vector Routine (ISR)<br>
Acknowledge<br>
4<br>
North Bridge<br>
Interrupt Table (ISR<br>
starting addresses)<br>
PCI Bus<br>
Bridge<br>
Data Buffer<br>
South Bridge<br>
PCI Bus<br>
1<br>
Interrupt Controller<br>
(PIC) INTA#<br>
Device<br>
**----- End of picture text -----**<br>


**797**

**PCI Ex ress 3.0 Technolo p gy**

## **对多处理器的支持变更**

此模型在单 CPU 系统中运行良好，但有一个限制使其在多 CPU 系统中不是最优的。问题是 INTR 引脚只能连接到一个 CPU。如果存在多个处理器，则只有其中一个处理器将看到中断，并且必须为所有中断提供服务，而其他 CPU 看不到任何中断。为了获得最佳性能，此类系统实际上需要在所有处理器之间均匀分配系统任务，称为 SMP（对称多处理），但引脚模型不支持它。

为了实现更好的 SMP，需要一种新模型，为此，PIC 被修改为 IO APIC（高级可编程中断控制器）。IO APIC 被设计为具有一个称为 APIC 总线的单独小型总线，它可以通过该总线传递中断消息，如图 17-4（第 799 页）所示。在此模型中，消息包含中断向量号，因此不需要 CPU 将中断确认向下发送到 IO 世界以获取它。APIC 总线连接到处理器内称为本地 APIC 的新内部逻辑块。该总线在所有代理之间共享，任何代理都可以在其上发起消息，但出于我们的目的，有趣的部分是它用于来自外围设备的中断传递。现在可以通过软件静态分配这些中断以由不同的 CPU 服务、多个 CPU 服务，甚至可以由 IO APIC 动态分配。

**798**

**第 17 章：中断支持**

_Figure 17-4: APIC Model for Interrupt Delivery_

**==> picture [316 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Local Local<br>
APIC APIC<br>
CPU CPU<br>
Memory<br>
APIC<br>
bus North Bridge<br>
PCI Bus<br>
Bridge<br>
Write Buffer<br>
South Bridge<br>
PCI Bus<br>
Interrupt Controller<br>
(IO APIC) INTA#<br>
Device<br>
**----- End of picture text -----**<br>


该模型称为 APIC 模型，多年来已经足够使用，但仍然依赖于来自外围设备的边带引脚。该模型的另一个限制是到 IO APIC 的 IRQ（中断请求线）数量。如果没有大量的 IRQ，外围设备必须共享 IRQ，这意味着每当该 IRQ 被断言时都会增加延迟，因为可能有多个设备可以断言它，并且软件必须评估所有这些设备。这种将多个 ISR 链接在一起的技术通常称为中断链接 (interrupt chaining)。最终，由于这个问题和另外一些小问题，又出现了另一个改进。

为什么不让外围设备本身直接向本地 APIC 发送中断消息？所需的只是一种通信路径，它已经以 PCI 总线和处理器总线的形式存在。因此，APIC 总线被消除，所有中断都以内存写入的形式传递到本地 APIC，称为 MSI 或消息信号中断。这些 MSI 针对系统理解为针对本地 APIC 的中断消息的特殊地址。（此特殊地址是

**799**

**PCI Ex ress 3.0 Technolo p gy**

对于 x86 基础系统，传统上为 FEEx_xxxxh。）甚至 IO APIC 也被编程为使用内存写入 (MSI) 通过普通数据总线发送其中断通知。现在它只需通过数据总线发送针对所需处理器的本地 APIC 的内存地址的 MSI 内存写入，这具有通知处理器中断的效果。

该模型称为 xAPIC 模型，由于它不基于进入输入有限的中断控制器的边带信号，因此几乎消除了共享中断的需要。有关此模型的更多信息可以在第 827 页的"An MSI Solution"中找到。
