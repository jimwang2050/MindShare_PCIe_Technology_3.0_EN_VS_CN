The specification points out a special consideration for devices that implement only VC0. For example, the only Non‐Posted writes are I/O Writes and Configu‐ ration Writes both of which are permitted only on VC0. Thus, Non‐Posted data buffers are not used for VC1 ‐ VC7 and an infinite value can be advertised for those values. However, the Non‐Posted Header must still operate and header credits must still need to be updated. 

**221** 

**PCI Ex ress Technolo p gy** 

## **Flow Control Initialization** 

## **General** 

Prior to sending any transactions, flow control initialization is needed. In fact, TLPs cannot be sent across the Link until Flow Control Initialization is per‐ formed successfully. Initialization occurs on every Link in the system and involves a handshake between the devices at each end of a link. This process begins as soon as the Physical Layer link training has completed. The Link Layer knows the Physical Layer is ready when it observes the LinkUp signal is active, as illustrated in Figure 6‐3. 

_Figure 6‐3: Physical Layer Reports That It’s Ready_ 

**==> picture [338 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core  Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer  Transaction Layer<br>DLL DLCMSM  DLL DLCMSM DLCMSM<br>LinkUp LinkUp<br>Phy Phy<br>LTSSM  LTSSM<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>


Once started, the Flow Control initialization process is fundamentally the same for all Virtual Channels and is controlled by hardware once a VC has been enabled. VC0 is always enabled by default, so its initialization is automatic. 

**222** 

**Chapter 6: Flow Control** 

That allows configuration transactions to traverse the topology and carry out the enumeration process. Other VCs only initialize when configuration soft‐ ware has set up and enabled them at both ends of the Link. 

## **The FC Initialization Sequence** 

The flow control initialization process involves the Link Layer’s DLCMSM (Data Link Control and Management State Machine). As shown in Figure 6‐4 on page 223, a reset puts the state machine into the DL_Inactive state. While in the DL_Inactive state, DL_Down is signaled to both the Link and Transaction Lay‐ ers. Meanwhile, it waits to see LinkUp from the Physical Layer to indicate that the LTSSM has finished its work and the Physical Layer is ready. That causes a transition to the DL_Init sub‐state, which contains two stages that handle flow control initialization: FC_INIT1 and FC_INIT2. 

_Figure 6‐4: The Data Link Control & Management State Machine_ 

**==> picture [251 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
Reset<br>DL_Inactive Report DL_Down to Link<br>and Transaction Layers<br>Physical LinkUp=1<br>Physical LinkUp=0 &<br>Link Enabled andr<br>DL_Init<br>Report DL_Down<br>FC_Init1<br>(during FC_Init1)<br>Report DL_Up to remaining<br>FC_Init2<br>Link and Transaction Layers<br>(during FC_Init2)<br>FC_Init Complete<br>&<br>Physical LinkUp=1<br>DL_Active Report DL_Up<br>**----- End of picture text -----**<br>


**223** 

**PCI Ex ress Technolo p gy** 

## **FC_Init1 Details** 

During the FC_INIT1 state, devices continuously send a sequence of 3 InitFC1 Flow Control DLLPs advertising their receiver buffer sizes (see Figure 6‐5). According to the spec, the packets must be sent in this order: Posted, Non‐ posted, and Completions as illustrated in Figure 6‐6 on page 225. The specifica‐ tion strongly encourages that these be repeated frequently to make it easier for the receiving device to see them, especially if there are no TLPs or DLLPs to send. Each device should also receive this sequence from its neighbor so it can register the buffer sizes. Once a device has sent its own values and received the complete sequence enough times to be confident that the values were seen cor‐ rectly, it’s ready to exit FC_INIT1. To do that, it records the received values in its transmit counters, sets an internal flag (FL1), and changes to the FC_INIT2 state to begin the second initialization step. 

_Figure 6‐5: INIT1 Flow Control DLLP Format and Contents_ 

**==> picture [373 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataHdr FC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>0100  Init 1 Posted<br>0101  Init 1 Non Posted<br>0110  Init 1 Completion<br>1100  Init 2 Posted<br>1101  Init 2 Non Posted<br>1110  Init 2 Completion<br>**----- End of picture text -----**<br>


**224** 

**Chapter 6: Flow Control** 

_Figure 6‐6: Devices Send InitFC1 in the DL_Init State_ 

**==> picture [366 x 338] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIeX-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters RCV Buffers FC Counters RCV Buffers<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>InitFC1-P InitFC1-NP InitFC1-Cpl<br>InitFC1-Cpl InitFC1-NP InitFC1-P<br>- Note required order of InitFC transmission<br>InitFC1 P<br>**----- End of picture text -----**<br>


## **FC_Init2 Details** 

In this state a device continuously sends InitFC2 DLLPs. These are sent in the same sequence as the InitFC1s and contain the same credit information, but they also confirm that FC initialization has succeeded at the sender. Since the device has already registered the values from the neighbor it doesn’t need any more credit information and will ignore any incoming InitFC1s while it waits to see InitFC2s. It can even send TLPs at this point, even though initialization hasn’t completed for the other side of the Link, and this is indicated to the Transaction Layer by the DL_Up signal (See Figure 6‐7). 

**225** 

## **PCI Ex ress Technolo p gy** 

Why is this second initialization step needed? The simple answer is that neigh‐ boring devices may finish FC initialization at different times and this method ensures that the late one will continue to receive the FC information it needs even if the neighbor finishes early. Once a device receives an FC_INIT2 packet for any buffer type, it sets an internal flag (Fl2). (It doesnʹt wait to receive an FC_Init2 for each type.) Note that FL2 is also set upon receipt of an UpdateFC packet or TLP. When both sides are done and have sent InitFC2s, the DLCMSM transitions to the DL_Active state and the Link Layer is ready for normal opera‐ tion. 

_Figure 6‐7: FC Values Registered ‐ Send InitFC2s, Report DL_Up_ 

**==> picture [346 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core  Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer  Transaction Layer<br>DL_Up<br>DLL DLCMSM  DLL DLCMSMDLCMSM<br>Phy Phy<br>LTSSM  LTSSM<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>InitFC2-Cpl InitFC2-NP InitFC2-P<br>**----- End of picture text -----**<br>


## **Rate of FC_INIT1 and FC_INIT2 Transmission** 

The specification defines the latency between sending FC_INIT DLLPs as fol‐ lows: 

**226** 

**Chapter 6: Flow Control** 

- **VC0** . Hardware‐initiated flow control of VC0 requires that FC_INIT1 and FC_INIT2 packets be transmitted “continuously at the maximum rate possi‐ ble.” That is, the resend timer is set to a value of zero. 

- **VC1‐VC7** . When software initiates flow control initialization for other VCs, the FC_INIT sequence is repeated “when no other TLPs or DLLPs are avail‐ able for transmission.” However, the latency between the beginning of one sequence to the next can be no greater than 17μs. 

## **Violations of the Flow Control Initialization Protocol** 

A violation of the flow control initialization protocol can be optionally checked by a device. An error detected can be reported as a Data Link Layer protocol error. 

## **Introduction to the Flow Control Mechanism** 

## **General** 

The specification defines the requirements of the Flow Control mechanism using registers, counters, and mechanisms for reporting, tracking, and calculat‐ ing whether a transaction can be sent. These elements are not required and the actual implementation is left to the device designer. This section introduces the specification model and serves to explain the concepts and to define the require‐ ments. 

## **The Flow Control Elements** 

Figure 6‐8 illustrates the elements used for managing flow control. The diagram shows transactions flowing in a single direction across a Link, and another set of these elements supports transfers in the opposite direction. The primary function of each element is listed below. While these Flow Control elements are duplicated for all six receive buffers, for simplicity this example only deals with non‐posted header flow control. 

One final element associated with managing flow control is the Flow Control Update DLLP. This is the only Flow Control packet that is used during normal transmission. The format of the FC Update packet is illustrated in Figure 6‐9 on page 229. 

**227** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐8: Flow Control Elements_ 

**==> picture [380 x 251] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>FC Gating Logic<br>PTLP<br>Transactions CC+PTLP =CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>Credits<br>Consumed Credit Limit VC0<br>Incr Check FC<br>Buffer<br>Link Packet optional incr<br>Control<br>incr Credits Rcv CredAlloc (NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC DLLPs<br>TLP Link<br>**----- End of picture text -----**<br>


## **Transmitter Elements** 

- **Transactions Pending Buffer** — holds transactions that are waiting to be sent in the same virtual channel. 

- **Credits Consumed counter** — contains the credit sum of all transactions sent for this buffer. This count is abbreviated “CC.” 

- **Credit Limit counter** — initialized by the receiver with the size of the corre‐ sponding Flow Control buffer. After initialization, Flow Control update packets are sent periodically to update the Flow Control credits as they become available at the receiver. This value is abbreviated “CL.” 

- **Flow Control Gating Logic** — performs the calculations to determine if the receiver has sufficient Flow Control credits to accept the pending TLP (PTLP). In essence, this logic checks that the CREDITS_CONSUMED (CC) plus the credits required for the next Pending TLP (PTLP) does not exceed the CREDIT_LIMIT (CL). This specification defines the following equation for performing the check, with all values represented in credits. 

**228** 

**Chapter 6: Flow Control** 

_CL_ –  _CC_ + _PTLP_  _mod_ 2  _[FieldSize]_   2  _[FieldSize]_   2 

For an example application of this equation, See “Stage 1 — Flow Control Fol‐ lowing Initialization” on page 230. 

## **Receiver Elements** 

- **Flow Control Buffer** — stores incoming headers or data. 

- **Credit Allocated** — tracks the total Flow Control credits that have been allocated (made available). It’s initialized by hardware to reflect the size of the associated Flow Control buffer. The buffer fills as transactions arrive but then they are eventually removed from the buffer by the core logic at the receiver. When they are removed, the number of Flow Control credits is added to the CREDIT_ALLOCATED counter. Thus the counter tracks the number of credits currently available. 
