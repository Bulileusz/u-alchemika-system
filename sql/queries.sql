-- Przykladowe zapytania testowe dla bazy u_alchemika uruchamianej przez Django.

-- 1. Lista wszystkich tabel w schemacie public.
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 2. Lista pokoi z podstawowymi informacjami.
SELECT id, name, slug, capacity, base_price, is_active
FROM core_room
ORDER BY id;

-- 3. Uzytkownicy Django.
SELECT
    u.id,
    u.email,
    u.username,
    u.is_active,
    u.date_joined
FROM auth_user AS u
ORDER BY u.id;

-- 4. Pokoje i przypisane udogodnienia.
SELECT
    rm.name AS room_name,
    a.name AS amenity_name
FROM core_roomamenity AS ra
JOIN core_room AS rm ON rm.id = ra.room_id
JOIN core_amenity AS a ON a.id = ra.amenity_id
ORDER BY rm.name, a.name;

-- 5. Zapytania klientow w kolejnosci od najnowszych.
SELECT id, full_name, email, status, created_at
FROM core_inquiry
ORDER BY created_at DESC;

-- 6. EXPLAIN ANALYZE dla zapytan filtrowanych po statusie.
EXPLAIN ANALYZE
SELECT id, full_name, email, status, created_at
FROM core_inquiry
WHERE status = 'new'
ORDER BY created_at DESC;
