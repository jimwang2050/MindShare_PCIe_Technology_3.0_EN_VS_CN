# 📘 第 12 章　物理层 - 逻辑 (Gen3) (Chapter 12. Physical Layer - Logical (Gen3))

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0285.md` ... `chunks/chunk0292.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Physical Layer - Logical (Gen3)](#-本章目录-table-of-contents)

<a id="sec-12-1"></a>
## 12.1 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-2"></a>
## 12.2 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- **Block Lock** : For 8.0 GT/s (Gen3), the process is a little different from Symbol Lock because since 8b/10b encoding is not used, there are no COM charac‐ ters. However, Receivers still need to find a recognizable packet boundary in the incoming bit stream. The solution is to include more instances of the EIEOS (Electrical Idle Exit Ordered Set) in the training sequence and use that to locate the boundaries. An EIEOS is recognizable as a pattern of alternating 00h and FFh bytes, and it defines the Block boundary because, by definition, when that pattern ends the next Block must begin. 

- **Link Width** : Devices with multiple Lanes may be able to use different Link widths. For example, a device with a x2 port may be connected to one with a x4 port. During Link training, the Physical Layer of both devices tests the Link and sets the width to the highest common value. 

- **Lane Reversal:** The Lanes on a multi‐Lane device’s port are numbered sequentially beginning with Lane 0. Normally, Lane 0 of one device’s port connects to Lane 0 of the neighbor’s port, Lane 1 to Lane 1, and so on. How‐ ever, sometimes it’s desirable to be able to logically reverse the Lane numbers to simplify routing and allow the Lanes to be wired directly without having to crisscross (see Figure 14‐2 on page 508). As long as one device supports the optional Lane Reversal feature, this will work. The situation is detected dur‐ 

**507** 

**PCI Ex ress Technolo p gy** 

ing Link training and one device must internally reverse its Lane numbering. Since the spec doesn’t require support for this, board designers will need to verify that at least one of the connected devices supports this feature before wiring the Lanes in reverse order. 

_Figure 14‐2: Lane Reversal Example (Support Optional)_ 

**==> picture [352 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
Example 1 Example 2<br>Neither device supports Lane Reversal Device B supports Lane Reversal<br>Device A Device A<br>(Upstream Device) (Upstream Device)<br>0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3<br>Lanes<br>after<br>reversal<br>0 1 2 3 0 1 2 3<br>3 2 1 0 3 2 1 0 3 2 1 0 3 2 1 0 Lanes<br>before<br>Device B Device B<br>reversal<br>(Downstream Device) (Downstream Device)<br>Traces must cross to wire the Lanes Lane Reversal allows Lane<br>correctly, adding complexity and cost. numbers to match directly.<br>**----- End of picture text -----**<br>


- **Polarity Inversion** : The D+ and D‐ differential pair terminals for two devices may also be reversed as needed to make board layout and routing easier. Every Receiver Lane must independently check for this and automatically correct it as needed during training, as illustrated in Figure 14‐3 on page 509. To do this, the Receiver looks at Symbols 6 to 15 of the incoming TS1s or TS2s. If a D21.5 is received instead of a D10.2 in a TS1, or a D26.5 instead of the D5.2 expected for a TS2, then the polarity of that lane is inverted and must be corrected. Unlike Lane reversal, support for this feature is manda‐ tory. 

**508** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐3: Polarity Inversion Example (Support Required)_ 

**==> picture [270 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A<br>(Upstream Device)<br>D+ D- D+ D-<br>After Polarity Inversion<br>D- D+<br>After Polarity Inversion<br>D+ D-<br>Before Polarity Inversion<br>D- D+ D- D+<br>Device B<br>(Downstream Device)<br>**----- End of picture text -----**<br>


- **Link Data Rate** : After a reset, Link initialization and training will always use the default 2.5Gbit/s data rate for backward compatibility. If higher data rates are available, they are advertised during this process and, when the training is completed, devices will automatically go through a quick re‐training to change to the highest commonly supported rate. 

- **Lane‐to‐Lane De‐skew** : Trace length variations and other factors cause the parallel bit streams of a multi‐Lane Link to arrive at the Receivers at different times, a problem referred to as signal skew. Receivers are required to com‐ pensate for this skew by delaying the early arrivals as needed to align the bit streams (see “Lane‐to‐Lane Skew” on page 442). They must correct a rela‐ tively big skew automatically (20ns difference in arrival time is permitted at 2.5GT/s), and that frees board designers from the sometimes difficult con‐ straint of creating equal‐length traces. Together with Polarity Inversion and Lane Reversal, this greatly simplifies the board designer’s task of creating a reliable high‐speed Link. 

## **Ordered Sets in Link Training** 

## **General** 

All of the different types of Physical Layer Ordered Sets were described in the section called “Ordered sets” on page 388. Training Sequences TS1 and TS2 are of interest during the training process. The format for these when in Gen1 or Gen2 mode is shown in Figure 14‐4 on page 510, while for Gen3 mode of opera‐ tion, they are as shown in Figure 14‐5 on page 511. A detailed description of their contents follows. 

**509** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐4: TS1 and TS2 Ordered Sets When In Gen1 or Gen2 Mode_ 

**==> picture [281 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM K28.5<br>1 Link # 0 - 255 = D0.0 - D31.7,   PAD = K23.7<br>2 Lane # 0 - 31 = D0.0 - D17.1,   PAD = K23.7<br>3 # FTS # of FTSs required by Receiver for L0s recovery<br>4 Rate ID Bit 1 must be set, indicates 2.5 GT/s support<br>5 Train Ctl<br>6 TS ID or Equalization info when<br>changing to 8.0 GT/s, else<br>9 EQ Info TS1 or TS2 Identifier<br>10<br>TS1 Identifier = D10.2<br>TS ID<br>TS2 Identifier = D5.2<br>15<br>**----- End of picture text -----**<br>


## **TS1 and TS2 Ordered Sets** 

As seen in the illustrations, TS1s and TS2s consist of 16 Symbols. They are exchanged during the Polling, Configuration, and Recovery states of the LTSSM described in “Link Training and Status State Machine (LTSSM)” on page 518. The Symbols are described below and summarized in Table 14‐1 on page 514 for TS1s and Table 14‐2 on page 516 for TS2s. 

To make the descriptions a little shorter and easier to read, the term “Gen1” will be used to indicated data rate of 2.5 GT/s, “Gen2” to indicated data rate of 5.0 GT/s and “Gen3” to indicate data rates of 8.0 GT/s. Also, note that the PAD char‐ acter used in the Link and Lane numbers is represented by the K23.7 character for the lower data rates, but as the data byte F7h for Gen3. In our discussion the distinction between the types of PAD is not interesting and will simply be implied. 

**510** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐5: TS1 and TS2 Ordered Set Block When In Gen3 Mode of Operation_ 

**==> picture [295 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 TS1 = 1Eh,   TS2 = 2Dh<br>1 Link # 0 - 31,   PAD = F7h<br>2 Lane # 0 - 31,   PAD = F7h<br>3 # FTS # of FTSs required by Receiver for L0s recovery<br>4 Rate ID Bit 3 indicates 8.0 GT/s support<br>5 Train Ctl<br>6<br>Equalization presets<br>EQ Info<br>and coefficients or TS2<br>9<br>10<br>TS1 Identifier = 4Ah<br>TS ID<br>TS2 Identifier = 45h<br>13<br>14 TS ID TS1, TS2, or<br>15 DC Balance Symbols<br>**----- End of picture text -----**<br>


Table 14‐1 on page 514 and Table 14‐2 on page 516 is a summary of TS1 and TS2 contents. A more detailed description of the 16 TS1/TS2 Symbols follows: 

- **Symbol 0** : 

- For **Gen1 or Gen2** , the first Symbol of any Ordered Set is the K28.5 (COM) character. Receivers use this character to acquire Symbol Lock. Since it must appear on all Lanes at the same time it’s also useful for de‐skewing the Lanes. 

- For **Gen3** , an Ordered Set is identified by the 2‐bit Sync Header that must precede the Block (not shown in the illustration), and the first Symbol after that indicates which Ordered Set will follow. For a TS1, the first Symbol is 1Eh, and for a TS2, it’s 2Dh. 

- **Symbol 1 (Link #)** : In the Polling state this field contains the PAD Symbol, but in the other states a Link Number is assigned. 

- **Symbol 2 (Lane #)** : In the Polling state this field contains the PAD Symbol, but in the other states a Lane Number is assigned. 

- **Symbol 3 (N_FTS)** : Indicates the number of Fast Training Sequences the Receiver will need in order to achieve the L0 state when exiting from the L0s power state at the current speed. Transmitters will send at least that many 

**511** 

## **PCI Ex ress Technolo p gy** 

FTSs to exit L0s. The amount of time needed for this depends on how many are needed and the data rate in use. For example, at 2.5 GT/s each Symbol takes 4ns so, if 200 FTSs were needed the required time would be 200 FTS * 4 Symbols per FTS * 4ns/Symbol = 3200 ns. If the Extended Synch bit is set in the transmitter device, a total of 4096 FTSs must be sent. This large number is intended to provide enough time for external Link monitoring tools to acquire Bit and Symbol Lock, since some of them may be slow in this regard. 

- **Symbol 4 (Rate ID** ): Devices report which data rates they support, along with a little more information used for hardware‐initiated bandwidth changes. The 2.5 GT/s rate must always be supported and the Link will always train to that speed automatically after reset so that newer components will remain backward compatible with older ones. If 8.0 GT/s is supported, it’s also required that 5.0 GT/s must be available. Other information in this Symbol includes the following: 

- **Autonomous Change** : If set, any requested bandwidth change was initi‐ ated for power‐management reasons. If a change is requested and this bit is not set, then unreliable operation has been detected at the higher speed or wider Link and the change is requested to fix that problem. 

- **Selectable De‐emphasis** 

   - **Upstream Ports** set this to indicate their desired de‐emphasis level at 5.0 GT/s. How they make this choice is implementation specific. In the Recovery.RcvrCfg state, they register the value they receive for this bit internally (the spec describes it as being stored in a select_deemphasis variable). 

   - **Downstream Ports and Root Ports** : In the Polling.Compliance state the select_deemphasis variable must be set to match the received value of this bit. In the Recovery.RcvrCfg state, the Transmitter sets this bit in its TS2s to match the Selectable De‐emphasis field in the Link Control 2 register. Since this register bit is hardware‐initialized, the expectation is that it’s assigned to an optimal value at power‐up by firmware or a strapping option. 

   - In Loopback mode at 5.0 GT/s, the Slave de‐emphasis value is assigned by this bit in the TS1s sent by the Master. 

- **Link Upconfigure Capability** : Reports whether a wide Link whose width is reduced will be capable of going back to the wide case or not. If both sides of a Link report this during Configuration.Complete, this fact is recorded internally (e.g. an upconfigure_capable bit is set). 

- **Symbol 5 (Training Control)** : Communicates special conditions such as a Hot Reset, Enable Loopback mode, Disable Link, Disable Scrambling. 

**512** 

**Chapter 14: Link Initialization & Training** 

- **Symbols 6‐9 (Equalization Control** ):

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-3"></a>
## 12.3 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- For **Gen1 or Gen2** , Symbols 7‐9 are just TS1 or TS2 indicators, and Symbol 6 usually is, too. However, if bit 7 of Symbol 6 is set to one instead of the zero that would be there for the TS1 or TS2 identifier, that indicates that this is an EQ TS1 or EQ TS2 sent from the Downstream Port (DSP ‐ port that faces downstream, like a Root Port). The “EQ” label stands for equal‐ ization, and means that the Link is going to change to 8.0 GT/s and so the Upstream Port (USP ‐ port that faces upstream, like an Endpoint Port) needs to know what equalizer values to use. For EQ TS1s or TS2s, Symbol 6 gives that information to the USP in the form of Transmitter Presets and Receiver Preset Hints. Ports that support 8.0 GT/s must accept either TS type (regular or EQ), but ports that do not support it are not required to accept the EQ type. The possible values for these presets are listed in Table 14‐8 on page 579 and Table 14‐9 on page 580. 

- For **Gen3** , Symbols 6‐9 provide Preset values and Coefficients for the Equalization process. Bit 7 of Symbol 6 in a TS2 can now be used by a USP to request that equalization be redone. If it does, bit 6 may also be set to indicate that the time needed to repeat the equalization process won’t cause problems, such as a completion timeout, as long as it’s done quickly (within 1ms of returning to L0). This might be needed, for example, if a problem was detected with the equalization results. A DSP can also use bits 6 and 7 to ask the USP to make such a request and guarantee no side effects, although the USP is not required to respond to this. For more on the equalization process, see “Link Equalization Overview” on page 577. 

- **Symbols 10‐13** : TS1 or TS2 identifiers. 

- **Symbols 14‐15** : (DC Balance) 

- For **Gen1 and Gen2** , these are just TS1 or TS2 indicators since DC Balance is maintained by 8b/10b encoding. 

- For **Gen3** , the contents of these two Symbols depend on the DC Balance of the Lane. Each Lane of a Transmitter must independently track the run‐ ning DC Balance for all the scrambled bits sent for TS1s and TS2s. “Run‐ ning DC Balance” means the difference between the number of ones sent vs. the number of zeroes sent, and Lanes must be capable of tracking a dif‐ ference of up to 511 in either direction. These counters saturate at their max value but continue to track reductions. For example, if the counter indi‐ cates that 511 more ones than zeroes have been sent, then no matter how many more ones are sent, the value will stay at 511. However, if 2 zeroes are sent, the counter will count down to 509. When a TS1 or TS2 is sent, the following algorithm is used to determine Symbols 14 and 15: 

   - If the running DC Balance value is > 31 at the end of Symbol 11 and more ones have been sent, Symbol 14 = 20h and Symbol 15 = 08h. If more zeroes have been sent, Symbol 14 = DFh and Symbol 15 = F7h. 

**513** 

## **PCI Ex ress Technolo p gy** 

   - If the running DC Balance value is > 15, Symbol 14 = the normal scrambled TS1 or TS2 identifier, while Symbol 15 = 08h to reduce the number of ones, or F7h to reduce the number of zeroes in the DC Bal‐ ance count. 

   - Otherwise, the normal TS1 or TS2 identifier Symbols will be sent. 

- Other notes on Gen3 DC Balance: 

   - The running DC Balance is reset by an exit from Electrical Idle or an EIEOS after a Data Block. 

   - The DC Balance Symbols bypass scrambling to ensure that the expected bit pattern is sent. 

_Table 14‐1: Summary of TS1 Ordered Set Contents_ 

|**Symbol**<br>**Number**|**Description**|
|---|---|
|0|• For Gen1 or Gen2, the COM (K28.5) Symbol<br>• For Gen3, 1Eh indicates a TS1.|
|1|Link Number<br>• Ports that don’t support Gen3: 0‐255, PAD<br>• Downstream ports that support Gen3: 0‐31, PAD<br>• Upstream ports that support Gen3: 0‐255, PAD|
|2|Lane Number<br>• 0‐31, PAD|
|3|N_FTS<br>• Number of FTS Ordered Sets required by receiver to achieve L0 when exiting<br>L0s: 0 ‐ 255|
|4|Data Rate Identifier:<br>• Bit 0 — Reserved.<br>• Bit 1 — 2.5 GT/s supported (must be set to 1b)<br>• Bit 2 — 5.0 GT/s supported (must be set if bit 3 is set)<br>• Bit 3 — 8.0 GT/s supported<br>• Bits 5:4 — Reserved<br>• Bit 6 — Autonomous Change/Selectable De‐emphasis<br>–<br>Downstream Ports: Used in Polling.Active, Configuration.Linkwidth.Start,<br>and Loopback.Entry LTSSM states, and reserved in all other states.<br>–<br>Upstream Ports: Used in Polling.Active, Configuration, Recovery, and<br>Loopback.Entry LTSSM states and reserved in all other states.<br>• Bit 7 — Speed change. This can only be set to one in the Recovery.RcvrLock<br>LTSSM state, and is reserved in all other states.|



**514** 

**Chapter 14: Link Initialization & Training** 

_Table 14‐1: Summary of TS1 Ordered Set Contents (Continued)_ 

|**Symbol**<br>**Number**|**Description**|
|---|---|
|5|Training Control (0=De‐assert, 1 = Assert)<br>• Bit 0 — Hot Reset<br>• Bit 1 — Disable Link<br>• Bit 2 — Loopback<br>• Bit 3 — Disable Scrambling (for 2.5 or 5.0 GT/s; reserved for Gen3)<br>• Bit 4 — Compliance Receive (optional for 2.5 GT/s, required for all other rates)<br>• Bits 7:5 — Reserved, Set to 0|
|6|For Gen1 or Gen2:<br>• TS1 identifier (4Ah) encoded as D10.2<br>• EQ TS1s encode this as<br>Bits 2:0 — Receiver preset hint<br>Bits 6:3 — Transmitter Preset<br>Bit 7 — set to 1b<br>For Gen3:<br>• Bits 1:0 — Equalization Control (EC). Only used in Recovery.Equalization and<br>Loopback LTSSM states; must be 00b in all other states.<br>• Bit 2 — Reset EIEOS Interval Count. Only used in Recovery.Equalization<br>LTSSM state; reserved in all other states.<br>• Bits 6:3 — Transmitter Preset<br>• Bit 7 — Use Preset. (If one, use the preset values instead of the coefficient val‐<br>ues. If zero, use the coefficients rather than the presets.) Only used in Recov‐<br>ery.Equalization and Loopback LTSSM states; reserved in all other states.|
|7|For Gen1 or Gen2 GT/s, TS1 identifier (4Ah) encoded as D10.2<br>For Gen3:<br>• Bits 5:0 — FS (Full Swing value) when the EC field of Symbol 6 is 01b, other‐<br>wise, Pre‐cursor Coefficient.<br>• Bits 7:6 — Reserved.|
|8|For Gen1 or Gen2, TS1 identifier (4Ah) encoded as D10.2<br>For Gen3:<br>• Bits 5:0 — LF (Low Frequency value) when the EC field of Symbol 6 is 01b, oth‐<br>erwise, Cursor Coefficient.<br>• Bits 7:6 — Reserved.|



**515** 

**PCI Ex ress Technolo p gy** 

_Table 14‐1: Summary of TS1 Ordered Set Contents (Continued)_ 

|**Symbol**<br>**Number**|**Description**|
|---|---|
|9|For Gen1 or Gen2, TS1 identifier (4Ah) encoded as D10.2<br>For Gen3:<br>• Bits 5:0 — Post‐cursor Coefficient.<br>• Bit 6 — Reject Coefficient Values. Only set in specific Phases of the Recov‐<br>ery.Equalization LTSSM state; must be 0b otherwise.<br>• Bit 7 — Parity (P) This is the even parity of all bits of Symbols 6, 7, and 8 and<br>bits 6:0 of Symbol 9. Receivers must calculate this and compare it to the<br>received Parity bit. Received TS1s are only valid if the Parity bits match.|
|10‐13|For Gen1 or Gen2, TS1 identifier (4Ah) encoded as D10.2<br>• For Gen3, TS1 identifier (4Ah)|
|14‐15|For Gen1 or Gen2, TS1 identifier (4Ah) encoded as D10.2<br>• For Gen3, TS1 identifier (4Ah), or a DC‐Balance Symbol.|



The observant reader may wonder why EQ TS1s are shown in Symbol 6 for the lower data rates since only 8.0 GT/s data rates use equalization. That’s because they’re used to deliver EQ values for Lanes that support Gen3 but are currently operating at a lower rate and want to change to 8.0 GT/s. For more details regarding this and the Equalization process for Gen3 in general, see “Link Equalization Overview” on page 577. 

_Table 14‐2: Summary of TS2 Ordered Set Contents_ 

|**Symbol**<br>**Number**|**Description**|
|---|---|
|0|• For Gen1 or Gen2, the COM (K28.5) Symbol<br>• For Gen3, 2Dh indicates a TS2.|
|1|Link Number<br>• Ports that don’t support Gen3: 0‐255, PAD<br>• Downstream ports that support Gen3: 0‐31, PAD<br>• Upstream ports that support Gen3 0‐255, PAD|
|2|Lane Number<br>• 0‐31, PAD|



**516** 

**Chapter 14: Link Initialization & Training** 

_Table 14‐2: Summary of TS2 Ordered Set Contents (Continued)_ 

|**Symbol**<br>**Number**|**Description**|
|---|---|
|3|N_FTS<br>• Number of FTS Ordered Sets required by receiver to achieve L0 when exiting<br>L0s: 0 ‐ 255|
|4|Data Rate Identifier:<br>• Bit 0 — Reserved.<br>• Bit 1 — 2.5 GT/s supported (must be set to 1b)<br>• Bit 2 — 5.0 GT/s supported (must be set if bit 3 is set)<br>• Bit 3 — 8.0 GT/s supported<br>• Bits 5:4 — Reserved<br>• Bit 6 — Autonomous Change/Selectable De‐emphasis/Link Upconfigure Capa‐<br>bility. Used in Polling.Configuration, Configuration.Complete, and Recovery<br>LTSSM states; reserved in all other states.<br>• Bit 7 — Speed change. This can only be set to one in the Recovery.RcvrLock<br>LTSSM state, and is reserved in all other states.|
|5|Training Control (0 = De‐assert, 1 = Assert)<br>• Bit 0 — Hot Reset,<br>• Bit 1 — Disable Link<br>• Bit 2 — Loopback<br>• Bit 3 — Disable Scrambling (for 2.5 or 5.0 GT/s; reserved for Gen3)<br>• Bits 7:4 — Reserved, Set to 0|
|6|For Gen1 or Gen2:<br>• TS2 identifier (4Ah) encoded as D10.2<br>• EQ TS2s encode this as<br>Bits 2:0 — Receiver preset Hint<br>Bits 6:3 — Transmitter Preset<br>Bit 7 — Equalization Command<br>For Gen3:<br>• Bits 5:0 — Reserved.<br>• Bit 6 — Quiesce Guarantee. Defined for use in Recovery.RcvrCfg only;<br>reserved in all other states.<br>• Bit 7 — Request Equalization. Defined for use in Recovery.RcvrCfg only;<br>reserved in all other states.|
|7‐13|• For Gen1 or Gen2, TS2 identifier (45h) encoded as D5.2<br>• For Gen3, TS2 identifier (45h)|
|14‐15|• For Gen1 or Gen2, TS2 identifier (45h) encoded as D5.2<br>• For Gen3, TS2 identifier (45h), or a DC‐Balance Symbol|



**517** 

**PCI Ex ress Technolo p gy** 

## **Link Training and Status State Machine (LTSSM)** 

## **General** 

Figure 14‐6 on page 519 illustrates the top‐level states of the Link Training and Status State Machine (LTSSM). Each state consists of substates. The first LTSSM state entered after exiting Fundamental Reset (Cold or Warm Reset) or Hot Reset is the Detect state. 

The LTSSM consists of 11 top‐level states: Detect, Polling, Configuration, Recov‐ ery, L0, L0s, L1, L2, Hot Reset, Loopback, and Disable. These can be grouped into five categories: 

1. Link Training states 

2. Re‐Training (Recovery) state 

3. Software driven Power Management states 

4. Active‐State Power Management (ASPM) states 

5. Other states 

When exiting from any type of Reset, the flow of the LTSSM follows the **Link Training states** : Detect => Polling => Configuration => L0. In L0 state, normal packet transmission/reception is in progress. 

The **Link Re‐Training also called Recovery** state is entered for a variety of rea‐ sons, such as changing back from a low‐power Link state, like L1, or changing the Link bandwidth (through speed or width changes). In this state, the Link repeats as much of the training process as needed to handle the matter and returns to L0 (normal operation). 

Power management software may also place a device into a low‐power device state (D1, D2, D3Hot or D3Cold) and that will force the Link into a lower **Power Management Link state** (L1 or L2). 

If there are no packets to send for a time, ASPM hardware may be allowed to automatically transition the Link into low power **ASPM states** (L0s or ASPM L1). 

In addition, software can direct a Link to enter some **other special states** : Dis‐ abled, Loopback, or Hot Reset. Here, these are collectively called the Other states group. 

**518** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐6: Link Training and Status State Machine (LTSSM)_ 

**==> picture [322 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-4"></a>
## 12.4 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Initial State after any<br>Reset or as directed<br>by the Data Link Layer<br>Disabled<br>Detect<br>Training States<br>Re-Training State<br>External<br>Loop back Power Mgt States<br>Polling<br>ASPM States<br>Hot<br>Reset Other States<br>From<br>Configuration From Configuration<br>or Recovery<br>Recovery<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


## **Overview of LTSSM States** 

Below is a brief description of the 11 high‐level LTSSM states. 

- **Detect** : The initial state after reset. In this state, a device electrically detects a Receiver is present at the far end of the Link. That’s an unusual thing in the world of serial transports, but it’s done to facilitate testing, as we’ll see in the next state. Detect may also be entered from a number of other LTSSM states as described later. 

- **Polling** : In this state, Transmitters begin to send TS1s and TS2s (at 2.5 GT/s for backward compatibility) so that Receivers can use them to accomplish the following: 

   - Achieve Bit Lock 

   - Acquire Symbol Lock or Block Lock 

   - Correct Lane polarity inversion, if needed 

   - Learn available Lane data rates 

**519** 

**PCI Ex ress Technolo p gy** 

   - If directed, Initiate the Compliance test sequence: The way this works is that if a receiver was detected in the Detect state but no incoming signal is seen, it’s understood to mean that the device has been connected to a test load. In that case, it should send the specified Compliance test pat‐ tern to facilitate testing. This allows test equipment to quickly verify that voltage, BER, timing, and other parameters are within tolerance. 

- **Configuration** : Upstream and Downstream components now play specific roles as they continue to exchange TS1s and TS2s at 2.5 GT/s to accomplish the following: 

   - Determine Link width 

   - Assign Lane numbers 

   - Optionally check for Lane reversal and correct it 

   - Deskew Lane‐to‐Lane timing differences 

      - From this state, scrambling can be disabled, the Disable and Loopback states can be entered, and the number of FTS Ordered Sets required to transition from the L0s state to the L0 state is recorded from the TS1s and TS2s. 

- **L0** : This is the normal, fully‐active state of a Link during which TLPs, DLLPs and Ordered Sets can be exchanged. In this state, the Link could be running at higher speeds than 2.5 GT/s, but only after re‐training (Recovery) the Link and going through a speed change procedure. 

- **Recovery** : This state is entered when the Link needs re‐training. This could be caused by errors in L0, or recovery from L1 back to L0, or recovery from L0s if the Link does not train properly using the FTS sequence. In Recovery, Bit Lock and Symbol/Block Lock are re‐established in a manner similar to that used in the Polling state but it typically takes much less time. 

- **L0s** : This ASPM state is designed to provide some power savings while affording a quick recovery time back to L0. It’s entered when one Transmitter sends the EIOS while in the L0 state. Exit from L0s involves sending FTSs to quickly re‐acquire Bit and Symbol/Block Lock. 

- **L1** : This state provides greater power savings by trading off a longer recovery time than L0s does (see “Active State Power Management (ASPM)” on page 735). Entry into L1 involves a negotiation between both Link partners to enter it together and can occur in one of two ways: 

   - The first is autonomous with ASPM: hardware in an Upstream Port with no scheduled TLPs or DLLPs to transmit can automatically negotiate to put its Link into the L1 state. If the Downstream Port agrees, the Link enters L1. If not, the Upstream Port will enter L0s instead (if enabled). 

   - The second is the result of power management software issuing a com‐ manding a device to a low‐power state (D1, D2, or D3Hot). As a result, the Upstream Port notifies the Downstream Port that they must enter L1, the Downstream Port acknowledges that, and they enter L1. 

**520** 

**Chapter 14: Link Initialization & Training** 

- **L2** : In this state the main power to the devices is turned off to achieve a greater power savings. Almost all of the logic is off, but a small amount of power is still available from the Vaux source to allow the device to indicate a wakeup event. An Upstream Port that supports this wakeup capability can send a very low frequency signal called the Beacon and a Downstream Port can forward it to the Root Complex to get system attention (see “Beacon Sig‐ naling” on page 483). Using the Beacon, or a side‐band WAKE# signal, a device can trigger a system wakeup event to get main power restored. [An L3 Link power state is also defined, but it doesn’t relate to the LTSSM states. The L3 state is the full‐off condition in which Vaux power is not available and a wakeup event can’t be signaled.] 

- **Loopback** : This state is used for testing but exactly what a Receiver does in this mode (for example: how much of the logic participates) is left unspeci‐ fied. The basic operation is simple enough: the device that will be the Loop‐ back Master sends TS1 Ordered Sets that have the Loopback bit set in the Training Control field to the device that will be the Loopback Slave. When a device sees two consecutive TS1s with the Loopback bit set, it enters the Loopback state as the Loopback Slave and echoes back everything that comes in. The Master, recognizing that what it is sending is now being echoed, sends any pattern of Symbols that follow the 8b/10b encoding rules, and the Slave echoes them back exactly as they were sent, providing a round‐trip ver‐ ification of Link integrity. 

- **Disable** : This state allows a configured Link to be disabled. In this state, the Transmitter is in the Electrical Idle state while the Receiver is in the low impedance state. This might be necessary because the Link has become unre‐ liable or due to a surprise removal of the device. Software commands a device to do this by setting the Disable bit in the Link Control register. The device then sends 16 TS1s with the Disable Link bit set in the TS1 Training Control field. Receivers are disabled when they receive those TS1s. 

- **Hot Reset:** Software can reset a Link by setting the Secondary Bus Reset bit in the Bridge Control register. That causes the bridge’s Downstream Port to send TS1s with the Hot Reset bit set in the TS1 Training Control field (see “Hot Reset (In‐band Reset)” on page 837) When a Receiver sees two consecutive TS1s with the Hot Reset bit set, it must reset its device. 

## **Introductions, Examples and State/Substates** 

The balance of this chapter covers each of the LTSSM states. Depending on the complexity of a given state, the discussion may include an introduction, general background, and/or examples that accompanies the detailed discussion of the State/Substate. In some cases, the reader may choose to skip the detailed cover‐ 

**521** 

## **PCI Ex ress Technolo p gy** 

age and jump to introductory material. Each section is organized to facilitate these options. 

Every device must perform initial link training at the base rate of 2.5 GT/s. Fig‐ ure 14‐7 highlights the states involved in the initial training sequence. Devices capable of operating at 5.0 or 8.0 GT/s must transition to the Recovery state to change the speed to the higher rate chosen. 

_Figure 14‐7: States Involved in Initial Link Training at 2.5 Gb/s_ 

**==> picture [304 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
Initial State after any<br>Reset or as directed<br>by the Data Link Layer<br>Disabled<br>Detect<br>Training States<br>Re-Training State<br>External<br>Loop back Power Mgt States<br>Polling<br>ASPM States<br>Hot<br>Reset Other States<br>From<br>Configuration From Configuration<br>or Recovery<br>Recovery<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


## **Detect State** 

## **Introduction** 

Figure 14‐8 represents the two substates and transitions associated with the Detect state. The actions associated with the Detect state are performed by each 

**522** 

**Chapter 14: Link Initialization & Training** 

transmitter in the process of detecting the presence of a receiver at the opposite end of the link. Because there are only two substates and because they are fairly simple, we will move directly to the substate discussions. 

_Figure 14‐8: Detect State Machine_ 

**==> picture [288 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from Reset.<br>Also from Disabled,<br>Loopback, L2, Polling,<br>Configuration or<br>Recovery<br>No Electrical<br>Idle on Link or<br>12 ms timeout Receiver<br>Detected<br>Detect.Quiet Detect.Active<br>No Detect<br>12 ms Charge or<br>DC common mode<br>voltage stable<br>Exit to<br>Polling<br>**----- End of picture text -----**<br>


## **Detailed Detect Substate** 

## **Detect.Quiet** 

This substate is the initial state after any reset (except Function Level Reset) or power‐up event and must be entered within 20 ms after Reset. This substate is also entered from other states if unable to move forward (See the states that may enter Detect.Quiet in Figure 14‐8 on page 523). The properties of this substate are listed below: 

- The Transmitter starts in Electrical Idle (but the DC common mode voltage doesn’t have to be within the normally‐specified range). 

- The intended data rate is set to 2.5 GT/s (Gen1). If it set to a different rate when this substate was entered, the LTSSM must stay in this substate for 1ms before changing the rate to Gen1. 

- The Physical Layer’s status bit (LinkUp = 0) informs the Data Link Layer that the Link is not operational. The LinkUp status bit is an internal state bit 

**523** 

## **PCI Ex ress Technolo p gy** 

- (not found in standard config space) and also indicates when the Physical Layer has completed Link Training (LinkUp=1), thereby informing the Data Link Layer and Flow Control initialization to begin its part of Link initial‐ ization (for more on this, see “The FC Initialization Sequence” on page 223). 

- • Any previous equalization (Eq.) status is cleared by setting the four Link Status 2 register bits to zero: Eq. Phase 1 Successful, Eq. Phase 2 Successful, Eq. Phase 3 Successful, Eq. Complete. 

- Variables: 

   - Several variables are cleared to zero: (directed_speed_change=0b, upconfigure_capable=0b, equalization_done_8GT_data_rate=0b, idle_to_rlock_transitioned=00h). The select_deemphasis variable setting depends on the port type: for an Upstream Port it’s selected by hardware, while for a Downstream Port it takes the value in the Link Control 2 regis‐ ter of the Selectable Preset/De‐emphasis field. 

   - Since these variables were defined beginning with the 2.0 spec version, devices designed to earlier spec versions won’t have them and will behave as if directed_speed_change and upconfigure_capable were set to 0b and idle_to_rlock_transitioned was set to FFh. 

## _Exit to “Detect.Active”_ 

The next substate is Detect.Active after a 12 ms timeout or when any Lane exits Electrical Idle. 

## **Detect.Active** 

This substate is entered from Detect.Quiet. At this time the Transmitter tests whether a Receiver is connected on each Lane by setting a DC common mode voltage of any value in the legal range and then changing it. The detection logic observes the rate of change as the time it takes the line voltage to charge up and compares it to an expected time, such as how long it would take without a Receiver termination. If a Receiver is attached, the charge time will be much longer, making it easy to recognize. For more details on this process, see “Receiver Detection” on page 460. To simplify the discussions that follow, Lanes that detect a Receiver during this substate are referred to as “Detected Lanes.” 

## _Exit to “Detect.Quiet”_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-5"></a>
## 12.5 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- If no Lanes detect a Receiver, go back to Detect.Quiet. The loop between them is repeated every 12ms, as long as no Receiver is detected. 

## _Exit to “Polling State”_ 

- If a receiver is detected on all Lanes, the next state will be Polling. The Lanes must now drive a DC common voltage within the 0 ‐ 3.6 V VTX‐CM‐DC spec. 

## _Special Case:_ 

If some but not all Lanes of a device are connected to a Receiver (like a x4 

**524** 

**Chapter 14: Link Initialization & Training** 

device connected to a x2 device), then wait 12 ms and try it again. If the same Lanes detect a Receiver the second time, exit to the Polling state, oth‐ erwise go back to Detect.Quiet. If going to Polling, there are two possibili‐ ties for the Lanes that didn’t see a Receiver: 

1. If the Lanes can operate as a separate Link (see “Designing Devices with Links that can be Merged” on page 541), use another LTSSM and have those Lanes repeat the detect sequence. 

2. If another LTSSM is not available, then the Lanes that don’t detect a Receiver will not be part of a Link and must transition to Electrical Idle. 

## **Polling State** 

## **Introduction** 

To this point the link has been in the electrical idle state, however during Polling the LTSSM TS1s and TS2s are exchanged between the two connected devices. The primary purpose of this state is for the two devices to understand what the each other is saying. In other words, they need to establish bit and symbol lock on each other’s transmitted bit stream and resolve any polarity inversion issues. Once this has been accomplished, each device is successfully receiving the TS1 and TS2 ordered‐sets from their link partner. Figure 14‐9 on page 525 shows the substates of the Polling state machine. 

_Figure 14‐9: Polling State Machine_ 

**==> picture [339 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Detect<br>Entry from<br>Detect<br>24 ms<br>48 ms<br>Exchange<br>1024 TS1s<br>(unless directed Polling.Active Polling.Configuration<br>to Compliance) Bit/Symbol Lock (Polarity Inversion)<br>Directed or<br>Insufficient Lanes Electrical 8 TS1, TS2 (or complement) Rx on ALL 8 TS2 Rx. 16 TS2 Tx.<br>Lanes or 24 ms timeout and ANY<br>detect Idle Exit<br>exit from Electrical Idle Lane Rx 8 TS1, TS2 and ALL Lanes<br>detect exit from Electrical Idle<br>Exit to<br>Polling.Compliance Configuration<br>**----- End of picture text -----**<br>


**525** 

**PCI Ex ress Technolo p gy** 

## **Detailed Polling Substates** 

## **Polling.Active** 

## _During Polling.Active_ 

Transmitters send a minimum of 1024 consecutive TS1s on all detected Lanes once their common‐mode voltage has settled at the level specified in the Transmit Margin field. The two Link partners may exit the Detect state at different times, so the TS1 exchange is not synchronized. The time needed to send 1024 TS1s at Gen1 speed (2.5 GT/s) is 64μs. 

Some notes regarding this substate are: 

- The PAD Symbol must be used in the Lane and Link Number fields of the TS1s. 

- All data rates a device supports must be advertised, even if it doesn’t intend to use them all. 

- Receivers use the incoming TS1s to acquire Bit Lock (see “Achieving Bit Lock” on page 395) and then either Symbol Lock (see “Achieving Symbol Lock” on page 396) for the lower rates, or Block Alignment for 8.0 GT/s (see “Achieving Block Alignment” on page 438). 

## _Exit to “Polling.Configuration”_ 

- The next state is Polling.Configuration if, after sending at least 1024 TS1s **ALL** detected Lanes receive 8 consecutive training sequences (or their com‐ plement, due to polarity inversion) that satisfy one of the following condi‐ tions: 

- TS1s with Link and Lane set to PAD were received with the Compli‐ ance Receive bit cleared to 0b (bit 4 of Symbol 5). 

- TS1s with Link and Lane set to PAD were received with the Loopback bit of Symbol 5 set to 1b. 

- 

- TS2s were received with Link and Lane set to PAD. 

If the conditions above are not met, then after a 24ms timeout, if at least 1024 TS1s were sent after receiving a TS1, and **ANY** detected Lane received eight consecutive TS1 or TS2 Ordered Sets (or their complement) with the Lane and Link numbers set to PAD, and one of the following is true: 

- TS1s with Link and Lane set to PAD were received with the Compli‐ ance Receive (bit 4 of Symbol 5) cleared to 0b. 

- TS1s with Link and Lane set to PAD were received with the Loopback (bit 2 of Symbol 5) set to 1b. 

- TS2s were received with Link and Lane set to PAD. 

**526** 

**Chapter 14: Link Initialization & Training** 

If still none of the conditions above are met, if at least a predetermined number of detected Lanes also detected an exit from Electrical Idle at least once since entering Polling.Active (this prevents one or more bad Transmit‐ ters or Receivers from holding up Link configuration). The exact set of pre‐ determined Lanes is implementation specific now, which is a change from the 1.1 spec that needed to see an Electrical Idle exit on all detected Lanes. 

## _Exit to “Polling.Compliance”_ 

If the Enter Compliance bit in the Link Control 2 register is set to 1b, or if this bit was set before entering Polling.Active, the change to Polling.Com‐ pliance must be immediate and no TS1s are sent in Polling.Active. 

Otherwise, after a 24ms timeout, if: 

- All Lanes from the predetermined set have not seen an exit from Elec‐ trical Idle since entering Polling.Active (indicates a passive test load such as a resistor on at least one Lane forces all Lanes into Poll‐ ing.Compliance). 

- Any detected Lane received 8 consecutive TS1s (or their complement) with Link and Lane numbers set to PAD, the Compliance Receive bit of Symbol 5 set to 1b and the Loopback bit cleared to 0b. 

## _Exit to “Detect State”_ 

- If, after 24ms, the conditions for going to Polling.Configuration or Poll‐ ing.Compliane are not met, return to the Detect state. 

## **Polling.Configuration** 

In this substate, a transmitter will stop sending TS1s and start sending TS2s, still with PAD set for the Link and Lane numbers. The purpose of the change to sending TS2s instead of TS1s is to advertise to the link partner that this device is ready to proceed to the next state in the state machine. It is a handshake mecha‐ nism to ensure that both devices on the link proceed through the LTSSM together. Neither device can proceed to the next state until both devices are ready. The way they advertise they are ready is by sending TS2 ordered‐sets. So once a device is both sending AND receiving TS2s, it knows it can proceed to the next state because it is ready and its link partner is ready too. 

## _During Polling.Configuration_ 

- Transmitters send TS2s with Link and Lane numbers set to PAD on all detected Lanes, and they must advertise all the data rates they support, even those they don’t intend to use. Also, each Lane’s receiver must inde‐ pendently invert the polarity of its differential input pair if necessary. For an explanation of how this is done, see “Overview” on page 506. The Trans‐ mit Margin field must be reset to 000b. 

**527** 

## **PCI Ex ress Technolo p gy** 

## _Exit to “Configuration State”_ 

After eight consecutive TS2s with Link and Lane set to PAD are received on any detected Lanes, and at least 16 TS2s have been sent since receiving one TS2, exit to Configuration. 

## _Exit to “Detect State”_ 

Otherwise, exit to Detect after a 48ms timeout. 

## _Exit to Polling.Speed (Non‐existent substate)_ 

As a historical aside, the substates of Polling have changed since the 1.0 version of the spec was released. At that time it was thought that when other speeds became available it would make sense to change to the highest available rate as soon as possible in this state. However, the advent of higher rates coincided with the realization that it would be advantageous to be able to change speeds both higher and lower during runtime for power management reasons. Going through the Polling state involves clearing a number of Link values and that makes it an unattractive path for runtime use, so the rate change stage was moved out of this state into the Recovery state. See Figure 14‐10 on page 528. 

_Figure 14‐10: Polling State Machine with Legacy Speed Change_ 

**==> picture [355 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Detect<br>Entry from<br>Detect<br>24 ms<br>Speed change step was<br>48 ms moved from this state to<br>Exchange Recovery state<br>1024 TS1s Polling.Speed<br>(unless directed Polling.Active Polling.Configuration (E lect ri c a l Idle ,<br>to Compliance) Bit/Symbol Lock (Polarity Inversion) Ch a ng e Spee d)<br>Directed or<br>Insufficient Lanes Electrical 8 TS1, TS2 (or complement) Rx on ALLLanes or 24 ms timeout and ANY 8 TS2 Rx. 16 TS2 Tx.<br>detect Idle Exit<br>exit from Electrical Idle Lane Rx 8 TS1, TS2 and ALL Lanes<br>detect exit from Electrical Idle<br>Exit to<br>Polling.Compliance Configuration<br>**----- End of picture text -----**<br>


Today, the Link always trains to 2.5 GT/s after a reset, even if other speeds are available. If higher speeds are available once the LTSSM has reached L0, then it transitions to Recovery and attempts to change to the highest commonly‐sup‐ ported or advertised rate. Supported speeds are reported in the exchanged TS1s 

**528** 

**Chapter 14: Link Initialization & Training** 

and TS2s, so that either device can subsequently decide to initiate a speed change by transitioning to the Recovery state. The spec still lists this substate but declares that it is now unreachable. 

## **Polling.Compliance** 

This substate is only used for testing and causes a Transmitter to send specific patterns intended to create near‐worst‐case Inter‐Symbol Interference (ISI) and cross‐talk conditions to facilitate analysis of the Link. Two different patterns can be sent while in this substate, the Compliance Pattern and the Modified Compli‐ ance Pattern. 

**Compliance Pattern for 8b/10b.** This pattern consists of 4 Symbols that are repeated sequentially: K28.5‐, D21.5+, K28.5+ and D10.2‐, where (‐) means negative current running disparity or CRD and (+) means positive CRD (since the CRD is forced, it’s permissible to have a disparity error at the beginning of the pattern). If the Link has multiple Lanes, then four Delay Symbols (shown as D, but are really just additional K28.5 symbols) are injected on Lane 0, two before the next compliance pattern and two after the compliance pattern. Once the last Delay symbol has been sent on Lane 0, the four delay symbols are also sent on Lane 1 (again, two before the next compliance pattern and two after). This process continues until after the Delay symbols have propagated through Lane 7. Then they go back to start‐ ing on Lane 0 again as can be seen in Table 14‐3 on page 529 (the compli‐ ance pattern is shaded in grey). Every group of eight lanes behaves this way. Shifting the Delay Symbols will ensure interference between adjacent Lanes and provide better test conditions. 

_Table 14‐3: Symbol Sequence 8b/10b Compliance Pattern_ 

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|



**529** 

## **PCI Ex ress Technolo p gy** 

_Table 14‐3: Symbol Sequence 8b/10b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|6|D|K28.5+|K28.5+||D|
|7|D|D10.2|D10.2||D|
|8|K28.5‐|D|K28.5‐||K28.5‐|
|9|K21.5|D|K21.5||K21.5|
|10|K28.5+|K28.5‐|K28.5+||K28.5+|
|...|...|...|...||...|
|16|K28.5‐|K28.5‐|D||K28.5‐|
|17|K21.5|K21.5|D||K21.5|
|18|K28.5+|K28.5+|K28.5‐||K28.5+|



**Compliance Pattern for 128b/130b.** This pattern consists of the follow‐ ing repeating sequence of 36 Blocks:

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-6"></a>
## 12.6 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

1. The first Block consists of the Sync Header 01b and contains the unscrambled payload of 64 ones followed by 64 zeros. 

2. The second Block has Sync Header 01b and contains the unscrambled payload shown in Table 14‐4 on page 530 (note that the pattern repeats after 8 Lanes, and that P means the 4‐bit Tx preset being used, while ~P is the bit‐wise inverse of that). 

3. The third Block has Sync Header 01b and contains the unscrambled payload shown in Table 14‐5 on page 531 (same notes as the second Block). 

4. The fourth Block is an EIEOS Block 

5. 32 more Data Blocks, each containing 16 scrambled IDL Symbols (00h). 

_Table 14‐4: Second Block of 128b/130b Compliance Pattern_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|0|55h|FFh|FFh|FFh|55h|FFh|FFh|FFh|
|1|55h|FFh|FFh|FFh|55h|FFh|FFh|FFh|



**530** 

**Chapter 14: Link Initialization & Training** 

_Table 14‐4: Second Block of 128b/130b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|2|55h|00h|FFh|FFh|55h|FFh|FFh|FFh|
|3|55h|00h|FFh|C0h|55h|FFh|F0h|F0h|
|4|55h|00h|FFh|00h|55h|FFh|00h|00h|
|5|55h|00h|C0h|00h|55h|E0h|00h|00h|
|6|55h|00h|00h|00h|55h|00h|00h|00h|
|7|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|
|8|00h|1Eh|2Dh|3Ch|4Bh|5Ah|69h|78h|
|9|00h|55h|00h|00h|00h|55h|00h|F0h|
|10|00h|55h|00h|00h|00h|55h|00h|00h|
|11|00h|55h|00h|00h|00h|55h|00h|00h|
|12|00h|55h|0Fh|0Fh|00h|55h|07h|00h|
|13|00h|55h|FFh|FFh|00h|55h|FFh|00h|
|14|00h|55h|FFh|FFh|7Fh|55h|FFh|00h|
|15|00h|55h|FFh|FFh|FFh|55h|FFh|00h|



_Table 14‐5: Third Block of 128b/130b Compliance Pattern_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|0|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|1|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|2|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|3|F0h|F0h|55h|F0h|F0h|F0h|55h|F0h|
|4|00h|00h|55h|00h|00h|00h|55h|00h|



**531** 

## **PCI Ex ress Technolo p gy** 

_Table 14‐5: Third Block of 128b/130b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|5|00h|00h|55h|00h|00h|00h|55h|00h|
|6|00h|00h|55h|00h|00h|00h|55h|00h|
|7|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|
|8|00h|1Eh|2Dh|3Ch|4Bh|5Ah|69h|78h|
|9|00h|00h|00h|55h|00h|00h|00h|55h|
|10|00h|00h|00h|55h|00h|00h|00h|55h|
|11|00h|00h|00h|55h|00h|00h|00h|55h|
|12|FFh|0Fh|0Fh|55h|0Fh|0Fh|0Fh|55h|
|13|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|
|14|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|
|15|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|



**Modified Compliance Pattern for 8b/10b.** The second compliance pat‐ tern adds an error status field that reports how many Receiver errors have been detected while in Polling.Compliance. 

In 8b/10b mode, the original pattern is still used, but 2 Symbols are added to report the error status (2 are used instead of one to avoid interfering with the required disparity of the sequence) and 2 more K28.5 Symbols are added at the end, making the pattern 8 Symbols long altogether. 

_Table 14‐6: Symbol Sequence of 8b/10b Modified Compliance Pattern_ 

|Symbol|Lane 0|Lane 1|Lane 2|...|Lane 8|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|D|K28.5+|K28.5+||D|
|3|D|D10.2|D10.2||D|



**532** 

**Chapter 14: Link Initialization & Training** 

_Table 14‐6: Symbol Sequence of 8b/10b Modified Compliance Pattern (Continued)_ 

|Symbol|Lane 0|Lane 1|Lane 2|...|Lane 8|
|---|---|---|---|---|---|
|4|K28.5‐|ERR|ERR||K28.5‐|
|5|K21.5|ERR|ERR||K21.5|
|6|K28.5+|K28.5‐|K28.5‐||K28.5+|
|7|D10.2|K28.5+|K28.5+||D10.2|
|8|ERR|K28.5‐|K28.5‐||ERR|
|9|ERR|K21.5|K21.5||ERR|
|10|K28.5‐|K28.5+|K28.5+||K28.5‐|
|11|K28.5+|D10.2|D10.2||K28.5+|
|12|K28.7‐|ERR|ERR||K28.7‐|
|13|K28.7‐|ERR|ERR||K28.7‐|
|14|K28.7‐|K28.5‐|K28.5‐||K28.7‐|
|15|K28.7‐|K28.5+|K28.5+||K28.7‐|
|16|K28.5‐|D|K28.5‐||K28.5‐|



The encoded error status byte contains a Receiver Error Count in ERR [6:0] that reports the number of errors seen since Pattern Lock was asserted. The “Pattern Lock” indicator is ERR bit [7], and shows when the Receiver has locked to the incoming Modified Compliance Pattern. The delay sequence is also different for this pattern, and now adds four K28.5 Symbols (shown as “D” in the table) in a row at the beginning of the sequence and four K28.7 Symbols at the end of the 8‐Symbol pattern, making a total of 16 Symbols that are sent before the Delay pattern shifts to the next Lane. This pattern is illustrated in Table 14‐6 on page 532. It can be seen that the delay pattern shifts to Lane 1 after 16 Symbols. As before, the basic pattern (8‐Symbols now) is highlighted in grey. 

**Modified Compliance Pattern for 128b/130b.** This pattern consists of a repeating sequence of 65792 Blocks as listed here: 

1. One EIEOS Block 

2. 256 Data Blocks of 16 scrambled IDL Symbols (00h) each. 

**533** 

**PCI Ex ress Technolo p gy** 

3. 255 sets of the following sequence: 

   - One SOS 

   - 256 Data Blocks of 16 scrambled IDL Symbols each. 

Since the payload in the Data Blocks is all zeros, the output ends up being simply the output of the scrambler for that Lane. Recall that the scrambler doesn’t advance with the Sync Header bits and is initialized by the EIEOS. Since the scrambler seed value depends on the Lane number, it’s important that they be understood correctly. If Link training completed earlier but then software sent the LTSSM to this substate by setting the Enter Compli‐ ance bit in the Link Control 2 register, then the Lane numbers and polarity inversions that were assigned during training are used. If a Lane wasn’t active during training, or if this substate was entered in any other way, then the Lane numbers will be the default numbers assigned by the Port. Finally, note that the Data Blocks in this pattern don’t form a Data Stream and don’t have to follow the requirements for that (such as sending any SDS Ordered Sets or EDS Tokens). 

The thoughtful reader may be wondering about the absence of error status Symbols in this sequence that are prominent in the 8b/10b sequence. As it turns out, for 128b/130b they’re included inside the SOSs now. Recall that the last 2 bytes of the SOS are used to report the Receiver error count during Polling.Compliance (see “Ordered Set Example ‐ SOS” on page 426 for more on this). 

## _Entering Polling.Compliance:_ 

As was the case when entering Polling.Active, the Transmit Margin field of the Link Control 2 register is used to set the Transmitter voltage range that will be in effect while in this substate. 

The data rate and de‐emphasis level are determined as described below. Since many of the choices about these settings depend on the Link Control 2 register fields, that register is shown in Figure 14‐11 on page 536 for refer‐ ence. 

- If a Port only supports 2.5 GT/s, then that will be the data rate and the de‐ emphasis level will be ‐3.5dB. 

- Otherwise, if this substate was entered because 8 consecutive TS1s were received with the Compliance Receive bit set to 1b and the Loopback bit cleared to 0b (bits 4 and 2 of TS1 Symbol 5), then the rate will be the high‐ est common value for any Lane. The select_deemphasis variable must be set to match the Selectable De‐emphasis bit in TS1 Symbol 4. If the chosen rate is 8.0 GT/s, the select_preset variable on each Lane is taken from 

**534** 

**Chapter 14: Link Initialization & Training** 

Symbol 6 of the consecutive TS1s. For this Gen3 rate, Lanes that didn’t receive 8 consecutive TS1s with Transmitter Preset information can choose any value they support. 

- Otherwise, if the Enter Compliance bit is set in the Link Control 2 regis‐ ter, the compliance pattern is transmitted at the data rate given by the Target Link Speed field. If the rate will be 5.0 GT/s, the select_deemphasis variable is set if the Compliance Preset/De‐emphasis field equals 0001b. If the rate will be 8.0 GT/s, the select_preset variable of each Lane is cleared to 0b and the Transmitter must use the Compliance Preset/De‐emphasis value, as long as it isn’t a Reserved encoding. 

- Finally, if none of the other cases are true, then the data rate, preset, and de‐emphasis settings will cycle through a sequence based on the compo‐ nent’s maximum supported speed and the number of times Polling.Com‐ pliance is entered this way. The sequence is given in Table 14‐7 on page 535 and begins with Setting Number 1 the first time Polling.Compli‐ ance is entered, it increments through the list each time it’s re‐entered, and eventually repeats the pattern if it’s re‐entered more than 14 times. This provides a handy way to test all of a component’s supported set‐ tings: transition to Polling.Compliance, test that setting, transition back to Polling.Active, then back to Polling.Compliance again to test the next set‐ ting. A method for a load board to cause these transitions is described in the spec, and consists of sending a 100MHz, 350mVp‐p signal for about 1ms on one leg of a receiver’s differential pair. 

_Table 14‐7: Sequence of Compliance Tx Settings_ 

|Setting<br>Number|Data<br>Rate|De‐<br>emphasis|Tx Preset<br>Encoding|
|---|---|---|---|
|1|2.5|‐3.5|n/a|
|2|5.0|‐3.5|n/a|
|3|5.0|‐6.0|n/a|
|4|8.0|n/a|0000b|
|5|8.0|n/a|0001b|
|6|8.0|n/a|0010b|
|7|8.0|n/a|0011b|
|8|8.0|n/a|0100b|



**535** 

## **PCI Ex ress Technolo p gy** 

_Table 14‐7: Sequence of Compliance Tx Settings (Continued)_ 

|Setting<br>Number|Data<br>Rate|De‐<br>emphasis|Tx Preset<br>Encoding|
|---|---|---|---|
|9|8.0|n/a|0101b|
|10|8.0|n/a|0110b|
|11|8.0|n/a|0111b|
|12|8.0|n/a|1000b|
|13|8.0|n/a|1001b|
|14|8.0|n/a|1010b|



_Figure 14‐11: Link Control 2 Register_ 

**==> picture [316 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 Register<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


If the data rate won’t be 2.5 GT/s, then: 

- If any TS1s were sent during Polling.Active, the Transmitter must send either one or two consecutive EIOSs before going into Electrical Idle. 

- If no TS1s were sent in Polling.Active, the transmitter enters Electrical Idle without sending any EIOSs. 

- The Electrical Idle period must be >1ms and <2ms. During this time, the data rate is changed to the new speed and stabilized. If the rate will be 5.0 GT/s, the de‐emphasis level is given by the select_deemphasis variable 

**536** 

**Chapter 14: Link Initialization & Training** 

(0b = ‐3.5dB, 1b = ‐6.0 dB). If the rate will be 8.0 GT/s, then the select_preset variable gives the transmitter presets to use. 

## _During Polling.Compliance:_ 

Once the data rate and de‐emphasis or preset values have been determined, the following rules will apply: 

**Compliance Pattern.** If entry was not due to the Compliance Receive bit set and Loopback bit cleared in the TS Ordered Sets and was not due to both the Enter Compliance and Enter Modified Compliance bits being set in the Link Control 2 register, then Transmitters send the compliance pattern on all detected Lanes. 

## _Exit to “Polling.Active”_ 

If any of these conditions are true: 

- a) Electrical Idle exit is detected at the Receiver of any detected Lane and the Enter Compliance bit is cleared (0b).

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-7"></a>
## 12.7 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- The spec notes that the stipulation “any Lane” supports the Load Board usage model described earlier to allow the device to cycle through all the supported test cases. 

- b) The Enter Compliance bit has been cleared (0b) since Polling.Compli‐ ance was entered. 

- c) For an Upstream Port, the Enter Compliance bit is set (1b) and EIOS has been detected on any Lane. This condition clears the Enter Compliance bit (0b). 

If the data rate was not 2.5 GT/s or the Enter Compliance bit was set during entry to Polling.Compliance, the Transmitter sends 8 consecutive EIOSs and goes to Electrical Idle before transitioning to Polling.Active. During the Electrical Idle time the Port changes to 2.5 GT/s and stabilized for a time between 1ms and 2ms. 

Sending multiple EIOSs helps ensure that the Link partner will detect at least one and exit Polling.Compliance when the Enter Compliance register bit was used for entry 

**Modified Compliance Pattern.** If Polling.Compliance was entered because TS1s directed it, and either the Compliance Receive bit was set and Loopback bit was cleared or both Enter Compliance and Enter Modified Compliance bits were set in Link Control 2 register then send the Modified Compliance Pattern on all detected Lanes with the error status Symbol cleared to all zeroes. 

**537** 

**PCI Ex ress Technolo p gy** 

If the rate is 2.5 or 5.0 GT/s, each Lane indicates a successful lock on the incoming pattern by looking for one instance of the Modified Compliance Pattern and then setting the Pattern Lock bit in the Modified Compliance Pattern that it sends back (bit 7 of the 8‐bit error status Symbol). 

- The error status Symbols cannot be used in the locking process because they don’t have meaning if the Link partner isn’t already locked and therefore their meaning can be undefined. 

- An instance of the pattern is defined to be the sequence of 4 Symbols described earlier: K28.5, D21.5, K28.5, and D10.2 or the complement of these Symbols (meaning the polarity is inverted). 

- The device under test must set the Pattern Lock bit in the Modified Compliance Patterns it sends within 1ms of receiving the Modified Compliance Pattern from the Link partner. 

- Any Receiver errors on a Lane increment that Lane’s error count by 1, and it saturates when the count reaches 127 (doesn’t go higher or wrap around). 

If the rate is 8.0 GT/s 

- The Error_Status field is set to 00h on entry to this substate. 

- The device under test must set the Pattern Lock bit in the Modified Compliance Patterns it sends within 4ms of receiving the Modified Compliance Pattern from the Link partner. 

- Each Lane independently sets Pattern Lock when it achieves Block Alignment. After that, Symbols in Data Blocks are expected to be IDLs (00h) and any mismatched Symbols increment the count by 1. The Receiver Error Count saturates at 127, and is sent in the last 2 Symbols of the SOS’s included in this pattern. 

- The scrambling requirements are applied as usual to the Modified Compliance Pattern: the seed value is set per Lane, an EIEOS initiates the LFSR, and SOS’s don’t advance the LFSR. 

- The spec notes that devices should wait long enough before acquiring Block alignment to ensure that their Receivers have stabilized and won’t see any bit slips. It even mentions that devices might want to re‐ validate their Block alignment before setting the Pattern Lock bit. 

## _Exit to “Polling.Active”_ 

If the Enter Compliance bit was set (1b) on entry to Polling.Compliance and either the Enter Compliance bit has been cleared (0b), or it’s an Upstream Port and received an EIOS on any Lane. This also causes its Enter Compliance bit to be cleared (0b). 

**538** 

**Chapter 14: Link Initialization & Training** 

If the data rate was not 2.5 GT/s or the Enter Compliance bit was set during entry to Polling.Compliance, the Transmitter sends 8 consecu‐ tive EIOSs and goes to Electrical Idle before transitioning to Poll‐ ing.Active. During the Electrical Idle time the Port changes to 2.5 GT/s and ‐3.5dB de‐emphasis, and this time must be between 1ms and 2ms. 

Sending multiple EIOSs helps ensure that the Link partner will detect at least one and exit Polling.Compliance when the Enter Compliance reg‐ ister bit was used for entry. 

## _Exit to “Detect State”_ 

If the Enter Compliance bit in the Link Control 2 register is cleared (0b) and the device is directed to exit this substate. 

_Figure 14‐12: Link Control 2 Register’s “Enter Compliance” Bit_ 

**==> picture [301 x 168] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 Register<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


## **Configuration State** 

Initially, the Configuration state performs Link and Lane Numbering at the 2.5 GT/s rate; however, provisions exist that allow the 5 GT/s and 8 GT/s devices to also enter the Configuration state from the Recovery state. The transition from Recovery to Configuration is done primarily for making dynamic changes in the link width of multi‐lane devices. The dynamic changes are supported for the 5 GT/s and 8 GT/s devices only. Consequently, the detailed state transitions for these devices appear in the detailed Configuration Substate descriptions beginning on page 552. 

**539** 

**PCI Ex ress Technolo p gy** 

## **Configuration State — General** 

The main goal of this state is to discover how the Port has been connected and assign Lane numbers for it. For example, 8 Lanes may be available but only 2 are active, or perhaps the Lanes can be split into multiple Links, such as two x4 Links. Unlike the other states, Ports have defined roles that depend on whether they are facing upstream or downstream. For that reason, the description of these substates is grouped into the behavior for Downstream Lanes and for Upstream Lanes. The Downstream Port (port that transmits downstream) plays the “leader” role on this Link to walk through the rest of the states in the link initialization process. The Upstream Port (port that transmits upstream) plays the “follower” role. The leader, or Downstream Port, will specify the Link and Lane numbers to the Upstream Port, and the Upstream Port will simply reply with the same values it was told, unless there is a conflict, as we will see in this section. The Link and Lane numbers are reported in the fields of the TS1s exchanged during this time, as shown again in Figure 14‐13 on page 540. These fields contain PAD symbols as a placeholder until actual values are assigned. 

_Figure 14‐13: Link and Lane Number Encoding in TS1/TS2_ 

**==> picture [292 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM K28.5<br>1 Link # 0 - 255 = D0.0 - D31.7,   PAD = K23.7<br>2 Lane # 0 - 31 = D0.0 - D17.1,   PAD = K23.7<br>3 # FTS # of FTSs required by Receiver for L0s recovery<br>4 Rate ID Bit 1 must be set, indicates 2.5 GT/s support<br>5 Train Ctl<br>6 TS ID or Equalization info when<br>changing to 8.0 GT/s, else<br>9 EQ Info TS1 or TS2 Identifier<br>10<br>TS1 Identifier = D10.2<br>TS ID<br>TS2 Identifier = D5.2<br>15<br>**----- End of picture text -----**<br>


**540** 

**Chapter 14: Link Initialization & Training** 

## **Designing Devices with Links that can be Merged** 

A designer chooses how many Lanes to implement on a given Link based on performance and cost requirements. Narrow Links may optionally be able to combine into a wider Link, and a wide Link can optionally be split into multiple narrower Links. Figure 14‐14 on page 541 shows a Switch with one Upstream Port and four x2 Downstream Ports. In this example, they can also be grouped into two x4 Links. As a reminder, the spec requires that every Port must also support operating as a x1 Link. 

As seen on the left side of the figure, the switch internally consists of one upstream logical bridge and four downstream logical bridges. One bridge is required for each Port, so supporting 4 Downstream Ports requires 4 down‐ stream bridges. However, if the Ports are combined as shown on the right side of the diagram, then some of the bridges simply go unused. During Link Train‐ ing, the LTSSM of each Downstream Port determines which of the supported connection options is actually implemented. 

_Figure 14‐14: Combining Lanes to Form Wider Links (Link Merging)_ 

**==> picture [378 x 204] intentionally omitted <==**

**----- Start of picture text -----**<br>
x8<br>x8<br>Switch Switch<br>Virtual Virtual<br>PCI PCI<br>Bridge 0 Bridge 0<br>OR<br>Virtual Virtual Virtual Virtual Virtual Virtual<br>PCI PCI PCI PCI PCI PCI<br>Bridge 1 Bridge 2 Bridge 3 Bridge 4 Bridge 1 Bridge 2<br>x2 x2 x2 x2<br>x4 x4<br>**----- End of picture text -----**<br>


**541** 

**PCI Ex ress Technolo p gy** 

## **Configuration State — Training Examples** 

## **Introduction** 

In the Configuration state, the Link and Lane numbering process is initiated by a Downstream Port, the “leader,” (e.g., Root Port or Switch Downstream Port). Endpoints and switch Upstream Ports don’t initiate, but respond. They are the “follower.” Let’s now consider some examples to make the concepts easier to understand. 

## **Link Configuration Example 1** 

The devices shown in Figure 14‐15 on page 543 both support a single Link that implements lane sizes of x4, x2, or x1. The Lane number assignments are fixed by the device internally and must be sequential starting from zero. The physical Lane numbers are shown within the device box and the reported, or logical, Lane numbers are reported by the TS Ordered Sets. Usually, these will be the same, but not in every case. 

## **Link Number Negotiation.** 

1. Since only one Link is possible in this example, the Downstream Port (the Port that transmits downstream) sends TS1s using the same Link Number, _N_ , for all the Lanes and PAD for the Lane Numbers. 

2. In this Configuration state, the Upstream Port starts out sending TS1s with PAD in the Link and Lane number fields, but upon receiving the TS1s from the Downstream Port with the non‐PAD Link number, the Upstream Port responds with TS1s on all connected Lanes that reflect the same Link Number _N_ and PAD for the Lane Number field. Based on this response, the Downstream LTSSM recognizes that four Lanes responded and used the same Link number as is being sent, so all 4 Lanes will be configured as one Link. The Link Number itself is an implementation‐specific value that isn’t stored in any defined configu‐ ration register and isn’t related to the Port Number or any other value. 

**542** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐15: Example 1 ‐ Steps 1 and 2_ 

**==> picture [298 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 1<br>Lane # PAD PAD PAD PAD<br>TS1s<br>Link # N N N N<br>N N N N Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 2 3 Step 2<br>(Upstream Port)<br>LTSSM<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Lane Number Negotiation.** 

3. The Downstream Port now begins to send TS1s with the same Link Number but assigns Lane Numbers of 0, 1, 2 and 3 to the connected Lanes, as shown in Figure 14‐16 on page 544.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-12-8"></a>
## 12.8 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

4. In response to seeing non‐PAD Lane numbers coming in, the Upstream Port will verify that the incoming Lane numbers match the Lane num‐ bers they are received on. In this example, the Lanes of the Downstream and Upstream Ports are connected correctly. Because all the Lane num‐ bers match, the Upstream Port advertises its Lane numbers in the TS1s it is sending as well. When the Downstream Port sees non‐PAD Lane numbers in response, it compares the incoming numbers to the values it’s sending. If they match, all is well but, if not, then other steps will need to be taken. If some but not all Lane numbers match, then the Link width may be adjusted accordingly. If the Lanes are reversed, then the optional Lane Reversal feature will be needed. Because it’s optional, it’s possible that the Lanes have been reversed but neither device is capable of correcting it. This would be a dramatic board design error because it is possible the Link cannot be configured for operation in this case. 

**543** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐16: Example 1 ‐ Steps 3 and 4_ 

**==> picture [356 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 3<br>Lane # 0 1 2 3<br>TS1s<br>Link # N N N N<br>N N N N Link #<br>TS1s<br>0 1 2 3 Lane #<br>0 1 2 3 Step 4<br>(Upstream Port)<br>LTSSM<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Confirming Link and Lane Numbers.** 

5. Since the transmitted and received Link and Lane numbers matched on all the Lanes, the Downstream Port indicates it is ready to conclude this negotiation and proceed to the next state, L0, by sending TS2 Ordered Sets with the same Link and Lane numbers. 

6. Upon receiving TS2s with the same Link and Lane numbers, the Upstream Port also indicates its readiness to leave the Configuration state and proceed to L0 by sending TS2s back. This is shown in Figure 14‐17 on page 545. 

7. Once a Port receives at least 8 TS2s and transmits at least 16, it sends some logical idle data and then transitions to L0. 

**544** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐17: Example 1 ‐ Steps 5 and 6_ 

**==> picture [345 x 215] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 5<br>Lane # 0 1 2 3<br>TS2s<br>Link # N N N N<br>N N N N Link #<br>TS2s<br>0 1 2 3 Lane #<br>0 1 2 3 Step 6<br>LTSSM<br>(Upstream Port)<br>**----- End of picture text -----**<br>


Options: One Link x4, x2 or x1 

## **Link Configuration Example 2** 

Another example that should be covered is of a Device with 4 Downstream Lanes that is capable of being configured as a single x4 Link or a combination of two x2 Links or four x1 Links. So even a configuration of one x2 Link and two x1 Links would be just fine. An example of this type of Device can be seen in Fig‐ ure 14‐18 on page 546. 

If all four Lanes have detected a receiver and made it to the Configuration state, there are a number of connection possibilities: 

- One x4 Link 

- Two x2 Links 

- One x2 Link and two x1 Links 

- Four x1 Links 

One example method defined in the spec to determine which of the configura‐ tions are implemented is described below. 

**545** 

**PCI Ex ress Technolo p gy** 

## **Link Number Negotiation.** 

1. In this example method, the Downstream Port begins by advertising a unique Link number on each Lane. Lane 0 advertises a Link number of N, Lane 1 advertises a Link number of N+1, etc. as shown in Figure 14‐ 18 on page 546. These Link numbers are just examples, and they do not have to be sequential. Also, it is important to remember that the Down‐ stream Port does not know what it is connected to and it is this process where the Port is trying to determine the connections for each Lane. 

_Figure 14‐18: Example 2 ‐ Step 1_ 

**==> picture [298 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>Two Links x2 or x1<br>Four Links x1<br>LTSSM<br>(Downstream Port)<br>Step 1 0 1 2 3<br>Lane # PAD PAD PAD PAD<br>TS1s<br>Link # N N+1 N+2 N+3<br>PAD PAD PAD PAD Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 1 0<br>(Upstream (Upstream<br>Port) Port)<br>LTSSM LTSSM<br>Options: Options:<br>One Link x2 or x1 One Link x2 or x1<br>**----- End of picture text -----**<br>


2. Upon receiving the returned TS1s, the Downstream Port recognizes two things: all four Lanes are working and they are connected to two differ‐ ent Upstream Ports. This means there will actually be _two_ Downstream Ports. Each Downstream Port will have its own Lane 0 and Lane 1 as shown in Figure 14‐20 on page 548. 

**546** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐19: Example 2 ‐ Step 2_ 

**==> picture [286 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>Two Links x2 or x1<br>Four Links x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Lane # 0 PAD PAD PAD<br>TS1s<br>Link # N N+1 N+2 N+3<br>N N N+2 N+2 Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 1 0 Step 2<br>(Upstream (Upstream<br>Port) Port)<br>LTSSM LTSSM<br>Options: Options:<br>One Link x2 or x1 One Link x2 or x1<br>**----- End of picture text -----**<br>


## **Lane Number Negotiation.** 

3. The process continues now for each Link independently but they’ll take the same steps as before to determine the Lane numbers: the Down‐ stream Ports will advertise their Lane numbers in the TS1s. It is also important to note that the Downstream Ports begin advertising the sin‐ gle returned Link number for all Lanes of the Link. The Link on the left is advertising a Link number of N for both Lanes and the Link on the right is advertising N+2. 

4. In this example, the Lane numbers of the Link on the left match between the Downstream and Upstream Port. However, for the Link on the right, the Lane numbers of the Downstream Port are reversed from the connected Upstream Port. The Upstream Port realizes this and if it supports Lane Reversal, it will implement that internally and reply back with the same Lane numbers that were advertised by the Down‐ stream Port, as shown in Figure 14‐20. If the Upstream Port did not sup‐ port Lane Reversal, it would have advertised its own Lane numbers in 

**547** 

## **PCI Ex ress Technolo p gy** 

   - the returned TS1s and then the Downstream Port would have realized the issue and had a chance to implement Lane Reversal. 

5. Lane Reversal can optionally be handled by either Port. If the Upstream Port detects this case and supports Lane Reversal, it simply makes the Lane assignment change internally and returns TS1s with the proper Lane numbers. As a result, the Downstream Port is unaware that there was ever an issue. If the Upstream Port is unable to handle Lane Rever‐ sal though, then the Downstream Port will see the incoming Lane num‐ bers in reverse order. If it supports Lane Reversal, it will then correct the numbering and begin sending TS2s with the new Lane numbers. 

_Figure 14‐20: Example 2 ‐ Steps 3, 4 and 5_ 

**==> picture [370 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Step 3<br>LTSSM LTSSM<br>(Downstream (Downstream<br>Port) Port)<br>0 1 0 1<br>Step 4<br>Lane # 0 1 0 1<br>TS1s<br>Link # N N N+2 N+2<br>N N N+2 N+2 Link #<br>TS1s<br>0 1 0 1 Lane #<br>0 1 1 0 Step 5<br>(Upstream (Upstream<br>Lane Reversal<br>Port) Port)<br>LTSSM LTSSM<br>**----- End of picture text -----**<br>


## **Confirming Link and Lane Numbers.** 

6. The Downstream Ports receive the TS1s with the Link and Lane num‐ bers that match what was advertised so each Port, independently, starts sending TS2s as a notification that it is ready to proceed to the L0 state with the negotiated settings. 

**548** 

**Chapter 14: Link Initialization & Training** 

7. The Upstream Ports receive the TS2s with no Link and Lane number changes and start transmitting TS2s in return with the same values. 

8. Once each Port receives at least 8 TS2s and transmits at least 16 TS2s, it sends some logical idle data and then transitions to L0. The Upstream Port of the Link on the right is implementing Lane Reversal internally. 

## **Link Configuration Example 3: Failed Lane** 

Finally, let’s consider what happens if one of the Lanes isn’t working properly. Consider an example in which Lane 2 of the Upstream Port is not functioning well as shown in Figure 14‐21 on page 550. It’s important to note that the Lane isn’t physically broken because if it were it wouldn’t have detected a Receiver and wouldn’t be considered for inclusion in the Link. However, even though the Lane is attached, either the Transmitter or Receiver (or both) of Lane 2 on the Upstream Port is not getting the job done. 

In cases like this, it is likely that the link training process will take considerably longer because most of the state transitions wait to proceed to the next state until ALL Lanes are ready for the next state, OR if a subset of Lanes are ready and a timeout condition has occurred. 

The steps below indicate a way this situation could be handled when transition‐ ing through the substates of the Configuration state machine. 

## **Link Number Negotiation.** 

9. Even though the Lane 2 Receiver on the Upstream Port is having issues, the Downstream Port is going to take the same process upon entering the Configuration state. The Downstream Port sends TS1s on all Lanes with the Link number N and with the Lane number set to PAD. 

10. Lanes 0, 1 and 3 all received the TS1s with the non‐PAD Link number, so those Lanes send TS1s back to the Downstream Port. However, Lane 2 of the Upstream Port did not successfully receive the TS1s with the non‐PAD Link number, so its Transmitter continues sending TS1s with PAD in the Link and Lane number fields as shown in Figure 14‐21 on page 550. 

**549** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐21: Example 3 ‐ Steps 1 and 2_ 

**==> picture [356 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 1<br>Lane # PAD PAD PAD PAD<br>TS1s<br>Link # N N N N<br>N N PAD N Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 2 3 Step 2<br>LTSSM<br>(Upstream Port)<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Lane Number Negotiation.** 

11. Once the Downstream Port has received the TS1s with the same Link number on Lanes 0, 1 and 3, it waits until the required timeout period hoping that Lane 2 will start working. When that doesn’t happen, the Downstream Port realizes that it will only be able to train as a x2 Link. After accepting this fact, the Downstream Port will advertise its Lane numbers for Lanes 0 and 1, but Lanes 2 and 3 go back to send PADs in the Link and Lane number fields. 

12. When the Upstream Port receives the TS1s on Lanes 0 and 1 with the advertised Lane numbers and it sees that Lane 3 has gone back to receiving PAD TS1s, it advertises its Lane number for Lanes 0 and 1 but all the other Lanes start (or continue) sending TS1s with PAD set in both the Lane and Link number fields as shown in Figure 14‐22 on page 551. 

**550** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐22: Example 3 ‐ Steps 3 and 4_ 

**==> picture [356 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 3<br>Lane # 0 1 PAD PAD<br>TS1s<br>Link # N N PAD PAD<br>N N PAD PAD Link #<br>TS1s<br>0 1 PAD PAD Lane #<br>0 1 2 3 Step 4<br>LTSSM<br>(Upstream Port)<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Confirming Link and Lane Numbers.**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
