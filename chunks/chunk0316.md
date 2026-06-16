**==> picture [379 x 417] intentionally omitted <==**

**----- Start of picture text -----**<br>
AER Capability Structure<br>Extended Capability Header<br>00 01 00 01<br>Uncorrectable Error Status<br>00 00 00 00<br>Uncorrectable Error Mask<br>00 06 20 11<br>Uncorrectable Error Severity<br>Correctable Error Status00 00 20 00 CPU<br>00 00 20 00<br>Correctable Error Mask<br>00 00 00 06<br>Advanced Error Capability and Control00 00 00 00 Root Complex MemorySystem<br>Header Log - 1st DW00 00 00 00 P2P (DRAM)<br>Header Log - 2nd DW 0:28:0<br>00 00 00 00<br>Header Log - 3rd DW<br>00 00 00 00<br>Header Log - 4th DW<br>00 00 00 00<br>Root Error Command 2:0:0<br>00 00 00 06 Switch<br>Root Error Status P2P AER Capability Structure<br>08 00 00 7C<br>Error Source ID Extended Capability Header<br>05 00 00 00 14 01 00 01<br>3:0:0 3:5:0 Uncorrectable Error Status<br>00 04 10 00<br>Uncorrectable Error Mask<br>AER Capability Structure 00 00 00 00<br>Uncorrectable Error Severity<br>Extended Capability Header 00 06 20 11<br>14 01 00 01 Correctable Error Status<br>Uncorrectable Error Status 00 00 00 01<br>00 10 80 00 Correctable Error Mask<br>Uncorrectable Error Mask 4:0:0 5:0:0 00 00 20 00<br>00 00 00 00 Advanced Error Capability and Control<br>Uncorrectable Error Severity 00 00 00 12<br>00 16 20 11 PCIe PCIe Header Log - 1st DW<br>Correctable Error Status 60 00 80 80<br>00 00 00 40 Endpoint Endpoint Header Log - 2nd DW<br>Correctable Error Mask 00 00 04 FF<br>00 00 20 00 Header Log - 3rd DW<br>Advanced Error Capability and Control FB 80 10 00<br>00 00 00 0F Header Log - 4th DW<br>Header Log - 1st DW 00 00 00 01<br>00 00 00 80<br>Header Log - 2nd DW<br>0A 00 0C FF<br>Header Log - 3rd DW<br>FB 80 10 00<br>Header Log - 4th DW<br>00 00 00 00<br>P2P P2P<br>**----- End of picture text -----**<br>


**701** 

**PCI Ex ress Technolo p gy** 

6. Now that the error handler knows that the first uncorrectable error at 5:0:0 was a Malformed TLP, it can check the Header Log register to see the header of the packet that was malformed, since this is one of the errors where a header is recorded. In reading the Header Log register it finds these four doublewords: 

   - 6000_8080h ‐ 1st DW 

   - 0000_04FFh ‐ 2nd DW 

   - FB80_1000h ‐ 3rd DW 

   - 0000_0001h ‐ 4th DW 

7. The evaluation of those 4 DWs identifies the malformed packet as: Memory Write, 4DW header, TC=0, TD=1, EP=0, Attr=0, AT=0, Length=80h (128 DWs or 512 bytes), Requester ID=0:0:0, Tag=4, Byte Enables=FFh, Address=1_FB80_1000h. The header of the packet all looks correct and every field uses valid encod‐ ings, so software must dig a little deeper to discover why this was treated as a Malformed TLP. In this example, let’s assume that after further inspection of config space on 5:0:0, software discovers that the Max Payload Size enabled for this Function is 256 bytes, but this packet contained 512 bytes. This is a condition that will be treated as a Malformed TLP by the target device, in this case 5:0:0. 

If you would like verify your knowledge of this error investigation process, go ahead and evaluate what the first uncorrectable error detected on 4:0:0 was. 

If you’re feeling adventurous and would like to check out this type of info on a real system, say your desktop or laptop, you can do so by downloading the MindShare Arbor software (www.mindshare.com/arbor). You can run this on an x86‐based machine and it will scan your system and display every visible PCI‐compatible device with its configuration space decoded for easy interpreta‐ tion. 

**702** 

## _**16 Power Management**_ 

## **The Previous Chapter** 

The previous chapter discusses error types that occur in a PCIe Port or Link, how they are detected, reported, and options for handling them. Since PCIe is designed to be backward compatible with PCI error reporting, a review of the PCI approach to error handling is included as background information. Then we focus on PCIe error handling of correctable, non‐fatal and fatal errors. 

## **This Chapter** 

This chapter provides an overall context for the discussion of system power management and a detailed description of PCIe power management, which is compatible with the _PCI Bus PM Interface Spec_ and the _Advanced Configuration and Power Interface_ (ACPI). PCIe defines extensions to the PCI‐PM spec that focus primarily on Link Power and event management. An overview of the OnNow Initiative, ACPI, and the involvement of the Windows OS is also pro‐ vided. 

## **The Next Chapter** 

The next chapter details the different ways that PCIe Functions can generate interrupts. The old PCI model used pins for this, but side‐band signals are undesirable in a serial model so support for the in‐band MSI (Message‐Signaled Interrupts) mechanism was made mandatory. The PCI INTx# pin operation can still be emulated in support of a legacy system using PCIe INTx messages. Both the PCI legacy INTx# method and the newer versions of MSI/MSI‐X are described. 

**703** 

**PCI Ex ress Technolo p gy** 

## **Introduction** 

PCI Express power management (PM) defines four major areas of support: 

- **PCI‐Compatible PM** . PCIe power management is hardware and software compatible with the PCI‐PM and ACPI specs. This support requires that all Functions include the PCI Power Management Capability registers, allow‐ ing software to transition a Function between PM states under software control through the use of Configuration requests. This was modified in the 2.1 spec revision with the addition of Dynamic Power Allocation (DPA), another set of registers that added several substates to the D0 power state to give software a finer‐grained PM mechanism. 

- **Native PCIe Extensions** . These define autonomous, hardware‐based Active State Power Management (ASPM) for the Link, as well as mechanisms for waking the system, a Message transaction to report Power Management Events (PME), and a method for calculating and reporting the low‐power‐to‐active‐state latency. 

- **Bandwidth Management.** The 2.1 spec revision added the ability for hard‐ ware to automatically change either the Link width or Link data rate or both to improve power consumption. This allows high performance when needed and keeps power usage low when lower performance is acceptable. Even though Bandwidth Management is considered a Power Management topic, we describe this capability in the section “Dynamic Bandwidth Changes” on page 618 in the “Link Initialization & Training” chapter because it involves the LTSSM. 

- **Event Timing Optimization.** Peripheral devices that initiate bus master events or interrupts without regard to the system power state cause other system components to stay in high power states to service them, resulting in higher power consumption than would be necessary. This shortcoming was corrected in the 2.1 spec by adding two new mechanisms: Optimized Buffer Flush and Fill (OBFF), which lets the system inform peripherals about the current system power state, and Latency Tolerance Reporting (LTR), which allows devices to report the service delay they can tolerate at the moment. 

This chapter is segmented into several major sections: 

1. The first part is a primer on power management in general and covers the role of system software in controlling power management features. This discussion only considers the Windows Operating System perspective since it’s the most common one for PCs, and other OSs are not described. 

**704** 

**Chapter 16: Power Management** 

2. The second section, “Function Power Management” on page 713, discusses the method for putting Functions into their low‐power device states using the PCI‐PM capability registers. Note that some of the register definitions are modified or unused by PCIe Functions. 

3. “Active State Power Management (ASPM)” on page 735 describes the hard‐ ware‐based autonomous Link power management. Software determines which level of ASPM to enable for the environment, possibly by reading the recovery latency values that will be incurred for that Function, but after that the timing of the power transitions is controlled by hardware. Software doesn’t control the transitions and is unable to see which power state the Link is in. 

4. “Software Initiated Link Power Management” on page 760 discusses the Link power management that is forced when software changes the power state of a device. 

5. “Link Wake Protocol and PME Generation” on page 768 describes how Devices may request that software return them to the active state so they can service an event. When power has been removed from a Device, auxil‐ iary power must be present if it is to monitor events and signal a Wakeup to the system to get power restored and reactivate the Link. 

6. Finally, event‐timing features are described, including OBFF and LTR. 

## **Power Management Primer** 

The _PCI Bus PM Interface spec_ describes the power management registers required for PCIe. These permit the OS to manage the power environment of a Function directly. Rather than dive into a detailed description, let’s start by describing where this capability fits in the overall context of the system. 

## **Basics of PCI PM** 

This section provides an overview of how a Windows OS interacts with other major software and hardware elements to manage the power usage of individ‐ ual devices and the system as a whole. Table 16‐1 on page 706 introduces the major elements involved in this process and provides a very basic description of how they relate to each other. It should be noted that neither the PCI Power Management spec nor the ACPI spec dictate the PM policies that the OS uses. They do, however, define the registers (and some data structures) that are used to control the power usage of a Function. 

**705** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐1: Major Software/Hardware Elements Involved In PC PM_ 

|**Element**|**Responsibility**|
|---|---|
|OS|Directs**overall system power management**by sending requests to the<br>ACPI Driver, device driver, and the PCI Express Bus Driver. Applica‐<br>tions that are power conservation‐aware interact with the OS to accom‐<br>plish device power management.|
|ACPI Driver|Manages configuration, power management, and thermal control of<br>embedded system devices that don’t adhere to an industry‐standard<br>spec. Examples of this include chipset‐specific registers, system<br>board‐specific registers to control power planes, etc. The PM registers<br>within PCIe Functions (embedded or otherwise) are defined by the PCI<br>PM spec and are therefore not managed by the ACPI driver, but rather<br>by the PCI Express Bus Driver (see entry in this table).|