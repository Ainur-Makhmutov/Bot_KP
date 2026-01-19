from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_tokens_from_browser():
    """Автоматический вход в игру и получение токенов"""
    driver = webdriver.Chrome()
    driver.get("https://www.playdungeoncrusher.com/")

    # Ждем загрузки и авторизации
    time.sleep(500)

    # Получаем куки
    cookies = driver.get_cookies()

    # Запускаем перехватчик трафика через DevTools Protocol
    # (сложная часть, требует настройки proxy или CDP)

    driver.quit()
    return cookies

get_tokens_from_browser()