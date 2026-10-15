from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # El camino vacío '' representa la página de inicio (Home)
]
