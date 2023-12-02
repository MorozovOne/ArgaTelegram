import telebot
from telebot import types
import os
import json
from pathlib import Path
import telebot
from pydub import AudioSegment
from telebot import TeleBot
from telebot import types
import shutil


token='6730043869:AAHacpzHhLSHiW6y49WTUIQ5qhH25cAeRX8'

bot=telebot.TeleBot(token)

version = 0
src = ""



@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Отправь мне песню в формате mp3 или wav\n'
                              'иначе будешь вечность ждать свою песню мухахаха! =) \n \n \n'
                              'P.S Хотел бы упомянуть что это тестовая версия проекта,'
                              'сообщайте мне в личку, если найдете баги \n ===> @MorozovOne')
        

@bot.message_handler(content_types=['document', 'audio', 'voice', 'text'])
def get_file(message):
    global src
    try:
        if message.content_type == 'audio':  # mp3
            print(message.audio)

            file_info = bot.get_file(message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'files/' + message.audio.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, 'Секунду...')

        elif message.content_type == 'document': # wav
            print(message.audio)

            file_info = bot.get_file(message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'files/' + message.audio.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, 'Секунду...')

    except Exception as e:
        bot.reply_to(message, str(e))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Slowed + Reverb")
    item2 = types.KeyboardButton("Superslow + Reverb")
    item3 = types.KeyboardButton("NightCore")
    item4 = types.KeyboardButton("SpeedUp")
    markup.add(item2, item1, item3, item4)
    send = bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    bot.register_next_step_handler(send, choose)
    return src

@bot.message_handler(content_types='text')
def choose(message):
    global src

    try:
        if message.text == "Slowed + Reverb":

            bot.send_message(message.chat.id, 'Еще чуть чуть...')

            filename = src
            sound = AudioSegment.from_file(filename, format="mp3")
            print(src)

            octaves = 0.5
            new_sample_rate = int(sound.frame_rate * (0.8 ** octaves))
            pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            pitch_sound = pitch_sound.set_frame_rate(44100)
            pitch_sound.export(filename, format="mp3")

            with open(src, 'rb') as doc:
                out_msg = bot.send_document(message.chat.id, doc)
                print(doc)

        elif message.text == "Superslow + Reverb":

            bot.send_message(message.chat.id, 'Еще чуть чуть...')

            filename = src
            sound = AudioSegment.from_file(filename, format="mp3")
            print(src)

            octaves = 0.5
            new_sample_rate = int(sound.frame_rate * (0.5 ** octaves))
            pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            pitch_sound = pitch_sound.set_frame_rate(44100)
            pitch_sound.export(filename, format="mp3")

            with open(src, 'rb') as doc:
                out_msg = bot.send_document(message.chat.id, doc)
                print(doc)
        elif message.text == "NightCore":

            bot.send_message(message.chat.id, 'Еще чуть чуть...')

            filename = src
            sound = AudioSegment.from_file(filename, format="mp3")
            print(src)

            octaves = 0.5
            new_sample_rate = int(sound.frame_rate * (1.3 ** octaves))
            pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            pitch_sound = pitch_sound.set_frame_rate(44100)
            pitch_sound.export(filename, format="mp3")

            with open(src, 'rb') as doc:
                out_msg = bot.send_document(message.chat.id, doc)
                print(doc)
        elif message.text == "SpeedUp":

            bot.send_message(message.chat.id, 'Еще чуть чуть...')

            filename = src
            sound = AudioSegment.from_file(filename, format="mp3")
            print(src)

            octaves = 0.5
            new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
            pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            pitch_sound = pitch_sound.set_frame_rate(44100)
            pitch_sound.export(filename, format="mp3")

            with open(src, 'rb') as doc:
                out_msg = bot.send_document(message.chat.id, doc)
                print(doc)
        else:
            bot.send_message(message.chat.id, 'Ой... у нас кажись баг ¯\_(ツ)_/¯')
    except Exception as e:
        bot.reply_to(message, str(e))




DIR = 'files/'

for x in range(len(os.listdir(DIR))):
    if x > 50:
        shutil.rmtree('files/')
        os.mkdir('files/')



bot.polling(none_stop=True, interval=0)