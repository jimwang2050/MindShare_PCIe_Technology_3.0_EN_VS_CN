Fatal errors indicate that a Link or Device has had an operational failure, caus‐ ing data loss that is unlikely to be recovered. For these cases, resetting at least the failed Link or Device will probably be the first step in any recovery process because it’s clearly not operational for some reason. The spec also invites imple‐ mentation‐specific approaches, in which software may attempt to limit the effects of the failure, but it doesn’t define any particular actions that should be taken. An example of this type of error would be a receiver buffer overflow, in which case information has been lost because flow control tracking counters have gotten out of sync with each other. Since there’s no mechanism to fix this, a reset of this Link will usually be required. 

## **PCIe Error Checking Mechanisms** 

The scope of PCIe error checking focuses on errors associated with the Link and packet delivery, as shown in Figure 15‐2 on page 653. Errors that don’t pertain to Link transmission are not reported through PCIe error‐handling mechanisms and would need proprietary methods to report them, such as device‐specific 

**652** 

**Chapter 15: Error Detection and Handling** 

interrupts. Each layer of the interface includes error checking capabilities, and these are summarized in the sections that follow. 

_Figure 15‐2: Scope of PCI Express Error Checking and Reporting_ 

**==> picture [291 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) Link (RX) (TX)<br>Scope of PCIe Error Reporting<br>**----- End of picture text -----**<br>


## **CRC** 

Before diving into error handling as it relates to the layers, it will help to first discuss the concept of CRC (Cyclic Redundancy Check) because it’s an integral part of PCIe error checking. A CRC code is calculated by the transmitter based on the contents of the packet and adds it to the packet for transmission. The CRC name is derived from the fact that this _check_ code (calculated from the packet to check for errors) is _redundant_ (adds no information to the packet), and is derived from _cyclic_ codes. Although a CRC doesn’t supply enough informa‐ tion to do automatic error correction the way ECC (Error Correcting Code) can, it does provide robust error detection. CRCs are also commonly used in serial transports because they’re good at detecting a string of incorrect bits. 

**653** 

## **PCI Ex ress Technolo p gy** 

CRCs have two different usage cases in PCIe. One is the mandatory LCRC (Link CRC) generated and checked in the Data Link Layer for every TLP that goes across a Link. It’s intended to detect transmission errors on the Link. 

The second is the optional ECRC (End‐to‐end CRC) that’s generated in the Transaction Layer of the sender and checked in the Transaction Layer of the ulti‐ mate target of the packet. This is intended to detect errors that might otherwise be silent, such as when a TLP passes through an intermediate agent like a Switch, as shown in Figure 15‐3 on page 654. In this illustration, the packet arrived safely on the downstream port of the Switch but while it was being stored or processed within the Switch a bit error occurred. The LCRC only pro‐ tects TLPs while on the Link. Once the Data Link Layer of the Ingress Port checks the LCRC, it removes it from the packet because a new LCRC will be cal‐ culated (which will include the new Sequence Number) at the Egress Port. This means that the packet is unprotected while inside the Switch. This is the pur‐ pose of having an ECRC. It is calculated at the originating device and is not removed or recalculated by intermediate devices. So if the target device is checking the ECRC and sees a mismatch, then there must have been an error somewhere along the way even though no LCRC error was seen. Note that using the ECRC requires the presence of the optional Advanced Error Report‐ ing registers, since they contain the bits to enable this functionality. 

_Figure 15‐3: ECRC Usage Example_ 

**==> picture [267 x 192] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>Internal<br>Bit Error Switch<br>No external  (LCRC)<br>transmission errors<br>PCIe<br>Endpoint<br>**----- End of picture text -----**<br>


**654** 

**Chapter 15: Error Detection and Handling** 

## **Error Checks by Layer** 

Different aspects of an incoming packet are checked in the different layers at the Receiver. Some error checking is listed as optional. For those cases, if the error occurs but the designer has chosen not to implement that form of checking, it will not be detected. 

## **Physical Layer Errors** 

A packet arriving at the Receiver arrives at the Physical Layer first. There are a few things that must be checked at this level and others that may optionally be checked. Link training also takes place at this layer, and a variety of problems may arise during that process but those and other details of the Physical Layer are covered in Chapter 14, entitled ʺLink Initialization & Training,ʺ on page 505. In summary, though, Physical Layer errors, also called Receiver Errors or Link Errors, include the following cases: 

- When using 8b/10b, checking for decode violations (checking required) 

- Framing violations (optional for 8b/10b, required for 128b/130b) 

- Elastic buffer errors (checking optional) 

- Loss of symbol lock or Lane deskew (checking optional) 

If a TLP was in progress when a Receiver Error was detected, it is discarded. To resolve the error, the Data Link Layer is signaled to send a NAK if one isn’t already pending. 

## **Data Link Layer Errors** 

After the Physical Layer, incoming packets go next into the Data Link Layer, where they are checked for several possible problems. The details of these con‐ ditions can be found in Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317. In summary, the errors are: 

- LCRC failure for TLPs 

- Sequence Number violation for TLPs 

- 16‐bit CRC failure for DLLPs 

- Link Layer Protocol errors 

As with the Physical Layer, if a TLP was in progress when an error is seen, the TLP is discarded and a NAK is scheduled if one isn’t already pending. 

There are some Data Link Layer errors to watch for at the transmitter, too, including REPLAY_TIMER expiring and the REPLAY_NUM counter rolling over. A timeout is handled by replaying the contents of the Replay Buffer and 

**655** 

**PCI Ex ress Technolo p gy** 

incrementing the REPLAY_NUM counter. The timer and counter are reset whenever an ACK or NAK arrives at the transmitter that indicates forward progress has been made (meaning it results in clearing one or more TLPs from the Replay Buffer). But if an Ack or Nak isn’t received quickly enough, the time‐ out condition is seen which will result in a replay. 

## **Transaction Layer Errors** 

Lastly, if incoming TLPs pass all the checks at the Physical and Data Link Lay‐ ers, they will finally reach the Transaction Layer, where they are checked for: 

- ECRC failure (checking optional) 

- Malformed TLP (error in packet format) 

- Flow Control Protocol violation 

- Unsupported Requests 

- Data Corruption (poisoned packet) 

- Completer Abort (checking optional) 

- Receiver Overflow (checking optional) 

As with the Data Link Layer, there are some error checks at the transmitter Transaction Layer, too, such as: 

- Completion Timeouts 

- Unexpected Completion (Completion does not match pending Request) 

## **Error Pollution** 

A problem can arise if a device sees several problems for the same transaction. This could result in several errors getting reported (referred to as “Error Pollu‐ tion”). To avoid this, reported errors are limited to only the most significant one. For example, if a TLP has a Receiver Error at the Physical Layer, it would certainly be found to have errors at the Data Link Layer and Transaction Layers, too, but reporting them all would just add confusion. What is most relevant is reporting the first error that was seen. Consequently, if an error is seen in the Physical Layer, there’s no reason to forward the packet to the higher layers. Similarly, if an error is seen in the Data Link Layer, then the packet won’t be for‐ warded to the Transaction Layer. Offending packets at one level are not for‐ warded to the next level but are dropped. 

Still, multiple errors may be seen for the same packet at the Transaction Layer. Only the most significant one should be reported in the order of priority as defined by the spec. Transaction Layer error priority from highest to lowest is: 

**656** 

**Chapter 15: Error Detection and Handling** 

- Uncorrectable Internal Error 

- Receiver Buffer Overflow 

- Flow Control Protocol Error 

- ECRC Check Failed 

- Malformed TLP 

- AtomicOp Egress Blocked 

- TLP Prefix Blocked 

- ACS (Access Control Services) Violation 

- MC (Multi‐cast) Blocked TLP 

- UR (Unsupported Request), CA (Completer Abort), or Unexpected Com‐ pletion 

- Poisoned TLP Received 

As an example, a TLP might experience an ECRC fault caused by a corrupted header. Since something was corrupted within the packet, it might also be seen as Malformed or possibly as an Unsupported Request. The ECRC fault is the highest priority, since it means that the header contents may have been cor‐ rupted, and due to this, there is no point in reporting errors that depend on those contents. 

## **Sources of PCI Express Errors** 

Rather than consider all of the error conditions individually, it will be helpful to group them into common areas. 

## **ECRC Generation and Checking** 

As mentioned earlier, ECRC generation and checking requires the optional Advanced Error Reporting configuration register structure to be present, as shown in Figure 15‐4 on page 658. Configuration software checks for this capa‐ bility register to determine whether ECRCs are supported in a Function. If it is, a write to the Error Capability and Control register can be used to enable it. 

**657** 

**PCI Ex ress Technolo p gy** 

_Figure 15‐4: Location of Error‐Related Configuration Registers_ 

**==> picture [287 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
Byte 0d<br>Status Command<br>Header<br>63d CapPtr<br>PCI<br>Required Compatible<br>PCIe Capability Block<br> Space<br>255d<br>Advanced Error Reporting<br>Optional<br> Capability Structure<br>Other PCIe Extended<br>Capability Structures Capability<br> Space<br>4095d<br>**----- End of picture text -----**<br>


A device enabled to generate ECRCs originates a TLP (Request or Completion), computes the 32‐bit ECRC based on the header and data portions of the packet and adds it to the end of the packet. The ECRC is called “end‐to‐end” because the intent is that it will be generated at the TLP’s origin and never stripped off or regenerated by any intermediate device along its path. Switches in the path between the originating and receiving devices are allowed to check and report ECRC errors but aren’t required to do so. Whether or not there is an error, a Switch must still forward the packet unaltered so that the ultimate target device can evaluate the ECRC and take appropriate steps. If a Switch is acting as the originator or recipient of the TLP it can participate like an ordinary device in ECRC generation and checking. For more on the topic of how a Switch is allowed to report such errors, see “Advisory Non‐Fatal Errors” on page 670. 

**658** 

**Chapter 15: Error Detection and Handling** 

## **TLP Digest** 
