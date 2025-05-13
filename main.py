from fastapi import FastAPI
from sqlalchemy import create_engine, text  # Adicione text aqui
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World Autocampos!"}

@app.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM usuarios"))

        # Usando .mappings() para converter automaticamente
        usuarios = [dict(row._mapping) for row in result]

        return {"usuarios": usuarios}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        db.close()
