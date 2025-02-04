# 🚀 **Auth API**

## 📄 **Descripción**

Esta API de autenticación permite registrar y autenticar usuarios mediante correos electrónicos y contraseñas. El registro de usuarios está protegido por una API key configurable. La API utiliza tokens JWT para la autenticación y permite configurar CORS y base de datos a través de variables de entorno.

---

## 🏗️ **Arquitectura**

La arquitectura de esta aplicación es la siguiente:

- **Framework**: FastAPI
- **Base de datos**: SQLite (por defecto) o PostgreSQL (opcional)
- **Autenticación**: JWT (JSON Web Tokens)
- **Protección del registro**: API key
- **Contenedorización**: Docker y Docker Compose

### **Estructura del Proyecto**

```plaintext
.
├── Dockerfile
├── docker-compose.yml
├── .env
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
└── data/              # Directorio para la base de datos SQLite
```

---

## 📋 **Requisitos**

- **Docker** y **Docker Compose** instalados.
- **Python 3.10+** (opcional si no se usa Docker).

---

## ⚙️ **Instalación**

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/auth-api.git
   cd auth-api
   ```

2. **Configurar el archivo `.env`** (ver sección de Configuración).

3. **Construir y levantar el contenedor Docker**:

   ```bash
   docker-compose up --build
   ```

4. La API estará disponible en `http://localhost:8001`.

---

## 🛠️ **Configuración**

Configura las variables de entorno en el archivo `.env`:

```env
# Clave secreta para JWT
SECRET_KEY=your-very-secure-and-secret-key

# Algoritmo para JWT
ALGORITHM=HS256

# Expiración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES=30

# URL de la base de datos (SQLite por defecto)
DATABASE_URL=sqlite:///./data/auth.db
# Para PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname

# Orígenes permitidos para CORS (separados por comas)
CORS_ORIGINS=http://localhost:3000,https://my-frontend.com

# API Key para proteger el registro de usuarios
API_KEY=my-secret-api-key
```

---

## 🚀 **Uso de la API**

### **Endpoints Disponibles**

1. **Registro de Usuario (protegido por API Key)**

   - **URL**: `POST /register`
   - **Headers**: `X-API-Key: <tu-api-key>`
   - **Body** (JSON):

     ```json
     {
       "email": "user@example.com",
       "password": "password123",
       "applications": {"app1": "admin"}
     }
     ```

2. **Login de Usuario**

   - **URL**: `POST /login`
   - **Body** (JSON):

     ```json
     {
       "email": "user@example.com",
       "password": "password123"
     }
     ```

   - **Respuesta**:

     ```json
     {
       "access_token": "<jwt-token>",
       "token_type": "bearer"
     }
     ```

3. **Raíz**

   - **URL**: `GET /`
   - **Descripción**: Verifica que la API está en funcionamiento.

### **Documentación de la API**

Accede a la documentación interactiva en:

- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **Redoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)

---

## 📊 **Monitoreo**

Puedes monitorear la API con herramientas como:

- **Docker Logs**:

  ```bash
  docker-compose logs -f
  ```

- **Endpoints de Salud**: Implementar endpoints adicionales para monitoreo (`/health`).

---

## 👨‍💻 **Guía para Desarrolladores**

### **Instalación Local (sin Docker)**

1. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la API**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```

### **Estructura de Archivos**

- **`main.py`**: Configura los endpoints y CORS.
- **`auth.py`**: Maneja la autenticación, creación de tokens y validación de API keys.
- **`database.py`**: Configura la base de datos.
- **`models.py`**: Define los modelos de SQLAlchemy.
- **`schemas.py`**: Define los esquemas de Pydantic.
- **`Dockerfile`**: Configura el contenedor Docker.
- **`docker-compose.yml`**: Orquesta los servicios con Docker Compose.

---

## 🛠️ **Troubleshooting**

1. **Error de Puerto Ocupado**:

   - **Solución**: Asegúrate de que el puerto `8001` no esté en uso o cambia el puerto en `docker-compose.yml`:

     ```yaml
     ports:
       - "8002:8001"
     ```

2. **Base de Datos no Persistente**:

   - **Solución**: Asegúrate de que el volumen esté montado correctamente:

     ```yaml
     volumes:
       - ./data:/app/data
     ```

3. **API Key Inválida**:

   - **Solución**: Verifica que `API_KEY` en el `.env` coincida con el encabezado `X-API-Key` en la solicitud.

---

## 📞 **Soporte**

Para soporte técnico, contacta a:

- **Email**: joselacunzarw@gmail.com
- **GitHub Issues**: [https://github.com/tu-usuario/auth-api/issues](https://github.com/tu-usuario/auth-api/issues)

---

