_退出到"Recovery.Speed"_

否则,经过 24ms 超时(容差为 -0 或 +2ms)后,下一个状态将是 Recovery.Speed,successful_speed_negotiation 标志被清零至 0b,而 Equalization Complete 状态位置为 1b。

**Phase 3 上游端口。** 在此阶段,上游端口发送 EC = 11b 的 TS1,并响应来自下游端口的请求 Tx 值。

**594** 

**Chapter 14: Link Initialization & Training** 

如果未看到两个连续的 TS1,则保持当前的 Tx 预设和系数值。但是,如果接收到两个连续的 EC = 11b 的 TS1(下游端口已进入 Phase 3),无论是第一次收到,还是与上次预设或系数值不同,并且如果请求的值是合法且受支持的,那么在第二个 TS1 请求结束后的 500ns 内将 Tx 设置更改为使用这些值。请求的值必须反映在发回上游端口的 TS1 中,并将 Reject Coefficient Values 位清零至 0b。请注意,此更改不得导致发送器上的电压或参数非法超过 1ns。

- 如果请求的预设或系数是非法或不受支持的,则不更改 Tx 设置,但在发送的 TS1 中反映接收到的值,并将 Reject Coefficient Values 位置为 1b(参见第 590 页的 Figure 14-38)。

_退出到"详细恢复子状态"_

当下游端口对更改满意时,它将开始发送 EC = 00b 的 TS1,表示希望完成均衡过程。当接收到两个这样的连续 TS1 时,将 Equalization Phase 3 Successful 和 Equalization Complete 状态位置为 1b。

_退出到"Recovery.Speed"_

如果在 32ms 超时内不满足上述条件,则下一个状态将是 Recovery.Speed。successful_speed_negotiation 标志将被清零至 0b,Equalization Complete 状态位将被设置。

## **Recovery.Speed** 

进入此子状态时,设备必须在其发送器上进入 Electrical Idle,并等待其接收器进入 Electrical Idle。在此之后,如果速率更改成功(successful_speed_negotiation = 1b),则必须保持至少 800ns;如果速率更改不成功(successful_speed_negotiation = 0b),则必须保持至少 6µs,但不超过额外的 1ms。

如果当前速率为 2.5 GT/s 或 8.0 GT/s,则在进入此子状态之前必须发送一个 EIOS;如果当前速率为 5.0 GT/s,则必须发送两个 EIOS。当已看到这些 EIOS 或以其他方式检测或推断出 Lane 上的 Electrical Idle 条件(如第 736 页的"Electrical Idle"中所述)时,Lane 上存在 Electrical Idle 条件。

**595** 

**PCI Ex ress Technolo p gy** 

只有在接收器 Lane 进入 Electrical Idle 后,才允许更改工作频率。如果 Link 已经以最高共同支持的速率运行,则即使执行此子状态,也不会更改速率。

如果协商的速率为 5.0 GT/s,则必须根据 select_deemphasis 变量的设置来选择去加重级别:如果变量为 0b,则应用 -6 dB 去加重;但如果变量为 1b,则应用 -3.5 dB 去加重。

奇怪的是,在此子状态期间,DC 共模电压不必保持在规范限制范围内。

如果在成功的速率协商(successful_speed_negotiation = 1b)之后进入此子状态,则可以如第 596 页的 Table 14-10 所示推断 Electrical Idle。规范指出,这涵盖了链路两端都已识别传入 TS1 和 TS2 的情况,因此它们的缺失可以解释为进入 Electrical Idle。

如果在未成功的速率协商(successful_speed_negotiation = 0b)之后进入此子状态,则如果在指定时间内未在任何已配置的 Lane 上检测到至少一次 Electrical Idle 退出,则可以推断 Electrical Idle。这是为了涵盖链路的至少一端无法识别 TS Ordered Sets 的情况,因此在较长时间内未退出 Electrical Idle 可以视为进入 Electrical Idle。

_Table 14-10: 推断 Electrical Idle 的条件_ 

|**状态**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|
|---|---|---|---|
|L0|在 128µs 窗口中<br>缺少流控更新<br>DLLP 或 SOS|在 128µs 窗口中<br>缺少流控更新<br>DLLP 或 SOS|在 128µs 窗口中<br>缺少流控更新<br>DLLP 或 SOS|
|Recovery.RcvrCfg|在 1280 UI 间隔<br>中缺少 TS1 或 TS2|在 1280 UI 间隔<br>中缺少 TS1 或 TS2|在 4ms 窗口<br>中缺少 TS1 或 TS2|
|Recovery.Speed 当<br>successful_speed_neg<br>otiation = 1b|在 1280 UI 间隔<br>中缺少 TS1 或 TS2|在 1280 UI 间隔<br>中缺少 TS1 或 TS2|在 4680 间隔<br>中缺少 TS1 或 TS2|



**596** 

**Chapter 14: Link Initialization & Training** 

_Table 14-10: 推断 Electrical Idle 的条件(续)_ 

|**状态**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|
|---|---|---|---|
|Recovery.Speed 当<br>successful_speed_neg<br>otiation = 0b|在 2000 UI 间隔<br>中缺少 Electrical<br>Idle 退出|在 16000 UI<br>间隔中缺少<br>Electrical Idle 退出|在 16000 UI 间隔<br>中缺少 Electrical<br>Idle 退出|
|Loopback.Active(作为<br>slave)|在 128µs 窗口<br>中缺少 Electrical<br>Idle 退出|N/A|N/A|



directed_speed_change 变量将被清零至 0b,新数据速率必须显示在 Link Status 寄存器的 Current Link Speed 字段中,如图 14-39 所示。

如果因链路带宽更改而更改了速率:

- 如果 successful_speed_negotiation 设置为 1b,并且 8 个连续 TS2 中的 Autonomous Change 位置为 1b,或速率更改是由下游端口出于自治原因发起的(不是可靠性问题,也不是由软件设置 Link Retrain 位引起的),则 Link Status 寄存器中的 Link Autonomous Bandwidth Status 位置为 1b。

- 否则,Link Bandwidth Management Status 位置为 1b。

_Figure 14-39: Link Status 寄存器_ 

**==> picture [373 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


**597** 

**PCI Ex ress Technolo p gy** 

## _退出到"详细恢复子状态"_

一旦超时到期,下一个状态将是 Recovery.RcvrLock

如果此子状态是从 Recovery.RcvrCfg 进入的,并且速率更改成功,则新数据速率将在所有已配置的 Lane 上更改为最高共同支持的速率,并且 changed_speed_recovery 变量设置为 1b。

如果自从从 L0 或 L1 进入 Recovery 以来第二次进入此子状态(由 changed_speed_recovery = 1b 指示),则新数据速率将是 LTSSM 进入 Recovery 时正在使用的速率,并且 changed_speed_recovery 变量清零至 0b。

否则,新数据速率将恢复为 2.5 GT/s,并且 changed_speed_recovery 变量保持清零至 0b。规范指出,这表示 L0 中的速率大于 2.5 GT/s,但一个链路伙伴无法以该速率运行并在第一次通过时在 Recovery.RcvrLock 中超时的情况。

## _退出到"Detect 状态"_

如果不满足退出到 Recovery.RcvrLock 的任何条件,则下一个状态将是 Detect,虽然规范指出这在正常情况下应该是不可能的。这将意味着链路邻居根本无法再进行通信。

## **Recovery.RcvrCfg** 

只有在接收到至少 8 个具有相同先前协商的 Link 和 Lane 编号的 TS1 或 TS2 有序集之后,才能从 Recovery.RcvrLock 进入此状态。这意味着已建立位、符号或块锁,现在端口必须确定在 Recovery 状态中是否还有任何其他需要处理的项目。如果进入 Recovery 的目的只是要在离开链路电源管理状态后重新建立位和符号锁,那么这里可能会交换 TS2 并继续进行到 Recovery.Idle。但是,如果进入 Recovery 状态有其他原因(例如速率更改或链路宽度更改),则将在此子状态中确定,并发生适当的状态转换。

在此子状态期间,发送器在所有已配置的 Lane 上发送 TS2,具有先前配置的相同 Link 和 Lane 编号。如果 directed_speed_change 变量设置为 1b,则 TS2 中的 speed_change 位也必须被设置。TS2 中的 N_FTS 值应反映当前速率所需的数量。start_equalization_w_preset 变量在进入此子状态时被清零至 0b。

**598** 

**Chapter 14: Link Initialization & Training** 

如果速率已更改,可能会在 TS2 中看到不同的 N_FTS 数字。该值必须用于退出未来的 L0s 低功耗链路状态。对于 8b/10b 编码,必须在离开此子状态之前完成 Lane-to-Lane 去偏移。设备必须注意传入 TS2 中通告的速率标识符,并使用它来覆盖任何先前记录的值。使用 128b/130b 编码时,设备必须记录 Request Equalization 位的值以供将来参考。

关于此子状态的说明:变量 successful_speed_negotiation 被设置为 1b。在此时记录在 TS2 中以 speed_change 位设置的 TS2 中通告的数据速率以供将来参考,以及 Autonomous Change 位以供在 Recovery.Speed 期间可能记录到 Link Status 寄存器中。将在 Recovery.Speed 中选择的速率将是最高共同支持的速率。有趣的是,即使 Link 已经在最高支持的速率下运行,这种情况下也会发生到 Recovery.Speed 的转换,虽然在这种情况下速率实际上不会更改。

如果速率将要更改为 8.0 GT/s,则下游端口将需要发送 EQ TS2(Symbol 6 的位 7 设置为 1b 以指示 EQ 训练序列)。如果共同支持 8.0 GT/s 并且在任何已配置的 Lane 上看到 8 个连续的 speed_change 位设置的 TS1 或 TS2,或者如果 equalization_done_8GT_data_rate 变量为 0b,或者如果已指示,则会识别这种情况。如果当前数据速率为 8.0 GT/s 且均衡过程出现问题,上游端口可以设置 Request Equalization 位。任何一端都可以通过将 Request Equalization 和 Quiesce Guarantee 位都设置为 1b 来请求重新进行均衡。

上游端口根据接收到的 TS2 中的 Selectable De-emphasis 位设置其 select_deemphasis 变量。并且,如果 TS2 是 EQ TS2,则将 start_equalization_w_preset 变量设置为 1b,并使用新信息更新其 Lane Equalization 寄存器(即:更新寄存器中的上游端口发送器预设和接收器预设提示字段)。任何未收到 EQ TS2 的已配置 Lane 将以设计特定的方式选择其 8.0 GT/s 操作的预设值。如果 equalization_done_8GT_data_rate 变量被清零至 0b,或如果已指示,则下游端口必须将 start_equalization_w_preset 变量设置为 1b。

最后,如果使用 128b/130b 编码,设备必须记录 Request Equalization 位的值。如果已设置,则必须将其和 Quiesce Guarantee 位一起存储以供将来参考。

**599** 

**PCI Ex ress Technolo p gy** 

## _退出到"Recovery.Idle"_

如果满足以下两个条件,则下一个状态将是 Recovery.Idle:

- 在任何已配置的 Lane 上接收到 8 个连续的 TS2,具有与正在发送的 Link 和 Lane 编号以及速率标识符相匹配的内容,并且:
   - a) TS2 中的 speed_change 位被清零至 0b,或
   - b) 没有高于 2.5 GT/s 的速率被共同支持。

- 在接收到一个 TS2 后已发送了 16 个 TS2,并且它们没有被任何中间的 EIEOS 中断。changed_speed_recovery 和 directed_speed_change 变量在进入此子状态时都被清零至 0b。

## _退出到"Recovery.Speed"_

如果下面列出的所有三个条件都为真,则 LTSSM 将进入 Recovery.Speed:

- 在任何已配置的 Lane 上接收到 8 个连续的 speed_change 位设置的 TS2,具有相同的速率标识符,Symbol 6 中具有相同的值,并且:
   - a) TS2 是标准的 8b/10b TS2,或
   - b) TS2 是 EQ TS2,或
   - c) 在任何已配置的 Lane 上接收到 8 个 EQ TS2 后已过去 1ms。

- 两个链路伙伴都支持高于 2.5 GT/s 的速率,或者该速率已经高于 2.5 GT/s。

- 对于 8b/10b 编码,在已配置的同一 Lane 上接收到一个 speed_change 位设置为 1b 的 TS2 后,至少已发送 32 个 speed_change 位设置为 1b 的 TS2 而没有任何中间的 EIEOS。对于 128b/130b 编码,在已配置的同一 Lane 上接收到一个 speed_change 位设置为 1b 的 TS2 后,至少已发送 128 个 speed_change 位设置为 1b 的 TS2。

如果自从从 L0 或 L1 进入 Recovery 以来,速率已更改为协商的速率(changed_speed_recovery = 1b),并且任何已配置的 Lane 已看到 EIOS 或检测到/推断出 Electrical Idle,并且自进入此子状态以来未看到 TS2,则也可以发生到 Recovery.Speed 的转换。这意味着尝试了较高的速率,但链路伙伴表明由于某种原因该速率不起作用。新速率将恢复为从 L0 或 L1 进入 Recovery 时的速率。

最后一种可能导致转换到 Recovery.Speed 的情况是,如果自从从 L0 进入 Recovery 以来速率尚未更改为协商的速率

**600** 

**Chapter 14: Link Initialization & Training** 

或 L1(changed_speed_recovery = 0b),并且当前速率已经高于 2.5 GT/s,并且任何已配置的 Lane 已看到 EIOS 或检测到/推断出 Electrical Idle,并且自进入此子状态以来未看到 TS2。在这种情况下,理解是当前速率不起作用,解决方案是降低速率,因此新速率将变为 2.5 GT/s。

## _退出到"Configuration 状态"_

如果在任何已配置的 Lane 上接收到 8 个连续的 TS1,其 Link 或 Lane 编号与正在发送的编号不匹配,并且 speed_change 位被清零至 0b,或没有高于 2.5 GT/s 的速率被共同支持,则下一个状态将是 Configuration。

当 LTSSM 转换到 Configuration 时,变量 changed_speed_recovery 和 directed_speed_change 被清零至 0b。如果 N_FTS 值自上次以来已更改,则必须将新值用于以后的 L0s。

## _退出到"Detect 状态"_

经过 48ms 仍未解析为先前定义的状态转换之一时,如果数据速率为 2.5 GT/s 或 5.0 GT/s,则下一个状态将是 Detect。

如果速率为 8.0 GT/s,则还有另一种可能性,因为尝试次数可能尚未超过。这由 idle_to_rlock_transitioned 变量指示,如果在速率为 8.0 GT/s 时它小于 FFh,则新状态将是"Recovery.Idle"。如果进行此转换,则变量 changed_speed_recovery 和 directed_speed_change 将被清零至 0b。但是,一旦 idle_to_rlock_transitioned 达到 FFh,并且看到 48ms 超时,则下一个状态将是 Detect。

## **Recovery.Idle** 

顾名思义,发送器通常在此子状态中发送 Idles,作为更改为完全操作的 L0 状态的准备。对于 8b/10b 模式,通常在所有 Lane 上发送 Idle 数据,而对于 128b/130b,发送 SDS 以启动数据流,然后在所有 Lane 上发送 Idle 数据符号。

## _退出到"L0 状态"_

如果以下任一情况为真,则下一个状态是 L0。在任一情况下,如果自上次从 Recovery 或 Configuration 转换到 L0 以来,Retrain Link 位已被写入 1b,则下游端口将 Link Bandwidth Management Status 位置为 1b(参见第 597 页的 Figure 14-39)。

- 正在使用 8b/10b 编码,并且已接收到 8 个连续 Symbol Time 的 Idle 数据,并且自接收到第一个以来已发送了 16 个 Idle 数据符号。

**601** 

## **PCI Ex ress Technolo p gy** 

- 正在使用 128b/130b 编码,已接收到 8 个连续 Symbol Time 的 Idle 数据,并且自接收到第一个以来已发送了 16 个 Idle 数据符号,并且此状态不是从 Recovery.RcvrCfg 进入的。请注意,Idle 数据符号必须包含在数据块中,Lane-to-Lane 去偏移必须在数据流处理开始之前完成,并且 idle_to_rlock_transitioned 变量在转换到 L0 时被清零至 00h。

## _退出到"Configuration 状态"_

如果满足以下任一条件,则下一个状态是 Configuration:

- 端口被更高层指示可选地重新配置链路,例如更改链路宽度。

- 任何已配置的 Lane 看到两个连续的传入 TS1,其 Lane 编号设置为 PAD(将转换到 Configuration 以更改链路的端口将在所有 Lane 上发送 PAD Lane 编号)。规范建议 LTSSM 在更改链路宽度时使用此转换,以减少将花费的时间。

## _退出到"Disable 状态"_

如果满足以下任一条件,则下一个状态是 Disabled:

- 下游或可选的 crosslink 端口被更高层指示在其 TS1 或 TS2 中设置 Disable Link 位。

- 上游或可选的 crosslink 端口的任何已配置 Lane 看到两个连续的传入 TS1 中设置了 Disable Link 位。

## _退出到"Hot Reset 状态"_

如果满足以下任一条件,则下一个状态是 Hot Reset:

- 下游或可选的 crosslink 端口被更高层指示在其 TS1 或 TS2 中设置 Hot Reset 位。

- 上游或可选的 crosslink 端口的任何已配置 Lane 看到两个连续的传入 TS1 中设置了 Hot Reset 位。

## _退出到"Loopback 状态"_

如果满足以下任一条件,则下一个状态是 Loopback:

- 已知发送器具有 Loopback Master 能力(设计特定;规范未提供验证方法)并被更高层指示在其 TS1 或 TS2 中设置 Loopback 位。

- 上游或可选的 crosslink 端口的任何已配置 Lane 看到两个连续的传入 TS1 中设置了 Loopback 位。然后接收设备成为 Loopback slave。

**602** 

**Chapter 14: Link Initialization & Training** 

## _退出到"Detect 状态"_

否则,经过 2ms 超时后,下一个状态将是 Detect,除非 idle_to_rlock_transitioned 变量小于 FFh,在这种情况下,下一个状态将是"详细恢复子状态"。对于到 Recovery.RcvrLock 的转换,如果数据速率为 8.0 GT/s,则 idle_to_rlock_transitioned 变量加 1b;而对于 2.5 或 5.0 GT/s,它将被设置为 FFh。

## **L0s 状态** 

这是具有从 L0 返回的最短退出延迟的低功耗链路状态。设备在硬件控制下自动管理此状态的进入和退出,无需任何软件参与。链路的每个方向可以独立于彼此进入和退出 L0s 状态。

## **L0s 发送器状态机** 

L0s 状态对发送器和接收器有不同的子状态。将首先描述发送器子状态。如第 603 页的 Figure 14-40 所示,与 L0s 状态关联的发送器状态机是一个简单的状态机。

_Figure 14-40: L0s Tx 状态机_ 

**==> picture [288 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Tx sends  Transmitter sends<br>EIOS FTSs on all Lanes<br>TTX-IDLE-MIN<br>= 20 ns Tx_L0s.Idle Directed<br>Tx_L0s.Entry Tx_L0s.FTS<br>(Tx Electrical Idle)<br>Transmitter sends<br>SOS or EIEOS<br>Exit to<br>L0<br>**----- End of picture text -----**<br>


**603** 

**PCI Ex ress Technolo p gy** 

## **Tx_L0s.Entry。** 

当上层指示时,发送器进入 L0s。规范未给出此决定的决策标准,但凭直觉,这将基于不活动超时发生:在给定时间内没有发送 TLP 或 DLLP。要进入 L0s,发送器发送一个 EIOS(对于 5.0 GT/s 速率为两个 EIOS)并进入 Electrical Idle。但是,发送器未关闭,必须保持 DC 共模电压在规范范围内。

## _退出到"Tx_L0s.Idle"_

下一个状态将在 TTX-IDLE-MIN 超时(20ns)后是 Tx_L0s.Idle。此时间旨在确保发送器已建立 Electrical Idle 条件。

## **Tx_L0s.Idle。** 

在此子状态中,发送器继续处于 Electrical Idle 状态,直到被指示离开。由于此方向的链路处于 Electrical Idle,因此将带来节能优势,这正是 L0s 状态的整个目的。

_退出到"Tx_L0s.FTS"_

当被指示时(例如当端口需要恢复分组传输时),下一个状态将是 Tx_L0s.FTS。LTSSM 将以设计特定的方式被指示退出此状态。

## **Tx_L0s.FTS。** 

在此子状态中,发送器将开始发送 FTS 有序集以重新训练链路伙伴的接收器。发送的 FTS 数量是链路伙伴在上次训练序列(导致 L0)期间在其 TS 有序集中通告的 N_FTS 值。规范指出,如果接收器在尝试执行此操作时超时,则可以选择在 Recovery 状态期间增加其通告的 N_FTS 值。

如果设置了 Extended Synch 位(参见第 644 页的 Figure 14-71),则发送器必须发送 4096 个 FTS 而不是 N_FTS 数字。这扩展了同步外部测试和分析逻辑的可用时间,这些逻辑可能无法像嵌入式逻辑那样快地恢复位锁。

对于所有数据速率,在发送任何 FTS 之前不能发送 SOS。但是,对于 5.0 GT/s 速率,必须在发送 FTS 之前发送 4 到 8 个 EIE 符号。对于 128b/130b,必须在 FTS 之前发送 EIEOS。

**604** 

**Chapter 14: Link Initialization & Training** 

## _退出到"L0 状态"_

一旦所有 FTS 都已发送,发送器将转换到 L0 状态,并且:

- a) 对于 8b/10b 编码,在所有已配置的 Lane 上发送一个 SOS,尽管在 FTS 之前或期间不发送任何 SOS。

- b) 对于 128b/130b 编码,发送一个 EIEOS,然后是 SDS 和数据流。

## **L0s 接收器状态机** 

Figure 14-41(第 605 页)显示了接收器 L0s 状态机。如果 Link Capability 寄存器中的 ASPM Support 字段显示支持 L0s,则要求接收器实现 L0s 支持;即使未指示支持,允许实现它。

_Figure 14-41: L0s 接收器状态机_ 

**==> picture [327 x 184] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Rx detects<br>EIOS Exit from FTSs Received<br>TTX-IDLE-MIN Electrical<br>= 20 ns Rx_L0s.Idle Idle<br>Rx_L0s.Entry Rx_L0s.FTS<br>(Rx Electrical Idle)<br>Tx sends N_FTS<br>SOS or EIEOS Timeout<br>Exit to Exit to<br>L0 Recovery<br>**----- End of picture text -----**<br>


**605** 

**PCI Ex ress Technolo p gy** 

## **Rx_L0s.Entry。** 

当接收器接收到 EIOS 时进入,前提是它支持 L0s 并且尚未被指示为 L1 或 L2。

_退出到"Rx_L0s.Idle"_

下一个状态将在 TTX-IDLE-MIN 超时(20ns)后是 Rx_L0s.Idle。

## **Rx_L0s.Idle。** 

接收器现在处于 Electrical Idle 模式,只是等待看到退出 Electrical Idle。
