Title: [读书笔记]Redis实战-列表
Date: 2017-12-24
Category: 杂项
Slug: redis_list
Authors: qi
Summary: Redis 列表


#### 简介
Redis 中的列表允许用户从序列的两端推入或弹出元素，获取列表元素、以及执行各种常见的列表操作，

#### 命令
下表展示 redis 中列表常用的命令：

| 命令 | 用例和描述 |
| ---- | ---- |
| RPUSH | RPUSH key-name value [value ...] 将一个或多个值推入列表的右端 |
| LPUSH | LPUSH key-name value [value ...] 将一个或多个值推入列表的左端 |
| RPOP | RPOP key-name 移除并返回列表最右端的元素 |
| LPOP | LPOP key-name 移除并返回列表最左端的元素 |
| LINDEX | LINDEX key-name offset 返回列表中偏移量为 offset 的元素 |
| LRANGE | LRANGE key-name start end 返回列表中从偏移量 start 到 偏移量 end 之间的所有元素，包含 start 和 end 在内 |
| LTRIM | LTRIM key-name start end 只保留列表中从偏移量 start 到 偏移量 end 之间的元素，包含 start 和 end 在内 |

代码示例(Python 3.6)：

    >>> conn.rpush('list-key', 'last') # 返回值为列表长度
    1
    >>> conn.lpush('list-key', 'first')
    2
    >>> conn.rpush('list-key', 'new last')
    3
    >>> conn.lrange('list-key', 0, -1)
    [b'first', b'last', b'new last']
    >>> conn.lpop('list-key')
    b'first'
    >>> conn.lpop('list-key')
    b'last'
    >>> conn.lrange('list-key', 0, -1)
    [b'new last']
    >>> conn.rpush('list-key', 'a', 'b', 'c')
    4
    >>> conn.lrange('list-key', 0, -1)
    [b'new last', b'a', b'b', b'c']
    >>> conn.ltrim('list-key', 2, -1)
    True
    >>> conn.lrange('list-key', 0, -1)
    [b'b', b'c']

除以上命令外，还有几个命令，可以将元素从一个列表移动到另一个列表，或者阻塞执行命令的客户端，直到有其他客户端给列表添加元素为止，如下表：

| 命令 | 用例和描述 |
| ---- | ---- |
| BLPOP | BLPOP key-name [key-name ...] timeout 从第一个非空列表弹出位于最左端的元素，或者在 timeout 秒内阻塞并等待可弹出元素出现 |
| BRPOP | BLPOP key-name [key-name ...] timeout 从第一个非空列表弹出位于最右端的元素，或者在 timeout 秒内阻塞并等待可弹出元素出现 |
| RPOPLPUSH | RPOPLPUSH source-key dest-key 从 source-key 列表中弹出最右端的元素，然后将其推入 dest-key 列表的最左端，并返回这个元素 |
| BRPOPLPUSH | BRPOPLPUSH source-key dest-key timeout 从 source-key 列表中弹出最右端的元素，然后将其推入 dest-key 列表的最左端，并返回这个元素；如果 source-key 为空，那么在 timeout 秒之内阻塞并等待可弹出的元素出现 |

代码示例(Python 3.6)：

    >>> conn.rpush('list', 'item1')
    1
    >>> conn.rpush('list', 'item2')
    2
    >>> conn.rpush('list2', 'item3')
    1
    >>> conn.brpoplpush('list2', 'list', 1)
    b'item3'
    >>> conn.brpoplpush('list2', 'list', 1)        # 由于 list2 为空，因此会阻塞一秒，并返回空
    >>> conn.lrange('list', 0, -1)
    [b'item3', b'item1', b'item2']
    >>> conn.blpop(['list2', 'list'], 1)    # BLPOP 命令会从左到右检查传入的列表，并对最先遇到的非空列表执行弹出
    (b'list', b'item3')

对于阻塞弹出命令和弹出并推入命令的使用，最常见的就是消息传递和消息队列，将在之后进行介绍。
