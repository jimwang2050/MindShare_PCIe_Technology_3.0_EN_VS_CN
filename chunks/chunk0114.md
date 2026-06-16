## **PCI Error Handling** 

PCI devices can optionally detect and report address and data phase parity errors during transactions. PCI generates ʺeven parityʺ across most of the sig‐ nals during a transaction by using the PAR signal. This means that if the num‐ ber of set bits during an address or data phase is odd, the master device will set the PAR signal to make the parity ʺeven.ʺ The target device receives the address or data and checks for errors. Parity errors are detectable only as long as an odd number of signals are affected causing the received number of ones to be odd. If a device detects a data phase parity error, it asserts PERR# (parity error). This is potentially a recoverable error since, for cases like a memory read, just repeat‐ ing the transaction may resolve the problem. PCI does not include any auto‐ matic or hardware‐based recovery mechanisms, though, so any attempts to resolve the error would be handled by software. 

_Figure 1‐9: PCI Error Handling_ 

**==> picture [376 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
NMI<br>Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data Port<br>PCI 33 MHz<br>Slots<br>CD HDD IDE PERR#<br>Error<br>South Bridge Logic<br>USB SERR#<br>ISA<br>Ethernet SCSI<br>Boot Modem Audio Super<br>ROM Chip Chip I/O<br>COM1<br>COM2<br>**----- End of picture text -----**<br>

However, it’s a different matter if a parity error is detected during the address phase. In this case the address was corrupted and the wrong target may have recognized the address. There’s no way to tell what the corrupted address became or what devices on the bus did in response to it, so there’s also no sim‐ 

**24** 

**Chapter 1: Background** 

ple recovery. As a result, errors of this type result in the assertion of the SERR# (system error) pin, which typically results in a call to the system error handler. In older machines, this would often halt the system as a precaution, resulting in the “blue screen of death.” 

In older machines, both PERR# and SERR# were connected to the error logic in the South Bridge. For reasons of simplicity and cost, this typically resulted in the assertion of an NMI signal (non‐maskable interrupt signal) to the CPU, which would often simply halt the system. 