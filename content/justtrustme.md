Title: 使用 JustTrustMe 解除 SSL Pinning
Date: 2019-04-10
Category: 逆向
Slug: justtrustme
Authors: qi
Summary: 应组长要求在公司 Confluence 写的教程，大致介绍一下相关工具和相关知识，因此会比较初级。第五节 - 使用 JustTrustMe 解除 SSL Pinning


JustTrustMe 是一个 Xposed 模块，使用时只需将 JustTrustMe 安装在手机上，并在 Xposed Installer 中启用即可。

它的原理是通过 classLoader.loadClass 去查找网络请求库，如 okhttp 的证书锁定类，找到之后直接 Hook 其证书检测的方法 。以下是 JustTrustMe 对 okhttp3 的证书锁定进行 Hook 的代码：

    try {
        classLoader.loadClass("okhttp3.CertificatePinner");
        findAndHookMethod("okhttp3.CertificatePinner",
              classLoader,
              "check",
              String.class,
              List.class,
              new XC_MethodReplacement() {
                @Override
                protected Object replaceHookedMethod(MethodHookParam methodHookParam) throws Throwable {
                    return null;
                }
            });
    } catch (ClassNotFoundException e) {
        Log.d(TAG, "OKHTTP 3.x not found in " + currentPackageName + " -- not hooking");
    }
    
那么对于大部分 App 来说，由于在应用编译打包时很少会对项目依赖的第三方库进行混淆，我们并不需要修改 JustTruestMe 的代码即可使用。但是对于少部分对第三方库也进行代码混淆的 App 来说，他们对代码的混淆会直接使 JustTrustMe 查找不到证书锁定类而失效，以下是未混淆的 okhttp3 与中国电信 App 中对 okhttp3 进行混淆的结构对比图：

![1](https://img.biubiu7.cn/blog/201904100001.png)![2](https://img.biubiu7.cn/blog/201904100002.png)

注：.kt 文件为 Kotlin 语言代码文件，Kotlin 已被 Google 声明为 Android 官方支持的开发语言

可以看到，原本的类名被混淆为无法与原类名关联的类名，这势必会使 JustTrustMe 的 Hook 失效。

##### 解决代码混淆导致的失效

我们从 github 拉下 JustTrustMe 的源码，使用全局搜索定位到 JustTrustMe 源码中与
okhttp 有关的代码如下：


    try {
        classLoader.loadClass("okhttp3.CertificatePinner");
        findAndHookMethod("okhttp3.CertificatePinner",
                classLoader,
                "check",
                String.class,
                List.class,
                new XC_MethodReplacement() {
                    @Override
                    protected Object replaceHookedMethod(MethodHookParam methodHookParam) throws Throwable {
                        return null;
                    }
                });
    } catch (ClassNotFoundException e) {
        Log.d(TAG, "OKHTTP 3.x not found in " + currentPackageName + " -- not hooking");
        // pass
    }
 
    try {
        classLoader.loadClass("okhttp3.internal.tls.OkHostnameVerifier");
        findAndHookMethod("okhttp3.internal.tls.OkHostnameVerifier",
                classLoader,
                "verify",
                String.class,
                javax.net.ssl.SSLSession.class,
                new XC_MethodReplacement() {
                    @Override
                    protected Object replaceHookedMethod(MethodHookParam methodHookParam) throws Throwable {
                        return true;
                    }
                });
    } catch (ClassNotFoundException e) {
        Log.d(TAG, "OKHTTP 3.x not found in " + currentPackageName + " -- not hooking OkHostnameVerifier.verify(String, SSLSession)");
        // pass
    }
 
    //https://github.com/square/okhttp/blob/parent-3.0.1/okhttp/src/main/java/okhttp3/internal/tls/OkHostnameVerifier.java
    try {
        classLoader.loadClass("okhttp3.internal.tls.OkHostnameVerifier");
        findAndHookMethod("okhttp3.internal.tls.OkHostnameVerifier",
                classLoader,
                "verify",
                String.class,
                java.security.cert.X509Certificate.class,
                new XC_MethodReplacement() {
                    @Override
                    protected Object replaceHookedMethod(MethodHookParam methodHookParam) throws Throwable {
                        return true;
                    }
                });
    } catch (ClassNotFoundException e) {
        Log.d(TAG, "OKHTTP 3.x not found in " + currentPackageName + " -- not hooking OkHostnameVerifier.verify(String, X509)(");
        // pass
    }


可以看到源码中共对 okhttp3 的三个方法进行了 hook ，分别是：okhttp3.CertificatePinner 类的 check 方法和 okhttp3.internal.tls.OkHostnameVerifier 的两个 verify 方法。

接下来我们对照 okhttp3 的源代码，
分别找出对应的混淆后的类名和方法，然后在JustTrustMe 的源码中替换，并编译后安装即可。

 
注：使用 Andoid Studio 编译 JustTrustMe 时需在设置中关闭 Instant Run

