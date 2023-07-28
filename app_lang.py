from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from flask import Flask, request, jsonify

os.environ["OPENAI_API_KEY"] = "aaa"

# Cargar el modelo de lenguaje preentrenado en español
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=2000))
prompt_helper = PromptHelper(max_input_size=4096, num_output=2000, max_chunk_overlap=20, chunk_size_limit=600)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

# Crear la aplicación Flask
app = Flask(__name__)

directory_path = "Data\Data_bot"
documents = SimpleDirectoryReader(directory_path).load_data()
index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
index.save_to_disk('index.json')


def chat_bot(query):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    respuesta = index.query(query)
    return respuesta.respuesta


@app.route('/chat_bot', methods=['POST'])
def query_ai():
    data = request.get_json()
    query = data['query']
    respuesta = chat_bot(query)
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True)