The second condition is when both partners support 8.0 GT/s and one of them wants to perform Tx Equalization. In both conditions the directed_speed_change variable will be set to 1b and the changed_speed_recovery bit will be cleared to 0b. 

A Port will not attempt a speed change (the directed_speed_change variable won’t be set) if a rate higher than 2.5 GT/s has never been seen as advertised by the other Port in the Configuration.Complete or Recovery.RcvrCfg substates. 

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

## **Link Width Change** 

An upper layer would normally only direct a Link width reduction if upconfigure_capable has been set to 1b because otherwise the Link won’t be able to go back to the original width. If the Hardware Autonomous Width Dis‐ able bit is set to 1b a Port can only reduce the width in an effort to correct a reli‐ ability problem. An upper layer can only initiate an increase in Link width if the Link partner advertised that it was upconfigure capable and the Link is not already at its maximum width. Apart from these guidelines, the decision crite‐ ria for changing the Link width are not given in the spec and are therefore implementation specific. 

## **Link Partner Initiated** 

The spec describes three possibilities for this case. 

First, if Electrical Idle is detected or inferred (see Table 14‐10 on page 596) on all Lanes without first receiving an EIOS on any Lane, the Port may choose to enter Recovery or stay in L0. If errors result from this condition, the Port may be directed to Recovery by means such as setting the Retrain Link bit. 

The second case happens when TS1s or TS2s are received (or an EIEOS for 128b/ 130b) on any configured Lanes, indicating that the Link partner has already entered Recovery. Since both of these cases are initiated by the Link partner, the Transmitter is allowed to complete any TLP or DLLP currently in progress. 

Finally, if an EIOS is received on any Lane, indicating a Link power manage‐ ment change, but the Receiver doesn’t support L0s and hasn’t been directed to L1 or L2, then going to Recovery is the only option. 

## _Exit to “L0s State”_ 

The next state will be L0s for a Transmitter that’s been instructed to initiate it, or for a Receiver that sees an EIOS. Interestingly, the LTSSM states for the Transmitter and Receiver of the Port can be different now, because one can be in L0s while the other is still in L0. 

- Transmitters go to L0s when directed, if they implement L0s, and send EIOS to initiate the change. 

- Receivers go to L0s when an EIOS is seen on any Lane. However, if the Receiver doesn’t implement L0s and hasn’t been directed to L1 or L2, this will be seen as a problem and the next state will be “Recovery State” instead. 

**570** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Rx_L0s.Entry”_ 

- The next state will be L1 when one Link partner is directed to initiate this and sends one EIOS on all Lanes (two EIOSs if the speed is 5.0 GT/s) and receives an EIOS on any Lane. Note that both Link partners must have already agreed to enter L1 beforehand and that a Data Link Layer hand‐ shake is needed to ensure that both are ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. 

## _Exit to “L2 State”_ 

The next state will be L2 when one Link partner is directed to initiate this and sends one EIOS on all Lanes (two EIOSs if the speed is 5.0 GT/s) and receives an EIOS on any Lane. Note that both Link partners must have already agreed to enter L2 beforehand and that a handshake is needed to ensure that both are ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. 

## **Recovery State** 

If everything works as expected, the Link trains to the L0 state without ever going into the Recovery state. But we’ve already discussed two reasons why it might not. First, if the correct Symbol pattern isn’t seen in Configuration.Idle, the LTSSM goes to Recovery in an effort to correct signaling problems by, for example, adjusting equalization values. Secondly, once L0 is reached with a data rate of 2.5 GT/s and both devices support higher speeds, the LTSSM goes to Recovery and attempts to change the Link speed to the highest commonly‐sup‐ ported/advertised speed. In this state, Bit Lock and either Symbol Lock or Block Alignment is re‐acquired and the Link is de‐skewed again. The Link and Lane Numbers should remain unchanged unless the Link width is being changed. In that case, the LTSSM passes through the Configuration state where Link width is re‐negotiated. 

NOTE: To simplify the discussion and avoid repeating the same text many times, the term “Lock” will be used here to mean the combination of Bit Lock and either Symbol Lock for 8b/10b encoding or Block Alignment for 128b/130b encoding. A Receiver must acquire this Lock to be able to recognize Symbols, Ordered Sets and Packets. 

**571** 

**PCI Ex ress Technolo p gy** 

## **Reasons for Entering Recovery State** 

- Exiting the L1 state; Required because there is no fast training option (like sending FTS ordered sets) when exiting L1 

- Exiting L0s if the receiver fails to achieve Lock from the FTS ordered sets in the required time, the Link must transition to Recovery 

- From L0 if: 

- A higher data rate is available when initial training completes. 

- A Link speed or width change has been requested (for power management or because the current speed or width is unreliable). 

- Software sets the Retrain Link bit in the Link Control Register (see Figure 14‐71 on page 644) in an effort to clear transmission problems. 

- An error condition such as a Replay Num Roll‐over event associated with the Ack/Nak protocol of the Data Link Layer automatically causes the Physical Layer logic to retrain the Link. 

- Receiver sees TS1s or TS2s on any configured Lane, meaning that the neighbor must have entered Recovery. 

- Receiver sees Electrical Idle on all configured Lanes but did not first receive the Electrical Idle Ordered Set. 

## **Initiating the Recovery Process** 

Either Port can initiate Recovery by sending TS1s to its neighbor. When a Port sees incoming TS1s it knows that the other Port has entered Recovery, so it also goes into Recovery and returns TS1s. Both receivers first use the TS1s to reac‐ quire Lock (if necessary) and then proceed to the other substates as needed. This is shown in Figure 14‐27 on page 573. A detailed description of what hap‐ pens in the substates is provided in the sections that follow. 

**572** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐27: Recovery State Machine_ 

**==> picture [343 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from Recovery.Speed Exit to Exit to<br>L1, L0, L0s Loopback Configuration<br>Recovery.Equalization<br>Recovery.RcvrLock Recovery.Idle Exit to<br>(bit/sym bol re-lock) Recovery.RcvrCfg (Send idle data) Disabled<br>Exit to Hot<br>Exit to Exit to Reset<br>Configuration Detect<br>Exit to L0<br>**----- End of picture text -----**<br>


## **Detailed Recovery Substates** 

## _During Recovery.RcvrLock_ 

- Regardless of the speed, Transmitters send TS1s on all configured Lanes using the same Link and Lane numbers that were set in the Configuration state. If the purpose of entering the Recovery state was to change speeds, the speed_change bit in the Data Rate Identifier Symbol will be set to 1b in the TS1s from the initiating device and the internal variable directed_speed_change is set to 1b. This same variable will be set in the other device if the speed_change bit is set in the incoming TS1s. In addition, The successful_speed_negotiation variable is cleared to 0b on entry to this substate. 

In this substate, an Upstream Port is allowed to specify the de‐emphasis level the Downstream Port should use when operating at 5GT/s. This is accomplished by setting the Selectable De‐emphasis bit in its TS1s to the desired value. It’s possible that bit errors on the Link will prevent this infor‐ mation from reaching the Downstream Port, so the Upstream Port is allowed to request the de‐emphasis level again when going to the Recovery state for a speed change. If the Downstream Port plans to use the requested level, it must record the value of the Selectable De‐emphasis bit while in this state. 

**573** 

**PCI Ex ress Technolo p gy** 

A new transmitter voltage can also be applied upon entry to this state. The Transmit Margin field in the Link Control 2 register is sampled on entry to this substate and remains in effect until a new value is sampled on another entry to this substate from L0, L0s, or L1. 

A Downstream Port that wants to change the rate to 8.0 GT/s and redo the equalization must send EQ TS1s with the speed_change bit set and adver‐ tising the 8.0 GT/s rate. If an Upstream Port receives 8 consecutive EQ TS1s or EQ TS2s with the speed_change bit set to 1b and the 8.0 GT/s rate sup‐ ported, it is expected to advertise the 8.0 GT/s rate, too, unless it has con‐ cluded that there are reliability problems at that rate that can’t be fixed with equalization. Note that a Port is allowed to change its advertised data rates when entering this state, but only those rates that can be supported reliably. And apart from the conditions described here, a device is not allowed to change its supported data rates in this substate or in Recovery.RcvrCfg or Recovery.Equalization. 

## _Exit to “Recovery.RcvrCfg”_ 

- The next state will be Recovery.RcvrCfg if 8 consecutive TS1s or TS2s are received whose Link and Lane numbers match what is being sent _and_ their speed_change bit is equal to the directed_speed_change variable _and_ their EC field is 00b (if the current data rate is 8.0 GT/s). 

- If the Extended Synch bit is set, a minimum of 1024 TS1s in a row must be sent before going to Recovery.RcvrCfg. 

- If this substate was entered from Recovery.Equalization, the Upstream Port must compare the equalization coefficients or preset received by all Lanes against the final set of coefficients or preset that was accepted in Phase 2 of the equalization process. If they don’t match, it sets the Request Equalization bit in the TS2s it sends. 

## _Exit to “Recovery.Equalization”_ 

When the data rate is 8.0 GT/s, the Lanes must establish the proper equal‐ ization parameters to obtain good signal integrity. This section does not apply for lower speeds. Just because the Link is running at 8.0 GT/s, it does not go through the Recovery.Equalization substate every time Recovery is entered. Recovery.Equalization is only entered if one of these conditions is met: 

- If the start_equalization_w_preset variable is set to 1b then: 
