# 📘 第 14 章　链路初始化与训练 (Chapter 14. Link Initialization & Training)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0298.md` ... `chunks/chunk0315.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Link Initialization & Training](#-本章目录-table-of-contents)

<a id="sec-14-1"></a>
## 14.1 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The DSP performs the same actions as the USP and achieves a BER of 10[‐4] by detecting back‐to‐back TS1s. During this time, the DSP communicates its Tx presets and FS (Full Swing), LF (Low Frequency), and Post‐cursor coefficient values as shown in Figure 14‐32 on page 584. The spec gives some additional rules that must be satisfied for a set of requested coefficients, which are: 

1. |C‐1| <= Floor (FS/4), (Note: Floor means round down to the integer value) 2. |C‐1| + C0 + |C+1| = FS 

3. C0 ‐ |C‐1| ‐ |C+1| >= LF 

**581** 

## **PCI Ex ress Technolo p gy** 

FS represents the maximum voltage, and LF defines the minimum voltage as LF/FS. These inform the receiver about the number of possible values and allow the coefficients to be communicated as integer values but understood as frac‐ tional values. 

As an example, assume we’re using the coefficients defined for the P7 preset set‐ ting. The FS value acts as a reference and can be any number up to 63 but, for ease of calculation, let’s say it’s given as 30. In the case of P7, C‐1 is ‐0.1, the value communicated to represent C‐1 in the TS1s would be 3, since 3/30 = 0.1 and always considered negative. C+1 is ‐0.2, so it would be communicated as 6, since 6/30 = 0.2 and always negative. C0 is 0.7, so that will be sent as 21, since 21/30 = 0.7. Finally, the LF value represents the smallest possible ratio, and for P7 that is 0.4 times the max value. Consequently, LF will be communicated as 12, since 12/ 30 = 0.4. 

Armed with this information, let’s check the three rules to see whether they are satisfied for the P7 case: 

1. 3 <= Floor (12/4), This works out to be 3 <= 3 and is true. 

2. 3 + 21 + 6 = 30 This one is true. 

3. 21 ‐ 3 ‐ 6 >= 12 This one is also true, so all three checks are satisfied for P7. 

Once the Downstream Port is satisfied that the Link is working well enough to move forward (it recognizes incoming TS1s with EC = 01b), then this phase is complete and it initiates a change to Phase 2 by setting its EC = 10b as illustrated in Figure 14‐31 on page 583 and hands control of the next step back to the USP. When the USP responds with EC = 10b, both Ports go to Phase 2. As a happy alternative, the Downstream Port may conclude that the signal quality is already good enough at this point and no further adjustments are necessary. In that case, it set its EC = 00b to exit the equalization process. 

**582** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐31: Equalization Process: Initiating Phase 2_ 

**==> picture [232 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>Downstream<br>Port<br>EC = 10b EC = 01b<br>Upstream<br>Port<br>Endpoint<br>**----- End of picture text -----**<br>


## **Phase 2** 

The signal quality has been good enough to recognize TS1s, but not good enough for runtime operation. Once both Ports are in Phase 2, the Upstream Port is allowed to request Tx settings for the Downstream Port and then evalu‐ ate how well they work, reiterating the process until it arrives at optimal set‐ tings for the current environment. To make a request, it changes the value of the equalization information it sends in its TS1s. As shown in Figure 14‐32 on page 584, there are several values of interest: 

- **Tx Preset:** The Tx presets are a coarse‐grained adjustment to the Transmitter settings that are intended to get it into the right ballpark for the current sig‐ naling environment. The Upstream Port sets this value, and sets the “Use Preset” indicator (bit 7 of Symbol 6) to tell the Downstream Port’s Transmit‐ ter to use it. If the Use Preset bit is not set, then it’s understood that the pre‐ sets should stay as they are and that the coefficient values should be changed instead. The Tx coefficients are considered as fine‐grained adjust‐ ments. 

**583** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐32: Equalization Coefficients Exchanged_ 

**==> picture [309 x 267] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>7 6 5 4 3 2 1 0<br>0<br>Tx Preset EC<br>1 Link #<br>2 Lane # Use Preset Reset EIEOS<br>Interval Count<br>3 # FTS<br>Symbol 7<br>4 Rate ID<br>7 6 5 4 3 2 1 0<br>5 Train Ctl FS value when EC = 01b,<br>Rsvd<br>6 Otherwise Pre-Cursor Coefficient<br>EQ Info<br>Symbol 8<br>9<br>7 6 5 4 3 2 1 0<br>10<br>LF value when EC = 01b,<br>Rsvd<br>TS ID Otherwise Cursor Coefficient<br>13 Symbol 9<br>7 6 5 4 3 2 1 0<br>14<br>TS ID<br>15 P [RCV] Post-Cursor Coefficient<br>**----- End of picture text -----**<br>


- **Coefficients:** Since the spec requires a 3‐tap Tx equalizer, three coefficient values are defined that can be pictured as voltage adjustments to a signal pulse that compensates for the distortion it will experience going through the transmission medium, as shown in Figure 14‐33 on page 585. This is covered in more detail in the Physical Layer Electrical section titled, “Solu‐ tion for 8.0 GT/s ‐ Transmitter Equalization” on page 474. 

- **Pre‐Cursor Coefficient:** a multiplier applied to the signal prior to the sam‐ ple point that can boost or reduce the signal depending on the need. 

- **Cursor Coefficient:** the sample point multiplier; always positive. 

- **Post‐Cursor Coefficient:** a multiplier applied to the signal after the sample point that can boost or reduce the signal depending on the need. 

- Once the signal meets the quality standard needed, the Upstream Port indicates that it’s ready to move to the next phase by changing EC = 11b. 

**584** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐33: 3‐Tap Transmitter Equalization_ 

**==> picture [251 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
V<br>Unmodified Signal<br>t<br>UI UI UI UI<br>Cursor<br>V<br>Pre-cursor Post-cursor<br>reduction reduction<br>Equalized Signal<br>t<br>UI UI UI UI<br>Cursor<br>**----- End of picture text -----**<br>


_Figure 14‐34: Equalization Process: Adjustments During Phase 2_ 

**==> picture [250 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>Evaluate Propose<br>resulting new Tx<br>Rx signal EQ values<br>Endpoint<br>**----- End of picture text -----**<br>


**585** 

**PCI Ex ress Technolo p gy** 

## **Phase 3** 

The Downstream port responds by sending EC = 11b and can now do the same signal evaluation process for the Upstream Port’s Transmitter. It sends TS1s that request a new setting the same way: if the Use Preset bit is set, new presets are defined, otherwise new coefficients are being given. This is sent continuously for 1  s or until the request has been evaluated for its result, whichever is later. That evaluation must wait 500ns plus the round trip time through the outgoing logic and back in to the receive logic. Different equalization settings can be tested until one is found that achieves the desired signal quality. At that point the Downstream Port exits the equalization process by setting EC = 00b. 

_Figure 14‐35: Equalization Process: Adjustments During Phase 3_ 

**==> picture [252 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>Propose Evaluate<br>new Tx<br>resulting<br>EQ values<br>Rx signal<br>Endpoint<br>**----- End of picture text -----**<br>


## **Equalization Notes** 

The specification mentions other items associated with the equalization process, as described below: 

- All Lanes must participate in the process; even those that may only become active later after an upconfigure event. 

- The algorithm used by a component to evaluate the incoming signal and determine the equalization values that its Link partner should use is not given in the spec and is implementation specific. 

**586** 

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

**587** 

**PCI Ex ress Technolo p gy** 

- Equalization Phase 1 Successful 

- Equalization Phase 2 Successful 

- Equalization Phase 3 Successful 

- Link Equalization Request 

- Equalization Complete 

The Perform Equalization bit of the Link Control 3 register is also cleared to 0b as is the internal variable start_equalization_w_preset. The equalization_done_8GT_data_rate variable is set to 1b. 

_Figure 14‐36: Link Status 2 Register_ 

**==> picture [320 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 6 5 4 3 2 1 0<br>RsvdZ<br>Link Equalization Request<br>Equalization Phase 3 Successful<br>Equalization Phase 2 Successful<br>Equalization Phase 1 Successful<br>Equalization Complete<br>Current De-emphasis Level<br>**----- End of picture text -----**<br>


_Figure 14‐37: Link Control 3 Register_ 

**==> picture [341 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 2 1 0<br>RsvdP<br>Link Equalization Request<br>Interrupt Enable<br>Perform Equalization<br>**----- End of picture text -----**<br>


**588** 

**Chapter 14: Link Initialization & Training** 

**Phase 1 Downstream.** During this phase, the Downstream Port sends TS1s with EC = 01b while using the Preset values from the Lane Equaliza‐ tion Control register and with the FS, LF, and Post‐cursor Coefficient fields that correspond to the Tx Preset field. It’s allowed to wait 500ns before eval‐ uating incoming TS1s if it needs time to stabilize its Receiver logic. 

## _Exit to “Phase 2 Downstream”_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

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

**589** 

**PCI Ex ress Technolo p gy** 

TS1s being sent and set the Reject Coefficient Values bit to 1b (seeFigure 14‐38 on page 590). 

- If the two consecutive TS1s aren’t seen, keep the current Tx preset and coefficient values. 

## _Exit to “Phase 3 Downstream”_ 

When the Upstream Port is satisfied with the changes, it begins to send TS1s with EC = 11b, indicating a desire to change to Phase 3. When two consecu‐ tive TS1s like this are received, set the Eq. Phase 2 Successful status bit to 1b and change to Phase 3. 

## _Exit to “Recovery.Speed”_ 

If after 32 ms, the transition to Phase 3 has not happened, the Port should clear the successful_speed_negotiation flag, set the Equalization Complete status bit and exit to the Recovery.Speed substate. 

_Figure 14‐38: TS1s ‐ Rejecting Coefficient Values_ 

**==> picture [264 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>7 6 5 4 3 2 1 0<br>0<br>Tx Preset EC<br>1 Link #<br>2 Lane # Use Preset Reset EIEOS<br>Interval Count<br>3 # FTS<br>Symbol 7<br>4 Rate ID<br>7 6 5 4 3 2 1 0<br>5 Train Ctl FS value when EC = 01b,<br>Rsvd<br>6 Otherwise Pre-Cursor Coefficient<br>EQ Info<br>Symbol 8<br>9<br>7 6 5 4 3 2 1 0<br>10<br>LF value when EC = 01b,<br>Rsvd<br>TS ID Otherwise Cursor Coefficient<br>13 Symbol 9<br>7 6 5 4 3 2 1 0<br>14<br>TS ID<br>15 P [RCV] Post-Cursor Coefficient<br>**----- End of picture text -----**<br>


**590** 

**Chapter 14: Link Initialization & Training** 

**Phase 3 Downstream.** During this phase, the Downstream Port sends TS1s with EC = 11b and begins the process of evaluating Upstream Tx set‐ tings independently for each Lane. 

In the transmitted TS1s, the Downstream Port can either request a new pre‐ set by setting the Use Preset bit to 1b and Tx Preset field to the desired value, or it can request new coefficients by clearing the Use Preset bit to 0b and setting the Pre‐cursor, Cursor, and Post‐Cursor Coefficient fields to the desired values. Either request must be made continuously for at least 1  s or until the evaluation has completed. If new preset or coefficient settings are going to be presented, they must be sent on all Lanes at the same time. However, a given Lane isn’t required to request new settings if it wants to keep the ones it has. 

The Downstream Port must wait long enough to ensure the Upstream Transmitter has had a chance to implement the requested changes, (500ns plus the round‐trip delay for the logic), then obtain Block Alignment and evaluate the incoming TS1s. It’s not expected that anything useful will be coming from the Upstream Port during the waiting period, and it may not even be legal. That’s why obtaining Block Alignment after that time is a requirement. 

If two consecutive TS1s are seen that match the same preset or coefficient values that are being requested and don’t have the Reject Coefficient Values bit set, then the requested setting was accepted and can be evaluated. If the values match but the Reject Coefficient Values bit is set to 1b, then the requested values have been rejected by the Upstream Port and are not being used. For this case, he spec recommends that the Downstream Port try again with different values but it’s not required to do so and may choose to simply exit this phase. 

The total time spent on a preset or coefficient request, from the time the request is sent until the completion of its evaluation must be less than 2ms. An exception is available for designs that need more time for the final stage of optimization, but the total time in this phase cannot exceed 24ms and the exception can only be taken twice. If the Receiver doesn’t recognize any incoming TS1s, it may assume that the requested setting doesn’t work for that Lane. 

## _Exit to “Detailed Recovery Substates”_ 

The next state will be Recovery.RcvrLock when all configured Lanes have their optimal settings. When that happens, the Equalization Phase 3 Successful and Equalization Complete status bits will be set to 1b. 

**591** 

**PCI Ex ress Technolo p gy** 

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

**592** 

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

**593** 

**PCI Ex ress Technolo p gy** 

at least 1  s or until the evaluation is complete. If new preset or coefficient settings are going to be presented, they must be sent on all Lanes at the same time. However, a given Lane isn’t required to request new settings if it wants to keep the ones it has. 

The Upstream Port must wait long enough to ensure the Downstream Transmitter has had a chance to implement the requested changes, (500ns plus the round‐trip delay for the logic), then obtain Block Alignment and evaluate the incoming TS1s. It’s not expected that anything useful will be coming from the Downstream Port during the waiting period, and it may not even be legal. That’s why obtaining Block Alignment after that time is a requirement. 

When TS1s are received that contain the same equalization fields as are being sent and the Reject Coefficient Values bit is not set (0b), then the set‐ ting has been accepted and can now be evaluated. If the equalization fields match but the Reject Coefficient Values bit is set (1b), then the setting has been rejected. In that case the spec recommends that the Upstream Port request a different equalization setting, but this is not required. 

The total time spent on a preset or coefficient request, from the time the request is sent until the completion of its evaluation must be less than 2ms. An exception is available for designs that need more time for the final stage of optimization, but the total time in this phase cannot exceed 24ms and the exception can only be taken twice. If the Receiver doesn’t recognize any incoming TS1s, it may assume that the requested setting doesn’t work for that Lane. 

_Exit to “Phase 3 Upstream”_ 

The next phase is Phase 3 if all configured Lanes have their optimal set‐ tings. When that happens, the Equalization Phase 2 Successful status bit will be set to 1b.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-3"></a>
## 14.3 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

_Exit to “Recovery.Speed”_ 

Otherwise, after a 24ms timeout (with a tolerance of ‐0 or +2ms), the next state will be Recovery.Speed, and the successful_speed_negotiation flag is cleared to 0b while the Equaliza‐ tion Complete status bit is set to 1b. 

**Phase 3 Upstream.** During this phase, the Upstream Port sends TS1s with EC = 11b and responds to the requested Tx values from the Downstream Port. 

**594** 

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

**595** 

**PCI Ex ress Technolo p gy** 

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



**596** 

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

**==> picture [373 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


**597** 

**PCI Ex ress Technolo p gy** 

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

**598** 

**Chapter 14: Link Initialization & Training** 

If the speed has been changed a different N_FTS number may now be seen in the TS2s. That value must be used for exiting future L0s low‐power Link states. For 8b/10b encoding, Lane‐to‐Lane de‐skew must be completed before leaving this substate. Devices must note the advertised rate identifier in incoming TS2s and use this to override any previously‐recorded values. When using 128b/130b encoding, devices must make a note of the value of the Request Equalization bit for future reference. 

Notes about this substate: The variable successful_speed_negotiation is set to 1b. The data rates advertised in the TS2s with the speed_change bit set are noted at this point for future reference, as is the Autonomous Change bit for possible logging in the Link Status register during Recovery.Speed. The rate that will be selected in Recovery.Speed will be the highest commonly‐supported rate. Inter‐ estingly, the change to Recovery.Speed will take place for this case even if the Link is already operating at the highest supported rate, although in that case the rate won’t actually change. 

If the speed is going to change to 8.0 GT/s, a Downstream Port will need to send EQ TS2s (bit 7 of Symbol 6 is set to 1b to indicate an EQ training sequence). This case would be recognized if 8.0 GT/s is mutually supported and 8 consecutive TS1s or TS2s have been seen on any configured Lane with the speed_change bit set, or if the equalization_done_8GT_data_rate variable is 0b, or if directed. An Upstream Port can set the Request Equalization bit if the current data rate is 8.0 GT/s and there was a problem with the equalization process. Either Port can request equalization be done again by setting both the Request Equalization and Quiesce Guarantee bits to 1b. 

Upstream Ports set their select_deemphasis variable based on the Selectable De‐ emphasis bit in the received TS2s. And, if the TS2s were EQ TS2s, they set the start_equalization_w_preset variable to 1b and update their Lane Equalization register with the new information (i.e.: update the Upstream Port Transmitter Preset and Receiver Preset Hint fields in the register). Any configured Lanes that don’t receive EQ TS2s will choose their preset values for 8.0 GT/s operation in a design‐specific manner. Downstream Ports must set their start_equalization_w_preset variable to 1b if the equalization_done_8GT_data_rate variable is cleared to 0b or if directed. 

Finally, if 128b/130b encoding is in use, devices must make a note of the Request Equalization bit. If set, both it and the Quiesce Guarantee bit must be stored for future reference. 

**599** 

**PCI Ex ress Technolo p gy** 

## _Exit to “Recovery.Idle”_ 

The next state will be Recovery.Idle if two conditions are true:

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

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

**600** 

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

**601** 

## **PCI Ex ress Technolo p gy** 

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

**602** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Detect State”_ 

Otherwise, after a 2ms timeout, the next state will be Detect unless the idle_to_rlock_transitioned variable is less than FFh, in which case the next state will be “Detailed Recovery Substates”. For the transition to Recov‐ ery.RcvrLock, if the data rate is 8.0 GT/s the idle_to_rlock_transitioned vari‐ able is incremented by 1b, while for 2.5 or 5.0 GT/s it will be set to FFh. 

## **L0s State** 

This is the low power Link state that has the shortest exit latency back to L0. Devices manage entry and exit from this state automatically under hardware control without any software involvement. Each direction of a Link, can enter and exit the L0s state independent of each other. 

## **L0s Transmitter State Machine** 

The L0s state has different substates for the Transmitter and the Receiver. The Transmitter substates will be described first. As shown in Figure 14‐40 on page 603 the transmitter state machine associated with L0s state is a simple one. 

_Figure 14‐40: L0s Tx State Machine_ 

**==> picture [288 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Tx sends  Transmitter sends<br>EIOS FTSs on all Lanes<br>TTX-IDLE-MIN<br>= 20 ns Tx_L0s.Idle Directed<br>Tx_L0s.Entry Tx_L0s.FTS<br>(Tx Electrical Idle)<br>Transmitter sends<br>SOS or EIEOS<br>Exit to<br>L0<br>**----- End of picture text -----**<br>


**603** 

**PCI Ex ress Technolo p gy** 

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

**604** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “L0 State”_ 

The Transmitter will transition to the L0 state once all the FTSs have been sent and: 

- a)  For 8b/10b encoding, one SOS is sent on all configured Lanes, although none are sent before or during the FTSs. 

- b)  For 128b/130b encoding, one EIEOS is sent followed by an SDS and a Data Stream. 

## **L0s Receiver State Machine** 

Figure 14‐41 on page 605 shows the Receiver L0s state machine. A Receiver is required to implement L0s support if the ASPM Support field in the Link Capa‐ bility register shows it to be supported, and is allowed to implement it even if that support is not indicated. 

_Figure 14‐41: L0s Receiver State Machine_ 

**==> picture [327 x 184] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Rx detects<br>EIOS Exit from FTSs Received<br>TTX-IDLE-MIN Electrical<br>= 20 ns Rx_L0s.Idle Idle<br>Rx_L0s.Entry Rx_L0s.FTS<br>(Rx Electrical Idle)<br>Tx sends N_FTS<br>SOS or EIEOS Timeout<br>Exit to Exit to<br>L0 Recovery<br>**----- End of picture text -----**<br>


**605** 

**PCI Ex ress Technolo p gy** 

## **Rx_L0s.Entry.** 

Entered when a Receiver that receives an EIOS, provided it supports L0s and hasn’t been directed to L1 or L2. 

_Exit to “Rx_L0s.Idle”_ 

The next state will be Rx_L0s.Idle after the TTX‐IDLE‐MIN timeout (20ns). 

## **Rx_L0s.Idle.** 

The Receiver is now in Electrical Idle mode and is just waiting to see an exit from Electrical Idle.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

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

**606** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Recovery State”_ 

Otherwise the next state will be Recovery after the N_FTS timeout. If so, the Transmitter must also go to Recovery, although it’s allowed to finish any TLP or DLLP that was in progress. If the timeout occurs, the spec recommends that the N_FTS value be increased to reduce the likelihood of it happening again. The N_FTS timeout is defined as follows: 

For 8b/10b, the minimum timeout is given as 40 * [N_FTS + 3] * UI, while the maximum allowed is twice that time. Since 10 bits (UI repre‐ sents one bit time) are needed per Symbol, this works out to (4*N_FTS + 12) Symbols. The extra 12 Symbols are explained as 6 for a max‐sized SOS + 4 for the possible extra FTS + 2 more for Symbol margin. In sum‐ mary, then, the minimum time is the time it should take to send the requested number of FTSs plus 12 Symbols, while the maximum time is twice as much as that. 

If the extended synch bit is set, the min time = 2048 FTSs and the max time = 4096 FTSs. The actual timeout value a Receiver will use must also take into account the 4 to 8 EIE Symbols for speeds other than 2.5 GT/s. 

For 128b/130b, the timeout value is given as a minimum of 130 * [N_FTS + 5 + 12 + Floor (N_FTS/32)] * UI and a max of twice that time. The value 130 * UI means 130 bit times which represents one Block, so if we remove those two values we can say we’re looking at [N_FTS + 5 + 12 + Floor (N_FTS/32)] Blocks. The value [5 + Floor (N_FTS/32)] represents the EIEOSs that will need to be sent during this time. One EIEOS will be sent after every 32 FTSs, so Floor (N_FTS/32) gives that number. The other 5 are accounted for by the first EIEOS, the last EIEOS, the SDS, the periodic EIEOS and an additional EIEOS in case the Transmitter chooses to send two EIEOS followed by an SDS when N_FTS is divisi‐ ble by 32. Finally, the value of 12 represents the number of SOSs that will be sent if the extended synch bit is set. When that bit is set, the tim‐ eout will use N_FTS = 4096. 

## **L1 State** 

This Link power state trades a longer exit latency for more aggressive power management compared to the L0s state. L1 is an option for ASPM, like L0s, meaning devices can enter and exit this state automatically under hardware control without any software involvement. However, unlike L0s, software is also able to direct an Upstream Port to initiate a change to L1, and it does so by writing the device power state to a lower level (D1, D2, or D3). The L1 state is also different from L0s in that it affects both directions of the Link. 

**607** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐42: L1 State Machine_ 

**==> picture [260 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Directed and Remain in<br>EIOS Tx & Rx TTX-IDLE-MIN Electrical Idle<br>= 20 ns L1.Idle<br>L1.Entry<br>(Electrical Idle)<br>Tx in Electrical Idle Tx Directed or<br>Rx sees Electrical Idle Exit<br>Exit to<br>Recovery<br>**----- End of picture text -----**<br>


Since going to Electrical Idle can indicate a desire by the Link partner to enter L0s, L1 or L2, differentiating which should be the next state is handled by hav‐ ing both partners agree beforehand when they’re going to enter L1. A hand‐ shake informs them that the partner is ready and it’s therefore safe to proceed. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. Figure 14‐42 on page 608 shows the L1 state machine, which is described in the following sections. 

## **L1.Entry** 

In order for an Upstream Port to enter this state, it must send a request to enter L1 to its Link Partner and receive acknowledgement that it is OK to put the Link into L1. (The reason for requesting to go into L1 may be because of ASPM or because of software involvement.) Once the L1 request acknowledge is received, the Upstream Port enters the L1.Entry substate. 

In order for a Downstream Port to enter this state, it must receive an L1 enter request from the Upstream Port and send a positive response to that request. Then the Downstream Port waits to receive an Electrical Idle Ordered Set (EIOS) and have its receive lanes drop to Electrical Idle. It is at this point that the Downstream Port enters the L1.Entry substate. 

**608** 

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

**609** 

## **PCI Ex ress Technolo p gy** 

restored. There are two standard ways a device can inform the system of such an event. One is a side‐band signal called the WAKE# pin, and the other is an in‐ band signal called a “Beacon.” The L2 state isn’t needed for WAKE#, but is required if the optional Beacon will be used. The spec explicitly states that devices operating at 5.0 or 8.0 GT/s don’t need to support Beacon, so it would seem that this is legacy support and only interesting for devices operating at 2.5 GT/s. For more detail on Link wakeup options, refer to “Waking Non‐Commu‐ nicating Links” on page 772. 

If supported, the Beacon is a low‐frequency (30 KHz ‐ 500 MHz) in‐band signal that an Upstream Port supporting wakeup capability must be able to send on at least Lane 0 and a Downstream Port must be able to receive. Intermediate devices like Switches that receive a Beacon on a Downstream Port must forward it to their Upstream Port. The ultimate destination for the Beacon is the Root Complex, because that’s where the system power control logic is expected to reside. 

A Transmitter going to Electrical Idle could indicate a desire to enter any of the low‐power Link states (L0s, L1 or L2), so a means of differentiating them is needed. For L2, this is handled by having the Link partners agree beforehand that they’re going to enter L2 by using a handshake sequence to ensure that they’re both ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. Figure 14‐43 on page 611 shows the L2 entry and Exit state machine, which is described in the follow‐ ing text. 

**610** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐43: L2 State Machine_ 

**==> picture [349 x 227] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Directed, and<br>EIOS both sent<br>and received Upstream Tx<br>sends Beacon<br>Upstream Port directed to send Beacon,<br>L2.Idle or Downstream Port detects Beacon<br>(Electrical Idle, L2.TransmitWake<br>No DC CMV)<br>Rx termination enabled,<br>Rx looking for  Upstream Rx detects<br>Electrical Idle Exit Electrical Idle Exit<br>Root Port detects Beacon,<br>or Upstream Port sees<br>Electrical Idle Exit Exit to<br>Detect<br>**----- End of picture text -----**<br>


## **L2.Idle** 

To enter this substate, all the necessary handshake process must have already taken place between both ports on the Link and the ports have sent and received the required EIOS. 

All configured Transmitters must remain in the Electrical Idle state for at least the TTX‐IDLE‐MIN timeout (20ns). However, since the main power will now be shut off, they aren’t required to maintain the DC common‐mode voltage within the spec range. Receivers won’t start looking for the Electrical exit condition until at least after the 20ns timeout expires. All Receiver terminations must remain enabled in the low impedance condition. 

## _Exit to “L2.TransmitWake”_ 

The next state will be L2.TransmitWake if the Upstream Port is instructed to send a Beacon (the Beacon is always and only directed upstream to the Root Complex). 

**611** 

**PCI Ex ress Technolo p gy** 

If the Downstream Port of a Switch detects a Beacon, it must direct the Upstream Port of the Switch to exit to L2.TransmitWake and begin sending a Beacon. 

## _Exit to “Detect State”_ 

Once main power is returned, the next state will be Detect. 

If this Port has main power, but it detects an exit from Electrical Idle on any “predetermined” Lanes, meaning those that could be negotiated to be Lane 0 (multi‐Lane Links must have at least two predetermined Lanes), the next state will be detect. When this happens to a Switch Upstream Port, the Switch must also transition its Downstream Ports to Detect. 

## **L2.TransmitWake**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

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

**612** 

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

**613** 

## **PCI Ex ress Technolo p gy** 

clock tolerance compensation, so the master must continue to insert SOSs at the correct intervals. To perform clock tolerance compensation, the Loopback slave may have to add or delete SKP Symbols to the SOS it echoes to the Loopback master. 

The Loopback state is exited when the Loopback master transmits an EIOS and the receiver detects Electrical Idle. The Loopback state machine is shown in Fig‐ ure 14‐44 on page 614 and described in the following text. 

_Figure 14‐44: Loopback State Machine_ 

**==> picture [368 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from Configuration<br>Or Recovery<br>Slave: Enter Electrical<br>Master sends valid Idle for 2ms<br>Master sends Master receives Symbols - Master: Tx EIOSs<br>Identical TS1’s; Slave required to and enter Electrical<br>TS1s w/ Loopback Slave has retransmit exactly Slave: Directed or  Idle for 2 ms<br>bit set entered 4 EIOS seen<br>Loopback Master: Directed<br>Loopback.Entry Loopback.Active Loopback.Exit<br>Timeout less than<br>100 ms Exit to<br>Detect<br>**----- End of picture text -----**<br>


## **Loopback.Entry** 

The typical behavior for this substate is for the Loopback Master to send TS1s with the Loopback bit set until it starts seeing those TS1s being returned. Once the Loopback Master sees TS1s being returned with the Loopback bit asserted, it knows that it’s Link Partner is now behaving as the Loopback Slave and is simply repeating everything it receives. 

While in this substate, the Link is not considered to be active (LinkUp = 0b). Also, the Link and Lane numbers used in TS1s and TS2s are ignored by the Receiver. The spec makes an interesting observation regarding the use of Lane numbers with 128b/130b encoding. As it turns out, each Lane uses a different seed value for its scrambler (see “Scrambling” on page 430). Consequently, if the Lane numbers haven’t been negotiated before going into the Loopback mode, it’s possible that the Link partners could have different Lane assignments and would therefore be unable to recognize incoming Symbols. This can be avoided by waiting until the Lane numbers have been negotiated before direct‐ 

**614** 

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

**615** 

**PCI Ex ress Technolo p gy** 

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

**616** 

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

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-7"></a>
## 14.7 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The slave must be able to detect an Electrical Idle on any Lane within 1ms of EIOS being received. Between the time EIOS is received and Electrical Idle is actually detected, the Loopback Slave may receive a bit stream that is undefined by the encoding scheme, and it may loop that back to the trans‐ mitter. 

**617** 

**PCI Ex ress Technolo p gy** 

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

**618** 

**Chapter 14: Link Initialization & Training** 

fied. Interestingly, components are also permitted to go into the Recovery state and advertise a different set of supported speeds without requesting a speed change in the process. 

Changing the Link Speed or Link Width requires the Link to be re‐trained. When the Link is in the L0 state, and the speed needs to be changed, the LTSSM of the port desiring the speed change starts transmitting TS1s to its neighbor. Doing so results in the two involved ports’ LTSSMs going through Recovery state where the Link speed is changed and then back to L0. 

Similarly, the port that desires to change the Link width starts transmitting TS1s to its neighbor. Doing so results in the two involved ports’ LTSSMs going through Recovery state then Configuration state where the Link width is changed. The LTSSM finally returns to L0 with the new Link width established. 

Because the LTSSM is involved in dynamic Link bandwidth management, it makes sense to discuss the two aspects of Link bandwidth management, dynamic Link speed change and dynamic Link width change in the following sections. Let’s consider these two options separately, starting with Link speed changes. 

## **Dynamic Link Speed Changes** 

By way of review, the LTSSM states are illustrated in Figure 14‐45 on page 620 to make it easier to recall the flow of states. Although according to the Gen1 specification, speed change was indicated to be performed in the Polling state, the subsequent Gen2 spec moved this function to the Recovery state. 

**619** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐45: LTSSM Overview_ 

**==> picture [196 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Polling<br>Configuration<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


During the Polling state, TS1s are exchanged between Link neighbors, and these contain several kinds of information as shown in Figure 14‐46 on page 621. The most interesting part for us here is byte number 4, the Rate Identifier. Bits 1, 2 and 3 indicate which data rates are available and the spec points out that 2.5 GT/s must always be supported, while 5.0 GT/s must also be supported if 8.0 GT/s is supported. 

The meaning of bit 6 depends on whether the Port is facing upstream or down‐ stream and also on what LTSSM state the Port is in. However, for the speed change case the options are reduced because it’s only meaningful coming from the Upstream Port and just indicates whether or not the speed change is an autonomous event. “Autonomous” means that the Port is requesting this change for its own hardware‐specific reasons and not because of a reliability issue. Bit 7 is used by the Upstream Port to request a speed change. These val‐ ues are very similar in the TS2s, although bit 6 has another meaning now related to autonomous Link width changes that we’ll discuss later. 

**620** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐46: TS1 Contents_ 

**==> picture [315 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link #<br>Rate Identifier<br>2 Lane # Bit 0 Reserved, = 0<br>3 # FTS Bit 1 Indicates 2.5 GT/s support<br>4 Rate ID Bit 2 Indicates 5.0 GT/s support<br>5 Train Ctl Bit 3 Indicates 8.0 GT/s support<br>6 Bit 4:5 Reserved, = 0<br>TS ID Bit 6 Autonomous Change / Selectable De-<br>13 emphasis<br>14 TS ID Bit 7 Speed Change<br>15 TS ID<br>**----- End of picture text -----**<br>


_Figure 14‐47: TS2 Contents_ 

**==> picture [316 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link # Rate Identifier<br>Bit 0 Reserved, = 0<br>2 Lane #<br>Bit 1 Indicates 2.5 GT/s support<br>3 # FTS<br>Bit 2 Indicates 5.0 GT/s support<br>4 Rate ID<br>Bit 3 Indicates 8.0 GT/s support<br>5 Train Ctl<br>Bit 4:5 Reserved, = 0<br>6<br>Bit 6 Autonomous Change / Link Up-<br>TS ID configure Capability / Selectable De-<br>13 emphasis<br>14 TS ID Bit 7 Speed Change<br>15 TS ID<br>**----- End of picture text -----**<br>


**621** 

**PCI Ex ress Technolo p gy** 

## **Upstream Port Initiates Speed Change** 

A speed change must be initiated by the Upstream Port (Port facing upstream), and is accomplished by transitioning to the Recovery state. The substates of the Recovery state are shown in Figure 14‐48 on page 622 and the part of interest for this discussion is highlighted by the oval. The discussion that follows here is a relatively high‐level overview of the entire speed change process and doesn’t get into the details of the LTSSM operation. To learn more about that, refer to the discussion called “Recovery State” on page 571. 

_Figure 14‐48: Recovery Sub‐States_ 

**==> picture [342 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Recovery.Speed<br>Entry from Loopback Exit to<br>L1, L0, L0s Configuration<br>Recovery.Equalization<br>Recovery.RcvrLock Recovery.Idle Exit to<br>(bit/symbol re-lock) Recovery.RcvrCfg (Send idle data) Disabled<br>Exit to Hot<br>Exit to Exit to Reset<br>Configuration Detect<br>Exit to L0<br>**----- End of picture text -----**<br>


## **Speed Change Example** 

To illustrate the process, consider the speed change example shown in Figure 14‐49 on page 623. Note that the Equalization substate has been removed in this example to make the diagrams simpler and easier to follow. The example shows a change from 2.5 GT/s to 5.0 GT/s and so the Equalization substate is not used anyway. A change to 8.0 GT/s would go through the same process but would just add a trip through the Equalization substate at the end of the process. To 

**622** 

**Chapter 14: Link Initialization & Training** 

learn more about the Equalization process, refer to “Recovery.Equalization” on page 587. 

The Endpoint in this example, which can only have an Upstream Port, is shown connected to a Root Complex, which can only have Downstream Ports. Only the Upstream Port can initiate the speed change process, and it does so because its _Directed Speed Change_ flag was set earlier based on some hardware‐specific con‐ ditions. To start the sequence, it changes its LTSSM to the Recovery state, enters the Recovery.RcvrLock substate and sends TS1s with the Speed Change bit set and listing the speeds that it will support, as shown in Figure 14‐49 on page 623. When the Downstream Port sees the incoming TS1s, it also changes to the Recovery state and begins sending TS1s back. Since the Speed Change bit was set in the incoming TS1s, that will set the _Directed Speed Change_ flag in the Root Port and the outgoing TS1s will also have that bit set. The speed that the Link will attempt to use will be the highest commonly‐supported speed so, if a Device wants to use a lower speed it would simply not list the higher speeds as being supported at this time. 

_Figure 14‐49: Speed Change ‐ Initiated_ 

**==> picture [336 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 1<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 1<br>TS1 TS1 TS1 TS1<br>Root PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>TS1 TS1 TS1 TS1<br>Speed_Change = 1<br>**----- End of picture text -----**<br>


When the Upstream Port detects the TS1s coming back, its state machine changes to the Recovery.RcvrCfg substate and it begins to send TS2s that still have the Speed Change bit set, as illustrated in Figure 14‐50 on page 624. These 

**623** 

**PCI Ex ress Technolo p gy** 

TS2s will now also have the Autonomous Change bit set if this change was not caused by a reliability problem on the Link. When the Downstream Port sees incoming TS2s, it also changes to the Recovery.RcvrCfg substate and returns TS2s with the Speed Change bit set. However, the Autonomous Change bit is reserved in the TS2s for Downstream Ports during Recovery. 

_Figure 14‐50: Speed Change ‐ Part 2_ 

**==> picture [371 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 1 Directed Speed Change = 1<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 1<br>TS2 TS2 TS2 TS2<br>Root  PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>TS2 TS2 TS2 TS2<br>Speed_Change = 1<br>Autonomous Change = 1<br>**----- End of picture text -----**<br>


Once each Port has seen 8 consecutive TS2s with the Speed Change bit set, they know that the next step will be to go to the Recovery.Speed substate, as shown in Figure 14‐51 on page 625. At this point, the Downstream Port needs to regis‐ ter the setting of the Autonomous Change bit in the incoming TS2s. To support this, some extra fields have been added to the PCIe Capability registers. 

The status bits for Link bandwidth changes are found in the Link Status regis‐ ter, shown in Figure 14‐52 on page 625. Status changes can also be used to gen‐ erate an interrupt to notify software of these events if the device is capable and has been enabled to do so. This capability is reported by the Link Bandwidth Notification Capable bit, shown in Figure 14‐53 on page 626, and enabled by the Interrupt Enable bits in the Link Control register, as shown in Figure 14‐54 on 

**624**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-8"></a>
## 14.8 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Chapter 14: Link Initialization & Training** 

page 626. Note that there are two cases: autonomous and bandwidth manage‐ men. Autonomous means the change was not caused by a reliability problem, while bandwidth management means it was. 

_Figure 14‐51: Speed Change ‐ Part 3_ 

**==> picture [336 x 243] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 0<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>TS2 TS2 TS2 EIOSTS2<br>SSS<br>Root PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>EIOSTS2 TS2 TS2 TS2<br>Autonomous Change = 1<br>Root Complex Config Space<br>Link Autonomous Bandwidth Status bit = 1<br>i<br>Figure 14‐52: Bandwidth Change Status Bits<br>**----- End of picture text -----**<br>


**625** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐53: Bandwidth Notification Capability_ 

_Figure 14‐54: Bandwidth Change Notification Bits_ 

**626** 

**Chapter 14: Link Initialization & Training** 

Once the Recovery.Speed substate is reached, the Link is placed into the Electri‐ cal Idle condition in both directions and the speed is changed internally. The speed chosen will be the highest commonly‐supported speed reported in the Rate ID field of the TS1s and TS2s. In this example, that turns out to be 5.0 GT/s and so the change is made to that speed. After a timeout period, the Link neigh‐ bors both transition back to Recovery.RcvrLock and exit Electrical Idle by send‐ ing TS1s again, as shown in Figure 14‐55 on page 627. When the Upstream Port sees them coming back, it transitions to Recovery.RcvrCfg and begins sending TS2s, much like before. This time, though, the Speed Change bit is not set. Even‐ tually TS2s are seen coming back from the Downstream Port that also don’t have the Speed Change bit set, and at that point the state machines transition to the Recovery.Idle on their way back to L0. 

If a speed change has fails for some reason, a component is not allowed to try that speed or a higher one for at least 200 ms after returning to L0 or until the Link neighbor advertises support for a higher speed, whichever comes first. 

_Figure 14‐55: Speed Change Finish_ 

**==> picture [364 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 0<br>Entry Entry<br>Speed Speed<br>Exit to L0 Exit to L0<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 0<br>TS21 TS21 TS21 TS21<br>Root PCIe<br>Link Speed = 5.0 GT/s<br>Complex Endpoint<br>TS21 TS21 TS21 TS21<br>Speed_Change = 0<br>**----- End of picture text -----**<br>


## **Software Control of Speed Changes** 

Software is unable to control when hardware makes decisions about changing the speed but can limit or disable this capability. Limiting it is accomplished by setting the Target Link Speed value in the Link Control 2 Register shown in Fig‐ ure 14‐56 on page 628. This acts as the upper bound on the speeds available to 

**627** 

**PCI Ex ress Technolo p gy** 

the Upstream Port, which will try to maintain that value or the highest speed supported by both Link neighbors, whichever is lower. Software can also force a particular speed to be used by setting the Target Link Speed in the Upstream component and then setting the Retrain Link bit in the Link Control register, shown in Figure 14‐57 on page 629. As mentioned earlier, software is notified of any hardware‐based Link speed or width changes by the Link Bandwidth Noti‐ fication Mechanism. Finally, the speed change mechanism can be disabled by setting the Hardware Autonomous Speed Disable bit. 

_Figure 14‐56: Link Control 2 Register_ 

**628** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐57: Link Control Register_ 

## **Dynamic Link Width Changes** 

The same basic operation for changing the Link speed can also be used to change the Link width, although the sequence is a little more complicated because more LTSSM steps are involved. One thing that’s important for soft‐ ware to note before enabling Link width changes is whether the Link neighbor supports recovering from a narrow Link back to a wide Link (called Upconfig‐ uring the Link). Devices report this ability in bit 6 of the Rate ID field of the TS2s they send during training, as shown in Figure 14‐58 on page 630. If a component doesn’t support this, that would mean that changing to a narrower Link width would be a one‐way event and would only be suitable for the case of a reliabil‐ ity problem on the Link. 

**629** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐58: TS2 Contents_ 

**==> picture [368 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link # Rate Identifier<br>Bit 0 Reserved, = 0<br>2 Lane #<br>Bit 1 Indicates 2.5 GT/s support<br>3 # FTS<br>Bit 2 Indicates 5.0 GT/s support<br>4 Rate ID<br>Bit 3 Indicates 8.0 GT/s support<br>5 Train Ctl<br>Bit 3:5 Reserved, = 0<br>6 Bit 6 Autonomous Change / Link Up-<br>configure Capability / Selectable De-<br>TS ID<br>emphasis<br>13 Bit 7 Speed Change<br>14 TS ID<br>15 TS ID<br>**----- End of picture text -----**<br>


## **Link Width Change Example** 

Consider the example in Figure 14‐59 on page 631 of a Root Port connected to an Endpoint (Gigabit Ethernet Device). Only the Upstream Port will initiate this change, and it begins by going to the Recovery state as before. This time, though, the Speed Change bit is not set. To sort out what the new Link width will be, the Upstream Port will need to tell the Downstream Port to transition from the Recovery state to the Configuration state before going back to L0, as shown in Figure 14‐60 on page 631. There are several substates in the Configu‐ ration state, and a simplified version of them is shown in Figure 14‐61 on page 632. We’ll go through the sequence to be clear on how the steps work. 

**630** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐59: Link Width Change Example_ 

**==> picture [199 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root  Ethernet<br>Complex Device<br>Lane Lane<br>0 0<br>1 1<br>2 Lan2<br>e<br>3 3<br>**----- End of picture text -----**<br>


_Figure 14‐60: Link Width Change LTSSM Sequence_ 

**==> picture [183 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Polling<br>Configuration<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


**631** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐61: Simplified Configuration Substates_ 

**==> picture [136 x 351] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from<br>Polling or Recovery<br>Config.Linkwidth.Start<br>Config.Linkwidth.Accept<br>Config.Lanenum.Wait<br>Config.Lanenum.Accept<br>Config.Complete<br>Config.Idle<br>Exit to<br>L0<br>**----- End of picture text -----**<br>


As before, the Upstream Port initiates this process by going to Recovery and sending TS1s. These don’t have the Speed Change bit set, as highlighted in the example shown in Figure 14‐59 on page 631, where an Ethernet Device initiates this process on its Upstream Port. In response, the Downstream Port sends TS1s back, also with the Speed Change bit cleared. Link and Lane numbers are still shown as being unchanged from the last time the Link was trained. Referring back to Figure 14‐48 on page 622, the next state is Recovery.RcvrCfg during which the Link partners exchange TS2s. 

**632** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐62: Link Width Change ‐ Start_ 

**==> picture [296 x 299] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex<br>Device<br>Lane Lane<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:0) TS1 (Link:0, Lane:0)<br>0 0<br>TS1 (Link:0, Lane:0) TS1 (Link:0,  Lane:0) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:1) TS1 (Link:0, Lane:1)<br>1 1<br>TS1 (Link:0, Lane:1) TS1 (Link:0,  Lane:1) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:2) TS1 (Link:0, Lane:2)<br>Lan<br>2 2<br>e<br>TS1 (Link:0, Lane:2) TS1 (Link:0,  Lane:2) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:3) TS1 (Link:0, Lane:3)<br>3 3<br>TS1 (Link:0, Lane:3) TS1 (Link:0,  Lane:3) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>**----- End of picture text -----**<br>


Since a speed change is not requested, the next state is Recovery.Idle. In that state the Ports normally send the logical idle symbols (all zeros) and the Down‐ stream Port does so, as shown in Figure 14‐63 on page 634. However, the Upstream Port was directed to change the Link width so it doesn’t send the expected Idle symbols. Instead, it sends TS1s with PAD for both the Link and Lane numbers. The Downstream Port recognizes that a previously configured Lane now has a Lane number of PAD, and that causes it to transition to the first Configuration substate: Config.Linkwidth.Start. 

**633** 

**PCI Ex ress Technolo p gy** 

## _Figure 14‐63: Link Width Change ‐ Recovery.Idle_ 

**==> picture [311 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex<br>Device<br> (Link:PAD, L ane:PAD)Lane Idle Data Idle Data Lane<br>0 0<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>1 1<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>Lan<br>2 2<br>e<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>3 3<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br>**----- End of picture text -----**<br>


The Downstream Port now initiates the next step by sending TS1s that have the originally negotiated Link number but PAD on all the Lane numbers, as illus‐ trated in Figure 14‐64 on page 635. The Upstream Port responds with matching TS1s on the Lanes it wants to have “active”, but with PAD for both Link and Lane numbers on the Lanes it wishes to have inactive. When the Downstream Port sees this response, it transitions to the Config.Linkwidth.Accept substate. Note that the Autonomous Change bit is set for these TS1s. 

**634** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐64: Marking Active Lanes_ 

**==> picture [335 x 293] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>Lane State<br>Lane Lane<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>0 0 Active<br>TS1 (Link:0, Lane:PAD) TS1 (Link:0, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>1 1 Inactive<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>Lan<br>2 2 Inactive<br>e<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>3 3 Inactive<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-9"></a>
## 14.9 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The Root Port responds by changing its TS1s to show Lane numbers that are appropriate for the active Lanes, but PAD for the Link and Lane numbers of all the Lanes that were seen to be inactive. The Upstream Port responds with the same TS1s, as shown in Figure 14‐65 on page 636, and the state changes to Con‐ fig.Lanenum.Accept. At this point, the Root Port updates the status bit to show that an autonomous change was detected and changes to the Config.Complete substate. 

**635** 

## **PCI Ex ress Technolo p gy** 

## _Figure 14‐65: Response to Lane Number Changes_ 

**==> picture [344 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
g<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>State<br>Lane Lane<br>Link:PAD, Lane:PAD) TS1 (Link:0, Lane: 0) TS1 (Link:0, Lane: 0)<br>0 0 Active<br>TS1 (Link:0, Lane:0) TS1 (Link:0,  Lane:0) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>1 1 Inactive<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Lan<br>2 2 Inactive<br>e<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>3 3 Inactive<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>**----- End of picture text -----**<br>


In the next step, the Root Port begins to send TS2s on the active Lanes and puts the inactive Lanes into Electrical Idle. Recall that the TS2s report whether a com‐ ponent is “upconfigure capable” and in this example, both Link partners sup‐ port this capability. The Endpoint sends back the same thing: TS2s on active Lanes and Electrical Idle on inactive Lanes. Seeing that, the Root Port’s state machine changes to Config.Idle and it begins to send Logical Idle on the active Lanes. The Endpoint responds with the same thing and the Link state changes back to L0. The Link is now ready for normal operation, albeit with a reduced bandwidth for power conservation. 

**636** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐66: Link Width Change ‐ Finish_ 

**==> picture [344 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>Upconfigure Capability = 1 Upconfigure Capability = 1 State<br>Lane Lane<br>Link:PAD, Lane:PAD) TS2 (Link:0, Lane: 0) TS2 (Link:0, Lane: 0)<br>0 0 Active<br>TS2 (Link:0, Lane:0) TS2 (Link:0,  Lane:0) TS1 (Link:PAD, Lane:PAD)<br>Upconfigure Capability = 1 Upconfigure Capability = 1<br>Electrical Idle<br>1 1 Inactive<br>Electrical Idle<br>Lan<br>2 2 Inactive<br>e<br>Electrical Idle<br>3 3 Inactive<br>**----- End of picture text -----**<br>


As was the case for dynamic speed changes, software can’t initiate Link width changes, but it can disable this mechanism by setting the bit in the Link Control register shown in Figure 14‐67 on page 638. Unlike the speed change case, no software mechanism was defined to allow setting a particular Link width. 

**637** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐67: Link Control Register_ 

## **Related Configuration Registers** 

Many of the configuration registers that are relevant to Link Initialization and Training have been shown when their contents were described earlier, but it seems good to summarize them here. 

## **Link Capabilities Register** 

The Link Capabilities Register is pictured in Figure 14‐68 on page 639 and each bit field is described in the subsections that follow. 

**638** 

**Chapter 14: Link Initialization & Training** 

## _Figure 14‐68: Link Capabilities Register_ 

**==> picture [332 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 22 21 20 19 18 17 15 14 12 1110 9 4 3 0<br>Port Number<br>RsvdP<br>ASPM Optionality Compliance<br>Link Bandwidth<br>Notification Capability<br>Data Link Layer Link Active<br>Reporting Capable<br>Surprise Down Error<br>Reporting Capable<br>Clock Power Management<br>L1 Exit Latency<br>L0s Exit Latency<br>Active State<br>Link PM Support<br>Maximum Link Width<br>Max Link Speed<br>**----- End of picture text -----**<br>


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

**639** 

**PCI Ex ress Technolo p gy** 

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

**==> picture [329 x 113] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 9    8   7 1 0<br>RsvdP<br>Crosslink Supported<br>Supported Link<br>Speeds Vector<br>RsvdP<br>**----- End of picture text -----**<br>


**640** 

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

**641** 

**PCI Ex ress Technolo p gy** 

## **Undefined[10]** 

Currently undefined, this bit was previously set by hardware in earlier spec ver‐ sions when a Link Training Error had occurred. It was cleared when the LTSSM successfully entered L0. The spec states that software can write any value to this bit but must ignore any value read from it. 

## **Link Training[11]** 

This read‐only bit indicates that the LTSSM is in the process of training. Techni‐ cally, it means the LTSSM is either in the Configuration or Recovery state, or that the Retrain Link bit has been written to 1b but Link training has not yet begun. This bit is cleared by hardware when the LTSSM exits the Configuration or Recovery state. Since this must be visible to software while Link Training is in progress, it only has meaning for Ports that are facing downstream. Conse‐ quently, this bit is not applicable and reserved for Endpoints, bridge Upstream Ports and Switch Upstream Ports. For them, this bit must be hardwired to 0b. 

_Figure 14‐70: Link Status Register_ 

**==> picture [381 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


## **Link Control Register** 

The Link Control Register is pictured in Figure 14‐71 on page 644, and there are three fields in it that are interesting for us here. 

**642** 

**Chapter 14: Link Initialization & Training** 

## **Link Disable** 

When set to one, the link is disabled. Intuitively, this bit isn’t applicable and is reserved for Endpoints, bridge Upstream Ports, and Switch Upstream Ports because it must be accessible by software even when the Link is disabled. When this bit is written, any read immediately reflects the value written, regardless of the Link state. After clearing this bit, software must be careful to honor the tim‐ ing requirements regarding the first Configuration Read after a Conventional Reset (see “Reset Exit” on page 846). 

## **Retrain Link** 

This bit allows software to initiate Link re‐training whenever it is deemed nec‐ essary, as for error recovery. The bit is not applicable to and is reserved for End‐ point devices and Upstream Ports of Bridges and Switches. When set to 1b, this directs the LTSSM to the Recovery state before the completion of the Configura‐ tion write Request is returned. 

## **Extended Synch** 

As it affects training, this bit is used to greatly extend the time spent in two situ‐ ations, for the purpose of assisting slower external test or analysis hardware to synchronize with the Link before it resumes normal communication. One of these is when exiting L0s, where setting this bit forces the transmission of 4096 FTSs prior to entering L0. The other case is in the Recovery state prior to enter‐ ing Recovery.RcvrCfg, where it forces the transmission of 1024 TS1s. 

**643** 

**PCI Ex ress Technolo p gy** 

## _Figure 14‐71: Link Control Register_ 

**==> picture [313 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


**644** 

## Part Five: 

# Additional System Topics 

## _**15 Error Detection and Handling**_ 

## **The Previous Chapter**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

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

**647** 

**PCI Ex ress Technolo p gy** 

## **Background** 

Software backward compatibility with PCI is an important feature of PCIe, and that’s accomplished by retaining the PCI configuration registers that were already in place. PCI verified the correct parity on each transmission phase of the bus to check for errors. Detected errors were recorded in the Status register and could optionally be reported with either of two side‐band signals: PERR# (Parity Error) for a potentially recoverable parity fault during data transmis‐ sion, and SERR# (System Error) for a more serious problem that was usually not recoverable. These two types can be categorized as follows: 

- Ordinary data parity errors — reported via PERR# 

- Data parity errors during multi‐task transactions (special cycles) — reported via SERR# 

- Address and command parity errors — reported via SERR# 

- • Other types of errors (device‐specific) — reported via SERR# 

How the errors should be handled was outside the scope of the PCI spec and might include hardware support or device‐specific software. As an example, a data parity error on a read from memory might be recovered in hardware by detecting the condition and simply repeating the Request. That would be a safe step if the memory contents weren’t changed by the failed operation. 

As shown in Figure 15‐1 on page 649, both error pins were typically connected to the chipset and used to signal the CPU in a consumer PC. These machines were very cost sensitive, so they didn’t usually have the budget for much in the way of error handling. Consequently, the resulting error reporting signal chosen was the NMI (Non‐Maskable Interrupt) signal from the chipset to the processor that indicated significant system trouble requiring immediate attention. Most consumer PCs didn’t include an error handler for this condition, so the system would simply be stopped to avoid corruption and the BSOD (Blue Screen Of Death) would inform the operator. An example of an SERR# condition would be an address parity mismatch seen during the command phase of a transaction. This is a potentially destructive case because the wrong target might respond. If that happened and SERR# reported it, recovery would be difficult and would probably require significant software overhead. (To learn more about PCI error handling, refer to MindShare’s book _PCI System Architecture_ .) 

PCI‐X uses the same two error reporting signals but defines specific error han‐ dling requirements depending on whether device‐specific error handling soft‐ ware is present. If such a handler is not present, then all parity errors are reported with SERR#. 

**648** 

**Chapter 15: Error Detection and Handling** 

## _Figure 15‐1: PCI Error Handling_ 

**==> picture [370 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
NMI<br>Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data Port<br>PCI 33 MHz<br>Slots<br>CD HDD IDE PERR#<br>Error<br>South Bridge Logic<br>USB SERR#<br>ISA<br>Ethernet SCSI<br>Boot Modem Audio Super<br>ROM Chip Chip I/O<br>COM1<br>COM2<br>**----- End of picture text -----**<br>


PCI‐X 2.0 uses source‐synchronous clocking to achieve faster data rates (up to 4GB/s). This bus targeted high‐end enterprise systems because it was generally too expensive for consumer machines. Since these high‐performance systems also require high availability, the spec writers chose to improve the error han‐ dling by adding Error‐Correcting Code (ECC) support. ECC allows more robust error detection and enables correction of single‐bit errors on the fly. ECC is very helpful in minimizing the impact of transmission errors. (To learn more about PCI‐X error handling, see MindShare’s book _PCI‐X System Architecture_ .) 

PCIe maintains backward compatibility with these legacy mechanisms by using the error status bits in the legacy configuration registers to record error events in PCIe that are analogous to those of PCI. That lets legacy software see PCIe error events in terms that it understands, and allows it to operate with PCIe hardware. See “PCI‐Compatible Error Reporting Mechanisms” on page 674 for the details of these registers. 

**649** 

**PCI Ex ress Technolo p gy** 

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

**650** 

**Chapter 15: Error Detection and Handling** 

- PCI Express Capability Registers — these registers will only be useful to newer software that is aware of PCIe, but they provide more error informa‐ tion specifically for PCIe software. 

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

**651** 

**PCI Ex ress Technolo p gy** 

required to be reported to software, but doing so could allow software to track error trends that might indicate that some devices are showing signs of immi‐ nent failure. 

## **Uncorrectable Errors** 

Errors that can’t be automatically corrected in hardware are called Uncorrect‐ able, and these are either Non‐fatal or Fatal in severity. 

## **Non-fatal Uncorrectable Errors** 

Non‐fatal errors indicate that information has been lost but the cause was likely something other than the integrity of a Link or Device. A packet failed some‐ where, but the Link continues to function correctly and other packets are unaf‐ fected. Since the Link is still working, recovery of the lost information may be possible, but will depend on implementation‐specific software to handle it. An example of this error type would be a Completion timeout, in which a Request was sent but no Completion was returned within the allowed time. Somewhere there was an issue, but it could be something as simple as a random bit error within a Switch that caused the Completion to be routed incorrectly. An attempt at recovery for this case could be as simple as re‐issuing the Request. 

## **Fatal Uncorrectable Errors**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

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

**652** 

**Chapter 15: Error Detection and Handling** 

interrupts. Each layer of the interface includes error checking capabilities, and these are summarized in the sections that follow. 

_Figure 15‐2: Scope of PCI Express Error Checking and Reporting_ 

**==> picture [291 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) Link (RX) (TX)<br>Scope of PCIe Error Reporting<br>**----- End of picture text -----**<br>


## **CRC** 

Before diving into error handling as it relates to the layers, it will help to first discuss the concept of CRC (Cyclic Redundancy Check) because it’s an integral part of PCIe error checking. A CRC code is calculated by the transmitter based on the contents of the packet and adds it to the packet for transmission. The CRC name is derived from the fact that this _check_ code (calculated from the packet to check for errors) is _redundant_ (adds no information to the packet), and is derived from _cyclic_ codes. Although a CRC doesn’t supply enough informa‐ tion to do automatic error correction the way ECC (Error Correcting Code) can, it does provide robust error detection. CRCs are also commonly used in serial transports because they’re good at detecting a string of incorrect bits. 

**653** 

## **PCI Ex ress Technolo p gy** 

CRCs have two different usage cases in PCIe. One is the mandatory LCRC (Link CRC) generated and checked in the Data Link Layer for every TLP that goes across a Link. It’s intended to detect transmission errors on the Link. 

The second is the optional ECRC (End‐to‐end CRC) that’s generated in the Transaction Layer of the sender and checked in the Transaction Layer of the ulti‐ mate target of the packet. This is intended to detect errors that might otherwise be silent, such as when a TLP passes through an intermediate agent like a Switch, as shown in Figure 15‐3 on page 654. In this illustration, the packet arrived safely on the downstream port of the Switch but while it was being stored or processed within the Switch a bit error occurred. The LCRC only pro‐ tects TLPs while on the Link. Once the Data Link Layer of the Ingress Port checks the LCRC, it removes it from the packet because a new LCRC will be cal‐ culated (which will include the new Sequence Number) at the Egress Port. This means that the packet is unprotected while inside the Switch. This is the pur‐ pose of having an ECRC. It is calculated at the originating device and is not removed or recalculated by intermediate devices. So if the target device is checking the ECRC and sees a mismatch, then there must have been an error somewhere along the way even though no LCRC error was seen. Note that using the ECRC requires the presence of the optional Advanced Error Report‐ ing registers, since they contain the bits to enable this functionality. 

_Figure 15‐3: ECRC Usage Example_ 

**==> picture [267 x 192] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>Internal<br>Bit Error Switch<br>No external  (LCRC)<br>transmission errors<br>PCIe<br>Endpoint<br>**----- End of picture text -----**<br>


**654** 

**Chapter 15: Error Detection and Handling** 

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

**655** 

**PCI Ex ress Technolo p gy** 

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

**656** 

**Chapter 15: Error Detection and Handling** 

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

**657** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐4: Location of Error‐Related Configuration Registers_ 

**==> picture [287 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
Byte 0d<br>Status Command<br>Header<br>63d CapPtr<br>PCI<br>Required Compatible<br>PCIe Capability Block<br> Space<br>255d<br>Advanced Error Reporting<br>Optional<br> Capability Structure<br>Other PCIe Extended<br>Capability Structures Capability<br> Space<br>4095d<br>**----- End of picture text -----**<br>


A device enabled to generate ECRCs originates a TLP (Request or Completion), computes the 32‐bit ECRC based on the header and data portions of the packet and adds it to the end of the packet. The ECRC is called “end‐to‐end” because the intent is that it will be generated at the TLP’s origin and never stripped off or regenerated by any intermediate device along its path. Switches in the path between the originating and receiving devices are allowed to check and report ECRC errors but aren’t required to do so. Whether or not there is an error, a Switch must still forward the packet unaltered so that the ultimate target device can evaluate the ECRC and take appropriate steps. If a Switch is acting as the originator or recipient of the TLP it can participate like an ordinary device in ECRC generation and checking. For more on the topic of how a Switch is allowed to report such errors, see “Advisory Non‐Fatal Errors” on page 670. 

**658** 

**Chapter 15: Error Detection and Handling** 

## **TLP Digest**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-12"></a>
## 14.12 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

If the optional ECRC capability is enabled, a special bit called TD (TLP Digest) is set in the header to indicate that it’s present at the end of the packet (the ECRC is also called the Digest). The TD bit in the packet header is shown in Figure 15‐ 5 on page 659. The spec emphasizes that this bit must be treated with special care when forwarding a TLP because if it’s missing but the ECRC is present, or vice‐versa, then the packet will be considered Malformed. 

_Figure 15‐5: TLP Digest Bit in a Completion Header_ 

**==> picture [373 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


## **Variant Bits Not Included in ECRC Mechanism** 

The ECRC is calculated based on the contents of the header and data. Since these are not expected to change, the result should be the same when the check is performed at the receiver. However, it turns out that two header bits can legally change while the packet is in flight: bit 0 of the Type field, and the EP bit. Bit 0 of the Type field can change in Configuration Requests for the simple rea‐ son that the Request will be Type 1 until it has reached its destination bus, and then it will become Type 0. That involves changing bit 0 of the Type field. The EP bit can also be legally changed by intermediate devices if they detect a data error. For example, if a Switch forwards a TLP but it suffers an internal error of some kind that corrupts the data, setting the EP bit as it goes out the Egress Port is one way to report the error (known as error forwarding or data poisoning). 

Since these two bits can change while the packet is in flight they are called “variant bits” and cannot be used in the generation or checking of ECRC. Instead, their values are always assumed to be 1b for ECRC generation and checking instead of using the actual values. That way the ECRC doesn’t depend on them and will be correctly evaluated. 

**659** 

**PCI Ex ress Technolo p gy** 

The actions taken when an ECRC error is detected are beyond the scope of the spec, but the possible choices will depend on whether the error is found in a Request or a Completion. 

- **ECRC in Request** — Completers that detect an ECRC error must set the ECRC error status bit. They may also choose not to return a Completion for this Request, resulting in a Completion timeout at the Requester, whose software might then choose to reschedule the Request. 

- **ECRC in Completion** — Requesters that detect an ECRC error must set the ECRC error status bit. Besides the standard error reporting mechanism, they may also choose to report the error to their device driver with a Func‐ tion‐specific interrupt. As before, the software might decide to reschedule the failed Request. 

In either case, an Uncorrectable Non‐fatal error Message may be sent to the sys‐ tem. If so, the device driver would probably be accessed to check the status bits in the _Uncorrectable Error Status Register_ and learn the nature of the error. If pos‐ sible, the failed Request may be rescheduled, but other steps might be needed. 

## **Data Poisoning** 

Data poisoning, also called Error Forwarding, provides an optional way for a device to indicate that the data associated with a TLP is corrupted. In these cases, the EP (Error Poisoned) bit in the packet header is set to indicate the error. The EP bit is shown in Figure 15‐6 on page 660. 

_Figure 15‐6: The Error/Poisoned Bit in a Completion Header_ 

**==> picture [373 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


**660** 

**Chapter 15: Error Detection and Handling** 

Anytime data is transferred, such as in write Requests or Completions with data, corruption of that data could happen which needs to be reported to the target device. In each of these cases, the packet can be forwarded to the recipient but marked as having bad data by the EP bit in the header. The thoughtful reader may wonder why one might want to send data that is already known to be bad. As it happens, there are some cases where it’s useful: 

1. If a Request results in a Completion returned with data, but that data encountered an error as it was gathered from the target (like a parity or ECC failure in memory), then what is the best way to report it? One approach would be not to send the Completion at all but, if the error isn’t reported in some other way, the system only sees a Completion timeout at the Requester. That response isn’t very helpful because any number of prob‐ lems might result in that outcome. 

   - If, on the other hand, the Completion is delivered with the poisoned bit set, then at least the Requester can see that the round‐trip path to the Completer must have been working correctly. Therefore, the problem must have occurred internally to the Completer or else in a Switch that was in the path. What steps will be taken will be implementation specific, but more is known about what must have gone wrong than if the Completion simply timed out. 

2. It can be used to report an intermediate problem. If a data payload is cor‐ rupted while passing through a Switch, the packet can still be forwarded with the EP bit set to indicate the problem. 

3. It may be that the target device can accept the data with errors. As an exam‐ ple, an audio output device needs to receive a timely data stream to work well. If incoming data has an error, the consequences are small (glitch in the audio output) and the time to recover would be long enough to cause a noticeable delay, so it can be better to take it as is rather than attempting recovery of the data. 

4. A target device might have a means of correcting the data. The data might be directly recoverable, or the target might have a means of re‐creating parts of it, or have some other means of working around the problem. 

The spec states that data poisoning applies only to the data payload associated with a packet (such as Memory, Configuration, or I/O writes and Completions) and never to the contents of the TLP header. Consequently, a receiver’s behavior is undefined if it sees a poisoned packet (EP=1) with no payload (like a poisoned memory read). Poisoning can only be done at the Transaction Layer of a device; the Data Link Layer does not examine or affect the contents of the TLP header. 

Error forwarding support is stated to be optional for transmitters, and the absence of such a statement for receivers implies that it’s not optional for them. 

**661** 

## **PCI Ex ress Technolo p gy** 

If a transmitter supports it, it’s enabled with the Parity Error Response bit in the legacy Command register. That’s because a Poisoned packet is roughly analo‐ gous to a parity error in PCI, since that’s how PCI reports bad data. Receipt of a poisoned packet may be reported to the system with an error Message if enabled and, if the optional Advanced Error Reporting registers are present, will also set the Poisoned TLP status bit. 

As one might expect, poisoned writes to control locations are not allowed to modify the contents in the target. Examples given in the spec are Configuration writes, IO or memory writes to control registers, and AtomicOps. Switches that receive poisoned packets must forward them unchanged to the destination port although, if they’ve been enabled to do so, they must report this packet as an error to help software determine where the error happened. Completers that receive a poisoned non‐posted Request are expected to return a Completion with a status of UR (Unsupported Request). 

## **Split Transaction Errors** 

A variety of failures can occur during a split transaction associated with non‐ posted requests. PCIe defines a status field within the Completion header that allows the Completer to report some errors back to the Requester. Figure 15‐7 on page 662 illustrates the location of this field in a completion header and Table 15‐1 on page 663 gives the possible values. As the table shows, only four encodings are defined, two of which represent error conditions. 

_Figure 15‐7: Completion Status Field within the Completion Header_ 

**==> picture [378 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 x 0 0 1 0 1 0 tr H D P 0 0<br>Compl. B<br>Byte 4 Completer ID Status MC Byte Count<br>Byte 8 Requester ID Tag R Lower Address<br>**----- End of picture text -----**<br>


**662** 

**Chapter 15: Error Detection and Handling** 

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

**663** 

**PCI Ex ress Technolo p gy** 

## **Completer Abort (CA) Status** 

Several circumstances can occur that could result in a Completer returning this CA status to the Requester. Some examples are: 

- Completer receives a Request that it cannot complete without violating its programming rules. For example, some Functions may be designed to only allow accesses to some registers in a complete and aligned manner (e.g. a 4‐ byte register may require a 4‐byte aligned access). Any attempt to access one of these registers in a partial or misaligned fashion (e.g. reading only two bytes of a 4‐byte register) would fail. Such restrictions are not violations of the spec, but rather legal constraints associated with the programming interface for this Function. Access to such a Function is based on the expec‐ tation that the device driver understands how to access its Function.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

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

**664** 

**Chapter 15: Error Detection and Handling** 

## **Completion Timeout** 

For the case of a pending Request that never receives the Completion it’s expect‐ ing, the spec defines a Completion timeout mechanism. The spec clearly intends this to detect when a Completion has no reasonable chance of returning; it should be longer than any normal expected latencies. 

The Completion timeout timer must be implemented by all devices that initiate Requests that expect Completions, except for devices that only initiate configu‐ ration transactions. Note also that every Request waiting for Completions is timed independently, and so there must be a way to track time for each out‐ standing transaction. The 1.x and 2.0 versions of the spec defined the permissi‐ ble range of the timeout value as follows: 

- It is strongly recommended that a device not timeout earlier than 10ms after sending a Request; however, if the device requires greater granularity a tim‐ eout can occur as early as 50μs. 

- Devices must time‐out no later than 50ms. 

Beginning with the 2.1 spec revision, the Device Control Register 2 was added to the PCI Express Capability Block to allow software visibility and control of the timeout values, as shown in Figure 15‐8 on page 665. 

_Figure 15‐8: Device Control Register 2_ 

**==> picture [152 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 oO 0000b = 50µs - 50ms<br>0001b = 50µs - 100µs<br>A<br>0010b = 1ms - 10ms<br>EK of<br>0101b = 16ms - 55ms<br>B<br>0110b = 65ms - 210ms<br>1001b = 260ms - 900ms<br>C<br>1010b = 1s - 3.5s<br>1100b = 4s - 13s<br>D<br>[ 1110b = 17s - 64s<br>High-order bits<br>select range<br>**----- End of picture text -----**<br>


If Requests need multiple Completions to return the requested data, a single Completion won’t stop the timer. Instead, the timer continues to run until all the data has been returned regardless of how many Completions are needed. If only part of the data has been returned when the timeout occurs, the Requester may discard or keep that data. 

**665** 

**PCI Ex ress Technolo p gy** 

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

**666** 

**Chapter 15: Error Detection and Handling** 

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

**667** 

**PCI Ex ress Technolo p gy** 

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

**668** 

**Chapter 15: Error Detection and Handling** 

_Table 15‐2: Error Message Codes and Description_ 

**==> picture [389 x 479] intentionally omitted <==**

**----- Start of picture text -----**<br>
Message<br>Name Description<br>Code<br>30h ERR_COR Device detected a correctable error. This is automati‐<br>cally corrected by hardware and doesn’t require soft‐<br>ware attention. However, it can be helpful to report<br>them anyway so software can watch for trends like<br>an increasing number of correctable errors.<br>31h ERR_NONFATAL Indicates an uncorrectable Non‐Fatal error. No hard‐<br>ware correction mechanism was available but the<br>Link is still working reliably. Software attention will<br>be required to resolve the problem.<br>33h ERR_FATAL Indicates an uncorrectable Fatal error. No hardware<br>correction mechanism was available and Link opera‐<br>tion has failed in some important respect. Software<br>attention will be required and a reset of at least one<br>device will probably be required to resolve this issue.<br>Figure 15‐9: Error Message Format<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 1 1 0  0 0 0 tr H D P<br>Message Code<br>Byte 4 Requester ID Tag<br>(30h, 31h or 33h)<br>Byte 8 Reserved for Error Messages<br>Byte 12 Reserved for Error Messages<br>Route to Root Complex 30h = ERR_COR<br>31h = ERR_NONFATAL<br>33h = ERR_FATAL<br>**----- End of picture text -----**<br>


**669** 

**PCI Ex ress Technolo p gy** 

## **Advisory Non-Fatal Errors**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

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

**==> picture [264 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capabilities Register<br>31 28 27 26 25 18 17 16 15 14 12 11 9 8 6 5 4 3 2 0<br>RsvdP RsvdP<br>Function-Level Reset Capability<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>Role-Based Error Reporting<br>Undefined<br>Endpoint L1 Acceptable Latency<br>Endpoint L0s Acceptable Latency<br>Extended Tag Field Supported<br>Phantom Functions Supported<br>Max Payload Size Supported<br>**----- End of picture text -----**<br>


**670** 

**Chapter 15: Error Detection and Handling** 

In spite of the reasons just described, software might want to stop operation as soon as some advisory errors are seen by an intermediate device. Since newer devices will always perform role‐based error reporting, an override mechanism is needed. To handle this case, software can escalate the severity of the advisory errors from Non‐Fatal to Fatal in the AER (Advanced Error Reporting) registers. Since there is no “advisory fatal” case, the error will now be reported as a Fatal Error (ERR_FATAL), if enabled, regardless of the role of the device. 

## **Advisory Non-Fatal Cases** 

The spec lists five situations for which an advisory message (ERR_COR) is pre‐ ferred over a ERR_NONFATAL message. In each of these cases, the detecting agent will handle the error as an Advisory Non‐Fatal Error. This means that a Non‐Fatal condition will be handled by sending an ERR_COR, assuming the agent has AER registers and has enabled ERR_COR. If it doesn’t have AER reg‐ isters or ERR_COR was not enabled, it sends no Error Message. The five cases are as follows: 

1. Completer sent a Completion with UR or CA Status. The expectation in this case is that the Requester will have a mechanism to handle the error when it sees the offending Completion and will be the best agent to send whatever Error Messages are needed. A ERR_NONFATAL message from the Compl‐ eter would just be confusing, so it must be handled as Advisory Non‐Fatal (ERR_COR). 

   - Curiously, there is no PCIe mechanism for the Requester to report that it received a Completion with this status. Instead, a design‐specific method like an interrupt will be needed to get device driver attention. An important example of this happens when the Root Complex receives a Completion with UR or CA status in response to a Configuration Read Request. On some platforms the response is to return all 1’s to software for this case, to support backward compatibility with PCI enumeration (configuration probing) software. 

2. Intermediate device detected an error. This case comes up in systems that employ Switches because a detecting agent may not be the final destination for a TLP. As an example of this, consider Figure 15‐11 on page 672, show‐ ing a poisoned packet delivered through an intermediate Switch. The TLP is seen as a Non‐Fatal error by the Switch but it can only signal an ERR_COR message instead (as long as it’s enabled to do so). To explore this concept a little more, why wouldn’t we want the Switch to report ERR_NONFATAL? One reason is seen by looking at error tracking in the AER registers. Figure 15‐12 on page 672 shows the AER registers that track the Source ID (BDF of the sending device) of Error Messages coming into a Root Port and we can see that there’s only one space available for 

**671** 

## **PCI Ex ress Technolo p gy** 

uncorrectable errors. If multiple uncorrectable errors are seen, that fact will be noted but only the first source ID will be saved since it is considered to be the probable cause of subsequent errors. It’s important, therefore, that uncorrectable errors come from the most appropriate device to report them. It’s worth noting that it’s still helpful for intermediate devices to report ERR_COR, because it allows software to determine where the error was first detected. 

_Figure 15‐11: Role‐Based Error Reporting Example_ 

**==> picture [230 x 219] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Poisoned<br>Packet<br>ERR_COR<br>PCIe<br>PCIe Switch Endpoint<br>Endpoint<br>PCIe Legacy<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


_Figure 15‐12: Advanced Source ID Register_ 

**==> picture [333 x 77] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Source Identification Register<br>of the AER Capability Structure<br>31 0<br>ERR_FATAL/NONFATAL Source ID ERR_COR Source ID<br>(ROS) (ROS)<br>ROS: Read-Only and Sticky<br>**----- End of picture text -----**<br>


**672** 

**Chapter 15: Error Detection and Handling** 

As another example, 1.0a devices that have the UR Reporting Enable bit cleared but don’t have the Role‐Based Error Reporting capability are unable to report any error Messages when a UR error is detected (for posted or non‐posted Requests). In contrast, a 1.1‐compliant or later Completer that has the SERR# Enable bit set will send an ERR_NONFATAL or ERR_FATAL message for bad posted Requests, even if the Unsupported Request Report‐ ing Enable bit is clear, so as to avoid silent data corruption. But it won’t send an error Message for non‐posted Requests received, so as to support the PCI‐compatible configuration method of probing with configuration reads. It’s recommended that software keep the UR Error Reporting Enable bit clear for devices that are not capable of Role‐Based Error Reporting, but set it for those that are. That way, UR errors are reported on bad posted requests, but not for bad non‐posted requests like configuration probing transactions, and backward compatibility with older software is main‐ tained. 

The spec also mentions that poisoned TLPs sent to the Root will be handled in the same way if the Root is acting as an intermediate agent, but there is one exception: If the Root doesn’t support Error Forwarding, it will be unable to communicate the poisoned error with the TLP and must report this as a Non‐Fatal error instead. 

3. Destination device received a poisoned TLP. Normally, Endpoints would report the Non‐Fatal error in this case, but there’s an exception to this rule: If the ultimate destination device is able to handle the poisoned data in a way that allows for continued operation, it must treat this case as an Advi‐ sory Non‐Fatal Error instead. 

   - An example of this behavior might be an audio device that receives stream‐ ing data that has been poisoned. In this situation, the data may be accepted even though it’s known to be corrupted because pausing the audio flow long enough to get software attention and take remedial action would be a worse alternative than allowing a glitch in the sound output. 

4. Requester experienced a Completion Timeout. This is a similar case to the previous one; if the Requester has a means of continuing operation in spite of the problem then it must treat this as an Advisory Non‐Fatal Error. A simple work‐around for the Requester in this case would simply be to send the request again and hope for better results this time. Clearly, this would only make sense if the previous request did not cause any side effects, but Requesters are permitted to do this as often as they like (although the spec says the number of retries must be finite). 

5. Unexpected completion received. This must be handled as an Advisory Non‐Fatal Error. The reason is that it was probably caused by a mis‐routed Completion and the original Requester will eventually report a Completion timeout. To allow that other Requester to attempt a retry of the failed 

**673** 

**PCI Ex ress Technolo p gy** 

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

**674** 

**Chapter 15: Error Detection and Handling** 

## **Legacy Command and Status Registers** 

Figure 15‐13 on page 675 illustrates the Command register and the location of the error‐related fields. These bits are set to enable baseline error reporting under control of PCI‐compatible software. Table 15‐3 defines the specific effects of each bit. 

_Figure 15‐13: Command Register in Configuration Header_ 

**==> picture [390 x 396] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-15"></a>
## 14.15 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

15 11 10 9 8 7 6 5 4 3 2 1 0<br>Reserved 0 0 0 0 0<br>Interrupt Disable<br>Fast Back-to-back Enable *<br>SERR# Enable<br>Stepping Control *<br>Parity Error Response<br>VGA Palette Snoop Enable *<br>Mem Write & Invalidate Enable *<br>Special Cycles *<br>Bus Master Enable<br>Memory Space Enable<br>IO Space Enable<br>* Not used in PCIe, these must be set to zero<br>Table 15‐3: Error‐Related Fields in Command Register<br>Name Description<br>SERR# Enable Setting this bit enables sending ERR_FATAL and ERR_NONFATAL<br>error messages to the Root Complex. These are considered roughly<br>analogous to asserting the System Error (SERR#) signal in PCI.<br>For Type 1 headers (bridges), this bit controls the forwarding of<br>ERR_FATAL and ERR_NONFATAL error messages from the sec‐<br>ondary interface to the primary interface.<br>This field has no affect over ERR_COR messages.<br>**----- End of picture text -----**<br>


**675** 

**PCI Ex ress Technolo p gy** 

_Table 15‐3: Error‐Related Fields in Command Register (Continued)_ 

|**Name**|**Description**|
|---|---|
|Parity Error<br>Response|Setting this bit enables logging of poisoned TLPs in the Master Data<br>Parity Error bit in the Status register.<br>Poisoned packets indicate bad data and are roughly analogous to a<br>PCI parity error.|



Figure 15‐14 on page 676 illustrates the Configuration Status register and the location of the error‐related bit fields. Table 15‐4 on page 677 defines the circum‐ stances under which each bit is set and the actions taken by the device when error reporting is enabled. 

_Figure 15‐14: Status Register in Configuration Header_ 

**==> picture [304 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 8 7 6 5 4 3 2 0<br>0  0 0 R 0 1 Reserved<br>Interrupt Status<br>Capabilities List**<br>66 MHz Capable*<br>Reserved<br>Fast Back-to-back Capable*<br>Master Data Parity Error<br>DEVSEL Timing*<br>Signalled Target Abort<br>Received Target Abort<br>Received Master Abort<br>Signalled System Error<br>Detected Parity Error<br>* Not used in PCIe, these must be set to zero<br>** Must be set to one because some capability registers are required<br>**----- End of picture text -----**<br>


**676** 

**Chapter 15: Error Detection and Handling** 

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

**677** 

**PCI Ex ress Technolo p gy** 

Figure 15‐15 on page 678 illustrates the PCI Express Capability structure. Some of these registers provide support for: 

- Enabling/disabling error reporting (Error Message Generation) 

- Providing error status 

- Providing link training status and initiating link re‐training 

_Figure 15‐15: PCI Express Capability Structure_ 

**==> picture [336 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 15 7 0<br>PCI Express Capabilities Register Next Cap Pointer PCI ExpressCap ID DW0<br>Device Capabilities Register DW1<br>Device Status Device Control DW2<br>{<br>Link Capabilities DW3<br>Link Status Link Control DW4<br>{<br>Slot Capabilities DW5<br>Slot Status Slot Control DW6<br>{<br>Root Capability Root Control DW7<br>Root Status DW8<br>{<br>{<br>Device Capabilities 2 DW9<br>Device Status 2 Device Control 2 DW10<br>{<br>Link Capabilities 2 DW11<br>Link Status 2 Link Control 2 DW12<br>{<br>Slot Capabilities 2 DW13<br>Slot Status 2 Slot Control 2 DW14<br>{<br>Gen2 and later devices only<br>ks Pstro<br>niL ll<br>h A<br>Solst tiswe<br>h<br>ti civ<br>w e<br>str str D<br>o o r<br>P P x o<br>t tc<br>Roo elpmo Cello<br>C t<br>t n<br>o e<br>o v<br>R E<br>ks Pstro<br>niL llA<br>h<br>Solst tiswe<br>h<br>ti civ<br>w e<br>str D<br>o<br>P<br>**----- End of picture text -----**<br>


## **Enabling/Disabling Error Reporting** 

The Device Control registers allow software to enable generation of three differ‐ ent Error Messages for four error events, and Device Status registers allow it to see which error has been detected. The four error cases are: 

**678** 

**Chapter 15: Error Detection and Handling** 

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



**679** 

**PCI Ex ress Technolo p gy** 

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

**680** 

**Chapter 15: Error Detection and Handling** 

For Correctable Errors, a Function will only send the ERR_COR message if the _Correctable Error Reporting Enable_ bit in the Device Control register is set. There is no control to enable ERR_COR messages from the PCI‐Compatible mechanisms, which makes sense because in PCI, there was no concept of correctable errors. 

_Figure 15‐16: Device Control Register Fields Related to Error Handling_ 

**==> picture [357 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 12 11 10 9 8 7 5 4 3 2 1 0<br>Bridge Config. Retry Enable/<br>Initiate Function-Level Reset<br>Max Read Request Size<br>Enable No Snoop<br>Aux Power PM Enable<br>Phantom Functions Enable<br>Extended Tag Field Enable<br>Max Payload Size<br>Enable Relaxed Ordering<br>Unsupported Request<br>Reporting Enable<br>Fatal Error Reporting Enable<br>Non-Fatal Error<br>Reporting Enable<br>Correctable Error<br>Reporting Enable<br>**----- End of picture text -----**<br>


**Device Status Register.** An error status bit is set in the Device Status reg‐ ister, shown in Figure 15‐17 on page 682, anytime an error associated with its classification is detected, regardless of the setting of the error reporting enable bits in the Device Control Register. Because Unsupported Request errors are considered Non‐Fatal Errors, when these errors occur both the _Non‐Fatal Error Detected_ status bit and the _Unsupported Request Detected_ sta‐ tus bit will be set. Like several other status bits, these are “Sticky” (their val‐ ues are not cleared by a reset event so they’ll be available for diagnosing problems even if a reset was needed to get the Link working well enough to read the status). 

**681** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐17: Device Status Register Bit Fields Related to Error Handling_ 

**==> picture [337 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 6 5 4 3 2 1 0<br>RsvdZ<br>Transactions Pending<br>Aux Power Detected<br>Unsupported Request Detected<br>Fatal Error Detected<br>Non-Fatal Error Detected<br>Correctable Error Detected<br>**----- End of picture text -----**<br>


## **Root’s Response to Error Message**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-14-16"></a>
## 14.16 Link Initialization & Training | 链路初始化与训练

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

When an Error Message is received by the Root, the action it takes is determined in part by the settings in the Root Control Register. Figure 15‐18 depicts this reg‐ ister and highlights the three fields that specify whether a received Error Mes‐ sage should be reported as System Error. In some x86‐based systems, it’s likely that an NMI (Non‐Maskable Interrupt) will be signaled if the error is enabled to trigger a System Error. 

Other options for reporting Error Messages are not configurable via standard registers. The most likely scenario is that an interrupt will be signaled to the processor that will call an Error Handler, which may log the error and attempt to clear the problem. 

**682** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐18: Root Control Register_ 

**==> picture [313 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 5 4 3 2 1 0<br>RsvdP<br>CRS Software Visibility Enable<br>PME Interrupt Enable<br>System Error on Fatal Error Enable<br>System Error on Non-Fatal Error Enable<br>System Error on Correctable Error Enable<br>**----- End of picture text -----**<br>


## **Link Errors** 

Link failures are typically detected in the Physical Layer and communicated to the Data Link Layer. For a downstream device, if the link has incurred a Fatal error and is not operating correctly, it can’t report the error to the host. For these cases, the error must be reported by the upstream device. If software can isolate errors to a given link, one step in handling an uncorrectable error (or to prevent future uncorrectable errors) is to retrain the Link. The Link Control Register includes a bit that allows software to force the Link to retrain, as shown inFig‐ ure 15‐19 on page 684. If that solves the problem, operation resumes with little downtime. 

**683** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐19: Link Control Register ‐ Force Link Retraining_ 

**==> picture [297 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


Having once requested retraining, software can poll the _Link Training_ bit in the Link Status Register to see when training has completed. Figure 15‐20 high‐ lights this status bits. When this bit is 1b, the Link is still in the retraining pro‐ cess (or has yet to start retraining). Hardware will clear this bit once the Physical Layer reports the Link as active meaning the training process has completed successfully. 

**684** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐20: Link Training Status in the Link Status Register_ 

**==> picture [360 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


## **Advanced Error Reporting (AER)** 

The Advanced Error Reporting Structure illustrated in Figure 15‐21 on page 686 allows for much more sophisticated error handling. These registers provide several additional features: 

- Better granularity in logging the actual type of error that occurred 

- Control to specify the severity of each uncorrectable error type 

- Support for logging the header of packets that had errors 

- Standardizing control for the Root to report received Error Messages with an interrupt 

- Identifying the source of the error in the PCIe topology 

- Ability to mask reporting individual types of errors 

**685** 

## **PCI Ex ress Technolo p gy** 

_Figure 15‐21: Advanced Error Capability Structure_ 

|Root Ports &<br>Root Complex<br>Event Collectors<br>Functions<br>that support<br>TLP Prefixes|Root Error Command<br>Root Error Status<br>Uncorr.  Error Source ID<br>Corr.  Error Source ID<br>TLP Prefix Log Register<br>00h<br>04h<br>08h<br>0Ch<br>10h<br>14h<br>18h<br>1Ch<br>2Ch<br>30h<br>34h<br>38h<br>PCIe Extended CapabilityRegister<br>Uncorrectable Error Status Register<br>Uncorrectable Error Mask Register<br>Uncorrectable Error SeverityRegister<br>Correctable Error Status Register<br>Correctable Error Mask Register<br>Advanced Error Capability and Control Register<br>Header Log Register|
|---|---|



## **Advanced Error Capability and Control** 

Let’s begin our discussion of AER by looking at the Advanced Error Capability and Control register. End‐to‐End CRC (ECRC) generation and checking requires AER, and this register, shown in Figure 15‐22 on page 687, reports 

**686** 

**Chapter 15: Error Detection and Handling** 

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

**687** 

**PCI Ex ress Technolo p gy** 

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

**688** 

**Chapter 15: Error Detection and Handling** 

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

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

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

**689** 

## **PCI Ex ress Technolo p gy** 

- Replay Timer Timeout — At the Data Link Layer, transmitted TLPs have not received an acknowledgement (Ack or Nak) within the timeout period. Hardware automatically replays all unacknowledged TLPs, meaning all packets in the Replay Buffer. 

- Advisory Non‐Fatal Error — Detection of these cases (see “Advisory Non‐ Fatal Errors” on page 670) is logged in the corresponding Uncorrectable Error Status register and as a correctable error here. It may also generate a Correctable Error Message, if enabled. 

- Corrected Internal Error (optional) — An error internal to the device was detected, but it was corrected or worked around without causing improper behavior. 

- Header Log Overflow (optional) — The maximum number of headers that can be stored in the header log has been reached. The number is just one if the Multiple Header Recording Enable bit is not set in the Advanced Error Capability and Control register. 

## **Advanced Correctable Error Masking** 

Correctable Error reporting is controlled collectively by the Correctable Error Enable bit in the Device Control register, but also individually by the Correct‐ able Mask register, illustrated in Figure 15‐24. The default state of the mask bits is cleared, meaning an ERR_COR message can be delivered when any correct‐ able errors are detected if they’ve been enabled (meaning the Correctable Error Enable bit is set). However, software may choose to set bits in this mask register to prevent a message from being sent when those specific errors are detected. 

_Figure 15‐24: Advanced Correctable Error Mask Register_ 

**==> picture [353 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 14 13 12 11 9 8 7 6 5 1 0<br>RsvdP RsvdP RsvdP<br>Header Log Overflow Mask<br>Corrected Internal Error Mask<br>Advisory Non-Fatal Error Mask<br>Replay Timer Timeout Mask<br>REPLAY_NUM Rollover Mask<br>Bad DLLP Mask<br>Bad TLP Mask<br>Receiver Error Mask<br>Note: all bits designated RWS<br>**----- End of picture text -----**<br>


**690** 

**Chapter 15: Error Detection and Handling** 

## **Advanced Uncorrectable Error Handling** 

For uncorrectable errors, AER provides the ability to track which specific error has occurred, control whether it should be considered Fatal or Non‐Fatal, and choose whether it will result in an Uncorrectable Error Message being sent to the Root. 

## **Advanced Uncorrectable Error Status** 

When an uncorrectable error occurs, the corresponding bit in this register is automatically set by hardware (see Figure 15‐25 on page 691) regardless of whether the error will be reported to the Root. If multiple errors occur, hard‐ ware will set the corresponding bit for each error and will record which one was first in the First Error Pointer field of the Advanced Error Capability and Con‐ trol register. It may even happen that multiple instances of the same error are detected before the first one can be serviced. Hardware that is compliant with the 2.1 spec revision or later will be able to keep track of a design‐specific num‐ ber of those cases. 

_Figure 15‐25: Advanced Uncorrectable Error Status Register_ 

**==> picture [366 x 184] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdZ RsvdZ RsvdZ<br>TLP Prefix Blocked Error Status<br>Atomic Op Egress Blocked Status Undefined<br>MC Blocked TLP Status<br> Uncorrectable Internal Error Status<br>ACS Violation Status<br>Data Link<br>Unsupported Request Error Status Protocol<br>ECRC Error Status Error Status<br>Malformed TLP Status<br>Surprise Down<br>Receiver Overflow Status Error Status<br>Unexpected Completion Status<br>Completer Abort Status<br>Completion Timeout Status<br>Flow Control Protocol Error Status<br>Poisoned TLP Status<br>Note: all bits designated RW1CS<br>**----- End of picture text -----**<br>


The following list describes each of the register bits from right to left: 

- Undefined — Previously, this first bit represented a link training failure at the Physical Layer, but that meaning was removed with the 1.1 revision of 

**691** 

## **PCI Ex ress Technolo p gy** 

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

**692** 

**Chapter 15: Error Detection and Handling** 

   - grammed to block AtomicOps from being forwarded to agents that shouldn’t see them (see “AtomicOps” on page 897). 

- TLP Prefix Blocked Error — Egress Ports of routing elements can be pro‐ grammed not to forward TLPs containing End‐to‐End TLP Prefixes. If they then see one, they’ll drop the TLP and report this error. For more on this, see “TPH (TLP Processing Hints)” on page 899. 

Recall that the First Error Pointer in the Capability and Control Register indi‐ cates which unmasked uncorrectable error was the first to arrive since the pointer was last updated. Error handling software can read the pointer to find out which error to investigate first. As an example, if the pointer value is 18d, that means bit position 18 in the Uncorrectable Status register was first, which is a Malformed TLP. Once that error has been serviced, software writes a one to bit 18 in the status register to clear that event, which updates the First Error Pointer to the next‐most‐recent error 

## **Selecting Uncorrectable Error Severity** 

Software can select whether or not uncorrectable errors should be considered Fatal in this register, allowing errors to be treated differently for different appli‐ cations. For example, a Poisoned TLP will be a Non‐Fatal condition by default, and is treated as an Advisory Non‐Fatal error in some cases, as discussed ear‐ lier. But software can escalate it to Fatal by setting its severity bit to one and then it will no longer be an advisory case. The default severity values are illus‐ trated in the individual bit fields of Figure 15‐26 on page 694 (1 = Fatal, 0 = Non‐ Fatal). If they are enabled and not masked, those errors selected as Non‐Fatal will cause an ERR_NONFATAL message to be sent to the Root Complex, and those selected as Fatal will cause an ERR_FATAL message. 

**693** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐26: Advanced Uncorrectable Error Severity Register_ 

**==> picture [376 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdP 0 0 0 1 0 0 0 1 1 0 0 0 1 0 RsvdP 1 1 RsvdP x<br>TLP Prefix Blocked Error Severity<br>Atomic Op Egress Blocked Severity Undefined<br>MC Blocked TLP Severity<br> Uncorrectable Internal Error Severity Data Link<br>ACS Violation Severity Protocol Error<br>Unsupported Request Error Severity<br>Severity<br>ECRC Error Severity<br>Malformed TLP Severity Surprise Down<br>Receiver Overflow Severity Error Severity<br>Unexpected Completion Severity<br>Completer Abort Severity<br>Completion Timeout Severity<br>Flow Control Protocol Error Severity<br>Poisoned TLP Severity<br>Note: all bits designated RWS<br>**----- End of picture text -----**<br>


## **Uncorrectable Error Masking** 

Software can mask out individual errors so they won’t cause an error message to be sent by using the Advanced Uncorrectable Error Mask register, shown in Figure 15‐27 on page 694. The default condition is to allow Error Messages for each type of error (all mask bits are cleared). 

_Figure 15‐27: Advanced Uncorrectable Error Mask Register_ 

**==> picture [369 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdP RsvdP RsvdP<br>TLP Prefix Blocked Error Mask<br>Atomic Op Egress Blocked Mask Undefined<br>MC Blocked TLP Mask<br> Uncorrectable Internal Error Mask<br>ACS Violation Mask<br>Data Link<br>Unsupported Request Error Mask Protocol<br>ECRC Error Mask Error Mask<br>Malformed TLP Mask<br>Surprise Down<br>Receiver Overflow Mask Error Mask<br>Unexpected Completion Mask<br>Completer Abort Mask<br>Completion Timeout Mask<br>Flow Control Protocol Error Mask<br>Poisoned TLP Mask<br>Note: all bits designated RWS<br>**----- End of picture text -----**<br>


**694** 

**Chapter 15: Error Detection and Handling** 

## **Header Logging**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

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



**695** 

**PCI Ex ress Technolo p gy** 

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

**696** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐28: Root Error Status Register_ 

**==> picture [327 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 27 26 7 6 5 4 3 2 1 0<br>RsvdZ<br>Advanced Error Interrupt Message Number (RO)<br>Fatal Error Messages Received<br>Non-Fatal Error Messages Received<br>RW1CS First Uncorrectable Fatal<br>Multiple ERR_FATAL/NONFATAL Received<br>ERR_FATAL/NONFATAL Received<br>Multiple ERR_COR Received<br>ERR_COR Received<br>**----- End of picture text -----**<br>


Finally, an interrupt may have been enabled (in the Root Error Command regis‐ ter) to be sent to the host system as a result of detecting one of these events. To support that, the 5‐bit Interrupt Message Number in this register supplies the MSI or MSI‐X vector number to be used, and there are 32 possibilities. For MSI, the number is the offset from the base data pattern. For MSI‐X, it represents the table entry to be used, and must be one of the first 32 even if the agent supports more than 32. This read‐only value is set by hardware and must be automati‐ cally updated if the number of MSI messages assigned to the device changes. 

## **Advanced Source ID Register** 

Software error handlers may need to read and clear status registers in the device that detected and reported the error. To facilitate this, the error Messages contain the ID (Bus:Dev:Func) of the first device reporting that error type. The Source ID register captures that ID from the Message for an incoming ERR_FATAL/NONFATAL message if the ERR_FATAL/NONFATAL bit isn’t already set (meaning this is the first one). Similarly, the Source ID of the first received ERR_COR message is captured, too, as shown in Figure 15‐29 on page 698. 

**697** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐29: Advanced Source ID Register_ 

**==> picture [327 x 47] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 0<br>ERR_FATAL/NONFATAL Source ID ERR_COR Source ID<br>(ROS) (ROS)<br>ROS: Read-Only and Sticky<br>**----- End of picture text -----**<br>


## **Root Error Command Register** 

The Root Complex has separate enable bits for each of the three error categories to control whether that error type will generate an interrupt to call an error han‐ dler as shown in Figure 15‐30 on page 698. The interrupt that is generate will either be an MSI or MSI‐X as discussed in “Root Complex Error Status Regis‐ ters” on page 696. Once the interrupt is received, the called error handler would probably first read the Root Complex status registers to determine the nature of the error, and then go down to the source BDF of the error to read standard sta‐ tus register as well as possibly device‐specific registers to determine what occurred and how it should be handled. 

_Figure 15‐30: Advanced Root Error Command Register_ 

**==> picture [332 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 3 2 1 0<br>RsvdP<br>Fatal Error Reporting Enable<br>Non-Fatal Error Reporting Enable<br>Correctable Error Reporting Enable<br>Note: all bits designated RW<br>**----- End of picture text -----**<br>


## **Summary of Error Logging and Reporting** 

The spec includes the flow chart in Figure 15‐31 on page 699 that shows the actions taken by a Function when an error is detected. The part inside the dashed line highlights the items that are added when the optional AER capabil‐ ity structure is present. 

**698** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐31: Flow Chart of Error Handling Within a Function_ 

**==> picture [327 x 391] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Detected<br>Uncorrectable Error Type? Correctable<br>Determine severity using<br> Uncorrectable Error Severity Register<br>Advisory Yes AER Yes<br>Non-Fatal Error? Implemented?<br>No No<br>Set Fatal/NonFatal Error Detected bit Set Correctable Error Detected bit<br>in Device Status Reg Done in Device Status Reg<br>If UR, set Unsupported Request If UR, set Unsupported Request<br> Detected bit in Device Status Reg  Detected bit in Device Status Reg<br>Advanced Set corresponding bit in<br>Uncorrectable Error Status RegSet corresponding bit in Error Correctable Error Status Reg<br>Reporting<br>Only Is error masked in Yes<br>Correctable Error Mask<br>Masked in Yes  Register?<br>Uncorrectable Error Mask<br> Register? No Done<br>No Done 1) Set Uncorrectable Error status bit, andIf Advisory Non-Fatal Error:<br>header, and update prefix and header As appropriate, record prefix and reporting fields and registers 2) If not masked by Uncorrectable mask,header, and update prefix and header as appropriate, record prefix and reporting fields and registers<br>both SERR and UR ReportingUR Error anddisabled? Yes UR Reporting disabled?UR error and Yes<br>No Done No Done<br>Fatal Non-Fatal<br>Severity?<br>SERR enabled or No SERR enabled or No Correctable Reporting  No<br>Fatal Error Reporting Non-Fatal Error Reporting Enabled?<br>Enabled? Enabled?<br>Yes Done Yes Done Yes Done<br>Send ERR_FATAL Send ERR_NONFATAL Send ERR_COR<br>Done Done Done<br>**----- End of picture text -----**<br>


## **Example Flow of Software Error Investigation** 

Now that we know all the mechanisms defined in PCIe for detecting, logging and reporting errors, it is worthwhile to look at how software would find and use this information to determine how to handle a reported error. 

**699** 

## **PCI Ex ress Technolo p gy** 

This example is going to assume that both the originating Function as well as the Root Port upstream of it both support AER. Without AER support, the stan‐ dardized registers for error logging are very limited. 

The system used for this example is shown in Figure 15‐32 on page 701. The Root Port has a BDF of 0:28:0 and was enabled to generate an interrupt when it receives either an ERR_FATAL or ERR_NONFATAL message. We are going to follow the steps of error handling software would take to determine what errors have occurred, where they occurred and what packets were they detected in. 

The error handling software has been called because of an interrupt from Root Port 0:28:0. The steps below are just an example, but illustrate the process of error handling software gathering error information. 

1. Software knows it was Root Port 0:28:0 that called the error handler based on the interrupt vector used. Since MSI or MSI‐X interrupts are used to report errors, each Root Port will have their own unique set of interrupt vectors. 

2. The error handler reads the Root Error Status register of the AER structure on 0:28:0 to determine what types of error messages have been received by the Root Port. The value in that register is 0800_007Ch which indicates that this Root Port has not received any ERR_COR messages, but has received both ERR_FATAL and ERR_NONFATAL messages and the first uncorrect‐ able error message that it received was an ERR_FATAL. 

3. The next step is to determine which BDF beneath this Root Port sent the first uncorrectable error. Software then reads the Source ID register of the Root Port and finds the value 0500_0000h, which indicates that the source BDF of the first uncorrectable error was 5:0:0. 

4. Now software knows that the first uncorrectable error received by Root Port 0:28:0 was a Fatal error that originated from BDF 5:0:0. With this informa‐ tion, software then goes and reads the Uncorrectable Error Status register on BDF 5:0:0 to see which specific uncorrectable errors have occurred on that BDF. The value returned from that read is 0004_1000h which means that this BDF has detected at least one Malformed TLP and at least one Poi‐ soned TLP. But what the error handler really cares about is which one occurred first, because that’s the one that should be handled first. 

5. To determine which of the multiple uncorrectable errors occurred first, soft‐ ware then reads the Advanced Error Capability and Control register of 5:0:0 and finds the value 0000_0012h which has a First Error Pointer value of 12h meaning that the first uncorrectable error was a Malformed TLP (bit 18d) and not the Poisoned TLP (bit 12d). 

**700** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐32: Error Investigation Example System_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
