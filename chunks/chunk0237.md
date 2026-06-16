Information moves between PCI Express devices in packets. The three major classes of packets are _Transaction Layer Packets_ (TLPs), _Data Link Layer Packets_ (DLLPs) and _Ordered Sets_ . This chapter describes the use, format, and definition of the variety of TLPs and the details of their related fields. DLLPs are described separately in Chapter 9, entitled ʺDLLP Elements,ʺ on page 307. 

## **The Next Chapter** 

The next chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Transaction Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like disconnects, retries, and wait‐states. 

## **Introduction to Packet-Based Protocol** 

## **General** 

Unlike parallel buses, serial transport buses like PCIe use no control signals to identify what’s happening on the Link at a given time. Instead, the bit stream they send must have an expected size and a recognizable format to make it pos‐ 

**169** 

**PCI Ex ress Technolo p gy** 

sible for the receiver to understand the content. In addition, PCIe does not use any immediate handshake for the packet while it is being transmitted. 

With the exception of the Logical Idle symbols and Physical Layer packets called _Ordered Sets_ , information moves across an active PCIe Link in fundamen‐ tal chunks called packets that are comprised of symbols. The two major classes of packets exchanged are the high‐level _Transaction Layer Packets_ (TLPs), and low‐level Link maintenance packets called _Data Link Layer Packets_ (DLLPs). The packets and their flow are illustrated in Figure 5‐1 on page 170. Ordered Sets are packets too, however, they are not framed with a start and end symbol like TLPs and DLLPs are. They are also not byte striped like TLPs and DLLPs are. Ordered Set packets are instead replicated on all Lanes of a Link. 

_Figure 5‐1: TLP And DLLP Packets_ 

**==> picture [350 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>DLLP TLP<br>DLLP TLP (Link)<br>Transaction Layer Packet (TLP)<br>STP Seq Num HDR Data Digest CRC End TLP Types:<br>- Memory Read / Write<br>- IO Read / Write<br>- Configuration Read / Write<br>- Completion<br>- Message<br>Data Link Layer Packet (DLLP)<br>- AtomicOp<br>Framing C Framing DLLP Types:<br>DLLP R - TLP Ack/Nak<br>(SDP) C (END)<br>- Power Management<br>- Link Flow Control<br>- Vendor-Specific<br>**----- End of picture text -----**<br>


**170** 

**Chapter 5: TLP Elements** 

## **Motivation for a Packet-Based Protocol** 

There are three distinct advantages to using a packet‐based protocol especially when it comes to data integrity: 

## **1. Packet Formats Are Well Defined** 

Earlier buses like PCI allow transfers of indeterminate size, making identifica‐ tion of payload boundaries impossible until the end of the transfer. In addition, either device is able to terminate the transfer before it completes, making it diffi‐ cult for the sender to calculate and send a checksum or CRC covering an entire payload. Instead, PCI uses a simple parity scheme and checks it on each data phase. 

By comparison, PCIe packets have a known size and format. The packet _header_ at the beginning indicates the packet type and contains the required and optional fields. The size of the header fields is fixed except for the address, which can be 32 bits or 64 bits in size. Once a transfer commences, the recipient can’t pause or terminate it early. This structured format allows including infor‐ mation in the TLPs to aid in reliable delivery, including framing symbols, CRC, and a packet Sequence Number. 

## **2. Framing Symbols Define Packet Boundaries** 

When using 8b/10b encoding in Gen1 and Gen2 mode of operation, each TLP and DLLP packet sent is framed by Start and End control symbols, clearly defining the packet boundaries for the receiver. This is a big improvement over PCI and PCI‐X, where the assertion and de‐assertion of the single FRAME# sig‐ nal indicates the beginning and end of a transaction. A glitch on that signal (or any of the other control signals) could cause a target to misconstrue bus events. A PCIe receiver must properly decode a complete 10‐bit symbol before conclud‐ ing Link activity is beginning or ending, so unexpected or unrecognized sym‐ bols are more easily recognized and handled as errors. 

For the 128b/130b encoding used in Gen3, control characters are no longer employed and there are no framing symbols as such. For more on the differ‐ ences between Gen3 encoding and the earlier versions, see Chapter 12, entitled ʺPhysical Layer ‐ Logical (Gen3),ʺ on page 407. 

**171** 

**PCI Ex ress Technolo p gy** 

## **3. CRC Protects Entire Packet** 

Unlike the side‐band parity signals used by PCI during the address and data phases of a transaction, the in‐band CRC value of PCIe verifies error‐free deliv‐ ery of the entire packet. TLP packets also have a Sequence Number appended to them by the transmitter’s Data Link Layer so that if an error is detected at the Receiver, the problem packet can be automatically resent. The transmitter main‐ tains a copy of each TLP sent in a _Retry Buffer_ until it has been acknowledged by the receiver. This TLP acknowledgement mechanism, called the _Ack/Nak Proto‐ col_ , (and described in Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317) forms the basis of Link‐level TLP error detection and correction. This Ack/Nak Protocol error recovery mechanism allows for a timely resolution of the prob‐ lem at the place or Link where the problem occurred, but requires a local hard‐ ware solution to support it. 

## **Transaction Layer Packet (TLP) Details** 

In PCI Express, high‐level transactions originate in the device core of the trans‐ mitting device and terminate at the core of the receiving device. The Transaction Layer acts on these requests to assemble outbound TLPs in the Transmitter and interpret them at the Receiver. Along the way, the Data Link Layer and Physical Layer of each device also contribute to the final packet assembly. 

## **TLP Assembly And Disassembly** 

The general flow of TLP assembly at the transmit side of a Link and disassem‐ bly at the receiver is shown in Figure 5‐2 on page 173. Let’s now walk through the steps from creation of a packet to its delivery to the core logic of the receiver. The key stages in Transaction Layer Packet assembly and disassembly are listed below. The list numbers correspond to the numbers in Figure 5‐2 on page 173. 

## **Transmitter:** 

1. The core logic of Device A sends a request to its PCIe interface. How this is accomplished is outside the scope of the spec or this book. The request includes: 

   - Target address or ID (routing information) 

   - Source information such as Requester ID and Tag 

   - Transaction type/packet type (Command to perform, such as a memory read.) 

   - Data payload size (if any) along with data payload (if any) 

   - Traffic Class (to assign packet priority) 

   - Attributes of the Request (No Snoop, Relaxed Ordering, etc.) 

**172** 

**Chapter 5: TLP Elements** 

2. Based on that request, the Transaction Layer builds the TLP header, appends any data payload, and optionally calculates and appends the digest (End‐to‐End CRC, ECRC) if that’s supported and has been enabled. At this point the TLP is placed into a Virtual Channel buffer. The Virtual Channel manages the sequence of TLPs according to the Transaction Order‐ ing rules and also verifies that the receiver has enough flow control credits to accept a TLP before it can be passed down to the Data Link Layer. 

3. When it arrives at the Data Link Layer, the TLP is assigned a Sequence Number and then a Link CRC is calculated based on the contents of the TLP and that Sequence Number. A copy of the resulting packet is saved in the Retry Buffer in case of transmission errors while it is also passed on to the Physical Layer. 

_Figure 5‐2: PCIe TLP Assembly/Disassembly_ 

**==> picture [370 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) Outbound From Transmitter Core: Device A Device B (8) Inbound To Receiver Core:<br>Requests to write/read data, Data R/W Requests,<br>Completions, Messages, etc. Device Device Completions, Messages, etc.<br>Core Core<br>(2) Transaction Transaction (7)<br>HDR Data Digest  Layer  Layer HDR Data Digest<br>(3) (3) Data Data (6) (6)<br>Seq Num HDR Data Digest CRC Link Layer Link Layer Seq Num HDR Data Digest CRC<br>STP(4) Seq Num HDR Data Digest CRC End(4) PhysicalLayer PhysicalLayer STP(5) Seq Num HDR Data Digest CRC End(5)<br>(RX) (TX) (RX) (TX)<br>**----- End of picture text -----**<br>


4. The Physical Layer does several things to prepare the packet for serial transmission, including byte striping, scrambling, encoding, and serializing the bits. For Gen1 and Gen2 devices, when using 8b/10b encoding, the con‐ trol characters STP and END are added to either end of the packet. Finally, the packet is transmitted across the Link. In Gen3 mode, STP token is added to the front end of a TLP, but END is not added to the end of the packet. Rather the STP token contains information about TLP packet size. 

## **Receiver:** 

5. At the Receiver (Device B in this example), everything done to prepare the packet for transmission must now be undone. The Physical Layer de‐serial‐ izes the bit stream, decodes the resulting symbols, and un‐stripes the bytes. 

**173** 

**PCI Ex ress Technolo p gy** 

   - The control characters are removed here because they only have meaning at the Physical Layer, and then the packet is forwarded to the Data Link Layer. 

6. The Data Link Layer calculates the CRC and compares it to the received CRC. If that matches, the Sequence Number is checked. If there are no errors, the CRC and Sequence Number are removed and the TLP is passed to the Transaction Layer of the receiver and notifies the sender of good reception by returning an Ack DLLP. In the event of an error a Nak will be returned instead, and the transmitter will re‐replay TLPs in its Retry Buffer. 

7. At the Transaction Layer, the TLP is decoded and the information is passed to the core logic for appropriate action. If the receiving device is the final target of this packet, it checks for ECRC errors and reports any related ECRC error condition to the core logic should there be any. 

## **TLP Structure** 

The basic usage of each field in a Transaction Layer Packet is defined in Table 5‐ 1 on page 174. 

_Table 5‐1: TLP Header Type Field Defines Transaction Variant_ 

|**TLP**<br>**Component**|**Protocol**<br>**Layer**|**Component Use**|
|---|---|---|
|Header|Transaction<br>Layer|3 or 4DW (12 or 16 bytes) in size. Format varies with<br>type, but Header defines parameters, including:<br>•<br>Transaction type<br>•<br>Target address, ID, etc.<br>•<br>Transfer size (if any), Byte Enables<br>•<br>Attributes<br>•<br>Traffic Class|
|Data|Transaction<br>Layer|Optional 1‐1024 DW Payload, which is qualified<br>with Byte Enables or byte‐aligned start and end<br>addresses. Note that a length of zero can’t be speci‐<br>fied, but a zero‐length read (useful in some cases)<br>can be approximated by specifying a length of 1 DW<br>and Byte Enables of all zero. The resulting data from<br>the Completer will be undefined but the Requester<br>doesn’t use it, so the result is the same.|
|Digest/ECRC|Transaction<br>Layer|Optional. When present, ECRC is always 1 DW in<br>size.|



**174** 

**Chapter 5: TLP Elements** 

## **Generic TLP Header Format** 

## **General** 
