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
