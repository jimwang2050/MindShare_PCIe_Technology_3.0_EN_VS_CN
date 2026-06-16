|VRX‐DIFF‐<br>PP‐CC|175<br>(min)<br>1200<br>(max)|120 (min)<br>1200<br>(max)|Indirectly<br>specified|mV|Peak‐to‐peak differential voltage<br>sensitivity of common‐clocked<br>Receiver.|
|VRX‐DIFF‐<br>PP‐DC|175<br>(min)<br>1200<br>(max)|100 (min)<br>1200<br>(max)|Indirectly<br>specified|mV|Peak‐to‐peak differential voltage<br>sensitivity of data‐clocked<br>Receiver.|
|VRX‐IDLE‐<br>DET‐DIFFp‐<br>p|65 (min) 175 (max)|||mV|Electrical Idle detect threshold<br>at the Receiver pins.|
|ZRX‐DIFF‐<br>DC|80<br>(min)<br>120<br>(max)|Covered by<br>RLRX‐DIFF|||At higher frequencies imped‐<br>ance can no longer be repre‐<br>sented by a lumped‐sum value<br>and must be described in more<br>detail.|
|ZRX‐‐DC|40<br>(min)<br>60<br>(max)|40 (min)<br>60 (max)|Bounded<br>by<br>RLRX‐CM||DC impedance needed for<br>Receiver Detect.|



**498** 

**Chapter 13: Physical Layer - Electrical** 

_Table 13‐5: Common Receiver Characteristics (Continued)_ 

|**Item**|**2.5 GT/**<br>**s.**|**5.0 GT/s.**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|LRX‐SKEW|20|8|6|ns|Max Lane‐to‐Lane skew that a<br>Receiver must be able to correct.|
|RLRX‐‐DIFF|10<br>(min)|10 (min)<br>for 0.05 ‐<br>1.25 GHz,<br>8 (min)<br>for >1.25 ‐<br>2.5 GHz|10 (min)<br>for 0.05 ‐<br>1.25 GHz,<br>8 (min)<br>for >1.25 ‐<br>2.5 GHz,<br>5 (min)<br>for >2.5 ‐<br>4.0 GHz|dB|Rx package + Si differential<br>return loss|
|RLRX‐‐CM|6 (min)|6 (min)|6 (min)<br>for 0.05 ‐<br>2.5 GHz,<br>5 (min)<br>for >2.5 ‐ 4<br>GHz|dB|Common mode Rx return loss|



_Figure 13‐34: 2.5 GT/s Receiver Eye Diagram_ 

**==> picture [305 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
V = 88 mV<br>VRX-CM-DC= 0 V RX-DIFFp-MIN<br>TRX-EYE-MIN = 0.4 UI<br>**----- End of picture text -----**<br>


**499** 

**PCI Ex ress Technolo p gy** 

## **Link Power Management States** 

Figure 13‐35 on page 500 through Figure 13‐39 on page 504 illustrate the electri‐ cal state of the Physical Layer while the link is in various power management states and describe several characteristics. One of these is the Tx and Rx termi‐ nations, which are sometimes implemented as active logic 

_Figure 13‐35: L0 Full‐On Link State_ 

**==> picture [375 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>ON direction ON<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM High or Low  VRX-CM = 0 V Low impedance ON<br>impedance termination termination<br>ON<br> Transmission and reception in progress<br> Recommended Power Budget about 80 mW per Lane<br> One direction of the Link can be in L0 while the other<br>side is in L0s<br> Transmitter and Receiver clock PLL are ON<br> Transmitter is On, Receiver is ON<br> Low impedance termination at transmitter<br>No Spec<br>**----- End of picture text -----**<br>


**500** 

**Chapter 13: Physical Layer - Electrical** 

## _Figure 13‐36: L0s Low Power Link State_ 

**==> picture [368 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect Held at 0 - 3.6 V DC common mode voltage<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>ON direction ON<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM High or Low impedance termination VRX-CM = 0 V Low impedancetermination ON<br>ON<br> Transmitter holds Electrical Idle voltage (VTX-DIFFp < 20 mV) and DC common<br>mode voltage ( VTX-CM-DC 0 – 3.6 V)<br>No Spec<br>**----- End of picture text -----**<br>


- Recommended Power Budget <= 20 mW per Lane 

- Recommended exit latency < 50 ns, however designers indicate that a more realistic number appears to be 1 us-2 us 

- One direction of the Link can be in L0s while the other is in L0 

- Transmitter and Receiver clock PLL are ON but Rx Clock loses sync 

- Transmitter is On, Receiver is ON  High or Low impedance termination at transmitter 

**501** 

## **PCI Ex ress Technolo p gy** 

## _Figure 13‐37: L1 Low Power Link State_ 

**==> picture [380 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect Held at 0 - 3.6 V DC common mode voltage<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>ON direction ON<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM High or Low impedance termination VRX-CM = 0 V Lterminationow impedance May be OFF<br>May be OFF<br> Transmitter holds Electrical Idle voltage and DC common mode voltage<br> Recommended Power Budget <= 5 mW per Lane<br> Recommended exit latency < 10 microseconds (may be greater)<br> Both directions of the Link must be in L1 at the same time<br> Transmitter and Receiver clock PLL may be OFF, but clock to device ON<br> Transmitter is On, Receiver is ON<br> High or Low impedance termination at transmitter<br>No Spec<br>**----- End of picture text -----**<br>


**502** 

**Chapter 13: Physical Layer - Electrical** 

_Figure 13‐38: L2 Low Power Link State_ 

**==> picture [378 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect Transmitter most likely OFF,<br>no DC value maintained<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>OFF direction OFF<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM High or Low  VRX-CM = 0 V High impedance OFF<br>impedance termination termination<br>OFF<br>Low frequency   Transmitter holds Electrical Idle voltage, but not required to hold<br>DC common mode voltage. Most likely OFF.<br>for Beacon ON  Recommended Power Budget <= 1 mW per Lane<br> Recommended exit latency < 12 - 50 milliseconds<br> Both directions of the Link in L2<br> Transmitter and Receiver clock PLL OFF, and clock to device OFF<br> Low frequency clock for Beacon in transmitter ON<br> Main power to device OFF, but Vaux ON<br> Transmitter is OFF, Receiver is OFF<br> High or Low impedance termination at transmitter, high impedance at receiver<br>No Spec<br>**----- End of picture text -----**<br>


**503** 

## **PCI Ex ress Technolo p gy** 

## _Figure 13‐39: L3 Link Off State_ 

**==> picture [366 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect DC common mode voltage OFF<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>OFF direction OFF<br>CTX ZTX<br>-<br>D- D-<br>Clock<br>ZTX ZTX ZRX ZRX<br>Clock High impedance  High impedance Source<br>Source VCM termination VRX-CM = 0 V termination OFF<br>OFF<br> Transmitter does not hold DC common mode voltage<br>Low frequency   Recommended Power Budget: zero<br>for Beacon OFF  Recommended L3 -> L0 exit latency < 12 - 50 milliseconds after<br>power turned ON<br> Both directions of the Link in L3<br> Transmitter and Receiver clock PLL OFF, and clock to device OFF<br> Low frequency clock for Beacon in transmitter OFF<br> Main power to device OFF, Vaux OFF<br> Transmitter and Receiver OFF<br> High impedance termination at transmitter and receiver<br>No Spec<br>**----- End of picture text -----**<br>


**504** 

## _**14 Link Initialization & Training**_ 

## **The Previous Chapter** 

The previous chapter describes the Physical Layer electrical interface to the Link, including some low‐level characteristics of the differential Transmitters and Receivers. The need for signal equalization and the methods used to accom‐ plish it are also discussed here. This chapter combines electrical transmitter and receiver characteristics for both Gen1, Gen2 and Gen3 speeds. 

## **This Chapter** 

This chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process of the Link is described from Power‐On or Reset until the Link reaches fully‐operational L0 state during which normal packet traffic occurs. In addition, the Link power management states L0s, L1, L2, and L3 are discussed along with the state transi‐ tions. The Recovery state, during which bit lock, symbol lock or block lock are re‐established is described. Link speed and width change for Link bandwidth management is also discussed. 

## **The Next Chapter** 

The next chapter discusses error types that occur in a PCIe Port or Link, how they are detected, reported, and options for handling them. Since PCIe is designed to be backward compatible with PCI error reporting, a review of the PCI approach to error handling is included as background information. Then we focus on PCIe error handling of correctable, non‐fatal and fatal errors. 

**505** 

**PCI Ex ress Technolo p gy** 

## **Overview** 

Link initialization and training is a hardware‐based (not software) process con‐ trolled by the Physical Layer. The process configures and initializes a device’s link and port so that normal packet traffic proceeds on the link. 

_Figure 14‐1: Link Training and Status State Machine Location_ 

**==> picture [380 x 338] intentionally omitted <==**

**----- Start of picture text -----**<br>
Memory, I/O, Configuration R/W Requests or Message Requests or Completions<br>(Software layer sends / receives address/transaction type/data/message index)<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Transaction layer<br>Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers Buffers<br>Management<br>per VC per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC ACK/NAK CRC ACK/NAK CRC Sequence TLP LCRC<br>Data Link layer TLP Replay De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Link  Serial-to-Parallel<br>Differential Driver Training Differential Receiver<br>(LTSSM)<br>Port<br>**----- End of picture text -----**<br>


**506** 

**Chapter 14: Link Initialization & Training** 

The full training process is automatically initiated by hardware after a reset and is managed by the LTSSM (Link Training and Status State Machine), shown in Figure 14‐1 on page 506. 

Several things are configured during the Link initialization and training pro‐ cess. Let’s consider what they are and define some terms up front. 

- **Bit Lock** : When Link training begins the Receiver’s clock is not yet synchro‐ nized with the transmit clock of the incoming signal, and is unable to reliably sample incoming bits. During Link training, the Receiver CDR (Clock and Data Recovery) logic recreates the Transmitter’s clock by using the incoming bit stream as a clock reference. Once the clock has been recovered from the stream, the Receiver is said to have acquired Bit Lock and is then able to sam‐ ple the incoming bits. For more on the Bit Lock mechanism, see “Achieving Bit Lock” on page 395. 

- **Symbol Lock** : For 8b/10b encoding (used in Gen1 and Gen2), the next step is to acquire Symbol Lock. This is a similar problem in that the receiver can now see individual bits but doesn’t know where the boundaries of the 10‐bit Symbols are found. As TS1s and TS2s are exchanged, Receivers search for a recognizable pattern in the bit stream. A simple one to use for this is the COM Symbol. Its unique encoding makes it easy to recognize and its arrival shows the boundary of both the Symbol and the Ordered Set since a TS1 or TS2 must be in progress. For more on this, see “Achieving Symbol Lock” on page 396. 
