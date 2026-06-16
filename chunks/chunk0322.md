**Gen3 Mode Encoding.** For Gen3 mode, the EIOS is an Ordered Set block that consists of an Ordered Set Sync Header (01b) followed by 16 bytes that are all 66h, as shown in Figure 16‐10 on page 737. Curiously, a Transmitter is not required to finish the block if it will go directly to Electrical Idle but is allowed to stop after Symbol 13 (anywhere in Symbol 14 or 15). The reason is to allow for the case where an internal clock doesn’t line up with the Sym‐ bol boundaries due to 128b/130b encoding. This truncation won’t cause a problem at the Receiver because it only needs to see Symbols 0 ‐ 3 of the EIOS to recognize it. 

_Figure 16‐10: Gen3 Mode EIOS Pattern_ 

**==> picture [110 x 153] intentionally omitted <==**

**----- Start of picture text -----**<br>
EIOS<br>Sync Header 01<br>Byte 0 01100110<br>1 01100110<br>2 01100110<br>3 01100110<br>4 01100110<br>13 01100110<br>14 01100110<br>15 01100110<br>**----- End of picture text -----**<br>


**737** 

**PCI Ex ress Technolo p gy** 

## **Transmitter Exit from Electrical Idle** 

When a Transmitter is instructed to exit from Electrical Idle, the steps it takes depend on the data rate in use (see below). However, it must resume transmis‐ sion within less than 8ns by sending FTSs or TS1/TS2s causing transition back to the L0 full‐on state. 

**Gen1 Mode.** For 2.5 GT/s, the process is simple: it begins using valid dif‐ ferential signals to send the TS1s or FTSs that will serve to inform the Receiver about the change. The Receiver detects the voltage as being above the squelch threshold and begins to evaluate the incoming signal. 

**Gen2 Mode.** When using 5.0 GT/s, the signals are changing so quickly that they don’t have time to reach the higher voltage levels. That makes it more difficult to quickly detect when the voltages have changed back to the oper‐ ational values. To make this easier, the EIEOS (Electrical Idle Exit Ordered Set), was defined to provide a lower‐frequency sequence. The EIEOS for 8b/ 10b encoding, shown in Figure 16‐11 on page 739, uses repeated K28.7 con‐ trol characters to appear as a repeating string of 5 ones followed by 5 zeros. This gives the low‐frequency signal that allows the higher signal voltages that are more readily seen. In fact, the spec states that this pattern guaran‐ tees that the Receiver will properly detect an exit from Electrical Idle, some‐ thing that scrambled data cannot do. The EIEOS is to be sent under the following conditions: 

- Before the first TS1 after entering the Configuration.Linkwidth.Start or Recovery.RcvrLock state. 

- After every 32 TS1s or TS2s are sent in Configuration.Linkwidth.Start, Recovery.RcvrLock, or Recovery.RcvrCfg states. The TS1/TS2 count is reset to zero whenever an EIEOS is sent or the first TS2 is received in the Recovery.RcvrCfg state. 

**738** 

**Chapter 16: Power Management** 

_Figure 16‐11: Gen1/Gen2 Mode EIEOS Symbol Pattern_ 

**==> picture [100 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
EIEOS<br>Symbol 0 K28.5<br>1 K28.7<br>2 K28.7<br>3 K28.7<br>4 K28.7<br>13 K28.7<br>14 K28.7<br>15 D10.2<br>**----- End of picture text -----**<br>


**Gen3 Mode.** An EIEOS is needed for 8 GT/s rate too and for the same rea‐ son as for 5.0 GT/s. Now, though, the Ordered Set takes the form of a block, as shown in Figure 16‐12 on page 740. As before, it gives a low‐frequency pattern in alternating bytes of 00h and FFh, which appears as a repeating string of 8 zeros followed by 8 ones. 

In addition, EIEOS is sent so as to allow a receiver during LTSSM Recovery state to establish Block Lock after which the Link transitions to the L0 state. See the section “Block Alignment” on page 411 and “Achieving Block Align‐ ment” on page 438. 

In Gen3 mode, EIEOS is to be sent: 

- Before the first TS1 after entering the Configuration.Linkwidth.Start or Recovery.RcvrLock state. 

- Immediately after an EDS Framing Token when a Data Stream is end‐ ing if an EIOS is not being sent and the LTSSM is not entering Recov‐ ery.RcvrLock. 

- After every 32 TS1s/TS2s whenever TS1s or TS2s are sent. The count is reset to zero when: 

- 

   - an EIEOS is sent 

- the first TS2 is received while in either the Recovery.RcvrCfg or Config‐ uration.Complete LTSSM state 

- a Downstream Port in Phase 2 of the Equalization sequence, or an Upstream Port in Phase 3, receives two TS1s with the Reset EIEOS Inter‐ val Count bit set. 

**739** 

**PCI Ex ress Technolo p gy** 

- After every 2[16] TS1s during the Equalization sequence, if the Reset EIEOS Interval Count bit has prevented it from being sent. The spec states that designs are allowed to satisfy this requirement by sending and EIEOS within 2 TS1s of the scrambling LFSR matching its seed value. 

- As part of an FTS sequence, Compliance Pattern, or Modified Compliance pattern. 

_Figure 16‐12: 128b/130b EIEOS Block_ 

**==> picture [138 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
EIEOS<br>Sync Header 01<br>Byte 0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


## **Receiver Entry to Electrical Idle** 

When a Transmitter enters Electrical Idle, the Link partner’s Receiver responds based on the data rate, as described in the following sections. Receipt of an EIOS informs the Receiver that this is going to happen, preparing it to detect when it actually does happen. When the Receiver detects this condition it de‐gates the error logic to prevent reporting errors caused by unreliable activity on the Link and arms its Electrical Idle Exit detector so it will be ready to resume normal activity when the Transmitter begins to send data again. There are two Electri‐ cal Idle detection options.: 

**Detecting Electrical Idle Voltage.** Once an EIOS has been received, the expectation is that the Transmitter will cease transmission very quickly. In the 1.x spec versions Receivers detect this by observing that the incoming voltage has dropped below the threshold of a valid signal. This isn’t too dif‐ ficult at 2.5 GT/s but it requires a squelch detect circuit that consumes space and power. 

**740** 

**Chapter 16: Power Management** 

**Inferring Electrical Idle.** However, at higher frequencies the signal becomes increasingly attenuated, making it difficult for squelch detect logic to distinguish the levels. This is especially true for 8.0 GT/s, where it’s expected that the Receiver may need to perform equalization internally to recover a good signal. To alleviate these detection problems, the 2.0 spec introduced the concept of allowing a Receiver to infer when the Link has gone to the Electrical Idle condition rather than testing the voltage level. In this model, the absence of expected events is used to indicate that the Link is not signaling and can therefore be assumed to be in Electrical Idle, as listed in Table 16‐17. By way of explanation, Flow Control Updates should arrive regularly while the Link is in L0, and SOSs are expected with certain timing, too. For simplicity, a Receiver is allowed to check for one or the other or both of these conditions. During Link training the TS1s and TS2s should arrive regularly, so their absence can also be taken to mean that the Link is Idle. For the last two rows of the table, though, it’s possible that no Symbols have been received at all, and that will also be understood to mean the Link is Idle. Since Electrical Idle takes place for the overall Link and not for Lanes independently, there’s no need for each Lane to measure these times. Instead, an LTSSM can just use one timer in common for all the Lanes on that Link. 

_Table 16‐17: Electrical Idle Inference Conditions_ 

|State|2.5GT/s|5.0 GT/s|8.0 GT/s|
|---|---|---|---|
|L0|Absence of an FC Update or SOS in a 128s window|||
|Recovery.RcvrCfg|Absence of a TS1 or TS2 in a 1280 UI<br>interval||Absence of a TS1<br>or TS2 in a 4ms<br>window|
|Recovery.Speed<br>(successful_speed_<br>negotiation = 1b)|Absence of a TS1 or TS2 in a 1280 UI<br>interval||Absence of a TS1<br>or TS2 in a 4680<br>UI interval|
|Recovery.Speed<br>(successful_speed_<br>negotiation = 0b)|Absence of an exit<br>from Electrical Idle<br>in a 2000 UI interval|Absence of an exit from Electrical<br>Idle in a 16000 UI interval||
|Loopback.Active<br>(as a slave)|Absence of an exit<br>from Electrical Idle<br>in a 128s window|N/A|N/A|



**741** 

**PCI Ex ress Technolo p gy** 

How the EIOS is recognized at the Receiver also depends on the encoding scheme. For Gen1/Gen2 mode, a receiver recognizes an EIOS when it sees two of the three IDL Symbols. For Gen3 mode, it’s recognized when Symbols 0‐3 of the incoming block match the EIOS pattern. 

## **Receiver Exit from Electrical Idle** 

Receivers detect a voltage difference to signify a resumption of normal signal‐ ing. An exit from Electrical Idle will be detected when the differential peak‐to‐peak voltage exceeds the Electrical Idle Detect threshold, which is allowed to be set between 65 and 175mV for all data rates. 

At 2.5 GT/s nothing more is needed, but at higher rates Receivers don’t have to rely on this detection circuit except when receiving EIEOS during certain LTSSM states or during the four EIE Symbols that precede transmission of an FTS sequence at 5.0 GT/s. The number and timing of EIEOSs to facilitate detec‐ tion of Electrical Idle exit depends on the Link state. For more on this, see “Active State Power Management (ASPM)” on page 735. 

In Electrical Idle, the Receiver’s PLL looses clock synchronization. When the Transmitter exits Electrical Idle, it sends FTSs to exit from L0s, or TS1/TS2s to exit from all other Link states. Doing so supplies the needed transition density for the CDR logic to re‐synchronize the receiver PLL and achieve Bit Lock and Symbol Lock or Block Alignment. 

Figure 16‐13 illustrates the Link state transitions and highlights the transitions between L0, L0s, and L1. Note that there is no direct path from L0s to L1, so the Link must be returned to the L0 state before changing between them. 

_Figure 16‐13: ASPM Link State Transitions_ 

**==> picture [274 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
L0<br>L2/L3<br>L0s L1 Recovery LDn<br>Ready<br>L2 L3<br>**----- End of picture text -----**<br>


**742** 

**Chapter 16: Power Management** 

The Link Capability register specifies a device’s support for Active State Power Management. Figure 16‐14 illustrates the _ASPM Support_ field within this regis‐ ter. In earlier spec versions, not all 4 options were available, but the 2.1 spec filled in all of them. Note that bit 22 indicates whether all the options are avail‐ able. 

_Figure 16‐14: ASPM Support_ 

**==> picture [360 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Capabilities Register<br>31 24 23 22 21 20 19 18 17 1514 12 11 10 9 4 3 0<br>Port Number<br>ASPM Optionality<br>Compliance<br>0  0 No ASPM Support<br>0  1 L0s Supported<br>1  0 L1 Supported<br>1  1 L0s & L1 supported<br>Active State PM Support<br>**----- End of picture text -----**<br>


Software can enable and disable ASPM via the _Active State PM Control_ field of the Link Control Register as illustrated in Figure 16‐15 on page 744. The possi‐ ble settings are listed in Table 16‐18 on page 743. Note: The spec recommends that ASPM be disabled for all components in a path used for Isochronous trans‐ actions if the additional latencies associated with ASPM exceed the limits of the isochronous transactions. 

_Table 16‐18: Active State Power Management Control Field Definition_ 

|**Setting**|**Description**|
|---|---|
|00b|L0s and L1 ASPM disabled|
|01b|L0s enabled and L1 disabled|



**743** 

**PCI Ex ress Technolo p gy** 

_Table 16‐18: Active State Power Management Control Field Definition (Continued)_ 

|**Setting**|**Description**|
|---|---|
|10b|L1 enabled and L0s disabled|