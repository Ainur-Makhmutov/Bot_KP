import requests
import os
import json
import re
import socks
import socket


socks.set_default_proxy(socks.SOCKS5, "localhost", 9150) # Порт тора
socket.socket = socks.socksocket


# ====== OCR.Space API ======
def ocr_space_api(image_path):

    try:
        with open(image_path, 'rb') as image_file:

            url = "https://api.ocr.space/parse/image"
            api_key = 'K88266104688957'

            # Проверка размера. Надо будет проверку в тг
            file_size = os.path.getsize(image_path)
            if file_size > 1024 * 1024:
                return f"Файл слишком большой: {file_size / 1024 / 1024:.2f} МБ"

            payload = {
                'apikey': api_key,  # ключ
                'language': 'rus',  # Русский язык
                'isOverlayRequired': False,
                'OCREngine': 2,  # Более точный движок
                'detectOrientation': True,
                'scale': True
            }

            files = {'image': ('filename.jpg', image_file, 'image/jpeg')}

            response = requests.post(url, files=files, data=payload, timeout=30)
            result = response.json()

            if result.get('ParsedResults'):
                text = result['ParsedResults'][0]['ParsedText']
                return text.strip()
            else:
                error_msg = result.get('ErrorMessage', 'Неизвестная ошибка API')
                return f"Ошибка API: {error_msg}"
    except requests.exceptions.Timeout:
        return "Таймаут запроса к API"
    except Exception as e:
        return f"Ошибка запроса: {str(e)}"


# ====== 2 вида шаблона извлечения данных ======
def parse_ocr_text(ocr_text):
    """
    Парсит текст, полученный от OCR, в структурированный формат
    """
    # Разбиваем текст на строки и убираем пустые
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]

    # Инициализируем структуру данных
    parsed_data = {
        'event_name': '',
        'week': '',
        'total_players': 0,
        'clans': []
    }

    clan_data = []
    i = 0
    total_lines = len(lines)

    # Пропускаем начальные числа (например, "055")
    while i < total_lines and lines[i].isdigit():
        i += 1

    # Парсим заголовки
    while i < total_lines:
        line = lines[i]

        # Парсим название события
        if 'Событие —' in line:
            parsed_data['event_name'] = line.replace('Событие —', '').strip()
            i += 1

        # Парсим текущую неделю
        elif 'Текущая неделя' in line:
            parsed_data['week'] = 'Текущая неделя'
            i += 1

        # Парсим общее количество игроков
        elif 'Всего:' in line:
            total_text = line.split('Всего:')[-1].strip()
            try:
                parsed_data['total_players'] = int(total_text)
            except:
                parsed_data['total_players'] = 0
            i += 1

        # Пропускаем заголовки столбцов
        elif line in ['Игроки', 'Кланы'] or line == 'Игроки\nКланы':
            i += 1

        # Парсим данные кланов (позиция - число)
        elif line.isdigit():
            position = int(line)
            clan_info = {'position': position, 'name': '', 'tag': '', 'points': 0}

            # Переходим к следующей строке - название клана
            i += 1
            if i < total_lines:
                name_line = lines[i]

                # Обработка названия клана
                clan_name_parts = []

                # Собираем все части названия клана
                while i < total_lines:
                    current_line = lines[i]

                    # Если находим очки, останавливаемся
                    if 'K' in current_line and any(c.isdigit() for c in current_line.replace(',', '')):
                        # Извлекаем очки
                        try:
                            points_str = current_line.replace('K', '').replace(',', '').strip()
                            points = int(float(points_str) * 1000)
                            clan_info['points'] = points
                        except:
                            clan_info['points'] = 0
                        i += 1
                        break

                    # Если находим следующую позицию, останавливаемся
                    if current_line.isdigit():
                        break

                    # Обработка символа ®
                    if current_line == '®':
                        i += 1
                        continue

                    # Добавляем часть названия клана
                    clan_name_parts.append(current_line)
                    i += 1

                # Объединяем части названия клана
                full_name = ' '.join(clan_name_parts)

                # Извлекаем тег из квадратных скобок
                import re
                tag_match = re.search(r'\[(.*?)\]', full_name)
                if tag_match:
                    clan_info['tag'] = tag_match.group(1)
                    # Убираем тег из названия
                    clan_info['name'] = re.sub(r'\s*\[.*?\]\s*', '', full_name).strip()
                else:
                    clan_info['name'] = full_name.strip()

                clan_data.append(clan_info)
            else:
                i += 1

        # Пропускаем символ ® отдельно стоящий
        elif line == '®':
            i += 1

        # Пропускаем кнопки
        elif line in ['Правила', 'Назад']:
            i += 1

        else:
            i += 1

    # Сортируем кланы по позиции
    clan_data.sort(key=lambda x: x['position'])
    parsed_data['clans'] = clan_data

    return parsed_data

def parse_siege_screenshot(image_path):
    """
    Основная функция для парсинга скриншота осады
    """

    # Шаг 1: Получаем текст через OCR
    print(f"🔄 Обработка изображения: {image_path}")

    print("📡 Использую OCR.Space API...")
    ocr_text = ocr_space_api(image_path)

    print(ocr_text)
    # Проверяем на ошибки
    if "Ошибка" in ocr_text or ocr_text.startswith("Таймаут"):
        return {"error": ocr_text, "raw_text": ""}

    print(f"✅ Текст распознан ({len(ocr_text)} символов)")

    # Шаг 2: Парсим текст
    print("🔄 Анализ данных...")
    parsed_data = parse_ocr_text(ocr_text)
    parsed_data["raw_ocr"] = ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text

    return parsed_data


if __name__ == "__main__":
    print("=" * 60)
    print("ПАРСЕР СКРИНШОТОВ ОСАДЫ")
    print("=" * 60)

    # путь к скриншоту
    path_image = "telegram_photos/photo_1960868942_20260120_235005.jpg"

    if os.path.exists(path_image):
        result = parse_siege_screenshot(path_image)

        if "error" not in result:
            # Сохраняем результат
            with open("result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("\n💾 Результат сохранен в result.json")
        else:
            print(f"❌ API метод не сработал: {result['error']}")
    else:
        print(f"❌ Файл {path_image} не найден")
        print("Создайте скриншот или укажите правильный путь")