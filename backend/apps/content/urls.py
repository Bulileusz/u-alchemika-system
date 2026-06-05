from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
  # --- Osoba C: blog i atrakcje ---
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('atrakcje/', views.attraction_list, name='attraction_list'),
]

