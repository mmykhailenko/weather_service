import os
import requests
from flask import Flask, request
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

WEATHER_API_TOKEN = os.environ.get("WEATHER_API_TOKEN")
SERVER_URL = "https://weather1-test.herokuapp.com"


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    city = message.text
    url = "{}{}".format(SERVER_URL, "/weather/{}".format(city))

    try:
        resp = requests.get(url).json()
    except Exception as exc:
        print(exc)
    else:
        bot.send_message(message.chat.id, text=f'{resp.get("temp")}')


@bot.message_handler(commands=['location'])
def location(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Do you now the way", reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
    url = requests.get(f'http://api.openweathermap.org/data/2.5/weather?'
                       f'lat={message.location.latitude}&lon={message.location.longitude}&appid={WEATHER_API_TOKEN}').json()
    bot.send_message(message.chat.id, text=f'{url.get("name")}, '
                                           f'{url.get("main").get("temp")}')


@server.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-django.herokuapp.com/' + BOT_TOKEN)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
