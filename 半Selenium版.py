# -*- coding: utf-8 -*-
# @Time : 8/9/2021 3:41 PM
# @Author : Michael
# @File : 半Selenium版.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from urllib.parse import unquote
import time
import requests
import re
reseed=re.compile(r"\?seed=([^&]*)&|$") #匹配Seed参数,选择第二个匹配项
rets=re.compile(r"&ts=([^&]*)&|$")#匹配ts参数
rename=re.compile(r"&name=([^&]*)&|$")#匹配name参数
def getinfo():      #第一个请求,获取Cookies,获取合成zpstoken需要的参数seed和ts
    head = []
    param={}
    headers = {
        "Host": "www.zhipin.com",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:90.0)Gecko/20100101Firefox/90.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br"
    }
    url = "https://www.zhipin.com/c101010100-p100122/?page=1"
    res = requests.get(url=url, headers=headers, allow_redirects=False)
    head.append(res.cookies)    #第一个元素为Cookies
    head.append(unquote(res.headers['location'].encode().decode("utf-8")))   #第二个元素为设置Refer需要的参数,location前加上域名即为Refer
    param['seed']=re.findall(reseed,head[1])[0]  #匹配Seed
    param['ts']=re.findall(rets, head[1])[0] #匹配ts
    param['name']=re.findall(rename, head[1])[0] #匹配name
    head.append(param)
    return head
def getCookie():
    # chrome_options = Options()
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.headless = True  # 开启无头模式
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    url = "https://www.zhipin.com/c101010100-p100122/?page=1"
    wb = webdriver.Chrome("E:\WebDriver\chromedriver.exe")#, options=chrome_options)
    wb.get(url)
    Flag=True
    Cookies = wb.get_cookies()
    while Flag:
        for i in Cookies:
            if i['name']=="__zp_stoken__":
                Flag=False
                break
        time.sleep(1)
        Cookies = wb.get_cookies()
    wb.quit()
    Cookie={}
    for cook in Cookies:
        name=cook['name']
        value=cook['value']
        Cookie[name]=value
    return Cookie
def gethtml(page,Cookie,info):
    headers = {
            "Host": "www.zhipin.com",
            "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:90.0)Gecko/20100101Firefox/90.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer":"https://www.zhipin.com"+info
    }
    Cookie1={
        "__zp_stoken__":Cookie['__zp_stoken__'],
        "acw_tc":Cookie['acw_tc'],
    }
    print(headers["Referer"],"\n",Cookie1)
    res=requests.get(f"https://www.zhipin.com/c101010100-p100109/?page={page}",headers=headers,cookies=Cookie1)
    return res.content.decode("utf-8")
def parserhtml(html):
    tree=etree.HTML(html)
    ul=tree.xpath('//*[@id="main"]/div/div[3]/ul/li')
    if ul==[]:
        return False
    joblist=[]
    for li in ul:
        job = {}
        job['name']=li.xpath("./div/div[1]/div[1]/div/div[1]/span[1]/a/text()")[0]
        job['money']=li.xpath("./div/div[1]/div[1]/div/div[2]/span/text()")[0]
        job['exp']=li.xpath("./div/div[1]/div[1]/div/div[2]/p//text()")[0]
        job['edu']=li.xpath("./div/div[1]/div[1]/div/div[2]/p//text()")[1]
        text="".join(li.xpath("./div/div[2]/div[1]//text()"))
        job['ability'] =text.replace("\n","").replace("                                                    ",",").replace("                                        ","")[1:]
        job['address']=li.xpath("./div/div[1]/div[1]/div/div[1]/span[2]/span/text()")[0]
        job['company']=li.xpath("./div/div[1]/div[2]/div/h3/a/text()")[0]
        text=",".join(li.xpath("./div/div[1]/div[2]/div/p//text()"))
        job['cminfo']=text
        job['gift']=li.xpath("./div/div[2]/div[2]/text()")[0]
        joblist.append(job)
    return joblist
if __name__ == '__main__':
    head=getinfo()
    Cookie=getCookie()
    html=gethtml(1,Cookie,head[1])
    if "请稍后" in html:
        print("获取页面Cookie及Referer失败 或__zp_stoken__失效")
        exit()
    res=parserhtml(html)
    print(res)
