import datetime
import os
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = "ACdc16ce57c4532d91713a090d2babe7f3"
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

alpha_api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
alpha_api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alpha_api_key
}
response = requests.get(url=STOCK_ENDPOINT, params=alpha_api_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

new_value = data_list[0]["4. close"]
old_value = data_list[1]["4. close"]
percent = ((float(new_value) - float(old_value)) / float(old_value)) * 100

formatted_articles = ""
if percent > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_api_key = os.environ.get("NEWS_API_KEY")
news_api_parameters = {
    "q": COMPANY_NAME,
    "pageSize": "3",
    "apikey": news_api_key
}
response = requests.get(url=NEWS_ENDPOINT, params=news_api_parameters)
response.raise_for_status()
news_data = response.json()["articles"][:3]

formatted_articles = [f"{STOCK}: {up_down}{round(percent)}%\nHeadline: {article['title']}." 
                      f"\nBrief: {article['description']}"
                      for article in news_data]
print(formatted_articles)

if percent > 5:
    for article in formatted_articles:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=article,
                from_='+19894798012',
                to='+32475862631'
            )
        print(message.status)
