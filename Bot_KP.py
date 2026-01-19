import telebot
from telebot import types
import os
from datetime import datetime

bot = telebot.TeleBot('8347600297:AAEEcKnqelE7wg7Blu0NXRse3p3vpZnRfQY')

SAVE_FOLDER = "telegram_photos"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Инструмент поноса")


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    try:
        # Получаем информацию о фото
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Создаем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_id = message.from_user.id
        filename = f"photo_{user_id}_{timestamp}.jpg"
        filepath = os.path.join(SAVE_FOLDER, filename)

        # Сохраняем фото
        with open(filepath, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"✅ Фото сохранено как: {filename}")

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при сохранении: {str(e)}")


@bot.message_handler(commands=['stats'])
def show_stats(message):
    """Показать статистику сохраненных фото"""
    if os.path.exists(SAVE_FOLDER):
        files = os.listdir(SAVE_FOLDER)
        photo_count = len([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        bot.send_message(message.chat.id, f"📊 Сохранено фотографий: {photo_count}")
    else:
        bot.send_message(message.chat.id, "📁 Папка с фото еще не создана")

bot.infinity_polling()