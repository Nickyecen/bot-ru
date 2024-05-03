import os
import discord
import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

#MUDANÇA DO BER vv (Importar o valendometro)
from valendometro.dic import *

# Carrega Token de ativação do bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Carrega bot
client = discord.Client(intents=discord.Intents.default())

dia = 0

# Cardápio atual, RU[a][b][c]
#                    |  |  |- Dia
#                    |  |- Almoço/Janta
#                    |- Qual RU
ru = [[[],[]],  # RU1: Almoço e Janta
      [[],[]],
      [[]],       # RU3: Não tem janta
      [[],[]],
      [[],[]],
      [[],[]]]

# Constantes de servidores para debug
SERVER_TESTE = 0
SERVER_MAGOS = 1

# announce: String -> Void
# Obj.: dada uma String, envia em todos os servidores a string
async def announce(string):
    for guild in client.guilds:
        await guild.text_channels[0].send(string)

# print_test: String -> void
# Obj.: dada uma string, imprime essa string no servidor de testes
async def print_test(string):
    await client.guilds[SERVER_TESTE].text_channels[0].send(string)

# organize: List List -> Void
# Obj.: Dado uma lista com uma tabela de semana de almoço ou janta
# de algum RU, organiza a tabela e coloca na segunda lista
async def organize(current_menu, organized_menus): 
    transposed_menu = []
    # Separado em 5 dias da semana com suas respectivas comidas
    organized_menu = [[],[],[],[],[]]

    # Passa por cada elemento da tabela organizando
    for row in current_menu.find_all('tr'):
        columns = row.find_all('td')
        menu_item = [element.text.strip() for element in columns]
        transposed_menu.append(menu_item)
    
    # O HTML está separado em 10 linhas, transpõe-se para 5 colunas
    for j in range(len(transposed_menu)):
        for k in range(5):
            organized_menu[k].append(transposed_menu[j][k])
    
    organized_menus.append(organized_menu)

# fetch_menu: Void -> Void
# Obj.: Pega cardápio do site e coloca na tabela do RU
async def fetch_menu():
    # Se for fim de semana, não faz nada
    if dia > 4:
        return

    # Pega tabelas do HTML do site
    url = "https://www.ufrgs.br/prae/cardapio-ru/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')

    # Organiza menus
    organized_menus = []

    num_menus = len(tables)
    if num_menus == 11:
        for menu in tables:
            await organize(menu, organized_menus)
    else:
        for i in range(0, 22, 2):
            await organize(tables[i], organized_menus)
           
    # Coloca na tabela do RU
    ru[0][0] = organized_menus[0]
    ru[0][1] = organized_menus[1]
    ru[1][0] = organized_menus[2]
    ru[1][1] = organized_menus[3]
    ru[2][0] = organized_menus[4]
   
    # Pega almoço e janta
    for i in range(3, 6):
        ru[i][0] = organized_menus[2*i-1]
        ru[i][1] = organized_menus[2*i]

# print_day_menu: Number Bboolean Boolean Number -> Void
# Obj.: Dado o número do RU, se é ou não almoço, o dia da
# semana e um servidor, envia o almoço/janta daquele dia
# naquele RU no servidor especificado
async def print_day_menu(num_ru, ehAlmoco, dia, guilda):
    # Se for fim de semana, não faz nada 
    if dia > 4:
        return

    # Prepara string com menu do dia
    ehAlmoco = 0 if ehAlmoco else 1
    day_menu = ''
    for i in range(len(ru[0][0][0])):
        day_menu += ru[num_ru-1][ehAlmoco][dia][i] + '\n'

    # Imprime menu no servidor providenciado
    await client.guilds[guilda].text_channels[0].send(day_menu)

    #MUDANÇA DO BER vv (Adicionar o valendometro)
    menu = get_menu("valendometro/menu.csv")
    valendometro = get_valendometro(menu, day_menu)
    await client.guilds[guilda].text_channels[0].send(f"Valendometro: {valendometro['valendometro']}\nPolemometro: {valendometro['polemometro']}\nReconhecidos: {valendometro['reconhecidos']}")

# Função realizada pelo bot ao ligar
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    dia = datetime.date.today().weekday()
    await fetch_menu()
    await print_day_menu(6, True, dia, SERVER_MAGOS)
    #await print_day_menu(6, True, dia, SERVER_TESTE)

# Liga o bot
client.run(TOKEN)
