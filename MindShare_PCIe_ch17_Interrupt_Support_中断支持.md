# 📘 第 17 章　中断支持 (Chapter 17. Interrupt Support)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0332.md` ... `chunks/chunk0340.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Interrupt Support](#-本章目录-table-of-contents)

<a id="sec-17-1"></a>
## 17.1 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

CPU<br>Root Complex<br>Memory<br>Interrupt Controller<br>Switch<br>Assert_INTA Assert_INTB<br>Deassert_INTA Deassert_INTB<br>INTA#<br>PCIe PCIe- INTB#<br>Endpoint PCI(X) INTC#INTD#<br>Bridge<br>PCI(X)<br>**----- End of picture text -----**<br>


**806** 

**Chapter 17: Interrupt Support** 

## **INTx Message Format** 

Figure 17‐10 on page 807 depicts the format of the INTx message header. The interrupt controller is the ultimate destination of these messages, however the routing method employed is _not_ “Route to the Root Complex”, but is actually “Local ‐ Terminate at Receiver” as shown in Figure 17‐10. There are two reasons for this. The first is because each bridge (including Switch Ports and Root Ports) along the upstream path may map the virtual interrupt wire to a different vir‐ tual interrupt wire across the bridge (e.g., a Switch Port receives Assert_INTA but maps it to Assert_INTB when propogating it upstream). More info about this INTx mapping can be found in “INTx Mapping” on page 808. 

The second reason for the local routing type of these messages is due to the fact that we’re emulating a pin‐based signal. If a port receives an assert interrupt message that maps to INTA on its primary side and it has already sent an Assert_INTA message upstream because of a previous interrupt, then there is no reason to send another one. INTA is already seen as asserted. More info about this collapsing of INTx messages can be found in “INTx Collapsing” on page 810. 

_Figure 17‐10: INTx Message Format and Type_ 

|||||+0|+0|||||||||+1|+1|||||||||+2|+2|+3|+3|||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||7|6|5|4|3|2|1|0||7||6|5|4|3|2||1|0|7|6||5|4|3|7 6 5 4 <br> 2 1 0|3|2|1|0||
|Byte 0|Fmt<br>0 0 1|||Type<br>1 0**1 0**||||**0**||R||TC|||R|At<br>tr||R|T<br>H|T<br>D|E<br>P||Attr||Length<br>AT|||||||
|Byte 4|||||Requester||||||||ID|||||||||||Tag||**Message**||**Code**||||
|Byte 8|||||||||||Reserved for INTx|||||||||||Messages||||||||||
|Byte 12|||||||||||Reserved for INTx|||||||||||Messages||||||||||
|**Local**|||**- Terminate**|||||||**at Receiver**|||||||||||||||**20h = Assert_INTA**|||||||
||||||||||||||||||||||||||**21h = Assert_INTB**|||||||
||||||||||||||||||||||||||**22h = Assert_INTC**|||||||
||||||||||||||||||||||||||**23h = Assert_INTD**|||||||
||||||||||||||||||||||||||**24h = Deassert_INTA**|||||||
||||||||||||||||||||||||||**25h = Deassert_INTB**|||||||
||||||||||||||||||||||||||**26h = Deassert_INTC**|||||||
||||||||||||||||||||||||||**27h = Deassert_INTD**|||||||



**807** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Mapping and Collapsing INTx Messages** 

## **INTx Mapping** 

Switches must adhere to the INTx mapping defined by the PCI spec, shown in Table 17‐1 on page 809. This mapping defines the virtual connection that exists when interrupts are routed across a PCI‐to‐PCI bridge. The mapping is based on the INTx message type and the Device number from the Requester ID field in the message. 

Refer to Figure 17‐11 on page 810 for this example. The assert interrupt mes‐ sages received on the two downstream switch ports are both INTA messages. The virtual PCI‐to‐PCI bridge at each of the ingress ports will map both INTA messages to INTA, meaning no change. This is because the Device number of both originating Endpoint devices is zero (which is contained in the interrupt message itself as part of the Requester ID, ReqID). Table 17‐1 shows that inter‐ rupts messages coming from Device 0 map to the same INTx message on the other side of the bridge (i.e., internal to the Switch both INTA messages are mapped to INTA). So each downstream port will propogate the interrupt mes‐ sages upstream without changing their virtual wire. However, the propogated interrupt messages no longer have the ReqID of the original requester, they now have the ReqID of the port that is propogating the interrupt message. 

Next, the upstream Switch Port receives the propogated interrupt messages. The INTA interrupt from port 2:1:0 is going to be mapped to an INTB message when progopated upstream because the interrupt message indicates it came from Device 1 (ReqID 2:1:0). The other interrupt being propogated by port 2:2:0 is going to be mapped to an INTC message when sent from the upstream Switch Port to the Root Port. Refer to Table 17‐1 to confirm these mappings. 

The reason for this interrupt mapping is the same as it was for PCI: to avoid as much as possible having multiple functions sharing the same INTx# pin. As stated previously, single function devices are required to use INTA if using leg‐ acy interrupts. So if all the Functions downstream of a Root Port used INTA and there was no mapping across bridges, they would all be routed to the same IRQ. Which means anytime one of the Functions asserted INTA, all the Functions would have to be checked. This would result in significant interrupt servicing latencies for the Functions at the end of the list. This interrupt mapping method is a crude attempt at distributing interrupts (especially INTA) across all four INTx virtual wires because each INTx virtual wire can be mapped to a separate IRQ at the interrupt controller. 

**808** 

**Chapter 17: Interrupt Support** 

_Table 17‐1: INTx Message Mapping Across Virtual PCI‐to‐PCI Bridges_ 

|**Device Number of**<br>**Delivering INTx**|**INTx Message**<br>**Type at Input**|**INTx Message**<br>**Type at Output**|
|---|---|---|
|0, 4, 8, 12 etc.|INTA|INTA|
||INTB|INTB|
||INTC|INTC|
||INTD|INTD|
|1, 5, 9, 13 etc.|INTA|INTB|
||INTB|INTC|
||INTC|INTD|
||INTD|INTA|
|2, 6, 10, 14 etc.|INTA|INTC|
||INTB|INTD|
||INTC|INTA|
||INTD|INTB|
|3, 7, 11, 15 etc.|INTA|INTD|
||INTB|INTA|
||INTC|INTB|
||INTD|INTC|



**809** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 17‐11: Example of INTx Mapping_ 

**==> picture [295 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>Interrupt Controller<br>Assert_INTB (ReqID 1:0:0)<br>Assert_INTC (ReqID 1:0:0)<br>INTA from Dev 1 maps to INTB 1:0:0 INTA from Dev 2 maps to INTC<br>Assert_INTA (ReqID 2:1:0)<br>Switch Assert_INTA (ReqID 2:2:0)<br>INTA from Dev 0 maps to INTA 2:1:0 2:2:0 INTA from Dev 0 maps to INTA<br>Assert_INTA (ReqID 3:0:0)<br>Assert_INTA (ReqID 4:0:0)<br>3:0:0 4:0:0<br>PCIe PCIe<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


## **INTx Collapsing** 

PCIe Switches must ensure that INTx messages are delivered upstream in the correct fashion. Specifically, interrupt routing of legacy PCI implementations must be handled such that software can determine which interrupts are routed to which interrupt controller inputs. INTx# lines may be wire‐ORed and be routed to the same IRQ input on the interrupt controller, and when multiple devices signal interrupts on the same line, only the first assertion is seen by the interrupt controller. Similarly, when one of these devices deasserts its INTx# line, the line remains asserted until the last one is turned off. These same princi‐ ples apply to PCIe INTx messages. 

In some cases, however, two overlapping INTx messages may be mapped to the same INTx message by a virtual PCI bridge at the egress port, requiring the messages to be collapsed. Consider the following example illustrated in Figure 17‐12 on page 811. 

**810** 

**Chapter 17: Interrupt Support** 

When the upstream Switch Port maps the interrupt messages for delivery on the upstream link, both interrupts will be mapped as INTB (based on the device numbers of the downstream Switch Ports). Note that because these two over‐ lapping messages are the same they must be collapsed. 

Collapsing ensures that the interrupt controller will never receive two consecu‐ tive Assert_INTx or Deassert_INTx messages for the shared interrupts. This is equivalent to INTx signals being wire‐ORed. 

_Figure 17‐12: Switch Uses Bridge Mapping of INTx Messages_ 

**==> picture [273 x 382] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>Interrupt Controller<br>Assert_INTB (1:0:0)<br>3<br>Deassert_INTB (1:0:0)<br>1:0:0<br>Switch<br>2:1:0 2:5:0<br>Assert_INTA (3:0:0) Assert_INTA (4:0:0)<br>1 2<br>Deassert_INTA (3:0:0) Deassert_INTA (4:0:0)<br>3:0:0 4:0:0<br>PCIe PCIe<br>Endpoint Endpoint<br>Deassert_INTA (3:0:0)<br>1<br>Assert_INTA (3:0:0)<br>(blocked by 1:0:0)<br>2<br>Assert_INTA (4:0:0) Deassert_INTA (4:0:0)<br>(blocked by 1:0:0)<br>3<br>Assert_INTB (1:0:0) Deassert_INTB (1:0:0)<br>caused by Assert_INTA (4:0:0) caused by Deassert_INTA (3:0:0)<br>**----- End of picture text -----**<br>


**811** 

**PCI Ex ress 3.0 Technolo p gy** 

## **INTx Delivery Rules** 

The rules associated with the delivery of INTx messages have some unique characteristics: 

- Assert_INTx and Deassert_INTx are only issued in the upstream direction. 

- Switches that are collapsing interrupts will only issue INTx messages upstream when there is a change of the interrupt status. 

- Devices on either side of a link must track the current state of INTA‐INTD assertion. 

- A Switch tracks the state of the four virtual wires for each of its downstream ports, and may present a collapsed set of virtual wires on its upstream port. 

- The Root Complex must track the state of the four virtual wires (A‐D) for each downstream port. 

- INTx signaling may be disabled with the Interrupt Disable bit in the Com‐ mand Register. 

- If any INTx virtual wires are active and device interrupts are then disabled, a corresponding Deassert_INTx message must be sent. 

- If a downstream Switch Port goes to DL_Down status, any active INTx vir‐ tual wires must be deasserted, and the upstream port updated accordingly (Deassert_INTx message required if that INTx was in active state). 

## **The MSI Model** 

A PCIe Function indicates MSI support via the MSI Capability registers. Each Function must implement either the MSI Capability Structure or the MSI‐X (eXtended MSI, see “The MSI‐X Model” on page 821) Capability Structure, or both. The MSI Capability registers are set up by configuration software and include: 

- Target memory address 

- Data Value to be written to that address 

- The number of unique messages that can be encoded into the data 

See “Memory Request Header Fields” on page 188 for a review of the Memory Write Transaction Header. Note that MSIs always have a data payload of 1DW. 

## **The MSI Capability Structure** 

The MSI Capability Structure resides in the PCI‐compatible config space area (first 256 bytes). There are four variations of the MSI Capability Structure based on whether it supports 64‐bit addressing or only 32‐bit and whether it supports 

**812** 

**Chapter 17: Interrupt Support** 

per vector masking or not. Native PCIe devices are required to support 64‐bit addressing. All four variations of the MSI Capability Structure can be found in Figure 17‐13 on page 813. 

_Figure 17‐13: MSI Capability Structure Variations_ 

|||32-bit Address|||||
|---|---|---|---|---|---|---|
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Message Data||||DW2|
|||64-bit Address|||||
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Message Address [63:32]||||DW2|
|||Message Data||||DW3|
|||32-bit Address with Per-Vector|Masking||||
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Reserved<br>Message Data||||DW2|
|||Mask Bits||||DW3|
|||Pending Bits||||DW4|
|||64-bit Address with Per-Vector|Masking||||
||31|15<br>8<br>16||7|0||
|||Message Control<br>Next Capability<br>Pointer||Capability ID<br>(05h)||DW0|
|||Message Address [31:0]||||DW1|
|||Message Address [63:32]||||DW2|
|||Reserved<br>Message Data||||DW3|
|||Mask Bits||||DW4|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-2"></a>
## 17.2 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|||Pending Bits||||DW5|
||||||||



**813** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Capability ID** 

A Capability ID value of **05h** identifies the MSI capability and is a read‐only value. 

## **Next Capability Pointer** 

The second byte of the register is a read‐only value that gives the dword‐ aligned offset from the top of config space to the next Capability Structure in the linked list of structures or else contains 00h to indicate the end of the linked list. 

## **Message Control Register** 

Figure 17‐14 on page 814 and Table 17‐2 on page 814 illustrate the layout and usage of the Message Control register. 

_Figure 17‐14: Message Control Register_ 

**==> picture [358 x 114] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9 8 7 6 4 3 1 0<br>Reserved<br>MSI Enable<br>Multiple Message Capable<br>Multiple Message Enable<br>64-bit Address Capable<br>Per-vector Masking Capable<br>**----- End of picture text -----**<br>


_Table 17‐2: Format and Usage of Message Control Register_ 

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|0|MSI Enable|Read/Write. State after reset is 0, indicating that the<br>device’s MSI capability is disabled.<br>• **0**= Function is**disabled**from using**MSI**. It must<br>use MSI‐X or else INTx Messages.<br>• **1**= Function is**enabled**to use**MSI**to request<br>service and won’t use MSI‐X or INTx Messages.|



**814** 

**Chapter 17: Interrupt Support** 

_Table 17‐2: Format and Usage of Message Control Register (Continued)_ 

|**Bit(s)**|**Field Name**||**Description**|
|---|---|---|---|
|3:1|Multiple Message<br>Capable||Read‐Only. System software reads this field to<br>determine how many messages (interrupt vectors)<br>the Function would like to use. The requested<br>number of messages is a power of two, therefore a<br>Function that would like three messages must<br>request that four messages be allocated to it.<br>**Value**<br>   **Number of Messages Requested**<br>000b                                    1<br>001b                                    2<br>010b                                    4<br>011b                                    8<br>100b                                   16<br>101b                                   32<br>110b                              Reserved<br>111b                              Reserved|
|6:4|Multiple Message<br>Enable||Read/Write. After system software reads the Multi‐<br>ple Message Capable field (previous row in this<br>table) to see how many messages (interrupt vec‐<br>tors) are requested by the Function, it programs a<br>3‐bit value in this field indicating the actual num‐<br>ber of messages allocated to the Function. The<br>number allocated can be equal to or less than the<br>number actually requested. The state of this field<br>after reset is 000b.<br>**Value**<br>   **Number of Messages Requested**<br>000b                                    1<br>001b                                    2<br>010b                                    4<br>011b                                    8<br>100b                                   16<br>101b                                   32<br>110b                              Reserved<br>111b                              Reserved|



**815** 

**PCI Ex ress 3.0 Technolo p gy** 

_Table 17‐2: Format and Usage of Message Control Register (Continued)_ 

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|7|64‐bit Address<br>Capable|Read‐Only.<br>• 0 = Function does not implement the upper 32<br>bits of the Message Address register; only a 32‐<br>bit address is possible.<br>• 1 = Function implements the upper 32 bits of the<br>Message Address register and is capable of gen‐<br>erating a 64‐bit memory address.|
|8|Per‐Vector<br>Masking Capable|Read‐Only.<br>• 0 = Function does not implement the Mask Bit<br>register or the Pending Bit register; software<br>does NOT have the ability to mask individual<br>interrupts with this capability structure.<br>• 1 = Function does implement the Mask Bit regis‐<br>ter or the Pending Bit register; software does<br>have the ability to mask individual interrupts<br>with this capability structure.|
|15:9|Reserved|Read‐Only. Always zero.|



## **Message Address Register** 

The lower two bits of the 32‐bit Message Address register are zero and cannot be changed, forcing the address assigned by software to be dword aligned. Typ‐ ically, this would be the address of the Local APIC in the system CPU. In x86‐ based systems (Intel‐compatible), this address has traditionally been FEEx_xxxxh where the lower 20 bits indicate which Local APIC is being tar‐ geted as well as some other info about the interrupt itself. It is important to note that how the address is interpreted is platform specific and is not dictated in the PCI or PCIe specs. 

The register containing bits [63:32] of the Message Address are required for native PCI Express devices but is optional for legacy endpoints. This register is present if Bit 7 of the Message Control register is set. If so, it is a read/write reg‐ ister used in conjunction with the Message Address [31:0] register to enable a 64‐bit memory address for interrupt delivery from this Function. 

**816** 

**Chapter 17: Interrupt Support** 

## **Message Data Register** 

System software writes a base message data pattern into this 16‐bit, read/write register. When the Function generates an interrupt request, it writes a 32‐bit data value to the memory address specified in the Message Address register. The upper 16 bits of this data are always set to zero, while the lower 16 bits are supplied by the Message Data register. 

If more than one message has been assigned to the Function, it modifies the lower bits (the number of modifiable bits depends on how many messages have been assigned to the Function by configuration software) of the Message Data register value to form the appropriate value for the event it wishes to report. As an example, refer to “Basics of Generating an MSI Interrupt Request” on page 820. 

## **Mask Bits Register and Pending Bits Register** 

If the Function supports per‐vector masking (indicated in bit [8] of the Message Control register) then these registers are present. The max number of interrupt messages (itnerrupt vectors) that can be requested and assigned to a Function using MSI is 32. So these two registers are 32 bits in length with each potential interrupt message having its own mask and pending bit. If bit [0] of the Mask Bits register is set, then interrupt message 0 is masked (this is the base vector from this Function). If bit [1] is set, then interrupt message 1 is masked (this is the base vector + 1). 

When an interrupt message is masked, the MSI for that vector cannot be sent. Instead, the corresponding Pending Bit is set. This allows software to mask indi‐ vidual interrupts from a Function and then periodically poll the Function to see if there are any masked interrupts that are pending. 

If software clears a mask bit and the corresponding pending bit is set, the Func‐ tion must send the MSI request at that time. Once the interrupt message has been sent, the Function would clear the pending bit. 

## **Basics of MSI Configuration** 

The following list specifies the steps taken by software to configure MSI inter‐ rupts for a PCI Express device. Refer to Figure 17‐15 on page 819. 

1. At startup time, enumeration software scans the system for all PCI‐compat‐ ible Functions (see “Single Root Enumeration Example” on page 109 for a discussion of the enumeration process). 

**817** 

## **PCI Ex ress 3.0 Technolo p gy** 

2. Once a Function is discovered software reads the Capabilities List Pointer, to find the location of the first capability structure in the linked list. 

3. If the MSI Capability structure (Capability ID of 05h) is found in the list, software reads the Multiple Message Capable field in the device’s Message Control register to determine how many event‐specific messages the device supports and if it supports a 64‐bit message address or only 32‐bit. Software then allocates a number of messages equal to or less than that and writes that value into the Multiple Message Enable field. At a minimum, one mes‐ sage will be allocated to the device. 

4. Software writes the base message data pattern into the device’s Message Data register and writes a dword‐aligned memory address to the device’s Message Address register to serve as the destination address for MSI writes. 

5. Finally, software sets the MSI Enable bit in the device’s Message Control register, enabling it to generate MSI writes and disabling other interrupt delivery options. 

**818** 

**Chapter 17: Interrupt Support** 

_Figure 17‐15: Device MSI Configuration Process_ 

**==> picture [159 x 456] intentionally omitted <==**

**----- Start of picture text -----**<br>
Scan PCI bus(es)<br>until device<br>discovered<br>New<br>N<br>Capabilities<br>?<br>Y<br>MSI N<br>Capable<br>?<br>Y<br>Determine number of<br>messages requested<br>and assign number<br>of messages to device<br>Write base data<br>pattern into<br>Message Data<br>Register<br>Assign Memory<br>Address to Message<br>Address Register<br>Enable device to<br>use MSI with<br>MSI Enable bit<br>in Message Control<br>Register<br>**----- End of picture text -----**<br>


**819** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Basics of Generating an MSI Interrupt Request** 

Figure 17‐16 on page 821 illustrates the contents of an MSI Memory Write Trans‐ action Header and Data field. Key points include: 

- Format field must be 011b for native functions, indicating a 4DW header (64‐bit address) with Data, but it may be 010b for Legacy Endpoints, indi‐ cating a 32‐bit address. 

- The Attribute bits for No Snoop and Relaxed Ordering must be zero. 

- Length field must be 01h to indicate maximum data payload of 1DW. 

- First BE field must be 1111b, indicating valid data in all four bytes of the DW, even though the upper two bytes will always be zero for MSI. 

- Last BE field must be 0000b, indicating a single DW transaction. 

- Address fields within the header come directly from the address fields within the MSI Capability registers. 

- Lower 16 bits of the Data payload are derived from the data field within the MSI Capability registers. 

## **Multiple Messages** 

If system software allocated more than one message to the Function, the multi‐ ple values are created by modifying the lower bits of the assigned Message Data value to send a different message for each device‐specific event type. 

As an example, assume the following: 

- Four messages have been allocated to a device. 

- A data value of 49A0h has been assigned to the device’s Message Data reg‐ ister. 

- Memory address FEEF_F00Ch has been written into the device’s Message Address register. 

- When one of the four events occurs, the device generates a request by per‐ forming a dword write to memory address FEEF_F00Ch with a data value of 0000_49A0h, 0000_49A1h, 0000_49A2h, or 0000_49A3h. In other words, the lower two bits of the data value are modified to specify which event occurred. If this Function would have been allocated 8 messages, then the lower three bits could be modified. Also, the device always uses 0000h for the upper 2 bytes of its message data value. 

**820** 

**Chapter 17: Interrupt Support** 

_Figure 17‐16: Format of Memory Write Transaction for Native‐Device MSI Delivery_ 

**==> picture [329 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-3"></a>
## 17.3 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

MSI (Memory Write) Transaction<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 1 1Fmt 0 0 0 0 0Type R TC R Attr R HT DT EP Attr0 0 AT 0 0 0 0 0 0 0 0 0 1Length<br>Last DW First DW<br>Byte 4 Requester ID Tag 0 0 0 0 1 1 1 1<br>Header<br>Byte 8 MSI Message Address [63:32]<br>Byte 12 MSI Message Address [31:0] 0 0<br>Byte 16 MSI Message Data 0000h Data<br>MSI Capability Structure<br>31 16 15 8 7 0<br>Message Control Next CapabilityPointer Capability ID(05h) DW0<br>Message Address [31:0] DW1<br>Message Address [63:32] DW2<br>Message Data DW3<br>**----- End of picture text -----**<br>


## **The MSI-X Model** 

## **General** 

The 3.0 revision of the PCI spec added support for MSI‐X, which has its own capability structure. MSI‐X was motivated by a desire to alleviate three short‐ comings of MSI: 

- 32 vectors per function are not enough for some applications. 

- Having only one destination address makes static distribution of interrupts across multiple CPUs difficult. The most flexibility would be achieved if a unique address could be assigned for each vector. 

**821** 

**PCI Ex ress 3.0 Technolo p gy** 

- In several platforms, like x86‐based systems, the vector number of the inter‐ rupt indicates its priority relative to other interrupts. With MSI, a single Function could be allocated multiple interrupts, but all the interrupt vectors would be contiguous, meaning similar priority. This is not a good solution if some interrupts from this Function should be high priority and others should be low priority. A better approach would be for software to desig‐ nate a unique vector (message data value), that does not have to be contigu‐ ous, for each interrupt allocated to the Function. 

Keeping those goals in mind, it’s easy to understand the register changes that were implemented to provide more vectors with each vector being assigned a target address and message data value. 

## **MSI-X Capability Structure** 

As shown in Figure 17‐17 on page 822, the Message Control register is quite dif‐ ferent from MSI. Interestingly, even though MSI‐X can support up to 2048 vec‐ tors per Function versus the 32 for MSI, the number of configuration registers for MSI‐X is actually a little smaller than for MSI. That’s because the vector information isn’t contained here. Instead, it’s in a memory location (MMIO) pointed to by the Table BIR (Base address Indicator Register), as shown in Fig‐ ure 17‐18 on page 824. 

_Figure 17‐17: MSI‐X Capability Structure_ 

**==> picture [326 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 8 7 0<br>Message Control Next CapabilityPointer Capability ID(11h) DW0<br>Table<br>MSI-X Table Offset DW1<br>BIR<br>PBA<br>Pending Bit Array (PBA) Offset BIR DW2<br>(BIR = BAR Index Register)<br>15 14 13 11 10 0<br>Rsvd Table Size in N-1 (RO)<br>Function Mask (RW)<br>MSI-X Enable (RW)<br>**----- End of picture text -----**<br>


**822** 

**Chapter 17: Interrupt Support** 

_Table 17‐3: Format and Usage of MSI‐X Message Control Register_ 

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|10:0|Table Size|Read‐Only. This field indicates the number of inter‐<br>rupt messages (vectors) that this Function sup‐<br>ports. The value here is interpreted in an N‐1<br>fashion, so a value of 0 means 1 vector. A value of 7<br>means 8 vectors. Each vector has its own entry in<br>the MSI‐X Table and its own bit in the Pending Bit<br>Array.|
|13:11|Reserved|Read‐Only. Always zero.|
|14|Function Mask|Read/Write. This field provides system software an<br>easy way to mask all the interrupts from a Func‐<br>tion. If this bit is cleared, interrupts can still be<br>masked individually by setting the mask bit within<br>each vector’s MSI‐X table entry.|
|15|MSI‐X Enable|Read/Write. State after reset is 0, indicating that the<br>device’s MSI‐X capability is disabled.<br>• **0**= Function is**disabled**from using**MSI‐X**. It<br>must use MSI or INTx Messages.<br>• **1**= Function is**enabled**to use**MSI‐S**to request<br>service and won’t use MSI‐X or INTx Messages.|



**823** 

**PCI Ex ress 3.0 Technolo p gy** 

## _Figure 17‐18: Location of MSI‐X Table_ 

**==> picture [332 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
Doubleword<br>Byte (in decimal)Number Syste Memory Address Space m Memory<br>3 2 1 0<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>BIST HeaderType LatencyTimer CacheLineSize 03<br>Base A ddress 0 04<br>Base A ddress 1 05 Table BIR = 2<br>MSI-X Table<br>Base A ddress 2 06<br>Base A ddress 3 07<br>08<br>Base A ddress 4 MSI-X Table<br>Base A ddress 5 09 Offset<br>10<br>CardBus CIS Pointer<br>Subsystem ID SubsystemVendor ID 11<br>Expansion R OM 12<br>Base Ad dress<br>Reserved Capabilities 13<br>Pointer<br>Reserved 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>Required configuration registers<br>**----- End of picture text -----**<br>


## **MSI-X Table** 

The MSI‐X Table itself is an array of vectors and addresses, as shown in Figure 17‐19 on page 825. Each entry represents one vector and contains four Dwords. DW0 and DW1 supply a unique 64‐bit address for that vector, while DW2 gives a unique 32‐bit data pattern for it. DW3 only contains one bit at present: a mask bit for that vector, allowing each vector to be independently masked off as needed. 

**824** 

**Chapter 17: Interrupt Support** 

_Figure 17‐19: MSI‐X Table Entries_ 

|DW3||DW2|DW1|DW0||
|---|---|---|---|---|---|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 0|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 1|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 2|
|….||….|….|….||
|….||….|….|….||
|Vector Control||Message Data|Upper Address|Lower Address|Entry N-1|
|Bit 0 is||vector Mask Bit (R/W)||||



## **Pending Bit Array** 

In much the same way, the Pending Bit Array is also located within a memory address. It can use the same BIR value (same BAR) as the MSI‐X Table with a different offset, or it could use a different BAR altogether. The array, shown in Figure 17‐20, simply contains a bit for every vector that will be used. If the event to trigger that interrupt occurs but its Mask Bit has been set, then an MSI‐X transaction will not be sent. Instead, the corresponding pending bit is set. Later, if that vector is unmasked and the pending bit is still set, the interrupt will be generated at that time. 

**825** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 17‐20: Pending Bit Array_ 

**==> picture [211 x 116] intentionally omitted <==**

**----- Start of picture text -----**<br>
DW1 DW0<br>Pending Bits 0 - 63 QW 0<br>Pending Bits 64 - 127 QW 1<br>Pending Bits 128 - 191<br>….<br>….<br>Pending Bits QW (N-1)/64<br>**----- End of picture text -----**<br>


## **Memory Synchronization When Interrupt Handler Entered** 

## **The Problem** 

There is a potential problem with any interrupt scheme when data is being delivered. For example, if the device has previously sent data and wants to report that with an interrupt, a unexpected delay on data delivery could allow the interrupt to arrive too soon. That might happen in the bridge data buffer shown in Figure 17‐21 on page 827, and the result is a race condition. The steps are similar to our earlier discussion (see “The Legacy Model” on page 796): 

1. The function writes a data block toward memory. The write completes on the local bus as a posted transaction, meaning that the sender has finished all it needed to do and the transaction is considered completed. 

2. An interrupt is delivered to notify software that some requested data is now present in memory. However, the data has been delayed in the bridge for some reason. 

3. The interrupt vector is fetched as before. 

4. The ISR starting address is fetched and control is passed to it. 

5. The ISR reads from the target memory buffer but the data payload still hasn’t been delivered so it fetches stale data, possibly causing an error. 

**826** 

**Chapter 17: Interrupt Support** 

_Figure 17‐21: Memory Synchronization Problem_ 

**==> picture [268 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTR<br>CPU 5 Memory<br>Memory Buffer<br>4 Interrupt Service<br>Routine (ISR)<br>North Bridge<br>Interrupt Table (ISR<br>3 starting addresses)<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>1<br>PCI Bus<br>2<br>Interrupt Controller<br>(PIC) INTA#<br>Device<br>**----- End of picture text -----**<br>


## **One Solution** 

One way to alleviate this problem takes advantage of PCI transaction ordering rules. If the ISR first sends a read request to the device that initiated the inter‐ rupt before it attempts to fetch the data, the resulting read completion will fol‐ low the same path back to the CPU that any write data would have taken from that device to get to memory. Transaction ordering rules guarantee that a read result in a bridge cannot pass a posted write going in the same direction, so the end result is that the data will get written into memory before the read result will be allowed to reach the CPU. Therefore, if the ISR waits for the read com‐ pletion to arrive before proceeding, it can be sure that any data will have been delivered to memory and thus the race condition is avoided. Since the read is basically being used as a data flush mechanism, it isn’t necessary for it to return any data. In that case the read can be zero length and the data returned is dis‐ carded. For that reason, this type of read is sometimes called a “dummy read.” 

## **An MSI Solution** 

MSI can simplify this process, although there are some requirements for it to work (refer to Figure 17‐22 on page 829). If the system allows the device to gen‐ 

**827** 

**PCI Ex ress 3.0 Technolo p gy** 

erate its own MSI writes rather than going through an intermediary like an IO APIC, then the following example can take place: 

1. The device writes the payload data toward memory and it is absorbed by the write buffer in the bridge. 

2. The device believes the data has been delivered and signals an interrupt to notify the CPU. In this case, an MSI is sent and uses the same path as the data. Since both data and MSI appear as memory writes to the bridge, the normal transaction ordering rules will keep them in the correct sequence. 

3. The payload data is delivered to memory, freeing the path through the bridge for the MSI write. 

4. The MSI write is delivered to the CPU Local APIC and the software now knows that the payload data is available. 

## **Traffic Classes Must Match** 

An important point must be stressed here, however. Both the data and MSI must use the same Traffic Class for this to work. Recall that packets that have been assigned different TC values may end up being mapped into different Vir‐ tual Channels, and that packets in different VCs have no ordering relationship. If the data were mapped to VC0 and the MSI was mapped to VC1, then the sys‐ tem would be unaware of any ordering relationship between them and unable to enforce memory coherency automatically. 

If giving both packets the same TC is not possible, the system would need to use the “dummy read” method instead and the TC of the read request would need to match the TC of the data write packet. It should be clear that even if the same TC is used for both, the use of the Relaxed Ordering bit must be avoided. We’re counting on the transaction ordering rules to achieve memory synchronization, so they must not be relaxed. 

**828** 

**Chapter 17: Interrupt Support** 

_Figure 17‐22: MSI Delivery_ 

**==> picture [280 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-4"></a>
## 17.4 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Local Local<br>APIC APIC<br>CPU CPU<br>4<br>Memory<br>3<br>North Bridge<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>1<br>2<br>PCI Bus<br>Interrupt Controller<br>(IO APIC)<br>Device<br>**----- End of picture text -----**<br>


## **Interrupt Latency** 

The time from signaling an interrupt until software services the device is referred to as the interrupt latency. In spite of its advantages, MSI, like other interrupt delivery mechanisms, does not provide interrupt latency guarantees. 

## **MSI May Result In Errors** 

Because MSIs are delivered as Memory Write transactions, an error associated with delivery of an MSI is treated the same as any other Memory Write error condition. See “ECRC Generation and Checking” on page 657 for treatment of ECRC errors, as one example. The concern, of course, is that if an error results in the MSI packet being unrecognized then no interrupt will be seen by the proces‐ sor. How this condition would be handled is outside the scope of the PCIe spec. 

**829** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Some MSI Rules and Recommendations** 

1. It is the intent of the spec that mutually‐exclusive messages will be assigned to Functions by system software and that each message will be converted to an exclusive interrupt on delivery to the processor. 

2. More than one MSI capability register set per Function is prohibited. 

3. A read of the Message Address register produces undefined results. 

4. Reserved registers and bits are read‐only and always return zero when read. 

5. System software can modify Message Control register bits, but the device itself is prohibited from doing so. In other words, modifying the bits by a “back door” mechanism is not allowed. 

6. At a minimum, a single message will be assigned to each device (assuming software supports and plans to use MSI in the system). 

7. System software must not write to the upper half of the dword that contains the Message Data register. 

8. If the device writes the same message multiple times, only one of those messages is guaranteed to be serviced. If all of them must be serviced, the device must not generate the same message again until the previous one has been serviced. 

9. If a device has more than one message assigned, and it writes a series of dif‐ ferent messages, it is guaranteed that all of them will be serviced. 

## **Special Consideration for Base System Peripherals** 

Interrupts may also originate in embedded legacy hardware, such as an IO Con‐ troller Hub or Super IO device. Some of the typical legacy devices required in such systems include: 

- Serial ports 

- Parallel ports 

- Keyboard and Mouse Controller 

- System Timer 

- IDE controllers 

These devices typically require a specific IRQ line into a PIC or IO APIC, which allows legacy software to interact with them correctly. 

Using the INTx messages does not guarantee that the devices will receive the IRQ assignment they require. The following example illustrates a system that will support the proper legacy interrupt assignment. 

**830** 

**Chapter 17: Interrupt Support** 

## **Example Legacy System** 

Figure 17‐23 on page 831 shows a older PCI Express system that includes an IO Controller Hub (ICH) attached to the Root Complex via a proprietary Hub link. The IO APIC embedded within the ICH can generate an MSI when it receives an interrupt request at its inputs. In such an implementation, software can assign the legacy vector number to each input to ensure that the correct legacy software will be called. 

The advantage of this approach is that existing hardware can be used to support the legacy requirements of a PCIe platform. This system also requires that the MSI subsystem be configured for use during the boot sequence. The example illustrated eliminates the need for INTx messages unless a PCIe expansion device incorporates a PCI Express‐to‐PCI Bridge. 

_Figure 17‐23: PCI Express System with PCI‐Based IO Controller Hub_ 

**==> picture [361 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>PCI Express<br>GFX<br>PCI Express Root Complex DDR<br>Links SDRAM<br>Hub Link<br>IDE<br>CD HDD IO Controller Hub<br>MSI<br>USB 2.0 Interrupt 4 INTA# - INTD#<br>Controller<br>LPC (APIC) PCI - 33MHz<br>1<br>Serial Interrupts Timer<br>S IEEE Slots<br>IO AC’97 1394<br>COM1 Link<br>COM2<br>Modem Audio Boot<br>Codec Codec Ethernet ROM<br>RouterInterrupt<br>**----- End of picture text -----**<br>


**831** 

**PCI Ex ress 3.0 Technolo p gy** 

**832** 

## _**18**_ 

## _**System Reset**_ 

## **The Previous Chapter** 

The previous chapter describes the different ways that PCIe Functions can gen‐ erate interrupts. The old PCI model used pins for this, but sideband signals are undesirable in a serial model so support for the inband MSI (Message Signaled Interrupt) mechanism was made mandatory. The PCI INTx# pin operation can still be emulated using PCIe INTx messages for software backward compatibil‐ ity reasons. Both the PCI legacy INTx# method and the newer versions of MSI/ MSI‐X are described. 

## **This Chapter** 

This chapter describes the four types of resets defined for PCIe: cold reset, warm reset, hot reset, and function‐level reset. The use of a side‐band reset PERST# signal to generate a system reset is discussed, and so is the in‐band TS1 used to generate a Hot Reset. 

## **The Next Chapter** 

The next chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it’s important to ensure that its power needs don’t exceed what the system can deliver. A mechanism was needed to query and control the power requirements of a device, Power Budgeting provides this. 

## **Two Categories of System Reset** 

The PCI Express spec describes four types of reset mechanisms. Three of these were part of the earlier revisions of the PCIe spec and are collectively referred to now as **Conventional Resets,** and two of them are called Fundamental Resets. The fourth category and method, added with the 2.0 spec revision, is called the **Function Level Reset** . 

**833** 

**PCI Ex ress Technolo p gy** 

## **Conventional Reset** 

## **Fundamental Reset** 

A Fundamental Reset is handled in hardware and resets the entire device, re‐ initializing every state machine and all the hardware logic, port states and con‐ figuration registers. The exception to this rule is a group of some configuration register fields that are identified as “sticky”, meaning they retain their contents unless all power is removed. This makes them very useful for diagnosing prob‐ lems that require a reset to get a Link working again, because the error status survives the reset and is available to software afterwards. If main power is removed but Vaux is available, that will also maintain the sticky bits, but if both main power and Vaux are lost, the sticky bits will be reset along with everything else. 

A Fundamental Reset will occur on a system‐wide reset, but it can also be done for individual devices. 

Two types of Fundamental Reset are defined: 

- **Cold Reset** : The result when the main power is turned on for a device. Cycling the power will cause a cold reset. 

- **Warm Reset (optional):** Triggered by a system‐specific means without shut‐ ting off main power. For example, a change in the system power status might be used to initiate this. The mechanism for generating a Warm Reset is not defined by the spec, so the system designer will choose how this is done. 

When a Fundamental Reset occurs: 

- For positive voltages, receiver terminations are required to meet the ZRX‐HIGH‐IMP‐DC‐POS parameter. At 2.5 GT/s, this is no less than 10 K  . At the higher speeds it must be no less than 10 K  for voltages below 200mv, and 20 K  for voltages above 200mv. These are the values when the termi‐ nations are not powered. 

- Similarly for negative voltages, the ZRX‐HIGH‐IMP‐DC‐NEG parameter, the value is a minimum of 1 K  in every case. 

- Transmitter terminations are required to meet the output impedance ZTX‐DIFF‐DC from 80 to 120  for Gen1 and max of 120  for Gen2 and Gen3, but may place the driver in a high impedance state. 

- The transmitter holds a DC common mode voltage between 0 and 3.6 V. 

**834** 

**Cha ter 18: S stem Reset p y** 

When exiting from a Fundamental Reset: 

- The receiver single‐ended terminations must be present when receiver ter‐ minations are enabled so that Receiver Detect works properly (40‐60  for Gen1 and Gen2, and 50  for Gen3. By the time Detect is entered, the common‐mode impedance must be within the proper range of 50   

- must re‐enable its receiver terminations ZRX‐DIFF‐DC of 100  within 5 ms of Fundamental Reset exit, making it detectable by the neighbor’s transmitter during training. 

- The transmitter holds a DC common mode voltage between 0 and 3.6 V. 

Two methods of delivering a Fundamental Reset are defined. First, it can be sig‐ naled with an auxiliary side‐band signal called PERST# (PCI Express Reset). Second, when PERST# is not provided to an add‐in card or component, a Fun‐ damental Reset is generated autonomously by the component or add‐in card when the power is cycled. 

## **PERST# Fundamental Reset Generation** 

A central resource device such as a chipset in the PCI Express system provides this reset. For example, the IO Controller Hub (ICH) chip in Figure 18‐1 on page 836 may generate PERST# based on the status of the system power supply ‘POWERGOOD’ signal, since this indicates that the main power is turned on and stable. If power is cycled off, POWERGOOD toggles and causes PERST# to assert and deassert., resulting in a Cold Reset. The system may also provide a method of toggling PERST# by some other means to accomplish a Warm Reset. 

The PERST# signal feeds all PCI Express devices on the motherboard including the connectors and graphics controller. Devices may choose to use PERST# but are not required to do so. PERST# also feeds the PCIe‐to‐PCI‐X bridge shown in the figure. Bridges always forward a reset on their primary (upstream) bus to their secondary (downstream) bus, so the PCI‐X bus sees RST# asserted. 

## **Autonomous Reset Generation** 

A device must be designed to generate its own reset in hardware upon applica‐ tion of main power. The spec doesn’t describe how this would be done, so a self‐ reset mechanism can be built into the device or added as external logic. For example, an add‐in card that detects Power‐On may use that event to generate a local reset to its device. The device must also generate an autonomous reset if it detects its power go outside of the limits specified. 

**835** 

**PCI Ex ress Technolo p gy** 

## **Link Wakeup from L2 Low Power State** 

As an example of the need for an autonomous reset, a device whose main power has been turned off as part of a power management policy may be able to request a return to full power if it was designed to signal a wakeup. When power is restored, the device must be reset. The power controller for the system may assert the PERST# pin to the device, as shown in Figure 18‐1 on page 836, but if it doesn’t, or if the device doesn’t support PERST#, the device must auton‐ omously generate its own Fundamental Reset when it senses main power re‐ applied. 

_Figure 18‐1: PERST# Generation_ 

**==> picture [299 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>GFX Root Complex<br>DDR<br>PCI Express SDRAM<br>GFX<br>PCI Express<br>POWERGOOD PRST#<br>PCI<br>IO Controller Hub<br>(ICH) IEEE<br>1394<br>PERST#<br>Add-In Add-In<br>Switch<br>PCI Express<br>PCI Express Link<br>SCSI<br>to-PCI-X<br>PRST#<br>PCI-X<br>Gigabit<br>Ethernet<br>**----- End of picture text -----**<br>


**836**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-5"></a>
## 17.5 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Cha ter 18: S stem Reset p y** 

## **Hot Reset (In-band Reset)** 

A Hot Reset is propagated in‐band from one link neighbor to another by send‐ ing several TS1s (whose contents are shown in Figure 18‐2) with bit 0 of symbol 5 asserted. These TS1s are sent on all Lanes, using the previously negotiated Link and Lane numbers, for 2 ms. Once it’s been sent, the Transmitter and Receiver of the Hot Reset will both end up in the Detect LTSSM state (see “Hot Reset State” on page 612). 

_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_ 

|_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_|_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_|_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_|
|---|---|---|
||||
|**TS1**<br>TS ID<br>TS ID<br>TS ID<br>Train Ctl<br>Rate ID<br># FTS<br>Lane #<br>Link #<br>COM<br>0<br>1<br>2<br>3<br>4<br>5<br>6<br>14<br>15<br>13|K28.5<br>D0.0-D31.7, K23.7 (0-255)<br>D0.0-D31.0, K23.7 (0-31)<br># of FTS ordered sets required by<br>receiver to obtain bit and symbol lock<br>D10.2 for TS1 Identifier<br>D10.2 for TS1 Identifier<br>D10.2 for TS1 Identifier|**0** **=** **De-assert** **Disable** **Scrambling**<br>**1** **=** **Assert** **Disable** **Scrambling**<br>**Bit** **3**<br>**Reserved**<br>**Bit** **5:7**<br>**0** **=** **De-assert** **Compliance** **Receive**<br>**1** **=** **Assert** **Compliance** **Receive**<br>**Bit** **4**<br>**0** **=** **De-assert** **Loopback**<br>**1** **=** **Assert** **Loopback**<br>**Bit** **2**<br>**0** **=** **De-assert** **Disable** **Link**<br>**1** **=** **Assert** **Disable** **Link**<br>**Bit** **1**<br>**0** **=** **De-assert** **Hot** **Reset**<br>**1** **=** **Assert** **Hot** **Reset**<br>**Bit** **0**<br>**Training Control**|
||||



A hot reset is initiated in software by setting the Secondary Bus Reset bit in a bridge’s Bridge Control configuration register, as shown in Figure 18‐5 on page 840. Consequently, only devices containing bridges, like the Root Complex or a Switch, can do this. A Switch that receives hot reset on its Upstream Port must broadcast it to all of its Downstream Ports and reset itself. All devices down‐ stream of a switch that receive the hot reset will reset themselves. 

## **Response to Receiving Hot Reset** 

- The device’s LTSSM goes through the Recovery and Hot Reset state, and then back to the Detect state, where it starts the Link Training process. 

- • All of the device’s state machines, hardware logic, port states and configura‐ tion registers (except sticky registers) initialize to their default conditions. 

**837** 

**PCI Ex ress Technolo p gy** 

## **Switches Generate Hot Reset on Downstream Ports** 

A Switch generates a hot reset on all of its Downstream Ports when: 

- It receives a hot reset on its Upstream Port 

- For a Switch or Bridge Upstream Port, if the Data Link Layer reports a DL_Down state, the effect is very similar to a hot reset. This can happen when the Upstream Port has lost its connection with an upstream device due to an error that is not recoverable by the Physical Layer or Data Link Layer. 

- Software sets the ‘Secondary Bus Reset’ bit of the Bridge Control configura‐ tion register associated with the Upstream Port, as shown in Figure 18‐3 on page 838. 

_Figure 18‐3: Switch Generates Hot Reset on One Downstream Port_ 

**==> picture [251 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>FSB<br>PCI Express<br>GFX<br>GFX Root Complex DDR<br>SDRAM<br>‘Secondary Bus Reset’<br>Bit Set<br>Switch A Switch C<br>1<br>Switch B Ethernet10Gb PCI Expressto-PCI SCSI<br>Slots<br>PCI<br>Gb<br>Add-In Ethernet S IEEE<br>IO 1394<br>COM1<br>COM2<br>**----- End of picture text -----**<br>


## **Bridges Forward Hot Reset to the Secondary Bus** 

If a bridge such as a PCI Express‐to‐PCI(‐X) bridge detects a hot reset on its Upstream Port, it must assert the PRST# signal on its secondary PCI(‐X) bus, as illustrated in Figure 18‐4 on page 839. 

## **Software Generation of Hot Reset** 

Software generates a Hot Reset on a specific port by writing a 1 followed by 0 to the ‘Secondary Bus Reset’ bit in the Bridge Control register of that associated 

**838** 

**Cha ter 18: S stem Reset p y** 

port’s configuration header (see Figure 18‐5 on page 840). Consider the example shown in Figure 18‐3 on page 838. Software sets the ‘Secondary Bus Reset’ regis‐ ter of Switch A’s left Downstream Port, causing it to send TS1 Ordered Sets with the Hot Reset bit set. Switch B receives this Hot Reset on its Upstream Port and forwards it to all its Downstream Ports. 

_Figure 18‐4: Switch Generates Hot Reset on All Downstream Ports_ 

**==> picture [277 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>FSB<br>PCI Express<br>GFX<br>GFX Root Complex<br>DDR<br>SDRAM<br>‘Secondary Bus Reset’<br>1<br>Bit is Set<br>Switch A Switch C<br>Switch B Ethernet10Gb PCI Expressto-PCI SCSI<br>Slots<br>PRST#<br>PCI<br>Gb<br>Add-In Ethernet S IEEE<br>IO 1394<br>COM1<br>COM2<br>**----- End of picture text -----**<br>


If software sets the Secondary Bus Reset bit of a Switch’s Upstream Port, then the switch generates a hot reset on all of its Downstream Ports, as shown in Fig‐ ure 18‐4 on page 839. Here, software sets the Secondary Bus Reset bit in Switch C’s Upstream Port, causing it to send TS1s with the Hot Reset bit set on all its Downstream Ports. The PCIe‐to‐PCI bridge receives this Hot Reset and for‐ wards it on to the PCI bus by asserting PRST#. 

Setting the Secondary Bus Reset bit causes a Port’s LTSSM to transition to the Recovery state (for more on the LTSSM, see “Overview of LTSSM States” on page 519) where it generates the TS1s with the Hot Reset bit set. The TS1s are generated continuously for 2 ms and then the Port exits to the Detect state where it is ready to start the Link training process. 

**839** 

**PCI Ex ress Technolo p gy** 

The receiver of the Hot Reset TS1s (always downstream) will go to the Recovery state, too. When it sees two consecutive TS1s with the Hot Reset bit set, it goes to the Hot Reset state for a 2ms timeout and then exits to Detect. Both Upstream and Downstream Ports are initialized and end up in the Detect state, ready to begin Link training. If the downstream device is also a Switch or Bridge, it for‐ wards the Hot Reset to its Downstream Ports as well, as shown in Figure 18‐3 on page 838. 

_Figure 18‐5: Secondary Bus Reset Register to Generate Hot Reset_ 

**==> picture [374 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Doubleword<br>Number<br>Byte (in decimal)<br>15 12 11 10 9 8 7 6 5 4 3 2 1 0 3 2 1 0<br>Reserved 2.2 2.2 2.2 2.2 DeviceID VendorID 00<br>Status Command 01<br>Discard Timer SERR# Enable Register Register<br>Discard Timer Status Class Code Revision 02<br>ID<br>Secondary Discard TimeoutPrimary Discard Timeout BISTBase Add ress 0HeaderType LatencyTimer CacheLineSize 0304<br>Fast Back-to-Back Enable<br>Secondary Bus Reset Base Add ress 1 05<br>Master Abort Mode Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>VGA Enable Secondary I/O I/O 07<br>ISA Enable Status Limit Base<br>SERR# Enable MemoryLimit MemoryBase 08<br>Parity Error Response Prefetchable Prefetchable 09<br>Memory Limit Memory Base<br>Prefetchable Ba se 10<br>Upper 3 2 Bits<br>Prefetchable L imit 11<br>Upper 3 2 Bits<br>I/O Limit I/O Base 12<br>Upper 16 Bits Upper 16 Bits<br>Reserved CapabilityPointer 13<br>Expansion R OM Base Address 14<br>Bridge Interrupt Interrupt 15<br>Control Pin Line<br>Required configuration registers<br>**----- End of picture text -----**<br>


## **Software Can Disable the Link** 

Software can also disable a Link, forcing it to go into Electrical Idle and remain there until further notice. The reason for mentioning that at this point is that disabling the Link also has the effect of causing a Hot Reset on downstream components. Disabling is accomplished by setting the Link Disable bit in the Link Control Register of the Downstream Port, shown in Figure 18‐6 on page 841. That causes the Port to go to the Recovery LTSSM state and begin sending TS1s with the Disable bit set. Since this can only be controlled for Downstream Ports if the Link has been disabled, this bit is reserved for Upstream Ports (such as Endpoints or Switch Upstream Ports). 

**840** 

**Cha ter 18: S stem Reset p y** 

## _Figure 18‐6: Link Control Register_ 

**==> picture [346 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


When the Upstream Port recognizes incoming TS1s with the Disabled bit set, its Physical Layer signals LinkUp=0 (false) to the Link Layer and all the Lanes go to Electrical Idle. After a 2ms timeout, an Upstream Port will go to Detect, but a Downstream Port will remain in the Disabled LTSSM state until directed to exit from it (such as by clearing the Link Disable bit), so the Link will remain dis‐ abled and will not attempt training until then. 

**841** 

**PCI Ex ress Technolo p gy** 

## _Figure 18‐7: TS1 Ordered‐Set Showing Disable Link Bit_ 

**==> picture [366 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
TS1 Training Control<br>Bit 0 0 = De-assert Hot Reset<br>0 COM K28.5<br>1 = Assert Hot Reset<br>1 Link # D0.0-D31.7, K23.7 (0-255)<br>2 Lane # D0.0-D31.0, K23.7 (0-31) Bit 1 0 = De-assert Disable Link<br># of FTS ordered sets required by<br>3 # FTS receiver to obtain bit and symbol lock 1 = Assert Disable Link<br>4 Rate ID<br>5 Train Ctl Bit 2 0 = De-assert Loopback<br>6 1 = Assert Loopback<br>TS ID D10.2 for TS1 Identifier Bit 3 0 = De-assert Disable Scrambling<br>1 = Assert Disable Scrambling<br>13<br>14 TS ID D10.2 for TS1 Identifier Bit 4 0 = De-assert Compliance Receive<br>15 TS ID D10.2 for TS1 Identifier 1 = Assert Compliance Receive<br>Bit 5:7 Reserved<br>**----- End of picture text -----**<br>


## **Function Level Reset (FLR)** 

The FLR capability allows software to reset just one Function within a multi‐ function device without affecting the Link that is shared by them all. Its imple‐ mentation is strongly recommended but isn’t required, so software would need to confirm its availability before attempting to use it by examining the Device Capabilities register, as shown in Figure 18‐8 on page 843. If the Function‐Level Reset Capability bit is set, then an FLR can be initiated by simply setting the Ini‐ tiate Function‐Level Reset bit in the Device Control Register as shown in Figure 18‐9 on page 843. 

**842** 

**Cha ter 18: S stem Reset p y** 

_Figure 18‐8: Function‐Level Reset Capability_ 

## _Figure 18‐9: Function‐Level Reset Initiate Bit_ 

**843** 

The spec mentions a few examples that motivate the addition of FLR: 

1. It can happen that software controlling a Function encounters a problem and is no longer operating correctly. Preventing data corruption necessi‐ tates a reset of that Function, but if other Functions within that device are still working properly it would nice to be able to reset just the one having trouble.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-6"></a>
## 17.6 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

2. In a virtualized environment, where applications can migrate from one piece of hardware to another, it’s important that when an application is moved off a Function that the Function doesn’t retain any information about what it was doing. This prevents information used by one application that might be considered confidential from becoming visible to the new one running on that Function. The simplest way to clean up after migrating the previous application is simply to reset the Function. 

3. When software is rebuilding a software stack for a Function, it is sometimes necessary to first put the Function into an uninitialized state. As before, avoiding a reset of all Functions sharing the Link is desirable. 

Another feature doesn’t appear in the list of cases in the spec but is still a moti‐ vating factor in its own right. While a conventional reset will re‐initialize every‐ thing within the device, it does not require that all external activity, such as traffic on a network interface, must cease right away. FLR adds this requirement and is the only reset that does. 

FLR resets the Function’s internal state and registers, making it quiescent, but doesn’t affect any sticky bits, or hardware‐initialized bits, or link‐specific regis‐ ters like Captured Power, ASPM Control, Max_Payload_Size or Virtual Channel registers. If an outstanding Assert INTx interrupt message was sent, a corre‐ sponding Deassert INTx message must be sent, unless that interrupt was shared by another Function internally that still has it asserted. All external activity for that Function is required to cease when an FLR is received. 

## **Time Allowed** 

A Function must complete an FLR within 100ms. However, software may need to delay initiating an FLR if there are any outstanding split completions that haven’t yet been returned (indicated by the fact that the Transactions Pending bit remains set in the Device Status register). In that case, software must either wait for them to finish before initiating the FLR, or wait 100ms after FLR before attempting to re‐initialize the Function. If this isn’t managed, a potential data corruption problem arises: a Function may have split transactions outstanding but a reset causes it to lose track of them. If they are returned later they could be 

**Cha ter 18: S stem Reset p y** 

mistaken for responses to new requests that have been issued since the FLR. To avoid this problem, the spec recommends that software should: 

1. Coordinate with other software that might access the Function to ensure it doesn’t attempt access during the FLR. 

2. Clear the entire Command register, thereby quiescing the Function. 

3. Ensure that previously‐requested Completions have been returned by poll‐ ing the Transactions Pending bit in the Device Status register until it’s cleared or waiting long enough to be sure the Completions won’t ever be returned. How long would be long enough? If Completion Timeouts are being used, wait for the timeout period before sending the FLR. If Comple‐ tion Timeouts are disabled, then wait at least 100ms. 

4. Initiate the FLR and wait 100ms. 

5. Set up the Function’s configuration registers and enable it for normal opera‐ tion. 

When the FLR has completed, regardless of the timing, the Transaction Pending bit must be cleared. 

## **Behavior During FLR** 

The spec writers chose to describe the behavior of a Function reset in fairly broad terms so as not to preclude any internal steps that designers might wish to take. The following behaviors are listed in the spec: 

- The Function must not appear to an external interface as though it was an initialized adapter with an active host. The steps to ensure that all activity on external interfaces is terminated will be design specific. An example would be a network adapter that must not respond to requests that would require an active host during this time. 

- The Function must not retain any software‐readable state that might include secret information left behind by some previous use of the Func‐ tion. For example, any internal memory must be cleared or randomized. 

- The Function must be configurable as normal by the next driver. 

- The Function must return a completion for the configuration write that caused the FLR and then initiate the FLR. 

While an FLR is in progress: 

- Any requests that arrive are allowed to be silently discarded without log‐ ging them or signaling an error. Flow control credits must be updated to maintain the link operation, though. 

**845** 

## **PCI Ex ress Technolo p gy** 

- Incoming completions can be treated as Unexpected Completions or silently discarded without logging them or signaling an error. 

- The FLR itself must be completed within the time described above, but fur‐ ther initialization after that could take longer. If a configuration Request comes in before initialization is completed, the Function must return a com‐ pletion with CRS (Configuration Retry Status) status. Once a completion is returned with any other status, a CRS status will not be legal again until the Function is reset again. 

## **Reset Exit** 

After exiting the reset state, Link Training and Initialization must begin within 20 ms. Devices may exit the reset state at different times, since reset signaling is asynchronous, but must begin training within this time. 

To allow reset components to perform internal initialization, system software must wait for at least 100 ms from the end of a reset before attempting to send Configuration Requests to them. If software initiates a configuration request to a device after the 100 ms wait time, but the device still hasn’t finished its self‐ini‐ tialization, it returns a Completion with status CRS. Since configuration Requests can only be initiated by the CPU, the Completion will be returned to the Root Complex. In response, the Root may re‐issue the configuration Request automatically or make the failure visible to software. The spec also states that software should only use 100ms wait periods if CRS Software Visibility has been enabled, since long timeouts or processor stalls may otherwise result. 

Devices are allowed a full 1.0 second (‐0%/+50%) after a reset before they must give a proper response to a configuration request. Consequently, the system must be careful to wait that long before deciding that an unresponsive device is broken. This value is inherited from PCI and the reason for this lengthy delay may be that some devices implement configuration space as a local memory that must be initialized before it can be seen correctly by configuration software. Its initialization may involve copying the necessary information from a slow serial EEPROM, and so it might take some time. 

**846** 

## _**19 Hot Plug and Power Budgeting**_ 

## **The Previous Chapter** 

The previous chapter describes three types of resets defined for PCIe: Funda‐ mental reset (consisting of cold and warm reset), hot reset, and function‐level reset (FLR). The use of a side‐band reset PERST# signal to generate a system reset is discussed, and so is the in‐band TS1 based Hot Reset described. 

## **This Chapter** 

This chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it’s important to ensure that its power needs don’t exceed what the system can deliver. A mechanism was needed to query the power requirements of a device before giving it permission to operate. Power budgeting registers provide that. 

## **The Next Chapter** 

The next chapter describes the changes and new features that were added with the 2.1 revision of the spec. Some of these topics, like the ones related to power management, are described in earlier chapters, but for others there wasn’t another logical place for them. In the end, it seemed best to group them all together in one chapter to ensure that they were all covered and to help clarify what features are new. 

**847** 

**PCI Ex ress Technolo p gy** 

## **Background** 

Some systems using PCIe require high availability or non‐stop operation. Online service suppliers require computer systems that experience downtimes of just a few minutes a year or less. There are many aspects to building such sys‐ tems, but equipment reliability is clearly important. To facilitate these goals PCIe supports the Hot Plug/Hot Swap solutions for add‐in cards that provide three important capabilities: 

1. a method of replacing failed expansion cards without turning the system off 2. keeping the O/S and other services running during the repair 3. shutting down and restarting software associated with a failed device 

Prior to the widespread acceptance of PCI, many proprietary Hot Plug solu‐ tions were developed to support this type of removal and replacement of expansion cards. The original PCI implementation did not support hot removal and insertion of cards, but two standardized solutions for supporting this capa‐ bility in PCI have been developed. The first is the Hot Plug PCI Card used in PC Server motherboard and expansion chassis implementations. The other is called Hot Swap and is used in CompactPCI systems based on a passive PCI back‐ plane implementation. 

In both solutions, control logic is used to electrically isolate the card logic from the shared PCI bus. Power, reset, and clock are controlled to ensure an orderly power down and power up of cards as they are removed and replaced, and sta‐ tus and power LEDs inform the user when it’s safe to change a card. 

Extending hot plug support to PCI Express cards is an obvious step, and designers have incorporated some Hot Plug features as “native” to PCIe. The spec defines configuration registers, Hot Plug Messages, and procedures to sup‐ port Hot Plug solutions. 

## **Hot Plug in the PCI Express Environment** 

PCIe Hot Plug is derived from the 1.0 revision of the Standard Hot Plug Con‐ troller spec (SHPC 1.0) for PCI. The goals of PCI Express Hot Plug are to: 

- Support the same “Standardized Usage Model” as defined by the Standard Hot Plug Controller spec. This ensures that the PCI Express hot plug is identical from the user perspective to existing implementations based on the SHPC 1.0 spec 

**848** 

**Chapter 19: Hot Plug and Power Budgeting** 

- Support the same software model implemented by existing operating sys‐ tems. However, an OS using a SHPC 1.0 compliant driver won’t work with PCI Express Hot Plug controllers because they have a different program‐ ming interface. 

The registers necessary to support a Hot Plug Controller are integrated into individual Root and Switch Ports. Under Hot Plug software control, these con‐ trollers and the associated port interface must control the card interface signals to ensure orderly power down and power up as cards are changed. To accom‐ plish that, they’ll need to: 

- Assert and deassert the PERST# signal to the PCI Express card connector 

- • Remove or apply power to the card connector. 

- Selectively turn on or off the Power and Attention Indicators associated with a specific card connector to draw the user’s attention to the connector and indicate whether power is applied to the slot. 

- Monitor slot events (e.g. card removal) and report them to software via interrupts. 

PCI Express Hot‐Plug (like PCI) is designed as a “no surprises” Hot‐Plug meth‐ odology. In other words, the user is not normally allowed to install or remove a PCI Express card without first notifying the system. Software then prepares both the card and slot and finally indicates to the operator the status of the hot plug process and notification that installation or removal may now be per‐ formed. 

## **Surprise Removal Notification**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-7"></a>
## 17.7 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Cards designed to the PCIe Card ElectroMechanical spec (CEM) implement card presence detect pins (PRSNT1# and PRSNT2#) on the connector. These pins are shorter than the others so that they break contact first (when the card is removed from the slot). This can be used to give advanced notice to software of a “surprise” removal, allowing time to remove power before the signals break contact. 

## **Differences between PCI and PCIe Hot Plug** 

The elements needed to support hot plug are essentially the same in both PCI and PCIe hot plug solutions. Figure 19‐1 on page 850 shows the PCI hardware and software elements required to support hot plug. PCI solutions implement a single standardized hot plug controller on the system board that handled all the 

**849** 

## **PCI Ex ress Technolo p gy** 

hot plug slots on the bus. Isolation logic is needed in the PCI environment to electrically disconnect a card from the shared bus prior to making changes to avoid glitching the signals on an active bus. 

PCIe uses point‐to‐point connections (see Figure 19‐2 on page 851) that elimi‐ nate the need for isolation logic but require a separate hot plug controller for each Port to which a connector is attached. A standardized software interface defined for each Root and Switch Port controls hot plug operations. 

_Figure 19‐1: PCI Hot Plug Elements_ 

**850** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Figure 19‐2: PCI Express Hot‐Plug Elements_ 

**851** 

**PCI Ex ress Technolo p gy** 

## **Elements Required to Support Hot Plug** 

As shown in Figure 19‐2 on page 851 there are several parts involved in making a hog‐plug environment work. For discussion, let’s break these down into soft‐ ware and hardware elements. 

## **Software Elements** 

The following table describes the major software elements that support Hot‐ Plug capability. 

_Table 19‐1: Introduction to Major Hot‐Plug Software Elements_ 

|**Software Element**|**Supplied by**|**Description**|
|---|---|---|
|User Interface|OS vendor|An OS‐supplied utility that permits the<br>user to request that a connector be pow‐<br>ered off to remove a card or turned on to<br>use a card that has just been installed.|
|Hot‐Plug Service|OS vendor|A service that processes requests<br>(referred to as Hot‐Plug Primitives)<br>issued by the OS. This includes requests<br>to:<br>• provide slot identifiers<br>• turn card power On or Off<br>• turn Attention Indicator On or Off<br>• read current power of slot (On or Off)<br>The Hot‐Plug Service interacts with the<br>Hot‐Plug System Driver to satisfy the<br>requests. The interface (i.e., API) with<br>the Hot‐Plug System Driver is defined<br>by the OS vendor.|
|Standardized Hot‐<br>Plug System Driver|System Board<br>vendor or OS|Receives requests (Hot‐Plug Primitives)<br>from the Hot‐Plug Service within the<br>OS. Interacts with the hardware Hot‐<br>Plug Controllers to accomplish requests.|



**852** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐1: Introduction to Major Hot‐Plug Software Elements (Continued)_ 

|**Software Element**|**Supplied by**|**Description**|
|---|---|---|
|Device Driver|Adapter card<br>vendor|Some Hot‐Plug‐specific capabilities<br>must be incorporated in a Hot‐Plug‐<br>capable device driver. This includes:<br>• support for the**Quiesce**command.<br>• optional support of the**Pause**com‐<br>mand.<br>• Support for**Start**command or<br>optional**Resume**command.|



A Hot‐Plug‐capable system may use an OS that doesn’t support Hot‐Plug capa‐ bility. In that case, although the system BIOS would contain Hot‐Plug‐related software, the Hot‐Plug Service would not be present. Assuming that the user doesn’t attempt hot insertion or removal of a card, the system will operate as a standard, non‐Hot‐Plug system: 

- The system startup firmware must ensure that all Attention Indicators are Off. 

- The spec also states: “the Hot‐Plug slots must be in a state that would be appropriate for loading non‐Hot‐Plug system software.” 

## **Hardware Elements** 

Table 19‐2 on page 853 lists the major hardware elements necessary to support PCI Express Hot‐Plug operation. 

_Table 19‐2: Major Hot‐Plug Hardware Elements_ 

|**Hardware Element**|**Description**|
|---|---|
|Hot‐Plug Controller|Receives and processes commands issued by the<br>Hot‐Plug System Driver. One Controller is associ‐<br>ated with each Root or Switch Port that supports<br>hot plug operation. The PCIe spec defines a stan‐<br>dard software interface for the Hot‐Plug Control‐<br>ler.|



**853** 

## **PCI Ex ress Technolo p gy** 

_Table 19‐2: Major Hot‐Plug Hardware Elements (Continued)_ 

|**Hardware Element**|**Description**|
|---|---|
|Card Slot Power Switching<br>Logic|Allows power to a slot to be turned on or off under<br>program control. Controlled by the Hot Plug con‐<br>troller under the direction of the Hot‐Plug System<br>Driver.|
|Card Reset Logic|Hot Plug Controller drives the PERST# signal to a<br>specific slot as directed by the Hot‐Plug System<br>Driver.|
|Power Indicator|Indicates whether power is currently active on the<br>connector. Controlled by the Hot Plug logic associ‐<br>ated with each port and directed by the Hot Plug<br>System Driver.|
|Attention Indicator|Draws operator attention to a connector that needs<br>service. Controlled by the Hot Plug logic and<br>directed by the Hot‐Plug System Driver.|
|Attention Button|Pressed by the operator to notify Hot Plug soft‐<br>ware of a request to change a card.|
|Card Present Detect Pins|There are two of these: PRSNT1# is located at one<br>end of the card slot and PRSNT2# at the opposite<br>end. These pins are shorter than the others so that<br>they disconnect first when a card is removed. The<br>system board ties PRSNT1# to ground and con‐<br>nects PRSNT2# as an input to the Hot‐Plug Con‐<br>troller with a pull‐up resistor. Additional PRSNT2#<br>pins are defined for wider connectors to support<br>the insertion and recognition of shorter cards<br>installed into longer connectors. The card itself<br>shorts PRSNT1# to PRSNT2#, so that the PRSNT2#<br>input is high if a card is not physically plugged in<br>or low if it is.|



**854** 

**Chapter 19: Hot Plug and Power Budgeting** 

## **Card Removal and Insertion Procedures** 

The descriptions of typical card removal and insertion that follow are intended to be introductory in nature. It should be noted that the procedures described in the following sections assume that the OS, rather than the Hot‐Plug System Driver, is responsible for configuring a newly‐installed device. If the Hot‐Plug System Driver has this responsibility, the Hot‐Plug Service will call the Hot‐ Plug System Driver and instruct it to configure the newly‐installed device. 

## **On and Off States** 

A slot in the On state has the following characteristics: 

- Power is applied to the slot. 

- REFCLK is on. 

- The link is active or in an Active State Power Management state. 

- The PERST# signal is deasserted. 

A slot in the Off state has the following characteristics: 

- Power to the slot is turned off. 

- REFCLK is off. 

- The link is inactive. (Driver at the root of switch port is in Hi Z state) 

- The PERST# signal is asserted. 

## **Turning Slot Off** 

Steps required to turn off a slot that is currently in the On state: 

1. Deactivate the link. This may involve issuing a EIOS to enter the Hi Z state. 

2. Assert the PERST# signal to the slot. 

3. Turn off REFCLK to the slot. 

4. Remove power from the slot. 

## **Turning Slot On** 

Steps to turn on a slot that is currently in the off state: 

1. Apply power to the slot. 

2. Turn on REFCLK to the slot 

**855** 

## **PCI Ex ress Technolo p gy** 

3. Deassert the PERST# signal to the slot. The system must meet the setup and hold timing requirements (specified in the PCI Express spec) relative to the rising edge of PERST#. 

Once power and clock have been restored and PERST# removed, the physical layers at both ports will perform link training and initialization. When the link is active, the devices will initialize VC0 (including flow control), making the link ready to transfer TLPs. 

## **Card Removal Procedure** 

When a card is to be removed, a number of steps are needed to prepare software and hardware for safe removal of the card, and set the indicators for the card being processed. The condition of the indicators during normal operation are: 

- Attention Indicator (Amber or Yellow) — “Off” during normal operation. 

- Power Indicator (Green) — “On” during normal operation 

Software sends requests to the Hot Plug Controller using configuration writes that target the Slot Control Registers implemented by Hot‐Plug capable ports. These control the power to the slot and the state of the indicators. 

The sequence of events is as follows: 

1. The operator requests card removal by pressing the slot’s attention button or by using the system’s user interface to select the Physical Slot number of the card to be removed. If the button was used, the Hot‐Plug Controller detects this event and delivers an interrupt to the root complex. The inter‐ rupt directs the Hot Plug service to call the Hot Plug System Driver to read slot status information and detect the Attention Button request. 

2. Next, the Hot‐Plug Service commands the Hot‐Plug System Driver to blink the slot’s Power Indicator as visual feedback to the operator for 5 seconds. If this was initiated by pressing the Attention button, the operator can press the button a second time to cancel the request during this 5‐second interval. 

3. The Power Indicator continues to blink while the Hot Plug software vali‐ dates the request. If the card is currently in use for some critical system operation, software may deny the request. In that case, it will issue a com‐ mand to the Hot Plug controller to turn the Power Indicator back ON. The spec also recommends that software notify the operator, perhaps with a message or by logging an entry indicating the reason the request was denied. 

**856** 

**Chapter 19: Hot Plug and Power Budgeting** 

4. If the request is validated, the Hot‐Plug Service utility commands the card’s device driver to quiesce the device. That is, disable its ability to generate new Requests and complete or terminate all outstanding Root or Switch Port requests. 

5. Software then issues a command to disable the card’s Link via the Link Con‐ trol register in the Root or Switch Port to which the slot is attached. 

6. Next, software commands the Hot Plug Controller to turn the slot off. 

7. Following successful power down, software issues the Power Indicator Off Request to turn off the power indicator so the operator knows the card may be removed. 

8. The operator releases the Mechanical Retention Latch, if there is one, caus‐ ing the Hot Plug Controller to remove all switched signals from the slot (e.g., SMBus and JTAG signals). The card can now be removed. 

9. The OS deallocates the memory space, IO space, interrupt line, etc. that had been assigned to the device and makes these resources available for assign‐ ment to other devices in the future. 

## **Card Insertion Procedure** 

The procedure for installing a new card basically reverses the steps listed for card removal. The following steps assume that the slot was left in the same state that it was in immediately after a card was removed from the connector (in other words, the Power Indicator is in the Off state, indicating the slot is ready for card insertion). 

The steps taken to Insert and enable a card are as follows: 

1. The operator installs the card and secures the MRL. If implemented, the MRL sensor will signal the Hot‐Plug Controller that the latch is closed, causing switched auxiliary signals and Vaux to be connected to the slot. 

2. Next, the operator notifies the Hot‐Plug Service that the card has been installed by pressing the Attention Button or using the Hot Plug Utility pro‐ gram to select the slot.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-8"></a>
## 17.8 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

3. If the button was pressed, it signals the Hot Plug controller of the event, resulting in status register bits being set and causing a system interrupt to be sent to the Root Complex. Subsequently, Hot Plug software reads slot status from the port and recognizes the request. 

4. The Hot‐Plug Service issues a request to the Hot‐Plug System Driver com‐ manding the Hot Plug Controller to blink the slot’s Power Indicator to inform the operator that the card must not be removed. The operator is granted a 5 second abort interval, from the time that the indicators starts to blink, to abort the request by pressing the button a second time. 

**857** 

## **PCI Ex ress Technolo p gy** 

5. The Power Indicator continues to blink while Hot Plug software validates the request. Note that software may fail to validate the request (e.g., the security policy settings may prohibit the slot being enabled). If the request is not validated, software will issue a command to the Hot Plug controller to turn the Power Indicator back OFF. The spec recommends that software notify the operator via a message or by logging an entry indicating the cause of the request denial. 

6. The Hot‐Plug Service issues a request to the Hot‐Plug System Driver com‐ manding the Hot Plug Controller to turn the slot on. 

7. Once power is applied, software issues a command to turn the Power Indi‐ cator ON. 

8. Once link training is complete, the OS commands the Platform Configura‐ tion Routine to configure the card function(s) by assigning the necessary resources. 

9. The OS locates the appropriate driver(s) (using the Vendor ID and Device ID, or the Class Code, or the Subsystem Vendor ID and Subsystem ID con‐ figuration register values as search criteria) for the function(s) within the PCI Express device and loads it (or them) into memory. 

10. The OS then calls the driver’s initialization code entry point, causing the processor to execute the driver’s initialization code. This code finishes the setup of the device and then sets the appropriate bits in the device’s PCI configuration Command register to enable the device. 

## **Standardized Usage Model** 

## **Background** 

Systems based on the original 1.0 version of the PCI Hot Plug spec implemented hardware and software designs that varied widely because the spec did not define standardized registers or user interfaces. Consequently, customers who purchased Hot Plug capable systems from different vendors were confronted with a wide variation in user interfaces that required retraining operators when new systems were purchased. Furthermore, every board designer was required to write software to manage their implementation‐specific hot plug controller. The 1.1 revision of the PCI Hot‐Plug Controller (HPC) spec defines: 

- a standard user interface that eliminates retraining of operators 

- a standard programming interface for the hot plug controller, which per‐ mits a standardized hot plug driver to be incorporated into the operating system. PCI Express implements registers not defined by the HPC spec, 

**858** 

**Chapter 19: Hot Plug and Power Budgeting** 

hence the standard Hot Plug Controller driver implementations for PCI and PCI Express are slightly different. 

## **Standard User Interface** 

The user interface includes the following features: 

- Attention Indicator — shows the attention state of the slot with an LED that is on, off, or blinking. The spec defines the blinking frequency as 1 to 2 Hz and 50% (+/‐ 5%) duty cycle. The state of this indicator is strictly under soft‐ ware control. 

- Power Indicator (called Slot State Indicator in PCI HP 1.1) — shows the power status of the slot and also can be on, off, or blinking (at 1 to 2 Hz and 50% (+/‐ 5%) duty cycle). This indicator is controlled by software; however, the spec permits an exception in the event of a hardware power fault condi‐ tion. 

- Manually Operated Retention Latch and Optional Sensor — secures card within slot and notifies the system when the latch is released 

- Electromechanical Interlock (optional) — locks the card or retention latch to prevent the card from being removed while power is applied. 

- Software User Interface — allows operator to request hot plug operation 

- Attention Button — allows operator to manually request hot plug opera‐ tion. 

- Slot Numbering Identification — provides visual identification of slot on the board. 

## **Attention Indicator** 

As mentioned in the previous section, the spec requires the system vendor to include an Attention Indicator associated with each Hot‐Plug slot. This indica‐ tor must be located in close proximity to the corresponding slot and is yellow or amber in color. This Indicator draws the attention of the end user to the slot for service. The spec makes a clear distinction between operational and validation errors and does not permit the attention indicator to report validation errors. Validation errors are problems detected and reported by software prior to beginning the hot plug operation. The behavior of the Attention Indicator is listed in Table 19‐3 on page 860. 

**859** 

**PCI Ex ress Technolo p gy** 

_Table 19‐3: Behavior and Meaning of the Slot Attention Indicator_ 

|**Indicator Behavior**|**Attention State**|
|---|---|
|Off|Normal — Normal Operation|
|On|Attention — Hot Plug Operation Failed due to an oper‐<br>ational problem (e.g., problems with external cabling,<br>add‐in cards, software drivers, and power faults)|
|Blinking|Locate — Slot is being identified at operator’s request|



## **Power Indicator** 

The power indicator simply reflects the state of main power at the slot, and is controlled by Hot Plug software. The color of this indicator is green and is illu‐ minated when power to the slot is “on.” 

The spec specifically prohibits Root or Switch Port hardware from changing the power indicator state autonomously as a result of power fault or other events. A single exception to this rule allows a platform to detect stuck‐on power faults. A stuck‐on fault is simply a condition in which commands issued to remove slot power are ineffective. If the system is designed to detect this condition the sys‐ tem may override the Root or Switch Port’s command to turn the power indica‐ tor off and force it to remain on. This notifies the operator that the card should not be removed from the slot. The spec further states that supporting stuck‐on faults is optional and, if handled via system software, “the platform vendor must ensure that this optional feature of the Standard Usage Model is addressed via other software, platform documentation, or by other means.” 

The behavior of the power indicator and the related power states are listed in Table 19‐4 on page 861. Note that Vaux remains on and switch signals are still connected until the retention latch is released or when the card is removed as detected by the Prsnt1# and Prsnt2# signals. 

**860** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐4: Behavior and Meaning of the Power Indicator_ 

|**Indicator Behavior**|**Power State**|
|---|---|
|Off|Power Off — it is safe to remove or insert a card. All power<br>has been removed as required for hot plug operation. Vaux is<br>only removed when the Manual Retention Latch is released.|
|On|Power On — removal or insertion of a card is not allowed.<br>Power is currently applied to the slot.|
|Blinking|Power Transition — card removal or insertion is not allowed.<br>This state notifies the operator that software is currently<br>removing or applying slot power in response to a hot plug<br>request.|



## **Manually Operated Retention Latch and Sensor** 

The Manual Retention Latch (MRL) is required and holds PCI Express cards rig‐ idly in the slot. Each MRL can implement an optional sensor that notifies the Hot‐Plug Controller that the latch has been closed or opened. The spec also allows a single latch that can hold down multiple cards. Such implementations do not support the MRL sensor. 

An MRL Sensor is a switch, optical device, or other type of sensor that reports whether the latch is closed or open. If an unexpected latch release is detected, the port automatically disables the slot and notifies system software, although changing the state of the Power or Attention indicators autonomously is not allowed. 

The switched signals and auxiliary power (Vaux) must be automatically removed from the slot when the MRL Sensor indicates that the MRL is open, and they must be restored to the slot when the MRL Sensor indicates that the latch is closed. The switched signals are Vaux, SMBCLK, and SMBDAT. 

The spec also describes an alternate method for removing Vaux and SMBus power when an MRL sensor is not present. The PRSNT#2 pin indicates whether a card is physically installed into the slot and can be used to trigger the port to remove the switched signals. 

**861** 

**PCI Ex ress Technolo p gy** 

## **Electromechanical Interlock (optional)** 

The optional electromechanical card interlock mechanism provides a more sophisticated method of ensuring that a card is not removed while power is applied to the slot. The spec does not define the specific nature of the interlock, but states that it can physically lock the add‐in card or the MRL in place. 

The lock mechanism is controlled via software; however, there is no specific programming interface defined for it. Instead, an interlock is controlled by the same Port signal that enables main power to the slot. 

## **Software User Interface** 

An operator may use a software interface to request card removal or insertion. This interface is provided by system software, which also monitors slots and reports status information to the operator. The spec states that the user interface is implemented by the Operating System and consequently is beyond the scope of the spec. 

The operator must be able to initiate operations at each slot independent of other slots. Consequently, the operator may initiate a hot‐plug operation on one slot using the software user interface or attention button while a hot‐plug oper‐ ation on another slot is in process. This can be done regardless of which inter‐ face the operator used to start the first Hot‐Plug operation. 

## **Attention Button** 

The Attention Button is a momentary‐contact push‐button switch, located near the corresponding Hot‐Plug slot or on a module. The operator presses this but‐ ton to initiate a hot‐plug operation for this slot (e.g., card removal or insertion). Once the Attention Button is pressed, the Power Indicator starts to blink. From the time the blinking begins the operator has 5 seconds to abort the Hot Plug operation by pressing the button a second time. 

The spec recommends that if an operation initiated by an Attention Button fails, the system software should notify the operator of the failure. For example, a message explaining the nature of the failure can be reported or logged. 

## **Slot Numbering Identification** 

Software and operators must be able to identify a physical slot based on its slot number. Each hot‐plug capable port must implement registers that software uses to identify the physical slot number. The registers include a Physical Slot 

**862** 

**Chapter 19: Hot Plug and Power Budgeting** 

number and a chassis number. The main chassis is always labeled chassis 0. The chassis numbers for other chassis must be non‐zero and are assigned via the PCI‐to‐PCI bridge’s Chassis Number register. 

## **Standard Hot Plug Controller Signaling Interface** 

Figure 19‐3 on page 864 presents a more detailed view of the logic within Switch Ports, along with the signals routed between the slot and the Port. The importance of the standardized Hot Plug Controller is the common software interface that allows the device driver to be integrated into operating systems.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-17-9"></a>
## 17.9 Interrupt Support | 中断支持

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The PCIe spec, together with the Card ElectroMechanical (CEM) spec, defines the slot signals and the support required for Hot Plug PCI Express. Following is a list of required and optional port interface signals needed to support the Stan‐ dard Usage Model: 

- PWRLED# (required) — port output that controls state of Power Indicator 

- ATNLED# (required) — port output controls state of Attention Indicator 

- PWREN (required if reference clock is implemented) — port output that controls main power to slot 

- REFCLKEN# (required) — port output that controls delivery of reference clock to the slot 

- PERST# (required) — port output that controls PERST# at slot 

- PRSNT1# (required) — Grounded at the connector 

- PRSNT2# (required) — port input, pulled up on system board, that indi‐ cates presence of card in slot. 

- PWRFLT# (required) — port input that notifies the Hot‐Plug controller of a power fault condition detected by external logic 

- AUXEN# (required if AUX power is implemented) — port output that con‐ trols switched AUX signals and AUX power to slot when MRL is opened and closed. The MRL# signal is required with AUX power is present. 

- MRL# (required if MRL Sensor is implemented) — port input from the MRL sensor 

- BUTTON# (required if Attention Button is implemented) — port input indi‐ cating operator has pressed the Attention Button. 

**863** 

**PCI Ex ress Technolo p gy** 

_Figure 19‐3: Hot Plug Control Functions within a Switch_ 

## **The Hot-Plug Controller Programming Interface** 

The standard programming interface to the Hot‐Plug Controller is provided via the PCI Express Capability register block, shown in Figure 19‐4 on page 865, where the Hot‐Plug related registers are highlighted. Hot Plug features are pri‐ 

**864** 

**Chapter 19: Hot Plug and Power Budgeting** 

marily found in the Slot Registers defined for Root and Switch Ports. The Device Capability register is also used in some implementations as described later in this chapter. 

_Figure 19‐4: PCIe Capability Registers Used for Hot‐Plug_ 

**==> picture [263 x 305] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 15 7 0<br>PCI Express Capabilities Register Next Cap Pointer PCI ExpressCap ID DW0<br>Device Capabilities Register DW1<br>Device Status Device Control DW2<br>Link Capabilities DW3<br>Link Status Link Control DW4<br>Slot Capabilities DW5<br>Slot Status Slot Control DW6<br>Root Capability Root Control DW7<br>Root Status DW8<br>Device Capabilities 2 DW9<br>Device Status 2 Device Control 2 DW10<br>Link Capabilities 2 DW11<br>Link Status 2 Link Control 2 DW12<br>Slot Capabilities 2 DW13<br>Slot Status 2 Slot Control 2 DW14<br>**----- End of picture text -----**<br>


## **Slot Capabilities** 

Figure 19‐5 on page 866 illustrates the slot capability register and bit fields. Hardware initializes all of these capability register fields to reflect the features implemented by this port. This register applies to both card slots and rack mount implementations, except for the indicators and attention button. Soft‐ ware must read from the device capability register within the module to deter‐ mine if indicators and attention buttons are implemented. Table 19‐5 on page 866 lists and defines the slot capability fields. 

**865** 

**PCI Ex ress Technolo p gy** 

_Figure 19‐5: Slot Capabilities Register_ 

||Hot Plug Surprise<br>Slot Power Limit Scale<br>5<br>0<br>6<br>7<br>31<br>14<br>3 2<br>4<br>15<br>16<br>18 17<br>19<br>Attention Button Present<br>Power Controller Present<br>MRL Sensor Present<br>Attention Indicator Present<br>Electromechanical Interlock Present<br>Physical Slot Number<br>Slot Power Limit Value<br>Hot Plug Capable<br>Power Indicator Present<br>No Command Completed Support|Hot Plug Surprise<br>Slot Power Limit Scale<br>5<br>0<br>6<br>7<br>31<br>14<br>3 2<br>4<br>15<br>16<br>18 17<br>19<br>Attention Button Present<br>Power Controller Present<br>MRL Sensor Present<br>Attention Indicator Present<br>Electromechanical Interlock Present<br>Physical Slot Number<br>Slot Power Limit Value<br>Hot Plug Capable<br>Power Indicator Present<br>No Command Completed Support|
|---|---|---|
||**Bit(s)**|**Register Name and Description**|
||0|**Attention Button Present**— indicates the presence of an attention button<br>on the chassis adjacent to the slot.|
||1|**Power Controller Present**— indicates the presence of a power controller<br>for this slot.|
||2|**MRL Sensor Present**— indicates the presence of a MRL Sensor on the<br>slot.|
||3|**Attention Indicator Present**— indicates the presence of an attention indi‐<br>cator on the chassis adjacent to the slot.|
||4|**Power Indicator Present**— indicates the presence of a power indicator on<br>the chassis adjacent to the slot.|



**866** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐5: Slot Capability Register Fields and Descriptions (Continued)_ 

|**Bit(s)**|**Register Name and Description**|
|---|---|
|5|**Hot‐Plug Surprise**— indicates that it’s possible for the user to remove the<br>card from the system without prior notification. This tells the OS to allow<br>for such removal without affecting continued software operation.|
|6|**Hot‐Plug Capable**— indicates that this slot supports hot plug operation.|
|14:7|**Slot Power Limit Value**— specifies the maximum power that can be sup‐<br>plied by this slot. This limit value is multiplied by the scale specified in the<br>next field.|
|16:15|**Slot Power Limit Scale**— specifies the scaling factor for the Slot Power<br>Limit Value.|
|17|**ElectroMechanical Interlock Present**— indicates that this is implemented<br>for this slot|
|18|No Command Completed Support— indicates that this slot doesn’t gener‐<br>ate software notification when a command has been completed. Earlier<br>versions sometimes took a long time to execute hot‐plug commands (for<br>example, sometimes taking a second or more to communicate across an<br>I2C bus to turn the power on or off), and generated an interrupt when they<br>were finally done. When set this bit means that this Port can accept writes<br>to all fields in the Slot Control register without delay, so there’s no need for<br>the notification.|
|31:19|P**hysical Slot Number**— Indicates the physical slot number associated<br>with this port. It must be hardware initialized to a number that is unique<br>within the chassis. Note that software will need this number to relate the<br>physical slot to the Logical Slot ID (Bus, Device, & Function number for<br>this device).|



## **Slot Power Limit Control** 

The spec provides a method for software to limit the amount of power con‐ sumed by a card installed into an expansion slot or backplane implementation. The registers to support this feature are included in the Slot Capability register. 

**867** 

**PCI Ex ress Technolo p gy** 

## **Slot Control** 

Software controls the Hot Plug events through the Slot Control register, shown in Figure 19‐6 on page 868. This register permits software to enable various Hot Plug features and control hot plug operations. It’s also used to enable interrupt generation as well as enabling the sources of Hot‐Plug events that can result in interrupt generation. 

_Figure 19‐6: Slot Control Register_ 

**==> picture [385 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 13 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Data Link Layer<br>State Changed Enable<br>Electromechanical<br>Interlock Control<br>Power Controller Control<br>Power Indicator Control<br>Attention Indicator Control<br>Hot Plug Interrupt Enable<br>Command Completed Interrupt Enable<br>Presence Detect Changed Enable<br>MRL Sensor Changed Enable<br>Power Fault Detected Enable<br>Attention Button Pressed Enable<br>**----- End of picture text -----**<br>


**868** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐6: Slot Control Register Fields and Descriptions_ 

|**Bit(s)**|**Register Name and Description**|
|---|---|
|0|**Attention Button Pressed Enable.**When set, this bit enables the genera‐<br>tion of a hot‐plug interrupt (if enabled) or assertion of the Wake# message,<br>when the attention button is pressed.|
|1|**Power Fault Detected Enable.**When set, enables generation of a hot‐plug<br>interrupt (if enabled) or Wake# message upon detection of a power fault.|
|2|**MRL Sensor Changed Enable.**When set, enables generation of a hot‐<br>plug interrupt or Wake# (if enabled) message upon detection of a MRL<br>sensor changed event.|
|3|**Presence Detect Changed Enable.**When set this bit enables the genera‐<br>tion of the hot‐plug interrupt or a Wake message when the presence<br>detect changed bit in the Slot Status register is set.|
|4|**Command Completed Interrupt Enable.**When set, enables a Hot‐ Plug<br>interrupt to be generated that informs software that the hot‐plug control‐<br>ler is ready to receive the next command.|
|5|**Hot‐Plug Interrupt Enable.**When set, enables the generation of Hot‐Plug<br>interrupts.|
|7:6|**Attention Indicator Control.**Writes to the field control the state of the<br>attention indicator and reads return the current state, as follows:<br>• 00b = Reserved<br>• 01b = On<br>• 10b = Blink<br>• 11b = Off|
|9:8|**Power Indicator Control.**Writes to the field control the state of the power<br>indicator and reads return the current state, as follows:<br>• 00b = Reserved<br>• 01b = On<br>• 10b = Blink<br>• 11b = Off|
|10|**Power Controller Control.**Writes to the field switch main power to the<br>slot and reads return the current state: 0b = Power On, 1b = Power Off|



**869** 

**PCI Ex ress Technolo p gy** 

_Table 19‐6: Slot Control Register Fields and Descriptions (Continued)_ 

|**Bit(s)**|**Register Name and Description**|
|---|---|
|11|**Electromechanical Interlock Control ‐**If the interlock is implemented,<br>writing a 1b to this bit toggles the state of it while writing a 0b has no<br>effect. Reading this bit always returns a 0b.|
|12|**Data Link Layer State Changed Enable**‐ If the Data Link Layer Link<br>Active Reporting capability is 1b, setting this bit enables software notifica‐<br>tion when the Data Link Layer Link Active bit changes. If the Data Link<br>Layer Link Active Reporting capability is 0b, then this bit becomes read‐<br>only with a value of 0b.|



## **Slot Status and Events Management** 

The Hot Plug Controller monitors a variety of events and reports these events to the Hot Plug System Driver. Software can use the “detected” bits to determine which event has occurred, while the status bit identifies that nature of the change. The changed bits must be cleared by software in order to detect a subse‐ quent change. Note that whether these events get reported to the system (via a system interrupt) is determined by the related enable bits in the Slot Control Register. 

_Figure 19‐7: Slot Status Register_ 

**==> picture [386 x 204] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9 8 7 6 5 4 3 2 1 0<br>RsvdZ<br>Data Link Layer State Changed<br>Electromechanical Interlock Status<br>Presence Detect State<br>MRL Sensor State<br>Command Completed<br>Presence Detect Changed<br>MRL Sensor Changed<br>Power Fault Detected<br>Attention Button Pressed<br>**----- End of picture text -----**<br>


**870** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐7: Slot Status Register Fields and Descriptions_ 

|**Bit**<br>**Location**|**Register Name and Description**|
|---|---|
|0|**Attention Button Pressed**— If the button is implemented, this bit is<br>set when the Attention Button is pressed.|
|1|**Power Fault Detected**— If a Power Controller that supports power<br>fault detection is implemented, this bit is set when it detects a power<br>fault at this slot. The spec notes that it’s possible for a power fault to<br>be detected at any time, regardless of the Power Control setting or<br>whether the slot is occupied.|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
