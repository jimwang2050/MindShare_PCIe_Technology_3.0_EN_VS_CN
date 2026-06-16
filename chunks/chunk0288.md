Initial State after any<br>Reset or as directed<br>by the Data Link Layer<br>Disabled<br>Detect<br>Training States<br>Re-Training State<br>External<br>Loop back Power Mgt States<br>Polling<br>ASPM States<br>Hot<br>Reset Other States<br>From<br>Configuration From Configuration<br>or Recovery<br>Recovery<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


## **Overview of LTSSM States** 

Below is a brief description of the 11 high‐level LTSSM states. 

- **Detect** : The initial state after reset. In this state, a device electrically detects a Receiver is present at the far end of the Link. That’s an unusual thing in the world of serial transports, but it’s done to facilitate testing, as we’ll see in the next state. Detect may also be entered from a number of other LTSSM states as described later. 

- **Polling** : In this state, Transmitters begin to send TS1s and TS2s (at 2.5 GT/s for backward compatibility) so that Receivers can use them to accomplish the following: 

   - Achieve Bit Lock 

   - Acquire Symbol Lock or Block Lock 

   - Correct Lane polarity inversion, if needed 

   - Learn available Lane data rates 

**519** 

**PCI Ex ress Technolo p gy** 

   - If directed, Initiate the Compliance test sequence: The way this works is that if a receiver was detected in the Detect state but no incoming signal is seen, it’s understood to mean that the device has been connected to a test load. In that case, it should send the specified Compliance test pat‐ tern to facilitate testing. This allows test equipment to quickly verify that voltage, BER, timing, and other parameters are within tolerance. 

- **Configuration** : Upstream and Downstream components now play specific roles as they continue to exchange TS1s and TS2s at 2.5 GT/s to accomplish the following: 

   - Determine Link width 

   - Assign Lane numbers 

   - Optionally check for Lane reversal and correct it 

   - Deskew Lane‐to‐Lane timing differences 

      - From this state, scrambling can be disabled, the Disable and Loopback states can be entered, and the number of FTS Ordered Sets required to transition from the L0s state to the L0 state is recorded from the TS1s and TS2s. 

- **L0** : This is the normal, fully‐active state of a Link during which TLPs, DLLPs and Ordered Sets can be exchanged. In this state, the Link could be running at higher speeds than 2.5 GT/s, but only after re‐training (Recovery) the Link and going through a speed change procedure. 

- **Recovery** : This state is entered when the Link needs re‐training. This could be caused by errors in L0, or recovery from L1 back to L0, or recovery from L0s if the Link does not train properly using the FTS sequence. In Recovery, Bit Lock and Symbol/Block Lock are re‐established in a manner similar to that used in the Polling state but it typically takes much less time. 

- **L0s** : This ASPM state is designed to provide some power savings while affording a quick recovery time back to L0. It’s entered when one Transmitter sends the EIOS while in the L0 state. Exit from L0s involves sending FTSs to quickly re‐acquire Bit and Symbol/Block Lock. 

- **L1** : This state provides greater power savings by trading off a longer recovery time than L0s does (see “Active State Power Management (ASPM)” on page 735). Entry into L1 involves a negotiation between both Link partners to enter it together and can occur in one of two ways: 

   - The first is autonomous with ASPM: hardware in an Upstream Port with no scheduled TLPs or DLLPs to transmit can automatically negotiate to put its Link into the L1 state. If the Downstream Port agrees, the Link enters L1. If not, the Upstream Port will enter L0s instead (if enabled). 

   - The second is the result of power management software issuing a com‐ manding a device to a low‐power state (D1, D2, or D3Hot). As a result, the Upstream Port notifies the Downstream Port that they must enter L1, the Downstream Port acknowledges that, and they enter L1. 

**520** 

**Chapter 14: Link Initialization & Training** 

- **L2** : In this state the main power to the devices is turned off to achieve a greater power savings. Almost all of the logic is off, but a small amount of power is still available from the Vaux source to allow the device to indicate a wakeup event. An Upstream Port that supports this wakeup capability can send a very low frequency signal called the Beacon and a Downstream Port can forward it to the Root Complex to get system attention (see “Beacon Sig‐ naling” on page 483). Using the Beacon, or a side‐band WAKE# signal, a device can trigger a system wakeup event to get main power restored. [An L3 Link power state is also defined, but it doesn’t relate to the LTSSM states. The L3 state is the full‐off condition in which Vaux power is not available and a wakeup event can’t be signaled.] 

- **Loopback** : This state is used for testing but exactly what a Receiver does in this mode (for example: how much of the logic participates) is left unspeci‐ fied. The basic operation is simple enough: the device that will be the Loop‐ back Master sends TS1 Ordered Sets that have the Loopback bit set in the Training Control field to the device that will be the Loopback Slave. When a device sees two consecutive TS1s with the Loopback bit set, it enters the Loopback state as the Loopback Slave and echoes back everything that comes in. The Master, recognizing that what it is sending is now being echoed, sends any pattern of Symbols that follow the 8b/10b encoding rules, and the Slave echoes them back exactly as they were sent, providing a round‐trip ver‐ ification of Link integrity. 

- **Disable** : This state allows a configured Link to be disabled. In this state, the Transmitter is in the Electrical Idle state while the Receiver is in the low impedance state. This might be necessary because the Link has become unre‐ liable or due to a surprise removal of the device. Software commands a device to do this by setting the Disable bit in the Link Control register. The device then sends 16 TS1s with the Disable Link bit set in the TS1 Training Control field. Receivers are disabled when they receive those TS1s. 

- **Hot Reset:** Software can reset a Link by setting the Secondary Bus Reset bit in the Bridge Control register. That causes the bridge’s Downstream Port to send TS1s with the Hot Reset bit set in the TS1 Training Control field (see “Hot Reset (In‐band Reset)” on page 837) When a Receiver sees two consecutive TS1s with the Hot Reset bit set, it must reset its device. 

## **Introductions, Examples and State/Substates** 

The balance of this chapter covers each of the LTSSM states. Depending on the complexity of a given state, the discussion may include an introduction, general background, and/or examples that accompanies the detailed discussion of the State/Substate. In some cases, the reader may choose to skip the detailed cover‐ 

**521** 

## **PCI Ex ress Technolo p gy** 

age and jump to introductory material. Each section is organized to facilitate these options. 

Every device must perform initial link training at the base rate of 2.5 GT/s. Fig‐ ure 14‐7 highlights the states involved in the initial training sequence. Devices capable of operating at 5.0 or 8.0 GT/s must transition to the Recovery state to change the speed to the higher rate chosen. 

_Figure 14‐7: States Involved in Initial Link Training at 2.5 Gb/s_ 

**==> picture [304 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
Initial State after any<br>Reset or as directed<br>by the Data Link Layer<br>Disabled<br>Detect<br>Training States<br>Re-Training State<br>External<br>Loop back Power Mgt States<br>Polling<br>ASPM States<br>Hot<br>Reset Other States<br>From<br>Configuration From Configuration<br>or Recovery<br>Recovery<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


## **Detect State** 

## **Introduction** 

Figure 14‐8 represents the two substates and transitions associated with the Detect state. The actions associated with the Detect state are performed by each 

**522** 

**Chapter 14: Link Initialization & Training** 

transmitter in the process of detecting the presence of a receiver at the opposite end of the link. Because there are only two substates and because they are fairly simple, we will move directly to the substate discussions. 

_Figure 14‐8: Detect State Machine_ 

**==> picture [288 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from Reset.<br>Also from Disabled,<br>Loopback, L2, Polling,<br>Configuration or<br>Recovery<br>No Electrical<br>Idle on Link or<br>12 ms timeout Receiver<br>Detected<br>Detect.Quiet Detect.Active<br>No Detect<br>12 ms Charge or<br>DC common mode<br>voltage stable<br>Exit to<br>Polling<br>**----- End of picture text -----**<br>


## **Detailed Detect Substate** 

## **Detect.Quiet** 

This substate is the initial state after any reset (except Function Level Reset) or power‐up event and must be entered within 20 ms after Reset. This substate is also entered from other states if unable to move forward (See the states that may enter Detect.Quiet in Figure 14‐8 on page 523). The properties of this substate are listed below: 

- The Transmitter starts in Electrical Idle (but the DC common mode voltage doesn’t have to be within the normally‐specified range). 

- The intended data rate is set to 2.5 GT/s (Gen1). If it set to a different rate when this substate was entered, the LTSSM must stay in this substate for 1ms before changing the rate to Gen1. 

- The Physical Layer’s status bit (LinkUp = 0) informs the Data Link Layer that the Link is not operational. The LinkUp status bit is an internal state bit 

**523** 

## **PCI Ex ress Technolo p gy** 

- (not found in standard config space) and also indicates when the Physical Layer has completed Link Training (LinkUp=1), thereby informing the Data Link Layer and Flow Control initialization to begin its part of Link initial‐ ization (for more on this, see “The FC Initialization Sequence” on page 223). 

- • Any previous equalization (Eq.) status is cleared by setting the four Link Status 2 register bits to zero: Eq. Phase 1 Successful, Eq. Phase 2 Successful, Eq. Phase 3 Successful, Eq. Complete. 

- Variables: 

   - Several variables are cleared to zero: (directed_speed_change=0b, upconfigure_capable=0b, equalization_done_8GT_data_rate=0b, idle_to_rlock_transitioned=00h). The select_deemphasis variable setting depends on the port type: for an Upstream Port it’s selected by hardware, while for a Downstream Port it takes the value in the Link Control 2 regis‐ ter of the Selectable Preset/De‐emphasis field. 

   - Since these variables were defined beginning with the 2.0 spec version, devices designed to earlier spec versions won’t have them and will behave as if directed_speed_change and upconfigure_capable were set to 0b and idle_to_rlock_transitioned was set to FFh. 

## _Exit to “Detect.Active”_ 

The next substate is Detect.Active after a 12 ms timeout or when any Lane exits Electrical Idle. 

## **Detect.Active** 

This substate is entered from Detect.Quiet. At this time the Transmitter tests whether a Receiver is connected on each Lane by setting a DC common mode voltage of any value in the legal range and then changing it. The detection logic observes the rate of change as the time it takes the line voltage to charge up and compares it to an expected time, such as how long it would take without a Receiver termination. If a Receiver is attached, the charge time will be much longer, making it easy to recognize. For more details on this process, see “Receiver Detection” on page 460. To simplify the discussions that follow, Lanes that detect a Receiver during this substate are referred to as “Detected Lanes.” 

## _Exit to “Detect.Quiet”_ 
