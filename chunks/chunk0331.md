PCI added MSI support as an option years ago and PCIe made that capability a requirement. A peripheral that can generate MSI transactions on its own opens new options for handling interrupts, such as giving each Function the ability to generate multiple unique interrupts instead of just one. 

## **Legacy PCI Interrupt Delivery** 

This section provides more detail on legacy PCI interrupt delivery. Readers familiar with PCI may wish to proceed to “Virtual INTx Signaling” on page 805 to learn more about how PCIe emulates this legacy model, or to “The MSI Model” on page 812 to learn more about that method. 

PCI devices that use interrupts have two options. They may use either: 

- INTx# active low‐level signals that can be shared and were defined in the original spec. 

- Message Signaled Interrupts that were added as an option with the 2.2 ver‐ sion of the spec. MSI needs no modification for use in a PCIe system. 

## **Device INTx# Pins** 

A PCI device can implement up to 4 INTx# signals (INTA#, INTB#, INTC#, and INTD#). More than one pin is available because PCI devices can support up to 8 functions, each of which is allowed to drive one (but only one) interrupt pin. When PCI was developed, a typical system used a chipset that included the 15‐ input 8259 PIC, so that’s how many IRQs (which map to interrupt vectors) that were available to the system. However, many of those were already used for system purposes like the system timer, keyboard interrupt, mouse interrupt, and so on. In addition, some pins were reserved for ISA cards that could still be plugged into these older systems. Consequently, the PCI spec writers consid‐ ered that only four IRQs would reliably be available for their new bus, and so the spec only supported four interrupt pins. However, as you probably know, there are typically more than four PCI devices on a PCI bus and even a single device could have more than four functions inside, each wanting its own inter‐ 

**800** 

**Chapter 17: Interrupt Support** 

rupt. These reasons are why the PCI interrupts were designed to be level‐sensi‐ tive and shareable. These signals could simply be wire‐ORed together to get down to a handful of resulting outputs, each one representing interrupt requests. Since they are shared, when an interrupt is detected, the interrupt handler software will need to go through the list of functions that are sharing the same pin and test to see which ones need servicing. 

## **Determining INTx# Pin Support** 

PCI functions indicate support for an INTx# signal in their configuration head‐ ers. The read‐only Interrupt Pin register illustrated in Figure 17‐5 indicates whether an INTx# is supported by this function and if so, which interrupt pin will it assert when requesting an interrupt. 

_Figure 17‐5: Interrupt Registers in PCI Configuration Header_ 

**==> picture [284 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 2 Byte1 0 DW<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>BIST HeaderType LatencyTimer CacheLineSize 03 00h = IRQ0<br>04 01h = IRQ1<br>Base Address 0<br>Base Address 1 05 RW 02h = IRQ2<br>03h = IRQ3<br>06 access<br>Base Address 2 04h = IRQ4<br>Base Address 3 07 05h = IRQ5<br>08 :<br>Base Address 4 :<br>:<br>09<br>Base Address 5 FEh = IRQ254<br>10<br>CardBus CIS Pointer FFh = IRQ255<br>Subsystem ID SubsystemVendor ID 11<br>Expansion ROM 12<br>Base Address<br>Reserved CapabilitiesPointer 13 RO 00h = No INTx# pin used<br>Reserved 14 access 01h = INTA#<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 02h = INTB#03h = INTC#<br>04h = INTD#<br>**----- End of picture text -----**<br>


**801** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Interrupt Routing** 

The Interrupt Line register shown in Figure 17‐5 on page 801 gives the next information that a driver needs to know: the input pin of the PIC to which this pin has been connected. The PIC is programmed by system software with a unique vector number for each input pin (IRQ). The vector for the highest‐prior‐ ity interrupt asserted is reported to the processor who then uses that vector to index into a corresponding entry in the interrupt vector table. This entry points to the interrupting device’s interrupt service routine which the processor exe‐ cutes. 

The platform designer assigns the routing of INTx# pins from devices. They can be routed in a variety of ways, but ultimately each INTx# pin connects to an input of the interrupt controller. Figure 17‐6 on page 803 illustrates an example in which several PCI device interrupts are connected to the interrupt controller through a programmable router. All signals connected to a given input of the programmable router will be directed to a specific input of the interrupt con‐ troller. Functions whose interrupts are routed to a common interrupt controller input will all have the same Interrupt Line number assigned to them by plat‐ form software (typically firmware). In this example, IRQ15 has three PCI INTx# inputs from different devices connected to it. Consequently, the functions using these INTx# lines will share IRQ15 and will therefore all cause the controller to send the same vector when queried. That vector will have the three ISRs for the different Functions chained together. 

## **Associating the INTx# Line to an IRQ Number** 

Based on system requirements, the router is programmed to connect its four inputs to four available PIC inputs. Once this is done, the routing of the INTx# pin associated with each function is known and the Interrupt Line number is written by software into each Function. The value is ultimately read by the Function’s device driver so it will know which interrupt table entry it has been assigned. That’s the place where the starting address of its ISR will be written, a process referred to as “hooking the interrupt”. When this function later gener‐ ates an interrupt, the CPU will receive the vector number that corresponds to the IRQ specified in the Interrupt Line register. The CPU uses this vector to index into the interrupt vector table to fetch the entry point of the interrupt ser‐ vice routine associated with the Function’s device driver. 

**802** 

**Chapter 17: Interrupt Support** 

_Figure 17‐6: INTx Signal Routing is Platform Specific_ 

**==> picture [371 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTA#<br>INTA#<br>INTB# ISA<br>Slave<br>Programmable 8259A<br>Interrupt<br>Interrupt<br>Router<br>Controller<br>INTA#<br>IRQ8<br>IRQ9 (IRQ2)<br>IRQ10<br>INTA# IRQ11<br>INTB# IRQ12 ISA<br>INTC# Input 0# IRQ13 Master<br>INTD# InInput 2#put 1# IRQ14 IRQ15 Interrupt8259A<br>Controller<br>INTA# Input 3#<br>IRQ0<br>IRQ1<br>Interrupt<br>to CPU<br>INTA# IRQ3<br>INTB# IRQ4<br>IRQ5<br>IRQ6<br>IRQ7<br>INTA#<br>**----- End of picture text -----**<br>


## **INTx# Signaling** 

The INTx# lines are active‐low signals implemented as open‐drain with a pul‐ lup resistor provided on each line by the system. Multiple devices connected to the same PCI interrupt request signal line can assert it simultaneously without damage. 

When a Function signals an interrupt it also sets the Interrupt Status bit located in the Status register of the config header. This bit can be read by system soft‐ ware to see if an interrupt is currently pending. (See Figure 17‐8 on page 805.) 

**Interrupt Disable.** The 2.3 PCI spec added an Interrupt Disable bit (Bit 10) to the Command register of the config header. See Figure 17‐7 on page 804. The bit is cleared at reset permitting INTx# signal generation, but software may set it 

**803** 

**PCI Ex ress 3.0 Technolo p gy** 

to prevent that. Note that the Interrupt Disable bit has no effect on Message Sig‐ nalled Interrupts (MSI). MSIs are enabled via the Command Register in the MSI Capability structure. Enabling MSI automatically has the effect of disabling interrupt pins or emulation. 

**Interrupt Status.** The PCI 2.3 spec added a read‐only Interrupt Status bit to the configuration status register (pictured in Figure 17‐8 on page 805). A func‐ tion must set this status bit when an interrupt is pending. In addition, if the Interrupt Disable bit in the Command register of the header is cleared (i.e. inter‐ rupts enabled), then the function’s INTx# signal is asserted when this status bit is set. This bit is unaffected by the state of the Interrupt Disable bit. 

_Figure 17‐7: Configuration Command Register — Interrupt Disable Field_ 

**==> picture [316 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 11 10 9 8 7 6 5 4 3 2 1 0<br>Reserved R<br>Interrupt Disable, was Reserved<br>Fast Back-to-Back Enable<br>SERR# Enable<br>Reserved, was Stepping Control<br>Parity Error Response<br>VGA Palette Snoop Enable<br>Memory Write and Invalidate Enable<br>Special Cycles<br>Bus Master<br>Memory Space<br>IO Space<br>**----- End of picture text -----**<br>


**804** 

**Chapter 17: Interrupt Support** 

_Figure 17‐8: Configuration Status Register — Interrupt Status Field_ 

**==> picture [342 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 8 7 6 5 4 3 2 0<br>R Reserved<br>Interrupt Status<br>Capabilities List<br>66MHz-Capable<br>Reserved<br>Fast Back-to-Back Capable<br>Master Data Parity Error<br>DEVSEL Timing<br>Signalled Target-Abort<br>Received Target-Abort<br>Received Master-Abort<br>Signalled System Error<br>Detected Parity Error<br>**----- End of picture text -----**<br>


## **Virtual INTx Signaling** 

## **General** 

If circumstances make the use of MSI not possible in a PCIe topology, the INTx signaling model would be used. Following are two examples of devices that would need to be able to use INTx messages: 

**PCIe‐to‐(PCI or PCI‐X) bridges** — Most PCI devices will use the INTx# pins because MSI support is optional for them. Since PCIe doesn’t support sideband interrupt signaling, the inband messages are used instead. The interrupt con‐ troller understands the message and delivers an interrupt request to the CPU which would include a pre‐programmed vector number. 

**Boot Devices** — PC systems commonly use the legacy interrupt model during the boot sequence because MSI usually requires OS‐level initialization. Gener‐ ally, a minimum of three subsystems are needed for booting: an output to the operator such as video, an input from the operator which is typically the key‐ board, and a device that can be used to fetch the OS, typically a hard drive. PCIe devices involved in initializing the system are called “boot devices.” Boot devices will use legacy interrupt support until the OS and device drivers are loaded, after which it’s preferable they use MSI. 

**805** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Virtual INTx Wire Delivery** 

Figure 17‐9 on page 806 illustrates a system with a PCIe Endpoint and a PCI Express‐to‐PCI Bridge. If we assume software has not enabled MSI on the End‐ point, it will deliver interrupt requests with INTx messages. In this example, the bridge is propogating pin‐based interrupts from connected PCI devices with INTx messages. As can be seen, the bridge sends an INTB messages to signal the assertion and deassertion of its INTB# input from the PCI bus. The PCIe Endpoint is shown signaling an INTA using emulation messages. Note that INTx# signaling involves two messages: 

- **Assert_INTx** messages indicate a high‐to‐low transition (from inactive to active) of the virtual INTx# signal. 

- **Deassert_INTx** messages indicate a low‐to‐high transition. 

When a Function delivers an Assert_INTx message, it also sets its Interrupt Sta‐ tus bit in the Configuration Status register, just as it would if it asserted the physical INTx# pin (see Figure 17‐8 on page 805). 

_Figure 17‐9: Example of INTx Messages to Virtualize INTA#‐INTD# Signal Transitions_ 

**==> picture [230 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>