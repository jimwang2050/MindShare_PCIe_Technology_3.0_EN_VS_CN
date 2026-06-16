## **Bus Compare and Data Port Usage** 

The Host Bridge within the Root Complex, shown in Figure 3‐5 on page 95, implements a Secondary Bus Number register and a Subordinate Bus Number register. The Secondary Bus Number is the bus number of the bus immediately beneath the bridge. The Subordinate Bus Number is the target bus number that lives downstream of the bridge. 

In a single Root Complex system, the bridge may have a Secondary Bus Num‐ ber register that is hardwired to 0, a read/write register that reset forces to 0, or it may just implicitly know that the first accessible bus will be Bus 0. If bit 31 in the Configuration Address Port (see Figure 3‐4 on page 92) is set to 1b, the bridge will compare the target bus number to the range of buses that exists downstream. 

When a Request is seen, the Bridge evaluates whether the target bus number is within the range of bus numbers downstream, from the value of the Secondary Bus number to the Subordinate Bus number, inclusive. If the target bus matches the Secondary Bus, then that bus is targeted and the Request is passed through as a Type 0 Configuration Request. When devices see a Type 0 Request, they know that a device local to that bus is the target device (rather than one on a subordinate bus downstream). 

If the target bus is larger than the bridge’s Secondary Bus number, but less than or equal to the bridge’s Subordinate Bus number, the Request will be forwarded as a Type 1 configuration request on the bridge’s secondary bus. A Type 1 con‐ figuration access is understood to mean that, even though the Request has to go across this bus, it does not target a device on this bus. Instead, the request will 

**93** 