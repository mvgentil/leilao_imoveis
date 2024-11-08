import folium

def adicionar_marcadores(grupo_modalidade, df):
    for _, row in df.iterrows():
        # Conteúdo HTML do popup
        popup_content = f"""
        <div style="
            border: 1px solid #ddd; 
            padding: 10px; 
            font-family: Arial, sans-serif; 
            font-size: 13px; 
            color: #333;
            border-radius: 6px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.15);
            max-width: 250px;
        ">
            <h3 style="margin-top: 0; color: #4CAF50; font-size: 14px;">{row['Descrição']}</h3>
            <p style="margin: 5px 0;"><strong>Endereço:</strong> {row['Endereço']}, {row['Bairro']}</p>
            <p style="margin: 5px 0;"><strong>Cidade/UF:</strong> {row['Cidade']} - {row['UF']}</p>
            <p style="margin: 5px 0;"><strong>Preço:</strong> R$ {row['Preço']}</p>
            <p style="margin: 5px 0;"><strong>Valor de avaliação:</strong> R$ {row['Valor de avaliação']}</p>
            <p style="margin: 5px 0;"><strong>Desconto:</strong> {row['Desconto']}%</p>
            <p style="margin: 5px 0;"><strong>Modalidade de venda:</strong> {row['Modalidade de venda']}</p>
            <p style="margin: 5px 0;">
                <a href="{row['Link de acesso']}" target="_blank" style="color: #1E90FF; text-decoration: none;">Mais informações</a>
            </p>
            <button onclick="saveProperty({row['N° do imóvel']})" style="
                background-color: #4CAF50; 
                color: white; 
                padding: 5px 10px; 
                font-size: 13px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer;
                margin-top: 5px;
            ">Salvar Imóvel</button>
        </div>
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(grupo_modalidade)

def gera_mapa(df):
    # Script JavaScript para salvar imóvel
    save_script = """
    <script>
        function saveProperty(imovelId) {
            fetch('/save_property', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: imovelId }),
            }).then(response => {
                if (response.ok) {
                    alert('Imóvel salvo com sucesso!');
                } else {
                    alert('Erro ao salvar imóvel.');
                }
            });
        }
    </script>
    """
    
    # Define o centro do mapa com base na média das coordenadas
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
    
    # Adiciona o script JavaScript ao mapa
    mapa.get_root().html.add_child(folium.Element(save_script))

    # Salva o mapa em um arquivo HTML
    mapa.save("../html/mapa_imoveis_leilao.html")
    print("Mapa gerado e salvo como 'mapa_imoveis_leilao.html'")

