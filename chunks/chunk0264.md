Now that we’ve described how the protocol works, this is a good time to explain an exception to its general operation. PCIe supports a Switch feature, called ‘cut‐through mode’, that can be used to improve the transfer latency for large TLPs through a Switch. 

**354** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Background** 

Consider an example where a large TLP needs to pass through a Switch as shown in Figure 10‐16 on page 357. Since the Ingress Switch Port can’t tell whether there was an error in the packet until it has seen the whole TLP, it’ll normally store the entire packet and check it for errors before forwarding it to the Egress Port. This store‐and‐forward method works but, for large packets, the latency to get through the Switch can be large which may be an issue for some applications. It would be nice to minimize this latency if possible. 

## **A Latency Improvement Option** 

Since the first part of the TLP contains the header with the routing information for the packet, one option would be to assume that the packet is a good packet and start evaluating the routing info in header even before the entire packet is received. This would allow a Switch to begin forwarding the TLP to the Egress Port as soon as that routing is evaluated. The Egress Port could then go ahead and start sending it out onto its Link, as long as doing so will not cause an underflow condition within the Switch. (A potential underflow case could eas‐ ily happen if the Ingress Port is x1 and the Egress Port is x16. The Egress Port would be sending the packet out much faster than it is being received.) 

Of course, the Ingress Port can’t check for errors in the packet until it receives the LCRC at the end of the packet, so there is a small risk involved that the TLP being forwarded out may actually contain an error. Eventually, the end of the TLP arrives at the Ingress Port and the packet can be checked. If it turns out there was an error, the Ingress Port takes the normal behavior to a bad TLP and simply sends a Nak to have the packet replayed. However, we now have to deal with the problem that most of a packet that we now know is bad has already been forwarded on to the Egress Port. What are our options at this point? We could finish forwarding the packet and wait for a Nak from the neighboring receiver when it sees the error, but the packet in the replay buffer would be the bad one, and so a replay there won’t fix the problem. We might truncate the bad packet in flight, but the spec doesn’t allow for that possibility. To make this work, we need another option, and that’s where the Cut‐Through option comes into play. 

**355** 

**PCI Ex ress Technolo p gy** 

## **Cut-Through Operation** 

Cut‐though mode provides the solution to the forwarding problem described in the previous section: if an error is seen in the incoming packet, the packet that is already on its way out must be ‘ **nullified** ’. 

A **nullified** packet is terminated with an EDB (end bad) symbol instead of an END (end good) symbol and, to make the condition very clear, the TLPs 32‐bit LCRC is inverted (1’s complement) from the original calculated value. In essence, a nullified packet is handled as though it had never existed. On the Switch Egress Port, that means the replay buffer discards the packet and the NEXT_TRANSMIT_SEQ counter is decremented by one (rolled back). 

When a device receives a TLP that it recognizes as being a nullified TLP, it sim‐ ply drops the packet and treats it as if it never existed. The NEXT_RCV_SEQ is not incremented, the AckNak_LATENCY_TIMER is not started, nor is the NAK_SCHEDULED set. The receiving device silently discards the nullified TLP and does not return an Ack/Nak for it. 

## **Example of Cut-Through Operation** 

Figure 10‐16 on page 357 illustrates a TLP coming in from the left, going through the Switch, and ending up at an Endpoint on the right. A TLP error occurs on the left Link. The steps are as follows: 

1. An incoming TLP is seen at the Switch Ingress Port. It has become cor‐ rupted in flight but that isn’t known yet. 

2. The TLP header arrives, is decoded, and the packet is forwarded to the des‐ tination Egress Port in cut‐through operation. 

3. Eventually, the end of the packet arrives and the Switch Ingress Port is able to complete the LCRC error check. It finds a CRC error and returns a Nak to the TLP source. 

4. At the Egress Port, the Switch replaces the END framing symbol at the end of the bad TLP with EDB and inverts the calculated LCRC value. The TLP is now ‘nullified’ and the Switch discards it from the Replay Buffer. 

5. The nullified packet arrives at the Endpoint. The Endpoint detects the EDB symbol and inverted LCRC and silently discards the packet. It does not return a Nak. 

Now let’s say the TLP source device replays the packet and no error occurs. As before, the TLP is forwarded to the Egress Port with very short latency. When 

**356** 

**Cha ter 10: Ack/Nak Protocol p** 

the rest of the TLP arrives at the Switch, there is no error, so an Ack is returned to the TLP source which then purges this TLP from its Replay Buffer. This time the Switch Egress Port keeps a copy of the TLP in its Replay Buffer. When the TLP reaches the destination, the packet has no errors and the Endpoint returns an Ack. Based on that, the Switch purges the copy of the TLP from its Replay Buffer and the sequence is complete. 

_Figure 10‐16: Switch Cut‐Through Mode Showing Error Handling_ 

**==> picture [378 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error occurs<br>1) 2) 4)<br>END TLP STP END TLP STP EDB TLP STP<br>EDB TLP STP<br>Switch Endpoint<br>5) Discard Packet<br>NAK 6) No ACK or NAK<br>3)<br>**----- End of picture text -----**<br>


**357** 

**PCI Ex ress Technolo p gy** 

**358** 

## Part Four: 

# Physical Layer 

## _**11 Physical Layer ‐ Logical (Gen1 and Gen2)**_ 

## **The Previous Chapter** 

The previous chapter describes the Ack/Nak Protocol: an automatic, hardware‐ based mechanism for ensuring reliable transport of TLPs across the Link. Ack DLLPs confirm good reception of TLPs while Nak DLLPs indicate a transmis‐ sion error. The chapter describes the normal rules of operation as well as error recovery mechanisms. 

## **This Chapter** 

This chapter describes the Logical sub‐block of the Physical Layer. This pre‐ pares packets for serial transmission and recovery. Several steps are needed to accomplish this and they are described in detail. This chapter covers the logic associated with the Gen1 and Gen2 protocol that use 8b/10b encoding. The logic for Gen3 does not use 8b/10b encoding and is described separately in the chap‐ ter called “Physical Layer ‐ Logical (Gen3)” on page 407. 

## **The Next Chapter** 

The next chapter describes the Physical Layer characteristics for the third gener‐ ation (Gen3) of PCIe. The major change includes the ability to double the band‐ width relative to Gen2 without needing to double the frequency by eliminating the need for 8b/10b encoding. More robust signal compensation is necessary at Gen3 speed. Making these changes is more complex than might be expected. 

**361** 

**PCI Ex ress Technolo p gy** 

## **Physical Layer Overview** 

This Physical Layer Overview introduces the relationships between the Gen1, Gen2 and Gen3 implementations. Thereafter the focus is the logical Physical Layer implementation associated with Gen1 and Gen2. The logical Physical Layer implementation for Gen3 is described in the next chapter. 

The Physical Layer resides at the bottom of the interface between the external physical link and Data Link Layer. It converts outbound packets from the Data Link Layer into a serialized bit stream that is clocked onto all Lanes of the Link. This layer also recovers the bit stream from all Lanes of the Link at the receiver. The receive logic de‐serializes the bits back into a Symbol stream, re‐assembles the packets, and forwards TLPs and DLLPs up to the Data Link Layer. 

_Figure 11‐1: PCIe Port Layers_ 

**==> picture [307 x 307] intentionally omitted <==**

**----- Start of picture text -----**<br>
Software layer sends and receives address and transaction information<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Transaction layer<br>Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers Buffers<br>Management<br>per VC per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC Ack/Nak CRC Ack/Nak CRC Sequence TLP LCRC<br>Data Link layer TLP Retry De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**----- End of picture text -----**<br>


**362** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

The contents of the layers are conceptual and don’t define precise logic blocks, but to the extent that designers do partition them to match the spec their imple‐ mentations can benefit because of the constantly increasing data rates affect the Physical Layer more than the others. Partitioning a design by layered responsi‐ bilities allows the Physical Layer to be adapted to the higher clock rates while changing as little as possible in the other layers. 

The 3.0 revision of the PCIe spec does not use specific terms to distinguish the different transmission rates defined by the versions of the spec. With that in mind, the following terms are defined and used in this book. 

- **Gen1** ‐ the first generation of PCIe (rev 1.x) operating at 2.5 GT/s 

- **Gen2** ‐ the second generation (rev 2.x) operating at 5.0 GT/s 

- **Gen3** ‐ the third generation (rev 3.x) operating at 8.0 GT/s 

The Physical Layer is made up of two sub‐blocks: the Logical part and the Elec‐ trical part as shown in Figure 11‐2. Both contain independent transmit and receive logic, allowing dual‐simplex communication. 

_Figure 11‐2: Logical and Electrical Sub‐Blocks of the Physical Layer_ 

**==> picture [366 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Physical Layer Physical Layer<br>Tx Rx Tx Rx<br>Logical Logical<br>Tx Rx Tx Rx<br>Electrical Electrical<br>Link<br>Tx+ Tx- Rx+ Rx- CTX Tx- Tx+ Rx- Rx+<br>CTX<br>**----- End of picture text -----**<br>


**363** 

**PCI Ex ress Technolo p gy** 

## **Observation** 

The spec describes the functionality of the Physical Layer but is purposefully vague regarding implementation details. Evidently, the spec writers were reluc‐ tant to give details or example implementations because they wanted to leave room for individual vendors to add value with clever or creative versions of the logic. For our discussion though, an example is indispensable, and one was cho‐ sen that illustrates the concepts. It’s important to make clear that this example has not been tested or validated, nor should a designer feel compelled to imple‐ ment a Physical Layer in such a manner. 

## **Transmit Logic Overview** 

For simplicity, let’s begin with a high‐level overview of the transmit side of this layer, shown in Figure 11‐3 on page 365. Starting at the top, we can see that packet bytes entering from the Data Link layer first go into a buffer. It makes sense to have a buffer here because there will be times when the packet flow from the Data Link Layer must be delayed to allow Ordered Set packets and other items to be injected into the flow of bytes. 

For Gen1 and Gen2 operation, these injected items are control and data charac‐ ters used to mark packet boundaries and create ordered sets. To differentiate between these two types of characters, a D/K# bit (Data or “Kontrol”) is added. The logic can see what value D/K# should take on based on the source of the character. 
