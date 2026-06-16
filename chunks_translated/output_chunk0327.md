3. 相应的拆分完成必须基于事务排序规则将其之前的所有已发布 PME 消息推到其前面。

4. 根复合体无法接受新的 PME 消息，因为队列已满，因此路径被临时阻塞。但这也意味着读完成无法到达根复合体以清除队列中较旧的条目。

5. 没有任何进展，发生死锁。

## **解决方案**

如果根复合体始终接受新的 PME 消息，即使它们会使队列溢出，则可以避免此问题。在这种情况下，根只是丢弃后来的 PME 消息。为防止被丢弃的 PME 消息永久丢失，发送 PME 消息的设备必须测量一个称为 PME Service Time-out 的超时间隔。如果设备的 PME_Status 位未在 100ms (+ 50%/‐ 5%) 内被清除，则它假定其消息必定已丢失并重新发出该消息。

## **PME 上下文**

生成 PME 的设备必须继续为设备中用于检测、发信号和处理 PME 事件的部分供电，这些部分统称为 PME 上下文。支持 D3cold 状态下 PME 的设备在主电源被移除时使用辅助电源来维护 PME 上下文。PME 上下文中通常包括的项目：

- PME_Status 位（必需）— 在设备发送 PME 消息时设置，由 PM 软件清除。支持 D3cold 状态下 PME 的设备必须将 PME_Status 位实现为"粘性"，这意味着该值在基本复位后仍然存在。

**771**

## **PCI Ex ress Technolo p gy**

- PME_Enable 位（必需）— 该位必须保持置位以继续启用 Function 生成 PME 消息和发出唤醒信号的能力。支持 D3cold 状态下 PME 的设备必须将 PME_Enable 实现为"粘性"，这意味着该值在基本复位后仍然存在。

- 设备特定的状态信息 — 例如，设备可能在有多种不同类型的事件可以触发 PME 的情况下保留事件状态信息。

- 应用程序特定的信息 — 例如，启动唤醒的调制解调器在支持时会保留来电显示信息。

## **唤醒不可通信链路**

当支持 D3cold 状态下 PME 的设备需要发送 PME 消息时，它必须首先将 Link 转换到 L0。这有时称为唤醒。PCI Express 定义了触发不可通信链路唤醒的两种方法：

- Beacon — 由 AUX 电源驱动的带内指示符

- WAKE# 信号 — 由 AUX 电源驱动的边带信号

在这两种情况下，都必须通知 PM 软件以恢复主电源和参考时钟。这也会导致基本复位，迫使设备进入 D0uninitialized 状态。一旦 Link 转换到 L0，设备就会发送 PME 消息。由于需要复位才能重新激活 Link，设备必须跨上述复位序列维护 PME 上下文。

## **Beacon**

此信令机制被设计为在 AUX 电源上工作，且不需要太多电力。Beacon 仅仅是通知上游组件软件应被通知唤醒请求的一种方式。当交换机在下游端口上收到 beacon 时，它们会依次在其上游端口上发出 beacon。最终，beacon 到达根复合体，在那里它生成一个调用 PM 软件的中断。

某些外形尺寸要求 beacon 支持唤醒系统，而其他外形尺寸则不需要。规范要求符合外形尺寸规范，并且如果其外形尺寸不需要 beacon 支持，则不需要设备支持 beacon。但是，对于设计用于各种外形尺寸的"通用"组件，则需要 beacon 支持。有关详细信息，请参见第 483 页的"Beacon Signaling"。

**772**

**第 16 章：电源管理**

## **WAKE#**

PCI Express 提供了一个名为 WAKE# 的边带信号作为 beacon 的替代方案，可以直接路由到根或其他系统逻辑以通知 PM 软件。尽管希望最小化链路的引脚数，但添加此额外引脚的动机很容易理解。原因是组件必须消耗辅助电源才能识别下游端口上的 beacon，然后将其转发到上游端口。在电池供电的系统中，辅助电源受到严格保护，因为它即使在系统不工作时也会消耗电池电量。在这种情况下，首选的解决方案是在传递唤醒通知时绕过尽可能多的组件，而 WAKE# 引脚正好可以很好地满足此目的。另一方面，如果不担心功耗，那么 WAKE# 引脚可能就不那么理想了。

也可以使用混合实现。在这种情况下，WAKE# 被发送到交换机，而交换机又在其上游端口上发送 beacon。这些选项如图 16-29（第 774 页 A 和 B）所示。注意，当断言时，WAKE# 信号保持低电平，直到软件清除 PME_Status 位。

此信号必须由 ATX 或基于 ATX 的连接器以及插卡以及小型插卡外形尺寸实现。对于嵌入式设备使用 WAKE# 信号没有规定要求。

**773**

## **PCI Ex ress Technolo p gy**

_图 16-29：WAKE# 信号实现_

**==> picture [317 x 472] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>
L2 State<br>
(F) PM State D3<br>
Switch<br>
L2 State L2 State<br>
PM State<br>
PM State D3 PCIe D3 PCIe PM State D3<br>
Endpoint (C) Endpoint<br>
(D) Switch (E)<br>
L2 State L2 State WAKE#<br>
A Card Slots<br>
Root Complex<br>
L2 State<br>
(F)<br>
Switch PM State D3<br>
Beacon signaling used from L2 State<br>
switch to Root Complex.<br>
PM State D3 PCIe PM StateD3 PCIe PM State D3<br>
Endpoint Endpoint<br>
(C)<br>
(D) Switch (E)<br>
L2 State WAKE#<br>
B Card Slots<br>
**----- End of picture text -----**<br>


**774**

**第 16 章：电源管理**

## **辅助电源**

支持 D3cold 状态下 PME 的设备必须支持唤醒序列，并被 PCI-PM 规范允许消耗最大辅助电流 375mA（否则只能消耗 20mA）。它们所需的电流量在 PM Capability 寄存器的 _Aux_Current_ 字段中报告。当 PMCSR 寄存器中的 _PME_Enable_ 位被设置时，启用辅助电源。

PCI Express 扩展了辅助电源的使用，超出了 PCI-PM 给出的限制。现在，任何设备都可以在通过设置设备控制寄存器的 _Aux Power PM Enable_ 位启用时消耗最大辅助电流，如图 16-30（第 775 页）所示。这使设备有机会在低功耗状态下支持 SM Bus 等其他功能。与 PCI-PM 中一样，设备消耗的电流量在 PMC 寄存器的 _Aux_Current_ 字段中报告。

_图 16-30：不支持 PME 的设备的辅助电流启用_

|||15|14|12|11|10|9|8|7|5|4|3|2|1|0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||
|Bridge Config. Retry Enable/||||||||||||||||
|Initiate Function-Level Reset||||||||||||||||
|Max Read Request Size||||||||||||||||
||Enable No Snoop|||||||||||||||
||Aux Power PM Enable|||||||||||||||
|Phantom Functions Enable||||||||||||||||
|Extended Tag Field Enable||||||||||||||||
||Max Payload Size|||||||||||||||
|Enable Relaxed Ordering||||||||||||||||
||Unsupported Request|||||||||||||||
||Reporting Enable|||||||||||||||
|Fatal|Error Reporting Enable|||||||||||||||
||Non-Fatal Error|||||||||||||||
||Reporting Enable|||||||||||||||
||Correctable Error|||||||||||||||
||Reporting Enable|||||||||||||||

**775**

**PCI Ex ress Technolo p gy**

## **提高 PM 效率**

## **背景**

随着处理器和其他系统组件获得更好的电源管理机制，像 PCIe 组件这样的外围设备开始成为 PC 系统中较大的功耗贡献者。早期的 PCIe 几代允许一些软件和硬件电源管理，但与系统的 PM 决策协调并不是高优先级的，因此软件可见性和控制是有限的。

缺乏协调可能导致的一个问题是，当系统进入睡眠状态但设备仍保持运行状态时。这些设备可以发起中断或 DMA 流量，从而需要系统唤醒以处理它们，即使它们是低优先级事件，因此破坏了节能的目标。

系统也可能不知道设备在请求系统服务（如内存读取）到收到响应之间可以等待多长时间。如果不知道该信息，软件通常被迫假设响应时间必须始终最小，因此电源管理策略无法承担足够的时间来做更多工作。但是，如果系统知道何时不需要快速响应的时间窗口，则可以更积极地进行电源管理，并在不冒性能风险的情况下在低功耗状态下停留更长时间。2.1 规范修订版增加了两个新特性来解决这些问题。

## **OBFF（优化的缓冲区刷新与填充）**

第一个机制是优化缓冲区刷新和填充（Optimized Buffer Flush and Fill），它提供了一种机制，使端点能够了解系统电源状态，从而了解与系统进行数据传输的最佳时间。

## **问题**

能够进行总线主控的设备的问题在于，如果它们不了解系统电源状态，它们可能会在最好等待的时候发起事务。第 777 页的图 16-31 中的图示以简单的术语说明了该问题：有许多组件发起事件，因此，

**776**

**第 16 章：电源管理**

系统空闲且可以进入睡眠的时间很少且很短。相比之下，第 777 页的图 16-32 展示了一种改进，其中相同的事件被分组并一起处理，从而使系统空闲到足以进入睡眠的时间更频繁且持续时间更长。显然，这将带来更好的节能效果，而且幸运的是，实现起来并不困难。PCIe 组件只需了解它们应根据系统电源状态做什么，并且它们需要一种方法来了解当前的状态。

_图 16-31：较差的系统空闲时间_

**==> picture [310 x 135] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Idle System Idle<br>
Window Window<br>
System Events<br>
Endpoint A<br>
Events<br>
Endpoint B<br>
Events<br>
Endpoint C<br>
Events<br>
Time<br>
**----- End of picture text -----**<br>


_图 16-32：改进后的系统空闲时间_

**==> picture [327 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Idle System Idle System Idle<br>
Window Window Window<br>
System Events<br>
Endpoint A<br>
Events<br>
Endpoint B<br>
Events<br>
Endpoint C<br>
Events<br>
Time<br>
LTR could also be used to inform system software of acceptable latency for<br>
the endpoints between accesses, suggesting a limit on this idle time.<br>
**----- End of picture text -----**<br>


**777**

**PCI Ex ress Technolo p gy**

## **解决方案**
