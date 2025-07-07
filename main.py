import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

from src.admin import admin_endpoint
from src.anuncio import anuncio_endpoint
from src.venda import venda_endpoint 
from src.carro import carro_endpoint
from src.cliente import cliente_endpoint
from src.funcionario import funcionario_endpoint
from src.interesse import interesse_endpoint
from src.moto import moto_endpoint
from src.usuario import usuario_endpoint
from src.minio import minio_endpoint

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_endpoint.router , prefix="/api/v1" , tags=["Usuários"])
app.include_router(admin_endpoint.router , prefix="/api/v1" , tags=["Administradores"])
app.include_router(cliente_endpoint.router , prefix="/api/v1" , tags=["Clientes"])
app.include_router(funcionario_endpoint.router , prefix="/api/v1" , tags=["Funcionários"])
app.include_router(moto_endpoint.router , prefix="/api/v1" , tags=["Motos"])
app.include_router(anuncio_endpoint.router , prefix="/api/v1" , tags=["Anúncios"])
app.include_router(carro_endpoint.router , prefix="/api/v1" , tags=["Carros"])
app.include_router(venda_endpoint.router , prefix="/api/v1" , tags=["Vendas"])
app.include_router(interesse_endpoint.router , prefix="/api/v1" , tags=["Interesses"])
app.include_router(minio_endpoint.router, prefix="/api/v1", tags=["MinIO"])

@app.get("/")
async def root():
    return {"message": "Hello World Autocampos!"}
