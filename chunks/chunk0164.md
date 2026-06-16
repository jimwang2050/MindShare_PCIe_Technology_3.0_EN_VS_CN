## **Transaction Layer** 

In response to requests from the Software Layer, the Transaction Layer gener‐ ates outbound packets. It also examines inbound packets and forwards the information contained in them up to the Software Layer. It supports the split transaction protocol for non‐posted transactions and associates an inbound Completion with an outbound non‐posted Request that was transmitted earlier. The transactions handled by this layer use TLPs (Transaction Layer Packets) and can be grouped into four request categories: 

1. Memory 

2. IO 

3. Configuration 

4. Messages 

The first three of these were already supported in PCI and PCI‐X, but messages are a new type for PCIe. A **Transaction** is defined as the combination of a **Request** packet that a delivers a command to a targeted device, together with any **Completion** packets the target sends back in reply. A list of the request types is given in Table 2‐2 on page 59. 

_Table 2‐2: PCI Express Request Types_ 

|**Request Type**|**Non‐Posted or Posted**|
|---|---|
|Memory Read|Non‐Posted|
|Memory Write|Posted|
|Memory Read Lock|Non‐Posted|

**59** 