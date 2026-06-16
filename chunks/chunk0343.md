The power budget information is maintained within a table that consists of one or more 32‐bit entries. Each table entry contains power budget information for the different operating modes supported by the device. Each table entry is selected via the data select field, and the selected entry is then read from the data field. The index values start at zero and are implemented in sequential order. When a selected index returns all zeros in the data field, the end of the power budget table has been located. Figure 19‐13 on page 885 illustrates the format and types of information available from the data field. 

_Figure 19‐12: Power Budget Capability Registers_ 

**==> picture [341 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                                                                                               0<br>Offset<br>PCIe Extended Capability Header 00h<br>RsvdP Data Select  04h<br>Register<br>Data Register 08h<br>Power Budget<br>RsvdP 0Ch<br>Capability Register<br>**----- End of picture text -----**<br>


**884** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Figure 19‐13: Power Budget Data Field Format and Definition_ 

**==> picture [243 x 476] intentionally omitted <==**

**----- Start of picture text -----**<br>
Base Power<br>Data Scale Specifies the base power (in watts)for the state indicated by bits [20:10]. Base Power x Scale = actual power consumption.   Data Scale Values:     00b            1.0x     01b            0.1x     10b            0.01x     11b            0.001x All other encodings are reserved. PM sub state of operating condition described by this entry:  000b             Default Sub State   001b –111b   Device-specific Sub StateAll other encodings are reserved. PM state described by this entry:  00b            D0   01b            D1   10b            D2   11b            D3 D3-Cold PM State description = 11b and Aux or PME Aux in Type field.D3-Hot state = 11b + any other Type value.  entries starting with n<br>    10 9    8  7                                   0<br>State<br>PM Sub<br>PM State<br>Type<br>Rail<br>Power<br>This entire register is read-only<br>RsvdP<br>31                                            21 20      18 17     15 14 13 12<br>How it works: The power budgeting data for the function consists of a table of entry 0. Each entry is read by placing an index value in the Power Budgeting DataSelect register and then reading the value returned in the Power Budgeting Data register.The end of table is indicated by a return value of all 0's in the Data register.<br>Auxiliary<br>Type of operating condition described by this entry:  000b            PME Aux   001b   010b            Idle   011b            Sustained   111b            Maximum All other encodings are reserved.<br>Power rail of operating condition described by this entry:  000b     12V power.  001b     3.3V power.  010b     1.8V power.  111b     Thermal All other encodings are reserved.<br>**----- End of picture text -----**<br>


**885** 

**PCI Ex ress Technolo p gy** 

**886** 

## _**20**_ 

## _**Updates for Spec Revision 2.1**_ 

## **Previous Chapter** 

The previous chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it’s important to ensure that its power needs don’t exceed what the system can deliver. A mechanism was needed to query the power requirements of a device before giving it permission to oper‐ ate. Power budgeting registers provide that. 

## **This Chapter** 

This chapter describes the changes and new features that were added with the 2.1 revision of the spec. Some of these topics, like the ones related to power management, are described in other chapters, but for others there wasn’t another logical place for them. In the end, it seemed best to group them all together in one chapter to ensure that they were all covered and to help clarify what features were new. 

## **The Next Chapter** 

The next section is the book appendix which includes topics such as: Debugging PCI Express Traffic using LeCroy Tools, Markets & Applications of PCI Express Architecture, Implementing Intelligent Adapters and Multi‐Host Systems with PCI Express Technology, Legacy Support for Locking and the book Glossary. 

## **Changes for PCIe Spec Rev 2.1** 

The 2.1 revision of the spec for PCIe introduced several changes to enhance per‐ formance or improve operational characteristics. It did not add another data rate and that’s why it was considered an incremental revision. The modifica‐ tions can be grouped generally into four areas of improvement: System Redun‐ dancy, Performance, Power Management, and Configuration. 

**887** 

**PCI Ex ress Technolo p gy** 

## **System Redundancy Improvement: Multi-casting** 

The Multi‐casting capability allows a Posted Write TLP to be routed to more than one destination at the same time, allowing for things like automatically making redundant copies of data or supporting multi‐headed graphics. As shown in Figure 20‐1 on page 888, a TLP sourced from one Endpoint can be routed to multiple destinations based solely on its address. In this example, data is sent to the video port for display while redundant copies of it are auto‐ matically routed to storage. There are other ways this activity could be sup‐ ported, of course, but this is very efficient in terms of Link usage since it doesn’t require a recipient to re‐send the packet to secondary locations. 

_Figure 20‐1: Multicast System Example_ 

**==> picture [372 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDRAM<br>GFX Root Complex<br>Endpoint Endpoint<br>Switch<br>NIC<br>Disk  Disk<br>SCSI SCSI<br>**----- End of picture text -----**<br>


This mechanism is only supported for posted, address‐routed Requests, such as Memory Writes, that contain data to be delivered and an address that can be decoded to show which Ports should receive it. Non‐posted Requests will not be treated as Multicast even if their addresses fall within the MultiCast address range. Those will be treated as unicast TLPs just as they normally would. 

The setup for Multicast operation involves programming a new register block for each routing element and Function that will be involved, called the Multi‐ cast Capability structure. The contents of this block are shown in Figure 20‐2 on page 889, where it can be seen that they define addresses and also MCGs (Mul‐ tiCast Group numbers) that explain whether a Function should send or receive copies of an incoming TLP or whether a Port should forward them. Let’s 

**888** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

describe these registers next and discuss how they’re used to create Multicast operations in a system. 

_Figure 20‐2: Multicast Capability Registers_ 

|20<br>31|19|19|16|15||0||||
|---|---|---|---|---|---|---|---|---|---|
|Next Extended<br>Capability Offset||Version<br>(1h)||PCIe Extended Capability ID<br>(0012h for Multicast)||||||
||||31|||||0|Offset|
|||||PCIe Enhanced Capability Header|||||00h|
|||||Multicast Control||Multicast Capability|||04h|
|MCGs this Function||||MC_Base_Address Register|||||08h<br>0Ch|
|is allowed to receive||||||||||
|or forward||||MC_Receive||Register|||10h<br>14h|
|MCGs this Function||||||||||
|must not send|||||||||18h|
|or forward||||MC_Block_All||Register|||1Ch|
|MCGs this Function<br>must not send or||||MC_Block_Untranslated Register|||||20h<br>24h|
|forward if the address||||||||||
|Root Ports and<br>is untranslated||||MC_Overlay_BAR|||||28h<br>2Ch|
|Switch Ports||||||||||



## **Multicast Capability Registers** 

The Capability Header register at the top of the figure includes the Capability ID of 0012h, a 4‐bit Version number, and a pointer to the next capability struc‐ ture in the linked list of registers. 

## **Multicast Capability** 

This register, shown in detail in Figure 20‐3 on page 890, contains several fields. The MC_Max_Group value defines how many Multicast Groups this Function has been designed to support minus one, so that a value of zero means one 

**889** 

**PCI Ex ress Technolo p gy** 

group is supported. The Window Size Requested, which is only valid for End‐ points and reserved in Switches and Root Ports, represents the address size needed for this purpose as a power of two. 

_Figure 20‐3: Multicast Capability Register_ 

**==> picture [294 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
15   14   13 8   7   6   5 0<br>MC_Window_Size RsvdP MC_Max_Group<br>Requested<br>RsvdP<br>Exponent for MC  Max number of MCGs<br>MC_ECRC_ window size in  Supported minus 1<br>Regeneration_Supported endpoints –<br>RsvdP in Switches<br>and RC<br>**----- End of picture text -----**<br>


Lastly, bit 15 indicates whether this Function supports regenerating the ECRC value in a TLP if forwarding it involved making address changes to it. Refer to the section called “Overlay Example” on page 895 for more detail on this. 

## **Multicast Control** 

This register, shown in Figure 20‐4 on page 890, contains the MC_Num_Group that is programmed with the number of Multicast Groups configured by soft‐ ware for use by this Function. The default number is zero, and the spec notes that programming a value here that is greater than the max value defined in the MC_Max_Group register will result in undefined behavior. The MC_Enable bit is used to enable the Multicast mechanism for this component. 

_Figure 20‐4: Multicast Control Register_ 

**==> picture [274 x 82] intentionally omitted <==**

**----- Start of picture text -----**<br>
15   14 6   5 0<br>RsvdP MC_Num_Group<br>MC_Enable Number of MCGs<br>Configured minus 1<br>**----- End of picture text -----**<br>


**890** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

## **Multicast Base Address** 

The base address register, shown in Figure 20‐5 on page 891, contains the 64‐bit starting address of the Multicast Address range for this component. The Multi‐ Cast Index Position register indicates the bit position within the address where the MultiCast Group (MCG) number is to be found. When the address of an incoming TLP falls within the MultiCast address range starting at this Base Address, the logic will offset into the address itself by the number of bit loca‐ tions given in the Index Position and interpret the next bits (up to 6 bits, allow‐ ing up to 64 groups) as the MCG number for that TLP. The MCG number, in turn, will indicate whether the Port should forward a copy of this TLP. 

_Figure 20‐5: Multicast Base Address Register_ 

**==> picture [287 x 91] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 12   11 6   5 0<br>MC_Index<br>MC_Base_Address [31:12] RsvdP<br>_Position<br>MC_Base_Address [63:32]<br>**----- End of picture text -----**<br>


An example of locating the MCG within the address is shown in Figure 20‐6 on page 892. Here the Index Position value is 24, so the MCG is found in address bits 25 to 30. Interestingly, since the base address doesn’t define the lower 12 bits of the address, the MC Index Position must be 12 or greater to be valid. If it’s less than 12 and the MC_Enable bit is set, the component’s behavior will be unde‐ fined. 

**891** 

## **PCI Ex ress Technolo p gy** 

_Figure 20‐6: Position of Multicast Group Number_ 

**==> picture [364 x 165] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [63:32]<br>Byte 12 MCG Address [31:2] R<br>MC_Index_Position = 24<br>**----- End of picture text -----**<br>


## **MC Receive** 
