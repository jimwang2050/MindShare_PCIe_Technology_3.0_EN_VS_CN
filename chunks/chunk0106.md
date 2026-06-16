## **Direct Memory Access (DMA)** 

A more efficient method of transferring data is called DMA (direct memory access). In this model another device, called a DMA engine, handles the details of memory transfers to a peripheral on behalf of the processor, off‐loading this 

**19** 

**PCI Ex ress Technolo p gy** 

tedious task. Once the CPU has programmed the starting address and byte count into it, the DMA engine handled the bus protocol and address sequencing on its own. This didn’t involve any change to the PCI peripherals and allowed them to keep their low‐cost designs. Later, improved integration allowed peripherals to integrate this DMA functionality locally, so they didn’t need an external DMA engine. These devices were capable of handling their own bus transfers and were called Bus Master devices. 

Figure 1‐3 on page 15 is an example of a Bus Master transaction on PCI. The North Bridge might decode the address and recognize that it will be the target for the transaction. In the data phase of the bus cycle, data is transferred between the Bus Master and the North Bridge acting as the target. The North Bridge in turn will generate DRAM bus cycles to communicate with system memory. After the transfer is completed, the PCI peripheral might generate an interrupt to inform the system. The DMA method of data transfer is more effi‐ cient because the CPU is not involved in the data movement, and a single bus cycle may be sufficient to move a block of data. 