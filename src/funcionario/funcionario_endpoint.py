from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.funcionario.funcionario_schema import FuncionarioCreate, FuncionarioRead
from src.funcionario.funcionario_service import funcionario_service
from typing import List
from datetime import date
from pydantic import BaseModel
from src.usuario.usuario_service import usuario_service
from src.funcionario.funcionario_model import Funcionario

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=FuncionarioRead)
def create_funcionario_api(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.create_funcionario(db, funcionario)
    if not db_funcionario:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário.")
    return db_funcionario

@router.get("/get", response_model=List[FuncionarioRead])
def get_all_funcionarios_api(db: Session = Depends(get_db)):
    return funcionario_service.get_all_funcionarios(db)

@router.get("/get/{funcionario_id}", response_model=FuncionarioRead)
def get_funcionario_by_id_api(funcionario_id: int, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.get_funcionario_by_id(db, funcionario_id)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return db_funcionario

@router.put("/update/{funcionario_id}", response_model=FuncionarioRead)
def update_funcionario_api(funcionario_id: int, funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = funcionario_service.update_funcionario(db, funcionario_id, funcionario)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return db_funcionario

@router.delete("/delete/{funcionario_id}", response_model=FuncionarioRead)
def delete_funcionario_api(funcionario_id: int, db: Session = Depends(get_db)):
    try:
        db_funcionario = funcionario_service.delete_funcionario(db, funcionario_id)
        if not db_funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
        return db_funcionario
    except Exception as e:
        # Captura erros de integridade referencial
        error_msg = str(e).lower()
        if "foreign key constraint" in error_msg or "violates foreign key constraint" in error_msg:
            raise HTTPException(
                status_code=409, 
                detail="Não é possível excluir o funcionário. Existem anúncios ou vendas associados a este funcionário."
            )
        elif "constraint" in error_msg:
            raise HTTPException(
                status_code=409,
                detail="Não é possível excluir o funcionário devido a restrições de integridade de dados."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/{funcionario_id}/dashboard")
def get_dashboard_funcionario(
    funcionario_id: int,
    db: Session = Depends(get_db),
):
    """
    Endpoint para obter dados de dashboard do funcionário:
    - Total de carros vendidos
    - Total de motos vendidas
    - Total de comissões
    - Valor total das vendas
    - Clientes ativos
    - Gráfico em base64
    """
    try:
        # Verificar se o funcionário existe
        funcionario = funcionario_service.get_funcionario_by_id(db, funcionario_id)
        if not funcionario:
            raise HTTPException(
                status_code=404,
                detail="Funcionário não encontrado."
            )

        # Obter dados consolidados
        dados = funcionario_service.get_dashboard_vendas(
            db, 
            funcionario_id=funcionario_id,
        )
        
        # Permitir dashboard mesmo sem vendas, mas com dados zerados
        if dados["total_veiculos_vendidos"] == 0:
            # Retornar dados zerados em vez de erro
            dados_zerados = {
                "total_carros_vendidos": 0,
                "total_motos_vendidas": 0,
                "total_veiculos_vendidos": 0,
                "total_comissoes": 0.0,
                "total_vendas": 0.0,
                "clientes_ativos": 0,
                "valor_carros": 0.0,
                "valor_motos": 0.0
            }
            return JSONResponse(content={
                "funcionario_id": funcionario_id,
                "metricas": dados_zerados,
                "grafico": None
            })

        # Gerar gráfico apenas se houver dados
        grafico_base64 = funcionario_service.gerar_grafico_vendas(dados)

        return JSONResponse(content={
            "funcionario_id": funcionario_id,
            "metricas": dados,
            "grafico": f"data:image/png;base64,{grafico_base64}"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar dashboard: {str(e)}"
        )

class FuncionarioLogin(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login_funcionario_api(login: FuncionarioLogin, db: Session = Depends(get_db)):
    # Autentica usuário
    usuario = usuario_service.authenticate_usuario(db, login.email, login.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")
    # Verifica se é funcionário
    funcionario = db.query(Funcionario).filter(Funcionario.usuario_id == usuario.id).first()
    if not funcionario:
        raise HTTPException(status_code=403, detail="Não autorizado como funcionário.")
    # Retorna dados do funcionário
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": "funcionario"
    }