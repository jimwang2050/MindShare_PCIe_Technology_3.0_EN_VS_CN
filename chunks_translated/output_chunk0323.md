|11b|L0s 和 L1 都启用|



_图 16-15：Active State PM Control 字段_

**==> 图片 [296 x 269] 已省略 <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


## **L0s 状态 (L0s State)**

L0s 是一种只能在硬件控制下进入的链路电源状态，并应用于链路的单个方向。例如，传统基于 PC 的系统中的大量流量是由于函数向主系统内存发送数据而产生的。因此，上游 Lane 承载大量流量，而下游 Lane 可能承载很少。这些下游 Lane 可以在空闲总线时段进入 L0s 状态以节省功率。

**744**

**第 16 章：电源管理**

## **进入 L0s (Entry into L0s)**

发送器在检测到实现特定的空闲时间后启动从 L0 到 L0s 的更改。

**进入 L0s.** 进入是基于检测到链路空闲时间段来管理链路的单个方向的。端口需要在检测到不超过 7μs 的空闲时间后进入 L0s。

端点和交换机的空闲定义不同。这样做的原因是希望最小化恢复时间，因为链路恢复时间通过交换机传播。例如，如果交换机上游端口处于低功率状态并且现在看到活动，则意味着 TLP 可能正在向交换机传送。数据包需要路由到哪里？它将转到下游端口之一，但是不是等待接收数据包并确定哪个端口将作为目标然后再开始唤醒它，最低延迟的方法是唤醒所有下游端口，以便最终成为目标的那个端口能够尽快就绪。

关于空闲时间的基本规则：

- **Endpoint Port 或 Root Port**：

   - 没有待发送的 TLP，或者暂时由于缺乏流控信用而被阻止。

   - 没有待发送的 DLLP。

- **Upstream Switch Port**：

   - 所有下游端口的接收 Lane 都已处于 L0s。

   - 没有待发送的 TLP，或者暂时由于缺乏流控信用而被阻止。

   - 没有待发送的 DLLP。

- **Downstream Switch Port**：

   - 交换机的 Upstream Port 的接收 Lane 处于 L0s。

   - 没有待发送的 TLP，或者暂时由于缺乏流控信用而被阻止。

   - 没有待发送的 DLLP

事务层和数据链路层不知道物理层发送器是否已进入 L0s，但触发到 L0s 的转换的空闲条件必须从事务层和链路层连续报告给物理层，以便它可以及时做出有关此的决策。请注意，端口必须始终容忍其接收器上的 L0s，即使软件已禁用 ASPM。这允许链路另一端的启用了 ASPM 的设备仍然将链路的一侧转换为 L0s 状态。

**745**

**PCI Ex ress Technolo p gy**

**必须传送流控信用 (Flow Control Credits Must be Delivered).** 有资格作为空闲时间的一种情况是由于 FC 信用不足而阻止的待处理 TLP。当收到允许传送待处理 TLP 的流控信用时，发送端口必须启动返回 L0。此外，如果与 L0s 中的发送器关联的接收缓冲区使附加的流控信用可用，则发送器必须返回 L0 并将 FC_Update DLLP 传送给邻居。

**发送器启动进入 L0s (Transmitter Initiates Entry to L0s).** 当发送器观察到足够的空闲时间时，它通过向接收器发送"electrical idle"有序集 (EIOS) 并停止传输来强制从 L0 转换到 L0s。发送器和接收器现在处于其电气空闲状态并且已降低功耗。发送器和接收器之间的同步已丢失，并且将需要重新训练以进行恢复。规范要求接收器中的 PLL 逻辑必须保持活动（通电），以允许从 L0s 快速恢复到 L0。

## **退出 L0s 状态 (Exit from L0s State)**

如果发送器检测到空闲条件不再成立，则它必须启动从 L0s 到 L0 的退出。规范鼓励设计人员监视给出 L0s 退出即将发生的早期指示的事件，并启动恢复过程以加速转换回 L0。例如，如果端口的接收器收到 non-posted 请求，则发送器知道它很快将被要求发送完成作为响应。因此，发送器可以提前开始退出过程，以便在被要求传送完成时链路状态是 L0。

**发送器启动 L0s 退出 (Transmitter Initiates L0s Exit).** 要退出 L0s，发送器发送一个或多个 Fast Training Sequence (FTS) 有序集。链路伙伴的接收器所需的这些数量在链路训练期间较早传达（训练中使用的 TS1 和 TS2 中的 N_FTS 字段）。在发送所请求数量的 FTS 后，传送一个 SOS。接收器应该能够建立位锁定和符号锁定或块锁定，并应准备好恢复正常操作。

**接收 L0s 退出的交换机采取的操作 (Actions Taken by Switches that Receive L0s Exit).** 在一个端口上接收到 L0s 到 L0 转换序列的交换机也可能需要对其其他端口启动 L0s 退出。考虑以下两种具体情况：

- **Switch Downstream Port 接收 L0s 到 L0 转换.** 交换机必须在其上游端口上发出 L0s 到 L0 的信号（如果它当前处于 L0s 状态），因为从端点或下游交换机上来的数据包很可能需要向上游复合体发送。

**746**

**第 16 章：电源管理**

- **Switch Upstream Port 接收 L0s 到 L0 转换.** 交换机必须对当前处于 L0s 状态的所有下游端口发出 L0s 到 L0 的转换信号，因为它不想等到数据包到达才开始唤醒目标路径。

由软件对设备电源状态的更改而置于 L1 的交换机端口保持不受 L0s 到 L0 转换的影响。但是，一旦上游链路已完成到 L0 的转换，随后的事务可能以此端口为目标，导致从 L1 到 L0 的转换。

## **L1 ASPM 状态 (L1 ASPM State)**

可选的 L1 ASPM 状态提供比 L0s 更深的节能，但具有更大的恢复延迟。此状态导致链路的两个方向都进入 L1 状态，并导致每个设备内的链路和事务层停用。

通过上游端口（例如来自端点或交换机的上游端口）请求进入此状态（上游端口如图 16-16 所示带阴影）。下游端口响应此请求，并通过与下游组件的协商过程同意进入 L1 或拒绝该请求。退出 L1 ASPM 可以由下游或上游端口启动。

_图 16-16：仅上游端口启动 L1 ASPM_

**747**

**PCI Ex ress Technolo p gy**

## **下游组件决定进入 L1 ASPM (Downstream Component Decides to Enter L1 ASPM)**

规范并未精确定义端点或交换机的上游端口决定尝试进入 L1 ASPM 状态的所有条件，但确实建议一种情况可能是当链路的两侧都处于 L0s 状态达到预设时间量时。给出的要求包括：

- 支持并启用 ASPM L1 进入

- 已满足进入 L1 的设备特定要求

- 没有待发送的 TLP

- 没有待发送的 DLLP

- 如果下游组件是交换机，则在交换机上游端口可以启动 L1 进入之前，交换机的所有下游端口必须处于 L1 或更高的节能状态。

## **进入 L1 ASPM 所需的协商 (Negotiation Required to Enter L1 ASPM)**

由于从 L1 ASPM 恢复需要更长的延迟，因此采用协商过程以确保链路另一端的端口启用了 L1 ASPM 并准备好进入它。协商涉及发送几个数据包：

- PM_Active_State_Request_L1 DLLP — 由下游端口发出以启动协商过程。

- PM_Request_Ack DLLP — 当上游端口满足其进入 L1 ASPM 的所有要求时由上游端口返回。

- PM_Active_State_Nak 消息 TLP — 当上游端口无法进入 L1 ASPM 状态时由上游端口返回。

上游组件可能接受或可能不接受到 L1 ASPM 状态的转换。以下场景描述了导致两种条件的各种情况。

## **场景 1：两个端口都准备好进入 L1 ASPM 状态 (Scenario 1: Both Ports Ready to Enter L1 ASPM State)**

图 16-17 在第 750 页总结了必须发生以启用到 L1 ASPM 状态转换的事件序列。本场景假设两个方向上的所有事务都已完成，并且在新事务要求出现之前不出现。

**下游组件请求 L1 状态 (Downstream Component Requests L1 State).** 如果下游组件希望转换为 L1 状态，则它可以在完成以下步骤后发送进入 L1 的请求：

**748**

**第 16 章：电源管理**

1. TLP 调度在事务层被阻止。

2. 链路层已收到先前发送的最后一个 TLP 的确认，并且重放缓冲区为空。

3. 足够的流控信用可用，以允许为任何 FC 类型发送最大可能的数据包。这确保组件可以在退出 L1 状态后立即发出 TLP。

然后下游组件传送 PM_Active_State_Request_L1 以通知上游组件请求进入 L1 状态。这将被重复发送，直到上游组件响应 — 要么是 PM_Request_ACK DLLP，要么是 PM_Active_State_NAK 消息。

**上游组件对 L1 ASPM 请求的响应 (Upstream Component Response to L1 ASPM Request).** 下游端口（即面向下游的上游组件的端口）必须接受进入低功耗 L1 状态的请求（如果所有以下条件都为真）：

- 该端口支持 ASPM L1 进入并已启用

- 没有 TLP 调度用于传输

- 没有 Ack 或 Nak DLLP 调度用于传输

**上游组件确认进入 L1 的请求 (Upstream Component Acknowledges Request to Enter L1).** 上游

组件发送 PM_Request_ACK 以通知下游组件其同意在以下操作后进入 L1 ASPM 状态：

1. 阻止任何新 TLP 的调度。

2. 收到先前发送的最后一个 TLP 的确认（意味着其重放缓冲区为空）。

3. 确保有足够的流控信用可用于发送任何 FC 类型的最大可能的数据包，以便它可以在退出 L1 状态后立即发出 TLP。

然后上游组件连续发送 PM_Request_Ack，直到它在其接收 Lane 上检测到 EIOS，表明下游设备已进入电气空闲。

**下游组件看到确认 (Downstream Component Sees Acknowledgement).** 当下游组件看到 PM_Request_Ack 时，它停止发送 PM_Active_State_Request_L1，禁用 DLLP 和 TLP 传输，发送 EIOS 并将其发送 Lane 置于电气空闲。

**上游组件接收电气空闲 (Upstream Component Receives Electrical Idle).** 当上游组件接收到 EIOS 时，它停止发送 PM_Request_Ack DLLP，

**749**

**PCI Ex ress Technolo p gy**

禁用 DLLP 和 TLP 传输，发送 EIOS 并将其自己的发送 Lane 置于电气空闲。

_图 16-17：进入 L1 Active State PM 所需的协商序列_

**==> 图片 [371 x 344] 已省略 <==**
