# 🍝 Pastas a Colores Malargüe

**Proyecto Integrador – Final de Semestre | Cohorte 2025**

Desarrollado por el equipo **Rebelde Bug**.

---

## 📌 Descripción del proyecto

Pastas a Colores Malargüe es una aplicación web desarrollada para un emprendimiento de pastas artesanales. Su objetivo es ofrecer a los clientes una plataforma sencilla e intuitiva donde puedan consultar el catálogo de productos, conocer sus precios y disponibilidad, armar un pedido y gestionar su compra.

El sistema incorpora un catálogo dinámico conectado a una base de datos, un carrito de compras, registro e inicio de sesión, integración con Mercado Pago en entorno de pruebas y confirmación logística mediante WhatsApp.

Además, cuenta con un panel de administración que permite al propietario gestionar los productos, actualizar precios y controlar el inventario sin necesidad de modificar el código fuente.

## 🎯 Objetivos

- Digitalizar la presentación y comercialización de pastas artesanales.
- Facilitar la consulta del catálogo y la realización de pedidos.
- Permitir una gestión autónoma de productos, precios y stock.
- Incorporar mecanismos de autenticación de clientes.
- Integrar una pasarela de pagos para probar el flujo de compra.
- Facilitar la comunicación entre el comercio y sus clientes mediante WhatsApp.

## 🛠️ Tecnologías utilizadas

| Tecnología | Utilización |
|---|---|
| Python | Lenguaje principal del backend. |
| Django 6.1.2 | Framework para el desarrollo de la aplicación web. |
| SQLite3 | Sistema de gestión de base de datos. |
| HTML5 | Estructura de las páginas. |
| CSS3 | Diseño y presentación visual. |
| JavaScript | Interactividad y funcionalidades del carrito. |
| Mercado Pago SDK | Integración de pagos en entorno Sandbox. |
| Pillow | Procesamiento y gestión de imágenes. |
| PythonAnywhere | Alojamiento de la aplicación mediante WSGI. |
| Git y GitHub | Control de versiones y colaboración. |

## ⚙️ Funcionalidades principales

### 1. Catálogo de productos

- Visualización dinámica de las pastas disponibles.
- Consulta de imágenes, descripciones y precios.
- Visualización de la disponibilidad de cada producto.
- Actualización de la información a partir de los registros almacenados en la base de datos.

### 2. Carrito de compras

- Selección de cantidades mediante controles para aumentar o disminuir unidades.
- Incorporación de productos al carrito.
- Visualización de los artículos seleccionados.
- Cálculo del subtotal en tiempo real.
- Acceso al carrito mediante el botón flotante «Mi Pedido».
- Inicio del proceso de compra desde el carrito.

### 3. Registro e inicio de sesión

El sistema utiliza una pantalla unificada para el registro de nuevos clientes y el acceso de usuarios existentes.

- Registro mediante número de teléfono y contraseña.
- El número telefónico funciona como identificador único del usuario.
- Solicitud de datos para la entrega: nombre, domicilio, entrecalles y horario.
- Inicio de sesión para clientes registrados.
- Ocultamiento de los campos de registro al seleccionar la opción de iniciar sesión.

### 4. Integración con Mercado Pago

El proyecto incorpora el SDK oficial de Mercado Pago para generar preferencias de pago desde el backend.

- Envío del importe total de la compra.
- Generación de una preferencia de pago.
- Redirección al entorno de pruebas de Mercado Pago.

**Importante:** la integración corresponde al entorno Sandbox. Está destinada a probar el flujo de pago y no representa una implementación de cobros reales en producción.

Debido a las limitaciones de redirección del entorno de pruebas, el retorno automático hacia la aplicación puede no comportarse como lo haría en un despliegue productivo. El procedimiento documentado contempla el acceso a la ruta `/pedido-exitoso/` para continuar con la confirmación del pedido.

### 5. Confirmación del pedido por WhatsApp

Una vez alcanzada la pantalla de confirmación:

- El backend recupera los datos del cliente almacenados en la sesión.
- Se prepara un comprobante digital con la información de la compra.
- Se genera un mensaje estructurado con los datos del pedido.
- El cliente puede continuar la comunicación con el comercio mediante WhatsApp.

### 6. Retorno a la página principal

Después de la acción de despacho logístico, un script interno espera dos segundos y redirige al usuario a la página principal (`/`), reiniciando los estados de navegación para facilitar una nueva compra.

### 7. Administración del inventario

El propietario puede administrar el catálogo desde el panel de Django Admin, disponible en la ruta `/admin/`.

Entre las operaciones disponibles se encuentran:

- Alta y modificación de productos.
- Actualización de precios.
- Modificación de descripciones e imágenes.
- Administración de categorías.
- Control de existencias.

**Control de stock:** cuando la cantidad disponible de un producto llega a cero, el sistema muestra el indicador «Agotado» en el catálogo y evita que se realicen nuevas compras de ese artículo.

## 🗄️ Base de datos

La aplicación utiliza SQLite3 mediante el sistema ORM de Django.

Entre los modelos principales del proyecto se encuentran:

- **Categoria:** almacena las categorías utilizadas para organizar los productos.
- **Producto:** almacena el nombre, descripción, precio, stock, imagen, categoría y disponibilidad de cada pasta.

El modelo Producto mantiene una relación con Categoria mediante una clave foránea (`ForeignKey`).

La configuración de la base de datos se encuentra en `core/settings.py`.

## 📂 Estructura general del proyecto

```text
RebeldeBug-CuartoSemestre-ProyectoIntegrador/
│
├── core/
│   ├── settings.py
│   └── urls.py
│
├── static/
│
├── templates/
│
├── tienda/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── datos_locales.json
├── ManualDeUsuario_RebeldeBug_PastasCaseras.pdf
└── README.md
```

*La estructura representa los directorios y archivos principales del proyecto.*

## 🚀 Instalación y ejecución local

### Requisitos previos

- Python instalado.
- Git.
- Un editor de código, como Visual Studio Code.

### 1. Clonar el repositorio

```bash
git clone https://github.com/HotCode2025/RebeldeBug-CuartoSemestre-ProyectoIntegrador.git
```

### 2. Ingresar al directorio

```bash
cd RebeldeBug-CuartoSemestre-ProyectoIntegrador
```

### 3. Crear un entorno virtual

En Windows:

```bash
python -m venv venv
```

### 4. Activar el entorno virtual

En PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Aplicar las migraciones

```bash
python manage.py migrate
```

### 7. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible localmente en:

```text
http://127.0.0.1:8000/
```

Para acceder al panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

## ☁️ Despliegue

La aplicación se encuentra alojada en **PythonAnywhere**, utilizando un servidor WSGI para atender las solicitudes web.

La implementación utiliza SQLite3 como motor de base de datos y permite acceder a la tienda mediante la URL pública del proyecto.

## 📖 Manual de usuario

Para consultar las instrucciones de uso de la tienda y la administración del inventario, se encuentra disponible el siguiente documento:

[**Manual de Usuario – Pastas a Colores Malargüe (PDF)**](ManualDeUsuario_RebeldeBug_PastasCaseras.pdf)

## 👩‍💻 Equipo de desarrollo

**Rebelde Bug – Cohorte 2025**

- Jimena Pérez
- Melina Gallo
- Micaela Aramayo
- Zoe Garnica

---

**Proyecto Integrador – Final de Semestre**

Desarrollo de una plataforma web para la gestión y comercialización de pastas artesanales.