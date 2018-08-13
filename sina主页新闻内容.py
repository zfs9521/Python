# -*- coding: utf-8 -*-
import urllib.request
import os
import re

def getRespon(url):
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req).read().decode()

def getLink(url):
    respon=getRespon(url)
    stringList=re.compile('<div id=\"subShowContent1_news1\">(.*?)class=\"load-more\" id=\"subShowContent1_loadMoreW\"',re.S).findall(respon)
    stringLinkList=re.compile('<h2><a href=\"(.*?)\"',re.S).findall(stringList[0])
    return stringLinkList

def getNews(url,path):
    responString=getRespon(url)
    stringList=re.compile('<div class=\"article\" id=\"article\">.*?<p class=\"show_author\">',re.S).findall(responString)
    stringNews=re.compile('<p>(.*?)</p>',re.S).findall(stringList[0])
    f=open(path,'a')
    for string in stringNews:
        f.write(string+'\n')

def main():
    if os.path.exists('D:/workNews/') == False:
        os.mkdir('D:/workNews/')
    i=1
    stringLinkList=getLink('http://news.sina.com.cn/china/')
    for link in stringLinkList:
        getNews(link,'D:/workNews/'+str(i)+'.txt')
        print('已保存'+str(i)+'个文件到D:/workNews/！')
        i+=1

if __name__=="__main__":
    main()
