import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
from map import gera_mapa
from streamlit_folium import st_folium

# Função para exibir o mapa
def exibir_mapa():
    HtmlFile = open("html/mapa_imoveis_leilao.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=500)

# Obter a data e hora atual e formatá-la
data_formatada = datetime.now().strftime("%d/%m/%Y")

# Título do aplicativo
st.set_page_config(page_title="Leilão de Imóveis", layout="wide")  # Definir título da página e layout
st.title("Imóveis disponíveis para leilão")

# Mostrar data atual com título de destaque
st.markdown(f"**Atualizado em {data_formatada}**")

# Barra lateral para navegação
st.sidebar.header("Menu de Navegação")
st.sidebar.write("Escolha uma das opções abaixo:")
opcao = st.sidebar.radio("Selecione", ("Mapa de Imóveis", "Informações Gerais"))

if opcao == "Mapa de Imóveis":
    # Se o usuário escolher "Mapa de Imóveis", exibe o mapa
    st.header("Mapa de Imóveis Disponíveis")
    st.write("""
        Filtre os imóveis pela modalidade de venda clicando nos filtros na parte superior do mapa.
    """)
    exibir_mapa()

elif opcao == "Informações Gerais":
    # Se o usuário escolher "Informações Gerais", pode adicionar mais detalhes ou outros conteúdos
    st.subheader("Sobre o Leilão")
    st.write("""
        O leilão de imóveis da Caixa Econômica Federal oferece uma grande variedade de propriedades
        que estão disponíveis para aquisição. Os imóveis incluem opções residenciais e comerciais.
        Acompanhe os imóveis e faça sua oferta diretamente pela plataforma.
    """)

# Adicionando um spinner para o mapa
#with st.spinner('Carregando mapa...'):
    # Aqui você pode adicionar o código de carregamento do mapa
    #exibir_mapa()

# Rodapé com mais informações (exemplo)
st.markdown("---")
st.markdown("**Caixa Econômica Federal - Leilão de Imóveis**")
st.write("Para mais informações, entre em contato com a Caixa Econômica Federal.")

