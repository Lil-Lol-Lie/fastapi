from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_token
from app import models
from alembic import command

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
    
@pytest.fixture
def token(test_user):
    return create_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first",
        "content": "first",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']    
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()
    return posts