# 📘 第 9 章　DLLP 元素 (Chapter 9. DLLP Elements)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0264.md` ... `chunks/chunk0270.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [DLLP Elements](#-本章目录-table-of-contents)

<a id="sec-9-1"></a>
## 9.1 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-2"></a>
## 9.2 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Gen3 mode of operation, doesn’t use control characters, so data patterns are used to make up the ordered sets that identify if transmitted bytes are associ‐ ated with TLPs / DLLPs or Ordered Sets. A 2‐bit Sync Header is inserted at the beginning of a 128 bit (16 byte) block of data. The Sync Header informs the receiver whether the received block is a Data Block (TLP or DLLP related bytes) or an Ordered Set Block. Since there are no control characters in Gen3 mode, the D/K# bit is not needed. 

**364** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐3: Physical Layer Transmit Details_ 

**==> picture [252 x 355] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Gen3 Scrambler Lane 1, ... ,N-1 Gen3 Scrambler<br>Scrambler Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>8 10 Tx Clk 8 10<br>Mux Mux<br>Gen3 Sync<br>Serializer Bits Generator Serializer<br>Mux Mux<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- End of picture text -----**<br>


Next, the parallel data bytes coming from the upper layers are sent to Byte Striping logic where they are spread out, or striped, onto all the lanes of this link. One byte of the packet is transferred per lane, and all active lanes are used for each packet going out. The Lanes of the Link are all transmitting at the same time, so the bytes must come into this logic fast enough to accommodate that. For example, if there are eight Lanes, eight bytes of parallel from the upper lay‐ ers may arrive at the byte‐striping logic allowing data to be clocked onto all lanes simultaneously. 

**365** 

## **PCI Ex ress Technolo p gy** 

Next is the Scrambler, which XORs a pseudo‐random pattern onto the outgoing data bytes to mix up the bits. Although it would seem that this might introduce problems, it doesn’t because the scrambling pattern is predictable and not truly random, so the receiver can use the same algorithm to easily recover the origi‐ nal data. If the scramblers get out of step then the Receiver won’t be able to make sense of the bit stream so, to guard against that problem, the scrambler is reset periodically (Gen1 and Gen2). That way, if the scramblers do get out of step with each other it won’t be long before they’re both re‐initialized and back in step again. For Gen1 and Gen2 modes that re‐initialization happens when‐ ever the COM character is detected. For Gen3 mode, it happens whenever an EIEOS ordered set is seen. A more sophisticated 24‐bit based scrambler is uti‐ lized in Gen3 mode, hence the alternate path through the Gen3 scrambler, as depicted in Figure 11‐3 on page 365. 

For Gen1 and Gen2 mode, the scrambled 8‐bit characters are then encoded for transmission by the 8b/10b Encoder. Recall that a Character is an 8‐bit un‐ encoded byte, while a Symbol is the 10‐bit encoded output of the 8b/10b logic. There are several advantages to 8b/10b encoding, but it does add overhead. 

For Gen3 a separate path is shown bypassing the encoder. In other words, scrambled bytes of a packet are transmitted without 8b/10b encoding. The Sync Bit Generator adds a 2‐bit Sync Header prior to every 16 byte block of a packet. The added 2‐bit Sync Header identifies the following 16 byte block to be either a data block or an ordered set block. This addition of a 2‐bit Sync Header every 16 bytes (128 bits) is the basis of Gen3’s 128b/130b encoding scheme. 

Finally, the Symbols are serialized into a bit stream and forwarded to the electri‐ cal sub‐block of the Physical Layer and transmitted to the other end of the link. 

## **Receive Logic Overview** 

Figure 11‐4 on page 367 shows the key elements that make up the receiver logic. The process described below is performed for each lane. Starting at the bottom this time, the first thing to mention is the receiver Clock and Data Recovery (CDR). The first step in this process is to recover the clock based on transitions in the incoming bit stream. This recovered clock faithfully reproduces the Trans‐ mitter’s clock that was used to send the data and is used to latch the incoming bits into a deserializing buffer. 

The next steps in the CDR process are to find the Gen1/Gen2 Symbol bound‐ aries and divide the recovered clock by 10 to latch the 10‐bit Symbols into the Elastic Buffer. For Gen3, the next step is to acquire Block Lock and then latch the 8‐bit Symbols associated with each of the 16 bytes in the block into the Elastic Buffer — more on this in the next chapter. 

**366** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

Logic controlling the Elastic Buffer adjusts for minor clock variations between the recovered clock and the local clock of the receiver by adding or removing SKP Symbols as needed when an SOS (SKP Ordered Set) is detected. Finally, the Receiver’s local clock moves each Symbol out of the Elastic Buffer. 

_Figure 11‐4: Physical Layer Receive Logic Details_ 

**==> picture [262 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


Using the 8b/10b Decoder, Gen1/Gen2 Symbols are decoded thus converting the 10‐bit symbols to 8‐bit characters. The descrambler applies the same scrambling method used at the transmitter to recover the original data. Finally, the bytes from each Lane are un‐striped to form a byte stream that will be forwarded up to the Data Link Layer. Only TLPs and DLLPs are loaded into the receive buffer and sent to the Data Link Layer. 

**367** 

**PCI Ex ress Technolo p gy** 

## **Transmit Logic Details (Gen1 and Gen2 Only)** 

The section provides more detail associated with the steps identified in the pre‐ vious section. Refer to the block diagram in Figure 11‐5 on page 369 during this discussion. 

## **Tx Buffer** 

Starting from the top of the diagram once again, the buffer accepts TLPs and DLLPs from the Data Link Layer, along with ‘Control’ information that specifies when a new packet begins. As mentioned, the buffer allows us to stall the flow of characters from time to time in order to insert control characters and ordered sets. A ‘throttle’ signal is also shown going back up to the Data Link Layer to stop the flow of characters if the buffer should become full. 

## **Mux and Control Logic** 

The multiplexer, shown in Figure 11‐6 on page 370, is used to insert special con‐ trol (K) characters into the data flow coming from the buffer. Only the Physical Layer uses K control characters; they are inserted during transmission and removed at the receiver. The four different inputs to the mux are: 

- **Transmit Data Buffer** . When the Data Link Layer supplies a packet, the mux gates the character stream through. All of the characters coming from the buffer are D characters, so the D/K# signal is driven high when Tx Buffer contents are gated. 

- **Start and End characters.** These Control characters are added to the start and end of every TLP and DLLP (see Figure 11‐7 on page 371) and allow a receiver to readily detect the boundaries of a packet. There are two Start characters: STP indicates the start of a TLP, while SDP indicates the start of a DLLP. An indicator from the Data Link Layer, along with the packet type, determines what type of framing character to insert. There are also two end characters, the End Good character (END) for normal transmission, and the End Bad character (EDB) to handle some error cases. Start and End charac‐ ters are K characters, so the D/K# signal is driven low when the Start and End characters are inserted (see Table 11‐1 on page 386 for a list of Control characters). 

**368** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐5: Physical Layer Transmit Logic Details (Gen1 and Gen2 Only)_ 

**==> picture [190 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle N*8<br>Tx<br>Buffer Control/ Ordered<br>Token Logical Sets<br>Characters Idle<br>N*8 8 8 8<br>Mux<br>N*8 D/K#<br>Lane 0 Byte Striping Lane N<br>8 D/K# 8 D/K#<br>Scrambler Lane 1, ... ,N-1 Scrambler<br>8 8<br>D/K# Tx Local D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane 1, ... ,N-1 Lane N<br>**----- End of picture text -----**<br>


- **Ordered Sets** . As mentioned earlier, control characters are only used by the Physical Layer and are not seen by the higher layers. Some communication across the Link is necessary to initiate and maintain Link operation, and that is accomplished by exchanging Ordered Sets. Every ordered set starts with a K character called a comma (COM), and contains other K or D char‐ acters depending on the type of Order Set be delivered. Ordered Sets are always aligned on four byte boundaries and are transmitted during a vari‐ ety of circumstances including: 

   - Error recovery, initiating events (such as Hot Reset), or exit from low‐ power states. In these cases, the Training Sequence 1 and 2 (TS1 and TS2) ordered sets are exchanged across the Link. 

   - At periodic intervals, the mux inserts the SKIP ordered set pattern to facilitate clock tolerance compensation in the receiver. For a detailed description of this process, refer to “Clock Compensation” on page 391. 

**369** 

## **PCI Ex ress Technolo p gy** 

- When a device wants to place its transmitter in the Electrical Idle state, it must inform the remote receiver at the other end of the Link. The mux inserts an **Electrical Idle ordered set** to accomplish this. 

- When a device wants to change the Link power state from L0s low power state to the L0 full‐on power state, it sends a set of **Fast Training Sequence** (FTS) ordered sets to the receiver. The receiver uses this ordered set to re‐synchronize its PLL to the transmitter clock. 

- **Logical Idle Sequence.** When there are no packets ready to transmit and no ordered sets to send, the link is logically idle. In order to keep the receiver PLL locked on to the transmitter’s frequency, it’s important that the transmitter keep sending something, so Logical Idle characters are inserted for that case. Logical Idle is very simple, and consists of nothing more than a string of Data 00h characters. 

_Figure 11‐6: Transmit Logic Multiplexer_ 

**==> picture [380 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
From Data Link Layer<br>Packet Boundary Indicator<br>Throttle<br>N*8<br>Tx<br>Buffer Control/ Ordered<br>CharactersToken LogicalIdle Sets<br>N*8<br>N*8 8 8 8 N*8 Ordered Sets:<br>Mux Tx   TS1,  TS2,<br>Buffer<br>N*8 D/K# STP, SDP   SKIP Logical<br>END, EDB  Electrical Idle Idle<br>Lane 0 Byte Striping Lane N<br>N*8<br>8 D/K# 8 D/K#<br>D K K/D D<br>Scrambler Lane 1, ... ,N-1 Scrambler Mux<br>8 8<br>D/K# Tx Local D/K# N*8 D/K#<br>PLL<br>8b/10b 8b/10b<br>Encoder Encoder<br>10 Tx Clk 10<br>Serializer Serializer<br>Tx Tx<br>Lane 0 Lane N<br>Lane 1, ... ,N-1<br>**----- End of picture text -----**<br>


**370** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐7: TLP and DLLP Packet Framing with Start and End Control Characters_ 

**==> picture [289 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-3"></a>
## 9.3 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

‘D’ Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>‘D’ Character<br>‘K’ Character ‘K’ Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>‘K’ Character ‘K’ Character<br>**----- End of picture text -----**<br>


## **Byte Striping (for Wide Links)** 

The next step shown in our example is Byte Striping, although this is only needed if the port implements more than one Lane (called a wide Link). Strip‐ ing means that each consecutive outbound character in a character stream is routed onto consecutive Lanes. The number of Lanes used is configured during the Link training process based on what is supported by both devices that share the Link. 

Three examples of byte striping are illustrated in the following diagrams. In Figure 11‐8 on page 372, a single‐lane link (x1) is shown. This is not a very inter‐ esting case, since the packet enters the Physical Layer a byte at a time and goes out the same way, but illustrates the way the sequence of characters will be drawn. 

Figure 11‐9 on page 372 shows the incoming Dword packets from the muti‐ plexer. Each byte is directed to the corresponding lanes. Finally, Figure 11‐10 on page 373 illustrates an eight‐lane (x8) link. In this example, two Dwords are required to populate all 8 lanes. This requires the Dword to arrive at twice the rate as the previous example. The format of the data being sent across each lane is described in the sections that follow. 

**371** 

## **PCI Ex ress Technolo p gy** 

_Figure 11‐8: x1 Byte Striping_ 

**==> picture [154 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- End of picture text -----**<br>


_Figure 11‐9: x4 Byte Striping_ 

**==> picture [338 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- End of picture text -----**<br>


**372** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐10: x8 Byte Striping with DWord Parallel Data_ 

**==> picture [368 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- End of picture text -----**<br>


## **Packet Format Rules** 

## **General Rules** 

- The total packet length (including Start and End characters) of each packet is always a multiple of four characters. This is a natural extension of the fact that the data length is measured in dwords. 

- TLPs start with the STP character and finish with either an END or EDB character. 

- DLLPs start with SDP, terminate with the END character. and are exactly 8 characters long (SDP + 6 characters + END) 

- STP and SDP characters are placed on Lane 0 when starting the transmis‐ sion of a packet after the transmission of Logical Idles. In other cases, they may start on a Lane number divisible by 4. 

- The receiver’s Physical Layer is allowed to watch for violation of these rules and may report them as Receiver Errors to the Data Link Layer. 

**373** 

**PCI Ex ress Technolo p gy** 

## **Example: x1 Format** 

The example shown in Figure 11‐11 on page 374 illustrates the format of packets transmitted over a x1 link (a link with only one lane operational). A sequence of packets is shown interspersed with one SKIP Ordered Set. Logical Idles are shown at the end to represent the case when the transmitter has no more pack‐ ets to send and uses idle characters as filler. 

_Figure 11‐11: x1 Packet Format_ 

**==> picture [351 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- End of picture text -----**<br>


## **x4 Format Rules** 

- STP and SDP characters are always sent on Lane 0. 

- END and EDB characters are always sent on Lane 3. 

- When an ordered set such as the SKIP is sent, it must appear on all lanes simultaneously. 

- When Logical Idles are transmitted, they must be sent on all lanes simulta‐ neously. 

- Any violation of these rules may be reported as a Receiver Error to the Data Link Layer. 

**374** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Example x4 Format** 

The example shown in Figure 11‐12 on page 375 illustrates the format of packets sent over a x4 Link (link with four data lanes operational). The illustration shows one TLP followed by a SKIP ordered set transmitted on all Lanes for receiver clock compensation. Next is a DLLP, followed by Logical Idle on all lanes. This example highlights that the packets are always multiples of 4 charac‐ ters because the start character always appears in lane 0 and the end character is always in lane 3. It also illustrates that ordered sets must appear on all the lanes simultaneously. 

_Figure 11‐12: x4 Packet Format_ 

**375** 

**PCI Ex ress Technolo p gy** 

## **Large Link-Width Packet Format Rules** 

The following rules apply when a packet is transmitted over a x8, x12, x16, or x32 Link: 

- STP/SDP characters are always sent on Lane 0 when transmission starts after a period during which Logical Idles are transmitted. After that, they may only be sent on Lane numbers divisible by 4 when sending back‐to‐ back packets (Lane 4, 8, 12, etc.). 

- END/EDB characters are sent on Lane numbers divisible by 4 and then minus one (Lane 3, 7, 11, etc.). 

- If a packet doesn’t end on the last Lane of the Link and there are no more packets ready to go, PAD Symbols are used as filler on the remaining lane numbers. Logical Idle can’t be used for this purpose because it must appear on all Lanes at the same time. 

- Ordered sets must be sent on all lanes simultaneously. 

- Similarly, logical idles must be sent on all lanes when they are used. 

- Any violation of these rules may be reported as a Receiver Error to the Data Link Layer. 

## **x8 Packet Format Example** 

The example shown in Figure 11‐13 on page 377 illustrates the format of packets transmitted over a x8 link. The illustration shows a TLP followed by a SKIP ordered set, a DLLP, and finally a TLP that ends on Lane 3. At that point, the transmitter has no more packets ready to send but the current packet doesn’t extend to include all the available lanes. One might expect the extra lanes to be filled with Logical Idle, but it won’t work here because idles must appear on all lanes at the same time. So another fill character is needed, and the spec writers chose to use the PAD control character here. The only other place that PAD is used is during the training process. Finally, since there are still no more packets to send, Logical Idles are sent on all the lanes. 

**376** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐13: x8 Packet Format_ 

## **Scrambler** 

The next step in our example is scrambling, as shown in Figure 11‐5 on page 369, which is intended to prevent repetitive patterns in the data stream. Repeti‐ tive patterns create “pure tones” on the link, meaning a consistent frequency caused by the pattern that generates more than the usual noise, or EMI. Reduc‐ ing this problem by spreading this energy over a wider frequency range is the primary goal of scrambling. In addition, though, scrambled transmission on one Lane also reduces interference with adjacent Lanes on a wide Link. This “spatial frequency de‐correlation”, or reduction of crosstalk noise, helps the receiver on each lane to distinguish the desired signal. 

**377** 

## **PCI Ex ress Technolo p gy** 

To help the receiver maintain synchronization with the scrambled sequence, control characters do not get scrambled and are thus recognizable even if the scramblers get out of sync. In addition, the arrival of the COM control character (K28.5) reinitializes the scramblers on both ends of the Link each time it arrives and thus re‐synchronizes them. 

## **Scrambler Algorithm** 

The scrambler described in the spec is shown in Figure 11‐14 on page 378. It’s made of a 16‐bit Linear Feedback Shift Register (LFSR) with feedback points that implement the following polynomial: 

G(x) = X[16] + X[5] + X[4] + X[3 ] +1 

_Figure 11‐14: Scrambler_ 

The LFSR is clocked at 8 times the frequency of the clock feeding the data bytes, and its output is clocked into an 8‐bit register that is XORed with the 8‐bit data characters to form the scrambled data output. 

**378** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Some Scrambler implementation rules:** 

- On a multi‐Lane Link implementation, Scramblers associated with each Lane must operate in concert, maintaining the same simultaneous value in each LFSR. 

- Scrambling is applied to ‘D’ characters only, meaning those associated with TLP and DLLPs and the Logical Idle (00h) characters. However, those ‘D’ characters that are within the TS1 and TS2 ordered sets are not scrambled. 

- Scrambling is never applied to ‘K’ characters and characters within ordered sets, such as TS1, TS2, SKIP, FTS and Electrical Idle. These characters bypass the scrambler logic. One reason for this is to ensure they’ll still be recogniz‐ able by the receiver even if the scramblers somehow get out of sequence. 

- Compliance Pattern characters (used for testing) are also not scrambled. 

- • The COM character, a control character that does not get scrambled, is used to reinitialize the LFSR to FFFFh at both the transmitter and receiver. 

- Except for the COM character, the LFSR normally will serially advance eight times for every D or K character sent, but it does not advance on SKP characters associated with the SKIP ordered set. The reason is that a receiver may add or delete SKP Symbols to perform clock tolerance com‐ pensation. Changing the number of characters in the receiver compared to the number that were sent would cause the value in the receiver LFSR to lose synchronization with the transmitter LFSR value if they were not ignored. 

## **Disabling Scrambling** 

Scrambling is enabled by default, but the spec allows it to be disabled for test and debug purposes. That’s because testing may require control of the exact bit pattern sent and, since the hardware handles scrambling, there’s no reasonable way for the software to be able to force a specific pattern. No specific software mechanism is defined by which to instruct the Physical Layer to disable scram‐ bling, so this has to be a design‐specific implementation.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-4"></a>
## 9.4 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

If scrambling is disabled by a device, this gets communicated to the neighbor‐ ing device by sending at least two TS1s and TS2s that have the appropriate bit set in the control field as described in “Configuration State” on page 539. In response, the neighboring device also disables its scrambling. 

**379** 

**PCI Ex ress Technolo p gy** 

## **8b/10b Encoding** 

## **General** 

The first two generations of PCIe use 8b/10b encoding. Each Lane implements an 8b/10b Encoder that translates the 8‐bit characters into 10‐bit Symbols. This coding scheme was patented by IBM in 1984 and is widely used in many serial transports today, such as Gigabit Ethernet and Fibre Channel. 

## **Motivation** 

Encoding accomplishes several desirable goals for serial transmission. Three of the most important are listed here: 

- **Embedding a Clock into the Data.** Encoding ensures that the data stream has enough edges in it to recover a clock at the Receiver, with the result that a distributed clock is not needed. This avoids some limitations of a parallel bus design, such as flight time and clock skew. It also eliminates the need to distribute a high‐frequency clock that would cause other problems like increased EMI and difficult routing. 

   - As an example of this process, Figure 11‐15 on page 381 shows the encoding results of the data byte 00h. As can be seen, this 8‐bit character that had no transitions converts to a 10‐bit Symbol with 5 transitions. The 8b/10b guar‐ antees enough edges to ensure the “run length” (sequence of consecutive ones or zeros) in the bit stream to no more than 5 consecutive bits under any conditions. 

- **Maintaining DC Balance.** PCIe uses an AC‐coupled link, placing a capaci‐ tor serially in the path to isolate the DC part of the signal from the other end of the Link. This allows the Transmitter and Receiver to use different com‐ mon‐mode voltages and makes the electrical design easier for cases where the path between them is long enough that they’re less likely to have exactly the same reference voltages. That DC value, or common‐mode voltage, can change during run time because the line charges up when the signal is driven. Normally, the signal changes so quickly that there isn’t time for this to cause a problem but, if the signal average is predominantly one level or the other, the common‐mode value will appear to drift. Referred to as “DC Wander”, this drifting voltage degrades signal integrity at the Receiver. To compensate, the 8b/10b encoder tracks the “disparity” of the last Symbol that was sent. Disparity, or inequality, simply indicates whether the previ‐ ous Symbol had more ones than zeros (called positive disparity), more zeros than ones (negative disparity), or a balance of ones and zeros (neutral 

**380** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

   - disparity). If the previous Symbol had negative disparity, for example, the next one should balance that by using more ones. 

- **Enhancing Error Detection.** The encoding scheme also facilitates the detec‐ tion of transmission errors. For a 10‐bit value, 1024 codes are possible, but the character to be encoded only has 256 unique codes. To maintain DC bal‐ ance the design uses two codes for each character, and chooses which one based on the disparity of the last Symbol that was sent, so 512 codes would be needed. However, many of the neutral disparity encodings have the same values (D28.5 is one example), so not all 512 are used. As a result, more than half the possible encodings are not used and will be considered illegal if seen at a Receiver. If a transmission error does change the bit pat‐ tern of a Symbol, there’s a good chance the result would be one of these ille‐ gal patterns that can be recognized right away. For more on this see the section titled, “Disparity” on page 383. 

The major disadvantage of 8b/10b encoding is the overhead it requires. The actual transmission performance is degraded by 20% from the Receiver’s point of view because 10 bits are sent for each byte, but only 8 useful bits are recov‐ ered at the receiver. This is a non‐trivial price to pay but is still considered acceptable to gain the advantages mentioned. 

_Figure 11‐15: Example of 8‐bit Character 00h Encoding_ 

**==> picture [224 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
8b Value<br>0 0 0 0 0 0 0 0<br>Data 00h<br>10b Encoded<br>0 11 0 0 0 1 0 1 1<br>Value<br>**----- End of picture text -----**<br>


## **Properties of 10-bit Symbols** 

As described in the literature on 8b/10b coding, the design isn’t strictly 8 bits to 10 bits. Instead, it’s really a 5‐to‐6 bit encoding followed by a 3‐to‐4 bit encoding. The sub‐blocks are internal to the design but their existence helps to explain some of the properties for a legal Symbol, as listed below. A Symbol that doesn’t follow these properties is considered invalid. 

**381** 

**PCI Ex ress Technolo p gy** 

- The bit stream never contains more than five continuous 1s or 0s, even from the end of one Symbol to beginning of the next. 

- Each 10‐bit Symbol contains: 

   - Four 0s and six 1s (not necessarily contiguous), or 

   - Six 0s and four 1s (not necessarily contiguous), or 

   - Five 0s and five 1s (not necessarily contiguous). 

- Each 10‐bit Symbol is subdivided into two sub‐blocks: the first is six bits wide and the second is four bits wide. 

   - The 6‐bit sub‐block contains no more than four 1s or four 0s. 

   - The 4‐bit sub‐block contains no more than three 1s or three 0s. 

## **Character Notation** 

The 8b/10b uses a special notation shorthand, and Figure 11‐16 on page 382 illustrates the steps to arrive at the shorthand for a given character: 

1. Partition the character into its 3‐bit and 5‐bit sub‐blocks. 

2. Transpose the position of the sub‐blocks. 

3. Create the decimal equivalent for each sub‐block. 

4. The character takes the form Dxx.y for Data characters, or Kxx.y for Control characters. In this notation, xx is the decimal equivalent of the 5‐bit field, and y is the decimal equivalent of the 3‐bit field. 

_Figure 11‐16: 8b/10b Nomenclature_ 

**==> picture [348 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
8b Designation Example Data (6Ah)<br>D/<br>8b Character 7 6 5 4 3 2 1 0 D 01101010<br>K#<br>Partition into D/ H G F E D C B A<br>D 011 01010<br>sub-blocks K#<br>Flip sub-blocks K#D/ E D C B A H G F D 01010 011<br>Convert sub-blocks<br>to decimal notation D/K xx . y D 10 . 3<br>Final Notation D/Kxx.y D10.3<br>**----- End of picture text -----**<br>


**382** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Disparity** 

**Definition.** Disparity refers to the inequality between the number of ones and zeros within a 10‐bit Symbol and is used to help maintain DC balance on the link. A Symbol with more zeros is said to have a negative (–) dispar‐ ity, while a Symbol with more ones has a positive (+) disparity. When a Symbol has an equal number of ones and zeros, it’s said to have a neutral disparity. Interestingly, most characters encode into Symbols with + or – dis‐ parity, but some only encode into Symbols with neutral disparity. 

**CRD (Current Running Disparity).** The CRD is the information as to the current state of disparity on the link. Since it’s just a single bit it can only be positive or negative and doesn’t always change when the next Symbol is sent out. To see how it works, remember that the next Symbol decoded can have negative, neutral, or positive disparity, then consider the following example. If the CRD was positive, an outgoing Symbol with a negative dis‐ parity would change it to negative, a neutral disparity would leave it as positive, and a positive disparity would be an error because the CRD is only one bit and can’t be made more positive. 

The initial state of the CRD (before any characters are transmitted) may not match between the sender and receiver but it turns out that it doesn’t mat‐ ter. When the receiver sees the first Symbol after training is complete, it will check for a disparity error and, if one is found, just change the CRD. This won’t be considered an error but simply an adjustment of the CRD to match the receiver and sender. After that, there are only two legal CRD cases: it can remain the same if the new Symbol has neutral disparity, or it can flip to the opposite polarity if the new Symbol has the opposite disparity. What is not legal is for the disparity of the new Symbol to be the same as the CRD. Such an event would be a disparity error and should never occur after the initial adjustment unless an error has occurred. 

## **Encoding Procedure** 

There are different ways that 8b/10b encoding could be accomplished. The sim‐ plest approach is probably to implement a look‐up table that contains all the possible output values. However, this table can require a comparatively large number of gates. Another approach is to implement the decoder as a logic block, and this is usually the preferred choice because it typically results in a smaller and cheaper solution. The specifics of the encoding logic are described in detail in the referenced literature, so we’ll focus here on the bigger picture of how it works instead. 

**383** 

## **PCI Ex ress Technolo p gy** 

An example 8b/10b block diagram is shown in Figure 11‐17 on page 384. A new outgoing Symbol is created based on three things: the incoming character, the D/K# indication for that character, and the CRD. A new CRD value is computed based on the outgoing Symbol and is fed back for use in encoding the next char‐ acter. After encoding, the resulting Symbol is fed to a serializer that clocks out the individual bits. Figure 11‐18 on page 385 shows some sample 8b/10b encod‐ ings that will be useful for the example that follows. 

_Figure 11‐17: 8‐bit to 10‐bit (8b/10b) Encoder_ 

**==> picture [343 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bytes from Scrambler D/K#<br>8b Character 7 6 5 4 3 2 1 0<br>H G F E D C B A<br>8b/10b Encoding Logic<br>Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>Serial Stream<br>Serializer j h g f i e d c b a to Transmitter<br>using Tx Clock<br>**----- End of picture text -----**<br>


**384** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐18: Example 8b/10b Encodings_ 

## **Example Transmission** 

Figure 11‐19 illustrates the encode and transmission of three characters: the first and second are the control character K28.5 and the third character is the data character D10.3. 

In this example the initial CRD is negative so K28.5 encodes into 001111 1010b. This Symbol has positive disparity (more ones than zeros), and causes the CRD polarity to flip to positive. The next K28.5 is encoded into 110000 0101b and has a negative disparity. That causes the CRD this time to flip to negative. Finally, D10.3 is encoded into 010101 1100b. Since its disparity is neutral, the CRD doesn’t change in this case but remains negative for whatever the next character will be. 

**385** 

**PCI Ex ress Technolo p gy** 

_Figure 11‐19: Example 8b/10b Transmission_ 

## **Use these two characters in the example below:** 

|**D/K#**|**Hex**<br>**Byte**|**Binary Bits**<br>**HGF EDCBA**|**Byte**<br>**Name**|**CRD –**<br>**abcdei fghj**|**CRD +**<br>**abcdei fghj**|
|---|---|---|---|---|---|
|**Control(K)**|**BC**|**101 11100**|**K28.5**|**001111 1010**|**110000 0101**|
|**Data(D)**|**6A**|**011 01010**|**D10.3**|**010101 1100**|**010101 0011**|



## **Example Transmission** 

||**CRD**|**Character**|**CRD**|**Character**|**CRD**|**Character**|**CRD**|
|---|---|---|---|---|---|---|---|
|**Character to**<br>**be transmitted**|**-**|**K28.5 (BCh)**|**+**|**K28.5 (BCh)**|**-**|**D10.3 (6Ah)**|**-**|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-5"></a>
## 9.5 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-6"></a>
## 9.6 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- They are only inserted on packet boundaries (nothing is allowed to interrupt a packet) and must go simultaneously on all Lanes. If a packet is already in progress the SKP Ordered Set will have to wait. The maxi‐ mum possible packet size would require more than 4096 Symbol times, though, and during that time several SKIP ordered sets should have 

**391** 

**PCI Ex ress Technolo p gy** 

been sent. This case is handled by accumulating the SKIPs that should have gone out and injecting them all at the next packet boundary. 

- Since this ordered set must be transmitted on all Lanes simultaneously, a multi‐lane link may need to add PAD characters on some Lanes to allow the ordered set to go on all Lanes simultaneously (see Figure 11‐ 13 on page 377). 

- During low‐power link states, any counters used to schedule SKIP ordered sets must be reset. There’s no need for them when the transmit‐ ter isn’t signaling, and it wouldn’t make sense to wake up the link to send them. 

- SKIP ordered sets must not be transmitted while the Compliance Pat‐ tern is in progress. 

_Figure 11‐20: SKIP Ordered Set_ 

**==> picture [128 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
Encoding<br>COM K28.5<br>SKP K28.0<br>SKP K28.0<br>SKP K28.0<br>**----- End of picture text -----**<br>


## **Receive Logic Details (Gen1 and Gen2 Only)** 

Figure 11‐21 shows the receiver logic of the Logical Physical Layer. This section describes packet processing from the time the data is received serially on each lane until the packet byte stream is clocked into the Data Link Layer. 

**392** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐21: Physical Layer Receive Logic Details (Gen1 and Gen2 Only)_ 

**==> picture [283 x 367] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>Control<br>Receive<br>8<br>Rx<br>Buffer<br>8 Control<br>Start/End/Idle/Pad Character Removal and<br>Packet Alignment Check<br>8 D/K#<br>Lane 0 Byte Un-Striping Lane N<br>8 D/K# 8 D/K#<br>De-Scrambler De-Scrambler<br>8 D/K# 8 D/K#<br>Error 8b/10b Error 8b/10b<br>Detect Decoder Detect Decoder<br>Rx Local<br>10 PLL 10<br>Serial-to-Parallel Serial-to-Parallel<br>and Elastic Buffer and Elastic Buffer<br>Rx Clk Rx Clk<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


## **Differential Receiver** 

The first parts of the receiver logic are shown in Figure 11‐22, including the dif‐ ferential input buffer for each lane. The buffer senses peak‐to‐peak voltage dif‐ ferences and determines whether the difference represents a logical one or zero. 

**393** 

**PCI Ex ress Technolo p gy** 

For a detailed discussion of receiver characteristics, see section “Receiver Char‐ acteristics” on page 492. 

_Figure 11‐22: Receiver Logic’s Front End Per Lane_ 

**==> picture [372 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
10-bit Sym bols<br>Symbol<br>Lock<br>Lane<br>Serial-to-Parallel K28.5 Detection Elastic De-skew<br>Converter (Comma Symbol) Buffer Delay<br>10 Circuit 10<br>Differential<br>Input<br>Rx Local<br>Clock Clock<br>Control<br>D+<br>Rx Clock Local<br>Differential<br>Recovery Clock<br>D- Receiver Serial Bit PLL PLL<br>Stream<br>a     b     c     d    e     f     g     h     i      j<br>**----- End of picture text -----**<br>


## **Rx Clock Recovery** 

## **General** 

Next the receiver generates an Rx Clock from the data bit transitions in the input data stream, probably using a PLL. This recovered clock has the same fre‐ quency (2.5 or 5.0 GHz) as that of the Tx Clock that was used to clock the bit stream onto the wire. The Rx Clock is used to clock the inbound bit stream into the deserializer. The deserializer has to be aligned to the 10‐bit Symbol bound‐ ary (a process called achieving Symbol lock), and then its Symbol stream output is clocked into the elastic buffer with a version of the Rx Clock that’s been divided by 10. Even thought both must be accurate to within +/–300ppm of the center frequency, the Rx Clock is probably a little different from the Local Clock and if so, compensation is needed. 

**394** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Achieving Bit Lock** 

Recall that the 8b/10b encoding scheme guarantees the inbound serial Symbol stream will contain frequent transitions. The receiver PLL uses those transitions to create an Rx Clock that is synchronized with the Tx Clock that was used to clock the bit stream out of the transmitter. When the receiver locks on to the Tx Clock frequency, the receiver is said to have achieved **“Bit Lock”** . 

During Link training, the transmitter sends a long series of TS1 and TS2 ordered sets to the receiver, which then uses the bit transitions in them to achieve Bit Lock. There are enough transitions on the Link during normal operation for the receiver to maintain Bit Lock after that. 

## **Losing Bit Lock** 

If the Link is put in a low power state (such as L0s or L1) in which packet trans‐ mission ceases, the receiver will lose synchronization. To avoid having the error circuit see this as an error, the transmitter sends an electrical Idle ordered set (EIOS) before going to the lower power state to tell the receiver to de‐gate its input. 

## **Regaining Bit Lock** 

When the transmitter is ready to wake the Link from the L0s state, it sends a specific number FTS ordered sets (the actual number is design specific) and the receiver uses these to regain bit and Symbol lock. A relatively small number of FTSs are needed to recover and so the recovery latency is short. Because the Link is in the L0s state for a short time, the receiver PLL does not usually drift too far from the Tx Clock before it begins to receive the FTSs. If the Link was instead in the L1 low power state and the transmitter instead starts transmitting TS1OSs. This results in the Link getting re‐trained and wakeup time is longer than L0s wakeup time. Should the Link have a more serious error and the Ack/ Nak mechanism be unsuccessful in error recovery after four attempts of retry‐ ing the TLPs, the Data Link Layer signals the Physical Layer to re‐training the Link. Here again, Bit Lock is re‐established during the re‐training process. 

## **Deserializer** 

## **General** 

The incoming data is clocked into each Lane’s deserializer (serial‐to‐parallel converter) by the Rx clock (see Figure 11‐22 on page 394). The 10‐bit Symbols produced are clocked into the Elastic Buffer using a divided‐by‐10 version of the Rx Clock. 

**395** 

**PCI Ex ress Technolo p gy** 

## **Achieving Symbol Lock** 

When the receive logic starts receiving a bit stream, it is JABOB (just a bunch of bits) with no markers to differentiate Symbols or any boundaries. The receive logic must have a way to find the start and end of a 10‐bit Symbol, and the Comma (COM) Symbol serves this purpose. 

The 10‐bit encoding of the COM Symbol contains two bits of one polarity fol‐ lowed by five bits of the opposite polarity (0011111010b or 1100000101b), mak‐ ing it easily detectable. Recall that the COM Control character, like all other Control characters, is also not scrambled by the transmitter, and that ensures that the desired sequence will be seen at the receiver. Upon detection of the COM, the logic knows that the next bit received will be the first bit of the next 10‐bit Symbol. At that point, the deserializer is said to have achieved **‘Symbol Lock’** . 

The COM Symbol is used to achieve Symbol Lock as follows: 

- During Link training when the Link is first established or when re‐training is needed, and TS1 and TS2 ordered sets are transmitted. 

- When FTS ordered sets are sent to inform the receiver to change the state of the Link from L0s to L0. 

## **Receiver Clock Compensation Logic** 

## **Background** 

We’ve observed before that the clocks used by the transmitter and receiver on either end of a link aren’t required to have exactly the same frequencies. This will be the case whenever the link doesn’t use a common reference clock and introduces the problem that one of them is running slightly faster than the other. The only requirement is that both clocks must be within +/– 300 ppm (parts per million) of the center frequency. Since one could be +300 ppm and the other could be ‐300 ppm in the worst case, the worst separation between them could be 600ppm. That difference translates into a gain or loss of one Symbol clock every 1666 clocks. Once the Link is trained, the receive clock (Rx Clock) in the receiver is the same as the transmit clock (Tx Clock) at the other end of the Link (because the receive clock is derived from the bit stream). 

**396** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Elastic Buffer’s Role** 

To compensate for that worst‐case frequency difference, an elastic buffer (see Figure 11‐22 on page 394) is built into the receive path. Received Symbols are clocked into it using the recovered clock and clocked out using the receiver’s local clock. The Elastic Buffer compensates for the frequency difference by add‐ ing or removing SKP Symbols. When a SKP ordered set arrives, logic watching the status of the elastic buffer makes an evaluation. If the local clock is running faster, Symbols are being clocked out faster than they’re coming in, so the buffer will be approaching an underflow condition. The logic will compensate for this by appending an extra SKP Symbol to the ordered set when it arrives to quickly refill the buffer. On the other hand, if the recovered clock is running faster, the buffer will be approaching an overflow condition and the logic will compensate for that by deleting one of the SKP Symbols to quickly drain the buffer. These actions will make up for difference in rates of arrival and consumption of the Symbols and prevent any confusion or loss of data. 

The transmitter periodically sends the SKIP ordered sets for this purpose. As the name implies, the SKP characters are really disposable characters. Deleting or adding a SKP Symbol prevents a buffer overflow or underflow in the elastic buffer and then they get discarded along with all the other control characters when the Symbols are forwarded to the next layer. Consequently, they use a lit‐ tle bandwidth but don’t otherwise affect the flow of packets at all. 

Although lost Symbols due to an Elastic Buffer overflow or underflow is an error condition, it’s optional for receivers to check for this. If they do, and this situation occurs, a Receiver Error will be indicated to the Data Link Layer. 

The transmitter schedules a SKIP ordered set transmission once every 1180 to 1538 Symbol times. However, if the transmitter starts a maximum sized TLP transmission right at the 1538 Symbol time boundary when a SKIP ordered set is scheduled to be transmitted, the SKIP ordered set transmission is deferred. Receivers must be able to tolerate SKIP ordered sets that have a maximum sepa‐ ration dependent on the maximum packet payload size a device supports. The formula for the maximum number of Symbols ( _n_ ) between SKIP ordered sets is: _n_ = 1538 + (maximum packet payload size + 28) 

The number 28 in the equation is the TLP overhead. It is the largest number of Symbols that would be associated with the header (16 bytes), the optional ECRC (4 bytes), the LCRC (4 bytes), the sequence number (2 bytes) and the framing Symbols STP and END (2 bytes). 

**397** 

**PCI Ex ress Technolo p gy** 

## **Lane-to-Lane Skew** 

## **Flight Time Will Vary Between Lanes** 

For wide links, skew between lanes is an issue that can’t be avoided and which must be compensated at the receiver. Symbols are sent simultaneously on all lanes using the same transmit clock, but they can’t be expected to arrive at the receiver at precisely the same time. Sources of Lane‐to‐Lane skew include: 

- Differences between electrical drivers and receivers

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-9-7"></a>
## 9.7 DLLP Elements | DLLP 元素

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- Printed wiring board impedance variations 

- Trace length mismatches 

When the serial bit streams carrying a packet arrive at the receiver, this Lane‐to‐ Lane skew must be removed to receive the bytes in the correct order. This pro‐ cess is referred to as de‐skewing the link. 

## **Ordered sets Help De-Skewing** 

The unique structure of the ordered sets and the fact that they are sent simulta‐ neously on all the lanes makes them useful for detecting timing misalignment between Lanes. The spec doesn’t define a method for doing this but in Gen1 and Gen2 the receiver logic can simply look for the COM character on each lane. If it doesn’t appear at the same time on all Lanes, then the early arriving COMs are delayed until they all match up on all Lanes. 

## **Receiver Lane-to-Lane De-Skew Capability** 

This could be done by adjusting an analog delay line on the incoming signals. Alternatively, it could be done after the elastic buffer, which has the advantage that the arrival time differences are now digitized to Symbol times by the local clock of the receiver (see Figure 11‐23 on page 399). If the input to one lane makes it on a clock edge and another one doesn’t, the early arrival COMs can simply be delayed by the appropriate number of Symbol clocks to line it up with the late arriving COMs. The fact that the maximum allowable skew at the receiver is a multiple of the clock periods infers that the spec writers probably had an implementation like this in mind (see Table 11‐3 on page 399). 

**398** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐3: Allowable Receiver Signal Skew_ 

|Spec Version|Allowable Rx Skew|
|---|---|
|Gen1|20 ns<br>(5 clocks at 4ns per Symbol)|
|Gen2|8 ns<br>(4 clocks at 2ns per Symbol)|
|Gen3|6 ns<br>(4 clocks at 1.25ns per Symbol)|



In Gen3 mode there aren’t any COM characters to use for de‐skewing, but detecting Ordered Sets can still provide the necessary timing alignment. 

## **De-Skew Opportunities** 

An unambiguous pattern is needed on all lanes at the same time to perform de‐ skewing and any ordered set will do. Link training sends these, but the SKIP ordered set is sent regularly during normal Link operation. Checking its arrival time allows the skew to be checked on an ongoing basis in case it might change based on temperature or voltage. If it does, the Link will need to transition to the Recovery LTSSM state to correct it. If that happens while packets are in flight, however, a receiver error may occur and a packet could be dropped, pos‐ sibly resulting in replayed TLPs. 

_Figure 11‐23: Receiver’s Link De‐Skew Logic_ 

**==> picture [307 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
TS1/TS2 TS1/TS2<br>Lane 0 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 1 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 2 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 3 Rx FTS Delay FTS<br>(symbols)<br>COM COM<br>COM COM<br>COM COM<br>COM COM<br>**----- End of picture text -----**<br>


**399** 

**PCI Ex ress Technolo p gy** 

## **8b/10b Decoder** 

## **General** 

The first two generations of PCIe use 8b/10b, while Gen3 does not. Let’s explore the operation of it first and then consider the difference for Gen3. Refer to Fig‐ ure 11‐24 on page 401. Each receiver Lane incorporates a 10b/8b decoder which is fed from the Elastic Buffer. The decoder is shown with two lookup tables (the D and K tables) to decode the 10‐bit Symbol stream into 8‐bit characters plus the D/K# signal. The state of the D/K# signal indicates that the received Symbol is a Data (D) character if a match for the received Symbol is found in the D table, or a Control (K) character if a match for the received Symbol is discovered in the K table. 

## **Disparity Calculator** 

The decoder sets the disparity value based on the disparity of the first Symbol received. After the first Symbol, once Symbol lock has been achieved and dis‐ parity has been initialized, the calculated disparity for each subsequent Sym‐ bol’s disparity is expected to follow the rules. If it does not, a Receiver Error is reported. 

## **Code Violation and Disparity Error Detection** 

**General.** The error detection logic of the 8b/10b decoder detects illegal Symbols in the received Symbol stream. Some error checking is optional in the receiver, but the spec requires that these errors be checked and reported as a Receiver Error. The two types of errors detected are: 

## **Code Violations.** 

- Any 6‐bit sub‐block containing more than four 1s or four 0s is in error. 

- Any 4‐bit sub‐block containing more than three 1s or three 0s is in error. 

- Any 10‐bit Symbol containing more than six 1s or six 0s is in error. 

- Any 10‐bit Symbol containing more than five consecutive 1s or five con‐ secutive 0s is in error. 

- Any 10‐bit Symbol that doesn’t decode into an 8‐bit character is in error. 

## **Disparity Errors.** 

At the receiver a Symbol cannot have a disparity that doesn’t match what it should be for the CRD. If it does, a disparity error is detected. Some dispar‐ ity errors may not be detectable until the subsequent Symbol is processed 

**400** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

(see Figure 11‐25 on page 401). For example, if two bits in a Symbol flip in error, the error may not be visible and the Symbol may decode into a valid 8‐bit character. Such an error won’t be detected in the Physical Layer. 

_Figure 11‐24: 8b/10b Decoder per Lane_ 

**==> picture [373 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bytes to De-Scrambler D/K#<br>D/<br>7 6 5 4 3 2 1 0<br>K#<br>8b Character H G F E D C B A<br>To Error Reporting<br>8b/10b Look-Up Table For D Characters<br>8b/10b Look-Up Table For K Characters Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>10b Symbol<br>From Elastic Buffer<br>**----- End of picture text -----**<br>


_Figure 11‐25: Example of Delayed Disparity Error Detection_ 

||**CRD**|**Character**|**Character**|**CRD**|**Character**|**CRD**|**Character**|**CRD**|
|---|---|---|---|---|---|---|---|---|
|**Transmitted**<br>**Character Stream**|**-**|**D21.1**||**-**|**D10.2**|**-**|**D23.5**|**+**|
|**Transmitted Bit**<br>**Stream**|**-**|**101010 1001**||**-**|**010101 0101**|**-**|**111010 1010**|**+**|
|**Bit Stream After**<br>**Error**|**-**|**101010 101**<br>**1**||**+**|**010101 0101**|**+**|**111010 1010**|**+**|
|**Decoded**<br>**Character Stream**|**-**|**D21.0**||**+**|**D10.2**|**+**|**Invalid**|**+**|
|Error occurs here<br>Error detected here|||||||||



**401** 

**PCI Ex ress Technolo p gy** 

## **Descrambler** 

The descrambler is fed by the 8b/10b decoder. It only descrambles Data (D) characters associated with a TLP or DLLP (D/K# is high). It doesn’t descramble Control (K) characters or ordered sets because they’re not scrambled at the transmitter. 

## **Some Descrambler Implementation Rules:** 

- On a multi‐Lane Link, descramblers associated with each Lane must oper‐ ate in concert, maintaining the same simultaneous value in each LFSR. 

- Descrambling is applied to ‘D’ characters associated with TLP and DLLPs including the Logical Idle (00h) sequence. ‘D’ characters within ordered set are not descrambled. 

- ‘K’ characters and ordered set characters bypass the descrambler logic. 

- Compliance Pattern characters are not descrambled. 

- When a COM character enters the descrambler, it reinitializes the LFSR value to FFFFh. 

- With one exception, the LFSR serially advances eight times for every char‐ acter (D or K character) received. The LFSR does NOT advance on SKP characters associated with the SKIP ordered sets received. The reason the LFSR is not advanced on detecting SKPs is because there may be a differ‐ ence between the number of SKP characters transmitted and the SKP char‐ acters exiting the Elastic Buffer (as discussed in “Receiver Clock Compensation Logic” on page 396). 

## **Disabling Descrambling** 

By default, descrambling is always enabled, but the spec allows it to be disabled for test and debug purposes although no standard software method is given for disabling it. If the descrambler receives at least two TS1/TS2 ordered sets with the “disable scrambling” bit set on all of its configured Lanes, it disables the descrambler. 

## **Byte Un-Striping** 

Figure 11‐26 on page 403 shows eight character streams from the descramblers of a x8 Link being un‐striped into a single byte stream which is fed to the char‐ acter filter logic. 

**402** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐26: Example of x8 Byte Un‐Striping_ 

**==> picture [354 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Multiplexer block<br>Data Stream D/K#<br>Character 0<br>Character 1<br>Character 2<br>Character 3<br>Character 4<br>Character 5<br>Character 6<br>Character 7<br>Byte Un-Striping<br>Character 0 Character 1 Character 7<br>Character 8 Character 9 Character 15<br>Character 16 Character 17 Character 23<br>From Lane 0 From Lane 1 From Lane 7<br>De-Scrambler De-Scrambler De-Scrambler<br>**----- End of picture text -----**<br>


## **Filter and Packet Alignment Check** 

The serial byte stream supplied by the byte un‐striping logic contains TLPs, DLLPs, Logical Idle sequences, Control characters such as STP, SDP, END, EDB, and PADs, as well as the ordered sets. Of these, the Logical Idle sequence, the control characters and ordered sets are detected and eliminated before they get to the next layer. What remains are the TLPs and DLLPs and these are sent to the Rx Buffer along with an indicator of the start and end of each packet. 

## **Receive Buffer (Rx Buffer)** 

The Rx Buffer holds received TLPs and DLLPs after the start and end characters have been eliminated. The received packets are ready to send to the Data Link Layer. The interface to the Data Link Layer is not described in the spec, so the designer is free to decide details like data bus width. As an example, we can 

**403** 

**PCI Ex ress Technolo p gy** 

assume an interface clock of 250MHz and a Gen1 speed on the Link. For that case, the number of bytes in the data bus between these layers would be the same as the number of Lanes supported. 

## **Physical Layer Error Handling** 

## **General** 

Physical Layer errors are reported as Receiver Errors to the Data Link Layer. According to the spec, some errors must be checked and trigger a receiver error, while others are optional. 

Required error checking: 

- 8b/10b decode errors: disparity error, illegal Symbol 

Optional error checking: 

- Loss of Symbol lock (see “Achieving Symbol Lock” on page 396) 

- Elastic Buffer overflow or underflow 

- Lane deskew errors (see “Lane‐to‐Lane Skew” on page 398) 

- Packets inconsistent with format rules 

## **Response of Data Link Layer to Receiver Error** 

If the Physical Layer indicates a Receiver Error to the Data Link Layer, the Data Link Layer discards the TLP currently being received and frees any storage allo‐ cated for the TLP. It then schedules a NAK to go back to the transmitter of the TLP. That causes the transmitter to replay TLPs from the Replay Buffer, which should automatically correct the error. The Data Link Layer may also direct the Physical Layer to initiate Link re‐training. 

If the PCI Express Extended Advanced Error Capabilities register set is imple‐ mented, a Receiver Error sets the Receiver Error Status bit in the Correctable Error Status register. If enabled, the device can send an ERR_COR (correctable error) message to the Root Complex. 

**404** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Active State Power Management**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
