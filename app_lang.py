from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
import sys
import os
import gradio as gr
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response

load_dotenv()

os.chdir(os.path.dirname(__file__))
Api_key = os.environ.get("OPENAI_API_KEY")

def construct_index(directory_path):

    
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600 

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs, openai_api_key= Api_key))
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index


def chat_bot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

app = Flask(__name__)
index = construct_index("Data_bot")

@app.route('/', methods=['GET'])
def welcome():
    return '¡Hola! Bienvenido a Sol7. En que te puedo ayudar?.'

@app.route('/chat', methods=['POST'])
def chatbot_api():
    try:
        question = request.args.get('question')
        if question:
            response = chat_bot(question)

            # Create a response object with plain text content
            response_text = make_response(response)
            response_text.headers['Content-Type'] = 'text/plain'
            
            return response_text
        else:
            return "Lo siento, la pregunta debe ser proporcionada en el formulario."
    except Exception as e:
        return f"Error: {str(e)}"
    
    
if __name__ == '__main__':
    app.run(debug=True)

 