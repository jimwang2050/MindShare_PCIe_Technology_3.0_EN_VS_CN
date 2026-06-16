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
