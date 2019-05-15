#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'qi'
SITENAME = 'biubiu7'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

THEME = "attila"

HEADER_COLOR = "black"

BEIAN = "豫ICP备18037159号"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/panjiajia01'),
)

AUTHORS_BIO = {
  "qi": {
    "name": "七",
    "cover": "https://arulrajnet.github.io/attila-demo/assets/images/avatar.png",
    "image": "https://arulrajnet.github.io/attila-demo/assets/images/avatar.png",
    "website": "https://www.biubiu7.cn",
    "location": "ShangHai/China",
    "bio": "爬虫 / Android/ 逆向工程师，数据科学萌新，主要语言 Python、Java、Golang"
  }
}


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


STATIC_PATHS = ['assets']

EXTRA_PATH_METADATA = {
    'assets/favicon.ico': {'path': 'favicon.ico'},
    'assets/CNAME': {'path': 'CNAME'}
}

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# 文章评论，使用 gitalk
# GITALK_CLIENTID = '6214d54e6d518aaa2f6a'
# GITALK_CLIENT_SECRET = '9f76763102db0d037a87dcffbfd88f3a45f723f9'
# GITALK_REPO = 'panjiajia01.github.io'
# GITALK_OWNER = 'panjiajia01'
# GITALK_ADMIN = ['panjiajia01']
# GITALK_DISTRACTION_FREE_MODE = 'false'


# 文章评论，使用 valine
VALINE_APPID = '2WOykmLJ16hcACygaOrAxKJQ-gzGzoHsz'
VALINE_APPKEY = 'roiSV2zvTdHgyKldWSCstCu2'
# VALINE_VERIFY = 'true'  # 是否启用验证码
# VALINE_PLACE_HOLDER = 'lallala'  # 输入框提示输入文字