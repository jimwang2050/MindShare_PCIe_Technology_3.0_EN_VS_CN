## **Generating Configuration Transactions** 

Processors are generally unable to perform configuration read and write requests directly because they can only generate memory and IO requests. That means the Root Complex will need to translate certain of those accesses into configuration requests in support of this process. Configuration space can be accessed using either of two mechanisms: 

- The legacy PCI configuration mechanism, using IO‐indirect accesses. 

- The enhanced configuration mechanism, using memory‐mapped accesses. 