## **事务层 (Transaction Layer)** 

响应来自软件层的请求，事务层生成出站报文（outbound packets）。它还会检查入站报文（inbound packets），并将其所含信息向上传递给软件层。它支持用于 Non-Posted 事务的分离事务协议（split transaction protocol），并将入站的完成报文（Completion）与先前发出的出站 Non-Posted 请求（Request）相关联。该层所处理的事务使用 TLP（事务层包，Transaction Layer Packets），可分为以下四种请求类别：

1. Memory（内存）

2. IO（输入/输出）

3. Configuration（配置）

4. Messages（消息）

前三种类型在 PCI 和 PCI‐X 中就已支持，但消息是 PCIe 新增的类型。一个**事务 (Transaction)** 被定义为：由一个将命令传送到目标设备的**请求 (Request)** 报文，加上目标设备作为响应发回的任何**完成报文 (Completion)** 所共同组成。请求类型的列表见表 2‐2（第 59 页）。

_表 2‐2：PCI Express 请求类型 (Request Types)_ 

|**请求类型**|**Non-Posted 或 Posted**|
|---|---|
|Memory Read（内存读）|Non-Posted|
|Memory Write（内存写）|Posted|
|Memory Read Lock（内存读锁定）|Non-Posted|

**59**
