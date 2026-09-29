import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#1 Ler o arquivo
df_resumo=pd.read_csv('resumo_cyclistic.csv')

# 2. Configurando o estilo do gráfico (para ficar bonito)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# 3. Criando o Gráfico de Barras
# x = eixo horizontal, y = eixo vertical, hue = dividir por cor
sns.barplot(
    data=df_resumo, 
    x="day_of_week", 
    y="total_corridas", 
    hue="member_casual"
)

#4 Titulos
plt.title("Total de Corridas por Dia da Semana (Membros vs. Casuais)")
plt.xlabel("Dia da Semana (1=Domingo, 7=Sábado)")
plt.ylabel("Total de Corridas")

#5 Grafico
plt.show()