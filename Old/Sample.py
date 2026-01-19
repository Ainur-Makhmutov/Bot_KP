import requests
import json
import uuid

# Создаем сессию для сохранения кук
session = requests.Session()

# Базовые заголовки
headers = {
    "accept": "application/json",
    "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "origin": "https://www.playdungeoncrusher.com",
    "referer": "https://www.playdungeoncrusher.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "x-client-platform": "webgl",
    "x-client-version": "1181"
}

# 1. Отправляем ping
ping_url = "https://api.playdungeoncrusher.ru/api/ping"
print("1. Отправляем ping...")
response_ping = session.get(ping_url, headers=headers)
print(f"   Status: {response_ping.status_code}")
print(f"   Response: {response_ping.text[:100]}...")

# 2. Проверяем, не пришел ли X-Session-ID в ответе на ping
print("\n2. Проверяем заголовки ответа ping:")
for key, value in response_ping.headers.items():
    if 'session' in key.lower():
        print(f"   {key}: {value}")

# 3. Отправляем session запрос
# Генерируем свой X-Session-ID если нужно
x_session_id = str(uuid.uuid4())  # Пример: "ced6c765-2d9d-47ae-91b9-27b4cd3a4cab"
print(f"\n3. Используем X-Session-ID: {x_session_id}")

session_url = "https://api.playdungeoncrusher.ru/api/session"
session_headers = headers.copy()
session_headers.update({
    "content-type": "application/json",
    "x-auth-token": "qCOqunqaUtIglXKIEBLRug==$B7Mu5ZCzlLARQ7Kff17ohRd64dENZaHUW9K3EsxX+V3BO2gVHbxhKKZgKXA9$$5AyPb+yT+kjPcevzfFxV7n+eq3KP8BLMbES8icb549YVn4YkcOVzHJcdY6te$$am6j8pIQgovQMmPq/Iby2NafvMiXCu0gCNCq3g6dF5D5h6jdc40=",
    "x-device-token": "41f1f02c-7d55-4ec5-9103-84916b629dd6",
    "x-session-id": x_session_id,  # Добавляем наш X-Session-ID
})

# Тело запроса session (попробуй разные варианты)
session_payload = {
    "device": "web",
    "platform": "webgl",
    "version": "1181",
    "client_counter": 981251,
    "client_reference": 982292
}

print("\n4. Отправляем session запрос...")
response_session = session.put(session_url,
                               headers=session_headers,
                               json=session_payload,
                               allow_redirects=False)

print(f"   Status: {response_session.status_code}")
print(f"   Response headers:")
for key, value in response_session.headers.items():
    print(f"   {key}: {value}")
print(f"\n   Response body: {response_session.text[:500]}...")