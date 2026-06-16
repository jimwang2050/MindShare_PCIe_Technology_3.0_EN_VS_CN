**General.** Before a device transmits a TLP, it stores a copy of the TLP in the Replay Buffer. ( _Note that the spec uses the term Retry Buffer but in this book ‘Replay’ was chosen instead of ‘Retry’ to more clearly distinguish this mechanism from the old PCI Retry mechanism_ ). Each buffer entry stores a complete TLP with all of its fields including the Sequence Number (12 bits wide, it occu‐ pies two bytes), Header (up to 16 bytes), an optional Data Payload (up to 4KB), an optional ECRC (four bytes) and the LCRC field (four bytes). 

It is important to note that the spec describes the Replay Buffer in this fash‐ ion, but it is NOT a spec requirement that it be implemented this way. As long as your device can replay a sequence of TLPs if required, as defined by the spec, then how that is accomplished within a device is completely up to the designer. Having a Replay Buffer that behaves as described above is one way to accomplish this. 

**Replay Buffer Sizing.** The spec writers chose not to specify the Replay Buffer size, leaving it as an optimization for the device designers. It should be made big enough to store TLPs that haven’t yet been acknowledged by Acks so that under normal operating conditions it doesn’t become full and stall new TLPs coming in from the Transaction Layer, but also small enough to keep the cost down. To determine the optimal buffer size, a designer will consider: 

- Ack DLLP Latency from the receiver. 

- Delays caused by the physical Link. 

- Receiver L0s exit latency to L0. In other words, the buffer should be big enough to hold TLPs without stalling while the Link returns from the L0s state to L0. 

When the transmitter receives an Ack, it purges TLPs from the Replay Buffer with Sequence Numbers equal to or earlier than the Sequence Num‐ ber in the Ack ( _normally this term would be ‘smaller than’ but the counter roll‐ over behavior will sometimes make that an incorrect evaluation, so the term ‘earlier than’ was chosen instead_ ). Similarly, when the transmitter receives a Nak, it still purges the Replay Buffer of TLPs with Sequence Numbers that are equal to or earlier than the Sequence Number that arrives in the Nak, but then it also replays (re‐sends) TLPs of later Sequence Numbers (the remain‐ ing TLPs in the Replay Buffer). 

**330** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Transmitter’s Response to an Ack DLLP** 

A single Ack returned by the receiver may acknowledge multiple TLPs; it isn’t necessary that every TLP transmitted receive a dedicated Ack. The receiver can get multiple good TLPs and send one Ack with the Sequence Number of the last good TLP received. The transmitter’s response to an Ack that makes forward progress (has a Sequence Number that is later than the last one seen) is to load the AckD_SEQ register with the Sequence Number of the new Ack. It also resets the REPLAY_NUM counter and REPLAY_TIMER, and purges the Replay Buffer of all TLPs that were acknowledged by that Ack. 

## **Ack/Nak Examples** 

**Example 1.** Consider Figure 10‐8 on page 332 for the following discus‐ sion. 

1. Device A transmits TLPs with Sequence Numbers 3, 4, 5, 6, 7. 

2. Device B successfully receives TLP 3 and increments its NEXT_RCV_SEQ counter from 3 to 4. Since Device B had previously acknowledged all successfully received TLPs, the AckNak_LATENCY_TIMER was not running. Having received TLP 3, Device B has now successfully received a TLP that it has not acknowl‐ edged, so the AckNak_LATENCY_TIMER is started (this is equivalent of scheduling an Ack). 

3. Device B successfully receives TLPs 4 and 5 before the AckNak_LATENCY_TIMER expires. Receiving TLPs 4 and 5 does NOT reset the AckNak_LATENCY_TIMER. 

4. Once the AckNak_LATENCY_TIMER expires, Device B sends a single Ack with the Sequence Number 5, the last good TLP received. The AckNak_LATENCY_TIMER is reset but does not restart until it suc‐ cessfully receives TLP 6. 

5. Device A receives Ack 5, resets the REPLAY_TIMER and REPLAY_NUM counter, because forward progress is being made. And it purges TLPs from the Replay Buffer that have Sequence Numbers earlier than or equal to 5. 

6. Once Device B receives TLPs 6 and 7 and its AckNak_LATENCY_TIMER expires again, it will send an Ack with a Sequence Number of 7 which will purge the last two TLPs in the Replay Buffer of Device A (according to this example). 

**331** 

## **PCI Ex ress Technolo p gy** 

_Figure 10‐8: Example 1 ‐ Example of Ack_ 

**==> picture [378 x 249] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 Good TLP<br>Receive Buffer<br>4 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>5 Good TLP<br>Replay Buffer 8 NEXT_RCV_SEQ<br>6<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 7<br>6 Ack<br>Purge Lat Tmr<br>5 5<br>4<br>Earlier TLP 3 Ack/Nak<br>Generator<br>Link<br>7 6<br>**----- End of picture text -----**<br>


**Example 2.** This example is showing the exact same behavior as Exam‐ ple 1, but it is pointing out the rollover behavior for the Sequence Numbers, as show in Figure 10‐9 on page 333. 

1. Device A transmits TLPs with Sequence Numbers 4094, 4095, 0, 1, and 2 where TLP 4094 is the first TLP sent and TLP 2 is the last TLP sent in this example. 

2. Device B successfully receives TLPs with Sequence Numbers 4094, 4095, 0, 1 in that order. Reception of TLP 4094 causes the AckNak_LATENCY_TIMER to start. TLPs 4095, 0 and 1 are received before the AckNak_LATENCY_TIMER expires. TLP 2 is still en route. 

3. Because the AckNak_LATENCY_TIMER expires, Device B send an Ack with a Sequence Number of 1 to acknowledge receipt of TLP 1 and all prior TLPs (0, 4095 and 4094 in this example). 

4. Device A successfully receives Ack 1, purges TLPs 4094, 4095, 0, and 1 from the Replay Buffer and resets the REPLAY_TIMER and REPLAY_NUM count. 

**332** 

**Cha ter 10: Ack/Nak Protocol p** 

_Figure 10‐9: Example 2 ‐ Ack with Sequence Number Rollover_ 

**==> picture [381 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>1 Good TLP<br>Replay Buffer 3 NEXT_RCV_SEQ<br>2<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 2 Ack<br>Purge<br>1 1<br>0 Lat Tmr<br>4095<br>Earlier TLP 4094 Ack/Nak<br>Generator<br>Link<br>2<br>**----- End of picture text -----**<br>


## **Transmitter’s Response to a Nak** 

A Nak indicates that a problem has occurred. When a transmitter receives one, it first purges from the Replay Buffer any TLPs with earlier or equal Sequence Numbers and then replays the remaining TLPs starting with the Sequence Number immediately after the Sequence Number in the Nak. If the Nak caused at least one TLP to be purged from the buffer, then we’ve made forward progress. In that case, the transmitter resets the REPLAY_NUM counter and REPLAY_TIMER and loads the AckD_SEQ register with the Sequence Number of the Nak. 

## **TLP Replay** 

When a Replay becomes necessary, the transmitter blocks acceptance of new TLPs from its Transaction Layer. It then replays the necessary TLPs in the buffer in the same order they were placed into the buffer (like a FIFO). After the replay event, the Data Link Layer unblocks acceptance of new TLPs from its Transac‐ 

**333** 

**PCI Ex ress Technolo p gy** 

tion Layer. The replayed TLPs remain in the buffer until they are finally acknowledged at some later time. 

## **Efficient TLP Replay** 

Ack or Nak DLLPs received during replay must be processed. So there are two main options here, the transmitter may hold them until the replay is finished and then evaluate the Acks or Naks and take the appropriate steps. Another option would be to begin processing the new Ack/Nak DLLPs even during the replay. If this option is used, the newly received Acks might purge some entries from the buffer while replay is in progress, possibly reducing the number of TLPs that need to be replayed and saving time on the Link. This is allowed, but it is important to remember that once a TLP is started for transmission, it must be completed. 

## **Example of a Nak** 

Consider Figure 10‐10 on page 335. 

1. Device A transmits TLPs with Sequence Number 4094, 4095, 0, 1, and 2. 

2. Device B receives TLP 4094 without error and increments the NEXT_RCV_SEQ count to 4095 and starts the AckNak_LATENCY_TIMER. 

3. Device B detects a CRC error in the next TLP received (TLP 4095) and sets the NAK_SCHEDULED flag, which will cause a Nak to be sent with Sequence Number 4094 (NEXT_RCV_SEQ count ‐ 1). Device B does NOT wait until the AckNak_LATENCY_TIMER expires before sending the Nak. It will typically be sent on the next packet boundary. In face, since a Nak is scheduled for transmission, the AckNak_LATENCY_TIMER is stopped and reset. 

4. Device B will continue evaluating incoming TLPs looking for TLP 4095. However, because Device A did not know there was a problem yet, it had sent packets 0, 1 and 2, which Device B will receive. However, Device B will not accept them, even though they may be good TLPs (meaning they did not fail the LCRC check). This is because all packets have to be accepted in order. So Device B will simply drop those pack‐ ets because they are considered out of sequence, but no addition Nak will be sent. Even if one or more of these TLPs fail the LCRC check, no additional NAK is sent. The NAK_SCHEDULED flag is already set and it will only be cleared once Device B successfully receives the TLP it is expecting (TLP 4095 in this example). 

**334** 

**Cha ter 10: Ack/Nak Protocol p** 

5. Device A receives Nak 4094 and purges TLP 4094 and earlier TLPs (none in this example) from the Replay Buffer. Also, since forward progress was made, it resets the REPLAY_TIMER and REPLAY_NUM count. 

6. Since the acknowledge DLLP received was a Nak and not an Ack, Device A then replays all remaining TLPs in the Replay Buffer (TLPs 4095, 0, 1, and 2) and restarts the REPLAY_TIMER and increments the REPLAY_NUM count by one. 

7. Once Device B receives the replayed TLP 4095, it will clear the NAK_SCHEDULED flag, increment the NEXT_RCV_SEQ count and start the AckNak_LATENCY_TIMER. 

_Figure 10‐10: Example of a Nak_ 

**==> picture [372 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
Receive Buffer 4094 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>4095<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 4095 LCRC fail<br>Later TLP 2<br>1<br>0 Lat Tmr<br>4095 Nak 0 Out of sequence<br>Earlier TLP 4094 Purge 4094 Ack/Nak<br>Generator<br>Link<br>Replayed TLPs<br>2 1 0 4095 2 1<br>**----- End of picture text -----**<br>


## **Repeated Replay of TLPs** 

**General.** Each time the transmitter receives a Nak, it replays the buffer contents, and the 2‐bit REPLAY_NUM counter is incremented to keep track of the number of replay events. The replay caused by a Nak in the previous example will increment REPLAY_NUM. 

**335** 

## **PCI Ex ress Technolo p gy** 

If the replay doesn’t clear the problem, though, we enter a new situation. The receiver has set the Nak Scheduled Flag and cannot send any more Acks or Naks until it sees the offending TLP correctly received. If the replay doesn’t make that happen for some reason, then there will be no response from the receiver. What saves us now is the transmitter’s REPLAY_TIMER. When it times out, the entire contents of the Replay Buffer will be resent, the REPLAY_NUM counter will be incremented and the REPLAY_TIMER will be reset and restarted. If the REPLAY_TIMER expires without receiving an Ack or Nak indicating forward progress, this replay process can be repeated up to three times. If after the third replay, there is still no forward progress and the REPLAY_TIMER expires again, this would cause the REPLAY_NUM counter to roll over from 3 back to 0. 
