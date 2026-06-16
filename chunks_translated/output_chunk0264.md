'D' Character<br>Transaction Layer Packet (TLP)<br>STP Sequence Header Data Payload  ECRC LCRC END<br>'D' Character<br>'K' Character 'K' Character<br>Data Link Layer Packet (DLLP)<br>SDP DLLP Type Misc. CRC END<br>'K' Character 'K' Character<br>**----- 图片文字结束 -----**<br>


## **字节交叉（用于宽链路）**

我们示例中显示的下一步是字节交叉，尽管仅当端口实现多个 Lane（称为宽链路）时才需要。交叉意味着字符流中的每个连续输出字符被路由到连续的 Lane。使用的 Lane 数量是在链路训练过程中配置的，基于共享链路的两个设备所支持的。

以下图中说明了字节交叉的三个示例。在第 372 页的图 11-8 中，显示了单 Lane 链路 (x1)。这不是一个非常有趣的案例，因为报文一次以一个字节进入物理层并以相同的方式离开，但它说明了字符序列的绘制方式。

第 372 页的图 11-9 显示了来自多路复用器的传入 Dword 报文。每个字节被定向到相应的 Lane。最后，第 373 页的图 11-10 说明了一个八 Lane (x8) 链路。在此示例中，需要两个 Dword 才能填充所有 8 个 Lane。这要求 Dword 以比先前示例快两倍的速率到达。每个 Lane 上发送的数据格式将在以下小节中描述。

**371**

## **PCI Exress Technology**

_图 11-8：x1 字节交叉_

**==> 图片 [154 x 220] 已省略 <==**

**----- 图片文字开始 -----**<br>
Packet byte stream from Mux block<br>8 D/K#<br>Character 7<br>Character 6<br>Character 5<br>Character 4<br>Character 3<br>Character 2<br>Character 1<br>Character 0<br>x1 Byte Striping 8 D/K#<br>Character 2<br>Character 1<br>Character 0<br>8 D/K#<br>To Scrambler<br>**----- 图片文字结束 -----**<br>


_图 11-9：x4 字节交叉_

**==> 图片 [338 x 205] 已省略 <==**

**----- 图片文字开始 -----**<br>
Packet Dword Stream from Mux Block<br>D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>Character 12 Character 13 Character 14 Character 15<br>Character 16 Character 17 Character 11 Character 11<br>Character 8 Character 9 Character 7 Character 7<br>Character 0 Character 1 Character 3 Character 3<br>8 D/K# 8 D/K# 8 D/K# 8 D/K#<br>To Lane 0 To Lane 1 To Lane 2 To Lane 3<br>Scrambler Scrambler Scrambler Scrambler<br>**----- 图片文字结束 -----**<br>


**372**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-10：使用 DWord 并行数据的 x8 字节交叉_

**==> 图片 [368 x 240] 已省略 <==**

**----- 图片文字开始 -----**<br>
D/K# D/K# D/K# D/K#<br>8 8 8 8<br>Character 20 Character 21 Character 22 Character 23<br>Character 16 Character 17 Character 18 Character 19<br>Character 12 Character 13 Character 14 Character 15<br>Character 8 Character 9 Character 10 Character 11<br>Character 4 Character 5 Character 6 Character 7<br>Character 0 Character 1 Character 2 Character 3<br>x8 Byte Striping<br>Character 16 Character 17 Character 23<br>Character 8 Character 9 Character 15<br>Character 0 Character 1 Character 7<br>8 D/K# 8 D/K# 8<br>To Lane 0 To Lane 1 To Lane 7<br>Scrambler Scrambler Scrambler<br>**----- 图片文字结束 -----**<br>


## **报文格式规则**

## **一般规则**

- 每个报文的总报文长度（包括起始和结束字符）始终是四的倍数。这是数据长度以 dword 为单位测量的自然扩展。

- TLP 以 STP 字符开始，以 END 或 EDB 字符结束。

- DLLP 以 SDP 开始，以 END 字符结束。并且正好 8 个字符长 (SDP + 6 字符 + END)。

- STP 和 SDP 字符在逻辑空闲传输之后开始报文传输时放置在 Lane 0 上。在其他情况下，它们可以从可被 4 整除的 Lane 编号开始。

- 接收方的物理层允许监视这些规则的违规行为，并可能将其作为接收方错误报告给数据链路层。

**373**

**PCI Exress Technology**

## **示例：x1 格式**

第 374 页的图 11-11 中所示的示例说明了通过 x1 链路（仅一个 Lane 运行的链路）传输的报文的格式。显示了一系列报文，其中穿插了一个 SKIP 有序集。末尾显示了逻辑空闲，以表示发送方没有更多报文要发送并使用空闲字符作为填充的情况。

_图 11-11：x1 报文格式_

**==> 图片 [351 x 220] 已省略 <==**

**----- 图片文字开始 -----**<br>
Lane<br>0<br>STP COM STP STP<br>SKP<br>TLP SKP TLP<br>SKP<br>STP<br>TLP<br>END END<br>SDP SDP<br>DLLP TLP DLLP<br>END<br>Idle (00h)<br>Idle (00h)<br>Idle (00h)<br>END END END<br>Time<br>**----- 图片文字结束 -----**<br>


## **x4 格式规则**

- STP 和 SDP 字符始终在 Lane 0 上发送。

- END 和 EDB 字符始终在 Lane 3 上发送。

- 当发送有序集（如 SKIP）时，它必须同时出现在所有 Lane 上。

- 当传输逻辑空闲时，它们必须同时在所有 Lane 上发送。

- 这些规则的任何违规都可能作为接收方错误报告给数据链路层。

**374**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **示例 x4 格式**

第 375 页的图 11-12 中所示的示例说明了通过 x4 链路（具有四个运行数据 Lane 的链路）发送的报文的格式。该图显示了一个 TLP，后跟在所有 Lane 上传输的用于接收方时钟补偿的 SKIP 有序集。接下来是一个 DLLP，然后是所有 Lane 上的逻辑空闲。本例强调了报文始终是 4 的字符倍数，因为起始字符始终出现在 Lane 0 中，而结束字符始终在 Lane 3 中。它还说明了有序集必须同时出现在所有 Lane 上。

_图 11-12：x4 报文格式_

**375**

**PCI Exress Technology**

## **大链路宽度报文格式规则**

以下规则适用于通过 x8、x12、x16 或 x32 链路传输报文时：

- 当在传输逻辑空闲期间之后开始传输时，STP/SDP 字符始终在 Lane 0 上发送。之后，当发送背靠背报文时，它们只能发送到可被 4 整除的 Lane 编号（Lane 4、8、12 等）。

- END/EDB 字符发送到可被 4 整除的 Lane 编号，然后减一（Lane 3、7、11 等）。

- 如果报文没有在链路的最后一个 Lane 上结束，并且没有更多准备发送的报文，则 PAD 符号用作剩余 Lane 编号的填充。逻辑空闲不能用于此目的，因为它必须同时出现在所有 Lane 上。

- 有序集必须同时在所有 Lane 上发送。

- 类似地，逻辑空闲在使用时必须在所有 Lane 上发送。

- 这些规则的任何违规都可能作为接收方错误报告给数据链路层。

## **x8 报文格式示例**

第 377 页的图 11-13 中所示的示例说明了通过 x8 链路传输的报文的格式。该图显示了一个 TLP，后跟 SKIP 有序集、一个 DLLP，最后是一个在 Lane 3 结束的 TLP。在那时，发送方没有更多准备发送的报文，但当前报文未扩展到包括所有可用 Lane。有人可能期望用逻辑空闲填充额外的 Lane，但这在这里不起作用，因为空闲必须同时出现在所有 Lane 上。因此需要另一个填充字符，规范编写者选择在此处使用 PAD 控制字符。PAD 唯一使用的另一个位置是在训练过程中。最后，由于仍没有更多要发送的报文，因此会在所有 Lane 上发送逻辑空闲。

**376**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

_图 11-13：x8 报文格式_

## **加扰器**

我们示例中的下一步是加扰，如图 11-5（第 369 页）所示，旨在防止数据流中的重复模式。重复模式在链路上产生"纯音"，这意味着由该模式产生的一致频率会产生比通常更多的噪声或 EMI。通过将此能量扩展到更宽的频率范围来减少此问题是加扰的主要目标。此外，单个 Lane 上的加扰传输还可减少对宽链路上相邻 Lane 的干扰。这种"空间频率去相关"，或减少串扰噪声，有助于每个 Lane 上的接收方区分所需的信号。

**377**

## **PCI Exress Technology**

为了帮助接收方与加扰序列保持同步，控制字符不会进行加扰，因此即使加扰器失去同步，它们也可被识别。此外，COM 控制字符 (K28.5) 的每次到达都会重新初始化链路两端的加扰器，从而重新同步它们。

## **加扰算法**

规范中描述的加扰器如图 11-14（第 378 页）所示。它由一个 16 位线性反馈移位寄存器 (Linear Feedback Shift Register, LFSR) 组成，其反馈点实现以下多项式：

G(x) = X[16] + X[5] + X[4] + X[3] + 1

_图 11-14：加扰器_

LFSR 以馈送数据字节的时钟频率的 8 倍频率进行计时，其输出被计时到 8 位寄存器中，该寄存器与 8 位数据字符进行 XOR 以形成加扰的数据输出。

**378**

**第 11 章：物理层 - 逻辑 (Gen1 和 Gen2)**

## **一些加扰器实现规则：**

- 在多 Lane 链路实现中，与每个 Lane 相关联的加扰器必须协同工作，在每个 LFSR 中保持相同的同步值。

- 加扰仅应用于 'D' 字符，即与 TLP 和 DLLP 以及逻辑空闲 (00h) 字符相关联的字符。但是，TS1 和 TS2 有序集内的那些 'D' 字符不会被加扰。

- 加扰从不应用于 'K' 字符和有序集中的字符，例如 TS1、TS2、SKIP、FTS 和电子空闲。这些字符绕过加扰器逻辑。其中一个原因是确保即使加扰器意外失去顺序，它们仍然可以被接收方识别。

- 合规性模式字符（用于测试）也不会被加扰。

- COM 字符（不会被加扰的控制字符）用于将链路两端的 LFSR 重新初始化为 FFFFh。

- 除 COM 字符外，LFSR 通常对每个发送的 D 或 K 字符串行前进 8 次，但它在与 SKIP 有序集关联的 SKP 字符上不前进。原因在于接收方可能会添加或删除 SKP 符号以执行时钟容限补偿。改变接收方中的字符数与发送的字符数相比，如果不忽略这些字符，则会导致接收方 LFSR 中的值与发送方 LFSR 值失去同步。

## **禁用加扰**

加扰默认启用，但规范允许出于测试和调试目的禁用它。这是因为测试可能需要控制发送的确切比特模式，并且由于硬件处理加扰，因此软件没有合理的方法来强制执行特定模式。规范未定义用于指示物理层禁用加扰的特定软件机制，因此这必须是特定于设计的实现。
