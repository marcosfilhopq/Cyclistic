import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Carrega os dados processados
df_dia = pd.read_csv("resumo_dia_semana.csv")
df_mes = pd.read_csv("resumo_meses.csv")
df_bike = pd.read_csv("resumo_tipos_bike.csv")
df_estacoes = pd.read_csv("resumo_top_estacoes.csv")
df_kpis = pd.read_csv("resumo_kpis.csv")

# Mapeamento de cores oficiais
cor_membro = "#2563EB"  # Azul Royal
cor_casual = "#F97316"  # Laranja Vibrante

# Ordenação de dias
ordem_dias_nomes = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

# Prepara dados de dia da semana
df_dia_membro = df_dia[df_dia["member_casual"] == "member"].set_index("dia_nome").reindex(ordem_dias_nomes).reset_index()
df_dia_casual = df_dia[df_dia["member_casual"] == "casual"].set_index("dia_nome").reindex(ordem_dias_nomes).reset_index()

# Prepara dados mensais
nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
df_mes_membro = df_mes[df_mes["member_casual"] == "member"].sort_values("mes")
df_mes_casual = df_mes[df_mes["member_casual"] == "casual"].sort_values("mes")

# ==============================================================================
# Gráfico 1: Volume por Dia da Semana
# ==============================================================================
fig_dias = go.Figure()
fig_dias.add_trace(go.Bar(
    x=df_dia_membro["dia_nome"],
    y=df_dia_membro["total_corridas"],
    name="Membros",
    marker_color=cor_membro,
    hovertemplate="<b>Membros</b><br>Dia: %{x}<br>Corridas: %{y:,.0f}<extra></extra>"
))
fig_dias.add_trace(go.Bar(
    x=df_dia_casual["dia_nome"],
    y=df_dia_casual["total_corridas"],
    name="Casuais",
    marker_color=cor_casual,
    hovertemplate="<b>Casuais</b><br>Dia: %{x}<br>Corridas: %{y:,.0f}<extra></extra>"
))
fig_dias.update_layout(
    title="<b>Volume de Corridas por Dia da Semana</b>",
    barmode="group",
    template="plotly_white",
    height=380,
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ==============================================================================
# Gráfico 2: Duração Média por Dia da Semana
# ==============================================================================
fig_duracao = go.Figure()
fig_duracao.add_trace(go.Bar(
    x=df_dia_membro["dia_nome"],
    y=df_dia_membro["media_duracao_min"],
    name="Membros",
    marker_color=cor_membro,
    hovertemplate="<b>Membros</b><br>Dia: %{x}<br>Duração Média: %{y:.1f} min<extra></extra>"
))
fig_duracao.add_trace(go.Bar(
    x=df_dia_casual["dia_nome"],
    y=df_dia_casual["media_duracao_min"],
    name="Casuais",
    marker_color=cor_casual,
    hovertemplate="<b>Casuais</b><br>Dia: %{x}<br>Duração Média: %{y:.1f} min<extra></extra>"
))
fig_duracao.update_layout(
    title="<b>Duração Média por Dia (Minutos)</b>",
    barmode="group",
    template="plotly_white",
    height=380,
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ==============================================================================
# Gráfico 3: Sazonalidade Mensal
# ==============================================================================
fig_meses = go.Figure()
fig_meses.add_trace(go.Scatter(
    x=df_mes_membro["mes_nome"],
    y=df_mes_membro["total_corridas"],
    mode="lines+markers",
    name="Membros",
    line=dict(color=cor_membro, width=3),
    marker=dict(size=7),
    hovertemplate="<b>Membros</b><br>Mês: %{x}<br>Corridas: %{y:,.0f}<extra></extra>"
))
fig_meses.add_trace(go.Scatter(
    x=df_mes_casual["mes_nome"],
    y=df_mes_casual["total_corridas"],
    mode="lines+markers",
    name="Casuais",
    line=dict(color=cor_casual, width=3),
    marker=dict(size=7),
    hovertemplate="<b>Casuais</b><br>Mês: %{x}<br>Corridas: %{y:,.0f}<extra></extra>"
))
fig_meses.update_layout(
    title="<b>Sazonalidade Mensal (Evolução no Ano)</b>",
    template="plotly_white",
    height=380,
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ==============================================================================
# Gráfico 4: Tipos de Bicicleta
# ==============================================================================
df_bike_pivot = df_bike.pivot(index="rideable_type", columns="member_casual", values="total_corridas").fillna(0)
nome_bikes = {"classic_bike": "Bicicleta Clássica", "electric_bike": "Bicicleta Elétrica"}
df_bike_pivot.index = [nome_bikes.get(x, x) for x in df_bike_pivot.index]

fig_bike = go.Figure()
fig_bike.add_trace(go.Bar(
    y=df_bike_pivot.index,
    x=df_bike_pivot["member"],
    name="Membros",
    orientation="h",
    marker_color=cor_membro,
    hovertemplate="<b>Membros</b><br>Tipo: %{y}<br>Total: %{x:,.0f}<extra></extra>"
))
fig_bike.add_trace(go.Bar(
    y=df_bike_pivot.index,
    x=df_bike_pivot["casual"],
    name="Casuais",
    orientation="h",
    marker_color=cor_casual,
    hovertemplate="<b>Casuais</b><br>Tipo: %{y}<br>Total: %{x:,.0f}<extra></extra>"
))
fig_bike.update_layout(
    title="<b>Volume por Tipo de Bicicleta</b>",
    barmode="stack",
    template="plotly_white",
    height=380,
    margin=dict(l=120, r=20, t=50, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# ==============================================================================
# Gráfico 5: Top 10 Estações Casuais
# ==============================================================================
df_estacoes_ord = df_estacoes.sort_values("total_saidas", ascending=True)
fig_estacoes = go.Figure()
fig_estacoes.add_trace(go.Bar(
    y=df_estacoes_ord["start_station_name"],
    x=df_estacoes_ord["total_saidas"],
    orientation="h",
    marker_color=cor_casual,
    hovertemplate="<b>%{y}</b><br>Partidas de Casuais: %{x:,.0f}<extra></extra>"
))
fig_estacoes.update_layout(
    title="<b>Top 10 Estações de Início de Casuais</b>",
    template="plotly_white",
    height=380,
    margin=dict(l=190, r=20, t=50, b=40)
)

# ==============================================================================
# Gráfico 6: Mapa de Dispersão das Estações em Chicago
# ==============================================================================
fig_mapa = go.Figure()
fig_mapa.add_trace(go.Scattermap(
    lat=df_estacoes["lat"],
    lon=df_estacoes["lng"],
    mode="markers+text",
    marker=dict(
        size=df_estacoes["total_saidas"] / 1200 + 10,
        color=cor_casual,
        opacity=0.85
    ),
    text=df_estacoes["start_station_name"],
    textposition="top right",
    hovertemplate="<b>%{text}</b><br>Total Casuais: %{marker.size:,.0f}<extra></extra>"
))
fig_mapa.update_layout(
    title="<b>Mapa Geográfico: Hotspots de Casuais em Chicago</b>",
    map=dict(
        center=dict(lat=41.90, lon=-87.62),
        zoom=11,
        style="carto-positron"
    ),
    height=380,
    margin=dict(l=10, r=10, t=50, b=10)
)


# Renderiza os fragmentos HTML de cada gráfico
html_dias = fig_dias.to_html(full_html=False, include_plotlyjs="cdn")
html_duracao = fig_duracao.to_html(full_html=False, include_plotlyjs=False)
html_meses = fig_meses.to_html(full_html=False, include_plotlyjs=False)
html_bike = fig_bike.to_html(full_html=False, include_plotlyjs=False)
html_estacoes = fig_estacoes.to_html(full_html=False, include_plotlyjs=False)
html_mapa = fig_mapa.to_html(full_html=False, include_plotlyjs=False)

# Template completo HTML com Tailwind/CSS limpo integrado
dashboard_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyclistic Bike-Share | Dashboard Executivo</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #F8FAFC;
            color: #1E293B;
            padding: 24px;
        }}
        .header {{
            background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
            color: white;
            padding: 28px 32px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .header h1 {{ font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }}
        .header p {{ font-size: 14px; opacity: 0.9; margin-top: 4px; }}
        .badge {{
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
            backdrop-filter: blur(4px);
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: white;
            padding: 20px 24px;
            border-radius: 14px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.06);
        }}
        .kpi-label {{ font-size: 13px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-value {{ font-size: 28px; font-weight: 800; margin: 8px 0 4px; color: #0F172A; }}
        .kpi-sub {{ font-size: 12px; color: #64748B; }}
        .membro-cor {{ color: #2563EB; }}
        .casual-cor {{ color: #F97316; }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 24px;
        }}
        @media (max-width: 1024px) {{
            .charts-grid {{ grid-template-columns: 1fr; }}
        }}
        .chart-box {{
            background: white;
            border-radius: 14px;
            padding: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }}
        .insights-box {{
            background: white;
            border-radius: 14px;
            padding: 28px 32px;
            border-left: 6px solid #2563EB;
            border: 1px solid #E2E8F0;
            border-left-width: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            margin-bottom: 24px;
        }}
        .insights-box h2 {{ font-size: 20px; font-weight: 700; margin-bottom: 16px; color: #1E293B; }}
        .insights-list {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
        .insight-item {{
            background: #F8FAFC;
            padding: 16px;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        }}
        .insight-item strong {{ display: block; font-size: 15px; margin-bottom: 6px; color: #0F172A; }}
        .insight-item p {{ font-size: 13px; line-height: 1.5; color: #475569; }}
        .footer {{
            text-align: center;
            font-size: 13px;
            color: #94A3B8;
            padding: 16px 0;
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1>🚲 Cyclistic Bike-Share Analytics</h1>
            <p>Estudo de Caso Google Data Analytics | Análise Comparativa de Comportamento (5.95M Viagens Válidas)</p>
        </div>
        <div class="badge">
            Relatório Executivo Interativo
        </div>
    </div>

    <!-- KPIs -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Volume Total Analisado</div>
            <div class="kpi-value">5.951.769</div>
            <div class="kpi-sub">Viagens limpas e auditadas</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Membros Anuais</div>
            <div class="kpi-value membro-cor">3.870.739</div>
            <div class="kpi-sub"><b>65,0%</b> do volume total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Ciclistas Casuais</div>
            <div class="kpi-value casual-cor">2.081.030</div>
            <div class="kpi-sub"><b>35,0%</b> do volume total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Duração Média (Casual)</div>
            <div class="kpi-value casual-cor">18,4 min</div>
            <div class="kpi-sub">+50,7% mais tempo vs. membros</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Duração Média (Membro)</div>
            <div class="kpi-value membro-cor">12,2 min</div>
            <div class="kpi-sub">Padrão ágil de comutação diária</div>
        </div>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
        <div class="chart-box">
            {html_dias}
        </div>
        <div class="chart-box">
            {html_duracao}
        </div>
        <div class="chart-box">
            {html_meses}
        </div>
        <div class="chart-box">
            {html_bike}
        </div>
        <div class="chart-box">
            {html_estacoes}
        </div>
        <div class="chart-box">
            {html_mapa}
        </div>
    </div>

    <!-- Executive Insights -->
    <div class="insights-box">
        <h2>💡 Recomendações Estratégicas para Conversão de Casuais (Fase Act)</h2>
        <div class="insights-list">
            <div class="insight-item">
                <strong>1. Bônus de Boas-Vindas & Degustação</strong>
                <p>Oferecer os <b>3 primeiros meses com desconto agressivo</b> (taxa simbólica de entrada) ou permitir que o valor gasto em viagens casuais nos últimos 30 dias seja abatido como crédito na anuidade.</p>
            </div>
            <div class="insight-item">
                <strong>2. Plano Universitário / Desconto Estudantil</strong>
                <p>Criar a categoria <i>"Cyclistic Universitário"</i> com desconto especial para os milhares de estudantes em Chicago (DePaul, UIC, Loyola, UChicago), convertendo jovens ciclistas em membros fiéis.</p>
            </div>
            <div class="insight-item">
                <strong>3. Assinatura "Fim de Semana & Lazer"</strong>
                <p>Aproveitar o pico de sábado (438k) e domingo (334k) para oferecer um plano específico de lazer com opção de upgrade fácil para a assinatura anual completa.</p>
            </div>
            <div class="insight-item">
                <strong>4. Campanha de Verão Hiperfocada</strong>
                <p>Concentrar investimentos de mídia digital entre maio e agosto, quando o uso casual salta de 23k para 345k corridas/mês (quase 15x mais).</p>
            </div>
            <div class="insight-item">
                <strong>5. Ativação nos Hotspots da Orla</strong>
                <p>Instalar totens e notificações via aplicativo nas principais estações de saída casual (Navy Pier, Millennium Park, Lake Shore Dr) promovendo conversão imediata.</p>
            </div>
            <div class="insight-item">
                <strong>6. Calculadora de Economia no App</strong>
                <p>Como os casuais passam de 18 a 28 min pedalando, demonstrar no app o quanto eles economizam por minuto e corrida ao migrar para a anuidade.</p>
            </div>
            <div class="insight-item">
                <strong>7. Plano Anual Família & Grupos (Family Pass)</strong>
                <p>As estações #1 e #6 (Navy Pier e Shedd Aquarium) são grandes atrações de lazer familiar. Um plano anual com desbloqueio de 2 a 4 bikes com desconto familiar converte grupos que acham caro assinar 4 planos individuais.</p>
            </div>
        </div>
    </div>

    <div class="footer">
        Desenvolvido por Marcos Filho • Estudo de Caso Google Data Analytics • Base de dados pública Cyclistic / Divvy Trips
    </div>

</body>
</html>
"""

with open("dashboard_interativo.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print("[OK] Dashboard interativo gerado com sucesso em 'dashboard_interativo.html'!")
