sent in one time slot? The answer depends on speed and Link width, or course. At 5.0 Gb/s it takes 2ns to send each 10‐bit symbol, so 50 symbols can be deliv‐ ered per Lane in 100ns. If the packet size is 512 bytes of data plus another 28 or so for the header, then 11 time slots would be needed to deliver 550 symbols for one packet using a x1 Link. It is possible to give one port several contiguous 

**279** 

## **PCI Ex ress Technolo p gy** 

slots if needed, so that’s one solution. Since the packet size that will be sent is always the same, we can’t really program 2.5 instances of it, so we’d have to use 3 instead. From our equation, 3 instances of 512 bytes each results in an actual bandwidth of 120MB/s. That’s higher than we need, but it solves the problem. The number of time slots used would then be 11 x 3 = 33, leaving 95 for other use in the Service Interval. Each group of 11 time slots would need to be contig‐ uous but the groups could be spaced out over the service interval. 

Another solution would be increase the Link width. Although the hardware would cost more, using 11 Lanes would allow delivery of all the data in one time slot. The CEM spec doesn’t currently support a x11 option, but a x12 option is available and would work for our example. Using a wide Link like that means software would only need to program one time slot for each packet, and just three over the whole service interval to support isochronous traffic for this device. Unlike the x1 case, now we wouldn’t need contiguous time slots. Instead, they could be spaced over the service interval in some optimal fashion. 

**Bandwidth Allocation Problems.** The TBWRR table must be pro‐ grammed to guarantee sufficient timely bandwidth for isochronous traffic, and that other traffic won’t be allowed to interfere. In Figure 7‐25 on page 279, the SCSI controller is shown as sending one packet in SI 1 and another in SI 3. If the timing was such that one packet from that endpoint per SI was allowed then this works fine. 

Now let’s say the SCSI controller attempts to inject more packets than it has permission to do in SI 1, illustrated in Figure 7‐26 on page 280. This is the first of two bandwidth allocation problems mentioned in the spec and is called “oversubscription.” This could interfere with isochronous traffic flow, but programming the TBWRR table readily avoids that problem because the arbitration only allows a packet from that port at specific times. If more packets from that port are queued up, they simply have to wait until the next available time, which might be in SI 2, as shown in this exam‐ ple. Eventually, this can result in flow control back‐pressure at the sending agent 

_Figure 7‐26: Over‐Subscribing the Bandwidth_ 

**==> picture [263 x 94] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**280** 

**Chapter 7: Quality of Service** 

The second timing problem is called “congestion” and happens when too many isochronous requests are sent within a given time window, as shown in Figure 7‐27 on page 281. This is a similar problem but now there is no simple solution. Unlike the previous case, postponing high‐priority packets until another time slot is not an option, so the system must make an effort to handle them all. The result is that some requests may experience excessive service latencies. To correct this, software would need to change the distri‐ bution of packets so that they can be supported by the available hardware bandwidth. 

_Figure 7‐27: Bandwidth Congestion_ 

**==> picture [263 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**Latency Issues .** Managing latency for packet delivery is an important part of isochrony, and involves the combination of the fabric latency and the Completer latency. Fabric latency depends on all the characteristics of the Link between the various components in the system, especially the Link width and frequency of operation. A simple way to minimize this value is to constrain the complexity of the PCIe topology for isochronous paths. Completer latency depends on the target endpoint internal characteristics, such as memory speed and internal arbitration. 

## **Root Complex** 

The RC has the same arbitration and timing requirements as a switch. It receives packets on several downstream ports and forwards them to the target in a way that’s consistent with the rules for isochrony described earlier. However, much of how this is done will be vendor specific because the spec doesn’t define the RC or how it should be programmed. 

**Problem: Snooping.** One interesting thing affecting timing and latency in the root that we haven’t yet discussed is the process of snooping. Normally, anytime an access to system memory takes place it will be to a location that the processor considers cacheable, meaning it has permission to store a tem‐ 

**281** 

**PCI Ex ress Technolo p gy** 

porary copy in its local caches. If an external device attempts to accesses that area of memory, the chipset must first check the processor caches before allowing the access because a cached copy may have been modified. If so, the modified data will need to be written back to memory before it will be available for the device access. Although it’s necessary to ensure memory coherency, the problem is that snooping takes time. How long it takes is typically bounded but not predictable because it depends on what else the CPUs are doing at that time. Depending on the timing require‐ ments, that kind of uncertainty could ruin an isochronous data flow. 

**Snooping Solutions.** One way to avoid snooping is for devices to only access areas of memory that have been designated as uncacheable. Another option is for software to set the “No Snoop” attribute bit in the high‐priority packet headers. That forces the chipset to skip the snoop step regardless of the memory type and go directly to memory because software has guaran‐ teed that doing so won’t cause a problem. To enforce this as a requirement for the isochronous path, another bit can be initialized by hardware in the root port for the high‐priority VC called “Reject Snoop Transactions” (see the VC Resource Capability Register in Figure 7‐17 on page 265). The pur‐ pose of this is to allow only transactions for that VC that have the No Snoop attribute set. Any incoming packets that don’t have it set are discarded to ensure that the timing will never be violated by waiting for a snoop. 

## **Power Management** 

It’s a simple observation, but if timing is important for a path in PCIe, then power management (PM) mechanisms for devices in that path will need to han‐ dled carefully. Configuration software can read the latencies associated with every PM condition and select those cases that the timing budget will permit. The simplest approach, though, would just be to disable all PM options in an isochronous path. Fortunately, this is easily done using existing configuration registers. Devices can be placed into the device state D0 and left there, while the hardware‐controlled Link PM mechanism can be disabled (for more on PM, see Chapter 16, entitled ʺPower Management,ʺ on page 703). 

## **Error Handling** 

Finally, there is one last issue: what to do when errors occur on the Link. The ACK/NAK protocol, covered in Chapter 7, provides an automatic, hardware‐ based retry mechanism to correct packets that encounter transmission prob‐ lems. This otherwise desirable feature presents a problem for isochrony because it takes time to do it. And how long it takes to resolve an error can vary widely depending on things like how the problem was detected. 

**282** 

**Chapter 7: Quality of Service** 

To decide this question we have to know how much time uncertainty the sys‐ tem can tolerate and still deliver isochronous data. If the latency budget is too tight, there simply won’t be time for retrying failed packets and the ACK/NAK protocol will have to be disabled. Interestingly, the spec writers evidently didn’t consider that possibility because no configuration bits are included for dis‐ abling it or deciding how to handle packets that would have been retried but now won’t be. Therefore disabling this will require non‐standard mechanisms like vendor‐specific registers. 

If there _isn’t_ enough time available for retries, the target agent may simply choose to discard any bad packets. Another option would be to use the bad packets as they are, errors and all. For some applications using isochronous support that isn’t as counter‐intuitive as it sounds. An error in video streaming, for example, might cause an occasional glitch on the display, but that could be considered an acceptable risk. 

If there _is_ enough time in the Service Interval to allow retries, a limit could be placed on the possible latency they might add by adding a timer to track the time until the end of the Service Interval and use that to decide whether a retry could be attempted. Errors shouldn’t happen very often, of course, so this might be sufficient to correct the occasional transmission fault while still maintaining isochronous timing. 

**283** 

**PCI Ex ress Technolo p gy** 

**284** 

## _**8**_ 

## _**Transaction Ordering**_ 

## **The Previous Chapter** 

The previous chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different packets traversing the fabric. These mechanisms include application‐specific software that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **This Chapter** 

This chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock condi‐ tions that must be avoided. 

## **The Next Chapter** 

The next chapter describes, Data Link Layer Packets (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power manage‐ ment, flow control mechanism and can be used for vender defined purposes. 

## **Introduction** 

As with other protocols, PCI Express imposes ordering rules on transactions of the same traffic class (TC) moving through the fabric at the same time. Transac‐ tions with different TCs do not have ordering relationships. The reasons for these ordering rules related to transactions of the same TC include: 

- Maintaining compatibility with legacy buses (PCI, PCI‐X, and AGP). 

- • Ensuring that the completion of transactions is deterministic and in the sequence intended by the programmer. 

**285** 

**PCI Ex ress 3.0 Technolo p gy** 

- Avoiding deadlock conditions. 

- Maximize performance and throughput by minimizing read latencies and managing read and write ordering. 

Implementation of the specific PCI/PCIe transaction ordering is based on the following features: 

1. Producer/Consumer programming model on which the fundamental order‐ ing rules are based. 

2. Relaxed Ordering option that allows an exception to this when the Requester knows that a transaction does not have any dependencies on pre‐ vious transactions. 

3. ID Ordering option that allows a switches to permit requests from one device to move ahead of requests from another device because unrelated threads of execution are being performed by these two devices. 

4. Means for avoiding deadlock conditions and supporting PCI legacy imple‐ mentations. 

## **Definitions** 
