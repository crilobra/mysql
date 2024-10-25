import mysql.connector
from collections import Counter
import re
from textblob import TextBlob


def get_objectivity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity


connection = mysql.connector.connect(
            host='localhost',
            port='33060',
            database='nao',
            user='root',
            password='secret',
            charset='utf8mb4'
            )

cursor = connection.cursor()
cursor.execute("SELECT texto from nao.tweet")
all_words = []
for tabla in cursor:
    objectivity = get_objectivity(str(tabla))
    if objectivity > 0.9:
        print(f"Tweet: {str(tabla)}, Sentiment: {objectivity}")
        all_words.append(str(tabla))

# Calcular el sentimiento de cada texto
objetividad = [(
    text, TextBlob(text).sentiment.subjectivity) for text in all_words]

# Encontrar el texto con el sentimiento más intenso (mayor valor absoluto)
texto_mas_objetivo, intensidad_mas_alta = max(objetividad, key=lambda x: abs(x[1]))

# Mostrar el resultado
print(f"El objetividad más intenso es '{texto_mas_objetivo}' con una objetividad de {intensidad_mas_alta:.2f}")


connection.close()
