import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from bokeh.plotting import figure, show, output_file

"""Script created to scrap and analyze news and stock prices from Warsaw Stock Exchange. Data gathered on BiznesRadar.pl"""

# Scrapping functions
def prices_scrapper(company):
    """Scrap stock prices using WSE code."""

    stock_url = "https://www.biznesradar.pl/notowania-historyczne/"+company
    r = requests.get(stock_url,
                    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    page = int(soup.find_all("a", {"class": "pages_pos"})[-1].text)

    
    stock_prices=[]
    for page in range(1,int(page)+1):
        #print(stock_url+","+str(page))
        r = requests.get(stock_url+","+str(page), 
                        headers={'User-agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        table = soup.find_all("table", {"class": "qTableFull"})
        for row in table:
            temp=[]
            for col in row.find_all('td'):
                temp.append(col.text)
            for i in range(0,len(temp),7):
                d = {}
                d["Date"] = datetime.datetime.strptime(temp[i],'%d.%m.%Y')
                d["Open"] =float(temp[i+1])
                d["Max"] = float(temp[i+2])
                d["Min"] = float(temp[i+3])
                d["Close"] = float(temp[i+4])
                d["Volume"] = float(temp[i+5].replace(" ",""))
                d["Value"] = int(temp[i+6].replace(" ",""))
                stock_prices.append(d)
         
    df=pd.DataFrame(stock_prices)
    df = df.set_index("Date")
    return df

def news_scrapper(company):
    """Scrap news about the company using WSE code."""
    
    news_url = "https://www.biznesradar.pl/wiadomosci/"+company
    r = requests.get(news_url,
                    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    page = int(soup.find_all("a", attrs={"class": "pages_pos"})[-1].text)

    news=[]
    for page in range(1,int(page)+1):
        #print(news_url+","+str(page))
        r = requests.get(news_url+","+str(page),headers={'User-agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        table = soup.find_all("div", attrs={"id": "news-radar-body"})
        for row in table:
            for col in row.find_all('div', attrs={'class': 'record record-type-NEWS'}):
                n={}
                for title in col.find_all('div', attrs={'class': "record-header"}):
                    n["Title"] = title.text.replace('\n','').strip()
                    for link in title.find_all('a',href=True):
                        n["Link"] = link.get('href')
                for lead in col.find_all('div', attrs= {"class": "record-body"}):
                    n["Lead"]=lead.text.replace('\n','').replace('\t','').strip()
                for source in col.find_all('a', attrs= {"class": "record-author"}):
                    n["Source"]=source.text
                for date in col.find_all("span", attrs= {"class": "record-date"}):
                    n["Published"] = date.text
                news.append(n)

    df=pd.DataFrame(news)
    return df

# Analytics
def inc_dec(c,o):
    if c > o:
        value = "Increase"
    elif c < o:
        value = "Decrease"
    else:
        value = "Equal"
    return value

def sma(rolling_interval):
    df["CloseSMA"+str(rolling_interval)] = df.Close.rolling(rolling_interval, min_periods =1).mean()
    df["OpenSMA"+str(rolling_interval)] = df.Open.rolling(rolling_interval, min_periods =1).mean()

company = input("Which company are you looking for?: ")

df = prices_scrapper(company)
news_df = news_scrapper(company)

df["Status"] = [inc_dec(c,o) for c,o in zip(df.Close, df.Open)]
df["Middle"] = (df.Close+df.Open)/2
df["Height"] = abs(df.Open-df.Close)

#simple moving average
sma(20)
sma(50)
sma(100)

#expotential moving average
df["CloseEMA"] = df.Close.ewm(alpha = 0.1, adjust = False).mean()
df["OpenEMA"] = df.Open.ewm(alpha = 0.1, adjust = False).mean()

#print(df)
print(news_df)

d = figure(x_axis_type = "datetime", width = 1000, height = 300)

hours_12 = 12 * 60 * 60 * 1000

statuses = {'Increase': 'green', 
            'Decrease': 'red',
            'Equal':'grey'}

for status, color in statuses.items():
    d.rect(df.index[df.Status == status], df.Middle[df.Status == status], hours_12,df.Height[df.Status == status], 
    fill_color = color, line_color = 'black')
    
output_file(company+".html")
show(d)