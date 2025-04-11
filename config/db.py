from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://root:3euzgylJZMZoTv7YbLPwNQqzyFxc5QEe@dpg-cvs8bauuk2gs739os6d0-a:5432/baseprueba_68wt"

# Crear el engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear la sesión
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

from models.materiales import Material
from models.prestamos import Prestamo
import models.user as User

# Para crear tablas manualmente:
# Base.metadata.create_all(bind=engine)
