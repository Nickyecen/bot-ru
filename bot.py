import os
import discord
import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

#MUDANÇA DO BER vv (Importar o valendometro)
from valendometro.dic import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

dia = 0

ru = [[[],[]],  # RU1: Almoço e Janta
      [[],[]],
      [[]],       # RU3: Não tem janta
      [[],[]],
      [[],[]],
      [[],[]]]

SERVER_TESTE = 0
SERVER_MAGOS = 1

async def announce(string):
    for guild in client.guilds:
        await guild.text_channels[0].send(string)

async def print_test(string):
    await client.guilds[0].text_channels[0].send(string)

async def fetch_menu():
    if dia > 4:
        return null

    url = "https://www.ufrgs.br/prae/cardapio-ru/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')

    parsed_menus = []

    for i in range(22):
        if i%2 == 1:
            continue
        current_menu = tables[i]
        transposed_menu = []
        parsed_menu = [[],[],[],[],[]]
        for row in current_menu.find_all('tr'):
            columns = row.find_all('td')
            menu_item = [element.text.strip() for element in columns]
            transposed_menu.append(menu_item)
        for j in range(len(transposed_menu)):
            for k in range(5):
                parsed_menu[k].append(transposed_menu[j][k])
        
        parsed_menus.append(parsed_menu)

    ru[0][0] = parsed_menus[0]
    ru[0][1] = parsed_menus[1]
    ru[1][0] = parsed_menus[2]
    ru[1][1] = parsed_menus[3]
    ru[2][0] = parsed_menus[4]
    
    for i in range(3, 6):
        ru[i][0] = parsed_menus[2*i-1]
        ru[i][1] = parsed_menus[2*i]

async def print_day_menu(num_ru, ehAlmoco, dia, guilda):
   
    if dia > 4:
        return

    ehAlmoco = 0 if ehAlmoco else 1
    day_menu = ''
    for i in range(len(ru[0][0][0])):
        day_menu += ru[num_ru-1][ehAlmoco][dia][i] + '\n'

    await client.guilds[guilda].text_channels[0].send(day_menu)

    #MUDANÇA DO BER vv (Adicionar o valendometro)
    menu = get_menu("valendometro/menu.csv")
    valendometro = get_valendometro(menu, day_menu)
    await client.guilds[guilda].text_channels[0].send(f"Valendometro: {valendometro['valendometro']}\nPolemometro: {valendometro['polemometro']}")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await announce("Acordei, gurizada")
    dia = datetime.date.today().weekday()
    await fetch_menu()
    await print_day_menu(6, True, dia, SERVER_MAGOS)
    
client.run(TOKEN)
