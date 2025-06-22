from fastapi import FastAPI
from app.api.endpoints import login, user, students, classes

app = FastAPI(title="Sistema de Gerenciamento Escolar")

# Inclui os roteadores na aplicação principal com prefixos
app.include_router(login.router, tags=["Login"], prefix="/login")
app.include_router(user.router, tags=["Users"], prefix="/users")
app.include_router(students.router, tags=["Students"], prefix="/students")
app.include_router(classes.router, tags=["Classes"], prefix="/classes")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento Escolar!"}