# ============================================================
# Dodatki do settings.py — Osoba B
# Wklej do backend/config/settings.py w odpowiednie sekcje
# ============================================================


# ── Zagadnienie #4: Cache ────────────────────────────────────────────────────
# Redis przez Docker Compose (usługa "redis").
# Fallback: LocMemCache jeśli Redis niedostępny.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        # Jeśli chcesz prostszy fallback bez Redisa, użyj zamiast:
        # "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}


# ── Zagadnienie #13: Mailing (MailHog w dev) ─────────────────────────────────
# MailHog startuje jako serwis w docker-compose.yml (patrz niżej).
# Panel podglądu e-maili: http://localhost:8025
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST    = "mailhog"       # nazwa serwisu w Docker Compose
EMAIL_PORT    = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

# Dla produkcji nadpisz przez zmienne środowiskowe:
#   EMAIL_HOST=smtp.sendgrid.net EMAIL_PORT=587 EMAIL_USE_TLS=True
#   EMAIL_HOST_USER=apikey EMAIL_HOST_PASSWORD=<klucz>


# ── Zagadnienie #19: Logging ─────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {name}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "app.log",
            "maxBytes": 5 * 1024 * 1024,   # 5 MB
            "backupCount": 3,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        # Logi naszej aplikacji — INFO i wyżej
        "apps": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        # Django request errors
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


# ── Zagadnienie #11: Uwierzytelnianie ────────────────────────────────────────
# Django ma login/logout wbudowane — wystarczy podpiąć URL i ustawić redirecty.
LOGIN_URL          = "/login/"
LOGIN_REDIRECT_URL = "/panel/zapytania/"
LOGOUT_REDIRECT_URL = "/"

# Hasło: minimalne wymagania
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
