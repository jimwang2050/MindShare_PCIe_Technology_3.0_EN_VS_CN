**Replay Number Rollover.** When this happens, the assumption is that there must be something wrong with the Link, so the Link Layer trig‐ gers the Physical Layer to re‐train the Link, causing it to go into the Recov‐ ery State (see “Recovery State” on page 571). If the optional Advanced Error Reporting registers are implemented, the Replay Number Rollover error status bit will also be set (“Advanced Correctable Error Handling” on page 688). The Replay Buffer contents are preserved and the Link Layer is not initialized during the re‐training process (this is simply re‐training the Link, not performing a reset of the Link). When re‐training completes, the transmitter resumes the same replay process again in hopes that the prob‐ lem has been cleared and the TLPs can now be replayed successfully. 

The spec does not describe how a device might handle repeated rollover events if the Link training doesn’t clear the problem. The author has seen commercially available hardware that had no mechanism to detect this con‐ dition and got stuck in an endless loop of re‐training. It seems good there‐ fore, to recommend that a device track the number of re‐train attempts. After sufficient attempts, the device could signal an Uncorrectable Fatal Error or an interrupt as a way to notify software of this condition. 

## **Replay Timer** 

The transmitter REPLAY_TIMER is running anytime there are TLPs that have been transmitted but have not yet been acknowledged. The goal of the REPLAY_TIMER is to ensure that TLPs are being acknowledged in a timely fashion. If this timer expires, it indicates that an Ack or Nak should have been received by that point in time, so something must have gone wrong and the fix from the transmitter’s point‐of‐view is to perform a replay, meaning to re‐send everything in the Replay Buffer. 

**336** 

**Cha ter 10: Ack/Nak Protocol p** 

Based on the purpose of this timer, it makes sense that its timeout value should be correlated the AckNak_LATENCY_TIMER in the receiver. In fact, the REPLAY_TIMER is simply three times longer than the AckNak_LATENCY_TIMER. 

A formula in the spec determines the timer’s count value. Its expiration triggers a replay event and increments the REPLAY_NUM counter. A couple of cases where timeout may arise is if an Ack or Nak is lost en route, or because an error in the receiver prevents it from returning an Ack or Nak. Timer‐related rules: 

- If not already running, the timer starts when the last symbol of any TLP is transmitted 

- The timer is reset and restarted when: 

   - An Ack indicating forward progress is received, AND there are still unacknowledged TLPs in the Replay Buffer 

   - A Replay event occurs and the last symbol of the first replayed TLP is sent 

- The timer is reset and held when: 

   - There are no TLPs to transmit, or the Replay Buffer is empty 

   - A Nak is received; it restarts when the last symbol of the first replayed TLP is sent 

   - The timer expires; it restarts when the last symbol of the first replayed TLP is sent 

   - 

   - The Data Link Layer is inactive 

- The timer is held during Link training or re‐training 

**REPLAY_TIMER Equation.** The timeout value depends primarily on the max data payload and the width of the Link. The equation to calculate the REPLAY_TIMER value in symbol times is given below. Note that the value is simply three times the Ack/Nak Latency value. 

. 

( Max_Payload_Size + TLPOverhead ) * AckFactor LinkWidth ( 

+ InternalDelay *** 3** + _Rx_L0s_Adjustment_ ) _this term removed_ ( _for Gen2 and later_ ) 

The equation fields are defined as follows: 

- **Max_Payload_Size** ‐ the value in the Device Control Register. In the case of multiple Functions with different Max_Payload_Size values, the spec recommends using the smallest one of them. 

**337** 

**PCI Ex ress Technolo p gy** 

- **TLP Overhead** ‐ the additional TLP fields beyond the data payload (sequence number, header, digest, LCRC and Start/End framing sym‐ bols). In the spec, the overhead value is treated as a constant of 28 sym‐ bols. 

- **AckFactor** (AF) ‐ is basically a fudge factor representing the number of max payload‐sized TLPs that can be received before an Ack must be sent. The AF value ranges from 1.0 to 3.0 and is intended to balance Link bandwidth efficiency and Replay Buffer size. The table in Figure 10‐11 on page 339 shows the Ack Factor values for various link widths and payload sizes. These Ack Factor values are chosen to allow imple‐ mentations to achieve good performance without requiring a large uneconomical buffer. 

- **LinkWidth** ‐ ranges from x1 (1‐bit wide) to x32 (32‐bits wide). 

- **InternalDelay** ‐ the internal delay of processing a TLP within the receiver and DLLPs (Acks) within the transmitter. This value is defined in the spec in symbol times, and depends on the Link speed: Gen1 = 19, Gen2 = 70, Gen3 = 115. 

- **Rx_L0s_Adjustment** ‐ This is a value that was included in the 1.x PCIe specs but was dropped for 2.0 and later PCIe specs. It could be used to account for the time required by the receive circuits to exit from L0s to L0. Setting the Extended Sync bit of the Link Control register affects the exit time from L0s and must be taken into account in this adjustment. Interestingly, the spec writers chose to assume this to be zero when cre‐ ating their table of Replay Timer values. More on this in the following section. 

**REPLAY_TIMER Summary Table.** Figure 10‐11 on page 339 is a summary table for the Gen1 rate that shows timer load values for various values of the variables in the REPLAY_TIMER equation. The numbers have changed for the newer generations of the spec, and the new tables and a dis‐ cussion of them can be found in the section called “Timing Differences for Newer Spec Versions” on page 350. The tolerance for all of the table values is ‐0% to +100%. 

Note that the table values in the spec (copied here for convenience) are con‐ sidered “unadjusted” because they leave out the last item of the equation involving the time to recover from L0s. No explanation is given for this in the spec, but if the Link had to wake up from L0s to L0 just to replay a packet in case the timeout might have been an error, that would be poor power management. 

**338** 

**Cha ter 10: Ack/Nak Protocol p** 

A simple way to avoid this problem altogether is for the transmitter to ensure that the Replay Buffer is empty before entering L0s. The spec requires that step for entry into L1 but not L0s, and the reason probably has to do with the relative risk involved. Going to L1 requires a longer recovery process back to L0 that has some small risk of failure. If it fails to recover, the Physical Layer state machine will have to do more of the Link training, a process that clears the LinkUp flag to the Link Layer, causing the Link Layer to re‐initialize. If there were entries in the Replay Buffer when that happened they’d be lost and problems could result. The recovery risk from L0s was evidently considered low enough not to warrant that requirement. Still, the L0s latency was left out when the table was constructed, leaving the reader to wonder about this. In the author’s opinion, the spec writers expected designers to take steps to ensure that a Replay Timer timeout either doesn’t occur while in L0s (by emptying the Replay Buffer before L0s entry), or will be delayed if the path for the Acks is observed to be in L0s. 

_Figure 10‐11: Gen1 Unadjusted REPLAY_TIMER Values_ 

||**Max_Payload**<br>**Size**|**X1**<br>**Link**|**X2**<br>**Link**|**X4**<br>**Link**|**X8**<br>**Link**|**X12**<br>**Link**|**x16**<br>**Link**|**X32**<br>**Link**|
|---|---|---|---|---|---|---|---|---|
||**128 Bytes**|**711**|**384**|**219**|**201**|**174**|**144**|**99**|
||**256 Bytes**|**1248**|**651**|**354**|**321**|**270**|**216**|**135**|
||**512 Bytes**|**1677**|**867**|**462**|**258**|**327**|**258**|**156**|
||**1024 Bytes**|**3213**|**1635**|**846**|**450**|**582**|**450**|**252**|
||**2048 Bytes**|**6285**|**3171**|**1614**|**834**|**1095**|**834**|**444**|
||**4096 Bytes**|**12,429**|**6243**|**3150**|**1602**|**2118**|**1602**|**828**|
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||



**339** 

**PCI Ex ress Technolo p gy** 

## **Transmitter DLLP Handling** 

The Ack/Nak Error Checking block determines whether there is an error in the 16‐bit CRC of a received DLLP. If an error is detected, the DLLP is discarded. This is considered a correctable error and may have been set up to be reported in the optional Advanced Error Reporting registers (see Bad DLLP in “Advanced Correctable Error Handling” on page 688), but no further action is taken because this isn’t really a problem. The next successfully received DLLP of that type will bring the counters back up to speed. Consequently, TLPs might be purged a little later than they would have been or a replay may happen at a later time, but no information is lost. Of course, if the delay between successful Acks becomes too large, the REPLAY_TIMER could expire, causing the TLPs to be replayed. 

## **Receiver Protocol Details** 

## **Physical Layer** 

TLPs received at the Physical Layer are checked for receiver errors (such as framing, disparity, and invalid symbols). If there are errors at this level, the TLP is discarded and the Link Layer may be informed by some design‐specific method so it can schedule a Nak and have the packet replayed. If the Link Layer is not informed, then eventually it will detect a Sequence Number violation and that will cause a Nak and a replay. 

**340** 

**Cha ter 10: Ack/Nak Protocol p** 

_Figure 10‐12: Ack/Nak Receiver Elements_ 

**==> picture [224 x 283] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- End of picture text -----**<br>


## **TLP LCRC Check** 

If there were no Physical Layer errors, the Link Layer checks first for CRC errors. The receiver calculates an expected LCRC value from the received TLP (excluding the LCRC field) and compares this value with the TLP’s 32‐bit LCRC. If the two match, the TLP is good. Otherwise, the TLP is discarded and the receiver schedules a Nak. 

## **Next Received TLP’s Sequence Number** 

If the LCRC was correct, the receiver next compares the NEXT_RCV_SEQ counter against the Sequence Number that should be in the newly‐received TLP. Under normal operational conditions, these two numbers will match. If they do, the receiver forwards the TLP to the Transaction Layer, increments the NEXT_RCV_SEQ counter, and schedules an Ack. 

**341** 

**PCI Ex ress Technolo p gy** 

If the received TLP’s Sequence Number turns out to be earlier or later than the NEXT_RCV_SEQ count, we have one of two cases: a duplicate TLP or an out of sequence TLP. 

**Duplicate TLP.** If the Sequence Number of the incoming packet is ear‐ lier (logically smaller) than the expected value, it means the transmitter decided to resend a packet that the receiver has already seen before. This duplicate packet is not an error although we are wasting time on the Link by resending it. This might be caused by a timeout at the transmitter if the Ack or Nak for a previous TLP failed. When this is seen at the receiver, the duplicate packet is discarded and an Ack is scheduled with the Sequence Number of the last good TLP it has received (which is probably not the same Sequence Number in the replayed TLP). 
