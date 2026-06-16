If scrambling is disabled by a device, this gets communicated to the neighbor‐ ing device by sending at least two TS1s and TS2s that have the appropriate bit set in the control field as described in “Configuration State” on page 539. In response, the neighboring device also disables its scrambling. 

**379** 

**PCI Ex ress Technolo p gy** 

## **8b/10b Encoding** 

## **General** 

The first two generations of PCIe use 8b/10b encoding. Each Lane implements an 8b/10b Encoder that translates the 8‐bit characters into 10‐bit Symbols. This coding scheme was patented by IBM in 1984 and is widely used in many serial transports today, such as Gigabit Ethernet and Fibre Channel. 

## **Motivation** 

Encoding accomplishes several desirable goals for serial transmission. Three of the most important are listed here: 

- **Embedding a Clock into the Data.** Encoding ensures that the data stream has enough edges in it to recover a clock at the Receiver, with the result that a distributed clock is not needed. This avoids some limitations of a parallel bus design, such as flight time and clock skew. It also eliminates the need to distribute a high‐frequency clock that would cause other problems like increased EMI and difficult routing. 

   - As an example of this process, Figure 11‐15 on page 381 shows the encoding results of the data byte 00h. As can be seen, this 8‐bit character that had no transitions converts to a 10‐bit Symbol with 5 transitions. The 8b/10b guar‐ antees enough edges to ensure the “run length” (sequence of consecutive ones or zeros) in the bit stream to no more than 5 consecutive bits under any conditions. 

- **Maintaining DC Balance.** PCIe uses an AC‐coupled link, placing a capaci‐ tor serially in the path to isolate the DC part of the signal from the other end of the Link. This allows the Transmitter and Receiver to use different com‐ mon‐mode voltages and makes the electrical design easier for cases where the path between them is long enough that they’re less likely to have exactly the same reference voltages. That DC value, or common‐mode voltage, can change during run time because the line charges up when the signal is driven. Normally, the signal changes so quickly that there isn’t time for this to cause a problem but, if the signal average is predominantly one level or the other, the common‐mode value will appear to drift. Referred to as “DC Wander”, this drifting voltage degrades signal integrity at the Receiver. To compensate, the 8b/10b encoder tracks the “disparity” of the last Symbol that was sent. Disparity, or inequality, simply indicates whether the previ‐ ous Symbol had more ones than zeros (called positive disparity), more zeros than ones (negative disparity), or a balance of ones and zeros (neutral 

**380** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

   - disparity). If the previous Symbol had negative disparity, for example, the next one should balance that by using more ones. 

- **Enhancing Error Detection.** The encoding scheme also facilitates the detec‐ tion of transmission errors. For a 10‐bit value, 1024 codes are possible, but the character to be encoded only has 256 unique codes. To maintain DC bal‐ ance the design uses two codes for each character, and chooses which one based on the disparity of the last Symbol that was sent, so 512 codes would be needed. However, many of the neutral disparity encodings have the same values (D28.5 is one example), so not all 512 are used. As a result, more than half the possible encodings are not used and will be considered illegal if seen at a Receiver. If a transmission error does change the bit pat‐ tern of a Symbol, there’s a good chance the result would be one of these ille‐ gal patterns that can be recognized right away. For more on this see the section titled, “Disparity” on page 383. 

The major disadvantage of 8b/10b encoding is the overhead it requires. The actual transmission performance is degraded by 20% from the Receiver’s point of view because 10 bits are sent for each byte, but only 8 useful bits are recov‐ ered at the receiver. This is a non‐trivial price to pay but is still considered acceptable to gain the advantages mentioned. 

_Figure 11‐15: Example of 8‐bit Character 00h Encoding_ 

**==> picture [224 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
8b Value<br>0 0 0 0 0 0 0 0<br>Data 00h<br>10b Encoded<br>0 11 0 0 0 1 0 1 1<br>Value<br>**----- End of picture text -----**<br>


## **Properties of 10-bit Symbols** 

As described in the literature on 8b/10b coding, the design isn’t strictly 8 bits to 10 bits. Instead, it’s really a 5‐to‐6 bit encoding followed by a 3‐to‐4 bit encoding. The sub‐blocks are internal to the design but their existence helps to explain some of the properties for a legal Symbol, as listed below. A Symbol that doesn’t follow these properties is considered invalid. 

**381** 

**PCI Ex ress Technolo p gy** 

- The bit stream never contains more than five continuous 1s or 0s, even from the end of one Symbol to beginning of the next. 

- Each 10‐bit Symbol contains: 

   - Four 0s and six 1s (not necessarily contiguous), or 

   - Six 0s and four 1s (not necessarily contiguous), or 

   - Five 0s and five 1s (not necessarily contiguous). 

- Each 10‐bit Symbol is subdivided into two sub‐blocks: the first is six bits wide and the second is four bits wide. 

   - The 6‐bit sub‐block contains no more than four 1s or four 0s. 

   - The 4‐bit sub‐block contains no more than three 1s or three 0s. 

## **Character Notation** 

The 8b/10b uses a special notation shorthand, and Figure 11‐16 on page 382 illustrates the steps to arrive at the shorthand for a given character: 

1. Partition the character into its 3‐bit and 5‐bit sub‐blocks. 

2. Transpose the position of the sub‐blocks. 

3. Create the decimal equivalent for each sub‐block. 

4. The character takes the form Dxx.y for Data characters, or Kxx.y for Control characters. In this notation, xx is the decimal equivalent of the 5‐bit field, and y is the decimal equivalent of the 3‐bit field. 

_Figure 11‐16: 8b/10b Nomenclature_ 

**==> picture [348 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
8b Designation Example Data (6Ah)<br>D/<br>8b Character 7 6 5 4 3 2 1 0 D 01101010<br>K#<br>Partition into D/ H G F E D C B A<br>D 011 01010<br>sub-blocks K#<br>Flip sub-blocks K#D/ E D C B A H G F D 01010 011<br>Convert sub-blocks<br>to decimal notation D/K xx . y D 10 . 3<br>Final Notation D/Kxx.y D10.3<br>**----- End of picture text -----**<br>


**382** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

## **Disparity** 

**Definition.** Disparity refers to the inequality between the number of ones and zeros within a 10‐bit Symbol and is used to help maintain DC balance on the link. A Symbol with more zeros is said to have a negative (–) dispar‐ ity, while a Symbol with more ones has a positive (+) disparity. When a Symbol has an equal number of ones and zeros, it’s said to have a neutral disparity. Interestingly, most characters encode into Symbols with + or – dis‐ parity, but some only encode into Symbols with neutral disparity. 

**CRD (Current Running Disparity).** The CRD is the information as to the current state of disparity on the link. Since it’s just a single bit it can only be positive or negative and doesn’t always change when the next Symbol is sent out. To see how it works, remember that the next Symbol decoded can have negative, neutral, or positive disparity, then consider the following example. If the CRD was positive, an outgoing Symbol with a negative dis‐ parity would change it to negative, a neutral disparity would leave it as positive, and a positive disparity would be an error because the CRD is only one bit and can’t be made more positive. 

The initial state of the CRD (before any characters are transmitted) may not match between the sender and receiver but it turns out that it doesn’t mat‐ ter. When the receiver sees the first Symbol after training is complete, it will check for a disparity error and, if one is found, just change the CRD. This won’t be considered an error but simply an adjustment of the CRD to match the receiver and sender. After that, there are only two legal CRD cases: it can remain the same if the new Symbol has neutral disparity, or it can flip to the opposite polarity if the new Symbol has the opposite disparity. What is not legal is for the disparity of the new Symbol to be the same as the CRD. Such an event would be a disparity error and should never occur after the initial adjustment unless an error has occurred. 

## **Encoding Procedure** 

There are different ways that 8b/10b encoding could be accomplished. The sim‐ plest approach is probably to implement a look‐up table that contains all the possible output values. However, this table can require a comparatively large number of gates. Another approach is to implement the decoder as a logic block, and this is usually the preferred choice because it typically results in a smaller and cheaper solution. The specifics of the encoding logic are described in detail in the referenced literature, so we’ll focus here on the bigger picture of how it works instead. 

**383** 

## **PCI Ex ress Technolo p gy** 

An example 8b/10b block diagram is shown in Figure 11‐17 on page 384. A new outgoing Symbol is created based on three things: the incoming character, the D/K# indication for that character, and the CRD. A new CRD value is computed based on the outgoing Symbol and is fed back for use in encoding the next char‐ acter. After encoding, the resulting Symbol is fed to a serializer that clocks out the individual bits. Figure 11‐18 on page 385 shows some sample 8b/10b encod‐ ings that will be useful for the example that follows. 

_Figure 11‐17: 8‐bit to 10‐bit (8b/10b) Encoder_ 

**==> picture [343 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bytes from Scrambler D/K#<br>8b Character 7 6 5 4 3 2 1 0<br>H G F E D C B A<br>8b/10b Encoding Logic<br>Current<br>Running<br>Disparity<br>(CRD)<br>CRD Calculator j h g f i e d c b a<br>Serial Stream<br>Serializer j h g f i e d c b a to Transmitter<br>using Tx Clock<br>**----- End of picture text -----**<br>


**384** 

**Chapter 11: Physical Layer - Logical (Gen1 and Gen2)** 

_Figure 11‐18: Example 8b/10b Encodings_ 

## **Example Transmission** 

Figure 11‐19 illustrates the encode and transmission of three characters: the first and second are the control character K28.5 and the third character is the data character D10.3. 

In this example the initial CRD is negative so K28.5 encodes into 001111 1010b. This Symbol has positive disparity (more ones than zeros), and causes the CRD polarity to flip to positive. The next K28.5 is encoded into 110000 0101b and has a negative disparity. That causes the CRD this time to flip to negative. Finally, D10.3 is encoded into 010101 1100b. Since its disparity is neutral, the CRD doesn’t change in this case but remains negative for whatever the next character will be. 

**385** 

**PCI Ex ress Technolo p gy** 

_Figure 11‐19: Example 8b/10b Transmission_ 

## **Use these two characters in the example below:** 

|**D/K#**|**Hex**<br>**Byte**|**Binary Bits**<br>**HGF EDCBA**|**Byte**<br>**Name**|**CRD –**<br>**abcdei fghj**|**CRD +**<br>**abcdei fghj**|
|---|---|---|---|---|---|
|**Control(K)**|**BC**|**101 11100**|**K28.5**|**001111 1010**|**110000 0101**|
|**Data(D)**|**6A**|**011 01010**|**D10.3**|**010101 1100**|**010101 0011**|



## **Example Transmission** 

||**CRD**|**Character**|**CRD**|**Character**|**CRD**|**Character**|**CRD**|
|---|---|---|---|---|---|---|---|
|**Character to**<br>**be transmitted**|**-**|**K28.5 (BCh)**|**+**|**K28.5 (BCh)**|**-**|**D10.3 (6Ah)**|**-**|