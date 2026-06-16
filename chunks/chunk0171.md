## **Posted Writes** 

**Memory Writes.** Memory writes are always posted and never receive com‐ pletions. Once the request has been sent, the Requester doesn’t wait for any feedback before going on to the next request, and no time or bandwidth is spent returning a completion. As a result, posted writes are faster and more efficient than non‐posted requests and improve system performance. As shown in Fig‐ ure 2‐21 on page 69, the packet is routed through the system using its target memory address to the Completer. Once a Link has successfully sent the request, that transaction is finished on that Link and its available for other pack‐ ets. Eventually, the Completer accepts the data and the transaction is truly fin‐ ished. Of course, one trade‐off with this approach is that, since no Completion packets are sent, there’s also no means for reporting errors back to the Requester. If the Completer encounters an error, it can log it and send a Message to the Root to inform system software about the error, but the Requester won’t see it. 

_Figure 2‐21: Posted Memory Write Transaction Protocol_ 

**==> picture [335 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Requester:<br>Step 1: Root Complex<br>      initiates MWr request<br>Root Complex<br>DDR<br>SDRAM<br>MWr<br>Switch A Switch C<br>MWr<br>Switch B Endpoint Endpoint Endpoint<br>MWr<br>Completer:<br>Endpoint Endpoint<br>Step 2: Endpoint receives MWr<br>**----- End of picture text -----**<br>

**69** 