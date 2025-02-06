import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}',
    echo=False,
    pool_size=50,
    max_overflow=10,
    pool_timeout=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 10,
        "charset": "utf8mb4"
    }
)

Session = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    """Yield a database session to the caller. The session is closed after the caller is done with it
    :returns: active database session
    :rtype: sqlalchemy.orm.session.Session
    """
    try:
        session = Session()
        yield session
    finally:
        session.close()

def initialise_all_tables():
    """Initialise all tables in the database"""
    Base.metadata.create_all(engine)
