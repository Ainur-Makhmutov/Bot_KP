import requests
from bs4 import BeautifulSoup
import socks
import socket


socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket


