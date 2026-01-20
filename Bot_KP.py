import telebot
from telebot import types
import os
from datetime import datetime
from tabulate import tabulate

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


@bot.message_handler(commands=['1'])
def send_table(message):
    # Создаем ASCII таблицу
    table = """
┌─────┬────────────┬─────────┐
│ ID  │    Имя     │  Цена   │
├─────┼────────────┼─────────┤
│  1  │  Товар А   │  100₽   │
│  2  │  Товар Б   │  200₽   │
│  3  │  Товар В   │  150₽   │
└─────┴────────────┴─────────┘
"""

    bot.send_message(message.chat.id, f"`{table}`", parse_mode='Markdown')

@bot.message_handler(commands=['2'])
def send_table(message):
    # Данные для таблицы
    data = [
        [1, "Товар А", 100],
        [2, "Товар Б", 200],
        [3, "Товар В", 150],
        [4, "Товар Г", 250]
    ]

    headers = ["ID", "Название", "Цена"]

    # Формируем таблицу
    table = tabulate(data, headers=headers, tablefmt="grid")

    bot.send_message(
        message.chat.id,
        f"```\n{table}\n```",
        parse_mode='Markdown'
    )


@bot.message_handler(commands=['3'])
def send_html_table(message):
    html = """
<b>📊 Таблица товаров:</b>

<pre>
┌─────┬────────────┬─────────┐
│ ID  │    Имя     │  Цена   │
├─────┼────────────┼─────────┤
│  1  │  Товар А   │  100₽   │
├─────┼────────────┼─────────┤
│  2  │  Товар Б   │  200₽   │
├─────┼────────────┼─────────┤
│  3  │  Товар В   │  150₽   │
└─────┴────────────┴─────────┘
</pre>

<i>Обновлено: сегодня</i>
"""

    bot.send_message(message.chat.id, html, parse_mode='HTML')


@bot.message_handler(commands=['4']) # это!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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


@bot.message_handler(commands=['5'])
def select_product(message):
    # Данные для таблицы
    products = [
        {"id": 1, "name": "Товар А", "price": 100},
        {"id": 2, "name": "Товар Б", "price": 200},
        {"id": 3, "name": "Товар В", "price": 150}
    ]

    # Создаем inline-клавиатуру
    markup = types.InlineKeyboardMarkup(row_width=3)

    # Добавляем кнопки
    for product in products:
        button = types.InlineKeyboardButton(
            text=f"{product['id']}. {product['name']} - {product['price']}₽",
            callback_data=f"product_{product['id']}"
        )
        markup.add(button)

    bot.send_message(
        message.chat.id,
        "Выберите товар:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def handle_product_selection(call):
    product_id = call.data.split('_')[1]
    bot.answer_callback_query(call.id, f"Вы выбрали товар {product_id}")




bot.infinity_polling()