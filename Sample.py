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


# ====== Парсит текст, полученный из OCR, в структурированный формат ======
def parse_siege_ocr_text(ocr_text):

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

    return result



# ====== ОСНОВНАЯ ФУНКЦИЯ ======
def parse_siege_screenshot(image_path):
    """
    Основная функция для парсинга скриншота осады
    """

    # Шаг 1: Получаем текст через OCR
    print(f"🔄 Обработка изображения: {image_path}")

    print("📡 Использую OCR.Space API...")
    ocr_text = ocr_space_api(image_path)

    # Проверяем на ошибки
    if "Ошибка" in ocr_text or ocr_text.startswith("Таймаут"):
        return {"error": ocr_text, "raw_text": ""}

    print(f"✅ Текст распознан ({len(ocr_text)} символов)")

    # Шаг 2: Парсим текст
    print("🔄 Анализ данных...")
    parsed_data = parse_siege_ocr_text(ocr_text)
    parsed_data["raw_ocr"] = ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text

    return parsed_data


if __name__ == "__main__":
    print("=" * 60)
    print("ПАРСЕР СКРИНШОТОВ ОСАДЫ")
    print("=" * 60)

    # путь к скриншоту
    path_image = "telegram_photos/photo_1960868942_20260119_190015.jpg"

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