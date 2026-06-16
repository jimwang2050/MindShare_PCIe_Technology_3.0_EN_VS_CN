# 📘 第 16 章　电源管理 (Chapter 16. Power Management)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0323.md` ... `chunks/chunk0331.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Power Management](#-本章目录-table-of-contents)

<a id="sec-16-1"></a>
## 16.1 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|11b|Both L0s and L1 enabled|



_Figure 16‐15: Active State PM Control Field_ 

**==> picture [296 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


## **L0s State** 

L0s is a Link power state that can only be entered under hardware control and is applied to a single direction of the Link. For example, a large volume of traffic in conventional PC‐based systems results from Functions sending data to main system memory. As a result, the upstream lanes carry heavy traffic while the downstream lanes may carry very little. These downstream lanes can enter the L0s state to conserve power during stretches of idle bus time. 

**744** 

**Chapter 16: Power Management** 

## **Entry into L0s** 

A Transmitter initiates a change from L0 to L0s after detecting a period of idle time that is implementation specific. 

**Entry into L0s.** Entry is managed for a single direction of the Link based on detecting a period of Link idle time. Ports are required to enter L0s after detecting idle time of no greater than 7μs. 

Idle is defined differently for Endpoints and Switches. The reason for this is a desire to minimize recovery time as Link recovery time propagates through Switches. For example, if a Switch upstream port was in a low power state and now sees activity, it means that a TLP is probably on its way down to the Switch. Where will the packet need to be routed? It will go to one of the downstream ports, but rather than wait to receive the packet and determine which port will be the target before starting to wake it up, the lowest‐latency approach would be to wake all the downstream ports so that the one that turns out to be the target will be ready as quickly as possi‐ ble. 

Basic rules regarding idle time: 

- **Endpoint Port or Root Port** : 

   - No TLPs are pending transmission or a lack of Flow Control credits is temporarily blocking them. 

   - No DLLPs are pending transmission. 

- **Upstream Switch Port** : 

   - The receive lane of all downstream ports are already in L0s. 

   - No TLPs are pending transmission or a lack of Flow Control credits is temporarily blocking them. 

   - No DLLPs are pending transmission. 

- **Downstream Switch Port** : 

   - The Switch’s Upstream Port’s Receive Lanes are in L0s. 

   - No TLPs are pending transmission or a lack of Flow Control credits is temporarily blocking them. 

   - No DLLPs are pending for transmission 

The Transaction and Data Link Layers are unaware of whether the Physical Layer transmitter has entered L0s, but the idle conditions that trigger a tran‐ sition to L0s must be continuously reported from the Transaction and Link layers to the Physical Layer so it can make timely choices about this. Note that a port must always tolerate L0s on its receiver, even if software has dis‐ abled ASPM. This allows a device at the other end of the Link that is enabled for ASPM to still transition one side of the Link to the L0s state. 

**745** 

**PCI Ex ress Technolo p gy** 

**Flow Control Credits Must be Delivered.** One situation that qualifies as idle time is a pending TLP that is blocked due to insufficient FC credits. When flow control credits are received that allow delivery of the pending TLP, the transmitting port must initiate a return to L0. Also, if the receive buffer associated with the transmitter in L0s makes additional flow control credits available, the transmitter must return to L0 and deliver the FC_Update DLLP to the neighbor. 

**Transmitter Initiates Entry to L0s.** When sufficient idle time has been observed by a Transmitter, it forces a transition from L0 to L0s by sending an “electrical idle” ordered set (EIOS) to the receiver and stopping trans‐ mission. The transmitter and receiver are now in their electrical idle states and have reduced power consumption. Synchronization between the trans‐ mitter and receiver has been lost and retraining will be required for recov‐ ery. The spec requires that the PLL logic in the receiver must remain active (powered) to allow quick recovery from L0s back to L0. 

## **Exit from L0s State** 

If the transmitter detects that the idle condition is no longer true, it must initiate the exit from L0s to L0. The spec encourages designers to monitor events that give an early indication that an L0s exit is imminent and start the recovery pro‐ cess to speed up the transition back to L0. For example, if the Receiver of the port receives a non‐posted Request, the Transmitter knows that it will soon be asked to send a Completion in response. Consequently, the Transmitter can go ahead and start the exit process so the Link state is L0 by the time it is asked to deliver the Completion. 

**Transmitter Initiates L0s Exit.** To exit L0s, the Transmitter sends one or more Fast Training Sequence (FTS) Ordered Sets. The number of these required by the Link partner’s Receiver was communicated earlier during Link training (N_FTS field in the TS1s and TS2s used in training). After sending the requested number of FTSs, one SOS is delivered. The receiver should be able to establish bit lock and symbol lock or Block lock, and should be ready to resume normal operation. 

**Actions Taken by Switches that Receive L0s Exit.** A switch that receives an L0s to L0 transition sequence on one port may also need to ini‐ tiate an L0s exit to other of its ports. Two specific cases are considered: 

- **Switch Downstream Port Receives L0s to L0 transition.** The switch must signal an L0s to L0 on its upstream port if it is currently in the L0s state because the packet coming up from the Endpoint or downstream switch will most likely need to go upstream to the Root Complex. 

**746** 

**Chapter 16: Power Management** 

- **Switch Upsteam Port Receives L0s to L0 transition.** The switch must signal an L0s to L0 transition on all downstream ports currently in the L0s state because it doesn’t want to wait until the packet arrives to begin waking the target path. 

Switch ports that were put into L1 by a software change to the device power state remain unaffected by L0s to L0 transitions. However, once the upstream Link has completed the transition to L0, a subsequent transaction may target this port, causing a transition from L1 to L0. 

## **L1 ASPM State** 

The optional L1 ASPM state provides deeper power savings than L0s, but has a greater recovery latency. This state results in both directions of the Link going into the L1 state and results in Link and Transaction layer deactivation within each device. 

Entry into this state is requested by an upstream port, such as from an Endpoint or the upstream port of a switch (upstream ports are shaded as shown in Figure 16‐16). The downstream port responds to this request and either agrees to go into L1 or rejects the request through a negotiation process with the down‐ stream component. Exiting L1 ASPM can be initiated by either the downstream or upstream port. 

_Figure 16‐16: Only Upstream Ports Initiate L1 ASPM_ 

**747** 

**PCI Ex ress Technolo p gy** 

## **Downstream Component Decides to Enter L1 ASPM** 

The spec does not precisely define all conditions under which an Endpoint or upstream port of a switch decides to attempt entry into the L1 ASPM state but does suggest that one case might be when both sides of the Link have been in L0s for a preset amount of time. The requirements given include: 

- ASPM L1 entry is supported and enabled 

- Device‐specific requirements for entering L1 have been satisfied 

- No TLPs are pending transmission 

- No DLLPs are pending transmission 

- If the downstream component is a switch, then all of the switch’s down‐ stream ports must be in the L1 or higher power conservation state before the upstream port can initiate L1 entry. 

## **Negotiation Required to Enter L1 ASPM** 

Because of the longer latency required to recover from L1 ASPM, a negotiation process is employed to ensure that the port at the other end of the Link is enabled for L1 ASPM and is prepared to enter it. The negotiation involves send‐ ing several packets: 

- PM_ Active_State_Request_L1 DLLP — issued by the downstream port to start the negotiation process. 

- PM_ Request_Ack DLLP — returned by the upstream port when all of its requirements to enter L1 ASPM have been satisfied. 

- PM_Active_State_Nak message TLP — returned by the upstream port when it is unable to enter the L1 ASPM state. 

The upstream component may or may not accept the transition to the L1 ASPM state. The following scenarios describe a variety of circumstances that result in both conditions. 

## **Scenario 1: Both Ports Ready to Enter L1 ASPM State** 

Figure 16‐17 on page 750 summarizes the sequence of events that must occur to enable transition to the L1 ASPM state. This scenario assumes that all transac‐ tions have completed in both directions and no new transaction requirements emerge during the negotiation. 

**Downstream Component Requests L1 State.** If the downstream com‐ ponent wishes to transition to the L1 state, it can send the request to enter L1 after the following steps have completed: 

**748** 

**Chapter 16: Power Management** 

1. TLP scheduling is blocked at the Transaction Layer. 

2. The Link Layer has received acknowledgement for the last TLP it had previously sent and the replay buffer is empty. 

3. Sufficient flow control credits are available to allow transmission of the largest possible packet for any FC type. This ensures that the compo‐ nent can issue a TLP immediately upon exiting the L1 state. 

The downstream component then delivers the PM_ Active_State_Request_L1 to notify the upstream component of the request to enter the L1 state. This is sent repeatedly until the upstream component responds — either a PM_Request_ACK DLLP or a PM_Active_State_NAK message. 

**Upstream Component Response to L1 ASPM Request.** Down‐ stream ports (i.e., ports of an upstream component that face downward) must accept a request to enter a low power L1 state if all of the following conditions are true: 

- The Port supports ASPM L1 entry and is enabled to do so 

- No TLP is scheduled for transmission 

- No Ack or Nak DLLP is scheduled for transmission 

**Upstream Component Acknowledges Request to Enter L1.** The 

upstream component sends a PM_Request_ACK to notify the downstream component of its agreement to enter the L1 ASPM state after it: 

1. Block scheduling of any new TLPs. 

2. Receive acknowledgement for the last TLP previously sent (meaning its replay buffer is empty). 

3. Ensure enough flow control credits are available to send the largest possible packet for any FC type so that it can issue a TLP immediately after exiting the L1 state. 

The Upstream component then sends PM_Request_Ack continuously until it detects the EIOS on its receive lanes, indicating that the downstream device has entered Electrical Idle. 

**Downstream Component Sees Acknowledgement.** When the Down‐ stream component sees the PM_Request_Ack, it stops sending the PM_Active_State_Request_L1, disables DLLP and TLP transmission, sends the EIOS and places its transmit lanes into Electrical Idle. 

**Upstream Component Receives Electrical Idle.** When the Upstream component receives the EIOS, it stops sending the PM_Request_Ack DLLP, 

**749** 

**PCI Ex ress Technolo p gy** 

disables DLLP and TLP transmission, sends EIOS and places its own trans‐ mit lanes into Electrical Idle. 

_Figure 16‐17: Negotiation Sequence Required to Enter L1 Active State PM_ 

**==> picture [371 x 344] intentionally omitted <==**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-2"></a>
## 16.2 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-3"></a>
## 16.3 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

If system firmware or software determines that both components on the Link use the platform clock then the reference clocks within both devices will be in phase. This results in shorter exit latencies from L0s and L1, and is reported in the _Common Clock_ field of the Link Control register. Components must then update their reported exit latencies to reflect the correct value. Note that if the clocks are not common then the default values will be correct and no further action is required. 

**L0s Exit Latency Update.** Exit latency for L0s is reported in the Link Capability register based on the default assumption that a common clock implementation does not exist. L0s exit latency is also reported in the TS1s 

**756** 

**Chapter 16: Power Management** 

used during Link training as the number of FTS Ordered Sets (N_FTS) required to exit L0s. If software then detects a common clock implementa‐ tion, it sets the Common Clock field writes to the _Retrain Link_ bit in the Link Control register to force Link training to repeat. During retraining new N_FTS values are reported and in the _L0s Latency_ field of the Link Capabil‐ ity register. 

**L1 Exit Latency Update.** Following Link retraining, new values will also be reported in the _L1 Latency_ field. 

_Figure 16‐21: Config. Registers for ASPM Exit Latency Management and Reporting_ 

**757** 

**PCI Ex ress Technolo p gy** 

## **Calculating Latency from Endpoint to Root Complex** 

Figure 16‐22 on page 759 illustrates an Endpoint whose transactions must trans‐ verse two switches to reach the Root Complex. Presuming that all Links in the path are in the L1 state, let’s take the example that Endpoint B needs to send a packet to main memory. 

1. First, it begins the wake sequence by initiating a TS1 ordered set on its Link at time “T.” The L1 exit latency for EP B is a maximum of 8μs, but Switch C has a maximum exit latency of 16μs. Therefore, the exit latency for this Link is 16μs. 

2. Within 1μs of detecting the L1 exit on Link B/C, Switch C signals L1 exit on Link C/F at T+1μs. 

3. Link C/F completes its exit from L1 in 16μs, at T+17μs. 

4. Switch F signals an exit from L1 to the Root Complex within 1μs of detect‐ ing L1 exit from Switch C (T+2μs). 

5. Link F/RC completes exit from L1 in 8μs, completing at T+10μs. 

6. Total latency to transition path to target back to L0 = T+17μs. 

**758** 

**Chapter 16: Power Management** 

_Figure 16‐22: Example of Total L1 Latency_ 

**==> picture [345 x 423] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>RC L1 latency (8μs)<br>5. Exit to L0 also takes 8μs L1 State<br>PM State D0 4. Within 1μs of detected L1 exit<br>    from Switch C, Switch F signals<br>Switch     L1 Exit to RC<br>(F)<br>Switch F, L1 latency (8μs)<br>3. Exit to L0 takes 16μs L1 State<br>L1 State<br>2. Within 1μs of detecting,<br>PM State D0 PM State         L1 Exit from EP B, Switch<br>PCIe D0        C signals Exit to Switch FPCI-XP<br>Endpoint Switch Endpoint PM State D1<br>(D) (E)<br>(C)<br>Switch C, L1 latency (16μs)<br>1. Exit to L0 takes 16μs<br>L1 State L1 State            because the switch takes<br>          longer than the endpoint<br>PM State D2 PM State D0<br>PCIe PCIe<br>EP B, L1 latency (8μs)<br>Endpoint Endpoint<br>(A) (B)<br>T T+16<br>Link B/C starts L1 exit at T and takes 16μs T+17<br>T+1<br>Link C/F starts L1 exit at T+1 and takes 16μs<br>T+2 T+10<br>Link F/RC starts L1 exit at T+1 and takes 8μs<br>**----- End of picture text -----**<br>


**759** 

**PCI Ex ress Technolo p gy** 

## **Software Initiated Link Power Management** 

When software initiates configuration writes to change the power state for power conservation, devices must respond by transitioning their Link to the corresponding low power state. 

## **D1/D2/D3 and the L1 State Hot** 

The spec requires that when all Functions within a device have been placed into any of the low power states (D1, D2, or D3hot), the device must initiate a transi‐ tion to the L1 state as shown in Figure 16‐23. A device returns to L0 as a result of software initiating a configuration access to the device or a device initiated event. 

_Figure 16‐23: Devices Transition to L1 When Software Changes their Power Level from D0_ 

**==> picture [320 x 116] intentionally omitted <==**

**----- Start of picture text -----**<br>
L0<br>L2/L3<br>L0s L1 L2 L3<br>Ready<br>**----- End of picture text -----**<br>


Upon receiving a configuration write to the _Power State_ field of the PMCSR reg‐ ister, a device initiates the change from L0 to L1 by sending a PM_Enter_L1 DLLP to the upstream component. 

## **Entering the L1 State** 

The procedure to place the Link into an L1 state is illustrated in Figure 16‐24 on page 762. The steps in the figure are described in greater detail in the following list: 

1. Once a device recognizes that all its Functions are in the D2 state, it must prepare to transition the Link into L1. This begins with blocking new TLPs from being scheduled. 

**760** 

**Chapter 16: Power Management** 

2. A TLP may from the downstream Endpoint may not have been acknowl‐ edged prior to receiving the request to enter D2. The device must not respond to a request to change the Link power until all outstanding TLPs have been acknowledged. In other words, the Replay Buffer must be empty before proceeding to the L1 state. 

3. Because of the long latencies involved in returning the Link to its active state, a device must be able to send a maximum‐sized TLP immediately upon return to the active state. Since a lack of Flow Control credits could block this, the Endpoint must have sufficient credits to permit transmission of the biggest packet supported for each Flow Control type before entering L1. 

4. When the requirements listed above have been met, the Endpoint sends a PM_Enter_L1 DLLP to the upstream device. This instructs the upstream component to put the Link into L1. The PM_Enter_L1 is repeated until a PM_Request_ACK DLLP is received from the upstream device. 

5. When the upstream component receives PM_Enter_L1, it begins its prepa‐ ration by performing steps 6, 7, and 8. This is the same preparation as per‐ formed by the downstream component prior to signaling the L1 transition. 

6. All new TLP scheduling is blocked. 

7. In the event that a previous TLP has not yet been acknowledged, the upstream device will wait until all transactions in the Replay Buffer have been acknowledged. 

8. Sufficient Flow Control credits must be accumulated to ensure that the larg‐ est TLP can be transmitted for each Flow Control type. 

9. The upstream component sends a PM_Request_ACK DLLP to confirm that it’s ready to enter the L1 state. This DLLP is repeated until an Electrical Idle ordered set is received, indicating that it’s been accepted. 

10. When the downstream component receives the acknowledgement, it sends an EIOS and places its transmit lanes into electrical idle (transmitter is in Hi‐Z state). 

11. The upstream component recognizes the EIOS and places its transmit lanes into electrical idle. The Link has now entered the L1 state. 

**761** 

**PCI Ex ress Technolo p gy** 

_Figure 16‐24: Procedure Used to Transition a Link from the L0 to L1 State_ 

**==> picture [342 x 323] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Function<br>6. Device blocks new TLP<br>PCIe-Core scheduling<br>Hardware/Software<br>Interface<br>7. ACK received for last TLP<br>Transaction Layer (Retry Buffer empty)<br>5. PM_Enter_ L1 DLLP is 8. All FC credits sufficient to send a<br>received Data Link Layer maximum-sized transaction<br>9. PM_Request_ACK sent<br>12. Electrical Idle ordered set received continuously until electrical<br>Causing TLP and DLLP transmission Physical Layer idle ordered set is received<br>to be disabled<br>(RX) (TX)<br>11. Electrical Idle ordered set<br>is sent and transmitter goes (Link) 13. Transmit lanes are placed into<br>to Electrical idle Electrical idle<br>(TX) (RX)<br>4. PM_Enter_L1 DLLP is sent Physical Layer<br>continuously until PM_Request_ACK<br>is received from the opposite port<br>3. All FC credits sufficient to send  Data Link Layer 10. PM_Request_ACK received,causing TLP and DLLP Packet<br>a maximum-sized transaction<br>transmission to be disabled<br>2. ACK received for last TLP Transaction Layer<br>(Retry Buffer empty)<br>PCIe-Core<br>Hardware/Software<br>1. Device blocks new TLP scheduling Interface<br>Device Core<br>Downstream Component<br>**----- End of picture text -----**<br>


## **Exiting the L1 State** 

An exit from the L1 state can be initiated by either the upstream or downstream component, as discussed below. This section also summarizes the signaling pro‐ tocol used to exit L1. 

**Upstream Component Initiates.** Software may need to use a device which is currently in a low‐power state, and that means the Power Manage‐ ment software must issue a configuration write to change its power state back to D0. When the configuration Request is ready to be sent from the upstream component (a Root Port or downstream Switch Port) the port will exit the electrical idle state and initiate re‐training to return the Link to the 

**762** 

**Chapter 16: Power Management** 

L0 state. Once the Link is active, the configuration write can be delivered to the device to transition it back to D0, at which point it’s ready for normal use. 

**Downstream Component Initiates L1 to L0 Transition.** In the L1 state the reference clock and power are still applied to devices on the Link. That allows a downstream device to be designed to monitor external events and trigger a Power Management Event (PME) when it occurs. In conven‐ tional PCI, this is reported by a side‐band PME# signal, and system board logic usually uses it to generate an interrupt that informs the CPU of the need to bring the device back to full operation. PCIe eliminates the side‐ band signal and instead sends an in‐band message to report the PME (see “The PME Message” on page 769 for details). 

**The L1 Exit Protocol.** In the L1 state both directions of the Link are in the electrical idle state. A device signals an exit from L1 by changing from elec‐ trical idle and sending TS1s. When the Link neighbor detects the exit from electrical idle it sends TS1s back. This sequence triggers both devices to enter the Recovery state and, when that has completed its operation, both devices will have returned to the L0 state. 

## **L2/L3 Ready — Removing Power from the Link** 

Once software has placed all Functions within a Device into the D3hot state power can be safely removed from the device. A typical application for this would be to place all devices in the system into D3 and then remove power from them all to achieve the lowest power consumption. However, the spec does not give details of the actual mechanism that would be used to remove clock and power or require that a particular sequence be followed, allowing for a variety of implementations. 

The state transitions to prepare devices for power removal involve the prelimi‐ nary steps of entering L1 and then returning to L0 before arriving at the L2/L3 Ready state as illustrated in Figure 16‐25 on page 764. 

**763** 

**PCI Ex ress Technolo p gy** 

_Figure 16‐25: Link States Transitions Associated with Preparing Devices for Removal of the Reference Clock and Power_ 

## **L2/L3 Ready Handshake Sequence** 

The spec does require a handshake sequence when transitioning to the L2/L3 Ready state. This ensures that all devices are ready for reference clock and power removal, and also that inband PME messages being sent to the Root Complex won’t accidentally be lost when power is removed.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-4"></a>
## 16.4 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-5"></a>
## 16.5 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

3. The corresponding split completion must push all previously posted PME messages ahead of it based on transaction ordering rules. 

4. The Root Complex cannot accept a new PME message because the queue is full, so the path is temporarily blocked. But that also means that the read completion can’t reach the Root Complex to clear the older entry in the queue. 

5. No progress can be made and deadlock occurs. 

## **The Solution** 

The problem is avoided if the Root Complex always accepts new PME mes‐ sages, even when they would overflow the queue. In this case, the Root simply discards the later PME messages. To prevent a discarded PME message from being lost permanently, a device that sends a PME message is required to mea‐ sure a time‐out interval, called the PME Service Time‐out. If the device’s PME_Status bit is not cleared with 100 ms (+ 50%/‐ 5%), it assumes its message must have been lost and it re‐issues the message. 

## **The PME Context** 

Devices that generate PME must continue to power portions of the device that are used for detecting, signaling, and handling PME events, referred to collec‐ tively as the PME context. Devices that support PME in the D3cold state use aux‐ iliary power to maintain the PME context when the main power is removed. Items that are typically part of the PME context include: 

- PME_Status bit (required) — set when a device sends a PME message and cleared by PM software. Devices that support PME in the D3cold state must implement the PME_Status bit as “sticky,” meaning that the value survives a fundamental reset. 

**771** 

## **PCI Ex ress Technolo p gy** 

- PME_Enable bit (required) — this bit must remain set to continue enabling a Function’s ability to generate PME messages and signal wakeup. Devices that support PME in the D3cold state must implement PME_Enable as “sticky,” meaning that the value survives a fundamental reset. 

- Device‐specific status information — for example, a device might preserve event status information in cases where several different types of events can trigger a PME. 

- Application‐specific information — for example, modems that initiate wakeup would preserve Caller ID information if supported. 

## **Waking Non-Communicating Links** 

When a device that supports PME in the D3cold state needs to send a PME mes‐ sage, it must first transition the Link to L0. This is sometimes referred to as a wakeup. PCI Express defines two methods of triggering the wakeup of non‐communicating Links: 

- Beacon — an in‐band indicator driven by AUX power 

- • WAKE# Signal — a sideband signal driven by AUX power 

In both cases, PM software must be notified to restore main power and the ref‐ erence clock. This also causes a fundamental reset that forces a device into the D0uninitialized state. Once the Link transitions to L0, the device sends the PME message. Since a reset is required to re‐activate the Link, devices must maintain PME context across the reset sequence described above. 

## **Beacon** 

This signaling mechanism is designed to operate on AUX power and doesn’t require much power. The beacon is simply a way of notifying the upstream component that software should be notified of the wakeup request. When switches receive a beacon on a downstream port, they in turn signal beacon on their upstream port. Ultimately, the beacon reaches the root complex, where it generates an interrupt that calls PM software. 

Some form‐factors require beacon support for waking the system while others don’t. The spec requires compliance with the form‐factor specs, and doesn’t require beacon support for devices if their form‐factor doesn’t. However, for “universal” components designed for use in a variety of form‐factors, beacon support is required. See “Beacon Signaling” on page 483 for details. 

**772** 

**Chapter 16: Power Management** 

## **WAKE#** 

PCI Express provides a sideband signal called WAKE# as a alternative to the beacon that can be routed directly to the Root or to other system logic to notify PM software. In spite of the desire to minimize the pin count of a Link, the moti‐ vation for adding this extra pin is easy to understand. The reason is that a com‐ ponent must consume auxiliary power to be able to recognize a beacon on a downstream port and then forward it to an upstream port. In a battery‐powered system auxiliary power is jealously guarded because it drains the battery even when the system isn’t doing any work. The preferred solution in that case would be to bypass as many components as possible when delivering the wakeup notification, and the WAKE# pin serves that purpose very well. On the other hand, if power is not a concern then the WAKE# pin might be considered less desirable. 

A hybrid implementation may also be used. In this case, WAKE# is sent to a switch, which in turn sends the beacon on its upstream port. The options are illustrated in Figure 16‐29 on page 774 A and B. Note that when asserted, the WAKE# signal remains low until the PME_Status bit is cleared by software. 

This signal must be implemented by ATX or ATX‐based connectors and cards as well as by the mini‐card form factor. No requirement is specified for embedded devices to use the WAKE# signal. 

**773** 

## **PCI Ex ress Technolo p gy** 

_Figure 16‐29: WAKE# Signal Implementations_ 

**==> picture [317 x 472] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>L2 State<br>(F) PM State D3<br>Switch<br>L2 State L2 State<br>PM State<br>PM State D3 PCIe D3 PCIe PM State D3<br>Endpoint (C) Endpoint<br>(D) Switch (E)<br>L2 State L2 State WAKE#<br>A Card Slots<br>Root Complex<br>L2 State<br>(F)<br>Switch PM State D3<br>Beacon signaling used from L2 State<br>switch to Root Complex.<br>PM State D3 PCIe PM StateD3 PCIe PM State D3<br>Endpoint Endpoint<br>(C)<br>(D) Switch (E)<br>L2 State WAKE#<br>B Card Slots<br>**----- End of picture text -----**<br>


**774** 

**Chapter 16: Power Management** 

## **Auxiliary Power** 

Devices that support PME in the D3cold state must support the wakeup sequence and are allowed by the PCI‐PM spec to consume the maximum auxil‐ iary current of 375 mA (otherwise only 20mA). The amount of current they need is reported in the _Aux_Current_ field of the PM Capability registers. Auxiliary power is enabled when the _PME_Enable_ bit is set within the PMCSR register. 

PCI Express extends the use of auxiliary power beyond the limitations given by PCI‐PM. Now, any Device may consume the maximum auxiliary current if enabled by setting the _Aux Power PM Enable_ bit of the Device Control register, illustrated in Figure 16‐30 on page 775. This gives devices the opportunity to support other things like SM Bus while in a low power state. As in PCI‐PM the amount of current consumed by a device is reported in the _Aux_Current_ field in the PMC register. 

_Figure 16‐30: Auxiliary Current Enable for Devices Not Supporting PMEs_ 

|||15|14|12|11|10|9|8|7|5|4|3|2|1|0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||
|Bridge Config. Retry Enable/||||||||||||||||
|Initiate Function-Level Reset||||||||||||||||
|Max Read Request Size||||||||||||||||
||Enable No Snoop|||||||||||||||
||Aux Power PM Enable|||||||||||||||
|Phantom Functions Enable||||||||||||||||
|Extended Tag Field Enable||||||||||||||||
||Max Payload Size|||||||||||||||
|Enable Relaxed Ordering||||||||||||||||
||Unsupported Request|||||||||||||||
||Reporting Enable|||||||||||||||
|Fatal|Error Reporting Enable|||||||||||||||
||Non-Fatal Error|||||||||||||||
||Reporting Enable|||||||||||||||
||Correctable Error|||||||||||||||
||Reporting Enable|||||||||||||||



**775** 

**PCI Ex ress Technolo p gy** 

## **Improving PM Efficiency** 

## **Background** 

As processors and other system components acquire better power management mechanisms, peripherals like PCIe components start to appear as a bigger con‐ tributor to power consumption in PC systems. Earlier generations of PCIe allowed some software and hardware power management, but coordinating PM decisions with the system was not a high priority and consequently soft‐ ware visibility and control was limited. 

One problem that can arise from this lack of coordination happens when the system goes into a sleep state but the devices remain operational. Such devices can initiate interrupts or DMA traffic that would require the system to wake up to handle them, even thought they were low‐priority events, and thus defeat the goal of power conservation. 

It can also happen that the system is unaware of how long the devices can afford to wait from the time they request system service (like a memory read) until they get a response. Without that information, software is often forced to assume that the response time must always be minimal and therefore power management policies can’t afford enough time to do much. However, if the sys‐ tem was aware of time windows when a fast response was not needed, it could be more aggressive with power management and stay in a low power state for a longer time without risking performance problems. The 2.1 spec revision added two new features to address these problems. 

## **OBFF (Optimized Buffer Flush and Fill)** 

The first of these mechanisms is Optimized Buffer Flush and Fill, which pro‐ vides a mechanism for Endpoints to be made aware of the system power state and therefore the best times to do data transfers to and from the system. 

## **The Problem** 

The problem with bus‐master capable devices is that if they’re not aware of the system power status, they may initiate transactions at times when it would be better to wait. The diagram in Figure 16‐31 on page 777 illustrates the problem in simple terms: there are many components initiating events and as a result, 

**776** 

**Chapter 16: Power Management** 

the times without activity when the system is idle and can go to sleep are few and short‐lived. In contrast, Figure 16‐32 on page 777 illustrates an improve‐ ment in which the same events are grouped and serviced together so that the times when the system is idle enough to go to sleep are both more frequent and of longer duration. Clearly, this would result in better power conservation and fortunately, it’s not difficult to implement. PCIe components simply need to understand what they should do based on the system power state, and they’ll need a way to learn what that state currently is. 

_Figure 16‐31: Poor System Idle Time_ 

**==> picture [310 x 135] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Idle System Idle<br>Window Window<br>System Events<br>Endpoint A<br>Events<br>Endpoint B<br>Events<br>Endpoint C<br>Events<br>Time<br>**----- End of picture text -----**<br>


_Figure 16‐32: Improved System Idle Time_ 

**==> picture [327 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Idle System Idle System Idle<br>Window Window Window<br>System Events<br>Endpoint A<br>Events<br>Endpoint B<br>Events<br>Endpoint C<br>Events<br>Time<br>LTR could also be used to inform system software of acceptable latency for<br>the endpoints between accesses, suggesting a limit on this idle time.<br>**----- End of picture text -----**<br>


**777** 

**PCI Ex ress Technolo p gy** 

## **The Solution**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-6"></a>
## 16.6 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

OBFF is an optional hint that a system can use to inform components about optimal time windows for traffic. It’s just a hint, though, so bus‐master‐capable devices can still initiate traffic whenever they like. Of course, power consump‐ tion will be negatively affected if they do, so overriding the OBFF hints should be avoided as much as possible. The information is communicated in one of two ways: by sending messages to the Endpoints or by toggling the WAKE# pin. If both options are available, using the pin is strongly recommended because it avoids the counter‐productive step of using excess power, possibly across sev‐ eral Links, to inform a component about the current system power state. In fact, the OBFF message should only be used if the WAKE# pin is not available. 

Figure 16‐33 on page 778 gives an example showing a mix of both communica‐ tion types. Using the pin is required if it’s available, but in this example it’s not an option between the two switches. To work around this problem, the upper switch can translate the state received on the WAKE# pin into a message going downstream. It should perhaps be noted here that switches are strongly encour‐ aged to forward all OBFF indications downstream but not required to do so. It may be necessary, especially when using messages, to discard or collapse some indications and that is permitted. 

_Figure 16‐33: OBFF Signaling Example_ 

**==> picture [207 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>WAKE#<br>Endpoint<br>Switch<br>Endpoint<br>OBFF<br>Message<br>Endpoint<br>WAKE# Switch<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


**778** 

**Chapter 16: Power Management** 

**Using the WAKE# Pin.** This pin, previously only used to inform the sys‐ tem that a component needed to have power restored, is given an extra meaning as the simplest and lowest‐power option for communicating sys‐ tem power status to PCIe components. It’s optional, and the protocol is fairly simple: the WAKE# pin toggles to communicate the system state. As seen in Figure 16‐34 on page 779, there are several transitions but only three states, which are described below: 

1. CPU Active ‐ system awake; all transactions OK. This is every compo‐ nent’s initial state. 

2. OBFF ‐ system memory path available; transfers to and from memory are OK, but other transactions should wait for a higher power state. 

3. Idle ‐ wait for a higher state before initiating. 

_Figure 16‐34: WAKE# Pin OBFF Signaling_ 

**==> picture [382 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transition Event OBFF Message Code<br>Idle OBFF OBFF<br>Idle CPU Active CPU Active<br>OBFF or CPU Active Idle Idle<br>OBFF CPU Active CPU Active<br>CPU Active               OBFF OBFF<br>**----- End of picture text -----**<br>


When the CPU Active or OBFF state is indicated, it’s recommended that the platform not return to the Idle state for at least 10  s so as to give compo‐ nents enough time to deliver the packets they may have been queuing up while in the previous Idle state. However, since that timing isn’t required, it’s also recommended that Endpoints not assume they’ll have a certain amount of time in a CPU Active or OBFF window. Along the same lines, the platform is allowed to indicate that it’s going to Idle before it actually does 

**779** 

## **PCI Ex ress Technolo p gy** 

so as to give components advance notice that it’s time to finish. The case this early notice is specifically designed to avoid is having an Endpoint start a transfer just as the platform goes to Idle, causing an immediate exit from the Idle state. The spec strongly recommends that this should be the only reason for an early indication of the Idle state and also that this advance notice time should be as short as possible. 

Interestingly, the WAKE# pin can still be used for its original purpose of allowing a component to wake the system, and it’s no surprise that this might confuse other components that are monitoring that pin for OBFF information. That could result in sub‐optimal behavior in power or perfor‐ mance, but this is considered a recoverable situation so no steps were taken to guard against it. To cover all of these cases, any time the signal is unclear the default state will be CPU Active. 

**Using the OBFF Message.** As mentioned earlier, OBFF information can be communicated using a message, although it’s recommend that this only be used if the WAKE# pin is not available. These messages only flow down‐ stream from the Root. The message contents are shown in Figure 16‐35 on page 781, including the Routing type 100b (point‐to‐point) and an OBFF Code that gives the following values (all other codes are reserved): 

1. 1111b ‐ CPU Active 

2. 0001b ‐ OBFF 

3. 0000b ‐ Idle 

If a reserved code is received, components must treat it as “CPU Active.” If a Port receives an OBFF message but doesn’t support OBFF or hasn’t enabled it yet, it must treat it as an Unsupported Request (Completion sta‐ tus UR). 

**780** 

**Chapter 16: Power Management** 

_Figure 16‐35: OBFF Message Contents_ 

**==> picture [359 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 1 1 0  1 0 0 tr H D P<br>Message Code<br>Byte 4 Requester ID Tag 0001 0010<br>Byte 8 Reserved for Error Messages<br>OBFF<br>Byte 12 Reserved for Error Messages Code<br>Point-to-Point 0000b = Idle<br>0001b = OBFF<br>1111b  =  CPU Active<br>**----- End of picture text -----**<br>


Support for OBFF is indicated via the Device Capability 2 register (Figure 16‐36 on page 782), and enabled using the Device Control 2 register (Figure 16‐37 on page 783). Note that both the pin and message options may be available. However, the pin method is preferred because it is the lower power option. 

Note that there are two variations for enabling a component to forward OBFF messages, and the difference between them has to do with handling a targeted Link that’s not in L0. In Variation A, the message will only be sent if the Link is in L0. If it’s not, the message is simply dropped to avoid the cost of waking the Link. This is preferred for Downstream Ports when the Device below it is not expected to have time‐critical communication requirements and can indicate its need for non‐urgent attention by simply returning the Link to L0. For Variation B, the message will always be for‐ warded and the Link will be returned to L0. This variation is preferred when the downstream Device can benefit from timely notification of the platform state. 

**781** 

## _Figure 16‐36: OBFF Support Indication_ 

**==> picture [364 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capability 2 Register<br>31 24  23  22  21  20  19 18 14  13   12  11  10  9  8   7  6  5  4  3        0<br>[eee] o vem<br>RsvdP RsvdP<br>[eee] “ TET<br>Za<br>See om [os] ||<br>eee] os Max End-End<br>TLP Prefixes<br>om<br>ede End-End TLP<br>ow Prefix Supported<br>owno Extended Fmt<br>ow Field Supported<br>ow<br>TPH Completer Supported<br>[see omJo LTR Mechanism Supported<br>No RO-enabled PR-PR Passing<br>128-bit CAS Completer Supported<br>OBFF Support<br>64-bit AtomicOp Completer Supported<br>00 – Not supported 32-bit AtomicOp Completer Supported<br>AtomicOp Routing Supported<br>01 – Message only<br>ARI Forwarding Supported<br>10 – WAKE# only<br>Completion Timeout Disable Supported<br>11 – Both Completion Timeout Ranges Supported<br>**----- End of picture text -----**<br>


When using WAKE#, enabling any Root Port to assert it is considered a glo‐ bal enable unless there are multiple WAKE# signals, in which case only those associated with that Port are affected. When using the OBFF message, enabling a Root Port only enables the messages on that Port. The expecta‐ tion in the spec is that all Root Ports would normally be enabled if any of them are, so as to ensure that the whole platform was enabled. However, selectively enabling some Ports and not others is permitted. 

When enabling Ports for OBFF, the spec recommends that all Upstream Ports be enabled before Downstream Ports, and Root Ports be enabled last of all. For unpopulated hot plug slots this isn’t possible. For that case enabling OBFF using the WAKE# pin to the slot is permitted, but it’s recom‐ mended that the Downstream Port above the slot not be enabled to deliver OBFF messages. 

**Chapter 16: Power Management** 

## _Figure 16‐37: OBFF Enable Register_ 

**==> picture [236 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Control 2 Register<br>15  14  13 11  10  9  8   7  6  5  4  3        0<br>RsvdP<br>End-End TLP Prefix Blocking<br>LTR Mechanism Enable<br>IDO Completion Enable<br>IDO Request Enable<br>AtomicOp Egress Blocking<br>AtomicOp Requester Enable<br>ARI Forwarding Enable<br>Completion Timeout Disable<br>Completion Timeout Value<br>OBFF Enable<br>00 – Disabled<br>01 – Enabled with Message signaling Variation A<br>10 – Enabled with Message signaling Variation B<br>11 – Enabled using WAKE# signaling<br>**----- End of picture text -----**<br>


Finally, let’s refer back to the earlier example in Figure 16‐33 on page 778 to consider what these registers might look like for that case. The Downstream Port of the switch that connects to the lower switch will have a value for OBFF Support of 01b ‐ Message Only, while its Upstream Port might have a value of 11b ‐ Both. These values might be hard coded into the device or hardware initialized in some other fashion to make them visible to software after a reset. The Downstream Port would need to have an OBFF Enable value of 01b or 10b ‐ Enabled with Message variation A or B so it could deliver an OBFF message. The Upstream Port would expect to have an OBFF Enable value of 11b ‐ Enabled with WAKE# signaling. The spec points out that when a switch is configured to use the different methods when going from one Port to another, it’s required to make the translation and for‐ ward the indications. 

**783** 

**PCI Ex ress Technolo p gy** 

## **LTR (Latency Tolerance Reporting)** 

The second new feature added to improve PM efficiency is called Latency Toler‐ ance Reporting (LTR). This optional capability allows devices to report the delay they can tolerate when requesting service from the platform so that PM policies for platform resources like main memory can take that into consider‐ ation. If software supports it, this provides good performance for devices when they need it and lower power for the system when they don’t need a fast response. One simple way of using this information would be to allow the sys‐ tem to postpone waking up to service a request as long as the latency tolerance was still met. 

The meaning of “latency tolerance” is not made explicitly clear in the spec, but some things are mentioned that might play into it. For example, the latency tol‐ erance may affect acceptable performance or it may impact whether the compo‐ nent will function properly at all. Clearly, such a distinction would make a big difference in designing a PM policy. Similarly, the device may use buffering or other techniques to compensate for latency sensitivity and knowledge of that would be useful for software. 

## **LTR Registers**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-7"></a>
## 16.7 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The LTR capability in a device is discovered using a new bit in the PCIe Device Capability 2 Register, as shown in Figure 16‐38 on page 785, and enabled in the Device Control 2 Register, illustrated in Figure 16‐39 on page 785. The spec pre‐ scribes a sequence for enabling LTR, too: devices closest to the Root must be enabled first, working down to the Endpoints. An Endpoint must not be enabled unless its associated Root Port and all intermediate switches also sup‐ port LTR and have been enabled to service it. It’s permissible for some End‐ points to support LTR while others do not. If a Root Port or switch Downstream Port receives an LTR message but doesn’t support it or hasn’t been enabled yet, the message must be treated as an Unsupported Request. It’s recommended that Endpoints send an LTR message shortly after being enabled to do so. It’s strongly recommended that Endpoints not send more than two LTR messages within any 500  s period unless required by the spec. However, if they do, Downstream Ports must properly handle them and not generate an error based on that. 

**784** 

**Chapter 16: Power Management** 

## _Figure 16‐38: LTR Capability Status_ 

**==> picture [235 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capability 2 Register<br>31 24  23  22  21  20  19  18 14  13   12  11  10  9  8   7  6  5  4  3        0<br>RsvdP RsvdP<br>Max End-End<br>TLP Prefixes<br>End-End TLP<br>Prefix Supported<br>Extended Fmt<br>Field Supported<br>TPH Completer Supported<br>LTR Mechanism Supported<br>O<br>**----- End of picture text -----**<br>


_Figure 16‐39: LTR Enable_ 

**==> picture [218 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Control 2 Register<br>15  14  13         11  10  9  8   7  6  5  4  3        0<br>RsvdP<br>End-End TLP Prefix Blocking<br>LTR Mechanism Enable<br>IDO Completion Enable<br>IDO Request Enable<br>AtomicOp Egress Blocking<br>AtomicOp Requester Enable<br>ARI Forwarding Enable<br>Completion Timeout Disable<br>Completion Timeout Value<br>**----- End of picture text -----**<br>


The target for LTR information is the Root Complex. Participating downstream devices all report their values but the Port just uses the smallest value that was reported as the latency limit for all devices accessed through that Port. The Root is not required to honor requested service latencies but is strongly encouraged to do so. 

**785** 

**PCI Ex ress Technolo p gy** 

## **LTR Messages** 

The LTR message itself has the format shown in Figure 16‐40 on page 788, where it can be seen that the Routing type 100b (point‐to‐point) and the LTR message code is 0001 0000b. Two latency values are reported, one for Requests that must be snooped and another for Requests that will not be snooped and therefore should complete more quickly. As seen in the diagram, the format for both is the same and includes the following fields: 

- Latency Value and Scale ‐ combine to give a value in the range from 1ns to about 34 seconds. Setting these fields to all zeros indicates that any delay will affect the device and thus the best possible service is requested. The meaning of the latency is defined as follows: 

   - For Read Requests, it’s the delay from sending the END symbol in the Request TLP until receiving the STP symbol in the first Completion TLP for that Request. 

   - For Write Requests, it relates to Flow Control back‐pressure. If a write has been issued but the next write can’t proceed due to a lack of Flow Control credits, the latency is the time from the last symbol of that write (END) until the first symbol of the DLLP that gives more credits (SDP). In other words, this represents the time within which the Root Port should be able to accept the next write. 

- Requirement ‐ can be set for none, or one, or both to indicate whether that latency value is required. If a device doesn’t implement one of these traffic types or has no service requirements for it, then this bit must be cleared for the associated field. If a device has reported requirements but has since been directed into a device power state lower than D0, or if its LTR Enable bit has been cleared, the device must send another LTR message reporting that these latencies are no longer required. 

## **Guidelines Regarding LTR Use** 

Endpoints have a few guidelines regarding the use of LTR: 

1. It’s recommended that they send an updated LTR message every time their service requirements change, and the spec spends some time going over examples of this. The bottom line here is that devices need to take all the delays into account when making a change to the service requirements. That accounting includes time for the reference clock to be restored if was turned off, for the Link to be brought back to L0, for the LTR message to be delivered, and for the platform to prepare to handle the new requirement. 

2. If the latency tolerance is being reduced, it’s recommended that the LTR message be sent far enough ahead of the first associated Request to ensure that the platform is ready. 

**786** 

**Chapter 16: Power Management** 

3. If the latency tolerance is being increased, then the LTR message to report that should immediately follow the final Request that used the previous latency value. 

4. To achieve the best overall platform power efficiency, it’s recommended that Endpoints buffer Requests as much as they can and then send them in bursts that are as long as the Endpoint can support. 

Multi‐Function Devices (MFDs) have a few rules of their own. For example, they must send a “conglomerated” LTR message as follows: 

1. Reported latency values must reflect the lowest values associated with any Function. The snoop and no‐snoop latencies could be associated with differ‐ ent Functions, but if none of them have a requirement for snoop or no‐snoop traffic, then the requirement bit for that type must not be set. 

2. MFDs must send a new LTR message upstream if any of the Functions changes its values in a way that affects the conglomerated value. 

Switches have a similar set of rules related to LTR. Basically, they collect the messages from Downstream Ports that have been enabled to use LTR and send a “conglomerated” message upstream according to the following rules: 

1. If the Switch supports LTR, it must support it on all of its Ports. 

2. The Upstream Port is allowed to send LTR messages only when the LTR Enable bit is set or shortly after software has cleared it so it can report that any previous requirements are no longer in effect. 

3. The conglomerated LTR value is based on the lowest value reported by any participating Downstream Port. If the Requirement bit is clear, or an invalid value is reported, the latency is considered effectively infinite. 

4. If any Downstream Port reports that an LTR value is required, the Require‐ ment bit will be set for that type in the LTR message forwarded upstream. 

5. The LTR values reported upstream must take into account the latency of the Switch itself. If the Switch latency changes based on its operational mode, it must not be allowed to exceed 20% of the minimum value reported on all Downstream Ports. The value reported on the Upstream Port is the mini‐ mum reported value on all the Downstream Ports minus the Switch’s own latency, although the value can’t be less than zero. 

6. If a Downstream Port goes to DL_Down status, previous latencies for that Port must be treated as invalid. If that changes the conglomerated values upstream then a new message must be sent to report that. 

7. If a Downstream Port’s LTR Enable bit is cleared, any latencies associated with that Port must be considered invalid, which may also result in a new LTR message being sent upstream. 

8. If any Downstream Ports receive new LTR values that would change the conglomerated value, the Switch must send a new LTR message upstream to report that. 

**787** 

**PCI Ex ress Technolo p gy** 

Finally, the Root Complex also has a few rules related to LTR: 

1. The RC is allowed to delay processing of a device Request as long as it satis‐ fies the service requirements. One application of this might be to buffer up several Requests from an Endpoint and service them all in a batch. 

2. If the latency requirements are updated while a series of Requests is in progress, the new values must be comprehended by the RC prior to servic‐ ing the next Request, and within less time than the previously reported latency requirements. 

_Figure 16‐40: LTR Message Format_ 

**==> picture [350 x 264] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1<br>Byte 0 Fmt Type R TC Rsv T E Attr AT Length (Reserved)<br>0 0 1 1 0  1 0 0 0 0 0 D P 0 0 0 0<br>Message Code<br>Byte 4 Requester ID Tag 0001 0000<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>Point-to-Point<br>15 14 13 12 10 9 0<br>Rsv [Latency] Latency Value<br>Scale<br>Requirement<br>Scale:<br>000 - x 1ns   001 - x 32 ns<br>010 - x 1K ns   011 - x 32K ns<br>100 - x 1M ns  101 - x 32M ns<br>110 - x not permitted<br>**----- End of picture text -----**<br>


**788** 

**Chapter 16: Power Management** 

## **LTR Example** 

To illustrate the concepts discussed so far, consider the example topology shown in Figure 16‐41 on page 789. Here, the Endpoint on the lower left has delivered an LTR message to the Switch reporting a Snoop Latency requirement of 1200ns. At this point, none of the other Endpoints connected to the Switch has reported an LTR value, so that becomes the conglomerated value to be reported upstream. However, the Switch has an internal latency of 50ns so that must be subtracted from the value to be reported, resulting in the Upstream Port sending an LTR message reporting 1150ns to the Root Port. 

_Figure 16‐41: LTR Example_ 

**==> picture [122 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>value<br>Conglomerate  i<br>value 1200 ns —<br>& _<br>1200 ns<br>[| Va i<br>**----- End of picture text -----**<br>


Next, the Legacy Endpoint delivers an LTR message with a large latency requirement of 5000ns, as shown in Figure 16‐42 on page 790. Since this is larger than the current conglomerate value for the Switch, no LTR message is sent for this case. 

**789** 

**PCI Ex ress Technolo p gy** 

_Figure 16‐42: LTR ‐ Change but no Update_ 

**==> picture [176 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>value<br>—<br>Conglomerate  1200 ns<br>value<br>Switch EndpointPCle<br>e ¢<br>Vl i IN 5000 ns<br>**----- End of picture text -----**<br>


In the next stage, the middle Endpoint reports its LTR value as 700ns. This is smaller than the current conglomerate value, so the Switch calculates the new value of 650ns by subtracting its internal latency and forwards that upstream as an LTR message. That makes the current latency requirement for that Root Port 650ns, as seen in Figure 16‐43 on page 791. 

Finally, the Link to the middle Endpoint stops working for some reason as shown in Figure 16‐44 on page 791, and the Switch Port reports DL_Down. Con‐ sequently, the LTR value for that Port must be considered invalid. Since its value was being used as the current conglomerate value, the conglomerate will be updated to the lowest value that is still valid, which is the 1200ns reported by the left‐most Endpoint. The Switch will then subtract its internal latency and report 1150ns to the Root Port with a new LTR message. 

**790** 

**Chapter 16: Power Management** 

_Figure 16‐43: LTR ‐ Change with Update_ 

**==> picture [107 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  650 ns<br>value<br>Conglomerate<br>value 700 ns<br>> _<br>Va i<br>ES}<br>EndpointPCle # =ndnaint§PCle<br>700 ns<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-8"></a>
## 16.8 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

_Figure 16‐44: LTR ‐ Link Down Case_ 

**==> picture [121 x 75] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>value<br>Conglomerate  1200 ns115700 ns<br>value<br>Switch<br>**----- End of picture text -----**<br>


**791** 

**PCI Ex ress Technolo p gy** 

**792** 

## _**17 Interrupt Support**_ 

## **The Previous Chapter** 

The previous chapter provides an overall context for the discussion of system power management and a detailed description of PCIe power management, which is compatible with the _PCI Bus PM Interface Spec_ and the _Advanced Config‐ uration and Power Interface_ (ACPI) spec. PCIe defines extensions to the PCI‐PM spec that focus primarily on Link Power and event management. An overview of the OnNow Initiative, ACPI, and the involvement of the Windows OS is also provided. 

## **This Chapter** 

This chapter describes the different ways that PCIe Functions can generate interrupts. The old PCI model used pins for this, but sideband signals are unde‐ sirable in a serial model so support for the inband MSI (Message Signaled Inter‐ rupt) mechanism was made mandatory. The PCI INTx# pin operation can still be emulated using PCIe INTx messages for software backward compatibility reasons. Both the PCI legacy INTx# method and the newer versions of MSI/MSI‐ X are described. 

## **The Next Chapter** 

The next chapter describes three types of resets defined for PCIe: Fundamental reset (consisting of cold and warm reset), hot reset, and function‐level reset (FLR). The use of a sideband reset PERST# signal to generate a system reset is discussed, and so is the inband TS1 based Hot Reset described. 

**793** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Interrupt Support Background** 

## **General** 

The PCI architecture supported interrupts from peripheral devices as a means of improving their performance and offloading the CPU from the need to poll devices to determine when they require servicing. PCIe inherits this support largely unchanged from PCI, allowing software backwards compatibility to PCI. We provide a background to system interrupt handling in this chapter, but the reader who wants more details on interrupts is encouraged to look into these references: 

- For PCI interrupt background, refer to the PCI spec rev 3.0 or to chapter 14 of MindShare’s textbook: PCI System Architecture (www.mindshare.com). 

- To learn more about Local and IO APICs, refer to MindShare’s textbook: x86 Instruction Set Architecture. 

## **Two Methods of Interrupt Delivery** 

PCI used sideband interrupt wires that were routed to a central interrupt con‐ troller. This method worked well in simple, single‐CPU systems, but had some shortcomings that motivated moving to a newer method called MSI (Message Signaled Interrupts) with an extension called MSI‐X (eXtented). 

**Legacy PCI Interrupt Delivery** — This original mechanism defined for the PCI bus consists of up to four signals per device or INTx# (INTA#, INTB#, INTC#, and INTD#) as shown in Figure 17‐1 on page 795. In this model, the pins are shared by wire‐ORing them together, and they’d eventually be connected to an input on the 8259 PIC (Programmable Interrupt Controller). When a pin is asserted, the PIC in turn asserts its interrupt request pin to the CPU as part of a process described in “The Legacy Model” on page 796. 

PCIe supports this PCI interrupt functionality for backward compatibility, but a design goal for serial transports is to minimize the pin count. As a result, the INTx# signals were not implemented as sideband pins. Instead, a Function can generate an inband interrupt message packet to indicate the assertion or deas‐ sertion of a pin. These messages act as “virtual wires”, and target the interrupt controller in the system (typically in the Root Complex), as shown in Figure 17‐ 2 on page 796. This picture also illustrates how an older PCI device using the 

**794** 

**Chapter 17: Interrupt Support** 

pins can work in a PCIe system; the bridge translates the assertion of a pin into an interrupt emulation message (INTx) going upstream to the Root Complex. The expectation is that PCIe devices would not normally need to use the INTx messages but, at the time of this writing, in practice they often do because sys‐ tem software has not been updated to support MSI. 

_Figure 17‐1: PCI Interrupt Delivery_ 

**— MSI I nterrupt Delivery** MSI eliminates the need for sideband signals by using memory writes to deliver the interrupt notification. The term “Message Signaled Interrupt” can be confusing because its name includes the term “Mes‐ sage” which is a type of TLP in PCIe, but an MSI interrupt is a Posted Memory Write instead of a Message transaction. MSI memory writes are distinguished from other memory writes only by the addresses they target, which are typi‐ cally reserved by the system for interrupt delivery (e.g., x86‐based systems tra‐ ditionally reserve the address range FEEx_xxxxh for interrupt delivery). 

Figure 17‐2 illustrates the delivery of interrupts from various types of PCIe devices. All PCIe devices are required to support MSI, but software may or may not support MSI, in which case, the INTx messages would be used. Figure 17‐2 also shows how a PCIe‐to‐PCI Bridge is required to convert sideband interrupts from connected PCI devices to PCIe‐supported INTx messages. 

**795** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 17‐2: Interrupt Delivery Options in PCIe System_ 

**==> picture [370 x 274] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>Interrupt Controller<br>INTx<br>MSI or Message<br>INTx Message<br>PCIe<br>Switch<br>MSI or MSI or Bridge<br>INTx Message INTx Message to PCI<br>or PCI-X<br>INTx#<br>PCIe Legacy<br>PCI/PCI-X<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


## **The Legacy Model** 

## **General** 

To illustrate the legacy interrupt delivery model, refer to Figure 17‐3 on page 797 and consider the usual steps involved in interrupt delivery using the legacy method of interrupt pins: 

1. The device generates an interrupt by asserting its pin to the controller. In older systems this controller was typically an Intel 8259 PIC that had 15 IRQ inputs and one INTR output. The PIC would then assert INTR to inform the CPU that one or more interrupts were pending. 

**796** 

**Chapter 17: Interrupt Support** 

2. Once the CPU detects the assertion of INTR and is ready to act on it, it must identify which interrupt actually needs service, and that is done by the CPU issuing a special command on the processor bus called an Interrupt Acknowledge. 

3. This command is routed by the system to the PIC, which returns an 8‐bit value called the Interrupt Vector to report the highest priority interrupt cur‐ rently pending. A unique vector would have been programmed earlier by system software for each IRQ input. 

4. The interrupt handler then uses the vector as an offset into the Interrupt Table (an area set up by software to contain the start addresses of all the Interrupt Service Routines, ISRs), and fetches the ISR start address it finds at that location. 

5. That address would point to the first instruction of the ISR that had been set up to handle this interrupt. This handler would be executed, servicing the interrupt and telling its device to deassert its INTx# line and then would return control to the previously interrupted task. 

_Figure 17‐3: Legacy Interrupt Example_ 

**==> picture [304 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTR<br>CPU Memory<br>5<br>Interrupt Service<br>Interrupt<br>Vector Routine (ISR)<br>Acknowledge<br>4<br>North Bridge<br>Interrupt Table (ISR<br>starting addresses)<br>PCI Bus<br>2 3<br>Bridge<br>Data Buffer<br>South Bridge<br>PCI Bus<br>1<br>Interrupt Controller<br>(PIC) INTA#<br>Device<br>**----- End of picture text -----**<br>


**797** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Changes to Support Multiple Processors** 

This model works well for single‐CPU systems, but has a limitation that makes it sub‐optimal in a multi‐CPU system. The problem is that the INTR pin can only be connected to one CPU. If multiple processors are present then only one of them will see the interrupts and will have to service them all while the other CPUs won’t see any of them. To obtain the best performance, such systems really need an even distribution of the system tasks across all the processors, referred to as SMP (Symmetric Multi‐Processing) but the pin model won’t sup‐ port it. 

To achieve better SMP, a new model was needed, and toward this end the PIC was modified to become the IO APIC (Advanced Programmable Interrupt Con‐ troller). The IO APIC was designed to have a separate small bus, called the APIC Bus, over which it could deliver interrupt messages, as shown in Figure 17‐4 on page 799. In this model, the message contained the interrupt vector number, so there was no need for the CPU to send an Interrupt Acknowledge down into the IO world to fetch it. The APIC Bus connected to a new internal logic block within the processors called the Local APIC. The bus was shared among all the agents and any of them could initiate messages on it but, for our purposes, the interesting part is its use for interrupt delivery from peripherals. Those interrupts could now be statically assigned by software to be serviced by different CPUs, multiple CPUs or even dynamically assigned by the IO APIC. 

**798** 

**Chapter 17: Interrupt Support** 

_Figure 17‐4: APIC Model for Interrupt Delivery_ 

**==> picture [316 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Local Local<br>APIC APIC<br>CPU CPU<br>Memory<br>APIC<br>bus North Bridge<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>PCI Bus<br>Interrupt Controller<br>(IO APIC) INTA#<br>Device<br>**----- End of picture text -----**<br>


That model, known as the APIC model, was sufficient for several years but still depended on sideband pins from the peripheral devices to work. Another limi‐ tation of this model was the number of IRQs (interrupt request lines) into the IO APIC. Without a very large number of IRQs, peripheral devices had to share IRQs which means added latency anytime that IRQ is asserted because there could be multiple devices that could have asserted it and software must evalu‐ ate all of them. This technique of linking multiple ISRs together was often referred to as interrupt chaining. Eventually, because of this issue and a couple other minor issues, another improvement came along. 

Why not have the peripheral devices themselves send interrupt messages directly to the Local APICs? All that is needed is a communications path which already exists in the form of the PCI bus and the processor bus. So the APIC bus was eliminated and all interrupts were delivered to the Local APICs in the form of memory writes, referred to as MSIs or Message Signaled Interrupts. These MSIs were targeting a special address that the system understood to be an inter‐ rupt message targeting the Local APICs. (This special address address was tra‐ 

**799** 

**PCI Ex ress 3.0 Technolo p gy** 

ditionally FEEx_xxxxh for x86‐based systems.) Even the IO APIC was programmed to send its interrupt notifications over the ordinary data bus using memory writes (MSI). Now it simply sends an MSI memory write across the data bus targeting the memory address of the desired processor’s Local APIC, and that has the effect of notifying the processor of the interrupt. 

This model is known as the xAPIC model, and since it is not based on sideband signals which go into an interrupt controller with a limited number of inputs, the need to share interrupts is almost eliminated. More information can be found about this model in “An MSI Solution” on page 827.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-16-9"></a>
## 16.9 Power Management | 电源管理

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

PCI added MSI support as an option years ago and PCIe made that capability a requirement. A peripheral that can generate MSI transactions on its own opens new options for handling interrupts, such as giving each Function the ability to generate multiple unique interrupts instead of just one. 

## **Legacy PCI Interrupt Delivery** 

This section provides more detail on legacy PCI interrupt delivery. Readers familiar with PCI may wish to proceed to “Virtual INTx Signaling” on page 805 to learn more about how PCIe emulates this legacy model, or to “The MSI Model” on page 812 to learn more about that method. 

PCI devices that use interrupts have two options. They may use either: 

- INTx# active low‐level signals that can be shared and were defined in the original spec. 

- Message Signaled Interrupts that were added as an option with the 2.2 ver‐ sion of the spec. MSI needs no modification for use in a PCIe system. 

## **Device INTx# Pins** 

A PCI device can implement up to 4 INTx# signals (INTA#, INTB#, INTC#, and INTD#). More than one pin is available because PCI devices can support up to 8 functions, each of which is allowed to drive one (but only one) interrupt pin. When PCI was developed, a typical system used a chipset that included the 15‐ input 8259 PIC, so that’s how many IRQs (which map to interrupt vectors) that were available to the system. However, many of those were already used for system purposes like the system timer, keyboard interrupt, mouse interrupt, and so on. In addition, some pins were reserved for ISA cards that could still be plugged into these older systems. Consequently, the PCI spec writers consid‐ ered that only four IRQs would reliably be available for their new bus, and so the spec only supported four interrupt pins. However, as you probably know, there are typically more than four PCI devices on a PCI bus and even a single device could have more than four functions inside, each wanting its own inter‐ 

**800** 

**Chapter 17: Interrupt Support** 

rupt. These reasons are why the PCI interrupts were designed to be level‐sensi‐ tive and shareable. These signals could simply be wire‐ORed together to get down to a handful of resulting outputs, each one representing interrupt requests. Since they are shared, when an interrupt is detected, the interrupt handler software will need to go through the list of functions that are sharing the same pin and test to see which ones need servicing. 

## **Determining INTx# Pin Support** 

PCI functions indicate support for an INTx# signal in their configuration head‐ ers. The read‐only Interrupt Pin register illustrated in Figure 17‐5 indicates whether an INTx# is supported by this function and if so, which interrupt pin will it assert when requesting an interrupt. 

_Figure 17‐5: Interrupt Registers in PCI Configuration Header_ 

**==> picture [284 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 2 Byte1 0 DW<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>BIST HeaderType LatencyTimer CacheLineSize 03 00h = IRQ0<br>04 01h = IRQ1<br>Base Address 0<br>Base Address 1 05 RW 02h = IRQ2<br>03h = IRQ3<br>06 access<br>Base Address 2 04h = IRQ4<br>Base Address 3 07 05h = IRQ5<br>08 :<br>Base Address 4 :<br>:<br>09<br>Base Address 5 FEh = IRQ254<br>10<br>CardBus CIS Pointer FFh = IRQ255<br>Subsystem ID SubsystemVendor ID 11<br>Expansion ROM 12<br>Base Address<br>Reserved CapabilitiesPointer 13 RO 00h = No INTx# pin used<br>Reserved 14 access 01h = INTA#<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 02h = INTB#03h = INTC#<br>04h = INTD#<br>**----- End of picture text -----**<br>


**801** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Interrupt Routing** 

The Interrupt Line register shown in Figure 17‐5 on page 801 gives the next information that a driver needs to know: the input pin of the PIC to which this pin has been connected. The PIC is programmed by system software with a unique vector number for each input pin (IRQ). The vector for the highest‐prior‐ ity interrupt asserted is reported to the processor who then uses that vector to index into a corresponding entry in the interrupt vector table. This entry points to the interrupting device’s interrupt service routine which the processor exe‐ cutes. 

The platform designer assigns the routing of INTx# pins from devices. They can be routed in a variety of ways, but ultimately each INTx# pin connects to an input of the interrupt controller. Figure 17‐6 on page 803 illustrates an example in which several PCI device interrupts are connected to the interrupt controller through a programmable router. All signals connected to a given input of the programmable router will be directed to a specific input of the interrupt con‐ troller. Functions whose interrupts are routed to a common interrupt controller input will all have the same Interrupt Line number assigned to them by plat‐ form software (typically firmware). In this example, IRQ15 has three PCI INTx# inputs from different devices connected to it. Consequently, the functions using these INTx# lines will share IRQ15 and will therefore all cause the controller to send the same vector when queried. That vector will have the three ISRs for the different Functions chained together. 

## **Associating the INTx# Line to an IRQ Number** 

Based on system requirements, the router is programmed to connect its four inputs to four available PIC inputs. Once this is done, the routing of the INTx# pin associated with each function is known and the Interrupt Line number is written by software into each Function. The value is ultimately read by the Function’s device driver so it will know which interrupt table entry it has been assigned. That’s the place where the starting address of its ISR will be written, a process referred to as “hooking the interrupt”. When this function later gener‐ ates an interrupt, the CPU will receive the vector number that corresponds to the IRQ specified in the Interrupt Line register. The CPU uses this vector to index into the interrupt vector table to fetch the entry point of the interrupt ser‐ vice routine associated with the Function’s device driver. 

**802** 

**Chapter 17: Interrupt Support** 

_Figure 17‐6: INTx Signal Routing is Platform Specific_ 

**==> picture [371 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTA#<br>INTA#<br>INTB# ISA<br>Slave<br>Programmable 8259A<br>Interrupt<br>Interrupt<br>Router<br>Controller<br>INTA#<br>IRQ8<br>IRQ9 (IRQ2)<br>IRQ10<br>INTA# IRQ11<br>INTB# IRQ12 ISA<br>INTC# Input 0# IRQ13 Master<br>INTD# InInput 2#put 1# IRQ14 IRQ15 Interrupt8259A<br>Controller<br>INTA# Input 3#<br>IRQ0<br>IRQ1<br>Interrupt<br>to CPU<br>INTA# IRQ3<br>INTB# IRQ4<br>IRQ5<br>IRQ6<br>IRQ7<br>INTA#<br>**----- End of picture text -----**<br>


## **INTx# Signaling** 

The INTx# lines are active‐low signals implemented as open‐drain with a pul‐ lup resistor provided on each line by the system. Multiple devices connected to the same PCI interrupt request signal line can assert it simultaneously without damage. 

When a Function signals an interrupt it also sets the Interrupt Status bit located in the Status register of the config header. This bit can be read by system soft‐ ware to see if an interrupt is currently pending. (See Figure 17‐8 on page 805.) 

**Interrupt Disable.** The 2.3 PCI spec added an Interrupt Disable bit (Bit 10) to the Command register of the config header. See Figure 17‐7 on page 804. The bit is cleared at reset permitting INTx# signal generation, but software may set it 

**803** 

**PCI Ex ress 3.0 Technolo p gy** 

to prevent that. Note that the Interrupt Disable bit has no effect on Message Sig‐ nalled Interrupts (MSI). MSIs are enabled via the Command Register in the MSI Capability structure. Enabling MSI automatically has the effect of disabling interrupt pins or emulation. 

**Interrupt Status.** The PCI 2.3 spec added a read‐only Interrupt Status bit to the configuration status register (pictured in Figure 17‐8 on page 805). A func‐ tion must set this status bit when an interrupt is pending. In addition, if the Interrupt Disable bit in the Command register of the header is cleared (i.e. inter‐ rupts enabled), then the function’s INTx# signal is asserted when this status bit is set. This bit is unaffected by the state of the Interrupt Disable bit. 

_Figure 17‐7: Configuration Command Register — Interrupt Disable Field_ 

**==> picture [316 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 11 10 9 8 7 6 5 4 3 2 1 0<br>Reserved R<br>Interrupt Disable, was Reserved<br>Fast Back-to-Back Enable<br>SERR# Enable<br>Reserved, was Stepping Control<br>Parity Error Response<br>VGA Palette Snoop Enable<br>Memory Write and Invalidate Enable<br>Special Cycles<br>Bus Master<br>Memory Space<br>IO Space<br>**----- End of picture text -----**<br>


**804** 

**Chapter 17: Interrupt Support** 

_Figure 17‐8: Configuration Status Register — Interrupt Status Field_ 

**==> picture [342 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 8 7 6 5 4 3 2 0<br>R Reserved<br>Interrupt Status<br>Capabilities List<br>66MHz-Capable<br>Reserved<br>Fast Back-to-Back Capable<br>Master Data Parity Error<br>DEVSEL Timing<br>Signalled Target-Abort<br>Received Target-Abort<br>Received Master-Abort<br>Signalled System Error<br>Detected Parity Error<br>**----- End of picture text -----**<br>


## **Virtual INTx Signaling** 

## **General** 

If circumstances make the use of MSI not possible in a PCIe topology, the INTx signaling model would be used. Following are two examples of devices that would need to be able to use INTx messages: 

**PCIe‐to‐(PCI or PCI‐X) bridges** — Most PCI devices will use the INTx# pins because MSI support is optional for them. Since PCIe doesn’t support sideband interrupt signaling, the inband messages are used instead. The interrupt con‐ troller understands the message and delivers an interrupt request to the CPU which would include a pre‐programmed vector number. 

**Boot Devices** — PC systems commonly use the legacy interrupt model during the boot sequence because MSI usually requires OS‐level initialization. Gener‐ ally, a minimum of three subsystems are needed for booting: an output to the operator such as video, an input from the operator which is typically the key‐ board, and a device that can be used to fetch the OS, typically a hard drive. PCIe devices involved in initializing the system are called “boot devices.” Boot devices will use legacy interrupt support until the OS and device drivers are loaded, after which it’s preferable they use MSI. 

**805** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Virtual INTx Wire Delivery** 

Figure 17‐9 on page 806 illustrates a system with a PCIe Endpoint and a PCI Express‐to‐PCI Bridge. If we assume software has not enabled MSI on the End‐ point, it will deliver interrupt requests with INTx messages. In this example, the bridge is propogating pin‐based interrupts from connected PCI devices with INTx messages. As can be seen, the bridge sends an INTB messages to signal the assertion and deassertion of its INTB# input from the PCI bus. The PCIe Endpoint is shown signaling an INTA using emulation messages. Note that INTx# signaling involves two messages: 

- **Assert_INTx** messages indicate a high‐to‐low transition (from inactive to active) of the virtual INTx# signal. 

- **Deassert_INTx** messages indicate a low‐to‐high transition. 

When a Function delivers an Assert_INTx message, it also sets its Interrupt Sta‐ tus bit in the Configuration Status register, just as it would if it asserted the physical INTx# pin (see Figure 17‐8 on page 805). 

_Figure 17‐9: Example of INTx Messages to Virtualize INTA#‐INTD# Signal Transitions_ 

**==> picture [230 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
