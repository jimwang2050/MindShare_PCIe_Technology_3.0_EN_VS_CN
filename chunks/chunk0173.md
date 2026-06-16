## **Quality of Service (QoS)** 

PCIe was designed from its inception to be able to support time‐sensitive trans‐ actions for applications like streaming audio or video where data delivery must be timely in order to be useful. This is referred to as providing Quality of Ser‐ vice and is accomplished by the addition of a few things. First, each packet is assigned a priority by software by setting a 3‐bit field within it called Traffic Class (TC). Generally speaking, assigning a higher‐numbered TC to a packet is expected to give it a higher priority in the system. Second, multiple buffers, called Virtual Channels (VC), are built into the hardware for each port and a packet is placed into the appropriate buffer based on its TC. Third, since a port now has multiple buffers with packets available for transmission at a given time, arbitration logic is needed to select among the VCs. Finally, Switches must select between competing input ports for access to the VCs of a given output port. This is called Port Arbitration and can be hardware assigned or software programmable. All of these hardware pieces must be in place to allow a system to prioritize packets. If properly programmed and set up, such a system can even provide guaranteed service for a given path. 

To illustrate the concept, consider Figure 2‐22 on page 71, in which a video cam‐ era and SCSI device both need to send data to system DRAM. The difference is that the camera data is time critical; if the transmission path to the target device is unable to keep up with its bandwidth, frames will get dropped. The system needs to be able to guarantee a bandwidth that’s at least as high as the camera or the captured video may appear choppy. At the same time, the SCSI data needs to be delivered without errors, but how long it takes is not as important. Clearly, then, when both a video data packet and a SCSI packet need to be sent at the same time, the video traffic should have a higher priority. QoS refers to the abil‐ ity of the system to assign different priorities to packets and route them through the topology with deterministic latencies and bandwidth. For more detail on QoS, refer to Chapter 7, entitled ʺQuality of Service,ʺ on page 245. 

**70** 

**Chapter 2: PCIe Architecture Overview** 

_Figure 2‐22: QoS Example_ 

**==> picture [368 x 314] intentionally omitted <==**

**----- Start of picture text -----**<br>
Intel Processor<br>System<br>Memory<br>PCIe<br>Uncore<br>GFX<br>QPI<br>IOH Root Complex<br>10 Gb<br>LAN Switch Ethernet Switch Fibre<br>Endpoint Channel<br>Endpoint Endpoint<br>10 Gb PCI Express SAS/SATA<br>Add-In Switch Ethernet to-PCI<br>RAID<br>Endpoint Endpoint<br>Endpoint<br>PCI<br>Add-In EthernetGb IEEE Slots<br>Isochronous Ordinary 1394<br>Traffic Endpoint Endpoint Traffic<br>**----- End of picture text -----**<br>