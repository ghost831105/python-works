# -*- coding: utf-8 -*-
# =============================================================================
#  小程式：抓取PTT八卦版三、五頁的文章標題，並輸出成Gossip_titles.txt          #
# =============================================================================
def getdata(url, Gos_title = ""):
    
    # 獲取原始碼
    import urllib.request as req
    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        "Cookie":"over18=1"
        })
    with req.urlopen(request) as response:
        rec = response.read().decode('utf-8')
        
    # 讀取原始碼並篩出需要資料
    import bs4
    root = bs4.BeautifulSoup(rec, "html.parser")
    
        # 篩標題並存入變數中
    titles = root.find_all("div", class_='title')
    for title in titles:
        if title.a != None:
            #print(title.a.string)
            Gos_title = Gos_title + title.a.string + "\n"
        
        # 篩超連結
    nextLink = root.find('a', string = "‹ 上頁")
    # print(nextLink)
    return [nextLink["href"], Gos_title]

pageURL = "https://www.ptt.cc/bbs/Gossiping/index39577.html"
page = 1 
getpage = 4
while page <= getpage:
    if page==1 :
        Gos_titles= ""
    result = getdata(pageURL)
    pageURL = "https://www.ptt.cc" + result[0]
    Gos_titles = Gos_titles + f"page: {page}\n" + result[1]
    page += 1

Gos_titles = f"[PTT八卦版之文章標題]  Total pages:{getpage}\n" + Gos_titles

 # 輸出結果
with open("Gossip_titles.txt", mode="w", encoding="utf-8") as file:
        file.write(Gos_titles)
