from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)  # Puede ser nulo para usuarios de Google
    google_id = Column(String, unique=True, nullable=True)  # ID único de Google
    is_google_account = Column(Boolean, default=False)  # Indica si es usuario de Google
    applications = Column(String)  # Roles y aplicaciones del usuario como JSON
