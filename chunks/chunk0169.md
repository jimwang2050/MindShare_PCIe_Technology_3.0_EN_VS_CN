## **Non-Posted Transactions** 

**Ordinary Reads.** Figure 2‐18 on page 65 shows an example of a Memory Read Request sent from an Endpoint to system memory. A detailed discussion of the TLP contents can be found in Chapter 5, entitled ʺTLP Elements,ʺ on page 169, but an important part of any memory read request is the target address. The address for a memory Request can be 32 or 64 bits, and determines the packet routing. In this example, the request gets routed through two Switches that forward it up to the target, which is the Root in this case. When the Root decodes the request and recognizes that the address in the packet targets sys‐ tem memory, it fetches the requested data. To return that data to the Requester, the Transaction Layer of the Root Port creates as many Completions as are needed to deliver all the requested data to the Requester. The largest possible data payload for PCIe is 4 KB per packet, but devices are often designed to use smaller payloads than that, so several completions may be needed to return a large amount of data. 

_Figure 2‐18: Non‐Posted Read Example_ 

**==> picture [326 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Completer<br>Processor<br>Step 2: Root receives MRd<br>Step 3: Root fetches data,<br>returns CplD<br>Root Complex<br>CplD MRd System<br>Memory<br>Switch A Switch C<br>CplD<br>MRd<br>Switch B Endpoint Endpoint Endpoint<br>MRd<br>CplD<br>Requester<br>Endpoint Endpoint Step 1: Endpoint initiates MRd<br>Step 4: Endpoint receives CplD<br>**----- End of picture text -----**<br>

**65** 