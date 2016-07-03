# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup

class Login:

    #初始化
    def __init__(self):
        #学号密码
        self.username = '2151574'
        self.password = 'aaayy1314'
        self.cj = cookielib.MozillaCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        # 注意：url地址在网络监测器中显示格式可能为http://cas.dhu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.dhu.edu.cn%2Findex.portal
        # 这是url编码格式，需要转换成正常格式
        self.login_url= "http://cas.dhu.edu.cn/authserver/login?service=http://my.dhu.edu.cn/index.portal"

        #第一次抓取页面，保存获得的登录页面的内容
        response = self.opener.open(self.login_url)
        resultStr = response.read()


        # 获取隐藏的三个元素
        #方法一：正则表达式搜索
        #self.lt = re.search(re.compile('name="lt".*?value="(.*?)".*?'), resultStr).group(1).strip()
        #self.execution = re.search(re.compile('name="execution".*?value="(.*?)".*?'), resultStr).group(1).strip()
        #self._eventId = re.search(re.compile('name="_eventId".*?value="(.*?)".*?'), resultStr).group(1).strip()

        #方法二：beautifulsoup搜索
        soup = BeautifulSoup(resultStr, "lxml")
        self.execution = soup.find_all(attrs={"name": "execution"})[0]['value']
        self.lt= soup.find_all(attrs={"name": "lt"})[0]['value']
        self._eventId = soup.find_all(attrs={"name": "_eventId"})[0]['value']


    # 模拟登录
    def login(self):
        # print self.getCurrentTime(), u"正在尝试认证QLSC_STU无线网络"
        # 登录元素初始化
        data = urllib.urlencode({
            'username': self.username,
            'password': self.password ,
            'lt': self.lt,
            'execution': self.execution,
            '_eventId': self._eventId,
            'rmShown': 1
        })

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',

        }

        request = urllib2.Request(self.login_url, data, headers)
        try:
            response = self.opener.open(request)
        except urllib2.URLError, e:
            print e.reason

        result = response.read()
        return result
        # self.getLoginResult(result)


l=Login().login()
print l