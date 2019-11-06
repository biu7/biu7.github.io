Title: 验证码识别之 pytesseract
Date: 2017-12-31
Category: 爬虫
Slug: tesseract
Authors: qi
Summary: 使用 pytesseract 识别简单的图片验证码 


#### 前言
前些天在工作之余接了个爬虫的私活，反爬倒是一般，但是每次翻页都要输入验证码，接入打码平台倒是省事儿，但是能不花钱还是不花钱的好，所以来看一下这个网站的验证码的识别

#### 安装
系统 ubuntu 16.04
首先，pytesseract 是依赖于 tesseract 运行的，因此我们先安装tesseract：

sudo apt install tesseract-ocr
安装完成之后再安装 pytesseract：

    pip install pytesseract

#### 识别
pytesseract 的使用还是比较简单的，先看我们需要识别的图片：
![](https://img.biubiu7.cn/blog/validatecode.jpg)
图片比较简单，字符之间没有粘连，字体变形也不严重，目测不需要分割字符，直接识别就可以，代码如下：
    
    import pytesseract
    from PIL import Image

    img = Image.open('validatecode.jpg')
    code = pytesseract.image_to_string(img)
    print(code)
可以看到直接就可以识别成功。
再获取其他图片进行识别时，发现会有识别成小写字母和数字以外的字符的情况，因此我们对识别的字符做一下限定：

    code = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz')
这样，就限制 pytesseract 只识别小写字母和数字了，再去测试，可以发现成功率有所提高。
不过 pytesseract 也只能对简单的字符进行识别，如果字符有粘连、扭曲、干扰线等情况，pytesseract就无能为力了，需要我们对图片进行处理后再识别。
