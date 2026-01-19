import telebot
import json
from datetime import datetime
from telebot import types

bot = telebot.TeleBot('8347600297:AAEEcKnqelE7wg7Blu0NXRse3p3vpZnRfQY')

with open('boss_sieges_scores.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "ff")

# Форматирование чисел с разделителями тысяч
def format_number(num):
    if num is None:
        return "—"
    return f"{num:,}".replace(",", " ")


# Команда /table - основная таблица
@bot.message_handler(commands=['table'])
def send_compact_table(message):
    """Компактная таблица с горизонтальным скроллингом"""
    try:
        players = data.get('members_info', [])
        clan_name = data.get('name', 'Неизвестный')

        # Сортируем
        players.sort(key=lambda x: x.get('scores', {}).get('current', {}).get('rating') or 0, reverse=True)

        # Формируем компактную таблицу
        table_parts = []
        current_table = ""

        for i, member in enumerate(players, 1):
            name = member.get('name', '?')
            if len(name) > 12:
                name = name[:9] + "..."

            # Текущие значения
            current = member.get('scores', {}).get('current', {})
            curr_rating = current.get('rating')
            curr_siege = current.get('boss_siege')

            # Форматируем значения
            r_str = format_number(curr_rating) if curr_rating else "—"
            s_str = format_number(curr_siege) if curr_siege else "—"

            line = f"{i:>2}. {name:<12} R:{r_str:>8} S:{s_str:>12}\n"

            # Если текущая часть становится слишком большой, начинаем новую
            if len(current_table) + len(line) > 3500:
                table_parts.append(current_table)
                current_table = "```\n" + line
            else:
                if not current_table:
                    current_table = "```\n"
                current_table += line

        # Добавляем последнюю часть
        if current_table:
            current_table += "```"
            table_parts.append(current_table)

        # Отправляем заголовок
        header = f"🏰 *{clan_name}* ({len(players)} игроков)\nКомпактный вид:\n"
        bot.send_message(message.chat.id, header, parse_mode='Markdown')

        # Отправляем части
        for i, part in enumerate(table_parts, 1):
            part_msg = f"📄 *Часть {i}/{len(table_parts)}*\n\n{part}"
            bot.send_message(message.chat.id, part_msg, parse_mode='Markdown')

    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        bot.send_message(message.chat.id, error_msg)

bot.infinity_polling()