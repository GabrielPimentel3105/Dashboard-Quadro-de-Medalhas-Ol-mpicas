https://dashboard-quadro-de-medalhas-ol-mpicas.onrender.com/

GIT - https://github.com/GabrielPimentel3105/Dashboard-Quadro-de-Medalhas-Ol-mpicas

DASHBOARD INTERATIVO — QUADRO DE MEDALHAS OLÍMPICAS

Arquivos:
- app.py: aplicação Dash, callbacks e gráficos Plotly Express.
- Country_Medals.csv: base de dados separada por ponto e vírgula.
- requirements.txt: dependências para instalação local e deploy.
- assets/style.css: estilo responsivo.

REQUISITOS IMPLEMENTADOS
1. Mapa coroplético por país.
2. Gráfico de áreas empilhadas para o Top 10 de países.
3. Gráfico de barras com Top 10 do ano olímpico selecionado (inclui país/cidade-sede).
4. Gráfico de pizza com Ouro, Prata e Bronze para o país escolhido.
5. Filtro global de tipo de medalha (Ouro, Prata, Bronze ou Todos) aplicado ao mapa, áreas e barras.
6. Filtro de ano olímpico aplicado diretamente ao gráfico de barras.
7. Período de análise: 1992–2020, seguindo o tutorial da disciplina.

EXECUTAR LOCALMENTE (Windows PowerShell)
1. Abra o terminal dentro da pasta do projeto.
2. Crie um ambiente virtual:
   python -m venv .venv
3. Ative o ambiente:
   .venv\Scripts\Activate.ps1
4. Instale as dependências:
   python -m pip install -r requirements.txt
5. Inicie o dashboard:
   python app.py
6. Abra no navegador:
   http://127.0.0.1:8050

PUBLICAR NO RENDER
1. Envie o conteúdo desta pasta para um repositório GitHub.
2. No Render, crie um novo Web Service conectado ao repositório.
3. Configure:
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:server
4. Selecione uma versão de Python compatível com as dependências.
5. Aguarde o deploy e teste o endereço público gerado pelo Render.
6. Cole o link público final no campo de entrega do SIGAA.

ATENÇÃO
O link público do Render só existe depois que você criar e publicar o serviço na sua conta.
Não invente nem entregue um link antes de o deploy terminar.
