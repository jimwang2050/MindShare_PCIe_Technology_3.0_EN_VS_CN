_Figure 16‐44: LTR ‐ Link Down Case_ 

**==> picture [121 x 75] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>value<br>Conglomerate  1200 ns115700 ns<br>value<br>Switch<br>**----- End of picture text -----**<br>


**791** 

**PCI Ex ress Technolo p gy** 

**792** 

## _**17 Interrupt Support**_ 

## **The Previous Chapter** 

The previous chapter provides an overall context for the discussion of system power management and a detailed description of PCIe power management, which is compatible with the _PCI Bus PM Interface Spec_ and the _Advanced Config‐ uration and Power Interface_ (ACPI) spec. PCIe defines extensions to the PCI‐PM spec that focus primarily on Link Power and event management. An overview of the OnNow Initiative, ACPI, and the involvement of the Windows OS is also provided. 

## **This Chapter** 

This chapter describes the different ways that PCIe Functions can generate interrupts. The old PCI model used pins for this, but sideband signals are unde‐ sirable in a serial model so support for the inband MSI (Message Signaled Inter‐ rupt) mechanism was made mandatory. The PCI INTx# pin operation can still be emulated using PCIe INTx messages for software backward compatibility reasons. Both the PCI legacy INTx# method and the newer versions of MSI/MSI‐ X are described. 

## **The Next Chapter** 

The next chapter describes three types of resets defined for PCIe: Fundamental reset (consisting of cold and warm reset), hot reset, and function‐level reset (FLR). The use of a sideband reset PERST# signal to generate a system reset is discussed, and so is the inband TS1 based Hot Reset described. 

**793** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Interrupt Support Background** 

## **General** 

The PCI architecture supported interrupts from peripheral devices as a means of improving their performance and offloading the CPU from the need to poll devices to determine when they require servicing. PCIe inherits this support largely unchanged from PCI, allowing software backwards compatibility to PCI. We provide a background to system interrupt handling in this chapter, but the reader who wants more details on interrupts is encouraged to look into these references: 

- For PCI interrupt background, refer to the PCI spec rev 3.0 or to chapter 14 of MindShare’s textbook: PCI System Architecture (www.mindshare.com). 

- To learn more about Local and IO APICs, refer to MindShare’s textbook: x86 Instruction Set Architecture. 

## **Two Methods of Interrupt Delivery** 

PCI used sideband interrupt wires that were routed to a central interrupt con‐ troller. This method worked well in simple, single‐CPU systems, but had some shortcomings that motivated moving to a newer method called MSI (Message Signaled Interrupts) with an extension called MSI‐X (eXtented). 

**Legacy PCI Interrupt Delivery** — This original mechanism defined for the PCI bus consists of up to four signals per device or INTx# (INTA#, INTB#, INTC#, and INTD#) as shown in Figure 17‐1 on page 795. In this model, the pins are shared by wire‐ORing them together, and they’d eventually be connected to an input on the 8259 PIC (Programmable Interrupt Controller). When a pin is asserted, the PIC in turn asserts its interrupt request pin to the CPU as part of a process described in “The Legacy Model” on page 796. 

PCIe supports this PCI interrupt functionality for backward compatibility, but a design goal for serial transports is to minimize the pin count. As a result, the INTx# signals were not implemented as sideband pins. Instead, a Function can generate an inband interrupt message packet to indicate the assertion or deas‐ sertion of a pin. These messages act as “virtual wires”, and target the interrupt controller in the system (typically in the Root Complex), as shown in Figure 17‐ 2 on page 796. This picture also illustrates how an older PCI device using the 

**794** 

**Chapter 17: Interrupt Support** 

pins can work in a PCIe system; the bridge translates the assertion of a pin into an interrupt emulation message (INTx) going upstream to the Root Complex. The expectation is that PCIe devices would not normally need to use the INTx messages but, at the time of this writing, in practice they often do because sys‐ tem software has not been updated to support MSI. 

_Figure 17‐1: PCI Interrupt Delivery_ 

**— MSI I nterrupt Delivery** MSI eliminates the need for sideband signals by using memory writes to deliver the interrupt notification. The term “Message Signaled Interrupt” can be confusing because its name includes the term “Mes‐ sage” which is a type of TLP in PCIe, but an MSI interrupt is a Posted Memory Write instead of a Message transaction. MSI memory writes are distinguished from other memory writes only by the addresses they target, which are typi‐ cally reserved by the system for interrupt delivery (e.g., x86‐based systems tra‐ ditionally reserve the address range FEEx_xxxxh for interrupt delivery). 

Figure 17‐2 illustrates the delivery of interrupts from various types of PCIe devices. All PCIe devices are required to support MSI, but software may or may not support MSI, in which case, the INTx messages would be used. Figure 17‐2 also shows how a PCIe‐to‐PCI Bridge is required to convert sideband interrupts from connected PCI devices to PCIe‐supported INTx messages. 

**795** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 17‐2: Interrupt Delivery Options in PCIe System_ 

**==> picture [370 x 274] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>Interrupt Controller<br>INTx<br>MSI or Message<br>INTx Message<br>PCIe<br>Switch<br>MSI or MSI or Bridge<br>INTx Message INTx Message to PCI<br>or PCI-X<br>INTx#<br>PCIe Legacy<br>PCI/PCI-X<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


## **The Legacy Model** 

## **General** 

To illustrate the legacy interrupt delivery model, refer to Figure 17‐3 on page 797 and consider the usual steps involved in interrupt delivery using the legacy method of interrupt pins: 

1. The device generates an interrupt by asserting its pin to the controller. In older systems this controller was typically an Intel 8259 PIC that had 15 IRQ inputs and one INTR output. The PIC would then assert INTR to inform the CPU that one or more interrupts were pending. 

**796** 

**Chapter 17: Interrupt Support** 

2. Once the CPU detects the assertion of INTR and is ready to act on it, it must identify which interrupt actually needs service, and that is done by the CPU issuing a special command on the processor bus called an Interrupt Acknowledge. 

3. This command is routed by the system to the PIC, which returns an 8‐bit value called the Interrupt Vector to report the highest priority interrupt cur‐ rently pending. A unique vector would have been programmed earlier by system software for each IRQ input. 

4. The interrupt handler then uses the vector as an offset into the Interrupt Table (an area set up by software to contain the start addresses of all the Interrupt Service Routines, ISRs), and fetches the ISR start address it finds at that location. 

5. That address would point to the first instruction of the ISR that had been set up to handle this interrupt. This handler would be executed, servicing the interrupt and telling its device to deassert its INTx# line and then would return control to the previously interrupted task. 

_Figure 17‐3: Legacy Interrupt Example_ 

**==> picture [304 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTR<br>CPU Memory<br>5<br>Interrupt Service<br>Interrupt<br>Vector Routine (ISR)<br>Acknowledge<br>4<br>North Bridge<br>Interrupt Table (ISR<br>starting addresses)<br>PCI Bus<br>2 3<br>Bridge<br>Data Buffer<br>South Bridge<br>PCI Bus<br>1<br>Interrupt Controller<br>(PIC) INTA#<br>Device<br>**----- End of picture text -----**<br>


**797** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Changes to Support Multiple Processors** 

This model works well for single‐CPU systems, but has a limitation that makes it sub‐optimal in a multi‐CPU system. The problem is that the INTR pin can only be connected to one CPU. If multiple processors are present then only one of them will see the interrupts and will have to service them all while the other CPUs won’t see any of them. To obtain the best performance, such systems really need an even distribution of the system tasks across all the processors, referred to as SMP (Symmetric Multi‐Processing) but the pin model won’t sup‐ port it. 

To achieve better SMP, a new model was needed, and toward this end the PIC was modified to become the IO APIC (Advanced Programmable Interrupt Con‐ troller). The IO APIC was designed to have a separate small bus, called the APIC Bus, over which it could deliver interrupt messages, as shown in Figure 17‐4 on page 799. In this model, the message contained the interrupt vector number, so there was no need for the CPU to send an Interrupt Acknowledge down into the IO world to fetch it. The APIC Bus connected to a new internal logic block within the processors called the Local APIC. The bus was shared among all the agents and any of them could initiate messages on it but, for our purposes, the interesting part is its use for interrupt delivery from peripherals. Those interrupts could now be statically assigned by software to be serviced by different CPUs, multiple CPUs or even dynamically assigned by the IO APIC. 

**798** 

**Chapter 17: Interrupt Support** 

_Figure 17‐4: APIC Model for Interrupt Delivery_ 

**==> picture [316 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Local Local<br>APIC APIC<br>CPU CPU<br>Memory<br>APIC<br>bus North Bridge<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>PCI Bus<br>Interrupt Controller<br>(IO APIC) INTA#<br>Device<br>**----- End of picture text -----**<br>


That model, known as the APIC model, was sufficient for several years but still depended on sideband pins from the peripheral devices to work. Another limi‐ tation of this model was the number of IRQs (interrupt request lines) into the IO APIC. Without a very large number of IRQs, peripheral devices had to share IRQs which means added latency anytime that IRQ is asserted because there could be multiple devices that could have asserted it and software must evalu‐ ate all of them. This technique of linking multiple ISRs together was often referred to as interrupt chaining. Eventually, because of this issue and a couple other minor issues, another improvement came along. 

Why not have the peripheral devices themselves send interrupt messages directly to the Local APICs? All that is needed is a communications path which already exists in the form of the PCI bus and the processor bus. So the APIC bus was eliminated and all interrupts were delivered to the Local APICs in the form of memory writes, referred to as MSIs or Message Signaled Interrupts. These MSIs were targeting a special address that the system understood to be an inter‐ rupt message targeting the Local APICs. (This special address address was tra‐ 

**799** 

**PCI Ex ress 3.0 Technolo p gy** 

ditionally FEEx_xxxxh for x86‐based systems.) Even the IO APIC was programmed to send its interrupt notifications over the ordinary data bus using memory writes (MSI). Now it simply sends an MSI memory write across the data bus targeting the memory address of the desired processor’s Local APIC, and that has the effect of notifying the processor of the interrupt. 

This model is known as the xAPIC model, and since it is not based on sideband signals which go into an interrupt controller with a limited number of inputs, the need to share interrupts is almost eliminated. More information can be found about this model in “An MSI Solution” on page 827. 
