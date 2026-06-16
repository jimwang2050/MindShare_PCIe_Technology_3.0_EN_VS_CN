15 11 10 9 8 7 6 5 4 3 2 1 0<br>Reserved 0 0 0 0 0<br>Interrupt Disable<br>Fast Back-to-back Enable *<br>SERR# Enable<br>Stepping Control *<br>Parity Error Response<br>VGA Palette Snoop Enable *<br>Mem Write & Invalidate Enable *<br>Special Cycles *<br>Bus Master Enable<br>Memory Space Enable<br>IO Space Enable<br>* Not used in PCIe, these must be set to zero<br>Table 15‐3: Error‐Related Fields in Command Register<br>Name Description<br>SERR# Enable Setting this bit enables sending ERR_FATAL and ERR_NONFATAL<br>error messages to the Root Complex. These are considered roughly<br>analogous to asserting the System Error (SERR#) signal in PCI.<br>For Type 1 headers (bridges), this bit controls the forwarding of<br>ERR_FATAL and ERR_NONFATAL error messages from the sec‐<br>ondary interface to the primary interface.<br>This field has no affect over ERR_COR messages.<br>**----- End of picture text -----**<br>


**675** 

**PCI Ex ress Technolo p gy** 

_Table 15‐3: Error‐Related Fields in Command Register (Continued)_ 

|**Name**|**Description**|
|---|---|
|Parity Error<br>Response|Setting this bit enables logging of poisoned TLPs in the Master Data<br>Parity Error bit in the Status register.<br>Poisoned packets indicate bad data and are roughly analogous to a<br>PCI parity error.|



Figure 15‐14 on page 676 illustrates the Configuration Status register and the location of the error‐related bit fields. Table 15‐4 on page 677 defines the circum‐ stances under which each bit is set and the actions taken by the device when error reporting is enabled. 

_Figure 15‐14: Status Register in Configuration Header_ 

**==> picture [304 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 8 7 6 5 4 3 2 0<br>0  0 0 R 0 1 Reserved<br>Interrupt Status<br>Capabilities List**<br>66 MHz Capable*<br>Reserved<br>Fast Back-to-back Capable*<br>Master Data Parity Error<br>DEVSEL Timing*<br>Signalled Target Abort<br>Received Target Abort<br>Received Master Abort<br>Signalled System Error<br>Detected Parity Error<br>* Not used in PCIe, these must be set to zero<br>** Must be set to one because some capability registers are required<br>**----- End of picture text -----**<br>


**676** 

**Chapter 15: Error Detection and Handling** 

_Table 15‐4: Error‐Related Fields in Status Register_ 

|**Error‐Related Bit**|**Description**|
|---|---|
|Detected Parity Error|Set by the port that receives a poisoned TLP. This status<br>bit is updated regardless of the state of the Parity Error<br>Response bit.|
|Signalled System Error|Set by a port that has reported an Uncorrectable Error<br>with ERR_FATAL or ERR_NONFATAL and the SERR#<br>enable bit in the Command register was set.|
|Received Master Abort|Set by a Requester that receives a Completion with sta‐<br>tus of UR (Unsupported Request). This is considered<br>analogous to a PCI master abort because the target did<br>not “claim the transaction”.|
|Received Target Abort|Set by a Requester that receives a Completion with sta‐<br>tus of CA (Completer Abort). This is analogous to a PCI<br>target abort in that the target has had a programming<br>violation or internal error condition.|
|Signaled Target Abort|Set by the Completer that handled a request (either<br>posted or non‐posted) as a Completer Abort. If it was a<br>non‐posted request, then a Completion with a Comple‐<br>tion Status of CA is sent.|
|Master Data Parity Error|For Type 0 headers (e.g., Endpoints), this bit is set if the<br>Parity Error Response bit in the Command register is<br>set AND it either initiates a poisoned request OR<br>receives a poisoned completion.<br>For Type 1 headers (e.g., Switches and Root Ports), this<br>bit is set if the Parity Error Response bit in the Com‐<br>mand register is set AND it either initiates a poisoned<br>request heading upstream OR receives a poisoned com‐<br>pletion heading downstream.|



## **Baseline Error Handling** 

The Baseline capability requires the use of the PCI Express Capability structure. These registers include error detection and handling fields that provide finer granularity regarding the nature of an error and whether to report it or not than what is possible with just PCI‐compatible error handling. 

**677** 

**PCI Ex ress Technolo p gy** 

Figure 15‐15 on page 678 illustrates the PCI Express Capability structure. Some of these registers provide support for: 

- Enabling/disabling error reporting (Error Message Generation) 

- Providing error status 

- Providing link training status and initiating link re‐training 

_Figure 15‐15: PCI Express Capability Structure_ 

**==> picture [336 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 15 7 0<br>PCI Express Capabilities Register Next Cap Pointer PCI ExpressCap ID DW0<br>Device Capabilities Register DW1<br>Device Status Device Control DW2<br>{<br>Link Capabilities DW3<br>Link Status Link Control DW4<br>{<br>Slot Capabilities DW5<br>Slot Status Slot Control DW6<br>{<br>Root Capability Root Control DW7<br>Root Status DW8<br>{<br>{<br>Device Capabilities 2 DW9<br>Device Status 2 Device Control 2 DW10<br>{<br>Link Capabilities 2 DW11<br>Link Status 2 Link Control 2 DW12<br>{<br>Slot Capabilities 2 DW13<br>Slot Status 2 Slot Control 2 DW14<br>{<br>Gen2 and later devices only<br>ks Pstro<br>niL ll<br>h A<br>Solst tiswe<br>h<br>ti civ<br>w e<br>str str D<br>o o r<br>P P x o<br>t tc<br>Roo elpmo Cello<br>C t<br>t n<br>o e<br>o v<br>R E<br>ks Pstro<br>niL llA<br>h<br>Solst tiswe<br>h<br>ti civ<br>w e<br>str D<br>o<br>P<br>**----- End of picture text -----**<br>


## **Enabling/Disabling Error Reporting** 

The Device Control registers allow software to enable generation of three differ‐ ent Error Messages for four error events, and Device Status registers allow it to see which error has been detected. The four error cases are: 

**678** 

**Chapter 15: Error Detection and Handling** 

- Correctable Errors 

- Non‐Fatal Errors 

- Fatal Errors 

- Unsupported Request Errors 

Note that the only specific error identified here is the Unsupported Request. Although an Unsupported Request is technically a subset of Non‐Fatal errors, and, when reported, is even signaled with an ERR_NONFATAL message, it has its own enable and status bits. Thatʹs because during system enumeration Unsupported Requests are going to happen (whenever an attempt it made to read config space from a Function that doesnʹt actually exist in the system) but they must not be reported as errors. The enumeration software may have very limited error‐handling capability and if it was required to stop and service an error it might fail. Therefore, the software doesnʹt want error messages gener‐ ated for the UR case during that time, but does want to know about any other Non‐Fatal errors that may be detected. (See the section titled “Discovering the Presence or Absence of a Function” on page 105 for more details on Unsup‐ ported Requests during enumeration.) 

Table 15‐5 on page 679 lists each error type and its associated error classifica‐ tion. 

_Table 15‐5: Default Classification of Errors_ 

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Correctable|Receiver Error|Physical|
|Correctable|Bad TLP|Link|
|Correctable|Bad DLLP|Link|
|Correctable|Replay Number Rollover|Link|
|Correctable|Replay Timer Timeout|Link|
|Correctable|Advisory Non‐Fatal Error|Transaction|
|Correctable|Corrected Internal Error||
|Correctable|Header Log Overflow|Transaction|
|Uncorrectable ‐ Non Fatal|Poisoned TLP Received|Transaction|
|Uncorrectable ‐ Non Fatal|ECRC Check Failed|Transaction|



**679** 

**PCI Ex ress Technolo p gy** 

_Table 15‐5: Default Classification of Errors (Continued)_ 

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Uncorrectable ‐ Non Fatal|Unsupported Request|Transaction|
|Uncorrectable ‐ Non Fatal|Completion Timeout|Transaction|
|Uncorrectable ‐ Non Fatal|Completer Abort|Transaction|
|Uncorrectable ‐ Non Fatal|Unexpected Completion|Transaction|
|Uncorrectable ‐ Non Fatal|ACS Violation|Transaction|
|Uncorrectable ‐ Non Fatal|MC Blocked TLP|Transaction|
|Uncorrectable ‐ Non Fatal|AtomicOps Egress Blocked|Transaction|
|Uncorrectable ‐ Non Fatal|TLP Prefix Blocked|Transaction|
|Uncorrectable ‐ Fatal|Uncorrectable Internal Error<br>(optional)||
|Uncorrectable ‐ Fatal|Surprise Down (optional)|Link|
|Uncorrectable ‐ Fatal|Receiver Overflow (optional)|Transaction|
|Uncorrectable ‐ Fatal|DLL Protocol Error|Link|
|Uncorrectable ‐ Fatal|Receiver Overflow|Transaction|
|Uncorrectable ‐ Fatal|Flow Control Protocol Error|Transaction|
|Uncorrectable ‐ Fatal|Malformed TLP|Transaction|



**Device Control Register.** Setting bits in the Device Control Register, shown in Figure 15‐16 on page 681, enables sending the corresponding Error Messages to report errors. Unsupported Request errors are specified as Non‐Fatal errors and are reported via a Non‐Fatal Error Message, but only when the _UR Reporting Enable_ bit is set. 

In order for a Function to actually send an error message, either the corre‐ sponding enable bit in the Device Control register needs to be set, or for Fatal and Non‐Fatal errors, the SERR# Enable should be set. For Uncorrect‐ able Errors, if either the SERR# Enable bit in the Command Register is set OR the corresponding enable bit in the Device Control register is set, the appropriate error message will be sent (ERR_FATAL or ERR_NONFATAL). 

**680** 

**Chapter 15: Error Detection and Handling** 

For Correctable Errors, a Function will only send the ERR_COR message if the _Correctable Error Reporting Enable_ bit in the Device Control register is set. There is no control to enable ERR_COR messages from the PCI‐Compatible mechanisms, which makes sense because in PCI, there was no concept of correctable errors. 

_Figure 15‐16: Device Control Register Fields Related to Error Handling_ 

**==> picture [357 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 12 11 10 9 8 7 5 4 3 2 1 0<br>Bridge Config. Retry Enable/<br>Initiate Function-Level Reset<br>Max Read Request Size<br>Enable No Snoop<br>Aux Power PM Enable<br>Phantom Functions Enable<br>Extended Tag Field Enable<br>Max Payload Size<br>Enable Relaxed Ordering<br>Unsupported Request<br>Reporting Enable<br>Fatal Error Reporting Enable<br>Non-Fatal Error<br>Reporting Enable<br>Correctable Error<br>Reporting Enable<br>**----- End of picture text -----**<br>


**Device Status Register.** An error status bit is set in the Device Status reg‐ ister, shown in Figure 15‐17 on page 682, anytime an error associated with its classification is detected, regardless of the setting of the error reporting enable bits in the Device Control Register. Because Unsupported Request errors are considered Non‐Fatal Errors, when these errors occur both the _Non‐Fatal Error Detected_ status bit and the _Unsupported Request Detected_ sta‐ tus bit will be set. Like several other status bits, these are “Sticky” (their val‐ ues are not cleared by a reset event so they’ll be available for diagnosing problems even if a reset was needed to get the Link working well enough to read the status). 

**681** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐17: Device Status Register Bit Fields Related to Error Handling_ 

**==> picture [337 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 6 5 4 3 2 1 0<br>RsvdZ<br>Transactions Pending<br>Aux Power Detected<br>Unsupported Request Detected<br>Fatal Error Detected<br>Non-Fatal Error Detected<br>Correctable Error Detected<br>**----- End of picture text -----**<br>


## **Root’s Response to Error Message** 
