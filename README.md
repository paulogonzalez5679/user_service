# CRUD de Usuarios - FastAPI + MongoDB

Una API REST completa para gestión de usuarios desarrollada con FastAPI y MongoDB.

## 🚀 Características

- **CRUD completo** para usuarios (Crear, Leer, Actualizar, Eliminar)
- **Autenticación segura** con bcrypt para hash de contraseñas
- **Validación de datos** con Pydantic
- **Base de datos MongoDB** con Motor (async driver)
- **Middleware de logging** con tiempo de respuesta
- **Documentación automática** con Swagger UI
- **Dockerizado** para fácil despliegue
- **Docker Compose** para desarrollo local

## 📋 Requisitos

- Python 3.11+
- MongoDB 6.0+
- Docker y Docker Compose (opcional)

## 🛠️ Instalación

### Opción 1: Instalación Local

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd CRUD-de-Usuarios-DigitalMind--FastAPI-MongoDB-
```

2. **Crear entorno virtual**
```bash
python -m venv fastAPI
source fastAPI/bin/activate  # En Windows: fastAPI\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

5. **Iniciar MongoDB** (si no tienes Docker)
```bash
# Instalar MongoDB localmente o usar Docker
docker run -d -p 27017:27017 --name mongo mongo:6.0
```

6. **Ejecutar la aplicación**
```bash
uvicorn main:app --reload
```

### Opción 2: Con Docker Compose

1. **Clonar y configurar**
```bash
git clone <repository-url>
cd CRUD-de-Usuarios-DigitalMind--FastAPI-MongoDB-
cp env.example .env
```

2. **Ejecutar con Docker Compose**
```bash
docker-compose up --build
```

## 📚 Uso de la API

### Documentación Interactiva

Una vez iniciada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Disponibles

#### Usuarios

- `POST /users/` - Crear usuario
- `GET /users/{user_id}` - Obtener usuario por ID
- `PUT /users/{user_id}` - Actualizar usuario
- `DELETE /users/{user_id}` - Eliminar usuario

### Ejemplos de Uso

#### Crear Usuario
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "mi_password_seguro"
  }'
```

#### Obtener Usuario
```bash
curl -X GET "http://localhost:8000/users/{user_id}"
```

#### Actualizar Usuario
```bash
curl -X PUT "http://localhost:8000/users/{user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Carlos Pérez",
    "email": "juan.carlos@example.com"
  }'
```

#### Eliminar Usuario
```bash
curl -X DELETE "http://localhost:8000/users/{user_id}"
```

## 🏗️ Estructura del Proyecto

```
├── main.py                 # Aplicación principal FastAPI
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Imagen Docker
├── docker-compose.yml     # Orquestación de servicios
├── env.example            # Variables de entorno de ejemplo
├── .gitignore            # Archivos ignorados por Git
├── config/
│   └── database.py       # Configuración de MongoDB
├── models/
│   └── user.py           # Modelos Pydantic
└── routes/
    └── user_routes.py    # Rutas de la API
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `MONGODB_URL` | URL de conexión a MongoDB | `mongodb://localhost:27017` |
| `MONGODB_DATABASE` | Nombre de la base de datos | `usuariosdb` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto del servidor | `8000` |
| `DEBUG` | Modo debug | `True` |

### Base de Datos

La aplicación se conecta automáticamente a MongoDB y crea las colecciones necesarias. Los índices se crean automáticamente para optimizar las consultas.

## 🐳 Docker

### Construir imagen
```bash
docker build -t user-service-api .
```

### Ejecutar contenedor
```bash
docker run -p 8000:8000 user-service-api
```

### Con Docker Compose
```bash
# Desarrollo
docker-compose up --build

# Producción
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Middleware de Logging

La aplicación incluye un middleware que registra:

- **Método HTTP** y **ruta**
- **Tiempo de respuesta** en milisegundos
- **Headers de respuesta** con tiempo de procesamiento

Ejemplo de log:
```
[POST] /users/ completed in 24.65ms
```

## 🔒 Seguridad

- **Hash de contraseñas** con bcrypt
- **Validación de entrada** con Pydantic
- **Validación de email** con EmailStr
- **Límite de 72 bytes** para contraseñas (bcrypt)
- **Sanitización automática** de datos

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con cobertura
pytest --cov=.
```

## 📈 Monitoreo

- **Logs estructurados** en consola
- **Métricas de rendimiento** en headers HTTP
- **Health checks** automáticos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Paulo González** - *Desarrollo inicial* - [@paulogonzalez](https://github.com/paulogonzalez)

## 🙏 Agradecimientos

- FastAPI por el framework web
- MongoDB por la base de datos
- Pydantic por la validación de datos
- Docker por la containerización