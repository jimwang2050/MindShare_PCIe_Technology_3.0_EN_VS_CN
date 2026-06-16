8. If a read request of 1 DW has no byte enables set, the completer returns a 1DW data payload of undefined data. This may be used as a Flush mecha‐ nism that takes advantage of transaction ordering rules to force all previ‐ ously posted writes out to memory before the completion is returned. 

**181** 

## **PCI Ex ress Technolo p gy** 

**Byte Enable Example.** An example of byte enable use in this case is illus‐ trated in Figure 5‐4 on page 182. Note that the transfer length must extend from the first DW with any valid byte enabled to the last DW with any valid bytes enabled. Because the transfer is more than 2DW, the byte enables may only be used to specify the start address location (2d) and end address location (34d) of the transfer. 

_Figure 5‐4: Using First DW and Last DW Byte Enable Fields_ 

## **Transaction Descriptor Fields** 

As transactions move between requester and completer, it’s necessary to uniquely identify a transaction, since many split transactions may be queued up from the same Requester at any instant. To help with this, the spec defines sev‐ eral important header fields that form a unique Transaction Descriptor, as illus‐ trated in Figure 5‐5. 

**182** 

**Chapter 5: TLP Elements** 

_Figure 5‐5: Transaction Descriptor Fields_ 

**==> picture [384 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Completer ID Cmpl CB Byte Count<br>Status M<br>Byte 8 Requester ID Tag R Lower Addr<br>**----- End of picture text -----**<br>


While the Transaction Descriptor fields are not in adjacent header locations, col‐ lectively they describe key transaction attributes, including: 

**Transaction ID.** The combination of the Requester ID (Bus, Device, and Function Number of the Requester) and the Tag field of the TLP. 

**Traffic Class.** The Traffic Class (TC) is added by the requester based on the core logic request and travels unmodified through the topology to the Compl‐ eter. On every Link, the TC is mapped to one of the Virtual Channels. 

**Transaction Attributes.** The ID‐based Ordering, Relaxed Ordering, and No Snoop bits also travel with the Request packet to the Completer. 

## **Additional Rules For TLPs With Data Payloads** 

The following rules apply when a TLP includes a data payload. 

1. The Length field refers only to the data payload. 

2. The first byte of data in the payload (immediately after the header) is always associated with the lowest (start) address. 

3. The Length field always represents an integral number of DWs transferred. Partial DWs are qualified using First and Last Byte Enable fields. 

4. The spec states that, when multiple transactions are returned by a compl‐ eter in response to a single memory request, each intermediate transaction must end on naturally‐aligned 64‐ or 128‐byte address boundaries for a Root Complex. This is controlled by a configuration bit called the Read Completion Boundary (RCB). All other devices follow the PCI‐X protocol 

**183** 

## **PCI Ex ress Technolo p gy** 

and break such transactions at naturally‐aligned 128‐byte boundaries. This makes buffer management simpler in bridges. 

5. The Length field is reserved when sending Message Requests unless the message is the version with data ( _MsgD_ ). 

6. The TLP data payload must not exceed the current value in the Max_Payload_Size field of the Device Control Register. Only write transac‐ tions have data payloads, so this restriction doesn’t apply to read requests. A receiver is required to check for violations of the Max_Payload_Size limit during writes, and violations are treated as Malformed TLPs. 

7. Receivers also must check for discrepancies between the value in the Length field and the actual amount of data transferred in a TLP. This type of viola‐ tion is also treated as a Malformed TLP. 

8. Requests must not mix combinations of start address and transfer length that would cause a memory access to cross a 4KB boundary. While checking for this is optional, if seen it’s treated as a Malformed TLP. 

## **Specific TLP Formats: Request & Completion TLPs** 

In this section, the format of 3DW and 4DW headers used to accomplish specific transaction types are described. Many of the generic fields described previously apply, but an emphasis is placed on the fields which are handled differently with specific transaction types. Detailed description of TLP Header format are described is sections following for TLP types: 1) IO Request, 2) Memory Requests, 3) Configuration Requests, 4) Completions and 5) Message Requests. 

## **IO Requests** 

While the spec discourages the use of IO transactions, allowance is made for Legacy devices and for software that may need to rely on a compatible device residing in the system IO map rather than the memory map. While the IO trans‐ actions can technically access a 32‐bit IO range, in reality many systems (and CPUs) restrict IO access to the lower 16 bits (64KB) of this range. Figure 5‐6 on page 185 depicts the system IO map and the 16‐ and 32‐bit address boundaries. Devices that don’t identify themselves as Legacy devices are not permitted to request IO address space in their configuration Base Address Registers. 

**184** 

**Chapter 5: TLP Elements** 

_Figure 5‐6: System IO Map_ 

**IO Request Header Format.** A 3 DW IO request header is shown in Fig‐ ure 5‐7 on page 185 and each of the fields is described in the section that fol‐ lows. 

_Figure 5‐7: 3DW IO Request Header Format_ 

**==> picture [281 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>IO Request TLP<br>a|<br>Legacy =o Framing(STP) SequenceNumber Header Data Digest LCRC Framing(End)<br>Endpoint<br>+0 +1 +2 +3<br>Peer 7 6 5 4 3 2 1 0 7 nT 6 5 4 3 2 1 0 7 6 5 4 3 2 TTT 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 0 1 0Type R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**185** 

**PCI Ex ress Technolo p gy** 

**IO Request Header Fields.** The location and use of each field in an IO request header is described in Table 5‐4 on page 186. 

_Table 5‐4: IO Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Format for IO requests:<br>000b = IO Read (3DW without data)<br>010b = IO Write (3DW with data)|
|Type [4:0]|Byte 0 Bit 4:0|Packet type is 00010b for IO requests|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Traffic Class for IO requests is always<br>zero, ensuring that these packets will<br>never interfere with any high‐priority<br>packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|ID‐based Ordering doesn’t apply for<br>IO requests and this bit is reserved.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|TLP processing Hints don’t apply to<br>IO requests and this bit is reserved.|
|TD<br>(TLP Digest)|Byte 2 Bit 7|Indicates the presence of a digest field<br>(ECRC) at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|Indicates whether the data payload (if<br>present) is poisoned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Relaxed Ordering and No Snoop bits<br>don’t apply for IO requests and are<br>always zero.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type doesn’t apply for IO<br>requests and these bits must be zero.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW.<br>For IO requests, this field is always<br>just 1 since no more than 4 bytes can<br>be transferred. The First DW Byte<br>Enables qualify which bytes are used.|



**186** 

**Chapter 5: TLP Elements** 

_Table 5‐4: IO Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester’s “return<br>address” for corresponding Comple‐<br>tion.<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These bits identify the specific<br>requests from the requester. A unique<br>tag value is assigned to each outgoing<br>Request. By default, only bits 4:0 are<br>used, but the Extended Tag and Phan‐<br>tom Functions options can extend that<br>to 11 bits, permitting up to 2048 out‐<br>standing requests to be in progress<br>simultaneously.|
|Last DW BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These bits must be 0000b because IO<br>requests can only be one DW in size.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These bits qualify the bytes in the one‐<br>DW payload. For IO requests, any bit<br>combination is valid (including all<br>zeros).|
|Address [31:2]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:2|The upper 30 bits of the 32‐bit start<br>address for the IO transfer. The lower<br>two bits of the 32 bit address are<br>reserved (00b), forcing a DW‐aligned<br>start address.|



**187** 

**PCI Ex ress Technolo p gy** 

## **Memory Requests** 

PCI Express memory transactions include two classes: Read Requests with their corresponding Completions, and Write Requests. The system memory map shown in Figure 5‐8 on page 188 depicts both a 3DW and 4DW memory request packet. Keep in mind a point that the spec reiterates several times: a memory transfer is never permitted to cross a 4KB address boundary. 

_Figure 5‐8: 3DW And 4DW Memory Request Header Formats_ 

**==> picture [382 x 316] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex Memory<br>3DW or 4DW Memory Request TLP<br>Framing(STP) SequenceNumber Header Data Digest LCRC Framing(End)<br>4DW Memory Request Header<br>PCIe +0 +1 +2 +3<br>Endpoint System Memory Map<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2 64<br>Byte 0 0 x 1Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>3DW Memory Request Header<br>+0 +1 +2 +3<br>4GB<br>32<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2<br>Byte 0 0 x 0Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE 0<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**Memory Request Header Fields.** The location and use of each field in a 4DW memory request header is listed in Table 5‐5 on page 189. Note that the difference between a 3DW header and a 4DW header is simply the location and size of the starting Address field. 

**188** 

**Chapter 5: TLP Elements** 

_Table 5‐5: 4DW Memory Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Formats:<br>000b = Memory Read (3DW w/o data)<br>010b = Memory Write (3DW w/ data)<br>001b = Memory Read (4DW w/o data)<br>011b = Memory Write (4DW w/ data)<br>1xxb = TLP Prefix has been added to<br>the beginning of the packet. See “TPH<br>(TLP Processing Hints)” on page 899<br>for more on this.|
|Type[4:0]|Byte 0 Bit 4:0|TLP packet Type field:<br>00000b = Memory Read or Write<br>00001b = Memory Read Locked<br>Type field is used with Fmt [1:0] field<br>to specify transaction type, header<br>size, and whether data payload is<br>present.|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|These bits encode the traffic class to<br>be applied to a Request and to any<br>associated Completion.<br>000b = Traffic Class 0 (Default)<br>.<br>.<br>111b = Traffic Class 7<br>See“Traffic Class (TC)” on page 247<br>for more on this.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|Indicates whether ID‐based Ordering<br>is to be used for this TLP. To learn<br>more, see “ID Based Ordering (IDO)”<br>on page 301.|