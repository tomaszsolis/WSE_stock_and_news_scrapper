

# Do news impact stock prices?

# Introduction & Goals
As I am investing on Warsw Stock Exchange (WSE), I noticed that price rises and drops coincide with some portals publishing positive or negative news more than others. I would like to investigate how most popular portals in Poland impact selected stock prices.

To do that I would like to answer the following questions:
1) Is it possible to react to news before they impact the prices? 
2) Are certain portal more negative or positive towards certain companies?
3) Is it possible to predict the general trend for stock prices based on the sentiment analysis of the news?

Data: 
    - biznesradar.pl not only has the information about the stock prices but also gathers the information from most important business news portals.

Tools:
    - Python - for webscrapping and analytics
    - Heroku - cloud platform to store the simple webpage containg the results for sample companies.

# Contents

- [Project Plan](#project-plan)
- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)

# Project Plan
Due to multiple options, I decided to split the project in 2 parts.

Analyze the trends for the stock price 1 week after the publication:
1) without analyzing the news itself
2) with analyzing the text (NLP)

# The Data Set
Data is scrapped from Biznesradar.pl and it consists of:
- stock prices (open, close, min, max, volume and value)
- news from main business portals (money.pl, infosfera, wnp.pl, bankier.pl, egospodarka.pl, portalspozywczy.pl, wirtualnemedia.pl and other similar).

I omit popular news portals like wp.pl, onet.pl and similar because of the lack of quality in business news.

# Used Tools

# Demo
1. Execute the file
2. Type in the company code (f.e. ALE for Allegro, CDR for CD Project Red etc).
3. Type in the number of prior calendar days to be included. Default value is set for 90 days to prevent messy information for companies which are present on the stock market for a long time. 
4. Enjoy the basic stock price graph with the main indicators (like SMA).
5. <work in progress> News analytics

# Conclusion

# Follow Me On
https://www.linkedin.com/in/tomaszsolis/
