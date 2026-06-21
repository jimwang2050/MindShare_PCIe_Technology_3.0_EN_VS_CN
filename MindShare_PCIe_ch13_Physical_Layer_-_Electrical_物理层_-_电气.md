# 📘 第 13 章　物理层 - 电气 (Chapter 13. Physical Layer - Electrical)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0293.md` ... `chunks/chunk0297.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [13.1 Physical Layer - Electrical — 物理层 - 电气](#sec-13-1)
- [13.2 Physical Layer - Electrical — 物理层 - 电气](#sec-13-2)
- [13.3 Physical Layer - Electrical — 物理层 - 电气](#sec-13-3)
- [13.4 Physical Layer - Electrical — 物理层 - 电气](#sec-13-4)
- [13.5 Physical Layer - Electrical — 物理层 - 电气](#sec-13-5)

<a id="sec-13-1"></a>
## 13.1 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

13. Since the transmitted and received Link and Lane numbers matched on Lanes 0 and 1, the Downstream Port indicates it is ready to conclude
this negotiation and proceed to the next state, L0, by sending TS2 Ordered Sets with the same Link and Lane numbers on these Lanes. The
other Lanes continue sending TS1s with PAD for both the Link and Lane numbers.

14. Upon receiving TS2s with the same Link and Lane numbers on Lanes 0 and 1, the Upstream Port also indicates its readiness to leave the
Con‐ figuration state and proceed to L0 by sending TS2s back on these Lanes. The other Lanes continue sending TS1s with PAD for both the
Link and Lane numbers. This is shown in Figure 14‐23 on page 552.

_Figure 14‐23: Example 3 ‐ Steps 5 and 6_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


Once a Port receives at least 8 TS2s and transmits at least 16, it sends some logical idle data and those Lanes transitions to L0. The other
Lanes, Lanes 2 and 3 in this example, transition to Electrical Idle until the next time the link training process is initiated at which
point those Lanes will attempt the training process like normal.

## **Detailed Configuration Substates** 

A detailed explanation of each substate is presented here to cover all the sub‐ states of Configuration, as shown in Figure 14‐24 on page
553. The Configura‐ tion Substates should be easier to follow, given the Link Training examples discussed previously.
_Figure 14‐24: Configuration State Machine_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


## **Configuration.Linkwidth.Start** 

This substate is entered after either the normal completion of the Polling state (as described in “Polling.Configuration” on page 527), or
if the Recovery state finds that Link or Lane numbers have changed since the last time they were assigned and thus the recovery process
can’t finish normally (as described in the “Recovery State” on page 571).

## **Downstream Lanes.** 

## _During Configuration.Linkwidth.Start_ 

The Downstream Port is now the leader on this Link and sends TS1s with a non‐PAD link number on all active Lanes (as long as LinkUp is 

not set and upconfiguration of the Link width is not taking place). In the TS1s, the Link number field is changed from PAD to a number while
the Lane number remains PAD. The only constraint on the value of the Link numbers in the spec is that they must be unique for each possible
Link if multiple Links are supported. For example, a x8 Link would have the same Link number on all 8 Lanes, but if it could also be
configured as two x4 Links, both groups of 4 Lanes would be assigned different Link numbers, such as 5 for one group and 6 for the other.
The values are local to the Link partners and there’s no need for software to track them or try to make them unique throughout the system.
If the upconfigure_capable bit is set to 1b, these TS1s will also be sent on any inactive Lanes that received two consecutive TS1s with Link
and Lane numbers set to PAD.

- When entering this substate from Polling, any Lane that detected a Receiver is considered active. 

- When entering from Recovery, any Lane that was part of the Link after going through Configuration.Complete is considered an active Lane. 

- All supported data rates must be advertised in the TS1s, even if the Port doesn’t intend to use them. 

**Crosslinks.** For cases where LinkUp = 0b and the optional crosslink capa‐ bility is supported, all Lanes that detected a Receiver must
send a minimum of 16 to 32 TS1s with a non‐PAD Link number and PAD Lane number. After that, the port will evaluate what it is receiving to
see if a crosslink is present.

**Upconfiguring the Link Width.** If LinkUp = 1b and the LTSSM wants to upconfigure the Link, TS1s with Link and Lane numbers set to PAD are
sent on the currently active Lanes, the inactive Lanes it intends to activate, and the Lanes that have seen incoming TS1s. When the Lanes
have received two consecutive TS1s coming back, or after 1ms, the Link number is assigned a value in the TS1s being sent.

- If activating an inactive Lane, the Transmitter must wait for the Tx com‐ mon mode voltage to settle before exiting Electrical Idle and
sending TS1s.

- Link numbers must be the same for Lanes that will be grouped into a Link. The numbers can only be different for groups of Lanes that are
capable of acting as a unique Link.

- _Exit to “After a 24ms timeout if none of the other conditions are true.”_ Any Lanes that previously received at least one TS1 with Link
and Lane
number of PAD now receive two consecutive TS1s with a non‐PAD Link number that matches a transmitted Link number and Lane num‐ bers are
still PAD will exit to the Configuration.Linkwidth.Accept sub‐ state.

## _Exit to “Configuration.Linkwidth.Start”_ 

- If the first set of received TS1s for this substate have a non‐PAD Link number then it’s understood that a crosslink is present and the
Link neighbor is also behaving as a Downstream Port. To handle this situa‐ tion, the Downstream Lanes are changed to Upstream Lanes and a
ran‐ dom crosslink timeout is chosen. The next substate will be the same Confiuration.Linkwidth.Start again but the Lanes will now behave as
Upstream Lanes.

This supports the optional behavior when both Link partners behave as Downstream Ports. The solution for this situation is to change both to
Upstream Ports and assign each a random timeout that, when it expires, changes it to a Downstream Port. Since the timeouts won’t be the
same, eventually one Port is seen as Downstream while the other is seen as Upstream and then the training can go forward. The timeout must
be random so that even if two of the same devices are connected any possible deadlock will eventually be broken.

If crosslinks are supported, receiving a sequence of TS1s that first have a Link number of PAD and later have a non‐PAD Link number that
matches the transmitted Link number is valid only if the sequence wasn’t interrupted by a TS2.

## _Exit to “Disable State”_ 

If the Port is instructed by a higher layer to send TS1s or TS2s with the Disable Link bit asserted on all detected Lanes. Normally, the
Down‐ stream Port will initiate this but, for the optional crosslink case, it could become an Upstream Port instead and then Disabled will
be the next state if 2 consecutive TS1s are received with the Loopback bit set.

## _Exit to “Loopback State”_ 

If the loopback‐capable Transmitter is instructed by a higher layer to send TS Ordered Sets with the Loopback bit asserted, or if Lanes that
are sending TS1s receive 2 consecutive TS1s with the Loopback bit set. Whichever Port sends the TS1s with the bit set will become the Loop‐
back master, while the Port that receives them will become the Loop‐ back slave.

## _Exit to “Detect State”_ 

After a 24ms timeout if none of the other conditions are true. 

## **Upstream Lanes.** 

## _During Configuration.Linkwidth.Start_ 

The Upstream Port is now the follower on this Link and goes back to sending TS1 ordered‐sets with PAD set for the Link and Lane number
fields. It will continue to do this until it begins receiving TS1s with a non‐PAD Link number from the Downstream Port (leader).

The Upstream Port sends TS1s with Link and Lane values of PAD on a) all active Lanes, b) the Lanes it wants to upconfigure and, c) if
upconfigure_capable is set to 1b, on each of the inactive Lanes that have received two consecutive TS1s with Link and Lane numbers set to
PAD while in this substate.

- When entering this substate from Polling, any Lane that detected a Receiver is considered active. 

- When entering from Recovery, any Lane that was part of the Link after going through Configuration.Complete is considered an active Lane.
If the transition wasn’t caused by an LTSSM timeout, the Trans‐ mitter must set the Autonomous Change bit (Symbol 4, bit 6) to 1b in the
TS1s being sent in the Configuration state if it does, in fact, plan to change the Link width for autonomous reasons.

- All supported data rates must be advertised in the TS1s, even if the Port doesn’t intend to use them. 

**Crosslinks.** For cases where LinkUp = 0b and the optional crosslink capa‐ bility is supported, all Lanes that detected a Receiver must
send a minimum of 16 to 32 TS1s with Link and Lane values of PAD. After that, the port will evaluate what it is receiving to see if a
crosslink is present.

_Exit to “After a 24ms timeout if none of the other conditions are true.”_ 

- If _any_ Lanes receive two consecutive TS1s with non‐PAD Link number and PAD Lane number, this port transitions to the Configuration.Link‐
width.Accept substate where one of the received Link numbers is selected for those Lanes and TS1s are sent back with that Link number and a
PAD Lane number, on _all_ the Lanes that received TS1s with a non‐ PAD Link number. Any left‐over Lanes that detected a Receiver but no Link
number must send TS1s with Link and Lane numbers set to PAD.

- If upconfiguring the Link, the LTSSM waits until it receives two con‐ secutive TS1s with a non‐PAD Link number and PAD Lane number on
either a) all the inactive Lanes it wants to activate, or b) on any
Lane 1ms after entering this substate, whichever is earlier. After that, it sends TS1s with the selected Link number along with PAD Lane
numbers.

- To avoid configuring a Link smaller than necessary, it’s recom‐ mended that a multi‐Lane Link that sees an error or loses Block Alignment
on some Lanes delay this Receiver evaluation. For 8b/10b encoding, it should wait at least two more TS1s, while for 128b/130b encoding it
should wait for at least 34 TS1s, but never more than 1ms in any case.

- After activating an inactive Lane, the Transmitter must wait for the Tx common mode voltage to settle before exiting Electrical Idle and
sending TS1s.

## _Exit to “Configuration.Linkwidth.Start”_ 

- After a crosslink timeout, send 16 to 32 TS2s with Link and Lane values of PAD. The Upstream Lanes change to Downstream Lanes and the next
substate will be the same Confiuration.Linkwidth.Start again but this time the Lanes behave as Downstream Lanes. For the case of two
Upstream Ports connected together, this optional behavior allows one of them to eventually take the lead as a Downstream Port.

## _Exit to “Disable State”_ 

If either of the following is true: 

- Any Lanes that are sending TS1s also receive TS1s with the Disable Link bit asserted. 

- The optional crosslink is supported and either all Lanes that are sending and receiving TS1s receive the Disable Link bit in two con‐
secutive TS1s, or else a crosslink Port is directed by a higher Layer to assert the Disable bit in its TS1s and TS2s on all Lanes that
detected a Receiver.

## _Exit to “Loopback State”_

</td>
<td width="50%">

- If a loopback‐capable Transmitter is directed by a higher Layer to send TS Ordered Sets with the Loopback bit asserted or all Lanes that
are sending and receiving TS1s receive 2 consecutive TS1s with the Loopback bit set. Whichever Port sends the TS1s with the bit set will
become the Loopback master, while the Port that receives them will become the Loopback slave.

## _Exit to "Detect State"_

- After a 24ms timeout if none of the other conditions are true.

## **Configuration.Linkwidth.Accept**

At this point, the Upstream Port is now sending back TS1 ordered‐sets on all its Lanes with the same Link number. The Link number originated
from the Downstream Port, and the Upstream Port is simply reflecting that value back on all its Lanes. Now the Downstream Port knows the
Link width (number of Lanes receiving the same Link number) and it must start advertising the Lane numbers. So the leader (Downstream Port)
continues sending TS1s, but now with the actual Lane numbers designated instead of PAD. Also, all these TS1s will have the same Link number.
The detailed behavior for the Downstream and Upstream Lanes are outlined below:

## **Downstream Lanes**

## _During Configuration.Linkwidth.Accept_

- The Downstream Port will now initiate Lane numbers. If a Link can be formed from at least one group of Lanes that all receive two
consecutive TS1s and all see the same Link number, then TS1s are sent that keep that same Link number but now assign unique, non‐PAD Lane
numbers as well.

## _Exit to "Configuration.Lanenum.Wait"_

- The Downstream Port does not stay in the Configuration.Linkwidth.Accept substate very long. Once it has received the necessary TS1s from
the Upstream Port indicating, the Link width, it updates any internal state info that is required, starts sending TS1s with non‐PAD Lane
numbers, as indicated above, and immediately transitions to Configuration.Lanenum.Wait to await Lane Number confirmation from the Upstream
Port.

## **Upstream Lanes**

## _During Configuration.Linkwidth.Accept_

- The Upstream Port transmits TS1s where one of the received Link numbers is selected and sent back in the TS1s on _all_ the Lanes that
received TS1s with a non‐PAD Link number. Any left‐over Lanes that detected a Receiver but no Link number must send TS1s with Link and Lane
numbers set to PAD.

## _Exit to "Configuration.Lanenum.Wait"_

- The Upstream Port must respond to the Lane numbers proposed to it by the Link neighbor. If a Link can be formed using Lanes that sent a
non‐PAD Link number on their TS1s and received two consecutive TS1s with the same Link number and any non‐PAD Lane number, then it should
send TS1s that match the same Lane number assignments, if possible, or are different if necessary (such as with the optional Lane reversal).
## **Configuration.Lanenum.Wait**

Prior to discussing the Configuration.Lanenum.Wait state, some background information may be helpful. Lane numbers are assigned sequentially
from zero to the maximum number possible for a Link. For example, a x8 Link will be assigned Lane numbers 0 ‐ 7. Ports are required to
support a Link as wide as the number of Lanes they have and as small as one Lane. The Lanes will always start with Lane 0 and must be both
sequential and contiguous. For example, if some Lanes on a x8 Port aren't working, it might optionally be designed to configure a x4 Link
and, if so, it would need to use Lanes 0‐3. As another example, if Lane 2 of a x8 Port is not working, it wouldn't be possible to use Lanes
0, 1, 3, and 4 to form a x4 Link because the Lanes wouldn't be contiguous. Any left‐over Lanes must send TS1s with Link and Lane set to PAD.

A common timing consideration is repeated many times in the spec for the Configuration substates. Rather than repeat it for every case here,
just be aware that it applies in general to both Upstream and Downstream Ports:

To avoid configuring a Link smaller than necessary, it's recommended that a multi‐Lane Port delay the final link width evaluation if it sees
an error or loses Block Alignment on some Lanes. For 8b/10b, it should wait at least two more TS1s, while for 128b/130b mode it should wait
for at least 34 TS1s, but never more than 1ms in any case. The idea is that the Lanes might need settling time after powering up or being
reset.

## _Exit to "Detect State"_

After a 2ms timeout if no Link can be configured (e.g.: Lane 0 is not working and Lane Reversal isn't available), or if all Lanes receive
two consecutive TS1s with PAD in both the Link and Lane numbers, the link must exit to the Detect State.

## **Downstream Lanes**

## _During Configuration.Lanenum.Wait_

The Downstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met.

## _Exit to "Configuration.Lanenum.Accept"_

If either of the cases listed below is true:

- If two consecutive TS1s have been received on all Lanes with Link and Lane numbers that match what is being transmitted on those Lanes.

- If any Lanes that detected a Receiver see two consecutive TS1s with a Lane number different from when the Lane first entered this substate
and at least some Lanes see a non‐PAD Link number. The spec points out that this allows the two Ports to settle on a mutually acceptable
Link width.

## _Exit to "Detect State"_

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD.

Upstream Lanes

## _During Configuration.Lanenum.Wait_

The Upstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met.

## _Exit to "Configuration.Lanenum.Accept"_

If either of the cases listed below is true:

- If any Lanes receive two consecutive TS2s.

- If any Lanes receive two consecutive TS1s with a Lane number different from when the Lane first entered this substate and at least some
Lanes see a non‐PAD Link number.

Note that Upstream Lanes are allowed to wait up to 1ms before changing to that substate, so as to prevent received errors or skew between
Lanes from affecting the final Link configuration.

## _Exit to "Detect State"_

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD.

## **Configuration.Lanenum.Accept**

Downstream Lanes

## _During Configuration.Lanenum.Accept_

The Downstream Port has now received TS1s with non‐PAD Link and Lane numbers. It is at this point that the Downstream Port must decide if a
Link can be established with the Lane numbers returned by the Upstream Port. The three possible state transitions are listed below.

## _Exit to "Configuration.Complete"_

If two consecutive TS1s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being transmitted
in the TS1s for all the Lanes, then Upstream Port has agreed with the Link and
Lane numbers advertised by the Downstream Port and the next substate is Configuration.Complete. Or if the Lane numbers in the received TS1s
are reversed from what the Downstream Port advertised, if the Downstream Port supports Lane Reversal, it can still proceed to
Configuration.Complete while using the reversed Lane numbers.

The spec points out that the Reversed Lane condition is strictly defined as Lane 0 receiving TS1s with the highest Lane number (total number
of Lanes ‐ 1) and the highest Lane number receiving TS1s with Lane number of zero. One thing that can be understood from this is the answer
to a question that comes up in class sometimes: Can the Lane numbers be mixed up, rather than sequential? The answer is no, they must be
from 0 to n‐1 or from n‐1 to 0; no other options are supported.

If the Configuration state was entered from the Recovery state, a bandwidth change may have been requested. If so, status bits will be
updated to report the nature of what happened. Basically, the system needs to report whether this change was initiated because the Link
wasn't working reliably or because hardware is simply managing the Link power. The bits are updated as follows:

- If the bandwidth change was initiated by the Downstream Port because of a reliability problem, the Link Bandwidth Management Status bit is
set to 1b.

- If the bandwidth change was not initiated by the Downstream Port but the Autonomous Change bit in two consecutive received TS1s is cleared
to 0b, the Link Bandwidth Management Status bit is set to 1b.

- Otherwise the Link Autonomous Bandwidth Status bit is set to 1b.

## _Exit to "Configuration.Lanenum.Wait"_

- If a configured Link can be formed with some but not all of the Lanes that receive two consecutive TS1s with the same non‐PAD Link and
Lane numbers, those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve
a working Link.

The new Lane numbers must start with zero and increase sequentially to cover the Lanes that will be used. Any Lanes that don't receive TS1s
can't be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s with Link and Lane set to PAD. For
example, if 8 Lanes are available, but Lane 2 doesn't see incoming TS1s, then the Link can't consist of a group that would need Lane 2.
Consequently, the x8 and x4 options would not be available, and only a x1 or x2 Link is possible.

## _Exit to "Detect State"_

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers.

## **Upstream Lanes**

## _During Configuration.Lanenum.Accept_

- The Upstream Port has now received either TS2s or TS1s with non‐PAD Link and Lane numbers. It is at this point that the Upstream Port must
decide if a Link can be established with the Lane numbers sent by the Downstream Port. The three possible state transitions are listed
below.

## _Exit to "Configuration.Complete"_

- If two consecutive TS2s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being
transmitted in the TS1s for those Lanes, all is well and the next substate will be Configuration.Complete.

## _Exit to "Configuration.Lanenum.Wait"_

- If a configured Link can be formed with a subset of Lanes that receive two consecutive TS1s with the same non‐PAD Link and Lane numbers,
those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve a working
Link. The next substate in this case will be Configuration.Lanenum.Wait.

As was the case for the Downstream Lanes, the new Lane numbers must start with zero and increase sequentially to cover the Lanes that will
be used. Any Lanes that don't receive TS1s can't be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s
with Link and Lane set to PAD.

## _Exit to "Detect State"_

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers, then the next state will be
Detect.

## **Configuration.Complete**

This is the only substate of the Configuration state where TS2s are exchanged. As discussed before, the purpose of TS2s is a handshake, or
confirmation between the two devices on the link that they are ready to proceed to the next state. So this is the final confirmation of the
Link and Lane numbers exchanged in the TS1s leading up to this point.
It should be noted that Devices are allowed to change their supported data rates and upconfigure capability when they enter this substate,
but not while in it. This is because Devices record the capabilities of their Link partner from what is advertised in these TS2s, as will be
described in this section.

## **Downstream Lanes**

## _During Configuration.Complete_

TS2s are sent using the Link and Lane numbers that match the received TS1s. The TS2s can have the Upconfigure Capability bit set if the Port
supports a x1 Link using Lane 0 and is able to up‐configure the Link.

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes
see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling
cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity.

The Downstream Port is transmitting TS2s and watching for TS2s coming back. For future reference, record the number of FTSs that must be
sent when exiting from the L0s state from the N_FTS field in the incoming TS2s.

## _Exit to "Configuration.Idle"_

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching
rate identifiers, and matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2.

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane and this overrides
any previously recorded value. The variable used to track speed changes in Recovery, "changed_speed_recovery", is cleared to zero.

The variable "upconfigure_capable" is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8
consecutive TS2s with the same bit set. Otherwise it's cleared to zero.

Any Lanes that aren't configured as part of the Link are no longer associated with the LTSSM in progress and must either be:

- Associated with a new LTSSM or

- Transitioned to Electrical Idle

 - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b

since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it's also recommended that
those Lanes leave their Receiver terminations on because they'll become part of the Link again if it is upconfigured. If the terminations
aren't left on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete.
Lanes that weren't part of the Link before can't become part of it through this process, though.

- b) For the optional crosslink, Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG.

- c) If the LTSSM goes back to Detect, these Lanes will once again be associated with it.

- d) No EIOS is needed before Lanes go to Electrical Idle, and the transition doesn't have to happen on Symbol or Ordered Set boundaries.

## After a 2ms timeout:

_Exit to "Configuration.Idle"_

Next state is Configuration.Idle if the idle_to_rlock_transitioned variable is less than FFh **and** the current data rate is 8.0 GT/s.

In this transition, the "changed_speed_recovery" variable is cleared to zero. Also, the "upconfigure_capable" variable may be updated,
though it's not required to do so, if at least one Lane saw eight consecutive TS2s with matching Link and Lane numbers (non‐PAD). If the
transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero.

Lanes that aren't part of the configured Link aren't associated with the LTSSM in progress and have the same requirements as the non‐timeout
case listed above.

_Exit to "Detect State"_

Otherwise, the next state is Detect.

## **Upstream Lanes**

_During Configuration.Complete_

TS2s are sent using the Link and Lane numbers that match the received TS2s. The TS2s can have the Upconfigure Capability bit set if the Port
supports a x1 Link using Lane 0 and is able to up‐configure the Link.
For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes
see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling
cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity.

In this substate, the Upstream Port is receiving TS2s from the Downstream Port, and for future reference, should record the N_FTS field
value number of FTSs that must be sent when exiting from the L0s state from the in the incoming TS2s.

## _Exit to "Configuration.Idle"_

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching
rate identifiers, and a matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2.

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane, overriding any
previously recorded value. The variable used to track speed changes in Recovery, "changed_speed_recovery", is cleared to zero.

The variable "upconfigure_capable" is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8
consecutive TS2s with the same bit set. Otherwise it's cleared to zero.

Any Lanes that aren't configured as part of the Link are no longer associated with the LTSSM in progress and must either be:

- Optionally associated with a new crosslink LTSSM (if this feature is supported), or

- Transitioned to Electrical Idle

 - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b
since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it's also recommended that
those Lanes leave their Receiver terminations on because they'll become part of the Link again if it is upconfigured. If they're not left
on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete. Lanes that
weren't part of the Link before can't become part of it through this process, though.

- b) Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐

 - HIGH‐IMP‐DC‐NEG[.]

- c) If the LTSSM goes back to Detect, these Lanes will once again be associated with it.

- d) No EIOS is needed before Lanes go to Electrical Idle, and the transition doesn't have to happen on Symbol or Ordered Set boundaries.

## After a 2ms timeout:

## _Exit to "Configuration.Idle"_

Next state is Configuration.Idle if the idle_to_rlock_transitioned variable is less than FFh **and** the current data rate is 8.0 GT/s.

In this transition, the "changed_speed_recovery" variable is cleared to zero. Also, the "upconfigure_capable" variable may be updated,
though it's not required to do so, if at least one Lane saw eight consecutive TS2s with matching Link and Lane numbers (non‐PAD). If the
transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero.

Lanes that aren't part of the configured Link aren't associated with the LTSSM in progress and have the same requirements as the non‐timeout
case listed above.

## _Exit to "Detect State"_

Otherwise, the next state is Detect.

## **Configuration.Idle**

## _During Configuration.Idle_

In this substate, the transmitter is sending Idle data and waiting for the minimum number of received Idle data so this Link can transition
to L0. During this time, the Physical Layer reports to the upper layers that the link is operational (Linkup = 1b).

For 8b/10b encoding, the transmitter is sending Idle data on all configured Lanes. Idle data are just data zeros that get scrambled and
encoded.

For 128b/130b encoding, the transmitter sends one SDS Ordered Set on all configured Lanes followed by Idle data Symbols. The first Idle
Symbol on Lane 0 is the first Symbol of the Data Stream.
## _Exit to "L0 State"_

If using 8b/10b encoding, the next state is L0 if 8 consecutive Idle data symbol times are received on all configured Lanes, and 16 symbol
times of idle data were sent after receiving one Idle Symbol.

If using 128b/130b, the next state is L0 if 8 consecutive Idle data are received on all configured Lanes, 16 Idles were sent after receiving
one Idle Symbol, and this state wasn't entered by a timeout from Configuration.Complete.

- Lane‐to‐Lane de‐skew must be completed before Data Stream processing begins.

- The Idle Symbols must be received in Data Blocks.

- If software set the Retrain Link bit in the Link Control register since the last transition to L0 from Recovery or Configuration, the
Downstream Port must set the Link Bandwidth Management bit in the Link Status register to 1b to indicate that this change was not hardware
initiated (autonomous).

- The "idle_to_rlock_transitioned" variable is cleared to 00h on transition to L0.

## After a 2ms timeout:

## _Exit to "Detailed Recovery Substates"_

If the idle_to_rlock_transitioned variable is less than FFh, the next state is Recovery (Recovery.RcvrLock). Then:

- a) For 8.0 GT/s, increment idle_to_rlock_transitioned by 1.

- b) For 2.5 or 5.0 GT/s, set idle_to_rlock_transitioned to FFh.

- c) NOTE: This variable counts the number of times the LTSSM has transitioned from this state to the Recovery state because the sequence
isn't working. The problem may be that equalization hasn't been properly adjusted or that the selected speed just isn't going to work, and
the Recovery state will take steps to address these issues. This variable limits the number of these attempts so as to avoid an endless
loop. If the Link still isn't working after doing this 256 times (when the count reaches FFh), go back to Detect and start over, hoping for
a better result.

_Exit to "Detect State"_

Otherwise (meaning idle_to_rlock = FFh), the next state is Detect.

## **L0 State**

This is the normal, fully‐operational Link state, during which Logical Idle, TLPs and DLLPs are exchanged between Link neighbors. L0 is
achieved immediately following the conclusion of the Link Training process. The Physical Layer also notifies the upper layers that the Link
is ready for operation, by setting the LinkUp variable. In addition, the idle_to_rlock_transitioned variable is cleared to 00h.

## _Exit to "Recovery State"_

The next state will be Recovery if a change in the Link speed or Link width is indicated, or if the Link partner initiates this by going to
Recovery or Electrical Idle. Let's consider each of these three cases in a little more detail in the following discussion.

## **Speed Change**

Two conditions are described in the spec that will cause an automatic change in speed.

The first is when rates higher than 2.5 GT/s are supported by both partners and the Link is active (Data Link Layer reports DL_Active), or
when one partner requests a speed change in its TS Ordered Sets. For example, a Downstream Port will initiate a speed change if a higher
rate was noted and software writes the Retrain Link bit and after setting the Target Link Speed field (see Figure 14‐ 26 on page 569) to a
different rate than the current rate.

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0547_img1_tight.png" alt="Figure from page 547" width="700">

<a id="sec-13-2"></a>
## 13.2 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

- If a loopback‐capable Transmitter is directed by a higher Layer to send TS Ordered Sets with the Loopback bit asserted or all Lanes that
are sending and receiving TS1s receive 2 consecutive TS1s with the Loop‐ back bit set. Whichever Port sends the TS1s with the bit set will
become the Loopback master, while the Port that receives them will become the Loopback slave.

## _Exit to “Detect State”_ 

- After a 24ms timeout if none of the other conditions are true. 

## **Configuration.Linkwidth.Accept** 

At this point, the Upstream Port is now sending back TS1 ordered‐sets on all its Lanes with the same Link number. The Link number originated
from the Down‐ stream Port, and the Upstream Port is simply reflecting that value back on all its Lanes. Now the Downstream Port knows the
Link width (number of Lanes receiving the same Link number) and it must start advertising the Lane num‐ bers. So the leader (Downstream
Port) continues sending TS1s, but now with the actual Lane numbers designated instead of PAD. Also, all these TS1s will have the same Link
number. The detailed behavior for the Downstream and Upstream Lanes are outlined below:

## **Downstream Lanes** 

## _During Configuration.Linkwidth.Accept_ 

- The Downstream Port will now initiate Lane numbers. If a Link can be formed from at least one group of Lanes that all receive two
consecutive TS1s and all see the same Link number, then TS1s are sent that keep that same Link number but now assign unique, non‐PAD Lane
numbers as well.

## _Exit to “Configuration.Lanenum.Wait”_ 

- The Downstream Port does not stay in the Configuration.Linkwidth.Accept substate very long. Once it has received the necessary TS1s from
the Upstream Port indicating, the Link width, it updates any internal state info that is required, starts sending TS1s with non‐PAD Lane
numbers, as indi‐ cated above, and immediately transitions to Configuration.Lanenum.Wait to await Lane Number confirmation from the Upstream
Port.

## **Upstream Lanes** 

## _During Configuration.Linkwidth.Accept_ 

- The Upstream Port transmits TS1s where one of the received Link numbers is selected and sent back in the TS1s on _all_ the Lanes that
received TS1s with a non‐PAD Link number. Any left‐over Lanes that detected a Receiver but no Link number must send TS1s with Link and Lane
numbers set to PAD.

## _Exit to “Configuration.Lanenum.Wait”_ 

- The Upstream Port must respond to the Lane numbers proposed to it by the Link neighbor. If a Link can be formed using Lanes that sent a
non‐PAD Link number on their TS1s and received two consecutive TS1s with the same Link number and any non‐PAD Lane number, then it should
send TS1s that match the same Lane number assignments, if possible, or are dif‐ ferent if necessary (such as with the optional Lane
reversal).
## **Configuration.Lanenum.Wait** 

Prior to discussing the Configuration.Lanenum.Wait state, some background information may be helpful. Lane numbers are assigned sequentially
from zero to the maximum number possible for a Link. For example, a x8 Link will be assigned Lane numbers 0 ‐ 7. Ports are required to
support a Link as wide as the number of Lanes they have and as small as one Lane. The Lanes will always start with Lane 0 and must be both
sequential and contiguous. For example, if some Lanes on a x8 Port aren’t working, it might optionally be designed to con‐ figure a x4 Link
and, if so, it would need to use Lanes 0‐3. As another example, if Lane 2 of a x8 Port is not working, it wouldn’t be possible to use Lanes
0, 1, 3, and 4 to form a x4 Link because the Lanes wouldn’t be contiguous. Any left‐ over Lanes must send TS1s with Link and Lane set to
PAD.

A common timing consideration is repeated many times in the spec for the Con‐ figuration substates. Rather than repeat it for every case
here, just be aware that it applies in general to both Upstream and Downstream Ports:

To avoid configuring a Link smaller than necessary, it’s recommended that a multi‐Lane Port delay the final link width evaluation if it sees
an error or loses Block Alignment on some Lanes. For 8b/10b, it should wait at least two more TS1s, while for 128b/130b mode it should wait
for at least 34 TS1s, but never more than 1ms in any case. The idea is that the Lanes might need settling time after powering up or being
reset.

## _Exit to “Detect State”_ 

After a 2ms timeout if no Link can be configured (e.g.: Lane 0 is not working and Lane Reversal isn’t available), or if all Lanes receive
two consecutive TS1s with PAD in both the Link and Lane numbers, the link must exit to the Detect State.

## **Downstream Lanes** 

## _During Configuration.Lanenum.Wait_ 

The Downstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met. 

## _Exit to “Configuration.Lanenum.Accept”_ 

If either of the cases listed below is true: 

- If two consecutive TS1s have been received on all Lanes with Link and Lane numbers that match what is being transmitted on those Lanes. 

- If any Lanes that detected a Receiver see two consecutive TS1s with a Lane number different from when the Lane first entered this substate
and at least some Lanes see a non‐PAD Link number. The spec points out that this allows the two Ports to settle on a mutually acceptable
Link width.

## _Exit to “Detect State”_ 

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD. 

Upstream Lanes 

## _During Configuration.Lanenum.Wait_ 

The Upstream Port will continue to transmit TS1s with the non‐PAD Link and Lane numbers until one of the exit conditions is met. 

## _Exit to “Configuration.Lanenum.Accept”_ 

If either of the cases listed below is true: 

- If any Lanes receive two consecutive TS2s. 

- If any Lanes receive two consecutive TS1s with a Lane number different from when the Lane first entered this substate and at least some
Lanes see a non‐PAD Link number.

Note that Upstream Lanes are allowed to wait up to 1ms before changing to that substate, so as to prevent received errors or skew between
Lanes from affecting the final Link configuration.

## _Exit to “Detect State”_ 

After a 2ms timeout or if all Lanes receive two consecutive TS1s with Link and Lane numbers set to PAD. 

## **Configuration.Lanenum.Accept** 

Downstream Lanes 

## _During Configuration.Lanenum.Accept_ 

The Downstream Port has now received TS1s with non‐PAD Link and Lane numbers. It is at this point that the Downstream Port must decide if a
Link can be established with the Lane numbers returned by the Upstream Port. The three possible state transitions are listed below.

## _Exit to “Configuration.Complete”_ 

If two consecutive TS1s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being transmitted
in the TS1s for all the Lanes, then Upstream Port has agreed with the Link and
Lane numbers advertised by the Downstream Port and the next substate is Configuration.Complete. Or if the Lane numbers in the received TS1s
are reversed from what the Downstream Port advertised, if the Downstream Port supports Lane Reversal, it can still proceed to
Configuration.Complete while using the reversed Lane numbers.

The spec points out that the Reversed Lane condition is strictly defined as Lane 0 receiving TS1s with the highest Lane number (total number
of Lanes ‐ 1) and the highest Lane number receiving TS1s with Lane number of zero. One thing that can be understood from this is the answer
to a question that comes up in class sometimes: Can the Lane numbers be mixed up, rather than sequential? The answer is no, they must be
from 0 to n‐1 or from n‐1 to 0; no other options are supported.

If the Configuration state was entered from the Recovery state, a bandwidth change may have been requested. If so, status bits will be
updated to report the nature of what happened. Basically, the system needs to report whether this change was initiated because the Link
wasn’t working reliably or because hardware is simply managing the Link power. The bits are updated as follows:

- If the bandwidth change was initiated by the Downstream Port because of a reliability problem, the Link Bandwidth Management Status bit is
set to 1b.

- If the bandwidth change was not initiated by the Downstream Port but the Autonomous Change bit in two consecutive received TS1s is cleared
to 0b, the Link Bandwidth Management Status bit is set to 1b.

- Otherwise the Link Autonomous Bandwidth Status bit is set to 1b. 

## _Exit to “Configuration.Lanenum.Wait”_ 

- If a configured Link can be formed with some but not all of the Lanes that receive two consecutive TS1s with the same non‐PAD Link and
Lane num‐ bers, those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to
achieve a working Link.

The new Lane numbers must start with zero and increase sequentially to cover the Lanes that will be used. Any Lanes that don’t receive TS1s
can’t be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s with Link and Lane set to PAD. For
example, if 8 Lanes are available, but Lane 2 doesn’t see incoming TS1s, then the Link can’t consist of a group that would need Lane 2.
Consequently, the x8 and x4 options would not be available, and only a x1 or x2 Link is possible.

## _Exit to “Detect State”_ 

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers. 

## **Upstream Lanes** 

## _During Configuration.Lanenum.Accept_ 

- The Upstream Port has now received either TS2s or TS1s with non‐PAD Link and Lane numbers. It is at this point that the Upstream Port must
decide if a Link can be established with the Lane numbers sent by the Downstream Port. The three possible state transitions are listed
below.

## _Exit to “Configuration.Complete”_ 

- If two consecutive TS2s are received with the same non‐PAD Link and Lane numbers, and they match the Link and Lane numbers being
transmitted in the TS1s for those Lanes, all is well and the next substate will be Configura‐ tion.Complete.

## _Exit to “Configuration.Lanenum.Wait”_ 

- If a configured Link can be formed with a subset of Lanes that receive two consecutive TS1s with the same non‐PAD Link and Lane numbers,
those Lanes send TS1s with the same Link number and new Lane numbers. The object is to use a smaller group of Lanes to achieve a working
Link. The next substate in this case will be Configuration.Lanenum.Wait.

As was the case for the Downstream Lanes, the new Lane numbers must start with zero and increase sequentially to cover the Lanes that will
be used. Any Lanes that don’t receive TS1s can’t be part of the group and will disrupt the Lane numbering. Any leftover Lanes must send TS1s
with Link and Lane set to PAD.

## _Exit to “Detect State”_ 

- If no Link can be configured, or if all Lanes receive two consecutive TS1s with PAD for Link and Lane numbers, then the next state will be
Detect.

## **Configuration.Complete** 

This is the only substate of the Configuration state where TS2s are exchanged. As discussed before, the purpose of TS2s is a handshake, or
confirmation between the two devices on the link that they are ready to proceed to the next state. So this is the final confirmation of the
Link and Lane numbers exchanged in the TS1s leading up to this point.
</td>
<td width="50%">

- 如果支持回环的发送器被更高层指示发送 Loopback 位置位的 TS 有序集，或者所有正在发送和接收 TS1 的 Lane 收到 2 个连续的 Loopback 位置位的 TS1。无论哪个端口发送带此位设置的 TS1 都将成为 Loopback 主机，而接收它们的端口将成为
Loopback 从机。

## _退出至"Detect 状态"_

- 在 24ms 超时后，如果其他条件都不成立。

**PCI Express 技术**

## **Configuration.Linkwidth.Accept**

此时，上游端口 (Upstream Port) 正在通过其所有 Lane 发送回具有相同 Link 号的 TS1 有序集。Link 号源自下游端口 (Downstream Port)，上游端口只是在所有 Lane 上将该值反射回去。现在下游端口知道链路宽度（接收相同 Link
号的 Lane 数），并且它必须开始通告 Lane 号。因此，主导方（下游端口）继续发送 TS1，但现在使用指定的实际 Lane 号代替 PAD。此外，所有这些 TS1 将具有相同的 Link 号。下游和上游 Lane 的详细行为概述如下：

## **下游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 下游端口 (Downstream Port) 现在将发起 Lane 号。如果可以由至少一组 Lane 形成链路，并且所有这些 Lane 都接收到两个连续的 TS1 并且都看到相同的 Link 号，则发送保持相同 Link 号但现在也分配唯一非 PAD 的 Lane 号的
TS1。

## _退出至"Configuration.Lanenum.Wait"_

- 下游端口 (Downstream Port) 不会在 Configuration.Linkwidth.Accept 子状态中停留很长时间。一旦它从上游端口接收到指示链路宽度的必要 TS1，它就会更新所需的任何内部状态信息，开始发送具有非 PAD Lane 号的
TS1，如上所述，并立即转换到 Configuration.Lanenum.Wait 以等待来自上游端口的 Lane 号确认。

## **上游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 上游端口 (Upstream Port) 发送 TS1，其中选择接收到的 Link 号之一并在**所有**接收到具有非 PAD Link 号的 TS1 的 Lane 上的 TS1 中发送回去。任何已检测到接收器但未检测到 Link 号的剩余 Lane 必须发送 Link 和
Lane 号设置为 PAD 的 TS1。

## _退出至"Configuration.Lanenum.Wait"_

- 上游端口 (Upstream Port) 必须响应链路邻居向其提议的 Lane 号。如果可以使用在其 TS1 上发送非 PAD Link 号并且接收到两个具有相同 Link 号和任何非 PAD Lane 号的连续 TS1 的 Lane 形成链路，那么它应发送匹配相同 Lane
号分配的 TS1（如果可能），或者在必要时发送不同的（例如使用可选的 Lane 反转）。

**第 14 章：链路初始化与训练**

## **Configuration.Lanenum.Wait**

在讨论 Configuration.Lanenum.Wait 状态之前，一些背景信息可能会有所帮助。Lane 号从零开始顺序分配到链路可能的最大数量。例如，x8 链路将被分配 Lane 号 0 至 7。端口需要支持与其所具有的 Lane 数一样宽的链路，且至少为一个
Lane。Lane 将始终从 Lane 0 开始，并且必须既顺序又连续。例如，如果 x8 端口上的一些 Lane 无法工作，可以选择将其设计为配置 x4 链路，如果是这种情况，则它需要使用 Lane 0-3。作为另一个示例，如果 x8 端口的 Lane 2 出现故障，则无法使用
Lane 0、1、3 和 4 来形成 x4 链路，因为 Lane 不是连续的。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

一个常见的时序考虑因素在 Configuration 子状态的规范中重复多次。这里不是为每种情况都重复它，只需注意它通常适用于上游和下游端口：

为避免将链路配置得比必要的更小，建议多 Lane 端口在看到错误或丢失某些 Lane 的块对齐 (Block Alignment) 时延迟最终的链路宽度评估。对于 8b/10b，它应至少再等待两个 TS1，而对于 128b/130b 模式，它应至少等待 34 个
TS1，但在任何情况下都不能超过 1ms。其思想是 Lane 在上电或复位后可能需要稳定时间。

## _退出至"Detect 状态"_

在 2ms 超时后，如果无法配置链路（例如：Lane 0 不工作且 Lane 反转不可用），或者如果所有 Lane 收到两个连续的 Link 和 Lane 号都为 PAD 的 TS1，则链路必须退出到 Detect 状态。

## **下游 Lane**

## _在 Configuration.Lanenum.Wait 期间_

下游端口 (Downstream Port) 将继续使用非 PAD Link 和 Lane 号发送 TS1，直到满足退出条件之一为止。

## _退出至"Configuration.Lanenum.Accept"_

如果下面列出的任一情况为真：

- 如果在所有 Lane 上都收到两个连续的 TS1，其 Link 和 Lane 号与在这些 Lane 上传输的内容匹配。

**PCI Express 技术**

- 如果任何检测到接收器的 Lane 看到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD Link 号。规范指出，这允许两个端口在相互可接受的链路宽度上达成一致。

## _退出至"Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

上游 Lane

## _在 Configuration.Lanenum.Wait 期间_

上游端口 (Upstream Port) 将继续使用非 PAD Link 和 Lane 号发送 TS1，直到满足退出条件之一为止。

## _退出至"Configuration.Lanenum.Accept"_

如果下面列出的任一情况为真：

- 如果任何 Lane 收到两个连续的 TS2。

- 如果任何 Lane 收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD Link 号。

请注意，允许上游 Lane 在更改为该子状态之前等待最多 1ms，以防止接收错误或 Lane 之间的偏移影响最终的链路配置。

## _退出至"Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

## **Configuration.Lanenum.Accept**

下游 Lane

## _在 Configuration.Lanenum.Accept 期间_

下游端口 (Downstream Port) 现在已收到具有非 PAD Link 和 Lane 号的 TS1。在此时，下游端口必须决定是否可以使用上游端口返回的 Lane 号建立链路。列出了三种可能的状态转换。

## _退出至"Configuration.Complete"_

如果收到两个连续的 TS1 具有相同的非 PAD Link 和 Lane 号，并且它们与为所有 Lane 的 TS1 中传输的 Link 和 Lane 号匹配，则上游端口已同意下游端口通告的 Link 和

**第 14 章：链路初始化与训练**

Lane 号，下一个子状态为 Configuration.Complete。或者如果接收到的 TS1 中的 Lane 号与下游端口通告的相反，如果下游端口支持 Lane 反转 (Lane Reversal)，它仍然可以继续到
Configuration.Complete，同时使用反转的 Lane 号。

规范指出，反转 Lane 条件严格定义为 Lane 0 收到具有最高 Lane 号（Lane 总数 ‐ 1）的 TS1，而最高 Lane 号收到 Lane 号为零的 TS1。可以从此了解课堂上偶尔出现的一个问题的答案：Lane 号可以混合而不是顺序吗？答案是不可以，它们必须是从
0 到 n‐1 或从 n‐1 到 0；不支持其他选项。

如果 Configuration 状态是从 Recovery 状态进入的，则可能已请求带宽更改。如果是这样，将更新状态位以报告发生的情况的性质。基本上，系统需要报告此更改是因链路无法可靠工作而发起，还是硬件只是管理链路电源。按如下方式更新位：

- 如果带宽更改是由下游端口 (Downstream Port) 由于可靠性问题而发起的，则将链路带宽管理状态 (Link Bandwidth Management Status) 位置为 1b。

- 如果带宽更改不是由下游端口发起，但在两个连续接收的 TS1 中的 Autonomous Change 位清零为 0b，则将链路带宽管理状态位置为 1b。

- 否则将链路自主带宽状态 (Link Autonomous Bandwidth Status) 位置为 1b。

## _退出至"Configuration.Lanenum.Wait"_

- 如果可以使用一些但不是所有接收两个具有相同非 PAD Link 和 Lane 号的连续 TS1 的 Lane 来形成已配置的链路，则这些 Lane 发送具有相同 Link 号和新 Lane 号的 TS1。目标是使用较小的 Lane 组来实现工作的链路。

新的 Lane 号必须从零开始并按顺序增加，以覆盖将使用的 Lane。任何未收到 TS1 的 Lane 不能成为该组的一部分，并且会扰乱 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。例如，如果有 8 个 Lane 可用，但
Lane 2 未看到传入的 TS1，则链路不能由需要 Lane 2 的组组成。因此，x8 和 x4 选项将不可用，并且仅可能使用 x1 或 x2 链路。

**PCI Express 技术**

## _退出至"Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号均为 PAD 的 TS1。

## **上游 Lane**

## _在 Configuration.Lanenum.Accept 期间_

- 上游端口 (Upstream Port) 现在已收到 TS2 或具有非 PAD Link 和 Lane 号的 TS1。在此时，上游端口必须决定是否可以使用下游端口发送的 Lane 号建立链路。列出了三种可能的状态转换。

## _退出至"Configuration.Complete"_

- 如果收到两个连续的 TS2 具有相同的非 PAD Link 和 Lane 号，并且它们与为这些 Lane 的 TS1 中传输的 Link 和 Lane 号匹配，则一切正常，下一个子状态将为 Configura‐ tion.Complete。

## _退出至"Configuration.Lanenum.Wait"_

- 如果可以使用接收两个具有相同非 PAD Link 和 Lane 号的连续 TS1 的 Lane 子集来形成已配置的链路，则这些 Lane 发送具有相同 Link 号和新 Lane 号的 TS1。目标是使用较小的 Lane 组来实现工作的链路。在这种情况下，下一个子状态将为
Configuration.Lanenum.Wait。

与下游 Lane 的情况一样，新的 Lane 号必须从零开始并按顺序增加，以覆盖将使用的 Lane。任何未收到 TS1 的 Lane 不能成为该组的一部分，并且会扰乱 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

## _退出至"Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号均为 PAD 的 TS1，则下一个状态将为 Detect。

## **Configuration.Complete**

这是 Configuration 状态中唯一交换 TS2 的子状态。如前所述，TS2 的目的是在链路上的两个设备之间进行握手或确认它们已准备好进入下一状态。因此，这是对迄今为止在 TS1 中交换的 Link 和 Lane 号的最终确认。

**第 14 章：链路初始化与训练**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0547_img2_tight.png" alt="Figure from page 547" width="700">

<a id="sec-13-3"></a>
## 13.3 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

It should be noted that Devices are allowed to change their supported data rates and upconfigure capability when they enter this substate,
but not while in it. This is because Devices record the capabilities of their Link partner from what is advertised in these TS2s, as will be
described in this section.

## **Downstream Lanes** 

## _During Configuration.Complete_ 

TS2s are sent using the Link and Lane numbers that match the received TS1s. The TS2s can have the Upconfigure Capability bit set if the Port
sup‐ ports a x1 Link using Lane 0 and is able to up‐configure the Link.

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes
see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling
cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity.

The Downstream Port is transmitting TS2s and watching for TS2s coming back. For future reference, record the number of FTSs that must be
sent when exiting from the L0s state from the N_FTS field in the incoming TS2s.

## _Exit to “Configuration.Idle”_ 

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching
rate identifiers, and matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2.

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane and this overrides
any previ‐ ously recorded value. The variable used to track speed changes in Recovery, “changed_speed_recovery”, is cleared to zero.

The variable “upconfigure_capable” is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8
consecutive TS2s with the same bit set. Otherwise it’s cleared to zero.

Any Lanes that aren’t configured as part of the Link are no longer associ‐ ated with the LTSSM in progress and must either be: 

- Associated with a new LTSSM or 

- Transitioned to Electrical Idle 

 - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b 

since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it’s also recom‐ mended that
those Lanes leave their Receiver terminations on because they’ll become part of the Link again if it is upconfigured. If the terminations
aren’t left on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete.
Lanes that weren’t part of the Link before can’t become part of it through this process, though.

- b) For the optional crosslink, Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG. 

- c) If the LTSSM goes back to Detect, these Lanes will once again be associated with it. 

- d) No EIOS is needed before Lanes go to Electrical Idle, and the transi‐ tion doesn’t have to happen on Symbol or Ordered Set boundaries. 

## After a 2ms timeout: 

_Exit to “Configuration.Idle”_ 

Next state is Configuration.Idle if the idle_to_rlock_transitioned vari‐ able is less than FFh **and** the current data rate is 8.0 GT/s. 

In this transition, the “changed_speed_recovery” variable is cleared to zero. Also, the “upconfigure_capable” variable may be updated,
though it’s not required to do so, if at least one Lane saw eight consecu‐ tive TS2s with matching Link and Lane numbers (non‐PAD). If the
transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero.

Lanes that aren’t part of the configured Link aren’t associated with the LTSSM in progress and have the same requirements as the non‐timeout
case listed above.

_Exit to “Detect State”_ 

Otherwise, the next state is Detect. 

## **Upstream Lanes** 

_During Configuration.Complete_ 

TS2s are sent using the Link and Lane numbers that match the received TS2s. The TS2s can have the Upconfigure Capability bit set if the Port
sup‐ ports a x1 Link using Lane 0 and is able to up‐configure the Link.
For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes
see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling
cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity.

In this substate, the Upstream Port is receiving TS2s from the Downstream Port, and for future reference, should record the N_FTS field
value number of FTSs that must be sent when exiting from the L0s state from the in the incoming TS2s.

## _Exit to “Configuration.Idle”_ 

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching
rate identifiers, and a matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2.

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane, overriding any
previously recorded value. The variable used to track speed changes in Recovery, “changed_speed_recovery”, is cleared to zero.

The variable “upconfigure_capable” is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8
consecutive TS2s with the same bit set. Otherwise it’s cleared to zero.

Any Lanes that aren’t configured as part of the Link are no longer associ‐ ated with the LTSSM in progress and must either be: 

- Optionally associated with a new crosslink LTSSM (if this feature is sup‐ ported), or 

- Transitioned to Electrical Idle 

 - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b
since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it’s also recommended that
those Lanes leave their Receiver terminations on because they’ll become part of the Link again if it is upconfigured. If they’re not left
on, they must be turned on from when the LTSSM enters the Recov‐ ery.RcvrCfg state all the way through Configuration.Complete. Lanes that
weren’t part of the Link before can’t become part of it through this process, though.

- b) Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐ 

 - HIGH‐IMP‐DC‐NEG[.] 

- c) If the LTSSM goes back to Detect, these Lanes will once again be asso‐ ciated with it. 

- d) No EIOS is needed before Lanes go to Electrical Idle, and the transi‐ tion doesn’t have to happen on Symbol or Ordered Set boundaries. 

After a 2ms timeout: 

## _Exit to “Configuration.Idle”_ 

Next state is Configuration.Idle if the idle_to_rlock_transitioned vari‐ able is less than FFh **and** the current data rate is 8.0 GT/s. 

In this transition, the “changed_speed_recovery” variable is cleared to zero. Also, the “upconfigure_capable” variable may be updated,
though it’s not required to do so, if at least one Lane saw eight consecu‐ tive TS2s with matching Link and Lane numbers (non‐PAD). If the
transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero.

Lanes that aren’t part of the configured Link aren’t associated with the LTSSM in progress and have the same requirements as the non‐timeout
case listed above.

## _Exit to “Detect State”_ 

Otherwise, the next state is Detect. 

## **Configuration.Idle** 

## _During Configuration.Idle_ 

In this substate, the transmitter is sending Idle data and waiting for the minimum number of received Idle data so this Link can transition
to L0. During this time, the Physical Layer reports to the upper layers that the link is operational (Linkup = 1b).

For 8b/10b encoding, the transmitter is sending Idle data on all configured Lanes. Idle data are just data zeros that get scrambled and
encoded.

For 128b/130b encoding, the transmitter sends one SDS Ordered Set on all configured Lanes followed by Idle data Symbols. The first Idle
Symbol on Lane 0 is the first Symbol of the Data Stream.
## _Exit to “L0 State”_ 

If using 8b/10b encoding, the next state is L0 if 8 consecutive Idle data sym‐ bol times are received on all configured Lanes, and 16 symbol
times of idle data were sent after receiving one Idle Symbol.

If using 128b/130b, the next state is L0 if 8 consecutive Idle data are received on all configured Lanes, 16 Idles were sent after receiving
one Idle Symbol, and this state wasn’t entered by a timeout from Configuration.Complete.

- Lane‐to‐Lane de‐skew must be completed before Data Stream processing begins. 

- The Idle Symbols must be received in Data Blocks. 

- If software set the Retrain Link bit in the Link Control register since the last transition to L0 from Recovery or Configuration, the
Downstream Port must set the Link Bandwidth Management bit in the Link Status reg‐ ister to 1b to indicate that this change was not hardware
initiated (auton‐ omous).

- The “idle_to_rlock_transitioned” variable is cleared to 00h on transition to L0. 

## After a 2ms timeout: 

## _Exit to “Detailed Recovery Substates”_ 

If the idle_to_rlock_transitioned variable is less than FFh, the next state is Recovery (Recovery.RcvrLock). Then: 

- a) For 8.0 GT/s, increment idle_to_rlock_transitioned by 1. 

- b) For 2.5 or 5.0 GT/s, set idle_to_rlock_transitioned to FFh. 

- c) NOTE: This variable counts the number of times the LTSSM has tran‐ sitioned from this state to the Recovery state because the sequence
isn’t working. The problem may be that equalization hasn’t been properly adjusted or that the selected speed just isn’t going to work, and
the Recovery state will take steps to address these issues. This variable limits the number of these attempts so as to avoid an endless
loop. If the Link still isn’t working after doing this 256 times (when the count reaches FFh), go back to Detect and start over, hoping for
a better result.

_Exit to “Detect State”_ 

Otherwise (meaning idle_to_rlock = FFh), the next state is Detect. 

## **L0 State** 

This is the normal, fully‐operational Link state, during which Logical Idle, TLPs and DLLPs are exchanged between Link neighbors. L0 is
achieved immediately following the conclusion of the Link Training process. The Physical Layer also notifies the upper layers that the Link
is ready for operation, by setting the LinkUp variable. In addition, the idle_to_rlock_transitioned variable is cleared to 00h.

## _Exit to “Recovery State”_ 

The next state will be Recovery if a change in the Link speed or Link width is indicated, or if the Link partner initiates this by going to
Recovery or Electrical Idle. Let’s consider each of these three cases in a little more detail in the following discussion.

## **Speed Change** 

Two conditions are described in the spec that will cause an automatic change in speed. 

The first is when rates higher than 2.5 GT/s are supported by both partners and the Link is active (Data Link Layer reports DL_Active), or
when one partner requests a speed change in its TS Ordered Sets. For example, a Downstream Port will initiate a speed change if a higher
rate was noted and software writes the Retrain Link bit and after setting the Target Link Speed field (see Figure 14‐ 26 on page 569) to a
different rate than the current rate.

</td>
<td width="50%">

- 如果支持环回的发送器被更高层指示发送 Loopback 位被断言的 TS 有序集，或者所有正在发送和接收 TS1 的 Lane 接收到 2 个连续的设置了 Loopback 位的 TS1。发送设置了该位的 TS1 的端口将成为环回主设备，而接收它们的端口将成为环回从设备。

## _退出到 "Detect 状态"_

- 如果其他条件都不成立，则在 24ms 超时后。

## **Configuration.Linkwidth.Accept**

此时，上游端口现在在其所有 Lane 上发送回具有相同链路号的 TS1 有序集。链路号源自下游端口，上游端口只是将该值反映回其所有 Lane。现在下游端口知道链路宽度（接收相同链路号的 Lane 数）并且必须开始通告 Lane 号。因此领导者（下游端口）继续发送
TS1，但现在使用指定的实际 Lane 号而不是 PAD。此外，所有这些 TS1 将具有相同的链路号。下游和上游 Lane 的详细行为概述如下：

## **下游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 下游端口现在将启动 Lane 号。如果可以从至少一组 Lane 形成链路，并且所有 Lane 都接收两个连续的 TS1 并且都看到相同的链路号，则发送保持相同链路号的 TS1 但现在也分配唯一的非 PAD Lane 号。

## _退出到 "Configuration.Lanenum.Wait"_

- 下游端口不会在 Configuration.Linkwidth.Accept 子状态中停留很长时间。一旦它从上游端口接收到指示链路宽度的必要 TS1，它就会更新所需的任何内部状态信息，开始发送如上所述的具有非 PAD Lane 号的 TS1，并立即转换到
Configuration.Lanenum.Wait 以等待来自上游端口的 Lane 号确认。

## **上游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 上游端口发送 TS1，其中在_所有_接收到具有非 PAD 链路号的 TS1 的 Lane 上的 TS1 中选择并发送一个接收到的链路号。任何剩余的检测到接收器但没有链路号的 Lane 必须发送 Link 和 Lane 号设置为 PAD 的 TS1。

## _退出到 "Configuration.Lanenum.Wait"_

- 上游端口必须响应链路邻居向其提议的 Lane 号。如果可以使用在其 TS1 上发送非 PAD 链路号并接收到两个具有相同链路号和任何非 PAD Lane 号的连续 TS1 的 Lane 形成链路，那么它应发送与相同 Lane 号分配匹配的
TS1（如果可能），或者如果需要则不同（例如使用可选的 Lane 反转）。

**第 14 章：链路初始化与训练**

## **Configuration.Lanenum.Wait**

在讨论 Configuration.Lanenum.Wait 状态之前，一些背景信息可能会有所帮助。Lane 号从零开始按顺序分配到链路可能的最大数量。例如，x8 链路将被分配 Lane 号 0 ‐ 7。端口需要支持与其具有的 Lane 数一样宽的链路和一个小至一个 Lane
的链路。Lane 将始终从 Lane 0 开始，并且必须既是顺序的又是连续的。例如，如果 x8 端口上的某些 Lane 无法工作，则可以选择将其设计为配置 x4 链路，如果是这样，它将需要使用 Lane 0‐3。作为另一个示例，如果 x8 端口的 Lane 2
无法工作，则不可能使用 Lane 0、1、3 和 4 形成 x4 链路，因为 Lane 不是连续的。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

规范中针对 Configuration 子状态重复了许多次的常见时序注意事项。这里不是在每种情况下重复它，只需注意它通常适用于上游和下游端口：

为了避免配置比必要的更小的链路，建议在某些 Lane 上看到错误或丢失块对齐的多 Lane 端口延迟最终链路宽度评估。对于 8b/10b，它应至少再等待两个 TS1，而对于 128b/130b 模式，它应至少等待 34 个 TS1，但任何情况下都不能超过 1ms。其想法是
Lane 在上电或复位后可能需要稳定时间。

## _退出到 "Detect 状态"_

在 2ms 超时后，如果无法配置链路（例如：Lane 0 不工作且 Lane 反转不可用），或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号中都带有 PAD 的 TS1，则链路必须退出到 Detect 状态。

## **下游 Lane**

## _在 Configuration.Lanenum.Wait 期间_

下游端口将继续传输具有非 PAD 链路和 Lane 号的 TS1，直到满足退出条件之一。

## _退出到 "Configuration.Lanenum.Accept"_

如果满足下列任一情况：

- 如果在所有 Lane 上接收到两个连续的 TS1，其链路和 Lane 号与在这些 Lane 上发送的内容匹配。

- 如果任何检测到接收器的 Lane 接收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD 链路号。规范指出，这允许两个端口就相互可接受的链路宽度达成一致。

## _退出到 "Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

上游 Lane

## _在 Configuration.Lanenum.Wait 期间_

上游端口将继续传输具有非 PAD 链路和 Lane 号的 TS1，直到满足退出条件之一。

## _退出到 "Configuration.Lanenum.Accept"_

如果满足下列任一情况：

- 如果任何 Lane 接收到两个连续的 TS2。

- 如果任何 Lane 接收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD 链路号。

请注意，允许上游 Lane 在更改为该子状态之前等待最多 1ms，以防止接收错误或 Lane 之间的偏移影响最终链路配置。

## _退出到 "Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

## **Configuration.Lanenum.Accept**

下游 Lane

## _在 Configuration.Lanenum.Accept 期间_

下游端口现在已接收到具有非 PAD 链路和 Lane 号的 TS1。在这一点上，下游端口必须决定是否可以使用上游端口返回的 Lane 号建立链路。三个可能的状态转换在下面列出。

## _退出到 "Configuration.Complete"_

如果接收到两个连续的 TS1 具有相同的非 PAD 链路和 Lane 号，并且它们与所有 Lane 的 TS1 中传输的链路和 Lane 号匹配，则上游端口已同意下游端口通告的链路和

**第 14 章：链路初始化与训练**

Lane 号，下一个子状态是 Configuration.Complete。或者如果接收到的 TS1 中的 Lane 号与下游端口通告的相反，如果下游端口支持 Lane 反转，它仍然可以使用反转的 Lane 号继续到 Configuration.Complete。

规范指出，反转 Lane 条件严格定义为 Lane 0 接收具有最高 Lane 号（Lane 总数 ‐ 1）的 TS1，并且最高 Lane 号接收 Lane 号为零的 TS1。可以从中理解的是，课堂上偶尔出现的问题的答案：Lane
号是否可以混合而不是顺序的？答案是不可以的，它们必须是从 0 到 n‐1 或从 n‐1 到 0；不支持其他选项。

如果 Configuration 状态是从 Recovery 状态进入的，则可能已请求带宽更改。如果是这样，状态位将更新以报告发生的情况的性质。基本上，系统需要报告此更改是由于链路工作不可靠而启动，还是因为硬件只是在管理链路功率。位更新如下：

- 如果带宽更改是由下游端口因可靠性问题而启动的，则链路带宽管理状态位设置为 1b。

- 如果带宽更改不是由下游端口启动，但两个连续接收的 TS1 中的 Autonomous Change 位清零为 0b，则链路带宽管理状态位设置为 1b。

- 否则，链路自动带宽状态位设置为 1b。

## _退出到 "Configuration.Lanenum.Wait"_

- 如果可以使用部分（但不是全部）接收两个连续的具有相同非 PAD 链路和 Lane 号的 TS1 的 Lane 形成配置的链路，则这些 Lane 使用相同的链路号和新的 Lane 号发送 TS1。目标是使用较小的 Lane 组来实现工作的链路。

新的 Lane 号必须从零开始并按顺序递增以覆盖将使用的 Lane。任何不接收 TS1 的 Lane 不能成为组的一部分，并将破坏 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。例如，如果 8 个 Lane 可用，但 Lane
2 看不到传入的 TS1，则链路不能由需要 Lane 2 的组组成。因此，x8 和 x4 选项将不可用，只有 x1 或 x2 链路是可能的。

## _退出到 "Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 接收到两个连续的具有 PAD 的链路和 Lane 号的 TS1。

## **上游 Lane**

## _在 Configuration.Lanenum.Accept 期间_

- 上游端口现在已接收到具有非 PAD 链路和 Lane 号的 TS2 或 TS1。在这一点上，上游端口必须决定是否可以使用下游端口发送的 Lane 号建立链路。三个可能的状态转换在下面列出。

## _退出到 "Configuration.Complete"_

- 如果接收到两个连续的 TS2 具有相同的非 PAD 链路和 Lane 号，并且它们与这些 Lane 的 TS1 中传输的链路和 Lane 号匹配，则一切正常，下一个子状态将是 Configuration.Complete。

## _退出到 "Configuration.Lanenum.Wait"_

- 如果可以使用接收两个连续的具有相同非 PAD 链路和 Lane 号的 TS1 的 Lane 的子集形成配置的链路，则这些 Lane 使用相同的链路号和新的 Lane 号发送 TS1。目标是使用较小的 Lane 组来实现工作的链路。在这种情况下，下一个子状态将是
Configuration.Lanenum.Wait。

与下游 Lane 的情况一样，新的 Lane 号必须从零开始并按顺序递增以覆盖将使用的 Lane。任何不接收 TS1 的 Lane 不能成为组的一部分，并将破坏 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

## _退出到 "Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 接收到两个连续的具有 PAD 的链路和 Lane 号的 TS1，则下一个状态将是 Detect。

## **Configuration.Complete**

这是 Configuration 状态中交换 TS2 的唯一子状态。如前所述，TS2 的目的是一种握手或确认，即链路上的两个设备已准备好继续到下一个状态。因此这是 TS1 中交换的链路和 Lane 号的最终确认

**第 14 章：链路初始化与训练**

应注意的是，允许设备在进入此子状态时更改其支持的数据速率和向上配置能力，但不能在其中更改。这是因为设备从这些 TS2 中通告的内容记录其链路伙伴的能力，如本节所述。

## **下游 Lane**

## _在 Configuration.Complete 期间_

使用与接收到的 TS1 匹配的链路和 Lane 号发送 TS2。如果端口支持使用 Lane 0 的 x1 链路并能够向上配置链路，则 TS2 可以设置 Upconfigure Capability 位。

对于 8b/10b 编码，离开此子状态时必须完成 Lane 去偏移。此外，如果所有配置的 Lane 看到两个连续的设置了 Disable Scrambling 位的 TS2，则将禁用加扰。发送这些的端口还必须禁用加扰。请注意，由于加扰对信号完整性有必要贡献，因此在
128b/130b 模式下不能禁用加扰。

下游端口正在发送 TS2 并监视返回的 TS2。供将来参考，记录从传入 TS2 的 N_FTS 字段中退出 L0s 状态时必须发送的 FTS 数。

## _退出到 "Configuration.Idle"_

当所有发送 TS2 的 Lane 接收 8 个 TS2，具有匹配的链路和 Lane 号（非 PAD）、匹配的速率标识符以及所有链路中匹配的 Link Upconfigure Capability 位时，下一个状态将是 Configuration.Idle。在接收到一个 TS2
之后，还必须发送至少 16 个 TS2。

如果设备支持大于 2.5 GT/s 的速率，则它必须记录在任何已配置 Lane 上接收到的速率标识符，并且这将覆盖任何先前记录的值。用于跟踪 Recovery 中速度更改的变量 "changed_speed_recovery" 被清零。

变量 "upconfigure_capable" 在以下情况下设置为 1b：如果设备发送 Link Upconfigure Capability 设置为 1b 的 TS2 并接收 8 个连续的设置了相同位的 TS2。否则，它被清零。

未配置为链路一部分的任何 Lane 不再与正在进行的 LTSSM 关联，并且必须是以下之一：

- 与新的 LTSSM 关联，或

- 转换到电气空闲

 - a) 如果那些 Lane 之前已通过 L0 配置为链路的一部分，并且 LinkUp 仍设置为 1b，则出现特殊情况

从那以后。如果链路具有向上配置能力，它们必须保持与同一 LTSSM 关联。对于这种情况，还建议那些 Lane 保持其接收器终端开启，因为如果链路被向上配置，它们将再次成为链路的一部分。如果终端未保持开启，则它们必须在 LTSSM 进入 Recovery.RcvrCfg
状态时一直通过 Configuration.Complete 打开。但是，通过此过程，之前不是链路一部分的 Lane 不能成为其一部分。

- b) 对于可选交叉链路，接收器终端必须介于 ZRX‐HIGH‐IMP‐DC‐POS 和 ZRX‐HIGH‐IMP‐DC‐NEG 之间。

- c) 如果 LTSSM 返回 Detect，这些 Lane 将再次与其关联。

- d) 在 Lane 进入电气空闲之前不需要 EIOS，并且转换不必在符号或有序集边界上发生。

## 在 2ms 超时后：

_退出到 "Configuration.Idle"_

如果 idle_to_rlock_transitioned 变量小于 FFh **且**当前数据速率为 8.0 GT/s，则下一个状态是 Configuration.Idle。

在此转换中，变量 "changed_speed_recovery" 被清零。此外，如果至少一个 Lane 看到八个具有匹配链路和 Lane 号（非 PAD）的连续 TS2，则变量 "upconfigure_capable" 可以更新，尽管不需要这样做。如果发送和接收的 Link
Upconfigure Capability 位为 1b，则将其设置为 1b，否则清零。

未配置链路一部分的 Lane 不与正在进行的 LTSSM 关联，并具有与上面列出的非超时情况相同的要求。

_退出到 "Detect 状态"_

否则，下一个状态是 Detect。

## **上游 Lane**

_在 Configuration.Complete 期间_

使用与接收到的 TS2 匹配的链路和 Lane 号发送 TS2。如果端口支持使用 Lane 0 的 x1 链路并能够向上配置链路，则 TS2 可以设置 Upconfigure Capability 位。

**第 14 章：链路初始化与训练**

对于 8b/10b 编码，离开此子状态时必须完成 Lane 去偏移。此外，如果所有配置的 Lane 看到两个连续的设置了 Disable Scrambling 位的 TS2，则将禁用加扰。发送这些的端口还必须禁用加扰。请注意，由于加扰对信号完整性有必要贡献，因此在
128b/130b 模式下不能禁用加扰。

在此子状态中，上游端口正在从下游端口接收 TS2，供将来参考，应记录从传入 TS2 中的 N_FTS 字段值退出 L0s 状态时必须发送的 FTS 数。

## _退出到 "Configuration.Idle"_

当所有发送 TS2 的 Lane 接收 8 个 TS2，具有匹配的链路和 Lane 号（非 PAD）、匹配的速率标识符以及所有链路中匹配的 Link Upconfigure Capability 位时，下一个状态将是 Configuration.Idle。在接收到一个 TS2
之后，还必须发送至少 16 个 TS2。

如果设备支持大于 2.5 GT/s 的速率，则它必须记录在任何已配置 Lane 上接收到的速率标识符，并且这将覆盖任何先前记录的值。用于跟踪 Recovery 中速度更改的变量 "changed_speed_recovery" 被清零。

变量 "upconfigure_capable" 在以下情况下设置为 1b：如果设备发送 Link Upconfigure Capability 设置为 1b 的 TS2 并接收 8 个连续的设置了相同位的 TS2。否则，它被清零。

未配置为链路一部分的任何 Lane 不再与正在进行的 LTSSM 关联，并且必须是以下之一：

- 可选择与新的交叉链路 LTSSM 关联（如果支持此功能），或

- 转换到电气空闲

 - a) 如果那些 Lane 之前已通过 L0 配置为链路的一部分，并且 LinkUp 自那时起仍设置为 1b，则出现特殊情况。如果链路具有向上配置能力，它们必须保持与同一 LTSSM 关联。对于这种情况，还建议那些 Lane
保持其接收器终端开启，因为如果链路被向上配置，它们将再次成为链路的一部分。如果它们未保持开启，则它们必须在 LTSSM 进入 Recovery.RcvrCfg 状态时一直通过 Configuration.Complete 打开。但是，通过此过程，之前不是链路一部分的 Lane
不能成为其一部分。

- b) 接收器终端必须介于 ZRX‐HIGH‐IMP‐DC‐POS 和 ZRX‐

 - HIGH‐IMP‐DC‐NEG 之间。

- c) 如果 LTSSM 返回 Detect，这些 Lane 将再次与其关联。

- d) 在 Lane 进入电气空闲之前不需要 EIOS，并且转换不必在符号或有序集边界上发生。

## 在 2ms 超时后：

## _退出到 "Configuration.Idle"_

如果 idle_to_rlock_transitioned 变量小于 FFh **且**当前数据速率为 8.0 GT/s，则下一个状态是 Configuration.Idle。

在此转换中，变量 "changed_speed_recovery" 被清零。此外，如果至少一个 Lane 看到八个具有匹配链路和 Lane 号（非 PAD）的连续 TS2，则变量 "upconfigure_capable" 可以更新，尽管不需要这样做。如果发送和接收的 Link
Upconfigure Capability 位为 1b，则将其设置为 1b，否则清零。

未配置链路一部分的 Lane 不与正在进行的 LTSSM 关联，并具有与上面列出的非超时情况相同的要求。

## _退出到 "Detect 状态"_

否则，下一个状态是 Detect。

## **Configuration.Idle**

## _在 Configuration.Idle 期间_

在此子状态中，发送器正在发送空闲数据并等待接收空闲数据的最小数量，以便此链路可以转换到 L0。在此期间，物理层向上层报告链路处于运行状态（Linkup = 1b）。

对于 8b/10b 编码，发送器在所有已配置 Lane 上发送空闲数据。空闲数据只是被加扰和编码的数据零。

对于 128b/130b 编码，发送器在所有已配置 Lane 上发送一个 SDS 有序集，后跟空闲数据符号。Lane 0 上的第一个空闲符号是数据流的第一个符号。

**第 14 章：链路初始化与训练**

## _退出到 "L0 状态"_

如果使用 8b/10b 编码，则下一个状态是 L0，如果在所有已配置 Lane 上接收到 8 个连续的空闲数据符号时间，并且在接收到一个空闲符号之后发送了 16 个符号时间的空闲数据。

如果使用 128b/130b，则下一个状态是 L0，如果在所有已配置 Lane 上接收到 8 个连续的空闲数据，在接收到一个空闲符号之后发送了 16 个空闲，并且此状态不是通过 Configuration.Complete 的超时进入的。

- 数据流处理开始之前必须完成 Lane 到 Lane 去偏移。

- 必须在数据块中接收空闲符号。

- 如果软件自上次从 Recovery 或 Configuration 转换到 L0 以来在 Link Control 寄存器中设置了 Retrain Link 位，则下游端口必须将 Link Status 寄存器中的 Link Bandwidth Management 位设置为
1b，以指示此更改不是硬件发起的（自动）。

- 转换到 L0 时，变量 "idle_to_rlock_transitioned" 清零为 00h。

## 在 2ms 超时后：

## _退出到 "Recovery 子状态详解"_

如果 idle_to_rlock_transitioned 变量小于 FFh，则下一个状态是 Recovery (Recovery.RcvrLock)。然后：

- a) 对于 8.0 GT/s，idle_to_rlock_transitioned 递增 1。

- b) 对于 2.5 或 5.0 GT/s，将 idle_to_rlock_transitioned 设置为 FFh。

- c) 注意：此变量计算 LTSSM 因序列未工作而从此状态转换到 Recovery 状态的次数。问题可能是均衡尚未正确调整或所选速度根本不起作用，Recovery 状态将采取措施解决这些问题。此变量限制这些尝试的次数以避免无限循环。如果在进行此操作 256 次（当计数达到
FFh 时）后链路仍不工作，则返回 Detect 并重新开始，希望获得更好的结果。

_退出到 "Detect 状态"_

否则（即 idle_to_rlock = FFh），下一个状态是 Detect。

## **L0 状态**

这是正常的、完全运行的链路状态，在此期间逻辑空闲、TLP 和 DLLP 在链路邻居之间交换。L0 在链路训练过程结束后立即实现。物理层还通过设置 LinkUp 变量来通知上层链路已准备好运行。此外，变量 idle_to_rlock_transitioned 清零为 00h。

## _退出到 "Recovery 状态"_

如果指示链路速度或链路宽度的变化，或者如果链路伙伴通过转到 Recovery 或电气空闲来启动此操作，则下一个状态将是 Recovery。让我们在下面的讨论中更详细地考虑这三种情况中的每一种。

## **速度更改**

规范中描述了将导致自动速度更改的两种条件。

第一种是当两个伙伴都支持高于 2.5 GT/s 的速率并且链路处于活动状态（数据链路层报告 DL_Active），或者当一个伙伴在其 TS 有序集中请求速度更改时。例如，如果注意到更高速率并且软件写入 Retrain Link 位并在将 Target Link Speed
字段（参见第 569 页的图 14‐26）设置为与当前速率不同的速率之后，下游端口将启动速度更改。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0554_img1_tight.png" alt="Figure from page 554" width="700">

<a id="sec-13-4"></a>
## 13.4 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

The second condition is when both partners support 8.0 GT/s and one of them wants to perform Tx Equalization. In both conditions the
directed_speed_change variable will be set to 1b and the changed_speed_recovery bit will be cleared to 0b.

A Port will not attempt a speed change (the directed_speed_change variable won’t be set) if a rate higher than 2.5 GT/s has never been seen
as advertised by the other Port in the Configuration.Complete or Recovery.RcvrCfg substates.
_Figure 14‐25: Link Control Register_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


## _Figure 14‐26: Link Control 2 Register_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


## **Link Width Change** 

An upper layer would normally only direct a Link width reduction if upconfigure_capable has been set to 1b because otherwise the Link won’t
be able to go back to the original width. If the Hardware Autonomous Width Dis‐ able bit is set to 1b a Port can only reduce the width in an
effort to correct a reli‐ ability problem. An upper layer can only initiate an increase in Link width if the Link partner advertised that it
was upconfigure capable and the Link is not already at its maximum width. Apart from these guidelines, the decision crite‐ ria for changing
the Link width are not given in the spec and are therefore implementation specific.

## **Link Partner Initiated** 

The spec describes three possibilities for this case. 

First, if Electrical Idle is detected or inferred (see Table 14‐10 on page 596) on all Lanes without first receiving an EIOS on any Lane,
the Port may choose to enter Recovery or stay in L0. If errors result from this condition, the Port may be directed to Recovery by means
such as setting the Retrain Link bit.

The second case happens when TS1s or TS2s are received (or an EIEOS for 128b/ 130b) on any configured Lanes, indicating that the Link
partner has already entered Recovery. Since both of these cases are initiated by the Link partner, the Transmitter is allowed to complete
any TLP or DLLP currently in progress.

Finally, if an EIOS is received on any Lane, indicating a Link power manage‐ ment change, but the Receiver doesn’t support L0s and hasn’t
been directed to L1 or L2, then going to Recovery is the only option.

## _Exit to “L0s State”_ 

The next state will be L0s for a Transmitter that’s been instructed to initiate it, or for a Receiver that sees an EIOS. Interestingly, the
LTSSM states for the Transmitter and Receiver of the Port can be different now, because one can be in L0s while the other is still in L0.

- Transmitters go to L0s when directed, if they implement L0s, and send EIOS to initiate the change. 

- Receivers go to L0s when an EIOS is seen on any Lane. However, if the Receiver doesn’t implement L0s and hasn’t been directed to L1 or L2,
this will be seen as a problem and the next state will be “Recovery State” instead.
## _Exit to “Rx_L0s.Entry”_ 

- The next state will be L1 when one Link partner is directed to initiate this and sends one EIOS on all Lanes (two EIOSs if the speed is
5.0 GT/s) and receives an EIOS on any Lane. Note that both Link partners must have already agreed to enter L1 beforehand and that a Data
Link Layer hand‐ shake is needed to ensure that both are ready. For more detail on how this works, see the section called “Introduction to
Link Power Management” on page 733.

## _Exit to “L2 State”_ 

The next state will be L2 when one Link partner is directed to initiate this and sends one EIOS on all Lanes (two EIOSs if the speed is 5.0
GT/s) and receives an EIOS on any Lane. Note that both Link partners must have already agreed to enter L2 beforehand and that a handshake is
needed to ensure that both are ready. For more detail on how this works, see the section called “Introduction to Link Power Management” on
page 733.

## **Recovery State** 

If everything works as expected, the Link trains to the L0 state without ever going into the Recovery state. But we’ve already discussed two
reasons why it might not. First, if the correct Symbol pattern isn’t seen in Configuration.Idle, the LTSSM goes to Recovery in an effort to
correct signaling problems by, for example, adjusting equalization values. Secondly, once L0 is reached with a data rate of 2.5 GT/s and
both devices support higher speeds, the LTSSM goes to Recovery and attempts to change the Link speed to the highest commonly‐sup‐
ported/advertised speed. In this state, Bit Lock and either Symbol Lock or Block Alignment is re‐acquired and the Link is de‐skewed again.
The Link and Lane Numbers should remain unchanged unless the Link width is being changed. In that case, the LTSSM passes through the
Configuration state where Link width is re‐negotiated.

NOTE: To simplify the discussion and avoid repeating the same text many times, the term “Lock” will be used here to mean the combination of
Bit Lock and either Symbol Lock for 8b/10b encoding or Block Alignment for 128b/130b encoding. A Receiver must acquire this Lock to be able
to recognize Symbols, Ordered Sets and Packets.

## **Reasons for Entering Recovery State** 

- Exiting the L1 state; Required because there is no fast training option (like sending FTS ordered sets) when exiting L1 

- Exiting L0s if the receiver fails to achieve Lock from the FTS ordered sets in the required time, the Link must transition to Recovery 

- From L0 if: 

- A higher data rate is available when initial training completes. 

- A Link speed or width change has been requested (for power management or because the current speed or width is unreliable). 

- Software sets the Retrain Link bit in the Link Control Register (see Figure 14‐71 on page 644) in an effort to clear transmission
problems.

- An error condition such as a Replay Num Roll‐over event associated with the Ack/Nak protocol of the Data Link Layer automatically causes
the Physical Layer logic to retrain the Link.

- Receiver sees TS1s or TS2s on any configured Lane, meaning that the neighbor must have entered Recovery. 

- Receiver sees Electrical Idle on all configured Lanes but did not first receive the Electrical Idle Ordered Set. 

## **Initiating the Recovery Process** 

Either Port can initiate Recovery by sending TS1s to its neighbor. When a Port sees incoming TS1s it knows that the other Port has entered
Recovery, so it also goes into Recovery and returns TS1s. Both receivers first use the TS1s to reac‐ quire Lock (if necessary) and then
proceed to the other substates as needed. This is shown in Figure 14‐27 on page 573. A detailed description of what hap‐ pens in the
substates is provided in the sections that follow.
_Figure 14‐27: Recovery State Machine_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


## **Detailed Recovery Substates** 

## _During Recovery.RcvrLock_ 

- Regardless of the speed, Transmitters send TS1s on all configured Lanes using the same Link and Lane numbers that were set in the
Configuration state. If the purpose of entering the Recovery state was to change speeds, the speed_change bit in the Data Rate Identifier
Symbol will be set to 1b in the TS1s from the initiating device and the internal variable directed_speed_change is set to 1b. This same
variable will be set in the other device if the speed_change bit is set in the incoming TS1s. In addition, The successful_speed_negotiation
variable is cleared to 0b on entry to this substate.

In this substate, an Upstream Port is allowed to specify the de‐emphasis level the Downstream Port should use when operating at 5GT/s. This
is accomplished by setting the Selectable De‐emphasis bit in its TS1s to the desired value. It’s possible that bit errors on the Link will
prevent this infor‐ mation from reaching the Downstream Port, so the Upstream Port is allowed to request the de‐emphasis level again when
going to the Recovery state for a speed change. If the Downstream Port plans to use the requested level, it must record the value of the
Selectable De‐emphasis bit while in this state.

A new transmitter voltage can also be applied upon entry to this state. The Transmit Margin field in the Link Control 2 register is sampled
on entry to this substate and remains in effect until a new value is sampled on another entry to this substate from L0, L0s, or L1.

A Downstream Port that wants to change the rate to 8.0 GT/s and redo the equalization must send EQ TS1s with the speed_change bit set and
adver‐ tising the 8.0 GT/s rate. If an Upstream Port receives 8 consecutive EQ TS1s or EQ TS2s with the speed_change bit set to 1b and the
8.0 GT/s rate sup‐ ported, it is expected to advertise the 8.0 GT/s rate, too, unless it has con‐ cluded that there are reliability problems
at that rate that can’t be fixed with equalization. Note that a Port is allowed to change its advertised data rates when entering this
state, but only those rates that can be supported reliably. And apart from the conditions described here, a device is not allowed to change
its supported data rates in this substate or in Recovery.RcvrCfg or Recovery.Equalization.

## _Exit to “Recovery.RcvrCfg”_ 

- The next state will be Recovery.RcvrCfg if 8 consecutive TS1s or TS2s are received whose Link and Lane numbers match what is being sent
_and_ their speed_change bit is equal to the directed_speed_change variable _and_ their EC field is 00b (if the current data rate is 8.0
GT/s).

- If the Extended Synch bit is set, a minimum of 1024 TS1s in a row must be sent before going to Recovery.RcvrCfg. 

- If this substate was entered from Recovery.Equalization, the Upstream Port must compare the equalization coefficients or preset received
by all Lanes against the final set of coefficients or preset that was accepted in Phase 2 of the equalization process. If they don’t match,
it sets the Request Equalization bit in the TS2s it sends.

## _Exit to “Recovery.Equalization”_ 

When the data rate is 8.0 GT/s, the Lanes must establish the proper equal‐ ization parameters to obtain good signal integrity. This section
does not apply for lower speeds. Just because the Link is running at 8.0 GT/s, it does not go through the Recovery.Equalization substate
every time Recovery is entered. Recovery.Equalization is only entered if one of these conditions is met:

- If the start_equalization_w_preset variable is set to 1b then:

</td>
<td width="50%">

第二种情况是当两个端口都支持 8.0 GT/s，并且其中之一希望执行 Tx 均衡 (Tx Equalization) 时。在这两种情况下，directed_speed_change 变量将被设置为 1b，changed_speed_recovery 位将被清除为 0b。

如果从未在 Configuration.Complete 或 Recovery.RcvrCfg 子状态中看到对端 Port 通告过高于 2.5 GT/s 的速率，那么该 Port 将不会尝试速率变更（不会设置 directed_speed_change 变量）。
## ## **链路宽度变更**

上层通常只有在 upconfigure_capable 被设置为 1b 时才会指示减小链路宽度 (Link width reduction)，否则链路将无法恢复为原始宽度。如果 Hardware Autonomous Width Disable 位设置为 1b，则 Port
只能通过减小宽度来尝试纠正可靠性问题。上层只有在链路对端已通告其支持 upconfigure 并且链路尚未达到其最大宽度时，才能启动链路宽度的增加。除了这些指导原则之外，更改链路宽度的决策标准在规范中并未给出，因此属于实现相关的。

## **由链路对端启动**

规范为此情况描述了三种可能性。

第一种情况是，如果在任何 Lane 上未先收到 EIOS，就在所有 Lane 上检测到或推断出 Electrical Idle（参见 596 页的 Table 14‐10），则该 Port 可以选择进入 Recovery 状态或保持在 L0。如果此条件导致错误，则可以通过设置
Retrain Link 位等手段将 Port 引导至 Recovery。

第二种情况是，当在任何已配置的 Lane 上收到 TS1 或 TS2（或 128b/130b 的 EIEOS）时，表明链路对端已经进入 Recovery 状态。由于这两种情况都是由链路对端发起的，因此允许发送器 (Transmitter) 完成当前正在进行的任何 TLP 或
DLLP。

最后，如果在任何 Lane 上收到 EIOS，表明发生了链路电源管理变化，但接收器 (Receiver) 不支持 L0s 并且也未被引导至 L1 或 L2，那么进入 Recovery 状态是唯一的选择。

## _退出至 "L0s 状态"_

对于已被指示启动 L0s 的发送器，或已看到 EIOS 的接收器，下一状态将是 L0s。有趣的是，此时 Port 的发送器和接收器的 LTSSM 状态可以不同，因为一方可能处于 L0s 状态，而另一方仍处于 L0 状态。

- 发送器在指示时（如果实现了 L0s）进入 L0s，并发送 EIOS 来启动该变更。

- 接收器在任何 Lane 上看到 EIOS 时进入 L0s。但是，如果接收器未实现 L0s 并且未被引导至 L1 或 L2，这将被视为问题，下一状态将是 "Recovery 状态"。
## _退出至 "Rx_L0s.Entry"_

- 当一个链路对端被指示启动此状态并向所有 Lane 发送一个 EIOS（速率为 5.0 GT/s 时为两个 EIOS）并且在任何 Lane 上接收到 EIOS 时，下一状态将为 L1。请注意，两个链路对端必须事先就进入 L1 达成一致，并且需要数据链路层 (Data Link
Layer) 的握手以确保双方都已准备好。有关其工作原理的更多详细信息，请参见 733 页 "Introduction to Link Power Management" 一节。

## _退出至 "L2 状态"_

当一个链路对端被指示启动此状态并向所有 Lane 发送一个 EIOS（速率为 5.0 GT/s 时为两个 EIOS）并且在任何 Lane 上接收到 EIOS 时，下一状态将为 L2。请注意，两个链路对端必须事先就进入 L2
达成一致，并且需要握手以确保双方都已准备好。有关其工作原理的更多详细信息，请参见 733 页 "Introduction to Link Power Management" 一节。

## **Recovery 状态**

如果一切如预期工作，链路将训练到 L0 状态而无需进入 Recovery 状态。但我们已经讨论了可能并非如此的两个原因。首先，如果在 Configuration.Idle 中未看到正确的 Symbol 模式，LTSSM 将进入 Recovery
状态，以通过例如调整均衡值的方式来尝试纠正信号问题。其次，一旦以 2.5 GT/s 的数据速率达到 L0，并且两个设备都支持更高速度，LTSSM 将进入 Recovery 状态并尝试将链路速度更改为最高共同支持/通告的速度。在此状态下，将重新获取 Bit Lock 以及
Symbol Lock 或 Block Alignment，并对链路进行重新去偏斜 (de-skew)。链路号和 Lane 号应保持不变，除非正在更改链路宽度。在这种情况下，LTSSM 将通过 Configuration 状态重新协商链路宽度。

注意：为了简化讨论并避免多次重复相同文本，此处将使用术语 "Lock" 来表示 Bit Lock 与 Symbol Lock（针对 8b/10b 编码）或 Block Alignment（针对 128b/130b 编码）的组合。接收器必须获取此 Lock 才能识别
Symbol、有序集 (Ordered Sets) 和数据包 (Packets)。

## **进入 Recovery 状态的原因**

- 退出 L1 状态；这是必需的，因为退出 L1 时没有像发送 FTS 有序集那样的快速训练选项

- 退出 L0s 时，如果接收器未能在规定时间内从 FTS 有序集获得 Lock，则链路必须转移至 Recovery

- 从 L0 进入，如果：

 - 初始训练完成时，存在更高的数据速率可用。

 - 已请求链路速度或宽度变更（用于电源管理或当前速度/宽度不可靠）。

 - 软件设置 Link Control 寄存器中的 Retrain Link 位（参见 644 页 Figure 14‐71），以尝试清除传输问题。

 - 错误条件（例如与数据链路层 Ack/Nak 协议关联的 Replay Num Roll-over 事件）会自动导致物理层 (Physical Layer) 逻辑重新训练链路。

 - 接收器在任何已配置的 Lane 上看到 TS1 或 TS2，意味着相邻设备已进入 Recovery。

 - 接收器在所有已配置的 Lane 上看到 Electrical Idle，但并未先收到 Electrical Idle Ordered Set。

## **启动 Recovery 过程**

任一 Port 都可以通过向其相邻设备发送 TS1 来启动 Recovery。当 Port 看到传入的 TS1 时，它知道另一个 Port 已进入 Recovery，因此它也会进入 Recovery 并返回 TS1。两个接收器首先使用 TS1 重新获取
Lock（如有必要），然后根据需要继续进行其他子状态。这在 573 页的 Figure 14‐27 中显示。子状态中发生什么的详细描述在后续各节中提供。
## **详细的 Recovery 子状态**

## _在 Recovery.RcvrLock 期间_

- 无论速度如何，发送器在所有已配置的 Lane 上使用在 Configuration 状态中设置的相同链路号和 Lane 号发送 TS1。如果进入 Recovery 状态的目的是更改速度，则在启动设备的 TS1 中，Data Rate Identifier Symbol 中的
speed_change 位将被设置为 1b，并且内部变量 directed_speed_change 被设置为 1b。如果传入 TS1 中的 speed_change
位置位，则该变量也将在另一个设备中设置。此外，进入此子状态时，successful_speed_negotiation 变量被清除为 0b。

在此子状态中，允许上游端口 (Upstream Port) 指定当以 5GT/s 运行时下游端口 (Downstream Port) 应使用的去加重 (de-emphasis) 电平。这是通过将其 TS1 中的 Selectable De-emphasis
位设置为所需值来实现的。链路上的位错误可能会阻止此信息到达下游端口，因此允许上游端口在为速度变更进入 Recovery 状态时再次请求去加重电平。如果下游端口计划使用所请求的电平，则它必须在此状态下记录 Selectable De-emphasis 位的值。

进入此状态时也可以应用新的发送器电压。Link Control 2 寄存器中的 Transmit Margin 字段在进入此子状态时被采样，并保持有效直到在从 L0、L0s 或 L1 再次进入此子状态时采样到新值。

希望将速率更改为 8.0 GT/s 并重新执行均衡的下游端口必须发送 speed_change 位置位的 EQ TS1 并通告 8.0 GT/s 速率。如果上游端口接收到 8 个连续的 speed_change 位设置为 1b 且支持 8.0 GT/s 速率的 EQ TS1 或
EQ TS2，则预计它也将通告 8.0 GT/s 速率，除非它已确定该速率存在无法通过均衡修复的可靠性问题。请注意，允许 Port 在进入此状态时更改其通告的数据速率，但只能更改那些可以可靠支持的速率。除了此处描述的条件之外，设备不允许在此子状态或
Recovery.RcvrCfg 或 Recovery.Equalization 中更改其支持的数据速率。

## _退出至 "Recovery.RcvrCfg"_

- 如果接收到 8 个连续的 TS1 或 TS2，其链路号和 Lane 号与正在发送的匹配 _并且_ 它们的 speed_change 位等于 directed_speed_change 变量 _并且_ 它们的 EC 字段为 00b（如果当前数据速率为 8.0
GT/s），则下一状态将为 Recovery.RcvrCfg。

- 如果设置了 Extended Synch 位，则在进入 Recovery.RcvrCfg 之前必须发送至少 1024 个连续的 TS1。

- 如果此子状态是从 Recovery.Equalization 进入的，则上游端口必须将所有 Lane 接收到的均衡系数或预设值与均衡过程第 2 阶段接受的最终系数或预设值集合进行比较。如果它们不匹配，它将在其发送的 TS2 中设置 Request Equalization
位。

## _退出至 "Recovery.Equalization"_

当数据速率为 8.0 GT/s 时，Lane 必须建立适当的均衡参数以获得良好的信号完整性。本节不适用于较低的速度。仅仅因为链路以 8.0 GT/s 运行，它并不会在每次进入 Recovery 时都经过 Recovery.Equalization
子状态。仅当满足以下条件之一时才会进入 Recovery.Equalization：

- 如果 start_equalization_w_preset 变量设置为 1b，则：

 - a) 上游端口在切换到 8.0 GT/s 之前，从其看到的 8 个连续 TS2 中注册了预设值。它必须使用发送器预设，并且可以可选地使用其接收到的接收器预设。

 - b) 下游端口必须在切换到 8.0 GT/s 时立即使用其 Lane Equalization Control 寄存器中定义的发送器预设，并且可以可选地使用其中找到的接收器预设。

- 否则（变量未设置），发送器必须使用在均衡过程上一次执行时它们所同意的系数设置。

 - a) 如果 8 个连续的传入 TS1 具有与正在发送的链路号和 Lane 号匹配、speed_change 位为 0b、但 EC 位为非零的值，则上游端口的下一状态将为
Recovery.Equalization，表明下游端口希望重做均衡过程的某些部分。规范指出，下游端口可以在软件或实现特定的指示下执行此操作。与往常一样，执行此操作所花费的时间不得导致事务超时错误，这实际上意味着下游端口需要确保在执行此步骤之前没有进行中的事务。

 - a) 如果被指示，下游端口的下一状态将为 Recovery.Equalization，只要此状态不是从 Configuration.Idle 或 Recovery.Idle 进入的。规范指出，在发送 EC 值为非零的 TS1 之前，不应发送超过两个 EC=00b 的
TS1，以请求重做均衡。

否则，经过 24ms 超时后：

## _退出至 "Recovery.RcvrCfg"_

如果同时满足以下两个条件，则下一状态将为 Recovery.RcvrCfg：

- 接收到 8 个连续的 TS1 或 TS2，其链路号和 Lane 号与正在发送的匹配，并且其 speed_change 位等于 1b。

- 并且当前数据速率已经高于 2.5 GT/s，或者至少在 TS1 或 TS2 中显示支持更高速率。

## _退出至 "Recovery.Speed"_

如果满足以下两个条件中的另一个，则下一状态将为 Recovery.Speed：

- 如果当前速度设置为高于 2.5 GT/s 但自进入 Recovery 以来无法正常工作（通过将变量 changed_speed_recovery 清零为 0b 来指示）。离开 Recovery.Speed 后的新速率将回退到 2.5 GT/s。

- 如果 changed_speed_recovery 变量设置为 1b，表明高于 2.5 GT/s 的速率已经可以工作，但链路无法以新协商的速率运行。结果，链路将恢复为从 L0 或 L1 进入 Recovery 时的速率。

## _退出至 "Configuration 状态"_

否则，如果未请求速度变更（directed_speed_change 变量 = 0b 并且 TS1 和 TS2 中的 speed_change 位为 0b），或者最高共同支持的数据速率为 2.5 GT/s，则 LTSSM 将返回到 Configuration。

## _退出至 "Detect 状态"_

最后，如果其他条件都不满足，则下一状态将为 Detect。

## **速度变更示例**

规范在此子状态的讨论中包含了一个速度变更的示例。场景是两个链路相邻设备（设备 A 和设备 B）正在退出复位，两者都支持 5.0 GT/s 和 8.0 GT/s 速率。

首先，链路将使用 Gen1 速率 2.5 GT/s 自动训练到 L0。（此行为很可能会在未来的规范版本中继续存在，因为它提供了与旧设计的向后兼容性。）

在我们的示例中，两个设备都支持更高的速率，这由训练期间其 TS 有序集中的 Rate Identifier 字段指示。两个设备都注意到对方支持更高的速率，其中之一（设备 A）将首先将其 directed_speed_change 变量设置为 1b。发生这种情况时，它将进入
Recovery.RcvrLock 并发送 speed_change 位置位的 TS1。如果所需速率为 8.0 GT/s 且之前未使用过，则设备将交换 EQ TS1 以传递要使用的 TX 均衡器预设，而不是发送普通 TS1。

设备 B 看到传入的 TS1，并转换到 Recovery.RcvrLock。当它识别出 8 个连续的 speed_change 位置位的 TS1 时，它通过在其自己的 TS1 中设置 speed_change 位进行响应并进入 Recovery.Speed。设备 A
等待该响应，当看到 8 个连续的 speed_change 位置位的 TS1 时，它进入 Recovery.RcvrCfg，然后进入 Recovery.Speed。在该子状态中，发送器被置为 Electrical Idle，速率被更改为最高共同支持的速率，并且
directed_speed_change 变量被清除。

经过超时周期后，两个设备都转移回 Recovery.RcvrLock，并且发送器使用新速度（在本例中为 8.0 GT/s）重新激活。它们现在再次发送 TS1，这次 speed_change 位被清除为 0b。如果新速度工作正常，它们将转移到 Recovery.RcvrCfg
并返回 L0。但是，如果设备 B 存在问题，例如未能获得 Bit Lock，则它将在此子状态中超时并返回到 Recovery.Speed。设备 A 此时可能
已经转移到 Recovery.RcvrCfg，但是当它现在看到 Electrical Idle（指示相邻设备已返回到 Recovery.Speed）时，它也将返回到该状态。返回到 Recovery.Speed 会导致两个设备都恢复到进入 Recovery 时的速度（在本例中为
2.5 GT/s），并返回到 Recovery.RcvrLock。

作为对该发展的响应，设备 A 可能会再次设置 directed_speed_change 并第二次尝试该过程。如果再次失败，设备 A 可以选择从其通告列表中删除 8.0 GT/s 速率并在没有该速率的情况下再次尝试速度变更。由于现在最高公共速率为 5.0
GT/s，如果此尝试成功，则速率将最终为 5.0 GT/s。如果仍然无效，设备 A 可能会放弃尝试使用更高的速率。设备如何以及何时选择更改其通告的速率或放弃尝试使更高速率工作，在规范中并未给出，将取决于具体实现。

## **链路均衡概述**

本节提供了均衡过程的概述，并为读者理解详细的子状态机行为做好准备（如果他们对此感兴趣）。

使用更高的链路速度会比较低的数据速率产生更多的信号失真。为了补偿这种失真并最大限度地减少系统设计人员的工作和成本，3.0 规范增加了对发送器均衡 (Transmitter Equalization)
的要求。与较低速率的固定去加重值不同（去加重实际上本身就是一种简单的发送器均衡形式），新方法使用主动握手过程来使发送器与实际信号环境相匹配。在此过程中，每个接收器 Lane 评估传入信号的质量，并建议链路对端应使用的 Tx 均衡参数，以满足信号质量要求。

链路均衡过程在第一次更改为 8.0 GT/s 数据速率之后执行。规范强烈建议自主启动均衡过程（在硬件中自动启动），但并不要求这样做。如果组件选择不使用自主机制，则必须使用基于软件的机制。如果任一端口无法通过此过程实现必要的信号质量，LTSSM 将得出该速率无法工作的结论，并返回到
Recovery.Speed 以请求较低的速率。

该过程涉及多达四个阶段，如下文所述。一旦速度已更改为 8.0 GT/s，正在使用的当前均衡阶段由 TS1 中的 EC（Equalization Control）字段指示，如 Figure 14‐28 所示。

## **Phase 0**

当下游端口准备好从较低速率更改为 8.0 GT/s 速率时，它进入 Recovery.RcvrCfg 子状态，并使用 EQ TS2 向上游端口发送 Tx 预设和 Rx 提示，如 510 页 "TS1 and TS2 Ordered Sets" 中所述。（请注意，如果链路已经以
8.0 GT/s 运行，则跳过此阶段。）下游端口 (DSP) 根据其 Equalization Control 寄存器（参见 579 页 Figure 14‐29）的内容发送 Tx 预设值。这突出的一点是，每个 Lane 可以具有不同的均衡值。下游端口将对其自己的发送器使用
DSP 值，并可选地用于其接收器，并将 USP 值发送到上游端口，以供其在切换到更高速度时使用。
_Table 14‐8: Tx Preset Encodings_

|**Encoding**|**De‐emphasis**|**Preshoot**|
|---|---|---|
|0000b|‐6|0|
|0001b|‐3.5|0|
|0010b|‐4.5|0|
|0011b|‐2.5|0|
|0100|0|0|

## **PCI Express Technology**

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

一旦速率确实改变，下游端口从 Phase 1 开始，并发送 EC = 01b 的 TS1。然后它等待上游端口以相同的 EC 值进行响应。

同时，上游端口从 Phase 0 开始，如 581 页 Figure 14‐30 所示，并发送回显其早先从
EQ TS1 和 EQ TS2 接收到的预设值的 TS1。如果支持，它将使用所请求的 Tx 预设，并可选地使用 Rx 提示。USP 允许在评估传入信号之前等待 500ns，但一旦它能够识别两个连续的 TS1，就准备好进行下一步。这意味着信号质量满足最低 BER
10[‐4]（即误码率小于万分之一）。随后 USP 在其 TS1 中设置 EC=01b，从而进入 Phase 1 并将下一步的控制权交给 DSP。

**Phase 1**

</td>
</tr></tbody></table>

<p align="center"><b>Figure 14‐25: Link Control Register</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐26: Link Control 2 Register</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐27: Recovery State Machine</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐28: EC Field in TS1s and TS2s for 8.0 GT/s</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐29: Equalization Control Registers</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐30: Equalization Process: Starting Point</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-13-5"></a>
## 13.5 Physical Layer - Electrical | 物理层 - 电气

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

- a) Upstream Port registered preset values from the 8 consecutive TS2s it saw prior to changing to 8.0 GT/s. It must use the Transmitter
presets and it may optionally use the Receiver presets it received.
 - b) Downstream Port must use the Transmitter presets defined in its Lane Equalization Control register as soon as it changes to 8.0 GT/s
and it may optionally use the Receiver presets found there.

- Else (the variable is not set), Transmitters must use the coefficient settings they agreed to when the equalization process was last
executed.

 - a) Upstream Port’s next state will be Recovery.Equalization if 8 consecu‐ tive incoming TS1s have Link and Lane numbers that match those
being sent and the speed_change bit is 0b, but the EC bits are non‐ zero, indicating that the Downstream Port wishes to redo some parts of
the equalization process. The spec notes that a Downstream Port could do this under software or implementation‐specific direction. As
always, the time it takes to do this must not be allowed to cause transaction timeout errors, which really means the Downstream Port would
need to ensure there were no transactions in flight before tak‐ ing this step.

 - a) Downstream Port’s next state will be Recovery.Equalization if directed, as long as this state wasn’t entered from Configuration.Idle
or Recovery.Idle. The spec points out that no more than two TS1s whose EC=00b should be sent before sending TS1s with a non‐zero EC value to
request that equalization be redone.

Otherwise, after a 24ms timeout: 

## _Exit to “Recovery.RcvrCfg”_ 

The next state will be Recovery.RcvrCfg if both: 

- 8 consecutive TS1s or TS2s are received whose Link and Lane num‐ bers match what it being sent and their speed_change bit is equal to 1b. 

- And either the current data rate is already higher than 2.5 GT/s, or at least a higher rate is shown to be supported in the TS1s or TS2s. 

## _Exit to “Recovery.Speed”_ 

The next state will be Recovery.Speed if other of the two following condi‐ tions are met: 

- If the current speed is set higher than 2.5 GT/s but isn’t working since entering Recovery (indicated by clearing the variable
changed_speed_recovery to 0b). The new rate after leaving Recov‐ ery.Speed will drop back to 2.5 GT/s.

- If the changed_speed_recovery variable is set to 1b, indicating that a higher rate than 2.5 GT/s is already working but the Link was
unable to operate at a new negotiated rate. As a result, the operating speed will revert to what it was when Recovery was entered from L0 or
L1.

## _Exit to “Configuration State”_ 

Otherwise, the LTSSM will return to Configuration if a speed change is not requested (directed_speed_change variable = 0b and the
speed_change bit in the TS1s and TS2s is 0b), or if the highest commonly supported data rate is 2.5 GT/s.

## _Exit to “Detect State”_ 

Finally, if none of the other conditions are true, the next state will be Detect. 

## **Speed Change Example** 

The spec includes an example of a speed change in the discussion of this sub‐ state. The scenario is two Link neighbors (device A and device
B) that are com‐ ing out of reset, both of which support the 5.0 GT/s and 8.0 GT/s rates.

To begin with, the Link will automatically train to L0 using the Gen1 rate of 2.5 GT/s. (This behavior is likely to continue in future spec
versions because it pro‐ vides backward compatibility with older designs.)

In our example both devices support higher rates and this is indicated by the Rate Identifier field in their TS Ordered Sets during
training. Both devices note that the other supports a higher rate and one of them (device A) will be the first to set its
directed_speed_change variable to 1b. When that happens, it will go to Recovery.RcvrLock and send TS1s with the speed_change bit set. If the
desired rate will be 8.0 GT/s and hasn’t been before, the devices will exchange EQ TS1s to deliver the TX equalizer presets to be used
instead of sending ordinary TS1s.

Device B sees incoming TS1s and also transitions to Recovery.RcvrLock. When it recognizes 8 TS1s in a row with the speed_change bit set, it
responds by set‐ ting the speed_change bit in its own TS1s and goes to Recovery.Speed. Device A waits for that response and, when 8 TS1s in
a row with the speed_change bit have been seen, it goes to Recovery.RcvrCfg and then to Recovery.Speed. In that substate, the transmitters
are put into Electrical Idle, the speed is changed to the highest commonly‐supported rate, and the directed_speed_change variable is
cleared.

After a timeout period, both devices transition back to Recovery.RcvrLock and the transmitters are re‐activated using the new speed (8.0
GT/s in this case). They send TS1s again now, this time with the speed_change bit cleared to 0b. If the new speed works well, they
transition to Recovery.RcvrCfg and back to L0. However, if device B has a problem, such as failure to achieve Bit Lock, it will timeout in
this substate and go back to Recovery.Speed. Device A may have
already transitioned to Recovery.RcvrCfg by this time, but when it sees Electri‐ cal Idle now, indicating the neighbor has returned to
Recovery.Speed, it will also go back to that state. Returning to Recovery.Speed causes both devices to revert to the speed in use when
Recovery was entered, 2.5 GT/s in this case, and return to Recovery.RcvrLock.

In response to that development, Device A might set directed_speed_change again and try the process a second time. If it failed again,
device A might choose to remove the 8.0 GT/s rate from its advertised list and try the speed change again without it. Since the highest
common rate is now 5.0 GT/s, if this attempt succeeds the rate will end up at 5.0 GT/s. If it doesn’t work, Device A might give up trying to
use a higher rate. How and when a device chooses to change its advertised rates or give up trying to get a higher rate working is not given
in the spec and will be implementation specific.

## **Link Equalization Overview** 

This section provides an overview of the Equalization Process and prepares the reader to understand the detailed substate machine behaviors
if they are of interest.

Using a higher Link speed results in more signal distortion than lower data rates. To compensate for this and minimize the effort and cost
for system designers, the 3.0 spec adds a requirement for Transmitter Equalization. Unlike the fixed de‐emphasis values for the lower rates,
which is really a simple form of Transmitter equalization itself, the new method uses an active handshake process to match the Transmitters
to the actual signaling environment. During this process, each Receiver Lane evaluates the quality of the incoming signal and suggests Tx
equalization parameters that the Link partner should use to meet the signal quality requirements.

The Link Equalization procedure executes after the first change to the 8.0 GT/s data rate. The spec strongly recommends that the
equalization process be initi‐ ated autonomously (automatically in hardware) but doesn’t require it. If a com‐ ponent chooses not to use the
autonomous mechanism then a software‐based mechanism must be used. If either port is unable to achieve the necessary signal quality through
this process, the LTSSM will conclude that the rate is not work‐ ing and will go back to Recovery.Speed to request a lower speed.

The process involves up to four phases, as described in the text that follows. Once the speed has been changed to 8.0 GT/s, the current
equalization phase in use is indicated by the EC (Equalization Control) field in the TS1s being, as shown in Figure 14‐28.

_Figure 14‐28: EC Field in TS1s and TS2s for 8.0 GT/s_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


## **Phase 0** 

When the Downstream Port is ready to change from a lower rate to the 8.0 GT/s rate, it enters the Recovery.RcvrCfg sub‐state and sends Tx
Presets and Rx Hints to the Upstream Port using EQ TS2s as described in “TS1 and TS2 Ordered Sets” on page 510. (Note that this phase is
skipped if the Link is already running at 8.0 GT/s.) The Downstream Port (DSP) sends Tx Preset values based on the con‐ tents of its
Equalization Control register shown in Figure 14‐29 on page 579. One thing this highlights is that there can be different equalization
values for each Lane. The Downstream Port will use the DSP values for its own Transmit‐ ter and optionally for its Receiver, and send the
USP values to the Upstream Port for it to use when going to the higher speed.
_Figure 14‐29: Equalization Control Registers_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


_Table 14‐8: Tx Preset Encodings_ 

|**Encoding**|**De‐emphasis**|**Preshoot**|
|---|---|---|
|0000b|‐6|0|
|0001b|‐3.5|0|
|0010b|‐4.5|0|
|0011b|‐2.5|0|
|0100|0|0|


## **PCI Express Technology** 

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


Once the rate does change, the Downstream Port begins in Phase 1 and sends TS1s with EC = 01b. It then waits for the Upstream Port to
respond with the same EC value.

Meanwhile, the Upstream Port starts in Phase 0, as illustrated in Figure 14‐30 on page 581, and sends TS1s that echo the preset values it
received earlier from the
EQ TS1s and EQ TS2s. It will use those requested Tx presets if they’re sup‐ ported, and will optionally use the Rx Hints. The USP is allowed
to wait 500ns before evaluating the incoming signal but, once it’s able to recognize two TS1s in a row it’s ready for the next step. This
means the signal quality meets the min‐ imum BER of 10[‐4] (e.g., Bit Error Ratio of less than one error in 10,000 bits). Sub‐ sequently the
USP sets EC=01b in its TS1s thereby moving to Phase 1 and handing control of the next step to the DSP.

_Figure 14‐30: Equalization Process: Starting Point_ 

<img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" alt="Figure 14‐23: Example 3 ‐ Steps 5 and 6"
width="700">

<br>


**Phase 1**

</td>
<td width="50%">

DSP 执行与 USP 相同的操作，并通过检测背靠背 TS1 实现 10[‐4] 的 BER。在此期间，DSP 传达其 Tx 预设和 FS（Full Swing）、LF（Low Frequency）以及 Post-cursor 系数值，如 584 页 Figure 14‐32
所示。规范给出了一些必须满足的、针对一组所请求系数的附加规则，这些规则如下：

1. |C‐1| <= Floor (FS/4)，（注意：Floor 意味着向下舍入到整数值） 2. |C‐1| + C0 + |C+1| = FS

3. C0 ‐ |C‐1| ‐ |C+1| >= LF

## **PCI Express Technology**

FS 表示最大电压，LF 将最小电压定义为 LF/FS。这些信息告知接收器可能的值数量，并允许系数作为整数值传达但作为小数值被理解。

作为示例，假设我们使用为 P7 预设设置定义的系数。FS 值用作参考，可以是 63 之前的任何数字，但为了便于计算，我们假设它为 30。对于 P7，C‐1 为 ‐0.1，在 TS1 中传达以表示 C‐1 的值为 3，因为 3/30 = 0.1，并且始终被视为负值。C+1 为
‐0.2，因此将其传达为 6，因为 6/30 = 0.2 并且始终为负值。C0 为 0.7，因此它将作为 21 发送，因为 21/30 = 0.7。最后，LF 值表示可能的最小比值，对于 P7 而言，该比值为最大值的 0.4 倍。因此，LF 将被传达为 12，因为 12/30 =
0.4。

有了这些信息，让我们检查三个规则，看它们是否对 P7 情况得到满足：

1. 3 <= Floor (12/4)，这等于 3 <= 3，并且为真。

2. 3 + 21 + 6 = 30 这是真的。

3. 21 ‐ 3 ‐ 6 >= 12 这也为真，因此 P7 满足所有三个检查。

一旦下游端口确认链路工作得足够好可以继续进行（它识别出 EC = 01b 的传入 TS1），那么此阶段就完成了，它通过将其 EC = 10b 启动向 Phase 2 的变更（如图 583 页 Figure 14‐31 所示），并将下一步的控制权交回给 USP。当 USP 以 EC
= 10b 响应时，两个 Port 都进入 Phase 2。作为一种愉快的替代方案，下游端口可以确定此时的信号质量已经足够好，无需进一步调整。在这种情况下，它将其 EC 设置为 00b 以退出均衡过程。
## **Phase 2**

信号质量已经足够好以识别 TS1，但还不足以用于运行时操作。一旦两个 Port 都进入 Phase 2，则允许上游端口为下游端口请求 Tx 设置，然后评估它们的工作效果，重复该过程直到获得当前环境下的最佳设置。为了提出请求，它更改其在 TS1 中发送的均衡信息值。如 584 页
Figure 14‐32 所示，有几个感兴趣的值：

- **Tx 预设 (Tx Preset)：** Tx 预设是对发送器设置的粗粒度调整，旨在使其进入当前信号环境的正确大致范围。上游端口设置此值，并设置 "Use Preset" 指示符（Symbol 6 的位 7）以告诉下游端口的发送器使用它。如果未设置 Use Preset
位，则表示预设应保持不变，并且应更改系数值。Tx 系数被视为细粒度调整。

## **PCI Express Technology**

- **系数 (Coefficients)：** 由于规范要求使用 3-tap Tx 均衡器，定义了三个系数值，可以将其视为对信号脉冲的电压调整，以补偿其在通过传输介质时将经历的失真，如 585 页 Figure 14‐33 所示。这在 474 页 "Solution for
8.0 GT/s ‐ Transmitter Equalization" 一节的物理层电气部分中进行了更详细的介绍。

- **Pre-Cursor 系数：** 应用于采样点之前信号的乘数，可根据需要增强或减弱信号。

- **Cursor 系数：** 采样点乘数；始终为正。

- **Post-Cursor 系数：** 应用于采样点之后信号的乘数，可根据需要增强或减弱信号。

- 一旦信号达到所需的质量标准，上游端口通过将 EC 更改为 11b 来表示它已准备好进入下一阶段。
## **Phase 3**

下游端口通过发送 EC = 11b 进行响应，并且现在可以为上游端口的发送器执行相同的信号评估过程。它发送请求新设置的 TS1，方式如下：如果设置了 Use Preset 位，则定义新预设，否则将提供新系数。连续发送此内容 1μs
或直到请求已对其结果进行评估，以较晚者为准。该评估必须等待 500ns，加上通过发送逻辑传出和返回到接收逻辑的往返时间。可以测试不同的均衡设置，直到找到实现所需信号质量的一个设置为止。在该点，下游端口通过将 EC 设置为 00b 来退出均衡过程。

## **均衡说明**

规范提到了与均衡过程相关的其他项目，如下所述：

- 所有 Lane 必须参与该过程；即使那些稍后可能在 upconfigure 事件之后才变为活动的 Lane。

- 组件用于评估传入信号并确定其链路对端应使用的均衡值的算法在规范中并未给出，属于实现特定的。
- 均衡变更可以针对任意数量的 Lane 请求，并且 Lane 可以使用不同的值。

- 在细调步骤结束时（上游端口为 Phase 2，下游端口为 Phase 3），每个组件负责确保发送器设置使其满足规范要求。

- 组件必须评估调整其发送器设置的请求并采取行动。如果给出了有效值，它们必须使用这些值，并将其反映在它们发送的 TS1 中。

- 如果值不符合规则，则可以拒绝调整系数的请求。所请求的值仍会反映在发回的 TS1 中，但 Reject Coefficient Values 位将被设置。

- 组件必须存储通过此过程确定的均衡值，以供将来在 8.0 GT/s 下使用。规范并未明确说明这一点，但作者的观点是这些值将在速度更改为较低速率然后再返回到 8.0 GT/s 速率时仍然保留。这是有意义的，因为重复 EQ
过程可能需要很长时间，并且假设电气环境没有变化，所得到的值将相同。

- 组件允许随时微调其接收器，只要不会导致链路变得不可靠或进入 Recovery 状态。

## **详细的均衡子状态**

本节涵盖链路均衡期间状态机行为的详细描述。

## **Recovery.Equalization**

此子状态用于执行 8.0 GT/s 及更高速率的链路均衡过程。较低速率不使用均衡，并且在这些速率生效时 LTSSM 不会进入此子状态。由于这是 PCIe 的一个新且复杂的主题，因此从高级别视图对整体均衡过程的描述在状态机详细信息之后呈现，参见 577 页 "Link
Equalization Overview" 一节。但首先，让我们逐步了解子状态以查看该过程的机制。

## **下游 Lane**

下游端口从均衡过程的 Phase 1 开始。要开始此过程，需要重置几个位。在 Link Status 2 寄存器（588 页 Figure 14‐36）中，进入此子状态时清除以下位：

- Equalization Phase 1 Successful

- Equalization Phase 2 Successful

- Equalization Phase 3 Successful

- Link Equalization Request

- Equalization Complete

Link Control 3 寄存器的 Perform Equalization 位也被清除为 0b，内部变量 start_equalization_w_preset 也被清除。equalization_done_8GT_data_rate 变量被设置为 1b。

**Phase 1 Downstream。** 在此阶段，下游端口发送 EC = 01b 的 TS1，同时使用来自 Lane Equalization Control 寄存器的预设值，并使用与 Tx 预设字段对应的 FS、LF 和 Post-cursor
系数字段。如果需要时间稳定其接收器逻辑，则允许其等待 500ns 后再评估传入的 TS1。

## _退出至 "Phase 2 Downstream"_

如果下游端口希望继续均衡过程，并且当所有已配置的 Lane 接收到两个连续的 EC = 01b 的 TS1 时，下游端口将转换到 Phase 2。此时，Port 将 Equalization Phase 1 Successful 状态位设置为 1b，并存储接收到的 TS1 LF
和 FS 值以在 Phase 3 中使用（如果下游端口计划调整上游端口的 Tx 系数）。

## _退出至 "详细的 Recovery 子状态"_

如果下游端口不希望使用 Phase 2 和 Phase 3，则它将状态位设置为 1b（Eq. Phase 1 Successful、Eq. Phase 2 Successful、Eq. Phase 3 Successful 和 Eq.
Complete）。这样做的原因之一可能是它已经可以看到信号特性足够好，不需要其他阶段。

## _退出至 "Recovery.Speed"_

如果在 24ms 超时后仍未看到连续的 TS1，则下一状态为 Recovery.Speed。successful_speed_negotiation 标志被清除为 0b，Equalization Complete 状态位被设置为 1b。

**Phase 2 Downstream。** 在此阶段，下游端口发送 EC = 10b 的 TS1，并根据以下规则在每个 Lane 上独立分配系数设置：

- 如果接收到两个连续的 EC = 10b 的 TS1（上游端口已进入 Phase 2），无论是首次接收，还是具有与上次不同的预设或系数值，并且如果所请求的值是合法且受支持的，则在第二个 TS1 请求结束后的 500ns 内将 Tx 设置更改为使用它们。同时，在发送回上游端口的
TS1 中反映这些值，并将 Reject Coefficient Values 位清除为 0b。请注意，更改不得使发送器处的电压或参数违规超过 1ns。

 - a) 如果所请求的预设或系数不合法或不受支持，则不要更改 Tx 设置，但在

## **PCI Express Technology**

发送的 TS1 中反映接收到的值，并将 Reject Coefficient Values 位设置为 1b（参见 590 页 Figure 14‐38）。

- 如果未看到两个连续的 TS1，则保持当前 Tx 预设和系数值。

## _退出至 "Phase 3 Downstream"_

当上游端口对更改感到满意时，它开始发送 EC = 11b 的 TS1，表明希望更改为 Phase 3。当接收到两个这样的连续 TS1 时，将 Eq. Phase 2 Successful 状态位设置为 1b 并更改为 Phase 3。

## _退出至 "Recovery.Speed"_

如果在 32ms 之后，尚未发生到 Phase 3 的转换，则 Port 应清除 successful_speed_negotiation 标志，设置 Equalization Complete 状态位并退出到 Recovery.Speed 子状态。

**Phase 3 Downstream。** 在此阶段，下游端口发送 EC = 11b 的 TS1，并开始为每个 Lane 独立评估上游 Tx 设置的过程。

在发送的 TS1 中，下游端口可以通过将 Use Preset 位设置为 1b 并将 Tx 预设字段设置为所需值来请求新预设，或者通过将 Use Preset 位清除为 0b 并将 Pre-cursor、Cursor 和 Post-Cursor
系数字段设置为所需值来请求新系数。任何一种请求都必须连续发送至少 1μs 或直到评估完成。如果要提供新的预设或系数设置，则必须在所有 Lane 上同时发送。但是，如果某个 Lane 希望保留其当前设置，则不需要该 Lane 请求新设置。

下游端口必须等待足够长的时间以确保上游发送器有机会实现所请求的更改（500ns 加上逻辑的往返延迟），然后获取 Block Alignment 并评估传入的 TS1。在等待期间，预计不会从上游端口收到任何有用的内容，甚至可能不合法。这就是为什么在那段时间之后获取 Block
Alignment 是必需的。

如果看到两个连续的 TS1 与正在请求的相同预设或系数值匹配，并且未设置 Reject Coefficient Values 位，则所请求的设置已被接受并可以评估。如果值匹配但 Reject Coefficient Values 位设置为
1b，则所请求的值已被上游端口拒绝并且未在使用中。对于这种情况，规范建议下游端口使用不同的值重试，但不要求这样做，并且可以选择简单地退出此阶段。

对预设或系数请求所花费的总时间（从发送请求到完成评估）必须小于 2ms。对于在最终优化阶段需要更多时间的设计，可提供例外，但此阶段的总时间不能超过 24ms，并且例外只能使用两次。如果接收器无法识别任何传入的 TS1，则可以假定所请求的设置对该 Lane 不起作用。

## _退出至 "详细的 Recovery 子状态"_

当所有已配置的 Lane 都具有其最佳设置时，下一状态将为 Recovery.RcvrLock。发生这种情况时，Equalization Phase 3 Successful 和 Equalization Complete 状态位将被设置为 1b。

_退出至 "Recovery.Speed"_

否则，在 24ms 超时后（容差为 ‐0 或 +2ms），下一状态将为 Recovery.Speed，successful_speed_negotiation 标志被清除为 0b，同时 Equalization Complete 状态位被设置为 1b。

## **上游 Lane**

上游端口从均衡过程的 Phase 0 开始，并且必须重置几个内部位。在 Link Status 2 寄存器（588 页 Figure 14‐36）中，进入此子状态时清除以下位：

- Equalization Phase 1 Successful

- Equalization Phase 2 Successful

- Equalization Phase 3 Successful

- Link Equalization Request

- Equalization Complete

Link Control 3 寄存器的 Perform Equalization 位也被清除为 0b，内部变量 start_equalization_w_preset 也被清除。equalization_done_8GT_data_rate 变量被设置为 1b。

**Phase 0 Upstream。** 在此阶段，上游端口发送 EC = 00b 的 TS1，同时使用在进入此状态之前在 EQ TS2 中传递的 Tx 预设值。正在发送的 TS1 中的均衡信息字段必须显示预设值以及与该预设对应的 Pre-cursor、Cursor 和
Post-cursor 系数字段。请注意，如果 Lane 在 EQ TS2 中接收到保留的或不受支持的 Tx 预设值，或者根本没有接收到 EQ TS2，则该 Lane 的 Tx 预设字段和系数值由设备特定的方法选择。

_退出至 "Phase 1 Upstream"_

当所有已配置的 Lane 接收到两个连续的 EC = 01b 的 TS1 时，表明它们能够识别来自下游端口的 TS1（下游端口始终以此值开始），则下一阶段为 Phase 1。

如果上游端口计划调整下游端口的 Tx 系数，则必须存储在 TS1 中接收到的均衡值 LF 和 FS 以在 Phase 2 期间使用。

上游端口可以在进入 Phase 0 之后等待 500ns 再评估传入的 TS1，以使其接收器逻辑有时间稳定。
## _退出至 "Recovery.Speed"_

如果在 12ms 超时内未识别传入的 TS1，则 LTSSM 将转换到 Recovery.Speed，清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 1 Upstream。** 在此阶段，上游端口发送 EC = 01b 的 TS1，同时使用在 Phase 0 中确定的发送器设置。这些 TS1 包含 FS、LF 和 Post-cursor 系数值以及当前正在使用的内容。

## _退出至 "Phase 2 Upstream"_

如果所有已配置的 Lane 接收到两个连续的 EC = 10b 的 TS1，表明下游端口希望进入 Phase 2，则下一阶段将为 Phase 2，并且此 Port 将设置 Equalization Phase 1 Successful 状态位。

_退出至 "详细的 Recovery 子状态"_

如果所有已配置的 Lane 接收到两个连续的 EC = 00b 的 TS1，则意味着下游端口已确定均衡过程已经完成，并希望跳过剩余阶段。在这种情况下，下一状态将为 Recovery.RcvrLock，并且 Equalization Phase 1 Successful 和
Equalization Complete 状态位被设置为 1b。

## _退出至 "Recovery.Speed"_

否则，在 12ms 超时后，LTSSM 将转换到 Recovery.Speed，清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 2 Upstream。** 在此阶段，上游端口发送 EC = 10b 的 TS1，并开始为下游端口寻找最佳 Tx 值的过程。回想一下，每个 Lane 的设置是独立确定的。过程如下：

在发送的 TS1 中，上游端口可以通过在正在发送的 TS1 的 Transmitter Preset 字段中放置合法值并将 Use Preset 位设置为 1b 来告诉下游端口开始使用它，以请求新预设。或者，通过在这些字段中放置合法值并将 Use Preset 位清除为 0b
来请求新系数，以便下游端口加载它们而不是预设字段。一旦发出请求，必须重复

至少 1μs 或直到评估完成。如果要提供新的预设或系数设置，则必须在所有 Lane 上同时发送。但是，如果某个 Lane 希望保留其当前设置，则不需要该 Lane 请求新设置。

上游端口必须等待足够长的时间以确保下游发送器有机会实现所请求的更改（500ns 加上逻辑的往返延迟），然后获取 Block Alignment 并评估传入的 TS1。在等待期间，预计不会从下游端口收到任何有用的内容，甚至可能不合法。这就是为什么在那段时间之后获取 Block
Alignment 是必需的。

当接收到包含与正在发送的相同均衡字段的 TS1 并且 Reject Coefficient Values 位未设置（0b）时，则该设置已被接受并且现在可以评估。如果均衡字段匹配但 Reject Coefficient Values
位被设置（1b），则该设置已被拒绝。在这种情况下，规范建议上游端口请求不同的均衡设置，但这不是必需的。

对预设或系数请求所花费的总时间（从发送请求到完成评估）必须小于 2ms。对于在最终优化阶段需要更多时间的设计，可提供例外，但此阶段的总时间不能超过 24ms，并且例外只能使用两次。如果接收器无法识别任何传入的 TS1，则可以假定所请求的设置对该 Lane 不起作用。

_退出至 "Phase 3 Upstream"_

如果所有已配置的 Lane 都具有其最佳设置，则下一阶段为 Phase 3。发生这种情况时，Equalization Phase 2 Successful 状态位将被设置为 1b。

</td>
</tr></tbody></table>

<p align="center"><b>Figure 14‐31: Equalization Process: Initiating Phase 2</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐32: Equalization Coefficients Exchanged</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐33: 3‐Tap Transmitter Equalization</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐34: Equalization Process: Adjustments During Phase 2</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐35: Equalization Process: Adjustments During Phase 3</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐36: Link Status 2 Register</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐37: Link Control 3 Register</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>


<p align="center"><b>Figure 14‐38: TS1s ‐ Rejecting Coefficient Values</b></p>
<p align="center"><img src="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_13_Physical_Layer_-_Electrical/embedded/page0554_img1.png">Page 554</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
