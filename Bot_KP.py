import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
from datetime import datetime
from tabulate import tabulate

bot = telebot.TeleBot('8347600297:AAEEcKnqelE7wg7Blu0NXRse3p3vpZnRfQY')

SAVE_FOLDER = "telegram_photos"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


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

    # Убираем часики "часики" (индикатор загрузки) с кнопки
    bot.answer_callback_query(call.id)

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
