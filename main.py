import html

import requests
import smtplib
from api import *
stocks_api_key = stock_key
news_api_key = news_key


# STEP 1: Use https://www.alphavantage.co
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={stocks_api_key}'

r = requests.get(url)
data = r.json()


prices = data["Time Series (Daily)"]
close_list = list(prices.items())
close_list_final = list(close_list[0:2])
today_close = float(close_list_final[0][1]["4. close"])
yester_close = float(close_list_final[1][1]["4. close"])


change = round(today_close - yester_close, 2)
change_perc = round((change / today_close) * 100, 2)

# STEP 1: Use https://www.alphavantage.co

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


def get_news():
    news_url = ("https://newsapi.org/v2/everything?"
                "q=tesla&from=2023-07-17&sortBy=publishedAt&apiKey=1d29379d6ccb4e0f94db6440b5bb2cf9"
                "&language=en")
    req = requests.get(news_url)
    news_data = req.json()

    news_articles = {
        "first_article": {
            "Headline": html.unescape(news_data["articles"][0]["title"]),
            "Brief": html.unescape(news_data["articles"][0]["description"]),
            "url": html.unescape(news_data["articles"][0]["url"])
        },
        "second_article": {
            "Headline": html.unescape(news_data["articles"][1]["title"]),
            "Brief": html.unescape(news_data["articles"][1]["description"]),
            "url": html.unescape(news_data["articles"][1]["url"])
        },

        "third_article": {
            "Headline": html.unescape(news_data["articles"][2]["title"]),
            "Brief": html.unescape(news_data["articles"][2]["description"]),
            "url": html.unescape(news_data["articles"][2]["url"])
        }
    }
    return news_articles


if change_perc < -5 or change_perc > 5:

    articles = get_news()
    article1 = "first_article"
    article2 = "second_article"
    article3 = "third_article"
    headline_string = "Headline"
    brief_string = "Brief"
    url_string = "url"

    if change_perc > 5:
        change_perc_string = f"🔺{change_perc}%"
    elif change_perc < -5:
        change_perc_string = f"🔻{change_perc}%"

    MESSAGE = (f"Subject: {COMPANY_NAME} \n\n"
               f"{STOCK}{change_perc_string}\n"
               f"\nHeadline: {articles[article1][headline_string]}. (TSLA)?.\n"
               f"Brief: {articles[article1][brief_string]}\n"
               f"url: {articles[article1][url_string]}\n"
               f"\n"
               f"Headline: {articles[article2][headline_string]}. (TSLA)?.\n"
               f"Brief: {articles[article2][brief_string]}\n"
               f"url: {articles[article2][url_string]}\n"
               f"\n"
               f"Headline: {articles[article3][headline_string]}. (TSLA)?.\n"
               f"Brief: {articles[article3][brief_string]}\n"
               f"url: {articles[article3][url_string]}\n")

    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=email_from, password=email_password)
    connection.sendmail(from_addr=email_from, to_addrs=email_to,
                        msg=MESSAGE.encode("utf-8")
                        )
    connection.close()

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""