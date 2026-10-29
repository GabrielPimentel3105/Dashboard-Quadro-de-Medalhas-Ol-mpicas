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
df["Country_Name"] = df["Country_Name"].replace(
    {"United States": "United States of America"}
)
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
paises = sorted(df["Country_Name"].dropna().unique().tolist())
ano_options = []
for ano in anos:
    linha = df[df["Year"] == ano]
    sede = linha["Host_country"].iloc[0] if not linha.empty else "Sede não informada"
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
                                    options=[{"label": p, "value": p} for p in paises],
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
    por_pais = df.groupby("Country_Name", as_index=False)[coluna].sum()
    mapa = px.choropleth(
        por_pais,
        locations="Country_Name",
        locationmode="country names",
        color=coluna,
        hover_name="Country_Name",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={coluna: rotulo},
        title=f"{rotulo} por país (1992–2020)",
    )
    mapa.update_geos(showframe=False, showcoastlines=True, projection_type="natural earth")
    aplicar_estilo(mapa, 500)

    # Área empilhada: dez países com maior contagem da métrica selecionada.
    totais = df.groupby("Country_Name")[coluna].sum().nlargest(10).index.tolist()
    serie = df[df["Country_Name"].isin(totais)].groupby(
        ["Year", "Country_Name"], as_index=False
    )[coluna].sum()
    area = px.area(
        serie,
        x="Year",
        y=coluna,
        color="Country_Name",
        labels={"Year": "Ano olímpico", coluna: rotulo, "Country_Name": "País"},
        title=f"Evolução das medalhas — Top 10 países ({tipo_medalha})",
    )
    aplicar_estilo(area, 430)

    # Barras: filtra diretamente o ano olímpico escolhido.
    dados_ano = df[df["Year"] == int(ano_escolhido)]
    barras_df = dados_ano.groupby("Country_Name", as_index=False)[coluna].sum()
    barras_df = barras_df.nlargest(10, coluna).sort_values(coluna, ascending=True)
    sede_linha = dados_ano.iloc[0]
    titulo_ano = f"{int(ano_escolhido)} — {sede_linha['Host_city']}, {sede_linha['Host_country']}"
    barras = px.bar(
        barras_df,
        x=coluna,
        y="Country_Name",
        orientation="h",
        labels={coluna: rotulo, "Country_Name": "País"},
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
        title=f"Medalhas de {pais} (1992–2020)",
    )
    fig.update_traces(textposition="inside", textinfo="label+value+percent")
    aplicar_estilo(fig, 430)
    return fig

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
