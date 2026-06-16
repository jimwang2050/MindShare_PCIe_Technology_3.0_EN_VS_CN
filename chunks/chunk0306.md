The Root Port responds by changing its TS1s to show Lane numbers that are appropriate for the active Lanes, but PAD for the Link and Lane numbers of all the Lanes that were seen to be inactive. The Upstream Port responds with the same TS1s, as shown in Figure 14‐65 on page 636, and the state changes to Con‐ fig.Lanenum.Accept. At this point, the Root Port updates the status bit to show that an autonomous change was detected and changes to the Config.Complete substate. 

**635** 

## **PCI Ex ress Technolo p gy** 

## _Figure 14‐65: Response to Lane Number Changes_ 

**==> picture [344 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
g<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>State<br>Lane Lane<br>Link:PAD, Lane:PAD) TS1 (Link:0, Lane: 0) TS1 (Link:0, Lane: 0)<br>0 0 Active<br>TS1 (Link:0, Lane:0) TS1 (Link:0,  Lane:0) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>1 1 Inactive<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Lan<br>2 2 Inactive<br>e<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>3 3 Inactive<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>**----- End of picture text -----**<br>


In the next step, the Root Port begins to send TS2s on the active Lanes and puts the inactive Lanes into Electrical Idle. Recall that the TS2s report whether a com‐ ponent is “upconfigure capable” and in this example, both Link partners sup‐ port this capability. The Endpoint sends back the same thing: TS2s on active Lanes and Electrical Idle on inactive Lanes. Seeing that, the Root Port’s state machine changes to Config.Idle and it begins to send Logical Idle on the active Lanes. The Endpoint responds with the same thing and the Link state changes back to L0. The Link is now ready for normal operation, albeit with a reduced bandwidth for power conservation. 

**636** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐66: Link Width Change ‐ Finish_ 

**==> picture [344 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>Upconfigure Capability = 1 Upconfigure Capability = 1 State<br>Lane Lane<br>Link:PAD, Lane:PAD) TS2 (Link:0, Lane: 0) TS2 (Link:0, Lane: 0)<br>0 0 Active<br>TS2 (Link:0, Lane:0) TS2 (Link:0,  Lane:0) TS1 (Link:PAD, Lane:PAD)<br>Upconfigure Capability = 1 Upconfigure Capability = 1<br>Electrical Idle<br>1 1 Inactive<br>Electrical Idle<br>Lan<br>2 2 Inactive<br>e<br>Electrical Idle<br>3 3 Inactive<br>**----- End of picture text -----**<br>


As was the case for dynamic speed changes, software can’t initiate Link width changes, but it can disable this mechanism by setting the bit in the Link Control register shown in Figure 14‐67 on page 638. Unlike the speed change case, no software mechanism was defined to allow setting a particular Link width. 

**637** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐67: Link Control Register_ 

## **Related Configuration Registers** 

Many of the configuration registers that are relevant to Link Initialization and Training have been shown when their contents were described earlier, but it seems good to summarize them here. 

## **Link Capabilities Register** 

The Link Capabilities Register is pictured in Figure 14‐68 on page 639 and each bit field is described in the subsections that follow. 

**638** 

**Chapter 14: Link Initialization & Training** 

## _Figure 14‐68: Link Capabilities Register_ 

**==> picture [332 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 22 21 20 19 18 17 15 14 12 1110 9 4 3 0<br>Port Number<br>RsvdP<br>ASPM Optionality Compliance<br>Link Bandwidth<br>Notification Capability<br>Data Link Layer Link Active<br>Reporting Capable<br>Surprise Down Error<br>Reporting Capable<br>Clock Power Management<br>L1 Exit Latency<br>L0s Exit Latency<br>Active State<br>Link PM Support<br>Maximum Link Width<br>Max Link Speed<br>**----- End of picture text -----**<br>


## **Max Link Speed [3:0]** 

This indicates the maximum Link speed for this port, and is given as a pointer to a bit location in the Link Capabilities 2 register Supported Link Speeds Vector that corresponds to the max Link speed. Defined encodings are: 

- 0001b ‐ Supported Link Speeds Vector field bit 0 

- 0010b ‐ Supported Link Speeds Vector field bit 1 

- 0011b ‐ Supported Link Speeds Vector field bit 2 

- 0100b ‐ Supported Link Speeds Vector field bit 3 

- 0101b ‐ Supported Link Speeds Vector field bit 4 

- 0110b ‐ Supported Link Speeds Vector field bit 5 

- 0111b ‐ Supported Link Speeds Vector field bit 6 

All other encodings are reserved. Multi‐function devices sharing an Upstream Port must report the same value in this field in all Functions. This register is Read Only. 

**639** 

**PCI Ex ress Technolo p gy** 

## **Maximum Link Width[9:4]** 

This field indicates the maximum width of the PCI Express Link. The values that are defined are: 

- 00 0000b: Reserved 

- 00 0001b: x1 

- 00 0010b: x2 

- 00 0100b: x4 

- 00 1000b: x8 

- 00 1100b: x12 

- 01 0000b: x16 

- 10 0000b: x32 

All other encodings are reserved. Multi‐function devices sharing an Upstream Port must report the same value in this field in all Functions. This register is Read Only. 

## **Link Capabilities 2 Register** 

The Link Capabilities Register is pictured in Figure 14‐68 on page 639 and shows the Supported Link Speeds Vector to which the Max Link Speed field in the Link Capabilities register points. The values for this field are: 

- Bit 0 = 2.5 GT/s 

- Bit 1 = 5.0 GT/s 

- Bit 2 = 8.0 GT/s 

- Bits 6:3 RsvdP (reserved and preserved). 

_Figure 14‐69: Link Capabilities 2 Register_ 

**==> picture [329 x 113] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 9    8   7 1 0<br>RsvdP<br>Crosslink Supported<br>Supported Link<br>Speeds Vector<br>RsvdP<br>**----- End of picture text -----**<br>


**640** 

**Chapter 14: Link Initialization & Training** 

## **Link Status Register** 

The Link Status Register is pictured in Figure 14‐39 on page 597. 

## **Current Link Speed[3:0]:** 

This read‐only field indicates the current Link speed. The speed will always be 2.5 GT/s when the Link first trains to L0. After that, if a higher commonly‐sup‐ ported speed is available, the LTSSM will go to Recovery and attempt to change to that speed. The values in this field are the same as the Max Link Speed encod‐ ings shown in the Link Capabilities register: 

- 0001b ‐ Supported Link Speeds Vector field bit 0 

- 0010b ‐ Supported Link Speeds Vector field bit 1 

- 0011b ‐ Supported Link Speeds Vector field bit 2 

- 0100b ‐ Supported Link Speeds Vector field bit 3 

- 0101b ‐ Supported Link Speeds Vector field bit 4 

- 0110b ‐ Supported Link Speeds Vector field bit 5 

- 0111b ‐ Supported Link Speeds Vector field bit 6 

All other encodings are reserved. 

Note that the value of this field is undefined when the Link is not up (LinkUp = 0b). 

## **Negotiated Link Width[9:4]** 

This field indicates the result of link width negotiation. There are seven possible widths, all other encodings are reserved. The defined encodings are: 

- 00 0001b: for x1. 

- 00 0010b for x2. 

- 00 0100b for x4. 

- 00 1000b for x8. 

- 00 1100b for x12. 

- 01 0000b for x16. 

- 10 0000b for x32. 

All other encodings are reserved. Note that the value of this field is undefined when the Link is not up (LinkUp = 0b). 

**641** 

**PCI Ex ress Technolo p gy** 

## **Undefined[10]** 

Currently undefined, this bit was previously set by hardware in earlier spec ver‐ sions when a Link Training Error had occurred. It was cleared when the LTSSM successfully entered L0. The spec states that software can write any value to this bit but must ignore any value read from it. 

## **Link Training[11]** 

This read‐only bit indicates that the LTSSM is in the process of training. Techni‐ cally, it means the LTSSM is either in the Configuration or Recovery state, or that the Retrain Link bit has been written to 1b but Link training has not yet begun. This bit is cleared by hardware when the LTSSM exits the Configuration or Recovery state. Since this must be visible to software while Link Training is in progress, it only has meaning for Ports that are facing downstream. Conse‐ quently, this bit is not applicable and reserved for Endpoints, bridge Upstream Ports and Switch Upstream Ports. For them, this bit must be hardwired to 0b. 

_Figure 14‐70: Link Status Register_ 

**==> picture [381 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


## **Link Control Register** 

The Link Control Register is pictured in Figure 14‐71 on page 644, and there are three fields in it that are interesting for us here. 

**642** 

**Chapter 14: Link Initialization & Training** 

## **Link Disable** 

When set to one, the link is disabled. Intuitively, this bit isn’t applicable and is reserved for Endpoints, bridge Upstream Ports, and Switch Upstream Ports because it must be accessible by software even when the Link is disabled. When this bit is written, any read immediately reflects the value written, regardless of the Link state. After clearing this bit, software must be careful to honor the tim‐ ing requirements regarding the first Configuration Read after a Conventional Reset (see “Reset Exit” on page 846). 

## **Retrain Link** 

This bit allows software to initiate Link re‐training whenever it is deemed nec‐ essary, as for error recovery. The bit is not applicable to and is reserved for End‐ point devices and Upstream Ports of Bridges and Switches. When set to 1b, this directs the LTSSM to the Recovery state before the completion of the Configura‐ tion write Request is returned. 

## **Extended Synch** 

As it affects training, this bit is used to greatly extend the time spent in two situ‐ ations, for the purpose of assisting slower external test or analysis hardware to synchronize with the Link before it resumes normal communication. One of these is when exiting L0s, where setting this bit forces the transmission of 4096 FTSs prior to entering L0. The other case is in the Recovery state prior to enter‐ ing Recovery.RcvrCfg, where it forces the transmission of 1024 TS1s. 

**643** 

**PCI Ex ress Technolo p gy** 

## _Figure 14‐71: Link Control Register_ 

**==> picture [313 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


**644** 

## Part Five: 

# Additional System Topics 

## _**15 Error Detection and Handling**_ 

## **The Previous Chapter** 
