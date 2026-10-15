from django.shortcuts import render
from .models import Producto

def home(request):
    # Traemos todos los productos cargados en la base de datos
    productos = Producto.objects.all()
    # Se los enviamos a la plantilla HTML llamada home.html
    return render(request, 'home.html', {'productos': productos})

def checkout(request):
    # Esta vista va a renderizar la pantalla del formulario de entrega
    return render(request, 'checkout.html')

