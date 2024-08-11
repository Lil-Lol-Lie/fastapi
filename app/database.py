'''Use Object Relational Mapper (ORM) SQLalchemy to perform all database operations. It will translate to SQL themselves
and create tables in postgres as python models'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'# creating connection link

#creating engine responsible for establish connection to database
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#create connection or session to database or Dependency
def get_db():
    db = SessionLocal() #responsible for talking to database
    try:
        yield db
    finally:
            db.close()
            
#hile True:
#   try: #connect to postgres database
#       conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password123', cursor_factory=RealDictCursor)
#       cursor = conn.cursor()#to execute cursor statement
#       print("Connected to Database")
#       break  
#   except Exception as error:
#       print("Connecting to database failed")
#       print("Error: ", error)
#       time.sleep(2)