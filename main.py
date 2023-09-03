import os
from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup
import requests
import schedule

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT-ID")


def bot_send_text(bot_message):

    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def scraping():
    url = requests.get('https://www.zooplus.es/shop/tienda_gatos/comida_humeda/felix/so_gut_fantastic/620449')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find(attrs={'data-zta': 'productStandardPriceAmount'})
    format_result = result.text
    return format_result

def report():
    price = f'El precio de Felix Fantastic 120 x 85 g - Jumbopack es de {scraping()}'
    bot_send_text(price)

if __name__ == '__main__':

    report()
        
    schedule.every().day.at("19:00").do(report)

    while True:
        schedule.run_pending()