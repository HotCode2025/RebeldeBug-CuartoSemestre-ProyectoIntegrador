from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Producto
import mercadopago
import urllib.parse

# Token unificado de Mercado Pago
sdk = mercadopago.SDK("APP_USR-3297171459987328-101611-ee33ac5e4ae7360be04f6b1161d1a8cb-3686889775")

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def checkout(request):
    if request.method == 'POST':
        # 1. Capturamos los datos de autenticación y envío desde el formulario
        telefono_usuario = request.POST.get('telefono_usuario')
        password = request.POST.get('password')
        
        nombre = request.POST.get('nombre')
        domicilio = request.POST.get('domicilio')
        entrecalles = request.POST.get('entrecalles')
        horario = request.POST.get('horario')
        
        # Evaluamos el comportamiento basándonos en si los campos de envío vienen llenos o no
        # Si 'nombre' es None o vacío, significa que el usuario tocó "Iniciar Sesión"
        es_login_puro = not nombre 

        if es_login_puro:
            # 🔐 FLUJO: EL CLIENTE YA TIENE CUENTA E INICIA SESIÓN
            user = authenticate(request, username=telefono_usuario, password=password)
            if user is not None:
                login(request, user)
                # Al loguearse con éxito, lo redirigimos de nuevo al checkout para que 
                # ahora vea los campos de entrega (o podés mandarlo directo a Mercado Pago si autocompletás)
                return redirect('/checkout/')
            else:
                return HttpResponse("<h3>Error de Autenticación</h3><p>El teléfono o la contraseña son incorrectos.</p><p><a href='/checkout/'>Volver a intentar</a></p>")
        
        else:
            # 📝 FLUJO: CLIENTE NUEVO (REGISTRO SILENCIOSO + COMPRA)
            # Verificamos si el usuario ya existe para evitar errores por duplicado
            if not User.objects.filter(username=telefono_usuario).exists():
                user = User.objects.create_user(username=telefono_usuario, password=password)
                # Opcional: guardamos su nombre real en el modelo de Django
                user.first_name = nombre
                user.save()
            
            # Logueamos automáticamente al nuevo usuario en la sesión del servidor
            user = authenticate(request, username=telefono_usuario, password=password)
            if user is not None:
                login(request, user)

        # 2. Tomamos el valor del carrito dinámico que envía el HTML
        total_carrito = request.POST.get('total_final_input', '0')
        try:
            precio_final = float(total_carrito)
        except ValueError:
            precio_final = 30000.00  # Respaldo por si falla la conversión
        
        # Guardamos la orden temporal en la sesión para la confirmación posterior por WhatsApp
        request.session['datos_pedido'] = {
            'nombre': nombre if nombre else request.user.first_name,
            'telefono': telefono_usuario,
            'domicilio': domicilio,
            'entrecalles': entrecalles,
            'horario': horario,
            'total': precio_final
        }
        
        # 3. Preferencia con las URLs de retorno activas hacia tu entorno local
        preference_data = {
            "items": [
                {
                    "title": "Pedido de Pastas a Colores",
                    "quantity": 1,
                    "unit_price": precio_final,
                    "currency_id": "ARS"
                }
            ],
                        "back_urls": {
                "success": "http://127.0.0",
                "failure": "http://127.0.0",
                "pending": "http://127.0.0"
            }, 
            "auto_return": "approved"

        }

        try:
            preference_response = sdk.preference().create(preference_data)
            status_code = preference_response["status"]
            preference = preference_response["response"]
            
            if status_code == 201 and "init_point" in preference:
                return redirect(preference["init_point"])
            else:
                return HttpResponse(f"<h3>Error de Mercado Pago</h3><p>Status: {status_code}</p>")
                
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
    
    mensaje = f"¡Hola Pastas a Colores! Ya realicé mi pago de ${total}. Mi nombre es {nombre}. Solicito la entrega en {domicilio} (Entre calles: {entrecalles}) en el rango de la {horario}. Mi teléfono es: {telefono}."
    telefono_negocio = "5492604507091"
    
    mensaje_url = urllib.parse.quote(mensaje)
    # 🛠️ CORRECCIÓN: Ajustamos la sintaxis oficial de la API de WhatsApp para el retorno post-pago
    url_whatsapp = f"https://whatsapp.com{telefono_negocio}&text={mensaje_url}"
    
    return render(request, 'exito.html', {'url_whatsapp': url_whatsapp})
