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
        Gera um gráfico combinado (barra + linha) com visual moderno:
        - Barras: Quantidade de carros vendidos
        - Linha: Valor das comissões (em escala separada)
        """
        try:
            # Configuração do estilo profissional
            plt.style.use('seaborn-v0_8-whitegrid')
            fig, ax1 = plt.subplots(figsize=(12, 6))
            
            # Paleta de cores moderna
            palette = {
                'carros': '#1f77b4',
                'comissoes': '#ff7f0e',
                'linha': '#d62728'
            }

            # --- Gráfico de Barras (Carros Vendidos) ---
            bars = ax1.bar(
                'Carros Vendidos', 
                dados["total_carros_vendidos"],
                color=palette['carros'],
                width=0.6,
                alpha=0.8,
                label=f'Carros: {dados["total_carros_vendidos"]}'
            )
            ax1.set_ylabel('Quantidade de Carros', color=palette['carros'])
            ax1.tick_params(axis='y', labelcolor=palette['carros'])
            
            # Adiciona valores nas barras
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(
                    f'{height}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color=palette['carros']
                )

            # --- Gráfico de Linha (Comissões) ---
            ax2 = ax1.twinx()
            line = ax2.plot(
                'Comissões', 
                dados["total_comissoes"],
                marker='o',
                markersize=10,
                linewidth=3,
                color=palette['linha'],
                alpha=0.8,
                label=f'Comissões: R$ {dados["total_comissoes"]:,.2f}'
            )
            ax2.set_ylabel('Valor (R$)', color=palette['linha'])
            ax2.tick_params(axis='y', labelcolor=palette['linha'])
            
            # --- Ajustes Visuais ---
            plt.title(
                'DESEMPENHO DE VENDAS\n',
                fontsize=14,
                pad=20,
                fontweight='bold'
            )
            
            # Unifica as legendas
            lines_labels = [ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels()]
            lines, labels = [sum(l, []) for l in zip(*lines_labels)]
            fig.legend(
                lines, labels,
                loc='upper center',
                bbox_to_anchor=(0.5, 0.95),
                ncol=2,
                frameon=True
            )

            # Grid e layout
            ax1.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()

            # --- Converter para Base64 ---
            buffer = io.BytesIO()
            plt.savefig(
                buffer, 
                format='png', 
                dpi=120, 
                bbox_inches='tight',
                facecolor='white'  # Fundo branco para sistemas modernos
            )
            plt.close(fig)
            buffer.seek(0)
            
            return base64.b64encode(buffer.read()).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico: {str(e)}")
            raise ValueError("Falha na geração da visualização")

funcionario_service = FuncionarioService()