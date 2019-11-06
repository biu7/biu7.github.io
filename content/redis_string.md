Title: [读书笔记]Redis实战-字符串
Date: 2017-12-24
Category: 杂项
Slug: redis_string
Authors: qi
Summary: Redis 字符串



#### 简介
之前说过，redis中的 String 可以存储三种类型的值：字符串、整数、浮点数。对于整数和浮点数，用户可以对它们执行自增或自减操作。

整数的取值范围和系统的长整数取值范围相同（在32位系统上，整数为32位有符号整数，在64位系统上，整数为64位有符号整数），浮点数的取值范围和精度与IEEE 754标准的双精度浮点数相同。

#### 命令
下表展示 redis 中的自增自减命令：

| 命令 | 用例和描述 |
| ---- | ---- |
| INCR | INCR key-name 将键存储的值加上1 |
| DECR | DECR key-name 将键存储的值减去1 |
| INCRBY | INCRBY key-name amount 将键存储的值加上整数amount |
| DECRBY | DECRBY key-name amount 将键存储的值减去整数amount |
| INCRBYFLOUT | INCRBYFLOAT key-name amount 将键存储的值加上浮点数amount，这个命令仅在 Redis 2.6 及以上版本可用 |

当一个值存储到 Redis 字符串中，Redis会检查这个值是否可以被解释为十进制数或浮点数，以允许用户对这个字符串进行自增或自减操作。如果对不存在的键或空字符串进行自增自减操作，Redis 会将这个键的值作为 0 处理，如果对无法解释成整数或浮点数的字符串进行自增自减，Redis 将返回一个错误。

代码实例(Python 3.6)：

    >>> import redis
    >>> conn = redis.Redis()
    >>> conn.get('key')        # 获取一个值，如果值不存在，终端不会显示
    >>> conn.incr('key')    # 我们可以对不存在的键进行自增操作
    1
    >>> conn.incr('key', 10)    # python的incr操作其实是封装了 Redis 的incrby操作，不指定自增值时默认自增 1 
    11
    >>> conn.decr('key', 5)
    6
    >>> conn.get('key')
    b'6'
除自增自减操作之外，Redis 还拥有对字节串的其中一部分内容进行读取或者写入的操作，下表展示用来处理字符串子串和二进制位的命令：

| 命令 | 用例和描述 |
| ---- | ---- |
| APPEND | APPEND key-name value 将value值追加到给定键的值的末尾 |
| GETRANGE | GETRANGE key-name start end 获取一个由偏移量 start 至 end 范围内所有字符组成的子串，包含 start 和 end 在内 |
| SETRANGE | SETRANGE key-name offset value 将从偏移量 start 开始的子串设置为给定值 |
| GETBIT | GETBIT key-name offset 将字节串看作二进制位串，并返回位串中偏移量为 offset 的二进制位的值 |
| SETBIT | SETBIT key-name offset value 将字节串看作二进制位串，并将位串中偏移量为 offset 的二进制位的值设置为 value |
| BITCOUNT | BITCOUNT key-name [start end] 统计二进制位串中值为 1 的二进制位的数量，如果给定可选的 start 偏移量和 end 偏移量，则只对偏移量范围内的二进制位进行统计 |
| BITOP | BITOP operation dest-key key-name [key-name ...] 对一个或多个二进制串执行包括并(AND)、或(OR)、异或(XOR)、非(NOT)在内的任意一种按位运算操作，并将计算结果保存在 dest-key 键内 |

在使用 SETRANGE 或 SETBIT 操作时，如果字符串长度不能满足操作要求，Redis 会自动使用空字节来将字符串扩展到所需的长度，然后再进行操作。而在使用 GETBIT 操作的时候，超出字符串末尾的二进制位会被视为 0 。

代码实例(Python 3.6)：

    >>> conn.append('new-key', 'hello ')
    6
    >>> conn.append('new-key', 'world!')
    12
    >>> conn.getrange('new-key', 3, 7)
    b'lo wo'
    >>> conn.setrange('new-key', 0, 'H') # 从偏移为 0 的字符开始设置为 H ，由于 H 只有一个字符，因此只替换偏移为 0 处的字符
    12
    >>> conn.get('new-key')
    b'Hello world!'
    >>> conn.setbit('another-key', 2, 1)
    0
    >>> conn.setbit('another-key', 7, 1)
    0
    >>> conn.get('another-key')
    b'!'

