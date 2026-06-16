## **PCI Express 技术**

**消息写（Message Writes）。** 有趣的是，与我们迄今为止看到的其他请求不同，消息有几种可能的路由方法，并且消息中的一个字段指示应使用哪种类型。例如，有些消息是发布到特定 Completer 的 Posted 写请求，有些是从根复合体 (Root Complex) 广播到所有端点 (Endpoint) 的，而从端点 (Endpoint) 发送的其他消息则会自动路由到根复合体 (Root)。要了解更多关于不同路由类型的信息，请参阅第 121 页第 4 章"地址空间与事务路由"。

消息在 PCIe 中很有用，有助于实现降低引脚 (Pin) 数的设计目标。它们消除了对 PCI 曾经用于报告中断 (Interrupt)、电源管理事件 (Power Management Events) 和错误 (Error) 等内容的边带 (Sideband) 信号的需要，因为它们可以通过正常的数据路径以报文的形式报告这些信息。
