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

