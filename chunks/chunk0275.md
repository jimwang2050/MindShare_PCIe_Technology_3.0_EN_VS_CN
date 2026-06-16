- Receivers must check to see that every SOS in a Data Stream is preceded by a Data Block that ends with EDS. 

## **Scrambling** 

The scrambling logic for 128b/130b is modified from the previous PCIe genera‐ tions to address the two issues that 8b/10b encoding handled automatically: maintaining DC Balance and providing a sufficient transition density. By way of review, recall that DC Balance means the bit stream has an equal number of ones and zeros. This is intended to avoid the problem of “DC wonder”, in which the transmission medium is charged toward one voltage or the other so much, by a prevalence of ones or zeros, that it becomes difficult to switch the signal within the necessary time. The other problem is that clock recovery at the Receiver needs to see enough edges in the input signal to be able to compare them to the recovered clock and adjust the timing and phase as needed. 

Without 8b/10b to handle these issues, three steps were taken: First, the new scrambling method improves both transition density and DC Balance over longer time periods, but doesn’t guarantee them over short periods the way 8b/ 10b did. Second, the TS1 and TS2 Ordered Set patterns used during training include fields that are adjusted as needed to improve DC Balance. And third, Receivers must be more robust and tolerant of these issues than they were in the earlier generations. 

## **Number of LFSRs** 

At the lower data rates every Lane was scrambled in the same way, so a single Linear‐Feedback Shift Register (LFSR) could supply the scrambling input for all of them. For Gen3, though, the designers wanted different scrambling values for neighboring Lanes. The reasons probably include a desire to decrease the possibility of cross‐talk between the Lanes by scrambling their outputs with respect to each other and avoid having the same value on each Lane, as might 

**430** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

happen when sending IDLs. The spec describes two approaches to achieving this goal, one that emphasizes lower latency and one that emphasizes lower cost. 

**First Option: Multiple LFSRs.** One solution is to implement a separate LFSR for each Lane, and initialize each with a different starting value or “seed”. This has the advantage of simplicity and speed, at the cost of add‐ ing logic. As shown in Figure 12‐16, each LFSR creates a pseudo‐random output based on the polynomial given in the spec as G(X) = X[23] + X[21] + X[16] + X[8] + X[5] + X[2] + 1. This polynomial is longer than the previous version and also behaves a little differently because of the different seed values. Eight different seed values for each Lane are specified requiring eight different LFSRs, one per Lane 0 through 7. 

_Figure 12‐16: Gen3 Per‐Lane LFSR Scrambling Logic_ 

**==> picture [369 x 155] intentionally omitted <==**

**----- Start of picture text -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>+ + +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+ +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>Data In + Data Out<br>**----- End of picture text -----**<br>


The 24‐bit seed value for each Lane is listed in Table 12‐3 on page 432. The series repeats itself, meaning the seed for Lane 8 will be the same as Lane 0, so only the first 8 values are shown. Every Lane uses the same LFSR and the same tap points to create the scrambling output, and the different seed val‐ ues give the desired difference. 

**431** 

## **PCI Ex ress Technolo p gy** 

_Table 12‐3: Gen3 Scrambler Seed Values_ 

|**Lane**|**Seed Value**|
|---|---|
|0|1DBFBCh|
|1|0607BBh|
|2|1EC760h|
|3|18C0DBh|
|4|010F12h|
|5|19CFC9h|
|6|0277CEh|
|7|1BB807h|



**Second Option: Single LFSR.** The alternative solution, illustrated in Figure 12‐17 on page 433 for Lanes 2, 10, 18, and 26, is to use just one LFSR and create the scrambling inputs for each Lane by XORing different tap points together. Since there’s only one LFSR, the seed value is the same for all Lanes (all ones), but the scrambling “Tap Equation” for each Lane is derived by combining different tap points, as shown in Table 12‐4 on page 433. The spec also notes that 4 of the Lanes Tap Equations can be derived by XORing the tap values of their bit neighbors: 

- Lane 0 = Lane 7 XOR Lane 1 (note that the process of going to lower Lane numbers wraps around, with the result that Lane 7 is considered lower that Lane 0) 

- Lane 2 = Lane 1 XOR Lane 3 

- Lane 4 = Lane 3 XOR Lane 5 

- Lane 6 = Lane 5 XOR Lane 7 

The single‐LFSR solution uses fewer gates than the multi‐LFSR version does, but incurs extra latency through the XOR process, providing a differ‐ ent cost/performance option. 

**432** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐17: Gen3 Single‐LFSR Scrambler_ 

**==> picture [378 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>+ + +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+ +<br>Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed Seed<br>D12 D13 D14 D15 D16 D17 D18 D19 D20 D21 D22<br>+<br>“Tap Equation” for Lanes 2, 10, 18, and 26<br>Data In + Data Out<br>(for Lanes 2, 10, 18, or 26)<br>**----- End of picture text -----**<br>


_Table 12‐4: Gen3 Tap Equations for Single‐LFSR Scrambler_ 

|**Lane Numbers**<br>**T**|**ap Equation**|
|---|---|
|0, 8, 16, 24<br>|D9 xor D13|
|1, 9, 17, 25<br>|D1 xor D13|
|2, 10, 18, 26<br>|D13 xor D22|
|3, 11, 19, 27<br>|D1 xor D22|
|4, 12, 20, 28<br>|D3 xor D22|
|5, 13, 21, 29|D1 xor D3|
|6, 14, 22, 30|D3 xor D9|
|7, 15, 23, 31|D1 xor D9|



## **Scrambling Rules** 

The Gen3 scrambler LFSRs (whether one or more) do not continually advance, but only advance based on what is being sent. The scramblers must be re‐initial‐ ized periodically and that takes place whenever an EIEOS or FTSOS is seen. The spec gives several rules for scrambling that are listed here for convenience: 

**433** 

## **PCI Ex ress Technolo p gy** 

- Sync Header bits are not scrambled and do not advance the LFSR. 

- The Transmitter LFSR is reset when the last EIEOS Symbol has been sent, and the Receiver LFSR is reset when the last EIEOS Symbol is received. 

- TS1 and TS2 Ordered Sets: 

   - Symbol 0 bypasses scrambling 

   - Symbols 1 to 13 are scrambled 

   - Symbols 14 and 15 may or may not be scrambled. The spec states that they will bypass scrambling if necessary to improve DC Balance, but otherwise will be scrambled (see “TS1 and TS2 Ordered Sets” on page 510 for more details on how DC Balance is maintained). 

- All Symbols of the Ordered Sets FTS, SDS, EIEOS, EIOS, and SOS bypass scrambling. Despite this, the output data stream will have sufficient transi‐ tion density to allow clock recovery and the symbols chosen for the Ordered Sets result in a DC balanced output. 

- Even when bypassed, Transmitters advance their LFSRs for all Ordered Set Symbols except for those in the SOS. 

- Receivers do the same, checking Symbol 0 of an incoming Ordered Set to see whether it is an SOS. If so, the LFSRs are not advanced for any of the Symbols in that Block. Otherwise the LFSRs are advanced for all the Sym‐ bols in that Block. 

- All Data Block Symbols are scrambled and advance the LFSRs. 

- Symbols are scrambled in little‐endian order, meaning the least‐significant bit is scrambled first and the most‐significant bit is scrambled last. 

- The seed value for a per‐Lane LFSR depends on the Lane number assigned to the Lane when the LTSSM first entered Configuration.Idle (having fin‐ ished the Polling state). The seed values, modulo 8, are shown in Table 12‐3 on page 432 and, once assigned, won’t change as long LinkUp = 1 even if Lane assignments are changed by going back to the Configuration state. 

- Unlike 8b/10b, scrambling cannot be disabled while using 128b/130b encod‐ ing because it is needed to help with signal integrity. It’s not expected that the Link would operate reliably without it, so it must always be on. 

- A Loopback Slave must not scramble or de‐scramble the looped‐back bit. 

## **Serializer** 

This shift register works like it does for Gen1/Gen2 data rates except that it is now receiving 8 bits at a time instead of 10 (i.e., the serializer is an 8‐bit parallel to serial shift register). 

**434** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

## **Mux for Sync Header Bits** 

Finally, the two Sync Header bits must be injected to distinguish the next Block of characters as a Data Block or an Ordered Set Block. These are the first two bits of each 130‐bit Block and the logic for them could be added anywhere in the transmitter that makes sense for the design. In this example the bits are injected at the end of the process for simplicity. Wherever they are included, the flow of bytes from above must be stalled to allow time for them. In this example there will need to be a way to inform the logic above to pause for two bit times. The flow of incoming packets will just be queued in the Tx Buffer during the time the Sync bits are being sent. 

## **Gen3 Physical Layer Receive Logic** 

As in the earlier generations, the Receiver’s logic, shown in Figure 12‐18 on page 436, begins with the CDR (Clock and Data Recovery) circuit. This probably includes a PLL that locks onto the frequency of the Transmitter clock based on knowledge of the expected frequency and the edges in the bit stream to gener‐ ate a recovered clock (Rx Clock). This recovered clock latches the incoming bits into a deserializing buffer and then, once Block Alignment has been established (during the Recovery state of the LTSSM), another version of the recovered clock that is divided by 8.125 (Rx Clock/8.125) latches the 8‐bit Symbols into the Elastic Buffer. After that, the de‐scrambler recreates the original data from the scrambled characters. The bytes bypass the 8b/10b decoder and are delivered directly to the Byte Un‐striping logic. Finally, the Ordered Sets are filtered out, and the remaining byte stream of TLPs and DLLPs is forwarded up to the Data Link Layer. 

In the following discussion, each part is described working upward from the bottom. The focus is on describing aspects of the Physical Layer changed for 8.0 GT/s. Sub‐block unchanged from Gen1/Gen2 will not be described in this sec‐ tion. 

## **Differential Receiver** 

The differential receiver logic is unchanged, but there are electrical changes to improve signal integrity (see “Signal Compensation” on page 468), as well as training changes to establish signal equalization, which are covered in “Link Equalization Overview” on page 577. 

**435** 

## **PCI Ex ress Technolo p gy** 

_Figure 12‐18: Gen3 Physical Layer Receiver Details_ 

**==> picture [276 x 369] intentionally omitted <==**

**----- Start of picture text -----**<br>
To Data Link Layer<br>eceiTLP/DLLPIndicator<br>N*8<br>Rx<br>Buffer<br>TLP/DLLP<br>N*8 Indicator<br>Packet<br>Filtering<br>Block<br>N*8 D/K# Type<br>Lane 0 Byte Un-Striping Lane N<br>8 8<br>Mux Mux<br>8 8 8 8<br>D/K# D/K#<br>Gen3 De-Scrambler Gen3 De-Scrambler<br>De-Scrambler De-Scrambler<br>8 8 D/K# 8 8 D/K#<br>8b/10b 8b/10b<br>Decoder Decoder<br>Gen3 Gen3<br>10 Block 10 Block<br>Type Type<br>CDR Logic CDR Logic<br>Rx Rx<br>Lane 0 Lane 1, ..,N-1 Lane N<br>**----- End of picture text -----**<br>


**436** 

**Chapter 12: Physical Layer - Logical (Gen3)** 

_Figure 12‐19: Gen3 CDR Logic_ 

**==> picture [385 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>