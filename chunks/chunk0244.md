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
