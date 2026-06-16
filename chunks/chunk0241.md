|Type [4:0]|Byte 0 Bit 4:0|Packet type is 01010b for Completions.|



**197** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐7: Completion Header Fields (Continued)_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Completions must use the same value<br>here as the corresponding Request.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|Indicates whether ID‐based Ordering is<br>to be used for this TLP. To learn more,<br>see “ID Based Ordering (IDO)” on<br>page 301.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|Reserved for Completions.|
|TD<br>(TLP Digest)|Byte 2 Bit 7|If = 1, indicates the presence of a<br>digest field at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|If = 1, indicates the data payload is poi‐<br>soned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Completions must use the same values<br>here as the corresponding Request.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type is reserved for Comple‐<br>tions and must be zero, but Receivers<br>are not required or even encouraged to<br>check this.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW. For<br>Completions, this field reflects the size<br>of the data payload associated with this<br>completion.|
|Completer ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Completer to support<br>debugging problems.<br>Byte 4 7:0 = Completer Bus #<br>Byte 5 7:3 = Completer Dev #<br>Byte 5 2:0 = Completer Function #|



**198** 

**Chapter 5: TLP Elements** 

_Table 5‐7: Completion Header Fields (Continued)_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Compl. Status [2:0]<br>(Completion Status<br>Code)|Byte 6 Bit 7:5|These bits indicate status for this Com‐<br>pletion.<br>000b = Successful Completion (SC)<br>001b = Unsupported Request (UR)<br>010b = Config Req Retry Status (CRS)<br>100b = Completer abort (CA)<br>All other codes are reserved. See “Sum‐<br>mary of Completion Status Codes” on<br>page 200.|
|BCM<br>(Byte Count Modified)|Byte 6 Bit 4|This is only used by PCI‐X Completers<br>and indicates that the Byte Count field<br>reports only the first payload rather<br>than the total payload remaining. See<br>“Using The Byte Count Modified Bit”<br>on page 201.|
|Byte Count [11:0]|Byte 6 Bit 3:0<br>Byte 7 Bit 7:0|Byte count remaining to satisfy a read<br>request, as derived from the original<br>request Length field. See “Data<br>Returned For Read Requests:” on<br>page 201 for special cases caused by<br>multiple completions.|
|Requester ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|Copied from the Request for use as the<br>return address (target) for this Comple‐<br>tion.<br>Byte 8, 7:0 = Requester Bus #<br>Byte 9, 7:3 = Requester Device #<br>Byte 9, 2:0 = Requester Function #|
|Tag [7:0]|Byte 10 Bit 7:0|This must be the Tag value received<br>with the Request. Requester associates<br>this Completion with a pending<br>Request based on the Tag.|



**199** 

**PCI Ex ress Technolo p gy** 

_Table 5‐7: Completion Header Fields (Continued)_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Lower Address [6:0]|Byte 11 Bit 6:0|The lower 7 bits of address for the first<br>data returned for a read request. Calcu‐<br>lated from Request Length and Byte<br>Enables, it assists buffer management<br>by showing how many bytes can be<br>transferred before reaching the next<br>Read Completion Boundary. See “Cal‐<br>culating Lower Address Field” on<br>page 200.|



## **Summary of Completion Status Codes.** 

- 000b (SC) Successful Completion: the Request was serviced properly. 

- 001b (UR) Unsupported Request: Request is not legal or was not recognized by the Completer. This is an error condition but how the Completer responds depends on the spec revision to which it was designed. Before the 1.1 spec, this were considered an uncorrectable error, but for 1.1 and later it’s treated as an Advisory Non‐Fatal Error. See the “Unsupported Request (UR) Status” on page 663 for details. 

- 010b (CRS) Configuration Request Retry Status: Completer is temporarily unable to service a configuration request, and the request should be attempted again later. 

- 100b (CA) Completer Abort: Completer should have been able to service the request but has failed for some reason. This is an uncorrectable error. 

**Calculating The Lower Address Field .** This field is set up by the Com‐ pleter to reflect the byte‐aligned address of the first enabled byte of data being returned in the Completion payload. Hardware calculates this by considering both the DW start address and the Byte Enable pattern in the First DW Byte Enable field provided in the original request. 

For Memory Read Requests, the address is an offset from the DW start address: 

- If the First DW Byte Enable field is 1111b, all bytes are enabled in the first DW and the offset is 0. This field matches the DW‐aligned start address. 

- If the First DW Byte Enable field is 1110b, the upper three bytes are enabled in the first DW and the offset is 1. This field is the DW start address + 1. 

- If the First DW Byte Enable field is 1100b, the upper two bytes are enabled 

**200** 

**Chapter 5: TLP Elements** 

- in the first DW and the offset is 2. This field is the DW start address + 2. 

- • If the First DW Byte Enable field is 1000b, only the upper byte is enabled in the first DW and the offset is 3. This field is the DW start address + 3. 

Once calculated, the lower 7 bits are placed in the Lower Address field of the Completion header to facilitate the case in which the read completion is smaller than the entire payload and needs to stop at the first RCB. Breaking a transac‐ tion must be done on RCBs, and the number of bytes transferred to reach the first one is based on start address. 

For AtomicOp Completions, the Lower Address field is reserved. For all other Completion types, it’s set to zero. 

**Using The Byte Count Modified Bit.** This bit is only set by PCI‐X Com‐ pleters, but they could exist in a PCIe topology if a bridge from PCIe to PCI‐X is used. Rules for its assertion include: 

1. It’s only set by a PCI‐X Completer if a read request is going to be broken into multiple completions. 

2. It’s only set for the first Completion of the series, and only then to indicate that the first Completion contains a Byte Count field that reflects the first Completion payload rather than the total remaining (as it normally would). The Requester understands that, even though the Byte Count appears to show that this is the last Completion for this request, this Completion will instead be followed by others to satisfy the original request as required. 

3. For subsequent Completions in the series, the BCM bit must be deasserted and the Byte Count field will reflect the total remaining count as it normally would. 

4. Devices receiving Completions with the BCM bit set must interpret this case properly. 

5. The Lower Address field is set by the Completer during completions with data to reflect the address of the first enabled byte of data being returned 

## **Data Returned For Read Requests:** 

1. A read request may require multiple completions to be fulfilled, but total data transfer must eventually equal the size of original request, or a Com‐ pletion Timeout error will probably result. 

2. A given Completion can only service one Request. 

3. IO and Configuration reads are always 1 DW, and will always be satisfied with a single Completion 

4. A Completion with a Status Code other than SC (successful) terminates a transaction. 

**201** 

## **PCI Ex ress Technolo p gy** 

5. The Read Completion Boundary (RCB) must be observed when handling a read request with multiple completions. The RCB is 64 bytes or 128 bytes for the Root Complex, since it is allowed to modify the size of packets flow‐ ing between its ports, and the value used is visible in a configuration regis‐ ter. 

6. Bridges and endpoints may implement a bit for selecting the RCB size (64 or 128 bytes) under software control. 

7. Completions that are entirely within an aligned RCB boundary must com‐ plete in one transfer, since the transfer won’t reach the RCB, which is the only place it can legally stop early. 

8. Multiple Completions for a single read request must return data in increas‐ ing address order. 

## **Receiver Completion Handling Rules:** 

1. A received Completion that doesn’t match a pending request is an Unex‐ pected Completion and treated as an error. 

2. Completions with a completion status other than SC or CRS will be handled as errors and buffer space associated with them will be released. 

3. When the Root Complex receives a CRS status during a configuration cycle, the request is terminated. What happens next is implementation specific, but if the Root supports it, the action is defined by the setting of its CRS Software Visibility bit in the Root Control register. 

   - If CRS Software Visibility is not enabled, the Root will reissue the config request for an implementation‐specific number of times before giving up and concluding the target has a problem. 

   - If CRS Software Visibility is enabled, software designed to support it will always read both bytes of the Vendor ID field first. If the hardware then receives a CRS for that Request, it returns the value 0001h for the Vendor ID. This value, reserved for this use by the PCI‐SIG, doesn’t cor‐ respond to any valid Vendor ID and informs software about this event. This allows software to go on to some other task while waiting for the target to become ready (which could take as long as 1 second after reset) rather than being stalled. Any other config read or write will simply be automatically retried by the Root as a new Request for the design‐spe‐ cific number of iterations. 

4. A CRS status in response to a request other than configuration is illegal and may be reported as a Malformed TLP. 

5. Completions with status = reserved code are treated as if the code was UR. 6. If a Read Completion or an AtomicOp Completion is received with a status other than SC, no data is included with the completion and the Requester must consider this Request terminated. How the Requester handles this case is implementation‐specific. 

**202** 

**Chapter 5: TLP Elements** 

7. In the event multiple completions are being returned for a read request, a completion status other than SC ends the transaction. Device handling of data received prior to the error is implementation‐specific. 

8. For compatibility with PCI, a Root Complex may be required to synthesize a read value of all “1’s” when a configuration cycle ends with a completion indicating an Unsupported Request. This is analogous to a PCI Master Abort that happens when enumeration software attempts to read from devices that are not present. 

## **Message Requests** 

Message Requests replace many of the interrupt, error, and power management sideband signals used on PCI and PCI‐X. All Message Requests use the 4DW header format, but not all of the fields are used in every Message type. Fields in bytes 8 through 15 are not defined for some Messages and are reserved for those cases. Messages are treated much like posted Memory Write transactions but their routing can be based on address, ID, and in some cases the routing can be implicit. The _routing subfield_ (Byte 0, bits 2:0) in the packet header indicates which routing method is used and which additional header registers are defined. The general Message Request header format is shown in Figure 5‐11 on page 203. 

_Figure 5‐11: 4DW Message Request Header Format_ 
