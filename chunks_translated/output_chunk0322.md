**Gen3 模式编码 (Gen3 Mode Encoding).** 对于 Gen3 模式，EIOS 是一个 Ordered Set 块，由 Ordered Set Sync Header (01b) 后跟 16 个字节（均为 66h）组成，如图 16-10 在第 737 页所示。奇怪的是，如果发送器将直接进入电气空闲但不要求完成块，则允许在 Symbol 13 后停止（在 Symbol 14 或 15 中的任何位置）。原因是允许内部时钟因 128b/130b 编码而与 Symbol 边界不一致的情况。此截断不会在接收器处引起问题，因为它只需要看到 EIOS 的 Symbol 0-3 即可识别它。

_图 16-10：Gen3 模式 EIOS 模式_

**==> 图片 [110 x 153] 已省略 <==**

**----- Start of picture text -----**<br>
EIOS<br>Sync Header 01<br>Byte 0 01100110<br>1 01100110<br>2 01100110<br>3 01100110<br>4 01100110<br>13 01100110<br>14 01100110<br>15 01100110<br>**----- End of picture text -----**<br>


**737**

**PCI Ex ress Technolo p gy**

## **发送器退出电气空闲 (Transmitter Exit from Electrical Idle)**

当发送器被指示退出电气空闲时，它采取的步骤取决于正在使用的数据速率（见下文）。但是，它必须在不到 8ns 的时间内通过发送 FTS 或 TS1/TS2 恢复传输，导致转换回 L0 全开状态。

**Gen1 模式.** 对于 2.5 GT/s，该过程很简单：它开始使用有效的差分信号发送 TS1 或 FTS，这些将用于通知接收方有关更改。接收方检测到电压高于 squelch 阈值并开始评估传入信号。

**Gen2 模式.** 当使用 5.0 GT/s 时，信号变化非常快，以至于它们没有时间达到更高的电压电平。这使得快速检测电压何时变化回操作值变得更加困难。为了使这更容易，定义了 EIEOS (Electrical Idle Exit Ordered Set) 以提供较低频率的序列。第 739 页的图 16-11 中所示的用于 8b/10b 编码的 EIEOS 使用重复的 K28.7 控制字符显示为 5 个 1 后跟 5 个 0 的重复字符串。这提供了允许更容易看到更高信号电压的低频信号。事实上，规范规定此模式保证接收器将正确检测电气空闲的退出，这是加扰数据无法做到的。EIEOS 将在以下条件下发送：

- 在进入 Configuration.Linkwidth.Start 或 Recovery.RcvrLock 状态后的第一个 TS1 之前。

- 在 Configuration.Linkwidth.Start、Recovery.RcvrLock 或 Recovery.RcvrCfg 状态下发送每 32 个 TS1 或 TS2 之后。在 Recovery.RcvrCfg 状态下发送 EIEOS 或接收到第一个 TS2 时，TS1/TS2 计数被重置为零。

**738**

**第 16 章：电源管理**

_图 16-11：Gen1/Gen2 模式 EIEOS 符号模式_

**==> 图片 [100 x 150] 已省略 <==**

**----- Start of picture text -----**<br>
EIEOS<br>Symbol 0 K28.5<br>1 K28.7<br>2 K28.7<br>3 K28.7<br>4 K28.7<br>13 K28.7<br>14 K28.7<br>15 D10.2<br>**----- End of picture text -----**<br>


**Gen3 模式.** 8 GT/s 速率也需要 EIEOS，原因与 5.0 GT/s 相同。不过现在，Ordered Set 采用块的形式，如图 16-12 在第 740 页所示。像以前一样，它在 00h 和 FFh 的交替字节中给出低频模式，显示为 8 个零后跟 8 个 1 的重复字符串。

此外，发送 EIEOS 是为了允许 LTSSM Recovery 状态期间的接收方建立块锁定，之后链路转换为 L0 状态。请参见第 411 页的"Block Alignment"部分和第 438 页的"Achieving Block Alignment"部分。

在 Gen3 模式下，EIEOS 将在以下情况发送：

- 在进入 Configuration.Linkwidth.Start 或 Recovery.RcvrLock 状态后的第一个 TS1 之前。

- 在 EDS Framing Token 之后当数据流结束且未发送 EIOS 且 LTSSM 未进入 Recovery.RcvrLock 时。

- 发送 TS1 或 TS2 时每 32 个 TS1/TS2 之后。在以下情况下，计数被重置为零：

- 

   - 发送了 EIEOS

- 在 Recovery.RcvrCfg 或 Configuration.Complete LTSSM 状态下接收到第一个 TS2

- 在均衡序列的阶段 2 中的下游端口，或在阶段 3 中的上游端口，收到两个设置了 Reset EIEOS Interval Count 位的 TS1。

**739**

**PCI Ex ress Technolo p gy**

- 在均衡序列期间每 2[16] 个 TS1 之后，如果 Reset EIEOS Interval Count 位已阻止其发送。规范规定，允许设计通过在加扰 LFSR 与其种子值匹配后的 2 个 TS1 内发送 EIEOS 来满足此要求。

- 作为 FTS 序列、Compliance Pattern 或 Modified Compliance 模式的一部分。

_图 16-12：128b/130b EIEOS 块_

**==> 图片 [138 x 176] 已省略 <==**

**----- Start of picture text -----**<br>
EIEOS<br>Sync Header 01<br>Byte 0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


## **接收器进入电气空闲 (Receiver Entry to Electrical Idle)**

当发送器进入电气空闲时，链路伙伴的接收器根据数据速率进行响应，如以下各节所述。收到 EIOS 通知接收器即将发生这种情况，使其准备检测实际发生的情况。当接收器检测到此条件时，它会停止错误逻辑以防止报告由链路上不可靠活动引起的错误，并启动其电气空闲退出检测器，以便在发送器再次开始发送数据时准备好恢复正常活动。有两种电气空闲检测选项：

**检测电气空闲电压 (Detecting Electrical Idle Voltage).** 一旦收到 EIOS，预期发送器将很快停止传输。在 1.x 规范版本中，接收器通过观察传入电压已降至有效信号阈值以下来检测到这一点。在 2.5 GT/s 时这并不太困难，但它需要消耗空间和功率的 squelch 检测电路。

**740**

**第 16 章：电源管理**

**推断电气空闲 (Inferring Electrical Idle).** 然而，在较高频率下，信号变得越来越衰减，使得 squelch 检测逻辑难以区分电平。对于 8.0 GT/s 尤其如此，预期接收器可能需要在内部执行均衡以恢复良好的信号。为了缓解这些检测问题，2.0 规范引入了允许接收器推断链路何时进入电气空闲条件而不是测试电压电平的概念。在此模型中，缺少预期事件用于指示链路不在发信号，因此可以假定处于电气空闲，如表 16-17 所列。解释一下，Flow Control Updates 在链路处于 L0 时应定期到达，并且 SOS 也以某些时定期出现。为简单起见，允许接收器检查这些条件中的一个或另一个或两者。在链路训练期间，TS1 和 TS2 应定期到达，因此它们的缺席也可以被解释为链路处于空闲。对于表中的最后两行，可能根本未接收到 Symbol，这也将被理解为链路处于空闲。由于电气空闲是针对整个链路而不是独立针对 Lane 进行的，因此不需要每个 Lane 测量这些时间。相反，LTSSM 可以仅对该链路上所有 Lane 共同使用一个计时器。

_表 16-17：电气空闲推断条件_

|State|2.5GT/s|5.0 GT/s|8.0 GT/s|
|---|---|---|---|
|L0|在 128μs 窗口中缺少 FC Update 或 SOS|||
|Recovery.RcvrCfg|在 1280 UI 间隔中缺少 TS1 或 TS2||在 4ms 窗口中缺少 TS1 或 TS2|
|Recovery.Speed<br>(successful_speed_<br>negotiation = 1b)|在 1280 UI 间隔中缺少 TS1 或 TS2||在 4680 UI 间隔中缺少 TS1 或 TS2|
|Recovery.Speed<br>(successful_speed_<br>negotiation = 0b)|在 2000 UI 间隔中缺少电气空闲退出|在 16000 UI 间隔中缺少电气空闲退出||
|Loopback.Active<br>(as a slave)|在 128μs 窗口中缺少电气空闲退出|N/A|N/A|



**741**

**PCI Ex ress Technolo p gy**

接收器如何识别 EIOS 也取决于编码方案。对于 Gen1/Gen2 模式，当接收器看到三个 IDL 符号中的两个时，它会识别 EIOS。对于 Gen3 模式，当传入块的 Symbol 0-3 与 EIOS 模式匹配时，它会被识别。

## **接收器退出电气空闲 (Receiver Exit from Electrical Idle)**

接收器检测电压差异以表示恢复正常信令。当差分峰峰值电压超过电气空闲检测阈值时，将检测到电气空闲退出，对于所有数据速率，该阈值允许设置在 65 和 175mV 之间。

在 2.5 GT/s 时不需要任何其他操作，但在较高数据速率下，接收器不必依赖此检测电路，除非在某些 LTSSM 状态下接收 EIEOS 或在 5.0 GT/s 下 FTS 序列传输之前的四个 EIE 符号期间。为便于检测电气空闲退出而发送的 EIEOS 的数量和时序取决于链路状态。有关详细信息，请参见第 735 页的"活动状态电源管理 (ASPM)"。

在电气空闲期间，接收器的 PLL 失去时钟同步。当发送器退出电气空闲时，它会发送 FTS 以退出 L0s，或发送 TS1/TS2 以退出所有其他链路状态。这样做提供了 CDR 逻辑所需的转换密度，以重新同步接收器 PLL 并实现位锁定和符号锁定或块对齐。

图 16-13 说明链路状态转换并突出显示 L0、L0s 和 L1 之间的转换。请注意，从 L0s 到 L1 没有直接路径，因此必须将链路返回到 L0 状态才能在它们之间进行更改。

_图 16-13：ASPM 链路状态转换_

**==> 图片 [274 x 157] 已省略 <==**

**----- Start of picture text -----**<br>
L0<br>L2/L3<br>L0s L1 Recovery LDn<br>Ready<br>L2 L3<br>**----- End of picture text -----**<br>


**742**

**第 16 章：电源管理**

Link Capability 寄存器指定设备对活动状态电源管理 (Active State Power Management) 的支持。图 16-14 说明此寄存器中的 _ASPM Support_ 字段。在早期规范版本中，并非所有 4 个选项都可用，但 2.1 规范填补了所有这些选项。请注意，位 22 指示是否所有选项都可用。

_图 16-14：ASPM Support_

**==> 图片 [360 x 188] 已省略 <==**

**----- Start of picture text -----**<br>
Link Capabilities Register<br>31 24 23 22 21 20 19 18 17 1514 12 11 10 9 4 3 0<br>Port Number<br>ASPM Optionality<br>Compliance<br>0  0 No ASPM Support<br>0  1 L0s Supported<br>1  0 L1 Supported<br>1  1 L0s & L1 supported<br>Active State PM Support<br>**----- End of picture text -----**<br>


软件可以通过 Link Control 寄存器的 _Active State PM Control_ 字段启用和禁用 ASPM，如图 16-15 在第 744 页所示。可能的设置列于第 743 页的表 16-18 中。注：规范建议对用于等时事务的路径中的所有组件禁用 ASPM，如果与 ASPM 相关的额外延迟超过等时事务的限制。

_表 16-18：Active State Power Management Control 字段定义_

|**Setting**|**Description**|
|---|---|
|00b|L0s 和 L1 ASPM 禁用|
|01b|L0s 启用，L1 禁用|



**743**

**PCI Ex ress Technolo p gy**

_表 16-18：Active State Power Management Control 字段定义（续）_

|**Setting**|**Description**|
|---|---|
|10b|L1 启用，L0s 禁用|
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
