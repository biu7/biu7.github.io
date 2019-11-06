Title: Ubuntu Server 16.04 SSH 开启多因素认证（MFA）
Date: 2018-09-02
Category: 杂项
Slug: ubuntu_ssh_mfa
Authors: qi
Summary: Ubuntu Server 16.04 SSH 开启多因素认证（MFA）



今天想把腾讯云的服务器（ubuntu 16.04）加上二次认证，大致google了一下，大致流程如下。

##### 安装Google PAM
首先更新一下ubuntu软件仓库缓存，然后apt安装libpam-google-authenticator。

    sudo apt update
    sudo apt install libpam-google-authenticator
    
##### 初始化
安装完成之后运行google-authenticator进行初始化：

    google-authenticator

出现如下提示，回复y：

    Do you want authentication tokens to be time-based (y/n) y
然后会输出一些信息，其中包含一个很大的二维码，用你手机上的google身份验证器（或者别的OATH-TOTP软件）扫描输出的二维码，添加成功之后会有每30秒刷新一次的6位数字码。

之后对输出的问题一一回复：
    
    是否将 key 和配置写入 .google_authenticator 文件，我们选择y
    Do you want me to update your "/home/ubuntu/.google_authenticator" file (y/n) y
&ensp;

    是否设置使用过的密码立即过期，防止有人截获你使用的代码用它登录，选y
    Do you want to disallow multiple uses of the same authentication
    token? This restricts you to one login about every 30s, but it increases
    your chances to notice or even prevent man-in-the-middle attacks (y/n) y
&ensp;

    默认每组数字码的有效时间是30s，是否把时间调到4分钟，选n
    By default, tokens are good for 30 seconds and in order to compensate for
    possible time-skew between the client and the server, we allow an extra
    token before and after the current time. If you experience problems with poor
    time synchronization, you can increase the window from its default
    size of 1:30min to about 4min. Do you want to do so (y/n) n
&ensp;

    是否限制30秒内只允许尝试登录3次，选y
    If the computer that you are logging into isn't hardened against brute-force
    login attempts, you can enable rate-limiting for the authentication module.
    By default, this limits attackers to no more than 3 login attempts every 30s.
    Do you want to enable rate-limiting (y/n) y
    
##### 配置
修改 /etc/pam.d/sshd 文件

    sudo vim /etc/pam.d/sshd
在文件底部添加一行：
    
    auth required pam_google_authenticator.so nullok
最后的 nullok 是指这种登录方式是可选的，如果最后测试可用，可以把 nullok 删掉。
修改 /etc/ssh/sshd_config 文件

    sudo vim /etc/ssh/sshd_config
找到 ChallengeResponseAuthentication ，并设置为 yes

    ChallengeResponseAuthentication yes
重启 ssh 服务：
    
    sudo service ssh restart
从新的终端尝试 ssh 登录，应该已经可以使用数字验证码登陆了，不过建议继续配置 ssh 密钥 + mfa 登录
修改 /etc/ssh/sshd_config 文件

    sudo vim /etc/ssh/sshd_config
在底部添加如下行：

    UsePAM yes
    AuthenticationMethods publickey,keyboard-interactive
    
然后修改 /etc/pam.d/sshd 文件，找到 @include common-auth ，在行前加#号注释掉：
    
    #@include common-auth
重启 ssh 服务：
    
    sudo service ssh restart
从新的终端尝试登录，应该ok了
