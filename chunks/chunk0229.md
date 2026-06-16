34. Bridge J is discovered and a series of configuration writes are performed to set bridge its bus number registers as follows: 

   - Primary Bus Number Register = 8 

   - Secondary Bus Number Register = 9 

   - Subordinate Bus Number Register = 255 

35. All devices and their respective Functions on bus 9 are discovered and none of them are bridges, so the Subordinate Bus Number of bridges H and J are updated to 9. 

36. Bridge I is then discovered and a series of configuration writes are per‐ formed to set its bus number registers as follows: 

   - Primary Bus Number Register = 6 

   - Secondary Bus Number Register = 10 

   - Subordinate Bus Number Register = 255 

37. A single‐function Endpoint device is discovered at bus 10, device 0, func‐ tion 0. 

38. Since software has reached the bottom of this branch of the tree structure required for PCIe topologies, the Subordinate Bus Number registers for bridges B, F, and I are updated to 10, and so is the Host/PCI bridge’s Subor‐ dinate Bus Number register. 

The final values encoded into each bridge’s Primary, Secondary and Subordi‐ nate Bus Number fields can be found in Figure 3‐9 on page 104. 

**112** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐13: Single‐Root System_ 

**==> picture [322 x 443] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bridge<br>Bus 0<br>Bus 0 Bus 0<br>Virtual Virtual<br>A Dev 0 Dev 1 B<br>P2P Func 0 Func 0 P2P<br>Bus 1<br>Bus 5<br>Virtual<br>Virtual<br>P2P C P2P F<br>Bus 2 Bus 6<br>D VirtualP2P E VirtualP2P G VirtualP2P H VirtualP2P I VirtualP2P<br>Bus 3<br>Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 1 Function 0 Function 0 Function 0<br>Dev 0 Dev 0 Dev 0 Dev 0<br>Bus 8<br>Dev 0<br>Express Func 0<br>J PCI<br>Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>Dev 1 Dev 2 Dev 3<br>Func 0 Func 0 Func 0<br>**----- End of picture text -----**<br>


**113** 

**PCI Ex ress Technolo p gy** 

## **Multi-Root Enumeration Example** 

## **General** 

Consider the Multi‐Root System shown in Figure 3‐14 on page 116. In this sys‐ tem, each Root Complex: 

- Implements the Configuration Address Port and the Configuration Data Port at the same IO addresses (an x86‐based system). 

- Implements the Enhanced Configuration Mechanism. 

- Contains a Host/PCI bridge. 

- Implements the Secondary Bus Number and Subordinate Bus Number reg‐ isters at separate addresses known to the configuration software. 

In the illustration, each Root Complex is a chipset member and one of them is designated as the bridge to bus 0 (the primary Root Complex) while the other is designated as the bridge to bus 255 (secondary Root Complex). 

## **Multi-Root Enumeration Process** 

During enumeration of the left‐hand tree structure in Figure 3‐14 on page 116, the Host/PCI bridge in the secondary Root Complex ignores all configuration accesses because the targeted bus number is no greater than 9. Note that, although detected and numbered, Bus 8 has no device attached. Once that enu‐ meration process has been completed, the enumeration software takes the fol‐ lowing steps to enumerate the secondary Root Complex: 

1. The enumeration software changes the Secondary and Subordinate Bus Number values in the secondary Root Complex’s Host/PCI bridge to bus 64 in this example. (The values of 64 and 128 are commonly used as the start‐ ing bus number in multi‐root systems, but this is just a software convention. There are no PCI or PCIe rules requiring that configuration. There would be nothing wrong with starting the secondary Root Complex’s bus numbers at 10 in this example.) 

2. Enumeration software then starts searching on bus 64 and discovers the bridge attached to the downstream Root Port. 

3. A series of configuration writes are performed to set its bus number regis‐ ters as follows: 

   - Primary Bus Number Register = 64 

   - Secondary Bus Number Register = 65 

   - Subordinate Bus Number Register = 255 

**114** 

**Cha ter 3: Confi uration Overview p g** 

The bridge is now aware that the number of the bus directly attached to its downstream side is 65 (Secondary Bus Number = 65) and the number of the bus farthest downstream of it is 65 (Subordinate Bus Number = 65). 

4. Device 0 is discovered on Bus 65 that implements a only Function 0, and further searching reveals no other Devices are present on Bus 65, so the search process moves back up one Bus level. 

5. Enumeration continues on bus 64 and no additional devices are discovered, so the Host/PCI’s Subordinate Bus Number is updated to 65. 

6. This completes the enumeration process. 

**115** 

## **PCI Ex ress Technolo p gy** 

_Figure 3‐14: Multi‐Root System_ 

**==> picture [374 x 389] intentionally omitted <==**

**----- Start of picture text -----**<br>
Inter-Processor<br>Communications<br>Processor Processor<br>Root Complex Root Complex<br>Sec = 0 Host/PCI Sec = 64 Host/PCI<br>Sub = 9 Bridge Sub = 65 Bridge<br>Bus 0<br>Bus 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 9 P2P Device 0 Sec = 65Sub = 65 P2P<br>Bus 65<br>Bus 1 Bus 5<br>Function 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>Bus 2 P2P Bus 6 P2P Bus 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 Device 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 9<br>Function 0 Function 0 Function 0 Function 0<br>Bus 3 Bus 4 Bus 7 Bus 9<br>Device 0 Device 0 Device 0 Device 0<br>**----- End of picture text -----**<br>


## **Hot-Plug Considerations** 

In a hot‐plug environment, meaning one in which add‐in cards can be added or removed during runtime, the situation illustrated by Bus number 8 in Figure 3‐ 

**116** 

**Cha ter 3: Confi uration Overview p g** 

14 on page 116 can potentially cause trouble. A problem can occur if the system has been enumerated and is up and running and then a card is plugged into Bus 8 that has a bridge on it. The bridge would need to have bus numbers assigned for its Secondary and Subordinate Bus Numbers that are higher than the bus number on its primary bus and completely inclusive. The reason is that the bus numbers have to be within the Secondary and Subordinate Bus Numbers of the bridge upstream of the new card. 

One approach is to assign the Bus number(s) required for the bridge residing on Bus number 8 and increment the current Bus number 9 to a number than is one greater than the previous bus number, thereby making room for the new bus(s). Swizzling the bus numbers around during runtime can be done, but experi‐ enced people say it’s hard to get it to work very well. 

There is a simpler solution to this potential problem: simply leave a bus number gap whenever an unpopulated slot is found. For example, when Bus 8 is assigned but then an open slot is seen below it, give the next discovered bus a higher number, like 19 instead of 9, so as to leave room for these add‐in situa‐ tions to be resolved easily. Then, if a card with a bridge is added, the new bus number can be assigned as Bus 9 without causing any trouble. In most cases, leaving a bus number gap will not be an issue since the system can assign up to 256 bus numbers in total. 

## **MindShare Arbor: Debug/Validation/Analysis and Learning Software Tool** 

## **General** 

MindShare Arbor is a computer system debug, validation, analysis and learning tool that allows the user to read and write any memory, IO or configuration space address. The data from these address spaces can be viewed in a clean and informative style. 

The book authors made a decision to not include detailed descriptions of all configuration registers summarized in a signal chapter. Rather, registers are described through out the book in associated chapters where they are relevant. 

In lieu of a configuration register space description chapter in this book, Mind‐ Share Arbor is an excellent reference learning tool to quickly understand config‐ uration registers and structures implemented in PCI, PCI‐X and PCI Express 

**117** 

## **PCI Ex ress Technolo p gy** 

devices. All the register and field definitions are up‐to‐date with the latest ver‐ sion of the PCI Express spec. Several other types of structures (e.g. x86 MSRs, ACPI, USB, NVM Express) can also be viewed with MindShare Arbor (or will be coming soon). 

Visit www.mindshare.com/arbor to download a free trial version of MindShare Arbor. 

_Figure 3‐15: Partial Screenshot of MindShare Arbor_ 

**118** 

**Cha ter 3: Confi uration Overview p g** 

## **MindShare Arbor Feature List** 

- Description of all config registers included in the PCIe 3.0 spec 

- Scan config space for all PCI‐visible functions in system and a description of every one of these registers displayed in an easily readable format 

- Directly access any memory or IO address 

- Write to any config space location, memory address or IO address 

- View standard and non‐standard structures in a decoded format 

   - Decode info included for standard PCI, PCI‐X and PCI Express struc‐ tures 

   - Decode info included for some x86‐based structures and device‐specific registers 

- Create your own XML‐based decode files to drive Arborʹs display 

   - Create decode files for structures in config space, memory address space and IO space 

- Save system scans for viewing later or on other systems 

   - Saved system scans are XML‐based and open‐format 

- New features that are either already in or coming soon: 

   - Difference checking between scans 

   - Post‐processing scans for illegal or non‐optimal settings 

   - Scripting support for automation 

   - Decode for x86 structures (MSRs, paging, segmentation, interrupt tables, etc.) 

   - Decode for ACPI structures 

   - Decode for USB structures 

   - Decode for NVM Express structures 

**119** 

**PCI Ex ress Technolo p gy** 

**120** 

## _**4 Address Space & Transaction Routing**_ 

## **The Previous Chapter** 

The previous chapter provides an introduction to configuration in the PCI Express environment. This includes the space in which a Function’s configura‐ tion registers are implemented, how a Function is discovered, how configura‐ tion transactions are generated and routed, the difference between PCI‐ compatible configuration space and PCIe extended configuration space, and how software differentiates between an Endpoint and a Bridge. 

## **This Chapter** 

This chapter describes the purpose and methods of a function requesting address space (either memory address space or IO address space) through Base Address Registers (BARs) and how software must setup the Base/Limit regis‐ ters in all bridges to route TLPs from a source port to the correct destination port. The general concepts of TLP routing in PCI Express are also discussed, including address‐based routing, ID‐based routing and implicit routing. 

## **The Next Chapter** 

The next chapter describes Transaction Layer Packet (TLP) content in detail. We describe the use, format, and definition of the TLP packet types and the details of their related fields. 

## **I Need An Address** 

Almost all devices have internal registers or storage locations that software (and potentially other devices) need to be able to access. These internal locations may control the device’s behavior, report the status of the device, or may be a loca‐ tion to hold data for the device to process. Regardless of the purpose of the internal registers/storage, it is important to be able to access them from outside 

**121** 

**PCI Express Technology** 
