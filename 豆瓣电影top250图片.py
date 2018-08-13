# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import re
import os
def getHtmlString(url):
    kv={'User-Agent':'Mozilla/5.0'}
    try:
        req=urllib.request.Request(url,headers=kv)
        htmlString=urllib.request.urlopen(req).read().decode()
    except urllib.error.URLError as e:
        print(e)
        htmlString=''
    except urllib.error.HTTPError as reason:
        print(reason)
        htmlString=''
    finally:
        return htmlString
def getImageLinkList(htmlString):
    imageLinkList=re.compile('<img width="100" alt="(.*?)" src="(.*?)"').findall(htmlString)
    return imageLinkList
def saveImage(imageLinkList,path):
    i=1
    if os.path.exists(path)==False:
        os.mkdir(path)
    for tup in imageLinkList:
        urllib.request.urlretrieve(tup[1],filename=path+tup[0]+'.jpg')
        print('第'+str(i)+'个文件已经保存到'+path)
        i+=1
def main():
    path='D:/doubanImage/'
    for i in range(10):
        url='https://movie.douban.com/top250?start='+str(i*25)
        htmlString=getHtmlString(url)
        if htmlString!='':
            imageLinkList=getImageLinkList(htmlString)
            saveImage(imageLinkList,path)
if __name__=='__main__':
    main()