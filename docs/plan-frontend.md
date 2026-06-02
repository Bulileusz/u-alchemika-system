# Plan frontendu — U Alchemika System

**Przedmiot:** Projektowanie i programowanie systemów internetowych I  
**Etap:** Warstwa webowa (baza danych gotowa)  
**Zespół:** 3 osoby, każda na własnym branchu

---

## Stack technologiczny

| Warstwa | Technologia |
|---------|------------|
| Backend | Django 4.2 |
| Baza danych | PostgreSQL 16 (gotowe) |
| CSS | Bootstrap 5 przez CDN |
| Interaktywność | HTMX |
| Szablony | Django Templates |
| Uruchomienie | Docker Compose |

---

## Faza 0 — Fundament wspólny

> **Jedna osoba** robi to jako pierwsza i merguje do `main`.  
> Dopiero potem każdy odgałęzia swój branch.

Zakres Fazy 0:

- **`settings.py`** — dodanie katalogu szablonów, statyk, context processora
- **`context_processors.py`** — `PropertyInfo` (telefon, booking URL, Facebook) dostępne globalnie w każdym szablonie (navbar, stopka)
- **`base.html`** — szkielet z Bootstrap 5 CDN + HTMX CDN, navbar, stopka, blok na messages
- **`index.html`** — strona główna składana z 3 partiali `{% include %}` (każda osoba dostarcza swój partial)
- **`style.css`** — bazowe style marki
- **`config/urls.py`** — routing główny do obu aplikacji
- **Szkielety `urls.py`** dla `core` i `content` z oznaczonymi sekcjami dla każdej osoby
- **`views/` jako pakiet** (`rooms.py`, `inquiries.py`) — żeby osoby A i B nie kolidowały w jednym pliku
- Placeholdery partiali — strona główna renderuje się od razu, nawet pusta

---

## Podział pracy

### 👤 Osoba A — Pokoje + strona główna
**Branch:** `feature/rooms`

**Pliki:**
- `apps/core/views/rooms.py` — widoki: `index`, `room_list`, `room_detail`
- `templates/core/room_list.html`
- `templates/core/room_detail.html`
- `templates/core/_featured_rooms.html` ← partial do strony głównej
- sekcja pokoi w `apps/core/urls.py`

**Co robi:**
- Lista pokoi — karty Bootstrap: zdjęcie, nazwa, cena, liczba osób
- Szczegóły pokoju — galeria zdjęć (wg `display_order`), znaczniki udogodnień
- Przyciski: „Zarezerwuj" → Booking.com, „Zapytaj" → formularz (Osoba B)
- Partial ze wyróżnionymi pokojami na stronie głównej

---

### 👤 Osoba B — Formularz zapytań (HTMX) + kontakt + dane obiektu
**Branch:** `feature/inquiries`

**Pliki:**
- `apps/core/forms.py` — `InquiryForm` (ModelForm; walidacja dat z modelu)
- `apps/core/views/inquiries.py` — widoki: `inquiry_create`, `contact`, `property_info`
- `templates/core/inquiry_form.html`
- `templates/core/_inquiry_form.html` ← partial HTMX
- `templates/core/_inquiry_success.html` ← partial HTMX po sukcesie
- `templates/core/contact.html`
- `templates/core/property_info.html`
- `templates/core/_contact_cta.html` ← partial do strony głównej
- sekcja zapytań/kontaktu w `apps/core/urls.py`

**Co robi:**
- Formularz wysyłany przez HTMX bez przeładowania strony (`hx-post`, `hx-target`, `hx-swap`)
- Serwer zwraca partial z formularzem (z błędami) lub partial sukcesu
- Strona kontaktu i informacje o obiekcie (godziny, płatności, polityki) z `PropertyInfo`

---

### 👤 Osoba C — Blog + atrakcje okolicy
**Branch:** `feature/content`

**Pliki (cała apka `content` — ZERO konfliktów z A i B):**
- `apps/content/views.py` — widoki: `post_list`, `post_detail`, `attraction_list`
- `apps/content/urls.py`
- `templates/content/post_list.html`
- `templates/content/post_detail.html`
- `templates/content/attraction_list.html`
- `templates/content/_attractions_teaser.html` ← partial do strony głównej

**Co robi:**
- Lista i szczegóły wpisów blogowych (tylko `is_published=True`)
- Lista atrakcji okolicy z opisem i lokalizacją
- Partial z zajawką atrakcji na stronie głównej

> **Dobry moduł dla osoby uczącej się** — apka `content` jest całkowicie niezależna.

---

## Jak strona główna się składa

```
index.html (Faza 0)
├── {% include 'core/_featured_rooms.html' %}     ← Osoba A
├── {% include 'content/_attractions_teaser.html' %} ← Osoba C
└── {% include 'core/_contact_cta.html' %}         ← Osoba B
```

Nikt nie edytuje cudzego partiala → brak konfliktów.

---

## Strategia Git — jak unikać konfliktów

| Plik | Właściciel | Uwagi |
|------|-----------|-------|
| `views/rooms.py` | Osoba A | oddzielny plik |
| `views/inquiries.py` | Osoba B | oddzielny plik |
| `apps/content/` (cały katalog) | Osoba C | oddzielna apka |
| `apps/core/urls.py` | A + B (osobne sekcje) | jedyny celowo współdzielony plik |
| `templates/core/_featured_rooms.html` | Osoba A | |
| `templates/core/_contact_cta.html` | Osoba B | |
| `templates/content/_attractions_teaser.html` | Osoba C | |

`apps/core/urls.py` to jedyny plik, w którym może dojść do merge'a — celowo, żeby każdy przeszedł przez tę sytuację.

---

## Workflow Git krok po kroku

```bash
# 1. Po zmergowaniu Fazy 0 — każda osoba:
git checkout main
git pull origin main
git checkout -b feature/rooms       # lub inquiries / content

# 2. Praca na branchu...

# 3. Regularne synchronizowanie z mainem:
git fetch origin
git rebase origin/main

# 4. Gotowe → PR do main
```

**Sugerowana kolejność merge:** A → B → C  
(B linkuje do formularza z kart pokoi A, ale partiale są niezależne — kolejność elastyczna)

---

## Weryfikacja gotowości

```bash
docker compose up --build
docker compose exec web python manage.py loaddata seed
```

Otworzyć `http://localhost:8000` i sprawdzić:

- [ ] `/` — hero + wyróżnione pokoje + atrakcje + CTA kontaktu
- [ ] `/pokoje/` — lista pokoi z kartami
- [ ] `/pokoje/<slug>/` — szczegóły: galeria, udogodnienia, przyciski
- [ ] Formularz zapytań — HTMX, bez przeładowania, walidacja inline
- [ ] Zapytanie pojawia się w `/admin/` → Zapytania
- [ ] `/blog/` i `/blog/<slug>/` — wpisy blogowe
- [ ] `/atrakcje/` — lista atrakcji
- [ ] Navbar i stopka — dane z PropertyInfo na każdej stronie
