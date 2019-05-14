Title: python3爬虫-烂大街的新浪微博之移动版网页登录
Date: 2017-11-26 10:01
Modified: 2017-11-27 12:30
Category: 爬虫
Tags: python, 爬虫
Slug: 新浪微博
Authors: qi
Summary: 新浪微博的模拟登录已经要被大家写烂了，不过我倒是真的没有写过，为了博客不这么空荡荡的我还是得写一写的。。。


#### 前言
新浪微博的模拟登录已经要被大家写烂了，不过我倒是真的没有写过，为了博客不这么空荡荡的我还是得写一写的。。。
#### 抓包
微博的移动版页面登陆时比较简单的，我们抓包看一下,过滤掉js、css和图片请求之后：
![图片1](https://img.biubiu7.cn/sinaweibo/sina_wap_login_1.png)

很明显最后一个就是登录请求，post参数和返回信息如下图：
![图片2](https://img.biubiu7.cn/sinaweibo/sina_wap_login_2.png)
看上去没有加密，并且其他的参数看上去也都是一些固定参数，是一个比较简单的请求，我们直接来写代码。
#### 代码
由于模拟登录需要保持cookie，所以我们需要使用requests.Session类来保持回话。从charles（或者你使用的其他抓包工具）中复制出请求链接，初始化requests.Session对象然后进行请求，代码如下：

	from requests import Session
	s = Session()
	s.verify = False
    INIT_LOGIN_URL = 'https://passport.weibo.cn/signin/login?display=0&retcode=6102'
	LOGIN_URL = 'https://passport.weibo.cn/sso/login'
	username = input("请输入用户名：")
	password = input("请输入密码：")

	login_resp = s.post(
        url=LOGIN_URL,
        data={
            'username': username,
            'password': password,
            'savestate': '1',
            'r': '',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': INIT_LOGIN_URL
    	}
	)
    print(login_resp.text)

运行一下，看到输出：
![图片3](https://img.biubiu7.cn/sinaweibo/sina_wap_login_3.png)

看到没有输出错误信息，表示我们已经登录成功了。然后我们尝试获取一下登录后的个人信息，来确定我们登录成功。从抓包工具中拿到链接后放进代码中进行请求：

	if login_resp.json()['retcode'] == 20000000:
    	profile_resp = s.get(PROFILE_URL)
    	print(f'登录成功，微博昵称为{profile_resp.json()["data"]["user"]["screen_name"]}')
	else:
    	print(f'登陆失败，{login_resp.json()["msg"]}')
运行：

![图片4](https://img.biubiu7.cn/sinaweibo/sina_wap_login_4.png)

完美。微博的移动端模拟登录难度几乎为0，所以下一篇会写一下电脑网页版的登录。