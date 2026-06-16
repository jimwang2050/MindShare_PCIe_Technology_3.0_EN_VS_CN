As an aside regarding Electrical Idle, the early versions of the spec expected that Electrical Idle would be based on a squelch‐detect circuit measuring a voltage threshold. Later, as speeds increased, detecting such small voltage differences became increasingly difficult. Consequently, more recent spec versions allow Electrical Idle to be inferred by observing Link behavior, rather than actually measuring the voltage. However, if the voltage level isn’t used to detect entry into Electrical Idle, then it also can’t be used to detect an exit from it. To handle that problem, a new Ordered Set was intro‐ duced called the EIEOS (Electrical Idle Exit Ordered Set). The EIEOS con‐ sists of alternating bytes of all zeros and all ones and creates the effect of a low‐frequency clock on the Lanes. Once a Receiver has entered Electrical Idle it can watch for this pattern on the signal to inform it that the Link is exiting from Electrical Idle. 

_Exit to “Rx_L0s.FTS”_ 

The next state will be Rx_L0s.FTS after the Receiver detects an exit from Electrical Idle. 

## **Rx_L0s.FTS.** 

In this substate, the Receiver has noticed an exit from Electrical Idle and is now trying to re‐establish Bit and Symbol or Block lock on the incoming bit stream (which are really FTS ordered sets). 

_Exit to “L0 State”_ 

The next state will be L0 if an SOS is received in 8b/10b encoding or an SDS in 128b/130b encoding on all configured Lanes. The Receiver must be able to accept valid data immediately after that, and Lane‐to‐Lane de‐skew must be completed before leaving this state. 

**606** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Recovery State”_ 

Otherwise the next state will be Recovery after the N_FTS timeout. If so, the Transmitter must also go to Recovery, although it’s allowed to finish any TLP or DLLP that was in progress. If the timeout occurs, the spec recommends that the N_FTS value be increased to reduce the likelihood of it happening again. The N_FTS timeout is defined as follows: 

For 8b/10b, the minimum timeout is given as 40 * [N_FTS + 3] * UI, while the maximum allowed is twice that time. Since 10 bits (UI repre‐ sents one bit time) are needed per Symbol, this works out to (4*N_FTS + 12) Symbols. The extra 12 Symbols are explained as 6 for a max‐sized SOS + 4 for the possible extra FTS + 2 more for Symbol margin. In sum‐ mary, then, the minimum time is the time it should take to send the requested number of FTSs plus 12 Symbols, while the maximum time is twice as much as that. 

If the extended synch bit is set, the min time = 2048 FTSs and the max time = 4096 FTSs. The actual timeout value a Receiver will use must also take into account the 4 to 8 EIE Symbols for speeds other than 2.5 GT/s. 

For 128b/130b, the timeout value is given as a minimum of 130 * [N_FTS + 5 + 12 + Floor (N_FTS/32)] * UI and a max of twice that time. The value 130 * UI means 130 bit times which represents one Block, so if we remove those two values we can say we’re looking at [N_FTS + 5 + 12 + Floor (N_FTS/32)] Blocks. The value [5 + Floor (N_FTS/32)] represents the EIEOSs that will need to be sent during this time. One EIEOS will be sent after every 32 FTSs, so Floor (N_FTS/32) gives that number. The other 5 are accounted for by the first EIEOS, the last EIEOS, the SDS, the periodic EIEOS and an additional EIEOS in case the Transmitter chooses to send two EIEOS followed by an SDS when N_FTS is divisi‐ ble by 32. Finally, the value of 12 represents the number of SOSs that will be sent if the extended synch bit is set. When that bit is set, the tim‐ eout will use N_FTS = 4096. 

## **L1 State** 

This Link power state trades a longer exit latency for more aggressive power management compared to the L0s state. L1 is an option for ASPM, like L0s, meaning devices can enter and exit this state automatically under hardware control without any software involvement. However, unlike L0s, software is also able to direct an Upstream Port to initiate a change to L1, and it does so by writing the device power state to a lower level (D1, D2, or D3). The L1 state is also different from L0s in that it affects both directions of the Link. 

**607** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐42: L1 State Machine_ 

**==> picture [260 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Directed and Remain in<br>EIOS Tx & Rx TTX-IDLE-MIN Electrical Idle<br>= 20 ns L1.Idle<br>L1.Entry<br>(Electrical Idle)<br>Tx in Electrical Idle Tx Directed or<br>Rx sees Electrical Idle Exit<br>Exit to<br>Recovery<br>**----- End of picture text -----**<br>


Since going to Electrical Idle can indicate a desire by the Link partner to enter L0s, L1 or L2, differentiating which should be the next state is handled by hav‐ ing both partners agree beforehand when they’re going to enter L1. A hand‐ shake informs them that the partner is ready and it’s therefore safe to proceed. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. Figure 14‐42 on page 608 shows the L1 state machine, which is described in the following sections. 

## **L1.Entry** 

In order for an Upstream Port to enter this state, it must send a request to enter L1 to its Link Partner and receive acknowledgement that it is OK to put the Link into L1. (The reason for requesting to go into L1 may be because of ASPM or because of software involvement.) Once the L1 request acknowledge is received, the Upstream Port enters the L1.Entry substate. 

In order for a Downstream Port to enter this state, it must receive an L1 enter request from the Upstream Port and send a positive response to that request. Then the Downstream Port waits to receive an Electrical Idle Ordered Set (EIOS) and have its receive lanes drop to Electrical Idle. It is at this point that the Downstream Port enters the L1.Entry substate. 

**608** 

**Chapter 14: Link Initialization & Training** 

## _During L1.Entry_ 

All configured Transmitters send an EIOS and enter Electrical Idle while maintaining the proper DC common mode voltage. 

## _Exit to “L1.Idle”_ 

The next state will be L1.Idle after the TTX‐IDLE‐MIN timeout (20ns). This time is intended to ensure that the Transmitter has established the Electrical Idle condition. 

## **L1.Idle** 

During this substate, Transmitters remain in the Electrical Idle. 

For rates other than 2.5 GT/s the LTSSM must remain in this substate for at least 40ns. In the spec, this delay is said “to account for the delay in the logic levels to arm the Electrical Idle detection circuitry in case the Link enters L1 and immedi‐ ately exits”. 

## _Exit to “Recovery State”_ 

The next state will be Recovery when a Transmitter is directed to change it or when any Receiver detects an exit from Electrical Idle. Reasons for leav‐ ing L1 include the need to deliver a DLLP or TLP, or a desire to change the Link width or speed. If a speed change is desired, a Port is allowed to set the directed_speed_change variable to 1b and must clear the changed_speed_recovery variable to 0b. Optionally, the Port may exit L1 and then initiate the speed change later by setting directed_speed_change to 1b and entering Recovery from L0 instead. 

## **L2 State** 

This is a deeper power state with a longer exit latency than L1. Power Manage‐ ment software directs an Upstream Port to initiate entry into L2 (both directions of the Link go to L2) when its device is placed in the D3Cold power state and the appropriate Link handshakes have been completed. 

Main power will be shut off by the system once it learns that everything is ready. When power is removed, the Link power state will become either L2 or L3, depending on whether a secondary power source called VAUX (auxiliary voltage) is available. If VAUX is present, the Link enters L2; if not, it enters L3. 

The motivation for L2 is to use the small power available from VAUX to inform the system when an event has occurred for which the Link needs to have power 

**609** 

## **PCI Ex ress Technolo p gy** 

restored. There are two standard ways a device can inform the system of such an event. One is a side‐band signal called the WAKE# pin, and the other is an in‐ band signal called a “Beacon.” The L2 state isn’t needed for WAKE#, but is required if the optional Beacon will be used. The spec explicitly states that devices operating at 5.0 or 8.0 GT/s don’t need to support Beacon, so it would seem that this is legacy support and only interesting for devices operating at 2.5 GT/s. For more detail on Link wakeup options, refer to “Waking Non‐Commu‐ nicating Links” on page 772. 

If supported, the Beacon is a low‐frequency (30 KHz ‐ 500 MHz) in‐band signal that an Upstream Port supporting wakeup capability must be able to send on at least Lane 0 and a Downstream Port must be able to receive. Intermediate devices like Switches that receive a Beacon on a Downstream Port must forward it to their Upstream Port. The ultimate destination for the Beacon is the Root Complex, because that’s where the system power control logic is expected to reside. 

A Transmitter going to Electrical Idle could indicate a desire to enter any of the low‐power Link states (L0s, L1 or L2), so a means of differentiating them is needed. For L2, this is handled by having the Link partners agree beforehand that they’re going to enter L2 by using a handshake sequence to ensure that they’re both ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. Figure 14‐43 on page 611 shows the L2 entry and Exit state machine, which is described in the follow‐ ing text. 

**610** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐43: L2 State Machine_ 

**==> picture [349 x 227] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Directed, and<br>EIOS both sent<br>and received Upstream Tx<br>sends Beacon<br>Upstream Port directed to send Beacon,<br>L2.Idle or Downstream Port detects Beacon<br>(Electrical Idle, L2.TransmitWake<br>No DC CMV)<br>Rx termination enabled,<br>Rx looking for  Upstream Rx detects<br>Electrical Idle Exit Electrical Idle Exit<br>Root Port detects Beacon,<br>or Upstream Port sees<br>Electrical Idle Exit Exit to<br>Detect<br>**----- End of picture text -----**<br>


## **L2.Idle** 

To enter this substate, all the necessary handshake process must have already taken place between both ports on the Link and the ports have sent and received the required EIOS. 

All configured Transmitters must remain in the Electrical Idle state for at least the TTX‐IDLE‐MIN timeout (20ns). However, since the main power will now be shut off, they aren’t required to maintain the DC common‐mode voltage within the spec range. Receivers won’t start looking for the Electrical exit condition until at least after the 20ns timeout expires. All Receiver terminations must remain enabled in the low impedance condition. 

## _Exit to “L2.TransmitWake”_ 

The next state will be L2.TransmitWake if the Upstream Port is instructed to send a Beacon (the Beacon is always and only directed upstream to the Root Complex). 

**611** 

**PCI Ex ress Technolo p gy** 

If the Downstream Port of a Switch detects a Beacon, it must direct the Upstream Port of the Switch to exit to L2.TransmitWake and begin sending a Beacon. 

## _Exit to “Detect State”_ 

Once main power is returned, the next state will be Detect. 

If this Port has main power, but it detects an exit from Electrical Idle on any “predetermined” Lanes, meaning those that could be negotiated to be Lane 0 (multi‐Lane Links must have at least two predetermined Lanes), the next state will be detect. When this happens to a Switch Upstream Port, the Switch must also transition its Downstream Ports to Detect. 

## **L2.TransmitWake** 
