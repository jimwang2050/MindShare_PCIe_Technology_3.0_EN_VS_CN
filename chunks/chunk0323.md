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
