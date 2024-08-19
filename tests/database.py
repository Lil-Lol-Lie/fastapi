from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test"
#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#creating engine responsible for establish connection to database
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

            
client = TestClient(app)

@pytest.fixture()
def session():
    #drop tables before run new test
    Base.metadata.drop_all(bind=engine)
    #create new tables for testing
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal() #responsible for talking to database
    try:
        yield db
    finally:
            db.close()

@pytest.fixture()
def client(session):  
    def overrid_get_db():
        try:
            yield session
        finally:
                session.close()
    app.dependency_overrides[get_db] = overrid_get_db  
    yield TestClient(app)#return testclient instance