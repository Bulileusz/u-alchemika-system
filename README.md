# U Alchemika System

Projekt realizowany w ramach przedmiotów:
- Projektowanie i programowanie systemów internetowych I
- Projektowanie systemów baz danych

System obsługi obiektu noclegowego „U Alchemika" — aplikacja webowa Django z bazą PostgreSQL.

## Technologie

- Python 3.12 + Django 4.2
- PostgreSQL 16
- Docker Compose

## Struktura repozytorium

```
u-alchemika-system/
├── backend/               — aplikacja Django
│   ├── config/            — ustawienia projektu (settings.py, urls.py)
│   └── apps/
│       ├── core/          — pokoje, udogodnienia, zapytania, logi
│       └── content/       — posty, atrakcje
├── database/
│   ├── init/001_init.sql  — historyczny prototyp schematu (artefakt)
│   └── seeds/             — historyczne dane testowe (artefakt)
├── docs/psbd/             — dokumentacja bazy danych i ERD
└── docker-compose.yml     — konfiguracja serwisów db + web
```

## Wymagania

- Docker Desktop z obsługą `docker compose`

## Uruchomienie projektu

```bash
# 1. Uruchom kontenery (buduje obraz Django i startuje db + web)
docker compose up --build -d

# 2. Sprawdź logi — migracje Django powinny przejść bez błędów
docker logs u_alchemika_web

# 3. Załaduj dane testowe
docker exec -it u_alchemika_web python manage.py loaddata seed

# 4. Utwórz konto administratora
docker exec -it u_alchemika_web python manage.py createsuperuser
```

Panel administracyjny: **http://localhost:8000/admin/**

## Migracje

```bash
# Sprawdź stan migracji
docker exec -it u_alchemika_web python manage.py showmigrations

# Cofnij ostatnią migrację core (demo rollbacku)
docker exec -it u_alchemika_web python manage.py migrate core 0002

# Przywróć do HEAD
docker exec -it u_alchemika_web python manage.py migrate core
```

## Weryfikacja tabel w bazie

```bash
docker exec -it u_alchemika_db psql -U postgres -d u_alchemika -c "\dt"
```

## Restart na czysto

```bash
docker compose down --volumes --remove-orphans
docker compose up --build -d
```

## Testy

```bash
docker exec -it u_alchemika_web python manage.py test
```

## Zmienne środowiskowe

Plik `.env.example` zawiera wzorzec zmiennych. Serwisy Docker korzystają z wartości zdefiniowanych bezpośrednio w `docker-compose.yml` (sekcja `environment`) — nie jest wymagane tworzenie `.env` do uruchomienia przez Docker.

Do lokalnego uruchomienia poza Dockerem skopiuj `.env.example` → `.env` i dostosuj wartości.
