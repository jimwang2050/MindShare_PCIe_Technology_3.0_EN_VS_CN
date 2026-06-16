For multi‐Lane Links, the difference in arrival times between lanes is automati‐ cally corrected at the Receiver by delaying the early arrivals until they all match up. The spec allows this to be accomplished by any means a designer prefers, but using a digital delay after the elastic buffer has one advantage in that the arrival time differences are now digitized to the local Symbol clock of the receiver. If the input to one lane makes it on a clock edge and another one doesn’t, the difference between them will be measured in clock periods, so the early arrival can simply be delayed by the appropriate number of clocks to get it to line up with the late‐comers (see Figure 12‐22 on page 444). The fact that the maximum allowable skew at the receiver is a multiple of the clock periods makes this easy and infers that the spec writers may have had this implementa‐ tion in mind. As defined in the spec, the receiver must be capable of de‐skewing up to 20ns for Gen1 (5 Symbol‐time clocks at 4ns per Symbol) and 8ns for Gen2 (4 Symbol‐time clocks at 2ns per Symbol), and 6ns for Gen3 (6 Symbol‐time clocks at 1ns per Symbol). 

## **De-skew Opportunities** 

The same Symbol must be seen on all lanes at the same time to perform de‐ skewing, and any Ordered Set will do. However, de‐skewing is only performed in the L0s, Recovery, and Configuration LTSSM states. In particular, it must be completed as a condition for: 

- Leaving Configuration.Complete 

- Beginning to process a Data Stream after leaving Configuration.Idle or Recovery.Idle 

- Leaving Recovery.RcvrCfg 

- Leaving Rx_L0s.FTS 

**442** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

If skew values change while in L0 (based on temperature or voltage changes, for example), a Receiver error may occur and cause replayed TLPs. If the problem becomes persistent, the Link would eventually transition to the Recovery state and de‐skewing would take place there. The spec notes that, while devices are not allowed to de‐skew their Lanes while in L0, the SOSs that must be sent peri‐ odically in this state contain an LFSR value that is intended to aid external tools in doing this. These tools, unconstrained by the rules for Data Streams, can search for the SOSs and use the patterns to achieve Bit Lock, Block Alignment and Lane‐to‐Lane de‐skew in the midst of a Data Stream. 

The spec notes that when leaving L0s the Transmitter will send an EIEOS, then the correct number of FTSs with another EIEOS inserted after every 32 FTSs, then one last EIEOS to assist with Block Alignment and, finally, an SDS Ordered Set for the purpose of de‐skewing in addition to starting the Data Stream. 

## **Receiver Lane-to-Lane De-skew Capability** 

Understandably, the transmitter is only allowed to introduce a minimal amount of skew so as to leave the rest of the skew budget to cover routing differences and other variations. The amount of allowed skew that can be corrected at the Receiver is shown in Table 12‐5 on page 443, where it can be seen that this skew corresponds easily to a number of Symbol times for Gen3 just as it did for the earlier data rates. That allows the same option of using delay registers to accom‐ plish de‐skew after the elastic buffer as was described for Gen1/Gen2 Physical Layer implementations earlier. 

_Table 12‐5: Signal Skew Parameters_ 

||Gen1|Gen2|Gen3|
|---|---|---|---|
|Tx max skew|1.3 ns|1.3 ns|1.1 ns|
|Rx max skew|20 ns|8 ns|6 ns|
|Symbol time period|4ns|2ns|1ns|
|Rx skew expressed<br>in Symbol Times|5|4|6|



When using 8b/10b encoding, an unambiguous de‐skew mechanism is to watch for the COM control character, which must appear on all Lanes simultaneously. That option is not available for 128b/130b, but Ordered Sets still arrive at the same time on all the Lanes, such as the SOS, SDS, and EIEOS. As a result, the process can be very much the same even though the pattern to search for when de‐skewing the Lanes is different. 

**443** 

**PCI Ex ress Technolo p gy** 

_Figure 12‐22: Receiver Link De‐Skew Logic_ 

**==> picture [374 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOS, SDS, SOS, SDS,<br>Lane 0 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>Lane 1 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>Lane 2 Rx EIEOS Delay EIEOS<br>(symbols)<br>SOS, SDS, SOS, SDS,<br>EIEOS EIEOS<br>Lane 3 Rx Delay<br>(symbols)<br>SYNC SYNC<br>SYNC SYNC<br>SYNC SYNC<br>SYNC SYNC<br>**----- End of picture text -----**<br>


## **Descrambler** 

## **General** 

Receivers follow exactly the same rules for generating the scrambling polyno‐ mial that the Transmitter does and simply XOR the same value to the input data a second time to recover the original information. Like on the transmit side, they are allowed to implement a separate LFSR for each Lane or just one. 

## **Disabling Descrambling** 

Unlike at Gen1/Gen2 data rates, in Gen3 mode, descrambling cannot be dis‐ abled because of its role in facilitating clock recovery and signal integrity. At the lower rates, the “disable scrambling” bit in the control byte of TS1s and TS2s would be used to inform a Link neighbor that scrambling was being turned off. That bit is reserved for rates of 8.0 GT/s and higher. 

**444** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **Byte Un-Striping** 

This logic is basically unchanged from Gen1 or Gen2 implementation. At some point, the byte streams for Gen3 and for the lower data rates will have to muxed together, and the example in Figure 12‐23 on page 445 shows that happening just before the un‐striping logic. 

_Figure 12‐23: Physical Layer Receive Logic Details_ 

**==> picture [272 x 358] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


**445** 

**PCI Ex ress Technolo p gy** 

## **Packet Filtering** 

The serial byte stream supplied by the byte un‐striping logic contains TLPs, DLLPs, Logical Idles (IDLs), and Ordered Sets. The Logical Idle bytes and Ordered Sets are eliminated here and are not forwarded to the Data Link layer. What remains are the TLPs and DLLPs, which get forwarded along with an indicator of their packet type. 

## **Receive Buffer (Rx Buffer)** 

The Rx Buffer holds received TLPs and DLLPs until the Data Link Layer is able to accept them. The interface to the Data Link Layer is not described in the spec, and so a designer is free to choose details like the width of this bus. The wider the path, the lower the clock frequency will be, but more signals and logic will be needed to support it. 

## **Notes Regarding Loopback with 128b/130b** 

The spec makes a special point to describe the operation of Loopback Mode at the higher rate. The basic rules can be summarized as follows: 

- Loopback masters must send actual Ordered Sets or Data Blocks, but they aren’t required to follow the normal protocol rules when changing from Data Blocks to Ordered Sets or vice versa. In other words, the SDS Ordered Set and EDS token are not required. Slaves must not expect or check for the presence of them. 

- Masters must send SOS as usual, and must allow for the number of SKP Symbols in the loopback stream to be different because the receiver will be performing clock compensation. 

- Loopback slaves are allowed to modify the SOS by adding or removing 4 SKP Symbols at a time as they normally would for clock compensa‐ tion, but the resulting SOS must still follow the proper format rules. 

- Everything should be looped back exactly as it was sent except for SOS which can change as just described, and both EIEOS and EIOS which have defined purposes in loopback and should be avoided. 

- If a slave is unable to acquire Block alignment, it won’t be able to loop back all bits as received and is allowed to add or remove Symbols as needed to continue operation. 

**446** 

## _**13 Physical Layer ‐ Electrical**_ 

## **The Previous Chapter** 

The previous chapter describes the logical Physical Layer characteristics for the third generation (Gen3) of PCIe. The major change includes the ability to double the bandwidth relative to Gen2 speed without needing to double the frequency (Link speed goes from 5 GT/s to 8 GT/s). This is accomplished by eliminating 8b/10b encoding when in Gen3 mode. More robust signal compensation is nec‐ essary at Gen3 speed. Making these changes is more complex than might be expected. 

## **This Chapter** 

This chapter describes the Physical Layer electrical interface to the Link, includ‐ ing some low‐level characteristics of the differential Transmitters and Receivers. The need for signal equalization and the methods used to accomplish it are also discussed here. This chapter combines electrical transmitter and receiver char‐ acteristics for both Gen1, Gen2 and Gen3 speeds. 

## **The Next Chapter** 

The next chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process of the Link is described from Power‐On or Reset until the Link reaches the fully‐operational L0 state during which normal packet traffic occurs. In addition, the Link power management states L0s, L1, L2, L3 are discussed along with the causes of transi‐ tions between the states. The Recovery state during which bit lock, symbol lock or block lock can be re‐established is described. 

**447** 

**PCI Ex ress Technolo p gy** 

## **Backward Compatibility** 

The spec begins the Physical Layer Electrical section with the observation that newer data rates need to be backward compatible with the older rates. The fol‐ lowing summary defines the requirements: 

- Initial training is done at 2.5 GT/s for all devices. 

- Changing to other rates requires negotiation between the Link partners to determine the peak common frequency. 

- Root ports that support 8.0 GT/s are required to support both 2.5 and 5.0 GT/s as well. 

- Downstream devices must obviously support 2.5 GT/s, but all higher rates are optional. This means that an 8 GT/s device is not required to support 5 GT/s. 

In addition, the optional Reference clock (Refclk) remains the same regardless of the data rate and does not require improved jitter characteristics to support the higher rates. 

In spite of these similarities, the spec does describe some changes for the 8.0 GT/ s rate: 

- **ESD standards:** Earlier PCIe versions required all signal and power pins to withstand a certain level of ESD (Electro‐Static Discharge) and that’s true for the 3.0 spec, too. The difference is that more JEDEC standards are listed and the spec notes that they apply to devices regardless of which rates they support. 

- **Rx powered‐off Resistance:** The new impedance values specified for 8.0 GT/s (ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG) will be applied to devices supporting 2.5 and 5.0 GT/s as well. 

- **Tx Equalization Tolerance:** Relaxing the previous spec tolerance on the Tx de‐emphasis values from +/‐ 0.5 dB to +/‐ 1.0 dB makes the ‐3.5 and ‐6.0 dB de‐emphasis tolerance consistent across all three data rates. 

- **Tx Equalization during Tx Margining:** The de‐emphasis tolerance was already relaxed to +/‐ 1.0 dB for this case in the earlier specs. The accuracy for 8.0 GT/s is determined by the Tx coefficient granularity and the TxEQ tolerances for the Transmitter during normal operation. 

- **VTX‐ACCM and VRX‐ACCM:** For 2.5 and 5.0 GT/s these are relaxed to 150 mVPP for the Transmitter and 300 mVPP for the Receiver. 

**448** 
