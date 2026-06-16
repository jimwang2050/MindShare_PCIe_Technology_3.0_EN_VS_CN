It should be noted that Devices are allowed to change their supported data rates and upconfigure capability when they enter this substate, but not while in it. This is because Devices record the capabilities of their Link partner from what is advertised in these TS2s, as will be described in this section. 

## **Downstream Lanes** 

## _During Configuration.Complete_ 

TS2s are sent using the Link and Lane numbers that match the received TS1s. The TS2s can have the Upconfigure Capability bit set if the Port sup‐ ports a x1 Link using Lane 0 and is able to up‐configure the Link. 

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity. 

The Downstream Port is transmitting TS2s and watching for TS2s coming back. For future reference, record the number of FTSs that must be sent when exiting from the L0s state from the N_FTS field in the incoming TS2s. 

## _Exit to “Configuration.Idle”_ 

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching rate identifiers, and matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2. 

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane and this overrides any previ‐ ously recorded value. The variable used to track speed changes in Recovery, “changed_speed_recovery”, is cleared to zero. 

The variable “upconfigure_capable” is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8 consecutive TS2s with the same bit set. Otherwise it’s cleared to zero. 

Any Lanes that aren’t configured as part of the Link are no longer associ‐ ated with the LTSSM in progress and must either be: 

- Associated with a new LTSSM or 

- Transitioned to Electrical Idle 

   - a)   A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b 

**563** 

**PCI Ex ress Technolo p gy** 

since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it’s also recom‐ mended that those Lanes leave their Receiver terminations on because they’ll become part of the Link again if it is upconfigured. If the terminations aren’t left on, they must be turned on from when the LTSSM enters the Recovery.RcvrCfg state all the way through Configuration.Complete. Lanes that weren’t part of the Link before can’t become part of it through this process, though. 

- b)  For the optional crosslink, Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐HIGH‐IMP‐DC‐NEG. 

- c) If the LTSSM goes back to Detect, these Lanes will once again be associated with it. 

- d)  No EIOS is needed before Lanes go to Electrical Idle, and the transi‐ tion doesn’t have to happen on Symbol or Ordered Set boundaries. 

## After a 2ms timeout: 

_Exit to “Configuration.Idle”_ 

Next state is Configuration.Idle if the idle_to_rlock_transitioned vari‐ able is less than FFh **and** the current data rate is 8.0 GT/s. 

In this transition, the “changed_speed_recovery” variable is cleared to zero. Also, the “upconfigure_capable” variable may be updated, though it’s not required to do so, if at least one Lane saw eight consecu‐ tive TS2s with matching Link and Lane numbers (non‐PAD). If the transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero. 

Lanes that aren’t part of the configured Link aren’t associated with the LTSSM in progress and have the same requirements as the non‐timeout case listed above. 

_Exit to “Detect State”_ 

Otherwise, the next state is Detect. 

## **Upstream Lanes** 

_During Configuration.Complete_ 

TS2s are sent using the Link and Lane numbers that match the received TS2s. The TS2s can have the Upconfigure Capability bit set if the Port sup‐ ports a x1 Link using Lane 0 and is able to up‐configure the Link. 

**564** 

**Chapter 14: Link Initialization & Training** 

For 8b/10b encoding, Lane de‐skewing must be completed when leaving this substate. Also, scrambling will be disabled if all configured Lanes see two consecutive TS2s with the Disable Scrambling bit set. The Port that sends these must also disable scrambling. Note that scrambling cannot be disabled when in 128b/130b mode because of the necessary contribution it makes to signal integrity. 

In this substate, the Upstream Port is receiving TS2s from the Downstream Port, and for future reference, should record the N_FTS field value number of FTSs that must be sent when exiting from the L0s state from the in the incoming TS2s. 

## _Exit to “Configuration.Idle”_ 

The next state will be Configuration.Idle when all Lanes sending TS2s receive 8 TS2s with matching Link and Lane numbers (non‐PAD), matching rate identifiers, and a matching Link Upconfigure Capability bit in all of them. At least 16 TS2s must also be sent after receiving one TS2. 

If the device supports rates greater than 2.5 GT/s, it must record the rate identifier received on any configured Lane, overriding any previously recorded value. The variable used to track speed changes in Recovery, “changed_speed_recovery”, is cleared to zero. 

The variable “upconfigure_capable” is set to 1b if the device sends TS2s with Link Upconfigure Capability set to 1b and receives 8 consecutive TS2s with the same bit set. Otherwise it’s cleared to zero. 

Any Lanes that aren’t configured as part of the Link are no longer associ‐ ated with the LTSSM in progress and must either be: 

- Optionally associated with a new crosslink LTSSM (if this feature is sup‐ ported), or 

- Transitioned to Electrical Idle 

   - a) A special case arises if those Lanes had been configured as part of the Link through L0 previously and LinkUp has remained set at 1b since then. They must remain associated with the same LTSSM if the Link is upconfigure capable. For that case, it’s also recommended that those Lanes leave their Receiver terminations on because they’ll become part of the Link again if it is upconfigured. If they’re not left on, they must be turned on from when the LTSSM enters the Recov‐ ery.RcvrCfg state all the way through Configuration.Complete. Lanes that weren’t part of the Link before can’t become part of it through this process, though. 

**565** 

**PCI Ex ress Technolo p gy** 

- b)  Receiver terminations must be between ZRX‐HIGH‐IMP‐DC‐POS and ZRX‐ 

   - HIGH‐IMP‐DC‐NEG[.] 

- c)    If the LTSSM goes back to Detect, these Lanes will once again be asso‐ ciated with it. 

- d)  No EIOS is needed before Lanes go to Electrical Idle, and the transi‐ tion doesn’t have to happen on Symbol or Ordered Set boundaries. 

After a 2ms timeout: 

## _Exit to “Configuration.Idle”_ 

Next state is Configuration.Idle if the idle_to_rlock_transitioned vari‐ able is less than FFh **and** the current data rate is 8.0 GT/s. 

In this transition, the “changed_speed_recovery” variable is cleared to zero. Also, the “upconfigure_capable” variable may be updated, though it’s not required to do so, if at least one Lane saw eight consecu‐ tive TS2s with matching Link and Lane numbers (non‐PAD). If the transmitted and received Link Upconfigure Capability bits are 1b, set it to 1b, otherwise clear it to zero. 

Lanes that aren’t part of the configured Link aren’t associated with the LTSSM in progress and have the same requirements as the non‐timeout case listed above. 

## _Exit to “Detect State”_ 

Otherwise, the next state is Detect. 

## **Configuration.Idle** 

## _During Configuration.Idle_ 

In this substate, the transmitter is sending Idle data and waiting for the minimum number of received Idle data so this Link can transition to L0. During this time, the Physical Layer reports to the upper layers that the link is operational (Linkup = 1b). 

For 8b/10b encoding, the transmitter is sending Idle data on all configured Lanes. Idle data are just data zeros that get scrambled and encoded. 

For 128b/130b encoding, the transmitter sends one SDS Ordered Set on all configured Lanes followed by Idle data Symbols. The first Idle Symbol on Lane 0 is the first Symbol of the Data Stream. 

**566** 

**Chapter 14: Link Initialization & Training** 

## _Exit to “L0 State”_ 

If using 8b/10b encoding, the next state is L0 if 8 consecutive Idle data sym‐ bol times are received on all configured Lanes, and 16 symbol times of idle data were sent after receiving one Idle Symbol. 

If using 128b/130b, the next state is L0 if 8 consecutive Idle data are received on all configured Lanes, 16 Idles were sent after receiving one Idle Symbol, and this state wasn’t entered by a timeout from Configuration.Complete. 

- Lane‐to‐Lane de‐skew must be completed before Data Stream processing begins. 

- The Idle Symbols must be received in Data Blocks. 

- If software set the Retrain Link bit in the Link Control register since the last transition to L0 from Recovery or Configuration, the Downstream Port must set the Link Bandwidth Management bit in the Link Status reg‐ ister to 1b to indicate that this change was not hardware initiated (auton‐ omous). 

- The “idle_to_rlock_transitioned” variable is cleared to 00h on transition to L0. 

## After a 2ms timeout: 

## _Exit to “Detailed Recovery Substates”_ 

If the idle_to_rlock_transitioned variable is less than FFh, the next state is Recovery (Recovery.RcvrLock). Then: 

- a) For 8.0 GT/s, increment idle_to_rlock_transitioned by 1. 

- b)  For 2.5 or 5.0 GT/s, set idle_to_rlock_transitioned to FFh. 

- c) NOTE: This variable counts the number of times the LTSSM has tran‐ sitioned from this state to the Recovery state because the sequence isn’t working. The problem may be that equalization hasn’t been properly adjusted or that the selected speed just isn’t going to work, and the Recovery state will take steps to address these issues. This variable limits the number of these attempts so as to avoid an endless loop. If the Link still isn’t working after doing this 256 times (when the count reaches FFh), go back to Detect and start over, hoping for a better result. 

_Exit to “Detect State”_ 

Otherwise (meaning idle_to_rlock = FFh), the next state is Detect. 

**567** 

**PCI Ex ress Technolo p gy** 

## **L0 State** 

This is the normal, fully‐operational Link state, during which Logical Idle, TLPs and DLLPs are exchanged between Link neighbors. L0 is achieved immediately following the conclusion of the Link Training process. The Physical Layer also notifies the upper layers that the Link is ready for operation, by setting the LinkUp variable. In addition, the idle_to_rlock_transitioned variable is cleared to 00h. 

## _Exit to “Recovery State”_ 

The next state will be Recovery if a change in the Link speed or Link width is indicated, or if the Link partner initiates this by going to Recovery or Electrical Idle. Let’s consider each of these three cases in a little more detail in the following discussion. 

## **Speed Change** 

Two conditions are described in the spec that will cause an automatic change in speed. 

The first is when rates higher than 2.5 GT/s are supported by both partners and the Link is active (Data Link Layer reports DL_Active), or when one partner requests a speed change in its TS Ordered Sets. For example, a Downstream Port will initiate a speed change if a higher rate was noted and software writes the Retrain Link bit and after setting the Target Link Speed field (see Figure 14‐ 26 on page 569) to a different rate than the current rate. 
