# 📘 第 14 章　链路初始化与训练 (Chapter 14. Link Initialization & Training)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0298.md` ... `chunks/chunk0315.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [14.1 PCI Express Technology — 链路初始化与训练](#sec-14-1)
- [14.2 _Exit to “Detailed Recovery Substates”_ — 链路初始化与训练](#sec-14-2)
- [14.3 Recovery.Speed — 链路初始化与训练](#sec-14-3)
- [14.4 _Exit to “Recovery.Speed”_ — 链路初始化与训练](#sec-14-4)
- [14.5 Rx_L0s.FTS. — 链路初始化与训练](#sec-14-5)
- [14.6 _Exit to “Detect State”_ — 链路初始化与训练](#sec-14-6)
- [14.7 Loopback.Exit — 链路初始化与训练](#sec-14-7)
- [14.8 PCI Express Technology — 链路初始化与训练](#sec-14-8)
- [14.9 PCI Express Technology — 链路初始化与训练](#sec-14-9)
- [14.10 This Chapter — 链路初始化与训练](#sec-14-10)
- [14.11 PCIe Error Checking Mechanisms — 链路初始化与训练](#sec-14-11)
- [14.12 Variant Bits Not Included in ECRC Mechanism — 链路初始化与训练](#sec-14-12)
- [14.13 Unexpected Completion — 链路初始化与训练](#sec-14-13)
- [14.14 Advisory Non-Fatal Cases — 链路初始化与训练](#sec-14-14)
- [14.15 Baseline Error Handling — 链路初始化与训练](#sec-14-15)
- [14.16 Link Errors — 链路初始化与训练](#sec-14-16)
- [14.17 PCI Express Technology — 链路初始化与训练](#sec-14-17)
- [14.18 Root Complex Error Tracking and Reporting — 链路初始化与训练](#sec-14-18)

<a id="sec-14-1"></a>
## 14.1 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The DSP performs the same actions as the USP and achieves a BER of 10[‐4] by detecting back‐to‐back TS1s. During this time, the DSP communicates its Tx presets and FS (Full Swing), LF (Low Frequency), and Post‐cursor coefficient values as shown in Figure 14‐32 on page 584. The spec gives some additional rules that must be satisfied for a set of requested coefficients, which are: 

1. |C‐1| <= Floor (FS/4), (Note: Floor means round down to the integer value) 2. |C‐1| + C0 + |C+1| = FS 

3. C0 ‐ |C‐1| ‐ |C+1| >= LF 

## **PCI Express Technology** 

FS represents the maximum voltage, and LF defines the minimum voltage as LF/FS. These inform the receiver about the number of possible values and allow the coefficients to be communicated as integer values but understood as frac‐ tional values. 

As an example, assume we’re using the coefficients defined for the P7 preset set‐ ting. The FS value acts as a reference and can be any number up to 63 but, for ease of calculation, let’s say it’s given as 30. In the case of P7, C‐1 is ‐0.1, the value communicated to represent C‐1 in the TS1s would be 3, since 3/30 = 0.1 and always considered negative. C+1 is ‐0.2, so it would be communicated as 6, since 6/30 = 0.2 and always negative. C0 is 0.7, so that will be sent as 21, since 21/30 = 0.7. Finally, the LF value represents the smallest possible ratio, and for P7 that is 0.4 times the max value. Consequently, LF will be communicated as 12, since 12/ 30 = 0.4. 

Armed with this information, let’s check the three rules to see whether they are satisfied for the P7 case: 

1. 3 <= Floor (12/4), This works out to be 3 <= 3 and is true. 

2. 3 + 21 + 6 = 30 This one is true. 

3. 21 ‐ 3 ‐ 6 >= 12 This one is also true, so all three checks are satisfied for P7. 

Once the Downstream Port is satisfied that the Link is working well enough to move forward (it recognizes incoming TS1s with EC = 01b), then this phase is complete and it initiates a change to Phase 2 by setting its EC = 10b as illustrated in Figure 14‐31 on page 583 and hands control of the next step back to the USP. When the USP responds with EC = 10b, both Ports go to Phase 2. As a happy alternative, the Downstream Port may conclude that the signal quality is already good enough at this point and no further adjustments are necessary. In that case, it set its EC = 00b to exit the equalization process. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐31: Equalization Process: Initiating Phase 2_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Phase 2** 

The signal quality has been good enough to recognize TS1s, but not good enough for runtime operation. Once both Ports are in Phase 2, the Upstream Port is allowed to request Tx settings for the Downstream Port and then evalu‐ ate how well they work, reiterating the process until it arrives at optimal set‐ tings for the current environment. To make a request, it changes the value of the equalization information it sends in its TS1s. As shown in Figure 14‐32 on page 584, there are several values of interest: 

- **Tx Preset:** The Tx presets are a coarse‐grained adjustment to the Transmitter settings that are intended to get it into the right ballpark for the current sig‐ naling environment. The Upstream Port sets this value, and sets the “Use Preset” indicator (bit 7 of Symbol 6) to tell the Downstream Port’s Transmit‐ ter to use it. If the Use Preset bit is not set, then it’s understood that the pre‐ sets should stay as they are and that the coefficient values should be changed instead. The Tx coefficients are considered as fine‐grained adjust‐ ments. 

## **PCI Express Technology** 

_Figure 14‐32: Equalization Coefficients Exchanged_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


- **Coefficients:** Since the spec requires a 3‐tap Tx equalizer, three coefficient values are defined that can be pictured as voltage adjustments to a signal pulse that compensates for the distortion it will experience going through the transmission medium, as shown in Figure 14‐33 on page 585. This is covered in more detail in the Physical Layer Electrical section titled, “Solu‐ tion for 8.0 GT/s ‐ Transmitter Equalization” on page 474. 

- **Pre‐Cursor Coefficient:** a multiplier applied to the signal prior to the sam‐ ple point that can boost or reduce the signal depending on the need. 

- **Cursor Coefficient:** the sample point multiplier; always positive. 

- **Post‐Cursor Coefficient:** a multiplier applied to the signal after the sample point that can boost or reduce the signal depending on the need. 

- Once the signal meets the quality standard needed, the Upstream Port indicates that it’s ready to move to the next phase by changing EC = 11b. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐33: 3‐Tap Transmitter Equalization_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


_Figure 14‐34: Equalization Process: Adjustments During Phase 2_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Phase 3** 

The Downstream port responds by sending EC = 11b and can now do the same signal evaluation process for the Upstream Port’s Transmitter. It sends TS1s that request a new setting the same way: if the Use Preset bit is set, new presets are defined, otherwise new coefficients are being given. This is sent continuously for 1  s or until the request has been evaluated for its result, whichever is later. That evaluation must wait 500ns plus the round trip time through the outgoing logic and back in to the receive logic. Different equalization settings can be tested until one is found that achieves the desired signal quality. At that point the Downstream Port exits the equalization process by setting EC = 00b. 

_Figure 14‐35: Equalization Process: Adjustments During Phase 3_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Equalization Notes** 

The specification mentions other items associated with the equalization process, as described below: 

- All Lanes must participate in the process; even those that may only become active later after an upconfigure event. 

- The algorithm used by a component to evaluate the incoming signal and determine the equalization values that its Link partner should use is not given in the spec and is implementation specific. 

**Chapter 14: Link Initialization & Training** 

- Equalization changes can be requested for any number of Lanes and the Lanes can use different values. 

- At the end of the fine‐tuning steps (Phase 2 for Upstream Ports and Phase 3 for Downstream Ports), each component is responsible for ensuring that the Transmitter settings cause it to meet the spec requirements. 

- Components must evaluate requests to adjust their Transmitter settings and act on them. If valid values are given they must use them and reflect those values in the TS1s they send. 

- A request to adjust coefficients may be rejected if the values are not compli‐ ant with the rules. The requested values will still be reflected in the TS1s sent back but the Reject Coefficient Values bit will be set. 

- Components must store the equalization values that they settled on through this process for future use at 8.0 GT/s. The spec is not explicit on this, but the author’s opinion is that these values would survive a change in speed to a lower rate and then back to the 8.0 GT/s rate. That makes sense because it could potentially take a long time to repeat the EQ process and the resulting values would be the same, provided the electrical environ‐ ment hasn’t changed. 

- Components are allowed to fine‐tune their Receivers at any time, as long as it doesn’t cause the Link to become unreliable or go to Recovery. 

## **Detailed Equalization Substates** 

This section covers detailed descriptions of the state machine behaviors during Link Equalization. 

## **Recovery.Equalization** 

This substate is used to execute the Link Equalization Procedure for 8.0 GT/s and higher rates. The lower rates don’t use equalization and the LTSSM won’t enter this substate when they’re in effect. Since this is a new and complex topic for PCIe, a description of the overall equalization procedure from a high‐level view is presented after the state machine details in the section called “Link Equalization Overview” on page 577. First though, let’s step through the sub‐ states to see the mechanics of the process. 

## **Downstream Lanes** 

The Downstream Port starts in Phase 1 of the equalization process. To begin this process, there are several bits that need to be reset. In the Link Status 2 register (Figure 14‐36 on page 588), the following bits are cleared when entering this substate: 

- Equalization Phase 1 Successful 

- Equalization Phase 2 Successful 

- Equalization Phase 3 Successful 

- Link Equalization Request 

- Equalization Complete 

The Perform Equalization bit of the Link Control 3 register is also cleared to 0b as is the internal variable start_equalization_w_preset. The equalization_done_8GT_data_rate variable is set to 1b. 

_Figure 14‐36: Link Status 2 Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


_Figure 14‐37: Link Control 3 Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**Chapter 14: Link Initialization & Training** 

**Phase 1 Downstream.** During this phase, the Downstream Port sends TS1s with EC = 01b while using the Preset values from the Lane Equaliza‐ tion Control register and with the FS, LF, and Post‐cursor Coefficient fields that correspond to the Tx Preset field. It’s allowed to wait 500ns before eval‐ uating incoming TS1s if it needs time to stabilize its Receiver logic. 

## _Exit to “Phase 2 Downstream”_

</td>
<td style="background-color:#e8e8e8">

_退出至 "Recovery.Speed"_

否则，在 24ms 超时后（容差为 ‐0 或 +2ms），下一状态将为 Recovery.Speed，successful_speed_negotiation 标志被清除为 0b，同时 Equalization Complete 状态位被设置为 1b。

**Phase 3 Upstream。** 在此阶段，上游端口发送 EC = 11b 的 TS1，并响应来自下游端口的 Tx 值请求。

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

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


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

**Chapter 14: Link Initialization & Training**

如果速度已更改，则 TS2 中现在可能会看到不同的 N_FTS 数字。该值必须用于退出将来的 L0s 低功耗链路状态。对于 8b/10b 编码，必须在离开此子状态之前完成 Lane 间去偏斜。设备必须注意传入 TS2 中通告的速率标识符，并使用它来覆盖任何先前记录的值。使用 128b/130b 编码时，设备必须注意 Request Equalization 位的值以供将来参考。

有关此子状态的说明：变量 successful_speed_negotiation 被设置为 1b。此时注意到 TS2 中以 speed_change 位置位通告的数据速率以供将来参考，并且 Autonomous Change 位用于在 Recovery.Speed 期间在 Link Status 寄存器中可能记录日志。将在 Recovery.Speed 中选择的速率是最高共同支持的速率。有趣的是，在这种情况下即使链路已经以最高支持的速率运行，仍会发生到 Recovery.Speed 的更改，尽管在这种情况下速率实际上不会改变。

如果速度将更改为 8.0 GT/s，则下游端口将需要发送 EQ TS2（Symbol 6 的位 7 设置为 1b 以指示 EQ 训练序列）。如果 8.0 GT/s 是共同支持的，并且在任何已配置的 Lane 上看到 8 个连续的 speed_change 位置位的 TS1 或 TS2，或者 equalization_done_8GT_data_rate 变量为 0b，或者被指示，则将识别这种情况。如果当前数据速率为 8.0 GT/s 且均衡过程存在问题，则上游端口可以设置 Request Equalization 位。任何一端都可以通过将 Request Equalization 和 Quiesce Guarantee 位都设置为 1b 来请求再次执行均衡。

上游端口根据接收到的 TS2 中的 Selectable De-emphasis 位设置其 select_deemphasis 变量。并且，如果 TS2 是 EQ TS2，则它们将 start_equalization_w_preset 变量设置为 1b，并使用新信息更新其 Lane Equalization 寄存器（即：更新寄存器中的 Upstream Port Transmitter Preset 和 Receiver Preset Hint 字段）。任何未接收到 EQ TS2 的已配置 Lane 将以设计特定的方式选择其 8.0 GT/s 操作的预设值。如果 equalization_done_8GT_data_rate 变量被清除为 0b 或被指示，则下游端口必须将其 start_equalization_w_preset 变量设置为 1b。

最后，如果使用 128b/130b 编码，则设备必须注意 Request Equalization 位的值。如果已设置，则必须将其与 Quiesce Guarantee 位一起存储以供将来参考。

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

## **PCI Express Technology**

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

**Chapter 14: Link Initialization & Training**

## _退出至 "Detect 状态"_

否则，在 2ms 超时后，下一状态将为 Detect，除非 idle_to_rlock_transitioned 变量小于 FFh，在这种情况下下一状态将为 "详细的 Recovery 子状态"。对于到 Recovery.RcvrLock 的转换，如果数据速率为 8.0 GT/s，则 idle_to_rlock_transitioned 变量加 1b，而对于 2.5 或 5.0 GT/s，它将被设置为 FFh。

## **L0s 状态**

这是具有到 L0 的最短退出延迟的低功耗链路状态。设备在硬件控制下自动管理此状态的进入和退出，无需任何软件参与。链路的每个方向可以独立地进入和退出 L0s 状态。

## **L0s 发送器状态机**

L0s 状态对于发送器和接收器具有不同的子状态。将首先描述发送器子状态。如 603 页 Figure 14‐40 所示，与 L0s 状态关联的发送器状态机是一个简单的状态机。

_Figure 14‐40: L0s Tx State Machine_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


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

**Chapter 14: Link Initialization & Training**

## _退出至 "L0 状态"_

一旦已发送所有 FTS，发送器将转换到 L0 状态，并且：

- a) 对于 8b/10b 编码，一个 SOS 在所有已配置的 Lane 上发送，尽管在 FTS 之前或期间不发送任何 SOS。

- b) 对于 128b/130b 编码，发送一个 EIEOS 后跟一个 SDS 和 Data Stream。

## **L0s 接收器状态机**

605 页 Figure 14‐41 显示了接收器 L0s 状态机。如果 Link Capability 寄存器中的 ASPM Support 字段显示支持 L0s，则接收器需要实现 L0s 支持，即使未指示支持也允许实现。

_Figure 14‐41: L0s Receiver State Machine_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Rx_L0s.Entry**

当接收器接收到 EIOS 时进入，前提是它支持 L0s 并且未被引导至 L1 或 L2。

_退出至 "Rx_L0s.Idle"_

下一状态将在 TTX-IDLE-MIN 超时（20ns）后为 Rx_L0s.Idle。

## **Rx_L0s.Idle**

接收器现在处于 Electrical Idle 模式，并且只是等待看到退出 Electrical Idle。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0684_img2_tight.png" alt="Figure from page 684" width="700">

<a id="sec-14-2"></a>
## 14.2 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The Downstream Port will transition to Phase 2 if it want to continue with the equalization process and when all configured Lanes receive two consecutive TS1s with EC = 01b. At this point, the Port will set the Equalization Phase 1 Successful status bit to 1b and store the received TS1 LF and FS values for use in Phase 3 (if the Downstream Port plans to adjust the Upstream Port’s Tx coefficients). 

## _Exit to “Detailed Recovery Substates”_ 

If the Downstream Port doesn’t want to use Phases 2 and 3, it sets the status bits to 1b (Eq. Phase 1 Successful, Eq. Phase 2 Successful, Eq. Phase 3 Successful, and Eq. Complete). One reason to do this would be because it can already see that the signal characteristics are good enough and the rest of the phases aren’t needed. 

## _Exit to “Recovery.Speed”_ 

If the consecutive TS1s are not seen after a 24ms timeout, the next state is Recovery.Speed. The successful_speed_negotiation flag is cleared to 0b, and the Equalization Complete status bit is set to 1b. 

**Phase 2 Downstream.** During this phase, the Downstream Port sends TS1s with EC = 10b and coefficient settings independently assigned on each Lane according to the following: 

- If two consecutive TS1s are received with EC = 10b (Upstream Port has entered Phase 2) either for the first time, or with different preset or coefficient values than the last time, and if the values requested are legal and supported, then change the Tx settings to use them within 500ns of the end of the second TS1 requesting them. Also, reflect the values in the TS1s being sent back to the Upstream Port and clear the Reject Coefficient Values bit to 0b. Note that the change must not cause illegal voltages or parameters at the Transmitter for more than 1ns. 

 - a) If the requested preset or coefficients are illegal or not supported, don’t change the Tx settings but reflect the received values in the 

TS1s being sent and set the Reject Coefficient Values bit to 1b (seeFigure 14‐38 on page 590). 

- If the two consecutive TS1s aren’t seen, keep the current Tx preset and coefficient values. 

## _Exit to “Phase 3 Downstream”_ 

When the Upstream Port is satisfied with the changes, it begins to send TS1s with EC = 11b, indicating a desire to change to Phase 3. When two consecu‐ tive TS1s like this are received, set the Eq. Phase 2 Successful status bit to 1b and change to Phase 3. 

## _Exit to “Recovery.Speed”_ 

If after 32 ms, the transition to Phase 3 has not happened, the Port should clear the successful_speed_negotiation flag, set the Equalization Complete status bit and exit to the Recovery.Speed substate. 

_Figure 14‐38: TS1s ‐ Rejecting Coefficient Values_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**Chapter 14: Link Initialization & Training** 

**Phase 3 Downstream.** During this phase, the Downstream Port sends TS1s with EC = 11b and begins the process of evaluating Upstream Tx set‐ tings independently for each Lane. 

In the transmitted TS1s, the Downstream Port can either request a new pre‐ set by setting the Use Preset bit to 1b and Tx Preset field to the desired value, or it can request new coefficients by clearing the Use Preset bit to 0b and setting the Pre‐cursor, Cursor, and Post‐Cursor Coefficient fields to the desired values. Either request must be made continuously for at least 1  s or until the evaluation has completed. If new preset or coefficient settings are going to be presented, they must be sent on all Lanes at the same time. However, a given Lane isn’t required to request new settings if it wants to keep the ones it has. 

The Downstream Port must wait long enough to ensure the Upstream Transmitter has had a chance to implement the requested changes, (500ns plus the round‐trip delay for the logic), then obtain Block Alignment and evaluate the incoming TS1s. It’s not expected that anything useful will be coming from the Upstream Port during the waiting period, and it may not even be legal. That’s why obtaining Block Alignment after that time is a requirement. 

If two consecutive TS1s are seen that match the same preset or coefficient values that are being requested and don’t have the Reject Coefficient Values bit set, then the requested setting was accepted and can be evaluated. If the values match but the Reject Coefficient Values bit is set to 1b, then the requested values have been rejected by the Upstream Port and are not being used. For this case, he spec recommends that the Downstream Port try again with different values but it’s not required to do so and may choose to simply exit this phase. 

The total time spent on a preset or coefficient request, from the time the request is sent until the completion of its evaluation must be less than 2ms. An exception is available for designs that need more time for the final stage of optimization, but the total time in this phase cannot exceed 24ms and the exception can only be taken twice. If the Receiver doesn’t recognize any incoming TS1s, it may assume that the requested setting doesn’t work for that Lane. 

## _Exit to “Detailed Recovery Substates”_ 

The next state will be Recovery.RcvrLock when all configured Lanes have their optimal settings. When that happens, the Equalization Phase 3 Successful and Equalization Complete status bits will be set to 1b. 

_Exit to “Recovery.Speed”_ 

Otherwise, after a 24ms timeout (with a tolerance of ‐0 or +2ms), the next state will be Recovery.Speed, and the successful_speed_negotiation flag is cleared to 0b while the Equaliza‐ tion Complete status bit is set to 1b. 

## **Upstream Lanes** 

The Upstream Port starts in Phase 0 of the equalization process and must reset several internal bits. In the Link Status 2 register (Figure 14‐36 on page 588), the following bits are cleared when entering this substate: 

- Equalization Phase 1 Successful 

- Equalization Phase 2 Successful 

- Equalization Phase 3 Successful 

- Link Equalization Request 

- Equalization Complete 

The Perform Equalization bit of the Link Control 3 register is also cleared to 0b as is the internal variable start_equalization_w_preset. The equalization_done_8GT_data_rate variable is set to 1b. 

**Phase 0 Upstream.** During this phase, the Upstream Port sends TS1s with EC = 00b while using the Tx Preset values that were delivered in the EQ TS2s before entering this state. The equalization information fields in the TS1s being sent must show the preset value and also the Pre‐cursor, Cursor, and Post‐cursor coefficient fields that correspond to that preset. Note that if a Lane received a reserved or unsupported Tx Preset value in the EQ TS2s, or no EQ TS2s at all, then the Tx Preset field and coefficient values are cho‐ sen by a device‐specific method for that Lane. 

_Exit to “Phase 1 Upstream”_ 

When all configured Lanes receive two consecutive TS1s with EC = 01b, indicating that they can recognize the TS1s from the Downstream Port which always starts with this value, then the next phase is Phase 1. 

The equalization values LF and FS that are received in the TS1s must be stored and used during Phase 2 if the Upstream Port plans to adjust the Downstream Port’s Tx coefficients. 

Upstream Port may wait 500ns after entering Phase 0 before evaluating the incoming TS1s to give time for its Receiver logic to stabilize. 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Recovery.Speed”_ 

If incoming TS1s are not recognized within a 12ms timeout, the LTSSM will transition to Recovery.Speed, clear the successful_speed_negotiation flag and set the Equalization Complete status bit. 

**Phase 1 Upstream.** During this phase, the Upstream Port send TS1s with EC = 01b while using the Transmitter settings that were determined in Phase 0. These TS1s contain the FS, LF, and Post‐cursor Coefficient values with what is currently being used. 

## _Exit to “Phase 2 Upstream”_ 

If all configured Lanes receive two consecutive TS1s with EC = 10b, indicating that the Downstream Port wants to go to Phase 2, then the next phase will be Phase 2, and this Port will set the Equalization Phase 1 Successful status bit. 

_Exit to “Detailed Recovery Substates”_ 

If all configured Lanes receive two consecutive TS1s with EC = 00b, it means that the Downstream Port has decided that the equalization pro‐ cess is already complete and it wants to skip the remaining phases. In this case, the next state will be Recovery.RcvrLock, and the Equalization Phase 1 Successful and Equalization Complete status bits are set to 1b. 

## _Exit to “Recovery.Speed”_ 

Otherwise, after a 12ms timeout, the LTSSM will transition to Recov‐ ery.Speed, clear the successful_speed_negotiation flag and set the Equalization Complete status bit. 

**Phase 2 Upstream.** During this phase, the Upstream Port sends TS1s with EC = 10b and begins the process of finding optimal Tx values for the Down‐ stream Port. Recall that the settings are independently determined for each Lane. The process is as follows: 

In the transmitted TS1s, the Upstream Port can either request a new preset by putting a legal value in the Transmitter Preset field of the TS1s being sent and setting the Use Preset bit to 1b to tell the Downstream Port to begin using it. Or, request new coefficients by putting legal values in those fields and clearing the Use Preset bit to 0b so the Downstream Port will load them instead of the preset field. Once the request is made it must be repeated for 

at least 1  s or until the evaluation is complete. If new preset or coefficient settings are going to be presented, they must be sent on all Lanes at the same time. However, a given Lane isn’t required to request new settings if it wants to keep the ones it has. 

The Upstream Port must wait long enough to ensure the Downstream Transmitter has had a chance to implement the requested changes, (500ns plus the round‐trip delay for the logic), then obtain Block Alignment and evaluate the incoming TS1s. It’s not expected that anything useful will be coming from the Downstream Port during the waiting period, and it may not even be legal. That’s why obtaining Block Alignment after that time is a requirement. 

When TS1s are received that contain the same equalization fields as are being sent and the Reject Coefficient Values bit is not set (0b), then the set‐ ting has been accepted and can now be evaluated. If the equalization fields match but the Reject Coefficient Values bit is set (1b), then the setting has been rejected. In that case the spec recommends that the Upstream Port request a different equalization setting, but this is not required. 

The total time spent on a preset or coefficient request, from the time the request is sent until the completion of its evaluation must be less than 2ms. An exception is available for designs that need more time for the final stage of optimization, but the total time in this phase cannot exceed 24ms and the exception can only be taken twice. If the Receiver doesn’t recognize any incoming TS1s, it may assume that the requested setting doesn’t work for that Lane. 

_Exit to “Phase 3 Upstream”_ 

The next phase is Phase 3 if all configured Lanes have their optimal set‐ tings. When that happens, the Equalization Phase 2 Successful status bit will be set to 1b.

</td>
<td style="background-color:#e8e8e8">

下游端口 (Downstream Port) 如果希望继续进行均衡过程,以及当所有已配置的 Lane 接收到两个连续的 EC = 01b 的 TS1 时,将转换到 Phase 2。此时,该端口将 Equalization Phase 1 Successful 状态位置为 1b,并存储接收到的 TS1 LF 和 FS 值,以供 Phase 3 使用(如果下游端口计划调整上游端口的 Tx 系数)。

## _退出到"详细恢复子状态"_

如果下游端口不希望使用 Phase 2 和 Phase 3,则将状态位都置为 1b(Eq. Phase 1 Successful、Eq. Phase 2 Successful、Eq. Phase 3 Successful 和 Eq. Complete)。这样做的原因之一是它已经能够看到信号特性足够好,其余阶段不需要了。

## _退出到"Recovery.Speed"_

如果在 24ms 超时后未看到连续的 TS1,则下一个状态是 Recovery.Speed。successful_speed_negotiation 标志被清除为 0b,Equalization Complete 状态位被置为 1b。

**Phase 2 下游端口。** 在此阶段,下游端口发送 EC = 10b 的 TS1,并根据以下规则在每个 Lane 上独立分配系数设置:

- 如果接收到两个连续的 EC = 10b 的 TS1(上游端口已进入 Phase 2),无论是第一次收到,还是与上次预设或系数值不同,并且如果请求的值是合法且受支持的,那么在第二个 TS1 请求结束后的 500ns 内将 Tx 设置更改为使用这些值。此外,在发回上游端口的 TS1 中反映这些值,并将 Reject Coefficient Values 位清零至 0b。请注意,此更改不得导致发送器上的电压或参数非法超过 1ns。

 - a) 如果请求的预设或系数是非法或不受支持的,则不更改 Tx 设置,但在发送的 TS1 中反映接收到的值,并将 Reject Coefficient Values 位置为 1b(参见第 590 页的 Figure 14-38)。

- 如果未看到两个连续的 TS1,则保持当前的 Tx 预设和系数值。

## _退出到"Phase 3 下游端口"_

当上游端口对更改满意时,它将开始发送 EC = 11b 的 TS1,表示希望更改为 Phase 3。当接收到两个这样的连续 TS1 时,将 Eq. Phase 2 Successful 状态位置为 1b,并更改为 Phase 3。

## _退出到"Recovery.Speed"_

如果在 32ms 之后,Phase 3 的转换尚未发生,则该端口应清除 successful_speed_negotiation 标志,设置 Equalization Complete 状态位并退出到 Recovery.Speed 子状态。

_Figure 14-38: TS1 - 拒绝系数值_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**Chapter 14: Link Initialization & Training** 

**Phase 3 下游端口。** 在此阶段,下游端口发送 EC = 11b 的 TS1,并开始为每个 Lane 独立评估上游端口的 Tx 设置。

在传输的 TS1 中,下游端口可以通过将 Use Preset 位置为 1b 并将 Tx Preset 字段设置为所需值来请求新的预设,或者通过将 Use Preset 位清零至 0b 并将 Pre-cursor、Cursor 和 Post-Cursor Coefficient 字段设置为所需值来请求新的系数。任何请求必须持续至少 1µs,或直到评估完成。如果要呈现新的预设或系数设置,则必须同时在所有 Lane 上发送。但是,如果给定 Lane 希望保留其当前设置,则不要求它请求新设置。

下游端口必须等待足够长的时间以确保上游发送器有机会实现请求的更改(500ns 加上逻辑的往返延迟),然后获取 Block Alignment 并评估传入的 TS1。在等待期间,预计不会有任何有用的内容来自上游端口,甚至可能是不合法的。这就是为什么之后获取 Block Alignment 是必需的原因。

如果看到两个连续的 TS1 与正在请求的相同预设或系数值匹配,并且 Reject Coefficient Values 位未设置,则请求的设置已被接受并可以评估。如果值匹配但 Reject Coefficient Values 位置为 1b,则请求的值已被上游端口拒绝且未被使用。对于这种情况,规范建议下游端口使用不同的值再试一次,但不要求这样做,也可以选择直接退出此阶段。

从请求发送之时到其评估完成之时,每个预设或系数请求所花费的总时间必须小于 2ms。对于在最终优化阶段需要更多时间的设计,可以有一个例外,但此阶段的总时间不能超过 24ms,并且该例外只能使用两次。如果接收器未识别任何传入的 TS1,则可以假设所请求的设置对该 Lane 不起作用。

## _退出到"详细恢复子状态"_

当所有已配置的 Lane 都具有最佳设置时,下一个状态将是 Recovery.RcvrLock。发生这种情况时,Equalization Phase 3 Successful 和 Equalization Complete 状态位将置为 1b。

_退出到"Recovery.Speed"_

否则,经过 24ms 超时(容差为 -0 或 +2ms)后,下一个状态将是 Recovery.Speed,successful_speed_negotiation 标志被清零至 0b,而 Equalization Complete 状态位置为 1b。

## **上游 Lane** 

上游端口从均衡过程的 Phase 0 开始,必须重置若干内部位。在 Link Status 2 寄存器(第 588 页的 Figure 14-36)中,以下位在进入此子状态时被清除:

- Equalization Phase 1 Successful 

- Equalization Phase 2 Successful 

- Equalization Phase 3 Successful 

- Link Equalization Request 

- Equalization Complete 

Link Control 3 寄存器的 Perform Equalization 位也被清零至 0b,内部变量 start_equalization_w_preset 也被清零。变量 equalization_done_8GT_data_rate 被置为 1b。

**Phase 0 上游端口。** 在此阶段,上游端口发送 EC = 00b 的 TS1,同时使用在进入此状态之前的 EQ TS2 中传递的 Tx Preset 值。正在发送的 TS1 中的均衡信息字段必须显示预设值以及与该预设对应的 Pre-cursor、Cursor 和 Post-cursor 系数字段。注意,如果 Lane 在 EQ TS2 中接收到保留或不受支持的 Tx Preset 值,或者根本没有收到 EQ TS2,则 Tx Preset 字段和系数值由该 Lane 的设备特定方法选择。

_退出到"Phase 1 上游端口"_

当所有已配置的 Lane 收到两个连续的 EC = 01b 的 TS1,表明它们可以识别始终以该值开始的来自下游端口的 TS1 时,下一个阶段是 Phase 1。

在 TS1 中接收到的均衡值 LF 和 FS 必须被存储并用于 Phase 2,如果上游端口计划调整下游端口的 Tx 系数的话。

上游端口在进入 Phase 0 之后,在评估传入的 TS1 之前可以等待 500ns,以便其接收器逻辑有时间稳定。

**Chapter 14: Link Initialization & Training** 

## _退出到"Recovery.Speed"_

如果在 12ms 超时内未识别出传入的 TS1,则 LTSSM 将转换到 Recovery.Speed,清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 1 上游端口。** 在此阶段,上游端口发送 EC = 01b 的 TS1,同时使用在 Phase 0 中确定的发送器设置。这些 TS1 包含当前正在使用的 FS、LF 和 Post-cursor Coefficient 值。

## _退出到"Phase 2 上游端口"_

如果所有已配置的 Lane 接收到两个连续的 EC = 10b 的 TS1,表明下游端口希望转到 Phase 2,则下一个阶段将是 Phase 2,并且此端口将设置 Equalization Phase 1 Successful 状态位。

_退出到"详细恢复子状态"_

如果所有已配置的 Lane 接收到两个连续的 EC = 00b 的 TS1,这意味着下游端口已决定均衡过程已经完成,并希望跳过剩余的阶段。在这种情况下,下一个状态将是 Recovery.RcvrLock,并且 Equalization Phase 1 Successful 和 Equalization Complete 状态位置为 1b。

## _退出到"Recovery.Speed"_

否则,经过 12ms 超时后,LTSSM 将转换到 Recovery.Speed,清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 2 上游端口。** 在此阶段,上游端口发送 EC = 10b 的 TS1,并开始为下游端口寻找最佳 Tx 值的过程。请记住,设置是为每个 Lane 独立确定的。过程如下:

在传输的 TS1 中,上游端口可以通过在正在发送的 TS1 的 Transmitter Preset 字段中放入合法值并将 Use Preset 位置为 1b 来请求新的预设,以告诉下游端口开始使用它。或者,通过在这些字段中放入合法值并将 Use Preset 位清零至 0b 来请求新系数,以便下游端口加载它们而不是预设字段。一旦发出请求,必须重复

至少 1µs,或直到评估完成。如果要呈现新的预设或系数设置,则必须同时在所有 Lane 上发送。但是,如果给定 Lane 希望保留其当前设置,则不要求它请求新设置。

上游端口必须等待足够长的时间以确保下游发送器有机会实现请求的更改(500ns 加上逻辑的往返延迟),然后获取 Block Alignment 并评估传入的 TS1。在等待期间,预计不会有任何有用的内容来自下游端口,甚至可能是不合法的。这就是为什么之后获取 Block Alignment 是必需的原因。

当接收到包含与正在发送的均衡字段相同且 Reject Coefficient Values 位未设置(0b)的 TS1 时,则该设置已被接受并可以评估。如果均衡字段匹配但 Reject Coefficient Values 位置为 1b,则该设置已被拒绝。在这种情况下,规范建议上游端口请求不同的均衡设置,但这不是必需的。

从请求发送之时到其评估完成之时,每个预设或系数请求所花费的总时间必须小于 2ms。对于在最终优化阶段需要更多时间的设计,可以有一个例外,但此阶段的总时间不能超过 24ms,并且该例外只能使用两次。如果接收器未识别任何传入的 TS1,则可以假设所请求的设置对该 Lane 不起作用。

_退出到"Phase 3 上游端口"_

如果所有已配置的 Lane 都具有最佳设置,则下一个阶段是 Phase 3。发生这种情况时,Equalization Phase 2 Successful 状态位将置为 1b。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0684_img1.png" alt="Figure from page 684" width="700">

<a id="sec-14-3"></a>
## 14.3 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

_Exit to “Recovery.Speed”_ 

Otherwise, after a 24ms timeout (with a tolerance of ‐0 or +2ms), the next state will be Recovery.Speed, and the successful_speed_negotiation flag is cleared to 0b while the Equaliza‐ tion Complete status bit is set to 1b. 

**Phase 3 Upstream.** During this phase, the Upstream Port sends TS1s with EC = 11b and responds to the requested Tx values from the Downstream Port. 

**Chapter 14: Link Initialization & Training** 

If two consecutive TS1s aren’t seen, keep the current Tx preset and coeffi‐ cient values. However, if two consecutive TS1s are received with EC = 11b (Downstream Port has entered Phase 3) either for the first time, or with dif‐ ferent preset or coefficient values than the last time, and if the values requested are legal and supported, then change the Tx settings to use them within 500ns of the end of the second TS1 requesting them. The requested values must be reflected in the TS1s being sent back to the Upstream Port and clear the Reject Coefficient Values bit to 0b. Note that the change must not cause illegal voltages or parameters at the Transmitter for more than 1ns. 

- If the requested preset or coefficients are illegal or not supported, don’t change the Tx settings but reflect the received values in the TS1s being sent and set the Reject Coefficient Values bit to 1b (see Figure 14‐38 on page 590). 

_Exit to “Detailed Recovery Substates”_ 

When the Downstream Port is satisfied with the changes, it begins to send TS1s with EC = 00b, indicating a desire to finish the equalization process. When two consecutive TS1s like this are received, set the Equalization Phase 3 Successful and Equalization Complete status bits to 1b. 

_Exit to “Recovery.Speed”_ 

If the above criteria are not met within a 32 ms timeout, the next state will be Recovery.Speed. The successful_speed_negotiation flag will be cleared to 0b and the Equalization Complete status bit will be set. 

## **Recovery.Speed** 

When entering this substate, a device must enter Electrical Idle on its Trans‐ mitter and wait for its Receiver to enter Electrical Idle. After that, it must remain there for at least 800ns if the speed change succeeded (successful_speed_negotiation = 1b) or for at least 6  s if the speed change was not successful (successful_speed_negotiation = 0b), but not longer than an additional 1ms. 

An EIOS must be sent prior to entering this substate if the current rate is 2.5 GT/s or 8.0 GT/s, and two must be sent if the current rate is 5.0 GT/s. An Electrical Idle condition exists on a Lane when these EIOSs have been seen or when it is otherwise detected or inferred (as described in “Electrical Idle” on page 736). 

The operating frequency is only allowed to change after the Receiver Lanes have entered Electrical Idle. If the Link is already operating at the highest commonly‐supported rate, the rate won’t be changed even though this sub‐ state is executed. 

If the negotiated rate is 5.0 GT/s, the de‐emphasis level must be selected based on the setting of the select_deemphasis variable: if the variable is 0b, apply ‐6 dB de‐emphasis, but if the variable is 1b, apply ‐3.5 dB de‐empha‐ sis instead. 

Curiously, the DC common‐mode voltage does not have to be maintained within spec limits during this substate. 

If this substate is entered after a successful speed negotiation (successful_speed_negotiation = 1b), Electrical Idle can be inferred as shown in Table 14‐10 on page 596. The spec points out that this covers the case in which both Link partners have recognized incoming TS1s and TS2s, so their absence can be interpreted as an entry to Electrical Idle. 

If this substate is entered after an unsuccessful speed negotiation (successful_speed_negotiation = 0b), Electrical Idle can be inferred if an Electrical Idle exit has not been detected at least once on any configured Lane in the specified time. This is intended to cover the case when at least one side of the Link is not able to recognize TS Ordered Sets, and so the lack of an exit from Electrical Idle over a longer interval can be treated as an entry to Electrical Idle. 

_Table 14‐10: Conditions for Inferring Electrical Idle_ 

|**State**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|
|---|---|---|---|
|L0|Absence of Flow<br>Control Update<br>DLLP or SOS in a<br>128s window|Absence of Flow Con‐<br>trol Update DLLP or<br>SOS in a 128s win‐<br>dow|Absence of Flow<br>Control Update<br>DLLP or SOS in a<br>128s window|
|Recovery.RcvrCfg|Absence of a TS1 or<br>TS2 in a 1280 UI<br>interval|Absence of a TS1 or<br>TS2 in a 1280 UI inter‐<br>val|Absence of a TS1 or<br>TS2 in a 4ms win‐<br>dow|
|Recovery.Speed when<br>successful_speed_neg<br>otiation = 1b|Absence of a TS1 or<br>TS2 in a 1280 UI<br>interval|Absence of a TS1 or<br>TS2 in a 1280 UI inter‐<br>val|Absence of a TS1 or<br>TS2 in a 4680 inter‐<br>val|


**Chapter 14: Link Initialization & Training** 

_Table 14‐10: Conditions for Inferring Electrical Idle (Continued)_ 

|**State**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|
|---|---|---|---|
|Recovery.Speed when<br>successful_speed_neg<br>otiation = 0b|Absence of an Elec‐<br>trical Idle exit in a<br>2000 UI interval|Absence of an Electri‐<br>cal Idle exit in a 16000<br>UI interval|Absence of an Elec‐<br>trical Idle exit in a<br>16000 UI interval|
|Loopback.Active (as a<br>slave)|Absence of an Elec‐<br>trical Idle exit in a<br>128s window|N/A|N/A|


The directed_speed_change variable will be cleared to 0b and the new data rate must be visible in the Current Link Speed field of the Link Status regis‐ ter, shown in Figure 14‐39. 

If the speed was changed because of a Link bandwidth change: 

- If successful_speed_negotiation is set to 1b and the Autonomous Change bit in the 8 consecutive TS2s is set to 1b, or the speed change was initiated by the Downstream Port for autonomous reasons (not a reliability problem and not caused by software setting the Link Retrain bit), then the Link Autonomous Bandwidth Status bit in the Link Status register is set to 1b. 

- Otherwise, the Link Bandwidth Management Status bit is set to 1b. 

_Figure 14‐39: Link Status Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## _Exit to “Detailed Recovery Substates”_ 

Once the timeout has expired, the next state will be Recovery.RcvrLock 

If this substate was entered from Recovery.RcvrCfg and the speed change was successful, the new data rate is changed on all the configured Lanes to the highest commonly‐supported rate and the changed_speed_recovery variable is set to 1b. 

If this substate was entered for a second time since entering Recovery from L0 or L1 (indicated by changed_speed_recovery = 1b), the new data rate will be the rate that was in use when the LTSSM entered Recovery, and the changed_speed_recovery variable is cleared to 0b. 

Otherwise, the new data rate will revert to 2.5 GT/s and the changed_speed_recovery variable remains cleared to 0b. The spec notes that this represents the case when the rate in L0 was greater than 2.5 GT/s but one Link partner couldn’t operate at that rate and timed out in Recov‐ ery.RcvrLock the first time through. 

## _Exit to “Detect State”_ 

If none of the conditions for exiting to Recovery.RcvrLock are met, the next state will be Detect, although the spec points out that this shouldn’t be pos‐ sible under normal conditions. It would mean that the Link neighbors can no longer communicate at all. 

## **Recovery.RcvrCfg** 

This state can only be entered from Recovery.RcvrLock after receiving at least 8 TS1 or TS2 ordered‐sets with the same Link and Lane numbers that had been negotiated previously. This means that bit and symbol or block lock have been established and now the Port must determine if there are any other items that need addressed in the Recovery state. If the purpose of entering Recovery was simply to re‐establish bit and symbol lock after leaving a link power manage‐ ment state, then it is likely that TS2s will be exchanged here and progress on to Recovery.Idle. If, however, there was another reason for entering the Recovery state (e.g. speed change or link width change), then that will be determined in this substate and the appropriate state transition will occur. 

During this substate, the Transmitter sends TS2s on all configured Lanes with the same Link and Lane Numbers configured earlier. If the directed_speed_change variable is set to 1b, then the speed_change bit in the TS2s must also be set. The N_FTS value in the TS2s should reflect the number needed at the current rate. The start_equalization_w_preset variable is cleared to 0b when entering this substate. 

**Chapter 14: Link Initialization & Training** 

If the speed has been changed a different N_FTS number may now be seen in the TS2s. That value must be used for exiting future L0s low‐power Link states. For 8b/10b encoding, Lane‐to‐Lane de‐skew must be completed before leaving this substate. Devices must note the advertised rate identifier in incoming TS2s and use this to override any previously‐recorded values. When using 128b/130b encoding, devices must make a note of the value of the Request Equalization bit for future reference. 

Notes about this substate: The variable successful_speed_negotiation is set to 1b. The data rates advertised in the TS2s with the speed_change bit set are noted at this point for future reference, as is the Autonomous Change bit for possible logging in the Link Status register during Recovery.Speed. The rate that will be selected in Recovery.Speed will be the highest commonly‐supported rate. Inter‐ estingly, the change to Recovery.Speed will take place for this case even if the Link is already operating at the highest supported rate, although in that case the rate won’t actually change. 

If the speed is going to change to 8.0 GT/s, a Downstream Port will need to send EQ TS2s (bit 7 of Symbol 6 is set to 1b to indicate an EQ training sequence). This case would be recognized if 8.0 GT/s is mutually supported and 8 consecutive TS1s or TS2s have been seen on any configured Lane with the speed_change bit set, or if the equalization_done_8GT_data_rate variable is 0b, or if directed. An Upstream Port can set the Request Equalization bit if the current data rate is 8.0 GT/s and there was a problem with the equalization process. Either Port can request equalization be done again by setting both the Request Equalization and Quiesce Guarantee bits to 1b. 

Upstream Ports set their select_deemphasis variable based on the Selectable De‐ emphasis bit in the received TS2s. And, if the TS2s were EQ TS2s, they set the start_equalization_w_preset variable to 1b and update their Lane Equalization register with the new information (i.e.: update the Upstream Port Transmitter Preset and Receiver Preset Hint fields in the register). Any configured Lanes that don’t receive EQ TS2s will choose their preset values for 8.0 GT/s operation in a design‐specific manner. Downstream Ports must set their start_equalization_w_preset variable to 1b if the equalization_done_8GT_data_rate variable is cleared to 0b or if directed. 

Finally, if 128b/130b encoding is in use, devices must make a note of the Request Equalization bit. If set, both it and the Quiesce Guarantee bit must be stored for future reference. 

## _Exit to “Recovery.Idle”_ 

The next state will be Recovery.Idle if two conditions are true:

</td>
<td style="background-color:#e8e8e8">

_退出到"Recovery.Speed"_

否则,经过 24ms 超时(容差为 -0 或 +2ms)后,下一个状态将是 Recovery.Speed,successful_speed_negotiation 标志被清零至 0b,而 Equalization Complete 状态位置为 1b。

**Phase 3 上游端口。** 在此阶段,上游端口发送 EC = 11b 的 TS1,并响应来自下游端口的请求 Tx 值。

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

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


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

**Chapter 14: Link Initialization & Training** 

如果速率已更改,可能会在 TS2 中看到不同的 N_FTS 数字。该值必须用于退出未来的 L0s 低功耗链路状态。对于 8b/10b 编码,必须在离开此子状态之前完成 Lane-to-Lane 去偏移。设备必须注意传入 TS2 中通告的速率标识符,并使用它来覆盖任何先前记录的值。使用 128b/130b 编码时,设备必须记录 Request Equalization 位的值以供将来参考。

关于此子状态的说明:变量 successful_speed_negotiation 被设置为 1b。在此时记录在 TS2 中以 speed_change 位设置的 TS2 中通告的数据速率以供将来参考,以及 Autonomous Change 位以供在 Recovery.Speed 期间可能记录到 Link Status 寄存器中。将在 Recovery.Speed 中选择的速率将是最高共同支持的速率。有趣的是,即使 Link 已经在最高支持的速率下运行,这种情况下也会发生到 Recovery.Speed 的转换,虽然在这种情况下速率实际上不会更改。

如果速率将要更改为 8.0 GT/s,则下游端口将需要发送 EQ TS2(Symbol 6 的位 7 设置为 1b 以指示 EQ 训练序列)。如果共同支持 8.0 GT/s 并且在任何已配置的 Lane 上看到 8 个连续的 speed_change 位设置的 TS1 或 TS2,或者如果 equalization_done_8GT_data_rate 变量为 0b,或者如果已指示,则会识别这种情况。如果当前数据速率为 8.0 GT/s 且均衡过程出现问题,上游端口可以设置 Request Equalization 位。任何一端都可以通过将 Request Equalization 和 Quiesce Guarantee 位都设置为 1b 来请求重新进行均衡。

上游端口根据接收到的 TS2 中的 Selectable De-emphasis 位设置其 select_deemphasis 变量。并且,如果 TS2 是 EQ TS2,则将 start_equalization_w_preset 变量设置为 1b,并使用新信息更新其 Lane Equalization 寄存器(即:更新寄存器中的上游端口发送器预设和接收器预设提示字段)。任何未收到 EQ TS2 的已配置 Lane 将以设计特定的方式选择其 8.0 GT/s 操作的预设值。如果 equalization_done_8GT_data_rate 变量被清零至 0b,或如果已指示,则下游端口必须将 start_equalization_w_preset 变量设置为 1b。

最后,如果使用 128b/130b 编码,设备必须记录 Request Equalization 位的值。如果已设置,则必须将其和 Quiesce Guarantee 位一起存储以供将来参考。

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

## **PCI Express Technology** 

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

**Chapter 14: Link Initialization & Training** 

## _退出到"Detect 状态"_

否则,经过 2ms 超时后,下一个状态将是 Detect,除非 idle_to_rlock_transitioned 变量小于 FFh,在这种情况下,下一个状态将是"详细恢复子状态"。对于到 Recovery.RcvrLock 的转换,如果数据速率为 8.0 GT/s,则 idle_to_rlock_transitioned 变量加 1b;而对于 2.5 或 5.0 GT/s,它将被设置为 FFh。

## **L0s 状态** 

这是具有从 L0 返回的最短退出延迟的低功耗链路状态。设备在硬件控制下自动管理此状态的进入和退出,无需任何软件参与。链路的每个方向可以独立于彼此进入和退出 L0s 状态。

## **L0s 发送器状态机** 

L0s 状态对发送器和接收器有不同的子状态。将首先描述发送器子状态。如第 603 页的 Figure 14-40 所示,与 L0s 状态关联的发送器状态机是一个简单的状态机。

_Figure 14-40: L0s Tx 状态机_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


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

**Chapter 14: Link Initialization & Training** 

## _退出到"L0 状态"_

一旦所有 FTS 都已发送,发送器将转换到 L0 状态,并且:

- a) 对于 8b/10b 编码,在所有已配置的 Lane 上发送一个 SOS,尽管在 FTS 之前或期间不发送任何 SOS。

- b) 对于 128b/130b 编码,发送一个 EIEOS,然后是 SDS 和数据流。

## **L0s 接收器状态机** 

Figure 14-41(第 605 页)显示了接收器 L0s 状态机。如果 Link Capability 寄存器中的 ASPM Support 字段显示支持 L0s,则要求接收器实现 L0s 支持;即使未指示支持,允许实现它。

_Figure 14-41: L0s 接收器状态机_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Rx_L0s.Entry。** 

当接收器接收到 EIOS 时进入,前提是它支持 L0s 并且尚未被指示为 L1 或 L2。

_退出到"Rx_L0s.Idle"_

下一个状态将在 TTX-IDLE-MIN 超时(20ns)后是 Rx_L0s.Idle。

## **Rx_L0s.Idle。** 

接收器现在处于 Electrical Idle 模式,只是等待看到退出 Electrical Idle。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0685_img1_tight.png" alt="Figure from page 685" width="700">

<a id="sec-14-4"></a>
## 14.4 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Eight consecutive TS2s are received on any configured Lane with Link and Lane numbers and rate identifiers that match those being sent and either: 

 - a) The speed_change bit in the TS2s is cleared to 0b, or 

 - b) No rate higher than 2.5 GT/s is commonly supported. 

- Sixteen TS2 have been sent after receiving one and they haven’t been interrupted by any intervening EIEOS. The changed_speed_recovery and directed_speed_change variables are both cleared to 0b on entry to this substate. 

## _Exit to “Recovery.Speed”_ 

The LTSSM will go to Recovery.Speed if ALL three conditions listed below are true: 

- Eight consecutive TS2s are received on any configured Lane with the speed_change bit set, identical rate identifiers, identical values in Symbol 6, and: 

 - a) The TS2s were standard 8b/10b TS2s, or 

 - b) The TS2s were EQ TS2s, or 

 - c) 1ms has expired since receiving eight EQ TS2s on any configured Lane. 

- Both Link partners support rates higher than 2.5 GT/s, or the rate is already higher than 2.5 GT/s. 

- For 8b/10b encoding, at least 32 TS2s were sent with the speed_change bit set to 1b without any intervening EIEOS after receiving one TS2 with the speed_change bit set to 1b in the same con‐ figured Lane. For 128b/130b encoding, at least 128 TS2s are sent with the speed_change bit set to 1b after receiving one TS2 with the speed_change bit set to 1b in the same configured Lane. 

A transition to Recovery.Speed can also occur if the rate has changed to a mutually negotiated rate since entering Recovery from L0 or L1 (changed_speed_recovery = 1b) and any configured Lanes have either seen EIOS or detected/inferred Electrical Idle and haven’t seen TS2s since enter‐ ing this substate. This means a higher rate was attempted but the Link part‐ ner indicates that it isn’t working for some reason. The new rate will return to whatever it was when Recovery was entered from L0 or L1. 

The final case that can cause a transition to Recovery.Speed is if the rate has _not_ changed to a mutually negotiated rate since entering Recovery from L0 

**Chapter 14: Link Initialization & Training** 

or L1 (changed_speed_recovery = 0b), and the current rate is already higher than 2.5 GT/s, and any configured Lanes have either seen EIOS or detected/ inferred Electrical Idle and haven’t seen TS2s since entering this substate. In this case, the understanding is that the current rate isn’t working and the solution is to drop back down, so the new rate will become 2.5 GT/s. 

## _Exit to “Configuration State”_ 

The next state will be Configuration if 8 consecutive TS1s are received on any configured Lane with Link or Lane numbers that don’t match those being sent and either the speed_change bit is cleared to 0b, or no rate higher than 2.5 GT/s is commonly supported. 

The variables changed_speed_recovery and directed_speed_change are cleared to 0b when the LTSSM transitions to Configuration. If the N_FTS value has changed since last time, the new value must be used for L0s going forward. 

## _Exit to “Detect State”_ 

After 48ms without resolving to one of the previously‐defined state transi‐ tions, the next state will be Detect if the data rate is 2.5 GT/s or 5.0 GT/s. 

If the rate is 8.0 GT/s there is another possibility because the number of attempts may not have been exceeded yet. That is indicated by the idle_to_rlock_transitioned variable, and if it’s less than FFh when the rate is 8.0 GT/s, the new state will be “Recovery.Idle”. If that transition is made, the variables changed_speed_recovery and directed_speed_change will be cleared to 0b. However, once idle_to_rlock_transitioned reaches FFh, and the 48ms timeout is seen, the next state will be Detect. 

## **Recovery.Idle** 

As the name implies, Transmitters will usually send Idles in this substate as a preparation for changing to the fully operational L0 state. For 8b/10b mode, Idle data is normally sent on all the Lanes, while for 128b/130b an SDS is sent to start a Data Stream and then Idle data Symbols are sent on all the Lanes. 

## _Exit to “L0 State”_ 

The next state is L0 if either of the following cases is true. In either case, if the Retrain Link bit has been written to 1b since the last transition to L0 from Recovery or Configuration, the Downstream Port will set the Link Bandwidth Management Status bit to 1b (see Figure 14‐39 on page 597). 

- 8b/10b encoding is in use and 8 consecutive Symbol Times of Idle data have been received and 16 Idle data Symbols have been sent since the first one was received. 

## **PCI Express Technology** 

- 128b/130b encoding in use, 8 consecutive Symbol Times of Idle data have been received and 16 Idle data Symbols have been sent since the first one was received, and this state wasn’t entered from Recov‐ ery.RcvrCfg. Note that Idle data Symbols must be contained in Data Blocks, Lane‐to‐Lane De‐skew must be completed before Data Stream processing starts, and the idle_to_rlock_transitioned variable is cleared to 00h on transition to L0. 

## _Exit to “Configuration State”_ 

The next state is Configuration if either: 

- A Port is instructed by a higher layer to optionally reconfigure the Link, such as to change the Link width. 

- Any configured Lane sees two consecutive incoming TS1s with Lane numbers set to PAD (a Port that transitions to Configuration to change the Link will send PAD Lane numbers on all Lanes). The spec recommends that the LTSSM use this transition when changing the Link width to reduce the time it will take. 

## _Exit to “Disable State”_ 

The next state is Disabled if either: 

- A Downstream or optional crosslink Port is instructed by a higher layer to set the Disable Link bit in its TS1s or TS2s. 

- Any configured Lane of an Upstream or optional crosslink Port sees the Disable Link bit set in two consecutive incoming TS1s. 

## _Exit to “Hot Reset State”_ 

The next state is Hot Reset if either: 

- A Downstream or optional crosslink Port is instructed by a higher layer to set the Hot Reset bit in its TS1s or TS2s. 

- Any configured Lane of an Upstream or optional crosslink Port sees the Hot Reset bit set in two consecutive incoming TS1s. 

## _Exit to “Loopback State”_ 

The next state is Loopback if either: 

- A Transmitter is known to be Loopback Master capable (design spe‐ cific; the spec does not provide a means to verify this) and instructed by a higher layer to set the Loopback bit in its TS1s or TS2s. 

- Any configured Lane of an Upstream or optional crosslink Port sees the Loopback bit set in two consecutive incoming TS1s. The receiving device then becomes the Loopback slave. 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Detect State”_ 

Otherwise, after a 2ms timeout, the next state will be Detect unless the idle_to_rlock_transitioned variable is less than FFh, in which case the next state will be “Detailed Recovery Substates”. For the transition to Recov‐ ery.RcvrLock, if the data rate is 8.0 GT/s the idle_to_rlock_transitioned vari‐ able is incremented by 1b, while for 2.5 or 5.0 GT/s it will be set to FFh. 

## **L0s State** 

This is the low power Link state that has the shortest exit latency back to L0. Devices manage entry and exit from this state automatically under hardware control without any software involvement. Each direction of a Link, can enter and exit the L0s state independent of each other. 

## **L0s Transmitter State Machine** 

The L0s state has different substates for the Transmitter and the Receiver. The Transmitter substates will be described first. As shown in Figure 14‐40 on page 603 the transmitter state machine associated with L0s state is a simple one. 

_Figure 14‐40: L0s Tx State Machine_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Tx_L0s.Entry.** 

A Transmitter enters L0s when directed by an upper layer. The spec gives no decision criteria for this, but intuitively it would occur based on an inac‐ tivity timeout: no TLPs or DLLPs being sent for a given time. To enter L0s, the Transmitter sends one EIOS (two EIOSs for the 5.0 GT/s rate) and enters Electrical Idle. The Transmitter is not turned off, however, and must main‐ tain the DC common‐mode voltage within the spec range. 

## _Exit to “Tx_L0s.Idle”_ 

The next state will be Tx_L0s.Idle after the TTX‐IDLE‐MIN timeout (20ns). This time is intended to ensure that the Transmitter has established the Electrical Idle condition. 

## **Tx_L0s.Idle.** 

In this substate, the transmitter continues the Electrical Idle state until directed to leave. Because this direction of the Link is in Electrical Idle, there will be a power savings benefit, which is the entire purpose of the L0s state. 

_Exit to “Tx_L0s.FTS”_ 

The next state will be Tx_L0s.FTS when directed, such as when the Port needs to resume packet transmission. The LTSSM will be instructed in a design‐specific manner to exit this state. 

## **Tx_L0s.FTS.** 

In this substate, the Transmitter will start sending FTS ordered sets to retrain the Receiver of the Link Partner. The number of FTSs sent is the N_FTS value advertised by the Link Partner in its TS Ordered Sets during the last training sequence that led to L0. The spec notes that if a Receiver times out while trying to do this, it may choose to increase the N_FTS value it advertises during the Recovery state. 

If the Extended Synch bit is set (see Figure 14‐71 on page 644), the transmit‐ ter must sends 4096 FTSs instead of the N_FTS number. This extends the time available to synchronize external test and analysis logic, which may not be able to recover Bit Lock as quickly as the embedded logic can. 

For all data rates, no SOSs can be sent prior to sending any FTSs. However, for the 5.0 GT/s rate, 4 to 8 EIE Symbols must be sent prior to sending the FTSs. For 128b/130b, an EIEOS must be sent prior to the FTSs. 

**Chapter 14: Link Initialization & Training** 

## _Exit to “L0 State”_ 

The Transmitter will transition to the L0 state once all the FTSs have been sent and: 

- a) For 8b/10b encoding, one SOS is sent on all configured Lanes, although none are sent before or during the FTSs. 

- b) For 128b/130b encoding, one EIEOS is sent followed by an SDS and a Data Stream. 

## **L0s Receiver State Machine** 

Figure 14‐41 on page 605 shows the Receiver L0s state machine. A Receiver is required to implement L0s support if the ASPM Support field in the Link Capa‐ bility register shows it to be supported, and is allowed to implement it even if that support is not indicated. 

_Figure 14‐41: L0s Receiver State Machine_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Rx_L0s.Entry.** 

Entered when a Receiver that receives an EIOS, provided it supports L0s and hasn’t been directed to L1 or L2. 

_Exit to “Rx_L0s.Idle”_ 

The next state will be Rx_L0s.Idle after the TTX‐IDLE‐MIN timeout (20ns). 

## **Rx_L0s.Idle.** 

The Receiver is now in Electrical Idle mode and is just waiting to see an exit from Electrical Idle.

</td>
<td style="background-color:#e8e8e8">

关于 Electrical Idle 的旁注,规范的早期版本预计 Electrical Idle 将基于测量电压阈值的 squelch 检测电路。后来,随着速度增加,检测如此小的电压差异变得越来越困难。因此,较新的规范版本允许通过观察链路行为来推断 Electrical Idle,而不是实际测量电压。但是,如果未使用电压电平来检测进入 Electrical Idle,那么它也不能用于检测退出 Electrical Idle。为了处理该问题,引入了一种称为 EIEOS(Electrical Idle Exit Ordered Set)的新有序集。EIEOS 由全零和全 1 的交替字节组成,在 Lane 上产生低频时钟的效果。一旦接收器进入 Electrical Idle,它可以监视信号上的此模式以通知它链路正在退出 Electrical Idle。

_退出到"Rx_L0s.FTS"_

在接收器检测到退出 Electrical Idle 之后,下一个状态将是 Rx_L0s.FTS。

## **Rx_L0s.FTS。** 

在此子状态中,接收器已注意到退出 Electrical Idle,现在正尝试在传入的位流(实际上是 FTS 有序集)上重新建立位和符号或块锁。

_退出到"L0 状态"_

如果在 8b/10b 编码中所有已配置的 Lane 上接收到 SOS,或者在 128b/130b 编码中接收到 SDS,则下一个状态将是 L0。接收器必须能够在此之后立即接受有效数据,并且必须在离开此状态之前完成 Lane-to-Lane 去偏移。

**Chapter 14: Link Initialization & Training** 

## _退出到"Recovery 状态"_

否则,在 N_FTS 超时后,下一个状态将是 Recovery。如果是这样,发送器也必须进入 Recovery,尽管允许完成正在进行的任何 TLP 或 DLLP。如果发生超时,规范建议增加 N_FTS 值以降低再次发生的可能性。N_FTS 超时定义如下:

对于 8b/10b,最小超时为 40 * [N_FTS + 3] * UI,而最大允许为该时间的两倍。由于每个符号需要 10 位(UI 表示一个位时间),因此这等于 (4*N_FTS + 12) 个符号。额外的 12 个符号解释为:最大大小 SOS 的 6 个 + 4 个用于可能的额外 FTS + 2 个用于符号裕度。总之,最小时间是发送所请求的 FTS 数量加上 12 个符号所需的时间,而最大时间是该时间的两倍。

如果设置了扩展同步位,则最小时间 = 2048 FTS,最大时间 = 4096 FTS。接收器将使用的实际超时值还必须考虑 2.5 GT/s 以外速度的 4 到 8 个 EIE 符号。

对于 128b/130b,超时值被给定为最小 130 * [N_FTS + 5 + 12 + Floor(N_FTS/32)] * UI,最大为该时间的两倍。值 130 * UI 意味着 130 个位时间,代表一个块,因此如果我们删除这两个值,我们可以说我们正在查看 [N_FTS + 5 + 12 + Floor(N_FTS/32)] 个块。值 [5 + Floor(N_FTS/32)] 表示在此期间需要发送的 EIEOS 数。每 32 个 FTS 之后将发送一个 EIEOS,因此 Floor(N_FTS/32) 给出该数字。另一个 5 是由第一个 EIEOS、最后一个 EIEOS、SDS、周期性 EIEOS 和当 N_FTS 能被 32 整除时发送两个 EIEOS 后跟一个 SDS 的情况下发送的额外 EIEOS 解释的。最后,值 12 表示如果设置了扩展同步位将发送的 SOS 数量。当设置了该位时,超时将使用 N_FTS = 4096。

## **L1 状态** 

此链路电源状态与 L0s 状态相比,权衡了更长的退出延迟以获得更积极的电源管理。L1 是 ASPM 的一个选项,像 L0s 一样,意味着设备可以在硬件控制下自动进入和退出此状态,无需任何软件参与。但是,与 L0s 不同,软件也能够指示上游端口发起更改为 L1,它通过将设备电源状态写入较低级别(D1、D2 或 D3)来执行此操作。L1 状态与 L0s 的不同之处还在于它影响链路的两个方向。

## **PCI Express Technology** 

_Figure 14-42: L1 状态机_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


由于进入 Electrical Idle 可能表示链路伙伴希望进入 L0s、L1 或 L2,因此通过让两个伙伴事先同意何时将进入 L1 来处理应将哪个作为下一个状态。握手通知他们伙伴已准备好,因此可以安全地继续。有关此工作原理的更多详细信息,请参阅第 733 页的"Link Power Management 简介"部分。第 608 页的 Figure 14-42 显示了 L1 状态机,将在以下部分中描述。

## **L1.Entry** 

要使上游端口进入此状态,它必须向其链路伙伴发送进入 L1 的请求,并收到可以进入 L1 状态的确认。请求进入 L1 的原因可能是由于 ASPM 或软件参与。一旦接收到 L1 请求确认,上游端口将进入 L1.Entry 子状态。

要使下游端口进入此状态,它必须从上游端口接收 L1 进入请求,并向该请求发送肯定响应。然后下游端口等待接收 Electrical Idle Ordered Set (EIOS) 并让其接收 Lane 下降至 Electrical Idle。此时,下游端口进入 L1.Entry 子状态。

**Chapter 14: Link Initialization & Training** 

## _在 L1.Entry 期间_

所有已配置的发送器发送一个 EIOS 并进入 Electrical Idle,同时保持适当的 DC 共模电压。

## _退出到"L1.Idle"_

下一个状态将在 TTX-IDLE-MIN 超时(20ns)后是 L1.Idle。此时间旨在确保发送器已建立 Electrical Idle 条件。

## **L1.Idle** 

在此子状态期间,发送器保持处于 Electrical Idle 状态。

对于 2.5 GT/s 以外的速率,LTSSM 必须在此子状态中保持至少 40ns。在规范中,此延迟被称为"用于补偿逻辑电平中的延迟,以防链路进入 L1 后立即退出时使能 Electrical Idle 检测电路"。

## _退出到"Recovery 状态"_

当发送器被指示更改或任何接收器检测到退出 Electrical Idle 时,下一个状态将是 Recovery。离开 L1 的原因包括需要传递 DLLP 或 TLP,或希望更改链路宽度或速度。如果需要速度更改,则允许端口将 directed_speed_change 变量设置为 1b,并且必须将 changed_speed_recovery 变量清零至 0b。可选地,端口可以退出 L1,然后通过将 directed_speed_change 设置为 1b 并从 L0 进入 Recovery 来稍后启动速度更改。

## **L2 状态** 

这是比 L1 更深的电源状态,具有更长的退出延迟。当其设备置于 D3Cold 电源状态并且已完成的相应链路握手后,电源管理软件指示上游端口发起进入 L2(链路的两个方向都进入 L2)。

一旦系统了解到一切就绪,主电源将被关闭。断电后,链路电源状态将变为 L2 或 L3,具体取决于是否可获得称为 VAUX(辅助电压)的辅助电源。如果存在 VAUX,则链路进入 L2;如果不存在,则进入 L3。

L2 的动机是使用 VAUX 提供的小功率来通知系统何时发生需要恢复链路电源的事件。

## **PCI Express Technology** 

有两种标准方式设备可以通知系统此类事件。一种是称为 WAKE# 引脚的边带信号,另一种是称为"Beacon"的带内信号。L2 状态对于 WAKE# 是不需要的,但如果要使用可选的 Beacon,则是必需的。规范明确指出,以 5.0 或 8.0 GT/s 运行的设备不需要支持 Beacon,因此这似乎是旧版支持,仅对以 2.5 GT/s 运行的设备有意义。有关链路唤醒选项的更多详细信息,请参阅第 772 页的"Waking Non-Communicating Links"。

如果支持,Beacon 是低频(30 KHz - 500 MHz)带内信号,支持唤醒功能的上游端口必须能够在至少 Lane 0 上发送它,下游端口必须能够接收它。像交换机这样的中间设备,如果在下游端口上接收到 Beacon,必须将其转发到其上游端口。Beacon 的最终目的地是根复合体 (Root Complex),因为这是系统电源控制逻辑预期所在的位置。

进入 Electrical Idle 的发送器可能表示希望进入任何低功耗链路状态(L0s、L1 或 L2),因此需要一种区分它们的方法。对于 L2,这通过让链路伙伴事先同意将通过使用握手序列来进入 L2 来处理,以确保它们都已准备好。有关此工作原理的更多详细信息,请参阅第 733 页的"Link Power Management 简介"部分。第 611 页的 Figure 14-43 显示了 L2 进入和退出状态机,将在以下文本中描述。

**Chapter 14: Link Initialization & Training** 

_Figure 14-43: L2 状态机_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **L2.Idle** 

要进入此子状态,链路两端的所有必要握手过程必须已经发生,并且端口已发送和接收到所需的 EIOS。

所有已配置的发送器必须保持处于 Electrical Idle 状态至少 TTX-IDLE-MIN 超时(20ns)。但是,由于主电源现在将被关闭,因此它们不需要将 DC 共模电压保持在规范范围内。接收器在 20ns 超时到期之前不会开始寻找 Electrical 退出条件。所有接收器终端必须保持处于低阻抗条件下的使能状态。

## _退出到"L2.TransmitWake"_

如果上游端口被指示发送 Beacon(Beacon 始终且仅指向上游到根复合体),则下一个状态将是 L2.TransmitWake。

如果交换机的下游端口检测到 Beacon,则它必须指示交换机的上游端口退出到 L2.TransmitWake 并开始发送 Beacon。

## _退出到"Detect 状态"_

一旦主电源恢复,下一个状态将是 Detect。

如果此端口具有主电源,但它在任何"预定的"Lane 上检测到退出 Electrical Idle,这意味着那些可以协商为 Lane 0 的 Lane(多 Lane 链路必须具有至少两个预定的 Lane),则下一个状态将是 detect。当这种情况发生在交换机上游端口时,交换机还必须将其下游端口转换为 Detect。

## **L2.TransmitWake**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0685_img2_tight.png" alt="Figure from page 685" width="700">

<a id="sec-14-5"></a>
## 14.5 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

As an aside regarding Electrical Idle, the early versions of the spec expected that Electrical Idle would be based on a squelch‐detect circuit measuring a voltage threshold. Later, as speeds increased, detecting such small voltage differences became increasingly difficult. Consequently, more recent spec versions allow Electrical Idle to be inferred by observing Link behavior, rather than actually measuring the voltage. However, if the voltage level isn’t used to detect entry into Electrical Idle, then it also can’t be used to detect an exit from it. To handle that problem, a new Ordered Set was intro‐ duced called the EIEOS (Electrical Idle Exit Ordered Set). The EIEOS con‐ sists of alternating bytes of all zeros and all ones and creates the effect of a low‐frequency clock on the Lanes. Once a Receiver has entered Electrical Idle it can watch for this pattern on the signal to inform it that the Link is exiting from Electrical Idle. 

_Exit to “Rx_L0s.FTS”_ 

The next state will be Rx_L0s.FTS after the Receiver detects an exit from Electrical Idle. 

## **Rx_L0s.FTS.** 

In this substate, the Receiver has noticed an exit from Electrical Idle and is now trying to re‐establish Bit and Symbol or Block lock on the incoming bit stream (which are really FTS ordered sets). 

_Exit to “L0 State”_ 

The next state will be L0 if an SOS is received in 8b/10b encoding or an SDS in 128b/130b encoding on all configured Lanes. The Receiver must be able to accept valid data immediately after that, and Lane‐to‐Lane de‐skew must be completed before leaving this state. 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Recovery State”_ 

Otherwise the next state will be Recovery after the N_FTS timeout. If so, the Transmitter must also go to Recovery, although it’s allowed to finish any TLP or DLLP that was in progress. If the timeout occurs, the spec recommends that the N_FTS value be increased to reduce the likelihood of it happening again. The N_FTS timeout is defined as follows: 

For 8b/10b, the minimum timeout is given as 40 * [N_FTS + 3] * UI, while the maximum allowed is twice that time. Since 10 bits (UI repre‐ sents one bit time) are needed per Symbol, this works out to (4*N_FTS + 12) Symbols. The extra 12 Symbols are explained as 6 for a max‐sized SOS + 4 for the possible extra FTS + 2 more for Symbol margin. In sum‐ mary, then, the minimum time is the time it should take to send the requested number of FTSs plus 12 Symbols, while the maximum time is twice as much as that. 

If the extended synch bit is set, the min time = 2048 FTSs and the max time = 4096 FTSs. The actual timeout value a Receiver will use must also take into account the 4 to 8 EIE Symbols for speeds other than 2.5 GT/s. 

For 128b/130b, the timeout value is given as a minimum of 130 * [N_FTS + 5 + 12 + Floor (N_FTS/32)] * UI and a max of twice that time. The value 130 * UI means 130 bit times which represents one Block, so if we remove those two values we can say we’re looking at [N_FTS + 5 + 12 + Floor (N_FTS/32)] Blocks. The value [5 + Floor (N_FTS/32)] represents the EIEOSs that will need to be sent during this time. One EIEOS will be sent after every 32 FTSs, so Floor (N_FTS/32) gives that number. The other 5 are accounted for by the first EIEOS, the last EIEOS, the SDS, the periodic EIEOS and an additional EIEOS in case the Transmitter chooses to send two EIEOS followed by an SDS when N_FTS is divisi‐ ble by 32. Finally, the value of 12 represents the number of SOSs that will be sent if the extended synch bit is set. When that bit is set, the tim‐ eout will use N_FTS = 4096. 

## **L1 State** 

This Link power state trades a longer exit latency for more aggressive power management compared to the L0s state. L1 is an option for ASPM, like L0s, meaning devices can enter and exit this state automatically under hardware control without any software involvement. However, unlike L0s, software is also able to direct an Upstream Port to initiate a change to L1, and it does so by writing the device power state to a lower level (D1, D2, or D3). The L1 state is also different from L0s in that it affects both directions of the Link. 

## **PCI Express Technology** 

_Figure 14‐42: L1 State Machine_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


Since going to Electrical Idle can indicate a desire by the Link partner to enter L0s, L1 or L2, differentiating which should be the next state is handled by hav‐ ing both partners agree beforehand when they’re going to enter L1. A hand‐ shake informs them that the partner is ready and it’s therefore safe to proceed. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. Figure 14‐42 on page 608 shows the L1 state machine, which is described in the following sections. 

## **L1.Entry** 

In order for an Upstream Port to enter this state, it must send a request to enter L1 to its Link Partner and receive acknowledgement that it is OK to put the Link into L1. (The reason for requesting to go into L1 may be because of ASPM or because of software involvement.) Once the L1 request acknowledge is received, the Upstream Port enters the L1.Entry substate. 

In order for a Downstream Port to enter this state, it must receive an L1 enter request from the Upstream Port and send a positive response to that request. Then the Downstream Port waits to receive an Electrical Idle Ordered Set (EIOS) and have its receive lanes drop to Electrical Idle. It is at this point that the Downstream Port enters the L1.Entry substate. 

**Chapter 14: Link Initialization & Training** 

## _During L1.Entry_ 

All configured Transmitters send an EIOS and enter Electrical Idle while maintaining the proper DC common mode voltage. 

## _Exit to “L1.Idle”_ 

The next state will be L1.Idle after the TTX‐IDLE‐MIN timeout (20ns). This time is intended to ensure that the Transmitter has established the Electrical Idle condition. 

## **L1.Idle** 

During this substate, Transmitters remain in the Electrical Idle. 

For rates other than 2.5 GT/s the LTSSM must remain in this substate for at least 40ns. In the spec, this delay is said “to account for the delay in the logic levels to arm the Electrical Idle detection circuitry in case the Link enters L1 and immedi‐ ately exits”. 

## _Exit to “Recovery State”_ 

The next state will be Recovery when a Transmitter is directed to change it or when any Receiver detects an exit from Electrical Idle. Reasons for leav‐ ing L1 include the need to deliver a DLLP or TLP, or a desire to change the Link width or speed. If a speed change is desired, a Port is allowed to set the directed_speed_change variable to 1b and must clear the changed_speed_recovery variable to 0b. Optionally, the Port may exit L1 and then initiate the speed change later by setting directed_speed_change to 1b and entering Recovery from L0 instead. 

## **L2 State** 

This is a deeper power state with a longer exit latency than L1. Power Manage‐ ment software directs an Upstream Port to initiate entry into L2 (both directions of the Link go to L2) when its device is placed in the D3Cold power state and the appropriate Link handshakes have been completed. 

Main power will be shut off by the system once it learns that everything is ready. When power is removed, the Link power state will become either L2 or L3, depending on whether a secondary power source called VAUX (auxiliary voltage) is available. If VAUX is present, the Link enters L2; if not, it enters L3. 

The motivation for L2 is to use the small power available from VAUX to inform the system when an event has occurred for which the Link needs to have power 

## **PCI Express Technology** 

restored. There are two standard ways a device can inform the system of such an event. One is a side‐band signal called the WAKE# pin, and the other is an in‐ band signal called a “Beacon.” The L2 state isn’t needed for WAKE#, but is required if the optional Beacon will be used. The spec explicitly states that devices operating at 5.0 or 8.0 GT/s don’t need to support Beacon, so it would seem that this is legacy support and only interesting for devices operating at 2.5 GT/s. For more detail on Link wakeup options, refer to “Waking Non‐Commu‐ nicating Links” on page 772. 

If supported, the Beacon is a low‐frequency (30 KHz ‐ 500 MHz) in‐band signal that an Upstream Port supporting wakeup capability must be able to send on at least Lane 0 and a Downstream Port must be able to receive. Intermediate devices like Switches that receive a Beacon on a Downstream Port must forward it to their Upstream Port. The ultimate destination for the Beacon is the Root Complex, because that’s where the system power control logic is expected to reside. 

A Transmitter going to Electrical Idle could indicate a desire to enter any of the low‐power Link states (L0s, L1 or L2), so a means of differentiating them is needed. For L2, this is handled by having the Link partners agree beforehand that they’re going to enter L2 by using a handshake sequence to ensure that they’re both ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. Figure 14‐43 on page 611 shows the L2 entry and Exit state machine, which is described in the follow‐ ing text. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐43: L2 State Machine_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **L2.Idle** 

To enter this substate, all the necessary handshake process must have already taken place between both ports on the Link and the ports have sent and received the required EIOS. 

All configured Transmitters must remain in the Electrical Idle state for at least the TTX‐IDLE‐MIN timeout (20ns). However, since the main power will now be shut off, they aren’t required to maintain the DC common‐mode voltage within the spec range. Receivers won’t start looking for the Electrical exit condition until at least after the 20ns timeout expires. All Receiver terminations must remain enabled in the low impedance condition. 

## _Exit to “L2.TransmitWake”_ 

The next state will be L2.TransmitWake if the Upstream Port is instructed to send a Beacon (the Beacon is always and only directed upstream to the Root Complex). 

If the Downstream Port of a Switch detects a Beacon, it must direct the Upstream Port of the Switch to exit to L2.TransmitWake and begin sending a Beacon. 

## _Exit to “Detect State”_ 

Once main power is returned, the next state will be Detect. 

If this Port has main power, but it detects an exit from Electrical Idle on any “predetermined” Lanes, meaning those that could be negotiated to be Lane 0 (multi‐Lane Links must have at least two predetermined Lanes), the next state will be detect. When this happens to a Switch Upstream Port, the Switch must also transition its Downstream Ports to Detect. 

## **L2.TransmitWake**

</td>
<td style="background-color:#e8e8e8">

在此子状态期间,发送器将在至少 Lane 0 上发送 Beacon。请注意,此状态仅适用于上游端口,因为只有它们才能发送 Beacon。

## _退出到"Detect 状态"_

如果在任何上游端口的接收器上检测到退出 Electrical Idle,则下一个状态将是 Detect。当然,必须已经恢复了设备的电源,以便邻居退出 Electrical Idle。

## **Hot Reset 状态** 

由于以下任一原因,端口将进入 Hot Reset 状态:它是一个桥接器并且软件对其配置空间进行了编程以向下游传播 Hot Reset,如第 837 页的"Hot Reset(带内复位)"中所述;或者由于端口接收到两个连续的 Hot Reset 位为 1 的 TS1。

## _在 Hot Reset 期间_

端口持续传输 Hot Reset 位设置的 TS1,但不更改已配置的 Link 和 Lane 编号。

如果交换机的上游端口进入 Hot Reset 状态,则所有已配置的下游端口必须尽快转换为 Hot Reset。

## _退出到"Detect 状态"_

在发起 Hot Reset 的桥接器中,一旦软件清除启动 Hot Reset 的配置空间位,桥接端口将进入 Detect。但是,该端口必须保持在 Hot Reset 状态至少 2ms。

**Chapter 14: Link Initialization & Training** 

对于由于接收到两个连续的 Hot Reset 位为 1 的 TS1 而进入 Hot Reset 的端口,只要它继续接收此类 TS1,它就会保持此状态。一旦端口停止接收 Hot Reset 位为 1 的 TS1,它将转换到 Detect 状态。但是,该端口必须保持在 Hot Reset 状态至少 2ms。

## **Disable 状态** 

禁用的链路处于 Electrical Idle 状态,不必保持 DC 共模电压。软件通过设置设备的 Link Control 寄存器中的 Link Disable 位(参见第 644 页的 Figure 14-71)来启动此操作,然后设备发送 Disable Link 位为 1 的 TS1。

## _在 Disable 期间_

所有 Lane 发送 16 到 32 个 Disable Link 位为 1 的 TS1,发送一个 EIOS(对于 5.0 GT/s 情况为两个连续的 EIOS),然后转换到 Electrical Idle。DC 共模电压不需要在规范范围内。

如果已发送 EIOS(对于 5.0 GT/s 情况为两个连续的 EIOS)并且在任何已配置的 Lane 上也接收到 EIOS,则 LinkUp = 0b(False),并且 Lane 被认为是禁用的。

## _退出到"Detect 状态"_

对于上游端口,当在接收器处检测到 Electrical Idle,或在 2ms 超时内未接收到 EIOS 时,下一个状态将是 Detect。

对于下游端口,下一个状态也将是 Detect,但要等到软件将 Link Disable 位清零至 0b 之后。

## **Loopback 状态** 

Loopback 状态是在正常操作期间不使用的测试和调试功能。作为 Loopback 主站的设备可以通过发送 Loopback 位为 1 的 TS1 将链路伙伴置于 Loopback 从站模式。这可以在线完成,从而允许使用 Loopback 状态对链路执行 BIST(Built In Self Test)的可能性。

一旦处于此状态,Loopback 主站将有效符号发送给 Loopback 从站,然后 Loopback 从站回显它们。Loopback 从站继续执行

## **PCI Express Technology** 

时钟容差补偿,因此主站必须继续以正确的间隔插入 SOS。要执行时钟容差补偿,Loopback 从站可能必须向回显给 Loopback 主站的 SOS 添加或删除 SKP 符号。

当 Loopback 主站发送 EIOS 并且接收器检测到 Electrical Idle 时,Loopback 状态退出。Loopback 状态机如图 14-44(第 614 页)所示,并在以下文本中描述。

_Figure 14-44: Loopback 状态机_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Loopback.Entry** 

此子状态的典型行为是 Loopback Master 发送 Loopback 位置 1 的 TS1,直到它开始看到那些返回的 TS1。一旦 Loopback Master 看到返回的 Loopback 位为 1 的 TS1,它就知道其链路伙伴现在正在作为 Loopback Slave 运行,只是简单地重复它接收到的所有内容。

在此子状态中,链路不被视为处于活动状态(LinkUp = 0b)。此外,TS1 和 TS2 中使用的 Link 和 Lane 编号被接收器忽略。规范对 128b/130b 编码的 Lane 编号的使用进行了有趣的观察。事实证明,每个 Lane 对其加扰器使用不同的种子值(参见第 430 页的"加扰")。因此,如果 Lane 编号在进入 Loopback 模式之前尚未协商,则链路伙伴可能具有不同的 Lane 分配,因此将无法识别传入的符号。这可以通过在指

**Chapter 14: Link Initialization & Training** 

定 Master 进入 Loopback 状态之前等待 Lane 编号协商完成,或者通过指示 Master 在 Loopback.Entry 期间设置 Compliance Receive 位,或通过其他方法来避免。

## **Loopback Master:** 

在此子状态中,Loopback Master 将持续发送 Loopback 位置 1 的 TS1。Master 还可以在 TS1 中置位 Compliance Receive 位以帮助测试,当一个或两个端口在速率更改后难以获取位锁、符号锁或块对齐时。如果设置了该位,则在此状态期间不得清除它。

如果此子状态是从 Configuration.Linkwidth.Start 进入的,请检查正在使用的速度是否为两个链路伙伴共同支持的最高速率。如果不是:

- 更改为最高共同速度。发送 16 个 Loopback 位置 1 的 TS1,后跟一个 EIOS(如果当前速度为 5.0 GT/s,则为两个 EIOS),然后进入 Electrical Idle 1ms。在空闲期间,将速度更改为最高共同支持的速率。

- 如果最高共同速率为 5.0 GT/s,则从站的 Tx 去加重由 Master 通过将其 TS1 中的 Selectable De-emphasis 位设置为所需值来控制(1b = -3.5 dB,0b = -6 dB)。

- 对于 5.0 GT/s 及更高的数据速率,Master 的发送器可以选择其想要的任何去加重设置,无论它发送给从站的设置如何。

- 潜在问题:如果在链路已经训练到 L0 并且 LinkUp = 1b 之后进入 Loopback,则一个端口可能从 Recovery 进入 Loopback,而伙伴从 Configuration 进入。如果发生这种情况,后一个端口可能尝试更改速度,而从 Recovery 进入的端口则不会,从而导致结果未定义的情况。规范指出,测试设置必须避免此类冲突情况。

## _退出到"Loopback.Active"_

下一个状态将在 2ms 后是 Loopback.Active,前提是 TS1 中的 Compliance Receive 位已设置,或者在设计特定数量的 Lane 上接收到两个连续的 Loopback 位为 1 的 TS1 并且 TS1 中的 Compliance Receive 位未设置。

请注意,如果速度已更改,Master 必须确保已发送足够的 TS1,以便从站能够在进入 Loopback.Active 状态之前获取符号锁或块对齐。

## **PCI Express Technology** 

## _退出到"Loopback.Exit"_

如果不满足进入 Loopback.Active 的任一条件,则下一个状态将在小于 100ms 的设计特定超时后是 Loopback.Exit。

## **Loopback Slave:** 

此子状态通过接收两个连续的 Loopback 位为 1 的 TS1 来进入。

如果此子状态是从 Configuration.Linkwidth.Start 进入的,请检查正在使用的速度是否为两个链路伙伴共同支持的最高速度。如果不是:

- 更改为最高共同速度。发送一个 EIOS(如果当前速度为 5.0 GT/s,则为两个 EIOS),然后进入 Electrical Idle 2ms。在空闲期间,将速度更改为最高共同支持的速率。

- 如果最高共同速率为 5.0 GT/s,则根据接收到的 TS1 中的 Selectable De-emphasis 位设置发送器的去加重(1b = -3.5 dB,0b = -6 dB)。

- 如果最高共同速率为 8.0 GT/s,并且:

 - a) EQ TS1 指示从站进入此状态,则使用它们指定的 Tx Preset 设置。

 - b) 普通 TS1 指示从站进入此状态,则允许从站使用其默认发送器设置。

## _退出到"Loopback.Active"_

如果将指示从站进入此状态的传入 TS1 中的 Compliance Receive 位置 1,则下一个状态将是 Loopback.Active。从站不需要等待特定边界来发送环回数据,并且允许截断任何正在进行的有序集。

否则,从站发送 Link 和 Lane 编号设置为 PAD 的 TS1,并且下一个状态将是 Loopback.Active,前提是:

- 速率为 2.5 或 5.0 GT/s,并且所有 Lane 上获取了符号锁。

- 速率为 8.0 GT/s,并且在所有活动 Lane 上看到两个连续的 TS1。通过评估和应用 TS1 中给定的值来处理均衡,只要它们受支持并且 EC 值适合端口方向(下游端口为 10b,

**Chapter 14: Link Initialization & Training** 

上游端口为 11b)。可选地,端口可以接受此情况下的任一 EC 值。如果应用了设置,则它们必须在接收后 500ns 内生效,并且不得导致发送器在任何电气规范上违规超过 1ns。与 Recovery.Equalization 中的过程相比的一个显着差异是,从站正在发送的 TS1 中不回显新设置。– 对于 8b/10b,从站必须仅在符号边界上转换为环回数据,但允许截断任何正在进行的有序集。对于 128b/130b,未指定何时可以发送环回数据的边界,并且仍然允许截断任何正在进行的有序集。

## **Loopback.Active** 

在此子状态期间,Loopback Master 发送有效的编码数据,并且在准备退出 Loopback 之前不应发送 EIOS。Loopback Slave 在不修改的情况下回显接收到的信息(即使编码被确定为无效),可能的例外是反转极性,正如在 Polling 状态中确定的那样。从站还继续执行时钟容差补偿。这意味着必须根据需要添加或删除 SKP,但不要求所有 Lane 发送相同数量。

## _退出到"Loopback.Exit"_

对于 Loopback master,如果被指示,下一个状态将是 Loopback.Exit。

对于 Loopback slave,如果以下两个条件之一为真,则下一个状态将是 Loopback.Exit:

- 从站被指示退出,或在任何 Lane 上看到四个连续的 EIOS。

- 可选地,如果当前速度为 2.5 GT/s,并且接收到 EIOS 或在任何 Lane 上检测到或推断出 Electrical Idle。如果任何已配置的 Lane 在 128µs 内未检测到退出 Electrical Idle,则可以推断 Electrical Idle。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0687_img1_tight.png" alt="Figure from page 687" width="700">

<a id="sec-14-6"></a>
## 14.6 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

During this substate, the Transmitter will send the Beacon on at least Lane 0. Note that this state only applies to Upstream Ports because only they can send a Beacon. 

## _Exit to “Detect State”_ 

The next state will be Detect if an Electrical Idle exit is detected on any Receiver of an Upstream Port. Of course, power must have already been restored to the devices in order for the neighbor to exit from Electrical Idle. 

## **Hot Reset State** 

A Port enters the Hot Reset state either because it is a Bridge and software pro‐ grammed its configuration space to propagate a Hot Reset Downstream as explained in “Hot Reset (In‐band Reset)” on page 837, because a Port received two consecutive TS1s with the Hot Reset bit asserted. 

## _During Hot Reset_ 

A Port transmits TS1s with the Hot Reset bit set continuously but doesn’t change the configured Link and Lane Numbers. 

If the Upstream Port of Switch enters the Hot Reset state, all configured Downstream Ports must transition to Hot Reset as soon as possible. 

## _Exit to “Detect State”_ 

In the Bridge where Hot Reset was originated, once software clears the con‐ figuration space bit that initiated the Hot Reset, the Bridge Port enters Detect. However, the Port must remain in the Hot Reset state for a mini‐ mum of 2ms. 

**Chapter 14: Link Initialization & Training** 

For Ports where Hot Reset was entered because of receiving two consecu‐ tive TS1s with the Hot Reset bit asserted, it remains in this state as long as it continues to receive these type of TS1s. Once the Port stops receiving TS1s with the Hot Reset bit asserted, it will transition to the Detect state. How‐ ever, the Port must remain in the Hot Reset state for a minimum of 2ms. 

## **Disable State** 

A Disabled Link is Electrically Idle and does not have to maintain the DC com‐ mon mode voltage. Software initiates this by setting the Link Disable bit (see Figure 14‐71 on page 644) in the Link Control register of a device and the device then sends TS1s with the Link Disable bit asserted. 

## _During Disable_ 

All Lanes transmit 16 to 32 TS1s with the Disable Link bit asserted, send an EIOS (two consecutive EIOSs for the 5.0 GT/s case) and then transition to Electrical Idle. The DC common‐mode voltage does not need be within spec. 

If an EIOS (two consecutive EIOSs for the 5.0 GT/s case) was sent and an EIOS was also received on any configured Lane, then LinkUp = 0b (False) and the Lanes are considered to be disabled. 

## _Exit to “Detect State”_ 

For Upstream Ports, the next state will be Detect when Electrical Idle is detected at the Receiver or if no EIOS has been received within a 2ms time‐ out. 

For Downstream Ports, the next state will also be Detect, but not until the Link Disable bit has been cleared to 0b by software. 

## **Loopback State** 

The Loopback state is a test and debug feature that isn’t used during normal operation. A device acting as a Loopback master can put the Link partner into the Loopback slave mode by sending TS1s with the Loopback bit asserted. This can be done in‐circuit, allowing the possibility of using the Loopback state to perform a BIST (Built In Self Test) on the Link. 

Once in this state, the Loopback master sends valid Symbols to the Loopback slave, which then echoes them back. The Loopback slave continues to perform 

## **PCI Express Technology** 

clock tolerance compensation, so the master must continue to insert SOSs at the correct intervals. To perform clock tolerance compensation, the Loopback slave may have to add or delete SKP Symbols to the SOS it echoes to the Loopback master. 

The Loopback state is exited when the Loopback master transmits an EIOS and the receiver detects Electrical Idle. The Loopback state machine is shown in Fig‐ ure 14‐44 on page 614 and described in the following text. 

_Figure 14‐44: Loopback State Machine_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Loopback.Entry** 

The typical behavior for this substate is for the Loopback Master to send TS1s with the Loopback bit set until it starts seeing those TS1s being returned. Once the Loopback Master sees TS1s being returned with the Loopback bit asserted, it knows that it’s Link Partner is now behaving as the Loopback Slave and is simply repeating everything it receives. 

While in this substate, the Link is not considered to be active (LinkUp = 0b). Also, the Link and Lane numbers used in TS1s and TS2s are ignored by the Receiver. The spec makes an interesting observation regarding the use of Lane numbers with 128b/130b encoding. As it turns out, each Lane uses a different seed value for its scrambler (see “Scrambling” on page 430). Consequently, if the Lane numbers haven’t been negotiated before going into the Loopback mode, it’s possible that the Link partners could have different Lane assignments and would therefore be unable to recognize incoming Symbols. This can be avoided by waiting until the Lane numbers have been negotiated before direct‐ 

**Chapter 14: Link Initialization & Training** 

ing the master to go to the Loopback state, or by directing the master to set the Compliance Receive bit during Loopback.Entry, or by some other method. 

## **Loopback Master:** 

In this substate, the Loopback Master will continuously send TS1s with the Loopback bit set. The master may also assert the Compliance Receive bit in the TS1s to help testing when one or both Ports are having trouble obtaining bit lock, Symbol lock, or Block alignment after a rate change. If the bit is set it must not be cleared while in this state. 

If this substate was entered from Configuration.Linkwidth.Start, check to see whether the speed in use is the highest mutually supported rate for both Link partners. If not: 

- Change to the highest common speed. Send 16 TS1s with the Loop‐ back bit set followed by an EIOS (two EIOSs if the current speed is 5.0 GT/s), and then go to Electrical Idle for 1ms. During the idle time, change the speed to the highest commonly‐supported rate. 

- If the highest common rate is 5.0 GT/s, the slave’s Tx de‐emphasis is controlled by the master setting its Selectable De‐emphasis bit in the TS1s to the desired value (1b = ‐3.5 dB, 0b = ‐6 dB). 

- For data rates of 5.0 GT/s and higher, the master’s Transmitter can choose any de‐emphasis settings it wants, regardless of the settings it sent to the slave. 

- Potential problem: if Loopback is entered after the Link has already trained to L0 and LinkUp = 1b, it’s possible for one Port to enter Loop‐ back from Recovery and the partner to enter from Configuration. If that happened, the latter Port might try to change the speed while the Port entering from Recovery does not, resulting in a situation where the results are undefined. The spec states that the test set‐up must avoid conflicting cases like this. 

## _Exit to “Loopback.Active”_ 

The next state will be Loopback.Active after either 2ms, if the Compli‐ ance Receive bit is set in the outgoing TS1s, or two consecutive TS1s are received on a design‐specific number of Lanes with the Loopback bit set and the Compliance Receive bit was not set in the outgoing TS1s. 

Note that if the speed was changed, the master must ensure that enough TS1s have been sent for the slave to be able to acquire Symbol lock or Block alignment before going to the Loopback.Active state. 

## _Exit to “Loopback.Exit”_ 

If neither of the conditions to enter Loopback.Active are met, the next state will be Loopback.Exit after a design‐specific timeout of less than 100ms. 

## **Loopback Slave:** 

This substate is entered by receiving two consecutive TS1s with the Loop‐ back bit asserted. 

If this substate was entered from Configuration.Linkwidth.Start, check to see whether the speed in use is the highest one that mutually supported by both Link partners. If not: 

- Change to the highest common speed. Send one EIOS (two EIOSs if the current speed is 5.0 GT/s), and then go to Electrical Idle for 2ms. During the idle time, change the speed to the highest commonly‐sup‐ ported rate. 

- If the highest common rate is 5.0 GT/s, set the Transmitter’s de‐ emphasis according to the Selectable De‐emphasis bit in the received TS1s (1b = ‐3.5 dB, 0b = ‐6 dB). 

- If the highest common rate is 8.0 GT/s and: 

 - a) EQ TS1s directed the slave to this state, use the Tx Preset settings they specified. 

 - b) Normal TS1s directed the slave to this state, the slave is allowed to use its default transmitter settings. 

## _Exit to “Loopback.Active”_ 

The next state will be Loopback.Active if the Compliance Receive bit was set in the incoming TS1s that directed the slave to this state. The slave doesn’t need to wait for particular boundaries to send looped‐back data, and is allowed to truncate any Ordered Set in progress. 

Otherwise, the slave sends TS1s with Link and Lane numbers set to PAD and the next state will be Loopback.Active if: 

- The rate is 2.5 or 5.0 GT/s and Symbol lock is acquired on all Lanes. 

- The rate is 8.0 GT/s and two consecutive TS1s are seen on all active Lanes. Equalization is handled by evaluating and applying the values given in the TS1s, as long as they’re supported and the EC value is appropriate for the direction of the Port (10b for Downstream Ports, 

**Chapter 14: Link Initialization & Training** 

and 11b for Upstream Ports). Optionally, the Port can accept either of the EC values for this case. If the settings are applied, they must take effect within 500ns of receiving them and must not cause the Trans‐ mitter to violate any electrical specs for more than 1ns. A significant difference compared to the process in Recovery.Equalization is that the new settings are not echoed in the TS1s being sent by the slave. – For 8b/10b, the slave must only transition to looped‐back data on a Symbol boundary, but is allowed to truncate any Ordered Set in progress. For 128b/130b, no boundary is specified for when the looped‐back data can be sent, and it is still allowed to truncate any Ordered Set in progress. 

## **Loopback.Active** 

During this substate, the Loopback Master sends valid encoded data and should not send EIOS until it’s ready to exit Loopback. The Loopback Slave ech‐ oes the received information without modification (even if the encoding is determined to be invalid), with the possible exception of inverting the polarity as determined in the Polling state. The slave also continues to perform clock tol‐ erance compensation. That means SKPs must be added or removed as needed, but the Lanes aren’t required to all send the same number. 

## _Exit to “Loopback.Exit”_ 

The next state will be Loopback.Exit for the loopback master if directed. 

The next state will be Loopback.Exit for the loopback slave if either of two conditions is true: 

- The slave is directed to exit or four consecutive EIOSs are seen on any Lane. 

- Optionally, if the current speed is 2.5 GT/s and an EIOS is received or Electrical Idle is detected or inferred on any Lane. Electrical Idle may be inferred if any configured Lane has not detected an exit from Elec‐ trical Idle for 128  s.

</td>
<td style="background-color:#e8e8e8">

在此子状态期间，发送器将在至少 Lane 0 上发送 Beacon。请注意，此状态仅适用于上游端口，因为只有它们才能发送 Beacon。

## _退出到"Detect 状态"_

如果在某个上游端口的接收器上检测到电气空闲退出，则下一个状态将是 Detect。当然，必须已经恢复了设备的供电，相邻设备才能从电气空闲中退出。

## **热复位状态**

端口进入热复位状态，要么是因为它是一个桥，并且软件对其配置空间进行编程以向下游传播热复位（如第 837 页的"热复位（带内复位）"中所述），要么是因为端口接收到了两个连续的、Hot Reset 位被置位的 TS1。

## _热复位期间_

端口以 Hot Reset 位置位连续发送 TS1，但不更改已配置的链路和 Lane 编号。

如果交换机的上游端口进入热复位状态，则所有已配置的下游端口必须尽快转换为热复位。

## _退出到"Detect 状态"_

在发起热复位的桥中，一旦软件清除了发起热复位的配置空间位，桥端口就进入 Detect。但是，端口必须在热复位状态中保持至少 2ms。

**第 14 章：链路初始化与训练**

对于由于接收到两个连续的、Hot Reset 位置位的 TS1 而进入热复位的端口，只要它继续接收此类 TS1，它就保持在该状态。一旦端口停止接收 Hot Reset 位置位的 TS1，它将转换到 Detect 状态。但是，端口必须在热复位状态中保持至少 2ms。

## **禁用状态**

禁用的链路处于电气空闲状态，无需维持 DC 共模电压。软件通过在设备的 Link Control 寄存器中设置 Link Disable 位（请参见第 644 页的图 14‐71）来启动此操作，然后设备发送 Link Disable 位置位的 TS1。

## _禁用期间_

所有 Lane 发送 16 到 32 个 Link Disable 位置位的 TS1，发送一个 EIOS（对于 5.0 GT/s 情况为两个连续的 EIOS），然后转换到电气空闲。DC 共模电压不需要在规范范围内。

如果发送了 EIOS（对于 5.0 GT/s 情况为两个连续的 EIOS），并且在任何已配置的 Lane 上也接收到了 EIOS，则 LinkUp = 0b（假），并且 Lane 被认为是禁用的。

## _退出到"Detect 状态"_

对于上游端口，当在接收器处检测到电气空闲或者在 2ms 超时内未接收到 EIOS 时，下一个状态将是 Detect。

对于下游端口，下一个状态也将是 Detect，但只有在软件将 Link Disable 位清零至 0b 后才会发生。

## **回环状态**

回环状态是一个测试和调试功能，在正常运行期间不使用。充当回环主设备的设备可以通过发送 Loopback 位置位的 TS1 将链路伙伴置于回环从设备模式。这可以在电路中完成，从而可以使用回环状态对链路执行 BIST（Built In Self Test，内建自测试）。

一旦进入此状态，回环主设备将有效的 Symbol 发送给回环从设备，然后回环从设备将其回显。回环从设备继续执行

## **PCI Express 技术**

时钟容差补偿，因此主设备必须继续以正确的间隔插入 SOS。为了执行时钟容差补偿，回环从设备可能必须向其回传给回环主设备的 SOS 添加或删除 SKP Symbol。

回环状态在回环主设备发送 EIOS 并且接收器检测到电气空闲时退出。回环状态机如图 14‐44（第 614 页）所示，并在以下文本中描述。

_图 14‐44：回环状态机_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Loopback.Entry**

此子状态的典型行为是回环主设备发送 Loopback 位置位的 TS1，直到它开始看到这些 TS1 被返回。一旦回环主设备看到 Loopback 位被置位的 TS1 被返回，它就知道其链路伙伴现在正在充当回环从设备，并简单地重复其接收到的所有内容。

在此子状态期间，链路不被认为是活动的（LinkUp = 0b）。此外，TS1 和 TS2 中使用的链路和 Lane 编号将被接收器忽略。规范对 128b/130b 编码的 Lane 编号的使用做了一个有趣的观察。事实证明，每个 Lane 使用不同的种子值用于其加扰器（参见第 430 页的"加扰"）。因此，如果在进入回环模式之前尚未协商 Lane 编号，则链路伙伴可能具有不同的 Lane 分配，因此将无法识别传入的 Symbol。这可以通过在指导主设备进入回环状态之前等待 Lane 编号协商完成，或者通过指导主设备在 Loopback.Entry 期间设置 Compliance Receive 位，或通过其他方法来避免。

**第 14 章：链路初始化与训练**

## **Loopback Master:**

在此子状态中，回环主设备将连续发送 Loopback 位置位的 TS1。主设备还可以在 TS1 中置位 Compliance Receive 位，以帮助当一个或两个端口在速率变化后难以获得位锁定、Symbol 锁定或块对齐时进行测试。如果该位被置位，则在此状态期间不得清除。

如果此子状态是从 Configuration.Linkwidth.Start 进入的，请检查当前使用的速率是否是两个链路伙伴共同支持的最高速率。如果不是：

- 更改为最高公共速率。发送 16 个 Loopback 位置位的 TS1，后跟一个 EIOS（如果当前速率为 5.0 GT/s，则为两个 EIOS），然后进入电气空闲状态 1ms。在空闲期间，将速率更改为共同支持的最高速率。

- 如果最高公共速率为 5.0 GT/s，则从设备的 Tx 去加重由主设备在 TS1 中将其 Selectable De‐emphasis 位设置为所需的值（1b = ‐3.5 dB，0b = ‐6 dB）来控制。

- 对于 5.0 GT/s 及更高的数据速率，主设备的发送器可以选择任何其想要的去加重设置，无论它发送给从设备的设置如何。

- 潜在问题：如果在链路已经训练到 L0 且 LinkUp = 1b 之后进入回环，则一个端口可能从 Recovery 进入回环，而其伙伴从 Configuration 进入。如果发生这种情况，后一个端口可能尝试更改速率，而从 Recovery 进入的端口不会更改，从而导致结果未定义的情况。规范指出测试设置必须避免此类冲突情况。

## _退出到"Loopback.Active"_

在 2ms 之后，如果 Compliance Receive 位在发出的 TS1 中被置位，或者在设计特定数量的 Lane 上接收到两个连续的、Loopback 位置位且 Compliance Receive 位未在发出的 TS1 中置位的 TS1，则下一个状态将是 Loopback.Active。

请注意，如果更改了速率，则主设备必须确保已发送了足够的 TS1，以便从设备能够在进入 Loopback.Active 状态之前获得 Symbol 锁定或块对齐。

**PCI Express 技术**

## _退出到"Loopback.Exit"_

如果进入 Loopback.Active 的两个条件均未满足，则在小于 100ms 的设计特定超时之后，下一个状态将是 Loopback.Exit。

## **Loopback Slave:**

此子状态通过接收 Loopback 位置位的两个连续的 TS1 进入。

如果此子状态是从 Configuration.Linkwidth.Start 进入的，请检查当前使用的速率是否是两个链路伙伴共同支持的最高速率。如果不是：

- 更改为最高公共速率。发送一个 EIOS（如果当前速率为 5.0 GT/s，则为两个 EIOS），然后进入电气空闲状态 2ms。在空闲期间，将速率更改为共同支持的最高速率。

- 如果最高公共速率为 5.0 GT/s，则根据接收到的 TS1 中的 Selectable De‐emphasis 位设置发送器的去加重（1b = ‐3.5 dB，0b = ‐6 dB）。

- 如果最高公共速率为 8.0 GT/s 并且：

 - a) EQ TS1 指导从设备进入此状态，则使用它们指定的 Tx 预设设置。

 - b) 常规 TS1 指导从设备进入此状态，则允许从设备使用其默认发送器设置。

## _退出到"Loopback.Active"_

如果在指导从设备进入此状态的传入 TS1 中设置了 Compliance Receive 位，则下一个状态将是 Loopback.Active。从设备无需等待特定边界即可发送回送数据，并允许截断任何进行中的有序集。

否则，从设备发送链路和 Lane 编号设置为 PAD 的 TS1，并且如果满足以下条件，则下一个状态将是 Loopback.Active：

- 速率为 2.5 或 5.0 GT/s，并且在所有 Lane 上获得了 Symbol 锁定。

- 速率为 8.0 GT/s，并且在所有活动 Lane 上看到两个连续的 TS1。通过评估和应用 TS1 中给定的值来处理均衡，只要它们受支持并且 EC 值对于端口的方向是适当的（下行端口为 10b，

**第 14 章：链路初始化与训练**

上行端口为 11b）。可选地，端口可以接受这两个 EC 值中的任何一个以应对此情况。如果应用了设置，则必须在接收后 500ns 内生效，并且不得导致发送器在任何电气规范上违规超过 1ns。与 Recovery.Equalization 中的过程相比，一个重要的区别是从设备正在发送的 TS1 中不会回显新设置。— 对于 8b/10b，从设备必须仅在 Symbol 边界上转换为回送数据，但允许截断任何进行中的有序集。对于 128b/130b，没有指定何时可以发送回送数据的边界，但仍允许截断任何进行中的有序集。

## **Loopback.Active**

在此子状态期间，回环主设备发送有效的编码数据，并且在其准备退出回环之前不应发送 EIOS。回环从设备不加修改地回显接收到的信息（即使编码被确定为无效），但根据 Polling 状态确定的极性反转可能除外。从设备还继续执行时钟容差补偿。这意味着必须根据需要添加或删除 SKP，但不要求所有 Lane 都发送相同数量。

## _退出到"Loopback.Exit"_

对于回环主设备，如果被指导，则下一个状态将是 Loopback.Exit。

对于回环从设备，如果以下两个条件中的任何一个为真，则下一个状态将是 Loopback.Exit：

- 从设备被指示退出，或者在任何 Lane 上看到四个连续的 EIOS。

- 可选地，如果当前速率为 2.5 GT/s，并且接收到 EIOS 或在任何 Lane 上检测到或推断出电气空闲。如果任何已配置的 Lane 在 128 μs 内未检测到电气空闲退出，则可以推断为电气空闲。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0688_img1_tight.png" alt="Figure from page 688" width="700">

<a id="sec-14-7"></a>
## 14.7 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The slave must be able to detect an Electrical Idle on any Lane within 1ms of EIOS being received. Between the time EIOS is received and Electrical Idle is actually detected, the Loopback Slave may receive a bit stream that is undefined by the encoding scheme, and it may loop that back to the trans‐ mitter. 

## **Loopback.Exit** 

During this substate, the Loopback Master sends an EIOS for Ports that support only 2.5 GT/s and eight consecutive EIOSs for Ports that support rates higher than 2.5 GT/s (optionally send 8 for the Ports that only support 2.5 GT/s, too), and then enter Electrical Idle on all Lanes for 2ms. 

- The Loopback Master must transition to Electrical Idle within TTX‐IDLE‐SET‐ TO‐IDLE[after sending the last EIOS. Note that the EIOS marks the end of] the master’s transmit and compare operations. Any data received by the master after any EIOS is received is undefined and should be ignored. 

The loopback slave must enter Electrical Idle on all Lanes for 2ms but must echo back all Symbols received prior to detecting Electrical Idle to ensure that the master sees the arrival of the EIOS as the end of the logical send and compare operation. 

## _Exit to “Detect State”_ 

The next state will be Detect once the required EIOSs have been exchanged and the Lanes have been in Electrical Idle for 2ms. 

## **Dynamic Bandwidth Changes** 

Higher data rates and wider Links for PCIe offer higher performance than pre‐ vious generations but use more power, too. Consequently, the 2.0 spec writers chose to include another pair of power management mechanisms that allow the hardware to adjust the Link speed and width on the fly. These allow the Link to use the highest speed and widest possible Link when performance is needed, or to drop down to a lower speed or narrower Link width or both to reduce power. There are two clear advantages to this method compared to changing the Link or Device power state. 

First, the Link is always able to communicate regardless of the changes, with a relatively short interruption in service to make the change. Second, the power saving can be greater. For example, a x16 Link would almost certainly use less power operating as an active x1 Link than as a x16 Link in L0s. 

Secondly, in addition to power conservation, bandwidth reductions can also be used to resolve reliability problems. For example, it may be that a high speed Link produces unacceptable reliability, in which case either Link component is allowed to remove the offending speed from the list of supported speeds that it advertises. How a component makes that reliability determination is not speci‐ 

**Chapter 14: Link Initialization & Training** 

fied. Interestingly, components are also permitted to go into the Recovery state and advertise a different set of supported speeds without requesting a speed change in the process. 

Changing the Link Speed or Link Width requires the Link to be re‐trained. When the Link is in the L0 state, and the speed needs to be changed, the LTSSM of the port desiring the speed change starts transmitting TS1s to its neighbor. Doing so results in the two involved ports’ LTSSMs going through Recovery state where the Link speed is changed and then back to L0. 

Similarly, the port that desires to change the Link width starts transmitting TS1s to its neighbor. Doing so results in the two involved ports’ LTSSMs going through Recovery state then Configuration state where the Link width is changed. The LTSSM finally returns to L0 with the new Link width established. 

Because the LTSSM is involved in dynamic Link bandwidth management, it makes sense to discuss the two aspects of Link bandwidth management, dynamic Link speed change and dynamic Link width change in the following sections. Let’s consider these two options separately, starting with Link speed changes. 

## **Dynamic Link Speed Changes** 

By way of review, the LTSSM states are illustrated in Figure 14‐45 on page 620 to make it easier to recall the flow of states. Although according to the Gen1 specification, speed change was indicated to be performed in the Polling state, the subsequent Gen2 spec moved this function to the Recovery state. 

_Figure 14‐45: LTSSM Overview_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


During the Polling state, TS1s are exchanged between Link neighbors, and these contain several kinds of information as shown in Figure 14‐46 on page 621. The most interesting part for us here is byte number 4, the Rate Identifier. Bits 1, 2 and 3 indicate which data rates are available and the spec points out that 2.5 GT/s must always be supported, while 5.0 GT/s must also be supported if 8.0 GT/s is supported. 

The meaning of bit 6 depends on whether the Port is facing upstream or down‐ stream and also on what LTSSM state the Port is in. However, for the speed change case the options are reduced because it’s only meaningful coming from the Upstream Port and just indicates whether or not the speed change is an autonomous event. “Autonomous” means that the Port is requesting this change for its own hardware‐specific reasons and not because of a reliability issue. Bit 7 is used by the Upstream Port to request a speed change. These val‐ ues are very similar in the TS2s, although bit 6 has another meaning now related to autonomous Link width changes that we’ll discuss later. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐46: TS1 Contents_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


_Figure 14‐47: TS2 Contents_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Upstream Port Initiates Speed Change** 

A speed change must be initiated by the Upstream Port (Port facing upstream), and is accomplished by transitioning to the Recovery state. The substates of the Recovery state are shown in Figure 14‐48 on page 622 and the part of interest for this discussion is highlighted by the oval. The discussion that follows here is a relatively high‐level overview of the entire speed change process and doesn’t get into the details of the LTSSM operation. To learn more about that, refer to the discussion called “Recovery State” on page 571. 

_Figure 14‐48: Recovery Sub‐States_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Speed Change Example** 

To illustrate the process, consider the speed change example shown in Figure 14‐49 on page 623. Note that the Equalization substate has been removed in this example to make the diagrams simpler and easier to follow. The example shows a change from 2.5 GT/s to 5.0 GT/s and so the Equalization substate is not used anyway. A change to 8.0 GT/s would go through the same process but would just add a trip through the Equalization substate at the end of the process. To 

**Chapter 14: Link Initialization & Training** 

learn more about the Equalization process, refer to “Recovery.Equalization” on page 587. 

The Endpoint in this example, which can only have an Upstream Port, is shown connected to a Root Complex, which can only have Downstream Ports. Only the Upstream Port can initiate the speed change process, and it does so because its _Directed Speed Change_ flag was set earlier based on some hardware‐specific con‐ ditions. To start the sequence, it changes its LTSSM to the Recovery state, enters the Recovery.RcvrLock substate and sends TS1s with the Speed Change bit set and listing the speeds that it will support, as shown in Figure 14‐49 on page 623. When the Downstream Port sees the incoming TS1s, it also changes to the Recovery state and begins sending TS1s back. Since the Speed Change bit was set in the incoming TS1s, that will set the _Directed Speed Change_ flag in the Root Port and the outgoing TS1s will also have that bit set. The speed that the Link will attempt to use will be the highest commonly‐supported speed so, if a Device wants to use a lower speed it would simply not list the higher speeds as being supported at this time. 

_Figure 14‐49: Speed Change ‐ Initiated_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


When the Upstream Port detects the TS1s coming back, its state machine changes to the Recovery.RcvrCfg substate and it begins to send TS2s that still have the Speed Change bit set, as illustrated in Figure 14‐50 on page 624. These 

TS2s will now also have the Autonomous Change bit set if this change was not caused by a reliability problem on the Link. When the Downstream Port sees incoming TS2s, it also changes to the Recovery.RcvrCfg substate and returns TS2s with the Speed Change bit set. However, the Autonomous Change bit is reserved in the TS2s for Downstream Ports during Recovery. 

_Figure 14‐50: Speed Change ‐ Part 2_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


Once each Port has seen 8 consecutive TS2s with the Speed Change bit set, they know that the next step will be to go to the Recovery.Speed substate, as shown in Figure 14‐51 on page 625. At this point, the Downstream Port needs to regis‐ ter the setting of the Autonomous Change bit in the incoming TS2s. To support this, some extra fields have been added to the PCIe Capability registers. 

The status bits for Link bandwidth changes are found in the Link Status regis‐ ter, shown in Figure 14‐52 on page 625. Status changes can also be used to gen‐ erate an interrupt to notify software of these events if the device is capable and has been enabled to do so. This capability is reported by the Link Bandwidth Notification Capable bit, shown in Figure 14‐53 on page 626, and enabled by the Interrupt Enable bits in the Link Control register, as shown in Figure 14‐54 on 

</td>
<td style="background-color:#e8e8e8">

**Chapter 14: Link Initialization & Training** 

第 626 页。请注意,有两种情况:自主和带宽管理。自主意味着更改不是由可靠性问题引起的,而带宽管理意味着是。

_Figure 14-51: 速度更改 - 第 3 部分_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **PCI Express Technology** 

_Figure 14-53: Bandwidth Notification Capability_ 

_Figure 14-54: Bandwidth Change Notification Bits_ 

**Chapter 14: Link Initialization & Training** 

一旦到达 Recovery.Speed 子状态,链路将在两个方向上置于 Electrical Idle 条件,并且内部更改速度。所选速度将是 TS1 和 TS2 的 Rate ID 字段中报告的最高共同支持的速度。在此示例中,结果为 5.0 GT/s,因此将更改为该速度。经过一段时间后,链路邻居都转换回 Recovery.RcvrLock 并通过再次发送 TS1 退出 Electrical Idle,如图 14-55(第 627 页)所示。当上游端口看到它们返回时,它转换为 Recovery.RcvrCfg 并开始发送 TS2,类似于之前。但是,这次未设置 Speed Change 位。最终,从未设置 Speed Change 位的下游端口也看到了 TS2 返回,此时状态机转换到 Recovery.Idle,然后返回 L0。

如果速度更改由于某种原因失败,则不允许组件在返回 L0 后至少 200ms 或直到链路伙伴通告支持更高速度之前(以先到者为准)再尝试该速度或更高的速度。

_Figure 14-55: 速度更改完成_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **速度更改的软件控制** 

软件无法控制硬件何时做出更改速度的决定,但可以限制或禁用此功能。限制它是通过设置 Link Control 2 Register(如图 14-56(第 628 页)所示)中的 Target Link Speed 值来实现的。这充当上游端口可用速度的上限,它将尝试维持该值或两个链路邻居都支持的最高速度,以较低者为准。软件还可以通过在上游组件中设置 Target Link Speed 然后设置 Link Control 寄存器(如图 14-57(第 629 页)所示)中的 Retrain Link 位来强制使用特定速度。如前所述,任何基于硬件的链路速度或宽度更改都会通过 Link Bandwidth Notification Mechanism 通知软件。最后,可以通过设置 Hardware Autonomous Speed Disable 位来禁用速度更改机制。

_Figure 14-56: Link Control 2 寄存器_ 

**Chapter 14: Link Initialization & Training** 

_Figure 14-57: Link Control 寄存器_ 

## **Dynamic Link Width Changes** 

用于更改链路速度的相同基本操作也可用于更改链路宽度,尽管由于涉及更多 LTSSM 步骤,该序列稍微更复杂。在启用链路宽度更改之前,软件需要注意的一件重要事情是链路邻居是否支持从窄链路恢复到宽链路(称为 Upconfiguring the Link)。设备在训练期间发送的 TS2 的 Rate ID 字段的位 6 中报告此能力,如图 14-58(第 630 页)所示。如果组件不支持此功能,则意味着更改到较窄的链路宽度将是单向事件,并且仅适用于链路上存在可靠性问题的情况。

## **PCI Express Technology** 

_Figure 14-58: TS2 内容_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **链路宽度更改示例** 

考虑图 14-59(第 631 页)中连接到端点 (千兆以太网设备) 的 Root Port 的示例。只有上游端口将发起此更改,并且它像之前一样通过进入 Recovery 状态来开始。但是,这次未设置 Speed Change 位。为了确定新的链路宽度是什么,上游端口将需要告诉下游端口从 Recovery 状态转换为 Configuration 状态,然后再返回 L0,如图 14-60(第 631 页)所示。Configuration 状态中有几个子状态,其简化版本如图 14-61(第 632 页)所示。我们将介绍该序列,以清楚地了解步骤的工作原理。

**Chapter 14: Link Initialization & Training** 

_Figure 14-59: 链路宽度更改示例_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


_Figure 14-60: 链路宽度更改 LTSSM 序列_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **PCI Express Technology** 

_Figure 14-61: 简化的 Configuration 子状态_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


与之前一样,上游端口通过进入 Recovery 并发送 TS1 来启动此过程。这些未设置 Speed Change 位,如第 631 页的 Figure 14-59 中突出显示的示例所示,其中以太网设备在其上游端口上启动此过程。作为响应,下游端口发回 TS1,也清除了 Speed Change 位。Link 和 Lane 编号仍显示为与上次训练链路时未更改。参考第 622 页的 Figure 14-48,下一个状态是 Recovery.RcvrCfg,在该状态中链路伙伴交换 TS2。

**Chapter 14: Link Initialization & Training** 

_Figure 14-62: 链路宽度更改 - 开始_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


由于未请求速度更改,因此下一个状态是 Recovery.Idle。在该状态下,端口通常发送逻辑空闲符号(全零),下游端口会这样做,如图 14-63(第 634 页)所示。但是,上游端口被指示更改链路宽度,因此它不会发送预期的 Idle 符号。相反,它发送 Link 和 Lane 编号均为 PAD 的 TS1。下游端口识别出先前配置的 Lane 现在的 Lane 编号为 PAD,这会导致其转换为第一个 Configuration 子状态:Config.Linkwidth.Start。

## **PCI Express Technology** 

## _Figure 14-63: 链路宽度更改 - Recovery.Idle_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


下游端口现在通过发送具有原始协商的 Link 编号但所有 Lane 编号为 PAD 的 TS1 来启动下一步,如图 14-64(第 635 页)所示。上游端口在其希望"活动"的 Lane 上以匹配的 TS1 进行响应,但在其希望处于非活动状态的 Lane 上以 Link 和 Lane 编号均为 PAD 进行响应。当下游端口看到此响应时,它将转换为 Config.Linkwidth.Accept 子状态。请注意,这些 TS1 设置了 Autonomous Change 位。

**Chapter 14: Link Initialization & Training** 

_Figure 14-64: 标记活动 Lane_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0697_img1_tight.png" alt="Figure from page 697" width="700">

<a id="sec-14-8"></a>
## 14.8 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Chapter 14: Link Initialization & Training** 

page 626. Note that there are two cases: autonomous and bandwidth manage‐ men. Autonomous means the change was not caused by a reliability problem, while bandwidth management means it was. 

_Figure 14‐51: Speed Change ‐ Part 3_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **PCI Express Technology** 

_Figure 14‐53: Bandwidth Notification Capability_ 

_Figure 14‐54: Bandwidth Change Notification Bits_ 

**Chapter 14: Link Initialization & Training** 

Once the Recovery.Speed substate is reached, the Link is placed into the Electri‐ cal Idle condition in both directions and the speed is changed internally. The speed chosen will be the highest commonly‐supported speed reported in the Rate ID field of the TS1s and TS2s. In this example, that turns out to be 5.0 GT/s and so the change is made to that speed. After a timeout period, the Link neigh‐ bors both transition back to Recovery.RcvrLock and exit Electrical Idle by send‐ ing TS1s again, as shown in Figure 14‐55 on page 627. When the Upstream Port sees them coming back, it transitions to Recovery.RcvrCfg and begins sending TS2s, much like before. This time, though, the Speed Change bit is not set. Even‐ tually TS2s are seen coming back from the Downstream Port that also don’t have the Speed Change bit set, and at that point the state machines transition to the Recovery.Idle on their way back to L0. 

If a speed change has fails for some reason, a component is not allowed to try that speed or a higher one for at least 200 ms after returning to L0 or until the Link neighbor advertises support for a higher speed, whichever comes first. 

_Figure 14‐55: Speed Change Finish_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Software Control of Speed Changes** 

Software is unable to control when hardware makes decisions about changing the speed but can limit or disable this capability. Limiting it is accomplished by setting the Target Link Speed value in the Link Control 2 Register shown in Fig‐ ure 14‐56 on page 628. This acts as the upper bound on the speeds available to 

the Upstream Port, which will try to maintain that value or the highest speed supported by both Link neighbors, whichever is lower. Software can also force a particular speed to be used by setting the Target Link Speed in the Upstream component and then setting the Retrain Link bit in the Link Control register, shown in Figure 14‐57 on page 629. As mentioned earlier, software is notified of any hardware‐based Link speed or width changes by the Link Bandwidth Noti‐ fication Mechanism. Finally, the speed change mechanism can be disabled by setting the Hardware Autonomous Speed Disable bit. 

_Figure 14‐56: Link Control 2 Register_ 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐57: Link Control Register_ 

## **Dynamic Link Width Changes** 

The same basic operation for changing the Link speed can also be used to change the Link width, although the sequence is a little more complicated because more LTSSM steps are involved. One thing that’s important for soft‐ ware to note before enabling Link width changes is whether the Link neighbor supports recovering from a narrow Link back to a wide Link (called Upconfig‐ uring the Link). Devices report this ability in bit 6 of the Rate ID field of the TS2s they send during training, as shown in Figure 14‐58 on page 630. If a component doesn’t support this, that would mean that changing to a narrower Link width would be a one‐way event and would only be suitable for the case of a reliabil‐ ity problem on the Link. 

_Figure 14‐58: TS2 Contents_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Link Width Change Example** 

Consider the example in Figure 14‐59 on page 631 of a Root Port connected to an Endpoint (Gigabit Ethernet Device). Only the Upstream Port will initiate this change, and it begins by going to the Recovery state as before. This time, though, the Speed Change bit is not set. To sort out what the new Link width will be, the Upstream Port will need to tell the Downstream Port to transition from the Recovery state to the Configuration state before going back to L0, as shown in Figure 14‐60 on page 631. There are several substates in the Configu‐ ration state, and a simplified version of them is shown in Figure 14‐61 on page 632. We’ll go through the sequence to be clear on how the steps work. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐59: Link Width Change Example_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


_Figure 14‐60: Link Width Change LTSSM Sequence_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **PCI Express Technology** 

_Figure 14‐61: Simplified Configuration Substates_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


As before, the Upstream Port initiates this process by going to Recovery and sending TS1s. These don’t have the Speed Change bit set, as highlighted in the example shown in Figure 14‐59 on page 631, where an Ethernet Device initiates this process on its Upstream Port. In response, the Downstream Port sends TS1s back, also with the Speed Change bit cleared. Link and Lane numbers are still shown as being unchanged from the last time the Link was trained. Referring back to Figure 14‐48 on page 622, the next state is Recovery.RcvrCfg during which the Link partners exchange TS2s. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐62: Link Width Change ‐ Start_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


Since a speed change is not requested, the next state is Recovery.Idle. In that state the Ports normally send the logical idle symbols (all zeros) and the Down‐ stream Port does so, as shown in Figure 14‐63 on page 634. However, the Upstream Port was directed to change the Link width so it doesn’t send the expected Idle symbols. Instead, it sends TS1s with PAD for both the Link and Lane numbers. The Downstream Port recognizes that a previously configured Lane now has a Lane number of PAD, and that causes it to transition to the first Configuration substate: Config.Linkwidth.Start. 

## _Figure 14‐63: Link Width Change ‐ Recovery.Idle_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


The Downstream Port now initiates the next step by sending TS1s that have the originally negotiated Link number but PAD on all the Lane numbers, as illus‐ trated in Figure 14‐64 on page 635. The Upstream Port responds with matching TS1s on the Lanes it wants to have “active”, but with PAD for both Link and Lane numbers on the Lanes it wishes to have inactive. When the Downstream Port sees this response, it transitions to the Config.Linkwidth.Accept substate. Note that the Autonomous Change bit is set for these TS1s. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐64: Marking Active Lanes_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

</td>
<td style="background-color:#e8e8e8">

Root Port 通过将其 TS1 更改为显示适合活动 Lane 的 Lane 编号,但对于看到非活动的所有 Lane 的 Link 和 Lane 编号使用 PAD 来响应。上游端口以相同的 TS1 进行响应,如图 14-65(第 636 页)所示,并且状态更改为 Config.Lanenum.Accept。此时,Root Port 更新状态位以显示检测到自主更改,并更改为 Config.Complete 子状态。

## **PCI Express Technology** 

## _Figure 14-65: 对 Lane 编号更改的响应_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


在下一步中,Root Port 开始在活动 Lane 上发送 TS2,并将非活动 Lane 置于 Electrical Idle。请记住,TS2 报告组件是否"支持 upconfigure",在此示例中,两个链路伙伴都支持此能力。端点发回相同的内容:活动 Lane 上的 TS2 和非活动 Lane 上的 Electrical Idle。看到这一点,Root Port 的状态机更改为 Config.Idle,并开始在活动 Lane 上发送 Logical Idle。端点以相同的内容进行响应,链路状态变回 L0。链路现在已准备好进行正常操作,尽管带宽已降低以节省功率。

**Chapter 14: Link Initialization & Training** 

_Figure 14-66: 链路宽度更改 - 完成_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


与动态速度更改的情况一样,软件无法发起链路宽度更改,但它可以通过设置 Link Control 寄存器(如图 14-67(第 638 页)所示)中的相应位来禁用此机制。与速度更改情况不同,未定义允许设置特定链路宽度的软件机制。

## **PCI Express Technology** 

_Figure 14-67: Link Control 寄存器_ 

## **相关配置寄存器** 

许多与链路初始化和训练相关的配置寄存器已在其内容描述时显示过,但在这里汇总它们似乎很好。

## **Link Capabilities 寄存器** 

Link Capabilities 寄存器如图 14-68(第 639 页)所示,每个位字段在以下小节中描述。

**Chapter 14: Link Initialization & Training** 

## _Figure 14-68: Link Capabilities 寄存器_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Max Link Speed [3:0]** 

这指示此端口的最大链路速度,并作为指向 Link Capabilities 2 寄存器 Supported Link Speeds Vector 中对应于最大链路速度的位位置的指针给出。已定义的编码为:

- 0001b - Supported Link Speeds Vector 字段位 0 

- 0010b - Supported Link Speeds Vector 字段位 1 

- 0011b - Supported Link Speeds Vector 字段位 2 

- 0100b - Supported Link Speeds Vector 字段位 3 

- 0101b - Supported Link Speeds Vector 字段位 4 

- 0110b - Supported Link Speeds Vector 字段位 5 

- 0111b - Supported Link Speeds Vector 字段位 6 

所有其他编码均保留。共享上游端口的多功能设备必须在所有 Function 中的此字段中报告相同的值。此寄存器为只读。

## **PCI Express Technology** 

## **Maximum Link Width[9:4]** 

此字段指示 PCI Express 链路的最大宽度。定义的值有:

- 00 0000b: 保留 

- 00 0001b: x1 

- 00 0010b: x2 

- 00 0100b: x4 

- 00 1000b: x8 

- 00 1100b: x12 

- 01 0000b: x16 

- 10 0000b: x32 

所有其他编码均保留。共享上游端口的多功能设备必须在所有 Function 中的此字段中报告相同的值。此寄存器为只读。

## **Link Capabilities 2 寄存器** 

Link Capabilities 寄存器如图 14-68(第 639 页)所示,并显示 Link Capabilities 寄存器中的 Max Link Speed 字段所指向的 Supported Link Speeds Vector。此字段的值为:

- 位 0 = 2.5 GT/s 

- 位 1 = 5.0 GT/s 

- 位 2 = 8.0 GT/s 

- 位 6:3 RsvdP(保留并保留)。

_Figure 14-69: Link Capabilities 2 寄存器_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**Chapter 14: Link Initialization & Training** 

## **Link Status 寄存器** 

Link Status 寄存器如图 14-39(第 597 页)所示。

## **Current Link Speed[3:0]:** 

此只读字段指示当前链路速度。当链路首次训练到 L0 时,速度始终为 2.5 GT/s。之后,如果可获得更高的共同支持的速度,LTSSM 将进入 Recovery 并尝试更改为该速度。此字段中的值与 Link Capabilities 寄存器中显示的 Max Link Speed 编码相同:

- 0001b - Supported Link Speeds Vector 字段位 0 

- 0010b - Supported Link Speeds Vector 字段位 1 

- 0011b - Supported Link Speeds Vector 字段位 2 

- 0100b - Supported Link Speeds Vector 字段位 3 

- 0101b - Supported Link Speeds Vector 字段位 4 

- 0110b - Supported Link Speeds Vector 字段位 5 

- 0111b - Supported Link Speeds Vector 字段位 6 

所有其他编码均保留。

请注意,当链路未启动时(LinkUp = 0b),此字段的值是未定义的。

## **Negotiated Link Width[9:4]** 

此字段指示链路宽度协商的结果。有七种可能的宽度,所有其他编码均保留。已定义的编码为:

- 00 0001b: 对于 x1。 

- 00 0010b: 对于 x2。 

- 00 0100b: 对于 x4。 

- 00 1000b: 对于 x8。 

- 00 1100b: 对于 x12。 

- 01 0000b: 对于 x16。 

- 10 0000b: 对于 x32。 

所有其他编码均保留。请注意,当链路未启动时(LinkUp = 0b),此字段的值是未定义的。

## **PCI Express Technology** 

## **Undefined[10]** 

当前未定义,此位在早期规范版本中由硬件在发生链路训练错误时设置。它在 LTSSM 成功进入 L0 时被清除。规范指出,软件可以向此位写入任何值,但必须忽略从中读取的任何值。

## **Link Training[11]** 

此只读位指示 LTSSM 正在训练过程中。从技术上讲,它意味着 LTSSM 处于 Configuration 或 Recovery 状态,或者 Retrain Link 位已写入 1b 但链路训练尚未开始。当 LTSSM 退出 Configuration 或 Recovery 状态时,此位由硬件清除。由于这必须在链路训练进行时对软件可见,因此它仅对面向下游的端口有意义。因此,对于端点、桥接器上游端口和交换机上游端口,此位不适用并保留。对于它们,此位必须硬连线为 0b。

_Figure 14-70: Link Status 寄存器_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Link Control 寄存器** 

Link Control 寄存器如图 14-71(第 644 页)所示,其中有三个字段对我们来说是有意义的。

**Chapter 14: Link Initialization & Training** 

## **Link Disable** 

当设置为 1 时,链路被禁用。直观地说,此位不适用,对于端点、桥接器上游端口和交换机上游端口是保留的,因为即使链路被禁用,它也必须可由软件访问。写入此位后,任何读取立即反映写入的值,与链路状态无关。清除此位后,软件必须小心遵守有关 Conventional Reset 后首次 Configuration 读取的时序要求(参见第 846 页的"Reset Exit")。

## **Retrain Link** 

只要认为有必要,例如用于错误恢复,此位允许软件发起链路重新训练。该位不适用于端点设备以及桥接器和交换机的上游端口,并为其保留。当设置为 1b 时,这将在 Configuration 写入请求完成返回之前将 LTSSM 定向到 Recovery 状态。

## **Extended Synch** 

就其对训练的影响而言,此位用于大幅延长两种情况下的时间,以帮助较慢的外部测试或分析硬件在链路恢复正常通信之前与之同步。其中一种是在退出 L0s 时,设置此位强制在进入 L0 之前传输 4096 个 FTS。另一种情况是在进入 Recovery.RcvrCfg 之前的 Recovery 状态中,它强制传输 1024 个 TS1。

## **PCI Express Technology** 

## _Figure 14-71: Link Control 寄存器_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## Part Five: 

# Additional System Topics 

## _**15 Error Detection and Handling**_ 

## **The Previous Chapter**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-9"></a>
## 14.9 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The Root Port responds by changing its TS1s to show Lane numbers that are appropriate for the active Lanes, but PAD for the Link and Lane numbers of all the Lanes that were seen to be inactive. The Upstream Port responds with the same TS1s, as shown in Figure 14‐65 on page 636, and the state changes to Con‐ fig.Lanenum.Accept. At this point, the Root Port updates the status bit to show that an autonomous change was detected and changes to the Config.Complete substate. 

## **PCI Express Technology** 

## _Figure 14‐65: Response to Lane Number Changes_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


In the next step, the Root Port begins to send TS2s on the active Lanes and puts the inactive Lanes into Electrical Idle. Recall that the TS2s report whether a com‐ ponent is “upconfigure capable” and in this example, both Link partners sup‐ port this capability. The Endpoint sends back the same thing: TS2s on active Lanes and Electrical Idle on inactive Lanes. Seeing that, the Root Port’s state machine changes to Config.Idle and it begins to send Logical Idle on the active Lanes. The Endpoint responds with the same thing and the Link state changes back to L0. The Link is now ready for normal operation, albeit with a reduced bandwidth for power conservation. 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐66: Link Width Change ‐ Finish_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


As was the case for dynamic speed changes, software can’t initiate Link width changes, but it can disable this mechanism by setting the bit in the Link Control register shown in Figure 14‐67 on page 638. Unlike the speed change case, no software mechanism was defined to allow setting a particular Link width. 

## **PCI Express Technology** 

_Figure 14‐67: Link Control Register_ 

## **Related Configuration Registers** 

Many of the configuration registers that are relevant to Link Initialization and Training have been shown when their contents were described earlier, but it seems good to summarize them here. 

## **Link Capabilities Register** 

The Link Capabilities Register is pictured in Figure 14‐68 on page 639 and each bit field is described in the subsections that follow. 

**Chapter 14: Link Initialization & Training** 

## _Figure 14‐68: Link Capabilities Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Max Link Speed [3:0]** 

This indicates the maximum Link speed for this port, and is given as a pointer to a bit location in the Link Capabilities 2 register Supported Link Speeds Vector that corresponds to the max Link speed. Defined encodings are: 

- 0001b ‐ Supported Link Speeds Vector field bit 0 

- 0010b ‐ Supported Link Speeds Vector field bit 1 

- 0011b ‐ Supported Link Speeds Vector field bit 2 

- 0100b ‐ Supported Link Speeds Vector field bit 3 

- 0101b ‐ Supported Link Speeds Vector field bit 4 

- 0110b ‐ Supported Link Speeds Vector field bit 5 

- 0111b ‐ Supported Link Speeds Vector field bit 6 

All other encodings are reserved. Multi‐function devices sharing an Upstream Port must report the same value in this field in all Functions. This register is Read Only. 

## **Maximum Link Width[9:4]** 

This field indicates the maximum width of the PCI Express Link. The values that are defined are: 

- 00 0000b: Reserved 

- 00 0001b: x1 

- 00 0010b: x2 

- 00 0100b: x4 

- 00 1000b: x8 

- 00 1100b: x12 

- 01 0000b: x16 

- 10 0000b: x32 

All other encodings are reserved. Multi‐function devices sharing an Upstream Port must report the same value in this field in all Functions. This register is Read Only. 

## **Link Capabilities 2 Register** 

The Link Capabilities Register is pictured in Figure 14‐68 on page 639 and shows the Supported Link Speeds Vector to which the Max Link Speed field in the Link Capabilities register points. The values for this field are: 

- Bit 0 = 2.5 GT/s 

- Bit 1 = 5.0 GT/s 

- Bit 2 = 8.0 GT/s 

- Bits 6:3 RsvdP (reserved and preserved). 

_Figure 14‐69: Link Capabilities 2 Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**Chapter 14: Link Initialization & Training** 

## **Link Status Register** 

The Link Status Register is pictured in Figure 14‐39 on page 597. 

## **Current Link Speed[3:0]:** 

This read‐only field indicates the current Link speed. The speed will always be 2.5 GT/s when the Link first trains to L0. After that, if a higher commonly‐sup‐ ported speed is available, the LTSSM will go to Recovery and attempt to change to that speed. The values in this field are the same as the Max Link Speed encod‐ ings shown in the Link Capabilities register: 

- 0001b ‐ Supported Link Speeds Vector field bit 0 

- 0010b ‐ Supported Link Speeds Vector field bit 1 

- 0011b ‐ Supported Link Speeds Vector field bit 2 

- 0100b ‐ Supported Link Speeds Vector field bit 3 

- 0101b ‐ Supported Link Speeds Vector field bit 4 

- 0110b ‐ Supported Link Speeds Vector field bit 5 

- 0111b ‐ Supported Link Speeds Vector field bit 6 

All other encodings are reserved. 

Note that the value of this field is undefined when the Link is not up (LinkUp = 0b). 

## **Negotiated Link Width[9:4]** 

This field indicates the result of link width negotiation. There are seven possible widths, all other encodings are reserved. The defined encodings are: 

- 00 0001b: for x1. 

- 00 0010b for x2. 

- 00 0100b for x4. 

- 00 1000b for x8. 

- 00 1100b for x12. 

- 01 0000b for x16. 

- 10 0000b for x32. 

All other encodings are reserved. Note that the value of this field is undefined when the Link is not up (LinkUp = 0b). 

## **Undefined[10]** 

Currently undefined, this bit was previously set by hardware in earlier spec ver‐ sions when a Link Training Error had occurred. It was cleared when the LTSSM successfully entered L0. The spec states that software can write any value to this bit but must ignore any value read from it. 

## **Link Training[11]** 

This read‐only bit indicates that the LTSSM is in the process of training. Techni‐ cally, it means the LTSSM is either in the Configuration or Recovery state, or that the Retrain Link bit has been written to 1b but Link training has not yet begun. This bit is cleared by hardware when the LTSSM exits the Configuration or Recovery state. Since this must be visible to software while Link Training is in progress, it only has meaning for Ports that are facing downstream. Conse‐ quently, this bit is not applicable and reserved for Endpoints, bridge Upstream Ports and Switch Upstream Ports. For them, this bit must be hardwired to 0b. 

_Figure 14‐70: Link Status Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Link Control Register** 

The Link Control Register is pictured in Figure 14‐71 on page 644, and there are three fields in it that are interesting for us here. 

**Chapter 14: Link Initialization & Training** 

## **Link Disable** 

When set to one, the link is disabled. Intuitively, this bit isn’t applicable and is reserved for Endpoints, bridge Upstream Ports, and Switch Upstream Ports because it must be accessible by software even when the Link is disabled. When this bit is written, any read immediately reflects the value written, regardless of the Link state. After clearing this bit, software must be careful to honor the tim‐ ing requirements regarding the first Configuration Read after a Conventional Reset (see “Reset Exit” on page 846). 

## **Retrain Link** 

This bit allows software to initiate Link re‐training whenever it is deemed nec‐ essary, as for error recovery. The bit is not applicable to and is reserved for End‐ point devices and Upstream Ports of Bridges and Switches. When set to 1b, this directs the LTSSM to the Recovery state before the completion of the Configura‐ tion write Request is returned. 

## **Extended Synch** 

As it affects training, this bit is used to greatly extend the time spent in two situ‐ ations, for the purpose of assisting slower external test or analysis hardware to synchronize with the Link before it resumes normal communication. One of these is when exiting L0s, where setting this bit forces the transmission of 4096 FTSs prior to entering L0. The other case is in the Recovery state prior to enter‐ ing Recovery.RcvrCfg, where it forces the transmission of 1024 TS1s. 

## _Figure 14‐71: Link Control Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## Part Five: 

# Additional System Topics 

## _**15 Error Detection and Handling**_ 

## **The Previous Chapter**

</td>
<td style="background-color:#e8e8e8">

本章描述了物理层 (Physical Layer) 的链路训练和状态状态机 (LTSSM) 的操作。链路的初始化过程从电源开启或复位开始描述,直到链路达到完全可操作的 L0 状态,在该状态下发生正常的分组流量。此外,还讨论了链路电源管理状态 L0s、L1、L2 和 L3 以及状态转换。描述了在其中重新建立位锁、符号锁或块锁的 Recovery 状态。还讨论了用于链路带宽管理的链路速度和宽度更改。

## **本章** 

虽然始终注意最小化错误,但无法消除它们,因此检测和报告它们是一个重要的考虑因素。本章讨论了发生在 PCIe 端口或链路中的错误类型,如何检测、报告以及处理选项。由于 PCIe 被设计为与 PCI 错误报告向后兼容,因此包括对 PCI 错误处理方法的审查作为背景信息。然后我们专注于 PCIe 错误处理的可纠正、非致命和致命错误。

## **下一章** 

下一章为系统电源管理的讨论提供整体上下文,并详细描述 PCIe 电源管理,它与 _PCI Bus PM Interface Spec_ 和 _Advanced Configuration and Power Interface_ (ACPI) 兼容。PCIe 定义了对 PCI-PM 规范的扩展,主要侧重于链路电源和事件管理。

## **PCI Express Technology** 

## **背景** 

与 PCI 的软件向后兼容性是 PCIe 的一个重要特性,这是通过保留已就位的 PCI 配置寄存器来实现的。PCI 在总线的每个传输阶段验证正确的奇偶校验以检查错误。检测到的错误记录在状态寄存器中,并且可以选择使用两个边带信号中的任一个进行报告:PERR#(奇偶校验错误)用于数据传输期间潜在可恢复的奇偶校验错误,SERR#(系统错误)用于通常不可恢复的更严重的问题。这两种类型可分类如下:

- 普通数据奇偶校验错误 — 通过 PERR# 报告 

- 多任务事务(特殊周期)期间的数据奇偶校验错误 — 通过 SERR# 报告 

- 地址和命令奇偶校验错误 — 通过 SERR# 报告 

- • 其他类型的错误(设备特定) — 通过 SERR# 报告 

应如何处理错误不在 PCI 规范的范围内,可能包括硬件支持或设备特定软件。例如,对内存的读取期间的数据奇偶校验错误可以通过检测条件并简单地重复请求在硬件中恢复。如果失败的操作未更改内存内容,则这将是安全的步骤。

如图 15-1(第 649 页)所示,两个错误引脚通常连接到芯片组,并用于在消费 PC 中向 CPU 发出信号。这些机器对成本非常敏感,因此它们通常没有足够的错误处理预算。因此,所选择的最终错误报告信号是从芯片组到处理器的 NMI(Non-Maskable Interrupt)信号,指示需要立即关注的重大系统问题。大多数消费 PC 不包括这种情况的错误处理程序,因此系统将简单地停止以避免损坏,并且 BSOD(蓝屏死机)将通知操作员。SERR# 条件的示例是事务命令阶段期间看到的地址奇偶校验不匹配。这是潜在破坏性的情况,因为错误的目标可能会响应。如果发生这种情况并且 SERR# 报告它,恢复将很困难,并且可能需要大量软件开销。(要了解有关 PCI 错误处理的更多信息,请参阅 MindShare 的书 _PCI System Architecture_ 。)

PCI-X 使用相同的两个错误报告信号,但定义具体的错误处理要求,具体取决于是否存在设备特定的错误处理软件。如果不存在此类处理程序,则所有奇偶校验错误都将使用 SERR# 报告。
## _Figure 15-1: PCI 错误处理_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


PCI-X 2.0 使用源同步时钟来实现更快的数据速率(高达 4GB/s)。该总线面向高端企业系统,因为它通常对于消费类机器来说过于昂贵。由于这些高性能系统还需要高可用性,规范作者选择通过添加纠错码 (ECC) 支持来改进错误处理。ECC 允许更强大的错误检测,并能够即时纠正单位错误。ECC 在最小化传输错误的影响方面非常有用。(要了解有关 PCI-X 错误处理的更多信息,请参阅 MindShare 的书 _PCI-X System Architecture_ 。)

PCIe 通过使用旧版配置寄存器中的错误状态位来记录与 PCI 相似的 PCIe 错误事件,从而保持与这些旧版机制的向后兼容性。这使旧版软件能够以其理解的术语查看 PCIe 错误事件,并允许它与 PCIe 硬件一起使用。有关这些寄存器的详细信息,请参阅第 674 页的"PCI-Compatible Error Reporting Mechanisms"。

## **PCI Express Technology** 

## **PCIe 错误定义** 

规范使用四个关于错误的一般术语,在此处定义:

1. **错误检测 (Error Detection)** - 确定存在错误的过程。错误由代理作为本地问题的结果发现,例如接收到坏分组,或者因为它从另一个设备接收到指示错误的分组(例如中毒分组)。

2. **错误记录 (Error Logging)** - 根据检测到的错误在架构寄存器中设置适当的位,以帮助错误处理软件。

3. **错误报告 (Error Reporting)** - 通知系统存在错误条件。这可以采用将错误消息传递到根复合体的形式,假设设备已启用发送错误消息。根复合体在接收到错误消息时可以向系统发送中断。

4. **错误信号 (Error Signaling)** - 一个代理通过发送错误消息,或发送具有 UR(Unsupported Request)或 CA(Completer Abort)状态的完成,或对 TLP 进行 Poisoning(也称为错误转发),通知另一个代理的错误条件的过程。

## **PCIe 错误报告** 

为 PCIe 定义了两个错误报告级别。第一个是所有设备所需的基线功能。这包括对旧版错误报告的支持以及对 PCIe 错误报告的基本支持。第二个是可选的高级错误报告功能,它添加了一组新的配置寄存器,并跟踪更多有关已发生错误、严重程度以及在某些情况下甚至可以记录导致错误的分组的详细信息。

## **基线错误报告** 

在所有设备中需要两组配置寄存器来支持基线错误报告。这些在第 674 页的"基线错误检测和处理"中详细描述,此处汇总如下:

- PCI 兼容寄存器 — 这些是与 PCI 使用的相同寄存器,并为现有的 PCI 兼容软件提供向后兼容性。为了使其工作,PCIe 错误映射到 PCI 兼容错误,使它们对旧版软件可见。
- PCI Express 功能寄存器 — 这些寄存器仅对了解 PCIe 的较新软件有用,但它们提供专门针对 PCIe 软件的更多错误信息。

## **高级错误报告 (AER)** 

此可选的错误报告机制包括一组新的专用配置寄存器,可为错误处理软件提供更多信息以用于诊断和恢复问题。AER 寄存器映射到扩展配置空间中,并提供有关任何错误性质的更多信息。有关这些寄存器的详细说明,请参阅第 685 页的"Advanced Error Reporting (AER)"。

## **错误类别** 

根据硬件是否能够修复问题,错误分为两大类:可纠正 (Correctable) 和不可纠正 (Uncorrectable)。不可纠正类别进一步细分为软件是否可以修复问题:非致命 (Non-fatal) 和致命 (Fatal)。

- 可纠正错误 — 由硬件自动处理 

- 不可纠正错误 

- 非致命 — 由设备特定软件处理;链路仍可操作,可以在不丢失数据的情况下恢复 

- 致命 — 由系统软件处理;链路或设备无法正常工作,并且在不丢失数据的情况下不太可能恢复 

基于这些类别,错误处理软件可以分区为单独的处理程序以执行所需的操作。此类操作的范围可能从简单地监视可纠正错误的频率到在致命错误事件中重置整个系统。无论错误类型如何,软件都可以安排通知系统所有错误,以允许跟踪和记录它们。

## **可纠正错误** 

根据定义,可纠正错误在硬件中自动纠正。它们可能会通过增加延迟和消耗带宽来影响性能,但如果一切顺利,恢复是自动且快速的,因为它不依赖于软件干预,并且在此过程中不会丢失信息。这些错误不需要报告给软件,但这样做可以允许软件跟踪可能表明某些设备显示出即将发生故障迹象的错误趋势。

## **PCI Express Technology** 

## **不可纠正错误** 

无法在硬件中自动纠正的错误称为不可纠正错误,这些错误的严重性为非致命或致命。

## **非致命的不可纠正错误** 

非致命错误表明信息已丢失,但原因可能不是链路或设备的完整性。一个分组在某处失败,但链路继续正常运行,其他分组不受影响。由于链路仍在工作,因此可能可以恢复丢失的信息,但这将依赖于特定于实现的软件来处理。此类错误的示例是完成超时,其中已发送请求但在允许的时间内未返回完成。某处存在问题,但这可能只是交换机中的随机位错误,导致完成被错误路由。对于这种情况的恢复尝试可以像重新发出请求一样简单。

## **致命的不可纠正错误**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-10"></a>
## 14.10 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

This chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process of the Link is described from Power‐On or Reset until the Link reaches fully‐operational L0 state during which normal packet traffic occurs. In addition, the Link power management states L0s, L1, L2, and L3 are discussed along with the state transi‐ tions. The Recovery state, during which bit lock, symbol lock or block lock are re‐established is described. Link speed and width change for Link bandwidth management is also discussed. 

## **This Chapter** 

Although care is always taken to minimize errors they can’t be eliminated, so detecting and reporting them is an important consideration. This chapter dis‐ cusses error types that occur in a PCIe Port or Link, how they are detected, reported, and options for handling them. Since PCIe is designed to be backward compatible with PCI error reporting, a review of the PCI approach to error han‐ dling is included as background information. Then we focus on PCIe error han‐ dling of correctable, non‐fatal and fatal errors. 

## **The Next Chapter** 

The next chapter provides an overall context for the discussion of system power management and a detailed description of PCIe power management, which is compatible with the _PCI Bus PM Interface Spec_ and the _Advanced Configuration and Power Interface_ (ACPI). PCIe defines extensions to the PCI‐PM spec that focus primarily on Link Power and event management. 

## **Background** 

Software backward compatibility with PCI is an important feature of PCIe, and that’s accomplished by retaining the PCI configuration registers that were already in place. PCI verified the correct parity on each transmission phase of the bus to check for errors. Detected errors were recorded in the Status register and could optionally be reported with either of two side‐band signals: PERR# (Parity Error) for a potentially recoverable parity fault during data transmis‐ sion, and SERR# (System Error) for a more serious problem that was usually not recoverable. These two types can be categorized as follows: 

- Ordinary data parity errors — reported via PERR# 

- Data parity errors during multi‐task transactions (special cycles) — reported via SERR# 

- Address and command parity errors — reported via SERR# 

- • Other types of errors (device‐specific) — reported via SERR# 

How the errors should be handled was outside the scope of the PCI spec and might include hardware support or device‐specific software. As an example, a data parity error on a read from memory might be recovered in hardware by detecting the condition and simply repeating the Request. That would be a safe step if the memory contents weren’t changed by the failed operation. 

As shown in Figure 15‐1 on page 649, both error pins were typically connected to the chipset and used to signal the CPU in a consumer PC. These machines were very cost sensitive, so they didn’t usually have the budget for much in the way of error handling. Consequently, the resulting error reporting signal chosen was the NMI (Non‐Maskable Interrupt) signal from the chipset to the processor that indicated significant system trouble requiring immediate attention. Most consumer PCs didn’t include an error handler for this condition, so the system would simply be stopped to avoid corruption and the BSOD (Blue Screen Of Death) would inform the operator. An example of an SERR# condition would be an address parity mismatch seen during the command phase of a transaction. This is a potentially destructive case because the wrong target might respond. If that happened and SERR# reported it, recovery would be difficult and would probably require significant software overhead. (To learn more about PCI error handling, refer to MindShare’s book _PCI System Architecture_ .) 

PCI‐X uses the same two error reporting signals but defines specific error han‐ dling requirements depending on whether device‐specific error handling soft‐ ware is present. If such a handler is not present, then all parity errors are reported with SERR#. 
## _Figure 15‐1: PCI Error Handling_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


PCI‐X 2.0 uses source‐synchronous clocking to achieve faster data rates (up to 4GB/s). This bus targeted high‐end enterprise systems because it was generally too expensive for consumer machines. Since these high‐performance systems also require high availability, the spec writers chose to improve the error han‐ dling by adding Error‐Correcting Code (ECC) support. ECC allows more robust error detection and enables correction of single‐bit errors on the fly. ECC is very helpful in minimizing the impact of transmission errors. (To learn more about PCI‐X error handling, see MindShare’s book _PCI‐X System Architecture_ .) 

PCIe maintains backward compatibility with these legacy mechanisms by using the error status bits in the legacy configuration registers to record error events in PCIe that are analogous to those of PCI. That lets legacy software see PCIe error events in terms that it understands, and allows it to operate with PCIe hardware. See “PCI‐Compatible Error Reporting Mechanisms” on page 674 for the details of these registers. 

## **PCIe Error Definitions** 

The spec uses four general terms regarding errors, defined here: 

1. **Error Detection** ‐ the process of determining that an error exists. Errors are discovered by an agent as a result of a local problem, such as receiving a bad packet, or because it received a packet signaling an error from another device (like a poisoned packet). 

2. **Error Logging** ‐ setting the appropriate bits in the architected registers based on the error detected as an aid for error‐handling software. 

3. **Error Reporting** ‐ notifying the system that an error condition exists. This can take the form of an error Message being delivered to the Root Complex, assuming the device is enabled to send error messages. The Root, in turn, can send an interrupt to the system when it receives an error Message. 

4. **Error Signaling** ‐ the process of one agent notifying another of an error con‐ dition by sending an error Message, or sending a Completion with a UR (Unsupported Request) or CA (Completer Abort) status, or poisoning a TLP (also known as error forwarding). 

## **PCIe Error Reporting** 

Two error reporting levels are defined for PCIe. The first is a Baseline capability required for all devices. This includes support for legacy error reporting as well as basic support for reporting PCIe errors. The second is an optional Advanced Error Reporting Capability that adds a new set of configuration registers and tracks many more details about which errors have occurred, how serious they are and in some cases, can even record information about the packet that caused the error. 

## **Baseline Error Reporting** 

Two sets of configuration registers are required in all devices in support of Baseline error reporting. These are described in detail in “Baseline Error Detec‐ tion and Handling” on page 674 and are summarized here: 

- PCI‐compatible Registers — these are the same registers used by PCI and provide backward compatibility for existing PCI‐compatible software. To make this work, PCIe errors are mapped to PCI‐compatible errors, making them visible to the legacy software. 
- PCI Express Capability Registers — these registers will only be useful to newer software that is aware of PCIe, but they provide more error information specifically for PCIe software. 

## **Advanced Error Reporting (AER)** 

This optional error reporting mechanism includes a new and dedicated set of configuration registers that give error handling software more information to work with in diagnosing and recovering from problems. The AER registers are mapped into the extended configuration space and provide much more infor‐ mation about the nature of any errors. See “Advanced Error Reporting (AER)” on page 685 for a detailed description of these registers. 

## **Error Classes** 

Errors fall into two general categories based on whether hardware is able to fix the problem or not, Correctable and Uncorrectable. The Uncorrectable category is further subdivided based on whether software can fix the problem, Non‐fatal and Fatal. 

- Correctable errors — automatically handled by hardware 

- Uncorrectable errors 

- Non‐fatal — handled by device‐specific software; Link is still operational and recovery without data loss may be possible 

- Fatal — handled by system software; Link or Device is not working prop‐ erly and recovery without data loss is unlikely 

Based on these classes, error handling software can be partitioned into separate handlers to perform the actions required. Such actions might range from simply monitoring the frequency of Correctable errors to resetting the entire system in the event of a Fatal error. Regardless of the type of error, software may arrange for the system to be notified of all errors to allow tracking and logging them. 

## **Correctable Errors** 

Correctable errors are, by definition, automatically corrected in hardware. They may impact performance by adding latency and consuming bandwidth, but if all goes well, recovery is automatic and fast because it doesn’t depend on soft‐ ware intervention, and no information is lost in the process. These errors aren’t 

required to be reported to software, but doing so could allow software to track error trends that might indicate that some devices are showing signs of immi‐ nent failure. 

## **Uncorrectable Errors** 

Errors that can’t be automatically corrected in hardware are called Uncorrect‐ able, and these are either Non‐fatal or Fatal in severity. 

## **Non-fatal Uncorrectable Errors** 

Non‐fatal errors indicate that information has been lost but the cause was likely something other than the integrity of a Link or Device. A packet failed some‐ where, but the Link continues to function correctly and other packets are unaf‐ fected. Since the Link is still working, recovery of the lost information may be possible, but will depend on implementation‐specific software to handle it. An example of this error type would be a Completion timeout, in which a Request was sent but no Completion was returned within the allowed time. Somewhere there was an issue, but it could be something as simple as a random bit error within a Switch that caused the Completion to be routed incorrectly. An attempt at recovery for this case could be as simple as re‐issuing the Request. 

## **Fatal Uncorrectable Errors**

</td>
<td style="background-color:#e8e8e8">

致命错误表明链路或设备已发生操作故障,导致不太可能恢复的数据丢失。对于这些情况,至少重置失败的链路或设备可能是任何恢复过程中的第一步,因为它显然由于某种原因无法运行。规范还邀请特定于实现的方法,其中软件可以尝试限制故障的影响,但它没有定义应采取的任何特定操作。此类错误的示例是接收器缓冲区溢出,在这种情况下,由于流控制跟踪计数器彼此不同步而丢失了信息。由于没有机制可以解决此问题,因此通常需要重置此链路。

## **PCIe 错误检查机制** 

PCIe 错误检查的范围集中在与链路和分组传送相关的错误上,如图 15-2(第 653 页)所示。与链路传输无关的错误不通过 PCIe 错误处理机制报告,需要专有方法来报告它们,例如设备特定
中断。接口的每一层都包括错误检查功能,这些将在以下部分中汇总。

_Figure 15-2: PCI Express 错误检查和报告的范围_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **CRC** 

在深入研究与层相关的错误处理之前,首先讨论 CRC(循环冗余校验)的概念会有所帮助,因为它是 PCIe 错误检查的组成部分。CRC 代码由发送器根据分组内容计算,并将其添加到分组中以进行传输。CRC 名称源自以下事实:此 _check_ 代码(从分组计算以检查错误)是 _redundant_(不向分组添加信息),并且源自 _cyclic_ 代码。虽然 CRC 不提供足够的信息来执行像 ECC(纠错码)那样的自动纠错,但它确实提供了强大的错误检测功能。CRC 也常用于串行传输中,因为它们擅长检测一串不正确的位。

## **PCI Express Technology** 

CRC 在 PCIe 中有两种不同的使用情况。第一种是强制的 LCRC(Link CRC),在数据链路层 (Data Link Layer) 中为跨链路的每个 TLP 生成和检查。它旨在检测链路上的传输错误。

第二个是可选的 ECRC(端到端 CRC),它在发送方的事务层 (Transaction Layer) 中生成,并在分组的最终目标的事务层中进行检查。这旨在检测可能以其他方式保持静默的错误,例如当 TLP 通过像交换机这样的中间代理时,如图 15-3(第 654 页)所示。在此图示中,分组已安全到达交换机的下游端口,但当它在交换机内被存储或处理时发生位错误。LCRC 仅在链路上保护 TLP。一旦入口端口的数据链路层检查 LCRC,它就会将其从分组中删除,因为将在出口端口重新计算新的 LCRC(将包括新的序列号)。这意味着分组在交换机内未受保护。这就是拥有 ECRC 的目的。它在原始设备处计算,并且不被中间设备删除或重新计算。因此,如果目标设备正在检查 ECRC 并看到不匹配,则沿途中必定发生错误,即使没有看到 LCRC 错误。请注意,使用 ECRC 需要存在可选的高级错误报告寄存器,因为它们包含启用此功能的位。

_Figure 15-3: ECRC 使用示例_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

## **按层的错误检查** 

传入分组的不同方面在接收器的不同层进行检查。某些错误检查被列为可选的。对于这些情况,如果错误发生但设计者选择不实现该形式的检查,则不会检测到它。

## **物理层错误** 

到达接收器的分组首先到达物理层。在此级别必须检查一些事情,而其他一些可以可选地检查。链路训练也发生在该层,并且在该过程中可能出现各种问题,但这些问题以及物理层的其他详细信息在第 505 页的第 14 章"链路初始化和训练"中介绍。总之,物理层错误(也称为接收器错误或链路错误)包括以下情况:

- 使用 8b/10b 时,检查解码违规(检查必需) 

- 帧违规(对于 8b/10b 为可选,对于 128b/130b 为必需) 

- 弹性缓冲区错误(检查可选) 

- 丢失符号锁或 Lane 去偏移(检查可选) 

如果在检测到接收器错误时 TLP 正在进行中,则会丢弃它。为了解决错误,如果尚未挂起,则向数据链路层发出信号以发送 NAK。

## **数据链路层错误** 

在物理层之后,传入分组接下来进入数据链路层,在那里检查几个可能的问题。这些条件的详细信息可以在第 317 页的第 10 章"Ack/Nak 协议"中找到。总之,错误是:

- TLP 的 LCRC 失败 

- TLP 的序列号违规 

- DLLP 的 16 位 CRC 失败 

- 链路层协议错误 

与物理层一样,如果在看到错误时 TLP 正在进行中,则会丢弃该 TLP,如果尚未挂起,则会安排 NAK。

发送器处也有一些数据链路层错误需要注意,包括 REPLAY_TIMER 过期和 REPLAY_NUM 计数器翻转。通过重放重放缓冲区的内容来处理超时,

## **PCI Express Technology** 

并增加 REPLAY_NUM 计数器。每当发送器接收到指示已取得前进的 ACK 或 NAK时(意味着它导致从重放缓冲区中清除一个或多个 TLP),定时器和计数器就会被重置。但是,如果未足够快地接收到 Ack 或 Nak,则将看到超时条件,这将导致重放。

## **事务层错误** 

最后,如果传入的 TLP 通过物理层和数据链路层中的所有检查,则它们最终将到达事务层,在那里检查:

- ECRC 失败(检查可选) 

- 格式错误的 TLP(分组格式中的错误) 

- 流控制协议违规 

- 不受支持的请求 

- 数据损坏(中毒分组) 

- 完成者中止(检查可选) 

- 接收器溢出(检查可选) 

与数据链路层一样,发送器事务层也有一些错误检查,例如:

- 完成超时 

- 意外完成(完成与挂起的请求不匹配) 

## **错误污染** 

如果设备对同一事务看到多个问题,则可能会出现问题。这可能导致报告多个错误(称为"错误污染")。为避免这种情况,报告的错误仅限于最显著的一个。例如,如果 TLP 在物理层具有接收器错误,则肯定会在数据链路层和事务层中发现错误,但报告所有错误只会增加混乱。最相关的是报告看到的第一错误。因此,如果在物理层中看到错误,则没有理由将分组转发到更高层。类似地,如果在数据链路层中看到错误,则不会将分组转发到事务层。一个级别的违规分组不会转发到下一个级别,而是被丢弃。

尽管如此,对于同一分组在事务层可能会看到多个错误。应仅按规范定义的优先级顺序报告最显著的一个。事务层错误优先级从最高到最低为:
- 不可纠正的内部错误 

- 接收器缓冲区溢出 

- 流控制协议错误 

- ECRC 检查失败 

- 格式错误的 TLP 

- AtomicOp Egress Blocked 

- TLP Prefix Blocked 

- ACS(访问控制服务)违规 

- MC(多播)阻止的 TLP 

- UR(不受支持的请求)、CA(完成者中止)或意外完成 

- 接收到中毒的 TLP 

例如,TLP 可能由于标头损坏而遇到 ECRC 故障。由于分组内的某些内容已损坏,因此它也可能被视为格式错误或可能是不受支持的请求。ECRC 故障是最高优先级,因为它意味着标头内容可能已损坏,因此,报告依赖于这些内容的错误毫无意义。

## **PCI Express 错误的来源** 

而不是单独考虑所有错误条件,有助于将它们分组到公共区域。

## **ECRC 生成和检查** 

如前所述,ECRC 生成和检查需要存在可选的高级错误报告配置寄存器结构,如图 15-4(第 658 页)所示。配置软件检查此功能寄存器以确定 Function 中是否支持 ECRC。如果是,则对错误功能和控制寄存器的写入可用于启用它。

## **PCI Express Technology** 

_Figure 15-4: 错误相关配置寄存器的位置_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


启用了生成 ECRC 的设备会发起 TLP(请求或完成),根据分组的标头和数据部分计算 32 位 ECRC,并将其添加到分组的末尾。ECRC 被称为"端到端",因为其意图是它将在 TLP 的源处生成,并且永远不会被路径上的任何中间设备剥离或重新生成。路径中原始设备和接收设备之间的交换机允许检查和报告 ECRC 错误,但不是必需的。无论是否存在错误,交换机仍必须原样转发分组,以便最终目标设备可以评估 ECRC 并采取适当的步骤。如果交换机充当 TLP 的发起者或接收者,则它可以像普通设备一样参与 ECRC 生成和检查。有关交换机如何允许报告此类错误的更多信息,请参阅第 670 页的"Advisory Non-Fatal Errors"。
## **TLP Digest** 

如果启用了可选的 ECRC 功能,则在标头中设置一个称为 TD(TLP Digest)的特殊位,以指示它存在于分组的末尾(ECCRC 也称为 Digest)。分组标头中的 TD 位如图 15-5(第 659 页)所示。规范强调,在转发 TLP 时必须特别小心地处理此位,因为如果缺少它但存在 ECRC,反之亦然,则分组将被视为格式错误。

_Figure 15-5: 完成标头中的 TLP Digest 位_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **不包含在 ECRC 机制中的可变位** 

ECRC 是根据标头和数据的内容计算的。由于这些内容预计不会更改,因此在接收器处执行检查时,结果应相同。然而,事实证明,在分组传输过程中,两个标头位可以合法地更改:Type 字段的位 0 和 EP 位。Type 字段的位 0 可以在配置请求中更改,原因很简单,即在到达目标总线之前,请求将是 Type 1,然后将变为 Type 0。这涉及更改 Type 字段的位 0。如果中间设备检测到数据错误,EP 位也可以被合法地更改。例如,如果交换机转发 TLP,但它遭受某种内部错误导致数据损坏,则在通过出口端口传出时设置 EP 位是报告错误的一种方式(称为错误转发或数据中毒)。

由于这两个位可以在分组传输过程中更改,因此它们被称为"可变位",不能用于 ECRC 的生成或检查。相反,它们的值在 ECRC 生成和检查中始终假定为 1b,而不是使用实际值。这样,ECRC 不依赖于它们,并且将被正确地评估。

## **PCI Express Technology** 

检测到 ECRC 错误时所采取的操作超出规范的范围,但可能的选项将取决于错误是在请求中还是在完成中找到。

- **请求中的 ECRC** — 检测到 ECRC 错误的完成者必须设置 ECRC 错误状态位。它们也可以选择不为该请求返回完成,导致请求者的完成超时,请求者的软件可能选择重新调度该请求。

- **完成中的 ECRC** — 检测到 ECRC 错误的请求者必须设置 ECRC 错误状态位。除了标准错误报告机制之外,它们还可以选择使用特定于功能的中断将错误报告给它们的设备驱动程序。与之前一样,软件可能决定重新安排失败的请求。

在任何一种情况下,可能会将不可纠正的非致命错误消息发送到系统。如果是这样,则可能会访问设备驱动程序以检查 _Uncorrectable Error Status Register_ 中的状态位并了解错误的性质。如果可能,可以重新调度失败的请求,但可能需要其他步骤。

## **数据中毒** 

数据中毒,也称为错误转发,提供了一种可选方式让设备指示与 TLP 关联的数据已损坏。在这些情况下,分组标头中的 EP(Error Poisoned)位被设置以指示错误。EP 位如图 15-6(第 660 页)所示。

_Figure 15-6: 完成标头中的错误/中毒位_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

每当传输数据时,例如在写请求或带数据的完成中,这些数据的损坏可能会发生,这需要报告给目标设备。在每种情况下,分组都可以转发给接收者,但通过标头中的 EP 位标记为具有坏数据。细心的读者可能想知道为什么人们可能想要发送已知为坏的数据。碰巧的是,有些情况下这是有用的:

1. 如果请求导致返回带数据的完成,但该数据在从目标收集时遇到错误(例如内存中的奇偶校验或 ECC 失败),那么报告它的最佳方式是什么?一种方法是不发送完成,但是如果错误不以其他方式报告,则系统仅在请求者处看到完成超时。该响应没有多大帮助,因为任何数量的问题都可能导致该结果。

 - 另一方面,如果以设置中毒位的方式传送完成,则至少请求者可以看到到完成者的往返路径必须正确工作。因此,问题一定发生在完成者内部,或者在路径中的交换机中。将采取什么步骤将是特定于实现的,但比简单地完成超时更清楚地知道出了什么问题。

2. 它可用于报告中间问题。如果数据有效负载在通过交换机时被损坏,则仍可以转发分组并设置 EP 位以指示问题。

3. 目标设备可能可以接受有错误的数据。例如,音频输出设备需要接收及时的数据流才能正常工作。如果传入数据有错误,则后果很小(音频输出中的毛刺),并且恢复时间将足够长以引起明显的延迟,因此可以按原样接受数据,而不是尝试恢复数据。

4. 目标设备可能具有纠正数据的手段。数据可能可以直接恢复,或者目标可能具有重新创建其部分的方法,或者具有解决该问题的某种其他方法。

规范规定,数据中毒仅适用于与分组关联的数据有效负载(例如内存、配置或 I/O 写入和完成),而从不适用于 TLP 标头的内容。因此,如果接收器看到没有有效负载的中毒分组(EP=1)(例如中毒的内存读取),则其行为未定义。只能在设备的事务层执行中毒;数据链路层不检查或影响 TLP 标头的内容。

错误转发支持被声明为发送器可选的,并且对于接收器缺少这样的声明暗示它不是可选的。

## **PCI Express Technology** 

如果发送器支持它,则使用旧版 Command 寄存器中的 Parity Error Response 位启用它。这是因为中毒分组大致类似于 PCI 中的奇偶校验错误,因为 PCI 以这种方式报告坏数据。如果启用,接收到中毒分组可以通过错误消息报告给系统,并且如果存在可选的高级错误报告寄存器,也将设置 Poisoned TLP 状态位。

可以预期,不允许对控制位置的中毒写入修改目标中的内容。规范中给出的示例是配置写入、对控制寄存器的 IO 或内存写入以及 AtomicOp。接收到中毒分组的交换机必须将它们不变地转发到目标端口,尽管如果它们已启用,则必须将此分组报告为错误,以帮助软件确定错误发生的位置。接收到中毒的非发布请求的完成者预期将返回具有 UR(Unsupported Request)状态的完成。

## **拆分事务错误** 

在与非发布请求相关联的拆分事务期间可能发生各种故障。PCIe 在完成标头中定义了一个状态字段,允许完成者将某些错误报告回请求者。图 15-7(第 662 页)说明了该字段在完成标头中的位置,表 15-1(第 663 页)给出了可能的值。如表所示,仅定义了四种编码,其中两种表示错误情况。

_Figure 15-7: 完成标头内的完成状态字段_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

_Table 15-1: 完成代码和描述_ 

|**状态代码**|**完成状态定义**|
|---|---|
|000b|成功完成 (SC)|
|001b|不受支持的请求 (UR) - 错误|
|010b|配置请求重试状态 (CRS)|
|011b|完成者中止 (CA) - 错误|
|100b - 111b|保留|


## **不受支持的请求 (UR) 状态** 

如果接收器不支持请求,则返回具有 UR 状态的完成。规范定义了许多可能导致 UR 状态的条件。一些示例是:

- 不支持请求类型(示例:对原生端点的 IO 请求或对原生端点的 MRdLk) 

- 带有不受支持或未定义消息代码的消息 

- 请求未引用映射到设备的地址空间 

- 请求地址未映射到交换机端口的地址范围内 

- 中毒写请求(EP=1)以完成者中的 I/O 或内存映射控制空间为目标。此类请求不得被允许修改该位置,而是由完成者丢弃并以具有 UR 状态的完成进行报告。

- 下游根或交换机端口接收到针对其辅助总线上不存在的设备的配置请求(例如,具有非零设备号的设备,除非启用 ARI)。该端口必须终止请求并返回具有 UR 状态的完成,因为下游设备号需要为零(除非启用 ARI,替代路由 ID 解释)。

- 在端点处接收到 Type 1 配置请求。 

- 使用保留的完成状态字段编码的完成必须解释为 UR。 

- 处于 D1、D2 或 D3hot 电源管理状态下的 Function 接收到除配置请求或消息之外的请求。 

- 标头中未设置 No Snoop 位的 TLP 被路由到其 VC Resource Capability 寄存器中设置了 Reject Snoop Transactions 位的端口。 

## **PCI Express Technology** 

## **完成者中止 (CA) 状态** 

可能发生多种情况,导致完成者将 CA 状态返回给请求者。一些示例是:

- 完成者收到无法在不违反其编程规则的情况下完成的请求。例如,某些 Function 可能被设计为仅允许以完整和对齐的方式访问某些寄存器(例如,4 字节寄存器可能需要 4 字节对齐访问)。以部分或未对齐方式访问其中一个寄存器的任何尝试(例如,仅读取 4 字节寄存器的两个字节)将失败。此类限制不是违反规范,而是与该 Function 的编程接口相关的合法约束。访问此类 Function 基于设备驱动程序了解如何访问其 Function 的期望。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-11"></a>
## 14.11 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Fatal errors indicate that a Link or Device has had an operational failure, caus‐ ing data loss that is unlikely to be recovered. For these cases, resetting at least the failed Link or Device will probably be the first step in any recovery process because it’s clearly not operational for some reason. The spec also invites imple‐ mentation‐specific approaches, in which software may attempt to limit the effects of the failure, but it doesn’t define any particular actions that should be taken. An example of this type of error would be a receiver buffer overflow, in which case information has been lost because flow control tracking counters have gotten out of sync with each other. Since there’s no mechanism to fix this, a reset of this Link will usually be required. 

## **PCIe Error Checking Mechanisms** 

The scope of PCIe error checking focuses on errors associated with the Link and packet delivery, as shown in Figure 15‐2 on page 653. Errors that don’t pertain to Link transmission are not reported through PCIe error‐handling mechanisms and would need proprietary methods to report them, such as device‐specific 
interrupts. Each layer of the interface includes error checking capabilities, and these are summarized in the sections that follow. 

_Figure 15‐2: Scope of PCI Express Error Checking and Reporting_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **CRC** 

Before diving into error handling as it relates to the layers, it will help to first discuss the concept of CRC (Cyclic Redundancy Check) because it’s an integral part of PCIe error checking. A CRC code is calculated by the transmitter based on the contents of the packet and adds it to the packet for transmission. The CRC name is derived from the fact that this _check_ code (calculated from the packet to check for errors) is _redundant_ (adds no information to the packet), and is derived from _cyclic_ codes. Although a CRC doesn’t supply enough information to do automatic error correction the way ECC (Error Correcting Code) can, it does provide robust error detection. CRCs are also commonly used in serial transports because they’re good at detecting a string of incorrect bits. 

## **PCI Express Technology** 

CRCs have two different usage cases in PCIe. One is the mandatory LCRC (Link CRC) generated and checked in the Data Link Layer for every TLP that goes across a Link. It’s intended to detect transmission errors on the Link. 

The second is the optional ECRC (End‐to‐end CRC) that’s generated in the Transaction Layer of the sender and checked in the Transaction Layer of the ulti‐ mate target of the packet. This is intended to detect errors that might otherwise be silent, such as when a TLP passes through an intermediate agent like a Switch, as shown in Figure 15‐3 on page 654. In this illustration, the packet arrived safely on the downstream port of the Switch but while it was being stored or processed within the Switch a bit error occurred. The LCRC only pro‐ tects TLPs while on the Link. Once the Data Link Layer of the Ingress Port checks the LCRC, it removes it from the packet because a new LCRC will be cal‐ culated (which will include the new Sequence Number) at the Egress Port. This means that the packet is unprotected while inside the Switch. This is the pur‐ pose of having an ECRC. It is calculated at the originating device and is not removed or recalculated by intermediate devices. So if the target device is checking the ECRC and sees a mismatch, then there must have been an error somewhere along the way even though no LCRC error was seen. Note that using the ECRC requires the presence of the optional Advanced Error Report‐ ing registers, since they contain the bits to enable this functionality. 

_Figure 15‐3: ECRC Usage Example_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

## **Error Checks by Layer** 

Different aspects of an incoming packet are checked in the different layers at the Receiver. Some error checking is listed as optional. For those cases, if the error occurs but the designer has chosen not to implement that form of checking, it will not be detected. 

## **Physical Layer Errors** 

A packet arriving at the Receiver arrives at the Physical Layer first. There are a few things that must be checked at this level and others that may optionally be checked. Link training also takes place at this layer, and a variety of problems may arise during that process but those and other details of the Physical Layer are covered in Chapter 14, entitled ʺLink Initialization & Training,ʺ on page 505. In summary, though, Physical Layer errors, also called Receiver Errors or Link Errors, include the following cases: 

- When using 8b/10b, checking for decode violations (checking required) 

- Framing violations (optional for 8b/10b, required for 128b/130b) 

- Elastic buffer errors (checking optional) 

- Loss of symbol lock or Lane deskew (checking optional) 

If a TLP was in progress when a Receiver Error was detected, it is discarded. To resolve the error, the Data Link Layer is signaled to send a NAK if one isn’t already pending. 

## **Data Link Layer Errors** 

After the Physical Layer, incoming packets go next into the Data Link Layer, where they are checked for several possible problems. The details of these con‐ ditions can be found in Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317. In summary, the errors are: 

- LCRC failure for TLPs 

- Sequence Number violation for TLPs 

- 16‐bit CRC failure for DLLPs 

- Link Layer Protocol errors 

As with the Physical Layer, if a TLP was in progress when an error is seen, the TLP is discarded and a NAK is scheduled if one isn’t already pending. 

There are some Data Link Layer errors to watch for at the transmitter, too, including REPLAY_TIMER expiring and the REPLAY_NUM counter rolling over. A timeout is handled by replaying the contents of the Replay Buffer and 

incrementing the REPLAY_NUM counter. The timer and counter are reset whenever an ACK or NAK arrives at the transmitter that indicates forward progress has been made (meaning it results in clearing one or more TLPs from the Replay Buffer). But if an Ack or Nak isn’t received quickly enough, the time‐ out condition is seen which will result in a replay. 

## **Transaction Layer Errors** 

Lastly, if incoming TLPs pass all the checks at the Physical and Data Link Lay‐ ers, they will finally reach the Transaction Layer, where they are checked for: 

- ECRC failure (checking optional) 

- Malformed TLP (error in packet format) 

- Flow Control Protocol violation 

- Unsupported Requests 

- Data Corruption (poisoned packet) 

- Completer Abort (checking optional) 

- Receiver Overflow (checking optional) 

As with the Data Link Layer, there are some error checks at the transmitter Transaction Layer, too, such as: 

- Completion Timeouts 

- Unexpected Completion (Completion does not match pending Request) 

## **Error Pollution** 

A problem can arise if a device sees several problems for the same transaction. This could result in several errors getting reported (referred to as “Error Pollu‐ tion”). To avoid this, reported errors are limited to only the most significant one. For example, if a TLP has a Receiver Error at the Physical Layer, it would certainly be found to have errors at the Data Link Layer and Transaction Layers, too, but reporting them all would just add confusion. What is most relevant is reporting the first error that was seen. Consequently, if an error is seen in the Physical Layer, there’s no reason to forward the packet to the higher layers. Similarly, if an error is seen in the Data Link Layer, then the packet won’t be for‐ warded to the Transaction Layer. Offending packets at one level are not for‐ warded to the next level but are dropped. 

Still, multiple errors may be seen for the same packet at the Transaction Layer. Only the most significant one should be reported in the order of priority as defined by the spec. Transaction Layer error priority from highest to lowest is: 
- Uncorrectable Internal Error 

- Receiver Buffer Overflow 

- Flow Control Protocol Error 

- ECRC Check Failed 

- Malformed TLP 

- AtomicOp Egress Blocked 

- TLP Prefix Blocked 

- ACS (Access Control Services) Violation 

- MC (Multi‐cast) Blocked TLP 

- UR (Unsupported Request), CA (Completer Abort), or Unexpected Com‐ pletion 

- Poisoned TLP Received 

As an example, a TLP might experience an ECRC fault caused by a corrupted header. Since something was corrupted within the packet, it might also be seen as Malformed or possibly as an Unsupported Request. The ECRC fault is the highest priority, since it means that the header contents may have been cor‐ rupted, and due to this, there is no point in reporting errors that depend on those contents. 

## **Sources of PCI Express Errors** 

Rather than consider all of the error conditions individually, it will be helpful to group them into common areas. 

## **ECRC Generation and Checking** 

As mentioned earlier, ECRC generation and checking requires the optional Advanced Error Reporting configuration register structure to be present, as shown in Figure 15‐4 on page 658. Configuration software checks for this capa‐ bility register to determine whether ECRCs are supported in a Function. If it is, a write to the Error Capability and Control register can be used to enable it. 

_Figure 15‐4: Location of Error‐Related Configuration Registers_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


A device enabled to generate ECRCs originates a TLP (Request or Completion), computes the 32‐bit ECRC based on the header and data portions of the packet and adds it to the end of the packet. The ECRC is called “end‐to‐end” because the intent is that it will be generated at the TLP’s origin and never stripped off or regenerated by any intermediate device along its path. Switches in the path between the originating and receiving devices are allowed to check and report ECRC errors but aren’t required to do so. Whether or not there is an error, a Switch must still forward the packet unaltered so that the ultimate target device can evaluate the ECRC and take appropriate steps. If a Switch is acting as the originator or recipient of the TLP it can participate like an ordinary device in ECRC generation and checking. For more on the topic of how a Switch is allowed to report such errors, see “Advisory Non‐Fatal Errors” on page 670. 
## **TLP Digest**

</td>
<td style="background-color:#e8e8e8">

致命错误表明链路或设备已发生操作故障,导致不太可能恢复的数据丢失。对于这些情况,至少重置失败的链路或设备可能是任何恢复过程中的第一步,因为它显然由于某种原因无法运行。规范还邀请特定于实现的方法,其中软件可以尝试限制故障的影响,但它没有定义应采取的任何特定操作。此类错误的示例是接收器缓冲区溢出,在这种情况下,由于流控制跟踪计数器彼此不同步而丢失了信息。由于没有机制可以解决此问题,因此通常需要重置此链路。

## **PCIe 错误检查机制** 

PCIe 错误检查的范围集中在与链路和分组传送相关的错误上,如图 15-2(第 653 页)所示。与链路传输无关的错误不通过 PCIe 错误处理机制报告,需要专有方法来报告它们,例如设备特定
中断。接口的每一层都包括错误检查功能,这些将在以下部分中汇总。

_Figure 15-2: PCI Express 错误检查和报告的范围_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **CRC** 

在深入研究与层相关的错误处理之前,首先讨论 CRC(循环冗余校验)的概念会有所帮助,因为它是 PCIe 错误检查的组成部分。CRC 代码由发送器根据分组内容计算,并将其添加到分组中以进行传输。CRC 名称源自以下事实:此 _check_ 代码(从分组计算以检查错误)是 _redundant_(不向分组添加信息),并且源自 _cyclic_ 代码。虽然 CRC 不提供足够的信息来执行像 ECC(纠错码)那样的自动纠错,但它确实提供了强大的错误检测功能。CRC 也常用于串行传输中,因为它们擅长检测一串不正确的位。

## **PCI Express Technology** 

CRC 在 PCIe 中有两种不同的使用情况。第一种是强制的 LCRC(Link CRC),在数据链路层为跨链路的每个 TLP 生成和检查。它旨在检测链路上的传输错误。

第二个是可选的 ECRC(端到端 CRC),它在发送方的事务层生成,并在分组的最终目标的事务层中进行检查。这旨在检测可能以其他方式保持静默的错误,例如当 TLP 通过像交换机这样的中间代理时,如图 15-3(第 654 页)所示。在此图示中,分组已安全到达交换机的下游端口,但当它在交换机内被存储或处理时发生位错误。LCRC 仅在链路上保护 TLP。一旦入口端口的数据链路层检查 LCRC,它就会将其从分组中删除,因为将在出口端口重新计算新的 LCRC(将包括新的序列号)。这意味着分组在交换机内未受保护。这就是拥有 ECRC 的目的。它在原始设备处计算,并且不被中间设备删除或重新计算。因此,如果目标设备正在检查 ECRC 并看到不匹配,则沿途中必定发生错误,即使没有看到 LCRC 错误。请注意,使用 ECRC 需要存在可选的高级错误报告寄存器,因为它们包含启用此功能的位。

_Figure 15-3: ECRC 使用示例_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

## **按层的错误检查** 

传入分组的不同方面在接收器的不同层进行检查。某些错误检查被列为可选的。对于这些情况,如果错误发生但设计者选择不实现该形式的检查,则不会检测到它。

## **物理层错误** 

到达接收器的分组首先到达物理层。在此级别必须检查一些事情,而其他一些可以可选地检查。链路训练也发生在该层,并且在该过程中可能出现各种问题,但这些问题以及物理层的其他详细信息在第 505 页的第 14 章"链路初始化和训练"中介绍。总之,物理层错误(也称为接收器错误或链路错误)包括以下情况:

- 使用 8b/10b 时,检查解码违规(检查必需) 

- 帧违规(对于 8b/10b 为可选,对于 128b/130b 为必需) 

- 弹性缓冲区错误(检查可选) 

- 丢失符号锁或 Lane 去偏移(检查可选) 

如果在检测到接收器错误时 TLP 正在进行中,则会丢弃它。为了解决错误,如果尚未挂起,则向数据链路层发出信号以发送 NAK。

## **数据链路层错误** 

在物理层之后,传入分组接下来进入数据链路层,在那里检查几个可能的问题。这些条件的详细信息可以在第 317 页的第 10 章"Ack/Nak 协议"中找到。总之,错误是:

- TLP 的 LCRC 失败 

- TLP 的序列号违规 

- DLLP 的 16 位 CRC 失败 

- 链路层协议错误 

与物理层一样,如果在看到错误时 TLP 正在进行中,则会丢弃该 TLP,如果尚未挂起,则会安排 NAK。

发送器处也有一些数据链路层错误需要注意,包括 REPLAY_TIMER 过期和 REPLAY_NUM 计数器翻转。通过重放重放缓冲区的内容来处理超时,

## **PCI Express Technology** 

并增加 REPLAY_NUM 计数器。每当发送器接收到指示已取得前进的 ACK 或 NAK 时(意味着它导致从重放缓冲区中清除一个或多个 TLP),定时器和计数器就会被重置。但是,如果未足够快地接收到 Ack 或 Nak,则将看到超时条件,这将导致重放。

## **事务层错误** 

最后,如果传入的 TLP 通过物理层和数据链路层中的所有检查,则它们最终将到达事务层,在那里检查:

- ECRC 失败(检查可选) 

- 格式错误的 TLP(分组格式中的错误) 

- 流控制协议违规 

- 不受支持的请求 

- 数据损坏(中毒分组) 

- 完成者中止(检查可选) 

- 接收器溢出(检查可选) 

与数据链路层一样,发送器事务层也有一些错误检查,例如:

- 完成超时 

- 意外完成(完成与挂起的请求不匹配) 

## **错误污染** 

如果设备对同一事务看到多个问题,则可能会出现问题。这可能导致报告多个错误(称为"错误污染")。为避免这种情况,报告的错误仅限于最显著的一个。例如,如果 TLP 在物理层具有接收器错误,则肯定会在数据链路层和事务层中发现错误,但报告所有错误只会增加混乱。最相关的是报告看到的第一错误。因此,如果在物理层中看到错误,则没有理由将分组转发到更高层。类似地,如果在数据链路层中看到错误,则不会将分组转发到事务层。一个级别的违规分组不会转发到下一个级别,而是被丢弃。

尽管如此,对于同一分组在事务层可能会看到多个错误。应仅按规范定义的优先级顺序报告最显著的一个。事务层错误优先级从最高到最低为:
- 不可纠正的内部错误 

- 接收器缓冲区溢出 

- 流控制协议错误 

- ECRC 检查失败 

- 格式错误的 TLP 

- AtomicOp Egress Blocked 

- TLP Prefix Blocked 

- ACS(访问控制服务)违规 

- MC(多播)阻止的 TLP 

- UR(不受支持的请求)、CA(完成者中止)或意外完成 

- 接收到中毒的 TLP 

例如,TLP 可能由于标头损坏而遇到 ECRC 故障。由于分组内的某些内容已损坏,因此它也可能被视为格式错误或可能是不受支持的请求。ECRC 故障是最高优先级,因为它意味着标头内容可能已损坏,因此,报告依赖于这些内容的错误毫无意义。

## **PCI Express 错误的来源** 

而不是单独考虑所有错误条件,有助于将它们分组到公共区域。

## **ECRC 生成和检查** 

如前所述,ECRC 生成和检查需要存在可选的高级错误报告配置寄存器结构,如图 15-4(第 658 页)所示。配置软件检查此功能寄存器以确定 Function 中是否支持 ECRC。如果是,则对错误功能和控制寄存器的写入可用于启用它。

## **PCI Express Technology** 

_Figure 15-4: 错误相关配置寄存器的位置_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


启用了生成 ECRC 的设备会发起 TLP(请求或完成),根据分组的标头和数据部分计算 32 位 ECRC,并将其添加到分组的末尾。ECRC 被称为"端到端",因为其意图是它将在 TLP 的源处生成,并且永远不会被路径上的任何中间设备剥离或重新生成。路径中原始设备和接收设备之间的交换机允许检查和报告 ECRC 错误,但不是必需的。无论是否存在错误,交换机仍必须原样转发分组,以便最终目标设备可以评估 ECRC 并采取适当的步骤。如果交换机充当 TLP 的发起者或接收者,则它可以像普通设备一样参与 ECRC 生成和检查。有关交换机如何允许报告此类错误的更多信息,请参阅第 670 页的"Advisory Non-Fatal Errors"。
## **TLP Digest** 

如果启用了可选的 ECRC 功能,则在标头中设置一个称为 TD(TLP Digest)的特殊位,以指示它存在于分组的末尾(ECRC 也称为 Digest)。分组标头中的 TD 位如图 15-5(第 659 页)所示。规范强调,在转发 TLP 时必须特别小心地处理此位,因为如果缺少它但存在 ECRC,反之亦然,则分组将被视为格式错误。

_Figure 15-5: 完成标头中的 TLP Digest 位_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **不包含在 ECRC 机制中的可变位** 

ECRC 是根据标头和数据的内容计算的。由于这些内容预计不会更改,因此在接收器处执行检查时,结果应相同。然而,事实证明,在分组传输过程中,两个标头位可以合法地更改:Type 字段的位 0 和 EP 位。Type 字段的位 0 可以在配置请求中更改,原因很简单,即在到达目标总线之前,请求将是 Type 1,然后将变为 Type 0。这涉及更改 Type 字段的位 0。如果中间设备检测到数据错误,EP 位也可以被合法地更改。例如,如果交换机转发 TLP,但它遭受某种内部错误导致数据损坏,则在通过出口端口传出时设置 EP 位是报告错误的一种方式(称为错误转发或数据中毒)。

由于这两个位可以在分组传输过程中更改,因此它们被称为"可变位",不能用于 ECRC 的生成或检查。相反,它们的值在 ECRC 生成和检查中始终假定为 1b,而不是使用实际值。这样,ECRC 不依赖于它们,并且将被正确地评估。

## **PCI Express Technology** 

检测到 ECRC 错误时所采取的操作超出规范的范围,但可能的选项将取决于错误是在请求中还是在完成中找到。

- **请求中的 ECRC** — 检测到 ECRC 错误的完成者必须设置 ECRC 错误状态位。它们也可以选择不为该请求返回完成,导致请求者的完成超时,请求者的软件可能选择重新调度该请求。

- **完成中的 ECRC** — 检测到 ECRC 错误的请求者必须设置 ECRC 错误状态位。除了标准错误报告机制之外,它们还可以选择使用特定于功能的中断将错误报告给它们的设备驱动程序。与之前一样,软件可能决定重新安排失败的请求。

在任何一种情况下,可能会将不可纠正的非致命错误消息发送到系统。如果是这样,则可能会访问设备驱动程序以检查 _Uncorrectable Error Status Register_ 中的状态位并了解错误的性质。如果可能,可以重新调度失败的请求,但可能需要其他步骤。

## **数据中毒** 

数据中毒,也称为错误转发,提供了一种可选方式让设备指示与 TLP 关联的数据已损坏。在这些情况下,分组标头中的 EP(Error Poisoned)位被设置以指示错误。EP 位如图 15-6(第 660 页)所示。

_Figure 15-6: 完成标头中的错误/中毒位_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

每当传输数据时,例如在写请求或带数据的完成中,这些数据的损坏可能会发生,这需要报告给目标设备。在每种情况下,分组都可以转发给接收者,但通过标头中的 EP 位标记为具有坏数据。细心的读者可能想知道为什么人们可能想要发送已知为坏的数据。碰巧的是,有些情况下这是有用的:

1. 如果请求导致返回带数据的完成,但该数据在从目标收集时遇到错误(例如内存中的奇偶校验或 ECC 失败),那么报告它的最佳方式是什么?一种方法是不发送完成,但是如果错误不以其他方式报告,则系统仅在请求者处看到完成超时。该响应没有多大帮助,因为任何数量的问题都可能导致该结果。

 - 另一方面,如果以设置中毒位的方式传送完成,则至少请求者可以看到到完成者的往返路径必须正确工作。因此,问题一定发生在完成者内部,或者在路径中的交换机中。将采取什么步骤将是特定于实现的,但比简单地完成超时更清楚地知道出了什么问题。

2. 它可用于报告中间问题。如果数据有效负载在通过交换机时被损坏,则仍可以转发分组并设置 EP 位以指示问题。

3. 目标设备可能可以接受有错误的数据。例如,音频输出设备需要接收及时的数据流才能正常工作。如果传入数据有错误,则后果很小(音频输出中的毛刺),并且恢复时间将足够长以引起明显的延迟,因此可以按原样接受数据,而不是尝试恢复数据。

4. 目标设备可能具有纠正数据的手段。数据可能可以直接恢复,或者目标可能具有重新创建其部分的方法,或者具有解决该问题的某种其他方法。

规范规定,数据中毒仅适用于与分组关联的数据有效负载(例如内存、配置或 I/O 写入和完成),而从不适用于 TLP 标头的内容。因此,如果接收器看到没有有效负载的中毒分组(EP=1)(例如中毒的内存读取),则其行为未定义。只能在设备的事务层执行中毒;数据链路层不检查或影响 TLP 标头的内容。

错误转发支持被声明为发送器可选的,并且对于接收器缺少这样的声明暗示它不是可选的。

## **PCI Express Technology** 

如果发送器支持它,则使用旧版 Command 寄存器中的 Parity Error Response 位启用它。这是因为中毒分组大致类似于 PCI 中的奇偶校验错误,因为 PCI 以这种方式报告坏数据。如果启用,接收到中毒分组可以通过错误消息报告给系统,并且如果存在可选的高级错误报告寄存器,也将设置 Poisoned TLP 状态位。

可以预期,不允许对控制位置的中毒写入修改目标中的内容。规范中给出的示例是配置写入、对控制寄存器的 IO 或内存写入以及 AtomicOp。接收到中毒分组的交换机必须将它们不变地转发到目标端口,尽管如果它们已启用,则必须将此分组报告为错误,以帮助软件确定错误发生的位置。接收到中毒的非发布请求的完成者预期将返回具有 UR(Unsupported Request)状态的完成。

## **拆分事务错误** 

在与非发布请求相关联的拆分事务期间可能发生各种故障。PCIe 在完成标头中定义了一个状态字段,允许完成者将某些错误报告回请求者。图 15-7(第 662 页)说明了该字段在完成标头中的位置,表 15-1(第 663 页)给出了可能的值。如表所示,仅定义了四种编码,其中两种表示错误情况。

_Figure 15-7: 完成标头内的完成状态字段_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

_Table 15-1: 完成代码和描述_ 

|**状态代码**|**完成状态定义**|
|---|---|
|000b|成功完成 (SC)|
|001b|不受支持的请求 (UR) - 错误|
|010b|配置请求重试状态 (CRS)|
|011b|完成者中止 (CA) - 错误|
|100b - 111b|保留|


## **不受支持的请求 (UR) 状态** 

如果接收器不支持请求,则返回具有 UR 状态的完成。规范定义了许多可能导致 UR 状态的条件。一些示例是:

- 不支持请求类型(示例:对原生端点的 IO 请求或对原生端点的 MRdLk) 

- 带有不受支持或未定义消息代码的消息 

- 请求未引用映射到设备的地址空间 

- 请求地址未映射到交换机端口的地址范围内 

- 中毒写请求(EP=1)以完成者中的 I/O 或内存映射控制空间为目标。此类请求不得被允许修改该位置,而是由完成者丢弃并以具有 UR 状态的完成进行报告。

- 下游根或交换机端口接收到针对其辅助总线上不存在的设备的配置请求(例如,具有非零设备号的设备,除非启用 ARI)。该端口必须终止请求并返回具有 UR 状态的完成,因为下游设备号需要为零(除非启用 ARI,替代路由 ID 解释)。

- 在端点处接收到 Type 1 配置请求。 

- 使用保留的完成状态字段编码的完成必须解释为 UR。 

- 处于 D1、D2 或 D3hot 电源管理状态下的 Function 接收到除配置请求或消息之外的请求。 

- 标头中未设置 No Snoop 位的 TLP 被路由到其 VC Resource Capability 寄存器中设置了 Reject Snoop Transactions 位的端口。 

## **PCI Express Technology** 

## **完成者中止 (CA) 状态** 

可能发生多种情况,导致完成者将 CA 状态返回给请求者。一些示例是:

- 完成者收到无法在不违反其编程规则的情况下完成的请求。例如,某些 Function 可能被设计为仅允许以完整和对齐的方式访问某些寄存器(例如,4 字节寄存器可能需要 4 字节对齐访问)。以部分或未对齐方式访问其中一个寄存器的任何尝试(例如,仅读取 4 字节寄存器的两个字节)将失败。此类限制不是违反规范,而是与该 Function 的编程接口相关的合法约束。访问此类 Function 基于设备驱动程序了解如何访问其 Function 的期望。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-12"></a>
## 14.12 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

If the optional ECRC capability is enabled, a special bit called TD (TLP Digest) is set in the header to indicate that it’s present at the end of the packet (the ECRC is also called the Digest). The TD bit in the packet header is shown in Figure 15‐ 5 on page 659. The spec emphasizes that this bit must be treated with special care when forwarding a TLP because if it’s missing but the ECRC is present, or vice‐versa, then the packet will be considered Malformed. 

_Figure 15‐5: TLP Digest Bit in a Completion Header_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Variant Bits Not Included in ECRC Mechanism** 

The ECRC is calculated based on the contents of the header and data. Since these are not expected to change, the result should be the same when the check is performed at the receiver. However, it turns out that two header bits can legally change while the packet is in flight: bit 0 of the Type field, and the EP bit. Bit 0 of the Type field can change in Configuration Requests for the simple rea‐ son that the Request will be Type 1 until it has reached its destination bus, and then it will become Type 0. That involves changing bit 0 of the Type field. The EP bit can also be legally changed by intermediate devices if they detect a data error. For example, if a Switch forwards a TLP but it suffers an internal error of some kind that corrupts the data, setting the EP bit as it goes out the Egress Port is one way to report the error (known as error forwarding or data poisoning). 

Since these two bits can change while the packet is in flight they are called “variant bits” and cannot be used in the generation or checking of ECRC. Instead, their values are always assumed to be 1b for ECRC generation and checking instead of using the actual values. That way the ECRC doesn’t depend on them and will be correctly evaluated. 

The actions taken when an ECRC error is detected are beyond the scope of the spec, but the possible choices will depend on whether the error is found in a Request or a Completion. 

- **ECRC in Request** — Completers that detect an ECRC error must set the ECRC error status bit. They may also choose not to return a Completion for this Request, resulting in a Completion timeout at the Requester, whose software might then choose to reschedule the Request. 

- **ECRC in Completion** — Requesters that detect an ECRC error must set the ECRC error status bit. Besides the standard error reporting mechanism, they may also choose to report the error to their device driver with a Func‐ tion‐specific interrupt. As before, the software might decide to reschedule the failed Request. 

In either case, an Uncorrectable Non‐fatal error Message may be sent to the sys‐ tem. If so, the device driver would probably be accessed to check the status bits in the _Uncorrectable Error Status Register_ and learn the nature of the error. If pos‐ sible, the failed Request may be rescheduled, but other steps might be needed. 

## **Data Poisoning** 

Data poisoning, also called Error Forwarding, provides an optional way for a device to indicate that the data associated with a TLP is corrupted. In these cases, the EP (Error Poisoned) bit in the packet header is set to indicate the error. The EP bit is shown in Figure 15‐6 on page 660. 

_Figure 15‐6: The Error/Poisoned Bit in a Completion Header_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

Anytime data is transferred, such as in write Requests or Completions with data, corruption of that data could happen which needs to be reported to the target device. In each of these cases, the packet can be forwarded to the recipient but marked as having bad data by the EP bit in the header. The thoughtful reader may wonder why one might want to send data that is already known to be bad. As it happens, there are some cases where it’s useful: 

1. If a Request results in a Completion returned with data, but that data encountered an error as it was gathered from the target (like a parity or ECC failure in memory), then what is the best way to report it? One approach would be not to send the Completion at all but, if the error isn’t reported in some other way, the system only sees a Completion timeout at the Requester. That response isn’t very helpful because any number of prob‐ lems might result in that outcome. 

 - If, on the other hand, the Completion is delivered with the poisoned bit set, then at least the Requester can see that the round‐trip path to the Completer must have been working correctly. Therefore, the problem must have occurred internally to the Completer or else in a Switch that was in the path. What steps will be taken will be implementation specific, but more is known about what must have gone wrong than if the Completion simply timed out. 

2. It can be used to report an intermediate problem. If a data payload is cor‐ rupted while passing through a Switch, the packet can still be forwarded with the EP bit set to indicate the problem. 

3. It may be that the target device can accept the data with errors. As an exam‐ ple, an audio output device needs to receive a timely data stream to work well. If incoming data has an error, the consequences are small (glitch in the audio output) and the time to recover would be long enough to cause a noticeable delay, so it can be better to take it as is rather than attempting recovery of the data. 

4. A target device might have a means of correcting the data. The data might be directly recoverable, or the target might have a means of re‐creating parts of it, or have some other means of working around the problem. 

The spec states that data poisoning applies only to the data payload associated with a packet (such as Memory, Configuration, or I/O writes and Completions) and never to the contents of the TLP header. Consequently, a receiver’s behavior is undefined if it sees a poisoned packet (EP=1) with no payload (like a poisoned memory read). Poisoning can only be done at the Transaction Layer of a device; the Data Link Layer does not examine or affect the contents of the TLP header. 

Error forwarding support is stated to be optional for transmitters, and the absence of such a statement for receivers implies that it’s not optional for them. 

## **PCI Express Technology** 

If a transmitter supports it, it’s enabled with the Parity Error Response bit in the legacy Command register. That’s because a Poisoned packet is roughly analo‐ gous to a parity error in PCI, since that’s how PCI reports bad data. Receipt of a poisoned packet may be reported to the system with an error Message if enabled and, if the optional Advanced Error Reporting registers are present, will also set the Poisoned TLP status bit. 

As one might expect, poisoned writes to control locations are not allowed to modify the contents in the target. Examples given in the spec are Configuration writes, IO or memory writes to control registers, and AtomicOps. Switches that receive poisoned packets must forward them unchanged to the destination port although, if they’ve been enabled to do so, they must report this packet as an error to help software determine where the error happened. Completers that receive a poisoned non‐posted Request are expected to return a Completion with a status of UR (Unsupported Request). 

## **Split Transaction Errors** 

A variety of failures can occur during a split transaction associated with non‐ posted requests. PCIe defines a status field within the Completion header that allows the Completer to report some errors back to the Requester. Figure 15‐7 on page 662 illustrates the location of this field in a completion header and Table 15‐1 on page 663 gives the possible values. As the table shows, only four encodings are defined, two of which represent error conditions. 

_Figure 15‐7: Completion Status Field within the Completion Header_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

_Table 15‐1: Completion Code and Description_ 

|**Status Code**|**Completion Status Definition**|
|---|---|
|000b|Successful Completion (SC)|
|001b|Unsupported Request (UR) ‐ error|
|010b|Configuration Request Retry Status (CRS)|
|011b|Completer Abort (CA) ‐ error|
|100b ‐ 111b|Reserved|


## **Unsupported Request (UR) Status** 

If a receiver doesn’t support a Request, it returns a Completion with UR status. The spec defines a number of conditions that could result in a UR status. Some examples are: 

- Request type not supported (example: IO Request to native Endpoint or MRdLk to native Endpoint) 

- Message with unsupported or undefined message code 

- Request does not reference address space mapped to the device 

- Request address isn’t mapped within a Switch Port’s address range 

- Poisoned write Request (EP=1) targets an I/O or Memory‐mapped control space in the Completer. Such Requests must not be allowed to modify the location and are instead discarded by the Completer and reported with a Completion having a UR status. 

- A downstream Root or Switch Port receives a configuration Request target‐ ing a device on its Secondary Bus that doesn’t exist (e.g. a device with a non‐zero device number, unless ARI is enabled). The Port must terminate the Request and return a Completion with UR status because the down‐ stream Device number is required to be zero (unless ARI, Alternative Rout‐ ing‐ID Interpretation, is enabled). 

- Type 1 configuration Request is received at an Endpoint. 

- Completion using a reserved Completion Status field encoding must be interpreted as UR. 

- A function in the D1, D2, or D3hot power management state receives a Request other than a configuration Request or Message. 

- A TLP without the No Snoop bit set in its header is routed to a port that has the Reject Snoop Transactions bit set in its VC Resource Capability register. 

## **Completer Abort (CA) Status** 

Several circumstances can occur that could result in a Completer returning this CA status to the Requester. Some examples are: 

- Completer receives a Request that it cannot complete without violating its programming rules. For example, some Functions may be designed to only allow accesses to some registers in a complete and aligned manner (e.g. a 4‐ byte register may require a 4‐byte aligned access). Any attempt to access one of these registers in a partial or misaligned fashion (e.g. reading only two bytes of a 4‐byte register) would fail. Such restrictions are not violations of the spec, but rather legal constraints associated with the programming interface for this Function. Access to such a Function is based on the expec‐ tation that the device driver understands how to access its Function.

</td>
<td style="background-color:#e8e8e8">

如果启用了可选的 ECRC 功能，则头标中称为 TD（TLP Digest，TLP 摘要）的一个特殊位被置位，以指示它在包的末尾存在（ECRC 也称为 Digest）。包头中的 TD 位在第 659 页的图 15‐5 中显示。规范强调在转发 TLP 时必须特别小心地处理此位，因为如果缺失但 ECRC 存在，反之亦然，那么该包将被视为格式错误（Malformed）。

_图 15‐5：完成头中的 TLP Digest 位_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **未包含在 ECRC 机制中的可变位**

ECRC 是基于头标和数据的内容计算的。由于这些预计不会更改，因此在接收器执行检查时结果应该是相同的。然而，事实上在包传输过程中，两个头标位可以合法地更改：Type 字段的位 0 和 EP 位。Type 字段的位 0 可以在配置请求中更改，原因很简单：请求在到达其目标总线之前将是 Type 1，然后变为 Type 0。这涉及更改 Type 字段的位 0。如果中间设备检测到数据错误，EP 位也可以被合法地更改。例如，如果交换机转发了 TLP，但它由于某种内部错误而使数据损坏，则在通过出口端口发出时设置 EP 位是报告错误的一种方法（称为错误转发或数据中毒）。

由于这两个位在包传输过程中可以更改，因此它们被称为"可变位"，不能用于 ECRC 的生成和检查。相反，它们的值在 ECRC 生成和检查时始终假定为 1b，而不是使用实际值。这样 ECRC 不依赖于它们，并且将被正确评估。

**PCI Express 技术**

检测到 ECRC 错误时所采取的操作超出了规范的范围，但可能的选择将取决于错误是在请求中还是在完成中发现的。

- **请求中的 ECRC** — 检测到 ECRC 错误的完成器必须设置 ECRC 错误状态位。它们也可以选择不为该请求返回完成，从而在请求方导致完成超时，其软件可能随后选择重新调度该请求。

- **完成中的 ECRC** — 检测到 ECRC 错误的请求方必须设置 ECRC 错误状态位。除了标准错误报告机制外，它们还可以选择使用特定功能的中断向其设备驱动程序报告错误。如前所述，软件可能决定重新调度失败的请求。

在任何情况下，都可以将不可恢复的非致命错误消息发送到系统。如果是这样，则可能需要访问设备驱动程序以检查 _Uncorrectable Error Status Register_（不可恢复错误状态寄存器）中的状态位并了解错误的性质。如果可能，可以重新调度失败的请求，但可能需要其他步骤。

## **数据中毒**

数据中毒（也称为错误转发）提供了一种可选方式，让设备指示与 TLP 关联的数据已损坏。在这些情况下，包头中的 EP（Error Poisoned，错误中毒）位被设置以指示错误。EP 位在第 660 页的图 15‐6 中显示。

_图 15‐6：完成头中的错误/中毒位_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**第 15 章：错误检测和处理**

任何时候传输数据（例如在写请求或带数据的完成中），都可能发生数据损坏，需要将其报告给目标设备。在这些情况下，包可以被转发给接收者，但通过头中的 EP 位标记为具有错误数据。细心的读者可能想知道为什么要发送已知错误的数据。事实是，有些情况下这是有用的：

1. 如果请求导致返回带数据的完成，但在从目标收集数据时遇到错误（例如内存中的奇偶校验或 ECC 故障），那么最好的报告方式是什么？一种方法是根本不发送完成，但如果错误未以其他方式报告，则系统仅在请求方看到完成超时。该响应不是很有帮助，因为任何数量的问题都可能导致该结果。

 - 另一方面，如果完成以中毒位被置位的方式传递，则请求方至少可以看到到完成器的往返路径必须已正常工作。因此，问题一定发生在完成器内部或路径中的交换机中。将采取哪些步骤是实现特定的，但比完成简单超时要更清楚地知道发生了什么问题。

2. 它可以用于报告中间问题。如果数据有效载荷在通过交换机时被损坏，则仍然可以转发包并将 EP 位置位以指示问题。

3. 目标设备可能能够接受有错误的数据。例如，音频输出设备需要接收及时的数据流才能良好工作。如果传入数据有错误，则后果很小（音频输出中的毛刺），并且恢复时间足够长以导致明显的延迟，因此最好按原样接收数据，而不是尝试恢复数据。

4. 目标设备可能有办法纠正数据。数据可能可直接恢复，或者目标可能有办法重新创建其某些部分，或者有其他方法可以解决该问题。

规范声明数据中毒仅适用于与包关联的数据有效负载（例如 Memory、Configuration 或 I/O 写以及完成），而从不适用于 TLP 头的内容。因此，如果接收器看到没有有效负载的中毒包（如中毒的内存读取），则其行为是未定义的。中毒只能由设备的事务层执行；数据链路层不检查或影响 TLP 头的内容。

错误转发支持对于发送器是可选的，而对于接收器缺少此类声明意味着它对它们不是可选的。

## **PCI Express 技术**

如果发送器支持它，则通过传统 Command 寄存器中的 Parity Error Response 位启用它。这是因为中毒包大致类似于 PCI 中的奇偶校验错误，因为那是 PCI 报告错误数据的方式。如果已启用，则可以将接收到中毒包的情况通过错误消息报告给系统，并且如果存在可选的高级错误报告寄存器，则还将设置中毒 TLP 状态位。

可以预期的是，对控制位置的中毒写入不允许修改目标中的内容。规范中给出的示例包括配置写入、对控制寄存器的 IO 或内存写入，以及 AtomicOps。接收到中毒包的交换机必须将其原封不动地转发到目标端口，但如果它们已启用相应的错误报告功能，则必须将该包报告为错误，以帮助软件确定错误发生的位置。预期接收到中毒的非发布请求的完成器将返回状态为 UR（Unsupported Request，不支持的请求）的完成。

## **分离事务错误**

在与非发布请求相关联的分离事务期间可能会发生各种故障。PCIe 在完成头中定义了一个状态字段，允许完成器将某些错误报告回请求方。第 662 页的图 15‐7 说明了该字段在完成头中的位置，第 663 页的表 15‐1 给出了可能的值。如表所示，仅定义了四个编码，其中两个表示错误情况。

_图 15‐7：完成头中的完成状态字段_

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**第 15 章：错误检测和处理**

_表 15‐1：完成代码及其描述_

|**状态码**|**完成状态定义**|
|---|---|
|000b|成功完成 (SC)|
|001b|不支持的请求 (UR) - 错误|
|010b|配置请求重试状态 (CRS)|
|011b|完成器中止 (CA) - 错误|
|100b - 111b|保留|


## **不支持的请求 (UR) 状态**

如果接收器不支持某个请求，则返回带有 UR 状态的完成。规范定义了许多可能导致 UR 状态的条件。一些示例是：

- 不支持请求类型（例如：对原生端点的 IO 请求或对原生端点的 MRdLk）

- 带有不受支持或未定义消息代码的消息

- 请求未引用映射到设备的地址空间

- 请求地址未映射到交换机端口的地址范围内

- 中毒的写请求（EP=1）目标是完成器中的 I/O 或内存映射的控制空间。此类请求不得允许修改该位置，而是由完成器丢弃，并报告带有 UR 状态的完成。

- 下游根或交换机端口接收到针对其辅助总线上不存在设备的配置请求（例如，具有非零设备号的设备，除非启用了 ARI）。端口必须终止该请求并返回带有 UR 状态的完成，因为下游设备号必须为零（除非启用了 ARI，即 Alternative Routing‐ID Interpretation，备用路由 ID 解释）。

- 在端点接收到 Type 1 配置请求。

- 使用保留的完成状态字段编码的完成必须被解释为 UR。

- 处于 D1、D2 或 D3hot 电源管理状态的功能接收到除配置请求或消息以外的请求。

- 头中未设置 No Snoop 位的 TLP 被路由到其 VC 资源能力寄存器中设置了 Reject Snoop Transactions 位的端口。

## **PCI Express 技术**

## **完成器中止 (CA) 状态**

在某些情况下，可能导致完成器向请求方返回此 CA 状态。一些示例是：

- 完成器接收到一个无法在不违反其编程规则的情况下完成的请求。例如，某些功能可能设计为仅允许以完整和对齐的方式访问某些寄存器（例如，4 字节寄存器可能需要 4 字节对齐的访问）。以部分或不对齐的方式访问这些寄存器中的任何一个（例如，仅读取 4 字节寄存器中的两个字节）都将失败。此类限制不是违反规范，而是与该功能的编程接口相关的合法约束。对此类功能的访问基于设备驱动程序了解如何访问其功能的预期。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-13"></a>
## 14.13 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Completer receives a Request that it cannot process because of some perma‐ nent error condition in the device. For example, a wireless LAN card that won’t accept new packets because it can’t transmit or receive over its radio until an approved antenna is attached. 

- Completer receives a Request for which it detects an ACS (Access Control Services) error. An example of this would be a Root Port that implements the ACS registers and has ACS Translation Blocking enabled. If a memory Request is seen on that Port with anything other than the default value in the AT field, it will be an ACS violation. 

- PCIe‐to‐PCI Bridge may receive a Request that targets the PCI bus. PCI allows the target device to signal a target abort if it can’t complete the Request due to some permanent condition or violation of the Function’s programming rules. In response, the bridge would return a Completion with CA status. 

A Completer that aborts a Request may report the error to the Root with a Non‐ fatal Error Message and, if the Request requires a Completion, the status would be CA. 

## **Unexpected Completion** 

When a Requester receives a Completion, it uses the transaction descriptor (Requester ID and Tag) to match it with an earlier Request. In rare circum‐ stances, the transaction descriptor may not match any previous Request. This might happen because the Completion was mis‐routed on its journey back to the intended Requester. An Advisory Non‐fatal Error Message can be sent by the device that receives the unexpected Completion, but it’s expected that the correct Requester will eventually timeout and take the appropriate action, so that error Message would be a low priority. 
## **Completion Timeout** 

For the case of a pending Request that never receives the Completion it’s expect‐ ing, the spec defines a Completion timeout mechanism. The spec clearly intends this to detect when a Completion has no reasonable chance of returning; it should be longer than any normal expected latencies. 

The Completion timeout timer must be implemented by all devices that initiate Requests that expect Completions, except for devices that only initiate configu‐ ration transactions. Note also that every Request waiting for Completions is timed independently, and so there must be a way to track time for each out‐ standing transaction. The 1.x and 2.0 versions of the spec defined the permissi‐ ble range of the timeout value as follows: 

- It is strongly recommended that a device not timeout earlier than 10ms after sending a Request; however, if the device requires greater granularity a tim‐ eout can occur as early as 50μs. 

- Devices must time‐out no later than 50ms. 

Beginning with the 2.1 spec revision, the Device Control Register 2 was added to the PCI Express Capability Block to allow software visibility and control of the timeout values, as shown in Figure 15‐8 on page 665. 

_Figure 15‐8: Device Control Register 2_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


If Requests need multiple Completions to return the requested data, a single Completion won’t stop the timer. Instead, the timer continues to run until all the data has been returned regardless of how many Completions are needed. If only part of the data has been returned when the timeout occurs, the Requester may discard or keep that data. 

## **Link Flow Control Related Errors** 

Prior to forwarding the packet to the Data Link Layer for transmission, the Transaction Layer must check Flow Control (FC) credits to ensure that the receive buffers of the Link neighbor have sufficient room to hold it. Flow Con‐ trol violations may occur, and they are considered uncorrectable. Protocol viola‐ tions related to Flow Control can detected by and associated with the port receiving the Flow Control information. Some examples are given here: 

- Link partner fails to advertise at least the minimum number of FC credits defined by the spec during FC initialization for any Virtual Channel. 

- Link partner advertises more than the allowed maximum number of FC credits (up to 2047 unused credits for data payload and 127 unused credits for headers). 

- Receipt of FC updates containing non‐zero values in credit fields that were initially advertised as infinite. 

- A receive buffer overflow, resulting in lost data. This check is optional but a detected violation is considered to be a Fatal error. 

## **Malformed TLP** 

TLPs arriving in the Transaction Layer are checked for violations of the packet formatting rules. A violation in the packet format is considered a Fatal error because it means the transmitter has made a grievous mistake in protocol, such as failing to properly maintain its counters, and the result is that it’s no longer performing as expected. Some examples of a packet being considered mal‐ formed (badly formed) include the following: 

- Data payload exceeds Max payload size. 

- Data length does not match length specified in the header. 

- Memory start address and length combine to cause a transaction to cross a naturally‐aligned 4KB boundary. 

- TLP Digest (TD field) indication doesn’t correspond with packet size (ECRC is unexpectedly missing or present). 

- Byte Enable violation. 

- Undefined Type field values. 

- Completion that violates the Read Completion Boundary (RCB) value. 

- Completion with status of Configuration Request Retry Status in response to a Request other than a configuration Request. 

- Traffic Class field contains a value not assigned to an enabled Virtual Chan‐ nel (this is also known as TC Filtering). 
- I/O and Configuration Request violations (checking optional) ‐ examples: TC field, Attr[1:0], and the AT field must all be zero, while the Length field must have a value of one. 

- Interrupt emulation messages sent downstream (checking optional). 

- TLP received with a TLP Prefix error: 

 - 

 - TLP Prefix but no TLP Header 

- End‐to‐End TLP Prefixes preceding Local Prefixes 

- Local TLP Prefix type not supported 

- 

 - More than 4 End‐to‐End TLP Prefixes 

 - More End‐to‐End TLP Prefixes than are supported 

- Transaction type requiring use of TC0 has a different TC value: 

 - 

 - I/O Read or Write Requests and corresponding Completions 

- Configuration Read or Write Requests and corresponding Completions 

- — Error Messages 

- INTx messages 

- Power Management messages 

- Unlock messages 

- Slot Power messages 

- LTR messages 

- 

 - OBFF messages 

- AtomicOp operand doesn’t match an architected value. 

- AtomicOp address isn’t naturally aligned with operand size. 

- Routing is incorrect for transaction type (e.g., transactions requiring routing to Root Complex detected moving away from Root Complex). 

## **Internal Errors** 

## **The Problem** 

The first versions of the PCIe spec did not include a mechanism for reporting errors within a device that were unrelated to transactions on the interface itself. For Endpoints this wasn’t really a problem because they have a vendor‐specific device driver associated with them that can detect and report internal errors. However, Switches are considered system resources that are managed by the OS, and typically don’t have software to help with internal error detection. In high‐end systems, the ability to contain errors is important, so Switch vendors created proprietary means of handling internal errors. Unfortunately, since dif‐ ferent vendor solutions were incompatible with each other, the end result was that they were seldom used. 

## **The Solution** 

To alleviate this situation, a standardized internal error reporting option was added with the 2.1 spec version. The definition of what constitutes an internal error is beyond the scope of the spec, but they can be reported as either Cor‐ rected or Uncorrectable Internal Errors. 

A Corrected Internal Error means an error was masked or worked around by the hardware with no loss of information or improper behavior. An example would be an ECC error on an internal memory location that was corrected auto‐ matically. On the other hand, an Uncorrectable Internal Error means improper operation has resulted with potential data loss, such as a parity error on an internal memory location. Reporting internal errors is optional and, if it is used, the AER (Advanced Error Reporting) registers must be present to support it. 

## **How Errors are Reported** 

## **Introduction** 

PCI Express includes three methods of reporting errors, as shown below. The first two, Completions and poisoned packets, were covered earlier, so our next topic will be the error Messages. 

- Completions — Completion Status reports errors back to the Requester 

- Poisoned Packet — reports bad data in a TLP to the receiver 

- Error Message — reports errors to the host (software) 

## **Error Messages** 

PCIe eliminated the sideband signals from PCI and replaced them with Error Messages. These Messages provide information that could not be conveyed with the PERR# and SERR# signals, such as identifying the detecting Function and indicating the severity of the error. Figure 15‐9 illustrates the Error Message format. Note that they’re routed to the Root Complex for handling. The Mes‐ sage Code defines the type of Message being signaled. Not surprisingly, the spec defines three types of error Messages, as shown in Table 15‐2. 
_Table 15‐2: Error Message Codes and Description_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Advisory Non-Fatal Errors**

</td>
<td style="background-color:#e8e8e8">

- Completer 收到一个由于设备中某些永久性错误状态而无法处理的请求 (Request)。例如，一张无线 LAN 卡因天线未获批而无法通过其无线电进行发送或接收，因此不接受新数据包。

- Completer 收到检测到 ACS (Access Control Services) 错误的请求。这种情况的一个例子是实现 ACS 寄存器的根端口 (Root Port) 启用了 ACS Translation Blocking。如果在该端口上看到 AT 字段不是默认值的内存请求，就会发生 ACS 违规。

- PCIe-to-PCI 桥 (Bridge) 可能收到一个目标为 PCI 总线的请求。PCI 允许目标设备在因某种永久性状态或函数 (Function) 编程规则被违反而无法完成请求时发出目标中止 (target abort)。作为响应，桥将返回一个 CA 状态的完成 (Completion)。

中止请求的 Completer 可以通过 Non-fatal Error Message 向根 (Root) 报告该错误，并且如果该请求需要完成，则状态将为 CA。

## **意外完成 (Unexpected Completion)**

当 Requester 收到完成时，它使用事务描述符 (Requester ID 和 Tag) 将其与先前的请求进行匹配。在极少数情况下，事务描述符可能不匹配任何先前的请求。这可能是因为完成在返回到指定 Requester 的途中被错误路由。收到意外完成的设备可以发送一个 Advisory Non-fatal Error Message，但预计正确的 Requester 最终会超时并采取适当的措施，因此该错误消息优先级较低。

**第 15 章：错误检测与处理**

## **完成超时 (Completion Timeout)**

对于永不收到其所期望的完成的待处理请求，规范定义了一种完成超时机制。规范明确地将其用于检测完成没有合理机会返回的情况；它应当长于任何正常预期的延迟。

完成超时计时器必须由所有发起期望完成的请求的设备实现，但只发起配置事务的设备除外。另请注意，每个等待完成的请求都是独立计时的，因此必须有一种方法为每个未完成的事务单独计时。规范的 1.x 和 2.0 版本定义了超时值的允许范围，如下所示：

- 强烈建议设备在发出请求后不少于 10ms 才超时；但是，如果设备需要更精细的粒度，超时可以早至 50µs。

- 设备必须不迟于 50ms 超时。

从 2.1 规范版本开始，在 PCI Express Capability Block 中增加了 Device Control Register 2，以便软件可见和控制超时值，如图 15-8 在第 665 页所示。

_图 15-8：Device Control Register 2_

**==> 图片 [152 x 122] 已省略 <==**


如果请求需要多个完成才能返回所请求的数据，单个完成不会停止计时器。相反，计时器会持续运行，直到所有数据都已返回，无论需要多少个完成。如果在超时时仅返回了部分数据，Requester 可以丢弃或保留这些数据。

## **链路流控相关错误 (Link Flow Control Related Errors)**

在将数据包转发到数据链路层进行传输之前，事务层 (Transaction Layer) 必须检查流控 (Flow Control, FC) 信用，以确保链路邻居的接收缓冲区有足够的空间容纳它。可能发生流控违规，这些违规被认为是不可纠正的。与流控相关的协议违规可由接收流控信息的端口检测到并与之关联。以下给出了一些示例：

- 链路伙伴在任意虚通道 (Virtual Channel) 的 FC 初始化期间未公布规范所定义的至少最小数量的 FC 信用。

- 链路伙伴公布的 FC 信用超过允许的最大数量（数据负载最多 2047 个未使用信用，标头最多 127 个未使用信用）。

- 收到的 FC 更新在初始被通告为无限的信用字段中包含非零值。

- 接收缓冲区溢出，导致数据丢失。此检查是可选的，但检测到的违规被认为是致命 (Fatal) 错误。

## **格式错误的 TLP (Malformed TLP)**

到达事务层的 TLP 会检查其是否违反数据包格式规则。数据包格式的违规被认为是致命错误，因为这意味着发送方在协议上犯了严重错误（例如未能正确维护其计数器），其结果是它不再按预期执行。以下是一些被视为格式错误（malformed）的数据包示例：

- 数据负载超过最大有效负载大小 (Max payload size)。

- 数据长度与标头中指定的长度不匹配。

- 内存起始地址和长度组合导致事务跨越自然对齐的 4KB 边界。

- TLP Digest（TD 字段）指示与数据包大小不对应（ECRC 意外缺失或存在）。

- 字节使能 (Byte Enable) 违规。

- 未定义的 Type 字段值。

- 违反读完成边界 (Read Completion Boundary, RCB) 值的完成。

- 对非配置请求的响应中包含 Configuration Request Retry Status 状态的完成。

- Traffic Class 字段包含未分配给已启用虚通道的值（也称为 TC 过滤）。

**第 15 章：错误检测与处理**

- I/O 和 Configuration 请求违规（检查可选）— 示例：TC 字段、Attr[1:0] 和 AT 字段必须全部为零，而 Length 字段必须具有值 1。

- 下游发送的中断仿真消息（检查可选）。

- 收到的 TLP 带有 TLP Prefix 错误：

 - 

 - TLP Prefix 但无 TLP Header

- End-to-End TLP Prefix 位于 Local Prefix 之前

- 不支持的 Local TLP Prefix 类型

- 

 - 超过 4 个 End-to-End TLP Prefix

 - End-to-End TLP Prefix 多于所支持的数量

- 需要使用 TC0 的事务类型具有不同的 TC 值：

 - 

 - I/O Read 或 Write 请求以及相应的完成

- Configuration Read 或 Write 请求以及相应的完成

- — Error Messages

- INTx messages

- Power Management messages

- Unlock messages

- Slot Power messages

- LTR messages

- 

 - OBFF messages

- AtomicOp 操作数与架构化值不匹配。

- AtomicOp 地址未与操作数大小自然对齐。

- 事务类型的路由不正确（例如，需要路由到根复合体的事务被发现远离根复合体）。

## **内部错误 (Internal Errors)**

## **问题 (The Problem)**

PCIe 规范的早期版本不包括报告设备内与接口本身事务无关的错误机制。对于端点 (Endpoint) 而言这并不是真正的问题，因为它们具有关联的供应商特定的设备驱动程序，可以检测和报告内部错误。然而，交换机 (Switch) 被视为由操作系统管理的系统资源，通常没有软件来帮助进行内部错误检测。在高端系统中，遏制错误的能力很重要，因此交换机供应商创建了专有的内部错误处理方法。不幸的是，由于不同供应商的解决方案互不兼容，最终结果是它们很少被使用。

## **解决方案 (The Solution)**

为了缓解这种情况，2.1 规范版本中增加了标准化的内部错误报告选项。什么构成内部错误的定义超出了规范的范围，但它们可以报告为已纠正 (Corrected) 或未纠正 (Uncorrectable) 的内部错误。

Corrected Internal Error 意味着硬件已屏蔽或绕过错误，没有信息丢失或行为不当。例如内部存储位置上的 ECC 错误被自动纠正。另一方面，Uncorrectable Internal Error 意味着操作不当已导致潜在的数据丢失，例如内部存储位置上的奇偶校验错误。报告内部错误是可选的，如果使用它，则必须存在 AER (Advanced Error Reporting) 寄存器以支持它。

## **如何报告错误 (How Errors are Reported)**

## **介绍 (Introduction)**

PCI Express 包含三种报告错误的方法，如下所示。前两种（完成和被毒化的数据包）已在前文介绍，所以我们的下一个主题将是错误消息 (Error Messages)。

- Completions — 完成状态 (Completion Status) 向 Requester 报告错误

- Poisoned Packet — 向接收方报告 TLP 中的坏数据

- Error Message — 向主机（软件）报告错误

## **错误消息 (Error Messages)**

PCIe 取消了 PCI 的边带信号，并用 Error Messages 替代。这些消息提供了 PERR# 和 SERR# 信号无法传达的信息，例如识别检测的函数并指示错误的严重程度。图 15-9 说明了错误消息格式。请注意，它们被路由到根复合体 (Root Complex) 进行处理。Message Code 定义了正在发信号的消息类型。毫不奇怪，规范定义了三种类型的错误消息，如表 15-2 所示。

**第 15 章：错误检测与处理**

_表 15-2：错误消息代码与描述_

**==> 图片 [389 x 479] 已省略 <==**


## **建议性非致命错误 (Advisory Non-Fatal Errors)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-14"></a>
## 14.14 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Since we’ve just seen that both types of Uncorrectable errors will need software attention, it sounds counter‐intuitive to say that there are cases where it’s prefer‐ able that a device not report Non‐Fatal errors it detects, but there are. These cases are predominantly based on the role of the detecting agent (Requester, Completer, or Intermediate device) and the type of error. The problem is that multiple devices might report an error caused by the same event and, on some platforms, sending one of the Non‐Fatal Error Messages (ERR_NONFATAL) can prevent software from properly handling the error. For example, if an End‐ point reports an error, its device driver will be called to service the situation. However, if a Switch reports an error first for the same transaction, system soft‐ ware might be called to investigate and might not understand what the driver was trying to accomplish or what would be the optimal response. 

That example illustrates that some detecting agents aren’t the best ones to deter‐ mine the ultimate disposition of the error and shouldn’t send an uncorrectable message. Instead, such an agent can signal an advisory notification to software with ERR_COR. This avoids confusion about the source of the uncorrectable error but still gives software a little more information about what happened. Eventually, the appropriate detecting agent will send the ERR_NONFATAL message whenever it sees the error. Beginning with the 1.1 spec revision, a new field was added in the PCI Express Device Capabilities register to indicate sup‐ port for this capability as shown in Figure 15‐10 on page 670. This bit must be set for every agent that is compliant with the 1.1 spec or later. 

_Figure 15‐10: Device Capabilities Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

In spite of the reasons just described, software might want to stop operation as soon as some advisory errors are seen by an intermediate device. Since newer devices will always perform role‐based error reporting, an override mechanism is needed. To handle this case, software can escalate the severity of the advisory errors from Non‐Fatal to Fatal in the AER (Advanced Error Reporting) registers. Since there is no “advisory fatal” case, the error will now be reported as a Fatal Error (ERR_FATAL), if enabled, regardless of the role of the device. 

## **Advisory Non-Fatal Cases** 

The spec lists five situations for which an advisory message (ERR_COR) is pre‐ ferred over a ERR_NONFATAL message. In each of these cases, the detecting agent will handle the error as an Advisory Non‐Fatal Error. This means that a Non‐Fatal condition will be handled by sending an ERR_COR, assuming the agent has AER registers and has enabled ERR_COR. If it doesn’t have AER reg‐ isters or ERR_COR was not enabled, it sends no Error Message. The five cases are as follows: 

1. Completer sent a Completion with UR or CA Status. The expectation in this case is that the Requester will have a mechanism to handle the error when it sees the offending Completion and will be the best agent to send whatever Error Messages are needed. A ERR_NONFATAL message from the Compl‐ eter would just be confusing, so it must be handled as Advisory Non‐Fatal (ERR_COR). 

 - Curiously, there is no PCIe mechanism for the Requester to report that it received a Completion with this status. Instead, a design‐specific method like an interrupt will be needed to get device driver attention. An important example of this happens when the Root Complex receives a Completion with UR or CA status in response to a Configuration Read Request. On some platforms the response is to return all 1’s to software for this case, to support backward compatibility with PCI enumeration (configuration probing) software. 

2. Intermediate device detected an error. This case comes up in systems that employ Switches because a detecting agent may not be the final destination for a TLP. As an example of this, consider Figure 15‐11 on page 672, show‐ ing a poisoned packet delivered through an intermediate Switch. The TLP is seen as a Non‐Fatal error by the Switch but it can only signal an ERR_COR message instead (as long as it’s enabled to do so). To explore this concept a little more, why wouldn’t we want the Switch to report ERR_NONFATAL? One reason is seen by looking at error tracking in the AER registers. Figure 15‐12 on page 672 shows the AER registers that track the Source ID (BDF of the sending device) of Error Messages coming into a Root Port and we can see that there’s only one space available for 

## **PCI Express Technology** 

uncorrectable errors. If multiple uncorrectable errors are seen, that fact will be noted but only the first source ID will be saved since it is considered to be the probable cause of subsequent errors. It’s important, therefore, that uncorrectable errors come from the most appropriate device to report them. It’s worth noting that it’s still helpful for intermediate devices to report ERR_COR, because it allows software to determine where the error was first detected. 

_Figure 15‐11: Role‐Based Error Reporting Example_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


_Figure 15‐12: Advanced Source ID Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

As another example, 1.0a devices that have the UR Reporting Enable bit cleared but don’t have the Role‐Based Error Reporting capability are unable to report any error Messages when a UR error is detected (for posted or non‐posted Requests). In contrast, a 1.1‐compliant or later Completer that has the SERR# Enable bit set will send an ERR_NONFATAL or ERR_FATAL message for bad posted Requests, even if the Unsupported Request Report‐ ing Enable bit is clear, so as to avoid silent data corruption. But it won’t send an error Message for non‐posted Requests received, so as to support the PCI‐compatible configuration method of probing with configuration reads. It’s recommended that software keep the UR Error Reporting Enable bit clear for devices that are not capable of Role‐Based Error Reporting, but set it for those that are. That way, UR errors are reported on bad posted requests, but not for bad non‐posted requests like configuration probing transactions, and backward compatibility with older software is main‐ tained. 

The spec also mentions that poisoned TLPs sent to the Root will be handled in the same way if the Root is acting as an intermediate agent, but there is one exception: If the Root doesn’t support Error Forwarding, it will be unable to communicate the poisoned error with the TLP and must report this as a Non‐Fatal error instead. 

3. Destination device received a poisoned TLP. Normally, Endpoints would report the Non‐Fatal error in this case, but there’s an exception to this rule: If the ultimate destination device is able to handle the poisoned data in a way that allows for continued operation, it must treat this case as an Advi‐ sory Non‐Fatal Error instead. 

 - An example of this behavior might be an audio device that receives stream‐ ing data that has been poisoned. In this situation, the data may be accepted even though it’s known to be corrupted because pausing the audio flow long enough to get software attention and take remedial action would be a worse alternative than allowing a glitch in the sound output. 

4. Requester experienced a Completion Timeout. This is a similar case to the previous one; if the Requester has a means of continuing operation in spite of the problem then it must treat this as an Advisory Non‐Fatal Error. A simple work‐around for the Requester in this case would simply be to send the request again and hope for better results this time. Clearly, this would only make sense if the previous request did not cause any side effects, but Requesters are permitted to do this as often as they like (although the spec says the number of retries must be finite). 

5. Unexpected completion received. This must be handled as an Advisory Non‐Fatal Error. The reason is that it was probably caused by a mis‐routed Completion and the original Requester will eventually report a Completion timeout. To allow that other Requester to attempt a retry of the failed 

request, it’s important that the one that sees the Unexpected Completion not send an Non‐Fatal message. 

## **Baseline Error Detection and Handling** 

This section defines the required support for detecting and reporting PCI Express errors. Compliant devices must include: 

- PCI‐Compatible support — required to honor PCI‐compatible error control and status fields for older software that has no awareness of PCI Express. 

- PCI Express Error reporting — uses standard PCIe structures to for error control and status which can be used by newer software that does have knowledge of PCI Express. 

## **PCI-Compatible Error Reporting Mechanisms** 

## **General** 

PCI Express errors are mapped into the original PCI configuration register bits for backward compatibility, allowing error status and control to be accessible to PCI‐compliant software. To understand the features available from the PCI‐ compatible point of view, consider the error‐related bits of the Command and Status registers located within the Configuration header. Some of the field defi‐ nitions have been modified to reflect the related PCIe error conditions and reporting mechanisms. The PCI Express errors tracked by the PCI‐compatible registers are: 

- Transaction Poisoning/Error Forwarding (synonymous to data parity error in PCI) 

- Completer Abort (CA) detected by a Completer (synonymous to Target Abort in PCI) 

- Unsupported Request (UR) detected by a Completer (synonymous to Mas‐ ter Abort in PCI) 

As mentioned earlier, the PCI mechanism for reporting errors is the assertion of PERR# (data parity errors) and SERR# (unrecoverable errors). The PCI Express mechanisms for reporting these events are the Completion Status values in Completions and Error Messages to the Root. 
## **Legacy Command and Status Registers** 

Figure 15‐13 on page 675 illustrates the Command register and the location of the error‐related fields. These bits are set to enable baseline error reporting under control of PCI‐compatible software. Table 15‐3 defines the specific effects of each bit. 

_Figure 15‐13: Command Register in Configuration Header_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**第 15 章：错误检测与处理**

尽管有上述原因，软件可能希望一旦中间设备检测到某些建议性错误就立即停止操作。由于较新的设备将始终执行基于角色的错误报告，因此需要一种覆盖机制。为了处理这种情况，软件可以在 AER (Advanced Error Reporting) 寄存器中将建议性错误的严重性从 Non-Fatal 升级为 Fatal。由于没有"建议性致命"的情况，如果启用，无论设备的角色如何，错误现在都将报告为致命错误 (ERR_FATAL)。

## **建议性非致命情况 (Advisory Non-Fatal Cases)**

规范列出了五种情况，其中建议性消息 (ERR_COR) 优于 ERR_NONFATAL 消息。在每种情况下，检测代理将把错误作为 Advisory Non-Fatal Error 处理。这意味着假设代理具有 AER 寄存器并已启用 ERR_COR，将通过发送 ERR_COR 来处理 Non-Fatal 条件。如果没有 AER 寄存器或未启用 ERR_COR，则不发送 Error Message。这五种情况如下：

1. Completer 发送了 UR 或 CA 状态的完成。在这种情况下，预期是 Requester 在看到违规的完成时将具有处理错误的机制，并且将是发送所需的任何 Error Message 的最佳代理。来自 Completer 的 ERR_NONFATAL 消息只会引起混淆，因此必须将其作为 Advisory Non-Fatal (ERR_COR) 处理。

 - 奇怪的是，没有 PCIe 机制供 Requester 报告它收到了具有此状态的完成。相反，将需要一种特定于设计的方法（如中断）来获得设备驱动程序的关注。当根复合体收到对 Configuration Read Request 的具有 UR 或 CA 状态的完成响应时，会发生这种情况的重要示例。在某些平台上，对此情况的响应是向软件返回全 1，以支持与 PCI 枚举（配置探测）软件的向后兼容性。

2. 中间设备检测到错误。这种情况出现在使用交换机的系统中，因为检测代理可能不是 TLP 的最终目的地。作为一个例子，考虑图 15-11 在第 672 页，显示通过中间交换机传递的被毒化数据包。TLP 被交换机视为 Non-Fatal 错误，但它只能发出 ERR_COR 消息代替（只要它已启用）。为了进一步探讨这个概念，为什么我们不希望交换机报告 ERR_NONFATAL？其中一个原因可以通过查看 AER 寄存器中的错误跟踪看出。图 15-12 在第 672 页显示了跟踪进入根端口 (Root Port) 的 Error Message 的源 ID（发送设备的 BDF）的 AER 寄存器，我们可以看到，对于

## **PCI Express Technology**

不可纠正错误只有一个可用空间。如果看到多个不可纠正的错误，则将注意到这一事实，但仅保存第一个源 ID，因为它被认为是后续错误的可能原因。因此，重要的是不可纠正的错误来自最合适的报告设备。值得注意的是，中间设备报告 ERR_COR 仍然是有帮助的，因为它允许软件确定错误最初是在哪里检测到的。

_图 15-11：基于角色的错误报告示例_

**==> 图片 [230 x 219] 已省略 <==**


_图 15-12：Advanced Source ID Register_

**==> 图片 [333 x 77] 已省略 <==**


**第 15 章：错误检测与处理**

作为另一个示例，清除了 UR Reporting Enable 位但没有基于角色的错误报告功能的 1.0a 设备在检测到 UR 错误（对于 posted 或 non-posted 请求）时无法报告任何错误消息。相比之下，符合 1.1 或更高版本的 Completer 如果设置了 SERR# Enable 位，则会针对错误的 posted 请求发送 ERR_NONFATAL 或 ERR_FATAL 消息，即使清除了 Unsupported Request Reporting Enable 位也是如此，以避免静默数据损坏。但它不会为收到的 non-posted 请求发送错误消息，以支持通过配置读取进行探测的 PCI 兼容配置方法。建议软件对那些不具备基于角色的错误报告功能的设备保持清空 UR Error Reporting Enable 位，但对具备该功能的设备则设置该位。这样，UR 错误会在错误的 posted 请求上报告，但不会在像配置探测事务这样的错误的 non-posted 请求上报告，并且保持了与旧软件的向后兼容性。

规范还提到，发送到根 (Root) 的被毒化的 TLP 在根充当中间代理时将以相同方式处理，但有一个例外：如果根不支持 Error Forwarding，它将无法通过 TLP 传达被毒化的错误，而必须将其报告为 Non-Fatal 错误。

3. 目标设备收到被毒化的 TLP。通常，端点会在这种情况下报告 Non-Fatal 错误，但此规则有一个例外：如果最终目标设备能够以允许继续操作的方式处理被毒化数据，则它必须将这种情况视为 Advisory Non-Fatal Error。

 - 这种行为的一个例子可能是收到已被毒化的流数据的音频设备。在这种情况下，即使已知数据已损坏，数据也可能会被接受，因为暂停音频流足够长的时间以引起软件注意并采取补救措施将是比允许声音输出中出现故障更糟糕的替代方案。

4. Requester 经历了 Completion Timeout。这与前一种情况类似；如果 Requester 有尽管出现问题仍能继续操作的方法，则它必须将其视为 Advisory Non-Fatal Error。在这种情况下，Requester 的简单解决方法将只是重新发送请求并希望这次有更好的结果。显然，只有在先前的请求没有引起任何副作用时这才有意义，但允许 Requester 根据需要执行此操作（尽管规范规定重试次数必须是有限的）。

5. 收到意外完成。这必须作为 Advisory Non-Fatal Error 处理。原因可能是由错误路由的完成引起的，并且原始 Requester 最终将报告完成超时。为了允许该其他 Requester 尝试重试失败

请求，看到意外完成的那一个不发送 Non-Fatal 消息是很重要的。

## **基线错误检测与处理 (Baseline Error Detection and Handling)**

本节定义了检测和报告 PCI Express 错误所需的支持。兼容设备必须包括：

- PCI 兼容支持 — 必须遵守 PCI 兼容错误控制和状态字段，以便不感知 PCI Express 的旧软件使用。

- PCI Express 错误报告 — 使用标准 PCIe 结构进行错误控制和状态，可供了解 PCI Express 的较新软件使用。

## **PCI 兼容错误报告机制 (PCI-Compatible Error Reporting Mechanisms)**

## **概述 (General)**

为了向后兼容，PCI Express 错误被映射到原始的 PCI 配置寄存器位，允许 PCI 兼容软件访问错误状态和控制。要从 PCI 兼容的角度了解可用的功能，请考虑配置头中 Command 和 Status 寄存器的错误相关位。一些字段定义已被修改，以反映相关的 PCIe 错误条件和报告机制。由 PCI 兼容寄存器跟踪的 PCI Express 错误包括：

- Transaction Poisoning/Error Forwarding（与 PCI 中的数据奇偶校验错误同义）

- 由 Completer 检测到的 Completer Abort (CA)（与 PCI 中的 Target Abort 同义）

- 由 Completer 检测到的 Unsupported Request (UR)（与 PCI 中的 Master Abort 同义）

如前所述，PCI 的错误报告机制是 PERR#（数据奇偶校验错误）和 SERR#（不可恢复错误）的断言。PCI Express 报告这些事件的机制是完成中的 Completion Status 值和到根的 Error Message。

**第 15 章：错误检测与处理**

## **传统 Command 和 Status 寄存器 (Legacy Command and Status Registers)**

图 15-13 在第 675 页说明了 Command 寄存器以及错误相关字段的位置。设置这些位是为了在 PCI 兼容软件的控制下启用基线错误报告。表 15-3 定义了每个位的具体作用。

_图 15-13：配置头中的 Command 寄存器_

**==> 图片 [390 x 396] 已省略 <==**


_表 15-3：Command 寄存器中与错误相关的字段（续）_

|**Name**|**Description**|
|---|---|
|Parity Error<br>Response|设置此位可启用在 Status 寄存器的 Master Data<br>Parity Error 位中记录被毒化的 TLP。<br>被毒化的数据包表示坏数据，大致类似于 PCI<br>奇偶校验错误。|


图 15-14 在第 676 页说明了 Configuration Status 寄存器以及错误相关位字段的位置。表 15-4 在第 677 页定义了设置每个位的情况以及启用错误报告时设备采取的操作。

_图 15-14：配置头中的 Status 寄存器_

**==> 图片 [304 x 220] 已省略 <==**


**第 15 章：错误检测与处理**

_表 15-4：Status 寄存器中与错误相关的字段_

|**Error-Related Bit**|**Description**|
|---|---|
|Detected Parity Error|由接收到被毒化 TLP 的端口设置。无论 Parity Error Response<br>位的状态如何，都会更新此状态位。|
|Signalled System Error|由已使用 ERR_FATAL 或 ERR_NONFATAL 报告了 Uncorrectable<br>Error 并且 Command 寄存器中的 SERR# Enable 位已设置的端口设置。|
|Received Master Abort|由收到具有 UR (Unsupported Request) 状态的完成的 Requester 设置。<br>这被认为类似于 PCI master abort，因为目标未"声明事务"。|
|Received Target Abort|由收到具有 CA (Completer Abort) 状态的完成的 Requester 设置。<br>这类似于 PCI target abort，因为目标有编程违规或内部错误状态。|
|Signaled Target Abort|由将请求（posted 或 non-posted）作为 Completer Abort 处理的 Completer 设置。<br>如果是非发布请求，则会发送具有 CA 完成状态的完成。|
|Master Data Parity Error|对于 Type 0 标头（例如 Endpoints），如果设置了 Command 寄存器中的 Parity Error Response 位<br>并且它发起了被毒化的请求或收到了被毒化的完成，则设置此位。<br>对于 Type 1 标头（例如 Switches 和 Root Ports），如果设置了 Command 寄存器中的 Parity Error Response 位<br>并且它发起了向上游移动的被毒化请求或收到了向下游移动的被毒化完成，则设置此位。|


## **基线错误处理 (Baseline Error Handling)**

基线功能需要使用 PCI Express Capability 结构。这些寄存器包括错误检测和处理字段，相对于仅使用 PCI 兼容错误处理所能实现的，它们提供了关于错误性质以及是否报告它的更细粒度。

图 15-15 在第 678 页说明了 PCI Express Capability 结构。这些寄存器中的一些提供以下支持：

- 启用/禁用错误报告（错误消息生成）

- 提供错误状态

- 提供链路训练状态和发起链路重新训练

_图 15-15：PCI Express Capability 结构_

**==> 图片 [336 x 315] 已省略 <==**


## **启用/禁用错误报告 (Enabling/Disabling Error Reporting)**

Device Control 寄存器允许软件启用四种错误事件的三种不同 Error Message 的生成，Device Status 寄存器允许软件查看检测到的错误。四种错误情况是：

**第 15 章：错误检测与处理**

- Correctable Errors

- Non-Fatal Errors

- Fatal Errors

- Unsupported Request Errors

请注意，此处识别的唯一特定错误是 Unsupported Request。虽然 Unsupported Request 在技术上是 Non-Fatal 错误的子集，并且在报告时甚至通过 ERR_NONFATAL 消息发出信号，但它有自己的启用和状态位。这是因为在系统枚举期间将发生 Unsupported Request（每当尝试从系统中实际不存在的函数读取配置空间时），但它们不得报告为错误。枚举软件可能具有非常有限的错误处理能力，如果需要停止并处理错误，它可能会失败。因此，软件不希望在 UR 情况下生成错误消息，但希望了解可能检测到的任何其他 Non-Fatal 错误。（有关枚举期间 Unsupported Request 的更多详细信息，请参见第 105 页的"发现 Function 的存在或不存在"部分。）

表 15-5 在第 679 页列出了每种错误类型及其关联的错误分类。

_表 15-5：错误的默认分类_

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Correctable|Receiver Error|Physical|
|Correctable|Bad TLP|Link|
|Correctable|Bad DLLP|Link|
|Correctable|Replay Number Rollover|Link|
|Correctable|Replay Timer Timeout|Link|
|Correctable|Advisory Non-Fatal Error|Transaction|
|Correctable|Corrected Internal Error||
|Correctable|Header Log Overflow|Transaction|
|Uncorrectable - Non Fatal|Poisoned TLP Received|Transaction|
|Uncorrectable - Non Fatal|ECRC Check Failed|Transaction|


_表 15-5：错误的默认分类（续）_

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Uncorrectable - Non Fatal|Unsupported Request|Transaction|
|Uncorrectable - Non Fatal|Completion Timeout|Transaction|
|Uncorrectable - Non Fatal|Completer Abort|Transaction|
|Uncorrectable - Non Fatal|Unexpected Completion|Transaction|
|Uncorrectable - Non Fatal|ACS Violation|Transaction|
|Uncorrectable - Non Fatal|MC Blocked TLP|Transaction|
|Uncorrectable - Non Fatal|AtomicOps Egress Blocked|Transaction|
|Uncorrectable - Non Fatal|TLP Prefix Blocked|Transaction|
|Uncorrectable - Fatal|Uncorrectable Internal Error<br>(optional)||
|Uncorrectable - Fatal|Surprise Down (optional)|Link|
|Uncorrectable - Fatal|Receiver Overflow (optional)|Transaction|
|Uncorrectable - Fatal|DLL Protocol Error|Link|
|Uncorrectable - Fatal|Receiver Overflow|Transaction|
|Uncorrectable - Fatal|Flow Control Protocol Error|Transaction|
|Uncorrectable - Fatal|Malformed TLP|Transaction|


**Device Control Register.** 在 Device Control 寄存器（如图 15-16 在第 681 页所示）中设置位可启用发送相应的 Error Message 以报告错误。Unsupported Request 错误被指定为 Non-Fatal 错误，并通过 Non-Fatal Error Message 报告，但仅当设置了 _UR Reporting Enable_ 位时。

为了使函数实际发送错误消息，需要在 Device Control 寄存器中设置相应的启用位，或对于 Fatal 和 Non-Fatal 错误，应设置 SERR# Enable。对于 Uncorrectable Errors，如果 Command Register 中的 SERR# Enable 位已设置或 Device Control 寄存器中相应的启用位已设置，则将发送适当的错误消息（ERR_FATAL 或 ERR_NONFATAL）。

**第 15 章：错误检测与处理**

对于 Correctable Errors，函数仅当 Device Control 寄存器中的 _Correctable Error Reporting Enable_ 位已设置时才会发送 ERR_COR 消息。无法通过 PCI 兼容机制控制启用 ERR_COR 消息，这很合理，因为在 PCI 中，没有可纠正错误的概念。

_图 15-16：与错误处理相关的 Device Control 寄存器字段_

**==> 图片 [357 x 231] 已省略 <==**


**Device Status Register.** 每当检测到与其分类关联的错误时，Device Status 寄存器（如图 15-17 在第 682 页所示）中的错误状态位即被设置，无论 Device Control 寄存器中错误报告启用位的设置如何。由于 Unsupported Request 错误被视为 Non-Fatal 错误，因此当这些错误发生时，_Non-Fatal Error Detected_ 状态位和 _Unsupported Request Detected_ 状态位都将被设置。与其他几个状态位一样，这些是"粘性的"（Sticky）（其值不会通过重置事件清除，因此即使需要重置才能使链路正常工作以读取状态，它们也可用于诊断问题）。

_图 15-17：与错误处理相关的 Device Status 寄存器位字段_

**==> 图片 [337 x 160] 已省略 <==**


## **根对错误消息的响应 (Root's Response to Error Message)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-15"></a>
## 14.15 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

15 11 10 9 8 7 6 5 4 3 2 1 0<br>Reserved 0 0 0 0 0<br>Interrupt Disable<br>Fast Back-to-back Enable *<br>SERR# Enable<br>Stepping Control *<br>Parity Error Response<br>VGA Palette Snoop Enable *<br>Mem Write & Invalidate Enable *<br>Special Cycles *<br>Bus Master Enable<br>Memory Space Enable<br>IO Space Enable<br>* Not used in PCIe, these must be set to zero<br>Table 15‐3: Error‐Related Fields in Command Register<br>Name Description<br>SERR# Enable Setting this bit enables sending ERR_FATAL and ERR_NONFATAL<br>error messages to the Root Complex. These are considered roughly<br>analogous to asserting the System Error (SERR#) signal in PCI.<br>For Type 1 headers (bridges), this bit controls the forwarding of<br>ERR_FATAL and ERR_NONFATAL error messages from the sec‐<br>ondary interface to the primary interface.<br>This field has no affect over ERR_COR messages.<br>_Table 15‐3: Error‐Related Fields in Command Register (Continued)_ 

|**Name**|**Description**|
|---|---|
|Parity Error<br>Response|Setting this bit enables logging of poisoned TLPs in the Master Data<br>Parity Error bit in the Status register.<br>Poisoned packets indicate bad data and are roughly analogous to a<br>PCI parity error.|


Figure 15‐14 on page 676 illustrates the Configuration Status register and the location of the error‐related bit fields. Table 15‐4 on page 677 defines the circum‐ stances under which each bit is set and the actions taken by the device when error reporting is enabled. 

_Figure 15‐14: Status Register in Configuration Header_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

_Table 15‐4: Error‐Related Fields in Status Register_ 

|**Error‐Related Bit**|**Description**|
|---|---|
|Detected Parity Error|Set by the port that receives a poisoned TLP. This status<br>bit is updated regardless of the state of the Parity Error<br>Response bit.|
|Signalled System Error|Set by a port that has reported an Uncorrectable Error<br>with ERR_FATAL or ERR_NONFATAL and the SERR#<br>enable bit in the Command register was set.|
|Received Master Abort|Set by a Requester that receives a Completion with sta‐<br>tus of UR (Unsupported Request). This is considered<br>analogous to a PCI master abort because the target did<br>not “claim the transaction”.|
|Received Target Abort|Set by a Requester that receives a Completion with sta‐<br>tus of CA (Completer Abort). This is analogous to a PCI<br>target abort in that the target has had a programming<br>violation or internal error condition.|
|Signaled Target Abort|Set by the Completer that handled a request (either<br>posted or non‐posted) as a Completer Abort. If it was a<br>non‐posted request, then a Completion with a Comple‐<br>tion Status of CA is sent.|
|Master Data Parity Error|For Type 0 headers (e.g., Endpoints), this bit is set if the<br>Parity Error Response bit in the Command register is<br>set AND it either initiates a poisoned request OR<br>receives a poisoned completion.<br>For Type 1 headers (e.g., Switches and Root Ports), this<br>bit is set if the Parity Error Response bit in the Com‐<br>mand register is set AND it either initiates a poisoned<br>request heading upstream OR receives a poisoned com‐<br>pletion heading downstream.|


## **Baseline Error Handling** 

The Baseline capability requires the use of the PCI Express Capability structure. These registers include error detection and handling fields that provide finer granularity regarding the nature of an error and whether to report it or not than what is possible with just PCI‐compatible error handling. 

Figure 15‐15 on page 678 illustrates the PCI Express Capability structure. Some of these registers provide support for: 

- Enabling/disabling error reporting (Error Message Generation) 

- Providing error status 

- Providing link training status and initiating link re‐training 

_Figure 15‐15: PCI Express Capability Structure_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Enabling/Disabling Error Reporting** 

The Device Control registers allow software to enable generation of three differ‐ ent Error Messages for four error events, and Device Status registers allow it to see which error has been detected. The four error cases are: 
- Correctable Errors 

- Non‐Fatal Errors 

- Fatal Errors 

- Unsupported Request Errors 

Note that the only specific error identified here is the Unsupported Request. Although an Unsupported Request is technically a subset of Non‐Fatal errors, and, when reported, is even signaled with an ERR_NONFATAL message, it has its own enable and status bits. Thatʹs because during system enumeration Unsupported Requests are going to happen (whenever an attempt it made to read config space from a Function that doesnʹt actually exist in the system) but they must not be reported as errors. The enumeration software may have very limited error‐handling capability and if it was required to stop and service an error it might fail. Therefore, the software doesnʹt want error messages gener‐ ated for the UR case during that time, but does want to know about any other Non‐Fatal errors that may be detected. (See the section titled “Discovering the Presence or Absence of a Function” on page 105 for more details on Unsup‐ ported Requests during enumeration.) 

Table 15‐5 on page 679 lists each error type and its associated error classifica‐ tion. 

_Table 15‐5: Default Classification of Errors_ 

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Correctable|Receiver Error|Physical|
|Correctable|Bad TLP|Link|
|Correctable|Bad DLLP|Link|
|Correctable|Replay Number Rollover|Link|
|Correctable|Replay Timer Timeout|Link|
|Correctable|Advisory Non‐Fatal Error|Transaction|
|Correctable|Corrected Internal Error||
|Correctable|Header Log Overflow|Transaction|
|Uncorrectable ‐ Non Fatal|Poisoned TLP Received|Transaction|
|Uncorrectable ‐ Non Fatal|ECRC Check Failed|Transaction|


_Table 15‐5: Default Classification of Errors (Continued)_ 

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Uncorrectable ‐ Non Fatal|Unsupported Request|Transaction|
|Uncorrectable ‐ Non Fatal|Completion Timeout|Transaction|
|Uncorrectable ‐ Non Fatal|Completer Abort|Transaction|
|Uncorrectable ‐ Non Fatal|Unexpected Completion|Transaction|
|Uncorrectable ‐ Non Fatal|ACS Violation|Transaction|
|Uncorrectable ‐ Non Fatal|MC Blocked TLP|Transaction|
|Uncorrectable ‐ Non Fatal|AtomicOps Egress Blocked|Transaction|
|Uncorrectable ‐ Non Fatal|TLP Prefix Blocked|Transaction|
|Uncorrectable ‐ Fatal|Uncorrectable Internal Error<br>(optional)||
|Uncorrectable ‐ Fatal|Surprise Down (optional)|Link|
|Uncorrectable ‐ Fatal|Receiver Overflow (optional)|Transaction|
|Uncorrectable ‐ Fatal|DLL Protocol Error|Link|
|Uncorrectable ‐ Fatal|Receiver Overflow|Transaction|
|Uncorrectable ‐ Fatal|Flow Control Protocol Error|Transaction|
|Uncorrectable ‐ Fatal|Malformed TLP|Transaction|


**Device Control Register.** Setting bits in the Device Control Register, shown in Figure 15‐16 on page 681, enables sending the corresponding Error Messages to report errors. Unsupported Request errors are specified as Non‐Fatal errors and are reported via a Non‐Fatal Error Message, but only when the _UR Reporting Enable_ bit is set. 

In order for a Function to actually send an error message, either the corre‐ sponding enable bit in the Device Control register needs to be set, or for Fatal and Non‐Fatal errors, the SERR# Enable should be set. For Uncorrect‐ able Errors, if either the SERR# Enable bit in the Command Register is set OR the corresponding enable bit in the Device Control register is set, the appropriate error message will be sent (ERR_FATAL or ERR_NONFATAL). 
For Correctable Errors, a Function will only send the ERR_COR message if the _Correctable Error Reporting Enable_ bit in the Device Control register is set. There is no control to enable ERR_COR messages from the PCI‐Compatible mechanisms, which makes sense because in PCI, there was no concept of correctable errors. 

_Figure 15‐16: Device Control Register Fields Related to Error Handling_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


**Device Status Register.** An error status bit is set in the Device Status reg‐ ister, shown in Figure 15‐17 on page 682, anytime an error associated with its classification is detected, regardless of the setting of the error reporting enable bits in the Device Control Register. Because Unsupported Request errors are considered Non‐Fatal Errors, when these errors occur both the _Non‐Fatal Error Detected_ status bit and the _Unsupported Request Detected_ sta‐ tus bit will be set. Like several other status bits, these are “Sticky” (their val‐ ues are not cleared by a reset event so they’ll be available for diagnosing problems even if a reset was needed to get the Link working well enough to read the status). 

_Figure 15‐17: Device Status Register Bit Fields Related to Error Handling_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Root’s Response to Error Message**

</td>
<td style="background-color:#e8e8e8">

当根收到 Error Message 时，它采取的操作部分由 Root Control 寄存器中的设置决定。图 15-18 描述了此寄存器并突出显示了指定是否应将收到的 Error Message 报告为 System Error 的三个字段。在一些基于 x86 的系统中，如果错误被启用以触发 System Error，则可能会发出 NMI (Non-Maskable Interrupt)。

通过标准寄存器无法配置报告 Error Message 的其他选项。最可能的情况是向处理器发出将调用错误处理程序 (Error Handler) 的中断，它可能会记录错误并尝试清除问题。

**第 15 章：错误检测与处理**

_图 15-18：Root Control 寄存器_

**==> 图片 [313 x 142] 已省略 <==**


## **链路错误 (Link Errors)**

链路故障通常在物理层检测到，并传送到数据链路层。对于下游设备，如果链路遇到 Fatal 错误且无法正常运行，则无法向主机报告错误。在这些情况下，错误必须由上游设备报告。如果软件可以将错误隔离到给定链路，则处理不可纠正错误（或防止将来发生不可纠正错误）的一个步骤是重新训练链路。Link Control 寄存器包括一个允许软件强制链路重新训练的位，如图 15-19 在第 684 页所示。如果这解决了问题，则操作会在很少停机的情况下恢复。

_图 15-19：Link Control 寄存器 — 强制链路重新训练_

**==> 图片 [297 x 260] 已省略 <==**


一旦请求重新训练后，软件可以轮询 Link Status 寄存器中的 _Link Training_ 位以查看训练何时完成。图 15-20 突出显示此状态位。当此位为 1b 时，链路仍处于重新训练过程中（或尚未开始重新训练）。一旦物理层报告链路处于活动状态（意味着训练过程已成功完成），硬件将清除此位。

**第 15 章：错误检测与处理**

_图 15-20：Link Status 寄存器中的链路训练状态_

**==> 图片 [360 x 167] 已省略 <==**


## **高级错误报告 (AER, Advanced Error Reporting)**

图 15-21 在第 686 页所示的高级错误报告结构允许更复杂的错误处理。这些寄存器提供以下一些附加功能：

- 更好地粒度地记录实际发生的错误类型

- 控制指定每种不可纠正错误类型的严重性

- 支持记录有错误的数据包的标头

- 标准化根的控制以中断形式报告收到的 Error Message

- 识别 PCIe 拓扑中错误的来源

- 能够屏蔽报告个别类型的错误

## **PCI Express Technology**

_图 15-21：Advanced Error Capability 结构_

|Root Ports &<br>Root Complex<br>Event Collectors<br>Functions<br>that support<br>TLP Prefixes|Root Error Command<br>Root Error Status<br>Uncorr. Error Source ID<br>Corr. Error Source ID<br>TLP Prefix Log Register<br>00h<br>04h<br>08h<br>0Ch<br>10h<br>14h<br>18h<br>1Ch<br>2Ch<br>30h<br>34h<br>38h<br>PCIe Extended CapabilityRegister<br>Uncorrectable Error Status Register<br>Uncorrectable Error Mask Register<br>Uncorrectable Error SeverityRegister<br>Correctable Error Status Register<br>Correctable Error Mask Register<br>Advanced Error Capability and Control Register<br>Header Log Register|
|---|---|


## **Advanced Error Capability and Control**

让我们从查看 Advanced Error Capability and Control 寄存器开始对 AER 的讨论。端到端 CRC (ECRC) 生成和检查需要 AER，并且此寄存器（如图 15-22 在第 687 页所示）报告

**第 15 章：错误检测与处理**

此设备是否支持 ECRC。如果支持，配置软件可以通过设置适当的位来启用（并强制）使用它。

此寄存器的低 5 位包含 First Error Pointer，由硬件在更新 Uncorrectable Error 状态位时设置。共有 32 个状态位，First Error Pointer 指示哪个未屏蔽的 Uncorrectable Error 是首先被检测到的，即当所有其他状态位仍为 0 时设置了哪个状态位。第一个错误是最有趣的，因为其他错误可能是由第一个错误引起的。

_图 15-22：Advanced Error Capability and Control 寄存器_

|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|_图 15-22：Advanced Error Capability and Control 寄存器_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||
|RsvdP<br>ECRC Check Enable(RWS)<br>ECRC Check Capable(RO)<br>ECRC Generation Enable(RWS)<br>ECRC Generation Capable(RO)<br>Multiple Header Recording Capable(RO)<br>Multiple Header Recording Enable(RWS<br>TLP Prefix Log Present(ROS)<br>31|||||First Error<br>Pointer (ROS)<br><br>)<br>0<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12|||||||||
||RsvdP||||||||||||First Error<br>Pointer (ROS)|
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||


从 2.1 规范版本开始，此功能得到增强，允许跟踪多个错误。因此，如果多个错误状态位已被设置和清除，那么其含义实际上更像"最旧错误指针"（Oldest Error Pointer）。当相应的状态位被软件清除时，指针由硬件更新，此时它指向下一个检测到的错误（有关不可纠正错误的列表，请参见第 691 页的图 15-25）。有趣的是，如果该错误已被多次检测，则下一个错误可能再次是相同的错误，其结果是更新的指针仍指示相同的值。

由于可以在 Uncorrectable Status 寄存器中记录多个错误，因此存储多个标头也将非常有帮助。硬件必须被设计为能够记录至少一个标头，但允许支持更多。如果支持，则 Multiple Header Recording Capable 位将被设置，并且 Multiple Header Recording Enable 位可用于启用存储多个标头。每当 First Error Pointer 指示未设置或未实现的状态位位置时，这意味着没有更多不可纠正错误需要处理。

此寄存器中的最后一位 TLP Prefix Log Present 指示 TLP Prefix Log 寄存器是否包含 First Error Pointer 指示的不可纠正错误的有效信息。

此寄存器中的字段以及其他 AER 寄存器具有各种特征，缩写如下：

- RO — Read Only，由硬件设置

- ROS — Read Only and Sticky（见下一节关于 sticky 位）

- RsvdP — Reserved and Preserved。这些位不得用于任何目的，但软件必须小心维护它们包含的任何值。

- RsvdZ — Reserved and Zero。不得用于任何目的，并且必须始终写入零的位。

- RWS — Readable, Writeable and Sticky

- • RW1CS — Readable, Write 1 to Clear, and Sticky

## **处理粘性位 (Handling Sticky Bits)**

几个 AER 寄存器字段采用 sticky 位，这意味着重置不会清除其内容。所有其他寄存器字段在重置时都强制为默认值，但这些不会。这是一个好主意，因为链路可能遇到无法在不复位的情况下清除的故障。如果问题出在失败链路的下游设备中，则在链路再次工作之前其寄存器内容不可用，重置将实现这一点。但是如果寄存器被重置清除，则信息将丢失。为了解决这个问题，sticky 位通过重置保持错误状态信息可用。具体来说，sticky 位将在 FLR (Function Level Reset)、热复位 (Hot Reset) 和热重启 (Warm Reset) 中存活下来，因为有电源使其保持活动状态。如果有像 Vaux 这样的辅助电源在主电源关闭时使其保持活动状态，则它们甚至可以在冷复位 (Cold Reset) 中存活。

## **高级可纠正错误处理 (Advanced Correctable Error Handling)**

高级错误报告提供了记录已检测到哪些特定可纠正错误的能力。这些错误可用于向主机系统发起 Correctable Error Message。尽管系统操作继续正常进行，但报告可纠正错误可能很有用，因为它允许系统软件查看哪些组件出现问题并预测它们将来是否可能完全失败。

**第 15 章：错误检测与处理**

## **高级可纠正错误状态 (Advanced Correctable Error Status)**

可纠正错误将自动在 Advanced Correctable Error Status 寄存器（如图 15-23 在第 689 页所示）中设置相应的位，无论该错误是否通过 Error Message 报告。这些位通过软件向位位置写入"1"来清除，因此被指定为 RW1CS。

_图 15-23：Advanced Correctable Error Status 寄存器_

|31|31||16|15|14|13|12|11|9|8|8|7|7|6|6|5||1|0|0||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||RsvdZ||||||RsvdZ|||||||||RsvdZ|||||
|||Header Log Overflow Status||||||||||||||||||||
|||Corrected Internal Error Status||||||||||||||||||||
|||Advisory Non-Fatal Error Status||||||||||||||||||||
|||Replay Timer Timeout Status||||||||||||||||||||
|||REPLAY_NUM Rollover Status||||||||||||||||||||
|||Bad DLLP Status||||||||||||||||||||
|||Bad TLP Status||||||||||||||||||||
|||Receiver Error Status||||||||||||||||||||
||||注意：所有位被指定为 RW1CS||||||||||||||||||||

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-16"></a>
## 14.16 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

When an Error Message is received by the Root, the action it takes is determined in part by the settings in the Root Control Register. Figure 15‐18 depicts this reg‐ ister and highlights the three fields that specify whether a received Error Mes‐ sage should be reported as System Error. In some x86‐based systems, it’s likely that an NMI (Non‐Maskable Interrupt) will be signaled if the error is enabled to trigger a System Error. 

Other options for reporting Error Messages are not configurable via standard registers. The most likely scenario is that an interrupt will be signaled to the processor that will call an Error Handler, which may log the error and attempt to clear the problem. 
_Figure 15‐18: Root Control Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Link Errors** 

Link failures are typically detected in the Physical Layer and communicated to the Data Link Layer. For a downstream device, if the link has incurred a Fatal error and is not operating correctly, it can’t report the error to the host. For these cases, the error must be reported by the upstream device. If software can isolate errors to a given link, one step in handling an uncorrectable error (or to prevent future uncorrectable errors) is to retrain the Link. The Link Control Register includes a bit that allows software to force the Link to retrain, as shown inFig‐ ure 15‐19 on page 684. If that solves the problem, operation resumes with little downtime. 

_Figure 15‐19: Link Control Register ‐ Force Link Retraining_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


Having once requested retraining, software can poll the _Link Training_ bit in the Link Status Register to see when training has completed. Figure 15‐20 high‐ lights this status bits. When this bit is 1b, the Link is still in the retraining pro‐ cess (or has yet to start retraining). Hardware will clear this bit once the Physical Layer reports the Link as active meaning the training process has completed successfully. 
_Figure 15‐20: Link Training Status in the Link Status Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Advanced Error Reporting (AER)** 

The Advanced Error Reporting Structure illustrated in Figure 15‐21 on page 686 allows for much more sophisticated error handling. These registers provide several additional features: 

- Better granularity in logging the actual type of error that occurred 

- Control to specify the severity of each uncorrectable error type 

- Support for logging the header of packets that had errors 

- Standardizing control for the Root to report received Error Messages with an interrupt 

- Identifying the source of the error in the PCIe topology 

- Ability to mask reporting individual types of errors 

## **PCI Express Technology** 

_Figure 15‐21: Advanced Error Capability Structure_ 

|Root Ports &<br>Root Complex<br>Event Collectors<br>Functions<br>that support<br>TLP Prefixes|Root Error Command<br>Root Error Status<br>Uncorr. Error Source ID<br>Corr. Error Source ID<br>TLP Prefix Log Register<br>00h<br>04h<br>08h<br>0Ch<br>10h<br>14h<br>18h<br>1Ch<br>2Ch<br>30h<br>34h<br>38h<br>PCIe Extended CapabilityRegister<br>Uncorrectable Error Status Register<br>Uncorrectable Error Mask Register<br>Uncorrectable Error SeverityRegister<br>Correctable Error Status Register<br>Correctable Error Mask Register<br>Advanced Error Capability and Control Register<br>Header Log Register|
|---|---|


## **Advanced Error Capability and Control** 

Let’s begin our discussion of AER by looking at the Advanced Error Capability and Control register. End‐to‐End CRC (ECRC) generation and checking requires AER, and this register, shown in Figure 15‐22 on page 687, reports 
whether this device supports it. If so, configuration software can enable (and force) its use by setting the appropriate bits. 

The five low‐order bits of this register contain the First Error Pointer, set by hardware when the Uncorrectable Error status bits are updated. There are 32 status bits and the First Error Pointer indicates which of the unmasked, Uncor‐ rectable Errors was detected first, meaning which status bit was set when all the other status bits were still 0. The first error is the most interesting because the others may have been caused by the first one. 

_Figure 15‐22: The Advanced Error Capability and Control Register_ 

|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||
|RsvdP<br>ECRC Check Enable(RWS)<br>ECRC Check Capable(RO)<br>ECRC Generation Enable(RWS)<br>ECRC Generation Capable(RO)<br>Multiple Header Recording Capable(RO)<br>Multiple Header Recording Enable(RWS<br>TLP Prefix Log Present(ROS)<br>31|||||First Error<br>Pointer (ROS)<br><br>)<br>0<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12|||||||||
||RsvdP||||||||||||First Error<br>Pointer (ROS)|
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||


Beginning with the 2.1 spec revision, this capability was enhanced to allow tracking multiple errors. For that reason, if multiple error status bits have been set and cleared, the meaning really becomes more like an “Oldest Error Pointer” instead. The pointer is updated by hardware when the corresponding status bit is cleared by software, at which time it points to whichever error was detected next (see Figure 15‐25 on page 691 for the list of uncorrectable errors). Interestingly, the next error may be the same one again if that error had been detected multiple times, with the result that the updated pointer still indicates the same value. 

Since multiple errors can be recorded in the Uncorrectable Status register, it would be very helpful to store multiple headers, too. Hardware must be designed to log at least one header, but is allowed to support more. If it does, the Multiple Header Recording Capable bit will be set and the Multiple Header Recording Enable bit can be used to enable storing more than one. Whenever the First Error Pointer indicates a status bit position that is not set or is not implemented, it means there are no more uncorrectable errors to service. 

The last bit in this register, TLP Prefix Log Present, indicates whether the TLP Prefix Log registers contain valid information for the uncorrectable error indi‐ cated by the First Error Pointer. 

The fields in this register and the other AER registers have various characteris‐ tics, which are abbreviated as follows: 

- RO — Read Only, set by hardware 

- ROS — Read Only and Sticky (see the next section on sticky bits) 

- RsvdP ‐ Reserved and Preserved. These bits must not be used for any pur‐ pose, but software must be careful to maintain whatever values they con‐ tain. 

- RsvdZ ‐ Reserved and Zero. Bits that must not be used for any purpose and must always be written to zeros. 

- RWS — Readable, Writeable and Sticky 

- • RW1CS — Readable, Write 1 to Clear, and Sticky 

## **Handling Sticky Bits** 

Several AER register fields employ sticky bits, which means that a reset won’t clear their contents. All other register fields are forced to default values on a reset, but these are not. This is a good idea because a Link may encounter a fail‐ ure that can’t be cleared without a reset. If the problem is in the downstream device of the failed Link, its register contents are unavailable until the Link is working again, which the reset will accomplish. But if the registers were cleared by the reset then the information is lost. To solve this problem, sticky bits keep error status information available through a reset. Specifically, sticky bits will survive an FLR (Function Level Reset), a Hot Reset, and a Warm Reset because power is available to keep them active. They may even survive a Cold Reset if a secondary power source like Vaux is available to keep them active when the main power is shut off. 

## **Advanced Correctable Error Handling** 

Advanced Error Reporting provides the ability to record which specific correct‐ able errors have been detected. These errors can be used to initiate a Correctable Error Message to the host system. Although system operation continues nor‐ mally, reporting correctable errors can be useful because it allows system soft‐ ware to see which components are having trouble and to predict whether they may fail completely in the future. 
## **Advanced Correctable Error Status** 

Correctable errors will automatically set the corresponding bit in the Advanced Correctable Error Status register, shown in Figure 15‐23 on page 689, regardless of whether the error is reported with an Error Message. These bits are cleared by software writing a “1” to the bit position, hence the designation RW1CS. 

_Figure 15‐23: Advanced Correctable Error Status Register_ 

|31|31||16|15|14|13|12|11|9|8|8|7|7|6|6|5||1|0|0||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||RsvdZ||||||RsvdZ|||||||||RsvdZ|||||
|||Header Log Overflow Status||||||||||||||||||||
|||Corrected Internal Error Status||||||||||||||||||||
|||Advisory Non-Fatal Error Status||||||||||||||||||||
|||Replay Timer Timeout Status||||||||||||||||||||
|||REPLAY_NUM Rollover Status||||||||||||||||||||
|||Bad DLLP Status||||||||||||||||||||
|||Bad TLP Status||||||||||||||||||||
|||Receiver Error Status||||||||||||||||||||
||||Note: all bits designated RW1CS|||||||||||||||||||

</td>
<td style="background-color:#e8e8e8">

- Receiver Error (optional) — 物理层检测到传入数据包中的错误。该数据包在物理层被丢弃，分配给它的任何缓冲区空间被释放，并通知链路层发生了接收错误。

- Bad TLP — 数据链路层检测到具有错误 LCRC、序列号乱序或错误置空的数据包。在每种情况下，链路层丢弃该数据包并向发送方报告 Nak DLLP，从而触发 TLP 重传。

- Bad DLLP — 数据链路层注意到传入的 DLLP 具有 16 位 CRC 错误，因此该数据包被丢弃。预期随后将出现相同类型的 DLLP 以补偿其包含的信息。

- REPLAY_NUM Rollover — 在数据链路层，一组 TLP 已连续四次发送未成功（没有 Ack），并且此计数器已回滚至零。硬件将自动重新训练链路以尝试清除故障状态，然后通过重放 Replay Buffer 的内容重新开始序列。

## **PCI Express Technology**

- Replay Timer Timeout — 在数据链路层，已发送的 TLP 在超时期限内未收到确认（Ack 或 Nak）。硬件自动重放所有未确认的 TLP，这意味着 Replay Buffer 中的所有数据包。

- Advisory Non-Fatal Error — 在对应的 Uncorrectable Error Status 寄存器中记录这些情况的检测（见第 670 页的"Advisory Non-Fatal Errors"）并在此作为可纠正错误。如果启用，它也可能生成 Correctable Error Message。

- Corrected Internal Error (optional) — 检测到设备内部的错误，但它已被纠正或绕过而不会导致不当行为。

- Header Log Overflow (optional) — 已达到可在标头日志中存储的最大标头数。如果未在 Advanced Error Capability and Control 寄存器中设置 Multiple Header Recording Enable 位，则该数字仅为 1。

## **高级可纠正错误屏蔽 (Advanced Correctable Error Masking)**

可纠正错误报告由 Device Control 寄存器中的 Correctable Error Enable 位集中控制，但也由 Correctable Mask 寄存器（如图 15-24 所示）单独控制。屏蔽位的默认状态是清零的，这意味着当检测到任何可纠正错误时，如果已启用（意味着已设置 Correctable Error Enable 位），则可以传递 ERR_COR 消息。但是，软件可以选择设置此屏蔽寄存器中的位以防止在检测到那些特定错误时发送消息。

_图 15-24：Advanced Correctable Error Mask 寄存器_

**==> 图片 [353 x 173] 已省略 <==**


**第 15 章：错误检测与处理**

## **高级不可纠正错误处理 (Advanced Uncorrectable Error Handling)**

对于不可纠正错误，AER 提供了跟踪已发生的特定错误的能力，控制是否应将其视为 Fatal 或 Non-Fatal，并选择它是否将导致向根发送 Uncorrectable Error Message。

## **高级不可纠正错误状态 (Advanced Uncorrectable Error Status)**

当发生不可纠正错误时，该寄存器中的相应位由硬件自动设置（请参见第 691 页的图 15-25），无论该错误是否将报告给根。如果发生多个错误，硬件将为每个错误设置相应的位，并将首先在 Advanced Error Capability and Control 寄存器的 First Error Pointer 字段中记录哪一个。也有可能在对第一个错误进行服务之前检测到同一错误的多个实例。符合 2.1 规范版本或更高版本的硬件将能够跟踪设计特定数量的此类情况。

_图 15-25：Advanced Uncorrectable Error Status 寄存器_

**==> 图片 [366 x 184] 已省略 <==**


以下列表从右到左描述了每个寄存器位：

- Undefined — 以前，该第一位表示物理层的链路训练失败，但该含义已在规范的 1.1 版本中删除

## **PCI Express Technology**

的规范。现在软件必须忽略此位中的任何值，但可以向其写入任何值。不再需要此信息，因为位 5（Surprise Down Error）现在在更广泛的含义中包含相同的信息：链路未在物理层通信。

- Data Link Protocol Errors — 由数据链路层协议错误引起，包括 Ack/Nak 重试机制。例如，发送方收到的 Ack 或 Nak 的序列号不对应于未确认的 TLP 或 ACKD_SEQ 编号。

- Surprise Down — 如果物理层报告 LinkUp = 0b（链路不再通信）意外地发生，则这将被视为错误，除非它是允许的异常。例如，如果已设置 Link Disable 位，则 LinkUp 将被清除是预期的，并且这种情况不会是错误。此位仅对 Downstream Ports 有效，因为如果链路不起作用，将无法从 Upstream Port 读取状态。

- Poisoned TLP — 看到的 TLP 设置了 EP 位。

- Flow Control Protocol Error (optional) — 与流控机制失败相关的错误。示例：接收方报告超过 2047 个数据信用。

- Completion Timeout — 在发送 non-posted 请求后，在所需的时间内未收到完成。

- Completer Abort (optional) — Completer 由于请求问题或 Completer 失败而无法完成请求。

- Unexpected Completion — Requester 收到与任何正在等待完成的请求都不匹配的完成。

- Receiver Overflow (optional) — 到达的 TLP 多于 Receive Buffer 容纳的空间，导致溢出错误。

- Malformed TLP — 由与收到的 TLP 标头相关的错误引起（请参见第 666 页的"Malformed TLP"）。

- ECRC Error (optional) — 由接收方的 ECRC 检查失败引起。

- • Unsupported Request Error — Completer 不支持该请求。请求格式正确且没有其他错误，但无法由 Completer 完成，可能是因为它对该设备是无效命令。

- ACS Violation — 在收到的 posted 或 non-posted 请求中看到访问控制错误。

- Uncorrectable Internal Error — 设备内部检测到的错误无法由硬件自身纠正或绕过。

- MC Blocked TLP — 指定用于多播路由的 TLP 被阻止。例如，Egress Port 可被编程为阻止任何到达的具有未翻译地址的 MC 命中（请参见第 896 页的"Routing Multicast TLPs"）。

- AtomicOp Egress Blocked — 路由元素的 Egress Port 可被编

**第 15 章：错误检测与处理**

 - 程为阻止 AtomicOps 被转发到不应看到它们的代理（请参见第 897 页的"AtomicOps"）。

- TLP Prefix Blocked Error — 路由元素的 Egress Port 可被编程为不转发包含 End-to-End TLP Prefix 的 TLP。如果他们然后看到其中一个，他们将丢弃 TLP 并报告此错误。有关详细信息，请参见第 899 页的"TPH (TLP Processing Hints)"。

回想一下，Capability and Control Register 中的 First Error Pointer 指示自指针上次更新以来哪个未屏蔽的不可纠正错误是第一个到达的。错误处理软件可以读取指针以找出首先要调查的错误。例如，如果指针值为 18d，则表示 Uncorrectable Status 寄存器中的位 18 位置是首先的，这是一个 Malformed TLP。一旦该错误已被处理，软件会向状态寄存器中的位 18 写入 1 以清除该事件，从而将 First Error Pointer 更新为下一个最近的错误

## **选择不可纠正错误的严重性 (Selecting Uncorrectable Error Severity)**

软件可以在此寄存器中选择是否应将不可纠正错误视为 Fatal，从而允许针对不同应用以不同方式处理错误。例如，Poisoned TLP 默认情况下将是 Non-Fatal 条件，并在某些情况下被视为 Advisory Non-Fatal 错误，如前所述。但是软件可以通过将其严重性位设置为 1 来将其升级为 Fatal，然后它将不再是建议性情况。默认严重性值在图 15-26 在第 694 页的各个位字段中说明（1 = Fatal，0 = Non-Fatal）。如果已启用且未屏蔽，那些被选为 Non-Fatal 的错误将导致向根复合体发送 ERR_NONFATAL 消息，那些被选为 Fatal 的错误将导致 ERR_FATAL 消息。

_图 15-26：Advanced Uncorrectable Error Severity 寄存器_

**==> 图片 [376 x 183] 已省略 <==**


## **不可纠正错误屏蔽 (Uncorrectable Error Masking)**

软件可以使用 Advanced Uncorrectable Error Mask 寄存器（如图 15-27 在第 694 页所示）屏蔽单个错误，因此它们不会导致错误消息被发送。默认情况是允许每种类型的错误消息（所有屏蔽位都被清除）。

_图 15-27：Advanced Uncorrectable Error Mask 寄存器_

**==> 图片 [369 x 187] 已省略 <==**


**第 15 章：错误检测与处理**

## **标头记录 (Header Logging)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-14-17"></a>
## 14.17 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Receiver Error (optional) — Physical Layer detected an error in the incom‐ ing packet. The packet is discarded at the Physical Layer, any buffer space allocated to it is released, and the Link Layer is informed that a receive error occurred. 

- Bad TLP — Data Link Layer detected a packet with a bad LCRC, an out‐of‐ sequence Sequence Number or an incorrectly nullified packet. In each case, the Link Layer discards the packet and reports a Nak DLLP to the transmit‐ ter, triggering a TLP replay. 

- Bad DLLP — Data Link Layer noticed an incoming DLLP had a 16‐bit CRC failure so the packet is dropped. A subsequent DLLP of the same type is expected to make up for the information it contained. 

- REPLAY_NUM Rollover — At the Data Link Layer, a set of TLPs have been sent without success (no Ack) four times in a row and this counter has rolled over back to zero. Hardware will automatically retrain the link in an attempt to clear the failure condition, then start the sequence again by replaying the contents of the Replay Buffer. 

## **PCI Express Technology** 

- Replay Timer Timeout — At the Data Link Layer, transmitted TLPs have not received an acknowledgement (Ack or Nak) within the timeout period. Hardware automatically replays all unacknowledged TLPs, meaning all packets in the Replay Buffer. 

- Advisory Non‐Fatal Error — Detection of these cases (see “Advisory Non‐ Fatal Errors” on page 670) is logged in the corresponding Uncorrectable Error Status register and as a correctable error here. It may also generate a Correctable Error Message, if enabled. 

- Corrected Internal Error (optional) — An error internal to the device was detected, but it was corrected or worked around without causing improper behavior. 

- Header Log Overflow (optional) — The maximum number of headers that can be stored in the header log has been reached. The number is just one if the Multiple Header Recording Enable bit is not set in the Advanced Error Capability and Control register. 

## **Advanced Correctable Error Masking** 

Correctable Error reporting is controlled collectively by the Correctable Error Enable bit in the Device Control register, but also individually by the Correct‐ able Mask register, illustrated in Figure 15‐24. The default state of the mask bits is cleared, meaning an ERR_COR message can be delivered when any correct‐ able errors are detected if they’ve been enabled (meaning the Correctable Error Enable bit is set). However, software may choose to set bits in this mask register to prevent a message from being sent when those specific errors are detected. 

_Figure 15‐24: Advanced Correctable Error Mask Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

## **Advanced Uncorrectable Error Handling** 

For uncorrectable errors, AER provides the ability to track which specific error has occurred, control whether it should be considered Fatal or Non‐Fatal, and choose whether it will result in an Uncorrectable Error Message being sent to the Root. 

## **Advanced Uncorrectable Error Status** 

When an uncorrectable error occurs, the corresponding bit in this register is automatically set by hardware (see Figure 15‐25 on page 691) regardless of whether the error will be reported to the Root. If multiple errors occur, hard‐ ware will set the corresponding bit for each error and will record which one was first in the First Error Pointer field of the Advanced Error Capability and Con‐ trol register. It may even happen that multiple instances of the same error are detected before the first one can be serviced. Hardware that is compliant with the 2.1 spec revision or later will be able to keep track of a design‐specific num‐ ber of those cases. 

_Figure 15‐25: Advanced Uncorrectable Error Status Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


The following list describes each of the register bits from right to left: 

- Undefined — Previously, this first bit represented a link training failure at the Physical Layer, but that meaning was removed with the 1.1 revision of 

## **PCI Express Technology** 

the spec. Software must now ignore any value in this bit but may write any value to it. This information was no longer needed because bit 5, Surprise Down Error, now includes the same information in a broader meaning: the Link is not communicating at the Physical Layer. 

- Data Link Protocol Errors — Caused by Data Link Layer protocol errors including the Ack/Nak retry mechanism. For example, a transmitter receives an Ack or Nak whose sequence number doesn’t correspond to an unacknowledged TLP or to the ACKD_SEQ number. 

- Surprise Down — If the Physical Layer reports LinkUp = 0b (Link is no longer communicating) unexpectedly, this will be seen as an error unless it was an allowed exception. For example, if the Link Disable bit has already been set, then it’s expected that LinkUp will be cleared and this condition won’t be an error. This bit is only valid for Downstream Ports, which makes sense because it won’t be possible to read status from an Upstream Port if the Link isn’t working. 

- Poisoned TLP — TLP was seen that had the EP bit set. 

- Flow Control Protocol Error (optional) — Errors associated with failures of the Flow Control mechanism. Example: receiver reports more than 2047 data credits. 

- Completion Timeout — A Completion is not received within the required amount of time after a non‐posted request was sent. 

- Completer Abort (optional) — Completer cannot fulfill a Request due to problems with the Request or failure of the Completer. 

- Unexpected Completion — Requester receives a Completion that doesn’t match any Requests that are awaiting a Completion. 

- Receiver Overflow (optional) — More TLPs have arrived than the Receive Buffer had room to accept, resulting in an overflow error. 

- Malformed TLP — Caused by errors associated with a received TLP header (see “Malformed TLP” on page 666). 

- ECRC Error (optional) — Caused by an ECRC check failure at the Receiver. 

- • Unsupported Request Error — Completer does not support the Request. Request is correctly formed and had no other errors, but cannot be fulfilled by the Completer, perhaps because it’s an invalid command for this device. 

- ACS Violation — Access control error was seen in a received posted or non‐ posted request. 

- Uncorrectable Internal Error — An internal error detected in the device could not be corrected or worked around by the hardware itself. 

- MC Blocked TLP — A TLP designated for Multi‐Cast routing was blocked. For example, an Egress Port can be programmed to block any MC hits that arrive with untranslated addresses (see “Routing Multicast TLPs” on page 896). 

- AtomicOp Egress Blocked — Egress Ports of routing elements can be pro‐ 
 - grammed to block AtomicOps from being forwarded to agents that shouldn’t see them (see “AtomicOps” on page 897). 

- TLP Prefix Blocked Error — Egress Ports of routing elements can be pro‐ grammed not to forward TLPs containing End‐to‐End TLP Prefixes. If they then see one, they’ll drop the TLP and report this error. For more on this, see “TPH (TLP Processing Hints)” on page 899. 

Recall that the First Error Pointer in the Capability and Control Register indi‐ cates which unmasked uncorrectable error was the first to arrive since the pointer was last updated. Error handling software can read the pointer to find out which error to investigate first. As an example, if the pointer value is 18d, that means bit position 18 in the Uncorrectable Status register was first, which is a Malformed TLP. Once that error has been serviced, software writes a one to bit 18 in the status register to clear that event, which updates the First Error Pointer to the next‐most‐recent error 

## **Selecting Uncorrectable Error Severity** 

Software can select whether or not uncorrectable errors should be considered Fatal in this register, allowing errors to be treated differently for different appli‐ cations. For example, a Poisoned TLP will be a Non‐Fatal condition by default, and is treated as an Advisory Non‐Fatal error in some cases, as discussed ear‐ lier. But software can escalate it to Fatal by setting its severity bit to one and then it will no longer be an advisory case. The default severity values are illus‐ trated in the individual bit fields of Figure 15‐26 on page 694 (1 = Fatal, 0 = Non‐ Fatal). If they are enabled and not masked, those errors selected as Non‐Fatal will cause an ERR_NONFATAL message to be sent to the Root Complex, and those selected as Fatal will cause an ERR_FATAL message. 

_Figure 15‐26: Advanced Uncorrectable Error Severity Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Uncorrectable Error Masking** 

Software can mask out individual errors so they won’t cause an error message to be sent by using the Advanced Uncorrectable Error Mask register, shown in Figure 15‐27 on page 694. The default condition is to allow Error Messages for each type of error (all mask bits are cleared). 

_Figure 15‐27: Advanced Uncorrectable Error Mask Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>

## **Header Logging**

</td>
<td style="background-color:#e8e8e8">

Advanced Error Reporting 结构的 4DW 部分用于存储发生未屏蔽、不可纠正错误的收到 TLP 的标头。由于当物理层或数据链路层未看到 TLP 出现问题时，标头记录才有用，因此可能性数量有限，如表 15-6 在第 695 页所示。如前所述，当实现可选的 AER 功能时，硬件必须能够记录至少一个标头，尽管它可能支持记录更多。

当 First Error Pointer 有效时，标头日志包含相应错误的标头（如果它是由传入的 TLP 引起的）。更新 Uncorrectable Error Status 寄存器将导致 Header Log 寄存器也按顺序更新为下一个值，这意味着下一个被检测到的不可纠正错误。由于硬件只能跟踪有限数量的标头，因此软件必须足够快地处理不可纠正的错误以避免耗尽标头空间。如果达到标头日志容量，则这本身就是一个可纠正的错误（Header Log Overflow）。如果超出支持的日志寄存器数量，或者如果未设置 Multiple Header Log Enable 位且在检测到新的不可纠正错误时 First Error Pointer 已有效，则可能会发生这种情况。

_表 15-6：可以使用 Header Log 寄存器的错误_

|**错误名称**|**默认分类**|
|---|---|
|Poisoned TLP Received|Uncorrectable - NonFatal|
|ECRC Check Failed|Uncorrectable - NonFatal|
|Unsupported Request|Uncorrectable - NonFatal|
|Completer Abort|Uncorrectable - NonFatal|
|Unexpected Completion|Uncorrectable - NonFatal|
|ACS Violation|Uncorrectable - NonFatal|
|Malformed TLP|Uncorrectable - Fatal|


## **根复合体错误跟踪和报告 (Root Complex Error Tracking and Reporting)**

根复合体是 PCIe 拓扑中设备的所有错误消息的目标。根收到的错误会更新状态寄存器，并在启用时可能报告给主机系统。

## **根复合体错误状态寄存器 (Root Complex Error Status Registers)**

当根收到错误消息时，它会在 Root Error Status 寄存器（如图 15-28 在第 697 页所示）中设置状态位。该寄存器指示收到的错误类型以及是否已收到相同类型的多个错误。请注意，在 Root Port 本身检测到的错误也会设置这些状态位，就好像该端口已向自身发送了错误消息一样。状态位为：

- ERR_COR Received

- Multiple ERR_COR Received — 收到 ERR_COR 消息，或在 ERR_COR Received 位已设置时检测到未屏蔽的根端口可纠正错误。

- ERR_FATAL/NONFATAL Received

- Multiple ERR_FATAL/NONFATAL Received — 收到 ERR_FATAL 或 ERR_NONFATAL 消息，或在 ERR_FATAL/NONFATAL Received 位已设置时检测到未屏蔽的根端口不可纠正错误。

系统可能为 Correctable、Non-Fatal 和 Fatal 错误实现单独的软件错误处理程序，因此该寄存器包括用于区分不可纠正错误是 Fatal 还是 Non-Fatal 的位：

- 如果收到的第一个 Uncorrectable Error Message 是 Fatal，则"First Uncorrectable Fatal"位也会与"Fatal Error Message Received"位一起设置。

- 如果收到的第一个 Uncorrectable Error Message 是 Non-Fatal，则设置"Non-fatal Error Message Received"位。（如果随后的 Uncorrectable Error 是 Fatal，则将设置"Fatal Error Message Received"位，但由于"First Uncorrectable Fatal"保持清零，软件知道第一个 Uncorrectable Error 是 Non-Fatal）。

**第 15 章：错误检测与处理**

_图 15-28：Root Error Status 寄存器_

**==> 图片 [327 x 143] 已省略 <==**


最后，可能已（在 Root Error Command 寄存器中）启用中断以作为检测到这些事件之一的结果发送到主机系统。为了支持这一点，此寄存器中的 5 位 Interrupt Message Number 提供了要使用的 MSI 或 MSI-X 向量号，共有 32 种可能。对于 MSI，该号是距基本数据模式的偏移。对于 MSI-X，它表示要使用的表条目，并且必须是前 32 个中的一个，即使代理支持超过 32 个。此只读值由硬件设置，并且必须在分配给设备的 MSI 消息数更改时自动更新。

## **Advanced Source ID 寄存器 (Advanced Source ID Register)**

软件错误处理程序可能需要读取和清除检测和报告错误的设备中的状态寄存器。为此，错误消息包含报告该错误类型的第一个设备的 ID（Bus:Dev:Func）。如果尚未设置 ERR_FATAL/NONFATAL 位（意味着这是第一个），则 Source ID 寄存器从消息中为传入的 ERR_FATAL/NONFATAL 消息捕获该 ID。类似地，第一个收到的 ERR_COR 消息的 Source ID 也被捕获，如图 15-29 在第 698 页所示。

_图 15-29：Advanced Source ID 寄存器_

**==> 图片 [327 x 47] 已省略 <==**


## **根错误命令寄存器 (Root Error Command Register)**

根复合体对三种错误类别中的每一种都有单独的启用位，以控制该错误类型是否将生成中断以调用错误处理程序，如图 15-30 在第 698 页所示。生成的中断将是 MSI 或 MSI-X，如"根复合体错误状态寄存器"中第 696 页所述。一旦收到中断，被调用的错误处理程序可能首先读取根复合体状态寄存器以确定错误的性质，然后转到错误的源 BDF 读取标准状态寄存器以及可能的设备特定寄存器以确定发生了什么以及应如何处理。

_图 15-30：Advanced Root Error Command 寄存器_

**==> 图片 [332 x 93] 已省略 <==**


## **错误记录和报告摘要 (Summary of Error Logging and Reporting)**

规范包括第 699 页的图 15-31 中的流程图，显示了函数在检测到错误时采取的操作。虚线内的部分突出显示了存在可选 AER 功能结构时添加的项目。

**第 15 章：错误检测与处理**

_图 15-31：函数内错误处理流程图_

**==> 图片 [327 x 391] 已省略 <==**


## **软件错误调查的示例流程 (Example Flow of Software Error Investigation)**

现在我们已经了解了 PCIe 中定义的用于检测、记录和报告错误的所有机制，值得看看软件将如何找到并使用此信息来确定如何处理报告的错误。

## **PCI Express Technology**

本示例将假设发起函数及其上游根端口都支持 AER。如果没有 AER 支持，则用于错误记录的标准寄存器非常有限。

本示例中使用的系统如图 15-32 在第 701 页所示。根端口的 BDF 为 0:28:0，并已启用以在收到 ERR_FATAL 或 ERR_NONFATAL 消息时生成中断。我们将按照错误处理软件将采取的步骤来确定已发生什么错误、在哪里发生以及在哪些数据包中检测到它们。

由于来自根端口 0:28:0 的中断，已调用错误处理软件。下面的步骤只是一个示例，但说明了错误处理软件收集错误信息的过程。

1. 软件根据使用的中断向量知道调用错误处理程序的是根端口 0:28:0。由于使用 MSI 或 MSI-X 中断来报告错误，因此每个根端口将具有自己唯一的一组中断向量。

2. 错误处理程序读取 0:28:0 上 AER 结构的 Root Error Status 寄存器，以确定根端口已收到哪些类型的错误消息。该寄存器中的值为 0800_007Ch，表示此根端口未收到任何 ERR_COR 消息，但已收到 ERR_FATAL 和 ERR_NONFATAL 消息，并且它收到的第一个不可纠正的错误消息是 ERR_FATAL。

3. 下一步是确定此根端口下的哪个 BDF 发送了第一个不可纠正错误。然后，软件读取根端口的 Source ID 寄存器，并找到值 0500_0000h，这表示第一个不可纠正错误的源 BDF 为 5:0:0。

4. 现在软件知道根端口 0:28:0 收到的第一个不可纠正错误是从 BDF 5:0:0 发起的 Fatal 错误。有了此信息，软件然后去读取 BDF 5:0:0 上的 Uncorrectable Error Status 寄存器，以查看在该 BDF 上已发生哪些特定的不可纠正错误。从该读取返回的值是 0004_1000h，这意味着此 BDF 已检测到至少一个 Malformed TLP 和至少一个 Poisoned TLP。但错误处理程序真正关心的是哪个先发生，因为那就是要首先处理的。

5. 为了确定多个不可纠正错误中哪个先发生，软件然后读取 5:0:0 的 Advanced Error Capability and Control 寄存器，并找到值 0000_0012h，其 First Error Pointer 值为 12h，表示第一个不可纠正错误是 Malformed TLP（位 18d），而不是 Poisoned TLP（位 12d）。

**第 15 章：错误检测与处理**

_图 15-32：错误调查示例系统_

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---
<a id="sec-14-18"></a>
## 14.18 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

A 4DW portion of the Advanced Error Reporting structure is used for storing the header of a received TLP that incurs an unmasked, uncorrectable error. Since header logging is only useful when a TLP has been received with a prob‐ lem that wasn’t seen by the Physical or Data Link Layers, the number of possi‐ bilities is limited, as shown in Table 15‐6 on page 695. As mentioned earlier, when the optional AER capability is implemented, hardware is required to be able to log at least one header, though it may support logging more. 

When the First Error Pointer is valid, the header log contains the header for the corresponding error if it was caused by an incoming TLP. Updating the Uncor‐ rectable Error Status register will cause the Header Log registers to also update to the next value in sequence, meaning the next uncorrectable error that was detected. Since the hardware can only track a limited number of headers, it’s important that software service uncorrectable errors quickly enough to avoid running out of header space. If the header log capacity is reached, that’s a cor‐ rectable error in itself (Header Log Overflow). This could happen if the number of supported log registers is exceeded or if the Multiple Header Log Enable bit is not set and the First Error Pointer is already valid when a new uncorrectable error is detected. 

_Table 15‐6: Errors That Can Use Header Log Registers_ 

|**Name of Error**|**Default Classification**|
|---|---|
|Poisoned TLP Received|Uncorrectable ‐ NonFatal|
|ECRC Check Failed|Uncorrectable ‐ NonFatal|
|Unsupported Request|Uncorrectable ‐ NonFatal|
|Completer Abort|Uncorrectable ‐ NonFatal|
|Unexpected Completion|Uncorrectable ‐ NonFatal|
|ACS Violation|Uncorrectable ‐ NonFatal|
|Malformed TLP|Uncorrectable ‐ Fatal|


## **Root Complex Error Tracking and Reporting** 

The Root Complex is the target of all error Messages from devices in a PCIe topology. Errors received by the Root update status registers and may be reported to the host system if enabled to do so. 

## **Root Complex Error Status Registers** 

When the Root receives an error Message, it sets status bits within the Root Error Status register (Figure 15‐28 on page 697). This register indicates the type of error received and whether multiple errors of the same type have been received. Note that an error detected in the Root Port itself will set these status bits, too, as if the port had sent itself an error message. The status bits are: 

- ERR_COR Received 

- Multiple ERR_COR Received ‐ received an ERR_COR message, or detected an unmasked Root Port correctable error with the ERR_COR Received bit already set. 

- ERR_FATAL/NONFATAL Received 

- Multiple ERR_FATAL/NONFATAL Received ‐ received an ERR_FATAL or ERR_NONFATAL message or detected an unmasked Root Port uncorrect‐ able error with the ERR_FATAL/NONFATAL Received bit already set. 

It’s possible for a system to implement separate software error handlers for Cor‐ rectable, Non‐Fatal, and Fatal errors, so this register includes bits to differenti‐ ate whether Uncorrectable errors were Fatal or Non‐Fatal: 

- If the first Uncorrectable Error Message received is Fatal the “First Uncor‐ rectable Fatal” bit is also set along with the “Fatal Error Message Received” bit. 

- If the first Uncorrectable Error Message received is Non‐Fatal the “Non‐ fatal Error Message Received” bit is set. (If a subsequent Uncorrectable Error is Fatal, the “Fatal Error Message Received” bit will be set, but because the “First Uncorrectable Fatal” remains cleared, software knows that the first Uncorrectable Error was Non‐Fatal). 
_Figure 15‐28: Root Error Status Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0685_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


Finally, an interrupt may have been enabled (in the Root Error Command regis‐ ter) to be sent to the host system as a result of detecting one of these events. To support that, the 5‐bit Interrupt Message Number in this register supplies the MSI or MSI‐X vector number to be used, and there are 32 possibilities. For MSI, the number is the offset from the base data pattern. For MSI‐X, it represents the table entry to be used, and must be one of the first 32 even if the agent supports more than 32. This read‐only value is set by hardware and must be automati‐ cally updated if the number of MSI messages assigned to the device changes. 

## **Advanced Source ID Register** 

Software error handlers may need to read and clear status registers in the device that detected and reported the error. To facilitate this, the error Messages contain the ID (Bus:Dev:Func) of the first device reporting that error type. The Source ID register captures that ID from the Message for an incoming ERR_FATAL/NONFATAL message if the ERR_FATAL/NONFATAL bit isn’t already set (meaning this is the first one). Similarly, the Source ID of the first received ERR_COR message is captured, too, as shown in Figure 15‐29 on page 698. 

_Figure 15‐29: Advanced Source ID Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0687_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Root Error Command Register** 

The Root Complex has separate enable bits for each of the three error categories to control whether that error type will generate an interrupt to call an error han‐ dler as shown in Figure 15‐30 on page 698. The interrupt that is generate will either be an MSI or MSI‐X as discussed in “Root Complex Error Status Regis‐ ters” on page 696. Once the interrupt is received, the called error handler would probably first read the Root Complex status registers to determine the nature of the error, and then go down to the source BDF of the error to read standard sta‐ tus register as well as possibly device‐specific registers to determine what occurred and how it should be handled. 

_Figure 15‐30: Advanced Root Error Command Register_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0688_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Summary of Error Logging and Reporting** 

The spec includes the flow chart in Figure 15‐31 on page 699 that shows the actions taken by a Function when an error is detected. The part inside the dashed line highlights the items that are added when the optional AER capabil‐ ity structure is present. 
_Figure 15‐31: Flow Chart of Error Handling Within a Function_ 

<img src="figures/chapter_14_Link_Initialization_Training/embedded/page0684_img1.png" alt="Figure 14‐31: Equalization Process: Initiating Phase 2" width="700">

<br>


## **Example Flow of Software Error Investigation** 

Now that we know all the mechanisms defined in PCIe for detecting, logging and reporting errors, it is worthwhile to look at how software would find and use this information to determine how to handle a reported error. 

## **PCI Express Technology** 

This example is going to assume that both the originating Function as well as the Root Port upstream of it both support AER. Without AER support, the stan‐ dardized registers for error logging are very limited. 

The system used for this example is shown in Figure 15‐32 on page 701. The Root Port has a BDF of 0:28:0 and was enabled to generate an interrupt when it receives either an ERR_FATAL or ERR_NONFATAL message. We are going to follow the steps of error handling software would take to determine what errors have occurred, where they occurred and what packets were they detected in. 

The error handling software has been called because of an interrupt from Root Port 0:28:0. The steps below are just an example, but illustrate the process of error handling software gathering error information. 

1. Software knows it was Root Port 0:28:0 that called the error handler based on the interrupt vector used. Since MSI or MSI‐X interrupts are used to report errors, each Root Port will have their own unique set of interrupt vectors. 

2. The error handler reads the Root Error Status register of the AER structure on 0:28:0 to determine what types of error messages have been received by the Root Port. The value in that register is 0800_007Ch which indicates that this Root Port has not received any ERR_COR messages, but has received both ERR_FATAL and ERR_NONFATAL messages and the first uncorrect‐ able error message that it received was an ERR_FATAL. 

3. The next step is to determine which BDF beneath this Root Port sent the first uncorrectable error. Software then reads the Source ID register of the Root Port and finds the value 0500_0000h, which indicates that the source BDF of the first uncorrectable error was 5:0:0. 

4. Now software knows that the first uncorrectable error received by Root Port 0:28:0 was a Fatal error that originated from BDF 5:0:0. With this information, software then goes and reads the Uncorrectable Error Status register on BDF 5:0:0 to see which specific uncorrectable errors have occurred on that BDF. The value returned from that read is 0004_1000h which means that this BDF has detected at least one Malformed TLP and at least one Poi‐ soned TLP. But what the error handler really cares about is which one occurred first, because that’s the one that should be handled first. 

5. To determine which of the multiple uncorrectable errors occurred first, soft‐ ware then reads the Advanced Error Capability and Control register of 5:0:0 and finds the value 0000_0012h which has a First Error Pointer value of 12h meaning that the first uncorrectable error was a Malformed TLP (bit 18d) and not the Poisoned TLP (bit 12d). 
_Figure 15‐32: Error Investigation Example System_

</td>
<td style="background-color:#e8e8e8">

**==> 图片 [379 x 417] 已省略 <==**


6. 现在错误处理程序知道 5:0:0 处的第一个不可纠正错误是 Malformed TLP，它可以检查 Header Log 寄存器以查看格式错误的数据包的标头，因为这是记录标头的错误之一。在读取 Header Log 寄存器时，它找到以下四个双字：

 - 6000_8080h — 1st DW

 - 0000_04FFh — 2nd DW

 - FB80_1000h — 3rd DW

 - 0000_0001h — 4th DW

7. 对这 4 个 DW 的评估将格式错误的数据包标识为：Memory Write，4DW 标头，TC=0，TD=1，EP=0，Attr=0，AT=0，Length=80h（128 DW 或 512 字节），Requester ID=0:0:0，Tag=4，Byte Enables=FFh，Address=1_FB80_1000h。数据包的标头看起来都是正确的，并且每个字段都使用有效的编码，因此软件必须深入挖掘以发现为什么它被视为 Malformed TLP。在本例中，假设在进一步检查 5:0:0 上的配置空间后，软件发现为此函数启用的 Max Payload Size 为 256 字节，但此数据包包含 512 字节。这是目标设备（在本例中为 5:0:0）将视为 Malformed TLP 的情况。

如果您想验证您对此错误调查过程的了解，请继续评估在 4:0:0 上检测到的第一个不可纠正错误是什么。

如果您喜欢冒险并希望在真实系统（例如您的台式机或笔记本电脑）上检查此类信息，您可以通过下载 MindShare Arbor 软件（www.mindshare.com/arbor）来执行此操作。您可以在基于 x86 的计算机上运行它，它将扫描您的系统并显示每个可见的 PCI 兼容设备，并解码其配置空间以方便解释。

## _**16 电源管理 (Power Management)**_

## **上一章 (The Previous Chapter)**

上一章讨论了 PCIe 端口或链路上发生的错误类型、如何检测、报告以及处理它们的选项。由于 PCIe 旨在与 PCI 错误报告向后兼容，因此 PCI 错误处理方法作为背景信息也包含在内。然后我们重点介绍了 PCIe 对可纠正、非致命和致命错误的错误处理。

## **本章 (This Chapter)**

本章提供了系统电源管理讨论的整体背景以及 PCIe 电源管理的详细描述，该管理兼容 _PCI Bus PM Interface Spec_ 和 _Advanced Configuration and Power Interface_ (ACPI)。PCIe 定义了对 PCI-PM 规范的扩展，主要侧重于链路电源和事件管理。还提供了 OnNow 计划、ACPI 和 Windows 操作系统参与的概述。

## **下一章 (The Next Chapter)**

下一章详细介绍了 PCIe 函数生成中断的不同方式。旧的 PCI 模型使用引脚执行此操作，但在串行模型中边带信号是不希望的，因此支持带内 MSI (Message-Signaled Interrupts) 机制是强制性的。PCI INTx# 引脚操作仍可被仿真以支持使用 PCIe INTx 消息的传统系统。PCI 旧版 INTx# 方法和较新版本的 MSI/MSI-X 都被描述。

## **介绍 (Introduction)**

PCI Express 电源管理 (PM) 定义了四个主要支持领域：

- **PCI 兼容 PM** . PCIe 电源管理与 PCI-PM 和 ACPI 规范在硬件和软件上兼容。此支持要求所有函数都包含 PCI Power Management Capability 寄存器，允许软件通过使用 Configuration 请求在软件控制下在 PM 状态之间转换函数。这在 2.1 规范版本中通过添加 Dynamic Power Allocation (DPA) 进行了修改，这是另一组寄存器，为 D0 电源状态添加了几个子状态，为软件提供了更细粒度的 PM 机制。

- **Native PCIe Extensions** . 这些定义了链路的自主、基于硬件的活动状态电源管理 (ASPM)，以及唤醒系统的机制、报告电源管理事件 (PME) 的消息事务，以及计算和报告低功耗到活动状态延迟的方法。

- **Bandwidth Management.** 2.1 规范版本增加了硬件自动改变链路宽度或链路数据速率或两者兼而有之的能力以改善功耗。这允许在需要时实现高性能，并在性能较低可接受时保持低功耗使用。即使带宽管理被视为电源管理主题，我们也会在"链路初始化与训练"章节的第 618 页的"动态带宽变化"部分中描述此功能，因为它涉及 LTSSM。

- **Event Timing Optimization.** 外围设备发起总线主事件或中断而不考虑系统电源状态会导致其他系统组件保持高功率状态以为它们提供服务，从而导致功耗高于必要的水平。这种缺陷在 2.1 规范中通过添加两种新机制得到了纠正：Optimized Buffer Flush and Fill (OBFF)，它允许系统通知外围设备当前的系统电源状态；以及 Latency Tolerance Reporting (LTR)，它允许设备报告它们此时可以容忍的服务延迟。

本章分为几个主要部分：

1. 第一部分是关于电源管理的入门知识，并涵盖了系统软件在控制电源管理功能方面的作用。本讨论仅考虑 Windows 操作系统的观点，因为它是 PC 最常见的观点，不描述其他操作系统。

**第 16 章：电源管理**

2. 第二部分"函数电源管理"在第 713 页讨论了使用 PCI-PM 能力寄存器将函数置于其低功耗设备状态的方法。请注意，某些寄存器定义被 PCIe 函数修改或未使用。

3. "活动状态电源管理 (ASPM)"在第 735 页描述了基于硬件的自主链路电源管理。软件确定要为环境启用哪个 ASPM 级别，可能通过读取将为该函数产生的恢复延迟值，但之后电源转换的时序由硬件控制。软件不控制转换，并且无法看到链路处于哪个电源状态。

4. "软件发起的链路电源管理"在第 760 页讨论了当软件更改设备的电源状态时强制执行的链路电源管理。

5. "链路唤醒协议和 PME 生成"在第 768 页描述了设备如何请求软件将它们返回到活动状态以便它们可以对事件进行服务。当设备的电源被移除时，如果要监视事件并向系统发出唤醒信号以恢复电源并重新激活链路，则必须存在辅助电源。

6. 最后，描述事件计时功能，包括 OBFF 和 LTR。

## **电源管理入门 (Power Management Primer)**

_PCI Bus PM Interface spec_ 描述了 PCIe 所需的电源管理寄存器。这些寄存器允许 OS 直接管理函数的电源环境。与其深入详细描述，不如让我们首先描述此功能在系统整体背景中的适用位置。

## **PCI PM 基础 (Basics of PCI PM)**

本节概述了 Windows OS 如何与其他主要软件和硬件元素交互以管理各个设备以及整个系统的功耗。表 16-1 在第 706 页介绍了此过程中涉及的主要元素，并提供了它们如何相互关联的非常基本的描述。值得注意的是，PCI 电源管理规范和 ACPI 规范都未规定操作系统使用的 PM 策略。但是，它们确实定义了用于控制函数功耗的寄存器（以及一些数据结构）。

## **PCI Express Technology**

_表 16-1：PC PM 中涉及的主要软件/硬件元素_

|**元素**|**职责**|
|---|---|
|OS|通过向 ACPI 驱动程序、设备驱动程序和 PCI Express 总线驱动程序发送请求来**指导整体系统电源管理**。具有节能意识的应用与 OS 交互以完成设备电源管理。|
|ACPI Driver|管理不遵守行业标准规范的嵌入式系统设备的配置、电源管理和热控制。这方面的示例包括芯片组特定寄存器、系统板特定寄存器以控制电源平面等。PCIe 函数（嵌入式或其他）中的 PM 寄存器由 PCI PM 规范定义，因此不由 ACPI 驱动程序管理，而是由 PCI Express Bus Driver 管理（请参见此表中的条目）。|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
