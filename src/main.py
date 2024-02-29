from fastapi import FastAPI
from routers import answer
from configs import get_session_with_headers
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchText
from qdrant_client.http.models import Distance, VectorParams
from utils.utils import extract_text_from_pdf
from langchain_openai import OpenAIEmbeddings
import getpass
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

load_dotenv()
os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
COLLECTION_NAME = 'test_collection'
VUE_PERFORMANCE_PDF_PATH = 'src/mock_data/vue-performance.txt'
QDRANT_HOST = "http://localhost:6333"

app = FastAPI()
app.include_router(answer.router)

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
client = QdrantClient("localhost", port=6333)
# extracted_text = extract_text_from_pdf(VUE_PERFORMANCE_PDF_PATH)

loader = TextLoader(VUE_PERFORMANCE_PDF_PATH)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=5)

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    url=QDRANT_HOST,
    prefer_grpc=True,
    collection_name=COLLECTION_NAME,
    force_recreate=True,
)

retriever = qdrant.as_retriever()

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "how can reduce loading speed?"})
print(response["answer"])
