_退出至 "Recovery.Speed"_

否则，在 24ms 超时后（容差为 ‐0 或 +2ms），下一状态将为 Recovery.Speed，successful_speed_negotiation 标志被清除为 0b，同时 Equalization Complete 状态位被设置为 1b。

**Phase 3 Upstream。** 在此阶段，上游端口发送 EC = 11b 的 TS1，并响应来自下游端口的 Tx 值请求。

**594**

**Chapter 14: Link Initialization & Training**

如果未看到两个连续的 TS1，则保持当前 Tx 预设和系数值。但是，如果接收到两个连续的 EC = 11b 的 TS1（下游端口已进入 Phase 3），无论是首次接收，还是具有与上次不同的预设或系数值，并且如果所请求的值是合法且受支持的，则在第二个 TS1 请求结束后的 500ns 内将 Tx 设置更改为使用它们。必须在发送回上游端口的 TS1 中反映所请求的值，并将 Reject Coefficient Values 位清除为 0b。请注意，更改不得使发送器处的电压或参数违规超过 1ns。

- 如果所请求的预设或系数不合法或不受支持，则不要更改 Tx 设置，但在发送的 TS1 中反映接收到的值，并将 Reject Coefficient Values 位设置为 1b（参见 590 页 Figure 14‐38）。

_退出至 "详细的 Recovery 子状态"_

当下游端口对更改感到满意时，它开始发送 EC = 00b 的 TS1，表明希望完成均衡过程。当接收到两个这样的连续 TS1 时，将 Equalization Phase 3 Successful 和 Equalization Complete 状态位设置为 1b。

_退出至 "Recovery.Speed"_

如果在 32ms 超时内未满足上述条件，则下一状态将为 Recovery.Speed。successful_speed_negotiation 标志将被清除为 0b，并将设置 Equalization Complete 状态位。

## **Recovery.Speed**

进入此子状态时，设备必须使其发送器进入 Electrical Idle，并等待其接收器进入 Electrical Idle。在此之后，如果速度变更成功（successful_speed_negotiation = 1b），它必须保持在该状态至少 800ns；如果速度变更未成功（successful_speed_negotiation = 0b），则保持至少 6μs，但不超过额外的 1ms。

如果当前速率为 2.5 GT/s 或 8.0 GT/s，则在进入此子状态之前必须发送一个 EIOS，如果当前速率为 5.0 GT/s，则必须发送两个。当已看到这些 EIOS 或以其他方式检测或推断出 Electrical Idle 时（如 736 页 "Electrical Idle" 中所述），Lane 上存在 Electrical Idle 条件。

**595**

**PCI Ex ress Technolo p gy**

工作频率仅在接收器 Lane 已进入 Electrical Idle 之后才允许更改。如果链路已经以最高共同支持的速率运行，则即使执行此子状态，速率也不会更改。

如果协商的速率为 5.0 GT/s，则必须根据 select_deemphasis 变量的设置选择去加重电平：如果变量为 0b，则应用 ‐6 dB 去加重，但如果变量为 1b，则改为应用 ‐3.5 dB 去加重。

奇怪的是，在此子状态期间不必将 DC 共模电压保持在规范限制范围内。

如果此子状态是在成功的速度协商之后进入的（successful_speed_negotiation = 1b），则可以如 596 页 Table 14‐10 所示推断 Electrical Idle。规范指出，这涵盖了双方链路对端都已识别传入 TS1 和 TS2 的情况，因此它们的不存在可以解释为进入 Electrical Idle。

如果此子状态是在不成功的速度协商之后进入的（successful_speed_negotiation = 0b），如果在指定时间内未在任何已配置的 Lane 上检测到 Electrical Idle 退出，则可以推断 Electrical Idle。这旨在涵盖链路的至少一方无法识别 TS 有序集的情况，因此较长间隔内未退出 Electrical Idle 可以视为进入 Electrical Idle。

_Table 14‐10: Conditions for Inferring Electrical Idle_

|**State**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|
|---|---|---|---|
|L0|Absence of Flow<br>Control Update<br>DLLP or SOS in a<br>128μs window|Absence of Flow Con-<br>trol Update DLLP or<br>SOS in a 128μs win-<br>dow|Absence of Flow<br>Control Update<br>DLLP or SOS in a<br>128μs window|
|Recovery.RcvrCfg|Absence of a TS1 or<br>TS2 in a 1280 UI<br>interval|Absence of a TS1 or<br>TS2 in a 1280 UI inter-<br>val|Absence of a TS1 or<br>TS2 in a 4ms win-<br>dow|
|Recovery.Speed when<br>successful_speed_neg<br>otiation = 1b|Absence of a TS1 or<br>TS2 in a 1280 UI<br>interval|Absence of a TS1 or<br>TS2 in a 1280 UI inter-<br>val|Absence of a TS1 or<br>TS2 in a 4680 inter-<br>val|



**596**

**Chapter 14: Link Initialization & Training**

_Table 14‐10: Conditions for Inferring Electrical Idle (Continued)_

|**State**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|
|---|---|---|---|
|Recovery.Speed when<br>successful_speed_neg<br>otiation = 0b|Absence of an Elec-<br>trical Idle exit in a<br>2000 UI interval|Absence of an Electri-<br>cal Idle exit in a 16000<br>UI interval|Absence of an Electri-<br>cal Idle exit in a<br>16000 UI interval|
|Loopback.Active (as a<br>slave)|Absence of an Elec-<br>trical Idle exit in a<br>128μs window|N/A|N/A|



directed_speed_change 变量将被清除为 0b，并且新数据速率必须可见于 Link Status 寄存器（如图 14‐39 所示）的 Current Link Speed 字段中。

如果速度因链路带宽变更而更改：

- 如果 successful_speed_negotiation 设置为 1b 并且 8 个连续 TS2 中的 Autonomous Change 位设置为 1b，或者速度变更由下游端口出于自主原因启动（不是可靠性问题，也不是由软件设置 Link Retrain 位引起的），则 Link Status 寄存器中的 Link Autonomous Bandwidth Status 位设置为 1b。

- 否则，Link Bandwidth Management Status 位设置为 1b。

_Figure 14‐39: Link Status Register_

**==> picture [373 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>
Link Autonomous<br>
Bandwidth Status<br>
Link Bandwidth<br>
Management Status<br>
Data Link Layer<br>
Link Active<br>
Slot Clock<br>
Configuration<br>
Link Training<br>
Undefined<br>
Negotiated<br>
Link Width<br>
Current Link Speed<br>
**----- End of picture text -----**<br>


**597**

**PCI Ex ress Technolo p gy**

## _退出至 "详细的 Recovery 子状态"_

一旦超时已过，下一状态将为 Recovery.RcvrLock

如果此子状态是从 Recovery.RcvrCfg 进入的，并且速度变更成功，则所有已配置的 Lane 的新数据速率将更改为最高共同支持的速率，并将 changed_speed_recovery 变量设置为 1b。

如果此子状态是在从 L0 或 L1 进入 Recovery 以来第二次进入的（通过 changed_speed_recovery = 1b 指示），则新数据速率将是 LTSSM 进入 Recovery 时正在使用的速率，并且 changed_speed_recovery 变量被清除为 0b。

否则，新数据速率将恢复为 2.5 GT/s，并且 changed_speed_recovery 变量保持清除为 0b。规范指出，这表示 L0 中的速率高于 2.5 GT/s，但一个链路对端无法以该速率运行并在首次通过时在 Recovery.RcvrLock 中超时的情况。

## _退出至 "Detect 状态"_

如果不符合退出到 Recovery.RcvrLock 的任何条件，则下一状态将为 Detect，尽管规范指出在正常情况下这应该是不可能的。它将意味着链路相邻设备根本无法再通信。

## **Recovery.RcvrCfg**

此状态只能从 Recovery.RcvrLock 进入，前提是至少接收到 8 个 TS1 或 TS2 有序集，且其链路号和 Lane 号与之前协商的相同。这意味着已建立位和符号或块锁定 (bit and symbol or block lock)，现在该 Port 必须确定 Recovery 状态中是否还有其他需要处理的项目。如果进入 Recovery 的目的只是重新建立位和符号锁定以离开链路电源管理状态，那么可能会在此处交换 TS2 并继续进行到 Recovery.Idle。但是，如果存在进入 Recovery 状态的其他原因（例如速度变更或链路宽度变更），则将在此子状态中确定并发生适当的状态转换。

在此子状态期间，发送器在所有已配置的 Lane 上发送 TS2，其链路号和 Lane 号与之前配置的相同。如果 directed_speed_change 变量设置为 1b，则 TS2 中的 speed_change 位也必须被设置。TS2 中的 N_FTS 值应反映当前速率所需的数量。进入此子状态时，start_equalization_w_preset 变量被清除为 0b。

**598**

**Chapter 14: Link Initialization & Training**

如果速度已更改，则 TS2 中现在可能会看到不同的 N_FTS 数字。该值必须用于退出将来的 L0s 低功耗链路状态。对于 8b/10b 编码，必须在离开此子状态之前完成 Lane 间去偏斜。设备必须注意传入 TS2 中通告的速率标识符，并使用它来覆盖任何先前记录的值。使用 128b/130b 编码时，设备必须注意 Request Equalization 位的值以供将来参考。

有关此子状态的说明：变量 successful_speed_negotiation 被设置为 1b。此时注意到 TS2 中以 speed_change 位置位通告的数据速率以供将来参考，并且 Autonomous Change 位用于在 Recovery.Speed 期间在 Link Status 寄存器中可能记录日志。将在 Recovery.Speed 中选择的速率是最高共同支持的速率。有趣的是，在这种情况下即使链路已经以最高支持的速率运行，仍会发生到 Recovery.Speed 的更改，尽管在这种情况下速率实际上不会改变。

如果速度将更改为 8.0 GT/s，则下游端口将需要发送 EQ TS2（Symbol 6 的位 7 设置为 1b 以指示 EQ 训练序列）。如果 8.0 GT/s 是共同支持的，并且在任何已配置的 Lane 上看到 8 个连续的 speed_change 位置位的 TS1 或 TS2，或者 equalization_done_8GT_data_rate 变量为 0b，或者被指示，则将识别这种情况。如果当前数据速率为 8.0 GT/s 且均衡过程存在问题，则上游端口可以设置 Request Equalization 位。任何一端都可以通过将 Request Equalization 和 Quiesce Guarantee 位都设置为 1b 来请求再次执行均衡。

上游端口根据接收到的 TS2 中的 Selectable De-emphasis 位设置其 select_deemphasis 变量。并且，如果 TS2 是 EQ TS2，则它们将 start_equalization_w_preset 变量设置为 1b，并使用新信息更新其 Lane Equalization 寄存器（即：更新寄存器中的 Upstream Port Transmitter Preset 和 Receiver Preset Hint 字段）。任何未接收到 EQ TS2 的已配置 Lane 将以设计特定的方式选择其 8.0 GT/s 操作的预设值。如果 equalization_done_8GT_data_rate 变量被清除为 0b 或被指示，则下游端口必须将其 start_equalization_w_preset 变量设置为 1b。

最后，如果使用 128b/130b 编码，则设备必须注意 Request Equalization 位的值。如果已设置，则必须将其与 Quiesce Guarantee 位一起存储以供将来参考。

**599**

**PCI Ex ress Technolo p gy**

## _退出至 "Recovery.Idle"_

如果满足以下两个条件，则下一状态将为 Recovery.Idle：

- 在任何已配置的 Lane 上接收到 8 个连续的 TS2，其链路号和 Lane 号以及速率标识符与正在发送的匹配，并且以下任一条件：

   - a) TS2 中的 speed_change 位被清除为 0b，或者

   - b) 没有高于 2.5 GT/s 的速率被共同支持。

- 在接收到一个 TS2 之后已发送 16 个 TS2，并且它们未被任何中间的 EIEOS 中断。changed_speed_recovery 和 directed_speed_change 变量在进入此子状态时都被清除为 0b。

## _退出至 "Recovery.Speed"_

如果以下列出的所有三个条件都为真，则 LTSSM 将进入 Recovery.Speed：

- 在任何已配置的 Lane 上接收到 8 个连续的 speed_change 位置位的 TS2，速率标识符相同，Symbol 6 中的值相同，并且：

   - a) TS2 是标准 8b/10b TS2，或者

   - b) TS2 是 EQ TS2，或者

   - c) 自在任何已配置的 Lane 上接收到 8 个 EQ TS2 以来已过去 1ms。

- 两个链路对端都支持高于 2.5 GT/s 的速率，或者速率已经高于 2.5 GT/s。

- 对于 8b/10b 编码，在同一已配置的 Lane 上接收到一个 speed_change 位设置为 1b 的 TS2 之后，至少发送了 32 个 speed_change 位设置为 1b 的 TS2 而没有任何中间的 EIEOS。对于 128b/130b 编码，在同一已配置的 Lane 上接收到一个 speed_change 位设置为 1b 的 TS2 之后，发送了至少 128 个 speed_change 位设置为 1b 的 TS2。

如果自上次从 L0 或 L1 进入 Recovery 以来（changed_speed_recovery = 1b）速率已更改为相互协商的速率，并且任何已配置的 Lane 已看到 EIOS 或检测到/推断出 Electrical Idle 并且自进入此子状态以来未看到 TS2，则也可以发生到 Recovery.Speed 的转换。这意味着尝试了更高速率，但链路对端表示出于某种原因它无法工作。新速率将返回到从 L0 或 L1 进入 Recovery 时的速率。

导致到 Recovery.Speed 的转换的最后一种情况是，如果自上次从 L0 进入 Recovery 以来速率 _未_ 更改

**600**

**Chapter 14: Link Initialization & Training**

或者 L1（changed_speed_recovery = 0b），并且当前速率已经高于 2.5 GT/s，并且任何已配置的 Lane 已看到 EIOS 或检测到/推断出 Electrical Idle 并且自进入此子状态以来未看到 TS2。在这种情况下，理解是当前速率不起作用，解决方案是降下来，因此新速率将变为 2.5 GT/s。

## _退出至 "Configuration 状态"_

如果在任何已配置的 Lane 上接收到 8 个连续的 TS1，其链路号或 Lane 号与正在发送的不匹配，并且 speed_change 位被清除为 0b，或者没有高于 2.5 GT/s 的速率被共同支持，则下一状态将为 Configuration。

当 LTSSM 转换到 Configuration 时，变量 changed_speed_recovery 和 directed_speed_change 被清除为 0b。如果 N_FTS 值自上次以来已更改，则新值必须用于将来的 L0s。

## _退出至 "Detect 状态"_

在 48ms 内未解决为先前定义的状态转换之一后，如果数据速率为 2.5 GT/s 或 5.0 GT/s，则下一状态将为 Detect。

如果速率为 8.0 GT/s，则存在另一种可能性，因为尝试次数可能尚未超过。这由 idle_to_rlock_transitioned 变量指示，并且当速率为 8.0 GT/s 且其小于 FFh 时，新状态将为 "Recovery.Idle"。如果进行了该转换，则变量 changed_speed_recovery 和 directed_speed_change 将被清除为 0b。但是，一旦 idle_to_rlock_transitioned 达到 FFh 并且看到 48ms 超时，则下一状态将为 Detect。

## **Recovery.Idle**

顾名思义，发送器通常在此子状态中发送 Idles，作为更改为完全可操作的 L0 状态的准备。对于 8b/10b 模式，Idle 数据通常在所有 Lane 上发送，而对于 128b/130b，发送 SDS 以启动 Data Stream，然后在所有 Lane 上发送 Idle 数据符号。

## _退出至 "L0 状态"_

如果以下任一情况为真，则下一状态为 L0。在任一情况下，如果 Retrain Link 位自上次从 Recovery 或 Configuration 转换到 L0 以来已写入 1b，则下游端口将 Link Bandwidth Management Status 位设置为 1b（参见 597 页 Figure 14‐39）。

- 使用 8b/10b 编码并且已接收到 8 个连续的 Symbol Times 的 Idle 数据，并且自接收到第一个 16 个 Idle 数据符号以来已发送。

**601**

## **PCI Ex ress Technolo p gy**

- 使用 128b/10b 编码，已接收到 8 个连续的 Symbol Times 的 Idle 数据，并且自接收到第一个 16 个 Idle 数据符号以来已发送，并且此状态不是从 Recovery.RcvrCfg 进入的。请注意，Idle 数据符号必须包含在 Data Block 中，Lane 间去偏斜必须在 Data Stream 处理开始之前完成，并且 idle_to_rlock_transitioned 变量在转换到 L0 时被清除为 00h。

## _退出至 "Configuration 状态"_

如果以下任一情况，则下一状态为 Configuration：

- Port 被更高层指示以选择性地重新配置链路，例如更改链路宽度。

- 任何已配置的 Lane 看到两个连续的 Lane 号设置为 PAD 的传入 TS1（要转换到 Configuration 以更改链路的 Port 将在所有 Lane 上发送 PAD Lane 号）。规范建议 LTSSM 在更改链路宽度时使用此转换，以减少所需的时间。

## _退出至 "Disable 状态"_

如果以下任一情况，则下一状态为 Disabled：

- 下游或可选 crosslink Port 被更高层指示在其 TS1 或 TS2 中设置 Disable Link 位。

- 上游或可选 crosslink Port 的任何已配置的 Lane 看到两个连续的传入 TS1 中设置了 Disable Link 位。

## _退出至 "Hot Reset 状态"_

如果以下任一情况，则下一状态为 Hot Reset：

- 下游或可选 crosslink Port 被更高层指示在其 TS1 或 TS2 中设置 Hot Reset 位。

- 上游或可选 crosslink Port 的任何已配置的 Lane 看到两个连续的传入 TS1 中设置了 Hot Reset 位。

## _退出至 "Loopback 状态"_

如果以下任一情况，则下一状态为 Loopback：

- 已知发送器具有 Loopback Master 能力（设计特定的；规范不提供验证方法）并被更高层指示在其 TS1 或 TS2 中设置 Loopback 位。

- 上游或可选 crosslink Port 的任何已配置的 Lane 看到两个连续的传入 TS1 中设置了 Loopback 位。接收设备随后成为 Loopback slave。

**602**

**Chapter 14: Link Initialization & Training**

## _退出至 "Detect 状态"_

否则，在 2ms 超时后，下一状态将为 Detect，除非 idle_to_rlock_transitioned 变量小于 FFh，在这种情况下下一状态将为 "详细的 Recovery 子状态"。对于到 Recovery.RcvrLock 的转换，如果数据速率为 8.0 GT/s，则 idle_to_rlock_transitioned 变量加 1b，而对于 2.5 或 5.0 GT/s，它将被设置为 FFh。

## **L0s 状态**

这是具有到 L0 的最短退出延迟的低功耗链路状态。设备在硬件控制下自动管理此状态的进入和退出，无需任何软件参与。链路的每个方向可以独立地进入和退出 L0s 状态。

## **L0s 发送器状态机**

L0s 状态对于发送器和接收器具有不同的子状态。将首先描述发送器子状态。如 603 页 Figure 14‐40 所示，与 L0s 状态关联的发送器状态机是一个简单的状态机。

_Figure 14‐40: L0s Tx State Machine_

**==> picture [288 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>
from L0<br>
Tx sends  Transmitter sends<br>
EIOS FTSs on all Lanes<br>
TTX-IDLE-MIN<br>
= 20 ns Tx_L0s.Idle Directed<br>
Tx_L0s.Entry Tx_L0s.FTS<br>
(Tx Electrical Idle)<br>
Transmitter sends<br>
SOS or EIEOS<br>
Exit to<br>
L0<br>
**----- End of picture text -----**<br>


**603**

**PCI Ex ress Technolo p gy**

## **Tx_L0s.Entry**

当被上层指示时，发送器进入 L0s。规范未给出此决策标准，但凭直觉，它将基于不活动超时发生：给定时间内未发送 TLP 或 DLLP。要进入 L0s，发送器发送一个 EIOS（5.0 GT/s 速率为两个 EIOS）并进入 Electrical Idle。但是，发送器不会被关闭，并且必须将 DC 共模电压保持在规范范围内。

## _退出至 "Tx_L0s.Idle"_

下一状态将在 TTX-IDLE-MIN 超时（20ns）后为 Tx_L0s.Idle。该时间旨在确保发送器已建立 Electrical Idle 条件。

## **Tx_L0s.Idle**

在此子状态中，发送器继续 Electrical Idle 状态，直到被指示离开。由于此方向的链路处于 Electrical Idle 状态，因此将产生节能效益，这是 L0s 状态的整个目的。

_退出至 "Tx_L0s.FTS"_

下一状态将在被指示时为 Tx_L0s.FTS，例如当 Port 需要恢复数据包传输时。LTSSM 将以设计特定的方式被指示退出此状态。

## **Tx_L0s.FTS**

在此子状态中，发送器将开始发送 FTS 有序集以重新训练链路对端的接收器。发送的 FTS 数量是链路对端在上次训练到 L0 期间的 TS 有序集中通告的 N_FTS 值。规范指出，如果接收器在尝试执行此操作时超时，它可以选择在 Recovery 状态期间增加其通告的 N_FTS 值。

如果设置了 Extended Synch 位（参见 644 页 Figure 14‐71），则发送器必须发送 4096 个 FTS，而不是 N_FTS 数量。这扩展了可用于同步外部测试和分析逻辑的时间，该逻辑可能无法像嵌入式逻辑那样快地恢复 Bit Lock。

对于所有数据速率，在发送任何 FTS 之前不能发送 SOS。但是，对于 5.0 GT/s 速率，必须在发送 FTS 之前发送 4 到 8 个 EIE 符号。对于 128b/130b，必须在 FTS 之前发送 EIEOS。

**604**

**Chapter 14: Link Initialization & Training**

## _退出至 "L0 状态"_

一旦已发送所有 FTS，发送器将转换到 L0 状态，并且：

- a) 对于 8b/10b 编码，一个 SOS 在所有已配置的 Lane 上发送，尽管在 FTS 之前或期间不发送任何 SOS。

- b) 对于 128b/130b 编码，发送一个 EIEOS 后跟一个 SDS 和 Data Stream。

## **L0s 接收器状态机**

605 页 Figure 14‐41 显示了接收器 L0s 状态机。如果 Link Capability 寄存器中的 ASPM Support 字段显示支持 L0s，则接收器需要实现 L0s 支持，即使未指示支持也允许实现。

_Figure 14‐41: L0s Receiver State Machine_

**==> picture [327 x 184] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>
from L0<br>
Rx detects<br>
EIOS Exit from FTSs Received<br>
TTX-IDLE-MIN Electrical<br>
= 20 ns Rx_L0s.Idle Idle<br>
Rx_L0s.Entry Rx_L0s.FTS<br>
(Rx Electrical Idle)<br>
Tx sends N_FTS<br>
SOS or EIEOS Timeout<br>
Exit to Exit to<br>
L0 Recovery<br>
**----- End of picture text -----**<br>


**605**

**PCI Ex ress Technolo p gy**

## **Rx_L0s.Entry**

当接收器接收到 EIOS 时进入，前提是它支持 L0s 并且未被引导至 L1 或 L2。

_退出至 "Rx_L0s.Idle"_

下一状态将在 TTX-IDLE-MIN 超时（20ns）后为 Rx_L0s.Idle。

## **Rx_L0s.Idle**

接收器现在处于 Electrical Idle 模式，并且只是等待看到退出 Electrical Idle。
