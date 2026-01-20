import requests
from bs4 import BeautifulSoup
import socks
import socket


socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    print(soup.find('body').text)

def check_ip_with_country():
    """Проверка IP с определением страны"""
    try:
        # Получаем IP
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        ip_address = response.json()['ip']
        print(f"🌐 Ваш IP: {ip_address}")

        # Используем ip-api для получения полной информации
        geo_response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10)
        geo_data = geo_response.json()

        if geo_data['status'] == 'success':
            print("\n📊 Геолокационные данные:")
            print(f"   Страна: {geo_data.get('country', 'N/A')}")
            print(f"   Код страны: {geo_data.get('countryCode', 'N/A')}")
            print(f"   Регион: {geo_data.get('regionName', 'N/A')}")
            print(f"   Город: {geo_data.get('city', 'N/A')}")
            print(f"   Почтовый индекс: {geo_data.get('zip', 'N/A')}")
            print(f"   Широта/Долгота: {geo_data.get('lat', 'N/A')}/{geo_data.get('lon', 'N/A')}")
            print(f"   Часовой пояс: {geo_data.get('timezone', 'N/A')}")
            print(f"   Провайдер: {geo_data.get('isp', 'N/A')}")
            print(f"   Организация: {geo_data.get('org', 'N/A')}")
            print(f"   AS: {geo_data.get('as', 'N/A')}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    print("=" * 50)
    checkIP()
    print("=" * 50)
    check_ip_with_country()