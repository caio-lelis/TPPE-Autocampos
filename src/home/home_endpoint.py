"""
Endpoint para a página Home - Dashboard do funcionário logado
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.core.session import SessionLocal
from src.funcionario.funcionario_service import funcionario_service
from src.venda.venda_model import Venda
from src.cliente.cliente_model import Cliente
from sqlalchemy import func

router = APIRouter(prefix="/home", tags=["Home"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/funcionario/{funcionario_id}/metrics")
def get_funcionario_home_metrics(
    funcionario_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obter métricas do funcionário para a página Home:
    - Total de vendas realizadas
    - Total em vendas (valor)
    - Comissão recebida
    - Clientes ativos
    """
    try:
        # Verificar se o funcionário existe
        funcionario = funcionario_service.get_funcionario_by_id(db, funcionario_id)
        if not funcionario:
            raise HTTPException(
                status_code=404,
                detail="Funcionário não encontrado."
            )

        # Buscar dados de vendas
        vendas_data = db.query(
            func.count(Venda.id).label("total_vendas"),
            func.sum(Venda.valor_final).label("valor_total"),
            func.sum(Venda.comissao_venda).label("comissao_total"),
            func.count(func.distinct(Venda.cliente_id)).label("clientes_ativos")
        ).filter(
            Venda.funcionario_id == funcionario_id
        ).first()

        # Processar os dados
        total_vendas = vendas_data.total_vendas if vendas_data else 0
        valor_total = float(vendas_data.valor_total) if vendas_data and vendas_data.valor_total else 0.0
        comissao_total = float(vendas_data.comissao_total) if vendas_data and vendas_data.comissao_total else 0.0
        clientes_ativos = vendas_data.clientes_ativos if vendas_data else 0

        # Calcular progresso da meta (considerando meta de 15 vendas)
        meta_vendas = 15
        progresso_meta = (total_vendas / meta_vendas) * 100 if meta_vendas > 0 else 0

        return JSONResponse(content={
            "funcionario_id": funcionario_id,
            "total_vendas": total_vendas,
            "valor_total": valor_total,
            "comissao_total": comissao_total,
            "clientes_ativos": clientes_ativos,
            "meta_vendas": meta_vendas,
            "progresso_meta": round(progresso_meta, 1)
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar métricas: {str(e)}"
        )
