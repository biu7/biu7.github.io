Title: 爬虫工程师相关工具
Date: 2019-03-24
Category: 逆向
Slug: tools
Authors: qi
Summary: 应组长要求在公司 Confluence 写的教程，大致介绍一下相关工具和相关知识，因此会比较初级。第一节 - 相关工具介绍。

##### 抓包工具
[Fiddler](https://www.telerik.com/fiddler) / [Charles](https://www.charlesproxy.com/) 个人惯用 Charles ，颜值即正义。

[Packet Capture](https://play.google.com/store/apps/details?id=app.greyshirts.sslcapture) 通过在手机上创建一个 VPN 来抓包，对部分 APP 有奇效。

##### 代理工具
[ProxyDroid](https://github.com/madeye/proxydroid) 部分 APP 会设置请求不走代理，这时会抓不到包。可在手机上安装这个 APP 来强制所有连接通过代理。需手机获取 ROOT 权限后使用。

##### Hook 工具
[Xposed](https://repo.xposed.info/) 杀手级 Hook 框架，有很多好用的模块。但是目前各大厂商对于 Xposed 的检测日趋严格，需要使用多种方法跳过对应的检测。或使用 Frida 也是不错的选择。

[Magisk](https://github.com/topjohnwu/Magisk) 一个台湾同胞开发的 Android 平台框架（但是他最近却入职了苹果？？？），与 Xposed 原理不同，模块比较少，我一般搭配 Xposed 使用。同时也是目前首选的 ROOT 权限管理软件。

[Frida](https://www.frida.re/) 基于 JS 的 Hook 框架，最近才开始了解，多平台可用，还在学习。

##### Xposed 模块
[JustTrustMe](https://github.com/Fuzion24/JustTrustMe) 破除 SSL Pinning 有奇效，github 上的 release 不是由最新代码编译的，建议自己 clone 下来编译，我也会上传一份最新代码编译的 apk 在 confluence 。

[BDOpener](https://github.com/riusksk/BDOpener) 真机调试时需开启全局 debug 开关，即设置 default.prop 中 ro.debuggable=1 。懒得修改 boot.img 重新刷机的可使用此模块直接开启。（其实使用 Magisk 开启调试更方便，以后写）

##### Frida 脚本
[DroidSSLUnpinning](https://github.com/WooyunDota/DroidSSLUnpinning) 根据 JustTrustMe 搞得一份 Frida 脚本，在无法破解 Xposed 检测的时候可用。

##### 逆向工具
[Apktool](https://ibotpeaches.github.io/Apktool/) Android 逆向必备，可逆向，也可重打包。

[dex2jar](https://github.com/pxb1988/dex2jar) Android 逆向必备，可直接转换 apk 为 jar / smali 。

[smali/baksmali/smalieda](https://bitbucket.org/JesusFreke/smali/downloads/) Android 逆向必备，反编译 / 回编译 / 适用于 idea 和 Android Studio 的 smali 代码调试插件。

[jadx](https://github.com/skylot/jadx) Android 逆向必备，直接反编译 apk 为 Java 源码。可用于静态分析代码，如果需要调试 smali 还是得用 smali 、 dex2jar 之类的工具。

[JEB](https://www.pnfsoftware.com/) 用过它的试用版，贼好用，正式版 1080 USD / 年，迫于贫穷，可自行搜索破解版。

##### 调试工具
[AndroidStudio](https://developer.android.com/studio) 其实是 Android 开发工具，配合 smalidea 插件可以调试 smali 源码。

[ida](https://www.hex-rays.com/products/ida/) 反汇编与动态调试工具，可用于 Android Native 层调试。瞅了一眼价格，1879 USD ，迫于贫穷，可自行搜索破解版。

##### 脱壳工具
脱壳比较复杂，待续

