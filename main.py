import telebot
import requests
from bs4 import BeautifulSoup as b
from telebot import types


def get_temperature():
    url = 'https://world-weather.ru/pogoda/russia/moscow/'
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    weather = soup.find('div', class_='weather-now-info').find('div', id='weather-now-number')
    _temperature = weather.text
    return(_temperature)


bot = telebot.TeleBot('5911496711:AAEyfvN7CcveRH7i1ktEQ5O-3wFSNchiJwo')

@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.username)
    mess = f'Привет, <b>{message.from_user.first_name}</b>. Напиши команду "/help", чтобы посмотреть, что я умею'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help_help(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    temperature =types.KeyboardButton('/temperature')
    button.add(temperature)
    bot.send_message(message.chat.id, 'Я могу сказать <u><b>температуру на улице в Москве</b></u>. Используй команду'
                                      ' "/temperature", чтобы узнать',parse_mode='html',  reply_markup=button)


@bot.message_handler(['temperature'])
def temperature(message):
    bot.send_message(message.chat.id, get_temperature())


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'document', 'audio'])
def get_user_text(message):
    if message.text:
        print(message.text)
        photo = open('myReaction.png', 'rb')
        bot.send_photo(message.chat.id, photo)


bot.polling(none_stop=True)
