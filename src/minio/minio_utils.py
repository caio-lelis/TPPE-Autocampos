"""
Módulo com funções para manipulação de arquivos (jsons) no MinIO.
"""

import os
from minio import Minio
from minio.error import S3Error

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio_admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio_admin123")
# Usa endpoint público se configurado, senão fallback para MINIO_ENDPOINT ou localhost
"""
# HOST para conexões internas do cliente MinIO (normalmente o serviço Docker ou localhost)
"""
MINIO_HOST = os.getenv("MINIO_ENDPOINT", "localhost:9000")

# Flag para usar HTTPS na conexão com o MinIO (cliente interno)
MINIO_USE_SSL = os.getenv("MINIO_USE_SSL", "false").lower() == "true"

BUCKET_NAME = "carros"
PATH_MINIO = ""
# PATH_FILE_PROCESS = "src/data/jsons"

def minio_client():
    """
    Configuração do cliente MinIO.
    """
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_USE_SSL,
    )
    return client


def listar_arquivos_minio(bucket_name, prefixo):
    """
    Lista os arquivos em um bucket do MinIO com um prefixo específico.
    """
    try:
        client = minio_client()
        objects = client.list_objects(bucket_name, prefix=prefixo, recursive=True)
        files = [obj.object_name for obj in objects]
        return files
    except S3Error as e:
        print(f"Ocorreu um erro ao acessar o bucket: {e}")
        return []


def verificar_conexao_minio():
    """
    Verifica a conexão com o MinIO tentando listar os buckets.
    """
    try:
        client = minio_client()
        buckets = client.list_buckets()
        return buckets
    except S3Error as e:
        print(f"Erro de conexão com o MinIO: {e}")
        return False


# def baixar_arquivos(bucket_name, arquivos, pasta_local):
#     """
#     Baixa arquivos de um bucket do MinIO para uma pasta local.
#     """
#     try:
#         if not os.path.exists(pasta_local):
#             os.makedirs(pasta_local)

#         client = minio_client()
#         for arquivo in arquivos:
#             caminho_local = os.path.join(pasta_local, os.path.basename(arquivo))
#             client.fget_object(bucket_name, arquivo, caminho_local)
#     except S3Error as e:
#         print(f"Erro ao baixar arquivos: {e}")


# def extrai_arquivos():
#     """ "
#     Essa função extrai os arquivos do Minio e salva em um diretório local
#     para que possam passar pela transformação.
#     """
#     baixar_arquivos(
#         BUCKET_NAME,
#         listar_arquivos_minio(BUCKET_NAME, PATH_MINIO),
#         PATH_FILE_PROCESS,
#     )
