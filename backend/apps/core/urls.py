from django.urls import path

from .views.rooms import index

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    # --- Osoba A: pokoje ---
    # path('pokoje/', rooms.room_list, name='room_list'),
    # path('pokoje/<slug:slug>/', rooms.room_detail, name='room_detail'),

    # --- Osoba B: zapytania i kontakt ---
    # path('zapytanie/', inquiries.inquiry_create, name='inquiry_create'),
    # path('kontakt/', inquiries.contact, name='contact'),
]
