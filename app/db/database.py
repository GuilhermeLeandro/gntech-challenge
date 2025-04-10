from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings # Import relativo da configuração

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# O connect_args é específico para SQLite, remova se não usar SQLite
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# Engine para PostgreSQL (ou MySQL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- Dependência para obter a sessão do DB em cada request ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()