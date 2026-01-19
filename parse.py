import requests
import json
from pprint import pprint

url = "https://api.playdungeoncrusher.ru/api/clans/2664fbea-24c8-48d2-8fd5-11a8111a5f92/?bonuses=1"

# ВАЖНО: Эти заголовки МАНДАТОРНЫ для этой игры!
headers = {
    # === ОСНОВНЫЕ ЗАГОЛОВКИ ===
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "cache-control": "no-cache",
    "content-type": "gzip/json",  # Необычный content-type!
    "origin": "https://www.playdungeoncrusher.com",
    "pragma": "no-cache",
    "referer": "https://www.playdungeoncrusher.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",

    # === АВТОРИЗАЦИЯ И ИДЕНТИФИКАЦИЯ (САМОЕ ВАЖНОЕ!) ===
    "x-auth-token": "qCOqunqaUtIglXKIEBLRug==$B7Mu5ZCzlLARQ7Kff17ohRd64dENZaHUW9K3EsxX+V3BO2gVHbxhKKZgKXA9$$5AyPb+yT+kjPcevzfFxV7n+eq3KP8BLMbES8icb549YVn4YkcOVzHJcdY6te$$am6j8pIQgovQMmPq/Iby2NafvMiXCu0gCNCq3g6dF5D5h6jdc40=",
    "x-client-platform": "webgl",
    "x-client-version": "1181",
    "x-device-token": "41f1f02c-7d55-4ec5-9103-84916b629dd6",
    "x-request-cid": "8df608a7-254d-4cbb-bfe7-ff6628958598",
    "x-session-id": "50e8f536-182c-4f48-9a55-909b5c776ef2",

    # === ДОПОЛНИТЕЛЬНЫЕ ===
    "priority": "u=1, i",
    "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
}

try:
    print("Отправляем запрос к API игры...")

    # Отправляем GET запрос (метод виден в "Request Method: GET")
    response = requests.get(url, headers=headers)

    print(f"Статус код: {response.status_code}")
    print(f"Заголовки ответа:")
    for key, value in response.headers.items():
        if key.startswith('x-') or key in ['content-type', 'cache-control']:
            print(f"  {key}: {value}")

    if response.status_code == 200:
        print("\n=== УСПЕХ! ДАННЫЕ ПОЛУЧЕНЫ ===")

        # Парсим JSON ответ
        data = response.json()

        # Красиво выводим структуру
        print(f"Тип ответа: {type(data)}")

        if isinstance(data, dict):
            print("\nКлючи в ответе:")
            for key in data.keys():
                print(f"  - {key}")

            # Покажем немного данных для понимания структуры
            print("\nПример данных:")
            for key, value in list(data.items())[:3]:  # Первые 3 элемента
                print(f"{key}: {type(value)}")
                if isinstance(value, (list, dict)) and len(str(value)) > 100:
                    print(f"  Размер: {len(value) if isinstance(value, (list, dict)) else 'N/A'}")
                else:
                    print(f"  Значение: {value}")

        elif isinstance(data, list):
            print(f"\nЭто список из {len(data)} элементов")
            if len(data) > 0:
                print(f"Первый элемент: {type(data[0])}")
                print(f"Пример: {data[0]}")

        # Сохраняем в файл для дальнейшего анализа
        with open('boss_sieges_scores.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nПолные данные сохранены в файл: boss_sieges_scores.json")

        # Анализ содержимого (предполагаемая структура)
        print("\n=== АНАЛИЗ СТРУКТУРЫ ДАННЫХ ===")
        if isinstance(data, dict) and 'scores' in data:
            print("Найдены результаты (scores)")
        if isinstance(data, dict) and 'players' in data:
            print(f"Данные игроков: {len(data['players'])} записей")

    else:
        print(f"\nОшибка {response.status_code}:")
        print(response.text[:500])  # Первые 500 символов ошибки

except requests.exceptions.RequestException as e:
    print(f"Ошибка сети: {e}")
except json.JSONDecodeError as e:
    print(f"Ошибка парсинга JSON: {e}")
    print(f"Ответ сервера (первые 500 символов):")
    print(response.text[:500])
except Exception as e:
    print(f"Неожиданная ошибка: {e}")