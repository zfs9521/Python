# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import re
import xlwt
def getHtmlString(url):
    kv=('User-Agent','Mozilla/5.0')
    try:
        opener=urllib.request.build_opener()
        opener.addheaders=[kv]
        urllib.request.install_opener(opener)
        respon=urllib.request.urlopen(url)
        htmlString=respon.read().decode()
    except (urllib.error.HttpError,urllib.error.URLError) as e:
        print(e)
        htmlString=''
    except Exception as res:
        print(res)
        htmlString=''
    finally:
        return htmlString

def getGoodsInfo(htmlString):
    infoList=re.compile('"pid":"","title":"(.*?)","raw_title":"(.*?)","pic_url":"(.*?)","detail_url":".*?","view_price":"(.*?)","view_fee":"(.*?)","item_loc":"(.*?)","view_sales":"(.*?)","comment_count":".*?","user_id":"(.*?)","nick":"(.*?)","shopcard"').findall(htmlString)
    return infoList
def printGoodsInfo(goodsInfoList):
    for info in goodsInfoList:
        print(info)
def saveGoodsInfo(goodsInfo,path):
    workbook=xlwt.Workbook(encoding='utf-8')
    sheet=workbook.add_sheet('goodsinfo')
    j=0
    for tup in goodsInfo:
        for i in range(len(tup)):
            sheet.write(j,i,tup[i])
        j+=1
    workbook.save(path)
    print('文件已保存在D:/goods.xlsx')
def main():
    path='D:/goods.xlsx'
    allGoodsInfo=[]
    for i in range(50):
        url='https://s.taobao.com/search?q=%E9%9B%B6%E9%A3%9F&s='+str(i*44)
        htmlString=getHtmlString(url)
        if htmlString!='':
            goodsInfoList=getGoodsInfo(htmlString)
            allGoodsInfo.extend(goodsInfoList)
            # printGoodsInfo(goodsInfoList)
        print('商品第'+str(i+1)+'页已完成,请等待程序结束！')
    saveGoodsInfo(allGoodsInfo,path)
if __name__=='__main__':
    main()


