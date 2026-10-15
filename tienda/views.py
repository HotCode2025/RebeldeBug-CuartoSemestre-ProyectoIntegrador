from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
import mercadopago

# Tu Access Token original de Información General con los guiones corregidos
sdk = mercadopago.SDK("APP-USR-1183847139670830-101510-7954a1bf55e5c9f52f36f6aa2e70e9f4-3689791640")

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def checkout(request):
    if request.method == 'POST':
        # 1. Capturamos los datos del formulario de Malargüe
        nombre_recibe = request.POST.get('nombre')
        telefono_contacto = request.POST.get('telefono')
        calle_altura = request.POST.get('domicilio')
        entre_calles = request.POST.get('entrecalles')
        rango_horario = request.POST.get('horario')
        
        # 2. Preparamos el mensaje de WhatsApp de respaldo por si falla la API
        mensaje_whatsapp = f"Hola Pastas a Colores! Nuevo pedido de {nombre_recibe}. Entregar en {calle_altura} (Entre calles: {entre_calles}) en el rango de la {rango_horario}. Teléfono: {telefono_contacto}."
        telefono_negocio = "5492604507091" 
        url_whatsapp_respaldo = f"https://wa.me{telefono_negocio}?text={mensaje_whatsapp.replace(' ', '%20')}"
        
        # 3. Estructura de datos para procesar la orden en Mercado Pago
        preference_data = {
            "items": [
                {
                    "title": "Pedido - Pastas a Colores",
                    "quantity": 1,
                    "unit_price": 1500,
                    "currency_id": "ARS"
                }
            ],
            "payer": {
                "name": nombre_recibe,
                "email": "comprador_prueba@testuser.com", # Email ficticio obligatorio para no chocar con tu cuenta real
                "phone": {
                    "area_code": "260",
                    "number": telefono_contacto[-7:] if telefono_contacto else "1234567"
                }
            },
            "back_urls": {
                "success": "http://localhost:8000/",
                "failure": "http://localhost:8000/",
                "pending": "http://localhost:8000/"
            }
        }

        # 4. Intentamos conectar con Mercado Pago
        try:
            preference_response = sdk.preference().create(preference_data)
            status_code = preference_response["status"]
            preference = preference_response["response"]
            
            # Si el token general responde bien, saltamos directo a la pasarela azul
            if status_code == 201 and "init_point" in preference:
                return redirect(preference["init_point"])
            else:
                # Si Mercado Pago tira error de políticas por estar logueada, te manda al WhatsApp directo para no frenar
                return redirect(url_whatsapp_respaldo)
                
        except Exception:
            # Ante cualquier caída de internet o de los servidores de MP, el plan de respaldo de WhatsApp se activa solo
            return redirect(url_whatsapp_respaldo)
        
    return render(request, 'checkout.html')
