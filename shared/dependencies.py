from sqlalchemy.orm import Session
from shared.database import SessionLocal


# Função para obter uma sessão de banco de dados
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
