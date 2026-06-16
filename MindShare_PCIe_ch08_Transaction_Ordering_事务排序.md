# 📘 第 8 章　事务排序 (Chapter 8. Transaction Ordering)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0257.md` ... `chunks/chunk0263.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Transaction Ordering](#-本章目录-table-of-contents)

<a id="sec-8-1"></a>
## 8.1 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Device A Device B<br>Device Core Device Core<br>PCI-XP Core  PCI-XP Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>Framing C Framing<br>DLLP R<br>(SDP) C (END)<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 DLLP Type (Fields Vary With DLLP Type)<br>Byte 4 16 Bit CRC<br>**----- End of picture text -----**<br>


## **DLLP Packet Size is Fixed at 8 Bytes** 

Data Link Layer Packets are always 8 bytes long for both 8b/10b and 128b/130b and consist of the following components: 

1. A 1 DW core (4 bytes) containing the one‐byte DLLP Type field and three additional bytes of attributes. The attributes vary with the DLLP type. 

2. A 2‐byte CRC value that is calculated based on the core contents of the DLLP. It is important to point out that this CRC is different from the LCRCs added to TLPs. This CRC is only 16 bits in size and is calculated differently than the 32‐bit LCRCs in TLPs. This CRC is appended to the core DLLP and then these 6 bytes are passed to the Physical Layer. 

**310** 

**Chapter 9: DLLP Elements** 

3. If 8b/10b encoding is in use, a Start of DLLP (SDP) control symbol and an End Good (END) control symbol are added to the beginning and end of the packet. As usual, before transmission the Physical Layer encodes the bytes into 10‐bit symbols for transmission. 

4. In Gen3 mode, when 128b/130b encoding is in use, a 2‐byte SDP Token is added to the front of the packet to create the 8‐byte packet and there is no END symbol or token. 

Note that there is never a data payload with a DLLP; all the information is car‐ ried in the core four bytes of the packet. 

## **DLLP Packet Types** 

There are four groups of DLLPs defined that deal with Ack/Nak, Power Man‐ agement, and Flow Control, along with one Vendor Specific version. Some of these have several variants, and Table 9‐1 on page 311 summarizes each variant as well as their _DLLP Type_ field encoding. 

_Table 9‐1: DLLP Types_ 

|**DLLP Type**|**Type Field**<br>**Encoding**|**Purpose**|
|---|---|---|
|Ack (TLP Acknowledge)|0000 0000b|TLP transmission integrity|
|Nak (TLP Negative Acknowl‐<br>edge)|0001 0000b|TLP transmission integrity|
|PM_Enter_L1|0010 0000b|Power Management|
|PM_Enter_L23|0010 0001b|Power Management|
|PM_Active_State_Request_L1|0010 0011b|Power Management|
|PM_Request_Ack|0010 0100b|Power Management|
|Vendor Specific|0011 0000b|Vendor Defined|
|InitFC1‐P|0100 0xxxb|TLP Flow Control<br>(xxx = VC number)|
|InitFC1‐NP|0101 0xxxb|TLP Flow Control|



**311** 

**PCI Ex ress Technolo p gy** 

_Table 9‐1: DLLP Types (Continued)_ 

|**DLLP Type**|**Type Field**<br>**Encoding**|**Purpose**|
|---|---|---|
|InitFC1‐Cpl|0110 0xxxb|TLP Flow Control|
|InitFC2‐P|1100 0xxxb|TLP Flow Control|
|InitFC2‐NP|1101 0xxxb|TLP Flow Control|
|InitFC2‐Cpl|1110 0xxxb|TLP Flow Control|
|UpdateFC‐P|1000 0xxxb|TLP Flow Control|
|UpdateFC‐NP|1001 0xxxb|TLP Flow Control|
|UpdateFC‐Cpl|1010 0xxxb|TLP Flow Control|
|Reserved|Others|Reserved|



## **Ack/Nak DLLP Format** 

The format of the DLLP used by a device to Ack (acknowledge) or Nak (nega‐ tively acknowledge) the receipt of a TLP is illustrated in Figure 9‐3, and its fields are described in “Ack/Nak DLLP Fields” on page 313. For more discus‐ sion on how these are used to handle the Ack/Nak protocol, refer to Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317. 

_Figure 9‐3: Ack Or Nak DLLP Format_ 

**==> picture [366 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved AckNak_Seq_Num<br>Byte 4 16-bit CRC<br>**----- End of picture text -----**<br>


**312** 

**Chapter 9: DLLP Elements** 

_Table 9‐2: Ack/Nak DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:0]|Indicates the type of DLLP:<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|If a good TLP was received:<br>• If incoming Sequence Number =<br>NEXT_RCV_SEQ (matched what was<br>expected), schedule Ack DLLP with that<br>number.<br>• If incoming Sequence Number was ear‐<br>lier than NEXT_RCV_SEQ count (a<br>duplicate TLP was received), schedule<br>Ack DLLP with NEXT_RCV_SEQ ‐ 1<br>(effectively, this is the number of the last<br>good TLP).<br>For a TLP received with a problem:<br>• If the TLP had an error, or its Sequence<br>Number was higher than<br>NEXT_RCV_SEQ, schedule a Nak<br>DLLP with NEXT_RCV_SEQ ‐ 1.|
|16‐bit CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|This 16‐bit CRC protects the contents of<br>this DLLP. Calculation is based on Bytes 0‐<br>3 of the Ack/Nak.|



## **Power Management DLLP Format** 

Power management DLLP information is shown in Figure 9‐4, and its fields are described in Table 9‐3 on page 314. To learn more about the use of these packets in power management, refer to Chapter 16, entitled ʺPower Management,ʺ on page 703. 

**313** 

**PCI Ex ress Technolo p gy** 

_Figure 9‐4: Power Management DLLP Format_ 

**==> picture [372 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1 0 0 x x x Reserved<br>Byte 4 16-bit CRC<br>**----- End of picture text -----**<br>


_Table 9‐3: Power Management DLLP Fields_ 

|**Field**<br>**Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP<br>Type|Byte 0, [7:0]|Indicates DLLP type. For Power Management DLLPs:<br>0010 0000b = PM_Enter_L1<br>0010 0001b = PM_Enter_L23<br>0010 0011b = PM_Active_State_Request_L1<br>0010 0100b = PM_Request_Ack|
|16‐bit<br>CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|A 16‐Bit CRC used to protect DLLP contents. Calcula‐<br>tion is based on Bytes 0‐3, regardless of whether fields<br>are used.|



## **Flow Control DLLP Format** 

Like many other serial transport buses, PCIe improves transport efficiency by using a credit‐based flow control scheme. This topic is covered in detail in Chapter 6, entitled ʺFlow Control,ʺ on page 215. DLLPs are used to communi‐ cate flow control credit information. A variety of different DLLPs initialize flow control credits. Another category of update DLLPs are used to manage the runt‐ ime credit management as receiver buffer space is recovered. There are two Flow Control Initialization DLLPs called InitFC1 and InitFC2, and one Flow Control Update DLLP called UpdateFC. 

The packet format for all three variants is illustrated in Figure 9‐5 on page 315, while Table 9‐4 on page 315 describes the fields contained in it. 

**314** 

**Chapter 9: DLLP Elements** 

_Figure 9‐5: Flow Control DLLP Format_ 

**==> picture [369 x 105] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 x x x x 0 VC ID R HeaderFC R DataFC<br>Byte 4 16-bit CRC<br>**----- End of picture text -----**<br>


_Table 9‐4: Flow Control DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:4]|This code indicates the type of FC DLLP:<br>0100b = InitFC1‐P (Posted Requests)<br>0101b = InitFC1‐NP (Non‐Posted Requests)<br>0110b = InitFC1‐Cpl (Completions)<br>0101b = InitFC2‐P (Posted Requests)<br>1101b = InitFC2‐NP (Non‐Posted Requests)<br>1110b = InitFC2‐Cpl (Completions)<br>1000b = UpdateFC‐P (Posted Requests)<br>1001b = UpdateFC‐NP (Non‐Posted Requests)<br>1010b = UpdateFC‐Cpl (Completions)|
||Byte 0, [3]|Must be 0b as part of flow control encoding.|
||Byte 0, [2:0]|VC ID. Indicates the Virtual Channel (VC 0‐7) to<br>be updated with these credits.|
|HdrFC|Byte 1, [5:0]<br>Byte 2, [7:6]|Contains the credit count for header storage for<br>the specified Virtual Channel. Each credit repre‐<br>sents space for 1 header + the optional TLP Digest<br>(ECRC).|
|DataFC|Byte 2, [3:0]<br>Byte 3, [7:0]|Contains the credit count for data storage for the<br>specified Virtual Channel. Each credit represents<br>16 bytes.|



**315** 

**PCI Ex ress Technolo p gy** 

_Table 9‐4: Flow Control DLLP Fields (Continued)_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|16‐bit CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|A 16‐Bit CRC that protects the contents of this<br>DLLP. Calculation is based on Bytes 0‐3, regard‐<br>less of whether all fields are used.|



## **Vendor-Specific DLLP Format** 

The last defined DLLP type is used for vendor specific purposes. Therefore only the DLLP Type field is defined by the spec (0011 0000b), leaving the remaining contents available for vendor‐defined use. 

_Figure 9‐6: Vendor‐Specific DLLP Format_ 

**==> picture [372 x 99] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 0 1 1 0 0 0 0 Vendor-Defined<br>Byte 4 16-bit CRC<br>**----- End of picture text -----**<br>


**316** 

## _**10 Ack/Nak Protocol**_ 

## **The Previous Chapter** 

In the previous chapter we describe _Data Link Layer Packets_ (DLLPs). We describe the use, format, and definition of the DLLP types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power man‐ agement, flow control mechanism and can be used for vendor‐defined pur‐ poses. 

## **This Chapter** 

This chapter describes a key feature of the Data Link Layer: an automatic, hard‐ ware‐based mechanism for ensuring reliable transport of TLPs across the Link. Ack DLLPs confirm successful reception of TLPs while Nak DLLPs indicate a transmission error. We describe the normal rules of operation when no TLP or DLLP error is detected as well as error recovery mechanisms associated with both TLP and DLLP errors. 

## **The Next Chapter** 

The next chapter describes the Logical sub‐block of the Physical Layer, which prepares packets for serial transmission and reception. Several steps are needed to accomplish this and they are described in detail. This chapter covers the logic associated with the first two spec versions Gen1 and Gen2 that use 8b/10b encoding. The logic for Gen3 does not use 8b/10b encoding and is described separately in the chapter called “Physical Layer ‐ Logical (Gen3)” on page 407. 

## **Goal: Reliable TLP Transport** 

The function of the Data Link Layer (shown in Figure 10‐1 on page 318) is to ensure reliable delivery of TLPs. The spec requires a BER (Bit Error Rate) of no worse than 10[‐12] , but errors will still happen often enough to cause trouble, and a single bit error will corrupt an entire packet. This problem will only become more pronounced as Link rates continue to increase with new generations. 

**317** 

**PCI Ex ress Technolo p gy** 

## _Figure 10‐1: Data Link Layer_ 

**==> picture [375 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
Memory, I/O, Configuration R/W Requests or Message Requests or Completions<br>(Software layer sends / receives address/transaction type/data/message index)<br>Software layer<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Transaction layer Flow Control<br>Transmit Receive<br>Virtual Channel<br>Buffers Buffers<br>per VC Management per VC<br>Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC ACK/NAK CRC ACK/NAK CRC Sequence TLP LCRC<br>Data Link layer TLP Replay De-mux<br>Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical layer Encode Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-8-2"></a>
## 8.2 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-8-3"></a>
## 8.3 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

As shown in Figure 10‐4 on page 322, when an Ack or Nak makes forward progress it causes TLPs with Sequence Numbers equal to or older than the value in the DLLP to be purged out of the Replay Buffer. It also resets both the REPLAY_TIMER and the REPLAY_NUM count. If no forward progress is made, no TLPs can be purged so we only check to see if it’s a Nak that would necessi‐ tate a replay. 

This is a good place to mention a potential problem with the counters: the num‐ ber of TLPs sent might theoretically become much larger than the number that have been acknowledged by the receiver. As mentioned earlier, this is very unlikely; it’s only mentioned here for completeness. The problem is basically the same as it for the Flow Control counters (see “Stage 3 — Counters Roll Over” on page 234) and has the same solution: the NEXT_TRANSMIT_SEQ and ACKD_SEQ counters are never allowed to be separated by more than half their total count value. If a large number of TLPs are sent without acknowledgement so that the NEXT_TRANSMIT_SEQ count value is later than ACKD_SEQ count by 2048, no more TLPs will be accepted from the Transaction Layer until this is resolved by receiving more Acks. If the difference between the Sequence Num‐ ber sent and the acknowledged count ever did exceed half the maximum count value, a Data Link Layer protocol error would be reported. (For more on error reporting, see “Data Link Layer Errors” on page 655.) 

## **DLLP CRC Check** 

This block checks for errors in the 16‐bit CRC of DLLPs. If an error is detected, the DLLP is discarded and a Correctable Error may be reported, if enabled. No further action is taken because there is no mechanism to replay or correct failed DLLPs. Instead, we simply wait for the next successful Ack/Nak, which will get the counters back up‐to‐date and allow normal operation to continue. 

## **Receiver Elements** 

Incoming TLPs are first checked for LCRC errors and then for Sequence Num‐ bers. If there are no errors, the TLP is forwarded to the receiver’s Transaction 

**324** 

**Cha ter 10: Ack/Nak Protocol p** 

Layer. If there are errors, the TLP is discarded and a Nak will be scheduled unless there was already a Nak outstanding. 

Figure 10‐5 on page 325 illustrates the receiver Data Link Layer elements associ‐ ated with processing of inbound TLPs and outbound Ack/Nak DLLPs. 

_Figure 10‐5: Receiver Elements Associated with the Ack/Nak Protocol_ 

**==> picture [223 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- End of picture text -----**<br>


## **LCRC Error Check** 

This block checks for transmission errors in the received TLP by verifying the 32‐bit LCRC. This block calculates an LCRC value based on the received bits of the TLP and then compares the calculated LCRC to the received LCRC. If they match, then all the bits of the packet were received exactly as they were trans‐ mitted. If it doesn’t match, then there was a bit error in the TLP so it gets dropped and a Nak will be sent to get a replay of that packet and any TLPs sent after the bad packet. 

**325** 

**PCI Ex ress Technolo p gy** 

## **NEXT_RCV_SEQ Counter** 

The 12‐bit NEXT_RCV_SEQ (Next Receive Sequence number) counter keeps track of the expected Sequence Number and is used to verify sequential packet reception. It’s initialized to 0 at reset or when the Data Link Layer is inactive, and is incremented once for each good TLP forwarded to the Transaction Layer. TLPs that have errors or were nullified are not sent to the Transaction Layer and therefore don’t increment this counter. 

## **Sequence Number Check** 

If the LCRC check was OK, the TLP’s Sequence Number is checked against the expected count (the NRS number). As can be seen in Figure 10‐5 on page 325, there are three possible outcomes of this check: 

1. The TLP Sequence Number equals the NRS count (the number we’re expecting). In this case, everything is good: the TLP is accepted and for‐ warded to the Transaction Layer and the NRS count is incremented. The Receiver schedules an Ack, but it doesn’t have to be sent until the AckNak_LATENCY_TIMER expires. In the meantime, other good TLPs may be received, incrementing the NEXT_RCV_SEQ counter. Then, once the timer expires, a single Ack is sent with the Sequence Number of the last good TLP received (NRS ‐ 1). That allows one Ack to represent several suc‐ cessful TLPs and reduces overhead, since a dedicated Ack is not required for every TLP. 

2. If the TLP’s Sequence Number is earlier than the NRS count (smaller than expected), this TLP has been seen before and is a duplicate. As long as the expected Sequence Number and received Sequence Number don’t get sepa‐ rated by more than half the total count value (2048), this is not an error, but is seen as a duplicate, meaning the TLP has already been accepted earlier. In this case, the TLP is silently dropped (no Nak, no error reporting) and an Ack is sent with the Sequence Number of the last good TLP it received (NRS ‐ 1). Why would this situation happen? The transmitter may not have received a transmitted Ack, so his REPLAY_TIMER expired and he retrans‐ mitted everything in his Replay Buffer. By sending the transmitter an Ack with the Sequence Number of the last good packet we received, we’re noti‐ fying him of the furthest progress we’ve made. 

3. If the TLP’s Sequence Number is a later Sequence Number than NEXT_RCV_SEQ count (larger than expected), then the Link Layer has missed a TLP. For example, if we’re expecting Sequence Number 30 and the incoming TLP has Sequence Number 31 we know there’s a problem. The numbers must be sequential and, since they aren’t, one must have failed 

**326** 

**Cha ter 10: Ack/Nak Protocol p** 

and been dropped, as might happen at the Physical Layer. This out‐of‐order TLP is discarded, whether or not it had any other errors because we must accept TLPs in order, and a Nak will be sent if there wasn’t one already out‐ standing. 

The concept of the expected sequence number (NRS) incrementing as new TLPs are successfully received and seeing how that affects the sliding windows for the invalid range of sequence numbers and the duplicate range of sequence numbers can be seen in Figure 10‐6. 

_Figure 10‐6: Examples of Sequence Number Ranges_ 

**==> picture [270 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 30 2078 4095<br>Dupli- Invalid<br>Duplicate<br>cate (out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 31 2079 4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>0 32 2080 4095<br>Invalid<br>Duplicate Duplicate<br>(out of sequence)<br>Next Receive<br>Sequence (NRS) Number<br>**----- End of picture text -----**<br>


## **NAK_SCHEDULED Flag** 

This flag is set whenever the receiver schedules a Nak, and is cleared when the receiver successfully receives the TLP with the expected Sequence Number (NRS). The spec is clear that the receiver must not schedule additional Nak DLLPs while the NAK_SCHEDULED flag remains set. The author’s opinion is 

**327** 

**PCI Ex ress Technolo p gy** 

that this is intended to prevent the possibility of an endless loop; a case in which the transmitter begins to replay some packets but the receiver sends another Nak before the replays finish and causes it to restart sending them again. What‐ ever the motivation, once a Nak has been sent there will be no more Naks forth‐ coming until the problem is resolved by successful receipt of the replayed TLP with the correct Sequence Number. 

## **AckNak_LATENCY_TIMER** 

This timer is running anytime a receiver successfully receives a TLP that it has not yet acknowledged. The receiver is required to send an Ack once the timer expires. The length of time the AckNak Latency Timer runs is dictated by the spec (see “AckNak_LATENCY_TIMER” on page 328) and determines how long a receiver can coalesce Acks. Once the AckNak Latency Timer expires, an Ack with sequence number NRS‐1 is generated and sent which indicates the last good packet it received. This timer is reset whenever an Ack or Nak are sent and it only restarts once a new good TLP is received. 

## **Ack/Nak Generator** 

Ack or Nak DLLPs are scheduled by the error checking blocks and contain a 12‐ bit AckNak_Seq_Num field as illustrated in Figure 10‐7 on page 328. It calcu‐ lates this number by subtracting one from the NRS count, which results in reporting the last good Sequence Number received. That’s because a good TLP received increments NRS before scheduling the Ack, while a failed TLP just schedules a Nak without incrementing NRS. This method makes it easier to handle failed packets because the error in the TLP might have been in the Sequence Number, so that number can’t be used in the Nak. Instead, it uses the number of the last good TLP; what we’re expecting minus one. The only case where this value doesn’t represent the last good TLP is for the first TLP after a reset. If that first TLP, using Sequence Number 0, fails, the resulting Nak will have an AckNak_Seq_Num value of zero minus one which results in all 1’s. 

_Figure 10‐7: Ack Or Nak DLLP Format_ 

**==> picture [386 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>0000 0000 - Ack<br>Byte 0 0001 0000 - Nak Reserved AckNak_Seq_Num<br>Byte 4 16-bit CRC<br>**----- End of picture text -----**<br>


**328** 

**Cha ter 10: Ack/Nak Protocol p** 

_Table 10‐1: Ack or Nak DLLP Fields_ 

|**Field Name**|**Header Byte/Bit**|**DLLP Function**|
|---|---|---|
|DLLP Type|Byte 0, [7:0]|Indicates the type:<br>• 0000 0000b = Ack<br>• 0001 0000b = Nak|
|AckNak_Seq_Num|Byte 2, [3:0]<br>Byte 3, [7:0]|This value will always be NEXT_RCV_SEQ<br>count ‐ 1.|
|16‐bit CRC|Byte 4, [7:0]<br>Byte 5, [7:0]|16‐bit CRC used to protect the contents of<br>this DLLP.|



## **Ack/Nak Protocol Details** 

This section describes the detailed transmitter and receiver behavior in process‐ ing TLPs and Ack/Nak DLLPs. Several examples are used to demonstrate vari‐ ous cases that may occur. 

## **Transmitter Protocol Details** 

## **Sequence Number** 

Referring back to Figure 10‐4 on page 322, when TLPs are delivered by the Transaction Layer to the Link Layer, one of the first steps is to append a 12‐bit Sequence Number. Keep in mind that the next incremental Sequence Number may actually be smaller, as will happen when the counter rolls over back to zero after it reaches a maximum value of 4095. Consequently, a value of zero can actually be ‘larger’ than a value of 4095, for example. It may help to think of the Sequence Number comparison as evaluating a ‘window’ of numbers that con‐ sistently moves upward and rolls over. To clarify this concept, such a count roll‐ over is used in several of the upcoming examples. 

## **32-Bit LCRC** 

The transmitter also generates and appends a 32‐bit LCRC (Link CRC) based on the TLP contents (Sequence Number, Header, Data Payload and ECRC). 

**329** 

**PCI Ex ress Technolo p gy** 

## **Replay (Retry) Buffer**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-8-4"></a>
## 8.4 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**General.** Before a device transmits a TLP, it stores a copy of the TLP in the Replay Buffer. ( _Note that the spec uses the term Retry Buffer but in this book ‘Replay’ was chosen instead of ‘Retry’ to more clearly distinguish this mechanism from the old PCI Retry mechanism_ ). Each buffer entry stores a complete TLP with all of its fields including the Sequence Number (12 bits wide, it occu‐ pies two bytes), Header (up to 16 bytes), an optional Data Payload (up to 4KB), an optional ECRC (four bytes) and the LCRC field (four bytes). 

It is important to note that the spec describes the Replay Buffer in this fash‐ ion, but it is NOT a spec requirement that it be implemented this way. As long as your device can replay a sequence of TLPs if required, as defined by the spec, then how that is accomplished within a device is completely up to the designer. Having a Replay Buffer that behaves as described above is one way to accomplish this. 

**Replay Buffer Sizing.** The spec writers chose not to specify the Replay Buffer size, leaving it as an optimization for the device designers. It should be made big enough to store TLPs that haven’t yet been acknowledged by Acks so that under normal operating conditions it doesn’t become full and stall new TLPs coming in from the Transaction Layer, but also small enough to keep the cost down. To determine the optimal buffer size, a designer will consider: 

- Ack DLLP Latency from the receiver. 

- Delays caused by the physical Link. 

- Receiver L0s exit latency to L0. In other words, the buffer should be big enough to hold TLPs without stalling while the Link returns from the L0s state to L0. 

When the transmitter receives an Ack, it purges TLPs from the Replay Buffer with Sequence Numbers equal to or earlier than the Sequence Num‐ ber in the Ack ( _normally this term would be ‘smaller than’ but the counter roll‐ over behavior will sometimes make that an incorrect evaluation, so the term ‘earlier than’ was chosen instead_ ). Similarly, when the transmitter receives a Nak, it still purges the Replay Buffer of TLPs with Sequence Numbers that are equal to or earlier than the Sequence Number that arrives in the Nak, but then it also replays (re‐sends) TLPs of later Sequence Numbers (the remain‐ ing TLPs in the Replay Buffer). 

**330** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Transmitter’s Response to an Ack DLLP** 

A single Ack returned by the receiver may acknowledge multiple TLPs; it isn’t necessary that every TLP transmitted receive a dedicated Ack. The receiver can get multiple good TLPs and send one Ack with the Sequence Number of the last good TLP received. The transmitter’s response to an Ack that makes forward progress (has a Sequence Number that is later than the last one seen) is to load the AckD_SEQ register with the Sequence Number of the new Ack. It also resets the REPLAY_NUM counter and REPLAY_TIMER, and purges the Replay Buffer of all TLPs that were acknowledged by that Ack. 

## **Ack/Nak Examples** 

**Example 1.** Consider Figure 10‐8 on page 332 for the following discus‐ sion. 

1. Device A transmits TLPs with Sequence Numbers 3, 4, 5, 6, 7. 

2. Device B successfully receives TLP 3 and increments its NEXT_RCV_SEQ counter from 3 to 4. Since Device B had previously acknowledged all successfully received TLPs, the AckNak_LATENCY_TIMER was not running. Having received TLP 3, Device B has now successfully received a TLP that it has not acknowl‐ edged, so the AckNak_LATENCY_TIMER is started (this is equivalent of scheduling an Ack). 

3. Device B successfully receives TLPs 4 and 5 before the AckNak_LATENCY_TIMER expires. Receiving TLPs 4 and 5 does NOT reset the AckNak_LATENCY_TIMER. 

4. Once the AckNak_LATENCY_TIMER expires, Device B sends a single Ack with the Sequence Number 5, the last good TLP received. The AckNak_LATENCY_TIMER is reset but does not restart until it suc‐ cessfully receives TLP 6. 

5. Device A receives Ack 5, resets the REPLAY_TIMER and REPLAY_NUM counter, because forward progress is being made. And it purges TLPs from the Replay Buffer that have Sequence Numbers earlier than or equal to 5. 

6. Once Device B receives TLPs 6 and 7 and its AckNak_LATENCY_TIMER expires again, it will send an Ack with a Sequence Number of 7 which will purge the last two TLPs in the Replay Buffer of Device A (according to this example). 

**331** 

## **PCI Ex ress Technolo p gy** 

_Figure 10‐8: Example 1 ‐ Example of Ack_ 

**==> picture [378 x 249] intentionally omitted <==**

**----- Start of picture text -----**<br>
3 Good TLP<br>Receive Buffer<br>4 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>5 Good TLP<br>Replay Buffer 8 NEXT_RCV_SEQ<br>6<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 7<br>6 Ack<br>Purge Lat Tmr<br>5 5<br>4<br>Earlier TLP 3 Ack/Nak<br>Generator<br>Link<br>7 6<br>**----- End of picture text -----**<br>


**Example 2.** This example is showing the exact same behavior as Exam‐ ple 1, but it is pointing out the rollover behavior for the Sequence Numbers, as show in Figure 10‐9 on page 333. 

1. Device A transmits TLPs with Sequence Numbers 4094, 4095, 0, 1, and 2 where TLP 4094 is the first TLP sent and TLP 2 is the last TLP sent in this example. 

2. Device B successfully receives TLPs with Sequence Numbers 4094, 4095, 0, 1 in that order. Reception of TLP 4094 causes the AckNak_LATENCY_TIMER to start. TLPs 4095, 0 and 1 are received before the AckNak_LATENCY_TIMER expires. TLP 2 is still en route. 

3. Because the AckNak_LATENCY_TIMER expires, Device B send an Ack with a Sequence Number of 1 to acknowledge receipt of TLP 1 and all prior TLPs (0, 4095 and 4094 in this example). 

4. Device A successfully receives Ack 1, purges TLPs 4094, 4095, 0, and 1 from the Replay Buffer and resets the REPLAY_TIMER and REPLAY_NUM count. 

**332** 

**Cha ter 10: Ack/Nak Protocol p** 

_Figure 10‐9: Example 2 ‐ Ack with Sequence Number Rollover_ 

**==> picture [381 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>1 Good TLP<br>Replay Buffer 3 NEXT_RCV_SEQ<br>2<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>0<br>Later TLP 2 Ack<br>Purge<br>1 1<br>0 Lat Tmr<br>4095<br>Earlier TLP 4094 Ack/Nak<br>Generator<br>Link<br>2<br>**----- End of picture text -----**<br>


## **Transmitter’s Response to a Nak** 

A Nak indicates that a problem has occurred. When a transmitter receives one, it first purges from the Replay Buffer any TLPs with earlier or equal Sequence Numbers and then replays the remaining TLPs starting with the Sequence Number immediately after the Sequence Number in the Nak. If the Nak caused at least one TLP to be purged from the buffer, then we’ve made forward progress. In that case, the transmitter resets the REPLAY_NUM counter and REPLAY_TIMER and loads the AckD_SEQ register with the Sequence Number of the Nak. 

## **TLP Replay** 

When a Replay becomes necessary, the transmitter blocks acceptance of new TLPs from its Transaction Layer. It then replays the necessary TLPs in the buffer in the same order they were placed into the buffer (like a FIFO). After the replay event, the Data Link Layer unblocks acceptance of new TLPs from its Transac‐ 

**333** 

**PCI Ex ress Technolo p gy** 

tion Layer. The replayed TLPs remain in the buffer until they are finally acknowledged at some later time. 

## **Efficient TLP Replay** 

Ack or Nak DLLPs received during replay must be processed. So there are two main options here, the transmitter may hold them until the replay is finished and then evaluate the Acks or Naks and take the appropriate steps. Another option would be to begin processing the new Ack/Nak DLLPs even during the replay. If this option is used, the newly received Acks might purge some entries from the buffer while replay is in progress, possibly reducing the number of TLPs that need to be replayed and saving time on the Link. This is allowed, but it is important to remember that once a TLP is started for transmission, it must be completed. 

## **Example of a Nak** 

Consider Figure 10‐10 on page 335. 

1. Device A transmits TLPs with Sequence Number 4094, 4095, 0, 1, and 2. 

2. Device B receives TLP 4094 without error and increments the NEXT_RCV_SEQ count to 4095 and starts the AckNak_LATENCY_TIMER. 

3. Device B detects a CRC error in the next TLP received (TLP 4095) and sets the NAK_SCHEDULED flag, which will cause a Nak to be sent with Sequence Number 4094 (NEXT_RCV_SEQ count ‐ 1). Device B does NOT wait until the AckNak_LATENCY_TIMER expires before sending the Nak. It will typically be sent on the next packet boundary. In face, since a Nak is scheduled for transmission, the AckNak_LATENCY_TIMER is stopped and reset. 

4. Device B will continue evaluating incoming TLPs looking for TLP 4095. However, because Device A did not know there was a problem yet, it had sent packets 0, 1 and 2, which Device B will receive. However, Device B will not accept them, even though they may be good TLPs (meaning they did not fail the LCRC check). This is because all packets have to be accepted in order. So Device B will simply drop those pack‐ ets because they are considered out of sequence, but no addition Nak will be sent. Even if one or more of these TLPs fail the LCRC check, no additional NAK is sent. The NAK_SCHEDULED flag is already set and it will only be cleared once Device B successfully receives the TLP it is expecting (TLP 4095 in this example). 

**334** 

**Cha ter 10: Ack/Nak Protocol p** 

5. Device A receives Nak 4094 and purges TLP 4094 and earlier TLPs (none in this example) from the Replay Buffer. Also, since forward progress was made, it resets the REPLAY_TIMER and REPLAY_NUM count. 

6. Since the acknowledge DLLP received was a Nak and not an Ack, Device A then replays all remaining TLPs in the Replay Buffer (TLPs 4095, 0, 1, and 2) and restarts the REPLAY_TIMER and increments the REPLAY_NUM count by one. 

7. Once Device B receives the replayed TLP 4095, it will clear the NAK_SCHEDULED flag, increment the NEXT_RCV_SEQ count and start the AckNak_LATENCY_TIMER. 

_Figure 10‐10: Example of a Nak_ 

**==> picture [372 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
Receive Buffer 4094 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>4095<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 4095 LCRC fail<br>Later TLP 2<br>1<br>0 Lat Tmr<br>4095 Nak 0 Out of sequence<br>Earlier TLP 4094 Purge 4094 Ack/Nak<br>Generator<br>Link<br>Replayed TLPs<br>2 1 0 4095 2 1<br>**----- End of picture text -----**<br>


## **Repeated Replay of TLPs** 

**General.** Each time the transmitter receives a Nak, it replays the buffer contents, and the 2‐bit REPLAY_NUM counter is incremented to keep track of the number of replay events. The replay caused by a Nak in the previous example will increment REPLAY_NUM. 

**335** 

## **PCI Ex ress Technolo p gy** 

If the replay doesn’t clear the problem, though, we enter a new situation. The receiver has set the Nak Scheduled Flag and cannot send any more Acks or Naks until it sees the offending TLP correctly received. If the replay doesn’t make that happen for some reason, then there will be no response from the receiver. What saves us now is the transmitter’s REPLAY_TIMER. When it times out, the entire contents of the Replay Buffer will be resent, the REPLAY_NUM counter will be incremented and the REPLAY_TIMER will be reset and restarted. If the REPLAY_TIMER expires without receiving an Ack or Nak indicating forward progress, this replay process can be repeated up to three times. If after the third replay, there is still no forward progress and the REPLAY_TIMER expires again, this would cause the REPLAY_NUM counter to roll over from 3 back to 0.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-8-5"></a>
## 8.5 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Replay Number Rollover.** When this happens, the assumption is that there must be something wrong with the Link, so the Link Layer trig‐ gers the Physical Layer to re‐train the Link, causing it to go into the Recov‐ ery State (see “Recovery State” on page 571). If the optional Advanced Error Reporting registers are implemented, the Replay Number Rollover error status bit will also be set (“Advanced Correctable Error Handling” on page 688). The Replay Buffer contents are preserved and the Link Layer is not initialized during the re‐training process (this is simply re‐training the Link, not performing a reset of the Link). When re‐training completes, the transmitter resumes the same replay process again in hopes that the prob‐ lem has been cleared and the TLPs can now be replayed successfully. 

The spec does not describe how a device might handle repeated rollover events if the Link training doesn’t clear the problem. The author has seen commercially available hardware that had no mechanism to detect this con‐ dition and got stuck in an endless loop of re‐training. It seems good there‐ fore, to recommend that a device track the number of re‐train attempts. After sufficient attempts, the device could signal an Uncorrectable Fatal Error or an interrupt as a way to notify software of this condition. 

## **Replay Timer** 

The transmitter REPLAY_TIMER is running anytime there are TLPs that have been transmitted but have not yet been acknowledged. The goal of the REPLAY_TIMER is to ensure that TLPs are being acknowledged in a timely fashion. If this timer expires, it indicates that an Ack or Nak should have been received by that point in time, so something must have gone wrong and the fix from the transmitter’s point‐of‐view is to perform a replay, meaning to re‐send everything in the Replay Buffer. 

**336** 

**Cha ter 10: Ack/Nak Protocol p** 

Based on the purpose of this timer, it makes sense that its timeout value should be correlated the AckNak_LATENCY_TIMER in the receiver. In fact, the REPLAY_TIMER is simply three times longer than the AckNak_LATENCY_TIMER. 

A formula in the spec determines the timer’s count value. Its expiration triggers a replay event and increments the REPLAY_NUM counter. A couple of cases where timeout may arise is if an Ack or Nak is lost en route, or because an error in the receiver prevents it from returning an Ack or Nak. Timer‐related rules: 

- If not already running, the timer starts when the last symbol of any TLP is transmitted 

- The timer is reset and restarted when: 

   - An Ack indicating forward progress is received, AND there are still unacknowledged TLPs in the Replay Buffer 

   - A Replay event occurs and the last symbol of the first replayed TLP is sent 

- The timer is reset and held when: 

   - There are no TLPs to transmit, or the Replay Buffer is empty 

   - A Nak is received; it restarts when the last symbol of the first replayed TLP is sent 

   - The timer expires; it restarts when the last symbol of the first replayed TLP is sent 

   - 

   - The Data Link Layer is inactive 

- The timer is held during Link training or re‐training 

**REPLAY_TIMER Equation.** The timeout value depends primarily on the max data payload and the width of the Link. The equation to calculate the REPLAY_TIMER value in symbol times is given below. Note that the value is simply three times the Ack/Nak Latency value. 

. 

( Max_Payload_Size + TLPOverhead ) * AckFactor LinkWidth ( 

+ InternalDelay *** 3** + _Rx_L0s_Adjustment_ ) _this term removed_ ( _for Gen2 and later_ ) 

The equation fields are defined as follows: 

- **Max_Payload_Size** ‐ the value in the Device Control Register. In the case of multiple Functions with different Max_Payload_Size values, the spec recommends using the smallest one of them. 

**337** 

**PCI Ex ress Technolo p gy** 

- **TLP Overhead** ‐ the additional TLP fields beyond the data payload (sequence number, header, digest, LCRC and Start/End framing sym‐ bols). In the spec, the overhead value is treated as a constant of 28 sym‐ bols. 

- **AckFactor** (AF) ‐ is basically a fudge factor representing the number of max payload‐sized TLPs that can be received before an Ack must be sent. The AF value ranges from 1.0 to 3.0 and is intended to balance Link bandwidth efficiency and Replay Buffer size. The table in Figure 10‐11 on page 339 shows the Ack Factor values for various link widths and payload sizes. These Ack Factor values are chosen to allow imple‐ mentations to achieve good performance without requiring a large uneconomical buffer. 

- **LinkWidth** ‐ ranges from x1 (1‐bit wide) to x32 (32‐bits wide). 

- **InternalDelay** ‐ the internal delay of processing a TLP within the receiver and DLLPs (Acks) within the transmitter. This value is defined in the spec in symbol times, and depends on the Link speed: Gen1 = 19, Gen2 = 70, Gen3 = 115. 

- **Rx_L0s_Adjustment** ‐ This is a value that was included in the 1.x PCIe specs but was dropped for 2.0 and later PCIe specs. It could be used to account for the time required by the receive circuits to exit from L0s to L0. Setting the Extended Sync bit of the Link Control register affects the exit time from L0s and must be taken into account in this adjustment. Interestingly, the spec writers chose to assume this to be zero when cre‐ ating their table of Replay Timer values. More on this in the following section. 

**REPLAY_TIMER Summary Table.** Figure 10‐11 on page 339 is a summary table for the Gen1 rate that shows timer load values for various values of the variables in the REPLAY_TIMER equation. The numbers have changed for the newer generations of the spec, and the new tables and a dis‐ cussion of them can be found in the section called “Timing Differences for Newer Spec Versions” on page 350. The tolerance for all of the table values is ‐0% to +100%. 

Note that the table values in the spec (copied here for convenience) are con‐ sidered “unadjusted” because they leave out the last item of the equation involving the time to recover from L0s. No explanation is given for this in the spec, but if the Link had to wake up from L0s to L0 just to replay a packet in case the timeout might have been an error, that would be poor power management. 

**338** 

**Cha ter 10: Ack/Nak Protocol p** 

A simple way to avoid this problem altogether is for the transmitter to ensure that the Replay Buffer is empty before entering L0s. The spec requires that step for entry into L1 but not L0s, and the reason probably has to do with the relative risk involved. Going to L1 requires a longer recovery process back to L0 that has some small risk of failure. If it fails to recover, the Physical Layer state machine will have to do more of the Link training, a process that clears the LinkUp flag to the Link Layer, causing the Link Layer to re‐initialize. If there were entries in the Replay Buffer when that happened they’d be lost and problems could result. The recovery risk from L0s was evidently considered low enough not to warrant that requirement. Still, the L0s latency was left out when the table was constructed, leaving the reader to wonder about this. In the author’s opinion, the spec writers expected designers to take steps to ensure that a Replay Timer timeout either doesn’t occur while in L0s (by emptying the Replay Buffer before L0s entry), or will be delayed if the path for the Acks is observed to be in L0s. 

_Figure 10‐11: Gen1 Unadjusted REPLAY_TIMER Values_ 

||**Max_Payload**<br>**Size**|**X1**<br>**Link**|**X2**<br>**Link**|**X4**<br>**Link**|**X8**<br>**Link**|**X12**<br>**Link**|**x16**<br>**Link**|**X32**<br>**Link**|
|---|---|---|---|---|---|---|---|---|
||**128 Bytes**|**711**|**384**|**219**|**201**|**174**|**144**|**99**|
||**256 Bytes**|**1248**|**651**|**354**|**321**|**270**|**216**|**135**|
||**512 Bytes**|**1677**|**867**|**462**|**258**|**327**|**258**|**156**|
||**1024 Bytes**|**3213**|**1635**|**846**|**450**|**582**|**450**|**252**|
||**2048 Bytes**|**6285**|**3171**|**1614**|**834**|**1095**|**834**|**444**|
||**4096 Bytes**|**12,429**|**6243**|**3150**|**1602**|**2118**|**1602**|**828**|
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||



**339** 

**PCI Ex ress Technolo p gy** 

## **Transmitter DLLP Handling** 

The Ack/Nak Error Checking block determines whether there is an error in the 16‐bit CRC of a received DLLP. If an error is detected, the DLLP is discarded. This is considered a correctable error and may have been set up to be reported in the optional Advanced Error Reporting registers (see Bad DLLP in “Advanced Correctable Error Handling” on page 688), but no further action is taken because this isn’t really a problem. The next successfully received DLLP of that type will bring the counters back up to speed. Consequently, TLPs might be purged a little later than they would have been or a replay may happen at a later time, but no information is lost. Of course, if the delay between successful Acks becomes too large, the REPLAY_TIMER could expire, causing the TLPs to be replayed. 

## **Receiver Protocol Details** 

## **Physical Layer** 

TLPs received at the Physical Layer are checked for receiver errors (such as framing, disparity, and invalid symbols). If there are errors at this level, the TLP is discarded and the Link Layer may be informed by some design‐specific method so it can schedule a Nak and have the packet replayed. If the Link Layer is not informed, then eventually it will detect a Sequence Number violation and that will cause a Nak and a replay. 

**340** 

**Cha ter 10: Ack/Nak Protocol p** 

_Figure 10‐12: Ack/Nak Receiver Elements_ 

**==> picture [224 x 283] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer (RX)<br>Increment NRS Good TLPs<br>NEXT_RCV_SEQ (NRS) Seq Num = NRS<br>Seq Num < NRS (Duplicate TLP) Seq Num<br>(Schedule Ack) >, <, =<br>NRS?<br>Seq Num > NRS (Lost TLP)<br>(Send Nak) Yes<br>(Send Nak) No Pass<br>LCRC?<br>Nak Flag Clear?<br>Set & Send Nak<br>NAK_SCHEDULED Good TLP?<br>Clear Nak Flag<br>Ack Nak<br>Ack/Nak AckNak Latency<br>Generator Timer<br>Link<br>(NRS – 1) = AckNak_Seq_Num[11:0]<br>**----- End of picture text -----**<br>


## **TLP LCRC Check** 

If there were no Physical Layer errors, the Link Layer checks first for CRC errors. The receiver calculates an expected LCRC value from the received TLP (excluding the LCRC field) and compares this value with the TLP’s 32‐bit LCRC. If the two match, the TLP is good. Otherwise, the TLP is discarded and the receiver schedules a Nak. 

## **Next Received TLP’s Sequence Number** 

If the LCRC was correct, the receiver next compares the NEXT_RCV_SEQ counter against the Sequence Number that should be in the newly‐received TLP. Under normal operational conditions, these two numbers will match. If they do, the receiver forwards the TLP to the Transaction Layer, increments the NEXT_RCV_SEQ counter, and schedules an Ack. 

**341** 

**PCI Ex ress Technolo p gy** 

If the received TLP’s Sequence Number turns out to be earlier or later than the NEXT_RCV_SEQ count, we have one of two cases: a duplicate TLP or an out of sequence TLP. 

**Duplicate TLP.** If the Sequence Number of the incoming packet is ear‐ lier (logically smaller) than the expected value, it means the transmitter decided to resend a packet that the receiver has already seen before. This duplicate packet is not an error although we are wasting time on the Link by resending it. This might be caused by a timeout at the transmitter if the Ack or Nak for a previous TLP failed. When this is seen at the receiver, the duplicate packet is discarded and an Ack is scheduled with the Sequence Number of the last good TLP it has received (which is probably not the same Sequence Number in the replayed TLP).

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-8-6"></a>
## 8.6 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Out of Sequence TLP.** If the Sequence Number of the incoming packet is later (logically larger) than the expected value, the only explana‐ tion is that a TLP must have been lost. This is a correctable error and is han‐ dled by sending a Nak. It doesn’t matter if the incoming packet is good because they can only be accepted in correct Sequence Number order. The packet is discarded and the receiver waits for a TLP with the expected Sequence Number. 

The NEXT_RCV_SEQ counter is not incremented when a TLP is received with a CRC error, or was nullified, or for which the Sequence Number check fails. 

A transmitter orders TLPs according to the PCI ordering rules to maintain cor‐ rect program flow and avoid potential deadlock and livelock conditions (see Chapter 8, entitled ʺTransaction Ordering,ʺ on page 285). The Receiver is required to preserve this order and applies these three rules: 

- When the receiver detects a bad TLP, it discards the TLP and all new TLPs that follow in the pipeline until the replayed TLPs are detected. 

- Duplicate TLPs are discarded. 

- TLPs received while waiting for a lost or corrupt TLP are discarded. 

## **Receiver Schedules An Ack DLLP** 

If the Data Link Layer of the receiver does not detect an error in an incoming TLP, it forwards the TLP to the Transaction Layer. The NEXT_RCV_SEQ counter is incremented and the receiver starts the AckNak_LATENCY_TIMER (assuming it was not already running). This is the equivalent of “scheduling an Ack.” The receiver is allowed to continue receiving good TLPs without sending an Ack until the AckNak_LATENCY_TIMER expires. When the timer expires it 

**342** 

**Cha ter 10: Ack/Nak Protocol p** 

sends just one Ack with the Sequence Number of the last good TLP, acknowl‐ edging good receipt of all received TLPs up to the Sequence Number in the cur‐ rent Ack. This technique improves Link efficiency by reducing Ack/Nak traffic. For review, recall that this technique works because the TLPs must always be successfully received in order. 

## **Receiver Schedules a Nak** 

As mentioned earlier in the discussion of the receiver logic (see “Receiver Ele‐ ments” on page 324), when the receiver detects an error on a TLP, it discards the bad packet and sets the NAK_SCHEDULED flag if it was clear, which will cause a Nak to be scheduled with the Sequence Number of NEXT_RCV_SEQ count ‐ 1. Since a Nak is now scheduled, the AckNak_LATENCY_TIMER is reset and halted. Scheduling a Nak can be thought of as being an “edge‐triggered” event instead of a level‐triggered event. It is seeing the rising edge of the NAK_SCHEDULED flag that causes a Nak to be scheduled. Another Nak can‐ not be sent until the next rising edge, which means the NAK_SCHEDULED flag must be cleared (falling edge) first. There are only two events that will clear the NAK_SCHEDULED flag. The first is successfully receiving the expected next TLP (TLP with a Sequence Number that matches the NEXT_RCV_SEQ count). The second is a reset of the link (not retraining, but reset). 

Although it’s important to get the Nak to the transmitter quickly (no other TLPs can be accepted until the failed one is seen without errors), other outgoing TLPs, DLLPs or Ordered Sets already be in progress or have a higher priority than the Nak which means the receiver would have to delay the transmission of the Nak until they’re done (see “Recommended Priority To Schedule Packets” on page 350). In the meantime, if other TLPs arrive at the receiver they are dis‐ carded and no additional Acks or Naks will be scheduled while the NAK_SCHEDULED flag is set. 

## **AckNak_LATENCY_TIMER** 

This timer defines how long a receiver can wait before it must send an Ack for a successfully received TLP (or sequence of TLPs). As stated before, this timer is running anytime a receiver successfully receives a TLP that it has not yet acknowledged. Once the timer expires, an Ack is scheduled for transmission with the Sequence Number of the last good TLP it received. Scheduling an Ack resets the AckNak_LATENCY_TIMER and it only starts counting again once the next TLP is successfully received. 

**343** 

**PCI Ex ress Technolo p gy** 

## **AckNak_LATENCY_TIMER Equation.** 

The timeout value for the AckNak_LATENCY_TIMER is defined by the spec and varies based on the Negotiated Link Width and Max Payload Size Enabled. The equation which defines the timeout is shown below: 

( Max_Payload_Size + TLPOverhead ) * AckFactor 

+ InternalDelay  + _Tx_L0s_Adjustment_ LinkWidth _this term removed_ ( _for Gen2 and later_ ) 

The value in the timer is given in symbol times, the time it takes to send one symbol across the Link: 4ns for Gen1, 2ns for Gen2, and 1ns for Gen3. 

The equation fields are: 

- **Max_Payload_Size** ‐ the value in the Device Control Register. In the case of multiple Functions with different Max_Payload_Size values, the spec recommends using the smallest one of them. 

- **TLPOverhead** ‐ the additional TLP fields beyond the data payload (sequence number, header, digest, LCRC and Start/End framing sym‐ bols). In the spec, the overhead value is treated as a constant of 28 sym‐ bols. 

- **AckFactor** (AF) ‐ is basically a fudge factor representing the number of max payload‐sized TLPs that can be received before an Ack must be sent. The AF value ranges from 1.0 to 3.0 and is intended to balance Link bandwidth efficiency and Replay Buffer size. The table in Figure 10‐11 on page 339 shows the Ack Factor values for various link widths and payload sizes. These Ack Factor values are chosen to allow imple‐ mentations to achieve good performance without requiring a large uneconomical buffer. 

- **LinkWidth** ‐ ranges from x1 (1‐bit wide) to x32 (32‐bits wide).‐ from 1 to 32 Lanes. 

- **InternalDelay** ‐ the internal delay of processing a TLP within the receiver and DLLPs (Acks) within the transmitter. This value is defined in the spec in symbol times, and depends on the Link speed: Gen1 = 19, Gen2 = 70, Gen3 = 115. 

- **Tx_L0s_Adjustment** : ‐ This is a value that was included in the 1.x PCIe specs but was dropped for 2.0 and later PCIe specs. It could be used to account for the time required by the receive circuits to exit from L0s to L0. Setting the Extended Sync bit of the Link Control register affects the exit time from L0s and must be taken into account in this adjustment. Interestingly, the spec writers chose to assume this to be zero when cre‐ ating their table of Replay Timer values. 

**344** 

**Cha ter 10: Ack/Nak Protocol p** 

**AckNak_LATENCY_TIMER Summary Table.** Figure 10‐2 on page 345 shows the Gen1 timer load values for all the possible values used in the AckNak_LATENCY_TIMER equation. Higher data rates change the equation and the resulting table (see “Timing Differences for Newer Spec Versions” on page 350). Like the Replay Timer table, this table is con‐ structed by assuming the L0s adjustment in the equation is zero and then referring to the resulting values as ‘unadjusted’. Note that the tolerance for all of the table values is ‐0% to +100%. 

_Table 10‐2: Gen1 Unadjusted Ack Transmission Latency_ 

|**Max_Payload**<br>**Size**|**X1**<br>**Link**|**X2**<br>**Link**|**X4**<br>**Link**|**X8**<br>**Link**|**X12**<br>**Link**|**x16**<br>**Link**|**X32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|**128 Bytes**|**237**<br>**(AF=1.4)**|**128**<br>**(AF=1.4)**|**73**<br>**(AF=1.4)**|**67**<br>**(AF=2.5)**|**58**<br>**(AF=3.0)**|**48**<br>**(AF=3.0)**|**33**<br>**(AF=3.0)**|
|**256 Bytes**|**416**<br>**(AF=1.4)**|**217**<br>**(AF=1.4)**|**118**<br>**(AF=1.4)**|**107**<br>**(AF=2.5)**|**90**<br>**(AF=3.0)**|**72**<br>**(AF=3.0)**|**45**<br>**(AF=3.0)**|
|**512 Bytes**|**559**<br>**(AF=1.0)**|**289**<br>**(AF=1.0)**|**154**<br>**(AF=1.0)**|**86**<br>**(AF=1.0)**|**109**<br>**(AF=2.0)**|**86**<br>**(AF=2.0)**|**52**<br>**(AF=2.0)**|
|**1024 Bytes**|**1071**<br>**(AF=1.0)**|**545**<br>**(AF=1.0)**|**282**<br>**(AF=1.0)**|**150**<br>**(AF=1.0)**|**194**<br>**(AF=2.0)**|**150**<br>**(AF=2.0)**|**84**<br>**(AF=2.0)**|
|**2048 Bytes**|**2095**<br>**(AF=1.0)**|**1057**<br>**(AF=1.0)**|**538**<br>**(AF=1.0)**|**278**<br>**(AF=1.0)**|**365**<br>**(AF=2.0)**|**278**<br>**(AF=2.0)**|**148**<br>**(AF=2.0)**|
|**4096 Bytes**|**4143**<br>**(AF=1.0)**|**2081**<br>**(AF=1.0)**|**1050**<br>**(AF=1.0)**|**534**<br>**(AF=1.0)**|**706**<br>**(AF=2.0)**|**534**<br>**(AF=2.0)**|**276**<br>**(AF=2.0)**|



## **More Examples** 

In the classroom setting examples often make it much easier to grasp the Ack/ Nak process and so some of them are presented here to illustrate special cases. 

## **Lost TLPs** 

Consider Figure 10‐13 on page 346, showing how a lost TLP is detected and handled. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B successfully receives TLP 4094 so it starts its AckNak_LATENCY_TIMER and increments its NEXT_RCV_SEQ count. After that, it also receives TLPs 4095 and 0. 

**345** 

## **PCI Ex ress Technolo p gy** 

3. After receiving TLP 0, the AckNak_LATENCY_TIMER expires which causes it to schedule an Ack with Sequence Number of 0. 

4. Seeing Ack 0, Device A purges TLPs 4094, 4095, and 0 from its replay buffer. 

5. TLP 1 is lost en route for some reason (maybe the Physical Layer dropped it), and TLP 2 arrives instead. The Sequence Number check shows Device B that TLP 2’s Sequence Number is not equal to the NEXT_RCV_SEQ count but is in the out of sequence range. 

6. Device B discards TLP 2 and sets the NAK_SCHEDULED flag which will send a Nak 0 (NEXT_RCV_SEQ count ‐ 1) in this case. 

7. Upon receipt of Nak 0, Device A replays TLPs 1 and 2. It would purge TLP 0 and any earlier ones in the Replay Buffer, but they were removed earlier so that becomes unnecessary. 

8. TLPs 1 and 2 arrive without error at Device B and are forwarded to the Transaction Layer. 

_Figure 10‐13: Handling Lost TLPs_ 

**==> picture [382 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>1<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Replay 1 2 Out of sequence<br>Later TLP 2<br>1 Ack<br>Purge Lat Tmr<br>0 0<br>4095<br>Earlier TLP 4094 Ack/Nak<br>0 Nak Generator<br>Link<br>Replayed TLPs<br>2 1<br>**----- End of picture text -----**<br>


**346** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Bad Ack** 

Figure 10‐14 on page 347 which shows the protocol for handling a corrupt Ack. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B receives TLPs 4094, 4095, and 0, sets NEXT_RCV_SEQ to 1, and returns Ack 0 because the AckNak_LATENCY_TIMER had expired. 

3. Ack 0 has a bit during its flight on the Link, so when Device A checks its 16‐ bit CRC, it fails the check and is discarded. This means TLPs 4094, 4095, and 0 remain in Device A’s Replay Buffer. 

4. TLPs 1 and 2 arrive at Device B and are good, so NEXT_RCV_SEQ count increments to 3 and Ack 2 is returned once the AckNak_LATENCY_TIMER expires again. 

5. Ack 2 arrives safely at Device A, which purges its Replay Buffer of TLPs 4094, 4095, 0, 1, and 2. 

If Ack 2 is also lost or corrupted and no further Ack or Nak DLLPs are returned to Device A, its REPLAY_TIMER expires causing a replay of its entire buffer. Device B sees TLPs 4094, 4095, 0, 1 and 2 and considers them to be duplicates [their sequence numbers are earlier than NEXT_RCV_SEQ count (3)]. They are discarded and _another_ Ack 2 would be returned to Device A because of the duplicate packets. 

_Figure 10‐14: Handling Bad Ack_ 

**==> picture [368 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-8-7"></a>
## 8.7 Transaction Ordering | 事务排序

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>1<br>REPLAY_TIMER<br>NAK_SCHEDULED<br>Later TLP 2 Replay 1 2 Out of sequence<br>1 Ack<br>Purge Lat Tmr<br>0 0<br>4095<br>Earlier TLP 4094 Ack/Nak<br>0 Nak Generator<br>Link<br>Replayed TLPs<br>2 1<br>**----- End of picture text -----**<br>


**347** 

**PCI Ex ress Technolo p gy** 

## **Bad Nak** 

Figure 10‐15 on page 349 which shows protocol for handling a corrupt Nak. 

1. Device A transmits TLPs 4094, 4095, 0, 1, and 2. 

2. Device B receives TLPs 4094, 4095, and 0 all successfully (and the AckNak_LATENCY_TIMER has not yet expired). The next TLP that it receives fails the LCRC check, so Device B sets the NAK_SCHEDULED flag, and resets and holds the AckNak_LATENCY_TIMER. The Nak is transmit‐ ted back with a Sequence Number of the last good TLP received, 0. 

3. Nak 0 fails the 16‐bit CRC check at Device A and is discarded. 

4. At this point, Device B will not be sending anymore Acks or Naks until it successfully receives the next TLP it is expecting, TLP 1 in this example. However, this will require a replay. Device A does not yet know that a replay is required because the one Nak that was sent back was corrupted and discarded. This gets resolved by the REPLAY_TIMER. The REPLAY_TIMER will eventually expire because it has not seen an Ack or Nak that makes forward progress in the specified time frame. 

5. Once the REPLAY_TIMER expires, Device A will replay all TLPs in the Replay Buffer, increment REPLAY_NUM count and reset and restart the REPLAY_TIMER. 

6. Device B will receive TLPs 4094, 4095 and 0 and recognize that they are duplicates. The duplicate TLPs will be dropped and an Ack will be sched‐ uled with a Sequence Number 0 (indicating the furthest progress made). 

7. Once TLP 1 is successfully received by Device B, it will clear the NAK_SCHEDULED flag, increment the NEXT_RCV_SEQ and restart the AckNak_LATENCY_TIMER because it has successfully received a TLP that it has not yet acknowledged. 

**348** 

**Cha ter 10: Ack/Nak Protocol p** 

## _Figure 10‐15: Handling Bad Nak_ 

**==> picture [383 x 266] intentionally omitted <==**

**----- Start of picture text -----**<br>
4094 Good TLP<br>Receive Buffer 4095 Good TLP<br>0 Good TLP<br>Device A Device B<br>Data Link Layer NEXT_TRANSMIT_SEQ Data Link Layer<br>Replay Buffer 3 NEXT_RCV_SEQ<br>3<br>REPLAY_TIMER<br>(expires) NAK_SCHEDULED<br>1 1 LCRC Fail<br>Later TLP 2<br>1 Replay<br>0 Lat Tmr<br>4095 Nak<br>Earlier TLP 4094 2 CRC Ack/Nak 2 Out of sequence<br>Fail Generator<br>Link<br>Replayed TLPs<br>2 1 0 4095 4094<br>**----- End of picture text -----**<br>


## **Error Situations Handled by Ack/Nak** 

The Ack/Nak protocol guarantees reliable delivery of TLPs despite several pos‐ sible errors. The list of errors below includes the correction mechanism used to resolve them. 

- **LCRC error** in a TLP. **Solution** : Receiver detects LCRC error and schedules a Nak that contains the NEXT_RCV_SEQ count ‐ 1. In response, the trans‐ mitter replays at least one TLP, starting with the one that failed. 

- **TLPs lost** en route to the receiver’s Data Link Layer ( _e.g._ Physical Layer detects issue with packet and drops it). **Solution** : The receiver checks the Sequence Number on all received TLPs, expecting them to arrive with the next sequential Sequence Number. If a TLP is lost, the Sequence Number of the next one that succeeds will be out of sequence. In response, the Receiver 

**349** 

**PCI Ex ress Technolo p gy** 

   - schedules a Nak with NRS count ‐ 1, and the transmitter replays at least one TLP, starting with the missing one. 

- **Corrupted Ack or Nak** en route to the transmitter. **Solution:** The Transmit‐ ter detects a CRC error in the DLLP (see “Receiver handling of DLLPs” on page 309), discards the packet and simply waits for the next one. 

   - **Ack Case:** A subsequent Ack received with a later Sequence Number causes the transmitter Replay Buffer to purge all TLPs with Sequence Numbers equal to or earlier than it. The transmitter is unaware that anything was wrong (except for a potential case of the Replay Buffer temporarily filling up). 

   - **Nak Case:** The receiver, having set the Nak Scheduled flag, will not send another Nak or any Acks until it successfully receives the next expected TLP, meaning a replay is needed. Of course, the transmitter doesn’t know it needs to replay if the Nak was lost. In this case, the REPLAY_TIMER will eventually expire and trigger the replay. 

- **No Ack/Nak seen** within the expected time. **Solution** : REPLAY_TIMER timeout triggers a replay. 

- **Receiver fails to send Ack/Nak** for a received TLP. **Solution** : Again, the transmitter’s REPLAY_TIMER will expire and result in a replay. 

## **Recommended Priority To Schedule Packets** 

A device may have many types of TLPs, DLLPs and Ordered Sets to transmit on a given Link. The recommended priority for scheduling packets is: 

1. Completion of any TLP or DLLP currently in progress (highest priority) 2. Ordered Set 

3. Nak 

4. Ack 

5. Flow Control 

6. Replay Buffer re‐transmissions 

7. TLPs that are waiting in the Transaction Layer 

8. All other DLLP transmissions (lowest priority) 

## **Timing Differences for Newer Spec Versions** 

As mentioned earlier, the timer values for the Ack/Nak protocol are different for Gen2 and later versions of the spec. To improve readability of the text, only the Gen1 versions (2.5 GT/s rate) were included in the earlier discussion, but all three versions are included here for convenience. 

**350** 

**Cha ter 10: Ack/Nak Protocol p** 

As before, the values given are in symbol times, so the actual time is that value multiplied by the time needed to deliver one symbol over the Link at that rate. For review, the time to transmit one symbol (known as a Symbol Time) is 4ns for Gen1, 2ns for Gen2, and 1.25ns to transmit 1 byte for Gen3. 

## **Ack Transmission Latency (AckNak Latency)** 

One interesting difference between the spec versions is the way the L0s recov‐ ery time is considered. In the 1.x specs, an argument is included in the AckNak_LATENCY_TIMER equation to account for this, but the tables in the spec based on that equation put its value at zero and call the resulting values ‘unadjusted’. Beginning with the 2.0 spec, the L0s recovery value is dropped from the equation altogether and the text states that the receiver is not required to adjust Ack scheduling based on L0s exit latency or the value of the Extended Sync bit. None of the table values contain an L0s recovery component and are therefore all still called ‘unadjusted’. 

Note that, since the AF (Ack Factor) values are the same in all the tables and were shown in the earlier presentation of the Gen1 table, they’re not included in the tables here. 

Also, as it was for Gen1, the tolerance for all of the table values is ‐0% to +100%. To illustrate this, Table 10‐3 on page 351 lists the time for a x1 Link and Max Payload size of 128 Bytes as 237 symbol times. Legal values would therefore range from no less than 237 symbol times to no more than 474. 

## **2.5 GT/s Operation** 

_Table 10‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|237|128|73|67|58|48|33|
|256 Bytes|416|217|118|107|90|72|45|
|512 Bytes|559|289|154|86|109|86|52|
|1024 Bytes|1071|545|282|150|194|150|84|
|2048 Bytes|2095|1057|538|278|365|278|148|



**351** 

## **PCI Ex ress Technolo p gy** 

_Table 10‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|4096 Bytes|4143|2081|1050|534|706|534|276|



## **5.0 GT/s Operation** 

_Table 10‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|288|179|124|118|109|99|84|
|256 Bytes|467|268|169|158|141|123|96|
|512 Bytes|610|340|205|137|160|137|103|
|1024 Bytes|1122|596|333|201|245|201|135|
|2048 Bytes|2146|1108|589|329|416|329|199|
|4096 Bytes|4194|2132|1101|585|757|585|327|



## **8.0 GT/s Operation** 

_Table 10‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|333|224|169|163|154|144|129|
|256 Bytes|512|313|214|203|186|168|141|
|512 Bytes|655|385|250|182|205|182|148|
|1024 Bytes|1167|641|378|246|290|246|180|
|2048 Bytes|2191|1153|634|374|461|374|244|
|4096 Bytes|4239|2177|1146|630|802|630|372|



**352** 

**Cha ter 10: Ack/Nak Protocol p** 

## **Replay Timer** 

Much like the AckNak Latency Timer calculation, L0s recovery time is consid‐ ered differently for the Replay Timer in newer spec versions. In the 1.x specs, an argument is included in the Replay Timer equation to account for this, but the tables in the spec based on that equation put its value at zero and call the result‐ ing values ‘unadjusted’. Beginning with the 2.0 spec, the argument is dropped from the equation altogether and the text states that the transmitter should com‐ pensate for L0s exit if it will be used, either by statically adding that time to the table values or by sensing when the Link is in that state and allowing extra time in that case. The table values still don’t contain an L0s component and are still called ‘unadjusted’. 

As a final word on this topic, the spec strongly recommends that a transmitter should not do a replay on a Replay Timer timeout if it’s possible that the delay in receiving an Ack was caused by the other device’s transmitter being in the L0s state. 

Note that, just like for the Ack Latency Timer tables, the tolerance for all of the table values is ‐0% to +100%. To illustrate this, Table 10‐6 on page 353 lists the time for a x1 Link and Max Payload size of 128 Bytes as 711 symbol times. Legal values would therefore range from no less than 711 symbol times to no more than 1422. 

## **2.5 GT/s Operation** 

_Table 10‐6: Gen1 Unadjusted REPLAY_TIMER Values in Symbol Times_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|711|384|219|201|174|144|99|
|256 Bytes|1248|651|354|321|270|216|135|
|512 Bytes|1677|867|462|258|327|258|156|
|1024 Bytes|3213|1635|846|450|582|450|252|
|2048 Bytes|6285|3171|1614|834|1095|834|444|
|4096 Bytes|12429|6243|3150|1602|2118|1602|828|



**353** 

**PCI Ex ress Technolo p gy** 

## **5.0 GT/s Operation** 

_Table 10‐7: Gen2 Unadjusted REPLAY_TIMER Values in Symbol Times_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|864|537|372|354|327|297|252|
|256 Bytes|1401|804|507|474|423|369|288|
|512 Bytes|1830|1020|615|411|480|411|309|
|1024 Bytes|3366|1788|999|603|735|603|405|
|2048 Bytes|6438|3324|1767|987|1248|987|597|
|4096 Bytes|12582|6396|3303|1755|2271|1755|981|



## **8.0 GT/s Operation** 

_Table 10‐8: Gen3 Unadjusted REPLAY_TIMER Values_ 

|Max Payload|x1<br>Link|x2<br>Link|x4<br>Link|x8<br>Link|x12<br>Link|x16<br>Link|x32<br>Link|
|---|---|---|---|---|---|---|---|
|128 Bytes|999|672|507|489|462|432|387|
|256 Bytes|1536|939|642|609|558|504|423|
|512 Bytes|1965|1155|750|546|615|546|444|
|1024 Bytes|3501|1923|1134|738|870|738|540|
|2048 Bytes|6573|3459|1902|1122|1383|1122|732|
|4096 Bytes|12717|6531|3438|1890|2406|1890|1116|



## **Switch Cut-Through Mode**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
