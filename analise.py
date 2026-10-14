import duckdb
import pandas as pd

con=duckdb.connect("cyclist.db") #con->conexao

# con.execute("""
#     CREATE OR REPLACE TABLE trips_combined AS
#     SELECT
#         ride_id,
#         rideable_type,
#         started_at,
#         ended_at,	
#         start_station_name,	
#         start_station_id,	
#         end_station_name,	
#         end_station_id,	
#         start_lat,	
#         start_lng,	
#         end_lat,
#         end_lng,	
#         member_casual
#         FROM read_csv_auto('trips/*.csv')
# """)

#Teste para ver se pegou
#fetchone() -> Busca a próxima linha do resultado da consulta SQL como uma tupla (ou retorna None se não houver mais linhas).
#[0] ->  Acessa o primeiro elemento dessa tupla (o valor da primeira coluna selecionada)
# total=con.execute("SELECT count(*) FROM trips_combined").fetchone()[0]
# print(f"{total:,}".replace(",", "."))

# Cria a tabela processada com limpeza de dados (Fase Processar do Google)
# - Remove viagens com duração negativa ou zero (erros de sistema)
# - Remove viagens menores que 60 segundos (desbloqueios falsos ou docks quebrados)
# - Remove viagens maiores que 24h (anomalias/esquecimentos)
# - Converte a duração para minutos decimais (ride_length_min) para facilitar gráficos e médias
con.execute(
    """
    CREATE OR REPLACE TABLE trips_processed AS
    SELECT
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        ended_at - started_at AS ride_length,
        date_part('epoch', ended_at - started_at) / 60.0 AS ride_length_min,
        dayofweek(started_at) + 1 AS day_of_week,
        CASE dayofweek(started_at)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda'
            WHEN 2 THEN 'Terça'
            WHEN 3 THEN 'Quarta'
            WHEN 4 THEN 'Quinta'
            WHEN 5 THEN 'Sexta'
            WHEN 6 THEN 'Sábado'
        END AS dia_nome,
        MONTH(started_at) AS mes,
        CASE MONTH(started_at)
            WHEN 1 THEN 'Jan' WHEN 2 THEN 'Fev' WHEN 3 THEN 'Mar' WHEN 4 THEN 'Abr'
            WHEN 5 THEN 'Mai' WHEN 6 THEN 'Jun' WHEN 7 THEN 'Jul' WHEN 8 THEN 'Ago'
            WHEN 9 THEN 'Set' WHEN 10 THEN 'Out' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dez'
        END AS mes_nome,
        start_station_name,
        start_station_id,
        end_station_name,
        end_station_id,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual
    FROM trips_combined
    WHERE ended_at > started_at
      AND date_part('epoch', ended_at - started_at) >= 60
      AND date_part('epoch', ended_at - started_at) <= 86400
    """
)

# 1. KPIs Gerais
df_kpis = con.execute(
    """
    SELECT 
        member_casual,
        COUNT(*) AS total_corridas,
        ROUND(AVG(ride_length_min), 2) AS media_duracao_min,
        ROUND(MEDIAN(ride_length_min), 2) AS mediana_duracao_min,
        ROUND(MAX(ride_length_min), 2) AS max_duracao_min
    FROM trips_processed
    GROUP BY member_casual
    """
).df()
print("\n=== KPIS GERAIS ===")
print(df_kpis)
df_kpis.to_csv("resumo_kpis.csv", index=False)

# 2. Corridas e Duração por Dia da Semana
df_pivot = con.execute(
    """
    SELECT 
        member_casual,
        day_of_week,
        dia_nome,
        COUNT(*) AS total_corridas,
        ROUND(AVG(ride_length_min), 2) AS media_duracao_min
    FROM trips_processed
    GROUP BY member_casual, day_of_week, dia_nome
    ORDER BY member_casual, day_of_week
    """
).df()
print("\n=== RESUMO POR DIA DA SEMANA ===")
print(df_pivot)
# Mantém o nome antigo para compatibilidade e salva também descritivo
df_pivot.to_csv("resumo_cyclistic.csv", index=False)
df_pivot.to_csv("resumo_dia_semana.csv", index=False)

# 3. Tipos de Bicicleta
df_pivot_2 = con.execute(
    """
    SELECT 
        member_casual,
        rideable_type,
        COUNT(*) AS total_corridas,
        ROUND(AVG(ride_length_min), 2) AS media_duracao_min
    FROM trips_processed
    GROUP BY member_casual, rideable_type
    ORDER BY member_casual, total_corridas DESC
    """
).df()
print("\n=== RESUMO POR TIPO DE BICICLETA ===")
print(df_pivot_2)
df_pivot_2.to_csv("resumo_tipos_bike.csv", index=False)

# 4. Sazonalidade Mensal
df_meses = con.execute(
    """
    SELECT
        member_casual,
        mes,
        mes_nome,
        COUNT(*) AS total_corridas,
        ROUND(AVG(ride_length_min), 2) AS media_duracao_min
    FROM trips_processed
    GROUP BY member_casual, mes, mes_nome
    ORDER BY member_casual, mes
    """
).df()
print("\n=== RESUMO MENSAL ===")
print(df_meses)
df_meses.to_csv("resumo_meses.csv", index=False)

# 5. Top 10 Estações mais populares entre usuários casuais
df_estacoes_casuais = con.execute(
    """
    SELECT 
        start_station_name,
        ROUND(AVG(start_lat), 4) AS lat,
        ROUND(AVG(start_lng), 4) AS lng,
        COUNT(*) AS total_saidas
    FROM trips_processed
    WHERE member_casual = 'casual' AND start_station_name IS NOT NULL
    GROUP BY start_station_name
    ORDER BY total_saidas DESC
    LIMIT 10
    """
).df()
print("\n=== TOP 10 ESTAÇÕES (CASUAIS) ===")
print(df_estacoes_casuais)
df_estacoes_casuais.to_csv("resumo_top_estacoes.csv", index=False)

print("\n[OK] Análises concluídas e arquivos CSV exportados com sucesso!")