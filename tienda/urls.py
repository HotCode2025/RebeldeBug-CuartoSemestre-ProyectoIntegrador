from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carrito/', views.carrito_api, name='carrito_api'),
    path('checkout/', views.checkout, name='checkout'),
    path('pedido-exitoso/', views.pedido_exitoso, name='pedido_exitoso'),
]