# src/models/caminhao.py

from src.models.veiculo import Veiculo, TipoCombustivel

class Caminhao(Veiculo):
    """
    Classe que representa um caminhão, herdando da classe Veiculo.
    Adiciona atributos específicos como carga, tamanho, número de eixos e tipo de carroceria.
    """
    def __init__(
        self,
        id: int,
        marca: str,
        modelo: str,
        cor: str,
        ano: int,
        valor: float,
        combustivel: TipoCombustivel,
        carga: int,
        tamanho: float,
        numEixos: int,
        tipoCarroceria: str
    ):
        super().__init__(id, marca, modelo, cor, ano, valor, combustivel)
        self.carga = carga
        self.tamanho = tamanho
        self.numEixos = numEixos
        self.tipoCarroceria = tipoCarroceria

    def __str__(self) -> str:
        return (
            f"{super().__str__()}, Caminhão [Carga: {self.carga} kg, "
            f"Tamanho: {self.tamanho} m, Eixos: {self.numEixos}, "
            f"Carroceria: {self.tipoCarroceria}]"
        )

if __name__ == "__main__":
    meu_caminhao = Caminhao(
        id=1,
        marca="Mercedes-Benz",
        modelo="Actros",
        cor="Branco",
        ano=2022,
        valor=500000.00,
        combustivel=TipoCombustivel.DIESEL,
        carga=20000,
        tamanho=6.5,
        numEixos=3,
        tipoCarroceria="Baú"
    )
    
    print(meu_caminhao)