**==> 图片 [379 x 417] 已省略 <==**

**----- Start of picture text -----**<br>
AER Capability Structure<br>Extended Capability Header<br>00 01 00 01<br>Uncorrectable Error Status<br>00 00 00 00<br>Uncorrectable Error Mask<br>00 06 20 11<br>Uncorrectable Error Severity<br>Correctable Error Status00 00 20 00 CPU<br>00 00 20 00<br>Correctable Error Mask<br>00 00 00 06<br>Advanced Error Capability and Control00 00 00 00 Root Complex MemorySystem<br>Header Log - 1st DW00 00 00 00 P2P (DRAM)<br>Header Log - 2nd DW 0:28:0<br>00 00 00 00<br>Header Log - 3rd DW<br>00 00 00 00<br>Header Log - 4th DW<br>00 00 00 00<br>Root Error Command 2:0:0<br>00 00 00 06 Switch<br>Root Error Status P2P AER Capability Structure<br>08 00 00 7C<br>Error Source ID Extended Capability Header<br>05 00 00 00 14 01 00 01<br>3:0:0 3:5:0 Uncorrectable Error Status<br>00 04 10 00<br>Uncorrectable Error Mask<br>AER Capability Structure 00 00 00 00<br>Uncorrectable Error Severity<br>Extended Capability Header 00 06 20 11<br>14 01 00 01 Correctable Error Status<br>Uncorrectable Error Status 00 00 00 01<br>00 10 80 00 Correctable Error Mask<br>Uncorrectable Error Mask 4:0:0 5:0:0 00 00 20 00<br>00 00 00 00 Advanced Error Capability and Control<br>Uncorrectable Error Severity 00 00 00 12<br>00 16 20 11 PCIe PCIe Header Log - 1st DW<br>Correctable Error Status 60 00 80 80<br>00 00 00 40 Endpoint Endpoint Header Log - 2nd DW<br>Correctable Error Mask 00 00 04 FF<br>00 00 20 00 Header Log - 3rd DW<br>Advanced Error Capability and Control FB 80 10 00<br>00 00 00 0F Header Log - 4th DW<br>Header Log - 1st DW 00 00 00 01<br>00 00 00 80<br>Header Log - 2nd DW<br>0A 00 0C FF<br>Header Log - 3rd DW<br>FB 80 10 00<br>Header Log - 4th DW<br>00 00 00 00<br>P2P P2P<br>**----- End of picture text -----**<br>


**701**

**PCI Ex ress Technolo p gy**

6. 现在错误处理程序知道 5:0:0 处的第一个不可纠正错误是 Malformed TLP，它可以检查 Header Log 寄存器以查看格式错误的数据包的标头，因为这是记录标头的错误之一。在读取 Header Log 寄存器时，它找到以下四个双字：

   - 6000_8080h — 1st DW

   - 0000_04FFh — 2nd DW

   - FB80_1000h — 3rd DW

   - 0000_0001h — 4th DW

7. 对这 4 个 DW 的评估将格式错误的数据包标识为：Memory Write，4DW 标头，TC=0，TD=1，EP=0，Attr=0，AT=0，Length=80h（128 DW 或 512 字节），Requester ID=0:0:0，Tag=4，Byte Enables=FFh，Address=1_FB80_1000h。数据包的标头看起来都是正确的，并且每个字段都使用有效的编码，因此软件必须深入挖掘以发现为什么它被视为 Malformed TLP。在本例中，假设在进一步检查 5:0:0 上的配置空间后，软件发现为此函数启用的 Max Payload Size 为 256 字节，但此数据包包含 512 字节。这是目标设备（在本例中为 5:0:0）将视为 Malformed TLP 的情况。

如果您想验证您对此错误调查过程的了解，请继续评估在 4:0:0 上检测到的第一个不可纠正错误是什么。

如果您喜欢冒险并希望在真实系统（例如您的台式机或笔记本电脑）上检查此类信息，您可以通过下载 MindShare Arbor 软件（www.mindshare.com/arbor）来执行此操作。您可以在基于 x86 的计算机上运行它，它将扫描您的系统并显示每个可见的 PCI 兼容设备，并解码其配置空间以方便解释。

**702**

## _**16 电源管理 (Power Management)**_

## **上一章 (The Previous Chapter)**

上一章讨论了 PCIe 端口或链路上发生的错误类型、如何检测、报告以及处理它们的选项。由于 PCIe 旨在与 PCI 错误报告向后兼容，因此 PCI 错误处理方法作为背景信息也包含在内。然后我们重点介绍了 PCIe 对可纠正、非致命和致命错误的错误处理。

## **本章 (This Chapter)**

本章提供了系统电源管理讨论的整体背景以及 PCIe 电源管理的详细描述，该管理兼容 _PCI Bus PM Interface Spec_ 和 _Advanced Configuration and Power Interface_ (ACPI)。PCIe 定义了对 PCI-PM 规范的扩展，主要侧重于链路电源和事件管理。还提供了 OnNow 计划、ACPI 和 Windows 操作系统参与的概述。

## **下一章 (The Next Chapter)**

下一章详细介绍了 PCIe 函数生成中断的不同方式。旧的 PCI 模型使用引脚执行此操作，但在串行模型中边带信号是不希望的，因此支持带内 MSI (Message-Signaled Interrupts) 机制是强制性的。PCI INTx# 引脚操作仍可被仿真以支持使用 PCIe INTx 消息的传统系统。PCI 旧版 INTx# 方法和较新版本的 MSI/MSI-X 都被描述。

**703**

**PCI Ex ress Technolo p gy**

## **介绍 (Introduction)**

PCI Express 电源管理 (PM) 定义了四个主要支持领域：

- **PCI 兼容 PM** . PCIe 电源管理与 PCI-PM 和 ACPI 规范在硬件和软件上兼容。此支持要求所有函数都包含 PCI Power Management Capability 寄存器，允许软件通过使用 Configuration 请求在软件控制下在 PM 状态之间转换函数。这在 2.1 规范版本中通过添加 Dynamic Power Allocation (DPA) 进行了修改，这是另一组寄存器，为 D0 电源状态添加了几个子状态，为软件提供了更细粒度的 PM 机制。

- **Native PCIe Extensions** . 这些定义了链路的自主、基于硬件的活动状态电源管理 (ASPM)，以及唤醒系统的机制、报告电源管理事件 (PME) 的消息事务，以及计算和报告低功耗到活动状态延迟的方法。

- **Bandwidth Management.** 2.1 规范版本增加了硬件自动改变链路宽度或链路数据速率或两者兼而有之的能力以改善功耗。这允许在需要时实现高性能，并在性能较低可接受时保持低功耗使用。即使带宽管理被视为电源管理主题，我们也会在"链路初始化与训练"章节的第 618 页的"动态带宽变化"部分中描述此功能，因为它涉及 LTSSM。

- **Event Timing Optimization.** 外围设备发起总线主事件或中断而不考虑系统电源状态会导致其他系统组件保持高功率状态以为它们提供服务，从而导致功耗高于必要的水平。这种缺陷在 2.1 规范中通过添加两种新机制得到了纠正：Optimized Buffer Flush and Fill (OBFF)，它允许系统通知外围设备当前的系统电源状态；以及 Latency Tolerance Reporting (LTR)，它允许设备报告它们此时可以容忍的服务延迟。

本章分为几个主要部分：

1. 第一部分是关于电源管理的入门知识，并涵盖了系统软件在控制电源管理功能方面的作用。本讨论仅考虑 Windows 操作系统的观点，因为它是 PC 最常见的观点，不描述其他操作系统。

**704**

**第 16 章：电源管理**

2. 第二部分"函数电源管理"在第 713 页讨论了使用 PCI-PM 能力寄存器将函数置于其低功耗设备状态的方法。请注意，某些寄存器定义被 PCIe 函数修改或未使用。

3. "活动状态电源管理 (ASPM)"在第 735 页描述了基于硬件的自主链路电源管理。软件确定要为环境启用哪个 ASPM 级别，可能通过读取将为该函数产生的恢复延迟值，但之后电源转换的时序由硬件控制。软件不控制转换，并且无法看到链路处于哪个电源状态。

4. "软件发起的链路电源管理"在第 760 页讨论了当软件更改设备的电源状态时强制执行的链路电源管理。

5. "链路唤醒协议和 PME 生成"在第 768 页描述了设备如何请求软件将它们返回到活动状态以便它们可以对事件进行服务。当设备的电源被移除时，如果要监视事件并向系统发出唤醒信号以恢复电源并重新激活链路，则必须存在辅助电源。

6. 最后，描述事件计时功能，包括 OBFF 和 LTR。

## **电源管理入门 (Power Management Primer)**

_PCI Bus PM Interface spec_ 描述了 PCIe 所需的电源管理寄存器。这些寄存器允许 OS 直接管理函数的电源环境。与其深入详细描述，不如让我们首先描述此功能在系统整体背景中的适用位置。

## **PCI PM 基础 (Basics of PCI PM)**

本节概述了 Windows OS 如何与其他主要软件和硬件元素交互以管理各个设备以及整个系统的功耗。表 16-1 在第 706 页介绍了此过程中涉及的主要元素，并提供了它们如何相互关联的非常基本的描述。值得注意的是，PCI 电源管理规范和 ACPI 规范都未规定操作系统使用的 PM 策略。但是，它们确实定义了用于控制函数功耗的寄存器（以及一些数据结构）。

**705**

## **PCI Ex ress Technolo p gy**

_表 16-1：PC PM 中涉及的主要软件/硬件元素_

|**元素**|**职责**|
|---|---|
|OS|通过向 ACPI 驱动程序、设备驱动程序和 PCI Express 总线驱动程序发送请求来**指导整体系统电源管理**。具有节能意识的应用与 OS 交互以完成设备电源管理。|
|ACPI Driver|管理不遵守行业标准规范的嵌入式系统设备的配置、电源管理和热控制。这方面的示例包括芯片组特定寄存器、系统板特定寄存器以控制电源平面等。PCIe 函数（嵌入式或其他）中的 PM 寄存器由 PCI PM 规范定义，因此不由 ACPI 驱动程序管理，而是由 PCI Express Bus Driver 管理（请参见此表中的条目）。|
