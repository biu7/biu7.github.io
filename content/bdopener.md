Title: 开启 Android 全局调试的几种方法
Date: 2019-03-30
Category: 逆向
Slug: bdopener
Authors: qi
Summary: 应组长要求在公司 Confluence 写的教程，大致介绍一下相关工具和相关知识，因此会比较初级。第三节 - 开启 Android 全局调试的几种方法



- 自己打包 AOSP 刷入手机，麻烦程度五颗星
- 修改 boot.img 并重新刷入，麻烦程度四颗星
- 使用 Xposed 模块 [BDOpener](https://github.com/riusksk/BDOpener) 来开启，麻烦程度三颗星
- 使用 Magisk 来开启，麻烦程度两颗星

##### 方法一：

太麻烦，且 Google 的文档很详细，就不说了，可以自己去 [此处](https://source.android.google.cn/source/initializing) 看文档。

##### 方法二：

也很麻烦，且效果和三、四差不多，有兴趣的就自己搜一下 Android boot.img 怎么重打包好了。

##### 方法三：

首先你需要在手机上安装 Xposed 框架，截至目前 Xposed 仅支持到 Android 8 版本（基于 Magisk 的 Xposed 或许有更高的版本支持，未尝试）。

之后下载 BDOpener.apk 安装，然后在 Xposed Installer 中启用并重启手机即可。

##### 方法四：

首先你需要在手机上安装 Magisk 框架，Magisk 支持 Android 各版本。

打开 Magisk Manager ，从左侧划出菜单，选择下载，搜索 BusyBox，选择结果 BusyBox for Android NDK，点击下载，选择安装。
打开 Magisk Manager ，从左侧划出菜单，选择下载，搜索 MagiskHide，选择结果 MagiskHide Props Config，点击下载，安装，安装完成之后点击重启按钮重启手机。

手机开机之后连接电脑，终端输入 adb shell 进入手机 shell，输入 props，选择4，再选择 ro.debuggable，会提示你现在是 0 ，你确定要改成 1 吗，输入 y 确认，再输入 y 重启，重启完就完事儿了。
 

##### 确认调试已开启的方法

手机连接电脑，终端输入 adb jdwp ，如果调试已开启，会打印出可调试的进程的 PID ，如果没有成功开启调试，自然什么都打印不出来。