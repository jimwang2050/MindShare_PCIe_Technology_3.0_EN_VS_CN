|Assert_INTD|0010 0011b||
|Deassert_INTA|0010 0100b||
|Deassert_INTB|0010 0101b||
|Deassert_INTC|0010 0110b||
|Deassert_INTD|0010 0111b||

有关使用 INTx Messages 的规则：

1. 它们没有数据负载，因此 Length 字段被保留。

2. 它们仅由 Upstream Ports 发出。对接收到的包检查此规则是可选的，但如果检查，违反将作为 Malformed TLPs 处理。

3. 它们必须使用默认流量类 TC0。接收方必须检查此规则，违反将作为 Malformed TLPs 处理。

4. 链路两端的组件必须跟踪四个虚拟中断的当前状态。如果 Upstream Port 的逻辑状态发生变化，则必须发送适当的 INTx 消息。

5. 当 Command Register 的 Interrupt Disable 位设置为 = 1 时，INTx 信令被禁用（与物理中断线的情况一样）。

6. 如果在设备中设置了 Interrupt Disable 位时任何虚拟 INTx 信号处于 active 状态，则 Upstream Port 必须发送相应的 Deassert_INTx 消息。

7. 交换机必须为每个 Downstream Port 独立跟踪四个 INTx 信号的状态，并为 Upstream Port 组合这些状态。

8. 根复合体必须独立跟踪四个 INTx 线的状态，并以实现特定的方式将它们转换为系统中断。

**207**

## **PCI Express Technology**

9. 它们使用 "Local‐Terminate at Receiver" 路由类型，以允许 Switch 在必要时重新映射指定的中断引脚（参见第 808 页 "Mapping and Collapsing INTx Messages"）。因此，INTx 消息中的 Requester ID 可以由最后一个发送者分配。

**Power Management Messages.** PCI Express 与 PCI 电源管理兼容，并增加了基于硬件的链路电源管理。消息用于传达其中一些信息，但要了解整个 PCIe 电源管理协议的工作原理，请参考第 16 章 "Power Management"，位于第 703 页。第 208 页的表 5‐10 总结了四种电源管理消息类型。

*Table 5‐10: Power Management Message Coding*

|**Power Management Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|PM_Active_State_Nak|0001 0100b|100b|
|PM_PME|0001 1000b|000b|
|PM_Turn_Off|0001 1001b|011b|
|PME_TO_Ack|0001 1011b|101b|

电源管理消息规则：

1. 电源管理消息没有数据负载，因此 Length 字段被保留。

2. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

3. PM_Active_State_Nak 由 Downstream Port 在观察到链路邻居请求将链路电源状态更改为 L1 但其选择不这样做时发送（Local ‐ Terminate at Receiver 路由）。

4. PM_PME 由请求电源管理事件的组件向上游发送（Implicitly Routed to the Root Complex）。

5. PM_Turn_Off 向下游发送到所有端点（Implicitly Broadcast from the Root Complex 路由）。

6. PME_TO_Ack 由端点向上游发送。对于具有多个 Downstream Ports 的交换机，在所有 Downstream Ports 收到此消息之前，该消息不会被转发到上游（Gather and Route to the Root Complex 路由）。

**208**

**Chapter 5: TLP Elements**

**Error Messages.** Error Messages 由检测到错误的已启用组件向上游发送（Implicitly Routed to the Root Complex）。为了帮助软件了解如何处理错误，Error Message 在消息头的 Requester ID 字段中标识请求代理。第 209 页的表 5‐11 描述了三种错误消息类型。

*Table 5‐11: Error Message Coding*

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|ERR_COR (Correctable)|0011 0000b|000b|
|ERR_NONFATAL<br>(Uncorrectable, Non‐fatal)|0011 0001b||
|ERR_FATAL<br>(Uncorrectable, Fatal)|0011 0011b||

错误信令消息规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，因此 Length 字段被保留。

3. 根复合体将 Error Messages 转换为系统特定的事件。

**Locked Transaction Support.** Unlock Message 用作 PCI 中定义的 Locked transaction 协议的一部分，对于 Legacy Devices 仍然可用。协议以 Memory Read Locked Request 开头。当路径中的端口看到该 Request 时，它们通过锁定其他 Requesters 使用 VC0 直到收到 Unlock Message 来实现原子读‐修改‐写协议。此消息发送到目标以释放路径中的所有端口并完成 Locked Transaction 序列。第 209 页的表 5‐12 总结了该消息的编码。

*Table 5‐12: Unlock Message Coding*

|**Unlock Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Unlock|0000 0000b|011b|

**209**

**PCI Express Technology**

Unlock Message 规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，Length 字段被保留。

**Set Slot Power Limit Message.** 这从 Downstream Port 发送到插入插槽的设备。此功率限制存储在端点中的 Device Capabilities Register 中。表 5‐13 总结了消息编码。

*Table 5‐13: Slot Power Limit Message Coding*

|**Slot Power Limit Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Set_Slot_Power_Limit|0101 0000b|100b|

Set_Slot_Power_Limit 消息规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 数据负载为 1 DW，因此 Length 字段设置为 1。32 位数据负载的低 10 位用于插槽功率缩放；高负载位必须设置为零。

3. 每当数据链路层转换到 DL_Up 状态时，或者在数据链路层已报告 DL_Up 状态时对 Slot Capabilities Register 进行配置写时，此消息都会自动发送。

4. 如果插槽中的卡已经消耗的功率小于指定的功率限制，则允许忽略该 Message。

**Vendor‐Defined Message 0 and 1.** 这些旨在允许通过规范或供应商特定扩展来扩展 PCIe 消息传递能力。它们的头显示在第 211 页的图 5‐12 中，代码在第 211 页的图 5‐14 中给出。

**210**

**Chapter 5: TLP Elements**

*Figure 5‐12: Vendor‐Defined Message Header*

**==> picture [368 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 1Fmt 1  0  r  r  rType R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 1 1 1 1 1 1 x<br>Byte 8 Target BDF if ID Routing used, Vendor ID<br>otherwise Reserved<br>Byte 12 For Vendor Definition<br>**----- End of picture text -----**<br>


*Table 5‐14: Vendor‐Defined Message Coding*

|**Vendor‐Defined Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Vendor Defined Message 0|0111 1110b|000b, 010b,<br>011b, 100b|
|Vendor Defined Message 1|0111 1111b||

供应商定义消息规则：

1. 数据负载可以包含也可以不包含在任一类型中。

2. 消息通过 Vendor ID 字段区分。

3. Attribute 位 [2] 和 [1:0] 不被保留。

4. 如果 Receiver 不识别该 Message：

   - Type 1 Messages 将被静默丢弃

   - Type 0 Messages 将被视为 Unsupported Request 错误情况

**Ignored Messages.** 列出整个要忽略的 Messages 类别在没有上下文的情况下听起来有点奇怪。这些是以前支持在插卡上而不是在系统板上具有热插拔指示器和按钮的设备的 Hot Plug Signaling 消息。此消息类型在规范修订版 1.0a 中定义，但此选项从 1.1 规范发布开始不再受支持，因此此处仅包含详细信息供参考。正如现在名称所暗示的那样，强烈建议 Transmitters 不要发送这些消息，强烈建议 Receivers 在看到这些消息时忽略它们。如果它们仍要被使用，它们必须符合 1.0a 规范细节。

**211**

**PCI Express Technology**

*Table 5‐15: Hot Plug Message Coding*

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Attention_Indicator_On|0100 0001b|100b|
|Attention_Indicator_Blink|0100 0011b|100b|
|Attention_Indicator_Off|0100 0000b|100b|
|Power_Indicator_On|0100 0101b|100b|
|Power_Indicator_Blink|0100 0111b|100b|
|Power_Indicator_Off|0100 0100b|100b|
|Attention_Button_Pressed|0100 1000b|100b|

Hot Plug Message 规则：

- 它们由 Downstream Port 驱动到插槽中的卡。

- Attention Button Message 由插槽设备向上游驱动。

**Latency Tolerance Reporting Message.** LTR Messages 用于可选地报告设备的可接受读/写服务延迟。要了解有关此电源管理技术的更多信息，请参见第 784 页 "LTR (Latency Tolerance Reporting)" 一节。

*Figure 5‐13: LTR Message Header*

**==> picture [346 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1 0 0 0 0<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>**----- End of picture text -----**<br>


**212**

**Chapter 5: TLP Elements**

*Table 5‐16: LTR Message Coding*

|**Latency Tolerance Reporting Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|LTR|0001 0000|100|

LTR Message 规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，Length 字段被保留。

**Optimized Buffer Flush and Fill Messages.** OBFF Messages 用于向 Endpoints 报告平台电源状态并促进更有效的系统电源管理。要了解有关此技术的更多信息，请参见第 776 页 "OBFF (Optimized Buffer Flush and Fill)" 讨论。

*Figure 5‐14: OBFF Message Header*

**==> picture [346 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1  0 0 1 0<br>Byte 8 Reserved<br>OBFF<br>Byte 12 Reserved<br>Code<br>**----- End of picture text -----**<br>


*Table 5‐17: LTR Message Coding*

|**Optimized Buffer Flush/Fill Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|OBFF|0001 0010|100|

**213**

## **PCI Express Technology**

## OBFF Message 规则：

1. 它们必须使用默认流量类 TC0。接收方必须检查此规则并处理违反为 Malformed TLPs。

2. 它们没有数据负载，Length 字段被保留。

3. Requester ID 必须设置为 Transmitting Port 的 ID。

**214**

## _**6**_

## _**Flow Control**_

## **The Previous Chapter**

上一章讨论了三类主要的包：_Transaction Layer Packets_ (TLPs)、_Data Link Layer Packets_ (DLLPs) 和 _Ordered Sets_。本章描述了各种 TLP 的使用、格式和定义以及其相关字段的详细信息。DLLPs 在第 9 章 "DLLP Elements" 中单独描述，位于第 307 页。

## **This Chapter**
