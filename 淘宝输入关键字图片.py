# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import re
import os
def getHtml(url):
    return urllib.request.urlopen(url).read().decode()

def getImageLink(urlHtmlString):
    imageLinkList=re.compile('pic_url":"(.*?)"').findall(urlHtmlString)
    for index in range(len(imageLinkList)):
        imageLinkList[index]='https:'+imageLinkList[index]
    return imageLinkList

def saveImage(imageLinkList):
    if os.path.exists('D:/imageTao/')==False:
        os.mkdir('D:/imageTao')
    i=1
    for link in imageLinkList:
        urllib.request.urlretrieve(link,filename='D:/imageTao/'+str(i)+'.jpg')
        print('第'+str(i)+'个图片已经保存到D:/imageTao/')
        i+=1

def main():
    keyWord=input('请输入关键字:')
    for i in range(10):
        keyWord=urllib.request.quote(keyWord)
        url='https://s.taobao.com/search?q='+keyWord+'&s='+str(i*48)
        urlHtmlString=getHtml(url)
        imageLinkList=getImageLink(urlHtmlString)
        saveImage(imageLinkList)


if __name__=='__main__':
    main()