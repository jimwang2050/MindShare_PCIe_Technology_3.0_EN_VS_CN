Figure 5‐3 on page 175 illustrates the format and contents of a generic TLP 4DW header. In this section, fields common to nearly all transactions are summa‐ rized. Header format differences associated with specific transaction types are covered later. 

_Figure 5‐3: Generic TLP Header Fields_ 

**==> picture [328 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Framing Sequence Framing<br>Header Data Digest LCRC<br>(STP) Number (End)<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Bytes 4-7 vary with Type BE BE<br>Byte 8 Bytes 8-11 vary with Type<br>Byte 12 Bytes 12-15 vary with Type (not always required)<br>**----- End of picture text -----**<br>


## **Generic Header Field Summary** 

Table 5‐2 on page 176 summarizes the size and use of each of the generic TLP header fields. Note that fields marked “R” in Figure 5‐3 on page 175 are reserved and should be set to zero. 

**175** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐2: Generic Header Field Summary_ 

|**Header**<br>**Field**|**Header**<br>**Location**|**Field Use**|
|---|---|---|
|Fmt[2:0]<br>(Format)|Byte 0 Bit 7:5|These bits encode information about header size and<br>whether a data payload will be part of the TLP:<br>00b 3DW header, no data<br>01b 4DW header, no data<br>10b 3DW header, with data<br>11b 4DW header, with data<br>An address below 4GB must use a 3DW header. The<br>spec states that receiver behavior is undefined if<br>4DW header is used for an address below 4GB with<br>the upper 32 bits of the 64‐bit address set to zero.|
|Type[4:0]|Byte 0 Bit 4:0|These bits encode the transaction variant used with<br>this TLP. The Type field is used with Fmt [1:0] field<br>to specify transaction type, header size, and whether<br>data payload is present. See “Generic Header Field<br>Details” on page 178 for details.|
|TC [2:0]<br>(Traffic<br>Class)|Byte 1 Bit 6:4|These bits encode the traffic class to be applied to<br>this TLP and to the completion associated with it (if<br>any):<br>000b = Traffic Class 0 (Default)<br>.<br>.<br>111b = Traffic Class 7<br>TC 0 is the default class, while TC 1‐7 are used to<br>provide differentiated services. See “Traffic Class<br>(TC)” on page 247 for additional information.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|This third Attribute bit indicates whether ID‐based<br>Ordering is to be used for this TLP. To learn more,<br>see “ID Based Ordering (IDO)” on page 301.|
|TH<br>(TLP Pro‐<br>cessing<br>Hints)|Byte 1 Bit 0|Indicates when TLP Hints have been included to<br>give the system some idea about how best to handle<br>this TLP. See “TPH (TLP Processing Hints)” on<br>page 899 for a discussion on their usage.|



**176** 

**Chapter 5: TLP Elements** 

_Table 5‐2: Generic Header Field Summary (Continued)_ 

|**Header**<br>**Field**|**Header**<br>**Location**||**Field Use**|
|---|---|---|---|
|TD<br>(TLP Digest)|Byte 2 Bit 7||If TD = 1, the optional 4‐byte TLP Digest has been<br>included with this TLP as the ECRC value.<br>Some rules<br>:<br>• Presence of the Digest field must be checked by all<br>receivers based on this bit.<br>• A TLP with TD = 1 but no Digest is handled as a<br>Malformed TLP.<br>• If a device supports checking ECRC and TD=1, it<br>must perform the ECRC check.<br>• If a device does not support checking ECRC<br>(optional) at the ultimate destination, it must<br>ignore the digest.<br>For more on this topic see “CRC” on page 653 and<br>“ECRC Generation and Checking” on page 657.|
|EP<br>(Poisoned<br>Data)|Byte 2 Bit 6||If EP = 1, the data accompanying this data should be<br>considered invalid although the transaction is being<br>allowed to complete normally. For more on poisoned<br>packets, refer to “Data Poisoning” on page 660.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4||Bit 5=Relaxed ordering<br>:When set to 1, PCI‐X<br>relaxed ordering is enabled for this TLP. If 0, then<br>strict PCI ordering is used.<br>Bit 4=No Snoop:<br>When set to 1, Requester is indicat‐<br>ing that no host cache coherency issues exist for this<br>TLP. System hardware can thus save time by skip‐<br>ping the normal processor cache snoop for this<br>request. When 0, PCI ‐type cache snoop protection is<br>required.|



**177** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐2: Generic Header Field Summary (Continued)_ 

|**Header**<br>**Field**|**Header**<br>**Location**|**Field Use**|
|---|---|---|
|Address<br>Type [1:0]|Byte 2 Bit 3:2|For Memory and Atomic Requests, this field sup‐<br>ports address translation for virtualized systems.<br>The translation protocol is described in a separate<br>spec called_Address Translation Services_, where it can<br>be seen that the field encodes as:<br>00 = Default/Untranslated<br>01 = Translation Request<br>10 = Translated<br>11 = Reserved|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|TLP data payload transfer size, in DW. Encoding:<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|Last DW<br>Byte Enables<br>[3:0]|Byte 7 Bit 7:4|These four high‐true bits map one‐to‐one to the<br>bytes within the last double word of payload.<br>Bit 7 = 1: Byte 3 in last DW is valid; otherwise not<br>Bit 6 = 1: Byte 2 in last DW is valid; otherwise not<br>Bit 5 = 1: Byte 1 in last DW is valid; otherwise not<br>Bit 4 = 1: Byte 0 in last DW is valid; otherwise not|
|First DW<br>Byte Enables<br>[3:0]|Byte 7 Bit 3:0|These four high‐true bits map one‐to‐one to the<br>bytes within the first double word of payload.<br>Bit 3 = 1: Byte 3 in first DW is valid; otherwise not<br>Bit 2 = 1: Byte 2 in first DW is valid; otherwise not<br>Bit 1 = 1: Byte 1 in first DW is valid; otherwise not<br>Bit 0 = 1: Byte 0 in first DW is valid; otherwise not|



## **Generic Header Field Details** 

In the following sections, we describe details of each TLP Header field depicted in Figure 5‐3 on page 175. 

**178** 

**Chapter 5: TLP Elements** 

## **Header** _**Type/Format**_ **Field Encodings** 

Table 5‐3 on page 179 summarizes the encodings used in TLP header Type and Format (Fmt) fields. 

_Table 5‐3: TLP Header Type and Format Field Encodings_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Memory Read Request (MRd)|000 = 3DW, no data<br>001 = 4DW, no data|0 0000|
|Memory Read Lock Request (MRdLk)|000 = 3DW, no data<br>001 = 4DW, no data|0 0001|
|Memory Write Request (MWr)|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 0000|
|IO Read Request (IORd)|000 = 3DW, no data|0 0010|
|IO Write Request (IOWr)|010 = 3DW, w/ data|0 0010|
|Config Type 0 Read Request (CfgRd0)|000 = 3DW, no data|0 0100|
|Config Type 0 Write Request (CfgWr0)|010 = 3DW, w/ data|0 0100|
|Config Type 1 Read Request (CfgRd1)|000 = 3DW, no data|0 0101|
|Config Type 1 Write Request (CfgWr1)|010 = 3DW, w/ data|0 0101|
|Message Request (Msg)|001 = 4DW, no data|1 0 rrr*<br>(see routing field)|
|Message Request W/Data (MsgD)|011 = 4DW, w/ data|1 0rrr*<br>(see routing field)|
|Completion (Cpl)|000 = 3DW, no data|0 1010|
|Completion W/Data (CplD)|010 = 3DW, w/ data|0 1010|
|Completion‐Locked (CplLk)|000 = 3DW, no data|0 1011|
|Completion W/Data (CplDLk)|010 = 3DW, w/ data|0 1011|
|Fetch and Add AtomicOp Request|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 1100|



**179** 

**PCI Ex ress Technolo p gy** 

_Table 5‐3: TLP Header Type and Format Field Encodings (Continued)_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Unconditional Swap AtomicOp<br>Request|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 1101|
|Compare and Swap AtomicOp<br>Request|010 = 3DW, w/ data<br>011 = 4DW, w/ data|0 1110|
|Local TLP Prefix|100 = TLP Prefix|0L3L2L1L0|
|End‐to‐End TLP Prefix|100 = TLP Prefix|1E3E2E1E0|



## **Digest / ECRC Field** 

The TLP Digest bit reports the presence of the End‐to‐End CRC (ECRC). If this optional feature is supported and enabled by software, devices calculate and apply an ECRC for all TLPs they originate. Note that using ECRC requires devices to include the optional Advanced Error Reporting registers, since the capability and control registers for it are located there. 

**ECRC Generation and Checking.** ECRC covers all fields that do not change as the TLP is forwarded across the fabric. However, there are two bits that can legally change as a packet makes its way across a topology: 

- **Bit 0 of the Type field** — changes when a configuration transaction is for‐ warded across a bridge and changes from a type 1 to a type 0 configuration transaction because it has reached the targeted bus. This is accomplished by changing bit 0 of the type field. 

- **Error/Poisoned (EP) bit** — this can change as a TLP traverses the fabric if the data associated with the packet is seen as corrupted. This is an optional feature referred to as error forwarding. 

**Who Checks ECRC?** The intended target of an ECRC is the ultimate recipi‐ ent of the TLP. Checking the LCRC verifies no transmission errors across a given Link, but that gets recalculated for the packet at the egress port of a rout‐ ing element (Switch or Root Complex) before being forwarded to the next Link, which could mask an internal error in the routing element. To protect against that, the ECRC is carried forward unchanged on its journey between the Requester and Completer. When the target device checks the ECRC, any error possibilities along the way have a high probability of being detected. 

**180** 

**Chapter 5: TLP Elements** 

The spec makes two statements regarding a Switch’s role in ECRC checking: 

- A Switch that supports ECRC checking performs this check on TLPs des‐ tined to a location within the Switch itself. “On all other TLPs a Switch must preserve the ECRC (forward it untouched) as an integral part of the TLP.” 

- “Note that a Switch may perform ECRC checking on TLPs passing through the Switch. ECRC Errors detected by the Switch are reported in the same way any other device would report them, but do not alter the TLPs passage through the Switch.” 

## **Using Byte Enables** 

**General.** Like PCI, PCIe needs a mechanism to reconcile its DW‐aligned addresses with the need, at times, for transfer sizes or starting/ending addresses that are not DW aligned. Toward this end, PCI Express makes use of the two Byte Enable fields introduced earlier in Figure 5‐3 on page 175 and in Table 5‐2 on page 176. The First DW Byte Enable field and the Last DW Byte Enable fields allow the Requester to qualify the bytes of interest within the first and last dou‐ ble words transferred. 

## **Byte Enable Rules** 

1. Byte enable bits are high true. A value of 0 indicates the corresponding byte in the data payload should not be used by the Completer. A value of 1 indi‐ cates it should. 

2. If the valid data is all within a single double word, the Last DW Byte enable field must be = 0000b. 

3. If the header Length field indicates a transfer is more than 1DW, the First DW Byte Enable must have at least one bit enabled. 

4. If the Length field indicates a transfer of 3DW or more, then the First DW Byte Enable field and the Last DW Byte Enable field must have contiguous bits set. In these cases, the Byte Enables are only being used to give the byte offset of the effective starting and ending address from the DW‐aligned address. 

5. Discontinuous byte enable bit patterns in the First DW Byte enable field are allowed if the transfer is 1DW. 

6. Discontinuous byte enable bit patterns in both the First and Second DW Byte enable fields are allowed if the transfer is between one and two DWs. 

7. A write request with a transfer length of 1DW and no byte enables set is legal, but has no effect on the Completer. 
