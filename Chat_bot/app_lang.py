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

def chat_bot_gen(input_text):
    index = GPTSimpleVectorIndex.load_from_disk("index.json")
    response = index.query(input_text, response_mode="compact")
    return response.response

def chat_bot_client(input_text):
    index = GPTSimpleVectorIndex.load_from_disk("index_client.json")
    response = index.query(input_text, response_mode="compact")
    return response.response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    return '¡Hola! Bienvenido a Sol7. En que te puedo ayudar?.'

@app.route('/chat', methods=['POST'])
def chatbot_gen():
    try:
        question = request.args.get('question')
        if question:
            response = chat_bot_gen(question)

            # Create a response object with plain text content
            response_text = make_response(response)
            response_text.headers['Content-Type'] = 'text/plain'
            
            return response_text
        else:
            return "Lo siento, no he entendido la pregunta."
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/chat_client', methods=['POST'])
def chatbot_client():
    try:
        question = request.args.get('question')
        if question:
            response = chat_bot_client(question)

            # Create a response object with plain text content
            response_text = make_response(response)
            response_text.headers['Content-Type'] = 'text/plain'
            
            return response_text
        else:
            return "Lo siento, no he entendido la pregunta."
    except Exception as e:
        return f"Error: {str(e)}"    
    
if __name__ == '__main__':
    app.run(debug=True)

 