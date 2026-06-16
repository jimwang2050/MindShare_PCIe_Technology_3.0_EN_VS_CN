## **PCI Address Space Map** 

PCI architecture supports 3 address spaces as shown in Figure 1‐10 on page 26: memory, I/O and configuration address space. x86 processors can access mem‐ ory and IO space directly. A PCI device maps into the processors memory address space and can either support 32 or 64 bit memory addressing. In I/O address space, PCI supports 32 bit addresses but, since x86 CPUs only used 16 bits for I/O space, many platforms limit the I/O space to 64 KB (16 bits worth). 

PCI also introduced a third address space called configuration space that the CPU could only indirectly access. Each function contains internal registers for configuration space that allow software visibility and control of its addresses and resources in a standardized way, providing a true “plug and play” environ‐ ment in the PC. Each PCI function may have up to 256 Bytes of configuration address space. Given that PCI supports up to 8 functions/device, 32 devices/bus and up to 256 buses/system, then the total amount of configuration space asso‐ ciated with a system is 256 Bytes/function x 8 functions/device x 32 devices/bus x 256 buses/system = 16MB of configuration space. 

Since an x86 CPU cannot access configuration space directly, it must do so indi‐ rectly by indexing through IO registers (although with PCI Express a new method to access configuration space was introduced by mapping it into the memory address space). The legacy model, shown in Figure 1‐10 on page 26, uses an IO Port called Configuration Address Port located at address CF8h‐ CFBh and a Configuration Data Port mapped to address CFCh‐CFFh. Details regarding this method and the memory mapped method of accessing configu‐ ration space are explained in the next section. 

**25** 

**PCI Ex ress Technolo p gy** 

_Figure 1‐10: Address Space Mapping_ 

**==> picture [372 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
Memory Map<br>4GB / 16 EB<br>PCI PCI<br>Memory Configuration<br>AGP Video Space<br>16MB<br>PCI<br>Memory<br>DRAM Boundary<br>Extended IO Map<br>Memory 64KB<br>1MB<br>Boot ROM<br>PCI IO<br>Expansion ROM Space<br>Legacy Video<br>640KB Data Port CFCh-CFFh<br>Conventional Address Port CF8h-CFBh<br>256B<br>Memory 1KB 256B<br>Legacy IO 256B<br>**----- End of picture text -----**<br>