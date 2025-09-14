# 🎬 Nick Pelis API

Proyecto en **Flask** para la gestión de películas, actores, géneros y usuarios.
Incluye endpoints REST con **validación (Marshmallow)**, **ORM con SQLAlchemy**, autenticación con **JWT**, carga inicial de datos (`seed.py`) y soporte para imágenes (poster/banner).

---

## 📥 Descarga del proyecto

1. Ir al link de release en GitHub:
   👉 [Descargar ZIP](https://github.com/lina1salazar/NickPelis/releases)
   (elige el archivo `nick_pelis.zip`)

2. Extraer el contenido en una carpeta de tu computadora, por ejemplo:

   ```bash
   C:\nick_pelis
   ```

---

## 🐍 Instalar Python

El proyecto usa **Python 3.13**.

1. Descargar desde la página oficial:
   👉 [https://www.python.org/downloads/release/python-3137/](https://www.python.org/downloads/release/python-3137/)

2. Durante la instalación:

   * Marca la opción ✅ **“Add Python to PATH”**
   * Instala normalmente.

3. Verificar instalación:

   ```bash
   python --version
   ```

   Debería mostrar:

   ```
   Python 3.13.x
   ```

---

## 🛢️ Instalar MySQL

El proyecto usa **MySQL 8+**.

1. Descargar e instalar desde:
   👉 [https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)

2. Crear la base de datos:

   ```sql
   CREATE DATABASE nick_pelis CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
   ```

---

## ⚙️ Configuración del proyecto

1. Abrir una terminal en la carpeta donde se descomprimió el ZIP:

   ```bash
   cd C:\nick_pelis
   ```

2. Crear un entorno virtual:

   ```bash
   python -m venv venv
   ```

3. Activar el entorno virtual:

   * En Windows:

     ```bash
     venv\Scripts\activate
     ```
   * En Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

4. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Configurar variables de entorno (`.env`):

   ```ini
   DB_USER=root
   DB_PASSWORD=
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=nick_pelis

   JWT_SECRET_KEY=jwtsecret

   ADMIN_EMAIL=admin@nickpelis.com
   ADMIN_PASSWORD=Admin123*
   ```

   > Ajusta `DB_USER` y `DB_PASSWORD` según tu instalación de MySQL.

---

## ▶️ Ejecutar el proyecto

En la terminal:

```bash
python app.py
```

Esto hará:

* Crear las tablas (`db.create_all()`).
* Insertar los datos iniciales (`llenar_datos_iniciales()`).
* Crear un usuario administrador por defecto con las variables `ADMIN_EMAIL` y `ADMIN_PASSWORD`.
* Levantar el servidor Flask.

La API estará disponible en:
👉 [http://localhost:5000/api](http://localhost:5000/api)

---

## 🔑 Autenticación y roles

El sistema usa **JWT (JSON Web Tokens)**.

* **Registro de usuario normal:**

  ```
  POST /auth/registro
  {
    "nombre": "Carlos",
    "correo": "carlos@mail.com",
    "contrasena": "Clave123*"
  }
  ```

  → Crea siempre un usuario con rol `USUARIO`.

* **Inicio de sesión:**

  ```
  POST /auth/iniciar_sesion
  {
    "correo": "admin@nickpelis.com",
    "contrasena": "Admin123*"
  }
  ```

  → Devuelve `access_token` y `refresh_token`.

* **Refrescar token:**

  ```
  POST /auth/refrescar
  ```

* **Cerrar sesión:**

  ```
  POST /auth/logout
  ```

### Roles

* `USUARIO` → puede comentar películas y actualizar su perfil.
* `ADMIN` → puede crear, editar y eliminar películas, géneros, actores y usuarios.

---

## 📌 Endpoints principales

### 🎞️ Películas

* `GET /api/peliculas`
* `GET /api/peliculas/<id>`
* `POST /api/peliculas` (**solo admin**)
* `PUT /api/peliculas/<id>` (**solo admin**)
* `DELETE /api/peliculas/<id>` (**solo admin**)

### 📝 Comentarios

* `GET /api/peliculas/<id>/comentarios` → listar comentarios de una película
* `POST /api/peliculas/<id>/comentarios` (**solo usuarios autenticados**)

### 🎭 Géneros

* `GET /api/generos` (**solo admin**)
* `POST /api/generos` (**solo admin**)
* `PUT /api/generos/<id>` (**solo admin**)
* `DELETE /api/generos/<id>` (**solo admin**)

### 👤 Actores

* `GET /api/actores` (**solo admin**)
* `POST /api/actores` (**solo admin**)
* `PUT /api/actores/<id>` (**solo admin**)
* `DELETE /api/actores/<id>` (**solo admin**)

### 👥 Usuarios

* `GET /api/usuarios` (**solo admin**) → listar todos
* `POST /api/usuarios` (**solo admin**) → crear usuario (admin o normal)
* `GET /api/usuarios/<id>` (**solo admin**)
* `PUT /api/usuarios/<id>` (**solo admin, con validación para no quitarse su propio rol admin**)
* `DELETE /api/usuarios/<id>` (**solo admin**)
* `GET /api/me` (**autenticado**) → ver perfil propio
* `PUT /api/me` (**autenticado**) → actualizar perfil (no rol)

---

## 📦 Imágenes

El ZIP incluye la carpeta `static/img/` con:

* `posters/default.jpg`
* `banners/default.jpg`

Si falta una imagen de película, la API devuelve automáticamente la `default.jpg`.

---

## 🧪 Probar con Postman

El proyecto incluye una colección lista para importar en Postman:

```
NickPelis.postman_collection.json
```

Con ella puedes probar fácilmente todos los endpoints.

---

## 👑 Usuario administrador inicial

Cuando corres `seed.py` o `app.py` por primera vez, se crea un usuario administrador con:

* **Correo:** `ADMIN_EMAIL` (por defecto `admin@nickpelis.com`)
* **Contraseña:** `ADMIN_PASSWORD` (por defecto `Admin123*`)

Puedes cambiar estas credenciales en el archivo `.env`.

