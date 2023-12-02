import telebot
from telebot import types

token='6730043869:AAHacpzHhLSHiW6y49WTUIQ5qhH25cAeRX8'

bot=telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Привет')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("ss")
    item2 = types.KeyboardButton("sdf")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    print(bot.send_message(message.chat.id, 'mk xmk', reply_markup=markup))
    print(message.content_type)

