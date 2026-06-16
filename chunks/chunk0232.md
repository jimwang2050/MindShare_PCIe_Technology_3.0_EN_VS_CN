At this point, the configuration of BAR3 is complete. Once software enables IO address decoding in the Command register (offset 04h), the device will accept and respond to IO transactions within the range 4000h ‐ 40FFh (256 bytes in size). 

**133** 

## **PCI Express Technology** 

_Figure 4‐6: IO BAR Set Up_ 

**==> picture [389 x 485] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Header<br>31 23 15 7 0<br>Uninitialized IO BAR<br>Device ID Vendor ID 00h 31 8 2 1 0<br>Status Command 04h XXXX XXXX XXXX XXXX XXXX XXXX 0000 00 0 1 (1)<br>Class Code   Rev 08h<br>      ID<br>BIST Header Latency Cache 0Ch IO BAR Written with all 1s<br>Type Timer Line Size 31 8 2 1 0<br>Base Address 0 (BAR0) 10h 1111 1111 1111 1111 1111 1111 0000 00 0 1 (2)<br>Base Address 1 (BAR1) 14h<br>Base Address 2 (BAR2) 18h IO BAR Written With Base Address<br>31 8 2 1 0<br>Base Address 3 (BAR3) 1Ch<br>0000 0000 0000 0000 0100 0000 0000 00 0 1 (3)<br>Base Address 4 (BAR4) 20h (0) (0) (0) (0) (4) (0)<br>Base Address 5 (BAR5) 24h 0 = Memory request<br>1 = IO request<br>CardBus CIS Pointer 28h<br>Reserved (0)<br>SubsystemDevice ID SubsystemVendor ID 2Ch<br>Upper 24 bits of 256-byte aligned<br>Expansion ROM Base Address 30h start address (lower 7 bits assumed to be = 0)<br>(0000 4000h)<br>Reserved Capability 34h<br>Pointer<br>Reserved 38h This Example:<br>-256 bytes of IO address space<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch -Software assigns the start address at 16KB in IO address map.<br>Note: Only Legacy PCIe devices should make requests for IO<br>address space.<br>Table 4‐3: Results Of Reading the IO BAR after Writing All 1s To It<br>BAR Bits Meaning<br>0 Read as 1b, indicating an IO request. Since this is an IO request, bit 1 is<br>reserved.<br>1 Reserved. Hard‐coded to 0b.<br>7:2 Read as 0s Indicates size of the request (these bits are hard‐coded to 0)<br>31:8 Read as 1s because software has not yet programmed the upper bits<br>with a start address for the block. Note that because bit 8 was the least<br>significant writable bit, the IO request size is 2 [8] , or 256 bytes.<br>**----- End of picture text -----**<br>


**134** 

**Chapter 4: Address Space & Transaction Routing** 

## **All BARs Must Be Evaluated Sequentially** 

After going through the previous three examples, it becomes clear that software must evaluate BARs in a sequential fashion. 

Most of the time, functions do not need all six BARs. Even in the examples we went through, only four of the six available BARs were used. If the function in our example did not need to request any additional address space, the device designer would hard‐code all bits of BAR4 and BAR5 to 0s. So even though soft‐ ware writes those BARs with all 1s, the writes have no affect. After evaluating BAR3, software would move on to evaluating BAR4. Once it detected that none of the bits were set, software would know this BAR is not being used and move on to evaluating the next BAR. 

All BARs must be evaluated, even if software finds a BAR that is not being used. There are no rules in PCI or PCIe, that state that BAR0 must be the first BAR used for address space requests. If a device designer chooses to, they can use BAR4 for an address space request and hard‐code BAR0, BAR1, BAR2, BAR3 and BAR5 to all 0s. This means software must evaluate every BAR in the header. 

## **Resizable BARs** 

The 2.1 version of the PCI Express specification added support for changing the size of the requested address space in the BARs by defining a new capability structure in extended config space. The new structure allows the function to advertise what address space sizes it can operate with and then have software enable one of the sizes based on the available system resources. For example, if a function would ideally like to have 2GB of prefetchable memory address space, but it could still operate with only 1GB, 512MB or 256MB of P‐MMIO, system software may only enable the function to request 256MB of address space if software would not be able to accommodate a request of a larger size. 

**135** 

**PCI Express Technology** 

## **Base and Limit Registers** 

## **General** 

Once a function’s BARs are programmed, the function knows what address range(s) it owns, which means that function will claim any transactions it sees that is targeting an address range it owns, an address range programmed into one of its BARs. This is good, but it’s important to realize that the only way that function is going to “see” the transactions it should claim is if the bridge(s) upstream of it, forward those transactions downstream to the appropriate link that the target function is connected to. Therefore, each bridge (e.g. switch ports and root complex ports) needs to know what address ranges live beneath it so it can determine which requests should be forwarded from its primary interface (upstream side) to its secondary interface (downstream side). If the request is targeting an address that is owned by a BAR in a function beneath the bridge, the request should be forwarded to the bridge’s secondary interface. 

It is the Base and Limit registers in the Type 1 headers that are programmed with the range of addresses that live beneath this bridge. There are the three sets of Base and Limit registers found in each Type 1 header. Three sets of registers are needed because there can be three separate address ranges living below a bridge: 

- Prefetchable Memory space (P‐MMIO) 

- Non‐Prefetchable Memory space (NP‐MMIO) 

- IO space (IO) 

To explain how these Base and Limit registers work, let’s continue the example from the previous section and place that programmed function (an endpoint) beneath a switch as shown in Figure 4‐7 on page 137. The figure also lists the address ranges owned by the BARs of that function. 

The Base and Limit registers of every bridge upstream of the endpoint will need to be programmed, but to start out, we’re going to focus on the bridge that is connected to the endpoint (Port B). 

**136** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐7: Example Topology for Setting Up Base and Limit Values_ 

**==> picture [301 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex MemorySystem<br>P2P (DRAM)<br>Port<br>A<br>P2P<br>Switch<br>Port Port<br>B C<br>PCIe PCIe<br>Endpoint Endpoint<br>BAR0: NP-MMIO (4KB)<br>F900_0000h - F900_0FFFh<br>BAR1-2: P-MMIO (64MB)<br>2_4000_0000h - 243FF_FFFFh<br>BAR3: IO (256 bytes)<br>4000h - 40FFh<br>BAR4-5: Not Used (All 0s)<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Prefetchable Range (P-MMIO)** 

Type 1 headers have two pairs of prefetchable memory base/limit registers. The Prefetchable Memory Base/Limit registers store address info for the lower 32 bits of the prefetchable address range. If this bridge supports decoding 64‐bit addresses, then the Prefetchable Memory Base/Limit Upper 32 Bits registers are also used and hold the upper 32 bits (bits [63:32]) of the address range. Figure 4‐ 8 on page 138 shows the values software would program into these registers to indicate that the prefetchable address range of 2_4000_0000h ‐ 2_43FF_FFFFh lives beneath that bridge (Port B). The meaning of each field in those registers is summarized in Table 4‐4. 

**137** 

**PCI Express Technology** 

_Figure 4‐8: Example Prefetchable Memory Base/Limit Register Values_ 

**==> picture [368 x 305] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>31 23 15 7 0 Prefetchable Base Prefetchable<br>Device ID Vendor ID 00h Upper 32 Bits Memory Base<br>31 0 15 3 0<br>Status Command 04h 0000 0000 0000 0000 0000 0000 0000 0010 0100 0000 0000 0001<br>Class Code       ID  Rev 08h (0) (0) (0) (0) (0) (0) (0) (2) (4) (0) (0) (RO)<br>0h = 32-bit<br>BIST HeaderType LatencyTimer Line SizeCache 0Ch Prefetchable Base Address(RW) Bits 63:32 of Prefetchable Base Address(RW) Bits 31:20 of 1h = 64-bit<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h Prefetchable Range<br>Secondary Subordinate Secondary Primary 18h Base Address 0000 0002 4000 0000h<br>Lat Timer Bus # Bus # Bus # Bits 19:0 are<br>SecondaryStatus LimitIO BaseIO 1Ch always 0s for Base<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Memory LimitPrefetchable Memory BasePrefetchable 24h Prefetchable LimitUpper 32 Bits Memory LimitPrefetchable<br>Prefetchable Memory Base 28h 31 0 15 3 0<br>Upper 32 Bits 0000 0000 0000 0000 0000 0000 0000 0010 0100 0011 1111 0001<br>Prefetchable Memory LimitUpper 32 Bits 2Ch (0) (0) (0) (0) (0) (0) (0) (2) (4) (3) (F) (RO)<br>IO Limit IO Base 0h = 32-bit<br>Upper 16 Bits Upper 16 Bits 30h (RW) Bits 63:32 of (RW) Bits 31:20 of 1h = 64-bit<br>Prefetchable Base Address Prefetchable Base Address<br>Reserved Capability 34h<br>Pointer<br>Expansion ROM Base Address 38h<br>Prefetchable Range<br>ControlBridge InterruptPin InterruptLine 3Ch Limit Address 0000 0002 43FF FFFFh<br>Bits 19:0 are<br>always Fs for Limit<br>Prefetchable Memory Range: 2_4000_0000h - 2_43FF_FFFFh<br>**----- End of picture text -----**<br>


**138** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐4: Example Prefetchable Memory Base/Limit Register Meanings_ 

|**Register**|**Value**|**Use**|
|---|---|---|
|Prefetchable Memory<br>Base|4001h|The upper 12 bits of this register hold the<br>upper 12 bits of the 32‐bit BASE address (bits<br>[31:20]). The lower 20 bits of the base address<br>are implied to be all 0s, meaning the base<br>address is always aligned on a 1MB bound‐<br>ary.<br>The lower 4 bits of this register indicate<br>whether a 64‐bit address decoder is supported<br>in the bridge, meaning the Upper Base/Limit<br>Registers are used.|
|Prefetchable Memory<br>Limit|43F1h|Similarly, the upper 12 bits of this register<br>hold the upper 12 bits of the 32‐bit LIMIT<br>address (bits [31:20]). The lower 20 bits of the<br>limit address are all implied to be all Fs.<br>The lower 4 bits of this register have the same<br>meaning as the lower 4 bits of the base regis‐<br>ter.|
|Prefetchable Memory<br>Base Upper 32 Bits|00000002h|Holds the upper 32 bits of the 64‐bit BASE<br>address for Prefetchable Memory down‐<br>stream of this port.|
|Prefetchable Memory<br>Limit Upper 32 Bits|00000002h|Holds the upper 32 bits of the 64‐bit LIMIT<br>address for Prefetchable Memory down‐<br>stream of this port.|



## **Non-Prefetchable Range (NP-MMIO)** 

Unlike the prefetchable memory range, the non‐prefetchable memory range can only support 32‐bit addresses. So there is only one register for the base and one register for the limit. Following the example in Figure 4‐7, the Non‐Prefetchable Memory Base/Limit registers of Port B would be programmed with the values shown in Figure 4‐9 on page 140. The meaning of these values is summarized in Table 4‐5. 

**139** 

**PCI Express Technology** 

_Figure 4‐9: Example Non‐Prefetchable Memory Base/Limit Register Values_ 

**==> picture [375 x 360] intentionally omitted <==**

**----- Start of picture text -----**<br>