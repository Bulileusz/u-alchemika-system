-- Przykladowe zapytania testowe dla bazy u_alchemika.

-- 1. Lista wszystkich tabel w schemacie public.
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 2. Lista pokoi z podstawowymi informacjami.
SELECT id, name, slug, capacity, base_price, is_active
FROM rooms
ORDER BY id;

-- 3. Uzytkownicy wraz z przypisana rola.
SELECT
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    r.name AS role_name
FROM users AS u
JOIN roles AS r ON r.id = u.role_id
ORDER BY u.id;

-- 4. Pokoje i przypisane udogodnienia.
SELECT
    rm.name AS room_name,
    a.name AS amenity_name
FROM room_amenities AS ra
JOIN rooms AS rm ON rm.id = ra.room_id
JOIN amenities AS a ON a.id = ra.amenity_id
ORDER BY rm.name, a.name;

-- 5. Zapytania klientow w kolejnosci od najnowszych.
SELECT id, full_name, email, status, created_at
FROM inquiries
ORDER BY created_at DESC;
