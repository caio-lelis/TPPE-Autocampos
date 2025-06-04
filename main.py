from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from src.api import concessionaria_endpoint
import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World Autocampos!"}

app.include_router(
    concessionaria_endpoint.router, prefix="/api/v1", tags=["Concessionárias"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)