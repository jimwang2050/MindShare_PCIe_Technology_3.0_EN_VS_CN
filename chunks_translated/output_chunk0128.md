## **PCI Ex ress Technolo p gy** 

likes while it waits for the completer, such as initiating other requests, even to the same completer. Once the completer has gathered the requested data, it then arbitrates for ownership of the bus and initiates a split completion during which it returns the requested data. The requester claims the split completion bus cycle and accepts the data from the completer. The split completion looks very much like a write transaction to the system. This Split Transaction Model is pos‐ sible because not only does the request indicate how much data they are requesting in the Attribute phase, but they also indicate who they are (their Bus:Device:Function number) which allows the completer to target the correct device with the completion. 

Two bus transactions are needed to complete the entire data transfer, but between the read request and the split completion the bus is available for other work. The requester does not need to poll the device with retries to learn when the data is ready. The completer simply arbitrates for the bus and drives the requested data back when it is ready. This makes for a much more efficient transaction model in terms of bus utilization. 

These protocol enhancements made to the PCI‐X bus architecture described so far contribute towards an increased transfer efficiency of around 85% for PCI‐X as compared to 50%‐60% with the standard PCI protocol. 

_Figure 1‐17: PCI‐X Split Transaction Protocol_ 

**==> picture [364 x 153] intentionally omitted <==**

**----- Start of picture text -----**<br>
1. Requester initiates<br>read transaction 2. Completer unable to<br>return data immediately<br>4. Completer issues 3. Completer<br>split response<br>Requester Completer memorizes<br>    transaction<br>5. Later, Completer initiates split completion<br>bus cycle to return read data<br>**----- End of picture text -----**<br>