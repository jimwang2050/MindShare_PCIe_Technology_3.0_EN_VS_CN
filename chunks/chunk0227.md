```
movdx,0CF8h;set dx = config address port address
moveax,80040000h;enable=1, bus 4, dev 0, func 0, DW 0
outdx,eax;IO write to set up address port
movdx,0CFCh; set dx = config data port address
inax,dx;2-byte read from config data port
```

1. The out instruction generates an IO write from the processor targeting the Configuration Address Port in the Root Complex Host bridge (0CF8h), as shown in Figure 3‐4 on page 92. 

2. The Host bridge compares the target bus number (4) specified in the Con‐ figuration Address Port to the range of buses (0‐through‐10) that reside downstream. The target bus falls within the range, so the bridge is primed with the destination of the next configuration request. 

3. The in instruction, generates an IO read transaction from the processor tar‐ geting the Configuration Data Port in the Root Complex Host bridge. It’s a 2‐byte read from the first two locations in the Configuration Data Port. 

4. Since the target bus is not bus 0, the Host/PCI bridge initiates a Type 1 Con‐ figuration read on bus 0. 

5. All of the devices on bus 0 latch the transaction request and see that it’s a Type 1 Configuration Request. As a result, both of the virtual PCI‐to‐PCI bridges in the Root Complex compare the target bus number in the Type 1 request to the range of buses downstream from each of them. 

6. The destination bus (4) is within the range of buses downstream of the left‐ hand bridge, so it passes the packet through to its secondary bus, but as a Type 1 request because the destination bus doesn’t match the Secondary Bus Number. 

7. The upstream port on the left‐hand switch receives the packet and delivers it to the upstream PCI‐to‐PCI bridge. 

8. The bridge determines that the destination bus resides beneath it, but is not targeting its secondary bus, so it passes the packet to bus 2 as a Type 1 request. 

9. Both of the bridges on bus 2 receive the Type 1 request packet. The right‐ hand bridge determines that the destination bus matches its Secondary Bus Number. 

**102** 

**Cha ter 3: Confi uration Overview p g** 

10. The bridge passes the configuration read request through to bus 4, but con‐ verts into a Type 0 Configuration Read request because the packet has reached the destination bus (target bus number matches the secondary bus number). 

11. Device 0 on bus 4 receives the packet and decodes the target Device, Func‐ tion, and Register Number fields to select the target dword in its configura‐ tion space (see Figure 3‐3 on page 90). 

12. Bits 0 and 1 in the First Dword Byte Enable field are asserted, so the Func‐ tion returns its first two bytes, (Vendor ID in this case) in the Completion packet. The Completion packet is routed to the Host bridge using the Requester ID field obtained from the Type 0 request packet. 

13. The two bytes of read data are delivered to the processor, thus completing the execution of the “in“ instruction. The Vendor ID is placed in the proces‐ sor’s AX register. 

## **Example Enhanced Configuration Access** 

Refer to Figure 3‐9 on page 104. The following x86 code sample causes the Root Complex to perform a read from Bus 4, Device 0, Function 0, Register 0 (Vendor ID). Before this will work, the Host Bridge must have been assigned a base address value. This example assumes that the 256MB‐aligned base address of the Enhanced Configuration memory‐mapped range is E0000000h: 

```
movax,[E0400000h];memory-mapped Config read
```

- Address bits 63:28 indicate the upper 36 bits of the 256MB‐aligned base address of the overall Enhanced Configuration address range (in this case, 00000000 E0000000h). 

- Address bits 27:20 select the target bus (in this case, 4). 

- Address bits 19:15 select the target device (in this case, 0) on the bus. 

- Address bits 14:12 select the target Function (in this case, 0) within the device. 

- Address bits 11:2 selects the target dword (in this case, 0) within the selected Function’s configuration space. 

- Address bits 1:0 define the start byte location within the selected dword (in this case, 0). 

The processor initiates a 2‐byte memory read starting from memory location E0400000h, and this is latched by the Host Bridge in the Root Complex. The Host Bridge recognizes that the address matches the area designated for Con‐ figuration and generates a Configuration read Request for the first two bytes in dword 0, Function 0, device 0, bus 4. The remainder of the operation is the same as that described in the previous section. 

**103** 

## **PCI Ex ress Technolo p gy** 

_Figure 3‐9: Example Configuration Read Access_ 

**==> picture [266 x 367] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bus = 0 Bridge<br>Sub = 10<br>Bus 0<br>Pri = 0 Pri = 0<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 10 P2P<br>Bus 1 Bus 5<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 10<br>Bus 2 P2P Bus 6 P2P<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 10<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 10<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 0 Function 0 Function 0<br>Pri = 8 Express<br>Sec = 9 PCI<br>Sub = 9 Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>**----- End of picture text -----**<br>


## **Enumeration - Discovering the Topology** 

After a system reset or power up, configuration software has to scan the PCIe fabric to discover the machine topology and learn how the fabric is populated. Before that happens, as shown in Figure 3‐10 on page 105, the only thing that software can know for sure is that there will be a Host/PCI bridge and that bus 

**104** 

**Cha ter 3: Confi uration Overview p g** 

number 0 will be on the secondary side of that bridge. Note that the upstream side of a bridge device is called its primary bus, while the downstream side is referred to as its secondary bus. The process of scanning the PCI Express fabric to discover its topology is referred to as the _enumeration process_ . 

_Figure 3‐10: Topology View At Startup_ 

**==> picture [238 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex has bus<br>number zero assigned.<br>Processor The remaining topology<br>have yet to be discovered<br>and numbered.<br>Host/PCI<br>Bridge<br>Bus 0<br>? ? ? ? ? ? ? ?<br>**----- End of picture text -----**<br>


## **Discovering the Presence or Absence of a Function** 

The configuration software executing on the processor normally discovers the existence of a Function by reading from its Vendor ID register. A unique 16‐bit value is assigned to each vendor by the PCI‐SIG and is hardwired into the Ven‐ dor ID register of each Function designed by that vendor. By reading this regis‐ ter in all of the possible combinations of Bus, Device, and Function numbers in the system, enumeration software can search through the entire topology to learn which devices are present. This process is fairly simple, but there are two problems that can arise: a targeted device may not be present, or it may be present but unprepared to respond. Handling these two cases is described next. 

## **Device not Present** 

It can happen several times during the process of discovery that the targeted device doesn’t actually exist in the system and when that happens it needs to be understood correctly. In PCI, the Configuration Read Request would timeout on the bus and generate a Master Abort error condition. Since no device was driv‐ ing the bus and all the signals were pulled up, the data bits on the bus would be 

**105** 

## **PCI Ex ress Technolo p gy** 

seen as all ones and that would become the data value seen. The resulting Ven‐ dor ID of FFFFh is reserved. If enumeration software saw that result for the read, it understood that the device wasn’t present. Since this wasn’t really an error condition, the Master Abort would not be reported as an error during the enumeration process. 

For PCIe, a Configuration Read Request to a non‐existent device will result in the bridge above the target device returning a Completion without data that has a status of UR (Unsupported Request). For backward compatibility with the leg‐ acy enumeration model, the Root Complex returns all ones (FFFFh) to the pro‐ cessor for the data when this Completion is seen during enumeration. Note that enumeration software depends on receiving a value of all 1s for a Configuration Read Request that returns an Unsupported Request when probing for the exist‐ ence of Functions in the system. 

It’s important to avoid accidentally reporting an error for this case. Even though this timeout or UR result would be seen as an error during runtime, it’s an expected result that isn’t considered an error during enumeration. To help avoid confusion on this, devices are usually not enabled to signal errors until later. For PCIe it may still be useful to make a note of this event, and that’s why a fourth “error” status bit, called Unsupported Request Status is given in the PCIe Capa‐ bility register block (refer to “Enabling/Disabling Error Reporting” on page 678 for more on this). That allows this condition to be noted without marking it as an error, and that’s important because a detected error might stop the enumera‐ tion process to call the system error handler. The error handling software might have only limited capabilities during this time and thus have trouble resolving the problem. The enumeration software could fail in that case, since it’s typically written to execute before the OS or other error handling software is available. To avoid this risk, errors should not normally be reported during enumeration. 

## **Device not Ready** 

Another problem that can arise is that the targeted device is present but isn’t ready to respond to a configuration access. There is a timing consideration for configuration because of the time it takes devices to prepare for access. If the data rate is 5.0 GT/s or less, software must wait 100ms after reset before initiat‐ ing a Configuration Request. If the rate is higher than 5.0 GT/s (Gen3 speed), software must wait until 100ms after Link training completes before attempting this. The reason for the longer delay for the higher speeds is that the Gen3 Equalization Process during Link training can take a long time (on the order of 50ms; see “Link Equalization Overview” on page 577 for more on this topic). 

As defined in the PCI 2.3 spec, Initialization Time (Trhfa ‐ Time from Reset High to First Access) begins when RST# is deasserted and completes 2[25] PCI clocks 

**106** 

**Cha ter 3: Confi uration Overview p g** 

later. That works out to one full second during which the Function is preparing for its first configuration access and that value has been carried forward for PCIe as 1.0s (+50%/‐0%). A Function could use that time to populate its configu‐ ration registers by loading the contents from an external serial EEPROM, for example. That might take a while to load and the Function would be unpre‐ pared for a successful access until it finished. In PCI, if a configuration access was seen before the Function was ready, it had three choices: ignore the Request, Retry the Request, or accept the Request but postpone delivering its response until it was fully ready. That last response could cause trouble for Hot‐ plug systems because the shared bus could end up being stalled for one second until the Request resolved. 
