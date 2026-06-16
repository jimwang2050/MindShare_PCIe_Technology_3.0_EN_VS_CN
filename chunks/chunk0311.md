Since we’ve just seen that both types of Uncorrectable errors will need software attention, it sounds counter‐intuitive to say that there are cases where it’s prefer‐ able that a device not report Non‐Fatal errors it detects, but there are. These cases are predominantly based on the role of the detecting agent (Requester, Completer, or Intermediate device) and the type of error. The problem is that multiple devices might report an error caused by the same event and, on some platforms, sending one of the Non‐Fatal Error Messages (ERR_NONFATAL) can prevent software from properly handling the error. For example, if an End‐ point reports an error, its device driver will be called to service the situation. However, if a Switch reports an error first for the same transaction, system soft‐ ware might be called to investigate and might not understand what the driver was trying to accomplish or what would be the optimal response. 

That example illustrates that some detecting agents aren’t the best ones to deter‐ mine the ultimate disposition of the error and shouldn’t send an uncorrectable message. Instead, such an agent can signal an advisory notification to software with ERR_COR. This avoids confusion about the source of the uncorrectable error but still gives software a little more information about what happened. Eventually, the appropriate detecting agent will send the ERR_NONFATAL message whenever it sees the error. Beginning with the 1.1 spec revision, a new field was added in the PCI Express Device Capabilities register to indicate sup‐ port for this capability as shown in Figure 15‐10 on page 670. This bit must be set for every agent that is compliant with the 1.1 spec or later. 

_Figure 15‐10: Device Capabilities Register_ 

**==> picture [264 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capabilities Register<br>31 28 27 26 25 18 17 16 15 14 12 11 9 8 6 5 4 3 2 0<br>RsvdP RsvdP<br>Function-Level Reset Capability<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>Role-Based Error Reporting<br>Undefined<br>Endpoint L1 Acceptable Latency<br>Endpoint L0s Acceptable Latency<br>Extended Tag Field Supported<br>Phantom Functions Supported<br>Max Payload Size Supported<br>**----- End of picture text -----**<br>


**670** 

**Chapter 15: Error Detection and Handling** 

In spite of the reasons just described, software might want to stop operation as soon as some advisory errors are seen by an intermediate device. Since newer devices will always perform role‐based error reporting, an override mechanism is needed. To handle this case, software can escalate the severity of the advisory errors from Non‐Fatal to Fatal in the AER (Advanced Error Reporting) registers. Since there is no “advisory fatal” case, the error will now be reported as a Fatal Error (ERR_FATAL), if enabled, regardless of the role of the device. 

## **Advisory Non-Fatal Cases** 

The spec lists five situations for which an advisory message (ERR_COR) is pre‐ ferred over a ERR_NONFATAL message. In each of these cases, the detecting agent will handle the error as an Advisory Non‐Fatal Error. This means that a Non‐Fatal condition will be handled by sending an ERR_COR, assuming the agent has AER registers and has enabled ERR_COR. If it doesn’t have AER reg‐ isters or ERR_COR was not enabled, it sends no Error Message. The five cases are as follows: 

1. Completer sent a Completion with UR or CA Status. The expectation in this case is that the Requester will have a mechanism to handle the error when it sees the offending Completion and will be the best agent to send whatever Error Messages are needed. A ERR_NONFATAL message from the Compl‐ eter would just be confusing, so it must be handled as Advisory Non‐Fatal (ERR_COR). 

   - Curiously, there is no PCIe mechanism for the Requester to report that it received a Completion with this status. Instead, a design‐specific method like an interrupt will be needed to get device driver attention. An important example of this happens when the Root Complex receives a Completion with UR or CA status in response to a Configuration Read Request. On some platforms the response is to return all 1’s to software for this case, to support backward compatibility with PCI enumeration (configuration probing) software. 

2. Intermediate device detected an error. This case comes up in systems that employ Switches because a detecting agent may not be the final destination for a TLP. As an example of this, consider Figure 15‐11 on page 672, show‐ ing a poisoned packet delivered through an intermediate Switch. The TLP is seen as a Non‐Fatal error by the Switch but it can only signal an ERR_COR message instead (as long as it’s enabled to do so). To explore this concept a little more, why wouldn’t we want the Switch to report ERR_NONFATAL? One reason is seen by looking at error tracking in the AER registers. Figure 15‐12 on page 672 shows the AER registers that track the Source ID (BDF of the sending device) of Error Messages coming into a Root Port and we can see that there’s only one space available for 

**671** 

## **PCI Ex ress Technolo p gy** 

uncorrectable errors. If multiple uncorrectable errors are seen, that fact will be noted but only the first source ID will be saved since it is considered to be the probable cause of subsequent errors. It’s important, therefore, that uncorrectable errors come from the most appropriate device to report them. It’s worth noting that it’s still helpful for intermediate devices to report ERR_COR, because it allows software to determine where the error was first detected. 

_Figure 15‐11: Role‐Based Error Reporting Example_ 

**==> picture [230 x 219] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Poisoned<br>Packet<br>ERR_COR<br>PCIe<br>PCIe Switch Endpoint<br>Endpoint<br>PCIe Legacy<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


_Figure 15‐12: Advanced Source ID Register_ 

**==> picture [333 x 77] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Source Identification Register<br>of the AER Capability Structure<br>31 0<br>ERR_FATAL/NONFATAL Source ID ERR_COR Source ID<br>(ROS) (ROS)<br>ROS: Read-Only and Sticky<br>**----- End of picture text -----**<br>


**672** 

**Chapter 15: Error Detection and Handling** 

As another example, 1.0a devices that have the UR Reporting Enable bit cleared but don’t have the Role‐Based Error Reporting capability are unable to report any error Messages when a UR error is detected (for posted or non‐posted Requests). In contrast, a 1.1‐compliant or later Completer that has the SERR# Enable bit set will send an ERR_NONFATAL or ERR_FATAL message for bad posted Requests, even if the Unsupported Request Report‐ ing Enable bit is clear, so as to avoid silent data corruption. But it won’t send an error Message for non‐posted Requests received, so as to support the PCI‐compatible configuration method of probing with configuration reads. It’s recommended that software keep the UR Error Reporting Enable bit clear for devices that are not capable of Role‐Based Error Reporting, but set it for those that are. That way, UR errors are reported on bad posted requests, but not for bad non‐posted requests like configuration probing transactions, and backward compatibility with older software is main‐ tained. 

The spec also mentions that poisoned TLPs sent to the Root will be handled in the same way if the Root is acting as an intermediate agent, but there is one exception: If the Root doesn’t support Error Forwarding, it will be unable to communicate the poisoned error with the TLP and must report this as a Non‐Fatal error instead. 

3. Destination device received a poisoned TLP. Normally, Endpoints would report the Non‐Fatal error in this case, but there’s an exception to this rule: If the ultimate destination device is able to handle the poisoned data in a way that allows for continued operation, it must treat this case as an Advi‐ sory Non‐Fatal Error instead. 

   - An example of this behavior might be an audio device that receives stream‐ ing data that has been poisoned. In this situation, the data may be accepted even though it’s known to be corrupted because pausing the audio flow long enough to get software attention and take remedial action would be a worse alternative than allowing a glitch in the sound output. 

4. Requester experienced a Completion Timeout. This is a similar case to the previous one; if the Requester has a means of continuing operation in spite of the problem then it must treat this as an Advisory Non‐Fatal Error. A simple work‐around for the Requester in this case would simply be to send the request again and hope for better results this time. Clearly, this would only make sense if the previous request did not cause any side effects, but Requesters are permitted to do this as often as they like (although the spec says the number of retries must be finite). 

5. Unexpected completion received. This must be handled as an Advisory Non‐Fatal Error. The reason is that it was probably caused by a mis‐routed Completion and the original Requester will eventually report a Completion timeout. To allow that other Requester to attempt a retry of the failed 

**673** 

**PCI Ex ress Technolo p gy** 

request, it’s important that the one that sees the Unexpected Completion not send an Non‐Fatal message. 

## **Baseline Error Detection and Handling** 

This section defines the required support for detecting and reporting PCI Express errors. Compliant devices must include: 

- PCI‐Compatible support — required to honor PCI‐compatible error control and status fields for older software that has no awareness of PCI Express. 

- PCI Express Error reporting — uses standard PCIe structures to for error control and status which can be used by newer software that does have knowledge of PCI Express. 

## **PCI-Compatible Error Reporting Mechanisms** 

## **General** 

PCI Express errors are mapped into the original PCI configuration register bits for backward compatibility, allowing error status and control to be accessible to PCI‐compliant software. To understand the features available from the PCI‐ compatible point of view, consider the error‐related bits of the Command and Status registers located within the Configuration header. Some of the field defi‐ nitions have been modified to reflect the related PCIe error conditions and reporting mechanisms. The PCI Express errors tracked by the PCI‐compatible registers are: 

- Transaction Poisoning/Error Forwarding (synonymous to data parity error in PCI) 

- Completer Abort (CA) detected by a Completer (synonymous to Target Abort in PCI) 

- Unsupported Request (UR) detected by a Completer (synonymous to Mas‐ ter Abort in PCI) 

As mentioned earlier, the PCI mechanism for reporting errors is the assertion of PERR# (data parity errors) and SERR# (unrecoverable errors). The PCI Express mechanisms for reporting these events are the Completion Status values in Completions and Error Messages to the Root. 

**674** 

**Chapter 15: Error Detection and Handling** 

## **Legacy Command and Status Registers** 

Figure 15‐13 on page 675 illustrates the Command register and the location of the error‐related fields. These bits are set to enable baseline error reporting under control of PCI‐compatible software. Table 15‐3 defines the specific effects of each bit. 

_Figure 15‐13: Command Register in Configuration Header_ 

**==> picture [390 x 396] intentionally omitted <==**

**----- Start of picture text -----**<br>