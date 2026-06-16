The PCIe spec, together with the Card ElectroMechanical (CEM) spec, defines the slot signals and the support required for Hot Plug PCI Express. Following is a list of required and optional port interface signals needed to support the Stan‐ dard Usage Model: 

- PWRLED# (required) — port output that controls state of Power Indicator 

- ATNLED# (required) — port output controls state of Attention Indicator 

- PWREN (required if reference clock is implemented) — port output that controls main power to slot 

- REFCLKEN# (required) — port output that controls delivery of reference clock to the slot 

- PERST# (required) — port output that controls PERST# at slot 

- PRSNT1# (required) — Grounded at the connector 

- PRSNT2# (required) — port input, pulled up on system board, that indi‐ cates presence of card in slot. 

- PWRFLT# (required) — port input that notifies the Hot‐Plug controller of a power fault condition detected by external logic 

- AUXEN# (required if AUX power is implemented) — port output that con‐ trols switched AUX signals and AUX power to slot when MRL is opened and closed. The MRL# signal is required with AUX power is present. 

- MRL# (required if MRL Sensor is implemented) — port input from the MRL sensor 

- BUTTON# (required if Attention Button is implemented) — port input indi‐ cating operator has pressed the Attention Button. 

**863** 

**PCI Ex ress Technolo p gy** 

_Figure 19‐3: Hot Plug Control Functions within a Switch_ 

## **The Hot-Plug Controller Programming Interface** 

The standard programming interface to the Hot‐Plug Controller is provided via the PCI Express Capability register block, shown in Figure 19‐4 on page 865, where the Hot‐Plug related registers are highlighted. Hot Plug features are pri‐ 

**864** 

**Chapter 19: Hot Plug and Power Budgeting** 

marily found in the Slot Registers defined for Root and Switch Ports. The Device Capability register is also used in some implementations as described later in this chapter. 

_Figure 19‐4: PCIe Capability Registers Used for Hot‐Plug_ 

**==> picture [263 x 305] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 15 7 0<br>PCI Express Capabilities Register Next Cap Pointer PCI ExpressCap ID DW0<br>Device Capabilities Register DW1<br>Device Status Device Control DW2<br>Link Capabilities DW3<br>Link Status Link Control DW4<br>Slot Capabilities DW5<br>Slot Status Slot Control DW6<br>Root Capability Root Control DW7<br>Root Status DW8<br>Device Capabilities 2 DW9<br>Device Status 2 Device Control 2 DW10<br>Link Capabilities 2 DW11<br>Link Status 2 Link Control 2 DW12<br>Slot Capabilities 2 DW13<br>Slot Status 2 Slot Control 2 DW14<br>**----- End of picture text -----**<br>


## **Slot Capabilities** 

Figure 19‐5 on page 866 illustrates the slot capability register and bit fields. Hardware initializes all of these capability register fields to reflect the features implemented by this port. This register applies to both card slots and rack mount implementations, except for the indicators and attention button. Soft‐ ware must read from the device capability register within the module to deter‐ mine if indicators and attention buttons are implemented. Table 19‐5 on page 866 lists and defines the slot capability fields. 

**865** 

**PCI Ex ress Technolo p gy** 

_Figure 19‐5: Slot Capabilities Register_ 

||Hot Plug Surprise<br>Slot Power Limit Scale<br>5<br>0<br>6<br>7<br>31<br>14<br>3 2<br>4<br>15<br>16<br>18 17<br>19<br>Attention Button Present<br>Power Controller Present<br>MRL Sensor Present<br>Attention Indicator Present<br>Electromechanical Interlock Present<br>Physical Slot Number<br>Slot Power Limit Value<br>Hot Plug Capable<br>Power Indicator Present<br>No Command Completed Support|Hot Plug Surprise<br>Slot Power Limit Scale<br>5<br>0<br>6<br>7<br>31<br>14<br>3 2<br>4<br>15<br>16<br>18 17<br>19<br>Attention Button Present<br>Power Controller Present<br>MRL Sensor Present<br>Attention Indicator Present<br>Electromechanical Interlock Present<br>Physical Slot Number<br>Slot Power Limit Value<br>Hot Plug Capable<br>Power Indicator Present<br>No Command Completed Support|
|---|---|---|
||**Bit(s)**|**Register Name and Description**|
||0|**Attention Button Present**— indicates the presence of an attention button<br>on the chassis adjacent to the slot.|
||1|**Power Controller Present**— indicates the presence of a power controller<br>for this slot.|
||2|**MRL Sensor Present**— indicates the presence of a MRL Sensor on the<br>slot.|
||3|**Attention Indicator Present**— indicates the presence of an attention indi‐<br>cator on the chassis adjacent to the slot.|
||4|**Power Indicator Present**— indicates the presence of a power indicator on<br>the chassis adjacent to the slot.|



**866** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐5: Slot Capability Register Fields and Descriptions (Continued)_ 

|**Bit(s)**|**Register Name and Description**|
|---|---|
|5|**Hot‐Plug Surprise**— indicates that it’s possible for the user to remove the<br>card from the system without prior notification. This tells the OS to allow<br>for such removal without affecting continued software operation.|
|6|**Hot‐Plug Capable**— indicates that this slot supports hot plug operation.|
|14:7|**Slot Power Limit Value**— specifies the maximum power that can be sup‐<br>plied by this slot. This limit value is multiplied by the scale specified in the<br>next field.|
|16:15|**Slot Power Limit Scale**— specifies the scaling factor for the Slot Power<br>Limit Value.|
|17|**ElectroMechanical Interlock Present**— indicates that this is implemented<br>for this slot|
|18|No Command Completed Support— indicates that this slot doesn’t gener‐<br>ate software notification when a command has been completed. Earlier<br>versions sometimes took a long time to execute hot‐plug commands (for<br>example, sometimes taking a second or more to communicate across an<br>I2C bus to turn the power on or off), and generated an interrupt when they<br>were finally done. When set this bit means that this Port can accept writes<br>to all fields in the Slot Control register without delay, so there’s no need for<br>the notification.|
|31:19|P**hysical Slot Number**— Indicates the physical slot number associated<br>with this port. It must be hardware initialized to a number that is unique<br>within the chassis. Note that software will need this number to relate the<br>physical slot to the Logical Slot ID (Bus, Device, & Function number for<br>this device).|



## **Slot Power Limit Control** 

The spec provides a method for software to limit the amount of power con‐ sumed by a card installed into an expansion slot or backplane implementation. The registers to support this feature are included in the Slot Capability register. 

**867** 

**PCI Ex ress Technolo p gy** 

## **Slot Control** 

Software controls the Hot Plug events through the Slot Control register, shown in Figure 19‐6 on page 868. This register permits software to enable various Hot Plug features and control hot plug operations. It’s also used to enable interrupt generation as well as enabling the sources of Hot‐Plug events that can result in interrupt generation. 

_Figure 19‐6: Slot Control Register_ 

**==> picture [385 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 13 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Data Link Layer<br>State Changed Enable<br>Electromechanical<br>Interlock Control<br>Power Controller Control<br>Power Indicator Control<br>Attention Indicator Control<br>Hot Plug Interrupt Enable<br>Command Completed Interrupt Enable<br>Presence Detect Changed Enable<br>MRL Sensor Changed Enable<br>Power Fault Detected Enable<br>Attention Button Pressed Enable<br>**----- End of picture text -----**<br>


**868** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐6: Slot Control Register Fields and Descriptions_ 

|**Bit(s)**|**Register Name and Description**|
|---|---|
|0|**Attention Button Pressed Enable.**When set, this bit enables the genera‐<br>tion of a hot‐plug interrupt (if enabled) or assertion of the Wake# message,<br>when the attention button is pressed.|
|1|**Power Fault Detected Enable.**When set, enables generation of a hot‐plug<br>interrupt (if enabled) or Wake# message upon detection of a power fault.|
|2|**MRL Sensor Changed Enable.**When set, enables generation of a hot‐<br>plug interrupt or Wake# (if enabled) message upon detection of a MRL<br>sensor changed event.|
|3|**Presence Detect Changed Enable.**When set this bit enables the genera‐<br>tion of the hot‐plug interrupt or a Wake message when the presence<br>detect changed bit in the Slot Status register is set.|
|4|**Command Completed Interrupt Enable.**When set, enables a Hot‐ Plug<br>interrupt to be generated that informs software that the hot‐plug control‐<br>ler is ready to receive the next command.|
|5|**Hot‐Plug Interrupt Enable.**When set, enables the generation of Hot‐Plug<br>interrupts.|
|7:6|**Attention Indicator Control.**Writes to the field control the state of the<br>attention indicator and reads return the current state, as follows:<br>• 00b = Reserved<br>• 01b = On<br>• 10b = Blink<br>• 11b = Off|
|9:8|**Power Indicator Control.**Writes to the field control the state of the power<br>indicator and reads return the current state, as follows:<br>• 00b = Reserved<br>• 01b = On<br>• 10b = Blink<br>• 11b = Off|
|10|**Power Controller Control.**Writes to the field switch main power to the<br>slot and reads return the current state: 0b = Power On, 1b = Power Off|



**869** 

**PCI Ex ress Technolo p gy** 

_Table 19‐6: Slot Control Register Fields and Descriptions (Continued)_ 

|**Bit(s)**|**Register Name and Description**|
|---|---|
|11|**Electromechanical Interlock Control ‐**If the interlock is implemented,<br>writing a 1b to this bit toggles the state of it while writing a 0b has no<br>effect. Reading this bit always returns a 0b.|
|12|**Data Link Layer State Changed Enable**‐ If the Data Link Layer Link<br>Active Reporting capability is 1b, setting this bit enables software notifica‐<br>tion when the Data Link Layer Link Active bit changes. If the Data Link<br>Layer Link Active Reporting capability is 0b, then this bit becomes read‐<br>only with a value of 0b.|



## **Slot Status and Events Management** 

The Hot Plug Controller monitors a variety of events and reports these events to the Hot Plug System Driver. Software can use the “detected” bits to determine which event has occurred, while the status bit identifies that nature of the change. The changed bits must be cleared by software in order to detect a subse‐ quent change. Note that whether these events get reported to the system (via a system interrupt) is determined by the related enable bits in the Slot Control Register. 

_Figure 19‐7: Slot Status Register_ 

**==> picture [386 x 204] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9 8 7 6 5 4 3 2 1 0<br>RsvdZ<br>Data Link Layer State Changed<br>Electromechanical Interlock Status<br>Presence Detect State<br>MRL Sensor State<br>Command Completed<br>Presence Detect Changed<br>MRL Sensor Changed<br>Power Fault Detected<br>Attention Button Pressed<br>**----- End of picture text -----**<br>


**870** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐7: Slot Status Register Fields and Descriptions_ 

|**Bit**<br>**Location**|**Register Name and Description**|
|---|---|
|0|**Attention Button Pressed**— If the button is implemented, this bit is<br>set when the Attention Button is pressed.|
|1|**Power Fault Detected**— If a Power Controller that supports power<br>fault detection is implemented, this bit is set when it detects a power<br>fault at this slot. The spec notes that it’s possible for a power fault to<br>be detected at any time, regardless of the Power Control setting or<br>whether the slot is occupied.|