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
- Se recomienda utilizar **OAuth2 con Django REST Framework** para gestionar la autenticación y los permisos correctamente.

#===================================================================================================================================================


## Autenticación y Token en la API

### 📌 Obtener datos del usuario autenticado
- **Método:** `GET`
- **URL:** `/api/usuario/`
- **Autenticación:** Requiere token OAuth2 en la cabecera `Authorization: Bearer <TOKEN>`

**Ejemplo de petición con `curl`:**
```bash
curl -X GET http://127.0.0.1:8000/template-api/usuario/ -H "Authorization: Bearer TU_ACCESS_TOKEN"


===================================================================================================================================================


Ejemplo con un usuario kazan de ambos get.

curl -X GET http://127.0.0.1:8000/template-api/usuario/ -H "Authorization: Bearer CWSWUHQBXTK7w3CNl5CFkg0SVTUAgn"

https://imgur.com/a/13wIkBP


curl -X GET http://127.0.0.1:8000/template-api/procesadores/usuario/ -H "Authorization: Bearer CWSWUHQBXTK7w3CNl5CFkg0SVTUAgn"
https://imgur.com/a/uIsH3Ff


