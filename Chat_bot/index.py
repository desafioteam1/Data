from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

os.chdir(os.path.dirname(__file__))
Api_key = os.environ.get("OPENAI_API_KEY")

def construct_index(directory_path, title):

    # set number of output tokens
    num_outputs = 2000
   
    # define prompt helper
    prompt_helper = PromptHelper(4096, 2000, 20, 600)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs, openai_api_key= Api_key))
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk(title)

    return index

index = construct_index("Data_bot", "index.json")
index = construct_index("Data_client", "index_client.json")