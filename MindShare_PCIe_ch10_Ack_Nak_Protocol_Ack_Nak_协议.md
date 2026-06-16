# 📘 第 10 章　Ack/Nak 协议 (Chapter 10. Ack/Nak Protocol)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0271.md` ... `chunks/chunk0277.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Ack/Nak Protocol](#-本章目录-table-of-contents)

<a id="sec-10-1"></a>
## 10.1 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-2"></a>
## 10.2 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Chapter 12: Physical Layer - Logical (Gen3)** 

To give the reader an example of the Ordered Set structure, Figure 12‐6 shows the content of an FTS Ordered Set when running at 8.0 GT/s. An Ordered Set Block is only recognized as an Ordered Set by the Sync Header, and identified as an FTS type by the first Symbol in the Block. The right‐hand side of the figure lists the Ordered Set Identifiers (the first Symbol for each Ordered Set) that serve to identify the type of Ordered Set is being transmitted. 

_Figure 12‐6: Gen3 FTS Ordered Set Example_ 

|**8Bh**<br>**14**<br>**8Dh**<br>**13**<br>**80h**<br>**12**<br>**7Fh**<br>**11**<br>**88h**<br>**10**<br>**ECh**<br>**9**<br>**6Eh**<br>**8**<br>**25h**<br>**7**<br>**C9h**<br>**6**<br>**C6h**<br>**5**<br>**CCh**<br>**4**<br>**C7h**<br>**3**<br>**4Eh**<br>**2**<br>**8Eh**<br>**15**<br>**47h**<br>**1**<br>**55h**<br>**0**<br>**01b**<br>**Sync Header**<br>**Value**<br>**Symbol**<br>**FTS Ordered Set**|**8Bh**<br>**14**<br>**8Dh**<br>**13**<br>**80h**<br>**12**<br>**7Fh**<br>**11**<br>**88h**<br>**10**<br>**ECh**<br>**9**<br>**6Eh**<br>**8**<br>**25h**<br>**7**<br>**C9h**<br>**6**<br>**C6h**<br>**5**<br>**CCh**<br>**4**<br>**C7h**<br>**3**<br>**4Eh**<br>**2**<br>**8Eh**<br>**15**<br>**47h**<br>**1**<br>**55h**<br>**0**<br>**01b**<br>**Sync Header**<br>**Value**<br>**Symbol**<br>**FTS Ordered Set**|**AAh**<br>**SKP**<br>**2Dh**<br>**TS2**<br>**1Eh**<br>**TS1**<br>**E1**<br>**SDS**<br>**55h**<br>**FTS**<br>**66h**<br>**EIOS**<br>**00h**<br>**EIEOS**<br>**First Symbol**<br>**Ordered Set**<br>**Ordered Set Identifiers**|**AAh**<br>**SKP**<br>**2Dh**<br>**TS2**<br>**1Eh**<br>**TS1**<br>**E1**<br>**SDS**<br>**55h**<br>**FTS**<br>**66h**<br>**EIOS**<br>**00h**<br>**EIEOS**<br>**First Symbol**<br>**Ordered Set**<br>**Ordered Set Identifiers**|
|---|---|---|---|
|**Symbol**|**Value**|**Ordered Set**|**First Symbol**|
|**Sync Header**|**01b**|**EIEOS**|**00h**|
|**0**|**55h**|**EIOS**|**66h**|
|**1**|**47h**|**FTS**|**55h**|
|**2**|**4Eh**|**SDS**|**E1**|
|**3**|**C7h**|**TS1**|**1Eh**|
|**4**|**CCh**|**TS2**|**2Dh**|
|**5**|**C6h**|**SKP**|**AAh**|
|**6**|**C9h**|||
|**7**|**25h**|||
|**8**|**6Eh**|||
|**9**|**ECh**|||
|**10**|**88h**|||
|**11**|**7Fh**|||
|**12**|**80h**|||
|**13**|**8Dh**|||
|**14**|**8Bh**|||
|**15**|**8Eh**|||



## **Data Stream and Data Blocks** 

The Link enters a Data Stream by sending an SDS Ordered Set and transitioning to the L0 Link state. While in a Data Stream multiple Data Blocks are trans‐ ferred, until the Data Stream ends with an EDS Token (unless an error ends it early). An EDS Token always occupies the last four Symbols of the Data Block that precedes an Ordered Set. An exception is made for Skip Ordered Sets because they do not interrupt a Data Stream as long as certain conditions are 

**413** 

**PCI Ex ress Technolo p gy** 

met that are discussed later. A Data Stream is no longer in effect when the Link state transitions out of the L0 state to any other Link state, such as Recovery. For more on Link states, see “Link Training and Status State Machine (LTSSM)” on page 518. 

## **Data Block Frame Construction** 

Data Blocks comprise TLPs, DLLP, and Tokens that are used to deliver the infor‐ mation. Five types of Data structures (called Tokens) are also used within a Data Block. Each has patterns for easy detection by the receiver. Three of the token may be sent at the beginning of a block (i.e., immediately following a Sync Data Block). These include: 

- Start TLP (STP) — followed by a TLP 

- Start DLLP (SDP) — followed by a DLLP 

- Logical Idle (IDLA) — sent when there is no packet activity 

The remaining Tokens are delivered at the end of the Data Block: 

- End of Data Stream (EDS) — Precedes the transition to Ordered Sets 

- End Bad (EDB) — reports a nullified packet has been detected 

Figure 12‐7 provides an example of a Data Block consisting of a single lane TLP transmission. 

_Figure 12‐7: Gen3 x1 Frame Construction Example_ 

**==> picture [376 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Header and Data Payload (8 bytes, same as 2.0) LCRC (4 bytes, same as 2.0)<br>Symbol 15<br>Sequence Sequence<br>1111b LEN [3:0] LEN [10:4] Parity bit Number [11:8]Frame CRC [3:0] Number [7:0]<br>**----- End of picture text -----**<br>


**414** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

In summary, the contents of a given Data Block vary depending on the activity: 

- IDLs — when no packets are being delivered Data Blocks consist of nothing but IDL. (The spec designates IDL as one of the Tokens) 

- TLPs — One or more TLPs may be sent in a given Data Block depend‐ ing on the link width. 

- DLLPs — One or more DLLPs may be sent in a Data Block. 

- Combinations of the activity listed above may be delivered in a single Data Block 

## **Framing Tokens** 

The spec defines five Framing Tokens (or just “Tokens” for short) that are allowed to appear in a Data Block, and those are repeated for convenience here in Figure 12‐8 on page 417. The five Tokens are: 

**1. STP ‐ Start TLP** : Much like earlier version, but now includes dword count for the entire packet. 

**2. SDP ‐ Start DLLP** 

3. **EDB ‐ End Bad** : Used to nullify a TLP the way it was in earlier Gen1 and Gen2 designs, but now four EDB symbols in a row are sent. The END (End Good) symbol is done away now; if not explicitly marked as bad, the TLP will be assumed to be good. 

**4. EDS ‐ End of Data Stream** : Last dword of a Data Stream, indicating that at least one Ordered Set will follow. Curiously, the Data Stream may not actually be ended by this event. If the Ordered Set that follows it is an SOS and is immediately followed by another Data Block, the Data Stream continues. If the Ordered Set that follows the EDS is anything other than SOS, or if the SOS is not followed by a Data Block, the Data Stream ends. 

**5. IDL ‐ Logical Idle:** The Idle Token is simply data zero bytes sent during Link Logical Idle state when no TLPs or DLLPs are ready to transmit. 

The difference between the way the spec shows the Tokens and the way they’re presented in Figure 12‐8 on page 417 is that this drawing shows both bytes and bits in little‐endian order instead of the big‐endian bit representa‐ tion used in the spec. The reason it’s shown that way is to illustrate the order that the bits will actually appear on the Lane. 

## **Packets** 

The STP and SDP, indicate the start of a packet as shown in Figure 12‐7 

- **TLPs** . An **STP** Token consists of a nibble of 1’s followed by an 11‐bit dword‐ length field. The length counts all the dwords of the TLP, including the 

**415** 

## **PCI Ex ress Technolo p gy** 

Token, header, optional data payload, optional digest, and LCRC. That allows the receiver to count dwords to recognize where the TLP ends. Con‐ sequently, it’s very important to verify that the Length field doesn’t have an error, and so it has a 4‐bit Frame CRC, and an even parity bit that protects both the Length and Frame CRC fields. The combination of these bits pro‐ vides a robust triple‐bit‐flip detection capability for the Token (as many as 3 bits could be incorrect and it would still be recognized as an error). The 11‐ bit Length field allows for a TLP of 2K dwords (8KB) for the entire TLP. 

- **DLLPs** . The **SDP** Token indicates the beginning of a DLLP and doesn’t include a length field because it will always be exactly 8 bytes long: the 2‐ byte Token is followed by 4 bytes of DLLP payload and 2 bytes of DLLP LCRC. Perhaps coincidently, this DLLP length is the same as it was in ear‐ lier PCIe generations, but they also do not have an end good symbol. 

The **EDB** Token is added to the end of TLPs that are nullified. For a normal TLP, there is no “end good” indication; it’s assumed to be good unless explicitly marked as bad. If the TLP ends up being nullified, the LCRC value is inverted and an EDB Token is appended as an extension of the TLP, although it’s not included in the length value. Physical layer receivers must check for the EDB at the end of every TLP and inform the Link layer if they see one. Not surprisingly, receiving an EDB at any time other than immediately after a TLP will be consid‐ ered to be a Framing Error. 

**416** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## _Figure 12‐8: Gen3 Frame Token Examples_ 

**==> picture [368 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 STP<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 SDP<br>Symbol 0 Symbol 1<br>Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 EDS<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Tx<br>0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 EDB<br>Symbol 0 Symbol 1 Symbol 2 Symbol 3<br>Tx<br>0 1 2 3 4 5 6 7 IDL<br>Symbol 0<br>0011 0101<br>1111 1000b 0000 0001b 0000 1001b 0000 0000b<br>0000 0011b 0000 0011b 0000 0011b 0000 0011b<br>0000 0000b<br>Sequence Sequence<br>1111b LEN [0:3] LEN [4:10] Frame Parity bitNumber [8:11]Frame CRC [0:3] Number [0:7]<br>0000b 1111b<br>**----- End of picture text -----**<br>


## **Transmitter Framing Requirements** 

To begin this discussion, it will be helpful first to define a couple of things. First, recall that a Data Stream starts with the first Symbol following an SDS and it may contain Data Blocks made up of Tokens, TLPs and DLLPs. The Data Stream finishes with the last Symbol before an Ordered Set other than SOS, or when a Framing Error is detected. During a Data Stream no Ordered Sets can be sent except for the SOS. 

Secondly, since framing problems will usually result in a Framing Error, it will help to explain what happens in that case. When Framing Errors occur, they are 

**417** 

## **PCI Ex ress Technolo p gy** 

considered Receiver Errors and will be reported as such. The Receiver stops processing the Data Stream in progress and will only process a new Data Stream when it sees an SDS Ordered Set. In response to the error, a recovery process is initiated by directing the LTSSM to the Recovery state from L0. The expectation is that this will be resolved in the Physical Layer and will not require any action by the upper layers. In addition, the spec states that the round‐trip time to accomplish this is expected to take less than 1  s from the time both Ports have entered Recovery. 

Now, with that background in place, let’s continue with the framing require‐ ments. While in a Data Stream, a transmitter must observe the following rules: 

- When sending a TLP: 

   - An STP Token must be immediately followed by the entire contents of the TLP as delivered from the Link Layer, even if it’s nullified. 

   - If the TLP was nullified, the EDB Token must appear immediately after the last dword of the TLP, but must not be included in the TLP length value. 

   - An STP cannot be sent more than once per Symbol Time on the Link. 

- When sending a DLLP: 

   - An SDP Token must be immediately followed by the entire contents of the DLLP as delivered from the Data Link Layer. 

   - 

      - An SDP cannot be sent more than once per Symbol Time on the Link. 

- When sending an SOS (SKP Ordered Set) within a Data Stream: 

   - Send an EDS Token in the last dword of the current Data Block. 

   - Send the SOS as the next Ordered Set Block. 

   - Send another Data Block immediately after the SOS. The Data Stream resumes with the first Symbol of this subsequent Data Block. 

   - If multiple SOS’s are scheduled, they can’t be back‐to‐back as they were in earlier generations. Instead, each one must be preceded by a Data Block that ends with the EDS Token. The Data block can be filled with TLPs, DLLPs or IDLs during this time.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-3"></a>
## 10.3 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- To end a Data Stream, send the EDS Token in the last dword of the current Data Block and follow that with either the EIOS to go into a low power Link state, or an EIEOS for all other cases. 

- The IDL Token must be sent on all Lanes if a TLP, DLLP, or other Framing Token is not being sent on the Link. 

- For multi‐Lane Links: 

   - After sending an IDL Token, the first Symbol of the next TLP or DLLP must be in Lane 0 when it starts. An EDS Token must always be the last dword of a Data Block and therefore may not always follow that rule. 

   - IDL Tokens must be used to fill in dwords during a Symbol Time that would otherwise be empty. For example, if a x8 Link has a TLP that 

**418** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

ends in Lane 3, but the sender doesn’t have another TLP or a DLLP ready to start in Lane 4, then IDLs must fill in the remaining bytes until the end of that Symbol Time. 

- Since packets are still multiples of 4 bytes as they were in the earlier generations, they’ll start and end on 4‐Lane boundaries. For example, a x8 Link with a DLLP that ends in Lane 3 could start the next TLP by placing its STP Token in Lane 4. 

## **Receiver Framing Requirements** 

When a Data Stream is seen at the Receiver, the following rules apply: 

- When Framing Tokens are expected, Symbols that look like anything else will be Framing Errors. 

- Some error checks and reports shown in the list below are optional, and the spec points out that they are independently optional. 

- When an STP is received: 

   - Receivers must check the Frame CRC and Frame Parity fields, and any mismatch will be a Framing Error. (Note that an STP Token with a Framing Error isn’t considered to be part of a TLP when reporting this error.). 

   - The Symbol immediately after the last DW of the TLP is the next Token to process, and Receivers must check to see whether it’s the start of an EDB Token showing that the TLP has been nullified. 

   - Optionally check for length value of zero; if detected, it’s a Framing Error. 

   - Optionally check for the arrival of more than one STP Token in the same Symbol Time. If checking and detected, this is a Framing Error. 

- When an EDB is received: 

   - Receiver must inform the Link Layer as soon as the first EDB Symbol is detected, or after any of the remaining bytes of it have been received. 

   - If any Symbols in the Token are not EDBs, the result is a Framing Error. 

   - The only legal time for an EDB Token is right after a TLP; any other use will be a Framing Error. 

   - The Symbol immediately following the EDB Token will be the first Symbol of the next Token to be processed. 

- When an EDS Token is received as the last DW of a Data Block: 

   - Receivers must stop processing the Data Stream. 

   - Only a SKP, EIOS, or EIEOS Ordered Set will be acceptable next; receiv‐ ing any other Ordered set will be a Framing Error. 

   - If a SKP Ordered Set is received after an EDS, Receivers must resume Data Stream processing with the first Symbol of the Data Block that fol‐ lows, unless a Framing Error was detected. 

**419** 

## **PCI Ex ress Technolo p gy** 

- When an SDP Token is received: 

   - The Symbol immediately after the DLLP is the next Token to be pro‐ cessed. 

   - Optionally check for more than one SDP Token in the same Symbol Time. If checking and this occurs, it is a Framing Error. 

- When an IDL Token is received: 

   - The next Token is allowed to begin on any DW‐aligned Lane following the IDL Token. For Links that are x4 or narrower, that means the next Token can only start in Lane 0 of the next Symbol Time. For wider Links there are more options. For example, a x16 Link could start the next Token in Lane 0, 4, 8, or 12 of the current Symbol Time. 

   - The only Token that would be expected in the same Symbol Time as an IDL would be another IDL or an EDS. 

- While processing a Data Stream, Receivers will see the following as Fram‐ ing Errors: 

   - 

   - An Ordered Set immediately following an SDS. 

- A Block with an illegal Sync Header (11b or 00b). This can optionally be reported in the Lane Error Status register. 

- An Ordered Set Block on any Lane without receiving an EDS Token in the previous Block. 

- A Data Block immediately following an EDS Token in the previous block. 

- 

- Optionally, verify that all Lanes receive the same Ordered Set. 

## **Recovery from Framing Errors** 

If a Framing Error is seen while processing a Data Stream, the Receiver must: 

- Report a Receiver Error (if the optional Advanced Error Reporting registers are available, set the status bit shown in Figure 12‐9 on page 421). 

- Stop processing the Data Stream. Processing a new Data Stream can begin when the next SDS Ordered Set is seen. 

- Initiate the error recovery process. If the Link is in the L0 state, that will involve a transition to the Recovery state. The spec says that the time through the Recovery state is “expected” to be less than 1  s. 

- Note that recovery from Framing Errors is not necessarily expected to directly cause Data Link Layer initiated recovery activity via the Ack/Nak mechanism. Of course, if a TLP is lost or corrupted as a result of the error, then a replay event will be needed. 

**420** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐9: AER Correctable Error Register_ 

**==> picture [366 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 14 13 12 11 9 8 7 6 5 1 0<br>RsvdZ RsvdZ RsvdZ<br>Header Log Overflow Status<br>Corrected Internal Error Status<br>Advisory Non-Fatal Error Status<br>Replay Timer Timeout Status<br>REPLAY_NUM Rollover Status<br>Bad DLLP Status<br>Bad TLP Status<br>Receiver Error Status<br>Note: all bits designated RW1CS<br>**----- End of picture text -----**<br>


## **Gen3 Physical Layer Transmit Logic** 

Figure 12‐10 on page 422 illustrates a conceptual block diagram of the Physical Layer transmit logic that supports Gen3 speeds. The overall design is very simi‐ lar to Gen2 so there’s no need to go through all the details again but there are some differences. Those who are new to PCIe are encouraged to review the ear‐ lier chapter called “Physical Layer ‐ Logical (Gen1 and Gen2)” on page 361 to learn the basics of the Physical Layer design. Let’s start at the top of the diagram and explain the changes for Gen3 along the way. As before, it’s important to point out that this implementation is only for instructional purposes and is not meant to show an actual Gen3 Physical Layer implementation. 

## **Multiplexer** 

TLPs and DLLPs arrive from the Data Link Layer at the top. The multiplexer mixes in the STP or SDP Tokens necessary to build a complete TLP or DLLP. The previous section described the Token formats. 

**421** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐10: Gen3 Physical Layer Transmitter Details_ 

**==> picture [260 x 371] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Gen3 Scrambler Lane 1, ... ,N-1 Gen3 Scrambler<br>Scrambler Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>8 10 Tx Clk 8 10<br>Mux Mux<br>Gen3 Sync<br>Serializer Bits Generator Serializer<br>Mux Mux<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- End of picture text -----**<br>


**422** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

Gen3 TLP boundaries are defined by the dword count in the Length field of the STP Token at the beginning of a TLP packet, therefore, no END frame character is needed. 

When ending a Data Stream or just before sending an SOS, the EDS Token in muxed into the Data Stream. At regular intervals, based on a Skip timer, an SOS is inserted into the Data Stream by the multiplexer. Other Ordered‐Sets such as TS1, TS2, FTS, EIEOS, EIOS, SDS may also be muxed based on Link require‐ ments and are outside the Data Stream. 

Packets are transmitted in Blocks which are identified by the 2‐bit Sync Header. The Sych Header is added by the multiplexer. However, the Sych Header is rep‐ licated on all Lanes of a multi‐Lane Link by the Byte Striping logic. 

When there are no packets or Ordered Sets to send but the Link is to remain active in L0 state, the IDL (Logical Idle, or data zero) Tokens are used as fillers. These are scrambled just like other data bytes and are recognized as filler by the Receiver. 

## **Byte Striping** 

This logic spreads the bytes to be delivered across all the available Lanes. The framing rules were described earlier in “Transmitter Framing Requirements” on page 417, so now let’s look at some examples and discuss how the rules apply. 

Consider first the example shown in Figure 12‐11 on page 424, where a 4‐Lane Link is illustrated. Notice that the Sync Header bits appear on all the Lanes at the same time when a new Block begins and define the block type (a Data Block in this example). Block encoding is handled independently for each Lane, but the bytes (or symbols) are striped across all the Lanes just as they were for the earlier generations of PCIe. 

**423** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐11: Gen3 Byte Striping x4_ 

**==> picture [376 x 222] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane 0 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 0 Symbol 4 Symbol 60<br>Lane 1 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 1 Symbol 5 Symbol 61<br>Lane 2 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 2 Symbol 6 Symbol 62<br>Lane 3 0 1 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7<br>Sync Symbol 3 Symbol 7 Symbol 63<br>**----- End of picture text -----**<br>


## **Byte Striping x8 Example** 

Next, consider the x8 Link shown in Figure 12‐12 on page 425, which is an example from the spec redrawn to make it easier to read. Here the bit stream is vertical instead of horizontal. At the top we can see that the Sync bits, shown in little‐endian order as required, appear on all Lanes simultaneously and indicate that a Data Block is starting. 

In this example, a TLP is sent first, so Symbols 0 ‐ 4 contain the STP framing Token, which includes a length of 7 DW for the entire TLP including the Token. The receiver needs to know the length of the TLP because for 8 GT/s speeds there is no END control character. Instead, the receiver counts the dwords and if there is no EDB (End Bad) observed, the TLP is assumed to be good. In this case, the TLP ends on Lane 3 of Symbol 3. 

**424** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_ 

|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|_Figure 12‐12: Gen3 x8 Example: TLP Straddles Block Boundary_|
|---|---|---|---|---|---|---|---|---|
||||||||||

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-4"></a>
## 10.4 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-5"></a>
## 10.5 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Receivers must check to see that every SOS in a Data Stream is preceded by a Data Block that ends with EDS. 

## **Scrambling** 

The scrambling logic for 128b/130b is modified from the previous PCIe genera‐ tions to address the two issues that 8b/10b encoding handled automatically: maintaining DC Balance and providing a sufficient transition density. By way of review, recall that DC Balance means the bit stream has an equal number of ones and zeros. This is intended to avoid the problem of “DC wonder”, in which the transmission medium is charged toward one voltage or the other so much, by a prevalence of ones or zeros, that it becomes difficult to switch the signal within the necessary time. The other problem is that clock recovery at the Receiver needs to see enough edges in the input signal to be able to compare them to the recovered clock and adjust the timing and phase as needed. 

Without 8b/10b to handle these issues, three steps were taken: First, the new scrambling method improves both transition density and DC Balance over longer time periods, but doesn’t guarantee them over short periods the way 8b/ 10b did. Second, the TS1 and TS2 Ordered Set patterns used during training include fields that are adjusted as needed to improve DC Balance. And third, Receivers must be more robust and tolerant of these issues than they were in the earlier generations. 

## **Number of LFSRs** 

At the lower data rates every Lane was scrambled in the same way, so a single Linear‐Feedback Shift Register (LFSR) could supply the scrambling input for all of them. For Gen3, though, the designers wanted different scrambling values for neighboring Lanes. The reasons probably include a desire to decrease the possibility of cross‐talk between the Lanes by scrambling their outputs with respect to each other and avoid having the same value on each Lane, as might 

**430** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

happen when sending IDLs. The spec describes two approaches to achieving this goal, one that emphasizes lower latency and one that emphasizes lower cost. 

**First Option: Multiple LFSRs.** One solution is to implement a separate LFSR for each Lane, and initialize each with a different starting value or “seed”. This has the advantage of simplicity and speed, at the cost of add‐ ing logic. As shown in Figure 12‐16, each LFSR creates a pseudo‐random output based on the polynomial given in the spec as G(X) = X[23] + X[21] + X[16] + X[8] + X[5] + X[2] + 1. This polynomial is longer than the previous version and also behaves a little differently because of the different seed values. Eight different seed values for each Lane are specified requiring eight different LFSRs, one per Lane 0 through 7. 

_Figure 12‐16: Gen3 Per‐Lane LFSR Scrambling Logic_ 

**==> picture [369 x 155] intentionally omitted <==**

**----- Start of picture text -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>+ + +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+ +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>Data In + Data Out<br>**----- End of picture text -----**<br>


The 24‐bit seed value for each Lane is listed in Table 12‐3 on page 432. The series repeats itself, meaning the seed for Lane 8 will be the same as Lane 0, so only the first 8 values are shown. Every Lane uses the same LFSR and the same tap points to create the scrambling output, and the different seed val‐ ues give the desired difference. 

**431** 

## **PCI Ex ress Technolo p gy** 

_Table 12‐3: Gen3 Scrambler Seed Values_ 

|**Lane**|**Seed Value**|
|---|---|
|0|1DBFBCh|
|1|0607BBh|
|2|1EC760h|
|3|18C0DBh|
|4|010F12h|
|5|19CFC9h|
|6|0277CEh|
|7|1BB807h|



**Second Option: Single LFSR.** The alternative solution, illustrated in Figure 12‐17 on page 433 for Lanes 2, 10, 18, and 26, is to use just one LFSR and create the scrambling inputs for each Lane by XORing different tap points together. Since there’s only one LFSR, the seed value is the same for all Lanes (all ones), but the scrambling “Tap Equation” for each Lane is derived by combining different tap points, as shown in Table 12‐4 on page 433. The spec also notes that 4 of the Lanes Tap Equations can be derived by XORing the tap values of their bit neighbors: 

- Lane 0 = Lane 7 XOR Lane 1 (note that the process of going to lower Lane numbers wraps around, with the result that Lane 7 is considered lower that Lane 0) 

- Lane 2 = Lane 1 XOR Lane 3 

- Lane 4 = Lane 3 XOR Lane 5 

- Lane 6 = Lane 5 XOR Lane 7 

The single‐LFSR solution uses fewer gates than the multi‐LFSR version does, but incurs extra latency through the XOR process, providing a differ‐ ent cost/performance option. 

**432** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐17: Gen3 Single‐LFSR Scrambler_ 

**==> picture [378 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>+ + +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+ +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+<br>“Tap Equation” for Lanes 2, 10, 18, and 26<br>Data In + Data Out<br>(for Lanes 2, 10, 18, or 26)<br>**----- End of picture text -----**<br>


_Table 12‐4: Gen3 Tap Equations for Single‐LFSR Scrambler_ 

|**Lane Numbers**<br>**T**|**ap Equation**|
|---|---|
|0, 8, 16, 24<br>|D9 xor D13|
|1, 9, 17, 25<br>|D1 xor D13|
|2, 10, 18, 26<br>|D13 xor D22|
|3, 11, 19, 27<br>|D1 xor D22|
|4, 12, 20, 28<br>|D3 xor D22|
|5, 13, 21, 29|D1 xor D3|
|6, 14, 22, 30|D3 xor D9|
|7, 15, 23, 31|D1 xor D9|



## **Scrambling Rules** 

The Gen3 scrambler LFSRs (whether one or more) do not continually advance, but only advance based on what is being sent. The scramblers must be re‐initial‐ ized periodically and that takes place whenever an EIEOS or FTSOS is seen. The spec gives several rules for scrambling that are listed here for convenience: 

**433** 

## **PCI Ex ress Technolo p gy** 

- Sync Header bits are not scrambled and do not advance the LFSR. 

- The Transmitter LFSR is reset when the last EIEOS Symbol has been sent, and the Receiver LFSR is reset when the last EIEOS Symbol is received. 

- TS1 and TS2 Ordered Sets: 

   - Symbol 0 bypasses scrambling 

   - Symbols 1 to 13 are scrambled 

   - Symbols 14 and 15 may or may not be scrambled. The spec states that they will bypass scrambling if necessary to improve DC Balance, but otherwise will be scrambled (see “TS1 and TS2 Ordered Sets” on page 510 for more details on how DC Balance is maintained). 

- All Symbols of the Ordered Sets FTS, SDS, EIEOS, EIOS, and SOS bypass scrambling. Despite this, the output data stream will have sufficient transi‐ tion density to allow clock recovery and the symbols chosen for the Ordered Sets result in a DC balanced output. 

- Even when bypassed, Transmitters advance their LFSRs for all Ordered Set Symbols except for those in the SOS. 

- Receivers do the same, checking Symbol 0 of an incoming Ordered Set to see whether it is an SOS. If so, the LFSRs are not advanced for any of the Symbols in that Block. Otherwise the LFSRs are advanced for all the Sym‐ bols in that Block. 

- All Data Block Symbols are scrambled and advance the LFSRs. 

- Symbols are scrambled in little‐endian order, meaning the least‐significant bit is scrambled first and the most‐significant bit is scrambled last. 

- The seed value for a per‐Lane LFSR depends on the Lane number assigned to the Lane when the LTSSM first entered Configuration.Idle (having fin‐ ished the Polling state). The seed values, modulo 8, are shown in Table 12‐3 on page 432 and, once assigned, won’t change as long LinkUp = 1 even if Lane assignments are changed by going back to the Configuration state. 

- Unlike 8b/10b, scrambling cannot be disabled while using 128b/130b encod‐ ing because it is needed to help with signal integrity. It’s not expected that the Link would operate reliably without it, so it must always be on. 

- A Loopback Slave must not scramble or de‐scramble the looped‐back bit. 

## **Serializer** 

This shift register works like it does for Gen1/Gen2 data rates except that it is now receiving 8 bits at a time instead of 10 (i.e., the serializer is an 8‐bit parallel to serial shift register). 

**434** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **Mux for Sync Header Bits** 

Finally, the two Sync Header bits must be injected to distinguish the next Block of characters as a Data Block or an Ordered Set Block. These are the first two bits of each 130‐bit Block and the logic for them could be added anywhere in the transmitter that makes sense for the design. In this example the bits are injected at the end of the process for simplicity. Wherever they are included, the flow of bytes from above must be stalled to allow time for them. In this example there will need to be a way to inform the logic above to pause for two bit times. The flow of incoming packets will just be queued in the Tx Buffer during the time the Sync bits are being sent. 

## **Gen3 Physical Layer Receive Logic** 

As in the earlier generations, the Receiver’s logic, shown in Figure 12‐18 on page 436, begins with the CDR (Clock and Data Recovery) circuit. This probably includes a PLL that locks onto the frequency of the Transmitter clock based on knowledge of the expected frequency and the edges in the bit stream to gener‐ ate a recovered clock (Rx Clock). This recovered clock latches the incoming bits into a deserializing buffer and then, once Block Alignment has been established (during the Recovery state of the LTSSM), another version of the recovered clock that is divided by 8.125 (Rx Clock/8.125) latches the 8‐bit Symbols into the Elastic Buffer. After that, the de‐scrambler recreates the original data from the scrambled characters. The bytes bypass the 8b/10b decoder and are delivered directly to the Byte Un‐striping logic. Finally, the Ordered Sets are filtered out, and the remaining byte stream of TLPs and DLLPs is forwarded up to the Data Link Layer. 

In the following discussion, each part is described working upward from the bottom. The focus is on describing aspects of the Physical Layer changed for 8.0 GT/s. Sub‐block unchanged from Gen1/Gen2 will not be described in this sec‐ tion. 

## **Differential Receiver** 

The differential receiver logic is unchanged, but there are electrical changes to improve signal integrity (see “Signal Compensation” on page 468), as well as training changes to establish signal equalization, which are covered in “Link Equalization Overview” on page 577. 

**435** 

## **PCI Ex ress Technolo p gy** 

_Figure 12‐18: Gen3 Physical Layer Receiver Details_ 

**==> picture [276 x 369] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


**436** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐19: Gen3 CDR Logic_ 

**==> picture [385 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-6"></a>
## 10.6 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-10-7"></a>
## 10.7 Ack/Nak Protocol | Ack/Nak 协议

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

For multi‐Lane Links, the difference in arrival times between lanes is automati‐ cally corrected at the Receiver by delaying the early arrivals until they all match up. The spec allows this to be accomplished by any means a designer prefers, but using a digital delay after the elastic buffer has one advantage in that the arrival time differences are now digitized to the local Symbol clock of the receiver. If the input to one lane makes it on a clock edge and another one doesn’t, the difference between them will be measured in clock periods, so the early arrival can simply be delayed by the appropriate number of clocks to get it to line up with the late‐comers (see Figure 12‐22 on page 444). The fact that the maximum allowable skew at the receiver is a multiple of the clock periods makes this easy and infers that the spec writers may have had this implementa‐ tion in mind. As defined in the spec, the receiver must be capable of de‐skewing up to 20ns for Gen1 (5 Symbol‐time clocks at 4ns per Symbol) and 8ns for Gen2 (4 Symbol‐time clocks at 2ns per Symbol), and 6ns for Gen3 (6 Symbol‐time clocks at 1ns per Symbol). 

## **De-skew Opportunities** 

The same Symbol must be seen on all lanes at the same time to perform de‐ skewing, and any Ordered Set will do. However, de‐skewing is only performed in the L0s, Recovery, and Configuration LTSSM states. In particular, it must be completed as a condition for: 

- Leaving Configuration.Complete 

- Beginning to process a Data Stream after leaving Configuration.Idle or Recovery.Idle 

- Leaving Recovery.RcvrCfg 

- Leaving Rx_L0s.FTS 

**442** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

If skew values change while in L0 (based on temperature or voltage changes, for example), a Receiver error may occur and cause replayed TLPs. If the problem becomes persistent, the Link would eventually transition to the Recovery state and de‐skewing would take place there. The spec notes that, while devices are not allowed to de‐skew their Lanes while in L0, the SOSs that must be sent peri‐ odically in this state contain an LFSR value that is intended to aid external tools in doing this. These tools, unconstrained by the rules for Data Streams, can search for the SOSs and use the patterns to achieve Bit Lock, Block Alignment and Lane‐to‐Lane de‐skew in the midst of a Data Stream. 

The spec notes that when leaving L0s the Transmitter will send an EIEOS, then the correct number of FTSs with another EIEOS inserted after every 32 FTSs, then one last EIEOS to assist with Block Alignment and, finally, an SDS Ordered Set for the purpose of de‐skewing in addition to starting the Data Stream. 

## **Receiver Lane-to-Lane De-skew Capability** 

Understandably, the transmitter is only allowed to introduce a minimal amount of skew so as to leave the rest of the skew budget to cover routing differences and other variations. The amount of allowed skew that can be corrected at the Receiver is shown in Table 12‐5 on page 443, where it can be seen that this skew corresponds easily to a number of Symbol times for Gen3 just as it did for the earlier data rates. That allows the same option of using delay registers to accom‐ plish de‐skew after the elastic buffer as was described for Gen1/Gen2 Physical Layer implementations earlier. 

_Table 12‐5: Signal Skew Parameters_ 

||Gen1|Gen2|Gen3|
|---|---|---|---|
|Tx max skew|1.3 ns|1.3 ns|1.1 ns|
|Rx max skew|20 ns|8 ns|6 ns|
|Symbol time period|4ns|2ns|1ns|
|Rx skew expressed<br>in Symbol Times|5|4|6|



When using 8b/10b encoding, an unambiguous de‐skew mechanism is to watch for the COM control character, which must appear on all Lanes simultaneously. That option is not available for 128b/130b, but Ordered Sets still arrive at the same time on all the Lanes, such as the SOS, SDS, and EIEOS. As a result, the process can be very much the same even though the pattern to search for when de‐skewing the Lanes is different. 

**443** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐22: Receiver Link De‐Skew Logic_ 

**==> picture [374 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOS, SDS, SOS, SDS,<br>Lane 0 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>Lane 1 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>Lane 2 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>EIEOS EIEOS<br>Lane 3 Rx Delay<br>(symbols)<br>SYNC SYNC<br>SYNC SYNC<br>SYNC SYNC<br>SYNC SYNC<br>**----- End of picture text -----**<br>


## **Descrambler** 

## **General** 

Receivers follow exactly the same rules for generating the scrambling polyno‐ mial that the Transmitter does and simply XOR the same value to the input data a second time to recover the original information. Like on the transmit side, they are allowed to implement a separate LFSR for each Lane or just one. 

## **Disabling Descrambling** 

Unlike at Gen1/Gen2 data rates, in Gen3 mode, descrambling cannot be dis‐ abled because of its role in facilitating clock recovery and signal integrity. At the lower rates, the “disable scrambling” bit in the control byte of TS1s and TS2s would be used to inform a Link neighbor that scrambling was being turned off. That bit is reserved for rates of 8.0 GT/s and higher. 

**444** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **Byte Un-Striping** 

This logic is basically unchanged from Gen1 or Gen2 implementation. At some point, the byte streams for Gen3 and for the lower data rates will have to muxed together, and the example in Figure 12‐23 on page 445 shows that happening just before the un‐striping logic. 

_Figure 12‐23: Physical Layer Receive Logic Details_ 

**==> picture [272 x 358] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


**445** 

**PCI Ex ress Technolo p gy** 

## **Packet Filtering** 

The serial byte stream supplied by the byte un‐striping logic contains TLPs, DLLPs, Logical Idles (IDLs), and Ordered Sets. The Logical Idle bytes and Ordered Sets are eliminated here and are not forwarded to the Data Link layer. What remains are the TLPs and DLLPs, which get forwarded along with an indicator of their packet type. 

## **Receive Buffer (Rx Buffer)** 

The Rx Buffer holds received TLPs and DLLPs until the Data Link Layer is able to accept them. The interface to the Data Link Layer is not described in the spec, and so a designer is free to choose details like the width of this bus. The wider the path, the lower the clock frequency will be, but more signals and logic will be needed to support it. 

## **Notes Regarding Loopback with 128b/130b** 

The spec makes a special point to describe the operation of Loopback Mode at the higher rate. The basic rules can be summarized as follows: 

- Loopback masters must send actual Ordered Sets or Data Blocks, but they aren’t required to follow the normal protocol rules when changing from Data Blocks to Ordered Sets or vice versa. In other words, the SDS Ordered Set and EDS token are not required. Slaves must not expect or check for the presence of them. 

- Masters must send SOS as usual, and must allow for the number of SKP Symbols in the loopback stream to be different because the receiver will be performing clock compensation. 

- Loopback slaves are allowed to modify the SOS by adding or removing 4 SKP Symbols at a time as they normally would for clock compensa‐ tion, but the resulting SOS must still follow the proper format rules. 

- Everything should be looped back exactly as it was sent except for SOS which can change as just described, and both EIEOS and EIOS which have defined purposes in loopback and should be avoided. 

- If a slave is unable to acquire Block alignment, it won’t be able to loop back all bits as received and is allowed to add or remove Symbols as needed to continue operation. 

**446** 

## _**13 Physical Layer ‐ Electrical**_ 

## **The Previous Chapter** 

The previous chapter describes the logical Physical Layer characteristics for the third generation (Gen3) of PCIe. The major change includes the ability to double the bandwidth relative to Gen2 speed without needing to double the frequency (Link speed goes from 5 GT/s to 8 GT/s). This is accomplished by eliminating 8b/10b encoding when in Gen3 mode. More robust signal compensation is nec‐ essary at Gen3 speed. Making these changes is more complex than might be expected. 

## **This Chapter** 

This chapter describes the Physical Layer electrical interface to the Link, includ‐ ing some low‐level characteristics of the differential Transmitters and Receivers. The need for signal equalization and the methods used to accomplish it are also discussed here. This chapter combines electrical transmitter and receiver char‐ acteristics for both Gen1, Gen2 and Gen3 speeds. 

## **The Next Chapter** 

The next chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process of the Link is described from Power‐On or Reset until the Link reaches the fully‐operational L0 state during which normal packet traffic occurs. In addition, the Link power management states L0s, L1, L2, L3 are discussed along with the causes of transi‐ tions between the states. The Recovery state during which bit lock, symbol lock or block lock can be re‐established is described. 

**447** 

**PCI Ex ress Technolo p gy** 

## **Backward Compatibility** 

The spec begins the Physical Layer Electrical section with the observation that newer data rates need to be backward compatible with the older rates. The fol‐ lowing summary defines the requirements: 

- Initial training is done at 2.5 GT/s for all devices. 

- Changing to other rates requires negotiation between the Link partners to determine the peak common frequency. 

- Root ports that support 8.0 GT/s are required to support both 2.5 and 5.0 GT/s as well. 

- Downstream devices must obviously support 2.5 GT/s, but all higher rates are optional. This means that an 8 GT/s device is not required to support 5 GT/s. 

In addition, the optional Reference clock (Refclk) remains the same regardless of the data rate and does not require improved jitter characteristics to support the higher rates. 

In spite of these similarities, the spec does describe some changes for the 8.0 GT/ s rate: 

- **ESD standards:** Earlier PCIe versions required all signal and power pins to withstand a certain level of ESD (Electro‐Static Discharge) and that’s true for the 3.0 spec, too. The difference is that more JEDEC standards are listed and the spec notes that they apply to devices regardless of which rates they support. 

- **Rx powered‐off Resistance:** The new impedance values specified for 8.0 GT/s (ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG) will be applied to devices supporting 2.5 and 5.0 GT/s as well. 

- **Tx Equalization Tolerance:** Relaxing the previous spec tolerance on the Tx de‐emphasis values from +/‐ 0.5 dB to +/‐ 1.0 dB makes the ‐3.5 and ‐6.0 dB de‐emphasis tolerance consistent across all three data rates. 

- **Tx Equalization during Tx Margining:** The de‐emphasis tolerance was already relaxed to +/‐ 1.0 dB for this case in the earlier specs. The accuracy for 8.0 GT/s is determined by the Tx coefficient granularity and the TxEQ tolerances for the Transmitter during normal operation. 

- **VTX‐ACCM and VRX‐ACCM:** For 2.5 and 5.0 GT/s these are relaxed to 150 mVPP for the Transmitter and 300 mVPP for the Receiver. 

**448**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
