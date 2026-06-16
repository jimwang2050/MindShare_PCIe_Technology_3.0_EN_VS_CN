# 📘 第 15 章　错误检测与处理 (Chapter 15. Error Detection and Handling)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0316.md` ... `chunks/chunk0322.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Error Detection and Handling](#-本章目录-table-of-contents)

<a id="sec-15-1"></a>
## 15.1 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-15-2"></a>
## 15.2 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Device Driver|The**Class driver**can work with any device that falls within the Class of<br>devices that it was written to control. The fact that it’s not written for a<br>specific vendor means that it doesn’t have bit‐level knowledge of the<br>device’s interface. When it needs to issue a command to or check the sta‐<br>tus of the device, it issues a request to the**Miniport**driver supplied by<br>the vendor of the specific device.<br>The device driver also doesn’t understand device characteristics that are<br>peculiar to a specific bus implementation of that device type. As an<br>example, it won’t understand a PCIe Function’s configuration register<br>set. The**PCI Express Bus Driver**is the one to communicate with those<br>registers.<br>When it receives requests from the OS to control the power state of a<br>PCIe device, it passes the request to the PCI Express Bus Driver.<br>• When a request to power down its device is received from the OS, the<br>device driver saves the contents of its associated Function’s<br>device‐specific registers (in other words, a context save) and then<br>passes the request to the PCI Express Bus Driver to change the power<br>state of the device.<br>• Conversely, when a request to re‐power the device is received, the<br>device driver passes the request to the PCI Express Bus Driver to<br>change the power state of the device. After the PCI Express Bus Driver<br>has re‐powered the device, the device driver then restores the context<br>to the Function’s device‐specific registers.|
|Miniport Driver|**Supplied by the vendor of a device**, it receives requests from the Class<br>driver and converts them into the proper series of accesses to the<br>device’s register set.|



**706** 

**Chapter 16: Power Management** 

_Table 16‐1: Major Software/Hardware Elements Involved In PC PM (Continued)_ 

|**Element**|**Responsibility**|
|---|---|
|PCI Express Bus<br>Driver|This driver is**generic to all PCI Express‐compliant devices**. It**manages**<br>**their power states and configuration registers**, but does not have<br>knowledge of a Function’s device‐specific register set (that knowledge is<br>possessed by the Miniport Driver that the device driver uses to commu‐<br>nicate with the device’s register set). It receives requests from the device<br>driver to change the state of the device’s power management logic. For<br>example:<br>• When a request to power down the device is received, this driver is<br>responsible for saving the context of the Function’s PCI Express con‐<br>figuration registers. It then disables the ability of the device to act as a<br>Requester or respond as a target and writes to the Function’s PM regis‐<br>ters to change its state.<br>• Conversely, when the device must be re‐powered, the PCI Express<br>Bus Driver writes to the PCI Express Function’s PM registers to change<br>its state and then restores the Function’s configuration registers to<br>their original state.|
|PCI Express PM regis‐<br>ters within each Func‐<br>tion’s configuration<br>space.|**The location, format and usage of these registers is defined by the**<br>**PCIe spec**. The PCI Express Bus Driver understands this spec and there‐<br>fore is the entity responsible for accessing a Function’s PM registers<br>when requested to do so by the Function’s device driver.|
|System Board power<br>plane and bus clock<br>control logic|The implementation and control of this logic is typically system board<br>design‐specific and is therefore**controlled by the ACPI Driver**(under<br>OS direction).|



## **ACPI Spec Defines Overall PM** 

The ACPI (Advanced Configuration and Power Interface) spec was first written several years ago as a joint effort by several companies to provide industry stan‐ dards for OSPM (OS‐level Power Management) in compute platforms. Power management at that time was being handled in proprietary ways on different platforms and that made it difficult for vendors to coordinate their efforts. In addition, platform‐specific code wasn’t always fully compatible with OS opera‐ tions or aware of all the system conditions or policy considerations. ACPI helped in these areas by defining system power states, hardware registers and software interactions to accomplish OS‐based power management. A detailed description of ACPI is beyond the scope of this book, but an introduction to the concepts and terminology will be helpful. 

**707** 

**PCI Ex ress Technolo p gy** 

## **System PM States** 

Table 16‐2 on page 708 defines the possible states of the overall system with ref‐ erence to power consumption. The “Working”, “Sleep”, and “Soft Off” states are defined in the OnNow Design Initiative documents. 

_Table 16‐2: System PM States as Defined by the OnNow Design Initiative_ 

|**Power**<br>**State**|**Description**|
|---|---|
|Working<br>(G0/S0)|The system is fully operational.|
|Sleeping<br>(G1)|The system appears to be off and power consumption has been<br>reduced. The amount of time it takes to return to the “Working” state<br>is inversely proportional to the selected level of power conservation.<br>• S1 ‐ caches flushed, CPU halted<br>• S2 ‐ same as S1 except that now CPU is powered off. Not commonly<br>used because it’s not much better than S3.<br>• S3 ‐ (also called “Suspend to RAM” or “Standby”) This is the same<br>as S2 except that the system context is saved in memory and more<br>of the system is shut down. When the system wakes up the CPU<br>begins the full boot process but finds flags set in the CMOS mem‐<br>ory that direct it to reload the context from RAM instead, and thus<br>program execution can be resumed very quickly.<br>• S4 ‐ (also called “Suspend to Disk” or “Hibernate”) Similar to S3,<br>except that now the system copies the system context to disk, and<br>then removes power from the system, including main memory.<br>This gives better power savings but the restart time will be longer<br>because the context must be restored from the disk before resuming<br>program execution.|
|Soft Off<br>(G2/S5)|The system appears to be off and power consumption is minimal. It<br>requires a full reboot to return to the “Working” state because the<br>contents of memory have been lost, but there is still some power avail‐<br>able to do the wakeup, such as by pressing the “Power” button on the<br>system.|
|Mechanical<br>Off (G3)|The system has been disconnected from all power sources and no<br>power is available.|



**708** 

**Chapter 16: Power Management** 

## **Device PM States** 

ACPI also defines the PM states at the device level, which are listed in Table 16‐3 on page 709. Table 16‐3 on page 709 presents the same information in a slightly different form. The registers that support these device states must be implemented for PCIe devices. 

_Table 16‐3: OnNow Definition of Device‐Level PM States_ 

|**State**|**Description**|
|---|---|
|D0|**Mandatory**. Device is fully operational and uses full power from the sys‐<br>tem. The 2.1 spec revision added another set of registers to support 32<br>substates under D0 referred to as Dynamic Power Allocation registers.|
|D1|**Optional**. Low‐power state in which device context may or may not be<br>lost. No definition for this state is given, but it would represent a lower<br>power state than D0 and higher than D2|
|D2|**Optional**. Presumably a lower power state than D1 that attains greater<br>power savings, but would incur a longer recovery delay and may cause<br>Device to lose some context.|
|D3|**Mandatory**. Device is prepared for loss of power and context may be lost<br>whether the power actually goes off or not. Recovery time will be longer<br>than for D2, but power can be removed from the device gracefully in this<br>state.|



## **Definition of Device Context** 

**General.** During normal operation, the operational state of a Device is con‐ stantly changing. A device driver may write or read its registers, or a local processor on the Device may execute code that affects its interaction with the system. The state of the device at a given instant in time includes: 

- The contents of its configuration registers. 

- The state of its local memory and IO registers. 

- If it contains a processor, then the current program pointer and contents of its other registers would be included. 

This state information is referred to as the _device context_ . Some or all of this may be lost if the Device PM state is changed to a more aggressive level. If the context information is not maintained, the Device won’t operate cor‐ rectly when it returns to the D0 (fully operational) state. 

**709** 

**PCI Ex ress Technolo p gy** 

**PME Context.** If the OS enables a modem to wake the system for an incoming call and then powers down the system, the Device wake‐up con‐ text will need to be retained locally during that time. The chipset retains enough power to allow it to monitor for these events. To support this fea‐ ture, a PCIe modem must implement configuration registers including: 

- PME Message capability. 

- PME enable/disable control bit. 

- PME status bit indicating whether the device has sent a PME message. 

- ‐ One or more device‐specific control bits that selectively enable or dis‐ able various device‐specific events that can cause the device to send a PME message. 

- Corresponding device‐specific status bits that indicate why the device issued a PME message. 

## **Device-Class-Specific PM Specs** 

**Default Device Class Spec.** As mentioned earlier, ACPI gives four pos‐ sible device power states (D0 ‐ through ‐ D3). It also defines the minimum PM states that all device types must implement, as listed in Table 16‐4 on page 710. 

_Table 16‐4: Default Device Class PM States_ 

|**State**|**Description**|
|---|---|
|D0|Device is on, is running at full power, and is fully operational.|
|D1|This optional state is only defined as being lower power than D0. It is not<br>commonly used.|
|D2|This optional state is only defined as being lower power than D1. It is not<br>commonly used.|
|D3|Device consumes the minimum possible power and main power may be<br>turned off. The only requirement is that, while power is still on, the device<br>must be able to service a configuration command to re‐enter D0. Power<br>can be removed from the device in this state, and the device will experi‐<br>ence a hardware reset when power is restored.|



**710** 

**Chapter 16: Power Management** 

**Device Class‐Specific PM Specs.** Above and beyond the power states mandated by the _Default Device Class Spec_ , certain device classes may require the intermediate power states (D1 and/or D2) or exhibit certain common characteristics in a particular power state. 

The rules associated with a particular device class are found in the _Device Class Power Management Specs_ available on Microsoft’s Hardware Develop‐ ers’ web site. For example, Device Class Power Management Specs exist for the following classes: 

- Audio 

- Communications 

- Display 

- Input 

- Network 

- PC Card 

- Storage 

## **Power Management Policy Owner** 

A Device’s PM policy owner is defined as the software module that makes deci‐ sions regarding the PM state of a device. In a Windows environment, the policy owner is the class‐specific driver associated with devices of that class. 

## **PCI Express Power Management vs. ACPI** 

## **PCI Express Bus Driver Accesses PM Registers** 

As indicated in Table 16‐1 on page 706 and Figure 16‐1 on page 712, the PCI Express Bus Driver understands the location, format and usage of the PM con‐ figuration registers. It’s called when the OS needs to change the power state of a PCIe device or determine its status and capabilities. Other examples include: 

- The IEEE 1394 Bus Driver, which understands how to use the PM registers defined in the 1394 Power Management spec. 

- The USB Bus Driver, which understands how to use the PM registers defined in the USB Power Management spec. 

**711** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-15-3"></a>
## 15.3 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **ACPI Driver Controls Non-Standard Embedded Devices** 

There are devices embedded on the system board whose register sets do not adhere to any particular industry standard spec. At boot time, the BIOS reports these devices to the OS via the **ACPI tables** , also referred to as the **namespace** . When the OS needs to communicate with any of these devices, it calls the ACPI Driver, which executes a handler called a **Control Method** associated with the device. The handler is also found in the ACPI tables and is written by the plat‐ form designer using a special interpretive language called ACPI Source Lan‐ guage, or **ASL** . The ASL code is then compiled into ACPI Machine Language, or **AML** . Note that AML is not a processor‐specific machine language. It’s a token‐ ized (i.e., compressed) version of the ASL source code. An ACPI Driver incorpo‐ rates an AML token interpreter that allows it to “execute” a Control Method. 

_Figure 16‐1: Relationship of OS, Device Drivers, Bus Driver, PCI Express Registers, and ACPI_ 

**==> picture [348 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
Microsoft<br>OS<br>Interface defined  Interface defined<br>by Microsoft by Microsoft<br>Windows ACPI Written by Microsoft<br>Device Driver Driver to ACPI spec<br>Interface defined<br>by Microsoft<br>Written by Microsoft PCIe Bus AML Control Written by system<br>to OS, PCIe, and PCI  Driver Method board designer to ACPI<br>PM specs and chip-specific specs<br>Non-standard<br>PCIe Function’s  PCIe Function’s  Embedded Register set defined<br>Configuration PM Registers System Board by chip designer<br>Registers Device<br>Register set defined Register set defined<br>by PCIe spec by PCI PM spec and<br>extensions for PCIe<br>**----- End of picture text -----**<br>


**712** 

**Chapter 16: Power Management** 

## **Function Power Management** 

PCI Express Functions are required to support power management, and several registers and related bit fields must be implemented as discussed below. 

## **The PM Capability Register Set** 

The PCI‐PM spec defines the Power Management Capability configuration reg‐ isters. These registers were optional for PCI, but required for PCIe, and are located in the PCI‐compatible configuration space with a Capability ID of 01h. Software can perform the following sequence to locate these registers: 

1. Bit 4 of the Function’s **Configuration Status register** should be set, indicat‐ ing that the Capabilities Pointer in the first byte of dword 13d of the Func‐ tion’s configuration Header is valid. Reading the **Capabilities Pointer register** gives the offset to the first of the Function’s linked list of capability registers. 

2. If the least significant byte of the dword at that offset contains **Capability ID 01h (** see Figure 16‐2 on page 713), this is the PM register set. The byte immediately following the Capability ID byte is the _Pointer to Next Capabil‐ ity_ field that gives the offset in configuration space of the next Capability (if there is one). A non‐zero value is a valid pointer, while a value of 00h indi‐ cates the end of the linked list. A description of all the PM registers can be found in “Detailed Description of PCI‐PM Registers” on page 724. 

_Figure 16‐2: PCI Power Management Capability Register Set_ 

**==> picture [367 x 62] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 8 7 0<br>Power Management Capabilities Pointer to Capability ID<br>(PMC) Next Capability 01h 1st Dword<br>Bridge Support<br>Data Register Extensions Control/Status Register 2nd Dword<br>(PMCSR_BSE) (PMCSR)<br>**----- End of picture text -----**<br>


## **Device PM States** 

Each PCI Express Function must support the full‐on D0 state and the full‐off D3 state, while D1 and D2 are optional. The sections that follow describe the possi‐ ble PM states. 

**713** 

**PCI Ex ress Technolo p gy** 

## **D0 State—Full On** 

**Mandatory.** In this state, no power conservation is in effect and the device is fully operational. All PCIe Functions must support the D0 state and there are technically two substates: D0 Uninitialized and D0 Active. ASPM hard‐ ware control can change the Link power while the Device is in this state. Table 16‐5 on page 714 summarizes the PM policies in the D0 state. 

**D0 Uninitialized.** A Function enters D0 Uninitialized after a Fundamen‐ tal Reset or, in some cases, when software transitions it from D3hot to D0. Usually, the registers are returned to their default state. In this state, the Function exhibits the following characteristics: 

- It only responds to configuration transactions. 

- Its Command register enable bits are all returned to their default states, meaning it cannot initiate transactions or act as the target of memory or IO transactions. 

**D0 Active.** Once the Function has been configured and enabled by soft‐ ware, it is in the D0 Active state and is fully operational. 

_Table 16‐5: D0 Power Management Policies_ 

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers or**<br>**State that must**<br>**be valid**|**Power**|**Actions**<br>**permitted to**<br>**Function**|**Actions**<br>**permitted by**<br>**Function**|
|---|---|---|---|---|---|
|L0|D0 un‐initialized|PME context **|< 10W|PCI Express<br>config transac‐<br>tions.|None|
|L0<br>L0s (required)*<br>L1 (optional)*|D0 active|all|full|Any PCI<br>Express trans‐<br>action.|Any transac‐<br>tion, interrupt,<br>or PME. **|
|L2/L3|D0 active|N/A***||||



* Active State Power Management 

- ** If PME supported in this state. 

- *** This combination of Bus/Function PM states not allowed. 

## **Dynamic Power Allocation (DPA)** 

**Optional** . The 2.1 revision of the base spec added another optional capability that defines 32 more substates for D0 and describes their characteristics. This was intended to facilitate negotiation regarding power management between a 

**714** 

**Chapter 16: Power Management** 

device driver, OS, and an executing application, partly because some Functions don’t have device drivers that handle PM well. One advantage of this model is that the Device technically still remains in the D0 state and may therefore be able to continue operating in a reduced capacity instead of going offline as would be caused by a change to the D1 or lower state. 

DPA registers only apply when the Device power state is in D0 and aren’t appli‐ cable in states D1‐D3. Up to 32 substates can be defined, and they must be con‐ tiguously numbered from zero to the maximum value. Substate 0 is the initial default value and represents the maximum power the Function is capable of consuming. Software is not required to transition between substates in sequen‐ tial order or even wait until a previous transition is completed before requesting another change in the substate. Consequently, when a Function has completed a substate change it must check the configured substate and, if they don’t match, it must begin changing to the configured value. The registers to support DPA, illustrated in Figure 16‐3 on page 715, are found in the Enhanced configuration space. 

_Figure 16‐3: Dynamic Power Allocation Registers_ 

**==> picture [265 x 155] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>DPA Capability Register 004h<br>DPA Latency Indicator Register 008h<br>DPA Control Register DPA Status Register 00Ch<br>010h<br>DPA Power Allocation Array<br>(Sized by number of substates)<br>Up to<br>02Ch<br>**----- End of picture text -----**<br>


The DPA capability register, shown in Figure 16‐4 on page 716, contains several interesting values associated with the substates. The Substate_Max number indicates how many substates are described, and the numbers must increment contiguously from zero to that value. Two Transition Latency Values are given and each substate will be associated with one or the other by the Latency Indica‐ tor register. which contains one bit for each possible substate; if that bit is set Transition Latency Value 1 is used, otherwise Value 0 is used. The latency value gives the maximum time required to transition into that substate from any other 

**715** 

**PCI Ex ress Technolo p gy** 

substate. The latencies are multiplied by the Transition Latency Units to give the time in milliseconds. Similarly, the Power Allocation Scale value gives the multi‐ plier for the power used in each substate, expressed in watts. For each defined substate, a 32‐bit field in the DPA Power Allocation Array describes the power used for that state. The first one of these is located at offset 010h, and the rest are implemented in subsequent dwords. 

_Figure 16‐4: DPA Capability Register_ 

**==> picture [311 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24  23 16  15 14  13  12  11  10   9 8   7        5   4                0<br>Xlcy1 Xlcy0 RsvdZ PAS RsvdZ RsvdZ Substate_Max<br>Transition Latency Value 0 All fields not reserved<br>are read-only<br>Transition Latency Value 1<br>Power Allocation Scale (PAS)<br>Transition Latency Unit (Tlunit)<br>**----- End of picture text -----**<br>


The low‐order five bits of the DPA Control register are written by software to set a new substate, and the current substate can be read from the Status register, as shown in Figure 16‐5 on page 716. Notice that bit 8 of the Status register indi‐ cates whether the use of DPA substates has been enabled but it’s labeled as RW1C (Read, Write 1 to Clear), meaning software can clear this bit but can’t set it. DPA is enabled by default after a reset, and software would need to disable it by writing a one to this bit if it did not intend to use DPA. 

_Figure 16‐5: DPA Status Register_ 

**==> picture [298 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9   8  7          5   4     0<br>RsvdZ RsvdZ<br>Substate Control Enabled (RW1C)<br>Substate status (RO)<br>**----- End of picture text -----**<br>


## **D1 State—Light Sleep** 

**Optional** . Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of 

**716** 

**Chapter 16: Power Management** 

the PCI Express Capability block; when the bit is cleared to zero, it’s safe to pro‐ ceed. In this light power conservation state the Function won’t initiate Requests except PME Messages, if enabled. Other characteristics of the D1 state include: 

- Link is forced to the L1 power state when the Device goes into the D1 state. 

- Configuration and Message Requests are accepted in this state, but all other Requests must be handled as Unsupported Requests and all completions may optionally be handled as Unexpected Completions. 

- If an error is caused by an incoming Request and reporting it is enabled, an Error Message may be sent while in this state. If a different type of error occurs (such as a Completion timeout), the message won’t be sent until the Device is returned to the D0 state. 

- The Function may reactivate the Link and send a PME message, if sup‐ ported and enabled in this state, to notify software that the Function has experienced an event requiring that power be restored. 

- The Function may or may not lose its context in this state. If it does and the device supports PME, it must at least maintain its PME context (see “PME Context” on page 710) while in this state. 

- The Function must be returned to the D0 Active PM state in order to be fully operational. 

Table 16‐6 lists the PM policies while in the D1 state. 

_Table 16‐6: D1 Power Management Policies_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-15-4"></a>
## 15.4 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers or**<br>**State that**<br>**must be valid**|**Power**|**Actions permitted to**<br>**Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D1|Device<br>class‐specific<br>registers<br>and PME<br>context.*|D0<br>unini‐<br>tial‐<br>ized|Config Requests and<br>Messages. Link transi‐<br>tions back to L0 to ser‐<br>vice the request.|PME Messages.**<br>Though not typi‐<br>cally permitted,<br>they would require<br>the Link to transi‐<br>tion back to L0.|
|L2‐L3||NA *||||



* This combination of Bus/Function PM states not allowed. 

- ** If PME supported in this state. 

## **D2 State—Deep Sleep** 

**Optional** . Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of 

**717** 

**PCI Ex ress Technolo p gy** 

the PCI Express Capability block; when the bit is cleared to zero, it’s safe to pro‐ ceed. This power state provides deeper power conservation than D1 but less than the D3hot state. As in D1, the Function won’t initiate Requests (except a PME Message) or act as the target of Requests other than configuration. Soft‐ ware must still be able to access the Function’s configuration registers in this state. 

Other characteristics of the D2 state include: 

- Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of the PCIe Capability block. It could happen that the Completions will never be returned and, in that case, software should wait long enough to ensure they never will be returned. 

- Link state must transition to L1 when the Device transitions to the D2 state. 

- • Configuration and Message Requests are accepted in this state, but all other Requests must be handled as Unsupported Requests and all completions may optionally be handled as Unexpected Completions. 

- If an error is caused by an incoming Request and reporting it is enabled, an Error Message may be sent while in this state. If a different type of error occurs (such as a Completion timeout), the message won’t be sent until the Device is returned to the D0 state. 

- Function may send a PME message, if supported and enabled, to notify software that it needs power restored to handle an event. 

- The Function may or may not lose its context in this state. If it does and the device supports PME messages, it must at least maintain its PME context for this purpose. 

- The Function must return to the D0 Active state to be fully operational. 

Table 16‐7 on page 719 illustrates the PM policies while in the D2 state. 

**718** 

**Chapter 16: Power Management** 

_Table 16‐7: D2 Power Management Policies_ 

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must be**<br>**valid**|**Power**|**Actions permitted**<br>**to Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D2|Device<br>class‐specific<br>registers<br>and PME con‐<br>text. *|next higher<br>supported PM<br>state orD0<br>uninitialized.|Config Requests<br>and transactions<br>permitted by<br>device class (typi‐<br>cally none).<br>This requires the<br>Link to transition<br>back to L0|PME Messages.*<br>Though not typi‐<br>cally permitted,<br>they would require<br>the Link to transi‐<br>tion back to L0.|
|L2/L3||N/A**||||



- If PME supported in this state. 

- ** This combination of Bus/Function PM states not allowed. 

## **D3—Full Off** 

**Mandatory** . All Functions must support the D3 state. This is the deepest state and power conservation is maximized. When software writes this power state to the Device, it goes to the **D3hot** state, meaning power is still applied. Remov‐ ing power (Vcc) from the Device puts it into the **D3cold** state and the Link into L2, if a secondary power source (Vaux) is available, or L3 if it’s not. 

**D3Hot State. (Mandatory** .) Software puts a Function into D3hot by writing the appropriate value into the PowerState field of its Power Mgt Control and Status Register (PMCSR). In this state, the Function can only initiate PME or PME_TO_ACK Messages, and can only respond to configuration Requests or the PME_Turn_Off Message. Software must be able to access the Function’s configuration registers while the device is in the D3hot state, if only to be able to change the state back to D0. Other characteristics of D3hot include: 

- Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of the PCIe Capability block. It could happen that the Completions will never be returned and, in that case, software should wait long enough to ensure they never will be returned. 

- The Link is forced to the L1 state when the Function changes to D3hot. 

**719** 

## **PCI Ex ress Technolo p gy** 

- The Function is allowed to send a PME message to notify PM software of its need to be returned to the fully active state (assuming it supports genera‐ tion of PM events in the D3hot state and has been enabled to do so). 

- Function context may be lost when going to this state and if the power is turned off the spec assumes all context will be lost. On the other hand, if the power never goes off before software initiates a return to D0 the context could be maintained. In earlier spec versions that wasn’t possible; changing from D3hot to D0 involved a soft reset and all the registers were re‐initial‐ ized. However, the 1.2 revision of that spec added a new capability bit called “No Soft Reset” to indicate that the Function would not do a soft reset in that case. To be able to generate PME messages in the D3hot state, a Device must maintain its PME context (see “PME Context” on page 710). 

The Function exits from the D3hot state under two circumstances: 

- If Vcc is removed from the device, it transitions from D3hot to D3cold. 

- Software can write to the PowerState field of the Function’s PMCSR register to change its PM state to D0. When programmed to exit D3hot and return to D0, the Function returns to the D0 Uninitialized PM state. A reset may or may not be required. Table 16‐8 on page 721 lists the PM policies while in the D3hot state. 

**720** 

**Chapter 16: Power Management** 

_Table 16‐8: D3hot Power Management Policies_ 

|**Bus**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must**<br>**be valid**|**Power**|**Actions permitted**<br>**to Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D3hot|PME con‐<br>text. **|next higher<br>supported PM<br>state orD0<br>uninitialized.|PCI Express config<br>transactions<br>& PME_Turn_Off<br>broadcast<br>message***<br>(These can only<br>occur after the Link<br>transitions back to<br>its L0 state.|PME message**<br>PME_TO_ACK<br>message***<br>PM_Enter_L23<br>DLLP***<br>(These can occur<br>only after the Link<br>returns to L0)|
|L2/L3<br>Ready||L2/L3 Ready entered following the PME_Turn_Off handshake sequence, which<br>prepares a device for power removal***||||
|L2/L3||NA *||||



- This combination of Bus/Function PM states not allowed. 

** If PME supported in this state. 

*** See “L2/L3 Ready Handshake Sequence” on page 764 for details regarding the sequence. 

**D3Cold State. Mandatory** . Every PCI Express Function enters the D3Cold PM state upon removal of power (Vcc) from the Function. When power is restored, the device must be reset or generate an internal reset, taking it from D3Cold to D0 Uninitialized. A Function capable of generating a PME must maintain PME context while in this state and when transitioning to the D0 state. Since power was removed to arrive at this state, the Function must have an auxiliary power source available if it is to maintain the PME context. Then, when the device goes to D0 Uninitialized, it can generate a PME message to inform the system of a wakeup event, if it’s capable and enabled to do so. For more on auxiliary power, refer to “Auxiliary Power” on page 775. 

Table 16‐9 on page 722 illustrates the PM policies while in the D3Cold state. 

**721** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐9: D3cold Power Management Policies_ 

|**Bus**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must be**<br>**valid**|**Power**|**Actions**<br>**permitted to**<br>**Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L2|D3cold|PME<br>context*|AUX<br>Power|Bus reset only|Signal Beacon<br>or WAKE#**|
|L3||None|||None|



- If PME supported in this state. 

** The method used to signal a wake to restore clock and power depends on the form factor. 

## **Function PM State Transitions** 

Figure 16‐6 illustrates the PM state transitions for a PCIe Function. Table 16‐10 on page 723 provides a description of each transition. Table 16‐11 on page 724 illustrates the transitions from one state to another from both a hardware and a software perspective. 

_Figure 16‐6: PCIe Function D‐State Transitions_ 

**==> picture [192 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
Power On<br>Reset D0<br>Un-initialized<br>D0<br>Active<br>D3<br>D1 D2<br>Hot<br>D3<br>Vcc Cold<br>Removed<br>**----- End of picture text -----**<br>


**722** 

**Chapter 16: Power Management** 

_Table 16‐10: Description of Function State Transitions_ 

|**From State**|**To State**|**Description**|
|---|---|---|
|D0<br>Uninitialized|D0 Active|Function has been completely configured and<br>enabled by its driver.|
|D0 Active|D1|Software writes the PMCSR PowerState to D1.|
||D2|Software writes the PMCSR PowerState to D2.|
||D3hot|Software writes the PMCSR PowerState to D3hot.|
|D1|D0 Active|Software writes the PMCSR PowerState to D0.|
||D2|Software writes the PMCSR PowerState to D2.|
||D3hot|Software writes the PMCSR PowerState to D3hot.|
|D2|D0 Active|Software writes the PMCSR PowerState to D0.|
||D3hot|Software writes the PMCSR PowerState to D3hot.|
|D3hot|D3cold|Power is removed from the Function.|
||D0<br>Uninitialized|Software writes the PMCSR PowerState to D0.|
|D3cold|D0<br>Uninitialized|Power is restored to the Function.|



**723** 

**PCI Ex ress Technolo p gy** 

_Table 16‐11: Function State Transition Delays_ 

|**Initial State**|**Next**<br>**State**|**Minimum software‐guaranteed delays**|
|---|---|---|
|D0|D1|0|
|D0 or D1|D2|200s from new state setting to first access (including<br>config accesses).|
|D0, D1, or D2|D3hot|10ms from new state setting to first access.|
|D1|D0|0|
|D2|D0|200s from new state setting to first access.|
|D3hot|D0|10ms from new state setting to first access.|
|D3cold|D0||



## **Detailed Description of PCI-PM Registers** 

The _PCI Bus PM Interface spec_ defines the PM registers (see Figure 16‐7) that are implemented in PCIe Functions. Configuration software can determine the PM capabilities and control its properties. 

_Figure 16‐7: PCI Function’s PM Registers_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-15-5"></a>
## 15.5 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|
|---|---|---|---|
|**Power Management Capabilities**<br>**(PMC)**||**Pointer to**<br>**Next Capability**|**Capability ID**<br>**01h**|
|**Data Register**|**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Control/Status Register**<br>**(PMCSR)**||



## **PM Capabilities (PMC) Register** 

The fields of this 16‐bit read‐only register are described in Table 16‐12. 

**724** 

**Chapter 16: Power Management** 

_Table 16‐12: The PMC Register Bit Assignments_ 

|**Bit(s)**|**Description**|
|---|---|
|31:27|**PME_Support**field. Indicates in which PM states the Function is capable<br>of sending a PME message. A zero in a bit indicates PME notification is<br>not supported in the respective PM state.<br>**Bit**<br>  **Corresponds to PM State**<br>27                      D0<br>28                      D1<br>29                      D2<br>30                      D3hot<br>31                      D3cold(Function requires aux power for PME logic<br>and Wake signaling via beacon or WAKE# pin)<br>Systems that support wake from D3coldmust also support aux power and<br>must use it to signal the wakeup.<br>Bits 31, 30, and 27 must be set to 1b for virtual PCI‐PCI Bridges imple‐<br>mented within Root and Switch Ports. This is required for ports that for‐<br>ward PME Messages.|
|26|**D2_Support**bit. 1 = Function supports the D2 PM state.|
|25|**D1_Support**bit. 1 = Function supports the D1 PM state.|



**725** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐12: The PMC Register Bit Assignments (Continued)_ 

|**Bit(s)**|**Description**|
|---|---|
|24:22|**Aux_Current**field. For a Function that supports generation of the PME<br>message from the D3coldstate, this field reports the current demand made<br>upon the 3.3Vaux power source (see “Auxiliary Power” on page 775) by<br>the Function’s logic that retains the PME context information. This infor‐<br>mation is used by software to determine how many Functions can simul‐<br>taneously be enabled for PME generation (based on the total amount of<br>current each draws from the system 3.3Vaux power source and the power<br>sourcing capability of the power source).<br>•<br>If the Function does not support PME notification from within the<br>D3coldPM state, this field is not implemented and always returns zero<br>when read. Alternatively, a new feature defined by PCI Express per‐<br>mits devices that do not support PMEs to report the amount of Aux<br>current they draw when enabled by the_Aux Power PM Enable_bit<br>within the Device Control register.<br>•<br>If the Function implements the Data register (see “Data Register” on<br>page 731), this field always returns zeros when read. The Data register<br>then takes precedence over this field in reporting the 3.3Vaux current<br>requirements for the Function.<br>•<br>If the Function supports PME notification from the D3coldstate and<br>does not implement the Data register, then the Aux_Current field<br>reports the 3.3Vaux current requirements for the Function. It is<br>encoded as follows:<br> **Bit**<br> **24 23 22                 Max Current Required**<br>1   1   1                                375mA<br>1   1   0                                320mA<br>1   0   1                                270mA<br>1   0   0                                220mA<br>0   1   1                                160mA<br>0   1   0                                100mA<br>0   0   1                                 55mA<br>0   0   0                                   0mA|



**726** 

**Chapter 16: Power Management** 

_Table 16‐12: The PMC Register Bit Assignments (Continued)_ 

|**Bit(s)**|**Description**|
|---|---|
|21|**Device‐Specific Initialization (DSI)**bit. A one in this bit indicates that<br>immediately after entry into the D0 Uninitialized state, the Function<br>requires additional configuration above and beyond setup of its PCI con‐<br>figuration Header registers before the Class driver can use the Function.<br>Microsoft OSs do not use this bit. Rather, the determination and initializa‐<br>tion is made by the Class driver.|
|20|Reserved.|
|19|**PME Clock**bit. Does not apply to PCI Express. Must be hardwired to 0.|
|18:16|**Version**field. This field indicates the version of the PCI Bus PM Interface<br>spec that the Function complies with.<br>**Bit**<br> **18 17 16       Complies with Spec Version**<br>0   0   1                             1.0<br>0   1   0                             1.1 (required by PCI Express)|



## **PM Control and Status Register (PMCSR)** 

This register, required for all PCI Express Devices, serves several purposes as described below. Table 16‐13 on page 728 provides a description of the PMCSR bit fields. 

- If the Function implements PME capability, a PME Enable bit permits soft‐ ware to enable or disable the Function’s ability to assert the PME message or WAKE# signal, and a Status bit reflects whether or not a PME has occurred. 

- If the optional Data register is implemented (see “Data Register” on page 731), two fields are used to permit software to select which informa‐ tion can be read through the Data register, and provide the scaling multi‐ plier for the Data register value. 

- The register’s PowerState field can be read to determine the current PM state of the Function and written to place the Function into a new PM state. 

**727** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐13: PM Control/Status Register (PMCSR) Bit Assignments_ 

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|31:24|all<br>zeros|Read<br>Only|See “Data Register” on page 731.|
|23|zero|Read<br>Only|Not used in PCI Express|
|22|zero|Read<br>Only|Not used in PCI Express|
|21:16|all<br>zeros|Read<br>Only|Reserved|
|15|See<br>Descrip<br>tion.|Read,<br>Write<br>one to<br>clear,<br>Sticky<br>RW1CS|**PME_Status**bit.**Optional**: only implemented if the<br>Function supports PME notification, otherwise zero.<br>This bit reflects whether the Function has experienced<br>a PME (even if the PME_En bit in this register has dis‐<br>abled the Function’s ability to send a PME message). If<br>set to one, the Function has experienced a PME. Soft‐<br>ware clears this bit by writing a one to it.<br>After reset, this bit is zero if the Function doesn’t sup‐<br>port PME in D3cold. If the Function does support PME<br>in D3cold, this bit is indeterminate at initial OS boot<br>time but after that reflects whether the Function has<br>experienced a PME.<br>If the Function supports PME from D3cold, the state of<br>this bit must persist even if power is lost or the Func‐<br>tion is reset (a sticky bit). This implies that an auxil‐<br>iary power source keeps this logic active during these<br>conditions (see “Auxiliary Power” on page 775).|



**728** 

**Chapter 16: Power Management** 

_Table 16‐13: PM Control/Status Register (PMCSR) Bit Assignments (Continued)_ 

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|14:13|Device‐<br>specific|Read<br>Only|**Data_Scale**field.**Optional**. If the Function does not<br>implement the Data register this field is hardwired to<br>return zeros.<br>If the Data register is implemented, the Data_Scale<br>field is mandatory and must be a read‐only value rep‐<br>resenting the multiplier for it. The value and interpre‐<br>tation of the Data_Scale field depends on the data<br>item selected to be viewed through the Data register<br>by the Data_Select field.|
|12:9|0000b|Read/<br>Write|**Data_Select**field.**Optional**. If the Function does not<br>implement the Data register, this field is hardwired to<br>return zeros.<br>If the Data register is implemented, Data_Select is a<br>mandatory read/write field. The value placed in this<br>register selects the data to be viewed in the Data regis‐<br>ter. That value must then be multiplied by the value<br>read from the Data_Scale field.|



**729** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐13: PM Control/Status Register (PMCSR) Bit Assignments (Continued)_ 

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|8|See<br>Descrip<br>tion.|Read/<br>Write|**PME_En**bit.**Optional**.<br>1 = enable Function’s ability to send PME messages<br>when an event occurs.<br>0 = disable.<br>If the Function does not support the generation of<br>PMEs from any power state, this bit always return<br>zero when read.<br>After reset, this bit is zero if the Function doesn’t sup‐<br>port PME from D3cold. If the Function supports PME<br>from D3cold:<br>• this bit is indeterminate at initial OS boot time.<br>• otherwise, it enables or disables whether the Func‐<br>tion can send a PME message in case a PME occurs.<br>If the Function supports PME from D3cold, the state of<br>this bit must persist while the Function remains in the<br>D3coldstate and during the transition from D3coldto<br>the D0 Uninitialized state. This implies that the PME<br>logic must use an aux power source to power this<br>logic during these conditions.|
|7:2|all<br>zeros|Read<br>Only|Reserved|
|1:0|00b|Read/<br>Write|**PowerState**field.**Mandatory**. Software uses this field<br>to read the current PM state of the Function or write a<br>new PM state. If software selects a PM state not sup‐<br>ported by the Function, the write completes normally<br>but the data is discarded and no state change occurs.<br>  **1 0           PM State**<br>0 0                D0<br>0 1                D1<br>1 0                D2<br>1 1                D3hot|



**730** 

**Chapter 16: Power Management** 

## **Data Register** 

**Optional, read‐only** . Refer to Figure 16‐8 on page 732. The Data register is an 8‐bit, read‐only register that provides software with the following information: 

- Power consumed in the selected PM state; useful in power budgeting. 

- Power dissipated in the selected PM state; useful in managing the thermal environment. 

- Any type of data could be reported through this register, but the PCI‐PM spec only defines power consumption and power dissipation information for it. 

If the Data register is implemented, the Data_Select and Data_Scale fields of the PMCSR registers must also be implemented, and the Aux_Current field of the PMC register must not be implemented. 

**Determining Presence of the Data Register.** Software can perform the following procedure to check for the presence of the Data register: 

1. Write a value of 0000b into the Data_Select field of the PMCSR register. 

2. Read from either the Data register or the Data_Scale field of the PMCSR register. A non‐zero value indicates that the Data register as well as the Data_Scale and Data_Select fields of the PMCSR registers are imple‐ mented. If a value of zero is read, go to step 4.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-15-6"></a>
## 15.6 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

3. If the current value of the Data_Select field is a value other than 1111b, go to step 4. If the current value of the Data_Select field is 1111b, all pos‐ sible Data register values have been scanned and returned zero, indicat‐ ing that neither the Data register nor the Data_Scale and Data_Select fields of the PMCSR registers are implemented. 

4. Increment the content of the Data_Select field and go back to step 2. Since the data select field is only 4 bits, a complete scan requires testing 16 possible select values and looking to see if any non‐zero values are seen for the data and scale registers. 

**Operation of the Data Register.** The information returned is typically a static copy of the Function’s worst‐case power consumption and power dis‐ sipation characteristics in the various PM states (as listed in the Device’s data sheet). To use the Data register, the programmer uses the following sequence: 

1. Write a value into the Data_Select field (see Table 16‐14 on page 733) of the PMCSR register to select the data item to be viewed through the Data register. 

**731** 

**PCI Ex ress Technolo p gy** 

2. Read the data value from Data register and the Data_Scale field of the PMCSR register. 

3. Multiply the value by the scaling factor. 

**Multi‐Function Devices.** In a multi‐function PCI Express device, each Function must supply its own power information. The power information for the logic common to all the Functions is reported through Function zero’s Data register (see Data Select Value = 8 in Table 16‐14 on page 733). 

**Virtual PCI‐to‐PCI Bridge Power Data.** The spec doesn’t specify data field use in PCI‐to‐PCI bridge Functions in a Root Complex or Switch. But, to maintain PCI‐PM compatibility, bridges must report the power informa‐ tion they consume. Software could read the virtual PPB Data registers at each port of a switch to determine the power consumed by the switch in each power state. 

_Figure 16‐8: PM Registers_ 

|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|
|---|---|---|---|
|**Power Management Capabilities**<br>**(PMC)**||**Pointer to**<br>**Next Capability**|**Capability ID**<br>**01h**|
|**Data Register**|**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Control/Status Register**<br>**(PMCSR)**||



**732** 

**Chapter 16: Power Management** 

_Table 16‐14: Data Register Interpretation_ 

|**Data Select Value**|**Data Reported in**<br>**Data Register**|**Interpretation of Data**<br>**Scale Field in PMCSR**|**Units/**<br>**Accuracy**|
|---|---|---|---|
|00h|Power consumed in D0|00b = unknown<br>01b = multiply by 0.1<br>10b = multiply by 0.01<br>11b = multiply by 0.001|Watts|
|01h|Power consumed in D1|||
|02h|Power consumed in D2|||
|03h|Power consumed in D3|||
|04h|Power dissipated in D0|||
|05h|Power dissipated in D1|||
|06h|Power dissipated in D2|||
|07h|Power dissipated in D3|||
|08h|In a multi‐function PCI<br>device, Function 0 indi‐<br>cates power consumed<br>by logic common to all<br>Functions in the pack‐<br>age.|||
|09h‐0Fh|Reserved for future use<br>of Function 0 in a<br>multi‐function device.|Reserved|TBD|
|08h‐0Fh|Reserved in single‐func‐<br>tion devices and Func‐<br>tions other than<br>Function 0 in a<br>multi‐function device|||



## **Introduction to Link Power Management** 

We’ve just seen how software can put Devices into one of several device power states, now let’s consider how PCIe also manages Link power. Device power and Link power are related to each other, as shown in Table 16‐15 on page 734. Note also the relationship between downstream and upstream devices, which can be summarized by saying that an upstream Device or Link cannot be in a more aggressive power‐conserving state than the one below it. The reason is to 

**733** 

**PCI Ex ress Technolo p gy** 

facilitate timely delivery of packets from the Endpoints, whose traffic would be delayed if upstream devices were in a lower power state. Each relationship is described below: 

**D0** — Device is fully powered and typically in the L0 Link state. Some power conservation is available without leaving this state by using DPA substates (see “Dynamic Power Allocation (DPA)” on page 714), and by using the hard‐ ware‐based Link power management (see “Active State Power Management (ASPM)” on page 735 for more details). 

**D1 & D2** — When software changes the device state to D1 or D2, the Link must automatically transition to the L1 state. Since both Link partners are involved in this operation there is a handshake mechanism to ensure that things are done in an orderly fashion. 

**D3hot** — When software places a device into the D3 state, the Link automati‐ cally transitions to L1 just as it does when going to the D1 and D2 states. Soft‐ ware may now choose to remove the reference clock and power, putting the device into D3cold. But, before doing that, it’s expected that the system will ini‐ tiate a handshake process to prepare the Links by putting them into the L2/L3 Ready state. 

**D3cold** — In this state, main power and the reference clock have been turned off. However, auxiliary power (VAUX) may be available, allowing the device to sig‐ nal a wakeup event to the system. If it is, the Link state will be in L2. If main power is removed but VAUX is not available, the Link will be in L3. Table 16‐16 on page 735 provides additional information regarding the Link power states. 

_Table 16‐15: Relationship Between Device and Link Power States_ 

|**Downstream**<br>**Component D‐State**|**Permissible Upstream**<br>**Component D‐State**|**Permissible**<br>**Interconnect State**|
|---|---|---|
|D0|D0|L0, L0s & L1 (optional)|
|D1|D0‐D1|L1|
|D2|D0‐D2|L1|
|D3 hot|D0‐D3 hot|L1, L2/L3 Ready|
|D3 cold|D0‐D3 cold|L2 (AUX Pwr), L3|



**734** 

**Chapter 16: Power Management** 

## _Table 16‐16: Link Power State Characteristics_ 

|**State**|**Description**|**Software**<br>**Directed?**|**Active**<br>**State**<br>**Link PM**|**Ref.**<br>**Clocks**|**Main**<br>**Power**|**PLL**|**Vaux**|
|---|---|---|---|---|---|---|---|
|L0|Fully Active|Yes (D0)|On|On|On|On|On/Off|
|L0s|Standby|No|Yes<br>(D0)|On|On|On|On/Off|
|L1|Low Power<br>Standby|Yes*<br>(D1‐D3 hot)|Yes(option)<br>(D0)|On|On|On/Off|On/Off|
|L2/L3<br>Ready|Staging for<br>power<br>removal|Yes<br>PME_Turn_Off<br>handshake|No|On|On|On/Off|On/Off|
|L2|Low Power<br>Sleep|Yes**|No|Off|Off|Off|On|
|L3|Off<br>(Zero Power)|N/A|N/A|Off|Off|Off|Off|



- The L1 state is entered either due to PM software placing a device into the D1, D2, or D3 states or under hardware control with ASPM. 

- ** The spec describes the L2 state as being software directed. The other L‐states in the table are listed as software directed because software initiates the transition into these states. For example, when software initiating a device power state change to D1, D2, or D3 devices must respond by enter‐ ing the L1 state. Software then causes the transition to the L2/L3 Ready state by initiating a PME_Turn_Off message. Finally, software initiates the removal of power from a device after the device has transitioned to the L2/ L3 Ready state. Because Vaux power is available in L2, a wakeup event can be signaled to notify software. 

## **Active State Power Management (ASPM)** 

ASPM is a hardware‐based Link power conservation mechanism that only applies while the device is in the D0 device power state. Transitions into and out of ASPM states are initiated by hardware based on implementation‐specific cri‐ teria; software can’t control or observe this operation, it can only enable or dis‐ able it using configuration register bits (see Figure 16‐15 on page 744). 

**735** 

**PCI Ex ress Technolo p gy** 

Two low power states are defined for ASPM: 

1. L0s (standby state) — This state provide substantial power savings but still allows quick entry and exit latencies. The main way this is done is by put‐ ting the Transmitter into the Electrical Idle condition. Support for this state was previously required for all PCIe devices in the earlier spec versions, but in the 3.0 spec it became optional. 

2. L1 ASPM — The goal for L1 is to achieve greater power conservation than L0s for situations where longer entry and exit latencies are acceptable. For example, in this state both Transmitters go into Electrical Idle at the same time. Support for this state continues to be optional in the 3.0 spec as it was in the earlier specs. 

## **Electrical Idle** 

Since putting a Transmitter into Electrical Idle is a central part of ASPM, it will help to discuss how doing so works. When a Transmitter’s differential signals (TxD+ and TxD‐) goes into the Electrical Idle condition, it stops signaling and instead holds its voltage very close to the common mode voltage with a differ‐ ential voltage of 0 V. Signal transitions consume power, so stopping them on the Link gives power savings while still allowing a fairly quick resumption back to normal Link activity during which it is said to be in the L0 state. Depending on the degree of power savings, the Link is either in the L0s or L1 state. During this time, the transmitter may choose to remain in the low‐impedance state or change to high impedance by turning off its termination logic to save more power. In addition to L0s and L1, Electrical Idle will also be in effect when the Link has been disabled. 

## **Transmitter Entry to Electrical Idle** 

Transmitters that wish to enter the Electrical Idle condition must first inform the Link partner so the lack of further signaling won’t be misinterpreted as an error. They do that by sending the EIOS (Electrical Idle Ordered‐Set) and then quickly ceasing transmission and tri‐stating the Link output drivers. What the EIOS looks like depends on the encoding method in use, as described in the following sections. Once the last EIOS has been sent, the Transmitter must enter Electrical Idle within 8ns and remain in that mode for at least 20ns, regardless of the data rate. The differential peak voltage allowed during Electrical Idle must be between 0 and 20mV peak, again regardless of the data rate, to reduce the chance of the Receiver misinterpreting noise on the line as a valid signal. (See Table 13‐3 on page 489 for more on these timing and voltage parameters.) 

**736** 

**Chapter 16: Power Management** 

**Gen1/Gen2 Mode Encoding.** For Gen1/Gen2 mode, the EIOS takes the form shown in Figure 16‐9 on page 737. All four Symbols must be sent, but the Receiver only needs to see two IDL control characters to recognize this condition. 

_Figure 16‐9: Gen1/Gen2 Mode EIOS Pattern_ 

**==> picture [134 x 100] intentionally omitted <==**

**----- Start of picture text -----**<br>
Encoding<br>COM K28.5<br>IDL K28.3<br>IDL K28.3<br>IDL K28.3<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-15-7"></a>
## 15.7 Error Detection and Handling | 错误检测与处理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Gen3 Mode Encoding.** For Gen3 mode, the EIOS is an Ordered Set block that consists of an Ordered Set Sync Header (01b) followed by 16 bytes that are all 66h, as shown in Figure 16‐10 on page 737. Curiously, a Transmitter is not required to finish the block if it will go directly to Electrical Idle but is allowed to stop after Symbol 13 (anywhere in Symbol 14 or 15). The reason is to allow for the case where an internal clock doesn’t line up with the Sym‐ bol boundaries due to 128b/130b encoding. This truncation won’t cause a problem at the Receiver because it only needs to see Symbols 0 ‐ 3 of the EIOS to recognize it. 

_Figure 16‐10: Gen3 Mode EIOS Pattern_ 

**==> picture [110 x 153] intentionally omitted <==**

**----- Start of picture text -----**<br>
EIOS<br>Sync Header 01<br>Byte 0 01100110<br>1 01100110<br>2 01100110<br>3 01100110<br>4 01100110<br>13 01100110<br>14 01100110<br>15 01100110<br>**----- End of picture text -----**<br>


**737** 

**PCI Ex ress Technolo p gy** 

## **Transmitter Exit from Electrical Idle** 

When a Transmitter is instructed to exit from Electrical Idle, the steps it takes depend on the data rate in use (see below). However, it must resume transmis‐ sion within less than 8ns by sending FTSs or TS1/TS2s causing transition back to the L0 full‐on state. 

**Gen1 Mode.** For 2.5 GT/s, the process is simple: it begins using valid dif‐ ferential signals to send the TS1s or FTSs that will serve to inform the Receiver about the change. The Receiver detects the voltage as being above the squelch threshold and begins to evaluate the incoming signal. 

**Gen2 Mode.** When using 5.0 GT/s, the signals are changing so quickly that they don’t have time to reach the higher voltage levels. That makes it more difficult to quickly detect when the voltages have changed back to the oper‐ ational values. To make this easier, the EIEOS (Electrical Idle Exit Ordered Set), was defined to provide a lower‐frequency sequence. The EIEOS for 8b/ 10b encoding, shown in Figure 16‐11 on page 739, uses repeated K28.7 con‐ trol characters to appear as a repeating string of 5 ones followed by 5 zeros. This gives the low‐frequency signal that allows the higher signal voltages that are more readily seen. In fact, the spec states that this pattern guaran‐ tees that the Receiver will properly detect an exit from Electrical Idle, some‐ thing that scrambled data cannot do. The EIEOS is to be sent under the following conditions: 

- Before the first TS1 after entering the Configuration.Linkwidth.Start or Recovery.RcvrLock state. 

- After every 32 TS1s or TS2s are sent in Configuration.Linkwidth.Start, Recovery.RcvrLock, or Recovery.RcvrCfg states. The TS1/TS2 count is reset to zero whenever an EIEOS is sent or the first TS2 is received in the Recovery.RcvrCfg state. 

**738** 

**Chapter 16: Power Management** 

_Figure 16‐11: Gen1/Gen2 Mode EIEOS Symbol Pattern_ 

**==> picture [100 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
EIEOS<br>Symbol 0 K28.5<br>1 K28.7<br>2 K28.7<br>3 K28.7<br>4 K28.7<br>13 K28.7<br>14 K28.7<br>15 D10.2<br>**----- End of picture text -----**<br>


**Gen3 Mode.** An EIEOS is needed for 8 GT/s rate too and for the same rea‐ son as for 5.0 GT/s. Now, though, the Ordered Set takes the form of a block, as shown in Figure 16‐12 on page 740. As before, it gives a low‐frequency pattern in alternating bytes of 00h and FFh, which appears as a repeating string of 8 zeros followed by 8 ones. 

In addition, EIEOS is sent so as to allow a receiver during LTSSM Recovery state to establish Block Lock after which the Link transitions to the L0 state. See the section “Block Alignment” on page 411 and “Achieving Block Align‐ ment” on page 438. 

In Gen3 mode, EIEOS is to be sent: 

- Before the first TS1 after entering the Configuration.Linkwidth.Start or Recovery.RcvrLock state. 

- Immediately after an EDS Framing Token when a Data Stream is end‐ ing if an EIOS is not being sent and the LTSSM is not entering Recov‐ ery.RcvrLock. 

- After every 32 TS1s/TS2s whenever TS1s or TS2s are sent. The count is reset to zero when: 

- 

   - an EIEOS is sent 

- the first TS2 is received while in either the Recovery.RcvrCfg or Config‐ uration.Complete LTSSM state 

- a Downstream Port in Phase 2 of the Equalization sequence, or an Upstream Port in Phase 3, receives two TS1s with the Reset EIEOS Inter‐ val Count bit set. 

**739** 

**PCI Ex ress Technolo p gy** 

- After every 2[16] TS1s during the Equalization sequence, if the Reset EIEOS Interval Count bit has prevented it from being sent. The spec states that designs are allowed to satisfy this requirement by sending and EIEOS within 2 TS1s of the scrambling LFSR matching its seed value. 

- As part of an FTS sequence, Compliance Pattern, or Modified Compliance pattern. 

_Figure 16‐12: 128b/130b EIEOS Block_ 

**==> picture [138 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
EIEOS<br>Sync Header 01<br>Byte 0 00000000<br>1 11111111<br>2 00000000<br>3 11111111<br>4 00000000<br>13 11111111<br>14 00000000<br>15 11111111<br>**----- End of picture text -----**<br>


## **Receiver Entry to Electrical Idle** 

When a Transmitter enters Electrical Idle, the Link partner’s Receiver responds based on the data rate, as described in the following sections. Receipt of an EIOS informs the Receiver that this is going to happen, preparing it to detect when it actually does happen. When the Receiver detects this condition it de‐gates the error logic to prevent reporting errors caused by unreliable activity on the Link and arms its Electrical Idle Exit detector so it will be ready to resume normal activity when the Transmitter begins to send data again. There are two Electri‐ cal Idle detection options.: 

**Detecting Electrical Idle Voltage.** Once an EIOS has been received, the expectation is that the Transmitter will cease transmission very quickly. In the 1.x spec versions Receivers detect this by observing that the incoming voltage has dropped below the threshold of a valid signal. This isn’t too dif‐ ficult at 2.5 GT/s but it requires a squelch detect circuit that consumes space and power. 

**740** 

**Chapter 16: Power Management** 

**Inferring Electrical Idle.** However, at higher frequencies the signal becomes increasingly attenuated, making it difficult for squelch detect logic to distinguish the levels. This is especially true for 8.0 GT/s, where it’s expected that the Receiver may need to perform equalization internally to recover a good signal. To alleviate these detection problems, the 2.0 spec introduced the concept of allowing a Receiver to infer when the Link has gone to the Electrical Idle condition rather than testing the voltage level. In this model, the absence of expected events is used to indicate that the Link is not signaling and can therefore be assumed to be in Electrical Idle, as listed in Table 16‐17. By way of explanation, Flow Control Updates should arrive regularly while the Link is in L0, and SOSs are expected with certain timing, too. For simplicity, a Receiver is allowed to check for one or the other or both of these conditions. During Link training the TS1s and TS2s should arrive regularly, so their absence can also be taken to mean that the Link is Idle. For the last two rows of the table, though, it’s possible that no Symbols have been received at all, and that will also be understood to mean the Link is Idle. Since Electrical Idle takes place for the overall Link and not for Lanes independently, there’s no need for each Lane to measure these times. Instead, an LTSSM can just use one timer in common for all the Lanes on that Link. 

_Table 16‐17: Electrical Idle Inference Conditions_ 

|State|2.5GT/s|5.0 GT/s|8.0 GT/s|
|---|---|---|---|
|L0|Absence of an FC Update or SOS in a 128s window|||
|Recovery.RcvrCfg|Absence of a TS1 or TS2 in a 1280 UI<br>interval||Absence of a TS1<br>or TS2 in a 4ms<br>window|
|Recovery.Speed<br>(successful_speed_<br>negotiation = 1b)|Absence of a TS1 or TS2 in a 1280 UI<br>interval||Absence of a TS1<br>or TS2 in a 4680<br>UI interval|
|Recovery.Speed<br>(successful_speed_<br>negotiation = 0b)|Absence of an exit<br>from Electrical Idle<br>in a 2000 UI interval|Absence of an exit from Electrical<br>Idle in a 16000 UI interval||
|Loopback.Active<br>(as a slave)|Absence of an exit<br>from Electrical Idle<br>in a 128s window|N/A|N/A|



**741** 

**PCI Ex ress Technolo p gy** 

How the EIOS is recognized at the Receiver also depends on the encoding scheme. For Gen1/Gen2 mode, a receiver recognizes an EIOS when it sees two of the three IDL Symbols. For Gen3 mode, it’s recognized when Symbols 0‐3 of the incoming block match the EIOS pattern. 

## **Receiver Exit from Electrical Idle** 

Receivers detect a voltage difference to signify a resumption of normal signal‐ ing. An exit from Electrical Idle will be detected when the differential peak‐to‐peak voltage exceeds the Electrical Idle Detect threshold, which is allowed to be set between 65 and 175mV for all data rates. 

At 2.5 GT/s nothing more is needed, but at higher rates Receivers don’t have to rely on this detection circuit except when receiving EIEOS during certain LTSSM states or during the four EIE Symbols that precede transmission of an FTS sequence at 5.0 GT/s. The number and timing of EIEOSs to facilitate detec‐ tion of Electrical Idle exit depends on the Link state. For more on this, see “Active State Power Management (ASPM)” on page 735. 

In Electrical Idle, the Receiver’s PLL looses clock synchronization. When the Transmitter exits Electrical Idle, it sends FTSs to exit from L0s, or TS1/TS2s to exit from all other Link states. Doing so supplies the needed transition density for the CDR logic to re‐synchronize the receiver PLL and achieve Bit Lock and Symbol Lock or Block Alignment. 

Figure 16‐13 illustrates the Link state transitions and highlights the transitions between L0, L0s, and L1. Note that there is no direct path from L0s to L1, so the Link must be returned to the L0 state before changing between them. 

_Figure 16‐13: ASPM Link State Transitions_ 

**==> picture [274 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
L0<br>L2/L3<br>L0s L1 Recovery LDn<br>Ready<br>L2 L3<br>**----- End of picture text -----**<br>


**742** 

**Chapter 16: Power Management** 

The Link Capability register specifies a device’s support for Active State Power Management. Figure 16‐14 illustrates the _ASPM Support_ field within this regis‐ ter. In earlier spec versions, not all 4 options were available, but the 2.1 spec filled in all of them. Note that bit 22 indicates whether all the options are avail‐ able. 

_Figure 16‐14: ASPM Support_ 

**==> picture [360 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Capabilities Register<br>31 24 23 22 21 20 19 18 17 1514 12 11 10 9 4 3 0<br>Port Number<br>ASPM Optionality<br>Compliance<br>0  0 No ASPM Support<br>0  1 L0s Supported<br>1  0 L1 Supported<br>1  1 L0s & L1 supported<br>Active State PM Support<br>**----- End of picture text -----**<br>


Software can enable and disable ASPM via the _Active State PM Control_ field of the Link Control Register as illustrated in Figure 16‐15 on page 744. The possi‐ ble settings are listed in Table 16‐18 on page 743. Note: The spec recommends that ASPM be disabled for all components in a path used for Isochronous trans‐ actions if the additional latencies associated with ASPM exceed the limits of the isochronous transactions. 

_Table 16‐18: Active State Power Management Control Field Definition_ 

|**Setting**|**Description**|
|---|---|
|00b|L0s and L1 ASPM disabled|
|01b|L0s enabled and L1 disabled|



**743** 

**PCI Ex ress Technolo p gy** 

_Table 16‐18: Active State Power Management Control Field Definition (Continued)_ 

|**Setting**|**Description**|
|---|---|
|10b|L1 enabled and L0s disabled|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
