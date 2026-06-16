## **The Need for Speed** 

Of course, a serial model must run much faster than a parallel design to accom‐ plish the same bandwidth because it may only send one bit at a time. This has not proven difficult, though, and in the past PCIe has worked reliably at 2.5 GT/ s and 5.0 GT/s. The reason these and still higher speeds (8 GT/s) are attainable is that the serial model overcomes the shortcomings of the parallel model. 

**Overcoming Problems.** By way of review, there are a handful of problems that limit the performance of a parallel bus and three are illustrated in Figure 2‐ 3 on page 42. To get started, recall that parallel buses use a common clock; out‐ puts are clocked out on one clock edge and clocked into the receiver on the next edge. One issue with this model is the time it takes to send a signal from trans‐ mitter to receiver, called the flight time. The flight time must be less than the clock period or the model won’t work, so going to smaller clock periods is chal‐ lenging. To make this possible, traces must get shorter and loads reduced but eventually this becomes impractical. Another factor is the difference in the arrival time of the clock at the sender and receiver, called clock skew. Board lay‐ out designers work hard to minimize this value because it detracts from the tim‐ ing budget but it can never be eliminated. A third factor is signal skew, which is 

**41** 

**PCI Ex ress Technolo p gy** 

the difference in arrival times for all the signals needed on a given clock. Clearly, the data can’t be latched until all the bits are ready and stable, so we end up waiting for the slowest one. 

_Figure 2‐3: Parallel Bus Limitations_ 

**==> picture [384 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Flight Time<br>Transmitter<br>Receiver<br>Incorrect<br>Transmission<br>Media sampling<br>due to skew<br>Common Clock Common Clock<br>**----- End of picture text -----**<br>

How does a serial transport like PCIe get around these problems? First, flight time becomes a non‐issue because the clock that will latch the data into the receiver is actually built into the data stream and no external reference clock is necessary. As a result, it doesn’t matter how small the clock period is or how long it takes the signal to arrive at the receiver because the clock arrives with it at the same time. For the same reason there’s no clock skew, again because the latching clock is recovered from the data stream. Finally, signal skew is elimi‐ nated within a Lane because there’s only one data bit being sent. The signal skew problem returns if a multi‐lane design is used, but the receiver corrects for this automatically and can fix a generous amount of skew. Although serial designs overcome many of the problems of parallel models, they have their own set of complications. Still, as we’ll see later, the solutions are manageable and allow for high‐speed, reliable communication. 

**Bandwidth.** The combination of high speed and wide Links that PCIe sup‐ ports can result in some impressive bandwidth numbers, as shown in Table 2‐1 on page 43. These numbers are derived from the bit rate and bus characteristics. One such characteristic is that, like many other serial transports, the first two generations of PCIe use an encoding process called **8b/10b** that generates a 10‐ bit output based on an 8‐bit input. In spite of the overhead this introduces, there are several good reasons for doing it as we’ll see later. For now it’s enough to 

**42** 

**Chapter 2: PCIe Architecture Overview** 

know that sending one byte of data requires transmitting 10 bits. The first gen‐ eration (Gen1 or PCIe spec version 1.x) bit rate is 2.5 GT/s and dividing that by 10 means that one lane will be able to send 0.25 GB/s. Since the Link permits sending and receiving at the same time, the aggregate bandwidth can be twice that amount, or 0.5 GB/s per Lane. Doubling the frequency for the second gener‐ ation (Gen2 or PCIe 2.x) doubled the bandwidth. The third generation (Gen3 or PCIe 3.0) doubles the bandwidth yet again, but this time the spec writers chose not to double the frequency. Instead, for reasons we’ll discuss later, they chose to increase the frequency only to 8 GT/s and remove the 8b/10b encoding in favor of another encoding mechanism called **128b/130b** encoding (for more on this, see the chapter “Physical Layer ‐ Logical (Gen3)” on page 407). Table 2‐1 summarizes the bandwidth available for all the current possible combinations and shows the peak throughput the Link could deliver in that configuration. 

_Table 2‐1: PCIe Aggregate Gen1, Gen2 and Gen3 Bandwidth for Various Link Widths_ 

|**Link Width**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 Bandwidth**<br>**(GB /s)**|0.5|1|2|4|6|8|16|
|**Gen2 Bandwidth**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 Bandwidth**<br>**(GB/s)**|2|4|8|16|24|32|64|