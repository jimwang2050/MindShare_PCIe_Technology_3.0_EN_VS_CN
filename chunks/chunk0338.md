Cards designed to the PCIe Card ElectroMechanical spec (CEM) implement card presence detect pins (PRSNT1# and PRSNT2#) on the connector. These pins are shorter than the others so that they break contact first (when the card is removed from the slot). This can be used to give advanced notice to software of a “surprise” removal, allowing time to remove power before the signals break contact. 

## **Differences between PCI and PCIe Hot Plug** 

The elements needed to support hot plug are essentially the same in both PCI and PCIe hot plug solutions. Figure 19‐1 on page 850 shows the PCI hardware and software elements required to support hot plug. PCI solutions implement a single standardized hot plug controller on the system board that handled all the 

**849** 

## **PCI Ex ress Technolo p gy** 

hot plug slots on the bus. Isolation logic is needed in the PCI environment to electrically disconnect a card from the shared bus prior to making changes to avoid glitching the signals on an active bus. 

PCIe uses point‐to‐point connections (see Figure 19‐2 on page 851) that elimi‐ nate the need for isolation logic but require a separate hot plug controller for each Port to which a connector is attached. A standardized software interface defined for each Root and Switch Port controls hot plug operations. 

_Figure 19‐1: PCI Hot Plug Elements_ 

**850** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Figure 19‐2: PCI Express Hot‐Plug Elements_ 

**851** 

**PCI Ex ress Technolo p gy** 

## **Elements Required to Support Hot Plug** 

As shown in Figure 19‐2 on page 851 there are several parts involved in making a hog‐plug environment work. For discussion, let’s break these down into soft‐ ware and hardware elements. 

## **Software Elements** 

The following table describes the major software elements that support Hot‐ Plug capability. 

_Table 19‐1: Introduction to Major Hot‐Plug Software Elements_ 

|**Software Element**|**Supplied by**|**Description**|
|---|---|---|
|User Interface|OS vendor|An OS‐supplied utility that permits the<br>user to request that a connector be pow‐<br>ered off to remove a card or turned on to<br>use a card that has just been installed.|
|Hot‐Plug Service|OS vendor|A service that processes requests<br>(referred to as Hot‐Plug Primitives)<br>issued by the OS. This includes requests<br>to:<br>• provide slot identifiers<br>• turn card power On or Off<br>• turn Attention Indicator On or Off<br>• read current power of slot (On or Off)<br>The Hot‐Plug Service interacts with the<br>Hot‐Plug System Driver to satisfy the<br>requests. The interface (i.e., API) with<br>the Hot‐Plug System Driver is defined<br>by the OS vendor.|
|Standardized Hot‐<br>Plug System Driver|System Board<br>vendor or OS|Receives requests (Hot‐Plug Primitives)<br>from the Hot‐Plug Service within the<br>OS. Interacts with the hardware Hot‐<br>Plug Controllers to accomplish requests.|



**852** 

**Chapter 19: Hot Plug and Power Budgeting** 

_Table 19‐1: Introduction to Major Hot‐Plug Software Elements (Continued)_ 

|**Software Element**|**Supplied by**|**Description**|
|---|---|---|
|Device Driver|Adapter card<br>vendor|Some Hot‐Plug‐specific capabilities<br>must be incorporated in a Hot‐Plug‐<br>capable device driver. This includes:<br>• support for the**Quiesce**command.<br>• optional support of the**Pause**com‐<br>mand.<br>• Support for**Start**command or<br>optional**Resume**command.|



A Hot‐Plug‐capable system may use an OS that doesn’t support Hot‐Plug capa‐ bility. In that case, although the system BIOS would contain Hot‐Plug‐related software, the Hot‐Plug Service would not be present. Assuming that the user doesn’t attempt hot insertion or removal of a card, the system will operate as a standard, non‐Hot‐Plug system: 

- The system startup firmware must ensure that all Attention Indicators are Off. 

- The spec also states: “the Hot‐Plug slots must be in a state that would be appropriate for loading non‐Hot‐Plug system software.” 

## **Hardware Elements** 

Table 19‐2 on page 853 lists the major hardware elements necessary to support PCI Express Hot‐Plug operation. 

_Table 19‐2: Major Hot‐Plug Hardware Elements_ 

|**Hardware Element**|**Description**|
|---|---|
|Hot‐Plug Controller|Receives and processes commands issued by the<br>Hot‐Plug System Driver. One Controller is associ‐<br>ated with each Root or Switch Port that supports<br>hot plug operation. The PCIe spec defines a stan‐<br>dard software interface for the Hot‐Plug Control‐<br>ler.|



**853** 

## **PCI Ex ress Technolo p gy** 

_Table 19‐2: Major Hot‐Plug Hardware Elements (Continued)_ 

|**Hardware Element**|**Description**|
|---|---|
|Card Slot Power Switching<br>Logic|Allows power to a slot to be turned on or off under<br>program control. Controlled by the Hot Plug con‐<br>troller under the direction of the Hot‐Plug System<br>Driver.|
|Card Reset Logic|Hot Plug Controller drives the PERST# signal to a<br>specific slot as directed by the Hot‐Plug System<br>Driver.|
|Power Indicator|Indicates whether power is currently active on the<br>connector. Controlled by the Hot Plug logic associ‐<br>ated with each port and directed by the Hot Plug<br>System Driver.|
|Attention Indicator|Draws operator attention to a connector that needs<br>service. Controlled by the Hot Plug logic and<br>directed by the Hot‐Plug System Driver.|
|Attention Button|Pressed by the operator to notify Hot Plug soft‐<br>ware of a request to change a card.|
|Card Present Detect Pins|There are two of these: PRSNT1# is located at one<br>end of the card slot and PRSNT2# at the opposite<br>end. These pins are shorter than the others so that<br>they disconnect first when a card is removed. The<br>system board ties PRSNT1# to ground and con‐<br>nects PRSNT2# as an input to the Hot‐Plug Con‐<br>troller with a pull‐up resistor. Additional PRSNT2#<br>pins are defined for wider connectors to support<br>the insertion and recognition of shorter cards<br>installed into longer connectors. The card itself<br>shorts PRSNT1# to PRSNT2#, so that the PRSNT2#<br>input is high if a card is not physically plugged in<br>or low if it is.|



**854** 

**Chapter 19: Hot Plug and Power Budgeting** 

## **Card Removal and Insertion Procedures** 

The descriptions of typical card removal and insertion that follow are intended to be introductory in nature. It should be noted that the procedures described in the following sections assume that the OS, rather than the Hot‐Plug System Driver, is responsible for configuring a newly‐installed device. If the Hot‐Plug System Driver has this responsibility, the Hot‐Plug Service will call the Hot‐ Plug System Driver and instruct it to configure the newly‐installed device. 

## **On and Off States** 

A slot in the On state has the following characteristics: 

- Power is applied to the slot. 

- REFCLK is on. 

- The link is active or in an Active State Power Management state. 

- The PERST# signal is deasserted. 

A slot in the Off state has the following characteristics: 

- Power to the slot is turned off. 

- REFCLK is off. 

- The link is inactive. (Driver at the root of switch port is in Hi Z state) 

- The PERST# signal is asserted. 

## **Turning Slot Off** 

Steps required to turn off a slot that is currently in the On state: 

1. Deactivate the link. This may involve issuing a EIOS to enter the Hi Z state. 

2. Assert the PERST# signal to the slot. 

3. Turn off REFCLK to the slot. 

4. Remove power from the slot. 

## **Turning Slot On** 

Steps to turn on a slot that is currently in the off state: 

1. Apply power to the slot. 

2. Turn on REFCLK to the slot 

**855** 

## **PCI Ex ress Technolo p gy** 

3. Deassert the PERST# signal to the slot. The system must meet the setup and hold timing requirements (specified in the PCI Express spec) relative to the rising edge of PERST#. 

Once power and clock have been restored and PERST# removed, the physical layers at both ports will perform link training and initialization. When the link is active, the devices will initialize VC0 (including flow control), making the link ready to transfer TLPs. 

## **Card Removal Procedure** 

When a card is to be removed, a number of steps are needed to prepare software and hardware for safe removal of the card, and set the indicators for the card being processed. The condition of the indicators during normal operation are: 

- Attention Indicator (Amber or Yellow) — “Off” during normal operation. 

- Power Indicator (Green) — “On” during normal operation 

Software sends requests to the Hot Plug Controller using configuration writes that target the Slot Control Registers implemented by Hot‐Plug capable ports. These control the power to the slot and the state of the indicators. 

The sequence of events is as follows: 

1. The operator requests card removal by pressing the slot’s attention button or by using the system’s user interface to select the Physical Slot number of the card to be removed. If the button was used, the Hot‐Plug Controller detects this event and delivers an interrupt to the root complex. The inter‐ rupt directs the Hot Plug service to call the Hot Plug System Driver to read slot status information and detect the Attention Button request. 

2. Next, the Hot‐Plug Service commands the Hot‐Plug System Driver to blink the slot’s Power Indicator as visual feedback to the operator for 5 seconds. If this was initiated by pressing the Attention button, the operator can press the button a second time to cancel the request during this 5‐second interval. 

3. The Power Indicator continues to blink while the Hot Plug software vali‐ dates the request. If the card is currently in use for some critical system operation, software may deny the request. In that case, it will issue a com‐ mand to the Hot Plug controller to turn the Power Indicator back ON. The spec also recommends that software notify the operator, perhaps with a message or by logging an entry indicating the reason the request was denied. 

**856** 

**Chapter 19: Hot Plug and Power Budgeting** 

4. If the request is validated, the Hot‐Plug Service utility commands the card’s device driver to quiesce the device. That is, disable its ability to generate new Requests and complete or terminate all outstanding Root or Switch Port requests. 

5. Software then issues a command to disable the card’s Link via the Link Con‐ trol register in the Root or Switch Port to which the slot is attached. 

6. Next, software commands the Hot Plug Controller to turn the slot off. 

7. Following successful power down, software issues the Power Indicator Off Request to turn off the power indicator so the operator knows the card may be removed. 

8. The operator releases the Mechanical Retention Latch, if there is one, caus‐ ing the Hot Plug Controller to remove all switched signals from the slot (e.g., SMBus and JTAG signals). The card can now be removed. 

9. The OS deallocates the memory space, IO space, interrupt line, etc. that had been assigned to the device and makes these resources available for assign‐ ment to other devices in the future. 

## **Card Insertion Procedure** 

The procedure for installing a new card basically reverses the steps listed for card removal. The following steps assume that the slot was left in the same state that it was in immediately after a card was removed from the connector (in other words, the Power Indicator is in the Off state, indicating the slot is ready for card insertion). 

The steps taken to Insert and enable a card are as follows: 

1. The operator installs the card and secures the MRL. If implemented, the MRL sensor will signal the Hot‐Plug Controller that the latch is closed, causing switched auxiliary signals and Vaux to be connected to the slot. 

2. Next, the operator notifies the Hot‐Plug Service that the card has been installed by pressing the Attention Button or using the Hot Plug Utility pro‐ gram to select the slot. 
