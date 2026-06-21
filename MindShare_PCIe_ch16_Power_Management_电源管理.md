# 📘 第 16 章　电源管理 (Chapter 16. Power Management)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0323.md` ... `chunks/chunk0331.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [16.1 Power Management — 电源管理](#sec-16-1)
- [16.2 Power Management — 电源管理](#sec-16-2)
- [16.3 Power Management — 电源管理](#sec-16-3)
- [16.4 Power Management — 电源管理](#sec-16-4)
- [16.5 Power Management — 电源管理](#sec-16-5)
- [16.6 Power Management — 电源管理](#sec-16-6)
- [16.7 Power Management — 电源管理](#sec-16-7)
- [16.8 Power Management — 电源管理](#sec-16-8)
- [16.9 Power Management — 电源管理](#sec-16-9)

<a id="sec-16-1"></a>
## 16.1 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

|11b|Both L0s and L1 enabled|


_Figure 16‐15: Active State PM Control Field_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **L0s State** 

L0s is a Link power state that can only be entered under hardware control and is applied to a single direction of the Link. For example, a
large volume of traffic in conventional PC‐based systems results from Functions sending data to main system memory. As a result, the
upstream lanes carry heavy traffic while the downstream lanes may carry very little. These downstream lanes can enter the L0s state to
conserve power during stretches of idle bus time.

## **Entry into L0s** 

A Transmitter initiates a change from L0 to L0s after detecting a period of idle time that is implementation specific. 

**Entry into L0s.** Entry is managed for a single direction of the Link based on detecting a period of Link idle time. Ports are required to
enter L0s after detecting idle time of no greater than 7μs.

Idle is defined differently for Endpoints and Switches. The reason for this is a desire to minimize recovery time as Link recovery time
propagates through Switches. For example, if a Switch upstream port was in a low power state and now sees activity, it means that a TLP is
probably on its way down to the Switch. Where will the packet need to be routed? It will go to one of the downstream ports, but rather than
wait to receive the packet and determine which port will be the target before starting to wake it up, the lowest‐latency approach would be
to wake all the downstream ports so that the one that turns out to be the target will be ready as quickly as possi‐ ble.

Basic rules regarding idle time: 

- **Endpoint Port or Root Port** : 

 - No TLPs are pending transmission or a lack of Flow Control credits is temporarily blocking them. 

 - No DLLPs are pending transmission. 

- **Upstream Switch Port** : 

 - The receive lane of all downstream ports are already in L0s. 

 - No TLPs are pending transmission or a lack of Flow Control credits is temporarily blocking them. 

 - No DLLPs are pending transmission. 

- **Downstream Switch Port** : 

 - The Switch’s Upstream Port’s Receive Lanes are in L0s. 

 - No TLPs are pending transmission or a lack of Flow Control credits is temporarily blocking them. 

 - No DLLPs are pending for transmission 

The Transaction and Data Link Layers are unaware of whether the Physical Layer transmitter has entered L0s, but the idle conditions that
trigger a tran‐ sition to L0s must be continuously reported from the Transaction and Link layers to the Physical Layer so it can make timely
choices about this. Note that a port must always tolerate L0s on its receiver, even if software has dis‐ abled ASPM. This allows a device at
the other end of the Link that is enabled for ASPM to still transition one side of the Link to the L0s state.

**Flow Control Credits Must be Delivered.** One situation that qualifies as idle time is a pending TLP that is blocked due to insufficient
FC credits. When flow control credits are received that allow delivery of the pending TLP, the transmitting port must initiate a return to
L0. Also, if the receive buffer associated with the transmitter in L0s makes additional flow control credits available, the transmitter must
return to L0 and deliver the FC_Update DLLP to the neighbor.

**Transmitter Initiates Entry to L0s.** When sufficient idle time has been observed by a Transmitter, it forces a transition from L0 to L0s
by sending an “electrical idle” ordered set (EIOS) to the receiver and stopping transmission. The transmitter and receiver are now in their
electrical idle states and have reduced power consumption. Synchronization between the trans‐ mitter and receiver has been lost and
retraining will be required for recov‐ ery. The spec requires that the PLL logic in the receiver must remain active (powered) to allow quick
recovery from L0s back to L0.

## **Exit from L0s State** 

If the transmitter detects that the idle condition is no longer true, it must initiate the exit from L0s to L0. The spec encourages
designers to monitor events that give an early indication that an L0s exit is imminent and start the recovery pro‐ cess to speed up the
transition back to L0. For example, if the Receiver of the port receives a non‐posted Request, the Transmitter knows that it will soon be
asked to send a Completion in response. Consequently, the Transmitter can go ahead and start the exit process so the Link state is L0 by the
time it is asked to deliver the Completion.

**Transmitter Initiates L0s Exit.** To exit L0s, the Transmitter sends one or more Fast Training Sequence (FTS) Ordered Sets. The number of
these required by the Link partner’s Receiver was communicated earlier during Link training (N_FTS field in the TS1s and TS2s used in
training). After sending the requested number of FTSs, one SOS is delivered. The receiver should be able to establish bit lock and symbol
lock or Block lock, and should be ready to resume normal operation.

**Actions Taken by Switches that Receive L0s Exit.** A switch that receives an L0s to L0 transition sequence on one port may also need to
ini‐ tiate an L0s exit to other of its ports. Two specific cases are considered:

- **Switch Downstream Port Receives L0s to L0 transition.** The switch must signal an L0s to L0 on its upstream port if it is currently in
the L0s state because the packet coming up from the Endpoint or downstream switch will most likely need to go upstream to the Root Complex.

- **Switch Upsteam Port Receives L0s to L0 transition.** The switch must signal an L0s to L0 transition on all downstream ports currently in
the L0s state because it doesn’t want to wait until the packet arrives to begin waking the target path.

Switch ports that were put into L1 by a software change to the device power state remain unaffected by L0s to L0 transitions. However, once
the upstream Link has completed the transition to L0, a subsequent transaction may target this port, causing a transition from L1 to L0.

## **L1 ASPM State** 

The optional L1 ASPM state provides deeper power savings than L0s, but has a greater recovery latency. This state results in both directions
of the Link going into the L1 state and results in Link and Transaction layer deactivation within each device.

Entry into this state is requested by an upstream port, such as from an Endpoint or the upstream port of a switch (upstream ports are shaded
as shown in Figure 16‐16). The downstream port responds to this request and either agrees to go into L1 or rejects the request through a
negotiation process with the down‐ stream component. Exiting L1 ASPM can be initiated by either the downstream or upstream port.

_Figure 16‐16: Only Upstream Ports Initiate L1 ASPM_ 

## **Downstream Component Decides to Enter L1 ASPM** 

The spec does not precisely define all conditions under which an Endpoint or upstream port of a switch decides to attempt entry into the L1
ASPM state but does suggest that one case might be when both sides of the Link have been in L0s for a preset amount of time. The
requirements given include:

- ASPM L1 entry is supported and enabled 

- Device‐specific requirements for entering L1 have been satisfied 

- No TLPs are pending transmission 

- No DLLPs are pending transmission 

- If the downstream component is a switch, then all of the switch’s down‐ stream ports must be in the L1 or higher power conservation state
before the upstream port can initiate L1 entry.

## **Negotiation Required to Enter L1 ASPM** 

Because of the longer latency required to recover from L1 ASPM, a negotiation process is employed to ensure that the port at the other end
of the Link is enabled for L1 ASPM and is prepared to enter it. The negotiation involves send‐ ing several packets:

- PM_ Active_State_Request_L1 DLLP — issued by the downstream port to start the negotiation process. 

- PM_ Request_Ack DLLP — returned by the upstream port when all of its requirements to enter L1 ASPM have been satisfied. 

- PM_Active_State_Nak message TLP — returned by the upstream port when it is unable to enter the L1 ASPM state. 

The upstream component may or may not accept the transition to the L1 ASPM state. The following scenarios describe a variety of
circumstances that result in both conditions.

## **Scenario 1: Both Ports Ready to Enter L1 ASPM State** 

Figure 16‐17 on page 750 summarizes the sequence of events that must occur to enable transition to the L1 ASPM state. This scenario assumes
that all transac‐ tions have completed in both directions and no new transaction requirements emerge during the negotiation.

**Downstream Component Requests L1 State.** If the downstream com‐ ponent wishes to transition to the L1 state, it can send the request to
enter L1 after the following steps have completed:

1. TLP scheduling is blocked at the Transaction Layer. 

2. The Link Layer has received acknowledgement for the last TLP it had previously sent and the replay buffer is empty. 

3. Sufficient flow control credits are available to allow transmission of the largest possible packet for any FC type. This ensures that the
compo‐ nent can issue a TLP immediately upon exiting the L1 state.

The downstream component then delivers the PM_ Active_State_Request_L1 to notify the upstream component of the request to enter the L1
state. This is sent repeatedly until the upstream component responds — either a PM_Request_ACK DLLP or a PM_Active_State_NAK message.

**Upstream Component Response to L1 ASPM Request.** Down‐ stream ports (i.e., ports of an upstream component that face downward) must accept
a request to enter a low power L1 state if all of the following conditions are true:

- The Port supports ASPM L1 entry and is enabled to do so 

- No TLP is scheduled for transmission 

- No Ack or Nak DLLP is scheduled for transmission 

**Upstream Component Acknowledges Request to Enter L1.** The 

upstream component sends a PM_Request_ACK to notify the downstream component of its agreement to enter the L1 ASPM state after it: 

1. Block scheduling of any new TLPs. 

2. Receive acknowledgement for the last TLP previously sent (meaning its replay buffer is empty). 

3. Ensure enough flow control credits are available to send the largest possible packet for any FC type so that it can issue a TLP
immediately after exiting the L1 state.

The Upstream component then sends PM_Request_Ack continuously until it detects the EIOS on its receive lanes, indicating that the downstream
device has entered Electrical Idle.

**Downstream Component Sees Acknowledgement.** When the Down‐ stream component sees the PM_Request_Ack, it stops sending the
PM_Active_State_Request_L1, disables DLLP and TLP transmission, sends the EIOS and places its transmit lanes into Electrical Idle.

**Upstream Component Receives Electrical Idle.** When the Upstream component receives the EIOS, it stops sending the PM_Request_Ack DLLP, 

disables DLLP and TLP transmission, sends EIOS and places its own trans‐ mit lanes into Electrical Idle. 

_Figure 16‐17: Negotiation Sequence Required to Enter L1 Active State PM_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

</td>
<td width="50%">

|11b|L0s 和 L1 都启用|


_图 16-15：Active State PM Control 字段_

**==> 图片 [296 x 269] 已省略 <==**


## **L0s 状态 (L0s State)**

L0s 是一种只能在硬件控制下进入的链路电源状态，并应用于链路的单个方向。例如，传统基于 PC 的系统中的大量流量是由于函数向主系统内存发送数据而产生的。因此，上游 Lane 承载大量流量，而下游 Lane 可能承载很少。这些下游 Lane 可以在空闲总线时段进入 L0s
状态以节省功率。

**第 16 章：电源管理**

## **进入 L0s (Entry into L0s)**

发送器在检测到实现特定的空闲时间后启动从 L0 到 L0s 的更改。

**进入 L0s.** 进入是基于检测到链路空闲时间段来管理链路的单个方向的。端口需要在检测到不超过 7μs 的空闲时间后进入 L0s。

端点和交换机的空闲定义不同。这样做的原因是希望最小化恢复时间，因为链路恢复时间通过交换机传播。例如，如果交换机上游端口处于低功率状态并且现在看到活动，则意味着 TLP
可能正在向交换机传送。数据包需要路由到哪里？它将转到下游端口之一，但是不是等待接收数据包并确定哪个端口将作为目标然后再开始唤醒它，最低延迟的方法是唤醒所有下游端口，以便最终成为目标的那个端口能够尽快就绪。

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

事务层和数据链路层不知道物理层发送器是否已进入 L0s，但触发到 L0s 的转换的空闲条件必须从事务层和链路层连续报告给物理层，以便它可以及时做出有关此的决策。请注意，端口必须始终容忍其接收器上的 L0s，即使软件已禁用 ASPM。这允许链路另一端的启用了 ASPM
的设备仍然将链路的一侧转换为 L0s 状态。

**必须传送流控信用 (Flow Control Credits Must be Delivered).** 有资格作为空闲时间的一种情况是由于 FC 信用不足而阻止的待处理 TLP。当收到允许传送待处理 TLP 的流控信用时，发送端口必须启动返回 L0。此外，如果与 L0s
中的发送器关联的接收缓冲区使附加的流控信用可用，则发送器必须返回 L0 并将 FC_Update DLLP 传送给邻居。

**发送器启动进入 L0s (Transmitter Initiates Entry to L0s).** 当发送器观察到足够的空闲时间时，它通过向接收器发送"electrical idle"有序集 (EIOS) 并停止传输来强制从 L0 转换到
L0s。发送器和接收器现在处于其电气空闲状态并且已降低功耗。发送器和接收器之间的同步已丢失，并且将需要重新训练以进行恢复。规范要求接收器中的 PLL 逻辑必须保持活动（通电），以允许从 L0s 快速恢复到 L0。

## **退出 L0s 状态 (Exit from L0s State)**

如果发送器检测到空闲条件不再成立，则它必须启动从 L0s 到 L0 的退出。规范鼓励设计人员监视给出 L0s 退出即将发生的早期指示的事件，并启动恢复过程以加速转换回 L0。例如，如果端口的接收器收到 non-posted
请求，则发送器知道它很快将被要求发送完成作为响应。因此，发送器可以提前开始退出过程，以便在被要求传送完成时链路状态是 L0。

**发送器启动 L0s 退出 (Transmitter Initiates L0s Exit).** 要退出 L0s，发送器发送一个或多个 Fast Training Sequence (FTS) 有序集。链路伙伴的接收器所需的这些数量在链路训练期间较早传达（训练中使用的 TS1
和 TS2 中的 N_FTS 字段）。在发送所请求数量的 FTS 后，传送一个 SOS。接收器应该能够建立位锁定和符号锁定或块锁定，并应准备好恢复正常操作。

**接收 L0s 退出的交换机采取的操作 (Actions Taken by Switches that Receive L0s Exit).** 在一个端口上接收到 L0s 到 L0 转换序列的交换机也可能需要对其其他端口启动 L0s 退出。考虑以下两种具体情况：

- **Switch Downstream Port 接收 L0s 到 L0 转换.** 交换机必须在其上游端口上发出 L0s 到 L0 的信号（如果它当前处于 L0s 状态），因为从端点或下游交换机上来的数据包很可能需要向上游复合体发送。

**第 16 章：电源管理**

- **Switch Upstream Port 接收 L0s 到 L0 转换.** 交换机必须对当前处于 L0s 状态的所有下游端口发出 L0s 到 L0 的转换信号，因为它不想等到数据包到达才开始唤醒目标路径。

由软件对设备电源状态的更改而置于 L1 的交换机端口保持不受 L0s 到 L0 转换的影响。但是，一旦上游链路已完成到 L0 的转换，随后的事务可能以此端口为目标，导致从 L1 到 L0 的转换。

## **L1 ASPM 状态 (L1 ASPM State)**

可选的 L1 ASPM 状态提供比 L0s 更深的节能，但具有更大的恢复延迟。此状态导致链路的两个方向都进入 L1 状态，并导致每个设备内的链路和事务层停用。

通过上游端口（例如来自端点或交换机的上游端口）请求进入此状态（上游端口如图 16-16 所示带阴影）。下游端口响应此请求，并通过与下游组件的协商过程同意进入 L1 或拒绝该请求。退出 L1 ASPM 可以由下游或上游端口启动。

_图 16-16：仅上游端口启动 L1 ASPM_

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

**下游组件看到确认 (Downstream Component Sees Acknowledgement).** 当下游组件看到 PM_Request_Ack 时，它停止发送 PM_Active_State_Request_L1，禁用 DLLP 和 TLP 传输，发送 EIOS
并将其发送 Lane 置于电气空闲。

**上游组件接收电气空闲 (Upstream Component Receives Electrical Idle).** 当上游组件接收到 EIOS 时，它停止发送 PM_Request_Ack DLLP，

禁用 DLLP 和 TLP 传输，发送 EIOS 并将其自己的发送 Lane 置于电气空闲。

_图 16-17：进入 L1 Active State PM 所需的协商序列_

**==> 图片 [371 x 344] 已省略 <==**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0806_img1_tight.png" alt="Figure from page 806" width="700">

<a id="sec-16-2"></a>
## 16.2 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Scenario 2: Upstream Component Transmits TLP Just Prior to Receiving L1 Request** 

This scenario presumes that the upstream component has just been instructed by its core logic to send a TLP downstream before it receives
the request to enter L1 from the downstream device. Several negotiation rules define the actions to ensure that this situation is managed
correctly.

**TLP Must Be Accepted by Downstream Component.** Note that after the downstream device sends the PM_Active_State_L1 DLLP it must wait for a
response from the upstream component. While waiting, the down‐ stream component must be able to accept TLPs and DLLPs from the upstream
device. Although it won’t send any TLPs, it must be able to send DLLPs as needed, such as ACKs for incoming TLPs. In this case, two possi‐
bilities exist:

- an ACK is returned to verify successful receipt of the TLP. 

- a NAK is returned if a TLP transmission error is detected. The resulting retry of the TLP is allowed during the L1 negotiation. 

**Upstream Component Receives Request to Enter L1.** The spec requires that the upstream component immediately accept or reject the request
to enter the L1 state. However, it further states that prior to sending a PM_Request_ACK it must:

1. Block scheduling of new TLPs 

2. Wait for acknowledgement of the last TLP previously sent, if necessary, and retry TLPs that receive a NAK, unless a Link Acknowledgement
timeout condition occurs.

Once all outstanding TLPs have been acknowledged, and all other condi‐ tions are satisfied, the upstream device must return a PM_Request_ACK
DLLP.

## **Scenario 3: Downstream Component Receives TLP During Negotiation** 

During the negotiation sequence the downstream device may be instructed to send a new TLP upstream. However, a device that begins the L1
ASPM negotia‐ tion process must block new TLP scheduling. This prevents a race condition between going into L1 and sending a new TLP that
would prevent entry into L1. Consequently, once the downstream device has scheduled delivery of the PM_Request_L1 it must complete the
transition to L1 if a PM_Request_ACK is received. Sending a new TLP will have to wait until L1 has been entered, after which the device can
initiate a transition from L1 back to L0 to send the TLP.

## **Scenario 4: Upstream Component Receives TLP During Negotiation** 

If the upstream component needs to send a TLP or DLLP after sending the PM_Request_Ack, it must first complete the transition to L1. It can
then initiate a change from L1 to L0 to send the packet.

## **Scenario 5: Upstream Component Rejects L1 Request** 

Figure 16‐18 on page 752 summarizes the negotiation sequence when the upstream component rejects the request to enter the L1 ASPM state. The
negoti‐ ation begins normally as the downstream component requests L1. However, the upstream device returns a PM_Active_State_Nak TLP to
reject the request. The reasons for rejecting the request to enter L1 include:

- L1 ASPM not supported or software has not enabled this feature 

- One or more TLPs are scheduled for transfer across the Link 

- ACK or NAK DLLPs are scheduled for transfer 

Once the rejection message has been sent, the upstream component can con‐ tinue sending TLPs and DLLPs as needed. The rejection tells the
downstream component that L1 is not an option at present, and so it must transition to L0s instead, if possible.

_Figure 16‐18: Negotiation Sequence Resulting in Rejection to Enter L1 ASPM State_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Exit from L1 ASPM State** 

Either component can initiate the transition from L1 back to L0 when it needs to use the Link. The procedure is the same in either case and
doesn’t involve any negotiation. When switches are involved in exiting from L1 the spec requires that other switch ports in the ASPM low
power states must also transition to the L0 state if they are in the possible path of the packet that will be sent. These issues are
discussed in subsequent sections.

**L1 ASPM Exit Signaling.** The spec states that exit from L1 is invoked by exiting electrical idle, which begins by sending TS1s. The
receiving port responds by sending TS1s back to the originating device and the Physical Layer follows its LTSSM protocol to complete the
Recovery state and return the Link to L0. Refer to“Recovery State” on page 571 for details.

**Switch Receives L1 Exit from Downstream Component.** As pic‐ tured in Figure 16‐19, the Switch must respond to L1 exit on the down‐ stream
port by returning TS1s and, within 1μs (from signal L1 Exit downstream), it must also exit L1 on its upstream Link if it was in that state.

## **PCI Express Technology** 

_Figure 16‐19: Switch Behavior When Downstream Component Signals L1 Exit_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


Presumably the reason the downstream component is transitioning back to L0 is because it’s preparing to send a TLP upstream. Since L1 exit
latencies are relatively long, a switch “must not wait until its Downstream Port Link has fully exited to L0 before initiating an L1 exit
transition on its Upstream Port Link.” This prevents accumulated latencies that would otherwise result if all L1 to L0 transitions occurred
in a sequential fashion.

**Switch Receives L1 Exit from Upstream Component.** In this case, the switch must respond with TS1s back upstream, and within 1μs it must
also send TS1s to all downstream ports that are in the L1 ASPM state to return them to L0. As in the previous example, the goal is to
minimize the

overall exit latency of returning to the L0 state for every Link in the path from the initiator to the target of the transaction. Figure
16‐20 on page 755 summarizes these requirements. The Link between Switch F and EndPoint (EP) E is in the L1 state because software put EP E
into the D1 state, which caused the Link to transition to L1. Only Links in the L1 ASPM state are transitioned to L0 as a result of the Root
Complex (RC) initiating the exit from L1 ASPM.

_Figure 16‐20: Switch Behavior When Upstream Component Signals L1 Exit_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **ASPM Exit Latency** 

PCI Express provides mechanisms to ensure that the ASPM exit latencies for L0s and L1 don’t exceed the requirements of the devices. All
devices report their L0s and L1 exit latencies, and Endpoints also report the total acceptable latency they can tolerate for this when
performing accesses to and from the Root Com‐ plex. This acceptable latency is based on the data buffer size within the device. If the chain
of devices that reside between the Endpoint and target device have a total latency that exceeds the acceptable latency reported by the
Endpoint, software can disable ASPM for a given Endpoint.

The exit latencies reported by a device will change depending on whether the devices on each end of a Link share a common reference clock or
not. Conse‐ quently, the Link Status register includes a bit called _Slot Clock_ that specifies whether the component uses an external
reference clock provided by the plat‐ form, or an independent reference clock (perhaps generated internally). Soft‐ ware checks these bits
in devices at both ends of each Link to determine whether they both use it and thus share a common clock. If so, software sets the _Common
Clock_ bit to report this in both devices. Figure 16‐21 on page 757 illus‐ trates the registers and related bit fields involved in managing
the ASPM exit latency.

## **Reporting a Valid ASPM Exit Latency** 

Because the clock configuration affects the exit latency that a device will experi‐ ence, devices must report the source of their reference
clock via the _Slot Clock_ status bit within the Link Status register. This bit is initialized by the component to report the source of its
reference clock. If this bit is set to 1, the clock uses the platform generated reference clock and if it’s cleared (0) an independent clock
is used.

</td>
<td width="50%">

## **场景 2：上游组件在收到 L1 请求前刚发送 TLP**

本场景假设上游组件在其核心逻辑指示下要在收到来自下游设备的 L1 进入请求之前向下游发送一个 TLP。有几条协商规则定义了相关动作，以确保该情形能被正确处理。

**第 16 章：电源管理**

**TLP 必须被下游组件接受。** 注意下游设备在发送 PM_Active_State_L1 DLLP 之后必须等待来自上游组件的响应。在等待期间，下游组件必须能够接受来自上游设备的 TLP 和 DLLP。尽管它不会发送任何 TLP，它必须能够根据需要发送
DLLP，例如对收到的 TLP 进行 ACK。在这种情况下，存在两种可能：

- 返回 ACK 以确认 TLP 已被成功接收。

- 如果检测到 TLP 传输错误，则返回 NAK。对该 TLP 的重试在 L1 协商期间是允许的。

**上游组件收到进入 L1 的请求。** 规范要求上游组件必须立即接受或拒绝该进入 L1 状态的请求。然而规范进一步规定：在发送 PM_Request_ACK 之前，它必须：

1. 阻塞对新 TLP 的调度

2. 等待之前发送的最后一个 TLP 的确认（如果需要），并对收到 NAK 的 TLP 进行重试，除非发生 Link Acknowledgement 超时条件。

一旦所有未完成的 TLP 都已被确认，并且所有其他条件都满足，上游设备必须返回 PM_Request_ACK DLLP。

## **场景 3：下游组件在协商期间收到 TLP**

在协商过程中，下游设备可能会被指示向上游发送一个新的 TLP。然而，开始 L1 ASPM 协商过程的设备必须阻塞新的 TLP 调度。这可以防止进入 L1 和发送新 TLP 之间的竞态条件——后者会阻止进入 L1。因此，下游设备一旦调度了 PM_Request_L1
的发送，如果收到 PM_Request_ACK，就必须完成向 L1 的转换。发送新的 TLP 必须等到已进入 L1 之后，此后设备可以发起从 L1 回到 L0 的转换来发送该 TLP。

## **场景 4：上游组件在协商期间收到 TLP**

如果上游组件在发送 PM_Request_Ack 之后需要发送 TLP 或 DLLP，它必须首先完成向 L1 的转换。然后它可以从 L1 发起变到 L0 的状态变更来发送该包。

## **场景 5：上游组件拒绝 L1 请求**

第 752 页的图 16-18 总结了上游组件拒绝进入 L1 ASPM 状态的请求时的协商序列。当下游组件请求 L1 时，协商正常开始。然而，上游设备返回 PM_Active_State_Nak TLP 来拒绝该请求。拒绝进入 L1 的原因包括：

- 不支持 L1 ASPM 或软件未启用此特性

- 一个或多个 TLP 已被调度以通过该 Link 传输

- ACK 或 NAK DLLP 已被调度以传输

拒绝消息发送后，上游组件可以根据需要继续发送 TLP 和 DLLP。拒绝消息告知下游组件 L1 当前不可用，因此它必须改为转换到 L0s（如果可能）。

_图 16-18：协商序列导致拒绝进入 L1 ASPM 状态_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


**第 16 章：电源管理**

## **退出 L1 ASPM 状态**

任一组件都可以在需要使用该 Link 时发起从 L1 回到 L0 的转换。两种情况下过程相同，且不涉及任何协商。当交换机参与退出 L1 时，规范要求交换机处于 ASPM 低功耗状态的其他端口，如果它们位于将发送包的潜在路径上，也必须转换到 L0 状态。这些问题将在后续章节中讨论。

**L1 ASPM 退出信令。** 规范规定退出 L1 通过退出电气空闲来发起，方法为发送 TS1。接收端口通过回送 TS1 给发起设备作为响应，物理层遵循其 LTSSM 协议以完成 Recovery 状态并将 Link 返回到 L0。有关详细信息，请参见第 571
页的"Recovery State"。

**交换机收到来自下游组件的 L1 退出。** 如图 16-19 所示，交换机必须通过回送 TS1 来响应下游端口上的 L1 退出，并且在 1μs 内（从信号 L1 Exit 下游起），如果其上游 Link 处于该状态，它也必须退出 L1。

## **PCI Express Technology**

_图 16-19：下游组件发出 L1 退出信号时交换机的行为_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


可以推测，下游组件转换回 L0 的原因是它正准备向上游发送 TLP。由于 L1 退出延迟相对较长，交换机"不能等到其下游端口链路完全退出到 L0 之后才在上游端口链路上发起 L1 退出转换。"这可以防止延迟的累积，否则当所有 L1 到 L0 的转换按顺序发生时会造成延迟累积。

**交换机收到来自上游组件的 L1 退出。** 在这种情况下，交换机必须通过向上游回送 TS1 进行响应，并且在 1μs 内还必须向处于 L1 ASPM 状态的所有下游端口发送 TS1，以使它们返回 L0。与上例一样，目标是将发起方与事务目标之间路径上每条 Link 返回 L0
状态的整体退出延迟降至最小。第 755 页的图 16-20 总结了这些要求。Switch F 和端点 (EP) E 之间的 Link 处于 L1 状态，因为软件将 EP E 置于 D1 状态，这导致该 Link 转换到 L1。只有处于 L1 ASPM 状态的 Link
才会因根复合体 (RC) 发起退出 L1 ASPM 而转换到 L0。

_图 16-20：上游组件发出 L1 退出信号时交换机的行为_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **ASPM 退出延迟**

PCI Express 提供了多种机制以确保 L0s 和 L1 的 ASPM 退出延迟不超过设备的要求。所有设备都会报告其 L0s 和 L1
退出延迟，端点还会报告其在访问根复合体时所能容忍的总延迟。该可接受延迟基于设备内的数据缓冲区大小。如果位于端点和目标设备之间的设备链路的总延迟超过了端点所报告的可接受延迟，软件可以为给定的端点禁用 ASPM。

设备所报告的退出延迟将根据 Link 两端的设备是否共享公共参考时钟而变化。因此，Link Status 寄存器包含一个名为 _Slot Clock_ 的位，它指定该组件是使用平台提供的外部参考时钟还是使用独立参考时钟（可能由内部产生）。软件检查每条 Link
两端设备的这些位，以确定它们是否都使用它并因此共享公共时钟。如果是，则软件设置 _Common Clock_ 位以在两个设备中报告此情况。第 757 页的图 16-21 说明了管理 ASPM 退出延迟所涉及的寄存器和相关位字段。

## **报告有效的 ASPM 退出延迟**

由于时钟配置会影响设备经历的退出延迟，设备必须通过 Link Status 寄存器中的 _Slot Clock_ 状态位报告其参考时钟的来源。此位由组件初始化以报告其参考时钟的来源。如果该位置 1，则表示时钟使用平台生成的参考时钟；如果清零（0），则使用独立时钟。

如果系统固件或软件确定 Link 上的两个组件都使用平台时钟，那么两个设备内的参考时钟将同相。这导致从 L0s 和 L1 的退出延迟更短，并在 Link Control 寄存器的 _Common Clock_
字段中报告。然后组件必须更新其报告的退出延迟以反映正确的值。注意，如果时钟不是公共的，则默认值将是正确的，无需进一步操作。

**L0s 退出延迟更新。** L0s 的退出延迟在 Link Capability 寄存器中报告，基于默认假设（即不存在公共时钟实现）。L0s 退出延迟也在 Link 训练期间使用的 TS1 中报告，作为退出 L0s 所需的 FTS 有序集的数量
(N_FTS)。如果软件随后检测到公共时钟实现，则设置 Common Clock 字段并写入 Link Control 寄存器的 _Retrain Link_ 位，以强制 Link 训练重新进行。在重训练期间，将报告新的 N_FTS 值，并在 Link Capability
寄存器的 _L0s Latency_ 字段中报告。

**L1 退出延迟更新。** 在 Link 重训练之后，新的值也将在 _L1 Latency_ 字段中报告。

_图 16-21：用于 ASPM 退出延迟管理和报告的配置寄存器_

## **计算从端点到根复合体的延迟**

第 759 页的图 16-22 展示了一个端点，其事务必须经过两个交换机才能到达根复合体。假设路径中的所有 Link 都处于 L1 状态，我们以端点 B 需要向主存发送数据包为例。

1. 首先，它通过在 T 时刻在其 Link 上发起 TS1 有序集来开始唤醒序列。EP B 的 L1 退出延迟最大为 8μs，但 Switch C 的最大退出延迟为 16μs。因此，该 Link 的退出延迟为 16μs。

2. 在检测到 Link B/C 上的 L1 退出后 1μs 内，Switch C 在 T+1μs 时在 Link C/F 上发出 L1 退出信号。

3. Link C/F 在 16μs 内完成从 L1 的退出，在 T+17μs 时完成。

4. Switch F 在检测到来自 Switch C 的 L1 退出后 1μs 内（T+2μs）向根复合体发出从 L1 退出的信号。

5. Link F/RC 在 8μs 内完成从 L1 的退出，在 T+10μs 完成。

6. 将目标路径转换回 L0 的总延迟 = T+17μs。

**第 16 章：电源管理**

_图 16-22：总 L1 延迟示例_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **软件发起的链路电源管理**

当软件发起配置写以更改电源状态以节能时，设备必须通过将其 Link 转换到相应的低功耗状态来响应。

## **D1/D2/D3 和 L1 状态 Hot**

规范要求，当设备内的所有 Function 已被置于任何低功耗状态（D1、D2 或 D3hot）时，设备必须发起到 L1 状态的转换，如图 16-23 所示。设备因软件发起对设备的配置访问或设备发起的事件而返回 L0。

_图 16-23：软件将设备的电源级别从 D0 更改时设备转换到 L1_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


在收到对 PMCSR 寄存器中 _Power State_ 字段的配置写时，设备通过向上游组件发送 PM_Enter_L1 DLLP 来发起从 L0 到 L1 的更改。

## **进入 L1 状态**

将 Link 置于 L1 状态的过程如图 16-24（见第 762 页）所示。图中的步骤在以下列表中有更详细的描述：

1. 一旦设备识别出其所有 Function 都处于 D2 状态，它必须准备将 Link 转换到 L1。这从阻塞新 TLP 的调度开始。

**第 16 章：电源管理**

2. 来自下游端点的 TLP 在收到进入 D2 的请求之前可能尚未被确认。设备必须在所有未完成的 TLP 都被确认后才能响应更改 Link 电源的请求。换句话说，在进入 L1 状态之前，Replay Buffer 必须为空。

3. 由于返回 Link 到其活动状态的延迟较长，设备必须能够在返回活动状态时立即发送一个最大尺寸的 TLP。由于缺少流控信用可能会阻塞该操作，端点必须在进入 L1 之前累积足够的信用，以允许为每种流控类型发送所支持的最大包。

4. 当上述要求都已满足时，端点向上游设备发送 PM_Enter_L1 DLLP。这指示上游组件将 Link 置于 L1。PM_Enter_L1 被重复发送，直到从上游设备收到 PM_Request_ACK DLLP。

5. 当上游组件收到 PM_Enter_L1 时，它通过执行步骤 6、7 和 8 开始其准备工作。这与下游组件在发出 L1 转换信号之前执行的准备工作相同。

6. 所有新 TLP 的调度被阻塞。

7. 如果之前的 TLP 尚未被确认，上游设备将等待，直到 Replay Buffer 中的所有事务都被确认。

8. 必须积累足够的流控信用以确保可以为每种流控类型发送最大的 TLP。

9. 上游组件发送 PM_Request_ACK DLLP 以确认它已准备好进入 L1 状态。此 DLLP 被重复发送，直到收到 Electrical Idle 有序集，表明它已被接受。

10. 当下游组件收到确认时，它发送 EIOS 并将其发送通道置于电气空闲（发送器处于 Hi-Z 状态）。

11. 上游组件识别 EIOS 并将其发送通道置于电气空闲。该 Link 此时已进入 L1 状态。

_图 16-24：将 Link 从 L0 转换到 L1 状态的过程_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **退出 L1 状态**

L1 状态的退出可以由上游或下游组件发起，如下所述。本节还总结了用于退出 L1 的信令协议。

**上游组件发起。** 软件可能需要使用当前处于低功耗状态的设备，这意味着电源管理软件必须发出一个配置写，以将其电源状态改回 D0。当配置请求准备好从上游组件（根端口或下游交换机端口）发送时，该端口将退出电气空闲状态并发起重新训练以将 Link 返回到

**第 16 章：电源管理**

L0 状态。一旦 Link 处于活动状态，配置写就可以被传送到设备以将其转换回 D0，此时它已准备好供正常使用。

**下游组件发起 L1 到 L0 的转换。** 在 L1 状态下，参考时钟和电源仍会施加到 Link 上的设备。这允许将下游设备设计为监视外部事件，并在发生电源管理事件 (PME) 时触发。在传统的 PCI 中，这是通过边带 PME#
信号报告的，系统板逻辑通常使用它来生成中断以通知 CPU 需要将设备恢复到完全运行状态。PCIe 取消了边带信号，而是发送带内消息来报告 PME（详见第 769 页的"PME Message"）。

**L1 退出协议。** 在 L1 状态下，Link 的两个方向都处于电气空闲状态。设备通过改变电气空闲并发送 TS1 来发出退出 L1 的信号。当 Link 邻居检测到退出电气空闲时，它会回送 TS1。此序列触发两个设备进入 Recovery
状态，当该状态完成其操作后，两个设备都将返回 L0 状态。

## **L2/L3 Ready — 移除链路电源**

一旦软件已将设备内的所有 Function 置于 D3hot 状态，就可以安全地从设备移除电源。一个典型的应用是将系统中的所有设备置于
D3，然后从所有设备移除电源以实现最低功耗。然而，规范并未给出实际用于移除时钟和电源的机制的详细信息，也不要求遵循特定顺序，从而允许各种实现方式。

准备设备以移除电源的状态转换涉及先进入 L1 然后返回 L0 再到达 L2/L3 Ready 状态的预备步骤，如图 16-25（见第 764 页）所示。

_图 16-25：与准备设备以移除参考时钟和电源相关的链路状态转换_

## **L2/L3 Ready 握手序列**

当转换到 L2/L3 Ready 状态时，规范确实要求一个握手序列。这确保了所有设备都准备好移除参考时钟和电源，并且也确保在移除电源时，正在发送到根复合体的带内 PME 消息不会被意外丢失。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0816_img1_tight.png" alt="Figure from page 816" width="700">

<a id="sec-16-3"></a>
## 16.3 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

If system firmware or software determines that both components on the Link use the platform clock then the reference clocks within both
devices will be in phase. This results in shorter exit latencies from L0s and L1, and is reported in the _Common Clock_ field of the Link
Control register. Components must then update their reported exit latencies to reflect the correct value. Note that if the clocks are not
common then the default values will be correct and no further action is required.

**L0s Exit Latency Update.** Exit latency for L0s is reported in the Link Capability register based on the default assumption that a common
clock implementation does not exist. L0s exit latency is also reported in the TS1s

used during Link training as the number of FTS Ordered Sets (N_FTS) required to exit L0s. If software then detects a common clock
implementa‐ tion, it sets the Common Clock field writes to the _Retrain Link_ bit in the Link Control register to force Link training to
repeat. During retraining new N_FTS values are reported and in the _L0s Latency_ field of the Link Capabil‐ ity register.

**L1 Exit Latency Update.** Following Link retraining, new values will also be reported in the _L1 Latency_ field. 

_Figure 16‐21: Config. Registers for ASPM Exit Latency Management and Reporting_ 

## **Calculating Latency from Endpoint to Root Complex** 

Figure 16‐22 on page 759 illustrates an Endpoint whose transactions must trans‐ verse two switches to reach the Root Complex. Presuming that
all Links in the path are in the L1 state, let’s take the example that Endpoint B needs to send a packet to main memory.

1. First, it begins the wake sequence by initiating a TS1 ordered set on its Link at time “T.” The L1 exit latency for EP B is a maximum of
8μs, but Switch C has a maximum exit latency of 16μs. Therefore, the exit latency for this Link is 16μs.

2. Within 1μs of detecting the L1 exit on Link B/C, Switch C signals L1 exit on Link C/F at T+1μs. 

3. Link C/F completes its exit from L1 in 16μs, at T+17μs. 

4. Switch F signals an exit from L1 to the Root Complex within 1μs of detect‐ ing L1 exit from Switch C (T+2μs). 

5. Link F/RC completes exit from L1 in 8μs, completing at T+10μs. 

6. Total latency to transition path to target back to L0 = T+17μs. 

_Figure 16‐22: Example of Total L1 Latency_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Software Initiated Link Power Management** 

When software initiates configuration writes to change the power state for power conservation, devices must respond by transitioning their
Link to the corresponding low power state.

## **D1/D2/D3 and the L1 State Hot** 

The spec requires that when all Functions within a device have been placed into any of the low power states (D1, D2, or D3hot), the device
must initiate a transi‐ tion to the L1 state as shown in Figure 16‐23. A device returns to L0 as a result of software initiating a
configuration access to the device or a device initiated event.

_Figure 16‐23: Devices Transition to L1 When Software Changes their Power Level from D0_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


Upon receiving a configuration write to the _Power State_ field of the PMCSR reg‐ ister, a device initiates the change from L0 to L1 by
sending a PM_Enter_L1 DLLP to the upstream component.

## **Entering the L1 State** 

The procedure to place the Link into an L1 state is illustrated in Figure 16‐24 on page 762. The steps in the figure are described in
greater detail in the following list:

1. Once a device recognizes that all its Functions are in the D2 state, it must prepare to transition the Link into L1. This begins with
blocking new TLPs from being scheduled.

2. A TLP may from the downstream Endpoint may not have been acknowledged prior to receiving the request to enter D2. The device must not
respond to a request to change the Link power until all outstanding TLPs have been acknowledged. In other words, the Replay Buffer must be
empty before proceeding to the L1 state.

3. Because of the long latencies involved in returning the Link to its active state, a device must be able to send a maximum‐sized TLP
immediately upon return to the active state. Since a lack of Flow Control credits could block this, the Endpoint must have sufficient
credits to permit transmission of the biggest packet supported for each Flow Control type before entering L1.

4. When the requirements listed above have been met, the Endpoint sends a PM_Enter_L1 DLLP to the upstream device. This instructs the
upstream component to put the Link into L1. The PM_Enter_L1 is repeated until a PM_Request_ACK DLLP is received from the upstream device.

5. When the upstream component receives PM_Enter_L1, it begins its prepa‐ ration by performing steps 6, 7, and 8. This is the same
preparation as per‐ formed by the downstream component prior to signaling the L1 transition.

6. All new TLP scheduling is blocked. 

7. In the event that a previous TLP has not yet been acknowledged, the upstream device will wait until all transactions in the Replay Buffer
have been acknowledged.

8. Sufficient Flow Control credits must be accumulated to ensure that the larg‐ est TLP can be transmitted for each Flow Control type. 

9. The upstream component sends a PM_Request_ACK DLLP to confirm that it’s ready to enter the L1 state. This DLLP is repeated until an
Electrical Idle ordered set is received, indicating that it’s been accepted.

10. When the downstream component receives the acknowledgement, it sends an EIOS and places its transmit lanes into electrical idle
(transmitter is in Hi‐Z state).

11. The upstream component recognizes the EIOS and places its transmit lanes into electrical idle. The Link has now entered the L1 state. 

_Figure 16‐24: Procedure Used to Transition a Link from the L0 to L1 State_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Exiting the L1 State** 

An exit from the L1 state can be initiated by either the upstream or downstream component, as discussed below. This section also summarizes
the signaling pro‐ tocol used to exit L1.

**Upstream Component Initiates.** Software may need to use a device which is currently in a low‐power state, and that means the Power
Manage‐ ment software must issue a configuration write to change its power state back to D0. When the configuration Request is ready to be
sent from the upstream component (a Root Port or downstream Switch Port) the port will exit the electrical idle state and initiate
re‐training to return the Link to the

L0 state. Once the Link is active, the configuration write can be delivered to the device to transition it back to D0, at which point it’s
ready for normal use.

**Downstream Component Initiates L1 to L0 Transition.** In the L1 state the reference clock and power are still applied to devices on the
Link. That allows a downstream device to be designed to monitor external events and trigger a Power Management Event (PME) when it occurs.
In conven‐ tional PCI, this is reported by a side‐band PME# signal, and system board logic usually uses it to generate an interrupt that
informs the CPU of the need to bring the device back to full operation. PCIe eliminates the side‐ band signal and instead sends an in‐band
message to report the PME (see “The PME Message” on page 769 for details).

**The L1 Exit Protocol.** In the L1 state both directions of the Link are in the electrical idle state. A device signals an exit from L1 by
changing from elec‐ trical idle and sending TS1s. When the Link neighbor detects the exit from electrical idle it sends TS1s back. This
sequence triggers both devices to enter the Recovery state and, when that has completed its operation, both devices will have returned to
the L0 state.

## **L2/L3 Ready — Removing Power from the Link** 

Once software has placed all Functions within a Device into the D3hot state power can be safely removed from the device. A typical
application for this would be to place all devices in the system into D3 and then remove power from them all to achieve the lowest power
consumption. However, the spec does not give details of the actual mechanism that would be used to remove clock and power or require that a
particular sequence be followed, allowing for a variety of implementations.

The state transitions to prepare devices for power removal involve the prelimi‐ nary steps of entering L1 and then returning to L0 before
arriving at the L2/L3 Ready state as illustrated in Figure 16‐25 on page 764.

_Figure 16‐25: Link States Transitions Associated with Preparing Devices for Removal of the Reference Clock and Power_ 

## **L2/L3 Ready Handshake Sequence** 

The spec does require a handshake sequence when transitioning to the L2/L3 Ready state. This ensures that all devices are ready for
reference clock and power removal, and also that inband PME messages being sent to the Root Complex won’t accidentally be lost when power is
removed.

</td>
<td width="50%">

如果系统固件或软件确定 Link 上的两个组件都使用平台时钟，那么两个设备内的参考时钟将同相。这导致从 L0s 和 L1 的退出延迟更短，并在 Link Control 寄存器的 _Common Clock_
字段中报告。然后组件必须更新其报告的退出延迟以反映正确的值。注意，如果时钟不是公共的，则默认值将是正确的，无需进一步操作。

**L0s 退出延迟更新。** L0s 的退出延迟在 Link Capability 寄存器中报告，基于默认假设（即不存在公共时钟实现）。L0s 退出延迟也在

**第 16 章：电源管理**

链路训练期间使用的 TS1 中报告，作为退出 L0s 所需的 FTS 有序集的数量 (N_FTS)。如果软件随后检测到公共时钟实现，则设置 Common Clock 字段并写入 Link Control 寄存器的 _Retrain Link_
位，以强制链路训练重新进行。在重训练期间，将报告新的 N_FTS 值，并在 Link Capability 寄存器的 _L0s Latency_ 字段中报告。

**L1 退出延迟更新。** 在 Link 重训练之后，新的值也将在 _L1 Latency_ 字段中报告。

_图 16-21：用于 ASPM 退出延迟管理和报告的配置寄存器_

## **计算从端点到根复合体的延迟**

第 759 页的图 16-22 展示了一个端点，其事务必须经过两个交换机才能到达根复合体。假设路径中的所有 Link 都处于 L1 状态，我们以端点 B 需要向主存发送数据包为例。

1. 首先，它通过在 T 时刻在其 Link 上发起 TS1 有序集来开始唤醒序列。EP B 的 L1 退出延迟最大为 8μs，但 Switch C 的最大退出延迟为 16μs。因此，该 Link 的退出延迟为 16μs。

2. 在检测到 Link B/C 上的 L1 退出后 1μs 内，Switch C 在 T+1μs 时在 Link C/F 上发出 L1 退出信号。

3. Link C/F 在 16μs 内完成从 L1 的退出，在 T+17μs 时完成。

4. Switch F 在检测到来自 Switch C 的 L1 退出后 1μs 内（T+2μs）向根复合体发出从 L1 退出的信号。

5. Link F/RC 在 8μs 内完成从 L1 的退出，在 T+10μs 完成。

6. 将目标路径转换回 L0 的总延迟 = T+17μs。

**第 16 章：电源管理**

_图 16-22：总 L1 延迟示例_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **软件发起的链路电源管理**

当软件发起配置写以更改电源状态以节能时，设备必须通过将其 Link 转换到相应的低功耗状态来响应。

## **D1/D2/D3 和 L1 状态 Hot**

规范要求，当设备内的所有 Function 已被置于任何低功耗状态（D1、D2 或 D3hot）时，设备必须发起到 L1 状态的转换，如图 16-23 所示。设备因软件发起对设备的配置访问或设备发起的事件而返回 L0。

_图 16-23：软件将设备的电源级别从 D0 更改时设备转换到 L1_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


在收到对 PMCSR 寄存器中 _Power State_ 字段的配置写时，设备通过向上游组件发送 PM_Enter_L1 DLLP 来发起从 L0 到 L1 的更改。

## **进入 L1 状态**

将 Link 置于 L1 状态的过程如图 16-24（见第 762 页）所示。图中的步骤在以下列表中有更详细的描述：

1. 一旦设备识别出其所有 Function 都处于 D2 状态，它必须准备将 Link 转换到 L1。这从阻塞新 TLP 的调度开始。

**第 16 章：电源管理**

2. 来自下游端点的 TLP 在收到进入 D2 的请求之前可能尚未被确认。设备必须在所有未完成的 TLP 都被确认后才能响应更改 Link 电源的请求。换句话说，在进入 L1 状态之前，Replay Buffer 必须为空。

3. 由于返回 Link 到其活动状态的延迟较长，设备必须能够在返回活动状态时立即发送一个最大尺寸的 TLP。由于缺少流控信用可能会阻塞该操作，端点必须在进入 L1 之前累积足够的信用，以允许为每种流控类型发送所支持的最大包。

4. 当上述要求都已满足时，端点向上游设备发送 PM_Enter_L1 DLLP。这指示上游组件将 Link 置于 L1。PM_Enter_L1 被重复发送，直到从上游设备收到 PM_Request_ACK DLLP。

5. 当上游组件收到 PM_Enter_L1 时，它通过执行步骤 6、7 和 8 开始其准备工作。这与下游组件在发出 L1 转换信号之前执行的准备工作相同。

6. 所有新 TLP 的调度被阻塞。

7. 如果之前的 TLP 尚未被确认，上游设备将等待，直到 Replay Buffer 中的所有事务都被确认。

8. 必须积累足够的流控信用以确保可以为每种流控类型发送最大的 TLP。

9. 上游组件发送 PM_Request_ACK DLLP 以确认它已准备好进入 L1 状态。此 DLLP 被重复发送，直到收到 Electrical Idle 有序集，表明它已被接受。

10. 当下游组件收到确认时，它发送 EIOS 并将其发送通道置于电气空闲（发送器处于 Hi-Z 状态）。

11. 上游组件识别 EIOS 并将其发送通道置于电气空闲。该 Link 此时已进入 L1 状态。

_图 16-24：将 Link 从 L0 转换到 L1 状态的过程_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **退出 L1 状态**

L1 状态的退出可以由上游或下游组件发起，如下所述。本节还总结了用于退出 L1 的信令协议。

**上游组件发起。** 软件可能需要使用当前处于低功耗状态的设备，这意味着电源管理软件必须发出一个配置写，以将其电源状态改回 D0。当配置请求准备好从上游组件（根端口或下游交换机端口）发送时，该端口将退出电气空闲状态并发起重新训练以将 Link 返回到

**第 16 章：电源管理**

L0 状态。一旦 Link 处于活动状态，配置写就可以被传送到设备以将其转换回 D0，此时它已准备好供正常使用。

**下游组件发起 L1 到 L0 的转换。** 在 L1 状态下，参考时钟和电源仍会施加到 Link 上的设备。这允许将下游设备设计为监视外部事件，并在发生电源管理事件 (PME) 时触发。在传统的 PCI 中，这是通过边带 PME#
信号报告的，系统板逻辑通常使用它来生成中断以通知 CPU 需要将设备恢复到完全运行状态。PCIe 取消了边带信号，而是发送带内消息来报告 PME（详见第 769 页的"PME Message"）。

**L1 退出协议。** 在 L1 状态下，Link 的两个方向都处于电气空闲状态。设备通过改变电气空闲并发送 TS1 来发出退出 L1 的信号。当 Link 邻居检测到退出电气空闲时，它会回送 TS1。此序列触发两个设备进入 Recovery
状态，当该状态完成其操作后，两个设备都将返回 L0 状态。

## **L2/L3 Ready — 移除链路电源**

一旦软件已将设备内的所有 Function 置于 D3hot 状态，就可以安全地从设备移除电源。一个典型的应用是将系统中的所有设备置于
D3，然后从所有设备移除电源以实现最低功耗。然而，规范并未给出实际用于移除时钟和电源的机制的详细信息，也不要求遵循特定顺序，从而允许各种实现方式。

准备设备以移除电源的状态转换涉及先进入 L1 然后返回 L0 再到达 L2/L3 Ready 状态的预备步骤，如图 16-25（见第 764 页）所示。

_图 16-25：与准备设备以移除参考时钟和电源相关的链路状态转换_

## **L2/L3 Ready 握手序列**

当转换到 L2/L3 Ready 状态时，规范确实要求一个握手序列。这确保了所有设备都准备好移除参考时钟和电源，并且也确保在移除电源时，正在发送到根复合体的带内 PME 消息不会被意外丢失。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0823_img1_tight.png" alt="Figure from page 823" width="700">

<a id="sec-16-4"></a>
## 16.4 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

Consider the following example of the handshake sequence required for remov‐ ing the reference clock and power from PCIe devices in the
fabric. This example assumes a system‐wide power down is being initiated, but the sequence can also apply to individual devices. The steps
are summarized below and shown in Figure 16‐26 on page 766. The overall sequence is represented in two parts labeled A and B. The Link state
transitions involved in the complete sequence include:

- L0 ‐‐> L1 (when software places a device into D3) 

- L1 ‐‐> L0 (when software initiates a PME_Turn_Off message) 

- L0 ‐‐> L2/L3 Ready (resulting from the completion of the PME_Turn_Off handshake sequence, which culminates in a PM_Enter_L23 DLLP being
sent by the device and the Link going to electrical idle)

The following steps detail the sequence illustrated in Figure 16‐26 on page 766. 

1. Power Management software first places all Functions in the PCIe fabric into their D3 state. 

2. All devices transition their Links to the L1 state when they enter D3. 

3. Power Management software initiates a PME_Turn_Off TLP message, 

which is broadcast from all Root Complex ports to all devices. This prevents PME Messages from being lost in case they were in progress
upstream when power was removed. Note that delivery of this TLP causes each Link to transition back to L0 so it can be forwarded downstream.

4. All devices must receive and acknowledge the PME_Turn_Off message by returning a PME_TO_ACK TLP message while in the D3 state. 

5. Switches collect the PME_TO_ACK messages from all of their enabled downstream ports and forward just one aggregated PME_TO_ACK mes‐ sage
upstream toward the Root Complex. That’s because these messages have the routing attribute set as “Gather and Route to the Root”.

6. After sending the PME_TO_ACK, when it is ready to have the reference clock and power removed, devices send a PM_Enter_L23 DLLP repeatedly
until a PM_Request_ACK DLLP is returned. The Links that enter the L2/L3 Ready state last are those attached to the device originating the
PME_Turn_Off message (the Root Complex in this example).

7. The reference clock and power can finally be removed when all Links have transitioned to the L2/L3 state, but not sooner than 100ns after
that. If auxil‐ iary power (VAUX) is supplied to the devices, the Link transitions to L2. If no AUX power is available the Links will be in
the L3 state.

## **PCI Express Technology** 

_Figure 16‐26: Negotiation for Entering L2/L3 Ready State_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Exiting the L2/L3 Ready State — Clock and Power Removed** 

As illustrated in the state diagram in Figure 16‐27, a device exits the L2/L3 Ready state when power is removed and has only two choices.
When VAUX is available the transition is to L2, otherwise the transition is to L3.

Link state transitions are normally controlled by the LTSSM in the Physical Layer. However, transitions to L2 and L3 result from main power
being removed and the LTSSM is not operational then. Consequently, the spec refers to L2 and L3 as pseudo‐states defined for explaining the
resulting condition of a device when power is removed.

_Figure 16‐27: State Transitions from L2/L3 Ready When Power is Removed_ 

## **The L2 State** 

Some devices are designed to monitor external events and initiate a wakeup sequence to restore power to handle them. Since main power is
removed, these device will need a power source like VAUX to be able to monitor the events and to signal a wakeup.

## **The L3 State** 

In this state the device has no power and therefore no means of communication. Recovery from this state requires the system to restore power
and the reference clock. That causes devices to experience a fundamental reset, after which they’ll need be initialized by software to
return to normal operation.

## **Link Wake Protocol and PME Generation** 

The wake protocol provides a method for an Endpoint to reactivate the upstream Link and request that software return it to D0 so it can
perform required operations. PCIe PM is designed to be compatible with PCI‐PM soft‐ ware, although the methods are different.

Rather than using a sideband signal, PCIe devices use an inband PME message to notify PM software of the need to return the device to D0.
The ability to gen‐ erate PME messages may optionally be supported in any of the low power states. Recall that a device reports which PM
states it supports for PME message delivery.

PME messages can only be delivered when the Link state is L0. The latency involved in reactivating the Link is based on a device’s PM and
Link state, but can include the following:

1. Link is in non‐communicating (L2) state — when a Link is in the L2 state it cannot communicate because the reference clock and main power
have been removed. No PME message can be sent until clock and power are restored, a Fundamental Reset is asserted, and the Link is
re‐trained. These events will be triggered when a device signals a wakeup. This may result in all Links being re‐awakened in the path
between the device needing to com‐ municate and the Root Complex.

2. Link is in communicating (L1) state — when a Link is in the L1 state clock and main power are still active; thus, a device simply exits
the L1 state, goes to the Recovery state to re‐train the Link, and returns the Link to L0. Once the Link is in L0 the PME message is
delivered. Note that the devices never send a PME message while in the L2/L3 Ready state because entry into that state only occurs after PME
notification has been turned off, in preparation for clock and power to be removed. (See “L2/L3 Ready Handshake Sequence” on page 764.)

3. PME is delivered (L0) — If the Link is in the L0 state, the device transfers the PME message to the Root Complex, notifying Power
Management soft‐ ware that the device has observed an event that requires the device be placed back into its D0 state. Note that the message
contains the Requester ID (Bus#, Device#, and Function#) of the device. This quickly informs soft‐ ware which device needs service.

## **The PME Message** 

The PME message is delivered by devices that support PME notification. The message format is illustrated in Table 16‐28 on page 769. The
message may be initiated by a device in a low power state (D1, D2, D3hot, and D3cold) and is sent immediately upon return of the Link to L0.

_Figure 16‐28: PME Message Format_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


The PME message is a Transaction Layer Packet that has the following charac‐ teristics: 

- TC and VC are zero (no QoS applies) 

- Routed implicitly to the Root Complex 

- Handled as Posted Transaction 

- Relaxed Ordering is not permitted, forcing all transactions in the fabric between the signaling device and the Root Complex to be
delivered to the Root Complex ahead of the PME message

## **The PME Sequence** 

Devices may support PME in any of the low power states as specified in the PM Capabilities register. This register also specifies the amount
of VAUX current used by the device if it supports wakeup in the D3cold state. The basic sequence of events associated with sending a PME to
software is specified below and pre‐ sumes that the device and system are enabled to generate PME and the Link has already been transitioned
to the L0 state:

1. The device issues the PME message on its upstream port. 

2. PME messages are implicitly routed to the Root Complex. Switches in the path transition their upstream ports to L0 if necessary and
forward the packet upstream.

3. A root port receives the PME and forwards it to the Power Management Controller. 

4. The controller informs power management software, typically with an interrupt. Software uses the Requester ID in the message to read and
clear the PME_Status bit in the PMCSR and return the device to the D0 state. Depending on the degree of power conservation, the PCI Express
driver may also need to restore the devices configuration registers.

5. PM Software may also call the device driver in the event that device context was lost as a result of being placed in a low power state.
If so, device soft‐ ware restores information within the device.

## **PME Message Back Pressure Deadlock Avoidance** 

## **Background** 

The Root Complex typically stores the PME messages it receives in a queue, and calls PM software to handle each one. A PME is held in this
queue until PM soft‐

ware reads the PME_Status bit from the requesting device’s PMCSR register. Once the configuration read transaction completes, this PME
message can be removed from the internal queue.

## **The Problem** 

Deadlock can occur if the following scenario develops: 

1. Incoming PME Messages have filled the PME message queue but other PME messages have been issued downstream from the same root port. 

2. PM software initiates a configuration read request from the Root to read PME_Status from the oldest PME requester.

</td>
<td width="50%">

请考虑以下示例，展示从 PCIe 设备结构中移除参考时钟和电源所需的握手序列。本例假设正在发起系统范围的断电，但该序列也适用于单个设备。步骤如下汇总，并在第 766 页的图 16-26 中显示。整个序列由标记为 A 和 B 的两部分表示。完整序列中涉及的链路状态转换包括：

- L0 ‐‐> L1（当软件将设备置于 D3 时）

- L1 ‐‐> L0（当软件发起 PME_Turn_Off 消息时）

- L0 ‐‐> L2/L3 Ready（由 PME_Turn_Off 握手序列的完成引起，最终结果是由设备发送 PM_Enter_L23 DLLP，且链路进入电气空闲）

以下步骤详细描述了图 16-26（见第 766 页）中所示的序列。

1. 电源管理软件首先将 PCIe 结构中的所有 Function 置于其 D3 状态。

2. 当所有设备进入 D3 时，它们将其 Link 转换到 L1 状态。

3. 电源管理软件发起 PME_Turn_Off TLP 消息，

**第 16 章：电源管理**

该消息从所有根复合体端口广播到所有设备。这可以防止 PME 消息在上游进行时丢失。注意，此 TLP 的传递会导致每条 Link 转换回 L0，以便它可以向下游转发。

4. 所有设备必须通过在 D3 状态下返回 PME_TO_ACK TLP 消息来接收并确认 PME_Turn_Off 消息。

5. 交换机从其所有启用的下游端口收集 PME_TO_ACK 消息，并仅向上游向根复合体转发一个聚合的 PME_TO_ACK 消息。这是因为这些消息的路由属性设置为"Gather and Route to the Root"（收集并路由到根）。

6. 在发送 PME_TO_ACK 之后，当设备准备好移除参考时钟和电源时，设备会重复发送 PM_Enter_L23 DLLP，直到收到 PM_Request_ACK DLLP。最后进入 L2/L3 Ready 状态的 Link 是那些连接到发起 PME_Turn_Off
消息的设备（本例中为根复合体）的 Link。

7. 当所有 Link 都已转换到 L2/L3 状态时（但不早于此后 100ns），最终可以移除参考时钟和电源。如果为设备提供辅助电源（VAUX），则 Link 转换到 L2。如果没有 AUX 电源可用，则 Link 将处于 L3 状态。

## **PCI Express Technology**

_图 16-26：进入 L2/L3 Ready 状态的协商_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


**第 16 章：电源管理**

## **退出 L2/L3 Ready 状态 — 时钟和电源被移除**

如图 16-27 中的状态图所示，当电源被移除时，设备退出 L2/L3 Ready 状态，只有两个选择。当 VAUX 可用时，转换为 L2；否则转换为 L3。

链路状态转换通常由物理层中的 LTSSM 控制。但是，到 L2 和 L3 的转换是由于主电源被移除而产生的，并且 LTSSM 在那时不工作。因此，规范将 L2 和 L3 称为伪状态 (pseudo-states)，用于解释当电源被移除时设备的最终状况。

_图 16-27：电源被移除时从 L2/L3 Ready 的状态转换_

## **L2 状态**

一些设备被设计为监视外部事件并发起唤醒序列以恢复电源来处理这些事件。由于主电源已被移除，这些设备将需要 VAUX 之类的电源才能监视事件并发出唤醒信号。

## **L3 状态**

在此状态下，设备没有电源，因此无法通信。从此状态恢复需要系统恢复电源和参考时钟。这会导致设备经历基本复位，之后它们需要由软件初始化以恢复正常操作。

## **链路唤醒协议和 PME 生成**

唤醒协议提供了一种方法，使端点能够重新激活上游 Link 并请求软件将其返回到 D0，以便它可以执行所需的操作。PCIe PM 旨在与 PCI-PM 软件兼容，尽管方法不同。

PCIe 设备不使用边带信号，而是使用带内 PME 消息来通知 PM 软件设备需要返回到 D0。生成 PME 消息的能力可以在任何低功耗状态下可选地支持。回想一下，设备报告它支持的用于 PME 消息传递的 PM 状态。

PME 消息只能在 Link 状态为 L0 时传递。重新激活 Link 所涉及的延迟基于设备的 PM 和 Link 状态，但可能包括以下内容：

1. Link 处于不可通信状态 (L2) — 当 Link 处于 L2 状态时，由于参考时钟和主电源已被移除，因此无法通信。在时钟和电源恢复、断言基本复位以及 Link 重新训练之前，无法发送任何 PME
消息。当设备发出唤醒信号时，将触发这些事件。这可能导致需要通信的设备与根复合体之间的路径上的所有 Link 都被重新唤醒。

2. Link 处于可通信状态 (L1) — 当 Link 处于 L1 状态时，时钟和主电源仍处于活动状态；因此，设备只需退出 L1 状态，进入 Recovery 状态以重新训练 Link，并将 Link 返回到 L0。一旦 Link 处于 L0，PME
消息就会被传递。注意，设备永远不会在 L2/L3 Ready 状态下发送 PME 消息，因为只有准备好移除时钟和电源时才会进入该状态，PME 通知已经关闭。（参见第 764 页的"L2/L3 Ready 握手序列"。）

3. PME 已传递 (L0) — 如果 Link 处于 L0 状态，则设备将 PME 消息传递给根复合体，通知电源管理软件设备已观察到需要将设备放回其 D0 状态的事件。注意，消息包含设备的请求者 ID（总线号、设备号和功能号）。这可以快速通知软件哪个设备需要服务。

**第 16 章：电源管理**

## **PME 消息**

PME 消息由支持 PME 通知的设备传递。消息格式如图 16-28（第 769 页）所示。该消息可以由低功耗状态（D1、D2、D3hot 和 D3cold）中的设备发起，并在 Link 返回到 L0 时立即发送。

_图 16-28：PME 消息格式_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


PME 消息是一个事务层数据包，具有以下特征：

- TC 和 VC 都为零（不应用 QoS）

- 隐式路由到根复合体

- 作为 Posted 事务处理

- 不允许使用 Relaxed Ordering，强制 fabric 中信号设备和根复合体之间的所有事务在 PME 消息之前传递到根复合体

## **PME 序列**

设备可以在 PM Capabilities 寄存器中指定的任何低功耗状态下支持 PME。该寄存器还指定了设备在 D3cold 状态下支持唤醒时所使用的 VAUX 电流量。指定与向软件发送 PME 相关的事件的基本序列如下，并假设设备和系统能够生成 PME，并且 Link
已被转换到 L0 状态：

1. 设备在其上游端口上发出 PME 消息。

2. PME 消息被隐式路由到根复合体。路径中的交换机在必要时将其上游端口转换到 L0，并将数据包向上游转发。

3. 根端口接收 PME 并将其转发给电源管理控制器。

4. 控制器通知电源管理软件，通常通过中断。软件使用消息中的请求者 ID 来读取并清除 PMCSR 中的 PME_Status 位，并将设备返回到 D0 状态。根据节能程度，PCI Express 驱动程序可能还需要恢复设备的配置寄存器。

5. PM 软件可能也会调用设备驱动程序，以防设备上下文因被置于低功耗状态而丢失。如果是这样，设备软件将恢复设备内的信息。

## **PME 消息背压死锁避免**

## **背景**

根复合体通常将其收到的 PME 消息存储在一个队列中，并调用 PM 软件来处理每一个。PME 在该队列中保留，

**第 16 章：电源管理**

直到软件从请求设备的 PMCSR 寄存器读取 PME_Status 位。配置读事务完成后，可以从内部队列中删除此 PME 消息。

## **问题**

如果出现以下情形，则可能发生死锁：

1. 传入的 PME 消息已填满 PME 消息队列，但已有其他 PME 消息从同一根端口向下游发出。

2. PM 软件从根发起一个配置读请求以读取最早 PME 请求者的 PME_Status。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0826_img1_tight.png" alt="Figure from page 826" width="700">

<a id="sec-16-5"></a>
## 16.5 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

3. The corresponding split completion must push all previously posted PME messages ahead of it based on transaction ordering rules. 

4. The Root Complex cannot accept a new PME message because the queue is full, so the path is temporarily blocked. But that also means that
the read completion can’t reach the Root Complex to clear the older entry in the queue.

5. No progress can be made and deadlock occurs. 

## **The Solution** 

The problem is avoided if the Root Complex always accepts new PME mes‐ sages, even when they would overflow the queue. In this case, the
Root simply discards the later PME messages. To prevent a discarded PME message from being lost permanently, a device that sends a PME
message is required to mea‐ sure a time‐out interval, called the PME Service Time‐out. If the device’s PME_Status bit is not cleared with
100 ms (+ 50%/‐ 5%), it assumes its message must have been lost and it re‐issues the message.

## **The PME Context** 

Devices that generate PME must continue to power portions of the device that are used for detecting, signaling, and handling PME events,
referred to collec‐ tively as the PME context. Devices that support PME in the D3cold state use aux‐ iliary power to maintain the PME
context when the main power is removed. Items that are typically part of the PME context include:

- PME_Status bit (required) — set when a device sends a PME message and cleared by PM software. Devices that support PME in the D3cold state
must implement the PME_Status bit as “sticky,” meaning that the value survives a fundamental reset.

## **PCI Express Technology** 

- PME_Enable bit (required) — this bit must remain set to continue enabling a Function’s ability to generate PME messages and signal wakeup.
Devices that support PME in the D3cold state must implement PME_Enable as “sticky,” meaning that the value survives a fundamental reset.

- Device‐specific status information — for example, a device might preserve event status information in cases where several different types
of events can trigger a PME.

- Application‐specific information — for example, modems that initiate wakeup would preserve Caller ID information if supported. 

## **Waking Non-Communicating Links** 

When a device that supports PME in the D3cold state needs to send a PME mes‐ sage, it must first transition the Link to L0. This is
sometimes referred to as a wakeup. PCI Express defines two methods of triggering the wakeup of non‐communicating Links:

- Beacon — an in‐band indicator driven by AUX power 

- • WAKE# Signal — a sideband signal driven by AUX power 

In both cases, PM software must be notified to restore main power and the ref‐ erence clock. This also causes a fundamental reset that
forces a device into the D0uninitialized state. Once the Link transitions to L0, the device sends the PME message. Since a reset is required
to re‐activate the Link, devices must maintain PME context across the reset sequence described above.

## **Beacon** 

This signaling mechanism is designed to operate on AUX power and doesn’t require much power. The beacon is simply a way of notifying the
upstream component that software should be notified of the wakeup request. When switches receive a beacon on a downstream port, they in turn
signal beacon on their upstream port. Ultimately, the beacon reaches the root complex, where it generates an interrupt that calls PM
software.

Some form‐factors require beacon support for waking the system while others don’t. The spec requires compliance with the form‐factor specs,
and doesn’t require beacon support for devices if their form‐factor doesn’t. However, for “universal” components designed for use in a
variety of form‐factors, beacon support is required. See “Beacon Signaling” on page 483 for details.

## **WAKE#** 

PCI Express provides a sideband signal called WAKE# as a alternative to the beacon that can be routed directly to the Root or to other
system logic to notify PM software. In spite of the desire to minimize the pin count of a Link, the moti‐ vation for adding this extra pin
is easy to understand. The reason is that a com‐ ponent must consume auxiliary power to be able to recognize a beacon on a downstream port
and then forward it to an upstream port. In a battery‐powered system auxiliary power is jealously guarded because it drains the battery even
when the system isn’t doing any work. The preferred solution in that case would be to bypass as many components as possible when delivering
the wakeup notification, and the WAKE# pin serves that purpose very well. On the other hand, if power is not a concern then the WAKE# pin
might be considered less desirable.

A hybrid implementation may also be used. In this case, WAKE# is sent to a switch, which in turn sends the beacon on its upstream port. The
options are illustrated in Figure 16‐29 on page 774 A and B. Note that when asserted, the WAKE# signal remains low until the PME_Status bit
is cleared by software.

This signal must be implemented by ATX or ATX‐based connectors and cards as well as by the mini‐card form factor. No requirement is
specified for embedded devices to use the WAKE# signal.

## **PCI Express Technology** 

_Figure 16‐29: WAKE# Signal Implementations_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Auxiliary Power** 

Devices that support PME in the D3cold state must support the wakeup sequence and are allowed by the PCI‐PM spec to consume the maximum
auxil‐ iary current of 375 mA (otherwise only 20mA). The amount of current they need is reported in the _Aux_Current_ field of the PM
Capability registers. Auxiliary power is enabled when the _PME_Enable_ bit is set within the PMCSR register.

PCI Express extends the use of auxiliary power beyond the limitations given by PCI‐PM. Now, any Device may consume the maximum auxiliary
current if enabled by setting the _Aux Power PM Enable_ bit of the Device Control register, illustrated in Figure 16‐30 on page 775. This
gives devices the opportunity to support other things like SM Bus while in a low power state. As in PCI‐PM the amount of current consumed by
a device is reported in the _Aux_Current_ field in the PMC register.

_Figure 16‐30: Auxiliary Current Enable for Devices Not Supporting PMEs_ 

|||15|14|12|11|10|9|8|7|5|4|3|2|1|0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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


## **Improving PM Efficiency** 

## **Background** 

As processors and other system components acquire better power management mechanisms, peripherals like PCIe components start to appear as a
bigger con‐ tributor to power consumption in PC systems. Earlier generations of PCIe allowed some software and hardware power management,
but coordinating PM decisions with the system was not a high priority and consequently soft‐ ware visibility and control was limited.

One problem that can arise from this lack of coordination happens when the system goes into a sleep state but the devices remain
operational. Such devices can initiate interrupts or DMA traffic that would require the system to wake up to handle them, even thought they
were low‐priority events, and thus defeat the goal of power conservation.

It can also happen that the system is unaware of how long the devices can afford to wait from the time they request system service (like a
memory read) until they get a response. Without that information, software is often forced to assume that the response time must always be
minimal and therefore power management policies can’t afford enough time to do much. However, if the sys‐ tem was aware of time windows when
a fast response was not needed, it could be more aggressive with power management and stay in a low power state for a longer time without
risking performance problems. The 2.1 spec revision added two new features to address these problems.

## **OBFF (Optimized Buffer Flush and Fill)** 

The first of these mechanisms is Optimized Buffer Flush and Fill, which pro‐ vides a mechanism for Endpoints to be made aware of the system
power state and therefore the best times to do data transfers to and from the system.

## **The Problem** 

The problem with bus‐master capable devices is that if they’re not aware of the system power status, they may initiate transactions at times
when it would be better to wait. The diagram in Figure 16‐31 on page 777 illustrates the problem in simple terms: there are many components
initiating events and as a result,

the times without activity when the system is idle and can go to sleep are few and short‐lived. In contrast, Figure 16‐32 on page 777
illustrates an improve‐ ment in which the same events are grouped and serviced together so that the times when the system is idle enough to
go to sleep are both more frequent and of longer duration. Clearly, this would result in better power conservation and fortunately, it’s not
difficult to implement. PCIe components simply need to understand what they should do based on the system power state, and they’ll need a
way to learn what that state currently is.

_Figure 16‐31: Poor System Idle Time_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


_Figure 16‐32: Improved System Idle Time_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **The Solution**

</td>
<td width="50%">

3. 相应的拆分完成必须基于事务排序规则将其之前的所有已发布 PME 消息推到其前面。

4. 根复合体无法接受新的 PME 消息，因为队列已满，因此路径被临时阻塞。但这也意味着读完成无法到达根复合体以清除队列中较旧的条目。

5. 没有任何进展，发生死锁。

## **解决方案**

如果根复合体始终接受新的 PME 消息，即使它们会使队列溢出，则可以避免此问题。在这种情况下，根只是丢弃后来的 PME 消息。为防止被丢弃的 PME 消息永久丢失，发送 PME 消息的设备必须测量一个称为 PME Service Time-out 的超时间隔。如果设备的
PME_Status 位未在 100ms (+ 50%/‐ 5%) 内被清除，则它假定其消息必定已丢失并重新发出该消息。

## **PME 上下文**

生成 PME 的设备必须继续为设备中用于检测、发信号和处理 PME 事件的部分供电，这些部分统称为 PME 上下文。支持 D3cold 状态下 PME 的设备在主电源被移除时使用辅助电源来维护 PME 上下文。PME 上下文中通常包括的项目：

- PME_Status 位（必需）— 在设备发送 PME 消息时设置，由 PM 软件清除。支持 D3cold 状态下 PME 的设备必须将 PME_Status 位实现为"粘性"，这意味着该值在基本复位后仍然存在。

## **PCI Express Technology**

- PME_Enable 位（必需）— 该位必须保持置位以继续启用 Function 生成 PME 消息和发出唤醒信号的能力。支持 D3cold 状态下 PME 的设备必须将 PME_Enable 实现为"粘性"，这意味着该值在基本复位后仍然存在。

- 设备特定的状态信息 — 例如，设备可能在有多种不同类型的事件可以触发 PME 的情况下保留事件状态信息。

- 应用程序特定的信息 — 例如，启动唤醒的调制解调器在支持时会保留来电显示信息。

## **唤醒不可通信链路**

当支持 D3cold 状态下 PME 的设备需要发送 PME 消息时，它必须首先将 Link 转换到 L0。这有时称为唤醒。PCI Express 定义了触发不可通信链路唤醒的两种方法：

- Beacon — 由 AUX 电源驱动的带内指示符

- WAKE# 信号 — 由 AUX 电源驱动的边带信号

在这两种情况下，都必须通知 PM 软件以恢复主电源和参考时钟。这也会导致基本复位，迫使设备进入 D0uninitialized 状态。一旦 Link 转换到 L0，设备就会发送 PME 消息。由于需要复位才能重新激活 Link，设备必须跨上述复位序列维护 PME 上下文。

## **Beacon**

此信令机制被设计为在 AUX 电源上工作，且不需要太多电力。Beacon 仅仅是通知上游组件软件应被通知唤醒请求的一种方式。当交换机在下游端口上收到 beacon 时，它们会依次在其上游端口上发出 beacon。最终，beacon 到达根复合体，在那里它生成一个调用 PM
软件的中断。

某些外形尺寸要求 beacon 支持唤醒系统，而其他外形尺寸则不需要。规范要求符合外形尺寸规范，并且如果其外形尺寸不需要 beacon 支持，则不需要设备支持 beacon。但是，对于设计用于各种外形尺寸的"通用"组件，则需要 beacon 支持。有关详细信息，请参见第 483
页的"Beacon Signaling"。

**第 16 章：电源管理**

## **WAKE#**

PCI Express 提供了一个名为 WAKE# 的边带信号作为 beacon 的替代方案，可以直接路由到根或其他系统逻辑以通知 PM 软件。尽管希望最小化链路的引脚数，但添加此额外引脚的动机很容易理解。原因是组件必须消耗辅助电源才能识别下游端口上的
beacon，然后将其转发到上游端口。在电池供电的系统中，辅助电源受到严格保护，因为它即使在系统不工作时也会消耗电池电量。在这种情况下，首选的解决方案是在传递唤醒通知时绕过尽可能多的组件，而 WAKE# 引脚正好可以很好地满足此目的。另一方面，如果不担心功耗，那么 WAKE#
引脚可能就不那么理想了。

也可以使用混合实现。在这种情况下，WAKE# 被发送到交换机，而交换机又在其上游端口上发送 beacon。这些选项如图 16-29（第 774 页 A 和 B）所示。注意，当断言时，WAKE# 信号保持低电平，直到软件清除 PME_Status 位。

此信号必须由 ATX 或基于 ATX 的连接器以及插卡以及小型插卡外形尺寸实现。对于嵌入式设备使用 WAKE# 信号没有规定要求。

## **PCI Express Technology**

_图 16-29：WAKE# 信号实现_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


**第 16 章：电源管理**

## **辅助电源**

支持 D3cold 状态下 PME 的设备必须支持唤醒序列，并被 PCI-PM 规范允许消耗最大辅助电流 375mA（否则只能消耗 20mA）。它们所需的电流量在 PM Capability 寄存器的 _Aux_Current_ 字段中报告。当 PMCSR 寄存器中的
_PME_Enable_ 位被设置时，启用辅助电源。

PCI Express 扩展了辅助电源的使用，超出了 PCI-PM 给出的限制。现在，任何设备都可以在通过设置设备控制寄存器的 _Aux Power PM Enable_ 位启用时消耗最大辅助电流，如图 16-30（第 775 页）所示。这使设备有机会在低功耗状态下支持 SM
Bus 等其他功能。与 PCI-PM 中一样，设备消耗的电流量在 PMC 寄存器的 _Aux_Current_ 字段中报告。

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

## **提高 PM 效率**

## **背景**

随着处理器和其他系统组件获得更好的电源管理机制，像 PCIe 组件这样的外围设备开始成为 PC 系统中较大的功耗贡献者。早期的 PCIe 几代允许一些软件和硬件电源管理，但与系统的 PM 决策协调并不是高优先级的，因此软件可见性和控制是有限的。

缺乏协调可能导致的一个问题是，当系统进入睡眠状态但设备仍保持运行状态时。这些设备可以发起中断或 DMA 流量，从而需要系统唤醒以处理它们，即使它们是低优先级事件，因此破坏了节能的目标。

系统也可能不知道设备在请求系统服务（如内存读取）到收到响应之间可以等待多长时间。如果不知道该信息，软件通常被迫假设响应时间必须始终最小，因此电源管理策略无法承担足够的时间来做更多工作。但是，如果系统知道何时不需要快速响应的时间窗口，则可以更积极地进行电源管理，并在不冒性能风险的情况下在低功耗状态下停留更长时间。2.1
规范修订版增加了两个新特性来解决这些问题。

## **OBFF（优化的缓冲区刷新与填充）**

第一个机制是优化缓冲区刷新和填充（Optimized Buffer Flush and Fill），它提供了一种机制，使端点能够了解系统电源状态，从而了解与系统进行数据传输的最佳时间。

## **问题**

能够进行总线主控的设备的问题在于，如果它们不了解系统电源状态，它们可能会在最好等待的时候发起事务。第 777 页的图 16-31 中的图示以简单的术语说明了该问题：有许多组件发起事件，因此，

**第 16 章：电源管理**

系统空闲且可以进入睡眠的时间很少且很短。相比之下，第 777 页的图 16-32 展示了一种改进，其中相同的事件被分组并一起处理，从而使系统空闲到足以进入睡眠的时间更频繁且持续时间更长。显然，这将带来更好的节能效果，而且幸运的是，实现起来并不困难。PCIe
组件只需了解它们应根据系统电源状态做什么，并且它们需要一种方法来了解当前的状态。

_图 16-31：较差的系统空闲时间_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


_图 16-32：改进后的系统空闲时间_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **解决方案**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0841_img1_tight.png" alt="Figure from page 841" width="700">

<a id="sec-16-6"></a>
## 16.6 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

OBFF is an optional hint that a system can use to inform components about optimal time windows for traffic. It’s just a hint, though, so
bus‐master‐capable devices can still initiate traffic whenever they like. Of course, power consump‐ tion will be negatively affected if they
do, so overriding the OBFF hints should be avoided as much as possible. The information is communicated in one of two ways: by sending
messages to the Endpoints or by toggling the WAKE# pin. If both options are available, using the pin is strongly recommended because it
avoids the counter‐productive step of using excess power, possibly across sev‐ eral Links, to inform a component about the current system
power state. In fact, the OBFF message should only be used if the WAKE# pin is not available.

Figure 16‐33 on page 778 gives an example showing a mix of both communica‐ tion types. Using the pin is required if it’s available, but in
this example it’s not an option between the two switches. To work around this problem, the upper switch can translate the state received on
the WAKE# pin into a message going downstream. It should perhaps be noted here that switches are strongly encour‐ aged to forward all OBFF
indications downstream but not required to do so. It may be necessary, especially when using messages, to discard or collapse some
indications and that is permitted.

_Figure 16‐33: OBFF Signaling Example_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


**Using the WAKE# Pin.** This pin, previously only used to inform the sys‐ tem that a component needed to have power restored, is given an
extra meaning as the simplest and lowest‐power option for communicating sys‐ tem power status to PCIe components. It’s optional, and the
protocol is fairly simple: the WAKE# pin toggles to communicate the system state. As seen in Figure 16‐34 on page 779, there are several
transitions but only three states, which are described below:

1. CPU Active ‐ system awake; all transactions OK. This is every compo‐ nent’s initial state. 

2. OBFF ‐ system memory path available; transfers to and from memory are OK, but other transactions should wait for a higher power state. 

3. Idle ‐ wait for a higher state before initiating. 

_Figure 16‐34: WAKE# Pin OBFF Signaling_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


When the CPU Active or OBFF state is indicated, it’s recommended that the platform not return to the Idle state for at least 10  s so as to
give compo‐ nents enough time to deliver the packets they may have been queuing up while in the previous Idle state. However, since that
timing isn’t required, it’s also recommended that Endpoints not assume they’ll have a certain amount of time in a CPU Active or OBFF window.
Along the same lines, the platform is allowed to indicate that it’s going to Idle before it actually does

## **PCI Express Technology** 

so as to give components advance notice that it’s time to finish. The case this early notice is specifically designed to avoid is having an
Endpoint start a transfer just as the platform goes to Idle, causing an immediate exit from the Idle state. The spec strongly recommends
that this should be the only reason for an early indication of the Idle state and also that this advance notice time should be as short as
possible.

Interestingly, the WAKE# pin can still be used for its original purpose of allowing a component to wake the system, and it’s no surprise
that this might confuse other components that are monitoring that pin for OBFF information. That could result in sub‐optimal behavior in
power or perfor‐ mance, but this is considered a recoverable situation so no steps were taken to guard against it. To cover all of these
cases, any time the signal is unclear the default state will be CPU Active.

**Using the OBFF Message.** As mentioned earlier, OBFF information can be communicated using a message, although it’s recommend that this
only be used if the WAKE# pin is not available. These messages only flow down‐ stream from the Root. The message contents are shown in
Figure 16‐35 on page 781, including the Routing type 100b (point‐to‐point) and an OBFF Code that gives the following values (all other codes
are reserved):

1. 1111b ‐ CPU Active 

2. 0001b ‐ OBFF 

3. 0000b ‐ Idle 

If a reserved code is received, components must treat it as “CPU Active.” If a Port receives an OBFF message but doesn’t support OBFF or
hasn’t enabled it yet, it must treat it as an Unsupported Request (Completion sta‐ tus UR).

_Figure 16‐35: OBFF Message Contents_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


Support for OBFF is indicated via the Device Capability 2 register (Figure 16‐36 on page 782), and enabled using the Device Control 2
register (Figure 16‐37 on page 783). Note that both the pin and message options may be available. However, the pin method is preferred
because it is the lower power option.

Note that there are two variations for enabling a component to forward OBFF messages, and the difference between them has to do with
handling a targeted Link that’s not in L0. In Variation A, the message will only be sent if the Link is in L0. If it’s not, the message is
simply dropped to avoid the cost of waking the Link. This is preferred for Downstream Ports when the Device below it is not expected to have
time‐critical communication requirements and can indicate its need for non‐urgent attention by simply returning the Link to L0. For
Variation B, the message will always be for‐ warded and the Link will be returned to L0. This variation is preferred when the downstream
Device can benefit from timely notification of the platform state.

## _Figure 16‐36: OBFF Support Indication_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


When using WAKE#, enabling any Root Port to assert it is considered a glo‐ bal enable unless there are multiple WAKE# signals, in which case
only those associated with that Port are affected. When using the OBFF message, enabling a Root Port only enables the messages on that Port.
The expecta‐ tion in the spec is that all Root Ports would normally be enabled if any of them are, so as to ensure that the whole platform
was enabled. However, selectively enabling some Ports and not others is permitted.

When enabling Ports for OBFF, the spec recommends that all Upstream Ports be enabled before Downstream Ports, and Root Ports be enabled last
of all. For unpopulated hot plug slots this isn’t possible. For that case enabling OBFF using the WAKE# pin to the slot is permitted, but
it’s recom‐ mended that the Downstream Port above the slot not be enabled to deliver OBFF messages.

## _Figure 16‐37: OBFF Enable Register_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


Finally, let’s refer back to the earlier example in Figure 16‐33 on page 778 to consider what these registers might look like for that case.
The Downstream Port of the switch that connects to the lower switch will have a value for OBFF Support of 01b ‐ Message Only, while its
Upstream Port might have a value of 11b ‐ Both. These values might be hard coded into the device or hardware initialized in some other
fashion to make them visible to software after a reset. The Downstream Port would need to have an OBFF Enable value of 01b or 10b ‐ Enabled
with Message variation A or B so it could deliver an OBFF message. The Upstream Port would expect to have an OBFF Enable value of 11b ‐
Enabled with WAKE# signaling. The spec points out that when a switch is configured to use the different methods when going from one Port to
another, it’s required to make the translation and for‐ ward the indications.

## **LTR (Latency Tolerance Reporting)** 

The second new feature added to improve PM efficiency is called Latency Toler‐ ance Reporting (LTR). This optional capability allows devices
to report the delay they can tolerate when requesting service from the platform so that PM policies for platform resources like main memory
can take that into consider‐ ation. If software supports it, this provides good performance for devices when they need it and lower power
for the system when they don’t need a fast response. One simple way of using this information would be to allow the sys‐ tem to postpone
waking up to service a request as long as the latency tolerance was still met.

The meaning of “latency tolerance” is not made explicitly clear in the spec, but some things are mentioned that might play into it. For
example, the latency tol‐ erance may affect acceptable performance or it may impact whether the compo‐ nent will function properly at all.
Clearly, such a distinction would make a big difference in designing a PM policy. Similarly, the device may use buffering or other
techniques to compensate for latency sensitivity and knowledge of that would be useful for software.

## **LTR Registers**

</td>
<td width="50%">

OBFF 是一个可选的提示，系统可以使用它来通知组件关于流量的最佳时间窗口。然而，它只是一个提示，因此能够进行总线主控的设备仍然可以随时发起流量。当然，如果它们这样做，功耗将受到负面影响，因此应尽可能避免覆盖 OBFF
提示。信息通过以下两种方式之一传达：通过向端点发送消息或通过切换 WAKE# 引脚。如果两种选择都可用，则强烈建议使用引脚，因为它避免了使用过多功率的反向步骤——可能跨多条 Link 来通知组件当前系统电源状态。事实上，仅当 WAKE# 引脚不可用时才应使用 OBFF 消息。

第 778 页的图 16-33 给出了一个混合使用两种通信类型的示例。如果 WAKE# 引脚可用，则必须使用，但在本例中，两台交换机之间没有该选项。为了解决此问题，上游交换机可以将 WAKE# 引脚上接收到的状态转换为向下游发送的消息。这里也许应该指出，强烈鼓励交换机将所有
OBFF 指示转发到下游，但不要求这样做。可能有必要，特别是在使用消息时，丢弃或合并某些指示，这是允许的。

_图 16-33：OBFF 信令示例_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


**第 16 章：电源管理**

**使用 WAKE# 引脚。** 该引脚先前仅用于通知系统组件需要恢复电源，现在又被赋予了额外的含义，作为向 PCIe 组件传达系统电源状态的最简单、最低功耗的选项。它是可选的，协议相当简单：WAKE# 引脚切换以传达系统状态。如第 779 页的图 16-34
所示，存在多个转换但只有三个状态，描述如下：

1. CPU Active（CPU 活动）— 系统唤醒；所有事务 OK。这是每个组件的初始状态。

2. OBFF — 系统内存路径可用；与内存之间的传输 OK，但其他事务应等待更高的电源状态。

3. Idle（空闲）— 在发起之前等待更高的状态。

_图 16-34：WAKE# 引脚 OBFF 信令_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


当指示 CPU Active 或 OBFF 状态时，建议平台至少 10μs 后不要返回到 Idle 状态，以便为组件提供足够的时间来传递它们可能在先前 Idle 状态期间排队的包。然而，由于不需要该时序，也建议端点不要假设它们将在 CPU Active 或 OBFF
窗口中拥有一定的时间。同样，平台被允许在实际进入 Idle 之前指示它将进入 Idle

## **PCI Express Technology**

以便提前通知组件是时候完成了。设计此提前通知具体要避免的情况是：端点恰好在平台进入 Idle 时开始传输，导致立即退出 Idle 状态。规范强烈建议这应该是提前指示 Idle 状态的唯一原因，并且此提前通知时间应尽可能短。

有趣的是，WAKE# 引脚仍然可以用于其原始目的，即允许组件唤醒系统，并且毫不奇怪，这可能会使正在监视该引脚以获取 OBFF
信息的其他组件感到困惑。这可能导致电源或性能方面的次优行为，但这种情况被认为是可恢复的，因此没有采取任何措施来防范它。为了涵盖所有这些情况，每当信号不清楚时，默认状态将是 CPU Active。

**使用 OBFF 消息。** 如前所述，OBFF 信息可以使用消息来传达，但建议仅在 WAKE# 引脚不可用时使用。这些消息仅从根向下游流动。消息内容如图 16-35（第 781 页）所示，包括路由类型 100b（点对点）以及给出以下值的 OBFF 代码（所有其他代码保留）：

1. 1111b — CPU Active

2. 0001b — OBFF

3. 0000b — Idle

如果收到保留代码，组件必须将其视为"CPU Active"。如果端口收到 OBFF 消息但不支持 OBFF 或尚未启用 OBFF，则必须将其视为不支持的请求（完成状态 UR）。

**第 16 章：电源管理**

_图 16-35：OBFF 消息内容_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


通过 Device Capability 2 寄存器（图 16-36，第 782 页）指示 OBFF 支持，并通过 Device Control 2 寄存器（图 16-37，第 783 页）启用
OBFF。请注意，引脚和消息选项都可能可用。但是，首选引脚方法，因为它是较低功耗的选项。

注意，启用组件以转发 OBFF 消息有两种变体，它们之间的区别在于处理不在 L0 中的目标 Link。在变体 A 中，仅当 Link 处于 L0 时才会发送消息。如果不是，则简单地丢弃该消息以避免唤醒 Link 的成本。当下面的设备预期没有时间紧迫的通信要求并可以通过简单地将
Link 返回到 L0 来指示其对非紧急关注的需要时，对于下游端口而言这是优选的。对于变体 B，消息将始终被转发，并且 Link 将返回到 L0。当下游设备可以从平台状态的及时通知中受益时，此变体是优选的。

## _图 16-36：OBFF 支持指示_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


当使用 WAKE# 时，启用任何根端口来断言它被视为全局启用，除非有多个 WAKE# 信号，在这种情况下，只有与该端口相关的那些信号才会受到影响。当使用 OBFF
消息时，仅启用根端口仅在该端口上启用消息。规范中的期望是：如果任何根端口被启用，则通常所有根端口都会被启用，以确保整个平台都已启用。但是，允许有选择地启用某些端口而不启用其他端口。

启用 OBFF 端口时，规范建议先启用所有上游端口，然后再启用下游端口，并最后启用根端口。对于未填充的热插拔插槽，这是不可能的。对于这种情况，允许使用插槽的 WAKE# 引脚启用 OBFF，但建议不要启用插槽上方下游端口以传送 OBFF 消息。

**第 16 章：电源管理**

## _图 16-37：OBFF 启用寄存器_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


最后，让我们回到第 778 页图 16-33 中的早期示例，以考虑这些寄存器在该情况下可能是什么样子。连接到下交换机的交换机的下游端口的 OBFF Support 值为 01b — 仅消息，而其上游端口的值可能为 11b —
两者。这些值可能被硬编码到设备中或以其他方式由硬件初始化，以使其在复位后对软件可见。下游端口需要具有 01b 或 10b 的 OBFF Enable 值 — 启用了消息变体 A 或 B，以便它可以传递 OBFF 消息。上游端口将期望具有 11b 的 OBFF Enable 值 —
启用了 WAKE# 信令。规范指出，当交换机配置为从一个端口到另一个端口使用不同的方法时，需要进行翻译并转发指示。

## **LTR（延迟容忍报告）**

为提高 PM 效率而添加的第二个新特性称为延迟容忍报告（Latency Tolerance Reporting, LTR）。此可选功能允许设备在从平台请求服务时报告它们可容忍的延迟，以便像主存这样的平台资源的 PM
策略可以考虑这一点。如果软件支持，则当设备需要时提供良好的性能，而当它们不需要快速响应时则降低系统功耗。使用此信息的一个简单方法是允许系统在仍然满足延迟容忍度的情况下，推迟唤醒以服务请求。

规范中并未明确说明"延迟容忍"的含义，但提到了可能起作用的某些事项。例如，延迟容忍可能影响可接受的性能，或者可能影响组件是否能够正常运行。显然，这样的区别在设计 PM 策略时会产生很大的不同。同样，设备可以使用缓冲或其他技术来补偿延迟敏感性，了解这一点对于软件来说将是有用的。

## **LTR 寄存器**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0842_img1_tight.png" alt="Figure from page 842" width="700">

<a id="sec-16-7"></a>
## 16.7 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

The LTR capability in a device is discovered using a new bit in the PCIe Device Capability 2 Register, as shown in Figure 16‐38 on page 785,
and enabled in the Device Control 2 Register, illustrated in Figure 16‐39 on page 785. The spec pre‐ scribes a sequence for enabling LTR,
too: devices closest to the Root must be enabled first, working down to the Endpoints. An Endpoint must not be enabled unless its associated
Root Port and all intermediate switches also sup‐ port LTR and have been enabled to service it. It’s permissible for some End‐ points to
support LTR while others do not. If a Root Port or switch Downstream Port receives an LTR message but doesn’t support it or hasn’t been
enabled yet, the message must be treated as an Unsupported Request. It’s recommended that Endpoints send an LTR message shortly after being
enabled to do so. It’s strongly recommended that Endpoints not send more than two LTR messages within any 500  s period unless required by
the spec. However, if they do, Downstream Ports must properly handle them and not generate an error based on that.

## _Figure 16‐38: LTR Capability Status_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


_Figure 16‐39: LTR Enable_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


The target for LTR information is the Root Complex. Participating downstream devices all report their values but the Port just uses the
smallest value that was reported as the latency limit for all devices accessed through that Port. The Root is not required to honor
requested service latencies but is strongly encouraged to do so.

## **LTR Messages** 

The LTR message itself has the format shown in Figure 16‐40 on page 788, where it can be seen that the Routing type 100b (point‐to‐point)
and the LTR message code is 0001 0000b. Two latency values are reported, one for Requests that must be snooped and another for Requests that
will not be snooped and therefore should complete more quickly. As seen in the diagram, the format for both is the same and includes the
following fields:

- Latency Value and Scale ‐ combine to give a value in the range from 1ns to about 34 seconds. Setting these fields to all zeros indicates
that any delay will affect the device and thus the best possible service is requested. The meaning of the latency is defined as follows:

 - For Read Requests, it’s the delay from sending the END symbol in the Request TLP until receiving the STP symbol in the first Completion
TLP for that Request.

 - For Write Requests, it relates to Flow Control back‐pressure. If a write has been issued but the next write can’t proceed due to a lack
of Flow Control credits, the latency is the time from the last symbol of that write (END) until the first symbol of the DLLP that gives more
credits (SDP). In other words, this represents the time within which the Root Port should be able to accept the next write.

- Requirement ‐ can be set for none, or one, or both to indicate whether that latency value is required. If a device doesn’t implement one
of these traffic types or has no service requirements for it, then this bit must be cleared for the associated field. If a device has
reported requirements but has since been directed into a device power state lower than D0, or if its LTR Enable bit has been cleared, the
device must send another LTR message reporting that these latencies are no longer required.

## **Guidelines Regarding LTR Use** 

Endpoints have a few guidelines regarding the use of LTR: 

1. It’s recommended that they send an updated LTR message every time their service requirements change, and the spec spends some time going
over examples of this. The bottom line here is that devices need to take all the delays into account when making a change to the service
requirements. That accounting includes time for the reference clock to be restored if was turned off, for the Link to be brought back to L0,
for the LTR message to be delivered, and for the platform to prepare to handle the new requirement.

2. If the latency tolerance is being reduced, it’s recommended that the LTR message be sent far enough ahead of the first associated Request
to ensure that the platform is ready.

3. If the latency tolerance is being increased, then the LTR message to report that should immediately follow the final Request that used
the previous latency value.

4. To achieve the best overall platform power efficiency, it’s recommended that Endpoints buffer Requests as much as they can and then send
them in bursts that are as long as the Endpoint can support.

Multi‐Function Devices (MFDs) have a few rules of their own. For example, they must send a “conglomerated” LTR message as follows: 

1. Reported latency values must reflect the lowest values associated with any Function. The snoop and no‐snoop latencies could be associated
with differ‐ ent Functions, but if none of them have a requirement for snoop or no‐snoop traffic, then the requirement bit for that type
must not be set.

2. MFDs must send a new LTR message upstream if any of the Functions changes its values in a way that affects the conglomerated value. 

Switches have a similar set of rules related to LTR. Basically, they collect the messages from Downstream Ports that have been enabled to
use LTR and send a “conglomerated” message upstream according to the following rules:

1. If the Switch supports LTR, it must support it on all of its Ports. 

2. The Upstream Port is allowed to send LTR messages only when the LTR Enable bit is set or shortly after software has cleared it so it can
report that any previous requirements are no longer in effect.

3. The conglomerated LTR value is based on the lowest value reported by any participating Downstream Port. If the Requirement bit is clear,
or an invalid value is reported, the latency is considered effectively infinite.

4. If any Downstream Port reports that an LTR value is required, the Require‐ ment bit will be set for that type in the LTR message
forwarded upstream.

5. The LTR values reported upstream must take into account the latency of the Switch itself. If the Switch latency changes based on its
operational mode, it must not be allowed to exceed 20% of the minimum value reported on all Downstream Ports. The value reported on the
Upstream Port is the mini‐ mum reported value on all the Downstream Ports minus the Switch’s own latency, although the value can’t be less
than zero.

6. If a Downstream Port goes to DL_Down status, previous latencies for that Port must be treated as invalid. If that changes the
conglomerated values upstream then a new message must be sent to report that.

7. If a Downstream Port’s LTR Enable bit is cleared, any latencies associated with that Port must be considered invalid, which may also
result in a new LTR message being sent upstream.

8. If any Downstream Ports receive new LTR values that would change the conglomerated value, the Switch must send a new LTR message upstream
to report that.

Finally, the Root Complex also has a few rules related to LTR: 

1. The RC is allowed to delay processing of a device Request as long as it satis‐ fies the service requirements. One application of this
might be to buffer up several Requests from an Endpoint and service them all in a batch.

2. If the latency requirements are updated while a series of Requests is in progress, the new values must be comprehended by the RC prior to
servic‐ ing the next Request, and within less time than the previously reported latency requirements.

_Figure 16‐40: LTR Message Format_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **LTR Example** 

To illustrate the concepts discussed so far, consider the example topology shown in Figure 16‐41 on page 789. Here, the Endpoint on the
lower left has delivered an LTR message to the Switch reporting a Snoop Latency requirement of 1200ns. At this point, none of the other
Endpoints connected to the Switch has reported an LTR value, so that becomes the conglomerated value to be reported upstream. However, the
Switch has an internal latency of 50ns so that must be subtracted from the value to be reported, resulting in the Upstream Port sending an
LTR message reporting 1150ns to the Root Port.

_Figure 16‐41: LTR Example_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


Next, the Legacy Endpoint delivers an LTR message with a large latency requirement of 5000ns, as shown in Figure 16‐42 on page 790. Since
this is larger than the current conglomerate value for the Switch, no LTR message is sent for this case.

_Figure 16‐42: LTR ‐ Change but no Update_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


In the next stage, the middle Endpoint reports its LTR value as 700ns. This is smaller than the current conglomerate value, so the Switch
calculates the new value of 650ns by subtracting its internal latency and forwards that upstream as an LTR message. That makes the current
latency requirement for that Root Port 650ns, as seen in Figure 16‐43 on page 791.

Finally, the Link to the middle Endpoint stops working for some reason as shown in Figure 16‐44 on page 791, and the Switch Port reports
DL_Down. Con‐ sequently, the LTR value for that Port must be considered invalid. Since its value was being used as the current conglomerate
value, the conglomerate will be updated to the lowest value that is still valid, which is the 1200ns reported by the left‐most Endpoint. The
Switch will then subtract its internal latency and report 1150ns to the Root Port with a new LTR message.

_Figure 16‐43: LTR ‐ Change with Update_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>

</td>
<td width="50%">

设备中的 LTR 能力通过 PCIe Device Capability 2 寄存器中的一位来发现，如图 16-38（第 785 页）所示，并在 Device Control 2 寄存器中启用，如图 16-39（第 785 页）所示。规范还规定了启用 LTR
的序列：必须先启用最接近根的设备，然后向下到端点。除非关联的根端口和所有中间交换机也支持 LTR 并已启用以服务它，否则不得启用端点。某些端点支持 LTR 而其他端点不支持是允许的。如果根端口或交换机下游端口收到 LTR
消息但不支持它或尚未启用它，则该消息必须被视为不支持的请求。建议端点在启用后不久发送 LTR 消息。强烈建议端点在任何 500μs 期间内发送的 LTR 消息不超过两条，除非规范要求。但是，如果它们这样做了，下游端口必须正确处理它们，并且不应基于此产生错误。

**第 16 章：电源管理**

## _图 16-38：LTR 能力状态_

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>

LTR 信息的目标是根复合体 (Root Complex)。参与的下游设备都会报告其值，但端口仅使用所报告的最小值作为通过该端口访问的所有设备的延迟限制。根不需要遵守请求的服务延迟，但强烈鼓励这样做。

## **LTR 消息**

LTR 消息本身具有图 16-40（第 788 页）所示的格式，从图中可以看出，路由类型 100b（点对点）以及 LTR 消息代码为 0001
0000b。报告两个延迟值，一个用于必须侦听的请求，另一个用于不会被侦听因此应更快完成的请求。从图中可以看出，两者的格式相同，并包括以下字段：

- 延迟值和比例 — 组合给出范围从 1ns 到约 34 秒的值。将这些字段设置为全零表示任何延迟都会影响设备，因此请求最好的服务。延迟的含义定义如下：

 - 对于读请求，它是从请求 TLP 发送 END 符号到接收该请求的第一个完成 TLP 的 STP 符号之间的延迟。

 - 对于写请求，它与流控背压有关。如果已发出写但由于缺少流控信用而无法进行下一次写，则延迟是从该写的最后一个符号 (END) 到给予更多信用的 DLLP 的第一个符号 (SDP) 的时间。换句话说，这表示根端口应能接受下一次写的时间。

- Requirement（要求）— 可以为无、一个或两个设置，以指示是否需要该延迟值。如果设备未实现这些流量类型之一或对其没有服务要求，则该位必须为相关字段清零。如果设备已报告要求但此后被定向到低于 D0 的设备电源状态，或者其 LTR Enable
位已被清除，则设备必须发送另一条 LTR 消息，报告这些延迟不再需要。

## **关于 LTR 使用的指南**

端点有一些关于 LTR 使用的指南：

1. 建议它们在每次服务要求发生变化时发送更新的 LTR 消息，规范花了一些时间讨论了相关示例。这里的要点是，设备在对服务要求进行更改时需要考虑所有延迟。该计算包括恢复参考时钟（如果已关闭）所需的时间、将 Link 恢复到 L0 所需的时间、传递 LTR
消息所需的时间，以及平台准备处理新要求所需的时间。

2. 如果正在降低延迟容忍度，则建议在第一个相关请求之前足够早地发送 LTR 消息，以确保平台已准备好。

**第 16 章：电源管理**

3. 如果正在增加延迟容忍度，则报告该情况的 LTR 消息应紧跟在使用先前延迟值的最后一个请求之后。

4. 为实现最佳的整体平台电源效率，建议端点尽可能多地缓冲请求，然后以端点可以支持的尽可能长的突发方式发送它们。

多功能设备 (MFD) 有一些自己的规则。例如，它们必须按如下方式发送"合并"的 LTR 消息：

1. 报告的延迟值必须反映与任何 Function 关联的最低值。侦听和非侦听延迟可以与不同的 Function 相关联，但如果它们都没有对侦听或非侦听流量的要求，则该类型的 Requirement 位不得置位。

2. 如果任何 Function 以影响合并值的方式更改其值，则 MFD 必须向上游发送新的 LTR 消息。

交换机也有类似的一组与 LTR 相关的规则。基本上，它们从已启用 LTR 的下游端口收集消息，并根据以下规则向上游发送"合并"消息：

1. 如果交换机支持 LTR，则它必须在其所有端口上都支持 LTR。

2. 只有在设置了 LTR Enable 位时，或在软件清除它之后不久以报告任何先前的要求不再有效时，才允许上游端口发送 LTR 消息。

3. 合并的 LTR 值基于任何参与的下游端口报告的最低值。如果 Requirement 位清零或报告了无效值，则延迟被认为是有效地无限的。

4. 如果任何下游端口报告需要 LTR 值，则 Requirement 位将针对上游转发的 LTR 消息中的该类型置位。

5. 上游报告的 LTR 值必须考虑交换机本身的延迟。如果交换机延迟根据其操作模式而变化，则必须确保不超过所有下游端口报告的最小值的 20%。在上游端口上报告的值是所有下游端口报告的最小值减去交换机自身的延迟，但该值不能小于零。

6. 如果下游端口进入 DL_Down 状态，则该端口的先前延迟必须被视为无效。如果这改变了上游的合并值，则必须发送新消息以报告。

7. 如果下游端口的 LTR Enable 位被清除，则与该端口关联的任何延迟都必须被视为无效，这也可能导致向上游发送新的 LTR 消息。

8. 如果任何下游端口接收到会更改合并值的新 LTR 值，则交换机必须向上游发送新的 LTR 消息以报告。

最后，根复合体 (RC) 也有关于 LTR 的一些规则：

1. RC 可以延迟处理设备请求，只要它满足服务要求。一个应用可能是缓冲来自端点的多个请求并批量处理它们。

2. 如果在多个请求进行时更新了延迟要求，则新值必须在 RC 处理下一个请求之前被理解，并且时间应少于先前报告的延迟要求。

**第 16 章：电源管理**

## **LTR 示例**

为了说明到目前为止讨论的概念，请考虑图 16-41（第 789 页）中所示的示例拓扑。这里，左下角的端点已向交换机传送了一条 LTR 消息，报告侦听延迟要求为 1200ns。此时，连接到交换机的其他端点都未报告 LTR
值，因此这将成为要向上游报告的合并值。但是，交换机的内部延迟为 50ns，因此必须从要报告的值中减去该值，结果上游端口向上游发送一条 LTR 消息，报告 1150ns 给根端口。

接下来，遗留端点传送了一条 LTR 消息，延迟要求较大，为 5000ns，如图 16-42（第 790 页）所示。由于这大于交换机的当前合并值，因此不会为此情况发送 LTR 消息。

在下一阶段，中间的端点将其 LTR 值报告为 700ns。这小于当前合并值，因此交换机通过减去其内部延迟来计算新值 650ns，并将其作为 LTR 消息转发到上游。这使得该根端口的当前延迟要求为 650ns，如图 16-43（第 791 页）所示。

最后，到中间端点的链路因某种原因停止工作，如图 16-44（第 791 页）所示，并且交换机端口报告 DL_Down。因此，该端口的 LTR 值必须被视为无效。由于其值被用作当前合并值，因此合并值将更新为仍然有效的最低值，即最左侧端点报告的
1200ns。然后交换机将减去其内部延迟，并通过新的 LTR 消息向根端口报告 1150ns。

**第 16 章：电源管理**

</td>
</tr></tbody></table>

<p align="center"><b>Figure 16-39: LTR Enable</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 16-40: LTR Message Format</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 16-41: LTR Example</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 16-42: LTR ‐ Change but no Update</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 16-43: LTR ‐ Change with Update</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0844_img1_tight.png" alt="Figure from page 844" width="700">

<a id="sec-16-8"></a>
## 16.8 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

_Figure 16‐44: LTR ‐ Link Down Case_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## _**17 Interrupt Support**_ 

## **The Previous Chapter** 

The previous chapter provides an overall context for the discussion of system power management and a detailed description of PCIe power
management, which is compatible with the _PCI Bus PM Interface Spec_ and the _Advanced Config‐ uration and Power Interface_ (ACPI) spec.
PCIe defines extensions to the PCI‐PM spec that focus primarily on Link Power and event management. An overview of the OnNow Initiative,
ACPI, and the involvement of the Windows OS is also provided.

## **This Chapter** 

This chapter describes the different ways that PCIe Functions can generate interrupts. The old PCI model used pins for this, but sideband
signals are unde‐ sirable in a serial model so support for the inband MSI (Message Signaled Inter‐ rupt) mechanism was made mandatory. The
PCI INTx# pin operation can still be emulated using PCIe INTx messages for software backward compatibility reasons. Both the PCI legacy
INTx# method and the newer versions of MSI/MSI‐ X are described.

## **The Next Chapter** 

The next chapter describes three types of resets defined for PCIe: Fundamental reset (consisting of cold and warm reset), hot reset, and
function‐level reset (FLR). The use of a sideband reset PERST# signal to generate a system reset is discussed, and so is the inband TS1
based Hot Reset described.

## **Interrupt Support Background** 

## **General** 

The PCI architecture supported interrupts from peripheral devices as a means of improving their performance and offloading the CPU from the
need to poll devices to determine when they require servicing. PCIe inherits this support largely unchanged from PCI, allowing software
backwards compatibility to PCI. We provide a background to system interrupt handling in this chapter, but the reader who wants more details
on interrupts is encouraged to look into these references:

- For PCI interrupt background, refer to the PCI spec rev 3.0 or to chapter 14 of MindShare’s textbook: PCI System Architecture
(www.mindshare.com).

- To learn more about Local and IO APICs, refer to MindShare’s textbook: x86 Instruction Set Architecture. 

## **Two Methods of Interrupt Delivery** 

PCI used sideband interrupt wires that were routed to a central interrupt con‐ troller. This method worked well in simple, single‐CPU
systems, but had some shortcomings that motivated moving to a newer method called MSI (Message Signaled Interrupts) with an extension called
MSI‐X (eXtented).

**Legacy PCI Interrupt Delivery** — This original mechanism defined for the PCI bus consists of up to four signals per device or INTx#
(INTA#, INTB#, INTC#, and INTD#) as shown in Figure 17‐1 on page 795. In this model, the pins are shared by wire‐ORing them together, and
they’d eventually be connected to an input on the 8259 PIC (Programmable Interrupt Controller). When a pin is asserted, the PIC in turn
asserts its interrupt request pin to the CPU as part of a process described in “The Legacy Model” on page 796.

PCIe supports this PCI interrupt functionality for backward compatibility, but a design goal for serial transports is to minimize the pin
count. As a result, the INTx# signals were not implemented as sideband pins. Instead, a Function can generate an inband interrupt message
packet to indicate the assertion or deas‐ sertion of a pin. These messages act as “virtual wires”, and target the interrupt controller in
the system (typically in the Root Complex), as shown in Figure 17‐ 2 on page 796. This picture also illustrates how an older PCI device
using the
pins can work in a PCIe system; the bridge translates the assertion of a pin into an interrupt emulation message (INTx) going upstream to
the Root Complex. The expectation is that PCIe devices would not normally need to use the INTx messages but, at the time of this writing, in
practice they often do because sys‐ tem software has not been updated to support MSI.

_Figure 17‐1: PCI Interrupt Delivery_ 

**— MSI I nterrupt Delivery** MSI eliminates the need for sideband signals by using memory writes to deliver the interrupt notification. The
term “Message Signaled Interrupt” can be confusing because its name includes the term “Mes‐ sage” which is a type of TLP in PCIe, but an MSI
interrupt is a Posted Memory Write instead of a Message transaction. MSI memory writes are distinguished from other memory writes only by
the addresses they target, which are typi‐ cally reserved by the system for interrupt delivery (e.g., x86‐based systems tra‐ ditionally
reserve the address range FEEx_xxxxh for interrupt delivery).

Figure 17‐2 illustrates the delivery of interrupts from various types of PCIe devices. All PCIe devices are required to support MSI, but
software may or may not support MSI, in which case, the INTx messages would be used. Figure 17‐2 also shows how a PCIe‐to‐PCI Bridge is
required to convert sideband interrupts from connected PCI devices to PCIe‐supported INTx messages.

_Figure 17‐2: Interrupt Delivery Options in PCIe System_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **The Legacy Model** 

## **General** 

To illustrate the legacy interrupt delivery model, refer to Figure 17‐3 on page 797 and consider the usual steps involved in interrupt
delivery using the legacy method of interrupt pins:

1. The device generates an interrupt by asserting its pin to the controller. In older systems this controller was typically an Intel 8259
PIC that had 15 IRQ inputs and one INTR output. The PIC would then assert INTR to inform the CPU that one or more interrupts were pending.
2. Once the CPU detects the assertion of INTR and is ready to act on it, it must identify which interrupt actually needs service, and that
is done by the CPU issuing a special command on the processor bus called an Interrupt Acknowledge.

3. This command is routed by the system to the PIC, which returns an 8‐bit value called the Interrupt Vector to report the highest priority
interrupt cur‐ rently pending. A unique vector would have been programmed earlier by system software for each IRQ input.

4. The interrupt handler then uses the vector as an offset into the Interrupt Table (an area set up by software to contain the start
addresses of all the Interrupt Service Routines, ISRs), and fetches the ISR start address it finds at that location.

5. That address would point to the first instruction of the ISR that had been set up to handle this interrupt. This handler would be
executed, servicing the interrupt and telling its device to deassert its INTx# line and then would return control to the previously
interrupted task.

_Figure 17‐3: Legacy Interrupt Example_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Changes to Support Multiple Processors** 

This model works well for single‐CPU systems, but has a limitation that makes it sub‐optimal in a multi‐CPU system. The problem is that the
INTR pin can only be connected to one CPU. If multiple processors are present then only one of them will see the interrupts and will have to
service them all while the other CPUs won’t see any of them. To obtain the best performance, such systems really need an even distribution
of the system tasks across all the processors, referred to as SMP (Symmetric Multi‐Processing) but the pin model won’t sup‐ port it.

To achieve better SMP, a new model was needed, and toward this end the PIC was modified to become the IO APIC (Advanced Programmable
Interrupt Con‐ troller). The IO APIC was designed to have a separate small bus, called the APIC Bus, over which it could deliver interrupt
messages, as shown in Figure 17‐4 on page 799. In this model, the message contained the interrupt vector number, so there was no need for
the CPU to send an Interrupt Acknowledge down into the IO world to fetch it. The APIC Bus connected to a new internal logic block within the
processors called the Local APIC. The bus was shared among all the agents and any of them could initiate messages on it but, for our
purposes, the interesting part is its use for interrupt delivery from peripherals. Those interrupts could now be statically assigned by
software to be serviced by different CPUs, multiple CPUs or even dynamically assigned by the IO APIC.
_Figure 17‐4: APIC Model for Interrupt Delivery_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


That model, known as the APIC model, was sufficient for several years but still depended on sideband pins from the peripheral devices to
work. Another limi‐ tation of this model was the number of IRQs (interrupt request lines) into the IO APIC. Without a very large number of
IRQs, peripheral devices had to share IRQs which means added latency anytime that IRQ is asserted because there could be multiple devices
that could have asserted it and software must evalu‐ ate all of them. This technique of linking multiple ISRs together was often referred to
as interrupt chaining. Eventually, because of this issue and a couple other minor issues, another improvement came along.

Why not have the peripheral devices themselves send interrupt messages directly to the Local APICs? All that is needed is a communications
path which already exists in the form of the PCI bus and the processor bus. So the APIC bus was eliminated and all interrupts were delivered
to the Local APICs in the form of memory writes, referred to as MSIs or Message Signaled Interrupts. These MSIs were targeting a special
address that the system understood to be an inter‐ rupt message targeting the Local APICs. (This special address address was tra‐

ditionally FEEx_xxxxh for x86‐based systems.) Even the IO APIC was programmed to send its interrupt notifications over the ordinary data bus
using memory writes (MSI). Now it simply sends an MSI memory write across the data bus targeting the memory address of the desired
processor’s Local APIC, and that has the effect of notifying the processor of the interrupt.

This model is known as the xAPIC model, and since it is not based on sideband signals which go into an interrupt controller with a limited
number of inputs, the need to share interrupts is almost eliminated. More information can be found about this model in “An MSI Solution” on
page 827.

</td>
<td width="50%">

## _**17 Interrupt Support**_

## **上一章**

上一章提供了系统电源管理讨论的整体背景以及对 PCIe 电源管理的详细描述，电源管理与 _PCI Bus PM Interface Spec_ 以及 _Advanced Configuration and Power Interface_ (ACPI) 规范兼容。PCIe
定义了对 PCI-PM 规范的扩展，主要集中在链路电源和事件管理上。还提供了对 OnNow 计划、ACPI 以及 Windows 操作系统参与的概述。

## **本章**

本章描述 PCIe Function 可以生成中断的不同方式。旧的 PCI 模型使用引脚执行此操作，但在串行模型中边带信号是不可取的，因此带内 MSI（消息信号中断）机制的支持成为强制性要求。为了向后兼容软件，PCI INTx# 引脚操作仍然可以使用 PCIe INTx
消息进行模拟。PCI 旧式 INTx# 方法以及较新版本的 MSI/MSI-X 都进行了描述。

## **下一章**

下一章描述了为 PCIe 定义的三种类型的复位：基本复位（包括冷复位和热复位）、热复位和功能级复位 (FLR)。讨论了使用边带复位 PERST# 信号来生成系统复位，还讨论了描述的基于带内 TS1 的热复位。

## **中断支持背景**

## **概述**

PCI 体系结构支持来自外围设备的中断，作为提高其性能并减轻 CPU 必须轮询设备以确定何时需要服务的负担的一种手段。PCIe 在很大程度上从 PCI 继承了这种支持，允许软件向后兼容
PCI。我们在本章中提供有关系统中断处理的背景，但希望了解更多中断详细信息的读者鼓励查阅以下参考资料：

- 有关 PCI 中断的背景，请参阅 PCI 规范 3.0 版或 MindShare 教材的第 14 章：PCI System Architecture（www.mindshare.com）。

- 要了解有关 Local 和 IO APIC 的更多信息，请参阅 MindShare 教材：x86 Instruction Set Architecture。

## **两种中断传递方法**

PCI 使用路由到中央中断控制器的边带中断线。这种方法在简单的单 CPU 系统中运行良好，但存在一些缺点，这些缺点促使转移到一种称为 MSI（消息信号中断）的新方法，并带有一个称为 MSI-X（扩展）的扩展。

**旧式 PCI 中断传递** — 这种最初为 PCI 总线定义的机制由每个设备的最多四个信号或 INTx#（INTA#、INTB#、INTC# 和 INTD#）组成，如图 17-1（第 795 页）所示。在此模型中，引脚通过线或连接共享，它们最终将连接到 8259
PIC（可编程中断控制器）上的输入。当一个引脚被断言时，PIC 依次断言其到 CPU 的中断请求引脚，作为第 796 页"旧式模型"中描述的过程的一部分。

PCIe 支持此 PCI 中断功能以实现向后兼容性，但串行传输的设计目标是最小化引脚数。结果，INTx# 信号未作为边带引脚实现。相反，Function
可以生成带内中断消息数据包以指示引脚的断言或取消断言。这些消息充当"虚拟线路"，并以系统中的中断控制器（通常在根复合体中）为目标，如图 17-2（第 796 页）所示。该图还说明了使用

**第 17 章：中断支持**

引脚的旧 PCI 设备如何在 PCIe 系统中工作；桥将引脚的断言转换为向上游到根复合体的中断仿真消息 (INTx)。预期 PCIe 设备通常不需要使用 INTx 消息，但在撰写本文时，实际上它们经常这样做，因为尚未更新系统软件以支持 MSI。

_Figure 17-1: PCI Interrupt Delivery_

**— MSI 中断传递** MSI 通过使用内存写入来传递中断通知，从而消除了对边带信号的需要。术语"消息信号中断"可能会造成混淆，因为其名称中包含术语"消息"，这是 PCIe 中的 TLP 类型，但 MSI 中断是 Posted 内存写入而不是消息事务。MSI
内存写入仅通过它们寻址的目标地址与其他内存写入区分开，该地址通常由系统保留用于中断传递（例如，x86 基础系统传统上保留地址范围 FEEx_xxxxh 用于中断传递）。

图 17-2 说明了从各种类型的 PCIe 设备传递中断。所有 PCIe 设备都需要支持 MSI，但软件可能支持也可能不支持 MSI，在这种情况下，将使用 INTx 消息。图 17-2 还显示了 PCIe-to-PCI 桥如何需要将来自连接的 PCI 设备的边带中断转换为
PCIe 支持的 INTx 消息。

## **旧式模型**

## **概述**

为了说明旧式中断传递模型，请参考图 17-3（第 797 页）并考虑使用旧式中断引脚方法进行中断传递所涉及的常规步骤：

1. 设备通过向控制器断言其引脚来生成中断。在较旧的系统中，该控制器通常是具有 15 个 IRQ 输入和一个 INTR 输出的 Intel 8259 PIC。然后 PIC 将断言 INTR 以通知 CPU 一个或多个中断挂起。

**第 17 章：中断支持**

2. 一旦 CPU 检测到 INTR 的断言并准备好对其采取行动，它必须识别哪个中断实际需要服务，这是通过 CPU 在处理器总线上发出称为中断确认的特殊命令来完成的。

3. 该命令由系统路由到 PIC，PIC 返回一个称为中断向量的 8 位值，以报告当前挂起的最高优先级中断。每个 IRQ 输入的唯一向量先前已由系统软件编程。

4. 中断处理程序然后使用该向量作为中断表（由软件设置的区域，用于包含所有中断服务例程 ISR 的起始地址）中的偏移量，并获取在该位置找到的 ISR 起始地址。

5. 该地址将指向已设置为处理此中断的 ISR 的第一条指令。此处理程序将被执行，服务该中断并告诉其设备取消其 INTx# 线的断言，然后将控制权返回给先前被中断的任务。

## **对多处理器的支持变更**

此模型在单 CPU 系统中运行良好，但有一个限制使其在多 CPU 系统中不是最优的。问题是 INTR 引脚只能连接到一个 CPU。如果存在多个处理器，则只有其中一个处理器将看到中断，并且必须为所有中断提供服务，而其他 CPU
看不到任何中断。为了获得最佳性能，此类系统实际上需要在所有处理器之间均匀分配系统任务，称为 SMP（对称多处理），但引脚模型不支持它。

为了实现更好的 SMP，需要一种新模型，为此，PIC 被修改为 IO APIC（高级可编程中断控制器）。IO APIC 被设计为具有一个称为 APIC 总线的单独小型总线，它可以通过该总线传递中断消息，如图 17-4（第 799
页）所示。在此模型中，消息包含中断向量号，因此不需要 CPU 将中断确认向下发送到 IO 世界以获取它。APIC 总线连接到处理器内称为本地 APIC
的新内部逻辑块。该总线在所有代理之间共享，任何代理都可以在其上发起消息，但出于我们的目的，有趣的部分是它用于来自外围设备的中断传递。现在可以通过软件静态分配这些中断以由不同的 CPU 服务、多个 CPU 服务，甚至可以由 IO APIC 动态分配。

**第 17 章：中断支持**

该模型称为 APIC 模型，多年来已经足够使用，但仍然依赖于来自外围设备的边带引脚。该模型的另一个限制是到 IO APIC 的 IRQ（中断请求线）数量。如果没有大量的 IRQ，外围设备必须共享 IRQ，这意味着每当该 IRQ
被断言时都会增加延迟，因为可能有多个设备可以断言它，并且软件必须评估所有这些设备。这种将多个 ISR 链接在一起的技术通常称为中断链接 (interrupt chaining)。最终，由于这个问题和另外一些小问题，又出现了另一个改进。

为什么不让外围设备本身直接向本地 APIC 发送中断消息？所需的只是一种通信路径，它已经以 PCI 总线和处理器总线的形式存在。因此，APIC 总线被消除，所有中断都以内存写入的形式传递到本地 APIC，称为 MSI 或消息信号中断。这些 MSI 针对系统理解为针对本地 APIC
的中断消息的特殊地址。（此特殊地址是

对于 x86 基础系统，传统上为 FEEx_xxxxh。）甚至 IO APIC 也被编程为使用内存写入 (MSI) 通过普通数据总线发送其中断通知。现在它只需通过数据总线发送针对所需处理器的本地 APIC 的内存地址的 MSI 内存写入，这具有通知处理器中断的效果。

该模型称为 xAPIC 模型，由于它不基于进入输入有限的中断控制器的边带信号，因此几乎消除了共享中断的需要。有关此模型的更多信息可以在第 827 页的"An MSI Solution"中找到。

</td>
</tr></tbody></table>

<p align="center"><b>Figure 16-44: LTR ‐ Link Down Case</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-2: Interrupt Delivery Options in PCIe System</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-3: Legacy Interrupt Example</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-4: APIC Model for Interrupt Delivery</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0844_img2_tight.png" alt="Figure from page 844" width="700">

<a id="sec-16-9"></a>
## 16.9 Power Management | 电源管理

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

PCI added MSI support as an option years ago and PCIe made that capability a requirement. A peripheral that can generate MSI transactions on
its own opens new options for handling interrupts, such as giving each Function the ability to generate multiple unique interrupts instead
of just one.

## **Legacy PCI Interrupt Delivery** 

This section provides more detail on legacy PCI interrupt delivery. Readers familiar with PCI may wish to proceed to “Virtual INTx
Signaling” on page 805 to learn more about how PCIe emulates this legacy model, or to “The MSI Model” on page 812 to learn more about that
method.

PCI devices that use interrupts have two options. They may use either: 

- INTx# active low‐level signals that can be shared and were defined in the original spec. 

- Message Signaled Interrupts that were added as an option with the 2.2 ver‐ sion of the spec. MSI needs no modification for use in a PCIe
system.

## **Device INTx# Pins** 

A PCI device can implement up to 4 INTx# signals (INTA#, INTB#, INTC#, and INTD#). More than one pin is available because PCI devices can
support up to 8 functions, each of which is allowed to drive one (but only one) interrupt pin. When PCI was developed, a typical system used
a chipset that included the 15‐ input 8259 PIC, so that’s how many IRQs (which map to interrupt vectors) that were available to the system.
However, many of those were already used for system purposes like the system timer, keyboard interrupt, mouse interrupt, and so on. In
addition, some pins were reserved for ISA cards that could still be plugged into these older systems. Consequently, the PCI spec writers
consid‐ ered that only four IRQs would reliably be available for their new bus, and so the spec only supported four interrupt pins. However,
as you probably know, there are typically more than four PCI devices on a PCI bus and even a single device could have more than four
functions inside, each wanting its own inter‐
rupt. These reasons are why the PCI interrupts were designed to be level‐sensi‐ tive and shareable. These signals could simply be wire‐ORed
together to get down to a handful of resulting outputs, each one representing interrupt requests. Since they are shared, when an interrupt
is detected, the interrupt handler software will need to go through the list of functions that are sharing the same pin and test to see
which ones need servicing.

## **Determining INTx# Pin Support** 

PCI functions indicate support for an INTx# signal in their configuration head‐ ers. The read‐only Interrupt Pin register illustrated in
Figure 17‐5 indicates whether an INTx# is supported by this function and if so, which interrupt pin will it assert when requesting an
interrupt.

_Figure 17‐5: Interrupt Registers in PCI Configuration Header_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Interrupt Routing** 

The Interrupt Line register shown in Figure 17‐5 on page 801 gives the next information that a driver needs to know: the input pin of the
PIC to which this pin has been connected. The PIC is programmed by system software with a unique vector number for each input pin (IRQ). The
vector for the highest‐prior‐ ity interrupt asserted is reported to the processor who then uses that vector to index into a corresponding
entry in the interrupt vector table. This entry points to the interrupting device’s interrupt service routine which the processor exe‐
cutes.

The platform designer assigns the routing of INTx# pins from devices. They can be routed in a variety of ways, but ultimately each INTx# pin
connects to an input of the interrupt controller. Figure 17‐6 on page 803 illustrates an example in which several PCI device interrupts are
connected to the interrupt controller through a programmable router. All signals connected to a given input of the programmable router will
be directed to a specific input of the interrupt con‐ troller. Functions whose interrupts are routed to a common interrupt controller input
will all have the same Interrupt Line number assigned to them by plat‐ form software (typically firmware). In this example, IRQ15 has three
PCI INTx# inputs from different devices connected to it. Consequently, the functions using these INTx# lines will share IRQ15 and will
therefore all cause the controller to send the same vector when queried. That vector will have the three ISRs for the different Functions
chained together.

## **Associating the INTx# Line to an IRQ Number** 

Based on system requirements, the router is programmed to connect its four inputs to four available PIC inputs. Once this is done, the
routing of the INTx# pin associated with each function is known and the Interrupt Line number is written by software into each Function. The
value is ultimately read by the Function’s device driver so it will know which interrupt table entry it has been assigned. That’s the place
where the starting address of its ISR will be written, a process referred to as “hooking the interrupt”. When this function later gener‐
ates an interrupt, the CPU will receive the vector number that corresponds to the IRQ specified in the Interrupt Line register. The CPU uses
this vector to index into the interrupt vector table to fetch the entry point of the interrupt ser‐ vice routine associated with the
Function’s device driver.
_Figure 17‐6: INTx Signal Routing is Platform Specific_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **INTx# Signaling** 

The INTx# lines are active‐low signals implemented as open‐drain with a pul‐ lup resistor provided on each line by the system. Multiple
devices connected to the same PCI interrupt request signal line can assert it simultaneously without damage.

When a Function signals an interrupt it also sets the Interrupt Status bit located in the Status register of the config header. This bit can
be read by system soft‐ ware to see if an interrupt is currently pending. (See Figure 17‐8 on page 805.)

**Interrupt Disable.** The 2.3 PCI spec added an Interrupt Disable bit (Bit 10) to the Command register of the config header. See Figure
17‐7 on page 804. The bit is cleared at reset permitting INTx# signal generation, but software may set it

to prevent that. Note that the Interrupt Disable bit has no effect on Message Sig‐ nalled Interrupts (MSI). MSIs are enabled via the Command
Register in the MSI Capability structure. Enabling MSI automatically has the effect of disabling interrupt pins or emulation.

**Interrupt Status.** The PCI 2.3 spec added a read‐only Interrupt Status bit to the configuration status register (pictured in Figure 17‐8
on page 805). A func‐ tion must set this status bit when an interrupt is pending. In addition, if the Interrupt Disable bit in the Command
register of the header is cleared (i.e. inter‐ rupts enabled), then the function’s INTx# signal is asserted when this status bit is set.
This bit is unaffected by the state of the Interrupt Disable bit.

_Figure 17‐7: Configuration Command Register — Interrupt Disable Field_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>

_Figure 17‐8: Configuration Status Register — Interrupt Status Field_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

<br>


## **Virtual INTx Signaling** 

## **General** 

If circumstances make the use of MSI not possible in a PCIe topology, the INTx signaling model would be used. Following are two examples of
devices that would need to be able to use INTx messages:

**PCIe‐to‐(PCI or PCI‐X) bridges** — Most PCI devices will use the INTx# pins because MSI support is optional for them. Since PCIe doesn’t
support sideband interrupt signaling, the inband messages are used instead. The interrupt con‐ troller understands the message and delivers
an interrupt request to the CPU which would include a pre‐programmed vector number.

**Boot Devices** — PC systems commonly use the legacy interrupt model during the boot sequence because MSI usually requires OS‐level
initialization. Gener‐ ally, a minimum of three subsystems are needed for booting: an output to the operator such as video, an input from
the operator which is typically the key‐ board, and a device that can be used to fetch the OS, typically a hard drive. PCIe devices involved
in initializing the system are called “boot devices.” Boot devices will use legacy interrupt support until the OS and device drivers are
loaded, after which it’s preferable they use MSI.

## **Virtual INTx Wire Delivery** 

Figure 17‐9 on page 806 illustrates a system with a PCIe Endpoint and a PCI Express‐to‐PCI Bridge. If we assume software has not enabled MSI
on the End‐ point, it will deliver interrupt requests with INTx messages. In this example, the bridge is propogating pin‐based interrupts
from connected PCI devices with INTx messages. As can be seen, the bridge sends an INTB messages to signal the assertion and deassertion of
its INTB# input from the PCI bus. The PCIe Endpoint is shown signaling an INTA using emulation messages. Note that INTx# signaling involves
two messages:

- **Assert_INTx** messages indicate a high‐to‐low transition (from inactive to active) of the virtual INTx# signal. 

- **Deassert_INTx** messages indicate a low‐to‐high transition. 

When a Function delivers an Assert_INTx message, it also sets its Interrupt Sta‐ tus bit in the Configuration Status register, just as it
would if it asserted the physical INTx# pin (see Figure 17‐8 on page 805).

_Figure 17‐9: Example of INTx Messages to Virtualize INTA#‐INTD# Signal Transitions_ 

<img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" alt="Figure 16‐15: Active State PM Control Field" width="700">

</td>
<td width="50%">

多年前，PCI 将 MSI 支持作为可选项添加，而 PCIe 将该功能设为必需。能够自行生成 MSI 事务的外围设备为处理中断开辟了新的选择，例如赋予每个 Function 生成多个唯一中断的能力，而不仅仅是一个。

## **旧式 PCI 中断传递**

本节提供有关旧式 PCI 中断传递的更多详细信息。熟悉 PCI 的读者可能希望跳到第 805 页的"Virtual INTx Signaling"，以了解 PCIe 如何模拟此旧式模型，或者跳到第 812 页的"The MSI Model"以了解该方法。

使用中断的 PCI 设备有两种选择。它们可以使用：

- 原始规范中定义的、可共享的 INTx# 低电平有效信号。

- 随规范 2.2 版添加为可选项的消息信号中断。MSI 无需修改即可在 PCIe 系统中使用。

## **设备 INTx# 引脚**

PCI 设备最多可以实现 4 个 INTx# 信号（INTA#、INTB#、INTC# 和 INTD#）。提供多个引脚是因为 PCI 设备最多可以支持 8 个功能，每个功能允许驱动一个（但只有一个）中断引脚。在开发 PCI 时，典型系统使用包含 15 输入 8259 PIC
的芯片组，因此系统可用的 IRQ 数量（映射到中断向量）就是那么多。但是，其中许多已被用于系统用途，如系统计时器、键盘中断、鼠标中断等。此外，某些引脚是为仍可插入这些较旧系统的 ISA 卡保留的。因此，PCI 规范编写者认为只有四个 IRQ
可以可靠地用于其新总线，因此规范仅支持四个中断引脚。但是，您可能知道，PCI 总线上通常有四个以上的 PCI 设备，甚至单个设备内部可以有四个以上的功能，每个都需要自己的中断。

**第 17 章：中断支持**

这些原因就是 PCI 中断被设计为电平敏感和可共享的原因。这些信号可以简单地线或在一起以获得少量结果输出，每个输出表示中断请求。由于它们是共享的，因此当检测到中断时，中断处理程序软件将需要遍历共享同一引脚的 Function 列表，并测试哪些需要服务。

## **确定 INTx# 引脚支持**

PCI Function 在其配置头中指示对 INTx# 信号的支持。图 17-5 中所示的只读中断引脚寄存器指示此 Function 是否支持 INTx#，如果是，将在请求中断时断言哪个中断引脚。

## **中断路由**

图 17-5（第 801 页）中所示的中断行寄存器提供了驱动程序需要了解的下一个信息：该设备的引脚已连接到的 PIC 的输入引脚。PIC
由系统软件编程，每个输入引脚（IRQ）具有唯一的向量号。所断言的最高优先级中断的向量被报告给处理器，然后处理器使用该向量索引到中断向量表中的相应条目。此条目指向中断设备的 ISR，处理器将执行它。

平台设计人员分配 INTx# 引脚来自设备的路由。它们可以以各种方式路由，但最终每个 INTx# 引脚都连接到中断控制器的输入。第 803 页的图 17-6 示出了一个示例，其中多个 PCI
设备中断通过可编程路由器连接到中断控制器。连接到给定可编程路由器输入的所有信号将被定向到中断控制器的特定输入。由平台软件（通常为固件）将其中断路由到公共中断控制器输入的 Function 将具有相同的中断行编号分配给它们。在此示例中，IRQ15 上连接了来自不同设备的三个 PCI
INTx# 输入。因此，使用这些 INTx# 线的 Function 将共享 IRQ15，因此它们都会导致控制器在被查询时发送相同的向量。该向量将具有链接在一起的不同 Function 的三个 ISR。

## **将 INTx# 线关联到 IRQ 编号**

根据系统要求，对路由器进行编程以将其四个输入连接到四个可用的 PIC 输入。完成此操作后，与每个 Function 关联的 INTx# 引脚的路由是已知的，并且中断行号由软件写入每个 Function。该值最终由 Function
的设备驱动程序读取，以便知道已为其分配了哪个中断表条目。那就是将写入其 ISR 的起始地址的位置，此过程称为"挂接中断"。当此 Function 稍后生成中断时，CPU 将接收与中断行寄存器中指定的 IRQ 对应的向量号。CPU 使用此向量索引到中断向量表中，以获取与
Function 设备驱动程序关联的中断服务例程的入口点。

**第 17 章：中断支持**

## **INTx# 信令**

INTx# 线是低电平有效信号，作为漏极开路实现，由系统在线上提供上拉电阻。连接到同一 PCI 中断请求信号线的多个设备可以同时断言它而不会损坏。

当 Function 发出中断信号时，它还会设置配置头的状态寄存器中的中断状态位。该位可由系统软件读取以查看当前是否有中断挂起。（参见第 805 页的图 17-8。）

**中断禁用。** 2.3 PCI 规范将中断禁用位（第 10 位）添加到配置头的命令寄存器中。参见第 804 页的图 17-7。该位在复位时清零，允许 INTx# 信号生成，但软件可以设置它

以防止这种情况。注意，中断禁用位对消息信号中断 (MSI) 没有影响。MSI 通过 MSI 能力结构中的命令寄存器启用。启用 MSI 自动具有禁用中断引脚或仿真的效果。

**中断状态。** PCI 2.3 规范将一个只读中断状态位添加到配置状态寄存器中（如图 17-8（第 805 页）所示）。Function 在中断挂起时必须设置此状态位。此外，如果配置头的命令寄存器中的中断禁用位被清零（即中断已启用），则当此状态位被设置时，Function 的
INTx# 信号被断言。此位不受中断禁用位状态的影响。

**第 17 章：中断支持**

## **虚拟 INTx 信令**

## **概述**

如果在 PCIe 拓扑中使用 MSI 不可能，则将使用 INTx 信令模型。以下是可能需要能够使用 INTx 消息的设备的两个示例：

**PCIe-to-(PCI or PCI-X) 桥** — 大多数 PCI 设备将使用 INTx# 引脚，因为 MSI 支持对它们是可选的。由于 PCIe 不支持边带中断信令，因此改用带内消息。中断控制器理解该消息并将中断请求传送到 CPU，其中将包括预编程的向量号。

**启动设备** — PC 系统通常在启动序列期间使用旧式中断模型，因为 MSI 通常需要操作系统级初始化。通常，引导至少需要三个子系统：到操作员的输出（例如视频）、来自操作员的输入（通常是键盘）以及可用于获取操作系统的设备（通常是硬盘驱动器）。参与初始化系统的 PCIe
设备称为"启动设备"。启动设备将使用旧式中断支持，直到加载操作系统和设备驱动程序，此后最好使用 MSI。

## **虚拟 INTx 线传递**

图 17-9（第 806 页）说明了具有 PCIe 端点和 PCI Express-to-PCI 桥的系统。如果我们假设软件未在端点上启用 MSI，它将使用 INTx 消息传递中断请求。在此示例中，桥使用 INTx 消息传播来自所连接 PCI
设备的基于引脚的中断。可以看出，桥发送 INTB 消息以发出其来自 PCI 总线的 INTB# 输入的断言和取消断言信号。PCIe 端点显示使用仿真消息发出 INTA 信号。注意，INTx# 信令涉及两条消息：

- **Assert_INTx** 消息指示虚拟 INTx# 信号的高电平到低电平转换（从无效到有效）。

- **Deassert_INTx** 消息指示低电平到高电平转换。

当 Function 传递 Assert_INTx 消息时，它还会在配置状态寄存器中设置其中断状态位，就像它断言物理 INTx# 引脚一样（参见第 805 页的图 17-8）。

</td>
</tr></tbody></table>

<p align="center"><b>Figure 17-5: Interrupt Registers in PCI Configuration Header</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-6: INTx Signal Routing is Platform Specific</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-7: Configuration Command Register — Interrupt Disable Field</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-8: Configuration Status Register — Interrupt Status Field</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>


<p align="center"><b>Figure 17-9: Example of INTx Messages to Virtualize INTA#-INTD# Signal Transitions</b></p>
<p align="center"><img src="figures/chapter_16_Power_Management/embedded/page0761_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_16_Power_Management/embedded/page0761_img1.png">Page 761</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`


<img src="figures/embedded/page0848_img1_tight.png" alt="Figure from page 848" width="700">

