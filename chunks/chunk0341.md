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