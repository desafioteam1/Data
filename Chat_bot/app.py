import spacy
from flask import Flask, request
#python -m spacy download es_core_news_sm

app = Flask(__name__)

# Cargar el modelo de lenguaje preentrenado en español
nlp = spacy.load("es_core_news_sm")

# Definir las preguntas y respuestas predefinidas
intenciones_respuestas = {
    "presupuesto": "Para obtener un presupuesto personalizado, por favor visite nuestro sitio web o llámenos al número de contacto.",
    "contacto_comercial": "Puede comunicarse con nuestro equipo comercial al número de contacto o enviando un correo electrónico a comercial@empresa.com.",
    "otra_intencion": "Lo siento, no puedo responder a esa pregunta en este momento."
}

# Función para identificar la intención y obtener la respuesta adecuada
def obtener_respuesta(pregunta):
    # Procesar la pregunta con spaCy
    doc = nlp(pregunta)
    
    # Identificar la intención mediante una comparación de palabras clave
    if any(token.text.lower() in doc.text.lower() for token in doc):
        # Coincidencia de intención "presupuesto"
        return intenciones_respuestas["presupuesto"]
    elif any(token.text.lower() in doc.text.lower() for token in doc):
        # Coincidencia de intención "contacto_comercial"
        return intenciones_respuestas["contacto_comercial"]
    else:
        # Otra intención no reconocida
        return intenciones_respuestas["otra_intencion"]
    
@app.route('/', methods=['GET'])
def inicio():
    return '¡Hola! Bienvenido a Sol7. ¿En qué puedo ayudarte?'

# Ruta para recibir preguntas y devolver respuestas
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    question = request.form['question']

    if question.lower() == 'hola' or question.lower() == 'bienvenido':
        # Respuesta de bienvenida
        respuesta = 'Bienvenido a Sol7. ¿En qué puedo ayudarte?'
    else:
        # Obtener la respuesta del chatbot
        respuesta = obtener_respuesta(question)

    # Devolver la respuesta en formato JSON
    return respuesta

if __name__ == '__main__':
    app.run(debug=True)