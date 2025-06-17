from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv("HOST")
dbname = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
port = os.getenv("PORT")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("[SUCCESS] Conexão bem-sucedida:", result.scalar())
    except Exception as e:
        print("[ERROR] Falha na conexão com o banco:", e)
