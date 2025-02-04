from fastapi import HTTPException, Security
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError  # Importar desde sqlalchemy.exc
from fastapi.security import APIKeyHeader
from sqlalchemy.exc import NoResultFound
from schemas import GoogleLoginRequest, UserResponse


from models import User
from schemas import UserCreate
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
API_KEY = os.getenv("API_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definir el esquema de seguridad para la API key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, applications=str(user.applications))
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


def google_login(db: Session, google_id: str, email: str, name: str = None) -> UserResponse:
    try:
        # Buscar usuario en la base de datos por Google ID o email
        user = db.query(User).filter((User.email == email) | (User.google_id == google_id)).one()
       # if not user.is_google_account: #comentamos esto porque no tenemos el campo is_google_account cargado en la base, pero lo podemos implementar luego
       #     raise HTTPException(status_code=403, detail="Account is not linked to Google")
        return UserResponse(
            id=user.id,
            email=user.email,
            applications=eval(user.applications),
        )
    except NoResultFound:
        # Usuario no encontrado: puedes registrar automáticamente o devolver un error
        raise HTTPException(status_code=404, detail="User not found")
