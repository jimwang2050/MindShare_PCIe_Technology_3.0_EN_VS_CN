‘D’ Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>‘D’ Character<br>‘K’ Character ‘K’ Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>‘K’ Character ‘K’ Character<br>**----- End of picture text -----**<br>


## **Byte Striping (for Wide Links)** 

The next step shown in our example is Byte Striping, although this is only needed if the port implements more than one Lane (called a wide Link). Strip‐ ing means that each consecutive outbound character in a character stream is routed onto consecutive Lanes. The number of Lanes used is configured during the Link training process based on what is supported by both devices that share the Link. 

Three examples of byte striping are illustrated in the following diagrams. In Figure 11‐8 on page 372, a single‐lane link (x1) is shown. This is not a very inter‐ esting case, since the packet enters the Physical Layer a byte at a time and goes out the same way, but illustrates the way the sequence of characters will be drawn. 

Figure 11‐9 on page 372 shows the incoming Dword packets from the muti‐ plexer. Each byte is directed to the corresponding lanes. Finally, Figure 11‐10 on page 373 illustrates an eight‐lane (x8) link. In this example, two Dwords are required to populate all 8 lanes. This requires the Dword to arrive at twice the rate as the previous example. The format of the data being sent across each lane is described in the sections that follow. 

**371** 

## **PCI Ex ress Technolo p gy** 

_Figure 11‐8: x1 Byte Striping_ 

**==> picture [154 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- End of picture text -----**<br>


_Figure 11‐9: x4 Byte Striping_ 

**==> picture [338 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- End of picture text -----**<br>


**372** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐10: x8 Byte Striping with DWord Parallel Data_ 

**==> picture [368 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- End of picture text -----**<br>


## **Packet Format Rules** 

## **General Rules** 

- The total packet length (including Start and End characters) of each packet is always a multiple of four characters. This is a natural extension of the fact that the data length is measured in dwords. 

- TLPs start with the STP character and finish with either an END or EDB character. 

- DLLPs start with SDP, terminate with the END character. and are exactly 8 characters long (SDP + 6 characters + END) 

- STP and SDP characters are placed on Lane 0 when starting the transmis‐ sion of a packet after the transmission of Logical Idles. In other cases, they may start on a Lane number divisible by 4. 

- The receiver’s Physical Layer is allowed to watch for violation of these rules and may report them as Receiver Errors to the Data Link Layer. 

**373** 

**PCI Ex ress Technolo p gy** 

## **Example: x1 Format** 

The example shown in Figure 11‐11 on page 374 illustrates the format of packets transmitted over a x1 link (a link with only one lane operational). A sequence of packets is shown interspersed with one SKIP Ordered Set. Logical Idles are shown at the end to represent the case when the transmitter has no more pack‐ ets to send and uses idle characters as filler. 

_Figure 11‐11: x1 Packet Format_ 

**==> picture [351 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- End of picture text -----**<br>


## **x4 Format Rules** 

- STP and SDP characters are always sent on Lane 0. 

- END and EDB characters are always sent on Lane 3. 

- When an ordered set such as the SKIP is sent, it must appear on all lanes simultaneously. 

- When Logical Idles are transmitted, they must be sent on all lanes simulta‐ neously. 

- Any violation of these rules may be reported as a Receiver Error to the Data Link Layer. 

**374** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Example x4 Format** 

The example shown in Figure 11‐12 on page 375 illustrates the format of packets sent over a x4 Link (link with four data lanes operational). The illustration shows one TLP followed by a SKIP ordered set transmitted on all Lanes for receiver clock compensation. Next is a DLLP, followed by Logical Idle on all lanes. This example highlights that the packets are always multiples of 4 charac‐ ters because the start character always appears in lane 0 and the end character is always in lane 3. It also illustrates that ordered sets must appear on all the lanes simultaneously. 

_Figure 11‐12: x4 Packet Format_ 

**375** 

**PCI Ex ress Technolo p gy** 

## **Large Link-Width Packet Format Rules** 

The following rules apply when a packet is transmitted over a x8, x12, x16, or x32 Link: 

- STP/SDP characters are always sent on Lane 0 when transmission starts after a period during which Logical Idles are transmitted. After that, they may only be sent on Lane numbers divisible by 4 when sending back‐to‐ back packets (Lane 4, 8, 12, etc.). 

- END/EDB characters are sent on Lane numbers divisible by 4 and then minus one (Lane 3, 7, 11, etc.). 

- If a packet doesn’t end on the last Lane of the Link and there are no more packets ready to go, PAD Symbols are used as filler on the remaining lane numbers. Logical Idle can’t be used for this purpose because it must appear on all Lanes at the same time. 

- Ordered sets must be sent on all lanes simultaneously. 

- Similarly, logical idles must be sent on all lanes when they are used. 

- Any violation of these rules may be reported as a Receiver Error to the Data Link Layer. 

## **x8 Packet Format Example** 

The example shown in Figure 11‐13 on page 377 illustrates the format of packets transmitted over a x8 link. The illustration shows a TLP followed by a SKIP ordered set, a DLLP, and finally a TLP that ends on Lane 3. At that point, the transmitter has no more packets ready to send but the current packet doesn’t extend to include all the available lanes. One might expect the extra lanes to be filled with Logical Idle, but it won’t work here because idles must appear on all lanes at the same time. So another fill character is needed, and the spec writers chose to use the PAD control character here. The only other place that PAD is used is during the training process. Finally, since there are still no more packets to send, Logical Idles are sent on all the lanes. 

**376** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐13: x8 Packet Format_ 

## **Scrambler** 

The next step in our example is scrambling, as shown in Figure 11‐5 on page 369, which is intended to prevent repetitive patterns in the data stream. Repeti‐ tive patterns create “pure tones” on the link, meaning a consistent frequency caused by the pattern that generates more than the usual noise, or EMI. Reduc‐ ing this problem by spreading this energy over a wider frequency range is the primary goal of scrambling. In addition, though, scrambled transmission on one Lane also reduces interference with adjacent Lanes on a wide Link. This “spatial frequency de‐correlation”, or reduction of crosstalk noise, helps the receiver on each lane to distinguish the desired signal. 

**377** 

## **PCI Ex ress Technolo p gy** 

To help the receiver maintain synchronization with the scrambled sequence, control characters do not get scrambled and are thus recognizable even if the scramblers get out of sync. In addition, the arrival of the COM control character (K28.5) reinitializes the scramblers on both ends of the Link each time it arrives and thus re‐synchronizes them. 

## **Scrambler Algorithm** 

The scrambler described in the spec is shown in Figure 11‐14 on page 378. It’s made of a 16‐bit Linear Feedback Shift Register (LFSR) with feedback points that implement the following polynomial: 

G(x) = X[16] + X[5] + X[4] + X[3 ] +1 

_Figure 11‐14: Scrambler_ 

The LFSR is clocked at 8 times the frequency of the clock feeding the data bytes, and its output is clocked into an 8‐bit register that is XORed with the 8‐bit data characters to form the scrambled data output. 

**378** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Some Scrambler implementation rules:** 

- On a multi‐Lane Link implementation, Scramblers associated with each Lane must operate in concert, maintaining the same simultaneous value in each LFSR. 

- Scrambling is applied to ‘D’ characters only, meaning those associated with TLP and DLLPs and the Logical Idle (00h) characters. However, those ‘D’ characters that are within the TS1 and TS2 ordered sets are not scrambled. 

- Scrambling is never applied to ‘K’ characters and characters within ordered sets, such as TS1, TS2, SKIP, FTS and Electrical Idle. These characters bypass the scrambler logic. One reason for this is to ensure they’ll still be recogniz‐ able by the receiver even if the scramblers somehow get out of sequence. 

- Compliance Pattern characters (used for testing) are also not scrambled. 

- • The COM character, a control character that does not get scrambled, is used to reinitialize the LFSR to FFFFh at both the transmitter and receiver. 

- Except for the COM character, the LFSR normally will serially advance eight times for every D or K character sent, but it does not advance on SKP characters associated with the SKIP ordered set. The reason is that a receiver may add or delete SKP Symbols to perform clock tolerance com‐ pensation. Changing the number of characters in the receiver compared to the number that were sent would cause the value in the receiver LFSR to lose synchronization with the transmitter LFSR value if they were not ignored. 

## **Disabling Scrambling** 

Scrambling is enabled by default, but the spec allows it to be disabled for test and debug purposes. That’s because testing may require control of the exact bit pattern sent and, since the hardware handles scrambling, there’s no reasonable way for the software to be able to force a specific pattern. No specific software mechanism is defined by which to instruct the Physical Layer to disable scram‐ bling, so this has to be a design‐specific implementation. 
