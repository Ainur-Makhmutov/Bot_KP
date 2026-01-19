import requests
import pytesseract
from PIL import Image
import os
import json
import re

# ====== OCR ФУНКЦИИ ======
# OCR.Space API
def ocr_space_api(image_path, api_key='K88266104688957'):

    try:
        with open(image_path, 'rb') as image_file:
            url = "https://api.ocr.space/parse/image"

            payload = {
                'apikey': api_key,  # Бесплатный демо-ключ
                'language': 'rus',  # Русский язык
                'isOverlayRequired': False,
                'OCREngine': 2  # Более точный движок
            }

            files = {'image': image_file}

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


# Локальный Tesseract
def ocr_local(image_path):
    """
    Локальный OCR с помощью Tesseract
    Установите:
    1. pip install pytesseract pillow
    2. Установите Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
    """
    try:
        # Открываем изображение
        image = Image.open(image_path)

        # Извлекаем текст
        text = pytesseract.image_to_string(image, lang='rus+eng')

        return text.strip()
    except Exception as e:
        return f"Ошибка OCR: {str(e)}"


# ====== ПАРСЕР ДЛЯ СКРИНШОТОВ ОСАДЫ ======
def parse_siege_ocr_text(ocr_text):
    """
    Парсит текст, полученный из OCR, в структурированный формат
    """
    result = {
        "event": "Осада — Ледяная пустошь",
        "week": "Текущая неделя",
        "total_players": "2164",
        "players": []
    }

    lines = ocr_text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    # Ищем общее количество игроков
    for line in lines:
        if 'Всего:' in line:
            # Извлекаем число после "Всего:"
            match = re.search(r'Всего:\s*(\d+)', line)
            if match:
                result["total_players"] = match.group(1)

    # Ищем игроков с очками (длинные числа)
    player_pattern = re.compile(r'(.+?)\s+(\d{7,})\b')

    for line in lines:
        # Пропускаем заголовки
        if 'Осада' in line or 'Текущая' in line or 'Игроки' in line or 'Всего:' in line:
            continue

        # Ищем шаблон "имя очки"
        match = player_pattern.search(line)
        if match:
            name = match.group(1).strip()
            score = match.group(2).strip()

            # Очищаем имя от лишних символов
            name = re.sub(r'[^\w\s\[\]\-\(\)]', '', name)

            result["players"].append({
                "position": len(result["players"]) + 1,
                "name": name,
                "score": int(score) if score.isdigit() else score
            })

    # Если не нашли через regex, попробуем ручной парсинг
    if not result["players"]:
        result = manual_parse_fallback(lines)

    return result

# Ручной парсинг для сложных случаев
def manual_parse_fallback(lines):
    """
    Ручной парсинг для сложных случаев
    """
    result = {
        "event": "Осада — Ледяная пустошь",
        "week": "Текущая неделя",
        "total_players": "2164",
        "players": []
    }

    position = 1
    i = 0

    while i < len(lines) and position <= 10:  # Максимум 10 игроков
        line = lines[i]

        # Пропускаем заголовки
        if any(keyword in line for keyword in ['Осада', 'Текущая', 'Игроки', 'Всего:', 'Кланы']):
            i += 1
            continue

        # Ищем очень длинные числа (очки)
        numbers = re.findall(r'\b\d{7,}\b', line)

        if numbers and len(numbers[0]) >= 7:
            score = numbers[0]

            # Имя - все перед числом
            name_part = line.split(score)[0].strip()

            # Если есть предыдущая строка без чисел, возможно это часть имени
            if i > 0 and not re.search(r'\d{7,}', lines[i - 1]):
                name_part = lines[i - 1] + " " + name_part

            if name_part:
                result["players"].append({
                    "position": position,
                    "name": name_part,
                    "score": score
                })
                position += 1

        i += 1

    return result


# ====== ОСНОВНАЯ ФУНКЦИЯ ======
def parse_siege_screenshot(image_path):
    """
    Основная функция для парсинга скриншота осады
    """

    # Шаг 1: Получаем текст через OCR
    print(f"🔄 Обработка изображения: {image_path}")

    print("📡 Использую OCR.Space API...")
    ocr_text = ocr_local(image_path)

    # Проверяем на ошибки
    if "Ошибка" in ocr_text or ocr_text.startswith("Таймаут"):
        return {"error": ocr_text, "raw_text": ""}

    print(f"✅ Текст распознан ({len(ocr_text)} символов)")

    # Шаг 2: Парсим текст
    print("🔄 Анализ данных...")
    parsed_data = parse_siege_ocr_text(ocr_text)
    parsed_data["raw_ocr"] = ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text

    return parsed_data


# ====== ИНТЕГРАЦИЯ С TELEGRAM БОТОМ ======
def setup_telebot_integration(bot_instance, save_folder="telegram_photos"):
    """
    Настройка обработчиков для Telegram бота
    """

    @bot_instance.message_handler(commands=['parse_last'])
    def parse_last_screenshot(message):
        """Парсит последнее сохраненное фото"""
        try:
            if not os.path.exists(save_folder):
                bot_instance.reply_to(message, "❌ Папка с фото не существует")
                return

            files = os.listdir(save_folder)
            image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

            if not image_files:
                bot_instance.reply_to(message, "❌ Нет сохраненных фото для парсинга")
                return

            # Сортируем по времени изменения
            image_files.sort(key=lambda x: os.path.getmtime(os.path.join(save_folder, x)), reverse=True)
            latest_file = image_files[0]
            filepath = os.path.join(save_folder, latest_file)

            bot_instance.reply_to(message, f"🔄 Парсинг {latest_file}...")

            # Пробуем API сначала, потом локальный
            result = parse_siege_screenshot(filepath, method='api')

            if "error" in result:
                bot_instance.reply_to(message, f"API не сработал, пробую локальный OCR...")
                result = parse_siege_screenshot(filepath, method='local')

            if "error" in result:
                bot_instance.reply_to(message, f"❌ Ошибка: {result['error']}")
                return

            # Формируем красивый ответ
            response = "🎮 *РЕЗУЛЬТАТЫ ОСАДЫ*\n\n"
            response += f"*Событие:* {result.get('event', 'Осада')}\n"
            response += f"*Неделя:* {result.get('week', 'Текущая')}\n"
            response += f"*Всего игроков:* {result.get('total_players', '?')}\n\n"
            response += "*ТОП ИГРОКИ:*\n"

            for player in result.get("players", [])[:5]:
                score_formatted = f"{int(player['score']):,}".replace(",", ".")
                response += f"{player['position']}. {player['name']}\n   🏆 `{score_formatted}`\n"

            if len(result.get("players", [])) > 5:
                response += f"\n... и еще {len(result['players']) - 5} игроков"

            bot_instance.reply_to(message, response, parse_mode='Markdown')

            # Сохраняем в JSON файл
            json_path = filepath.replace('.jpg', '.json').replace('.png', '.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

        except Exception as e:
            bot_instance.reply_to(message, f"❌ Критическая ошибка: {str(e)}")


if __name__ == "__main__":
    # Демонстрация работы
    print("=" * 60)
    print("ПАРСЕР СКРИНШОТОВ ОСАДЫ")
    print("=" * 60)

    # путь к скриншоту
    path_image = "telegram_photos/photo_1960868942_20260119_190015.jpg"

    if os.path.exists(path_image):
        print("\n1. Тестируем с API методом:")
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