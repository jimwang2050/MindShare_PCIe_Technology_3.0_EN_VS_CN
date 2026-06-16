## **System Examples** 

Figure 2‐10 on page 53 illustrates an example of a PCIe‐based system designed for a low‐cost application like a consumer desktop machine. A few PCIe Ports are implemented, along with a few add‐in cards slots, but the basic architecture doesn’t differ much from the old‐style PCI system. 

By contrast, the high‐end server system shown in Figure 2‐11 on page 54 shows other networking interfaces built into the system. In the early days of PCIe some thought was given to making it cable of operating as a network that could replace those older models. After all, if PCIe is basically a simplified version of other networking protocols, couldn’t it fill all the needs? For a variety of rea‐ sons, this concept never really achieved much momentum and PCIe‐based sys‐ tems still generally connect to external networks using other transports. 

**52** 

**Chapter 2: PCIe Architecture Overview** 

This also gives us an opportunity to revisit the question of what constitutes the Root Complex. In this example, the block labeled as “Intel Processor” contains a number of components, as is true of most modern CPU architectures. This one includes a x16 PCIe Port for access to graphics, and 2 DRAM channels, which means the memory controller and some routing logic has been integrated into the CPU package. Collectively, these resources are often called the “Uncore” logic to distinguish them from the several CPU cores and their associated logic in the package. Since we previously described the Root as being the interface between the CPU and the PCIe topology, that means that part of the Root must be inside the CPU package. As shown by the dashed line in Figure 2‐11 on page 54, the Root here consists of part of several packages. This will likely be the case for many future system designs. 

_Figure 2‐10: Low‐Cost PCIe System_ 

**==> picture [376 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe<br>Graphics<br>DDR3<br>GFX Intel Processor<br>DDR3<br>DMI (very similar to PCIe)<br>Serial ATA<br>HiDef Audio<br>HDD<br>USB 2.0 P55 PCH  Video<br>“Ibex Peak”<br>SPI<br>BIOS<br>Gb<br>Add-in Add-in Add-in<br>Ethernet<br>PCIe ports<br>**----- End of picture text -----**<br>

**53** 

**PCI Ex ress Technolo p gy** 

_Figure 2‐11: Server PCIe System_ 

**==> picture [369 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>
Intel Processor<br>PCIe DDR3<br>Uncore<br>GFX<br>DDR3<br>QPI<br>IOH Root Complex<br>10 Gb<br>LAN Switch Ethernet Switch Fibre<br>Endpoint Channel<br>Endpoint Endpoint<br>10 Gb PCI Express SAS/SATA<br>Add-In Switch Ethernet to-PCI<br>RAID<br>Endpoint Endpoint<br>Endpoint<br>PCI<br>Add-In EthernetGb IEEE Slots<br>1394<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>