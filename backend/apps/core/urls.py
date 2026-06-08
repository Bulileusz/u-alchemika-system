from django.urls import path

from .views import rooms

app_name = "core"

urlpatterns = [
    path("", rooms.index, name="index"),
    path("pokoje/", rooms.room_list, name="room_list"),
    path("pokoje/<slug:slug>/", rooms.room_detail, name="room_detail"),
    path("galeria/", rooms.gallery, name="gallery"),
]
    # --- Osoba B: zapytania i kontakt ---
    # path('zapytanie/', inquiries.inquiry_create, name='inquiry_create'),
    # path('kontakt/', inquiries.contact, name='contact'),

