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