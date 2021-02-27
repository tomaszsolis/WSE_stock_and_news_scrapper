

# Do news impact stock prices?

# Introduction & Goals
As I am investing on Warsw Stock Exchange (WSE), I noticed that price rises and drops coincide with some portals publishing positive or negative news more than others. I would like to investigate how most popular portals in Poland impact selected stock prices.

To do that I would like to answer the following questions:
1) Is it possible to react to news before they impact the prices? 
2) Are certain portal more negative or positive towards certain companies?

Data: 
    - biznesradar.pl not only has the information about the stock prices but also gathers the information from most important business news portals.

Tools:
    - Python - for webscrapping and analytics

# Contents

- [Project Plan](#project-plan)
- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
- [Guide](#guide)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)

# Project Plan
Due to multiple options, I decided to split the project in 2 parts.

Analyze the trends for the stock price 3 days after the publication (parameter can be changed) after the publication without analyzing the news text.

# The Data Set
Data is scrapped from Biznesradar.pl and it consists of:
- stock prices (open, close, min, max, volume and value)
- news from main business portals (money.pl, infosfera, wnp.pl, bankier.pl, egospodarka.pl, portalspozywczy.pl, wirtualnemedia.pl and other similar).

I omit popular news portals like wp.pl, onet.pl and similar because of the lack of quality in business news.

# Used Tools
Python :)

# Guide
1. Execute the file
2. Type in the company code (f.e. allegro for Allegro, cd-projekt for CD Project Red etc). Letter size doesn't matter.
3. Type in the number of prior calendar days to be included. Default value is set for 90 days to prevent messy information for companies which are present on the stock market for a long time (20+ years)
4. Enjoy the stock price graph with the main indicators (like SMA).
5. Identify the most reliable news sources based on the price movement after the publication. 

# Demo

CD Project Red analysis

1. Run the script
2. Type in the company code
    -> type in cd-projekt
3. Type in the number of prior calendar days to be included.
    -> 365
4. Enjoy the stock price graph with the main indicators (like SMA).
5. Identify the most reliable news sources based on the price movement after the publication. 
    -> you will be presented a table with:
    - a news portal,
    - number of publications about a given company
    - number of news with price increase in the next 3 calendar days
    - number of news with price decrease in the next 3 calendar days
    - percentage of news with the price increase
    - percentage of news with the price decrease

# Conclusion

It turns out that news published in some media more often that others result in stock price drop.
Is it fair? No. 
So why does it happen? Internet media are driven by clicks. negative news are more clickable than positive ones. So every publisher tries to beat the others. Even most respectable portals fall for such issue. That's why it is crucial to pick the source for your news wisely (not only for investing).

But it is possible to react to the news on a certain portal given you know the sentiment of the portal towards a company. To fill in all the blanks and fully understand how positive/negative the news is, a more comprehensive sentiment analysis should be done. I have included the links to the news in the news scrapping part of the code. Current project will be expanded in the future to include NLP analysis using Naive Bayes classifier and Neural Networks. 

# Follow Me On
https://www.linkedin.com/in/tomaszsolis/
