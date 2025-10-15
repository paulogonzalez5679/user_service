
# 📌 CRUD de Usuarios con FastAPI y MongoDB

Proyecto técnico para la gestión de usuarios (CRUD) usando FastAPI y MongoDB. Permite crear, consultar, actualizar y eliminar usuarios de forma segura y eficiente.

---

## 🧰 Requisitos previos

- Python 3.10+
- MongoDB en ejecución local o remota
- Entorno virtual (recomendado)
- Instalar dependencias:
	```sh
	pip install -r requirements.txt
	```

---

## 🏗️ Creación de la base de datos y colección

Puedes crear la base de datos y la colección `users` de dos formas:

### 1. Manualmente en MongoDB

```mongodb
use <NOMBRE_DE_TU_BD>
db.createCollection('users')
db.users.createIndex({ email: 1 }, { unique: true })
```

### 2. Usando el script de inicialización

```sh
python config/database.py
```

---

## 🚀 Comando para levantar el proyecto en local

Activa tu entorno virtual y ejecuta:

```sh
uvicorn main:app --reload
# O si tu archivo principal está en una subcarpeta:
uvicorn user_service.main:app --reload
```

---

## 📥 Ejemplo JSON para crear usuario

```json
{
	"name": "Juan Pérez",
	"email": "juan.perez@email.com",
	"password": "MiClaveSegura123"
}
```

---

## 🧪 Prueba con curl

```sh
curl -X POST "http://localhost:8000/users/" \
	-H "Content-Type: application/json" \
	-d '{
		"name": "Juan Pérez",
		"email": "juan.perez@email.com",
		"password": "MiClaveSegura123"
	}'
```

---

## 📬 Prueba con Postman

1. Selecciona método **POST** y URL: `http://localhost:8000/users/`
2. En **Body**, selecciona `raw` y `JSON`.
3. Pega el JSON de ejemplo y envía la petición.

---

## 🧭 Documentación interactiva (Swagger UI)

Accede a la documentación y prueba los endpoints en:

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛡️ Notas y advertencias

- El campo **email** es único para cada usuario. Si intentas registrar un email ya existente, la API devolverá un error.
- Recuerda configurar correctamente las variables de entorno en tu archivo `.env`.
- Para producción, revisa la seguridad y configuración de CORS.