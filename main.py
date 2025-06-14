import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker
from src.api import (usuario_endpoint , admin_endpoint, cliente_endpoint,
                     funcionario_endpoint,moto_endpoint, anuncio_endpoint
                      , carro_endpoint,interesse_endpoint , venda_endpoint )
app = FastAPI()


app.include_router(usuario_endpoint.router , prefix="/api/v1" , tags=["Usuários"])
app.include_router(admin_endpoint.router , prefix="/api/v1" , tags=["Administradores"])
app.include_router(cliente_endpoint.router , prefix="/api/v1" , tags=["Clientes"])
app.include_router(funcionario_endpoint.router , prefix="/api/v1" , tags=["Funcionários"])
app.include_router(moto_endpoint.router , prefix="/api/v1" , tags=["Motos"])
app.include_router(anuncio_endpoint.router , prefix="/api/v1" , tags=["Anúncios"])
app.include_router(carro_endpoint.router , prefix="/api/v1" , tags=["Carros"])
app.include_router(venda_endpoint.router , prefix="/api/v1" , tags=["Vendas"])
app.include_router(interesse_endpoint.router , prefix="/api/v1" , tags=["Interesses"])

@app.get("/")
async def root():
    return {"message": "Hello World Autocampos!"}


