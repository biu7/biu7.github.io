Title: [读书笔记]Redis实战-排序、事务和键的过期时间
Date: 2018-01-13
Category: 杂项
Slug: redis_others
Authors: qi
Summary: Redis 排序、事务和键的过期时间


之前介绍了 Redis 的多种数据结构和 Redis 的发布订阅，下面介绍一些其他的命令

#### 排序
Redis 的排序类似 SQL 中的 order by ，可以根据某种比较规则对一系列元素进行有序的排列。

命令如下：

| 命令 | 用例和描述 | 
| ---- | ---- |
| SORT | SORT source-key [BY PATTERN] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC / DESC] [ALPHA] [STORE dest-key]    根据给定的选项，对输入的列表、集合、有序集合进行排序，然后返回或储存排序的结果 |

使用 SORT 命令提供的选项，可以根据降序或者默认的升序来排序；可以将元素看作数字来排序；可以将元素看作二进制字符串来排序；可以使用被排序元素之外的其他值作为权重来排序；甚至可以从输入的列表、集合、有序集合之外的其他地方进行取值。

代码示例如下(Python 3.6)：

    >>> conn.rpush('sort-input', 23, 15, 110, 7)
    4
    >>> conn.sort('sort-input')        # 根据数字大小排序
    [b'7', b'15', b'23', b'110']
    >>> conn.sort('sort-input', alpha=True)        # 根据字母表顺序排序
    [b'110', b'15', b'23', b'7']
    >>> conn.hset('d-7', 'field', 5)
    1
    >>> conn.hset('d-15', 'field', 1)
    1
    >>> conn.hset('d-23', 'field', 9)
    1
    >>> conn.hset('d-110', 'field', 3)
    1
    >>> conn.sort('sort-input', by='d-*->field')        # 将散列的域用作权重，对 sort-input 列表进行排序
    [b'15', b'110', b'7', b'23']
    >>> conn.sort('sort-input', by='d-*->field', get='d-*->field')        # 获取外部数据，并将它们用作命令的返回值，而不是返回被排序的数据
    [b'1', b'3', b'5', b'9']
    
#### 事务
Redis 有 5 个可以让用户在不被打断的情况下对多个键执行操作，分别是 WATCH 、MULTI 、EXEC 、UBWATCH 、DISCARD 。

Redis 的基本事务需要用到 MULTI 命令和 EXEC 命令，这种事务可以让一个客户端在不被其他客户端打断的情况下执行多个命令。与关系数据库的事务不同，Redis 中被 MULTI 和 EXEC 命令包围的所有命令会一个接一个的执行，直到所有命令执行完毕。当一个事务执行完毕之后，Redis 才会处理其他客户端的命令。

在 Python 的 Redis 客户端中， Redis 事务是由 pipeline 实现的：对连接对象使用 pipeline() 方法将创建一个事务，在正常情况下，客户端会自动使用 MULTI 和 EXEC 包裹起用户输入的多个命令，在事务执行时一次性将所有命令都发送给 Redis 。


未使用事务的代码如下：
    
    >>> def nonrans():
    ...     print(conn.incr('notrans:'))    # 对 notrans: 执行自增操作
    ...     time.sleep(.1)
    ...     conn.incr('nontrans:', -1)        # 对 notrans: 执行自增操作
    
    >>> if 1:
    ...     for i in range(3):
    ...         threading.Thread(target=nonrans).start()
    ...     time.sleep(.5)
    1    # 由于没有使用事务，所以三个线程执行的多个命令互相交错，使得计数器的值持续增大
    2
    3

使用事务的代码示例：

    >>> def trans():
    ...     pipeline = conn.pipeline()
    ...     pipeline.incr('trans:')
    ...     time.sleep(.1)
    ...     pipeline.incr('trans:', -1)
    ...     print(pipeline.execute()[0])
    
    >>>  if 1:
    ...     for i in range(3):
    ...         threading.Thread(target=trans).start()
    ...     time.sleep(.5)
    1
    1
    1

可以看到，使用事务时，各线程都可以在不被其他线程打乱的情况下执行各自队列中的命令。

#### 键的过期时间

使用 Redis 存储数据的时候，有些数据可能在某个时间点之后就不用了，虽然我们可以使用 DEL 命令手动去删除无用数据，但是使用 Redis 提供的键过期操作是更好的选择。设置了过期时间的键会在这个键的过期时间到达的时候自动删除该键。

Redis 提供的用于设置过期时间的命令如下：

| 命令 | 示例和描述 |
| ---- | ---- |
| PERSIST | PERSIST key-name 移除键的过期时间 |
| TTL | TTL key-name 查看键距离过期还有多少秒 |
| EXPIRE | EXPIRE key-name seconds 让给定键在 seconds 秒后过期 |
| EXPIREAT | EXPIREAT key-name timestamp 将给定键的过期时间设置为给定的 UNIX 时间戳 |
| PTTL | PTTL key-name 查看给定键距离过期时间还有多少毫秒，Redis 2.6 及以上版本可用 |
| PEXPIRE | PEXPIRE key-name milliseconds 让给定键在指定的毫秒之后过期，Redis 2.6 及以上版本可用 |
| PEXPIREAT | PEXPIREAT key-name timestamp-milliseconds 将一个毫秒级精度的 UNIX 时间戳设置为指定键的过期时间，Redis 2.6 及以上版本可用 |

使用示例：

    >>> conn.set('key', 'value')
    True
    >>> conn.get('key')
    b'value'
    >>> conn.expire('key', 2)
    True
    >>> time.sleep(2)
    >>> conn.get('key')



