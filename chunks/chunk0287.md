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