import requests
import os
import json
import re


def convert_formatted_number(value_str):
    """
    Преобразует форматированные числа с суффиксами:
    - '70,989K' -> 70989000 (K = тысячи)
    - '1.5M' -> 1500000 (M = миллионы)
    - '123' -> 123 (без суффикса)
    """
    if not value_str:
        return None

    value_str = value_str.strip().upper()

    # Определяем множитель
    multiplier = 1
    if value_str.endswith('K'):
        multiplier = 1000
        value_str = value_str[:-1]
    elif value_str.endswith('M'):
        multiplier = 1000000
        value_str = value_str[:-1]

    # Преобразуем строку в число
    # Заменяем запятую на точку для десятичного разделителя
    if ',' in value_str:
        value_str = value_str.replace(',', '')
    if '.' in value_str:
        value_str = value_str.replace('.', '')

    try:
        number = float(value_str)
        result = number * multiplier

        # Возвращаем int если нет дробной части
        if result.is_integer():
            return int(result)
        return result
    except ValueError:
        return None


def screenshot_templates (ocr_text, image_path):
    lines = ocr_text

    if "Осада -" in lines and "Братство стали" in lines:
        # скриншот - значение клана в осаде

        # Название осады
        siege_match = re.search(r'Осада - (.+?)\n', lines)
        siege_name = siege_match.group(1) if siege_match else "Неизвестная осада"

        # Значение
        value_match = re.search(r'Братство стали\n([\d,]+[KMB]?)', lines)

        if value_match:
            value = value_match.group(1)
            value = convert_formatted_number(value)

            return f"{siege_name}: {value}"

    elif "Событие —" in lines and "Братство стали" in lines:
        # скриншот - значение клана в событии

        # Название события
        event_match = re.search(r'Событие — (.+?)\n', lines)
        event_name = event_match.group(1) if event_match else "Неизвестное событие"

        # Значение
        value_match = re.search(r'Братство стали\s*\[[^\]]*\]\n([\d,]+(?:[KMB]|))', lines)

        if value_match:
            value = value_match.group(1)
            value = convert_formatted_number(value)

            return f"{event_name}: {value}"


    return None


ocr_text_siege = "7ตา24\nممميم\nОсада - Пески времени\nТекущая неделя\nИгроки\n47\nКланы\nВсего: 277\nappel de l'aventur\n592968837\n48\nхранители\n590547144\n49\n深夜手\n587166833\n50\nSolo Piratas\n582224568\n51\nБратство стали\n566098060\n52\nWTW\n562148032\n53\nГУНДОБАТ\n558276868\n54\nGod of War\n557569728\nНазад\nОсады"
ocr_text_event = "Событие — Камень и сталь\nТекущая неделя\nИгроки\nКланы\nВсего: 314\n60\nXandFarm [XFarm]\n74,817K\n61\nPraid 2 [Pra]\n74,394K\n62\nLosT [SLONs]\n73,392K\n63\nБлеск молнии [FLASH]\n71,199K\n64\nБратство стали [Steel]\n70,989K\n65\nCampGroundA [CampA]\n70,547K\n66\nBaGGi [BAGG]\n69,663K\n67\nCLAN [CLan]\n69,365K\nПравила\nНазад"

print (f"очень важный вывод: {screenshot_templates(ocr_text_siege)}")

# Тестируем
# test_cases = [
#     "70,989K",    # 70,989 * 1000 = 70,989,000
#     "1.5M",       # 1.5 * 1,000,000 = 1,500,000
#     "123K",       # 123 * 1000 = 123,000
#     "456",        # 456
#     "1,234.56K",  # 1234.56 * 1000 = 1,234,560
# ]
#
# print("Правильное преобразование с учетом множителей:")
# for test in test_cases:
#     result = convert_formatted_number(test)
#     print(result)