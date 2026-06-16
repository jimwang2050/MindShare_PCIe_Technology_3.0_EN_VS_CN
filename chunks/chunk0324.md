**----- Start of picture text -----**<br>
Device Function<br>PCIe-Core<br>Hardware/Software<br>6. Device blocks new TLP<br>Interface<br>scheduling<br>7. ACK received for last TLP<br>Transaction Layer<br>(Retry Buffer empty)<br>8. All FC credits sufficient to send a<br>5. PM_Active_State_Request L1<br>received Data Link Layer maximum-sized transaction<br>12. Electrical Idle ordered set received 9. PM_Request_ACK sent<br>Causing TLP and DLLP transmission Physical Layer continuously until electrical<br>to be disabled  idle ordered set is received<br>(RX) (TX)<br>11. Electrical Idle ordered set<br>is sent and transmitter goes (Link) 13. Transmit lanes are placed into<br>to Electrical idle Electrical idle<br>(TX) (RX)<br>Physical Layer<br>4. PM_Active_State_Request L1 sent<br>continuously until PM_Request_ACK<br>received from the opposite port Data Link Layer 10. PM_Request_ACK received,<br>3. All FC credits sufficient to send  causing TLP and DLLP Packet<br>a maximum-sized transaction transmission to be disabled<br>Transaction Layer<br>2. ACK received for last TLP<br>(Retry Buffer empty)<br>PCIe-Core<br>1. Device blocks new TLP scheduling Hardware/Software<br>Interface<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


## **Scenario 2: Upstream Component Transmits TLP Just Prior to Receiving L1 Request** 

This scenario presumes that the upstream component has just been instructed by its core logic to send a TLP downstream before it receives the request to enter L1 from the downstream device. Several negotiation rules define the actions to ensure that this situation is managed correctly. 

**750** 

**Chapter 16: Power Management** 

**TLP Must Be Accepted by Downstream Component.** Note that after the downstream device sends the PM_Active_State_L1 DLLP it must wait for a response from the upstream component. While waiting, the down‐ stream component must be able to accept TLPs and DLLPs from the upstream device. Although it won’t send any TLPs, it must be able to send DLLPs as needed, such as ACKs for incoming TLPs. In this case, two possi‐ bilities exist: 

- an ACK is returned to verify successful receipt of the TLP. 

- a NAK is returned if a TLP transmission error is detected. The resulting retry of the TLP is allowed during the L1 negotiation. 

**Upstream Component Receives Request to Enter L1.** The spec requires that the upstream component immediately accept or reject the request to enter the L1 state. However, it further states that prior to sending a PM_Request_ACK it must: 

1. Block scheduling of new TLPs 

2. Wait for acknowledgement of the last TLP previously sent, if necessary, and retry TLPs that receive a NAK, unless a Link Acknowledgement timeout condition occurs. 

Once all outstanding TLPs have been acknowledged, and all other condi‐ tions are satisfied, the upstream device must return a PM_Request_ACK DLLP. 

## **Scenario 3: Downstream Component Receives TLP During Negotiation** 

During the negotiation sequence the downstream device may be instructed to send a new TLP upstream. However, a device that begins the L1 ASPM negotia‐ tion process must block new TLP scheduling. This prevents a race condition between going into L1 and sending a new TLP that would prevent entry into L1. Consequently, once the downstream device has scheduled delivery of the PM_Request_L1 it must complete the transition to L1 if a PM_Request_ACK is received. Sending a new TLP will have to wait until L1 has been entered, after which the device can initiate a transition from L1 back to L0 to send the TLP. 

## **Scenario 4: Upstream Component Receives TLP During Negotiation** 

If the upstream component needs to send a TLP or DLLP after sending the PM_Request_Ack, it must first complete the transition to L1. It can then initiate a change from L1 to L0 to send the packet. 

**751** 

**PCI Ex ress Technolo p gy** 

## **Scenario 5: Upstream Component Rejects L1 Request** 

Figure 16‐18 on page 752 summarizes the negotiation sequence when the upstream component rejects the request to enter the L1 ASPM state. The negoti‐ ation begins normally as the downstream component requests L1. However, the upstream device returns a PM_Active_State_Nak TLP to reject the request. The reasons for rejecting the request to enter L1 include: 

- L1 ASPM not supported or software has not enabled this feature 

- One or more TLPs are scheduled for transfer across the Link 

- ACK or NAK DLLPs are scheduled for transfer 

Once the rejection message has been sent, the upstream component can con‐ tinue sending TLPs and DLLPs as needed. The rejection tells the downstream component that L1 is not an option at present, and so it must transition to L0s instead, if possible. 

_Figure 16‐18: Negotiation Sequence Resulting in Rejection to Enter L1 ASPM State_ 

**==> picture [304 x 279] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Function<br>PCIe-Core<br>Hardware/Software<br>Interface<br>6. PM_Active_State_NAK<br>Transaction Layer<br>TLP request sent<br>5. PM_Active_State_Request L1<br>received Data Link Layer<br>Physical Layer<br>(RX) (TX)<br>8. Transmit link of downstream<br>    device is transitioned to  (Link)<br>    L0s state assuming all<br>    conditions met (TX) (RX)<br>Physical Layer<br>4. PM_Active_State_Request L1 sent<br>continuously until response received Data Link Layer 7. PM_Active_State_NAK received<br>3. All FC credits sufficient to send<br>a maximum-sized transaction Transaction Layer<br>2. ACK received for last TLP<br>PCIe-Core<br>(Retry Buffer empty) Hardware/Software<br>1. Device blocks TLP scheduling at Interface<br>Transaction Layer<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


**752** 

**Chapter 16: Power Management** 

## **Exit from L1 ASPM State** 

Either component can initiate the transition from L1 back to L0 when it needs to use the Link. The procedure is the same in either case and doesn’t involve any negotiation. When switches are involved in exiting from L1 the spec requires that other switch ports in the ASPM low power states must also transition to the L0 state if they are in the possible path of the packet that will be sent. These issues are discussed in subsequent sections. 

**L1 ASPM Exit Signaling.** The spec states that exit from L1 is invoked by exiting electrical idle, which begins by sending TS1s. The receiving port responds by sending TS1s back to the originating device and the Physical Layer follows its LTSSM protocol to complete the Recovery state and return the Link to L0. Refer to“Recovery State” on page 571 for details. 

**Switch Receives L1 Exit from Downstream Component.** As pic‐ tured in Figure 16‐19, the Switch must respond to L1 exit on the down‐ stream port by returning TS1s and, within 1μs (from signal L1 Exit downstream), it must also exit L1 on its upstream Link if it was in that state. 

**753** 

## **PCI Ex ress Technolo p gy** 

_Figure 16‐19: Switch Behavior When Downstream Component Signals L1 Exit_ 

**==> picture [335 x 329] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>6. RC signals L1  L1 ASPM State<br>exit to Switch F<br>PM State D0 5. Within 1μs of<br>step 4, Switch F<br>Switch signals L1 Exit to RC<br>(F)<br>L1 ASPM State L1 State<br>4. Switch F signals L1<br>exit to Switch C L1 ASPM<br>State<br>3. Within 1μs of step 2,<br>PM State D0 PM State Switch C signals  PM State D1<br>PCIe D0 L1 Exit to Switch FPCI-XP<br>Endpoint Switch Endpoint<br>(D) (E)<br>(C)<br>L1 ASPM State<br>L1 State 1. EP B signals<br>L1 Exit to Switch C<br>2. Switch C signals<br>L1 Exit to EP B<br>PM State D2 PM State D0<br>PCIe PCIe<br>Endpoint Endpoint<br>(A) (B)<br>**----- End of picture text -----**<br>


Presumably the reason the downstream component is transitioning back to L0 is because it’s preparing to send a TLP upstream. Since L1 exit latencies are relatively long, a switch “must not wait until its Downstream Port Link has fully exited to L0 before initiating an L1 exit transition on its Upstream Port Link.” This prevents accumulated latencies that would otherwise result if all L1 to L0 transitions occurred in a sequential fashion. 

**Switch Receives L1 Exit from Upstream Component.** In this case, the switch must respond with TS1s back upstream, and within 1μs it must also send TS1s to all downstream ports that are in the L1 ASPM state to return them to L0. As in the previous example, the goal is to minimize the 

**754** 

**Chapter 16: Power Management** 

overall exit latency of returning to the L0 state for every Link in the path from the initiator to the target of the transaction. Figure 16‐20 on page 755 summarizes these requirements. The Link between Switch F and EndPoint (EP) E is in the L1 state because software put EP E into the D1 state, which caused the Link to transition to L1. Only Links in the L1 ASPM state are transitioned to L0 as a result of the Root Complex (RC) initiating the exit from L1 ASPM. 

_Figure 16‐20: Switch Behavior When Upstream Component Signals L1 Exit_ 

**==> picture [331 x 322] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>1. RC signals  L1 Exit  L1 ASPM State<br>to Switch F 2. Switch F signals<br>PM State D0 L1 Exit to RC<br>Switch<br>3. Within 1μs of<br>step 2, Switch F  (F)<br>signals L1 Exit to<br>EP D  & Switch C<br>L1 State<br>L1 ASPM State<br>L1 ASPM<br>State<br>4b. EP D signals  4a. Switch C signals<br>L1 Exit to Switch F L1 Exit to Switch F<br>PM State PM State D1<br>PM State D0 PCIe D0 PCIe<br>Endpoint Switch Endpoint<br>(D) (E)<br>(C)<br>L1 ASPM State<br>L1 State<br>6. EP B signals<br>5. Within 1μs of step  L1 Exit to Switch C<br>4a, Switch C signals<br>L1 Exit to EP B<br>PM State D3 PM State D0<br>PCIe PCIe<br>Endpoint Endpoint<br>(A) (B)<br>**----- End of picture text -----**<br>


**755** 

**PCI Ex ress Technolo p gy** 

## **ASPM Exit Latency** 

PCI Express provides mechanisms to ensure that the ASPM exit latencies for L0s and L1 don’t exceed the requirements of the devices. All devices report their L0s and L1 exit latencies, and Endpoints also report the total acceptable latency they can tolerate for this when performing accesses to and from the Root Com‐ plex. This acceptable latency is based on the data buffer size within the device. If the chain of devices that reside between the Endpoint and target device have a total latency that exceeds the acceptable latency reported by the Endpoint, software can disable ASPM for a given Endpoint. 

The exit latencies reported by a device will change depending on whether the devices on each end of a Link share a common reference clock or not. Conse‐ quently, the Link Status register includes a bit called _Slot Clock_ that specifies whether the component uses an external reference clock provided by the plat‐ form, or an independent reference clock (perhaps generated internally). Soft‐ ware checks these bits in devices at both ends of each Link to determine whether they both use it and thus share a common clock. If so, software sets the _Common Clock_ bit to report this in both devices. Figure 16‐21 on page 757 illus‐ trates the registers and related bit fields involved in managing the ASPM exit latency. 

## **Reporting a Valid ASPM Exit Latency** 

Because the clock configuration affects the exit latency that a device will experi‐ ence, devices must report the source of their reference clock via the _Slot Clock_ status bit within the Link Status register. This bit is initialized by the component to report the source of its reference clock. If this bit is set to 1, the clock uses the platform generated reference clock and if it’s cleared (0) an independent clock is used. 
