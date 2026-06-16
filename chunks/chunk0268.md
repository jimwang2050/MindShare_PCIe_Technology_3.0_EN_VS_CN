|**Bit stream**<br>**transmitted**||**Yields**<br>**001111 1010**<br>**CRD is +**||**Yields**<br>**110000 0101**<br>**CRD is -**||**Yields**<br>**010101 1100**<br>**CRD is neutral**||
|Initialized value of CRD is don’t care. Receiver can determine from incoming bit stream||||||||



## **Control Characters** 

The 8b/10b encoding provides several special characters for Link management and Table 11‐1 on page 386 shows their encoding. 

_Table 11‐1: Control Character Encoding and Definition_ 

|**8b/10b**<br>**Name**|**Description**|
|---|---|
|K28.5|First character in any ordered set. Also used by Rx<br>to achieve Symbol lock during training.|
|K23.7|Packet filler|
|K28.0|Used in SKIP ordered set for Clock Tolerance Com‐<br>pensation|



**386** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐1: Control Character Encoding and Definition (Continued)_ 

|**Character**<br>**Name**|**8b/10b**<br>**Name**|**Description**|
|---|---|---|
|STP|K27.7|Start of a TLP|
|SDP|K28.2|Start of a DLLP|
|END|K29.7|End of Good Packet|
|EDB|K30.7|End of a bad or ‘nullified’ TLP.|
|FTS|K28.1|Used to exit from L0s low power state to L0|
|IDL|K28.3|Used to place Link into Electrical Idle state|
|EIE|K28.7|Part of the Electrical Idle Exit Ordered Set sent<br>prior to bringing the Link back to full power for<br>speeds higher than 2.5 GT/s|



- **COM** (Comma): One of the main functions of this is to be the first Symbol in the physical layer communications called ordered sets (see “Ordered sets” on page 388). It has an interesting property that makes both of its Symbol encodings easily recognizable at the receiver: they start with two bits of one polarity followed by five bits of the opposite polarity (001111 1010 or 110000 0101). This property is especially helpful for initial training, when the receiver is trying to make sense of the string of bits coming in, because it helps the receiver lock onto the incoming Symbol stream. See “Link Training and Initialization” on page 405 for more on how this works. 

- • **PAD** : On a multi‐Lane Link, if a packet to be sent doesn’t cover all the avail‐ able lanes and there are no more packets ready to send, the PAD character is used to fill in the remaining Lanes. 

- **SKP** (Skip): This is used as part of the SKIP ordered set that is sent periodi‐ cally to facilitate clock tolerance compensation. 

- **STP** (Start TLP): Inserted to identify the start of a TLP. 

- **SDP** (Start DLLP): Inserted to identify the start of a DLLP. 

- **END** : Appended to identify the end of an error‐free TLP or DLLP. 

- **EDB** (EnD Bad): Inserted to identify the end of a TLP that a forwarding device (such as a switch) wishes to ‘nullify’. This case can arise when a switch using the “cut‐through mode” forwards a packet from an ingress port to an egress port without buffering the whole packet first. Any error detected during the forwarding process creates a problem because a portion of the packet is already being delivered before the packet can be checked for 

**387** 

**PCI Ex ress Technolo p gy** 

errors. To handle this case, the switch must cancel the one that’s already in route to the destination. This is accomplished by nullifying it: ending the packet with EDB and inverting the LCRC from what it should have been. When a receiver sees a nullified packet, it discards the packet and does not return an ACK or NAK. (See the “Example of Cut‐Through Operation” on page 356.) 

- **FTS** (Fast Training Sequence): Part of the FTS ordered set sent by a device to recover a link from the L0s standby state back to the full‐on L0 state. 

- **IDL** (Idle): Part of the Electrical Idle ordered set sent to inform the receiver that the Link is transitioning into a low power state. 

- **EIE** (Electrical Idle Exit): Added in the PCIe 2.0 spec and used to help an electrically‐idle link begin the wake up process. 

## **Ordered sets** 

**General.** Ordered Sets are used for communication between the Physical Layers of Link partners and may be thought of as Lane management pack‐ ets. By definition they are a series of characters that are not TLPs or DLLPs. For Gen1 and Gen2 they always begin with the COM character. Ordered Sets are replicated on all Lanes at the same time, because each Lane is tech‐ nically an independent serial path. This also allows Receivers to verify alignment and de‐skewing. Ordered Sets are used for things like Link train‐ ing, clock tolerance compensation, and changing Link power states. 

**TS1 and TS2 Ordered Set (TS1OS/TS2OS).** Training sequences one and two are used for Link initialization and training. They allow the Link partners to achieve bit lock and Symbol lock, negotiate the link speed, and report other variables associated with Link operation. They are described in more detail in the section titled “TS1 and TS2 Ordered Sets” on page 510. 

**Electrical Idle Ordered Set (EIOS).** A Transmitter that wishes to go to a lower‐power link state sends this before ceasing transmission. Upon receipt, Receivers know to prepare for the low power state. The EIOS con‐ sists of four Symbols: the COM Symbol followed by three IDL Symbols. Receivers detect this Ordered Set and prepare for the Link to go to into Elec‐ trical Idle by ignoring input errors until exiting from Electrical Idle. Shortly after sending EIOS, the Transmitter reduces its differential voltage to less than 20mV peak. 

**FTS Ordered Set (FTSOS).** A Transmitter sends the proper number of these (the minimum number was given by the Link neighbor during train‐ ing) to take a Link from the low‐power L0s state back to the fully‐opera‐ tional L0 state. The receiver detects the FTSs, recognizes that the Link is 

**388** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

exiting from Electrical Idle, and uses them to recover Bit and Symbol Lock.The FTS Ordered Set consists of four Symbols: the COM Symbol fol‐ lowed by three FTS Symbols. 

**SKP Ordered Set (SOS).** This consists of four Symbols: the COM Symbol followed by three SKP Symbols. It’s transmitted at regular intervals and is used for Clock Tolerance Compensation as described in “Clock Compensa‐ tion” on page 391 and “Receiver Clock Compensation Logic” on page 396. Basically, the Receiver evaluates the SOS and internally adds or removes SKP Symbols as needed to prevent its elastic buffer from under‐flowing or over‐flowing. 

**Electrical Idle Exit Ordered Set (EIEOS).** Added in the PCIe 2.0 spec, this Ordered Set was defined to provide a lower‐frequency sequence required to exit the electrical idle Link state. The EIEOS for 8b/10b encod‐ ing, uses repeated K28.7 control characters to appear as a repeating string of 5 ones followed by 5 zeros. This low frequency string produces a low‐fre‐ quency signal that allows for higher signal voltages that are more readily detected at the receiver. In fact, the spec states that this pattern guarantees that the Receiver will properly detect an exit from Electrical Idle, something that scrambled data cannot do. For details on electrical idle exit, refer to the section “Electrical Idle” on page 736. 

## **Serializer** 

The 8b/10b encoder on each lane feeds a serializer that clocks the Symbols out in bit order (see Figure 11‐17 on page 384), with the least significant bit (a) shifted out first and the most significant bit (j) shifted out last. For each lane, the Sym‐ bols will be supplied to the serializer at either 250MHz or 500MHz to support a serial bit rate 10 times faster than that at 2.5 GHz or 5.0 GHz. 

## **Differential Driver** 

The differential driver that actually sends the bit stream onto the wire uses NRZ encoding. NRZ simply means that there are no special or intermediate voltage levels used. Differential signalling improves signal integrity and allows for both higher frequencies and lower voltages. Details regarding the electrical charac‐ teristics of the driver are discussed in the section “Transmitter Voltages” on page 462. 

**389** 

**PCI Ex ress Technolo p gy** 

## **Transmit Clock (Tx Clock)** 

The serialized output on each Lane is clocked out by the Tx Clock signal. As mentioned earlier, the clock frequency must be accurate to +/–300ppm around the center frequency (600ppm total variation). There are two options regarding the source of this clock. It can be generated internally or derived from an exter‐ nal reference that may optionally be available. The PCIe spec for peripheral cards includes the definition of a 100MHz reference clock supplied by the sys‐ tem board for this purpose. This reference clock is multiplied internally to derive the local clock that drives the internal logic and the Tx clock used by the serializer. 

## **Miscellaneous Transmit Topics** 

## **Logical Idle** 

In order to keep the receiver’s PLL from drifting, something must be transmit‐ ted during periods when there are no TLPs, DLLPs or ordered sets to transmit, and it is logical idle characters that are injected into the character flow during these times. Some properties of the logical idle character: 

- It’s an 8‐bit Data character with a value of 00h. 

- When sent, it goes on all Lanes at the same time and the Link is said to be in the logical idle state (not to be confused with electrical Idle—the state when the output driver stops transmitting altogether and the receiver PLL loses synchronization). 

- The logical idle character is scrambled, but a receiver can distinguish it from other data because it occurs outside of a packet framing context (i.e.: after an END or EDB, but before an STP or SDP). 

- It is 8b/10b encoded. 

- During logical idle transmission, SKIP ordered sets are still sent periodi‐ cally. 

## **Tx Signal Skew** 

Understandably, the transmitter should introduce a minimal skew between lanes to leave as much Rx skew budget as possible for routing and other varia‐ tions. The spec lists the Tx skew values as 500ps + 2 UI for Gen1, 500ps + 4UI for Gen2, and 500ps + 6 UI for Gen3. Recalling that UI (unit interval) represents one bit time on the Link, this works out as shown in Table 11‐2 below. 

**390** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐2: Allowable Transmitter Signal Skew_ 

|**Spec Version**|**Allowable Tx Skew**|
|---|---|
|Gen1|1300 ps|
|Gen2|1300 ps|
|Gen3|1250 ps|



## **Clock Compensation** 

**Background.** High‐speed serial transports like PCIe have a particular clock problem to solve. The receiver recovers a clock from the incoming bit stream and uses that to latch in the data bits, but this recovered clock is not synchronized with the receiver’s internal clock and at some point it has to begin clocking the data with its own internal clock. Even if they have an optional common external reference clock, the best they can do is to gener‐ ate an internal clock within a specified tolerance of the desired frequency. Consequently, one of the clocks will almost always have a slightly higher frequency than the other. If the transmitter clock is faster, the packets will be arriving faster than they can be taken in. To compensate, the transmitter must inject some “throw‐away characters” in the bit stream that the receiver can discard if it proves necessary to avoid a buffer over‐run condition. For PCIe, these characters which can be deleted take the form of the SKIP ordered set, which consists of a COM character followed by three SKP char‐ acters (see Figure 11‐20). For more detail on this topic, refer to “Receiver Clock Compensation Logic” on page 396). 

**SKIP ordered set Insertion Rules.** A transmitter is required to send SKIP ordered sets on a periodic basis, and the following rules apply: 

- The SKIP ordered set must be scheduled for insertion between 1180 and 1538 Symbol times (a Symbol time is the time required to send one Symbol and is 10 bit times, so at 2.5 GT/s, a Symbol time is 4ns and at 5.0 GT/s, it’s 2ns). 
