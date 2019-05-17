Title: 使用 github webhook 和腾讯云云函数实现博客 cdn 自动刷新
Date: 2019-05-16 13:25
Category: 博客相关
Slug: cdn_refresh_webhook
Authors: qi
Summary: 使用 github 的 webhook 和腾讯云无服务器云函数实现博客更新后自动刷新 CDN 缓存

把博客迁移为静态博客之后，每次更新了文章或者配置，都要登录腾讯云控制台去手动刷新一下 cdn 缓存，次数多了实在受不了，想起来 github 是支持 webhook 的，而腾讯云也有 api 接口可以调用，很棒棒嘛。

找到腾讯云的 [cdn 文档](https://cloud.tencent.com/document/product/228/3947)中刷新目录的部分，可以看到需要以下参数：

参数 | 含义
---- | ---
Action | 具体操作的指令接口名称， 刷新 cdn 目录为 RefreshCdnDir
SecretId |  用户的云 API SecretId
Timestamp |  时间戳
Nonce |  随机正整数
Signature |  签名
dirs.0 |  要刷新的目录

以上参数中，**签名**需要计算得出，计算方法点[这里](https://cloud.tencent.com/document/api/228/1725)，简单来说，就是将以上除**签名**之外的几个参数拼接为字符串，然后以用户的 SecretKey 作为 key ，使用 hmac sha1 算法对拼接好的字符串进行签名，并做 base64 编码。

拼接字符串的格式如下：
	
    srcStr = f"POST{url}?Action={Action}&Nonce={Nonce}&SecretId={SecretId}&Timestamp={Timestamp}&dirs.0={dirs_0}"
    
**注意**：以上字符串务必保证正确顺序，不能颠倒。github 的 webhook 仅支持 POST 请求。

hmac-sha1 签名代码如下：

	import hmac
    import hashlib
    sig = base64.b64encode(hmac.new(SecretKey.encode(), srcStr.encode(), hashlib.sha1).digest()).decode()

ok，代码有了，我们打开[腾讯云无服务器云函数](https://console.cloud.tencent.com/scf/list?rid=4&ns=default)的页面，选择新建，选择模板函数，填入函数名称，选择** Python3.6 的API 网关返回 Web 页面**模板：
![图片1](https://img-1251994035.cos.ap-shanghai.myqcloud.com/blog/201905160001.png)

然后选择下一步，完成。
进入刚刚创建好的云函数中，选择函数代码选项，开始填入代码，完整代码如下：

	import time
	import random
	import requests
	import hashlib
	import hmac
	import base64

	def main_handler(event, context):
        url = "cdn.api.qcloud.com/v2/index.php"
        Action = "RefreshCdnDir"
        SecretId = "填入你的 SecretId "
        SecretKey = "填入你的 SecretKey "
        Timestamp = int(time.time())
        Nonce = random.randint(1, 10000000000)
        dirs_0 = "填入要刷新的地址"
        srcStr = f"POST{url}?Action={Action}&Nonce={Nonce}&SecretId={SecretId}&Timestamp={Timestamp}&dirs.0={dirs_0}"
        Signature = base64.b64encode(hmac.new(SecretKey.encode(), srcStr.encode(), hashlib.sha1).digest()).decode()
        resp = requests.post(
            url=f"https://{url}",
            data={
                "Action": Action,
                "SecretId": SecretId,
                "Timestamp": Timestamp,
                "Nonce": Nonce,
                "Signature": Signature,
                "dirs.0": dirs_0
            }
        )
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'text/html; charset=utf-8'},
            "body": resp.json()
        }

选择**保存并测试**，如果出现下图结果，表示提交 CDN 刷新任务成功：
![图片1](https://img.biubiu7.cn/blog/201905160002.png)
在返回结果中， statusCode 为云函数本身调用成功返回的结果，即上方代码 return 的结果。而 body 中的则是我们调用 CDN 刷新接口返回的结果。如果调用不成功，可以根据返回的 code 值和 codeDesc 来排查错误原因。

调用成功之后，选择右上角的发布新版本来发布你的代码。发布之后选择触发方式 -> 添加触发方式，选择 ** API网关触发器**，并新建一个 API 服务，请求方法选择 POST ，环境选择发布，然后保存，如下图：
![图片2](https://img.biubiu7.cn/blog/201905160003.png)

之后你会得到一个访问链接，使用 POST 方式访问这个链接就会触发云函数运行，继而向 CDN 刷新 API 发送请求：
![图片3](https://img.biubiu7.cn/blog/201905160004.png)

接下来去 github 中需要设置 webhook 的仓库，进入 Settings -> Webhooks -> Add webhook ，然后在 Payload URL
 中填入上一步获取到的 url ，其余选项根据需求选择即可，我是全部默认：
![图片4](https://img.biubiu7.cn/blog/201905160005.png)

接下来保存即可，可以尝试 push 一次，然后前往云函数和 CDN 控制台查看日志，确定是否调用成功。



**5月17日更新**

发现不管 push 到哪个分支都会触发 CDN 刷新，而 github 上并没有找到指定分支推送触发 webhook 的方法，那就只好在代码里做一次判断了。将以下代码添加到函数开头，重新发布即可：

    payload = json.loads(unquote(event["body"])[8:])
    if payload["ref"] != "refs/heads/master":
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {'Content-Type': 'text/html; charset=utf-8'},
            "body": "本次推送分支不是 master 分支，不作 CDN 刷新操作"
        }

