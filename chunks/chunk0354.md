- While locked, a legacy Endpoint must not issue any Requests using Traffic Classes which map to the default Virtual Channel (VC0). Note that this requirement applies to all possible sources of Requests within the Endpoint, in the case where there is more than one possible source of Requests. Requests may be issued using TCs which map to VCs other than VC0. 

## **Rules Related To PCI Express Endpoints** 

Native PCI Express Endpoints do not support lock. A PCI Express Endpoint must treat a MRdLk Request as an Unsupported Request. 

**972** 

## _**Glossary**_ 

|**Term**|**Definition**|
|---|---|
|128b/130b Encoding|This isn’t encoding in the same sense as 8b/10b. Instead,<br>the transmitter sends information in Blocks that consist<br>of 16 raw bytes in a row, preceded by a 2‐bit Sync field<br>that indicates whether the Block is to be considered as a<br>Data Block or an Ordered Set Block. This scheme was<br>introduced with Gen3, primarily to allow the Link band‐<br>width to double without doubling the clock rate. It pro‐<br>vides better bandwidth utilization but sacrifices some<br>benefits that 8b/10b provided for receivers.|
|8b/10b Encoding|Encoding scheme developed many years ago that’s used<br>in many serial transports today. It was designed to help<br>receivers recover the clock and data from the incoming<br>signal, but it also reduces available bandwidth at the<br>receiver by 20%. This scheme is used with the earlier<br>versions of PCIe: Gen1 and Gen2.|
|ACK/NAK Protocol|The Acknowledge/Negative Acknowledge mechanism<br>by which the Data Link Layer reports whether TLPs<br>have experienced any errors during transmission. If so, a<br>NAK is returned to the sender to request a replay of the<br>failed TLPs. If not, an ACK is returned to indicate that<br>one or more TLPs have arrived safely.|
|ACPI|Advanced Configuration and Power Interface. Specifies<br>the various system and device power states.|
|ACS|Access Control Services.|



**973** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|ARI|Alternative Routing‐ID Interpretation; optional feature<br>that allows Endpoints to have more Functions that the 8<br>allowed normally.|
|ASPM|Active State Power Management: When enabled, this<br>allows hardware to make changes to the Link power<br>state from L0 to L0s or L1 or both.|
|AtomicOps|Atomic Operations; three new Requests added with the<br>2.1 spec revision. These carry out multiple operations<br>that are guaranteed to take place without interruption<br>within the target device.|
|Bandwidth Management|Hardware‐initiated changes to Link speed or width for<br>the purpose of power conservation or reliability.|
|BAR|Base Address Register. Used by Functions to indicate the<br>type and size of their local memory and IO space.|
|Beacon|Low‐frequency in‐band signal used by Devices whose<br>main power has been shut off to signal that an event has<br>occurred for which they need to have the power<br>restored. This can be sent across the Link when the Link<br>is in the L2 state.|
|BER|Bit Error Rate or Ratio; a measure of signal integrity<br>based on the number of transmission bit errors seen<br>within a time period|
|Bit Lock|The process of acquiring the transmitter’s precise clock<br>frequency at the receiver. This is done in the CDR logic<br>and is one of the first steps in Link Training.|
|Block|The 130‐bit unit sent by a Gen3 transmitter, made up of a<br>2‐bit Sync Field followed by a group of 16 bytes.|



**974** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Block Lock|Finding the Block boundaries at the Receiver when<br>using 128b/130b encoding so as to recognize incoming<br>Blocks. The process involves three phases. First, search<br>the incoming stream for an EIEOS (Electrical Idle Exit<br>Ordered Set) and adjust the internal Block boundary to<br>match it. Next, search for the SDS (Start Data Stream)<br>Ordered Set. After that, the receiver is locked into the<br>Block boundary.|
|Bridge|A Function that acts as the interface between two buses.<br>Switches and the Root Complex will implement bridges<br>on their Ports to enable packet routing, and a bridge can<br>also be made to connect between different protocols,<br>such as between PCIe and PCI.|
|Byte Striping|Spreading the output byte stream across all available<br>Lanes. All available Lanes are used whenever sending<br>bytes.|
|CC|Credits Consumed: Number of credits already used by<br>the transmitter when calculating Flow Control.|
|CDR|Clock and Data Recovery logic used to recover the<br>Transmitter clock from the incoming bit stream and then<br>sample the bits to recognize patterns. For 8b/10b, that<br>pattern, found in the COM, FTS, and EIEOS symbols,<br>allows the logic to acquire Symbol Lock. For 128b/130b<br>the EIEOS sequence is used to acquire Block Lock by<br>going through the three phases of locking.|
|Character|Term used to describe the 8‐bit values to be communi‐<br>cated between Link neighbors. For Gen1 and Gen2, these<br>are a mix of ordinary data bytes (labeled as D characters)<br>and special control values (labeled as K characters). For<br>Gen3 there are no control characters because 8b/10b<br>encoding is no longer used. In that case, the characters<br>all appear as data bytes.|



**975** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|CL|Credit Limit: Flow Control credits seen as available from<br>the transmitter’s perspective. Checked to verify whether<br>enough credits are available to send a TLP.|
|Control Character|These are special characters (labeled as “K” characters)<br>used in 8b/10b encoding that facilitate Link training and<br>Ordered Sets. They are not used in Gen3, where there is<br>no distinction between characters.|
|Correctable Errors|Errors that are corrected automatically by hardware and<br>don’t require software attention.|
|CR|Credits Required ‐ this is the sum of CC and PTLP.|
|CRC|Cyclic Redundancy Code; added to TLPs and DLLPs to<br>allow verifying error‐free transmission. The name means<br>that the patterns are cyclic in nature and are redundant<br>(they don’t add any extra information). The codes don’t<br>contain enough information to permit automatic error<br>correction, but provide robust error detection.|
|Cut‐Through Mode|Mechanism by which a Switch allows a TLP to pass<br>through, forwarded from an ingress Port to an egress<br>Port without storing it first to check for errors. This<br>involves a risk, since the TLP may be found to have<br>errors after part of it has already been forwarded to the<br>egress Port. In that case, the end of the packet is modi‐<br>fied in the Data Link Layer to have an LCRC value that is<br>inverted from what it should be, and also modified at<br>the Physical Layer to have an End Bad (EDB) framing<br>symbol for 8b/10b encoding or an EDB token for 128b/<br>130b encoding. The combination tells the receiver that<br>the packet has been nullified and should be discarded<br>without sending an ACK/NAK response.|
|Data Characters|Characters (labeled as “D” characters) that represent<br>ordinary data and are distinguished from control char‐<br>acters in 8b/10b. For Gen3, there is no distinction<br>between characters.|



**976** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Data Stream|The flow of data Blocks for Gen3 operation. The stream<br>is entered by an SDS (Start of Data Stream Ordered Set)<br>and exited with an EDS (End of Data Stream token).<br>During a Data Stream, only data Blocks or the SOS are<br>expected. When any other Ordered Sets are needed, the<br>Data Stream must be exited and only re‐entered when<br>more data Blocks are ready to send. Starting a Data<br>Stream is equivalent to entering the L0 Link state, since<br>Ordered Sets are only sent while in other LTSSM states,<br>like Recovery.|
|De‐emphasis|The process of reducing the transmitter voltage for<br>repeated bits in a stream. This has the effect of de‐<br>emphasizing the low‐frequency components of the sig‐<br>nal that are known to cause trouble in a transmission<br>medium and thus improves the signal integrity at the<br>receiver.|
|Digest|Another name for the ECRC (End‐to‐End CRC) value<br>that can optionally be appended to a TLP when it’s cre‐<br>ated in the Transaction Layer.|
|DLCMSM|Data Link Control and Management State Machine;<br>manages the Link Layer training process (which is pri‐<br>marily Flow Control initialization).|
|DLLP|Data Link Layer Packet. These are created in the Data<br>Link Layer and are forwarded to the Physical Layer but<br>are not seen by the Transaction Layer.|
|DPA|Dynamic Power Allocation; a new set of configuration<br>registers with the 2.1 spec revision that defines 32 power<br>substates under the D0 device power state, making it<br>easier for software to control device power options.|
|DSP (Downstream Port)|Port that faces downstream, like a Root Port or a Switch<br>Downstream Port. This distinction is meaningful in the<br>LTSSM because the Ports have assigned roles during<br>some states.|



**977** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|ECRC|End‐to‐End CRC value, optionally appended to a TLP<br>when it’s created in the Transaction Layer. This enables a<br>receiver to verify reliable packet transport from source to<br>destination, regardless of how many Links were crossed<br>to get there.|
|Egress Port|Port that has outgoing traffic.|
|Elastic Buffer|Part of the CDR logic, this buffer enables the receiver to<br>compensate for the difference between the transmitter<br>and receiver clocks.|
|EMI|Electro‐Magnetic Interference: the emitted electrical<br>noise from a system. For PCIe, both SSC and scrambling<br>are used to attack it.|
|Endpoint|PCIe Function that is at the bottom of the PCI Inverted‐<br>Tree structure.|
|Enumeration|The process of system discovery in which software reads<br>all of the expected configuration locations to learn which<br>PCI‐configurable Functions are visible and thus present<br>in the system.|
|Equalization|The process of adjusting Tx and Rx values to compen‐<br>sate for actual or expected signal distortion through the<br>transmission media. For Gen1 and Gen2, this takes the<br>form of Tx De‐emphasis. For Gen3, an active evaluation<br>process is introduced to test the signaling environment<br>and adjust the Tx settings accordingly, and optional Rx<br>equalization is mentioned.|
|Flow Control|Mechanism by which transmitters avoid the risk of hav‐<br>ing packets rejected at a receiver due to lack of buffer<br>space. The receiver sends periodic updates about avail‐<br>able buffer space and the transmitter verifies that<br>enough is available before attempting to send a packet.|
|FLR|Function‐Level Reset|



**978** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Framing Symbols|The “start” and “end” control characters used in 8b/10b<br>encoding that indicate the boundaries of a TLP or DLLP.|
|Gen1|Generation 1, meaning designs created to be compliant<br>with the 1.x version of the PCIe spec.|
|Gen1, Gen2, Gen3|Abbreviations for the revisions of the PCIe spec. Gen1 =<br>rev 1.x, Gen2 = rev 2.x, and Gen3 = rev 3.0|
|Gen2|Generation 2, meaning designs created to be compliant<br>with the 2.x version of the PCIe spec.|
|Gen3|Generation 3, meaning designs created to be compliant<br>with the 3.x version of the PCIe spec.|
|IDO|ID‐based Ordering; when enabled, this allows TLPs<br>from different Requesters to be forwarded out of order<br>with respect to each other. The goal is to improve latency<br>and performance.|
|Implicit Routing|TLPs whose routing is understood without reference to<br>an address or ID. Only Message requests have the option<br>to use this type of routing.|
|Ingress Port|Port that has incoming traffic.|
|ISI|Inter‐Symbol Interference; the effect on one bit time that<br>is caused by the recent bits that preceded it.|