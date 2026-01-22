import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
from datetime import datetime
from tabulate import tabulate
import time

bot = telebot.TeleBot('8347600297:AAEEcKnqelE7wg7Blu0NXRse3p3vpZnRfQY')

SAVE_FOLDER = "telegram_photos"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Глобальный словарь для хранения состояний пользователей и их фото
user_data = {}

# Создаем inline-клавиатуру с кнопками
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
    user_id = call.from_user.id

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
        # Инициализируем данные пользователя
        user_data[user_id] = {
            'photos': [],
            'current_message_id': call.message.message_id,
            'awaiting_photos': True,  # Флаг ожидания фото
            'last_photo_time': time.time()
        }

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
                 "После отправки всех фото нажмите 'Сохранить'.\n\n"
                 "Отправлено фото: 0",
            reply_markup=save_markup
        )

        # Отправляем отдельное сообщение с инструкцией
        bot.send_message(
            call.message.chat.id,
            "📸 Отправляйте фото скриншотов одним или несколькими сообщениями. "
            "Когда закончите, нажмите кнопку 'Сохранить' в предыдущем сообщении."
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

        if user_id in user_data and user_data[user_id]['photos']:
            photos_count = len(user_data[user_id]['photos'])

            # Получаем все фото

            all_photos = user_data[user_id]['photos']

            # Отправляем подтверждение

            bot.edit_message_text(

                chat_id=call.message.chat.id,

                message_id=call.message.message_id,

                text=f"✅ Сохранено {photos_count} фото за текущую неделю!\n"

                     f"Файлы сохранены в папке: {SAVE_FOLDER}/{user_id}/"

            )

            # Очищаем данные пользователя

            del user_data[user_id]

            # Возвращаем в главное меню

            bot.send_message(

                call.message.chat.id,

                "Что еще хотите сделать?",

                reply_markup=create_inline_keyboard()

            )


    elif call.data == "cancel_photos":

        if user_id in user_data:
            # Очищаем данные пользователя

            del user_data[user_id]

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

                text="Загрузка фото отменена. Выберите за какой период хотите прислать скриншоты:",

                reply_markup=sendChoice_markup

            )

            bot.edit_message_text(

                chat_id=call.message.chat.id,

                message_id=call.message.message_id,

                text="Загрузка фото отменена. Выберите за какой период хотите прислать скриншоты:",

                reply_markup=sendChoice_markup

            )

    # Убираем часики "часики" (индикатор загрузки) с кнопки
    bot.answer_callback_query(call.id)


# Обработчик для получения фотографий от пользователя
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.from_user.id

    # Проверяем, ожидаем ли мы фото от этого пользователя
    if user_id in user_data and user_data[user_id].get('awaiting_photos'):

        # Создаем папку для пользователя если её нет
        user_folder = os.path.join(SAVE_FOLDER, str(user_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Сохраняем фото
        photo_info = []
        if message.photo:
            # Если несколько фото в одном сообщении (альбом)
            if hasattr(message, 'media_group_id') and message.media_group_id:
                # Это альбом фото
                for photo in message.photo:
                    photo_id = message.photo[-1].file_id
                    user_data[user_id]['photos'].append(photo_id)
                    file_info = bot.get_file(photo.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)

                    # Генерируем уникальное имя файла
                    timestamp = int(time.time())
                    filename = f"photo_{timestamp}_{len(photo_info)}.jpg"
                    file_path = os.path.join(user_folder, filename)

                    # Сохраняем файл
                    with open(file_path, 'wb') as new_file:
                        new_file.write(downloaded_file)

                    photo_info.append({
                        'file_path': file_path,
                        'file_id': message.photo[-1].file_id
                    })
            else:
                # Одно фото
                file_info = bot.get_file(message.photo[-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                # Генерируем уникальное имя файла
                timestamp = int(time.time())
                filename = f"photo_{timestamp}.jpg"
                file_path = os.path.join(user_folder, filename)

                # Сохраняем файл
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)

                photo_info.append({
                    'file_path': file_path,
                    'file_id': message.photo[-1].file_id
                })

        # Сохраняем информацию о фото в user_data
        if 'photos' not in user_data[user_id]:
            user_data[user_id]['photos'] = []

        user_data[user_id]['photos'].extend(photo_info)

        # Обновляем сообщение с количеством отправленных фото
        photos_count = len(user_data[user_id]['photos'])

        # Создаем клавиатуру для сохранения или отмены
        save_markup = InlineKeyboardMarkup(row_width=2)
        save_markup.add(
            InlineKeyboardButton("Сохранить", callback_data="save_photos"),
            InlineKeyboardButton("Отмена", callback_data="cancel_photos")
        )

        # Обновляем сообщение
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=user_data[user_id].get('current_message_id'),
            text=f"✅ Фото получены!\n\nПрисылайте скриншоты. После отправки всех фото нажмите 'Сохранить'.\n\n"
                 f"Отправлено фото: {photos_count}",
            reply_markup=save_markup
        )

        # Отправляем подтверждение получения
        bot.reply_to(message, f"✅ Получено {len(photo_info)} фото. Отправлено всего: {photos_count}")

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
