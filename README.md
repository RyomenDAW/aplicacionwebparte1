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






