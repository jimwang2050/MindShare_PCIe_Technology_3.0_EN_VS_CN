**----- Start of picture text -----**<br>
Device Function<br>PCIe-Core<br>Hardware/Software<br>6. 设备阻塞新的 TLP 调度 Interface<br>7. ACK received for last TLP<br>Transaction Layer<br>(Retry Buffer empty)<br>8. 所有 FC 信用足以发送一个<br>5. PM_Active_State_Request L1<br>received Data Link Layer 最大尺寸的事务<br>12. Electrical Idle ordered set received 9. PM_Request_ACK sent<br>Causing TLP and DLLP transmission Physical Layer 持续发送直到接收到电气<br>to be disabled  idle ordered set<br>(RX) (TX)<br>11. 发送 Electrical Idle ordered set<br>并将发送器进入 (Link) 13. 发送通道进入<br>Electrical idle Electrical idle<br>(TX) (RX)<br>Physical Layer<br>4. PM_Active_State_Request L1 持续发送<br>直到从对端接收到 PM_Request_ACK Data Link Layer 10. 收到 PM_Request_ACK，<br>3. 所有 FC 信用足以发送 导致 TLP 和 DLLP 包传输被禁用<br>一个最大尺寸的事务<br>Transaction Layer<br>2. ACK received for last TLP<br>(Retry Buffer empty)<br>PCIe-Core<br>1. 设备阻塞新的 TLP 调度 Hardware/Software<br>Interface<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


## **场景 2：上游组件在收到 L1 请求前刚发送 TLP**

本场景假设上游组件在其核心逻辑指示下要在收到来自下游设备的 L1 进入请求之前向下游发送一个 TLP。有几条协商规则定义了相关动作，以确保该情形能被正确处理。

**750**

**第 16 章：电源管理**

**TLP 必须被下游组件接受。** 注意下游设备在发送 PM_Active_State_L1 DLLP 之后必须等待来自上游组件的响应。在等待期间，下游组件必须能够接受来自上游设备的 TLP 和 DLLP。尽管它不会发送任何 TLP，它必须能够根据需要发送 DLLP，例如对收到的 TLP 进行 ACK。在这种情况下，存在两种可能：

- 返回 ACK 以确认 TLP 已被成功接收。

- 如果检测到 TLP 传输错误，则返回 NAK。对该 TLP 的重试在 L1 协商期间是允许的。

**上游组件收到进入 L1 的请求。** 规范要求上游组件必须立即接受或拒绝该进入 L1 状态的请求。然而规范进一步规定：在发送 PM_Request_ACK 之前，它必须：

1. 阻塞对新 TLP 的调度

2. 等待之前发送的最后一个 TLP 的确认（如果需要），并对收到 NAK 的 TLP 进行重试，除非发生 Link Acknowledgement 超时条件。

一旦所有未完成的 TLP 都已被确认，并且所有其他条件都满足，上游设备必须返回 PM_Request_ACK DLLP。

## **场景 3：下游组件在协商期间收到 TLP**

在协商过程中，下游设备可能会被指示向上游发送一个新的 TLP。然而，开始 L1 ASPM 协商过程的设备必须阻塞新的 TLP 调度。这可以防止进入 L1 和发送新 TLP 之间的竞态条件——后者会阻止进入 L1。因此，下游设备一旦调度了 PM_Request_L1 的发送，如果收到 PM_Request_ACK，就必须完成向 L1 的转换。发送新的 TLP 必须等到已进入 L1 之后，此后设备可以发起从 L1 回到 L0 的转换来发送该 TLP。

## **场景 4：上游组件在协商期间收到 TLP**

如果上游组件在发送 PM_Request_Ack 之后需要发送 TLP 或 DLLP，它必须首先完成向 L1 的转换。然后它可以从 L1 发起变到 L0 的状态变更来发送该包。

**751**

**PCI Express Technology**

## **场景 5：上游组件拒绝 L1 请求**

第 752 页的图 16-18 总结了上游组件拒绝进入 L1 ASPM 状态的请求时的协商序列。当下游组件请求 L1 时，协商正常开始。然而，上游设备返回 PM_Active_State_Nak TLP 来拒绝该请求。拒绝进入 L1 的原因包括：

- 不支持 L1 ASPM 或软件未启用此特性

- 一个或多个 TLP 已被调度以通过该 Link 传输

- ACK 或 NAK DLLP 已被调度以传输

拒绝消息发送后，上游组件可以根据需要继续发送 TLP 和 DLLP。拒绝消息告知下游组件 L1 当前不可用，因此它必须改为转换到 L0s（如果可能）。

_图 16-18：协商序列导致拒绝进入 L1 ASPM 状态_

**==> picture [304 x 279] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Function<br>PCIe-Core<br>Hardware/Software<br>Interface<br>6. PM_Active_State_NAK<br>Transaction Layer<br>TLP request sent<br>5. PM_Active_State_Request L1<br>received Data Link Layer<br>Physical Layer<br>(RX) (TX)<br>8. 下游设备的发送链路 (Link)<br>    转换到 L0s 状态，假设<br>    所有条件都已满足 (TX) (RX)<br>Physical Layer<br>4. PM_Active_State_Request L1 持续发送直到收到响应 Data Link Layer 7. 收到 PM_Active_State_NAK<br>3. 所有 FC 信用足以发送<br>一个最大尺寸的事务 Transaction Layer<br>2. ACK received for last TLP<br>PCIe-Core<br>(Retry Buffer empty) Hardware/Software<br>1. 设备在 Transaction Layer 阻塞 TLP 调度 Interface<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


**752**

**第 16 章：电源管理**

## **退出 L1 ASPM 状态**

任一组件都可以在需要使用该 Link 时发起从 L1 回到 L0 的转换。两种情况下过程相同，且不涉及任何协商。当交换机参与退出 L1 时，规范要求交换机处于 ASPM 低功耗状态的其他端口，如果它们位于将发送包的潜在路径上，也必须转换到 L0 状态。这些问题将在后续章节中讨论。

**L1 ASPM 退出信令。** 规范规定退出 L1 通过退出电气空闲来发起，方法为发送 TS1。接收端口通过回送 TS1 给发起设备作为响应，物理层遵循其 LTSSM 协议以完成 Recovery 状态并将 Link 返回到 L0。有关详细信息，请参见第 571 页的"Recovery State"。

**交换机收到来自下游组件的 L1 退出。** 如图 16-19 所示，交换机必须通过回送 TS1 来响应下游端口上的 L1 退出，并且在 1μs 内（从信号 L1 Exit 下游起），如果其上游 Link 处于该状态，它也必须退出 L1。

**753**

## **PCI Express Technology**

_图 16-19：下游组件发出 L1 退出信号时交换机的行为_

**==> picture [335 x 329] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>6. RC 向 Switch F 发出 L1 退出信号  L1 ASPM State<br>PM State D0 5. Within 1μs of<br>step 4, Switch F<br>Switch signals L1 Exit to RC<br>(F)<br>L1 ASPM State L1 State<br>4. Switch F signals L1<br>exit to Switch C L1 ASPM<br>State<br>3. Within 1μs of step 2,<br>PM State D0 PM State Switch C signals  PM State D1<br>PCIe D0 L1 Exit to Switch FPCI-XP<br>Endpoint Switch Endpoint<br>(D) (E)<br>(C)<br>L1 ASPM State<br>L1 State 1. EP B signals<br>L1 Exit to Switch C<br>2. Switch C signals<br>L1 Exit to EP B<br>PM State D2 PM State D0<br>PCIe PCIe<br>Endpoint Endpoint<br>(A) (B)<br>**----- End of picture text -----**<br>


可以推测，下游组件转换回 L0 的原因是它正准备向上游发送 TLP。由于 L1 退出延迟相对较长，交换机"不能等到其下游端口链路完全退出到 L0 之后才在上游端口链路上发起 L1 退出转换。"这可以防止延迟的累积，否则当所有 L1 到 L0 的转换按顺序发生时会造成延迟累积。

**交换机收到来自上游组件的 L1 退出。** 在这种情况下，交换机必须通过向上游回送 TS1 进行响应，并且在 1μs 内还必须向处于 L1 ASPM 状态的所有下游端口发送 TS1，以使它们返回 L0。与上例一样，目标是将发起方与事务目标之间路径上每条 Link 返回 L0 状态的整体退出延迟降至最小。第 755 页的图 16-20 总结了这些要求。Switch F 和端点 (EP) E 之间的 Link 处于 L1 状态，因为软件将 EP E 置于 D1 状态，这导致该 Link 转换到 L1。只有处于 L1 ASPM 状态的 Link 才会因根复合体 (RC) 发起退出 L1 ASPM 而转换到 L0。

_图 16-20：上游组件发出 L1 退出信号时交换机的行为_

**==> picture [331 x 322] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>1. RC 向 Switch F 发出 L1 退出  L1 ASPM State<br>to Switch F 2. Switch F signals<br>PM State D0 L1 Exit to RC<br>Switch<br>3. Within 1μs of<br>step 2, Switch F  (F)<br>signals L1 Exit to<br>EP D  & Switch C<br>L1 State<br>L1 ASPM State<br>L1 ASPM<br>State<br>4b. EP D signals  4a. Switch C signals<br>L1 Exit to Switch F L1 Exit to Switch F<br>PM State PM State D1<br>PM State D0 PCIe D0 PCIe<br>Endpoint Switch Endpoint<br>(D) (E)<br>(C)<br>L1 ASPM State<br>L1 State<br>6. EP B signals<br>5. Within 1μs of step  L1 Exit to Switch C<br>4a, Switch C signals<br>L1 Exit to EP B<br>PM State D3 PM State D0<br>PCIe PCIe<br>Endpoint Endpoint<br>(A) (B)<br>**----- End of picture text -----**<br>


**755**

**PCI Express Technology**

## **ASPM 退出延迟**

PCI Express 提供了多种机制以确保 L0s 和 L1 的 ASPM 退出延迟不超过设备的要求。所有设备都会报告其 L0s 和 L1 退出延迟，端点还会报告其在访问根复合体时所能容忍的总延迟。该可接受延迟基于设备内的数据缓冲区大小。如果位于端点和目标设备之间的设备链路的总延迟超过了端点所报告的可接受延迟，软件可以为给定的端点禁用 ASPM。

设备所报告的退出延迟将根据 Link 两端的设备是否共享公共参考时钟而变化。因此，Link Status 寄存器包含一个名为 _Slot Clock_ 的位，它指定该组件是使用平台提供的外部参考时钟还是使用独立参考时钟（可能由内部产生）。软件检查每条 Link 两端设备的这些位，以确定它们是否都使用它并因此共享公共时钟。如果是，则软件设置 _Common Clock_ 位以在两个设备中报告此情况。第 757 页的图 16-21 说明了管理 ASPM 退出延迟所涉及的寄存器和相关位字段。

## **报告有效的 ASPM 退出延迟**

由于时钟配置会影响设备经历的退出延迟，设备必须通过 Link Status 寄存器中的 _Slot Clock_ 状态位报告其参考时钟的来源。此位由组件初始化以报告其参考时钟的来源。如果该位置 1，则表示时钟使用平台生成的参考时钟；如果清零（0），则使用独立时钟。

**PCI Ex ress Technolo p gy**

如果系统固件或软件确定 Link 上的两个组件都使用平台时钟，那么两个设备内的参考时钟将同相。这导致从 L0s 和 L1 的退出延迟更短，并在 Link Control 寄存器的 _Common Clock_ 字段中报告。然后组件必须更新其报告的退出延迟以反映正确的值。注意，如果时钟不是公共的，则默认值将是正确的，无需进一步操作。

**L0s 退出延迟更新。** L0s 的退出延迟在 Link Capability 寄存器中报告，基于默认假设（即不存在公共时钟实现）。L0s 退出延迟也在 Link 训练期间使用的 TS1 中报告，作为退出 L0s 所需的 FTS 有序集的数量 (N_FTS)。如果软件随后检测到公共时钟实现，则设置 Common Clock 字段并写入 Link Control 寄存器的 _Retrain Link_ 位，以强制 Link 训练重新进行。在重训练期间，将报告新的 N_FTS 值，并在 Link Capability 寄存器的 _L0s Latency_ 字段中报告。

**L1 退出延迟更新。** 在 Link 重训练之后，新的值也将在 _L1 Latency_ 字段中报告。

_图 16-21：用于 ASPM 退出延迟管理和报告的配置寄存器_

**757**

**PCI Ex ress Technolo p gy**

## **计算从端点到根复合体的延迟**

第 759 页的图 16-22 展示了一个端点，其事务必须经过两个交换机才能到达根复合体。假设路径中的所有 Link 都处于 L1 状态，我们以端点 B 需要向主存发送数据包为例。

1. 首先，它通过在 T 时刻在其 Link 上发起 TS1 有序集来开始唤醒序列。EP B 的 L1 退出延迟最大为 8μs，但 Switch C 的最大退出延迟为 16μs。因此，该 Link 的退出延迟为 16μs。

2. 在检测到 Link B/C 上的 L1 退出后 1μs 内，Switch C 在 T+1μs 时在 Link C/F 上发出 L1 退出信号。

3. Link C/F 在 16μs 内完成从 L1 的退出，在 T+17μs 时完成。

4. Switch F 在检测到来自 Switch C 的 L1 退出后 1μs 内（T+2μs）向根复合体发出从 L1 退出的信号。

5. Link F/RC 在 8μs 内完成从 L1 的退出，在 T+10μs 完成。

6. 将目标路径转换回 L0 的总延迟 = T+17μs。

**758**

**第 16 章：电源管理**

_图 16-22：总 L1 延迟示例_

**==> picture [345 x 423] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>RC L1 latency (8μs)<br>5. 退出到 L0 同样需要 8μs L1 State<br>PM State D0 4. 在检测到来自 Switch C 的 L1 退出后 1μs 内，<br>    Switch F 向 RC 发出 L1 退出信号<br>Switch<br>(F)<br>Switch F, L1 latency (8μs)<br>3. 退出到 L0 需要 16μs L1 State<br>L1 State<br>2. Within 1μs of detecting,<br>PM State D0 PM State         Switch C 检测到来自 EP B 的<br>PCIe D0        L1 退出后向 Switch F 发出退出信号PCI-XP<br>Endpoint Switch Endpoint PM State D1<br>(D) (E)<br>(C)<br>Switch C, L1 latency (16μs)<br>1. 退出到 L0 需要 16μs<br>L1 State L1 State            因为交换机比端点耗时更长<br>PM State D2 PM State D0<br>PCIe PCIe<br>EP B, L1 latency (8μs)<br>Endpoint Endpoint<br>(A) (B)<br>T T+16<br>Link B/C 在 T 时开始 L1 退出，需要 16μs T+17<br>T+1<br>Link C/F 在 T+1 时开始 L1 退出，需要 16μs<br>T+2 T+10<br>Link F/RC 在 T+1 时开始 L1 退出，需要 8μs<br>**----- End of picture text -----**<br>


**759**

**PCI Ex ress Technolo p gy**

## **软件发起的链路电源管理**

当软件发起配置写以更改电源状态以节能时，设备必须通过将其 Link 转换到相应的低功耗状态来响应。

## **D1/D2/D3 和 L1 状态 Hot**

规范要求，当设备内的所有 Function 已被置于任何低功耗状态（D1、D2 或 D3hot）时，设备必须发起到 L1 状态的转换，如图 16-23 所示。设备因软件发起对设备的配置访问或设备发起的事件而返回 L0。

_图 16-23：软件将设备的电源级别从 D0 更改时设备转换到 L1_

**==> picture [320 x 116] intentionally omitted <==**

**----- Start of picture text -----**<br>
L0<br>
L2/L3<br>
L0s L1 L2 L3<br>
Ready<br>
**----- End of picture text -----**<br>


在收到对 PMCSR 寄存器中 _Power State_ 字段的配置写时，设备通过向上游组件发送 PM_Enter_L1 DLLP 来发起从 L0 到 L1 的更改。

## **进入 L1 状态**

将 Link 置于 L1 状态的过程如图 16-24（见第 762 页）所示。图中的步骤在以下列表中有更详细的描述：

1. 一旦设备识别出其所有 Function 都处于 D2 状态，它必须准备将 Link 转换到 L1。这从阻塞新 TLP 的调度开始。

**760**

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

**761**

**PCI Ex ress Technolo p gy**

_图 16-24：将 Link 从 L0 转换到 L1 状态的过程_

**==> picture [342 x 323] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Function<br>6. 设备阻塞新的 TLP<br>PCIe-Core 调度<br>Hardware/Software<br>Interface<br>7. ACK received for last TLP<br>Transaction Layer (Retry Buffer empty)<br>5. PM_Enter_ L1 DLLP is  8. 所有 FC 信用足以发送一个<br>received Data Link Layer 最大尺寸的事务<br>9. PM_Request_ACK sent<br>12. 收到 Electrical Idle ordered set， continuous until electrical<br>导致 TLP 和 DLLP 传输被禁用 Physical Layer idle ordered set is received<br>(RX) (TX)<br>11. 发送 Electrical Idle ordered set (Link) 13. 发送通道被置于<br>并将发送器进入 Electrical idle Electrical idle<br>(TX) (RX)<br>4. PM_Enter_L1 DLLP 持续发送 Physical Layer<br>直到从对端接收到 PM_Request_ACK<br>3. 所有 FC 信用足以发送 Data Link Layer 10. 收到 PM_Request_ACK，<br>一个最大尺寸的事务 causing TLP and DLLP Packet<br>transmission to be disabled<br>2. ACK received for last TLP Transaction Layer<br>(Retry Buffer empty)<br>PCIe-Core<br>Hardware/Software<br>1. 设备阻塞新的 TLP 调度 Interface<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


## **退出 L1 状态**

L1 状态的退出可以由上游或下游组件发起，如下所述。本节还总结了用于退出 L1 的信令协议。

**上游组件发起。** 软件可能需要使用当前处于低功耗状态的设备，这意味着电源管理软件必须发出一个配置写，以将其电源状态改回 D0。当配置请求准备好从上游组件（根端口或下游交换机端口）发送时，该端口将退出电气空闲状态并发起重新训练以将 Link 返回到

**762**

**第 16 章：电源管理**

L0 状态。一旦 Link 处于活动状态，配置写就可以被传送到设备以将其转换回 D0，此时它已准备好供正常使用。

**下游组件发起 L1 到 L0 的转换。** 在 L1 状态下，参考时钟和电源仍会施加到 Link 上的设备。这允许将下游设备设计为监视外部事件，并在发生电源管理事件 (PME) 时触发。在传统的 PCI 中，这是通过边带 PME# 信号报告的，系统板逻辑通常使用它来生成中断以通知 CPU 需要将设备恢复到完全运行状态。PCIe 取消了边带信号，而是发送带内消息来报告 PME（详见第 769 页的"PME Message"）。

**L1 退出协议。** 在 L1 状态下，Link 的两个方向都处于电气空闲状态。设备通过改变电气空闲并发送 TS1 来发出退出 L1 的信号。当 Link 邻居检测到退出电气空闲时，它会回送 TS1。此序列触发两个设备进入 Recovery 状态，当该状态完成其操作后，两个设备都将返回 L0 状态。

## **L2/L3 Ready — 移除链路电源**

一旦软件已将设备内的所有 Function 置于 D3hot 状态，就可以安全地从设备移除电源。一个典型的应用是将系统中的所有设备置于 D3，然后从所有设备移除电源以实现最低功耗。然而，规范并未给出实际用于移除时钟和电源的机制的详细信息，也不要求遵循特定顺序，从而允许各种实现方式。

准备设备以移除电源的状态转换涉及先进入 L1 然后返回 L0 再到达 L2/L3 Ready 状态的预备步骤，如图 16-25（见第 764 页）所示。

**763**

**PCI Ex ress Technolo p gy**

_图 16-25：与准备设备以移除参考时钟和电源相关的链路状态转换_

## **L2/L3 Ready 握手序列**

当转换到 L2/L3 Ready 状态时，规范确实要求一个握手序列。这确保了所有设备都准备好移除参考时钟和电源，并且也确保在移除电源时，正在发送到根复合体的带内 PME 消息不会被意外丢失。
