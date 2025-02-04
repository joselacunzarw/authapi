import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Leer la URL de la base de datos desde el archivo .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/auth.db")

# Crear el directorio si no existe
db_path = DATABASE_URL.replace("sqlite:///", "")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Crear las tablas si no existen
def init_db():
    Base.metadata.create_all(bind=engine)
