from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from src.venda.venda_model import Venda
from src.funcionario.funcionario_schema import FuncionarioCreate
from src.funcionario.funcionario_model import Funcionario as FuncionarioModel
from typing import List , Dict , Optional
import matplotlib.pyplot as plt
import io
import base64

class FuncionarioService:
    def create_funcionario(self, db: Session, funcionario: FuncionarioCreate) -> FuncionarioModel:
        db_funcionario = FuncionarioModel(
            usuario_id=funcionario.usuario_id,
            rendimento_mensal=funcionario.rendimento_mensal
        )
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario

    def get_all_funcionarios(self, db: Session) -> List[FuncionarioModel]:
        funcionarios = db.query(FuncionarioModel).all()
        for funcionario in funcionarios:
            if funcionario.usuario:
                funcionario.usuario.nome = funcionario.usuario.nome
                funcionario.usuario.email = funcionario.usuario.email
        return funcionarios

    def get_funcionario_by_id(self, db: Session, funcionario_id: int) -> FuncionarioModel:
        funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id).first()
        if funcionario and funcionario.usuario:
            funcionario.usuario.nome = funcionario.usuario.nome
            funcionario.usuario.email = funcionario.usuario.email
        return funcionario

    def get_funcionario_by_usuario_id(self, db: Session, usuario_id: int) -> FuncionarioModel:
        return db.query(FuncionarioModel).filter(FuncionarioModel.usuario_id == usuario_id).first()

    def update_funcionario(self, db: Session, funcionario_id: int, funcionario: FuncionarioCreate) -> FuncionarioModel:
        db_funcionario = self.get_funcionario_by_id(db, funcionario_id)
        if not db_funcionario:
            return None
        db_funcionario.usuario_id = funcionario.usuario_id
        db_funcionario.rendimento_mensal = funcionario.rendimento_mensal
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario

    def delete_funcionario(self, db: Session, funcionario_id: int):
        db_funcionario = self.get_funcionario_by_id(db, funcionario_id)
        if not db_funcionario:
            return None
        db.delete(db_funcionario)
        db.commit()
        return db_funcionario
    
    def get_dashboard_vendas(self, db: Session, funcionario_id: int) -> Dict[str, Optional[float]]:
        """
        Retorna dados consolidados para o dashboard de vendas do funcionário:
        - Total de carros vendidos
        - Soma das comissões
        """
        dados = db.query(
            func.count(Venda.carro_id).label("total_carros_vendidos"),
            func.sum(Venda.comissao_venda).label("total_comissoes")
        ).filter(
            Venda.funcionario_id == funcionario_id,
            Venda.carro_id.isnot(None)  # Filtra apenas vendas de carros
        ).first()

        return {
            "total_carros_vendidos": dados.total_carros_vendidos if dados else 0,
            "total_comissoes": float(dados.total_comissoes) if dados and dados.total_comissoes else 0.0
        }

    def gerar_grafico_vendas(self, dados: Dict) -> str:
        """
        Gera um gráfico de barras com valores normalizados (0–100%).
        Permite comparar comissões e carros vendidos proporcionalmente.
        """
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax = plt.subplots(figsize=(8, 5))

            # Dados originais
            valores_originais = {
                "Carros Vendidos": dados["total_carros_vendidos"],
                "Comissões (R$)": dados["total_comissoes"]
            }

            # Normaliza os dados (0 a 100%)
            valor_max = max(valores_originais.values()) or 1  # evita divisão por zero
            valores_normalizados = {
                k: (v / valor_max) * 100 for k, v in valores_originais.items()
            }

            # Cores
            cores = ['#1f77b4', '#ff7f0e']

            # Gráfico
            ax.bar(
                list(valores_normalizados.keys()),
                list(valores_normalizados.values()),
                color=cores,
                width=0.5,
                alpha=0.9
            )

            # Adiciona rótulos com os valores originais
            for i, (label, val) in enumerate(valores_originais.items()):
                ax.text(
                    i, valores_normalizados[label] + 2,
                    f'{val if isinstance(val, int) else f"R$ {val:,.2f}"}',
                    ha='center', fontsize=11, fontweight='bold'
                )

            ax.set_title('Comparativo Normalizado de Desempenho', fontsize=14, fontweight='bold')
            ax.set_ylabel('Percentual relativo (%)')
            ax.set_ylim(0, 110)

            plt.tight_layout()

            # Exporta como imagem base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            buffer.seek(0)

            return base64.b64encode(buffer.read()).decode('utf-8')

        except Exception as e:
            logger.error(f"Erro ao gerar gráfico normalizado: {str(e)}")
            raise ValueError("Falha na geração do gráfico")




funcionario_service = FuncionarioService()