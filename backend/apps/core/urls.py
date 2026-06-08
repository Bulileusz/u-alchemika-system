from django.urls import path
from .views import rooms
from .views.inquiries import (
    contact,
    inquiry_create,
    inquiry_list,
    property_info,
)

app_name = "core"

urlpatterns = [
    path("", rooms.index, name="index"),
    path("pokoje/", rooms.room_list, name="room_list"),
    path("pokoje/<slug:slug>/", rooms.room_detail, name="room_detail"),
    path("galeria/", rooms.gallery, name="gallery"),
    path("zapytanie/", inquiry_create, name="inquiry-create"),
    path("zapytanie/<slug:room_slug>/", inquiry_create, name="inquiry-create-room"),
    path("kontakt/", contact, name="contact"),
    path("obiekt/", property_info, name="property-info"),
    path("panel/zapytania/", inquiry_list, name="inquiry-list"),
]
