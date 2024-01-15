from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, PromptHelper, StorageContext, load_index_from_storage
from langchain.chat_models import ChatOpenAI
import sys
import os
from IPython.display import Markdown, display
import pandas as pd

def construct_index(directory_path):
    print("Constructing index...")  # Debugging print statement
    max_input_size = 4096
    num_outputs = 256
    max_chunk_overlap = 0.2

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106", max_tokens=num_outputs))
    print("LLM Predictor set with gpt-3.5-turbo")  # Debugging print statement

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap)
    print("Prompt helper initialized")  # Debugging print statement

    documents = SimpleDirectoryReader(directory_path).load_data()
    print(f"Loaded {len(documents)} documents")  # Debugging print statement

    index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    print("Index constructed from documents")  # Debugging print statement

    index.storage_context.persist(persist_dir="C:\\Users\\deezn\\Desktop\\py\\CHATBOTS\\WinnieBot")
    print("Index saved to disk")  # Debugging print statement

    return index

def ask():
    index = load_index_from_storage(StorageContext.from_defaults(persist_dir="C:\\Users\\deezn\\Desktop\\py\\CHATBOTS\\WinnieBot"))

    while True: 
        user_input = input("What do you want to ask Winnie? ")
        query = Winnie + """
        I am a member of the New Zealand public. """ + user_input

        query_engine = index.as_query_engine()
        response = query_engine.query(query)

        print(f"Winnie P.: {response.response}")


Winnie = "You will respond as Winston Peters, the current Acting Prime Minister of New Zealand (usually Deputy). You should not break character for any reason."
os.environ["OPENAI_API_KEY"] = "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"

construct_index('C:\\Users\\deezn\\Desktop\\py\\CHATBOTS\\WinnieBot\\WinnieScripts')

ask()
