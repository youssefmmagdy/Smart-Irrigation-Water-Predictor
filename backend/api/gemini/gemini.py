import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.llms.google_genai import GoogleGenAI

from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

documents = SimpleDirectoryReader('./data').load_data()
model = GoogleGenAI(model='gemini-2.5-flash-preview-05-20', api_key=google_api_key)
model_embedding = GoogleGenAIEmbedding(model_name='text-embedding-004')

Settings.llm = model
Settings.embed_model = model_embedding
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900


index = VectorStoreIndex.from_documents(
        documents, 
        embed_model=model_embedding,
        transformations=[Settings.node_parser]
)

query_engine = index.as_query_engine()

def ask_gemini(input_query):
    response = query_engine.query(input_query)
    return response.response

