from numpy._core import arrayprint
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

#Comando para criar a tabela
con.execute(
    """
    CREATE OR REPLACE TABLE trips_processed AS
    SELECT
        *, -- pegas as colnas originais
        ended_at - started_at AS ride_length,
        dayofweek(started_at) + 1 AS day_of_week
    FROM trips_combined
    """
)

#dataframe em si
df_processada=con.execute("SELECT * FROM trips_processed LIMIT 10").df()
print(df_processada)

df_resumo=con.execute(
    """
    SELECT 
        AVG(ride_length) AS media_duracao,
        MAX(ride_length) AS maxima_duracao,
        MODE(day_of_week) AS dia_mais_frequente
    FROM trips_processed
    """
).df()
#print(df_resumo)

#TABELAS DINAMICAS -> uso do GROUP BY
df_pivot=con.execute(
    """
    SELECT 
        member_casual,
        day_of_week,
        COUNT(*) AS total_corridas,
        AVG(ride_length) AS media_duracao
    FROM trips_processed
    GROUP BY member_casual, day_of_week
    ORDER BY member_casual, day_of_week  --Organiza de 1 para 7
    """
).df()
print(df_pivot)

# Adicione a linha abaixo DENTRO do arquivo analise.py
df_pivot.to_csv("resumo_cyclistic.csv", index=False)

#Aumento(ou perda) de uso de bicleltas eletricas - grafico de serie
df_pivot_2=con.execute(
    """
    SELECT 
        member_casual,
        rideable_type,
        MONTH(started_at) AS mes,
        COUNT(*) AS total_corridas
    FROM trips_processed
    GROUP BY member_casual, rideable_type, MONTH(started_at)
    ORDER BY mes ASC, member_casual, rideable_type
    """
).df()
print(df_pivot_2)

#Estacoes que os usarios mais pegam - com latitude e longitude
df_estacoes_casuais = con.execute(
    """
    SELECT 
        start_station_name,
        AVG(start_lat) AS lat,	--Como erra por alguns metros, pegar a media pegar o valor 'central'
        AVG(start_lng) AS lng,		
        COUNT(*) AS total_saidas
    FROM trips_processed
    WHERE member_casual = 'casual' AND start_station_name IS NOT NULL
    GROUP BY start_station_name
    ORDER BY total_saidas DESC
    LIMIT 10
    """
).df()
print(df_estacoes_casuais)

#Quais meses eles usam mais 
df_meses=con.execute(
    """
    SELECT
        member_casual,
        MONTH(started_at) AS mes,
        COUNT(*) AS total_corridas
    FROM trips_processed
    GROUP BY member_casual, MONTH(started_at)
    ORDER BY member_casual, mes
    """
).df()
print(df_meses)