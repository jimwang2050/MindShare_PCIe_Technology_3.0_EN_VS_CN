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