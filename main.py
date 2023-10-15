import os
from bs4 import BeautifulSoup  # del módulo bs4, necesitamos BeautifulSoup
import schedule
import logging
from dotenv import load_dotenv

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import pandas as pd

# Configurar el sistema de registro (logging)
logging.basicConfig(filename='errores.log', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

load_dotenv()

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT-ID")


def bot_send_text(bot_message):

    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + \
        CHAT_ID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def scraping():

    driver = webdriver.Chrome()
    url = 'https://www.zooplus.es/shop/tienda_gatos/comida_humeda/felix/so_gut_fantastic/620449'
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Encuentra todos los div con las clases especificadas
    divs = soup.find_all('div', attrs={"data-zta": "product-variant"})

    precios = []
    descripciones = []

    for div in divs:
        # Encuentra el span dentro de cada div
        span = div.find('span', class_='z-price__amount z-price__amount--standard')
        span_desc = div.find("span", attrs={"data-zta":"variantDescription"})
        
        # Comprueba si se encontró un span y extrae su contenido
        if span:
            price = span.get_text(strip=True)
            precios.append(price)

        if span_desc:
            desc = span_desc.get_text(strip=True).replace("\n", "").replace("  ", "")
            descripciones.append(desc)

        

    data = {
        'Precio': precios,
        'Descripción': descripciones
    }

    df = pd.DataFrame(data)
    print(df)

    return df.to_string(index=False)

def report():

    try:
        valor = scraping()

        if valor != None:
            price = f'El precio de Felix Fantastic 120 x 85 g - Jumbopack es de {valor}'
            bot_send_text(price)
        else:
            bot_send_text("Algo raro pasa, mira logs")
    except Exception as e:
        logging.error("Ocurrió una excepción:", exc_info=True)



if __name__ == '__main__':

    report()

    #schedule.every().day.at("10:00").do(report)
#
    #while True:
    #    schedule.run_pending()
