Both Endpoints and Root Ports are optionally allowed to act as AtomicOp Requesters and Completers, which might seem unexpected because, in PCs at least, this kind of transaction is usually only initiated by the central processor. But modern systems can include an Endpoint acting as a co‐processor, in which case it would need to be able to use AtomicOps to properly handle the protocol. All three commands support 32‐bit and 64‐bit operands, while CAS also sup‐ ports 128‐bit operands. The actual size in use will be given in the Length field in the header. Routing elements like Switch Ports and Root Ports with peer‐to‐peer access will need to support the AtomicOp routing capability to be able to recog‐ nize and route these Requests. 

A question naturally arises as to how the system (Root Complex) will be instructed to generate these new commands in response to processor activity, since there may not be a directly‐analogous processor bus command. The spec suggests two approaches. First, the Root could be designed to recognize specific processor activity and interpret that to “export” a PCIe AtomicOp in response. Second, a register‐based approach similar to the one used for legacy Configura‐ tion access could be used. In that case, one register might give the target address while another specified which command should be generated and the combina‐ tion of the two would generate the Request. 

AtomicOp Completers can be identified by the presence of the three new bits in the Device Capabilities 2 register, as shown in Figure 20‐10 on page 899. Bit 6 of this register also identifies whether routing elements are capable of routing AtomicOps. 

**898** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

Legacy PCI does not comprehend AtomicOps, of course, and there is no straight‐forward way to translate them into PCI commands. For that reason, PCIe‐to‐PCI bridges do not support AtomicOps. If atomic access is needed on that bus it would have to be done with the legacy locked protocol and the spec states that Locked Transactions and AtomicOps can operate concurrently on the same platform. 

_Figure 20‐10: Device Capabilities 2 Register_ 

**==> picture [356 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 22 21 20 19 14 13 12 11 10 9 8 7 6 5 4 3 0<br>RsvdP RsvdP<br>Max End-End<br>TLP Prefixes<br>End-End TLP<br>Prefix Supported<br>Extended Fmt<br>Field Supported<br>TPH Completer Supported<br>LTR Mechanism Supported<br>No RO-enabled PR-PR Passing<br>128-bit CAS Completer Supported<br>64-bit AtomicOp Completer Supported<br>32-bit AtomicOp Completer Supported<br>AtomicOp Routing Supported<br>ARI Forwarding Supported<br>Completion Timeout Disable Supported<br>Completion Timeout Ranges Supported<br>**----- End of picture text -----**<br>


## **TPH (TLP Processing Hints)** 

Adding hints about how the system should handle TLPs targeting memory space can improve latency and traffic congestion. The spec describes this special handling basically as providing information about which of several possible cache locations in the system would be the optimal place for a temporary copy 

**899** 

**PCI Ex ress Technolo p gy** 

of a TLP. The spec makes note of the fact that, since the usage described for TPH relates to caching, it wouldn’t usually make sense to use them with TLPs target‐ ing Non‐prefetchable Memory Space. If such usage was needed, it would be essential to somehow guarantee that caching such TLPs did not cause undesir‐ able side effects. 

## **TPH Examples** 

**Device Write to Host Read.** To help clarify the motivation for TPH, con‐ sider the example shown in Figure 20‐11 on page 901. Here the Endpoint is writing data into memory for later use by the CPU. The sequence is as follows: 

1. First, the Endpoint sends a memory write TLP containing an address that maps to the system memory. The packet gets routed to the Root Complex (RC). 

2. The RC recognizes this as an access to a cacheable memory space and pauses its progress while it snoops the CPU cache. This may result in a write‐back cycle from the CPU to update the system memory before the transaction can proceed, and this is shown as step 2a. 

3. Once any write backs have finished, the RC allows the write to update the system memory. 

4. At some point, the Endpoint notifies the CPU about data delivery. 

5. Finally, the CPU fetches the data from memory to complete the sequence. 

**900** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐11: TPH Example_ 

**==> picture [202 x 111] intentionally omitted <==**

**----- Start of picture text -----**<br>
4<br>2<br>e C)\ @ 5<br>2a<br>Roo! Complex @<br>3<br>1<br>lo [ |<br>**----- End of picture text -----**<br>


This sequence works but there’s an opportunity for performance improvement by adding an intermediate cache in the system. To illustrate this, consider the example shown in Figure 20‐12 on page 902. From the perspective of the End‐ point, the operation is the same but the knows to handle it a differently. The steps now are as follows: 

1. The Endpoint does the same memory write but this time TPH bits are included. The write is forwarded to the RC by the Switch as before. 

2. The RC understands that this memory access must be snooped to the CPU as before. However, once the snoop has been handled, the RC is informed by the TPH bits to store this TLP in an intermediate cache rather than going to system memory. 

3. The Endpoint notifies the CPU that the data item has been delivered. 4. The CPU reads from the specified address, but now the data is found in the intermediate cache and so the request does not go to system memory. This has the usual benefits we’d expect from a cache design: faster access time as well as reduced traffic for the system memory. 

**901** 

**PCI Ex ress Technolo p gy** 

This is a simple Device Write to Host Read (DWHR) example to illustrate the concept but it wouldn’t be hard to imagine a more complex system with a much larger topology in which there could be other caches placed in Switches or other locations to achieve the same benefits for other targets. 

_Figure 20‐12: TPH Example with System Cache_ 

**==> picture [108 x 75] intentionally omitted <==**

**----- Start of picture text -----**<br>
3<br>2 4<br>OC @VlEl@<br>Rant Camnlayx<br>Cache<br>1<br>**----- End of picture text -----**<br>


**Host Write to Device Read.** To illustrate the concept going the other way (called Host Write to Device Read or HWDR), consider the example shown in Figure 20‐13 on page 903. In this example, the CPU initiates a memory write whose address targets the PCIe Endpoint in step one. The packet contains TPH bits that tell the RC that it should be stored in an intermediate cache near the target, instead of the cache in the RC that was used in the previous example. In this case a cache built into the Switch serves the purpose. The TLP is then for‐ warded on to the target Endpoint in step two. This model is beneficial when the data is updated infrequently but read often by the Endpoint. That allows sev‐ eral memory reads that would normally go to system memory to be handled by the cache instead, off loading both the Link from the Switch to the RC and the path to memory. 

**902** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐13: TPH Usage for TLPs to Endpoint_ 

**==> picture [353 x 326] intentionally omitted <==**

**----- Start of picture text -----**<br>
1<br>ox<br>oct Complex<br>Cache<br>rl i) i<br>PCle PCle<br>Cache<br>2<br>OWN: Endpoint Bridge<br>Yi i IN orto PCI-X PCI<br>§ EndpointPCle §§ EndpointLegacy PCI/PCI-X | |<br>Device to Device.  One last example is illustrated in Figure 20‐14 on page<br>904, where two Endpoints communicate with each other (called Device Read/<br>Write to Device Read/Write or D*D*) through a shared memory location that is<br>directed by TPH bits to an intermediate cache. In this case, both may update dif‐<br>ferent locations that they need to handle as “read mostly”, or one Endpoint may<br>update data that the other needs to read several times. In both cases, using the<br>intermediate cache improves system performance.<br>**----- End of picture text -----**<br>


**903** 

## **PCI Ex ress Technolo p gy** 

_Figure 20‐14: TPH Usage Between Endpoints_ 

**==> picture [34 x 9] intentionally omitted <==**

**----- Start of picture text -----**<br>
Cache<br>**----- End of picture text -----**<br>


## **TPH Header Bits** 

Several bits in the TLP header describe how the hints are used. First, as shown in the middle at the top of Figure 20‐15 on page 905, the TH (TLP Hints) bit reports whether the optional TPH bits are in use for the TLP. When set, the PH (Processing Hint bits) indicate the next level of information. 

**904** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐15: TPH Header Bits_ 

**==> picture [339 x 115] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- End of picture text -----**<br>


When the TH bit is set the PH bits, shown at the bottom right of Figure 20‐15 on page 905, take the place of what were the two reserved LSBs in the address field. For a 32‐bit address, these are byte 11 [1:0], while for the 64‐bit address shown, they are byte 15 [1:0]. Their encoding is described in Table 20‐1 on page 905. These hints are provided by the Requester based on knowledge of the data pat‐ terns in use, which is information that would be difficult for a Completer to deduce on its own. 

_Table 20‐1: PH Encoding Table_ 

|**PH [1:0]**|**Processing Hint**|**Usage Model**|
|---|---|---|
|00b|Bi‐directional data<br>structure|Indicates frequent read/write access by Host and<br>device.|
|01b|Requester|D*D* (device‐to‐device transfers). Indicates fre‐<br>quent read/write access by device. The asterisk<br>means either device could be reading or writing.|
|10b|Target|DWHR, HWDR (device‐to‐host or host‐to‐device<br>transfers). Indicates frequent read/write access by<br>Host.|
|11b|Target with Priority|Same as Target but with additional temporal<br>re‐use priority information. Indicates frequent<br>read/write access by Host and high temporal local‐<br>ity for accessed data.|



**905** 

## **PCI Ex ress Technolo p gy** 

The next level of information is the Steering Tag byte that provides system‐spe‐ cific information regarding the best place to cache this TLP. Interestingly, the location of this byte in the header varies depending on the Request type. For Posted Memory Writes the Tag field is repurposed to be the Steering Tag (no completion will be returned so the Tag isn’t needed), while for Memory Reads the two Byte Enable fields are repurposed for it (byte enables are not needed for pre‐fetchable reads). The meaning of the bits is implementation specific but they need to uniquely identify the location of the desired cache in the system. 

Two formats for TPH are described in the spec and this level of hint information (TH + PH + 8‐bit Steering Tag), called Baseline TPH, is the first and is required of all Requests that provide TPH. The second format uses TLP Prefixes to extend the Steering Tags (see “TLP Prefixes” on page 908 for more detail). 

## **Steering Tags** 
