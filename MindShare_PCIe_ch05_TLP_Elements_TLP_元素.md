# 📘 第 5 章　TLP 元素 (Chapter 5. TLP Elements)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0230.md` ... `chunks/chunk0243.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [TLP Elements](#-本章目录-table-of-contents)

<a id="sec-5-1"></a>
## 5.1 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

the device itself. This means these internal locations need to be _addressable_ . Soft‐ ware must be able to perform a read or write operation with an address that will access the appropriate internal location within the targeted device. In order to make this work, these internal locations need to be assigned addresses from one of the address spaces supported in the system. 

PCI Express supports the exact same three address spaces that were supported in PCI: 

- Configuration 

- Memory 

- IO 

## **Configuration Space** 

As we saw in Chapter 1, configuration space was introduced with PCI to allow software to control and check the status of devices in a standardized way. PCI Express was designed to be software backwards compatible with PCI, so config‐ uration space is still supported and used for the same reason as it was in PCI. More info about configuration space (purpose of, how to access, size, contents, etc.) can be found in Chapter 3. 

Even though configuration space was originally meant to hold standardized structures (PCI‐defined headers, capability structures, etc.), it is very common for PCIe devices to have device‐specific registers mapped into their config space. In these cases, the device‐specific registers mapped into config space are often control, status or pointer registers as opposed to data storage locations. 

## **Memory and IO Address Spaces** 

## **General** 

In the early days of PCs, the internal registers/storage in IO devices were accessed via IO address space (as defined by Intel). However, because of several limitations and undesirable effects related to IO address space, that we will not be going into here, that address space quickly lost favor with software and hardware vendors. This resulted in the internal registers/storage of IO devices being mapped into memory address space (commonly referred to as memory‐ mapped IO, or MMIO). However, because early software was written to use IO address space to access internal registers/storage on IO devices, it became com‐ mon practice to map the same set of device‐specific registers in memory 

**122** 

**Chapter 4: Address Space & Transaction Routing** 

address space as well as in IO address space. This allows new software to access the internal locations of a device using memory address space (MMIO), while allowing legacy (old) software to continue to function because it can still access the internal registers of devices using IO address space. 

Newer devices that do not rely on legacy software or have legacy compatibility issues typically just map internal registers/storage through memory address space (MMIO), with no IO address space being requested. In fact, the PCI Express specification actually discourages the use of IO address space, indicat‐ ing that it is only supported for legacy reasons and may be deprecated in a future revision of the spec. 

A generic memory and IO map is shown in Figure 4‐1 on page 125. The size of the memory map is a function of the range of addresses that the system can use (often dictated by the CPU addressable range). The size of the IO map in PCIe is limited to 32 bits (4GB), although in many computers using Intel‐compatible (x86) processors, only the lower 16 bits (64KB) are used. PCIe can support mem‐ ory addresses up to 64 bits in size. 

The mapping example in Figure 4‐1 is only showing MMIO and IO space being claimed by Endpoints, but that ability is not exclusive to Endpoints. It is very common for Switches and Root Complexes to also have device‐specific registers accessed via MMIO and IO addresses. 

## **Prefetchable vs. Non-prefetchable Memory Space** 

Figure 4‐1 shows two different types of MMIO being claimed by PCIe devices: Prefetchable MMIO (P‐MMIO) and Non‐Prefetchable MMIO (NP‐MMIO). It’s important to describe the distinction between prefetchable and non‐prefetch‐ able memory space. Prefetchable space has two very well defined attributes: 

- Reads do not have side effects 

- Write merging is allowed 

Defining a region of MMIO as prefetchable allows the data in that region to be speculatively fetched ahead in anticipation that a Requester might need more data in the near future than was actually requested. The reason it’s safe to do this minor caching of the data is that reading the data doesn’t change any state info at the target device. That is to say there are no side effects from the act of reading the location. For example, if a Requester asks to read 128 bytes from an address, the Completer might prefetch the next 128 bytes as well in an effort to improve performance by having it on hand when it’s requested. However, if the Requester never asks for the extra data, the Completer will eventually have to 

**123** 

## **PCI Express Technology** 

discard it to free up the buffer space. If the act of reading the data changed the value at that address (or had some other side effect), it would be impossible to recover the discarded data. However, for prefetchable space, the read had no side effects, so it is always possible to go back and get it later since the original data would still be there. 

You may be wondering what sort of memory space might have read side effects? One example would be a memory‐mapped status register that was designed to automatically clear itself when read to save the programmer the extra step of explicitly clearing the bits after reading the status. 

Making this distinction was more important for PCI than it is for PCIe because transactions in that bus protocol did not include a transfer size. That wasn’t a problem when the devices exchanging data were on the same bus, because there was a real‐time handshake to indicate when the requester was finished and did not need anymore data, therefore knowing the byte count wasn’t so important. But when the transfer had to cross a bridge it wasn’t as easy because for reads, the bridge would need to guess the byte count when gathering data on the other bus. Guessing wrong on the transfer size would add latency and reduce performance, so having permission to prefetch could be very helpful. That’s why the notion of memory space being designated as prefetchable was helpful in PCI. Since PCIe requests do include a transfer size it’s less interesting than it was, but it’s carried forward for backward compatibility. 

**124** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐1: Generic Memory And IO Address Maps_ 

**==> picture [300 x 354] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>Memory<br>(DRAM)<br>Switch<br>Memory Map<br>2 [32]  or 2 [64]<br>MMIO<br>Legacy PCIe<br>(Prefetchable)<br>Endpoint Endpoint<br>MMIO (NP) MMIO (P)<br>MMIO<br>IO MMIO (NP) (Non-Prefetchable)<br>PCIe Functions may have registers<br>and buffers mapped into IO and<br>Memory address space<br>2 [32] IO Map System<br>Memory<br>(DRAM)<br>IO<br>Ports<br>2 [16]<br>0 0<br>**----- End of picture text -----**<br>


**125** 

**PCI Express Technology** 

## **Base Address Registers (BARs)** 

## **General** 

Each device in a system may have different requirements in terms of the amount and type of address space needed. For example, one device may have 256 bytes worth of internal registers/storage that should be accessible through IO address space and another device may have 16KB of internal registers/stor‐ age that should be accessible through MMIO. 

PCI‐based devices are not allowed to decide on their own, which addresses should be used to access their internal locations, that is the job of system soft‐ ware (i.e. BIOS and OS kernel). So the devices must provide a way for system software to determine the address space needs of the device. Once software knows what the device’s requirements are in terms of address space, then assuming the request can be fulfilled, software will simply allocate an available range of addresses, of the appropriate type (IO, NP‐MMIO or P‐MMIO), to that device. 

This is all accomplished through the Base Address Registers (BARs) in the header of configuration space. As shown in Figure 4‐2 on page 127, a Type 0 header has six BARs available (each one being 32 bits in size), while a Type 1 header has only two BARs. Type 1 headers are found in all bridge devices, which means every switch port and root complex port has a Type 1 header. Type 0 headers are in non‐bridge devices like endpoints. An example of this can be seen in Figure 4‐3 on page 128. 

System software must first determine the size and type of address space being requested by a device. The device designer knows the collective size of the internal registers/storage that should be accessible via IO or MMIO. The device designer also knows how the device will behave when those registers are accessed (i.e. do reads have side‐effects or not). This will determine whether prefetchable MMIO (reads have no side‐effects) or non‐prefetchable MMIO (reads do have side‐effects) should be requested. Knowing this information, the device designer hard‐codes the lower bits of the BARs to certain values indicat‐ ing the type and size of the address space being requested. 

The upper bits of the BARs are writable by software. Once system software checks the lower bits of the BARs to determine the size and type of address space requested, system software will then write the base address of the address range being allocated to this device into the upper bits of the BAR. Since a single 

**126** 

**Chapter 4: Address Space & Transaction Routing** 

Endpoint (Type 0 header) has six BARs, up to six different address space requests can be made. However, this is not common in the real world. Most devices will request 1‐3 different address ranges. 

Not all BARs have to be implemented. If a device does not need all the BARs to map their internal registers, the extra BARs are hard‐coded with all 0’s notifying software that these BARs are not implemented. 

_Figure 4‐2: BARs in Configuration Space_ 

**==> picture [386 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Header Type 1 Header<br>31 23 15 7 0 31 23 15 7 0<br>Device ID Vendor ID 00h Device ID Vendor ID 00h<br>Status Command 04h Status Command 04h<br>Class Code   Rev 08h Class Code   Rev 08h<br>      ID       ID<br>BIST Header Latency Cache 0Ch BIST Header Latency Cache 0Ch<br>Type Timer Line Size Type Timer Line Size<br>Base Address 0 (BAR0) 10h Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h Base Address 1 (BAR1) 14h<br>Base Address 2 (BAR2) 18h SecondaryLat Timer SubordinateBus # SecondaryBus # PrimaryBus # 18h<br>Base Address 3 (BAR3) 1Ch SecondaryStatus LimitIO BaseIO 1Ch<br>Base Address 4 (BAR4) 20h (Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Prefetchable Prefetchable<br>Base Address 5 (BAR5) 24h Memory Limit Memory Base 24h<br>CardBus CIS Pointer 28h Prefetchable Memory Base 28h<br>Upper 32 Bits<br>SubsystemDevice ID SubsystemVendor ID 2Ch Prefetchable Memory LimitUpper 32 Bits 2Ch<br>IO Limit IO Base<br>Expansion ROM Base Address 30h Upper 16 Bits Upper 16 Bits 30h<br>Reserved Capability 34h Reserved Capability 34h<br>Pointer Pointer<br>Reserved 38h Expansion ROM Base Address 38h<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch ControlBridge InterruptPin InterruptLine 3Ch<br>**----- End of picture text -----**<br>


Once the BARs have been programmed, the internal registers or local memory within the device can be accessed via the address ranges programmed into the BARs. Anytime the device sees a request with an address that maps to one of its BARs, it will accept that request because it is the target. 

**127** 

**PCI Express Technology** 

_Figure 4‐3: PCI Express Devices And Type 0 And Type 1 Header Use_ 

**==> picture [278 x 256] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-2"></a>
## 5.2 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-3"></a>
## 5.3 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-4"></a>
## 5.4 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-5"></a>
## 5.5 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

As illustrated in Figure 4‐12 on page 146, a PCI Express topology consists of independent, point‐to‐point links connecting each device with one or more neighbors. As traffic arrives at the inbound side of a link interface (called the _ingress port_ ), the port checks for errors, then makes one of three decisions: 

1. Accept the traffic and use it internally 

2. Forward the traffic to the appropriate outbound ( _egress_ ) port 

3. Reject the traffic because it is neither the intended target, nor an interface to it (Note that there are other reasons why traffic may be rejected) 

**146** 

**Chapter 4: Address Space & Transaction Routing** 

## **Receivers Check For Three Types of Traffic** 

Assuming a link is fully operational, the receiver interface of each device (ingress port) must detect and evaluated the arrival of the three types of link traffic: Ordered Sets, Data Link Layer Packets (DLLPs), and Transaction Layer Packets (TLPs). Ordered Sets and DLLPs are local to a link and thus are never routed to another link. TLPs can and do move from link to link, based on rout‐ ing information contained in the packet headers. 

## **Routing Elements** 

Devices with multiple ports, like Root Complexes and Switches, can forward TLPs between the ports and are sometimes called Routing Agents or Routing Elements. They accept TLPs that target internal resources and forward TLPs between ingress and egress ports. 

Interestingly, peer‐to‐peer routing support is required in Switches, but for a Root Complex it’s optional. Peer‐to‐peer traffic is typically where one Endpoint sends packets that target another Endpoint. 

Endpoints have only one Link and never expect to see ingress traffic other than what is targeting them. They simply accept or reject incoming TLPs. 

## **Three Methods of TLP Routing** 

## **General** 

TLPs can be routed based on address (either memory or IO), based on ID (meaning Bus, Device, Function number), or routed implicitly. The routing method used is based on the TLP type. Table 4‐7 on page 147 summarizes the TLP types and the routing methods used for each. 

_Table 4‐7: PCI Express TLP Types And Routing Methods_ 

|**TLP Type**|**Routing Method Used**|
|---|---|
|Memory Read [Lock], Memory Write, AtomicOp|Address Routing|
|IO Read and Write|Address Routing|



**147** 

**PCI Express Technology** 

_Table 4‐7: PCI Express TLP Types And Routing Methods (Continued)_ 

|**TLP Type**|**Routing Method Used**|
|---|---|
|Configuration Read and Write|ID Routing|
|Message, Message With Data|Address Routing, ID Rout‐<br>ing, or Implicit routing|
|Completion, Completion With Data|ID Routing|



Messages are the only TLP type that support more than one routing method. Most of the message TLPs defined in the PCI Express spec use implicit routing, however, the vendor‐defined messages could use address routing or ID routing if desired. 

## **Purpose of Implicit Routing and Messages** 

In implicit routing, neither address or ID routing information applies; instead, the packet is routed based on a code in the packet header indicating a destina‐ tion with a known location in the topology, such as the Root Complex. This sim‐ plifies routing of messages in the cases where a type of implicit routing applies. 

**Why Messages?** Message transactions were not defined in PCI or PCI‐X, but were introduced with PCIe. The main reason for adding Messages as a packet type was to pursue the PCIe design goal to drastically reduce the number of sideband signals implemented in PCI (e.g. interrupt pins, error pins, power management signals, etc.). Consequently, most of the sideband signals were replaced with in‐band packets in the form of Message TLPs. 

**How Implicit Routing Helps** Using in‐band messages in place of side‐ band signals requires a means of routing them to the proper recipient in a topology consisting of numerous point‐to‐point links. Implicit routing takes advantage of the fact that Switches and other routing elements understand the concept of upstream and downstream, and that the Root Complex is found at the top of the topology while Endpoints are found at the bottom. As a result, a Message can use a simple code to show that it should go to the Root Complex, for example, or to be sent to all devices downstream. This ability eliminates the need to define address ranges or ID lists specifically used as the target of different message transactions. 

The different types of implicit routing can be found in “Implicit Routing” on page 163. 

**148** 

**Chapter 4: Address Space & Transaction Routing** 

## **Split Transaction Protocol** 

Like most other serial technologies, PCI Express uses the split transaction proto‐ col which allows a target device to receive one or more requests and then respond to each request with a separate completion. This is a significant improvement over the PCI bus protocol that used wait‐states or delayed trans‐ actions (retries) to deal with latencies in accessing targets. Instead of testing to see when the target becomes ready to do a long‐latency transfer, the target ini‐ tiates the response whenever it’s ready. This results in at least two separate TLPs per transaction ‐ the Request and the Completion (as will be discussed later, a single read request may result in multiple completion TLPs being sent back). Figure 4‐13 on page 149 illustrates the Request‐Completion components of a split transaction. This example shows software reading data from an Endpoint. 

_Figure 4‐13: PCI Express Transaction Request And Completion TLPs_ 

**==> picture [304 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>IN OUT Memory<br>1) Request TLP (Memory Read)<br>K27.7 K29.7<br>OUT IN STP SEQ HDR LCRC END<br>END byte<br>Link CRC (4 bytes)<br>TLP Header (3DW or 4DW)<br>Switch<br>TLP Sequence Number (2 bytes)<br>Receiver decode of STP symbol indicates<br>start of a TLP<br>2) Completion w/Data TLP<br>K27.7 K29.7<br>OUT IN STP SEQ HDR Data LCRC END<br>PCIe<br>Endpoint<br>IN OUT<br>OUT IN<br>**----- End of picture text -----**<br>


**149** 

**PCI Express Technology** 

## **Posted versus Non-Posted** 

To mitigate the penalty of the Request‐Completion latency, memory write trans‐ actions are posted, meaning the transaction is considered completed from the Requester’s perspective as soon as the request leaves the Requester. If helpful, you can associate the term “posting” with the postal system, where posting a memory write is analogous to posting a letter in the mail. Once you’ve placed a letter in the postal box you put your faith in the system to deliver it and don’t wait for verification of delivery. This approach can be much faster than waiting for the entire Request‐Completion transit, but — as in all posting schemes — uncertainty exists concerning when (and if) the transaction completed success‐ fully at the ultimate recipient. 

In PCIe, the small amount of uncertainty involved by making all memory writes posted is considered acceptable in exchange for the performance gained. By contrast, writes to IO and configuration space almost always affect device behavior and have a timeliness associated with them. Consequently, it is impor‐ tant to know when (and if) those write requests completed. Because of this, IO writes and configuration writes are always non‐posted and a completion will always be returned to report the status of the operation. 

In summary, non‐posted transactions require a completion. Posted transactions do not require, and should never receive, a completion. Table 4‐8 on page 150 lists which PCIe transactions are posted and non‐posted. 

_Table 4‐8: Posted and Non‐Posted Transactions_ 

|**Request**|**How Request Is Handled**|
|---|---|
|Memory Write|All**memory write requests are posted**. No completions are<br>expected or sent.|
|Memory Read<br>Memory Read Lock|All**memory read requests are non‐posted**. A completion<br>with data (made of one or more TLPs) will be returned by the<br>Completer to deliver both the requested data and the status<br>of the memory read. In the event of an error, a completion<br>without data will be returned reporting the status.|
|AtomicOp|All**AtomicOp requests are non‐posted**. A completion with<br>data will be returned by the Completer containing the origi‐<br>nal value of the target location.|



**150** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐8: Posted and Non‐Posted Transactions (Continued)_ 

|**Request**|**How Request Is Handled**|
|---|---|
|IO Read<br>IO Write|All**IO requests are non‐posted**. A completion without data<br>will be returned for writes or failed reads, and a completion<br>with data will be returned for successful reads.|
|Configuration Read<br>Configuration Write|All**configuration requests are non‐posted**. A completion<br>without data will be returned for writes and failed reads,<br>while a completion with data will be returned for successful<br>reads.|
|Message|All**messages are posted**. The routing method depends on<br>the Message type, but they’re all considered posted requests.|



## **Header Fields Define Packet Format and Type** 

## **General** 

As shown in Figure 4‐14 on page 152, each TLP contains a three or four double‐ word (12 or 16 byte) header. This includes _Format_ and _Type_ fields that define the content of the rest of the header and indicate the routing method to be used for the TLP as it traverses the topology. 

**151** 

**PCI Express Technology** 

_Figure 4‐14: Transaction Layer Packet Generic 3DW And 4DW Headers_ 

**==> picture [256 x 344] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (END)<br>Generic 3DW (12-byte) Header<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Generic 4DW (16-byte) Header<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


**152** 

**Chapter 4: Address Space & Transaction Routing** 

## **Header Format/Type Field Encodings** 

Table 4‐9 on page 153 below summarizes the encodings used in TLP header For‐ mat and Type fields. 

_Table 4‐9: TLP Header Format and Type Field Encodings_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Memory Read Request (MRd)|000 = 3DW, no data<br>001 = 4DW, no data|0 0000|
|Memory Read Lock Request (MRdLk)|000 = 3DW, no data<br>001 = 4DW, no data|0 0001|
|Memory Write Request (MWr)|010 = 3DW, w/<br>data<br>011 = 4DW, w/<br>data|0 0000|
|IO Read Request (IORd)|000 = 3DW, no data|00010|
|IO Write Request (IOWr)|010 = 3DW, w/<br>data|0 0010|
|Config Type 0 Read Request (CfgRd0)|000 = 3DW, no data|0 0100|
|Config Type 0 Write Request<br>(CfgWr0)|010 = 3DW, w/<br>data|0 0100|
|Config Type 1 Read Request (CfgRd1)|000 = 3DW, no data|0 0101|
|Config Type 1 Write Request<br>(CfgWr1)|010 = 3DW, w/<br>data|0 0101|
|Message Request (Msg)|001 = 4DW, no data|1 0RRR* (for RRR,<br>see routing subfield<br>in “Message Type<br>Field Summary” on<br>page 164)|
|Message Request w/Data (MsgD)|011 = 4DW, w/<br>data|1 0RRR* (for RRR,<br>see routing subfield<br>in “Message Type<br>Field Summary” on<br>page 164)|



**153** 

**PCI Express Technology** 

_Table 4‐9: TLP Header Format and Type Field Encodings (Continued)_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Completion (Cpl)|000 = 3DW, no data|0 1010|
|Completion W/Data (CplD)|010 = 3DW, w/<br>data|0 1010|
|Completion‐Locked (CplLk)|000 = 3DW, no data|0 1011|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-6"></a>
## 5.6 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Completion w/Data (CplDLk)|010 = 3DW, w/<br>data|0 1011|
|Fetch and Add AtomicOp Request<br>(FetchAdd)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1100|
|Unconditional Swap AtomicOp<br>Request (Swap)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1101|
|Compare and Swap AtomicOp<br>Request (CAS)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1110|
|Local TLP Prefix (LPrfx)|100 = 1DW|0 LLLL|
|End‐to‐End TLP Prefix (EPrfx)|100 = 1DW|1 EEEE|



## **TLP Header Overview** 

When TLPs are received at an ingress port, they are first checked for errors at the Physical and Data Link Layers. If there are no errors, the TLP is examined at the Transaction Layer to learn which routing method is to be used. The basic steps are: 

1. _Format_ and _Type_ fields determine the header size, format and type of the packet. 

2. Depending on the routing method associated with the packet type, the device determines whether it’s the intended recipient. If so, it will accept (consume) the TLP, but if not, it will forward the TLP to the appropriate egress port ‐ subject to the rules for ordering and flow control for that egress port. 

3. If this device is not the intended recipient nor is it in the path to the intended recipient, it will generally reject the packet as an Unsupported Request (UR). 

**154** 

**Chapter 4: Address Space & Transaction Routing** 

## **Applying Routing Mechanisms** 

Once the system addresses have been configured and transactions are enabled, devices examine incoming TLPs and use the corresponding configuration fields to route the packet. The following sections describe the basic features/function‐ ality of each routing mechanism used in routing TLPs through the PCI Express fabric. 

## **ID Routing** 

ID routing is used to target the logical position ‐ Bus Number, Device Number, Function Number (typically referred to as **BDF** ), of a Function within the topol‐ ogy. It’s compatible with routing methods used in the PCI and PCI‐X protocols for configuration transactions. In PCIe, it is still used for routing configuration packets and is also used to route completions and some messages. 

## **Bus Number, Device Number, Function Number Limits** 

PCI Express supports the same topology limits as PCI and PCI‐X: 

1. Eight bits are used to give the bus number, so a **maximum of 256 busses** are possible in a system. This includes internal busses created by Switches. 

2. Five bits give the device number, so a **maximum of 32 devices** are possible per bus. An older PCI bus or an internal bus in a switch or root complex may host more than one downstream device. However, external PCIe links are always point‐to‐point and there’s only one downstream device on the link. The device number for an external link is forced by the downstream port to always be Device 0, so every external Endpoint will always be Device 0 (unless using Alternative Routing‐ID Interpretation (ARI), in which case, there are no device numbers; more about ARI can be found in the section on “IDO (ID‐based Ordering)” on page 909. 

3. Three bits give the function number, so a **maximum of 8 internal functions** is possible per device. 

## **Key TLP Header Fields in ID Routing** 

If the Type field in a received TLP indicates ID routing is to be used, then the ID fields in the header (Bus, Device, Function) are used to perform the routing check. There are two cases: ID routing with a 3DW header and ID routing with a 4DW header (only possible in messages). Figure 4‐15 on page 156 illustrates a TLP using ID routing and the 3DW header, while Fig‐ ure 4‐16 on page 156 shows the 4DW header for ID routing. 

**155** 

**PCI Express Technology** 

_Figure 4‐15: 3DW TLP Header ‐ ID Routing Fields_ 

**==> picture [354 x 357] intentionally omitted <==**

**----- Start of picture text -----**<br>
3DW Header Using ID Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 0 Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Device Func<br>Byte 8 Bus Number Bytes 10-11 Vary with  Type  Field<br>Function Number with ARI<br>Figure 4‐16: 4DW TLP Header ‐ ID Routing Fields<br>4DW Header Using ID Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Device Func<br>Byte 8 Bus Number Bytes 10-11 Vary with  Type  Field<br>Function Number with ARI<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


## **Endpoints: One Check** 

For ID routing, an Endpoint simply checks the ID field in the packet header against its own BDF. Each function “captures” its own Bus and Device Number every time a Type 0 configuration write is seen on its link from bytes 8‐9 in the TLP Header. Where the captured Bus and Device Number information should be stored in not specified, only that functions must save it. The saved Bus and 

**156** 

**Chapter 4: Address Space & Transaction Routing** 

Device numbers are used as the Requester ID in TLP requests that this Endpoint initiates so the Completer of that request can include the Requester ID value in the completion packet(s). The Requester ID in a completion packet is used to route the completion. 

## **Switches (Bridges): Two Checks Per Port** 

For an ID‐routed TLP, a switch port first checks to see whether it is the intended target by comparing the target ID in the TLP Header against its own BDF, as shown by (1) in Figure 4‐17 on page 158. As was true for an Endpoint, each switch port captures its own Bus and Device number every time a configuration write (Type 0) is detected on its Upstream Port. If the target ID field in the TLP agrees with the ID of the switch port, it consumes the packet. If the ID field doesn’t match, it then checks to see if the TLP is targeting a device below this switch port. It does this by checking the Secondary and Subordinate Bus Num‐ ber registers to see if the target Bus Number in the TLP is within this range (inclusive). If so, then the TLP should be forwarded downstream. This check is indicated by (2) in Figure 4‐17 on page 158. If the packet was moving down‐ stream (arrived on the Upstream Port) and doesn’t match the BDF of the Upstream Port or fall within the Secondary‐Subordinate bus range, it will be handled as an Unsupported Request on the Upstream Port. 

If the Upstream Port determines that a TLP it received is for one of the devices beneath it (because the target bus number was within the range of its Second‐ ary‐Subordinate bus number range), then it forwards it downstream and all the downstream ports of the switch perform the same checks. Each downstream port checks to see if the TLP is targeting them. If so, the targeted port will con‐ sume the TLP and the other ports ignore it. If not, all downstream ports check to see if the TLP is targeting a device beneath their port. The one port that returns true on that check will forward the TLP to its Secondary Bus and the other downstream ports ignore the TLP. 

In this section, it is important to remember that each port on a switch is a Bridge, and thus has its own configuration space with a Type 1 Header. Even though Figure 4‐17 on page 158 only shows a single Type 1 Header, in reality, each port (each P2P Bridge) has its own Type 1 Header and performs the same two checks on TLPs when they are seen by that port. 

**157** 

**PCI Express Technology** 

_Figure 4‐17: Switch Checks Routing Of An Inbound TLP Using ID Routing_ 

**==> picture [338 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>CPU 31 23 15 7 0<br>Device ID Vendor ID 00h<br>__ es<br>Status Command 04h<br>Root Complex MemorySystem Class Code Line SizeCache 08h<br>— P2P - (DRAM) ee [TT] TSS BIST HeaderType LatencyTimer ee Line SizeCache 0Ch<br>Base Address 0 (BAR0) 10h<br>TLP ID Field<br>1. Packet for me?<br>(BDF) ; ee Base Address 1 (BAR1) 14h<br>Secondary Subordinate Secondary Primary 18h<br>P2P Lat Timer Bus # Bus # Bus #<br>Switch + 2. Packet for someone    beneath me? SS SecondaryStatus LimitIO BaseIO 1Ch<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>NIK —}--—— Memory LimitPrefetchable Memory BasePrefetchable 24h<br>Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>PCIe ma PCIe Cc — OO IO Limit IO Base<br>oe Upper 16 Bits Upper 16 Bits 30h<br>Endpoint Endpoint Reserved Capability 34h<br>a Pointer<br>Expansion ROM Base Address 38h<br>—<br>or ControlBridge InterruptPin InterruptLine 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Address Routing** 

TLPs that use address routing refer to the same memory (system memory and memory‐mapped IO) and IO address maps that PCI and PCI‐X transactions do. Memory requests targeting an address below 4GB (i.e. a 32‐bit address) must use a 3DW header, and requests targeting an address above 4GB (i.e. a 64‐bit address) must use a 4DW header. IO requests are restricted to 32‐bit addresses and are only implemented to support legacy functionality. 

**158** 

**Chapter 4: Address Space & Transaction Routing** 

## **Key TLP Header Fields in Address Routing** 

When the Type field indicates address routing is to be used for a TLP, then the Address Fields in the header are used to perform the routing check. These can be 32‐bit addresses or 64‐bit addresses. 

**TLPs with 32‐Bit Address** For IO or 32‐bit memory requests, a 3DW header is used as shown in Figure 4‐18. The memory‐mapped registers tar‐ geted with these TLPs will therefore reside below the 4GB memory or IO address boundary. 

**TLPs with 64‐Bit Address** For 64‐bit memory requests, a 4DW header is used as shown in Figure 4‐19 on page 160. The memory‐mapped registers targeted with these TLPs are able to reside above the 4GB memory bound‐ ary. 

_Figure 4‐18: 3DW TLP Header ‐ Address Routing Fields_ 

**==> picture [370 x 148] intentionally omitted <==**

**----- Start of picture text -----**<br>
3DW Header Using Address Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>0 x 0 tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**159** 

**PCI Express Technology** 

_Figure 4‐19: 4DW TLP Header ‐ Address Routing Fields_ 

**==> picture [372 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
4DW Header Using Address Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>0 x 1 tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- End of picture text -----**<br>


## **Endpoint Address Checking** 

If an Endpoint receives a TLP that uses address routing then it checks the address in the header against each of its implemented Base Address Registers (BARs) in its configuration header, as shown in Figure 4‐20. Since Endpoints only have one link interface, it will either accept the packet or reject it. The End‐ point will accept the packet if the target address in the TLP matches one of the ranges programmed into its BARs. More info on how the BARs are used can be found in section “Base Address Registers (BARs)” on page 126. 

**160** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐20: Endpoint Checks Incoming TLP Address_ 

**==> picture [335 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-7"></a>
## 5.7 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

CPU Type 0 Header<br>31 23 15 7 0<br>Device ID Vendor ID 00h<br>Root Complex System Status Command 04h<br>Memory<br>P2P (DRAM) Class Code Line SizeCache 08h<br>BIST Header Latency Cache 0Ch<br>TLP Type Timer Line Size<br>(Addr) Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h<br>P2P<br>Base Address 2 (BAR2) 18h<br>Switch Packet for me? Base Address 3 (BAR3) 1Ch<br>Base Address 4 (BAR4) 20h<br>TLP { Base Address 5 (BAR5) 24h<br>(Addr) CardBus CIS Pointer 28h<br>PCIe PCIe SubsystemDevice ID SubsystemVendor ID 2Ch<br>Endpoint Endpoint Expansion ROM Base Address 30h<br>Reserved Capability 34h<br>TLP Address field Pointer<br>should match a BAR Reserved 38h<br>within a PCIe Function Max Lat Min Gnt InterruptPin InterruptLine 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Switch Routing** 

If an incoming TLP uses address routing, a Switch Port first checks to see if the address is local within the Port itself by comparing the address in the packet header against its two BARs in its Type 1 configuration header, as shown in Step 1 of Figure 4‐21 on page 162. If it matches one of these BARs, the switch port is the target of the TLP and consumes the packet. If not, the port then checks its Base/Limit register pairs to see if the TLP is targeting a function beneath (downstream of) this bridge. If the Request targets IO space, it will check the IO Base and Limit registers, as shown in Step 2a. However, if the Request targets memory space, it will check the Non‐ prefetchable Memory Base/ Limit registers and the Prefetchable Memory Base/Limit registers, as indicated by Step 2b in Figure 4‐21 on page 162. More info on how the Base/Limit register pairs are evaluated can be found in section “Base and Limit Registers” on page 136. 

**161** 

**PCI Express Technology** 

_Figure 4‐21: Switch Checks Routing Of An Inbound TLP Using Address_ 

**==> picture [349 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>CPU 31 23 15 7 0<br>Device ID Vendor ID 00h<br>__ es<br>Status Command 04h<br>Root Complex MemorySystem Class Code Line SizeCache 08h<br>P2P - (DRAM) [—_] e BIST HeaderType s e LatencyTimer Line Size ee Cache 0Ch<br>Base Address 0 (BAR0) 10h<br>TLP<br>1. Packet for me?<br>(Addr) Base Address 1 (BAR1) 14h<br>Secondary Subordinate Secondary Primary 18h<br>P2P Lat Timer Bus # Bus # Bus #<br>2a. IO Packet for some- SecondaryStatus LimitIO BaseIO 1Ch<br>Switch       one beneath me? | (Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>— —— 2b. Mem Packet for some- _— Prefetchable Prefetchable 24h<br>Memory Limit Memory Base<br>      one beneath me? Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>PCIe PCIe IO Limit IO Base<br>Upper 16 Bits Upper 16 Bits 30h<br>7 7 ee<br>Endpoint Endpoint Reserved Capability 34h<br>es Pointer<br>Expansion ROM Base Address 38h<br>— ae<br>ee ControlBridge InterruptPin Interrupt ee Line 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


To understand routing of address‐based TLPs in switches, it is good to remember that each switch port is its own bridge. Below are the steps that a bridge (switch port) takes upon receiving an address‐based TLP: 

## **Downstream Traveling TLPs (Received on Primary Interface)** 

1. IF the target address in the TLP matches one of the BARs, then this bridge (switch port) consumes the TLP because it is the target of the TLP. 

2. IF the target address in the TLP falls in the range of one of its Base/ Limit register sets, the packet will be forwarded to the secondary inter‐ face (downstream). 

3. ELSE the TLP will be handled as an Unsupported Request on the pri‐ mary interface. (This is true if no other bridges on the primary interface claim the TLP either.) 

**162** 

**Chapter 4: Address Space & Transaction Routing** 

## **Upstream Traveling TLPs (Received on Secondary Interface)** 

1. IF the target address in the TLP matches one of the BARs, then this bridge (switch port) consumes the TLP because it is the target of the TLP. 

2. IF the target address in the TLP falls in the range of one of its Base/ Limit register sets, the TLP will be handled as an Unsupported Request on the secondary interface. (This is true unless this port is the upstream port of the switch. In these cases, the packet may be a peer‐to‐peer transaction and will be forwarded downstream on a different down‐ stream port than the one it was received on.) 

3. ELSE the TLP will be forwarded to the primary interface (upstream) given that the TLP address is not for this bridge and is not for any func‐ tion beneath this bridge. 

## **Multicast Capabilities** 

The 2.1 version of the PCI Express specification added support for specifying a range of addresses that provide multicast functionality. Any packets received that fall within the address range specified as the multicast range are routed/ accepted according to the multicast rules. This address range might not be reserved in a function’s BARs and might not be within a bridge’s Base/Limit reg‐ ister pair, but would still need to be accepted/forwarded appropriately. More info can be found on the multicast functionality in the section on “Multicast Capability Registers” on page 889. 

## **Implicit Routing** 

Implicit routing, used in some message packets, is based on the awareness of routing elements that the topology has upstream and downstream directions and a single Root Complex at the top. This allows some simple routing methods without the need to assign a target address or ID. Since the Root Complex gen‐ erally integrates power management, interrupt, and error handling logic, it is either the source or recipient of most PCI Express messages. 

## **Only for Messages** 

Some messages use address or ID routing rather than implicit routing, and for them, the routing mechanisms are applied in the same way as described in the those sections. However, most messages use implicit routing. The purpose of implicit routing is to mimic side‐band signal behavior since a design goal for PCIe was to eliminate as many side‐band signals from PCI as possible. These 

**163** 

**PCI Express Technology** 

side‐band signals in PCI were typically either the host notifying all devices of an event or devices notifying the host of an event. In PCIe, we have Message TLPs to convey these events. The types of events that PCIe has defined messages for are: 

- Power Management 

- INTx legacy interrupt signaling 

- Error signaling 

- Locked Transaction support 

- Hot Plug signaling 

- Vendor‐specific signaling 

- Slot Power Limit settings 

## **Key TLP Header Fields in Implicit Routing** 

For implicit routing, the routing sub‐field in the header is used to determine the message destination. Figure 4‐22 on page 164 illustrates a message TLP using implicit routing. 

_Figure 4‐22: 4DW Message TLP Header ‐ Implicit Routing Fields_ 

**==> picture [355 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
4DW Header for Messages<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R TH T E Attr AT Length<br>0 x 1 1  0  r  r  r tr 0 D P 0 0 0 0<br>Message<br>Byte 4 Requester ID Tag<br>Code<br>Byte 8 Bytes 8-11 Vary with  Message Code  Field<br>Byte 12 Bytes 12-15 Vary with  Message Code  Field<br>**----- End of picture text -----**<br>


## **Message Type Field Summary** 

Table 4‐10 on page 165 shows how the TLP header Type field for Messages is interpreted. As shown, the upper two bits indicate the packet is a Message while the lower three bits specify the routing method to apply. Note that Mes‐ sage TLPs always use a 4DW header regardless of the routing option selected. 

**164** 

**Chapter 4: Address Space & Transaction Routing** 

For address routing, bytes 8‐15 contain up to a 64‐bit address, and for ID rout‐ ing, bytes 8 and 9 contain the target BDF. 

_Table 4‐10: Message Request Header Type Field Usage_ 

|**Type Field Bits**|**Description**|
|---|---|
|Bit 4:3|Defines the type of transaction:<br>10b = Message TLP|
|Bit 2:0|Message Routing Subfield R[2:0]<br>• 000b = Implicit ‐ Route to the Root Complex<br>• 001b = Route by Address (bytes 8‐15 of header contain address)<br>• 010b = Route by ID (bytes 8‐9 of header contain ID)<br>• 011b = Implicit ‐ Broadcast downstream<br>• 100b = Implicit ‐ Local: terminate at receiver<br>• 101b = Implicit ‐ Gather & route to the Root Complex<br>• 110b ‐ 111b = Reserved: terminate at receiver|



## **Endpoint Handling** 

For implicit routing, an Endpoint simply checks whether the routing sub‐field is appropriate for it. For example, an Endpoint will accept a Broadcast Message or a Message that terminates at the receiver; but not Messages that implicitly target the Root Complex. 

## **Switch Handling** 

Routing elements like Switches consider the port on which the TLP arrived on and whether the routing sub‐field code is appropriate for it. For example: 

1. A Switch Upstream Port may legitimately receive a Broadcast Message. It will duplicate that and forward it to all its Downstream Ports. An implicitly routed Broadcast Message received on a Downstream Port of a Switch (meaning the message was traveling upstream) would be an error that would be handled as a Malformed TLP. 

2. A Switch may receive implicitly routed Messages for the Root Complex on Downstream Ports and will forward these to its Upstream Port because the location of the Root Complex is understood to be upstream. It would not accept Messages received on its Upstream Port (meaning the message was traveling downstream) that are implicitly routed to the Root Complex. 

**165** 

## **PCI Express Technology** 

3. If an implicitly routed Message indicates it should terminate at the receiver, then the receiving switch port will consume the message rather than for‐ ward it. 

4. For messages routed using address or ID routing, a Switch will simply per‐ form normal address or ID checks in deciding whether to accept or forward it. 

## **DLLPs and Ordered Sets Are Not Routed** 

DLLP and Ordered Set traffic is not routed from ingress ports to egress ports of switches or root complexes. These packets move from port to port across a link from Physical Layer to Physical Layer. 

DLLPs originate at the Data Link Layer of a PCI Express port, pass through the Physical Layer, exit the port, traverse the Link and arrive at the neighboring port. At this port, the packet passes through the Physical Layer and ends up at the Data Link Layer where it is processed and consumed. DLLPs do not pro‐ ceed further up the port to the Transaction Layer and hence are not routed. 

Similarly, Ordered‐Set packets originate at the Physical Layer, exit the port, traverse the Link and arrive at the neighboring port. At this port, the packet arrives at the Physical Layer where it is processed and consumed. Ordered‐Sets do not proceed further up the port to the Data Link Layer and Transaction Layer and hence are not routed. 

As has been discussed in this chapter, only TLPs are routed through switches and root complexes. The originate at the Transaction Layer of a source port and end up at the Transaction Layer of a destination port. 

**166** 

## Part Two: 

# Transaction Layer 

## _**5**_ 

## _**TLP Elements**_ 

## **The Previous Chapter** 

The previous chapter describes the purpose and methods of a function request‐ ing address space (either memory address space or IO address space) through Base Address Registers (BARs) and how software must setup the Base/Limit registers in all bridges to route TLPs from a source port to the correct destina‐ tion port. The general concepts of TLP routing in PCI Express are also dis‐ cussed, including address‐based routing, ID‐based routing and implicit routing. 

## **This Chapter**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-8"></a>
## 5.8 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Information moves between PCI Express devices in packets. The three major classes of packets are _Transaction Layer Packets_ (TLPs), _Data Link Layer Packets_ (DLLPs) and _Ordered Sets_ . This chapter describes the use, format, and definition of the variety of TLPs and the details of their related fields. DLLPs are described separately in Chapter 9, entitled ʺDLLP Elements,ʺ on page 307. 

## **The Next Chapter** 

The next chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Transaction Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like disconnects, retries, and wait‐states. 

## **Introduction to Packet-Based Protocol** 

## **General** 

Unlike parallel buses, serial transport buses like PCIe use no control signals to identify what’s happening on the Link at a given time. Instead, the bit stream they send must have an expected size and a recognizable format to make it pos‐ 

**169** 

**PCI Ex ress Technolo p gy** 

sible for the receiver to understand the content. In addition, PCIe does not use any immediate handshake for the packet while it is being transmitted. 

With the exception of the Logical Idle symbols and Physical Layer packets called _Ordered Sets_ , information moves across an active PCIe Link in fundamen‐ tal chunks called packets that are comprised of symbols. The two major classes of packets exchanged are the high‐level _Transaction Layer Packets_ (TLPs), and low‐level Link maintenance packets called _Data Link Layer Packets_ (DLLPs). The packets and their flow are illustrated in Figure 5‐1 on page 170. Ordered Sets are packets too, however, they are not framed with a start and end symbol like TLPs and DLLPs are. They are also not byte striped like TLPs and DLLPs are. Ordered Set packets are instead replicated on all Lanes of a Link. 

_Figure 5‐1: TLP And DLLP Packets_ 

**==> picture [350 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>DLLP TLP<br>DLLP TLP (Link)<br>Transaction Layer Packet (TLP)<br>STP Seq Num HDR Data Digest CRC End TLP Types:<br>- Memory Read / Write<br>- IO Read / Write<br>- Configuration Read / Write<br>- Completion<br>- Message<br>Data Link Layer Packet (DLLP)<br>- AtomicOp<br>Framing C Framing DLLP Types:<br>DLLP R - TLP Ack/Nak<br>(SDP) C (END)<br>- Power Management<br>- Link Flow Control<br>- Vendor-Specific<br>**----- End of picture text -----**<br>


**170** 

**Chapter 5: TLP Elements** 

## **Motivation for a Packet-Based Protocol** 

There are three distinct advantages to using a packet‐based protocol especially when it comes to data integrity: 

## **1. Packet Formats Are Well Defined** 

Earlier buses like PCI allow transfers of indeterminate size, making identifica‐ tion of payload boundaries impossible until the end of the transfer. In addition, either device is able to terminate the transfer before it completes, making it diffi‐ cult for the sender to calculate and send a checksum or CRC covering an entire payload. Instead, PCI uses a simple parity scheme and checks it on each data phase. 

By comparison, PCIe packets have a known size and format. The packet _header_ at the beginning indicates the packet type and contains the required and optional fields. The size of the header fields is fixed except for the address, which can be 32 bits or 64 bits in size. Once a transfer commences, the recipient can’t pause or terminate it early. This structured format allows including infor‐ mation in the TLPs to aid in reliable delivery, including framing symbols, CRC, and a packet Sequence Number. 

## **2. Framing Symbols Define Packet Boundaries** 

When using 8b/10b encoding in Gen1 and Gen2 mode of operation, each TLP and DLLP packet sent is framed by Start and End control symbols, clearly defining the packet boundaries for the receiver. This is a big improvement over PCI and PCI‐X, where the assertion and de‐assertion of the single FRAME# sig‐ nal indicates the beginning and end of a transaction. A glitch on that signal (or any of the other control signals) could cause a target to misconstrue bus events. A PCIe receiver must properly decode a complete 10‐bit symbol before conclud‐ ing Link activity is beginning or ending, so unexpected or unrecognized sym‐ bols are more easily recognized and handled as errors. 

For the 128b/130b encoding used in Gen3, control characters are no longer employed and there are no framing symbols as such. For more on the differ‐ ences between Gen3 encoding and the earlier versions, see Chapter 12, entitled ʺPhysical Layer ‐ Logical (Gen3),ʺ on page 407. 

**171** 

**PCI Ex ress Technolo p gy** 

## **3. CRC Protects Entire Packet** 

Unlike the side‐band parity signals used by PCI during the address and data phases of a transaction, the in‐band CRC value of PCIe verifies error‐free deliv‐ ery of the entire packet. TLP packets also have a Sequence Number appended to them by the transmitter’s Data Link Layer so that if an error is detected at the Receiver, the problem packet can be automatically resent. The transmitter main‐ tains a copy of each TLP sent in a _Retry Buffer_ until it has been acknowledged by the receiver. This TLP acknowledgement mechanism, called the _Ack/Nak Proto‐ col_ , (and described in Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317) forms the basis of Link‐level TLP error detection and correction. This Ack/Nak Protocol error recovery mechanism allows for a timely resolution of the prob‐ lem at the place or Link where the problem occurred, but requires a local hard‐ ware solution to support it. 

## **Transaction Layer Packet (TLP) Details** 

In PCI Express, high‐level transactions originate in the device core of the trans‐ mitting device and terminate at the core of the receiving device. The Transaction Layer acts on these requests to assemble outbound TLPs in the Transmitter and interpret them at the Receiver. Along the way, the Data Link Layer and Physical Layer of each device also contribute to the final packet assembly. 

## **TLP Assembly And Disassembly** 

The general flow of TLP assembly at the transmit side of a Link and disassem‐ bly at the receiver is shown in Figure 5‐2 on page 173. Let’s now walk through the steps from creation of a packet to its delivery to the core logic of the receiver. The key stages in Transaction Layer Packet assembly and disassembly are listed below. The list numbers correspond to the numbers in Figure 5‐2 on page 173. 

## **Transmitter:** 

1. The core logic of Device A sends a request to its PCIe interface. How this is accomplished is outside the scope of the spec or this book. The request includes: 

   - Target address or ID (routing information) 

   - Source information such as Requester ID and Tag 

   - Transaction type/packet type (Command to perform, such as a memory read.) 

   - Data payload size (if any) along with data payload (if any) 

   - Traffic Class (to assign packet priority) 

   - Attributes of the Request (No Snoop, Relaxed Ordering, etc.) 

**172** 

**Chapter 5: TLP Elements** 

2. Based on that request, the Transaction Layer builds the TLP header, appends any data payload, and optionally calculates and appends the digest (End‐to‐End CRC, ECRC) if that’s supported and has been enabled. At this point the TLP is placed into a Virtual Channel buffer. The Virtual Channel manages the sequence of TLPs according to the Transaction Order‐ ing rules and also verifies that the receiver has enough flow control credits to accept a TLP before it can be passed down to the Data Link Layer. 

3. When it arrives at the Data Link Layer, the TLP is assigned a Sequence Number and then a Link CRC is calculated based on the contents of the TLP and that Sequence Number. A copy of the resulting packet is saved in the Retry Buffer in case of transmission errors while it is also passed on to the Physical Layer. 

_Figure 5‐2: PCIe TLP Assembly/Disassembly_ 

**==> picture [370 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) Outbound From Transmitter Core: Device A Device B (8) Inbound To Receiver Core:<br>Requests to write/read data, Data R/W Requests,<br>Completions, Messages, etc. Device Device Completions, Messages, etc.<br>Core Core<br>(2) Transaction Transaction (7)<br>HDR Data Digest  Layer  Layer HDR Data Digest<br>(3) (3) Data Data (6) (6)<br>Seq Num HDR Data Digest CRC Link Layer Link Layer Seq Num HDR Data Digest CRC<br>STP(4) Seq Num HDR Data Digest CRC End(4) PhysicalLayer PhysicalLayer STP(5) Seq Num HDR Data Digest CRC End(5)<br>(RX) (TX) (RX) (TX)<br>**----- End of picture text -----**<br>


4. The Physical Layer does several things to prepare the packet for serial transmission, including byte striping, scrambling, encoding, and serializing the bits. For Gen1 and Gen2 devices, when using 8b/10b encoding, the con‐ trol characters STP and END are added to either end of the packet. Finally, the packet is transmitted across the Link. In Gen3 mode, STP token is added to the front end of a TLP, but END is not added to the end of the packet. Rather the STP token contains information about TLP packet size. 

## **Receiver:** 

5. At the Receiver (Device B in this example), everything done to prepare the packet for transmission must now be undone. The Physical Layer de‐serial‐ izes the bit stream, decodes the resulting symbols, and un‐stripes the bytes. 

**173** 

**PCI Ex ress Technolo p gy** 

   - The control characters are removed here because they only have meaning at the Physical Layer, and then the packet is forwarded to the Data Link Layer. 

6. The Data Link Layer calculates the CRC and compares it to the received CRC. If that matches, the Sequence Number is checked. If there are no errors, the CRC and Sequence Number are removed and the TLP is passed to the Transaction Layer of the receiver and notifies the sender of good reception by returning an Ack DLLP. In the event of an error a Nak will be returned instead, and the transmitter will re‐replay TLPs in its Retry Buffer. 

7. At the Transaction Layer, the TLP is decoded and the information is passed to the core logic for appropriate action. If the receiving device is the final target of this packet, it checks for ECRC errors and reports any related ECRC error condition to the core logic should there be any. 

## **TLP Structure** 

The basic usage of each field in a Transaction Layer Packet is defined in Table 5‐ 1 on page 174. 

_Table 5‐1: TLP Header Type Field Defines Transaction Variant_ 

|**TLP**<br>**Component**|**Protocol**<br>**Layer**|**Component Use**|
|---|---|---|
|Header|Transaction<br>Layer|3 or 4DW (12 or 16 bytes) in size. Format varies with<br>type, but Header defines parameters, including:<br>•<br>Transaction type<br>•<br>Target address, ID, etc.<br>•<br>Transfer size (if any), Byte Enables<br>•<br>Attributes<br>•<br>Traffic Class|
|Data|Transaction<br>Layer|Optional 1‐1024 DW Payload, which is qualified<br>with Byte Enables or byte‐aligned start and end<br>addresses. Note that a length of zero can’t be speci‐<br>fied, but a zero‐length read (useful in some cases)<br>can be approximated by specifying a length of 1 DW<br>and Byte Enables of all zero. The resulting data from<br>the Completer will be undefined but the Requester<br>doesn’t use it, so the result is the same.|
|Digest/ECRC|Transaction<br>Layer|Optional. When present, ECRC is always 1 DW in<br>size.|



**174** 

**Chapter 5: TLP Elements** 

## **Generic TLP Header Format** 

## **General**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-9"></a>
## 5.9 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-10"></a>
## 5.10 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

8. If a read request of 1 DW has no byte enables set, the completer returns a 1DW data payload of undefined data. This may be used as a Flush mecha‐ nism that takes advantage of transaction ordering rules to force all previ‐ ously posted writes out to memory before the completion is returned. 

**181** 

## **PCI Ex ress Technolo p gy** 

**Byte Enable Example.** An example of byte enable use in this case is illus‐ trated in Figure 5‐4 on page 182. Note that the transfer length must extend from the first DW with any valid byte enabled to the last DW with any valid bytes enabled. Because the transfer is more than 2DW, the byte enables may only be used to specify the start address location (2d) and end address location (34d) of the transfer. 

_Figure 5‐4: Using First DW and Last DW Byte Enable Fields_ 

## **Transaction Descriptor Fields** 

As transactions move between requester and completer, it’s necessary to uniquely identify a transaction, since many split transactions may be queued up from the same Requester at any instant. To help with this, the spec defines sev‐ eral important header fields that form a unique Transaction Descriptor, as illus‐ trated in Figure 5‐5. 

**182** 

**Chapter 5: TLP Elements** 

_Figure 5‐5: Transaction Descriptor Fields_ 

**==> picture [384 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Completer ID Cmpl CB Byte Count<br>Status M<br>Byte 8 Requester ID Tag R Lower Addr<br>**----- End of picture text -----**<br>


While the Transaction Descriptor fields are not in adjacent header locations, col‐ lectively they describe key transaction attributes, including: 

**Transaction ID.** The combination of the Requester ID (Bus, Device, and Function Number of the Requester) and the Tag field of the TLP. 

**Traffic Class.** The Traffic Class (TC) is added by the requester based on the core logic request and travels unmodified through the topology to the Compl‐ eter. On every Link, the TC is mapped to one of the Virtual Channels. 

**Transaction Attributes.** The ID‐based Ordering, Relaxed Ordering, and No Snoop bits also travel with the Request packet to the Completer. 

## **Additional Rules For TLPs With Data Payloads** 

The following rules apply when a TLP includes a data payload. 

1. The Length field refers only to the data payload. 

2. The first byte of data in the payload (immediately after the header) is always associated with the lowest (start) address. 

3. The Length field always represents an integral number of DWs transferred. Partial DWs are qualified using First and Last Byte Enable fields. 

4. The spec states that, when multiple transactions are returned by a compl‐ eter in response to a single memory request, each intermediate transaction must end on naturally‐aligned 64‐ or 128‐byte address boundaries for a Root Complex. This is controlled by a configuration bit called the Read Completion Boundary (RCB). All other devices follow the PCI‐X protocol 

**183** 

## **PCI Ex ress Technolo p gy** 

and break such transactions at naturally‐aligned 128‐byte boundaries. This makes buffer management simpler in bridges. 

5. The Length field is reserved when sending Message Requests unless the message is the version with data ( _MsgD_ ). 

6. The TLP data payload must not exceed the current value in the Max_Payload_Size field of the Device Control Register. Only write transac‐ tions have data payloads, so this restriction doesn’t apply to read requests. A receiver is required to check for violations of the Max_Payload_Size limit during writes, and violations are treated as Malformed TLPs. 

7. Receivers also must check for discrepancies between the value in the Length field and the actual amount of data transferred in a TLP. This type of viola‐ tion is also treated as a Malformed TLP. 

8. Requests must not mix combinations of start address and transfer length that would cause a memory access to cross a 4KB boundary. While checking for this is optional, if seen it’s treated as a Malformed TLP. 

## **Specific TLP Formats: Request & Completion TLPs** 

In this section, the format of 3DW and 4DW headers used to accomplish specific transaction types are described. Many of the generic fields described previously apply, but an emphasis is placed on the fields which are handled differently with specific transaction types. Detailed description of TLP Header format are described is sections following for TLP types: 1) IO Request, 2) Memory Requests, 3) Configuration Requests, 4) Completions and 5) Message Requests. 

## **IO Requests** 

While the spec discourages the use of IO transactions, allowance is made for Legacy devices and for software that may need to rely on a compatible device residing in the system IO map rather than the memory map. While the IO trans‐ actions can technically access a 32‐bit IO range, in reality many systems (and CPUs) restrict IO access to the lower 16 bits (64KB) of this range. Figure 5‐6 on page 185 depicts the system IO map and the 16‐ and 32‐bit address boundaries. Devices that don’t identify themselves as Legacy devices are not permitted to request IO address space in their configuration Base Address Registers. 

**184** 

**Chapter 5: TLP Elements** 

_Figure 5‐6: System IO Map_ 

**IO Request Header Format.** A 3 DW IO request header is shown in Fig‐ ure 5‐7 on page 185 and each of the fields is described in the section that fol‐ lows. 

_Figure 5‐7: 3DW IO Request Header Format_ 

**==> picture [281 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>IO Request TLP<br>a|<br>Legacy =o Framing(STP) SequenceNumber Header Data Digest LCRC Framing(End)<br>Endpoint<br>+0 +1 +2 +3<br>Peer 7 6 5 4 3 2 1 0 7 nT 6 5 4 3 2 1 0 7 6 5 4 3 2 TTT 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 0 1 0Type R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**185** 

**PCI Ex ress Technolo p gy** 

**IO Request Header Fields.** The location and use of each field in an IO request header is described in Table 5‐4 on page 186. 

_Table 5‐4: IO Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Format for IO requests:<br>000b = IO Read (3DW without data)<br>010b = IO Write (3DW with data)|
|Type [4:0]|Byte 0 Bit 4:0|Packet type is 00010b for IO requests|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|Traffic Class for IO requests is always<br>zero, ensuring that these packets will<br>never interfere with any high‐priority<br>packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|ID‐based Ordering doesn’t apply for<br>IO requests and this bit is reserved.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|TLP processing Hints don’t apply to<br>IO requests and this bit is reserved.|
|TD<br>(TLP Digest)|Byte 2 Bit 7|Indicates the presence of a digest field<br>(ECRC) at the end of the TLP.|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|Indicates whether the data payload (if<br>present) is poisoned.|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Relaxed Ordering and No Snoop bits<br>don’t apply for IO requests and are<br>always zero.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type doesn’t apply for IO<br>requests and these bits must be zero.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW.<br>For IO requests, this field is always<br>just 1 since no more than 4 bytes can<br>be transferred. The First DW Byte<br>Enables qualify which bytes are used.|



**186** 

**Chapter 5: TLP Elements** 

_Table 5‐4: IO Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester’s “return<br>address” for corresponding Comple‐<br>tion.<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|These bits identify the specific<br>requests from the requester. A unique<br>tag value is assigned to each outgoing<br>Request. By default, only bits 4:0 are<br>used, but the Extended Tag and Phan‐<br>tom Functions options can extend that<br>to 11 bits, permitting up to 2048 out‐<br>standing requests to be in progress<br>simultaneously.|
|Last DW BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|These bits must be 0000b because IO<br>requests can only be one DW in size.|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|These bits qualify the bytes in the one‐<br>DW payload. For IO requests, any bit<br>combination is valid (including all<br>zeros).|
|Address [31:2]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:2|The upper 30 bits of the 32‐bit start<br>address for the IO transfer. The lower<br>two bits of the 32 bit address are<br>reserved (00b), forcing a DW‐aligned<br>start address.|



**187** 

**PCI Ex ress Technolo p gy** 

## **Memory Requests** 

PCI Express memory transactions include two classes: Read Requests with their corresponding Completions, and Write Requests. The system memory map shown in Figure 5‐8 on page 188 depicts both a 3DW and 4DW memory request packet. Keep in mind a point that the spec reiterates several times: a memory transfer is never permitted to cross a 4KB address boundary. 

_Figure 5‐8: 3DW And 4DW Memory Request Header Formats_ 

**==> picture [382 x 316] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex Memory<br>3DW or 4DW Memory Request TLP<br>Framing(STP) SequenceNumber Header Data Digest LCRC Framing(End)<br>4DW Memory Request Header<br>PCIe +0 +1 +2 +3<br>Endpoint System Memory Map<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2 64<br>Byte 0 0 x 1Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>3DW Memory Request Header<br>+0 +1 +2 +3<br>4GB<br>32<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 2<br>Byte 0 0 x 0Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE 0<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**Memory Request Header Fields.** The location and use of each field in a 4DW memory request header is listed in Table 5‐5 on page 189. Note that the difference between a 3DW header and a 4DW header is simply the location and size of the starting Address field. 

**188** 

**Chapter 5: TLP Elements** 

_Table 5‐5: 4DW Memory Request Header Fields_ 

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|Packet Formats:<br>000b = Memory Read (3DW w/o data)<br>010b = Memory Write (3DW w/ data)<br>001b = Memory Read (4DW w/o data)<br>011b = Memory Write (4DW w/ data)<br>1xxb = TLP Prefix has been added to<br>the beginning of the packet. See “TPH<br>(TLP Processing Hints)” on page 899<br>for more on this.|
|Type[4:0]|Byte 0 Bit 4:0|TLP packet Type field:<br>00000b = Memory Read or Write<br>00001b = Memory Read Locked<br>Type field is used with Fmt [1:0] field<br>to specify transaction type, header<br>size, and whether data payload is<br>present.|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4|These bits encode the traffic class to<br>be applied to a Request and to any<br>associated Completion.<br>000b = Traffic Class 0 (Default)<br>.<br>.<br>111b = Traffic Class 7<br>See“Traffic Class (TC)” on page 247<br>for more on this.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|Indicates whether ID‐based Ordering<br>is to be used for this TLP. To learn<br>more, see “ID Based Ordering (IDO)”<br>on page 301.|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-11"></a>
## 5.11 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-12"></a>
## 5.12 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-13"></a>
## 5.13 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|Requester ID<br>Tag<br>Message<br>Code<br>4DW Header for Messages<br>Byte 0<br>Byte 12<br>Byte 4<br>+3<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>7 6 5 4 3 2 1 0<br>+2<br>+1<br>+0<br>Length<br>TC<br>Bytes 12-15 Vary with_Message Code_Field<br>Byte 8<br>Bytes 8-11 Vary with_Message Code_Field<br>R<br>R<br>R<br>E<br>P<br>AT<br>0 0<br>Attr<br>0 0<br>Fmt<br>0 x 1<br>Type<br>1  0  r  r  r<br>T<br>D<br>TH<br>0<br>At<br>tr|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Fmt<br>0 x 1|Type<br>1  0  r  r  r|R|TC|R|At<br>tr|R|TH<br>0|T<br>D|E<br>P|Attr<br>0 0|AT<br>0 0|Length||
||Requester ID||||||||Tag|||||Message<br>Code|
||Bytes 8-11 Vary with_Message Code_Field||||||||||||||
||Bytes 12-15 Vary with_Message Code_Field||||||||||||||



**203** 

**PCI Ex ress Technolo p gy** 

## **Message Request Header Fields.** 

_Table 5‐8: Message Request Header Fields_ 

|**Field Name**|**Header Byte/**<br>**Bit**||**Function**|
|---|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5||Packet Format. Always a 4DW header<br>001b = Message Request without data<br>011b = Message Request with data|
|Type [4:0]|Byte 0 Bit 4:0||TLP packet type field. Set to:<br>Bit 4:3:<br>10b = Msg<br>Bit 2:0<br>(Message Routing Subfield)<br>000b = Implicitly Routed to RC (Root<br>Complex)<br>001b = Routed by address<br>010b = Routed by ID<br>011b = Implicitly Broadcast from RC<br>100b = Local; terminate at receiver<br>101b = Gather & route to RC<br>0thers = Reserved, treated as Local|
|TC [2:0]<br>(Traffic Class)|Byte 1 Bit 6:4||TC is always zero for most Message<br>Requests, ensuring that they don’t inter‐<br>fere with high‐priority packets.|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2||Indicates whether ID‐based Ordering is<br>to be used for this TLP. To learn more, see<br>“ID Based Ordering (IDO)” on page 301.|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||Reserved, except as noted.|
|TD|Byte 2 Bit 7||If = 1, indicates the presence of a<br>digest field (1 DW) at the end of the TLP<br>(preceding LCRC and END)|
|EP|Byte 2 Bit 6||If = 1, indicates the data payload (if<br>present) is poisoned.|



**204** 

**Chapter 5: TLP Elements** 

_Table 5‐8: Message Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/**<br>**Bit**|**Function**|
|---|---|---|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|Except as noted, these are always<br>reserved in Message Requests.|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|Address Type is reserved for Messages<br>and must be zero, but Receivers are not<br>required or even encouraged to check<br>this.|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|Indicates data payload size in DW. For<br>Message Requests, this field is always 0<br>(no data) or 1 (one DW of data)|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|Identifies the Requester sending the mes‐<br>sage.<br>Byte 4, 7:0 = Requester Bus #<br>Byte 5, 7:3 = Requester Device #<br>Byte 5, 2:0 = Requester Function #|
|Tag [7:0]|Byte 6 Bit 7:0|Since all Message Requests are posted<br>and don’t receive Completions, no tag is<br>assigned to them. These bits should be<br>zero.|
|Message Code [7:0]|Byte 7 Bit 7:0|This field contains the code indicating<br>the type of message being sent.<br>0000 0000b = Unlock Message<br>0001 0000b = Lat. Tolerance Reporting<br>0001 0010b = Optimized Buffer Flush/Fill<br>0001 xxxxb = Power Mgt. Message<br>0010 0xxxb = INTx Message<br>0011 00xxb = Error Message<br>0100 xxxxb = Ignored Messages<br>0101 0000b = Set Slot Power Message<br>0111 111xb = Vendor‐Defined Messages|



**205** 

## **PCI Ex ress Technolo p gy** 

_Table 5‐8: Message Request Header Fields (Continued)_ 

|**Field Name**|**Header Byte/**<br>**Bit**|**Function**|
|---|---|---|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|If address routing was selected for the<br>message (see Type 4:0 field above), then<br>this field contains the upper 32 bits of the<br>64 bit starting address.<br>Otherwise, this field is not used.|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|If address routing is selected (see Type<br>field above), then this field contains the<br>lower part of the 64‐bit starting address.<br>If ID routing is selected, Bytes 8 and 9<br>form the target ID.<br>Otherwise, this field is not used.|



**Message Notes:** The following tables specify the message coding used for each of the nine message groups, and is based on the message code field listed in Table 5‐8 on page 204. The defined message groups include: 

1. INTx Interrupt Signaling 

2. Power Management 

3. Error Signaling 

4. Locked Transaction Support 

5. Slot Power Limit Support 

6. Vendor‐Defined Messages 

7. Ignored Messages (related to Hot‐Plug support in spec revision 1.1) 

8. Latency Tolerance Reporting (LTR) 

9. Optimized Buffer Flush and Fill (OBFF) 

**INTx Interrupt Messages.** Many devices are capable of using the PCI 2.3 Message Signaled Interrupt (MSI) method of delivering interrupts, but older devices may not support it. For these cases, PCIe defines a “virtual wire” alter‐ native in which devices simulate the assertion and deassertion of the PCI inter‐ rupt pins (INTA‐INTD) by sending Messages. The interrupting device sends the first Message to inform the upstream device that an interrupt has been asserted. Once the interrupt has been serviced, the interrupting device sends a second Message to communicate that the signal has been released. For more on this protocol, refer to the section called “Virtual INTx Signaling” on page 805 for details. 

**206** 

**Chapter 5: TLP Elements** 

_Table 5‐9: INTx Interrupt Signaling Message Coding_ 

|**INTx Message**|**Message**<br>**Code 7:0**|**Routing 2:0**|
|---|---|---|
|Assert_INTA|0010 0000b|100b<br>(Local ‐<br>Terminate at Rx)|
|Assert_INTB|0010 0001b||
|Assert_INTC|0010 0010b||

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-5-14"></a>
## 5.14 TLP Elements | TLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Assert_INTD|0010 0011b||
|Deassert_INTA|0010 0100b||
|Deassert_INTB|0010 0101b||
|Deassert_INTC|0010 0110b||
|Deassert_INTD|0010 0111b||



Rules regarding the use of INTx Messages: 

1. They have no data payload and so the Length field is reserved. 

2. They’re only issued by Upstream Ports. Checking this rule for received packets is optional but, if checked, violations will be handled as Malformed TLPs. 

3. They’re required to use the default traffic class TC0. Receivers must check for this and violations will be handled as Malformed TLPs. 

4. Components at both ends of the Link must track the current state of the four virtual interrupts. If the logical state of one interrupt changes at the Upstream Port, it must send the appropriate INTx message. 

5. INTx signaling is disabled when the Interrupt Disable bit of the Command Register is set = 1 (as would be the case for physical interrupt lines). 

6. If any virtual INTx signals are active when the Interrupt Disable bit is set in the device, the Upstream Port must send corresponding Deassert_INTx messages. 

7. Switches must track the state of the four INTx signals independently for each Downstream Port and combine the states for the Upstream Port. 

8. The Root Complex must track the state of the four INTx lines indepen‐ dently and convert them into system interrupts in an implementation‐spe‐ cific way. 

**207** 

## **PCI Ex ress Technolo p gy** 

9. They use the routing type “Local‐Terminate at Receiver” to allow a Switch to remap the designated interrupt pin when necessary (see “Mapping and Collapsing INTx Messages” on page 808). Consequently, the Requester ID in an INTx message may be assigned by the last transmitter. 

**Power Management Messages.** PCI Express is compatible with PCI power management, and adds hardware‐based Link power management as well. Messages are used to convey some of this information, but to learn how the overall PCIe power management protocol works, refer to Chapter 16, enti‐ tled ʺPower Management,ʺ on page 703. Table 5‐10 on page 208 summarizes the four power management message types. 

_Table 5‐10: Power Management Message Coding_ 

|**Power Management Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|PM_Active_State_Nak|0001 0100b|100b|
|PM_PME|0001 1000b|000b|
|PM_Turn_Off|0001 1001b|011b|
|PME_TO_Ack|0001 1011b|101b|



Power Management Message Rules: 

1. Power Management Messages don’t have a data payload, so the Length field is reserved. 

2. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

3. PM_Active_State_Nak is sent from a Downstream Port after it observes a request from the Link neighbor to change the Link power state to L1 but it has chosen not to do so (Local ‐ Terminate at Receiver routing). 

4. PM_PME is sent upstream by the component requesting a Power Manage‐ ment Event (Implicitly Routed to the Root Complex). 

5. PM_Turn_Off is sent downstream to all endpoints (Implicitly Broadcast from the Root Complex routing). 

6. PME_TO_Ack is sent upstream by endpoints. For switches with multiple Downstream Ports, this message won’t be forwarded upstream until all Downstream Ports have received it (Gather and Route to the Root Complex routing). 

**208** 

**Chapter 5: TLP Elements** 

**Error Messages.** Error Messages are sent upstream (Implicitly Routed to the Root Complex) by enabled components that detect errors. To assist software in knowing how to service the error, the Error Message identifies the requesting agent in the Requester ID field of the message header. Table 5‐11 on page 209 describes the three error message types. 

_Table 5‐11: Error Message Coding_ 

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|ERR_COR (Correctable)|0011 0000b|000b|
|ERR_NONFATAL<br>(Uncorrectable, Non‐fatal)|0011 0001b||
|ERR_FATAL<br>(Uncorrectable, Fatal)|0011 0011b||



Error Signaling Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, so the Length field is reserved. 

3. The Root Complex converts Error Messages into system‐specific events. 

**Locked Transaction Support.** The Unlock Message is used as part of the Locked transaction protocol defined for PCI and still available to Legacy Devices. The protocol begins with a Memory Read Locked Request. When that Request is seen by Ports along the path to the target device, they implement an atomic read‐modify‐write protocol by locking out other Requesters from using VC0 until the Unlock Message is received. This Message is sent to the target to release all the Ports in the path to it and finish the Locked Transaction sequence. Table 5‐12 on page 209 summarizes the coding for this message. 

_Table 5‐12: Unlock Message Coding_ 

|**Unlock Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Unlock|0000 0000b|011b|



**209** 

**PCI Ex ress Technolo p gy** 

Unlock Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

**Set Slot Power Limit Message.** This is sent from a Downstream Port to the device plugged into the slot. This power limit is stored in the endpoint in its Device Capabilities Register. Table 5‐13 summarizes the message coding. 

_Table 5‐13: Slot Power Limit Message Coding_ 

|**Slot Power Limit Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Set_Slot_Power_Limit|0101 0000b|100b|



Set_Slot_Power_Limit Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. The data payload is 1 DW and so the Length field is set to one. Only the lower 10 bits of the 32‐bit data payload are used for slot power scaling; the upper payload bits must be set to zero. 

3. This message is sent automatically anytime the Data Link Layer transitions to DL_Up status or if a configuration write to the Slot Capabilities Register occurs while the Data Link Layer is already reporting DL_Up status. 

4. If the card in the slot already consumes less power than the power limit specified, it’s allowed to ignore the Message. 

**Vendor‐Defined Message 0 and 1.** These are intended to allow expan‐ sion of the PCIe messaging capabilities either by the spec or by vendor‐specific extensions. The header for them is shown in Figure 5‐12 on page 211, and the codes are given in Figure 5‐14 on page 211. 

**210** 

**Chapter 5: TLP Elements** 

_Figure 5‐12: Vendor‐Defined Message Header_ 

**==> picture [368 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 1Fmt 1  0  r  r  rType R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 1 1 1 1 1 1 x<br>Byte 8 Target BDF if ID Routing used, Vendor ID<br>otherwise Reserved<br>Byte 12 For Vendor Definition<br>**----- End of picture text -----**<br>


_Table 5‐14: Vendor‐Defined Message Coding_ 

|**Vendor‐Defined Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Vendor Defined Message 0|0111 1110b|000b, 010b,<br>011b, 100b|
|Vendor Defined Message 1|0111 1111b||



Vendor‐Defined Message Rules: 

1. A data payload may or may not be included with either type. 

2. Messages are distinguished by the Vendor ID field. 

3. Attribute bits [2] and [1:0] are not reserved. 

4. If the Receiver doesn’t recognize the Message: 

   - Type 1 Messages are silently discarded 

   - Type 0 Messages are treated as an Unsupported Request error condi‐ tion 

**Ignored Messages.** Listing an entire category of Messages that are to be ignored sounds a little strange without the context for it. These were formerly Hot Plug Signaling messages that supported devices that had Hot Plug indica‐ tors and push buttons on the add‐in card itself rather than on the system board. This Message type was defined through spec rev 1.0a, but this option was no longer supported beginning with the 1.1 spec release, so the details are only included here for reference. As the name now suggests, Transmitters are 

**211** 

**PCI Ex ress Technolo p gy** 

strongly encouraged not to send these messages, and Receivers are strongly encouraged to ignore them if they are seen. If they’re still going to be used any‐ way, they must conform to the 1.0a spec details. 

_Table 5‐15: Hot Plug Message Coding_ 

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Attention_Indicator_On|0100 0001b|100b|
|Attention_Indicator_Blink|0100 0011b|100b|
|Attention_Indicator_Off|0100 0000b|100b|
|Power_Indicator_On|0100 0101b|100b|
|Power_Indicator_Blink|0100 0111b|100b|
|Power_Indicator_Off|0100 0100b|100b|
|Attention_Button_Pressed|0100 1000b|100b|



Hot Plug Message Rules: 

- They are driven by a Downstream Port to the card in the slot. 

- The Attention Button Message is driven upstream by a slot device. 

**Latency Tolerance Reporting Message.** LTR Messages are used to optionally report acceptable read/write service latencies for a device. To learn more about this power management technique, see the section called “LTR (Latency Tolerance Reporting)” on page 784. 

_Figure 5‐13: LTR Message Header_ 

**==> picture [346 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1 0 0 0 0<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>**----- End of picture text -----**<br>


**212** 

**Chapter 5: TLP Elements** 

_Table 5‐16: LTR Message Coding_ 

|**Latency Tolerance Reporting Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|LTR|0001 0000|100|



LTR Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

**Optimized Buffer Flush and Fill Messages.** OBFF Messages are used to report platform power status to Endpoints and facilitate more effective sys‐ tem power management. To learn more about this technique, see the discussion called “OBFF (Optimized Buffer Flush and Fill)” on page 776. 

_Figure 5‐14: OBFF Message Header_ 

**==> picture [346 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1  0 0 1 0<br>Byte 8 Reserved<br>OBFF<br>Byte 12 Reserved<br>Code<br>**----- End of picture text -----**<br>


_Table 5‐17: LTR Message Coding_ 

|**Optimized Buffer Flush/Fill Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|OBFF|0001 0010|100|



**213** 

## **PCI Ex ress Technolo p gy** 

## OBFF Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

3. The Requester ID must be set to the Transmitting Port’s ID. 

**214** 

## _**6**_ 

## _**Flow Control**_ 

## **The Previous Chapter** 

The previous chapter discusses the three major classes of packets: _Transaction Layer Packets_ (TLPs), _Data Link Layer Packets_ (DLLPs) and _Ordered Sets_ . This chapter describes the use, format, and definition of the variety of TLPs and the details of their related fields. DLLPs are described separately in Chapter 9, enti‐ tled ʺDLLP Elements,ʺ on page 307. 

## **This Chapter**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
