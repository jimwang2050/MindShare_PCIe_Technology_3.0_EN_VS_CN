1. 第一个块由同步头 01b 组成，包含 64 个 1 后跟 64 个 0 的未加扰有效负载。

2. 第二个块具有同步头 01b，包含第 530 页表 14‐4 中所示的未加扰有效负载（注意，该模式在 8 个 Lane 后重复，P 表示正在使用的 4 位 Tx 预设，而 ~P 是其按位取反）。

3. 第三个块具有同步头 01b，包含第 531 页表 14‐5 中所示的未加扰有效负载（与第二个块的注释相同）。

4. 第四个块是 EIEOS 块

5. 32 个更多数据块，每个块包含 16 个加扰 IDL 符号 (00h)。

_表 14‐4：128b/130b 合规模式的第二个块_

|**符号**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|0|55h|FFh|FFh|FFh|55h|FFh|FFh|FFh|
|1|55h|FFh|FFh|FFh|55h|FFh|FFh|FFh|



**530**

**第 14 章：链路初始化与训练**

_表 14‐4：128b/130b 合规模式的第二个块（续）_

|**符号**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|2|55h|00h|FFh|FFh|55h|FFh|FFh|FFh|
|3|55h|00h|FFh|C0h|55h|FFh|F0h|F0h|
|4|55h|00h|FFh|00h|55h|FFh|00h|00h|
|5|55h|00h|C0h|00h|55h|E0h|00h|00h|
|6|55h|00h|00h|00h|55h|00h|00h|00h|
|7|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|
|8|00h|1Eh|2Dh|3Ch|4Bh|5Ah|69h|78h|
|9|00h|55h|00h|00h|00h|55h|00h|F0h|
|10|00h|55h|00h|00h|00h|55h|00h|00h|
|11|00h|55h|00h|00h|00h|55h|00h|00h|
|12|00h|55h|0Fh|0Fh|00h|55h|07h|00h|
|13|00h|55h|FFh|FFh|00h|55h|FFh|00h|
|14|00h|55h|FFh|FFh|7Fh|55h|FFh|00h|
|15|00h|55h|FFh|FFh|FFh|55h|FFh|00h|



_表 14‐5：128b/130b 合规模式的第三个块_

|**符号**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|0|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|1|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|2|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|3|F0h|F0h|55h|F0h|F0h|F0h|55h|F0h|
|4|00h|00h|55h|00h|00h|00h|55h|00h|



**531**

## **PCI Express Technology**

_表 14‐5：128b/130b 合规模式的第三个块（续）_

|**符号**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|5|00h|00h|55h|00h|00h|00h|55h|00h|
|6|00h|00h|55h|00h|00h|00h|55h|00h|
|7|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|
|8|00h|1Eh|2Dh|3Ch|4Bh|5Ah|69h|78h|
|9|00h|00h|00h|55h|00h|00h|00h|55h|
|10|00h|00h|00h|55h|00h|00h|00h|55h|
|11|00h|00h|00h|55h|00h|00h|00h|55h|
|12|FFh|0Fh|0Fh|55h|0Fh|0Fh|0Fh|55h|
|13|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|
|14|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|
|15|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|



**8b/10b 的修改合规模式。** 第二种合规模式添加了一个错误状态字段，该字段报告在 Polling.Compliance 中检测到的接收器错误数。

在 8b/10b 模式下，仍使用原始模式，但添加了 2 个符号来报告错误状态（使用 2 个而不是一个以避免干扰序列所需的差异），并在末尾添加了 2 个 K28.5 符号，使该模式总共 8 个符号长。

_表 14‐6：8b/10b 修改合规模式的符号序列_

|符号|Lane 0|Lane 1|Lane 2|...|Lane 8|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|D|K28.5+|K28.5+||D|
|3|D|D10.2|D10.2||D|



**532**

**第 14 章：链路初始化与训练**

_表 14‐6：8b/10b 修改合规模式的符号序列（续）_

|符号|Lane 0|Lane 1|Lane 2|...|Lane 8|
|---|---|---|---|---|---|
|4|K28.5‐|ERR|ERR||K28.5‐|
|5|K21.5|ERR|ERR||K21.5|
|6|K28.5+|K28.5‐|K28.5‐||K28.5+|
|7|D10.2|K28.5+|K28.5+||D10.2|
|8|ERR|K28.5‐|K28.5‐||ERR|
|9|ERR|K21.5|K21.5||ERR|
|10|K28.5‐|K28.5+|K28.5+||K28.5‐|
|11|K28.5+|D10.2|D10.2||K28.5+|
|12|K28.7‐|ERR|ERR||K28.7‐|
|13|K28.7‐|ERR|ERR||K28.7‐|
|14|K28.7‐|K28.5‐|K28.5‐||K28.7‐|
|15|K28.7‐|K28.5+|K28.5+||K28.7‐|
|16|K28.5‐|D|K28.5‐||K28.5‐|



编码的错误状态字节包含 ERR [6:0] 中的接收器错误计数，该计数报告自断言 Pattern Lock 以来看到的错误数。"Pattern Lock" 指示器是 ERR 位 [7]，显示接收器何时已锁定到传入的修改合规模式。该模式的延迟序列也不同，现在在序列开头添加四个连续的 K28.5 符号（在表中显示为"D"），在 8 符号模式末尾添加四个 K28.7 符号，使发送到下一个 Lane 之前的总符号数为 16。该模式在第 532 页的表 14‐6 中示出。可以看出延迟模式在 16 个符号后移至 Lane 1。和以前一样，基本模式（现在为 8 个符号）以灰色突出显示。

**128b/130b 的修改合规模式。** 此模式由 65792 个块的重复序列组成，如下所列：

1. 一个 EIEOS 块

2. 256 个数据块，每个块包含 16 个加扰 IDL 符号 (00h)。

**533**

**PCI Express Technology**

3. 255 组以下序列：

   - 一个 SOS

   - 256 个数据块，每个块包含 16 个加扰 IDL 符号。

由于数据块中的有效负载全为零，因此输出最终只是该 Lane 的加扰器的输出。回想一下，加扰器不会随同步头位推进，并且由 EIEOS 初始化。由于加扰种子值取决于 Lane 编号，因此正确理解它们很重要。如果链路训练较早完成但随后软件通过设置 Link Control 2 寄存器中的 Enter Compliance 位将 LTSSM 发送到此子状态，则使用训练期间分配的 Lane 编号和极性反转。如果 Lane 在训练期间未处于活动状态，或者以任何其他方式进入此子状态，则 Lane 编号将是端口分配的默认编号。最后，请注意此模式中的数据块不形成数据流，不必遵循该要求（例如发送任何 SDS 有序集或 EDS 标记）。

细心的读者可能想知道在此序列中缺少错误状态符号，这些符号在 8b/10b 序列中很突出。事实证明，对于 128b/130b，它们现在包含在 SOS 中。回想一下，SOS 的最后 2 个字节用于在 Polling.Compliance 期间报告接收器错误计数（有关详细信息，请参见第 426 页 "Ordered Set Example ‐ SOS"）。

## _进入 Polling.Compliance：_

与进入 Polling.Active 时的情况一样，Link Control 2 寄存器的 Transmit Margin 字段用于设置此子状态期间将生效的发送器电压范围。

数据速率和去加重级别按如下所述确定。由于这些设置的许多选择取决于 Link Control 2 寄存器字段，因此该寄存器在第 536 页的图 14‐11 中显示以供参考。

- 如果端口仅支持 2.5 GT/s，则这将是数据速率，去加重级别将为 ‐3.5dB。

- 否则，如果此子状态是因为接收到 8 个连续的 TS1 而进入的，其中 Compliance Receive 位设置为 1b 且 Loopback 位清零为 0b（TS1 符号 5 的位 4 和 2），则速率将是任何 Lane 的最高公共值。select_deemphasis 变量必须设置为与 TS1 符号 4 中的 Selectable De‐emphasis 位匹配。如果选择的速率是 8.0 GT/s，则每个 Lane 的 select_preset 变量取自

**534**

**第 14 章：链路初始化与训练**

连续 TS1 的符号 6。对于此 Gen3 速率，未接收到 8 个具有发送器预设信息的连续 TS1 的 Lane 可以选择它们支持的任何值。

- 否则，如果在 Link Control 2 寄存器中设置了 Enter Compliance 位，则合规模式以 Target Link Speed 字段给出的数据速率发送。如果速率为 5.0 GT/s，则如果 Compliance Preset/De‐emphasis 字段等于 0001b，则设置 select_deemphasis 变量。如果速率为 8.0 GT/s，则每个 Lane 的 select_preset 变量清零为 0b，并且发送器必须使用 Compliance Preset/De‐emphasis 值，只要它不是保留编码。

- 最后，如果其他情况都不成立，则数据速率、预设和去加重设置将根据组件支持的最大速度和以这种方式进入 Polling.Compliance 的次数循环遍历一个序列。该序列在第 535 页的表 14‐7 中给出，并以第一次进入 Polling.Compliance 时的设置编号 1 开始，每次重新进入时通过列表递增，如果重新进入超过 14 次，则最终重复该模式。这提供了一种方便的方法来测试组件所有支持的设置：转换到 Polling.Compliance，测试该设置，转换回 Polling.Active，然后再次返回 Polling.Compliance 以测试下一个设置。规范中描述了负载板引起这些转换的方法，包括在接收器差分对的一条腿上发送约 1ms 的 100MHz，350mVp‐p 信号。

_表 14‐7：合规 Tx 设置序列_

|设置<br>编号|数据<br>速率|去加重|Tx 预设<br>编码|
|---|---|---|---|
|1|2.5|‐3.5|n/a|
|2|5.0|‐3.5|n/a|
|3|5.0|‐6.0|n/a|
|4|8.0|n/a|0000b|
|5|8.0|n/a|0001b|
|6|8.0|n/a|0010b|
|7|8.0|n/a|0011b|
|8|8.0|n/a|0100b|



**535**

## **PCI Express Technology**

_表 14‐7：合规 Tx 设置序列（续）_

|设置<br>编号|数据<br>速率|去加重|Tx 预设<br>编码|
|---|---|---|---|
|9|8.0|n/a|0101b|
|10|8.0|n/a|0110b|
|11|8.0|n/a|0111b|
|12|8.0|n/a|1000b|
|13|8.0|n/a|1001b|
|14|8.0|n/a|1010b|



_图 14‐11：Link Control 2 寄存器_

**==> picture [316 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 寄存器<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


如果数据速率不是 2.5 GT/s，那么：

- 如果在 Polling.Active 期间发送了任何 TS1，则发送器必须在进入电气空闲之前发送一个或两个连续的 EIOS。

- 如果在 Polling.Active 期间未发送任何 TS1，则发送器在不发送任何 EIOS 的情况下进入电气空闲。

- 电气空闲周期必须 > 1ms 且 < 2ms。在此期间，数据速率更改为新速度并稳定。如果速率为 5.0 GT/s，则去加重级别由 select_deemphasis 变量给出

**536**

**第 14 章：链路初始化与训练**

(0b = ‐3.5dB, 1b = ‐6.0 dB)。如果速率为 8.0 GT/s，则 select_preset 变量给出发送器要使用的预设。

## _在 Polling.Compliance 期间：_

一旦确定了数据速率和去加重或预设值，将应用以下规则：

**合规模式。** 如果进入不是因为在 TS 有序集中设置了 Compliance Receive 位并清除了 Loopback 位，并且不是因为 Link Control 2 寄存器中的 Enter Compliance 和 Enter Modified Compliance 位都被设置，则发送器在所有检测到的 Lane 上发送合规模式。

## _退出到 "Polling.Active"_

如果满足以下任何条件：

- a) 在任何检测到的 Lane 的接收器处检测到电气空闲退出，并且 Enter Compliance 位清零 (0b)。