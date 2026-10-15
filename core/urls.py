from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <-- Agregamos esto
from django.conf.urls.static import static  # <-- Agregamos esto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),
]

# Esto le habilita a Django mostrar las imágenes en tu computadora (Modo Desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
