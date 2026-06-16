## **Extended Configuration Space** 

Refer to Figure 3‐3 on page 90 during this discussion. When PCIe was intro‐ duced, there was not enough room in the original 256‐byte configuration region to contain all the new capability structures needed. So the size of configuration space was expanded from 256 bytes per function to 4KB, called the Extended Configuration Space. The 960‐dword Extended Configuration area is only accessible using the Enhanced configuration mechanism and is therefore not visible to legacy PCI software. It contains additional optional Extended Capabil‐ ity registers for PCIe such as those listed in Figure 3‐3 (not a complete list). 

**89** 

**PCI Ex ress Technolo p gy** 

_Figure 3‐3: 4KB Configuration Space per PCI Express Function_ 

**==> picture [372 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
Config Header Byte Dword<br>3 2 1 0<br>PCI Config Hdr Offset 000h Device IDStatus CommandVendor ID 0001<br>16 DWs Class Code RevisionID 02<br>PCI-Compatible space is PCI Device-specific Offset 040h BIST HeaderType LatencyTimer Cache LineSize 03<br>accessible by legacy Base Address 0 04<br>& New Capability<br>PCI software or PCIe  register sets Base Address 1 05<br>Enhanced Configuration Base Address 2 06<br>Access Mechanism Base Address 3 07<br>48 DWs Base Address 4 08<br>Offset 100h Base Address 5 09<br>CardBus CIS Pointer 10<br>PCIe ExtendedConfiguration Expansion ROM Base AddressSubsystem ID SubsystemVendor ID 1112<br>Register Space Reserved CapabilitiesPointer 13<br>Capability registersOptional Extended Max_Lat Min_GntReservedInterruptPin InterruptLine 1415<br>implemented in this space,<br>such as: PCIe Capability Structure<br>PCIe Extended space is<br>must be implemented in<br>only accessible by PCIe<br>- Advanced Error Reporting this register space<br>Enhanced Configuration - Virtual Channels<br>Access Mechanism<br>- Device Serial Number<br>- Power Budgeting<br>960 DWs Offset FFFh<br>**----- End of picture text -----**<br>