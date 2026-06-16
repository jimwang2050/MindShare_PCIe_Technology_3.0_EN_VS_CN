The slave must be able to detect an Electrical Idle on any Lane within 1ms of EIOS being received. Between the time EIOS is received and Electrical Idle is actually detected, the Loopback Slave may receive a bit stream that is undefined by the encoding scheme, and it may loop that back to the trans‐ mitter. 

**617** 

**PCI Ex ress Technolo p gy** 

## **Loopback.Exit** 

During this substate, the Loopback Master sends an EIOS for Ports that support only 2.5 GT/s and eight consecutive EIOSs for Ports that support rates higher than 2.5 GT/s (optionally send 8 for the Ports that only support 2.5 GT/s, too), and then enter Electrical Idle on all Lanes for 2ms. 

- The Loopback Master must transition to Electrical Idle within TTX‐IDLE‐SET‐ TO‐IDLE[after sending the last EIOS. Note that the EIOS marks the end of] the master’s transmit and compare operations. Any data received by the master after any EIOS is received is undefined and should be ignored. 

The loopback slave must enter Electrical Idle on all Lanes for 2ms but must echo back all Symbols received prior to detecting Electrical Idle to ensure that the master sees the arrival of the EIOS as the end of the logical send and compare operation. 

## _Exit to “Detect State”_ 

The next state will be Detect once the required EIOSs have been exchanged and the Lanes have been in Electrical Idle for 2ms. 

## **Dynamic Bandwidth Changes** 

Higher data rates and wider Links for PCIe offer higher performance than pre‐ vious generations but use more power, too. Consequently, the 2.0 spec writers chose to include another pair of power management mechanisms that allow the hardware to adjust the Link speed and width on the fly. These allow the Link to use the highest speed and widest possible Link when performance is needed, or to drop down to a lower speed or narrower Link width or both to reduce power. There are two clear advantages to this method compared to changing the Link or Device power state. 

First, the Link is always able to communicate regardless of the changes, with a relatively short interruption in service to make the change. Second, the power saving can be greater. For example, a x16 Link would almost certainly use less power operating as an active x1 Link than as a x16 Link in L0s. 

Secondly, in addition to power conservation, bandwidth reductions can also be used to resolve reliability problems. For example, it may be that a high speed Link produces unacceptable reliability, in which case either Link component is allowed to remove the offending speed from the list of supported speeds that it advertises. How a component makes that reliability determination is not speci‐ 

**618** 

**Chapter 14: Link Initialization & Training** 

fied. Interestingly, components are also permitted to go into the Recovery state and advertise a different set of supported speeds without requesting a speed change in the process. 

Changing the Link Speed or Link Width requires the Link to be re‐trained. When the Link is in the L0 state, and the speed needs to be changed, the LTSSM of the port desiring the speed change starts transmitting TS1s to its neighbor. Doing so results in the two involved ports’ LTSSMs going through Recovery state where the Link speed is changed and then back to L0. 

Similarly, the port that desires to change the Link width starts transmitting TS1s to its neighbor. Doing so results in the two involved ports’ LTSSMs going through Recovery state then Configuration state where the Link width is changed. The LTSSM finally returns to L0 with the new Link width established. 

Because the LTSSM is involved in dynamic Link bandwidth management, it makes sense to discuss the two aspects of Link bandwidth management, dynamic Link speed change and dynamic Link width change in the following sections. Let’s consider these two options separately, starting with Link speed changes. 

## **Dynamic Link Speed Changes** 

By way of review, the LTSSM states are illustrated in Figure 14‐45 on page 620 to make it easier to recall the flow of states. Although according to the Gen1 specification, speed change was indicated to be performed in the Polling state, the subsequent Gen2 spec moved this function to the Recovery state. 

**619** 

**PCI Ex ress Technolo p gy** 

_Figure 14‐45: LTSSM Overview_ 

**==> picture [196 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Polling<br>Configuration<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


During the Polling state, TS1s are exchanged between Link neighbors, and these contain several kinds of information as shown in Figure 14‐46 on page 621. The most interesting part for us here is byte number 4, the Rate Identifier. Bits 1, 2 and 3 indicate which data rates are available and the spec points out that 2.5 GT/s must always be supported, while 5.0 GT/s must also be supported if 8.0 GT/s is supported. 

The meaning of bit 6 depends on whether the Port is facing upstream or down‐ stream and also on what LTSSM state the Port is in. However, for the speed change case the options are reduced because it’s only meaningful coming from the Upstream Port and just indicates whether or not the speed change is an autonomous event. “Autonomous” means that the Port is requesting this change for its own hardware‐specific reasons and not because of a reliability issue. Bit 7 is used by the Upstream Port to request a speed change. These val‐ ues are very similar in the TS2s, although bit 6 has another meaning now related to autonomous Link width changes that we’ll discuss later. 

**620** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐46: TS1 Contents_ 

**==> picture [315 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link #<br>Rate Identifier<br>2 Lane # Bit 0 Reserved, = 0<br>3 # FTS Bit 1 Indicates 2.5 GT/s support<br>4 Rate ID Bit 2 Indicates 5.0 GT/s support<br>5 Train Ctl Bit 3 Indicates 8.0 GT/s support<br>6 Bit 4:5 Reserved, = 0<br>TS ID Bit 6 Autonomous Change / Selectable De-<br>13 emphasis<br>14 TS ID Bit 7 Speed Change<br>15 TS ID<br>**----- End of picture text -----**<br>


_Figure 14‐47: TS2 Contents_ 

**==> picture [316 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link # Rate Identifier<br>Bit 0 Reserved, = 0<br>2 Lane #<br>Bit 1 Indicates 2.5 GT/s support<br>3 # FTS<br>Bit 2 Indicates 5.0 GT/s support<br>4 Rate ID<br>Bit 3 Indicates 8.0 GT/s support<br>5 Train Ctl<br>Bit 4:5 Reserved, = 0<br>6<br>Bit 6 Autonomous Change / Link Up-<br>TS ID configure Capability / Selectable De-<br>13 emphasis<br>14 TS ID Bit 7 Speed Change<br>15 TS ID<br>**----- End of picture text -----**<br>


**621** 

**PCI Ex ress Technolo p gy** 

## **Upstream Port Initiates Speed Change** 

A speed change must be initiated by the Upstream Port (Port facing upstream), and is accomplished by transitioning to the Recovery state. The substates of the Recovery state are shown in Figure 14‐48 on page 622 and the part of interest for this discussion is highlighted by the oval. The discussion that follows here is a relatively high‐level overview of the entire speed change process and doesn’t get into the details of the LTSSM operation. To learn more about that, refer to the discussion called “Recovery State” on page 571. 

_Figure 14‐48: Recovery Sub‐States_ 

**==> picture [342 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Recovery.Speed<br>Entry from Loopback Exit to<br>L1, L0, L0s Configuration<br>Recovery.Equalization<br>Recovery.RcvrLock Recovery.Idle Exit to<br>(bit/symbol re-lock) Recovery.RcvrCfg (Send idle data) Disabled<br>Exit to Hot<br>Exit to Exit to Reset<br>Configuration Detect<br>Exit to L0<br>**----- End of picture text -----**<br>


## **Speed Change Example** 

To illustrate the process, consider the speed change example shown in Figure 14‐49 on page 623. Note that the Equalization substate has been removed in this example to make the diagrams simpler and easier to follow. The example shows a change from 2.5 GT/s to 5.0 GT/s and so the Equalization substate is not used anyway. A change to 8.0 GT/s would go through the same process but would just add a trip through the Equalization substate at the end of the process. To 

**622** 

**Chapter 14: Link Initialization & Training** 

learn more about the Equalization process, refer to “Recovery.Equalization” on page 587. 

The Endpoint in this example, which can only have an Upstream Port, is shown connected to a Root Complex, which can only have Downstream Ports. Only the Upstream Port can initiate the speed change process, and it does so because its _Directed Speed Change_ flag was set earlier based on some hardware‐specific con‐ ditions. To start the sequence, it changes its LTSSM to the Recovery state, enters the Recovery.RcvrLock substate and sends TS1s with the Speed Change bit set and listing the speeds that it will support, as shown in Figure 14‐49 on page 623. When the Downstream Port sees the incoming TS1s, it also changes to the Recovery state and begins sending TS1s back. Since the Speed Change bit was set in the incoming TS1s, that will set the _Directed Speed Change_ flag in the Root Port and the outgoing TS1s will also have that bit set. The speed that the Link will attempt to use will be the highest commonly‐supported speed so, if a Device wants to use a lower speed it would simply not list the higher speeds as being supported at this time. 

_Figure 14‐49: Speed Change ‐ Initiated_ 

**==> picture [336 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 1<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 1<br>TS1 TS1 TS1 TS1<br>Root PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>TS1 TS1 TS1 TS1<br>Speed_Change = 1<br>**----- End of picture text -----**<br>


When the Upstream Port detects the TS1s coming back, its state machine changes to the Recovery.RcvrCfg substate and it begins to send TS2s that still have the Speed Change bit set, as illustrated in Figure 14‐50 on page 624. These 

**623** 

**PCI Ex ress Technolo p gy** 

TS2s will now also have the Autonomous Change bit set if this change was not caused by a reliability problem on the Link. When the Downstream Port sees incoming TS2s, it also changes to the Recovery.RcvrCfg substate and returns TS2s with the Speed Change bit set. However, the Autonomous Change bit is reserved in the TS2s for Downstream Ports during Recovery. 

_Figure 14‐50: Speed Change ‐ Part 2_ 

**==> picture [371 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 1 Directed Speed Change = 1<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 1<br>TS2 TS2 TS2 TS2<br>Root  PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>TS2 TS2 TS2 TS2<br>Speed_Change = 1<br>Autonomous Change = 1<br>**----- End of picture text -----**<br>


Once each Port has seen 8 consecutive TS2s with the Speed Change bit set, they know that the next step will be to go to the Recovery.Speed substate, as shown in Figure 14‐51 on page 625. At this point, the Downstream Port needs to regis‐ ter the setting of the Autonomous Change bit in the incoming TS2s. To support this, some extra fields have been added to the PCIe Capability registers. 

The status bits for Link bandwidth changes are found in the Link Status regis‐ ter, shown in Figure 14‐52 on page 625. Status changes can also be used to gen‐ erate an interrupt to notify software of these events if the device is capable and has been enabled to do so. This capability is reported by the Link Bandwidth Notification Capable bit, shown in Figure 14‐53 on page 626, and enabled by the Interrupt Enable bits in the Link Control register, as shown in Figure 14‐54 on 

**624** 
