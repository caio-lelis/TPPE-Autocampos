-- Remove tabelas existentes para evitar conflitos ao executar o script novamente.
-- A opção CASCADE remove automaticamente objetos dependentes (como views ou chaves estrangeiras).
DROP TABLE IF EXISTS interesses, vendas, anuncios, carros, motos, admins, funcionarios, usuarios, clientes CASCADE;

-- Tabela Central de Usuários do Sistema
-- Armazena dados de login e informações básicas para todos os usuários internos.
CREATE TABLE usuarios (
    id            SERIAL PRIMARY KEY,
    nome          TEXT NOT NULL,
    cpf           VARCHAR(11) NOT NULL UNIQUE,
    email         TEXT NOT NULL UNIQUE,
    senha         TEXT NOT NULL -- Em um ambiente real, a senha deve ser armazenada como um hash.
);

-- Tabela de Funcionários
-- Contém informações específicas de funcionários. Um funcionário é um tipo de usuário.
CREATE TABLE funcionarios (
    id                    SERIAL PRIMARY KEY,
    usuario_id            INTEGER NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    rendimento_mensal     NUMERIC(10, 2) NOT NULL
);

-- Tabela de Administradores
-- Designa quais usuários possuem privilégios de administrador. Um admin também é um tipo de usuário.
CREATE TABLE admins (
    id            SERIAL PRIMARY KEY,
    usuario_id    INTEGER NOT NULL UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    is_admin      BOOLEAN DEFAULT FALSE
);

-- Tabela de Clientes
-- Armazena informações de contato de clientes interessados ou que realizaram compras.
CREATE TABLE clientes (
    id            SERIAL PRIMARY KEY,
    nome          TEXT NOT NULL,
    cpf           VARCHAR(11) NOT NULL UNIQUE,
    email         TEXT UNIQUE,
    telefone      VARCHAR(20),
    endereco      TEXT
);

-- Tabela para Carros (agora inclui atributos de 'veiculos')
CREATE TABLE carros (
    id                    SERIAL PRIMARY KEY,
    modelo                TEXT NOT NULL,
    marca                 TEXT NOT NULL,
    ano                   INTEGER NOT NULL,
    cor                   TEXT,
    tipo_combustivel      VARCHAR(50),
    preco                 NUMERIC(10, 2) NOT NULL,
    revisado              BOOLEAN DEFAULT FALSE,
    disponivel            BOOLEAN DEFAULT TRUE,
    tipo_direcao          VARCHAR(50),
    tracao                VARCHAR(10),
    consumo_cidade        NUMERIC(4, 2),
    airbag                BOOLEAN DEFAULT FALSE,
    ar_condicionado       BOOLEAN DEFAULT FALSE
);

-- Tabela para Motos (agora inclui atributos de 'veiculos')
CREATE TABLE motos (
    id                    SERIAL PRIMARY KEY,
    modelo                TEXT NOT NULL,
    marca                 TEXT NOT NULL,
    ano                   INTEGER NOT NULL,
    cor                   TEXT,
    tipo_combustivel      VARCHAR(50),
    preco                 NUMERIC(10, 2) NOT NULL,
    revisado              BOOLEAN DEFAULT FALSE,
    disponivel            BOOLEAN DEFAULT TRUE,
    freio_dianteiro       VARCHAR(50),
    freio_traseiro        VARCHAR(50),
    estilo                VARCHAR(50),
    cilindradas           INTEGER,
    velocidade_max        INTEGER
);

-- Tabela de Anúncios
-- Um anúncio agora pode se referir a um carro OU uma moto, mas não a ambos.
CREATE TABLE anuncios (
    id                    SERIAL PRIMARY KEY,
    funcionario_id        INTEGER REFERENCES funcionarios(id),
    carro_id              INTEGER UNIQUE REFERENCES carros(id) ON DELETE CASCADE,
    moto_id               INTEGER UNIQUE REFERENCES motos(id) ON DELETE CASCADE,
    data_publicacao       DATE NOT NULL DEFAULT CURRENT_DATE,
    imagem1_url           TEXT,
    imagem2_url           TEXT,
    imagem3_url           TEXT,
    -- Restrição para garantir que apenas um dos IDs de veículo seja preenchido
    CONSTRAINT chk_carro_moto_anuncio CHECK ((carro_id IS NOT NULL AND moto_id IS NULL) OR (carro_id IS NULL AND moto_id IS NOT NULL))
);

-- Tabela de Vendas
-- Registra a venda de um veículo, que deve ser realizada por um funcionário.
-- Agora tem chaves estrangeiras diretas para carros e motos.
CREATE TABLE vendas (
    id                    SERIAL PRIMARY KEY,
    carro_id              INTEGER UNIQUE REFERENCES carros(id) ON DELETE RESTRICT,
    moto_id               INTEGER UNIQUE REFERENCES motos(id) ON DELETE RESTRICT,
    cliente_id            INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    funcionario_id        INTEGER NOT NULL REFERENCES funcionarios(id) ON DELETE RESTRICT,
    data_venda            DATE NOT NULL DEFAULT CURRENT_DATE,
    valor_final           NUMERIC(10, 2) NOT NULL,
    comissao_venda        NUMERIC(10, 2),
    -- Restrição para garantir que apenas um dos IDs de veículo seja preenchido
    CONSTRAINT chk_carro_moto_venda CHECK ((carro_id IS NOT NULL AND moto_id IS NULL) OR (carro_id IS NULL AND moto_id IS NOT NULL))
);


-- Tabela de Interesses
-- Registra o interesse de um cliente em um veículo específico.
CREATE TABLE interesses (
    id                    SERIAL PRIMARY KEY,
    cliente_id            INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    carro_id              INTEGER REFERENCES carros(id) ON DELETE CASCADE,
    moto_id               INTEGER REFERENCES motos(id) ON DELETE CASCADE,
    data_visita           DATE,
    test_drive   BOOLEAN DEFAULT FALSE,
    -- Restrição para garantir que apenas um dos IDs de veículo seja preenchido
    CONSTRAINT chk_carro_moto_interesse CHECK ((carro_id IS NOT NULL AND moto_id IS NULL) OR (carro_id IS NULL AND moto_id IS NOT NULL)),
    -- Garante que um cliente não registre interesse duas vezes no mesmo carro ou moto
    UNIQUE (cliente_id, carro_id, moto_id)
);

-- ============================================================================
-- INSERÇÃO DE DADOS DE EXEMPLO
-- ============================================================================

-- Inserção de 10 Usuários
INSERT INTO usuarios (nome, cpf, email, senha) VALUES
('João Silva', '12345678909', 'joao.silva@email.com', '123456'),
('Maria Santos', '23456789012', 'maria.santos@email.com', '123456'),
('Pedro Oliveira', '34567890123', 'pedro.oliveira@email.com', '123456'),
('Ana Costa', '45678901234', 'ana.costa@email.com', '123456'),
('Carlos Pereira', '56789012345', 'carlos.pereira@email.com', '123456'),
('Lucia Fernandes', '67890123456', 'lucia.fernandes@email.com', '123456'),
('Roberto Lima', '78901234567', 'roberto.lima@email.com', '123456'),
('Fernanda Alves', '89012345678', 'fernanda.alves@email.com', '123456'),
('Marcos Admin', '90123456789', 'marcos.admin@email.com', '123456'),
('Carla Admin', '01234567890', 'carla.admin@email.com', '123456');

-- Inserção de 8 Funcionários (usuários 1 a 8)
INSERT INTO funcionarios (usuario_id, rendimento_mensal) VALUES
(1, 3500.00),
(2, 2000.00),
(3, 3500.00),
(4, 2000.00),
(5, 3500.00),
(6, 2000.00),
(7, 3500.00),
(8, 2000.00);

-- Inserção de 2 Administradores (usuários 9 e 10)
INSERT INTO admins (usuario_id, is_admin) VALUES
(9, TRUE),
(10, TRUE);

-- Inserção de 15 Clientes
INSERT INTO clientes (nome, cpf, email, telefone, endereco) VALUES
('Gabriel Mendes', '98765432100', 'gabriel.mendes@email.com', '(61) 99999-1111', 'QI 15 Conjunto A, Casa 12 - Guará I/DF'),
('Juliana Rocha', '87654321098', 'juliana.rocha@email.com', '(61) 99999-2222', 'SQN 408, Bloco B, Apto 205 - Asa Norte/DF'),
('Ricardo Souza', '76543210987', 'ricardo.souza@email.com', '(61) 99999-3333', 'QNM 36, Conjunto E, Casa 15 - Ceilândia/DF'),
('Camila Barbosa', '65432109876', 'camila.barbosa@email.com', '(61) 99999-4444', 'Quadra 102, Conjunto 5, Casa 8 - Samambaia/DF'),
('Bruno Cardoso', '54321098765', 'bruno.cardoso@email.com', '(61) 99999-5555', 'QS 01, Rua 210, Casa 22 - Águas Claras/DF'),
('Aline Martins', '43210987654', 'aline.martins@email.com', '(61) 99999-6666', 'SQS 312, Bloco C, Apto 108 - Asa Sul/DF'),
('Diego Ferreira', '32109876543', 'diego.ferreira@email.com', '(61) 99999-7777', 'QR 425, Conjunto 12, Casa 7 - Sobradinho/DF'),
('Tatiana Gomes', '21098765432', 'tatiana.gomes@email.com', '(61) 99999-8888', 'Quadra 203, Bloco A, Apto 304 - Recanto das Emas/DF'),
('Renato Dias', '10987654321', 'renato.dias@email.com', '(61) 99999-9999', 'AC 03, Lote 15, Setor A - Planaltina/DF'),
('Priscila Lopes', '19876543210', 'priscila.lopes@email.com', '(61) 99999-0000', 'QI 23, Conjunto B, Casa 18 - Guará II/DF'),
('Thiago Ribeiro', '18765432109', 'thiago.ribeiro@email.com', '(61) 98888-1111', 'Quadra 108, Conjunto 9, Casa 3 - Santa Maria/DF'),
('Vanessa Castro', '17654321098', 'vanessa.castro@email.com', '(61) 98888-2222', 'QNN 14, Conjunto F, Casa 25 - Ceilândia/DF'),
('André Nunes', '16543210987', 'andre.nunes@email.com', '(61) 98888-3333', 'SQN 203, Bloco D, Apto 412 - Asa Norte/DF'),
('Larissa Pinto', '15432109876', 'larissa.pinto@email.com', '(61) 98888-4444', 'QS 07, Lote 28, Setor Habitacional - Taguatinga/DF'),
('Felipe Ramos', '14321098765', 'felipe.ramos@email.com', '(61) 98888-5555', 'Quadra 305, Conjunto 4, Casa 11 - Samambaia/DF');

-- Inserção de 10 Carros Populares
INSERT INTO carros (modelo, marca, ano, cor, tipo_combustivel, preco, revisado, disponivel, tipo_direcao, tracao, consumo_cidade, airbag, ar_condicionado) VALUES
('Onix', 'Chevrolet', 2022, 'Prata', 'Flex', 65000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 12.5, TRUE, TRUE),
('HB20', 'Hyundai', 2023, 'Branco', 'Flex', 68000.00, TRUE, TRUE, 'Elétrica', 'Dianteira', 13.2, TRUE, TRUE),
('Gol', 'Volkswagen', 2021, 'Azul', 'Flex', 55000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 11.8, TRUE, FALSE),
('Palio', 'Fiat', 2020, 'Vermelho', 'Flex', 48000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 11.5, TRUE, TRUE),
('Ka', 'Ford', 2022, 'Preto', 'Flex', 58000.00, TRUE, TRUE, 'Elétrica', 'Dianteira', 12.8, TRUE, TRUE),
('Sandero', 'Renault', 2023, 'Cinza', 'Flex', 62000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 12.1, TRUE, TRUE),
('Etios', 'Toyota', 2021, 'Branco', 'Flex', 59000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 13.5, TRUE, TRUE),
('March', 'Nissan', 2020, 'Prata', 'Flex', 46000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 12.9, TRUE, FALSE),
('Mobi', 'Fiat', 2022, 'Amarelo', 'Flex', 52000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 13.8, TRUE, TRUE),
('Kwid', 'Renault', 2023, 'Laranja', 'Flex', 54000.00, TRUE, TRUE, 'Hidráulica', 'Dianteira', 14.2, TRUE, TRUE);

-- Inserção de 5 Motos Populares
INSERT INTO motos (modelo, marca, ano, cor, tipo_combustivel, preco, revisado, disponivel, freio_dianteiro, freio_traseiro, estilo, cilindradas, velocidade_max) VALUES
('CG 160', 'Honda', 2023, 'Vermelha', 'Gasolina', 12500.00, TRUE, TRUE, 'Disco', 'Tambor', 'Street', 160, 130),
('Factor 150', 'Yamaha', 2022, 'Azul', 'Gasolina', 11800.00, TRUE, TRUE, 'Disco', 'Tambor', 'Street', 150, 125),
('Titan 160', 'Honda', 2023, 'Preta', 'Gasolina', 13200.00, TRUE, TRUE, 'Disco', 'Disco', 'Street', 160, 135),
('XTZ 150', 'Yamaha', 2021, 'Branca', 'Gasolina', 14500.00, TRUE, TRUE, 'Disco', 'Disco', 'Adventure', 150, 120),
('Bros 160', 'Honda', 2022, 'Verde', 'Gasolina', 15800.00, TRUE, TRUE, 'Disco', 'Disco', 'Adventure', 160, 130);
