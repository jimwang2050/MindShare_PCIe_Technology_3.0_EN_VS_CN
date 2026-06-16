|Lane|The two differential pairs that allow a transmit and<br>receive path of one bit between two Ports. A Link can<br>consist of just one Lane or it may contain as many as 32<br>Lanes.|
|Lane‐to‐Lane Skew|Difference in arrival times for bits on different Lanes.<br>Receivers are required to detect this and correct it inter‐<br>nally.|
|Legacy Endpoint|An Endpoint that carries any of three legacy items for‐<br>ward: support for IO transactions, support for local 32‐<br>bit‐only prefetchable memory space, or support for the<br>locked transactions.|



**979** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|LFSR|Linear‐Feedback Shift Register; creates a pseudo‐ran‐<br>dom pattern used to facilitate scrambling.|
|Link|Interface between two Ports, made up of one or more<br>Lanes.|
|LTR|Latency‐Tolerance Reporting; mechanism that allows<br>devices to report to the system how quickly they need to<br>get service when they send a Request. Longer latencies<br>afford more power management options to the system.|
|LTSSM|Link Training and Status State Machine; manages the<br>training process for the Physical Layer.|
|Non‐posted Request|A Request that expects to receive a Completion in<br>response. For example, any read request would be non‐<br>posted.|
|Non‐prefetchable<br>Memory|Memory that exhibits side effects when read. For exam‐<br>ple, a status register that automatically self‐clears when<br>read. Such data is not safe to prefetch since, if the<br>requester never requested the data and it was discarded,<br>it would be lost to the system. This was an important<br>distinction for PCI bridges, which had to guess about the<br>data size on reads. If they knew it was safe to specula‐<br>tively read ahead in the memory space, they could guess<br>a larger number and achieve better efficiency. The dis‐<br>tinction is much less interesting for PCIe, since the exact<br>byte count for a transfer is included in the TLP, but<br>maintaining it allows backward compatibility.|
|Nullified Packet|When a transmitter recognizes that a packet has an error<br>and should not have been sent, the packet can be “nulli‐<br>fied”, meaning it should be discarded and the receiver<br>should behave as if it had never been sent. This problem<br>can arise when using “cut‐through” operation on a<br>Switch.|



**980** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|OBFF|Optimized Buffer Flush and Fill; mechanism that allows<br>the system to tell devices about the best times to initiate<br>traffic. If devices send requests during optimal times<br>and not during other times system power management<br>will be improved.|
|Ordered Sets|Groups of Symbols sent as Physical Layer communica‐<br>tion for Lane management. These often consist of just<br>control characters for 8b/10b encoding. They are created<br>in the Physical Layer of the sender and consumed in the<br>Physical Layer of the receiver without being visible to<br>the other layers at all.|
|PCI|Peripheral Component Interface. Designed to replace<br>earlier bus designs used in PCs, such as ISA.|
|PCI‐X|PCI eXtended. Designed to correct the shortcomings of<br>PCI and enable higher speeds.|
|PME|Power Management Event; message from a device indi‐<br>cating that power‐related service is needed.|
|Poisoned TLP|Packet whose data payload was known to be bad when<br>it was created. Sending the packet with bad data can be<br>helpful as an aid to diagnosing the problem and deter‐<br>mining a solution for it.|
|Polarity Inversion|The receiver’s signal polarity is permitted to be con‐<br>nected backwards to support cases when doing so<br>would simplify board layout. The receiver is required to<br>detect this condition and internally invert the signal to<br>correct it during Link Training.|
|Port|Input/output interface to a PCIe Link.|
|Posted Request|A Request packet for which no completion is expected.<br>There are only two such requests defined by the spec:<br>Memory Writes and Messages.|



**981** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|Prefetchable Memory|Memory that has no side‐effects as a result of being read.<br>That property makes it safe to prefetch since, if it’s dis‐<br>carded by the intermediate buffer, it can always be read<br>again later if needed. This was an important distinction<br>for PCI bridges, which had to guess about the data size<br>on reads. Prefetchable space allowed speculatively read‐<br>ing more data and gave a chance for better efficiency.<br>The distinction is much less interesting for PCIe, since<br>the exact byte count for a transfer is included in the TLP,<br>but maintaining it allows backward compatibility.|
|PTLP|Pending TLP ‐ Flow Control credits needed to send the<br>current TLP.|
|QoS|Quality of Service; the ability of the PCIe topology to<br>assign different priorities for different packets. This<br>could just mean giving preference to packets at arbitra‐<br>tion points, but in more complex systems, it allows mak‐<br>ing bandwidth and latency guarantees for packets.|
|Requester ID|The configuration address of the Requester for a transac‐<br>tion, meaning the BDF (Bus, Device, and Function num‐<br>ber) that corresponds to it. This will be used by the<br>Completer as the return address for the resulting com‐<br>pletion packet.|
|Root Complex|The components that act as the interface between the<br>CPU cores in the system and the PCIe topology. This can<br>consist of one or more chips and may be simple or com‐<br>plex. From the PCIe perspective, it serves as the root of<br>the inverted tree structure that backward‐compatibility<br>with PCI demands.|
|Run Length|The number of consecutive ones or zeros in a row. For<br>8b/10b encoding the run length is limited to 5 bits. For<br>128b/130b, there is no defined limit, but the modified<br>scrambling scheme it uses is intended to compensate for<br>that.|



**982** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Scrambling|The process of randomizing the output bit stream to<br>avoid repeated patterns on the Link and thus reduce<br>EMI. Scrambling can be turned off for Gen1 and Gen2 to<br>allow specifying patterns on the Link, but it cannot be<br>turned off for Gen3 because it does other work at that<br>speed and the Link is not expected to be able to work<br>reliably without it.|
|SOS|Skip Ordered Set ‐ used to compensate for the slight fre‐<br>quency difference between Tx and Rx.|
|SSC|Spread‐Spectrum Clocking. This is a method of reducing<br>EMI in a system by allowing the clock frequency to vary<br>back and forth across an allowed range. This spreads the<br>emitted energy across a wider range of frequencies and<br>thus avoids the problem of having too much EMI energy<br>concentrated in one particular frequency.|
|Sticky Bits|Status bits whose value survives a reset. This characteris‐<br>tic is useful for maintaining status information when<br>errors are detected by a Function downstream of a Link<br>that is no longer operating correctly. The failed Link<br>must be reset to gain access to the downstream Func‐<br>tions, and the error status information in its registers<br>must survive that reset to be available to software.|
|Switch|A device containing multiple Downstream Ports and<br>one Upstream Port that is able to route traffic between its<br>Ports.|
|Symbol|Encoded unit sent across the Link. For 8b/10b these are<br>the 10‐bit values that result from encoding, while for<br>128b/130b they’re 8‐bit values.|
|Symbol Lock|Finding the Symbol boundaries at the Receiver when<br>using 8b/10b encoding so as to recognize incoming Sym‐<br>bols and thus the contents of packets.|
|Symbol time|The time it takes to send one symbol across the Link ‐<br>4ns for Gen1, 2ns for Gen2, and 1ns for Gen3.|



**983** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|TLP|Transaction Layer Packet. These are created in the Trans‐<br>action Layer and passed through the other layers.|
|Token|Identifier of the type of information being delivered dur‐<br>ing a Data Stream when operating at Gen3 speed.|
|TPH|TLP Processing Hints; these help system routing agents<br>make choices to improve latency and traffic congestion.|
|UI|Unit Interval; the time it takes to send one bit across the<br>Link ‐ 0.4ns for Gen1, 0.2ns for Gen2, 0.125ns for Gen3|
|Uncorrectable Errors|Errors that can’t be corrected by hardware and thus will<br>ordinarily require software attention to resolve. These<br>are divided into Fatal errors ‐ those that render further<br>Link operation unreliable, and Non‐fatal errors ‐ those<br>that do not affect the Link operation in spite of the prob‐<br>lem that was detected.|
|USP|Upstream Port, meaning a Port that faces upstream, as<br>for an Endpoint or a Switch Upstream Port. This distinc‐<br>tion is meaningful in the LTSSM because the Ports have<br>assigned roles during Configuration and Recovery.|



**984** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Variables|A number of flags are used to communicate events and<br>status between hardware layers. These are specific to<br>state transitions in the hardware are not usually visible<br>to software. Some examples:<br>—<br>LinkUp ‐ Indication from the Physical Layer to the<br>Data Link Layer that training has completed and<br>the Physical Layer is now operational.<br>—<br>idle_to_rlock_transitioned ‐ This counter tracks<br>the number of times the LTSSM has transitioned<br>from Configuration.Idle to the Recovery.RcvrLock<br>state. Any time the process of recognizing TS2s to<br>leave Configuration doesn’t work, the LTSSM tran‐<br>sitions to Recovery to take appropriate steps. If it<br>still doesn’t work after 256 passes through Recovery<br>(counter reaches FFh), then it goes back to Detect to<br>start over. It may be that some Lanes are not work‐<br>ing.|
|WAKE#|Side‐band pin used to signal to the system that the<br>power should be restored. It’s used instead of the Beacon<br>in systems where power conservation is an important<br>consideration.|



**985** 

**PCI Ex ress Technolo p gy** 

**986** 

## _**Numerics**_ 

128b/130b 43 128b/130b Encoding 973 1x Packet Format 374, 375 3DW Header 152 3-Tap Transmitter Equalization 585 4DW Headers 152 4x Packet Format 374 8.0 GT/s 410 8b/10b 42 8b/10b Decoder 367 8b/10b Encoder 366 8b/10b Encoding 973 

## _**A**_ 

AC Coupling 468 ACK 318 Ack 311 ACK DLLP 75, 312 ACK/NAK DLLP 312 ACK/NAK Latency 328 ACK/NAK Protocol 318, 320, 329, 973 Ack/Nak Protocol 74 ACKD_SEQ Count 323 ACKNAK_Latency_Timer 328, 343 ACPI 711, 973 ACPI Driver 706 ACPI Machine Language 712 ACPI Source Language 712 ACPI spec 705 ACPI tables 712 ACS 973 Active State Power Management 405, 735 Address Routing 158 Address Space 121 Address Translation 958, 959 Advanced Correctable Error Reporting 690 Advanced Correctable Error Status 689 Advanced Correctable Errors 688 Advanced Error Reporting 685 Advanced Source ID Register 697 Advanced Uncorrectable Error Handling 691 Advanced Uncorrectable Error Status 691 Aggregate Bandwidth 408 Alternative Routing-ID Interpretation 909 AML 712 AML token interpreter 712 Arbitration 20, 270 Arbor 117 Architecture Overview 39 ARI 909, 974 ASL 712 ASPM 735, 742, 910, 974 ASPM Exit Latency 756, 757 Assert_INTx messages 806 Async Notice of Slot Status Change 876 

AtomicOp 150 AtomicOps 897, 974 Attention Button 854, 862 Attention Indicator 854, 859 Aux_Current field 726 

## _**B**_ 
