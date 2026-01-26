import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
from datetime import datetime
from tabulate import tabulate
import time
from collections import defaultdict


bot = telebot.TeleBot('8347600297:AAEEcKnqelE7wg7Blu0NXRse3p3vpZnRfQY')


SAVE_FOLDER = "telegram_photos"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


# Глобальный словарь для хранения состояний пользователей и их фото
photo_data = []
# Глобальный флаг для сохранения фото
ENABLE_PHOTO_SAVING = False

# Создаем начальную inline-клавиатуру с кнопками
def create_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)  # row_width=1 значит одна кнопка в строке

    markup.add(
        InlineKeyboardButton("Отправить скрин", callback_data="send_screenshot"),
        InlineKeyboardButton("Статистика топ-20 игроков", callback_data="top20_statistics"),
        InlineKeyboardButton("Статистика клана", callback_data="clan_statistics")
    )
    return markup


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Добро пожаловать в тетрадь поноса!\n\nЧего желаете?"

    # Отправляем сообщение с inline-кнопками
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=create_inline_keyboard()
    )


# Обработчик нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global ENABLE_PHOTO_SAVING

    if call.data == "send_screenshot":
        # Редактируем текущее сообщение и добавляем новую клавиатуру
        sendChoice_markup = InlineKeyboardMarkup(row_width=1)
        sendChoice_markup.add(
            InlineKeyboardButton("Текущая неделя", callback_data="current_week"),
            InlineKeyboardButton("Предыдущая неделя", callback_data="previous_week"),
            InlineKeyboardButton("Неделя за период...", callback_data="week_period"),
            InlineKeyboardButton("Назад", callback_data="back_main")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите за какой период хотите прислать скриншоты:",
            reply_markup=sendChoice_markup
        )

    elif call.data == "current_week":
        ENABLE_PHOTO_SAVING = True

        # Создаем клавиатуру для сохранения или отмены
        save_markup = InlineKeyboardMarkup(row_width=2)
        save_markup.add(
            InlineKeyboardButton("Сохранить", callback_data="save_photos"),
            InlineKeyboardButton("Отмена", callback_data="cancel_photos")
        )

        # Редактируем сообщение с инструкцией
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📸 Теперь присылайте фото скриншотов.\n\n"
                 "Можете отправлять по одному или несколько фото сразу (альбомом).\n"
                 "После отправки всех фото нажмите 'Сохранить'.",
            reply_markup=save_markup
        )

    elif call.data == "top20_statistics":
        top20choice_markup = InlineKeyboardMarkup(row_width=1)
        top20choice_markup.add(
            InlineKeyboardButton("Текущая неделя", callback_data="current_week"),
            InlineKeyboardButton("Предыдущая неделя", callback_data="previous_week"),
            InlineKeyboardButton("Неделя за период...", callback_data="week_period"),
            InlineKeyboardButton("Назад", callback_data="back_main")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите за какой период должна быть статистика топ 20:",
            reply_markup=top20choice_markup
        )

    elif call.data == "clan_statistics":
        # выбор статистики клана по событию или осаде
        clanChoice_markup = InlineKeyboardMarkup(row_width=1)
        clanChoice_markup.add(
            InlineKeyboardButton("События", callback_data="event"),
            InlineKeyboardButton("Осада", callback_data="siege"),
            InlineKeyboardButton("Назад", callback_data="back_main")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите событие или осаду:",
            reply_markup=clanChoice_markup
        )

    elif call.data == "event":
        # выбор статистики клана по событию или осаде
        eventChoice_markup = InlineKeyboardMarkup(row_width=1)
        eventChoice_markup.add(
            InlineKeyboardButton("Текущая неделя", callback_data="current_week"),
            InlineKeyboardButton("Предыдущая неделя", callback_data="previous_week"),
            InlineKeyboardButton("Неделя за период...", callback_data="week_period"),
            InlineKeyboardButton("Назад", callback_data="clan_statistics")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите за какой период должна быть статистика клана по событию:",
            reply_markup=eventChoice_markup
        )

    elif call.data == "siege":
        # выбор статистики клана по событию или осаде
        siegeChoice_markup = InlineKeyboardMarkup(row_width=1)
        siegeChoice_markup.add(
            InlineKeyboardButton("Текущая неделя", callback_data="current_week"),
            InlineKeyboardButton("Предыдущая неделя", callback_data="previous_week"),
            InlineKeyboardButton("Неделя за период...", callback_data="week_period"),
            InlineKeyboardButton("Назад", callback_data="clan_statistics")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите за какой период должна быть статистика клана по осаде:",
            reply_markup=siegeChoice_markup
        )

    elif call.data == "back_main":
        # Возврат в главное меню
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Добро пожаловать в тетрадь поноса!\n\nЧего желаете?",
            reply_markup=create_inline_keyboard()
        )

    elif call.data == "save_photos":
        ENABLE_PHOTO_SAVING = False

        try:
            for i in photo_data:
                # Получаем информацию о файле
                file_info = bot.get_file(i)
                # Формируем путь для сохранения
                file_path = os.path.join(SAVE_FOLDER, f"{photo_data.index(i)}.jpg")
                # Скачиваем файл
                downloaded_file = bot.download_file(file_info.file_path)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
            bot.send_message(call.message.chat.id, f"✅ Cохранено {len(photo_data)} Фото!")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Ошибка при сохранении фото: {e}")

        photo_data.clear()

        sendChoice_markup = InlineKeyboardMarkup(row_width=1)

        sendChoice_markup.add(

            InlineKeyboardButton("Текущая неделя", callback_data="current_week"),

            InlineKeyboardButton("Предыдущая неделя", callback_data="previous_week"),

            InlineKeyboardButton("Неделя за период...", callback_data="week_period"),

            InlineKeyboardButton("Назад", callback_data="back_main")

        )

        bot.send_message(

            chat_id=call.message.chat.id,

            text="Загрузка фото выполнена успешно! Выберите за какой период хотите прислать скриншоты:",

            reply_markup=sendChoice_markup

        )

    elif call.data == "cancel_photos":
        ENABLE_PHOTO_SAVING = False

        photo_data.clear()

        sendChoice_markup = InlineKeyboardMarkup(row_width=1)

        sendChoice_markup.add(

            InlineKeyboardButton("Текущая неделя", callback_data="current_week"),

            InlineKeyboardButton("Предыдущая неделя", callback_data="previous_week"),

            InlineKeyboardButton("Неделя за период...", callback_data="week_period"),

            InlineKeyboardButton("Назад", callback_data="back_main")

        )

        bot.send_message(

            chat_id=call.message.chat.id,

            text="Загрузка фото отменена. Выберите за какой период хотите прислать скриншоты:",

            reply_markup=sendChoice_markup

        )

    # Убираем часики "часики" (индикатор загрузки) с кнопки
    bot.answer_callback_query(call.id)


# Обработчик для фото со включенным флагом
@bot.message_handler(content_types=['photo'], func=lambda message: ENABLE_PHOTO_SAVING)
def handle_photo(message):
    # Получаем file_id самого большого размера (последний в списке)
    file_id = message.photo[-1].file_id
    # Добавляем в список id фото
    photo_data.append(file_id)


@bot.message_handler(commands=['stats'])
def show_stats(message):
    """Показать статистику сохраненных фото"""
    if os.path.exists(SAVE_FOLDER):
        files = os.listdir(SAVE_FOLDER)
        photo_count = len([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        bot.send_message(message.chat.id, f"📊 Сохранено фотографий: {photo_count}")
    else:
        bot.send_message(message.chat.id, "📁 Папка с фото еще не создана")


@bot.message_handler(commands=['пример']) # это!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def show_products(message):
    # Пример данных (обычно берут из БД)
    products = [
        {"id": 1, "name": "Яблоки", "price": 89, "stock": 150},
        {"id": 2, "name": "Бананы", "price": 120, "stock": 80},
        {"id": 3, "name": "Апельсины", "price": 95, "stock": 200},
        {"id": 4, "name": "Манго", "price": 250, "stock": 45}
    ]

    # Формируем таблицу вручную
    table_lines = ["┌─────┬────────────┬─────────┬─────────┐"]
    table_lines.append("│ ID  │   Товар    │  Цена   │ Остаток │")
    table_lines.append("├─────┼────────────┼─────────┼─────────┤")

    for product in products:
        line = f"│ {product['id']:^3} │ {product['name']:^10} │ {product['price']:>6}₽ │ {product['stock']:>7} │"
        table_lines.append(line)

    table_lines.append("└─────┴────────────┴─────────┴─────────┘")

    table = "\n".join(table_lines)

    bot.send_message(message.chat.id, f"<pre>{table}</pre>", parse_mode='HTML')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
