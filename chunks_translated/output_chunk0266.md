'D' Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>'D' Character<br>'K' Character 'K' Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>'K' Character 'K' Character<br>**----- End of picture text -----**


## **字节条带化（用于宽链路）**

我们示例中显示的下一步是字节条带化 (Byte Striping)，尽管仅当端口实现多个 Lane（称为宽链路 (wide Link)）时才需要此步骤。条带化意味着字符流中的每个连续输出字符被路由到连续的 Lane 上。使用的 Lane 数在链路训练 (Link training) 过程中根据共享链路的两台设备所支持的 Lane 数进行配置。

以下图表中说明了字节条带化的三个示例。在第 372 页图 11-8 中，显示了单 Lane 链路 (x1)。这不是一个非常有趣的案例，因为数据包以字节为单位进入物理层 (Physical Layer) 并以相同方式发出，但它说明了字符序列的绘制方式。

第 372 页图 11-9 显示了来自多路复用器的传入双字 (Dword) 数据包。每个字节被定向到对应的 Lane。最后，第 373 页图 11-10 说明了八 Lane (x8) 链路。在此示例中，需要两个双字 (Dwords) 来填充所有 8 个 Lane。这要求双字以比前一示例快两倍的速率到达。后续章节中描述了通过每个 Lane 发送的数据格式。

**371**

## **PCI Express 技术**

_图 11-8：x1 字节条带化_

**==> picture [154 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- End of picture text -----**


_图 11-9：x4 字节条带化_

**==> picture [338 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- End of picture text -----**


**372**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-10：使用双字并行数据的 x8 字节条带化_

**==> picture [368 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- End of picture text -----**


## **数据包格式规则**

## **一般规则**

- 每个数据包的总长度（包括开始和结束字符）始终是 4 的倍数。这是数据长度以双字 (dwords) 为单位这一事实的自然延伸。

- TLP 以 STP 字符开始，并以 END 或 EDB 字符结束。

- DLLP 以 SDP 开头，以 END 字符结束，并且恰好为 8 个字符长 (SDP + 6 个字符 + END)。

- 在发送完逻辑空闲 (Logical Idles) 后开始传输数据包时，STP 和 SDP 字符被放置在 Lane 0 上。在其他情况下，它们可以以可被 4 整除的 Lane 号开始。

- 接收方的物理层 (Physical Layer) 允许监视对这些规则的违反情况，并可将其作为接收器错误 (Receiver Errors) 报告给数据链路层 (Data Link Layer)。

**373**

**PCI Express 技术**

## **示例：x1 格式**

第 374 页图 11-11 中所示的示例说明了通过 x1 链路（仅一个 Lane 工作的链路）传输的数据包的格式。图中显示了一系列数据包，其中穿插着一个 SKIP 有序集。最后显示逻辑空闲 (Logical Idles)，以表示发送器没有更多数据包可发送并使用空闲字符作为填充的情况。

_图 11-11：x1 数据包格式_

**==> picture [351 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- End of picture text -----**


## **x4 格式规则**

- STP 和 SDP 字符始终在 Lane 0 上发送。

- END 和 EDB 字符始终在 Lane 3 上发送。

- 当发送有序集（例如 SKIP）时，必须同时出现在所有 Lane 上。

- 当发送逻辑空闲 (Logical Idles) 时，必须同时在所有 Lane 上发送。

- 对这些规则的任何违反都可以作为接收器错误 (Receiver Error) 报告给数据链路层 (Data Link Layer)。

**374**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **x4 格式示例**

第 375 页图 11-12 中所示的示例说明了通过 x4 链路（四条数据 Lane 工作的链路）发送的数据包的格式。该图显示了在所有 Lane 上发送的一个 TLP 后跟一个 SKIP 有序集，用于接收器时钟补偿。接下来是一个 DLLP，然后是所有 Lane 上的逻辑空闲 (Logical Idle)。此示例突出表明数据包始终是 4 的倍数，因为起始字符始终出现在 Lane 0 中，结束字符始终在 Lane 3 中。它还说明有序集必须同时出现在所有 Lane 上。

_图 11-12：x4 数据包格式_

**375**

**PCI Express 技术**

## **大链路宽度数据包格式规则**

当通过 x8、x12、x16 或 x32 链路传输数据包时，以下规则适用：

- 在发送完一段时间的逻辑空闲 (Logical Idles) 后开始发送时，STP/SDP 字符始终在 Lane 0 上发送。在此之后，仅当背靠背发送数据包时，它们才能在可被 4 整除的 Lane 号上发送（Lane 4、8、12 等）。

- END/EDB 字符在可被 4 整除然后减一的 Lane 号上发送（Lane 3、7、11 等）。

- 如果数据包未在链路的最后一个 Lane 上结束，并且没有更多准备发送的数据包，则使用 PAD 符号 (PAD Symbols) 作为其余 Lane 号的填充。逻辑空闲 (Logical Idle) 不能用于此目的，因为它必须同时出现在所有 Lane 上。

- 有序集必须同时在所有 Lane 上发送。

- 类似地，在使用逻辑空闲时，必须同时在所有 Lane 上发送。

- 对这些规则的任何违反都可以作为接收器错误 (Receiver Error) 报告给数据链路层 (Data Link Layer)。

## **x8 数据包格式示例**

第 377 页图 11-13 中所示的示例说明了通过 x8 链路传输的数据包的格式。该图显示了一个 TLP 后跟一个 SKIP 有序集、一个 DLLP，最后是一个在 Lane 3 上结束的 TLP。此时，发送器没有更多准备发送的数据包，但当前数据包未扩展到包括所有可用的 Lane。人们可能期望用逻辑空闲 (Logical Idle) 填充额外的 Lane，但在这里不起作用，因为空闲必须同时出现在所有 Lane 上。因此需要另一个填充字符，规范作者选择在此处使用 PAD 控制字符。PAD 唯一使用的另一个地方是在训练过程中。最后，由于仍然没有更多数据包可发送，因此在所有 Lane 上发送逻辑空闲 (Logical Idles)。

**376**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-13：x8 数据包格式_

## **加扰器**

我们示例中的下一步是加扰 (scrambling)，如第 369 页图 11-5 所示，旨在防止数据流中出现重复模式。重复模式会在链路上产生"纯音"，即由模式引起的超过通常噪声的一致频率，或称为 EMI (电磁干扰)。通过将能量扩展到更宽的频率范围来减少此问题是加扰的主要目标。此外，一条 Lane 上的加扰传输还可减少宽链路上相邻 Lane 之间的干扰。这种"空间去相关"或串扰噪声的减少有助于每个 Lane 上的接收器区分所需信号。

**377**

## **PCI Express 技术**

为了帮助接收器与加扰序列保持同步，控制字符不会被加扰，因此即使加扰器失去同步也是可识别的。此外，COM 控制字符 (K28.5) 每次到达时都会重新初始化链路两端的加扰器，从而使其重新同步。

## **加扰算法**

规范中描述的加扰器 (scrambler) 如第 378 页图 11-14 所示。它由一个 16 位线性反馈移位寄存器 (Linear Feedback Shift Register, LFSR) 组成，其反馈点实现以下多项式：

G(x) = X[16] + X[5] + X[4] + X[3] + 1

_图 11-14：加扰器_

LFSR 以馈送数据字节的时钟频率的 8 倍频率进行计时，其输出被计时进入一个 8 位寄存器，该寄存器与 8 位数据字符进行 XOR 异或运算以形成加扰数据输出。

**378**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **一些加扰器实现规则：**

- 在多 Lane 链路 (multi‐Lane Link) 实现中，与每个 Lane 关联的加扰器 (Scramblers) 必须协调运行，在每个 LFSR 中保持相同的同步值。

- 加扰 (Scrambling) 仅应用于 'D' 字符，即那些与 TLP 和 DLLP 以及逻辑空闲 (Logical Idle, 00h) 字符相关联的字符。但是，TS1 和 TS2 有序集内的那些 'D' 字符不会被加扰。

- 加扰 (Scrambling) 从不应用于 'K' 字符以及有序集内的字符，例如 TS1、TS2、SKIP、FTS 和电气空闲 (Electrical Idle)。这些字符绕过加扰器逻辑。这样做的一个原因是确保即使加扰器以某种方式失去序列，接收器仍然可以识别它们。

- 合规模式 (Compliance Pattern) 字符（用于测试）也不被加扰。

- COM 字符（不被加扰的控制字符）用于将发送器和接收器两端的 LFSR 重新初始化为 FFFFh。

- 除 COM 字符外，LFSR 通常在每发送一个 D 或 K 字符时串行推进 8 次，但在与 SKIP 有序集关联的 SKP 字符上不推进。原因是接收器可以添加或删除 SKP 符号以执行时钟容差补偿。如果不忽略 SKP 字符，与发送的数量相比，接收器中字符数量的变化将导致接收器 LFSR 中的值与发送器 LFSR 值失去同步。

## **禁用加扰**

默认情况下启用加扰 (Scrambling)，但规范允许出于测试和调试目的将其禁用。那是因为测试可能需要控制发送的确切位模式，并且由于硬件处理加扰，软件没有合理的方法来强制特定模式。规范中未定义用于指示物理层 (Physical Layer) 禁用加扰的特定软件机制，因此这必须是特定于设计 (design‐specific) 的实现。
