These values are programmed by software into a table to be used during normal operation. The spec recommends that the table be located in the TPH Requester Capability structure, shown in Figure 20‐16 on page 906, but it can alternatively be built into the MSI‐X table instead. Only one or the other of these table loca‐ tions can be used for a given Function. The location is given in the ST Table Location field [10:9] of the Requester Capability register, shown in Figure 20‐17 on page 907. The encoding of these 2 bits is shown in Table 20‐2 on page 907. 

_Figure 20‐16: TPH Requester Capability Structure_ 

|31|15|0<br>7|
|---|---|---|
|PCI Express Capabilities Register|Next Cap<br>Pointer|PCI Express<br>Cap ID (17h)|
|TPH Requester Capability Register|||
|TPH Requester Control Register|||
|TPH ST Table (optional)<br>(Sized by number of ST entries)|||



**906** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐17: TPH Capability and Control Registers_ 

**==> picture [340 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPH Requester Capability Register<br>31 27 26 16 15 11 10 9 8 7 3 2 1 0<br>RsvdP ST Table Size RsvdP RsvdP<br>ST Table Location<br>Extended TPH Requester Supported<br>Device-Specific Mode Supported<br>Interrupt Vector Mode Supported<br>No ST Mode Supported<br>TPH Requester Control Register<br>31 10 9 8 7 3 2 0<br>RsvdP RsvdP<br>TPH Requester Enable<br>ST Mode Select<br>**----- End of picture text -----**<br>


_Table 20‐2: ST Table Location Encoding_ 

|**Bits [10:9]**|**ST Table Location**|
|---|---|
|00b|Not present|
|01b|Located in the Requester Capa‐<br>bility structure|
|10b|Located in the MSI‐X table|
|11b|Reserved|



**907** 

**PCI Ex ress Technolo p gy** 

The Requester Capability register lists the number of entries in the ST Table in bits [26:16]. Each table entry is 2 bytes wide, and the ST Table implemented in the TPH Capability register set is shown in Figure 20‐18 on page 908, where entry zero is highlighted. The Requester Capability register also describes which ST Modes are supported for the Requester with the 3 LSBs: 

- **No ST** ‐ uses zeros for ST bits. Selected in the TPH Requester Control regis‐ ter’s ST Mode Select field when the value = 000b. 

- **Interrupt Vector** ‐ uses the interrupt vector number as the offset into the table, meaning the values are contained in the MSI‐X table. (ST Mode Select value = 001b.) 

- **Device‐Specific** ‐ uses a device‐specific method to offset into the ST Table in the TPH Capability structure because the ST values are located there. This is the recommended implementation, although how a given Request is associated with a particular ST entry is outside the scope of the spec. (ST Mode Select value = 010b.) 

- All other ST Mode Select encodings are reserved for future use. 

_Figure 20‐18: TPH Capability ST Table_ 

||31|24|23|16|15|8|7|0||
|---|---|---|---|---|---|---|---|---|---|
||ST Upper Entry (1)||ST|Lower Entry (1)|ST Upper Entry (0)||ST Lower Entry (0)|||
||ST Upper Entry (3)||ST|Lower Entry (3)|ST Upper Entry (2)||ST Lower Entry (2)|||
|||||||||||
|||ST Upper Entry|ST Lower Entry|||ST Upper Entry|ST Lower Entry|||
|||(Table Size)||(Table Size)||(Table Size - 1)|(Table Size - 1)|||
|||||||||||



## **TLP Prefixes** 

The Steering Tag bits can be extended with the addition of optional TLP Prefixes if needed. When one or more Prefixes are given with the TLP, the header reports it by setting the most significant bit in the Format field, as shown in Figure 20‐19 on page 909. 

**908** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

_Figure 20‐19: TPH Prefix Indication_ 

**==> picture [344 x 126] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>1  0 0 tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- End of picture text -----**<br>


## **IDO (ID-based Ordering)** 

Transaction ordering rules are important for proper traffic flow, but there are times when it’s not necessary and latencies can be improved in those cases. In particular, TLPs from different Requesters are very unlikely to have dependen‐ cies between them, so this feature allows software to enable them to be re‐ordered for improved performance. The details of this operation are described in the section called “ID Based Ordering (IDO)” on page 301. 

## **ARI (Alternative Routing-ID Interpretation)** 

The motivation for this optional feature is to increase the number of Function numbers available to Endpoints. Device numbers were useful in a shared‐bus architecture like PCI but are not usually needed in a point‐to‐point architecture. Consequently, the spec writers chose to allow devices to interpret the destina‐ tion for ID‐routed commands differently. This was accomplished by defining the Device number to always be zero and then allowing the Function number to use the 5 bits in the ID that were previously the Device number. Effectively, the Device number goes away while the Function number grows to 8 bits. The tar‐ get for a TLP that uses ARI will need to be enabled to recognize it before soft‐ ware can use this feature, but Routing elements in the path to it don’t have to be aware of this. They’re only looking at the bus number to determine the routing. 

**909** 

**PCI Ex ress Technolo p gy** 

## **Power Management Improvements** 

There are four additions that improve the system’s ability to manage power effectively, and they are listed here. All of these are covered in Chapter 16, enti‐ tled ʺPower Management,ʺ on page 703. 

## **DPA (Dynamic Power Allocation** 

A new set of extended configuration registers defines up to 32 sub‐states below D0. This allows software to easily make changes to a device’s power state with‐ out incurring the latency penalty of going all the way to the D1 device power state. To learn more on this, see “Dynamic Power Allocation (DPA)” on page 714 

## **LTR (Latency Tolerance Reporting)** 

Allowing Endpoints to report the latencies they can tolerate in response to their requests enables system software to make better choices regarding system response time and sleep states. To learn more about this, see “LTR (Latency Tol‐ erance Reporting)” on page 784. 

## **OBFF (Optimized Buffer Flush and Fill)** 

Similarly, allowing the system to report the preferred time slots during which Endpoints should or should not initiate DMA or interrupt traffic helps coordi‐ nate system sleep times and improve power management. For more on this, see “OBFF (Optimized Buffer Flush and Fill)” on page 776. 

## **ASPM Options** 

This change simply permits devices to support no ASPM Link power manage‐ ment if they choose to do so. In the previous spec versions, support for L0s was mandatory, but now it becomes optional. 

**910** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

## **Configuration Improvements** 

A few configuration registers were added to improve software visibility and control of devices. 

## **Internal Error Reporting** 

This is intended to provide a standardized way of reporting internal problems for devices like switches that don’t have a driver to handle that for them. It also adds the capability to track multiple TLP headers when they result in errors instead of just one as before. This topic is covered in the section on errors called “Internal Errors” on page 667. 

## **Resizable BARs** 

This new set of extended configuration registers allows devices that use a large amount of local memory to report whether they can work with smaller amounts and, if so, what sizes are acceptable. Software that knows to look for them can find the new registers, shown in Figure 20‐20 on page 912, and program them to give the appropriate memory size for the platform based on the competing requirements of system memory and other devices. 

A few rules apply to the use of these registers: 

1. To avoid confusion, a BAR size should only be changed when the Memory Enable bit has been cleared in the Command register. 

2. The spec strongly recommends that Functions not advertise BARs that are bigger than they can effectively use. 

3. To ensure optimal performance, software should allocate the biggest BAR size that will work for the system. 

**911** 

## **PCI Ex ress Technolo p gy** 

## _Figure 20‐20: Resizable BAR Registers_ 

**==> picture [363 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 20 19 16 15 0<br>Next Extended Version PCIe Extended Capability ID<br>Capability Offset (1h) (0015h for Resizable BAR)<br>31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>Resizable BAR Capability Register (0) 004h<br>Register Pair<br>for each  Reserved Resizable BAR Control Register (0) 008h<br>supported<br>BAR …<br>Resizable BAR Capability Register (n) n*8 +4<br>Reserved Resizable BAR Control Register (n) n*8 +8<br>**----- End of picture text -----**<br>


## **Capability Register** 

This register simply reports which BAR sizes will work for this Function. Bits 4 to 23 are used for this and the values are as shown here: 

- Bit 4 ‐ 1MB BAR size will work for this Function 

- Bit 5 ‐ 2MB 

- Bit 6 ‐ 4MB 

- ... 

- Bit 23 ‐ 512GB will work for this Function 

_Figure 20‐21: Resizable BAR Capability Register_ 

**==> picture [242 x 38] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24   23 4   3 0<br>RsvdP RsvdP<br>**----- End of picture text -----**<br>


## **Control Register** 

The BAR Index field in this register reports to which BAR this size refers (0 to 5 are possible). The Number of Resizable BARs field is only defined for Control 

**912** 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

Register zero and is reserved for all the others. It tells how many of the six pos‐ sible BARs actually have an adjustable size. Finally, the BAR Size field is pro‐ grammed by software to specify the desired size the BAR indicated by the BAR Index field (0 = 1MB, 1=2MB, 2=4MB, ..., 19=512GB). 

_Figure 20‐22: Resizable BAR Control Register_ 

**==> picture [281 x 136] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 13  12 8   7 5   4 3    2 0<br>RsvdP RsvdP<br>BAR Size (RW)<br>Number of Resizable<br>BARs (RO)<br>BAR Index (RO)<br>**----- End of picture text -----**<br>


Once the Resizable values have been programmed, then enumeration software will be able to work as it normally does: writing all F’s to each BAR and reading it back will report the size that was selected. Note that if the size value is changed, the contents of the BAR will be lost and will need to reprogrammed if it was previously set up. Figure 20‐23 on page 914 highlights the BAR registers in the configuration header space for a Type 0 header. 

**913** 

**PCI Ex ress Technolo p gy** 

## _Figure 20‐23: BARs in a Type0 Configuration Header_ 

**==> picture [160 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 2 1 0 DW<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>HeaderType LatencyTimer CacheLineSize 03<br>04<br>Base Address 0<br>05<br>Base Address 1<br>06<br>Base Address 2<br>07<br>Base Address 3<br>08<br>Base Address 4<br>09<br>Base Address 5<br>10<br>CardBus CIS Pointer<br>Subsystem ID SubsystemVendor ID 11<br>Expansion ROM 12<br>Base Address<br>Reserved CapabilitiesPointer 13<br>14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>**----- End of picture text -----**<br>


## **Simplified Ordering Table** 
