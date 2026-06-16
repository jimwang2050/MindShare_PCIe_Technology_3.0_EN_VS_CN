- If a loopback‐capable Transmitter is directed by a higher Layer to send TS Ordered Sets with the Loopback bit asserted or all Lanes that are sending and receiving TS1s receive 2 consecutive TS1s with the Loopback bit set. Whichever Port sends the TS1s with the bit set will become the Loopback master, while the Port that receives them will become the Loopback slave.

## _Exit to "Detect State"_

- After a 24ms timeout if none of the other conditions are true.

**557**

**PCI Express Technology**

## **Configuration.Linkwidth.Accept**

At this point, the Upstream Port is now sending back TS1 ordered‐sets on all its Lanes with the same Link number. The Link number originated from the Downstream Port, and the Upstream Port is simply reflecting that value back on all its Lanes. Now the Downstream Port knows the Link width (number of Lanes receiving the same Link number) and it must start advertising the Lane numbers. So the leader (Downstream Port) continues sending TS1s, but now with the actual Lane numbers designated instead of PAD. Also, all these TS1s will have the same Link number. The detailed behavior for the Downstream and Upstream Lanes are outlined below:

## **Downstream Lanes**

## _During Configuration.Linkwidth.Accept_

- The Downstream Port will now initiate Lane numbers. If a Link can be formed from at least one group of Lanes that all receive two consecutive TS1s and all see the same Link number, then TS1s are sent that keep that same Link number but now assign unique, non‐PAD Lane numbers as well.

## _Exit to "Configuration.Lanenum.Wait"_

- The Downstream Port does not stay in the Configuration.Linkwidth.Accept substate very long. Once it has received the necessary TS1s from the Upstream Port indicating, the Link width, it updates any internal state info that is required, starts sending TS1s with non‐PAD Lane numbers, as indicated above, and immediately transitions to Configuration.Lanenum.Wait to await Lane Number confirmation from the Upstream Port.

## **Upstream Lanes**

## _During Configuration.Linkwidth.Accept_

- The Upstream Port transmits TS1s where one of the received Link numbers is selected and sent back in the TS1s on _all_ the Lanes that received TS1s with a non‐PAD Link number. Any left‐over Lanes that detected a Receiver but no Link number must send TS1s with Link and Lane numbers set to PAD.

## _Exit to "Configuration.Lanenum.Wait"_

- The Upstream Port must respond to the Lane numbers proposed to it by the Link neighbor. If a Link can be formed using Lanes that sent a non‐PAD Link number on their TS1s and received two consecutive TS1s with the same Link number and any non‐PAD Lane number, then it should send TS1s that match the same Lane number assignments, if possible, or are different if necessary (such as with the optional Lane reversal).

**558**

**Chapter 14: Link Initialization & Training**

## **Configuration.Lanenum.Wait**

Prior to discussing the Configuration.Lanenum.Wait state, some background information may be helpful. Lane numbers are assigned sequentially from zero to the maximum number possible for a Link. For example, a x8 Link will be assigned Lane numbers 0 ‐ 7. Ports are required to support a Link as wide as the number of Lanes they have and as small as one Lane. The Lanes will always start with Lane 0 and must be both sequential and contiguous. For example, if some Lanes on a x8 Port aren't working, it might optionally be designed to configure a x4 Link and, if so, it would need to use Lanes 0‐3. As another example, if Lane 2 of a x8 Port is not working, it wouldn't be possible to use Lanes 0, 1, 3, and 4 to form a x4 Link because the Lanes wouldn't be contiguous. Any left‐over Lanes must send TS1s with Link and Lane set to PAD.

A common timing consideration is repeated many times in the spec for the Configuration substates. Rather than repeat it for every case here, just be aware that it applies in general to both Upstream and Downstream Ports:

To avoid configuring a Link smaller than necessary, it's recommended that a multi‐Lane Port delay the final link width evaluation if it sees an error or loses Block Alignment on some Lanes. For 8b/10b, it should wait at least two more TS1s, while for 128b/130b mode it should wait for at least 34 TS1s, but never more than 1ms in any case. The idea is that the Lanes might need settling time after powering up or being reset.

## _Exit to "Detect State"_

After a 2ms timeout if no Link can be configured (e.g.: Lane 0 is not working and Lane Reversal isn't available), or if all Lanes receive two consecutive TS1s with PAD in both the Link and Lane numbers, the link must exit to the Detect State.

## **Downstream Lanes**

## _During Configuration.Lanenum.Wait_

The Downstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met.

## _Exit to "Configuration.Lanenum.Accept"_

If either of the cases listed below is true:

- If two consecutive TS1s have been received on all Lanes with Link and Lane numbers that match what is being transmitted on those Lanes.

**559**

**PCI Express Technology**

- If any Lanes that detected a Receiver see two consecutive TS1s with a Lane number different from when the Lane first entered this substate and at least some Lanes see a non‐PAD Link number. The spec points out that this allows the two Ports to settle on a mutually acceptable Link width.

## _Exit to "Detect State"_

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD.

Upstream Lanes

## _During Configuration.Lanenum.Wait_

The Upstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met.

## _Exit to "Configuration.Lanenum.Accept"_

If either of the cases listed below is true:

- If any Lanes receive two consecutive TS2s.

- If any Lanes receive two consecutive TS1s with a Lane number different from when the Lane first entered this substate and at least some Lanes see a non‐PAD Link number.

Note that Upstream Lanes are allowed to wait up to 1ms before changing to that substate, so as to prevent received errors or skew between Lanes from affecting the final Link configuration.

## _Exit to "Detect State"_

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD.

## **Configuration.Lanenum.Accept**

Downstream Lanes

## _During Configuration.Lanenum.Accept_

The Downstream Port has now received TS1s with non‐PAD Link and Lane numbers. It is at this point that the Downstream Port must decide if a Link can be established with the Lane numbers returned by the Upstream Port. The three possible state transitions are listed below.

## _Exit to "Configuration.Complete"_

If two consecutive TS1s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being transmitted in the TS1s for all the Lanes, then Upstream Port has agreed with the Link and

**560**

**Chapter 14: Link Initialization & Training**

Lane numbers advertised by the Downstream Port and the next substate is Configuration.Complete. Or if the Lane numbers in the received TS1s are reversed from what the Downstream Port advertised, if the Downstream Port supports Lane Reversal, it can still proceed to Configuration.Complete while using the reversed Lane numbers.

The spec points out that the Reversed Lane condition is strictly defined as Lane 0 receiving TS1s with the highest Lane number (total number of Lanes ‐ 1) and the highest Lane number receiving TS1s with Lane number of zero. One thing that can be understood from this is the answer to a question that comes up in class sometimes: Can the Lane numbers be mixed up, rather than sequential? The answer is no, they must be from 0 to n‐1 or from n‐1 to 0; no other options are supported.

If the Configuration state was entered from the Recovery state, a bandwidth change may have been requested. If so, status bits will be updated to report the nature of what happened. Basically, the system needs to report whether this change was initiated because the Link wasn't working reliably or because hardware is simply managing the Link power. The bits are updated as follows:

- If the bandwidth change was initiated by the Downstream Port because of a reliability problem, the Link Bandwidth Management Status bit is set to 1b.

- If the bandwidth change was not initiated by the Downstream Port but the Autonomous Change bit in two consecutive received TS1s is cleared to 0b, the Link Bandwidth Management Status bit is set to 1b.

- Otherwise the Link Autonomous Bandwidth Status bit is set to 1b.

## _Exit to "Configuration.Lanenum.Wait"_

- If a configured Link can be formed with some but not all of the Lanes that receive two consecutive TS1s with the same non‐PAD Link and Lane numbers, those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve a working Link.

The new Lane numbers must start with zero and increase sequentially to cover the Lanes that will be used. Any Lanes that don't receive TS1s can't be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s with Link and Lane set to PAD. For example, if 8 Lanes are available, but Lane 2 doesn't see incoming TS1s, then the Link can't consist of a group that would need Lane 2. Consequently, the x8 and x4 options would not be available, and only a x1 or x2 Link is possible.

**561**

**PCI Express Technology**

## _Exit to "Detect State"_

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers.

## **Upstream Lanes**

## _During Configuration.Lanenum.Accept_

- The Upstream Port has now received either TS2s or TS1s with non‐PAD Link and Lane numbers. It is at this point that the Upstream Port must decide if a Link can be established with the Lane numbers sent by the Downstream Port. The three possible state transitions are listed below.

## _Exit to "Configuration.Complete"_

- If two consecutive TS2s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being transmitted in the TS1s for those Lanes, all is well and the next substate will be Configuration.Complete.

## _Exit to "Configuration.Lanenum.Wait"_

- If a configured Link can be formed with a subset of Lanes that receive two consecutive TS1s with the same non‐PAD Link and Lane numbers, those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve a working Link. The next substate in this case will be Configuration.Lanenum.Wait.

As was the case for the Downstream Lanes, the new Lane numbers must start with zero and increase sequentially to cover the Lanes that will be used. Any Lanes that don't receive TS1s can't be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s with Link and Lane set to PAD.

## _Exit to "Detect State"_

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers, then the next state will be Detect.

## **Configuration.Complete**

This is the only substate of the Configuration state where TS2s are exchanged. As discussed before, the purpose of TS2s is a handshake, or confirmation between the two devices on the link that they are ready to proceed to the next state. So this is the final confirmation of the Link and Lane numbers exchanged in the TS1s leading up to this point.

**562**

**Chapter 14: Link Initialization & Training**

It should be noted that Devices are allowed to change their supported data rates and upconfigure capability when they enter this substate, but not while in it. This is because Devices record the capabilities of their Link partner from what is advertised in these TS2s, as will be described in this section.

## **Downstream Lanes**

## _During Configuration.Complete_

TS2s are sent using the Link and Lane numbers that match the received TS1s. The TS2s can have the Upconfigure Capability bit set if the Port supports a x1 Link using Lane 0 and is able to up‐configure the Link.

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity.

The Downstream Port is transmitting TS2s and watching for TS2s coming back. For future reference, record the number of FTSs that must be sent when exiting from the L0s state from the N_FTS field in the incoming TS2s.

## _Exit to "Configuration.Idle"_

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching rate identifiers, and matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2.

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane and this overrides any previously recorded value. The variable used to track speed changes in Recovery, "changed_speed_recovery", is cleared to zero.

The variable "upconfigure_capable" is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8 consecutive TS2s with the same bit set. Otherwise it's cleared to zero.

Any Lanes that aren't configured as part of the Link are no longer associated with the LTSSM in progress and must either be:

- Associated with a new LTSSM or

- Transitioned to Electrical Idle

   - a)   A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b

**563**

**PCI Express Technology**

since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it's also recommended that those Lanes leave their Receiver terminations on because they'll become part of the Link again if it is upconfigured. If the terminations aren't left on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete. Lanes that weren't part of the Link before can't become part of it through this process, though.

- b)  For the optional crosslink, Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG.

- c) If the LTSSM goes back to Detect, these Lanes will once again be associated with it.

- d)  No EIOS is needed before Lanes go to Electrical Idle, and the transition doesn't have to happen on Symbol or Ordered Set boundaries.

## After a 2ms timeout:

_Exit to "Configuration.Idle"_

Next state is Configuration.Idle if the idle_to_rlock_transitioned variable is less than FFh **and** the current data rate is 8.0 GT/s.

In this transition, the "changed_speed_recovery" variable is cleared to zero. Also, the "upconfigure_capable" variable may be updated, though it's not required to do so, if at least one Lane saw eight consecutive TS2s with matching Link and Lane numbers (non‐PAD). If the transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero.

Lanes that aren't part of the configured Link aren't associated with the LTSSM in progress and have the same requirements as the non‐timeout case listed above.

_Exit to "Detect State"_

Otherwise, the next state is Detect.

## **Upstream Lanes**

_During Configuration.Complete_

TS2s are sent using the Link and Lane numbers that match the received TS2s. The TS2s can have the Upconfigure Capability bit set if the Port supports a x1 Link using Lane 0 and is able to up‐configure the Link.

**564**

**Chapter 14: Link Initialization & Training**

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity.

In this substate, the Upstream Port is receiving TS2s from the Downstream Port, and for future reference, should record the N_FTS field value number of FTSs that must be sent when exiting from the L0s state from the in the incoming TS2s.

## _Exit to "Configuration.Idle"_

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching rate identifiers, and a matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2.

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane, overriding any previously recorded value. The variable used to track speed changes in Recovery, "changed_speed_recovery", is cleared to zero.

The variable "upconfigure_capable" is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8 consecutive TS2s with the same bit set. Otherwise it's cleared to zero.

Any Lanes that aren't configured as part of the Link are no longer associated with the LTSSM in progress and must either be:

- Optionally associated with a new crosslink LTSSM (if this feature is supported), or

- Transitioned to Electrical Idle

   - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it's also recommended that those Lanes leave their Receiver terminations on because they'll become part of the Link again if it is upconfigured. If they're not left on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete. Lanes that weren't part of the Link before can't become part of it through this process, though.

**565**

**PCI Express Technology**

- b)  Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐

   - HIGH‐IMP‐DC‐NEG[.]

- c)    If the LTSSM goes back to Detect, these Lanes will once again be associated with it.

- d)  No EIOS is needed before Lanes go to Electrical Idle, and the transition doesn't have to happen on Symbol or Ordered Set boundaries.

## After a 2ms timeout:

## _Exit to "Configuration.Idle"_

Next state is Configuration.Idle if the idle_to_rlock_transitioned variable is less than FFh **and** the current data rate is 8.0 GT/s.

In this transition, the "changed_speed_recovery" variable is cleared to zero. Also, the "upconfigure_capable" variable may be updated, though it's not required to do so, if at least one Lane saw eight consecutive TS2s with matching Link and Lane numbers (non‐PAD). If the transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero.

Lanes that aren't part of the configured Link aren't associated with the LTSSM in progress and have the same requirements as the non‐timeout case listed above.

## _Exit to "Detect State"_

Otherwise, the next state is Detect.

## **Configuration.Idle**

## _During Configuration.Idle_

In this substate, the transmitter is sending Idle data and waiting for the minimum number of received Idle data so this Link can transition to L0. During this time, the Physical Layer reports to the upper layers that the link is operational (Linkup = 1b).

For 8b/10b encoding, the transmitter is sending Idle data on all configured Lanes. Idle data are just data zeros that get scrambled and encoded.

For 128b/130b encoding, the transmitter sends one SDS Ordered Set on all configured Lanes followed by Idle data Symbols. The first Idle Symbol on Lane 0 is the first Symbol of the Data Stream.

**566**

**Chapter 14: Link Initialization & Training**

## _Exit to "L0 State"_

If using 8b/10b encoding, the next state is L0 if 8 consecutive Idle data symbol times are received on all configured Lanes, and 16 symbol times of idle data were sent after receiving one Idle Symbol.

If using 128b/130b, the next state is L0 if 8 consecutive Idle data are received on all configured Lanes, 16 Idles were sent after receiving one Idle Symbol, and this state wasn't entered by a timeout from Configuration.Complete.

- Lane‐to‐Lane de‐skew must be completed before Data Stream processing begins.

- The Idle Symbols must be received in Data Blocks.

- If software set the Retrain Link bit in the Link Control register since the last transition to L0 from Recovery or Configuration, the Downstream Port must set the Link Bandwidth Management bit in the Link Status register to 1b to indicate that this change was not hardware initiated (autonomous).

- The "idle_to_rlock_transitioned" variable is cleared to 00h on transition to L0.

## After a 2ms timeout:

## _Exit to "Detailed Recovery Substates"_

If the idle_to_rlock_transitioned variable is less than FFh, the next state is Recovery (Recovery.RcvrLock). Then:

- a) For 8.0 GT/s, increment idle_to_rlock_transitioned by 1.

- b)  For 2.5 or 5.0 GT/s, set idle_to_rlock_transitioned to FFh.

- c) NOTE: This variable counts the number of times the LTSSM has transitioned from this state to the Recovery state because the sequence isn't working. The problem may be that equalization hasn't been properly adjusted or that the selected speed just isn't going to work, and the Recovery state will take steps to address these issues. This variable limits the number of these attempts so as to avoid an endless loop. If the Link still isn't working after doing this 256 times (when the count reaches FFh), go back to Detect and start over, hoping for a better result.

_Exit to "Detect State"_

Otherwise (meaning idle_to_rlock = FFh), the next state is Detect.

**567**

**PCI Express Technology**

## **L0 State**

This is the normal, fully‐operational Link state, during which Logical Idle, TLPs and DLLPs are exchanged between Link neighbors. L0 is achieved immediately following the conclusion of the Link Training process. The Physical Layer also notifies the upper layers that the Link is ready for operation, by setting the LinkUp variable. In addition, the idle_to_rlock_transitioned variable is cleared to 00h.

## _Exit to "Recovery State"_

The next state will be Recovery if a change in the Link speed or Link width is indicated, or if the Link partner initiates this by going to Recovery or Electrical Idle. Let's consider each of these three cases in a little more detail in the following discussion.

## **Speed Change**

Two conditions are described in the spec that will cause an automatic change in speed.

The first is when rates higher than 2.5 GT/s are supported by both partners and the Link is active (Data Link Layer reports DL_Active), or when one partner requests a speed change in its TS Ordered Sets. For example, a Downstream Port will initiate a speed change if a higher rate was noted and software writes the Retrain Link bit and after setting the Target Link Speed field (see Figure 14‐ 26 on page 569) to a different rate than the current rate.