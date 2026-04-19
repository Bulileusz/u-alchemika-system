# U Alchemika System

Projekt realizowany w ramach przedmiotow:
- Projektowanie i programowanie systemow internetowych I
- Projektowanie systemow baz danych

Repozytorium zawiera warstwe bazodanowa systemu dla obiektu noclegowego "U Alchemika". Na obecnym etapie projekt obejmuje konfiguracje PostgreSQL w Dockerze, bazowy schemat danych oraz pomocnicze pliki SQL do testow i dalszego rozwoju.

## Technologie

- PostgreSQL 16
- Docker Compose

## Struktura repozytorium

- `database/init` - skrypty inicjalizujace strukture bazy
- `database/seeds` - przykladowe dane testowe
- `docs/psbd` - dokumentacja projektu bazodanowego
- `sql` - pomocnicze zapytania SQL do testow
- `docker-compose.yml` - konfiguracja kontenera PostgreSQL

## Wymagania

- Docker Desktop lub silnik Docker z obsluga `docker compose`

## Uruchomienie projektu

1. Uruchom baze danych:

```bash
docker compose up -d
```

2. Sprawdz stan kontenera:

```bash
docker ps
```

3. Odczytaj logi bazy:

```bash
docker logs u_alchemika_db
```

4. Polacz sie z PostgreSQL:

```bash
docker exec -it u_alchemika_db psql -U postgres -d u_alchemika
```

## Weryfikacja schematu

Lista tabel po poprawnej inicjalizacji:

```bash
docker exec -it u_alchemika_db psql -U postgres -d u_alchemika -c "\\dt"
```

Oczekiwane tabele:
- `amenities`
- `attractions`
- `audit_logs`
- `inquiries`
- `posts`
- `roles`
- `room_amenities`
- `room_images`
- `rooms`
- `users`

## Restart na czysto

Jesli chcesz odtworzyc baze od zera i ponownie wykonac skrypt `001_init.sql`, usun kontener i wolumen:

```bash
docker compose down --volumes --remove-orphans
docker compose up -d
```

## Zmienne srodowiskowe

Przykladowe wartosci znajduja sie w pliku `.env.example`. Na tym etapie `docker-compose.yml` korzysta z wartosci zapisanych bezposrednio w konfiguracji, ale plik pozostaje gotowy do dalszego rozwoju projektu.
