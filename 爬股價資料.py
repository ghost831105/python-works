# -*- coding: utf-8 -*-
""" Topic： 抓取股價 """
# =============================================================================
# 目標：包成函式重複呼叫，啟動定時器，定時(每分鐘)觸發爬蟲取得最新股價資訊
# =============================================================================
def getStockInfo(StockCode):
    # 組成stock_list
    stock_list   = '|'.join('tse_{}.tw'.format(target) for target in StockCode) 
    
    # 取得資料
    import urllib.request as ur
    import json
    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + stock_list
    
    with ur.urlopen(url) as response:
        data = json.load(response) #取得網路原始碼 json格式
                #response.read().decode('utf-8')  HTML讀取
    
    # 取出需要欄位
    import pandas as pd
    columns = ["c","n","z","tv","v","o","h","l","y"]
    df = pd.DataFrame(data["msgArray"], columns = columns)
    df.columns = ["股票代號","公司簡稱","當盤成交價","當盤成交量","累積成交量",
                  "開盤價","最高價","最低價","昨收價"]
    df.insert(9, "漲跌百分比", 0.0)
    
    # 新增漲跌百分比
    for i in range(len(df.index)):  #len(df.index)可得到row數
        if df['當盤成交價'].iloc[i] != "-":
            df.iloc[i,2:9] =  df.iloc[i,2:9].astype(float) #與一般使用方式不同，2:9 包含 2跟9
            df.loc[df.index[i],"漲跌百分比"] =(df.當盤成交價[i] - df.昨收價[i]) / df.昨收價[i] * 100 
    
    # 新增時間、日期
    import time
    df.insert(10,"Day",time.strftime("%Y:%m:%d", time.localtime(time.time())))
    df.insert(11,"Time",time.strftime("%H:%M:%S", time.localtime(time.time())))
    
    return df


import sched
import time

StockCode = [1101,2330,1103]
schedule = sched.scheduler( time.time,time.sleep)
def event_func(StockCode): #得到股票資訊
    print("Time is: " ,time.strftime("%H:%M:%S", time.localtime(time.time())))
    print(getStockInfo(StockCode))
def perform(delay_time): #重複執行
    schedule.enter(delay_time, 0, perform,argument = (delay_time,))
    event_func(StockCode)
    
if __name__=='__main__':
    perform(60) 
    schedule.run()
    