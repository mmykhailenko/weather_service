import telebot
import logging
from telebot import types
import requests

bot = telebot.TeleBot('802091036:AAGNYkVUPBkQlISYTBkne2wBkPF_Svlchp0', threaded=False)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.
API_TOKEN = ""

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
   # bot.send_message(message.chat.id, text=f'latitude: {message.location.latitude}; '
   #                                        f'longitude: {message.location.longitude}')

   url = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={message.location.latitude}&lon={message.location.longitude}&appid={API_TOKEN}').json()
   print(url)
   bot.send_message(message.chat.id, text=f'{url.get("name")}, {url.get("main").get("temp")}')

   #f'{url.get("name")}, {url.get("main").get("temp")}


@bot.message_handler(func=lambda message: True)
def echo_message(message):
   bot.reply_to(message, message.text)


bot.infinity_polling(True)