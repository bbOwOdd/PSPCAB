#**
#Copyright 2021 國立台北科技大學. All rights reserved. 
#File: get_cmoney_stock_ver1_one.py 
#Author: 健修 
#Date: 2021/01/27
#Version: 1.0 
#Since: python 3.7.6 64-bit
#Desc:爬取cmoney版內文章，此程式為抓取單一股票
#Output:None
#**

import requests
from bs4 import BeautifulSoup
import pandas as  pd
import time
import configparser
import csv

def get_api2_article(url_cmoney_api_2, channelId, articleId, end_time):
    article_end = True
    url_cmoney_api_2  = url_cmoney_api_2.replace('baseini.channelId', channelId)
    while article_end:
        
        #串api2
        try:
            url_cmoney_api_2_new = url_cmoney_api_2.replace('baseini.articleId', articleId)
            api_2 = requests.get(url_cmoney_api_2_new, verify = False).json()
        except:
            articleId = str(int(articleId) + 1)
            print('error')
            continue
        
        if len(api_2) != 0 :
            for article_data in api_2:
                if article_data["ArtCteTm"].find(end_time) == -1:
                    #response資料中的 ArtCtn為html因此使用BeautifulSoup解析
                    soup = BeautifulSoup(article_data["ArtCtn"], "lxml")
                    #每個留言都會有跟這篇留言相關的股票
                    related_stock = soup.find_all("a", class_= "stock")
                    #取出每個股票
                    stockList = [stock.contents for stock in related_stock]
                    #print(stockList)
                    #for s in stockList:
                        #因為s為只有一筆資料的list 如['台積電'] 因此s[0]直接取出
                        #print(s[0])

                    #取出留言切掉<div>等標籤留下內容
                    article = str(soup.find("div", class_="main-content"))
                    article_index_start = article.index('<div class="main-content">') + len('<div class="main-content">') 
                    article_index_end = article.index('</div>') 
                    article = article[article_index_start : article_index_end]
                    article = article.replace("<br/>", " ")
                    print("留言者Id:", article_data['ChlId'], "留言者暱稱: ", article_data['ChlCap'],"留言者等級: ", article_data['MemberLevel'], "留言者讚數: ",article_data['ArtLkdCnt'], "留言者被回應數: ",article_data['ArtRepdCnt'])
                    #print(channelId)
                    print(articleId)
                    print(article)
                    print(article_data["ArtCteTm"])
                    print("==========")
                    articleId = article_data["ArtId"]

                    data_list = [article_data["ArtCteTm"], stockName, article_data['ChlCap'], article_data['MemberLevel'], article_data['ArtLkdCnt'], article_data['ArtRepdCnt'], articleId, article ]
                    with open('./senior project/crawler/2603_test.csv', 'a', newline='', encoding='utf_8_sig') as f:
                        csv_write = csv.writer(f)
                        data_row = data_list
                        csv_write.writerow(data_row)
                else:
                    #到達日期結尾則break
                    print("datetime end!")
                    article_end = False
                    break
        else:
            #已擷取到結尾
            print("api end!")
            articleId = str(int(articleId) - 1)
            print(articleId)
            continue      
            #article_end = False

#================main==================

#取得base.ini檔
config = configparser.ConfigParser() ##讀取設定檔
config.read('./senior project/crawler/base.ini',encoding="utf-8-sig")
url_cmoney_stock_web = config['owner'].get('cmoney_stock_web').strip() ##股市爆料同學會url
url_cmoney_api_1 = config['owner'].get('cmoney_api_1').strip() #api1
url_cmoney_api_2 = config['owner'].get('cmoney_api_2').strip() #api2
end_time = config['owner'].get('end_time').strip()#想要結束的時間2021回推(ex想要取到2021~2015年則設為2014)

stockName = '長榮2603'
#搜尋不到該股票就不做
if stockName != None:
    #取得channelId以利之後api1使用
    channelId = '103298' #長榮
    #取得channelId之後串api1
    url_cmoney_api_1 = url_cmoney_api_1.replace('baseini.channelId', channelId)
    api_1 = requests.get(url_cmoney_api_1, verify = False).json()
    #取得第一筆的articleId就ok了，代表最新的留言的id
    articleId = api_1[0]['ArtId']
    #取得articleId使用api2開始爬資料
    print(channelId)
    print(articleId)
    first_line = ['Time', 'stockName', '留言者ID', '留言者等級', '留言讚數', '被回應數', 'AarticleID', '留言' ]
    with open('./senior project/crawler/2603_test.csv', 'w' , newline='', encoding='utf_8_sig') as f:
        csv_write = csv.writer(f)
        first_row = first_line
        csv_write.writerow(first_row)
    #start
    get_api2_article(url_cmoney_api_2, channelId, articleId, end_time)
else:
    print("找不到該股票")
