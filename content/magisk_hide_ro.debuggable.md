Title: Magisk 导致 ro.debuggable 修改无效的排查处理
Date: 2018-07-14
Category: 逆向
Tags: 逆向, 爬虫
Slug: Magisk-Hide-debuggable
Authors: qi
Summary: 做逆向时免不了几个操作：设置 ro.debuggable=1、root、xposed 。在 supersu 被国内公司收购之后， Magisk 成了 Android 设备 root 的第一选择。但是今天发现 magisk 的安装竟然会导致 ro.debuggable=1 的设置失效？



#### 简介
做逆向时免不了几个操作：设置 ro.debuggable=1、root、xposed 。在 supersu 被国内公司收购之后， Magisk 成了 Android 设备 root 的第一选择。但是今天发现 magisk 的安装竟然会导致 ro.debuggable=1 的设置失效？
#### 前情
之前一直使用正常的测试机 nexus 5，由于被同事借来借去，搞得手机里一团糟，因此打算直接重新刷机，还它一片碧水蓝天。nexus 5 刷机及逆向所需配置见 [此处还没写哈哈哈哈]，此处略过。

在之前，我是使用 xposed 的模块 [BDOpener](https://github.com/riusksk/BDOpener) 来直接开启调试，而非手动修改 ro.debuggable 的值，但是本次我打算直接改掉它，一劳永逸：[修改Nexus5的boot.img - 打开系统调试	](https://bbs.pediy.com/thread-197334.htm)。

在修改完 ro.debuggable=1 并重新刷入 boot.img 之后，顺手装上了 Magisk 作为
root 管理，并准备直接使用 magisk 安装 systemless 版的 xposed
框架来使用。全部装完之后，插上电脑准备看看 ro.debuggable 的修改生效了没，adb
shell 进入 Android shell，getprop ro.debuggable 获取一下值，如下图：

![图片1](https://img.biubiu7.cn/blog/201905140001.png)

似乎没生效？？？
#### 问题排查
查看 default.prop 文件中 ro.debuggable 的配置：

![图片2](https://img.biubiu7.cn/blog/201905140002.png)

配置似乎没有问题，说明之前的 boot.img 的修改是生效的。那么结合到 Magisk
的主要功能，这个大概就是 Magisk 的锅了。尝试完全卸载 Magisk 之后再查看
ro.dubuggable 的值，果然就是 1 了。

google 了一下，发现 MagiskHide 确实会修改 ro.debuggable 等参数的值来使手机更容易通过安全检查：[此处是文档](https://github.com/Magisk-Modules-Repo/MagiskHidePropsConf#setreset-magiskhide-sensitive-props)

注：部分应用会检测手机是否 root、是否安装了 Magisk 、xposed 等框架、甚至是否打开了 usb 调试，比如交通银行买单吧检测 root 退出、中国移动检测 root 和 xposed 闪退或卡启动页、微信检测 xposed 封号等，MagiskHide 能够一定程度上隐藏手机的 root 及 Magisk 安装情况。

#### 解决
既然知道了原因，自然有办法解决。Magisk 自身提供了 Resetprop 方法来修改系统属性值，不过经测试似乎不能持久化修改，即重启后修改后的值会恢复，我们使用 Magisk 模块 [MagiskHide Props Config](https://forum.xda-developers.com/apps/magisk/module-magiskhide-props-config-t3789228)来修改就好。

在 Magisk 自带的下载中搜索，然后安装、重启。重启后 adb shell 进入 shell，输入 props 回车，输入 4 选择 Edit MagiskHide props，然后选择修改 ro.debuggable ，之后按照提示一路 y 过去，重启后再查看 ro.debuggable ,已经 ok 了，电脑打开 DDMS 查看，也能够看到手机上的进程，完事儿。