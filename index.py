from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "PRD Full Stack Training.pdf"

loader = PyPDFLoader(file_path = pdf_path)
docs =loader.load()
print(docs[2])

# split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = text_splitter.split_documents(documents= docs)

# vector embeddings

embeddings_model = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)

vector_store = QdrantVectorStore.from_documents(
    documents= chunks,
    embedding = embeddings_model,
    url = "http://localhost:6333",
    collection_name = "langchain_docs"
)

print("indexing of documents is done....")