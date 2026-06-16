|Completion w/Data (CplDLk)|010 = 3DW, w/<br>data|0 1011|
|Fetch and Add AtomicOp Request<br>(FetchAdd)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1100|
|Unconditional Swap AtomicOp<br>Request (Swap)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1101|
|Compare and Swap AtomicOp<br>Request (CAS)|010 = 3DW, w/data<br>011 = 4DW, w/data|0 1110|
|Local TLP Prefix (LPrfx)|100 = 1DW|0 LLLL|
|End‐to‐End TLP Prefix (EPrfx)|100 = 1DW|1 EEEE|



## **TLP Header Overview** 

When TLPs are received at an ingress port, they are first checked for errors at the Physical and Data Link Layers. If there are no errors, the TLP is examined at the Transaction Layer to learn which routing method is to be used. The basic steps are: 

1. _Format_ and _Type_ fields determine the header size, format and type of the packet. 

2. Depending on the routing method associated with the packet type, the device determines whether it’s the intended recipient. If so, it will accept (consume) the TLP, but if not, it will forward the TLP to the appropriate egress port ‐ subject to the rules for ordering and flow control for that egress port. 

3. If this device is not the intended recipient nor is it in the path to the intended recipient, it will generally reject the packet as an Unsupported Request (UR). 

**154** 

**Chapter 4: Address Space & Transaction Routing** 

## **Applying Routing Mechanisms** 

Once the system addresses have been configured and transactions are enabled, devices examine incoming TLPs and use the corresponding configuration fields to route the packet. The following sections describe the basic features/function‐ ality of each routing mechanism used in routing TLPs through the PCI Express fabric. 

## **ID Routing** 

ID routing is used to target the logical position ‐ Bus Number, Device Number, Function Number (typically referred to as **BDF** ), of a Function within the topol‐ ogy. It’s compatible with routing methods used in the PCI and PCI‐X protocols for configuration transactions. In PCIe, it is still used for routing configuration packets and is also used to route completions and some messages. 

## **Bus Number, Device Number, Function Number Limits** 

PCI Express supports the same topology limits as PCI and PCI‐X: 

1. Eight bits are used to give the bus number, so a **maximum of 256 busses** are possible in a system. This includes internal busses created by Switches. 

2. Five bits give the device number, so a **maximum of 32 devices** are possible per bus. An older PCI bus or an internal bus in a switch or root complex may host more than one downstream device. However, external PCIe links are always point‐to‐point and there’s only one downstream device on the link. The device number for an external link is forced by the downstream port to always be Device 0, so every external Endpoint will always be Device 0 (unless using Alternative Routing‐ID Interpretation (ARI), in which case, there are no device numbers; more about ARI can be found in the section on “IDO (ID‐based Ordering)” on page 909. 

3. Three bits give the function number, so a **maximum of 8 internal functions** is possible per device. 

## **Key TLP Header Fields in ID Routing** 

If the Type field in a received TLP indicates ID routing is to be used, then the ID fields in the header (Bus, Device, Function) are used to perform the routing check. There are two cases: ID routing with a 3DW header and ID routing with a 4DW header (only possible in messages). Figure 4‐15 on page 156 illustrates a TLP using ID routing and the 3DW header, while Fig‐ ure 4‐16 on page 156 shows the 4DW header for ID routing. 

**155** 

**PCI Express Technology** 

_Figure 4‐15: 3DW TLP Header ‐ ID Routing Fields_ 

**==> picture [354 x 357] intentionally omitted <==**

**----- Start of picture text -----**<br>
3DW Header Using ID Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 0 Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Device Func<br>Byte 8 Bus Number Bytes 10-11 Vary with  Type  Field<br>Function Number with ARI<br>Figure 4‐16: 4DW TLP Header ‐ ID Routing Fields<br>4DW Header Using ID Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Device Func<br>Byte 8 Bus Number Bytes 10-11 Vary with  Type  Field<br>Function Number with ARI<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


## **Endpoints: One Check** 

For ID routing, an Endpoint simply checks the ID field in the packet header against its own BDF. Each function “captures” its own Bus and Device Number every time a Type 0 configuration write is seen on its link from bytes 8‐9 in the TLP Header. Where the captured Bus and Device Number information should be stored in not specified, only that functions must save it. The saved Bus and 

**156** 

**Chapter 4: Address Space & Transaction Routing** 

Device numbers are used as the Requester ID in TLP requests that this Endpoint initiates so the Completer of that request can include the Requester ID value in the completion packet(s). The Requester ID in a completion packet is used to route the completion. 

## **Switches (Bridges): Two Checks Per Port** 

For an ID‐routed TLP, a switch port first checks to see whether it is the intended target by comparing the target ID in the TLP Header against its own BDF, as shown by (1) in Figure 4‐17 on page 158. As was true for an Endpoint, each switch port captures its own Bus and Device number every time a configuration write (Type 0) is detected on its Upstream Port. If the target ID field in the TLP agrees with the ID of the switch port, it consumes the packet. If the ID field doesn’t match, it then checks to see if the TLP is targeting a device below this switch port. It does this by checking the Secondary and Subordinate Bus Num‐ ber registers to see if the target Bus Number in the TLP is within this range (inclusive). If so, then the TLP should be forwarded downstream. This check is indicated by (2) in Figure 4‐17 on page 158. If the packet was moving down‐ stream (arrived on the Upstream Port) and doesn’t match the BDF of the Upstream Port or fall within the Secondary‐Subordinate bus range, it will be handled as an Unsupported Request on the Upstream Port. 

If the Upstream Port determines that a TLP it received is for one of the devices beneath it (because the target bus number was within the range of its Second‐ ary‐Subordinate bus number range), then it forwards it downstream and all the downstream ports of the switch perform the same checks. Each downstream port checks to see if the TLP is targeting them. If so, the targeted port will con‐ sume the TLP and the other ports ignore it. If not, all downstream ports check to see if the TLP is targeting a device beneath their port. The one port that returns true on that check will forward the TLP to its Secondary Bus and the other downstream ports ignore the TLP. 

In this section, it is important to remember that each port on a switch is a Bridge, and thus has its own configuration space with a Type 1 Header. Even though Figure 4‐17 on page 158 only shows a single Type 1 Header, in reality, each port (each P2P Bridge) has its own Type 1 Header and performs the same two checks on TLPs when they are seen by that port. 

**157** 

**PCI Express Technology** 

_Figure 4‐17: Switch Checks Routing Of An Inbound TLP Using ID Routing_ 

**==> picture [338 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>CPU 31 23 15 7 0<br>Device ID Vendor ID 00h<br>__ es<br>Status Command 04h<br>Root Complex MemorySystem Class Code Line SizeCache 08h<br>— P2P - (DRAM) ee [TT] TSS BIST HeaderType LatencyTimer ee Line SizeCache 0Ch<br>Base Address 0 (BAR0) 10h<br>TLP ID Field<br>1. Packet for me?<br>(BDF) ; ee Base Address 1 (BAR1) 14h<br>Secondary Subordinate Secondary Primary 18h<br>P2P Lat Timer Bus # Bus # Bus #<br>Switch + 2. Packet for someone    beneath me? SS SecondaryStatus LimitIO BaseIO 1Ch<br>(Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>NIK —}--—— Memory LimitPrefetchable Memory BasePrefetchable 24h<br>Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>PCIe ma PCIe Cc — OO IO Limit IO Base<br>oe Upper 16 Bits Upper 16 Bits 30h<br>Endpoint Endpoint Reserved Capability 34h<br>a Pointer<br>Expansion ROM Base Address 38h<br>—<br>or ControlBridge InterruptPin InterruptLine 3Ch<br>P2P P2P<br>**----- End of picture text -----**<br>


## **Address Routing** 

TLPs that use address routing refer to the same memory (system memory and memory‐mapped IO) and IO address maps that PCI and PCI‐X transactions do. Memory requests targeting an address below 4GB (i.e. a 32‐bit address) must use a 3DW header, and requests targeting an address above 4GB (i.e. a 64‐bit address) must use a 4DW header. IO requests are restricted to 32‐bit addresses and are only implemented to support legacy functionality. 

**158** 

**Chapter 4: Address Space & Transaction Routing** 

## **Key TLP Header Fields in Address Routing** 

When the Type field indicates address routing is to be used for a TLP, then the Address Fields in the header are used to perform the routing check. These can be 32‐bit addresses or 64‐bit addresses. 

**TLPs with 32‐Bit Address** For IO or 32‐bit memory requests, a 3DW header is used as shown in Figure 4‐18. The memory‐mapped registers tar‐ geted with these TLPs will therefore reside below the 4GB memory or IO address boundary. 

**TLPs with 64‐Bit Address** For 64‐bit memory requests, a 4DW header is used as shown in Figure 4‐19 on page 160. The memory‐mapped registers targeted with these TLPs are able to reside above the 4GB memory bound‐ ary. 

_Figure 4‐18: 3DW TLP Header ‐ Address Routing Fields_ 

**==> picture [370 x 148] intentionally omitted <==**

**----- Start of picture text -----**<br>
3DW Header Using Address Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>0 x 0 tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


**159** 

**PCI Express Technology** 

_Figure 4‐19: 4DW TLP Header ‐ Address Routing Fields_ 

**==> picture [372 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
4DW Header Using Address Routing<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>0 x 1 tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- End of picture text -----**<br>


## **Endpoint Address Checking** 

If an Endpoint receives a TLP that uses address routing then it checks the address in the header against each of its implemented Base Address Registers (BARs) in its configuration header, as shown in Figure 4‐20. Since Endpoints only have one link interface, it will either accept the packet or reject it. The End‐ point will accept the packet if the target address in the TLP matches one of the ranges programmed into its BARs. More info on how the BARs are used can be found in section “Base Address Registers (BARs)” on page 126. 

**160** 

**Chapter 4: Address Space & Transaction Routing** 

_Figure 4‐20: Endpoint Checks Incoming TLP Address_ 

**==> picture [335 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>