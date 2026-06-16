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