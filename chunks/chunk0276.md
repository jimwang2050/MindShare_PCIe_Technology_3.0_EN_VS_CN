Block Alignment Block Type<br>& Block Type  Control<br>Detect Logic Sym bols<br>De-Serializing Lane<br>Register Elastic De-skew<br>Buffer Delay<br>8 8 Circuit<br>Control Local<br>Serial<br>Clock<br>Stream<br>PLL<br>Rx<br>D+<br>Clock<br>Rx Clock<br>Differential<br>Recovery<br>D- Receiver Rx Clock / 8.125<br>Serial Bit PLL<br>Stream<br>a     b     c     d     e     f     g     ha<br>**----- End of picture text -----**<br>


## **CDR (Clock and Data Recovery) Logic** 

## **Rx Clock Recovery** 

Although the new scrambling scheme helps with clock recovery, it doesn’t guar‐ antee good transition density over short intervals. As a result, the CDR logic must now be able to maintain synchronization for longer periods without as many edges. No specific method for accomplishing this is given in the spec, but a more robust PLL (Phase‐Locked Loop) or DLL (Delay‐Locked Loop) circuit will likely be needed. 

Another aspect of the CDR logic that’s different now is that the internal clock used by the Elastic Buffer is not simply the Rx clock divided by 8 as one might expect. The reason, of course, is that the input is not a regular multiple of 8‐bit bytes. Instead, it is a 2‐bit Sync Header followed by 16 bytes. Those extra two bits must be accounted for somewhere. The spec doesn’t require any particular implementation, but one solution would have the clock divided by 8.125, as shown in Figure 12‐19 on page 437, to produce 16 clock edges over 130 bit times. 

**437** 

**PCI Ex ress Technolo p gy** 

The Block Type Detection logic might then be used to take the extra two bits out of the deserializer that it needs to examine anyway, when a block boundary time is reached, ensuring that only 8‐bit bytes are delivered to the Elastic Buffer. 

Just to tie up all the loose ends on this discussion, the internal clock for the 8.0 GT/s data rate will actually be 8.0 GHz / 8.125 = 0.985 GHz. That results in slightly less than the 1.0 GB/s data rate that’s usually used to describe the Gen3 bandwidth, but the difference is small enough (1.5% less than 1 GB/s) that it usually isn’t mentioned. 

## **Deserializer** 

The incoming data is clocked into each Lane’s serial‐to‐parallel converter by the recovered Rx clock, as shown in Figure 12‐19 on page 437. The 8‐bit Symbols are sent to the Elastic Buffer and clocked into the Elastic Buffer by a version of the Rx Clock that has been divided by 8.125 to properly accommodate 16 bytes in 130 bits. 

## **Achieving Block Alignment** 

The EIEOSs sent during training serve to identify boundaries for the 130‐bit blocks. As shown in Figure 12‐20 on page 438, this Ordered Set can be recog‐ nized in a bit stream because it appears as a pattern of alternating bytes of 00h and FFh. When this pattern is seen, the last Symbol of the EIEOS is interpreted as the Block boundary, and testing the next 130 bits will reveal whether the boundary is correct. If not, the logic continues to search for this pattern. This process is described in the spec as occurring in three phases: Unaligned, Aligned, and Locked. 

_Figure 12‐20: EIEOS Symbol Pattern_ 

**==> picture [75 x 137] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


**438** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

**Unaligned Phase.** Receivers enter this phase after a period of Electrical Idle, such as after changing to 8.0 GT/s or exiting from a low‐power Link state. In this phase, the Block Alignment logic watches for the arrival of an EIEOS, since the end of the alternating bytes must correspond to the end of the Block. When an EIEOS is seen, the alignment is adjusted and the logic proceeds to the next phase. Until then, it must also adjust its Block align‐ ment based on the arrival of any SOS. 

**Aligned Phase.** In this phase Receivers continues to monitor for EIEOS and make any necessary adjustments to their bit and Block alignment if they see one. However, since they’ve tentatively identified block boundaries they can also now search for an SDS (Start of Data Stream) Ordered Set to indicate the beginning of a Data Stream. When an SDS is seen, the receiver proceeds to the Locked phase. Until then, it must also adjust its Block align‐ ment based on the arrival of SOSs. If an undefined Sync Header is detected (value of 00b or 11b) the Receiver is allowed to return to the Unaligned phase. The spec notes that this will happen during Link training when EIEOS is followed by a TS Ordered Set. 

**Locked Phase.** Once a Receiver reaches this phase, it no longer adjusts its Block alignment. Instead, it now expects to see a Data Block after the SDS and if the alignment has to be readjusted at this point, some misaligned data will probably be lost. If an undefined Sync Header is detected the Receiver is allowed to return to the Unaligned or Aligned phase. Receivers can be directed to transition out of the Locked phase to one of the others as long as Data Stream processing is stopped (see “Data Stream and Data Blocks” on page 413 for the rules regarding Data Streams). 

**Special Case: Loopback.** While discussing Block alignment, the spec describes what happens when the Link is in Loopback mode. The Loopback Master must be able to adjust alignment during Loopback, and is allowed to send EIEOS and adjust its Receiver based on a detected EIEOS when they are echoed back during Loopback.Active. The Loopback Slave must be able to adjust alignment during Loopback.Entry but must not adjust alignment during Loopback.Active. The Slave’s Receiver is considered to be in the Locked phase when the Slave begins to loop back the bit stream. 

## **Block Type Detection** 

Once Block Alignment has been achieved, the Receiver can recognize the start times of the incoming blocks and examine the first two bits to identify which of the two possible types are coming in. Ordered Set Blocks are only interesting to the Physical Layer, so they’re not forwarded to the higher layers, but Data 

**439** 

**PCI Ex ress Technolo p gy** 

Blocks do get forwarded. When the Sync Header is detected, this information is signaled to other parts of the Physical Layer to determine whether the current block should be removed from the byte stream going to the higher layers. The clock recovery mechanism and Sync Header detection effectively accomplishes the conversion from 130 bits to 128 bits that must take place in the Physical Layer. 

Note that since the block information is the same for every Lane, this logic may simply be implemented for only one Lane, such as Lane 0 as shown in Figure 12‐18 on page 436. However, if different Link widths and Lane Reversal were supported then more Lanes would need to include this logic to ensure that there would always be one active Lane with this logic available. An example might be that every Lane which is able to operate as Lane 0 would implement it, but only the one that was currently acting as Lane 0 would use it. Note also that, since the spec doesn’t give details in this regard, the examples discussed and illus‐ trated here are only educated guesses at a workable implementation. 

## **Receiver Clock Compensation Logic** 

## **Background** 

The clock requirements for 8.0 GT/s are the same as they were in the earlier spec versions: the clocks of both Link partners must be within +/– 300 ppm (parts per million) of the center frequency, which results (in the worst case) in gaining or losing one clock after every 1666 clocks. 

## **Elastic Buffer’s Role** 

The received Symbols are clocked into the elastic buffer, as shown in Figure 12‐ 21 on page 441, using the recovered clock and clocked out using the receiver’s local clock. The Elastic Buffer compensates for the frequency difference by add‐ ing or removing SKP Symbols as before, but now it does so four Symbols at a time instead of only one at a time. When a SKP Ordered Set arrives, control logic watching the status of the buffer makes an evaluation. If the local clock is running faster, the buffer will be approaching an underflow condition and the logic can compensate by appending four extra SKPs when the SOS arrives to quickly refill the buffer. On the other hand, if the recovered clock is running faster, the buffer will be approaching an overflow condition and the logic will compensate for that by deleting four SKPs to quickly drain the buffer when an SOS is seen. 

**440** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐21: Gen3 Elastic Buffer Logic_ 

**==> picture [383 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
Block Alignment Block Type<br>& Block Type  Control<br>Detect Logic Sym bols<br>De-Serializing Lane<br>Register Elastic De-skew<br>Buffer Delay<br>8 8 Circuit<br>Control Local<br>Serial<br>Clock<br>Stream<br>PLL<br>Rx<br>D+<br>Clock<br>Rx Clock<br>Differential<br>Recovery<br>D- Receiver Rx Clock / 8.125<br>Serial Bit PLL<br>Stream<br>a     b     c     d     e     f     g     ha<br>**----- End of picture text -----**<br>


Gen3 Transmitters schedule an SOS once every 370 to 375 blocks but, as before, they can only be sent on block boundaries. If a packet is in progress when SOSs are scheduled, they are accumulated and inserted at the next packet boundary. However, unlike the lower data rates, two consecutive SOSs are not allowed at 8.0 GT/s; they must be separated by a Data Block. Receivers must be able to tol‐ erate SOSs separated by the maximum packet payload size a device supports. 

The fact that adjustments are only made in increments of 4 Symbols may affect the depth of the Elastic Buffer, since a difference of 4 would need to be seen before any compensation is applied, and a large packet may be in progress at what would otherwise be the appropriate time. For that reason, care will need to be exercised in determining the optimal size of this buffer, so let’s consider an example. The allowed time between SOSs of 375 blocks at 16 Symbols per block equals 6000 Symbol times. Dividing that by the worst‐case time to gain or lose a clock of 1666 means that 3.6 clocks could be gained or lost during that period. If the largest possible TLP (4KB) had started just prior to the next SOS being sent, the overall delay for it becomes about 6000 + 4096 = 10096 Symbol times for a x1 Link, which translates to a gain or loss of 10096 / 1666 = 6.06 clocks. Conse‐ 

**441** 

**PCI Ex ress Technolo p gy** 

quently, if TLPs of 4KB in size are supported, the buffer might be designed to handle 7 Symbols too many or too few before an SOS is guaranteed to arrive. It may happen that two SOSs are scheduled before the first one is sent. At the lower data rates, the queued SOSs are sent back‐to‐back, but for 8.0 GT/s they are not and must be separated by a Data Block. Whenever an SOS does arrive at the Receiver, it can add or remove 4 SKP Symbols to quickly fill or drain the buffer and avoid a problem. 

## **Lane-to-Lane Skew** 

## **Flight Time Variance Between Lanes** 
