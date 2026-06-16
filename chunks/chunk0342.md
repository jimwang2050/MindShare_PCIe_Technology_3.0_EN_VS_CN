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
