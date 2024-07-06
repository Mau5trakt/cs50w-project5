# WEB50XNI FINAL PROJECT: ROLALOG
## By: Enrique Mauricio Alemany Torres


## Descripción

**Rolalog** es un sitio web que permite a los usuarios registrar y compartir la música que escuchan en Spotify. Además, ofrece la posibilidad de intercambiar música entre usuarios y generar un reporte semanal de la actividad musical. A continuación, se detallan las funcionalidades principales de la aplicación.

### Usuario
- Registro con nombre de usuario único, correo asociado a Spotify y contraseña.
- Inicio de sesión con nombre de usuario y redirección a la página principal (perfil).
- Envío y recepción de solicitudes de escucha.
- Historial de solicitudes de escucha.
- Notificaciones de acciones en el sitio.
- Visualización de reportes semanales.

### Perfil
- Resumen de Rolls (canciones escuchadas), artistas y canciones.
- Últimos Rolls y descripción del usuario.

### Biblioteca (Álbum/Artista/Canción)
- Resumen del tipo de elemento (Rolls, artistas, álbumes, canciones).
- Ranking de artistas/álbumes/canciones según la actividad del usuario.

### Intercambio de música
- Página de solicitudes de escucha pendientes.
- Historial de solicitudes entrantes y salientes.
- Posibilidad de dar like a canciones en solicitudes de escucha.

### Notificaciones
- Notificaciones por cada acción realizada en el sitio.
- Generación de un reporte semanal de escucha.

### Reporte semanal
- Contiene datos como cantidad de Rolls, canciones, álbumes y artistas escuchados, junto con porcentajes de comparación con la semana anterior.

## Distinción y Complejidad

**Rolalog** destaca por su integración profunda con Spotify y la amplia variedad de funcionalidades que ofrece para la gestión y visualización de la actividad musical de los usuarios. La complejidad del proyecto se manifiesta en varias áreas clave:

1. **Integración con Spotify:** La aplicación utiliza la API de Spotify para obtener datos precisos y actualizados sobre la música que escuchan los usuarios, lo que requiere una gestión cuidadosa de autenticación y permisos.

2. **Interacción Social:** Rolalog permite el intercambio de música entre usuarios, lo que incluye funcionalidades complejas como el envío y aceptación de solicitudes de escucha, el historial de solicitudes y la posibilidad de dar like a canciones específicas dentro de una solicitud.

3. **Notificaciones y Reportes:** La generación de notificaciones en tiempo real y reportes semanales detallados añade un nivel adicional de complejidad, ya que requiere procesamiento de datos en segundo plano y la presentación de información de manera clara y útil para los usuarios.

4. **Experiencia de Usuario Personalizada:** Cada usuario tiene un perfil personalizado con un resumen de su actividad musical, descripciones personales y la capacidad de gestionar sus canciones favoritas, lo cual implica un diseño de base de datos robusto y una interfaz de usuario intuitiva.

5. **Funcionalidades especificas:** Al ser una aplicación que requiere llevar un registro en tiempo real de la musica escuchada por los usuarios se necesitan hacer tareas periódicas las cuales pueden ser manejadas de forma asíncrona por celery usando redis como gestor

## Contenido de los Archivos

- **`app.py`:** Archivo principal que contiene la lógica del servidor y los puntos de entrada de la aplicación.
- **`models.py`:** Define los modelos de datos utilizados en la aplicación, incluyendo usuarios, canciones, álbumes, artistas y solicitudes de escucha.
- **`views.py`:** Contiene las vistas que manejan las solicitudes HTTP y renderizan las páginas HTML.
- **`templates/`:** Directorio que contiene las plantillas HTML para las diferentes páginas de la aplicación.
- **`static/`:** Directorio que contiene los archivos estáticos como CSS, JavaScript e imágenes.
- **`celerycommands`:** Comandos para activar el worker de celery y el scheduler de las tareas
- **`.env_templates`:** plantilla del archivo .env con las variables de entorno requeridas para correr la aplicación



## Cómo Ejecutar la Aplicación

1. **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu_usuario/rolalog.git
    cd rolalog
    ```

2. **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar las variables de entorno:**
    Crear un archivo `.env` con las variables definidas en el archivo `.env_templates`:
    ```bash
    client_id=
    client_secret=
    db_username=
    db_password=
    db_host=
    cloudinary_cloud_name=
    cloudinary_api_key=
    cloudinary_api_secret=
   ```

4. **Configuración de la base de datos**
    Por defecto, el proyecto tiene la configuración para ser utilizado con Postgres, en caso de querer utilizar sqlite hay que poner la confiduración por defecto de django
   

5. **Realizar las migraciones de la base de datos:**
    ```bash
    python manage.py migrate
    ```

6. **Proceso de ejecución:**
    Si se desea usar celery para manejar las tareas de registrar la musica y hacer el reporte se debe tener celery instalado o via una imagen de docker 
    y ejecutar los siguientes comandos
    ```bash
    celery -A Rolalog worker -l INFO -P eventlet
    celery -A Rolalog worker -l INFO -P eventlet
    ```
    También se puede llevar registro de lo antes mencionado ejecutando los siguientes archivos dentro de la carpeta music
    ```bash
    python currentsong.py
    python report.py
    ```
    Luego ejecutar la aplicacion
    ```bash
    python manage.py runserver
    ```
   

6. **Acceder a la aplicación:**
    Abrir un navegador y visitar `http://127.0.0.1:8000`.

## Información Adicional

- **Autenticación con Spotify:** La aplicación requiere que los usuarios se autentiquen con sus cuentas de Spotify para poder registrar y analizar la música que escuchan.
- **Gestión de solicitudes:** Las solicitudes de escucha permiten a los usuarios compartir su música con otros y recibir comentarios.
- **Reporte semanal:** Cada viernes, la aplicación genera un reporte detallado de la actividad musical de cada usuario, facilitando un análisis de su comportamiento musical.

