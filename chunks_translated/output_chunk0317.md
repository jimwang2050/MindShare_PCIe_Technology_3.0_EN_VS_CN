## **ACPI 驱动程序控制非标准嵌入式设备 (ACPI Driver Controls Non-Standard Embedded Devices)**

系统板上嵌入了寄存器集不遵守任何特定行业标准规范的设备。启动时，BIOS 通过 **ACPI tables**（也称为 **namespace**）向 OS 报告这些设备。当 OS 需要与这些设备中的任何一个通信时，它会调用 ACPI Driver，该 Driver 执行与设备关联的称为 **Control Method** 的处理程序。该处理程序也在 ACPI 表中找到，并由平台设计者使用称为 ACPI Source Language 或 **ASL** 的特殊解释性语言编写。然后将 ASL 代码编译为 ACPI Machine Language 或 **AML**。请注意，AML 不是特定于处理器的机器语言。它是 ASL 源代码的标记化（即压缩）版本。ACPI Driver 包含一个 AML 标记解释器，允许它"执行"Control Method。

_图 16-1：OS、设备驱动程序、总线驱动程序、PCI Express 寄存器和 ACPI 之间的关系_

**==> 图片 [348 x 236] 已省略 <==**

**----- Start of picture text -----**<br>
Microsoft<br>OS<br>Interface defined  Interface defined<br>by Microsoft by Microsoft<br>Windows ACPI Written by Microsoft<br>Device Driver Driver to ACPI spec<br>Interface defined<br>by Microsoft<br>Written by Microsoft PCIe Bus AML Control Written by system<br>to OS, PCIe, and PCI  Driver Method board designer to ACPI<br>PM specs and chip-specific specs<br>Non-standard<br>PCIe Function's  PCIe Function's  Embedded Register set defined<br>Configuration PM Registers System Board by chip designer<br>Registers Device<br>Register set defined Register set defined<br>by PCIe spec by PCI PM spec and<br>extensions for PCIe<br>**----- End of picture text -----**<br>


**712**

**第 16 章：电源管理**

## **函数电源管理 (Function Power Management)**

PCI Express 函数需要支持电源管理，并且必须实现多个寄存器和相关位字段，如下所述。

## **PM Capability 寄存器集 (The PM Capability Register Set)**

PCI-PM 规范定义了 Power Management Capability 配置寄存器。这些寄存器对于 PCI 是可选的，但对于 PCIe 是必需的，并且位于 PCI 兼容配置空间中，Capability ID 为 01h。软件可以执行以下序列来定位这些寄存器：

1. 函数的 **Configuration Status 寄存器**的位 4 应被设置，指示函数配置头的 dword 13d 第一个字节中的 Capabilities Pointer 有效。读取 **Capabilities Pointer 寄存器**会得到函数的链表能力寄存器的第一个偏移量。

2. 如果该偏移处的 dword 的最低有效字节包含 **Capability ID 01h**（请参见第 713 页的图 16-2），则这是 PM 寄存器集。紧跟 Capability ID 字节之后的字节是 _Pointer to Next Capability_ 字段，它给出配置空间中下一个 Capability 的偏移量（如果有）。非零值是有效指针，而值 00h 指示链表的结束。所有 PM 寄存器的描述可在第 724 页的"PCI-PM 寄存器的详细描述"中找到。

_图 16-2：PCI Power Management Capability 寄存器集_

**==> 图片 [367 x 62] 已省略 <==**

**----- Start of picture text -----**<br>
31 16 15 8 7 0<br>Power Management Capabilities Pointer to Capability ID<br>(PMC) Next Capability 01h 1st Dword<br>Bridge Support<br>Data Register Extensions Control/Status Register 2nd Dword<br>(PMCSR_BSE) (PMCSR)<br>**----- End of picture text -----**<br>


## **设备 PM 状态 (Device PM States)**

每个 PCI Express 函数必须支持全开 D0 状态和全关 D3 状态，而 D1 和 D2 是可选的。以下各节描述了可能的 PM 状态。

**713**

**PCI Ex ress Technolo p gy**

## **D0 状态 — 全开 (D0 State—Full On)**

**Mandatory.** 在这种状态下，没有节能效果，设备完全运行。所有 PCIe 函数必须支持 D0 状态，从技术上讲有两个子状态：D0 Uninitialized 和 D0 Active。ASPM 硬件控制可以在设备处于此状态时更改链路电源。表 16-5 在第 714 页总结了 D0 状态下的 PM 策略。

**D0 Uninitialized.** 函数在基本复位后或在某些情况下在软件将其从 D3hot 转换为 D0 时进入 D0 Uninitialized。通常，寄存器返回到其默认状态。在此状态下，函数表现出以下特征：

- 它仅响应配置事务。

- 其 Command 寄存器启用位都返回到其默认状态，意味着它无法发起事务或充当内存或 IO 事务的目标。

**D0 Active.** 一旦函数已被软件配置和启用，它就处于 D0 Active 状态并完全运行。

_表 16-5：D0 电源管理策略_

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers or**<br>**State that must**<br>**be valid**|**Power**|**Actions**<br>**permitted to**<br>**Function**|**Actions**<br>**permitted by**<br>**Function**|
|---|---|---|---|---|---|
|L0|D0 un-initialized|PME context **|< 10W|PCI Express<br>config transac-<br>tions.|None|
|L0<br>L0s (required)*<br>L1 (optional)*|D0 active|all|full|Any PCI<br>Express trans-<br>action.|Any transac-<br>tion, interrupt,<br>or PME. **|
|L2/L3|D0 active|N/A***||||



* Active State Power Management

- ** If PME supported in this state.

- *** This combination of Bus/Function PM states not allowed.

## **动态功率分配 (DPA, Dynamic Power Allocation)**

**Optional**. 基础规范的 2.1 版本添加了另一个可选功能，为 D0 定义了另外 32 个子状态并描述了它们的特征。这旨在促进设备驱动程序、操作系统和执行中应用之间关于电源管理的协商，部分原因是某些函数的设备驱动程序不能很好地处理 PM。该模型的一个优点是设备在技术上仍保持在 D0 状态，因此可以以降低的能力继续操作，而不是像 D1 或更低状态那样离线。

DPA 寄存器仅在设备电源状态处于 D0 时适用，并且不适用于状态 D1-D3。最多可以定义 32 个子状态，并且它们必须从零到最大值连续编号。子状态 0 是初始默认值，表示函数能够消耗的最大功率。软件不需要按顺序在子状态之间转换，甚至不需要等到先前的转换完成后再请求子状态的另一个更改。因此，当函数完成子状态更改时，它必须检查配置的子状态，并且如果它们不匹配，则它必须开始更改为配置的值。支持 DPA 的寄存器（如图 16-3 在第 715 页所示）位于增强配置空间中。

_图 16-3：动态功率分配寄存器_

**==> 图片 [265 x 155] 已省略 <==**

**----- Start of picture text -----**<br>
31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>DPA Capability Register 004h<br>DPA Latency Indicator Register 008h<br>DPA Control Register DPA Status Register 00Ch<br>010h<br>DPA Power Allocation Array<br>(Sized by number of substates)<br>Up to<br>02Ch<br>**----- End of picture text -----**<br>


DPA 能力寄存器（如图 16-4 在第 716 页所示）包含与子状态关联的多个有趣的值。Substate_Max 数指示描述了多少个子状态，并且数字必须从零连续递增到该值。给出了两个 Transition Latency Values，每个子状态将通过 Latency Indicator 寄存器与其中一个相关联；该寄存器包含每个可能子状态的一位；如果设置了该位，则使用 Transition Latency Value 1，否则使用 Value 0。延迟值给出从任何其他子状态转换到该子状态所需的最长时间。

**715**

**PCI Ex ress Technolo p gy**

子状态。延迟值乘以 Transition Latency Units 以毫秒为单位给出时间。类似地，Power Allocation Scale 值给出每个子状态中使用的功率的乘数，以瓦特表示。对于每个定义的子状态，DPA Power Allocation Array 中的 32 位字段描述了该状态下使用的功率。其中第一个位于偏移 010h，其余在后续 dwords 中实现。

_图 16-4：DPA Capability 寄存器_

**==> 图片 [311 x 104] 已省略 <==**

**----- Start of picture text -----**<br>
31 24  23 16  15 14  13  12  11  10   9 8   7        5   4                0<br>Xlcy1 Xlcy0 RsvdZ PAS RsvdZ RsvdZ Substate_Max<br>Transition Latency Value 0 All fields not reserved<br>are read-only<br>Transition Latency Value 1<br>Power Allocation Scale (PAS)<br>Transition Latency Unit (Tlunit)<br>**----- End of picture text -----**<br>


DPA Control 寄存器的低 5 位由软件写入以设置新的子状态，当前子状态可以从 Status 寄存器读取，如图 16-5 在第 716 页所示。请注意，Status 寄存器的位 8 指示是否已启用 DPA 子状态的使用，但它被标记为 RW1C（Read, Write 1 to Clear），这意味着软件可以清除此位但不能设置它。DPA 在复位后默认启用，如果软件不打算使用 DPA，则需要通过向该位写入 1 来禁用它。

_图 16-5：DPA Status 寄存器_

**==> 图片 [298 x 93] 已省略 <==**

**----- Start of picture text -----**<br>
15 9   8  7          5   4     0<br>RsvdZ RsvdZ<br>Substate Control Enabled (RW1C)<br>Substate status (RO)<br>**----- End of picture text -----**<br>


## **D1 状态 — 浅睡眠 (D1 State—Light Sleep)**

**Optional**. 在进入此状态之前，软件必须确保所有未完成的 non-posted 请求都已收到其相关的完成。这可以通过轮询 PCI Express Capability 块的 Device Status 寄存器中的 Transactions Pending 位来实现；当该位清零时，可以安全地进行。在这种轻节能状态下，函数不会发起请求，PME Messages 除外（如果已启用）。D1 状态的其他特征包括：

- 当设备进入 D1 状态时，链路被强制进入 L1 电源状态。

- 在此状态下接受配置和消息请求，但所有其他请求必须作为 Unsupported Requests 处理，并且所有完成可选择性地作为 Unexpected Completions 处理。

- 如果错误是由传入请求引起的并且启用了报告，则可以在此状态下发送 Error Message。如果发生不同类型的错误（例如 Completion timeout），则消息将不会发送，直到设备返回到 D0 状态。

- 函数可以重新激活链路并发送 PME 消息（如果支持并在此状态下已启用），以通知软件函数已发生需要恢复电源的事件。

- 函数可能在此状态下丢失其上下文。如果丢失并且设备支持 PME，则它必须至少在 D1 状态下维护其 PME 上下文（请参见第 710 页的"PME Context"）。

- 函数必须返回到 D0 Active PM 状态才能完全运行。

表 16-6 列出了 D1 状态下的 PM 策略。

_表 16-6：D1 电源管理策略_
