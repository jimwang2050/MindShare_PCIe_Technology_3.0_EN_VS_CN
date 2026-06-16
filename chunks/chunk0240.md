|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|Indicates whether TLP Hints have<br>been included. See “TPH (TLP Pro‐<br>cessing Hints)” on page 899 for a dis‐<br>cussion on these hints.|



**189** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐5: 4DW Memory Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**||**Function**|
|---|---|---|---|
|TD<br>(TLP Digest)|Byte 2 Bit 7||If 1, the optional TLP Digest field is<br>included with this TLP.<br>Some rules<br>:<br>The presence of the Digest field must<br>be checked by all receivers (using this<br>bit)<br>• TLPs with TD = 1 but no Digest<br>field are treated as Malformed.<br>• If the TD bit is set, recipient must<br>perform the ECRC check if enabled.<br>• If a Receiver doesn’t support the<br>optional ECRC checking, it must<br>ignore the digest field.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6||If 1, the data accompanying this<br>packet should be considered to have<br>an error although the transaction is<br>allowed to complete normally.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4||Bit 5=Relaxed ordering<br>.<br>When set = 1, PCI‐X relaxed ordering<br>is enabled for this TLP. Otherwise,<br>strict PCI ordering is used.<br>Bit 4=No Snoop<br>.<br>If 1, system hardware is not required<br>to cause processor cache snoop for<br>coherency for this TLP. Otherwise,<br>cache snooping is required.|
|Address Type [1:0]|Byte 2 Bit 3:2||This field supports address transla‐<br>tion for virtualized systems. The<br>translation protocol is described in a<br>separate spec called_Address Transla‐_<br>_tion Services_, where it can be seen that<br>the field encodes as:<br>00 = Default/Untranslated<br>01 = Translation Request<br>10 = Translated<br>11 = Reserved|



**190** 

**Chapter 5: TLP Elements** 

_Table 5‐5: 4DW Memory Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|TLP data payload transfer size, in<br>DW. Maximum size is 1024 DW<br>(4KB), encoded as:<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies a Requester’s return<br>address for a completion:<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These identify each outstanding<br>request issued by the Requester.<br>By default only bits 4:0 are used,<br>allowing up to 32 requests to be in<br>progress at a time. If the Extended<br>Tag bit in the Control Register is set,<br>then all 8 bits may be used (256 tags).|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These qualify bytes within the last<br>DW of data transferred.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These qualify bytes within the first<br>DW of the data payload.|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|The upper 32 bits of the 64‐bit start<br>address for the memory transfer.|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|The lower 32 bits of the 64 bit start<br>address for the memory transfer. The<br>lower two bits of the address are<br>reserved, forcing a DW‐aligned start<br>address.|



**191** 

## **PCI Ex ress Technolo p gy** 

**Memory Request Notes.** Features of memory requests include: 

1. Memory data transfers are not permitted to cross a 4KB boundary. 

2. All memory‐mapped writes are posted to improve performance. 

3. Either 32‐ or 64‐bit addressing may be used. 

4. Data payload size is between 0 and 1024 DW (0‐4KB). 

5. Quality of Service features may be used, including up to 8 Traffic Classes. 

6. The No Snoop attribute can be used to relieve the system of the need to snoop processor caches when transactions target main memory. 

7. The Relaxed Ordering attribute may be used to allow devices in the packet’s path to apply the relaxed ordering rules in hopes of improving perfor‐ mance. 

## **Configuration Requests** 

PCI Express uses both Type 0 and Type 1 configuration requests the same way PCI did to maintain backward compatibility. A Type 1 cycle propagates down‐ stream until it reaches the bridge whose secondary bus matches the target bus. At that point, the configuration transaction is converted from Type 1 to Type 0 by the bridge. The bridge knows when to forward and convert configuration cycles based on the previously programmed bus number registers: Primary, Secondary, and Subordinate Bus Numbers. For more on this topic, refer to the section “Legacy PCI Mechanism” on page 91. 

**192** 

**Chapter 5: TLP Elements** 

_Figure 5‐9: 3DW Configuration Request And Header Format_ 

**==> picture [368 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Type 1<br> Configuration Request<br>Switch<br>Type 0<br> Configuration Request Configuration Request TLP<br>Framing Sequence Framing<br>PCIe Header Data Digest LCRC<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 1 0 xType R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Bus Number Device Func Rsvd Ext Reg Register R<br>Function Number with ARI Number Number<br>**----- End of picture text -----**<br>


In Figure 5‐9 on page 193, a Type 1 configuration cycle is shown making its way downstream, where it is converted to Type 0 by the bridge for that bus (accom‐ plished by changing bit 0 of the Type field). Note that, unlike PCI, only one device can reside downstream on a Link. Consequently, no IDSEL or other hardware indication is needed to tell the device that it should claim the Type 0 cycle; any Type 0 configuration cycle a device sees on its Upstream Link will be understood as targeting that device. 

**Definitions Of Configuration Request Header Fields.** Table 5‐6 on page 194 describes the location and use of each field in the configuration request header illustrated in Figure 5‐9 on page 193. 

**193** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐6: Configuration Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Always a 3DW header<br>000b = configuration read (no data)<br>010b = configuration write (with data)|
|Type [4:0]|Byte 0 Bit 4:0|00100b = Type 0 Config Request<br>00101b = Type 1 Config Request|
|TC [2:0]<br>(Transfer Class)|Byte 1 Bit 6:4|Traffic Class must be zero for Configu‐<br>ration requests, ensuring that these<br>packets will never interfere with any<br>high‐priority packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|These bits are reserved and must be<br>zero for Config Requests.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||
|TD<br>(TLP Digest)|Byte 2 Bit 7|Indicates the presence of a digest field<br>(1 DW) at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|Indicates that data payload is poi‐<br>soned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Relaxed Ordering and No Snoop bits<br>are both always = 0 in configuration<br>requests.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type is reserved for config<br>requests and must be zero.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Data payload size in DW is always = 1<br>for configuration requests. Byte<br>Enables qualify bytes within the DW<br>and any combination is legal.|



**194** 

**Chapter 5: TLP Elements** 

_Table 5‐6: Configuration Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester’s return<br>address for a completion:<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These bits identify outstanding request<br>issued by the requester. By default,<br>only bits 4:0 are used (32 outstanding<br>transactions at a time), but if the<br>Extended Tag bit in the Control Regis‐<br>ter is set = 1, then all 8 bits may be used<br>(256 tags).|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These qualify bytes in the last data DW<br>transferred. Since config requests can<br>only be one DW in size, these bits must<br>be zero.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These high‐true bits qualify bytes in<br>the first data DW transferred. For con‐<br>fig requests, any bit combination is<br>valid (including none active).|
|Completer ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|Identifies the completer being accessed<br>with this configuration cycle.<br>Byte 8, 7:0 = Bus Number<br>Byte 9, 7:3 = Device Number<br>Byte 9, 2:0 = Function Number|
|Ext Register Number<br>[3:0]<br>(Extended Register<br>Number)|Byte 10 Bit 3:0|These provide the upper 4 bits of DW<br>space for accessing the extended con‐<br>fig space. They’re combined with Reg‐<br>ister Number to create the 10‐bit<br>address needed to access the 1024 DW<br>(4096 byte) space. For PCI‐compatible<br>config space, this field must be zero.|



**195** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐6: Configuration Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Register Number [5:0]|Byte 11 Bit 7:0|As the lower 8 bits of configuration<br>DW space, these specify the register<br>number. The two lowest bits are<br>always zero, forcing DW‐aligned<br>accesses.|



**Configuration Request Notes.** Configuration requests always use the 3DW header format and are routed based on the target Bus, Device and Func‐ tion numbers. All devices “capture” their Bus and Device Number from the tar‐ get numbers in the Request whenever they receive a Type 0 configuration write cycle. The reason for that is because they’ll need it later to use as their Requester ID when they send requests of their own in the future. 

## **Completions** 

Completions are expected in response to non‐posted Request, unless errors pre‐ vent them. For example Memory, IO, or Configuration Read requests usually result in Completions with data. On the other hand, IO or Configuration Write requests usually result in a completion without data that merely reports the sta‐ tus of the transaction. 

Many fields in the Completion use the same values as the associated request, including Traffic Class, Attribute bits, and the original Requester ID (used to route the completion back to the Requester). Figure 5‐10 on page 197 shows a completion returned for a non‐posted request, and the 3DW header format it uses. Completions also supply the Completer ID in the header. Completer ID is not interesting during normal operation, but knowing where the Completion came from could be useful for error diagnosis during system debug. 

**196** 

**Chapter 5: TLP Elements** 

_Figure 5‐10:  3DW Completion Header Format_ 

**==> picture [364 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Switch<br>Non-Posted<br>Request Completion TLP<br>PCIe Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 1 0 1 0Type R TC R Attr R TH0 DT EP Attr 0 0AT Length<br>Byte 4 Completer ID Compl.Status MCB Byte Count<br>Byte 8 Requester ID Tag R Lower Address<br>**----- End of picture text -----**<br>


**Definitions Of Completion Header Fields.** Table 5‐7 on page 197 describes the location and use of each field in a completion header. 

_Table 5‐7: Completion Header Fields_ 

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Format (always a 3DW header)<br>000b = Completion without data (Cpl)<br>010b = Completion with data (CplD)|