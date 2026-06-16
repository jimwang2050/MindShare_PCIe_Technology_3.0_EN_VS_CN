To facilitate this goal, an error detection code called an LCRC (Link Cyclic Redundancy Code) is added to each TLP. The first step in error checking is sim‐ ply to verify that this code still evaluates correctly at the receiver. If each packet is given a unique incremental Sequence Number as well, then it will be easy to sort out which packet, out of several that have been sent, encountered an error. Using that Sequence Number, we can also require that TLPs must be success‐ fully received in the same order they were sent. This simple rule makes it easy to detect missing TLPs at the Receiver’s Data Link Layer. 

The basic blocks in the Data Link Layer associated with the Ack/Nak protocol are shown in greater detail in Figure 10‐2 on page 319. Every TLP sent across the Link is checked at the receiver by evaluating the LCRC (first) and Sequence Number (second) in the packet. The receiving device notifies the transmitting device that a good TLP has been received by returning an Ack. Reception of an 

**318** 

**Cha ter 10: Ack/Nak Protocol p** 

Ack at the transmitter means that the receiver has received at least one TLP suc‐ cessfully. On the other hand, reception of a Nak by the transmitter indicates that the receiver has received at least one TLP in error. In that case, the transmitter will re‐send the appropriate TLP(s) in hopes of a better result this time. This is sensible, because things that would cause a transmission error would likely be transient events and a replay will have a very good chance of solving the prob‐ lem. 

_Figure 10‐2: Overview of the Ack/Nak Protocol_ 

**==> picture [374 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmit Receiver<br>Device A Device B<br>From To<br>Transaction Layer Transaction Layer<br>Tx Rx<br>Data Link Layer Data Link Layer<br>TLP DLLP DLLP TLP<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux De-mux<br>Error<br>Mux Mux Check<br>Tx Rx Tx Rx<br>DLLP<br>ACK /<br>NAK<br>Link<br>TLP<br>Sequence TLP LCRC<br>**----- End of picture text -----**<br>


Since both the sending and receiving devices in the protocol have both a trans‐ mit and a receive side, this chapter will use the terms: 

- **Transmitter** to mean the device that sends TLPs 

- **Receiver** to mean the device that receives TLPs 

**319** 

**PCI Ex ress Technolo p gy** 

## **Elements of the Ack/Nak Protocol** 

The major Ack/Nak protocol elements of the Data Link Layer are shown in Fig‐ ure 10‐3 on page 320. There’s too much to consider all at once, though, so let’s begin by focusing on just the transmitter elements, which are shown in a larger view in Figure 10‐4 on page 322. 

_Figure 10‐3: Elements of the Ack/Nak Protocol_ 

**==> picture [375 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer (TX) Block TLPs; Report Transaction Layer (RX)<br>DLL protocol error<br>Yes Increment NRS Good TLPs<br>No<br>TLPs (NTS-AS) ≥ 2048?<br>(Continue) NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Assign<br>SequenceNumber (IncrementNEXT_TRANSMIT_SEQ (NTS)) Seq Num < NRS (Duplicate TLP)(Schedule Ack) Seq Num>, <, =NRS?<br>REPLAY_TIMER<br>LCRC Increment on Replay) Seq Num > NRS (Lost TLP)<br>REPLAY_NUM<br>Generator (Send Nak) Yes<br>Purge Older TLPs (Reset Both)<br>(Send Nak) No Pass<br>Retry (Replay)Buffer (Replay)Yes Nak?Nak (Update)AckD_SEQ (AS)No Nak Flag Clear?Set & Send Nak LCRC?<br>Yes AckNak<br>(TLP copy) SeqNum = AS? NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>(TLP copy) Yes Ack Nak<br>(Discard) No CRC?Pass  GeneratorAck/Nak AckNak LatencyTimer<br>Ack/Nak<br>DLLP Link<br>TLP TLP<br>Block TLP during Replay<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- End of picture text -----**<br>


## **Transmitter Elements** 

As TLPs arrive from the Transaction Layer, several things are done to prepare them for robust error detection at the receiver. As shown in the diagram TLPs are first assigned the next sequential Sequence Number, obtained from the 12‐ bit NEXT_TRANSMIT_SEQ counter. 

**320** 

**Cha ter 10: Ack/Nak Protocol p** 

## **NEXT_TRANSMIT_SEQ Counter** 

This counter generates the Sequence Number that will be assigned to the next incoming TLP. It’s a 12‐bit counter that is initialized to 0 at reset or when the Link Layer reports DL_Down (Link Layer is inactive). Since it increments con‐ tinuously with each TLP and only counts forward, the counter eventually reaches its max value of 4095 and rolls over to 0 as it continues to count. 

This Sequence Number assigned to the TLP will be used in the Ack or Nak sent by the receiver to reference this TLP in the Replay Buffer. One might think that such a large counter means that a large number of unacknowledged TLPs could be in flight, but in practice this is very unlikely. The main reason is that the receiver has a requirement to send an Ack back for successfully received TLPs within a certain amount of time. That amount of time is discussed in detail in “AckNak_LATENCY_TIMER” on page 328, but is typically only long enough to transmit a few max sized packets. 

## **LCRC Generator** 

This block generates a 32‐bit CRC (Cyclic Redundancy Check) code based on the header and data to be sent and adds it to the end of the outgoing packet to facilitate error detection. The name is derived from the fact that this _check code_ (calculated from the packet to be sent) is _redundant_ (adds no information), and is derived from _cyclic codes_ . Although a CRC doesn’t supply enough information for the Receiver to do automatic error correction the way ECC (Error Correcting Code) methods can, it does provide robust error detection. CRCs are commonly used in serial transports because they’re easy to implement in hardware, and because they’re good at detecting burst errors: a string of incorrect bits. Since this is more likely to happen in a serial design than a parallel model, it helps explain why a CRC is a good choice for error detection in serial transports. The CRC code is calculated using all fields of the TLP, including the Sequence Num‐ ber. The receiver will make the same calculation and compare its result to the LCRC field in the TLP. If they don’t match, an error is detected in the Receiver’s Link Layer. 

## **Replay Buffer** 

The replay buffer, or retry buffer, stores TLPs, including the Sequence Number and LCRC, in the order of their transmission. When the transmitter receives an Ack indicating that TLPs have reached the receiver successfully, it purges from the Replay Buffer those TLPs whose Sequence Number is equal to or earlier than the number in the Ack. In this way, the design allows one Ack to represent several successful TLPs, reducing the number of Acks that must be sent. Since the packets must always be seen in order, then if an Ack is received with a 

**321** 

**PCI Ex ress Technolo p gy** 

Sequence Number of 7, then not only was TLP 7 received successfully, but all the packets before it must also have been received successfully, so there is no reason to keep a copy of them in the replay buffer. 

If a Nak is received, the Sequence Number in the Nak still indicates the last _good_ packet received. So even receiving a Nak can cause the transmitter to purge TLPs from the replay buffer. However, because it is a Nak, it means that some‐ thing was not received successfully at the receiver, so after purging all the acknowledged TLPs, the transmitter must replay everything still in the replay buffer in order. For example, if a Nak is received with a Sequence Number of 9, then packet 9 and all prior packets are purged from the replay buffer, because the receiver acknowledged that they have been successfully received. However, because it is a Nak, the transmitter must then replay all the remaining TLPs in the replay buffer in order, starting with packet 10. 

_Figure 10‐4: Transmitter Elements Associated with the Ack/Nak Protocol_ 

**==> picture [217 x 275] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer (TX) Block TLPs; Report<br>DLL protocol error<br>Yes<br>No<br>TLPs (NTS-AS) ≥ 2048?<br>(Continue)<br>Assign<br>Sequence<br>Number NEXT_TRANSMIT_SEQ (NTS)<br>(Increment)<br>REPLAY_TIMER<br>LCRC Increment on Replay)<br>REPLAY_NUM<br>Generator<br>Purge Older TLPs<br>(Reset Both)<br>Nak AckD_SEQ (AS)<br>Retry (Replay)Buffer Yes Nak? (Update) No<br>(Replay)<br>Yes AckNak<br>SeqNum = AS?<br>(TLP copy)<br>(TLP copy) Yes<br>No Pass<br>(Discard) CRC?<br>Link<br>Block TLP during Replay<br>**----- End of picture text -----**<br>


**322** 

**Cha ter 10: Ack/Nak Protocol p** 

## **REPLAY_TIMER Count** 

This timer is effectively a watchdog timer. It makes sure that the transmitter is receiving Ack/Nak packets for TLPs that have been transmitted. If this timer expires, it means that the transmitter has sent one or more TLPs that it has not received an acknowledgement for in the expected time frame. The fix is to retransmit everything in the replay buffer and restart the REPLAY_TIMER. 

This timer is running anytime a TLP has been transmitted but not yet acknowl‐ edged. If the REPLAY_TIMER is not currently running, it is started when the last Symbol of any TLP is transmitted. If the timer is already running, then sending additional TLPs does not reset the timer value. When an Ack or Nak is received that acknowledges TLPs in the replay buffer, the timer resets back to 0, and if there are still TLPs in the replay buffer (TLPs that have been transmitted, but not yet acknowledged), it immediately starts counting again. However, if an Ack is received that acknowledges the last TLP in the replay buffer, meaning the replay buffer is now empty, the REPLAY_TIMER resets to 0 but does not count. It will not begin counting again until the last Symbol of the next TLP is transmitted. 

## **REPLAY_NUM Count** 

This 2‐bit counter tracks the number of replay attempts after reception of a Nak or a REPLAY_TIMER time‐out. When the REPLAY_NUM count rolls over from 11b to 00b (indicating 4 failed attempts to deliver the same set of TLPs), the Data Link Layer automatically forces the Physical Layer to retrain the Link (LTSSM goes to the Recovery state). When re‐training is finished, it will attempt to send the failed TLPs again. The REPLAY_NUM counter is initialized to 00b at reset, or when the Link Layer is inactive. It is also reset whenever an Ack DLLP is received with a Sequence Number that is more recent than the last one seen, meaning forward progress is being made. 

## **ACKD_SEQ Register** 

This 12‐bit register stores the Sequence Number of the most recently received Ack or Nak. It is initialized to all 1s at reset, or when the Data Link Layer is inac‐ tive. This register is updated with the AckNak_Seq_Num [11:0] field of a received Ack or Nak. The ACKD_SEQ count is compared with the Sequence Number in the last received Ack or Nak to check for forward progress. If the lat‐ est Ack/Nak had a Sequence Number later than the ACKD_SEQ register, then we’re making forward progress. 

**323** 

## **PCI Ex ress Technolo p gy** 

As an aside, we use the term “later Sequence Number” to account for the fact that, like most counters in PCIe, the Sequence Number counters only count for‐ ward, meaning that they’ll eventually roll over back to zero. Technically, a later number would mean a numerically higher value, but we have to remember that when the counter reaches 4095 (it’s a 12‐bit counter), the next higher number will be zero. This wrap‐around effect will be easier to see in the examples later, as in “Ack/Nak Examples” on page 331. 
