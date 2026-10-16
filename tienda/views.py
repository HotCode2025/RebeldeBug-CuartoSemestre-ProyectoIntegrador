from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
import mercadopago
import urllib.parse

# Token unificado 
sdk = mercadopago.SDK("APP_USR-3297171459987328-101611-ee33ac5e4ae7360be04f6b1161d1a8cb-3686889775")

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def checkout(request):
    if request.method == 'POST':
        # 1. Capturamos los datos del formulario de Malargüe
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        domicilio = request.POST.get('domicilio')
        entrecalles = request.POST.get('entrecalles')
        horario = request.POST.get('horario')
        
        # Tomamos el valor del carrito dinámico que envía el HTML
        total_carrito = request.POST.get('total_final_input', '0')
        
        try:
            precio_final = float(total_carrito)
        except ValueError:
            precio_final = 30000.00 # Respaldo por si falla la conversión
        
        # Guardamos en la sesión para el mensaje final de WhatsApp
        request.session['datos_pedido'] = {
            'nombre': nombre,
            'telefono': telefono,
            'domicilio': domicilio,
            'entrecalles': entrecalles,
            'horario': horario,
            'total': precio_final
        }
        
                # 2. Preferencia con el monto real y las URLs de retorno activas
        preference_data = {
            "items": [
                {
                    "title": "Pedido de Pastas a Colores",
                    "quantity": 1,
                    "unit_price": precio_final,
                    "currency_id": "ARS"
                }
            ],
            # 🛠️ AGREGAMOS ESTO DE VUELTA:
            "back_urls": {
                "success": "http://127.0.0",
                "failure": "http://127.0.0",
                "pending": "http://127.0.0"
            }
        }


        try:
            preference_response = sdk.preference().create(preference_data)
            status_code = preference_response["status"]
            preference = preference_response["response"]
            
            # Al darnos el alta, nos vamos directo a Mercado Pago
            if status_code == 201 and "init_point" in preference:
                return redirect(preference["init_point"])
            else:
                return HttpResponse(f"<h3>Error de Mercado Pago</h3><p>Status: {status_code}</p><p>Detalle: {preference}</p>")
                
        except Exception as e:
            return HttpResponse(f"<h3>Excepción técnica en backend</h3><p>{e}</p>")
        
    return render(request, 'checkout.html')

def pedido_exitoso(request):
    datos = request.session.get('datos_pedido', {})
    nombre = datos.get('nombre', 'Cliente')
    telefono = datos.get('telefono', '-')
    domicilio = datos.get('domicilio', '-')
    entrecalles = datos.get('entrecalles', '-')
    horario = datos.get('horario', '-')
    total = datos.get('total', '0')
    
    mensaje = f"Hola Pastas a Colores! Ya realicé mi pago de ${total}. Mi nombre es {nombre}. Solicito la entrega en {domicilio} (Entre calles: {entrecalles}) en el rango de la {horario}. Mi teléfono es: {telefono}."
    telefono_negocio = "5492604507091"
    
    mensaje_url = urllib.parse.quote(mensaje)
    url_whatsapp = f"https://whatsapp.com{telefono_negocio}&text={mensaje_url}"
    
    return render(request, 'exito.html', {'url_whatsapp': url_whatsapp})
