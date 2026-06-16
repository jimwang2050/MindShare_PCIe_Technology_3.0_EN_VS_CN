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
