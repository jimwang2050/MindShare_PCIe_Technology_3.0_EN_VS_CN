PCIe 规范与卡电气机械 (CEM) 规范一起定义了插槽信号和支持热插拔 PCI Express 所需的支持。以下是支持标准化使用模型所需和可选的端口接口信号列表：

- PWRLED#（必需）— 端口输出，控制电源指示灯的状态

- ATNLED#（必需）— 端口输出，控制注意指示灯的状态

- PWREN（如果实现了参考时钟，则必需）— 端口输出，控制插槽的主电源

- REFCLKEN#（必需）— 端口输出，控制向插槽传送参考时钟

- PERST#（必需）— 端口输出，控制插槽的 PERST#

- PRSNT1#（必需）— 在连接器处接地

- PRSNT2#（必需）— 端口输入，在系统板上拉，指示插槽中存在卡。

- PWRFLT#（必需）— 端口输入，通知热插拔控制器外部逻辑检测到的电源故障条件

- AUXEN#（如果实现了 AUX 电源，则必需）— 端口输出，当 MRL 打开和关闭时，控制开关 AUX 信号和插槽的 AUX 电源。当存在 AUX 电源时，MRL# 信号是必需的。

- MRL#（如果实现了 MRL 传感器，则必需）— 来自 MRL 传感器的端口输入

- BUTTON#（如果实现了注意按钮，则必需）— 端口输入，指示操作员已按下注意按钮。

**863**

**PCI Ex ress Technolo p gy**

_图 19-3：交换机中的热插拔控制功能_

## **热插拔控制器编程接口**

如第 865 页的图 19-4 所示，热插拔控制器的标准编程接口通过 PCI Express Capability 寄存器块提供，其中突出显示了热插拔相关寄存器。热插拔特性主要

**864**

**第 19 章：热插拔和功率预算**

在为根端口和交换机端口定义的插槽寄存器中找到。Device Capability 寄存器也在某些实现中使用，如本章后面所述。

_图 19-4：用于热插拔的 PCIe Capability 寄存器_

**==> 图片 [263 x 305] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 15 7 0<br>PCI Express Capabilities Register Next Cap Pointer PCI ExpressCap ID DW0<br>Device Capabilities Register DW1<br>Device Status Device Control DW2<br>Link Capabilities DW3<br>Link Status Link Control DW4<br>Slot Capabilities DW5<br>Slot Status Slot Control DW6<br>Root Capability Root Control DW7<br>Root Status DW8<br>Device Capabilities 2 DW9<br>Device Status 2 Device Control 2 DW10<br>Link Capabilities 2 DW11<br>Link Status 2 Link Control 2 DW12<br>Slot Capabilities 2 DW13<br>Slot Status 2 Slot Control 2 DW14<br>**----- 图片文字结束 -----**


## **Slot Capabilities**

第 866 页的图 19-5 说明了插槽能力寄存器和位字段。硬件初始化所有这些能力寄存器字段以反映此端口实现的特性。除指示灯和注意按钮外，该寄存器适用于卡插槽和机架安装实现。软件必须从模块内的设备能力寄存器中读取以确定是否实现了指示灯和注意按钮。第 866 页的表 19-5 列出并定义了插槽能力字段。

**865**

**PCI Ex ress Technolo p gy**

_图 19-5：Slot Capabilities 寄存器_

||Hot Plug Surprise<br>Slot Power Limit Scale<br>5<br>0<br>6<br>7<br>31<br>14<br>3 2<br>4<br>15<br>16<br>18 17<br>19<br>Attention Button Present<br>Power Controller Present<br>MRL Sensor Present<br>Attention Indicator Present<br>Electromechanical Interlock Present<br>Physical Slot Number<br>Slot Power Limit Value<br>Hot Plug Capable<br>Power Indicator Present<br>No Command Completed Support|Hot Plug Surprise<br>Slot Power Limit Scale<br>5<br>0<br>6<br>7<br>31<br>14<br>3 2<br>4<br>15<br>16<br>18 17<br>19<br>Attention Button Present<br>Power Controller Present<br>MRL Sensor Present<br>Attention Indicator Present<br>Electromechanical Interlock Present<br>Physical Slot Number<br>Slot Power Limit Value<br>Hot Plug Capable<br>Power Indicator Present<br>No Command Completed Support|
|---|---|---|
||**位**|**寄存器名称和描述**|
||0|**Attention Button Present（注意按钮存在）**— 指示机箱上插槽旁边存在注意按钮。|
||1|**Power Controller Present（电源控制器存在）**— 指示此插槽存在电源控制器。|
||2|**MRL Sensor Present（MRL 传感器存在）**— 指示插槽上存在 MRL 传感器。|
||3|**Attention Indicator Present（注意指示灯存在）**— 指示机箱上插槽旁边存在注意指示灯。|
||4|**Power Indicator Present（电源指示灯存在）**— 指示机箱上插槽旁边存在电源指示灯。|


**866**

**第 19 章：热插拔和功率预算**

_表 19-5：Slot Capability 寄存器字段和描述（续）_

|**位**|**寄存器名称和描述**|
|---|---|
|5|**Hot-Plug Surprise（热插拔意外）**— 指示用户无需事先通知即可从系统中移除卡。这告诉操作系统允许此类移除而不影响后续的软件操作。|
|6|**Hot-Plug Capable（支持热插拔）**— 指示此插槽支持热插拔操作。|
|14:7|**Slot Power Limit Value（插槽功率限值）**— 指定此插槽可以提供的最大功率。此限值乘以下一字段中指定的缩放比例。|
|16:15|**Slot Power Limit Scale（插槽功率限值缩放）**— 指定插槽功率限值的缩放因子。|
|17|**ElectroMechanical Interlock Present（电气机械互锁存在）**— 指示此插槽实现了电气机械互锁|
|18|**No Command Completed Support（无命令完成支持）**— 指示此插槽在命令完成时不生成软件通知。早期版本有时需要很长时间来执行热插拔命令（例如，有时需要一秒钟或更长时间通过 I2C 总线通信以打开或关闭电源），并在最终完成时生成中断。当设置此位时，意味着此端口可以无延迟地接受对 Slot Control 寄存器中所有字段的写入，因此不需要通知。|
|31:19|**Physical Slot Number（物理插槽号）**— 指示与此端口关联的物理插槽号。必须由硬件初始化为机箱内唯一的数字。请注意，软件将需要此编号以将物理插槽与逻辑插槽 ID（设备的总线、设备和功能号）相关联。|


## **Slot Power Limit Control（插槽功率限制控制）**

规范提供了一种方法来限制软件对安装在扩展插槽或背板实现中的卡所消耗的功率。支持此功能的寄存器包含在 Slot Capability 寄存器中。

**867**

**PCI Ex ress Technolo p gy**

## **Slot Control（插槽控制）**

软件通过 Slot Control 寄存器控制热插拔事件，如图 19-6 所示（在第 868 页）。此寄存器允许软件启用各种热插拔功能并控制热插拔操作。它还用于启用中断生成以及启用可能导致中断生成的热插拔事件源。

_图 19-6：Slot Control 寄存器_

**==> 图片 [385 x 252] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
15 13 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Data Link Layer<br>State Changed Enable<br>Electromechanical<br>Interlock Control<br>Power Controller Control<br>Power Indicator Control<br>Attention Indicator Control<br>Hot Plug Interrupt Enable<br>Command Completed Interrupt Enable<br>Presence Detect Changed Enable<br>MRL Sensor Changed Enable<br>Power Fault Detected Enable<br>Attention Button Pressed Enable<br>**----- 图片文字结束 -----**


**868**

**第 19 章：热插拔和功率预算**

_表 19-6：Slot Control 寄存器字段和描述_

|**位**|**寄存器名称和描述**|
|---|---|
|0|**Attention Button Pressed Enable（注意按钮按下启用）**。当设置时，此位在按下注意按钮时启用热插拔中断的生成（如果已启用）或 Wake# 消息的断言。|
|1|**Power Fault Detected Enable（电源故障检测启用）**。当设置时，启用在检测到电源故障时生成热插拔中断（如果已启用）或 Wake# 消息。|
|2|**MRL Sensor Changed Enable（MRL 传感器变化启用）**。当设置时，在检测到 MRL 传感器变化事件时启用生成热插拔中断或 Wake#（如果已启用）消息。|
|3|**Presence Detect Changed Enable（存在检测变化启用）**。当设置此位时，在 Slot Status 寄存器中的存在检测变化位置位时启用热插拔中断或 Wake 消息的生成。|
|4|**Command Completed Interrupt Enable（命令完成中断启用）**。当设置时，启用生成热插拔中断，通知软件热插拔控制器已准备好接收下一个命令。|
|5|**Hot-Plug Interrupt Enable（热插拔中断启用）**。当设置时，启用热插拔中断的生成。|
|7:6|**Attention Indicator Control（注意指示灯控制）**。写入该字段控制注意指示灯的状态，读取返回当前状态，如下：<br>• 00b = 保留<br>• 01b = 开启<br>• 10b = 闪烁<br>• 11b = 关闭|
|9:8|**Power Indicator Control（电源指示灯控制）**。写入该字段控制电源指示灯的状态，读取返回当前状态，如下：<br>• 00b = 保留<br>• 01b = 开启<br>• 10b = 闪烁<br>• 11b = 关闭|
|10|**Power Controller Control（电源控制器控制）**。写入该字段切换插槽的主电源，读取返回当前状态：0b = 电源开启，1b = 电源关闭|


**869**

**PCI Ex ress Technolo p gy**

_表 19-6：Slot Control 寄存器字段和描述（续）_

|**位**|**寄存器名称和描述**|
|---|---|
|11|**Electromechanical Interlock Control（电气机械互锁控制）**- 如果实现了互锁，写入 1b 切换其状态，写入 0b 没有效果。读取此位始终返回 0b。|
|12|**Data Link Layer State Changed Enable（数据链路层状态变化启用）**- 如果数据链路层链路有效报告能力为 1b，则设置此位启用数据链路层链路有效位变化时的软件通知。如果数据链路层链路有效报告能力为 0b，则此位变为只读且值为 0b。|


## **Slot Status and Events Management（插槽状态和事件管理）**

热插拔控制器监视各种事件并将这些事件报告给热插拔系统驱动程序。软件可以使用"已检测"位来确定已发生的事件，而状态位标识更改的性质。变化位必须由软件清除以检测后续变化。请注意，这些事件是否报告给系统（通过系统中断）由 Slot Control 寄存器中的相关启用位决定。

_图 19-7：Slot Status 寄存器_

**==> 图片 [386 x 204] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
15 9 8 7 6 5 4 3 2 1 0<br>RsvdZ<br>Data Link Layer State Changed<br>Electromechanical Interlock Status<br>Presence Detect State<br>MRL Sensor State<br>Command Completed<br>Presence Detect Changed<br>MRL Sensor Changed<br>Power Fault Detected<br>Attention Button Pressed<br>**----- 图片文字结束 -----**


**870**

**第 19 章：热插拔和功率预算**

_表 19-7：Slot Status 寄存器字段和描述_

|**位位置**|**寄存器名称和描述**|
|---|---|
|0|**Attention Button Pressed（注意按钮按下）**— 如果实现了按钮，则在按下注意按钮时设置此位。|
|1|**Power Fault Detected（电源故障检测）**— 如果实现了支持电源故障检测的电源控制器，则当它检测到此插槽的电源故障时设置此位。规范指出，无论电源控制设置如何或插槽是否被占用，都可能随时检测到电源故障。|

**871**

**PCI Ex ress Technolo p gy**

_表 19-7：Slot Status 寄存器字段和描述（续）_

|**位位置**|**寄存器名称和描述**|
|---|---|
|2|**MRL Sensor Changed（MRL 传感器变化）**— 如果实现了 MRL 传感器，则在检测到 MRL 传感器状态变化时设置此位。如果不存在传感器，则此位始终为零。|
|3|**Presence Detect Changed（存在检测变化）**— 在 Presence Detect State 位中检测到变化时设置。|
|4|**Command Completed（命令完成）**— 如果 Slot Capabilities 寄存器中的 No Command Completed Support 位为 0b，则在热插拔命令完成且热插拔控制器准备好接受另一个命令时设置此位。从技术上讲，仅保证最后一个含义：控制器准备好接受另一个命令，无论前一个命令是否实际完成。|
|5|**MRL Sensor State（MRL 传感器状态）**— 当设置时，指示 MRL 传感器的当前状态（如果实现）：0b = MRL 关闭，1b = MRL 打开|
|6|**Presence Detect State（存在检测状态）**— 此位指示插槽中存在卡，并且对于实现插槽的所有下游端口都是必需的。其值是物理层检测逻辑和为此插槽实现的任何其他边带检测机制（例如 PRSNT1# 和 PRSNT2#）的逻辑"或"。它们之间的最大区别在于，引脚无需电源即可物理检测卡，因此可以在不恢复电源的情况下对其进行报告，而使用物理层检测逻辑则需要电源。|


## **Add-in Card Capabilities（附加卡能力）**

第 873 页的图 19-8 所示的 Device Capability 寄存器也具有与附加卡相关的字段，这些字段记录了热插拔控制器报告的插槽可用功率。无论以下哪种情况发生，都必须通过 Set_Slot_Power_Limit 消息自动传达此信息：

- 对 Slot Capabilities 寄存器的配置写入更改 Slot Power Limit Value 和 Slot Power Limit Scale 值。

- 链路从非 DL_UP 状态转换到 DL_Up 状态（除非 Slot Capabilities 寄存器尚未初始化）。

该消息使用消息中的值更新 Captured Slot Power Limit Value 和 Scale 寄存器，从而使此信息可供其设备驱动程序使用。

**872**

**第 19 章：热插拔和功率预算**

_图 19-8：Device Capabilities 寄存器_

**==> 图片 [386 x 235] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 29 28 27 26 25 18 17 1615 14 12 11 9 8 6 5 4 3 2 0<br>RsvdP Undefined<br>Function-Level<br>Reset Capability<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>RsvdP<br>Role-Based Error Reporting<br>Endpoint L1 Acceptable Latency<br>Endpoint L0 Acceptable Latency<br>Extended Tag Field Supported<br>Phantom Functions Supported<br>Max Payload Size Supported<br>**----- 图片文字结束 -----**


## **静默卡和驱动程序**

## **概述**

在从系统中移除卡之前，必须发生两件事：设备驱动程序必须停止访问卡，并且卡必须停止发起或响应新请求。如何实现这一点是操作系统特定的，但必须发生以下情况：

- 操作系统必须停止向设备的驱动程序发出新请求，或指示驱动程序停止接受新请求。

- 驱动程序必须终止或完成所有未完成的请求。

- 卡必须被禁止生成中断或请求。

当操作系统命令驱动程序静默自身及其设备时，操作系统不得期望设备保留在系统中（换句话说，可以将其移除而不用相同的卡替换）。

**873**

**PCI Ex ress Technolo p gy**

## **暂停驱动程序（可选）**

可选地，操作系统可以实现"Pause"（暂停）功能以临时停止驱动程序的活动，期望同一张卡将被重新插入。但是，如果在合理的时间内未重新安装卡，则必须静默驱动程序，然后将其从内存中移除。

作为一个示例，当前安装的卡正在失败或将被更高版本作为升级所替换。如果该操作在软件和操作角度看起来是无缝的，则驱动程序必须静默设备，保存当前上下文（寄存器内容、本地微控制器的堆栈和指令指针等），然后关闭插槽的电源。然后可以安装新卡并通电，然后，当其上下文被恢复时，它可以从中断处恢复正常操作。当然，如果旧卡已失败，则可能无法简单地恢复操作。

## **静默控制多个设备的驱动程序**

如果驱动程序控制多个卡并且它接收到来自操作系统的命令以使其针对特定卡的活动静默，则它必须仅静默其针对该卡和该卡本身的活动。

## **静默失败的卡**

如果卡已失败，则驱动程序可能无法完成先前向卡发出的请求。在这种情况下，驱动程序必须检测错误，终止请求而不完成，并尝试重置卡。

## **原语**

本节讨论热插拔软件元素及其之间传递的信息。有关软件元素及其相互关系的回顾，请参阅第 852 页的表 19-1。操作系统内的热插拔服务与热插拔系统驱动程序之间的通信采用请求的形式。规范未定义这些请求的确切格式，但定义了基本请求类型及其内容。由热插拔服务向热插拔系统驱动程序发出的每种请求类型称为 _原语_（primitive）。它们在第 875 页的表 19-8 中列出和描述。

**874**

**第 19 章：热插拔和功率预算**

_表 19-8：原语_

|**原语**|**参数**|**描述**|
|---|---|---|
|Query Hot-Plug System Driver（查询热插拔系统驱动程序）|**输入**：无|请求热插拔系统驱动程序返回其控制的插槽的一组逻辑插槽 ID。|
||**返回**：此驱动程序控制的插槽的逻辑插槽 ID 集合。||
|Set Slot Status（设置插槽状态）|**输入**：<br>• 逻辑插槽 ID<br>• 新插槽状态（开或关）。<br>• 新的注意指示灯状态。<br>• 新的电源指示灯状态。|此请求用于控制插槽和与每个插槽关联的注意指示灯。通过返回 Status Change Successful 参数来指示请求成功完成。如果在尝试状态更改期间发生故障，则热插拔系统驱动程序应返回适当的故障消息（请参见中间列）。除非另有规定，否则卡应保持关闭状态。|
||**返回**：请求完成状态：<br>• 状态更改成功<br>• 故障—频率错误<br>• 故障—功率不足<br>• 故障—配置资源不足<br>• 故障—电源故障<br>• 故障—一般故障||
|Query Slot Status（查询插槽状态）|**输入**：逻辑插槽 ID|此请求返回所指示插槽的状态（如果存在卡）。热插拔系统驱动程序必须返回插槽电源状态信息。|
||**返回**：<br>• 插槽状态（开或关）<br>• 卡功率要求。||


**875**

**PCI Ex ress Technolo p gy**

_表 19-8：原语（续）_

|**原语**|**参数**|**描述**|
|---|---|---|
|Async Notice of Slot Status Change（插槽状态更改的异步通知）|**输入**：逻辑插槽 ID|这是由规范定义的由热插拔系统驱动程序向热插拔服务发出的唯一原语。当驱动程序检测到插槽状态的非请求更改时发送。示例将是运行时电源故障或在没有警告的情况下在先前为空的插槽中安装了卡。|
||**返回**：无||


## **功率预算介绍**

PCI Express 功率预算能力的主要目标是为运行时添加到系统的 PCI Express 热插拔设备分配功率。这确保了系统可以为此类设备分配适量的功率和散热。

规范规定"对于以不需要热插拔的形态因素实现的 PCI Express 设备或集成在系统板上的设备，功率预算是可选的"。在撰写本文时发布的形态因素规范中没有要求支持热插拔或功率预算能力，但这些经常变化。

始终需要系统功率预算来支持所有系统板设备和附加卡。新能力提供了管理热插拔卡的预算过程的机制。每个形态因素规范定义了给定扩展插槽的最小和最大功率。例如，CEM 规范限制了完全启用之前扩展卡可以消耗的功率，但在启用之后，它可以使用为插槽指定的最大功率。如果没有功率预算能力寄存器，则系统设计人员负责保证功率已正确预算，并且有足够的散热可用于支持安装到连接器中的任何兼容卡。

规范定义了支持功率预算过程的配置寄存器，但没有定义功率预算方法和过程。下一节描述了将涉及功率预算的硬件和软件元素，包括指定的配置寄存器。

**876**

**第 19 章：热插拔和功率预算**

## **功率预算元素**

图 19-10 说明了热插拔卡的功率预算概念。功率预算、分配和报告过程中涉及的每个元素的角色被列出并描述如下：

- 用于电源管理的系统固件（在引导时使用）。

- 功率预算管理器（在运行时使用）。

- 扩展端口（卡插槽所连接的端口）。

- 附加设备（支持功率预算）。

## **系统固件**

由平台设计人员为特定系统编写，负责报告系统电源信息。规范建议将以下功率信息报告给 PCI Express 功率预算管理器，该管理器在运行时分配和验证功率消耗和散热：

- 系统可用的总功率。

- 由固件分配给系统设备的功率

- 系统中插槽的数量和类型。

固件还可以为支持功率预算能力寄存器集的 PCIe 设备分配功率，例如在引导时使用的热插拔设备。如第 878 页的图 19-9 所示的功率预算能力寄存器包含一个 System Allocated 位，由硬件初始化（通常由固件）以通知功率预算管理器该设备的功率已包含在系统功率分配中。如果是这种情况，则功率预算管理器仍需要读取并保存热插拔设备分配的功率信息，以防它们在运行时稍后被移除。

**877**

**PCI Ex ress Technolo p gy**

_图 19-9：功率预算寄存器_

**==> 图片 [379 x 171] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31                                                                                               0<br>Offset<br>PCIe Extended Capability Header 00h<br>Data Select<br>RsvdP 04h<br>Register<br>Data Register 08h<br>Power Budget<br>RsvdP 0Ch<br>Capability Register<br>System Allocated Bit<br>Bit 0 of Power Budget Capability Register<br>**----- 图片文字结束 -----**


## **功率预算管理器**

它在操作系统安装时初始化，并从系统固件接收功率预算信息，尽管规范没有定义传递此信息的方法。该管理器负责为所有 PCI Express 设备分配功率，包括：

- 尚未由系统分配的 PCI Express 设备（包括支持功率预算的嵌入式设备）。

- 在引导时安装的热插拔设备。

- 在运行时添加的新设备。

## **扩展端口**

第 880 页的图 19-10 说明了一个热插拔端口，该端口必须实现 Slot Capabilities 寄存器中的 Slot Power Limit 和 Slot Power Scale 字段。固件或功率预算管理器必须使用表示此端口支持的最大功率的值加载这些字段。当软件写入这些字段时，端口会自动向设备传送 Set_Slot_Power_Limit 消息。这些字段也会在软件配置作为热插拔安装添加的新卡时被写入。

**878**

**第 19 章：热插拔和功率预算**

## 规范要求：

- 任何连接了插槽的下游端口（其 PCIe Capabilities 寄存器中的 Slot Implemented 位已设置）必须实现 Slot Capabilities 寄存器。

- 软件必须初始化连接到附加插槽的下游端口的 Slot Capabilities 寄存器的 Slot Power Limit Value 和 Scale 字段。

- 上游端口必须实现 Device Capabilities 寄存器。

- 当卡安装在插槽中且软件更新下游端口的功率限值和缩放值时，该端口将自动向已安装卡的上游端口发送 Set_Slot_Power_Limit 消息。

- 消息的接收方必须使用数据有效负载来限制其整个卡的功率使用，除非该卡永远不会超过相应电气机械规范中指定的最低值。

## **附加设备**

支持功率预算能力的扩展卡必须包括 Device Capabilities 寄存器中的 Slot Power Limit Value 和 Slot Limit Scale 字段，以及用于报告功率相关信息的功率预算能力寄存器集。

这些设备不得消耗超过形态因素规范指定的最低功率。一旦功率预算软件通过 Set_Slot_Power_Limit 消息分配了额外的功率，则设备可以消耗已指定的功率，但直到它已被配置和启用之后才可以。

**设备驱动程序** — 设备的软件驱动程序负责在启用设备之前验证是否有足够的功率可用于正确的设备操作。如果功率低于设备所需的功率，则设备驱动程序负责将此情况报告给更高级别的软件机构。

**879**

**PCI Ex ress Technolo p gy**

_图 19-10：涉及功率预算的元素_

**==> 图片 [371 x 480] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Operating<br>Firmware<br>Power  Budgeting<br>System<br>Reports Power Budget Info<br>Device to Power Manager including:<br>Driver 1 Power Budget<br>Manager<br>- Total system power budget<br>- Total power allocated to system<br>  Devices board devices.<br>- Total number and type of slots<br>PCIe<br>Bus Driver<br>Configures Ports<br>Root or Switch Port with Power Limit<br>Information<br>Slot Capabilities Register<br>Hot-Plug<br>Controller 1 31 19 18 17 16 15 14 7 6 5 4 3 2 0<br>Physical Slot Number<br>Slot Power Scale<br>Slot Power Value<br>PortPort<br>InterfaceInterface Root or Switch port<br>sends power limit<br>message to add-in card.<br>Device Capabilities Register<br>31 28 27 26 25 18 17 15 14 13 12 11 9 8 6 5 4 3 2 0<br>RsvdP<br>Captured Slot Power Limit Value<br>Captured Slot Power Limit Scale<br>Power Budget Capability Registers<br>31                                                                                               0<br>PCIe Extended Capability Header<br>RsvdP Data Select Register<br>Data Register<br>RsvdP Power Budget Capability<br>Register<br>Indicator Ctl Hot Plug Stat Hot Plug Ctl<br>**----- 图片文字结束 -----**


**880**

**第 19 章：热插拔和功率预算**

## **Slot Power Limit Control（插槽功率限制控制）**

软件负责确定允许扩展设备消耗的最大功率。此分配基于系统内的功率分区、热能力等。系统的功率和热限制的知识来自系统固件。固件或电源管理器负责将功率限制报告给每个扩展端口。

## **扩展端口提供插槽功率限制**

软件写入 Slot Capability 寄存器的 _Slot Power Limit Value_ 和 _Slot Power Limit Scale_ 字段以指定设备可以消耗的最大功率。软件需要指定反映规范定义的最大值之一的功率值。例如，CEM 规范的 2.0 版定义了表 19-9 中列出的功率使用情况。

关于这些值的一个有趣的事实是，标准高度的 x1 服务器卡在复位后限制为 10W，并且仅在被配置和启用后才允许使用全部 25W。类似地，x16 显卡将被限制为 25W，直到被配置和启用以使用全部 75W。

_表 19-9：系统板扩展插槽的最大功耗_

||**X1 链路**|**X1 链路**|**X4/X8 链路**|**X16 链路**|**X16 链路**|
|---|---|---|---|---|---|
|标准高度|10W<br>（最大 -<br>桌面）|25W<br>（最大 -<br>服务器）|25W（最大）|25W<br>（最大 -<br>服务器）|75W<br>（最大 -<br>显卡）|
|低剖面卡|10W（最大）||25W（最大）|25W（最大）||

除了基本 CEM 规范之外，还为更高功率设备定义了两个规范。首先是 PCIe x16 Graphics 150W-ATX Spec 1.0，它定义了一个能够从卡连接器汲取 75W 以及从单独的 3 针 ATX 电源连接器汲取另外 75W 的视频卡。第二个是 PCIe 225W/300W High Power CEM Spec 1.0，它通过添加另一个 3 针电源连接器以达到 225W 或 4 针 ATX 连接器以达到总共 300W 来扩展此功能。

**881**

## **PCI Ex ress Technolo p gy**

当 Slot Power 寄存器由功率预算软件写入时，扩展端口向扩展设备发送 Set_Slot_Power_Limit 消息。此过程在第 882 页的图 19-11 中说明。

_图 19-11：插槽功率限制顺序_

**==> 图片 [367 x 229] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Root or Switch Port<br>Slot Capabilities Register<br>Hot-Plug<br>Controller 1 31 19 18 17 16 15 14 7 6 5 4 3 2 0<br>Physical Slot Number<br>Slot Power Scale<br>Slot Power Value<br>PortPort<br>InterfaceInterface Root or Switch port<br>sends power limit<br>message to add-in card.<br>Device Capabilities Register<br>31 28 27 26 25 18 17 15 14 13 12 9 8 6 5 4 3 2 0<br>RsvdP<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>Indicator Ctl Hot Plug Stat Hot Plug Ctl<br>**----- 图片文字结束 -----**


1. 当热插拔软件被通知卡插入请求时，电源和时钟恢复到插槽。

2. 热插拔软件调用配置和功率预算软件来配置和分配设备的功率。

3. 功率预算软件可以询问卡以确定其功率要求和特性。

4. 然后根据设备的要求和系统的能力分配功率。

5. 电源管理软件写入扩展端口内的 Slot Power Scale 和 Slot Power Value 字段。

6. 写入这些字段命令端口发送 Set_Slot_Power_Limit 消息以传送 Slot Power 字段的内容。

7. 插槽接收消息并更新其 Captured Slot Power Limit Value 和 Scale 字段。

8. 这些值限制了扩展设备在被其设备驱动程序启用后可以消耗的功率。

**882**

**第 19 章：热插拔和功率预算**

## **扩展设备限制功率消耗**

设备驱动程序从 Captured Slot Power Limit 和 Scale 字段读取值以验证可用功率是否足以操作设备。可能存在几种情况：

- 有足够的功率可用于全功能操作设备。在这种情况下，驱动程序通过写入配置 Command 寄存器来启用设备，允许设备消耗 Power Limit 字段中指定的限制功率。

- 可用功率足以操作设备但不能全功能操作。在这种情况下，驱动程序需要配置设备，使其消耗的功率不超过 Power Limit 字段中指定的功率。

- 可用功率不足以操作设备。在这种情况下，驱动程序不得启用卡，并且必须将功率不足的情况报告给上层软件，上层软件应相应地通知最终用户问题。

- 可用功率超过形态因素规范指定的最大功率。这种情况不应发生。但是，如果发生，则不允许设备消耗超过形态因素允许的最大功率。

- 可用功率低于形态因素规范指定的最低值。这违反了规范，该规范规定扩展端口"不得传输指示限制低于插槽形态因素的电气机械规范中指定的最低值的 Set_Slot_Power_Limit 消息。"

一些扩展设备可能消耗的功率低于其形态因素指定的最低限制。允许此类设备丢弃在 Set_Slot_Power_Limit 消息中传递的信息。当读取 Slot Power Limit Value 和 Scale 字段时，这些设备返回零。

## **功率预算能力寄存器集**

这些寄存器允许功率预算软件基于设备通过其功率预算数据选择和数据寄存器提供的信息更有效地分配功率。此功能类似于电源管理能力寄存器中的数据选择和数据字段。但是，功率预算寄存器向软件提供了更详细的信息，以帮助其确定运行时添加的扩展卡对系统功率预算和冷却要求的影响。通过此能力，设备可以报告其消耗的功率：

- 来自每个电源轨

- 在各种电源管理状态下

- 在不同的操作条件下

对于在系统板上实现的设备或不支持热插拔的扩展设备，这些寄存器不是必需的。第 884 页的图 19-12 说明了功率预算能力寄存器集，并显示了提供访问功率预算信息方法的数据选择和数据字段。

**883**

## **PCI Ex ress Technolo p gy**
