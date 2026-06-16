If the optional ECRC capability is enabled, a special bit called TD (TLP Digest) is set in the header to indicate that it’s present at the end of the packet (the ECRC is also called the Digest). The TD bit in the packet header is shown in Figure 15‐ 5 on page 659. The spec emphasizes that this bit must be treated with special care when forwarding a TLP because if it’s missing but the ECRC is present, or vice‐versa, then the packet will be considered Malformed. 

_Figure 15‐5: TLP Digest Bit in a Completion Header_ 

**==> picture [373 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


## **Variant Bits Not Included in ECRC Mechanism** 

The ECRC is calculated based on the contents of the header and data. Since these are not expected to change, the result should be the same when the check is performed at the receiver. However, it turns out that two header bits can legally change while the packet is in flight: bit 0 of the Type field, and the EP bit. Bit 0 of the Type field can change in Configuration Requests for the simple rea‐ son that the Request will be Type 1 until it has reached its destination bus, and then it will become Type 0. That involves changing bit 0 of the Type field. The EP bit can also be legally changed by intermediate devices if they detect a data error. For example, if a Switch forwards a TLP but it suffers an internal error of some kind that corrupts the data, setting the EP bit as it goes out the Egress Port is one way to report the error (known as error forwarding or data poisoning). 

Since these two bits can change while the packet is in flight they are called “variant bits” and cannot be used in the generation or checking of ECRC. Instead, their values are always assumed to be 1b for ECRC generation and checking instead of using the actual values. That way the ECRC doesn’t depend on them and will be correctly evaluated. 

**659** 

**PCI Ex ress Technolo p gy** 

The actions taken when an ECRC error is detected are beyond the scope of the spec, but the possible choices will depend on whether the error is found in a Request or a Completion. 

- **ECRC in Request** — Completers that detect an ECRC error must set the ECRC error status bit. They may also choose not to return a Completion for this Request, resulting in a Completion timeout at the Requester, whose software might then choose to reschedule the Request. 

- **ECRC in Completion** — Requesters that detect an ECRC error must set the ECRC error status bit. Besides the standard error reporting mechanism, they may also choose to report the error to their device driver with a Func‐ tion‐specific interrupt. As before, the software might decide to reschedule the failed Request. 

In either case, an Uncorrectable Non‐fatal error Message may be sent to the sys‐ tem. If so, the device driver would probably be accessed to check the status bits in the _Uncorrectable Error Status Register_ and learn the nature of the error. If pos‐ sible, the failed Request may be rescheduled, but other steps might be needed. 

## **Data Poisoning** 

Data poisoning, also called Error Forwarding, provides an optional way for a device to indicate that the data associated with a TLP is corrupted. In these cases, the EP (Error Poisoned) bit in the packet header is set to indicate the error. The EP bit is shown in Figure 15‐6 on page 660. 

_Figure 15‐6: The Error/Poisoned Bit in a Completion Header_ 

**==> picture [373 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


**660** 

**Chapter 15: Error Detection and Handling** 

Anytime data is transferred, such as in write Requests or Completions with data, corruption of that data could happen which needs to be reported to the target device. In each of these cases, the packet can be forwarded to the recipient but marked as having bad data by the EP bit in the header. The thoughtful reader may wonder why one might want to send data that is already known to be bad. As it happens, there are some cases where it’s useful: 

1. If a Request results in a Completion returned with data, but that data encountered an error as it was gathered from the target (like a parity or ECC failure in memory), then what is the best way to report it? One approach would be not to send the Completion at all but, if the error isn’t reported in some other way, the system only sees a Completion timeout at the Requester. That response isn’t very helpful because any number of prob‐ lems might result in that outcome. 

   - If, on the other hand, the Completion is delivered with the poisoned bit set, then at least the Requester can see that the round‐trip path to the Completer must have been working correctly. Therefore, the problem must have occurred internally to the Completer or else in a Switch that was in the path. What steps will be taken will be implementation specific, but more is known about what must have gone wrong than if the Completion simply timed out. 

2. It can be used to report an intermediate problem. If a data payload is cor‐ rupted while passing through a Switch, the packet can still be forwarded with the EP bit set to indicate the problem. 

3. It may be that the target device can accept the data with errors. As an exam‐ ple, an audio output device needs to receive a timely data stream to work well. If incoming data has an error, the consequences are small (glitch in the audio output) and the time to recover would be long enough to cause a noticeable delay, so it can be better to take it as is rather than attempting recovery of the data. 

4. A target device might have a means of correcting the data. The data might be directly recoverable, or the target might have a means of re‐creating parts of it, or have some other means of working around the problem. 

The spec states that data poisoning applies only to the data payload associated with a packet (such as Memory, Configuration, or I/O writes and Completions) and never to the contents of the TLP header. Consequently, a receiver’s behavior is undefined if it sees a poisoned packet (EP=1) with no payload (like a poisoned memory read). Poisoning can only be done at the Transaction Layer of a device; the Data Link Layer does not examine or affect the contents of the TLP header. 

Error forwarding support is stated to be optional for transmitters, and the absence of such a statement for receivers implies that it’s not optional for them. 

**661** 

## **PCI Ex ress Technolo p gy** 

If a transmitter supports it, it’s enabled with the Parity Error Response bit in the legacy Command register. That’s because a Poisoned packet is roughly analo‐ gous to a parity error in PCI, since that’s how PCI reports bad data. Receipt of a poisoned packet may be reported to the system with an error Message if enabled and, if the optional Advanced Error Reporting registers are present, will also set the Poisoned TLP status bit. 

As one might expect, poisoned writes to control locations are not allowed to modify the contents in the target. Examples given in the spec are Configuration writes, IO or memory writes to control registers, and AtomicOps. Switches that receive poisoned packets must forward them unchanged to the destination port although, if they’ve been enabled to do so, they must report this packet as an error to help software determine where the error happened. Completers that receive a poisoned non‐posted Request are expected to return a Completion with a status of UR (Unsupported Request). 

## **Split Transaction Errors** 

A variety of failures can occur during a split transaction associated with non‐ posted requests. PCIe defines a status field within the Completion header that allows the Completer to report some errors back to the Requester. Figure 15‐7 on page 662 illustrates the location of this field in a completion header and Table 15‐1 on page 663 gives the possible values. As the table shows, only four encodings are defined, two of which represent error conditions. 

_Figure 15‐7: Completion Status Field within the Completion Header_ 

**==> picture [378 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 x 0 0 1 0 1 0 tr H D P 0 0<br>Compl. B<br>Byte 4 Completer ID Status MC Byte Count<br>Byte 8 Requester ID Tag R Lower Address<br>**----- End of picture text -----**<br>


**662** 

**Chapter 15: Error Detection and Handling** 

_Table 15‐1: Completion Code and Description_ 

|**Status Code**|**Completion Status Definition**|
|---|---|
|000b|Successful Completion (SC)|
|001b|Unsupported Request (UR) ‐ error|
|010b|Configuration Request Retry Status (CRS)|
|011b|Completer Abort (CA) ‐ error|
|100b ‐ 111b|Reserved|



## **Unsupported Request (UR) Status** 

If a receiver doesn’t support a Request, it returns a Completion with UR status. The spec defines a number of conditions that could result in a UR status. Some examples are: 

- Request type not supported (example: IO Request to native Endpoint or MRdLk to native Endpoint) 

- Message with unsupported or undefined message code 

- Request does not reference address space mapped to the device 

- Request address isn’t mapped within a Switch Port’s address range 

- Poisoned write Request (EP=1) targets an I/O or Memory‐mapped control space in the Completer. Such Requests must not be allowed to modify the location and are instead discarded by the Completer and reported with a Completion having a UR status. 

- A downstream Root or Switch Port receives a configuration Request target‐ ing a device on its Secondary Bus that doesn’t exist (e.g. a device with a non‐zero device number, unless ARI is enabled). The Port must terminate the Request and return a Completion with UR status because the down‐ stream Device number is required to be zero (unless ARI, Alternative Rout‐ ing‐ID Interpretation, is enabled). 

- Type 1 configuration Request is received at an Endpoint. 

- Completion using a reserved Completion Status field encoding must be interpreted as UR. 

- A function in the D1, D2, or D3hot power management state receives a Request other than a configuration Request or Message. 

- A TLP without the No Snoop bit set in its header is routed to a port that has the Reject Snoop Transactions bit set in its VC Resource Capability register. 

**663** 

**PCI Ex ress Technolo p gy** 

## **Completer Abort (CA) Status** 

Several circumstances can occur that could result in a Completer returning this CA status to the Requester. Some examples are: 

- Completer receives a Request that it cannot complete without violating its programming rules. For example, some Functions may be designed to only allow accesses to some registers in a complete and aligned manner (e.g. a 4‐ byte register may require a 4‐byte aligned access). Any attempt to access one of these registers in a partial or misaligned fashion (e.g. reading only two bytes of a 4‐byte register) would fail. Such restrictions are not violations of the spec, but rather legal constraints associated with the programming interface for this Function. Access to such a Function is based on the expec‐ tation that the device driver understands how to access its Function. 
