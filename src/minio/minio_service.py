from minio import Minio
from minio.error import S3Error
from typing import Optional
import io
import uuid
from datetime import datetime
import os

class MinioService:
    def __init__(self):
        # Detecta se está rodando em Docker ou localmente
        is_docker = os.getenv("DOCKER_ENV", "false").lower() == "true"
        
        if is_docker:
            # Dentro do Docker, usa nome do container
            endpoint = os.getenv("MINIO_ENDPOINT", "tppe-autocampos-minio-minio-1:9000")
        else:
            # Localmente, usa localhost
            endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
            
        self.client = Minio(
            endpoint=endpoint,
            access_key=os.getenv("MINIO_ACCESS_KEY", "minio_admin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minio_admin123"),
            secure=False  # Para desenvolvimento local
        )
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME", "autocampos-images")
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Garante que o bucket existe, criando se necessário."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' criado com sucesso.")
        except S3Error as e:
            print(f"Erro ao verificar/criar bucket: {e}")

    def upload_image(self, image_data: bytes, filename: str = None, content_type: str = "image/jpeg") -> Optional[str]:
        """
        Faz upload de uma imagem para o MinIO.
        
        Args:
            image_data: Dados da imagem em bytes
            filename: Nome do arquivo (opcional, será gerado automaticamente se não fornecido)
            content_type: Tipo MIME da imagem
            
        Returns:
            URL da imagem no MinIO ou None se falhar
        """
        try:
            # Gera um nome único para o arquivo se não fornecido
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                extension = self._get_extension_from_content_type(content_type)
                filename = f"anuncio_{timestamp}_{unique_id}.{extension}"
            
            # Faz o upload
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                data=io.BytesIO(image_data),
                length=len(image_data),
                content_type=content_type
            )
            
            # Retorna a URL da imagem
            return f"http://localhost:9000/{self.bucket_name}/{filename}"
            
        except S3Error as e:
            print(f"Erro ao fazer upload da imagem: {e}")
            return None

    def delete_image(self, image_url: str) -> bool:
        """
        Remove uma imagem do MinIO.
        
        Args:
            image_url: URL da imagem no MinIO
            
        Returns:
            True se removida com sucesso, False caso contrário
        """
        try:
            # Extrai o nome do objeto da URL
            object_name = image_url.split(f"/{self.bucket_name}/")[-1]
            
            self.client.remove_object(self.bucket_name, object_name)
            return True
            
        except S3Error as e:
            print(f"Erro ao remover imagem: {e}")
            return False

    def get_image_url(self, object_name: str) -> str:
        """
        Retorna a URL de uma imagem no MinIO.
        
        Args:
            object_name: Nome do objeto no bucket
            
        Returns:
            URL da imagem
        """
        return f"http://localhost:9000/{self.bucket_name}/{object_name}"

    def _get_extension_from_content_type(self, content_type: str) -> str:
        """Converte content-type para extensão de arquivo."""
        content_type_map = {
            "image/jpeg": "jpg",
            "image/jpg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
            "image/webp": "webp"
        }
        return content_type_map.get(content_type, "jpg")

# Instância singleton do serviço
minio_service = MinioService()
