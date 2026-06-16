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
