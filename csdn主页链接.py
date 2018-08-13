# -*- coding: utf-8 -*-
import urllib.request
import os
import re
data=urllib.request.urlopen('https://www.csdn.net').read()
data.decode('utf-8')
if os.path.exists('D:/workHtml/')==False:
    print('\n-------------------------------------\n')
    print('创建目录：D:/workHtml/\n')
    print('-------------------------------------\n\n\n')
    os.mkdir('D:/workHtml/')
with open('D:/workHtml/csdn.html','wb') as f:
    f.write(data)
arr=re.compile('<a href=\"(.+?)\"').findall(str(data))
for index in range(len(arr)):
    if 'http' not in arr[index]:
        arr[index]='https://www.csdn.net'+arr[index]
arr=list(set(arr))
for i in arr:
    print(i)
i=1
for href in arr:
    data = urllib.request.urlopen(href).read()
    with open('D:/workHtml/'+str(i)+'.html', 'wb') as f:
        f.write(data)
        print('已保存'+str(i)+'个文件到  D:/workHtml/')
    i+=1
print('-------------------------------------')
print('\n\n文件已保存在D:/workHtml/,请查收~\n\n')
print('-------------------------------------')
