## **PCI Ex ress Technolo p gy** 

3. On clock edge 3, the initiator indicates its readiness for data transfer by asserting IRDY#. The round arrow symbol shown on the AD bus indicates that the tri‐stated bus is undergoing a “turn‐around cycle” as ownership of the signals changes (needed here because this is a read transaction; the initi‐ ator drives the address but receives data on the same pins). The target’s buffer is not turned on using the same clock edge that turns the initiator’s buffer off because we want to avoid the possibility of both buffers trying to drive a signal simultaneously, even for a brief time. That contention on the bus could damage the devices so, instead, the previous buffer is turned off one clock before the new one is turned on. Every shared signal is handled this way before changing direction. 

4. On clock edge 4, a device on the bus has recognized the requested address and responded by asserting DEVSEL# (device select) to claim this transac‐ tion and participate in it. At the same time, it asserts TRDY# (target ready) to show that it is delivering the first part of the read data and drives that data onto the AD bus (this could have been delayed ‐ the target is allowed 16 clocks from the assertion of FRAME# until TRDY#). Since both IRDY# and TRDY# are active at the same time here, data will be transferred on that clock edge, completing the first data phase. The initiator knows how many bytes will eventually be transferred, but the target does not. The command does not provide a byte count, so the target must look at the status of FRAME# whenever a data phase completes to learn when the initiator is satisfied with the amount of data transferred. If FRAME# is still asserted, this was not the last data phase and the transaction will continue with the next contiguous set of bytes, as is the case here. 

5. On clock edge 5, the target is not prepared to deliver the next set of data, so it deasserts TRDY#. This is called inserting a “Wait State” and the transac‐ tion is delayed for a clock. Both initiator and target are allowed to do this, and each can delay the next data transfer by up to 8 consecutive clocks. 

6. On clock edge 6, the second data item is transferred, and since FRAME# is still asserted, the target knows that the initiator still wants more data. 

7. On clock edge 7, the initiator forces a Wait State. Wait States allow devices to pause a transaction to quickly fill or empty a buffer and can be helpful because they allow the transaction to resume without having to stop and restart. On the other hand, they are often very inefficient because they not only stall the current transaction, they also prevent other devices from gain‐ ing access to the bus while it’s stalled. 

8. On clock edge 8, the third data set is transferred and now FRAME# has been deasserted so the target can tell that this was the last data item. Conse‐ quently, after this clock, all the control lines are turned off and the bus once again goes to the idle state. 

**14** 

**Chapter 1: Background** 

In keeping with the low cost design goal for PCI, several signals have more than one meaning on the bus to reduce the pin count. The 32 address and data sig‐ nals are multiplexed and the C/BE# (Command/Byte Enable) signals share their four pins for the same reason. Although reducing the pin count is desirable, it’s also the reason that PCI uses “turn‐around cycles”, which add more delay. It also precludes the option to pipeline transactions (sending the address for the next cycle while data for the previous one is delivered). Handshake signals like FRAME#, DEVSEL#, TRDY#, IRDY#, and STOP# control the timing of events during the transaction. 

_Figure 1‐3: Simple PCI Bus Transfer_ 

**==> picture [322 x 363] intentionally omitted <==**

**----- Start of picture text -----**<br>
Wait Wait Wait<br>State State State<br>Address<br>Data Phase 1 Data Phase 2 Data Phase 3<br>Phase<br>1 2 3 4 5 6 7 8<br>CLK<br>FRAME#<br>Data Data Data<br>AD Addr 1 2 3<br>Bus Byte Byte Byte<br>C/BE# Cmd Enables Enables Enables<br>IRDY#<br>TRDY#<br>DEVSEL#<br>GNT#<br>**----- End of picture text -----**<br>

**15** 

**PCI Ex ress Technolo p gy** 