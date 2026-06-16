CPU Type 0 Header<br>31 23 15 7 0<br>Device ID Vendor ID 00h<br>Root Complex System Status Command 04h<br>Memory<br>P2P (DRAM) Class Code Line SizeCache 08h<br>BIST Header Latency Cache 0Ch<br>TLP Type Timer Line Size<br>(Addr) Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h<br>P2P<br>Base Address 2 (BAR2) 18h<br>Switch Packet for me? Base Address 3 (BAR3) 1Ch<br>Base Address 4 (BAR4) 20h<br>TLP { Base Address 5 (BAR5) 24h<br>(Addr) CardBus CIS Pointer 28h<br>PCIe PCIe SubsystemDevice ID SubsystemVendor ID 2Ch<br>Endpoint Endpoint Expansion ROM Base Address 30h<br>Reserved Capability 34h<br>TLP Address field Pointer<br>should match a BAR Reserved 38h<br>within a PCIe Function Max Lat Min Gnt InterruptPin InterruptLine 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Switch Routing** 

If an incoming TLP uses address routing, a Switch Port first checks to see if the address is local within the Port itself by comparing the address in the packet header against its two BARs in its Type 1 configuration header, as shown in Step 1 of Figure 4‐21 on page 162. If it matches one of these BARs, the switch port is the target of the TLP and consumes the packet. If not, the port then checks its Base/Limit register pairs to see if the TLP is targeting a function beneath (downstream of) this bridge. If the Request targets IO space, it will check the IO Base and Limit registers, as shown in Step 2a. However, if the Request targets memory space, it will check the Non‐ prefetchable Memory Base/ Limit registers and the Prefetchable Memory Base/Limit registers, as indicated by Step 2b in Figure 4‐21 on page 162. More info on how the Base/Limit register pairs are evaluated can be found in section “Base and Limit Registers” on page 136. 

**161** 

**PCI Express Technology** 

_Figure 4‐21: Switch Checks Routing Of An Inbound TLP Using Address_ 

**==> picture [349 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>CPU 31 23 15 7 0<br>Device ID Vendor ID 00h<br>__ es<br>Status Command 04h<br>Root Complex MemorySystem Class Code Line SizeCache 08h<br>P2P - (DRAM) [—_] e BIST HeaderType s e LatencyTimer Line Size ee Cache 0Ch<br>Base Address 0 (BAR0) 10h<br>TLP<br>1. Packet for me?<br>(Addr) Base Address 1 (BAR1) 14h<br>Secondary Subordinate Secondary Primary 18h<br>P2P Lat Timer Bus # Bus # Bus #<br>2a. IO Packet for some- SecondaryStatus LimitIO BaseIO 1Ch<br>Switch       one beneath me? | (Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>— —— 2b. Mem Packet for some- _— Prefetchable Prefetchable 24h<br>Memory Limit Memory Base<br>      one beneath me? Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>PCIe PCIe IO Limit IO Base<br>Upper 16 Bits Upper 16 Bits 30h<br>7 7 ee<br>Endpoint Endpoint Reserved Capability 34h<br>es Pointer<br>Expansion ROM Base Address 38h<br>— ae<br>ee ControlBridge InterruptPin Interrupt ee Line 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


To understand routing of address‐based TLPs in switches, it is good to remember that each switch port is its own bridge. Below are the steps that a bridge (switch port) takes upon receiving an address‐based TLP: 

## **Downstream Traveling TLPs (Received on Primary Interface)** 

1. IF the target address in the TLP matches one of the BARs, then this bridge (switch port) consumes the TLP because it is the target of the TLP. 

2. IF the target address in the TLP falls in the range of one of its Base/ Limit register sets, the packet will be forwarded to the secondary inter‐ face (downstream). 

3. ELSE the TLP will be handled as an Unsupported Request on the pri‐ mary interface. (This is true if no other bridges on the primary interface claim the TLP either.) 

**162** 

**Chapter 4: Address Space & Transaction Routing** 

## **Upstream Traveling TLPs (Received on Secondary Interface)** 

1. IF the target address in the TLP matches one of the BARs, then this bridge (switch port) consumes the TLP because it is the target of the TLP. 

2. IF the target address in the TLP falls in the range of one of its Base/ Limit register sets, the TLP will be handled as an Unsupported Request on the secondary interface. (This is true unless this port is the upstream port of the switch. In these cases, the packet may be a peer‐to‐peer transaction and will be forwarded downstream on a different down‐ stream port than the one it was received on.) 

3. ELSE the TLP will be forwarded to the primary interface (upstream) given that the TLP address is not for this bridge and is not for any func‐ tion beneath this bridge. 

## **Multicast Capabilities** 

The 2.1 version of the PCI Express specification added support for specifying a range of addresses that provide multicast functionality. Any packets received that fall within the address range specified as the multicast range are routed/ accepted according to the multicast rules. This address range might not be reserved in a function’s BARs and might not be within a bridge’s Base/Limit reg‐ ister pair, but would still need to be accepted/forwarded appropriately. More info can be found on the multicast functionality in the section on “Multicast Capability Registers” on page 889. 

## **Implicit Routing** 

Implicit routing, used in some message packets, is based on the awareness of routing elements that the topology has upstream and downstream directions and a single Root Complex at the top. This allows some simple routing methods without the need to assign a target address or ID. Since the Root Complex gen‐ erally integrates power management, interrupt, and error handling logic, it is either the source or recipient of most PCI Express messages. 

## **Only for Messages** 

Some messages use address or ID routing rather than implicit routing, and for them, the routing mechanisms are applied in the same way as described in the those sections. However, most messages use implicit routing. The purpose of implicit routing is to mimic side‐band signal behavior since a design goal for PCIe was to eliminate as many side‐band signals from PCI as possible. These 

**163** 

**PCI Express Technology** 

side‐band signals in PCI were typically either the host notifying all devices of an event or devices notifying the host of an event. In PCIe, we have Message TLPs to convey these events. The types of events that PCIe has defined messages for are: 

- Power Management 

- INTx legacy interrupt signaling 

- Error signaling 

- Locked Transaction support 

- Hot Plug signaling 

- Vendor‐specific signaling 

- Slot Power Limit settings 

## **Key TLP Header Fields in Implicit Routing** 

For implicit routing, the routing sub‐field in the header is used to determine the message destination. Figure 4‐22 on page 164 illustrates a message TLP using implicit routing. 

_Figure 4‐22: 4DW Message TLP Header ‐ Implicit Routing Fields_ 

**==> picture [355 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
4DW Header for Messages<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R TH T E Attr AT Length<br>0 x 1 1  0  r  r  r tr 0 D P 0 0 0 0<br>Message<br>Byte 4 Requester ID Tag<br>Code<br>Byte 8 Bytes 8-11 Vary with  Message Code  Field<br>Byte 12 Bytes 12-15 Vary with  Message Code  Field<br>**----- End of picture text -----**<br>


## **Message Type Field Summary** 

Table 4‐10 on page 165 shows how the TLP header Type field for Messages is interpreted. As shown, the upper two bits indicate the packet is a Message while the lower three bits specify the routing method to apply. Note that Mes‐ sage TLPs always use a 4DW header regardless of the routing option selected. 

**164** 

**Chapter 4: Address Space & Transaction Routing** 

For address routing, bytes 8‐15 contain up to a 64‐bit address, and for ID rout‐ ing, bytes 8 and 9 contain the target BDF. 

_Table 4‐10: Message Request Header Type Field Usage_ 

|**Type Field Bits**|**Description**|
|---|---|
|Bit 4:3|Defines the type of transaction:<br>10b = Message TLP|
|Bit 2:0|Message Routing Subfield R[2:0]<br>• 000b = Implicit ‐ Route to the Root Complex<br>• 001b = Route by Address (bytes 8‐15 of header contain address)<br>• 010b = Route by ID (bytes 8‐9 of header contain ID)<br>• 011b = Implicit ‐ Broadcast downstream<br>• 100b = Implicit ‐ Local: terminate at receiver<br>• 101b = Implicit ‐ Gather & route to the Root Complex<br>• 110b ‐ 111b = Reserved: terminate at receiver|



## **Endpoint Handling** 

For implicit routing, an Endpoint simply checks whether the routing sub‐field is appropriate for it. For example, an Endpoint will accept a Broadcast Message or a Message that terminates at the receiver; but not Messages that implicitly target the Root Complex. 

## **Switch Handling** 

Routing elements like Switches consider the port on which the TLP arrived on and whether the routing sub‐field code is appropriate for it. For example: 

1. A Switch Upstream Port may legitimately receive a Broadcast Message. It will duplicate that and forward it to all its Downstream Ports. An implicitly routed Broadcast Message received on a Downstream Port of a Switch (meaning the message was traveling upstream) would be an error that would be handled as a Malformed TLP. 

2. A Switch may receive implicitly routed Messages for the Root Complex on Downstream Ports and will forward these to its Upstream Port because the location of the Root Complex is understood to be upstream. It would not accept Messages received on its Upstream Port (meaning the message was traveling downstream) that are implicitly routed to the Root Complex. 

**165** 

## **PCI Express Technology** 

3. If an implicitly routed Message indicates it should terminate at the receiver, then the receiving switch port will consume the message rather than for‐ ward it. 

4. For messages routed using address or ID routing, a Switch will simply per‐ form normal address or ID checks in deciding whether to accept or forward it. 

## **DLLPs and Ordered Sets Are Not Routed** 

DLLP and Ordered Set traffic is not routed from ingress ports to egress ports of switches or root complexes. These packets move from port to port across a link from Physical Layer to Physical Layer. 

DLLPs originate at the Data Link Layer of a PCI Express port, pass through the Physical Layer, exit the port, traverse the Link and arrive at the neighboring port. At this port, the packet passes through the Physical Layer and ends up at the Data Link Layer where it is processed and consumed. DLLPs do not pro‐ ceed further up the port to the Transaction Layer and hence are not routed. 

Similarly, Ordered‐Set packets originate at the Physical Layer, exit the port, traverse the Link and arrive at the neighboring port. At this port, the packet arrives at the Physical Layer where it is processed and consumed. Ordered‐Sets do not proceed further up the port to the Data Link Layer and Transaction Layer and hence are not routed. 

As has been discussed in this chapter, only TLPs are routed through switches and root complexes. The originate at the Transaction Layer of a source port and end up at the Transaction Layer of a destination port. 

**166** 

## Part Two: 

# Transaction Layer 

## _**5**_ 

## _**TLP Elements**_ 

## **The Previous Chapter** 

The previous chapter describes the purpose and methods of a function request‐ ing address space (either memory address space or IO address space) through Base Address Registers (BARs) and how software must setup the Base/Limit registers in all bridges to route TLPs from a source port to the correct destina‐ tion port. The general concepts of TLP routing in PCI Express are also dis‐ cussed, including address‐based routing, ID‐based routing and implicit routing. 

## **This Chapter** 
