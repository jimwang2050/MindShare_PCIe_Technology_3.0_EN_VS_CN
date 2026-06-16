请考虑以下示例，展示从 PCIe 设备结构中移除参考时钟和电源所需的握手序列。本例假设正在发起系统范围的断电，但该序列也适用于单个设备。步骤如下汇总，并在第 766 页的图 16-26 中显示。整个序列由标记为 A 和 B 的两部分表示。完整序列中涉及的链路状态转换包括：

- L0 ‐‐> L1（当软件将设备置于 D3 时）

- L1 ‐‐> L0（当软件发起 PME_Turn_Off 消息时）

- L0 ‐‐> L2/L3 Ready（由 PME_Turn_Off 握手序列的完成引起，最终结果是由设备发送 PM_Enter_L23 DLLP，且链路进入电气空闲）

以下步骤详细描述了图 16-26（见第 766 页）中所示的序列。

1. 电源管理软件首先将 PCIe 结构中的所有 Function 置于其 D3 状态。

2. 当所有设备进入 D3 时，它们将其 Link 转换到 L1 状态。

3. 电源管理软件发起 PME_Turn_Off TLP 消息，

**764**

**第 16 章：电源管理**

该消息从所有根复合体端口广播到所有设备。这可以防止 PME 消息在上游进行时丢失。注意，此 TLP 的传递会导致每条 Link 转换回 L0，以便它可以向下游转发。

4. 所有设备必须通过在 D3 状态下返回 PME_TO_ACK TLP 消息来接收并确认 PME_Turn_Off 消息。

5. 交换机从其所有启用的下游端口收集 PME_TO_ACK 消息，并仅向上游向根复合体转发一个聚合的 PME_TO_ACK 消息。这是因为这些消息的路由属性设置为"Gather and Route to the Root"（收集并路由到根）。

6. 在发送 PME_TO_ACK 之后，当设备准备好移除参考时钟和电源时，设备会重复发送 PM_Enter_L23 DLLP，直到收到 PM_Request_ACK DLLP。最后进入 L2/L3 Ready 状态的 Link 是那些连接到发起 PME_Turn_Off 消息的设备（本例中为根复合体）的 Link。

7. 当所有 Link 都已转换到 L2/L3 状态时（但不早于此后 100ns），最终可以移除参考时钟和电源。如果为设备提供辅助电源（VAUX），则 Link 转换到 L2。如果没有 AUX 电源可用，则 Link 将处于 L3 状态。

**765**

## **PCI Ex ress Technolo p gy**

_图 16-26：进入 L2/L3 Ready 状态的协商_

**==> picture [298 x 479] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>1. 软件先前已将所有 Function 置于 D3 状态， 2. 软件生成 PME_Turn_Off<br>所有都已按要求将其 Link 转换到 L1。 广播消息以临时禁用<br>PME 消息。<br>L1 State    L0 State<br>PM State D3 (F) 3. 当 PME_Turn_Off 消息到达<br>下游根端口和每个交换机的下游端口时，<br>Switch 必须发生 L1 到 L0 的转换以<br>传输消息。<br>L1 State    L0 State<br>L1 State    L0 State<br>PM State D3 PM State L1   L0 PM State D3<br>PCIe D3 (C) PCIe<br>5. 交换机等待所有下游 Endpoint Switch Endpoint<br>端口都已发送其 ACK 消息。(D) (E)<br>然后它们向上游返回单个聚合消息。<br>L1 State    L0 State L1 State    L0 State<br>PM State D3 4. 每个设备都收到PCI_Turn_Off Message<br>PCI_Turn_Off 消息并发送PCI-XP PCIe PM State D3<br>A Endpoint PME_TO_ACK 消息。 Endpoint PME_Turn_Off Message<br>(A) (B)<br>PME_TO_ACK Message<br>Root Complex<br>8. 当连接到发起 PME_Turn_Off 的设备的所有<br>Link 都已进入 L2/L3 Ready 状态时，可以移除<br>参考时钟和电源，但不早于在所有 Link 上观察到<br>L2/L3 Ready 后 100ns。 L0 State    L2/L3 Ready State<br>PM State D3 (F)<br>Switch<br>L0 State    L2/L3 Ready State L0 State    L2/L3 Ready State<br>PM State D3 PM State PM State D3<br>6. 在每个下游组件发送 PCIe D3 (C) PCIe<br>PCI_TO_ACK 后，它们重复发送 PM_Enter_L23 DLLP，<br>直到收到 PME_Request_Ack。这导致 Endpoint(D) Switch 7. 交换机等待所有下游端口都<br>下游设备发出电气空闲有序集， 已转换到 L2/L3 Ready 状态，<br>之后它进入空闲。上游设备检测到电气空闲，然后才向上游发送 PM_Enter_L23 DLLP<br>并也进入空闲。该 Link 现在处于 L1/L3 Ready 状态。Endpoint(E)<br>L0 State    L2/L3 Ready State L0 State    L2/L3 Ready State<br>PM State D3 PM State D3<br>PCIe PCIe<br>B Endpoint Endpoint PM_Enter_L23 DLLP<br>(A) (B)<br>**----- End of picture text -----**<br>


**766**

**第 16 章：电源管理**

## **退出 L2/L3 Ready 状态 — 时钟和电源被移除**

如图 16-27 中的状态图所示，当电源被移除时，设备退出 L2/L3 Ready 状态，只有两个选择。当 VAUX 可用时，转换为 L2；否则转换为 L3。

链路状态转换通常由物理层中的 LTSSM 控制。但是，到 L2 和 L3 的转换是由于主电源被移除而产生的，并且 LTSSM 在那时不工作。因此，规范将 L2 和 L3 称为伪状态 (pseudo-states)，用于解释当电源被移除时设备的最终状况。

_图 16-27：电源被移除时从 L2/L3 Ready 的状态转换_

## **L2 状态**

一些设备被设计为监视外部事件并发起唤醒序列以恢复电源来处理这些事件。由于主电源已被移除，这些设备将需要 VAUX 之类的电源才能监视事件并发出唤醒信号。

## **L3 状态**

在此状态下，设备没有电源，因此无法通信。从此状态恢复需要系统恢复电源和参考时钟。这会导致设备经历基本复位，之后它们需要由软件初始化以恢复正常操作。

**767**

**PCI Ex ress Technolo p gy**

## **链路唤醒协议和 PME 生成**

唤醒协议提供了一种方法，使端点能够重新激活上游 Link 并请求软件将其返回到 D0，以便它可以执行所需的操作。PCIe PM 旨在与 PCI-PM 软件兼容，尽管方法不同。

PCIe 设备不使用边带信号，而是使用带内 PME 消息来通知 PM 软件设备需要返回到 D0。生成 PME 消息的能力可以在任何低功耗状态下可选地支持。回想一下，设备报告它支持的用于 PME 消息传递的 PM 状态。

PME 消息只能在 Link 状态为 L0 时传递。重新激活 Link 所涉及的延迟基于设备的 PM 和 Link 状态，但可能包括以下内容：

1. Link 处于不可通信状态 (L2) — 当 Link 处于 L2 状态时，由于参考时钟和主电源已被移除，因此无法通信。在时钟和电源恢复、断言基本复位以及 Link 重新训练之前，无法发送任何 PME 消息。当设备发出唤醒信号时，将触发这些事件。这可能导致需要通信的设备与根复合体之间的路径上的所有 Link 都被重新唤醒。

2. Link 处于可通信状态 (L1) — 当 Link 处于 L1 状态时，时钟和主电源仍处于活动状态；因此，设备只需退出 L1 状态，进入 Recovery 状态以重新训练 Link，并将 Link 返回到 L0。一旦 Link 处于 L0，PME 消息就会被传递。注意，设备永远不会在 L2/L3 Ready 状态下发送 PME 消息，因为只有准备好移除时钟和电源时才会进入该状态，PME 通知已经关闭。（参见第 764 页的"L2/L3 Ready 握手序列"。）

3. PME 已传递 (L0) — 如果 Link 处于 L0 状态，则设备将 PME 消息传递给根复合体，通知电源管理软件设备已观察到需要将设备放回其 D0 状态的事件。注意，消息包含设备的请求者 ID（总线号、设备号和功能号）。这可以快速通知软件哪个设备需要服务。

**768**

**第 16 章：电源管理**

## **PME 消息**

PME 消息由支持 PME 通知的设备传递。消息格式如图 16-28（第 769 页）所示。该消息可以由低功耗状态（D1、D2、D3hot 和 D3cold）中的设备发起，并在 Link 返回到 L0 时立即发送。

_图 16-28：PME 消息格式_

**==> picture [366 x 335] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>
Root Complex<br>
PME Switch<br>
Message<br>
PME Message Request TLP<br>
Framing Sequence Framing<br>
Header Digest LCRC<br>
(STP) Number (End)<br>
PCIe<br>
Endpoint<br>
Route to Root Complex<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
Byte 0 0 x 1Fmt 1  0Type 0  0  0 R TC R Attr R HT DT EP Attr0 0 0 0AT Length<br>
Message Code<br>
Byte 4 Requester ID Tag<br>
0001 1000<br>
Byte 8 Reserved<br>
Byte 12 Reserved<br>
**----- End of picture text -----**<br>


**769**

**PCI Ex ress Technolo p gy**

PME 消息是一个事务层数据包，具有以下特征：

- TC 和 VC 都为零（不应用 QoS）

- 隐式路由到根复合体

- 作为 Posted 事务处理

- 不允许使用 Relaxed Ordering，强制 fabric 中信号设备和根复合体之间的所有事务在 PME 消息之前传递到根复合体

## **PME 序列**

设备可以在 PM Capabilities 寄存器中指定的任何低功耗状态下支持 PME。该寄存器还指定了设备在 D3cold 状态下支持唤醒时所使用的 VAUX 电流量。指定与向软件发送 PME 相关的事件的基本序列如下，并假设设备和系统能够生成 PME，并且 Link 已被转换到 L0 状态：

1. 设备在其上游端口上发出 PME 消息。

2. PME 消息被隐式路由到根复合体。路径中的交换机在必要时将其上游端口转换到 L0，并将数据包向上游转发。

3. 根端口接收 PME 并将其转发给电源管理控制器。

4. 控制器通知电源管理软件，通常通过中断。软件使用消息中的请求者 ID 来读取并清除 PMCSR 中的 PME_Status 位，并将设备返回到 D0 状态。根据节能程度，PCI Express 驱动程序可能还需要恢复设备的配置寄存器。

5. PM 软件可能也会调用设备驱动程序，以防设备上下文因被置于低功耗状态而丢失。如果是这样，设备软件将恢复设备内的信息。

## **PME 消息背压死锁避免**

## **背景**

根复合体通常将其收到的 PME 消息存储在一个队列中，并调用 PM 软件来处理每一个。PME 在该队列中保留，

**770**

**第 16 章：电源管理**

直到软件从请求设备的 PMCSR 寄存器读取 PME_Status 位。配置读事务完成后，可以从内部队列中删除此 PME 消息。

## **问题**

如果出现以下情形，则可能发生死锁：

1. 传入的 PME 消息已填满 PME 消息队列，但已有其他 PME 消息从同一根端口向下游发出。

2. PM 软件从根发起一个配置读请求以读取最早 PME 请求者的 PME_Status。
