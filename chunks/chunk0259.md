As shown in Figure 10‐4 on page 322, when an Ack or Nak makes forward progress it causes TLPs with Sequence Numbers equal to or older than the value in the DLLP to be purged out of the Replay Buffer. It also resets both the REPLAY_TIMER and the REPLAY_NUM count. If no forward progress is made, no TLPs can be purged so we only check to see if it’s a Nak that would necessi‐ tate a replay. 

This is a good place to mention a potential problem with the counters: the num‐ ber of TLPs sent might theoretically become much larger than the number that have been acknowledged by the receiver. As mentioned earlier, this is very unlikely; it’s only mentioned here for completeness. The problem is basically the same as it for the Flow Control counters (see “Stage 3 — Counters Roll Over” on page 234) and has the same solution: the NEXT_TRANSMIT_SEQ and ACKD_SEQ counters are never allowed to be separated by more than half their total count value. If a large number of TLPs are sent without acknowledgement so that the NEXT_TRANSMIT_SEQ count value is later than ACKD_SEQ count by 2048, no more TLPs will be accepted from the Transaction Layer until this is resolved by receiving more Acks. If the difference between the Sequence Num‐ ber sent and the acknowledged count ever did exceed half the maximum count value, a Data Link Layer protocol error would be reported. (For more on error reporting, see “Data Link Layer Errors” on page 655.) 

## **DLLP CRC Check** 

This block checks for errors in the 16‐bit CRC of DLLPs. If an error is detected, the DLLP is discarded and a Correctable Error may be reported, if enabled. No further action is taken because there is no mechanism to replay or correct failed DLLPs. Instead, we simply wait for the next successful Ack/Nak, which will get the counters back up‐to‐date and allow normal operation to continue. 

## **Receiver Elements** 

Incoming TLPs are first checked for LCRC errors and then for Sequence Num‐ bers. If there are no errors, the TLP is forwarded to the receiver’s Transaction 

**324** 

**Cha ter 10: Ack/Nak Protocol p** 

Layer. If there are errors, the TLP is discarded and a Nak will be scheduled unless there was already a Nak outstanding. 

Figure 10‐5 on page 325 illustrates the receiver Data Link Layer elements associ‐ ated with processing of inbound TLPs and outbound Ack/Nak DLLPs. 

_Figure 10‐5: Receiver Elements Associated with the Ack/Nak Protocol_ 

**==> picture [223 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- End of picture text -----**<br>


## **LCRC Error Check** 

This block checks for transmission errors in the received TLP by verifying the 32‐bit LCRC. This block calculates an LCRC value based on the received bits of the TLP and then compares the calculated LCRC to the received LCRC. If they match, then all the bits of the packet were received exactly as they were trans‐ mitted. If it doesn’t match, then there was a bit error in the TLP so it gets dropped and a Nak will be sent to get a replay of that packet and any TLPs sent after the bad packet. 

**325** 

**PCI Ex ress Technolo p gy** 

## **NEXT_RCV_SEQ Counter** 

The 12‐bit NEXT_RCV_SEQ (Next Receive Sequence number) counter keeps track of the expected Sequence Number and is used to verify sequential packet reception. It’s initialized to 0 at reset or when the Data Link Layer is inactive, and is incremented once for each good TLP forwarded to the Transaction Layer. TLPs that have errors or were nullified are not sent to the Transaction Layer and therefore don’t increment this counter. 

## **Sequence Number Check** 

If the LCRC check was OK, the TLP’s Sequence Number is checked against the expected count (the NRS number). As can be seen in Figure 10‐5 on page 325, there are three possible outcomes of this check: 

1. The TLP Sequence Number equals the NRS count (the number we’re expecting). In this case, everything is good: the TLP is accepted and for‐ warded to the Transaction Layer and the NRS count is incremented. The Receiver schedules an Ack, but it doesn’t have to be sent until the AckNak_LATENCY_TIMER expires. In the meantime, other good TLPs may be received, incrementing the NEXT_RCV_SEQ counter. Then, once the timer expires, a single Ack is sent with the Sequence Number of the last good TLP received (NRS ‐ 1). That allows one Ack to represent several suc‐ cessful TLPs and reduces overhead, since a dedicated Ack is not required for every TLP. 

2. If the TLP’s Sequence Number is earlier than the NRS count (smaller than expected), this TLP has been seen before and is a duplicate. As long as the expected Sequence Number and received Sequence Number don’t get sepa‐ rated by more than half the total count value (2048), this is not an error, but is seen as a duplicate, meaning the TLP has already been accepted earlier. In this case, the TLP is silently dropped (no Nak, no error reporting) and an Ack is sent with the Sequence Number of the last good TLP it received (NRS ‐ 1). Why would this situation happen? The transmitter may not have received a transmitted Ack, so his REPLAY_TIMER expired and he retrans‐ mitted everything in his Replay Buffer. By sending the transmitter an Ack with the Sequence Number of the last good packet we received, we’re noti‐ fying him of the furthest progress we’ve made. 

3. If the TLP’s Sequence Number is a later Sequence Number than NEXT_RCV_SEQ count (larger than expected), then the Link Layer has missed a TLP. For example, if we’re expecting Sequence Number 30 and the incoming TLP has Sequence Number 31 we know there’s a problem. The numbers must be sequential and, since they aren’t, one must have failed 

**326** 

**Cha ter 10: Ack/Nak Protocol p** 

and been dropped, as might happen at the Physical Layer. This out‐of‐order TLP is discarded, whether or not it had any other errors because we must accept TLPs in order, and a Nak will be sent if there wasn’t one already out‐ standing. 

The concept of the expected sequence number (NRS) incrementing as new TLPs are successfully received and seeing how that affects the sliding windows for the invalid range of sequence numbers and the duplicate range of sequence numbers can be seen in Figure 10‐6. 

_Figure 10‐6: Examples of Sequence Number Ranges_ 

**==> picture [270 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 30 2078 4095<br>Dupli- Invalid<br>Duplicate<br>cate (out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 31 2079 4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 32 2080 4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>**----- End of picture text -----**<br>


## **NAK_SCHEDULED Flag** 

This flag is set whenever the receiver schedules a Nak, and is cleared when the receiver successfully receives the TLP with the expected Sequence Number (NRS). The spec is clear that the receiver must not schedule additional Nak DLLPs while the NAK_SCHEDULED flag remains set. The author’s opinion is 

**327** 

**PCI Ex ress Technolo p gy** 

that this is intended to prevent the possibility of an endless loop; a case in which the transmitter begins to replay some packets but the receiver sends another Nak before the replays finish and causes it to restart sending them again. What‐ ever the motivation, once a Nak has been sent there will be no more Naks forth‐ coming until the problem is resolved by successful receipt of the replayed TLP with the correct Sequence Number. 

## **AckNak_LATENCY_TIMER** 

This timer is running anytime a receiver successfully receives a TLP that it has not yet acknowledged. The receiver is required to send an Ack once the timer expires. The length of time the AckNak Latency Timer runs is dictated by the spec (see “AckNak_LATENCY_TIMER” on page 328) and determines how long a receiver can coalesce Acks. Once the AckNak Latency Timer expires, an Ack with sequence number NRS‐1 is generated and sent which indicates the last good packet it received. This timer is reset whenever an Ack or Nak are sent and it only restarts once a new good TLP is received. 

## **Ack/Nak Generator** 

Ack or Nak DLLPs are scheduled by the error checking blocks and contain a 12‐ bit AckNak_Seq_Num field as illustrated in Figure 10‐7 on page 328. It calcu‐ lates this number by subtracting one from the NRS count, which results in reporting the last good Sequence Number received. That’s because a good TLP received increments NRS before scheduling the Ack, while a failed TLP just schedules a Nak without incrementing NRS. This method makes it easier to handle failed packets because the error in the TLP might have been in the Sequence Number, so that number can’t be used in the Nak. Instead, it uses the number of the last good TLP; what we’re expecting minus one. The only case where this value doesn’t represent the last good TLP is for the first TLP after a reset. If that first TLP, using Sequence Number 0, fails, the resulting Nak will have an AckNak_Seq_Num value of zero minus one which results in all 1’s. 

_Figure 10‐7: Ack Or Nak DLLP Format_ 

**==> picture [386 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved AckNak_Seq_Num<br>Byte 4 16-bit CRC<br>**----- End of picture text -----**<br>


**328** 

**Cha ter 10: Ack/Nak Protocol p** 

_Table 10‐1: Ack or Nak DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:0]|Indicates the type:<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|This value will always be NEXT_RCV_SEQ<br>count ‐ 1.|
|16‐bit CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|16‐bit CRC used to protect the contents of<br>this DLLP.|



## **Ack/Nak Protocol Details** 

This section describes the detailed transmitter and receiver behavior in process‐ ing TLPs and Ack/Nak DLLPs. Several examples are used to demonstrate vari‐ ous cases that may occur. 

## **Transmitter Protocol Details** 

## **Sequence Number** 

Referring back to Figure 10‐4 on page 322, when TLPs are delivered by the Transaction Layer to the Link Layer, one of the first steps is to append a 12‐bit Sequence Number. Keep in mind that the next incremental Sequence Number may actually be smaller, as will happen when the counter rolls over back to zero after it reaches a maximum value of 4095. Consequently, a value of zero can actually be ‘larger’ than a value of 4095, for example. It may help to think of the Sequence Number comparison as evaluating a ‘window’ of numbers that con‐ sistently moves upward and rolls over. To clarify this concept, such a count roll‐ over is used in several of the upcoming examples. 

## **32-Bit LCRC** 

The transmitter also generates and appends a 32‐bit LCRC (Link CRC) based on the TLP contents (Sequence Number, Header, Data Payload and ECRC). 

**329** 

**PCI Ex ress Technolo p gy** 

## **Replay (Retry) Buffer** 
