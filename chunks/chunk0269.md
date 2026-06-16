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
