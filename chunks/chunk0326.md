Consider the following example of the handshake sequence required for remov‐ ing the reference clock and power from PCIe devices in the fabric. This example assumes a system‐wide power down is being initiated, but the sequence can also apply to individual devices. The steps are summarized below and shown in Figure 16‐26 on page 766. The overall sequence is represented in two parts labeled A and B. The Link state transitions involved in the complete sequence include: 

- L0 ‐‐> L1 (when software places a device into D3) 

- L1 ‐‐> L0 (when software initiates a PME_Turn_Off message) 

- L0 ‐‐> L2/L3 Ready (resulting from the completion of the PME_Turn_Off handshake sequence, which culminates in a PM_Enter_L23 DLLP being sent by the device and the Link going to electrical idle) 

The following steps detail the sequence illustrated in Figure 16‐26 on page 766. 

1. Power Management software first places all Functions in the PCIe fabric into their D3 state. 

2. All devices transition their Links to the L1 state when they enter D3. 

3. Power Management software initiates a PME_Turn_Off TLP message, 

**764** 

**Chapter 16: Power Management** 

which is broadcast from all Root Complex ports to all devices. This prevents PME Messages from being lost in case they were in progress upstream when power was removed. Note that delivery of this TLP causes each Link to transition back to L0 so it can be forwarded downstream. 

4. All devices must receive and acknowledge the PME_Turn_Off message by returning a PME_TO_ACK TLP message while in the D3 state. 

5. Switches collect the PME_TO_ACK messages from all of their enabled downstream ports and forward just one aggregated PME_TO_ACK mes‐ sage upstream toward the Root Complex. That’s because these messages have the routing attribute set as “Gather and Route to the Root”. 

6. After sending the PME_TO_ACK, when it is ready to have the reference clock and power removed, devices send a PM_Enter_L23 DLLP repeatedly until a PM_Request_ACK DLLP is returned. The Links that enter the L2/L3 Ready state last are those attached to the device originating the PME_Turn_Off message (the Root Complex in this example). 

7. The reference clock and power can finally be removed when all Links have transitioned to the L2/L3 state, but not sooner than 100ns after that. If auxil‐ iary power (VAUX) is supplied to the devices, the Link transitions to L2. If no AUX power is available the Links will be in the L3 state. 

**765** 

## **PCI Ex ress Technolo p gy** 

_Figure 16‐26: Negotiation for Entering L2/L3 Ready State_ 

**==> picture [298 x 479] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>1. Software has previously placed all functions 2. Software generates a PME_Turn_Off<br>into the D3 state and all have transitioned their broadcast message to tempoarily disable<br>link to L1 as required. PME Messages.<br>L1 State    L0 State<br>PM State D3 (F) 3. As the PME_Turn_Off messagereaches the downstream root port and<br>Switch downstream ports of each switch an<br>L1 to L0 transition must occur to<br>transmit the message.<br>L1 State    L0 State<br>L1 State    L0 State<br>PM State D3 PM State L1   L0 PM State D3<br>PCIe D3 (C) PCIe<br>5. Switches wait until all down-Endpoint Switch Endpoint<br>stream ports have sent their ACK(D) (E)<br>message. They then return a single<br>aggregate message upstream.<br>L1 State    L0 State L1 State    L0 State<br>PM State D3 4. Each device receives thePCI_Turn_Off message andPCI-XP PCIe PM State D3<br>A Endpointsends a PME_TO_ACK message. Endpoint PME_Turn_Off Message<br>(A) (B)<br>PME_TO_ACK Message<br>Root Complex<br>8. When all links attached to the device that originated the<br>PME_Turn_Off have entered the L2/L3 Ready state, the<br>reference clock and power can be removed, but no sooner<br>than 100ns after observing L2/L3 Ready on all links. L0 State    L2/L3 Ready State<br>PM State D3 (F)<br>Switch<br>L0 State    L2/L3 Ready State L0 State    L2/L3 Ready State<br>PM State D3 PM State PM State D3<br>6. After each downstream component has sent the PCIe D3 (C) PCIe<br>PCI_TO_ACK, they send the PM_Enter_L23 DLLPrepeatedly until they receive a PME_Request_Ack.This causes the downstream device to issue anEndpoint(D) Switch 7. Switches wait until all downstream ports have transitioned to the L2/L3 Ready statebefore sending the PM_Enter_L23 DLLPEndpoint(E)<br>electrical idle ordered set, after which it enters idle. upstream.<br>The upstream device detects electrical idle and also<br>enters idle. The link is now in the L1/L3 Ready state.<br>L0 State    L2/L3 Ready State L0 State    L2/L3 Ready State<br>PM State D3 PM State D3<br>PCIe PCIe<br>B Endpoint Endpoint PM_Enter_L23 DLLP<br>(A) (B)<br>**----- End of picture text -----**<br>


**766** 

**Chapter 16: Power Management** 

## **Exiting the L2/L3 Ready State — Clock and Power Removed** 

As illustrated in the state diagram in Figure 16‐27, a device exits the L2/L3 Ready state when power is removed and has only two choices. When VAUX is available the transition is to L2, otherwise the transition is to L3. 

Link state transitions are normally controlled by the LTSSM in the Physical Layer. However, transitions to L2 and L3 result from main power being removed and the LTSSM is not operational then. Consequently, the spec refers to L2 and L3 as pseudo‐states defined for explaining the resulting condition of a device when power is removed. 

_Figure 16‐27: State Transitions from L2/L3 Ready When Power is Removed_ 

## **The L2 State** 

Some devices are designed to monitor external events and initiate a wakeup sequence to restore power to handle them. Since main power is removed, these device will need a power source like VAUX to be able to monitor the events and to signal a wakeup. 

## **The L3 State** 

In this state the device has no power and therefore no means of communication. Recovery from this state requires the system to restore power and the reference clock. That causes devices to experience a fundamental reset, after which they’ll need be initialized by software to return to normal operation. 

**767** 

**PCI Ex ress Technolo p gy** 

## **Link Wake Protocol and PME Generation** 

The wake protocol provides a method for an Endpoint to reactivate the upstream Link and request that software return it to D0 so it can perform required operations. PCIe PM is designed to be compatible with PCI‐PM soft‐ ware, although the methods are different. 

Rather than using a sideband signal, PCIe devices use an inband PME message to notify PM software of the need to return the device to D0. The ability to gen‐ erate PME messages may optionally be supported in any of the low power states. Recall that a device reports which PM states it supports for PME message delivery. 

PME messages can only be delivered when the Link state is L0. The latency involved in reactivating the Link is based on a device’s PM and Link state, but can include the following: 

1. Link is in non‐communicating (L2) state — when a Link is in the L2 state it cannot communicate because the reference clock and main power have been removed. No PME message can be sent until clock and power are restored, a Fundamental Reset is asserted, and the Link is re‐trained. These events will be triggered when a device signals a wakeup. This may result in all Links being re‐awakened in the path between the device needing to com‐ municate and the Root Complex. 

2. Link is in communicating (L1) state — when a Link is in the L1 state clock and main power are still active; thus, a device simply exits the L1 state, goes to the Recovery state to re‐train the Link, and returns the Link to L0. Once the Link is in L0 the PME message is delivered. Note that the devices never send a PME message while in the L2/L3 Ready state because entry into that state only occurs after PME notification has been turned off, in preparation for clock and power to be removed. (See “L2/L3 Ready Handshake Sequence” on page 764.) 

3. PME is delivered (L0) — If the Link is in the L0 state, the device transfers the PME message to the Root Complex, notifying Power Management soft‐ ware that the device has observed an event that requires the device be placed back into its D0 state. Note that the message contains the Requester ID (Bus#, Device#, and Function#) of the device. This quickly informs soft‐ ware which device needs service. 

**768** 

**Chapter 16: Power Management** 

## **The PME Message** 

The PME message is delivered by devices that support PME notification. The message format is illustrated in Table 16‐28 on page 769. The message may be initiated by a device in a low power state (D1, D2, D3hot, and D3cold) and is sent immediately upon return of the Link to L0. 

_Figure 16‐28: PME Message Format_ 

**==> picture [366 x 335] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>PME Switch<br>Message<br>PME Message Request TLP<br>Framing Sequence Framing<br>Header Digest LCRC<br>(STP) Number (End)<br>PCIe<br>Endpoint<br>Route to Root Complex<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 1Fmt 1  0Type 0  0  0 R TC R Attr R HT DT EP Attr0 0 0 0AT Length<br>Message Code<br>Byte 4 Requester ID Tag<br>0001 1000<br>Byte 8 Reserved<br>Byte 12 Reserved<br>**----- End of picture text -----**<br>


**769** 

**PCI Ex ress Technolo p gy** 

The PME message is a Transaction Layer Packet that has the following charac‐ teristics: 

- TC and VC are zero (no QoS applies) 

- Routed implicitly to the Root Complex 

- Handled as Posted Transaction 

- Relaxed Ordering is not permitted, forcing all transactions in the fabric between the signaling device and the Root Complex to be delivered to the Root Complex ahead of the PME message 

## **The PME Sequence** 

Devices may support PME in any of the low power states as specified in the PM Capabilities register. This register also specifies the amount of VAUX current used by the device if it supports wakeup in the D3cold state. The basic sequence of events associated with sending a PME to software is specified below and pre‐ sumes that the device and system are enabled to generate PME and the Link has already been transitioned to the L0 state: 

1. The device issues the PME message on its upstream port. 

2. PME messages are implicitly routed to the Root Complex. Switches in the path transition their upstream ports to L0 if necessary and forward the packet upstream. 

3. A root port receives the PME and forwards it to the Power Management Controller. 

4. The controller informs power management software, typically with an interrupt. Software uses the Requester ID in the message to read and clear the PME_Status bit in the PMCSR and return the device to the D0 state. Depending on the degree of power conservation, the PCI Express driver may also need to restore the devices configuration registers. 

5. PM Software may also call the device driver in the event that device context was lost as a result of being placed in a low power state. If so, device soft‐ ware restores information within the device. 

## **PME Message Back Pressure Deadlock Avoidance** 

## **Background** 

The Root Complex typically stores the PME messages it receives in a queue, and calls PM software to handle each one. A PME is held in this queue until PM soft‐ 

**770** 

**Chapter 16: Power Management** 

ware reads the PME_Status bit from the requesting device’s PMCSR register. Once the configuration read transaction completes, this PME message can be removed from the internal queue. 

## **The Problem** 

Deadlock can occur if the following scenario develops: 

1. Incoming PME Messages have filled the PME message queue but other PME messages have been issued downstream from the same root port. 

2. PM software initiates a configuration read request from the Root to read PME_Status from the oldest PME requester. 
