import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    """Создаёт таблицы в Базе Данных"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
