## **Reflected-Wave Signaling** 

PCI architecturally supports up to 32 devices on each bus, but the practical elec‐ trical limit is considerably less, on the order of 10 to 12 electrical loads at the base frequency of 33MHz. The reason for this is that the bus uses a technique called “reflected‐wave signaling” to reduce the power consumption on the bus (see Figure 1‐4 on page 17). In this model, devices save cost and power by implementing weak transmit buffers that can only drive the signal to about half the voltage needed to switch the signal. The incident wave of the signal propa‐ gates down the transmission line until it reaches the end. By design, there is no termination at the end of the line so the wavefront encounters an infinite imped‐ ance and reflects back. This reflection is additive in nature and increases the sig‐ nal to the full voltage level as it makes its way back to the transmitter. When the signal reaches the originating buffer, the low output impedance of the driver terminates the signal and prevents further reflections. The total elapsed time from the buffer asserting a signal until the receiver detects a valid signal is thus the propagation time down the wire plus the reflection delay coming back and the setup time. All of that must be less than the clock period. 

As the length of the trace and the number of electrical loads on a bus increase, the time required for the signal to make this round trip increases. A 33 MHz PCI bus can only meet the signal timing with about 10‐12 electrical loads. An electri‐ cal load is one device installed on the system board, but a populated connector slot actually counts as two loads. Therefore, as indicated in Table 1‐1 on page 11, a 33 MHz PCI bus can only be designed for reliable operation with a maximum of 4 or 5 add‐in card connectors. 

**16** 

**Chapter 1: Background** 

_Figure 1‐4: PCI Reflected‐Wave Signaling_ 

**==> picture [223 x 194] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCI CLK Cycle<br>30ns (at 33MHz)<br>C<br>Tprop Tsu<br>10ns max 7 min<br>Tval A B<br>11ns max<br>**----- End of picture text -----**<br>

To connect more loads in a system, a PCI‐to‐PCI bridge is needed, as shown in Figure 1‐5. By the time more modern chipsets were available, peripherals had grown so fast that their competition for access to the shared PCI bus was limit‐ ing their performance. PCI speeds didn’t keep up, and it became a system bot‐ tleneck even though it was still very popular for peripherals. The solution to this problem was to move PCI out of the main path between system peripherals and memory, replacing the chipset interconnect with a proprietary solution (in this example, Intel’s Hub Link interface). 

A PCI Bridge is an extension to the topology. Each Bridge creates a new PCI bus that is electrically isolated from the bus above it, allowing another 10‐12 loads. Some of these devices could also be bridges, allowing a large number of devices to be connected in a system. The PCI architecture allows up to 256 buses in a single system and each of those buses can have up to 32 devices. 

**17** 

**PCI Ex ress Technolo p gy** 

_Figure 1‐5: 33 MHz PCI System, Including a PCI‐to‐PCI Bridge_ 

**==> picture [353 x 219] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>AGP<br>4x Memory Controller Hub<br>GFX<br>(Intel 8XX GMCH) DDR<br>O n TT SDRAM<br>Hub Link Slots<br>IDE<br>CD HDD PCI-33MHz<br>USB IO Controller Hub Primary PCI Bus<br>(ICH4) PCI<br>LPC<br>Bridge<br>Super AC’97<br>IO Link Secondary PCI Bus<br>Ethernet<br>COM1 COM1 Modem Audio (a Boot<br>COM2 Codec Codec Ethernet ROM<br>**----- End of picture text -----**<br>