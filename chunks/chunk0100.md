## **Typical PCI Bus Cycle** 

Figure 1‐3 on page 15 represents a typical PCI bus cycle. PCI is synchronous, meaning events happen on clock edges, so the clock is shown at the top of the diagram and it’s rising edges are marked with dotted lines because those are the times when signals are driven out or sampled. A brief description of what hap‐ pens on the bus is as follows: 

1. On clock edge 1, FRAME# (used to indicate when a bus access is in progress) and IRDY# (Initiator Ready for data) are both inactive, showing that the bus is idle. At the same time, GNT# is active, meaning the bus arbi‐ ter has selected this device to be the next initiator. 

2. On clock edge 2, FRAME# is asserted by the initiator, indicating that a new transaction has started. At the same time, it drives the address and com‐ mand for this transaction. All of the other devices on the bus will latch this information and begin the process of decoding the address to see whether it’s a match for them. 

**13** 