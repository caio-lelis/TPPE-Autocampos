from sqlalchemy.orm import Session
from src.admin.admin_schema import AdminCreate
from src.admin.admin_model import Admin as AdminModel
from typing import List

class AdminService:
    def create_admin(self, db: Session, admin: AdminCreate) -> AdminModel:
        db_admin = AdminModel(
            usuario_id=admin.usuario_id,
            is_admin=admin.is_admin
        )
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        return db_admin

    def get_all_admins(self, db: Session) -> List[AdminModel]:
        admins = db.query(AdminModel).all()
        # Preenche info do usuário para cada admin
        for admin in admins:
            if admin.usuario:
                admin.usuario.nome = admin.usuario.nome
                admin.usuario.email = admin.usuario.email
        return admins

    def get_admin_by_id(self, db: Session, admin_id: int) -> AdminModel:
        admin = db.query(AdminModel).filter(AdminModel.id == admin_id).first()
        if admin and admin.usuario:
            admin.usuario.nome = admin.usuario.nome
            admin.usuario.email = admin.usuario.email
        return admin

    def get_admin_by_usuario_id(self, db: Session, usuario_id: int) -> AdminModel:
        return db.query(AdminModel).filter(AdminModel.usuario_id == usuario_id).first()

    def update_admin(self, db: Session, admin_id: int, admin: AdminCreate) -> AdminModel:
        db_admin = self.get_admin_by_id(db, admin_id)
        if not db_admin:
            return None
        db_admin.usuario_id = admin.usuario_id
        db_admin.is_admin = admin.is_admin
        db.commit()
        db.refresh(db_admin)
        return db_admin

    def delete_admin(self, db: Session, admin_id: int):
        db_admin = self.get_admin_by_id(db, admin_id)
        if not db_admin:
            return None
        db.delete(db_admin)
        db.commit()
        return db_admin

    def get_dashboard_stats(self, db: Session) -> (dict, str):
        """
        Retorna métricas de vendas e funções dos funcionários, e gráfico em base64
        """
        from src.venda.venda_model import Venda
        from src.funcionario.funcionario_model import Funcionario as FuncModel
        from src.usuario.usuario_model import Usuario as UserModel
        from sqlalchemy import func
        import matplotlib.pyplot as plt
        import io, base64

        # Vendas de carros
        total_carros_vendidos = db.query(func.count(Venda.id)).filter(Venda.carro_id != None).scalar() or 0
        valor_carros = float(db.query(func.coalesce(func.sum(Venda.valor_final), 0)).filter(Venda.carro_id != None).scalar())
        # Vendas de motos
        total_motos_vendidas = db.query(func.count(Venda.id)).filter(Venda.moto_id != None).scalar() or 0
        valor_motos = float(db.query(func.coalesce(func.sum(Venda.valor_final), 0)).filter(Venda.moto_id != None).scalar())

        # Funcionários: salário e comissões
        funcionarios = []
        func_objs = db.query(FuncModel).all()
        for f in func_objs:
            # soma comissões deste funcionário
            comissao_total = float(db.query(func.coalesce(func.sum(Venda.comissao_venda), 0)).filter(Venda.funcionario_id == f.id).scalar())
            # obtém nome do usuário associado
            user = db.query(UserModel).filter(UserModel.id == f.usuario_id).first()
            nome = user.nome if user else None
            funcionarios.append({
                "funcionario_id": f.id,
                "nome": nome,
                "salario": float(f.rendimento_mensal),
                "comissao_total": comissao_total
            })

        # Gera gráfico comparativo de valores de vendas com estilo aprimorado
        import matplotlib.pyplot as plt
        # Usa estilo embutido para evitar dependência externa
        plt.style.use('ggplot')
        labels = ['Carros', 'Motos']
        values = [valor_carros, valor_motos]
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
        bars = ax.bar(labels, values, color=['#FFD600', '#FFC107'], edgecolor='#333', linewidth=1.2)
        # Adiciona valores acima de cada barra
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + (max(values) * 0.02),
                    f"R$ {height:,.2f}", ha='center', va='bottom', fontsize=10, color='#111')
        # Configurações de títulos e rótulos
        ax.set_title('Valor de Vendas: Carros vs Motos', fontsize=14, fontweight='bold', color='#111')
        ax.set_ylabel('Valor Total (R$)', fontsize=12, color='#111')
        ax.set_xlabel('Categoria', fontsize=12, color='#111')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        # Layout e conversão para base64
        buf = io.BytesIO()
        fig.tight_layout(pad=2)
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

        stats = {
            "total_carros_vendidos": total_carros_vendidos,
            "valor_carros": valor_carros,
            "total_motos_vendidas": total_motos_vendidas,
            "valor_motos": valor_motos,
            "funcionarios": funcionarios
        }
        return stats, img_b64

    def get_admin_home_metrics(self, db: Session) -> dict:
        """
        Retorna métricas específicas para o painel home do administrador
        """
        from src.venda.venda_model import Venda
        from src.funcionario.funcionario_model import Funcionario as FuncModel
        from src.cliente.cliente_model import Cliente
        from src.carro.carro_model import Carro
        from src.moto.moto_model import Moto
        from src.anuncio.anuncio_model import Anuncio
        from sqlalchemy import func

        # Vendas totais
        total_vendas = db.query(func.count(Venda.id)).scalar() or 0
        valor_total_vendas = float(db.query(func.coalesce(func.sum(Venda.valor_final), 0)).scalar())
        
        # Vendas por tipo
        vendas_carros = db.query(func.count(Venda.id)).filter(Venda.carro_id != None).scalar() or 0
        vendas_motos = db.query(func.count(Venda.id)).filter(Venda.moto_id != None).scalar() or 0
        
        # Comissão total paga
        comissao_total = float(db.query(func.coalesce(func.sum(Venda.comissao_venda), 0)).scalar())
        
        # Contadores gerais
        total_funcionarios = db.query(func.count(FuncModel.id)).scalar() or 0
        total_clientes = db.query(func.count(Cliente.id)).scalar() or 0
        total_carros = db.query(func.count(Carro.id)).scalar() or 0
        total_motos = db.query(func.count(Moto.id)).scalar() or 0
        total_anuncios = db.query(func.count(Anuncio.id)).scalar() or 0
        
        # Anúncios ativos (considerando anúncios publicados nos últimos 30 dias como ativos)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        anuncios_ativos = db.query(func.count(Anuncio.id)).filter(
            Anuncio.data_publicacao >= thirty_days_ago
        ).scalar() or 0
        
        # Cálculo de progresso de vendas (meta fictícia de 100 vendas)
        meta_vendas = 100
        progresso_vendas = (total_vendas / meta_vendas) * 100 if meta_vendas > 0 else 0
        
        return {
            "total_vendas": total_vendas,
            "valor_total_vendas": valor_total_vendas,
            "vendas_carros": vendas_carros,
            "vendas_motos": vendas_motos,
            "comissao_total": comissao_total,
            "total_funcionarios": total_funcionarios,
            "total_clientes": total_clientes,
            "total_carros": total_carros,
            "total_motos": total_motos,
            "total_anuncios": total_anuncios,
            "anuncios_ativos": anuncios_ativos,
            "progresso_vendas": min(progresso_vendas, 100),
            "meta_vendas": meta_vendas
        }

    def get_business_overview(self, db: Session) -> dict:
        """
        Retorna uma visão geral do negócio para o administrador
        """
        from src.venda.venda_model import Venda
        from src.funcionario.funcionario_model import Funcionario as FuncModel
        from src.usuario.usuario_model import Usuario as UserModel
        from sqlalchemy import func, desc
        from datetime import datetime, timedelta

        # Top 3 funcionários por vendas
        top_funcionarios = db.query(
            FuncModel.id,
            UserModel.nome,
            func.count(Venda.id).label('total_vendas'),
            func.coalesce(func.sum(Venda.valor_final), 0).label('valor_total')
        ).join(
            UserModel, FuncModel.usuario_id == UserModel.id
        ).outerjoin(
            Venda, FuncModel.id == Venda.funcionario_id
        ).group_by(
            FuncModel.id, UserModel.nome
        ).order_by(
            desc('total_vendas')
        ).limit(3).all()

        # Vendas dos últimos 30 dias
        thirty_days_ago = datetime.now() - timedelta(days=30)
        vendas_recentes = db.query(func.count(Venda.id)).filter(
            Venda.data_venda >= thirty_days_ago
        ).scalar() or 0

        # Receita dos últimos 30 dias
        receita_recente = float(db.query(func.coalesce(func.sum(Venda.valor_final), 0)).filter(
            Venda.data_venda >= thirty_days_ago
        ).scalar())

        return {
            "top_funcionarios": [
                {
                    "id": f.id,
                    "nome": f.nome,
                    "total_vendas": f.total_vendas,
                    "valor_total": float(f.valor_total)
                }
                for f in top_funcionarios
            ],
            "vendas_ultimos_30_dias": vendas_recentes,
            "receita_ultimos_30_dias": receita_recente
        }

admin_service = AdminService()