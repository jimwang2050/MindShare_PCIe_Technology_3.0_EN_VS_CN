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