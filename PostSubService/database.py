from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# TODO: DB_URL

db_url = os.getenv("DB_URL_")
if db_url.startswith("postgres://"):  # no support for old postgres url in recent sqlalchemy versions
  db_url = db_url.replace("postgres://", "postgresql://")
SQLALCHEMY_DATABASE_URL = db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
