Transaction ordering is managed within Virtual Channel buffers. These buffers are grouped into Posted, Non‐Posted, and Completion transactions, and flow control is managed independently for each group. That makes weak ordering more useful because, as in our example, even if one buffer was full, others could still have space available. 

## **ID Based Ordering (IDO)** 

Another opportunity for optimizing ordering and improving performance is related to the nature of traffic streams. Packets from different requesters are very unlikely to have dependencies; after all, one device could hardly know when the other had finished certain steps based on ordering because they could have different paths to their shared resource. Bearing this in mind, the 2.1 revi‐ sion of the PCIe spec introduced what is called ID‐based Ordering to improve performance. 

## **The Solution** 

If the packet source isn’t taken into account for transaction ordering then perfor‐ mance can suffer, as shown in Figure 8‐7 on page 302. In the illustration, trans‐ action 1 makes it way to the upstream port of the switch but is blocked from further progress by a buffer‐full condition for that packet type in the Root port (which would be indicated by insufficient Flow Control credits). To use the spec terminology, packets from the same Requester are called a TLP stream. In this example, the path shown for Transaction 1 might include several TLPs as part of a TLP stream. Transaction 2 then arrives at the same egress port and is also blocked from moving forward because it must stay in order with Transaction 1. Since the packets came from different sources, (different TLP streams) this delay is almost certainly unnecessary; it’s very unlikely they could have depen‐ dencies between them, but the normal ordering model doesn’t take this into account. To get improved performance, we need another option. 

The solution is simple: allow packets to be reordered if they don’t use the same Requester ID (or Completer ID, for Completion packets). This optional capabil‐ ity allows software to enable a device to use IDO and a switch port can recog‐ nize that the packets are part of different TLP streams. This is done by setting the enable bits in Device Control 2 Register. 

**301** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 8‐7: Different Sources are Unlikely to Have Dependencies_ 

**==> picture [151 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Write Buffer Root<br>Full<br>ey<br>Switch<br>ty a ONO<br>®<br>Posted Write<br>| [7] [le ma"<br>sd Cle fl PCle ff Legacy<br>**----- End of picture text -----**<br>


## **When to use IDO** 

The spec highly recommends that both IDO and RO be used whenever safely possible. For example, it should be safe for Endpoints to use IDO for all TLPs when communicating directly with only one other entity, such as the Root Com‐ plex. On the other hand, it would not be safe to use it if the Endpoint is commu‐ nicating with multiple agents. An example failure case for this from the spec begins with one device doing a DMA write to memory and then doing a peer‐ to‐peer write to a flag in another device. When the second device receives the flag, it also initiates a DMA write to the same area of memory. Normally, the two DMA operations would stay in order, but with IDO that ordering can’t be guaranteed because upstream devices will see them as coming from different device IDs. Similarly, it would not be safe to use RO with packets that are involved in control traffic. 

For Completers, if IDO is enabled it’s recommended that it be used for all Com‐ pletions unless there is a specific reason not to do so. 

**302** 

**Chapter 8: Transaction Ordering** 

## **Software Control** 

Software can enable the use of IDO for Requests or Completions from a given port by setting the appropriate bits in its Device Control 2 Register. As with RO, there are no capability bits to let software find out what the device supports, just enable bits, so software would need to know by some other means that the device was capable of doing this. These bits enable the use of IDO for that packet type, but software must still decide whether each individual packet will have its IDO bit set. A new attribute bit in the header indicates whether a TLP is using IDO, as shown in Figure 8‐8 on page 303. This brings up another related point: Completions normally inherit all the attribute bits of the Request that generated them, but this may not be true for IDO, since this can be enabled independently by the Completer. In other words, Completions may use IDO even if the Request that initiated them did not. 

_Figure 8‐8: IDO Attribute in 64‐bit Header_ 

**==> picture [313 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- End of picture text -----**<br>


## **Deadlock Avoidance** 

Because the PCI bus employs delayed transactions or because PCI Express memory read request may be blocked due to lack of flow control credits, several deadlock scenarios can develop. These deadlock avoidance rules are included in PCI Express ordering to ensure that no deadlocks occur regardless of topol‐ ogy. Adhering to the ordering rules prevent problems when boundary condi‐ tions develop due to unanticipated topologies (e.g., two PCI Express to PCI bridges connected across the PCI Express fabric). Refer to the MindShare book entitled _PCI System Architecture, Fourth Edition (_ published by Addison‐Wesley) for a detailed explanation of the scenarios that are the basis for the PCI Express 

**303** 

## **PCI Ex ress 3.0 Technolo p gy** 

ordering rules related to deadlock avoidance. Table 8‐1 on page 289 lists the deadlock avoidance ordering rules which are identified as entries A3, A4, D3, D4 and A5b. Note that avoiding the deadlocks involves “Yes” entries in each of these 5 cases. If blocking occurs due to lack of flow control credits associated with the Non‐Posted Request buffer identified in column 3 or 4, the Posted Requests associated with row A or the Completions associated with row D must be moved ahead of the Non‐Posted Requests specified in the column 3 or 4 where the “Yes” entry exists. Note also that the “Yes” entry in A5b applies only to PCI Express to PCI or PCI‐X Bridges. 

Essentially, this deadlock avoidance rule can be summarized as “later arriving Memory Write Requests or Completions must be allowed to pass earlier blocked Non‐Posted Requests otherwise a deadlock could result”. 

**304** 

## Part Three: 

Data Link Layer 

## _**9**_ 

## _**DLLP Elements**_ 

## **The Previous Chapter** 

The previous chapter discussed the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI, and the Producer/ Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible dead‐ lock conditions that must be avoided, but did not include any means to avoid the performance problems that could result. 

## **This Chapter** 

In this chapter we describe the other major category of packets, _Data Link Layer Packets_ (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power management, flow control mechanism and can even be used for vendor‐defined purposes. 

## **The Next Chapter** 

The following chapter describes a key feature of the Data Link Layer: an auto‐ matic, hardware‐based mechanism for ensuring reliable transport of TLPs across the Link. Ack DLLPs confirm good reception of TLPs while Nak DLLPs indicate a transmission error. We describe the normal rules of operation when no TLP or DLLP error is detected as well as error recovery mechanisms associ‐ ated with both TLP and DLLP errors. 

## **General** 

The Data Link Layer can be thought of as managing the lower level Link proto‐ col. Its primary responsibility is to assure the integrity of TLPs moving between devices, but it also plays a part in TLP flow control, Link initialization and power management, and conveys information between the Transaction Layer above it and the Physical Layer below it. 

**307** 

**PCI Ex ress Technolo p gy** 

In performing these jobs, the Data Link Layer exchanges packets with its neigh‐ bor known as Data Link Layer Packets (DLLPs). DLLPs are communicated between the Data Link Layers of each device. Figure 9‐1 on page 308 illustrates a DLLP exchanged between devices. 

_Figure 9‐1: Data Link Layer Sends A DLLP_ 

**==> picture [342 x 298] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>Framing C Framing<br>DLLP R<br>(SDP) C (END)<br>**----- End of picture text -----**<br>


## **DLLPs Are Local Traffic** 

DLLPs have a simple packet format and are a fixed size, 8 bytes total, including the framing bytes. Unlike TLPs, they carry no target or routing information because they are only used for nearest‐neighbor communications and don’t get routed at all. They’re also not seen by the Transaction Layer since they’re not part of the information exchanged at that level. 

**308** 

**Chapter 9: DLLP Elements** 

## **Receiver handling of DLLPs** 

When DLLPs are received, several rules apply: 

1. They’re immediately processed at the Receiver. In other words, their flow cannot be controlled the way it is for TLPs (DLLPs are not subject to flow control). 

2. They’re checked for errors; first at the Physical Layer, and then at the Data Link Layer. The 16‐bit CRC included with the packet is checked by calculat‐ ing what the CRC should be and comparing it to the received value. DLLPs that fail this check are discarded. How will the Link recover from this error? DLLPs still arrive periodically, and the next one of that type that succeeds will update the missing information. 

3. Unlike TLPs, there’s no acknowledgement protocol for DLLPs. Instead, the spec defines time‐out mechanisms to facilitate recovery from failed DLLPs. 

4. If there are no errors, the DLLP type is determined and passed to the appro‐ priate internal logic to manage: 

   - Ack/Nak notification of TLP status 

   - Flow Control notification of buffer space available 

   - Power Management settings 

   - Vendor specific information 

## **Sending DLLPs** 

## **General** 

These packets originate at the Data Link Layer and are passed to the Physical Layer. If 8b/10b encoding is in use (Gen1 and Gen2 mode), framing symbols will be added to both ends of the DLLP at this level before the packet is sent. In Gen3 mode, a SDP token of two bytes is added to the front end of the DLLP, but no END is added to the end of the DLLP. Figure 9‐2 on page 310 shows a generic (Gen1/Gen2) DLLP in transit, showing the framing symbols and the general contents of the packet. 

**309** 

**PCI Ex ress Technolo p gy** 

_Figure 9‐2: Generic Data Link Layer Packet Format_ 

**==> picture [360 x 313] intentionally omitted <==**

**----- Start of picture text -----**<br>