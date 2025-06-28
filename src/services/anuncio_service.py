from sqlalchemy.orm import Session
from src.schemas.anuncio_schema import AnuncioCreate
from src.models.anuncio import Anuncio as AnuncioModel
from typing import List
from src.models.moto import Moto
from src.models.carro import Carro
from src.models.anuncio import Anuncio
class AnuncioService:
    def create_anuncio(self, db: Session, anuncio: AnuncioCreate) -> AnuncioModel:
        db_anuncio = AnuncioModel(
            funcionario_id=anuncio.funcionario_id,
            carro_id=anuncio.carro_id,
            moto_id=anuncio.moto_id,
            data_publicacao=anuncio.data_publicacao,
            imagem1_url=str(anuncio.imagem1_url) if anuncio.imagem1_url else None,
            imagem2_url=str(anuncio.imagem2_url) if anuncio.imagem2_url else None,
            imagem3_url=str(anuncio.imagem3_url) if anuncio.imagem3_url else None,
        )
        db.add(db_anuncio)
        db.commit()
        db.refresh(db_anuncio)
        return db_anuncio

    def get_all_anuncios(self, db: Session) -> List[AnuncioModel]:
        return db.query(AnuncioModel).all()

    def get_anuncio_by_id(self, db: Session, anuncio_id: int) -> AnuncioModel:
        return db.query(AnuncioModel).filter(AnuncioModel.id == anuncio_id).first()

    def update_anuncio(self, db: Session, anuncio_id: int, anuncio: AnuncioCreate) -> AnuncioModel:
        db_anuncio = self.get_anuncio_by_id(db, anuncio_id)
        if not db_anuncio:
            return None
        
        # Validação da exclusividade também no update
        if anuncio.carro_id is not None and anuncio.moto_id is not None:
            raise ValueError("Um anúncio não pode ter carro_id e moto_id preenchidos simultaneamente.")
        if anuncio.carro_id is None and anuncio.moto_id is None:
            raise ValueError("Um anúncio deve estar associado a um carro ou a uma moto.")

        db_anuncio.funcionario_id = anuncio.funcionario_id
        db_anuncio.carro_id = anuncio.carro_id
        db_anuncio.moto_id = anuncio.moto_id
        db_anuncio.data_publicacao = anuncio.data_publicacao
        db_anuncio.imagem1_url = str(anuncio.imagem1_url) if anuncio.imagem1_url else None
        db_anuncio.imagem2_url = str(anuncio.imagem2_url) if anuncio.imagem2_url else None
        db_anuncio.imagem3_url = str(anuncio.imagem3_url) if anuncio.imagem3_url else None
        db.commit()
        db.refresh(db_anuncio)
        return db_anuncio

    def delete_anuncio(self, db: Session, anuncio_id: int):
        db_anuncio = self.get_anuncio_by_id(db, anuncio_id)
        if not db_anuncio:
            return None
        db.delete(db_anuncio)
        db.commit()
        return db_anuncio


    def get_carros_anunciados_por_marca(self, db: Session, marca: str) -> List[Carro]:
        # Fazer join Anuncio -> Carro via carro_id, filtrar marca, garantir carro_id não nulo
        query = (
            db.query(Carro)
            .join(Anuncio, Carro.id == Anuncio.carro_id)
            .filter(Carro.marca.ilike(f"%{marca}%"))
            .filter(Anuncio.carro_id != None)  # só anúncios com carro
            .all()
        )
        return query

    def get_motos_anunciadas_por_marca(self, db: Session, marca: str) -> List[Moto]:
        return (
            db.query(Moto)
            .join(Anuncio, Moto.id == Anuncio.moto_id)
            .filter(Moto.marca.ilike(f"%{marca}%"))
            .filter(Anuncio.moto_id != None)
            .all()
        )
anuncio_service = AnuncioService()