# 📘 第 13 章　物理层 - 电气 (Chapter 13. Physical Layer - Electrical)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0293.md` ... `chunks/chunk0297.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Physical Layer - Electrical](#-本章目录-table-of-contents)

<a id="sec-13-1"></a>
## 13.1 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-13-2"></a>
## 13.2 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-13-3"></a>
## 13.3 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

It should be noted that Devices are allowed to change their supported data rates and upconfigure capability when they enter this substate, but not while in it. This is because Devices record the capabilities of their Link partner from what is advertised in these TS2s, as will be described in this section. 

## **Downstream Lanes** 

## _During Configuration.Complete_ 

TS2s are sent using the Link and Lane numbers that match the received TS1s. The TS2s can have the Upconfigure Capability bit set if the Port sup‐ ports a x1 Link using Lane 0 and is able to up‐configure the Link. 

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity. 

The Downstream Port is transmitting TS2s and watching for TS2s coming back. For future reference, record the number of FTSs that must be sent when exiting from the L0s state from the N_FTS field in the incoming TS2s. 

## _Exit to “Configuration.Idle”_ 

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching rate identifiers, and matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2. 

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane and this overrides any previ‐ ously recorded value. The variable used to track speed changes in Recovery, “changed_speed_recovery”, is cleared to zero. 

The variable “upconfigure_capable” is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8 consecutive TS2s with the same bit set. Otherwise it’s cleared to zero. 

Any Lanes that aren’t configured as part of the Link are no longer associ‐ ated with the LTSSM in progress and must either be: 

- Associated with a new LTSSM or 

- Transitioned to Electrical Idle 

   - a)   A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b 

**563** 

**PCI Ex ress Technolo p gy** 

since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it’s also recom‐ mended that those Lanes leave their Receiver terminations on because they’ll become part of the Link again if it is upconfigured. If the terminations aren’t left on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete. Lanes that weren’t part of the Link before can’t become part of it through this process, though. 

- b)  For the optional crosslink, Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG. 

- c) If the LTSSM goes back to Detect, these Lanes will once again be associated with it. 

- d)  No EIOS is needed before Lanes go to Electrical Idle, and the transi‐ tion doesn’t have to happen on Symbol or Ordered Set boundaries. 

## After a 2ms timeout: 

_Exit to “Configuration.Idle”_ 

Next state is Configuration.Idle if the idle_to_rlock_transitioned vari‐ able is less than FFh **and** the current data rate is 8.0 GT/s. 

In this transition, the “changed_speed_recovery” variable is cleared to zero. Also, the “upconfigure_capable” variable may be updated, though it’s not required to do so, if at least one Lane saw eight consecu‐ tive TS2s with matching Link and Lane numbers (non‐PAD). If the transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero. 

Lanes that aren’t part of the configured Link aren’t associated with the LTSSM in progress and have the same requirements as the non‐timeout case listed above. 

_Exit to “Detect State”_ 

Otherwise, the next state is Detect. 

## **Upstream Lanes** 

_During Configuration.Complete_ 

TS2s are sent using the Link and Lane numbers that match the received TS2s. The TS2s can have the Upconfigure Capability bit set if the Port sup‐ ports a x1 Link using Lane 0 and is able to up‐configure the Link. 

**564** 

**Chapter 14: Link Initialization & Training** 

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity. 

In this substate, the Upstream Port is receiving TS2s from the Downstream Port, and for future reference, should record the N_FTS field value number of FTSs that must be sent when exiting from the L0s state from the in the incoming TS2s. 

## _Exit to “Configuration.Idle”_ 

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching rate identifiers, and a matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2. 

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane, overriding any previously recorded value. The variable used to track speed changes in Recovery, “changed_speed_recovery”, is cleared to zero. 

The variable “upconfigure_capable” is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8 consecutive TS2s with the same bit set. Otherwise it’s cleared to zero. 

Any Lanes that aren’t configured as part of the Link are no longer associ‐ ated with the LTSSM in progress and must either be: 

- Optionally associated with a new crosslink LTSSM (if this feature is sup‐ ported), or 

- Transitioned to Electrical Idle 

   - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it’s also recommended that those Lanes leave their Receiver terminations on because they’ll become part of the Link again if it is upconfigured. If they’re not left on, they must be turned on from when the LTSSM enters the Recov‐ ery.RcvrCfg state all the way through Configuration.Complete. Lanes that weren’t part of the Link before can’t become part of it through this process, though. 

**565** 

**PCI Ex ress Technolo p gy** 

- b)  Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐ 

   - HIGH‐IMP‐DC‐NEG[.] 

- c)    If the LTSSM goes back to Detect, these Lanes will once again be asso‐ ciated with it. 

- d)  No EIOS is needed before Lanes go to Electrical Idle, and the transi‐ tion doesn’t have to happen on Symbol or Ordered Set boundaries. 

After a 2ms timeout: 

## _Exit to “Configuration.Idle”_ 

Next state is Configuration.Idle if the idle_to_rlock_transitioned vari‐ able is less than FFh **and** the current data rate is 8.0 GT/s. 

In this transition, the “changed_speed_recovery” variable is cleared to zero. Also, the “upconfigure_capable” variable may be updated, though it’s not required to do so, if at least one Lane saw eight consecu‐ tive TS2s with matching Link and Lane numbers (non‐PAD). If the transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero. 

Lanes that aren’t part of the configured Link aren’t associated with the LTSSM in progress and have the same requirements as the non‐timeout case listed above. 

## _Exit to “Detect State”_ 

Otherwise, the next state is Detect. 

## **Configuration.Idle** 

## _During Configuration.Idle_ 

In this substate, the transmitter is sending Idle data and waiting for the minimum number of received Idle data so this Link can transition to L0. During this time, the Physical Layer reports to the upper layers that the link is operational (Linkup = 1b). 

For 8b/10b encoding, the transmitter is sending Idle data on all configured Lanes. Idle data are just data zeros that get scrambled and encoded. 

For 128b/130b encoding, the transmitter sends one SDS Ordered Set on all configured Lanes followed by Idle data Symbols. The first Idle Symbol on Lane 0 is the first Symbol of the Data Stream. 

**566** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “L0 State”_ 

If using 8b/10b encoding, the next state is L0 if 8 consecutive Idle data sym‐ bol times are received on all configured Lanes, and 16 symbol times of idle data were sent after receiving one Idle Symbol. 

If using 128b/130b, the next state is L0 if 8 consecutive Idle data are received on all configured Lanes, 16 Idles were sent after receiving one Idle Symbol, and this state wasn’t entered by a timeout from Configuration.Complete. 

- Lane‐to‐Lane de‐skew must be completed before Data Stream processing begins. 

- The Idle Symbols must be received in Data Blocks. 

- If software set the Retrain Link bit in the Link Control register since the last transition to L0 from Recovery or Configuration, the Downstream Port must set the Link Bandwidth Management bit in the Link Status reg‐ ister to 1b to indicate that this change was not hardware initiated (auton‐ omous). 

- The “idle_to_rlock_transitioned” variable is cleared to 00h on transition to L0. 

## After a 2ms timeout: 

## _Exit to “Detailed Recovery Substates”_ 

If the idle_to_rlock_transitioned variable is less than FFh, the next state is Recovery (Recovery.RcvrLock). Then: 

- a) For 8.0 GT/s, increment idle_to_rlock_transitioned by 1. 

- b)  For 2.5 or 5.0 GT/s, set idle_to_rlock_transitioned to FFh. 

- c) NOTE: This variable counts the number of times the LTSSM has tran‐ sitioned from this state to the Recovery state because the sequence isn’t working. The problem may be that equalization hasn’t been properly adjusted or that the selected speed just isn’t going to work, and the Recovery state will take steps to address these issues. This variable limits the number of these attempts so as to avoid an endless loop. If the Link still isn’t working after doing this 256 times (when the count reaches FFh), go back to Detect and start over, hoping for a better result. 

_Exit to “Detect State”_ 

Otherwise (meaning idle_to_rlock = FFh), the next state is Detect. 

**567** 

**PCI Ex ress Technolo p gy** 

## **L0 State** 

This is the normal, fully‐operational Link state, during which Logical Idle, TLPs and DLLPs are exchanged between Link neighbors. L0 is achieved immediately following the conclusion of the Link Training process. The Physical Layer also notifies the upper layers that the Link is ready for operation, by setting the LinkUp variable. In addition, the idle_to_rlock_transitioned variable is cleared to 00h. 

## _Exit to “Recovery State”_ 

The next state will be Recovery if a change in the Link speed or Link width is indicated, or if the Link partner initiates this by going to Recovery or Electrical Idle. Let’s consider each of these three cases in a little more detail in the following discussion. 

## **Speed Change** 

Two conditions are described in the spec that will cause an automatic change in speed. 

The first is when rates higher than 2.5 GT/s are supported by both partners and the Link is active (Data Link Layer reports DL_Active), or when one partner requests a speed change in its TS Ordered Sets. For example, a Downstream Port will initiate a speed change if a higher rate was noted and software writes the Retrain Link bit and after setting the Target Link Speed field (see Figure 14‐ 26 on page 569) to a different rate than the current rate.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-13-4"></a>
## 13.4 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The second condition is when both partners support 8.0 GT/s and one of them wants to perform Tx Equalization. In both conditions the directed_speed_change variable will be set to 1b and the changed_speed_recovery bit will be cleared to 0b. 

A Port will not attempt a speed change (the directed_speed_change variable won’t be set) if a rate higher than 2.5 GT/s has never been seen as advertised by the other Port in the Configuration.Complete or Recovery.RcvrCfg substates. 

**568** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐25: Link Control Register_ 

**==> picture [280 x 235] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


## _Figure 14‐26: Link Control 2 Register_ 

**==> picture [306 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


**569** 

**PCI Ex ress Technolo p gy** 

## **Link Width Change** 

An upper layer would normally only direct a Link width reduction if upconfigure_capable has been set to 1b because otherwise the Link won’t be able to go back to the original width. If the Hardware Autonomous Width Dis‐ able bit is set to 1b a Port can only reduce the width in an effort to correct a reli‐ ability problem. An upper layer can only initiate an increase in Link width if the Link partner advertised that it was upconfigure capable and the Link is not already at its maximum width. Apart from these guidelines, the decision crite‐ ria for changing the Link width are not given in the spec and are therefore implementation specific. 

## **Link Partner Initiated** 

The spec describes three possibilities for this case. 

First, if Electrical Idle is detected or inferred (see Table 14‐10 on page 596) on all Lanes without first receiving an EIOS on any Lane, the Port may choose to enter Recovery or stay in L0. If errors result from this condition, the Port may be directed to Recovery by means such as setting the Retrain Link bit. 

The second case happens when TS1s or TS2s are received (or an EIEOS for 128b/ 130b) on any configured Lanes, indicating that the Link partner has already entered Recovery. Since both of these cases are initiated by the Link partner, the Transmitter is allowed to complete any TLP or DLLP currently in progress. 

Finally, if an EIOS is received on any Lane, indicating a Link power manage‐ ment change, but the Receiver doesn’t support L0s and hasn’t been directed to L1 or L2, then going to Recovery is the only option. 

## _Exit to “L0s State”_ 

The next state will be L0s for a Transmitter that’s been instructed to initiate it, or for a Receiver that sees an EIOS. Interestingly, the LTSSM states for the Transmitter and Receiver of the Port can be different now, because one can be in L0s while the other is still in L0. 

- Transmitters go to L0s when directed, if they implement L0s, and send EIOS to initiate the change. 

- Receivers go to L0s when an EIOS is seen on any Lane. However, if the Receiver doesn’t implement L0s and hasn’t been directed to L1 or L2, this will be seen as a problem and the next state will be “Recovery State” instead. 

**570** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Rx_L0s.Entry”_ 

- The next state will be L1 when one Link partner is directed to initiate this and sends one EIOS on all Lanes (two EIOSs if the speed is 5.0 GT/s) and receives an EIOS on any Lane. Note that both Link partners must have already agreed to enter L1 beforehand and that a Data Link Layer hand‐ shake is needed to ensure that both are ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. 

## _Exit to “L2 State”_ 

The next state will be L2 when one Link partner is directed to initiate this and sends one EIOS on all Lanes (two EIOSs if the speed is 5.0 GT/s) and receives an EIOS on any Lane. Note that both Link partners must have already agreed to enter L2 beforehand and that a handshake is needed to ensure that both are ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on page 733. 

## **Recovery State** 

If everything works as expected, the Link trains to the L0 state without ever going into the Recovery state. But we’ve already discussed two reasons why it might not. First, if the correct Symbol pattern isn’t seen in Configuration.Idle, the LTSSM goes to Recovery in an effort to correct signaling problems by, for example, adjusting equalization values. Secondly, once L0 is reached with a data rate of 2.5 GT/s and both devices support higher speeds, the LTSSM goes to Recovery and attempts to change the Link speed to the highest commonly‐sup‐ ported/advertised speed. In this state, Bit Lock and either Symbol Lock or Block Alignment is re‐acquired and the Link is de‐skewed again. The Link and Lane Numbers should remain unchanged unless the Link width is being changed. In that case, the LTSSM passes through the Configuration state where Link width is re‐negotiated. 

NOTE: To simplify the discussion and avoid repeating the same text many times, the term “Lock” will be used here to mean the combination of Bit Lock and either Symbol Lock for 8b/10b encoding or Block Alignment for 128b/130b encoding. A Receiver must acquire this Lock to be able to recognize Symbols, Ordered Sets and Packets. 

**571** 

**PCI Ex ress Technolo p gy** 

## **Reasons for Entering Recovery State** 

- Exiting the L1 state; Required because there is no fast training option (like sending FTS ordered sets) when exiting L1 

- Exiting L0s if the receiver fails to achieve Lock from the FTS ordered sets in the required time, the Link must transition to Recovery 

- From L0 if: 

- A higher data rate is available when initial training completes. 

- A Link speed or width change has been requested (for power management or because the current speed or width is unreliable). 

- Software sets the Retrain Link bit in the Link Control Register (see Figure 14‐71 on page 644) in an effort to clear transmission problems. 

- An error condition such as a Replay Num Roll‐over event associated with the Ack/Nak protocol of the Data Link Layer automatically causes the Physical Layer logic to retrain the Link. 

- Receiver sees TS1s or TS2s on any configured Lane, meaning that the neighbor must have entered Recovery. 

- Receiver sees Electrical Idle on all configured Lanes but did not first receive the Electrical Idle Ordered Set. 

## **Initiating the Recovery Process** 

Either Port can initiate Recovery by sending TS1s to its neighbor. When a Port sees incoming TS1s it knows that the other Port has entered Recovery, so it also goes into Recovery and returns TS1s. Both receivers first use the TS1s to reac‐ quire Lock (if necessary) and then proceed to the other substates as needed. This is shown in Figure 14‐27 on page 573. A detailed description of what hap‐ pens in the substates is provided in the sections that follow. 

**572** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐27: Recovery State Machine_ 

**==> picture [343 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from Recovery.Speed Exit to Exit to<br>L1, L0, L0s Loopback Configuration<br>Recovery.Equalization<br>Recovery.RcvrLock Recovery.Idle Exit to<br>(bit/sym bol re-lock) Recovery.RcvrCfg (Send idle data) Disabled<br>Exit to Hot<br>Exit to Exit to Reset<br>Configuration Detect<br>Exit to L0<br>**----- End of picture text -----**<br>


## **Detailed Recovery Substates** 

## _During Recovery.RcvrLock_ 

- Regardless of the speed, Transmitters send TS1s on all configured Lanes using the same Link and Lane numbers that were set in the Configuration state. If the purpose of entering the Recovery state was to change speeds, the speed_change bit in the Data Rate Identifier Symbol will be set to 1b in the TS1s from the initiating device and the internal variable directed_speed_change is set to 1b. This same variable will be set in the other device if the speed_change bit is set in the incoming TS1s. In addition, The successful_speed_negotiation variable is cleared to 0b on entry to this substate. 

In this substate, an Upstream Port is allowed to specify the de‐emphasis level the Downstream Port should use when operating at 5GT/s. This is accomplished by setting the Selectable De‐emphasis bit in its TS1s to the desired value. It’s possible that bit errors on the Link will prevent this infor‐ mation from reaching the Downstream Port, so the Upstream Port is allowed to request the de‐emphasis level again when going to the Recovery state for a speed change. If the Downstream Port plans to use the requested level, it must record the value of the Selectable De‐emphasis bit while in this state. 

**573** 

**PCI Ex ress Technolo p gy** 

A new transmitter voltage can also be applied upon entry to this state. The Transmit Margin field in the Link Control 2 register is sampled on entry to this substate and remains in effect until a new value is sampled on another entry to this substate from L0, L0s, or L1. 

A Downstream Port that wants to change the rate to 8.0 GT/s and redo the equalization must send EQ TS1s with the speed_change bit set and adver‐ tising the 8.0 GT/s rate. If an Upstream Port receives 8 consecutive EQ TS1s or EQ TS2s with the speed_change bit set to 1b and the 8.0 GT/s rate sup‐ ported, it is expected to advertise the 8.0 GT/s rate, too, unless it has con‐ cluded that there are reliability problems at that rate that can’t be fixed with equalization. Note that a Port is allowed to change its advertised data rates when entering this state, but only those rates that can be supported reliably. And apart from the conditions described here, a device is not allowed to change its supported data rates in this substate or in Recovery.RcvrCfg or Recovery.Equalization. 

## _Exit to “Recovery.RcvrCfg”_ 

- The next state will be Recovery.RcvrCfg if 8 consecutive TS1s or TS2s are received whose Link and Lane numbers match what is being sent _and_ their speed_change bit is equal to the directed_speed_change variable _and_ their EC field is 00b (if the current data rate is 8.0 GT/s). 

- If the Extended Synch bit is set, a minimum of 1024 TS1s in a row must be sent before going to Recovery.RcvrCfg. 

- If this substate was entered from Recovery.Equalization, the Upstream Port must compare the equalization coefficients or preset received by all Lanes against the final set of coefficients or preset that was accepted in Phase 2 of the equalization process. If they don’t match, it sets the Request Equalization bit in the TS2s it sends. 

## _Exit to “Recovery.Equalization”_ 

When the data rate is 8.0 GT/s, the Lanes must establish the proper equal‐ ization parameters to obtain good signal integrity. This section does not apply for lower speeds. Just because the Link is running at 8.0 GT/s, it does not go through the Recovery.Equalization substate every time Recovery is entered. Recovery.Equalization is only entered if one of these conditions is met: 

- If the start_equalization_w_preset variable is set to 1b then:

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-13-5"></a>
## 13.5 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- a) Upstream Port registered preset values from the 8 consecutive TS2s it saw prior to changing to 8.0 GT/s. It must use the Transmitter presets and it may optionally use the Receiver presets it received. 

**574** 

**Chapter 14: Link Initialization & Training** 

   - b) Downstream Port must use the Transmitter presets defined in its Lane Equalization Control register as soon as it changes to 8.0 GT/s and it may optionally use the Receiver presets found there. 

- Else (the variable is not set), Transmitters must use the coefficient settings they agreed to when the equalization process was last executed. 

   - a) Upstream Port’s next state will be Recovery.Equalization if 8 consecu‐ tive incoming TS1s have Link and Lane numbers that match those being sent and the speed_change bit is 0b, but the EC bits are non‐ zero, indicating that the Downstream Port wishes to redo some parts of the equalization process. The spec notes that a Downstream Port could do this under software or implementation‐specific direction. As always, the time it takes to do this must not be allowed to cause transaction timeout errors, which really means the Downstream Port would need to ensure there were no transactions in flight before tak‐ ing this step. 

   - a) Downstream Port’s next state will be Recovery.Equalization if directed, as long as this state wasn’t entered from Configuration.Idle or Recovery.Idle. The spec points out that no more than two TS1s whose EC=00b should be sent before sending TS1s with a non‐zero EC value to request that equalization be redone. 

Otherwise, after a 24ms timeout: 

## _Exit to “Recovery.RcvrCfg”_ 

The next state will be Recovery.RcvrCfg if both: 

- 8 consecutive TS1s or TS2s are received whose Link and Lane num‐ bers match what it being sent and their speed_change bit is equal to 1b. 

- And either the current data rate is already higher than 2.5 GT/s, or at least a higher rate is shown to be supported in the TS1s or TS2s. 

## _Exit to “Recovery.Speed”_ 

The next state will be Recovery.Speed if other of the two following condi‐ tions are met: 

- If the current speed is set higher than 2.5 GT/s but isn’t working since entering Recovery (indicated by clearing the variable changed_speed_recovery to 0b). The new rate after leaving Recov‐ ery.Speed will drop back to 2.5 GT/s. 

- If the changed_speed_recovery variable is set to 1b, indicating that a higher rate than 2.5 GT/s is already working but the Link was unable to operate at a new negotiated rate. As a result, the operating speed will revert to what it was when Recovery was entered from L0 or L1. 

**575** 

**PCI Ex ress Technolo p gy** 

## _Exit to “Configuration State”_ 

Otherwise, the LTSSM will return to Configuration if a speed change is not requested (directed_speed_change variable = 0b and the speed_change bit in the TS1s and TS2s is 0b), or if the highest commonly supported data rate is 2.5 GT/s. 

## _Exit to “Detect State”_ 

Finally, if none of the other conditions are true, the next state will be Detect. 

## **Speed Change Example** 

The spec includes an example of a speed change in the discussion of this sub‐ state. The scenario is two Link neighbors (device A and device B) that are com‐ ing out of reset, both of which support the 5.0 GT/s and 8.0 GT/s rates. 

To begin with, the Link will automatically train to L0 using the Gen1 rate of 2.5 GT/s. (This behavior is likely to continue in future spec versions because it pro‐ vides backward compatibility with older designs.) 

In our example both devices support higher rates and this is indicated by the Rate Identifier field in their TS Ordered Sets during training. Both devices note that the other supports a higher rate and one of them (device A) will be the first to set its directed_speed_change variable to 1b. When that happens, it will go to Recovery.RcvrLock and send TS1s with the speed_change bit set. If the desired rate will be 8.0 GT/s and hasn’t been before, the devices will exchange EQ TS1s to deliver the TX equalizer presets to be used instead of sending ordinary TS1s. 

Device B sees incoming TS1s and also transitions to Recovery.RcvrLock. When it recognizes 8 TS1s in a row with the speed_change bit set, it responds by set‐ ting the speed_change bit in its own TS1s and goes to Recovery.Speed. Device A waits for that response and, when 8 TS1s in a row with the speed_change bit have been seen, it goes to Recovery.RcvrCfg and then to Recovery.Speed. In that substate, the transmitters are put into Electrical Idle, the speed is changed to the highest commonly‐supported rate, and the directed_speed_change variable is cleared. 

After a timeout period, both devices transition back to Recovery.RcvrLock and the transmitters are re‐activated using the new speed (8.0 GT/s in this case). They send TS1s again now, this time with the speed_change bit cleared to 0b. If the new speed works well, they transition to Recovery.RcvrCfg and back to L0. However, if device B has a problem, such as failure to achieve Bit Lock, it will timeout in this substate and go back to Recovery.Speed. Device A may have 

**576** 

**Chapter 14: Link Initialization & Training** 

already transitioned to Recovery.RcvrCfg by this time, but when it sees Electri‐ cal Idle now, indicating the neighbor has returned to Recovery.Speed, it will also go back to that state. Returning to Recovery.Speed causes both devices to revert to the speed in use when Recovery was entered, 2.5 GT/s in this case, and return to Recovery.RcvrLock. 

In response to that development, Device A might set directed_speed_change again and try the process a second time. If it failed again, device A might choose to remove the 8.0 GT/s rate from its advertised list and try the speed change again without it. Since the highest common rate is now 5.0 GT/s, if this attempt succeeds the rate will end up at 5.0 GT/s. If it doesn’t work, Device A might give up trying to use a higher rate. How and when a device chooses to change its advertised rates or give up trying to get a higher rate working is not given in the spec and will be implementation specific. 

## **Link Equalization Overview** 

This section provides an overview of the Equalization Process and prepares the reader to understand the detailed substate machine behaviors if they are of interest. 

Using a higher Link speed results in more signal distortion than lower data rates. To compensate for this and minimize the effort and cost for system designers, the 3.0 spec adds a requirement for Transmitter Equalization. Unlike the fixed de‐emphasis values for the lower rates, which is really a simple form of Transmitter equalization itself, the new method uses an active handshake process to match the Transmitters to the actual signaling environment. During this process, each Receiver Lane evaluates the quality of the incoming signal and suggests Tx equalization parameters that the Link partner should use to meet the signal quality requirements. 

The Link Equalization procedure executes after the first change to the 8.0 GT/s data rate. The spec strongly recommends that the equalization process be initi‐ ated autonomously (automatically in hardware) but doesn’t require it. If a com‐ ponent chooses not to use the autonomous mechanism then a software‐based mechanism must be used. If either port is unable to achieve the necessary signal quality through this process, the LTSSM will conclude that the rate is not work‐ ing and will go back to Recovery.Speed to request a lower speed. 

The process involves up to four phases, as described in the text that follows. Once the speed has been changed to 8.0 GT/s, the current equalization phase in use is indicated by the EC (Equalization Control) field in the TS1s being, as shown in Figure 14‐28. 

**577** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐28: EC Field in TS1s and TS2s for 8.0 GT/s_ 

**==> picture [293 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>7 6 5 4 3 2 1 0<br>0<br>Tx Preset EC<br>1 Link #<br>2 Lane # Use Preset Reset EIEOS<br>Interval Count<br>3 # FTS<br>Symbol 7<br>4 Rate ID<br>7 6 5 4 3 2 1 0<br>5 Train Ctl FS value when EC = 01b,<br>Rsvd<br>6 Otherwise Pre-Cursor Coefficient<br>EQ Info<br>Symbol 8<br>9<br>7 6 5 4 3 2 1 0<br>10<br>LF value when EC = 01b,<br>Rsvd<br>TS ID Otherwise Cursor Coefficient<br>13 Symbol 9<br>7 6 5 4 3 2 1 0<br>14<br>TS ID<br>15 P [RCV] Post-Cursor Coefficient<br>**----- End of picture text -----**<br>


## **Phase 0** 

When the Downstream Port is ready to change from a lower rate to the 8.0 GT/s rate, it enters the Recovery.RcvrCfg sub‐state and sends Tx Presets and Rx Hints to the Upstream Port using EQ TS2s as described in “TS1 and TS2 Ordered Sets” on page 510. (Note that this phase is skipped if the Link is already running at 8.0 GT/s.) The Downstream Port (DSP) sends Tx Preset values based on the con‐ tents of its Equalization Control register shown in Figure 14‐29 on page 579. One thing this highlights is that there can be different equalization values for each Lane. The Downstream Port will use the DSP values for its own Transmit‐ ter and optionally for its Receiver, and send the USP values to the Upstream Port for it to use when going to the higher speed. 

**578** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐29: Equalization Control Registers_ 

**==> picture [275 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 Link Control 3 Register 2  1  0<br>RsvdP<br>31 Lane Error Status Register 0<br>Equalization Control Registers<br>31 16  15 0<br>Lane (1) Control Lane (0) Control<br>Lane (3) Control Lane (2) Control<br>Lane (n) Control Lane (n-1) Control<br>Control Register Contents<br>15  14 12  11 8  7  6 4  3 0<br>USP USP DSP DSP<br>R R<br>Rx Hint Tx Preset Rx Hint Tx Preset<br>USP = UpStream Port   DSP = DownStream Port<br>**----- End of picture text -----**<br>


_Table 14‐8: Tx Preset Encodings_ 

|**Encoding**|**De‐emphasis**|**Preshoot**|
|---|---|---|
|0000b|‐6|0|
|0001b|‐3.5|0|
|0010b|‐4.5|0|
|0011b|‐2.5|0|
|0100|0|0|



**579** 

## **PCI Ex ress Technolo p gy** 

_Table 14‐8: Tx Preset Encodings (Continued)_ 

|**Encoding**|**De‐emphasis**|**Preshoot**|
|---|---|---|
|0101|0|2|
|0110|0|2.5|
|0111|‐6|3.5|
|1000|‐3.5|3.5|
|1001|0|3.5|
|1010|Depends on FS<br>and LS values|Depends<br>on FS and<br>LS values|
|1011b to<br>1111b|Reserved|Reserved|



_Table 14‐9: Rx Preset Hint Encodings_ 

|**Encoding**|**Rx Preset Hint**|
|---|---|
|000b|‐6 dB|
|001b|‐7 dB|
|010b|‐8 dB|
|011b|‐9 dB|
|100|‐10 dB|
|101|‐11 dB|
|110|‐12 dB|
|111|Reserved|



Once the rate does change, the Downstream Port begins in Phase 1 and sends TS1s with EC = 01b. It then waits for the Upstream Port to respond with the same EC value. 

Meanwhile, the Upstream Port starts in Phase 0, as illustrated in Figure 14‐30 on page 581, and sends TS1s that echo the preset values it received earlier from the 

**580** 

**Chapter 14: Link Initialization & Training** 

EQ TS1s and EQ TS2s. It will use those requested Tx presets if they’re sup‐ ported, and will optionally use the Rx Hints. The USP is allowed to wait 500ns before evaluating the incoming signal but, once it’s able to recognize two TS1s in a row it’s ready for the next step. This means the signal quality meets the min‐ imum BER of 10[‐4] (e.g., Bit Error Ratio of less than one error in 10,000 bits). Sub‐ sequently the USP sets EC=01b in its TS1s thereby moving to Phase 1 and handing control of the next step to the DSP. 

_Figure 14‐30: Equalization Process: Starting Point_ 

**==> picture [250 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>Downstream<br>Port<br>EC = 01b EC = 00b<br>Upstream<br>Port<br>Endpoint<br>**----- End of picture text -----**<br>


**Phase 1**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
