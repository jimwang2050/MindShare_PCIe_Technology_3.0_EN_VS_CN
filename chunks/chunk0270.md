- Printed wiring board impedance variations 

- Trace length mismatches 

When the serial bit streams carrying a packet arrive at the receiver, this Lane‐to‐ Lane skew must be removed to receive the bytes in the correct order. This pro‐ cess is referred to as de‐skewing the link. 

## **Ordered sets Help De-Skewing** 

The unique structure of the ordered sets and the fact that they are sent simulta‐ neously on all the lanes makes them useful for detecting timing misalignment between Lanes. The spec doesn’t define a method for doing this but in Gen1 and Gen2 the receiver logic can simply look for the COM character on each lane. If it doesn’t appear at the same time on all Lanes, then the early arriving COMs are delayed until they all match up on all Lanes. 

## **Receiver Lane-to-Lane De-Skew Capability** 

This could be done by adjusting an analog delay line on the incoming signals. Alternatively, it could be done after the elastic buffer, which has the advantage that the arrival time differences are now digitized to Symbol times by the local clock of the receiver (see Figure 11‐23 on page 399). If the input to one lane makes it on a clock edge and another one doesn’t, the early arrival COMs can simply be delayed by the appropriate number of Symbol clocks to line it up with the late arriving COMs. The fact that the maximum allowable skew at the receiver is a multiple of the clock periods infers that the spec writers probably had an implementation like this in mind (see Table 11‐3 on page 399). 

**398** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Table 11‐3: Allowable Receiver Signal Skew_ 

|Spec Version|Allowable Rx Skew|
|---|---|
|Gen1|20 ns<br>(5 clocks at 4ns per Symbol)|
|Gen2|8 ns<br>(4 clocks at 2ns per Symbol)|
|Gen3|6 ns<br>(4 clocks at 1.25ns per Symbol)|



In Gen3 mode there aren’t any COM characters to use for de‐skewing, but detecting Ordered Sets can still provide the necessary timing alignment. 

## **De-Skew Opportunities** 

An unambiguous pattern is needed on all lanes at the same time to perform de‐ skewing and any ordered set will do. Link training sends these, but the SKIP ordered set is sent regularly during normal Link operation. Checking its arrival time allows the skew to be checked on an ongoing basis in case it might change based on temperature or voltage. If it does, the Link will need to transition to the Recovery LTSSM state to correct it. If that happens while packets are in flight, however, a receiver error may occur and a packet could be dropped, pos‐ sibly resulting in replayed TLPs. 

_Figure 11‐23: Receiver’s Link De‐Skew Logic_ 

**==> picture [307 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
TS1/TS2 TS1/TS2<br>Lane 0 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 1 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 2 Rx FTS Delay FTS<br>(symbols)<br>TS1/TS2 TS1/TS2<br>Lane 3 Rx FTS Delay FTS<br>(symbols)<br>COM COM<br>COM COM<br>COM COM<br>COM COM<br>**----- End of picture text -----**<br>


**399** 

**PCI Ex ress Technolo p gy** 

## **8b/10b Decoder** 

## **General** 

The first two generations of PCIe use 8b/10b, while Gen3 does not. Let’s explore the operation of it first and then consider the difference for Gen3. Refer to Fig‐ ure 11‐24 on page 401. Each receiver Lane incorporates a 10b/8b decoder which is fed from the Elastic Buffer. The decoder is shown with two lookup tables (the D and K tables) to decode the 10‐bit Symbol stream into 8‐bit characters plus the D/K# signal. The state of the D/K# signal indicates that the received Symbol is a Data (D) character if a match for the received Symbol is found in the D table, or a Control (K) character if a match for the received Symbol is discovered in the K table. 

## **Disparity Calculator** 

The decoder sets the disparity value based on the disparity of the first Symbol received. After the first Symbol, once Symbol lock has been achieved and dis‐ parity has been initialized, the calculated disparity for each subsequent Sym‐ bol’s disparity is expected to follow the rules. If it does not, a Receiver Error is reported. 

## **Code Violation and Disparity Error Detection** 

**General.** The error detection logic of the 8b/10b decoder detects illegal Symbols in the received Symbol stream. Some error checking is optional in the receiver, but the spec requires that these errors be checked and reported as a Receiver Error. The two types of errors detected are: 

## **Code Violations.** 

- Any 6‐bit sub‐block containing more than four 1s or four 0s is in error. 

- Any 4‐bit sub‐block containing more than three 1s or three 0s is in error. 

- Any 10‐bit Symbol containing more than six 1s or six 0s is in error. 

- Any 10‐bit Symbol containing more than five consecutive 1s or five con‐ secutive 0s is in error. 

- Any 10‐bit Symbol that doesn’t decode into an 8‐bit character is in error. 

## **Disparity Errors.** 

At the receiver a Symbol cannot have a disparity that doesn’t match what it should be for the CRD. If it does, a disparity error is detected. Some dispar‐ ity errors may not be detectable until the subsequent Symbol is processed 

**400** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

(see Figure 11‐25 on page 401). For example, if two bits in a Symbol flip in error, the error may not be visible and the Symbol may decode into a valid 8‐bit character. Such an error won’t be detected in the Physical Layer. 

_Figure 11‐24: 8b/10b Decoder per Lane_ 

**==> picture [373 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bytes to De-Scrambler D/K#<br>D/<br>7 6 5 4 3 2 1 0<br>K#<br>8b Character H G F E D C B A<br>To Error Reporting<br>8b/10b Look-Up Table For D Characters<br>8b/10b Look-Up Table For K Characters Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>10b Symbol<br>From Elastic Buffer<br>**----- End of picture text -----**<br>


_Figure 11‐25: Example of Delayed Disparity Error Detection_ 

||**CRD**|**Character**|**Character**|**CRD**|**Character**|**CRD**|**Character**|**CRD**|
|---|---|---|---|---|---|---|---|---|
|**Transmitted**<br>**Character Stream**|**-**|**D21.1**||**-**|**D10.2**|**-**|**D23.5**|**+**|
|**Transmitted Bit**<br>**Stream**|**-**|**101010 1001**||**-**|**010101 0101**|**-**|**111010 1010**|**+**|
|**Bit Stream After**<br>**Error**|**-**|**101010 101**<br>**1**||**+**|**010101 0101**|**+**|**111010 1010**|**+**|
|**Decoded**<br>**Character Stream**|**-**|**D21.0**||**+**|**D10.2**|**+**|**Invalid**|**+**|
|Error occurs here<br>Error detected here|||||||||



**401** 

**PCI Ex ress Technolo p gy** 

## **Descrambler** 

The descrambler is fed by the 8b/10b decoder. It only descrambles Data (D) characters associated with a TLP or DLLP (D/K# is high). It doesn’t descramble Control (K) characters or ordered sets because they’re not scrambled at the transmitter. 

## **Some Descrambler Implementation Rules:** 

- On a multi‐Lane Link, descramblers associated with each Lane must oper‐ ate in concert, maintaining the same simultaneous value in each LFSR. 

- Descrambling is applied to ‘D’ characters associated with TLP and DLLPs including the Logical Idle (00h) sequence. ‘D’ characters within ordered set are not descrambled. 

- ‘K’ characters and ordered set characters bypass the descrambler logic. 

- Compliance Pattern characters are not descrambled. 

- When a COM character enters the descrambler, it reinitializes the LFSR value to FFFFh. 

- With one exception, the LFSR serially advances eight times for every char‐ acter (D or K character) received. The LFSR does NOT advance on SKP characters associated with the SKIP ordered sets received. The reason the LFSR is not advanced on detecting SKPs is because there may be a differ‐ ence between the number of SKP characters transmitted and the SKP char‐ acters exiting the Elastic Buffer (as discussed in “Receiver Clock Compensation Logic” on page 396). 

## **Disabling Descrambling** 

By default, descrambling is always enabled, but the spec allows it to be disabled for test and debug purposes although no standard software method is given for disabling it. If the descrambler receives at least two TS1/TS2 ordered sets with the “disable scrambling” bit set on all of its configured Lanes, it disables the descrambler. 

## **Byte Un-Striping** 

Figure 11‐26 on page 403 shows eight character streams from the descramblers of a x8 Link being un‐striped into a single byte stream which is fed to the char‐ acter filter logic. 

**402** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐26: Example of x8 Byte Un‐Striping_ 

**==> picture [354 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Multiplexer block<br>Data Stream D/K#<br>Character 0<br>Character 1<br>Character 2<br>Character 3<br>Character 4<br>Character 5<br>Character 6<br>Character 7<br>Byte Un-Striping<br>Character 0 Character 1 Character 7<br>Character 8 Character 9 Character 15<br>Character 16 Character 17 Character 23<br>From Lane 0 From Lane 1 From Lane 7<br>De-Scrambler De-Scrambler De-Scrambler<br>**----- End of picture text -----**<br>


## **Filter and Packet Alignment Check** 

The serial byte stream supplied by the byte un‐striping logic contains TLPs, DLLPs, Logical Idle sequences, Control characters such as STP, SDP, END, EDB, and PADs, as well as the ordered sets. Of these, the Logical Idle sequence, the control characters and ordered sets are detected and eliminated before they get to the next layer. What remains are the TLPs and DLLPs and these are sent to the Rx Buffer along with an indicator of the start and end of each packet. 

## **Receive Buffer (Rx Buffer)** 

The Rx Buffer holds received TLPs and DLLPs after the start and end characters have been eliminated. The received packets are ready to send to the Data Link Layer. The interface to the Data Link Layer is not described in the spec, so the designer is free to decide details like data bus width. As an example, we can 

**403** 

**PCI Ex ress Technolo p gy** 

assume an interface clock of 250MHz and a Gen1 speed on the Link. For that case, the number of bytes in the data bus between these layers would be the same as the number of Lanes supported. 

## **Physical Layer Error Handling** 

## **General** 

Physical Layer errors are reported as Receiver Errors to the Data Link Layer. According to the spec, some errors must be checked and trigger a receiver error, while others are optional. 

Required error checking: 

- 8b/10b decode errors: disparity error, illegal Symbol 

Optional error checking: 

- Loss of Symbol lock (see “Achieving Symbol Lock” on page 396) 

- Elastic Buffer overflow or underflow 

- Lane deskew errors (see “Lane‐to‐Lane Skew” on page 398) 

- Packets inconsistent with format rules 

## **Response of Data Link Layer to Receiver Error** 

If the Physical Layer indicates a Receiver Error to the Data Link Layer, the Data Link Layer discards the TLP currently being received and frees any storage allo‐ cated for the TLP. It then schedules a NAK to go back to the transmitter of the TLP. That causes the transmitter to replay TLPs from the Replay Buffer, which should automatically correct the error. The Data Link Layer may also direct the Physical Layer to initiate Link re‐training. 

If the PCI Express Extended Advanced Error Capabilities register set is imple‐ mented, a Receiver Error sets the Receiver Error Status bit in the Correctable Error Status register. If enabled, the device can send an ERR_COR (correctable error) message to the Root Complex. 

**404** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Active State Power Management** 
