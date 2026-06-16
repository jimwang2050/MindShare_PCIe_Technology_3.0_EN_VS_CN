端点和根端口都可选地允许充当 AtomicOp 请求者和完成者，这可能看起来出乎意料，因为至少在 PC 中，这种事务通常仅由中央处理器发起。但是现代系统可以包括充当协处理器的端点，在这种情况下，它需要能够使用 AtomicOps 来正确处理协议。所有三个命令都支持 32 位和 64 位操作数，而 CAS 还支持 128 位操作数。实际使用的大小将在头部的 Length 字段中给出。具有对等访问功能的路由元素（如交换机端口和根端口）将需要支持 AtomicOp 路由功能，以便能够识别和路由这些请求。

很自然地会出现一个问题，即如何指示系统（根复合体）将生成这些新命令以响应处理器活动，因为可能没有直接类似的处理器总线命令。规范建议了两种方法。首先，根可以被设计为识别特定的处理器活动，并将其解释为响应"导出" PCIe AtomicOp。其次，可以使用类似于传统配置访问所使用的方法的基于寄存器的方法。在这种情况下，一个寄存器可以给出目标地址，而另一个寄存器指定应生成的命令，两者的组合将生成请求。

可以通过 Device Capabilities 2 寄存器中三个新位的存在来识别 AtomicOp 完成者，如图 20-10（在第 899 页）所示。该寄存器的第 6 位还标识路由元素是否能够路由 AtomicOp。

**898**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

传统 PCI 当然不理解 AtomicOps，并且没有直接的方法将它们转换为 PCI 命令。因此，PCIe-to-PCI 桥不支持 AtomicOps。如果在该总线上需要原子访问，则必须使用传统的锁定协议来完成，并且规范声明 Locked Transactions 和 AtomicOps 可以在同一平台上同时运行。

_图 20-10：Device Capabilities 2 寄存器_

**==> 图片 [356 x 280] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 24 23 22 21 20 19 14 13 12 11 10 9 8 7 6 5 4 3 0<br>RsvdP RsvdP<br>Max End-End<br>TLP Prefixes<br>End-End TLP<br>Prefix Supported<br>Extended Fmt<br>Field Supported<br>TPH Completer Supported<br>LTR Mechanism Supported<br>No RO-enabled PR-PR Passing<br>128-bit CAS Completer Supported<br>64-bit AtomicOp Completer Supported<br>32-bit AtomicOp Completer Supported<br>AtomicOp Routing Supported<br>ARI Forwarding Supported<br>Completion Timeout Disable Supported<br>Completion Timeout Ranges Supported<br>**----- 图片文字结束 -----**


## **TPH (TLP 处理提示)**

添加有关系统应如何处理目标为内存空间的 TLP 的提示可以改善延迟和流量拥塞。规范将此特殊处理基本上描述为提供关于系统中多个可能的缓存位置中的哪一个是 TLP 临时副本的最佳位置的信息。

**899**

**PCI Ex ress Technolo p gy**

规范指出，由于为 TPH 描述的使用与缓存相关，因此通常使用目标为不可预取内存空间 (Non-prefetchable Memory Space) 的 TLP 是不合理的。如果需要这样的使用，则必须以某种方式保证缓存此类 TLP 不会引起不良副作用。

## **TPH 示例**

**设备写入到主机读取**。为了帮助阐明 TPH 的动机，考虑第 901 页的图 20-11 所示的示例。这里端点正在将数据写入内存以供 CPU 稍后使用。序列如下：

1. 首先，端点发送一个内存写入 TLP，其中包含映射到系统内存的地址。数据包被路由到根复合体 (RC)。

2. RC 将此识别为对可缓存内存空间的访问，并在其窥探 CPU 缓存时暂停其进度。这可能导致从 CPU 的回写周期以在事务可以继续之前更新系统内存，这显示为步骤 2a。

3. 一旦任何回写完成，RC 允许写入更新系统内存。

4. 在某个时刻，端点通知 CPU 数据已传送。

5. 最后，CPU 从内存中获取数据以完成序列。

**900**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-11：TPH 示例_

**==> 图片 [202 x 111] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
4<br>2<br>e C)\ @ 5<br>2a<br>Roo! Complex @<br>3<br>1<br>lo [ |<br>**----- 图片文字结束 -----**


此序列有效，但通过在系统中添加中间缓存有改进性能的机会。为了说明这一点，考虑第 902 页的图 20-12 中所示的示例。从端点的角度来看，操作是相同的，但知道以不同方式处理它。现在的步骤如下：

1. 端点执行相同的内存写入，但这次包括 TPH 位。写入像以前一样通过交换机转发到 RC。

2. RC 理解此内存访问必须像以前一样窥探到 CPU。但是，一旦窥探处理完毕，RC 由 TPH 位通知将此 TLP 存储在中间缓存中，而不是转到系统内存。

3. 端点通知 CPU 数据项已传送。

4. CPU 从指定地址读取，但现在数据在中间缓存中找到，因此请求不会转到系统内存。这具有我们期望从缓存设计中获得的通常好处：更快的访问时间以及减少系统内存的流量。

**901**

**PCI Ex ress Technolo p gy**

这是一个简单的设备写入到主机读取 (DWHR) 示例，用于说明概念，但不难想象一个更复杂的系统，具有更大的拓扑，其中可以在交换机或其他位置放置其他缓存，以实现其他目标的相同好处。

_图 20-12：带系统缓存的 TPH 示例_

**==> 图片 [108 x 75] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
3<br>2 4<br>OC @VlEl@<br>Rant Camnlayx<br>Cache<br>1<br>**----- 图片文字结束 -----**


**主机写入到设备读取**。为了说明相反方向的概念（称为主机写入到设备读取 (HWDR)），考虑第 903 页的图 20-13 中所示的示例。在此示例中，CPU 在第一步中启动一个内存写入，其地址针对 PCIe 端点。该数据包包含 TPH 位，告诉 RC 应将其存储在目标附近的中间缓存中，而不是上例中使用的 RC 中的缓存。在这种情况下，内置于交换机中的缓存用于此目的。然后在第二步中将 TLP 转发到目标端点。当数据不经常更新但经常被端点读取时，此模型是有益的。这允许通常会转到系统内存的多个内存读取由缓存处理，从而减轻从交换机到 RC 的链路以及到内存的路径的负载。

**902**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-13：用于目标为端点的 TLP 的 TPH 使用_

**==> 图片 [353 x 326] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
1<br>ox<br>oct Complex<br>Cache<br>rl i) i<br>PCle PCle<br>Cache<br>2<br>OWN: Endpoint Bridge<br>Yi i IN orto PCI-X PCI<br>§ EndpointPCle §§ EndpointLegacy PCI/PCI-X | |<br>Device to Device.  One last example is illustrated in Figure 20‐14 on page<br>904, where two Endpoints communicate with each other (called Device Read/<br>Write to Device Read/Write or D*D*) through a shared memory location that is<br>directed by TPH bits to an intermediate cache. In this case, both may update dif‐<br>ferent locations that they need to handle as "read mostly", or one Endpoint may<br>update data that the other needs to read several times. In both cases, using the<br>intermediate cache improves system performance.<br>**----- 图片文字结束 -----**


**903**

## **PCI Ex ress Technolo p gy**

_图 20-14：端点之间的 TPH 使用_

**==> 图片 [34 x 9] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Cache<br>**----- 图片文字结束 -----**


## **TPH 头位**

TLP 头中的几位描述了如何使用提示。首先，如图 20-15（在第 905 页）顶部中间所示，TH（TLP 提示）位报告可选的 TPH 位是否正在用于 TLP。设置后，PH（处理提示位）指示下一级信息。

**904**

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-15：TPH 头位_

**==> 图片 [339 x 115] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- 图片文字结束 -----**


当 TH 位置位时，PH 位（如图 20-15（在第 905 页）右下角所示）取代地址字段中原本保留的两个 LSB。对于 32 位地址，这些是字节 11 [1:0]，而对于所示的 64 位地址，它们是字节 15 [1:0]。其编码在第 905 页的表 20-1 中描述。这些提示由请求者根据对使用中的数据模式的了解来提供，而完成者自己很难推断出这些信息。

_表 20-1：PH 编码表_

|**PH [1:0]**|**处理提示**|**使用模型**|
|---|---|---|
|00b|双向数据结构|指示主机和设备的频繁读/写访问。|
|01b|请求者|D*D*（设备到设备传输）。指示设备的频繁读/写访问。星号表示任一设备都可以读取或写入。|
|10b|目标|DWHR，HWDR（设备到主机或主机到设备的传输）。指示主机的频繁读/写访问。|
|11b|带优先级的目标|与目标相同，但具有额外的时间重用优先级信息。指示主机的频繁读/写访问以及所访问数据的高时间局部性。|


**905**

## **PCI Ex ress Technolo p gy**

下一级信息是 Steering Tag 字节，它提供关于系统中缓存此 TLP 的最佳位置的系统特定信息。有趣的是，此字节在头中的位置取决于请求类型。对于 Posted Memory Writes，Tag 字段被重新用作 Steering Tag（不会返回完成，因此不需要 Tag），而对于 Memory Reads，两个 Byte Enable 字段被重新用于它（可预取读取不需要字节启用）。位的含义是实现特定的，但它们需要唯一地标识系统中所需缓存的位置。

规范中描述了 TPH 的两种格式，此级别的提示信息（TH + PH + 8 位 Steering Tag），称为基线 TPH (Baseline TPH)，是第一种，并且是提供 TPH 的所有请求所必需的。第二种格式使用 TLP 前缀来扩展 Steering Tag（有关更多详细信息，请参阅第 908 页上的"TLP Prefixes"）。

## **Steering Tags**
