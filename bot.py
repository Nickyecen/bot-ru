import os
import discord
import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

async def fetch_menu_and_print():
    url = "https://www.ufrgs.br/prae/cardapio-ru/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    menu_table = tables[0]
    menu = []
    for row in menu_table.find_all('tr'):
        columns = row.find_all('td')
        menu_item = [column.text.strip() for column in columns]
        print(menu_item)
        menu.append(menu_item)
    # Check if menu is not empty before printing
    day_menu = ""
    if menu:
        for i in range(10):
            day_menu += menu[i][datetime.date.today().weekday()] + '\n'
    else:
        print("Menu is empty.")
    for guild in client.guilds:
        await guild.text_channels[0].send(day_menu)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await fetch_menu_and_print()

client.run(TOKEN)