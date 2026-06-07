"""
Dodatek do config/urls.py — Osoba B

Wklej poniższe urlpatterns do głównego config/urls.py projektu.
Zagadnienie #11 — uwierzytelnianie: login/logout wbudowane w Django.
"""

# Na górze pliku config/urls.py dodaj:
from django.contrib.auth import views as auth_views

# Do urlpatterns dołóż:
urlpatterns_auth = [
    # Login — Django renderuje gotowy formularz,
    # możesz nadpisać szablon: templates/registration/login.html
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]

# Przykład jak powinien wyglądać config/urls.py po dodaniu:
#
# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("apps.core.urls")),
#     path("", include("apps.content.urls")),
#     path("login/",  auth_views.LoginView.as_view(
#                         template_name="registration/login.html"), name="login"),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),
# ]
