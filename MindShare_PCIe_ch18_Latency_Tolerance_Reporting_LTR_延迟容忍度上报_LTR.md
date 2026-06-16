# 📘 第 18 章　延迟容忍度上报 (LTR) (Chapter 18. Latency Tolerance Reporting (LTR))

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0341.md` ... `chunks/chunk0343.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Latency Tolerance Reporting (LTR)](#-本章目录-table-of-contents)

<a id="sec-18-1"></a>
## 18.1 Latency Tolerance Reporting (LTR) | 延迟容忍度上报 (LTR)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|2|**MRL Sensor Changed**— If an MRL Sensor is implemented, this is<br>set when a MRL Sensor state change is detected. If no sensor is<br>present this bit will always be zero.|
|3|**Presence Detect Changed**— set when a change has been detected in<br>the Presence Detect State bit.|
|4|**Command Completed**— If the No Command Completed Support<br>bit in the Slot Capabilities register is 0b, then this bit is set when a<br>hot plug command has completed and the Hot Plug Controller is<br>ready to accept another command. Technically, only this last mean‐<br>ing is guaranteed: the controller is ready to accept another com‐<br>mand, regardless of whether the previous one has actually<br>completed.|
|5|**MRL Sensor State**— when set, indicates the current state of the<br>MRL sensor, if implemented: 0b = MRL Closed, 1b = MRL Open|
|6|**Presence Detect State**— this bit indicates the presence of a card in a<br>slot and is required for all Downstream Ports that implement a slot.<br>Its value is the logical “OR” of Physical Layer’s Detection logic and<br>any other side‐band detect mechanism implemented for the slot<br>(such as PRSNT1# and PRSNT2#). The big difference between them<br>is that the pins require no power to physically detect the card and<br>can thus report on it without needing the power restored, while<br>using the Physical Layer Detect logic does need power.|



**871** 

**PCI Ex ress Technolo p gy** 

_Table 19‐7: Slot Status Register Fields and Descriptions (Continued)_ 

|**Bit**<br>**Location**|**Register Name and Description**|
|---|---|
|7|**Electromechanical Interlock Status**—If an Electromechanical Inter‐<br>lock is implemented, this bit indicates whether it is engaged (1b) or<br>disengaged (0b).|
|8|**Data Link State Changed**— This bit is set when the Data Link<br>Layer Link Active bit in the Link Status register changes. In response<br>to this event, software must read the Data Link Layer Link Active bit<br>to determine whether the Link is active before sending configura‐<br>tion cycles to the hot plugged device.|



## **Add-in Card Capabilities** 

The Device Capability register, seen in Figure 19‐8 on page 873, also has fields relevant to add‐in cards that record the power reported by the Hot Plug Con‐ troller as being available to their slot. This information must be communicated automatically with a Set_Slot_Power_Limit Message whenever either of these takes place: 

- A configuration write to the Slot Capabilities register changes the Slot Power Limit Value and Slot Power Limit Scale values. 

- The Link transitions from non‐DL_UP to DL_Up status (unless the Slot Capabilities register has not yet been initialized). 

The message updates the Captured Slot Power Limit Value and Scale registers with the values in the message, making this information readily available to its device driver. 

**872** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Figure 19‐8: Device Capabilities Register_ 

**==> picture [386 x 235] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 29 28 27 26 25 18 17 1615 14 12 11 9 8 6 5 4 3 2 0<br>RsvdP Undefined<br>Function-Level<br>Reset Capability<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>RsvdP<br>Role-Based Error Reporting<br>Endpoint L1 Acceptable Latency<br>Endpoint L0 Acceptable Latency<br>Extended Tag Field Supported<br>Phantom Functions Supported<br>Max Payload Size Supported<br>**----- End of picture text -----**<br>


## **Quiescing Card and Driver** 

## **General** 

Prior to removing a card from the system, two things must occur: the device driver must stop accessing the card, and the card must stop initiating or responding to new Requests. How this is accomplished is OS‐specific, but the following must take place: 

- The OS must stop issuing new requests to the device’s driver or instruct the driver to stop accepting new requests. 

- The driver must terminate or complete all outstanding requests. 

- The card must be disabled from generating interrupts or Requests. 

When the OS commands the driver to quiesce itself and its device, the OS must not expect the device to remain in the system (in other words, it could be removed and not replaced with an identical card). 

**873** 

**PCI Ex ress Technolo p gy** 

## **Pausing a Driver (Optional)** 

Optionally, an OS could implement a “Pause” capability to temporarily stop driver activity in the expectation that the same card will be reinserted. If the card is not reinstalled within a reasonable amount of time, however, the driver must be quiesced and then removed from memory. 

As an example, the currently‐installed card is failing or is being replaced with a later revision as an upgrade. If the operation is to appear seamless from a soft‐ ware and operational perspective, the driver would have to quiesce the device, save the current context (contents of registers, stack and instruction pointer of local micro‐controller, etc.) and turn off the power to the slot. The new card could then be installed and powered, and then, when its context is restored, it could resume normal operation where it left off. Of course, if the old card had failed, it may not be possible to simply resume operation. 

## **Quiescing a Driver That Controls Multiple Devices** 

If a driver controls multiple cards and it receives a command from the OS to quiesce its activity with respect to a specific card, it must only quiesce its activ‐ ity with that card and the card itself. 

## **Quiescing a Failed Card** 

If a card has failed, it may not be possible for the driver to complete requests previously issued to the card. In this case, the driver must detect the error, ter‐ minate the requests without completion, and attempt to reset the card. 

## **The Primitives** 

This section discusses the hot‐plug software elements and the information passed between them. For a review of the software elements and their relation‐ ships to each other, refer to Table 19‐1 on page 852. Communications between the Hot‐Plug Service within the OS and the Hot‐Plug System Driver is in the form of requests. The spec doesn’t define the exact format of these requests, but does define the basic request types and their content. Each request type issued to the Hot‐Plug System Driver by the Hot‐Plug Service is referred to as a _primi‐ tive_ . They are listed and described in Table 19‐8 on page 875. 

**874** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐8: The Primitives_ 

|**Primitive**|**Parameters**|**Description**|
|---|---|---|
|Query Hot‐Plug<br>System Driver|**Input**: None|Requests that the Hot‐Plug System<br>Driver return a set of Logical Slot<br>IDs for the slots it controls.|
||**Return**: Set of Logical Slot<br>IDs for slots controlled by<br>this driver.||
|Set Slot Status|**Inputs**:<br>• Logical Slot ID<br>• New slot state (on or<br>off).<br>• New Attention Indica‐<br>tor state.<br>• New Power Indicator<br>state.|This request is used to control the<br>slots and the Attention Indicator<br>associated with each slot. Good<br>completion of a request is indicated<br>by returning the Status Change Suc‐<br>cessful parameter. If a fault is<br>incurred during an attempted sta‐<br>tus change, the Hot‐Plug System<br>Driver should return the appropri‐<br>ate fault message (see middle col‐<br>umn). Unless otherwise specified,<br>the card should be left in the off<br>state.|
||**Return**: Request comple‐<br>tion status:<br>• status change successful<br>• fault—wrong frequency<br>• fault—insufficient<br>power<br>• fault—insufficient con‐<br>figuration resources<br>• fault—power fail<br>• fault—general failure||
|Query Slot<br>Status|**Input**: Logical Slot ID|This request returns the state of the<br>indicated slot (if a card is present).<br>The Hot‐Plug System Driver must<br>return the Slot Power status infor‐<br>mation.|
||**Return**:<br>• Slot state (on or off)<br>• Card power require‐<br>ments.||



**875** 

**PCI Ex ress Technolo p gy** 

_Table 19‐8: The Primitives (Continued)_ 

|**Primitive**|**Parameters**|**Description**|
|---|---|---|
|Async Notice of<br>Slot Status<br>Change|**Input**: Logical Slot ID|This is the only primitive (defined<br>by the spec) that is issued to the<br>Hot‐Plug Service by the Hot‐Plug<br>System Driver. It is sent when the<br>Driver detects an unsolicited<br>change in the state of a slot. Exam‐<br>ples would be a run‐time power<br>fault or a card installed in a previ‐<br>ously‐empty slot with no warning.|
||**Return**: none||



## **Introduction to Power Budgeting** 

The primary goal of the PCI Express power budgeting capability is to allocate power for PCI Express hot plug devices that are added to the system during runtime. This ensures that the system can allocate the proper amount of power and cooling for these devices. 

The spec states that “power budgeting capability is optional for PCI Express devices implemented in a form factor which does not require hot plug, or that are integrated on the system board.” None of the form factor specs released at the time of this writing required support for hot plug or the power budgeting capability, but these change often. 

System power budgeting is always required to support all system board devices and add‐in cards. The new capability provides mechanisms for managing the budgeting process for a hot‐plug card. Each form factor spec defines the min and max power for a given expansion slot. For example, the CEM spec limits the power an expansion card can consume prior to being fully enabled but, after it is enabled, it can consume the maximum amount of power specified for the slot. In the absence of the power budgeting capability registers, the system designer is responsible for guaranteeing that power has been budgeted cor‐ rectly and that sufficient cooling is available to support any compliant card installed into the connector. 

The spec defines the configuration registers to support the power budgeting process, but does not define the power budgeting methods and processes. The next section describes the hardware and software elements that would be involved in power budgeting, including the specified configuration registers. 

**876** 

**Chapter 19: Hot Plug and Power Budgeting** 

## **The Power Budgeting Elements** 

Figure 19‐10 illustrates the concept of Power Budgeting for hot plug cards. The role of each element involved in the power budgeting, allocation, and reporting process is listed and described below: 

- System Firmware for Power Management (used during boot time). 

- Power Budget Manager (used during run time). 

- Expansion Ports (to which card slots are attached). 

- Add‐in Devices (Power Budget Capable). 

## **System Firmware** 

Written by the platform designers the specific system, this is responsible for reporting system power information. The spec recommends the following power information be reported to the PCI Express power budget manager, which allocates and verifies power consumption and dissipation during runt‐ ime: 

- Total system power available. 

- Power allocated to system devices by firmware 

- Number and type of slots in the system. 

Firmware may also allocate power to PCIe devices that support the power bud‐ geting capability register set, such as a hot‐plug device used during boot time. The Power Budgeting Capability register, shown in Figure 19‐9 on page 878, contains a System Allocated bit that is hardware initialized (usually by firm‐ ware) to notify the power budget manager that power for this device has already been included in the system power allocation. If so, the Power Budget Manager still needs to read and save the power information for the hot‐plug devices that were allocated in case they are later removed during runtime. 

**877** 

**PCI Ex ress Technolo p gy** 

_Figure 19‐9: Power Budget Registers_ 

**==> picture [379 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-18-2"></a>
## 18.2 Latency Tolerance Reporting (LTR) | 延迟容忍度上报 (LTR)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

31                                                                                               0<br>Offset<br>PCIe Extended Capability Header 00h<br>Data Select<br>RsvdP 04h<br>Register<br>Data Register 08h<br>Power Budget<br>RsvdP 0Ch<br>Capability Register<br>System Allocated Bit<br>Bit 0 of Power Budget Capability Register<br>**----- End of picture text -----**<br>


## **The Power Budget Manager** 

This initializes when the OS installs and receives power‐budget information from system firmware, although the spec does not define the method for deliv‐ ering this information. This manager is responsible for allocating power for all PCI Express devices including: 

- PCI Express devices that have not already been allocated by the system (including embedded devices that support power budgeting). 

- Hot‐plugged devices installed at boot time. 

- New devices added during runtime. 

## **Expansion Ports** 

Figure 19‐10 on page 880 illustrates a hot plug port that must have the Slot Power Limit and Slot Power Scale fields within the Slot Capabilities register implemented. The firmware or power budget manager must load these fields with a value that represents the maximum amount of power supported by this Port. When software writes to these fields the Port automatically delivers a Set_Slot_Power_Limit message to the device. These fields are also written when software configures a new card that has been added as a hot plug installation. 

**878** 

**Chapter 19: Hot Plug and Power Budgeting** 

## Spec requirements: 

- Any Downstream Port that has a slot attached (the Slot Implemented bit in its PCIe Capabilities register is set) must implement the Slot Capabilities register. 

- Software must initialize the Slot Power Limit Value and Scale fields of the Slot Capabilities register of the Downstream Port that is connected to an add‐in slot. 

- Upstream Ports must implement the Device Capabilities register. 

- When a card is installed in a slot and software updates the power limit and scale values in the Downstream Port, that Port will automatically send the Set_Slot_Power_Limit message to the Upstream Port on the installed card. 

- The recipient of the Message must use the data payload to limit its power usage for the entire card, unless the card will never exceed the lowest value specified in the corresponding electromechanical spec. 

## **Add-in Devices** 

Expansion cards that support the power budgeting capability must include the Slot Power Limit Value and Slot Limit Scale fields within the Device Capabilities register, and the Power Budgeting Capability register set for reporting power‐ related information. 

These devices must not consume more than the lowest power specified by the form factor spec. Once power budgeting software allocates additional power via the Set_Slot_Power_Limit message, the device can consume the power that has been specified, but not until it has been configured and enabled. 

**Device Driver** —The device’s software driver is responsible for verifying that sufficient power is available for proper device operation prior to enabling it. If the power is lower than that required by the device, the device driver is respon‐ sible for reporting this to a higher software authority. 

**879** 

**PCI Ex ress Technolo p gy** 

_Figure 19‐10: Elements Involved in Power Budget_ 

**==> picture [371 x 480] intentionally omitted <==**

**----- Start of picture text -----**<br>
Operating<br>Firmware<br>Power  Budgeting<br>System<br>Reports Power Budget Info<br>Device to Power Manager including:<br>Driver 1 Power Budget<br>Manager<br>- Total system power budget<br>- Total power allocated to system<br>  Devices board devices.<br>- Total number and type of slots<br>PCIe<br>Bus Driver<br>Configures Ports<br>Root or Switch Port with Power Limit<br>Information<br>Slot Capabilities Register<br>Hot-Plug<br>Controller 1 31 19 18 17 16 15 14 7 6 5 4 3 2 0<br>Physical Slot Number<br>Slot Power Scale<br>Slot Power Value<br>PortPort<br>InterfaceInterface Root or Switch port<br>sends power limit<br>message to add-in card.<br>Device Capabilities Register<br>31 28 27 26 25 18 17 15 14 13 12 11 9 8 6 5 4 3 2 0<br>RsvdP<br>Captured Slot Power Limit Value<br>Captured Slot Power Limit Scale<br>Power Budget Capability Registers<br>31                                                                                               0<br>PCIe Extended Capability Header<br>RsvdP Data Select Register<br>Data Register<br>RsvdP Power Budget Capability<br>Register<br>Indicator Ctl Hot Plug Stat Hot Plug Ctl<br>**----- End of picture text -----**<br>


**880** 

**Chapter 19: Hot Plug and Power Budgeting** 

## **Slot Power Limit Control** 

Software is responsible for determining the maximum power that an expansion device is allowed to consume. This allocation is based on the power partitioning within the system, thermal capabilities, etc. Knowledge of the system’s power and thermal limits comes from system firmware. The firmware or power man‐ ager is responsible for reporting the power limits to each expansion port. 

## **Expansion Port Delivers Slot Power Limit** 

Software writes to the _Slot Power Limit Value_ and _Slot Power Limit Scale_ fields of the Slot Capability register to specify the maximum power that can be con‐ sumed by the device. Software is required to specify a power value that reflects one of the maximum values defined by the spec. For example, revision 2.0 of the CEM spec defines power usage as listed in Table 19‐9. 

An interesting note about these values is that a standard‐height x1 server card is limited to 10W after a reset and is only allowed to use the full 25W after it’s been configured and enabled. Similarly, a x16 graphics card will be limited to 25W until configured and enabled to use the full 75W. 

_Table 19‐9: Maximum Power Consumption for System Board Expansion Slots_ 

||**X1 Link**|**X1 Link**|**X4/X8 Link**|**X16 Link**|**X16 Link**|
|---|---|---|---|---|---|
|Standard Height|10W<br>(max ‐<br>desktop)|25W<br>(max ‐<br>server)|25W (max)|25W<br>(max ‐<br>server)|75W<br>(max ‐<br>graph‐<br>ics card)|
|Low Profile Card|10W (max)||25W (max)|25W (max)||



In addition to the base CEM spec, two more specs have been defined for higher‐ powered devices. First is the PCIe x16 Graphics 150W‐ATX Spec 1.0, which defines a video card that’s able to draw 75W from the card connector and another 75W from a separate 3‐pin ATX power connector. The second is the PCIe 225W/300W High Power CEM Spec 1.0, which extends this by adding another 3‐pin power connector to achieve 225W, or a 4‐pin ATX connector that brings the total to 300W. 

**881** 

## **PCI Ex ress Technolo p gy** 

When the Slot Power registers are written by power budget software, the expan‐ sion port sends a Set_Slot_Power_Limit message to the expansion device. This procedure is illustrated in Figure 19‐11 on page 882. 

_Figure 19‐11: Slot Power Limit Sequence_ 

**==> picture [367 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root or Switch Port<br>Slot Capabilities Register<br>Hot-Plug<br>Controller 1 31 19 18 17 16 15 14 7 6 5 4 3 2 0<br>Physical Slot Number<br>Slot Power Scale<br>Slot Power Value<br>PortPort<br>InterfaceInterface Root or Switch port<br>sends power limit<br>message to add-in card.<br>Device Capabilities Register<br>31 28 27 26 25 18 17 15 14 13 12 11 9 8 6 5 4 3 2 0<br>RsvdP<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>Indicator Ctl Hot Plug Stat Hot Plug Ctl<br>**----- End of picture text -----**<br>


1. When Hot Plug software is notified of a card insertion request, Power and Clock are restored to the slot. 

2. Hot Plug software calls configuration and power budgeting software to configure and allocate power to the device. 

3. Power budget software may interrogate the card to determine it's power requirements and characteristics. 

4. Power is then allocated based on the device's requirements and the system's capabilities 5. Power management software writes to the Slot Power Scale and Slot Power Value fields within the expansion port. 

6. Writes to these fields command the port to send the Set_Slot_Power_Limit message to convey the contents of the Slot Power fields. 

7. The slot receives the message and updates its Captured Slot Power Limit Value and Scale fields. 

8. These values limit the power that the expansion device can consume once it is enabled by its device driver. 

**882** 

**Chapter 19: Hot Plug and Power Budgeting** 

## **Expansion Device Limits Power Consumption** 

The device driver reads the values from the Captured Slot Power Limit and Scale fields to verify that the power available is sufficient to operate the device. Several conditions may exist: 

- Enough power is available to operate the device at full capability. In this case, the driver enables the device by writing to the configuration Com‐ mand register, permitting the device to consume power up to the limit spec‐ ified in the Power Limit fields. 

- The power available is sufficient to operate the device but not at full capa‐ bility. In this case, the driver is required to configure the device such that it consumes no more power than specified in the Power Limit fields. 

- The power available is insufficient to operate the device. In this case, the driver must not enable the card and must report the inadequate power con‐ dition to the upper software layers, which should in turn inform the end user of the problem. 

- The power available exceeds the maximum power specified by the form factor spec. This condition should not occur. but, if it does, the device is not permitted to consume power beyond the maximum permitted by the form factor. 

- The power available is less than the lowest value specified by the form fac‐ tor spec. This is a violation of the spec, which states that the expansion port “must not transmit a Set_Slot_Power_Limit Message that indicates a limit lower than the lowest value specified in the electromechanical spec for the slotʹs form factor.” 

Some expansion devices may consume less power than the lowest limit speci‐ fied for their form factor. Such devices are permitted to discard the information delivered in the Set_Slot_Power_Limit Messages. When the Slot Power Limit Value and Scale fields are read, these devices return zeros. 

## **The Power Budget Capabilities Register Set** 

These registers permit power budgeting software to allocate power more effec‐ tively based on information provided by the device through its power budget data select and data register. This feature is similar to the data select and data fields within the power management capability registers. However, the power budget registers provide more detailed information to software to aid it in determining the effects of expansion cards that are added during runtime on 

**883** 

## **PCI Ex ress Technolo p gy** 

the system power budget and cooling requirements. Through this capability, a device can report the power it consumes: 

- from each power rail 

- in various power management states 

- in different operating conditions 

These registers are not required for devices implemented on the system board or on expansion devices that do not support hot plug. Figure 19‐12 on page 884 illustrates the power budget capabilities register set and shows the data select and data field that provide the method for accessing the power budget informa‐ tion.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-18-3"></a>
## 18.3 Latency Tolerance Reporting (LTR) | 延迟容忍度上报 (LTR)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
