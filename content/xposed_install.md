Title: Xposed 的安装
Date: 2019-03-27
Category: 逆向
Slug: xposed_install
Authors: qi
Summary: 应组长要求在公司 Confluence 写的教程，大致介绍一下相关工具和相关知识，因此会比较初级。第二节 - Xposed 安装。



Xposed 是 Android 平台常用的 Hook 框架，对于抓包 / 逆向来说有不小的帮助。对于没有 Android 刷机经验的人来说装起来还是有点麻烦的，本文以组里最多的测试机 Google Nexus 5 为例，说一下详细的安装流程。

##### 解锁

当然不是解锁屏幕的解锁。Android 手机厂商出于防止恶意刷机或用户手机丢失后信息泄露之类的考虑，默认给 bootloader 加了锁，因此刷机前需要先解开 bootloader 锁才能刷机。各手机厂商的解锁方式不同，需要自行搜索相关解锁方法。爬虫组的 Nexus 5 测试机应都是已解锁的，可以直接刷机使用，其他测试机不知。注意，解锁 bootloader 将清空手机所有数据。

##### 刷入第三方 recovery

Android 的 recovery 用于清除手机数据、手机系统升级等，一般来说，Android 手机官方的 recovery 仅支持清除 cacha / data 分区、ota 升级等操作，而不支持刷入自定义的 zip 包，而第三方 recovery 则功能比较全面。第三方的 recovery 使用最多的应是 [twrp](https://dl.twrp.me/) ，可自行下载对应机型的 twrp recovery 镜像，nexus 5 的 twrp 下载地址在 [这里](https://dl.twrp.me/hammerhead/)。

下载好之后，从手机的开发者选项中打开 usb 调试，把手机开机状态下连接电脑，终端输入 adb reboot bootloader （当然也可以选择关机状态下音量下加开机键进入 bootloader ），手机将重启至 bootloader，然后终端输入 fastboot flash recovery twrp.img （将 twrp.img 替换为你下载的 img 文件路径），刷入完成之后将手机重启至 recovery 即可使用。

##### 使用 recovery 刷入 xposed 包

你可以在 [这里](https://dl-xda.xposed.info/framework/) 找到 xposed 的 zip 安装包，需要自行根据手机安卓版本和架构下载对应的包，下载错了的话手机可是会开不了机。安卓版本与 SDK 版本对照如下：

安卓版本 | SDK 版本 
---- | ----
5.0 |21
5.1 |22
6.0	|23
7.0	|24
7.1	|25
8.0	|26
8.1	|27

将下载好的 zip 包复制到手机目录中，在 twrp 中选择 install ，然后选择你的 zip 文件，刷入。

刷入完成后重启手机，检查是否有 xposed installer 应用被安装，如果没有，去 [这里](https://forum.xda-developers.com/showthread.php?t=3034811) 下载最新版本安装即可。

##### 附送 Magisk 安装方法

去 [这里](https://github.com/topjohnwu/Magisk/releases) 下载最新的 release 包，依照上述方法刷入即可。