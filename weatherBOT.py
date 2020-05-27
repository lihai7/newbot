from telebot import types
import os
import telebot
from functions import parse_btc_to_usd, parse_weather, parse_chance_of_rain
from flask import Flask, request
###
#
TOKEN = '1159436936:AAG1FkCcfb6npHdRyYluwzLMdMGRfraIzhg'
bot = telebot.TeleBot('1159436936:AAG1FkCcfb6npHdRyYluwzLMdMGRfraIzhg')
server = Flask(__name__)
#
@bot.message_handler(commands=['start'])
def welcome(message):
    # bot.send_message(message.chat.id, 'Привет, я буду отправлять тебе погоду/курс биткоина.')
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать погоду")
    item2 = types.KeyboardButton("Узнать курс биткоина")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Привет, я буду отправлять тебе погоду/курс биткоина".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def weather(message):
    if message.text == 'Узнать погоду':
        bot.send_message(message.chat.id, (f'Сейчас на улице {parse_weather()}\nВероятность осадков {parse_chance_of_rain()}%'))
    if message.text == 'Узнать курс биткоина':
        bot.send_message(message.chat.id, (f'1 BTC={parse_btc_to_usd()}USD'))


@server.route("/" + TOKEN, methods = ['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://git.heroku.com/peaceful-cliffs-83269.git" + TOKEN)

if __name__ == "__main__":
    server.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))

#Bot srart
bot.polling(none_stop=True)
