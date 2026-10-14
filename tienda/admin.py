from django.contrib import admin  # <-- Acá cambiamos .config por .contrib, porque en la prueba de python manage.py makemigrations dio error
from .models import Categoria, Producto

admin.site.register(Categoria)
admin.site.register(Producto)
