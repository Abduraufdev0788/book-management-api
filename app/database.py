from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    username=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()