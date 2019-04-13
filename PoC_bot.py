import telebot
import logging
from telebot import types
import requests

bot = telebot.TeleBot('720667306:AAEn59qDt097495MjG9gevRkRrDDSFd9NIk', threaded=False)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
API_TOKEN = "6034d87efaa342b60bd74f470f24eb86"

SERVER_URL = "https://test-weather-the-best.herokuapp.com"


@bot.message_handler(commands=['start'])
def send_welcome(message):
   bot.reply_to(message, "Дороу")


@bot.message_handler(commands=['help'])
def send_welcome(message):
   bot.reply_to(message, "Бог в помощь")


@bot.message_handler(commands=['location'])
def location(message):
   keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   button_geo = types.KeyboardButton(text="Send de way", request_location=True)
   keyboard.add(button_geo)
   bot.send_message(message.chat.id, "Do u now de way", reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
   url = requests.get(f'http://api.openweathermap.org/data/2.5/weather?'
                      f'lat={message.location.latitude}&lon={message.location.longitude}&appid={API_TOKEN}').json()
   bot.send_message(message.chat.id, text=f'{url.get("name")}, {url.get("main").get("temp")}')

   #f'{url.get("name")}, {url.get("main").get("temp")}


@bot.message_handler(content_types=["city"])
def location(message):
   print(message)
   # city = message
   # "/weather/{}".format(city)
   # "".format(SERVER_URL,)


   # url = requests.get().json()
   # bot.send_message(message.chat.id, text=f'{url.get("name")}, {url.get("main").get("temp")}')

   #f'{url.get("name")}, {url.get("main").get("temp")}


@bot.message_handler(func=lambda message: True)
def echo_message(message):
   city = message.text


   url = "{}{}".format(SERVER_URL, "/weather/{}".format(city))

   try:
      resp = requests.get(url).json()
   except Exception as exc:
      print(exc)
      raise

   bot.send_message(message.chat.id, text=f'{resp.get("temp")}')


   # bot.reply_to(message, message.text)


bot.infinity_polling(True)