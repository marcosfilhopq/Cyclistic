import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração global de estilo
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "figure.titlesize": 18,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# Paleta oficial e intuitiva:
# Membro = Azul (#1f77b4), Casual = Laranja (#ff7f0e)
cores = {"member": "#2563EB", "casual": "#F97316"}
rotulos_legenda = {"member": "Membros Anuais", "casual": "Ciclistas Casuais"}

# Carrega os dados processados
df_dia = pd.read_csv("resumo_dia_semana.csv")
df_mes = pd.read_csv("resumo_meses.csv")
df_bike = pd.read_csv("resumo_tipos_bike.csv")
df_estacoes = pd.read_csv("resumo_top_estacoes.csv")

# Cria figura com grid 2x2 + 1 painel horizontal inferior ou 2x2 completo
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Cyclistic Bike-Share: Comportamento de Uso (Membros vs. Casuais)", fontsize=18, fontweight="bold", y=0.98)

# -------------------------------------------------------------
# 1. Total de Corridas por Dia da Semana (Eixo [0, 0])
# -------------------------------------------------------------
ax1 = axes[0, 0]
ordem_dias = [1, 2, 3, 4, 5, 6, 7]
nomes_dias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
sns.barplot(
    data=df_dia,
    x="day_of_week",
    y="total_corridas",
    hue="member_casual",
    palette=cores,
    order=ordem_dias,
    ax=ax1
)
ax1.set_title("1. Volume de Corridas por Dia da Semana", fontweight="bold")
ax1.set_xlabel("Dia da Semana")
ax1.set_ylabel("Total de Corridas")
ax1.set_xticks(range(7))
ax1.set_xticklabels(nomes_dias)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1000):,}k"))
ax1.legend(title="Tipo de Usuário", labels=["Casual", "Membro"], loc="upper left")

# Anotação de insight
ax1.annotate("Pico dos Casuais\n(Fim de Semana)", xy=(6, 438505), xytext=(4.5, 520000),
             arrowprops=dict(facecolor="#F97316", shrink=0.08, width=1.5, headwidth=7),
             fontweight="bold", color="#C2410C", fontsize=9)

# -------------------------------------------------------------
# 2. Duração Média da Corrida (Minutos) por Dia (Eixo [0, 1])
# -------------------------------------------------------------
ax2 = axes[0, 1]
sns.barplot(
    data=df_dia,
    x="day_of_week",
    y="media_duracao_min",
    hue="member_casual",
    palette=cores,
    order=ordem_dias,
    ax=ax2
)
ax2.set_title("2. Duração Média da Corrida (em minutos)", fontweight="bold")
ax2.set_xlabel("Dia da Semana")
ax2.set_ylabel("Duração Média (minutos)")
ax2.set_xticks(range(7))
ax2.set_xticklabels(nomes_dias)
ax2.legend(title="Tipo de Usuário", labels=["Casual", "Membro"], loc="upper left")

# Linha média de referência
ax2.axhline(12.22, color="#2563EB", linestyle="--", alpha=0.7, label="Média Membros (~12 min)")
ax2.axhline(18.42, color="#F97316", linestyle="--", alpha=0.7, label="Média Casuais (~18 min)")

# -------------------------------------------------------------
# 3. Sazonalidade Mensal de Corridas (Eixo [1, 0])
# -------------------------------------------------------------
ax3 = axes[1, 0]
sns.lineplot(
    data=df_mes,
    x="mes",
    y="total_corridas",
    hue="member_casual",
    palette=cores,
    marker="o",
    linewidth=2.5,
    markersize=7,
    ax=ax3
)
ax3.set_title("3. Sazonalidade Mensal (Tendência ao Longo do Ano)", fontweight="bold")
ax3.set_xlabel("Mês")
ax3.set_ylabel("Total de Corridas")
nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels(nomes_meses)
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1000):,}k"))
ax3.legend(title="Tipo de Usuário", labels=["Casual", "Membro"], loc="upper left")

# Anotação de verão
ax3.axvspan(6, 8.5, color="orange", alpha=0.1, label="Alta Temporada (Verão)")

# -------------------------------------------------------------
# 4. Top 10 Estações mais Frequentes para Casuais (Eixo [1, 1])
# -------------------------------------------------------------
ax4 = axes[1, 1]
sns.barplot(
    data=df_estacoes.sort_values(by="total_saidas", ascending=True),
    x="total_saidas",
    y="start_station_name",
    color="#F97316",
    ax=ax4
)
ax4.set_title("4. Top 10 Estações com Mais Saídas de Casuais", fontweight="bold")
ax4.set_xlabel("Total de Saídas de Casuais")
ax4.set_ylabel("")
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1000):,}k"))

for p in ax4.patches:
    width = p.get_width()
    ax4.annotate(f"{int(width):,}".replace(",", "."),
                 (width, p.get_y() + p.get_height() / 2.),
                 xytext=(5, 0), textcoords="offset points",
                 ha="left", va="center", fontsize=9, color="#4B5563")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Salva imagem do dashboard para uso no GitHub e portfólio
plt.savefig("dashboard_cyclistic.png", dpi=300, bbox_inches="tight")
print("[OK] Gráfico executivo salvo com sucesso em 'dashboard_cyclistic.png'!")

# Exibe na tela se rodado com interface gráfica
try:
    plt.show()
except Exception:
    pass