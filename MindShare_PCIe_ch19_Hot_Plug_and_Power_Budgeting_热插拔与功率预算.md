# 📘 第 19 章　热插拔与功率预算 (Chapter 19. Hot Plug and Power Budgeting)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0344.md` ... `chunks/chunk0346.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Hot Plug and Power Budgeting](#-本章目录-table-of-contents)

<a id="sec-19-1"></a>
## 19.1 Hot Plug and Power Budgeting | 热插拔与功率预算

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

This 64‐bit register is a bit vector that indicates for which of the 64 MCGs this Function should accept a copy or this Port should forward a copy. If the MCG value is found to be 47, for example, and bit 47 is set in this register, then this Function should receive it or this Port should forward it. 

## **MC Block All** 

This 64‐bit register indicates which MCGs an Endpoint Function is blocked from sending and which a Switch or Root Port is blocked from forwarding. This can be programmed in a Switch or Root Port to prevent it from forwarding Mul‐ tiCast TLPs to an Endpoint that doesn’t understand them, for example. A blocked TLP is considered an error condition, and how the error is handled is described in the next section. 

## **MC Block Untranslated** 

The meaning and use of this 64‐bit register is almost identical to the Block All register except that it doesn’t apply to TLPs whose AT header field shows them to be translated. This mechanism can be used to set up a Multicast window that is protected in that it can only receive translated addresses. 

If a TLP is blocked because of the setting of either of these two blocking regis‐ ters, it’s handled as an MC Blocked TLP, meaning it gets dropped and the Port 

**892** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

or Function logs and signals this as an error. Logging the error involves setting the Signaled Target Abort bit in its Status register or its Secondary Status regis‐ ter, as appropriate. That’s barely enough information to be useful, though, so the spec highly recommends that Advanced Error Reporting (AER) registers be implemented in Functions with Multicast capability to facilitate isolating and diagnosing faults. 

The spec notes that this register is required in all Functions that implement the MC Capability registers, but if an Endpoint Function doesn’t implement the ATS (Address Translation Services) registers, the designer may choose to make these bits reserved. 

## **Multicast Example** 

At this point, an example will help to illustrate how these registers can be used to set up a multicast environment. To set this up, let’s first give the relevant reg‐ isters some values: 

- MC_Base_Address = 2GB (Starting address for the multicast range) 

- MC_Max_Group = 7 (Meaning 8 windows are possible for this design) 

- MC_Window_Size_Requested = 10 (Meaning 2[10] or 1KB size was requested by an Endpoint) 

- MC_Index_Position = 12 (Meaning the actual size of each window is 2[12] ) 

- MC_Num_Group = 5 (Meaning software only configured 6 of the available multicast windows). 

Based on those register settings, the image in Figure 20‐7 on page 894 illustrates the result. The multicast window range is shown starting at 2GB and ranging as high as 2GB + 8 * (the window size). However, only 6 are enabled by software, so the actual multicast address range is from 2GB to 2GB + 24KB. The windows are all the same size and correspond to the MCGs: MCG 0 is the first window, 1 is the next window, and so on. 

**893** 

**PCI Ex ress Technolo p gy** 

_Figure 20‐7: Multicast Address Example_ 

**==> picture [370 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Memory Map<br>MC Address Range<br>= 2GB to 2GB + 2 [12] * 6<br>= 2GB to 2GB + 24KB<br>8 MC windows available in<br>2GB + 24KB<br>MC Group 5 hardware, each at least 2 [10]<br>Only 6 MC windows are  MC Group 4MC Group 3 in size (technically, 2 [12] is<br>configured for use MC Group 2MC Group 1 min. address granularity)<br>2GB MC Group 0 MC_Base_Address<br>**----- End of picture text -----**<br>


## **MC Overlay BAR** 

This last set of registers are required for Switch and Root Ports that implement Multicasting, but they’re not implemented in Endpoints. The motivation for this BAR is that it allows two special cases. First, a Port can forward TLPs down‐ stream if they hit in a multicast window even if the Endpoint wasn’t designed for multicasting. Second, a Port can forward multicast TLPs upstream to system memory. In both cases, this is accomplished by replacing part of the Request’s address with an address that will be recognized by the target. Doing so allows a single BAR in a component to serve as a target for both unicast and multicast writes even if it wasn’t designed with multicast capability. 

As shown in Figure 20‐8 on page 895, this register block consists of an address that will be overlaid onto the outgoing TLP, and a 6‐bit Overlay Size indicator. The size referred to here is simply the number of bits from the original 64‐bit address that will be retained, while all the others will be replaced by the Over‐ lay BAR bits. The spec mistakenly refers to this in at least one place as the size in bytes, but in other places it’s made clear that it is a bit number. Note that the overlay size value must be 6 or higher to enable the overlay operation. If the size is given as 5 or lower, no overlay will take place and the address is unchanged. 

**894** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐8: Multicast Overlay BAR_ 

**==> picture [287 x 91] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 6   5 0<br>MC_Overlay<br>MC_Overlay_BAR [31:6]<br>_Size<br>MC_Overlay_BAR [63:32]<br>**----- End of picture text -----**<br>


## **Overlay Example** 

Now consider the case in which an address overlay is desired, as shown in Fig‐ ure 20‐9 on page 896. Here the address of a TLP to be forwarded, ABCD_BEEFh, falls within the defined multicast range (also referred to as a multicast hit) and the egress Port has been configured with valid values in the Overlay BAR. 

The overlay case creates the unusual situation with the ECRC value that was mentioned earlier in the description of the Multicast Capability register. If the TLP whose address is being changed by the overlay includes an ECRC, that value would be rendered incorrect by this change. Switches and Root Ports optional support regenerating the ECRC based on the new address so that it still serves its purpose going forward. If the routing agent does not support it, the ECRC is simply dropped and the TD header bit is forced to zero to avoid any confusion. 

A potential problem can arise with ECRC regeneration. If the incoming TLP already had an error but the ECRC value is regenerated because the address was modified, that would inadvertently hide the original error. To avoid that, the routing agent must verify the original ECRC first. If it finds an error, it must force a bad ECRC on the outgoing TLP by inverting the calculated ECRC value before appending it to ensure that the target will see it as an error condition. 

**895** 

**PCI Ex ress Technolo p gy** 

_Figure 20‐9: Overlay Example_ 

**==> picture [315 x 268] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Memory Map<br>PCIe BAR Range Overlaid Address:<br>FEED_0000  FEED_BEEFh<br>to FEED_FFFF<br>Original Address:<br>ABCD_BEEFh<br>Multicast Address<br>Range<br>**----- End of picture text -----**<br>


## **Routing Multicast TLPs** 

When a Switch or Root Port detects an MC hit (address falls within the MC range) normal routing is suspended. The MCG is extracted from the address and is compared to the MC_Receive register of all the Ports to see which of them should forward a copy of this TLP. Ports whose corresponding Receive register bit is set will forward a copy of the TLP unless their corresponding MC Blocked register bit is also set. If no Ports forward the TLP and no Functions consume it, it is silently dropped. To prevent loops, a TLP is never forwarded back out on its ingress Port, with the possible exception of an ACS case. 

Endpoints extract the MCG and compare it with their Receive register. If there’s no match, the TLP is silently dropped. If the Endpoint doesn’t support Multi‐ casting, it will treat the TLP as having an ordinary address. 

**896** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

## **Congestion Avoidance** 

The use of Multicasting will increase the amount of system traffic in proportion to the percentage of MC traffic, which leads to the risk of packet congestion. To avoid creating backpressure, MC targets should be designed to accept MC traf‐ fic “at speed”, meaning with minimal delay. To avoid oversubscribing the Links, MC initiators should limit their packet injection rate. A system designer would be wise to choose components carefully to handle this. For example, using Switches and Root Ports whose buffers are big enough to handle the expected traffic, and Endpoints that are able to accept their incoming MC pack‐ ets quickly enough to avoid trouble. 

## **Performance Improvements** 

System performance is enhanced with the addition of four new features: 

1. AtomicOps to replace the legacy transaction locking mechanism 

2. TLP Processing Hints to allow software to suggest caching options 

3. ID‐Based Ordering to avoid unnecessary latency 

4. Alternative Routing‐ID Interpretation to increase the number of Functions available in a device. 

## **AtomicOps** 

Processors that share resources or otherwise communicate with each other sometimes need uninterrupted, or “atomic”, access to system resources to do things like testing and setting semaphores. On parallel processor buses this was accomplished by locking the bus with the assertion of a Lock pin until the origi‐ nator completed the whole sequence (a read followed by a write), during which time other processors were not allowed to initiate transactions on the bus. PCI included a Locked pin to apply this same model on the PCI bus as on the pro‐ cessor bus, allowing this protocol to used with peripheral devices. 

This model worked but was slow on the shared processor bus and even worse when going onto the PCI bus. That’s one reason why PCIe limited its use only to Legacy devices. However, the increasing use of shared processing in today’s PCs, such as graphics co‐processors and compute accelerators, has brought this issue back to the fore because the different compute engines need to be able to share an atomic protocol. The way this problem was resolved on PCIe was to introduce three new commands that can each do a series of things atomically 

**897** 

## **PCI Ex ress Technolo p gy** 

within the target device rather than requiring a series of separate uninterrupt‐ able commands on the interface. These new commands, called AtomicOps, are: 

1. FetchAdd (Fetch and Add) ‐ This Request contains an “add” value. It reads the target location, adds the “add”value to it, stores the result in the target location and returns the original value of the target location. This could be used in support of atomically updating statistics counters. 

2. Swap (Unconditional Swap) ‐ This Request contains a “swap” value. It reads the target location, writes the “swap” value into it, and returns the original target value. This could be useful for atomically reading and clear‐ ing counters. 

3. CAS (Compare and Swap) ‐ This Request contains both a “compare” value and a “swap” value. It reads the target location, compares it against the “compare” value and, if they’re equal, writes in the “swap” value. Finally, it returns the original value of the target location. This can be useful as a “test and set” mechanism for managing semaphores.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-19-2"></a>
## 19.2 Hot Plug and Power Budgeting | 热插拔与功率预算

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Both Endpoints and Root Ports are optionally allowed to act as AtomicOp Requesters and Completers, which might seem unexpected because, in PCs at least, this kind of transaction is usually only initiated by the central processor. But modern systems can include an Endpoint acting as a co‐processor, in which case it would need to be able to use AtomicOps to properly handle the protocol. All three commands support 32‐bit and 64‐bit operands, while CAS also sup‐ ports 128‐bit operands. The actual size in use will be given in the Length field in the header. Routing elements like Switch Ports and Root Ports with peer‐to‐peer access will need to support the AtomicOp routing capability to be able to recog‐ nize and route these Requests. 

A question naturally arises as to how the system (Root Complex) will be instructed to generate these new commands in response to processor activity, since there may not be a directly‐analogous processor bus command. The spec suggests two approaches. First, the Root could be designed to recognize specific processor activity and interpret that to “export” a PCIe AtomicOp in response. Second, a register‐based approach similar to the one used for legacy Configura‐ tion access could be used. In that case, one register might give the target address while another specified which command should be generated and the combina‐ tion of the two would generate the Request. 

AtomicOp Completers can be identified by the presence of the three new bits in the Device Capabilities 2 register, as shown in Figure 20‐10 on page 899. Bit 6 of this register also identifies whether routing elements are capable of routing AtomicOps. 

**898** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

Legacy PCI does not comprehend AtomicOps, of course, and there is no straight‐forward way to translate them into PCI commands. For that reason, PCIe‐to‐PCI bridges do not support AtomicOps. If atomic access is needed on that bus it would have to be done with the legacy locked protocol and the spec states that Locked Transactions and AtomicOps can operate concurrently on the same platform. 

_Figure 20‐10: Device Capabilities 2 Register_ 

**==> picture [356 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 22 21 20 19 14 13 12 11 10 9 8 7 6 5 4 3 0<br>RsvdP RsvdP<br>Max End-End<br>TLP Prefixes<br>End-End TLP<br>Prefix Supported<br>Extended Fmt<br>Field Supported<br>TPH Completer Supported<br>LTR Mechanism Supported<br>No RO-enabled PR-PR Passing<br>128-bit CAS Completer Supported<br>64-bit AtomicOp Completer Supported<br>32-bit AtomicOp Completer Supported<br>AtomicOp Routing Supported<br>ARI Forwarding Supported<br>Completion Timeout Disable Supported<br>Completion Timeout Ranges Supported<br>**----- End of picture text -----**<br>


## **TPH (TLP Processing Hints)** 

Adding hints about how the system should handle TLPs targeting memory space can improve latency and traffic congestion. The spec describes this special handling basically as providing information about which of several possible cache locations in the system would be the optimal place for a temporary copy 

**899** 

**PCI Ex ress Technolo p gy** 

of a TLP. The spec makes note of the fact that, since the usage described for TPH relates to caching, it wouldn’t usually make sense to use them with TLPs target‐ ing Non‐prefetchable Memory Space. If such usage was needed, it would be essential to somehow guarantee that caching such TLPs did not cause undesir‐ able side effects. 

## **TPH Examples** 

**Device Write to Host Read.** To help clarify the motivation for TPH, con‐ sider the example shown in Figure 20‐11 on page 901. Here the Endpoint is writing data into memory for later use by the CPU. The sequence is as follows: 

1. First, the Endpoint sends a memory write TLP containing an address that maps to the system memory. The packet gets routed to the Root Complex (RC). 

2. The RC recognizes this as an access to a cacheable memory space and pauses its progress while it snoops the CPU cache. This may result in a write‐back cycle from the CPU to update the system memory before the transaction can proceed, and this is shown as step 2a. 

3. Once any write backs have finished, the RC allows the write to update the system memory. 

4. At some point, the Endpoint notifies the CPU about data delivery. 

5. Finally, the CPU fetches the data from memory to complete the sequence. 

**900** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐11: TPH Example_ 

**==> picture [202 x 111] intentionally omitted <==**

**----- Start of picture text -----**<br>
4<br>2<br>e C)\ @ 5<br>2a<br>Roo! Complex @<br>3<br>1<br>lo [ |<br>**----- End of picture text -----**<br>


This sequence works but there’s an opportunity for performance improvement by adding an intermediate cache in the system. To illustrate this, consider the example shown in Figure 20‐12 on page 902. From the perspective of the End‐ point, the operation is the same but the knows to handle it a differently. The steps now are as follows: 

1. The Endpoint does the same memory write but this time TPH bits are included. The write is forwarded to the RC by the Switch as before. 

2. The RC understands that this memory access must be snooped to the CPU as before. However, once the snoop has been handled, the RC is informed by the TPH bits to store this TLP in an intermediate cache rather than going to system memory. 

3. The Endpoint notifies the CPU that the data item has been delivered. 4. The CPU reads from the specified address, but now the data is found in the intermediate cache and so the request does not go to system memory. This has the usual benefits we’d expect from a cache design: faster access time as well as reduced traffic for the system memory. 

**901** 

**PCI Ex ress Technolo p gy** 

This is a simple Device Write to Host Read (DWHR) example to illustrate the concept but it wouldn’t be hard to imagine a more complex system with a much larger topology in which there could be other caches placed in Switches or other locations to achieve the same benefits for other targets. 

_Figure 20‐12: TPH Example with System Cache_ 

**==> picture [108 x 75] intentionally omitted <==**

**----- Start of picture text -----**<br>
3<br>2 4<br>OC @VlEl@<br>Rant Camnlayx<br>Cache<br>1<br>**----- End of picture text -----**<br>


**Host Write to Device Read.** To illustrate the concept going the other way (called Host Write to Device Read or HWDR), consider the example shown in Figure 20‐13 on page 903. In this example, the CPU initiates a memory write whose address targets the PCIe Endpoint in step one. The packet contains TPH bits that tell the RC that it should be stored in an intermediate cache near the target, instead of the cache in the RC that was used in the previous example. In this case a cache built into the Switch serves the purpose. The TLP is then for‐ warded on to the target Endpoint in step two. This model is beneficial when the data is updated infrequently but read often by the Endpoint. That allows sev‐ eral memory reads that would normally go to system memory to be handled by the cache instead, off loading both the Link from the Switch to the RC and the path to memory. 

**902** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐13: TPH Usage for TLPs to Endpoint_ 

**==> picture [353 x 326] intentionally omitted <==**

**----- Start of picture text -----**<br>
1<br>ox<br>oct Complex<br>Cache<br>rl i) i<br>PCle PCle<br>Cache<br>2<br>OWN: Endpoint Bridge<br>Yi i IN orto PCI-X PCI<br>§ EndpointPCle §§ EndpointLegacy PCI/PCI-X | |<br>Device to Device.  One last example is illustrated in Figure 20‐14 on page<br>904, where two Endpoints communicate with each other (called Device Read/<br>Write to Device Read/Write or D*D*) through a shared memory location that is<br>directed by TPH bits to an intermediate cache. In this case, both may update dif‐<br>ferent locations that they need to handle as “read mostly”, or one Endpoint may<br>update data that the other needs to read several times. In both cases, using the<br>intermediate cache improves system performance.<br>**----- End of picture text -----**<br>


**903** 

## **PCI Ex ress Technolo p gy** 

_Figure 20‐14: TPH Usage Between Endpoints_ 

**==> picture [34 x 9] intentionally omitted <==**

**----- Start of picture text -----**<br>
Cache<br>**----- End of picture text -----**<br>


## **TPH Header Bits** 

Several bits in the TLP header describe how the hints are used. First, as shown in the middle at the top of Figure 20‐15 on page 905, the TH (TLP Hints) bit reports whether the optional TPH bits are in use for the TLP. When set, the PH (Processing Hint bits) indicate the next level of information. 

**904** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐15: TPH Header Bits_ 

**==> picture [339 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- End of picture text -----**<br>


When the TH bit is set the PH bits, shown at the bottom right of Figure 20‐15 on page 905, take the place of what were the two reserved LSBs in the address field. For a 32‐bit address, these are byte 11 [1:0], while for the 64‐bit address shown, they are byte 15 [1:0]. Their encoding is described in Table 20‐1 on page 905. These hints are provided by the Requester based on knowledge of the data pat‐ terns in use, which is information that would be difficult for a Completer to deduce on its own. 

_Table 20‐1: PH Encoding Table_ 

|**PH [1:0]**|**Processing Hint**|**Usage Model**|
|---|---|---|
|00b|Bi‐directional data<br>structure|Indicates frequent read/write access by Host and<br>device.|
|01b|Requester|D*D* (device‐to‐device transfers). Indicates fre‐<br>quent read/write access by device. The asterisk<br>means either device could be reading or writing.|
|10b|Target|DWHR, HWDR (device‐to‐host or host‐to‐device<br>transfers). Indicates frequent read/write access by<br>Host.|
|11b|Target with Priority|Same as Target but with additional temporal<br>re‐use priority information. Indicates frequent<br>read/write access by Host and high temporal local‐<br>ity for accessed data.|



**905** 

## **PCI Ex ress Technolo p gy** 

The next level of information is the Steering Tag byte that provides system‐spe‐ cific information regarding the best place to cache this TLP. Interestingly, the location of this byte in the header varies depending on the Request type. For Posted Memory Writes the Tag field is repurposed to be the Steering Tag (no completion will be returned so the Tag isn’t needed), while for Memory Reads the two Byte Enable fields are repurposed for it (byte enables are not needed for pre‐fetchable reads). The meaning of the bits is implementation specific but they need to uniquely identify the location of the desired cache in the system. 

Two formats for TPH are described in the spec and this level of hint information (TH + PH + 8‐bit Steering Tag), called Baseline TPH, is the first and is required of all Requests that provide TPH. The second format uses TLP Prefixes to extend the Steering Tags (see “TLP Prefixes” on page 908 for more detail). 

## **Steering Tags**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-19-3"></a>
## 19.3 Hot Plug and Power Budgeting | 热插拔与功率预算

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

These values are programmed by software into a table to be used during normal operation. The spec recommends that the table be located in the TPH Requester Capability structure, shown in Figure 20‐16 on page 906, but it can alternatively be built into the MSI‐X table instead. Only one or the other of these table loca‐ tions can be used for a given Function. The location is given in the ST Table Location field [10:9] of the Requester Capability register, shown in Figure 20‐17 on page 907. The encoding of these 2 bits is shown in Table 20‐2 on page 907. 

_Figure 20‐16: TPH Requester Capability Structure_ 

|31|15|0<br>7|
|---|---|---|
|PCI Express Capabilities Register|Next Cap<br>Pointer|PCI Express<br>Cap ID (17h)|
|TPH Requester Capability Register|||
|TPH Requester Control Register|||
|TPH ST Table (optional)<br>(Sized by number of ST entries)|||



**906** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐17: TPH Capability and Control Registers_ 

**==> picture [340 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPH Requester Capability Register<br>31 27 26 16 15 11 10 9 8 7 3 2 1 0<br>RsvdP ST Table Size RsvdP RsvdP<br>ST Table Location<br>Extended TPH Requester Supported<br>Device-Specific Mode Supported<br>Interrupt Vector Mode Supported<br>No ST Mode Supported<br>TPH Requester Control Register<br>31 10 9 8 7 3 2 0<br>RsvdP RsvdP<br>TPH Requester Enable<br>ST Mode Select<br>**----- End of picture text -----**<br>


_Table 20‐2: ST Table Location Encoding_ 

|**Bits [10:9]**|**ST Table Location**|
|---|---|
|00b|Not present|
|01b|Located in the Requester Capa‐<br>bility structure|
|10b|Located in the MSI‐X table|
|11b|Reserved|



**907** 

**PCI Ex ress Technolo p gy** 

The Requester Capability register lists the number of entries in the ST Table in bits [26:16]. Each table entry is 2 bytes wide, and the ST Table implemented in the TPH Capability register set is shown in Figure 20‐18 on page 908, where entry zero is highlighted. The Requester Capability register also describes which ST Modes are supported for the Requester with the 3 LSBs: 

- **No ST** ‐ uses zeros for ST bits. Selected in the TPH Requester Control regis‐ ter’s ST Mode Select field when the value = 000b. 

- **Interrupt Vector** ‐ uses the interrupt vector number as the offset into the table, meaning the values are contained in the MSI‐X table. (ST Mode Select value = 001b.) 

- **Device‐Specific** ‐ uses a device‐specific method to offset into the ST Table in the TPH Capability structure because the ST values are located there. This is the recommended implementation, although how a given Request is associated with a particular ST entry is outside the scope of the spec. (ST Mode Select value = 010b.) 

- All other ST Mode Select encodings are reserved for future use. 

_Figure 20‐18: TPH Capability ST Table_ 

||31|24|23|16|15|8|7|0||
|---|---|---|---|---|---|---|---|---|---|
||ST Upper Entry (1)||ST|Lower Entry (1)|ST Upper Entry (0)||ST Lower Entry (0)|||
||ST Upper Entry (3)||ST|Lower Entry (3)|ST Upper Entry (2)||ST Lower Entry (2)|||
|||||||||||
|||ST Upper Entry|ST Lower Entry|||ST Upper Entry|ST Lower Entry|||
|||(Table Size)||(Table Size)||(Table Size - 1)|(Table Size - 1)|||
|||||||||||



## **TLP Prefixes** 

The Steering Tag bits can be extended with the addition of optional TLP Prefixes if needed. When one or more Prefixes are given with the TLP, the header reports it by setting the most significant bit in the Format field, as shown in Figure 20‐19 on page 909. 

**908** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐19: TPH Prefix Indication_ 

**==> picture [344 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>1  0 0 tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- End of picture text -----**<br>


## **IDO (ID-based Ordering)** 

Transaction ordering rules are important for proper traffic flow, but there are times when it’s not necessary and latencies can be improved in those cases. In particular, TLPs from different Requesters are very unlikely to have dependen‐ cies between them, so this feature allows software to enable them to be re‐ordered for improved performance. The details of this operation are described in the section called “ID Based Ordering (IDO)” on page 301. 

## **ARI (Alternative Routing-ID Interpretation)** 

The motivation for this optional feature is to increase the number of Function numbers available to Endpoints. Device numbers were useful in a shared‐bus architecture like PCI but are not usually needed in a point‐to‐point architecture. Consequently, the spec writers chose to allow devices to interpret the destina‐ tion for ID‐routed commands differently. This was accomplished by defining the Device number to always be zero and then allowing the Function number to use the 5 bits in the ID that were previously the Device number. Effectively, the Device number goes away while the Function number grows to 8 bits. The tar‐ get for a TLP that uses ARI will need to be enabled to recognize it before soft‐ ware can use this feature, but Routing elements in the path to it don’t have to be aware of this. They’re only looking at the bus number to determine the routing. 

**909** 

**PCI Ex ress Technolo p gy** 

## **Power Management Improvements** 

There are four additions that improve the system’s ability to manage power effectively, and they are listed here. All of these are covered in Chapter 16, enti‐ tled ʺPower Management,ʺ on page 703. 

## **DPA (Dynamic Power Allocation** 

A new set of extended configuration registers defines up to 32 sub‐states below D0. This allows software to easily make changes to a device’s power state with‐ out incurring the latency penalty of going all the way to the D1 device power state. To learn more on this, see “Dynamic Power Allocation (DPA)” on page 714 

## **LTR (Latency Tolerance Reporting)** 

Allowing Endpoints to report the latencies they can tolerate in response to their requests enables system software to make better choices regarding system response time and sleep states. To learn more about this, see “LTR (Latency Tol‐ erance Reporting)” on page 784. 

## **OBFF (Optimized Buffer Flush and Fill)** 

Similarly, allowing the system to report the preferred time slots during which Endpoints should or should not initiate DMA or interrupt traffic helps coordi‐ nate system sleep times and improve power management. For more on this, see “OBFF (Optimized Buffer Flush and Fill)” on page 776. 

## **ASPM Options** 

This change simply permits devices to support no ASPM Link power manage‐ ment if they choose to do so. In the previous spec versions, support for L0s was mandatory, but now it becomes optional. 

**910** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

## **Configuration Improvements** 

A few configuration registers were added to improve software visibility and control of devices. 

## **Internal Error Reporting** 

This is intended to provide a standardized way of reporting internal problems for devices like switches that don’t have a driver to handle that for them. It also adds the capability to track multiple TLP headers when they result in errors instead of just one as before. This topic is covered in the section on errors called “Internal Errors” on page 667. 

## **Resizable BARs** 

This new set of extended configuration registers allows devices that use a large amount of local memory to report whether they can work with smaller amounts and, if so, what sizes are acceptable. Software that knows to look for them can find the new registers, shown in Figure 20‐20 on page 912, and program them to give the appropriate memory size for the platform based on the competing requirements of system memory and other devices. 

A few rules apply to the use of these registers: 

1. To avoid confusion, a BAR size should only be changed when the Memory Enable bit has been cleared in the Command register. 

2. The spec strongly recommends that Functions not advertise BARs that are bigger than they can effectively use. 

3. To ensure optimal performance, software should allocate the biggest BAR size that will work for the system. 

**911** 

## **PCI Ex ress Technolo p gy** 

## _Figure 20‐20: Resizable BAR Registers_ 

**==> picture [363 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 20 19 16 15 0<br>Next Extended Version PCIe Extended Capability ID<br>Capability Offset (1h) (0015h for Resizable BAR)<br>31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>Resizable BAR Capability Register (0) 004h<br>Register Pair<br>for each  Reserved Resizable BAR Control Register (0) 008h<br>supported<br>BAR …<br>Resizable BAR Capability Register (n) n*8 +4<br>Reserved Resizable BAR Control Register (n) n*8 +8<br>**----- End of picture text -----**<br>


## **Capability Register** 

This register simply reports which BAR sizes will work for this Function. Bits 4 to 23 are used for this and the values are as shown here: 

- Bit 4 ‐ 1MB BAR size will work for this Function 

- Bit 5 ‐ 2MB 

- Bit 6 ‐ 4MB 

- ... 

- Bit 23 ‐ 512GB will work for this Function 

_Figure 20‐21: Resizable BAR Capability Register_ 

**==> picture [242 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24   23 4   3 0<br>RsvdP RsvdP<br>**----- End of picture text -----**<br>


## **Control Register** 

The BAR Index field in this register reports to which BAR this size refers (0 to 5 are possible). The Number of Resizable BARs field is only defined for Control 

**912** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

Register zero and is reserved for all the others. It tells how many of the six pos‐ sible BARs actually have an adjustable size. Finally, the BAR Size field is pro‐ grammed by software to specify the desired size the BAR indicated by the BAR Index field (0 = 1MB, 1=2MB, 2=4MB, ..., 19=512GB). 

_Figure 20‐22: Resizable BAR Control Register_ 

**==> picture [281 x 136] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 13  12 8   7 5   4 3    2 0<br>RsvdP RsvdP<br>BAR Size (RW)<br>Number of Resizable<br>BARs (RO)<br>BAR Index (RO)<br>**----- End of picture text -----**<br>


Once the Resizable values have been programmed, then enumeration software will be able to work as it normally does: writing all F’s to each BAR and reading it back will report the size that was selected. Note that if the size value is changed, the contents of the BAR will be lost and will need to reprogrammed if it was previously set up. Figure 20‐23 on page 914 highlights the BAR registers in the configuration header space for a Type 0 header. 

**913** 

**PCI Ex ress Technolo p gy** 

## _Figure 20‐23: BARs in a Type0 Configuration Header_ 

**==> picture [160 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 2 1 0 DW<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>HeaderType LatencyTimer CacheLineSize 03<br>04<br>Base Address 0<br>05<br>Base Address 1<br>06<br>Base Address 2<br>07<br>Base Address 3<br>08<br>Base Address 4<br>09<br>Base Address 5<br>10<br>CardBus CIS Pointer<br>Subsystem ID SubsystemVendor ID 11<br>Expansion ROM 12<br>Base Address<br>Reserved CapabilitiesPointer 13<br>14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>**----- End of picture text -----**<br>


## **Simplified Ordering Table**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
