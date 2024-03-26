from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:3215725@localhost:5432/emdiateste"

# Criar o engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criar uma instância do objeto SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
