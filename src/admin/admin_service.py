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

admin_service = AdminService()