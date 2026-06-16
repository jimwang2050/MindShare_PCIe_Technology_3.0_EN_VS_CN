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
