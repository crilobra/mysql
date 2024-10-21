import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json


def convert_iso_to_mysql_format(iso_datetime):
    # Parsear la fecha del formato ISO 8601
    parsed_date = datetime.strptime(iso_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Formatear la fecha en el formato compatible con MySQL
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')




# Configurar la conexión
connection = mysql.connector.connect(
            host='localhost',
            port='33060',
            database='nao',
            user='root',
            password='secret',
            charset='utf8mb4'
            )
cursor = connection.cursor()

with open('crearTabla.sql', 'r') as sql_file:
    sql_script = sql_file.read()
sql_statements = sql_script.split(';')
# Ejecutar cada sentencia SQL
for statement in sql_statements:
    # Ignorar líneas vacías
    if statement.strip():
        cursor.execute(statement)
        print(f"Ejecutando: {statement.strip()}")
            
# Confirmar los cambios
connection.commit()

insert_query_tweet = '''
            INSERT INTO nao.tweet
            (id_tweet, texto, usuario, fecha, retweets, favoritos)
            VALUES (%s, %s, %s, %s, %s, %s);
            '''
insert_query_hash = '''
            INSERT INTO nao.hashtag
            ( hashtags, id_tweets)
            VALUES ( %s, %s);
            '''

with open('../tweets_extraction.json', 'r') as archivo:
    datos = json.load(archivo)

for record in datos:
    values = (
            record['id'],     
            record['texto'], 
            record['usuario'], 
            convert_iso_to_mysql_format(record['fecha']), 
            record['retweets'], 
            record['favoritos'],     
            )
    cursor.execute(insert_query_tweet, values)
    id_tweet = cursor.lastrowid
    if len(record['hashtags']):
        for hash in record['hashtags']:
            val = (
                hash,
                id_tweet,
            )
            cursor.execute(insert_query_hash, val)


connection.commit()