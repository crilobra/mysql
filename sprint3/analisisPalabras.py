import mysql.connector
from collections import Counter
import re
from textblob import TextBlob


def get_objectivity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity


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
all_words = []
for tabla in cursor:
    words = re.findall(r'\b\w+\b', str(tabla))
    # filtrado de palabras comunes como la, el,uy,del
    words = [word for word in words if len(word) > 5]
    all_words.extend(words)


# Contar las palabras más comunes
word_counts = Counter(all_words)
print(word_counts.most_common(10))


connection.close()
