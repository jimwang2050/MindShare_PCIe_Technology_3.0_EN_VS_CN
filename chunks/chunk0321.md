3. If the current value of the Data_Select field is a value other than 1111b, go to step 4. If the current value of the Data_Select field is 1111b, all pos‐ sible Data register values have been scanned and returned zero, indicat‐ ing that neither the Data register nor the Data_Scale and Data_Select fields of the PMCSR registers are implemented. 

4. Increment the content of the Data_Select field and go back to step 2. Since the data select field is only 4 bits, a complete scan requires testing 16 possible select values and looking to see if any non‐zero values are seen for the data and scale registers. 

**Operation of the Data Register.** The information returned is typically a static copy of the Function’s worst‐case power consumption and power dis‐ sipation characteristics in the various PM states (as listed in the Device’s data sheet). To use the Data register, the programmer uses the following sequence: 

1. Write a value into the Data_Select field (see Table 16‐14 on page 733) of the PMCSR register to select the data item to be viewed through the Data register. 

**731** 

**PCI Ex ress Technolo p gy** 

2. Read the data value from Data register and the Data_Scale field of the PMCSR register. 

3. Multiply the value by the scaling factor. 

**Multi‐Function Devices.** In a multi‐function PCI Express device, each Function must supply its own power information. The power information for the logic common to all the Functions is reported through Function zero’s Data register (see Data Select Value = 8 in Table 16‐14 on page 733). 

**Virtual PCI‐to‐PCI Bridge Power Data.** The spec doesn’t specify data field use in PCI‐to‐PCI bridge Functions in a Root Complex or Switch. But, to maintain PCI‐PM compatibility, bridges must report the power informa‐ tion they consume. Software could read the virtual PPB Data registers at each port of a switch to determine the power consumed by the switch in each power state. 

_Figure 16‐8: PM Registers_ 

|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|**Capability ID**<br>**01h**<br>**Pointer to**<br>**Next Capability**<br>1st Dword<br>2nd Dword<br>0<br>7<br>8<br>15<br>16<br>31<br>**Power Management Capabilities**<br>**(PMC)**<br>**Data Register**<br>**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**<br>**Control/Status Register**<br>**(PMCSR)**|
|---|---|---|---|
|**Power Management Capabilities**<br>**(PMC)**||**Pointer to**<br>**Next Capability**|**Capability ID**<br>**01h**|
|**Data Register**|**Bridge Support**<br>**Extensions**<br>**(PMCSR_BSE)**|**Control/Status Register**<br>**(PMCSR)**||



**732** 

**Chapter 16: Power Management** 

_Table 16‐14: Data Register Interpretation_ 

|**Data Select Value**|**Data Reported in**<br>**Data Register**|**Interpretation of Data**<br>**Scale Field in PMCSR**|**Units/**<br>**Accuracy**|
|---|---|---|---|
|00h|Power consumed in D0|00b = unknown<br>01b = multiply by 0.1<br>10b = multiply by 0.01<br>11b = multiply by 0.001|Watts|
|01h|Power consumed in D1|||
|02h|Power consumed in D2|||
|03h|Power consumed in D3|||
|04h|Power dissipated in D0|||
|05h|Power dissipated in D1|||
|06h|Power dissipated in D2|||
|07h|Power dissipated in D3|||
|08h|In a multi‐function PCI<br>device, Function 0 indi‐<br>cates power consumed<br>by logic common to all<br>Functions in the pack‐<br>age.|||
|09h‐0Fh|Reserved for future use<br>of Function 0 in a<br>multi‐function device.|Reserved|TBD|
|08h‐0Fh|Reserved in single‐func‐<br>tion devices and Func‐<br>tions other than<br>Function 0 in a<br>multi‐function device|||



## **Introduction to Link Power Management** 

We’ve just seen how software can put Devices into one of several device power states, now let’s consider how PCIe also manages Link power. Device power and Link power are related to each other, as shown in Table 16‐15 on page 734. Note also the relationship between downstream and upstream devices, which can be summarized by saying that an upstream Device or Link cannot be in a more aggressive power‐conserving state than the one below it. The reason is to 

**733** 

**PCI Ex ress Technolo p gy** 

facilitate timely delivery of packets from the Endpoints, whose traffic would be delayed if upstream devices were in a lower power state. Each relationship is described below: 

**D0** — Device is fully powered and typically in the L0 Link state. Some power conservation is available without leaving this state by using DPA substates (see “Dynamic Power Allocation (DPA)” on page 714), and by using the hard‐ ware‐based Link power management (see “Active State Power Management (ASPM)” on page 735 for more details). 

**D1 & D2** — When software changes the device state to D1 or D2, the Link must automatically transition to the L1 state. Since both Link partners are involved in this operation there is a handshake mechanism to ensure that things are done in an orderly fashion. 

**D3hot** — When software places a device into the D3 state, the Link automati‐ cally transitions to L1 just as it does when going to the D1 and D2 states. Soft‐ ware may now choose to remove the reference clock and power, putting the device into D3cold. But, before doing that, it’s expected that the system will ini‐ tiate a handshake process to prepare the Links by putting them into the L2/L3 Ready state. 

**D3cold** — In this state, main power and the reference clock have been turned off. However, auxiliary power (VAUX) may be available, allowing the device to sig‐ nal a wakeup event to the system. If it is, the Link state will be in L2. If main power is removed but VAUX is not available, the Link will be in L3. Table 16‐16 on page 735 provides additional information regarding the Link power states. 

_Table 16‐15: Relationship Between Device and Link Power States_ 

|**Downstream**<br>**Component D‐State**|**Permissible Upstream**<br>**Component D‐State**|**Permissible**<br>**Interconnect State**|
|---|---|---|
|D0|D0|L0, L0s & L1 (optional)|
|D1|D0‐D1|L1|
|D2|D0‐D2|L1|
|D3 hot|D0‐D3 hot|L1, L2/L3 Ready|
|D3 cold|D0‐D3 cold|L2 (AUX Pwr), L3|



**734** 

**Chapter 16: Power Management** 

## _Table 16‐16: Link Power State Characteristics_ 

|**State**|**Description**|**Software**<br>**Directed?**|**Active**<br>**State**<br>**Link PM**|**Ref.**<br>**Clocks**|**Main**<br>**Power**|**PLL**|**Vaux**|
|---|---|---|---|---|---|---|---|
|L0|Fully Active|Yes (D0)|On|On|On|On|On/Off|
|L0s|Standby|No|Yes<br>(D0)|On|On|On|On/Off|
|L1|Low Power<br>Standby|Yes*<br>(D1‐D3 hot)|Yes(option)<br>(D0)|On|On|On/Off|On/Off|
|L2/L3<br>Ready|Staging for<br>power<br>removal|Yes<br>PME_Turn_Off<br>handshake|No|On|On|On/Off|On/Off|
|L2|Low Power<br>Sleep|Yes**|No|Off|Off|Off|On|
|L3|Off<br>(Zero Power)|N/A|N/A|Off|Off|Off|Off|



- The L1 state is entered either due to PM software placing a device into the D1, D2, or D3 states or under hardware control with ASPM. 

- ** The spec describes the L2 state as being software directed. The other L‐states in the table are listed as software directed because software initiates the transition into these states. For example, when software initiating a device power state change to D1, D2, or D3 devices must respond by enter‐ ing the L1 state. Software then causes the transition to the L2/L3 Ready state by initiating a PME_Turn_Off message. Finally, software initiates the removal of power from a device after the device has transitioned to the L2/ L3 Ready state. Because Vaux power is available in L2, a wakeup event can be signaled to notify software. 

## **Active State Power Management (ASPM)** 

ASPM is a hardware‐based Link power conservation mechanism that only applies while the device is in the D0 device power state. Transitions into and out of ASPM states are initiated by hardware based on implementation‐specific cri‐ teria; software can’t control or observe this operation, it can only enable or dis‐ able it using configuration register bits (see Figure 16‐15 on page 744). 

**735** 

**PCI Ex ress Technolo p gy** 

Two low power states are defined for ASPM: 

1. L0s (standby state) — This state provide substantial power savings but still allows quick entry and exit latencies. The main way this is done is by put‐ ting the Transmitter into the Electrical Idle condition. Support for this state was previously required for all PCIe devices in the earlier spec versions, but in the 3.0 spec it became optional. 

2. L1 ASPM — The goal for L1 is to achieve greater power conservation than L0s for situations where longer entry and exit latencies are acceptable. For example, in this state both Transmitters go into Electrical Idle at the same time. Support for this state continues to be optional in the 3.0 spec as it was in the earlier specs. 

## **Electrical Idle** 

Since putting a Transmitter into Electrical Idle is a central part of ASPM, it will help to discuss how doing so works. When a Transmitter’s differential signals (TxD+ and TxD‐) goes into the Electrical Idle condition, it stops signaling and instead holds its voltage very close to the common mode voltage with a differ‐ ential voltage of 0 V. Signal transitions consume power, so stopping them on the Link gives power savings while still allowing a fairly quick resumption back to normal Link activity during which it is said to be in the L0 state. Depending on the degree of power savings, the Link is either in the L0s or L1 state. During this time, the transmitter may choose to remain in the low‐impedance state or change to high impedance by turning off its termination logic to save more power. In addition to L0s and L1, Electrical Idle will also be in effect when the Link has been disabled. 

## **Transmitter Entry to Electrical Idle** 

Transmitters that wish to enter the Electrical Idle condition must first inform the Link partner so the lack of further signaling won’t be misinterpreted as an error. They do that by sending the EIOS (Electrical Idle Ordered‐Set) and then quickly ceasing transmission and tri‐stating the Link output drivers. What the EIOS looks like depends on the encoding method in use, as described in the following sections. Once the last EIOS has been sent, the Transmitter must enter Electrical Idle within 8ns and remain in that mode for at least 20ns, regardless of the data rate. The differential peak voltage allowed during Electrical Idle must be between 0 and 20mV peak, again regardless of the data rate, to reduce the chance of the Receiver misinterpreting noise on the line as a valid signal. (See Table 13‐3 on page 489 for more on these timing and voltage parameters.) 

**736** 

**Chapter 16: Power Management** 

**Gen1/Gen2 Mode Encoding.** For Gen1/Gen2 mode, the EIOS takes the form shown in Figure 16‐9 on page 737. All four Symbols must be sent, but the Receiver only needs to see two IDL control characters to recognize this condition. 

_Figure 16‐9: Gen1/Gen2 Mode EIOS Pattern_ 

**==> picture [134 x 100] intentionally omitted <==**

**----- Start of picture text -----**<br>
Encoding<br>COM K28.5<br>IDL K28.3<br>IDL K28.3<br>IDL K28.3<br>**----- End of picture text -----**<br>

