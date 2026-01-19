import requests


def ocr_space_url(image_url, api_key='YOUR_API_KEY'):
    """Распознавание текста по URL изображения"""

    url = "https://api.ocr.space/parse/image"

    payload = {
        'apikey': api_key,
        'url': image_url,  # URL изображения
        'language': 'rus',
        'isOverlayRequired': False,
        'OCREngine': 2,
        'detectOrientation': True,
        'scale': True
    }

    try:
        response = requests.post(url, data=payload, timeout=30)
        result = response.json()

        print(f"Статус: {response.status_code}")

        if result.get('IsErroredOnProcessing', True) == False:
            text = result['ParsedResults'][0]['ParsedText']
            return text.strip()
        else:
            error_msg = result.get('ErrorMessage', ['Неизвестная ошибка'])
            return f"Ошибка API: {error_msg}"

    except Exception as e:
        return f"Ошибка: {str(e)}"


# Использование
image_url = 'https://i.imgur.com/MvHLuRM.jpeg'
api_key = 'K88266104688957'  # или ваш ключ

result = ocr_space_url(image_url, api_key)
print(result)