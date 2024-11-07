import folium

# Função para adicionar marcadores de imóveis ao mapa
def adicionar_marcadores(map, df):
    for _, row in df.iterrows():
        popup_content = f"""
            <strong>Descrição:</strong> : {row['Descrição']}<br>
            <strong>Endereço:</strong> {row['Endereço']}<br>
            <strong>Bairro:</strong> {row['Bairro']}<br>
            <strong>Cidade:</strong> {row['Cidade']}<br>
            <strong>UF:</strong> {row['UF']}<br>
            <strong>Preço:</strong> R$ {row['Preço']}<br>
            <strong>Valor de avaliação:</strong> R$ {row['Valor de avaliação']}<br>
            <strong>Desconto:</strong> {row['Desconto']}%<br>
            <strong>Modalidade de venda:</strong> : {row['Modalidade de venda']}<br>
            <strong>Link de acesso:</strong> : <a href="{row['Link de acesso']}" target="_blank">Mais informações</a>
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(map)

def gera_mapa(df):
    # Configuração do mapa centralizado na média das coordenadas
    centro_lat = df['Latitude'].mean()
    centro_lon = df['Longitude'].mean()
    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=8)

    # Criação de grupos de imóveis filtrados por modalidade
    modalidades = df['Modalidade de venda'].unique()

    for modalidade in modalidades:
        grupo_modalidade = folium.FeatureGroup(name=f"Modalidade: {modalidade}")
        mapa.add_child(grupo_modalidade)

        # Filtra os imóveis por modalidade
        df_modalidade = df[df['Modalidade de venda'] == modalidade]

        # Adiciona os marcadores de imóveis dessa modalidade
        adicionar_marcadores(grupo_modalidade, df_modalidade)

    # Adiciona controle de camadas para o usuário escolher a modalidade de venda
    folium.LayerControl(collapsed=False).add_to(mapa)

    # Salva o mapa em um arquivo HTML
    mapa.save("mapa_imoveis_leilao.html")

    print("Mapa gerado e salvo como 'mapa_imoveis_leilao.html'")