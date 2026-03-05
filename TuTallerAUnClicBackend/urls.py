from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye TODAS las rutas de TuTallerApp
    path('', include('TuTallerApp.urls')),
    path('usuarios/login/refresh/', TokenRefreshView.as_view()),
]