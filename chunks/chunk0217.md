## **Multi-Host System** 

If there are multiple Root Complexes (refer to Figure 3‐6 on page 97), the Con‐ figuration Address and Data ports can be duplicated at the same IO addresses in each of their respective Host/PCI bridges. In order to prevent contention, only one of the bridges responds to the processorʹs accesses to the configuration ports. 

1. When the processor initiates the IO write to the Configuration Address Port, the host bridges are configured so that only one will actively partici‐ pate in the transaction. 

2. During enumeration, software discovers and numbers all the buses under the active bridge. When that’s done, it enables the inactive host bridge and assigns a bus number to it that is outside the range already assigned to the active bridge and continues the enumeration process. Both host bridges see the Requests, but since they have non‐overlapping bus numbers they only respond to the appropriate bus number requests and so there’s no conflict. 

3. Accesses to the Configuration Address Port go to both host bridges after that, and a subsequent read or write access to the Configuration Data Port is only accepted by the host/PCI bridge that is the gateway to the target bus. This bridge responds to the processor’s transaction and the other ignores it. 

   - If the target bus is the Secondary Bus, the bridge converts the access to a Type 0 configuration access. 

   - Otherwise, it converts it into a Type 1 configuration access. 