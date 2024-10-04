import json
import jsonschema


# Abrir el archivo JSON y cargar el contenido
# with open('tweets_extraction.json', 'r') as archivo:
with open('reducido.json', 'r') as archivo:
    datos = json.load(archivo)

# Definir el esquema esperado
esquema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string"
      },
      "texto": {
        "type": "string"
      },
      "usuario": {
        "type": "string"
      },
      "hashtags": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "fecha": {
        "type": "string",
        "format": "date-time"
      },
      "retweets": {
        "type": "number"
      },
      "favoritos": {
        "type": "number"
      }
    },
    "required": [
      "id",
      "texto",
      "usuario",
      "hashtags",
      "fecha",
      "retweets",
      "favoritos"
    ]
  }
}


# Validar los datos contra el esquema
try:
    jsonschema.validate(instance=datos, schema=esquema)
    print("El JSON cumple con el esquema")
except jsonschema.exceptions.ValidationError as e:
    print(f"Error de validación: {e.message}")

# Imprimir el contenido para ver la estructura
for item in datos:
    for clave, valor in item.items():
        print(f"Clave: {clave}, Tipo de valor: {type(valor)}")
