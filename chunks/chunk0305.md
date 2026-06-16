**Chapter 14: Link Initialization & Training** 

page 626. Note that there are two cases: autonomous and bandwidth manage‐ men. Autonomous means the change was not caused by a reliability problem, while bandwidth management means it was. 

_Figure 14‐51: Speed Change ‐ Part 3_ 

**==> picture [336 x 243] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 0<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>TS2 TS2 TS2 EIOSTS2<br>SSS<br>Root PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>EIOSTS2 TS2 TS2 TS2<br>Autonomous Change = 1<br>Root Complex Config Space<br>Link Autonomous Bandwidth Status bit = 1<br>i<br>Figure 14‐52: Bandwidth Change Status Bits<br>**----- End of picture text -----**<br>


**625** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐53: Bandwidth Notification Capability_ 

_Figure 14‐54: Bandwidth Change Notification Bits_ 

**626** 

**Chapter 14: Link Initialization & Training** 

Once the Recovery.Speed substate is reached, the Link is placed into the Electri‐ cal Idle condition in both directions and the speed is changed internally. The speed chosen will be the highest commonly‐supported speed reported in the Rate ID field of the TS1s and TS2s. In this example, that turns out to be 5.0 GT/s and so the change is made to that speed. After a timeout period, the Link neigh‐ bors both transition back to Recovery.RcvrLock and exit Electrical Idle by send‐ ing TS1s again, as shown in Figure 14‐55 on page 627. When the Upstream Port sees them coming back, it transitions to Recovery.RcvrCfg and begins sending TS2s, much like before. This time, though, the Speed Change bit is not set. Even‐ tually TS2s are seen coming back from the Downstream Port that also don’t have the Speed Change bit set, and at that point the state machines transition to the Recovery.Idle on their way back to L0. 

If a speed change has fails for some reason, a component is not allowed to try that speed or a higher one for at least 200 ms after returning to L0 or until the Link neighbor advertises support for a higher speed, whichever comes first. 

_Figure 14‐55: Speed Change Finish_ 

**==> picture [364 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 0<br>Entry Entry<br>Speed Speed<br>Exit to L0 Exit to L0<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 0<br>TS21 TS21 TS21 TS21<br>Root PCIe<br>Link Speed = 5.0 GT/s<br>Complex Endpoint<br>TS21 TS21 TS21 TS21<br>Speed_Change = 0<br>**----- End of picture text -----**<br>


## **Software Control of Speed Changes** 

Software is unable to control when hardware makes decisions about changing the speed but can limit or disable this capability. Limiting it is accomplished by setting the Target Link Speed value in the Link Control 2 Register shown in Fig‐ ure 14‐56 on page 628. This acts as the upper bound on the speeds available to 

**627** 

**PCI Ex ress Technolo p gy** 

the Upstream Port, which will try to maintain that value or the highest speed supported by both Link neighbors, whichever is lower. Software can also force a particular speed to be used by setting the Target Link Speed in the Upstream component and then setting the Retrain Link bit in the Link Control register, shown in Figure 14‐57 on page 629. As mentioned earlier, software is notified of any hardware‐based Link speed or width changes by the Link Bandwidth Noti‐ fication Mechanism. Finally, the speed change mechanism can be disabled by setting the Hardware Autonomous Speed Disable bit. 

_Figure 14‐56: Link Control 2 Register_ 

**628** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐57: Link Control Register_ 

## **Dynamic Link Width Changes** 

The same basic operation for changing the Link speed can also be used to change the Link width, although the sequence is a little more complicated because more LTSSM steps are involved. One thing that’s important for soft‐ ware to note before enabling Link width changes is whether the Link neighbor supports recovering from a narrow Link back to a wide Link (called Upconfig‐ uring the Link). Devices report this ability in bit 6 of the Rate ID field of the TS2s they send during training, as shown in Figure 14‐58 on page 630. If a component doesn’t support this, that would mean that changing to a narrower Link width would be a one‐way event and would only be suitable for the case of a reliabil‐ ity problem on the Link. 

**629** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐58: TS2 Contents_ 

**==> picture [368 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link # Rate Identifier<br>Bit 0 Reserved, = 0<br>2 Lane #<br>Bit 1 Indicates 2.5 GT/s support<br>3 # FTS<br>Bit 2 Indicates 5.0 GT/s support<br>4 Rate ID<br>Bit 3 Indicates 8.0 GT/s support<br>5 Train Ctl<br>Bit 3:5 Reserved, = 0<br>6 Bit 6 Autonomous Change / Link Up-<br>configure Capability / Selectable De-<br>TS ID<br>emphasis<br>13 Bit 7 Speed Change<br>14 TS ID<br>15 TS ID<br>**----- End of picture text -----**<br>


## **Link Width Change Example** 

Consider the example in Figure 14‐59 on page 631 of a Root Port connected to an Endpoint (Gigabit Ethernet Device). Only the Upstream Port will initiate this change, and it begins by going to the Recovery state as before. This time, though, the Speed Change bit is not set. To sort out what the new Link width will be, the Upstream Port will need to tell the Downstream Port to transition from the Recovery state to the Configuration state before going back to L0, as shown in Figure 14‐60 on page 631. There are several substates in the Configu‐ ration state, and a simplified version of them is shown in Figure 14‐61 on page 632. We’ll go through the sequence to be clear on how the steps work. 

**630** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐59: Link Width Change Example_ 

**==> picture [199 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root  Ethernet<br>Complex Device<br>Lane Lane<br>0 0<br>1 1<br>2 Lan2<br>e<br>3 3<br>**----- End of picture text -----**<br>


_Figure 14‐60: Link Width Change LTSSM Sequence_ 

**==> picture [183 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Polling<br>Configuration<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


**631** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐61: Simplified Configuration Substates_ 

**==> picture [136 x 351] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from<br>Polling or Recovery<br>Config.Linkwidth.Start<br>Config.Linkwidth.Accept<br>Config.Lanenum.Wait<br>Config.Lanenum.Accept<br>Config.Complete<br>Config.Idle<br>Exit to<br>L0<br>**----- End of picture text -----**<br>


As before, the Upstream Port initiates this process by going to Recovery and sending TS1s. These don’t have the Speed Change bit set, as highlighted in the example shown in Figure 14‐59 on page 631, where an Ethernet Device initiates this process on its Upstream Port. In response, the Downstream Port sends TS1s back, also with the Speed Change bit cleared. Link and Lane numbers are still shown as being unchanged from the last time the Link was trained. Referring back to Figure 14‐48 on page 622, the next state is Recovery.RcvrCfg during which the Link partners exchange TS2s. 

**632** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐62: Link Width Change ‐ Start_ 

**==> picture [296 x 299] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex<br>Device<br>Lane Lane<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:0) TS1 (Link:0, Lane:0)<br>0 0<br>TS1 (Link:0, Lane:0) TS1 (Link:0,  Lane:0) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:1) TS1 (Link:0, Lane:1)<br>1 1<br>TS1 (Link:0, Lane:1) TS1 (Link:0,  Lane:1) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:2) TS1 (Link:0, Lane:2)<br>Lan<br>2 2<br>e<br>TS1 (Link:0, Lane:2) TS1 (Link:0,  Lane:2) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:3) TS1 (Link:0, Lane:3)<br>3 3<br>TS1 (Link:0, Lane:3) TS1 (Link:0,  Lane:3) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>**----- End of picture text -----**<br>


Since a speed change is not requested, the next state is Recovery.Idle. In that state the Ports normally send the logical idle symbols (all zeros) and the Down‐ stream Port does so, as shown in Figure 14‐63 on page 634. However, the Upstream Port was directed to change the Link width so it doesn’t send the expected Idle symbols. Instead, it sends TS1s with PAD for both the Link and Lane numbers. The Downstream Port recognizes that a previously configured Lane now has a Lane number of PAD, and that causes it to transition to the first Configuration substate: Config.Linkwidth.Start. 

**633** 

**PCI Ex ress Technolo p gy** 

## _Figure 14‐63: Link Width Change ‐ Recovery.Idle_ 

**==> picture [311 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex<br>Device<br> (Link:PAD, L ane:PAD)Lane Idle Data Idle Data Lane<br>0 0<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>1 1<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>Lan<br>2 2<br>e<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>3 3<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br>**----- End of picture text -----**<br>


The Downstream Port now initiates the next step by sending TS1s that have the originally negotiated Link number but PAD on all the Lane numbers, as illus‐ trated in Figure 14‐64 on page 635. The Upstream Port responds with matching TS1s on the Lanes it wants to have “active”, but with PAD for both Link and Lane numbers on the Lanes it wishes to have inactive. When the Downstream Port sees this response, it transitions to the Config.Linkwidth.Accept substate. Note that the Autonomous Change bit is set for these TS1s. 

**634** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐64: Marking Active Lanes_ 

**==> picture [335 x 293] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>Lane State<br>Lane Lane<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>0 0 Active<br>TS1 (Link:0, Lane:PAD) TS1 (Link:0, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>1 1 Inactive<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>Lan<br>2 2 Inactive<br>e<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>3 3 Inactive<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>**----- End of picture text -----**<br>

