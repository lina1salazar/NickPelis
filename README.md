# 🎬 Nick Pelis API

Proyecto en **Flask** para la gestión de películas, actores y géneros.  
Incluye endpoints REST con **validación (Marshmallow)**, **ORM con SQLAlchemy**, carga inicial de datos (`seed.py`) y soporte para imágenes (poster/banner).



## 📥 Descarga del proyecto

1. Ir al link de release en GitHub:  
   👉 [Descargar ZIP](https://github.com/lina1salazar/NickPelis/releases)  
   (elige el archivo `nick_pelis.zip`)

2. Extraer el contenido en una carpeta de tu computadora, por ejemplo:  
    ```
    C:\nick_pelis
    ````


## 🐍 Instalar Python

El proyecto usa **Python 3.13**.  

1. Descargar desde la página oficial:  
👉 [https://www.python.org/downloads/release/python-3137/](https://www.python.org/downloads/release/python-3137/)

2. Durante la instalación:  
    - Marca la opción ✅ **“Add Python to PATH”**  
    - Instala normalmente.

3. Verificar instalación:  
    ```bash
    python --version
    ````

    Debería mostrar:

    ```
    Python 3.13.x
    ```



## 🛢️ Instalar MySQL

El proyecto usa **MySQL 8+**.

1. Descargar e instalar desde:
   👉 [https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)

2. Crear la base de datos (puede ser desde Workbench o terminal):

   ```sql
   CREATE DATABASE nick_pelis CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
   ```


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

5. Configurar variables de entorno:
   Copiar el archivo `.env.example` y renombrarlo a `.env`:
   ```bash
   cp .env.example .env
   ```

   ```
   DB_USER=root
   DB_PASSWORD=
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=nick_pelis
   ```

   > Ajusta `DB_USER` y `DB_PASSWORD` según tu instalación de MySQL.


## ▶️ Ejecutar el proyecto

En la terminal, dentro de la carpeta del proyecto:

```bash
python app.py
```

Esto hará:

* Crear las tablas (`db.create_all()`).
* Insertar los datos iniciales (`llenar_datos_iniciales()`).
* Levantar el servidor Flask.

La API estará disponible en:

👉 [http://localhost:5000/api](http://localhost:5000/api)



## 📌 Endpoints

### Películas

* `GET /api/peliculas` → lista todas
* `GET /api/peliculas?destacadas` → solo destacadas
* `GET /api/peliculas?q=texto` → búsqueda por nombre
* `GET /api/peliculas?anio=1994` → filtro por año
* `GET /api/peliculas?genero=Drama` → filtro por género (nombre o id)
* `GET /api/peliculas/<id>` → ver pelicula
* `POST /api/peliculas` → crear (con `poster` y `banner` en form-data)
* `PUT /api/peliculas/<id>` → actualizar
* `DELETE /api/peliculas/<id>` → eliminar

### Géneros

* `GET /api/generos`
* `POST /api/generos`
* `GET /api/generos/<id>`
* `PUT /api/generos/<id>`
* `DELETE /api/generos/<id>`

### Actores

* `GET /api/actores`
* `POST /api/actores`
* `GET /api/actores/<id>`
* `PUT /api/actores/<id>`
* `DELETE /api/actores/<id>`


## 🧪 Probar con Postman

El proyecto incluye una colección lista para importar en Postman:

```
NickPelis.postman_collection.json
```

Con ella puede probar fácilmente todos los endpoints.

---

## 📦 Imágenes

El ZIP incluye la carpeta `static/img/` con:

* `posters/default.jpg`
* `banners/default.jpg`
* Algunos ejemplos de posters y banners (basados en el slug de cada película).

En caso de que falte una imagen, la API devolverá automáticamente la `default.jpg`.

---

## 👨‍🏫 Nota para el profesor

Este proyecto está listo para ejecutarse con los pasos descritos.
Al abrir en `http://localhost:5000/api/peliculas` podrá ver la lista de películas iniciales cargadas automáticamente.
