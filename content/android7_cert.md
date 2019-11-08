Title: Android 7.0 及以上版本抓包证书设置
Date: 2019-03-30
Category: 逆向
Slug: android7_cert
Authors: qi
Summary: 应组长要求在公司 Confluence 写的教程，大致介绍一下相关工具和相关知识，因此会比较初级。第四节 - Android 7.0 及以上版本抓包证书设置


由于 Android 7.0 起 Google 更新了 Android 的安全策略，App可以选择只信任系统证书及自己的证书，这样我们传统的抓包方式就失效了。以下是几种解决办法。

##### 将 App 逆向后修改证书策略，再重打包

老实讲，这是个虽然有用但是不怎么实用的方法，看标题就知道很麻烦了，跳过不讲

##### 在手机获取 root 权限后，将证书放入系统证书目录

Android 的系统证书目录为 /system/etc/security/cacerts/，里边证书的命名规则是 <Certificate_Hash>.<Number> 。

我们使用以下命令获取证书的 hash 值，

    openssl x509 -subject_hash_old -in <Certificate_File>

然后重命名证书为 <hash>.0，然后放入 /system/etc/security/cacerts/ 目录，再修改文件权限为 644 ，重启手机即可。

##### 使用 Magisk 自动将证书移入系统证书目录

原理和方法二一样，只是自动化了。直接在 Magisk Manager 中搜索 Move Certificates 安装，然后重启即可。