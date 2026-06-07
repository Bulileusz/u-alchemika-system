# Osoba B — feature/inquiries

## Pliki do dodania do repozytorium

```
backend/
├── apps/core/
│   ├── forms.py                              ← nowy
│   ├── views/
│   │   └── inquiries.py                      ← nowy
│   ├── urls.py                               ← edytuj (dodaj swoją sekcję)
│   └── templates/core/
│       ├── inquiry_form.html                 ← nowy
│       ├── _inquiry_form.html                ← nowy (HTMX partial)
│       ├── _inquiry_success.html             ← nowy (HTMX partial)
│       ├── _contact_cta.html                 ← nowy (partial → index.html)
│       ├── contact.html                      ← nowy
│       ├── property_info.html                ← nowy
│       ├── inquiry_list.html                 ← nowy (panel, @login_required)
│       ├── registration/
│       │   └── login.html                    ← nowy
│       └── emails/
│           └── inquiry_confirmation.txt      ← nowy
└── static/core/js/
    └── inquiry.js                            ← nowy
```

---

## Zmiany w istniejących plikach

### `config/settings.py` — dołóż na końcu:
Zawartość z pliku `config/settings_additions.py` (CACHES, EMAIL, LOGGING, AUTH).

### `config/urls.py` — dołóż:
```python
from django.contrib.auth import views as auth_views

urlpatterns += [
    path("login/",  auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
```

### `docker-compose.yml` — dołóż serwisy:
Zawartość z pliku `config/docker_compose_additions.yml` (mailhog + redis).

### `requirements.txt` — dołóż:
```
django-redis==5.4.0
```

### `apps/core/views/__init__.py` — upewnij się, że istnieje (może być pusty)

---

## Pokryte zagadnienia z listy prowadzącego

| # | Zagadnienie | Gdzie |
|---|---|---|
| 1 | framework MVC | widoki Django (views/inquiries.py) |
| 2 | framework CSS | Bootstrap 5 w szablonach |
| 4 | **cache** | `@cache_page` na `property_info`, ręczny `cache.get/set` w `contact` |
| 6 | HTML | wszystkie szablony `.html` |
| 7 | CSS | Bootstrap klasy w szablonach |
| 8 | **JavaScript** | `inquiry.js` — licznik znaków, walidacja dat |
| 9 | routing | `urls.py` z named URLs (`name=`) |
| 10 | ORM | `InquiryForm.save()` → zapis przez ORM |
| 11 | **uwierzytelnianie** | `@login_required` na `inquiry_list`, login/logout views |
| 13 | **mailing** | `send_mail()` po zapisaniu zapytania, MailHog w dev |
| 14 | formularze | `InquiryForm` (ModelForm) z walidacją |
| 15 | **async HTMX** | `hx-post`, `hx-target`, `hx-swap`, `hx-indicator` |
| 18 | RWD | Bootstrap grid we wszystkich widokach |
| 19 | **logger** | `logging.getLogger(__name__)` w widokach |

**Razem: 14 z 20 zagadnień pokrytych głównie przez Twój branch.**

---

## Uruchomienie

```bash
# Po merge Fazy 0 i podpiąć swój branch:
git checkout main && git pull origin main
git checkout -b feature/inquiries

# Skopiuj pliki, uruchom:
docker compose up --build

# Panel e-maili (MailHog):
open http://localhost:8025

# Strona z formularzem:
open http://localhost:8000/zapytanie/

# Panel zapytań (trzeba być zalogowanym):
open http://localhost:8000/panel/zapytania/
```

---

## Uwaga: katalog `logs/`

Logging zapisuje do `backend/logs/app.log`. Utwórz katalog:
```bash
mkdir -p backend/logs
echo "*.log" >> backend/logs/.gitignore
```
