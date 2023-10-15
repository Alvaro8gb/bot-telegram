from bs4 import BeautifulSoup
import pandas as pd

with open("base.html") as f:
    html = f.read()

# Parsea el HTML
soup = BeautifulSoup(html, 'html.parser')

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

