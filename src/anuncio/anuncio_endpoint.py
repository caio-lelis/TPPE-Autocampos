from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.moto.moto_schema import MotoRead
from src.anuncio.anuncio_schema import AnuncioCreate, AnuncioRead
from src.anuncio.anuncio_service import anuncio_service
from src.carro.carro_schema import CarroRead
from src.minio.minio_service import minio_service
from typing import List, Optional
from datetime import date

router = APIRouter(prefix="/anuncios", tags=["Anúncios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=AnuncioRead)
def create_anuncio_api(anuncio: AnuncioCreate, db: Session = Depends(get_db)):
    try:
        db_anuncio = anuncio_service.create_anuncio(db, anuncio)
    except ValueError as e: # Captura a exceção de validação do Pydantic/Service
        raise HTTPException(status_code=400, detail=str(e))
    if not db_anuncio:
        raise HTTPException(status_code=400, detail="Erro ao criar anúncio.")
    return db_anuncio

@router.get("/get", response_model=List[AnuncioRead])
def get_all_anuncios_api(db: Session = Depends(get_db)):
    return anuncio_service.get_all_anuncios(db)

@router.get("/get/{anuncio_id}", response_model=AnuncioRead)
def get_anuncio_by_id_api(anuncio_id: int, db: Session = Depends(get_db)):
    db_anuncio = anuncio_service.get_anuncio_by_id(db, anuncio_id)
    if not db_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    return db_anuncio

@router.put("/update/{anuncio_id}", response_model=AnuncioRead)
def update_anuncio_api(anuncio_id: int, anuncio: AnuncioCreate, db: Session = Depends(get_db)):
    try:
        db_anuncio = anuncio_service.update_anuncio(db, anuncio_id, anuncio)
    except ValueError as e: # Captura a exceção de validação do Pydantic/Service
        raise HTTPException(status_code=400, detail=str(e))
    if not db_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    return db_anuncio

@router.delete("/delete/{anuncio_id}", response_model=AnuncioRead)
def delete_anuncio_api(anuncio_id: int, db: Session = Depends(get_db)):
    # Busca o anúncio para obter as URLs das imagens
    db_anuncio = anuncio_service.get_anuncio_by_id(db, anuncio_id)
    if not db_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    
    # Remove as imagens do MinIO
    image_urls = [db_anuncio.imagem1_url, db_anuncio.imagem2_url, db_anuncio.imagem3_url]
    for url in image_urls:
        if url:
            minio_service.delete_image(url)
    
    # Remove o anúncio do banco
    deleted_anuncio = anuncio_service.delete_anuncio(db, anuncio_id)
    if not deleted_anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado.")
    
    return deleted_anuncio

@router.get("/carros-anunciados/marca/{marca}", response_model=List[CarroRead])
def get_carros_anunciados_por_marca(marca: str, db: Session = Depends(get_db)):
    carros = anuncio_service.get_carros_anunciados_por_marca(db, marca)
    if not carros:
        raise HTTPException(status_code=404, detail="Nenhum carro anunciado encontrado para esta marca.")
    return carros


@router.get("/motos-anunciadas/marca/{marca}", response_model=List[MotoRead])
def get_motos_anunciadas_por_marca(marca: str, db: Session = Depends(get_db)):
    motos = anuncio_service.get_motos_anunciadas_por_marca(db, marca)
    if not motos:
        raise HTTPException(status_code=404, detail="Nenhuma moto anunciada encontrada para esta marca.")
    return motos

@router.post("/create-with-images", response_model=AnuncioRead)
async def create_anuncio_with_images(
    funcionario_id: int = Form(...),
    carro_id: Optional[int] = Form(None),
    moto_id: Optional[int] = Form(None),
    data_publicacao: Optional[str] = Form(None),
    imagem1: Optional[UploadFile] = File(None),
    imagem2: Optional[UploadFile] = File(None),
    imagem3: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Cria um anúncio com upload de imagens para o MinIO.
    """
    image_urls = []  # Inicializa a lista no início
    
    try:
        # Validação básica
        if carro_id is not None and moto_id is not None:
            raise HTTPException(status_code=400, detail="Um anúncio não pode ter carro_id e moto_id preenchidos simultaneamente.")
        if carro_id is None and moto_id is None:
            raise HTTPException(status_code=400, detail="Um anúncio deve estar associado a um carro ou a uma moto.")

        # Processa as imagens
        images = [imagem1, imagem2, imagem3]
        
        for i, image in enumerate(images, 1):
            if image and image.filename:
                # Verifica se é uma imagem válida
                if not image.content_type.startswith('image/'):
                    raise HTTPException(status_code=400, detail=f"Arquivo {i} não é uma imagem válida.")
                
                # Lê os dados da imagem
                image_data = await image.read()
                
                # Faz upload para o MinIO
                image_url = minio_service.upload_image(
                    image_data=image_data,
                    content_type=image.content_type
                )
                
                if image_url:
                    image_urls.append(image_url)
                else:
                    raise HTTPException(status_code=500, detail=f"Erro ao fazer upload da imagem {i}.")
            else:
                image_urls.append(None)

        # Converte data_publicacao se fornecida
        parsed_date = None
        if data_publicacao:
            try:
                parsed_date = date.fromisoformat(data_publicacao)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

        # Cria o objeto AnuncioCreate
        anuncio_data = AnuncioCreate(
            funcionario_id=funcionario_id,
            carro_id=carro_id,
            moto_id=moto_id,
            data_publicacao=parsed_date or date.today(),
            imagem1_url=image_urls[0],
            imagem2_url=image_urls[1],
            imagem3_url=image_urls[2]
        )

        # Cria o anúncio
        db_anuncio = anuncio_service.create_anuncio(db, anuncio_data)
        
        if not db_anuncio:
            # Remove as imagens do MinIO se falhar
            for url in image_urls:
                if url:
                    minio_service.delete_image(url)
            raise HTTPException(status_code=400, detail="Erro ao criar anúncio.")
        
        return db_anuncio
        
    except HTTPException:
        # Re-raise HTTPException para manter o status code correto
        raise
    except ValueError as e:
        # Remove as imagens do MinIO se falhar
        for url in image_urls:
            if url:
                minio_service.delete_image(url)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Remove as imagens do MinIO se falhar
        for url in image_urls:
            if url:
                minio_service.delete_image(url)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.put("/update-with-images/{anuncio_id}", response_model=AnuncioRead)
async def update_anuncio_with_images(
    anuncio_id: int,
    funcionario_id: int = Form(...),
    carro_id: Optional[int] = Form(None),
    moto_id: Optional[int] = Form(None),
    data_publicacao: Optional[str] = Form(None),
    imagem1: Optional[UploadFile] = File(None),
    imagem2: Optional[UploadFile] = File(None),
    imagem3: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Atualiza um anúncio, incluindo upload de novas imagens.
    """
    try:
        # Busca o anúncio existente
        existing_anuncio = anuncio_service.get_anuncio_by_id(db, anuncio_id)
        if not existing_anuncio:
            raise HTTPException(status_code=404, detail="Anúncio não encontrado.")

        # Validação básica
        if carro_id is not None and moto_id is not None:
            raise HTTPException(status_code=400, detail="Um anúncio não pode ter carro_id e moto_id preenchidos simultaneamente.")
        if carro_id is None and moto_id is None:
            raise HTTPException(status_code=400, detail="Um anúncio deve estar associado a um carro ou a uma moto.")

        # Armazena URLs antigas para possível remoção
        old_image_urls = [
            existing_anuncio.imagem1_url,
            existing_anuncio.imagem2_url,
            existing_anuncio.imagem3_url
        ]

        # Processa as novas imagens
        image_urls = []
        images = [imagem1, imagem2, imagem3]
        
        for i, image in enumerate(images, 1):
            if image and image.filename:
                # Verifica se é uma imagem válida
                if not image.content_type.startswith('image/'):
                    raise HTTPException(status_code=400, detail=f"Arquivo {i} não é uma imagem válida.")
                
                # Lê os dados da imagem
                image_data = await image.read()
                
                # Faz upload para o MinIO
                image_url = minio_service.upload_image(
                    image_data=image_data,
                    content_type=image.content_type
                )
                
                if image_url:
                    image_urls.append(image_url)
                else:
                    raise HTTPException(status_code=500, detail=f"Erro ao fazer upload da imagem {i}.")
            else:
                # Mantém a imagem anterior se não houver nova
                image_urls.append(old_image_urls[i-1])

        # Converte data_publicacao se fornecida
        parsed_date = None
        if data_publicacao:
            try:
                parsed_date = date.fromisoformat(data_publicacao)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

        # Cria o objeto AnuncioCreate
        anuncio_data = AnuncioCreate(
            funcionario_id=funcionario_id,
            carro_id=carro_id,
            moto_id=moto_id,
            data_publicacao=parsed_date or existing_anuncio.data_publicacao,
            imagem1_url=image_urls[0],
            imagem2_url=image_urls[1],
            imagem3_url=image_urls[2]
        )

        # Atualiza o anúncio
        db_anuncio = anuncio_service.update_anuncio(db, anuncio_id, anuncio_data)
        
        if not db_anuncio:
            raise HTTPException(status_code=400, detail="Erro ao atualizar anúncio.")
        
        # Remove as imagens antigas se foram substituídas
        for i, old_url in enumerate(old_image_urls):
            if old_url and old_url != image_urls[i]:
                minio_service.delete_image(old_url)
        
        return db_anuncio
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/images/{image_name}")
def get_image(image_name: str):
    """
    Serve uma imagem do MinIO.
    """
    try:
        image_url = minio_service.get_image_url(image_name)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Imagem não encontrada: {str(e)}")
