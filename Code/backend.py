import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

# PDF Loader 
from langchain_community.document_loaders import PyPDFLoader 
loader = PyPDFLoader('economics_research_reference.pdf')
pages = loader.load() 

# Split Data 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
spliter = RecursiveCharacterTextSplitter(chunk_size=1800 , chunk_overlap=160)

split_data = spliter.split_documents(pages)

chunks = [i.page_content for i in split_data]
metadata = [i.metadata for i in split_data]

import hashlib 
ids = [hashlib.md5(chunk.encode('utf-8')).hexdigest() for chunk in chunks]

# Vector DB create 
import chromadb 
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction 
embedding_function  = DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path="./VectorDB")

collection = client.get_or_create_collection(name="Self_RAG",embedding_function=embedding_function)

if collection.count()!=len(chunks):
    collection.add(ids=ids , documents=chunks,metadatas=metadata)
