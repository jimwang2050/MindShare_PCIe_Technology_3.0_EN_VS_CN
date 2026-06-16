|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers or**<br>**State that**<br>**must be valid**|**Power**|**Actions permitted to**<br>**Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D1|Device<br>class-specific<br>registers<br>and PME<br>context.*|D0<br>unini-<br>tial-<br>ized|Config Requests and<br>Messages. Link transi-<br>tions back to L0 to ser-<br>vice the request.|PME Messages.**<br>Though not typi-<br>cally permitted,<br>they would require<br>the Link to transi-<br>tion back to L0.|
|L2-L3||NA *||||



* This combination of Bus/Function PM states not allowed.

- ** If PME supported in this state.

## **D2 状态 — 深睡眠 (D2 State—Deep Sleep)**

**Optional**. 在进入此状态之前，软件必须确保所有未完成的 non-posted 请求都已收到其相关的完成。这可以通过轮询 PCI Express Capability 块的 Device Status 寄存器中的 Transactions Pending 位来实现；

**717**

**PCI Ex ress Technolo p gy**

当位清零时，可以安全地进行。这种电源状态提供比 D1 更深但比 D3hot 状态少的节能。与 D1 中一样，函数不会发起请求（PME Message 除外）或不充当配置以外请求的目标。软件仍必须能够在此状态下访问函数的配置寄存器。

D2 状态的其他特征包括：

- 在进入此状态之前，软件必须确保所有未完成的 non-posted 请求都已收到其相关的完成。这可以通过轮询 PCIe Capability 块的 Device Status 寄存器中的 Transactions Pending 位来实现。可能会发生完成永远不会返回的情况，在这种情况下，软件应等待足够长的时间以确保它们永远不会返回。

- 当设备转换为 D2 状态时，链路状态必须转换为 L1。

- • 在此状态下接受配置和消息请求，但所有其他请求必须作为 Unsupported Requests 处理，并且所有完成可选择性地作为 Unexpected Completions 处理。

- 如果错误是由传入请求引起的并且启用了报告，则可以在此状态下发送 Error Message。如果发生不同类型的错误（例如 Completion timeout），则消息将不会发送，直到设备返回到 D0 状态。

- 函数可以发送 PME 消息（如果支持并已启用），以通知软件它需要恢复电源以处理事件。

- 函数可能在此状态下丢失其上下文。如果丢失并且设备支持 PME 消息，则它必须至少为此目的维护其 PME 上下文。

- 函数必须返回到 D0 Active 状态才能完全运行。

表 16-7 在第 719 页说明了 D2 状态下的 PM 策略。

**718**

**第 16 章：电源管理**

_表 16-7：D2 电源管理策略_

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must be**<br>**valid**|**Power**|**Actions permitted**<br>**to Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D2|Device<br>class-specific<br>registers<br>and PME con-<br>text. *|next higher<br>supported PM<br>state orD0<br>uninitialized.|Config Requests<br>and transactions<br>permitted by<br>device class (typi-<br>cally none).<br>This requires the<br>Link to transition<br>back to L0|PME Messages.*<br>Though not typi-<br>cally permitted,<br>they would require<br>the Link to transi-<br>tion back to L0.|
|L2/L3||N/A**||||



- If PME supported in this state.

- ** This combination of Bus/Function PM states not allowed.

## **D3 — 全关 (D3—Full Off)**

**Mandatory**. 所有函数必须支持 D3 状态。这是最深的状态，节能最大化。当软件将此电源状态写入设备时，它进入 **D3hot** 状态，这意味着电源仍然存在。从设备中移除电源 (Vcc) 会将其置于 **D3cold** 状态，并将链路置于 L2（如果有辅助电源 (Vaux) 可用），如果没有则置于 L3。

**D3Hot 状态 (Mandatory).** 软件通过将适当的值写入其 Power Mgt Control and Status Register (PMCSR) 的 PowerState 字段，将函数置于 D3hot。在此状态下，函数只能发起 PME 或 PME_TO_ACK 消息，并且只能响应配置请求或 PME_Turn_Off 消息。软件必须能够在设备处于 D3hot 状态时访问函数的配置寄存器，即使只是为了能够将状态更改回 D0。D3hot 的其他特征包括：

- 在进入此状态之前，软件必须确保所有未完成的 non-posted 请求都已收到其相关的完成。这可以通过轮询 PCIe Capability 块的 Device Status 寄存器中的 Transactions Pending 位来实现。可能会发生完成永远不会返回的情况，在这种情况下，软件应等待足够长的时间以确保它们永远不会返回。

- 当函数更改为 D3hot 时，链路被强制进入 L1 状态。

**719**

## **PCI Ex ress Technolo p gy**

- 允许函数发送 PME 消息以通知 PM 软件其需要返回到完全活动状态（假设它支持在 D3hot 状态下生成 PM 事件并已启用）。

- 函数上下文在进入此状态时可能会丢失，如果电源关闭，规范假定所有上下文都将丢失。另一方面，如果在软件启动返回 D0 之前电源从未关闭，则可以维护上下文。在早期规范版本中，这是不可能的；从 D3hot 更改为 D0 涉及软复位并且所有寄存器都重新初始化。但是，该规范的 1.2 版本添加了一个新的功能位，称为"No Soft Reset"，以指示函数在这种情况下不会执行软复位。为了能够在 D3hot 状态下生成 PME 消息，设备必须维护其 PME 上下文（请参见第 710 页的"PME Context"）。

函数在两种情况下退出 D3hot 状态：

- 如果从设备中移除了 Vcc，则它从 D3hot 转换到 D3cold。

- 软件可以写入函数的 PMCSR 寄存器的 PowerState 字段以将其 PM 状态更改为 D0。当编程退出 D3hot 并返回到 D0 时，函数返回到 D0 Uninitialized PM 状态。可能需要也可能不需要复位。表 16-8 在第 721 页列出了 D3hot 状态下的 PM 策略。

**720**

**第 16 章：电源管理**

_表 16-8：D3hot 电源管理策略_

|**Bus**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must**<br>**be valid**|**Power**|**Actions permitted**<br>**to Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D3hot|PME con-<br>text. **|next higher<br>supported PM<br>state orD0<br>uninitialized.|PCI Express config<br>transactions<br>& PME_Turn_Off<br>broadcast<br>message***<br>(These can only<br>occur after the Link<br>transitions back to<br>its L0 state.|PME message**<br>PME_TO_ACK<br>message***<br>PM_Enter_L23<br>DLLP***<br>(These can occur<br>only after the Link<br>returns to L0)|
|L2/L3<br>Ready||L2/L3 Ready entered following the PME_Turn_Off handshake sequence, which<br>prepares a device for power removal***||||
|L2/L3||NA *||||



- This combination of Bus/Function PM states not allowed.

** If PME supported in this state.

*** See "L2/L3 Ready Handshake Sequence" on page 764 for details regarding the sequence.

**D3Cold 状态 (Mandatory)**. 每个 PCI Express 函数在从函数中移除电源 (Vcc) 时进入 D3Cold PM 状态。当电源恢复时，设备必须被复位或生成内部复位，从而将其从 D3Cold 带至 D0 Uninitialized。能够生成 PME 的函数必须在此状态下以及转换为 D0 状态时维护 PME 上下文。由于移除电源才能进入此状态，因此如果函数要维护 PME 上下文，则必须具有可用的辅助电源。然后，当设备进入 D0 Uninitialized 时，它可以生成 PME 消息以通知系统唤醒事件（如果它有能力并已启用）。有关辅助电源的更多信息，请参见第 775 页的"Auxiliary Power"。

表 16-9 在第 722 页说明了 D3Cold 状态下的 PM 策略。

**721**

## **PCI Ex ress Technolo p gy**

_表 16-9：D3cold 电源管理策略_

|**Bus**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must be**<br>**valid**|**Power**|**Actions**<br>**permitted to**<br>**Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L2|D3cold|PME<br>context*|AUX<br>Power|Bus reset only|Signal Beacon<br>or WAKE#**|
|L3||None|||None|



- If PME supported in this state.

** The method used to signal a wake to restore clock and power depends on the form factor.

## **函数 PM 状态转换 (Function PM State Transitions)**

图 16-6 说明了 PCIe 函数的 PM 状态转换。表 16-10 在第 723 页提供了每个转换的描述。表 16-11 在第 724 页从硬件和软件角度说明了从一个状态到另一个状态的转换。

_图 16-6：PCIe 函数 D 状态转换_

**==> 图片 [192 x 195] 已省略 <==**

**----- Start of picture text -----**<br>
Power On<br>Reset D0<br>Un-initialized<br>D0<br>Active<br>D3<br>D1 D2<br>Hot<br>D3<br>Vcc Cold<br>Removed<br>**----- End of picture text -----**<br>


**722**

**第 16 章：电源管理**

_表 16-10：函数状态转换的描述_

|**From State**|**To State**|**Description**|
|---|---|---|
|D0<br>Uninitialized|D0 Active|函数已完全配置并由其驱动程序启用。|
|D0 Active|D1|软件将 PMCSR PowerState 写入 D1。|
||D2|软件将 PMCSR PowerState 写入 D2。|
||D3hot|软件将 PMCSR PowerState 写入 D3hot。|
|D1|D0 Active|软件将 PMCSR PowerState 写入 D0。|
||D2|软件将 PMCSR PowerState 写入 D2。|
||D3hot|软件将 PMCSR PowerState 写入 D3hot。|
|D2|D0 Active|软件将 PMCSR PowerState 写入 D0。|
||D3hot|软件将 PMCSR PowerState 写入 D3hot。|
|D3hot|D3cold|从函数中移除电源。|
||D0<br>Uninitialized|软件将 PMCSR PowerState 写入 D0。|
|D3cold|D0<br>Uninitialized|将电源恢复到函数。|



**723**

**PCI Ex ress Technolo p gy**

_表 16-11：函数状态转换延迟_

|**Initial State**|**Next**<br>**State**|**Minimum software-guaranteed delays**|
|---|---|---|
|D0|D1|0|
|D0 or D1|D2|从新状态设置到首次访问（包括配置访问）的 200μs。|
|D0, D1, or D2|D3hot|从新状态设置到首次访问的 10ms。|
|D1|D0|0|
|D2|D0|从新状态设置到首次访问的 200μs。|
|D3hot|D0|从新状态设置到首次访问的 10ms。|
|D3cold|D0||



## **PCI-PM 寄存器的详细描述 (Detailed Description of PCI-PM Registers)**

_PCI Bus PM Interface spec_ 定义了在 PCIe 函数中实现的 PM 寄存器（请参见图 16-7）。配置软件可以确定 PM 能力并控制其属性。

_图 16-7：PCI 函数的 PM 寄存器_
