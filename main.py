from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from auth import create_access_token, create_user, authenticate_user, verify_api_key,google_login
from database import SessionLocal, engine, init_db
from models import Base
from schemas import UserCreate, LoginRequest,GoogleLoginRequest
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Leer los orígenes permitidos para CORS desde el .env
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS, # Permitir todas las solicitudes configuradas en ev (ajusta esto para mayor seguridad)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)



# Definir el contexto lifespan
@asynccontextmanager
async def lifespan(app):
    # Inicialización de la base de datos
    init_db()
    yield  # Aquí se puede añadir lógica de limpieza si es necesario



@app.get("/")
def read_root():
    return {"message": "Auth API is running!"}

# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    return create_user(db, user)

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)  # Corregido a request.email
    token = create_access_token(data={"sub": user.email, "applications": eval(user.applications)})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login/google")
def login_with_google(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    user = google_login(db, request.googleId, request.email, request.name)
    token = create_access_token(data={"sub": user.email, "applications": user.applications})
    return {"access_token": token, "token_type": "bearer"}