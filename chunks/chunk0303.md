During this substate, the Transmitter will send the Beacon on at least Lane 0. Note that this state only applies to Upstream Ports because only they can send a Beacon. 

## _Exit to “Detect State”_ 

The next state will be Detect if an Electrical Idle exit is detected on any Receiver of an Upstream Port. Of course, power must have already been restored to the devices in order for the neighbor to exit from Electrical Idle. 

## **Hot Reset State** 

A Port enters the Hot Reset state either because it is a Bridge and software pro‐ grammed its configuration space to propagate a Hot Reset Downstream as explained in “Hot Reset (In‐band Reset)” on page 837, because a Port received two consecutive TS1s with the Hot Reset bit asserted. 

## _During Hot Reset_ 

A Port transmits TS1s with the Hot Reset bit set continuously but doesn’t change the configured Link and Lane Numbers. 

If the Upstream Port of Switch enters the Hot Reset state, all configured Downstream Ports must transition to Hot Reset as soon as possible. 

## _Exit to “Detect State”_ 

In the Bridge where Hot Reset was originated, once software clears the con‐ figuration space bit that initiated the Hot Reset, the Bridge Port enters Detect. However, the Port must remain in the Hot Reset state for a mini‐ mum of 2ms. 

**612** 

**Chapter 14: Link Initialization & Training** 

For Ports where Hot Reset was entered because of receiving two consecu‐ tive TS1s with the Hot Reset bit asserted, it remains in this state as long as it continues to receive these type of TS1s. Once the Port stops receiving TS1s with the Hot Reset bit asserted, it will transition to the Detect state. How‐ ever, the Port must remain in the Hot Reset state for a minimum of 2ms. 

## **Disable State** 

A Disabled Link is Electrically Idle and does not have to maintain the DC com‐ mon mode voltage. Software initiates this by setting the Link Disable bit (see Figure 14‐71 on page 644) in the Link Control register of a device and the device then sends TS1s with the Link Disable bit asserted. 

## _During Disable_ 

All Lanes transmit 16 to 32 TS1s with the Disable Link bit asserted, send an EIOS (two consecutive EIOSs for the 5.0 GT/s case) and then transition to Electrical Idle. The DC common‐mode voltage does not need be within spec. 

If an EIOS (two consecutive EIOSs for the 5.0 GT/s case) was sent and an EIOS was also received on any configured Lane, then LinkUp = 0b (False) and the Lanes are considered to be disabled. 

## _Exit to “Detect State”_ 

For Upstream Ports, the next state will be Detect when Electrical Idle is detected at the Receiver or if no EIOS has been received within a 2ms time‐ out. 

For Downstream Ports, the next state will also be Detect, but not until the Link Disable bit has been cleared to 0b by software. 

## **Loopback State** 

The Loopback state is a test and debug feature that isn’t used during normal operation. A device acting as a Loopback master can put the Link partner into the Loopback slave mode by sending TS1s with the Loopback bit asserted. This can be done in‐circuit, allowing the possibility of using the Loopback state to perform a BIST (Built In Self Test) on the Link. 

Once in this state, the Loopback master sends valid Symbols to the Loopback slave, which then echoes them back. The Loopback slave continues to perform 

**613** 

## **PCI Ex ress Technolo p gy** 

clock tolerance compensation, so the master must continue to insert SOSs at the correct intervals. To perform clock tolerance compensation, the Loopback slave may have to add or delete SKP Symbols to the SOS it echoes to the Loopback master. 

The Loopback state is exited when the Loopback master transmits an EIOS and the receiver detects Electrical Idle. The Loopback state machine is shown in Fig‐ ure 14‐44 on page 614 and described in the following text. 

_Figure 14‐44: Loopback State Machine_ 

**==> picture [368 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from Configuration<br>Or Recovery<br>Slave: Enter Electrical<br>Master sends valid Idle for 2ms<br>Master sends Master receives Symbols - Master: Tx EIOSs<br>Identical TS1’s; Slave required to and enter Electrical<br>TS1s w/ Loopback Slave has retransmit exactly Slave: Directed or  Idle for 2 ms<br>bit set entered 4 EIOS seen<br>Loopback Master: Directed<br>Loopback.Entry Loopback.Active Loopback.Exit<br>Timeout less than<br>100 ms Exit to<br>Detect<br>**----- End of picture text -----**<br>


## **Loopback.Entry** 

The typical behavior for this substate is for the Loopback Master to send TS1s with the Loopback bit set until it starts seeing those TS1s being returned. Once the Loopback Master sees TS1s being returned with the Loopback bit asserted, it knows that it’s Link Partner is now behaving as the Loopback Slave and is simply repeating everything it receives. 

While in this substate, the Link is not considered to be active (LinkUp = 0b). Also, the Link and Lane numbers used in TS1s and TS2s are ignored by the Receiver. The spec makes an interesting observation regarding the use of Lane numbers with 128b/130b encoding. As it turns out, each Lane uses a different seed value for its scrambler (see “Scrambling” on page 430). Consequently, if the Lane numbers haven’t been negotiated before going into the Loopback mode, it’s possible that the Link partners could have different Lane assignments and would therefore be unable to recognize incoming Symbols. This can be avoided by waiting until the Lane numbers have been negotiated before direct‐ 

**614** 

**Chapter 14: Link Initialization & Training** 

ing the master to go to the Loopback state, or by directing the master to set the Compliance Receive bit during Loopback.Entry, or by some other method. 

## **Loopback Master:** 

In this substate, the Loopback Master will continuously send TS1s with the Loopback bit set. The master may also assert the Compliance Receive bit in the TS1s to help testing when one or both Ports are having trouble obtaining bit lock, Symbol lock, or Block alignment after a rate change. If the bit is set it must not be cleared while in this state. 

If this substate was entered from Configuration.Linkwidth.Start, check to see whether the speed in use is the highest mutually supported rate for both Link partners. If not: 

- Change to the highest common speed. Send 16 TS1s with the Loop‐ back bit set followed by an EIOS (two EIOSs if the current speed is 5.0 GT/s), and then go to Electrical Idle for 1ms. During the idle time, change the speed to the highest commonly‐supported rate. 

- If the highest common rate is 5.0 GT/s, the slave’s Tx de‐emphasis is controlled by the master setting its Selectable De‐emphasis bit in the TS1s to the desired value (1b = ‐3.5 dB, 0b = ‐6 dB). 

- For data rates of 5.0 GT/s and higher, the master’s Transmitter can choose any de‐emphasis settings it wants, regardless of the settings it sent to the slave. 

- Potential problem: if Loopback is entered after the Link has already trained to L0 and LinkUp = 1b, it’s possible for one Port to enter Loop‐ back from Recovery and the partner to enter from Configuration. If that happened, the latter Port might try to change the speed while the Port entering from Recovery does not, resulting in a situation where the results are undefined. The spec states that the test set‐up must avoid conflicting cases like this. 

## _Exit to “Loopback.Active”_ 

The next state will be Loopback.Active after either 2ms, if the Compli‐ ance Receive bit is set in the outgoing TS1s, or two consecutive TS1s are received on a design‐specific number of Lanes with the Loopback bit set and the Compliance Receive bit was not set in the outgoing TS1s. 

Note that if the speed was changed, the master must ensure that enough TS1s have been sent for the slave to be able to acquire Symbol lock or Block alignment before going to the Loopback.Active state. 

**615** 

**PCI Ex ress Technolo p gy** 

## _Exit to “Loopback.Exit”_ 

If neither of the conditions to enter Loopback.Active are met, the next state will be Loopback.Exit after a design‐specific timeout of less than 100ms. 

## **Loopback Slave:** 

This substate is entered by receiving two consecutive TS1s with the Loop‐ back bit asserted. 

If this substate was entered from Configuration.Linkwidth.Start, check to see whether the speed in use is the highest one that mutually supported by both Link partners. If not: 

- Change to the highest common speed. Send one EIOS (two EIOSs if the current speed is 5.0 GT/s), and then go to Electrical Idle for 2ms. During the idle time, change the speed to the highest commonly‐sup‐ ported rate. 

- If the highest common rate is 5.0 GT/s, set the Transmitter’s de‐ emphasis according to the Selectable De‐emphasis bit in the received TS1s (1b = ‐3.5 dB, 0b = ‐6 dB). 

- If the highest common rate is 8.0 GT/s and: 

   - a) EQ TS1s directed the slave to this state, use the Tx Preset settings they specified. 

   - b) Normal TS1s directed the slave to this state, the slave is allowed to use its default transmitter settings. 

## _Exit to “Loopback.Active”_ 

The next state will be Loopback.Active if the Compliance Receive bit was set in the incoming TS1s that directed the slave to this state. The slave doesn’t need to wait for particular boundaries to send looped‐back data, and is allowed to truncate any Ordered Set in progress. 

Otherwise, the slave sends TS1s with Link and Lane numbers set to PAD and the next state will be Loopback.Active if: 

- The rate is 2.5 or 5.0 GT/s and Symbol lock is acquired on all Lanes. 

- The rate is 8.0 GT/s and two consecutive TS1s are seen on all active Lanes. Equalization is handled by evaluating and applying the values given in the TS1s, as long as they’re supported and the EC value is appropriate for the direction of the Port (10b for Downstream Ports, 

**616** 

**Chapter 14: Link Initialization & Training** 

and 11b for Upstream Ports). Optionally, the Port can accept either of the EC values for this case. If the settings are applied, they must take effect within 500ns of receiving them and must not cause the Trans‐ mitter to violate any electrical specs for more than 1ns. A significant difference compared to the process in Recovery.Equalization is that the new settings are not echoed in the TS1s being sent by the slave. – For 8b/10b, the slave must only transition to looped‐back data on a Symbol boundary, but is allowed to truncate any Ordered Set in progress. For 128b/130b, no boundary is specified for when the looped‐back data can be sent, and it is still allowed to truncate any Ordered Set in progress. 

## **Loopback.Active** 

During this substate, the Loopback Master sends valid encoded data and should not send EIOS until it’s ready to exit Loopback. The Loopback Slave ech‐ oes the received information without modification (even if the encoding is determined to be invalid), with the possible exception of inverting the polarity as determined in the Polling state. The slave also continues to perform clock tol‐ erance compensation. That means SKPs must be added or removed as needed, but the Lanes aren’t required to all send the same number. 

## _Exit to “Loopback.Exit”_ 

The next state will be Loopback.Exit for the loopback master if directed. 

The next state will be Loopback.Exit for the loopback slave if either of two conditions is true: 

- The slave is directed to exit or four consecutive EIOSs are seen on any Lane. 

- Optionally, if the current speed is 2.5 GT/s and an EIOS is received or Electrical Idle is detected or inferred on any Lane. Electrical Idle may be inferred if any configured Lane has not detected an exit from Elec‐ trical Idle for 128  s. 
