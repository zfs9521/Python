import requests
import bs4
import re
from bs4 import BeautifulSoup




def getHtmlInfo(url):#获取网页文档
    try:
       # dic={"start":"0","type":"T"}
        r=requests.get(url,timeout=30)
        r.raise_for_status() #根据状态码判断是否访问成功
       
        return r.text
    except:
        return "出错了！"



    
def selectReadInfo(html,urllist):#图书主页html  获取图书分类信息将图书的类别存到urllist列表中
    soup=BeautifulSoup(html,"html.parser")#解析
    lis=[]
    ss=""
    for tag in soup("ul",class_="clearfix"):
        if tag.find("li").string !=None:
            print(str(tag.find("li").string).strip(),":\n")#列表标签分类标题
        for tag_ in tag("a",class_="tag"):#遍历出每个分类里的子分类
            if(str(tag_.string)!="更多»"):
                lis.append(str(tag_.string))
                urllist.append(str(tag_.string))
        for s in lis:
            ss+=s+"\t"
        print(ss,"\n\n")
        ss=""
        lis=[]



        
def searchBook(html,lis,liss):#某个种类的图书排行主页html 图书名称及其链接存入lis字典 图书名称存入liss列表方便用户浏览
    print("\n\n\n")
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup("div",class_="info"):
        lis[tag.find("a").attrs["title"]]=tag.find("a").attrs["href"]#图书名和图书链接对应放入字典
        liss.append(tag.find("a").attrs["title"])#图书名称放入列表
        print(tag.find("a").attrs["title"]+"\n"+tag.find("div",class_="pub").string+"\n"+tag.find("span",class_="pl").string+"\n"+tag.find("p").string)
        print("\n\n\n\n\n\n\n")
    #print(lis)



        
    
def bookInfo(html):#某个图书信息的html  爬取出图书的相关信息以及部分精彩短评和长的书评
    #print(html[:200])
    i=5
    soup=BeautifulSoup(html,"html.parser")
    s=soup.find("div",id="info")
    for tag_ in s("span",class_="pl"):#爬取图书作者 出品方等信息
        if str(tag_.string)=="作者:" or str(tag_.string)=="丛书:" or str(tag_.string)=="出品方:":
            print(tag_.string,tag_.next_sibling.next_sibling.string)
        else:
            print(tag_.string,tag_.next_sibling)
    print("豆瓣评分:",soup.find("strong").string)
    
    for tag in soup("span",class_="rating_per"):#爬取图书评分
        print(i,"星:",tag.string)
        i-=1
        ss=soup.find("div",class_="intro")
    print("\n\n\n")
    print("内容简介:")
    for ta in ss("p"):#爬取图书简介
        print(ta.string)
    print("\n\n\n")
    print("章节目录：")
    so=soup.find("div",style="display:none")
    for t in so("br"):#爬取图书部分目录信息
        print(t.previous_sibling)
    j=1
    print("\n\n\n")
    print("部分短评:\n\n")
    for pl in soup("p",class_="comment-content"):#爬取部分精彩短评
        print(j,":",pl.string,"\n")
        j+=1
    j=1
    print("\n\n\n")
    print("部分书评:\n\n")
    for p in soup("div",class_="short-content"):#爬取部分精彩书评
        print(j,":",(((str(p).split(">"))[1]).split("..."))[0],"\n")
        j+=1
        #print(p)
        
def movie(html):#爬取电影排行
    i=1
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup("div",class_="pl2"):#循环遍历出具有电影信息的标签  提取电影信息
        print(i,":",str(tag.find("a")).split(">")[1].split("/")[0].lstrip().rstrip(),"\t地址:",tag.find("a").attrs["href"],"\n")
        i+=1

        
def music(html):#爬取音乐排行
    i=1
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup("li",class_="clearfix"):#循环遍历出具有歌曲信息的标签  提取歌曲信息
        if i<=10:
            t=tag.find("div")
            print(i,":",t.find("a").string)
            #print(t.find("p"))
            print(str(t.find("p")).split("/")[1].split("<")[0].lstrip(),"\n")
            i+=1
            

def main():
    selectP={"读书":"book","音乐":"music","电影":"movie","退出":"break"}
    while 1:
        string=str(input("请输入想查看的类别（读书、音乐、电影、退出）:"))
        print("\n")
        if string in selectP.keys():
            url="http://"+selectP.get(string)+".douban.com"#根据输入内容更改url信息
            if string=="读书":
                urllist=[]
                selectReadInfo(getHtmlInfo(url),urllist)#获取图书分类信息
                #print("\n")
                #print(urllist)
                string=str(input("请输入想读的图书种类:"))
                string2=int(input("请输入想读的页数:"))
                if string in urllist and string2<=10:#爬取相应图书种类的多少页图书排行
                    lis={}
                    liss=[]
                    for i in range(string2):
                        url="http://book.douban.com/tag/"+string+"?start="+str(i*20)+"&type=T" #每一页的url
                        searchBook(getHtmlInfo(url),lis,liss)#获取图书名称和对应的连接
                    print("书单表:\n\n")
                    print(liss)
                    print("\n\n\n\n\n\n")
                    string=str(input("请输入想查看的图书名称:"))
                    if string in lis.keys():
                        bookInfo(getHtmlInfo(lis[string]))#获取图书具体信息和评论等
            if string =="电影":
                url="http://movie.douban.com/chart"
                movie(getHtmlInfo(url))#爬取部分电影排行
            if string =="音乐":
                url="http://music.douban.com/chart"
                music(getHtmlInfo(url))#爬取部分音乐排行
            if string =="退出":
                break
if __name__=="__main__":
    main()
