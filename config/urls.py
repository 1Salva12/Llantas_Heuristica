from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('optimizador.urls')),  # Apunta directo a las urls de la app
]