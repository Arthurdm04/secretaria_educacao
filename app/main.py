from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from dotenv import load_dotenv
from uuid import uuid4
import os
import getpass

# Langchain imports
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from pdfminer.high_level import extract_text

# Routers da aplicação escolar
from app.api.endpoints import login, user, students, classes

load_dotenv()

# Criação da aplicação
app = FastAPI(
    title="Sistema de Gerenciamento Escolar + API BNCC",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
origins = ["http://127.0.0.1:8001", "http://localhost:8001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas escolares
app.include_router(login.router, tags=["Login"], prefix="/login")
app.include_router(user.router, tags=["Users"], prefix="/users")
app.include_router(students.router, tags=["Students"], prefix="/students")
app.include_router(classes.router, tags=["Classes"], prefix="/classes")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API unificada de Gerenciamento Escolar e BNCC!"}

# -------------------------- RAG CONFIG --------------------------

class QueryRequest(BaseModel):
    ask: str
    top_k: int = 5
    temperature: float = 0.5

# API KEY fallback (evita crash local)
if not os.environ.get("AZURE_OPENAI_API_KEY"):
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure: ")

# LLM e embeddings
llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION_EMBEDDINGS"],
)

# Vector Store
vector_store = Chroma(
    collection_name="bncc_em",
    embedding_function=embeddings,
    persist_directory="./chroma_db_nv"
)

# Upload de documento e indexação
def add_doc(File: str, vector_store):
    max_file_size = 10 * 1024 * 1024
    if os.path.getsize(File) > max_file_size:
        raise ValueError("Arquivo muito grande!")

    filename = os.path.basename(File)
    all_docs = vector_store._collection.get(include=["metadatas"])
    doc_names = [metadata.get("filename", "Documento sem nome") for metadata in all_docs["metadatas"]]

    if filename in doc_names:
        raise ValueError("Esse arquivo já foi enviado!")

    try:
        extracted_text = extract_text(File)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        chunks = text_splitter.split_text(extracted_text)

        docs = [
            Document(page_content=chunk, metadata={"filename": filename}, id=str(len(doc_names) + i + 1))
            for i, chunk in enumerate(chunks)
        ]

        uuids = [str(uuid4()) for _ in docs]
        vector_store.add_documents(documents=docs, ids=uuids)
    except Exception as e:
        raise e

#add_doc("./bncc_ensino_medio.pdf", vector_store) -> primeira vez, precisa ser descomentada para indexar o documento

# Endpoint de Query
@app.post("/query/", tags=["BNCC"])
def query(request: QueryRequest):
    try:
        results = vector_store.similarity_search(request.ask, k=request.top_k)
        context = "\n".join([doc.page_content for doc in results])
        template = """Utilize o contexto abaixo para responder a pergunta ao final. Se você não souber a resposta, diga que não sabe e não tente inventar uma resposta.
        Contexto: {context}
        Pergunta: {question}
        Resposta:"""
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )
        response = llm.invoke(prompt.invoke({"context": context, "question": request.ask}))
        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
