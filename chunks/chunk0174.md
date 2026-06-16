## **Transaction Ordering** 

Within a VC, the packets normally all flow through in the same order in which they arrived, but there are exceptions to this general rule. PCI Express protocol inherits the PCI transaction‐ordering model, including support for relaxed‐ ordering cases added with the PCI‐X architecture. These ordering rules guaran‐ tee that packets using the same traffic class will be routed through the topology in the correct order, preventing potential deadlock or live‐lock conditions. An interesting point to note is that, since ordering rules only apply within a VC and packets that use different TCs may not get mapped into the same VC, packets using different TCs are understood by software to have no ordering relation‐ ship. This ordering is maintained in the VCs within the transaction layer. 

**71** 

**PCI Ex ress Technolo p gy** 