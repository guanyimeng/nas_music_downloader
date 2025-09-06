# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/download_history.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
