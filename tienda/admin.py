from django.contrib import admin  
from .models import Categoria, Producto, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)
    list_editable = ('precio', 'stock', 'disponible')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_receptor', 'telefono_contacto', 'total', 'pagado', 'fecha_creacion')
    list_filter = ('pagado', 'fecha_creacion')
    search_fields = ('nombre_receptor', 'telefono_contacto', 'domicilio_entrega')
