# -*- coding: utf-8 -*-
import urllib.request
import re
import os
if os.path.exists('D:/校花image/')==False:
    os.mkdir('D:/校花image/')
htmlString=urllib.request.urlopen('http://www.xiaohuar.com/2014.html').read().decode('utf-8','ignore')
linkList=re.compile('img width="210"  alt="(.*?)" src="(.*?)"').findall(htmlString)
i=0
for tup in linkList:
    try:
        url=tup[1]
        if 'http' not in url:
            url='http://www.xiaohuar.com'+url
        urllib.request.urlretrieve(url,filename='D:/校花image/'+str(i)+'.jpg')
        i+=1
        print('\r保存图片到D:/校花image/  进度:{:.2f}%'.format(i*100/120),end='')
    except:
        continue
