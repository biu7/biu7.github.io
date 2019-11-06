Title: [读书笔记]Redis实战-发布和订阅
Date: 2018-01-13
Category: 杂项
Slug: redis_publish
Authors: qi
Summary: Redis 发布和订阅


#### 简介
发布与订阅，类似电台与收听者的关系，订阅者负责收听频道，发布者负责向频道发送二进制字符串消息。当有消息发送给指定频道时，该频道的所有订阅者都会收到消息。

#### 命令
以下是 Redis 提供的发布和订阅相关命令：

| 命令 | 用例和描述 |
| ---- | ---- |
| SUBSCRIBE | SUBSCRIBE channel [channel ...] 订阅给定的一个或多个频道 |
| UNSUBSCRIBE | UBSUBSCRIBE [channel [channel ...]] 退订给定的一个或多个频道，如果没有给定任何频道，则退订所有频道 | 
| PUBLISH | PUBLISH channel message 向给定频道发送消息 | 
| PSUBSCRIBE | PSUBSCRIBE pattern [pattern ...] 订阅与给定模式相匹配的所有频道 |

使用辅助线程执行 PUBLISH 命令示例：
    
    >>> def publisher(n):
    ...     time.sleep(1)
    ...     for i in range(n):
    ...         conn.publish('channel', i)
    ...         time.sleep(1)
            
    >>> def run_pubsub():
    ...     threading.Thread(target=publisher, args=(3, )).start()
    ...     pubsub = conn.pubsub()
    ...     pubsub.subscribe(['channel'])
    ...     count = 0
    ...     for item in pubsub.listen():
    ...         print(item)
    ...         count += 1
    ...         if count == 4:
    ...             pubsub.unsubscribe()
    ...         if count == 5:
    ...             break;
    
    >>> run_pubsub()
    {'type': 'subscribe', 'pattern': None, 'channel': b'channel', 'data': 1} # 刚订阅一个频道的时候，客户端会受到一条反馈
    {'type': 'message', 'pattern': None, 'channel': b'channel', 'data': b'0'}
    {'type': 'message', 'pattern': None, 'channel': b'channel', 'data': b'1'}
    {'type': 'message', 'pattern': None, 'channel': b'channel', 'data': b'2'}
    {'type': 'unsubscribe', 'pattern': None, 'channel': b'channel', 'data': 0} # 退订频道的时候，会受到一条反馈，告知退订的频道名，和目前订阅的频道数量

书中仅在这一节和 8.5 节使用了发布和订阅模式，原因如下：

一方面是由于旧版 Redis 的稳定性问题，如果一个客户端订阅了某个或某些频道，但它读取消息的速度不够快的话，不断积压的消息会使得 Redis 输出缓冲区的体积越来越大，这可能会导致 Redis 的速度变慢，甚至崩溃，也有可能导致 Redis 进程被操作系统强制杀死，甚至导致操作系统本身不可用。新版本的 Redis 通过 client-output-buffer-limit pubsub 选项来限制为每个客户端分配的最大输出缓冲区大小，如果为某个客户端分配的缓冲区大小超过了这个配置， Redis 可能会根据策略关闭这个客户端的连接。

另一方面是由于如果客户端在执行订阅操作的过程中断线，客户端会丢失断线期间发送的所有消息。

因此书中在第 6 章重新实现了两个不同的方法来实现可靠的消息传递，之后将进行介绍。如果能够承担可能丢失小部分数据的风险，继续使用发布和订阅功能也可以。
