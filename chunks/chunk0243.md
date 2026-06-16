|Assert_INTD|0010 0011b||
|Deassert_INTA|0010 0100b||
|Deassert_INTB|0010 0101b||
|Deassert_INTC|0010 0110b||
|Deassert_INTD|0010 0111b||



Rules regarding the use of INTx Messages: 

1. They have no data payload and so the Length field is reserved. 

2. They’re only issued by Upstream Ports. Checking this rule for received packets is optional but, if checked, violations will be handled as Malformed TLPs. 

3. They’re required to use the default traffic class TC0. Receivers must check for this and violations will be handled as Malformed TLPs. 

4. Components at both ends of the Link must track the current state of the four virtual interrupts. If the logical state of one interrupt changes at the Upstream Port, it must send the appropriate INTx message. 

5. INTx signaling is disabled when the Interrupt Disable bit of the Command Register is set = 1 (as would be the case for physical interrupt lines). 

6. If any virtual INTx signals are active when the Interrupt Disable bit is set in the device, the Upstream Port must send corresponding Deassert_INTx messages. 

7. Switches must track the state of the four INTx signals independently for each Downstream Port and combine the states for the Upstream Port. 

8. The Root Complex must track the state of the four INTx lines indepen‐ dently and convert them into system interrupts in an implementation‐spe‐ cific way. 

**207** 

## **PCI Ex ress Technolo p gy** 

9. They use the routing type “Local‐Terminate at Receiver” to allow a Switch to remap the designated interrupt pin when necessary (see “Mapping and Collapsing INTx Messages” on page 808). Consequently, the Requester ID in an INTx message may be assigned by the last transmitter. 

**Power Management Messages.** PCI Express is compatible with PCI power management, and adds hardware‐based Link power management as well. Messages are used to convey some of this information, but to learn how the overall PCIe power management protocol works, refer to Chapter 16, enti‐ tled ʺPower Management,ʺ on page 703. Table 5‐10 on page 208 summarizes the four power management message types. 

_Table 5‐10: Power Management Message Coding_ 

|**Power Management Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|PM_Active_State_Nak|0001 0100b|100b|
|PM_PME|0001 1000b|000b|
|PM_Turn_Off|0001 1001b|011b|
|PME_TO_Ack|0001 1011b|101b|



Power Management Message Rules: 

1. Power Management Messages don’t have a data payload, so the Length field is reserved. 

2. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

3. PM_Active_State_Nak is sent from a Downstream Port after it observes a request from the Link neighbor to change the Link power state to L1 but it has chosen not to do so (Local ‐ Terminate at Receiver routing). 

4. PM_PME is sent upstream by the component requesting a Power Manage‐ ment Event (Implicitly Routed to the Root Complex). 

5. PM_Turn_Off is sent downstream to all endpoints (Implicitly Broadcast from the Root Complex routing). 

6. PME_TO_Ack is sent upstream by endpoints. For switches with multiple Downstream Ports, this message won’t be forwarded upstream until all Downstream Ports have received it (Gather and Route to the Root Complex routing). 

**208** 

**Chapter 5: TLP Elements** 

**Error Messages.** Error Messages are sent upstream (Implicitly Routed to the Root Complex) by enabled components that detect errors. To assist software in knowing how to service the error, the Error Message identifies the requesting agent in the Requester ID field of the message header. Table 5‐11 on page 209 describes the three error message types. 

_Table 5‐11: Error Message Coding_ 

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|ERR_COR (Correctable)|0011 0000b|000b|
|ERR_NONFATAL<br>(Uncorrectable, Non‐fatal)|0011 0001b||
|ERR_FATAL<br>(Uncorrectable, Fatal)|0011 0011b||



Error Signaling Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, so the Length field is reserved. 

3. The Root Complex converts Error Messages into system‐specific events. 

**Locked Transaction Support.** The Unlock Message is used as part of the Locked transaction protocol defined for PCI and still available to Legacy Devices. The protocol begins with a Memory Read Locked Request. When that Request is seen by Ports along the path to the target device, they implement an atomic read‐modify‐write protocol by locking out other Requesters from using VC0 until the Unlock Message is received. This Message is sent to the target to release all the Ports in the path to it and finish the Locked Transaction sequence. Table 5‐12 on page 209 summarizes the coding for this message. 

_Table 5‐12: Unlock Message Coding_ 

|**Unlock Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Unlock|0000 0000b|011b|



**209** 

**PCI Ex ress Technolo p gy** 

Unlock Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

**Set Slot Power Limit Message.** This is sent from a Downstream Port to the device plugged into the slot. This power limit is stored in the endpoint in its Device Capabilities Register. Table 5‐13 summarizes the message coding. 

_Table 5‐13: Slot Power Limit Message Coding_ 

|**Slot Power Limit Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Set_Slot_Power_Limit|0101 0000b|100b|



Set_Slot_Power_Limit Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. The data payload is 1 DW and so the Length field is set to one. Only the lower 10 bits of the 32‐bit data payload are used for slot power scaling; the upper payload bits must be set to zero. 

3. This message is sent automatically anytime the Data Link Layer transitions to DL_Up status or if a configuration write to the Slot Capabilities Register occurs while the Data Link Layer is already reporting DL_Up status. 

4. If the card in the slot already consumes less power than the power limit specified, it’s allowed to ignore the Message. 

**Vendor‐Defined Message 0 and 1.** These are intended to allow expan‐ sion of the PCIe messaging capabilities either by the spec or by vendor‐specific extensions. The header for them is shown in Figure 5‐12 on page 211, and the codes are given in Figure 5‐14 on page 211. 

**210** 

**Chapter 5: TLP Elements** 

_Figure 5‐12: Vendor‐Defined Message Header_ 

**==> picture [368 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 1Fmt 1  0  r  r  rType R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 1 1 1 1 1 1 x<br>Byte 8 Target BDF if ID Routing used, Vendor ID<br>otherwise Reserved<br>Byte 12 For Vendor Definition<br>**----- End of picture text -----**<br>


_Table 5‐14: Vendor‐Defined Message Coding_ 

|**Vendor‐Defined Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Vendor Defined Message 0|0111 1110b|000b, 010b,<br>011b, 100b|
|Vendor Defined Message 1|0111 1111b||



Vendor‐Defined Message Rules: 

1. A data payload may or may not be included with either type. 

2. Messages are distinguished by the Vendor ID field. 

3. Attribute bits [2] and [1:0] are not reserved. 

4. If the Receiver doesn’t recognize the Message: 

   - Type 1 Messages are silently discarded 

   - Type 0 Messages are treated as an Unsupported Request error condi‐ tion 

**Ignored Messages.** Listing an entire category of Messages that are to be ignored sounds a little strange without the context for it. These were formerly Hot Plug Signaling messages that supported devices that had Hot Plug indica‐ tors and push buttons on the add‐in card itself rather than on the system board. This Message type was defined through spec rev 1.0a, but this option was no longer supported beginning with the 1.1 spec release, so the details are only included here for reference. As the name now suggests, Transmitters are 

**211** 

**PCI Ex ress Technolo p gy** 

strongly encouraged not to send these messages, and Receivers are strongly encouraged to ignore them if they are seen. If they’re still going to be used any‐ way, they must conform to the 1.0a spec details. 

_Table 5‐15: Hot Plug Message Coding_ 

|**Error Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|Attention_Indicator_On|0100 0001b|100b|
|Attention_Indicator_Blink|0100 0011b|100b|
|Attention_Indicator_Off|0100 0000b|100b|
|Power_Indicator_On|0100 0101b|100b|
|Power_Indicator_Blink|0100 0111b|100b|
|Power_Indicator_Off|0100 0100b|100b|
|Attention_Button_Pressed|0100 1000b|100b|



Hot Plug Message Rules: 

- They are driven by a Downstream Port to the card in the slot. 

- The Attention Button Message is driven upstream by a slot device. 

**Latency Tolerance Reporting Message.** LTR Messages are used to optionally report acceptable read/write service latencies for a device. To learn more about this power management technique, see the section called “LTR (Latency Tolerance Reporting)” on page 784. 

_Figure 5‐13: LTR Message Header_ 

**==> picture [346 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1 0 0 0 0<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>**----- End of picture text -----**<br>


**212** 

**Chapter 5: TLP Elements** 

_Table 5‐16: LTR Message Coding_ 

|**Latency Tolerance Reporting Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|LTR|0001 0000|100|



LTR Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

**Optimized Buffer Flush and Fill Messages.** OBFF Messages are used to report platform power status to Endpoints and facilitate more effective sys‐ tem power management. To learn more about this technique, see the discussion called “OBFF (Optimized Buffer Flush and Fill)” on page 776. 

_Figure 5‐14: OBFF Message Header_ 

**==> picture [346 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1Fmt 1 0 1 0 0Type R TC R Attr R HT DT EP Attr AT Length<br>Message Code<br>Byte 4 Requester ID Tag 0 0 0 1  0 0 1 0<br>Byte 8 Reserved<br>OBFF<br>Byte 12 Reserved<br>Code<br>**----- End of picture text -----**<br>


_Table 5‐17: LTR Message Coding_ 

|**Optimized Buffer Flush/Fill Message**|**Message Code 7:0**|**Routing 2:0**|
|---|---|---|
|OBFF|0001 0010|100|



**213** 

## **PCI Ex ress Technolo p gy** 

## OBFF Message Rules: 

1. They’re required to use the default traffic class TC0. Receivers must check for this and handle violations as Malformed TLPs. 

2. They don’t have a data payload, and the Length field is reserved. 

3. The Requester ID must be set to the Transmitting Port’s ID. 

**214** 

## _**6**_ 

## _**Flow Control**_ 

## **The Previous Chapter** 

The previous chapter discusses the three major classes of packets: _Transaction Layer Packets_ (TLPs), _Data Link Layer Packets_ (DLLPs) and _Ordered Sets_ . This chapter describes the use, format, and definition of the variety of TLPs and the details of their related fields. DLLPs are described separately in Chapter 9, enti‐ tled ʺDLLP Elements,ʺ on page 307. 

## **This Chapter** 
