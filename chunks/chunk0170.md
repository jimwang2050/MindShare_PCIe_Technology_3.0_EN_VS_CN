## **PCI Ex ress Technolo p gy** 

Those Completion packets also contain routing information to direct them back to the Requester, and the Requester includes its return address for this purpose in the original request. This “return address” is simply the Device ID of the Requester as it was defined for PCI, which is a combination of three things: its PCI Bus number in the system, its Device number on that bus, and its Function number within that device. This Bus, Device, and Function number information (sometimes abbreviated as BDF) is the routing information that Completions will use to get back to the original Requester. As was true for PCI‐X, a Requester can have several split transactions in progress at the same time and must be able to associate incoming completions with the correct requests. To facilitate that, another value was added to the original request called a Tag that is unique to each request. The Completer copies this transaction Tag and uses it in the Com‐ pletion so the Requester can quickly identify which Request this Completion is servicing. 

Finally, a Completer can also indicate error conditions by setting bits in the completion status field. That gives the Requester at least a broad idea of what might have gone wrong. How the Requester handles most of these errors will be determined by software and is outside the scope of the PCIe spec. 

**Locked Reads.** Locked Memory Reads are intended to support what are called Atomic Read‐Modify‐Write operations, a type of uninterruptable transac‐ tion that processors use for tasks like testing and setting a semaphore. While the test and set is in progress, no other access to the semaphore can take place or a race condition could develop. To prevent this, processors use a lock indicator (such as a separate pin on the parallel Front‐Side Bus) that prevents other trans‐ actions on the bus until the locked one is finished. What follows here is just a high level introduction to the topic. For more information on Locked transac‐ tions, refer to Appendix D called “Appendix D:  Locked Transactions” on page 963. 

As a bit of history, in the early days of PCI the spec writers anticipated cases where PCI would actually replace the processor bus. Consequently, support for things that a processor would need to do on the bus were included in the PCI spec, such as locked transactions. However, PCI was only rarely ever used this way and, in the end, much of this processor bus support was dropped. Locked cycles remained, though, to support a few special cases, and PCIe carries this mechanism forward for legacy support. Perhaps to speed migration away from its use, new PCIe devices are prohibited from accepting locked requests; it’s only legal for those that self‐identify as Legacy Devices. In the example shown in Figure 2‐19 on page 67, a Requester begins the process by sending a locked request (MRdLk). By definition, such a request is only allowed to come from the CPU, so in PCIe only a Root Port will ever initiate one of these. 

**66** 

**Chapter 2: PCIe Architecture Overview** 

The locked request is routed through the topology using the target memory address and eventually reaches the Legacy Endpoint. As the packet makes its way through each routing device (called a service point) along the way, the Egress Port for the packet is locked, meaning no other packets will be allowed in that direction until the path is unlocked. 

_Figure 2‐19: Non‐Posted Locked Read Transaction Protocol_ 

**==> picture [330 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>PCIe<br>Bridge<br>Switch Endpoint<br>to PCI<br>PCI<br>PCIe PCIe Legacy<br>Endpoint Endpoint Endpoint<br>MRdLk<br>CplDLk<br>CplDLk<br>MRdLk<br>**----- End of picture text -----**<br>

When the Completer receives the packet and decodes its contents, it gathers the data and creates one or more Locked Completions with data. These Comple‐ tions are routed back to the Requester using the Requester ID, and each Egress Port they pass through is then locked, too. 

If the Completer encounters a problem, it returns a locked completion packet without data (the original read should have resulted in data so if there isn’t any we know there’s been a problem) and the status field will indicate something about the error. The Requester will understand that to mean that the lock did not succeed and so the transaction will be cancelled and software will need to decide what to do next. 

**67** 

**PCI Ex ress Technolo p gy** 

**IO and Configuration Writes.** Figure 2‐20 on page 68 illustrates a non‐ posted IO write transaction. Like a locked request, an IO cycle can also legally target only a Legacy Endpoint. The request is routed through the Switches based on the IO address until it reaches the target Endpoint. When the Compl‐ eter receives the request, it accepts the data and returns a single completion packet without data that confirms reception of the packet. The status field in the completion would report whether an error had occurred and, if so, the Requester’s software would handle it. 

If the completion reports no errors the Requester knows that the write data has been successfully delivered and the next step in the sequence of instructions for that Completer is now permitted. And that really summarizes the motivation for the non‐posted write: unlike a memory write, it’s not enough to know that the data **will** get to the destination sometime in the future. Instead, the next step can’t logically take place until we know that it **has** gotten there. As with locked cycles, non‐posted writes can only come from the processor. 

_Figure 2‐20: Non‐Posted Write Transaction Protocol_ 

**==> picture [346 x 275] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Requester<br>Step 1: Root Initiates IOWr<br>Step 4: Root receives Cpl Root Complex<br>IOWr Cpl System<br>Memory<br>Switch A Switch C<br>IOWr<br>Cpl<br>Switch B Endpoint Endpoint Endpoint<br>IOWr Cpl<br>Completer<br>Legacy<br>Step 2: Endpoint receives IOWr<br>Endpoint<br>Endpoint Step 3: Endpoint writes data, returns Cpl<br>**----- End of picture text -----**<br>

**68** 

**Chapter 2: PCIe Architecture Overview** 