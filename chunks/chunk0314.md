- Receiver Error (optional) — Physical Layer detected an error in the incom‐ ing packet. The packet is discarded at the Physical Layer, any buffer space allocated to it is released, and the Link Layer is informed that a receive error occurred. 

- Bad TLP — Data Link Layer detected a packet with a bad LCRC, an out‐of‐ sequence Sequence Number or an incorrectly nullified packet. In each case, the Link Layer discards the packet and reports a Nak DLLP to the transmit‐ ter, triggering a TLP replay. 

- Bad DLLP — Data Link Layer noticed an incoming DLLP had a 16‐bit CRC failure so the packet is dropped. A subsequent DLLP of the same type is expected to make up for the information it contained. 

- REPLAY_NUM Rollover — At the Data Link Layer, a set of TLPs have been sent without success (no Ack) four times in a row and this counter has rolled over back to zero. Hardware will automatically retrain the link in an attempt to clear the failure condition, then start the sequence again by replaying the contents of the Replay Buffer. 

**689** 

## **PCI Ex ress Technolo p gy** 

- Replay Timer Timeout — At the Data Link Layer, transmitted TLPs have not received an acknowledgement (Ack or Nak) within the timeout period. Hardware automatically replays all unacknowledged TLPs, meaning all packets in the Replay Buffer. 

- Advisory Non‐Fatal Error — Detection of these cases (see “Advisory Non‐ Fatal Errors” on page 670) is logged in the corresponding Uncorrectable Error Status register and as a correctable error here. It may also generate a Correctable Error Message, if enabled. 

- Corrected Internal Error (optional) — An error internal to the device was detected, but it was corrected or worked around without causing improper behavior. 

- Header Log Overflow (optional) — The maximum number of headers that can be stored in the header log has been reached. The number is just one if the Multiple Header Recording Enable bit is not set in the Advanced Error Capability and Control register. 

## **Advanced Correctable Error Masking** 

Correctable Error reporting is controlled collectively by the Correctable Error Enable bit in the Device Control register, but also individually by the Correct‐ able Mask register, illustrated in Figure 15‐24. The default state of the mask bits is cleared, meaning an ERR_COR message can be delivered when any correct‐ able errors are detected if they’ve been enabled (meaning the Correctable Error Enable bit is set). However, software may choose to set bits in this mask register to prevent a message from being sent when those specific errors are detected. 

_Figure 15‐24: Advanced Correctable Error Mask Register_ 

**==> picture [353 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 14 13 12 11 9 8 7 6 5 1 0<br>RsvdP RsvdP RsvdP<br>Header Log Overflow Mask<br>Corrected Internal Error Mask<br>Advisory Non-Fatal Error Mask<br>Replay Timer Timeout Mask<br>REPLAY_NUM Rollover Mask<br>Bad DLLP Mask<br>Bad TLP Mask<br>Receiver Error Mask<br>Note: all bits designated RWS<br>**----- End of picture text -----**<br>


**690** 

**Chapter 15: Error Detection and Handling** 

## **Advanced Uncorrectable Error Handling** 

For uncorrectable errors, AER provides the ability to track which specific error has occurred, control whether it should be considered Fatal or Non‐Fatal, and choose whether it will result in an Uncorrectable Error Message being sent to the Root. 

## **Advanced Uncorrectable Error Status** 

When an uncorrectable error occurs, the corresponding bit in this register is automatically set by hardware (see Figure 15‐25 on page 691) regardless of whether the error will be reported to the Root. If multiple errors occur, hard‐ ware will set the corresponding bit for each error and will record which one was first in the First Error Pointer field of the Advanced Error Capability and Con‐ trol register. It may even happen that multiple instances of the same error are detected before the first one can be serviced. Hardware that is compliant with the 2.1 spec revision or later will be able to keep track of a design‐specific num‐ ber of those cases. 

_Figure 15‐25: Advanced Uncorrectable Error Status Register_ 

**==> picture [366 x 184] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdZ RsvdZ RsvdZ<br>TLP Prefix Blocked Error Status<br>Atomic Op Egress Blocked Status Undefined<br>MC Blocked TLP Status<br> Uncorrectable Internal Error Status<br>ACS Violation Status<br>Data Link<br>Unsupported Request Error Status Protocol<br>ECRC Error Status Error Status<br>Malformed TLP Status<br>Surprise Down<br>Receiver Overflow Status Error Status<br>Unexpected Completion Status<br>Completer Abort Status<br>Completion Timeout Status<br>Flow Control Protocol Error Status<br>Poisoned TLP Status<br>Note: all bits designated RW1CS<br>**----- End of picture text -----**<br>


The following list describes each of the register bits from right to left: 

- Undefined — Previously, this first bit represented a link training failure at the Physical Layer, but that meaning was removed with the 1.1 revision of 

**691** 

## **PCI Ex ress Technolo p gy** 

the spec. Software must now ignore any value in this bit but may write any value to it. This information was no longer needed because bit 5, Surprise Down Error, now includes the same information in a broader meaning: the Link is not communicating at the Physical Layer. 

- Data Link Protocol Errors — Caused by Data Link Layer protocol errors including the Ack/Nak retry mechanism. For example, a transmitter receives an Ack or Nak whose sequence number doesn’t correspond to an unacknowledged TLP or to the ACKD_SEQ number. 

- Surprise Down — If the Physical Layer reports LinkUp = 0b (Link is no longer communicating) unexpectedly, this will be seen as an error unless it was an allowed exception. For example, if the Link Disable bit has already been set, then it’s expected that LinkUp will be cleared and this condition won’t be an error. This bit is only valid for Downstream Ports, which makes sense because it won’t be possible to read status from an Upstream Port if the Link isn’t working. 

- Poisoned TLP — TLP was seen that had the EP bit set. 

- Flow Control Protocol Error (optional) — Errors associated with failures of the Flow Control mechanism. Example: receiver reports more than 2047 data credits. 

- Completion Timeout — A Completion is not received within the required amount of time after a non‐posted request was sent. 

- Completer Abort (optional) — Completer cannot fulfill a Request due to problems with the Request or failure of the Completer. 

- Unexpected Completion — Requester receives a Completion that doesn’t match any Requests that are awaiting a Completion. 

- Receiver Overflow (optional) — More TLPs have arrived than the Receive Buffer had room to accept, resulting in an overflow error. 

- Malformed TLP — Caused by errors associated with a received TLP header (see “Malformed TLP” on page 666). 

- ECRC Error (optional) — Caused by an ECRC check failure at the Receiver. 

- • Unsupported Request Error — Completer does not support the Request. Request is correctly formed and had no other errors, but cannot be fulfilled by the Completer, perhaps because it’s an invalid command for this device. 

- ACS Violation — Access control error was seen in a received posted or non‐ posted request. 

- Uncorrectable Internal Error — An internal error detected in the device could not be corrected or worked around by the hardware itself. 

- MC Blocked TLP — A TLP designated for Multi‐Cast routing was blocked. For example, an Egress Port can be programmed to block any MC hits that arrive with untranslated addresses (see “Routing Multicast TLPs” on page 896). 

- AtomicOp Egress Blocked — Egress Ports of routing elements can be pro‐ 

**692** 

**Chapter 15: Error Detection and Handling** 

   - grammed to block AtomicOps from being forwarded to agents that shouldn’t see them (see “AtomicOps” on page 897). 

- TLP Prefix Blocked Error — Egress Ports of routing elements can be pro‐ grammed not to forward TLPs containing End‐to‐End TLP Prefixes. If they then see one, they’ll drop the TLP and report this error. For more on this, see “TPH (TLP Processing Hints)” on page 899. 

Recall that the First Error Pointer in the Capability and Control Register indi‐ cates which unmasked uncorrectable error was the first to arrive since the pointer was last updated. Error handling software can read the pointer to find out which error to investigate first. As an example, if the pointer value is 18d, that means bit position 18 in the Uncorrectable Status register was first, which is a Malformed TLP. Once that error has been serviced, software writes a one to bit 18 in the status register to clear that event, which updates the First Error Pointer to the next‐most‐recent error 

## **Selecting Uncorrectable Error Severity** 

Software can select whether or not uncorrectable errors should be considered Fatal in this register, allowing errors to be treated differently for different appli‐ cations. For example, a Poisoned TLP will be a Non‐Fatal condition by default, and is treated as an Advisory Non‐Fatal error in some cases, as discussed ear‐ lier. But software can escalate it to Fatal by setting its severity bit to one and then it will no longer be an advisory case. The default severity values are illus‐ trated in the individual bit fields of Figure 15‐26 on page 694 (1 = Fatal, 0 = Non‐ Fatal). If they are enabled and not masked, those errors selected as Non‐Fatal will cause an ERR_NONFATAL message to be sent to the Root Complex, and those selected as Fatal will cause an ERR_FATAL message. 

**693** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐26: Advanced Uncorrectable Error Severity Register_ 

**==> picture [376 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdP 0 0 0 1 0 0 0 1 1 0 0 0 1 0 RsvdP 1 1 RsvdP x<br>TLP Prefix Blocked Error Severity<br>Atomic Op Egress Blocked Severity Undefined<br>MC Blocked TLP Severity<br> Uncorrectable Internal Error Severity Data Link<br>ACS Violation Severity Protocol Error<br>Unsupported Request Error Severity<br>Severity<br>ECRC Error Severity<br>Malformed TLP Severity Surprise Down<br>Receiver Overflow Severity Error Severity<br>Unexpected Completion Severity<br>Completer Abort Severity<br>Completion Timeout Severity<br>Flow Control Protocol Error Severity<br>Poisoned TLP Severity<br>Note: all bits designated RWS<br>**----- End of picture text -----**<br>


## **Uncorrectable Error Masking** 

Software can mask out individual errors so they won’t cause an error message to be sent by using the Advanced Uncorrectable Error Mask register, shown in Figure 15‐27 on page 694. The default condition is to allow Error Messages for each type of error (all mask bits are cleared). 

_Figure 15‐27: Advanced Uncorrectable Error Mask Register_ 

**==> picture [369 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 6 5 4 3 1 0<br>RsvdP RsvdP RsvdP<br>TLP Prefix Blocked Error Mask<br>Atomic Op Egress Blocked Mask Undefined<br>MC Blocked TLP Mask<br> Uncorrectable Internal Error Mask<br>ACS Violation Mask<br>Data Link<br>Unsupported Request Error Mask Protocol<br>ECRC Error Mask Error Mask<br>Malformed TLP Mask<br>Surprise Down<br>Receiver Overflow Mask Error Mask<br>Unexpected Completion Mask<br>Completer Abort Mask<br>Completion Timeout Mask<br>Flow Control Protocol Error Mask<br>Poisoned TLP Mask<br>Note: all bits designated RWS<br>**----- End of picture text -----**<br>


**694** 

**Chapter 15: Error Detection and Handling** 

## **Header Logging** 
