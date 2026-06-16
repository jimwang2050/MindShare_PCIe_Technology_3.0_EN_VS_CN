## **Message Signaled Interrupts** 

PCI‐X devices require MSI (Message Signaled Interrupt) capability, which was developed as a way to reduce or eliminate the need to share interrupts across multiple devices as was typically required in the legacy interrupt architecture. 

**34** 

**Chapter 1: Background** 

To generate an interrupt request using MSI, a device initiates a memory write transaction using a pre‐defined address range that is understood to be an inter‐ rupt which should be delivered to one of more CPUs, and the data is a unique interrupt vector associated with that device. The CPU, armed with the interrupt number, is able to immediately jump to the interrupt service routine for the device and avoids the overhead associated with finding which device generated the interrupt. In addition, no sideband pins are needed. 