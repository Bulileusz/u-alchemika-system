"""
apps/core/urls.py
Sekcje dla Osoby A i Osoby B są oznaczone komentarzami.
Zagadnienie #9 — routing z pretty URLs i named URLs.
"""

from django.urls import path

# ============================================================
# OSOBA A — pokoje (uzupełnij po merge Osoby A)
# ============================================================
# from .views.rooms import index, room_list, room_detail
#
# urlpatterns_rooms = [
#     path("", index, name="index"),
#     path("pokoje/", room_list, name="room-list"),
#     path("pokoje/<slug:slug>/", room_detail, name="room-detail"),
# ]
# ============================================================

# ============================================================
# OSOBA B — zapytania i kontakt
# ============================================================
from .views.inquiries import (
    contact,
    inquiry_create,
    inquiry_list,
    property_info,
)

urlpatterns = [
    # Formularz zapytania (ogólny)
    path("zapytanie/", inquiry_create, name="inquiry-create"),

    # Formularz zapytania z pre-wybranym pokojem (linkowane z kart pokoi Osoby A)
    path("zapytanie/<slug:room_slug>/", inquiry_create, name="inquiry-create-room"),

    # Strona kontaktu
    path("kontakt/", contact, name="contact"),

    # Informacje o obiekcie
    path("obiekt/", property_info, name="property-info"),

    # Panel zapytań (tylko zalogowani) — zagadnienie #11
    path("panel/zapytania/", inquiry_list, name="inquiry-list"),
]
# ============================================================
# koniec OSOBA B
# ============================================================
