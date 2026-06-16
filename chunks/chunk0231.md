CPU<br>Root Complex System<br>Memory<br>P2P (DRAM)<br>Type 1 Headers<br>P2P (Virtual PCI-PCI Bridges)<br>Switch<br>Type 0 Headers<br>PCIe PCIe<br>Endpoint Endpoint<br>P2P P2P<br>**----- End of picture text -----**<br>


## **BAR Example 1: 32-bit Memory Address Space Request** 

Figure 4‐4 on page 130 shows the basic steps in setting up a BAR, which in this example, is requesting a 4KB block of non‐prefetchable memory (NP‐MMIO). In the figure, the BAR is shown at three points in the configuration process: 

1. In (1) of Figure 4‐4, we see the uninitialized state of the BAR. The device designer has fixed the lower bits to indicate the size and type, but the upper bits (which are read‐write) are shown as Xs to indicate their value is not known. System software will first write all 1s to every BAR (using config writes) to set all writable bits. (Of course, the hard‐coded lower bits are unaffected by any configuration writes.) The second view of the BAR, 

**128** 

**Chapter 4: Address Space & Transaction Routing** 

shown in (2) of Figure 4‐4, shows how it looks after configuration software has written all 1’s to it. 

Writing all 1s is done to determine what the least‐significant writable bit is. This bit position indicates the size of the address space being requested. In this example, the least‐significant writable bit is bit 12, so this BAR is requesting 2[12] (or 4KB) of address space. If the least significant writable bit would have been bit 20, then the BAR would have been requesting 2[20] (or 1MB) of address space. 

2. After writing all 1s to the BARs, software turns around and reads the value of each BAR, starting with BAR0, to determine the type and size of the address space being requested. Table 4‐1 on page 129 summarizes the results of the configuration read of BAR0 for this example. 

3. The final step in this process is for system software to allocate an address range to BAR0 now that software knows the size and type of the address space being requested. The third view of the BAR, in (3) of Figure 4‐4, shows how it looks after software has written the start address for the allo‐ cated block of addresses. In this example, the start address is F900_0000h. 

At this point the configuration of BAR0 is complete. Once software enables memory address decoding in the Command register (offset 04h), this device will accept any memory requests it receives that fall within the range from F900_0000h ‐ F900_0FFFh (4KB in size). 

_Table 4‐1: Results of Reading the BAR after Writing All 1s To It_ 

|**BAR Bits**|**Meaning**|
|---|---|
|0|Read as 0b, indicating a memory request. Since this is a memory request,<br>bits 3:1 also have an encoded meaning.|
|2:1|Read as 00b indicating the target only supports decoding a 32‐bit<br>address|
|3|Read as 0b, indicating request is for non‐prefetchable memory (meaning<br>reads do have side‐effects); NP‐MMIO|
|11:4|Read as all 0s, indicating the size of the request (these bits are hard‐<br>coded to 0)|
|31:12|Read as all 1s because software has not yet programmed the upper bits<br>with a start address for the block. Since bit 12 is the least significant bit<br>that could be written, the memory size requested is 212= 4KB.|



**129** 

**PCI Express Technology** 

_Figure 4‐4: 32‐Bit Non‐Prefetchable Memory BAR Set Up_ 

## **Type 0 Header** 

**==> picture [364 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 23 15 7 0<br>Device ID Vendor ID 00h Uninitialized BAR<br>31 12 4 3 2 1 0<br>Status Command 04h<br>XXXX XXXX XXXX XXXX XXXX 00000000 0 0 0 0 (1)<br>Class Code   Rev 08h<br>      ID<br>BIST Header Latency Cache 0Ch BAR Written with all 1s<br>Type Timer Line Size 31 12 4 3 2 1 0<br>Base Address 0 (BAR0) 10h 1111 1111 1111 1111 1111 00000000 0 0 0 0 (2)<br>Base Address 1 (BAR1) 14h<br>Base Address 2 (BAR2) 18h BAR Written With Base Address<br>31 12 4 3 2 1 0<br>Base Address 3 (BAR3) 1Ch 1111 1001 0000 0000 0000 00000000 0 0 0 0 (3)<br>Base Address 4 (BAR4) 20h (F) (9) (0) (0) (0)<br>Base Address 5 (BAR5) 24h 0 = Memory request1 = IO request<br>CardBus CIS Pointer 28h 00 = 32-bit decoding<br>10 = 64-bit decoding<br>SubsystemDevice ID SubsystemVendor ID 2Ch 0 = non-prefetchable1 = prefetchable<br>Expansion ROM Base Address 30h<br>Upper 20 bits of 4KB aligned<br>Reserved CapabilityPointer 34h start address (lower 12 bits assumed to be = 0)(F900 0000h)<br>Reserved 38h<br>This Example:<br>Max Lat Min Gnt Interrupt Interrupt 3Ch -4KB of non-prefetchable memory<br>Pin Line -Address range must be below 4GB (32-bit decode)<br>Note: if memory address is assigned below 4GB boundary,<br>the 3DW header must be used when targeting this device.<br>**----- End of picture text -----**<br>


## **BAR Example 2: 64-bit Memory Address Space Request** 

In the previous example, we saw BAR0 being used to request non‐prefetchable memory address space (NP‐MMIO). In this example, as shown in Figure 4‐5 on page 132, BAR1 and BAR2 are being used to request a 64MB block of prefetch‐ able memory address space. Two sequential BARs are being used here because the device supports a 64‐bit address for this request, meaning that software can allocate the requested address space above the 4GB address boundary if it 

**130** 

**Chapter 4: Address Space & Transaction Routing** 

wants to (but that is not a requirement). Since the address can be a 64‐bit address, two sequential BARs must be used together. 

As before, the BARs are shown at three points in the configuration process: 

1. In (1) of Figure 4‐5, we see the uninitialized state of the BAR pair. The device designer has hard‐coded the lower bits of the lower BAR (BAR1 in our example) to indicate the request type and size, while the bits of the upper BAR (BAR2) are all read‐write. System software’s first step was to write all 1s to every BAR. In (2) of Figure 4‐5, we see the BARs after having all 1s written to them. 

2. As described in the previous example, system software already evaluated BAR0. So software’s next step is to read the next BAR (BAR1) and evaluate it to see if the device is requesting additional address space. Once BAR1 is read, software realizes that more address space is being requested and this request is for prefetchable memory address space that can be allocated any‐ where in the 64‐bit address range. Since it supports a 64‐bit address, the next sequential BAR (BAR2 in this case) is treated as the upper 32 bits of BAR1. So software now also reads in the contents of BAR2. However, soft‐ ware does not evaluate the lower bits of BAR2 in the same way it did for BAR1, because it knows BAR2 is simply the upper 32 bits of the 64‐bit address request started in BAR1. Table 4‐2 on page 132 summarizes the results of these configuration reads. 

3. The final step in this process is for system software to allocate an address range to the BARs now that software knows the size and type of the address space being requested. The third view of the BARs in (3) of Figure 4‐5 shows the result after software has used two configuration writes to pro‐ gram the 64‐bit start address for the allocated range. In this example, bit 1 of the Upper BAR (address bit 33 in the BAR pair) is set and bit 30 of the Lower BAR (address bit 30 in the BAR pair) is set to indicate a start address of 2_4000_0000h. All other writable bits in both BARs are cleared. 

At this point, the configuration of the BAR pair (BAR1 & BAR2) is complete. Once software enables memory address decoding in the Command register (offset 04h), this device will accept any memory requests it receives that fall within the range from 2_4000_0000h ‐ 2_43FF_FFFFh (64MB in size). 

**131** 

**PCI Express Technology** 

_Figure 4‐5: 64‐Bit Prefetchable Memory BAR Set Up_ 

## **Type 0 Header** 

**==> picture [375 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 23 15 7 0 Uninitialized BAR Pair<br>Device ID Vendor ID 00h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>Status Command 04h XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XX 00 0000 0000 0000 0000 0000 1 1 0 0 (1)<br>BAR n+1 BAR n<br>Class Code   Rev 08h<br>      ID<br>BIST Header Latency Cache 0Ch<br>Type Timer Line Size BAR Pair Written with all 1s<br>Base Address 0 (BAR0) 10h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>Base Address 1 (BAR1) 14h 1111 1111 1111 1111 1111 1111 1111 1111 1111 11 00 0000 0000 0000 0000 0000 1 1 0 0 (2)<br>Base Address 2 (BAR2) 18h<br>Base Address 3 (BAR3) 1Ch<br>BAR Pair Written With Base Address<br>Base Address 4 (BAR4) 20h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>Base Address 5 (BAR5) 24h 0000 0000 0000 0000 0000 0000 0000 0010 0100 00 00 0000 0000 0000 0000 0000 1 1 0 0 (3)<br>CardBus CIS Pointer 28h (0) (0) (0) (0) (0) (0) (0) (2) (4) (0) 0 = non-prefetchable<br>SubsystemDevice ID SubsystemVendor ID 2Ch 1 = prefetchable00 = 32-bit decoding<br>10 = 64-bit decoding<br>Expansion ROM Base Address 30h<br>0 = Memory request<br>Reserved Capability 34h 1 = IO request<br>Pointer<br>Reserved 38h Upper 38 bits of 64MB alignedstart address (lower bits assumed to be = 0)<br>(0000 0002 4000 0000h)<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch<br>This Example:<br>-64MB of prefetchable memory<br>-Address range may be above 4GB boundary (64-bit decode)<br>**----- End of picture text -----**<br>


_Table 4‐2: Results Of Reading the BAR Pair after Writing All 1s To Both_ 

|**BAR**|**BAR**<br>**Bits**|**Meaning**|
|---|---|---|
|Lower|0|Read as 0b, indicating a memory request. Since this is a mem‐<br>ory request, bits 3:1 also have an encoded meaning.|
|Lower|2:1|Read as 10b indicating the target supports a 64‐bit address<br>decoder, and that the next sequential BAR contains the upper<br>32 bits of the address information.|



**132** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐2: Results Of Reading the BAR Pair after Writing All 1s To Both (Continued)_ 

|**BAR**|**BAR**<br>**Bits**|**Meaning**|
|---|---|---|
|Lower|3|Read as 1b, indicating request is for prefetchable memory<br>(meaning reads do not have side‐effects); P‐MMIO|
|Lower|25:4|Read as all 0s, indicating the size of the request (these bits are<br>hard‐coded to 0)|
|Lower|31:26|Read as all 1s because software has not yet programmed the<br>upper bits with a start address for the block. Note that because<br>bit 26 was the least significant writable bit, the memory address<br>space request size is 226, or 64MB.|
|Upper|31:0|Read as all 1s. These bits will be used as the upper 32 bits of the<br>64‐bit start address programmed by system software.|



## **BAR Example 3: IO Address Space Request** 

Continuing from the previous two examples, this same function is also request‐ ing IO space, as shown in Figure 4‐6 on page 134. In the diagram, the requesting BAR (BAR3 in the example) is shown at three points in the configuration pro‐ cess: 

1. In (1) of Figure 4‐6, we see the uninitialized state of the BAR. System soft‐ ware has previously written all 1s to every BAR and has evaluated BAR0, then BAR1 and BAR2. Now software is going to see if this device is request‐ ing additional address space with BAR3. State (2) of Figure 4‐6 shows the state of the BAR3 after the write of all 1s. 

2. Software now reads in BAR3 to evaluate the size and type of the request. Table 4‐3 on page 134 summarizes the results of this configuration read. 

3. Now that software knows this is a request for 256 bytes of IO address space, the final step is to program the BAR with the base address of the IO address range being allocated to this device, specifically this BAR. State (3) of Figure 4‐6 shows the state of the BAR after this step. In our example, the device start address is 16KB, so bit 14 is written resulting in a base address of 4000h; all other upper bits are cleared. 
