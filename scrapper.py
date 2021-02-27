import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from bokeh.plotting import figure, show, output_file

"""Script created to scrap and analyze news and stock prices from Warsaw Stock Exchange. Data gathered from BiznesRadar.pl"""

class Scrapper:
    """Scrap stock prices and news from the Warsaw Stock Exchange"""

    def __init__(self, company):
        """Define the company."""
        self.company = company
        self.rolling_interval = [25,50,100]

    # Scrapping functions
    def prices_scrapper(self, days_prior):
        """Scrap stock prices using WSE code."""
        days_prior = int(days_prior) if days_prior != "" else 90
        date_included = pd.to_datetime(datetime.date.today() - datetime.timedelta(days = days_prior))
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
                    d["Date"] = datetime.datetime.strptime(temp[i],"%d.%m.%Y")
                    d["Open"] =float(temp[i+1])
                    d["Max"] = float(temp[i+2])
                    d["Min"] = float(temp[i+3])
                    d["Close"] = float(temp[i+4])
                    d["Volume"] = float(temp[i+5].replace(" ",""))
                    d["Value"] = int(temp[i+6].replace(" ",""))
                    stock_prices.append(d)
            
        df = pd.DataFrame(stock_prices)
        df = df.set_index("Date")
        df = df[df.index >= date_included]
        return df

    def news_scrapper(self, days_prior):
        """Scrap news about the company using WSE code."""

        days_prior = int(days_prior) if days_prior != "" else 90
        date_included = pd.to_datetime(datetime.date.today() - datetime.timedelta(days = days_prior))
        news_url = "https://www.biznesradar.pl/wiadomosci/"+company
        r = requests.get(news_url,
                        headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        page = int(soup.find_all("a", attrs={"class": "pages_pos"})[-1].text)

        news = []
        for page in range(1,int(page)+1):
            #print(news_url+","+str(page))
            r = requests.get(news_url+","+str(page), 
                    headers={'User-agent': 'Mozilla/6.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
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
                        n["Lead"] = lead.text.replace('\n','').replace('\t','').strip()
                    for source in col.find_all('a', attrs= {"class": "record-author"}):
                        n["Source"] = source.text
                    for date in col.find_all("span", attrs= {"class": "record-date"}):
                        n["Published"] = datetime.datetime.strptime(date.text,"%Y-%m-%d %H:%M:%S")
                    news.append(n)

        df=pd.DataFrame(news)
        df = df.set_index("Published")
        df = df[df.index >= date_included]
        return df

class StockAnalytics:
    """Basic stock analytics: simple moving average, expotential moving average."""

    def __init__(self,df):
        self.df = df

    def sma(self):
        """Simple moving average calculations - default at 25, 50, 100."""
        for interval in [25,50,100] :
            df["CloseSMA"+str(interval)] = df.Close.rolling(interval, min_periods =1).mean()
            df["OpenSMA"+str(interval)] = df.Open.rolling(interval, min_periods =1).mean()
        return df
    
    def ema(self):
        """Expotential moving average calculations."""
        df["CloseEMA"] = df.Close.ewm(alpha = 0.1, adjust = False).mean()
        df["OpenEMA"] = df.Open.ewm(alpha = 0.1, adjust = False).mean()
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
    
def status(df):
    df["Status"] = [inc_dec(c,o) for c,o in zip(df.Close, df.Open)]

def stock_plot(company,df):
    """Create a stock plot."""
    output_file(company+".html")
    d = figure(x_axis_type = "datetime", width = 1000, height = 300)
    hours_12 = 12 * 60 * 60 * 1000
    statuses = {'Increase': 'green', 
                'Decrease': 'red',
                'Equal':'grey'}

    for status, color in statuses.items():
        d.rect(df.index[df.Status == status], df.Middle[df.Status == status], hours_12, df.Height[df.Status == status], 
        fill_color = color, line_color = 'black')
    
    d.line(df.index, df.CloseSMA25, line_width=1, line_color='green')
    d.line(df.index, df.CloseSMA50, line_width=1, line_color='blue')
    d.line(df.index, df.CloseSMA100, line_width=1, line_color='black')
    show(d)
    return d

def news_analysis(df, news_df, days = 3):
    """Analytics of stock prices trend in the days following the publication."""
    #name cleanup
    news_df[pd.Series(news_df['Source']).str.contains(pat = 'Infostrefa')] = 'Infostrefa'

    #reset the index
    stock = df.reset_index(drop=False).copy()
    n_df = news_df.reset_index(drop=False).copy()

    stock.Date = pd.to_datetime(stock.Date)
    df = df[["Date","Open","Close"]]

    n_df["Date"]= pd.to_datetime(n_df.Published.dt.date)
    n_df = n_df[["Date","Source"]]

    #prices at the publication date
    publication = pd.merge(stock, n_df, on = "Date", how = 'inner')[["Source", "Date", "Open"]]

    #prices at the end of observation + 3 days
    publication["End_Date"] = publication.Date + datetime.timedelta(days)
    df_end = df[["Date","Close"]].copy()

    df_end.rename(columns = {"Date": "End_Date"}, inplace = True)
    news_prices = pd.merge(publication, df_end, on = "End_Date", how = 'inner')

    #status check
    status(news_prices)

    #counts of increase, decrease and total
    news_increase = news_prices[['Source','Status']].loc[news_prices.Status == 'Increase'].groupby(by = 'Source').count()
    news_decrease = news_prices[['Source','Status']].loc[news_prices.Status == 'Decrease'].groupby(by = 'Source').count()
    news_total = news_prices[['Source','Status']].groupby(by = 'Source').count()

    news_summary = pd.merge(news_total, news_increase, on = 'Source', how = 'left')
    news_summary = pd.merge(news_summary, news_decrease, on = 'Source', how = 'left')
    news_summary.rename(columns={'Source':'Source',
                                'Status_x': 'News_count',
                                'Status_y': 'Price_increase',
                                'Status': 'Price_decrease'}, inplace=True)
    #percentage count
    news_summary['Positive_pct'] = round(news_summary['Price_increase']/news_summary['News_count'] * 100)
    news_summary['Negative_pct'] = round(news_summary['Price_decrease']/news_summary['News_count'] * 100)
    news_summary = news_summary.fillna(0)

    #sorting of the df
    news_summary = news_summary.sort_values('News_count', ascending = False)

    return news_summary

try:
    company = input("Which company are you looking for?\n").upper()
    days_prior = input("How many prior calendar days you want to include? Default is 90 days. \n")
    df = Scrapper.prices_scrapper(company, days_prior)
    news_df = Scrapper.news_scrapper(company, days_prior)
except:
    print("Connection error. Please try again later.")

#simple moving average
StockAnalytics.sma(df)
StockAnalytics.ema(df)
status(df)
df["Middle"] = (df.Close+df.Open)/2
df["Height"] = abs(df.Open-df.Close)  

#print(df)
#print(news_df)

stock_plot(company, df)

print(news_analysis(df, news_df))