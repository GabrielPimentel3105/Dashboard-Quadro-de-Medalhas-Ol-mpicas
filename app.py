"""
Dashboard Interativo — Quadro de Medalhas Olímpicas
Baseado no tutorial da disciplina, com filtros e gráfico de pizza.
Execute localmente: python app.py
Render: gunicorn app:server
"""
import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(BASE_DIR, "Country_Medals.csv")

# O arquivo é salvo com separador ;, como no tutorial-base.
df = pd.read_csv(ARQUIVO_DADOS, sep=";")
# Mantém os nomes originais em inglês para o Plotly localizar corretamente
# os países no mapa e cria colunas traduzidas para exibição na interface.
TRADUCAO_PAISES = {
    "Afghanistan": "Afeganistão", "Algeria": "Argélia", "Argentina": "Argentina",
    "Armenia": "Armênia", "Australasia": "Australásia", "Australia": "Austrália",
    "Austria": "Áustria", "Azerbaijan": "Azerbaijão", "Bahamas": "Bahamas",
    "Bahrain": "Barein", "Barbados": "Barbados", "Belarus": "Belarus",
    "Belgium": "Bélgica", "Bermuda": "Bermudas", "Bohemia": "Boêmia",
    "Botswana": "Botsuana", "Brazil": "Brasil", "British West Indies": "Índias Ocidentais Britânicas",
    "Bulgaria": "Bulgária", "Burkina Faso": "Burkina Faso", "Burundi": "Burundi",
    "Cameroon": "Camarões", "Canada": "Canadá", "Ceylon": "Ceilão",
    "Chile": "Chile", "China": "China", "Chinese Taipei": "Taipé Chinês",
    "Colombia": "Colômbia", "Costa Rica": "Costa Rica", "Croatia": "Croácia",
    "Cuba": "Cuba", "Cyprus": "Chipre", "Czech Republic": "República Tcheca",
    "Czechoslovakia": "Tchecoslováquia", "Denmark": "Dinamarca", "Djibouti": "Djibuti",
    "Dominican Republic": "República Dominicana", "East Germany": "Alemanha Oriental",
    "Ecuador": "Equador", "Egypt": "Egito", "Eritrea": "Eritreia",
    "Estonia": "Estônia", "Ethiopia": "Etiópia", "Fiji": "Fiji",
    "Finland": "Finlândia", "France": "França", "Gabon": "Gabão",
    "Georgia": "Geórgia", "Germany": "Alemanha", "Ghana": "Gana",
    "Great Britain": "Grã-Bretanha", "Greece": "Grécia", "Grenada": "Granada",
    "Guatemala": "Guatemala", "Guyana": "Guiana", "Haiti": "Haiti",
    "Hong Kong": "Hong Kong", "Hungary": "Hungria", "Iceland": "Islândia",
    "Independent Olympic Athletes": "Atletas Olímpicos Independentes",
    "Independent Olympic Participants": "Participantes Olímpicos Independentes",
    "India": "Índia", "Indonesia": "Indonésia", "Iran": "Irã", "Iraq": "Iraque",
    "Ireland": "Irlanda", "Israel": "Israel", "Italy": "Itália", "Ivory Coast": "Costa do Marfim",
    "Jamaica": "Jamaica", "Japan": "Japão", "Jordan": "Jordânia", "Kazakhstan": "Cazaquistão",
    "Kenya": "Quênia", "Kosovo": "Kosovo", "Kuwait": "Kuwait", "Kyrgyzstan": "Quirguistão",
    "Latvia": "Letônia", "Lebanon": "Líbano", "Lithuania": "Lituânia", "Luxembourg": "Luxemburgo",
    "Macedonia": "Macedônia", "Malaysia": "Malásia", "Mauritius": "Maurício", "Mexico": "México",
    "Mixed team": "Equipe mista", "Moldova": "Moldávia", "Mongolia": "Mongólia",
    "Montenegro": "Montenegro", "Morocco": "Marrocos", "Mozambique": "Moçambique",
    "Namibia": "Namíbia", "Netherlands": "Países Baixos", "Netherlands Antilles": "Antilhas Neerlandesas",
    "New Zealand": "Nova Zelândia", "Niger": "Níger", "Nigeria": "Nigéria",
    "North Korea": "Coreia do Norte", "North Macedonia": "Macedônia do Norte", "Norway": "Noruega",
    "Pakistan": "Paquistão", "Panama": "Panamá", "Paraguay": "Paraguai", "Peru": "Peru",
    "Philippines": "Filipinas", "Poland": "Polônia", "Portugal": "Portugal", "Puerto Rico": "Porto Rico",
    "Qatar": "Catar", "ROC": "Comitê Olímpico Russo (ROC)", "Republic of China": "República da China",
    "Romania": "Romênia", "Russia": "Rússia", "Russian Empire": "Império Russo", "Samoa": "Samoa",
    "San Marino": "San Marino", "Saudi Arabia": "Arábia Saudita", "Senegal": "Senegal",
    "Serbia": "Sérvia", "Serbia and Montenegro": "Sérvia e Montenegro", "Singapore": "Singapura",
    "Slovakia": "Eslováquia", "Slovenia": "Eslovênia", "South Africa": "África do Sul",
    "South Korea": "Coreia do Sul", "Soviet Union": "União Soviética", "Spain": "Espanha",
    "Sri Lanka": "Sri Lanka", "Sudan": "Sudão", "Suriname": "Suriname", "Sweden": "Suécia",
    "Switzerland": "Suíça", "Syria": "Síria", "Tajikistan": "Tajiquistão", "Tanzania": "Tanzânia",
    "Thailand": "Tailândia", "Togo": "Togo", "Tonga": "Tonga", "Trinidad and Tobago": "Trinidad e Tobago",
    "Tunisia": "Tunísia", "Turkey": "Turquia", "Turkmenistan": "Turcomenistão", "Uganda": "Uganda",
    "Ukraine": "Ucrânia", "Unified Team": "Equipe Unificada", "United Arab Emirates": "Emirados Árabes Unidos",
    "United States": "Estados Unidos", "United Team of Germany": "Equipe Unificada da Alemanha",
    "Uruguay": "Uruguai", "Uzbekistan": "Uzbequistão", "Venezuela": "Venezuela",
    "Vietnam": "Vietnã", "Virgin Islands": "Ilhas Virgens", "West Germany": "Alemanha Ocidental",
    "Yugoslavia": "Iugoslávia", "Zambia": "Zâmbia", "Zimbabwe": "Zimbábue"
}
TRADUCAO_SEDES = {
    "Australia": "Austrália", "Belgium": "Bélgica", "Brazil": "Brasil", "Canada": "Canadá",
    "China": "China", "Finland": "Finlândia", "France": "França", "Germany": "Alemanha",
    "Great Britain": "Grã-Bretanha", "Greece": "Grécia", "Italy": "Itália", "Japan": "Japão",
    "Mexico": "México", "Netherlands": "Países Baixos", "South Korea": "Coreia do Sul",
    "Soviet Union": "União Soviética", "Spain": "Espanha", "Sweden": "Suécia",
    "United States": "Estados Unidos", "West Germany": "Alemanha Ocidental"
}
df["Country_Display"] = df["Country_Name"].map(TRADUCAO_PAISES).fillna(df["Country_Name"])
df["Host_Display"] = df["Host_country"].map(TRADUCAO_SEDES).fillna(df["Host_country"])
df["Total_Medals"] = df[["Gold", "Silver", "Bronze"]].sum(axis=1)

# O tutorial trabalha com o período de 1992 a 2020.
df = df[(df["Year"] >= 1992) & (df["Year"] <= 2020)].copy()
df["Year"] = df["Year"].astype(int)

MEDAL_COLS = {
    "Ouro": "Gold",
    "Prata": "Silver",
    "Bronze": "Bronze",
    "Todos": "Total_Medals",
}
MEDAL_LABELS = {
    "Gold": "Medalhas de Ouro",
    "Silver": "Medalhas de Prata",
    "Bronze": "Medalhas de Bronze",
    "Total_Medals": "Total de Medalhas",
}
COLORS = {"Gold": "#D4A017", "Silver": "#9AA3AD", "Bronze": "#B87333"}

app = Dash(__name__, title="Quadro de Medalhas Olímpicas")
server = app.server

anos = sorted(df["Year"].unique().tolist())
paises = sorted(df[["Country_Name", "Country_Display"]].drop_duplicates()["Country_Name"].dropna().unique().tolist())
pais_labels = dict(zip(df["Country_Name"], df["Country_Display"]))
ano_options = []
for ano in anos:
    linha = df[df["Year"] == ano]
    sede = linha["Host_Display"].iloc[0] if not linha.empty else "Sede não informada"
    cidade = linha["Host_city"].iloc[0] if not linha.empty else ""
    ano_options.append({"label": f"{ano} — {cidade}, {sede}", "value": int(ano)})

app.layout = html.Div(
    [
        html.Div(
            [
                html.P("VISUALIZAÇÃO DE DADOS • PYTHON / DASH / PLOTLY", className="eyebrow"),
                html.H1("Quadro de Medalhas Olímpicas"),
                html.P(
                    "Explore o desempenho dos países nos Jogos Olímpicos de Verão "
                    "entre 1992 e 2020."
                ),
            ],
            className="hero",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Tipo de medalha — filtro global"),
                        dcc.Dropdown(
                            id="filtro-medalha",
                            options=[
                                {"label": "Todas as medalhas", "value": "Todos"},
                                {"label": "Ouro", "value": "Ouro"},
                                {"label": "Prata", "value": "Prata"},
                                {"label": "Bronze", "value": "Bronze"},
                            ],
                            value="Todos",
                            clearable=False,
                        ),
                    ],
                    className="filter-card",
                ),
                html.Div(
                    [
                        html.Label("Ano olímpico (país-sede) — gráfico de barras"),
                        dcc.Dropdown(
                            id="filtro-ano",
                            options=ano_options,
                            value=2020 if 2020 in anos else anos[-1],
                            clearable=False,
                        ),
                    ],
                    className="filter-card",
                ),
            ],
            className="filters",
        ),
        html.Div(
            [
                html.Div([dcc.Graph(id="mapa-medalhas", config={"displayModeBar": True})], className="chart-card map-card"),
                html.Div(
                    [
                        html.Div([dcc.Graph(id="area-medalhas", config={"displayModeBar": True})], className="chart-card"),
                        html.Div([dcc.Graph(id="barras-medalhas", config={"displayModeBar": True})], className="chart-card"),
                    ],
                    className="two-columns",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2("Distribuição por país"),
                                html.P("Selecione um país para comparar Ouro, Prata e Bronze."),
                                dcc.Dropdown(
                                    id="filtro-pais",
                                    options=[{"label": pais_labels.get(p, p), "value": p} for p in paises],
                                    value="Brazil" if "Brazil" in paises else paises[0],
                                    clearable=False,
                                    searchable=True,
                                ),
                            ],
                            className="pie-controls",
                        ),
                        dcc.Graph(id="pizza-medalhas", config={"displayModeBar": True}),
                    ],
                    className="chart-card pie-card",
                ),
            ],
            className="charts",
        ),
        html.Footer(
            "Fonte: Country_Medals.csv • Período exibido: 1992–2020 • Dashboard acadêmico",
            className="footer",
        ),
    ],
    className="page",
)

def aplicar_estilo(fig, height=430):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=24, r=24, t=70, b=30),
        title=dict(x=0.03, xanchor="left", font=dict(size=18)),
        font=dict(family="Arial, sans-serif", color="#263445"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    return fig

@app.callback(
    Output("mapa-medalhas", "figure"),
    Output("area-medalhas", "figure"),
    Output("barras-medalhas", "figure"),
    Input("filtro-medalha", "value"),
    Input("filtro-ano", "value"),
)
def atualizar_graficos(tipo_medalha, ano_escolhido):
    coluna = MEDAL_COLS.get(tipo_medalha, "Total_Medals")
    rotulo = MEDAL_LABELS[coluna]

    # Mapa: agrega a medalha escolhida por país no período de 1992 a 2020.
    por_pais = df.groupby(["Country_Name", "Country_Display"], as_index=False)[coluna].sum()
    mapa = px.choropleth(
        por_pais,
        locations="Country_Name",
        locationmode="country names",
        color=coluna,
        hover_name="Country_Display",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={coluna: rotulo},
        title=f"{rotulo} por país (1992–2020)",
    )
    mapa.update_geos(showframe=False, showcoastlines=True, projection_type="natural earth")
    aplicar_estilo(mapa, 500)

    # Área empilhada: dez países com maior contagem da métrica selecionada.
    totais = df.groupby("Country_Name")[coluna].sum().nlargest(10).index.tolist()
    serie = df[df["Country_Name"].isin(totais)].groupby(
        ["Year", "Country_Name", "Country_Display"], as_index=False
    )[coluna].sum()
    area = px.area(
        serie,
        x="Year",
        y=coluna,
        color="Country_Display",
        labels={"Year": "Ano olímpico", coluna: rotulo, "Country_Display": "País"},
        title=f"Evolução das medalhas — Top 10 países ({tipo_medalha})",
    )
    aplicar_estilo(area, 430)

    area.update_layout(
    margin=dict(l=24, r=24, t=130, b=30),
    title=dict(
        x=0.03,
        y=0.99,
        xanchor="left",
        font=dict(size=18)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.88,
        xanchor="left",
        x=0
    )
    )

    # Barras: filtra diretamente o ano olímpico escolhido.
    dados_ano = df[df["Year"] == int(ano_escolhido)]
    barras_df = dados_ano.groupby(["Country_Name", "Country_Display"], as_index=False)[coluna].sum()
    barras_df = barras_df.nlargest(10, coluna).sort_values(coluna, ascending=True)
    sede_linha = dados_ano.iloc[0]
    titulo_ano = f"{int(ano_escolhido)} — {sede_linha['Host_city']}, {sede_linha['Host_Display']}"
    barras = px.bar(
        barras_df,
        x=coluna,
        y="Country_Display",
        orientation="h",
        labels={coluna: rotulo, "Country_Display": "País"},
        title=f"Top 10 países — {rotulo} • {titulo_ano}",
        color_discrete_sequence=["#D4A017" if tipo_medalha in ("Ouro", "Todos") else
                                 "#9AA3AD" if tipo_medalha == "Prata" else "#B87333"],
    )
    aplicar_estilo(barras, 430)
    barras.update_layout(yaxis=dict(title=""))

    return mapa, area, barras

@app.callback(
    Output("pizza-medalhas", "figure"),
    Input("filtro-pais", "value"),
)
def atualizar_pizza(pais):
    # O gráfico de pizza sempre compara as três categorias para o país escolhido.
    dados = df[df["Country_Name"] == pais][["Gold", "Silver", "Bronze"]].sum()
    pizza_df = pd.DataFrame({
        "Medalha": ["Ouro", "Prata", "Bronze"],
        "Quantidade": [int(dados["Gold"]), int(dados["Silver"]), int(dados["Bronze"])],
    })
    fig = px.pie(
        pizza_df,
        names="Medalha",
        values="Quantidade",
        hole=0.35,
        color="Medalha",
        color_discrete_map={"Ouro": COLORS["Gold"], "Prata": COLORS["Silver"], "Bronze": COLORS["Bronze"]},
        title=f"Medalhas de {pais_labels.get(pais, pais)} (1992–2020)",
    )
    fig.update_traces(textposition="inside", textinfo="label+value+percent")
    aplicar_estilo(fig, 430)
    return fig

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
