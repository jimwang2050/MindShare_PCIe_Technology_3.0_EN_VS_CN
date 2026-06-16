## **PCI Express 技术**

_表 2‐2：PCI Express 请求类型（续）_

|**请求类型**|**Non‐Posted 或 Posted**|
|---|---|
|IO 读 (IO Read)|Non‐Posted|
|IO 写 (IO Write)|Non‐Posted|
|配置读 (Configuration Read)（Type 0 和 Type 1）|Non‐Posted|
|配置写 (Configuration Write)（Type 0 和 Type 1）|Non‐Posted|
|消息 (Message)|Posted|

如表中右列所示，这些请求还可以分为两类：**non‐posted**（非发布）和 **posted**（发布）。对于 non‐posted 请求，请求者 (Requester) 发送一个数据包，被请求端 (Completer) 应以完成报文 (Completion) 数据包的形式作出响应。读者可能会注意到，这是从 PCI‐X 继承而来的分离事务协议 (split transaction protocol)。例如，任何读请求都是 non‐posted 的，因为所请求的数据需要在完成报文中返回。出乎意料的是，IO 写和配置写也是 non‐posted 的。尽管它们正在为命令传送数据，这些请求仍然期望从目标设备接收一个完成报文，以确认写数据实际上已经无误地到达目的地。

相比之下，内存写 (Memory Write) 和消息 (Message) 是 posted 的，意味着目标设备不会向请求者返回完成报文 (Completion) TLP。Posted 事务提高了性能，因为请求者不必等待回复，也无需承担完成报文的开销。其代价是它们无法获得关于写操作是否已完成或是否遇到错误的反馈。这种行为是从 PCI 继承而来的，并且仍被认为是一种良好的做法，因为发生故障的可能性很小，而性能提升却很显著。需要注意的是，即使 posted 写不需要完成报文，它们仍然会参与数据链路层 (Data Link Layer) 中的 Ack/Nak 协议，以确保数据包可靠传输。有关这方面的更多内容，请参阅第 317 页第 10 章"ʺAck/Nak 协议ʺ"。
