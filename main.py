import os

from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker
from src.api import (concessionaria_endpoint, vendedor_endpoint,
                     comprador_endpoint, carro_endpoint ,
                     caminhao_endpoint , moto_endpoint)

app = FastAPI()

app.include_router(concessionaria_endpoint.router ,prefix="/api" ,  tags=["Concessionárias"])
app.include_router(vendedor_endpoint.router ,prefix="/api" ,  tags=["Vendedores"])
app.include_router(comprador_endpoint.router ,prefix="/api" ,  tags=["Compradores"])
app.include_router(carro_endpoint.router , prefix="/api", tags=["Carros"])
app.include_router(caminhao_endpoint.router , prefix="/api", tags=["Caminhões"])
app.include_router(moto_endpoint.router, prefix="/api" , tags=["Motos"])

@app.get("/")
async def root():
    return {"message": "Hello World Autocampos!"}


