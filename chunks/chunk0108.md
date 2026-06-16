## **PCI Bus Arbitration** 

Consider Figure 1‐2 on page 13. Since PCI devices today are almost all capable of being bus‐master, they are able to do both DMA and peer‐to‐peer transfers. In a shared bus architecture like PCI, they have to take turns on the bus, so a device that wants to initiate transactions must first request ownership of the bus from the bus arbiter. The arbiter sees all the current requests and uses an imple‐ mentation‐specific algorithm to decide which Bus Master gets ownership of the bus next. The PCI spec doesn’t describe this algorithm, but does state that it must be “fair” and not starve any device for access. 

**20** 

**Chapter 1: Background** 

The arbiter can grant bus ownership to the next requesting device while the pre‐ vious Bus Master is still executing its transfer, so that no clocks are used on the bus to sort out the next owner. As a result, the arbitration appears to happen behind the scenes and is referred to as “hidden” bus arbitration, which was a design improvement over earlier bus protocols. 