import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# Função para exibir o mapa
def exibir_mapa():
    HtmlFile = open("html/mapa_imoveis_leilao.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=600)

# Obter a data e hora atual e formatá-la
data_formatada = datetime.now().strftime("%d/%m/%Y")

# Título do aplicativo
st.set_page_config(page_title="Leilão de Imóveis", layout="wide")  # Definir título da página e layout


# Barra lateral para navegação
st.sidebar.header("Menu de Navegação")
st.sidebar.write("Escolha uma das opções abaixo:")
opcao = st.sidebar.radio("Selecione", ("Mapa de Imóveis", "Informações Gerais",
                                        "Lista de Imóveis Salvos", "Análise de viabilidade econômica")) 

if opcao == "Mapa de Imóveis":
    # Se o usuário escolher "Mapa de Imóveis", exibe o mapa
    st.header("Mapa de Imóveis Disponíveis")
    # Mostrar data atual com título de destaque
    st.markdown(f"**Atualizado em {data_formatada}**")
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
    st.header("Lista de Imóveis Salvos")
    # Mostrar data atual com título de destaque
    st.markdown(f"**Atualizado em {data_formatada}**")
    # Importa o arquivo CSV
    file_path = 'data/Lista_imoveis_SC.csv'
    # Lê o arquivo ignorando as duas primeiras linhas e definindo a terceira como cabeçalho
    df = pd.read_csv(
        file_path,
        sep=';',               # Especifica o delimitador de campo
        encoding='latin1',     # Define a codificação para evitar erros de caracteres especiais
        skiprows=2,            # Pula as duas primeiras linhas
    )
    st.write(df)
    st.write("Para salvar um imovel, clique no botão 'Salvar' na tabela.")

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

