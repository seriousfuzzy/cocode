# resume.py

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
import tempfile
import os

def process_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    pages = loader.load_and_split()
    
    for page in pages:
        page.metadata["source"] = file.name
    
    os.unlink(temp_file_path)
    return pages

def create_vector_store(documents):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    return Chroma.from_documents(texts, embeddings)
