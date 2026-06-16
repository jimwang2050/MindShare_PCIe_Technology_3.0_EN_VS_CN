|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|
|---|---|---|---|
|**Power Management Capabilities**<br>**(PMC)**||**Pointer to**<br>**Next Capability**|**Capability ID**<br>**01h**|
|**Data Register**|**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Control/Status Register**<br>**(PMCSR)**||



## **PM Capabilities (PMC) 寄存器 (PM Capabilities (PMC) Register)**

此 16 位只读寄存器的字段在表 16-12 中描述。

**724**

**第 16 章：电源管理**

_表 16-12：PMC 寄存器位分配_

|**Bit(s)**|**Description**|
|---|---|
|31:27|**PME_Support** 字段。指示函数能够在哪些 PM 状态下发送 PME 消息。位中的零表示在相应 PM 状态下不支持 PME 通知。<br>**Bit**<br>  **对应于 PM 状态**<br>27                      D0<br>28                      D1<br>29                      D2<br>30                      D3hot<br>31                      D3cold（函数需要辅助电源用于 PME 逻辑和通过信标或 WAKE# 引脚的唤醒信令）<br>支持从 D3cold 唤醒的系统还必须支持辅助电源，并且必须使用它来发出唤醒信号。<br>对于在根和交换机端口中实现的虚拟 PCI-PCI 桥，必须将位 31、30 和 27 设置为 1b。这是转发 PME 消息的端口所必需的。|
|26|**D2_Support** 位。1 = 函数支持 D2 PM 状态。|
|25|**D1_Support** 位。1 = 函数支持 D1 PM 状态。|



**725**

## **PCI Ex ress Technolo p gy**

_表 16-12：PMC 寄存器位分配（续）_

|**Bit(s)**|**Description**|
|---|---|
|24:22|**Aux_Current** 字段。对于支持从 D3cold 状态生成 PME 消息的函数，此字段报告对函数的 3.3Vaux 电源（请参见第 775 页的"Auxiliary Power"）的当前需求（由保留 PME 上下文信息的函数逻辑提出）。此信息供软件用于确定可同时启用 PME 生成的函数数量（基于每个函数从系统 3.3Vaux 电源汲取的电流总量以及电源的供电能力）。<br>•<br>如果函数不支持从 D3cold PM 状态内进行 PME 通知，则此字段未实现并且在读取时始终返回零。或者，由 PCI Express 定义的新功能允许不支持 PME 的设备在 Device Control 寄存器中由 _Aux Power PM Enable_ 位启用时报告它们汲取的辅助电流。<br>•<br>如果函数实现 Data 寄存器（请参见第 731 页的"Data Register"），则此字段在读取时始终返回零。然后 Data 寄存器在报告函数的 3.3Vaux 电流要求时优先于此字段。<br>•<br>如果函数支持从 D3cold 状态进行 PME 通知并且不实现 Data 寄存器，则 Aux_Current 字段报告函数的 3.3Vaux 电流要求。编码如下：<br> **Bit**<br> **24 23 22                 最大所需电流**<br>1   1   1                                375mA<br>1   1   0                                320mA<br>1   0   1                                270mA<br>1   0   0                                220mA<br>0   1   1                                160mA<br>0   1   0                                100mA<br>0   0   1                                 55mA<br>0   0   0                                   0mA|



**726**

**第 16 章：电源管理**

_表 16-12：PMC 寄存器位分配（续）_

|**Bit(s)**|**Description**|
|---|---|
|21|**设备特定初始化 (DSI)** 位。此位中的 1 指示在进入 D0 Uninitialized 状态后立即，该函数需要超出其 PCI 配置标头寄存器设置的额外配置，然后 Class 驱动程序才能使用该函数。<br>Microsoft OS 不使用此位。而是由 Class 驱动程序进行确定和初始化。|
|20|保留。|
|19|**PME Clock** 位。不适用于 PCI Express。必须硬连线为 0。|
|18:16|**Version** 字段。此字段指示函数符合的 PCI Bus PM Interface 规范的版本。<br>**Bit**<br> **18 17 16       符合的规范版本**<br>0   0   1                             1.0<br>0   1   0                             1.1（PCI Express 所需）|



## **PM Control and Status Register (PMCSR)**

此寄存器是所有 PCI Express 设备所需的，具有多种用途，如下所述。表 16-13 在第 728 页提供了 PMCSR 位字段的描述。

- 如果函数实现 PME 功能，则 PME Enable 位允许软件启用或禁用函数断言 PME 消息或 WAKE# 信号的能力，Status 位反映是否已发生 PME。

- 如果实现了可选的 Data 寄存器（请参见第 731 页的"Data Register"），则使用两个字段允许软件选择可通过 Data 寄存器读取的信息，并提供 Data 寄存器值的缩放乘数。

- 可以读取寄存器的 PowerState 字段以确定函数的当前 PM 状态，并可以写入以将函数置于新的 PM 状态。

**727**

## **PCI Ex ress Technolo p gy**

_表 16-13：PM Control/Status Register (PMCSR) 位分配_

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|31:24|all<br>zeros|Read<br>Only|请参见第 731 页的"Data Register"。|
|23|zero|Read<br>Only|在 PCI Express 中未使用|
|22|zero|Read<br>Only|在 PCI Express 中未使用|
|21:16|all<br>zeros|Read<br>Only|保留|
|15|See<br>Descrip<br>tion.|Read,<br>Write<br>one to<br>clear,<br>Sticky<br>RW1CS|**PME_Status** 位。**Optional**：仅当函数支持 PME 通知时实现，否则为零。<br>此位反映函数是否已经历 PME（即使此寄存器中的 PME_En 位已禁用函数发送 PME 消息的能力）。如果设置为 1，则函数已经历 PME。软件通过向其写入 1 来清除此位。<br>复位后，如果函数不支持 D3cold 中的 PME，则此位为零。如果函数支持 D3cold 中的 PME，则此位在初始 OS 引导时是不确定的，但之后反映函数是否已经历 PME。<br>如果函数支持来自 D3cold 的 PME，则该位的状态必须保持不变，即使电源丢失或函数被复位（粘性位）。这意味着辅助电源在这些条件下保持该逻辑处于活动状态（请参见第 775 页的"Auxiliary Power"）。|



**728**

**第 16 章：电源管理**

_表 16-13：PM Control/Status Register (PMCSR) 位分配（续）_

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|14:13|Device-<br>specific|Read<br>Only|**Data_Scale** 字段。**Optional**。如果函数未实现 Data 寄存器，则此字段硬连线返回零。<br>如果实现了 Data 寄存器，则 Data_Scale 字段是必需的，并且必须是表示其乘数的只读值。Data_Scale 字段的值和解释取决于由 Data_Select 字段选择要通过 Data 寄存器查看的数据项。|
|12:9|0000b|Read/<br>Write|**Data_Select** 字段。**Optional**。如果函数未实现 Data 寄存器，则此字段硬连线返回零。<br>如果实现了 Data 寄存器，则 Data_Select 是必需的读/写字段。放置在此寄存器中的值选择要在 Data 寄存器中查看的数据。然后该值必须乘以从 Data_Scale 字段读取的值。|



**729**

## **PCI Ex ress Technolo p gy**

_表 16-13：PM Control/Status Register (PMCSR) 位分配（续）_

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|8|See<br>Descrip<br>tion.|Read/<br>Write|**PME_En** 位。**Optional**。<br>1 = 在事件发生时启用函数发送 PME 消息的能力。<br>0 = 禁用。<br>如果函数不支持从任何电源状态生成 PME，则此位在读取时始终返回零。<br>复位后，如果函数不支持来自 D3cold 的 PME，则此位为零。如果函数支持来自 D3cold 的 PME：<br>• 此位在初始 OS 引导时是不确定的。<br>• 否则，它启用或禁用函数在发生 PME 时是否可以发送 PME 消息。<br>如果函数支持来自 D3cold 的 PME，则该位的状态必须在函数保持在 D3cold 状态期间以及从 D3cold 转换为 D0 Uninitialized 状态期间保持不变。这意味着 PME 逻辑必须使用辅助电源在这些条件下为此逻辑供电。|
|7:2|all<br>zeros|Read<br>Only|保留|
|1:0|00b|Read/<br>Write|**PowerState** 字段。**Mandatory**。软件使用此字段读取函数的当前 PM 状态或写入新的 PM 状态。如果软件选择函数不支持的 PM 状态，则写入正常完成，但数据被丢弃且不发生状态更改。<br>  **1 0           PM 状态**<br>0 0                D0<br>0 1                D1<br>1 0                D2<br>1 1                D3hot|



**730**

**第 16 章：电源管理**

## **Data 寄存器 (Data Register)**

**Optional, read-only**。请参见第 732 页的图 16-8。Data 寄存器是一个 8 位只读寄存器，为软件提供以下信息：

- 在所选 PM 状态下消耗的功率；用于功率预算。

- 在所选 PM 状态下耗散的功率；用于管理热环境。

- 可以通过此寄存器报告任何类型的数据，但 PCI-PM 规范仅为其定义了功率消耗和功率耗散信息。

如果实现了 Data 寄存器，则还必须实现 PMCSR 寄存器的 Data_Select 和 Data_Scale 字段，并且不能实现 PMC 寄存器的 Aux_Current 字段。

**确定 Data 寄存器的存在 (Determining Presence of the Data Register).** 软件可以执行以下过程来检查 Data 寄存器的存在：

1. 将值 0000b 写入 PMCSR 寄存器的 Data_Select 字段。

2. 从 Data 寄存器或 PMCSR 寄存器的 Data_Scale 字段读取。非零值表示 Data 寄存器以及 PMCSR 寄存器的 Data_Scale 和 Data_Select 字段已实现。如果读取值为零，请转到步骤 4。
