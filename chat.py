from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
load_dotenv()

openai_client = OpenAI()
# vector embeddings
embeddings_model = OpenAIEmbeddings(
    model = "text-embedding-3-small"
)


vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    embedding = embeddings_model,
    collection_name = "langchain_docs"
)

user_query = input("ask anything:")

#Relevant chuks from the vector db
search_result = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join(
    f"Page Content: {result.page_content}\n"
    f"Page Number: {result.metadata['page_label']}\n"
    f"File Location: {result.metadata['source']}"
    for result in search_result
)
SYSTEM_PROMPT = f"""
You are a helpful AI assistant for answeres user query based ib the available context
retrived from a PDF file along with page_contents and page number.

You should only ans the user based on the following context and navigate the user to 
open the right page number to know more.

Context:
{context}
"""

response = openai_client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]
)

print(f"{response.choices[0].message.content}")