import mysql.connector
from collections import Counter
import re
from textblob import TextBlob


def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


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
count = 0
all_words = []
for tabla in cursor:
    count = count + 1
    sentiment_score = get_sentiment(str(tabla))
    if sentiment_score > 0.9:
        # print(f"Tweet: {str(tabla)}, Sentiment: {sentiment_score}")
        all_words.append(str(tabla))


# Calcular el sentimiento de cada texto
sentimientos = [(
    text, TextBlob(text).sentiment.polarity) for text in all_words]

# Encontrar el texto con el sentimiento más intenso (mayor valor absoluto)
texto_mas_intenso, intensidad_mas_alta = max(sentimientos, key=lambda x: abs(x[1]))

# Mostrar el resultado
print(f"El sentimiento más intenso es '{texto_mas_intenso}' con una intensidad de {intensidad_mas_alta:.2f}")

connection.close()
