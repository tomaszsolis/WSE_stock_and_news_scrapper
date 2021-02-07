import requests
from bs4 import BeautifulSoup
import pandas

"""Script created to scrap news and stock prices from Warsaw Stock Exchange. Data gathered on BiznesRadar.pl"""

def prices_scrapper(company):
    """Scrap stock prices using WSE code."""

    stock_url = "https://www.biznesradar.pl/notowania-historyczne/"+company
    r = requests.get(stock_url,
                    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    page = int(soup.find_all("a", {"class": "pages_pos"})[-1].text)

    temp=[]
    stock_prices=[]
    for page in range(1,int(page)+1):
        #print(stock_url+","+str(page))
        r = requests.get(stock_url+","+str(page), 
                        headers={'User-agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        table = soup.find_all("table", {"class": "qTableFull"})
        for row in table:
            for col in row.find_all('td'):
                temp.append(col.text)
            for i in range(0,len(temp),7):
                d = {}
                d["Date"] = temp[i]
                d["Open"] =float(temp[i+1])
                d["Max"] = float(temp[i+2])
                d["Min"] = float(temp[i+3])
                d["Close"] = float(temp[i+4])
                d["Volume"] = float(temp[i+5].replace(" ",""))
                d["Value"] = int(temp[i+6].replace(" ",""))
                stock_prices.append(d)
         
    df=pandas.DataFrame(stock_prices)
    return df

def news_scrapper(company):
    """Scrap news about the company using WSE code."""
    
    news_url = "https://www.biznesradar.pl/wiadomosci/"+company
    r = requests.get(news_url,
                    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    page = int(soup.find_all("a", {"class": "pages_pos"})[-1].text)

    news=[]
    for page in range(1,int(page)+1):
        #print(news_url+","+str(page))
        r = requests.get(news_url+","+str(page),headers={'User-agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        table = soup.find_all("div", {"id": "news-radar-body"})
        for row in table:
            for col in row.find_all('div',{'class': 'record record-type-NEWS'}):
                n={}
                for title in col.find_all('div', {'class': "record-header"}):
                    n["Title"] = title.text.replace('\n','').strip()
                for lead in col.find_all('div', {"class": "record-body"}):
                    n["Lead"]=lead.text.replace('\n','').replace('\t','').strip()
                for source in col.find_all('a', {"class": "record-author"}):
                    n["Source"]=source.text
                for date in col.find_all("span",{"class": "record-date"}):
                    n["Published"] = date.text
                news.append(n)

    df=pandas.DataFrame(news)
    return df

company = input("Which company are you looking for?: ")

print(prices_scrapper(company))
print(news_scrapper(company))