# --------------------------------------------------------------------------
# CONTRIBUTOR CHECK - DEVOPS & DATA ENGINEER: Zoe Garnica
# Configuración de migraciones en servidor local y producción. Mapeo de auth_user para login por teléfono.
# --------------------------------------------------------------------------


from django.db import models
from django.contrib.auth.models import User  # Importamos el modelo de usuarios base de Django

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)  # Control de stock en tiempo real para el catálogo
    imagen = models.ImageField(upload_to='productos/')  # Enlace al directorio de almacenamiento de imágenes
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

# Modelo para gestionar el historial de compras y direcciones de entrega
class Pedido(models.Model):
    # Vinculación opcional del cliente para mantener el soporte de compras como invitado
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    
    # Datos específicos de esta entrega y logistica
    nombre_receptor = models.CharField(max_length=150)
    telefono_contacto = models.CharField(max_length=50)
    domicilio_entrega = models.CharField(max_length=255)
    entre_calles = models.CharField(max_length=255)
    rango_horario = models.CharField(max_length=100)
    
    # Resumen económico y estado de la pasarela de pagos
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)  # Modificado dinámicamente tras el retorno de Mercado Pago
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Pedido #{self.id} - {self.nombre_receptor} ({estado})"
