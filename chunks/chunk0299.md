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
