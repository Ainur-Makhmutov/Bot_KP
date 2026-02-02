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

    elif "Осада -" in lines and "Братство стали" not in lines:
        # скриншот - значение топ 20 в осаде

        # Название осады
        siege_match = re.search(r'Осада - (.+?)\n', lines)
        siege_name = siege_match.group(1) if siege_match else "Неизвестная осада"

        # Паттерн для поиска записей: позиция\n имя\n значение
        # Учитываем, что имя может содержать пробелы, скобки и другие символы
        pattern = r'\n([^\n\d][^\n]*?)\s*\n\s*([\d,]+[KMB]?\b)'

        matches = re.findall(pattern, lines)

        results = []
        for match in matches:
            name = match[0].strip()
            value_str = match[1]

            if 'Всего:' in name:
                continue

            value = convert_formatted_number(value_str)

            results.append({
                'name': name,
                'value': value,
                'value_str': value_str
            })

        # Сортируем по позиции на случай, если порядок нарушен
        # results.sort(key=lambda x: x['position'])

        return {
            'name': siege_name,
            'players': results,
            'total': len(results)
        }

    elif "Событие —" in lines and "Братство стали" not in lines:
        # скриншот - значение топ 20 в событии

        # Название события
        event_match = re.search(r'Событие — (.+?)\n', lines)
        event_name = event_match.group(1) if event_match else "Неизвестное событие"

        # Паттерн для поиска записей: позиция\n имя\n значение
        # Учитываем, что имя может содержать пробелы, скобки и другие символы
        pattern = r'\n([^\n\d][^\n]*?)\s*\n\s*([\d,]+[KMB]?\b)'

        matches = re.findall(pattern, lines)

        results = []
        for match in matches:
            name = match[0].strip()
            value_str = match[1]

            if 'Всего:' in name:
                continue

            value = convert_formatted_number(value_str)

            results.append({
                'name': name,
                'value': value,
                'value_str': value_str
            })

        # Сортируем по позиции на случай, если порядок нарушен
        # results.sort(key=lambda x: x['position'])

        return {
            'name': event_name,
            'players': results,
            'total': len(results)
        }

    return None


ocr_text_siege = "7ตา24\nممميم\nОсада - Пески времени\nТекущая неделя\nИгроки\n47\nКланы\nВсего: 277\nappel de l'aventur\n592968837\n48\nхранители\n590547144\n49\n深夜手\n587166833\n50\nSolo Piratas\n582224568\n51\nБратство стали\n566098060\n52\nWTW\n562148032\n53\nГУНДОБАТ\n558276868\n54\nGod of War\n557569728\nНазад\nОсады"
ocr_text_event = "Событие — Камень и сталь\nТекущая неделя\nИгроки\nКланы\nВсего: 314\n60\nXandFarm [XFarm]\n74,817K\n61\nPraid 2 [Pra]\n74,394K\n62\nLosT [SLONs]\n73,392K\n63\nБлеск молнии [FLASH]\n71,199K\n64\nБратство стали [Steel]\n70,989K\n65\nCampGroundA [CampA]\n70,547K\n66\nBaGGi [BAGG]\n69,663K\n67\nCLAN [CLan]\n69,365K\nПравила\nНазад"

ocr_text_siegeTop20 = "عمدام\nОсада - Пески времени\nТекущая неделя\nИгроки\nКланы\nВсего: 1371\n1\nБадун [DoP]\n6970094485\n2\nMarty McFly [DoP]\n4183196699\n3\nsten [dlk]\n3657738586\nGnom [GDI]\n3348750000\n5\nАндрюха Россия [GDI]\n3087538946\nbond007 [RayDK]\n2802500000\n7\nYoneu [GDI]\n2747068064\n8\nАртем [GDI]\n2217322031\nНазад\nОсады"
ocr_text_eventTop20 = "Событие — Камень и сталь\nТекущая неделя\nИгроки\nКланы\nВсего: 1386\nSarpiton [DoP]\n541M\n2\nDeDok [DoP]\n465M\nАрсен [MeD]\n342M\nХазар [DoP]\n287M\nIrisKissKiss [DoP]\n256M\n6\nАртем [GDI]\n222M\nBatusai [DoP]\n211M\nShytnik [DAS]\n192M\nПравила\nНазад"

print (f"очень важный вывод: {screenshot_templates(ocr_text_eventTop20, "1")}")