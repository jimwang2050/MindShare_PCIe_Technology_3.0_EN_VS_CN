## **Non-Posted Transactions（非 Posted 事务）**

**Ordinary Reads（普通读）。** 第 65 页的图 2-18 展示了一个从端点 (Endpoint) 发往系统内存的 Memory Read Request（内存读请求）示例。关于 TLP 内容的详细讨论可参见第 169 页第 5 章 ʺTLP Elements（TLP 元素）ʺ，但任何内存读请求的一个重要部分是目标地址。内存 Request（请求）的地址可以是 32 位或 64 位，并由此决定报文路由。在本例中，请求通过两个交换机 (Switch) 转发到目标（本例中即 Root）。当 Root 解码该请求并识别到报文中的地址指向系统内存时，它会取回所请求的数据。为了将这些数据返回给 Requester（请求者），Root Port（根端口）的 Transaction Layer（事务层）会按需生成尽可能多的 Completion（完成报文）以将所有请求数据传送到 Requester（请求者）。PCIe 单个报文最大数据载荷为 4 KB，但设备通常被设计为使用更小的载荷，因此可能需要多个 Completion（完成报文）才能返回大量数据。

_Figure 2‐18: Non‐Posted Read Example（图 2-18：非 Posted 读示例）_

**==> picture [326 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Completer（完成者）<br>Processor（处理器）<br>Step 2: Root 接收 MRd（步骤 2：Root 收到 MRd）<br>Step 3: Root 取回数据，<br>返回 CplD（步骤 3：Root 取回数据并返回 CplD）<br>Root Complex（根复合体）<br>CplD MRd System<br>Memory（系统内存）<br>Switch A（交换机 A） Switch C（交换机 C）<br>CplD<br>MRd<br>Switch B（交换机 B） Endpoint（端点） Endpoint（端点） Endpoint（端点）<br>MRd<br>CplD<br>Requester（请求者）<br>Endpoint（端点） Endpoint（端点） Step 1: Endpoint 发起 MRd（步骤 1：Endpoint 发起 MRd）<br>Step 4: Endpoint 接收 CplD（步骤 4：Endpoint 收到 CplD）<br>
**----- End of picture text -----**<br>

**65**
