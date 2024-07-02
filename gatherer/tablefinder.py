import requests
from bs4 import BeautifulSoup

# Sugerido usar no código principal com try except

def get_table():
    url = 'https://www.ufrgs.br/prae/cardapio-ru/'

    response = requests.get(url)

    # Erro 1
    response.raise_for_status()

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    img = soup.find('img', src='https://www.ufrgs.br/prae/wp-content/uploads/2019/03/img-ru6.png')

    if not img:
        #Erro 2
        raise ValueError("Specified image not found in the HTML content.")

    next_table = img.find_next('table')
    
    if not next_table:
        #Erro 3
        raise ValueError("No table found after the specified image.")

    return next_table