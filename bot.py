import os
import telebot
from pydub import AudioSegment
from telebot import types
import tempfile

# Set the path for FFmpeg
ffmpeg_path = "/usr/bin/ffmpeg"
AudioSegment.ffmpeg = ffmpeg_path

# Initialize the bot
token = 'TOKEN'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        'Отправь или перешли мне песню, немного подожди и выбери нужную версию\n'

        'P.S Сообщайте мне в личку, если найдете баги \n ===> @MorozovOne'
    )


@bot.message_handler(content_types=['document', 'audio'])
def get_file(message):
    try:
        # Get the audio file
        file_info = bot.get_file(message.audio.file_id if message.content_type == 'audio' else message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(downloaded_file)
            temp_file_path = temp_file.name

        bot.send_message(message.chat.id, 'Секунду...')

        # Send options to the user
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        options = ["Slowed + Reverb", "Superslow + Reverb", "NightCore", "SpeedUp"]
        markup.add(*options)
        send = bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
        bot.register_next_step_handler(send, choose, temp_file_path, message.audio.file_name)

    except Exception as e:
        bot.reply_to(message, str(e))


def choose(message, temp_file_path, original_filename):
    try:
        # Define suffixes for each option
        suffix_map = {
            "Slowed + Reverb": "slowed",
            "Superslow + Reverb": "superslowed",
            "NightCore": "nightcore",
            "SpeedUp": "speedup"
        }

        if message.text in suffix_map:
            new_suffix = suffix_map[message.text]
            base_name, _ = os.path.splitext(original_filename)
            processed_filename = f"{base_name}_{new_suffix}.mp3"

            octaves = 0.6
            sound = AudioSegment.from_file(temp_file_path)
            new_sample_rate = int(sound.frame_rate * (
                0.9 if new_suffix == "slowed" else 0.7 if new_suffix == "superslowed" else 1.1 if new_suffix == "nightcore" else 1.2))
            pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            pitch_sound = pitch_sound.set_frame_rate(44100)

            # Export the processed file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as output_file:
                output_path = output_file.name
                pitch_sound.export(output_path, format="mp3")

            # Send the processed file to the user
            with open(output_path, 'rb') as doc:
                bot.send_document(message.chat.id, doc, caption=f"Обработанный файл: {processed_filename}")

            # Clean up the temporary files
            os.remove(temp_file_path)
            os.remove(output_path)

        else:
            bot.send_message(message.chat.id, 'Ой... у нас кажись баг')

    except Exception as e:
        bot.reply_to(message, str(e))


# Check if FFmpeg is installed
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError(f"FFmpeg not found at: {ffmpeg_path}")

# Start polling
bot.polling(none_stop=True, interval=0, timeout=30)
