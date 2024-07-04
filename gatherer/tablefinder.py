import requests
from bs4 import BeautifulSoup
from time import sleep 

# Sugerido usar no código principal com try except

def table_parser(HTMLtable):
    matrix = []

    # Iterate through each row in the table
    for row in HTMLtable.find_all('tr'):
        # Extract text from each cell in the row
        current_row = [cell.text for cell in row.find_all(['td', 'th'])]
        # Append the list of cell texts to the matrix
        matrix.append(current_row)

    return matrix

def get_tables():
    url = 'https://www.ufrgs.br/prae/cardapio-ru/'

    response = requests.get(url)

    # Erro 1
    response.raise_for_status()

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    tablesRU = {}

    for i in range (1, 7):
        
        if i != 3:
            img = soup.find('img', src='https://www.ufrgs.br/prae/wp-content/uploads/2019/03/img-ru' + str(i) + '.png')

        else:
            img = soup.find('img', src='https://www.ufrgs.br/prae/wp-content/uploads/2019/03/img-ru-0' + str(i) + '.png')

        if not img:
            #Erro 2
            print('https://www.ufrgs.br/prae/wp-content/uploads/2019/03/img-ru' + str(i) + '.png')
            raise ValueError("Specified image not found in the HTML content.")

        tables = {'almoco' : table_parser(img.find_next('table')), 
                  'janta' : table_parser(img.find_next('table').find_next('table'))}
        
        #ru 3 não tem janta
        if i == 3:
            tables['janta'] = tables['almoco']

        tablesRU['ru' + str(i)] = tables


    return tablesRU

#EXEMPLO DE USO DO TABLESRU
#tablesRU = get_tables()
#print(tablesRU['ru1']['almoco'])

tabesRU = get_tables()
print(len(tabesRU['ru1']['almoco']))