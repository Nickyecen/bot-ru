import requests
from bs4 import BeautifulSoup

URL = 'https://www.ufrgs.br/prae/cardapio-ru/'

def get_html(url):
    return requests.get(url).text

def get_containers(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('a', class_='elementor-toggle-title')
    tables = soup.find_all('table')
    return titles, tables

print(get_containers(get_html(URL)))
