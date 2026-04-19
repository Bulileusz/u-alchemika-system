-- Minimalny seed testowy.
-- Ten plik nie jest automatycznie wykonywany przez aktualny docker-compose.yml.
-- Mozna go uruchomic recznie po starcie bazy:
-- docker exec -i u_alchemika_db psql -U postgres -d u_alchemika < database/seeds/001_seed.sql

INSERT INTO roles (name)
VALUES
    ('admin'),
    ('editor')
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (role_id, first_name, last_name, email, password_hash)
SELECT 1, 'Admin', 'Systemu', 'admin@ualchemika.local', 'demo_hash'
WHERE NOT EXISTS (
    SELECT 1
    FROM users
    WHERE email = 'admin@ualchemika.local'
);
