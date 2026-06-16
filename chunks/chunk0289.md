- If no Lanes detect a Receiver, go back to Detect.Quiet. The loop between them is repeated every 12ms, as long as no Receiver is detected. 

## _Exit to “Polling State”_ 

- If a receiver is detected on all Lanes, the next state will be Polling. The Lanes must now drive a DC common voltage within the 0 ‐ 3.6 V VTX‐CM‐DC spec. 

## _Special Case:_ 

If some but not all Lanes of a device are connected to a Receiver (like a x4 

**524** 

**Chapter 14: Link Initialization & Training** 

device connected to a x2 device), then wait 12 ms and try it again. If the same Lanes detect a Receiver the second time, exit to the Polling state, oth‐ erwise go back to Detect.Quiet. If going to Polling, there are two possibili‐ ties for the Lanes that didn’t see a Receiver: 

1. If the Lanes can operate as a separate Link (see “Designing Devices with Links that can be Merged” on page 541), use another LTSSM and have those Lanes repeat the detect sequence. 

2. If another LTSSM is not available, then the Lanes that don’t detect a Receiver will not be part of a Link and must transition to Electrical Idle. 

## **Polling State** 

## **Introduction** 

To this point the link has been in the electrical idle state, however during Polling the LTSSM TS1s and TS2s are exchanged between the two connected devices. The primary purpose of this state is for the two devices to understand what the each other is saying. In other words, they need to establish bit and symbol lock on each other’s transmitted bit stream and resolve any polarity inversion issues. Once this has been accomplished, each device is successfully receiving the TS1 and TS2 ordered‐sets from their link partner. Figure 14‐9 on page 525 shows the substates of the Polling state machine. 

_Figure 14‐9: Polling State Machine_ 

**==> picture [339 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Detect<br>Entry from<br>Detect<br>24 ms<br>48 ms<br>Exchange<br>1024 TS1s<br>(unless directed Polling.Active Polling.Configuration<br>to Compliance) Bit/Symbol Lock (Polarity Inversion)<br>Directed or<br>Insufficient Lanes Electrical 8 TS1, TS2 (or complement) Rx on ALL 8 TS2 Rx. 16 TS2 Tx.<br>Lanes or 24 ms timeout and ANY<br>detect Idle Exit<br>exit from Electrical Idle Lane Rx 8 TS1, TS2 and ALL Lanes<br>detect exit from Electrical Idle<br>Exit to<br>Polling.Compliance Configuration<br>**----- End of picture text -----**<br>


**525** 

**PCI Ex ress Technolo p gy** 

## **Detailed Polling Substates** 

## **Polling.Active** 

## _During Polling.Active_ 

Transmitters send a minimum of 1024 consecutive TS1s on all detected Lanes once their common‐mode voltage has settled at the level specified in the Transmit Margin field. The two Link partners may exit the Detect state at different times, so the TS1 exchange is not synchronized. The time needed to send 1024 TS1s at Gen1 speed (2.5 GT/s) is 64μs. 

Some notes regarding this substate are: 

- The PAD Symbol must be used in the Lane and Link Number fields of the TS1s. 

- All data rates a device supports must be advertised, even if it doesn’t intend to use them all. 

- Receivers use the incoming TS1s to acquire Bit Lock (see “Achieving Bit Lock” on page 395) and then either Symbol Lock (see “Achieving Symbol Lock” on page 396) for the lower rates, or Block Alignment for 8.0 GT/s (see “Achieving Block Alignment” on page 438). 

## _Exit to “Polling.Configuration”_ 

- The next state is Polling.Configuration if, after sending at least 1024 TS1s **ALL** detected Lanes receive 8 consecutive training sequences (or their com‐ plement, due to polarity inversion) that satisfy one of the following condi‐ tions: 

- TS1s with Link and Lane set to PAD were received with the Compli‐ ance Receive bit cleared to 0b (bit 4 of Symbol 5). 

- TS1s with Link and Lane set to PAD were received with the Loopback bit of Symbol 5 set to 1b. 

- 

- TS2s were received with Link and Lane set to PAD. 

If the conditions above are not met, then after a 24ms timeout, if at least 1024 TS1s were sent after receiving a TS1, and **ANY** detected Lane received eight consecutive TS1 or TS2 Ordered Sets (or their complement) with the Lane and Link numbers set to PAD, and one of the following is true: 

- TS1s with Link and Lane set to PAD were received with the Compli‐ ance Receive (bit 4 of Symbol 5) cleared to 0b. 

- TS1s with Link and Lane set to PAD were received with the Loopback (bit 2 of Symbol 5) set to 1b. 

- TS2s were received with Link and Lane set to PAD. 

**526** 

**Chapter 14: Link Initialization & Training** 

If still none of the conditions above are met, if at least a predetermined number of detected Lanes also detected an exit from Electrical Idle at least once since entering Polling.Active (this prevents one or more bad Transmit‐ ters or Receivers from holding up Link configuration). The exact set of pre‐ determined Lanes is implementation specific now, which is a change from the 1.1 spec that needed to see an Electrical Idle exit on all detected Lanes. 

## _Exit to “Polling.Compliance”_ 

If the Enter Compliance bit in the Link Control 2 register is set to 1b, or if this bit was set before entering Polling.Active, the change to Polling.Com‐ pliance must be immediate and no TS1s are sent in Polling.Active. 

Otherwise, after a 24ms timeout, if: 

- All Lanes from the predetermined set have not seen an exit from Elec‐ trical Idle since entering Polling.Active (indicates a passive test load such as a resistor on at least one Lane forces all Lanes into Poll‐ ing.Compliance). 

- Any detected Lane received 8 consecutive TS1s (or their complement) with Link and Lane numbers set to PAD, the Compliance Receive bit of Symbol 5 set to 1b and the Loopback bit cleared to 0b. 

## _Exit to “Detect State”_ 

- If, after 24ms, the conditions for going to Polling.Configuration or Poll‐ ing.Compliane are not met, return to the Detect state. 

## **Polling.Configuration** 

In this substate, a transmitter will stop sending TS1s and start sending TS2s, still with PAD set for the Link and Lane numbers. The purpose of the change to sending TS2s instead of TS1s is to advertise to the link partner that this device is ready to proceed to the next state in the state machine. It is a handshake mecha‐ nism to ensure that both devices on the link proceed through the LTSSM together. Neither device can proceed to the next state until both devices are ready. The way they advertise they are ready is by sending TS2 ordered‐sets. So once a device is both sending AND receiving TS2s, it knows it can proceed to the next state because it is ready and its link partner is ready too. 

## _During Polling.Configuration_ 

- Transmitters send TS2s with Link and Lane numbers set to PAD on all detected Lanes, and they must advertise all the data rates they support, even those they don’t intend to use. Also, each Lane’s receiver must inde‐ pendently invert the polarity of its differential input pair if necessary. For an explanation of how this is done, see “Overview” on page 506. The Trans‐ mit Margin field must be reset to 000b. 

**527** 

## **PCI Ex ress Technolo p gy** 

## _Exit to “Configuration State”_ 

After eight consecutive TS2s with Link and Lane set to PAD are received on any detected Lanes, and at least 16 TS2s have been sent since receiving one TS2, exit to Configuration. 

## _Exit to “Detect State”_ 

Otherwise, exit to Detect after a 48ms timeout. 

## _Exit to Polling.Speed (Non‐existent substate)_ 

As a historical aside, the substates of Polling have changed since the 1.0 version of the spec was released. At that time it was thought that when other speeds became available it would make sense to change to the highest available rate as soon as possible in this state. However, the advent of higher rates coincided with the realization that it would be advantageous to be able to change speeds both higher and lower during runtime for power management reasons. Going through the Polling state involves clearing a number of Link values and that makes it an unattractive path for runtime use, so the rate change stage was moved out of this state into the Recovery state. See Figure 14‐10 on page 528. 

_Figure 14‐10: Polling State Machine with Legacy Speed Change_ 

**==> picture [355 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Detect<br>Entry from<br>Detect<br>24 ms<br>Speed change step was<br>48 ms moved from this state to<br>Exchange Recovery state<br>1024 TS1s Polling.Speed<br>(unless directed Polling.Active Polling.Configuration (E lect ri c a l Idle ,<br>to Compliance) Bit/Symbol Lock (Polarity Inversion) Ch a ng e Spee d)<br>Directed or<br>Insufficient Lanes Electrical 8 TS1, TS2 (or complement) Rx on ALLLanes or 24 ms timeout and ANY 8 TS2 Rx. 16 TS2 Tx.<br>detect Idle Exit<br>exit from Electrical Idle Lane Rx 8 TS1, TS2 and ALL Lanes<br>detect exit from Electrical Idle<br>Exit to<br>Polling.Compliance Configuration<br>**----- End of picture text -----**<br>


Today, the Link always trains to 2.5 GT/s after a reset, even if other speeds are available. If higher speeds are available once the LTSSM has reached L0, then it transitions to Recovery and attempts to change to the highest commonly‐sup‐ ported or advertised rate. Supported speeds are reported in the exchanged TS1s 

**528** 

**Chapter 14: Link Initialization & Training** 

and TS2s, so that either device can subsequently decide to initiate a speed change by transitioning to the Recovery state. The spec still lists this substate but declares that it is now unreachable. 

## **Polling.Compliance** 

This substate is only used for testing and causes a Transmitter to send specific patterns intended to create near‐worst‐case Inter‐Symbol Interference (ISI) and cross‐talk conditions to facilitate analysis of the Link. Two different patterns can be sent while in this substate, the Compliance Pattern and the Modified Compli‐ ance Pattern. 

**Compliance Pattern for 8b/10b.** This pattern consists of 4 Symbols that are repeated sequentially: K28.5‐, D21.5+, K28.5+ and D10.2‐, where (‐) means negative current running disparity or CRD and (+) means positive CRD (since the CRD is forced, it’s permissible to have a disparity error at the beginning of the pattern). If the Link has multiple Lanes, then four Delay Symbols (shown as D, but are really just additional K28.5 symbols) are injected on Lane 0, two before the next compliance pattern and two after the compliance pattern. Once the last Delay symbol has been sent on Lane 0, the four delay symbols are also sent on Lane 1 (again, two before the next compliance pattern and two after). This process continues until after the Delay symbols have propagated through Lane 7. Then they go back to start‐ ing on Lane 0 again as can be seen in Table 14‐3 on page 529 (the compli‐ ance pattern is shaded in grey). Every group of eight lanes behaves this way. Shifting the Delay Symbols will ensure interference between adjacent Lanes and provide better test conditions. 

_Table 14‐3: Symbol Sequence 8b/10b Compliance Pattern_ 

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|



**529** 

## **PCI Ex ress Technolo p gy** 

_Table 14‐3: Symbol Sequence 8b/10b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|6|D|K28.5+|K28.5+||D|
|7|D|D10.2|D10.2||D|
|8|K28.5‐|D|K28.5‐||K28.5‐|
|9|K21.5|D|K21.5||K21.5|
|10|K28.5+|K28.5‐|K28.5+||K28.5+|
|...|...|...|...||...|
|16|K28.5‐|K28.5‐|D||K28.5‐|
|17|K21.5|K21.5|D||K21.5|
|18|K28.5+|K28.5+|K28.5‐||K28.5+|



**Compliance Pattern for 128b/130b.** This pattern consists of the follow‐ ing repeating sequence of 36 Blocks: 
