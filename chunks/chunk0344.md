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
