## **ACPI Driver Controls Non-Standard Embedded Devices** 

There are devices embedded on the system board whose register sets do not adhere to any particular industry standard spec. At boot time, the BIOS reports these devices to the OS via the **ACPI tables** , also referred to as the **namespace** . When the OS needs to communicate with any of these devices, it calls the ACPI Driver, which executes a handler called a **Control Method** associated with the device. The handler is also found in the ACPI tables and is written by the plat‐ form designer using a special interpretive language called ACPI Source Lan‐ guage, or **ASL** . The ASL code is then compiled into ACPI Machine Language, or **AML** . Note that AML is not a processor‐specific machine language. It’s a token‐ ized (i.e., compressed) version of the ASL source code. An ACPI Driver incorpo‐ rates an AML token interpreter that allows it to “execute” a Control Method. 

_Figure 16‐1: Relationship of OS, Device Drivers, Bus Driver, PCI Express Registers, and ACPI_ 

**==> picture [348 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
Microsoft<br>OS<br>Interface defined  Interface defined<br>by Microsoft by Microsoft<br>Windows ACPI Written by Microsoft<br>Device Driver Driver to ACPI spec<br>Interface defined<br>by Microsoft<br>Written by Microsoft PCIe Bus AML Control Written by system<br>to OS, PCIe, and PCI  Driver Method board designer to ACPI<br>PM specs and chip-specific specs<br>Non-standard<br>PCIe Function’s  PCIe Function’s  Embedded Register set defined<br>Configuration PM Registers System Board by chip designer<br>Registers Device<br>Register set defined Register set defined<br>by PCIe spec by PCI PM spec and<br>extensions for PCIe<br>**----- End of picture text -----**<br>


**712** 

**Chapter 16: Power Management** 

## **Function Power Management** 

PCI Express Functions are required to support power management, and several registers and related bit fields must be implemented as discussed below. 

## **The PM Capability Register Set** 

The PCI‐PM spec defines the Power Management Capability configuration reg‐ isters. These registers were optional for PCI, but required for PCIe, and are located in the PCI‐compatible configuration space with a Capability ID of 01h. Software can perform the following sequence to locate these registers: 

1. Bit 4 of the Function’s **Configuration Status register** should be set, indicat‐ ing that the Capabilities Pointer in the first byte of dword 13d of the Func‐ tion’s configuration Header is valid. Reading the **Capabilities Pointer register** gives the offset to the first of the Function’s linked list of capability registers. 

2. If the least significant byte of the dword at that offset contains **Capability ID 01h (** see Figure 16‐2 on page 713), this is the PM register set. The byte immediately following the Capability ID byte is the _Pointer to Next Capabil‐ ity_ field that gives the offset in configuration space of the next Capability (if there is one). A non‐zero value is a valid pointer, while a value of 00h indi‐ cates the end of the linked list. A description of all the PM registers can be found in “Detailed Description of PCI‐PM Registers” on page 724. 

_Figure 16‐2: PCI Power Management Capability Register Set_ 

**==> picture [367 x 62] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 8 7 0<br>Power Management Capabilities Pointer to Capability ID<br>(PMC) Next Capability 01h 1st Dword<br>Bridge Support<br>Data Register Extensions Control/Status Register 2nd Dword<br>(PMCSR_BSE) (PMCSR)<br>**----- End of picture text -----**<br>


## **Device PM States** 

Each PCI Express Function must support the full‐on D0 state and the full‐off D3 state, while D1 and D2 are optional. The sections that follow describe the possi‐ ble PM states. 

**713** 

**PCI Ex ress Technolo p gy** 

## **D0 State—Full On** 

**Mandatory.** In this state, no power conservation is in effect and the device is fully operational. All PCIe Functions must support the D0 state and there are technically two substates: D0 Uninitialized and D0 Active. ASPM hard‐ ware control can change the Link power while the Device is in this state. Table 16‐5 on page 714 summarizes the PM policies in the D0 state. 

**D0 Uninitialized.** A Function enters D0 Uninitialized after a Fundamen‐ tal Reset or, in some cases, when software transitions it from D3hot to D0. Usually, the registers are returned to their default state. In this state, the Function exhibits the following characteristics: 

- It only responds to configuration transactions. 

- Its Command register enable bits are all returned to their default states, meaning it cannot initiate transactions or act as the target of memory or IO transactions. 

**D0 Active.** Once the Function has been configured and enabled by soft‐ ware, it is in the D0 Active state and is fully operational. 

_Table 16‐5: D0 Power Management Policies_ 

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers or**<br>**State that must**<br>**be valid**|**Power**|**Actions**<br>**permitted to**<br>**Function**|**Actions**<br>**permitted by**<br>**Function**|
|---|---|---|---|---|---|
|L0|D0 un‐initialized|PME context **|< 10W|PCI Express<br>config transac‐<br>tions.|None|
|L0<br>L0s (required)*<br>L1 (optional)*|D0 active|all|full|Any PCI<br>Express trans‐<br>action.|Any transac‐<br>tion, interrupt,<br>or PME. **|
|L2/L3|D0 active|N/A***||||



* Active State Power Management 

- ** If PME supported in this state. 

- *** This combination of Bus/Function PM states not allowed. 

## **Dynamic Power Allocation (DPA)** 

**Optional** . The 2.1 revision of the base spec added another optional capability that defines 32 more substates for D0 and describes their characteristics. This was intended to facilitate negotiation regarding power management between a 

**714** 

**Chapter 16: Power Management** 

device driver, OS, and an executing application, partly because some Functions don’t have device drivers that handle PM well. One advantage of this model is that the Device technically still remains in the D0 state and may therefore be able to continue operating in a reduced capacity instead of going offline as would be caused by a change to the D1 or lower state. 

DPA registers only apply when the Device power state is in D0 and aren’t appli‐ cable in states D1‐D3. Up to 32 substates can be defined, and they must be con‐ tiguously numbered from zero to the maximum value. Substate 0 is the initial default value and represents the maximum power the Function is capable of consuming. Software is not required to transition between substates in sequen‐ tial order or even wait until a previous transition is completed before requesting another change in the substate. Consequently, when a Function has completed a substate change it must check the configured substate and, if they don’t match, it must begin changing to the configured value. The registers to support DPA, illustrated in Figure 16‐3 on page 715, are found in the Enhanced configuration space. 

_Figure 16‐3: Dynamic Power Allocation Registers_ 

**==> picture [265 x 155] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>DPA Capability Register 004h<br>DPA Latency Indicator Register 008h<br>DPA Control Register DPA Status Register 00Ch<br>010h<br>DPA Power Allocation Array<br>(Sized by number of substates)<br>Up to<br>02Ch<br>**----- End of picture text -----**<br>


The DPA capability register, shown in Figure 16‐4 on page 716, contains several interesting values associated with the substates. The Substate_Max number indicates how many substates are described, and the numbers must increment contiguously from zero to that value. Two Transition Latency Values are given and each substate will be associated with one or the other by the Latency Indica‐ tor register. which contains one bit for each possible substate; if that bit is set Transition Latency Value 1 is used, otherwise Value 0 is used. The latency value gives the maximum time required to transition into that substate from any other 

**715** 

**PCI Ex ress Technolo p gy** 

substate. The latencies are multiplied by the Transition Latency Units to give the time in milliseconds. Similarly, the Power Allocation Scale value gives the multi‐ plier for the power used in each substate, expressed in watts. For each defined substate, a 32‐bit field in the DPA Power Allocation Array describes the power used for that state. The first one of these is located at offset 010h, and the rest are implemented in subsequent dwords. 

_Figure 16‐4: DPA Capability Register_ 

**==> picture [311 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24  23 16  15 14  13  12  11  10   9 8   7        5   4                0<br>Xlcy1 Xlcy0 RsvdZ PAS RsvdZ RsvdZ Substate_Max<br>Transition Latency Value 0 All fields not reserved<br>are read-only<br>Transition Latency Value 1<br>Power Allocation Scale (PAS)<br>Transition Latency Unit (Tlunit)<br>**----- End of picture text -----**<br>


The low‐order five bits of the DPA Control register are written by software to set a new substate, and the current substate can be read from the Status register, as shown in Figure 16‐5 on page 716. Notice that bit 8 of the Status register indi‐ cates whether the use of DPA substates has been enabled but it’s labeled as RW1C (Read, Write 1 to Clear), meaning software can clear this bit but can’t set it. DPA is enabled by default after a reset, and software would need to disable it by writing a one to this bit if it did not intend to use DPA. 

_Figure 16‐5: DPA Status Register_ 

**==> picture [298 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9   8  7          5   4     0<br>RsvdZ RsvdZ<br>Substate Control Enabled (RW1C)<br>Substate status (RO)<br>**----- End of picture text -----**<br>


## **D1 State—Light Sleep** 

**Optional** . Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of 

**716** 

**Chapter 16: Power Management** 

the PCI Express Capability block; when the bit is cleared to zero, it’s safe to pro‐ ceed. In this light power conservation state the Function won’t initiate Requests except PME Messages, if enabled. Other characteristics of the D1 state include: 

- Link is forced to the L1 power state when the Device goes into the D1 state. 

- Configuration and Message Requests are accepted in this state, but all other Requests must be handled as Unsupported Requests and all completions may optionally be handled as Unexpected Completions. 

- If an error is caused by an incoming Request and reporting it is enabled, an Error Message may be sent while in this state. If a different type of error occurs (such as a Completion timeout), the message won’t be sent until the Device is returned to the D0 state. 

- The Function may reactivate the Link and send a PME message, if sup‐ ported and enabled in this state, to notify software that the Function has experienced an event requiring that power be restored. 

- The Function may or may not lose its context in this state. If it does and the device supports PME, it must at least maintain its PME context (see “PME Context” on page 710) while in this state. 

- The Function must be returned to the D0 Active PM state in order to be fully operational. 

Table 16‐6 lists the PM policies while in the D1 state. 

_Table 16‐6: D1 Power Management Policies_ 
