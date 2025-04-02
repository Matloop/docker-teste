-- init.sql
-- Cria a tabela apenas se ela não existir
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Insere alguns dados iniciais apenas se a tabela estiver vazia
-- (Previne inserção duplicada se o container for recriado mas o volume persistir)
DO $$
BEGIN
   IF (SELECT COUNT(*) FROM items) = 0 THEN
      INSERT INTO items (name) VALUES
      ('Item Padrão A via init.sql'),
      ('Item Padrão B via init.sql'),
      ('Item Padrão C via init.sql');
   END IF;
END $$;