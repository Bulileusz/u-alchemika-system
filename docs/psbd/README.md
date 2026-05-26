# Dokumentacja techniczna — Projektowanie systemów baz danych

## Cel projektu

Projekt obejmuje zaprojektowanie i implementację relacyjnej bazy danych dla systemu obsługi obiektu noclegowego „U Alchemika". Baza danych stanowi warstwę persystencji aplikacji webowej opartej na Django.

---

## Encje i relacje

### Tabele aplikacyjne

| Encja | Opis | Powiązania |
|---|---|---|
| `core_room` | Pokoje obiektu (nazwa, slug, opis, cena, pojemność) | 1:N → room_images, M:N ↔ amenities via room_amenities, 1:N → inquiries |
| `core_roomimage` | Zdjęcia pokoi (URL, alt text, kolejność) | N:1 → room (CASCADE DELETE) |
| `core_amenity` | Udogodnienia (WiFi, parking, etc.) | M:N ↔ rooms via room_amenities |
| `core_roomamenity` | Tabela łącząca pokoje z udogodnieniami | N:1 → room (CASCADE), N:1 → amenity (CASCADE) |
| `core_inquiry` | Zapytania od klientów (formularz kontaktowy / zapytanie o nocleg) | N:1 → room (SET NULL on delete) |
| `core_auditlog` | Log akcji administracyjnych | N:1 → auth_user (SET NULL on delete) |
| `content_post` | Posty / aktualności | — |
| `content_attraction` | Atrakcje w okolicy | — |
| `auth_user` | Wbudowany model użytkownika Django | 1:N → audit_logs |

### Kardynalności

```
auth_user  1 ──── N  audit_logs      (SET NULL przy usunięciu usera)
room       1 ──── N  room_images     (CASCADE DELETE)
room       1 ──── N  inquiries       (SET NULL przy usunięciu pokoju)
room       M ──── N  amenities       (via room_amenities, CASCADE obie strony)
```

---

## Reguły integralności

### Klucze obce i strategie usuwania

| Tabela | Kolumna FK | Referencja | ON DELETE |
|---|---|---|---|
| `core_room` | — | — | — |
| `core_roomimage` | `room_id` | `core_room.id` | CASCADE |
| `core_roomamenity` | `room_id` | `core_room.id` | CASCADE |
| `core_roomamenity` | `amenity_id` | `core_amenity.id` | CASCADE |
| `core_inquiry` | `room_id` | `core_room.id` | SET NULL |
| `core_auditlog` | `user_id` | `auth_user.id` | SET NULL |

### Ograniczenia unikalności

| Tabela | Kolumna | Opis |
|---|---|---|
| `core_room` | `slug` | Unikalny identyfikator URL pokoju |
| `core_amenity` | `name` | Nazwa udogodnienia unikalna w systemie |
| `core_roomamenity` | `(room_id, amenity_id)` | Brak duplikatów w tabeli łączącej |
| `content_post` | `slug` | Unikalny identyfikator URL posta |

### Walidacja danych

- `core_inquiry`: walidacja `date_to >= date_from` w metodzie `clean()` modelu Django
- `core_room.capacity`: typ `PositiveIntegerField` — wymusza wartość > 0
- `core_inquiry.guests`: typ `PositiveIntegerField` — wymusza wartość > 0

### Indeksy

| Tabela | Indeks | Uzasadnienie |
|---|---|---|
| `core_room` | `room_slug_idx` na `slug` | Wyszukiwanie pokoi po URL |
| `core_inquiry` | `inquiry_status_idx` na `status` | Filtrowanie zapytań po statusie (panel admin) |
| `core_inquiry` | `inquiry_email_idx` na `email` | Wyszukiwanie zapytań po emailu klienta |

---

## Historia migracji

| Nr | Opis zmian | Jak cofnąć |
|---|---|---|
| `core/0001_initial` | Tworzenie tabel: Room, RoomImage, Amenity, RoomAmenity, Inquiry, AuditLog + indeksy | `python manage.py migrate core zero` |
| `content/0001_initial` | Tworzenie tabel: Post, Attraction | `python manage.py migrate content zero` |
| `core/0002_room_updated_at` | Dodanie pola `updated_at` do Room | `python manage.py migrate core 0001` |
| `core/0003_inquiry_index_created_at` | Dodanie indeksu na `Inquiry.created_at` (optymalizacja) | `python manage.py migrate core 0002` |

### Przykłady rollbacku

```bash
# Cofnięcie ostatniej migracji core (indeks created_at)
python manage.py migrate core 0002

# Cofnięcie do stanu przed dodaniem updated_at
python manage.py migrate core 0001

# Weryfikacja aktualnego stanu migracji
python manage.py showmigrations
```

---

## Architektura Docker

Projekt uruchamia dwa serwisy:

```
docker-compose.yml
├── db  (postgres:16)  — port 5432
│   └── healthcheck: pg_isready — web czeka na jego przejście
└── web (python:3.12)  — port 8000
    ├── CMD: python manage.py migrate && runserver
    └── volume: ./backend:/app (bind mount — zmiany widoczne lokalnie)
```

Wolumen `postgres_data` przechowuje dane bazy pomiędzy restartami.

---

## Uruchomienie projektu od zera

```bash
# 1. Sklonuj repo i wejdź do katalogu
git clone <repo-url>
cd u-alchemika-system

# 2. Uruchom kontenery (buduje obraz Django i startuje oba serwisy)
docker compose up --build -d

# 3. Sprawdź logi — migracje powinny przejść bez błędów
docker logs u_alchemika_web

# 4. Załaduj dane testowe
docker exec -it u_alchemika_web python manage.py loaddata seed

# 5. Utwórz superusera do panelu admin
docker exec -it u_alchemika_web python manage.py createsuperuser

# 6. Otwórz panel administracyjny
# http://localhost:8000/admin/
```

### Resetowanie bazy

```bash
docker compose down --volumes --remove-orphans
docker compose up --build -d
```

### Weryfikacja tabel w bazie

```bash
docker exec -it u_alchemika_db psql -U postgres -d u_alchemika -c "\dt"
```

---

## Uruchomienie testów

```bash
docker exec -it u_alchemika_web python manage.py test
```

---

## ERD

Diagram encji dostępny w katalogu [`erd/`](erd/).

**Do uzupełnienia:** Eksport z dbdiagram.io jako `erd/erd.png` i `erd/schema.dbml`.

Encje do zamodelowania w narzędziu:
- `auth_user` (Django built-in — blok zewnętrzny)
- `core_room`, `core_roomimage`, `core_amenity`, `core_roomamenity`
- `core_inquiry`, `core_auditlog`
- `content_post`, `content_attraction`
