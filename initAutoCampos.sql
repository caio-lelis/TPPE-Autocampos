/* Lógico_AutoCamposAtt: */

CREATE TABLE Concessionaria (
    nome VARCHAR,
    endereco VARCHAR,
    cnpj VARCHAR,
    telefone VARCHAR,
    id_concessionaria INTEGER PRIMARY KEY
);

CREATE TABLE Veiculo (
    id_veiculo INTEGER PRIMARY KEY,
    marca VARCHAR,
    modelo VARCHAR,
    cor VARCHAR,
    ano INTEGER,
    valor DOUBLE,
    tipo_combustivel VARCHAR,
    fk_Concessionaria_id_concessionaria INTEGER,
    fk_Comprador_fk_Pessoa_id INTEGER,
    fk_Vendedor_fk_Pessoa_id INTEGER
);

CREATE TABLE Carro (
    num_portas INTEGER,
    vidros_eletricos BOOLEAN,
    camera_re BOOLEAN,
    airbags BOOLEAN,
    fk_Veiculo_id_veiculo INTEGER PRIMARY KEY
);

CREATE TABLE Caminhao (
    carga DOUBLE,
    tamanho DOUBLE,
    tipo_carroceria VARCHAR,
    num_eixos INTEGER,
    fk_Veiculo_id_veiculo INTEGER PRIMARY KEY
);

CREATE TABLE Moto (
    cilindradas INTEGER,
    torque DOUBLE,
    peso DOUBLE,
    tipo_freio VARCHAR,
    fk_Veiculo_id_veiculo INTEGER PRIMARY KEY
);

CREATE TABLE Pessoa (
    id INTEGER PRIMARY KEY,
    nome VARCHAR,
    cpf VARCHAR,
    idade INTEGER
);

CREATE TABLE Vendedor (
    salario DOUBLE,
    especialidade VARCHAR,
    totalVendas DOUBLE,
    fk_Pessoa_id INTEGER PRIMARY KEY
);

CREATE TABLE Comprador (
    email VARCHAR,
    renda_mensal DOUBLE,
    profissao VARCHAR,
    saldo_compra DOUBLE,
    fk_Pessoa_id INTEGER PRIMARY KEY
);
 
ALTER TABLE Veiculo ADD CONSTRAINT FK_Veiculo_2
    FOREIGN KEY (fk_Concessionaria_id_concessionaria)
    REFERENCES Concessionaria (id_concessionaria)
    ON DELETE SET NULL;
 
ALTER TABLE Veiculo ADD CONSTRAINT FK_Veiculo_3
    FOREIGN KEY (fk_Comprador_fk_Pessoa_id)
    REFERENCES Comprador (fk_Pessoa_id)
    ON DELETE RESTRICT;
 
ALTER TABLE Veiculo ADD CONSTRAINT FK_Veiculo_4
    FOREIGN KEY (fk_Vendedor_fk_Pessoa_id)
    REFERENCES Vendedor (fk_Pessoa_id)
    ON DELETE CASCADE;
 
ALTER TABLE Carro ADD CONSTRAINT FK_Carro_2
    FOREIGN KEY (fk_Veiculo_id_veiculo)
    REFERENCES Veiculo (id_veiculo)
    ON DELETE CASCADE;
 
ALTER TABLE Caminhao ADD CONSTRAINT FK_Caminhao_2
    FOREIGN KEY (fk_Veiculo_id_veiculo)
    REFERENCES Veiculo (id_veiculo)
    ON DELETE CASCADE;
 
ALTER TABLE Moto ADD CONSTRAINT FK_Moto_2
    FOREIGN KEY (fk_Veiculo_id_veiculo)
    REFERENCES Veiculo (id_veiculo)
    ON DELETE CASCADE;
 
ALTER TABLE Vendedor ADD CONSTRAINT FK_Vendedor_2
    FOREIGN KEY (fk_Pessoa_id)
    REFERENCES Pessoa (id)
    ON DELETE CASCADE;
 
ALTER TABLE Comprador ADD CONSTRAINT FK_Comprador_2
    FOREIGN KEY (fk_Pessoa_id)
    REFERENCES Pessoa (id)
    ON DELETE CASCADE;