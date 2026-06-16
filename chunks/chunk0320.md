|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|
|---|---|---|---|
|**Power Management Capabilities**<br>**(PMC)**||**Pointer to**<br>**Next Capability**|**Capability ID**<br>**01h**|
|**Data Register**|**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Control/Status Register**<br>**(PMCSR)**||



## **PM Capabilities (PMC) Register** 

The fields of this 16‐bit read‐only register are described in Table 16‐12. 

**724** 

**Chapter 16: Power Management** 

_Table 16‐12: The PMC Register Bit Assignments_ 

|**Bit(s)**|**Description**|
|---|---|
|31:27|**PME_Support**field. Indicates in which PM states the Function is capable<br>of sending a PME message. A zero in a bit indicates PME notification is<br>not supported in the respective PM state.<br>**Bit**<br>  **Corresponds to PM State**<br>27                      D0<br>28                      D1<br>29                      D2<br>30                      D3hot<br>31                      D3cold(Function requires aux power for PME logic<br>and Wake signaling via beacon or WAKE# pin)<br>Systems that support wake from D3coldmust also support aux power and<br>must use it to signal the wakeup.<br>Bits 31, 30, and 27 must be set to 1b for virtual PCI‐PCI Bridges imple‐<br>mented within Root and Switch Ports. This is required for ports that for‐<br>ward PME Messages.|
|26|**D2_Support**bit. 1 = Function supports the D2 PM state.|
|25|**D1_Support**bit. 1 = Function supports the D1 PM state.|



**725** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐12: The PMC Register Bit Assignments (Continued)_ 

|**Bit(s)**|**Description**|
|---|---|
|24:22|**Aux_Current**field. For a Function that supports generation of the PME<br>message from the D3coldstate, this field reports the current demand made<br>upon the 3.3Vaux power source (see “Auxiliary Power” on page 775) by<br>the Function’s logic that retains the PME context information. This infor‐<br>mation is used by software to determine how many Functions can simul‐<br>taneously be enabled for PME generation (based on the total amount of<br>current each draws from the system 3.3Vaux power source and the power<br>sourcing capability of the power source).<br>•<br>If the Function does not support PME notification from within the<br>D3coldPM state, this field is not implemented and always returns zero<br>when read. Alternatively, a new feature defined by PCI Express per‐<br>mits devices that do not support PMEs to report the amount of Aux<br>current they draw when enabled by the_Aux Power PM Enable_bit<br>within the Device Control register.<br>•<br>If the Function implements the Data register (see “Data Register” on<br>page 731), this field always returns zeros when read. The Data register<br>then takes precedence over this field in reporting the 3.3Vaux current<br>requirements for the Function.<br>•<br>If the Function supports PME notification from the D3coldstate and<br>does not implement the Data register, then the Aux_Current field<br>reports the 3.3Vaux current requirements for the Function. It is<br>encoded as follows:<br> **Bit**<br> **24 23 22                 Max Current Required**<br>1   1   1                                375mA<br>1   1   0                                320mA<br>1   0   1                                270mA<br>1   0   0                                220mA<br>0   1   1                                160mA<br>0   1   0                                100mA<br>0   0   1                                 55mA<br>0   0   0                                   0mA|



**726** 

**Chapter 16: Power Management** 

_Table 16‐12: The PMC Register Bit Assignments (Continued)_ 

|**Bit(s)**|**Description**|
|---|---|
|21|**Device‐Specific Initialization (DSI)**bit. A one in this bit indicates that<br>immediately after entry into the D0 Uninitialized state, the Function<br>requires additional configuration above and beyond setup of its PCI con‐<br>figuration Header registers before the Class driver can use the Function.<br>Microsoft OSs do not use this bit. Rather, the determination and initializa‐<br>tion is made by the Class driver.|
|20|Reserved.|
|19|**PME Clock**bit. Does not apply to PCI Express. Must be hardwired to 0.|
|18:16|**Version**field. This field indicates the version of the PCI Bus PM Interface<br>spec that the Function complies with.<br>**Bit**<br> **18 17 16       Complies with Spec Version**<br>0   0   1                             1.0<br>0   1   0                             1.1 (required by PCI Express)|



## **PM Control and Status Register (PMCSR)** 

This register, required for all PCI Express Devices, serves several purposes as described below. Table 16‐13 on page 728 provides a description of the PMCSR bit fields. 

- If the Function implements PME capability, a PME Enable bit permits soft‐ ware to enable or disable the Function’s ability to assert the PME message or WAKE# signal, and a Status bit reflects whether or not a PME has occurred. 

- If the optional Data register is implemented (see “Data Register” on page 731), two fields are used to permit software to select which informa‐ tion can be read through the Data register, and provide the scaling multi‐ plier for the Data register value. 

- The register’s PowerState field can be read to determine the current PM state of the Function and written to place the Function into a new PM state. 

**727** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐13: PM Control/Status Register (PMCSR) Bit Assignments_ 

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|31:24|all<br>zeros|Read<br>Only|See “Data Register” on page 731.|
|23|zero|Read<br>Only|Not used in PCI Express|
|22|zero|Read<br>Only|Not used in PCI Express|
|21:16|all<br>zeros|Read<br>Only|Reserved|
|15|See<br>Descrip<br>tion.|Read,<br>Write<br>one to<br>clear,<br>Sticky<br>RW1CS|**PME_Status**bit.**Optional**: only implemented if the<br>Function supports PME notification, otherwise zero.<br>This bit reflects whether the Function has experienced<br>a PME (even if the PME_En bit in this register has dis‐<br>abled the Function’s ability to send a PME message). If<br>set to one, the Function has experienced a PME. Soft‐<br>ware clears this bit by writing a one to it.<br>After reset, this bit is zero if the Function doesn’t sup‐<br>port PME in D3cold. If the Function does support PME<br>in D3cold, this bit is indeterminate at initial OS boot<br>time but after that reflects whether the Function has<br>experienced a PME.<br>If the Function supports PME from D3cold, the state of<br>this bit must persist even if power is lost or the Func‐<br>tion is reset (a sticky bit). This implies that an auxil‐<br>iary power source keeps this logic active during these<br>conditions (see “Auxiliary Power” on page 775).|



**728** 

**Chapter 16: Power Management** 

_Table 16‐13: PM Control/Status Register (PMCSR) Bit Assignments (Continued)_ 

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|14:13|Device‐<br>specific|Read<br>Only|**Data_Scale**field.**Optional**. If the Function does not<br>implement the Data register this field is hardwired to<br>return zeros.<br>If the Data register is implemented, the Data_Scale<br>field is mandatory and must be a read‐only value rep‐<br>resenting the multiplier for it. The value and interpre‐<br>tation of the Data_Scale field depends on the data<br>item selected to be viewed through the Data register<br>by the Data_Select field.|
|12:9|0000b|Read/<br>Write|**Data_Select**field.**Optional**. If the Function does not<br>implement the Data register, this field is hardwired to<br>return zeros.<br>If the Data register is implemented, Data_Select is a<br>mandatory read/write field. The value placed in this<br>register selects the data to be viewed in the Data regis‐<br>ter. That value must then be multiplied by the value<br>read from the Data_Scale field.|



**729** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐13: PM Control/Status Register (PMCSR) Bit Assignments (Continued)_ 

|**Bit(s)**|**Value**<br>**at**<br>**Reset**|**Read/**<br>**Write**|**Description**|
|---|---|---|---|
|8|See<br>Descrip<br>tion.|Read/<br>Write|**PME_En**bit.**Optional**.<br>1 = enable Function’s ability to send PME messages<br>when an event occurs.<br>0 = disable.<br>If the Function does not support the generation of<br>PMEs from any power state, this bit always return<br>zero when read.<br>After reset, this bit is zero if the Function doesn’t sup‐<br>port PME from D3cold. If the Function supports PME<br>from D3cold:<br>• this bit is indeterminate at initial OS boot time.<br>• otherwise, it enables or disables whether the Func‐<br>tion can send a PME message in case a PME occurs.<br>If the Function supports PME from D3cold, the state of<br>this bit must persist while the Function remains in the<br>D3coldstate and during the transition from D3coldto<br>the D0 Uninitialized state. This implies that the PME<br>logic must use an aux power source to power this<br>logic during these conditions.|
|7:2|all<br>zeros|Read<br>Only|Reserved|
|1:0|00b|Read/<br>Write|**PowerState**field.**Mandatory**. Software uses this field<br>to read the current PM state of the Function or write a<br>new PM state. If software selects a PM state not sup‐<br>ported by the Function, the write completes normally<br>but the data is discarded and no state change occurs.<br>  **1 0           PM State**<br>0 0                D0<br>0 1                D1<br>1 0                D2<br>1 1                D3hot|



**730** 

**Chapter 16: Power Management** 

## **Data Register** 

**Optional, read‐only** . Refer to Figure 16‐8 on page 732. The Data register is an 8‐bit, read‐only register that provides software with the following information: 

- Power consumed in the selected PM state; useful in power budgeting. 

- Power dissipated in the selected PM state; useful in managing the thermal environment. 

- Any type of data could be reported through this register, but the PCI‐PM spec only defines power consumption and power dissipation information for it. 

If the Data register is implemented, the Data_Select and Data_Scale fields of the PMCSR registers must also be implemented, and the Aux_Current field of the PMC register must not be implemented. 

**Determining Presence of the Data Register.** Software can perform the following procedure to check for the presence of the Data register: 

1. Write a value of 0000b into the Data_Select field of the PMCSR register. 

2. Read from either the Data register or the Data_Scale field of the PMCSR register. A non‐zero value indicates that the Data register as well as the Data_Scale and Data_Select fields of the PMCSR registers are imple‐ mented. If a value of zero is read, go to step 4. 
