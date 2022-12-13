import os
import random

import requests
import telebot
from bs4 import BeautifulSoup


API_KEY = os.environ.get("API_KEY")
URL = "https://paper-trader.frwd.one/"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi, enter the pair you want to trade (BTCUSDT, ETHUSDT...)")


@bot.message_handler(content_types=["text"])
def send_img(message):
    img = get_image_url(message.text)
    if img:
        bot.send_photo(message.chat.id, img)
    else:
        bot.send_message(message.chat.id, "Please enter correct data or /help to see rules.")


def get_image_url(message):
    timeframe_list = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]

    timeframe = random.choice(timeframe_list)
    candles = str(random.randint(1, 1000))
    period = str(random.randint(1, 51))
    profit = str(random.randint(1, 101))
    loss = str(random.randint(1, 101))

    data = {
        "pair": message,
        "timeframe": timeframe,
        "candles": candles,
        "ma": period,
        "tp": profit,
        "sl": loss,
    }
    response = requests.post(URL, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img")
    return URL + image.get("src")


bot.polling(none_stop=True)
