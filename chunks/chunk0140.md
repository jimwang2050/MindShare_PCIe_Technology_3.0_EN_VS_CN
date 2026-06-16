## **PCI Ex ress Technolo p gy** 

As is true of many high‐speed serial transports, PCIe uses a bidirectional con‐ nection and is capable of sending and receiving information at the same time. The model used is referred to as a dual‐simplex connection because each inter‐ face has a simplex transmit path and a simplex receive path, as shown in Figure 2‐1 on page 40. Since traffic is allowed in both directions at once, the communi‐ cation path between two devices is technically full duplex, but the spec uses the term dual‐simplex because it’s a little more descriptive of the actual communi‐ cation channels that exist. 

_Figure 2‐1: Dual‐Simplex Link_ 

**==> picture [384 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet<br>PCIe PCIe<br>Device Device<br>Link (1 to 32 lanes wide)<br>A B<br>Packet<br>**----- End of picture text -----**<br>

The term for this path between the devices is a **Link** , and is made up of one or more transmit and receive pairs. One such pair is called a **Lane** , and the spec allows a Link to be made up 1, 2, 4, 8, 12, 16, or 32 Lanes. The number of lanes is called the Link Width and is represented as x1, x2, x4, x8, x16, and x32. The trade‐off regarding the number of lanes to be used in a given design is straight‐ forward: more lanes increase the bandwidth of the Link but add to its cost, space requirement, and power consumption. For more on this, see “Links and Lanes” on page 46. 

_Figure 2‐2: One Lane_ 

**==> picture [257 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter Receiver<br>Receiver Transmitter<br>One  lane<br>**----- End of picture text -----**<br>

**40** 

**Chapter 2: PCIe Architecture Overview** 