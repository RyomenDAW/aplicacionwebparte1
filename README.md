# Documentación de Permisos en la API

## **Roles de Usuario y Permisos**

La API define distintos roles de usuario, cada uno con permisos específicos para realizar operaciones dentro del sistema. A continuación, se detallan los roles y las acciones que pueden realizar:

| **Rol**                 | **Número** | **Permisos** |
|--------------------------|------------|--------------|
| **Administrador**       | 1          | Puede crear, buscar (avanzado), editar y eliminar elementos del CRUD. Tiene acceso total a todas las operaciones de la API. |
| **Cliente**            | 2          | Puede ver las listas de elementos, pero no puede realizar ninguna acción en el CRUD. |
| **Técnico Informático** | 3          | Puede editar y realizar búsquedas avanzadas en el CRUD. No puede crear ni eliminar elementos. |
| **Vendedor**           | 4          | Puede crear y eliminar elementos del CRUD, pero no puede editarlos ni realizar búsquedas avanzadas. |

---

## **Asignación de Permisos en la API**

### 📌 **Procesadores**
- **Crear un procesador** (`POST /template-api/procesadores/`): Solo Administrador (1) y Vendedor (4).
- **Obtener lista de procesadores** (`GET /template-api/procesadores/`): Disponible para cualquier usuario autenticado.
- **Actualizar un procesador** (`PUT /template-api/procesadores/{id}/`): Solo Administrador (1) y Técnico Informático (3).
- **Actualizar solo el nombre de un procesador** (`PATCH /template-api/procesadores/{id}/`): Solo Administrador (1) y Técnico Informático (3).
- **Eliminar un procesador** (`DELETE /template-api/procesadores/{id}/`): Solo Administrador (1) y Vendedor (4).

### 📌 **Gráficas**
- **Crear una gráfica** (`POST /template-api/graficas/`): Solo Administrador (1) y Vendedor (4).
- **Obtener lista de gráficas** (`GET /template-api/graficas/`): Disponible para cualquier usuario autenticado.
- **Actualizar una gráfica** (`PUT /template-api/graficas/{id}/`): Solo Administrador (1) y Técnico Informático (3).
- **Actualizar solo el nombre de una gráfica** (`PATCH /template-api/graficas/{id}/`): Solo Administrador (1) y Técnico Informático (3).
- **Eliminar una gráfica** (`DELETE /template-api/graficas/{id}/`): Solo Administrador (1) y Vendedor (4).

### 📌 **Monitores y Relación con Gráficas**
- **Crear relación Monitor-Gráfica** (`POST /template-api/monitor-grafica/`): Solo Administrador (1) y Vendedor (4).
- **Obtener lista de relaciones Monitor-Gráfica** (`GET /template-api/monitor-grafica/`): Disponible para cualquier usuario autenticado.
- **Actualizar relación Monitor-Gráfica** (`PUT /template-api/monitor-grafica/{id}/`): Solo Administrador (1) y Técnico Informático (3).
- **Actualizar solo la gráfica en una relación** (`PATCH /template-api/monitor-grafica/{id}/`): Solo Administrador (1) y Técnico Informático (3).
- **Eliminar relación Monitor-Gráfica** (`DELETE /template-api/monitor-grafica/{id}/`): Solo Administrador (1) y Vendedor (4).

### 📌 **Fuentes de Alimentación, RAMs y Placas Base**
- **Listar elementos** (`GET /template-api/fuentes/`, `GET /template-api/rams/`, `GET /template-api/placasbase/`): Disponible para cualquier usuario autenticado.
- **Búsqueda avanzada** (`GET /template-api/procesadores/busqueda-avanzada/`): Solo Administrador (1) y Técnico Informático (3).

---

## **Autenticación y Seguridad**
- Todas las operaciones requieren autenticación mediante **OAuth2**.
- Se usa `IsAuthenticated` en cada vista protegida para restringir el acceso.
- Cada usuario autenticado tiene un **token** que se debe enviar en los headers de las peticiones (`Authorization: Bearer <TOKEN>`).

Ejemplo de solicitud autenticada con cURL:
```sh
curl -X GET http://127.0.0.1:8000/template-api/procesadores/ \
     -H "Authorization: Bearer <TOKEN_DEL_USUARIO>"
```

---

## **Notas Finales**
- Los permisos están definidos en el backend y validados en cada endpoint.
- Los usuarios solo pueden realizar acciones que correspondan a su rol dentro del sistema.
- Utilizamos **OAuth2 con Django REST Framework** para gestionar la autenticación y los permisos correctamente.

#===================================================================================================================================================
Hacer dos peticiones GET donde se tenga en cuenta el usuario logueado y que usa el token (1 punto)

Vistas:

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_usuario_autenticado(request):
    """ Devuelve la información del usuario autenticado """
    usuario = request.user
    return Response({
        "id": usuario.id,
        "username": usuario.username,
        "email": usuario.email,
        "rol": ROLES.get(usuario.rol, "Desconocido"),  # Convertir número de rol a nombre de rol
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_procesadores_usuario(request):
    """ Devuelve solo los procesadores creados por el usuario autenticado """
    procesadores = Procesador.objects.filter(user=request.user)  # Filtrar por usuario autenticado
    serializer = ProcesadorSerializer(procesadores, many=True)
    return Response(serializer.data)


===================================================================================================================================================


Ejemplo con un usuario kazan de ambos get.

curl -X GET http://127.0.0.1:8000/template-api/usuario/ -H "Authorization: Bearer CWSWUHQBXTK7w3CNl5CFkg0SVTUAgn"

https://imgur.com/a/13wIkBP


curl -X GET http://127.0.0.1:8000/template-api/procesadores/usuario/ -H "Authorization: Bearer CWSWUHQBXTK7w3CNl5CFkg0SVTUAgn"
https://imgur.com/a/uIsH3Ff

Ese token creo que puede ser valido para cuando lo corrijas, si no, genera otro.


===================================================================================================================================================

Hacer dos peticiones POST donde se tenga en cuenta el usuario logueado y que usa el token, y no tengas que indicarlo en el formulario cliente (1 punto)

Vistas de ejemplo:

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_grafica(request):
    """ API para crear una nueva gráfica """

    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para crear gráficas."}, status=status.HTTP_403_FORBIDDEN)

    print("📌 RECIBIDA PETICIÓN POST EN /template-api/graficas/")  # DEBUG
    print("📌 DATOS RECIBIDOS:", request.data)  # DEBUG

    grafica_serializer = CrearGraficaSerializer(data=request.data, context={'request': request})

    if grafica_serializer.is_valid():
        try:
            grafica_serializer.save(user=request.user)
            return Response({"mensaje": "GRÁFICA CREADA CON ÉXITO"}, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(grafica_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

===================================================================================================================================================

# 🔹 Crear un procesador (Solo Vendedor y Administrador)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_procesador(request):
    if request.user.rol not in [1, 4]:  # Solo Administrador (1) y Vendedor (4)
        return Response({"error": "No tienes permisos para crear procesadores."}, status=status.HTTP_403_FORBIDDEN)

    print("📌 RECIBIDA PETICIÓN POST EN /template-api/procesadores/")  # DEBUG
    print("📌 DATOS RECIBIDOS:", request.data)  # DEBUG

    procesador_serializer = CrearProcesadorSerializer(data=request.data, context={'request': request})  

    if procesador_serializer.is_valid():
        try:
            procesador_serializer.save()
            return Response({"mensaje": "PROCESADOR CREADO CON ÉXITO"}, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(procesador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


===================================================================================================================================================


Entonces, utilizariamos estas 2 peticiones:

curl -X POST http://127.0.0.1:8000/template-api/graficas/ \
    -H "Authorization: Bearer CWSWUHQBXTK7w3CNl5CFkg0SVTUAgn" \
    -H "Content-Type: application/json" \
    -d '{
        "urlcompra": "https://www.nvidia.com/rtx4090",
        "nombre": "NVIDIA RTX 4090",
        "familiagrafica": "Nvidia",
        "potenciacalculo": 20000,
        "memoriavram": 2004,
        "trazadorayos": true
    }'

https://imgur.com/a/B9fCKp3
Guia para crear bien una grafica:

Explicación para la creación de una gráfica

Authorization: Bearer ... → Se envía el token del usuario autenticado en la cabecera. Solo los usuarios con rol Administrador (1) o Vendedor (4) pueden crear una gráfica.
urlcompra → Es obligatorio en el modelo, así que se debe incluir un enlace válido donde se pueda comprar la tarjeta gráfica, pccomponentes suele ser la comun.
nombre → Es el nombre de la tarjeta gráfica, por ejemplo, "NVIDIA RTX 4090".
familiagrafica → Debe ser una opción válida según mi modelo (Nvidia o AMD, según FAMILIA_GRAFICA).
potenciacalculo → Es un valor numérico positivo que indica la potencia de la tarjeta gráfica.
memoriavram → Especifica la cantidad de memoria VRAM en MB (ejemplo: 2004 MB para una RTX 4090), no hace falta que pongas MB, de hecho es number este field vaya.
trazadorayos → Debe ser true o false, indicando si la tarjeta gráfica soporta Ray Tracing (RTX)

Y luego, esta otra



curl -X POST http://127.0.0.1:8000/template-api/procesadores/ \
-H "Authorization: Bearer CWSWUHQBXTK7w3CNl5CFkg0SVTUAgn" \
-H "Content-Type: application/json" \
-d '{
"urlcompra": "https://www.intel.com/corei9",
"nombre": "Intel Core i9-14900K",
"familiaprocesador": "Intel",
"potenciacalculo": 25000,
"nucleos": 16000,
"hilos": 35000
}'

https://imgur.com/a/YEPh7qk


Guia para crear bien un procesador:

 Explicación
Authorization: Bearer ... → Se envía el token del usuario autenticado en la cabecera.
urlcompra → Es obligatorio en el modelo, así que le agregamos un enlace.
nombre → Nombre del procesador.
familiaprocesador → Una de las opciones válidas (Intel o AMD, según mi modelo FAMILIA_PROCESADOR).
potenciacalculo → Un valor numérico positivo.
nucleos → Un número positivo que representa la cantidad de núcleos, no debe ser menor que hilos.
hilos → Un número mayor o igual a 35000, como lo exige mi MinValueValidator.



Efectivamente copia los datos si quieres, pero, el nombre debes de cambiarlo aunque sea, no crees duplicados.

Modifica tokens si no te funcionan, kazan es administrador, si no, prueba con un token de vendedor si quieres tambien.

VENDEDOR:

Rammstein                   (Escribelo bien)
hakari123

TECNICOINFORMATICO:

Banana
hakari123

Si lo intentamos con Banana, que es TecnicoInformatico, da error como debe ser 

victortxakon@daw:~$ curl -X POST http://127.0.0.1:8000/template-api/procesadores/ -H "Authorization: Bearer jy2v1dV6rjfclZGGR3aH8ockjZcBCV" -H "Content-Type: application/json" -d '{
"urlcompra": "https://www.intel.com/corei9",
"nombre": "Intel Core i13-14900K",
"familiaprocesador": "Intel",
"potenciacalculo": 25000,
"nucleos": 16000,
"hilos": 35000
}'
{"error":"No tienes permisos para crear procesadores."}victortxakon@daw:~$ 



===================================================================================================================================================


Tutorial:

# 📌 Tutorial de Uso de la Aplicación

Este tutorial está diseñado para que cualquier persona pueda desplegar y utilizar la aplicación de manera efectiva. Explicamos los pasos para desplegar la aplicación y realizar operaciones fundamentales como GET, POST, PUT, DELETE y PATCH.

---

## 🔹 **Requisitos Previos**
Antes de comenzar, asegúrate de contar con los siguientes requisitos:

- **Python 3.x**: Necesario para ejecutar el servidor.
- **Django**: Framework utilizado para el backend.
- **Requests**: Para hacer solicitudes HTTP al backend.
- **Token de acceso válido**: Necesario para autenticar las operaciones. Se obtiene al iniciar sesión en la aplicación.

---

## 🖥️ **1. Desplegar la Aplicación**
Sigue estos pasos para ejecutar el servidor Django:

1️⃣ **Clona el repositorio** en tu máquina local:
```sh
git clone <URL_DE_TU_REPOSITORIO>
```

2️⃣ **Navega a la carpeta del proyecto:**
```sh
cd <nombre_del_proyecto>
```

3️⃣ **Crea un entorno virtual e instálalo:**
```sh
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

4️⃣ **Instala las dependencias necesarias:**
```sh
pip install -r requirements.txt
```

5️⃣ **Realiza las migraciones de la base de datos:**
```sh
python manage.py migrate
```

6️⃣ **Inicia el servidor de desarrollo Django:**
```sh
python manage.py runserver
```

La aplicación estará corriendo en `http://127.0.0.1:8000/`.

---

## 🔑 **2. Autenticación**
Para realizar cualquier operación en la API, primero debes obtener un token de autenticación.

1️⃣ **Realiza un POST a la URL de inicio de sesión para obtener el token.**

- **Endpoint:** `POST http://127.0.0.1:8000/template-api/login/`
- **Cuerpo (Body):**
```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```
- **Respuesta:**
```json
{
  "token": "aqui_va_tu_token"
}
```

Guarda este token, lo necesitarás en las siguientes peticiones.

---

## 📌 **3. Operaciones CRUD con la API**

### 🟢 **3.1. Obtener datos (GET)**
El método **GET** se usa para recuperar información de la API.

- **Ejemplo: Obtener lista de procesadores**
```sh
curl -X GET http://127.0.0.1:8000/template-api/procesadores/ \
     -H "Authorization: Token tu_token"
```
- **Respuesta esperada:**
```json
[
  {
    "id_procesador": 1,
    "nombre": "Intel i9-13900K",
    "nucleos": 24,
    "hilos": 32
  }
]
```

---

### 🟠 **3.2. Crear un nuevo recurso (POST)**
El método **POST** se usa para agregar un nuevo registro en la API.

- **Ejemplo: Crear un nuevo procesador**
```sh
curl -X POST http://127.0.0.1:8000/template-api/procesadores/ \
     -H "Authorization: Token tu_token" \
     -H "Content-Type: application/json" \
     -d '{
         "nombre": "AMD Ryzen 9 7950X",
         "nucleos": 16,
         "hilos": 32,
         "potenciacalculo": 5.6
     }'
```
- **Respuesta esperada:**
```json
{
  "mensaje": "PROCESADOR CREADO CON ÉXITO"
}
```

---

### 🔵 **3.3. Actualizar un recurso completamente (PUT)**
El método **PUT** se usa para reemplazar completamente un recurso existente.

- **Ejemplo: Actualizar un procesador**
```sh
curl -X PUT http://127.0.0.1:8000/template-api/procesadores/1/ \
     -H "Authorization: Token tu_token" \
     -H "Content-Type: application/json" \
     -d '{
         "nombre": "Intel i9-14900K",
         "nucleos": 24,
         "hilos": 32,
         "potenciacalculo": 5.8
     }'
```
- **Respuesta esperada:**
```json
{
  "mensaje": "Procesador actualizado correctamente"
}
```

---

### 🔴 **3.4. Eliminar un recurso (DELETE)**
El método **DELETE** se usa para borrar un recurso existente.

- **Ejemplo: Eliminar un procesador**
```sh
curl -X DELETE http://127.0.0.1:8000/template-api/procesadores/1/ \
     -H "Authorization: Token tu_token"
```
- **Respuesta esperada:**
```json
{
  "mensaje": "✅ Procesador eliminado correctamente."
}
```

---

### 🟣 **3.5. Actualizar parcialmente un recurso (PATCH)**
El método **PATCH** se usa para actualizar solo ciertos campos de un recurso.

- **Ejemplo: Actualizar solo el nombre de un procesador**
```sh
curl -X PATCH http://127.0.0.1:8000/template-api/procesadores/1/ \
     -H "Authorization: Token tu_token" \
     -H "Content-Type: application/json" \
     -d '{
         "nombre": "Intel i9-14900KS"
     }'
```
- **Respuesta esperada:**
```json
{
  "mensaje": "Nombre actualizado correctamente"
}
```

---

##  **Conclusión**
Siguiendo este tutorial, ahora puedes desplegar la aplicación y realizar operaciones CRUD (GET, POST, PUT, DELETE, PATCH) de manera sencilla utilizando la API REST.

Si tienes alguna duda o encuentras un error, revisa la consola del servidor Django (`python manage.py runserver`) para ver posibles mensajes de depuración. 

---


#====================================================================================================================================================================


DOCKERIZACION:

Dockerizacion de la Aplicacion
Este documento explica cómo desplegar la aplicación API REST y el Cliente utilizando Docker. Se incluyen los comandos necesarios para construir las imágenes, ejecutar los contenedores y gestionar el despliegue. Si no tienes experiencia previa con Docker, sigue los pasos en orden y no deberías tener muchos  problemas.

Requisitos previos
Antes de empezar, asegúrate de que tienes instalado lo siguiente:

Docker: Herramienta para contenedores.
Docker Compose: Permite orquestar varios contenedores, esta es mas importante incluso.
Además, necesitas clonar los repositorios del API REST y del Cliente en tu máquina local:

Repositorio API REST: https://github.com/RyomenDAW/aplicacionwebparte1
Repositorio Cliente: https://github.com/RyomenDAW/tiendaordenadores-clienteapi
Si aún no los tienes en tu máquina, usa estos comandos para clonarlos:

bash
Copy
Edit
git clone https://github.com/RyomenDAW/aplicacionwebparte1
git clone https://github.com/RyomenDAW/tiendaordenadores-clienteapi
Construcción de las imágenes Docker
Antes de poder ejecutar los contenedores, hay que construir las imágenes de Docker. Esto se hace desde las carpetas donde están los archivos Dockerfile de cada aplicación.

Construir la imagen de la API REST
bash
Copy
Edit
cd aplicacionwebparte1  # Moverse a la carpeta de la API
docker build -t api-tiendaordenadores .
Esto creará una imagen llamada api-tiendaordenadores con todo lo necesario para ejecutar la API.

Construir la imagen del Cliente
bash
Copy
Edit
cd tiendaordenadores-clienteapi  # Moverse a la carpeta del cliente
docker build -t cliente-tiendaordenadores .
Esto creará una imagen llamada cliente-tiendaordenadores con el cliente listo para ejecutarse.

Ejecutar la aplicación con Docker
Una vez creadas las imágenes, podemos iniciar los contenedores.

Ejecutar la API REST
bash
Copy
Edit
docker run -d -p 8000:8000 --name api-tienda api-tiendaordenadores
Este comando ejecuta la API en segundo plano (-d significa "detached"), la expone en el puerto 8000 y le asigna el nombre api-tienda.

Después de ejecutarlo, la API debería estar disponible en:
http://localhost:8000/

Ejecutar el Cliente
bash
Copy
Edit
docker run -d -p 8001:8001 --name cliente-tienda cliente-tiendaordenadores
Este comando ejecuta el cliente, lo expone en el puerto 8001 y le asigna el nombre cliente-tienda.

Después de ejecutarlo, el cliente debería estar disponible en:
http://localhost:8001/

Usar Docker Compose (Recomendado)
En lugar de ejecutar manualmente cada servicio, es más conveniente usar docker-compose. Para ello, asegúrate de tener un archivo docker-compose.yml en la raíz del proyecto con el siguiente contenido:

yaml
Copy
Edit
version: '3.8'

services:
  api:
    build: ./aplicacionwebparte1
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=True
    volumes:
      - ./aplicacionwebparte1:/app

  cliente:
    build: ./tiendaordenadores-clienteapi
    ports:
      - "8001:8001"
    depends_on:
      - api
    environment:
      - DEBUG=True
    volumes:
      - ./tiendaordenadores-clienteapi:/app

  db:
    image: postgres:latest
    environment:
      POSTGRES_DB: tiendaordenadores
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
    ports:
      - "5432:5432"
Este archivo define tres servicios:

api: Contiene la API REST y se ejecuta en el puerto 8000.
cliente: Contiene la aplicación cliente y se ejecuta en el puerto 8001.
db: Un contenedor de PostgreSQL para manejar la base de datos.
Levantar todos los servicios con un solo comando
bash
Copy
Edit
docker-compose up -d
Este comando creará y ejecutará todos los contenedores definidos en docker-compose.yml.
Si haces cambios en el código y necesitas reconstruir las imágenes:

bash
Copy
Edit
docker-compose up --build -d
Para ver los contenedores activos:

bash
Copy
Edit
docker ps
Para detener todos los contenedores:

bash
Copy
Edit
docker-compose down
Verificación y pruebas
Después de que los contenedores estén en ejecución, puedes hacer pruebas para asegurarte de que todo está funcionando.

Verificar la API REST:
Abre un navegador o usa curl para ver si la API responde correctamente:

bash
Copy
Edit
curl -X GET http://localhost:8000/template-api/procesadores/
Verificar el Cliente:
Abre en tu navegador:
http://localhost:8001/

Si todo está funcionando, deberías ver la interfaz del cliente y poder interactuar con la API.

Conclusión
Este proceso permite desplegar la API y el cliente de manera sencilla utilizando Docker. Con docker-compose, se puede levantar todo con un solo comando, lo que facilita la gestión del proyecto. Si alguna parte no funciona como esperas, revisa los logs con:

bash
Copy
Edit
docker logs api-tienda
docker logs cliente-tienda
Y si necesitas más detalles, revisa los contenedores en ejecución con:

bash
Copy
Edit
docker ps
Con esto, la aplicación esta completamente dockerizada y lista para ejecutarse en cualquier entorno, llevatela como quieras 