Title: [读书笔记]Redis实战-散列
Date: 2018-01-06
Category: 杂项
Slug: redis_hash
Authors: qi
Summary: Redis 散列


#### 简介
Redis 中的散列可以让用户将多个键值对存储到一个 Redis 键中，从功能上来讲，散列非常适合将一些相关数据存储在一起。

#### 命令
散列常用命令如下表：

| 命令 | 用例和描述 |
| ---- | ---- |
| HMGET | HMGET key-name key [key ...] 从散列中获取一个或多个键的值 | 
| HMSET | HMSET key-name key value [key value ...] 为散列中的一个或多个键设置值 |
| HDEL | HDEL key-name key [key ...] 删除散列中的一个或多个键值对，返回成功删除的键值对的数量 |
| HLEN | HLEN key-name 返回散列中的键值对数量 |

使用示例如下(Python 3.6)：

    >>> conn.hmset('hash-key', {'k1': 'v1', 'k2': 'v1', 'k3': 'v3'})
    True
    >>> conn.hmget('hash-key', ['k2', 'k3'])
    [b'v1', b'v3']
    >>> conn.hlen('hash-key')
    3
    >>> conn.hdel('hash-key', 'k1', 'k3')
    2

之前介绍的 HGET、HSET 命令分别是 HMGET、HMSET 的单参数版本。
下表是散列的其他几个批量操作命令，和一些与字符串操作类似的散列命令：

| 命令 | 用例和描述 |
| ---- | ---- |
| HEXISTS | HEXISTS key-name key 检查给定键是否存在于散列中 | 
| HKEYS | HKEYS key-name 获取散列中的所有键 | 
| HVALS | HVALS key-name 获取散列中的所有值 | 
| HGETALL | HGETALL key-name 获取散列中的所有键值对 | 
| HINCRBY | HINCRBY key-name key increment 将键 key 存储的值加上整数 increment | 
| HINCRBYFLOAT | HINCRBYFLOAT key-name key increment 将键 key 存储的值加上浮点数 increment | 

使用示例如下(Python 3.6)：

    >>> conn.hmset('hash-key2', {'short': 'hello', 'long': 1000 * '1'})
    True
    >>> conn.hkeys('hash-key2')
    [b'short', b'long']
    >>> conn.hexists('hash-key2', 'num')
    False
    >>> conn.hincrby('hash-key2', 'num')
    1
    >>> conn.hexists('hash-key2', 'num')
    True


