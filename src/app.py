import streamlit as st
import pandas as pd
import re
import streamlit.components.v1 as components
from datetime import datetime
from map import gera_mapa

file_path_coord = 'data/lista_imoveis_sc_coordenadas.csv'
file_path = 'data/Lista_imoveis_SC.csv'
def get_data_geracao(file_path):
    data_geracao = None  # Valor padrão caso não encontre a data

    with open(file_path, 'r', encoding='latin1') as file:
        for line in file:
            date_match = re.search(r'\d{2}/\d{2}/\d{4}', line)
            if date_match:
                data_geracao = datetime.strptime(date_match.group(), "%d/%m/%Y").strftime("%d/%m/%Y")
                break  # Interrompe a leitura ao encontrar a data

    if data_geracao is None:
        raise ValueError("Data de geração não encontrada no arquivo.")
    
    return data_geracao


# Função para exibir o mapa
def exibir_mapa():
    HtmlFile = open("html/mapa_imoveis_leilao.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=600)

# Obter a data e hora atual e formatá-la
data_geracao = get_data_geracao(file_path)


# Título do aplicativo
st.set_page_config(page_title="Leilão de Imóveis",
                    page_icon=":house:",
                    initial_sidebar_state="auto",
                    menu_items={
                        'Get Help': 'https://www.caixa.gov.br/voce/habitacao/imoveis-venda/Paginas/default.aspx',
                        'About': "Leilão de Imóveis da Caixa Econômica Federal"
                    },
                    layout="wide")  # Definir título da página e layout


# Barra lateral para navegação
st.sidebar.header("Menu de Navegação")
opcao = st.sidebar.radio("Selecione", ("Mapa de Imóveis", "Informações Gerais",
                                        "Lista de Imóveis Salvos", "Análise de viabilidade econômica")) 

if opcao == "Mapa de Imóveis":
    # Se o usuário escolher "Mapa de Imóveis", exibe o mapa
    st.header("Mapa de Imóveis Disponíveis")
    # Mostrar data atual com título de destaque
    if data_geracao is not None:
        st.markdown(f"**Atualizado em {data_geracao}**")
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
        Para mais informações consulte o site da Caixa Econômica Federal [link](https://www.caixa.gov.br/voce/habitacao/imoveis-venda/Paginas/default.aspx).
    """)
elif opcao == "Lista de Imóveis Salvos":
    # Se o usuário escolher "Lista de Imóveis Salvos", exibe uma tabela com os imóveis salvos
    st.subheader("Lista de Imóveis Salvos")
    st.write("""
        Em breve...
    """)

elif opcao == "Análise de viabilidade econômica":
    # Se o usuário escolher "Análise de viabilidade", pode adicionar mais detalhes ou outros conteúdos
    st.subheader("Análise de Viabilidade Econômica")
    st.write("""Em breve...""")

# Adicionando um spinner para o mapa
#with st.spinner('Carregando mapa...'):
    # Aqui você pode adicionar o código de carregamento do mapa
    #exibir_mapa()

# Rodapé com mais informações (exemplo)
st.markdown("---")
st.markdown("**Caixa Econômica Federal - Leilão de Imóveis**")
st.write("Para mais informações consulte o site da Caixa Econômica Federal [link](https://www.caixa.gov.br/voce/habitacao/imoveis-venda/Paginas/default.aspx).")

