import mysql.connector
import pandas as pd
from textblob import TextBlob
from prophet import Prophet


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
# Recuperar datos desde la tabla 'comentarios'
query = "SELECT fecha, texto FROM nao.tweet"
data = pd.read_sql(query, connection)

# Cerrar la conexión a la base de datos
connection.close()

# Calcular el sentimiento de cada comentario usando TextBlob
data['sentimiento'] = data['texto'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Prepara los datos para Prophet: debe tener las columnas 'ds' (fecha) y 'y' (sentimiento)
data_prophet = data[['fecha', 'sentimiento']].rename(columns={'fecha': 'ds', 'sentimiento': 'y'})

# Crear y entrenar el modelo Prophet
model = Prophet()
model.fit(data_prophet)

# Crear el DataFrame para predecir el sentimiento del día de mañana
future = model.make_future_dataframe(periods=1)  # Predicción de un día hacia el futuro

# Realizar la predicción
forecast = model.predict(future)

# Obtener el valor de sentimiento predicho para el día de mañana
prediccion_manana = forecast[['ds', 'yhat']].tail(1)
sentimiento_predicho = prediccion_manana['yhat'].values[0]

# Imprimir el sentimiento esperado
print(f"El sentimiento esperado para el día de mañana es {'positivo' if sentimiento_predicho > 0 else 'negativo' if sentimiento_predicho < 0 else 'neutral'} con un valor de {sentimiento_predicho:.2f}")