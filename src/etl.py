import pandas as pd
import re
import time
from datetime import datetime

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter

data_geracao = None

# Importa o arquivo CSV
file_path = 'data/Lista_imoveis_SC.csv'
# Lê o arquivo ignorando as duas primeiras linhas e definindo a terceira como cabeçalho
df = pd.read_csv(
    file_path,
    sep=';',               # Especifica o delimitador de campo
    encoding='latin1',     # Define a codificação para evitar erros de caracteres especiais
    skiprows=2,            # Pula as duas primeiras linhas
)

# Função para extrair rua e número
def extract_street_and_number(address):
    # Expressão regular para encontrar o padrão de rua e número
    match = re.match(r'([A-Za-z\s\d\.]+),\s*N\.\s*(\d+|SN)', address)
    match = re.match(r'(.+?),\s*N\.\s*(\d+|SN)', address)
    
    if match:
        street = match.group(1).strip()
        number = match.group(2).strip()
        return street, number
    else:
        return "Desconhecido", "Desconhecido"  # Retorna None caso não encontre o padrão

# Aplicar a função para extrair rua e número
df[['Rua', 'Número']] = df['Endereço'].apply(lambda x: pd.Series(extract_street_and_number(x)))

# Carregar o CSV
df_coord = df

# Função para geocodificar com RateLimiter
def get_coordinates(row):
    # Concatena as colunas para formar o endereço completo
    address_completo = f"{row['Rua']},{row['Número']}, {row['Bairro']}, {row['Cidade']}, {row['UF']}, Brazil"
    address_sem_num = f"{row['Rua']}, {row['Bairro']}, {row['Cidade']}, {row['UF']}, Brazil"
    address_bairro = f"{row['Bairro']}, {row['Cidade']}, {row['UF']}, Brazil"
    address_cidade = f"{row['Cidade']}, {row['UF']}, Brazil"
    
    # Instancia o geolocalizador
    geolocator = Nominatim(user_agent="geolocator")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)  # Delay de 1 segundo

    # Função auxiliar para tentar geocodificar com tratamento de timeout
    def try_geocode(address):
        try:
            location = geocode(address)
            return location.latitude, location.longitude if location else (None, None)
        except GeocoderTimedOut:
            print(f"Timeout para o endereço: {address}")
            return None, None

    # Tenta geocodificar o endereço completo
    latitude, longitude = try_geocode(address_completo)
    if latitude and longitude:
        return latitude, longitude

    # Tenta geocodificar o endereço sem número
    latitude, longitude = try_geocode(address_sem_num)
    if latitude and longitude:
        return latitude, longitude

    # Tenta geocodificar o bairro
    latitude, longitude = try_geocode(address_bairro)
    if latitude and longitude:
        return latitude, longitude

    # Tenta geocodificar a cidade
    latitude, longitude = try_geocode(address_cidade)
    if latitude and longitude:
        return latitude, longitude

    # Se nenhuma tentativa teve sucesso, retorna None
    return None, None


# Criar uma lista para armazenar as coordenadas
coordenadas = []

# Iterar sobre o DataFrame e geocodificar os endereços

for _, row in df_coord.iterrows():
    lat, lon = get_coordinates(row)
    coordenadas.append((lat, lon))
    time.sleep(1)  # Atraso de 1 segundo entre as requisições para evitar rate limit

# Adicionar as coordenadas ao DataFrame
df_coord['Latitude'] = [coord[0] for coord in coordenadas]
df_coord['Longitude'] = [coord[1] for coord in coordenadas]

df_coord.to_csv(f'data/lista_imoveis_sc_coordenadas{data_geracao}.csv')
