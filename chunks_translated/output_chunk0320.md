3. 如果 Data_Select 字段的当前值是 1111b 以外的值，请转到步骤 4。如果 Data_Select 字段的当前值为 1111b，则所有可能的 Data 寄存器值都已被扫描并返回零，这表明 Data 寄存器和 PMCSR 寄存器的 Data_Scale 和 Data_Select 字段都未实现。

4. 增加 Data_Select 字段的内容并返回步骤 2。由于数据选择字段只有 4 位，因此完整的扫描需要测试 16 个可能的 select 值并查看是否看到数据和缩放寄存器的任何非零值。

**Data 寄存器的操作 (Operation of the Data Register).** 返回的信息通常是函数在最坏情况下的功率消耗和功率耗散特性在各 PM 状态下的静态副本（如设备数据表中列出）。要使用 Data 寄存器，程序员使用以下序列：

1. 将值写入 PMCSR 寄存器的 Data_Select 字段（请参见第 733 页的表 16-14），以选择要通过 Data 寄存器查看的数据项。

**731**

**PCI Ex ress Technolo p gy**

2. 从 Data 寄存器和 PMCSR 寄存器的 Data_Scale 字段读取数据值。

3. 将值乘以缩放因子。

**多功能设备 (Multi-Function Devices).** 在多功能 PCI Express 设备中，每个函数必须提供其自己的功率信息。所有函数通用逻辑的功率信息通过函数零的 Data 寄存器报告（请参见表 16-14 中第 733 页的 Data Select Value = 8）。

**虚拟 PCI-to-PCI 桥功率数据 (Virtual PCI-to-PCI Bridge Power Data).** 规范未指定根复合体或交换机中 PCI-to-PCI 桥函数中的数据字段使用。但是，为了保持 PCI-PM 兼容性，桥必须报告它们消耗的功率信息。软件可以在交换机的每个端口读取虚拟 PPB Data 寄存器，以确定交换机在每个电源状态消耗的功率。

_图 16-8：PM 寄存器_

|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|
|---|---|---|---|
|**Power Management Capabilities**<br>**(PMC)**||**Pointer to**<br>**Next Capability**|**Capability ID**<br>**01h**|
|**Data Register**|**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Control/Status Register**<br>**(PMCSR)**||



**732**

**第 16 章：电源管理**

_表 16-14：Data 寄存器解释_

|**Data Select Value**|**Data Reported in**<br>**Data Register**|**Interpretation of Data**<br>**Scale Field in PMCSR**|**Units/**<br>**Accuracy**|
|---|---|---|---|
|00h|D0 中消耗的功率|00b = 未知<br>01b = 乘以 0.1<br>10b = 乘以 0.01<br>11b = 乘以 0.001|Watts|
|01h|D1 中消耗的功率|||
|02h|D2 中消耗的功率|||
|03h|D3 中消耗的功率|||
|04h|D0 中耗散的功率|||
|05h|D1 中耗散的功率|||
|06h|D2 中耗散的功率|||
|07h|D3 中耗散的功率|||
|08h|在多功能 PCI 设备中，Function 0 指示包中所有函数通用逻辑消耗的功率。|||
|09h-0Fh|保留供多功能设备中 Function 0 将来使用。|保留|TBD|
|08h-0Fh|在单功能设备和多功能设备中 Function 0 以外的函数中保留。|||



## **链路电源管理介绍 (Introduction to Link Power Management)**

我们刚刚看到软件如何将设备置于多个设备电源状态之一，现在让我们考虑 PCIe 如何也管理链路电源。设备电源和链路电源相互关联，如表 16-15 在第 734 页所示。另请注意下游和上游设备之间的关系，可以总结为：上游设备或链路不能处于比其下方更具攻击性的节能状态。原因是为了

**733**

**PCI Ex ress Technolo p gy**

便于及时传送来自端点的数据包，如果上游设备处于较低功率状态，则其流量将被延迟。每个关系描述如下：

**D0** — 设备已完全通电，通常处于 L0 链路状态。在不离开此状态的情况下，通过使用 DPA 子状态（请参见第 714 页的"Dynamic Power Allocation (DPA)"），以及使用基于硬件的链路电源管理（请参见第 735 页的"Active State Power Management (ASPM)"了解更多详细信息），可以使用一些节能。

**D1 和 D2** — 当软件将设备状态更改为 D1 或 D2 时，链路必须自动转换为 L1 状态。由于两个链路伙伴都参与此操作，因此存在握手机制以确保有序地完成操作。

**D3hot** — 当软件将设备置于 D3 状态时，链路会自动转换为 L1，就像转换为 D1 和 D2 状态一样。现在软件可以选择移除参考时钟和电源，将设备置于 D3cold。但在此之前，预期系统将启动握手过程，通过将链路置于 L2/L3 Ready 状态来准备链路。

**D3cold** — 在这种状态下，主电源和参考时钟已关闭。但是，辅助电源 (VAUX) 可能可用，允许设备向系统发出唤醒事件。如果可用，链路状态将处于 L2。如果主电源被移除但 VAUX 不可用，则链路将处于 L3。表 16-16 在第 735 页提供了有关链路电源状态的更多信息。

_表 16-15：设备和链路电源状态之间的关系_

|**Downstream**<br>**Component D-State**|**Permissible Upstream**<br>**Component D-State**|**Permissible**<br>**Interconnect State**|
|---|---|---|
|D0|D0|L0, L0s & L1 (optional)|
|D1|D0-D1|L1|
|D2|D0-D2|L1|
|D3 hot|D0-D3 hot|L1, L2/L3 Ready|
|D3 cold|D0-D3 cold|L2 (AUX Pwr), L3|



**734**

**第 16 章：电源管理**

## _表 16-16：链路电源状态特性_

|**State**|**Description**|**Software**<br>**Directed?**|**Active**<br>**State**<br>**Link PM**|**Ref.**<br>**Clocks**|**Main**<br>**Power**|**PLL**|**Vaux**|
|---|---|---|---|---|---|---|---|
|L0|Fully Active|Yes (D0)|On|On|On|On|On/Off|
|L0s|Standby|No|Yes<br>(D0)|On|On|On|On/Off|
|L1|Low Power<br>Standby|Yes*<br>(D1-D3 hot)|Yes(option)<br>(D0)|On|On|On/Off|On/Off|
|L2/L3<br>Ready|Staging for<br>power<br>removal|Yes<br>PME_Turn_Off<br>handshake|No|On|On|On/Off|On/Off|
|L2|Low Power<br>Sleep|Yes**|No|Off|Off|Off|On|
|L3|Off<br>(Zero Power)|N/A|N/A|Off|Off|Off|Off|



- L1 状态是由于 PM 软件将设备置于 D1、D2 或 D3 状态或由 ASPM 下的硬件控制而进入的。

- ** 规范将 L2 状态描述为软件定向。表中的其他 L 状态被列为软件定向，因为软件启动到这些状态的转换。例如，当软件启动设备电源状态更改为 D1、D2 或 D3 时，设备必须通过进入 L1 状态来响应。然后软件通过发起 PME_Turn_Off 消息来启动到 L2/L3 Ready 状态的转换。最后，软件在设备已转换为 L2/L3 Ready 状态后启动从设备中移除电源。由于 Vaux 电源在 L2 中可用，因此可以发出唤醒事件以通知软件。

## **活动状态电源管理 (ASPM, Active State Power Management)**

ASPM 是一种基于硬件的链路节能机制，仅在设备处于 D0 设备电源状态时适用。进入和退出 ASPM 状态由硬件根据实现特定的标准发起；软件无法控制或观察此操作，只能使用配置寄存器位启用或禁用它（请参见第 744 页的图 16-15）。

**735**

**PCI Ex ress Technolo p gy**

为 ASPM 定义了两个低功耗状态：

1. L0s (standby state) — 此状态提供大量节能，但仍允许快速的进入和退出延迟。这主要是通过将发送器置于电气空闲条件来实现的。在早期规范版本中，对该状态的支持以前是所有 PCIe 设备所必需的，但在 3.0 规范中它变为可选的。

2. L1 ASPM — L1 的目标是在可接受较长进入和退出延迟的情况下实现比 L0s 更大的节能。例如，在此状态下，两个发送器同时进入电气空闲。在 3.0 规范中，对该状态的支持仍然是可选的，就像在早期规范中一样。

## **电气空闲 (Electrical Idle)**

由于将发送器置于电气空闲是 ASPM 的核心部分，因此讨论其工作方式将会有所帮助。当发送器的差分信号 (TxD+ 和 TxD-) 进入电气空闲条件时，它停止信号传输，并将其电压保持在非常接近共模电压的位置，差分电压为 0V。信号转换消耗功率，因此在链路上停止它们可以节省功率，同时仍允许在 L0 状态期间相当快地恢复正常链路活动。根据节能程度，链路处于 L0s 或 L1 状态。在此期间，发送器可以选择保持低阻抗状态或通过关闭其端接逻辑变为高阻抗以节省更多功率。除了 L0s 和 L1 之外，当链路已被禁用时，电气空闲也将生效。

## **发送器进入电气空闲 (Transmitter Entry to Electrical Idle)**

希望进入电气空闲条件的发送器必须首先通知链路伙伴，以便缺乏进一步的信号不会被误解为错误。它们通过发送 EIOS (Electrical Idle Ordered-Set) 然后快速停止传输并将链路输出驱动器置于三态来执行此操作。EIOS 的外观取决于正在使用的编码方法，如以下各节所述。发送最后一个 EIOS 后，发送器必须在 8ns 内进入电气空闲并保持至少 20ns，无论数据速率如何。电气空闲期间允许的差分峰值电压必须在 0 和 20mV 峰值之间，无论数据速率如何，以减少接收器将线路上的噪声误解为有效信号的机会。（有关这些时序和电压参数的更多信息，请参见第 489 页的表 13-3。）

**736**

**第 16 章：电源管理**

**Gen1/Gen2 模式编码 (Gen1/Gen2 Mode Encoding).** 对于 Gen1/Gen2 模式，EIOS 形式如图 16-9 在第 737 页所示。必须发送所有四个符号，但接收器仅需要看到两个 IDL 控制字符即可识别此条件。

_图 16-9：Gen1/Gen2 模式 EIOS 模式_

**==> 图片 [134 x 100] 已省略 <==**

**----- Start of picture text -----**<br>
Encoding<br>COM K28.5<br>IDL K28.3<br>IDL K28.3<br>IDL K28.3<br>**----- End of picture text -----**<br>

