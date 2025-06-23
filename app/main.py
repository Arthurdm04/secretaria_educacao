from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from app.api.endpoints import login, user, students, classes 

app = FastAPI(title="Sistema de Gerenciamento Escolar")

origins = [
    "http://127.0.0.1:8001",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, tags=["Login"], prefix="/login")
app.include_router(user.router, tags=["Users"], prefix="/users")
app.include_router(students.router, tags=["Students"], prefix="/students")
app.include_router(classes.router, tags=["Classes"], prefix="/classes")


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento Escolar!"}