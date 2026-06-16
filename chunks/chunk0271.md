There are several Link power states that allow power savings under certain con‐ ditions. These are L0s, L1, L2, and L3, which represent progressively lower power and also longer recovery time to get the link back to the fully‐operation state of L0. The L0s state can only be entered under hardware control, while L1 can be initiated by hardware or software. Since L0s and L1 can be controlled by hardware, they are referred to by the spec as ASPM (Active State Power Man‐ agement) states. For more on the details of link and device power management see the section “Active State Power Management (ASPM)” on page 735. 

## **Link Training and Initialization** 

As we’ve just briefly mentioned in this chapter, the Physical Layer is also responsible for initializing the link after a reset. However, this topic is too big to cover here and is instead covered in Chapter 14, entitled ʺLink Initialization & Training,ʺ on page 505. 

**405** 

**PCI Ex ress Technolo p gy** 

**406** 

## _**12**_ 

## _**Physical Layer ‐ Logical (Gen3)**_ 

## **The Previous Chapter** 

The previous chapter describes the Gen1/Gen2 logical sub‐block of the Physical Layer. This layer prepares packets for serial transmission and recovery, and the several steps needed to accomplish this are described in detail. The chapter cov‐ ers logic associated with the Gen1 and Gen2 protocol that use 8b/10b encoding/ decoding. 

## **This Chapter** 

This chapter describes the logical Physical Layer characteristics for the third generation (Gen3) of PCIe. The major change includes the ability to double the bandwidth relative to Gen2 speed without needing to double the frequency (Link speed goes from 5 GT/s to 8 GT/s). This is accomplished by eliminating 8b/10b encoding when in Gen3 mode. More robust signal compensation is nec‐ essary at Gen3 speed. 

## **The Next Chapter** 

The next chapter describes the Physical Layer electrical interface to the Link. The need for signal equalization and the methods used to accomplish it are also discussed here. This chapter combines electrical transmitter and receiver char‐ acteristics for both Gen1, Gen2 and Gen3 speeds. 

## **Introduction to Gen3** 

Recall that when a PCIe Link enters training (i.e., after a reset) it always begins using Gen1 speed for backward compatibility. If higher speeds were advertised during the training, the Link will immediately transition to the Recovery state and attempt to change to the highest commonly‐supported speed. 

**407** 

## **PCI Ex ress Technolo p gy** 

The major motivation for upgrading the PCIe spec to Gen3 was to double the bandwidth, as shown in Table 12‐1 on page 408. The straightforward way to accomplish this would have been to simply double the signal frequency from 5 GT/s to 10 Gb/s, but doing that presented several problems: 

- Higher frequencies consume substantially more power, a condition exacer‐ bated by the need for sophisticated conditioning logic (equalization) to maintain signal integrity at the higher speeds. In fact, the power demand of this equalizing logic is mentioned in PCISIG literature as a big motivation for keeping the frequency as low as practical. 

- Some circuit board materials experience significant signal degradation at higher frequencies. This problem can be overcome with better materials and more design effort, but those add cost and development time. Since PCIe is intended to serve a wide variety of systems, the goal was that it should work well in inexpensive designs, too. 

- Similarly, allowing new designs to use the existing infrastructure (circuit boards and connectors, for example) minimizes board design effort and cost. Using higher frequencies makes that more difficult because trace lengths and other parameters must be adjusted to account for the new tim‐ ing, and that makes high frequencies less desirable. 

_Table 12‐1: PCI Express Aggregate Bandwidth for Various Link Widths_ 

|**Link Width**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 Bandwidth**<br>**(GB /s)**|0.5|1|2|4|6|8|16|
|**Gen2 Bandwidth**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 Bandwidth**<br>**(GB/s)**|2|4|8|16|24|32|64|



These considerations led to two significant changes to the Gen3 spec compared with the previous generations: a new encoding model and a more sophisticated signal equalization model. 

**408** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **New Encoding Model** 

The logical part of the Physical Layer replaced the 8b/10b encoding with a new 128b/130b encoding scheme. Of course, this meant departing from the well‐ understood 8b/10b model used in many serial designs. Designers were willing to take this step to recover the 20% transmission overhead imposed by the 8b/ 10b encoding. Using 128b/130b means the Lanes are now delivering 8 bits/byte instead of 10 bits, and that means an 8.0 GT/s data rate that doubles the band‐ width. This equates to a bandwidth of 1 GB/s in each direction. 

To illustrate the difference between these two encodings, first consider Figure 12‐1 that shows the general 8b/10b packet construction. The arrows highlight the Control (K) characters representing the framing Symbols for the 8b/10b packets. Receivers know what to expect by recognizing these control characters. See “8b/10b Encoding” on page 380 to review the benefits of this encoding scheme. 

_Figure 12‐1: 8b/10b Lane Encoding_ 

**==> picture [344 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
‘D’ Characters<br>STP Sequence Header Data Payload  ECRC LCRC END<br>‘D’ Characters<br>‘K’ Character ‘K’ Character<br>SDP DLLP Type Misc. CRC END<br>‘K’ Character ‘K’ Character<br>**----- End of picture text -----**<br>


By comparison, Figure 12‐2 on page 410 shows the 128b/130b encoding. This encoding does not affect bytes being transferred, instead the characters are grouped into blocks of 16 bytes with a 2‐bit Sync field at the beginning of each block. The 2‐bit Sync field specifies whether the block includes Data (10b) or Ordered Sets (01b). Consequently, the Sync field indicates to the receiver what kind of traffic to expect and when it will begin. Ordered sets are similar to the 8b/10b version in that they must be driven on all the Lanes simultaneously. That requires getting the Lanes properly synchronized and this is part of the training process (see “Achieving Block Alignment” on page 438). 

**409** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐2: 128b/130b Block Encoding_ 

**==> picture [354 x 50] intentionally omitted <==**

**----- Start of picture text -----**<br>
0    1 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7 0    1     2     3      4    5     6    7<br>Sync  Symbol 0 Symbol 1 Symbol 15<br>Field<br>**----- End of picture text -----**<br>


## **Sophisticated Signal Equalization** 

The second change is made to the electrical sub‐block of the Physical Layer and involves more sophisticated signal equalization both at the transmit side of the Link and optionally at the receiver. Gen1 and Gen2 implementations use a fixed Tx de‐emphasis to achieve good signal quality. However, increasing transmis‐ sion frequencies beyond 5 GT/s causes signal integrity problems to become more pronounced, requiring more transmitter and receiver compensation. This can be managed somewhat at the board level but the designers wanted to allow the external infrastructure to remain the same as much as possible, and instead placed the burden on the PHY transmitter and receiver circuits. For more details on signal conditioning, refer to “Solution for 8.0 GT/s ‐ Transmitter Equalization” on page 474. 

## **Encoding for 8.0 GT/s** 

As previously discussed, the Gen3 128b/130b encoding method uses Link‐wide packets and per‐Lane block encoding. This section provides additional details regarding the encoding. 

## **Lane-Level Encoding** 

To illustrate the use of Blocks, consider Figure 12‐3 on page 411, where a single‐ Lane Data Block is shown. At the beginning are the two Sync Header bits fol‐ lower by 16 bytes (128 bits) of information resulting in 130 transmitted bits. The Sync Header simply defines whether a Data block (10b) or an Ordered Set (01b) is being sent. You may have noticed the Data Block in Figure 12‐3 has a Sync Header value of 01 rather than the 10b value mentioned above. This is because the least significant bit of the Sync Header is sent first when transmitting the block across the link. Notice the symbols following the Sync Header are also sent with the least significant bit first. 

**410** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐3: Sync Header Data Block Example_ 

**==> picture [374 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 1 Symbol 15<br>(01)<br>128-bit Payload<br>Data Block<br>UI UI UI<br>0 2 10 122<br>= = = =<br>Time Time Time Time<br>**----- End of picture text -----**<br>


## **Block Alignment** 

Like previous implementations, Gen3 achieves Bit Lock first and then attempts to establish Block Alignment locking. This requires receivers to find the Sync Header that demarcates the Block boundary. Transmitters establish this bound‐ ary by sending recognizable EIEOS patterns consisting of alternating bytes of 00h and FFh, as shown in Figure 12‐4. Thus, the use of EIEOS has expanded from simply exiting Electrical Idle to also serving as the synchronizing mecha‐ nism that establishes Block Alignment. Note that the Sync Header bits immedi‐ ately precede and follow the EIEOS (not shown in the illustration). See “Achieving Block Alignment” on page 438 for details regarding this process. 

_Figure 12‐4: Gen3 Mode EIEOS Symbol Pattern_ 

**==> picture [89 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


**411** 

**PCI Ex ress Technolo p gy** 

## **Ordered Set Blocks** 

Ordered Sets have much the same meaning they did in Gen1 and Gen2. They are used to manage Lane protocol. When an Ordered Set Block is sent it must appear on all the Lanes at the same time and almost always consists of 16 bytes with one exception. The one exception to this size rule is the SOS (SKP Ordered Set) which can have SKP Symbols added or removed in groups of four by clock compensation logic (associated with a Link Repeater for example) and can therefore legally be 8, 12, 16, 20, or 24 bytes long. 

The basic format of the Ordered Set Block is similar to the Data Block, except that the Sync Header bits are reversed, as shown in Figure 12‐5 on page 412. 

_Figure 12‐5: Gen3 x1 Ordered Set Block Example_ 

**==> picture [347 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 0 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 1 Symbol 15<br>(10)<br>128-bit Payload<br>Ordered Set Block<br>UI UI UI<br>0 2 10 122<br>= = = =<br>Time Time Time Time<br>**----- End of picture text -----**<br>


The spec defines seven Ordered Sets for Gen3 (one additional Ordered Set over Gen1 and Gen2 PCIe). In most cases, their functionality is the same as it was for the previous generations. 

1. SOS ‐ Skip Ordered Set: used for clock compensation. See “Ordered Set Example ‐ SOS” on page 426 for more detail. 

2. EIOS ‐ Electrical Idle Ordered Set: used to enter Electrical Idle state 

3. EIEOS ‐ Electrical Idle Exit Ordered Set: used for two purposes now: — Electrical Idle Exit as before 

   - Block alignment indicator for 8.0 GT/s 

4. TS1 ‐ Training Sequence 1 Ordered Set 

5. TS2 ‐ Training Sequence 2 Ordered Set 

6. FTS ‐ Fast Training Sequence Ordered Set 

7. SDS ‐ Start of Data Stream Ordered Set: new ‐ see “Data Stream and Data Blocks” on page 413 for more 

**412** 
