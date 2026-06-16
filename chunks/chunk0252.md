Isochronous timing is defined in PCIe by the time slot used in the Time‐Based Weighted Round Robin port arbitration scheme. At present, the time for each slot is 100ns, and represents one entry of the 128 entries in the TBWRR table. Once set up, the arbiter will repeatedly cycle through this table once every 12.8  s, which represents the overall Service Interval. 

Making an isochronous path work as intended requires a few considerations. First, the data packets must be delivered with predictable timing at regular intervals. Second, the maximum amount of isochronous data to be delivered must be known ahead of time and packets must not be allowed to exceed that limit. Third, the Link bandwidth must be sufficient to support the amount of data that needs to be delivered in a given time slot. 

**274** 

**Chapter 7: Quality of Service** 

Consider the following example. A single‐Lane Link running at 2.5 Gbps deliv‐ ers one symbol every 4ns. That allows it to send 25 symbols within a 100ns time slot, but is that enough to be useful? In many cases it’s not, because a TLP may need 28 bytes of overhead for the combination of header, sequence number, LCRC, and so forth. That would mean there isn’t even time to finish sending the overhead, much less any data payload in 100ns. If we needed to send 128 bytes of data, then the bandwidth requirement would be 128+overhead = 156 bytes. One option for solving this problem would be to increase the Link width to 8 Lanes, allowing eight times as many bytes to be sent at once. That change would deliver 200 bytes in 100ns and allow a single time slot to deliver all the isochronous data. Another solution would be to use a single Lane but give the port more time slots, since 8 time slots at the lower Link width would deliver the same amount of data. The choice of solution depends on cost and perfor‐ mance constraints, but the system designer must know the timing and band‐ width requirements of the isochronous path to be able to set it up correctly. 

## **How Timing is Enforced** 

When timing is an integral part of the proper operation of a design, as in the previous example, it is enforced by the combination of things we’ve discussed so far. First, high‐priority TCs must be selected in software and VCs set up in hardware with the mappings between them defined so that only the correct packets will be placed into the high‐priority VCs. Then the desired timing is a matter of programming the arbitration schemes to accommodate the needed bandwidth in the specified time. For example, the choice for VC arbitration would probably be the Strict Priority option, since it’s the only choice that can ensure that a high‐priority packet won’t be delayed by other packets. For Port arbitration the choice must be TBWRR to enforce timing. 

## **Software Support** 

Supporting isochronous service requires some coordination between the soft‐ ware elements in the system. In a PC system, device drivers will report isochro‐ nous requirements and capabilities to the OS, which will then evaluate the overall system demands and allocate resources appropriately. Embedded sys‐ tems will be different, because the all the pieces are known at the outset and software can be simpler. In the following discussion we’ll describe the PC case since an embedded system should simply be a simpler subset of that. 

**275** 

**PCI Ex ress Technolo p gy** 

## **Device Drivers** 

A device driver must be able to report its timing requirements to the software that oversees isochronous operation and obtain permission before trying to use isochronous packets. It’s important to note that driver‐level software should not directly change hardware assignments or arbitration policies on its own, even though it could, because the result would be chaos. If multiple drivers were each independently trying to do this, the last one to make changes would over‐ write any previous assignments. To avoid that, an OS‐level program called an Isochronous Broker receives the timing requests from the system devices and assigns system resources in a coordinated way that accommodates them all. 

## **Isochronous Broker** 

This program manages the end‐to‐end flow of isochronous packets. It receives the isochronous timing requests from device drivers and allocates system resources in a way that accommodates the requests through the target path. In the spec this is referred to as establishing an isochronous contract between the requester/completer pair and the PCIe fabric. Doing so requires verifying that the intended path can indeed support isochronous traffic, and then program‐ ming the appropriate arbitration schemes to ensure it works within the speci‐ fied timing requirements. 

## **Bringing it all together** 

By now it should be reasonably clear what needs to be done to support isochro‐ nous traffic flow in a system, but let’s look at one last example to bring all the pieces together. If we expand on the previous video capture example to show a more complex system, like the one in Figure 7‐24 on page 277, we’ll be able to discuss all the parts that must be in place if the video camera is going to be able to deliver captured data into system memory. This would be a difficult environ‐ ment for isochronous service because there are so many devices that can com‐ pete for bandwidth in the path, but that also makes it useful to illustrate the various things that must be considered. 

## **Endpoints** 

Starting at the bottom, what will be needed in the PCIe interface for the video endpoint device itself? In hardware, more than one VC will be required if we’re going to differentiate packets. Let’s assume a single‐function device for simplic‐ ity. The device driver would need to report the device capabilities and isochro‐ nous timing requirements to the OS‐level Isochronous broker, which would evaluate the system and then report back whether an isochronous contract was possible and which TCs the software should use. 

**276** 

**Chapter 7: Quality of Service** 

_Figure 7‐24: Example Isochronous System_ 

**==> picture [308 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>GFX Root Complex<br>System<br>Memory<br>Switch 2<br>Switch 1<br>Slot<br>Video SCSI<br>Camera<br>Lower<br>Time-<br>priority<br>sensitive<br>data<br>data<br>**----- End of picture text -----**<br>


The driver would then program VC numbers and map the appropriate TCs to each VC. It would also most likely program the VC arbitration to be Strict Prior‐ ity for the high‐priority channels. The one caveat here is that the arbitration must still be “fair”, meaning the low‐priority channels won’t get starved for access. That means the high‐priority VCs can’t have traffic pending constantly but instead must spread out packet injection over time. 

One other observation regarding Link operation is necessary before we finish our discussion of endpoints, and that is regarding Flow Control. The receive buffers of devices in the isochronous path must be large enough to handle the expected packet flow without causing any back pressure as long as packets are injected uniformly according to the Isochronous Contract. In addition, Flow Control Updates must be returned quickly enough to avoid stalls. 

**277** 

**PCI Ex ress Technolo p gy** 

## **Switches** 

Next, consider what would need to be present in each of the switches that reside between the endpoint and the Root Complex. Switches don’t commonly have device drivers, so it would fall to OS‐level software like the Isochronous Broker to read their configuration information and determine what service they sup‐ port. First, all the ports in the isochronous path must support more than one VC, and the TC/VC mapping must match on both ends of each Link. Remember that once the packet gets into the Transaction Layer of the Switch port, only the TC remains with the packet, and the VC assignment for that TC is specific to each port. The TC/VC mapping of the downstream port of Switch 1 must match the mapping of the endpoint, but the other switch port mappings may be differ‐ ent to match the other end of their Links. 

**Arbitration Issues.** The choices for arbitration are straight‐forward. In our example, the isochronous path is shown as carrying traffic in only one direction for simplicity. It is possible to have isochronous traffic flowing in both directions in the case of a memory read, for example, but our example was chosen to resemble the video streaming case. 

VC arbitration for the isochronous egress port will most likely need to use the Strict Priority scheme for the same reasons the endpoint does. Port arbi‐ tration will need to use the Time‐Based WRR scheme, and that means soft‐ ware must understand the proper access ratios and program the Port Arbitration Tables to implement them. This might not be as simple as it sounds if multiple switches are in the path because even though they’ll all use the same TBWRR arbitration scheme, it’s not clear how the service inter‐ vals for each of them would be coordinated. If the SIs are not aligned, mean‐ ing timing guarantees could be more difficult depending on the how busy the Links are. Coordinating the service intervals wasn’t considered in the spec, though, so it would again involve a non‐standard method. Clearly, this problem would be much simpler if we didn’t have multiple switches in an isochronous path. 

**Timing Issues.** Figure 7‐25 on page 279 shows the timing of packets being delivered by the two endpoints for our example. Packets from the video device, with a known size and delivered in regular and predictable inter‐ vals, are shown as the heavier arrows. The smaller, lighter arrows represent packets from the SCSI drive that are lower priority and whose timing is not predictable. In the endpoint, the packets simply need to have the proper TC assigned to them, but a switch needs to ensure that the proper timing policy is enforced. This is done by using TBWRR, which specifies which port will have access at a given time and for how long. Knowing the size and fre‐ 

**278** 

**Chapter 7: Quality of Service** 

quency of the isochronous packets allows software to properly arrange the timing, but what kind of timing is needed? 

_Figure 7‐25: Injection of Isochronous Packets_ 

**==> picture [269 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


First, let’s review the parameters involved by considering a simple example. Recall that PCIe bases a time slot on the reference clock period is given by the Port Capability Register 1 field called Reference Clock. At present the only option for that field is 100ns, and the TBWRR table has no options besides 128 entries. The length of the Service Interval is the multiple of those, making it 12.8  s. The bandwidth for a given device can be expressed by the equation below, where Y is the data to be delivered in one time slot (the spec states that the Max Payload Size programmed during configuration must be used for this bandwidth calculation), M is the number of time slots, and T is the overall Ser‐ vice Interval. If we choose 128 bytes as the payload, and we know that SI is 12.8  s, then the BW = 10 MB/s for each time slot allocated. 

**==> picture [79 x 28] intentionally omitted <==**

Now let’s consider a more realistic example. Let’s say that our Links are running at the Gen2 speed, that the video device needs to have a guaranteed bandwidth of 100MB/s, and that it will send 512 byte packets. Filling in the equation shows M = 2.5 instances of 512 bytes are needed. But how much data can actually be 

**==> picture [324 x 41] intentionally omitted <==**
