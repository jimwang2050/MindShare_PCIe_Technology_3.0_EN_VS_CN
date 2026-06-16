- If a loopback‐capable Transmitter is directed by a higher Layer to send TS Ordered Sets with the Loopback bit asserted or all Lanes that are sending and receiving TS1s receive 2 consecutive TS1s with the Loop‐ back bit set. Whichever Port sends the TS1s with the bit set will become the Loopback master, while the Port that receives them will become the Loopback slave. 

## _Exit to “Detect State”_ 

- After a 24ms timeout if none of the other conditions are true. 

**557** 

**PCI Ex ress Technolo p gy** 

## **Configuration.Linkwidth.Accept** 

At this point, the Upstream Port is now sending back TS1 ordered‐sets on all its Lanes with the same Link number. The Link number originated from the Down‐ stream Port, and the Upstream Port is simply reflecting that value back on all its Lanes. Now the Downstream Port knows the Link width (number of Lanes receiving the same Link number) and it must start advertising the Lane num‐ bers. So the leader (Downstream Port) continues sending TS1s, but now with the actual Lane numbers designated instead of PAD. Also, all these TS1s will have the same Link number. The detailed behavior for the Downstream and Upstream Lanes are outlined below: 

## **Downstream Lanes** 

## _During Configuration.Linkwidth.Accept_ 

- The Downstream Port will now initiate Lane numbers. If a Link can be formed from at least one group of Lanes that all receive two consecutive TS1s and all see the same Link number, then TS1s are sent that keep that same Link number but now assign unique, non‐PAD Lane numbers as well. 

## _Exit to “Configuration.Lanenum.Wait”_ 

- The Downstream Port does not stay in the Configuration.Linkwidth.Accept substate very long. Once it has received the necessary TS1s from the Upstream Port indicating, the Link width, it updates any internal state info that is required, starts sending TS1s with non‐PAD Lane numbers, as indi‐ cated above, and immediately transitions to Configuration.Lanenum.Wait to await Lane Number confirmation from the Upstream Port. 

## **Upstream Lanes** 

## _During Configuration.Linkwidth.Accept_ 

- The Upstream Port transmits TS1s where one of the received Link numbers is selected and sent back in the TS1s on _all_ the Lanes that received TS1s with a non‐PAD Link number. Any left‐over Lanes that detected a Receiver but no Link number must send TS1s with Link and Lane numbers set to PAD. 

## _Exit to “Configuration.Lanenum.Wait”_ 

- The Upstream Port must respond to the Lane numbers proposed to it by the Link neighbor. If a Link can be formed using Lanes that sent a non‐PAD Link number on their TS1s and received two consecutive TS1s with the same Link number and any non‐PAD Lane number, then it should send TS1s that match the same Lane number assignments, if possible, or are dif‐ ferent if necessary (such as with the optional Lane reversal). 

**558** 

**Chapter 14: Link Initialization & Training** 

## **Configuration.Lanenum.Wait** 

Prior to discussing the Configuration.Lanenum.Wait state, some background information may be helpful. Lane numbers are assigned sequentially from zero to the maximum number possible for a Link. For example, a x8 Link will be assigned Lane numbers 0 ‐ 7. Ports are required to support a Link as wide as the number of Lanes they have and as small as one Lane. The Lanes will always start with Lane 0 and must be both sequential and contiguous. For example, if some Lanes on a x8 Port aren’t working, it might optionally be designed to con‐ figure a x4 Link and, if so, it would need to use Lanes 0‐3. As another example, if Lane 2 of a x8 Port is not working, it wouldn’t be possible to use Lanes 0, 1, 3, and 4 to form a x4 Link because the Lanes wouldn’t be contiguous. Any left‐ over Lanes must send TS1s with Link and Lane set to PAD. 

A common timing consideration is repeated many times in the spec for the Con‐ figuration substates. Rather than repeat it for every case here, just be aware that it applies in general to both Upstream and Downstream Ports: 

To avoid configuring a Link smaller than necessary, it’s recommended that a multi‐Lane Port delay the final link width evaluation if it sees an error or loses Block Alignment on some Lanes. For 8b/10b, it should wait at least two more TS1s, while for 128b/130b mode it should wait for at least 34 TS1s, but never more than 1ms in any case. The idea is that the Lanes might need settling time after powering up or being reset. 

## _Exit to “Detect State”_ 

After a 2ms timeout if no Link can be configured (e.g.: Lane 0 is not working and Lane Reversal isn’t available), or if all Lanes receive two consecutive TS1s with PAD in both the Link and Lane numbers, the link must exit to the Detect State. 

## **Downstream Lanes** 

## _During Configuration.Lanenum.Wait_ 

The Downstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met. 

## _Exit to “Configuration.Lanenum.Accept”_ 

If either of the cases listed below is true: 

- If two consecutive TS1s have been received on all Lanes with Link and Lane numbers that match what is being transmitted on those Lanes. 

**559** 

**PCI Ex ress Technolo p gy** 

- If any Lanes that detected a Receiver see two consecutive TS1s with a Lane number different from when the Lane first entered this substate and at least some Lanes see a non‐PAD Link number. The spec points out that this allows the two Ports to settle on a mutually acceptable Link width. 

## _Exit to “Detect State”_ 

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD. 

Upstream Lanes 

## _During Configuration.Lanenum.Wait_ 

The Upstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met. 

## _Exit to “Configuration.Lanenum.Accept”_ 

If either of the cases listed below is true: 

- If any Lanes receive two consecutive TS2s. 

- If any Lanes receive two consecutive TS1s with a Lane number different from when the Lane first entered this substate and at least some Lanes see a non‐PAD Link number. 

Note that Upstream Lanes are allowed to wait up to 1ms before changing to that substate, so as to prevent received errors or skew between Lanes from affecting the final Link configuration. 

## _Exit to “Detect State”_ 

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD. 

## **Configuration.Lanenum.Accept** 

Downstream Lanes 

## _During Configuration.Lanenum.Accept_ 

The Downstream Port has now received TS1s with non‐PAD Link and Lane numbers. It is at this point that the Downstream Port must decide if a Link can be established with the Lane numbers returned by the Upstream Port. The three possible state transitions are listed below. 

## _Exit to “Configuration.Complete”_ 

If two consecutive TS1s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being transmitted in the TS1s for all the Lanes, then Upstream Port has agreed with the Link and 

**560** 

**Chapter 14: Link Initialization & Training** 

Lane numbers advertised by the Downstream Port and the next substate is Configuration.Complete. Or if the Lane numbers in the received TS1s are reversed from what the Downstream Port advertised, if the Downstream Port supports Lane Reversal, it can still proceed to Configuration.Complete while using the reversed Lane numbers. 

The spec points out that the Reversed Lane condition is strictly defined as Lane 0 receiving TS1s with the highest Lane number (total number of Lanes ‐ 1) and the highest Lane number receiving TS1s with Lane number of zero. One thing that can be understood from this is the answer to a question that comes up in class sometimes: Can the Lane numbers be mixed up, rather than sequential? The answer is no, they must be from 0 to n‐1 or from n‐1 to 0; no other options are supported. 

If the Configuration state was entered from the Recovery state, a bandwidth change may have been requested. If so, status bits will be updated to report the nature of what happened. Basically, the system needs to report whether this change was initiated because the Link wasn’t working reliably or because hardware is simply managing the Link power. The bits are updated as follows: 

- If the bandwidth change was initiated by the Downstream Port because of a reliability problem, the Link Bandwidth Management Status bit is set to 1b. 

- If the bandwidth change was not initiated by the Downstream Port but the Autonomous Change bit in two consecutive received TS1s is cleared to 0b, the Link Bandwidth Management Status bit is set to 1b. 

- Otherwise the Link Autonomous Bandwidth Status bit is set to 1b. 

## _Exit to “Configuration.Lanenum.Wait”_ 

- If a configured Link can be formed with some but not all of the Lanes that receive two consecutive TS1s with the same non‐PAD Link and Lane num‐ bers, those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve a working Link. 

The new Lane numbers must start with zero and increase sequentially to cover the Lanes that will be used. Any Lanes that don’t receive TS1s can’t be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s with Link and Lane set to PAD. For example, if 8 Lanes are available, but Lane 2 doesn’t see incoming TS1s, then the Link can’t consist of a group that would need Lane 2. Consequently, the x8 and x4 options would not be available, and only a x1 or x2 Link is possible. 

**561** 

**PCI Ex ress Technolo p gy** 

## _Exit to “Detect State”_ 

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers. 

## **Upstream Lanes** 

## _During Configuration.Lanenum.Accept_ 

- The Upstream Port has now received either TS2s or TS1s with non‐PAD Link and Lane numbers. It is at this point that the Upstream Port must decide if a Link can be established with the Lane numbers sent by the Downstream Port. The three possible state transitions are listed below. 

## _Exit to “Configuration.Complete”_ 

- If two consecutive TS2s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being transmitted in the TS1s for those Lanes, all is well and the next substate will be Configura‐ tion.Complete. 

## _Exit to “Configuration.Lanenum.Wait”_ 

- If a configured Link can be formed with a subset of Lanes that receive two consecutive TS1s with the same non‐PAD Link and Lane numbers, those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve a working Link. The next substate in this case will be Configuration.Lanenum.Wait. 

As was the case for the Downstream Lanes, the new Lane numbers must start with zero and increase sequentially to cover the Lanes that will be used. Any Lanes that don’t receive TS1s can’t be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s with Link and Lane set to PAD. 

## _Exit to “Detect State”_ 

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers, then the next state will be Detect. 

## **Configuration.Complete** 

This is the only substate of the Configuration state where TS2s are exchanged. As discussed before, the purpose of TS2s is a handshake, or confirmation between the two devices on the link that they are ready to proceed to the next state. So this is the final confirmation of the Link and Lane numbers exchanged in the TS1s leading up to this point. 

**562** 

**Chapter 14: Link Initialization & Training** 
