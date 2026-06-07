<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.content.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
=======
from django.contrib import admin
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
=======
from django.contrib.auth import views as auth_views
>>>>>>> 776bd93 (feat: osoba B - formularze, HTMX, mailing, cache, auth)
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
<<<<<<< HEAD
    path('', include('apps.content.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
=======
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
>>>>>>> 776bd93 (feat: osoba B - formularze, HTMX, mailing, cache, auth)
>>>>>>> 51ade45 (wq)
