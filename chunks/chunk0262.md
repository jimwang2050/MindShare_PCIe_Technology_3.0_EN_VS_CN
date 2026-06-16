**Out of Sequence TLP.** If the Sequence Number of the incoming packet is later (logically larger) than the expected value, the only explana‐ tion is that a TLP must have been lost. This is a correctable error and is han‐ dled by sending a Nak. It doesn’t matter if the incoming packet is good because they can only be accepted in correct Sequence Number order. The packet is discarded and the receiver waits for a TLP with the expected Sequence Number. 

The NEXT_RCV_SEQ counter is not incremented when a TLP is received with a CRC error, or was nullified, or for which the Sequence Number check fails. 

A transmitter orders TLPs according to the PCI ordering rules to maintain cor‐ rect program flow and avoid potential deadlock and livelock conditions (see Chapter 8, entitled ʺTransaction Ordering,ʺ on page 285). The Receiver is required to preserve this order and applies these three rules: 

- When the receiver detects a bad TLP, it discards the TLP and all new TLPs that follow in the pipeline until the replayed TLPs are detected. 

- Duplicate TLPs are discarded. 

- TLPs received while waiting for a lost or corrupt TLP are discarded. 

## **Receiver Schedules An Ack DLLP** 

If the Data Link Layer of the receiver does not detect an error in an incoming TLP, it forwards the TLP to the Transaction Layer. The NEXT_RCV_SEQ counter is incremented and the receiver starts the AckNak_LATENCY_TIMER (assuming it was not already running). This is the equivalent of “scheduling an Ack.” The receiver is allowed to continue receiving good TLPs without sending an Ack until the AckNak_LATENCY_TIMER expires. When the timer expires it 

**342** 

**Cha ter 10: Ack/Nak Protocol p** 

sends just one Ack with the Sequence Number of the last good TLP, acknowl‐ edging good receipt of all received TLPs up to the Sequence Number in the cur‐ rent Ack. This technique improves Link efficiency by reducing Ack/Nak traffic. For review, recall that this technique works because the TLPs must always be successfully received in order. 

## **Receiver Schedules a Nak** 

As mentioned earlier in the discussion of the receiver logic (see “Receiver Ele‐ ments” on page 324), when the receiver detects an error on a TLP, it discards the bad packet and sets the NAK_SCHEDULED flag if it was clear, which will cause a Nak to be scheduled with the Sequence Number of NEXT_RCV_SEQ count ‐ 1. Since a Nak is now scheduled, the AckNak_LATENCY_TIMER is reset and halted. Scheduling a Nak can be thought of as being an “edge‐triggered” event instead of a level‐triggered event. It is seeing the rising edge of the NAK_SCHEDULED flag that causes a Nak to be scheduled. Another Nak can‐ not be sent until the next rising edge, which means the NAK_SCHEDULED flag must be cleared (falling edge) first. There are only two events that will clear the NAK_SCHEDULED flag. The first is successfully receiving the expected next TLP (TLP with a Sequence Number that matches the NEXT_RCV_SEQ count). The second is a reset of the link (not retraining, but reset). 

Although it’s important to get the Nak to the transmitter quickly (no other TLPs can be accepted until the failed one is seen without errors), other outgoing TLPs, DLLPs or Ordered Sets already be in progress or have a higher priority than the Nak which means the receiver would have to delay the transmission of the Nak until they’re done (see “Recommended Priority To Schedule Packets” on page 350). In the meantime, if other TLPs arrive at the receiver they are dis‐ carded and no additional Acks or Naks will be scheduled while the NAK_SCHEDULED flag is set. 

## **AckNak_LATENCY_TIMER** 

This timer defines how long a receiver can wait before it must send an Ack for a successfully received TLP (or sequence of TLPs). As stated before, this timer is running anytime a receiver successfully receives a TLP that it has not yet acknowledged. Once the timer expires, an Ack is scheduled for transmission with the Sequence Number of the last good TLP it received. Scheduling an Ack resets the AckNak_LATENCY_TIMER and it only starts counting again once the next TLP is successfully received. 

**343** 

**PCI Ex ress Technolo p gy** 

## **AckNak_LATENCY_TIMER Equation.** 

The timeout value for the AckNak_LATENCY_TIMER is defined by the spec and varies based on the Negotiated Link Width and Max Payload Size Enabled. The equation which defines the timeout is shown below: 

( Max_Payload_Size + TLPOverhead ) * AckFactor 

+ InternalDelay  + _Tx_L0s_Adjustment_ LinkWidth _this term removed_ ( _for Gen2 and later_ ) 

The value in the timer is given in symbol times, the time it takes to send one symbol across the Link: 4ns for Gen1, 2ns for Gen2, and 1ns for Gen3. 

The equation fields are: 

- **Max_Payload_Size** ‐ the value in the Device Control Register. In the case of multiple Functions with different Max_Payload_Size values, the spec recommends using the smallest one of them. 

- **TLPOverhead** ‐ the additional TLP fields beyond the data payload (sequence number, header, digest, LCRC and Start/End framing sym‐ bols). In the spec, the overhead value is treated as a constant of 28 sym‐ bols. 

- **AckFactor** (AF) ‐ is basically a fudge factor representing the number of max payload‐sized TLPs that can be received before an Ack must be sent. The AF value ranges from 1.0 to 3.0 and is intended to balance Link bandwidth efficiency and Replay Buffer size. The table in Figure 10‐11 on page 339 shows the Ack Factor values for various link widths and payload sizes. These Ack Factor values are chosen to allow imple‐ mentations to achieve good performance without requiring a large uneconomical buffer. 

- **LinkWidth** ‐ ranges from x1 (1‐bit wide) to x32 (32‐bits wide).‐ from 1 to 32 Lanes. 

- **InternalDelay** ‐ the internal delay of processing a TLP within the receiver and DLLPs (Acks) within the transmitter. This value is defined in the spec in symbol times, and depends on the Link speed: Gen1 = 19, Gen2 = 70, Gen3 = 115. 

- **Tx_L0s_Adjustment** : ‐ This is a value that was included in the 1.x PCIe specs but was dropped for 2.0 and later PCIe specs. It could be used to account for the time required by the receive circuits to exit from L0s to L0. Setting the Extended Sync bit of the Link Control register affects the exit time from L0s and must be taken into account in this adjustment. Interestingly, the spec writers chose to assume this to be zero when cre‐ ating their table of Replay Timer values. 

**344** 

**Cha ter 10: Ack/Nak Protocol p** 

**AckNak_LATENCY_TIMER Summary Table.** Figure 10‐2 on page 345 shows the Gen1 timer load values for all the possible values used in the AckNak_LATENCY_TIMER equation. Higher data rates change the equation and the resulting table (see “Timing Differences for Newer Spec Versions” on page 350). Like the Replay Timer table, this table is con‐ structed by assuming the L0s adjustment in the equation is zero and then referring to the resulting values as ‘unadjusted’. Note that the tolerance for all of the table values is ‐0% to +100%. 

_Table 10‐2: Gen1 Unadjusted Ack Transmission Latency_ 

|**Max_Payload**<br>**Size**|**X1**<br>**Link**|**X2**<br>**Link**|**X4**<br>**Link**|**X8**<br>**Link**|**X12**<br>**Link**|**x16**<br>**Link**|**X32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|**128 Bytes**|**237**<br>**(AF=1.4)**|**128**<br>**(AF=1.4)**|**73**<br>**(AF=1.4)**|**67**<br>**(AF=2.5)**|**58**<br>**(AF=3.0)**|**48**<br>**(AF=3.0)**|**33**<br>**(AF=3.0)**|
|**256 Bytes**|**416**<br>**(AF=1.4)**|**217**<br>**(AF=1.4)**|**118**<br>**(AF=1.4)**|**107**<br>**(AF=2.5)**|**90**<br>**(AF=3.0)**|**72**<br>**(AF=3.0)**|**45**<br>**(AF=3.0)**|
|**512 Bytes**|**559**<br>**(AF=1.0)**|**289**<br>**(AF=1.0)**|**154**<br>**(AF=1.0)**|**86**<br>**(AF=1.0)**|**109**<br>**(AF=2.0)**|**86**<br>**(AF=2.0)**|**52**<br>**(AF=2.0)**|
|**1024 Bytes**|**1071**<br>**(AF=1.0)**|**545**<br>**(AF=1.0)**|**282**<br>**(AF=1.0)**|**150**<br>**(AF=1.0)**|**194**<br>**(AF=2.0)**|**150**<br>**(AF=2.0)**|**84**<br>**(AF=2.0)**|
|**2048 Bytes**|**2095**<br>**(AF=1.0)**|**1057**<br>**(AF=1.0)**|**538**<br>**(AF=1.0)**|**278**<br>**(AF=1.0)**|**365**<br>**(AF=2.0)**|**278**<br>**(AF=2.0)**|**148**<br>**(AF=2.0)**|
|**4096 Bytes**|**4143**<br>**(AF=1.0)**|**2081**<br>**(AF=1.0)**|**1050**<br>**(AF=1.0)**|**534**<br>**(AF=1.0)**|**706**<br>**(AF=2.0)**|**534**<br>**(AF=2.0)**|**276**<br>**(AF=2.0)**|



## **More Examples** 

In the classroom setting examples often make it much easier to grasp the Ack/ Nak process and so some of them are presented here to illustrate special cases. 

## **Lost TLPs** 

Consider Figure 10‐13 on page 346, showing how a lost TLP is detected and handled. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B successfully receives TLP 4094 so it starts its AckNak_LATENCY_TIMER and increments its NEXT_RCV_SEQ count. After that, it also receives TLPs 4095 and 0. 

**345** 

## **PCI Ex ress Technolo p gy** 

3. After receiving TLP 0, the AckNak_LATENCY_TIMER expires which causes it to schedule an Ack with Sequence Number of 0. 

4. Seeing Ack 0, Device A purges TLPs 4094, 4095, and 0 from its replay buffer. 

5. TLP 1 is lost en route for some reason (maybe the Physical Layer dropped it), and TLP 2 arrives instead. The Sequence Number check shows Device B that TLP 2’s Sequence Number is not equal to the NEXT_RCV_SEQ count but is in the out of sequence range. 

6. Device B discards TLP 2 and sets the NAK_SCHEDULED flag which will send a Nak 0 (NEXT_RCV_SEQ count ‐ 1) in this case. 

7. Upon receipt of Nak 0, Device A replays TLPs 1 and 2. It would purge TLP 0 and any earlier ones in the Replay Buffer, but they were removed earlier so that becomes unnecessary. 

8. TLPs 1 and 2 arrive without error at Device B and are forwarded to the Transaction Layer. 

_Figure 10‐13: Handling Lost TLPs_ 

**==> picture [382 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>1<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 2 Out of sequence<br>Later TLP 2<br>1 Ack<br>Purge Lat Tmr<br>0 0<br>4095<br>Earlier TLP 4094 Ack/Nak<br>0 Nak Generator<br>Link<br>Replayed TLPs<br>2 1<br>**----- End of picture text -----**<br>


**346** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Bad Ack** 

Figure 10‐14 on page 347 which shows the protocol for handling a corrupt Ack. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B receives TLPs 4094, 4095, and 0, sets NEXT_RCV_SEQ to 1, and returns Ack 0 because the AckNak_LATENCY_TIMER had expired. 

3. Ack 0 has a bit during its flight on the Link, so when Device A checks its 16‐ bit CRC, it fails the check and is discarded. This means TLPs 4094, 4095, and 0 remain in Device A’s Replay Buffer. 

4. TLPs 1 and 2 arrive at Device B and are good, so NEXT_RCV_SEQ count increments to 3 and Ack 2 is returned once the AckNak_LATENCY_TIMER expires again. 

5. Ack 2 arrives safely at Device A, which purges its Replay Buffer of TLPs 4094, 4095, 0, 1, and 2. 

If Ack 2 is also lost or corrupted and no further Ack or Nak DLLPs are returned to Device A, its REPLAY_TIMER expires causing a replay of its entire buffer. Device B sees TLPs 4094, 4095, 0, 1 and 2 and considers them to be duplicates [their sequence numbers are earlier than NEXT_RCV_SEQ count (3)]. They are discarded and _another_ Ack 2 would be returned to Device A because of the duplicate packets. 

_Figure 10‐14: Handling Bad Ack_ 

**==> picture [368 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>