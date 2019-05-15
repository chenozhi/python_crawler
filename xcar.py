from bs4 import BeautifulSoup
from operator import attrgetter
import requests
import re
import os
import time
import  sqlite3 as sql



#定义一个cookie字典,用于传递到对方服务器
def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict


webPrefix = "www.xcar.com.cn"
cookie = "TY_SESSION_ID=5161db72-38a7-4936-aee6-5388d4fe8c3d; _Xdwuv=5444177068682; _PVXuv=5c0df1a5758f7; bbs_cookietime=31536000; bdshare_firstime=1555479648073; Hm_lvt_53eb54d089f7b5dd4ae2927686b183e0=1554685003,1555290086,1555300755,1555987037; _Xdwnewuv=1; _fwck_www=58cd4d57c66bf862fdef9f59ba2b9db9; _appuv_www=a83f70c3d4a5d218ad388dfe812908b3; _fwck_my=7a2a0efe10e2a99c4bcc9c012f26b9ee; _appuv_my=24cf7e3c56e42ac84333f9e52d507c23; fw_pvc=1%3A1556414067%3B1%3A1556414085%3B1%3A1556414089%3B1%3A1556414090%3B1%3A1556414440; fw_slc=1%3A1556414435%3B1%3A1556414437%3B1%3A1556414441%3B1%3A1556414442%3B1%3A1556414446; fw_exc=1%3A1556414086%3B1%3A1556414087%3B1%3A1556414094%3B1%3A1556414098%3B1%3A1556414494; fw_clc=1%3A1556414080%3B1%3A1556414086%3B1%3A1556414494%3B1%3A1556420272%3B1%3A1556423299; ad__city=386; uv_firstv_refers=http%3A//www.xcar.com.cn/bbs/forumdisplay.php%3Ffid%3D46; _discuz_uid=8822957; _discuz_pw=5741a1f9bccb40408e4e57a0dcba3923; _xcar_name=TheBigBang; _discuz_vip=0; bbs_auth=BBnhtVN4%2FBYPYyN1vZYTvV5it3%2BO7h7vNHbe7sLfACgM2GTxtbNdrYbRI0qkaFNBCA; bbs_sid=HxhVuZ; bbs_visitedfid=46D1109D91D43D114D1588D44D456D120D1783D53D255D1292; _Xdwstime=1556433790; Hm_lpvt_53eb54d089f7b5dd4ae2927686b183e0=1556433811"

class LineInfo:
    def __init__(self, content, clickcount, replycount):
            self.content = content
            self.clickCount = clickcount
            self.replyCount = replycount

    def __repr__(self):
            return repr((self.content, self.clickCount, self.replyCount))

postList = []
dict = {}
header = {'content-type': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
index = 0
fRecord = open("postRecord.txt", "wb")
for i in range(271):
    resp = requests.post(url='http://www.xcar.com.cn/bbs/forumdisplay.php?fid=46&page=%d' %(i+1), headers=header, cookies=cookie_to_dict(cookie))
    resp.encoding='utf-8'
    html=resp.text

    # fo = open("page%d.txt" % (i+1), "rb")
    # html = fo.read()
    # # 关闭打开的文件
    # fo.close()

    soup = BeautifulSoup(html,'lxml')
    # 数据库
    # conn = sql.connect('xcar.db')
    # cursor = conn.cursor()
    # cursor.execute('create table IF NOT EXISTS april (id INTEGER primary key AUTOINCREMENT,postdate VARCHAR(20),author VARCHAR(40),title VARCHAR,clickcount INTEGER,replycount INTEGER,link VARCHAR)')

    #通过tag的ID属性查找
    itemList = soup.find_all('dl', class_='list_dl')

    for itemdl in itemList:
        if(itemdl.find('span',class_= 'tdate') == None):
            continue
        attrs = itemdl.find_all('a',target="_blank",class_="linkblack") #获取这个标签下所有的a属性,只保留target,class这个条件的，后续按照索引查找
        #格式: 编号 日期 作者 标题 链接  itemdl.a是直接获取第一个字符串内容,就是标题,而作者需要通过数组来获取。因为有多个a href的标签，需要过滤下
        replyCount = itemdl.find('span',class_='fontblue').string
        clickCount = itemdl.find('span',class_='tcount').string
        postDate = itemdl.find('span',class_='tdate').string
        postAuthor = attrs[0].string
        postTitle = itemdl.find('a',class_="titlink").string
        postUrl = itemdl.find('a',class_="titlink").get("href")
        postID = postUrl.split('=')[1]
        #过滤掉本月之前的帖子
        postDateNow = time.strptime(postDate, "%Y-%m-%d")
        postDateMin = time.strptime("2019-01-01", "%Y-%m-%d")
        postDateMax = time.strptime("2019-05-15", "%Y-%m-%d")
        if(postDateNow < postDateMin or postDateNow > postDateMax):
            continue

        line = '%d' %(index+1) + "\t" + postDate + "\t" + postAuthor + "\t" + postTitle + "\t" + clickCount + "\t" + replyCount + "\t" + webPrefix + postUrl
        lineinfo = LineInfo(line, int(clickCount),int(replyCount))

        #cursor.execute("insert into april (id,postdate,author,title,clickcount,replycount,link) values (null,'%s','%s','%s','%s','%s','%s')"%(postDate,postAuthor,postTitle, clickCount,replyCount,webPrefix + postUrl))
        # cursor.execute(
        #     'INSERT INTO april (id,postdate,author,title,clickcount,replycount,link) values (null,?,?,?,?,?,?)',(postDate,postAuthor,postTitle, clickCount,replyCount,webPrefix + postUrl))
        # # 提交事务:
        # conn.commit()
        #postList.append(lineinfo)

        print(line)
        fRecord.write(str.encode(line + '\r\n'))

        index += 1

fRecord.close()
# # 关闭Cursor:
# cursor.close()
#
# # 关闭Connection:
# conn.close()


#降序
# newlist = sorted(postList, key=attrgetter('replyCount'), reverse=True)
#
#
#
# for i in range(len(newlist)):
#     print(newlist[i])

