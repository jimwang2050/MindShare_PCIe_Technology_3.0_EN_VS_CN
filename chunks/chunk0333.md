|||Pending Bits||||DW5|
||||||||



**813** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Capability ID** 

A Capability ID value of **05h** identifies the MSI capability and is a read‐only value. 

## **Next Capability Pointer** 

The second byte of the register is a read‐only value that gives the dword‐ aligned offset from the top of config space to the next Capability Structure in the linked list of structures or else contains 00h to indicate the end of the linked list. 

## **Message Control Register** 

Figure 17‐14 on page 814 and Table 17‐2 on page 814 illustrate the layout and usage of the Message Control register. 

_Figure 17‐14: Message Control Register_ 

**==> picture [358 x 114] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 9 8 7 6 4 3 1 0<br>Reserved<br>MSI Enable<br>Multiple Message Capable<br>Multiple Message Enable<br>64-bit Address Capable<br>Per-vector Masking Capable<br>**----- End of picture text -----**<br>


_Table 17‐2: Format and Usage of Message Control Register_ 

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|0|MSI Enable|Read/Write. State after reset is 0, indicating that the<br>device’s MSI capability is disabled.<br>• **0**= Function is**disabled**from using**MSI**. It must<br>use MSI‐X or else INTx Messages.<br>• **1**= Function is**enabled**to use**MSI**to request<br>service and won’t use MSI‐X or INTx Messages.|



**814** 

**Chapter 17: Interrupt Support** 

_Table 17‐2: Format and Usage of Message Control Register (Continued)_ 

|**Bit(s)**|**Field Name**||**Description**|
|---|---|---|---|
|3:1|Multiple Message<br>Capable||Read‐Only. System software reads this field to<br>determine how many messages (interrupt vectors)<br>the Function would like to use. The requested<br>number of messages is a power of two, therefore a<br>Function that would like three messages must<br>request that four messages be allocated to it.<br>**Value**<br>   **Number of Messages Requested**<br>000b                                    1<br>001b                                    2<br>010b                                    4<br>011b                                    8<br>100b                                   16<br>101b                                   32<br>110b                              Reserved<br>111b                              Reserved|
|6:4|Multiple Message<br>Enable||Read/Write. After system software reads the Multi‐<br>ple Message Capable field (previous row in this<br>table) to see how many messages (interrupt vec‐<br>tors) are requested by the Function, it programs a<br>3‐bit value in this field indicating the actual num‐<br>ber of messages allocated to the Function. The<br>number allocated can be equal to or less than the<br>number actually requested. The state of this field<br>after reset is 000b.<br>**Value**<br>   **Number of Messages Requested**<br>000b                                    1<br>001b                                    2<br>010b                                    4<br>011b                                    8<br>100b                                   16<br>101b                                   32<br>110b                              Reserved<br>111b                              Reserved|



**815** 

**PCI Ex ress 3.0 Technolo p gy** 

_Table 17‐2: Format and Usage of Message Control Register (Continued)_ 

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|7|64‐bit Address<br>Capable|Read‐Only.<br>• 0 = Function does not implement the upper 32<br>bits of the Message Address register; only a 32‐<br>bit address is possible.<br>• 1 = Function implements the upper 32 bits of the<br>Message Address register and is capable of gen‐<br>erating a 64‐bit memory address.|
|8|Per‐Vector<br>Masking Capable|Read‐Only.<br>• 0 = Function does not implement the Mask Bit<br>register or the Pending Bit register; software<br>does NOT have the ability to mask individual<br>interrupts with this capability structure.<br>• 1 = Function does implement the Mask Bit regis‐<br>ter or the Pending Bit register; software does<br>have the ability to mask individual interrupts<br>with this capability structure.|
|15:9|Reserved|Read‐Only. Always zero.|



## **Message Address Register** 

The lower two bits of the 32‐bit Message Address register are zero and cannot be changed, forcing the address assigned by software to be dword aligned. Typ‐ ically, this would be the address of the Local APIC in the system CPU. In x86‐ based systems (Intel‐compatible), this address has traditionally been FEEx_xxxxh where the lower 20 bits indicate which Local APIC is being tar‐ geted as well as some other info about the interrupt itself. It is important to note that how the address is interpreted is platform specific and is not dictated in the PCI or PCIe specs. 

The register containing bits [63:32] of the Message Address are required for native PCI Express devices but is optional for legacy endpoints. This register is present if Bit 7 of the Message Control register is set. If so, it is a read/write reg‐ ister used in conjunction with the Message Address [31:0] register to enable a 64‐bit memory address for interrupt delivery from this Function. 

**816** 

**Chapter 17: Interrupt Support** 

## **Message Data Register** 

System software writes a base message data pattern into this 16‐bit, read/write register. When the Function generates an interrupt request, it writes a 32‐bit data value to the memory address specified in the Message Address register. The upper 16 bits of this data are always set to zero, while the lower 16 bits are supplied by the Message Data register. 

If more than one message has been assigned to the Function, it modifies the lower bits (the number of modifiable bits depends on how many messages have been assigned to the Function by configuration software) of the Message Data register value to form the appropriate value for the event it wishes to report. As an example, refer to “Basics of Generating an MSI Interrupt Request” on page 820. 

## **Mask Bits Register and Pending Bits Register** 

If the Function supports per‐vector masking (indicated in bit [8] of the Message Control register) then these registers are present. The max number of interrupt messages (itnerrupt vectors) that can be requested and assigned to a Function using MSI is 32. So these two registers are 32 bits in length with each potential interrupt message having its own mask and pending bit. If bit [0] of the Mask Bits register is set, then interrupt message 0 is masked (this is the base vector from this Function). If bit [1] is set, then interrupt message 1 is masked (this is the base vector + 1). 

When an interrupt message is masked, the MSI for that vector cannot be sent. Instead, the corresponding Pending Bit is set. This allows software to mask indi‐ vidual interrupts from a Function and then periodically poll the Function to see if there are any masked interrupts that are pending. 

If software clears a mask bit and the corresponding pending bit is set, the Func‐ tion must send the MSI request at that time. Once the interrupt message has been sent, the Function would clear the pending bit. 

## **Basics of MSI Configuration** 

The following list specifies the steps taken by software to configure MSI inter‐ rupts for a PCI Express device. Refer to Figure 17‐15 on page 819. 

1. At startup time, enumeration software scans the system for all PCI‐compat‐ ible Functions (see “Single Root Enumeration Example” on page 109 for a discussion of the enumeration process). 

**817** 

## **PCI Ex ress 3.0 Technolo p gy** 

2. Once a Function is discovered software reads the Capabilities List Pointer, to find the location of the first capability structure in the linked list. 

3. If the MSI Capability structure (Capability ID of 05h) is found in the list, software reads the Multiple Message Capable field in the device’s Message Control register to determine how many event‐specific messages the device supports and if it supports a 64‐bit message address or only 32‐bit. Software then allocates a number of messages equal to or less than that and writes that value into the Multiple Message Enable field. At a minimum, one mes‐ sage will be allocated to the device. 

4. Software writes the base message data pattern into the device’s Message Data register and writes a dword‐aligned memory address to the device’s Message Address register to serve as the destination address for MSI writes. 

5. Finally, software sets the MSI Enable bit in the device’s Message Control register, enabling it to generate MSI writes and disabling other interrupt delivery options. 

**818** 

**Chapter 17: Interrupt Support** 

_Figure 17‐15: Device MSI Configuration Process_ 

**==> picture [159 x 456] intentionally omitted <==**

**----- Start of picture text -----**<br>
Scan PCI bus(es)<br>until device<br>discovered<br>New<br>N<br>Capabilities<br>?<br>Y<br>MSI N<br>Capable<br>?<br>Y<br>Determine number of<br>messages requested<br>and assign number<br>of messages to device<br>Write base data<br>pattern into<br>Message Data<br>Register<br>Assign Memory<br>Address to Message<br>Address Register<br>Enable device to<br>use MSI with<br>MSI Enable bit<br>in Message Control<br>Register<br>**----- End of picture text -----**<br>


**819** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Basics of Generating an MSI Interrupt Request** 

Figure 17‐16 on page 821 illustrates the contents of an MSI Memory Write Trans‐ action Header and Data field. Key points include: 

- Format field must be 011b for native functions, indicating a 4DW header (64‐bit address) with Data, but it may be 010b for Legacy Endpoints, indi‐ cating a 32‐bit address. 

- The Attribute bits for No Snoop and Relaxed Ordering must be zero. 

- Length field must be 01h to indicate maximum data payload of 1DW. 

- First BE field must be 1111b, indicating valid data in all four bytes of the DW, even though the upper two bytes will always be zero for MSI. 

- Last BE field must be 0000b, indicating a single DW transaction. 

- Address fields within the header come directly from the address fields within the MSI Capability registers. 

- Lower 16 bits of the Data payload are derived from the data field within the MSI Capability registers. 

## **Multiple Messages** 

If system software allocated more than one message to the Function, the multi‐ ple values are created by modifying the lower bits of the assigned Message Data value to send a different message for each device‐specific event type. 

As an example, assume the following: 

- Four messages have been allocated to a device. 

- A data value of 49A0h has been assigned to the device’s Message Data reg‐ ister. 

- Memory address FEEF_F00Ch has been written into the device’s Message Address register. 

- When one of the four events occurs, the device generates a request by per‐ forming a dword write to memory address FEEF_F00Ch with a data value of 0000_49A0h, 0000_49A1h, 0000_49A2h, or 0000_49A3h. In other words, the lower two bits of the data value are modified to specify which event occurred. If this Function would have been allocated 8 messages, then the lower three bits could be modified. Also, the device always uses 0000h for the upper 2 bytes of its message data value. 

**820** 

**Chapter 17: Interrupt Support** 

_Figure 17‐16: Format of Memory Write Transaction for Native‐Device MSI Delivery_ 

**==> picture [329 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>