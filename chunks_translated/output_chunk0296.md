第二种情况是当两个端口都支持 8.0 GT/s，并且其中之一希望执行 Tx 均衡 (Tx Equalization) 时。在这两种情况下，directed_speed_change 变量将被设置为 1b，changed_speed_recovery 位将被清除为 0b。

如果从未在 Configuration.Complete 或 Recovery.RcvrCfg 子状态中看到对端 Port 通告过高于 2.5 GT/s 的速率，那么该 Port 将不会尝试速率变更（不会设置 directed_speed_change 变量）。

**568**

**Chapter 14: Link Initialization & Training**

_Figure 14‐25: Link Control Register_

**==> picture [280 x 235] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


## _Figure 14‐26: Link Control 2 Register_

**==> picture [306 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


**569**

**PCI Ex ress Technolo p gy**

## **链路宽度变更**

上层通常只有在 upconfigure_capable 被设置为 1b 时才会指示减小链路宽度 (Link width reduction)，否则链路将无法恢复为原始宽度。如果 Hardware Autonomous Width Disable 位设置为 1b，则 Port 只能通过减小宽度来尝试纠正可靠性问题。上层只有在链路对端已通告其支持 upconfigure 并且链路尚未达到其最大宽度时，才能启动链路宽度的增加。除了这些指导原则之外，更改链路宽度的决策标准在规范中并未给出，因此属于实现相关的。

## **由链路对端启动**

规范为此情况描述了三种可能性。

第一种情况是，如果在任何 Lane 上未先收到 EIOS，就在所有 Lane 上检测到或推断出 Electrical Idle（参见 596 页的 Table 14‐10），则该 Port 可以选择进入 Recovery 状态或保持在 L0。如果此条件导致错误，则可以通过设置 Retrain Link 位等手段将 Port 引导至 Recovery。

第二种情况是，当在任何已配置的 Lane 上收到 TS1 或 TS2（或 128b/130b 的 EIEOS）时，表明链路对端已经进入 Recovery 状态。由于这两种情况都是由链路对端发起的，因此允许发送器 (Transmitter) 完成当前正在进行的任何 TLP 或 DLLP。

最后，如果在任何 Lane 上收到 EIOS，表明发生了链路电源管理变化，但接收器 (Receiver) 不支持 L0s 并且也未被引导至 L1 或 L2，那么进入 Recovery 状态是唯一的选择。

## _退出至 "L0s 状态"_

对于已被指示启动 L0s 的发送器，或已看到 EIOS 的接收器，下一状态将是 L0s。有趣的是，此时 Port 的发送器和接收器的 LTSSM 状态可以不同，因为一方可能处于 L0s 状态，而另一方仍处于 L0 状态。

- 发送器在指示时（如果实现了 L0s）进入 L0s，并发送 EIOS 来启动该变更。

- 接收器在任何 Lane 上看到 EIOS 时进入 L0s。但是，如果接收器未实现 L0s 并且未被引导至 L1 或 L2，这将被视为问题，下一状态将是 "Recovery 状态"。

**570**

**Chapter 14: Link Initialization & Training**

## _退出至 "Rx_L0s.Entry"_

- 当一个链路对端被指示启动此状态并向所有 Lane 发送一个 EIOS（速率为 5.0 GT/s 时为两个 EIOS）并且在任何 Lane 上接收到 EIOS 时，下一状态将为 L1。请注意，两个链路对端必须事先就进入 L1 达成一致，并且需要数据链路层 (Data Link Layer) 的握手以确保双方都已准备好。有关其工作原理的更多详细信息，请参见 733 页 "Introduction to Link Power Management" 一节。

## _退出至 "L2 状态"_

当一个链路对端被指示启动此状态并向所有 Lane 发送一个 EIOS（速率为 5.0 GT/s 时为两个 EIOS）并且在任何 Lane 上接收到 EIOS 时，下一状态将为 L2。请注意，两个链路对端必须事先就进入 L2 达成一致，并且需要握手以确保双方都已准备好。有关其工作原理的更多详细信息，请参见 733 页 "Introduction to Link Power Management" 一节。

## **Recovery 状态**

如果一切如预期工作，链路将训练到 L0 状态而无需进入 Recovery 状态。但我们已经讨论了可能并非如此的两个原因。首先，如果在 Configuration.Idle 中未看到正确的 Symbol 模式，LTSSM 将进入 Recovery 状态，以通过例如调整均衡值的方式来尝试纠正信号问题。其次，一旦以 2.5 GT/s 的数据速率达到 L0，并且两个设备都支持更高速度，LTSSM 将进入 Recovery 状态并尝试将链路速度更改为最高共同支持/通告的速度。在此状态下，将重新获取 Bit Lock 以及 Symbol Lock 或 Block Alignment，并对链路进行重新去偏斜 (de-skew)。链路号和 Lane 号应保持不变，除非正在更改链路宽度。在这种情况下，LTSSM 将通过 Configuration 状态重新协商链路宽度。

注意：为了简化讨论并避免多次重复相同文本，此处将使用术语 "Lock" 来表示 Bit Lock 与 Symbol Lock（针对 8b/10b 编码）或 Block Alignment（针对 128b/130b 编码）的组合。接收器必须获取此 Lock 才能识别 Symbol、有序集 (Ordered Sets) 和数据包 (Packets)。

**571**

**PCI Ex ress Technolo p gy**

## **进入 Recovery 状态的原因**

- 退出 L1 状态；这是必需的，因为退出 L1 时没有像发送 FTS 有序集那样的快速训练选项

- 退出 L0s 时，如果接收器未能在规定时间内从 FTS 有序集获得 Lock，则链路必须转移至 Recovery

- 从 L0 进入，如果：

  - 初始训练完成时，存在更高的数据速率可用。

  - 已请求链路速度或宽度变更（用于电源管理或当前速度/宽度不可靠）。

  - 软件设置 Link Control 寄存器中的 Retrain Link 位（参见 644 页 Figure 14‐71），以尝试清除传输问题。

  - 错误条件（例如与数据链路层 Ack/Nak 协议关联的 Replay Num Roll-over 事件）会自动导致物理层 (Physical Layer) 逻辑重新训练链路。

  - 接收器在任何已配置的 Lane 上看到 TS1 或 TS2，意味着相邻设备已进入 Recovery。

  - 接收器在所有已配置的 Lane 上看到 Electrical Idle，但并未先收到 Electrical Idle Ordered Set。

## **启动 Recovery 过程**

任一 Port 都可以通过向其相邻设备发送 TS1 来启动 Recovery。当 Port 看到传入的 TS1 时，它知道另一个 Port 已进入 Recovery，因此它也会进入 Recovery 并返回 TS1。两个接收器首先使用 TS1 重新获取 Lock（如有必要），然后根据需要继续进行其他子状态。这在 573 页的 Figure 14‐27 中显示。子状态中发生什么的详细描述在后续各节中提供。

**572**

**Chapter 14: Link Initialization & Training**

_Figure 14‐27: Recovery State Machine_

**==> picture [343 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from Recovery.Speed Exit to Exit to<br>L1, L0, L0s Loopback Configuration<br>Recovery.Equalization<br>Recovery.RcvrLock Recovery.Idle Exit to<br>(bit/sym bol re-lock) Recovery.RcvrCfg (Send idle data) Disabled<br>Exit to Hot<br>Exit to Exit to Reset<br>Configuration Detect<br>Exit to L0<br>**----- End of picture text -----**<br>


## **详细的 Recovery 子状态**

## _在 Recovery.RcvrLock 期间_

- 无论速度如何，发送器在所有已配置的 Lane 上使用在 Configuration 状态中设置的相同链路号和 Lane 号发送 TS1。如果进入 Recovery 状态的目的是更改速度，则在启动设备的 TS1 中，Data Rate Identifier Symbol 中的 speed_change 位将被设置为 1b，并且内部变量 directed_speed_change 被设置为 1b。如果传入 TS1 中的 speed_change 位置位，则该变量也将在另一个设备中设置。此外，进入此子状态时，successful_speed_negotiation 变量被清除为 0b。

在此子状态中，允许上游端口 (Upstream Port) 指定当以 5GT/s 运行时下游端口 (Downstream Port) 应使用的去加重 (de-emphasis) 电平。这是通过将其 TS1 中的 Selectable De-emphasis 位设置为所需值来实现的。链路上的位错误可能会阻止此信息到达下游端口，因此允许上游端口在为速度变更进入 Recovery 状态时再次请求去加重电平。如果下游端口计划使用所请求的电平，则它必须在此状态下记录 Selectable De-emphasis 位的值。

**573**

**PCI Ex ress Technolo p gy**

进入此状态时也可以应用新的发送器电压。Link Control 2 寄存器中的 Transmit Margin 字段在进入此子状态时被采样，并保持有效直到在从 L0、L0s 或 L1 再次进入此子状态时采样到新值。

希望将速率更改为 8.0 GT/s 并重新执行均衡的下游端口必须发送 speed_change 位置位的 EQ TS1 并通告 8.0 GT/s 速率。如果上游端口接收到 8 个连续的 speed_change 位设置为 1b 且支持 8.0 GT/s 速率的 EQ TS1 或 EQ TS2，则预计它也将通告 8.0 GT/s 速率，除非它已确定该速率存在无法通过均衡修复的可靠性问题。请注意，允许 Port 在进入此状态时更改其通告的数据速率，但只能更改那些可以可靠支持的速率。除了此处描述的条件之外，设备不允许在此子状态或 Recovery.RcvrCfg 或 Recovery.Equalization 中更改其支持的数据速率。

## _退出至 "Recovery.RcvrCfg"_

- 如果接收到 8 个连续的 TS1 或 TS2，其链路号和 Lane 号与正在发送的匹配 _并且_ 它们的 speed_change 位等于 directed_speed_change 变量 _并且_ 它们的 EC 字段为 00b（如果当前数据速率为 8.0 GT/s），则下一状态将为 Recovery.RcvrCfg。

- 如果设置了 Extended Synch 位，则在进入 Recovery.RcvrCfg 之前必须发送至少 1024 个连续的 TS1。

- 如果此子状态是从 Recovery.Equalization 进入的，则上游端口必须将所有 Lane 接收到的均衡系数或预设值与均衡过程第 2 阶段接受的最终系数或预设值集合进行比较。如果它们不匹配，它将在其发送的 TS2 中设置 Request Equalization 位。

## _退出至 "Recovery.Equalization"_

当数据速率为 8.0 GT/s 时，Lane 必须建立适当的均衡参数以获得良好的信号完整性。本节不适用于较低的速度。仅仅因为链路以 8.0 GT/s 运行，它并不会在每次进入 Recovery 时都经过 Recovery.Equalization 子状态。仅当满足以下条件之一时才会进入 Recovery.Equalization：

- 如果 start_equalization_w_preset 变量设置为 1b，则：

   - a) 上游端口在切换到 8.0 GT/s 之前，从其看到的 8 个连续 TS2 中注册了预设值。它必须使用发送器预设，并且可以可选地使用其接收到的接收器预设。

   - b) 下游端口必须在切换到 8.0 GT/s 时立即使用其 Lane Equalization Control 寄存器中定义的发送器预设，并且可以可选地使用其中找到的接收器预设。

- 否则（变量未设置），发送器必须使用在均衡过程上一次执行时它们所同意的系数设置。

   - a) 如果 8 个连续的传入 TS1 具有与正在发送的链路号和 Lane 号匹配、speed_change 位为 0b、但 EC 位为非零的值，则上游端口的下一状态将为 Recovery.Equalization，表明下游端口希望重做均衡过程的某些部分。规范指出，下游端口可以在软件或实现特定的指示下执行此操作。与往常一样，执行此操作所花费的时间不得导致事务超时错误，这实际上意味着下游端口需要确保在执行此步骤之前没有进行中的事务。

   - a) 如果被指示，下游端口的下一状态将为 Recovery.Equalization，只要此状态不是从 Configuration.Idle 或 Recovery.Idle 进入的。规范指出，在发送 EC 值为非零的 TS1 之前，不应发送超过两个 EC=00b 的 TS1，以请求重做均衡。

否则，经过 24ms 超时后：

## _退出至 "Recovery.RcvrCfg"_

如果同时满足以下两个条件，则下一状态将为 Recovery.RcvrCfg：

- 接收到 8 个连续的 TS1 或 TS2，其链路号和 Lane 号与正在发送的匹配，并且其 speed_change 位等于 1b。

- 并且当前数据速率已经高于 2.5 GT/s，或者至少在 TS1 或 TS2 中显示支持更高速率。

## _退出至 "Recovery.Speed"_

如果满足以下两个条件中的另一个，则下一状态将为 Recovery.Speed：

- 如果当前速度设置为高于 2.5 GT/s 但自进入 Recovery 以来无法正常工作（通过将变量 changed_speed_recovery 清零为 0b 来指示）。离开 Recovery.Speed 后的新速率将回退到 2.5 GT/s。

- 如果 changed_speed_recovery 变量设置为 1b，表明高于 2.5 GT/s 的速率已经可以工作，但链路无法以新协商的速率运行。结果，链路将恢复为从 L0 或 L1 进入 Recovery 时的速率。

**575**

**PCI Ex ress Technolo p gy**

## _退出至 "Configuration 状态"_

否则，如果未请求速度变更（directed_speed_change 变量 = 0b 并且 TS1 和 TS2 中的 speed_change 位为 0b），或者最高共同支持的数据速率为 2.5 GT/s，则 LTSSM 将返回到 Configuration。

## _退出至 "Detect 状态"_

最后，如果其他条件都不满足，则下一状态将为 Detect。

## **速度变更示例**

规范在此子状态的讨论中包含了一个速度变更的示例。场景是两个链路相邻设备（设备 A 和设备 B）正在退出复位，两者都支持 5.0 GT/s 和 8.0 GT/s 速率。

首先，链路将使用 Gen1 速率 2.5 GT/s 自动训练到 L0。（此行为很可能会在未来的规范版本中继续存在，因为它提供了与旧设计的向后兼容性。）

在我们的示例中，两个设备都支持更高的速率，这由训练期间其 TS 有序集中的 Rate Identifier 字段指示。两个设备都注意到对方支持更高的速率，其中之一（设备 A）将首先将其 directed_speed_change 变量设置为 1b。发生这种情况时，它将进入 Recovery.RcvrLock 并发送 speed_change 位置位的 TS1。如果所需速率为 8.0 GT/s 且之前未使用过，则设备将交换 EQ TS1 以传递要使用的 TX 均衡器预设，而不是发送普通 TS1。

设备 B 看到传入的 TS1，并转换到 Recovery.RcvrLock。当它识别出 8 个连续的 speed_change 位置位的 TS1 时，它通过在其自己的 TS1 中设置 speed_change 位进行响应并进入 Recovery.Speed。设备 A 等待该响应，当看到 8 个连续的 speed_change 位置位的 TS1 时，它进入 Recovery.RcvrCfg，然后进入 Recovery.Speed。在该子状态中，发送器被置为 Electrical Idle，速率被更改为最高共同支持的速率，并且 directed_speed_change 变量被清除。

经过超时周期后，两个设备都转移回 Recovery.RcvrLock，并且发送器使用新速度（在本例中为 8.0 GT/s）重新激活。它们现在再次发送 TS1，这次 speed_change 位被清除为 0b。如果新速度工作正常，它们将转移到 Recovery.RcvrCfg 并返回 L0。但是，如果设备 B 存在问题，例如未能获得 Bit Lock，则它将在此子状态中超时并返回到 Recovery.Speed。设备 A 此时可能

**576**

**Chapter 14: Link Initialization & Training**

已经转移到 Recovery.RcvrCfg，但是当它现在看到 Electrical Idle（指示相邻设备已返回到 Recovery.Speed）时，它也将返回到该状态。返回到 Recovery.Speed 会导致两个设备都恢复到进入 Recovery 时的速度（在本例中为 2.5 GT/s），并返回到 Recovery.RcvrLock。

作为对该发展的响应，设备 A 可能会再次设置 directed_speed_change 并第二次尝试该过程。如果再次失败，设备 A 可以选择从其通告列表中删除 8.0 GT/s 速率并在没有该速率的情况下再次尝试速度变更。由于现在最高公共速率为 5.0 GT/s，如果此尝试成功，则速率将最终为 5.0 GT/s。如果仍然无效，设备 A 可能会放弃尝试使用更高的速率。设备如何以及何时选择更改其通告的速率或放弃尝试使更高速率工作，在规范中并未给出，将取决于具体实现。

## **链路均衡概述**

本节提供了均衡过程的概述，并为读者理解详细的子状态机行为做好准备（如果他们对此感兴趣）。

使用更高的链路速度会比较低的数据速率产生更多的信号失真。为了补偿这种失真并最大限度地减少系统设计人员的工作和成本，3.0 规范增加了对发送器均衡 (Transmitter Equalization) 的要求。与较低速率的固定去加重值不同（去加重实际上本身就是一种简单的发送器均衡形式），新方法使用主动握手过程来使发送器与实际信号环境相匹配。在此过程中，每个接收器 Lane 评估传入信号的质量，并建议链路对端应使用的 Tx 均衡参数，以满足信号质量要求。

链路均衡过程在第一次更改为 8.0 GT/s 数据速率之后执行。规范强烈建议自主启动均衡过程（在硬件中自动启动），但并不要求这样做。如果组件选择不使用自主机制，则必须使用基于软件的机制。如果任一端口无法通过此过程实现必要的信号质量，LTSSM 将得出该速率无法工作的结论，并返回到 Recovery.Speed 以请求较低的速率。

该过程涉及多达四个阶段，如下文所述。一旦速度已更改为 8.0 GT/s，正在使用的当前均衡阶段由 TS1 中的 EC（Equalization Control）字段指示，如 Figure 14‐28 所示。

**577**

**PCI Ex ress Technolo p gy**

_Figure 14‐28: EC Field in TS1s and TS2s for 8.0 GT/s_

**==> picture [293 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>
7 6 5 4 3 2 1 0<br>
0<br>
Tx Preset EC<br>
1 Link #<br>
2 Lane # Use Preset Reset EIEOS<br>
Interval Count<br>
3 # FTS<br>
Symbol 7<br>
4 Rate ID<br>
7 6 5 4 3 2 1 0<br>
5 Train Ctl FS value when EC = 01b,<br>
Rsvd<br>
6 Otherwise Pre-Cursor Coefficient<br>
EQ Info<br>
Symbol 8<br>
9<br>
7 6 5 4 3 2 1 0<br>
10<br>
LF value when EC = 01b,<br>
Rsvd<br>
TS ID Otherwise Cursor Coefficient<br>
13 Symbol 9<br>
7 6 5 4 3 2 1 0<br>
14<br>
TS ID<br>
15 P [RCV] Post-Cursor Coefficient<br>
**----- End of picture text -----**<br>


## **Phase 0**

当下游端口准备好从较低速率更改为 8.0 GT/s 速率时，它进入 Recovery.RcvrCfg 子状态，并使用 EQ TS2 向上游端口发送 Tx 预设和 Rx 提示，如 510 页 "TS1 and TS2 Ordered Sets" 中所述。（请注意，如果链路已经以 8.0 GT/s 运行，则跳过此阶段。）下游端口 (DSP) 根据其 Equalization Control 寄存器（参见 579 页 Figure 14‐29）的内容发送 Tx 预设值。这突出的一点是，每个 Lane 可以具有不同的均衡值。下游端口将对其自己的发送器使用 DSP 值，并可选地用于其接收器，并将 USP 值发送到上游端口，以供其在切换到更高速度时使用。

**578**

**Chapter 14: Link Initialization & Training**

_Figure 14‐29: Equalization Control Registers_

**==> picture [275 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 Link Control 3 Register 2  1  0<br>
RsvdP<br>
31 Lane Error Status Register 0<br>
Equalization Control Registers<br>
31 16  15 0<br>
Lane (1) Control Lane (0) Control<br>
Lane (3) Control Lane (2) Control<br>
Lane (n) Control Lane (n-1) Control<br>
Control Register Contents<br>
15  14 12  11 8  7  6 4  3 0<br>
USP USP DSP DSP<br>
R R<br>
Rx Hint Tx Preset Rx Hint Tx Preset<br>
USP = UpStream Port   DSP = DownStream Port<br>
**----- End of picture text -----**<br>


_Table 14‐8: Tx Preset Encodings_

|**Encoding**|**De‐emphasis**|**Preshoot**|
|---|---|---|
|0000b|‐6|0|
|0001b|‐3.5|0|
|0010b|‐4.5|0|
|0011b|‐2.5|0|
|0100|0|0|



**579**

## **PCI Ex ress Technolo p gy**

_Table 14‐8: Tx Preset Encodings (Continued)_

|**Encoding**|**De‐emphasis**|**Preshoot**|
|---|---|---|
|0101|0|2|
|0110|0|2.5|
|0111|‐6|3.5|
|1000|‐3.5|3.5|
|1001|0|3.5|
|1010|Depends on FS<br>and LS values|Depends<br>on FS and<br>LS values|
|1011b to<br>1111b|Reserved|Reserved|



_Table 14‐9: Rx Preset Hint Encodings_

|**Encoding**|**Rx Preset Hint**|
|---|---|
|000b|‐6 dB|
|001b|‐7 dB|
|010b|‐8 dB|
|011b|‐9 dB|
|100|‐10 dB|
|101|‐11 dB|
|110|‐12 dB|
|111|Reserved|



一旦速率确实改变，下游端口从 Phase 1 开始，并发送 EC = 01b 的 TS1。然后它等待上游端口以相同的 EC 值进行响应。

同时，上游端口从 Phase 0 开始，如 581 页 Figure 14‐30 所示，并发送回显其早先从

**580**

**Chapter 14: Link Initialization & Training**

EQ TS1 和 EQ TS2 接收到的预设值的 TS1。如果支持，它将使用所请求的 Tx 预设，并可选地使用 Rx 提示。USP 允许在评估传入信号之前等待 500ns，但一旦它能够识别两个连续的 TS1，就准备好进行下一步。这意味着信号质量满足最低 BER 10[‐4]（即误码率小于万分之一）。随后 USP 在其 TS1 中设置 EC=01b，从而进入 Phase 1 并将下一步的控制权交给 DSP。

_Figure 14‐30: Equalization Process: Starting Point_

**==> picture [250 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>
Downstream<br>
Port<br>
EC = 01b EC = 00b<br>
Upstream<br>
Port<br>
Endpoint<br>
**----- End of picture text -----**<br>


**Phase 1**
