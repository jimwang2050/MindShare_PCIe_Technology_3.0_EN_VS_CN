   - a) Upstream Port registered preset values from the 8 consecutive TS2s it saw prior to changing to 8.0 GT/s. It must use the Transmitter presets and it may optionally use the Receiver presets it received. 

**574** 

**Chapter 14: Link Initialization & Training** 

   - b) Downstream Port must use the Transmitter presets defined in its Lane Equalization Control register as soon as it changes to 8.0 GT/s and it may optionally use the Receiver presets found there. 

- Else (the variable is not set), Transmitters must use the coefficient settings they agreed to when the equalization process was last executed. 

   - a) Upstream Port’s next state will be Recovery.Equalization if 8 consecu‐ tive incoming TS1s have Link and Lane numbers that match those being sent and the speed_change bit is 0b, but the EC bits are non‐ zero, indicating that the Downstream Port wishes to redo some parts of the equalization process. The spec notes that a Downstream Port could do this under software or implementation‐specific direction. As always, the time it takes to do this must not be allowed to cause transaction timeout errors, which really means the Downstream Port would need to ensure there were no transactions in flight before tak‐ ing this step. 

   - a) Downstream Port’s next state will be Recovery.Equalization if directed, as long as this state wasn’t entered from Configuration.Idle or Recovery.Idle. The spec points out that no more than two TS1s whose EC=00b should be sent before sending TS1s with a non‐zero EC value to request that equalization be redone. 

Otherwise, after a 24ms timeout: 

## _Exit to “Recovery.RcvrCfg”_ 

The next state will be Recovery.RcvrCfg if both: 

- 8 consecutive TS1s or TS2s are received whose Link and Lane num‐ bers match what it being sent and their speed_change bit is equal to 1b. 

- And either the current data rate is already higher than 2.5 GT/s, or at least a higher rate is shown to be supported in the TS1s or TS2s. 

## _Exit to “Recovery.Speed”_ 

The next state will be Recovery.Speed if other of the two following condi‐ tions are met: 

- If the current speed is set higher than 2.5 GT/s but isn’t working since entering Recovery (indicated by clearing the variable changed_speed_recovery to 0b). The new rate after leaving Recov‐ ery.Speed will drop back to 2.5 GT/s. 

- If the changed_speed_recovery variable is set to 1b, indicating that a higher rate than 2.5 GT/s is already working but the Link was unable to operate at a new negotiated rate. As a result, the operating speed will revert to what it was when Recovery was entered from L0 or L1. 

**575** 

**PCI Ex ress Technolo p gy** 

## _Exit to “Configuration State”_ 

Otherwise, the LTSSM will return to Configuration if a speed change is not requested (directed_speed_change variable = 0b and the speed_change bit in the TS1s and TS2s is 0b), or if the highest commonly supported data rate is 2.5 GT/s. 

## _Exit to “Detect State”_ 

Finally, if none of the other conditions are true, the next state will be Detect. 

## **Speed Change Example** 

The spec includes an example of a speed change in the discussion of this sub‐ state. The scenario is two Link neighbors (device A and device B) that are com‐ ing out of reset, both of which support the 5.0 GT/s and 8.0 GT/s rates. 

To begin with, the Link will automatically train to L0 using the Gen1 rate of 2.5 GT/s. (This behavior is likely to continue in future spec versions because it pro‐ vides backward compatibility with older designs.) 

In our example both devices support higher rates and this is indicated by the Rate Identifier field in their TS Ordered Sets during training. Both devices note that the other supports a higher rate and one of them (device A) will be the first to set its directed_speed_change variable to 1b. When that happens, it will go to Recovery.RcvrLock and send TS1s with the speed_change bit set. If the desired rate will be 8.0 GT/s and hasn’t been before, the devices will exchange EQ TS1s to deliver the TX equalizer presets to be used instead of sending ordinary TS1s. 

Device B sees incoming TS1s and also transitions to Recovery.RcvrLock. When it recognizes 8 TS1s in a row with the speed_change bit set, it responds by set‐ ting the speed_change bit in its own TS1s and goes to Recovery.Speed. Device A waits for that response and, when 8 TS1s in a row with the speed_change bit have been seen, it goes to Recovery.RcvrCfg and then to Recovery.Speed. In that substate, the transmitters are put into Electrical Idle, the speed is changed to the highest commonly‐supported rate, and the directed_speed_change variable is cleared. 

After a timeout period, both devices transition back to Recovery.RcvrLock and the transmitters are re‐activated using the new speed (8.0 GT/s in this case). They send TS1s again now, this time with the speed_change bit cleared to 0b. If the new speed works well, they transition to Recovery.RcvrCfg and back to L0. However, if device B has a problem, such as failure to achieve Bit Lock, it will timeout in this substate and go back to Recovery.Speed. Device A may have 

**576** 

**Chapter 14: Link Initialization & Training** 

already transitioned to Recovery.RcvrCfg by this time, but when it sees Electri‐ cal Idle now, indicating the neighbor has returned to Recovery.Speed, it will also go back to that state. Returning to Recovery.Speed causes both devices to revert to the speed in use when Recovery was entered, 2.5 GT/s in this case, and return to Recovery.RcvrLock. 

In response to that development, Device A might set directed_speed_change again and try the process a second time. If it failed again, device A might choose to remove the 8.0 GT/s rate from its advertised list and try the speed change again without it. Since the highest common rate is now 5.0 GT/s, if this attempt succeeds the rate will end up at 5.0 GT/s. If it doesn’t work, Device A might give up trying to use a higher rate. How and when a device chooses to change its advertised rates or give up trying to get a higher rate working is not given in the spec and will be implementation specific. 

## **Link Equalization Overview** 

This section provides an overview of the Equalization Process and prepares the reader to understand the detailed substate machine behaviors if they are of interest. 

Using a higher Link speed results in more signal distortion than lower data rates. To compensate for this and minimize the effort and cost for system designers, the 3.0 spec adds a requirement for Transmitter Equalization. Unlike the fixed de‐emphasis values for the lower rates, which is really a simple form of Transmitter equalization itself, the new method uses an active handshake process to match the Transmitters to the actual signaling environment. During this process, each Receiver Lane evaluates the quality of the incoming signal and suggests Tx equalization parameters that the Link partner should use to meet the signal quality requirements. 

The Link Equalization procedure executes after the first change to the 8.0 GT/s data rate. The spec strongly recommends that the equalization process be initi‐ ated autonomously (automatically in hardware) but doesn’t require it. If a com‐ ponent chooses not to use the autonomous mechanism then a software‐based mechanism must be used. If either port is unable to achieve the necessary signal quality through this process, the LTSSM will conclude that the rate is not work‐ ing and will go back to Recovery.Speed to request a lower speed. 

The process involves up to four phases, as described in the text that follows. Once the speed has been changed to 8.0 GT/s, the current equalization phase in use is indicated by the EC (Equalization Control) field in the TS1s being, as shown in Figure 14‐28. 

**577** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐28: EC Field in TS1s and TS2s for 8.0 GT/s_ 

**==> picture [293 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>7 6 5 4 3 2 1 0<br>0<br>Tx Preset EC<br>1 Link #<br>2 Lane # Use Preset Reset EIEOS<br>Interval Count<br>3 # FTS<br>Symbol 7<br>4 Rate ID<br>7 6 5 4 3 2 1 0<br>5 Train Ctl FS value when EC = 01b,<br>Rsvd<br>6 Otherwise Pre-Cursor Coefficient<br>EQ Info<br>Symbol 8<br>9<br>7 6 5 4 3 2 1 0<br>10<br>LF value when EC = 01b,<br>Rsvd<br>TS ID Otherwise Cursor Coefficient<br>13 Symbol 9<br>7 6 5 4 3 2 1 0<br>14<br>TS ID<br>15 P [RCV] Post-Cursor Coefficient<br>**----- End of picture text -----**<br>


## **Phase 0** 

When the Downstream Port is ready to change from a lower rate to the 8.0 GT/s rate, it enters the Recovery.RcvrCfg sub‐state and sends Tx Presets and Rx Hints to the Upstream Port using EQ TS2s as described in “TS1 and TS2 Ordered Sets” on page 510. (Note that this phase is skipped if the Link is already running at 8.0 GT/s.) The Downstream Port (DSP) sends Tx Preset values based on the con‐ tents of its Equalization Control register shown in Figure 14‐29 on page 579. One thing this highlights is that there can be different equalization values for each Lane. The Downstream Port will use the DSP values for its own Transmit‐ ter and optionally for its Receiver, and send the USP values to the Upstream Port for it to use when going to the higher speed. 

**578** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐29: Equalization Control Registers_ 

**==> picture [275 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 Link Control 3 Register 2  1  0<br>RsvdP<br>31 Lane Error Status Register 0<br>Equalization Control Registers<br>31 16  15 0<br>Lane (1) Control Lane (0) Control<br>Lane (3) Control Lane (2) Control<br>Lane (n) Control Lane (n-1) Control<br>Control Register Contents<br>15  14 12  11 8  7  6 4  3 0<br>USP USP DSP DSP<br>R R<br>Rx Hint Tx Preset Rx Hint Tx Preset<br>USP = UpStream Port   DSP = DownStream Port<br>**----- End of picture text -----**<br>


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



Once the rate does change, the Downstream Port begins in Phase 1 and sends TS1s with EC = 01b. It then waits for the Upstream Port to respond with the same EC value. 

Meanwhile, the Upstream Port starts in Phase 0, as illustrated in Figure 14‐30 on page 581, and sends TS1s that echo the preset values it received earlier from the 

**580** 

**Chapter 14: Link Initialization & Training** 

EQ TS1s and EQ TS2s. It will use those requested Tx presets if they’re sup‐ ported, and will optionally use the Rx Hints. The USP is allowed to wait 500ns before evaluating the incoming signal but, once it’s able to recognize two TS1s in a row it’s ready for the next step. This means the signal quality meets the min‐ imum BER of 10[‐4] (e.g., Bit Error Ratio of less than one error in 10,000 bits). Sub‐ sequently the USP sets EC=01b in its TS1s thereby moving to Phase 1 and handing control of the next step to the DSP. 

_Figure 14‐30: Equalization Process: Starting Point_ 

**==> picture [250 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>Downstream<br>Port<br>EC = 01b EC = 00b<br>Upstream<br>Port<br>Endpoint<br>**----- End of picture text -----**<br>


**Phase 1** 
