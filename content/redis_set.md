Title: [读书笔记]Redis实战-集合
Date: 2018-01-02
Category: 杂项
Slug: redis_set
Authors: qi
Summary: Redis 集合


#### 简介
Redis 中的集合以无序的方式来存储不同的元素，用户可以对集合执行添加元素、移除元素、检察元素是否存在等操作。

#### 命令
集合常用命令如下表：

| 命令 | 用例和描述 |
| ---- | ---- |
| SADD | SADD key-name item [item ...] 将一个或多个元素添加到集合，并返回被添加元素中原本不存在于集合中的元素数量 | 
| SREM | SREM key-name item [item ...] 从集合中移除一个或多个元素，并返回被移除元素的数量 | 
| SISMEMBER | SISMEMBER key-name item 检查元素是否存在于集合中 |
| SCARD | SCARD key-name 返回集合中的元素数量 |
| SMEMBERS | SMEMBERS key-name 返回集合中的所有元素 |
| SRANDMEMBER | SRANDMEMBER key-name [count] 从集合中随机返回一个或多个元素。当 count 为正数时，返回的元素不会重复，当 count 为负数时， 命令返回的随机元素可能会出现重复 |
| SPOP | SPOP key-name 随机的移除一个元素，并返回被移除的元素 |
| SMOVE | SMOVE source-key dest-key item 如果集合 source-key 中包含元素 item ，那么从 source-key 中移除 item ，并添加到集合 dest-key 中。如果 item 被成功移除，返回 1 ，否则返回 0 。 |

使用示例如下(Python 3.6)：

    >>> conn.sadd('set-key', 'a', 'b', 'c')
    3
    >>> conn.srem('set-key', 'c', 'd')
    1
    >>> conn.srem('set-key', 'c', 'd')
    0
    >>> conn.scard('set-key')
    2
    >>> conn.smembers('set-key')
    {b'a', b'b'}
    >>> conn.smove('set-key', 'set-key2', 'a')
    True
    >>> conn.smove('set-key', 'set-key2', 'c')
    False
    >>> conn.smembers('set-key')
    {b'b'}

以上是 Redis 集合的常用命令，但集合更厉害的在于组合和关联多个集合，相关命令如下：

| 命令 | 用例和描述 |
| ---- | ---- |
| SDIFF | SDIFF key-name [key-name ...] 返回存在于第一个集合，但不存在于其他集合的元素（数学上的差集运算）| 
| SDIFFSTORE | SDIFFSTORE dest-key key-name [key-name ...]  将存在于第一个集合但不存在于其他集合的元素存储到 dest-key 键中 | 
| SINTER | SINTER key-name [key-name ...] 返回同时存在于所有给定集合中的元素（数学中的交集运算） |
| SINTERSTORE | SINTERSTORE dest-key key-name [key-name ...] 将同时存在于所有给定集合的元素存储到 dest-key 键中 |
| SUNION | SUNION key-name [key-name ...] 返回至少存在于一个集合中的元素（数学中的并集运算） |
| SUNIONSTORE | SUNIONSTORE dest-key key-name [key-name ...] 降至少存在于一个集合中的元素存储到 dest-key 键中 |

使用示例如下(Python 3.6)：

    >>> conn.sadd('skey1', 'a','b','c','d')
    4
    >>> conn.sadd('skey2', 'c','d','e','f')
    4
    >>> conn.sdiff('skey1', 'skey2')
    {b'a', b'b'}
    >>> conn.sinter('skey1', 'skey2')
    {b'c', b'd'}
    >>> conn.sunion('skey1', 'skey2')
    {b'a', b'b', b'c', b'd', b'e', b'f'}

