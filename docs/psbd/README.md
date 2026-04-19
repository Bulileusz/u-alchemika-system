# Dokumentacja PSBD

## Cel projektu

Projekt obejmuje przygotowanie warstwy bazodanowej dla systemu obiektu noclegowego "U Alchemika". Schemat uwzglednia podstawowe obszary domenowe:
- uzytkownikow i role
- pokoje i ich udogodnienia
- obrazy pokoi
- zapytania od klientow
- atrakcje lokalne
- wpisy informacyjne
- log audytowy

## Zawartosc katalogu

- `README.md` - skrotowy opis warstwy bazodanowej
- `erd/` - miejsce na diagram ERD i materialy pomocnicze

## Inicjalizacja bazy

Struktura bazy jest tworzona przez skrypt:

```text
database/init/001_init.sql
```

Skrypt jest wykonywany automatycznie przy pierwszym uruchomieniu kontenera PostgreSQL na pustym wolumenie danych.

## Uruchomienie

Z katalogu glownego projektu:

```bash
docker compose up -d
```

Weryfikacja tabel:

```bash
docker exec -it u_alchemika_db psql -U postgres -d u_alchemika -c "\\dt"
```

## Dalsze kroki

- uzupelnienie diagramu ERD
- rozbudowa danych testowych w `database/seeds`
- dodanie zapytan biznesowych i raportowych w `sql/queries.sql`
