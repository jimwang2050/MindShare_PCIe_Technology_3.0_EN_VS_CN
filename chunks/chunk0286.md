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
