-- init.sql De teste!

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email)
VALUES 
    ('Admin', 'admin@exemplo.com'),
    ('Usuário Teste', 'teste@exemplo.com')
ON CONFLICT (email) DO NOTHING;