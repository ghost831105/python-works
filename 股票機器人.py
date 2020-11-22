# -*- coding: utf-8 -*-
import urllib.request as ur
import json
import pandas as pd

###############################################################################
#                     股票機器人 標準差分析（簡易板）                         #
###############################################################################

# 先與網站請求抓到價格
def getstock(stocknumber='1101'):
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20180814&stockNo=' + stocknumber 
    # url sjon格式
    with ur.urlopen(url) as response: 
        data = json.load(response) #response.read().decode('utf-8')
    
    # 判斷請求是否成功
    if data['stat'] != '很抱歉，沒有符合條件的資料!': 
        return data
    else:#請求失敗回傳空值
        return [] 

# 開始計算股票的平均以及標準差
def Standard_Deviation(stocknumber='1101'):
    stocklist = getstock(stocknumber)
    
    # 判斷是否為空值
    if len(stocklist) != 0:
        data = stocklist["data"]
        columns = stocklist["fields"]
        stockdf = pd.DataFrame(data, columns=columns)
        stockAverage = pd.to_numeric(stockdf['收盤價']).mean()
        stockSTD = pd.to_numeric(stockdf['收盤價']).std()
        stockname = stocklist["title"][8:15]
        # 看看這隻股票現在是否便宜（平均-兩倍標準差）
        buy='很貴不要買'
        if pd.to_numeric(stockdf['收盤價'][-1:]).values[0] < stockAverage - (2*stockSTD):
            buy = '這隻股票現在很便宜喔！'
            
        # 顯示結果
        print('股票: ', stockname)
        print('收盤價: ' + stockdf['收盤價'][-1:].values[0])
        print('\n中間價: ' + str(stockAverage))
        print('\n線距: ' + str(stockSTD))
        print(buy)
    else:
        print('請求失敗，請檢查您的股票代號')
       
Standard_Deviation(stocknumber='1101')