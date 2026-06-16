- Eight consecutive TS2s are received on any configured Lane with Link and Lane numbers and rate identifiers that match those being sent and either: 

   - a) The speed_change bit in the TS2s is cleared to 0b, or 

   - b) No rate higher than 2.5 GT/s is commonly supported. 

- Sixteen TS2 have been sent after receiving one and they haven’t been interrupted by any intervening EIEOS. The changed_speed_recovery and directed_speed_change variables are both cleared to 0b on entry to this substate. 

## _Exit to “Recovery.Speed”_ 

The LTSSM will go to Recovery.Speed if ALL three conditions listed below are true: 

- Eight consecutive TS2s are received on any configured Lane with the speed_change bit set, identical rate identifiers, identical values in Symbol 6, and: 

   - a) The TS2s were standard 8b/10b TS2s, or 

   - b) The TS2s were EQ TS2s, or 

   - c) 1ms has expired since receiving eight EQ TS2s on any configured Lane. 

- Both Link partners support rates higher than 2.5 GT/s, or the rate is already higher than 2.5 GT/s. 

- For 8b/10b encoding, at least 32 TS2s were sent with the speed_change bit set to 1b without any intervening EIEOS after receiving one TS2 with the speed_change bit set to 1b in the same con‐ figured Lane. For 128b/130b encoding, at least 128 TS2s are sent with the speed_change bit set to 1b after receiving one TS2 with the speed_change bit set to 1b in the same configured Lane. 

A transition to Recovery.Speed can also occur if the rate has changed to a mutually negotiated rate since entering Recovery from L0 or L1 (changed_speed_recovery = 1b) and any configured Lanes have either seen EIOS or detected/inferred Electrical Idle and haven’t seen TS2s since enter‐ ing this substate. This means a higher rate was attempted but the Link part‐ ner indicates that it isn’t working for some reason. The new rate will return to whatever it was when Recovery was entered from L0 or L1. 

The final case that can cause a transition to Recovery.Speed is if the rate has _not_ changed to a mutually negotiated rate since entering Recovery from L0 

**600** 

**Chapter 14: Link Initialization & Training** 

or L1 (changed_speed_recovery = 0b), and the current rate is already higher than 2.5 GT/s, and any configured Lanes have either seen EIOS or detected/ inferred Electrical Idle and haven’t seen TS2s since entering this substate. In this case, the understanding is that the current rate isn’t working and the solution is to drop back down, so the new rate will become 2.5 GT/s. 

## _Exit to “Configuration State”_ 

The next state will be Configuration if 8 consecutive TS1s are received on any configured Lane with Link or Lane numbers that don’t match those being sent and either the speed_change bit is cleared to 0b, or no rate higher than 2.5 GT/s is commonly supported. 

The variables changed_speed_recovery and directed_speed_change are cleared to 0b when the LTSSM transitions to Configuration. If the N_FTS value has changed since last time, the new value must be used for L0s going forward. 

## _Exit to “Detect State”_ 

After 48ms without resolving to one of the previously‐defined state transi‐ tions, the next state will be Detect if the data rate is 2.5 GT/s or 5.0 GT/s. 

If the rate is 8.0 GT/s there is another possibility because the number of attempts may not have been exceeded yet. That is indicated by the idle_to_rlock_transitioned variable, and if it’s less than FFh when the rate is 8.0 GT/s, the new state will be “Recovery.Idle”. If that transition is made, the variables changed_speed_recovery and directed_speed_change will be cleared to 0b. However, once idle_to_rlock_transitioned reaches FFh, and the 48ms timeout is seen, the next state will be Detect. 

## **Recovery.Idle** 

As the name implies, Transmitters will usually send Idles in this substate as a preparation for changing to the fully operational L0 state. For 8b/10b mode, Idle data is normally sent on all the Lanes, while for 128b/130b an SDS is sent to start a Data Stream and then Idle data Symbols are sent on all the Lanes. 

## _Exit to “L0 State”_ 

The next state is L0 if either of the following cases is true. In either case, if the Retrain Link bit has been written to 1b since the last transition to L0 from Recovery or Configuration, the Downstream Port will set the Link Bandwidth Management Status bit to 1b (see Figure 14‐39 on page 597). 

- 8b/10b encoding is in use and 8 consecutive Symbol Times of Idle data have been received and 16 Idle data Symbols have been sent since the first one was received. 

**601** 

## **PCI Ex ress Technolo p gy** 

- 128b/130b encoding in use, 8 consecutive Symbol Times of Idle data have been received and 16 Idle data Symbols have been sent since the first one was received, and this state wasn’t entered from Recov‐ ery.RcvrCfg. Note that Idle data Symbols must be contained in Data Blocks, Lane‐to‐Lane De‐skew must be completed before Data Stream processing starts, and the idle_to_rlock_transitioned variable is cleared to 00h on transition to L0. 

## _Exit to “Configuration State”_ 

The next state is Configuration if either: 

- A Port is instructed by a higher layer to optionally reconfigure the Link, such as to change the Link width. 

- Any configured Lane sees two consecutive incoming TS1s with Lane numbers set to PAD (a Port that transitions to Configuration to change the Link will send PAD Lane numbers on all Lanes). The spec recommends that the LTSSM use this transition when changing the Link width to reduce the time it will take. 

## _Exit to “Disable State”_ 

The next state is Disabled if either: 

- A Downstream or optional crosslink Port is instructed by a higher layer to set the Disable Link bit in its TS1s or TS2s. 

- Any configured Lane of an Upstream or optional crosslink Port sees the Disable Link bit set in two consecutive incoming TS1s. 

## _Exit to “Hot Reset State”_ 

The next state is Hot Reset if either: 

- A Downstream or optional crosslink Port is instructed by a higher layer to set the Hot Reset bit in its TS1s or TS2s. 

- Any configured Lane of an Upstream or optional crosslink Port sees the Hot Reset bit set in two consecutive incoming TS1s. 

## _Exit to “Loopback State”_ 

The next state is Loopback if either: 

- A Transmitter is known to be Loopback Master capable (design spe‐ cific; the spec does not provide a means to verify this) and instructed by a higher layer to set the Loopback bit in its TS1s or TS2s. 

- Any configured Lane of an Upstream or optional crosslink Port sees the Loopback bit set in two consecutive incoming TS1s. The receiving device then becomes the Loopback slave. 

**602** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “Detect State”_ 

Otherwise, after a 2ms timeout, the next state will be Detect unless the idle_to_rlock_transitioned variable is less than FFh, in which case the next state will be “Detailed Recovery Substates”. For the transition to Recov‐ ery.RcvrLock, if the data rate is 8.0 GT/s the idle_to_rlock_transitioned vari‐ able is incremented by 1b, while for 2.5 or 5.0 GT/s it will be set to FFh. 

## **L0s State** 

This is the low power Link state that has the shortest exit latency back to L0. Devices manage entry and exit from this state automatically under hardware control without any software involvement. Each direction of a Link, can enter and exit the L0s state independent of each other. 

## **L0s Transmitter State Machine** 

The L0s state has different substates for the Transmitter and the Receiver. The Transmitter substates will be described first. As shown in Figure 14‐40 on page 603 the transmitter state machine associated with L0s state is a simple one. 

_Figure 14‐40: L0s Tx State Machine_ 

**==> picture [288 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Tx sends  Transmitter sends<br>EIOS FTSs on all Lanes<br>TTX-IDLE-MIN<br>= 20 ns Tx_L0s.Idle Directed<br>Tx_L0s.Entry Tx_L0s.FTS<br>(Tx Electrical Idle)<br>Transmitter sends<br>SOS or EIEOS<br>Exit to<br>L0<br>**----- End of picture text -----**<br>


**603** 

**PCI Ex ress Technolo p gy** 

## **Tx_L0s.Entry.** 

A Transmitter enters L0s when directed by an upper layer. The spec gives no decision criteria for this, but intuitively it would occur based on an inac‐ tivity timeout: no TLPs or DLLPs being sent for a given time. To enter L0s, the Transmitter sends one EIOS (two EIOSs for the 5.0 GT/s rate) and enters Electrical Idle. The Transmitter is not turned off, however, and must main‐ tain the DC common‐mode voltage within the spec range. 

## _Exit to “Tx_L0s.Idle”_ 

The next state will be Tx_L0s.Idle after the TTX‐IDLE‐MIN timeout (20ns). This time is intended to ensure that the Transmitter has established the Electrical Idle condition. 

## **Tx_L0s.Idle.** 

In this substate, the transmitter continues the Electrical Idle state until directed to leave. Because this direction of the Link is in Electrical Idle, there will be a power savings benefit, which is the entire purpose of the L0s state. 

_Exit to “Tx_L0s.FTS”_ 

The next state will be Tx_L0s.FTS when directed, such as when the Port needs to resume packet transmission. The LTSSM will be instructed in a design‐specific manner to exit this state. 

## **Tx_L0s.FTS.** 

In this substate, the Transmitter will start sending FTS ordered sets to retrain the Receiver of the Link Partner. The number of FTSs sent is the N_FTS value advertised by the Link Partner in its TS Ordered Sets during the last training sequence that led to L0. The spec notes that if a Receiver times out while trying to do this, it may choose to increase the N_FTS value it advertises during the Recovery state. 

If the Extended Synch bit is set (see Figure 14‐71 on page 644), the transmit‐ ter must sends 4096 FTSs instead of the N_FTS number. This extends the time available to synchronize external test and analysis logic, which may not be able to recover Bit Lock as quickly as the embedded logic can. 

For all data rates, no SOSs can be sent prior to sending any FTSs. However, for the 5.0 GT/s rate, 4 to 8 EIE Symbols must be sent prior to sending the FTSs. For 128b/130b, an EIEOS must be sent prior to the FTSs. 

**604** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “L0 State”_ 

The Transmitter will transition to the L0 state once all the FTSs have been sent and: 

- a)  For 8b/10b encoding, one SOS is sent on all configured Lanes, although none are sent before or during the FTSs. 

- b)  For 128b/130b encoding, one EIEOS is sent followed by an SDS and a Data Stream. 

## **L0s Receiver State Machine** 

Figure 14‐41 on page 605 shows the Receiver L0s state machine. A Receiver is required to implement L0s support if the ASPM Support field in the Link Capa‐ bility register shows it to be supported, and is allowed to implement it even if that support is not indicated. 

_Figure 14‐41: L0s Receiver State Machine_ 

**==> picture [327 x 184] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Rx detects<br>EIOS Exit from FTSs Received<br>TTX-IDLE-MIN Electrical<br>= 20 ns Rx_L0s.Idle Idle<br>Rx_L0s.Entry Rx_L0s.FTS<br>(Rx Electrical Idle)<br>Tx sends N_FTS<br>SOS or EIEOS Timeout<br>Exit to Exit to<br>L0 Recovery<br>**----- End of picture text -----**<br>


**605** 

**PCI Ex ress Technolo p gy** 

## **Rx_L0s.Entry.** 

Entered when a Receiver that receives an EIOS, provided it supports L0s and hasn’t been directed to L1 or L2. 

_Exit to “Rx_L0s.Idle”_ 

The next state will be Rx_L0s.Idle after the TTX‐IDLE‐MIN timeout (20ns). 

## **Rx_L0s.Idle.** 

The Receiver is now in Electrical Idle mode and is just waiting to see an exit from Electrical Idle. 
