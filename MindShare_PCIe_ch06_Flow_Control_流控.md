# 📘 第 6 章　流控 (Chapter 6. Flow Control)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0244.md` ... `chunks/chunk0253.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Flow Control](#-本章目录-table-of-contents)

<a id="sec-6-1"></a>
## 6.1 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

This chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Trans‐ action Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like discon‐ nects, retries, and wait‐states. 

## **The Next Chapter** 

The next chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different pack‐ ets traversing the fabric. These mechanisms include application‐specific soft‐ ware that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **Flow Control Concept** 

Ports at each end of every PCIe Link must implement Flow Control. Before a packet can be transmitted, flow control checks must verify that the receiving port has sufficient buffer space to accept it. In parallel bus architectures like PCI, transactions are attempted without knowing whether the target is prepared to handle the data. If the request is rejected due to insufficient buffer space, the transaction is repeated (retried) until it completes. This is the “Delayed Transac‐ tion Model” of PCI and while it works the efficiency is poor. 

**215** 

## **PCI Ex ress Technolo p gy** 

Flow Control mechanisms can improve transmission efficiency if multiple Vir‐ tual Channels (VCs) are used. Each Virtual Channel carries transactions that are independent from the traffic flowing in other VCs because flow‐control buffers are maintained separately. Therefore, a full Flow Control buffer in one VC will not block access to other VC buffers. PCIe supports up to 8 Virtual Channels. 

The Flow Control mechanism uses a credit‐based mechanism that allows the transmitting port to be aware of buffer space available at the receiving port. As part of its initialization, each receiver reports the size of its buffers to the trans‐ mitter on the other end of the Link, and then during run‐time it regularly updates the number of credits available using Flow Control DLLPs. Technically, of course, DLLPs are overhead because they don’t convey any data payload, but they are kept small (always 8 symbols in size) to minimize their impact on per‐ formance. 

Flow control logic is actually a shared responsibility between two layers: the Transaction Layer contains the counters, but the Link Layer sends and receives the DLLPs that convey the information. Figure 6‐1 on page 217 illustrates that shared responsibility. In the process of making flow control work: 

- **Devices Report Available Buffer Space** — The receiver of each port reports the size of its Flow Control buffers in units called credits. The number of credits within a buffer is sent from the receive‐side transaction layer to the transmit‐side of the Link Layer. At the appropriate times, the Link Layer creates a Flow Control DLLP to forward this credit information to the receiver at the other end of the Link for each Flow Control Buffer. 

- **Receivers Register Credits** — The receiver gets Flow Control DLLPs and transfers the credit values to the transmit‐side of the transaction layer. The completes the transfer of credits from one link partner to the other. These actions are performed in both directions until all flow control information has been exchanged. 

- **Transmitters Check Credits** — Before it can send a TLP, a transmitter checks the Flow Control Counters to learn whether sufficient credits are available. If so, the TLP is forwarded to the Link Layer but, if not, the trans‐ action is blocked until more Flow Control credits are reported. 

**216** 

**Chapter 6: Flow Control** 

_Figure 6‐1: Location of Flow Control Logic_ 

**==> picture [371 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters FC Buffers FC Counters FC Buffers<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>Link<br>**----- End of picture text -----**<br>


## **Flow Control Buffers and Credits** 

Flow control buffers are implemented for each VC resource supported by a port. Recall that ports at each end of the Link may not support the same number of VCs, therefore the maximum number of VCs configured and enabled by soft‐ ware is the highest common number between the two ports. 

**217** 

**PCI Ex ress Technolo p gy** 

## **VC Flow Control Buffer Organization** 

Each VC Flow Control buffer at the receiver is managed for each category of transaction flowing through the virtual channel. These categories are: 

- Posted Transactions — Memory Writes and Messages 

- Non‐Posted Transactions — Memory Reads, Configuration Reads and Writes, and I/O Reads and Writes 

- Completions — Read and Write Completions 

In addition, each of these categories is separated into header and data portions for transactions that have both header and data. This yields six different buffers each of which implements its own flow control (see Figure 6‐2 on page 218). 

Some transactions, like read requests, consist of a header only while others, like write requests, have both a header and data. The transmitter must ensure that both header and data buffer space is available as needed for a transaction before it can be sent. Note that transaction ordering must be maintained within a VC Flow Control buffer when the transactions are forwarded to software or to an egress port in the case of a switch. Consequently, the receiver must also track the order of header and data components within the buffer. 

_Figure 6‐2: Flow Control Buffer Organization_ 

**==> picture [379 x 224] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Flow Control Buffers (Receiver)<br>Device Core Device Core<br>(PH) (PD) (NPH) (NPD) (CPLH) (CPLD)<br>PCIe-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters RCV Buffers P Posted Request<br>P NP CPL P NP CPL<br>NP Non-Posted Request<br>Data Link Layer Data Link Layer CPL Completion<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>Link<br>**----- End of picture text -----**<br>


**218** 

**Chapter 6: Flow Control** 

## **Flow Control Credits** 

Buffer space is reported by the receiver in units called Flow Control credits. The unit value of Flow Control Credits (FCCs) for header and data buffers are: 

- Header credits — maximum header size + digest 

   - 4 DWs for completions 

   - 5 DWs for requests 

- Data credits — 4 DWs (aligned 16 bytes) 

Flow Control DLLPs communicate this information, and do not require Flow Control credits themselves. That’s because they originate and terminate at the Link Layer and don’t use the Transaction Layer buffers. 

## **Initial Flow Control Advertisement** 

During Flow Control initialization, PCIe devices communicate their buffer sizes by “advertising” their buffer space via flow control credits. PCIe also defines an infinite Flow Control credit value that is required for some buffers. A receiver that advertises infinite buffer space is effectively guaranteeing that its buffer space will never overflow. 

## **Minimum and Maximum Flow Control Advertisement** 

The specification defines the minimum number of credits that can be reported for the different Flow Control buffer types as listed in Table 6‐1. However, devices normally advertise considerably more credits than the minimum. Table 6‐2 on page 220 lists the maximum advertisement allowed by the specifi‐ cation. 

_Table 6‐1: Required Minimum Flow Control Advertisements_ 

|Credit Type|**Minimum Advertisement**|
|---|---|
|Posted Request Header (PH)|1 unit. Credit Value = one 4DW HDR + Digest = 5DW.|
|Posted Request Data (PD)|Largest possible setting of the Max_Payload_Size in<br>credits. Example: If the largest Max_Payload_Size value<br>supported is 1024 bytes, the smallest permitted initial<br>credit value would be 040h.|



**219** 

## **PCI Ex ress Technolo p gy** 

_Table 6‐1: Required Minimum Flow Control Advertisements (Continued)_ 

|Credit Type|**Minimum Advertisement**|
|---|---|
|Non‐Posted Request HDR (NPH)|**1 unit**. Credit Value = one 4 DW HDR + Digest = 5DW.|
|Non‐Posted Request Data (NPD)|**1 unit**. Credit Value = 4DW.<br>**2 unit**. Receivers supporting AtomicOp routing or<br>AtomicOp Completer capability have credit value of 02h|
|Completion HDR (CPLH)|**1 unit**. Credit Value = one 3DW HDR + Digest = 4DW;<br>for Root Complex with peer‐to‐peer support and<br>Switches.<br>**Infinite units.**Initial Credit Value = all 0’s for Root Com‐<br>plex with no peer‐to‐peer support and Endpoints.|
|Completion Data (CPLD)|**n unit**. Value of largest possible setting of<br>Max_Payload_Size or size of largest Read Request<br>(which ever is smaller) divided by FC Unit Size (4DW);<br>for Root Complex with peer‐to‐peer support and<br>Switches.<br>**Infinite units**. Initial Credit Value = all 0’s; for Root<br>Complex with no peer‐to‐peer support and Endpoints.|



_Table 6‐2: Maximum Flow Control Advertisements_ 

|**Credit Type**|**Maximum Advertisement**|
|---|---|
|Posted Request Header (PH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes.|
|Posted Request Data (PD)|2048 units. Value of the Max_Payload_Size (4096 bytes)<br>including all functions supported by device (8) divided<br>by the credit size (4 DWs) = 32,768 bytes<br>2048 credits @ 4 DWs = 32,768 bytes|
|Non‐Posted Request HDR (NPH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes.|
|Non‐Posted Request Data (NPD)|The author’s could not find a precise value for the maxi‐<br>mum number of credits for Non‐Posted Data. The maxi‐<br>mum number of credits listed for Data is 2048. However,<br>a more reasonable approach might use the Non‐Posted<br>header limit of 128 credits, because Non‐Posted Data is<br>always associated with Non‐Posted Headers.|



**220** 

**Chapter 6: Flow Control** 

_Table 6‐2: Maximum Flow Control Advertisements (Continued)_ 

|**Credit Type**|**Maximum Advertisement**|
|---|---|
|Completion HDR (CPLH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes. This in<br>the limit for ports that do not originate transactions (e.g.,<br>Root Complex with peer‐to‐peer support and Switches).<br>**Infinite units**. Initial Credit Value = all 0’s for ports that<br>originate transactions (e.g., Root Complex with no peer‐<br>to‐peer support and Endpoints).|
|Completion Data (CPLD)|**2048 units**. Value of the Max_Payload_Size (4096 bytes)<br>including all functions supported by a device (8)<br>divided by the credit size (4 DWs) = 32,768 bytes<br>2048 credits @ 4 DWs = 32,768 bytes<br>**Infinite units**. Initial Credit Value = all 0’s for ports that<br>originate transactions (e.g., Root Complex with no peer‐<br>to‐peer support and Endpoints).|



## **Infinite Credits** 

Note that a flow control value of 00h will be understood to mean infinite credits during initialization. Following Flow‐Control initialization no further advertise‐ ments are made. Devices that originate transactions must reserve buffer space for the data or status information that will return during split transactions. These transaction combinations include: 

- Non‐posted Read requests and return of Completion Data 

- Non‐posted Read requests and return of Completion Status 

- Non‐posted Write requests and return of Completion Status 

## **Special Use for Infinite Credit Advertisements.**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-2"></a>
## 6.2 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-3"></a>
## 6.3 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- **Credits Received counter (optional)** — tracks the total credits of all TLPs received into the Flow Control buffer. When flow control is functioning properly, the CREDITS_RECEIVED count should be equal to or less than the CREDIT_ALLOCATED count. If this test ever becomes false, a flow con‐ trol buffer overflow has occurred and an error is detected. The spec recom‐ mends that this optional mechanism be implemented and notes that a failure here will be considered a fatal error. 

_Figure 6‐9: Types and Format of Flow Control DLLPs_ 

**==> picture [374 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataFCHdrFC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>1000  Update Posted<br>1001  Update Non Posted<br>1010  Update Completion<br>**----- End of picture text -----**<br>


**229** 

**PCI Ex ress Technolo p gy** 

## **Flow Control Example** 

The following example describes the non‐posted header Flow Control buffer, and attempts to capture the nuances of the flow control implementation in sev‐ eral situations. The discussion of Flow Control is described with a series of basic stages as follows: 

**Stage One** — Immediately following initialization a transaction is transmitted and tracked to explain the basic operation of the counters and registers. 

**Stage Two** — The transmitter sends transactions faster than the receiver can process them and the buffer becomes full. 

**Stage Three** — When counters roll over to zero, the mechanism still works but there are a couple of issues to consider. 

**Stage Four** — The optional receiver error check for a buffer overflow. 

## **Stage 1 — Flow Control Following Initialization** 

Once flow control initialization has completed, the devices are ready for normal operation. The Flow Control buffer in our example is 2KB in size. We’re describ‐ ing the non‐posted header buffer, and each credit is 5 dwords in size or 20 bytes. That means 102d (66h) Flow Control units are available. Figure 6‐10 on page 231 illustrates the elements involved, including the values that would be in each counter and register following flow control initialization. 

When the transmitter is ready to send a TLP, it must first check Flow Control credits. Our example is simple because a non‐posted header is the only packet being sent and it always requires just one Flow Control credit, and we are also assuming that no data is included in the transaction. 

The header credit check is made using unsigned arithmetic (2’s complement), and must satisfy the following formula: 

**==> picture [193 x 13] intentionally omitted <==**

Substituting values from Figure 6‐10 yields: 

66 _h_ –  00 _h_ + 01 _h_  _mod_ 2[8]  2[8]  2 66 _h_ –01 _h mod_ 256  80 _h_ 

**230** 

**Chapter 6: Flow Control** 

_Figure 6‐10: Flow Control Elements Following Initialization_ 

**==> picture [376 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 00h CL = 66h<br>FC<br>Incr Check<br>Buffer<br>Link Packet optional incr<br>Control<br>incr CrRcv=00h CrAl=66h<br>(NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>CrAl = Credits Allocated<br>CC = Credits Consumed<br>CrRcv = Credits Received<br>CL = Credit Limit<br>PTLP = Pending TLP<br>**----- End of picture text -----**<br>


In this case, the current CREDITS_CONSUMED count (CC) is added to the PTLP credits required, to determine the CREDITS_REQUIRED (CR), and that gives 00h + 01h = 01h. The CREDITS_REQUIRED count is subtracted from the CREDIT_LIMIT count (CL) to determine whether or not sufficient credits are available. 

The following description incorporates a brief review of 2’s complement sub‐ traction. When performing subtraction using 2’s complement the number to be subtracted is complemented (1’s complement) and 1 is added (2’s complement). This value is then added to the number from which we wish to subtract. Any carry due to the addition is dropped. 

**231** 

**PCI Ex ress Technolo p gy** 

Credit Check: 

```
CL 01100110b (66h) - CR 00000001b (01h) = n
```

CR is converted to 2’s complement: 

`00000001b` (CR) `11111110b` (CR inverted) `11111110b +1 11111111b` (2’s complement) 

2’s complement added to CL: 

```
01100110 (CL)
11111111(2’s complement of CR)
01100101 = 65h (carry bit is dropped)
```

Is result <= 80h? Yes. If the subtraction result is equal to or less than half the max value, which is tracked with a modulo 256 counter (128), then we know there is sufficient space in the receiver buffer and this packet can be sent. The decision to use only half the counter value avoids a potential count alias problem. See “Stage 3 — Counters Roll Over” on page 234. 

_Figure 6‐11: Flow Control Elements After First TLP Sent_ 

**==> picture [370 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 01h CL = 66h FC<br>Incr Check Buffer<br>Link Packet optional incr<br>Control (NP Hdr)<br>incr CrRcv=01h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


**232** 

**Chapter 6: Flow Control** 

## **Stage 2 — Flow Control Buffer Fills Up** 

Assume now that the receiver has been unable to remove transactions from the Flow Control buffer for some time. Perhaps the device core logic was tempo‐ rarily busy and unable to process transactions. Eventually, the Flow Control buffer becomes completely full, as shown in Figure 6‐12 on page 234. If the transmitter wishes to send another TLP and checks the Flow Control credits: 

Credit Limit (CL)= 66h Credits Required (CR) = 67h 

## `CL 01100110` (66) 

`CR 10011001` (add 2’s complement of 67h) 

`11111111 = FFh<=80h` (not true; don’t send packet) 

This channel is blocked until an Update Flow Control DLLP is received with a new CREDIT_LIMIT value of 67h or greater. When the new valued is loaded into the CL register the transmitter credit check will pass the test and a TLP can be sent. 

- `CL 01100111` (67) 

- `CR 10011001` add 2’s complement of 67 

   - `00000000 = 00h<=80h` (true, send transaction 

**233** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐12: Flow Control Elements with Flow Control Buffer Filled_ 

**==> picture [376 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>CC = 66h CL = 66h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


## **Stage 3 — Counters Roll Over** 

Since the Credit Limit (CL) and Credits Required (CR) counts only increment upward, they eventually roll over back to zero. When CL rolls over and CR has not, the credit check (CL‐CR) results in a small CL value and a large CR value. However, what might appear to be a problem is not when using unsigned arith‐ metic. As described in the previous examples the results are handled correctly when performing 2’s complement subtraction. Figure 6‐13 on page 235 shows the CL and CR counts before and after CL rollover along with the 2’s comple‐ ment results. 

**234** 

**Chapter 6: Flow Control** 

## _Figure 6‐13: Flow Control Rollover Problem_ 

**==> picture [368 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Before CL Rollover After CL Rollover<br>FFh<br>NTS = FF8h (4088d)CL = F8h AS = FE8h (4072d)CR = F8h<br>Available<br>Credit Available<br>NTS<br>Credit is the<br>AS = FE8h (4072d)CR = E8h Rollover<br>sum of these<br>two parts<br>NTS = FF8h (4088d)CL = 08h<br>00h<br>Using 2's complement: Using 2's complement:<br>  CL 11111000 (F8h)   CL 00001000 (08h)<br>+ CR 00011000 (E8h 2’s complement) + CR 00001000 (F8h 2’s complement)<br>  =  00010000 (0Fh)   =  00010000 (0Fh)<br>**----- End of picture text -----**<br>


## **Stage 4 — FC Buffer Overflow Error Check** 

Although it’s optional to do so, the specification recommends implementation of the FC buffer overflow error checking mechanism. Figure 6‐14 on page 236 shows the elements associated with the overflow error check that include: 

- Credits Received (CR) counter 

- Credits Allocated (CA) counter 

- Error Check Logic 

This permits the receiver to track Flow Control credits in the same manner as the transmitter. If flow control is working correctly, the transmitter’s Credits Consumed count will never exceed its Credit Limit, and the receiver’s Credits Received count will never exceed its Credits Allocated count. 

**235** 

**PCI Ex ress Technolo p gy** 

An overflow condition is detected if the following formula evaluates true. Note that the field size is either 8 (headers) or 12 (data): 

**==> picture [161 x 12] intentionally omitted <==**

If it does evaluate true, then more credits have been sent to the FC buffer than were available and an overflow has occurred. Note that the 1.0a version of the specification defines the equation as  rather than > as shown above. That appears to be an error, because when CA = CR no overflow condition exists. 

_Figure 6‐14: Buffer Overflow Error Check_ 

**==> picture [350 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=67h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


**236** 

**Chapter 6: Flow Control** 

## **Flow Control Updates** 

The receiver must regularly update its neighboring device with Flow Control credits that become available when transactions are removed from the buffer. Figure 6‐15 on page 238 illustrates an example where the transmitter was previ‐ ously blocked from sending header transactions because the buffer was full. In the illustration, the receiver has just removed three headers from the Flow Con‐ trol buffer. More space is now available, but the neighboring device is unaware of this. As headers are removed from the buffer, the CREDITS_ALLOCATED count increments from 66h to 69h. This new count is reported to the CREDIT_LIMIT register of the neighboring device using a Flow Control update packet. Once the credit limit has been updated, transmission of additional TLPs can proceed. 

An interesting note here is that the update reports the actual value of the Cred‐ its Allocated register. It would have worked to report just the change in the reg‐ ister, as perhaps “+3 credits on NP Headers” for example, but that represents a potential problem. To understand the risk, consider what would happen if the DLLP containing that increment information was lost for some reason. There is no replay mechanism for DLLPs; if an error occurs the packet is simply dropped. In this case, the increment information would be lost without a means of recovering it. 

If, on the other hand, the actual value of the register is reported instead and the DLLP fails, the next DLLP that succeeds will get the counters back in synchroni‐ zation. In that case some time might be wasted if the transmitter is waiting on the FC credits before it can send the next TLP, but no information is lost. 

**237** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐15: Flow Control Update Example_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-4"></a>
## 6.4 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**==> picture [368 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=69h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


## **FC_Update DLLP Format and Content** 

Recall that Flow Control update packets, like the Flow Control initialization packets, contain two credit fields, one for header and one for data, as shown in Figure 6‐16 on page 239. The receiver’s credit values reported in the HdrFC and DataFC fields may have been updated many times or not at all since the last update packet was sent. 

**238** 

**Chapter 6: Flow Control** 

_Figure 6‐16: Update Flow Control Packet Format and Contents_ 

## **Flow Control Update Frequency** 

The specification defines a variety of rules and suggested implementations that govern when and how often Flow Control Update DLLPs should be sent. These are motivated by a desire to: 

- Notify the transmitting device as early as possible about new credits allo‐ cated, especially if any transactions were previously blocked. 

- Establish worst‐case latency between FC Packets. 

- Balance the requirements associated with flow control operation, such as: — the need to report credits often enough to prevent transaction blocking 

- — the desire to reduce the Link bandwidth needed for FC_Update DLLPs 

- — selecting the optimum buffer size 

   - selecting the maximum data payload size 

- Detect violations of the maximum latency between Flow Control packets. 

Flow Control updates are permitted only when the Link is in the active state (L0 or L0s). All other Link states represent more aggressive power management that have longer recovery latencies. 

## **Immediate Notification of Credits Allocated** 

When a Flow Control buffer is so full that maximum‐sized packets cannot be sent, the spec requires immediate delivery of a FC_Update DLLP when more space becomes available. Two cases exist: 

**239** 

## **PCI Ex ress Technolo p gy** 

- **Maximum Packet Size = 1 Credit.** When packet transmission is blocked due to a buffer full condition for non‐infinite NPH, NPD, PH, and CPLH buffer types, an UpdateFC packet must be scheduled for Transmission when one or more credits are made available (allocated) for that buffer type. 

- **Maximum Packet Size = Max_Payload_Size.** Flow Control buffer space may decrease to the extent that a maximum‐sized packet cannot be sent for non‐infinite PD and CPLD credit types. In this case, when one or more additional credits are allocated, an Update FCP must be scheduled for transmission. 

## **Maximum Latency Between Update Flow Control DLLPs** 

The transmission frequency of Update FCPs for each FC credit type (non‐infi‐ nite) must be scheduled for transmission at least once every 30 μs (‐0%/+50%). If the Extended Sync bit within the Control Link register is set, updates must be scheduled no later than every 120 μs (‐0%/+50%). Note that Update FCPs may be scheduled for transmission more frequently than is required. 

## **Calculating Update Frequency Based on Payload Size and Link Width** 

The specification offers a formula for calculating the frequency at which update packets need to be sent for maximum data payload sizes and Link widths. The formula, shown below, defines FC Update delivery intervals in symbol times. For reference, a symbol time is defined as the time it takes to deliver one sym‐ bol: 4ns for Gen1, 2ns for Gen2, 1ns for Gen3. Table 6‐3, Table 6‐4 and Table 6‐5 show the unadjusted FC Update values for each speed. 

--------------------------------------------------------------------------------------------------------------------------------------- _MaxPayloadSize_ + _TLPOverhead_   _UpdateFactor_ **-** + _InternalDelay LinkWidth_ • **MaxPayloadSize** = The value in the Max_Payload_Size field of the Device Control register 

- **TLPOverhead** = the constant value (28 symbols) representing the additional TLP components that consume Link bandwidth (TLP Prefix, Sequence Number, Packet Header, LCRC, Framing Symbols) 

- **UpdateFactor** = the number of maximum size TLPs sent during the interval between UpdateFC Packets received. This number is intended to balance Link bandwidth efficiency and receive buffer sizes – the value varies with Max_Payload_Size and Link width 

**240** 

**Chapter 6: Flow Control** 

- **LinkWidth** = The number of Lanes the Link is using 

- **InternalDelay** = a constant value of 19 symbol times that represents the internal processing delays for received TLPs and transmitted DLLPs 

The relationship defined by the formula shows that the frequency of update packet delivery decreases as the Linkwidth increases and suggests a timer that triggers scheduling of update packets. Note that this formula does not account for delays associated with the receiver or transmitter being in the L0s power management state. 

_Table 6‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|237<br>UF=1.4|128<br>UF=1.4|73<br>UF=1.4|67<br>UF=2.5|58<br>UF=3.0|48<br>UF=3.0|33<br>UF=3.0|
|256 Bytes|416<br>FC=1.4|217<br>FC=1.4|118<br>UF=1.4|107<br>UF=2.5|90<br>UF=3.0|72<br>UF=3.0|45<br>UF=3.0|
|512 Bytes|559<br>UF=1.0|289<br>UF=1.0|154<br>UF=1.0|86<br>UF=1.0|109<br>UF=2.0|86<br>UF=2.0|52<br>UF=2.0|
|1024 Bytes|1071<br>UF=1.0|545<br>UF=1.0|282<br>UF=1.0|150<br>UF=1.0|194<br>UF=2.0|150<br>UF=2.0|84<br>UF=2.0|
|2048 Bytes|2095<br>UF=1.0|1057<br>UF=1.0|538<br>UF=1.0|278<br>UF=1.0|365<br>UF=2.0|278<br>UF=2.0|148<br>UF=2.0|
|4096 Bytes|4143<br>UF=1.0|2081<br>UF=1.0|1050<br>UF=1.0|534<br>UF=1.0|706<br>UF=2.0|534<br>UF=2.0|276<br>UF=2.0|



_Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|288<br>UF=1.4|179<br>UF=1.4|124<br>UF=1.4|118<br>UF=2.5|109<br>UF=3.0|99<br>UF=3.0|84<br>UF=3.0|
|256 Bytes|467<br>FC=1.4|268<br>FC=1.4|169<br>UF=1.4|158<br>UF=2.5|141<br>UF=3.0|123<br>UF=3.0|96<br>UF=3.0|



**241** 

## **PCI Ex ress Technolo p gy** 

_Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|512 Bytes|610<br>UF=1.0|340<br>UF=1.0|205<br>UF=1.0|137<br>UF=1.0|160<br>UF=2.0|137<br>UF=2.0|103<br>UF=2.0|
|1024 Bytes|1122<br>UF=1.0|596<br>UF=1.0|333<br>UF=1.0|201<br>UF=1.0|245<br>UF=2.0|201<br>UF=2.0|135<br>UF=2.0|
|2048 Bytes|2146<br>UF=1.0|1108<br>UF=1.0|589<br>UF=1.0|329<br>UF=1.0|416<br>UF=2.0|329<br>UF=2.0|199<br>UF=2.0|
|4096 Bytes|4194<br>UF=1.0|2132<br>UF=1.0|1101<br>UF=1.0|585<br>UF=1.0|757<br>UF=2.0|585<br>UF=2.0|327<br>UF=2.0|



_Table 6‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|333<br>UF=1.4|224<br>UF=1.4|169<br>UF=1.4|163<br>UF=2.5|154<br>UF=3.0|144<br>UF=3.0|129<br>UF=3.0|
|256 Bytes|512<br>FC=1.4|313<br>FC=1.4|214<br>UF=1.4|203<br>UF=2.5|186<br>UF=3.0|168<br>UF=3.0|141<br>UF=3.0|
|512 Bytes|655<br>UF=1.0|385<br>UF=1.0|250<br>UF=1.0|182<br>UF=1.0|205<br>UF=2.0|182<br>UF=2.0|148<br>UF=2.0|
|1024 Bytes|1167<br>UF=1.0|641<br>UF=1.0|378<br>UF=1.0|246<br>UF=1.0|290<br>UF=2.0|246<br>UF=2.0|180<br>UF=2.0|
|2048 Bytes|2191<br>UF=1.0|1153<br>UF=1.0|643<br>UF=1.0|374<br>UF=1.0|461<br>UF=2.0|374<br>UF=2.0|244<br>UF=2.0|
|4096 Bytes|4239<br>UF=1.0|2177<br>UF=1.0|1146<br>UF=1.0|630<br>UF=1.0|802<br>UF=2.0|630<br>UF=2.0|372<br>UF=2.0|



The specification recognizes that the formula will be inadequate for many appli‐ cations such as those that stream large blocks of data. These applications may require buffer sizes larger than the minimum specified, as well as a more sophisticated update policy in order to optimize performance and reduce 

**242** 

**Chapter 6: Flow Control** 

power consumption. Because a given solution is dependent on the particular requirements of an application, no definition for such policies is provided. 

## **Error Detection Timer — A Pseudo Requirement** 

The specification defines an optional time‐out mechanism for Flow Control packets that is highly recommended and may become a requirement in future versions of the specification. The maximum latency between FC packets for a given credit type is 120μs, and this timeout has a maximum limit of 200μs. A separate timer is implemented for each FC credit type (P, NP, Cpl), and each timer is reset when a FC Update DLLP of the corresponding type is received. Note that a timer associated with infinite FC credit values must not report an error. 

Apart from the infinite case, a timeout implies a serious problem with the Link. If it occurs, the Physical Layer is signaled to go into the Recovery state and retrain the Link in hopes of clearing the error condition. Timer characteristics include: 

- Operates only when the Link is in an active state (L0 or L0s). 

- Max time limited to 200 μs (‐0%/+50%) 

- Timer is reset when any Init or Update FCP is received, or optionally by receipt of any DLLP. 

- Timeout forces the Physical Layer to enter Link Training and Status State Machine (LTSSM) Recovery state. 

**243** 

**PCI Ex ress Technolo p gy** 

**244** 

_**7**_ 

## _**Quality of Service**_ 

## **The Previous Chapter** 

The previous chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Transaction Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like disconnects, retries, and wait‐states. 

## **This Chapter** 

This chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different pack‐ ets traversing the fabric. These mechanisms include application‐specific soft‐ ware that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **The Next Chapter** 

The next chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock condi‐ tions that must be avoided. 

## **Motivation** 

Many computer systems today don’t include mechanisms to manage band‐ width for peripheral traffic, but there are some applications that need it. One example is streaming video across a general‐purpose data bus, that requires data be delivered at the right time. In embedded guidance control systems timely delivery of video data is also critical to system operation. Foreseeing those needs, the original PCIe spec included Quality of Service (QoS) mecha‐ nisms that can give preference to some traffic flows. The broader term for this is 

**245** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-5"></a>
## 6.5 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Differentiated Service, since packets are treated differently based on an assigned priority and it allows for a wide range of service preferences. At the high end of that range, QoS can provide predictable and guaranteed perfor‐ mance for applications that need it. That level of support is called “isochro‐ nous” service, a term derived from the two Greek words “isos” (equal) and “chronos” (time) that together mean something that occurs at equal time inter‐ vals. To make that work in PCIe requires both hardware and software elements. 

## **Basic Elements** 

Supporting high levels of service places requirements on system performance. For example, the transmission rate must be high enough to deliver sufficient data within a time frame that meets the demands of the application while accommodating competition from other traffic flows. In addition, the latency must be low enough to ensure timely arrival of packets and avoid delay prob‐ lems. Finally, error handling must be managed so that it doesn’t interfere with timely packet delivery. Achieving these goals requires some specific hardware elements, one of which is a set of configuration registers called the Virtual Channel Capability Block as shown in Figure 7‐1. 

_Figure 7‐1: Virtual Channel Capability Registers_ 

**==> picture [368 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
0d<br>63d CapPtr Header<br>PCI Compatible<br>PCIeCapabilityBlock Space<br>PCIe Enhanced Capability Register<br>Port VC Cap Register 1 Ext VC Cnt 255d<br>VATOffset PortVCCapRegister2 VirtualChannel<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VCResourceCap(0) CapabilityStructure<br>VCResourceControlReg(0)<br>VCResourceStatus(0) Reserved PCIe Extended<br>PATnOffset VCResourceCap(n) CapabilitySpace<br>VCResourceControlReg(n)<br>VCResourceStatus(n) Reserved<br>VCArbitrationTable(VAT)<br>PortArbitrationTable0(PAT0) 4095d<br>PortArbitrationTablen(PATn)<br>**----- End of picture text -----**<br>


**246** 

**Chapter 7: Quality of Service** 

## **Traffic Class (TC)** 

The first thing we need is a way to differentiate traffic; something to distinguish which packets have high priority. This is accomplished by designating Traffic Classes (TCs) that define eight priorities specified by a 3‐bit TC field within each TLP header (with ascending priority; TC 0‐7). The 32‐bit memory request header in Figure 7‐2 reveals the location of the TC field. During initialization, the device driver communicates the level of services to the isochronous man‐ agement software, which returns the appropriate TC values to use for each type of packet. The driver then assigns the correct TC priority for the packet. The TC value defaults to zero so packets that don’t need priority service won’t acciden‐ tally interfere with those that do. 

_Figure 7‐2: Traffic Class Field in TLP Header_ 

**==> picture [372 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


Configuration software that’s unaware of PCIe won’t recognize the new regis‐ ters and will use the default TC0/VC0 combination for all transactions. In addi‐ tion, there are some packets that are always required to use TC0/VC0, including Configuration, I/O, and Message transactions. If these packets are thought of as maintenance‐level traffic, then it makes sense that they would need to be con‐ fined to VC0 and kept out of the path of high‐priority packets. 

## **Virtual Channels (VCs)** 

VCs are hardware buffers that act as queues for outgoing packets. Each port must include the default VC0, but may have as many as eight (from VC0 to VC7). Each channel represents a different path available for outgoing packets. 

**247** 

**PCI Ex ress Technolo p gy** 

The motivation for multiple paths is analogous to that of a toll road in which drivers purchase a radio tag that lets them take one of several high priority lanes at the toll booth. Those who don’t purchase a tag can still use the road but they’ll have to stop at the booth and pay cash each time they go through, and that takes longer. If there was only one path, everyone’s access time would be limited by the slowest driver, but having multiple paths available means that those who have priority are not delayed by those who don’t. 

## **Assigning TCs to each VC — TC/VC Mapping** 

The Traffic Class value assigned to each packet travels unchanged to the desti‐ nation and must be mapped to a VC at each service point as it traverses the path to the target. VC mapping is specific to a Link and can change from one Link to another. Configuration software establishes this association during initializa‐ tion using the _TC/VC Map_ field of the VC Resource Control Register. This 8‐bit field permits TC values to be mapped to a selected VC, where each bit position represents the corresponding TC value (bit 0 = TC0, bit 1 = TC1, etc.). Setting a bit assigns the corresponding TC value to the VC ID. Figure 7‐3 on page 249 shows a mapping example where TC0 and TC1 are mapped to VC0 and TC2:TC4 are mapped to VC3. 

Software has a great deal of flexibility in assigning VC IDs and mapping the TCs, but there are some rules regarding the TC/VC mapping: 

- TC/VC mapping must be identical for the two ports attached on either end of the same Link. 

- TC0 will automatically be mapped to VC0. 

- Other TCs may be mapped to any VC. 

- • A TC may **not** be mapped to more than one VC. 

The number of virtual channels used depends on the greatest capability shared by the two devices attached to a given link. Software assigns an ID for each VC and maps one or more TCs to the VCs. 

**248** 

**Chapter 7: Quality of Service** 

_Figure 7‐3: TC to VC Mapping Example_ 

**==> picture [348 x 407] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16 15                                      0<br>PCI Express Extended Capability Header<br>Port VC Capability Register 1<br>Port VC Capability Register 2<br>Port VC Status Register Port VC Control Register<br>PAT Offset VC0 Resource Capability Register<br>VC0 Resource Control Register<br>VC0 Resource Status Reg Reserved<br>PAT Offset VC3 Resource Capability Register<br>VC3 Resource Control Register<br>VC3 Resource Status Reg Reserved<br>31              26 24            19 17 16 15  8 7                     0<br>C0 VCID TC/VC Map<br>2      0 7                         0<br>0 0 0 0 0 0 0 0 0 1 1<br>31              26 24            19 17 16 15  8 7                     0<br>VC3 VCID TC/VC Map<br>2      0 7                         0<br>0 1 1 0 0 0 1 1 1 0 0<br>**----- End of picture text -----**<br>


## **Determining the Number of VCs to be Used** 

Software checks the number of VCs supported by the devices attached to a com‐ mon link and would usually assign the greatest number of VCs that both devices can support. Consider the example topology in Figure 7‐4 on page 250. 

**249** 

## **PCI Ex ress Technolo p gy** 

Here, the switch supports all 8 VCs on each of its ports, while Device A sup‐ ports only the default VC0, Device B supports 4 VC s, and Device C support 8 VCs. Note that even though switch port A supports all 8 VCs, Device A only supports VC0, so 7 VCs are left unused in switch port A. Similarly, only 4 VCs are used by switch port B. 

_Figure 7‐4: Multiple VCs Supported by a Device_ 

**==> picture [369 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>8 VCs supported<br>on each switch port<br>Switch<br>1 VC A C<br>B<br>8 VCs<br>4 VCs<br>Device<br>1 VC supported 8 VCs supported<br>B<br>4 VCs supported<br>A<br>Device<br>C<br>Device<br>**----- End of picture text -----**<br>


Configuration software determines the maximum number of VCs supported by each port interface by reading the _Extended VC Count_ field in the Virtual Chan‐ nel Capability registers, as shown in Figure 7‐5 on page 251. Software checks the Extended VC Count at both ends of the Link and selects the highest common count. Using all the available VCs is not mandatory, though. Software may choose to enable fewer VCs as well. 

**250** 

**Chapter 7: Quality of Service** 

_Figure 7‐5: Extended VCs Supported Field_ 

**==> picture [297 x 304] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header<br>Port VC Capability Register 1<br>Port VC Capability Register 2<br>Port VC Status Register  Port VC Control Register<br>PAT Offset VC0 Resource Capability Register<br>VC0 Resource Control Register<br>VC0 Resource Status Reg  Reserved<br>PAT Offset VCn Resource Capability Register<br>VCn Resource Control Register<br>VCn Resource Status Reg  Reserved<br>2                             0<br>Extended VC Count<br>0 = only VC0 supported<br>1-7 = number of additional<br>         VCs supported<br>**----- End of picture text -----**<br>


## **Assigning VC Numbers (IDs)** 

Configuration software assigns a number (ID) to each of the VCs, except VC0 which is always hardwired. As shown in Figure 7‐3 on page 249, the VC Capa‐ bilities registers include 12 bytes of configuration registers for each VC. The first set of registers always applies to VC0. The _Extended VC Count_ field defines the number of additional VCs implemented by this port, each of which will have a set of registers. The value “n” represents the number of additional VCs imple‐ mented. For example, if the _Extended VC Count_ contains a value of 3, then there are three VCs and register sets in addition to VC0. 

**251** 

**PCI Ex ress Technolo p gy** 

Software assigns a number for each of the additional VCs via the _VC ID_ field. (See Figure 7‐3 on page 249) The IDs don’t have to be contiguous but each num‐ ber can only be used once. 

## **VC Arbitration** 

## **General** 

If a device has more than one VC and they all have a packet ready to send, VC arbitration determines the order of packet transmission. Any of several schemes can be chosen by software from among the options implemented by hardware. The goals are to implement the desired service policy and ensure that all trans‐ actions are making forward progress to prevent inadvertent time‐outs. In addi‐ tion, VC Arbitration is affected by the requirements associated with flow control and transaction ordering. These topics are discussed in other chapters, but they affect arbitration, too, because: 

- Each supported VC provides its own buffers and flow control. 

- Transactions mapped to the same VC are normally passed along in strict order (although there are exceptions, such as when a packet has the “Relaxed Ordering” attribute bit set). 

- Transaction ordering only applies within a VC, so there’s no ordering rela‐ tionship among packets assigned to different VCs. 

The example in Figure 7‐6 on page 253 illustrates two VCs (VC0 and VC1) with a transmission priority based on a 3:1 ratio, meaning three VC1 packets are sent for every one VC0 packet. The device core sends requests (including a TC value) to the TC/VC Mapping logic. Based on the programmed mapping, the packet is placed into the appropriate VC buffer for transmission. Finally, the VC arbiter determines the VC priority for forwarding the packets. This example illustrates the flow in one direction, but the same logic exists for transmitting in the oppo‐ site direction at the same time. 

The VC capability registers provide three basic VC arbitration approaches: 

1. Strict Priority Arbitration — the highest numbered VC with a packet ready always wins.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-6"></a>
## 6.6 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

2. Group Arbitration — VCs are divided by hardware into one low‐priority group and one high‐priority group. The low‐priority group uses an arbitra‐ tion method selected by software from the available choices, while the high‐ priority group always uses strict‐priority arbitration. 

3. Hardware Fixed arbitration — scheme built into the hardware. 

**252** 

**Chapter 7: Quality of Service** 

_Figure 7‐6: VC Arbitration Example_ 

**==> picture [246 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>VC1 VC0<br>Root Complex<br>Memory<br>TC/VC Mapping<br>VC arbitration in this<br>example yields a 3 to 1<br>ratio for transmitting<br>VC1 and VC0.<br>Arbiter<br>VC1 VC0<br>TC/VC Mapping<br>Device<br>Core<br>**----- End of picture text -----**<br>


## **Strict Priority VC Arbitration** 

The default priority scheme is based on the inherent priority of VC IDs (VC0=lowest priority and VC7=highest priority). The mechanism is automatic and requires no configuration. Figure 7‐7 on page 254 illustrates a strict priority arbitration example that includes all VCs. The VC ID governs the order in which transactions are sent. The maximum number of VCs that use strict prior‐ ity arbitration cannot be greater than the value in the _Extended VC Count_ field. 

**253** 

**PCI Ex ress Technolo p gy** 

(See Figure 7‐5 on page 251.) Furthermore, if the designer has chosen strict pri‐ ority arbitration for all VCs supported, the _Low Priority Extended VC Count_ field of Port VC Capability Register 1 is hardwired to zero. (See Figure 7‐8 on page 255. 

_Figure 7‐7: Strict Priority Arbitration_ 

|VC Resources|Priority Order|Priority Order|
|---|---|---|
|8th VC|VC7|Highest|
|7th VC|VC6||
|6th VC|VC5||
|5th VC|VC4||
|4th VC|VC3||
|3rd VC|VC2||
|2nd VC|VC1||
|1st VC|VC0|Lowest|
||||



Strict priority requires that higher‐numbered VCs always get precedence over lower‐priority VCs. For example, if all eight VCs are governed by strict priority, then packets in VC0 can only be sent when no other VCs have packets pending. This achieves the goal of giving the highest priority packets very high band‐ width with minimal latencies. However, strict priority has the potential to starve low‐priority channels for bandwidth, so care must be taken to ensure this doesn’t happen. The spec requires that high priority traffic be regulated to avoid starvation, and gives two possible methods of regulation: 

- The originating port can restrict the injection rate of high priority packets to allow more bandwidth for lower priority transactions. 

- Switches can regulate multiple traffic flows at the egress port. This method may limit the throughput from high bandwidth applications and devices that attempt to exceed the limitations of the available bandwidth. 

A device designer may also limit the number of VCs that participate in strict priority by splitting the VCs into a low‐priority group and a high‐priority group as discussed in the next section. 

**254** 

**Chapter 7: Quality of Service** 

## **Group Arbitration** 

Figure 7‐8 illustrates the _Low Priority Extended VC Count_ field within VC Capa‐ bility Register 1. This read‐only field specifies a VC ID that identifies the upper limit of the low‐priority arbitration group for this device. For example, if this value is 4, then VC0‐VC4 are members of the low‐priority group and VC5‐VC7 are in the high‐priority group. Note that a _Low Priority Extended VC Count_ of 7 means that no strict priority is used. 

_Figure 7‐8: Low‐Priority Extended VCs_ 

**==> picture [333 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header 00h<br>Port VC Capability Register 1  04h<br>Port VC Capability Register 2  08h<br>Port VC Status Register  Port VC Control Register  0Ch<br>PAT Offset VC0 Resource Capability Register  10h<br>VC0 Resource Control Register  14h<br>VC0 Resource Status Reg  Reserved 18h<br>PAT Offset VCn Resource Capability Register  10h+(n*0Ch)<br>VCn Resource Control Register  14h+(n*0Ch)<br>VCn Resource Status Reg  Reserved 18h+(n*0Ch)<br>n = one of the extended VCs<br>31          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP<br>Port Arbitration Table Entry Size<br>Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>**----- End of picture text -----**<br>


**255** 

**PCI Ex ress Technolo p gy** 

As depicted in Figure 7‐10 on page 257, the high‐priority VCs continue to use strict priority arbitration, while the low‐priority arbitration group uses one of the other arbitration methods supported by the device. VC Capability Register 2 reports which alternate methods are supported for this group, as shown in Fig‐ ure 7‐9, and the VC Control Register permits selection of the method to be used. The low‐priority arbitration schemes include: 

- Hardware Based Fixed Arbitration 

- Weighted Round Robin Arbitration (WRR) 

_Figure 7‐9: VC Arbitration Capabilities_ 

**==> picture [304 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                     24  23                            8 7                        0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>7                       4   3     2     1     0<br>RsvdP<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>**----- End of picture text -----**<br>


**==> picture [193 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Control Register<br>15                                 4  3     1 0<br>RsvdP<br>VC Arbitration Select (000b-111b)<br>Load VC Arbitration Table<br>**----- End of picture text -----**<br>


**256** 

**Chapter 7: Quality of Service** 

_Figure 7‐10: VC Arbitration Priorities_ 

|VC Resources|VC IDs|||Split Priority||
|---|---|---|---|---|---|
|||||Highest||
|8th VC|VC7|||||
|7th VC|VC6||High-Priority (Strict Priority Scheme)|||
|5th VC<br>6th VC|VC5<br>VC4|||Low-Priority VC ID = 4||
|4th VC|VC3|||||
|3rd VC|VC2||Low-Priority (Alternate Priority Scheme)<br>(Selected by Software)|||
|||||||
|2nd VC|VC1|||||
|1st VC|VC0|||Lowest||



## **Hardware Fixed Arbitration Scheme** 

This selection defines a hardware‐based method and requires no additional software setup. This method can be anything the hardware designer chooses to build in, and could be based on anticipated loading or band‐ width needs for the device. A simple example might be an ordinary round robin sequence, in which each VC gets an equal turn at sending packets during the rotation. 

## **Weighted Round Robin Arbitration Scheme** 

This is a scheme in which some VCs can be weighted more (given higher priority) than others by giving them more entries in the sequence than oth‐ ers. The spec defines three WRR options, each with a different number of entries (called phases). The table size is selected by writing the correspond‐ ing value in to the _VC Arbitration Select_ field of the Port VC Control Register (see Figure 7‐9 on page 256). Each entry in the table represents one phase that software loads with a low priority VC number. The VC arbiter will repeatedly scan all table entries in a sequential fashion and send packets from the VC specified in the table entries. Once a packet has been sent, the 

**257** 

**PCI Ex ress Technolo p gy** 

arbiter immediately proceeds to the next phase. Figure 7‐11 on page 258 shows an example of a WRR arbitration table with 64 entries. 

_Figure 7‐11: WRR VC Arbitration Table_ 

**==> picture [165 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Phase VC ID<br>0 VC 4<br>1 VC 3<br>2 255 (16KB)VC 2<br>3 VC 1<br>4 VC 4<br>5 VC 3<br>6 VC 0<br>7 64 (4KB)VC 4<br>8 VC 3<br>9 128 (8KB)VC 2<br>10 VC 1<br>1111 VC 4<br>621 VC 3<br>632 VC 0<br>Arbitration Logic Scans Table Entries<br>**----- End of picture text -----**<br>


## **Setting up the Virtual Channel Arbitration Table** 

The location of the VC Arbitration Table (VAT) in configuration space is given as an offset from the base address of the VC Capability Structure, as shown in Figure 7‐12 on page 259. 

As shown in Figure 7‐13 on page 260, each entry in the VAT is a 4‐bit field that identifies the VC number of the buffer that is scheduled to deliver data during that phase. The table length is selected by the arbitration option shown in Figure 7‐9 on page 256. 

**258** 

**Chapter 7: Quality of Service** 

_Figure 7‐12: VC Arbitration Table Offset and Load VC Arbitration Table Fields_ 

**==> picture [331 x 385] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Capability Register 2<br>31                     24  23                                             8 7                      0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>0d<br>Header<br>CapPtr<br>63d<br>PCICompatible<br>PCIe Cap Structure (CapID=10h) Space<br>255d<br>PCIEXEnhancedCapabilityRegister<br>PortVCCapRegister1 ExtVCCnt<br>VATOffset PortVCCapRegister2<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VC0 Resource Cap Reg<br>VC Resource Control Register PCIEXExtended<br>VC Resource Status Reg Reserved CapabilitySpace<br>PATnOffset VCn Resource Cap Reg<br>VC Resource Control Register<br>VC Resource Status Reg Reserved<br>VC Arbitration Table (VAT)<br>4095d<br>**----- End of picture text -----**<br>


The table is loaded by configuration software to achieve the desired priority order for the virtual channels. Hardware sets the _VC Arbitration Table Status_ bit whenever any changes are made to the table, giving software a way to verify whether changes have been made but not yet applied to the hard‐ ware. Once the table is loaded, software sets the _Load VC Arbitration Table_ bit 

**259** 

## **PCI Ex ress Technolo p gy** 

in the Port VC Control register. That causes hardware to load, or apply, the new values to the VC Arbiter. Hardware clears the _VC Arbitration Table Sta‐ tus_ bit when table loading is complete, signaling to software that loading has finished. This method is probably motivated by the desire to change the table contents during run time without disruption. The problem is that con‐ figuration writes are only able to update a dword at a time and are rela‐ tively slow transactions, which means it could take a long time to finish making changes, during which the table is only partially updated. That, in turn, could result in unexpected behavior by the device as it continues to operate during this time. To avoid that, this mechanism allows software to complete all the changes to the table and then apply them all at once to the hardware arbiter. 

_Figure 7‐13: Loading the VC Arbitration Table Entries_ 

|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|31       28 27      24 23      20 19<br>16 15       12 11|8||7|4|3|||0||||
|Phase[2]<br>Phase[3]<br>Phase[4]<br>Phase[5]<br>Phase[6]<br>Phase[7]|||Phase[1]||Phase[0]||||||00h|
|Phase[10]<br>Phase[11]<br>Phase[12]<br>Phase[13]<br>Phase[14]<br>Phase[15]|||Phase[9]||Phase[8]||||||04h|
|Phase[18]<br>Phase[19]<br>Phase[20]<br>Phase[21]<br>Phase[22]<br>Phase[23]|||Phase[17]||Phase[16]||||||08h|
|Phase[26]<br>Phase[27]<br>Phase[28]<br>Phase[29]<br>Phase[30]<br>Phase[31]|||Phase[25]||Phase[24]|||||0Ch||
|<br>1. Configuration Software loads the VC Arbitration Table.<br>2. The VC Arbitration Table Status bit is set when any|3||2|1||0||||||
|table  entry is updated.|RsvdP|||VC ID||||||||
|3. Software sets the Load VC Arbitration Table bit.||||||||||||
|4. Hardware applies table contents to VC Arbiter.||||||||||||
|5. Hardware clears the VC Arbitration Table status bit||||||||||||

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-7"></a>
## 6.7 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|when the table has been loaded into the Arbiter.||||||||||||
|Port VC Control Register<br>Port VC Status Register||||||||||||
|15<br>15                                            1 0||||4||3     1||0||||
|RsvdZ|RsvdP|||||||||||
|VC Arbitration Select (000b-111b)||||||||||||
|Load VC Arbitration<br>VC Arbitration Table Status||||Table||||||||



**260** 

**Chapter 7: Quality of Service** 

## **Port Arbitration** 

## **General** 

Switch ports and root ports will often receive incoming packets that need to be routed to another port. Since packets arriving from multiple ports can all target the same VC in the same outgoing port, arbitration is needed to decide which incoming port’s packet gets next access to that VC. Like VC arbitration, port arbitration has several optional schemes available for selection by configuration software. The combination of TCs, VCs, and arbitration support a range of ser‐ vice levels that fall into two broad categories: 

**1. Asynchronous** — Packets get “best effort” service and may receive no prefer‐ ence at all. Many devices and applications, like mass storage devices, have no stringent requirements for bandwidth or latency and don’t need special timing mechanisms. On the other hand, packets generated by more demanding appli‐ cations can still be prioritized without much trouble by establishing a hierarchy of traffic classes for different packets. Differentiated service is still considered to be asynchronous until the level of service requires guarantees. Naturally, asyn‐ chronous service is always available and doesn’t need any special software or hardware options. 

**2. Isochronous** — When latency and bandwidth guarantees are needed, we move into the isochronous category. This would be useful when a synchronous connection would normally be required between two devices. For example, a CD‐ROM sourcing data from a music CD uses a synchronous connection when a headset is plugged directly into the drive. However, when the audio must be routed across a general‐purpose bus like PCIe to get to external speakers, the connection cannot be synchronous because other traffic may also need to use the same data stream. To achieve an equivalent result, isochronous service must guarantee proper delivery of the time‐sensitive audio data without preventing other traffic from using the Link during the same time. Not surprisingly, spe‐ cialized software and hardware are needed to support this. 

The concept of port arbitration is pictured in Figure 7‐14 on page 262. Note that port arbitration exists in several places in a system: 

- Egress ports of switches 

- Root Complex ports when peer‐to‐peer transactions are supported 

- Root Complex egress ports that lead to targets such as main memory 

**261** 

## **PCI Ex ress Technolo p gy** 

Port arbitration will usually need software configuration for each virtual chan‐ nel supported by a switch or root egress port. In the example below, root port 2 supports peer‐to‐peer transfers from root ports 1 and 2 and therefore needs port arbitration. It should be noted, though, that peer‐to‐peer support between root ports is optional, so it may be that not every root egress port would need port arbitration. 

The connection to system memory is an interesting path. There will likely be packets from multiple ingress ports trying to access this port at the same time, so it needs to support port arbitration. However, it doesn’t use a PCIe port, so it doesn’t have the set of PCIe registers to support arbitration that we’re describ‐ ing here. Instead, the root will need to supply a vendor‐specific set of registers called a Root Complex Register Block (RCRB) to provide the same functionality. 

Because port arbitration is managed independently for each VC of the egress port, a separate table is required for each VC that supports programmable port arbitration, as shown in Figure 7‐15 on page 263. Port arbitration tables are sup‐ ported only by switches and root ports and are not allowed in endpoints. 

_Figure 7‐14: Port Arbitration Concept_ 

**==> picture [368 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Port Arbitration<br>(configured via RCRB)<br>Root Complex<br>Memory<br>1 2 3<br>VC0<br>Port Arbitration<br>Switch<br>(configured via PPB)<br>VC0 VC0<br>VC0 VC0<br>Endpoint Endpoint Endpoint Endpoint<br>A B C D<br>**----- End of picture text -----**<br>


**262** 

**Chapter 7: Quality of Service** 

_Figure 7‐15: Port Arbitration Tables for Each VC_ 

**==> picture [320 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>PAT0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>PATn Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Port Arbitration Table 0 (PAT0)<br>Port Arbitration Table n (PATn)<br>**----- End of picture text -----**<br>


Although it isn’t stated in the spec, the process of arbitrating between different packet streams also implies the use of additional buffers to accumulate traffic from each port in the egress port as illustrated in Figure 7‐16 on page 264. This example illustrates two ingress ports (1 and 2) whose transactions are routed to an egress port (3). The actions taken by the switch include the following: 

1. Packets arriving at the ingress ports are directed to the appropriate flow control buffers (VC) based on the TC/VC mapping. 

2. Packets are forwarded from the flow control buffers to the routing logic, which determines and routes them to the proper egress port. 

3. Packets routed to the egress port (3) use TC/VC mapping to determine into which VC buffer they should be placed. 

4. A set of buffers is associated with each of the ingress ports, allowing the ingress port number to be tracked until port arbitration can be done. 

5. Port arbitration logic determines the order in which transactions are sent from each group of ingress buffers. 

**263** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐16: Port Arbitration Buffering_ 

**==> picture [356 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Ingress Ports Egress Port<br>Port Arbiter<br>Port 2<br>Port 1<br>TC0:TC3 1 VC0 VC0<br>Port 2 VC0 VC Arbiter<br>Port 3 VC0<br>3<br>Port 1<br>VC0<br>TC0:TC1 2 Port 1<br>TC2:TC4 VC7<br>VC5<br>Port 3 Port 2 VC7<br>VC7<br>Port Arbiter<br>TC/VC Mapping Routing Logic<br>TC/VC Mapping<br>TC/VC Mapping Routing Logic<br>**----- End of picture text -----**<br>


## **Port Arbitration Mechanisms** 

The actual port arbitration mechanisms defined are similar to the models used for VC arbitration. Configuration software determines the capability for a port by reading the registers shown in Figure 7‐17 on page 265 and selects the port arbitration scheme to use for each VC. 

**264** 

**Chapter 7: Quality of Service** 

_Figure 7‐17: Software Selects Port Arbitration Scheme_ 

**==> picture [276 x 325] intentionally omitted <==**

**----- Start of picture text -----**<br>
VCn Resource Capability Register<br>31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>7      6    5    4   3     2     1     0<br>Rsvd<br>WRR with 256 Phases (101b)<br>Time-based WRR with 128 Phases (100b)<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>VCn Resource Control Register<br>31              26 24            19 17 16 15  8 7                     0<br>VC<br>RsvdP ID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


## **Hardware-Fixed Arbitration** 

This mechanism doesn’t require software setup. Once selected, it’s managed solely by hardware. The actual arbitration scheme is chosen by the hard‐ ware designer, possibly based on the expected demands for the device. This may simply ensure fairness or it may optimize some aspect of the design, but it doesn’t support differentiated or isochronous services. 

## **Weighted Round Robin Arbitration** 

Just like the weighted round robin mechanism in VC arbitration, software can set up the port arbitration table so that some ports receive more oppor‐ 

**265** 

**PCI Ex ress Technolo p gy** 

tunities than others. This approach assigns different weights to traffic com‐ ing from different ports. 

As the table is scanned, each phase specifies the port number from which the next packet is received. Once the packet is delivered, the arbitration logic immediately proceeds to the next phase. If no transaction is pending transmission for the selected port, the arbiter advances immediately to the next phase. There is no time value associated with these entries. 

Four table lengths are given for WRR port arbitration, determined by the number of phases used by the table. Presumably, a larger number of entries in the table allows for more interesting ratios of arbitration selection. On the other hand, a smaller number of entries would use less storage and cost less. 

## **Time-Based, Weighted Round Robin Arbitration (TBWRR)** 

This mechanism is required for isochronous support. As the name implies, time‐based weighted round robin adds the element of time to each arbitra‐ tion phase. Just as in WRR the port arbiter delivers one transaction from the ingress port VC buffer indicated by the Port Number of the current phase. Now though, rather than immediately advancing to the next phase, the time‐based arbiter waits until the current virtual timeslot elapses before advancing. This ensures that transactions are accepted from the ingress port buffer at regular intervals. If the selected port does not have a packet ready to send then nothing will be sent until the next timeslot. Note that the timeslot does not govern the duration of the transfer, but rather the interval between transfers. The maximum duration of a transaction is the time it takes to complete the round robin and return to the original timeslot. The length of the timeslot may change in the future, but currently has the value of 100ns. 

Time‐based WRR arbitration supports a maximum table length of 128 phases, but the actual number of table entries available for a given VC may be less than that. The value is hardware initialized and reported in the _Max‐ imum Time Slots_ field of each virtual channel that supports TBWRR, as shown in Figure 7‐18 on page 267. 

**266** 

**Chapter 7: Quality of Service** 

_Figure 7‐18: Maximum Time Slots Register_ 

**==> picture [331 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>**----- End of picture text -----**<br>


## **Loading the Port Arbitration Tables** 

The actual size and format of the Port Arbitration Tables are a function of the number of phases and the number of ingress ports supported by the Switch, RCRB, or Root Port that supports peer‐to‐peer transfers. The maximum number of ingress ports supported by the Port Arbitration Table is 256 ports. The actual number of bits within each table entry is design dependent and governed by the number of ingress ports whose transactions can be delivered to the egress port. The size of each table entry is reported in the 2‐bit _Port Arbitration Table Entry Size_ field of Port VC Capability Register 1. The permissible values are: 

- 00b — 1 bit (selects between 2 ports) 

- 01b — 2 bits (4 ports)

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-8"></a>
## 6.8 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- 10b — 4 bits (16 ports) 

- 11b — 8 bits (256 ports) 

Configuration software loads each table with port numbers to accomplish the desired port priority for each VC supported. As illustrated in Figure 7‐19 on page 268, the table format depends on the size of each entry and the number of phases supported by this design. 

**267** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐19: Format of Port Arbitration Tables_ 

**==> picture [339 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
32-Phase Port Arbitration Table<br>with 4-bit entries<br>31       28 27      24 23      20 19 16 15       12 11         8 7          4 3           0<br>Phase[7] Phase[6] Phase[5] Phase[4] Phase[3] Phase[2] Phase[1] Phase[0] 00h<br>Phase[15] Phase[14] Phase[13] Phase[12] Phase[11] Phase[10] Phase[9] Phase[8] 04h<br>Phase[23] Phase[22] Phase[21] Phase[20] Phase[19] Phase[18] Phase[17] Phase[16] 08h<br>Phase[31] Phase[30] Phase[29] Phase[28] Phase[27] Phase[26] Phase[25] Phase[24] 0Bh<br>1. Configuration Software loads the Port Arbitration Table.<br>2. Changes to the table automatically set the Port Arbitration 00b PAT entry is 1 bit (2 ports)<br>Table Status bit.<br>01b PAT entry is 2 bits (4 ports)<br>3. Software sets the Load Port Arbitration Table bit to<br>10b PAT entry is 4 bits (16 ports)<br>     apply the table contents to the hardware.<br>4. Hardware loads table contents into the Port Arbiter, then  11b PAT entry is 8 bits (256 ports)<br>    automatically clears the Port Arbitration Table<br>    status bit when the table has been loaded.<br>VC Resource Status Register  Port VC Capability Register 1<br>15                                       2  1  0  31                                                          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP RsvdP<br>VC Negotiation Pending  Port Arbitration Table Entry Size<br> Port Arbitration Table Status  Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>VC Resource Capability Register<br>31              26 24            19 17 16 15 8 7                     0<br>RsvdP VCID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


**268** 

**Chapter 7: Quality of Service** 

## **Switch Arbitration Example** 

Let’s consider an example of a three‐port switch to illustrate both Port and VC arbitration. The example presumes that packets arriving on ingress ports 0 and 1 are moving in the upstream direction and port 2 is the egress port facing upstream (toward the Root Complex). Refer to Figure 7‐20 on page 270 during the following discussion. 

1. Packets arriving at ingress port 0 are placed in a receiver VC based on the TC/VC mapping for port 0. As shown, TLPs with traffic class TC0 or TC1 are sent to the VC0 buffers. TLPs carrying traffic class TC3 or TC5 are sent to the VC1 buffers. No other TCs are permitted on this link. As an aside, if a packet does arrive with a TC that has not been mapped to an existing VC, it will be treated as an error. 

2. Packets arriving at ingress port 1 are placed in a VC based on TC/VC map‐ ping, too, but it’s not the same for this port. As indicated, TLPs carrying traffic class TC0 are sent to VC0, while TLPs carrying traffic class TC2‐TC4 are sent to VC3. No other TCs are permitted on this link. 

3. In both ports, the target egress port is determined from routing information in each packet. For example, address routing is used in memory or IO request TLPs. 

4. All packets destined for egress port 2 are submitted to the TC/VC mapping logic for that port. As shown, TLPs carrying traffic class TC0‐TC2 are placed into buffers for VC0 that are labeled with their ingress port number, while TLPs carrying traffic class TC3‐TC7 are managed for VC1. 

5. Port Arbitration is applied independently to queued up packets to decide which port’s packets will get loaded next into the real VC. 

6. Finally, VC arbitration determines the order in which transactions in the VC buffers will be sent across the link. 

7. Note that the VC arbiter selects packets for transmission only if sufficient flow control credits exist. 

**269** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐20: Arbitration Examples in a Switch_ 

**==> picture [357 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
Switch<br>(1)<br>TC0,1TC3,5  VC0VC1 0 Of IngressMappingTC/VCPort 0 TC0,1TC3,5 INRESS EGRESS (5)Port Arbitration: VC0Egress Port 2<br>FC Buffer VC0 FC Buffer VC1<br>TLP1 RoutingTLP2 Routing TCTC TLP4 RoutingTLP3 Routing TCTC (4) PacketsPort 0 VC0VC0 ARB (6)<br>Egress Port 2<br>To  Port 1 TC/VC VC Arbitration (7)<br>(2) Determine Egress Port(Using Routing Info) (3) To  Port 2To  Port 3 Of EgressMappingPort 2 VC0VC1 ARB 2 TC0-2TC3-7 VC0VC1<br>TC2-4TC0   VC0VC3 1 Of IngressMappingTC/VCPort 1 TC2-4TC0 TC0-2=>VC0TC3-7=>VC1 (5)Port Arbitration: VC1Egress Port 2<br>FC Buffers VC0 FC Buffers VC3 PacketsPort 1 VC1 ARB<br>TLP3 Routing TLP4 Routing VC1<br>TLP1 Routing TLP2 Routing<br>Determine Egress Port(Using Routing Info) (3) To  Port 0To  Port 2To  Port 3 This logic replicated for each egress port<br>**----- End of picture text -----**<br>


## **Arbitration in Multi-Function Endpoints** 

Another set of registers called Multi‐Function Virtual Channel (MFVC) capabil‐ ity is defined for the specific case of endpoints that will implement QoS in a device with multiple functions. Not surprisingly, this case presents the same arbitration issues internally that a switch port must handle. 

There are two cases described in the spec for this arbitration. In the first case, shown in Figure 7‐21 on page 271, there are two Functions but only Function 0 includes VC Capability registers and the assignments made there are implicitly the same for all functions. For this option, arbitration between the functions will be handled in some vendor‐specific manner. That’s the simplest approach, but doesn’t include a standard structure to define priority between requests from different functions and so it doesn’t support QoS. 

**270** 

**Chapter 7: Quality of Service** 

_Figure 7‐21: Simple Multi‐Function Arbitration_ 

**==> picture [252 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Function 0 Vendor-Specific<br>Arbitration<br>VC Internal Link<br>Capability<br>0002h<br>Egress Port<br>Function 1<br>Internal Link<br>**----- End of picture text -----**<br>


If QoS support is desired, then an MFVC is implemented in VC0 and each func‐ tion has its own unique set of VC Capability registers. To preserve software backward compatibility, the spec states that the VC Capability ID for a device that _does not_ use MFVC must be 0002h, while the VC Capability ID for a device that _does_ implement an MFVC structure must be 0009h. 

Figure 7‐22 on page 272 shows the MFVC register block and a block diagram of an example with two functions in an endpoint whose port supports two VCs. Each function has a Transaction Layer and its own VC Capability registers, but doesn’t implement the lower layers. Instead, they connect to the Transaction Layer of the shared port that does have all the layers. Sharing the hardware interface results in lower cost, of course, and the addition of MFVC allows the functions to handle isochronous traffic. 

As can be seen in the figure, the MFVC registers reside in Function 0 only and define the VCs and arbitration methods to be used for this interface. The MFVC registers look very much the same as VC capability registers and support VC arbitration and Function arbitration. Since packets from multiple functions can attempt to access the same VC at the same time, Function Arbitration decides the priorities among them. That should look familiar by now because it’s the same concept as port arbitration and even uses the same arbitration options, including TBWRR. VC arbitration options are also the same as they are in the single‐function VC registers. 

**271** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐22: QoS Support in Multi‐Function Arbitration_ 

**==> picture [330 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header Cnt<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>Func 0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>Func n Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Function Arbitration Table 0<br>Function Arbitration Table n<br>Function<br>Function 0 Arbiter<br>MFVC Port 1<br>Capability VC0<br>0008h Internal Link<br>Port 2 VC0 VC Arbiter<br>VC<br>Capability VC0<br>0009h<br>Egress<br>Port<br>Function 1<br>Port 1<br>VC7<br>Internal Link<br>VC Port 2 VC7<br>Capability VC7<br>0009h<br>TC/VC Mapping<br>**----- End of picture text -----**<br>


## **Isochronous Support** 

As mentioned earlier, not every machine or application needs isochronous sup‐ port, but there are some that can’t get by without it. Since PCIe was designed to support it from the beginning, let’s consider what would need to be in place to make this work. 

**272** 

**Chapter 7: Quality of Service** 

## **Timing is Everything** 

Consider the example shown in Figure 7‐23 on page 274, where a synchronous connection would be desirable but isn’t possible. Instead, we emulate a synchro‐ nous path with isochronous mechanisms. In this example, isochrony defines the amount of data that will be delivered within each Service Interval to achieve the required service. The following sequence describes the operation: 

1. The synchronous source (video camera and PCI Express interface) accumu‐ lates data in Buffer A during the first of the equal service intervals (SI 1). 

2. The camera delivers all of the accumulated data across the general‐purpose bus during the next service interval (SI 2) while it accumulates the next block of data in Buffer B. 

   - Clearly, the system must be able to guarantee that the entire contents of buffer A can be delivered during the service interval, regardless of whether other traffic is in flight on the Link. This is handled by assigning a high pri‐ ority to the time‐sensitive packets and programming arbitration schemes so they’ll be handled first any time there is competition with other traffic. Also note that, as long as all the data is delivered within the time window, it doesn’t matter exactly when it arrives. It might be spread out across the interval or bunched up in one place inside it. As long as it’s all delivered with the Service Interval the guarantees can still be met. 

3. During SI 2, the tape deck receives and buffers the incoming data, which can then be delivered to storage for recording during SI 3. The camera unloads Buffer B onto the Link during SI 3 while accumulating new data into Buffer A, and the cycle repeats. 

**273** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐23: Example Application of Isochronous Transaction_ 

**==> picture [298 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
Camera<br>SI 1 Data accumulated<br>in Buffer A<br>SI 2 Data from Buffer A<br>delivered while<br>next data accumulates<br>in Buffer B<br>SI 3 Data from Buffer B<br>delivered while next<br>data accumulates in<br>Buffer A<br>PCI Express<br>Interface<br>SI 1 SI 2 SI 3<br>Service Interval (SI)<br>SI 2 Data received into<br>Buffer A<br>SI 3 Data from Buffer A<br>delivered to Storage<br>while data received<br>into Buffer B<br>Storage (e.g.: tape)<br>Buffer A Buffer B<br>Buffer A Buffer B<br>**----- End of picture text -----**<br>


## **How Timing is Defined**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-9"></a>
## 6.9 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Isochronous timing is defined in PCIe by the time slot used in the Time‐Based Weighted Round Robin port arbitration scheme. At present, the time for each slot is 100ns, and represents one entry of the 128 entries in the TBWRR table. Once set up, the arbiter will repeatedly cycle through this table once every 12.8  s, which represents the overall Service Interval. 

Making an isochronous path work as intended requires a few considerations. First, the data packets must be delivered with predictable timing at regular intervals. Second, the maximum amount of isochronous data to be delivered must be known ahead of time and packets must not be allowed to exceed that limit. Third, the Link bandwidth must be sufficient to support the amount of data that needs to be delivered in a given time slot. 

**274** 

**Chapter 7: Quality of Service** 

Consider the following example. A single‐Lane Link running at 2.5 Gbps deliv‐ ers one symbol every 4ns. That allows it to send 25 symbols within a 100ns time slot, but is that enough to be useful? In many cases it’s not, because a TLP may need 28 bytes of overhead for the combination of header, sequence number, LCRC, and so forth. That would mean there isn’t even time to finish sending the overhead, much less any data payload in 100ns. If we needed to send 128 bytes of data, then the bandwidth requirement would be 128+overhead = 156 bytes. One option for solving this problem would be to increase the Link width to 8 Lanes, allowing eight times as many bytes to be sent at once. That change would deliver 200 bytes in 100ns and allow a single time slot to deliver all the isochronous data. Another solution would be to use a single Lane but give the port more time slots, since 8 time slots at the lower Link width would deliver the same amount of data. The choice of solution depends on cost and perfor‐ mance constraints, but the system designer must know the timing and band‐ width requirements of the isochronous path to be able to set it up correctly. 

## **How Timing is Enforced** 

When timing is an integral part of the proper operation of a design, as in the previous example, it is enforced by the combination of things we’ve discussed so far. First, high‐priority TCs must be selected in software and VCs set up in hardware with the mappings between them defined so that only the correct packets will be placed into the high‐priority VCs. Then the desired timing is a matter of programming the arbitration schemes to accommodate the needed bandwidth in the specified time. For example, the choice for VC arbitration would probably be the Strict Priority option, since it’s the only choice that can ensure that a high‐priority packet won’t be delayed by other packets. For Port arbitration the choice must be TBWRR to enforce timing. 

## **Software Support** 

Supporting isochronous service requires some coordination between the soft‐ ware elements in the system. In a PC system, device drivers will report isochro‐ nous requirements and capabilities to the OS, which will then evaluate the overall system demands and allocate resources appropriately. Embedded sys‐ tems will be different, because the all the pieces are known at the outset and software can be simpler. In the following discussion we’ll describe the PC case since an embedded system should simply be a simpler subset of that. 

**275** 

**PCI Ex ress Technolo p gy** 

## **Device Drivers** 

A device driver must be able to report its timing requirements to the software that oversees isochronous operation and obtain permission before trying to use isochronous packets. It’s important to note that driver‐level software should not directly change hardware assignments or arbitration policies on its own, even though it could, because the result would be chaos. If multiple drivers were each independently trying to do this, the last one to make changes would over‐ write any previous assignments. To avoid that, an OS‐level program called an Isochronous Broker receives the timing requests from the system devices and assigns system resources in a coordinated way that accommodates them all. 

## **Isochronous Broker** 

This program manages the end‐to‐end flow of isochronous packets. It receives the isochronous timing requests from device drivers and allocates system resources in a way that accommodates the requests through the target path. In the spec this is referred to as establishing an isochronous contract between the requester/completer pair and the PCIe fabric. Doing so requires verifying that the intended path can indeed support isochronous traffic, and then program‐ ming the appropriate arbitration schemes to ensure it works within the speci‐ fied timing requirements. 

## **Bringing it all together** 

By now it should be reasonably clear what needs to be done to support isochro‐ nous traffic flow in a system, but let’s look at one last example to bring all the pieces together. If we expand on the previous video capture example to show a more complex system, like the one in Figure 7‐24 on page 277, we’ll be able to discuss all the parts that must be in place if the video camera is going to be able to deliver captured data into system memory. This would be a difficult environ‐ ment for isochronous service because there are so many devices that can com‐ pete for bandwidth in the path, but that also makes it useful to illustrate the various things that must be considered. 

## **Endpoints** 

Starting at the bottom, what will be needed in the PCIe interface for the video endpoint device itself? In hardware, more than one VC will be required if we’re going to differentiate packets. Let’s assume a single‐function device for simplic‐ ity. The device driver would need to report the device capabilities and isochro‐ nous timing requirements to the OS‐level Isochronous broker, which would evaluate the system and then report back whether an isochronous contract was possible and which TCs the software should use. 

**276** 

**Chapter 7: Quality of Service** 

_Figure 7‐24: Example Isochronous System_ 

**==> picture [308 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>GFX Root Complex<br>System<br>Memory<br>Switch 2<br>Switch 1<br>Slot<br>Video SCSI<br>Camera<br>Lower<br>Time-<br>priority<br>sensitive<br>data<br>data<br>**----- End of picture text -----**<br>


The driver would then program VC numbers and map the appropriate TCs to each VC. It would also most likely program the VC arbitration to be Strict Prior‐ ity for the high‐priority channels. The one caveat here is that the arbitration must still be “fair”, meaning the low‐priority channels won’t get starved for access. That means the high‐priority VCs can’t have traffic pending constantly but instead must spread out packet injection over time. 

One other observation regarding Link operation is necessary before we finish our discussion of endpoints, and that is regarding Flow Control. The receive buffers of devices in the isochronous path must be large enough to handle the expected packet flow without causing any back pressure as long as packets are injected uniformly according to the Isochronous Contract. In addition, Flow Control Updates must be returned quickly enough to avoid stalls. 

**277** 

**PCI Ex ress Technolo p gy** 

## **Switches** 

Next, consider what would need to be present in each of the switches that reside between the endpoint and the Root Complex. Switches don’t commonly have device drivers, so it would fall to OS‐level software like the Isochronous Broker to read their configuration information and determine what service they sup‐ port. First, all the ports in the isochronous path must support more than one VC, and the TC/VC mapping must match on both ends of each Link. Remember that once the packet gets into the Transaction Layer of the Switch port, only the TC remains with the packet, and the VC assignment for that TC is specific to each port. The TC/VC mapping of the downstream port of Switch 1 must match the mapping of the endpoint, but the other switch port mappings may be differ‐ ent to match the other end of their Links. 

**Arbitration Issues.** The choices for arbitration are straight‐forward. In our example, the isochronous path is shown as carrying traffic in only one direction for simplicity. It is possible to have isochronous traffic flowing in both directions in the case of a memory read, for example, but our example was chosen to resemble the video streaming case. 

VC arbitration for the isochronous egress port will most likely need to use the Strict Priority scheme for the same reasons the endpoint does. Port arbi‐ tration will need to use the Time‐Based WRR scheme, and that means soft‐ ware must understand the proper access ratios and program the Port Arbitration Tables to implement them. This might not be as simple as it sounds if multiple switches are in the path because even though they’ll all use the same TBWRR arbitration scheme, it’s not clear how the service inter‐ vals for each of them would be coordinated. If the SIs are not aligned, mean‐ ing timing guarantees could be more difficult depending on the how busy the Links are. Coordinating the service intervals wasn’t considered in the spec, though, so it would again involve a non‐standard method. Clearly, this problem would be much simpler if we didn’t have multiple switches in an isochronous path. 

**Timing Issues.** Figure 7‐25 on page 279 shows the timing of packets being delivered by the two endpoints for our example. Packets from the video device, with a known size and delivered in regular and predictable inter‐ vals, are shown as the heavier arrows. The smaller, lighter arrows represent packets from the SCSI drive that are lower priority and whose timing is not predictable. In the endpoint, the packets simply need to have the proper TC assigned to them, but a switch needs to ensure that the proper timing policy is enforced. This is done by using TBWRR, which specifies which port will have access at a given time and for how long. Knowing the size and fre‐ 

**278** 

**Chapter 7: Quality of Service** 

quency of the isochronous packets allows software to properly arrange the timing, but what kind of timing is needed? 

_Figure 7‐25: Injection of Isochronous Packets_ 

**==> picture [269 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


First, let’s review the parameters involved by considering a simple example. Recall that PCIe bases a time slot on the reference clock period is given by the Port Capability Register 1 field called Reference Clock. At present the only option for that field is 100ns, and the TBWRR table has no options besides 128 entries. The length of the Service Interval is the multiple of those, making it 12.8  s. The bandwidth for a given device can be expressed by the equation below, where Y is the data to be delivered in one time slot (the spec states that the Max Payload Size programmed during configuration must be used for this bandwidth calculation), M is the number of time slots, and T is the overall Ser‐ vice Interval. If we choose 128 bytes as the payload, and we know that SI is 12.8  s, then the BW = 10 MB/s for each time slot allocated. 

**==> picture [79 x 28] intentionally omitted <==**

Now let’s consider a more realistic example. Let’s say that our Links are running at the Gen2 speed, that the video device needs to have a guaranteed bandwidth of 100MB/s, and that it will send 512 byte packets. Filling in the equation shows M = 2.5 instances of 512 bytes are needed. But how much data can actually be 

**==> picture [324 x 41] intentionally omitted <==**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-10"></a>
## 6.10 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

sent in one time slot? The answer depends on speed and Link width, or course. At 5.0 Gb/s it takes 2ns to send each 10‐bit symbol, so 50 symbols can be deliv‐ ered per Lane in 100ns. If the packet size is 512 bytes of data plus another 28 or so for the header, then 11 time slots would be needed to deliver 550 symbols for one packet using a x1 Link. It is possible to give one port several contiguous 

**279** 

## **PCI Ex ress Technolo p gy** 

slots if needed, so that’s one solution. Since the packet size that will be sent is always the same, we can’t really program 2.5 instances of it, so we’d have to use 3 instead. From our equation, 3 instances of 512 bytes each results in an actual bandwidth of 120MB/s. That’s higher than we need, but it solves the problem. The number of time slots used would then be 11 x 3 = 33, leaving 95 for other use in the Service Interval. Each group of 11 time slots would need to be contig‐ uous but the groups could be spaced out over the service interval. 

Another solution would be increase the Link width. Although the hardware would cost more, using 11 Lanes would allow delivery of all the data in one time slot. The CEM spec doesn’t currently support a x11 option, but a x12 option is available and would work for our example. Using a wide Link like that means software would only need to program one time slot for each packet, and just three over the whole service interval to support isochronous traffic for this device. Unlike the x1 case, now we wouldn’t need contiguous time slots. Instead, they could be spaced over the service interval in some optimal fashion. 

**Bandwidth Allocation Problems.** The TBWRR table must be pro‐ grammed to guarantee sufficient timely bandwidth for isochronous traffic, and that other traffic won’t be allowed to interfere. In Figure 7‐25 on page 279, the SCSI controller is shown as sending one packet in SI 1 and another in SI 3. If the timing was such that one packet from that endpoint per SI was allowed then this works fine. 

Now let’s say the SCSI controller attempts to inject more packets than it has permission to do in SI 1, illustrated in Figure 7‐26 on page 280. This is the first of two bandwidth allocation problems mentioned in the spec and is called “oversubscription.” This could interfere with isochronous traffic flow, but programming the TBWRR table readily avoids that problem because the arbitration only allows a packet from that port at specific times. If more packets from that port are queued up, they simply have to wait until the next available time, which might be in SI 2, as shown in this exam‐ ple. Eventually, this can result in flow control back‐pressure at the sending agent 

_Figure 7‐26: Over‐Subscribing the Bandwidth_ 

**==> picture [263 x 94] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**280** 

**Chapter 7: Quality of Service** 

The second timing problem is called “congestion” and happens when too many isochronous requests are sent within a given time window, as shown in Figure 7‐27 on page 281. This is a similar problem but now there is no simple solution. Unlike the previous case, postponing high‐priority packets until another time slot is not an option, so the system must make an effort to handle them all. The result is that some requests may experience excessive service latencies. To correct this, software would need to change the distri‐ bution of packets so that they can be supported by the available hardware bandwidth. 

_Figure 7‐27: Bandwidth Congestion_ 

**==> picture [263 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**Latency Issues .** Managing latency for packet delivery is an important part of isochrony, and involves the combination of the fabric latency and the Completer latency. Fabric latency depends on all the characteristics of the Link between the various components in the system, especially the Link width and frequency of operation. A simple way to minimize this value is to constrain the complexity of the PCIe topology for isochronous paths. Completer latency depends on the target endpoint internal characteristics, such as memory speed and internal arbitration. 

## **Root Complex** 

The RC has the same arbitration and timing requirements as a switch. It receives packets on several downstream ports and forwards them to the target in a way that’s consistent with the rules for isochrony described earlier. However, much of how this is done will be vendor specific because the spec doesn’t define the RC or how it should be programmed. 

**Problem: Snooping.** One interesting thing affecting timing and latency in the root that we haven’t yet discussed is the process of snooping. Normally, anytime an access to system memory takes place it will be to a location that the processor considers cacheable, meaning it has permission to store a tem‐ 

**281** 

**PCI Ex ress Technolo p gy** 

porary copy in its local caches. If an external device attempts to accesses that area of memory, the chipset must first check the processor caches before allowing the access because a cached copy may have been modified. If so, the modified data will need to be written back to memory before it will be available for the device access. Although it’s necessary to ensure memory coherency, the problem is that snooping takes time. How long it takes is typically bounded but not predictable because it depends on what else the CPUs are doing at that time. Depending on the timing require‐ ments, that kind of uncertainty could ruin an isochronous data flow. 

**Snooping Solutions.** One way to avoid snooping is for devices to only access areas of memory that have been designated as uncacheable. Another option is for software to set the “No Snoop” attribute bit in the high‐priority packet headers. That forces the chipset to skip the snoop step regardless of the memory type and go directly to memory because software has guaran‐ teed that doing so won’t cause a problem. To enforce this as a requirement for the isochronous path, another bit can be initialized by hardware in the root port for the high‐priority VC called “Reject Snoop Transactions” (see the VC Resource Capability Register in Figure 7‐17 on page 265). The pur‐ pose of this is to allow only transactions for that VC that have the No Snoop attribute set. Any incoming packets that don’t have it set are discarded to ensure that the timing will never be violated by waiting for a snoop. 

## **Power Management** 

It’s a simple observation, but if timing is important for a path in PCIe, then power management (PM) mechanisms for devices in that path will need to han‐ dled carefully. Configuration software can read the latencies associated with every PM condition and select those cases that the timing budget will permit. The simplest approach, though, would just be to disable all PM options in an isochronous path. Fortunately, this is easily done using existing configuration registers. Devices can be placed into the device state D0 and left there, while the hardware‐controlled Link PM mechanism can be disabled (for more on PM, see Chapter 16, entitled ʺPower Management,ʺ on page 703). 

## **Error Handling** 

Finally, there is one last issue: what to do when errors occur on the Link. The ACK/NAK protocol, covered in Chapter 7, provides an automatic, hardware‐ based retry mechanism to correct packets that encounter transmission prob‐ lems. This otherwise desirable feature presents a problem for isochrony because it takes time to do it. And how long it takes to resolve an error can vary widely depending on things like how the problem was detected. 

**282** 

**Chapter 7: Quality of Service** 

To decide this question we have to know how much time uncertainty the sys‐ tem can tolerate and still deliver isochronous data. If the latency budget is too tight, there simply won’t be time for retrying failed packets and the ACK/NAK protocol will have to be disabled. Interestingly, the spec writers evidently didn’t consider that possibility because no configuration bits are included for dis‐ abling it or deciding how to handle packets that would have been retried but now won’t be. Therefore disabling this will require non‐standard mechanisms like vendor‐specific registers. 

If there _isn’t_ enough time available for retries, the target agent may simply choose to discard any bad packets. Another option would be to use the bad packets as they are, errors and all. For some applications using isochronous support that isn’t as counter‐intuitive as it sounds. An error in video streaming, for example, might cause an occasional glitch on the display, but that could be considered an acceptable risk. 

If there _is_ enough time in the Service Interval to allow retries, a limit could be placed on the possible latency they might add by adding a timer to track the time until the end of the Service Interval and use that to decide whether a retry could be attempted. Errors shouldn’t happen very often, of course, so this might be sufficient to correct the occasional transmission fault while still maintaining isochronous timing. 

**283** 

**PCI Ex ress Technolo p gy** 

**284** 

## _**8**_ 

## _**Transaction Ordering**_ 

## **The Previous Chapter** 

The previous chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different packets traversing the fabric. These mechanisms include application‐specific software that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **This Chapter** 

This chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock condi‐ tions that must be avoided. 

## **The Next Chapter** 

The next chapter describes, Data Link Layer Packets (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power manage‐ ment, flow control mechanism and can be used for vender defined purposes. 

## **Introduction** 

As with other protocols, PCI Express imposes ordering rules on transactions of the same traffic class (TC) moving through the fabric at the same time. Transac‐ tions with different TCs do not have ordering relationships. The reasons for these ordering rules related to transactions of the same TC include: 

- Maintaining compatibility with legacy buses (PCI, PCI‐X, and AGP). 

- • Ensuring that the completion of transactions is deterministic and in the sequence intended by the programmer. 

**285** 

**PCI Ex ress 3.0 Technolo p gy** 

- Avoiding deadlock conditions. 

- Maximize performance and throughput by minimizing read latencies and managing read and write ordering. 

Implementation of the specific PCI/PCIe transaction ordering is based on the following features: 

1. Producer/Consumer programming model on which the fundamental order‐ ing rules are based. 

2. Relaxed Ordering option that allows an exception to this when the Requester knows that a transaction does not have any dependencies on pre‐ vious transactions. 

3. ID Ordering option that allows a switches to permit requests from one device to move ahead of requests from another device because unrelated threads of execution are being performed by these two devices. 

4. Means for avoiding deadlock conditions and supporting PCI legacy imple‐ mentations. 

## **Definitions**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
