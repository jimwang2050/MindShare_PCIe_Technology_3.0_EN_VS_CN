A 4DW portion of the Advanced Error Reporting structure is used for storing the header of a received TLP that incurs an unmasked, uncorrectable error. Since header logging is only useful when a TLP has been received with a prob‐ lem that wasn’t seen by the Physical or Data Link Layers, the number of possi‐ bilities is limited, as shown in Table 15‐6 on page 695. As mentioned earlier, when the optional AER capability is implemented, hardware is required to be able to log at least one header, though it may support logging more. 

When the First Error Pointer is valid, the header log contains the header for the corresponding error if it was caused by an incoming TLP. Updating the Uncor‐ rectable Error Status register will cause the Header Log registers to also update to the next value in sequence, meaning the next uncorrectable error that was detected. Since the hardware can only track a limited number of headers, it’s important that software service uncorrectable errors quickly enough to avoid running out of header space. If the header log capacity is reached, that’s a cor‐ rectable error in itself (Header Log Overflow). This could happen if the number of supported log registers is exceeded or if the Multiple Header Log Enable bit is not set and the First Error Pointer is already valid when a new uncorrectable error is detected. 

_Table 15‐6: Errors That Can Use Header Log Registers_ 

|**Name of Error**|**Default Classification**|
|---|---|
|Poisoned TLP Received|Uncorrectable ‐ NonFatal|
|ECRC Check Failed|Uncorrectable ‐ NonFatal|
|Unsupported Request|Uncorrectable ‐ NonFatal|
|Completer Abort|Uncorrectable ‐ NonFatal|
|Unexpected Completion|Uncorrectable ‐ NonFatal|
|ACS Violation|Uncorrectable ‐ NonFatal|
|Malformed TLP|Uncorrectable ‐ Fatal|



**695** 

**PCI Ex ress Technolo p gy** 

## **Root Complex Error Tracking and Reporting** 

The Root Complex is the target of all error Messages from devices in a PCIe topology. Errors received by the Root update status registers and may be reported to the host system if enabled to do so. 

## **Root Complex Error Status Registers** 

When the Root receives an error Message, it sets status bits within the Root Error Status register (Figure 15‐28 on page 697). This register indicates the type of error received and whether multiple errors of the same type have been received. Note that an error detected in the Root Port itself will set these status bits, too, as if the port had sent itself an error message. The status bits are: 

- ERR_COR Received 

- Multiple ERR_COR Received ‐ received an ERR_COR message, or detected an unmasked Root Port correctable error with the ERR_COR Received bit already set. 

- ERR_FATAL/NONFATAL Received 

- Multiple ERR_FATAL/NONFATAL Received ‐ received an ERR_FATAL or ERR_NONFATAL message or detected an unmasked Root Port uncorrect‐ able error with the ERR_FATAL/NONFATAL Received bit already set. 

It’s possible for a system to implement separate software error handlers for Cor‐ rectable, Non‐Fatal, and Fatal errors, so this register includes bits to differenti‐ ate whether Uncorrectable errors were Fatal or Non‐Fatal: 

- If the first Uncorrectable Error Message received is Fatal the “First Uncor‐ rectable Fatal” bit is also set along with the “Fatal Error Message Received” bit. 

- If the first Uncorrectable Error Message received is Non‐Fatal the “Non‐ fatal Error Message Received” bit is set. (If a subsequent Uncorrectable Error is Fatal, the “Fatal Error Message Received” bit will be set, but because the “First Uncorrectable Fatal” remains cleared, software knows that the first Uncorrectable Error was Non‐Fatal). 

**696** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐28: Root Error Status Register_ 

**==> picture [327 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 27 26 7 6 5 4 3 2 1 0<br>RsvdZ<br>Advanced Error Interrupt Message Number (RO)<br>Fatal Error Messages Received<br>Non-Fatal Error Messages Received<br>RW1CS First Uncorrectable Fatal<br>Multiple ERR_FATAL/NONFATAL Received<br>ERR_FATAL/NONFATAL Received<br>Multiple ERR_COR Received<br>ERR_COR Received<br>**----- End of picture text -----**<br>


Finally, an interrupt may have been enabled (in the Root Error Command regis‐ ter) to be sent to the host system as a result of detecting one of these events. To support that, the 5‐bit Interrupt Message Number in this register supplies the MSI or MSI‐X vector number to be used, and there are 32 possibilities. For MSI, the number is the offset from the base data pattern. For MSI‐X, it represents the table entry to be used, and must be one of the first 32 even if the agent supports more than 32. This read‐only value is set by hardware and must be automati‐ cally updated if the number of MSI messages assigned to the device changes. 

## **Advanced Source ID Register** 

Software error handlers may need to read and clear status registers in the device that detected and reported the error. To facilitate this, the error Messages contain the ID (Bus:Dev:Func) of the first device reporting that error type. The Source ID register captures that ID from the Message for an incoming ERR_FATAL/NONFATAL message if the ERR_FATAL/NONFATAL bit isn’t already set (meaning this is the first one). Similarly, the Source ID of the first received ERR_COR message is captured, too, as shown in Figure 15‐29 on page 698. 

**697** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐29: Advanced Source ID Register_ 

**==> picture [327 x 47] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 0<br>ERR_FATAL/NONFATAL Source ID ERR_COR Source ID<br>(ROS) (ROS)<br>ROS: Read-Only and Sticky<br>**----- End of picture text -----**<br>


## **Root Error Command Register** 

The Root Complex has separate enable bits for each of the three error categories to control whether that error type will generate an interrupt to call an error han‐ dler as shown in Figure 15‐30 on page 698. The interrupt that is generate will either be an MSI or MSI‐X as discussed in “Root Complex Error Status Regis‐ ters” on page 696. Once the interrupt is received, the called error handler would probably first read the Root Complex status registers to determine the nature of the error, and then go down to the source BDF of the error to read standard sta‐ tus register as well as possibly device‐specific registers to determine what occurred and how it should be handled. 

_Figure 15‐30: Advanced Root Error Command Register_ 

**==> picture [332 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 3 2 1 0<br>RsvdP<br>Fatal Error Reporting Enable<br>Non-Fatal Error Reporting Enable<br>Correctable Error Reporting Enable<br>Note: all bits designated RW<br>**----- End of picture text -----**<br>


## **Summary of Error Logging and Reporting** 

The spec includes the flow chart in Figure 15‐31 on page 699 that shows the actions taken by a Function when an error is detected. The part inside the dashed line highlights the items that are added when the optional AER capabil‐ ity structure is present. 

**698** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐31: Flow Chart of Error Handling Within a Function_ 

**==> picture [327 x 391] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Detected<br>Uncorrectable Error Type? Correctable<br>Determine severity using<br> Uncorrectable Error Severity Register<br>Advisory Yes AER Yes<br>Non-Fatal Error? Implemented?<br>No No<br>Set Fatal/NonFatal Error Detected bit Set Correctable Error Detected bit<br>in Device Status Reg Done in Device Status Reg<br>If UR, set Unsupported Request If UR, set Unsupported Request<br> Detected bit in Device Status Reg  Detected bit in Device Status Reg<br>Advanced Set corresponding bit in<br>Uncorrectable Error Status RegSet corresponding bit in Error Correctable Error Status Reg<br>Reporting<br>Only Is error masked in Yes<br>Correctable Error Mask<br>Masked in Yes  Register?<br>Uncorrectable Error Mask<br> Register? No Done<br>No Done 1) Set Uncorrectable Error status bit, andIf Advisory Non-Fatal Error:<br>header, and update prefix and header As appropriate, record prefix and reporting fields and registers 2) If not masked by Uncorrectable mask,header, and update prefix and header as appropriate, record prefix and reporting fields and registers<br>both SERR and UR ReportingUR Error anddisabled? Yes UR Reporting disabled?UR error and Yes<br>No Done No Done<br>Fatal Non-Fatal<br>Severity?<br>SERR enabled or No SERR enabled or No Correctable Reporting  No<br>Fatal Error Reporting Non-Fatal Error Reporting Enabled?<br>Enabled? Enabled?<br>Yes Done Yes Done Yes Done<br>Send ERR_FATAL Send ERR_NONFATAL Send ERR_COR<br>Done Done Done<br>**----- End of picture text -----**<br>


## **Example Flow of Software Error Investigation** 

Now that we know all the mechanisms defined in PCIe for detecting, logging and reporting errors, it is worthwhile to look at how software would find and use this information to determine how to handle a reported error. 

**699** 

## **PCI Ex ress Technolo p gy** 

This example is going to assume that both the originating Function as well as the Root Port upstream of it both support AER. Without AER support, the stan‐ dardized registers for error logging are very limited. 

The system used for this example is shown in Figure 15‐32 on page 701. The Root Port has a BDF of 0:28:0 and was enabled to generate an interrupt when it receives either an ERR_FATAL or ERR_NONFATAL message. We are going to follow the steps of error handling software would take to determine what errors have occurred, where they occurred and what packets were they detected in. 

The error handling software has been called because of an interrupt from Root Port 0:28:0. The steps below are just an example, but illustrate the process of error handling software gathering error information. 

1. Software knows it was Root Port 0:28:0 that called the error handler based on the interrupt vector used. Since MSI or MSI‐X interrupts are used to report errors, each Root Port will have their own unique set of interrupt vectors. 

2. The error handler reads the Root Error Status register of the AER structure on 0:28:0 to determine what types of error messages have been received by the Root Port. The value in that register is 0800_007Ch which indicates that this Root Port has not received any ERR_COR messages, but has received both ERR_FATAL and ERR_NONFATAL messages and the first uncorrect‐ able error message that it received was an ERR_FATAL. 

3. The next step is to determine which BDF beneath this Root Port sent the first uncorrectable error. Software then reads the Source ID register of the Root Port and finds the value 0500_0000h, which indicates that the source BDF of the first uncorrectable error was 5:0:0. 

4. Now software knows that the first uncorrectable error received by Root Port 0:28:0 was a Fatal error that originated from BDF 5:0:0. With this informa‐ tion, software then goes and reads the Uncorrectable Error Status register on BDF 5:0:0 to see which specific uncorrectable errors have occurred on that BDF. The value returned from that read is 0004_1000h which means that this BDF has detected at least one Malformed TLP and at least one Poi‐ soned TLP. But what the error handler really cares about is which one occurred first, because that’s the one that should be handled first. 

5. To determine which of the multiple uncorrectable errors occurred first, soft‐ ware then reads the Advanced Error Capability and Control register of 5:0:0 and finds the value 0000_0012h which has a First Error Pointer value of 12h meaning that the first uncorrectable error was a Malformed TLP (bit 18d) and not the Poisoned TLP (bit 12d). 

**700** 

**Chapter 15: Error Detection and Handling** 

_Figure 15‐32: Error Investigation Example System_ 
