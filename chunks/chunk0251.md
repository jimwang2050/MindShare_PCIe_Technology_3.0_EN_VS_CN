- 10b — 4 bits (16 ports) 

- 11b — 8 bits (256 ports) 

Configuration software loads each table with port numbers to accomplish the desired port priority for each VC supported. As illustrated in Figure 7‐19 on page 268, the table format depends on the size of each entry and the number of phases supported by this design. 

**267** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐19: Format of Port Arbitration Tables_ 

**==> picture [339 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
32-Phase Port Arbitration Table<br>with 4-bit entries<br>31       28 27      24 23      20 19 16 15       12 11         8 7          4 3           0<br>Phase[7] Phase[6] Phase[5] Phase[4] Phase[3] Phase[2] Phase[1] Phase[0] 00h<br>Phase[15] Phase[14] Phase[13] Phase[12] Phase[11] Phase[10] Phase[9] Phase[8] 04h<br>Phase[23] Phase[22] Phase[21] Phase[20] Phase[19] Phase[18] Phase[17] Phase[16] 08h<br>Phase[31] Phase[30] Phase[29] Phase[28] Phase[27] Phase[26] Phase[25] Phase[24] 0Bh<br>1. Configuration Software loads the Port Arbitration Table.<br>2. Changes to the table automatically set the Port Arbitration 00b PAT entry is 1 bit (2 ports)<br>Table Status bit.<br>01b PAT entry is 2 bits (4 ports)<br>3. Software sets the Load Port Arbitration Table bit to<br>10b PAT entry is 4 bits (16 ports)<br>     apply the table contents to the hardware.<br>4. Hardware loads table contents into the Port Arbiter, then  11b PAT entry is 8 bits (256 ports)<br>    automatically clears the Port Arbitration Table<br>    status bit when the table has been loaded.<br>VC Resource Status Register  Port VC Capability Register 1<br>15                                       2  1  0  31                                                          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP RsvdP<br>VC Negotiation Pending  Port Arbitration Table Entry Size<br> Port Arbitration Table Status  Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>VC Resource Capability Register<br>31              26 24            19 17 16 15 8 7                     0<br>RsvdP VCID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


**268** 

**Chapter 7: Quality of Service** 

## **Switch Arbitration Example** 

Let’s consider an example of a three‐port switch to illustrate both Port and VC arbitration. The example presumes that packets arriving on ingress ports 0 and 1 are moving in the upstream direction and port 2 is the egress port facing upstream (toward the Root Complex). Refer to Figure 7‐20 on page 270 during the following discussion. 

1. Packets arriving at ingress port 0 are placed in a receiver VC based on the TC/VC mapping for port 0. As shown, TLPs with traffic class TC0 or TC1 are sent to the VC0 buffers. TLPs carrying traffic class TC3 or TC5 are sent to the VC1 buffers. No other TCs are permitted on this link. As an aside, if a packet does arrive with a TC that has not been mapped to an existing VC, it will be treated as an error. 

2. Packets arriving at ingress port 1 are placed in a VC based on TC/VC map‐ ping, too, but it’s not the same for this port. As indicated, TLPs carrying traffic class TC0 are sent to VC0, while TLPs carrying traffic class TC2‐TC4 are sent to VC3. No other TCs are permitted on this link. 

3. In both ports, the target egress port is determined from routing information in each packet. For example, address routing is used in memory or IO request TLPs. 

4. All packets destined for egress port 2 are submitted to the TC/VC mapping logic for that port. As shown, TLPs carrying traffic class TC0‐TC2 are placed into buffers for VC0 that are labeled with their ingress port number, while TLPs carrying traffic class TC3‐TC7 are managed for VC1. 

5. Port Arbitration is applied independently to queued up packets to decide which port’s packets will get loaded next into the real VC. 

6. Finally, VC arbitration determines the order in which transactions in the VC buffers will be sent across the link. 

7. Note that the VC arbiter selects packets for transmission only if sufficient flow control credits exist. 

**269** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐20: Arbitration Examples in a Switch_ 

**==> picture [357 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
Switch<br>(1)<br>TC0,1TC3,5  VC0VC1 0 Of IngressMappingTC/VCPort 0 TC0,1TC3,5 INRESS EGRESS (5)Port Arbitration: VC0Egress Port 2<br>FC Buffer VC0 FC Buffer VC1<br>TLP1 RoutingTLP2 Routing TCTC TLP4 RoutingTLP3 Routing TCTC (4) PacketsPort 0 VC0VC0 ARB (6)<br>Egress Port 2<br>To  Port 1 TC/VC VC Arbitration (7)<br>(2) Determine Egress Port(Using Routing Info) (3) To  Port 2To  Port 3 Of EgressMappingPort 2 VC0VC1 ARB 2 TC0-2TC3-7 VC0VC1<br>TC2-4TC0   VC0VC3 1 Of IngressMappingTC/VCPort 1 TC2-4TC0 TC0-2=>VC0TC3-7=>VC1 (5)Port Arbitration: VC1Egress Port 2<br>FC Buffers VC0 FC Buffers VC3 PacketsPort 1 VC1 ARB<br>TLP3 Routing TLP4 Routing VC1<br>TLP1 Routing TLP2 Routing<br>Determine Egress Port(Using Routing Info) (3) To  Port 0To  Port 2To  Port 3 This logic replicated for each egress port<br>**----- End of picture text -----**<br>


## **Arbitration in Multi-Function Endpoints** 

Another set of registers called Multi‐Function Virtual Channel (MFVC) capabil‐ ity is defined for the specific case of endpoints that will implement QoS in a device with multiple functions. Not surprisingly, this case presents the same arbitration issues internally that a switch port must handle. 

There are two cases described in the spec for this arbitration. In the first case, shown in Figure 7‐21 on page 271, there are two Functions but only Function 0 includes VC Capability registers and the assignments made there are implicitly the same for all functions. For this option, arbitration between the functions will be handled in some vendor‐specific manner. That’s the simplest approach, but doesn’t include a standard structure to define priority between requests from different functions and so it doesn’t support QoS. 

**270** 

**Chapter 7: Quality of Service** 

_Figure 7‐21: Simple Multi‐Function Arbitration_ 

**==> picture [252 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Function 0 Vendor-Specific<br>Arbitration<br>VC Internal Link<br>Capability<br>0002h<br>Egress Port<br>Function 1<br>Internal Link<br>**----- End of picture text -----**<br>


If QoS support is desired, then an MFVC is implemented in VC0 and each func‐ tion has its own unique set of VC Capability registers. To preserve software backward compatibility, the spec states that the VC Capability ID for a device that _does not_ use MFVC must be 0002h, while the VC Capability ID for a device that _does_ implement an MFVC structure must be 0009h. 

Figure 7‐22 on page 272 shows the MFVC register block and a block diagram of an example with two functions in an endpoint whose port supports two VCs. Each function has a Transaction Layer and its own VC Capability registers, but doesn’t implement the lower layers. Instead, they connect to the Transaction Layer of the shared port that does have all the layers. Sharing the hardware interface results in lower cost, of course, and the addition of MFVC allows the functions to handle isochronous traffic. 

As can be seen in the figure, the MFVC registers reside in Function 0 only and define the VCs and arbitration methods to be used for this interface. The MFVC registers look very much the same as VC capability registers and support VC arbitration and Function arbitration. Since packets from multiple functions can attempt to access the same VC at the same time, Function Arbitration decides the priorities among them. That should look familiar by now because it’s the same concept as port arbitration and even uses the same arbitration options, including TBWRR. VC arbitration options are also the same as they are in the single‐function VC registers. 

**271** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐22: QoS Support in Multi‐Function Arbitration_ 

**==> picture [330 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header Cnt<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>Func 0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>Func n Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Function Arbitration Table 0<br>Function Arbitration Table n<br>Function<br>Function 0 Arbiter<br>MFVC Port 1<br>Capability VC0<br>0008h Internal Link<br>Port 2 VC0 VC Arbiter<br>VC<br>Capability VC0<br>0009h<br>Egress<br>Port<br>Function 1<br>Port 1<br>VC7<br>Internal Link<br>VC Port 2 VC7<br>Capability VC7<br>0009h<br>TC/VC Mapping<br>**----- End of picture text -----**<br>


## **Isochronous Support** 

As mentioned earlier, not every machine or application needs isochronous sup‐ port, but there are some that can’t get by without it. Since PCIe was designed to support it from the beginning, let’s consider what would need to be in place to make this work. 

**272** 

**Chapter 7: Quality of Service** 

## **Timing is Everything** 

Consider the example shown in Figure 7‐23 on page 274, where a synchronous connection would be desirable but isn’t possible. Instead, we emulate a synchro‐ nous path with isochronous mechanisms. In this example, isochrony defines the amount of data that will be delivered within each Service Interval to achieve the required service. The following sequence describes the operation: 

1. The synchronous source (video camera and PCI Express interface) accumu‐ lates data in Buffer A during the first of the equal service intervals (SI 1). 

2. The camera delivers all of the accumulated data across the general‐purpose bus during the next service interval (SI 2) while it accumulates the next block of data in Buffer B. 

   - Clearly, the system must be able to guarantee that the entire contents of buffer A can be delivered during the service interval, regardless of whether other traffic is in flight on the Link. This is handled by assigning a high pri‐ ority to the time‐sensitive packets and programming arbitration schemes so they’ll be handled first any time there is competition with other traffic. Also note that, as long as all the data is delivered within the time window, it doesn’t matter exactly when it arrives. It might be spread out across the interval or bunched up in one place inside it. As long as it’s all delivered with the Service Interval the guarantees can still be met. 

3. During SI 2, the tape deck receives and buffers the incoming data, which can then be delivered to storage for recording during SI 3. The camera unloads Buffer B onto the Link during SI 3 while accumulating new data into Buffer A, and the cycle repeats. 

**273** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐23: Example Application of Isochronous Transaction_ 

**==> picture [298 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
Camera<br>SI 1 Data accumulated<br>in Buffer A<br>SI 2 Data from Buffer A<br>delivered while<br>next data accumulates<br>in Buffer B<br>SI 3 Data from Buffer B<br>delivered while next<br>data accumulates in<br>Buffer A<br>PCI Express<br>Interface<br>SI 1 SI 2 SI 3<br>Service Interval (SI)<br>SI 2 Data received into<br>Buffer A<br>SI 3 Data from Buffer A<br>delivered to Storage<br>while data received<br>into Buffer B<br>Storage (e.g.: tape)<br>Buffer A Buffer B<br>Buffer A Buffer B<br>**----- End of picture text -----**<br>


## **How Timing is Defined** 
