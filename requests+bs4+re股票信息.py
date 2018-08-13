# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
import xlwt

def getHtml(url,encode='utf-8'):
    try:
        respon=requests.get(url,timeout=30)
        respon.raise_for_status()
        respon.encoding=encode
        return respon.text
    except Exception as e:
        print(e)
        return ''

def getGuList(htmlString,numList):
    soup=BeautifulSoup(htmlString,'html.parser')
    aList=soup.find_all('a')

    for a in aList:
        try:
            string=a.attrs['href']
            num=re.findall('s[hz]\d{6}\.html',string)
            if len(num)!=0:
                numList.append(num[0])
        except:
            continue

def getGuInfo(urlb,numList,infoList):
    i=0
    numList=numList[:1]+numList[60:]
    length=len(numList)

    if length!=0:
        for num in numList:
            try:
                lis = []
                url=urlb+num
                htmlString=getHtml(url)
                soup=BeautifulSoup(htmlString,'html.parser')
                a=soup.find('a',class_='bets-name')
                lis.append(a.text.strip())
                div=soup.find('div',class_='bets-content')
                ddList=div.find_all('dd')
                for ddTag in ddList:
                    lis.append(ddTag.text.strip())
                if len(lis)!=1:
                    infoList.append(lis)
            except:
                pass
            i += 1
            print('\r信息提取进度：{:.2f},未保存，请不要退出！！'.format(i * 100 / length))

def saveGuInfo(infoList):
    i=1
    while os.path.exists('D:/'+str(i)+'.xlsx'):
        i+=1
    workbook=xlwt.Workbook(encoding='utf-8')
    workSheet=workbook.add_sheet('stock')
    for j in range(len(infoList)):
        for k in range(len(infoList[j])):
            workSheet.write(j,k,infoList[j][k])
    workbook.save('D:/'+str(i)+'.xlsx')
    print('文件已经保存在D:/'+str(i)+'.xlsx中！')
def main():
    url='http://quote.eastmoney.com/stocklist.html'
    numList=[]
    infoList=[]
    urlb='https://gupiao.baidu.com/stock/'
    htmlString=getHtml(url,'GB2312')
    if htmlString!='':
        getGuList(htmlString,numList)
        getGuInfo(urlb,numList,infoList)
        saveGuInfo(infoList)
        # print(infoList)
if __name__=='__main__':
    main()