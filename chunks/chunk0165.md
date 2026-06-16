## **PCI Ex ress Technolo p gy** 

_Table 2‐2: PCI Express Request Types (Continued)_ 

|**Request Type**|**Non‐Posted or Posted**|
|---|---|
|IO Read|Non‐Posted|
|IO Write|Non‐Posted|
|Configuration Read (Type 0 and Type 1)|Non‐Posted|
|Configuration Write (Type 0 and Type 1)|Non‐Posted|
|Message|Posted|

The requests also fall into one of two categories as shown in the right column of the table: **non‐posted** and **posted** . For non‐posted requests, a Requester sends a packet for which a Completer should generate a response in the form of a Com‐ pletion packet. The reader may recognize this as the split transaction protocol inherited from PCI‐X. For example, any read request will be non‐posted because the requested data will need to be returned in a completion. Perhaps unexpectedly, IO writes and Configuration writes are also non‐posted. Even though they are delivering the data for the command, these requests still expect to receive a completion from the target to confirm that the write data has in fact made it to the destination without error. 

In contrast, Memory Writes and Messages are posted, meaning the targeted device does not return a completion TLP to the Requester. Posted transactions improve performance because the Requester doesn’t have to wait for a reply or incur the overhead of a completion. The trade‐off is that they get no feedback about whether the write has finished or encountered an error. This behavior is inherited from PCI and is still considered a good thing to do because the likeli‐ hood of a failure is small and the performance gain is significant. Note that, even though they don’t require Completions, Posted Writes do still participate in the Ack/Nak protocol in the Data Link Layer that ensures reliable packet delivery. For more on this, see Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317. 