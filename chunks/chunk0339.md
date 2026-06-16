3. If the button was pressed, it signals the Hot Plug controller of the event, resulting in status register bits being set and causing a system interrupt to be sent to the Root Complex. Subsequently, Hot Plug software reads slot status from the port and recognizes the request. 

4. The Hot‐Plug Service issues a request to the Hot‐Plug System Driver com‐ manding the Hot Plug Controller to blink the slot’s Power Indicator to inform the operator that the card must not be removed. The operator is granted a 5 second abort interval, from the time that the indicators starts to blink, to abort the request by pressing the button a second time. 

**857** 

## **PCI Ex ress Technolo p gy** 

5. The Power Indicator continues to blink while Hot Plug software validates the request. Note that software may fail to validate the request (e.g., the security policy settings may prohibit the slot being enabled). If the request is not validated, software will issue a command to the Hot Plug controller to turn the Power Indicator back OFF. The spec recommends that software notify the operator via a message or by logging an entry indicating the cause of the request denial. 

6. The Hot‐Plug Service issues a request to the Hot‐Plug System Driver com‐ manding the Hot Plug Controller to turn the slot on. 

7. Once power is applied, software issues a command to turn the Power Indi‐ cator ON. 

8. Once link training is complete, the OS commands the Platform Configura‐ tion Routine to configure the card function(s) by assigning the necessary resources. 

9. The OS locates the appropriate driver(s) (using the Vendor ID and Device ID, or the Class Code, or the Subsystem Vendor ID and Subsystem ID con‐ figuration register values as search criteria) for the function(s) within the PCI Express device and loads it (or them) into memory. 

10. The OS then calls the driver’s initialization code entry point, causing the processor to execute the driver’s initialization code. This code finishes the setup of the device and then sets the appropriate bits in the device’s PCI configuration Command register to enable the device. 

## **Standardized Usage Model** 

## **Background** 

Systems based on the original 1.0 version of the PCI Hot Plug spec implemented hardware and software designs that varied widely because the spec did not define standardized registers or user interfaces. Consequently, customers who purchased Hot Plug capable systems from different vendors were confronted with a wide variation in user interfaces that required retraining operators when new systems were purchased. Furthermore, every board designer was required to write software to manage their implementation‐specific hot plug controller. The 1.1 revision of the PCI Hot‐Plug Controller (HPC) spec defines: 

- a standard user interface that eliminates retraining of operators 

- a standard programming interface for the hot plug controller, which per‐ mits a standardized hot plug driver to be incorporated into the operating system. PCI Express implements registers not defined by the HPC spec, 

**858** 

**Chapter 19: Hot Plug and Power Budgeting** 

hence the standard Hot Plug Controller driver implementations for PCI and PCI Express are slightly different. 

## **Standard User Interface** 

The user interface includes the following features: 

- Attention Indicator — shows the attention state of the slot with an LED that is on, off, or blinking. The spec defines the blinking frequency as 1 to 2 Hz and 50% (+/‐ 5%) duty cycle. The state of this indicator is strictly under soft‐ ware control. 

- Power Indicator (called Slot State Indicator in PCI HP 1.1) — shows the power status of the slot and also can be on, off, or blinking (at 1 to 2 Hz and 50% (+/‐ 5%) duty cycle). This indicator is controlled by software; however, the spec permits an exception in the event of a hardware power fault condi‐ tion. 

- Manually Operated Retention Latch and Optional Sensor — secures card within slot and notifies the system when the latch is released 

- Electromechanical Interlock (optional) — locks the card or retention latch to prevent the card from being removed while power is applied. 

- Software User Interface — allows operator to request hot plug operation 

- Attention Button — allows operator to manually request hot plug opera‐ tion. 

- Slot Numbering Identification — provides visual identification of slot on the board. 

## **Attention Indicator** 

As mentioned in the previous section, the spec requires the system vendor to include an Attention Indicator associated with each Hot‐Plug slot. This indica‐ tor must be located in close proximity to the corresponding slot and is yellow or amber in color. This Indicator draws the attention of the end user to the slot for service. The spec makes a clear distinction between operational and validation errors and does not permit the attention indicator to report validation errors. Validation errors are problems detected and reported by software prior to beginning the hot plug operation. The behavior of the Attention Indicator is listed in Table 19‐3 on page 860. 

**859** 

**PCI Ex ress Technolo p gy** 

_Table 19‐3: Behavior and Meaning of the Slot Attention Indicator_ 

|**Indicator Behavior**|**Attention State**|
|---|---|
|Off|Normal — Normal Operation|
|On|Attention — Hot Plug Operation Failed due to an oper‐<br>ational problem (e.g., problems with external cabling,<br>add‐in cards, software drivers, and power faults)|
|Blinking|Locate — Slot is being identified at operator’s request|



## **Power Indicator** 

The power indicator simply reflects the state of main power at the slot, and is controlled by Hot Plug software. The color of this indicator is green and is illu‐ minated when power to the slot is “on.” 

The spec specifically prohibits Root or Switch Port hardware from changing the power indicator state autonomously as a result of power fault or other events. A single exception to this rule allows a platform to detect stuck‐on power faults. A stuck‐on fault is simply a condition in which commands issued to remove slot power are ineffective. If the system is designed to detect this condition the sys‐ tem may override the Root or Switch Port’s command to turn the power indica‐ tor off and force it to remain on. This notifies the operator that the card should not be removed from the slot. The spec further states that supporting stuck‐on faults is optional and, if handled via system software, “the platform vendor must ensure that this optional feature of the Standard Usage Model is addressed via other software, platform documentation, or by other means.” 

The behavior of the power indicator and the related power states are listed in Table 19‐4 on page 861. Note that Vaux remains on and switch signals are still connected until the retention latch is released or when the card is removed as detected by the Prsnt1# and Prsnt2# signals. 

**860** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐4: Behavior and Meaning of the Power Indicator_ 

|**Indicator Behavior**|**Power State**|
|---|---|
|Off|Power Off — it is safe to remove or insert a card. All power<br>has been removed as required for hot plug operation. Vaux is<br>only removed when the Manual Retention Latch is released.|
|On|Power On — removal or insertion of a card is not allowed.<br>Power is currently applied to the slot.|
|Blinking|Power Transition — card removal or insertion is not allowed.<br>This state notifies the operator that software is currently<br>removing or applying slot power in response to a hot plug<br>request.|



## **Manually Operated Retention Latch and Sensor** 

The Manual Retention Latch (MRL) is required and holds PCI Express cards rig‐ idly in the slot. Each MRL can implement an optional sensor that notifies the Hot‐Plug Controller that the latch has been closed or opened. The spec also allows a single latch that can hold down multiple cards. Such implementations do not support the MRL sensor. 

An MRL Sensor is a switch, optical device, or other type of sensor that reports whether the latch is closed or open. If an unexpected latch release is detected, the port automatically disables the slot and notifies system software, although changing the state of the Power or Attention indicators autonomously is not allowed. 

The switched signals and auxiliary power (Vaux) must be automatically removed from the slot when the MRL Sensor indicates that the MRL is open, and they must be restored to the slot when the MRL Sensor indicates that the latch is closed. The switched signals are Vaux, SMBCLK, and SMBDAT. 

The spec also describes an alternate method for removing Vaux and SMBus power when an MRL sensor is not present. The PRSNT#2 pin indicates whether a card is physically installed into the slot and can be used to trigger the port to remove the switched signals. 

**861** 

**PCI Ex ress Technolo p gy** 

## **Electromechanical Interlock (optional)** 

The optional electromechanical card interlock mechanism provides a more sophisticated method of ensuring that a card is not removed while power is applied to the slot. The spec does not define the specific nature of the interlock, but states that it can physically lock the add‐in card or the MRL in place. 

The lock mechanism is controlled via software; however, there is no specific programming interface defined for it. Instead, an interlock is controlled by the same Port signal that enables main power to the slot. 

## **Software User Interface** 

An operator may use a software interface to request card removal or insertion. This interface is provided by system software, which also monitors slots and reports status information to the operator. The spec states that the user interface is implemented by the Operating System and consequently is beyond the scope of the spec. 

The operator must be able to initiate operations at each slot independent of other slots. Consequently, the operator may initiate a hot‐plug operation on one slot using the software user interface or attention button while a hot‐plug oper‐ ation on another slot is in process. This can be done regardless of which inter‐ face the operator used to start the first Hot‐Plug operation. 

## **Attention Button** 

The Attention Button is a momentary‐contact push‐button switch, located near the corresponding Hot‐Plug slot or on a module. The operator presses this but‐ ton to initiate a hot‐plug operation for this slot (e.g., card removal or insertion). Once the Attention Button is pressed, the Power Indicator starts to blink. From the time the blinking begins the operator has 5 seconds to abort the Hot Plug operation by pressing the button a second time. 

The spec recommends that if an operation initiated by an Attention Button fails, the system software should notify the operator of the failure. For example, a message explaining the nature of the failure can be reported or logged. 

## **Slot Numbering Identification** 

Software and operators must be able to identify a physical slot based on its slot number. Each hot‐plug capable port must implement registers that software uses to identify the physical slot number. The registers include a Physical Slot 

**862** 

**Chapter 19: Hot Plug and Power Budgeting** 

number and a chassis number. The main chassis is always labeled chassis 0. The chassis numbers for other chassis must be non‐zero and are assigned via the PCI‐to‐PCI bridge’s Chassis Number register. 

## **Standard Hot Plug Controller Signaling Interface** 

Figure 19‐3 on page 864 presents a more detailed view of the logic within Switch Ports, along with the signals routed between the slot and the Port. The importance of the standardized Hot Plug Controller is the common software interface that allows the device driver to be integrated into operating systems. 
