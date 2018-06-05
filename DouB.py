import requests
import bs4
import re
from bs4 import BeautifulSoup




def getHtmlInfo(url):
    try:
       # dic={"start":"0","type":"T"}
        r=requests.get(url,timeout=30)
        r.raise_for_status()
       
        return r.text
    except:
        return "出错了！"



    
def selectReadInfo(html,urllist):
    soup=BeautifulSoup(html,"html.parser")
    lis=[]
    ss=""
    for tag in soup("ul",class_="clearfix"):
        if tag.find("li").string !=None:
            print(str(tag.find("li").string).strip(),":\n")
        for tag_ in tag("a",class_="tag"):
            if(str(tag_.string)!="更多»"):
                lis.append(str(tag_.string))
                urllist.append(str(tag_.string))
        for s in lis:
            ss+=s+"\t"
        print(ss,"\n\n")
        ss=""
        lis=[]



        
def searchBook(html,lis,liss):
    print("\n\n\n")
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup("div",class_="info"):
        lis[tag.find("a").attrs["title"]]=tag.find("a").attrs["href"]
        liss.append(tag.find("a").attrs["title"])
        print(tag.find("a").attrs["title"]+"\n"+tag.find("div",class_="pub").string+"\n"+tag.find("span",class_="pl").string+"\n"+tag.find("p").string)
        print("\n\n\n\n\n\n\n")
    #print(lis)



        
    
def bookInfo(html):
    #print(html[:200])
    i=5
    soup=BeautifulSoup(html,"html.parser")
    s=soup.find("div",id="info")
    for tag_ in s("span",class_="pl"):
        if str(tag_.string)=="作者:" or str(tag_.string)=="丛书:" or str(tag_.string)=="出品方:":
            print(tag_.string,tag_.next_sibling.next_sibling.string)
        else:
            print(tag_.string,tag_.next_sibling)
    print("豆瓣评分:",soup.find("strong").string)
    
    for tag in soup("span",class_="rating_per"):
        print(i,"星:",tag.string)
        i-=1
        ss=soup.find("div",class_="intro")
    print("\n\n\n")
    print("内容简介:")
    for ta in ss("p"):
        print(ta.string)
    print("\n\n\n")
    print("章节目录：")
    so=soup.find("div",style="display:none")
    for t in so("br"):
        print(t.previous_sibling)
    j=1
    print("\n\n\n")
    print("部分短评:\n\n")
    for pl in soup("p",class_="comment-content"):
        print(j,":",pl.string,"\n")
        j+=1
    j=1
    print("\n\n\n")
    print("部分书评:\n\n")
    for p in soup("div",class_="short-content"):
        print(j,":",(((str(p).split(">"))[1]).split("..."))[0],"\n")
        j+=1
        #print(p)
        
def movie(html):
    i=1
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup("div",class_="pl2"):
        print(i,":",str(tag.find("a")).split(">")[1].split("/")[0].lstrip().rstrip(),"\t地址:",tag.find("a").attrs["href"],"\n")
        i+=1

        
def music(html):
    i=1
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup("li",class_="clearfix"):
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
            url="http://"+selectP.get(string)+".douban.com"
            if string=="读书":
                urllist=[]
                selectReadInfo(getHtmlInfo(url),urllist)
                #print("\n")
                #print(urllist)
                string=str(input("请输入想读的图书种类:"))
                string2=int(input("请输入想读的页数:"))
                if string in urllist and string2<=10:
                    lis={}
                    liss=[]
                    for i in range(string2):
                        url="http://book.douban.com/tag/"+string+"?start="+str(i*20)+"&type=T" 
                        searchBook(getHtmlInfo(url),lis,liss)
                    print("书单表:\n\n")
                    print(liss)
                    print("\n\n\n\n\n\n")
                    string=str(input("请输入想查看的图书名称:"))
                    if string in lis.keys():
                        bookInfo(getHtmlInfo(lis[string]))
            if string =="电影":
                url="http://movie.douban.com/chart"
                movie(getHtmlInfo(url))
            if string =="音乐":
                url="http://music.douban.com/chart"
                music(getHtmlInfo(url))
            if string =="退出":
                break
                
main()
