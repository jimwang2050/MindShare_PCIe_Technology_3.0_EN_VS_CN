Type 1 Header<br>31 23 15 7 0 (Non-Prefetchable)<br>Device ID Vendor ID 00h Memory Base<br>15 3 0<br>Status Command 04h<br>1111 1001 0000 0000<br>Class Code       ID  Rev 08h (F) (9) (0) (RO)<br>BIST Header Latency Cache 0Ch (RW) Bits 31:20 of Must be 0<br>Type Timer Line Size Non-Prefetchable Base Address<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h Non-Prefetchable<br>F900 0000h<br>Secondary Subordinate Secondary Primary 18h Range Base Address<br>Lat Timer Bus # Bus # Bus # Bits 19:0 are<br>Secondary IO IO 1Ch always 0s for Base<br>Status Limit Base<br>(Non-Prefetchable) (Non-Prefetchable) 20h<br>Memory Limit Memory Base<br>Prefetchable Prefetchable 24h (Non-Prefetchable)<br>Memory Limit Memory Base Memory Limit<br>Prefetchable Memory Base 28h 15 3 0<br>Upper 32 Bits<br>1111 1001 0000 0000<br>Prefetchable Memory Limit 2Ch<br>Upper 32 Bits (F) (9) (0)<br>IO Limit IO Base (RO)<br>Upper 16 Bits Upper 16 Bits 30h (RW) Bits 31:20 of Must be 0<br>Non-Prefetchable LimitAddress<br>Reserved Capability 34h<br>Pointer<br>Expansion ROM Base Address 38h<br>Non-Prefetchable<br>ControlBridge InterruptPin InterruptLine 3Ch Range Limit Address F90F FFFFh<br>Bits 19:0 are<br>always Fs for Limit<br>Non-Prefetchable Memory Range: F900_0000h - F90F_FFFFh<br>**----- End of picture text -----**<br>


**140** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐5: Example Non‐Prefetchable Memory Base/Limit Register Meanings_ 

|**Register**|**Value**|**Use**|
|---|---|---|
|(Non‐Prefetchable)<br>Memory Base|F900h|The upper 12 bits of this register hold the<br>upper 12 bits of the 32‐bit BASE address (bits<br>[31:20]). The lower 20 bits of the base address<br>are implied to be all 0s, meaning the base<br>address is always aligned on a 1MB bound‐<br>ary.<br>The lower 4 bits of this register must be 0s.|
|(Non‐Prefetchable)<br>Memory Limit|F900h|Similarly, the upper 12 bits of this register<br>hold the upper 12 bits of the 32‐bit LIMIT<br>address (bits [31:20]). The lower 20 bits of the<br>limit address are all implied to be all Fs.<br>The lower 4 bits of this register must be 0s.|



This example shows an interesting case where the non‐prefetchable address range programmed in Port B’s configuration space indicates a much larger range (1MB) than the NP‐MMIO range (4KB) owned by the endpoint living downstream. This is because the memory base/limit registers in the Type 1 header, can only be used to specify address bits 20 and above ([31:20]). The lower 20 address bits, [19:0], are implied. So the smallest address range that can be specified with the memory base/limit registers is 1MB. 

In our example, the endpoint requested, and was granted, 4KB of NP‐MMIO (F900_0000h ‐ F900_0FFFh). Port B was programmed with values indicating 1MB, or 1024KB, of NP‐MMIO lived downstream of that port (F900_0000h ‐ F90F_FFFFh). This means 1020KB (F900_1000h ‐ F90F_FFFFh) of memory address space is wasted. This address space CANNOT be allocated to another endpoint because the routing of the packets would not work. 

## **IO Range** 

Like with the prefetchable memory range, Type 1 headers have two pairs of IO base/limit registers. The IO Base/Limit registers store address info for the lower 16 bits of the IO address range. If this bridge supports decoding 32‐bit IO addresses (which is rare in real‐world devices), then the IO Base/Limit Upper 16 Bits registers are also used and hold the upper 16 bits (bits [31:16]) of the IO 

**141** 

**PCI Express Technology** 

address range. Following our example, Figure 4‐10 on page 142 shows the val‐ ues software would program into these registers to indicate that the IO address range of 4000h ‐ 4FFFh lives beneath that bridge (Port B). The meaning of each field in those registers is summarized in Table 4‐6. 

_Figure 4‐10: Example IO Base/Limit Register Values_ 

**==> picture [381 x 340] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>31 23 15 7 0 IO Base<br>Device ID Vendor ID 00h Upper 16 Bits IO Base<br>15 0 7 3 0<br>Status Command 04h<br>0000 0000 0000 0000 0100 0000<br>Class Code       ID  Rev 08h (0) (0) (0) (0) (4) (RO)<br>BIST HeaderType LatencyTimer Line SizeCache 0Ch (RW) Bits 31:16 ofIO Base Address of IO Base Address(RW) Bits 15:12 0h = 16-bit1h = 32-bit<br>(if used)<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h IO Range<br>Secondary Subordinate Secondary Primary 18h Base Address 4000h<br>Lat Timer Bus # Bus # Bus # Bits 11:0 are<br>SecondaryStatus LimitIO BaseIO 1Ch always 0s for IO Base<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Memory LimitPrefetchable Memory BasePrefetchable 24h Upper 16 BitsIO Limit IO Limit<br>Prefetchable Memory Base 28h 15 0 7 3 0<br>Upper 32 Bits<br>0000 0000 0000 0000 0100 0000<br>Prefetchable Memory LimitUpper 32 Bits 2Ch (0) (0) (0) (0) (4) (RO)<br>Upper 16 BitsIO Limit Upper 16 BitsIO Base 30h (RW) Bits 31:16 ofIO Limit Address of IO Limit Address(RW) Bits 15:12 0h = 16-bit1h = 32-bit<br>Reserved CapabilityPointer 34h (if used)<br>Expansion ROM Base Address 38h<br>IO Range<br>ControlBridge InterruptPin InterruptLine 3Ch Limit Address 4FFFh<br>Bits 11:0 are<br>always Fs for IO Limit<br>IO Range: 4000h - 4FFFh<br>**----- End of picture text -----**<br>


**142** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐6: Example IO Base/Limit Register Meanings_ 

|**Register**|**Value**|**Use**|
|---|---|---|
|IO Base|40h|The upper 4 bits of this register hold the<br>upper 4 bits of the 16‐bit BASE address (bits<br>[15:12]). The lower 12 bits of the base address<br>are implied to be all 0s, meaning the base<br>address is always aligned on a 4KB boundary.<br>The lower 4 bits of this register indicate<br>whether a 32‐bit IO address decoder is sup‐<br>ported in the bridge, meaning the Upper Base/<br>Limit Registers are used.|
|IO Limit|40h|Similarly, the upper 4 bits of this register hold<br>the upper 4 bits of the 16‐bit LIMIT address<br>(bits [15:12]). The lower 12 bits of the limit<br>address are all implied to be all Fs.<br>The lower 4 bits of this register have the same<br>meaning as the lower 4 bits of the base regis‐<br>ter.|
|IO Base Upper 16 Bits|0000h|Holds the upper 16 bits of the 32‐bit BASE<br>address for IO downstream of this port.|
|IO Limit Upper 16 Bits|0000h|Holds the upper 16 bits of the 32‐bit LIMIT<br>address for IO downstream of this port.|



In this example, we see another situation where the address range programmed into the upstream bridge far exceeds the actual address range owned by the downstream function. The endpoint in our example owns 256 bytes of IO address space (specifically 4000h ‐ 40FFh). Port B has been programmed with values indicating that 4KB of IO address space lives downstream (addresses 4000h ‐ 4FFFh). Again, this is simply a limitation of Type 1 headers. For IO address space, the lower 12 bits (bits [11:0]) have implied values, so the smallest range of IO addresses that can be specified is 4KB. This limitation turns out to be more serious than the 1MB minimum window for memory ranges. In x86‐ based (Intel compatible) systems, the processors only support 16 bits of IO address space, and since only bits [15:12] of the IO address range can be speci‐ fied in a bridge, that means that there can be a maximum of 16 (2[4] ) different IO address ranges in a system. 

**143** 

**PCI Express Technology** 

## **Unused Base and Limit Registers** 

Not every PCIe device will use all three types of address space. In fact, the PCI Express specification actually discourages the use of IO address space, indicat‐ ing that it is only supported for legacy reasons and may be deprecated in a future revision of the spec. 

In the cases where an endpoint does not request all three types of address space, what are the base and limit registers of the bridges upstream of those devices programmed with? They can’t be programmed with all 0s because the lower address bits would still be implied to be different (base = 0s; limit = Fs) which would represent a valid range. So to handle these cases, the limit register must be programmed with a higher address than the base. For example, if an end‐ point does not request IO address space, then the bridge immediately upstream of that function would have its IO Base register programmed to 00h and its IO Limit register programmed with F0h. Since the limit address is higher than the base address, the bridge understands this is an invalid setting and takes it to mean that there are no functions downstream of it that own IO address space. 

This method of invalidating base and limit registers is valid for all three base and limit pairs, not just for the IO base/limit registers. 

## **Sanity Check: Registers Used For Address Routing** 

To ensure that you understand the rules and methods for setting up BARs and Base/Limit registers, please look over Figure 4‐11 on page 145 to make sure it makes sense. We have simply extended the example system to include addi‐ tional address space requests from the other endpoint, as well as from one of the switch ports (Port A). Remember that Type 1 headers also have BARs (two of them to be exact) and can request address space too. The Base/Limit registers in a bridge do NOT include the addresses owned by that same bridge’s BARs. The Base/Limit registers only represent the addresses that live downstream of that bridge. 

**144** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐11: Final Example Address Routing Setup_ 

**==> picture [370 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
BAR0-1: Not Used (All 0s)<br>IO Range: 4000h - 5FFFh<br>NP-MMIO Range: F900_0000h - F90F_FFFFh<br>P-MMIO Range: 2_3E00_0000h - 2_440F_FFFFh<br>CPU<br>Root Complex MemorySystem<br>P2P (DRAM)<br>BAR0-1: [P-MMIO (1KB)]<br>2_3E00_0000h - 2_3E00_03FFh<br>Port IO Range:<br>A NP-MMIO Range:<br>P2P P-MMIO Range:<br>Switch<br>BAR0-1: Not Used (All 0s) BAR0-1: Not Used (All 0s)<br>IO Range: 4000h - 4FFFh Port Port IO Range: 5000h - 5FFFh<br>NP-MMIO Range: F900_0000h - F90F_FFFFh B C NP-MMIO Range: Not Used (Base > Limit)<br>P-MMIO Range: 2_4000_0000h - 2_43FF_FFFFh P-MMIO Range: 2_4400_0000h - 2_440F_FFFFh<br>PCIe PCIe<br>Endpoint Endpoint<br>BAR0: NP-MMIO (4KB) BAR0-1: P-MMIO (8KB)<br>F900_0000h - F900_0FFFh 2_4400_0000h - 2_4400_1FFFh<br>BAR1-2: P-MMIO (64MB) BAR2-4: Not Used (All 0s)<br>2_4000_0000h - 243FF_FFFFh BAR5: IO (4 bytes)<br>BAR3: IO (256 bytes) 5000h - 5003h<br>4000h - 40FFh<br>BAR4-5: Not Used (All 0s)<br>4000h - 5FFFh<br>F900_0000h - F90F_FFFFh<br>2_4000_0000h - 2_440F_FFFFh<br>P2P P2P<br>**----- End of picture text -----**<br>


## **TLP Routing Basics** 

The purpose of setting up the BARs and Base/Limit registers as described in the previous sections, is to ensure that traffic targeting a function will be routed cor‐ rectly so the targeted function can see the transactions and claim them. In shared‐bus architectures like PCI, all the traffic is visible to every device. The only time routing of requests happens is when the target is on another bus and must cross a bridge. Since PCIe Links are point‐to‐point, more routing will be needed to deliver transactions between devices. 

**145** 

## **PCI Express Technology** 

_Figure 4‐12: Multi‐Port PCIe Devices Have Routing Responsibilities_ 

**==> picture [330 x 297] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>IN OUT IN OUT Memory<br>Switch OUT IN OUT IN<br>Legacy<br>InternalUse Endpoint<br>?<br>Traffic Types:<br>  - Physical Layer Ordered Sets<br>  - Data Link Layer Packets (DLLPs)<br>  - Transaction Layer Packets (TLPs)<br>OUT IN OUT IN<br>    IN = INGRESS PORT<br>PCIe PCIe OUT = EGRESS PORT<br>Endpoint Endpoint<br>IN OUT<br>OUT IN<br>**----- End of picture text -----**<br>

