如果系统固件或软件确定 Link 上的两个组件都使用平台时钟，那么两个设备内的参考时钟将同相。这导致从 L0s 和 L1 的退出延迟更短，并在 Link Control 寄存器的 _Common Clock_ 字段中报告。然后组件必须更新其报告的退出延迟以反映正确的值。注意，如果时钟不是公共的，则默认值将是正确的，无需进一步操作。

**L0s 退出延迟更新。** L0s 的退出延迟在 Link Capability 寄存器中报告，基于默认假设（即不存在公共时钟实现）。L0s 退出延迟也在

**756**

**第 16 章：电源管理**

链路训练期间使用的 TS1 中报告，作为退出 L0s 所需的 FTS 有序集的数量 (N_FTS)。如果软件随后检测到公共时钟实现，则设置 Common Clock 字段并写入 Link Control 寄存器的 _Retrain Link_ 位，以强制链路训练重新进行。在重训练期间，将报告新的 N_FTS 值，并在 Link Capability 寄存器的 _L0s Latency_ 字段中报告。

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
Device Function<br>6. 设备阻塞新的 TLP<br>PCIe-Core 调度<br>Hardware/Software<br>Interface<br>7. ACK received for last TLP<br>Transaction Layer (Retry Buffer empty)<br>5. PM_Enter_ L1 DLLP is 8. 所有 FC 信用足以发送一个<br>received Data Link Layer 最大尺寸的事务<br>9. PM_Request_ACK sent<br>12. Electrical Idle ordered set received continuously until electrical<br>Causing TLP and DLLP transmission Physical Layer idle ordered set is received<br>to be disabled<br>(RX) (TX)<br>11. Electrical Idle ordered set<br>is sent and transmitter goes (Link) 13. Transmit lanes are placed into<br>to Electrical idle Electrical idle<br>(TX) (RX)<br>4. PM_Enter_L1 DLLP is sent Physical Layer<br>continuously until PM_Request_ACK<br>is received from the opposite port<br>3. All FC credits sufficient to send  Data Link Layer 10. PM_Request_ACK received,<br>a maximum-sized transaction causing TLP and DLLP Packet<br>transmission to be disabled<br>2. ACK received for last TLP Transaction Layer<br>(Retry Buffer empty)<br>PCIe-Core<br>Hardware/Software<br>1. 设备阻塞新的 TLP 调度 Interface<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


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
