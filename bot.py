import os
import discord
import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

#MUDANÇA DO BER vv (Importar o valendometro)
from valendometro.opinioes import *
from gatherer.tablefinder import *

# Carrega Token de ativação do bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Carrega bot
client = discord.Client(intents=discord.Intents.default())

dia = 0

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

# print_day_menu: Number Bboolean Boolean Number -> Void
# Obj.: Dado o número do RU, se é ou não almoço, o dia da
# semana e um servidor, envia o almoço/janta daquele dia
# naquele RU no servidor especificado
async def print_day_menu(num_ru, ehAlmoco, dia, guilda):
    # Se for fim de semana, não faz nada 
    if dia > 4:
        return

    table = get_tables()['ru' + str(num_ru)]['almoco' if ehAlmoco else 'janta']

    day_menu = ''
    for i in range(table):
        day_menu += table[dia][i] + '\n'

    # Imprime menu no servidor providenciado
    await client.guilds[guilda].text_channels[0].send(day_menu)

    #MUDANÇA DO BER vv (Adicionar o valendometro)
    valendometro = get_today_opinion(day_menu, "valendometro/menu.csv")
    message = (
    f"Valendometro: {valendometro['valendometro']}\n"
    f"Polemometro: {valendometro['polemometro']}\n"
)
    await client.guilds[guilda].text_channels[0].send(message)

# Função realizada pelo bot ao ligar
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    dia = datetime.date.today().weekday()
    try:
        await print_day_menu(3, True, dia, SERVER_MAGOS)
    except:
        print('Erro: pegando menu 3')
        await print_day_menu(1, True, dia, SERVER_MAGOS)
    #await print_day_menu(6, True, dia, SERVER_TESTE)

# Liga o bot
client.run(TOKEN)
