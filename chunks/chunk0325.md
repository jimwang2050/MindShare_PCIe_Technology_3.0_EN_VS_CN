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
