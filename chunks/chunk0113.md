## **PCI Interrupt Handling** 

PCI devices use one of four sideband interrupt signals (INTA#, INTB#, INTC#, or INTD#) to send an interrupt request to the system. When one of the pins is asserted, the interrupt controller in a single‐CPU system responded by asserting the INTR (interrupt request) pin to the CPU. Later multi‐CPU designs needed to improve on the single wire input for interrupts and changed to an APIC (Advanced Programmable Interrupt Controller) model, in which the controller sends a message to the multiple CPUs instead of asserting the INTR pin to one of them. Regardless of the delivery model, an interrupted CPU must determine the source of the interrupt and then service the interrupt. The legacy model required several bus cycles for this and wasn’t very efficient. The APIC model is better but also leaves room for improvement. 

**23** 

**PCI Ex ress Technolo p gy** 