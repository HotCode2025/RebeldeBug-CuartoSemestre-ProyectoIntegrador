from django.db import models
from django.contrib.auth.models import User  # <-- Importamos los usuarios de Django

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # <-- Control de stock en tiempo real
    imagen = models.ImageField(upload_to='productos/')  # <-- Enlazado a la carpeta de fotos
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

# Guarda las compras asociadas al usuario y su dirección histórica
class Pedido(models.Model):
    # Vinculamos al usuario de forma opcional (blank/null) por si prefieren compras sin registro en el futuro,
    # pero siempre vendrá enlazado al cliente logueado.
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    
    # Datos específicos de esta entrega en particular
    nombre_receptor = models.CharField(max_length=150)
    telefono_contacto = models.CharField(max_length=50)
    domicilio_entrega = models.CharField(max_length=255)
    entre_calles = models.CharField(max_length=255)
    rango_horario = models.CharField(max_length=100)
    
    # Información del pedido
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)  # Se vuelve True al volver exitoso de Mercado Pago
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Pedido #{self.id} - {self.nombre_receptor} ({estado})"
