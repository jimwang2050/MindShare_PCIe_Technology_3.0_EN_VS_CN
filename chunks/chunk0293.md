13. Since the transmitted and received Link and Lane numbers matched on Lanes 0 and 1, the Downstream Port indicates it is ready to conclude this negotiation and proceed to the next state, L0, by sending TS2 Ordered Sets with the same Link and Lane numbers on these Lanes. The other Lanes continue sending TS1s with PAD for both the Link and Lane numbers. 

14. Upon receiving TS2s with the same Link and Lane numbers on Lanes 0 and 1, the Upstream Port also indicates its readiness to leave the Con‐ figuration state and proceed to L0 by sending TS2s back on these Lanes. The other Lanes continue sending TS1s with PAD for both the Link and Lane numbers. This is shown in Figure 14‐23 on page 552. 

**551** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐23: Example 3 ‐ Steps 5 and 6_ 

**==> picture [356 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 5<br>TS1s<br>Lane # 0 1 PAD PAD<br>Link # N N PAD PAD<br>TS2s N N PAD PAD Link #<br>0 1 PAD PAD Lane #<br>0 1 2 3 Step 6<br>LTSSM<br>(Upstream Port)<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


Once a Port receives at least 8 TS2s and transmits at least 16, it sends some logical idle data and those Lanes transitions to L0. The other Lanes, Lanes 2 and 3 in this example, transition to Electrical Idle until the next time the link training process is initiated at which point those Lanes will attempt the training process like normal. 

## **Detailed Configuration Substates** 

A detailed explanation of each substate is presented here to cover all the sub‐ states of Configuration, as shown in Figure 14‐24 on page 553. The Configura‐ tion Substates should be easier to follow, given the Link Training examples discussed previously. 

**552** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐24: Configuration State Machine_ 

**==> picture [380 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from<br>Polling or Recovery Exit to<br>Directed Loopback<br>Config.Linkwidth.Start<br>Directed Exit to<br>Config.Linkwidth.Accept Disable<br>Exit to<br>Detect Config.Lanenum.Wait<br>Config.Lanenum.Accept<br>Config.Complete<br>2m s timeout &<br>2m s timeout, haven’t reached max<br>& max Recovery  attempts at Recovery. Exit to<br>attempts reached. Config.Idle<br>Recovery<br>8 Idle Rx, Tx 16 Idle<br>Exit to Full-On Power State<br>L0 Packet transmission/<br>reception begins<br>**----- End of picture text -----**<br>


## **Configuration.Linkwidth.Start** 

This substate is entered after either the normal completion of the Polling state (as described in “Polling.Configuration” on page 527), or if the Recovery state finds that Link or Lane numbers have changed since the last time they were assigned and thus the recovery process can’t finish normally (as described in the “Recovery State” on page 571). 

## **Downstream Lanes.** 

## _During Configuration.Linkwidth.Start_ 

The Downstream Port is now the leader on this Link and sends TS1s with a non‐PAD link number on all active Lanes (as long as LinkUp is 

**553** 

**PCI Ex ress Technolo p gy** 

not set and upconfiguration of the Link width is not taking place). In the TS1s, the Link number field is changed from PAD to a number while the Lane number remains PAD. The only constraint on the value of the Link numbers in the spec is that they must be unique for each possible Link if multiple Links are supported. For example, a x8 Link would have the same Link number on all 8 Lanes, but if it could also be configured as two x4 Links, both groups of 4 Lanes would be assigned different Link numbers, such as 5 for one group and 6 for the other. The values are local to the Link partners and there’s no need for software to track them or try to make them unique throughout the system. If the upconfigure_capable bit is set to 1b, these TS1s will also be sent on any inactive Lanes that received two consecutive TS1s with Link and Lane numbers set to PAD. 

- When entering this substate from Polling, any Lane that detected a Receiver is considered active. 

- When entering from Recovery, any Lane that was part of the Link after going through Configuration.Complete is considered an active Lane. 

- All supported data rates must be advertised in the TS1s, even if the Port doesn’t intend to use them. 

**Crosslinks.** For cases where LinkUp = 0b and the optional crosslink capa‐ bility is supported, all Lanes that detected a Receiver must send a minimum of 16 to 32 TS1s with a non‐PAD Link number and PAD Lane number. After that, the port will evaluate what it is receiving to see if a crosslink is present. 

**Upconfiguring the Link Width.** If LinkUp = 1b and the LTSSM wants to upconfigure the Link, TS1s with Link and Lane numbers set to PAD are sent on the currently active Lanes, the inactive Lanes it intends to activate, and the Lanes that have seen incoming TS1s. When the Lanes have received two consecutive TS1s coming back, or after 1ms, the Link number is assigned a value in the TS1s being sent. 

- If activating an inactive Lane, the Transmitter must wait for the Tx com‐ mon mode voltage to settle before exiting Electrical Idle and sending TS1s. 

- Link numbers must be the same for Lanes that will be grouped into a Link. The numbers can only be different for groups of Lanes that are capable of acting as a unique Link. 

- _Exit to “After a 24ms timeout if none of the other conditions are true.”_ Any Lanes that previously received at least one TS1 with Link and Lane 

**554** 

**Chapter 14: Link Initialization & Training** 

number of PAD now receive two consecutive TS1s with a non‐PAD Link number that matches a transmitted Link number and Lane num‐ bers are still PAD will exit to the Configuration.Linkwidth.Accept sub‐ state. 

## _Exit to “Configuration.Linkwidth.Start”_ 

- If the first set of received TS1s for this substate have a non‐PAD Link number then it’s understood that a crosslink is present and the Link neighbor is also behaving as a Downstream Port. To handle this situa‐ tion, the Downstream Lanes are changed to Upstream Lanes and a ran‐ dom crosslink timeout is chosen. The next substate will be the same Confiuration.Linkwidth.Start again but the Lanes will now behave as Upstream Lanes. 

This supports the optional behavior when both Link partners behave as Downstream Ports. The solution for this situation is to change both to Upstream Ports and assign each a random timeout that, when it expires, changes it to a Downstream Port. Since the timeouts won’t be the same, eventually one Port is seen as Downstream while the other is seen as Upstream and then the training can go forward. The timeout must be random so that even if two of the same devices are connected any possible deadlock will eventually be broken. 

If crosslinks are supported, receiving a sequence of TS1s that first have a Link number of PAD and later have a non‐PAD Link number that matches the transmitted Link number is valid only if the sequence wasn’t interrupted by a TS2. 

## _Exit to “Disable State”_ 

If the Port is instructed by a higher layer to send TS1s or TS2s with the Disable Link bit asserted on all detected Lanes. Normally, the Down‐ stream Port will initiate this but, for the optional crosslink case, it could become an Upstream Port instead and then Disabled will be the next state if 2 consecutive TS1s are received with the Loopback bit set. 

## _Exit to “Loopback State”_ 

If the loopback‐capable Transmitter is instructed by a higher layer to send TS Ordered Sets with the Loopback bit asserted, or if Lanes that are sending TS1s receive 2 consecutive TS1s with the Loopback bit set. Whichever Port sends the TS1s with the bit set will become the Loop‐ back master, while the Port that receives them will become the Loop‐ back slave. 

**555** 

**PCI Ex ress Technolo p gy** 

## _Exit to “Detect State”_ 

After a 24ms timeout if none of the other conditions are true. 

## **Upstream Lanes.** 

## _During Configuration.Linkwidth.Start_ 

The Upstream Port is now the follower on this Link and goes back to sending TS1 ordered‐sets with PAD set for the Link and Lane number fields. It will continue to do this until it begins receiving TS1s with a non‐PAD Link number from the Downstream Port (leader). 

The Upstream Port sends TS1s with Link and Lane values of PAD on a) all active Lanes, b) the Lanes it wants to upconfigure and, c) if upconfigure_capable is set to 1b, on each of the inactive Lanes that have received two consecutive TS1s with Link and Lane numbers set to PAD while in this substate. 

- When entering this substate from Polling, any Lane that detected a Receiver is considered active. 

- When entering from Recovery, any Lane that was part of the Link after going through Configuration.Complete is considered an active Lane. If the transition wasn’t caused by an LTSSM timeout, the Trans‐ mitter must set the Autonomous Change bit (Symbol 4, bit 6) to 1b in the TS1s being sent in the Configuration state if it does, in fact, plan to change the Link width for autonomous reasons. 

- All supported data rates must be advertised in the TS1s, even if the Port doesn’t intend to use them. 

**Crosslinks.** For cases where LinkUp = 0b and the optional crosslink capa‐ bility is supported, all Lanes that detected a Receiver must send a minimum of 16 to 32 TS1s with Link and Lane values of PAD. After that, the port will evaluate what it is receiving to see if a crosslink is present. 

_Exit to “After a 24ms timeout if none of the other conditions are true.”_ 

- If _any_ Lanes receive two consecutive TS1s with non‐PAD Link number and PAD Lane number, this port transitions to the Configuration.Link‐ width.Accept substate where one of the received Link numbers is selected for those Lanes and TS1s are sent back with that Link number and a PAD Lane number, on _all_ the Lanes that received TS1s with a non‐ PAD Link number. Any left‐over Lanes that detected a Receiver but no Link number must send TS1s with Link and Lane numbers set to PAD. 

- If upconfiguring the Link, the LTSSM waits until it receives two con‐ secutive TS1s with a non‐PAD Link number and PAD Lane number on either a) all the inactive Lanes it wants to activate, or b) on any 

**556** 

**Chapter 14: Link Initialization & Training** 

Lane 1ms after entering this substate, whichever is earlier. After that, it sends TS1s with the selected Link number along with PAD Lane numbers. 

- To avoid configuring a Link smaller than necessary, it’s recom‐ mended that a multi‐Lane Link that sees an error or loses Block Alignment on some Lanes delay this Receiver evaluation. For 8b/10b encoding, it should wait at least two more TS1s, while for 128b/130b encoding it should wait for at least 34 TS1s, but never more than 1ms in any case. 

- After activating an inactive Lane, the Transmitter must wait for the Tx common mode voltage to settle before exiting Electrical Idle and sending TS1s. 

## _Exit to “Configuration.Linkwidth.Start”_ 

- After a crosslink timeout, send 16 to 32 TS2s with Link and Lane values of PAD. The Upstream Lanes change to Downstream Lanes and the next substate will be the same Confiuration.Linkwidth.Start again but this time the Lanes behave as Downstream Lanes. For the case of two Upstream Ports connected together, this optional behavior allows one of them to eventually take the lead as a Downstream Port. 

## _Exit to “Disable State”_ 

If either of the following is true: 

- Any Lanes that are sending TS1s also receive TS1s with the Disable Link bit asserted. 

- The optional crosslink is supported and either all Lanes that are sending and receiving TS1s receive the Disable Link bit in two con‐ secutive TS1s, or else a crosslink Port is directed by a higher Layer to assert the Disable bit in its TS1s and TS2s on all Lanes that detected a Receiver. 

## _Exit to “Loopback State”_ 
