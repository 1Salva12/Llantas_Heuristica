from django.urls import path
from . import views

urlpatterns = [
    path('', views.optimizar_llantas, name='optimizar_llantas'),
]