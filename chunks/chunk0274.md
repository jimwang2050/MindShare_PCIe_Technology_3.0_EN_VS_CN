|**Symbol 0**<br>**Sync**<br>**Symbol 1**<br>**Symbol 2**<br>**Symbol 3**<br>**Symbol 4**<br>**Symbol 5**<br>**Symbol 6**<br>**Symbol 7**|**Lane 0**<br>**Lane 1**<br>**Lane 2**<br>**Lane 3**||||IDL<br>IDL<br>IDL<br>IDL<br>Data DW 17<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>Data DW 15<br>Hea3er DW 3<br>Header DW 1<br>SDP Token<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>DW 21<br>DW 19<br>DW 3<br>DW 1<br>**TLP**<br>**straddles**<br>**Block**<br>**boundary**<br>**Lane 4**<br>**Lane 5**<br>**Lane 6**<br>**Lane 7**<br>**Logical**<br>**Idle**<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL||||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
||STP Token: Length=7, CRC, Parity, Seq Num||||||||
||||TLP||||||
||||||||||
||**LCRC**||||SDP Token||||
|||DLLP|||IDL|IDL|IDL|IDL|
||IDL|IDL|IDL|IDL|IDL|IDL|IDL|IDL|
||STP Token: Length=23, CRC, Parity, Seq Num|||||Header DW 1<br>DW 1|||
|||Header DW 2<br>DW 2||||Hea3er DW 3<br>DW 3|||
|**Symbol 15**<br>**Sync**<br>**Symbol 0**<br>**Symbol 1**||Data DW 14<br>DW 18||||Data DW 15<br>DW 19|||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
|||Data DW 16<br>DW 20||||Data DW 17<br>DW 21|||
||**LCRC**||||IDL|IDL|IDL|IDL|
||||||||||
||||||||||



Next a DLLP is sent beginning with the SDP Token on Lanes 4 and 5. Since a DLLP is always 8 Symbols long, it will finish in Lane 3 of Symbol 4. Momen‐ tarily, there are no other packets to send, so IDL Symbols are transferred until another packet is ready. When IDLs are sent, the next STP Token can only start in Lane 0. In the example, the TLP starts in Lane 0 of Symbol 6. 

The packet length for the next TLP is 23 DW and that presents an interesting sit‐ uation because there are only 20 dwords available before the next Block bound‐ ary. When the Data Block ends the transmitter sends Sync and continues TLP transmission during Symbol 0 of the next Block. In other words, Packets simply straddle Block boundaries when necessary. Finally, the TLP finishes in Lane 3 of Symbol 1. Once again there are no packets ready to send, so IDLs are sent. 

## **Nullified Packet x8 Example** 

Nullified TLPs can occur when a TLP is being transferred across a switch to reduce latency. This is called Switch Cut‐Through operation. The reader may choose to review the section entitled “Switch Cut‐Through Mode” on page 354 before proceeding with this discussion. 

**425** 

## **PCI Ex ress Technolo p gy** 

A nullified TLP can occur when a switch forwards a packet to the egress port before having received the packet at the ingress port and before error checking. Because an error was detected in this example, the TLP must be nullified. 

Figure 12‐13 illustrates the steps taken to nullify TLP. The TLP being sent by the egress port, starts in the first block (Lane 0 of Symbol 6). When the error is detected, the egress port inverts the CRC (Lanes 0‐3 of Symbol 1) and adds an EDB token immediately following the TLP (Lanes 4‐7 of symbol 1). Together, those two changes make it clear to the Receiver that this TLP has been nullified and should be discarded. Note that the EDB bytes are not included in the packet length field, because they dynamically added to a packet in flight when an error occurs. 

_Figure 12‐13: Gen3 x8 Nullified Packet_ 

||||||||||
|---|---|---|---|---|---|---|---|---|
|**Symbol 0**<br>**Sync**<br>**Symbol 1**<br>**Symbol 2**<br>**Symbol 3**<br>**Symbol 4**<br>**Symbol 5**<br>**Symbol 6**<br>**Symbol 7**|**Lane 0**<br>**Lane 1**<br>**Lane 2**<br>**Lane 3**||||EDB<br>EDB<br>EDB<br>EDB<br>Data DW 17<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>Data DW 15<br>Hea3er DW 3<br>Header DW 1<br>SDP Token<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>**0**<br>**1**<br>DW 21<br>DW 19<br>DW 3<br>DW 1<br>**TLP**<br>**straddles**<br>**Block**<br>**boundary**<br>**Lane 4**<br>**Lane 5**<br>**Lane 6**<br>**Lane 7**<br>**Logical**<br>**Idle**<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>IDL<br>**Nullified  TLP**||||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
||STP Token: Length=7, CRC, Parity, Seq Num||||||||
||||TLP||||||
||||||||||
||**LCRC**||||SDP Token||||
|||DLLP|||IDL|IDL|IDL|IDL|
||IDL|IDL|IDL|IDL|IDL|IDL|IDL|IDL|
||STP Token: Length=23, CRC, Parity, Seq Num|||||Header DW 1<br>DW 1|||
|||Header DW 2<br>DW 2||||Hea3er DW 3<br>DW 3|||
|**Symbol 15**<br>**Sync**<br>**Symbol 0**<br>**Symbol 1**||Data DW 14<br>DW 18||||Data DW 15<br>DW 19|||
||**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|**0**<br>**1**|
|||Data DW 16<br>DW 20||||Data DW 17<br>DW 21|||
||LCRC (inverted)||||EDB|EDB|EDB|EDB|
||||||||||
||||||||||



## **Ordered Set Example - SOS** 

Now let’s consider an example of Ordered Set transmission. As shown in Figure 12‐14 on page 427, an Ordered Set is indicated by the 2‐bit Sync Header value of 01b. The bytes that follow will be understood by the receiver to make up an Ordered Set that is always 16 bytes (128 bits) in length. The one exception is the 

**426** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

SOS (Skip Ordered Set), because it can be changed by intermediate receivers in increments of 4 bytes at a time for clock compensation. Consequently, an SOS is legally allowed to be 8, 12, 16, 20, or 24 Symbols in length. In the absence of a Link repeater device that does not add or delete SKPs in a SOS, a SOS will also be made up of 16 bytes. 

_Figure 12‐14: Gen3 x1 Ordered Set Construction_ 

**==> picture [376 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 1 Symbol 15<br>(10)<br>128-bit Payload<br>Ordered Set Block<br>0 2UI 10UI 122UI<br>= = = =<br>Time Time Time Time<br>**----- End of picture text -----**<br>


To illustrate an Ordered Set, let’s use an SOS to show the various features and how they work together. Consider Figure 12‐15 on page 428, where a Data Block is followed by an SOS. The framing rules state that the previous Data Block must end with an EDS Token in the last dword to let the receiver know that an Ordered Set is coming. If the current Data Stream is to continue, the Ordered Set that follows must be an SOS, and that must be followed in turn by another Data Block. This example doesn’t show it, but it’s possible that a TLP might be incom‐ plete at this point and would straddle the SOS by resuming transmission in the Data Block that must immediately follow the SOS. 

Receiving the EDS Token means that the Data Stream is either ending or paus‐ ing to insert an SOS. An EDS is the only Token that can start on a dword‐ aligned Lane in the same Symbol Time as an IDL, and this example does just that, beginning in Lane 4 of Symbol Time 15. Recall that EDS must also be in the last dword of the Data Block. According to the receiver framing requirements, only an Ordered Set Block is allowed after an EDS and must be an SOS, EIOS, or EIEOS or else it will be seen as a framing error. As was true for earlier spec ver‐ sions, the Ordered Sets must appear on all Lanes at the same time. Receivers may optionally check to ensure that each Lane sees the same Ordered Set. 

In our example, a 16 byte SOS is seen next, and is recognized by the Ordered Set Sych Header as well as the SKP byte pattern. There are always 4 Symbols at the end of the SOS that contain the current 24‐bit scrambler LFSR state. In Symbol 

**427** 

**PCI Ex ress Technolo p gy** 

12 the Receiver knows that the SKP characters have ended and also that the Block has three more bytes to deliver per Lane. These are the output of the scrambling logic LFSR, as shown in Table 12‐2 on page 428. 

_Figure 12‐15: Gen3 x8 Skip Ordered Set (SOS) Example_ 

**==> picture [384 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane 0 Lane 1 Lane 2 Lane 3 Lane 4 Lane 5 Lane 6 Lane 7<br>Data<br>Sync 01 01 01 01 01 01 01 01 Block<br>Symbol 0 STP Token:STP: LengthLength=7,= 7, CRC,CRC,Parity,Parity, Seq NumSeq Num<br>Symbol 1 (TLPTLP7 DW )<br>Symbol 2<br>Symbol 3 LCRC SDP Token<br>Symbol 4 DLLP IDL IDL IDL IDL<br>Symbol 5 IDL IDL IDL IDL IDL IDL IDL IDL End of<br>Symbol 6 SDP Token DLLP Data<br>Stream<br>Symbol 7 IDL IDL IDL IDL IDL IDL IDL IDL<br>Marker<br>Symbol 15 IDL IDL IDL IDL EDS Token Marker(End of Data StreamPacket )<br>Sync 10 10 10 10 10 10 10 10 OrderedSet Block<br>Symbol 0 SKP SKP SKP SKP SKP SKP SKP SKP<br>Symbol 3 SKP SKP SKP SKP SKP SKP SKP SKP End of<br>SOS<br>Symbol 4 SKP_END SKP_END SKP_END SKP_END SKP_END SKP_END SKP_END SKP_END<br>LFSR<br>Symbol 5 LFSR LFSR LFSR LFSR LFSR LFSR LFSR LFSR output<br>Symbol 6 LFSR LFSR LFSR LFSR LFSR LFSR LFSR LFSR as filler<br>Symbol 7 LFSR LFSR LFSR LFSR LFSR LFSR LFSR LFSR<br>Data<br>Sync 01 01 01 01 01 01 01 01 Block<br>**----- End of picture text -----**<br>


_Table 12‐2: Gen3 16‐bit Skip Ordered Set Encoding_ 

|**Symbol**<br>**Number**|**Value**|**Description**|
|---|---|---|
|0 to 11|AAh|SKP Symbol. Since Symbol 0 is the Ordered Set Identifier,<br>this is seen as an SOS.|
|12|E1h|SKP_END Symbol, which indicates that the SOS will be com‐<br>plete after 3 more Symbols|



**428** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Table 12‐2: Gen3 16‐bit Skip Ordered Set Encoding (Continued)_ 

|**Symbol**<br>**Number**|**Value**|**Description**|
|---|---|---|
|13|00‐FFh|a) If LTSSM state is Polling.Compliance: AAh<br>b) Else if prior block was a Data Block:<br>Bit [7] = Data Parity<br>Bit [6:0] = LFSR [22:16]<br>c) Else<br>Bit [7] = ~LFSR [22]<br>Bit [6:0] = LFSR [22:16]|
|14|00‐FFh|a) If LTSSM state is Polling.Compliance: Error_Status [7:0]<br>b) Else LFSR [15:8]|
|15|00‐FFh|a) If LTSSM state is Polling.Compliance: Error_Status [7:0]<br>b) Else LFSR [7:0]|



The Data Parity bit mentioned in the table is the even parity of all the Data Block scrambled bytes that have been sent since the most recent SDS or SOS and is created independently for each Lane. Receivers are required to calculate and check the parity. If the bits don’t match, the Lane Error Status register bit corre‐ sponding to the Lane that saw the error must be set, but this is not considered a Receiver Error and does not initiate Link retraining. 

The 8‐bit Error_Status field only has meaning when the LTSSM is in the Poll‐ ing.Compliance state (see “Polling.Compliance” on page 529 for more details). For our example of an SOS following a Data Block, byte 13 is the Data Parity bit and LFSR[22:16], while the last two bytes are LFSR bits [15:0]. 

## **Transmitter SOS Rules** 

The SOS rules for Transmitters when using 128b/130b include: 

- An SOS must be scheduled to occur within 370 to 375 blocks. In Loopback mode, however, the Loopback Master must schedule two SOS’s within that time, and they must be no more than two blocks from each other. 

- SOS’s can still only be sent on packet boundaries and may be accumulated as a result. However, consecutive SOS’s are not permitted; they must be sep‐ arated by a Data Block. 

- It’s recommended that SOS timers and counters be reset whenever the Transmitter is Electrically Idle. 

**429** 

**PCI Ex ress Technolo p gy** 

- The Compliance SOS bit in Link Control Register 2 has no effect when using 128b/130b. (It’s used to disable SOSs during Compliance testing for 8b/10b, but that isn’t an option for 128b/130b.) 

## **Receiver SOS Rules** 

The Skip Ordered Set rules for Receivers when using 128b/130b include: 

- They must tolerate receiving SOS’s at an average interval of 370‐375 blocks. Note that the first SOS after Electrical Idle may arrive earlier than that, since Transmitters are not required to reset SOS timers during Electrical Idle time. 
