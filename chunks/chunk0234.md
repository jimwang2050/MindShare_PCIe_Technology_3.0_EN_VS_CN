As illustrated in Figure 4‐12 on page 146, a PCI Express topology consists of independent, point‐to‐point links connecting each device with one or more neighbors. As traffic arrives at the inbound side of a link interface (called the _ingress port_ ), the port checks for errors, then makes one of three decisions: 

1. Accept the traffic and use it internally 

2. Forward the traffic to the appropriate outbound ( _egress_ ) port 

3. Reject the traffic because it is neither the intended target, nor an interface to it (Note that there are other reasons why traffic may be rejected) 

**146** 

**Chapter 4: Address Space & Transaction Routing** 

## **Receivers Check For Three Types of Traffic** 

Assuming a link is fully operational, the receiver interface of each device (ingress port) must detect and evaluated the arrival of the three types of link traffic: Ordered Sets, Data Link Layer Packets (DLLPs), and Transaction Layer Packets (TLPs). Ordered Sets and DLLPs are local to a link and thus are never routed to another link. TLPs can and do move from link to link, based on rout‐ ing information contained in the packet headers. 

## **Routing Elements** 

Devices with multiple ports, like Root Complexes and Switches, can forward TLPs between the ports and are sometimes called Routing Agents or Routing Elements. They accept TLPs that target internal resources and forward TLPs between ingress and egress ports. 

Interestingly, peer‐to‐peer routing support is required in Switches, but for a Root Complex it’s optional. Peer‐to‐peer traffic is typically where one Endpoint sends packets that target another Endpoint. 

Endpoints have only one Link and never expect to see ingress traffic other than what is targeting them. They simply accept or reject incoming TLPs. 

## **Three Methods of TLP Routing** 

## **General** 

TLPs can be routed based on address (either memory or IO), based on ID (meaning Bus, Device, Function number), or routed implicitly. The routing method used is based on the TLP type. Table 4‐7 on page 147 summarizes the TLP types and the routing methods used for each. 

_Table 4‐7: PCI Express TLP Types And Routing Methods_ 

|**TLP Type**|**Routing Method Used**|
|---|---|
|Memory Read [Lock], Memory Write, AtomicOp|Address Routing|
|IO Read and Write|Address Routing|



**147** 

**PCI Express Technology** 

_Table 4‐7: PCI Express TLP Types And Routing Methods (Continued)_ 

|**TLP Type**|**Routing Method Used**|
|---|---|
|Configuration Read and Write|ID Routing|
|Message, Message With Data|Address Routing, ID Rout‐<br>ing, or Implicit routing|
|Completion, Completion With Data|ID Routing|



Messages are the only TLP type that support more than one routing method. Most of the message TLPs defined in the PCI Express spec use implicit routing, however, the vendor‐defined messages could use address routing or ID routing if desired. 

## **Purpose of Implicit Routing and Messages** 

In implicit routing, neither address or ID routing information applies; instead, the packet is routed based on a code in the packet header indicating a destina‐ tion with a known location in the topology, such as the Root Complex. This sim‐ plifies routing of messages in the cases where a type of implicit routing applies. 

**Why Messages?** Message transactions were not defined in PCI or PCI‐X, but were introduced with PCIe. The main reason for adding Messages as a packet type was to pursue the PCIe design goal to drastically reduce the number of sideband signals implemented in PCI (e.g. interrupt pins, error pins, power management signals, etc.). Consequently, most of the sideband signals were replaced with in‐band packets in the form of Message TLPs. 

**How Implicit Routing Helps** Using in‐band messages in place of side‐ band signals requires a means of routing them to the proper recipient in a topology consisting of numerous point‐to‐point links. Implicit routing takes advantage of the fact that Switches and other routing elements understand the concept of upstream and downstream, and that the Root Complex is found at the top of the topology while Endpoints are found at the bottom. As a result, a Message can use a simple code to show that it should go to the Root Complex, for example, or to be sent to all devices downstream. This ability eliminates the need to define address ranges or ID lists specifically used as the target of different message transactions. 

The different types of implicit routing can be found in “Implicit Routing” on page 163. 

**148** 

**Chapter 4: Address Space & Transaction Routing** 

## **Split Transaction Protocol** 

Like most other serial technologies, PCI Express uses the split transaction proto‐ col which allows a target device to receive one or more requests and then respond to each request with a separate completion. This is a significant improvement over the PCI bus protocol that used wait‐states or delayed trans‐ actions (retries) to deal with latencies in accessing targets. Instead of testing to see when the target becomes ready to do a long‐latency transfer, the target ini‐ tiates the response whenever it’s ready. This results in at least two separate TLPs per transaction ‐ the Request and the Completion (as will be discussed later, a single read request may result in multiple completion TLPs being sent back). Figure 4‐13 on page 149 illustrates the Request‐Completion components of a split transaction. This example shows software reading data from an Endpoint. 

_Figure 4‐13: PCI Express Transaction Request And Completion TLPs_ 

**==> picture [304 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex System<br>IN OUT Memory<br>1) Request TLP (Memory Read)<br>K27.7 K29.7<br>OUT IN STP SEQ HDR LCRC END<br>END byte<br>Link CRC (4 bytes)<br>TLP Header (3DW or 4DW)<br>Switch<br>TLP Sequence Number (2 bytes)<br>Receiver decode of STP symbol indicates<br>start of a TLP<br>2) Completion w/Data TLP<br>K27.7 K29.7<br>OUT IN STP SEQ HDR Data LCRC END<br>PCIe<br>Endpoint<br>IN OUT<br>OUT IN<br>**----- End of picture text -----**<br>


**149** 

**PCI Express Technology** 

## **Posted versus Non-Posted** 

To mitigate the penalty of the Request‐Completion latency, memory write trans‐ actions are posted, meaning the transaction is considered completed from the Requester’s perspective as soon as the request leaves the Requester. If helpful, you can associate the term “posting” with the postal system, where posting a memory write is analogous to posting a letter in the mail. Once you’ve placed a letter in the postal box you put your faith in the system to deliver it and don’t wait for verification of delivery. This approach can be much faster than waiting for the entire Request‐Completion transit, but — as in all posting schemes — uncertainty exists concerning when (and if) the transaction completed success‐ fully at the ultimate recipient. 

In PCIe, the small amount of uncertainty involved by making all memory writes posted is considered acceptable in exchange for the performance gained. By contrast, writes to IO and configuration space almost always affect device behavior and have a timeliness associated with them. Consequently, it is impor‐ tant to know when (and if) those write requests completed. Because of this, IO writes and configuration writes are always non‐posted and a completion will always be returned to report the status of the operation. 

In summary, non‐posted transactions require a completion. Posted transactions do not require, and should never receive, a completion. Table 4‐8 on page 150 lists which PCIe transactions are posted and non‐posted. 

_Table 4‐8: Posted and Non‐Posted Transactions_ 

|**Request**|**How Request Is Handled**|
|---|---|
|Memory Write|All**memory write requests are posted**. No completions are<br>expected or sent.|
|Memory Read<br>Memory Read Lock|All**memory read requests are non‐posted**. A completion<br>with data (made of one or more TLPs) will be returned by the<br>Completer to deliver both the requested data and the status<br>of the memory read. In the event of an error, a completion<br>without data will be returned reporting the status.|
|AtomicOp|All**AtomicOp requests are non‐posted**. A completion with<br>data will be returned by the Completer containing the origi‐<br>nal value of the target location.|



**150** 

**Chapter 4: Address Space & Transaction Routing** 

_Table 4‐8: Posted and Non‐Posted Transactions (Continued)_ 

|**Request**|**How Request Is Handled**|
|---|---|
|IO Read<br>IO Write|All**IO requests are non‐posted**. A completion without data<br>will be returned for writes or failed reads, and a completion<br>with data will be returned for successful reads.|
|Configuration Read<br>Configuration Write|All**configuration requests are non‐posted**. A completion<br>without data will be returned for writes and failed reads,<br>while a completion with data will be returned for successful<br>reads.|
|Message|All**messages are posted**. The routing method depends on<br>the Message type, but they’re all considered posted requests.|



## **Header Fields Define Packet Format and Type** 

## **General** 

As shown in Figure 4‐14 on page 152, each TLP contains a three or four double‐ word (12 or 16 byte) header. This includes _Format_ and _Type_ fields that define the content of the rest of the header and indicate the routing method to be used for the TLP as it traverses the topology. 

**151** 

**PCI Express Technology** 

_Figure 4‐14: Transaction Layer Packet Generic 3DW And 4DW Headers_ 

**==> picture [256 x 344] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (END)<br>Generic 3DW (12-byte) Header<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Generic 4DW (16-byte) Header<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Byte 4 Bytes 4-7 Vary with  Type  Field<br>Byte 8 Bytes 8-11 Vary with  Type  Field<br>Byte 12 Bytes 12-15 Vary with  Type  Field<br>**----- End of picture text -----**<br>


**152** 

**Chapter 4: Address Space & Transaction Routing** 

## **Header Format/Type Field Encodings** 

Table 4‐9 on page 153 below summarizes the encodings used in TLP header For‐ mat and Type fields. 

_Table 4‐9: TLP Header Format and Type Field Encodings_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Memory Read Request (MRd)|000 = 3DW, no data<br>001 = 4DW, no data|0 0000|
|Memory Read Lock Request (MRdLk)|000 = 3DW, no data<br>001 = 4DW, no data|0 0001|
|Memory Write Request (MWr)|010 = 3DW, w/<br>data<br>011 = 4DW, w/<br>data|0 0000|
|IO Read Request (IORd)|000 = 3DW, no data|00010|
|IO Write Request (IOWr)|010 = 3DW, w/<br>data|0 0010|
|Config Type 0 Read Request (CfgRd0)|000 = 3DW, no data|0 0100|
|Config Type 0 Write Request<br>(CfgWr0)|010 = 3DW, w/<br>data|0 0100|
|Config Type 1 Read Request (CfgRd1)|000 = 3DW, no data|0 0101|
|Config Type 1 Write Request<br>(CfgWr1)|010 = 3DW, w/<br>data|0 0101|
|Message Request (Msg)|001 = 4DW, no data|1 0RRR* (for RRR,<br>see routing subfield<br>in “Message Type<br>Field Summary” on<br>page 164)|
|Message Request w/Data (MsgD)|011 = 4DW, w/<br>data|1 0RRR* (for RRR,<br>see routing subfield<br>in “Message Type<br>Field Summary” on<br>page 164)|



**153** 

**PCI Express Technology** 

_Table 4‐9: TLP Header Format and Type Field Encodings (Continued)_ 

|**TLP**|**FMT[2:0]**|**TYPE [4:0]**|
|---|---|---|
|Completion (Cpl)|000 = 3DW, no data|0 1010|
|Completion W/Data (CplD)|010 = 3DW, w/<br>data|0 1010|
|Completion‐Locked (CplLk)|000 = 3DW, no data|0 1011|