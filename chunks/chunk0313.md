When an Error Message is received by the Root, the action it takes is determined in part by the settings in the Root Control Register. Figure 15‐18 depicts this reg‐ ister and highlights the three fields that specify whether a received Error Mes‐ sage should be reported as System Error. In some x86‐based systems, it’s likely that an NMI (Non‐Maskable Interrupt) will be signaled if the error is enabled to trigger a System Error. 

Other options for reporting Error Messages are not configurable via standard registers. The most likely scenario is that an interrupt will be signaled to the processor that will call an Error Handler, which may log the error and attempt to clear the problem. 

**682** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐18: Root Control Register_ 

**==> picture [313 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 5 4 3 2 1 0<br>RsvdP<br>CRS Software Visibility Enable<br>PME Interrupt Enable<br>System Error on Fatal Error Enable<br>System Error on Non-Fatal Error Enable<br>System Error on Correctable Error Enable<br>**----- End of picture text -----**<br>


## **Link Errors** 

Link failures are typically detected in the Physical Layer and communicated to the Data Link Layer. For a downstream device, if the link has incurred a Fatal error and is not operating correctly, it can’t report the error to the host. For these cases, the error must be reported by the upstream device. If software can isolate errors to a given link, one step in handling an uncorrectable error (or to prevent future uncorrectable errors) is to retrain the Link. The Link Control Register includes a bit that allows software to force the Link to retrain, as shown inFig‐ ure 15‐19 on page 684. If that solves the problem, operation resumes with little downtime. 

**683** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐19: Link Control Register ‐ Force Link Retraining_ 

**==> picture [297 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


Having once requested retraining, software can poll the _Link Training_ bit in the Link Status Register to see when training has completed. Figure 15‐20 high‐ lights this status bits. When this bit is 1b, the Link is still in the retraining pro‐ cess (or has yet to start retraining). Hardware will clear this bit once the Physical Layer reports the Link as active meaning the training process has completed successfully. 

**684** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐20: Link Training Status in the Link Status Register_ 

**==> picture [360 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


## **Advanced Error Reporting (AER)** 

The Advanced Error Reporting Structure illustrated in Figure 15‐21 on page 686 allows for much more sophisticated error handling. These registers provide several additional features: 

- Better granularity in logging the actual type of error that occurred 

- Control to specify the severity of each uncorrectable error type 

- Support for logging the header of packets that had errors 

- Standardizing control for the Root to report received Error Messages with an interrupt 

- Identifying the source of the error in the PCIe topology 

- Ability to mask reporting individual types of errors 

**685** 

## **PCI Ex ress Technolo p gy** 

_Figure 15‐21: Advanced Error Capability Structure_ 

|Root Ports &<br>Root Complex<br>Event Collectors<br>Functions<br>that support<br>TLP Prefixes|Root Error Command<br>Root Error Status<br>Uncorr.  Error Source ID<br>Corr.  Error Source ID<br>TLP Prefix Log Register<br>00h<br>04h<br>08h<br>0Ch<br>10h<br>14h<br>18h<br>1Ch<br>2Ch<br>30h<br>34h<br>38h<br>PCIe Extended CapabilityRegister<br>Uncorrectable Error Status Register<br>Uncorrectable Error Mask Register<br>Uncorrectable Error SeverityRegister<br>Correctable Error Status Register<br>Correctable Error Mask Register<br>Advanced Error Capability and Control Register<br>Header Log Register|
|---|---|



## **Advanced Error Capability and Control** 

Let’s begin our discussion of AER by looking at the Advanced Error Capability and Control register. End‐to‐End CRC (ECRC) generation and checking requires AER, and this register, shown in Figure 15‐22 on page 687, reports 

**686** 

**Chapter 15: Error Detection and Handling** 

whether this device supports it. If so, configuration software can enable (and force) its use by setting the appropriate bits. 

The five low‐order bits of this register contain the First Error Pointer, set by hardware when the Uncorrectable Error status bits are updated. There are 32 status bits and the First Error Pointer indicates which of the unmasked, Uncor‐ rectable Errors was detected first, meaning which status bit was set when all the other status bits were still 0. The first error is the most interesting because the others may have been caused by the first one. 

_Figure 15‐22: The Advanced Error Capability and Control Register_ 

|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|_Figure 15‐22: The Advanced Error Capability and Control Register_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||
|RsvdP<br>ECRC Check Enable(RWS)<br>ECRC Check Capable(RO)<br>ECRC Generation Enable(RWS)<br>ECRC Generation Capable(RO)<br>Multiple Header Recording Capable(RO)<br>Multiple Header Recording Enable(RWS<br>TLP Prefix Log Present(ROS)<br>31|||||First Error<br>Pointer (ROS)<br><br>)<br>0<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12|||||||||
||RsvdP||||||||||||First Error<br>Pointer (ROS)|
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||
|||||||||||||||



Beginning with the 2.1 spec revision, this capability was enhanced to allow tracking multiple errors. For that reason, if multiple error status bits have been set and cleared, the meaning really becomes more like an “Oldest Error Pointer” instead. The pointer is updated by hardware when the corresponding status bit is cleared by software, at which time it points to whichever error was detected next (see Figure 15‐25 on page 691 for the list of uncorrectable errors). Interestingly, the next error may be the same one again if that error had been detected multiple times, with the result that the updated pointer still indicates the same value. 

Since multiple errors can be recorded in the Uncorrectable Status register, it would be very helpful to store multiple headers, too. Hardware must be designed to log at least one header, but is allowed to support more. If it does, the Multiple Header Recording Capable bit will be set and the Multiple Header Recording Enable bit can be used to enable storing more than one. Whenever the First Error Pointer indicates a status bit position that is not set or is not implemented, it means there are no more uncorrectable errors to service. 

**687** 

**PCI Ex ress Technolo p gy** 

The last bit in this register, TLP Prefix Log Present, indicates whether the TLP Prefix Log registers contain valid information for the uncorrectable error indi‐ cated by the First Error Pointer. 

The fields in this register and the other AER registers have various characteris‐ tics, which are abbreviated as follows: 

- RO — Read Only, set by hardware 

- ROS — Read Only and Sticky (see the next section on sticky bits) 

- RsvdP ‐ Reserved and Preserved. These bits must not be used for any pur‐ pose, but software must be careful to maintain whatever values they con‐ tain. 

- RsvdZ ‐ Reserved and Zero. Bits that must not be used for any purpose and must always be written to zeros. 

- RWS — Readable, Writeable and Sticky 

- • RW1CS — Readable, Write 1 to Clear, and Sticky 

## **Handling Sticky Bits** 

Several AER register fields employ sticky bits, which means that a reset won’t clear their contents. All other register fields are forced to default values on a reset, but these are not. This is a good idea because a Link may encounter a fail‐ ure that can’t be cleared without a reset. If the problem is in the downstream device of the failed Link, its register contents are unavailable until the Link is working again, which the reset will accomplish. But if the registers were cleared by the reset then the information is lost. To solve this problem, sticky bits keep error status information available through a reset. Specifically, sticky bits will survive an FLR (Function Level Reset), a Hot Reset, and a Warm Reset because power is available to keep them active. They may even survive a Cold Reset if a secondary power source like Vaux is available to keep them active when the main power is shut off. 

## **Advanced Correctable Error Handling** 

Advanced Error Reporting provides the ability to record which specific correct‐ able errors have been detected. These errors can be used to initiate a Correctable Error Message to the host system. Although system operation continues nor‐ mally, reporting correctable errors can be useful because it allows system soft‐ ware to see which components are having trouble and to predict whether they may fail completely in the future. 

**688** 

**Chapter 15: Error Detection and Handling** 

## **Advanced Correctable Error Status** 

Correctable errors will automatically set the corresponding bit in the Advanced Correctable Error Status register, shown in Figure 15‐23 on page 689, regardless of whether the error is reported with an Error Message. These bits are cleared by software writing a “1” to the bit position, hence the designation RW1CS. 

_Figure 15‐23: Advanced Correctable Error Status Register_ 

|31|31||16|15|14|13|12|11|9|8|8|7|7|6|6|5||1|0|0||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||RsvdZ||||||RsvdZ|||||||||RsvdZ|||||
|||Header Log Overflow Status||||||||||||||||||||
|||Corrected Internal Error Status||||||||||||||||||||
|||Advisory Non-Fatal Error Status||||||||||||||||||||
|||Replay Timer Timeout Status||||||||||||||||||||
|||REPLAY_NUM Rollover Status||||||||||||||||||||
|||Bad DLLP Status||||||||||||||||||||
|||Bad TLP Status||||||||||||||||||||
|||Receiver Error Status||||||||||||||||||||
||||Note: all bits designated RW1CS|||||||||||||||||||


