4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>1<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Later TLP 2 Replay 1 2 Out of sequence<br>1 Ack<br>Purge Lat Tmr<br>0 0<br>4095<br>Earlier TLP 4094 Ack/Nak<br>0 Nak Generator<br>Link<br>Replayed TLPs<br>2 1<br>**----- End of picture text -----**<br>


**347** 

**PCI Ex ress Technolo p gy** 

## **Bad Nak** 

Figure 10‐15 on page 349 which shows protocol for handling a corrupt Nak. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B receives TLPs 4094, 4095, and 0 all successfully (and the AckNak_LATENCY_TIMER has not yet expired). The next TLP that it receives fails the LCRC check, so Device B sets the NAK_SCHEDULED flag, and resets and holds the AckNak_LATENCY_TIMER. The Nak is transmit‐ ted back with a Sequence Number of the last good TLP received, 0. 

3. Nak 0 fails the 16‐bit CRC check at Device A and is discarded. 

4. At this point, Device B will not be sending anymore Acks or Naks until it successfully receives the next TLP it is expecting, TLP 1 in this example. However, this will require a replay. Device A does not yet know that a replay is required because the one Nak that was sent back was corrupted and discarded. This gets resolved by the REPLAY_TIMER. The REPLAY_TIMER will eventually expire because it has not seen an Ack or Nak that makes forward progress in the specified time frame. 

5. Once the REPLAY_TIMER expires, Device A will replay all TLPs in the Replay Buffer, increment REPLAY_NUM count and reset and restart the REPLAY_TIMER. 

6. Device B will receive TLPs 4094, 4095 and 0 and recognize that they are duplicates. The duplicate TLPs will be dropped and an Ack will be sched‐ uled with a Sequence Number 0 (indicating the furthest progress made). 

7. Once TLP 1 is successfully received by Device B, it will clear the NAK_SCHEDULED flag, increment the NEXT_RCV_SEQ and restart the AckNak_LATENCY_TIMER because it has successfully received a TLP that it has not yet acknowledged. 

**348** 

**Cha ter 10: Ack/Nak Protocol p** 

## _Figure 10‐15: Handling Bad Nak_ 

**==> picture [383 x 266] intentionally omitted <==**

**----- Start of picture text -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>3<br>REPLAY_TIMER<br>(expires) NAK_SCHEDULED<br>1 1 LCRC Fail<br>Later TLP 2<br>1 Replay<br>0 Lat Tmr<br>4095 Nak<br>Earlier TLP 4094 2 CRC Ack/Nak 2 Out of sequence<br>Fail Generator<br>Link<br>Replayed TLPs<br>2 1 0 4095 4094<br>**----- End of picture text -----**<br>


## **Error Situations Handled by Ack/Nak** 

The Ack/Nak protocol guarantees reliable delivery of TLPs despite several pos‐ sible errors. The list of errors below includes the correction mechanism used to resolve them. 

- **LCRC error** in a TLP. **Solution** : Receiver detects LCRC error and schedules a Nak that contains the NEXT_RCV_SEQ count ‐ 1. In response, the trans‐ mitter replays at least one TLP, starting with the one that failed. 

- **TLPs lost** en route to the receiver’s Data Link Layer ( _e.g._ Physical Layer detects issue with packet and drops it). **Solution** : The receiver checks the Sequence Number on all received TLPs, expecting them to arrive with the next sequential Sequence Number. If a TLP is lost, the Sequence Number of the next one that succeeds will be out of sequence. In response, the Receiver 

**349** 

**PCI Ex ress Technolo p gy** 

   - schedules a Nak with NRS count ‐ 1, and the transmitter replays at least one TLP, starting with the missing one. 

- **Corrupted Ack or Nak** en route to the transmitter. **Solution:** The Transmit‐ ter detects a CRC error in the DLLP (see “Receiver handling of DLLPs” on page 309), discards the packet and simply waits for the next one. 

   - **Ack Case:** A subsequent Ack received with a later Sequence Number causes the transmitter Replay Buffer to purge all TLPs with Sequence Numbers equal to or earlier than it. The transmitter is unaware that anything was wrong (except for a potential case of the Replay Buffer temporarily filling up). 

   - **Nak Case:** The receiver, having set the Nak Scheduled flag, will not send another Nak or any Acks until it successfully receives the next expected TLP, meaning a replay is needed. Of course, the transmitter doesn’t know it needs to replay if the Nak was lost. In this case, the REPLAY_TIMER will eventually expire and trigger the replay. 

- **No Ack/Nak seen** within the expected time. **Solution** : REPLAY_TIMER timeout triggers a replay. 

- **Receiver fails to send Ack/Nak** for a received TLP. **Solution** : Again, the transmitter’s REPLAY_TIMER will expire and result in a replay. 

## **Recommended Priority To Schedule Packets** 

A device may have many types of TLPs, DLLPs and Ordered Sets to transmit on a given Link. The recommended priority for scheduling packets is: 

1. Completion of any TLP or DLLP currently in progress (highest priority) 2. Ordered Set 

3. Nak 

4. Ack 

5. Flow Control 

6. Replay Buffer re‐transmissions 

7. TLPs that are waiting in the Transaction Layer 

8. All other DLLP transmissions (lowest priority) 

## **Timing Differences for Newer Spec Versions** 

As mentioned earlier, the timer values for the Ack/Nak protocol are different for Gen2 and later versions of the spec. To improve readability of the text, only the Gen1 versions (2.5 GT/s rate) were included in the earlier discussion, but all three versions are included here for convenience. 

**350** 

**Cha ter 10: Ack/Nak Protocol p** 

As before, the values given are in symbol times, so the actual time is that value multiplied by the time needed to deliver one symbol over the Link at that rate. For review, the time to transmit one symbol (known as a Symbol Time) is 4ns for Gen1, 2ns for Gen2, and 1.25ns to transmit 1 byte for Gen3. 

## **Ack Transmission Latency (AckNak Latency)** 

One interesting difference between the spec versions is the way the L0s recov‐ ery time is considered. In the 1.x specs, an argument is included in the AckNak_LATENCY_TIMER equation to account for this, but the tables in the spec based on that equation put its value at zero and call the resulting values ‘unadjusted’. Beginning with the 2.0 spec, the L0s recovery value is dropped from the equation altogether and the text states that the receiver is not required to adjust Ack scheduling based on L0s exit latency or the value of the Extended Sync bit. None of the table values contain an L0s recovery component and are therefore all still called ‘unadjusted’. 

Note that, since the AF (Ack Factor) values are the same in all the tables and were shown in the earlier presentation of the Gen1 table, they’re not included in the tables here. 

Also, as it was for Gen1, the tolerance for all of the table values is ‐0% to +100%. To illustrate this, Table 10‐3 on page 351 lists the time for a x1 Link and Max Payload size of 128 Bytes as 237 symbol times. Legal values would therefore range from no less than 237 symbol times to no more than 474. 

## **2.5 GT/s Operation** 

_Table 10‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|237|128|73|67|58|48|33|
|256 Bytes|416|217|118|107|90|72|45|
|512 Bytes|559|289|154|86|109|86|52|
|1024 Bytes|1071|545|282|150|194|150|84|
|2048 Bytes|2095|1057|538|278|365|278|148|



**351** 

## **PCI Ex ress Technolo p gy** 

_Table 10‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|4096 Bytes|4143|2081|1050|534|706|534|276|



## **5.0 GT/s Operation** 

_Table 10‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|288|179|124|118|109|99|84|
|256 Bytes|467|268|169|158|141|123|96|
|512 Bytes|610|340|205|137|160|137|103|
|1024 Bytes|1122|596|333|201|245|201|135|
|2048 Bytes|2146|1108|589|329|416|329|199|
|4096 Bytes|4194|2132|1101|585|757|585|327|



## **8.0 GT/s Operation** 

_Table 10‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|333|224|169|163|154|144|129|
|256 Bytes|512|313|214|203|186|168|141|
|512 Bytes|655|385|250|182|205|182|148|
|1024 Bytes|1167|641|378|246|290|246|180|
|2048 Bytes|2191|1153|634|374|461|374|244|
|4096 Bytes|4239|2177|1146|630|802|630|372|



**352** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Replay Timer** 

Much like the AckNak Latency Timer calculation, L0s recovery time is consid‐ ered differently for the Replay Timer in newer spec versions. In the 1.x specs, an argument is included in the Replay Timer equation to account for this, but the tables in the spec based on that equation put its value at zero and call the result‐ ing values ‘unadjusted’. Beginning with the 2.0 spec, the argument is dropped from the equation altogether and the text states that the transmitter should com‐ pensate for L0s exit if it will be used, either by statically adding that time to the table values or by sensing when the Link is in that state and allowing extra time in that case. The table values still don’t contain an L0s component and are still called ‘unadjusted’. 

As a final word on this topic, the spec strongly recommends that a transmitter should not do a replay on a Replay Timer timeout if it’s possible that the delay in receiving an Ack was caused by the other device’s transmitter being in the L0s state. 

Note that, just like for the Ack Latency Timer tables, the tolerance for all of the table values is ‐0% to +100%. To illustrate this, Table 10‐6 on page 353 lists the time for a x1 Link and Max Payload size of 128 Bytes as 711 symbol times. Legal values would therefore range from no less than 711 symbol times to no more than 1422. 

## **2.5 GT/s Operation** 

_Table 10‐6: Gen1 Unadjusted REPLAY_TIMER Values in Symbol Times_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|711|384|219|201|174|144|99|
|256 Bytes|1248|651|354|321|270|216|135|
|512 Bytes|1677|867|462|258|327|258|156|
|1024 Bytes|3213|1635|846|450|582|450|252|
|2048 Bytes|6285|3171|1614|834|1095|834|444|
|4096 Bytes|12429|6243|3150|1602|2118|1602|828|



**353** 

**PCI Ex ress Technolo p gy** 

## **5.0 GT/s Operation** 

_Table 10‐7: Gen2 Unadjusted REPLAY_TIMER Values in Symbol Times_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|864|537|372|354|327|297|252|
|256 Bytes|1401|804|507|474|423|369|288|
|512 Bytes|1830|1020|615|411|480|411|309|
|1024 Bytes|3366|1788|999|603|735|603|405|
|2048 Bytes|6438|3324|1767|987|1248|987|597|
|4096 Bytes|12582|6396|3303|1755|2271|1755|981|



## **8.0 GT/s Operation** 

_Table 10‐8: Gen3 Unadjusted REPLAY_TIMER Values_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|999|672|507|489|462|432|387|
|256 Bytes|1536|939|642|609|558|504|423|
|512 Bytes|1965|1155|750|546|615|546|444|
|1024 Bytes|3501|1923|1134|738|870|738|540|
|2048 Bytes|6573|3459|1902|1122|1383|1122|732|
|4096 Bytes|12717|6531|3438|1890|2406|1890|1116|



## **Switch Cut-Through Mode** 
