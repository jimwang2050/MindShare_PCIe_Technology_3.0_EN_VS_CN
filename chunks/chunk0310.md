- Completer receives a Request that it cannot process because of some perma‐ nent error condition in the device. For example, a wireless LAN card that won’t accept new packets because it can’t transmit or receive over its radio until an approved antenna is attached. 

- Completer receives a Request for which it detects an ACS (Access Control Services) error. An example of this would be a Root Port that implements the ACS registers and has ACS Translation Blocking enabled. If a memory Request is seen on that Port with anything other than the default value in the AT field, it will be an ACS violation. 

- PCIe‐to‐PCI Bridge may receive a Request that targets the PCI bus. PCI allows the target device to signal a target abort if it can’t complete the Request due to some permanent condition or violation of the Function’s programming rules. In response, the bridge would return a Completion with CA status. 

A Completer that aborts a Request may report the error to the Root with a Non‐ fatal Error Message and, if the Request requires a Completion, the status would be CA. 

## **Unexpected Completion** 

When a Requester receives a Completion, it uses the transaction descriptor (Requester ID and Tag) to match it with an earlier Request. In rare circum‐ stances, the transaction descriptor may not match any previous Request. This might happen because the Completion was mis‐routed on its journey back to the intended Requester. An Advisory Non‐fatal Error Message can be sent by the device that receives the unexpected Completion, but it’s expected that the correct Requester will eventually timeout and take the appropriate action, so that error Message would be a low priority. 

**664** 

**Chapter 15: Error Detection and Handling** 

## **Completion Timeout** 

For the case of a pending Request that never receives the Completion it’s expect‐ ing, the spec defines a Completion timeout mechanism. The spec clearly intends this to detect when a Completion has no reasonable chance of returning; it should be longer than any normal expected latencies. 

The Completion timeout timer must be implemented by all devices that initiate Requests that expect Completions, except for devices that only initiate configu‐ ration transactions. Note also that every Request waiting for Completions is timed independently, and so there must be a way to track time for each out‐ standing transaction. The 1.x and 2.0 versions of the spec defined the permissi‐ ble range of the timeout value as follows: 

- It is strongly recommended that a device not timeout earlier than 10ms after sending a Request; however, if the device requires greater granularity a tim‐ eout can occur as early as 50μs. 

- Devices must time‐out no later than 50ms. 

Beginning with the 2.1 spec revision, the Device Control Register 2 was added to the PCI Express Capability Block to allow software visibility and control of the timeout values, as shown in Figure 15‐8 on page 665. 

_Figure 15‐8: Device Control Register 2_ 

**==> picture [152 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 oO 0000b = 50µs - 50ms<br>0001b = 50µs - 100µs<br>A<br>0010b = 1ms - 10ms<br>EK of<br>0101b = 16ms - 55ms<br>B<br>0110b = 65ms - 210ms<br>1001b = 260ms - 900ms<br>C<br>1010b = 1s - 3.5s<br>1100b = 4s - 13s<br>D<br>[ 1110b = 17s - 64s<br>High-order bits<br>select range<br>**----- End of picture text -----**<br>


If Requests need multiple Completions to return the requested data, a single Completion won’t stop the timer. Instead, the timer continues to run until all the data has been returned regardless of how many Completions are needed. If only part of the data has been returned when the timeout occurs, the Requester may discard or keep that data. 

**665** 

**PCI Ex ress Technolo p gy** 

## **Link Flow Control Related Errors** 

Prior to forwarding the packet to the Data Link Layer for transmission, the Transaction Layer must check Flow Control (FC) credits to ensure that the receive buffers of the Link neighbor have sufficient room to hold it. Flow Con‐ trol violations may occur, and they are considered uncorrectable. Protocol viola‐ tions related to Flow Control can detected by and associated with the port receiving the Flow Control information. Some examples are given here: 

- Link partner fails to advertise at least the minimum number of FC credits defined by the spec during FC initialization for any Virtual Channel. 

- Link partner advertises more than the allowed maximum number of FC credits (up to 2047 unused credits for data payload and 127 unused credits for headers). 

- Receipt of FC updates containing non‐zero values in credit fields that were initially advertised as infinite. 

- A receive buffer overflow, resulting in lost data. This check is optional but a detected violation is considered to be a Fatal error. 

## **Malformed TLP** 

TLPs arriving in the Transaction Layer are checked for violations of the packet formatting rules. A violation in the packet format is considered a Fatal error because it means the transmitter has made a grievous mistake in protocol, such as failing to properly maintain its counters, and the result is that it’s no longer performing as expected. Some examples of a packet being considered mal‐ formed (badly formed) include the following: 

- Data payload exceeds Max payload size. 

- Data length does not match length specified in the header. 

- Memory start address and length combine to cause a transaction to cross a naturally‐aligned 4KB boundary. 

- TLP Digest (TD field) indication doesn’t correspond with packet size (ECRC is unexpectedly missing or present). 

- Byte Enable violation. 

- Undefined Type field values. 

- Completion that violates the Read Completion Boundary (RCB) value. 

- Completion with status of Configuration Request Retry Status in response to a Request other than a configuration Request. 

- Traffic Class field contains a value not assigned to an enabled Virtual Chan‐ nel (this is also known as TC Filtering). 

**666** 

**Chapter 15: Error Detection and Handling** 

- I/O and Configuration Request violations (checking optional) ‐ examples: TC field, Attr[1:0], and the AT field must all be zero, while the Length field must have a value of one. 

- Interrupt emulation messages sent downstream (checking optional). 

- TLP received with a TLP Prefix error: 

   - 

   - TLP Prefix but no TLP Header 

- End‐to‐End TLP Prefixes preceding Local Prefixes 

- Local TLP Prefix type not supported 

- 

      - More than 4 End‐to‐End TLP Prefixes 

   - More End‐to‐End TLP Prefixes than are supported 

- Transaction type requiring use of TC0 has a different TC value: 

   - 

   - I/O Read or Write Requests and corresponding Completions 

- Configuration Read or Write Requests and corresponding Completions 

- — Error Messages 

- INTx messages 

- Power Management messages 

- Unlock messages 

- Slot Power messages 

- LTR messages 

- 

   - OBFF messages 

- AtomicOp operand doesn’t match an architected value. 

- AtomicOp address isn’t naturally aligned with operand size. 

- Routing is incorrect for transaction type (e.g., transactions requiring routing to Root Complex detected moving away from Root Complex). 

## **Internal Errors** 

## **The Problem** 

The first versions of the PCIe spec did not include a mechanism for reporting errors within a device that were unrelated to transactions on the interface itself. For Endpoints this wasn’t really a problem because they have a vendor‐specific device driver associated with them that can detect and report internal errors. However, Switches are considered system resources that are managed by the OS, and typically don’t have software to help with internal error detection. In high‐end systems, the ability to contain errors is important, so Switch vendors created proprietary means of handling internal errors. Unfortunately, since dif‐ ferent vendor solutions were incompatible with each other, the end result was that they were seldom used. 

**667** 

**PCI Ex ress Technolo p gy** 

## **The Solution** 

To alleviate this situation, a standardized internal error reporting option was added with the 2.1 spec version. The definition of what constitutes an internal error is beyond the scope of the spec, but they can be reported as either Cor‐ rected or Uncorrectable Internal Errors. 

A Corrected Internal Error means an error was masked or worked around by the hardware with no loss of information or improper behavior. An example would be an ECC error on an internal memory location that was corrected auto‐ matically. On the other hand, an Uncorrectable Internal Error means improper operation has resulted with potential data loss, such as a parity error on an internal memory location. Reporting internal errors is optional and, if it is used, the AER (Advanced Error Reporting) registers must be present to support it. 

## **How Errors are Reported** 

## **Introduction** 

PCI Express includes three methods of reporting errors, as shown below. The first two, Completions and poisoned packets, were covered earlier, so our next topic will be the error Messages. 

- Completions — Completion Status reports errors back to the Requester 

- Poisoned Packet — reports bad data in a TLP to the receiver 

- Error Message — reports errors to the host (software) 

## **Error Messages** 

PCIe eliminated the sideband signals from PCI and replaced them with Error Messages. These Messages provide information that could not be conveyed with the PERR# and SERR# signals, such as identifying the detecting Function and indicating the severity of the error. Figure 15‐9 illustrates the Error Message format. Note that they’re routed to the Root Complex for handling. The Mes‐ sage Code defines the type of Message being signaled. Not surprisingly, the spec defines three types of error Messages, as shown in Table 15‐2. 

**668** 

**Chapter 15: Error Detection and Handling** 

_Table 15‐2: Error Message Codes and Description_ 

**==> picture [389 x 479] intentionally omitted <==**

**----- Start of picture text -----**<br>
Message<br>Name Description<br>Code<br>30h ERR_COR Device detected a correctable error. This is automati‐<br>cally corrected by hardware and doesn’t require soft‐<br>ware attention. However, it can be helpful to report<br>them anyway so software can watch for trends like<br>an increasing number of correctable errors.<br>31h ERR_NONFATAL Indicates an uncorrectable Non‐Fatal error. No hard‐<br>ware correction mechanism was available but the<br>Link is still working reliably. Software attention will<br>be required to resolve the problem.<br>33h ERR_FATAL Indicates an uncorrectable Fatal error. No hardware<br>correction mechanism was available and Link opera‐<br>tion has failed in some important respect. Software<br>attention will be required and a reset of at least one<br>device will probably be required to resolve this issue.<br>Figure 15‐9: Error Message Format<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 1 1 0  0 0 0 tr H D P<br>Message Code<br>Byte 4 Requester ID Tag<br>(30h, 31h or 33h)<br>Byte 8 Reserved for Error Messages<br>Byte 12 Reserved for Error Messages<br>Route to Root Complex 30h = ERR_COR<br>31h = ERR_NONFATAL<br>33h = ERR_FATAL<br>**----- End of picture text -----**<br>


**669** 

**PCI Ex ress Technolo p gy** 

## **Advisory Non-Fatal Errors** 
