
!pip3 install python-firebase

import requests 
from bs4 import BeautifulSoup
import pandas as pd

from firebase import firebase

def get_news(url_page): #中時電子報
  url = 'https://final-40cb2.firebaseio.com/'
  fb = firebase.FirebaseApplication(url, None)
  page = 1
  r = requests.get(url_page)
  web_content_taiwan = r.text
  soup_taiwan = BeautifulSoup(web_content_taiwan,'lxml')   
  count = soup_taiwan.find('span', class_='search-result-count').text.replace(",","")
  print(count)
  page_max = int(int(count) / 20)
  url_to_news = []
  list_news = []
  list_author = []
  key = []
  keyword_list = []
  while page <= page_max:
    print("page:%d"%page)
    url_to_page = [url_page.replace('chdtv',''), str('page='), str(page), '&chdtv']
    url_to_page = ''.join(url_to_page)
    r_taiwan = requests.get(url_to_page)
    web_content_taiwan = r_taiwan.text
    soup_taiwan = BeautifulSoup(web_content_taiwan,'lxml')

    news_taiwan = soup_taiwan.find_all('div', class_='col') #擷取新聞資訊

    title = soup_taiwan.find_all('h3', class_='title') #擷取新聞標題
    titles = [t.find('a').text for t in title]

    time = soup_taiwan.find_all('span', class_='date') #擷取新聞時間
    times = [t.string for t in time]
    class_taiwan = soup_taiwan.find_all('div', class_='category') #擷取新聞類別
    classes = [c.find('a').text for c in class_taiwan]

    website = soup_taiwan.find_all('h3', class_='title') #擷取新聞網址
    w = [t.find('a') for t in website]    
    websites = [web.get('href') for web in w]

    #打開新聞網址
    i = 0
    while i < 20 :
      url_to_news.append(websites[i])
      r = requests.get(websites[i])
      web_content_news = r.text
      soup_news = BeautifulSoup(web_content_news,'lxml')
      news = soup_news.find("meta",  property="og:description")["content"]
      list_news.append(news)
      author_news = soup_news.find_all('div', class_='author') #擷取新聞記者

      try:
        key = soup_news.find("meta",{"itemprop":"keywords"})["content"]
      except:
        key = ""
      else:
        key = soup_news.find("meta",{"itemprop":"keywords"})["content"]

      keyword_list.append(key)

      for a in author_news:
        if a.find('a'):
          author = a.find('a').text
        else:
          author = a.text.replace(" ","").replace("\n","")
      list_author.append(author)
      i = i + 1     
    page = page + 1

    for i in range(1,len(titles)):
      print(titles[i],url_to_news[i],classes[i],keyword_list[i],list_author[i])
      fb.post('/FinalProject/',{"title":titles[i],"time":times[i],"category":classes[i],"url":url_to_news[i],"content":list_news[i],"author":list_author[i],"keyword":keyword_list[i]})
    keyword_list = []
    list_news = []
    list_author = []
    url_to_news = []


#get_news('https://www.chinatimes.com/search/%E5%8F%B0%E7%81%A3?chdtv') #關鍵字：台灣 page111 500 ~ 3755
#print("台灣 completed")

#get_news('https://www.chinatimes.com/search/%E9%9F%93%E5%9C%8B?chdtv') #關鍵字：韓國
#print("韓國 completed")
#get_news('https://www.chinatimes.com/search/%E5%B0%8F%E4%B8%89?chdtv') #關鍵字：小三
#print("小三 completed")
#get_news('https://www.chinatimes.com/search/%E9%81%8B%E5%8B%95?chdtv') #關鍵字：運動
#print("運動 completed")
#get_news('https://www.chinatimes.com/search/%E8%BB%8A%E7%A6%8D?chdtv') #關鍵字：車禍
#print("車禍 completed")
#get_news('https://www.chinatimes.com/search/%E7%BE%8E%E5%9C%8B?chdtv') #關鍵字：美國
#print("美國 completed")
#get_news('https://www.chinatimes.com/search/%E4%B8%AD%E5%9C%8B?chdtv') #關鍵字：中國 page2383
#print("中國 completed")

#below COMPLETED
#get_news('https://www.chinatimes.com/search/%E8%94%A1%E8%8B%B1%E6%96%87?chdtv') #關鍵字：蔡英文
#print("蔡英文 completed")
#get_news('https://www.chinatimes.com/search/%E7%B8%BD%E7%B5%B1?chdtv') #關鍵字：總統
#print("總統 completed")
#get_news('https://www.chinatimes.com/search/%E6%97%A5%E6%9C%AC?chdtv') #關鍵字：日本 #150
#print("日本 completed")
#get_news('https://www.chinatimes.com/search/%E7%A7%91%E6%8A%80?chdtv') #關鍵字：科技
#print("科技 completed")
#get_news('https://www.chinatimes.com/search/%E9%81%B8%E8%88%89?chdtv') #關鍵字：選舉
#print("選舉 completed")

#get_news('https://www.chinatimes.com/search/%E5%9C%B0%E9%9C%87?chdtv') #關鍵字：地震
#print("地震 completed")

get_news('https://www.chinatimes.com/search/%E9%86%AB%E9%99%A2?chdtv') #關鍵字醫院
print("醫院 completed") 



