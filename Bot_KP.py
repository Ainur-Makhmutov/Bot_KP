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
            'last_photo_time': 0,
            'photo_batch_count': 0
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
            text="Присылайте скриншоты. После отправки всех фото нажмите 'Сохранить'.\n\n"
                 "Отправлено фото: 0",
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

        if user_id in user_data and user_data[user_id]['photos']:

            photos_count = len(user_data[user_id]['photos'])

            # Очищаем таймеры если есть

            user_data[user_id].pop('confirm_timer', None)

            user_data[user_id].pop('pending_photos', None)

            bot.edit_message_text(

                chat_id=call.message.chat.id,

                message_id=call.message.message_id,

                text=f"✅ Сохранено {photos_count} фото за текущую неделю!"

            )

            del user_data[user_id]


    elif call.data == "cancel_photos":

        if user_id in user_data:
            # Очищаем таймеры если есть

            user_data[user_id].pop('confirm_timer', None)

            user_data[user_id].pop('pending_photos', None)

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

    # Убираем часики "часики" (индикатор загрузки) с кнопки
    bot.answer_callback_query(call.id)


# Обработчик для фото
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    user_id = message.from_user.id

    if user_id in user_data:
        photo_id = message.photo[-1].file_id
        user_data[user_id]['photos'].append(photo_id)

        # Используем media_group_id для определения альбомов
        media_group_id = message.media_group_id

        if media_group_id:
            # Если это альбом, проверяем, первое ли это фото в группе
            if media_group_id != user_data[user_id].get('last_media_group'):
                # Это первое фото в альбоме
                user_data[user_id]['last_media_group'] = media_group_id
                user_data[user_id]['album_photo_count'] = 1
            else:
                # Продолжение альбома
                user_data[user_id]['album_photo_count'] += 1
                # Не отправляем сообщение для каждого фото в альбоме
                return
        else:
            # Одиночное фото
            user_data[user_id].pop('last_media_group', None)
            user_data[user_id].pop('album_photo_count', None)

        # Обновляем счетчик
        count = len(user_data[user_id]['photos'])
        save_markup = InlineKeyboardMarkup(row_width=2)
        save_markup.add(
            InlineKeyboardButton("Сохранить", callback_data="save_photos"),
            InlineKeyboardButton("Отмена", callback_data="cancel_photos")
        )

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=user_data[user_id]['current_message_id'],
            text=f"Присылайте скриншоты. После отправки всех фото нажмите 'Сохранить'.\n\n"
                 f"Отправлено фото: {count}",
            reply_markup=save_markup
        )

        # Отправляем подтверждение
        if media_group_id and user_data[user_id].get('album_photo_count', 1) > 1:
            # Для альбома указываем количество фото
            album_count = user_data[user_id]['album_photo_count']
            start_num = count - album_count + 1
            end_num = count
            bot.send_message(
                message.chat.id,
                f"✅ Фото #{start_num}-#{end_num} получено. Можете отправить еще или нажмите 'Сохранить'."
            )
        else:
            bot.send_message(
                message.chat.id,
                f"✅ Фото #{count} получено. Можете отправить еще или нажмите 'Сохранить'."
            )


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
