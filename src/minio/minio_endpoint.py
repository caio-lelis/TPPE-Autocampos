"""
Endpoint para interação com o MinIO.
"""
from fastapi import APIRouter, HTTPException
from src.minio.minio_utils import listar_arquivos_minio, verificar_conexao_minio

router = APIRouter()


@router.get("/minio/status")
def get_minio_status():
    """
    Verifica e retorna o status da conexão com o MinIO.
    """
    if verificar_conexao_minio():
        return verificar_conexao_minio()
    else:
        raise HTTPException(status_code=500, detail={"status": "desconectado"})


@router.get("/minio/arquivos")
def listar_arquivos(bucket_name: str, prefixo: str):
    """
    Lista os arquivos em um bucket do MinIO com um prefixo específico.
    """
    try:
        arquivos = listar_arquivos_minio(bucket_name, prefixo)
        return {"arquivos": arquivos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
