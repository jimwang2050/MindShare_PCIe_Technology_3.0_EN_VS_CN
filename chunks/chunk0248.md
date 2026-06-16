Differentiated Service, since packets are treated differently based on an assigned priority and it allows for a wide range of service preferences. At the high end of that range, QoS can provide predictable and guaranteed perfor‐ mance for applications that need it. That level of support is called “isochro‐ nous” service, a term derived from the two Greek words “isos” (equal) and “chronos” (time) that together mean something that occurs at equal time inter‐ vals. To make that work in PCIe requires both hardware and software elements. 

## **Basic Elements** 

Supporting high levels of service places requirements on system performance. For example, the transmission rate must be high enough to deliver sufficient data within a time frame that meets the demands of the application while accommodating competition from other traffic flows. In addition, the latency must be low enough to ensure timely arrival of packets and avoid delay prob‐ lems. Finally, error handling must be managed so that it doesn’t interfere with timely packet delivery. Achieving these goals requires some specific hardware elements, one of which is a set of configuration registers called the Virtual Channel Capability Block as shown in Figure 7‐1. 

_Figure 7‐1: Virtual Channel Capability Registers_ 

**==> picture [368 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
0d<br>63d CapPtr Header<br>PCI Compatible<br>PCIeCapabilityBlock Space<br>PCIe Enhanced Capability Register<br>Port VC Cap Register 1 Ext VC Cnt 255d<br>VATOffset PortVCCapRegister2 VirtualChannel<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VCResourceCap(0) CapabilityStructure<br>VCResourceControlReg(0)<br>VCResourceStatus(0) Reserved PCIe Extended<br>PATnOffset VCResourceCap(n) CapabilitySpace<br>VCResourceControlReg(n)<br>VCResourceStatus(n) Reserved<br>VCArbitrationTable(VAT)<br>PortArbitrationTable0(PAT0) 4095d<br>PortArbitrationTablen(PATn)<br>**----- End of picture text -----**<br>


**246** 

**Chapter 7: Quality of Service** 

## **Traffic Class (TC)** 

The first thing we need is a way to differentiate traffic; something to distinguish which packets have high priority. This is accomplished by designating Traffic Classes (TCs) that define eight priorities specified by a 3‐bit TC field within each TLP header (with ascending priority; TC 0‐7). The 32‐bit memory request header in Figure 7‐2 reveals the location of the TC field. During initialization, the device driver communicates the level of services to the isochronous man‐ agement software, which returns the appropriate TC values to use for each type of packet. The driver then assigns the correct TC priority for the packet. The TC value defaults to zero so packets that don’t need priority service won’t acciden‐ tally interfere with those that do. 

_Figure 7‐2: Traffic Class Field in TLP Header_ 

**==> picture [372 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


Configuration software that’s unaware of PCIe won’t recognize the new regis‐ ters and will use the default TC0/VC0 combination for all transactions. In addi‐ tion, there are some packets that are always required to use TC0/VC0, including Configuration, I/O, and Message transactions. If these packets are thought of as maintenance‐level traffic, then it makes sense that they would need to be con‐ fined to VC0 and kept out of the path of high‐priority packets. 

## **Virtual Channels (VCs)** 

VCs are hardware buffers that act as queues for outgoing packets. Each port must include the default VC0, but may have as many as eight (from VC0 to VC7). Each channel represents a different path available for outgoing packets. 

**247** 

**PCI Ex ress Technolo p gy** 

The motivation for multiple paths is analogous to that of a toll road in which drivers purchase a radio tag that lets them take one of several high priority lanes at the toll booth. Those who don’t purchase a tag can still use the road but they’ll have to stop at the booth and pay cash each time they go through, and that takes longer. If there was only one path, everyone’s access time would be limited by the slowest driver, but having multiple paths available means that those who have priority are not delayed by those who don’t. 

## **Assigning TCs to each VC — TC/VC Mapping** 

The Traffic Class value assigned to each packet travels unchanged to the desti‐ nation and must be mapped to a VC at each service point as it traverses the path to the target. VC mapping is specific to a Link and can change from one Link to another. Configuration software establishes this association during initializa‐ tion using the _TC/VC Map_ field of the VC Resource Control Register. This 8‐bit field permits TC values to be mapped to a selected VC, where each bit position represents the corresponding TC value (bit 0 = TC0, bit 1 = TC1, etc.). Setting a bit assigns the corresponding TC value to the VC ID. Figure 7‐3 on page 249 shows a mapping example where TC0 and TC1 are mapped to VC0 and TC2:TC4 are mapped to VC3. 

Software has a great deal of flexibility in assigning VC IDs and mapping the TCs, but there are some rules regarding the TC/VC mapping: 

- TC/VC mapping must be identical for the two ports attached on either end of the same Link. 

- TC0 will automatically be mapped to VC0. 

- Other TCs may be mapped to any VC. 

- • A TC may **not** be mapped to more than one VC. 

The number of virtual channels used depends on the greatest capability shared by the two devices attached to a given link. Software assigns an ID for each VC and maps one or more TCs to the VCs. 

**248** 

**Chapter 7: Quality of Service** 

_Figure 7‐3: TC to VC Mapping Example_ 

**==> picture [348 x 407] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16 15                                      0<br>PCI Express Extended Capability Header<br>Port VC Capability Register 1<br>Port VC Capability Register 2<br>Port VC Status Register Port VC Control Register<br>PAT Offset VC0 Resource Capability Register<br>VC0 Resource Control Register<br>VC0 Resource Status Reg Reserved<br>PAT Offset VC3 Resource Capability Register<br>VC3 Resource Control Register<br>VC3 Resource Status Reg Reserved<br>31              26 24            19 17 16 15  8 7                     0<br>C0 VCID TC/VC Map<br>2      0 7                         0<br>0 0 0 0 0 0 0 0 0 1 1<br>31              26 24            19 17 16 15  8 7                     0<br>VC3 VCID TC/VC Map<br>2      0 7                         0<br>0 1 1 0 0 0 1 1 1 0 0<br>**----- End of picture text -----**<br>


## **Determining the Number of VCs to be Used** 

Software checks the number of VCs supported by the devices attached to a com‐ mon link and would usually assign the greatest number of VCs that both devices can support. Consider the example topology in Figure 7‐4 on page 250. 

**249** 

## **PCI Ex ress Technolo p gy** 

Here, the switch supports all 8 VCs on each of its ports, while Device A sup‐ ports only the default VC0, Device B supports 4 VC s, and Device C support 8 VCs. Note that even though switch port A supports all 8 VCs, Device A only supports VC0, so 7 VCs are left unused in switch port A. Similarly, only 4 VCs are used by switch port B. 

_Figure 7‐4: Multiple VCs Supported by a Device_ 

**==> picture [369 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>8 VCs supported<br>on each switch port<br>Switch<br>1 VC A C<br>B<br>8 VCs<br>4 VCs<br>Device<br>1 VC supported 8 VCs supported<br>B<br>4 VCs supported<br>A<br>Device<br>C<br>Device<br>**----- End of picture text -----**<br>


Configuration software determines the maximum number of VCs supported by each port interface by reading the _Extended VC Count_ field in the Virtual Chan‐ nel Capability registers, as shown in Figure 7‐5 on page 251. Software checks the Extended VC Count at both ends of the Link and selects the highest common count. Using all the available VCs is not mandatory, though. Software may choose to enable fewer VCs as well. 

**250** 

**Chapter 7: Quality of Service** 

_Figure 7‐5: Extended VCs Supported Field_ 

**==> picture [297 x 304] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header<br>Port VC Capability Register 1<br>Port VC Capability Register 2<br>Port VC Status Register  Port VC Control Register<br>PAT Offset VC0 Resource Capability Register<br>VC0 Resource Control Register<br>VC0 Resource Status Reg  Reserved<br>PAT Offset VCn Resource Capability Register<br>VCn Resource Control Register<br>VCn Resource Status Reg  Reserved<br>2                             0<br>Extended VC Count<br>0 = only VC0 supported<br>1-7 = number of additional<br>         VCs supported<br>**----- End of picture text -----**<br>


## **Assigning VC Numbers (IDs)** 

Configuration software assigns a number (ID) to each of the VCs, except VC0 which is always hardwired. As shown in Figure 7‐3 on page 249, the VC Capa‐ bilities registers include 12 bytes of configuration registers for each VC. The first set of registers always applies to VC0. The _Extended VC Count_ field defines the number of additional VCs implemented by this port, each of which will have a set of registers. The value “n” represents the number of additional VCs imple‐ mented. For example, if the _Extended VC Count_ contains a value of 3, then there are three VCs and register sets in addition to VC0. 

**251** 

**PCI Ex ress Technolo p gy** 

Software assigns a number for each of the additional VCs via the _VC ID_ field. (See Figure 7‐3 on page 249) The IDs don’t have to be contiguous but each num‐ ber can only be used once. 

## **VC Arbitration** 

## **General** 

If a device has more than one VC and they all have a packet ready to send, VC arbitration determines the order of packet transmission. Any of several schemes can be chosen by software from among the options implemented by hardware. The goals are to implement the desired service policy and ensure that all trans‐ actions are making forward progress to prevent inadvertent time‐outs. In addi‐ tion, VC Arbitration is affected by the requirements associated with flow control and transaction ordering. These topics are discussed in other chapters, but they affect arbitration, too, because: 

- Each supported VC provides its own buffers and flow control. 

- Transactions mapped to the same VC are normally passed along in strict order (although there are exceptions, such as when a packet has the “Relaxed Ordering” attribute bit set). 

- Transaction ordering only applies within a VC, so there’s no ordering rela‐ tionship among packets assigned to different VCs. 

The example in Figure 7‐6 on page 253 illustrates two VCs (VC0 and VC1) with a transmission priority based on a 3:1 ratio, meaning three VC1 packets are sent for every one VC0 packet. The device core sends requests (including a TC value) to the TC/VC Mapping logic. Based on the programmed mapping, the packet is placed into the appropriate VC buffer for transmission. Finally, the VC arbiter determines the VC priority for forwarding the packets. This example illustrates the flow in one direction, but the same logic exists for transmitting in the oppo‐ site direction at the same time. 

The VC capability registers provide three basic VC arbitration approaches: 

1. Strict Priority Arbitration — the highest numbered VC with a packet ready always wins. 
