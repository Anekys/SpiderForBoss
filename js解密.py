# -*- coding: utf-8 -*-
# @Time : 8/6/2021 8:53 PM
# @Author : Michael
# @File : js解密.py
import execjs
import requests
import re
reseed=re.compile(r"\?seed=([^&]*)&|$") #匹配Seed参数,选择第二个匹配项
rets=re.compile(r"&ts=([^&]*)&|$")#匹配ts参数
def firsreq():      #第一个请求,获取Cookies,获取合成zpstoken需要的参数seed和ts
    Cookies = []
    headers = {
        "Host": "www.zhipin.com",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:90.0)Gecko/20100101Firefox/90.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br"
    }
    url = "https://www.zhipin.com/c101010100-p100122/?page=1"
    res = requests.get(url=url, headers=headers, allow_redirects=False)
    Cookies.append(res.cookies)    #第一个元素为Cookies
    Cookies.append(res.headers['location'].encode().decode("utf-8"))    #第二个元素为设置Refer需要的参数,location前加上域名即为Refer
    Cookies.append(re.findall(reseed,Cookies[1])[0])  #匹配Seed
    Cookies.append(re.findall(rets, Cookies[1])[0]) #匹配ts
    return Cookies
def getjs(head):    #拿到Cookies等必要参数后获取加密用的js并写出文件
    headers = {
        "Host": "www.zhipin.com",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:90.0)Gecko/20100101Firefox/90.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br"
    }
    cookies=head[0]
    url="https://www.zhipin.com/web/common/security-js/028df162.js"
    js=requests.get(url=url,headers=headers,cookies=cookies).content.decode("utf-8")
    with open("security.js","w",encoding="utf-8") as f:
        f.write(js)

if __name__ == '__main__':
    head=firsreq()
    print(head)
    getjs(head)
    #test=execjs.compile(open("security.js","r").read())
    #test = execjs.compile(open(r"security.js").read()).call('ABC'，'steam')