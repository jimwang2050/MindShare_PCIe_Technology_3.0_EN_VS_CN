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
